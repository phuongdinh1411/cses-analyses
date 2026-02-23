---
layout: simple
title: "Design a Distributed Message Queue"
permalink: /system_design/design-message-queue
---

# Design a Distributed Message Queue

A distributed message queue is middleware that enables asynchronous communication between services by decoupling producers and consumers. Examples include Apache Kafka, RabbitMQ, Amazon SQS, and Pulsar. At scale, the challenge is delivering millions of messages per second with strong durability guarantees, ordering, and exactly-once semantics.

> **Interview context**: This is a common system design question. Focus on **durability vs throughput trade-offs** and be ready to discuss ordering guarantees, delivery semantics, and partition strategies.

---

## Table of Contents

1. [Requirements](#1-requirements)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Core Components](#3-core-components)
4. [Data Model](#4-data-model)
5. [Key Design Decisions](#5-key-design-decisions)
6. [Scalability](#6-scalability)
7. [Reliability](#7-reliability)
8. [Interview Tips](#8-interview-tips)
9. [Key Takeaways](#9-key-takeaways)

---

## 1. Requirements

> **Interview context**: Always start by clarifying requirements. Don't assume---ask questions to understand the scope.

### Questions to Ask the Interviewer

- Do we need strict ordering (per-partition) or global ordering?
- What delivery semantics? At-least-once, at-most-once, or exactly-once?
- What's the expected message size? KBs or MBs?
- Do consumers pull messages or should the queue push?
- What's the retention policy? Hours, days, or indefinite replay?
- Do we need fan-out (one message to many consumers)?

### Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Produce messages** | Producers publish messages to named topics |
| **Consume messages** | Consumers subscribe to topics and receive messages |
| **Topic partitioning** | Messages in a topic are split across partitions for parallelism |
| **Consumer groups** | Multiple consumer groups can independently consume the same topic |
| **Message retention** | Messages are retained for a configurable period (not deleted on consumption) |
| **Ordering** | Messages within a partition are strictly ordered |
| **Replay** | Consumers can re-read messages by resetting their offset |

### Non-Functional Requirements

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| **Availability** | 99.99% | Critical infrastructure for all downstream services |
| **Throughput** | 1M messages/sec | High-volume event streaming |
| **Latency** | p99 < 10ms (produce), p99 < 50ms (consume) | Near real-time processing |
| **Durability** | Zero message loss after acknowledgement | Financial and audit use cases |
| **Data retention** | Configurable, up to 30 days | Replay and debugging |

### Capacity Estimation

```
Producers:           10,000 services
Messages/sec:        1 million (average), 4 million (peak)
Average message size: 1 KB
Daily throughput:     ~86 billion messages
Daily storage:        ~86 TB (raw)
Replication factor:   3
Daily storage (with replication): ~258 TB
30-day retention:     ~7.7 PB
```

---

## 2. High-Level Architecture

> **Interview context**: "Let me draw the high-level architecture first, then we can dive into specific components."

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRODUCERS                               │
│           (Microservices, Applications, IoT devices)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LOAD BALANCER                              │
│                  (DNS round-robin / L4 LB)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Broker  │   │  Broker  │   │  Broker  │
        │    1     │   │    2     │   │    N     │
        └──────────┘   └──────────┘   └──────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Disk    │   │  Coord.  │   │  Metadata│
        │ Storage  │   │ Service  │   │  Store   │
        │ (Append  │   │(ZooKeeper│   │ (etcd)   │
        │  Log)    │   │/ Raft)   │   │          │
        └──────────┘   └──────────┘   └──────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CONSUMERS                                │
│            (Consumer Groups, Stream Processors)                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Technology Choice |
|-----------|---------------|-------------------|
| **Producer Client** | Serialize, partition, batch, and send messages | Client SDK (Java, Go, Python) |
| **Load Balancer** | Route producer/consumer connections to brokers | L4 LB / DNS |
| **Broker** | Receive, store, replicate, and serve messages | Custom (Kafka-like) |
| **Disk Storage** | Persist messages as append-only segment logs | Local SSD / EBS |
| **Coordination Service** | Leader election, partition assignment, cluster membership | ZooKeeper / Raft (KRaft) |
| **Metadata Store** | Topic configs, consumer offsets, ACLs | etcd / embedded in coordination |
| **Consumer Client** | Pull messages, track offsets, handle rebalancing | Client SDK |

---

## 3. Core Components

### 3.1 Broker and Partition Model

> **Interview context**: "Let me explain how messages are distributed across the cluster..."

#### The Challenge

A single server cannot handle 1M messages/sec with durability. We need to split the load across machines while preserving ordering guarantees.

#### Options

| Option | Pros | Cons |
|--------|------|------|
| Single queue per topic | Simple, global ordering | No horizontal scaling, single point of failure |
| Hash-based partitioning | Ordering per key, parallelism | Hot partitions if keys are skewed |
| Round-robin partitioning | Even distribution | No ordering guarantee |

#### Our Approach

Each **topic** is divided into **partitions**. Each partition is an ordered, immutable, append-only sequence of messages. Partitions are distributed across brokers.

```
Topic "orders" (4 partitions):

  Broker 1          Broker 2          Broker 3
┌────────────┐   ┌────────────┐   ┌────────────┐
│ Partition 0│   │ Partition 1│   │ Partition 2│
│ (leader)   │   │ (leader)   │   │ (leader)   │
│ [0,1,2,3..│   │ [0,1,2,3..│   │ [0,1,2,3..│
└────────────┘   └────────────┘   └────────────┘
                                  ┌────────────┐
                                  │ Partition 3│
                                  │ (leader)   │
                                  └────────────┘
```

- **Partition key**: Producer specifies a key; `hash(key) % num_partitions` determines the partition. Messages with the same key always go to the same partition, preserving per-key ordering.
- **No key**: Round-robin across partitions for even load distribution.

#### Why Not Global Ordering?

Global ordering requires funneling all messages through a single node, which caps throughput at what one machine can handle. Per-partition ordering is sufficient for most use cases (e.g., all events for `user_123` are ordered).

> **Interviewer might ask**: "What if I need strict global ordering?"
>
> Use a single partition. You trade throughput for ordering. If throughput is also needed, consider a sequencer service that assigns global sequence numbers, but consumers must buffer and re-order---adding latency and complexity.

---

### 3.2 Replication and Durability

> **Interview context**: "For durability, every partition is replicated across multiple brokers..."

#### The Challenge

If a broker crashes, messages on its partitions are lost unless replicated. We need durability without sacrificing too much throughput.

#### Options

| Option | Pros | Cons |
|--------|------|------|
| No replication | Maximum throughput | Data loss on failure |
| Synchronous replication (all replicas) | Strongest durability | High latency, low availability (one slow replica blocks all) |
| Quorum-based replication | Good durability + availability | More complex, slightly higher latency than async |
| Async replication | Low latency | Potential data loss on leader failure |

#### Our Approach

Each partition has one **leader** and `N-1` **followers** (replication factor = 3 typically). We use an **ISR (In-Sync Replica)** model:

```
Producer ──write──▶ Leader (Broker 1)
                      │
                      ├──replicate──▶ Follower (Broker 2)  ✓ in ISR
                      └──replicate──▶ Follower (Broker 3)  ✓ in ISR

                    ack sent when all ISR replicas confirm
```

- **Leader** handles all reads and writes for a partition.
- **Followers** replicate from the leader.
- **ISR**: The set of replicas that are fully caught up. A message is **committed** only when all ISR replicas have it.
- Producer chooses ack level:
  - `acks=0`: Fire and forget (fastest, risk of loss)
  - `acks=1`: Leader confirms (moderate)
  - `acks=all`: All ISR confirm (strongest durability)

#### Why Not Synchronous Replication to All Replicas?

If one replica is slow or down, the entire partition blocks. ISR allows the system to remove a lagging replica from the sync set and continue operating, re-adding it when it catches up.

> **Interviewer might ask**: "What if the ISR shrinks to just the leader?"
>
> This is configurable via `min.insync.replicas`. If set to 2, the broker rejects writes when ISR < 2, preferring unavailability over potential data loss. This is the **availability vs durability trade-off**.

---

### 3.3 Consumer Groups and Offset Management

> **Interview context**: "Let me explain how consumers read messages..."

#### The Challenge

Multiple services need to consume the same topic independently, and within each service, multiple instances need to share the work without double-processing.

#### Our Approach

- A **consumer group** is a set of consumers that cooperatively consume a topic.
- Each partition is assigned to **exactly one** consumer in the group (no double-processing).
- Different consumer groups get **independent copies** of all messages (fan-out).

```
Topic "orders" (4 partitions)

Consumer Group A (Order Service):     Consumer Group B (Analytics):
┌──────────┐ ┌──────────┐            ┌──────────┐
│Consumer 1│ │Consumer 2│            │Consumer 1│
│ P0, P1   │ │ P2, P3   │            │ P0,P1,P2,│
└──────────┘ └──────────┘            │ P3       │
                                     └──────────┘
```

**Offset tracking**: Each consumer group tracks a **committed offset** per partition---the position of the last successfully processed message. Offsets are stored in a dedicated internal topic (`__consumer_offsets`) or in the metadata store.

- **Auto-commit**: Offsets committed periodically (at-least-once, risk of re-processing on crash).
- **Manual commit**: Consumer commits after processing (stronger exactly-once when combined with idempotent processing).

#### Rebalancing

When consumers join or leave a group, partitions are **rebalanced** (reassigned). Strategies:

| Strategy | Behavior |
|----------|----------|
| **Eager** | Revoke all partitions, reassign. Brief unavailability. |
| **Cooperative (Incremental)** | Only move partitions that need reassigning. Minimal disruption. |

---

### 3.4 Storage Engine (Commit Log)

> **Interview context**: "Under the hood, each partition is stored as a commit log on disk..."

#### The Challenge

Writing millions of messages/sec to disk while maintaining low latency and supporting efficient sequential reads for consumers.

#### Our Approach

Each partition is stored as a series of **segment files**:

```
Partition 0/
├── 00000000000000000000.log    (segment: offsets 0-999999)
├── 00000000000000000000.index  (sparse offset → position index)
├── 00000000000001000000.log    (segment: offsets 1000000-1999999)
├── 00000000000001000000.index
└── ...
```

- **Append-only writes**: Sequential disk I/O (extremely fast, 600+ MB/s on modern SSDs).
- **Segment rotation**: When a segment reaches a size threshold (e.g., 1 GB), a new segment is created.
- **Sparse index**: An index maps every Nth offset to its byte position in the segment file. To find offset K, binary search the index, then scan forward.
- **Zero-copy transfer**: Use `sendfile()` syscall to transfer data from disk to network socket without copying to user space.
- **Retention**: Segments older than the retention period (or beyond size limit) are deleted.

#### Why Not a Traditional Database?

Databases optimize for random reads/writes with B-trees. Message queues are append-heavy with sequential reads---a commit log exploits OS page cache and sequential I/O, achieving 10-100x better throughput.

> **Interviewer might ask**: "How does zero-copy help?"
>
> Normal flow: disk → kernel buffer → user buffer → kernel socket buffer → NIC. With `sendfile()`: disk → kernel buffer → NIC. Eliminates 2 copies and context switches, critical at millions of messages/sec.

---

## 4. Data Model

> **Interview context**: "For the data model, let me think about the key entities..."

### Message Structure

```
Message {
    offset:         int64       // Assigned by broker, unique within partition
    key:            bytes       // Optional, used for partitioning
    value:          bytes       // The payload
    timestamp:      int64       // Producer-set or broker-set
    headers:        map<string, bytes>  // Optional metadata
    compression:    enum        // none, gzip, snappy, lz4, zstd
    crc:            int32       // Checksum for integrity
}
```

### Metadata Schema

```sql
-- Topics and their configurations
CREATE TABLE topics (
    topic_name      VARCHAR(255) PRIMARY KEY,
    num_partitions  INT NOT NULL,
    replication_factor INT NOT NULL,
    retention_ms    BIGINT DEFAULT 604800000,  -- 7 days
    config          JSONB,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Partition assignments (which broker leads/follows which partition)
CREATE TABLE partition_assignments (
    topic_name      VARCHAR(255),
    partition_id    INT,
    broker_id       INT,
    role            ENUM('leader', 'follower'),
    in_isr          BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (topic_name, partition_id, broker_id)
);

-- Consumer group offsets
CREATE TABLE consumer_offsets (
    group_id        VARCHAR(255),
    topic_name      VARCHAR(255),
    partition_id    INT,
    committed_offset BIGINT,
    metadata        VARCHAR(255),
    updated_at      TIMESTAMP,
    PRIMARY KEY (group_id, topic_name, partition_id)
);
```

### Access Patterns

| Query | Frequency | Storage |
|-------|-----------|---------|
| Append message to partition | Very High | Segment log (sequential write) |
| Read messages from offset | Very High | Segment log + sparse index |
| Get/update consumer offset | High | Metadata store / internal topic |
| Get partition leader | Medium | Coordination service cache |
| List topics/partitions | Low | Metadata store |

> **Interviewer might ask**: "Why store offsets in a topic rather than a database?"
>
> Storing offsets in a compacted internal topic (`__consumer_offsets`) uses the same replication infrastructure as data topics, avoiding an external dependency. The topic is compacted (only latest value per key is kept), keeping it small.

---

## 5. Key Design Decisions

### 5.1 Push vs Pull

> **Interview context**: "One key decision is whether consumers pull or the broker pushes..."

| Option | Trade-off |
|--------|-----------|
| **Push** | Lower latency, but broker must manage consumer pace; slow consumers can be overwhelmed |
| **Pull** | Consumer controls rate; supports batching; but requires long-polling to avoid empty polls |

**We chose Pull because**: Consumers process at their own speed. A slow analytics consumer won't back-pressure the broker or affect a fast order-processing consumer. Long-polling (`fetch.min.bytes` + `fetch.max.wait.ms`) eliminates busy-waiting.

### 5.2 Delivery Semantics

> **Interview context**: "For delivery guarantees, we can offer three levels..."

| Semantic | How | Trade-off |
|----------|-----|-----------|
| **At-most-once** | Commit offset before processing | Fast, but messages may be lost on consumer crash |
| **At-least-once** | Commit offset after processing | No loss, but duplicates on crash (consumer retries) |
| **Exactly-once** | Idempotent producer + transactional writes + consume-transform-produce atomically | Strongest, but ~20% throughput overhead |

**We chose at-least-once as default because**: Most use cases can tolerate and handle duplicates (idempotent consumers). Exactly-once is available as an opt-in for critical workflows (e.g., financial transactions).

### 5.3 Message Batching

| Option | Trade-off |
|--------|-----------|
| **No batching** | Lowest latency per message, but high overhead (one network round-trip per message) |
| **Client-side batching** | Amortizes network + compression cost; higher throughput; adds small latency |

**We chose client-side batching because**: Batching with `linger.ms=5ms` and `batch.size=64KB` increases throughput by 10x with negligible latency increase. Compression (lz4/zstd) on batches is far more effective than on individual messages.

### Design Decisions Summary

| Decision | Choice | Alternative | Rationale |
|----------|--------|-------------|-----------|
| Consumer model | Pull-based | Push-based | Consumer backpressure, batching flexibility |
| Delivery default | At-least-once | Exactly-once | Performance; consumers handle idempotency |
| Storage | Append-only log | Database (B-tree) | Sequential I/O; 10x throughput |
| Replication | ISR quorum | Sync-all / Async | Balance of durability and availability |
| Coordination | Raft (KRaft) | ZooKeeper | Fewer moving parts, built-in consensus |
| Batching | Client-side | None | 10x throughput improvement |

---

## 6. Scalability

> **Interview context**: "Let me discuss how this system scales..."

### Horizontal Scaling

```
Producers (stateless, scale freely)
         │
         ▼
┌────────────────────────────────────────────┐
│              Broker Cluster                │
│                                            │
│  Broker 1       Broker 2       Broker N    │
│  ┌──────┐       ┌──────┐      ┌──────┐    │
│  │P0(L) │       │P0(F) │      │P0(F) │    │
│  │P3(F) │       │P1(L) │      │P2(L) │    │
│  │P5(L) │       │P3(L) │      │P3(F) │    │
│  └──────┘       └──────┘      └──────┘    │
│                                            │
│  L = leader, F = follower                  │
└────────────────────────────────────────────┘
         │
         ▼
Consumer Groups (scale up to num_partitions)
```

**Adding capacity**: Add brokers → reassign partition leaders/followers to new brokers → traffic redistributes automatically.

### Scaling Strategies

| Component | Strategy | When to Apply |
|-----------|----------|---------------|
| **Producers** | Add more producer instances | Throughput limited by producer count |
| **Brokers** | Add brokers, increase partitions | Disk I/O > 80%, network saturation |
| **Consumers** | Add consumers (up to partition count) | Consumer lag growing |
| **Partitions** | Increase partition count | Need more parallelism (note: can't decrease) |
| **Storage** | Tiered storage (hot: SSD, cold: S3) | Retention exceeds local disk capacity |

### Bottlenecks and Mitigations

| Bottleneck | Symptom | Mitigation |
|------------|---------|------------|
| Hot partition | One partition has 10x traffic | Better partition key selection, add partitions |
| Disk I/O saturation | High produce latency | Faster SSDs, spread partitions across disks, increase brokers |
| Network bandwidth | Replication lag increases | Compression, dedicated replication network interface |
| Consumer lag | Consumers can't keep up | Add consumers (up to partition count), optimize processing |
| Large messages | Throughput drops, GC pressure | Store payload in object store (S3), send reference in message |
| Rebalancing storms | Frequent consumer joins/leaves | Sticky assignment, cooperative rebalancing, session timeouts |

---

## 7. Reliability

> **Interview context**: "For reliability, let's discuss failure scenarios..."

### Failure Scenarios

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| **Broker crash** | Partitions on that broker unavailable until leader election | ISR follower promoted to leader (< 10s); producer retries to new leader |
| **Disk failure** | Data on that disk lost | Replication ensures other brokers have copies; replace disk and re-replicate |
| **Network partition** | Split brain: two leaders for same partition | Fencing: old leader detects it's no longer in coordination quorum and stops serving |
| **Slow consumer** | Consumer lag grows, messages risk expiring | Monitoring + alerting on lag; scale consumers; increase retention |
| **Producer failure** | Messages in-flight lost | Idempotent producer (dedup on retry via producer ID + sequence number) |
| **Datacenter outage** | Regional unavailability | Multi-datacenter replication (async), MirrorMaker / geo-replication |

### Recovery Procedures

1. **Detection**: Broker heartbeats every 3s; missed 3 heartbeats = broker marked dead
2. **Leader election**: Coordination service picks new leader from ISR (< 10s)
3. **Re-replication**: New follower assigned; catches up from current leader
4. **Consumer rebalancing**: Partitions from dead consumers reassigned to live consumers

### Data Integrity

```
Producer                    Broker
   │                          │
   │──── msg (seq=5) ────────▶│  Write to log
   │                          │  Replicate to ISR
   │◀──── ack ────────────────│  Committed
   │                          │
   │──── msg (seq=5) ────────▶│  Duplicate detected
   │◀──── ack (dedup) ────────│  Idempotent: return success without re-writing
```

- **CRC checksum** on every message: detect corruption on disk or network.
- **Idempotent producer**: Broker tracks `(producer_id, sequence_number)` to dedup retries.
- **Transactional writes**: Atomically write to multiple partitions (for exactly-once stream processing).

---

## 8. Interview Tips

### Approach (45 minutes)

```
0-5 min:   CLARIFY REQUIREMENTS
           - Point-to-point or pub/sub? Ordering needs?
           - Delivery semantics: at-least-once vs exactly-once?
           - Throughput, latency, retention requirements?

5-10 min:  CAPACITY ESTIMATION
           - Messages/sec, message size, storage with replication
           - Number of brokers needed

10-25 min: HIGH-LEVEL DESIGN
           - Producer → Broker cluster → Consumer
           - Topics, partitions, replication
           - Coordination service for metadata

25-40 min: DEEP DIVE (pick 2-3)
           - Storage engine (commit log, segments, zero-copy)
           - Replication protocol (ISR, acks, leader election)
           - Consumer groups and offset management
           - Exactly-once delivery

40-45 min: WRAP UP
           - Summarize key trade-offs
           - Discuss monitoring (consumer lag, broker health)
           - Future: tiered storage, multi-DC replication
```

### Key Phrases That Show Depth

| Instead of... | Say... |
|---------------|--------|
| "Store messages on disk" | "Each partition is an append-only commit log with segment rotation, using sequential I/O and zero-copy for throughput" |
| "Replicate for safety" | "We use ISR-based replication with configurable ack levels---acks=all with min.insync.replicas=2 for strong durability" |
| "Consumers read messages" | "Consumer groups provide independent consumption with at-most-one-consumer-per-partition assignment for ordering guarantees" |
| "Handle failures" | "On broker failure, the coordination service promotes an ISR follower to leader; idempotent producers retry transparently" |

### Common Follow-up Questions

| Question | Key Points |
|----------|------------|
| "How is this different from RabbitMQ?" | RabbitMQ is a traditional message broker (push-based, message deleted after ack). Kafka is a distributed commit log (pull-based, retention-based). RabbitMQ for task queues; Kafka for event streaming. |
| "How do you handle message ordering?" | Per-partition ordering via partition key. Global ordering requires single partition (limits throughput). |
| "What if a consumer is stuck?" | Consumer lag monitoring, dead letter queue for poison messages, max retry count then skip. |
| "How do you handle backpressure?" | Pull model inherently handles it. Producers can be rate-limited. Quotas per client at broker level. |
| "What about exactly-once?" | Idempotent producer (dedup) + transactional writes + read-committed consumers. ~20% overhead. |
| "What if scale increases 10x?" | Add brokers and partitions. Move cold data to tiered storage (S3). Compress more aggressively. |

---

## 9. Key Takeaways

### Core Concepts

1. **Partition is the unit of parallelism**: All scaling decisions revolve around partitions---more partitions mean more throughput and consumer parallelism.
2. **Append-only commit log**: Sequential I/O, zero-copy, and OS page cache make disk-based systems faster than you'd expect.
3. **ISR replication**: A practical middle ground between synchronous replication (slow) and async (unsafe).
4. **Pull-based consumption**: Consumers control their pace, enabling diverse workloads on the same topic.

### Trade-offs to Remember

| Trade-off | When to choose A | When to choose B |
|-----------|------------------|------------------|
| Ordering vs Throughput | Single partition for global order | Many partitions for parallelism |
| Durability vs Latency | `acks=all` for financial data | `acks=1` for clickstream/logs |
| At-least-once vs Exactly-once | Most workloads (simpler, faster) | Financial transactions, dedup-sensitive |
| Retention vs Storage cost | Long retention for replay/debugging | Short retention for ephemeral events |
| Push vs Pull | Low-latency notifications (WebSocket) | Batch processing, diverse consumer speeds |

### Red Flags to Avoid

- Don't skip requirements clarification (push vs pull, ordering, delivery semantics)
- Don't propose a database as the message store without justifying it
- Don't forget replication when discussing durability
- Don't ignore consumer lag monitoring and dead letter queues
- Don't claim global ordering is free---always discuss the throughput trade-off
- Don't confuse message queue (SQS, RabbitMQ) with event streaming (Kafka)---clarify which the interviewer wants

---

## References

- [Designing Data-Intensive Applications - Martin Kleppmann, Ch. 11](https://dataintensive.net/)
- [Kafka: a Distributed Messaging System for Log Processing (LinkedIn, 2011)](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/09/Kafka.pdf)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [The Log: What every software engineer should know (Jay Kreps)](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)
