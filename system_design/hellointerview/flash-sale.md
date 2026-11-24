---
layout: simple
title: "Design a Flash Sale System — Hello Interview Style"
permalink: /system_design/hellointerview/flash-sale
---

# Flash Sale

**Patterns:** Real-time Updates · Dealing with Contention · Scaling Writes  
**Difficulty:** Hard  
**Source:** hellointerview.com (AI-generated full solution)

---

## Understanding the Problem

👟 **What is a Flash Sale?**  
Nike releases 10,000 pairs of a limited-edition shoe at noon. Tens of millions of users try to buy simultaneously. Our job: ensure inventory is never oversold, purchases are fair, and the system doesn't melt under extreme demand.

---

### Functional Requirements

**Core Requirements**

- Users can view the flash sale item (product details, inventory count, sale start time)
- Users can secure/reserve an available unit for a limited time while the sale is active
- Users who secure a unit can complete payment to purchase it

**Below the line (out of scope):**

- Browsing or searching the broader product catalog
- Managing shipping, returns, refunds, or order history
- Administrators creating or configuring flash sales

### Non-Functional Requirements

**Core Requirements**

- The system must **never oversell** — inventory count must never go below 0
- Reservations should be held for a limited time (e.g., 10 minutes) — expired reservations must be released
- The system should handle **tens of millions of concurrent users** arriving simultaneously
- The system should be **fair** — users who arrive first should have a better chance of securing inventory

**Below the line (out of scope):**

- Exactly-once payment processing (handled by separate payment system)

### Constraints & Estimates

- 10,000 units of inventory
- 10M–50M users attempting to buy within the first few seconds
- Extreme write contention: all 10M users try to decrement the same counter simultaneously
- Reservation TTL: 10 minutes
- After 10 min, unsold reserved units return to inventory (for failed payments)
- Sale duration: typically 10–60 minutes

---

## The Set Up

### Planning the Approach

The key insight the problem statement gives us: we need a **reservation step** between viewing the product and completing payment. Without it:
- Payment takes 3–10 seconds (external call to bank)
- During that time, inventory must be held — can't hold open DB transactions for 10M users

Three distinct phases:
1. **Sale page** – serve product info at massive scale (CDN + caching)
2. **Reservation** – decrement inventory atomically, hold unit for user
3. **Payment** – complete purchase within reservation window

### Defining the Core Entities

- **SaleItem** – id, product_id, name, description, price, total_inventory, sold_count, sale_starts_at, sale_ends_at, status (upcoming/active/ended)
- **Reservation** – id, sale_item_id, user_id, status (active/completed/expired/cancelled), reserved_at, expires_at
- **Order** – id, reservation_id, user_id, sale_item_id, payment_status, created_at

### API or System Interface

```
// View flash sale item
GET /sales/{sale_id}
-> { item: { name, price, inventory_remaining, sale_starts_at, status }, user_has_reservation: bool }

// Secure a reservation (called at sale start by user)
POST /sales/{sale_id}/reserve
-> { reservation_id, expires_at: "2024-12-01T12:10:00Z" } (success)
 | { error: "sold_out" }
 | { error: "already_reserved" }

// Complete payment (within reservation window)
POST /reservations/{reservation_id}/purchase
{ "payment_method_id": "pm_xxx" }
-> { order_id, status: "confirmed" }
 | { error: "reservation_expired" }

// Cancel reservation
DELETE /reservations/{reservation_id}
-> { status: "cancelled" }
```

---

## High-Level Design

### 1) Users can view the flash sale item

**Scale challenge:** 50M users hitting the sale page in the seconds before sale start = massive read spike.

**Solution: CDN + aggressive caching**

```
Client → CDN (CloudFront) → [cache miss] → API Server → Redis → PostgreSQL
```

- Sale item details (name, price, description, images) are **static** — cache at CDN with TTL 60s
- During active sale, `inventory_remaining` changes rapidly — **don't show real-time inventory on the page** (too expensive to serve live counts at this scale)
- Instead: show "Available" or "Sold Out" (binary), updated every 30 seconds via CDN cache bust

**Pre-warming the cache:**
- 1 hour before sale start, push sale page content to CDN edge nodes globally
- Zero cache misses at sale start → no origin server load for page views

### 2) Users can secure/reserve an available unit

**This is the critical path — where contention is extreme.**

**Naive approach (broken):**
```
READ inventory_remaining = 10000
IF inventory_remaining > 0:
  inventory_remaining -= 1
  CREATE reservation
```
Classic race condition: 10M users all read `10000`, all pass the check, 10M reservations created → oversell.

**Solution: Redis DECR + Lua Script (atomic)**

Before the sale starts, pre-load inventory into Redis:
```
SET sale:{sale_id}:inventory 10000
```

