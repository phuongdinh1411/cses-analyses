---
layout: simple
title: "Design Yelp — Hello Interview Style"
permalink: /system_design/hellointerview/yelp
---

# Yelp

**Patterns:** Scaling Reads · Geospatial Search  
**Difficulty:** Easy  
**Source:** hellointerview.com (AI-generated full solution)

---

## Summary

- **Key challenge:** Search businesses by keyword, category and location in < 500ms for 100M DAU over 10M businesses (~100K peak search QPS, read-heavy).
- **Core design:** Search Service queries Elasticsearch (text + geo_distance); Business Service reads PostgreSQL behind Redis; Review Service inserts a review and updates avg_rating in one transaction, syncing Elasticsearch via Kafka.
- **Techniques:** Elasticsearch geo_point bool query (text + geo together); precomputed avg_rating/review_count (O(1) reads); incremental rating update in one transaction (consistency); UNIQUE(business_id, user_id) (one review per user); Redis cache (read load); geocoding place names (location-name search).

## Understanding the Problem

🍽️ **What is Yelp?**  
Yelp is an online platform that allows users to search for and review local businesses, restaurants, and services.

---

### Functional Requirements

**Core Requirements**

- Users should be able to search for businesses by name, location (lat/long), and category
- Users should be able to view businesses (and their reviews)
- Users should be able to leave reviews on businesses (mandatory 1–5 star rating and optional text)

**Below the line (out of scope):**

- Admins should be able to add, update, and remove businesses
- Users should be able to view businesses on a map
- Users should be able to get recommended businesses

### Non-Functional Requirements

**Core Requirements**

- The system should have low latency for search operations (< 500ms)
- The system should be highly available; eventual consistency is acceptable
- The system should scale to 100M daily users and 10M businesses

**Below the line (out of scope):**

- GDPR data protection
- Spam / abuse prevention

### Constraints & Estimates

- 100M DAU, 10M businesses
- Read-heavy: ~90% reads, ~10% writes
- Each business ~1KB metadata + reviews
- Peak search QPS: ~100K/s
- Reviews: ~1M/day new submissions

---

## The Set Up

### Defining the Core Entities

- **Business** – id, name, address, lat, lng, category, avg_rating, review_count, attributes (hours, phone, etc.)
- **Review** – id, business_id, user_id, rating (1–5), text, created_at
- **User** – id, name, email

### The API

```
// Search for businesses
GET /businesses/search?q=pizza&lat=37.7&lng=-122.4&radius_km=5&category=restaurant&page=1&limit=20
-> { businesses: [...], total, next_cursor }

// Get business details
GET /businesses/{business_id}
-> { business, reviews_summary }

// Get reviews for a business
GET /businesses/{business_id}/reviews?page=1&limit=20
-> { reviews: [...], total }

// Submit a review
POST /businesses/{business_id}/reviews
{ "rating": 4, "text": "Great tacos!" }
-> { review_id, created_at }
```

---

## High-Level Design

### 1) Users should be able to search for businesses

**Components:**
- **Client** → **API Gateway** → **Search Service** → **Search Index (Elasticsearch)** + **Geo Index**
- **Business DB** (PostgreSQL) stores canonical business data
- Elasticsearch indexes business name, category, description; geo queries use a Geo Point field

**Flow:**
1. User submits search with keyword + location
2. Search Service queries Elasticsearch with a `bool` query: keyword match on `name/category` + `geo_distance` filter on lat/lng within radius
3. Results returned sorted by relevance + distance (combined score)
4. Business metadata fetched from cache (Redis) or DB for display

**Geospatial indexing options:**

| Approach | How It Works | Tradeoff |
|---|---|---|
| Elasticsearch geo_point | Native geo distance queries, great for search | Operational complexity |
| PostGIS | PostgreSQL extension with spatial indexes | Good for exact queries, less full-text |
| Geohash grid | Encode lat/lng to hash prefix, range query | Simple but coarse-grained |
| Quadtree | Recursive spatial partitioning | Efficient but complex to implement |

**Best choice:** Elasticsearch with `geo_distance` filter — it combines keyword search + geo queries natively.

### 2) Users should be able to view businesses

**Flow:**
1. `GET /businesses/{id}` hits the **Business Service**
2. Business Service checks **Redis cache** (TTL 5 min) for business metadata
3. On cache miss, fetches from **PostgreSQL** (businesses table)
4. Reviews summary (avg rating, count) is pre-computed and stored on the business row
5. Return combined response

**Data model (PostgreSQL):**

```sql
CREATE TABLE businesses (
  id          UUID PRIMARY KEY,
  name        TEXT NOT NULL,
  address     TEXT,
  lat         FLOAT,
  lng         FLOAT,
  category    TEXT,
  avg_rating  FLOAT DEFAULT 0,
  review_count INT DEFAULT 0,
  attributes  JSONB,
  created_at  TIMESTAMP
);

CREATE TABLE reviews (
  id          UUID PRIMARY KEY,
  business_id UUID REFERENCES businesses(id),
  user_id     UUID,
  rating      SMALLINT CHECK (rating BETWEEN 1 AND 5),
  text        TEXT,
  created_at  TIMESTAMP
);
CREATE UNIQUE INDEX idx_one_review ON reviews(business_id, user_id);
```

