---
layout: simple
title: "Redis Deep Dive — System Design School"
permalink: /system_design/sds/concepts/tech-redis
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

# Redis: The In-Memory Data-Structure Store

mediumRedisIn-memory cacheData structures

Redis is an in-memory data-structure store. Data lives in RAM, so reads and writes complete in well under a millisecond, and it exposes typed structures — strings, hashes, lists, sets, sorted sets — with atomic operations on each. Its value in a design is those structures and the operations on them, not just that it can hold cached bytes.

A live leaderboard shows why that distinction matters. Ranking the top 50 of 10 million players on every refresh, with scores changing constantly, fits a relational ORDER BY score DESC LIMIT 50 poorly: each read re-sorts hot rows and churns the index. Redis keeps the ranking in a sorted set and returns the top 50 directly, because the structure stays ordered as scores update.

For hands-on commands and practice, see the Redis tutorial.

## What Redis is

Redis is an in-memory data-structure store. Data lives in RAM, not on disk, so reads and writes finish in sub-millisecond time under normal operation. But speed is only half of it. The other half is that Redis stores typed data structures, not opaque blobs, and exposes operations that run inside the store.

That distinction matters. A plain cache holds bytes: you fetch a value, change it in your application, and write it back. Redis holds a sorted set, a counter, or a list, and gives you the operation directly. "Add this score and tell me the rank" is one command that runs where the data sits. The leaderboard above becomes a single sorted-set structure that stays ordered as scores change.

In-memory means volatile by default. RAM loses its contents on restart. Redis adds optional persistence (covered below), but treat it as a fast working store, not the permanent home for data you cannot lose.

## The data types and what each unlocks

Redis is best understood through its core types. Each one matches an access pattern, and each pattern maps to a system-design use. Pick the type for how you read and write the data, not for how the data happens to look.

### Strings and counters

A string holds a value up to 512 MB: a cached JSON blob, a rendered fragment, or a number. Numbers are the interesting case. INCR adds one and returns the new total in a single step. That backs rate-limit counters, view counts, and any tally that many clients bump at once.

### Hashes

A hash is a map of field-value pairs under one key, like a small object. You update one field without rewriting the whole value. This fits sessions and user objects: change last_seen without touching the other fields.

### Lists

A list is an ordered sequence you push and pop from either end. Push on the left, pop on the right, and it behaves as a first-in-first-out queue. Lists back simple job queues and work backlogs where one process enqueues and another drains.

### Sets

A set holds unique members with no order. It answers membership fast: is this user in the group, has this ID been seen. Sets handle tags, deduplication, and "unique visitors" style counting.

### Sorted sets

A sorted set gives each member a numeric score and keeps members ordered by that score. This is the type that solves the leaderboard. Adding a score and reading the top 50 are both cheap, because the structure stays sorted as writes arrive. The same shape powers top-K rankings and time-ordered feeds, where the score is a timestamp. The Top-K problem builds on this directly.

### TTL and expiry

Any key can carry a time-to-live (TTL): a countdown after which Redis deletes the key automatically. TTL is what makes Redis a cache rather than a growing pile of data. Set a cached page to expire in 60 seconds and stale entries clean themselves up. One caveat worth remembering: overwriting a key with a plain SET clears its existing TTL unless you set the expiry again.

## Common system-design uses

The types combine into a handful of patterns that recur across interviews. Each is a type plus an access pattern, not a new technology.

- Cache. Store a computed or fetched value with a TTL and an eviction policy for when memory fills. This is the classic read path, worked out in full in the Distributed Cache problem and the caching mental model.

- Rate limiting. An atomic INCR on a per-user key with a short TTL counts requests inside a window. See the Rate Limiter problem for the full design.

- Leaderboards and top-K. A sorted set keyed by score, read with a range query for the top N.

- Distributed lock. A key set only if absent, with a TTL so a crashed holder does not lock forever. It coordinates work across processes.

- Pub/sub. Lightweight message broadcasting: publishers send to a channel, subscribers receive. Useful for fan-out signals, not durable queues.

- Session store. A hash per session with a TTL, shared across stateless application servers.

## Single-threaded commands and atomicity

