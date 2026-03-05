---
layout: simple
title: "Design S3-Like Object Storage"
permalink: /system_design/design-s3-object-storage
---

# Design S3-Like Object Storage

A distributed object storage service that stores and retrieves any amount of data with 99.999999999% (11 nines) durability. Unlike file systems with hierarchical directories, object storage uses a flat namespace of buckets and keys — enabling massive scale without directory locking or inode bottlenecks.

> **Interview context**: This is a senior/staff-level system design question. Focus on **storage internals** — data placement, durability via erasure coding, metadata management, and the read/write path. Don't spend too long on the API layer; interviewers want to see you understand how bytes get stored reliably at massive scale.

---

## Table of Contents

1. [Requirements](#1-requirements)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Metadata Service](#3-metadata-service)
4. [Data Placement Engine](#4-data-placement-engine)
5. [Storage Engine](#5-storage-engine)
6. [Durability — Erasure Coding vs Replication](#6-durability--erasure-coding-vs-replication)
7. [Read/Write Path](#7-readwrite-path)
8. [Scalability](#8-scalability)
9. [Reliability](#9-reliability)
10. [Interview Tips](#10-interview-tips)
11. [Key Takeaways](#11-key-takeaways)

---

## 1. Requirements

> **Interview context**: Always start by clarifying requirements. Object storage sounds simple — PUT and GET — but the durability and scale requirements drive every design decision.

### Questions to Ask the Interviewer

- What's the expected object size distribution? (mostly small KBs or large GBs?)
- Do we need strong consistency or eventual consistency?
- What durability guarantee? (11 nines like S3?)
- Do we need versioning and lifecycle policies?
- What's the read/write ratio?

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Bucket operations** | Create, list, delete buckets (namespace containers) |
| **Object CRUD** | PUT, GET, DELETE objects identified by bucket + key |
| **Multipart upload** | Upload large objects (GBs) in parallel chunks |
| **Object versioning** | Optionally keep all versions of an object |
| **Object listing** | List objects in a bucket with prefix filtering |
| **Metadata** | Store and retrieve custom metadata per object |

### Non-Functional Requirements

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| **Durability** | 99.999999999% (11 nines) | Primary value proposition — never lose data |
| **Availability** | 99.99% | Business-critical storage |
| **Consistency** | Read-after-write for new PUTs; eventual for overwrites/deletes | Strong enough for most use cases |
| **Latency** | First-byte < 100ms (p99) for GETs | Competitive with S3 |
| **Scale** | 100B+ objects, exabytes of storage | Design for massive scale from day one |

### Capacity Estimation

```
Objects:           100 billion
Average object:    1 MB (heavily skewed — many small, few large)
Total storage:     100 PB (raw) → ~150 PB with erasure coding overhead

Traffic:
  PUT QPS:         100K (average), 500K (peak)
  GET QPS:         1M (average), 5M (peak)
  GET:PUT ratio:   ~10:1 (read-heavy)

Metadata:
  Per object:      ~500 bytes (key, size, checksum, location, timestamps)
  Total metadata:  ~50 TB
  Metadata QPS:    ~2M (every data op needs metadata lookup)
```

> **Key insight**: The metadata service sees **every request** — it's the hottest component. The data path moves terabytes, but the metadata path must handle millions of tiny lookups per second.

---

## 2. High-Level Architecture

> **Interview context**: "Let me draw the high-level architecture. The key insight is separating the metadata path from the data path — they have very different scaling characteristics."

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                     │
│                    (SDKs, CLI, Web Console)                               │
└─────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          API GATEWAY                                     │
│              (Rate limiting, Auth, REST routing)                          │
│         PUT /bucket/key    GET /bucket/key    DELETE                      │
└─────────────────────────────────────────────────────────────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
   ┌──────────────────────┐        ┌──────────────────────────┐
   │   METADATA SERVICE    │        │     DATA SERVICE          │
   │  (Distributed KV)     │        │  (Manages storage nodes)  │
   │                        │◄──────│                            │
   │  • Bucket index        │       │  • Data placement          │
   │  • Object index        │       │  • Erasure coding          │
   │  • Version history     │       │  • Read/write routing      │
   └──────────────────────┘        └──────────────────────────┘
              │                               │
              ▼                               ▼
   ┌──────────────────────┐        ┌──────────────────────────┐
   │   METADATA STORE      │        │     STORAGE CLUSTER       │
   │  (Sharded DB)         │        │                            │
   │                        │        │  ┌──────┐ ┌──────┐        │
   │  Partition key:        │        │  │Node 1│ │Node 2│ ...    │
   │  hash(bucket+key)     │        │  │ AZ-a │ │ AZ-b │        │
   └──────────────────────┘        │  └──────┘ └──────┘        │
                                     │  ┌──────┐ ┌──────┐        │
                                     │  │Node 3│ │Node N│        │
                                     │  │ AZ-c │ │ AZ-a │        │
                                     │  └──────┘ └──────┘        │
                                     └──────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Why Separate? |
|-----------|---------------|---------------|
| **API Gateway** | REST endpoint, auth, rate limiting | Stateless, horizontally scalable |
| **Metadata Service** | Object/bucket metadata CRUD | Latency-critical, small payloads (KBs) |
| **Data Service** | Route data to/from storage nodes | Throughput-critical, large payloads (MBs-GBs) |
| **Metadata Store** | Persist metadata durably | Different scaling (IOPS-bound, not bandwidth-bound) |
| **Storage Cluster** | Store raw object data on disks | Bandwidth-bound, petabytes of capacity |

> **Why separate metadata and data paths?** Metadata operations are tiny but extremely frequent (millions/sec). Data operations are large but less frequent. Mixing them in one system means metadata gets starved by bandwidth-hungry data transfers. Separating them lets each path scale independently.

---

## 3. Metadata Service

> **Interview context**: "The metadata service is the brain of the system. Let me explain how we index 100 billion objects efficiently."

### The Challenge

We need to:
- Look up any object among 100B+ by `(bucket, key)` in < 10ms
- Support prefix listing (`GET /bucket?prefix=photos/2024/`)
- Handle 2M+ metadata QPS
- Never lose metadata (it's the only way to find data)

### Options

| Option | Pros | Cons |
|--------|------|------|
| **Sharded SQL (e.g., Vitess)** | Strong consistency, SQL queries, prefix listing via LIKE | Sharding complexity, schema rigidity |
| **Distributed KV (e.g., DynamoDB-like)** | Massive scale, simple key-based sharding, proven at S3 scale | No native prefix listing (needs secondary index) |
| **LSM-based (e.g., RocksDB cluster)** | Excellent range scans, high write throughput | Operational complexity, compaction storms |

### Our Approach: Distributed KV Store with Prefix Index

We use a DynamoDB-like distributed KV store (this is what real S3 uses — S3's metadata runs on an internal DynamoDB derivative).

**Partition key**: `hash(bucket_name)` — distributes buckets across shards
**Sort key**: `object_key` — enables prefix listing within a bucket

```
┌─────────────────────────────────────────────┐
│            Metadata Record                    │
├─────────────┬───────────────────────────────┤
│ Partition   │ hash("my-bucket")              │
│ Sort Key    │ "photos/2024/cat.jpg"          │
├─────────────┼───────────────────────────────┤
│ object_id   │ uuid-v4                        │
│ version_id  │ "v3"                           │
│ size        │ 2,451,678                      │
│ checksum    │ sha256:abc123...               │
│ created_at  │ 2024-01-15T10:30:00Z           │
│ storage_cls │ "STANDARD"                     │
│ locations   │ [node17:disk3:off0,            │
│             │  node42:disk1:off0,            │
│             │  node89:disk7:off0]            │
│ ec_group    │ "pg-4521" (placement group)    │
│ user_meta   │ {"Content-Type": "image/jpeg"} │
└─────────────┴───────────────────────────────┘
```

### Why Not a Traditional RDBMS?

At 100B objects, even with sharding:
- **Schema migrations** across petabytes of metadata are nearly impossible
- **Join operations** are not needed (all queries are key-based or prefix-based)
- A KV store's **hash-based partitioning** naturally distributes hot buckets

> **Interviewer might ask**: "How do you handle listing objects with a prefix like `photos/2024/`?"
>
> Since the sort key is the full object key, prefix listing is a **range scan** within a single partition. We scan all sort keys starting with `photos/2024/` on the shard that holds `hash("my-bucket")`. For buckets with billions of objects, we paginate using a continuation token (the last key seen).

> **Interviewer might ask**: "What if one bucket has billions of objects and becomes a hot partition?"
>
> We **split hot partitions** by hashing `bucket_name + key_prefix`. For example, shard `hash("hot-bucket" + "a")` through `hash("hot-bucket" + "z")` across 26+ shards. The metadata service handles this transparently.

---

## 4. Data Placement Engine

> **Interview context**: "Now let me explain how we decide *where* to physically store each object's data. This is critical for both performance and durability."

### The Challenge

Given thousands of storage nodes across multiple availability zones:
- Decide which nodes store each object's data chunks
- Ensure chunks are spread across AZs (survive AZ failure)
- Minimize data movement when nodes join/leave
- Balance load evenly

### Options

| Option | Pros | Cons |
|--------|------|------|
| **Random placement** | Simple, good distribution | No locality, can't find data without metadata |
| **Consistent hashing (virtual nodes)** | Low data movement on changes, well-understood | Uneven distribution with heterogeneous hardware |
| **CRUSH-like algorithm** | Topology-aware, handles heterogeneous clusters | More complex to implement |

### Our Approach: CRUSH-like Placement with Placement Groups

Inspired by [Ceph's CRUSH algorithm](https://ceph.io/assets/pdfs/weil-crush-sc06.pdf), we use a deterministic, topology-aware placement.

**Key concept: Placement Groups (PGs)**

Instead of mapping each object directly to storage nodes (100B mappings!), we add an indirection layer:

```
Object Key  ──hash──▶  Placement Group (PG)  ──CRUSH──▶  Storage Nodes
                        (millions of PGs)                  (thousands)

Example:
  "photos/cat.jpg"
       │
       ▼ hash
  PG-4521
       │
       ▼ CRUSH(PG-4521, cluster_map)
  [Node-17 (AZ-a), Node-42 (AZ-b), Node-89 (AZ-c)]
```

**Why Placement Groups?**

| Without PGs | With PGs |
|-------------|----------|
| 100B object→node mappings | ~1M PG→node mappings |
| Massive rebalancing on node change | Only PGs on that node rebalance |
| Can't precompute | Placement is deterministic from PG ID + cluster map |

### CRUSH Algorithm: Topology-Aware Placement

```
Cluster Topology (Failure Domains):
┌──────────────────────────────────────────────────────┐
│                     Region: us-east                    │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────┐  │
│  │    AZ-a         │ │    AZ-b         │ │  AZ-c    │  │
│  │ ┌────┐ ┌────┐  │ │ ┌────┐ ┌────┐  │ │ ┌────┐   │  │
│  │ │Rack│ │Rack│  │ │ │Rack│ │Rack│  │ │ │Rack│   │  │
│  │ │ 1  │ │ 2  │  │ │ │ 3  │ │ 4  │  │ │ │ 5  │   │  │
│  │ │N1  │ │N2  │  │ │ │N3  │ │N4  │  │ │ │N5  │   │  │
│  │ │N6  │ │N7  │  │ │ │N8  │ │N9  │  │ │ │N10 │   │  │
│  │ └────┘ └────┘  │ │ └────┘ └────┘  │ │ └────┘   │  │
│  └────────────────┘ └────────────────┘ └──────────┘  │
└──────────────────────────────────────────────────────┘

CRUSH Rule for Standard storage class:
  1. Select 3 distinct AZs
  2. Within each AZ, select 1 rack
  3. Within each rack, select 1 node with available capacity
  → Guarantees survival of any single AZ failure
```

### Rebalancing on Node Add/Remove

When a node joins or leaves:

```
Before: 1000 PGs across 100 nodes → ~10 PGs/node
Add node 101:
  Only ~10 PGs migrate to new node (1/100 of data moves)
  Other 990 PGs stay exactly where they are

This is MUCH better than naive hash-mod where ~99% of data reshuffles.
```

> **Interviewer might ask**: "How do you handle nodes with different disk capacities?"
>
> We assign **weight proportional to capacity**. A 20TB node gets 2x the PGs of a 10TB node. CRUSH naturally handles this — each node's weight is an input to the placement function.

---

## 5. Storage Engine

> **Interview context**: "Let me now talk about what happens on a single storage node — how bytes actually get written to disk."

### The Challenge

Each storage node manages tens of terabytes across multiple disks. We need to:
- Write objects efficiently (minimize random I/O)
- Read objects with low latency
- Reclaim space from deleted objects
- Detect and repair data corruption (bit rot)

### Object Storage on Disk

Unlike a filesystem that creates one file per object (millions of tiny files = inode exhaustion), we pack objects into large append-only data files:

```
Storage Node Disk Layout:
┌──────────────────────────────────────────────────────┐
│  /data/disk1/                                          │
│  ├── pg-4521/                  (placement group dir)   │
│  │   ├── data.0001             (sealed data file ~1GB) │
│  │   ├── data.0002             (sealed data file ~1GB) │
│  │   ├── data.0003.active      (current write file)    │
│  │   └── index.db              (offset index)          │
│  ├── pg-4522/                                          │
│  │   ├── data.0001                                     │
│  │   └── ...                                           │
│  └── wal/                      (write-ahead log)       │
│      └── wal.current                                   │
└──────────────────────────────────────────────────────┘
```

### Data File Format

Objects are packed sequentially into large data files (similar to how Haystack at Facebook stores photos):

```
Data File (data.0001):
┌──────────┬──────────────┬──────────┬──────────────┬──────────┐
│ Header   │   Object A   │ Header   │   Object B   │ Header   │ ...
│ (64B)    │   (data)     │ (64B)    │   (data)     │ (64B)    │
└──────────┴──────────────┴──────────┴──────────────┴──────────┘

Header:
  ┌──────────────────────────────────────────────────┐
  │  magic_number    (4B)  — file format validation   │
  │  object_id       (16B) — UUID                     │
  │  data_size       (8B)  — payload length           │
  │  checksum_algo   (1B)  — 0=CRC32, 1=SHA256       │
  │  checksum        (32B) — data integrity check     │
  │  flags           (1B)  — deleted, compressed      │
  │  padding         (2B)  — alignment                │
  └──────────────────────────────────────────────────┘
```

### Write Path on a Storage Node

```
1. Receive object data from Data Service
2. Append to Write-Ahead Log (WAL) → fsync for durability
3. Append Header + Data to active data file
4. Update in-memory offset index: object_id → (file, offset, size)
5. Periodically flush index to disk (index.db)
6. When data file reaches 1GB → seal it, start new active file
```

### Why Append-Only?

| Approach | Write Throughput | Space Efficiency | Complexity |
|----------|-----------------|------------------|------------|
| **One file per object** | Low (metadata overhead per file) | Good | Low |
| **Append-only packed files** | High (sequential I/O) | Needs compaction | Medium |
| **LSM-tree** | Very high writes | Compaction amplification | High |

We choose append-only packed files because:
- **Sequential writes** saturate disk bandwidth (vs random I/O for one-file-per-object)
- **No filesystem overhead** for millions of tiny files (no inode exhaustion)
- Modern SSDs/HDDs perform best with large sequential operations

### Garbage Collection (Compaction)

When objects are deleted, their space in data files isn't immediately reclaimed (it's marked with a tombstone flag). A background GC process compacts files:

```
Before GC:
  data.0001: [ObjA][DELETED][ObjC][DELETED][DELETED][ObjF]
                    ▲ wasted      ▲ wasted  ▲ wasted

After GC:
  data.0001.compacted: [ObjA][ObjC][ObjF]
  (index updated with new offsets)
```

GC runs when a data file has > 30% deleted space, during low-traffic hours.

> **Interviewer might ask**: "What about bit rot — silent data corruption on disk?"
>
> Every object has a checksum stored in its header. A background **scrubber** process reads every object periodically (e.g., every 30 days) and verifies checksums. If corruption is detected, the object is repaired from another replica or erasure-coded chunk.

---

## 6. Durability — Erasure Coding vs Replication

> **Interview context**: "Durability is the #1 requirement. Let me explain how we achieve 11 nines of durability. The key insight is that **erasure coding gives us better durability at lower storage cost** than simple replication."

### The Challenge

11 nines durability means: of 1 trillion objects stored for a year, we lose at most 1. How?

### Option 1: Triple Replication

```
Object A → Copy 1 (AZ-a) + Copy 2 (AZ-b) + Copy 3 (AZ-c)

Storage overhead: 3x (store 300 PB for 100 PB of data)
Durability: ~8 nines (assuming annual disk failure rate of 2%)
Can lose: Any 2 of 3 copies and still recover
```

### Option 2: Erasure Coding (Reed-Solomon)

```
Object A (split into data chunks + parity chunks):

  6 data chunks + 3 parity chunks = 9 total chunks
  (each on a different node, across 3 AZs)

  d1──┐                    ┌──d1  ← Original data
  d2──┤                    ├──d2    can be reconstructed
  d3──┤  Reed-Solomon      ├──d3    from ANY 6 of 9 chunks
  d4──┤  Encode            ├──d4
  d5──┤  ──────────▶       ├──d5
  d6──┘                    ├──d6
                           ├──p1  ← Parity (computed)
                           ├──p2
                           └──p3

Storage overhead: 1.5x (store 150 PB for 100 PB of data)
Durability: ~11 nines
Can lose: Any 3 of 9 chunks and still recover
```

### Comparison

| Factor | 3x Replication | Erasure Coding (6+3) |
|--------|---------------|---------------------|
| **Storage overhead** | 200% extra | 50% extra |
| **Durability** | ~8 nines | ~11 nines |
| **Read latency** | Low (read any copy) | Higher (need 6 chunks, or read from single node if available) |
| **Write latency** | Low (parallel writes) | Higher (encode + write 9 chunks) |
| **Repair cost** | Copy 1 full object | Read 6 chunks, compute, write 3 chunks |
| **Best for** | Small objects (< 1MB), hot data | Large objects (> 1MB), cold/warm data |

### Our Approach: Hybrid Strategy

```
┌──────────────────────────────────────────────────┐
│              Object Size / Access Pattern          │
│                                                    │
│  < 256KB (small)  →  3x Replication               │
│    • Encoding overhead dominates for tiny objects  │
│    • Fast reads (any replica)                      │
│                                                    │
│  ≥ 256KB (large)  →  Erasure Coding (6+3)         │
│    • Massive storage savings at scale              │
│    • 11 nines durability                           │
│                                                    │
│  Storage class "REDUCED_REDUNDANCY"  →  (4+2) EC  │
│    • 1.5x overhead, ~9 nines durability            │
│    • For reproducible data                         │
└──────────────────────────────────────────────────┘
```

### How 11 Nines is Calculated

```
Assumptions:
  - Annual disk failure rate (AFR): 2%
  - 9 chunks on 9 different nodes/disks
  - Background repair detects and fixes within 6 hours

P(losing one chunk in a year) = 0.02
P(losing 4+ chunks before repair) = C(9,4) × (0.02)^4 × (repair_window)
                                   ≈ 1e-11

This gives us ~11 nines durability.

Key: fast repair time is critical. If repair takes days instead of hours,
durability drops significantly.
```

> **Interviewer might ask**: "Why not just use 3x replication everywhere? It's simpler."
>
> At 100 PB scale, the storage cost difference is enormous: 3x replication needs **300 PB** of raw storage, erasure coding needs **150 PB**. That's **150 PB of savings** — millions of dollars in hardware. The complexity of erasure coding is well worth the cost savings and better durability.

---

## 7. Read/Write Path

> **Interview context**: "Let me walk through the complete PUT and GET flows to tie everything together."

### PUT Object Flow

```
Client                API Gateway         Metadata Svc      Data Service       Storage Nodes
  │                       │                    │                 │                   │
  │── PUT /bucket/key ──▶│                    │                 │                   │
  │   + data payload      │                    │                 │                   │
  │                       │── Auth + validate ─▶│                │                   │
  │                       │                    │── Check bucket  │                   │
  │                       │                    │   exists         │                   │
  │                       │◀── OK ────────────│                 │                   │
  │                       │                    │                 │                   │
  │                       │── Route data ──────────────────────▶│                   │
  │                       │                    │                 │                   │
  │                       │                    │                 │── Hash key to PG  │
  │                       │                    │                 │── CRUSH → nodes   │
  │                       │                    │                 │                   │
  │                       │                    │                 │   ┌─ Erasure Code ─┐
  │                       │                    │                 │   │ Split into 6+3  │
  │                       │                    │                 │   │ chunks           │
  │                       │                    │                 │   └────────────────┘
  │                       │                    │                 │                   │
  │                       │                    │                 │── Write chunk 1 ──▶│ Node-17 (AZ-a)
  │                       │                    │                 │── Write chunk 2 ──▶│ Node-42 (AZ-b)
  │                       │                    │                 │── Write chunk 3 ──▶│ Node-89 (AZ-c)
  │                       │                    │                 │   ... (9 parallel)  │
  │                       │                    │                 │                   │
  │                       │                    │                 │◀── ACK (6 of 9) ──│
  │                       │                    │                 │   (quorum write)    │
  │                       │                    │                 │                   │
  │                       │                    │◀── Store meta ──│                   │
  │                       │                    │   (locations,    │                   │
  │                       │                    │    checksum,     │                   │
  │                       │                    │    size)         │                   │
  │                       │                    │                 │                   │
  │◀── 200 OK ───────────│                    │                 │                   │
  │   + ETag (checksum)   │                    │                 │                   │
```

**Key details:**
- **Quorum write**: We wait for 6 of 9 chunks to be acknowledged (not all 9). The remaining 3 are written asynchronously. This balances latency with durability.
- **Read-after-write consistency**: The metadata record is written *after* data chunks are durable. Any subsequent GET will find the metadata and locate the data.
- **ETag**: The response includes a content-MD5/SHA256 so the client can verify end-to-end integrity.

### GET Object Flow

```
Client                API Gateway         Metadata Svc      Data Service       Storage Nodes
  │                       │                    │                 │                   │
  │── GET /bucket/key ──▶│                    │                 │                   │
  │                       │── Lookup ─────────▶│                │                   │
  │                       │                    │── Find record   │                   │
  │                       │                    │   by (bucket,    │                   │
  │                       │                    │    key)          │                   │
  │                       │◀── Locations ──────│                 │                   │
  │                       │   [node17,42,89..] │                 │                   │
  │                       │                    │                 │                   │
  │                       │── Fetch data ──────────────────────▶│                   │
  │                       │                    │                 │── Read 6 chunks ──▶│
  │                       │                    │                 │   (closest/fastest │
  │                       │                    │                 │    nodes)           │
  │                       │                    │                 │                   │
  │                       │                    │                 │◀── Chunk data ────│
  │                       │                    │                 │                   │
  │                       │                    │                 │   ┌─ Decode ───────┐
  │                       │                    │                 │   │ Reassemble from │
  │                       │                    │                 │   │ 6 data chunks   │
  │                       │                    │                 │   │ (or repair if   │
  │                       │                    │                 │   │  chunk missing)  │
  │                       │                    │                 │   └────────────────┘
  │                       │                    │                 │                   │
  │◀── 200 + data ────────│                    │                 │                   │
```

**Read optimization**: If the object was stored with replication (small object), we read from a **single replica** — no decoding needed. For erasure-coded objects, we read from the 6 closest/fastest data nodes. If a node is slow or down, we substitute a parity chunk and decode.

### Multipart Upload

For large objects (GBs), we split into parts uploaded in parallel:

```
1. Client: POST /bucket/key?uploads → returns upload_id
2. Client: PUT /bucket/key?partNumber=1&uploadId=xxx (parallel, in any order)
   PUT /bucket/key?partNumber=2&uploadId=xxx
   PUT /bucket/key?partNumber=3&uploadId=xxx
3. Each part is independently erasure-coded and stored
4. Client: POST /bucket/key?uploadId=xxx (complete, with part manifest)
5. Metadata service creates final object record pointing to all parts

Benefits:
  - Parallel upload saturates network bandwidth
  - Failed parts can be retried without re-uploading everything
  - Parts can come from different machines (distributed upload)
```

> **Interviewer might ask**: "How do you achieve read-after-write consistency?"
>
> When a PUT completes (200 OK), the metadata record is already committed to the metadata store. Any subsequent GET hits the metadata store first, finds the record, and retrieves the data. Since metadata is written *after* data is durable, there's no window where metadata points to non-existent data. For overwrites, we use versioning internally — the new version becomes the "current" atomically in the metadata store.

---

## 8. Scalability

> **Interview context**: "Let me discuss what bottlenecks emerge at scale and how we address them."

### Scaling Each Component

| Component | Scaling Strategy | Bottleneck Signal |
|-----------|-----------------|-------------------|
| **API Gateway** | Horizontal (stateless) | CPU/connection count |
| **Metadata Service** | Partition splitting, read replicas | Query latency > 10ms |
| **Data Service** | Horizontal (stateless routing) | Network bandwidth |
| **Storage Nodes** | Add nodes, CRUSH rebalances PGs | Disk capacity > 80% |

### Metadata Hotspot: The "Celebrity Bucket" Problem

```
Problem: A bucket with 1 trillion objects (e.g., a logging service)
         gets 1M reads/sec — single partition overwhelmed.

Solution: Adaptive partition splitting

  Before: All of bucket "logs" on partition P1

  After:  hash("logs" + key[0:2]) distributes across 256 partitions
          P1: keys aa-af
          P2: keys ag-al
          ...
          P256: keys za-zz

  The metadata service detects hot partitions and splits automatically.
```

### Small Object Optimization

Small objects (< 4KB) have disproportionate overhead — the metadata and erasure-coding overhead can exceed the data itself.

```
Strategy: Object aggregation (packing)

Instead of storing each tiny object independently:

  ┌─────────────────────────────────────────┐
  │         Aggregate Object (4MB)            │
  │  ┌──────┐┌──────┐┌──────┐┌──────┐       │
  │  │Obj 1 ││Obj 2 ││Obj 3 ││ ...  │       │
  │  │(1KB) ││(2KB) ││(512B)││      │       │
  │  └──────┘└──────┘└──────┘└──────┘       │
  └─────────────────────────────────────────┘

  Erasure code the aggregate, not individual objects.
  Metadata points to: aggregate_id + offset + size

  Trade-off: Deleting a single small object requires rewriting
             the aggregate (or marking as tombstone, compact later)
```

### Bandwidth Bottleneck: Large Object Throughput

```
Problem: Uploading a 5TB object — one node can't handle it.

Solution: Multipart upload with parallel erasure coding

  5TB object = 5,000 parts × 1GB each
  Each 1GB part → independently erasure coded (6+3)

  Effective upload throughput: limited by client's network,
  not any single server.
```

---

## 9. Reliability

> **Interview context**: "For reliability, let's walk through failure scenarios from small (disk) to large (region)."

### Failure Scenarios and Recovery

| Failure | Frequency | Impact | Detection | Recovery |
|---------|-----------|--------|-----------|----------|
| **Disk failure** | Daily (large clusters) | ~0.01% of data | SMART monitoring, I/O errors | Re-replicate affected PGs from remaining chunks |
| **Node failure** | Weekly | ~0.1% of data | Heartbeat timeout (30s) | CRUSH reroutes reads; background repair rebuilds chunks on new nodes |
| **Rack failure** | Monthly | ~1% of data | Network monitoring | Cross-rack chunks serve reads; repair over hours |
| **AZ failure** | Yearly | ~33% of nodes | Regional health check | Remaining 2 AZs have enough data (6+3 across 3 AZs = 3 chunks per AZ) |
| **Region failure** | Very rare | Full region down | DNS failover | Cross-region replication (if configured); recovery from backup region |

### Background Integrity: Anti-Entropy and Scrubbing

```
Continuous processes running on every storage node:

1. SCRUBBER (every 30 days per object)
   - Read each object's data
   - Verify checksum against stored checksum
   - If mismatch → trigger repair from other chunks
   - Detects: bit rot, silent disk corruption

2. ANTI-ENTROPY (hourly)
   - Compare PG membership (expected vs actual)
   - Detect under-replicated/under-coded PGs
   - Trigger repair for any PG with fewer than 9 healthy chunks

3. HEARTBEAT (every 10 seconds)
   - Storage nodes report health to Data Service
   - If no heartbeat for 30s → mark node as "suspect"
   - If no heartbeat for 5 min → mark as "down", begin repair
```

### Data Repair Flow

```
Node-42 fails (was storing chunk 2 of PG-4521):

1. Data Service detects Node-42 is down
2. PG-4521 now has 8 of 9 chunks — still healthy, but degraded
3. Background repair job:
   a. Read any 6 of remaining 8 chunks
   b. Decode → reconstruct original data
   c. Re-encode → generate new chunk 2
   d. CRUSH selects new node (Node-55) for chunk 2
   e. Write new chunk 2 to Node-55
4. Update metadata: PG-4521 locations updated
5. PG-4521 back to 9/9 healthy chunks

Time to repair: ~minutes for a single PG, hours for full node recovery
(thousands of PGs in parallel, throttled to avoid network saturation)
```

---

## 10. Interview Tips

### Approach (45 minutes)

```
0-5 min:   CLARIFY REQUIREMENTS
           - "What size objects? Read/write ratio? Consistency needs?"
           - Identify: durability target, scale (objects, bytes)
           - State: "I'll focus on storage internals — metadata, placement, durability"

5-10 min:  CAPACITY ESTIMATION
           - Objects, storage, QPS
           - "Metadata service is the hottest component — every request hits it"

10-15 min: HIGH-LEVEL ARCHITECTURE
           - Draw: API Gateway → Metadata Service + Data Service → Storage Nodes
           - Key insight: "Separate metadata path from data path"

15-25 min: DEEP DIVE — CHOOSE 2 OF:
           - Metadata service: distributed KV, partition key design
           - Data placement: CRUSH algorithm, placement groups
           - Durability: erasure coding vs replication, 11 nines math

25-35 min: READ/WRITE PATH
           - Walk through PUT and GET end-to-end
           - Explain quorum writes, read optimization
           - Discuss multipart upload

35-42 min: RELIABILITY
           - Node/AZ failure recovery
           - Background scrubbing for bit rot
           - Anti-entropy repair

42-45 min: WRAP UP
           - "Key decisions: erasure coding for durability + cost, CRUSH for placement,
              separated metadata/data paths for independent scaling"
```

### Key Phrases That Show Depth

| Instead of... | Say... |
|---------------|--------|
| "Replicate the data 3 times" | "For objects > 256KB, we use Reed-Solomon erasure coding (6+3) to achieve 11 nines durability at 1.5x storage overhead instead of 3x" |
| "Hash to find the server" | "We use placement groups as an indirection layer — hash the key to a PG, then CRUSH maps PGs to nodes topology-aware across AZs" |
| "Store metadata in a database" | "The metadata store is a distributed KV partitioned by hash(bucket) with object keys as sort keys, enabling both point lookups and prefix listing" |
| "Just add more servers" | "Storage nodes are added to the CRUSH map — only 1/N of placement groups migrate, minimizing data movement" |

### Common Follow-up Questions

| Question | Key Points |
|----------|------------|
| "How do you achieve 11 nines?" | Erasure coding 6+3 across 3 AZs + fast repair (hours, not days) + background scrubbing for bit rot |
| "What happens during an AZ outage?" | Each AZ has 3 of 9 chunks. Remaining 2 AZs have 6 chunks = enough to decode. Reads continue, repairs queue up. |
| "How is this different from a filesystem?" | Flat namespace (no directories), append-only packed storage (no one-file-per-object), immutable objects (no partial updates) |
| "Why not just use HDFS?" | HDFS is optimized for large sequential reads (batch analytics). Object storage needs random access by key, REST API, per-object permissions, and massive small-object support. |
| "How do you handle versioning?" | Each version is a separate object in storage. Metadata stores a version chain: latest → v3 → v2 → v1. Lifecycle policies can auto-expire old versions. |
| "What about cross-region replication?" | Async replication of objects to a secondary region. Metadata is replicated via change stream. RPO of minutes, not seconds. |

---

## 11. Key Takeaways

### Core Concepts

1. **Separate metadata from data**: They scale differently — metadata is IOPS-bound (millions of small lookups), data is bandwidth-bound (terabytes of transfers)
2. **Placement Groups**: An indirection layer between objects and nodes. Reduces mapping complexity from billions to millions and minimizes rebalancing.
3. **Erasure Coding > Replication**: For large objects, Reed-Solomon (6+3) gives 11 nines durability at 1.5x overhead vs 3x for triple replication.
4. **Append-only packed storage**: Don't create one file per object. Pack objects into large data files for sequential I/O efficiency.
5. **Fast repair is the durability secret**: 11 nines depends on fixing degraded data within hours. Slow repair = lost data.

### Trade-offs to Remember

| Trade-off | When to choose A | When to choose B |
|-----------|------------------|------------------|
| **Replication (A) vs Erasure Coding (B)** | Small objects (< 256KB), hot data needing low latency | Large objects, cost-sensitive, need max durability |
| **Strong consistency (A) vs Eventual (B)** | Read-after-write for new objects (user expectation) | Cross-region replication, listing consistency |
| **Flat namespace (A) vs Hierarchical (B)** | Massive scale, no directory locking | Need POSIX semantics (use a filesystem instead) |
| **Single large metadata store (A) vs Embedded per-node (B)** | Centralized index, easy listing | Better locality, no single point of failure |

### Red Flags to Avoid

- Don't treat object storage as a filesystem — no directories, no partial updates, no renames
- Don't ignore the metadata scaling problem — it's the hardest part at 100B+ objects
- Don't forget the math on erasure coding — interviewers love the durability calculation
- Don't skip failure recovery — AZ-level failure handling shows real depth
- Don't propose only replication — it wastes 2x more storage than erasure coding

---

## References

- [Amazon S3 — Paper: Amazon DynamoDB (2022)](https://www.usenix.org/system/files/atc22-alhosni.pdf) — S3 metadata runs on DynamoDB
- [Facebook Haystack — Photo Storage](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Beaver.pdf) — Append-only packed object storage
- [Ceph CRUSH Algorithm](https://ceph.io/assets/pdfs/weil-crush-sc06.pdf) — Topology-aware data placement
- [Reed-Solomon Erasure Coding Explained](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction) — The math behind durability
- [Windows Azure Storage (WAS)](https://sigops.org/s/conferences/sosp/2011/current/2011-Cascais/printable/11-calder.pdf) — Microsoft's object storage architecture
