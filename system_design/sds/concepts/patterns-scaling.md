---
layout: simple
title: "Scaling Reads & Writes — System Design School"
permalink: /system_design/sds/concepts/patterns-scaling
---

System Design School

- Learn

- Practice

- Primer

- Roadmap

- Pricing

Ask AI TutorStart learning

System Design Primer12

★The TemplateIntroductionWhat Is System Design?What Are System Design Interviews?Level Expectations

Show all 12 →

Design Solutions35

LeetCode (Online Judge)Typeahead / AutocompleteDistributed Rate LimiterTicketmasterNews Feed

Show all 35 →

AI System Design6

RAG SystemChatGPTImage Generation ServiceCoding Agent CLI (Claude Code)

Show all 6 →

Patterns5

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time TransportHandling Large Files

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix Search

Show all 5 →

# Scaling Reads and Writes: Copy, Split, or Defer

mediumScalabilityRead replicasSharding

Reads and writes reach their scaling limits for opposite reasons, and the fix for one rarely helps the other. A read-heavy service strains because the same data is fetched over and over. A write-heavy service strains because every write must be accepted and made durable. Copying data relieves the first and does nothing for the second.

The asymmetry is concrete. A popular product page might take 50,000 reads a minute against data that changes weekly, while an event-tracking endpoint takes 20,000 writes a second and almost no reads. Both saturate a single database, but the levers that save them point in different directions.

## Reads and writes are not symmetric

A read just needs an answer. Any copy of the data that is current enough will do. Nothing changes, so you can serve the same value from ten places at once. A write changes the truth. It must land in an agreed order, survive a crash, and eventually reach every copy. You cannot casually run the same write in ten places and hope they agree.

That asymmetry sets the whole strategy. Reads scale by copying. Writes scale by splitting or deferring. Copying is safe for reads because copies never disagree about a value nobody is changing. Copying is dangerous for writes because two copies taking writes at once diverge. So writes take a different route: cut the data into independent pieces, or accept the write now and do the slow part later.

## Start with the ratio

Before choosing any technique, estimate the ratio of reads to writes. The ratio tells you which side to spend effort on, and spending it on the wrong side wastes work.

A social feed or a product catalog is read-heavy, often on the order of 100 reads per write. There, the write path can stay a plain insert; the reads are where the machine burns. A metrics pipeline or a location tracker is write-heavy: a flood of writes, almost no reads. There, replicas and caches solve a problem you do not have.

Say the ratio out loud when you design. "This is roughly 100:1 read-heavy, so I optimize the read path first" is a decision an interviewer can follow. It also guards against a common error: sharding a read-heavy system for write throughput it never needed, or piling on read replicas for a write-heavy ingest that has nothing to read.

Read:write ratio. Reads divided by writes over the same window. A comment feed might read a post 1,000 times per write (1000:1). An IoT sensor might write every second and read once a day (~1:86,000). The ratio, not raw volume, points to the bottleneck.

## Scaling reads: copy

Every read technique is a form of copying: put a current-enough copy of the data closer to the reader, or in a faster store, so most reads never touch the source. The cheapest read is the one that never reaches the database. Each copy adds one shared cost — the copy can lag the source — and the techniques differ mainly in where the copy lives and how stale it gets.

### In-memory cache

Keep hot data in an in-memory store in front of the database. Repeat reads hit RAM and skip the disk query entirely. A 90% hit rate means the database sees one read in ten. For our product page, caching the rendered item turns 50,000 queries a minute into a few hundred, since the value barely changes. The tradeoff is invalidation: when the source changes, stale cache entries must be evicted or expired, and getting that wrong serves old data. See the caching mental model for the patterns.

### Read replicas

Run copies of the database that take reads only. The primary handles writes and streams its changes to each replica; application reads fan out across the replicas. This multiplies read capacity without touching the write path, which is exactly what a read-heavy system wants. The cost is replica lag: a replica applies changes a moment after the primary, so a read right after a write may miss it. Route reads that must see their own write back to the primary. This split of read and write traffic is covered in read-write separation.

### CDN edge caching

For content that is the same for everyone — images, video, static pages, public API responses — cache it at CDN edge locations near users. The read never reaches your origin at all; it is served from a nearby edge. This is the widest copy of all, spread across the globe. It fits only non-personalized, cacheable content, and it carries the same freshness question: an edge holds a copy until its time-to-live expires or you purge it.

### Precomputed read models

