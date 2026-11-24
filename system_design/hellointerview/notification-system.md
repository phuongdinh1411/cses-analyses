---
layout: simple
title: "Design a Notification System — Hello Interview Style"
permalink: /system_design/hellointerview/notification-system
---

# Notification System

**Patterns:** Multi-step Processes · Scaling Writes  
**Difficulty:** Medium  
**Source:** hellointerview.com (AI-generated full solution)

---

## Understanding the Problem

🔔 **What is a Notification System?**  
An internal platform that other teams use to send messages to users across channels (push, email, SMS). Product services hand it a message and recipient — the platform handles delivery. Clients include the auth service (OTP), marketing (promo blasts), and product (order confirmations).

---

### Functional Requirements

**Core Requirements**

- Upstream services should be able to send a notification to a user via push, email, or SMS — immediately or scheduled
- Upstream services should be able to send campaigns (same message to a whole segment of users), immediately or scheduled
- Users should be able to set notification preferences (channel opt-outs and quiet hours)

**Below the line (out of scope):**

- Template management and rich content authoring
- Delivery analytics dashboards (open rates, click-through)
- In-app notification feeds and badge counts
- Frequency capping across notification types

### Non-Functional Requirements

**Core Requirements**

- An accepted notification must **never be dropped** (at-least-once delivery)
- High-priority notifications (OTP, security alerts) should be delivered within **5 seconds**
- Campaign blasts can sustain **5,000 notifications/second**
- Duplicate notifications must be prevented (idempotent delivery)

**Below the line (out of scope):**

- Exactly-once delivery guarantee (at-least-once + deduplication is the standard)

### Constraints & Estimates

- 10M notifications/day at steady state → ~115/sec baseline
- Peak campaign: 1M messages delivered in < 5 min → **3,333/sec peak**
- Design for **5,000/sec** to handle multiple concurrent campaigns
- Each notification: ~500 bytes of payload
- 5,000 × 500B = 2.5MB/sec ingestion — trivial; bottleneck is provider rate limits

---

## The Set Up

### Defining the Core Entities

- **Notification** – id, user_id, channel (push/email/sms), subject, body, scheduled_at, status (pending/sent/failed), idempotency_key
- **Campaign** – id, name, segment_query (or segment_id), template, scheduled_at, status, sent_count
- **UserPreferences** – user_id, opt_out_channels (array), quiet_hours_start, quiet_hours_end, timezone
- **DeliveryLog** – notification_id, provider, attempt_count, delivered_at, error

### API or System Interface

```
// Send a single notification (called by upstream services)
POST /notifications
{
  "user_id": "user_123",
  "channel": "push",        // push | email | sms | auto
  "subject": "Your OTP",
  "body": "Your code is 123456",
  "priority": "high",       // high | normal
  "scheduled_at": null,     // null = immediate
  "idempotency_key": "otp-user_123-20241201-083000"
}
-> { notification_id, status: "accepted" }

// Send a campaign blast
POST /campaigns
{
  "segment": "users:premium",   // segment identifier or user_ids list
  "template_id": "promo_holiday_2024",
  "channel": "email",
  "scheduled_at": "2024-12-01T09:00:00Z"
}
-> { campaign_id, estimated_recipients: 1000000 }

// Update user preferences
PUT /users/{user_id}/preferences
{
  "opt_out_channels": ["sms"],
  "quiet_hours_start": "22:00",
  "quiet_hours_end": "08:00",
  "timezone": "America/New_York"
}
-> { status: "updated" }
```

---

## High-Level Design

### 1) Upstream services should be able to send a notification to a user (immediately or scheduled)

**Pipeline for a single notification:**

```
Upstream Service → POST /notifications
  → Notification API (validates, checks preferences)
  → Persist to DB (status=pending)
  → Kafka ("notifications-high" or "notifications-normal")
  → Delivery Worker
    → Resolve channel (or pick best channel if "auto")
    → Check user preferences (opt-outs, quiet hours)
    → Call provider (FCM for push, SendGrid for email, Twilio for SMS)
    → Update status (sent/failed)
    → Log to DeliveryLog
```

