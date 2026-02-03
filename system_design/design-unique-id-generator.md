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

---

## Why Not Simple Solutions?

### Single Database Auto-Increment

```sql
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ...
);
```

**Problems:**
- **Single point of failure** - Database down = no IDs
- **Scalability bottleneck** - All writes hit one database
- **Network latency** - Round trip for every ID

### Timestamp Alone

```
ID = current_timestamp_millis()
```

**Problems:**
- **Collisions** - Multiple requests in same millisecond
- **Clock skew** - Distributed clocks drift

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

### Implementation

```python
class RangeIDGenerator:
    def __init__(self, coordinator, range_size=1000):
        self.range_size = range_size
        self.coordinator = coordinator
        self.current_id = 0
        self.max_id = 0

    def next_id(self):
        if self.current_id >= self.max_id:
            # Fetch new range from coordinator
            self.current_id = self.coordinator.allocate_range(self.range_size)
            self.max_id = self.current_id + self.range_size

        id = self.current_id
        self.current_id += 1
        return id
```

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

### Overview

Twitter's Snowflake generates **64-bit, time-sorted, unique IDs** without coordination.

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

Using a recent custom epoch (e.g., 2020-01-01) instead of Unix epoch (1970-01-01) extends the useful life of the timestamp bits.

```
Unix epoch (1970):  41 bits last until ~2039
Custom epoch (2020): 41 bits last until ~2089
```

### Pros and Cons

| Pros | Cons |
|------|------|
| 64-bit, fits in BIGINT | Clock sync required |
| Time-sortable | Machine ID assignment complexity |
| High throughput | IDs reveal timestamp |
| No coordination | Limited to 1024 nodes |

---

## ULID

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

## Implementation

### Snowflake Implementation (Python)

```python
import time
import threading

class SnowflakeGenerator:
    # Custom epoch: 2020-01-01 00:00:00 UTC
    EPOCH = 1577836800000

    # Bit lengths
    TIMESTAMP_BITS = 41
    DATACENTER_BITS = 5
    MACHINE_BITS = 5
    SEQUENCE_BITS = 12

    # Max values
    MAX_DATACENTER_ID = (1 << DATACENTER_BITS) - 1  # 31
    MAX_MACHINE_ID = (1 << MACHINE_BITS) - 1        # 31
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1         # 4095

    # Bit shifts
    MACHINE_SHIFT = SEQUENCE_BITS                           # 12
    DATACENTER_SHIFT = SEQUENCE_BITS + MACHINE_BITS         # 17
    TIMESTAMP_SHIFT = SEQUENCE_BITS + MACHINE_BITS + DATACENTER_BITS  # 22

    def __init__(self, datacenter_id: int, machine_id: int):
        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError(f"Datacenter ID must be between 0 and {self.MAX_DATACENTER_ID}")
        if machine_id > self.MAX_MACHINE_ID or machine_id < 0:
            raise ValueError(f"Machine ID must be between 0 and {self.MAX_MACHINE_ID}")

        self.datacenter_id = datacenter_id
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _current_millis(self) -> int:
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp: int) -> int:
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            timestamp = self._current_millis()
        return timestamp

    def next_id(self) -> int:
        with self.lock:
            timestamp = self._current_millis()

            # Clock moved backwards - handle error
            if timestamp < self.last_timestamp:
                raise Exception(f"Clock moved backwards. Refusing to generate ID.")

            # Same millisecond - increment sequence
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                if self.sequence == 0:
                    # Sequence exhausted, wait for next millisecond
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                # New millisecond - reset sequence
                self.sequence = 0

            self.last_timestamp = timestamp

            # Construct the ID
            id = ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) | \
                 (self.datacenter_id << self.DATACENTER_SHIFT) | \
                 (self.machine_id << self.MACHINE_SHIFT) | \
                 self.sequence

            return id

    @staticmethod
    def parse_id(id: int) -> dict:
        """Extract components from a Snowflake ID"""
        sequence = id & ((1 << SnowflakeGenerator.SEQUENCE_BITS) - 1)
        machine_id = (id >> SnowflakeGenerator.MACHINE_SHIFT) & ((1 << SnowflakeGenerator.MACHINE_BITS) - 1)
        datacenter_id = (id >> SnowflakeGenerator.DATACENTER_SHIFT) & ((1 << SnowflakeGenerator.DATACENTER_BITS) - 1)
        timestamp = (id >> SnowflakeGenerator.TIMESTAMP_SHIFT) + SnowflakeGenerator.EPOCH

        return {
            'timestamp': timestamp,
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000)),
            'datacenter_id': datacenter_id,
            'machine_id': machine_id,
            'sequence': sequence
        }
```

