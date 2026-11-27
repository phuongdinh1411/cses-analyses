---
layout: simple
title: "Design Pastebin — System Design School"
permalink: /system_design/sds/pastebin
---

# Design Pastebin

**Difficulty:** Easy  
**Topics:** Object storage · CDN · Caching · Sharding

## Summary

- **Key challenge:** Mint unique, non-enumerable 7-char keys without DB probes, under a 100:1 read skew (~116 writes/s vs ~11,600 reads/s).
- **Core design:** App servers pop pre-generated keys from a KGS batch, write the body to object storage, then insert a ~100-byte row into a hash-sharded DB; reads go CDN → cache → DB → object storage.
- **Techniques:** KGS pool claimed via `SKIP LOCKED` for collision-free keys; metadata/blob split for small rows; CDN `max-age` since pastes are immutable; request coalescing for viral pastes; per-shard Bloom filter against random-key probes; lazy expiry + capped max-age + sweeper.

## Problem statement

Design a service where a user submits a block of plain text — an error log, a configuration file, or a code snippet — and receives a short link (pb.example/a7x3kLm) that anyone can open to read that text later, optionally with an expiration time. Users can also propose a custom alias for their link if it is not already taken, and owners or moderators can delete a paste early.

In scope: creating a paste with an optional time-to-live (TTL) and optional custom alias, minting a short unique key, storing and serving the text body at high read volume, and expiring and reclaiming past-due pastes. Out of scope: user accounts and authentication, editing or versioning an existing paste, client-side syntax highlighting, and full-text search across pastes.

## Clarifying questions

Each question below fixes an assumption the rest of the design leans on.

- Immutable or editable? Each paste is immutable once created: written once and read many times. Supporting edits turns the problem into versioned document storage (covered in Google Docs), which is deferred.

- Who can read a paste? Unlisted-by-link by default: anyone holding the short key can read the paste, and the key itself acts as the lookup capability. Authenticated access control lists for private pastes are treated as a variant.

- Do pastes expire? Yes, optionally. Creators can set a TTL such as one hour, one day, thirty days, or never, making expiration enforcement and storage reclamation core requirements.

- How large is a paste? Plain text ranges from a single line up to a few megabytes, capped at 1 MB to 10 MB per paste. That payload is too large to sit inline inside a database index, while remaining small enough to upload in a single HTTP request without multi-part chunking.

- Accounts, syntax highlighting, and full-text search? Deferred. Accounts are a standard authentication layer, syntax highlighting runs in the browser, and full-text search requires an inverted index (covered in Inverted Index Fundamentals).

- What sizes the system? The read path and the key space size the system rather than write throughput. Pastes are written once and read heavily, and no two pastes may ever receive the same key.

## What makes this problem distinctive

At first glance, a pastebin looks like a single database table supporting create, read, and delete. That single-table model fails under two pressures: minting a short, collision-free, non-enumerable key on every write, and serving a heavily read-skewed, immutable, expiring text blob without hitting the database on every read.

If the system assigns auto-incrementing integer keys (1, 2, 3) in the URL, anyone can walk the entire corpus by counting up. That single sequence generator also becomes a coordination bottleneck. Conversely, if the system generates a random short string and queries the database on every write to check whether that string is already taken, every write pays an extra database read. Meanwhile, storing multi-megabyte text bodies inside the same row as the key bloats database pages, evicts hot index entries from memory, and forces every read of a viral paste to pull large byte payloads through the database engine.

Short key versus paste body. The short key is a compact seven-character base-62 identifier such as a7x3kLm that appears in the shareable URL. The paste body is the raw text payload, which can reach several megabytes. Separating the tiny, frequently queried key metadata from the large, immutable byte payload is the structural split the rest of the design builds on.

Every write needs a guaranteed-unique, hard-to-guess short key without probing the database, while reads outnumber writes by two orders of magnitude over large text bodies that can expire. The diagram below summarizes those two opposing pressures.

Key idea. Pastebin pairs a collision-free short-key generator on the write path with a cached, immutable, expiring blob store on the read path.

## Key concepts

This section covers the two prerequisite primitives needed before the design walkthrough.

### Base-62 encoding and the short key space

Base-62 encoding represents a non-negative integer using 62 alphanumeric characters: 0–9 (10 digits), a–z (26 lowercase letters), and A–Z (26 uppercase letters). Converting an integer into base-62 divides the number repeatedly by 62 and maps each remainder (0 through 61) to its character in the alphabet. For example, encoding 125,000 divides by 62² (3,844) to get quotient 32 (w) and remainder 1,992. Dividing 1,992 by 62 gives quotient 32 (w) and remainder 8 (8), producing "ww8" (or "0000ww8" when padded to seven characters).

Seven base-62 characters yield 62⁷ = 3,521,614,606,208 (roughly 3.52 trillion) distinct combinations. Because each added character multiplies the address space by 62, seven characters address tens of billions of pastes over a decade while consuming roughly one percent of the total key space.

What separates answers — short key encoding

BadBase-16 hex encoding with low information density▾

GoodBase-64 encoding with URL escaping or punctuation friction▾

