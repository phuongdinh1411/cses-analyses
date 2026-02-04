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

> **Interview context**: After sketching the high-level architecture, dive into each component. Start with the URL Frontier—it's the "brain" of the crawler.

### 5.1 URL Frontier

> **Interviewer might ask**: "How do you decide which URL to crawl next?"

The URL Frontier manages what to crawl next. It has two conflicting goals:

#### The Challenge

You want to crawl important pages first (priority), but you also can't hammer the same domain repeatedly (politeness). How do you balance these?

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

#### Two-Level Queue Design

The solution is a **two-level queue system**:

| Level | Purpose | Selection Strategy |
|-------|---------|-------------------|
| **Front queues** | Prioritization | Higher priority queues polled more frequently |
| **Back queues** | Politeness per domain | One queue per domain, round-robin selection |

**Flow**: URL enters → Assigned to priority queue → Mapped to domain's back queue → Selected only when domain's delay has elapsed

#### Why Not Just One Queue?

- **Single priority queue**: Might crawl same domain too fast, getting blocked
- **Single domain queue**: Ignores importance—low-value pages crawled same as high-value
- **Two-level**: Priority decides WHICH domain queues have URLs; politeness decides WHEN to pick from each

### 5.2 Crawler Worker

> **Interviewer might ask**: "Walk me through what happens when a worker picks up a URL."

#### Worker Responsibilities

| Step | Action | Potential Issues |
|------|--------|-----------------|
| 1 | Check robots.txt | URL might be disallowed |
| 2 | Resolve DNS | Slow or failed resolution |
| 3 | Fetch page | Timeouts, redirects, errors |
| 4 | Process response | Different status codes need different handling |

#### Handling HTTP Responses

| Status | Action |
|--------|--------|
| 200 | Success - process content |
| 301/302 | Follow redirect, add new URL to frontier |
| 404 | Mark as not found, don't retry |
| 429 | Too many requests - back off from domain |
| 5xx | Server error - retry with exponential backoff |

### 5.3 DNS Resolver with Cache

> **Interviewer might ask**: "Why is DNS a bottleneck?"

#### The Challenge

Every URL requires a DNS lookup to get the IP address. At 1000 pages/second, that's 1000 DNS queries/second—this can overwhelm DNS servers and add latency.

#### Solution: Local DNS Cache

| Approach | Benefit | Cache Duration |
|----------|---------|----------------|
| In-memory cache | Fastest lookup | TTL from DNS record (usually 1-24 hours) |
| Local DNS server | Shared across workers | Respects TTL |
| Fallback to public DNS | Reliability | When local fails |

**Key insight**: Most crawled pages share domains. If you crawl 1000 pages from wikipedia.org, you only need ONE DNS lookup.

### 5.4 Robots.txt Handler

> **Interviewer might ask**: "How do you respect robots.txt?"

#### The Protocol

robots.txt is a standard that websites use to tell crawlers what they can and cannot crawl.

```
# Example robots.txt
User-agent: *
Disallow: /private/
Crawl-delay: 2

User-agent: Googlebot
Allow: /private/public-page
```

#### Key Directives

| Directive | Meaning | Our Response |
|-----------|---------|--------------|
| `Disallow: /path` | Don't crawl this path | Skip these URLs |
| `Crawl-delay: N` | Wait N seconds between requests | Enforce minimum delay |
| `Allow: /path` | Exception to disallow | Can crawl this specific path |
| `Sitemap: url` | Location of sitemap | Discover more URLs |

#### Why Not Ignore robots.txt?

- **Legal**: Some jurisdictions treat ignoring robots.txt as trespass
- **Practical**: You'll get IP-banned quickly
- **Ethical**: It's the web's social contract

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

> **Interview context**: The URL Frontier is often the most discussed component. Be ready to explain prioritization and duplicate detection in detail.

### Priority Calculation

> **Interviewer might ask**: "How do you decide which URLs are more important?"

#### Factors for URL Priority

| Factor | Weight | Reasoning |
|--------|--------|-----------|
| **Domain authority** | High | Well-known sites more likely to have quality content |
| **URL depth** | Medium | Shallower pages (e.g., `/about`) typically more important than deep pages |
| **Page type** | Medium | Homepages, category pages > individual items |
| **Freshness** | Low-Medium | Recently modified pages may have new content |
| **Backlinks** | High | Pages linked by many others are likely important |