Redis runs commands on a single thread. One command finishes before the next begins. That sounds like a limit, and for raw CPU it is, but it hands you a strong guarantee for free: every command is atomic. Atomic means the operation completes fully or not at all, with no other command interleaving partway through.

This is why the counter patterns work. Consider two servers rate-limiting the same user. Both read the counter as 9, both add one in their own code, both write 10. One request slipped through, because the read-modify-write raced. INCR closes that gap: it reads, adds, and writes as one indivisible step on the single thread, so two INCR calls yield 10 then 11. No lock needed.

Compound logic that spans several commands needs more care. "Read the count, and if it is under the limit, add one" is three steps, and another client can act between them. Redis solves this with a Lua script: a small program you send to the server, which runs the whole thing atomically as one unit while nothing else interrupts it. The read-decide-write becomes a single atomic operation again.

Keep atomic scripts small. A Lua script blocks the single thread for its whole duration. A slow script stalls every other client. Use scripts for short read-modify-write logic, not heavy computation.

## Persistence at a glance

In-memory does not have to mean data vanishes on restart. Redis offers two persistence modes, and it helps to know the shape of each without the tuning details.

RDB takes point-in-time snapshots: periodically, Redis forks and writes the whole dataset to a file. Recovery is fast, but a crash between snapshots loses the writes since the last one, often minutes of data.

AOF (append-only file) logs every write to disk as it happens. It loses far less on a crash, down to about a second with the default sync policy, but the log grows and replay on startup is slower. The strictest setting syncs every write and sharply cuts throughput.

The takeaway is directional, not exact. Redis is durable-ish: good enough to survive most restarts, not a guarantee that every acknowledged write survives a crash. Treat it as a fast working store backed by a real system of record, not as the system of record itself.

## When not to use Redis

Redis is not the answer to every storage question. Its strengths invert into clear limits.

Data must fit in RAM. Memory is smaller and costlier than disk, so a multi-terabyte dataset does not belong in a single Redis instance. Sharding across a cluster helps but adds its own constraints on multi-key operations.

It is not your primary durable store. Because persistence is best-effort, financial records and other data you cannot lose need a database with stronger durability. Redis sits in front of that database, not in place of it.

It does not do complex queries. There is no rich query planner, no joins, no ad-hoc filtering across fields, and no SQL-style transactional rollback. Access is by key and by the operations each type provides. When you need flexible queries or full-text search, use a database or search engine built for it.

Design checkpoint

You are building a real-time leaderboard: top 50 out of 10M players, updated on every score change. Which Redis type fits best?

A hash keyed by player, one field per scoreA sorted set with the score as the member's scoreA list of players re-sorted on each read

## What a strong answer sounds like

How would you build a live leaderboard for millions of players?

BadSort the database on every read▾

GoodUse a Redis sorted set▾

GreatSorted set plus a durable backing store and refresh discipline▾

## The transferable pattern

Reach for Redis when the answer is fast shared state shaped like one of its types. Ask what access pattern the feature needs: a counter bumped atomically, a set tested for membership, a structure that stays ranked as it changes. Match that to the type, and the operation you want usually exists as one atomic command running inside the store. Keep a durable database behind it for anything you cannot lose, and keep the dataset within memory. Caching, rate limiting, leaderboards, locks, and sessions are all this same move: pick the type for the access pattern, then let the single-threaded command model give you atomicity for free.

Key idea. Redis is a data-structure store, not just a cache. Its value is matching a type to your access pattern and getting atomic, sub-millisecond operations on it.

## Sources and further reading

- Redis data types — Redis docs — the core types (strings, hashes, lists, sets, sorted sets) and their operations.

- Persistence — Redis docs — RDB snapshots vs the AOF log and their durability trade-offs.

- EVAL / Lua scripting — Redis docs — how scripts run atomically on the single thread for read-modify-write logic.

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

What Redis isThe data types and what each unlocksStrings and countersHashesListsSetsSorted setsTTL and expiryCommon system-design usesSingle-threaded commands and atomicityPersistence at a glanceWhen not to use RedisWhat a strong answer sounds likeThe transferable patternSources and further reading

Read0%

Need help?Ask about this section

On this pageWhat Redis is0%

Send feedback