Instead of assembling the answer on every read, assemble it once at write time and store it ready to serve. A user's home feed, computed by merging many sources, is expensive to build per request. Precompute it: when a source changes, update the stored feed, so the read is a single lookup. This moves cost from read time to write time — a good trade when reads vastly outnumber writes. The News Feed design builds exactly such a materialized timeline, worked out in full in News Feed. The cost is freshness: the precomputed copy must be rebuilt when its inputs change.

Design checkpoint

Your system is 100:1 read-heavy and reads are saturating one database. A teammate says: 'Writes are getting slow too under the load — let's just add more replicas to fix both.' What is wrong with that?

Nothing, replicas add general capacityReplicas only serve reads; every write still lands on the single primary, so they add zero write throughputReplicas are slower than the primary

## Scaling writes: split or defer

Writes cannot be scaled by copying, because copies taking writes independently diverge. Two moves remain. Split the data so each write lands on a different machine, or accept the write fast and defer the expensive part. Both raise write throughput; both trade away some simplicity or immediacy.

### Sharding by key

Split the data across machines by a partition key, so each machine owns one slice and its writes. Shard user data by user ID: writes for different users land on different shards, and total write capacity grows with the shard count. This is the primary way to scale writes past one box. Two costs follow. A hot key — one viral item whose shard takes a disproportionate share of writes — overloads a single shard while others idle. And a query spanning shards must gather from several machines and merge. Picking a key that spreads load evenly is the core problem; database partitioning covers how.

### Async writes through a queue

Accept the write onto a durable queue and return immediately; workers apply it to the database later. The write path now absorbs bursts: a spike of 20,000 writes a second lands on the queue at its own pace, and workers drain it steadily behind the scenes. The event-tracking service from the opening fits this exactly. The cost is eventual consistency — the write is durably accepted but not yet visible, so a read moments later may not see it. The queue also buffers, so a slow database no longer drops writes; it just clears the backlog more slowly.

### Batching small writes

Coalesce many small writes into one larger operation. A thousand individual inserts a second become ten batches of a hundred, cutting per-write overhead — one round trip, one index update, one commit instead of a hundred. This suits high-volume, low-value writes like metrics or logs. The tradeoff is latency and partial failure: a write waits for its batch to fill, and one bad record can fail the whole batch, so the handling must isolate or retry the offenders.

### CQRS: separate the paths

When the shape that is cheap to write differs from the shape that is cheap to read, split them. Command Query Responsibility Segregation keeps a write-optimized model for changes and a separate read-optimized model derived from it, updated as writes flow in. The write side stays a simple append; the read side is precomputed for fast queries. This is the async and precomputed ideas combined into an architecture. The cost is running two models and keeping the read side synchronized behind the write side. See CQRS for the full pattern.

## What a strong answer sounds like

How do you scale this system?

BadAdd a bigger server▾

GoodName one technique that fits▾

GreatRatio first, then copy for reads and split-or-defer for writes▾

## The transferable pattern

Any scaling question reduces to the same first move: separate reads from writes, because they scale in opposite directions. Reads scale by copying — a cache, a replica, a CDN edge, a precomputed model — and every copy trades freshness for capacity. Writes scale by splitting or deferring — a shard, a queue, a batch, a CQRS split — and every split trades away a hot-key or consistency guarantee. Neither lever is free, and the ratio tells you which one to reach for first.

Hold the one line and the rest follows: reads → copy; writes → split or defer. Feeds, catalogs, metrics pipelines, and event logs all fall out of this once you know their ratio.

Key idea. Reads and writes scale in opposite ways. Start from the read:write ratio, copy for reads and split or defer for writes, and name the tradeoff each copy or split introduces.

## Sources and further reading

- Amazon RDS read replicas — AWS docs — how replicas offload read traffic from a primary and the lag that follows.

- Designing Data-Intensive Applications, Ch. 5–6 — Martin Kleppmann — replication and partitioning: the tradeoffs behind copying reads and splitting writes.

- CQRS — Martin Fowler — separating the read and write models, and when the added complexity is worth it.

Explain

Add to Chat

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

Was this lesson clear?

👍👎

### How to Solve Any System Design Interview

#### Comments

Join the Discussion

The System Design Courses

Go beyond memorizing solutions to specific problems. Learn the core concepts, patterns and templates to solve any problem.

Start Learning

On this page

Reads and writes are not symmetricStart with the ratioScaling reads: copyIn-memory cacheRead replicasCDN edge cachingPrecomputed read modelsScaling writes: split or deferSharding by keyAsync writes through a queueBatching small writesCQRS: separate the pathsWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageReads and writes are not symmetric0%

Send feedback
