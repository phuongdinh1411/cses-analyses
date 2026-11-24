---
layout: simple
title: "Design a News Aggregator (Google News) — Hello Interview Style"
permalink: /system_design/hellointerview/google-news
---

# News Aggregator (Google News)

**Patterns:** Scaling Reads  
**Difficulty:** Medium  
**Source:** hellointerview.com (AI-generated full solution)

---

## Understanding the Problem

📰 **What is Google News?**  
Google News aggregates articles from thousands of publishers worldwide into a scrollable feed. It crawls publisher RSS/Atom feeds, indexes articles, and displays them in a feed ordered by recency and relevance.

---

### Functional Requirements

**Core Requirements**

- Users should be able to view an aggregated feed of news articles from thousands of source publishers all over the world
- Users should be able to scroll through the feed "infinitely" (pagination)
- Users should be able to click on articles and be redirected to the publisher's website to read the full content

**Below the line (out of scope):**

- Personalized feed based on reading history
- Saving articles for later
- Sharing articles on social media
- Category customization

### Non-Functional Requirements

**Core Requirements**

- The system should prioritize availability over consistency (eventual consistency OK — slightly stale feed is fine)
- Feed requests should have low latency (< 200ms)
- Articles should appear in feeds within **30 minutes** of publication
- The system should scale to handle massive traffic during breaking news spikes

**Below the line (out of scope):**

- Real-time article indexing (sub-minute)
- Strong consistency for article counts

### Constraints & Estimates

- 10,000 publisher RSS feeds, each updating every 5–60 minutes
- Average 100 new articles/day per publisher → 1M new articles/day globally
- ~100M DAU reading news
- Feed reads: 100M × 10 page loads/day = 1B reads/day → ~12K reads/sec
- Article metadata: ~2KB/article
- Crawl frequency: 10K feeds × every 15min = 667 RSS fetches/min

---

## The Set Up

### Planning the Approach

This is fundamentally a **crawl → index → serve** pipeline:
1. **Crawler** – periodically fetches publisher RSS/Atom feeds, discovers new articles
2. **Indexer** – stores article metadata, makes articles queryable
3. **Feed Service** – serves paginated, sorted article feeds to users

### Defining the Core Entities

- **Publisher** – id, name, rss_url, crawl_interval_mins, last_crawled_at
- **Article** – id, publisher_id, title, url, description, thumbnail_url, published_at, indexed_at, category
- **Feed** (virtual, computed at read time or pre-built)

### API or System Interface

```
// Get main news feed (paginated by cursor)
GET /feed?limit=20&cursor=<article_id_or_timestamp>
-> { articles: [ { id, title, publisher, url, thumbnail, published_at, category } ], next_cursor }

// Get feed by category
GET /feed?category=technology&limit=20&cursor=...
-> { articles: [...], next_cursor }

// Get article redirect (track click + redirect to publisher)
GET /articles/{article_id}/redirect
-> HTTP 302 → publisher URL
```

---

## High-Level Design

### 1) Users should be able to view an aggregated feed of news articles

**Architecture overview:**

```
RSS Feeds (publishers)
  ↓ crawl every 15 min
Feed Crawler
  ↓ new articles
Kafka (article events)
  ↓
Article Indexer → PostgreSQL (articles table)
                → Elasticsearch (full-text + filter index)
                → Redis (feed cache)

Client → API Gateway → Feed Service → Redis cache → PostgreSQL/Elasticsearch
```

**Feed query (simple):**
```sql
SELECT * FROM articles
WHERE published_at > NOW() - interval '7 days'
ORDER BY published_at DESC
LIMIT 20
OFFSET :page * 20;
```

