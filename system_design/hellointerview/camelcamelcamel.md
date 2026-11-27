---
layout: simple
title: "Design a Price Tracking Service (CamelCamelCamel) — Hello Interview Style"
permalink: /system_design/hellointerview/camelcamelcamel
---

# Price Tracking Service (CamelCamelCamel)

**Difficulty:** Medium  
**Source:** hellointerview.com (AI-generated full solution)

---

## Summary

- **Key challenge:** Track prices for 500M Amazon products (~580 changes/s) without being blocked by Amazon, and send price-drop alerts within 1 hour.
- **Core design:** Extension reports, the Amazon API and crawlers feed Ingest API → Kafka → Price Processor, which updates PostgreSQL, appends to TimescaleDB and publishes drops; a Notification Dispatcher matches subscriptions and fans out to email/push/SMS workers.
- **Techniques:** Extension users as free crawlers; crawl priority (hourly if subscribed, daily long-tail); consensus, trust scores and own-crawler checks against fake prices; (product_id, threshold) index with batched fan-out; continuous aggregates + Redis for <500ms charts; hot/warm/cold storage.

## Understanding the Problem

📈 **What is CamelCamelCamel?**  
CamelCamelCamel monitors Amazon product prices over time and alerts users when prices drop below their specified thresholds. It also has a popular Chrome extension with 1M active users that shows price history directly on Amazon product pages.

---

### Functional Requirements

**Core Requirements**

- Users should be able to view price history for Amazon products (via website or Chrome extension)
- Users should be able to subscribe to price drop notifications with thresholds (via website or Chrome extension)

**Below the line (out of scope):**

- Search and discover products
- Price comparison across multiple retailers
- Product reviews and ratings

### Non-Functional Requirements

**Core Requirements**

- The system should prioritize availability over consistency (eventual consistency OK)
- The system should track **500 million** Amazon products
- Price history queries should return in **< 500ms**
- Price drop notifications should be delivered within **1 hour** of the price change

**Below the line (out of scope):**

- Real-time price updates (sub-minute freshness)
- Strong consistency for price data

### Constraints & Estimates

- 500M Amazon products to track
- Price changes: assume ~10% of products change price daily → 50M price updates/day → ~580 price updates/sec
- Chrome extension: 1M active users, ~5% on Amazon at any time → 50K concurrent product page views
- Price history requests: 50K × 1 request = 50K/sec peak (via extension)
- Each price record: timestamp (8B) + price (4B) + product_id (8B) = ~20 bytes
- Price history per product: ~365 records/year × 20B = ~7KB/year/product
- 500M products × 7KB = **3.5TB/year** of price data

---

## The Set Up

### Planning the Approach

Three main sub-systems:
1. **Price Discovery** – how we find and track 500M products and detect price changes
2. **Notification Pipeline** – how we match price changes against subscriptions and deliver alerts
3. **Price History Serving** – how we serve fast price history charts

### Defining the Core Entities

- **Product** – id, asin (Amazon product ID), name, category, current_price, last_checked_at
- **PricePoint** – product_id, price, timestamp (time-series)
- **Subscription** – id, user_id, product_id, threshold_price, channel (email/push/SMS), created_at
- **User** – id, email, push_token, phone

### The API

```
// Get price history for a product (used by Chrome extension + website)
GET /products/{asin}/price-history?from=2024-01-01&to=2024-12-01&granularity=daily
-> { asin, name, current_price, history: [{ date, min, max, avg }] }

// Subscribe to price drop alerts
POST /products/{asin}/subscriptions
{ "threshold_price": 49.99, "channel": "email" }
-> { subscription_id }

// Get user's subscriptions
GET /users/{user_id}/subscriptions
-> { subscriptions: [{ product, threshold, current_price }] }

// Delete subscription
DELETE /subscriptions/{subscription_id}
-> { status: "deleted" }
```

### Data Flow

```
Amazon product pages
  ↓ crawl / extension reports
Price Ingestion → Kafka → Price Processor
                          ├─ Update current_price in DB
                          ├─ Append PricePoint to time-series DB
                          └─ Check subscriptions → Notify users

Client (extension / website) → Price History Service → Time-series DB
```

---

## High-Level Design

### 1) Users should be able to view price history

