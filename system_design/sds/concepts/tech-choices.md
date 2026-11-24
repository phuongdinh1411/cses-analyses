---
layout: simple
title: "Technology Choices — System Design School"
permalink: /system_design/sds/concepts/tech-choices
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

The 10 PatternsScaling Reads & WritesAsynchronous JobsReal-Time Transport

Show all 5 →

Key Technologies5

Networking EssentialsTechnology ChoicesRedisTries & Prefix SearchFail-Open vs Fail-Closed

# Technology Choices: Naming the Right Tool in an Interview

mediumTechnology selectionDatabasesInterview strategy

An interviewer asks how you would store user sessions. One candidate says "I'll use Redis." Another says "I need low-latency reads on hot keys, so an in-memory cache like Redis, because it serves lookups in well under a millisecond and keeps that load off the primary database." Both named the same product. Only the second showed why it fits.

Naming a tool by itself is not an answer. It sounds like pattern-matching from a blog post, and it invites the follow-up you cannot answer: "Why that one?" The technology is the last word in a sentence, not the whole sentence.

Most of this course names technologies generically on purpose: object storage, not S3; message queue, not Kafka. That keeps designs portable and forces reasoning about the requirement instead of the brand. This article is the deliberate exception. Interviews reward candidates who can attach a concrete, named tool to a pattern, so here we name real products. The rule that makes it safe: name the technology only after you have named the pattern and the reason.

## State the pattern, then the technology, then the reason

A good technology answer has three parts, in order. First the pattern: the shape of the problem, in words that hold for any vendor ("I need a durable, replayable log of events that many consumers read independently"). Then the technology: one concrete product that implements that pattern ("something like Kafka"). Then the reason: the property that makes it fit here ("because it retains messages after they are read, so a slow or crashed consumer can replay from its last offset").

The order matters because it shows the interviewer your reasoning, not just your vocabulary. Anyone can memorize "Kafka for streaming." Stating the pattern first proves you understand what class of tool you need, so if the interviewer bans your first pick, you can name another tool in the same class and keep the design intact.

Naming rule. Pattern → technology → reason. Say what the problem needs, name one tool that fills it, then give the property that makes it fit. Example: "I need atomic increments on a shared counter (pattern), so an in-memory store like Redis (technology), because it runs increment-and-read as one atomic operation, so concurrent updates do not lose writes (reason)." Never lead with the product name alone.

## Choosing the class of store first

Before any brand, decide which class of store the data belongs in. The class follows from the access pattern: how the data is written, how it is queried, and how large each item is. The diagram below routes a data need to a store class. Pick the class, then pick a named tool inside it.

The default is a relational database. Reach for another class only when a specific requirement pushes you off it: item size, query type, write volume, or latency. That framing keeps you honest, and it gives every answer a reason.

## The technology reference table

Each row names a need, the pattern behind it, one or more concrete tools, and the property you would cite. Read it as a set of ready sentences, not a menu to name-drop from. In the interview you say the pattern and the reason out loud; the product is the short middle word.

Need / PatternTechnologyWhy you'd name it

Structured data with transactions and joins; the default storePostgreSQL, MySQLACID transactions and rich queries with joins keep related data consistent (start here unless a requirement forces otherwise; see SQL vs NoSQL)

Very high write volume, simple key-based access, no single-writer bottleneckCassandra, DynamoDBLeaderless or partitioned writes scale horizontally with tunable consistency; DynamoDB is the managed option with predictable latency

Low-latency reads on hot keys; counters; rate-limit stateRedisIn-memory reads return in well under a millisecond and support atomic operations like increment (see caching)

Large files: images, video, backups, uploadsS3-style object storageCheap, durable storage for big blobs; keep only a pointer in the database (see object storage)

Decouple producers from consumers; absorb bursts; async workKafka, RabbitMQ, SQSA queue buffers work so a spike does not overwhelm downstream services and retries are safe (see message queue)

Durable, replayable event stream read by many consumersKafkaAn append-only log retains messages after reading, so consumers replay from their own offset after a crash

Real-time aggregation over a stream: windowed counts, joinsFlink, Spark StreamingWindowed computation over events as they arrive, not a batch job after the fact

Full-text search, relevance ranking, faceted filteringElasticsearchAn inverted index answers text and fuzzy queries that relational LIKE scans handle poorly

Serve static assets and media close to users worldwideCDNEdge caches deliver bytes from a nearby location, cutting latency and origin load

Leader election, distributed locks, service coordinationZooKeeper, etcdConsensus-backed coordination you get off the shelf instead of building it yourself

Metrics and monitoring: append-heavy, time-ordered dataTime-series DB (Prometheus, InfluxDB)Storage tuned for time-ordered appends and fast range and rollup queries

Similarity search over embeddings: recommendations, semantic searchVector DB (pgvector, Pinecone)Nearest-neighbor lookup over high-dimensional vectors at scale

Analytical queries: aggregates over billions of rows (OLAP)Column store (ClickHouse, BigQuery, Redshift)Columnar layout scans only the needed columns, so large aggregations stay fast, unlike a row-oriented OLTP database

Two rows deserve a note. The last one is the OLAP-versus-OLTP split: a transactional (OLTP) database like PostgreSQL is tuned for many small reads and writes of whole rows, while an analytical (OLAP) column store is tuned for scanning a few columns across huge tables. Naming the wrong one for the workload is a common miss. And several rows overlap: Kafka appears as both a queue and an event log, because the same tool serves a plain work queue and a replayable stream. Say which role you mean.

Design checkpoint

You need to store 10 million product photos, each a few megabytes, and show them fast worldwide. Which technology, and why?

Store the image bytes as BLOB columns in PostgreSQLObject storage for the files plus a CDN in front, with the database holding only the URLA large Redis cluster holding every image in memory

## What a strong answer sounds like

What database would you use to store chat messages?

BadNames a tool with no reason▾

GoodNames a fitting tool with one reason▾

GreatPattern, technology, reason, and the requirement behind the brand▾

## The transferable pattern

Every technology choice in an interview is the same three-step move. Name the pattern in vendor-neutral words, so the interviewer sees you understand the class of problem. Attach one concrete tool that implements the pattern. Then give the single property that makes it fit this requirement, ideally noting an alternative you rejected and why. The product is the least important word in that sentence; the reasoning around it is what gets scored.

This is why the rest of the course names tools generically and this page does not contradict it. The generic requirement — durable replayable log, low-latency key lookup, columnar scan — is the durable part of your answer. The brand is a convenience that lets the interviewer picture it. When you can restate any row of the table above as "pattern, because reason," and swap the brand without breaking the design, you have understood the choice rather than memorized it.

Key idea. Name the pattern first and the reason last; the technology is the short word in between. A tool named without a pattern and a reason is a guess, not a design decision.

## Sources and further reading

- Which database should you use? — AWS — a purpose-built breakdown of relational, key-value, in-memory, document, and other store classes by workload.

- Designing Data-Intensive Applications — Martin Kleppmann — the reference on how storage engines, replication, and stream processing differ, and why the access pattern picks the store.

- When to use Amazon S3 vs. a database — the blob-in-object-storage, pointer-in-database pattern in the object store's own docs.

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

State the pattern, then the technology, then the reasonChoosing the class of store firstThe technology reference tableWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageState the pattern, then the technology, then the reason0%

Send feedback
