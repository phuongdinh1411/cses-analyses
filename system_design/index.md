---
layout: simple
title: "System Design"
permalink: /system_design
---

# System Design

Comprehensive guides for designing scalable, distributed systems. Each guide covers requirements, high-level architecture, deep dives, and implementation details.

---

## Available Guides

### Building Blocks

| Guide | Description | Key Concepts |
|-------|-------------|--------------|
| [Consistent Hashing](/cses-analyses/system_design/consistent-hashing) | Distribute data across nodes with minimal reorganization | Hash ring, Virtual nodes, Replication |
| [Unique ID Generator](/cses-analyses/system_design/design-unique-id-generator) | Generate globally unique IDs at scale | UUID, Snowflake, Database sequences |

### Storage Systems

| Guide | Description | Key Concepts |
|-------|-------------|--------------|
| [Key-Value Store](/cses-analyses/system_design/design-key-value-store) | Design a distributed KV store like DynamoDB | Consistent hashing, Replication, CAP theorem |

### Web-Scale Systems

| Guide | Description | Key Concepts |
|-------|-------------|--------------|
| [URL Shortener](/cses-analyses/system_design/design-url-shortener) | Design TinyURL/bit.ly | Base62 encoding, Key generation, Caching |
| [Web Crawler](/cses-analyses/system_design/design-web-crawler) | Design a distributed web crawler | BFS, URL frontier, Politeness |

### Domain-Specific Systems

| Guide | Description | Key Concepts |
|-------|-------------|--------------|
| [Payment System](/cses-analyses/system_design/design-payment-system) | Design a payment processing system | Idempotency, Transactions, Reconciliation |
| [Skills GraphRAG](/cses-analyses/system_design/design-skills-graphrag) | Design a knowledge graph with RAG | Graph DB, Embeddings, LLM integration |

---

## System Design Framework

### Step 1: Requirements (5 min)

**Functional Requirements**
- What are the core features?
- What are the inputs/outputs?

**Non-Functional Requirements**
- Scale: How many users? QPS?
- Latency: What's acceptable response time?
- Availability: What's the SLA?
- Consistency: Strong or eventual?

### Step 2: Back of Envelope (5 min)

Calculate:
- QPS (queries per second)
- Storage requirements
- Bandwidth
- Memory for caching

### Step 3: High-Level Design (10 min)

Draw the main components:
- API Gateway / Load Balancer
- Application Servers
- Database(s)
- Cache
- Message Queue (if async)

### Step 4: Deep Dive (15 min)

Pick 2-3 components to discuss in detail:
- Database schema
- API design
- Scaling strategies
- Failure scenarios

### Step 5: Wrap Up (5 min)

- Bottlenecks and how to address them
- Trade-offs made
- Future improvements

---

## Common Patterns

### Scaling

| Pattern | Use Case |
|---------|----------|
| Horizontal scaling | Add more machines |
| Vertical scaling | Bigger machines |
| Sharding | Split data across DBs |
| Replication | Read replicas |

### Caching

| Pattern | Use Case |
|---------|----------|
| Cache-aside | App manages cache |
| Write-through | Write to cache + DB |
| Write-behind | Write to cache, async to DB |

### Messaging

| Pattern | Use Case |
|---------|----------|
| Pub/Sub | Fan-out to multiple consumers |
| Queue | Work distribution |
| Event sourcing | Audit log, replay |

---

## Quick Reference

### Numbers Everyone Should Know

| Operation | Time |
|-----------|------|
| L1 cache reference | 0.5 ns |
| L2 cache reference | 7 ns |
| Main memory reference | 100 ns |
| SSD random read | 150 us |
| HDD seek | 10 ms |
| Round trip within datacenter | 500 us |
| Round trip CA to Netherlands | 150 ms |

### Capacity Estimation

| Data | Size |
|------|------|
| 1 char | 1 byte (ASCII) / 2-4 bytes (UTF-8) |
| 1 UUID | 36 bytes (string) / 16 bytes (binary) |
| 1 Tweet | ~300 bytes |
| 1 Image | 200 KB - 2 MB |
| 1 Video (1 min, HD) | 50-100 MB |

### Scale Reference

| Scale | Requests | Storage |
|-------|----------|---------|
| Small | 100 QPS | GBs |
| Medium | 10K QPS | TBs |
| Large | 1M QPS | PBs |

---

## Resources

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
