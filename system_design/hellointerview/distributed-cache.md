---
layout: simple
title: "Design a Distributed Cache — Hello Interview Style"
permalink: /system_design/hellointerview/distributed-cache
---

# Distributed Cache

**Patterns:** Scaling Reads  
**Difficulty:** Medium  
**Source:** hellointerview.com (AI-generated full solution)

---

## Summary

- **Key challenge:** Serve get/set in <10ms over 1TB (~1B 1KB entries) at 100K RPS, staying available when nodes fail.
- **Core design:** Each node is a HashMap + doubly linked list (O(1) LRU) with TTL expiry; clients route keys over a consistent-hash ring (topology in ZooKeeper/etcd) to sharded primaries with async replicas.
- **Techniques:** Consistent hashing + vnodes to limit remapping and balance load; async primary-replica with auto-promotion for HA; lazy + sampled active expiry to bound memory; client L1 cache and key#N copies for hot reads; sharded counters/write coalescing for hot writes; pipelining + connection pools for latency.

## Understanding the Problem

💾 **What is a Distributed Cache?**  
A distributed cache stores key-value data in memory across multiple machines. Unlike a single-node cache, it scales horizontally to handle massive workloads and provides high availability through replication.

---

### Functional Requirements

**Core Requirements**

- Users should be able to `set`, `get`, and `delete` key-value pairs
- Users should be able to configure the expiration time (TTL) for key-value pairs
- Data should be evicted according to Least Recently Used (LRU) policy when memory is full

**Below the line (out of scope):**

- Users should be able to configure cache size per node
- Complex querying (only key-based lookup)
- Transaction support

### Non-Functional Requirements

**Core Requirements**

- The system should be highly available; eventual consistency is acceptable
- Operations should have low latency (< 10ms for `get` and `set`)
- The system should scale to store 1TB of data and handle 100K requests/second

**Below the line (out of scope):**

- Durability / persistence across restarts
- Strong consistency guarantees

### Constraints & Estimates

- 1TB total data, 100K RPS
- Assume average key-value size: 1KB → 1TB / 1KB = 1 billion entries
- 100K RPS / typical node handles ~10K RPS → need ~10 nodes minimum
- Read:write ratio assume ~80:20

---

## The Set Up

### Planning the Approach

This is an infrastructure design problem. We need to design **the cache itself** (data structures, eviction, TTL), not just use Redis as a black box. We'll:
1. Design the single-node cache (data structure + LRU + TTL)
2. Scale to a distributed cluster (sharding, replication, consistency)
3. Address operational concerns (hot keys, failures, rebalancing)

### Defining the Core Entities

- **CacheEntry** – key (string), value (bytes), created_at, ttl_seconds, last_accessed_at
- **CacheNode** – physical machine with an in-memory hash map + LRU doubly linked list

### The API

```
// Store a key-value pair with optional TTL
SET key value [EX seconds]
-> OK | ERROR

// Retrieve a value by key
GET key
-> value | NULL (key not found or expired)

// Delete a key
DELETE key
-> OK | NOT_FOUND

// Check existence without updating LRU
EXISTS key
-> true | false
```

---

## High-Level Design

### 1) Users should be able to `set`, `get`, and `delete` key-value pairs

**Single-node architecture:**

A cache node is an in-process key-value store backed by:
1. **Hash Map** (`HashMap<String, CacheEntry>`) – O(1) lookup by key
2. **Doubly Linked List** – tracks LRU order; head = most recently used, tail = least recently used
3. **Min-Heap or Sorted Set** – tracks TTL expirations

**GET flow:**
1. Look up key in HashMap
2. If found and not expired: move node to head of LRU list, return value
3. If found but expired: delete entry, return NULL
4. If not found: return NULL

**SET flow:**
1. If key exists: update value, move to head of LRU list
2. If key doesn't exist and cache is full: evict LRU tail, then insert new entry at head
3. Write entry to HashMap + LRU list

**DELETE flow:**
1. Look up in HashMap
2. Remove from HashMap + unlink from LRU list

