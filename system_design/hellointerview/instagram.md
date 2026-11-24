---
layout: simple
title: "Design Instagram — Hello Interview Style"
permalink: /system_design/hellointerview/instagram
---

# Instagram

**Patterns:** Scaling Reads · Managing Long Running Tasks · Handling Large Blobs  
**Difficulty:** Medium  
**Source:** hellointerview.com (AI-generated full solution)

---

## Understanding the Problem

📸 **What is Instagram?**  
Instagram is a social media platform primarily focused on visual content, allowing users to share photos and videos with their followers.

---

### Functional Requirements

**Core Requirements**

- Users should be able to create posts featuring photos, videos, and a simple caption
- Users should be able to follow other users
- Users should be able to see a chronological feed of posts from the users they follow

**Below the line (out of scope):**

- Likes and comments on posts
- Stories (ephemeral content)
- Live video streaming
- Search for users, hashtags, or locations

### Non-Functional Requirements

**Core Requirements**

- The system should deliver feed content with low latency (< 500ms)
- The system should render photos and videos instantly (photos up to 8MB, videos up to 4GB)
- The system should be scalable to 500M DAU with 100M posts per day

**Below the line (out of scope):**

- End-to-end encryption
- GDPR compliance

### Constraints & Estimates

- 500M DAU, 100M posts/day → ~1,200 posts/sec writes
- Feed reads: each user checks feed ~5x/day → ~29K feed reads/sec
- Storage: 100M posts × avg 2MB photo = 200TB/day new media
- Read:write ratio ~40:1 (feed dominated)

---

## The Set Up

### Defining the Core Entities

- **User** – id, username, profile_photo, follower_count, following_count
- **Post** – id, user_id, media_url, caption, created_at, media_type (photo/video)
- **Follow** – follower_id, followee_id, created_at

### API or System Interface

```
// Create a post
POST /posts
Content-Type: multipart/form-data
{ "media": <file>, "caption": "Sunset vibes" }
-> { post_id, media_url, created_at }

// Follow a user
POST /users/{user_id}/follow
-> { status: "following" }

// Unfollow a user
DELETE /users/{user_id}/follow
-> { status: "unfollowed" }

// Get feed (paginated)
GET /feed?limit=20&cursor=<timestamp_or_id>
-> { posts: [...], next_cursor }
```

---

## High-Level Design

### 1) Users should be able to create posts featuring photos, videos, and a simple caption

**Upload flow:**

1. Client requests a **pre-signed URL** from the **Post Service** for direct S3 upload
2. Client uploads media directly to **S3** (bypasses our servers for large files)
3. Client notifies Post Service with `{ s3_key, caption }`
4. Post Service writes post metadata to **PostgreSQL** (posts table)
5. Post Service enqueues a **media processing job** to Kafka
6. **Media Processing Workers** asynchronously:
   - Transcode video to multiple resolutions (360p, 720p, 1080p) using FFmpeg
   - Generate thumbnails for videos
   - Resize photos to multiple sizes (thumbnail, feed, full)
   - Store processed media back to S3
   - Update post record with processed media URLs
7. **CDN (CloudFront)** sits in front of S3 for global delivery

**Why pre-signed URL?**  
Avoids routing gigabytes of video through our API servers. Client-to-S3 direct upload is faster and cheaper.

### 2) Users should be able to follow other users

Simple write to a **follows** table (or graph DB like Neo4j for very large graphs):

```sql
CREATE TABLE follows (
  follower_id UUID,
  followee_id UUID,
  created_at  TIMESTAMP,
  PRIMARY KEY (follower_id, followee_id)
);
-- Index for "who does user X follow?"
CREATE INDEX idx_follower ON follows(follower_id);
-- Index for "who follows user X?"
CREATE INDEX idx_followee ON follows(followee_id);
```

For 500M users, the follows table can reach billions of rows. Shard by `follower_id` for fan-out reads.

### 3) Users should be able to see a chronological feed of posts from the users they follow

**Pull model (naive):**

1. `GET /feed` → Feed Service queries follows table for all followees of the user
2. For each followee, fetch their recent posts
3. Merge-sort by `created_at` and return top N

**Problem:** A user following 2,000 accounts requires 2,000 DB lookups per feed load → too slow for 500M DAU.

**Push model (fan-out on write):**

1. When a user creates a post, the **Fan-out Service** looks up all their followers
2. Writes post_id into each follower's **feed cache** (Redis sorted set, keyed by user_id, scored by timestamp)
3. `GET /feed` simply reads from the user's Redis feed cache → O(1)

**Trade-off:** High-follower accounts (celebrities with 50M followers) cause fan-out storms.