GreatBase-62 pure alphanumeric with high density and zero escaping▾

### HTTP Cache-Control: max-age on immutable content

Because a paste cannot be edited after creation, its payload is immutable: once written under a key, the bytes for that key never change before the paste expires. Immutability eliminates cache invalidation on updates. When the origin server returns a paste, it attaches an HTTP Cache-Control: public, max-age=<seconds> header specifying how many seconds the response remains fresh. Browser caches and content delivery network (CDN) edge nodes store the response keyed by the URL path (/{key}) and serve subsequent reads directly from edge memory until max-age elapses.

Key idea. Base-62 encoding packs 3.52 trillion URL-safe identifiers into seven characters, and content immutability lets HTTP caches serve repeat reads by key with Cache-Control: max-age and zero update-invalidation traffic.

## 1. Requirements

Before reading on. Name the core functional and non-functional requirements, then identify the one correctness property that must not fail on the write path and the load pattern that drives the read path.

### 1.1 Functional requirements

- Create a paste: Submit a text body along with an optional TTL and an optional custom_alias, and receive a short unique key and its shareable URL.

- Read a paste by key: Given a key, return the paste body with low latency, or return 404 Not Found if the key does not exist or has passed its expiration time.

- Expire a paste: Once a paste's TTL elapses, stop serving it to readers and reclaim its metadata row and blob storage.

- Claim a custom alias: Allow a creator to specify an 8-to-32-character custom key on creation, rejecting the request with 409 Conflict if that key is already in use.

User accounts and authentication, paste editing and versioning, syntax highlighting (handled client-side), full-text search, and detailed analytics beyond basic view counting are out of scope.

### 1.2 Non-functional requirements

- Key uniqueness: No two live pastes may share the same key. A key collision would overwrite or expose another user's paste.

- Low read latency and high availability: Reads dominate traffic and should return in the low tens of milliseconds. Cached pastes should continue serving from the CDN and in-memory cache even during a brief database outage.

- Durability of live pastes: Once a create call returns 201 Created, the paste's text body must not be lost before its expiration time.

- High cache offload on reads: The read path must serve repeat reads from CDN edges and memory caches so origin database and blob-store load stays small.

- Non-enumerable keys: Keys must not be sequential, preventing a scraper from walking all stored pastes by incrementing an integer.

### 1.3 The binding constraint versus the non-negotiable property

The non-negotiable correctness property and the scaling constraint that drives the architecture are distinct:

- Key uniqueness is non-negotiable: Handing the same key to two pastes corrupts data or leaks content between users, so the key generator must guarantee uniqueness by construction.

- The read/write asymmetry is the binding constraint: Pastes are written once and read roughly a hundred times more often, so every storage and caching layer is organized to keep reads off the origin database.

What separates answers — requirements and sizing

BadAuto-increment key in a single table with inline body, read straight from DB▾

GoodShort non-sequential key, body separated from metadata, cached reads with TTL▾

GreatPairs key uniqueness with read/write asymmetry, sizes reads and key space, enforces lazy expiry▾

Key idea. Key uniqueness is the correctness invariant that cannot bend; the 100:1 read/write asymmetry over immutable blobs is the load constraint that drives every storage and caching layer.

## 2. Back-of-the-envelope estimation

Capacity estimation here verifies three facts: write throughput is modest, read throughput dominates by two orders of magnitude, and a seven-character base-62 key space dwarfs multi-year paste volume. The numbers below follow from four baseline assumptions:

- ~10 million new pastes created per day (illustrative).

- ~100:1 read-to-write ratio (~1 billion paste reads per day, illustrative).

- ~10 KB average paste body size (with individual pastes up to a few megabytes).

- 7-character base-62 key (a–z, A–Z, 0–9).

Press 6-char key (62⁶) or drag Base-62 key length from 7 chars down to 6 chars to see 10-year key-space usage jump from 1.04% to 64.26%, then click 10× scale (100M/day) to watch read QPS scale while write QPS stays near 1,157/s.

Baseline (10M/day, 7-char)6-char key (62⁶)10× scale (100M/day)

New pastes / day10M / day

Read-to-write ratio100 : 1

Average paste size10 KB

Base-62 key length7 chars

Write QPS (average)

116/s

10M ÷ 86,400s — direct DB writes

Read QPS (average)

11,600/s

116/s × 100 — served by CDN + cache

Raw blob ingress

100 GB / day

36.5 TB / year (10 KB avg)

62^7 key space (3.52T)

1.04% in 10 yrs

36.5B pastes over 10 years

writes = 10M ÷ 86,400 ≈ 116/s · reads = 116 × 100 = 11,600/s · storage = 100 GB/day (36.5 TB/yr) · 10-yr keys = 36.5B / 3.52T

Writes average 116/s (no write queue needed), while reads reach 11,600/s and raw blobs grow at 100 GB/day (36.5 TB/year). A 7-character base-62 key uses 1.04% of the 3.52T space over 10 years — leaving wide headroom across a decade of writes.

### 2.1 Writes are modest; reads dominate

One day has 24 × 3,600 = 86,400 seconds. Dividing 10 million daily writes across 86,400 seconds gives the average write rate:

