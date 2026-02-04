---
layout: simple
title: "Design a Unique ID Generator in Distributed Systems"
permalink: /system_design/design-unique-id-generator
---

# Design a Unique ID Generator in Distributed Systems

Generating globally unique IDs in distributed systems is challenging because multiple machines must create IDs independently without coordination, yet guarantee no collisions.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Why Not Simple Solutions?](#why-not-simple-solutions)
3. [Approaches Overview](#approaches-overview)
4. [UUID (Universally Unique Identifier)](#uuid-universally-unique-identifier)
5. [Database Auto-Increment with Ranges](#database-auto-increment-with-ranges)
6. [Twitter Snowflake](#twitter-snowflake)
7. [ULID (Universally Unique Lexicographically Sortable Identifier)](#ulid)
8. [Other Approaches](#other-approaches)
9. [Comparison](#comparison)
10. [Implementation](#implementation)
11. [Real-World Systems](#real-world-systems)
12. [Key Takeaways](#key-takeaways)

---

## Requirements

> **Interview context**: Start by clarifying what "unique ID" means in this context. The requirements drive everything else.

### Functional Requirements

- **Uniqueness**: IDs must be globally unique across all nodes
- **High availability**: ID generation should not be a single point of failure

### Non-Functional Requirements

| Requirement | Description |
|-------------|-------------|
| **Scalability** | Support thousands of ID generations per second per node |
| **Low latency** | Generate IDs in microseconds, not milliseconds |
| **Sortability** | (Optional) IDs should be roughly time-ordered |
| **Size** | Fit in 64 bits for efficient storage and indexing |
| **No coordination** | Nodes generate IDs independently |

### Questions to Ask the Interviewer

> **Interviewer might ask**: "What clarifying questions would you ask?"

| Question | Why It Matters |
|----------|---------------|
| "What's the scale?" | 1000 IDs/sec vs 1M IDs/sec changes the approach |
| "Do IDs need to be sortable?" | Determines UUID vs Snowflake |
| "What's the size constraint?" | 64-bit vs 128-bit changes options |
| "Can IDs reveal information?" | Sequential IDs expose business volume |
| "How many nodes will generate IDs?" | Affects machine ID allocation |

---

## Why Not Simple Solutions?

> **Interview context**: This is the key discussion. Show you understand WHY simple solutions fail before jumping to complex ones.

### Single Database Auto-Increment

The obvious solution: let the database handle it with AUTO_INCREMENT.

**Problems:**
- **Single point of failure** - Database down = no IDs
- **Scalability bottleneck** - All writes hit one database
- **Network latency** - Round trip for every ID

> **Interviewer might ask**: "When IS database auto-increment acceptable?"
>
> For low-scale systems (< 1000 IDs/sec) with a single database, it's fine. The problems arise at scale.

### Timestamp Alone

Why not just use the current time?

**Problems:**
- **Collisions** - Multiple requests in same millisecond
- **Clock skew** - Distributed clocks can drift

> **Interviewer might ask**: "What if we use nanoseconds?"
>
> Even nanoseconds can collide under high load. And clock resolution varies by system—some don't even have nanosecond precision.

---

## Approaches Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ID Generation Strategies                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐   │
│   │    UUID     │   │  Snowflake  │   │  Database Ranges    │   │
│   │  (128-bit)  │   │   (64-bit)  │   │    (64-bit)         │   │
│   └─────────────┘   └─────────────┘   └─────────────────────┘   │
│         │                 │                     │                │
│         ▼                 ▼                     ▼                │
│   No coordination   Time + Node ID      Pre-allocated blocks     │
│   Random/Time       Sortable             Sortable                │
│   128-bit           64-bit compact       64-bit compact          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## UUID (Universally Unique Identifier)

### Overview

128-bit identifier that can be generated independently by any node.

```
550e8400-e29b-41d4-a716-446655440000
└──────┘ └──┘ └──┘ └──┘ └──────────┘
 time_low mid  hi   clk    node
```

### UUID Versions

| Version | Method | Use Case |
|---------|--------|----------|
| **v1** | Timestamp + MAC address | When time-ordering matters |
| **v4** | Random | Most common, simple |
| **v6** | Timestamp (reordered v1) | Sortable, newer standard |
| **v7** | Unix timestamp + random | Sortable, recommended for new systems |

### UUID v4 (Random)

```
xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
              │    │
              │    └── variant (8, 9, a, or b)
              └─────── version (4)
```

**122 random bits** → 2^122 possible values → collision probability negligible

### Pros and Cons

| Pros | Cons |
|------|------|
| No coordination needed | 128 bits (too large for some DBs) |
| Simple to implement | Not sortable (v4) |
| Available in all languages | Poor index performance (random) |
| Collision-free in practice | Not human-readable |

### When to Use UUID

- **Merge data** from independent systems
- **Security** - IDs shouldn't be guessable
- **Simplicity** over performance

---

## Database Auto-Increment with Ranges

> **Interview context**: This is a middle-ground approach. It has coordination, but minimizes it.

### How It Works

A coordinator pre-allocates ID ranges to each server:

```
┌─────────────────┐
│  ID Coordinator │
│  (Database)     │
└────────┬────────┘
         │ Allocate ranges
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
┌───────┐ ┌───────┐  ┌───────┐
│Server1│ │Server2│  │Server3│
│1-1000 │ │1001-  │  │2001-  │
│       │ │2000   │  │3000   │
└───────┘ └───────┘  └───────┘
```

### The Concept

1. Server requests a range of 1000 IDs from coordinator
2. Server generates 1-1000 locally (no network calls)
3. When exhausted, request new range (1001-2000)

**Key trade-off**: Infrequent coordination (every 1000 IDs) instead of per-ID coordination.

### Flickr's Ticket Server

Flickr used two MySQL databases with different auto-increment offsets:

```sql
-- Server 1: generates odd IDs
SET auto_increment_increment = 2;
SET auto_increment_offset = 1;
-- IDs: 1, 3, 5, 7, ...

-- Server 2: generates even IDs
SET auto_increment_increment = 2;
SET auto_increment_offset = 2;
-- IDs: 2, 4, 6, 8, ...
```

### Pros and Cons

| Pros | Cons |
|------|------|
| 64-bit IDs | Requires coordination service |
| Strictly sortable | Single point of failure (coordinator) |
| Simple concept | IDs reveal business volume |

---

## Twitter Snowflake

> **Interview context**: This is often what interviewers want to hear about. Be ready to explain the bit layout and trade-offs.

### Overview

Twitter's Snowflake generates **64-bit, time-sorted, unique IDs** without coordination.

> **Interviewer might ask**: "Why is 64-bit important?"
>
> 64-bit fits in a BIGINT column, which most databases handle efficiently. 128-bit UUIDs often require VARCHAR storage, hurting performance.

### ID Structure (64 bits)

```
0 - 00000000000000000000000000000000000000000 - 00000 - 00000 - 000000000000
│   └──────────────────┬──────────────────────┘ └──┬──┘ └──┬──┘ └─────┬──────┘
│                      │                           │       │          │
│                      │                           │       │          │
│           41 bits: timestamp                5 bits  5 bits    12 bits
│           (milliseconds since epoch)      datacenter machine  sequence
│                                              ID       ID       number
│
└── 1 bit: always 0 (reserved/sign bit)
```

### Bit Allocation

| Field | Bits | Max Value | Description |
|-------|------|-----------|-------------|
| Sign | 1 | 0 | Always 0 (positive number) |
| Timestamp | 41 | ~69 years | Milliseconds since custom epoch |
| Datacenter | 5 | 32 | Datacenter identifier |
| Machine | 5 | 32 | Machine within datacenter |
| Sequence | 12 | 4096 | Counter per millisecond |

### Capacity

- **4096 IDs per millisecond per machine**
- **32 datacenters × 32 machines = 1024 nodes**
- **Total: 4,096,000 IDs/second per node**

### Why Custom Epoch?

> **Interviewer might ask**: "What's the epoch and why customize it?"

Using a recent custom epoch (e.g., 2020-01-01) instead of Unix epoch (1970-01-01) extends the useful life of the timestamp bits.

```
Unix epoch (1970):  41 bits last until ~2039
Custom epoch (2020): 41 bits last until ~2089
```

**Key insight**: You're buying 50+ more years by starting your clock from when your system launches.

### Clock Synchronization Challenge

> **Interviewer might ask**: "What if the clock goes backward?"

This is the Achilles' heel of Snowflake. Options:

| Strategy | Trade-off |
|----------|-----------|
| **Refuse to generate** | Safe but causes errors |
| **Wait until clock catches up** | Delays, but safe |
| **Use last known timestamp** | Risk of collision |

Most implementations refuse to generate, as collision risk is worse than temporary unavailability.

### Pros and Cons

| Pros | Cons |
|------|------|
| 64-bit, fits in BIGINT | Clock sync required |
| Time-sortable | Machine ID assignment complexity |
| High throughput | IDs reveal timestamp |
| No coordination | Limited to 1024 nodes |

---

## ULID

> **Interview context**: ULID is a newer option that's gaining popularity. Mention it to show you know modern alternatives.

### Overview

**Universally Unique Lexicographically Sortable Identifier** - a modern alternative combining UUID's universality with sortability.

### Structure (128 bits, 26 characters)

```
01ARZ3NDEKTSV4RRFFQ69G5FAV
└────────┬────────┘└───┬───┘
         │              │
   48 bits: timestamp   80 bits: randomness
   (milliseconds)
```

### Format

```
 01AN4Z07BY      79KA1307SR9X4MV3
|----------|    |----------------|
 Timestamp          Randomness
   48bits             80bits
```

### Encoding

Uses **Crockford's Base32** (excludes I, L, O, U to avoid confusion):

```
0123456789ABCDEFGHJKMNPQRSTVWXYZ
```

### Comparison: UUID v4 vs ULID

| Feature | UUID v4 | ULID |
|---------|---------|------|
| Size | 128 bits | 128 bits |
| Encoding | Hex (36 chars) | Base32 (26 chars) |
| Sortable | No | Yes |
| Timestamp | No | Yes (48 bits) |
| Randomness | 122 bits | 80 bits |

### Pros and Cons

| Pros | Cons |
|------|------|
| Sortable by time | Larger than Snowflake (128 vs 64 bits) |
| No coordination | Less randomness than UUID v4 |
| URL-safe encoding | Newer, less library support |
| Database-friendly | |

---

## Other Approaches

### MongoDB ObjectId (96 bits)

```
|  4 bytes  |  5 bytes  |  3 bytes  |
| timestamp |  random   |  counter  |
```

### NanoID

- Customizable alphabet and length
- URL-safe by default
- ~126 bits of randomness (21 chars)

```javascript
import { nanoid } from 'nanoid'
nanoid() // => "V1StGXR8_Z5jdHi6B-myT"
```

### Sonyflake (Sony's Snowflake variant)

```
39 bits: timestamp (10ms resolution, ~174 years)
8 bits:  sequence (256 per 10ms)
16 bits: machine ID (65536 machines)
```

### Instagram's ID Generation

```
41 bits: timestamp (milliseconds, custom epoch)
13 bits: shard ID (logical shard)
10 bits: sequence (per shard per millisecond)
```

---

## Comparison

> **Interview context**: Be ready to compare approaches. This is often where interviewers probe your understanding.

### At a Glance

| Approach | Size | Sortable | Coordination | Throughput |
|----------|------|----------|--------------|------------|
| UUID v4 | 128-bit | No | None | Unlimited |
| UUID v7 | 128-bit | Yes | None | Unlimited |
| Snowflake | 64-bit | Yes | Machine ID setup | 4M/s/node |
| ULID | 128-bit | Yes | None | Unlimited |
| DB Range | 64-bit | Yes | Coordinator | Limited |
| MongoDB ObjectId | 96-bit | Yes | None | ~16M/s/node |

### Decision Tree

```
Need unique IDs?
│
├─ Need 64-bit? ──────────────────┐
│   │                             │
│   ├─ Yes ─► Snowflake           │
│   │         (or Sonyflake)      │
│   │                             │
│   └─ No ──► Continue            │
│                                 │
├─ Need sortability? ─────────────┤
│   │                             │
│   ├─ Yes ─► ULID or UUID v7     │
│   │                             │
│   └─ No ──► UUID v4             │
│                                 │
├─ Need sequential? ──────────────┤
│   │                             │
│   └─ Yes ─► DB Range/Ticket     │
│                                 │
└─ Default ─► UUID v4 (simplest)
```

---

## Interview Tips

### How to Approach (45 minutes)

```
0-5 min:   CLARIFY REQUIREMENTS
           "What's the scale? Do IDs need to be sortable?
            What's the size constraint? 64-bit or 128-bit?"

5-10 min:  DISCUSS SIMPLE SOLUTIONS AND WHY THEY FAIL
           Auto-increment: single point of failure
           Timestamp: collisions

10-25 min: PRESENT OPTIONS
           UUID: simple, no coordination, 128-bit
           Snowflake: 64-bit, sortable, needs clock sync
           Database ranges: strictly sequential, needs coordinator

25-35 min: DEEP DIVE ON CHOSEN APPROACH
           If interviewer asks for 64-bit sortable → Snowflake
           Explain bit layout, clock handling

35-45 min: DISCUSS TRADE-OFFS AND EDGE CASES
           Clock skew, machine ID assignment, collision probability
```

### Key Phrases That Show Depth

| Instead of... | Say... |
|---------------|--------|
| "UUID is unique" | "UUID v4 has 122 random bits. With 2^122 possibilities, collision probability is negligible—you'd need to generate 2.7 quintillion IDs for 50% collision chance." |
| "Snowflake uses time" | "Snowflake embeds 41-bit millisecond timestamp, giving ~69 years before overflow. Using a custom epoch extends this—if we start from 2020, we're good until ~2089." |
| "We need machine IDs" | "With 10 bits for machine ID, we support 1024 nodes. We could use Zookeeper for coordination, or derive from IP address for simpler deployment." |

### Common Follow-up Questions

| Question | Key Points |
|----------|------------|
| "What if clock goes backward?" | Refuse to generate (safest), wait until clock catches up, or use last timestamp (risky) |
| "How do you assign machine IDs?" | Zookeeper coordination, derive from IP/MAC, config files, or use container orchestration |
| "What's the collision probability?" | UUID: 2^-122 per ID pair. Snowflake: zero if machine IDs are unique |
| "Why not use database?" | Single point of failure, network latency per ID, scalability bottleneck |
| "When would you use UUID over Snowflake?" | When 128-bit is acceptable, no coordination desired, sortability not needed |

---

## Real-World Systems

> **Interview context**: Mentioning real systems shows industry awareness.

### Twitter

- **Snowflake** for tweet IDs, user IDs
- Custom epoch: November 4, 2010 (Twitter's internal date)
- Open-sourced but deprecated in favor of internal versions

### Discord

- Modified Snowflake with **42-bit timestamp** (milliseconds since Discord epoch)
- Used for message IDs, user IDs, server IDs
- Discord epoch: January 1, 2015

```python
# Discord Snowflake structure
# 42 bits: timestamp
# 5 bits:  internal worker ID
# 5 bits:  internal process ID
# 12 bits: sequence
```

### Instagram

- **PostgreSQL-based** at the database layer
- 41-bit timestamp + 13-bit shard ID + 10-bit sequence
- Each shard generates IDs independently
- Clever: ID generation in the database means no separate service

### Stripe

- Uses **custom IDs** with prefixes for type identification:

```
ch_1MzNLY2eZvKYlo2C5LGJ8YDh   # Charge
cus_NkPJq8AbSnpOQo            # Customer
pi_3MzNLY2eZvKYlo2C1IJCJQqA   # PaymentIntent
```

### MongoDB

- **ObjectId** (12 bytes = 96 bits):
  - 4 bytes: Unix timestamp
  - 5 bytes: Random value (unique per machine/process)
  - 3 bytes: Counter

---

## Key Takeaways

### Decision Summary

| Requirement | Best Choice | Why |
|-------------|-------------|-----|
| 64-bit, sortable | Snowflake | Compact, time-ordered |
| No coordination, simple | UUID v4 | Standard, available everywhere |
| Sortable, no coordination | ULID or UUID v7 | Modern, database-friendly |
| Strictly sequential | Database ranges | Predictable order |
| High throughput (>1M/s) | Snowflake | 4096 IDs/ms/node |

### Trade-offs to Discuss

| Trade-off | Option A | Option B |
|-----------|----------|----------|
| Size | 64-bit (efficient) | 128-bit (simpler) |
| Sortability | Time-sortable (reveals timing) | Random (index fragmentation) |
| Coordination | Required (machine IDs) | None (larger IDs) |
| Clock dependency | Yes (Snowflake) | No (UUID v4) |

### Critical Considerations

1. **Clock synchronization** is critical for time-based generators (NTP required)
2. **Machine ID assignment** needs a reliable mechanism (Zookeeper, config, or derivation)
3. **Sortable IDs leak information** - attackers can estimate your transaction volume
4. **Random IDs fragment B-tree indexes** - new inserts scatter across pages