### 3) Users should be able to leave reviews

**Flow:**
1. `POST /businesses/{id}/reviews` hits **Review Service**
2. Check `UNIQUE(business_id, user_id)` constraint → reject duplicates
3. Insert review row
4. Update `avg_rating` and `review_count` on the business row (see Deep Dive #1)
5. Async: propagate updated avg_rating to Elasticsearch for search result freshness

---

## Potential Deep Dives

### 1) How would you efficiently calculate and update the average rating?

**Bad Solution: Recalculate on every read**

Scan all reviews for a business and compute average. For popular businesses with 100K reviews, this is O(n) per read — catastrophically slow.

**Good Solution: Incremental update on write**

```sql
UPDATE businesses
SET
  review_count = review_count + 1,
  avg_rating   = (avg_rating * review_count + :new_rating) / (review_count + 1)
WHERE id = :business_id;
```

This is O(1) per write but requires careful handling of concurrent updates. It's also only correct in PostgreSQL (and standard SQL), where every SET expression sees the old row values; MySQL evaluates assignments left to right, so `avg_rating` would use the already-incremented `review_count` (put the `avg_rating` assignment first there).

**Great Solution: Atomic increment with optimistic locking or DB transaction**

Wrap review insert + business update in a single transaction:

```sql
BEGIN;
INSERT INTO reviews (id, business_id, user_id, rating, text) VALUES (...);
UPDATE businesses
  SET avg_rating = (avg_rating * review_count + :rating) / (review_count + 1),
      review_count = review_count + 1
  WHERE id = :business_id;
COMMIT;
```

This keeps the aggregate always consistent. For Staff+ level: use a Kafka event from Review Service → Rating Aggregator Service to keep the update async and avoid hot-row contention on popular businesses.

### 2) How would you ensure a user can only leave one review per business?

**Solution:** Enforce `UNIQUE(business_id, user_id)` index in the database — the DB will reject duplicate inserts at the constraint level, no application-level check required.

For distributed scenarios (multiple write nodes), the unique constraint needs to live at the DB level. With sharded DBs, ensure the shard key routes both the check and the insert to the same shard (shard on `business_id`).

### 3) How can you improve search to handle complex queries?

**Current state:** Simple Elasticsearch keyword + geo filter.

**Improvements:**

| Enhancement | Technique |
|---|---|
| Fuzzy matching | Elasticsearch `fuzziness: AUTO` to handle typos |
| Category filtering | Term filter on `category` field |
| Relevance tuning | Boost `name` field over `description`; boost businesses with higher ratings |
| Faceted search | Elasticsearch aggregations for category counts, price range buckets |
| Query understanding | Pre-process query: "pizza near me" → extract intent + location |

For Staff+ level: introduce a **Query Rewriting Service** that uses an NLP model to extract entities (cuisine type, location name, attributes) from free-text queries before hitting Elasticsearch.

### 4) How would you allow searching by predefined location names (cities, neighborhoods)?

**Problem:** Users type "pizza in SoHo" but we only store lat/lng.

**Solution: Geocoding Service**

1. Maintain a **Place Name → Bounding Box** lookup (backed by data from OpenStreetMap or Google Places)
2. Store `city`, `neighborhood` fields on each business (populate during ingestion via reverse geocoding)
3. On query: detect location entity → resolve to bounding box → pass as `geo_bounding_box` filter to Elasticsearch (radius searches like "near me" keep using `geo_distance`)
4. Cache place name lookups in Redis (place names change rarely)

**Data flow:**
```
User: "tacos in SoHo NYC"
  → NLP extracts: query="tacos", location="SoHo NYC"
  → Geocoding Service: "SoHo NYC" → { top_left: (40.728, -74.005), bottom_right: (40.720, -73.997) }
  → Elasticsearch: keyword="tacos" + geo_bounding_box filter with that box
```

---

## Final Design

```
Client
  │
  ▼
API Gateway
  ├── Search Service ──→ Elasticsearch (geo + text index)
  │                  └─→ Redis (business metadata cache)
  ├── Business Service ──→ PostgreSQL (businesses, reviews)
  │                    └─→ Redis (cache)
  └── Review Service ──→ PostgreSQL (reviews + atomic avg_rating update)
                      └─→ Kafka → Elasticsearch sync (async index update)
```

---

## What is Expected at Each Level?

### Mid-level
- Correctly identifies core entities and APIs
- Proposes Elasticsearch or PostGIS for geo search
- Knows about indexing and query structure
- Simple avg_rating update on write

### Senior
- Discusses geospatial indexing trade-offs (Elasticsearch vs PostGIS vs geohash)
- Handles avg_rating atomically within a transaction
- Adds caching layer for business reads
- Addresses one-review-per-user via DB constraint

### Staff+
- Proposes async rating aggregation via Kafka to avoid hot-row contention
- Discusses query understanding / NLP layer for search
- Addresses sharding strategy for 10M businesses
- Discusses CDN for business thumbnail images
- Considers Elasticsearch replication and index refresh intervals for search freshness