10,000,000 ÷ 86,400 ≈ 116 writes/s

Even with peak traffic several times the daily average (a few hundred writes per second), write volume sits well within the capacity of standard storage engines without write-buffering message queues.

At a 100:1 read-to-write ratio, 10 million daily writes produce 1 billion daily reads:

116 × 100 = 11,600 reads/s

Read throughput is the primary number to design around. Because pastes are immutable once created, a CDN and an in-memory cache absorb almost all of those 11,600 reads per second without touching the origin database.

### 2.2 Storage is bounded by expiry

Multiplying 10 million daily pastes by an average body size of 10 KB gives the daily raw blob ingress:

10,000,000 × 10 KB = 100 GB/day

Over 365 days, cumulative raw ingress is 100 GB/day × 365 = 36.5 TB/year. Because most pastes carry a finite TTL and are reclaimed after expiration, the active live dataset stays well below the cumulative total. Object storage handles tens of terabytes without custom partitioning.

### 2.3 The key space dwarfs demand

Seven base-62 characters provide 62⁷ ≈ 3.52 trillion unique keys. At 10 million new pastes per day, one year consumes 10,000,000 × 365 = 3.65 billion keys, and ten years consume 36.5 billion keys — 1.04% of the seven-character space. Key-space exhaustion is not the bottleneck; minting keys without collisions or sequential leaks is.

Key idea. At ~116 writes/s versus ~11,600 reads/s, the read path dominates by two orders of magnitude, and immutability makes that read load cacheable at the edge.

## 3. API design

Design checkpoint

Writes and reads have a 1:100 volume asymmetry, and a paste never changes after creation. How should that change the read API compared to the create API?

Both endpoints should go through application servers that query the database on every callPOST /v1/pastes handles key minting and storage, while GET /{key} returns an immutable response with a Cache-Control max-age header so CDN edges serve repeat reads directly

The API surface follows the read/write asymmetry: one write endpoint that mints the key and persists the paste, two read endpoints (structured metadata-plus-body and raw text body) that are cacheable by key, and a privileged delete endpoint.

### 3.1 Create a paste

POST /v1/pastes accepts the text body, an optional TTL in seconds, and an optional user-chosen custom_alias (restricted to 8 to 32 characters so it never overlaps the 7-character system key space). The server claims a 7-character key (or attempts to insert custom_alias and returns 409 Conflict if already taken), stores the body and metadata, and returns the short key, shareable URL, and expiration timestamp. The API gateway enforces a maximum payload size (1 MB to 10 MB) to reject oversized uploads early with 413 Payload Too Large.

POST/v1/pastes

Request & response

### 3.2 Read a paste record

GET /v1/pastes/{key} returns the structured paste representation (key, body, created_at, and expires_at) for API clients and web UI views, or 404 Not Found if the key does not exist or has passed expires_at.

GET/v1/pastes/{key}

Request & response

### 3.3 Read the raw paste body

GET /{key} (or GET /raw/{key}) returns the raw text/plain body directly. Because an unlisted paste is readable by link and immutable, the response carries Cache-Control: public, max-age=<remaining_ttl_seconds> (or 31,536,000 seconds for non-expiring pastes). The paste key in the URL path serves as the cache key, so CDN edges serve repeat reads without a redirect round-trip.

GET/{key}

Request & response

### 3.4 Delete a paste

Most pastes disappear through TTL expiration rather than manual deletion. When an owner (authenticated via a delete token returned on creation) or a moderator deletes a paste early, DELETE /v1/pastes/{key} removes the metadata row and blob object and issues a CDN cache purge for /{key}.

DELETE/v1/pastes/{key}

Request & response

Key idea. Everything stateful on write hides behind POST /v1/pastes; GET /{key} is a plain, cacheable fetch of an immutable resource keyed by the short code in the path.

## 4. Data model

Start with the single obvious entity and let what cannot fit inside it force the split.

### 4.1 First cut: a single paste record

Each paste has a short key, its text body, a creation timestamp (created_at), and an expiration timestamp (expires_at). Putting all four fields on one database row gives:

```
paste: key, body, created_at, expires_at

```

Database indexes operate by packing many small rows into fixed-size memory pages (typically 8 KB or 16 KB) inside the database buffer pool. The metadata lookup (key, expires_at) is ~100 bytes and runs on every cache fill, whereas body can be several megabytes. Storing 500 KB or 5 MB bodies inline inside the table row fills buffer-pool memory with cold text bytes and evicts hot index pages to disk.

### 4.2 Splitting the paste record from the body

Moving the raw text bytes into object storage (a blob store built for immutable byte payloads, the same split used in Dropbox) leaves a ~100-byte Paste metadata row holding a pointer (body_ref) to an immutable PasteBody object:

The Paste row is ~100 bytes, indexed by key with a secondary index on expires_at for background expiry sweeps. The PasteBody is an immutable byte blob stored under body_ref in object storage.

### 4.3 Custom aliases need no new entity

