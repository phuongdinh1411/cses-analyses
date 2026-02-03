---
layout: simple
title: "System Design: Web Crawler"
permalink: /system_design/design-web-crawler
---

# System Design: Web Crawler

## A Comprehensive Guide to Designing a Scalable Web Crawler

---

## Table of Contents

1. [Problem Understanding](#1-problem-understanding)
2. [Requirements](#2-requirements)
3. [Back-of-the-Envelope Estimation](#3-back-of-the-envelope-estimation)
4. [High-Level Architecture](#4-high-level-architecture)
5. [Component Deep Dive](#5-component-deep-dive)
6. [Data Flow](#6-data-flow)
7. [URL Frontier Design](#7-url-frontier-design)
8. [Politeness and Crawl Rate](#8-politeness-and-crawl-rate)
9. [Content Processing Pipeline](#9-content-processing-pipeline)
10. [Storage Design](#10-storage-design)
11. [Scalability](#11-scalability)
12. [Fault Tolerance](#12-fault-tolerance)
13. [Monitoring and Metrics](#13-monitoring-and-metrics)
14. [Advanced Topics](#14-advanced-topics)
15. [Interview Tips](#15-interview-tips)

---

## 1. Problem Understanding

### What is a Web Crawler?

A web crawler (also known as spider or bot) is a system that:
- **Discovers** web pages by following links
- **Downloads** content from those pages
- **Stores** the content for further processing (search indexing, data mining, etc.)

### Use Cases

| Use Case | Description | Scale |
|----------|-------------|-------|
| Search Engine | Google, Bing - index the web | Billions of pages |
| Data Mining | Extract specific data (prices, news) | Millions of pages |
| Web Archiving | Internet Archive - preserve web history | Billions of pages |
| SEO Tools | Analyze website structure | Thousands of pages |
| Content Monitoring | Track changes on specific sites | Hundreds of pages |

### Key Challenges

```
┌─────────────────────────────────────────────────────────────┐
│                  WEB CRAWLER CHALLENGES                     │
├─────────────────────────────────────────────────────────────┤
│  1. Scale: Billions of pages to crawl                       │
│  2. Politeness: Don't overwhelm target servers              │
│  3. Freshness: Keep content up-to-date                      │
│  4. Duplicates: Detect and avoid duplicate content          │
│  5. Spider Traps: Infinite loops of generated URLs          │
│  6. Dynamic Content: JavaScript-rendered pages              │
│  7. Robots.txt: Respect website crawling policies           │
│  8. Distributed: Coordinate multiple crawlers               │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Requirements

### Functional Requirements

```
1. Given seed URLs, crawl and discover new URLs
2. Download and store web page content
3. Respect robots.txt and crawl policies
4. Handle different content types (HTML, PDF, images)
5. Detect and handle duplicates
6. Support URL prioritization
7. Re-crawl pages based on update frequency
```

### Non-Functional Requirements

```
1. Scalability: Handle billions of pages
2. Politeness: Configurable rate limits per domain
3. Robustness: Handle failures gracefully
4. Extensibility: Pluggable content processors
5. Performance: High throughput (thousands of pages/sec)
6. Freshness: Configurable re-crawl policies
```

### Out of Scope (Clarify with Interviewer)

```
- Search indexing and ranking
- Natural language processing
- Image/video analysis
- User-facing search interface
```

---

## 3. Back-of-the-Envelope Estimation

### Scale Assumptions

```
Target: Crawl 1 billion pages per month

Pages per day:    1B / 30 = ~33 million pages/day
Pages per second: 33M / 86400 = ~400 pages/second

With overhead and burst capacity:
Target throughput: ~1000 pages/second
```

### Storage Estimation

```
Average page size: 100 KB (HTML + metadata)
Pages to store: 1 billion

Raw storage: 1B × 100 KB = 100 TB

With compression (5:1): ~20 TB
With metadata and indexes: ~30 TB total

Monthly growth: ~30 TB
```

### Bandwidth Estimation

```
Pages per second: 1000
Average page size: 100 KB

Bandwidth: 1000 × 100 KB = 100 MB/s = 800 Mbps

Peak (3x): ~2.4 Gbps
```

### URL Storage

```
URLs discovered: ~10 billion (including duplicates)
Average URL length: 100 bytes

URL storage: 10B × 100 = 1 TB

With hash-based deduplication: ~500 GB
```

### Summary

```
┌────────────────────────────────────────┐
│         ESTIMATION SUMMARY             │
├────────────────────────────────────────┤
│  Throughput:     1000 pages/sec        │
│  Bandwidth:      ~1 Gbps               │
│  Storage/month:  ~30 TB                │
│  URL storage:    ~500 GB               │
│  Crawlers:       50-100 machines       │
└────────────────────────────────────────┘
```

---

## 4. High-Level Architecture

### System Overview

```
                                    ┌─────────────────┐
                                    │   Seed URLs     │
                                    └────────┬────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           URL FRONTIER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  Priority   │  │   Domain    │  │   Politeness │                 │
│  │   Queue     │  │   Queues    │  │    Manager   │                 │
│  └─────────────┘  └─────────────┘  └──────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         CRAWLER WORKERS                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Worker 1 │  │ Worker 2 │  │ Worker 3 │  │ Worker N │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    ▼                        ▼                        ▼
           ┌───────────────┐        ┌───────────────┐        ┌───────────────┐
           │  DNS Resolver │        │ Robots.txt    │        │    HTTP       │
           │    (Cache)    │        │    Cache      │        │   Fetcher     │
           └───────────────┘        └───────────────┘        └───────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CONTENT PROCESSOR                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  HTML    │  │ Duplicate│  │   Link   │  │  Content │            │
│  │  Parser  │  │ Detector │  │ Extractor│  │  Store   │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    ▼                        ▼                        ▼
           ┌───────────────┐        ┌───────────────┐        ┌───────────────┐
           │  URL Storage  │        │    Content    │        │   Metadata    │
           │  (Seen URLs)  │        │    Storage    │        │   Database    │
           └───────────────┘        └───────────────┘        └───────────────┘
```

### Component Summary

| Component | Purpose | Technology Options |
|-----------|---------|-------------------|
| URL Frontier | Manage URLs to crawl | Redis, Kafka, Custom |
| Crawler Workers | Fetch web pages | Distributed workers |
| DNS Resolver | Resolve domain names | Local DNS cache |
| Robots.txt Cache | Store crawl policies | Redis, Local cache |
| Content Processor | Parse and extract | Jsoup, BeautifulSoup |
| Duplicate Detector | Detect duplicate content | SimHash, MinHash |
| Storage | Store content | S3, HDFS, Cassandra |

---

## 5. Component Deep Dive

### 5.1 URL Frontier

The URL Frontier is the "brain" of the crawler, managing what to crawl next.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         URL FRONTIER                                │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    PRIORITIZER                               │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │   │
│  │  │Priority │  │Priority │  │Priority │  │Priority │        │   │
│  │  │Queue P1 │  │Queue P2 │  │Queue P3 │  │Queue PN │        │   │
│  │  │(High)   │  │(Medium) │  │(Low)    │  │(Lowest) │        │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    POLITENESS ENFORCER                       │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │   │
│  │  │Domain   │  │Domain   │  │Domain   │  │Domain   │        │   │
│  │  │Queue    │  │Queue    │  │Queue    │  │Queue    │        │   │
│  │  │google   │  │amazon   │  │wiki     │  │...      │        │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│                       Queue Selector                                │
│                       (Round Robin)                                 │
└─────────────────────────────────────────────────────────────────────┘
```

**Key responsibilities:**

```python
class URLFrontier:
    """
    Manages URLs to be crawled with prioritization and politeness.
    """

    def __init__(self):
        self.priority_queues = {}     # Priority -> Queue
        self.domain_queues = {}       # Domain -> Queue
        self.domain_last_access = {}  # Domain -> Timestamp
        self.seen_urls = BloomFilter()  # Fast duplicate check

    def add_url(self, url: str, priority: int):
        """Add URL to frontier if not seen before."""
        if self.seen_urls.contains(url):
            return False

        self.seen_urls.add(url)
        domain = extract_domain(url)

        # Add to priority queue
        self.priority_queues[priority].add(url)

        # Add to domain queue for politeness
        if domain not in self.domain_queues:
            self.domain_queues[domain] = Queue()
        self.domain_queues[domain].add(url)

        return True

    def get_next_url(self) -> Optional[str]:
        """Get next URL respecting politeness constraints."""
        for domain, queue in self.domain_queues.items():
            if self._can_crawl_domain(domain) and not queue.empty():
                url = queue.pop()
                self.domain_last_access[domain] = time.now()
                return url
        return None

    def _can_crawl_domain(self, domain: str) -> bool:
        """Check if enough time has passed since last crawl."""
        if domain not in self.domain_last_access:
            return True

        elapsed = time.now() - self.domain_last_access[domain]
        min_delay = self._get_crawl_delay(domain)
        return elapsed >= min_delay
```

### 5.2 Crawler Worker

```python
class CrawlerWorker:
    """
    Worker that fetches and processes web pages.
    """

    def __init__(self, worker_id: int):
        self.worker_id = worker_id
        self.http_client = HTTPClient(timeout=30)
        self.dns_cache = DNSCache()
        self.robots_cache = RobotsCache()

    async def crawl(self, url: str) -> CrawlResult:
        """Main crawl loop for a single URL."""
        try:
            # Step 1: Check robots.txt
            if not await self._is_allowed(url):
                return CrawlResult(url, status="blocked_by_robots")

            # Step 2: Resolve DNS (with caching)
            ip = await self.dns_cache.resolve(url)

            # Step 3: Fetch the page
            response = await self.http_client.get(url)

            # Step 4: Process based on status
            if response.status == 200:
                return CrawlResult(
                    url=url,
                    status="success",
                    content=response.body,
                    content_type=response.headers.get("Content-Type"),
                    fetched_at=time.now()
                )
            elif response.status in (301, 302):
                # Handle redirect
                return CrawlResult(
                    url=url,
                    status="redirect",
                    redirect_url=response.headers.get("Location")
                )
            else:
                return CrawlResult(url=url, status=f"http_{response.status}")

        except TimeoutError:
            return CrawlResult(url=url, status="timeout")
        except Exception as e:
            return CrawlResult(url=url, status="error", error=str(e))

    async def _is_allowed(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt."""
        domain = extract_domain(url)
        robots = await self.robots_cache.get(domain)
        return robots.is_allowed(url, user_agent="MyBot")
```

### 5.3 DNS Resolver with Cache

DNS resolution can be a bottleneck. Caching is essential.

```python
class DNSCache:
    """
    Caching DNS resolver to avoid repeated lookups.
    """

    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}  # domain -> (ip, expiry_time)
        self.ttl = ttl_seconds

    async def resolve(self, url: str) -> str:
        domain = extract_domain(url)

        # Check cache
        if domain in self.cache:
            ip, expiry = self.cache[domain]
            if time.now() < expiry:
                return ip

        # Cache miss - do actual DNS lookup
        ip = await self._dns_lookup(domain)
        self.cache[domain] = (ip, time.now() + self.ttl)
        return ip

    async def _dns_lookup(self, domain: str) -> str:
        """Actual DNS resolution."""
        # Use local DNS server or public DNS (8.8.8.8)
        return await dns.resolve(domain)
```

### 5.4 Robots.txt Parser

```python
class RobotsCache:
    """
    Cache and parse robots.txt files.
    """

    def __init__(self):
        self.cache = {}  # domain -> RobotsRules
        self.ttl = 86400  # 24 hours

    async def get(self, domain: str) -> RobotsRules:
        if domain in self.cache:
            rules, expiry = self.cache[domain]
            if time.now() < expiry:
                return rules

        # Fetch robots.txt
        robots_url = f"https://{domain}/robots.txt"
        try:
            response = await http.get(robots_url, timeout=10)
            rules = self._parse_robots(response.body)
        except:
            rules = RobotsRules.allow_all()

        self.cache[domain] = (rules, time.now() + self.ttl)
        return rules

    def _parse_robots(self, content: str) -> RobotsRules:
        """Parse robots.txt content."""
        rules = RobotsRules()

        current_agent = None
        for line in content.split('\n'):
            line = line.strip().lower()

            if line.startswith('user-agent:'):
                current_agent = line.split(':')[1].strip()
            elif line.startswith('disallow:') and current_agent in ('*', 'mybot'):
                path = line.split(':')[1].strip()
                rules.add_disallow(path)
            elif line.startswith('crawl-delay:') and current_agent in ('*', 'mybot'):
                delay = float(line.split(':')[1].strip())
                rules.set_crawl_delay(delay)

        return rules
```

---

## 6. Data Flow

### Complete Crawl Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CRAWL DATA FLOW                              │
└─────────────────────────────────────────────────────────────────────┘

1. URL SELECTION
   ┌─────────┐     ┌─────────────┐     ┌─────────────┐
   │ Frontier│────▶│  Politeness │────▶│   Worker    │
   │         │     │   Check     │     │  Assignment │
   └─────────┘     └─────────────┘     └─────────────┘

2. PRE-FETCH CHECKS
   ┌─────────┐     ┌─────────────┐     ┌─────────────┐
   │  DNS    │────▶│ Robots.txt  │────▶│   URL       │
   │ Resolve │     │   Check     │     │ Validation  │
   └─────────┘     └─────────────┘     └─────────────┘

3. FETCH
   ┌─────────┐     ┌─────────────┐     ┌─────────────┐
   │  HTTP   │────▶│  Handle     │────▶│  Download   │
   │ Request │     │  Redirects  │     │  Content    │
   └─────────┘     └─────────────┘     └─────────────┘

4. PROCESSING
   ┌─────────┐     ┌─────────────┐     ┌─────────────┐
   │  Parse  │────▶│  Duplicate  │────▶│  Extract    │
   │  HTML   │     │  Detection  │     │  Links      │
   └─────────┘     └─────────────┘     └─────────────┘

5. STORAGE
   ┌─────────┐     ┌─────────────┐     ┌─────────────┐
   │  Store  │────▶│  Update     │────▶│  Add New    │
   │ Content │     │  Metadata   │     │  URLs       │
   └─────────┘     └─────────────┘     └─────────────┘
```

### Sequence Diagram

```
    Worker          Frontier        DNS Cache      Web Server       Storage
      │                │                │               │              │
      │  get_next_url  │                │               │              │
      │───────────────▶│                │               │              │
      │                │                │               │              │
      │  URL           │                │               │              │
      │◀───────────────│                │               │              │
      │                │                │               │              │
      │  resolve_dns   │                │               │              │
      │────────────────────────────────▶│               │              │
      │                │                │               │              │
      │  IP address    │                │               │              │
      │◀────────────────────────────────│               │              │
      │                │                │               │              │
      │  HTTP GET      │                │               │              │
      │──────────────────────────────────────────────▶ │              │
      │                │                │               │              │
      │  HTML content  │                │               │              │
      │◀──────────────────────────────────────────────│              │
      │                │                │               │              │
      │  store_content │                │               │              │
      │───────────────────────────────────────────────────────────────▶│
      │                │                │               │              │
      │  add_urls      │                │               │              │
      │───────────────▶│                │               │              │
      │                │                │               │              │
```

---

## 7. URL Frontier Design

### Priority Calculation

```python
def calculate_priority(url: str, metadata: dict) -> int:
    """
    Calculate URL priority (lower = higher priority).

    Factors:
    - Page importance (PageRank-like)
    - Domain authority
    - URL depth
    - Freshness requirements
    - Content type
    """
    score = 0

    # Domain authority (pre-computed)
    domain = extract_domain(url)
    score += domain_authority.get(domain, 50)

    # URL depth (shorter = more important)
    depth = url.count('/') - 2  # Subtract protocol slashes
    score += depth * 10

    # Homepage bonus
    if is_homepage(url):
        score -= 20

    # Freshness (recently updated pages)
    if metadata.get('last_modified'):
        age_days = (now() - metadata['last_modified']).days
        score += min(age_days, 30)

    return max(0, min(100, score))


class PriorityQueue:
    """
    Multi-level priority queue for URLs.
    """

    def __init__(self, num_levels: int = 10):
        self.queues = [deque() for _ in range(num_levels)]
        self.num_levels = num_levels

    def add(self, url: str, priority: int):
        level = min(priority // 10, self.num_levels - 1)
        self.queues[level].append(url)

    def pop(self) -> Optional[str]:
        """Pop from highest priority non-empty queue."""
        for queue in self.queues:
            if queue:
                return queue.popleft()
        return None
```

### URL Seen Detection (Bloom Filter)

```python
class URLSeenFilter:
    """
    Space-efficient duplicate URL detection using Bloom Filter.
    """

    def __init__(self, expected_urls: int = 1_000_000_000, fp_rate: float = 0.01):
        # Calculate optimal size
        self.size = self._optimal_size(expected_urls, fp_rate)
        self.num_hashes = self._optimal_hashes(expected_urls, self.size)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, url: str):
        for seed in range(self.num_hashes):
            index = self._hash(url, seed) % self.size
            self.bit_array[index] = 1

    def might_contain(self, url: str) -> bool:
        for seed in range(self.num_hashes):
            index = self._hash(url, seed) % self.size
            if not self.bit_array[index]:
                return False
        return True

    def _hash(self, url: str, seed: int) -> int:
        return mmh3.hash(url, seed) & 0xFFFFFFFF

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        return int(-n * math.log(p) / (math.log(2) ** 2))

    @staticmethod
    def _optimal_hashes(n: int, m: int) -> int:
        return int((m / n) * math.log(2))
```

### URL Normalization

```python
def normalize_url(url: str) -> str:
    """
    Normalize URL to canonical form for deduplication.

    - Lowercase scheme and host
    - Remove default ports
    - Sort query parameters
    - Remove fragments
    - Remove trailing slashes
    - Handle relative URLs
    """
    parsed = urlparse(url)

    # Lowercase scheme and host
    scheme = parsed.scheme.lower()
    host = parsed.netloc.lower()

    # Remove default ports
    if ':' in host:
        hostname, port = host.rsplit(':', 1)
        if (scheme == 'http' and port == '80') or \
           (scheme == 'https' and port == '443'):
            host = hostname

    # Normalize path
    path = parsed.path or '/'
    path = re.sub(r'/+', '/', path)  # Remove duplicate slashes
    if path != '/' and path.endswith('/'):
        path = path[:-1]  # Remove trailing slash

    # Sort query parameters
    query = parsed.query
    if query:
        params = sorted(parse_qsl(query))
        query = urlencode(params)

    # Remove fragment
    # (fragments are client-side only)

    return f"{scheme}://{host}{path}" + (f"?{query}" if query else "")
```

---

## 8. Politeness and Crawl Rate

### Politeness Policy

```
┌─────────────────────────────────────────────────────────────────────┐
│                      POLITENESS RULES                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Respect robots.txt                                              │
│     - Check before crawling any URL                                 │
│     - Cache for 24 hours                                            │
│                                                                     │
│  2. Crawl delay per domain                                          │
│     - Default: 1 request per second per domain                      │
│     - Respect Crawl-delay directive in robots.txt                   │
│     - Adaptive: slow down if server responds slowly                 │
│                                                                     │
│  3. Concurrent connections                                          │
│     - Max 1 connection per domain                                   │
│     - Max 100 total connections                                     │
│                                                                     │
│  4. Time-of-day awareness                                           │
│     - Reduce crawl rate during peak hours                           │
│     - Configurable per domain                                       │
│                                                                     │
│  5. Back-off on errors                                              │
│     - Exponential backoff on 5xx errors                             │
│     - Stop crawling after repeated failures                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Rate Limiter Implementation

```python
class DomainRateLimiter:
    """
    Token bucket rate limiter per domain.
    """

    def __init__(self, default_rate: float = 1.0):
        self.default_rate = default_rate  # requests per second
        self.domain_buckets = {}
        self.domain_config = {}

    def acquire(self, domain: str) -> bool:
        """Try to acquire a token for the domain."""
        if domain not in self.domain_buckets:
            rate = self.domain_config.get(domain, self.default_rate)
            self.domain_buckets[domain] = TokenBucket(rate)

        return self.domain_buckets[domain].acquire()

    def wait_time(self, domain: str) -> float:
        """Get time to wait before next request."""
        if domain not in self.domain_buckets:
            return 0
        return self.domain_buckets[domain].time_until_available()

    def set_rate(self, domain: str, rate: float):
        """Set custom rate for a domain."""
        self.domain_config[domain] = rate
        if domain in self.domain_buckets:
            self.domain_buckets[domain].set_rate(rate)


class TokenBucket:
    """
    Token bucket algorithm for rate limiting.
    """

    def __init__(self, rate: float, capacity: float = 1.0):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = threading.Lock()

    def acquire(self) -> bool:
        with self.lock:
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def time_until_available(self) -> float:
        with self.lock:
            self._refill()
            if self.tokens >= 1:
                return 0
            return (1 - self.tokens) / self.rate

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
```

### Adaptive Crawl Rate

```python
class AdaptiveRateLimiter:
    """
    Adjust crawl rate based on server response times.
    """

    def __init__(self, domain: str):
        self.domain = domain
        self.response_times = deque(maxlen=100)
        self.error_count = 0
        self.current_rate = 1.0

    def record_response(self, response_time: float, status: int):
        """Record response and adjust rate."""
        self.response_times.append(response_time)

        if status >= 500:
            self.error_count += 1
            self._slow_down()
        elif status == 429:  # Too Many Requests
            self._slow_down(factor=2)
        else:
            self.error_count = 0
            self._adjust_rate()

    def _slow_down(self, factor: float = 1.5):
        self.current_rate = max(0.1, self.current_rate / factor)

    def _adjust_rate(self):
        if len(self.response_times) < 10:
            return

        avg_time = sum(self.response_times) / len(self.response_times)

        if avg_time < 0.5:  # Server is fast
            self.current_rate = min(10.0, self.current_rate * 1.1)
        elif avg_time > 2.0:  # Server is slow
            self.current_rate = max(0.1, self.current_rate * 0.9)
```

---

## 9. Content Processing Pipeline

### HTML Parser and Link Extractor

```python
class ContentProcessor:
    """
    Process downloaded content: parse HTML, extract links, detect duplicates.
    """

    def __init__(self):
        self.duplicate_detector = SimHashDetector()

    def process(self, crawl_result: CrawlResult) -> ProcessedContent:
        if crawl_result.content_type.startswith('text/html'):
            return self._process_html(crawl_result)
        elif crawl_result.content_type == 'application/pdf':
            return self._process_pdf(crawl_result)
        else:
            return self._process_binary(crawl_result)

    def _process_html(self, result: CrawlResult) -> ProcessedContent:
        soup = BeautifulSoup(result.content, 'lxml')

        # Extract text content
        text = self._extract_text(soup)

        # Extract metadata
        metadata = self._extract_metadata(soup)

        # Extract links
        links = self._extract_links(soup, result.url)

        # Check for duplicate content
        content_hash = self.duplicate_detector.compute_hash(text)
        is_duplicate = self.duplicate_detector.is_duplicate(content_hash)

        return ProcessedContent(
            url=result.url,
            text=text,
            metadata=metadata,
            links=links,
            content_hash=content_hash,
            is_duplicate=is_duplicate
        )

    def _extract_links(self, soup, base_url: str) -> List[str]:
        links = []
        for tag in soup.find_all('a', href=True):
            href = tag['href']

            # Convert to absolute URL
            absolute_url = urljoin(base_url, href)

            # Normalize
            normalized = normalize_url(absolute_url)

            # Filter
            if self._should_crawl(normalized):
                links.append(normalized)

        return links

    def _should_crawl(self, url: str) -> bool:
        """Filter out unwanted URLs."""
        parsed = urlparse(url)

        # Only HTTP(S)
        if parsed.scheme not in ('http', 'https'):
            return False

        # Skip common non-content extensions
        skip_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.pdf',
                         '.zip', '.exe', '.css', '.js'}
        path_lower = parsed.path.lower()
        if any(path_lower.endswith(ext) for ext in skip_extensions):
            return False

        # Skip query-heavy URLs (potential spider traps)
        if parsed.query.count('=') > 3:
            return False

        return True

    def _extract_metadata(self, soup) -> dict:
        metadata = {}

        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()

        # Meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', meta.get('property', '')).lower()
            content = meta.get('content', '')

            if name in ('description', 'keywords', 'author'):
                metadata[name] = content
            elif name == 'robots':
                metadata['robots'] = content

        # Canonical URL
        canonical = soup.find('link', rel='canonical')
        if canonical:
            metadata['canonical'] = canonical.get('href')

        return metadata
```

### Duplicate Detection (SimHash)

```python
class SimHashDetector:
    """
    Near-duplicate detection using SimHash algorithm.
    """

    def __init__(self, hash_bits: int = 64, threshold: int = 3):
        self.hash_bits = hash_bits
        self.threshold = threshold  # Max hamming distance for duplicates
        self.seen_hashes = {}  # hash -> url

    def compute_hash(self, text: str) -> int:
        """Compute SimHash of text."""
        # Tokenize
        tokens = self._tokenize(text)

        # Compute weighted hash
        v = [0] * self.hash_bits

        for token in tokens:
            token_hash = self._hash(token)
            weight = tokens.count(token)  # TF weight

            for i in range(self.hash_bits):
                if token_hash & (1 << i):
                    v[i] += weight
                else:
                    v[i] -= weight

        # Convert to binary hash
        simhash = 0
        for i in range(self.hash_bits):
            if v[i] > 0:
                simhash |= (1 << i)

        return simhash

    def is_duplicate(self, hash_value: int) -> bool:
        """Check if content is near-duplicate of seen content."""
        for seen_hash in self.seen_hashes:
            if self._hamming_distance(hash_value, seen_hash) <= self.threshold:
                return True

        self.seen_hashes[hash_value] = True
        return False

    def _hamming_distance(self, h1: int, h2: int) -> int:
        """Count differing bits."""
        return bin(h1 ^ h2).count('1')

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into shingles."""
        words = re.findall(r'\w+', text.lower())
        # Create 3-word shingles
        return [' '.join(words[i:i+3]) for i in range(len(words) - 2)]

    def _hash(self, token: str) -> int:
        return mmh3.hash64(token)[0] & ((1 << self.hash_bits) - 1)
```

---

## 10. Storage Design

### Storage Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      STORAGE ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    URL STORAGE                               │   │
│  │                                                               │   │
│  │  Purpose: Track seen URLs, crawl status, schedule            │   │
│  │  Technology: Redis / RocksDB                                  │   │
│  │  Data: URL hash → (status, last_crawl, next_crawl)           │   │
│  │  Size: ~500 GB for 10B URLs                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   CONTENT STORAGE                            │   │
│  │                                                               │   │
│  │  Purpose: Store raw HTML and processed content               │   │
│  │  Technology: S3 / HDFS / Cassandra                           │   │
│  │  Data: URL → (content, metadata, timestamp)                  │   │
│  │  Size: ~30 TB/month compressed                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   METADATA DATABASE                          │   │
│  │                                                               │   │
│  │  Purpose: Searchable page metadata, link graph               │   │
│  │  Technology: PostgreSQL / Elasticsearch                       │   │
│  │  Data: Page info, links, crawl history                       │   │
│  │  Size: ~5 TB                                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Schema Design

```sql
-- URL Table (for crawl management)
CREATE TABLE urls (
    url_hash        BIGINT PRIMARY KEY,  -- Hash of normalized URL
    url             TEXT NOT NULL,
    domain          VARCHAR(255) NOT NULL,
    status          VARCHAR(20),          -- pending, crawled, failed, blocked
    http_status     SMALLINT,
    content_hash    BIGINT,               -- SimHash for duplicate detection
    first_seen      TIMESTAMP,
    last_crawled    TIMESTAMP,
    next_crawl      TIMESTAMP,
    crawl_count     INTEGER DEFAULT 0,
    priority        SMALLINT DEFAULT 50,

    INDEX idx_domain (domain),
    INDEX idx_next_crawl (next_crawl) WHERE status = 'crawled',
    INDEX idx_status (status)
);

-- Page Content (metadata, stored in DB; content in object storage)
CREATE TABLE pages (
    url_hash        BIGINT PRIMARY KEY REFERENCES urls(url_hash),
    title           TEXT,
    description     TEXT,
    content_type    VARCHAR(100),
    content_length  INTEGER,
    language        VARCHAR(10),
    content_path    VARCHAR(500),         -- S3/HDFS path
    fetched_at      TIMESTAMP,

    INDEX idx_content_type (content_type)
);

-- Link Graph
CREATE TABLE links (
    source_hash     BIGINT REFERENCES urls(url_hash),
    target_hash     BIGINT REFERENCES urls(url_hash),
    anchor_text     TEXT,
    discovered_at   TIMESTAMP,

    PRIMARY KEY (source_hash, target_hash),
    INDEX idx_target (target_hash)
);

-- Crawl History (for debugging and analytics)
CREATE TABLE crawl_history (
    id              BIGSERIAL PRIMARY KEY,
    url_hash        BIGINT REFERENCES urls(url_hash),
    http_status     SMALLINT,
    response_time   INTEGER,              -- milliseconds
    content_size    INTEGER,
    error_message   TEXT,
    crawled_at      TIMESTAMP,
    worker_id       VARCHAR(50),

    INDEX idx_url_time (url_hash, crawled_at DESC)
);
```

### Content Storage Strategy

```python
class ContentStore:
    """
    Store crawled content in object storage with compression.
    """

    def __init__(self, s3_bucket: str):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket

    def store(self, url: str, content: bytes, metadata: dict) -> str:
        """Store content and return storage path."""
        url_hash = hash_url(url)

        # Organize by date and hash prefix for efficient access
        date_prefix = datetime.now().strftime('%Y/%m/%d')
        hash_prefix = f"{url_hash:016x}"[:4]

        path = f"content/{date_prefix}/{hash_prefix}/{url_hash:016x}.gz"

        # Compress content
        compressed = gzip.compress(content)

        # Store with metadata
        self.s3.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=compressed,
            Metadata={
                'url': url,
                'content-type': metadata.get('content_type', ''),
                'crawled-at': datetime.now().isoformat()
            }
        )

        return path

    def retrieve(self, path: str) -> bytes:
        """Retrieve and decompress content."""
        response = self.s3.get_object(Bucket=self.bucket, Key=path)
        compressed = response['Body'].read()
        return gzip.decompress(compressed)
```

---

## 11. Scalability

### Horizontal Scaling Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     DISTRIBUTED ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                      ┌─────────────────┐                           │
│                      │  Coordinator    │                           │
│                      │  (Zookeeper)    │                           │
│                      └────────┬────────┘                           │
│                               │                                     │
│          ┌────────────────────┼────────────────────┐               │
│          │                    │                    │               │
│          ▼                    ▼                    ▼               │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐        │
│  │   Frontier    │   │   Frontier    │   │   Frontier    │        │
│  │   Shard 1     │   │   Shard 2     │   │   Shard N     │        │
│  │ (domains A-H) │   │ (domains I-P) │   │ (domains Q-Z) │        │
│  └───────┬───────┘   └───────┬───────┘   └───────┬───────┘        │
│          │                    │                    │               │
│          ▼                    ▼                    ▼               │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐        │
│  │   Crawler     │   │   Crawler     │   │   Crawler     │        │
│  │   Pool 1      │   │   Pool 2      │   │   Pool N      │        │
│  │ (10 workers)  │   │ (10 workers)  │   │ (10 workers)  │        │
│  └───────────────┘   └───────────────┘   └───────────────┘        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Domain-Based Sharding

```python
class DomainShardRouter:
    """
    Route URLs to appropriate frontier shard based on domain.
    """

    def __init__(self, num_shards: int):
        self.num_shards = num_shards
        self.shard_ring = ConsistentHashRing(num_shards)

    def get_shard(self, url: str) -> int:
        """Determine which shard handles this URL's domain."""
        domain = extract_domain(url)
        return self.shard_ring.get_node(domain)

    def add_shard(self):
        """Add a new shard (with minimal redistribution)."""
        self.num_shards += 1
        self.shard_ring.add_node(self.num_shards - 1)

    def remove_shard(self, shard_id: int):
        """Remove a shard (redistribute its domains)."""
        self.shard_ring.remove_node(shard_id)


class ConsistentHashRing:
    """
    Consistent hashing for minimal redistribution on scaling.
    """

    def __init__(self, num_nodes: int, virtual_nodes: int = 150):
        self.virtual_nodes = virtual_nodes
        self.ring = SortedDict()

        for node in range(num_nodes):
            self.add_node(node)

    def add_node(self, node_id: int):
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node_id}:{i}")
            self.ring[key] = node_id

    def remove_node(self, node_id: int):
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node_id}:{i}")
            del self.ring[key]

    def get_node(self, key: str) -> int:
        if not self.ring:
            return 0

        hash_key = self._hash(key)
        idx = self.ring.bisect_left(hash_key)

        if idx == len(self.ring):
            idx = 0

        return self.ring.peekitem(idx)[1]

    def _hash(self, key: str) -> int:
        return mmh3.hash(key) & 0xFFFFFFFF
```

### Worker Auto-Scaling

```python
class CrawlerAutoScaler:
    """
    Auto-scale crawler workers based on queue depth and throughput.
    """

    def __init__(self, min_workers: int = 10, max_workers: int = 100):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.current_workers = min_workers

    def evaluate(self, metrics: dict) -> int:
        """
        Determine desired worker count based on metrics.

        Metrics:
        - queue_depth: URLs waiting to be crawled
        - throughput: Pages crawled per second
        - avg_latency: Average crawl time
        - error_rate: Percentage of failed crawls
        """
        queue_depth = metrics['queue_depth']
        throughput = metrics['throughput']

        # Target: Process queue within 1 hour
        target_throughput = queue_depth / 3600

        # Current capacity per worker
        throughput_per_worker = throughput / self.current_workers

        # Desired workers
        desired = int(target_throughput / throughput_per_worker)

        # Apply limits
        desired = max(self.min_workers, min(self.max_workers, desired))

        # Gradual scaling (max 20% change)
        max_change = int(self.current_workers * 0.2) + 1
        if desired > self.current_workers:
            desired = min(desired, self.current_workers + max_change)
        else:
            desired = max(desired, self.current_workers - max_change)

        return desired
```

---

## 12. Fault Tolerance

### Failure Scenarios and Handling

```
┌─────────────────────────────────────────────────────────────────────┐
│                     FAULT TOLERANCE MATRIX                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Failure Type          │ Detection        │ Recovery               │
│  ──────────────────────┼──────────────────┼───────────────────────│
│  Worker crash          │ Heartbeat        │ Reschedule URLs        │
│  Network timeout       │ Request timeout  │ Retry with backoff     │
│  DNS failure           │ Resolution error │ Use backup DNS         │
│  Target server down    │ Connection error │ Mark domain, retry     │
│  Storage failure       │ Write error      │ Retry, failover        │
│  Frontier shard down   │ Health check     │ Redistribute domains   │
│  Coordinator down      │ Leader election  │ Standby takeover       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Retry Strategy

```python
class RetryStrategy:
    """
    Exponential backoff retry with jitter.
    """

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    async def execute(self, func, *args, **kwargs):
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except RetryableError as e:
                last_exception = e

                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    await asyncio.sleep(delay)

        raise last_exception

    def _calculate_delay(self, attempt: int) -> float:
        # Exponential backoff: 1, 2, 4, 8, ...
        delay = self.base_delay * (2 ** attempt)

        # Add jitter (±25%)
        jitter = delay * 0.25 * (random.random() * 2 - 1)

        # Cap at 60 seconds
        return min(60, delay + jitter)


class RetryableError(Exception):
    """Errors that should be retried."""
    pass


# Usage
retry = RetryStrategy(max_retries=3)

async def crawl_with_retry(url: str):
    try:
        return await retry.execute(fetch_page, url)
    except RetryableError:
        # Mark URL for later retry
        await frontier.mark_failed(url)
        return None
```

### Checkpointing

```python
class CrawlCheckpoint:
    """
    Checkpoint crawl progress for recovery.
    """

    def __init__(self, checkpoint_dir: str):
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_interval = 300  # 5 minutes

    def save_checkpoint(self, frontier_state: dict, worker_states: List[dict]):
        """Save current crawl state."""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'frontier': frontier_state,
            'workers': worker_states,
            'version': '1.0'
        }

        path = f"{self.checkpoint_dir}/checkpoint_{int(time.time())}.json"

        # Atomic write
        temp_path = f"{path}.tmp"
        with open(temp_path, 'w') as f:
            json.dump(checkpoint, f)
        os.rename(temp_path, path)

        # Clean old checkpoints (keep last 10)
        self._cleanup_old_checkpoints()

    def load_latest_checkpoint(self) -> Optional[dict]:
        """Load most recent checkpoint."""
        checkpoints = sorted(glob(f"{self.checkpoint_dir}/checkpoint_*.json"))

        if not checkpoints:
            return None

        with open(checkpoints[-1]) as f:
            return json.load(f)

    def _cleanup_old_checkpoints(self, keep: int = 10):
        checkpoints = sorted(glob(f"{self.checkpoint_dir}/checkpoint_*.json"))
        for old in checkpoints[:-keep]:
            os.remove(old)
```

---

## 13. Monitoring and Metrics

### Key Metrics Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CRAWLER DASHBOARD                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  THROUGHPUT                          QUEUE STATUS                   │
│  ┌─────────────────────────┐        ┌─────────────────────────┐    │
│  │ Pages/sec: 847          │        │ Pending URLs: 2.3M      │    │
│  │ Avg: 812  Peak: 1,203   │        │ In Progress: 15K        │    │
│  │ ▁▂▃▅▆▇█▇▆▅▄▃▂▁▂▃▄▅     │        │ Completed: 847M         │    │
│  └─────────────────────────┘        └─────────────────────────┘    │
│                                                                     │
│  ERROR RATES                         LATENCY (p50/p95/p99)         │
│  ┌─────────────────────────┐        ┌─────────────────────────┐    │
│  │ HTTP 4xx: 2.3%          │        │ DNS:      12/45/120 ms  │    │
│  │ HTTP 5xx: 0.8%          │        │ Connect:  23/89/340 ms  │    │
│  │ Timeout:  1.2%          │        │ Download: 156/890/2100ms│    │
│  │ DNS Fail: 0.1%          │        │ Total:    245/1.2s/3.1s │    │
│  └─────────────────────────┘        └─────────────────────────┘    │
│                                                                     │
│  TOP DOMAINS                         WORKER STATUS                  │
│  ┌─────────────────────────┐        ┌─────────────────────────┐    │
│  │ 1. wikipedia.org: 12K   │        │ Active: 48/50           │    │
│  │ 2. github.com: 8.5K     │        │ Idle: 2                 │    │
│  │ 3. medium.com: 6.2K     │        │ Error: 0                │    │
│  │ 4. amazon.com: 5.1K     │        │ CPU: 67%  Mem: 45%      │    │
│  └─────────────────────────┘        └─────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Metrics Collection

```python
class CrawlerMetrics:
    """
    Collect and expose crawler metrics.
    """

    def __init__(self):
        # Counters
        self.pages_crawled = Counter('crawler_pages_total',
                                     'Total pages crawled',
                                     ['status'])
        self.bytes_downloaded = Counter('crawler_bytes_total',
                                        'Total bytes downloaded')
        self.errors = Counter('crawler_errors_total',
                             'Total errors',
                             ['type'])

        # Gauges
        self.queue_size = Gauge('crawler_queue_size',
                               'URLs in queue')
        self.active_workers = Gauge('crawler_active_workers',
                                   'Active worker count')

        # Histograms
        self.crawl_duration = Histogram('crawler_duration_seconds',
                                       'Crawl duration',
                                       buckets=[.1, .25, .5, 1, 2.5, 5, 10])
        self.page_size = Histogram('crawler_page_bytes',
                                  'Page size in bytes',
                                  buckets=[1000, 10000, 50000, 100000, 500000])

    def record_crawl(self, result: CrawlResult):
        # Count
        self.pages_crawled.labels(status=result.status).inc()

        if result.content:
            self.bytes_downloaded.inc(len(result.content))
            self.page_size.observe(len(result.content))

        # Timing
        if result.duration:
            self.crawl_duration.observe(result.duration)

        # Errors
        if result.status.startswith('error'):
            self.errors.labels(type=result.status).inc()

    def update_queue_size(self, size: int):
        self.queue_size.set(size)

    def update_active_workers(self, count: int):
        self.active_workers.set(count)
```

### Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: crawler_alerts
    rules:
      - alert: CrawlerThroughputLow
        expr: rate(crawler_pages_total[5m]) < 100
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Crawler throughput is below 100 pages/sec"

      - alert: CrawlerErrorRateHigh
        expr: |
          rate(crawler_errors_total[5m]) / rate(crawler_pages_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Crawler error rate exceeds 5%"

      - alert: CrawlerQueueBacklog
        expr: crawler_queue_size > 10000000
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Crawler queue has more than 10M URLs"

      - alert: CrawlerWorkerDown
        expr: crawler_active_workers < 40
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Less than 40 workers active"
```

---

## 14. Advanced Topics

### 14.1 Spider Traps Detection

```python
class SpiderTrapDetector:
    """
    Detect and avoid spider traps (infinite URL generators).
    """

    def __init__(self):
        self.url_patterns = defaultdict(int)  # pattern -> count
        self.max_depth = 20
        self.max_per_pattern = 1000

    def is_trap(self, url: str) -> bool:
        # Check URL depth
        if url.count('/') > self.max_depth:
            return True

        # Check URL pattern
        pattern = self._extract_pattern(url)
        self.url_patterns[pattern] += 1

        if self.url_patterns[pattern] > self.max_per_pattern:
            return True

        # Check for calendar traps
        if self._is_calendar_trap(url):
            return True

        return False

    def _extract_pattern(self, url: str) -> str:
        """
        Extract URL pattern by replacing variable parts.
        /page/123 → /page/{num}
        /date/2024-01-01 → /date/{date}
        """
        parsed = urlparse(url)
        path = parsed.path

        # Replace numbers
        path = re.sub(r'/\d+', '/{num}', path)

        # Replace dates
        path = re.sub(r'/\d{4}-\d{2}-\d{2}', '/{date}', path)

        # Replace UUIDs
        path = re.sub(r'/[a-f0-9-]{36}', '/{uuid}', path)

        return f"{parsed.netloc}{path}"

    def _is_calendar_trap(self, url: str) -> bool:
        """Detect infinite calendar URLs."""
        # Match patterns like /calendar/2099/12 or /events/2050-01-01
        future_date = re.search(r'20[3-9]\d|2[1-9]\d{2}', url)
        past_date = re.search(r'19[0-8]\d|19[0-4]\d', url)
        return bool(future_date or past_date)
```

### 14.2 JavaScript Rendering

```python
class JavaScriptRenderer:
    """
    Render JavaScript-heavy pages using headless browser.
    """

    def __init__(self, pool_size: int = 10):
        self.browser_pool = BrowserPool(pool_size)

    async def render(self, url: str) -> str:
        """Render page with JavaScript execution."""
        browser = await self.browser_pool.acquire()

        try:
            page = await browser.new_page()

            # Set timeout and wait for network idle
            await page.goto(url, timeout=30000, wait_until='networkidle2')

            # Wait for dynamic content
            await page.wait_for_selector('body', timeout=5000)

            # Get rendered HTML
            content = await page.content()

            return content
        finally:
            await page.close()
            await self.browser_pool.release(browser)


class BrowserPool:
    """
    Pool of headless browser instances.
    """

    def __init__(self, size: int):
        self.size = size
        self.available = asyncio.Queue()
        self.browsers = []

    async def initialize(self):
        from playwright.async_api import async_playwright

        playwright = await async_playwright().start()

        for _ in range(self.size):
            browser = await playwright.chromium.launch(headless=True)
            self.browsers.append(browser)
            await self.available.put(browser)

    async def acquire(self):
        return await self.available.get()

    async def release(self, browser):
        await self.available.put(browser)
```

### 14.3 Recrawl Scheduling

```python
class RecrawlScheduler:
    """
    Schedule page recrawls based on change frequency.
    """

    def __init__(self):
        self.change_history = {}  # url -> [change_timestamps]

    def calculate_next_crawl(self, url: str, content_hash: int) -> datetime:
        """Determine when to recrawl based on change history."""

        if url not in self.change_history:
            self.change_history[url] = []
            return datetime.now() + timedelta(days=7)  # Default: 1 week

        history = self.change_history[url]

        # Check if content changed
        changed = history and history[-1]['hash'] != content_hash

        if changed:
            history.append({
                'hash': content_hash,
                'timestamp': datetime.now()
            })

        # Calculate change frequency
        if len(history) < 2:
            interval = timedelta(days=7)
        else:
            # Average time between changes
            deltas = []
            for i in range(1, len(history)):
                delta = history[i]['timestamp'] - history[i-1]['timestamp']
                deltas.append(delta)

            avg_delta = sum(deltas, timedelta()) / len(deltas)

            # Recrawl at half the average change interval
            interval = avg_delta / 2

            # Clamp between 1 hour and 30 days
            interval = max(timedelta(hours=1), min(timedelta(days=30), interval))

        return datetime.now() + interval
```

### 14.4 Distributed Crawl Coordination

```python
class CrawlCoordinator:
    """
    Coordinate distributed crawlers using Zookeeper.
    """

    def __init__(self, zk_hosts: str):
        self.zk = KazooClient(hosts=zk_hosts)
        self.zk.start()

        self.workers_path = '/crawler/workers'
        self.domains_path = '/crawler/domains'
        self.leader_path = '/crawler/leader'

    def register_worker(self, worker_id: str):
        """Register this worker with the coordinator."""
        path = f"{self.workers_path}/{worker_id}"
        self.zk.create(path, ephemeral=True, makepath=True)

    def claim_domain(self, domain: str, worker_id: str) -> bool:
        """Try to claim exclusive access to a domain."""
        path = f"{self.domains_path}/{domain}"

        try:
            self.zk.create(path, worker_id.encode(), ephemeral=True)
            return True
        except NodeExistsError:
            # Another worker has this domain
            return False

    def release_domain(self, domain: str):
        """Release domain when done crawling."""
        path = f"{self.domains_path}/{domain}"
        try:
            self.zk.delete(path)
        except NoNodeError:
            pass

    def elect_leader(self, worker_id: str, on_leader: Callable):
        """Participate in leader election."""
        election = self.zk.Election(self.leader_path, worker_id)
        election.run(on_leader)
```

---

## 15. Interview Tips

### Key Points to Cover

```
1. START WITH REQUIREMENTS
   - Clarify scale (how many pages?)
   - Clarify scope (entire web vs specific domains?)
   - Clarify freshness requirements

2. HIGH-LEVEL DESIGN FIRST
   - Draw the main components
   - Explain data flow
   - Identify bottlenecks

3. DIVE DEEP ON KEY AREAS
   - URL Frontier (prioritization + politeness)
   - Distributed coordination
   - Duplicate detection
   - Storage strategy

4. DISCUSS TRADE-OFFS
   - BFS vs DFS crawling
   - Freshness vs coverage
   - Speed vs politeness

5. HANDLE EDGE CASES
   - Spider traps
   - Robots.txt
   - Dynamic content
   - Redirects
```

### Common Follow-Up Questions

| Question | Key Points |
|----------|------------|
| How to handle robots.txt? | Cache per domain, respect Crawl-delay |
| How to detect duplicates? | URL normalization + content SimHash |
| How to prioritize URLs? | PageRank-like scoring, domain authority |
| How to handle failures? | Retry with backoff, checkpointing |
| How to scale to billions? | Shard by domain, consistent hashing |
| How to handle JS pages? | Headless browser pool, selective rendering |

### Time Allocation (45 min interview)

```
┌─────────────────────────────────────────────────────────────────────┐
│  0-5 min:   Requirements clarification                              │
│  5-10 min:  Back-of-envelope estimation                            │
│  10-25 min: High-level design + component deep-dive                │
│  25-35 min: Detailed design (URL frontier, storage, scaling)       │
│  35-40 min: Edge cases and fault tolerance                         │
│  40-45 min: Q&A and wrap-up                                        │
└─────────────────────────────────────────────────────────────────────┘
```

### Diagram to Draw

```
Minimal diagram for whiteboard:

    Seeds → [URL Frontier] → [Workers] → [Processor] → [Storage]
                  ↑              │             │
                  └──────────────┴─────────────┘
                      (new URLs discovered)

Expand each box as time permits:
- Frontier: Priority queues + Domain queues
- Workers: DNS cache + Robots cache + HTTP client
- Processor: Parser + Dedup + Link extractor
- Storage: URL store + Content store + Metadata DB
```

---

## Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WEB CRAWLER DESIGN SUMMARY                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CORE COMPONENTS                                                    │
│  • URL Frontier: Prioritization + Politeness                       │
│  • Crawler Workers: Fetch pages with caching                       │
│  • Content Processor: Parse + Extract + Deduplicate                │
│  • Storage: URLs + Content + Metadata                              │
│                                                                     │
│  KEY CHALLENGES                                                     │
│  • Scale: Billions of pages                                        │
│  • Politeness: Don't overload servers                              │
│  • Duplicates: URL normalization + SimHash                         │
│  • Traps: Pattern detection + depth limits                         │
│                                                                     │
│  SCALING STRATEGIES                                                 │
│  • Shard by domain (consistent hashing)                            │
│  • Horizontal worker scaling                                       │
│  • Distributed coordination (Zookeeper)                            │
│                                                                     │
│  IMPORTANT NUMBERS                                                  │
│  • 1000 pages/sec target throughput                                │
│  • 100KB average page size                                         │
│  • 30TB storage per month                                          │
│  • 50-100 crawler machines                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

**Good luck with your system design interviews!**