Reservation attempt:
```lua
-- Atomic Lua script (runs as a single Redis command, no race conditions)
local inventory = tonumber(redis.call('GET', KEYS[1]))
if inventory == nil or inventory <= 0 then
    return -1  -- sold out
end
redis.call('DECR', KEYS[1])
return inventory - 1  -- remaining count
```

Since Redis is **single-threaded**, `DECR` is atomic — no two users can decrement simultaneously and get the same result. Oversell is impossible at the Redis layer.

**Full reservation flow:**
1. User calls `POST /sales/{sale_id}/reserve`
2. API Server checks: user doesn't already have an active reservation (Redis `SISMEMBER reservations:{sale_id} {user_id}`)
3. Execute Redis Lua script: attempt DECR
4. If DECR successful (returned ≥ 0):
   - Write Reservation to PostgreSQL: `{ user_id, sale_item_id, status=active, expires_at = now + 10min }`
   - Add user to Redis set: `SADD reservations:{sale_id} {user_id}` (prevent duplicate reservations)
   - Return `{ reservation_id, expires_at }`
5. If DECR returned -1: return `{ error: "sold_out" }`

### 3) Users who secure a unit can complete payment

**Payment flow:**
1. User submits payment within 10-minute window
2. `POST /reservations/{id}/purchase`
3. API Server:
   - Verify reservation exists, status=active, not expired
   - Call Payment Service (external, e.g., Stripe) → may take 3–10 seconds
   - On payment success: update reservation `status=completed`, create Order record
   - On payment failure: reservation still active until expiry (user can retry)
4. Return `{ order_id, status: "confirmed" }`

**Why reservation TTL matters:** If user abandons the checkout, the reservation expires in 10 minutes → Redis inventory counter is **not** automatically restored (see Deep Dive #2).

---

## Potential Deep Dives

### 1) How do we maintain consistency under extreme contention?

**Three-layer consistency approach:**

**Layer 1: Redis (fast gate)**
- Redis DECR atomic operation is the primary inventory gate
- 50M requests → Redis single-threaded → serialized at ~1M ops/sec → first 10,000 get through; rest get `sold_out` immediately
- Redis is the first line of defense: rejects the vast majority of requests in microseconds

**Layer 2: PostgreSQL (source of truth)**
- `sold_count` column tracks sold units
- Constraint: `sold_count <= total_inventory` (enforced by DB trigger or application check)
- If Redis fails or is out of sync: DB is the fallback
  
**Layer 3: Reconciliation**
- Background job every 5 minutes: compare Redis inventory count with `total_inventory - COUNT(active reservations)` from PostgreSQL
- If mismatch (Redis says 50 remaining but DB says 100 reserved out of 10,000): reset Redis from DB
- This handles Redis crash/restart scenarios

**What if Redis crashes during the sale?**
- Redis crashes: inventory counter is gone
- Sale must be paused (return 503) until Redis is restored
- Restore Redis from DB: `SET sale:{id}:inventory {total_inventory - completed_orders - active_reservations}`
- Resume sale
- With Redis Cluster (AOF persistence): recovery in < 30 seconds

### 2) How do we efficiently release expired reservations?

**Problem:** 50M users rush in. 10,000 get reservations. 90% of those don't complete payment (many are bots, many are "just checking"). We need to release those 9,000 expired reservations so real buyers can get them.

**Approach: Reservation TTL tracking + background sweeper**

**Redis Sorted Set for expiry tracking:**
```
ZADD reservations:expiry {expires_at_unix} {reservation_id}
```

On reservation creation: add to this sorted set with expiry timestamp.

**Expiry sweeper (runs every 30 seconds):**
```python
expired = redis.zrangebyscore('reservations:expiry', 0, time.time())
for reservation_id in expired:
    # Atomically:
    db.execute("UPDATE reservations SET status='expired' WHERE id=? AND status='active'", reservation_id)
    if rows_affected > 0:
        redis.incr(f'sale:{sale_id}:inventory')  # restore inventory
    redis.zrem('reservations:expiry', reservation_id)
    redis.srem(f'reservations:{sale_id}', reservation_id)  # allow user to try again
```

**Why not rely on Redis TTL alone?** Redis key expiry is approximate (can be delayed). We need precise expiry for inventory accounting. The sorted set approach gives exact control.

**Cascading effect:** As reservations expire and inventory is restored, users polling the sale page see "Available" again → second wave of buyers → more reservations → potentially all 10,000 units are actually sold (not just held).

### 3) How do we handle millions of users arriving at once?

**The thundering herd problem:** At exactly noon, 50M users simultaneously:
1. Load the sale page
2. Click "Buy Now"
3. Hammer the reserve endpoint

**Solutions:**

**A) CDN absorbs page load spike**
- Sale page, images, and product info cached at CDN globally
- 50M page views → CDN handles ~100% → 0 origin server load for page content