**Hybrid model (used by Instagram/Facebook):**

- Regular users (< 1M followers): push fan-out on write to follower feed caches
- Celebrity accounts (> 1M followers): pull-on-read — excluded from fan-out; appended dynamically at read time by Feed Service

---

## Potential Deep Dives

### 1) The system should deliver feed content with low latency (< 500ms)

**Strategy: Pre-computed feed caches**

Each user has a feed cache in Redis (sorted set):
```
Key: feed:{user_id}
Score: unix_timestamp
Value: post_id
```

**Fan-out Service** maintains these caches asynchronously via Kafka events:
- New post → Kafka → Fan-out Worker → write to follower feed caches
- Unfollow → remove posts from feed cache
- Follow → backfill recent posts into feed cache

Feed Service reads from Redis in < 1ms, then fetches post metadata (hydration) in a single batch query to PostgreSQL or Redis post cache.

**Cache eviction:** Keep only the last 500 posts per user feed (prune old entries). Deeper history can be fetched from DB on scroll.

**Numbers:**
- 500M users × 500 posts × 8 bytes/post_id ≈ 2TB Redis for feed caches

### 2) The system should render photos and videos instantly

**Problem:** Raw uploads (8MB photos, 4GB videos) cannot be served directly — too slow on mobile, too expensive on bandwidth.

**Solution: Async media processing pipeline**

```
S3 (raw upload)
  → Kafka (processing jobs)
  → Media Workers (FFmpeg/ImageMagick)
  → S3 (processed: 3 photo sizes + 3 video resolutions)
  → CDN (CloudFront) with long TTL
```

**Photo processing:**
- Thumbnail: 150×150 (for feed grid)
- Feed: 600×600 (for feed display)
- Full: 1080×1080 (for detail view)

**Video processing:**
- 360p (mobile data saver)
- 720p (standard mobile)
- 1080p (WiFi / desktop)
- Thumbnail frame at t=1s

**CDN strategy:**
- All media served through CloudFront with `Cache-Control: max-age=31536000` (1 year, media is immutable)
- URLs include content hash to bust cache on reprocessing
- Edge PoPs in 50+ regions for global < 50ms delivery

### 3) The system should be scalable to support 500M DAU

**Horizontal scaling plan:**

| Component | Scaling strategy |
|---|---|
| API Servers | Stateless, auto-scale behind load balancer |
| Post metadata DB | Shard by user_id; read replicas for feed hydration |
| Follows DB | Shard by follower_id; cache heavily |
| Feed Redis | Redis Cluster with 20+ nodes; consistent hashing |
| Media processing | Autoscaling worker pool on Kubernetes |
| S3 / CDN | Inherently scalable; configure multiple S3 prefixes |

**Celebrity problem at scale:**

For accounts with 50M+ followers, fan-out would write to 50M Redis entries on each post — taking minutes. Solution:
1. Mark accounts as "celebrity" (threshold: > 1M followers)
2. Exclude celebrities from push fan-out
3. At feed read time, fetch the top 10 recent posts from each celebrity the user follows (pull)
4. Merge celebrity posts with pre-computed feed cache before returning

---

## Final Design

```
Client
  │
  ├─ [Upload] Pre-signed URL ──→ S3 (raw)
  │                              → Kafka → Media Workers → S3 (processed) → CDN
  │
  ├─ [Create Post] POST /posts ──→ Post Service ──→ PostgreSQL (posts)
  │                               └──→ Kafka → Fan-out Service → Redis (feed caches)
  │
  ├─ [Follow] POST /follow ──→ Follow Service ──→ PostgreSQL (follows)
  │                           └──→ Fan-out Service: backfill feed cache
  │
  └─ [Get Feed] GET /feed ──→ Feed Service
                              ├─ Read Redis feed cache (post_ids)
                              ├─ Hydrate: batch fetch post metadata (Redis/PG)
                              └─ Merge celebrity posts (pull for high-follower accounts)
```

---

## What is Expected at Each Level?

### Mid-level
- Correct entity design and REST APIs
- Pre-signed S3 upload flow
- Simple pull-based feed (acceptable starting point)
- Knows CDN is needed for media

### Senior
- Push fan-out on write for feed with Redis sorted sets
- Async media processing pipeline with job queue
- Multi-resolution photo/video transcoding
- Identifies celebrity fan-out problem

### Staff+
- Hybrid push/pull model for celebrities
- Feed cache sizing and eviction strategy
- Detailed sharding strategy for follows + posts at 500M DAU
- Backfill strategy when a user follows a new account
- Discusses CDN cache invalidation strategy