Supporting a user-chosen custom_alias requires no separate alias table. Whether a key was minted by the system (7 characters) or proposed by the user (8 to 32 characters), key is the unique primary key of Paste. Claiming a custom_alias executes an INSERT with key = custom_alias; the primary-key uniqueness constraint on key accepts the write if the alias is unused or rejects it if taken.

### 4.4 Where each entity lives

- Paste metadata record: Lives in a key-value store or relational database sharded by hash(key), with a unique constraint on key. Because each row is ~100 bytes, millions of active records fit in an in-memory cache.

- PasteBody object: Lives in object storage as an immutable blob behind the CDN.

- Key generation state: Minting collision-free keys without querying the Paste table on every write is handled by the key-generation service (introduced in section 5.2 and detailed in section 6.1).

Key idea. Large immutable bodies are separated from the 100-byte lookup row so metadata stays cache-friendly, and the unique constraint already on key handles custom aliases without an extra table.

## 5. High-level design

Before reading on. Starting from one application server and one database, identify the four bottlenecks that appear under real traffic and predict which component resolves each one.

Reading the diagrams. Each step marks the newly added components with a dashed outline so the diff from the previous step is clear at a glance.

### 5.1 One server and one database

Start with the minimal baseline: one application server and one database table holding (key, body, created_at, expires_at). On write, the server picks a random key and inserts the row; on read, it queries the row by key and returns body.

Four bottlenecks appear as traffic scales:

- Per-write database probes or collision risk: Generating a random key without checking the database risks overwriting an existing paste, while querying the database first adds a synchronous read probe to every write.

- Database bloat from large bodies: Storing megabyte text bodies inline inside database rows bloats B-tree pages and evicts hot index entries from memory.

- Read overload (100:1 read/write ratio): At ~11,600 reads/s, hitting the database on every read wastes capacity and bottlenecks on viral pastes.

- Unreclaimed expired pastes: Nothing enforces expires_at or deletes past-due rows, so expired pastes remain readable and storage grows without bound.

### 5.2 Fix 1: a key-generation service with a pre-filled pool

To remove both collision risk and per-write database probes from the hot path, introduce a key-generation service (KGS). The KGS pre-computes unique 7-character base-62 keys offline into a pool of unused keys and hands them to application servers in batches (detailed in deep dive 6.1).

Writes now obtain a guaranteed-unique key in memory without probing Pastes DB. Multi-megabyte bodies still sit inside database rows, which Fix 2 addresses next.

### 5.3 Fix 2: move paste bodies to object storage

Move the raw text payload into object storage as an immutable blob, and keep only key -> body_ref, size_bytes, created_at, and expires_at in the database row.

Database rows are now ~100 bytes each. Every read (~11,600/s) still traverses the origin database and object storage until a caching layer is added.

### 5.4 Fix 3: serve reads through a CDN and an in-memory cache

Because pastes are immutable, place a CDN at the edge to cache and serve paste bodies directly by key, and place an in-memory cache-aside metadata cache next to the application tier to hold hot key -> body_ref mappings. Only an edge miss reaches the origin, and only a metadata cache miss queries Pastes DB.

Reads are now absorbed by edge nodes and memory. The remaining gap is enforcing paste expiration and freeing disk space for expired pastes.

### 5.5 Fix 4: lazy expiry on read and a background sweeper

Enforce expiration in two places: on any origin read, check expires_at <= now and cap the CDN Cache-Control: max-age header at expires_at - now when serving a paste, so an expired paste stops being readable the instant its TTL lapses. Then add a background expiry sweeper that periodically scans for rows with expires_at < now and deletes expired metadata rows and blobs in batches.

### 5.6 The composed design

Combining all four fixes produces the complete architecture:

The write sequence writes the blob to object storage before inserting the metadata row into Pastes DB, ensuring a crash never creates a live key pointing to missing bytes:

On the read path, an edge cache hit returns immediately from the CDN. On an edge miss, the application server checks the metadata cache, queries Pastes DB on a cache miss, populates the cache, verifies expires_at > now, fetches the immutable body from object storage, and returns it with Cache-Control: public, max-age=<remaining_ttl>:

What separates answers — high-level architecture

BadSingle server and database table holding both key and body, no cache▾

GoodDedicated key generator, object storage for bodies, cache and CDN on reads▾

GreatDerives each component from a failure mode and orders writes for crash safety▾

Key idea. Each component in the high-level design answers one bottleneck of the single-database baseline: the key pool eliminates collision probes, object storage removes body bloat, the CDN and metadata cache absorb the 100:1 read skew, and lazy expiry plus a sweeper reclaims past-due pastes.

## 6. Deep dives

### 6.1 Short unique key generation and KGS internals

Before reading on. Every paste needs a seven-character key that is unique across billions of pastes, cheap to mint on the write path, and non-sequential so strangers cannot enumerate the corpus. Compare how random generation with a database check, a monotonic counter, a scrambled counter range, and a pre-generated key pool work, and trace how the key-generation service hands out keys safely under concurrency.

Design checkpoint

Why not encode an auto-incrementing counter (1, 2, 3...) directly into base-62 and use that as the paste key?

