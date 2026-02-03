---
layout: simple
title: "Design a URL Shortener"
permalink: /system_design/design-url-shortener
---

# Design a URL Shortener

A URL shortener service converts long URLs into short, memorable links that redirect to the original URL. Examples include TinyURL, bit.ly, and t.co.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Back of the Envelope Estimation](#back-of-the-envelope-estimation)
3. [System APIs](#system-apis)
4. [High-Level Design](#high-level-design)
5. [Short URL Generation](#short-url-generation)
6. [Database Design](#database-design)
7. [URL Redirection Flow](#url-redirection-flow)
8. [Deep Dive](#deep-dive)
9. [Implementation](#implementation)
10. [Real-World Systems](#real-world-systems)
11. [Key Takeaways](#key-takeaways)

---

## Requirements

### Functional Requirements

- **URL shortening**: Given a long URL, generate a shorter unique alias
- **URL redirection**: When user accesses short URL, redirect to original URL
- **Custom aliases** (optional): Users can choose custom short URLs
- **Expiration**: URLs can have optional expiration time

### Non-Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **High availability** | Service should be 99.99% available |
| **Low latency** | Redirection should happen in real-time (<100ms) |
| **Scalability** | Handle billions of URLs |
| **Non-predictable** | Short URLs should not be guessable |

### Extended Requirements

- Analytics (click counts, geographic data)
- Rate limiting
- API access for developers

---

## Back of the Envelope Estimation

### Traffic Estimates

Assume 100:1 read-to-write ratio (redirections vs. new URLs):

```
New URLs (write): 100 million/month
                  = ~40 URLs/second

Redirections (read): 10 billion/month
                     = ~4,000 redirections/second
```

### Storage Estimates

Assume each URL mapping is ~500 bytes and we keep data for 5 years:

```
URLs per month: 100 million
URLs in 5 years: 100M × 12 × 5 = 6 billion URLs

Storage needed: 6B × 500 bytes = 3 TB
```

### Bandwidth Estimates

```
Write: 40 URLs/s × 500 bytes = 20 KB/s
Read:  4,000/s × 500 bytes = 2 MB/s
```

### Memory Estimates (Cache)

Following 80-20 rule (20% of URLs generate 80% of traffic):

```
Daily read requests: 4,000/s × 86,400 = ~350 million/day
Cache 20%: 350M × 0.2 × 500 bytes = 35 GB
```

### Summary

| Metric | Value |
|--------|-------|
| New URLs | 40/second |
| Redirections | 4,000/second |
| Storage (5 years) | 3 TB |
| Cache memory | ~35 GB |

---

## System APIs

### REST API

```
POST /api/v1/shorten
Request:
{
    "long_url": "https://example.com/very/long/path?query=params",
    "custom_alias": "my-link",     // optional
    "expiration": "2025-12-31",    // optional
    "api_key": "user_api_key"
}

Response:
{
    "short_url": "https://short.ly/abc123",
    "long_url": "https://example.com/very/long/path?query=params",
    "created_at": "2024-01-15T10:30:00Z",
    "expires_at": "2025-12-31T00:00:00Z"
}
```

```
GET /{short_code}

Response: HTTP 301/302 Redirect to original URL
```

```
DELETE /api/v1/url/{short_code}
Headers: api_key: user_api_key

Response: HTTP 204 No Content
```

### Rate Limiting

Prevent abuse by limiting requests per API key:
- Free tier: 100 URLs/day
- Premium: 10,000 URLs/day

---

## High-Level Design

### Basic Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Clients                                     │
│                    (Web, Mobile, API Consumers)                          │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Load Balancer                                  │
│                        (Round Robin/Least Conn)                          │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
            ┌───────────────┐           ┌───────────────┐
            │   Web Server  │    ...    │   Web Server  │
            │   (Stateless) │           │   (Stateless) │
            └───────┬───────┘           └───────┬───────┘
                    │                           │
                    └─────────────┬─────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
    ┌───────────┐          ┌───────────┐          ┌───────────┐
    │   Cache   │          │  Database │          │Key Gen Svc│
    │  (Redis)  │          │  (MySQL)  │          │  (KGS)    │
    └───────────┘          └───────────┘          └───────────┘
```

### Component Overview

| Component | Responsibility |
|-----------|----------------|
| Load Balancer | Distribute traffic across servers |
| Web Servers | Handle API requests (stateless) |
| Cache | Store hot URLs for fast lookup |
| Database | Persistent storage for URL mappings |
| Key Generation Service | Pre-generate unique short codes |

---

## Short URL Generation

### Short Code Requirements

- **Length**: Short enough to remember, long enough for uniqueness
- **Characters**: [a-zA-Z0-9] = 62 characters
- **Length calculation**:

```
62^6 = ~57 billion combinations
62^7 = ~3.5 trillion combinations
```

With 6 characters, we can support **57 billion** unique URLs.

### Approach 1: Hash Function

Use MD5/SHA256 and take first N characters:

```
Long URL: https://example.com/long/path
MD5 Hash: 5d41402abc4b2a76b9719d911017c592
Short Code: 5d4140 (first 6 characters)
```

**Problems:**
- **Collisions**: Different URLs may produce same prefix
- **Solution**: Check database, re-hash with counter if collision

```python
def generate_short_code(long_url):
    counter = 0
    while True:
        hash_input = long_url + str(counter)
        hash_value = md5(hash_input).hexdigest()[:6]
        if not database.exists(hash_value):
            return hash_value
        counter += 1
```

### Approach 2: Base62 Encoding

Convert a unique integer ID to Base62:

```
ID: 125,984,756
Base62: "B3k9Zt"
```

**Encoding:**
```
0-9:   0-9
a-z:   10-35
A-Z:   36-61
```

**Pros:**
- No collisions (unique ID → unique code)
- Easy to decode for debugging

**Cons:**
- Predictable (sequential IDs visible)
- Requires unique ID generation

### Approach 3: Key Generation Service (KGS)

Pre-generate random keys and store in database:

```
┌───────────────────────────────────────────────────────┐
│                Key Generation Service                  │
├───────────────────────────────────────────────────────┤
│                                                        │
│   ┌─────────────────┐      ┌─────────────────┐        │
│   │  Unused Keys    │      │   Used Keys     │        │
│   │                 │      │                 │        │
│   │  abc123         │ ──►  │  xyz789         │        │
│   │  def456         │      │  pqr321         │        │
│   │  ghi789         │      │  ...            │        │
│   │  ...            │      │                 │        │
│   └─────────────────┘      └─────────────────┘        │
│                                                        │
│   Background process continuously generates new keys   │
└───────────────────────────────────────────────────────┘
```

**How it works:**
1. KGS pre-generates millions of unique 6-character keys
2. When a URL is shortened, grab a key from unused pool
3. Move key to used pool atomically
4. Background job replenishes unused pool

**Pros:**
- No collision handling
- Fast (no computation at request time)
- Non-predictable

**Cons:**
- Single point of failure (mitigate with replicas)
- Key synchronization complexity

### Approach Comparison

| Approach | Collision | Predictable | Complexity | Performance |
|----------|-----------|-------------|------------|-------------|
| Hash + Collision Check | Possible | No | Medium | Medium |
| Base62 + Auto-increment | None | Yes | Low | High |
| KGS | None | No | High | High |

### Recommended: KGS with Range Allocation

Combine KGS with the ID range approach:

```
┌─────────────────────────────────────────────────────────────────┐
│                        KGS Coordinator                           │
│                   (Allocates key ranges)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │ Server1 │         │ Server2 │         │ Server3 │
    │Range:   │         │Range:   │         │Range:   │
    │0-999999 │         │1M-1.99M │         │2M-2.99M │
    └─────────┘         └─────────┘         └─────────┘
```

Each server gets a range of IDs, converts them to Base62 locally.

---

## Database Design

### Schema Design

**URL Table:**
```sql
CREATE TABLE urls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    user_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    click_count BIGINT DEFAULT 0,

    INDEX idx_short_code (short_code),
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at)
);
```

**User Table:**
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(64) UNIQUE NOT NULL,
    tier ENUM('free', 'premium') DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Analytics Table (Optional):**
```sql
CREATE TABLE analytics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    url_id BIGINT NOT NULL,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer TEXT,
    country VARCHAR(2),

    INDEX idx_url_id (url_id),
    INDEX idx_clicked_at (clicked_at),
    FOREIGN KEY (url_id) REFERENCES urls(id)
);
```

### Database Choice

| Type | Database | Use Case |
|------|----------|----------|
| SQL | MySQL/PostgreSQL | Strong consistency, complex queries |
| NoSQL | DynamoDB/Cassandra | High write throughput, horizontal scaling |
| NoSQL | MongoDB | Flexible schema, moderate scale |

**Recommendation:** Start with MySQL, shard by short_code when needed.

### Sharding Strategy

**Option 1: Hash-based sharding on short_code**
```
Shard = hash(short_code) % num_shards
```

**Option 2: Range-based sharding**
```
Shard 1: a-m
Shard 2: n-z
Shard 3: A-M
Shard 4: N-Z0-9
```

---

## URL Redirection Flow

### Redirect Types

| Code | Type | Caching | Use Case |
|------|------|---------|----------|
| **301** | Permanent | Browser caches | Reduce server load |
| **302** | Temporary | No caching | Track every click |

**Trade-off:**
- 301 reduces server load but loses analytics
- 302 enables full analytics but higher load

### Redirection Flow

```
┌──────────┐     GET /abc123      ┌─────────────┐
│  Client  │ ──────────────────►  │ Load Balancer│
└──────────┘                      └──────┬──────┘
     ▲                                   │
     │                                   ▼
     │                           ┌─────────────┐
     │                           │ Web Server  │
     │                           └──────┬──────┘
     │                                  │
     │                    ┌─────────────┴─────────────┐
     │                    │                           │
     │                    ▼                           ▼
     │             ┌─────────────┐            ┌─────────────┐
     │             │    Cache    │◄──────────│  Database   │
     │             │   (Redis)   │ miss      │   (MySQL)   │
     │             └──────┬──────┘            └─────────────┘
     │                    │ hit
     │                    ▼
     │           Long URL found
     │                    │
     │    HTTP 302 Redirect
     └────────────────────┘
       Location: long_url
```

### Detailed Flow

1. User visits `https://short.ly/abc123`
2. Load balancer routes to web server
3. Web server checks cache for `abc123`
   - **Cache hit**: Return long URL
   - **Cache miss**: Query database, update cache
4. If URL found and not expired:
   - Return `HTTP 302` with `Location: <long_url>`
   - Async: Increment click count, log analytics
5. If URL not found or expired:
   - Return `HTTP 404 Not Found`

### Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                      Caching Layer                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Cache Key: short_code                                      │
│   Cache Value: {long_url, expires_at, created_at}            │
│   TTL: 24 hours (or until expiration)                        │
│                                                              │
│   Eviction: LRU (Least Recently Used)                        │
│   Memory: ~35GB for 20% of daily traffic                     │
│                                                              │
│   Cache Aside Pattern:                                       │
│   1. Check cache first                                       │
│   2. On miss, query DB                                       │
│   3. Populate cache                                          │
│   4. Return result                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Deep Dive

### Handling Hot URLs

Some URLs (viral content) get massive traffic:

**Solution 1: Cache Replication**
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│           Cache Cluster (Redis)          │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐     │
│  │Rep 1│  │Rep 2│  │Rep 3│  │Rep 4│     │
│  │abc12│  │abc12│  │abc12│  │abc12│     │
│  └─────┘  └─────┘  └─────┘  └─────┘     │
└─────────────────────────────────────────┘
```

**Solution 2: Local Cache + Distributed Cache**
```
App Server 1              App Server 2
┌─────────────┐          ┌─────────────┐
│ Local Cache │          │ Local Cache │
│ (in-memory) │          │ (in-memory) │
└──────┬──────┘          └──────┬──────┘
       │                        │
       └────────┬───────────────┘
                │
                ▼
       ┌─────────────┐
       │   Redis     │
       │ (Distributed)│
       └─────────────┘
```

### Duplicate URL Detection

Should `example.com/path` create new short URL if already exists?

**Option 1: Always create new**
- Pros: Simple, user gets unique URL
- Cons: Database bloat

**Option 2: Return existing**
- Pros: Save storage
- Cons: Complex lookup, privacy concerns (different users same short URL)

**Recommended: Per-user deduplication**
```python
def shorten_url(user_id, long_url):
    # Check if user already shortened this URL
    existing = db.find(user_id=user_id, long_url=long_url)
    if existing:
        return existing.short_code

    # Create new short URL
    short_code = generate_unique_code()
    db.insert(short_code, long_url, user_id)
    return short_code
```

### URL Expiration

**Background cleanup job:**
```python
# Run periodically (e.g., every hour)
def cleanup_expired_urls():
    expired = db.query("""
        SELECT short_code FROM urls
        WHERE expires_at < NOW()
        LIMIT 1000
    """)

    for url in expired:
        cache.delete(url.short_code)
        db.delete(url.short_code)
```

**Lazy expiration (check on access):**
```python
def redirect(short_code):
    url = cache.get(short_code) or db.get(short_code)

    if not url:
        return 404

    if url.expires_at and url.expires_at < now():
        cache.delete(short_code)
        return 404  # or 410 Gone

    return redirect_302(url.long_url)
```

### Analytics

**Real-time vs. Batch:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Analytics Pipeline                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Real-time Path (for dashboards):                           │
│   Click → Kafka → Stream Processor → Redis (counters)        │
│                                                              │
│   Batch Path (for reports):                                  │
│   Click → Kafka → S3 → Spark → Data Warehouse               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Click event schema:**
```json
{
    "short_code": "abc123",
    "timestamp": "2024-01-15T10:30:00Z",
    "ip_address": "203.0.113.42",
    "user_agent": "Mozilla/5.0...",
    "referrer": "https://twitter.com",
    "geo": {
        "country": "US",
        "city": "San Francisco"
    }
}
```

### Security Considerations

**1. Malicious URLs:**
```python
def shorten_url(long_url):
    # Check against blocklist
    if is_malicious(long_url):
        return error("URL blocked for safety")

    # Scan with Google Safe Browsing API
    if not safe_browsing_check(long_url):
        return error("Potentially unsafe URL")

    return create_short_url(long_url)
```

**2. Rate Limiting:**
```python
from redis import Redis

def rate_limit(api_key, limit=100, window=86400):
    key = f"rate:{api_key}:{today()}"
    count = redis.incr(key)

    if count == 1:
        redis.expire(key, window)

    if count > limit:
        raise RateLimitExceeded()
```

**3. Preventing Enumeration:**
- Use random/non-sequential short codes
- Add CAPTCHA for bulk creation
- Monitor for scraping patterns

---

## Implementation

### URL Shortening Service (Python)

```python
import hashlib
import random
import string
import time
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class URLMapping:
    short_code: str
    long_url: str
    user_id: Optional[int]
    created_at: datetime
    expires_at: Optional[datetime]
    click_count: int = 0

class URLShortener:
    BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase

    def __init__(self, db, cache, kgs):
        self.db = db
        self.cache = cache
        self.kgs = kgs  # Key Generation Service

    # === Short Code Generation ===

    def _base62_encode(self, num: int) -> str:
        """Convert integer to Base62 string"""
        if num == 0:
            return self.BASE62_CHARS[0]

        result = []
        while num:
            result.append(self.BASE62_CHARS[num % 62])
            num //= 62
        return ''.join(reversed(result))

    def _base62_decode(self, code: str) -> int:
        """Convert Base62 string to integer"""
        num = 0
        for char in code:
            num = num * 62 + self.BASE62_CHARS.index(char)
        return num

    def _generate_code_hash(self, url: str, attempt: int = 0) -> str:
        """Generate short code using MD5 hash"""
        data = f"{url}{attempt}".encode()
        hash_hex = hashlib.md5(data).hexdigest()
        # Take first 6 characters
        return hash_hex[:6]

    def _generate_code_kgs(self) -> str:
        """Get pre-generated key from KGS"""
        return self.kgs.get_key()

    # === Core Operations ===

    def shorten(
        self,
        long_url: str,
        user_id: Optional[int] = None,
        custom_alias: Optional[str] = None,
        expires_in_days: Optional[int] = None
    ) -> URLMapping:
        """Create a short URL"""

        # Validate URL
        if not self._is_valid_url(long_url):
            raise ValueError("Invalid URL format")

        # Check for malicious URL
        if self._is_malicious(long_url):
            raise ValueError("URL blocked for safety")

        # Handle custom alias
        if custom_alias:
            if self.db.exists(custom_alias):
                raise ValueError("Custom alias already taken")
            short_code = custom_alias
        else:
            # Generate short code
            short_code = self._generate_code_kgs()

        # Calculate expiration
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)

        # Create mapping
        mapping = URLMapping(
            short_code=short_code,
            long_url=long_url,
            user_id=user_id,
            created_at=datetime.utcnow(),
            expires_at=expires_at
        )

        # Store in database
        self.db.insert(mapping)

        # Populate cache
        self.cache.set(short_code, mapping, ttl=86400)

        return mapping

    def resolve(self, short_code: str) -> Optional[str]:
        """Resolve short code to original URL"""

        # Check cache first
        mapping = self.cache.get(short_code)

        if not mapping:
            # Cache miss - query database
            mapping = self.db.get(short_code)

            if mapping:
                # Populate cache
                self.cache.set(short_code, mapping, ttl=86400)

        if not mapping:
            return None

        # Check expiration
        if mapping.expires_at and mapping.expires_at < datetime.utcnow():
            self.cache.delete(short_code)
            return None

        # Async: increment click count
        self._record_click_async(short_code)

        return mapping.long_url

    def delete(self, short_code: str, user_id: int) -> bool:
        """Delete a short URL (owner only)"""
        mapping = self.db.get(short_code)

        if not mapping:
            return False

        if mapping.user_id != user_id:
            raise PermissionError("Not authorized to delete this URL")

        self.cache.delete(short_code)
        self.db.delete(short_code)
        return True

    # === Helper Methods ===

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        import re
        pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(pattern.match(url))

    def _is_malicious(self, url: str) -> bool:
        """Check URL against blocklist/Safe Browsing API"""
        # Simplified - in production, use Google Safe Browsing API
        blocklist = ['malware.com', 'phishing.net']
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain in blocklist

    def _record_click_async(self, short_code: str):
        """Record click event asynchronously"""
        # In production, push to message queue
        pass
```

### Key Generation Service

```python
import random
import string
import threading
from queue import Queue

class KeyGenerationService:
    """Pre-generate unique short codes"""

    CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
    KEY_LENGTH = 6
    POOL_SIZE = 100000
    REFILL_THRESHOLD = 10000

    def __init__(self, db):
        self.db = db
        self.unused_keys = Queue()
        self.lock = threading.Lock()

        # Load existing unused keys from database
        self._load_keys()

        # Start background key generation
        self._start_generator()

    def get_key(self) -> str:
        """Get a pre-generated key"""
        if self.unused_keys.qsize() < self.REFILL_THRESHOLD:
            self._trigger_refill()

        return self.unused_keys.get(timeout=5)

    def _generate_key(self) -> str:
        """Generate a random key"""
        return ''.join(random.choices(self.CHARS, k=self.KEY_LENGTH))

    def _load_keys(self):
        """Load unused keys from database"""
        keys = self.db.get_unused_keys(limit=self.POOL_SIZE)
        for key in keys:
            self.unused_keys.put(key)

    def _start_generator(self):
        """Start background key generation thread"""
        thread = threading.Thread(target=self._generate_keys_background, daemon=True)
        thread.start()

    def _generate_keys_background(self):
        """Background process to generate keys"""
        while True:
            if self.unused_keys.qsize() < self.POOL_SIZE:
                batch = []
                while len(batch) < 1000:
                    key = self._generate_key()
                    if not self.db.key_exists(key):
                        batch.append(key)

                # Insert batch to database
                self.db.insert_unused_keys(batch)

                # Add to queue
                for key in batch:
                    self.unused_keys.put(key)

            threading.Event().wait(1)  # Sleep 1 second

    def _trigger_refill(self):
        """Trigger async key generation"""
        # In production, send message to key generator workers
        pass
```

### FastAPI Web Server

```python
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
import time

app = FastAPI()

# Rate limiter using Redis
class RateLimiter:
    def __init__(self, redis, limit=100, window=86400):
        self.redis = redis
        self.limit = limit
        self.window = window

    def is_allowed(self, api_key: str) -> bool:
        key = f"rate:{api_key}:{int(time.time() // self.window)}"
        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, self.window)
        return count <= self.limit

# Request/Response models
class ShortenRequest(BaseModel):
    long_url: HttpUrl
    custom_alias: Optional[str] = None
    expiration_days: Optional[int] = None

class ShortenResponse(BaseModel):
    short_url: str
    long_url: str
    created_at: str
    expires_at: Optional[str] = None

# Endpoints
@app.post("/api/v1/shorten", response_model=ShortenResponse)
async def shorten_url(request: ShortenRequest, api_key: str):
    # Rate limiting
    if not rate_limiter.is_allowed(api_key):
        raise HTTPException(429, "Rate limit exceeded")

    try:
        mapping = url_shortener.shorten(
            long_url=str(request.long_url),
            custom_alias=request.custom_alias,
            expires_in_days=request.expiration_days
        )

        return ShortenResponse(
            short_url=f"https://short.ly/{mapping.short_code}",
            long_url=mapping.long_url,
            created_at=mapping.created_at.isoformat(),
            expires_at=mapping.expires_at.isoformat() if mapping.expires_at else None
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.get("/{short_code}")
async def redirect(short_code: str):
    long_url = url_shortener.resolve(short_code)

    if not long_url:
        raise HTTPException(404, "Short URL not found")

    # Use 302 to track clicks, 301 for permanent redirect
    return RedirectResponse(url=long_url, status_code=302)

@app.delete("/api/v1/url/{short_code}")
async def delete_url(short_code: str, api_key: str):
    user = get_user_by_api_key(api_key)

    if url_shortener.delete(short_code, user.id):
        return Response(status_code=204)

    raise HTTPException(404, "URL not found")
```

---

## Real-World Systems

### bit.ly

- **Scale**: Billions of links, 10+ billion clicks/month
- **Architecture**: Distributed across multiple data centers
- **Features**: Analytics, branded domains, QR codes
- **Tech stack**: Go, MySQL, Redis, Kafka

### TinyURL

- **Founded**: 2002 (one of the first URL shorteners)
- **Simplicity**: No analytics, just shortening
- **Scale**: 60+ million URLs per month

### Twitter (t.co)

- **Purpose**: All links on Twitter wrapped for:
  - Analytics
  - Malware detection
  - Spam prevention
- **Scale**: Handles all Twitter link traffic
- **Features**: Real-time link scanning

### Rebrandly

- **Focus**: Branded links (custom domains)
- **Features**:
  - Team collaboration
  - Deep linking
  - A/B testing

### Design Comparison

| Service | Primary Use | Key Feature |
|---------|-------------|-------------|
| bit.ly | Marketing | Analytics |
| TinyURL | Simple shortening | Simplicity |
| t.co | Twitter ecosystem | Security scanning |
| Rebrandly | Enterprise | Custom branding |

---

## Key Takeaways

### 1. Short Code Generation

- **KGS (Key Generation Service)** is the most scalable approach
- Pre-generate keys to avoid runtime computation
- Base62 encoding provides ~57 billion combinations with 6 characters

### 2. Database Design

- Start simple (single MySQL), shard when needed
- Use consistent hashing for shard selection
- Consider NoSQL for higher write throughput

### 3. Caching is Critical

- Cache hot URLs (20% of URLs = 80% of traffic)
- Use read-through caching pattern
- Consider local + distributed cache for hot URLs

### 4. Redirect Type Matters

- **301**: Better for SEO, browser caches
- **302**: Better for analytics, server sees every request

### 5. Trade-offs

| Decision | Option A | Option B |
|----------|----------|----------|
| ID Generation | Sequential (predictable) | Random (secure) |
| Redirect | 301 (cached) | 302 (trackable) |
| Storage | SQL (consistent) | NoSQL (scalable) |
| Duplicates | Dedupe (save space) | Allow (privacy) |

### 6. Production Checklist

- [ ] Rate limiting to prevent abuse
- [ ] URL validation and malware scanning
- [ ] Expiration handling (lazy + batch cleanup)
- [ ] Analytics pipeline (async, non-blocking)
- [ ] Monitoring and alerting
- [ ] Database backup and disaster recovery

### 7. Scalability Roadmap

```
Phase 1: Single Server
├── MySQL + Redis
├── ~1000 QPS
└── ~1M URLs

Phase 2: Horizontal Scaling
├── Load balancer + multiple app servers
├── MySQL primary + replicas
├── Redis cluster
├── ~10K QPS
└── ~100M URLs

Phase 3: Distributed Architecture
├── Multiple data centers
├── Sharded databases
├── CDN for static assets
├── ~100K QPS
└── ~10B URLs
```

### 8. Interview Discussion Points

1. **Why not just use hash?** Collision handling complexity
2. **Why 62 characters?** URL-safe, case-sensitive (more combinations)
3. **301 vs 302?** Trade-off between caching and analytics
4. **How to handle hot URLs?** Multi-layer caching, replication
5. **Expiration strategy?** Lazy deletion + batch cleanup
6. **Custom domains?** DNS CNAME, SSL certificates per domain