#### Priority Score Formula

```
priority = base_domain_score
         + depth_penalty × url_depth
         - homepage_bonus (if homepage)
         + age_penalty (days since last crawl)
```

**Key insight**: You don't need complex ML initially. A simple heuristic-based score works well and is explainable in interviews.

### URL Seen Detection (Bloom Filter)

> **Interviewer might ask**: "How do you avoid crawling the same URL twice?"

#### The Challenge

With 10 billion URLs, storing them all in a hash set would require ~1TB of memory. How do you efficiently check "have I seen this URL?"

#### Why Bloom Filter?

| Approach | Memory for 10B URLs | False Positives | False Negatives |
|----------|---------------------|-----------------|-----------------|
| Hash Set | ~1 TB | None | None |
| Bloom Filter | ~10 GB | 1% (configurable) | None |

A Bloom Filter trades a small false positive rate for massive memory savings. **False positives are acceptable**—we might skip a few URLs we haven't seen. **False negatives would be bad**—we'd crawl duplicates.

#### How Bloom Filter Works

1. Hash the URL with K different hash functions
2. Set K bits in a bit array
3. To check: if ALL K bits are set, "probably seen"
4. If ANY bit is 0, "definitely not seen"

#### Why Not Just Hash the URL?

A simple hash (MD5, SHA) per URL would still require 16+ bytes per URL = 160GB for 10B URLs. Bloom filter gets to ~10GB with 1% false positive rate.

### URL Normalization

> **Interviewer might ask**: "How do you handle different URLs that point to the same page?"

#### The Problem

These URLs all point to the same content:
- `http://Example.com/page`
- `https://example.com/page/`
- `https://example.com/PAGE`
- `https://example.com:443/page?a=1&b=2`
- `https://example.com/page?b=2&a=1`

Without normalization, we'd crawl the same page 5 times.

#### Normalization Rules

| Rule | Example |
|------|---------|
| Lowercase scheme and host | `HTTP://EXAMPLE.COM` → `http://example.com` |
| Remove default ports | `:443` for HTTPS, `:80` for HTTP |
| Remove trailing slash | `/page/` → `/page` |
| Sort query parameters | `?b=2&a=1` → `?a=1&b=2` |
| Remove fragments | `/page#section` → `/page` |
| Remove duplicate slashes | `/a//b` → `/a/b` |

**Important**: Normalization should be **consistent** and **deterministic**. The same URL should always normalize to the same canonical form.

---

## 8. Politeness and Crawl Rate

> **Interview context**: Politeness is a critical topic. Interviewers want to see that you understand the ethical and practical aspects of crawling.

### The Challenge

You want to crawl fast (1000 pages/second), but:
- Hammering a single domain will get you blocked
- Overwhelming small servers is unethical
- Some sites specify explicit crawl delays

How do you maximize throughput while being a good citizen?

### Politeness Rules

| Rule | Implementation | Why |
|------|---------------|-----|
| Respect robots.txt | Check before crawling, cache 24h | Legal and ethical requirement |
| Crawl delay per domain | Default 1 req/sec, respect Crawl-delay | Avoid overwhelming servers |
| Max 1 connection per domain | Domain queue enforces this | Browsers do the same |
| Back-off on errors | Exponential backoff on 5xx/429 | Server is struggling |
| Time-of-day awareness | Reduce during peak hours | Be extra polite to small sites |

### Rate Limiting: Token Bucket

> **Interviewer might ask**: "How do you implement per-domain rate limiting?"

#### Why Token Bucket?

| Algorithm | Pros | Cons |
|-----------|------|------|
| Fixed window | Simple | Burst at window edges |
| Sliding window | Smooth | More memory |
| **Token bucket** | Smooth, allows bursts, memory-efficient | Slightly complex |

#### How Token Bucket Works

```
Bucket starts with N tokens (capacity)
Tokens refill at rate R per second
Each request consumes 1 token
If no tokens available, wait

Example: rate=1/sec, capacity=1
- Request at t=0: ✓ (1 token used)
- Request at t=0.5: ✗ (no tokens, wait 0.5s)
- Request at t=1.0: ✓ (token refilled)
```

