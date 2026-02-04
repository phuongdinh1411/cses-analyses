---
layout: simple
title: "Design a News Feed System"
permalink: /system_design/design-news-feed
---

# Design a News Feed System

A news feed system displays a personalized, constantly updating list of posts from friends, pages, and groups. Examples include Facebook News Feed, Twitter Timeline, and Instagram Feed.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Back of the Envelope Estimation](#back-of-the-envelope-estimation)
3. [System APIs](#system-apis)
4. [High-Level Design](#high-level-design)
5. [Feed Generation Strategies](#feed-generation-strategies)
6. [Database Design](#database-design)
7. [Deep Dive](#deep-dive)
8. [Ranking Algorithm](#ranking-algorithm)
9. [Implementation](#implementation)
10. [Key Takeaways](#key-takeaways)

---

## Requirements

### Functional Requirements

- **Post creation**: Users can create posts with text, images, videos
- **Feed generation**: Generate personalized feed from friends/followees
- **Feed viewing**: Users can view their news feed with infinite scroll
- **Interactions**: Like, comment, share posts

### Non-Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Low latency** | Feed should load in < 500ms |
| **High availability** | 99.99% uptime |
| **Scalability** | Support billions of users |
| **Consistency** | Eventual consistency acceptable |

### Extended Requirements

- Push notifications for new posts
- Support for different media types
- Content moderation
- Ad integration

---

## Back of the Envelope Estimation

### Traffic Estimates

```
Daily Active Users (DAU): 500 million
Avg friends per user: 500
Avg posts per user per day: 2

Feed refreshes per user per day: 10
Total feed requests: 500M × 10 = 5 billion/day
                   = ~58,000 requests/second

New posts: 500M × 2 = 1 billion posts/day
         = ~12,000 posts/second
```

### Storage Estimates

```
Post metadata: ~1 KB per post
Posts per day: 1 billion
Posts per year: 365 billion

Storage per year: 365B × 1KB = 365 TB (metadata only)
Media storage: 10× metadata = 3.65 PB/year
```

### Memory Estimates (Cache)

```
Hot posts to cache: 20% of daily posts
Cache size: 200M posts × 1KB = 200 GB
Feed cache per user: 500 posts × 100 bytes = 50 KB
Active user feed cache: 100M × 50KB = 5 TB
```

### Summary

| Metric | Value |
|--------|-------|
| Feed requests | 58,000/second |
| New posts | 12,000/second |
| Storage (metadata) | 365 TB/year |
| Feed cache | 5 TB |

---

## System APIs

### Create Post

```
POST /v1/posts
```

**Request:**
```json
{
  "user_id": "user123",
  "content": "Hello world!",
  "media_ids": ["img1", "img2"],
  "privacy": "friends",
  "location": "San Francisco"
}
```

**Response:**
```json
{
  "post_id": "post456",
  "created_at": "2024-01-15T10:30:00Z",
  "status": "published"
}
```

### Get News Feed

```
GET /v1/feed?user_id={user_id}&page_token={token}&limit={limit}
```

**Response:**
```json
{
  "posts": [
    {
      "post_id": "post789",
      "author": {
        "user_id": "user456",
        "name": "John Doe",
        "avatar_url": "..."
      },
      "content": "Great day!",
      "media": [...],
      "likes_count": 150,
      "comments_count": 23,
      "created_at": "2024-01-15T09:00:00Z"
    }
  ],
  "next_page_token": "abc123"
}
```

---

## High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         Load Balancer                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Post Service │    │ Feed Service  │    │ User Service  │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Post Cache   │    │  Feed Cache   │    │  User Cache   │
│   (Redis)     │    │   (Redis)     │    │   (Redis)     │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Post DB     │    │   Feed DB     │    │   User DB     │
│  (Cassandra)  │    │   (Redis)     │    │  (PostgreSQL) │
└───────────────┘    └───────────────┘    └───────────────┘
        │
        ▼
┌───────────────┐
│ Media Storage │
│     (S3)      │
└───────────────┘
```

### Components

| Component | Responsibility |
|-----------|----------------|
| **Post Service** | Create, update, delete posts |
| **Feed Service** | Generate and serve news feeds |
| **User Service** | Manage user profiles and relationships |
| **Notification Service** | Push notifications for new posts |
| **Ranking Service** | Score and rank posts |

---

## Feed Generation Strategies

### 1. Pull Model (Fan-out on Read)

Generate feed when user requests it.

```
User Request → Get Friends List → Fetch Recent Posts → Rank → Return
```

**Pros:**
- No precomputation needed
- Fresh data always
- Works well for users with few friends

**Cons:**
- High latency for users with many friends
- Heavy load on read

**Best for:** Users with many followers (celebrities)

### 2. Push Model (Fan-out on Write)

Pre-generate feeds when posts are created.

```
New Post → Get Followers List → Write to Each Follower's Feed
```

**Pros:**
- Fast read (O(1))
- Pre-computed feeds

**Cons:**
- Wasteful for inactive users
- High write amplification
- Celebrity problem (millions of followers)

**Best for:** Users with few followers

### 3. Hybrid Model (Recommended)

Combine both approaches based on user type.

```
┌─────────────────┐
│    New Post     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Is user famous? │
│ (>10K followers)│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   YES        NO
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│ Pull  │ │ Push  │
│ Model │ │ Model │
└───────┘ └───────┘
```

**Implementation:**
- Regular users: Push to followers' feeds
- Celebrities: Pull at read time and merge
- Cache hot posts from celebrities

---

## Database Design

### User Table (PostgreSQL)

```sql
CREATE TABLE users (
    user_id         BIGINT PRIMARY KEY,
    username        VARCHAR(50) UNIQUE,
    email           VARCHAR(100) UNIQUE,
    created_at      TIMESTAMP,
    follower_count  INT DEFAULT 0,
    following_count INT DEFAULT 0
);
```

### Post Table (Cassandra)

```sql
CREATE TABLE posts (
    post_id     UUID,
    user_id     BIGINT,
    content     TEXT,
    media_ids   LIST<UUID>,
    created_at  TIMESTAMP,
    likes_count INT,
    PRIMARY KEY (user_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);
```

### Feed Table (Redis)

```
Key: feed:{user_id}
Value: Sorted Set of (post_id, timestamp)

ZADD feed:user123 1705312200 post456
ZADD feed:user123 1705312100 post789

ZREVRANGE feed:user123 0 49  # Get top 50 posts
```

### Friendship Table (Cassandra)

```sql
CREATE TABLE followers (
    user_id     BIGINT,
    follower_id BIGINT,
    created_at  TIMESTAMP,
    PRIMARY KEY (user_id, follower_id)
);

CREATE TABLE following (
    user_id      BIGINT,
    following_id BIGINT,
    created_at   TIMESTAMP,
    PRIMARY KEY (user_id, following_id)
);
```

---

## Deep Dive

### 1. Feed Publishing Flow

```
┌──────────────┐
│ User creates │
│    post      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Post Service │──────────────────────┐
│ saves post   │                      │
└──────┬───────┘                      │
       │                              │
       ▼                              ▼
┌──────────────┐              ┌───────────────┐
│ Message Queue│              │ Media Service │
│  (Kafka)     │              │ upload to S3  │
└──────┬───────┘              └───────────────┘
       │
       ▼
┌──────────────┐
│ Fanout       │
│ Workers      │
└──────┬───────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ User A's │   │ User B's │   │ User C's │
│  Feed    │   │  Feed    │   │  Feed    │
└──────────┘   └──────────┘   └──────────┘
```

### 2. Feed Reading Flow

```
┌──────────────┐
│ User requests│
│    feed      │
└──────┬───────┘
       │
       ▼
┌──────────────┐     Cache Hit
│ Feed Cache   │─────────────────────┐
│   (Redis)    │                     │
└──────┬───────┘                     │
       │ Cache Miss                  │
       ▼                             │
┌──────────────┐                     │
│ Feed Service │                     │
│              │                     │
│ 1. Get pre-  │                     │
│    computed  │                     │
│    feed      │                     │
│              │                     │
│ 2. Fetch     │                     │
│    celebrity │                     │
│    posts     │                     │
│              │                     │
│ 3. Merge &   │                     │
│    rank      │                     │
└──────┬───────┘                     │
       │                             │
       ▼                             ▼
┌──────────────────────────────────────┐
│           Return Feed                │
└──────────────────────────────────────┘
```

### 3. Handling the Celebrity Problem

When a celebrity with millions of followers posts:

**Option 1: Selective Push**
- Only push to active followers (logged in last 7 days)
- Pull for inactive followers when they return

**Option 2: Tiered Fanout**
- Immediate: Push to top 10K most engaged followers
- Background: Push to remaining followers over time

**Option 3: Pure Pull for Celebrities**
- Never push celebrity posts
- Always fetch at read time
- Cache aggressively

### 4. Cache Strategy

```
┌─────────────────────────────────────────┐
│              Cache Layers               │
├─────────────────────────────────────────┤
│                                         │
│  L1: CDN (Edge Cache)                   │
│      - Static media                     │
│      - TTL: 24 hours                    │
│                                         │
│  L2: Application Cache (Redis Cluster)  │
│      - User feeds                       │
│      - Hot posts                        │
│      - TTL: 1 hour                      │
│                                         │
│  L3: Database Query Cache               │
│      - Frequently accessed data         │
│      - TTL: 5 minutes                   │
│                                         │
└─────────────────────────────────────────┘
```

---

## Ranking Algorithm

### Factors for Ranking

| Factor | Weight | Description |
|--------|--------|-------------|
| **Recency** | High | Newer posts rank higher |
| **Engagement** | High | Likes, comments, shares |
| **Relationship** | Medium | Close friends rank higher |
| **Content type** | Medium | User preferences |
| **Creator** | Low | Past interaction history |

### Simple Ranking Formula

```python
def calculate_score(post, user):
    # Time decay (half-life = 6 hours)
    hours_old = (now - post.created_at).hours
    time_score = 1 / (1 + hours_old / 6)

    # Engagement score
    engagement = (
        post.likes * 1 +
        post.comments * 2 +
        post.shares * 3
    )
    engagement_score = log(1 + engagement)

    # Relationship score
    relationship = get_relationship_strength(user, post.author)

    # Final score
    score = (
        time_score * 0.4 +
        engagement_score * 0.3 +
        relationship * 0.3
    )
    return score
```

### ML-Based Ranking

For production systems:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Feature   │────▶│    Model    │────▶│   Ranked    │
│  Extraction │     │ (XGBoost/   │     │    Feed     │
│             │     │  Neural Net)│     │             │
└─────────────┘     └─────────────┘     └─────────────┘

Features:
- User features (age, location, interests)
- Post features (type, length, media)
- Context features (time of day, device)
- Interaction features (past clicks, likes)
```

---

## Implementation

### Feed Service (Python)

```python
class FeedService:
    def __init__(self, redis_client, post_db, user_db):
        self.redis = redis_client
        self.post_db = post_db
        self.user_db = user_db
        self.FEED_SIZE = 500
        self.CELEBRITY_THRESHOLD = 10000

    def get_feed(self, user_id: str, limit: int = 50,
                 offset: int = 0) -> List[Post]:
        # Try cache first
        cached = self.redis.zrevrange(
            f"feed:{user_id}", offset, offset + limit - 1
        )

        if cached:
            post_ids = [item.decode() for item in cached]
            posts = self.post_db.get_posts(post_ids)
            return posts

        # Generate feed
        feed = self._generate_feed(user_id)

        # Cache it
        self._cache_feed(user_id, feed)

        return feed[offset:offset + limit]

    def _generate_feed(self, user_id: str) -> List[Post]:
        # Get pre-computed feed (from push)
        precomputed = self.redis.zrevrange(
            f"feed:{user_id}", 0, self.FEED_SIZE - 1
        )

        # Get celebrity posts (pull)
        celebrities = self.user_db.get_celebrity_following(user_id)
        celebrity_posts = []
        for celeb_id in celebrities:
            posts = self.post_db.get_recent_posts(
                celeb_id, limit=10
            )
            celebrity_posts.extend(posts)

        # Merge and rank
        all_posts = list(precomputed) + celebrity_posts
        ranked = self._rank_posts(all_posts, user_id)

        return ranked[:self.FEED_SIZE]

    def _rank_posts(self, posts: List[Post],
                    user_id: str) -> List[Post]:
        scored = []
        for post in posts:
            score = self._calculate_score(post, user_id)
            scored.append((score, post))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [post for _, post in scored]

    def _calculate_score(self, post: Post, user_id: str) -> float:
        now = datetime.utcnow()
        hours_old = (now - post.created_at).total_seconds() / 3600

        time_score = 1 / (1 + hours_old / 6)
        engagement = (
            post.likes_count +
            post.comments_count * 2 +
            post.shares_count * 3
        )
        engagement_score = math.log(1 + engagement)

        return time_score * 0.5 + engagement_score * 0.5


class FanoutService:
    def __init__(self, redis_client, user_db, message_queue):
        self.redis = redis_client
        self.user_db = user_db
        self.queue = message_queue
        self.CELEBRITY_THRESHOLD = 10000

    def fanout_post(self, post: Post):
        author = self.user_db.get_user(post.user_id)

        if author.follower_count > self.CELEBRITY_THRESHOLD:
            # Celebrity: don't fanout, will be pulled
            return

        # Get all followers
        followers = self.user_db.get_followers(post.user_id)

        # Batch fanout
        for batch in chunks(followers, 1000):
            self.queue.publish('fanout', {
                'post_id': post.post_id,
                'timestamp': post.created_at.timestamp(),
                'follower_ids': batch
            })

    def process_fanout(self, message):
        post_id = message['post_id']
        timestamp = message['timestamp']
        follower_ids = message['follower_ids']

        pipeline = self.redis.pipeline()
        for follower_id in follower_ids:
            pipeline.zadd(
                f"feed:{follower_id}",
                {post_id: timestamp}
            )
            # Trim to keep feed size bounded
            pipeline.zremrangebyrank(
                f"feed:{follower_id}", 0, -501
            )
        pipeline.execute()
```

### Post Service (Go)

```go
type PostService struct {
    db       *cassandra.Session
    cache    *redis.Client
    queue    *kafka.Producer
    s3       *s3.Client
}

func (s *PostService) CreatePost(ctx context.Context,
    req *CreatePostRequest) (*Post, error) {

    post := &Post{
        PostID:    uuid.New(),
        UserID:    req.UserID,
        Content:   req.Content,
        MediaIDs:  req.MediaIDs,
        CreatedAt: time.Now(),
    }

    // Save to database
    err := s.db.Query(`
        INSERT INTO posts (post_id, user_id, content,
                          media_ids, created_at)
        VALUES (?, ?, ?, ?, ?)
    `, post.PostID, post.UserID, post.Content,
       post.MediaIDs, post.CreatedAt).Exec()

    if err != nil {
        return nil, err
    }

    // Publish to fanout queue
    msg, _ := json.Marshal(post)
    s.queue.Produce(&kafka.Message{
        Topic: "new-posts",
        Value: msg,
    })

    return post, nil
}

func (s *PostService) GetPost(ctx context.Context,
    postID string) (*Post, error) {

    // Try cache
    cached, err := s.cache.Get(ctx,
        fmt.Sprintf("post:%s", postID)).Result()
    if err == nil {
        var post Post
        json.Unmarshal([]byte(cached), &post)
        return &post, nil
    }

    // Query database
    var post Post
    err = s.db.Query(`
        SELECT post_id, user_id, content, media_ids,
               created_at, likes_count
        FROM posts WHERE post_id = ?
    `, postID).Scan(&post.PostID, &post.UserID,
        &post.Content, &post.MediaIDs,
        &post.CreatedAt, &post.LikesCount)

    if err != nil {
        return nil, err
    }

    // Cache for future
    data, _ := json.Marshal(post)
    s.cache.Set(ctx, fmt.Sprintf("post:%s", postID),
        data, time.Hour)

    return &post, nil
}
```

---

## Key Takeaways

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Feed generation | Hybrid push/pull | Balance latency and write cost |
| Post storage | Cassandra | High write throughput, time-series |
| Feed storage | Redis | Fast sorted set operations |
| Media storage | S3 + CDN | Cost-effective, scalable |

### Scalability Patterns

1. **Horizontal scaling**: Shard by user_id
2. **Caching**: Multi-layer cache strategy
3. **Async processing**: Message queues for fanout
4. **Read replicas**: For read-heavy workload

### Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Push model | Fast reads | High write cost |
| Pull model | Fresh data | Slow reads |
| Hybrid | Balanced | Complex |

### Common Interview Questions

1. How do you handle the celebrity problem?
2. How do you ensure feed freshness?
3. How do you rank posts?
4. How do you handle real-time updates?
5. How do you scale to billions of users?

### Related Topics

- [Consistent Hashing](/cses-analyses/system_design/consistent-hashing) - Data distribution
- [Design Key-Value Store](/cses-analyses/system_design/design-key-value-store) - Feed storage
- [Design URL Shortener](/cses-analyses/system_design/design-url-shortener) - Link handling