**Price History Service** fetches time-series data for a product:

1. Chrome extension or website calls `GET /products/{asin}/price-history`
2. Price History Service checks **Redis cache** (TTL: 1 hour) for pre-aggregated chart data
3. Cache miss: query **time-series DB** (TimescaleDB or InfluxDB) for raw price points
4. Aggregate: group by day/week/month, return min/max/avg per bucket
5. Cache result in Redis

**Time-series storage (TimescaleDB):**
```sql
CREATE TABLE price_points (
  product_id  BIGINT NOT NULL,
  price       DECIMAL(10,2) NOT NULL,
  recorded_at TIMESTAMP NOT NULL
);
SELECT create_hypertable('price_points', 'recorded_at');
CREATE INDEX ON price_points (product_id, recorded_at DESC);
```

TimescaleDB automatically partitions by time (chunks), enabling fast range queries by product + time window.

### 2) Users should be able to subscribe to price drop notifications

**Subscription storage (PostgreSQL):**
```sql
CREATE TABLE subscriptions (
  id            UUID PRIMARY KEY,
  user_id       UUID NOT NULL,
  product_id    BIGINT NOT NULL,
  threshold     DECIMAL(10,2) NOT NULL,
  channel       TEXT NOT NULL,  -- email | push | sms
  is_active     BOOLEAN DEFAULT TRUE,
  created_at    TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_product_subscriptions ON subscriptions(product_id, threshold, is_active);
```

**Notification check (on price update):**
1. Price update event arrives: `{ product_id, new_price, old_price }`
2. Only process if `new_price < old_price` (price dropped)
3. Query subscriptions: `SELECT * FROM subscriptions WHERE product_id = :id AND threshold >= :new_price AND is_active = TRUE`
4. For each matching subscription, enqueue notification job

---

## Potential Deep Dives

### 1) How do we efficiently discover and track 500 million Amazon products?

**Challenge:** We can't just crawl all 500M product pages continuously — Amazon will block us, and it would take enormous bandwidth.

**Three-pronged discovery strategy:**

**A) Chrome extension as a distributed crawler:**
- 1M extension users each browse Amazon product pages
- Extension reads the current price from the page DOM (no extra HTTP request needed)
- Extension reports: `{ asin, current_price, timestamp }` to our ingest API
- Effectively, our users are our crawlers for the most popular products

**B) Amazon Product Advertising API (affiliate API):**
- Amazon's official API provides product data including price
- Rate-limited but authorized
- Use for structured catalog discovery and bulk price lookups

**C) RSS/sitemap crawling + direct page scraping:**
- Amazon provides product sitemaps; use to discover new ASINs
- Crawl product pages for ASINs not covered by extension users
- Respect robots.txt, rate-limit per IP, rotate proxies for high-volume scraping
- Crawl priority: products with active subscriptions > popular products > rest

**Crawl scheduling:**
- Products with subscriptions: crawl every 1 hour (SLA: notify within 1 hour)
- Popular products (top 10% by traffic): crawl every 6 hours
- Long-tail products: crawl every 24 hours
- Total crawl load: prioritized 50M subscribed products × 1/hr = 13,900 crawls/sec → need a distributed crawler fleet

### 2) How do we handle potentially malicious price updates from Chrome extension users?

**Problem:** A malicious user could report fake prices (e.g., iPhone at $1) triggering false notifications to thousands of users.

**Validation strategies:**

**A) Anomaly detection:**
- If reported price deviates > 50% from last known price, flag for verification
- Cross-reference with other extension reports for the same product (consensus)
- If 3+ users independently report the same price change → accept it

**B) Trust scoring:**
- Track per-user report accuracy (do their reported prices match eventual verified prices?)
- Low-trust users' reports require corroboration before acceptance

**C) Authoritative verification:**
- For large price changes (> 20%), verify by fetching the product page from our own crawler before triggering notifications
- Slight delay (minutes) but prevents false positives

**D) Rate limiting:**
- Limit reports per user per product per hour
- Prevents flooding the system with fake reports

### 3) How do we efficiently process price changes and notify subscribed users?

**The fan-out problem:** A popular product (e.g., AirPods) drops in price → might have 100K subscribers to notify.