### Usage Example

```python
# Initialize generator for datacenter 1, machine 5
generator = SnowflakeGenerator(datacenter_id=1, machine_id=5)

# Generate IDs
for _ in range(5):
    id = generator.next_id()
    print(f"ID: {id}")
    print(f"Parsed: {SnowflakeGenerator.parse_id(id)}")
    print()

# Output:
# ID: 7151853158892699648
# Parsed: {'timestamp': 1704067200123, 'datetime': '2024-01-01 00:00:00',
#          'datacenter_id': 1, 'machine_id': 5, 'sequence': 0}
```

### ULID Implementation (Python)

```python
import time
import os
import struct

class ULIDGenerator:
    ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    def generate(self) -> str:
        # 48-bit timestamp (milliseconds)
        timestamp = int(time.time() * 1000)

        # 80-bit randomness
        randomness = os.urandom(10)

        # Encode timestamp (10 characters)
        time_chars = []
        for _ in range(10):
            time_chars.append(self.ENCODING[timestamp & 0x1F])
            timestamp >>= 5
        time_part = ''.join(reversed(time_chars))

        # Encode randomness (16 characters)
        random_int = int.from_bytes(randomness, 'big')
        rand_chars = []
        for _ in range(16):
            rand_chars.append(self.ENCODING[random_int & 0x1F])
            random_int >>= 5
        rand_part = ''.join(reversed(rand_chars))

        return time_part + rand_part

# Usage
ulid_gen = ULIDGenerator()
print(ulid_gen.generate())  # => "01HV3GXMJ6KQWN5X8YZ4R2P7TC"
```

---

## Real-World Systems

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

- **PostgreSQL-based** with PL/pgSQL function
- 41-bit timestamp + 13-bit shard ID + 10-bit sequence
- Each shard generates IDs independently

```sql
CREATE OR REPLACE FUNCTION next_id(OUT result bigint) AS $$
DECLARE
    our_epoch bigint := 1314220021721;
    seq_id bigint;
    now_millis bigint;
    shard_id int := 5;  -- Configured per shard
BEGIN
    SELECT nextval('table_id_seq') % 1024 INTO seq_id;
    SELECT FLOOR(EXTRACT(EPOCH FROM clock_timestamp()) * 1000) INTO now_millis;
    result := (now_millis - our_epoch) << 23;
    result := result | (shard_id << 10);
    result := result | (seq_id);
END;
$$ LANGUAGE plpgsql;
```

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

1. **No single best solution** - Choose based on requirements (size, sortability, simplicity)

2. **Snowflake** is ideal when you need:
   - 64-bit IDs
   - Time-sortable
   - High throughput
   - Predictable format

3. **UUID v4/v7** is ideal when you need:
   - No coordination
   - Maximum simplicity
   - Security (unpredictable IDs)

4. **ULID** is ideal when you need:
   - Sortability without coordination
   - URL-safe format
   - Modern UUID alternative

5. **Clock synchronization** is critical for time-based generators (NTP required)

6. **Trade-offs**:
   - Sortable IDs leak timing information
   - Random IDs cause index fragmentation
   - Smaller IDs (64-bit) require coordination or machine IDs