### Adaptive Crawl Rate

> **Interviewer might ask**: "What if a server is slow but not returning errors?"

#### The Problem

Some servers don't return 429 (Too Many Requests) or 5xx errors—they just get slower. How do you detect this?

#### Solution: Response Time Monitoring

| Server Response Time | Action |
|---------------------|--------|
| < 500ms (fast) | Gradually increase rate (up to 10x default) |
| 500ms - 2s (normal) | Maintain current rate |
| > 2s (slow) | Gradually decrease rate |
| 5xx error | Immediately halve rate |
| 429 error | Immediately quarter rate |

**Key insight**: This is similar to TCP congestion control—probe for capacity, back off when you see congestion signals.

---

## 9. Content Processing Pipeline

> **Interview context**: After fetching pages, you need to process them. This involves parsing, extracting links, detecting duplicates, and deciding what to store.

### Processing Steps

```
Raw HTML → Parse → Extract Metadata → Extract Links → Detect Duplicates → Store
```

### HTML Parsing and Link Extraction

> **Interviewer might ask**: "How do you extract links from a page?"

#### Link Extraction Rules

| Source | Example | Action |
|--------|---------|--------|
| `<a href="...">` | `<a href="/page">` | Primary link source |
| Relative URLs | `/page`, `../page` | Convert to absolute using base URL |
| Fragments | `/page#section` | Strip fragment (client-side only) |
| Non-HTTP | `mailto:`, `javascript:` | Skip |
| Binary files | `.jpg`, `.pdf`, `.exe` | Skip (or queue separately) |

#### URL Filtering

Not all discovered URLs should be crawled:

| Filter | Why |
|--------|-----|
| HTTP/HTTPS only | Other protocols not relevant |
| Skip images/CSS/JS | Unless specifically crawling media |
| Limit query parameters | URLs with >3 params often dynamic/traps |
| Domain scope | Stay within allowed domains |

### Duplicate Detection (SimHash)

> **Interviewer might ask**: "How do you detect near-duplicate content?"

#### The Problem

The web has massive duplication:
- Same article on multiple sites
- Pagination with similar content
- Mirror sites
- Slightly different versions of same content

Exact matching (MD5) misses near-duplicates. We need **fuzzy matching**.

#### Why SimHash?

| Approach | Pros | Cons |
|----------|------|------|
| MD5/SHA | Exact match, fast | Misses near-duplicates |
| MinHash | Good for Jaccard similarity | More complex |
| **SimHash** | Near-duplicate detection, compact (64 bits) | Threshold tuning |

#### How SimHash Works

1. **Tokenize**: Split text into shingles (n-grams of words)
2. **Hash each shingle**: Get 64-bit hash per shingle
3. **Weighted voting**: For each bit position, sum +weight if bit=1, -weight if bit=0
4. **Final hash**: Each bit = 1 if sum positive, else 0

**Key insight**: Similar documents have similar SimHash values. If Hamming distance (differing bits) ≤ 3, documents are likely near-duplicates.

#### Duplicate Detection Threshold

| Hamming Distance | Interpretation |
|-----------------|----------------|
| 0 | Exact duplicate |
| 1-3 | Near-duplicate (minor edits) |
| 4-10 | Related content |
| >10 | Different content |

### Metadata Extraction

| Metadata | Source | Use |
|----------|--------|-----|
| Title | `<title>` tag | Display in search results |
| Description | `<meta name="description">` | Snippet generation |
| Canonical URL | `<link rel="canonical">` | Deduplication hint |
| Robots directives | `<meta name="robots">` | noindex, nofollow |
| Language | `<html lang="">` | Language detection |

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

> **Interviewer might ask**: "How do you organize stored content?"

#### Storage Path Design

```
s3://crawler-bucket/content/2024/01/15/a3f2/a3f2b7c4d5e6f789.gz
                            └─date─┘ └hash prefix─┘ └─full hash─┘
```

| Component | Purpose |
|-----------|---------|
| Date prefix | Time-based organization, easy lifecycle policies |
| Hash prefix (4 chars) | Even distribution across S3 partitions |
| Full hash | Unique identifier for URL |
| .gz extension | Content is gzip compressed |

