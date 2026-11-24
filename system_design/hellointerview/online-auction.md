---
layout: simple
title: "Design an Online Auction — Hello Interview Style"
permalink: /system_design/hellointerview/online-auction
---

# Online Auction

**Patterns:** Dealing with Contention · Real-time Updates  
**Difficulty:** Medium  
**Source:** hellointerview.com (AI-generated full solution)

---

## Understanding the Problem

🛍️ **What is an Online Auction?**  
An online auction lets users list items for sale while others compete by placing bids that must exceed the current highest bid. The auction runs until its end date, at which point the highest bidder wins.

---

### Functional Requirements

**Core Requirements**

- Users should be able to post an item for auction with a starting price and end date
- Users should be able to bid on an item — bids are accepted only if higher than the current highest bid
- Users should be able to view an auction, including the current highest bid

**Below the line (out of scope):**

- Searching or filtering items
- Payment processing (assume separate system)
- Buyer/seller messaging
- Auction history

### Non-Functional Requirements

**Core Requirements**

- The system should ensure strong consistency for bids (no two users win the same auction)
- The system should be highly available
- The system should scale to 10M concurrent auctions
- The system should display the current highest bid in real-time (< 1s lag)
- The system should be durable — no bids should be lost

**Below the line (out of scope):**

- Sub-millisecond bid response (< 500ms is fine)

### Constraints & Estimates

- 10M concurrent auctions
- Peak bidding: assume 100 bids/sec per hot auction; most auctions see 1 bid/min
- Average: 10M auctions × 1 bid/min = ~167K bids/sec globally
- Hot auctions (sniping in last seconds): up to 10K bids/sec on a single item
- Each bid record: ~200 bytes
- Auction record: ~1KB

---

## The Set Up

### Defining the Core Entities

- **Auction** – id, seller_id, title, description, starting_price, current_highest_bid, highest_bidder_id, end_time, status (active/ended)
- **Bid** – id, auction_id, bidder_id, amount, placed_at
- **User** – id, name, email

### API or System Interface

```
// Create an auction
POST /auctions
{ "title": "Vintage Watch", "starting_price": 100.00, "end_time": "2024-12-01T18:00:00Z", "description": "..." }
-> { auction_id, status: "active" }

// Place a bid
POST /auctions/{auction_id}/bids
{ "amount": 150.00 }
-> { bid_id, accepted: true, current_highest: 150.00 }
  | { accepted: false, reason: "Bid too low", current_highest: 175.00 }

// Get auction details (current state)
GET /auctions/{auction_id}
-> { auction, current_highest_bid, time_remaining_seconds }

// Subscribe to real-time bid updates (SSE)
GET /auctions/{auction_id}/stream
-> Server-Sent Events: { event: "new_bid", amount: 160.00, bidder: "user_x", ts: ... }
```

---

## High-Level Design

### 1) Users should be able to post an item for auction

Simple CRUD operation:
1. POST `/auctions` → **Auction Service** validates input (end_time must be in the future, price > 0)
2. Write auction record to **PostgreSQL** with `status=active`, `current_highest_bid=starting_price`
3. Schedule an **Auction Expiry Job** (via cron or delayed job queue) to close the auction at `end_time`
4. Return `auction_id`

**Auction table:**
```sql
CREATE TABLE auctions (
  id                UUID PRIMARY KEY,
  seller_id         UUID NOT NULL,
  title             TEXT NOT NULL,
  starting_price    DECIMAL(12,2) NOT NULL,
  current_highest_bid DECIMAL(12,2) NOT NULL,
  highest_bidder_id UUID,
  end_time          TIMESTAMP NOT NULL,
  status            TEXT DEFAULT 'active',  -- active | ended | cancelled
  version           INT DEFAULT 0,  -- optimistic lock version
  created_at        TIMESTAMP DEFAULT NOW()
);
```

### 2) Users should be able to bid on an item

