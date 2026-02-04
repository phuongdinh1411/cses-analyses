---
layout: simple
title: "System Design: Key-Value Store"
permalink: /system_design/design-key-value-store
---

# System Design: Key-Value Store

A distributed key-value store is a non-relational database that stores data as key-value pairs across multiple nodes. This document covers the design of a scalable, highly available key-value store suitable for system design interviews.

---

## Table of Contents

1. [Requirements](#requirements)
2. [High-Level Architecture](#high-level-architecture)
3. [API Design](#api-design)
4. [Data Partitioning](#data-partitioning)
5. [Replication](#replication)
6. [Consistency Models](#consistency-models)
7. [Handling Failures](#handling-failures)
   - 7.1 [Failure Detection: Gossip Protocol](#71-failure-detection-gossip-protocol)
   - 7.2 [Temporary Failures: Hinted Handoff](#72-temporary-failures-hinted-handoff)
   - 7.3 [Permanent Failures: Re-replication](#73-permanent-failures-re-replication)
   - 7.4 [Read Repair](#74-read-repair)
   - 7.5 [Comparison: Temporary vs Permanent](#75-comparison-temporary-vs-permanent-failures)
8. [Storage Engine](#storage-engine)
9. [System Architecture Diagram](#system-architecture-diagram)
10. [Trade-offs and Design Decisions](#trade-offs-and-design-decisions)
11. [Real-World Examples](#real-world-examples)
12. [Interview Tips](#interview-tips)

---

## Requirements

### Functional Requirements

| Requirement | Description |
|------------|-------------|
| `put(key, value)` | Insert/update a key-value pair |
| `get(key)` | Retrieve value by key |
| `delete(key)` | Remove a key-value pair |

### Non-Functional Requirements

| Requirement | Target |
|------------|--------|
| **Scalability** | Handle petabytes of data, millions of QPS |
| **High Availability** | 99.99% uptime (< 52 mins downtime/year) |
| **Low Latency** | p99 < 10ms for reads and writes |
| **Durability** | No data loss once acknowledged |
| **Tuneable Consistency** | Support eventual to strong consistency |

### Capacity Estimation (Example)

```
Assumptions:
- 100 million DAU
- Each user: 10 reads, 2 writes per day
- Average key size: 100 bytes
- Average value size: 10 KB

Calculations:
- Read QPS: (100M × 10) / 86400 ≈ 11,574 QPS
- Write QPS: (100M × 2) / 86400 ≈ 2,315 QPS
- Peak QPS (3x): ~35K reads, ~7K writes
- Daily storage: 100M × 2 × 10KB = 2 TB/day
- Yearly storage: ~730 TB (before replication)
```

---

## High-Level Architecture

```
                                    ┌─────────────────────────────────────┐
                                    │           Client Layer              │
                                    │  (SDK / HTTP Client / CLI)          │
                                    └──────────────┬──────────────────────┘
                                                   │
                                    ┌──────────────▼──────────────────────┐
                                    │         Load Balancer               │
                                    │     (Round Robin / Least Conn)      │
                                    └──────────────┬──────────────────────┘
                                                   │
                    ┌──────────────────────────────┼──────────────────────────────┐
                    │                              │                              │
         ┌──────────▼──────────┐       ┌──────────▼──────────┐       ┌──────────▼──────────┐
         │   Coordinator 1     │       │   Coordinator 2     │       │   Coordinator N     │
         │  (Stateless API)    │       │  (Stateless API)    │       │  (Stateless API)    │
         └──────────┬──────────┘       └──────────┬──────────┘       └──────────┬──────────┘
                    │                              │                              │
                    └──────────────────────────────┼──────────────────────────────┘
                                                   │
                                    ┌──────────────▼──────────────────────┐
                                    │     Consistent Hash Ring            │
                                    │   (Partition Key → Node Mapping)    │
                                    └──────────────┬──────────────────────┘
                                                   │
      ┌────────────────────────────────────────────┼────────────────────────────────────────────┐
      │                    │                       │                       │                    │
┌─────▼─────┐        ┌─────▼─────┐          ┌─────▼─────┐          ┌─────▼─────┐        ┌─────▼─────┐
│  Node A   │        │  Node B   │          │  Node C   │          │  Node D   │        │  Node N   │
│ ┌───────┐ │        │ ┌───────┐ │          │ ┌───────┐ │          │ ┌───────┐ │        │ ┌───────┐ │
│ │MemTab│ │        │ │MemTab│ │          │ │MemTab│ │          │ │MemTab│ │        │ │MemTab│ │
│ └───┬───┘ │        │ └───┬───┘ │          │ └───┬───┘ │          │ └───┬───┘ │        │ └───┬───┘ │
│ ┌───▼───┐ │        │ ┌───▼───┐ │          │ ┌───▼───┐ │          │ ┌───▼───┐ │        │ ┌───▼───┐ │
│ │SSTable│ │        │ │SSTable│ │          │ │SSTable│ │          │ │SSTable│ │        │ │SSTable│ │
│ └───────┘ │        │ └───────┘ │          │ └───────┘ │          │ └───────┘ │        │ └───────┘ │
└───────────┘        └───────────┘          └───────────┘          └───────────┘        └───────────┘
     │                    │                       │                       │                    │
     └────────────────────┴───────────────────────┼───────────────────────┴────────────────────┘
                                                  │
                                    ┌─────────────▼─────────────┐
                                    │    Replication Layer      │
                                    │  (Sync/Async Replication) │
                                    └───────────────────────────┘
```

### Components

| Component | Responsibility |
|-----------|---------------|
| **Client** | SDK that routes requests and handles retries |
| **Coordinator** | Stateless node that handles routing, quorum reads/writes |
| **Storage Node** | Stores data partitions, handles local reads/writes |
| **Consistent Hash Ring** | Maps keys to nodes (see [consistent-hashing.md](./consistent-hashing.md)) |
| **Replication Manager** | Manages data replication across nodes |

---

## API Design

### Core Operations

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PUT /v1/kv/{key}                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Request:  { "value": "...", "ttl": 3600 }               │   │
│  │ Response: { "version": 12345, "status": "ok" }          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  GET /v1/kv/{key}                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Response: { "value": "...", "version": 12345 }          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  DELETE /v1/kv/{key}                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Response: { "status": "deleted" }                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Internal RPC (Node-to-Node)

| Operation | Purpose |
|-----------|---------|
| `put(key, value, context)` | Write to local storage with conflict detection |
| `get(key)` | Read from local storage |
| `replicate(key, value, context)` | Accept replicated data from peer |
| `handoff(key_range, target_node)` | Transfer key range to another node |

---

## Data Partitioning

> **Interview context**: After high-level design, the interviewer will ask: "How do you distribute data across multiple nodes?" This is where consistent hashing comes in.

### Why Do We Need Partitioning?

A single server can't store petabytes of data or handle millions of QPS. We need to **split data across multiple nodes**. But how do we decide which node stores which key?

```
┌─────────────────────────────────────────────────────────────────┐
│                  Partitioning Options                           │
│                                                                 │
│   ❌ Option 1: Simple Modulo Hash                              │
│      node = hash(key) % N                                      │
│      Problem: Adding/removing nodes remaps almost ALL keys!    │
│                                                                 │
│   ✓ Option 2: Consistent Hashing                               │
│      Only ~1/N keys remapped when nodes change                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

For detailed explanation of consistent hashing, see [consistent-hashing.md](./consistent-hashing.md).

### Partitioning Strategy

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Hash Ring (2^128 space)                      │
│                                                                     │
│                              0°                                     │
│                              │                                      │
│                     A3 ●─────┴─────● B1                            │
│                       /             \                               │
│                      /               \                              │
│               A1 ●──                  ──● B2                       │
│                  │    Virtual Nodes     │                          │
│               C2 ●──                  ──● C1                       │
│                      \               /                              │
│                       \             /                               │
│                     A2 ●───────────● B3                            │
│                             │                                       │
│                            180°                                     │
│                                                                     │
│   Physical Nodes:  A (vnodes: A1,A2,A3)                            │
│                    B (vnodes: B1,B2,B3)                            │
│                    C (vnodes: C1,C2,C3)                            │
└─────────────────────────────────────────────────────────────────────┘
```

### Key-to-Node Mapping

To find which nodes store a key:

1. **Hash the key**: `hash("user:123")` → position on ring
2. **Walk clockwise**: Starting from that position
3. **Collect N distinct physical nodes**: Skip virtual nodes pointing to same server
4. **Return node list**: First node is coordinator, others are replicas

### Why Virtual Nodes?

| Benefit | Explanation |
|---------|-------------|
| **Load Balancing** | Keys distributed evenly across nodes |
| **Heterogeneous Hardware** | More vnodes for powerful servers |
| **Smoother Scaling** | Adding node redistributes many small ranges |
| **Faster Recovery** | Multiple nodes share recovery load |

---

## Replication

> **Interview context**: After discussing partitioning, the interviewer will likely ask: "What happens if a node storing data crashes? How do you prevent data loss?"

### Why Do We Need Replication?

Partitioning solves **scalability** - we can store more data by adding nodes. But it introduces a problem:

```
Without Replication:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Key "user:123" → hash → Node B                               │
│                                                                 │
│   If Node B crashes → "user:123" is LOST FOREVER!              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

With Replication (N=3):
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Key "user:123" → stored on [Node A, Node B, Node C]          │
│                                                                 │
│   If Node B crashes → still have copies on A and C!            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Replication gives us:
- **Durability**: Data survives node failures
- **Availability**: Can read from replicas if primary is down
- **Read scalability**: Distribute read load across replicas

### Replication Strategy

```
┌──────────────────────────────────────────────────────────────────┐
│                    Replication Model (N=3)                       │
│                                                                  │
│    Key "user:123" hashes to position P                          │
│                                                                  │
│                        Hash Ring                                 │
│                           │                                      │
│               ┌───────────┼───────────┐                         │
│               │           P           │                         │
│               │           ↓           │                         │
│               │      ● Node A ← Primary (Coordinator)           │
│               │           │           │                         │
│               │           │ replicate │                         │
│               │           ↓           │                         │
│               │      ● Node B ← Replica 1                       │
│               │           │           │                         │
│               │           │ replicate │                         │
│               │           ↓           │                         │
│               │      ● Node C ← Replica 2                       │
│               │                       │                         │
│               └───────────────────────┘                         │
│                                                                  │
│    Preference List: [A, B, C, D, E] (in ring order)             │
│    Active Replicas: First 3 healthy nodes from list             │
└──────────────────────────────────────────────────────────────────┘
```

### Quorum Configuration (NWR)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Quorum Parameters                           │
│                                                                 │
│   N = Total replicas (typically 3)                             │
│   W = Write quorum (nodes that must acknowledge write)         │
│   R = Read quorum (nodes that must respond to read)            │
│                                                                 │
│   Rule: W + R > N guarantees reading latest write              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Configuration Examples:                                       │
│                                                                 │
│   ┌─────────────┬─────┬─────┬─────┬───────────────────────┐    │
│   │ Config      │  N  │  W  │  R  │ Use Case              │    │
│   ├─────────────┼─────┼─────┼─────┼───────────────────────┤    │
│   │ Strong      │  3  │  3  │  1  │ Write-heavy, strong   │    │
│   │ Consistency │     │     │     │ consistency           │    │
│   ├─────────────┼─────┼─────┼─────┼───────────────────────┤    │
│   │ Balanced    │  3  │  2  │  2  │ Default, good balance │    │
│   ├─────────────┼─────┼─────┼─────┼───────────────────────┤    │
│   │ Fast Reads  │  3  │  2  │  1  │ Read-heavy workloads  │    │
│   ├─────────────┼─────┼─────┼─────┼───────────────────────┤    │
│   │ Eventual    │  3  │  1  │  1  │ Max availability      │    │
│   └─────────────┴─────┴─────┴─────┴───────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Synchronous vs Asynchronous Replication

```
Synchronous (W=N):
┌────────┐    write    ┌────────┐
│ Client │────────────▶│ Node A │──┐
└────────┘             └────────┘  │ wait for all
    ▲                              │ replicas
    │                  ┌────────┐  │
    │                  │ Node B │◀─┤
    │                  └────────┘  │
    │                              │
    │                  ┌────────┐  │
    │      ack         │ Node C │◀─┘
    └──────────────────┴────────┘

    Pros: Strong consistency
    Cons: Higher latency, lower availability

Asynchronous (W=1):
┌────────┐    write    ┌────────┐
│ Client │────────────▶│ Node A │──┐
└────────┘             └────────┘  │ async
    ▲                      │       │ replication
    │ ack (immediate)      │       │
    └──────────────────────┘       │
                                   │
                       ┌────────┐  │
                       │ Node B │◀─┤
                       └────────┘  │
                       ┌────────┐  │
                       │ Node C │◀─┘
                       └────────┘

    Pros: Low latency, high availability
    Cons: Potential data loss, eventual consistency
```

---

## Consistency Models

> **Interview context**: After discussing replication, a natural follow-up is: "With multiple replicas, how do you keep them in sync? What if two clients write to different replicas at the same time?"

### The Consistency Challenge

With replication, we introduced a new problem: **keeping replicas consistent**.

```
┌─────────────────────────────────────────────────────────────────┐
│                  The Consistency Problem                        │
│                                                                 │
│   Time T1: Client 1 writes x=1 to Node A                       │
│   Time T2: Client 2 writes x=2 to Node B (before A replicates) │
│   Time T3: Client 3 reads from Node C                          │
│                                                                 │
│   What value does Client 3 see?                                 │
│   - Could be x=1 (replicated from A)                           │
│   - Could be x=2 (replicated from B)                           │
│   - Could be nothing (neither replicated yet)                  │
│   - Could be BOTH (conflict!)                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

This leads to a fundamental trade-off in distributed systems: the **CAP Theorem**.

### CAP Theorem Trade-offs

```
┌─────────────────────────────────────────────────────────────────┐
│                       CAP Theorem                               │
│                                                                 │
│                    Consistency (C)                              │
│                         ▲                                       │
│                        /│\                                      │
│                       / │ \                                     │
│                      /  │  \                                    │
│                     /   │   \                                   │
│                    / CP │ CA \                                  │
│                   /     │     \                                 │
│                  /      │      \                                │
│                 ────────┼────────                               │
│           Availability  │   Partition                           │
│               (A)       │   Tolerance (P)                       │
│                    \ AP │                                       │
│                     \   │                                       │
│                      \  │                                       │
│                       \ │                                       │
│                        \│                                       │
│                                                                 │
│   Key-Value Stores typically choose AP (DynamoDB, Cassandra)   │
│   or CP (HBase, traditional RDBMS)                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Conflict Resolution

When W + R ≤ N, concurrent writes can create conflicts. Resolution strategies:

#### 1. Last-Write-Wins (LWW)

```
┌─────────────────────────────────────────────────────────────────┐
│                   Last-Write-Wins (LWW)                         │
│                                                                 │
│   Client A writes: key="x", value="A", timestamp=100           │
│   Client B writes: key="x", value="B", timestamp=101           │
│                                                                 │
│   On read: Return value with highest timestamp → "B"           │
│                                                                 │
│   Pros: Simple, deterministic                                   │
│   Cons: Silent data loss                                        │
└─────────────────────────────────────────────────────────────────┘
```

#### 2. Vector Clocks

```
┌─────────────────────────────────────────────────────────────────┐
│                      Vector Clocks                              │
│                                                                 │
│   Each write carries a vector: {NodeA: 2, NodeB: 1, NodeC: 3}  │
│                                                                 │
│   Concurrent Write Detection:                                   │
│                                                                 │
│   V1 = {A:1, B:0}   (Client 1 writes via Node A)               │
│   V2 = {A:0, B:1}   (Client 2 writes via Node B)               │
│                                                                 │
│   Neither dominates → CONFLICT DETECTED                         │
│                                                                 │
│   Resolution Options:                                           │
│   1. Return both values to client (application resolves)        │
│   2. Merge values (CRDTs)                                       │
│   3. Use semantic rules (shopping cart = union)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 3. CRDTs (Conflict-free Replicated Data Types)

```
┌─────────────────────────────────────────────────────────────────┐
│                          CRDTs                                  │
│                                                                 │
│   G-Counter (Grow-only Counter):                               │
│   ┌────────────────────────────────────────────────────────┐   │
│   │ Node A: {A: 5, B: 3, C: 2}  → Total: 10               │   │
│   │ Node B: {A: 4, B: 4, C: 2}  → Total: 10               │   │
│   │                                                        │   │
│   │ Merge: {A: max(5,4), B: max(3,4), C: max(2,2)}        │   │
│   │      = {A: 5, B: 4, C: 2}   → Total: 11               │   │
│   └────────────────────────────────────────────────────────┘   │
│                                                                 │
│   Types: G-Counter, PN-Counter, G-Set, OR-Set, LWW-Register   │
│   Used by: Riak, Redis CRDT, Cassandra counters               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Handling Failures

> **Interview Tip**: When discussing failures, start by identifying what can go wrong, then systematically address each scenario. This shows structured thinking.

### The Problem: What Can Go Wrong?

In a distributed system, failures are inevitable. Let's think about what can fail:

```
┌─────────────────────────────────────────────────────────────────┐
│                    What Can Fail?                               │
│                                                                 │
│   1. NETWORK ISSUES                                            │
│      - Packet loss, network partition                          │
│      - Node appears dead but is actually alive                 │
│                                                                 │
│   2. NODE FAILURES                                             │
│      - Process crash (temporary - will restart)                │
│      - Server reboot (temporary - minutes)                     │
│      - Hardware failure (permanent - disk dead)                │
│                                                                 │
│   3. DATA CENTER FAILURES                                      │
│      - Power outage, natural disaster                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

This raises several questions we need to answer:

| Question | Why It Matters |
|----------|----------------|
| **How do we know a node failed?** | Can't fix what we can't detect |
| **Is it temporary or permanent?** | Different strategies needed |
| **How do writes succeed during failure?** | Maintain availability |
| **How do we recover lost replicas?** | Maintain durability |

Let's address each question systematically.

---

### 7.1 Failure Detection: Gossip Protocol

> **First question: How do we know a node has failed?**

In a distributed system, we can't rely on a single "master" to track health - that would be a single point of failure. Instead, we use a **decentralized approach** where nodes monitor each other.

#### Why Not Just Use Heartbeats to a Central Server?

```
❌ Centralized Health Check (Single Point of Failure):

     ┌────────────┐
     │  Monitor   │ ← If this dies, no failure detection!
     └─────┬──────┘
           │
    ┌──────┼──────┬──────┐
    ▼      ▼      ▼      ▼
   [A]    [B]    [C]    [D]


✓ Decentralized Gossip (No Single Point of Failure):

   [A] ←──→ [B]
    ↑  ╲  ╱  ↑
    │   ╲╱   │      Everyone monitors everyone
    │   ╱╲   │      through random peer exchange
    ↓  ╱  ╲  ↓
   [D] ←──→ [C]
```

#### How Gossip Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    Gossip Protocol                              │
│                                                                 │
│   Every T seconds (typically 1s), each node:                    │
│   1. Picks random peer                                          │
│   2. Exchanges membership list with heartbeat counters          │
│   3. Merges lists (keep highest heartbeat per node)            │
│                                                                 │
│   ┌──────┐ gossip  ┌──────┐                                    │
│   │Node A│────────▶│Node B│                                    │
│   └──────┘         └──────┘                                    │
│       │                │                                        │
│       │  {A:10,B:5,   {A:9,B:6,                                │
│       │   C:7,D:3}     C:7,D:4}                                │
│       │                │                                        │
│       │    Merged:     │                                        │
│       │  {A:10,B:6,C:7,D:4}                                    │
│       │                │                                        │
│                                                                 │
│   Node marked DOWN if heartbeat unchanged for T_fail seconds   │
└─────────────────────────────────────────────────────────────────┘
```

#### Failure State Transitions

```
┌─────────────────────────────────────────────────────────────────┐
│                 Node State Machine                              │
│                                                                 │
│   HEALTHY ──────────────────────────────────────────────────   │
│      │                                                          │
│      │ Missed heartbeats (T > 5s)                              │
│      ▼                                                          │
│   SUSPICIOUS ───────────────────────────────────────────────   │
│      │                                                          │
│      │ No recovery (T > 30s)                                   │
│      ▼                                                          │
│   DOWN (Temporary) ─────────────────────────────────────────   │
│      │         │                                                │
│      │         │ Node recovers → back to HEALTHY               │
│      │         │                                                │
│      │ No recovery (T > 10min)                                 │
│      ▼                                                          │
│   PERMANENTLY FAILED ───────────────────────────────────────   │
│      │                                                          │
│      │ Admin removes or system auto-removes                    │
│      ▼                                                          │
│   REMOVED (from ring)                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Timeline:
─────────────────────────────────────────────────────────────────
T=0      Node D stops responding
T=5s     Marked SUSPICIOUS (missed heartbeats)
T=30s    Marked DOWN (hinted handoff activates)
T=10min  Marked PERMANENTLY FAILED (re-replication triggers)
```

---

### 7.2 Temporary Failures: Hinted Handoff

> **Second question: How do writes succeed when a node is temporarily down?**

Now that we can detect failures, what happens when a write request comes in but one of the target nodes is down?

#### The Challenge

```
┌─────────────────────────────────────────────────────────────────┐
│                     The Problem                                 │
│                                                                 │
│   Scenario: Client wants to write key "user:123"               │
│   Target nodes: [A, B, C]  (N=3 replicas)                      │
│   But Node B is temporarily DOWN (restarting)                  │
│                                                                 │
│   Options:                                                      │
│   ❌ Option 1: Fail the write                                  │
│      → Bad UX, reduces availability                            │
│                                                                 │
│   ❌ Option 2: Write to only A and C (skip B)                  │
│      → Data lost if B never gets the update                    │
│                                                                 │
│   ✓ Option 3: Write to A, C, and temporarily store for B      │
│      → This is Hinted Handoff!                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### The Solution: Hinted Handoff

The key idea is simple: **when a target node is down, write to another node with a "hint" to forward the data when the target recovers**.

#### Normal Write Path (All Nodes Healthy)

```
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│ Client │────▶│ Node A │────▶│ Node B │────▶│ Node C │
└────────┘     └────────┘     └────────┘     └────────┘
                  │               │               │
                  └───────────────┴───────────────┘
                           All 3 receive data
                           W=2 satisfied
```

#### Write Path with Node B Down

```
┌─────────────────────────────────────────────────────────────────┐
│              Hinted Handoff in Action                           │
│                                                                 │
│   Step 1: Coordinator detects Node B is DOWN                   │
│                                                                 │
│   ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐     │
│   │ Client │────▶│ Node A │──X──│ Node B │     │ Node C │     │
│   └────────┘     └────────┘     │ (DOWN) │     └────────┘     │
│                      │          └────────┘          ▲          │
│                      │                              │          │
│                      └──────────────────────────────┘          │
│                            Write to C instead                  │
│                                                                 │
│   Step 2: Write to Node D with hint for B                      │
│                                                                 │
│                      │                                          │
│                      ▼                                          │
│                 ┌────────┐                                      │
│                 │ Node D │ ← Stores: {                         │
│                 │        │     key: "user:123",                │
│                 │        │     value: "data...",               │
│                 │        │     hint_for: "Node B",             │
│                 │        │     timestamp: 1706123456           │
│                 │        │   }                                  │
│                 └────────┘                                      │
│                                                                 │
│   Step 3: W=2 satisfied (A + C or A + D), return success       │
│                                                                 │
│   Step 4: When B recovers (detected via gossip)                │
│                                                                 │
│                 ┌────────┐         ┌────────┐                  │
│                 │ Node D │────────▶│ Node B │                  │
│                 │        │ handoff │(recovered)│                │
│                 └────────┘         └────────┘                  │
│                      │                  │                       │
│                      │   ACK received   │                       │
│                      │◀─────────────────│                       │
│                      │                                          │
│                      ▼                                          │
│                 Delete local hint                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Sloppy Quorum

Hinted handoff enables a **sloppy quorum** - writes succeed using *any* W healthy nodes:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Quorum Comparison                            │
│                                                                 │
│   STRICT QUORUM (Traditional):                                 │
│   ─────────────────────────────                                │
│   Preference list: [A, B, C]                                   │
│   Must write to 2 of [A, B, C] only                           │
│   If B is down → WRITE FAILS (only A, C available = 2, ok)    │
│   If B and C down → WRITE FAILS (only A available = 1)        │
│                                                                 │
│   SLOPPY QUORUM (With Hinted Handoff):                         │
│   ────────────────────────────────────                         │
│   Preference list: [A, B, C, D, E, ...]                        │
│   Must write to any 2 healthy nodes                            │
│   If B is down → write to A + C (or A + D with hint)          │
│   If B and C down → write to A + D + E (hints for B, C)       │
│                                                                 │
│   Result: Higher write availability                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### How It Works

1. **Write attempt**: Target node A is down
2. **Select hint holder**: Next healthy node on ring (D)
3. **Store hint**: D stores the data + metadata about intended target (A)
4. **Wait for recovery**: Gossip detects A is back
5. **Deliver hint**: D sends stored data to A
6. **Delete hint**: Once delivered, hint is removed

#### Trade-offs

| Pros | Cons |
|------|------|
| Higher write availability | Temporary inconsistency |
| Client doesn't see failures | Storage overhead on hint nodes |
| Automatic recovery | Hints can pile up for long outages |
| No data loss for temp failures | Read-your-write not guaranteed |

---

### 7.3 Permanent Failures: Re-replication

> **Third question: What if a node never comes back?**

Hinted handoff works great for temporary failures. But what if the node's disk crashed and it's never coming back? Hints will pile up forever, and more importantly, **we've lost a replica**.

#### The Challenge

```
┌─────────────────────────────────────────────────────────────────┐
│                     The Problem                                 │
│                                                                 │
│   Scenario: Node B's disk crashes (permanent failure)          │
│                                                                 │
│   Before failure:                                               │
│   Key "x" stored on: [A, B, C]  → 3 copies (safe)              │
│                                                                 │
│   After failure (with only hinted handoff):                    │
│   Key "x" stored on: [A, C] + hint on D → only 2 real copies!  │
│                                                                 │
│   Risk: If A or C also fails → DATA LOSS!                      │
│                                                                 │
│   We need to CREATE A NEW REPLICA to restore N=3               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### But How Do We Know It's Permanent?

Good question! We can't know for certain, so we use a **time threshold**:
- If a node is down for > 10 minutes → assume permanent
- Trigger re-replication to be safe
- If the node comes back later, we just have extra copies (harmless)

#### Why Re-replication is Necessary

```
┌─────────────────────────────────────────────────────────────────┐
│                Why Hinted Handoff Isn't Enough                  │
│                                                                 │
│   Scenario: Node B permanently fails (disk crash)              │
│                                                                 │
│   With only hinted handoff:                                     │
│   - Hints pile up on other nodes                               │
│   - B never comes back to receive them                         │
│   - Data only exists on 2 nodes (A, C) instead of 3           │
│   - If another node fails, DATA LOSS!                          │
│                                                                 │
│   Before B failed:        After B failed (no re-replication):  │
│   Key "x" on [A,B,C]      Key "x" on [A,C] only               │
│   3 copies = safe         2 copies = VULNERABLE               │
│                                                                 │
│   Solution: Detect permanent failure → create new replica      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Re-replication Process

```
┌─────────────────────────────────────────────────────────────────┐
│              Permanent Failure Recovery Flow                    │
│                                                                 │
│   BEFORE (Node B fails permanently):                           │
│                                                                 │
│   Hash Ring:              Data Distribution (N=3):              │
│        ● A                Key "x" → [A, B, C]                  │
│       / │                 Key "y" → [B, C, D]                  │
│      /  │                 Key "z" → [C, D, A]                  │
│     ●   │                                                       │
│     D   │                 Node B owned:                         │
│      \  │                 - Primary: keys in range (A, B]      │
│       \ │                 - Replica: keys from A and D         │
│        ● B ← PERMANENTLY FAILED                                │
│         \                                                       │
│          ● C                                                    │
│                                                                 │
│   AFTER (Re-replication complete):                             │
│                                                                 │
│   Hash Ring:              Data Distribution (N=3):              │
│        ● A                Key "x" → [A, C, D] ← D replaces B   │
│       /│ \                Key "y" → [C, D, E] ← E replaces B   │
│      / │  ● E (new)       Key "z" → [C, D, A]   (unchanged)    │
│     ●  │                                                        │
│     D  │                  Actions taken:                        │
│      \ │                  1. Remove B from ring                 │
│       \│                  2. Identify under-replicated keys     │
│        ● C                3. Stream data to new replicas        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Step-by-Step Recovery

```
┌────────────────────────────────────────────────────────────────┐
│              Permanent Failure Recovery Steps                  │
│                                                                │
│  1. DETECTION (via Gossip)                                     │
│     └─▶ Node B heartbeat unchanged for >10 minutes            │
│     └─▶ Marked as PERMANENTLY_FAILED                          │
│                                                                │
│  2. RING UPDATE                                                │
│     └─▶ Remove B's virtual nodes from hash ring               │
│     └─▶ B's key ranges now map to next nodes clockwise        │
│     └─▶ Broadcast new ring to all nodes                       │
│                                                                │
│  3. IDENTIFY UNDER-REPLICATED DATA                             │
│     └─▶ For each key range B owned:                           │
│         - Find keys that now have only 2 replicas             │
│         - Add to re-replication queue                         │
│                                                                │
│  4. SELECT NEW REPLICA NODES                                   │
│     └─▶ For each under-replicated key range:                  │
│         - Walk clockwise on ring from key position            │
│         - Pick next node NOT already holding that data        │
│                                                                │
│  5. STREAM DATA (Anti-Entropy)                                 │
│     └─▶ Existing replicas send data to new nodes              │
│     └─▶ Use Merkle trees for efficient diff                   │
│     └─▶ Throttle to prevent network saturation                │
│                                                                │
│  6. VERIFY & COMPLETE                                          │
│     └─▶ New replicas acknowledge receipt                      │
│     └─▶ Replication factor N=3 restored                       │
│     └─▶ Mark recovery complete                                │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

#### But Wait - How Do We Efficiently Sync Data?

> **Follow-up question an interviewer might ask**: "Re-replicating data sounds expensive. Do you copy ALL the data?"

Great question! If Node B had 100GB of data, we don't want to blindly copy everything. We need to find **only the missing keys**. But checking every key is O(N) - too slow!

**Solution: Merkle Trees** - a data structure that lets us find differences in O(log N).

#### Anti-Entropy with Merkle Trees

Merkle Trees let us efficiently find which keys differ between two nodes:

```
┌─────────────────────────────────────────────────────────────────┐
│                  Merkle Trees for Sync                          │
│                                                                 │
│   Problem: Node E needs B's data. Which keys exactly?           │
│            Scanning all keys is O(N) - too slow!               │
│                                                                 │
│   Solution: Compare hash trees to find differences O(log N)    │
│                                                                 │
│        Node C (has data)              Node E (needs data)       │
│                                                                 │
│            H(root)="abc"                 H(root)="xyz"          │
│           /            \                /            \          │
│       H(L)="def"    H(R)="ghi"     H(L)="def"    H(R)="000"    │
│       /     \       /     \        /     \       /     \       │
│     H1      H2    H3      H4     H1      H2    H3      H4      │
│     ✓       ✓     ✗       ✓      ✓       ✓     ✗       ✓       │
│                   │                            │                │
│                   └────── Different! ──────────┘                │
│                                                                 │
│   Sync Process:                                                 │
│   1. Compare root hashes: "abc" ≠ "xyz" → different            │
│   2. Compare children: H(L) same, H(R) different               │
│   3. Recurse into H(R): H3 different, H4 same                  │
│   4. Only sync keys in H3's range (25% of data)                │
│                                                                 │
│   Complexity: O(log N) comparisons to find differences          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Merkle Tree Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    Merkle Tree Example                          │
│                                                                 │
│                        Root Hash                                │
│                     H("abc"+"def")                              │
│                      ┌────┴────┐                                │
│                      │ H(root) │                                │
│                      └────┬────┘                                │
│               ┌───────────┴───────────┐                         │
│          ┌────┴────┐             ┌────┴────┐                   │
│          │ H("abc")│             │ H("def")│                   │
│          └────┬────┘             └────┬────┘                   │
│         ┌─────┴─────┐           ┌─────┴─────┐                  │
│    ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐            │
│    │keys 0-25│ │keys26-50│ │keys51-75│ │keys76-99│            │
│    │ H(data) │ │ H(data) │ │ H(data) │ │ H(data) │            │
│    └─────────┘ └─────────┘ └─────────┘ └─────────┘            │
│                                                                 │
│   Each leaf = hash of all keys in that range                   │
│   Each parent = hash of children's hashes                      │
│   Any change in data → changes propagate to root               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Recovery Process

1. **Detect failure**: Gossip protocol marks node as permanently failed (down >10 min)
2. **Update ring**: Remove failed node from membership
3. **Find affected ranges**: Identify key ranges with < N replicas
4. **Select new replica**: Next healthy node in ring not already holding data
5. **Sync using Merkle tree**: Compare tree hashes to find differences
6. **Transfer only diffs**: Stream only the differing keys (efficient!)

> **Interviewer might ask**: "Why use Merkle trees?"
>
> Merkle trees allow O(log N) comparison of datasets. Compare root hashes—if equal, data is identical. If different, recurse into children to find exactly which ranges differ. Much more efficient than comparing key-by-key.

---

### 7.4 Read Repair

> **Fourth question: What about replicas that get out of sync over time?**

Even without failures, replicas can become inconsistent:
- A write succeeded on 2 of 3 nodes (W=2), third node was slow
- Network issues caused a partial update
- A node was down briefly and missed some writes

Rather than running expensive background sync constantly, we can fix inconsistencies **opportunistically during reads**. This is called **Read Repair**.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Read Repair                                │
│                                                                 │
│   During read with R=2, N=3:                                    │
│                                                                 │
│   ┌────────┐     GET key="x"                                   │
│   │ Client │──────────────────┐                                │
│   └────────┘                  │                                │
│       ▲                       ▼                                │
│       │               ┌──────────────┐                         │
│       │               │ Coordinator  │                         │
│       │               └──────┬───────┘                         │
│       │                      │                                  │
│       │         ┌────────────┼────────────┐                    │
│       │         ▼            ▼            ▼                    │
│       │    ┌────────┐   ┌────────┐   ┌────────┐               │
│       │    │ Node A │   │ Node B │   │ Node C │               │
│       │    │ v=1    │   │ v=2    │   │ v=2    │               │
│       │    └────┬───┘   └────┬───┘   └────────┘               │
│       │         │            │                                  │
│       │         │ return     │ return                          │
│       │         │ (v=1)      │ (v=2)                           │
│       │         │            │                                  │
│       │         └────────────┘                                  │
│       │                │                                        │
│       │    Coordinator detects v=1 < v=2                       │
│       │    1. Return v=2 to client                             │
│       │    2. Async send v=2 to Node A (repair)                │
│       │                                                         │
│       └─────── value = 2                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 7.5 Comparison: Temporary vs Permanent Failures

> **Summary: How do all these mechanisms work together?**

Let's summarize the complete failure handling strategy:

```
┌─────────────────────────────────────────────────────────────────┐
│              Complete Failure Handling Flow                     │
│                                                                 │
│   Node stops responding                                         │
│           │                                                     │
│           ▼                                                     │
│   ┌───────────────────┐                                        │
│   │ Gossip detects    │                                        │
│   │ missed heartbeats │                                        │
│   └─────────┬─────────┘                                        │
│             │                                                   │
│             ▼                                                   │
│   ┌───────────────────┐     ┌────────────────────────────┐    │
│   │ Mark as DOWN      │────▶│ Hinted Handoff activates   │    │
│   │ (after 30s)       │     │ Writes go to backup nodes  │    │
│   └─────────┬─────────┘     └────────────────────────────┘    │
│             │                                                   │
│             │ Node still down after 10+ minutes?               │
│             │                                                   │
│     ┌───────┴───────┐                                          │
│     │               │                                          │
│     ▼               ▼                                          │
│   Node          Node stays                                     │
│   recovers      down                                           │
│     │               │                                          │
│     ▼               ▼                                          │
│   ┌─────────┐   ┌─────────────────────────────────────┐       │
│   │ Hints   │   │ Mark PERMANENTLY FAILED             │       │
│   │ replayed│   │ Remove from ring                    │       │
│   │ to node │   │ Trigger re-replication              │       │
│   └─────────┘   │ Use Merkle trees to sync efficiently│       │
│                 └─────────────────────────────────────┘       │
│                                                                 │
│   Meanwhile: Read Repair fixes any stale data opportunistically│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| Aspect | Temporary Failure | Permanent Failure |
|--------|-------------------|-------------------|
| **Detection time** | 30 seconds | 10+ minutes |
| **Mechanism** | Hinted Handoff | Re-replication |
| **Data location** | Hints on other nodes | New full replicas |
| **Ring change** | No | Yes, node removed |
| **Network cost** | Low (hints only) | High (full data streaming) |
| **Recovery** | Automatic on return | Manual or auto add node |
| **Data risk** | Low (hints preserved) | Medium (fewer replicas) |

### 7.6 Configuration Parameters

```
┌─────────────────────────────────────────────────────────────────┐
│                Failure Handling Configuration                   │
│                                                                 │
│   Parameter                    │ Typical Value │ Description    │
│   ────────────────────────────┼───────────────┼────────────────│
│   gossip_interval             │ 1 second      │ Heartbeat freq │
│   suspicion_threshold         │ 5 seconds     │ Mark suspicious│
│   down_threshold              │ 30 seconds    │ Mark DOWN      │
│   permanent_failure_threshold │ 10 minutes    │ Trigger re-rep │
│   hint_ttl                    │ 3 hours       │ Max hint age   │
│   max_hints_per_node          │ 10 GB         │ Hint storage   │
│   streaming_throughput        │ 50 MB/s       │ Re-rep speed   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.7 Real-World Implementations

| System | Temporary Failure | Permanent Failure |
|--------|-------------------|-------------------|
| **Cassandra** | Hinted handoff (3h default) | `nodetool removenode` + streaming |
| **DynamoDB** | Sloppy quorum + hints | Managed by AWS automatically |
| **Riak** | Hinted handoff | Automatic with Merkle trees |
| **etcd** | Raft leader election | Membership reconfiguration |

---

## Storage Engine

> **Interview context**: The interviewer might ask: "How does each node actually store data on disk? How do you optimize for both reads and writes?"

### The Storage Challenge

Key-value stores need to handle:
- **Fast writes**: Users expect low latency
- **Efficient reads**: Quick lookups by key
- **Durability**: Data must survive crashes

Traditional B-trees are optimized for reads but writes are slow (random I/O). For write-heavy workloads, we use a different approach.

### LSM Tree (Log-Structured Merge Tree)

Most distributed KV stores use **LSM trees** because they convert random writes into sequential writes, which are much faster.

```
┌─────────────────────────────────────────────────────────────────┐
│                     LSM Tree Architecture                       │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Write Path                            │  │
│   │                                                          │  │
│   │   Write ──▶ WAL (Write-Ahead Log) ──▶ MemTable          │  │
│   │              (Durability)             (In-Memory)        │  │
│   │                                           │              │  │
│   │                                    When full             │  │
│   │                                           │              │  │
│   │                                           ▼              │  │
│   │                                    Flush to SSTable      │  │
│   │                                      (Level 0)           │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Storage Levels                        │  │
│   │                                                          │  │
│   │   MemTable:     [ k1:v1, k3:v3, k5:v5 ]  (sorted)       │  │
│   │                            │                             │  │
│   │                            ▼                             │  │
│   │   Level 0:    ┌─────────┐ ┌─────────┐ ┌─────────┐       │  │
│   │               │SSTable 1│ │SSTable 2│ │SSTable 3│       │  │
│   │               └─────────┘ └─────────┘ └─────────┘       │  │
│   │                            │ compact                     │  │
│   │                            ▼                             │  │
│   │   Level 1:    ┌───────────────────────────────────┐     │  │
│   │               │     SSTable (sorted, no overlap)  │     │  │
│   │               └───────────────────────────────────┘     │  │
│   │                            │ compact                     │  │
│   │                            ▼                             │  │
│   │   Level 2:    ┌───────────────────────────────────────┐ │  │
│   │               │   SSTable (10x larger, no overlap)    │ │  │
│   │               └───────────────────────────────────────┘ │  │
│   │                            │                             │  │
│   │                            ▼                             │  │
│   │   Level N:    (exponentially larger)                    │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Read Path with Bloom Filters

```
┌─────────────────────────────────────────────────────────────────┐
│                        Read Path                                │
│                                                                 │
│   GET(key) ─┬──▶ Check MemTable ──────────┬──▶ Found? Return   │
│             │         │                    │                    │
│             │         │ Not found          │                    │
│             │         ▼                    │                    │
│             │    Check Bloom Filter        │                    │
│             │    for each SSTable          │                    │
│             │         │                    │                    │
│             │    ┌────┴────┐               │                    │
│             │    │         │               │                    │
│             │    ▼         ▼               │                    │
│             │  "Maybe"   "No"              │                    │
│             │    │         │               │                    │
│             │    │         │ Skip          │                    │
│             │    ▼         │               │                    │
│             │  Binary     │               │                    │
│             │  Search     │               │                    │
│             │  SSTable    │               │                    │
│             │    │         │               │                    │
│             │    └─────────┴───────────────┘                    │
│                                                                 │
│   Bloom Filter: Space-efficient probabilistic data structure    │
│   - "Definitely not in set" or "Maybe in set"                  │
│   - False positive rate ~1% with 10 bits per element           │
│   - Saves disk reads for keys that don't exist                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### SSTable Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    SSTable File Format                          │
│                                                                 │
│   ┌──────────────────────────────────────────────────────────┐ │
│   │                    Data Blocks                           │ │
│   │  ┌─────────┐┌─────────┐┌─────────┐┌─────────┐           │ │
│   │  │Block 0  ││Block 1  ││Block 2  ││Block N  │           │ │
│   │  │k1:v1    ││k50:v50  ││k100:v100││...      │           │ │
│   │  │k2:v2    ││k51:v51  ││k101:v101││         │           │ │
│   │  │...      ││...      ││...      ││         │           │ │
│   │  └─────────┘└─────────┘└─────────┘└─────────┘           │ │
│   └──────────────────────────────────────────────────────────┘ │
│   ┌──────────────────────────────────────────────────────────┐ │
│   │                    Index Block                           │ │
│   │  Block 0: first_key=k1,  offset=0                       │ │
│   │  Block 1: first_key=k50, offset=4096                    │ │
│   │  Block 2: first_key=k100, offset=8192                   │ │
│   └──────────────────────────────────────────────────────────┘ │
│   ┌──────────────────────────────────────────────────────────┐ │
│   │                    Bloom Filter                          │ │
│   └──────────────────────────────────────────────────────────┘ │
│   ┌──────────────────────────────────────────────────────────┐ │
│   │                    Footer/Metadata                       │ │
│   │  - Index offset                                          │ │
│   │  - Bloom filter offset                                   │ │
│   │  - Compression type                                      │ │
│   │  - Checksum                                              │ │
│   └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## System Architecture Diagram

### Complete System View

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           Distributed Key-Value Store                               │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                              Client SDK                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │   │
│  │  │ Routing     │  │ Retry       │  │ Load        │  │ Connection          │ │   │
│  │  │ (Ring Copy) │  │ Logic       │  │ Balancing   │  │ Pooling             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────┘ │   │
│  └───────────────────────────────────┬─────────────────────────────────────────┘   │
│                                      │                                              │
│  ═══════════════════════════════════════════════════════════════════════════════   │
│                                      │                                              │
│  ┌───────────────────────────────────▼─────────────────────────────────────────┐   │
│  │                            Coordinator Layer                                 │   │
│  │                                                                              │   │
│  │    ┌──────────────────────────────────────────────────────────────────┐     │   │
│  │    │  Request Flow:                                                    │     │   │
│  │    │  1. Parse request                                                │     │   │
│  │    │  2. Hash key → find nodes                                        │     │   │
│  │    │  3. Forward to replicas                                          │     │   │
│  │    │  4. Wait for quorum (W or R)                                     │     │   │
│  │    │  5. Return response (or conflict)                                │     │   │
│  │    └──────────────────────────────────────────────────────────────────┘     │   │
│  │                                                                              │   │
│  └───────────────────────────────────┬─────────────────────────────────────────┘   │
│                                      │                                              │
│  ┌───────────────────────────────────▼─────────────────────────────────────────┐   │
│  │                              Storage Nodes                                   │   │
│  │                                                                              │   │
│  │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │   │
│  │   │     Node A      │  │     Node B      │  │     Node C      │             │   │
│  │   │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │             │   │
│  │   │  │ MemTable  │  │  │  │ MemTable  │  │  │  │ MemTable  │  │             │   │
│  │   │  └─────┬─────┘  │  │  └─────┬─────┘  │  │  └─────┬─────┘  │             │   │
│  │   │  ┌─────▼─────┐  │  │  ┌─────▼─────┐  │  │  ┌─────▼─────┐  │             │   │
│  │   │  │  SSTable  │  │  │  │  SSTable  │  │  │  │  SSTable  │  │             │   │
│  │   │  │   L0-L6   │  │  │  │   L0-L6   │  │  │  │   L0-L6   │  │             │   │
│  │   │  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │             │   │
│  │   │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │             │   │
│  │   │  │    WAL    │  │  │  │    WAL    │  │  │  │    WAL    │  │             │   │
│  │   │  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │             │   │
│  │   └─────────────────┘  └─────────────────┘  └─────────────────┘             │   │
│  │           │                     │                     │                      │   │
│  │           └─────────────────────┼─────────────────────┘                      │   │
│  │                                 │                                            │   │
│  │                    ┌────────────▼────────────┐                               │   │
│  │                    │    Replication &        │                               │   │
│  │                    │    Anti-Entropy         │                               │   │
│  │                    └─────────────────────────┘                               │   │
│  │                                                                              │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │                           Control Plane                                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │   │
│  │  │   Gossip     │  │   Failure    │  │   Ring       │  │   Monitoring     │  │   │
│  │  │   Protocol   │  │   Detector   │  │   Manager    │  │   & Metrics      │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Write Flow Sequence

```
┌────────┐       ┌─────────────┐       ┌────────┐       ┌────────┐       ┌────────┐
│ Client │       │ Coordinator │       │ Node A │       │ Node B │       │ Node C │
└───┬────┘       └──────┬──────┘       └───┬────┘       └───┬────┘       └───┬────┘
    │                   │                  │                │                │
    │  PUT(k,v)         │                  │                │                │
    │──────────────────▶│                  │                │                │
    │                   │                  │                │                │
    │                   │ hash(k)→[A,B,C]  │                │                │
    │                   │                  │                │                │
    │                   │  write(k,v)      │                │                │
    │                   │─────────────────▶│                │                │
    │                   │                  │                │                │
    │                   │  write(k,v)      │                │                │
    │                   │─────────────────────────────────▶│                │
    │                   │                  │                │                │
    │                   │  write(k,v)      │                │                │
    │                   │────────────────────────────────────────────────▶│
    │                   │                  │                │                │
    │                   │         ACK      │                │                │
    │                   │◀─────────────────│                │                │
    │                   │                  │                │                │
    │                   │         ACK (W=2 reached)         │                │
    │                   │◀─────────────────────────────────│                │
    │                   │                  │                │                │
    │   SUCCESS         │                  │                │                │
    │◀──────────────────│                  │                │                │
    │                   │                  │                │                │
    │                   │         ACK (async, W already met)                 │
    │                   │◀────────────────────────────────────────────────│
    │                   │                  │                │                │
```

---

## Trade-offs and Design Decisions

### Key Design Decisions

| Decision | Options | Trade-off |
|----------|---------|-----------|
| **Partitioning** | Hash vs Range | Hash: even distribution. Range: range queries |
| **Replication** | Sync vs Async | Sync: consistency. Async: availability |
| **Consistency** | Strong vs Eventual | Strong: correctness. Eventual: performance |
| **Storage** | LSM vs B-Tree | LSM: writes. B-Tree: reads |
| **Conflict Resolution** | LWW vs Vector Clock | LWW: simple. VC: accurate |

### When to Choose What

```
┌─────────────────────────────────────────────────────────────────┐
│                    Decision Matrix                              │
│                                                                 │
│   Use Case                      │ Recommended Configuration     │
│   ─────────────────────────────┼──────────────────────────────│
│   Financial transactions       │ Strong consistency (W=R=N)    │
│   Session storage              │ Eventual (W=1, R=1)           │
│   User profiles                │ Balanced (W=2, R=2, N=3)      │
│   Analytics/metrics            │ Fast writes (W=1, R=N)        │
│   Shopping cart                │ CRDTs for merge               │
│   Leaderboards                 │ LWW for simplicity            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Consistency vs Latency Trade-off

```
                    Latency
                      ▲
                      │
                      │     ● W=1, R=1
                      │        (Eventual)
                      │
                      │
                      │        ● W=2, R=2
                      │           (Balanced)
                      │
                      │              ● W=3, R=3
                      │                 (Strong)
                      │
                      └──────────────────────────▶ Consistency
```

---

## Real-World Examples

| System | Company | Key Features |
|--------|---------|--------------|
| **DynamoDB** | Amazon | Fully managed, auto-scaling, single-digit ms latency |
| **Cassandra** | Apache | Wide-column, tunable consistency, multi-DC |
| **Redis** | Redis Labs | In-memory, data structures, Cluster mode |
| **Riak** | Basho | Masterless, CRDTs, high availability |
| **etcd** | CNCF | Strong consistency (Raft), Kubernetes config |
| **RocksDB** | Facebook | Embedded, LSM-based, used in many systems |
| **TiKV** | PingCAP | Distributed, Raft-based, ACID transactions |

### Feature Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                    Feature Comparison                           │
│                                                                 │
│              │ DynamoDB │ Cassandra │ Redis │ etcd │           │
│   ───────────┼──────────┼───────────┼───────┼──────┤           │
│   Consistency│ Eventual/│ Tunable   │ Event.│Strong│           │
│              │ Strong   │           │       │      │           │
│   ───────────┼──────────┼───────────┼───────┼──────┤           │
│   Partitions │ Auto     │ Consistent│ Hash  │ Raft │           │
│              │          │ Hash      │ Slots │      │           │
│   ───────────┼──────────┼───────────┼───────┼──────┤           │
│   Replication│ Multi-AZ │ Multi-DC  │ Async │ Raft │           │
│   ───────────┼──────────┼───────────┼───────┼──────┤           │
│   Storage    │ B-Tree   │ LSM       │Memory │ BoltDB│          │
│   ───────────┼──────────┼───────────┼───────┼──────┤           │
│   Use Case   │ General  │ Time-     │ Cache │Config│           │
│              │          │ series    │       │      │           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Interview Tips

### How to Approach the Problem

The key is to **show your thought process**. Don't just list solutions - identify problems first, then solve them.

```
┌─────────────────────────────────────────────────────────────────┐
│           Interview Flow (45 minutes)                           │
│                                                                 │
│   1. CLARIFY REQUIREMENTS (3-5 min)                            │
│      "Before I dive in, let me make sure I understand..."      │
│      □ Scale: How many keys? QPS? Data size?                   │
│      □ Consistency: Strong or eventual?                        │
│      □ Latency: p99 requirements?                              │
│      □ Availability: 99.9%? 99.99%?                            │
│      □ Features: TTL? Range queries? Transactions?             │
│                                                                 │
│   2. HIGH-LEVEL DESIGN (5-7 min)                               │
│      "Let me start with the basic architecture..."             │
│      □ API design (get, put, delete)                           │
│      □ Single server first, then identify bottlenecks          │
│      □ Add partitioning for scale                              │
│      □ Add replication for durability                          │
│      □ Draw architecture diagram                                │
│                                                                 │
│   3. DEEP DIVE - Show Problem → Solution Flow (20-25 min)      │
│                                                                 │
│      "Now that we have multiple nodes, how do we distribute    │
│       data? Simple modulo hash won't work because..."          │
│      → Consistent hashing                                       │
│                                                                 │
│      "What if a node crashes? We'd lose data..."               │
│      → Replication                                              │
│                                                                 │
│      "With multiple replicas, how do we keep them in sync?"    │
│      → Quorum (NWR), consistency models                        │
│                                                                 │
│      "What happens when a node temporarily fails?"             │
│      → Hinted handoff                                           │
│                                                                 │
│      "What if it never comes back?"                            │
│      → Re-replication with Merkle trees                        │
│                                                                 │
│   4. TRADE-OFFS (3-5 min)                                      │
│      "There are trade-offs to discuss..."                      │
│      □ CAP theorem: We chose AP, here's why...                 │
│      □ Consistency vs latency                                   │
│      □ Memory vs disk                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Phrases That Show Structured Thinking

| Instead of... | Say... |
|---------------|--------|
| "We use consistent hashing" | "Simple modulo hashing has a problem: if we add a node, almost all keys move. To solve this, we use consistent hashing which only moves 1/N keys." |
| "We replicate data" | "Partitioning alone is risky - if a node fails, we lose that data. So we replicate each key to N nodes for durability." |
| "We use hinted handoff" | "When a node is temporarily down, we have a choice: fail the write or buffer it somewhere. Hinted handoff lets us buffer on another node and deliver later." |

### Common Follow-up Questions

| Question | Key Points |
|----------|-----------|
| "How do you handle hotkeys?" | Caching, add salt to key, replicate reads |
| "How do you support range queries?" | Use range partitioning instead of hash |
| "How do you handle large values?" | Chunk values, store in blob storage |
| "How do you support transactions?" | 2PC, Paxos/Raft, or don't support |
| "How do you handle datacenter failure?" | Multi-DC replication, async with conflict resolution |

### Key Metrics to Know

```
Typical performance targets:
- Read latency: p50 < 1ms, p99 < 10ms
- Write latency: p50 < 5ms, p99 < 50ms
- Availability: 99.99% (52 min downtime/year)
- Replication factor: 3 (tolerates 1 failure)
- Virtual nodes: 100-256 per physical node
```

---

## Summary

A distributed key-value store combines several core concepts:

1. **Partitioning**: Consistent hashing distributes data across nodes
2. **Replication**: Multiple copies ensure durability and availability
3. **Consistency**: Quorum (NWR) provides tunable consistency levels
4. **Failure Handling**: Gossip, hinted handoff, and Merkle trees
5. **Storage**: LSM trees optimize for write-heavy workloads

The key trade-off is between **consistency** and **availability** (CAP theorem). Most modern KV stores choose availability and provide tunable consistency through quorum configuration.

---

## References

- [Amazon Dynamo Paper (2007)](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Consistent Hashing](./consistent-hashing.md)
- [Designing Data-Intensive Applications - Martin Kleppmann](https://dataintensive.net/)
- [Apache Cassandra Architecture](https://cassandra.apache.org/doc/latest/cassandra/architecture/)