**Pipeline:**
```
Price change event (Kafka)
  ↓
Notification Dispatcher (stateless workers)
  - Query subscriptions: products with threshold >= new_price
  - For products with many subscribers: batch into notification jobs
  ↓
Kafka ("notification-jobs")
  ↓
Notification Workers (email/push/SMS)
  - Email → SendGrid
  - Push → FCM/APNs
  - SMS → Twilio
```

**Subscription index optimization:**

Naive: scan all 500M subscriptions for each price change.

Better: index subscriptions by `(product_id, threshold)`:
```sql
-- Only subscriptions where threshold >= new_price qualify
SELECT user_id, channel FROM subscriptions
WHERE product_id = :id
  AND threshold >= :new_price
  AND is_active = TRUE;
```

For 100K subscribers per popular product: this query returns a large result set. Use cursor-based pagination to process in batches of 1000, enqueue each batch as a notification job.

**Notification deduplication:**
- Track sent notifications: `UNIQUE(user_id, product_id, notification_date)` 
- Don't spam: even if price changes multiple times in a day, send at most 1 notification per day per product per user

### 4) How do we serve fast price history queries for chart generation?

**Challenge:** 500M products × years of price history = tens of terabytes (~3.5TB/year). Can't query raw data for every chart render.

**Pre-aggregated rollups (TimescaleDB continuous aggregates):**

```sql
-- Auto-computed materialized view: daily aggregates
CREATE MATERIALIZED VIEW price_daily
WITH (timescaledb.continuous) AS
SELECT
  product_id,
  time_bucket('1 day', recorded_at) AS bucket,
  MIN(price) AS min_price,
  MAX(price) AS max_price,
  AVG(price) AS avg_price
FROM price_points
GROUP BY product_id, bucket;
```

Chart queries hit the materialized view (pre-aggregated per day) instead of raw points:
```sql
-- 1-year chart: 365 rows instead of potentially thousands of raw points
SELECT bucket, min_price, max_price, avg_price
FROM price_daily
WHERE product_id = :id AND bucket BETWEEN :start AND :end
ORDER BY bucket;
```

**Redis caching for hot products:**
- Popular products' price history cached in Redis (TTL: 1 hour)
- Key: `price_history:{asin}:{granularity}:{start_date}:{end_date}`

**Tiered storage:**
- Hot data (last 90 days): TimescaleDB (fast SSD-backed queries)
- Warm data (90 days–2 years): TimescaleDB with compression (10–20× space savings)
- Cold data (> 2 years): S3 Parquet files (cheap, rare access)

---

## Final Design

```
Chrome Extension (1M users)         Amazon APIs / Crawlers
  │ report {asin, price}              │ bulk price updates
  └─────────────────────┬─────────────┘
                        ▼
                 Price Ingest API (stateless, 1000 pods)
                        ↓
                 Kafka ("price-updates")
                        ├─→ Price Processor
                        │     ├─ Update products.current_price (PostgreSQL)
                        │     ├─ Append to price_points (TimescaleDB)
                        │     └─ Publish to Kafka("price-drops") if price fell
                        │
                        └─→ Kafka("price-drops")
                              ↓
                        Notification Dispatcher
                              - Query subscriptions (PostgreSQL)
                              - Batch into notification jobs (Kafka)
                              ↓
                        Notification Workers
                              → SendGrid (email)
                              → FCM/APNs (push)
                              → Twilio (SMS)

Client (extension / website)
  → Price History Service
    ├─ Redis cache (TTL 1h)
    └─ TimescaleDB (materialized daily/weekly/monthly aggregates)
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entity design and REST APIs
- TimescaleDB or InfluxDB for time-series price data
- Simple subscription + notification on price change
- Understands Chrome extension as a data source

### Senior
- Three-pronged crawl strategy (extension + API + scraper)
- Crawl prioritization by subscription count
- Tiered crawl frequency (hourly for subscribed, daily for long-tail)
- Notification fan-out via Kafka + worker pool
- Pre-aggregated rollups for fast chart queries

### Staff+
- Malicious price report validation (consensus + trust scoring)
- Tiered storage (hot/warm/cold) for 500M products × years of history
- Subscription index optimization for large fan-out
- Deduplication to avoid notification spam
- Compression strategy for cold price history