**The core challenge:** Multiple users bid simultaneously. Without care, two users can both read `current_highest_bid = 100`, both validate their `150` bid as winning, both write → **phantom win** (data corruption).

**Naive approach (broken):**
```
READ current_highest_bid = 100
IF 150 > 100: accept bid
WRITE current_highest_bid = 150
```

This has a classic TOCTOU (time-of-check-time-of-use) race condition.

**Solution: Optimistic Locking (database-level)**

Use a `version` column. The UPDATE only succeeds if the version matches what was read:

```sql
BEGIN;
-- Read current state
SELECT current_highest_bid, version FROM auctions WHERE id = :auction_id;
-- Validate in application: if bid_amount <= current_highest_bid, reject

-- Atomic update with version check
UPDATE auctions
SET current_highest_bid = :bid_amount,
    highest_bidder_id = :bidder_id,
    version = version + 1
WHERE id = :auction_id
  AND version = :read_version
  AND current_highest_bid < :bid_amount
  AND status = 'active'
  AND end_time > NOW();

-- Rows affected = 0 → concurrent update detected, retry or reject
INSERT INTO bids (id, auction_id, bidder_id, amount, placed_at) VALUES (...);
COMMIT;
```

If `UPDATE` affects 0 rows: another bid arrived concurrently. Return 409 Conflict with the latest `current_highest_bid` so the client can re-evaluate.

**Alternative: Pessimistic Locking**

```sql
SELECT ... FROM auctions WHERE id = :id FOR UPDATE;  -- acquires row lock
-- validate + update safely
-- lock released on COMMIT
```

Simpler logic, but serializes all bids for the same auction → lower throughput. Good for hot auctions with high contention.

### 3) Users should be able to view an auction

Standard read path:
1. `GET /auctions/{id}` → **Auction Service**
2. Check **Redis cache** (TTL: 5s) for auction state
3. Cache miss → fetch from PostgreSQL
4. Return auction + `current_highest_bid`