Base-62 counters frequently collide when two requests arrive at the same millisecondA raw counter never collides, but consecutive pastes receive consecutive keys, letting anyone enumerate and scrape every unlisted paste by counting up

Four progressive approaches can mint a seven-character base-62 key (the same family of techniques covered in Unique ID Generators and URL Shortener):

- Option 1: Random base-62 plus a database collision check. Draw a random seven-character base-62 string and query Pastes DB (or attempt an INSERT and retry on a duplicate-key error) to verify the key is unused. Because the key space (62⁷ ≈ 3.52 trillion) is roughly a hundred times larger than ten-year paste volume (36.5 billion), random collisions sit near 0% early on and reach only ~1% after a decade. Retry loops are therefore rare, and the real drawback is that 100% of writes must perform a synchronous database index lookup on the hot path before inserting the paste.

- Option 2: Monotonic counter encoded to base-62. Increment a counter and convert the integer to base-62. Collisions cannot happen because every write receives a distinct number, and no database lookup is needed to check uniqueness. Consecutive pastes receive adjacent keys ("000001a", "000001b", "000001c"), making the entire unlisted paste corpus trivially enumerable, while a single global counter becomes a write contention point.

- Option 3: Counter range allocation plus a reversible Feistel scramble. A coordination service allocates each application server a disjoint block of counter values (such as [10,000..19,999]), letting the server increment its counter in local memory and request a new block only when the current one runs low. Because 62⁷ ≈ 3.52 trillion sits between 2⁴¹ (2.20 trillion) and 2⁴² (4.40 trillion), seven base-62 characters hold 41 to 42 bits of state. Before base-62 encoding, the server passes the counter through a Feistel cipher permutation. A Feistel permutation splits the integer's bits into left and right halves (L, R) and applies several rounds of reversible XOR mixing with a secret key: L_next = R and R_next = L XOR F(R, round_key). Because every round is strictly invertible, two different counters can never produce the same output (zero collisions), while adjacent counters (10001, 10002) map to unrelated base-62 keys ("v4Kp9xM", "3nQr8bT") that cannot be enumerated.