Problem: OFFSET-based pagination is slow at large offsets. Use cursor-based pagination instead (see Deep Dive #1).

### 2) Users should be able to scroll through the feed "infinitely"

The feed is ordered by `published_at DESC`. Users scroll down, loading 20 articles at a time.

**Simple cursor-based pagination:**
```sql
-- First page
SELECT * FROM articles
ORDER BY published_at DESC, id DESC
LIMIT 20;
-- Returns cursor = { last_published_at, last_id }

-- Next page
SELECT * FROM articles
WHERE (published_at, id) < (:last_published_at, :last_id)
ORDER BY published_at DESC, id DESC
LIMIT 20;
```

This is O(log N) with a compound index on `(published_at DESC, id DESC)`.

### 3) Users should be able to click on articles and be redirected

Simple redirect through our system (allows tracking and prevents publisher URL changes from breaking bookmarks):

```
GET /articles/{id}/redirect
  → lookup article URL from DB/cache
  → HTTP 302 to publisher URL
```

Optionally, record the click event asynchronously (Kafka → analytics pipeline) without slowing down the redirect.

---

## Potential Deep Dives

### 1) How can we improve pagination consistency and efficiency?

**Problem with time-based cursors:** New articles published between page loads shift existing articles' offsets. User scrolling sees the same article twice or misses articles.

**Solution: Stable cursor = `(published_at, article_id)`**

Using the compound cursor `(published_at DESC, id DESC)` ensures:
1. No duplicates — same cursor always continues from the same position
2. New articles published at the top don't affect existing cursor positions
3. O(log N) with compound index — no full table scan

**Pre-built feed snapshots (for high traffic):**
- Periodically (every 5 min) build a feed snapshot: ordered list of article IDs for the last 7 days
- Store snapshot in Redis as a sorted set:
  ```
  Key: feed:global
  Score: published_at unix timestamp
  Members: article_id
  ```
- Pagination: `ZREVRANGEBYSCORE feed:global +inf {cursor_ts} LIMIT 0 20`
- Consistent pagination even as new articles arrive (snapshot doesn't change between user's scrolling session)

### 2) How do we achieve low latency (< 200ms) feed requests?

**Multi-tier caching strategy:**

**Tier 1: CDN caching**
- The global feed (first 2–3 pages) is the same for all users
- Cache it at CDN edge with TTL = 60s
- Cache-Control: `public, max-age=60`
- 95% of users only read the first page → CDN hit rate > 95%

**Tier 2: Redis feed cache**
- Cache paginated article ID lists in Redis
- `feed:global:page:1` → [article_id_1, article_id_2, ...]
- TTL: 5 minutes
- After fetching IDs, batch-fetch article metadata from Redis article cache

**Tier 3: PostgreSQL with read replicas**
- Multiple read replicas for cache misses
- Index on `(published_at DESC, id DESC)` for fast range queries

**Article metadata cache (Redis hash):**
```
Key: article:{id}
Fields: title, url, publisher, thumbnail, published_at, category
TTL: 30 minutes (articles rarely change)
```

### 3) How do we ensure articles appear in feeds within 30 minutes of publication?

**Crawling pipeline:**

```
Crawl Scheduler (every 15 min per feed)
  → HTTP GET {rss_url}
  → Parse RSS/Atom XML
  → Diff against known articles (by URL hash)
  → New articles → Kafka topic "new-articles"
  → Article Indexer: INSERT into PostgreSQL + Elasticsearch
  → Feed Cache Invalidator: DEL feed:global:page:*
```

**Crawl frequency optimization:**
- Not all feeds update equally. Use adaptive crawling:
  - High-frequency publishers (NYT, BBC): crawl every 5 min
  - Low-frequency publishers: crawl every 60 min
  - Track `articles_per_hour` per publisher, adjust interval dynamically

**RSS parsing and deduplication:**
- Hash the article URL to detect duplicates
- `UNIQUE(url_hash)` constraint in DB → idempotent inserts

**30-minute SLA:**
- Crawl every 15 min → new article discoverable within 15 min
- Index + cache update: < 30 seconds
- Total: < 16 minutes → comfortably within 30 min SLA

### 4) How do we handle media content (images/videos) efficiently?

**Problem:** Publisher thumbnail images are hosted on publisher servers — slow, unreliable, different sizes.

**Solution: Image proxy + CDN**

1. When indexing an article, extract `og:image` URL from the article's HTML `<head>`
2. Enqueue image for async processing:
   - Download from publisher → resize to standard sizes (thumbnail: 300×200, feed: 600×400)
   - Upload to our S3 bucket
   - Update article record with our CDN URL
3. Serve all thumbnails from our CDN:
   ```
   https://cdn.news.com/images/{article_id}/thumbnail.webp
   ```

**Benefits:**
- Fast, consistent image delivery from CDN edge
- WebP format: 30% smaller than JPEG
- Publisher images can break/change — ours are stable

### 5) How do we handle traffic spikes during breaking news?

**Problem:** Major news event (election result, natural disaster) → 100× normal traffic in seconds.

**Solutions:**

**CDN absorbs the spike:**
- Global feed pages (1–3) served from CDN cache (TTL 60s)
- CDN can absorb 1M+ QPS without touching our servers

**Auto-scaling:**
- API servers: Kubernetes HPA scales on CPU/RPS → adds pods in ~60s
- Feed Cache warming: pre-warm Redis cache immediately after major article indexing
- Alert: if article indexed has keywords matching "breaking news" → immediately build feed snapshot

**Cache stampede prevention:**
- When a popular cache key expires, many requests simultaneously try to rebuild it
- Use **probabilistic early expiration** (extend TTL slightly before it expires based on request rate)
- Or use **Redis distributed lock**: only one request rebuilds the cache at a time; others wait

---

## Final Design

```
Publishers (RSS feeds)
  ↓ crawl every 5–15 min
Crawl Scheduler (distributed, Kubernetes CronJob)
  ↓ new article events
Kafka ("new-articles")
  ├─→ Article Indexer → PostgreSQL (source of truth)
  │                  → Elasticsearch (full-text search, category filter)
  │                  → Redis (article metadata cache, feed sorted sets)
  └─→ Image Processor → S3 → CDN (thumbnails)

Client
  ↓
CDN (edge-cached feed pages, TTL 60s) ──→ [cache miss]
  ↓
API Gateway → Feed Service
  ├─ Redis (feed sorted set, article cache) ──→ [cache miss]
  └─ PostgreSQL read replica
```

---

## What is Expected at Each Level?

### Mid-level
- Crawler → DB → API pipeline
- Basic cursor-based pagination
- CDN for image delivery
- Understands RSS/Atom format

### Senior
- Redis sorted set for feed caching
- Adaptive crawl frequency
- CDN cache for feed pages with appropriate TTL
- Image proxy pipeline

### Staff+
- Cache stampede prevention
- Breaking news spike handling with pre-warming
- Personalized feed architecture (collaborative filtering, interest graph)
- Deduplication across publishers covering the same story (article clustering)
- Discusses crawl politeness (rate limiting, robots.txt compliance)
