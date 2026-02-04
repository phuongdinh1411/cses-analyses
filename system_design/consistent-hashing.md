---
layout: simple
title: "Consistent Hashing"
permalink: /system_design/consistent-hashing
---

# Consistent Hashing

Consistent hashing is a distributed systems technique for distributing data across nodes in a way that **minimizes reorganization when nodes are added or removed**.

> **Interview context**: Consistent hashing is a foundational concept that appears in many system design questions. When asked about distributed caches, databases, or load balancing, this is often the underlying mechanism.

---

## Table of Contents

1. [The Problem with Regular Hashing](#the-problem-with-regular-hashing)
2. [How Consistent Hashing Works](#how-consistent-hashing-works)
3. [Why It's Better](#why-its-better)
4. [Virtual Nodes](#virtual-nodes)
5. [Replication and Durability](#replication-and-durability)
6. [Implementation](#implementation)
7. [Real-World Systems](#real-world-systems)
8. [Key Takeaways](#key-takeaways)

---

## The Problem with Regular Hashing

> **Interview context**: Start by explaining WHY consistent hashing exists. The problem it solves is more important than the solution.

### The Challenge

With traditional hashing (e.g., `hash(key) % N` where N = number of servers):

```
Server = hash("user_123") % 3  →  Server 1
```

**Problem**: If you add or remove a server, `N` changes, and almost ALL keys get remapped to different servers. This causes massive cache invalidation or data migration.

| Operation | Traditional Hash | Consistent Hash |
|-----------|------------------|-----------------|
| Add/remove 1 of 100 servers | ~99% keys remapped | ~1% keys remapped |

> **Interviewer might ask**: "Why is remapping bad?"
>
> For caches: remapping means cache misses → database overload ("thundering herd")
> For databases: remapping means data migration → downtime or complex operations

---

## How Consistent Hashing Works

### The Hash Ring

Imagine a circular ring of hash values (0 to 2^32-1):

```
                    0
                    |
           +---------------+
          /                 \
         |    Hash Ring      |
         |                   |
          \                 /
           +---------------+
```

### Placing Nodes on the Ring

Hash each server's identifier to position it on the ring:

```
                   0
                   |
            o------+------o  Server A
           /               \
          /                 \
   Server C o               |
          \                 /
           \               /
            o-------------o
                 Server B
```

### Placing Keys on the Ring

Hash each key and walk **clockwise** to find the first server:

```
        Key "user_123" hashes here
                   |
                   v -----> walks clockwise -----> o Server A
                  /
                 /
```

**Key "user_123" is stored on Server A** (the first server clockwise from the key's position).

### Key Lookup Process

```
1. Hash the key        →  hash("user_123") = 847291...
2. Find position       →  Locate this value on the ring
3. Walk clockwise      →  Find first node >= hash value
4. Query that node     →  Ask Server A for "user_123"
```

**The client (or a coordinator) computes which node owns the key, then queries only that node directly.** No broadcast needed.

---

## Why It's Better

When a server is **added or removed**, only keys between that server and its predecessor are affected:

```
Before:  A handles keys in range [C, A]
After removing A:  B now handles [C, B] (only A's keys move)
```

---

## Virtual Nodes

> **Interview context**: Virtual nodes are a critical optimization. Interviewers often ask about load balancing, and this is the answer.

### The Challenge

**Problem**: With few servers, distribution can be uneven.

**Solution**: Map each physical server to multiple "virtual nodes" on the ring:

```
Server A → A1, A2, A3, A4 (4 virtual nodes spread around ring)
Server B → B1, B2, B3, B4
```

### How Virtual Nodes Work

A **virtual node** is simply a hash ring position that maps back to a physical server. Instead of placing one point on the ring per server, you place many points (all pointing to the same physical server).

**Without virtual nodes** (3 servers):

```
Ring positions:
  hash("ServerA") = 1000     → ServerA
  hash("ServerB") = 5000     → ServerB
  hash("ServerC") = 9000     → ServerC
```

**With 4 virtual nodes each**:

```
Ring positions:
  hash("ServerA:0") = 1000   → ServerA
  hash("ServerA:1") = 4200   → ServerA
  hash("ServerA:2") = 7800   → ServerA
  hash("ServerA:3") = 11500  → ServerA

  hash("ServerB:0") = 2300   → ServerB
  hash("ServerB:1") = 5600   → ServerB
  ... etc
```

### Why Virtual Nodes Improve Distribution

Without virtual nodes (3 servers):

```
       o A
      /
     /     Large gap - ServerA gets ~60% of keys
    o------------------o
    C                  B   <- Small gap, B gets only 15%
```

With virtual nodes spread around:

```
    A1  B2  C1  A3  B1  C3  A2  B3  C2  A4  B4  C4
    o---o---o---o---o---o---o---o---o---o---o---o
```

Keys are now evenly distributed because each server has many evenly-spaced "claim points" on the ring.

### Virtual Node Counts in Production

| System | Virtual Nodes per Physical Node |
|--------|--------------------------------|
| **Cassandra** | 256 (default) |
| **Typical production** | 100-500 |

### Data Structure in Memory

The ring is just a sorted map: `hash_position → physical_server_name`

```
Positions:  1000 → ServerA
            2300 → ServerB
            3100 → ServerC
            4200 → ServerA  (same server, different position)
            5600 → ServerB
            7800 → ServerA  (again ServerA)
```

The word "virtual" means these nodes don't exist physically—they're simply extra entries with different string suffixes (`:0`, `:1`, `:2`) that produce different hash values, all pointing back to the same real server.

> **Interviewer might ask**: "Why not just have evenly-spaced fixed positions?"
>
> Because nodes join and leave dynamically. Random hash positions (via `hash("ServerA:0")`) are simpler than coordinated even spacing.

---

## Replication and Durability

**Consistent hashing solves routing. Replication solves durability.**

### Without Replication: Data Loss

When a node is removed, its data is **LOST**:

```
Before:                          After removing A:

       o A (has keys X, Y, Z)          (gone!)
      /                               /
     /                               /
    o C                             o C
     \                               \
      \                               \
       o B                             o B <- now responsible for X, Y, Z
                                           but doesn't have the data!
```

### With Replication: Data Survives

Production systems replicate data to **N successor nodes** on the ring:

```
Key "user_123" → Store on:
  1. Server A (primary)
  2. Server B (replica 1) <- next clockwise
  3. Server C (replica 2) <- next after B
```

```
       o A --- has "user_123" (primary)
      /|
     / | replicated to
    o  v
    C  o B --- has "user_123" (replica)
    |
    +-- has "user_123" (replica)
```

**When A is removed:**
1. B becomes the new primary for those keys
2. B already has the data (it was a replica)
3. System replicates to a new third node to maintain N=3

### Data Status by Scenario

| Scenario | Data Status |
|----------|-------------|
| Node removed, no replication | **Data lost** |
| Node removed, with replication | Data safe on replicas, system rebalances |
| Node added | New node receives data from neighbors (gradual migration) |

---

## Interview Tips

### How to Explain Consistent Hashing (5 minutes)

```
1. STATE THE PROBLEM (1 min)
   "With modulo hashing, adding a server remaps ~99% of keys.
    This causes cache stampedes or massive data migration."

2. INTRODUCE THE RING (1 min)
   "We place both servers AND keys on a circular hash space.
    Keys belong to the first server clockwise."

3. SHOW THE BENEFIT (1 min)
   "Adding a server only affects keys between it and its predecessor.
    ~1/N keys move instead of ~(N-1)/N."

4. EXPLAIN VIRTUAL NODES (1 min)
   "With few servers, distribution is uneven. Virtual nodes spread
    each server across many ring positions for better balance."

5. MENTION REPLICATION (1 min)
   "For durability, we replicate to N successive nodes clockwise.
    When a node fails, replicas already have the data."
```

### Key Phrases That Show Depth

| Instead of... | Say... |
|---------------|--------|
| "We use consistent hashing" | "We use a hash ring with 100-200 virtual nodes per server. Keys walk clockwise to find their owner." |
| "It's more efficient" | "Adding a node remaps only 1/N keys versus (N-1)/N with modulo hashing—that's 1% vs 99% for 100 servers." |
| "We replicate data" | "We replicate to N successor nodes on the ring. When a node fails, its successor already has the data and becomes the new primary." |

### Common Follow-up Questions

| Question | Key Points |
|----------|------------|
| "Why virtual nodes?" | Even distribution with few servers, smoother rebalancing |
| "How many virtual nodes?" | 100-500 typical, Cassandra uses 256 |
| "What hash function?" | MD5 for simplicity, Murmur3 for performance |
| "Hot spots?" | Virtual nodes help, but some keys are inherently hot |
| "What about replication?" | Replicate to N successive distinct physical nodes |

---

## Real-World Systems

> **Interview context**: Mentioning real systems shows practical knowledge.

### Amazon DynamoDB

- Uses consistent hashing for **partitioning data** across storage nodes
- Each partition key is hashed to determine which partition stores the data
- Uses **virtual nodes (vnodes)** for better load distribution
- Implements **quorum-based replication** (N replicas, W writes, R reads)
- Introduced in the famous [Dynamo Paper (2007)](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

```
Partition Key → MD5 Hash → Ring Position → N Replicas
```

### Apache Cassandra

- Directly inspired by DynamoDB's design
- Uses **Murmur3 hash** (faster than MD5) by default
- **Token ranges**: Each node owns a range of hash values
- **Virtual nodes (vnodes)**: Default 256 vnodes per physical node
- **Replication factor**: Configurable per keyspace

```sql
CREATE KEYSPACE my_app WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc1': 3,  -- 3 replicas in datacenter 1
  'dc2': 2   -- 2 replicas in datacenter 2
};
```

### Redis Cluster

- Uses **hash slots** (16384 fixed slots) instead of a continuous ring
- Each key is hashed: `SLOT = CRC16(key) % 16384`
- Slots are distributed across master nodes
- Simpler than continuous hashing but same principle

```
Node A: slots 0-5460
Node B: slots 5461-10922
Node C: slots 10923-16383
```

### Other Notable Systems

| System | Description |
|--------|-------------|
| **Memcached** | Clients implement consistent hashing via `libketama` |
| **Akamai CDN** | Pioneered consistent hashing for web caching (1997) |
| **Discord** | Routes messages to Elixir processes |
| **Riak** | Dynamo-inspired with hinted handoff and read repair |
| **Apache Kafka** | Partition assignment for consumer groups |
| **Couchbase** | 1024 vBuckets (similar to Redis hash slots) |
| **Netflix EVCache** | Memcached with zone-aware consistent hashing |

### Implementation Comparison

| System | Hash Function | Partitioning | Replication |
|--------|---------------|--------------|-------------|
| DynamoDB | MD5 | Continuous ring + vnodes | Quorum (N,R,W) |
| Cassandra | Murmur3 | Token ranges + vnodes | Configurable RF |
| Redis Cluster | CRC16 | 16384 hash slots | Primary + replicas |
| Memcached | Ketama (MD5) | Client-side ring | None (cache only) |
| Riak | SHA-1 | Ring + vnodes | N replicas + hinted handoff |
| Kafka | Murmur2 | Fixed partitions | ISR (In-Sync Replicas) |
| Couchbase | CRC32 | 1024 vBuckets | Configurable replicas |

### Algorithm Variations

| Variation | Used By | Benefit |
|-----------|---------|---------|
| **Virtual nodes** | Cassandra, DynamoDB, Riak | Better load balance |
| **Fixed slots/buckets** | Redis, Couchbase | Simpler resharding |
| **Jump consistent hash** | Google | O(1) memory, no ring storage |
| **Rendezvous hashing** | Microsoft, Twitter | Alternative to ring-based |

---

## Key Takeaways

### Design Decisions Summary

| Decision | Choice | Why |
|----------|--------|-----|
| **Hash space** | Circular ring (0 to 2^32-1) | Allows clockwise lookup |
| **Key assignment** | First server clockwise | Simple, deterministic |
| **Virtual nodes** | 100-500 per server | Even distribution |
| **Replication** | N successors | Durability without coordination |

### Trade-offs to Discuss

| Trade-off | Option A | Option B |
|-----------|----------|----------|
| Virtual nodes | Many (even distribution) | Few (simpler, faster lookup) |
| Hash function | MD5 (simple, standard) | Murmur3 (faster) |
| Replication | On ring (N successors) | Separate replication layer |
| Hot keys | Consistent hashing can't help | Need separate caching layer |

### Core Concepts

1. **Hash ring** - Nodes and keys share the same circular hash space
2. **Clockwise lookup** - Keys are assigned to the next node clockwise
3. **Minimal disruption** - Adding/removing nodes only affects neighboring keys (~1/N)
4. **Virtual nodes** - Multiple ring positions per server improves load balance
5. **Replication** - Consistent hashing solves routing; replication solves durability