GET/SET/DELETE are O(1) for the HashMap + LRU list. HashMap for O(1) lookup; doubly linked list allows O(1) node removal + insertion at head. (If TTLs are tracked in a min-heap, SET/DELETE with a TTL add O(log n); the lazy + active sampling approach below keeps everything O(1).)

### 2) Users should be able to configure TTL for key-value pairs

**TTL implementation options:**

| Strategy | Description | Trade-off |
|---|---|---|
| **Lazy expiration** | Check expiry only on GET | Simple; dead entries accumulate in memory |
| **Active expiration** | Background thread scans entries periodically | Reclaims memory proactively; some overhead |
| **Min-heap** | Priority queue ordered by expiry time; background thread pops expired | O(log n) insert, O(1) min; efficient cleanup |

**Best approach: Lazy + Active hybrid**
- Lazy check on every GET (always correct)
- Background thread every 100ms samples N random keys and evicts expired ones (like Redis's approach)
- This keeps memory usage bounded without scanning all entries

### 3) Data should be evicted according to LRU policy

**LRU data structure: HashMap + Doubly Linked List**

```
HashMap: key → pointer to DLL node
DLL: [head/MRU] ↔ node1 ↔ node2 ↔ ... ↔ [tail/LRU]
```

On GET: unlink node, re-insert at head → O(1)  
On SET (new key, cache full): remove tail node from DLL + HashMap, insert new node at head → O(1)

This is the classic LRU Cache implementation (LeetCode #146).

---

## Potential Deep Dives

### 1) How do we ensure our cache is highly available and fault tolerant?

**Replication strategies:**

**Option A: Primary-Replica (async replication)**
- Each shard has 1 primary + 2 replicas
- Writes go to primary; replicas sync asynchronously
- Reads can go to any replica (read scaling)
- On primary failure: auto-promote a replica

**Trade-off:** Eventual consistency. If primary fails before sync, in-flight writes are lost.

**Option B: Quorum writes (like Cassandra)**
- Write succeeds when acknowledged by W nodes (e.g., W=2 out of 3)
- Read checks R nodes (e.g., R=2) for latest value
- With W + R > N (3), reads always see latest write
- More consistent but higher write latency

**For a cache (eventual consistency OK):** Primary-replica is preferred — faster writes, good enough consistency.

**Node failure handling:**
1. Health checks (heartbeat every 1s) detect failed nodes
2. Coordinator promotes replica to primary automatically
3. Clients get updated routing table from coordinator
4. Rebalance data to remaining nodes (consistent hashing minimizes data movement)

### 2) How do we ensure our cache is scalable?

**Horizontal sharding with consistent hashing:**

Distribute keys across N cache nodes. Naive approach: `node = hash(key) % N` — but when N changes (node added/removed), nearly all keys re-map → mass cache invalidation (thundering herd on the backend DB).

**Consistent hashing solution:**
- Place nodes on a virtual ring (hash ring 0 to 2^32)
- Each key maps to the first node clockwise on the ring
- Adding/removing a node only re-maps keys from its neighbor → average total_keys/N keys move
- Use **virtual nodes** (vnodes): each physical node is represented by K virtual nodes (e.g., K=150) for even key distribution

```
Physical nodes: A, B, C
Virtual ring: A1 A2 ... A150 B1 B2 ... B150 C1 C2 ... C150
Key "foo" → hash("foo") = 2^31 → maps to nearest clockwise vnode → B73 → node B
```

**Cluster coordination:**
- Zookeeper or etcd stores the ring topology and routing table
- Cache clients get the routing table on startup and cache it locally
- Clients route requests directly to the correct node (no proxy hop)

### 3) How can we ensure an even distribution of keys across our nodes?

**Problem:** Even with consistent hashing, skewed key popularity can overload one node.

**Virtual nodes (vnodes):** Already help — each physical node handles multiple non-contiguous ring segments, spreading load.

**Key distribution monitoring:**
- Track request count per node
- If one node handles 3× average load, increase its vnode count
- Dynamically rebalance vnodes between nodes

### 4) What happens if you have a hot key that is being read from a lot?

**Problem:** A single key (e.g., the front-page article cache entry) receives 50K reads/sec — far beyond one node's capacity.

**Solutions:**

**Option A: Local client-side cache**
- Each application server caches the hot key in process memory (L1 cache)
- TTL: 1–5 seconds (short, so staleness is bounded)
- Drastically reduces load on the cache cluster

**Option B: Key replication (scatter reads)**
- Replicate hot key to multiple nodes: `hot_key#1`, `hot_key#2`, ..., `hot_key#N`
- On GET, randomly pick one replica → load is distributed across N nodes
- On SET, write to all replicas (or use async background sync)

**Option C: Consistent hashing with read replicas**
- Route reads to any replica of the shard holding the hot key
- Already handled by primary-replica architecture

**Best practice:** Combine local client-side cache (sub-millisecond, free) with hot-key replication for extreme cases.

### 5) What happens if you have a hot key that is being written to a lot?

**Problem:** A counter (e.g., "X views") being incremented by 100K writes/sec on a single node.

**Solutions:**

**Option A: Write batching (write coalescing)**
- Each app server accumulates increments locally for N ms, then sends one batched write
- Reduces writes from 100K/sec to 1K/sec at the cost of small latency in value freshness

**Option B: Redis-style INCR with sharded counters**
- Split counter into N shards: `counter:views:0`, `counter:views:1`, ..., `counter:views:N`
- Each write goes to a random shard
- On read: sum all N shards (eventual, slightly stale)

**Option C: Dedicated write-heavy key handling**
- Detect hot write keys (via request rate monitoring)
- Route them to a dedicated high-throughput node with extra resources

### 6) How do we ensure our cache is performant?

**Network:** Use UDP for read-only GET requests (lower overhead); TCP for SET/DELETE (reliability). Redis actually uses TCP for all operations — a reasonable trade-off.

**Serialization:** Use compact binary protocols (MessagePack, Protocol Buffers) instead of JSON to reduce payload size and parsing overhead.

**Connection pooling:** Clients maintain a pool of persistent TCP connections to each cache node. Avoid connection setup overhead on every request.

**Pipeline:** Batch multiple commands in a single TCP round-trip (Redis pipelining). Instead of 100 individual GET calls (100 RTTs), send 100 GETs in one TCP write → 1 RTT.

**Kernel bypass (DPDK) for extreme performance:** Skip the OS network stack using DPDK/RDMA for sub-100μs latency. Used by hyperscalers but overkill for most systems.

---

## Final Design

```
Client Applications
  │  (consistent hash routing, connection pool)
  ▼
┌─────────────────────────────────────────┐
│          Cache Cluster (N nodes)         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Node A  │  │ Node B  │  │ Node C  │ │
│  │ Primary │  │ Primary │  │ Primary │ │
│  │  ↓ async│  │  ↓ async│  │  ↓ async│ │
│  │Replica1 │  │Replica1 │  │Replica1 │ │
│  │Replica2 │  │Replica2 │  │Replica2 │ │
│  └─────────┘  └─────────┘  └─────────┘ │
└─────────────────────────────────────────┘
  │
  ▼
Coordinator (Zookeeper/etcd)
  - Ring topology
  - Node health
  - Routing table
```

**Single node internals:**
```
┌─────────────────────────────────┐
│          Cache Node             │
│  HashMap<key → DLL node ptr>    │
│  DLL: [MRU head] ↔ ... ↔ [LRU tail]  │
│  MinHeap: (expiry_ts, key)      │
│  Background TTL sweeper (100ms) │
└─────────────────────────────────┘
```

---

## What is Expected at Each Level?

### Mid-level
- Correct HashMap + DLL for O(1) LRU
- Basic TTL with lazy expiration
- Understands consistent hashing concept
- Single-node design is solid

### Senior
- Consistent hashing with virtual nodes
- Primary-replica replication for HA
- Active + lazy TTL eviction hybrid
- Identifies hot key read problem; proposes local client cache

### Staff
- Detailed failure handling (node failure → replica promotion → rebalance)
- Hot write key solutions (counter sharding, write coalescing)
- Performance optimizations (pipelining, connection pooling)
- Discusses quorum vs. async replication trade-offs
- Dynamic vnode rebalancing for skewed key distributions
