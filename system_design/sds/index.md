---
layout: simple
title: "System Design School — Problem Solutions & Primer"
permalink: /system_design/sds/
---

# System Design School — Full Coverage

> Source: [systemdesignschool.io](https://systemdesignschool.io)  
> Crawled: 2024-11-24 · 41 problems + 20 concept pages

---

## Primer & Concepts

| Topic | Category |
|-------|----------|
| [System Design Primer](concepts/primer.md) | Overview |
| [The System Design Template](concepts/template.md) | Framework |
| [The 10 Patterns](concepts/patterns-overview.md) | Patterns |
| [Scaling Reads & Writes](concepts/patterns-scaling.md) | Patterns |
| [Asynchronous Jobs](concepts/patterns-async-jobs.md) | Patterns |
| [Real-Time Transport](concepts/patterns-realtime.md) | Patterns |
| [Handling Large Files](concepts/patterns-large-files.md) | Patterns |
| [Networking Essentials](concepts/tech-networking.md) | Technology |
| [Technology Choices](concepts/tech-choices.md) | Technology |
| [Redis Deep Dive](concepts/tech-redis.md) | Technology |
| [Tries & Prefix Search](concepts/tech-tries.md) | Technology |
| [Fail-Open vs Fail-Closed](concepts/tech-fail-open.md) | Technology |
| [Database Transactions](concepts/domain-transactions.md) | Domain |
| [Distributed Systems Theory](concepts/domain-distributed-systems.md) | Domain |
| [Geospatial Search](concepts/domain-geospatial.md) | Domain |
| [Search Engines & Inverted Index](concepts/domain-search.md) | Domain |
| [Media Systems (Video Transcoding)](concepts/domain-media.md) | Domain |
| [Probabilistic Data Structures](concepts/domain-probabilistic.md) | Domain |
| [Consistency Models](concepts/domain-consistency.md) | Domain |
| [CAP & PACELC Theorems](concepts/domain-cap.md) | Domain |

---

## Design Solutions (41 Problems)

### Classic Systems

| Problem | Key Patterns |
|---------|-------------|
| [URL Shortener](url-shortener.md) | Hashing, Caching |
| [Pastebin](pastebin.md) | Blob storage, CDN |
| [Twitter](twitter.md) | Fan-out, Celebrity problem |
| [News Feed](news-feed.md) | Fan-out, Push vs Pull |
| [Instagram](instagram.md) | Media storage, Feed |
| [YouTube](youtube.md) | Video transcoding, CDN |
| [Netflix](netflix.md) | Adaptive streaming, CDN |
| [Dropbox](dropbox.md) | Chunked upload, Sync |
| [Uber / Nearby Drivers](uber.md) | Geospatial, Real-time |
| [Yelp](yelp.md) | Geospatial, Search |
| [Tinder](tinder.md) | Geospatial, Matching |
| [Typeahead / Autocomplete](typeahead.md) | Tries, Prefix search |
| [Web Crawler](web-crawler.md) | BFS, Deduplication |
| [Chat App (WhatsApp)](chatapp.md) | WebSocket, Fan-out |
| [Live Comments](live-comments.md) | Real-time fan-out |
| [Google Docs](google-docs.md) | OT, WebSocket |
| [Google Calendar](google-calendar.md) | Scheduling, Conflicts |
| [Google Maps](google-map.md) | Graph, Geospatial |
| [Ticketmaster](ticketmaster.md) | Concurrency, Reservations |

### Infrastructure & Platform

| Problem | Key Patterns |
|---------|-------------|
| [Distributed Rate Limiter](rate-limiter.md) | Token bucket, Sliding window |
| [Distributed Cache](distributed-cache.md) | LRU, Consistent hashing |
| [Distributed Key-Value Store](distributed-kv-store.md) | Replication, Partitioning |
| [Pub-Sub / Message Queue](message-queue.md) | Kafka internals |
| [Distributed Job Scheduler](job-scheduler.md) | At-least-once, Polling |
| [Metrics Monitoring](metrics-monitoring.md) | Time-series, Alerting |
| [Payment System](payment-system.md) | Idempotency, Saga |
| [Webhook](webhook.md) | Retry, Fan-out |
| [Online Auction](online-auction.md) | Consistency, Real-time |
| [Post Search (Full-Text)](post-search.md) | Inverted index, Elasticsearch |
| [Top K (Trending)](topk.md) | Count-min sketch, Heap |
| [Ad Click Aggregator](ad-click-aggregator.md) | Stream processing |
| [News Aggregator](news-aggregator.md) | Crawling, Feed |
| [LeetCode (Online Judge)](leetcode.md) | Sandboxing, Queue |
| [Local Delivery (GoPuff)](local-delivery.md) | Geospatial, ETA |
| [Robinhood (Stock Trading)](robinhood.md) | Real-time prices |

### AI System Design

| Problem | Key Patterns |
|---------|-------------|
| [RAG System](rag.md) | Vector DB, Retrieval |
| [ChatGPT](chatgpt.md) | GPU scheduling, Streaming |
| [Image Generation Service](image-generation.md) | GPU queue, Async |
| [Coding Agent CLI (Claude Code)](claude-code-cli.md) | LLM orchestration |
| [Deep Research Agent](deep-research.md) | Multi-step LLM, Web search |
| [Effort Levels in System Design](effort-levels.md) | Interview strategy |