#### Compression

| Compression | Ratio | Speed | Use |
|-------------|-------|-------|-----|
| gzip | 5:1 | Medium | Good default |
| zstd | 6:1 | Fast | Better for large volumes |
| None | 1:1 | Fastest | When CPU-bound |

**Key insight**: HTML compresses very well (often 10:1). This turns 100TB of raw storage into ~10TB compressed.

---

## 11. Scalability

> **Interview context**: Scaling a web crawler involves distributing both the URL frontier and the crawling workers. The key insight is to shard by domain.

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

> **Interviewer might ask**: "How do you distribute work across crawler nodes?"

#### Why Shard by Domain?

| Sharding Strategy | Pros | Cons |
|-------------------|------|------|
| Random URL | Even distribution | Different nodes crawl same domain = politeness violation |
| **By domain** | Politeness automatic, single node owns domain | Some domains much larger |
| By URL hash | Even distribution | Same issue as random |

**Key insight**: Sharding by domain means each domain is owned by exactly one node. This automatically enforces politeness—no coordination needed.

#### Consistent Hashing for Domain Assignment

When scaling from 10 to 11 nodes:
- **Simple modulo**: ~90% of domains remapped (hash % N changes)
- **Consistent hashing**: ~10% of domains remapped (only 1/N moves)

This is critical for maintaining crawl state during scaling.

### Worker Auto-Scaling

> **Interviewer might ask**: "How do you know when to add more workers?"

#### Scaling Signals

| Signal | Scale Up When | Scale Down When |
|--------|---------------|-----------------|
| Queue depth | Growing > 1M URLs | Shrinking < 100K |
| Throughput | Below target | Exceeds need |
| CPU usage | Sustained > 80% | Below 30% |
| Memory | Queue doesn't fit | Over-provisioned |

#### Scaling Strategy

```
Target: Process queue within 1 hour
Current queue: 3.6M URLs
Required throughput: 3.6M / 3600 = 1000 URLs/sec
Current throughput per worker: 20 URLs/sec
Required workers: 1000 / 20 = 50 workers
```

**Gradual scaling**: Change by max 20% at a time to avoid oscillation.

---

## 12. Fault Tolerance

> **Interview context**: A production crawler will face many failure modes. Discuss how you handle each type.

### Failure Scenarios and Handling

| Failure Type | Detection | Recovery |
|--------------|-----------|----------|
| Worker crash | Heartbeat timeout | Reschedule in-progress URLs |
| Network timeout | Request timeout | Retry with backoff |
| DNS failure | Resolution error | Use backup DNS, retry later |
| Target server down | Connection error | Mark domain unavailable, retry later |
| Storage failure | Write error | Retry, failover to backup |
| Frontier shard down | Health check | Redistribute domains to other shards |
| Coordinator down | Leader election | Standby takes over |

### Retry Strategy

> **Interviewer might ask**: "How do you handle transient failures?"

#### Exponential Backoff with Jitter

```
Attempt 1: Wait 1 second (± 0.25s jitter)
Attempt 2: Wait 2 seconds (± 0.5s jitter)
Attempt 3: Wait 4 seconds (± 1s jitter)
Attempt 4: Give up, mark for later retry
```

#### Why Jitter?

Without jitter, if 1000 requests fail simultaneously, they all retry at exactly the same times, creating "thundering herd" that fails again. Jitter spreads retries over time.

#### What's Retryable?

| Error Type | Retry? | Reason |
|------------|--------|--------|
| Timeout | Yes | Transient network issue |
| 5xx errors | Yes | Server temporarily overloaded |
| 429 Too Many Requests | Yes (with longer delay) | Rate limited |
| DNS failure | Yes | DNS server might be temporarily down |
| 4xx errors | No | Client error, won't change on retry |
| Parse error | No | Content issue, not transient |

### Checkpointing

> **Interviewer might ask**: "What happens if the crawler crashes mid-crawl?"

#### The Problem

If a crawler crashes with 1M URLs in its queue, you don't want to lose that state and have to rediscover all those URLs.

#### Solution: Periodic Checkpoints

| Component | Checkpoint Data |
|-----------|-----------------|
| URL Frontier | Pending URLs, priority scores, domain states |
| Workers | In-progress URLs (to re-queue on crash) |
| Seen URLs | Bloom filter state (or URL hashes) |