**Channel selection ("auto" mode):**
Priority: Push → Email → SMS
- If user has a valid push token: use push (free, instant)
- Else if email: use email
- Else: SMS (most expensive)

**Scheduled notifications:**
- Store with `scheduled_at` timestamp and `status=pending`
- Scheduler polls every 10s: `SELECT * FROM notifications WHERE scheduled_at <= NOW() + 10s AND status = 'pending' FOR UPDATE SKIP LOCKED`
- Dispatch to Kafka when due

### 2) Upstream services should be able to send campaigns to segments

**Campaign fan-out challenge:** A campaign to 1M users cannot be a single DB row. We need to expand the segment into individual notification deliveries without overwhelming the system.

**Campaign expansion pipeline:**

```
Campaign created (or scheduled time arrives)
  → Campaign Worker reads campaign record
  → Queries segment (e.g., "all premium users"):
       SELECT user_id FROM users WHERE tier = 'premium'  -- returns 1M user_ids
  → Batch into groups of 1,000 user_ids
  → Publish 1,000 batch messages to Kafka("campaign-jobs")
  → Delivery Workers process each batch:
       For each user_id in batch:
         - Resolve user's preferred channel + preferences
         - Call provider API
         - Log delivery
```

**Why batch?** Processing 1M individual Kafka messages is fine, but batching reduces Kafka overhead and allows bulk API calls to providers (some support batch send).

**Progress tracking:**
- Campaign record tracks `sent_count` (atomic increment via Redis INCR)
- Status transitions: `scheduled → running → completed`

### 3) Users should be able to set notification preferences

**Preferences service (read-heavy):**
- Stored in PostgreSQL (`user_preferences` table)
- Heavily cached in Redis (TTL: 5 min) — read on every notification dispatch
- Key: `prefs:{user_id}` → `{ opt_out_channels, quiet_hours_start, quiet_hours_end, tz }`

**Quiet hours logic (delivery worker):**
```python
def should_deliver(user_prefs, channel, now):
    if channel in user_prefs.opt_out_channels:
        return False
    user_time = convert_to_user_timezone(now, user_prefs.timezone)
    if is_in_quiet_hours(user_time, user_prefs.quiet_hours_start, user_prefs.quiet_hours_end):
        if notification.priority == 'high':
            return True  # OTPs always delivered
        return False  # reschedule for end of quiet hours
    return True
```

---

## Potential Deep Dives

### 1) How do we guarantee an accepted notification is never dropped?

**At-least-once delivery via durable queue + status tracking:**

The key insight: once we write the notification to our DB with `status=pending`, we own it. We must deliver it or explicitly mark it failed after retries.

**Durable pipeline:**
1. `POST /notifications` → write to DB (status=pending) → publish to Kafka → return `accepted`
2. Kafka retains messages until consumer commits offset → no loss from consumer crash
3. Delivery worker: process → call provider → on success: commit Kafka offset + update status to `sent`
4. On provider failure: **don't commit offset** → Kafka re-delivers to another worker

**Retry with exponential backoff:**
```
Attempt 1: immediate
Attempt 2: 1 min
Attempt 3: 5 min
Attempt 4: 30 min
After 4 failures: status = 'failed', alert ops team
```

**Provider failover:**
- Keep 2 providers per channel (primary + backup): SendGrid + Amazon SES for email
- If primary fails (rate limit, outage): switch to backup automatically
- Delivery worker rotates providers on failure

**Dead Letter Queue (DLQ):**
- After N retries: move to DLQ Kafka topic
- Alert + manual review for critical notifications

### 2) How do we deliver high-priority notifications within 5 seconds, even during a campaign blast?

**Problem:** A marketing campaign blasting 1M emails floods Kafka. Meanwhile, a critical OTP needs to be delivered NOW. The OTP sits behind 1M campaign messages in the same queue → takes minutes to process.

**Solution: Separate priority queues**