**B) Virtual waiting room (queue)**
- Users who arrive at or just before sale start enter a **virtual queue**
- Each user gets a position number (Redis INCR) and is told their estimated wait time
- System releases users into the actual reservation flow in batches (e.g., 1,000 users/second)
- Prevents thundering herd on the reservation endpoint

**Virtual queue implementation:**
```
User arrives → POST /sales/{id}/queue
  → Redis INCR sale:{id}:queue_position → returns queue_pos
  → User shown: "You're #42,381 in line. Estimated wait: 42 seconds"
  → WebSocket/SSE connection: server pushes "it's your turn" when queue_pos ≤ released_count

Queue Manager (runs every 1 second):
  → Redis INCR sale:{id}:released_count BY 1000
  → Notify users with queue_pos ≤ released_count: "Proceed to checkout"
```

**C) Bot filtering**
- Rate limit by IP: max 1 reserve request per user per second
- Require valid session token (CAPTCHA at queue entry if suspicious)
- Fingerprint-based dedup: device fingerprint + user ID prevents one user from holding multiple reservations with different accounts

**D) API server autoscaling**
- Pre-scale before sale start: Kubernetes scales pods 30 minutes before `sale_starts_at`
- Target: 5,000 API pods × 1,000 req/sec each = 5M req/sec capacity (handle the burst)

### 4) How do we make access to limited inventory fair?

**The fairness problem:** With 50M users and 10,000 units, how do we ensure it's not purely luck-of-the-network? Those with the fastest internet connections / closest to the data center shouldn't have an inherent advantage.

**Virtual queue (from Deep Dive #3) is the primary fairness mechanism:**
- Queue position assigned on arrival time — first-come, first-served
- Deterministic: position 1–10,000 get inventory; position 10,001+ wait for cancellations
- Fairer than pure race-to-the-DB (where network speed determines winner)

**Anti-gaming measures:**
- One reservation per user (enforced by Redis set + DB constraint)
- Reservation non-transferable
- Payment required within 10 minutes — no speculative holding

**Lottery for extreme demand:**
- For the most hyped releases (10M demand for 100 units), pure queue may still favor bots/fast-connection users who queue up earliest
- Alternative: **lottery system** — users register in a 24-hour window; winners randomly selected at sale time
- Nike and Nike SNKRS app use this model for the most limited releases

---

## Final Design

```
Client
  │
  ├─ [View Sale] GET /sales/{id} ──→ CDN (cached, TTL 60s)
  │                                  → API Server → Redis (inventory count) → PostgreSQL
  │
  ├─ [Join Queue] POST /queue ──→ Queue Service
  │                               → Redis INCR (queue_pos)
  │                               → SSE connection (notified when "your turn")
  │
  ├─ [Reserve] POST /reserve ──→ API Server
  │  (triggered when "your turn")  → Redis: DECR inventory (Lua, atomic)
  │                                → Check duplicate (SISMEMBER)
  │                                → PostgreSQL: INSERT reservation
  │                                → Redis: ZADD expiry sorted set
  │                                → Return { reservation_id, expires_at }
  │
  └─ [Purchase] POST /purchase ──→ API Server
                                   → Verify reservation active + not expired
                                   → Call Payment Service (Stripe)
                                   → UPDATE reservation status=completed
                                   → CREATE order record

Background Workers:
  Expiry Sweeper (every 30s)
    → ZRANGEBYSCORE expiry sorted set → expired reservations
    → Mark expired + INCR Redis inventory (restore)
    → Allow user to re-queue

Queue Manager (every 1s)
    → INCR released_count
    → Notify users at front of queue via SSE/WebSocket
```

---

## What is Expected at Each Level?

### Mid-level
- Identifies the race condition (needs atomic inventory decrement)
- Proposes Redis DECR for atomic inventory check
- Understands why reservation step is needed (payment takes time)
- Basic expiry (time-based TTL)

### Senior
- Redis Lua script for atomic reserve-or-fail
- Reservation expiry sorted set + sweeper (restore inventory)
- CDN caching for sale page load spike
- One-reservation-per-user enforcement
- Pre-scaling API servers before sale start

### Staff+
- Virtual waiting room (queue) for fairness + thundering herd protection
- Three-layer consistency (Redis → PostgreSQL → reconciliation)
- Redis crash recovery path (AOF persistence + restore from DB)
- Bot detection (rate limiting, device fingerprint, CAPTCHA)
- Lottery system for extreme demand scenarios
- Discusses CAP theorem: AP system (availability over consistency) with Redis as the fast gate