**Checkpoint frequency**: Every 5 minutes is typical. Trade-off between recovery granularity and checkpoint overhead.

#### Atomic Checkpointing

Write to temp file, then atomic rename. This ensures you never have a partial checkpoint:

```
1. Write to checkpoint_1234.json.tmp
2. Rename to checkpoint_1234.json (atomic)
3. Delete old checkpoints (keep last 10)
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

### Metrics to Track

> **Interviewer might ask**: "How do you know if the crawler is healthy?"

#### Key Metrics

| Metric Type | Examples | Purpose |
|-------------|----------|---------|
| **Counters** | Pages crawled, bytes downloaded, errors | Throughput tracking |
| **Gauges** | Queue size, active workers | Current state |
| **Histograms** | Crawl duration, page size | Latency distribution |

#### Essential Metrics

| Metric | Alert Threshold | Meaning |
|--------|-----------------|---------|
| Pages/second | < 100 for 10min | Crawler slowing down |
| Error rate | > 5% | Something wrong with targets or crawler |
| Queue size | > 10M for 30min | Falling behind |
| Active workers | < 80% of expected | Workers dying |
| p99 latency | > 10 seconds | Network or server issues |

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

> **Interview context**: These are often follow-up questions after you've covered the basics. Be ready to discuss at least one in depth.

### 14.1 Spider Traps Detection

> **Interviewer might ask**: "How do you avoid getting stuck in infinite loops?"

#### What Are Spider Traps?

Websites (intentionally or not) can generate infinite URLs:
- Calendar pages: `/calendar/2024/01`, `/calendar/2024/02`, ... `/calendar/2099/12`
- Session IDs: `/page?sid=abc123`, `/page?sid=def456`, ...
- Pagination: `/items?page=1`, `/items?page=2`, ... `/items?page=999999`

#### Detection Strategies

| Strategy | How It Works | Trade-off |
|----------|--------------|-----------|
| **URL depth limit** | Stop at depth > 20 | May miss deep valid content |
| **Pattern counting** | Track `/path/{num}` patterns, limit per pattern | Blocks legitimate paginated content |
| **Calendar detection** | Reject dates far in future/past | Simple but specific |
| **Content similarity** | SimHash across pages from same pattern | Catches content-level duplicates |

#### Pattern Normalization

```
/product/12345    → /product/{num}
/date/2024-01-15  → /date/{date}
/user/a3f2-b4c5-d6e7-f8a9 → /user/{uuid}
```

If we see >1000 URLs matching the same pattern, likely a trap.

### 14.2 JavaScript Rendering

> **Interviewer might ask**: "How do you handle Single Page Applications (SPAs)?"

#### The Problem

Modern web pages often require JavaScript execution to see content. Simple HTTP fetch returns an empty shell.

#### Options

| Approach | Pros | Cons |
|----------|------|------|
| **Skip JS pages** | Simple, fast | Miss lots of content |
| **Headless browser** | Full rendering | 10-100x slower, resource intensive |
| **Selective rendering** | Balance | Need to detect which pages need JS |

#### Headless Browser Pool

Maintain a pool of browser instances (Puppeteer, Playwright):
- Pool size: 10-50 browsers
- Each render: ~5-30 seconds
- Reserved for high-value pages that need JS

**Key insight**: Most pages DON'T need JS rendering. Only use headless browser when initial crawl detects minimal content.

### 14.3 Recrawl Scheduling

> **Interviewer might ask**: "How do you keep content fresh?"

#### The Challenge

Some pages change hourly (news), some yearly (documentation). How do you decide when to recrawl?

#### Adaptive Scheduling

| Change Frequency | Recrawl Interval |
|------------------|------------------|
| Changed every crawl | Crawl every 1 hour |
| Changed sometimes | Half of average change interval |
| Never changed | Crawl every 30 days |
| New page | Default 7 days, then adapt |

**Formula**: `next_crawl = average_change_interval / 2`

This ensures you catch most changes while not wasting resources on static pages.

### 14.4 Distributed Crawl Coordination

> **Interviewer might ask**: "How do multiple crawler nodes coordinate?"

#### Coordination Needs

| Need | Solution |
|------|----------|
| Domain ownership | Ephemeral Zookeeper nodes |
| Leader election | Zookeeper election |
| Worker registry | Ephemeral nodes with heartbeat |
| Config distribution | Zookeeper watches |

#### Domain Claiming

When a worker wants to crawl a domain:
1. Try to create `/domains/example.com` ephemeral node
2. If success: worker owns domain
3. If fails: another worker owns it, get URLs from that shard
4. When worker dies: ephemeral node deleted, domain up for grabs

**Key insight**: Ephemeral nodes + automatic cleanup = no orphaned locks.

---

## 15. Interview Tips

### How to Approach (45 minutes)

```
0-5 min:   CLARIFY REQUIREMENTS
           "What's the scale? Entire web or specific domains?
            What's the freshness requirement?"