Short TTL (5s) means displays can lag by up to 5 seconds — acceptable for most auctions. For near-real-time, use SSE push (see Deep Dive #3).

---

## Potential Deep Dives

### 1) How can we ensure strong consistency for bids?

The optimistic locking approach above is the right starting point. Let's examine alternatives for high-contention scenarios:

**Problem at scale:** A popular auction (e.g., rare sneakers) has 10,000 users bidding in the final 10 seconds. With optimistic locking, most bids will fail the version check and need to be retried or rejected. This is high CPU churn.

**Solution: Single-writer serialization per auction**

Route all bids for a given `auction_id` to a **single Bid Processor** instance (like a virtual actor):

```
Client → API Server → Kafka (partitioned by auction_id) → Bid Processor (1 per partition)
```

Each Bid Processor handles bids for its assigned auctions sequentially:
1. Read current highest bid (in-memory, no DB round-trip)
2. Validate new bid
3. Update in-memory state
4. Write accepted bid to DB asynchronously (batch writes)

**Benefits:**
- Zero contention — bids for the same auction are processed serially
- No optimistic lock retries
- In-memory state = microsecond validation

**Trade-off:** Bid Processor is stateful. On crash, need to reload auction state from DB. Use Kafka consumer offsets to know where to resume.

This is essentially the **actor model** (Erlang/Akka) or **Kafka Streams stateful processing**.

### 2) How can we ensure the system is fault tolerant and durable?

**Bid durability:**
- All accepted bids written to PostgreSQL before returning success to client
- PostgreSQL WAL (Write-Ahead Log) ensures durability even on crash
- Multi-region replica for disaster recovery

**Auction state durability:**
- If using in-memory Bid Processor: periodically checkpoint `current_highest_bid` to Redis (every 100ms) and DB (every 1s)
- On restart: load last checkpoint from DB, replay Kafka messages since checkpoint

**Auction expiry reliability:**
- Don't rely on a single cron job — use a distributed scheduler (Kafka delayed messages, or a job queue like BullMQ/Sidekiq)
- Auction expiry worker: at `end_time`, mark auction `status=ended`, declare winner, trigger notification
- Idempotent: even if fired multiple times, only transition from `active → ended` once (compare-and-swap on status)

### 3) How can we ensure the system displays the current highest bid in real-time?

**Server-Sent Events (SSE) for bid streaming:**

1. When a user views an auction page, browser opens SSE connection: `GET /auctions/{id}/stream`
2. **Bid Streaming Service** subscribes to Redis Pub/Sub channel `auction:{id}:bids`
3. When a bid is accepted: Bid Service publishes `{ amount, bidder_anonymous_id, ts }` to Redis Pub/Sub
4. Bid Streaming Service fans out to all SSE subscribers for that auction

**Scale:** A popular auction might have 100K concurrent viewers.
- 100K SSE connections per auction → too many for one server
- Use multiple Bid Streaming Service instances; all subscribe to the same Redis Pub/Sub channel
- Each instance handles a subset of SSE connections
- Redis Pub/Sub broadcasts to all subscriber instances → they fan out to their connections

```
Bid accepted
  → Redis Pub/Sub publish("auction:123:bids", bid_event)
  → Streaming Server 1 (50K connections) → push to viewers
  → Streaming Server 2 (50K connections) → push to viewers
```

**Alternative:** WebSocket instead of SSE — bidirectional, but more complex. For read-only feed, SSE is simpler.

### 4) How can we ensure the system scales to support 10M concurrent auctions?

**Sharding by auction_id:**

- Partition auctions across multiple DB shards (shard key: auction_id)
- Each shard handles ~1M auctions
- Route `auction_id` to correct shard via consistent hashing

**Stateless API servers:** Horizontally scale behind a load balancer. All state in DB + Redis.

**Redis for hot auction state:**
- Cache `current_highest_bid` per auction in Redis
- Reduces DB reads for GET auction requests
- Write-through cache: update Redis + DB atomically

**Kafka partitioning for bid processing:**
- Partition Kafka by `auction_id`
- Each partition → one Bid Processor
- Scale partitions = scale throughput linearly

**Back-of-envelope:**
- 10M auctions × avg 1 bid/min = 167K bids/sec
- With 100 Kafka partitions, each partition handles ~1,670 bids/sec → manageable

---

## Final Design

```
Client
  │
  ├─ [Create Auction] POST /auctions ──→ Auction Service ──→ PostgreSQL
  │                                   └──→ Job Queue (schedule expiry)
  │
  ├─ [Place Bid] POST /bids ──→ API Server ──→ Kafka (partitioned by auction_id)
  │                                            → Bid Processor (serial per auction)
  │                                              ├─ Validate (in-memory highest bid)
  │                                              ├─ Write to PostgreSQL (bids + auction update)
  │                                              └─ Publish to Redis Pub/Sub
  │
  ├─ [View Auction] GET /auctions/{id} ──→ API Server ──→ Redis cache ──→ PostgreSQL
  │
  └─ [Live Updates] GET /stream ──→ Bid Streaming Service (SSE)
                                   └─ Subscribe Redis Pub/Sub → push to viewers

Auction Expiry Worker
  - Polls job queue for expired auctions
  - Marks status=ended, declares winner
  - Triggers notifications
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entity design and REST APIs
- Identifies the race condition in bid validation
- Proposes database transactions to resolve it
- Simple polling or SSE for live updates

### Senior
- Optimistic locking with version column
- Pessimistic locking trade-offs for high contention
- Redis cache with short TTL for auction reads
- SSE with Redis Pub/Sub for real-time updates

### Staff
- Single-writer Bid Processor (actor model) via Kafka partitioning for extreme contention
- Checkpoint + replay strategy for Bid Processor fault tolerance
- Detailed sharding strategy for 10M auctions
- Idempotent auction expiry with distributed job scheduler
- Discusses fan-out at scale for 100K viewers on popular auctions
