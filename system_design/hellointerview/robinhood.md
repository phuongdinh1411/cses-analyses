---
layout: simple
title: "Design Robinhood — Hello Interview Style"
permalink: /system_design/hellointerview/robinhood
---

# Robinhood

**Patterns:** Real-time Updates  
**Difficulty:** Hard  
**Source:** hellointerview.com (AI-generated full solution)

---

## Summary

- **Key challenge:** Fan out live prices to 5M concurrent users (~10K trades/sec → ~10M pushes/sec) in < 1s, while orders stay strongly consistent and durable.
- **Core design:** Price Feed Service caches exchange trades in Redis and publishes to per-symbol Pub/Sub channels that WebSocket servers push to clients; Order Service writes orders to PostgreSQL, calls the exchange synchronously, and applies async fills.
- **Techniques:** Per-symbol Pub/Sub (servers subscribe only to watched symbols); ~500 WebSocket servers × 10K connections (fan-out); idempotency key (no double orders); DB-write-first + recovery worker (no lost orders); reconciliation job (exchange/DB drift).

## Understanding the Problem

📈 **What is Robinhood?**  
Robinhood is a commission-free brokerage that lets users see live stock prices and place market/limit orders. It routes trades through external exchanges ("market makers") and receives payment for order flow.

**Key context:** Robinhood is a **broker**, not an exchange. We rely on an external exchange API:
- **Order Processing:** Synchronous request/response for placing/cancelling orders
- **Trade Feed:** Push-based stream — whenever a trade occurs, the exchange pushes `{ symbol, price, shares, order_id }` to us

---

### Functional Requirements

**Core Requirements**

- Users should be able to see live prices of stocks
- Users should be able to manage orders for stocks (market/limit orders, create/cancel)

**Below the line (out of scope):**

- Trading outside market hours
- ETFs, options, crypto
- Viewing the order book in real time

### Non-Functional Requirements

**Core Requirements**

- Live prices should update with low latency (< 1 second from trade to user display)
- The system should scale to **5M concurrent users** viewing live prices
- Order placement should be **strongly consistent** (no double-fills, no lost orders)
- Order state must be **durable** — no order lost even on system crash

**Below the line (out of scope):**