5-10 min:  BACK-OF-ENVELOPE
           1B pages/month → 400 pages/sec → need ~50 machines

10-25 min: HIGH-LEVEL DESIGN
           Draw: Seeds → Frontier → Workers → Processor → Storage
           Explain the feedback loop (new URLs)

25-35 min: DEEP DIVE (pick 2-3)
           - URL Frontier (priority + politeness)
           - Duplicate detection (Bloom filter + SimHash)
           - Distributed coordination
           - Storage strategy

35-40 min: EDGE CASES
           - Spider traps, robots.txt, JS rendering

40-45 min: Q&A AND WRAP-UP
```

### Key Phrases That Show Depth

| Instead of... | Say... |
|---------------|--------|
| "We check for duplicates" | "We use a Bloom filter for URL deduplication—it's probabilistic but uses 10GB instead of 1TB for 10B URLs. For content deduplication, we use SimHash to detect near-duplicates with Hamming distance ≤ 3." |
| "We limit crawl rate" | "We use a token bucket rate limiter per domain. Default is 1 request/sec, but we respect robots.txt Crawl-delay and adaptively slow down if response times increase." |
| "We shard the work" | "We shard by domain using consistent hashing. This automatically enforces politeness—one node owns each domain—and minimizes rebalancing when scaling." |
| "We handle failures" | "Transient errors get exponential backoff with jitter to avoid thundering herd. We checkpoint every 5 minutes so crash recovery loses at most 5 minutes of progress." |

### Common Follow-Up Questions

| Question | Key Points |
|----------|------------|
| "How to handle robots.txt?" | Fetch once per domain, cache 24h, respect Crawl-delay directive, check before every URL |
| "How to detect duplicates?" | Two levels: URL normalization (same page, different URL) + SimHash (same content, different URL) |
| "How to prioritize URLs?" | Domain authority + URL depth + recency. PageRank-like if you have link graph. |
| "How to handle failures?" | Exponential backoff with jitter. Checkpoint frontier state. Re-queue in-progress URLs on crash. |
| "How to scale to billions?" | Shard frontier by domain (consistent hashing). Add workers horizontally. |
| "How to handle JS pages?" | Headless browser pool for pages that need rendering. Detect by checking if initial content is empty. |

### Trade-offs to Discuss

| Decision | Option A | Option B |
|----------|----------|----------|
| Crawl order | BFS (breadth-first from seeds) | Priority-based (important pages first) |
| Freshness vs coverage | Recrawl frequently, crawl fewer pages | Crawl more, recrawl less |
| Speed vs politeness | Aggressive (fast but may get blocked) | Conservative (slow but sustainable) |
| Duplicate detection | Exact (MD5, miss near-dupes) | Fuzzy (SimHash, some false positives) |
| URL storage | Bloom filter (space efficient, false positives) | Full URL store (accurate, more space) |

### Diagram to Draw

```
Minimal diagram for whiteboard:

    Seeds → [URL Frontier] → [Workers] → [Processor] → [Storage]
                  ↑              │             │
                  └──────────────┴─────────────┘
                      (new URLs discovered)

Expand each box as time permits:
- Frontier: Priority queues + Domain queues (two-level)
- Workers: DNS cache + Robots cache + HTTP client
- Processor: Parser + Dedup (SimHash) + Link extractor
- Storage: URL store (Bloom) + Content store (S3) + Metadata (Postgres)
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