- Option 4: Pre-generated key pool via a Key-Generation Service (the design's choice). Rather than scrambling counters on the fly, a dedicated key-generation service (KGS) generates random unique 7-character base-62 keys offline and hands them to application servers in batches. Moving key generation offline keeps the hot write path to a single in-memory pop per request.

Press Step write (or Play writes) under Option 4: Pre-generated key pool to watch POST /v1/pastes pop "a7x3kLm" and subsequent keys from local server memory with 0 database collision probes, then switch to Option 1, Option 2, and Option 3 to compare per-write database probes and key predictability.

Option 1: Random + DB checkOption 2: Base-62 counterOption 3: Counter + scrambleOption 4: Pre-generated key pool

Step writePlay writes ResetWrite #1 of 8

DB collision probes / write

0 probes / write

Key uniqueness guaranteed before DB insert

Key predictability

Non-sequential

Random 7-char base-62 keys cannot be guessed

Local server key batch

5 / 6 keys ready

Popped in memory; refills when batch <= 2

Recent POST /v1/pastes key minting trace

Write #1: /a7x3kLm0 DB probes

Write #1: popped pre-verified key 'a7x3kLm' from local server memory (0 DB probes on write path).

#### How the Key-Generation Service (KGS) works internally

To guarantee that two application servers never hand out the same key and that KGS itself never becomes a latency bottleneck or single point of failure, KGS is structured around five mechanisms:

- free_keys and used_keys tables in the KGS database: An offline background worker generates random 7-character base-62 strings in bulk (or shuffles disjoint numeric ranges so offline generation itself is collision-free) and inserts them into a free_keys (key CHAR(7) PRIMARY KEY) table. Once a batch of keys is handed to an application server, those rows are moved from free_keys into used_keys so they can never be handed out again.

- Atomic batch claims using FOR UPDATE SKIP LOCKED: Application servers do not call the KGS database on every paste creation. Instead, each application server claims a batch of 1,000 keys at once by running an atomic transaction that selects and deletes 1,000 rows using SELECT key FROM free_keys LIMIT 1000 FOR UPDATE SKIP LOCKED, inserts them into used_keys, and returns the batch to the caller. The SKIP LOCKED clause instructs the database to skip any rows currently locked by another application server's concurrent batch request. Multiple application servers can therefore refill their batches in parallel without blocking one another and without ever receiving overlapping keys.

- In-memory server batching and crash-loss tolerance: Each application server stores its claimed 1,000 keys in an in-memory queue (synchronized with a local mutex) and pops one key per POST /v1/pastes in nanoseconds. When the server's in-memory queue drops below 200 keys, an asynchronous background thread fetches the next batch of 1,000 keys from KGS before the buffer runs dry. If an application server crashes or restarts, the remaining few hundred keys in its memory are already recorded in used_keys and are discarded rather than recovered. Discarding up to 1,000 keys on a server crash is harmless because 1,000 keys represent 0.00000003% of the 3.52-trillion key space, and throwing them away guarantees a crashed server can never cause a duplicate key assignment.

- High availability without a single point of failure: Because every application server holds hundreds of pre-claimed keys in local memory (several minutes of write runway per server), a brief KGS restart or database failover does not interrupt live POST /v1/pastes traffic. Running the KGS database with an active-standby replica (or partitioning free_keys across two independent KGS instances that own disjoint key prefixes) keeps batch refills continuously available.

- Write ordering and custom alias isolation: On POST /v1/pastes, the application server writes the text bytes to object storage before inserting the key -> body_ref row into Pastes DB. If the server crashes between the two steps, it leaves an unreferenced blob in object storage (cleaned up later) rather than a live database key pointing to missing bytes. Meanwhile, user-supplied custom_alias values must be 8 to 32 characters long, whereas KGS only mints 7-character keys. Because those two length ranges never overlap, a custom alias inserted directly into Pastes DB can never collide with a pre-generated key sitting inside free_keys.

### 6.2 The read-heavy serving path

Before reading on. One paste goes viral on a developer forum and is read one million times in an hour. Trace which layer serves those reads, how many of them reach the database, and what happens if bots flood the service with requests for random non-existent keys.

Design checkpoint

A botnet floods the service with GET requests for millions of random seven-character keys that were never created. Why does negative caching (caching 'key -> 404' in the memory cache or CDN) fail to protect the database, and what fixes it?

Negative caching works fine because bots repeat the same random keysEach random seven-character key out of 3.52 trillion is requested only once, so every probe misses the negative cache and hits the database; a Bloom or counting filter of existing keys on each shard rejects definite misses in memory before touching disk

Because a paste never changes after creation, caching requires no invalidation logic on updates. Every layer caches a paste with a TTL capped at its remaining lifetime (expires_at - now).

Reads flow through three layers:

- CDN edge: For raw reads (GET /{key}) and cacheable paste responses, the CDN caches the immutable body at edge points of presence (PoPs) worldwide. When a paste goes viral and receives a million reads in an hour, each CDN edge location fetches the paste from the origin at most once (a few dozen to a few hundred edge fills globally) and serves the remaining hundreds of thousands of reads directly from edge memory.

- In-memory metadata cache (cache-aside): When a request misses at the edge and reaches the origin, the application server checks the distributed in-memory metadata cache for the 100-byte key -> (body_ref, expires_at) record. On a cache hit, the server skips the database entirely and fetches body_ref from object storage.

- Hash-sharded database and object storage: On a metadata cache miss, the application server queries Pastes DB and writes the returned metadata row into the cache. Because every lookup is a point query by key with no cross-paste joins, sharding Pastes DB by hash(key) distributes storage and cache-miss queries uniformly across shards, with read replicas on each shard absorbing remaining read load.

Two distinct miss patterns require separate defenses at the origin:

- One viral paste (hot key): Millions of requests target the same valid key. The CDN edge and metadata cache absorb repeat hits, and the application server uses request coalescing (also called singleflight) on cache misses. With request coalescing, the first request for a cold key registers an in-flight entry in memory, and any concurrent requests arriving for that same key wait for that single database and object-storage fetch to complete rather than issuing duplicate origin reads.

- Repeated dead links versus random-key probe floods: When a popular external page links to a deleted or mistyped key, the application server uses negative caching, storing a key -> 404 entry in the metadata cache with a short TTL of 30 to 60 seconds so repeated requests for that dead key are absorbed in memory. When bots probe millions of distinct random keys, negative caching has a near-zero hit rate because each random key is requested only once. To block random probes without risking false 404 responses on newly created pastes across stateless app servers, each Pastes DB shard maintains an in-memory Bloom filter (alongside the LSM storage engine's per-SSTable Bloom filters) that is updated synchronously whenever that shard inserts a new key. Any lookup routed to that shard by hash(key) checks the shard's filter first and returns 404 Not Found in memory if the key is definitely absent, avoiding any disk read. Standard bit-array Bloom filters cannot clear individual bits when keys expire because flipping a 1 bit back to 0 could clear a bit shared by another live key's hash; shards therefore use a counting Bloom filter or periodically rebuild the filter from live keys after background sweeps.

- Failure modes and monitoring: If the metadata cache cluster degrades, cache misses fall through to the database shards. Provision database read replicas and request coalescing to survive a cold cache, and monitor CDN cache hit ratio, metadata cache hit ratio, p99 read latency, and shard filter rejection rates.

What separates answers — the read-heavy serving path

BadEvery read queries the database and reads the body from the row▾

GoodObject storage for bodies with a cache and CDN in front▾

GreatLayered CDN + cache + hash-sharded DB, shard membership filter for random probes, negative cache for dead links▾

### 6.3 Expiration and storage reclamation

Before reading on. A creator submits a paste with a one-hour TTL. Explain why the system does not schedule a per-paste timer job for the exact one-hour mark, what prevents an expired paste from remaining readable at the origin or CDN edge, and what reclaims the underlying storage bytes.

Design checkpoint

If a paste expires lazily when read at the origin, what stops a CDN edge node that cached the paste 30 minutes ago from continuing to serve it for hours after its expires_at timestamp?

The origin must run a per-second cron job that calls the CDN purge API for every expiring pasteWhen the origin serves a paste, it caps the HTTP Cache-Control max-age header at the paste's remaining lifetime (expires_at - now), so the CDN entry expires no later than the paste itself

Scheduling an individual timer to fire at the exact expiration second for each of millions of pastes creates timer-management overhead and delete spikes at popular round-number boundaries. Instead, the system separates expiration into two mechanisms operating on different timescales: visibility enforcement (an expired paste must stop being readable the instant its TTL elapses) and storage reclamation (the database row and object-storage bytes are deleted asynchronously so disk usage stays bounded):

- Lazy expiration on read (immediate visibility enforcement): Whenever a read reaches the origin on a cache or CDN miss, the application server compares expires_at against now. If expires_at <= now, the server treats the row as expired and returns 404 Not Found without fetching the body from object storage.

- Capping cache and CDN TTLs at remaining lifetime: When the origin serves a live paste that has an expiration timestamp, it computes remaining_seconds = expires_at - now and sets both the metadata cache TTL and the HTTP Cache-Control: public, max-age=<remaining_seconds> header to remaining_seconds. Edge nodes therefore stop serving the cached body at the exact expiration second and revalidate with the origin, which returns 404 Not Found. For pastes created with no expiration (expires_at IS NULL), the origin sets a long max-age such as one year.

- Batched background sweeper and native store lifecycle rules (asynchronous reclamation): Lazy expiration hides expired pastes from readers immediately while leaving their bytes on disk until the next cleanup cycle. A background sweeper periodically queries each database shard using the expires_at index for batches of past-due rows (SELECT key, body_ref FROM pastes WHERE expires_at < NOW() LIMIT 1000), deletes the corresponding objects from object storage in a batch request, and deletes the metadata rows. Native storage mechanisms further reduce the sweeper's work: key-value stores with native per-row TTL evict expired metadata rows during compaction, and object-storage bucket lifecycle policies (using prefixes grouped by TTL tier such as ttl-1h/, ttl-1d/, ttl-30d/) reclaim expired blobs automatically.

Press Step (+1s) or Play timeline to watch a paste with a 6s simulated TTL return 200 OK from the CDN edge until t = 6.0s, switch immediately to 404 Not Found at t = 6.0s via lazy expiration, and hold its past-due bytes on disk until the t = 10.0s batch sweep reclaims them.

Paste TTL (expires_at)6s

Sweeper batch interval10s

Step (+1s)Play timeline Resett = 0.0s · expires at 6.0s · sweep at 10.0s

0.0s (created)▲ expires_at (6.0s)▲ batch sweep (10.0s)

What a reader sees

200 OK (Readable)

CDN TTL: 6.0s left

CDN edge cache

Cached at edge

max-age capped at 6s

Disk / blob storage

Live bytes stored

Next batch sweep at t = 10.0s

t=0.0s: Paste created with expires_at = 6.0s (CDN max-age = 6s). Background batch sweep scheduled at t=10.0s.

- Failure modes and monitoring: If the background sweeper falls behind, read correctness is unaffected because lazy checks and capped max-age headers still prevent expired pastes from being served, while disk usage temporarily grows. Monitor sweeper lag, the count of past-due-but-unswept rows (expires_at < now), and a canary metric for any 200 OK response served where expires_at <= now (which must remain zero).

What separates answers — expiration and reclamation

BadPer-paste scheduled delete timers at the exact expiry second, or no cleanup▾

GoodLazy expiry check on read plus a periodic cleanup job▾

GreatRead-time lazy expiry, capped CDN/cache max-age, batched sweeper + native store TTLs▾

Key idea. Pre-generated key pools (or scrambled counter blocks) remove collision checks from writes, layered CDN and memory caches with a shard membership filter shield the hash-sharded database on reads, and capped max-age headers plus lazy read checks enforce expiration to the second while a batched sweeper reclaims storage asynchronously.

## 7. Variants

### 10× scale

At 10× scale (~100 million new pastes per day, ~1,157 writes/s, ~115,700 reads/s), the architecture keeps the same structure:

- Reads (~115,700/s): Absorbed almost entirely by the CDN edge and metadata cache because paste bodies remain immutable. Expanding CDN edge presence and keeping cache hit ratios high shields the origin.

- Writes (~1,157/s): Increase the batch size claimed by each application server from KGS (for example, from 1,000 keys to 10,000 keys per refill) so servers continue minting keys in memory without contending on the KGS database. Add shards to Pastes DB hashed by key, which scales horizontally with no cross-shard transactions.

- Storage: Active storage scales linearly with live pastes while TTL expiration caps the working set; cold archival object-storage tiers handle non-expiring pastes that have not been read in months.

### Private and unguessable pastes

Supporting private pastes rather than unlisted-by-link access adds an authentication and authorization layer (owner_id, visibility enum public | unlisted | private, or an access-control list on Paste). Unlisted pastes that need stronger resistance against brute-force guessing can lengthen the minted key from 7 characters (62⁷ ≈ 3.52 trillion) to 16 or 22 base-62 characters (~95 to 130 bits of entropy). Truly private pastes cannot be cached as public unauthenticated CDN objects; they either serve through authenticated application servers backed by the metadata cache or use short-lived signed CDN URLs minted after the application server verifies the caller's authorization.

### Analytics and view counts

Tracking a per-paste view counter inverts the workload: view_count is a high-write, low-read field updated on every read, the exact opposite of the immutable paste body. Incrementing a row in Pastes DB on every read would undo the read-path cache offload. Instead, application servers increment counters in an in-memory store (or local server buffers) and flush aggregated increments to the database asynchronously in periodic batches. This pattern is called write-behind batching (covered in Caching). When counting unique viewers rather than raw hits, a probabilistic cardinality sketch such as HyperLogLog estimates unique visitors per paste in ~1.5 KB of memory.

### Abuse and moderation

Public pastebins attract automated spam dumping, phishing pages, malware payloads, and leaked credentials, making write-side abuse defense and fast takedown operational priorities:

- Ingest protection: Enforce per-IP and per-account rate limiting and bot challenges on POST /v1/pastes. Scan uploaded text inline for known-bad cryptographic hashes and URL blocklists, and run heavier regular-expression scans for leaked credentials asynchronously.

- Fast takedown: When moderation flags a paste, mark the Paste row with a tombstone (status = 'deleted'), delete the object from object storage, and issue an active CDN cache purge for /{key} so edge nodes stop serving the content within seconds rather than waiting for max-age to expire.

Key idea. Scaling 10× widens the key batch size and adds hash shards while the CDN absorbs the read multiplier; view counters use write-behind batching so they do not turn cached reads back into database writes; and moderation relies on rate limiting, ingest scanning, and active CDN cache purges.

## 8. The transferable pattern

Pastebin is a minted short-key mapping in front of an immutable, cacheable, expiring blob. Because writes are rare and exist to mint a unique, non-enumerable handle while reads are frequent and fetch an immutable payload, the architecture reduces to three building blocks: a collision-free key generator (pre-generated KGS pool or scrambled counter ranges), a metadata-versus-blob storage split, and a layered edge/memory cache whose TTL is capped at the object's remaining lifetime.

The same architectural pattern recurs across every system where a short handle addresses a write-once resource: URL shorteners (where the payload is a redirect target URL small enough to stay inline in the row), image-hosting and screenshot-sharing services, build-artifact stores, and ephemeral file-drop links.

Key idea. Mint a collision-free, non-sequential short key off the database hot path, separate the 100-byte lookup row from the immutable blob, and let the CDN and metadata cache serve every subsequent read until the capped TTL expires.

## Review: the 30-second answer

- Model: Each paste is an immutable text blob addressed by a 7-character base-62 key: written once, read ~100× more often, and optionally set to expire after a TTL.

- Key generation: Mint short base-62 keys that never collide and are not sequentially enumerable by claiming in-memory key batches from a pre-generated key-generation service (KGS) pool via FOR UPDATE SKIP LOCKED (or counter blocks passed through a reversible Feistel scramble) rather than probing Pastes DB on every write.

- Storage split: Keep the ~100-byte key -> body_ref metadata row in a hash-sharded database and store the kilobyte-to-megabyte text body in object storage, writing the blob before the database row so a crash never leaves a dangling key.

- Read path: Serve raw bodies from a CDN and metadata mappings from a cache-aside metadata cache with request coalescing; shield the sharded database from random-key bot scans with a shard-level Bloom/counting filter and from repeated dead links with short-TTL negative caching.

- Expiration: Enforce expiry lazily at read time (expires_at <= now) and cap CDN and cache Cache-Control: max-age headers at expires_at - now, while a periodic batched sweeper and bucket lifecycle policies reclaim expired rows and blobs asynchronously.

## Quiz

Pastebin Design Quiz

Hide AllReveal All

1)Why is read latency — rather than write throughput — the primary number to design around in Pastebin, and what property of a paste makes optimizing reads straightforward?

2)What makes the GET /{key} read endpoint directly cacheable at the CDN edge, and what serves as the cache key?

3)In the data model, what forced the paste body out of the Paste database record, and why does supporting a custom_alias require no new table?

4)How does the Key-Generation Service (KGS) hand out keys without per-write database queries or duplicate assignments across concurrent application servers?

5)Why expire pastes lazily on read instead of scheduling a deletion job for each paste's exact expiration second, and why must CDN max-age be capped at (expires_at - now)?

## Sources and further reading

- RFC 7234 / RFC 9111: HTTP Caching — the specification for Cache-Control: max-age and how shared CDN caches compute freshness lifetimes and expiration.

- Space/Time Trade-offs in Hash Coding with Allowable Errors — Burton H. Bloom (1970) — the original paper introducing Bloom filters for compact set-membership checks that reject definite misses in memory.

- Ticket Servers: Distributed Unique Primary Keys on the Cheap — Flickr Engineering — early production write-up on distributed counter generation and why naive single-counter sequences become a bottleneck and leak order.

- Amazon S3 Object Expiration and Lifecycle Management — how object stores implement asynchronous background expiration rules to reclaim expired objects at scale.