- Sub-millisecond execution (we're a retail broker, not HFT)

### Constraints & Estimates

- 5M concurrent users watching prices
- S&P 500: ~500 heavily-traded symbols; each symbol may trade thousands of times/min
- Peak trade events: ~10K trades/sec across all symbols
- 5M users × avg 3 symbols watched = 15M subscriptions
- Price updates to push: 10K trades/sec × avg 1,000 watchers/symbol = 10M pushes/sec (needs fan-out)
- Orders: retail users → ~100K orders/day at peak → ~1.2 orders/sec average (easy)

---

## The Set Up

### Planning the Approach

Two largely independent sub-problems:
1. **Live price feed** – high fan-out pub/sub from exchange trade stream to 5M users
2. **Order management** – low-throughput but requires strong consistency and reliability

### Defining the Core Entities

- **Stock** – symbol, company_name, exchange, current_price, last_trade_at
- **Order** – id, user_id, symbol, type (market/limit), side (buy/sell), quantity, limit_price, status (pending/filled/cancelled/rejected), external_order_id, created_at
- **Position** – user_id, symbol, shares_held, avg_cost_basis
- **UserWatchlist** – user_id, symbols[]

### The API

```
// Get live price for a symbol
GET /stocks/{symbol}/price
-> { symbol, price, change, change_pct, last_trade_at }

// Subscribe to real-time price updates (WebSocket)
WS /prices/stream
Client sends: { "subscribe": ["AAPL", "GOOGL", "TSLA"] }
Server sends: { "symbol": "AAPL", "price": 182.50, "ts": 1700000000 }

// Place an order
POST /orders
{ "symbol": "AAPL", "type": "market", "side": "buy", "quantity": 10 }
-> { order_id, status: "pending" }

// Cancel an order
DELETE /orders/{order_id}
-> { status: "cancellation_requested" }

// Get order status
GET /orders/{order_id}
-> { order_id, status, filled_at, fill_price, quantity }

// Get order history
GET /orders?symbol=AAPL&limit=50
-> { orders: [...] }
```

---

## High-Level Design

### 1) Users should be able to see live prices of stocks

**Price update flow:**

```
Exchange Trade Feed (push) → Price Feed Service → WebSocket Server → Client
```

1. **Exchange Trade Feed** pushes `{ symbol, price, shares, order_id }` for every trade
2. **Price Feed Service** (single consumer of exchange feed):
   - Updates `current_price` in Redis: `SET price:{symbol} {price} EX 60`
   - Publishes to Redis Pub/Sub channel `price:{symbol}`
3. **WebSocket Servers** subscribe to Redis Pub/Sub channels for the symbols their connected users are watching
4. When a pub/sub message arrives, WebSocket server pushes `{ symbol, price }` to subscribed clients

**Client flow:**
1. Client opens WebSocket connection to WebSocket Server
2. Sends `{ subscribe: ["AAPL", "GOOGL"] }`
3. WebSocket Server subscribes to `price:AAPL` and `price:GOOGL` on Redis Pub/Sub
4. Receives price updates → forwards to client

**Initial price on page load:**
- `GET /stocks/{symbol}/price` → reads from Redis `price:{symbol}` → O(1)

### 2) Users should be able to manage orders

**Order placement flow:**

```
Client → POST /orders → Order Service
  → Write order to DB (status=pending, idempotency_key=unique)
  → Call Exchange API (synchronous): POST /exchange/orders
  → Exchange returns: { exchange_order_id, status }
  → Update order: status=submitted, external_order_id={exchange_order_id}
  → Return order_id to client

Exchange pushes trade fill event (async):
  → Trade Feed: { order_id: exchange_order_id, fill_price, quantity }
  → Order Updater: match to our internal order, update status=filled
  → Update Position: shares_held += quantity, recalculate avg_cost_basis
```

**Order cancellation:**
- Client: `DELETE /orders/{id}`
- Order Service: call Exchange API to cancel external order
- Exchange confirms (or returns "already filled")
- Update order status accordingly

---

## Potential Deep Dives

### 1) How can the system scale up live price updates?

**Problem:** 5M users watching live prices. 10K trade events/sec. Each trade may need to be pushed to thousands of users watching that symbol.

**Naive approach:** Exchange feed → one WebSocket server → push to all 5M connections.
Problem: one server can't hold 5M WebSocket connections (memory, file descriptors).

**Scalable architecture: WebSocket fleet + Redis Pub/Sub**

```
Exchange Trade Feed
  → Price Feed Service
    → Redis Pub/Sub (channel per symbol: "price:AAPL", "price:GOOGL", ...)

5M clients distributed across 500+ WebSocket servers:
  - Each WebSocket server holds ~10K connections
  - Each WebSocket server subscribes to Redis Pub/Sub channels for the symbols its clients are watching
  - On price update: Redis broadcasts to all WebSocket servers subscribed to that channel
  - WebSocket server delivers to its connected clients watching that symbol
```

**Efficiency:** A WebSocket server only subscribes to symbols that at least one of its clients is watching. If none of its 10K clients watches TSLA, that server doesn't receive TSLA updates.

**Scale math:**
- 500 WebSocket servers × 10K connections = 5M connections ✓
- 10K trades/sec → ~10K Pub/Sub messages/sec → Redis handles easily
- Each symbol update: published once to Redis → broadcast only to the WebSocket servers that have watchers for that symbol → each server pushes to its local watchers. Because connections are spread by user_id, a symbol with ~1,000 watchers across 500 servers lands on most servers (~430 on average), so popular symbols fan out to nearly all servers while long-tail symbols reach only a few; Redis Pub/Sub fan-out of ~10K msgs/sec × a few hundred subscribers is still manageable (shard Pub/Sub by symbol if needed)

**Connection routing:**
- Load balancer uses consistent hashing on user_id to route WebSocket connections
- Ensures same user reconnects to the same server (maintains subscription state)
- Or: stateless WebSocket servers (re-subscribe on reconnect from client)

### 2) How does the system track order updates?

**Problem:** After placing an order, it goes to the exchange asynchronously. Order status (filled, partially filled, cancelled by exchange) arrives via the trade feed.

**Order state tracking:**

```
Order placed → DB status=pending, external_order_id=X
Exchange fills order → Trade Feed: { order_id: X, fill_price, quantity }
  → Order Updater Service:
    - Look up our internal order by external_order_id (index on external_order_id)
    - Update status = filled, fill_price, filled_at
    - Update Position table
    - Notify user via WebSocket: { type: "order_filled", order_id, fill_price }
```

**Partial fills:**
- Market orders can be partially filled (order for 100 shares, only 60 available immediately)
- Track `filled_quantity` on order; multiple trade events accumulate until `filled_quantity = quantity`

**Order status push to client:**
- When order fills, push notification via WebSocket (same connection the client uses for prices)
- Or: SSE channel per user for order updates

### 3) How does the system manage order consistency?

**Problems to solve:**
1. **Double submission:** User taps "Buy" twice → 2 orders placed
2. **Lost order:** Server crash after sending to exchange but before writing confirmation to DB
3. **State mismatch:** Exchange fills order but our DB isn't updated

**Solution for double submission: Idempotency key**

Client generates a UUID for each order attempt and includes it:
```json
{ "symbol": "AAPL", "quantity": 10, "idempotency_key": "uuid-abc-123" }
```

Server:
```sql
INSERT INTO orders (..., idempotency_key)
VALUES (...)
ON CONFLICT (idempotency_key) DO NOTHING
RETURNING id;
```

Duplicate submission returns the same order_id — no double order.

**Solution for lost order (saga pattern):**

Write to DB **first**, then call exchange:
```
1. Write order to DB: status=pending, exchange_order_id=null
2. Call exchange API (synchronous)
3a. Success: update DB: status=submitted, exchange_order_id=X
3b. Network timeout: order may or may not have been received by exchange
   → Recovery worker: scan orders with status=pending AND created_at < 30s ago
     → Re-call exchange to check if order exists (by idempotency key)
     → If exists: update our DB; if not: re-submit
```

This is an **outbox pattern variant**: DB write is durable; network failure is handled by recovery.

**State mismatch (exchange vs. DB):**
- Reconciliation job runs every 1 hour:
  ```
  For all open orders (status=pending or submitted):
    → Query exchange API for order status
    → Reconcile with DB
  ```
- Alerts on discrepancies

---

## Final Design

```
Exchange
  ├─ Trade Feed (push) → Price Feed Service → Redis Pub/Sub → WebSocket Servers → Clients
  └─ Order API (request/response) ← Order Service

Client
  ├─ WebSocket (prices + order notifications) → WebSocket Server (500 pods)
  └─ REST API (orders, account) → API Gateway → Order Service

Price Feed Service (single consumer of exchange trade feed)
  → Redis: SET price:{symbol} {price}
  → Redis Pub/Sub: PUBLISH price:{symbol} {event}

Order Service
  → PostgreSQL (orders, positions — strong consistency, ACID)
  → Exchange API (sync HTTP)
  → Trade Feed Consumer (async fills) → PostgreSQL (update order + position)
  → WebSocket notification on fill

Recovery Worker (every 30s)
  → Find stale pending orders → re-check with exchange
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entities and REST + WebSocket API design
- Redis for current price storage
- Idempotency for order deduplication
- Basic order status tracking

### Senior
- Redis Pub/Sub fan-out for 5M users
- WebSocket fleet with per-symbol subscriptions
- Outbox / recovery pattern for order consistency
- Partial fill tracking

### Staff+
- Consistent hash routing for WebSocket connections
- Subscription optimization (server only subscribes to watched symbols)
- Exchange reconciliation job for state mismatch
- Detailed position update atomicity (order fill + position update in one transaction)
- Discusses circuit breaker for exchange API outages
