---
layout: simple
title: "System Design"
permalink: /system_design
---

# System Design

Comprehensive interview-focused guides for designing scalable, distributed systems. Each guide follows a **discussion-first approach**: explaining trade-offs and design decisions as you would in an actual interview, rather than presenting solutions directly.

---

## How to Use These Guides

These guides are designed to prepare you for system design interviews:

1. **Practice explaining out loud** - Read the "Interview context" callouts and practice articulating the trade-offs
2. **Use the "Interviewer might ask" prompts** - These highlight follow-up questions you should be ready for
3. **Study the "Why not X?" sections** - Understanding rejected alternatives shows depth
4. **Review Interview Tips sections** - Each guide has specific phrases and approaches for that topic

> **Tip**: Don't memorize solutions. Focus on understanding WHY each design decision was made, so you can adapt when requirements change.

---

## Available Guides

### Building Blocks

| Guide | Description | Key Trade-offs |
|-------|-------------|----------------|
| [Consistent Hashing](/cses-analyses/system_design/consistent-hashing) | Why modulo fails, hash ring mechanics, virtual nodes | Distribution vs complexity, memory vs balance |
| [Unique ID Generator](/cses-analyses/system_design/design-unique-id-generator) | UUID vs Snowflake vs ULID decision framework | Sortability vs randomness, coordination vs independence |

### Storage Systems

| Guide | Description | Key Trade-offs |
|-------|-------------|----------------|
| [Key-Value Store](/cses-analyses/system_design/design-key-value-store) | Distributed storage with replication and consistency | CAP trade-offs, consistency vs availability |
| [Google Drive](/cses-analyses/system_design/design-google-drive) | Cloud file storage, sync, sharing, versioning | Durability vs cost, sync latency vs consistency |

### Web-Scale Systems

| Guide | Description | Key Trade-offs |
|-------|-------------|----------------|
| [URL Shortener](/cses-analyses/system_design/design-url-shortener) | Short URL generation strategies and caching | Predictability vs security, SQL vs NoSQL |
| [Web Crawler](/cses-analyses/system_design/design-web-crawler) | URL frontier, politeness, duplicate detection | Breadth vs depth, crawl rate vs politeness |
| [Chat System](/cses-analyses/system_design/design-chat-system) | Real-time messaging with presence and delivery | WebSocket vs polling, push vs pull |
| [News Feed](/cses-analyses/system_design/design-news-feed) | Push vs pull vs hybrid, celebrity problem | Fan-out trade-offs, real-time vs batch |
| [Search Autocomplete](/cses-analyses/system_design/design-search-autocomplete) | Trie with cached top-K, multi-level caching | Freshness vs latency, memory vs CPU |
| [YouTube](/cses-analyses/system_design/design-youtube) | Video upload, transcoding, CDN, streaming | Storage tiering, processing speed vs cost |

### Domain-Specific Systems

| Guide | Description | Key Trade-offs |
|-------|-------------|----------------|
| [Payment System](/cses-analyses/system_design/design-payment-system) | Idempotency, exactly-once semantics, reconciliation | Sync vs async, retry vs reconciliation |
| [Skills GraphRAG](/cses-analyses/system_design/design-skills-graphrag) | Graph traversal with LLM-powered retrieval | Graph vs vector, latency vs accuracy |

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

Pick 2-3 components to **discuss** in detail:
- Database schema and why you chose it
- API design trade-offs
- Scaling strategies and when they apply
- Failure scenarios and how the system recovers

> **Interview tip**: Always explain WHY, not just WHAT. "I'd use Redis here because we need sub-millisecond latency for read-heavy workloads" beats "I'd use Redis for caching."

### Step 5: Wrap Up (5 min)

- Bottlenecks and how to address them
- Trade-offs you made (and alternatives you considered)
- Future improvements if requirements change

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

## Interview Mindset

### Discussion, Not Presentation

In an interview, you're having a conversation with your interviewer. The guides in this collection are structured to help you think like an interviewer expects:

| Instead of... | Do this... |
|---------------|------------|
| "We need a database" | "What kind of access patterns do we have? Read-heavy suggests..." |
| "Use Redis for caching" | "We could use Redis or Memcached. Redis gives us data structures, Memcached is simpler..." |
| "Here's the schema" | "Let me think about the queries we'll need to support..." |
| "Scale horizontally" | "At what point does horizontal scaling help? Let's estimate..." |

### When You Don't Know

It's okay to not know everything. Strong candidates:
- Acknowledge uncertainty: "I'm not sure about the exact number, but let me reason through it..."
- Ask clarifying questions: "Before I dive in, can I clarify the expected read/write ratio?"
- Show reasoning: "I haven't designed this exact system, but the core challenge seems similar to..."

---

## Interview Transition Phrases

Use these phrases to navigate smoothly through your interview.

### Clarifying Requirements

| Phrase | When to use |
|--------|-------------|
| "Before I start designing, let me make sure I understand the requirements..." | Opening |
| "What's the expected scale? Are we talking thousands or millions of users?" | Scoping |
| "Is consistency more important than availability for this use case?" | Trade-off setup |
| "Should I focus on the happy path first, or edge cases?" | Prioritization |
| "Are there any specific constraints I should know about?" | Constraints |

### Proposing Trade-offs

| Phrase | When to use |
|--------|-------------|
| "We have a few options here. Option A gives us X but costs us Y..." | Presenting alternatives |
| "The trade-off here is between latency and consistency..." | Explaining tension |
| "Given the requirements, I'd lean toward X because..." | Making a choice |
| "If the requirements change, we might reconsider this decision..." | Showing flexibility |
| "This is a classic CAP theorem situation..." | Referencing concepts |

### Transitioning Between Topics

| Phrase | When to use |
|--------|-------------|
| "Now that we have the high-level design, let me dive into..." | Moving to details |
| "Before I go deeper, does this approach make sense?" | Checking alignment |
| "Let me step back and think about how this scales..." | Shifting perspective |
| "One thing we haven't discussed yet is..." | Introducing new topic |
| "This connects to what I mentioned earlier about..." | Building connections |

### Handling Unknowns

| Phrase | When to use |
|--------|-------------|
| "I'm not certain about the exact number, but I can estimate..." | Acknowledging uncertainty |
| "I haven't worked with X directly, but my understanding is..." | Admitting gaps |
| "Let me think through this out loud..." | Buying time while reasoning |
| "That's a great question. Let me reason through it..." | Responding to challenges |
| "I'd want to validate this assumption with actual data..." | Being pragmatic |

### Wrapping Up

| Phrase | When to use |
|--------|-------------|
| "To summarize the key decisions..." | Concluding |
| "The main trade-offs we made were..." | Recap |
| "If we had more time, I'd also consider..." | Showing depth |
| "Potential bottlenecks include X, and we could address them by..." | Proactive thinking |
| "Questions for me before I continue?" | Inviting feedback |

---

## Resources

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