```
Kafka topics:
  notifications-high      (OTP, security, transactional)
  notifications-normal    (marketing, campaign, reminders)

Delivery Workers:
  - High-priority workers: dedicated pool (20 workers), ONLY consume notifications-high
  - Normal-priority workers: large autoscaling pool, consume notifications-normal
```

High-priority workers are never congested by campaigns. OTP notification → `notifications-high` → one of 20 dedicated workers → provider call → delivered in < 2s typically.

**Campaign Kafka partitioning:**
- Campaign batch messages on `notifications-normal` have many partitions (100+)
- Autoscale workers: Kubernetes HPA based on consumer lag
- Target: drain 1M notifications in < 5 min → need 3,333/sec throughput
- Assuming 10ms per send: 1 worker handles 100 sends/sec → need 33 workers minimum → autoscale up to 200 workers during blasts

### 3) How do we prevent duplicate notifications on top of at-least-once delivery?

**Problem:** At-least-once delivery means the same notification can be processed twice (network timeout: provider received it but we didn't get the 200 OK → retry → user gets 2 OTPs).

**Solution: Idempotency key + deduplication table**

**Caller provides idempotency key:**
```json
{ "idempotency_key": "otp-user_123-20241201-083000" }
```

**Deduplication at ingest:**
```sql
-- UNIQUE constraint on idempotency_key
INSERT INTO notifications (id, ..., idempotency_key)
VALUES (...)
ON CONFLICT (idempotency_key) DO NOTHING
RETURNING id;
-- If 0 rows returned: duplicate request, return existing notification_id
```

**Provider-level deduplication:**
- Many providers (FCM, SendGrid) support idempotency keys on their API calls
- Pass our `notification_id` as the provider's idempotency key
- Provider deduplicates at their end too

**Delivery tracking table:**
```sql
CREATE TABLE delivery_log (
  notification_id  UUID,
  provider         TEXT,
  delivered_at     TIMESTAMP,
  PRIMARY KEY (notification_id, provider)
);
-- Before calling provider, check if already delivered:
SELECT 1 FROM delivery_log WHERE notification_id = :id AND provider = :provider;
```

**Two-phase commit alternative (for critical notifications):**
1. Record "delivery attempt started" in delivery_log
2. Call provider
3. Record "delivery confirmed"
If step 3 fails: on retry, see step 1 exists → check provider status before re-sending

---

## Final Design

```
Upstream Services (auth, marketing, product)
  ↓ POST /notifications or POST /campaigns
Notification API
  ├─ Validate + persist (PostgreSQL)
  ├─ Check idempotency (UNIQUE constraint)
  └─ Publish to Kafka:
       notifications-high    (OTP, security)
       notifications-normal  (marketing, campaigns)

Campaign Worker
  - Expand segment → 1M user batches
  - Publish to notifications-normal (Kafka)

                         ┌─────────────────────────────────────────────┐
Kafka Topics             │  High-priority (20 dedicated workers)        │
  notifications-high ───→│  → Check prefs (Redis) → provider → log     │
  notifications-normal ─→│  Normal (200 autoscaled workers)             │
                         └─────────────────────────────────────────────┘
                                  ↓                   ↓               ↓
                              FCM/APNs           SendGrid/SES      Twilio
                              (Push)              (Email)           (SMS)

User Preferences Service
  → PostgreSQL (source of truth)
  → Redis cache (TTL 5 min, read on every delivery)

Scheduler
  - Polls for scheduled notifications / campaigns
  - Dispatches when due
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entities and API design (single notification + campaign)
- Kafka as delivery queue
- User preference opt-outs
- Basic retry on failure

### Senior
- Separate high/normal priority Kafka topics for SLA isolation
- Idempotency key deduplication at ingest + provider level
- Campaign fan-out with batching
- Provider failover strategy
- Quiet hours with timezone handling

### Staff+
- Autoscaling worker pool based on Kafka consumer lag
- Dead Letter Queue + alerting for failed notifications
- Campaign progress tracking (Redis INCR for sent_count)
- Delivery analytics pipeline (Kafka → ClickHouse for open rates)
- Rate limiting per provider (providers have per-second limits, need token bucket)
