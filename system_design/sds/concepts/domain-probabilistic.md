---
layout: simple
title: "Probabilistic Data Structures — System Design School"
permalink: /system_design/sds/concepts/domain-probabilistic
---

System Design School

- Learn

- Practice

- Primer

- Roadmap

- Pricing

Ask AI TutorStart learning

Lessons

Your progress0%

AllSaved

Concurrency & Transactions

Distributed Systems

Search, Feeds & Spatial

Specialized Systems & Data Structures

Media Systems

- Video Transcoding and Playback

- File Chunking

Probabilistic Data Structures

- Overview

- Bloom Filters 1

- Bloom Filters 2

- Count-Min Sketch 1

- Count-Min Sketch 2

- HyperLogLog 1

- HyperLogLog 2

# Introduction to Probabilistic Data Structures

Start quizSave

Tracking every unique key or event count with an exact hash table works until key cardinality reaches hundreds of millions or billions. Exact structures store every distinct key in memory, so their footprint grows linearly with the number of unique items. When a system only needs a fast membership check, an approximate frequency, or a distinct count, probabilistic data structures replace exact storage with compact summaries whose error rate can be bounded mathematically.

## Why Exact Structures Exhaust Memory at Scale

Consider a web service that tracks unique user IDs to count daily active users or filter out already-seen URLs. Suppose each key is a 16-byte UUID stored inside an exact hash table. Including the key bytes, object headers, and bucket pointers, a hash table entry commonly consumes around 64 bytes in memory. At 100,000,000 unique keys, storing that exact set requires 6.4 GB of RAM for a single metric.

Scaling that requirement to 1,000,000,000 unique keys pushes memory to 64 GB for just one set. Running dozens of such counters across endpoints, tenants, or time windows quickly exceeds single-node RAM and forces slow disk spills or distributed coordination.

Probabilistic data structures avoid storing the raw keys altogether. Each incoming item passes through one or more hash functions and updates a compact array of bits, small counters, or registers. That design discards the ability to list the original items, so the structure can answer one targeted query in constant or sub-linear space.

## Trading Exactness for Bounded Error

Probabilistic data structures do not guess arbitrarily. Their error behavior follows a mathematical bound determined by the memory budget chosen up front. Allocating more bits, counters, or registers shrinks the error rate predictably; allocating less memory increases the error rate in exchange for a smaller footprint.

Three properties make these structures practical in high-throughput distributed systems:

- One-pass streaming updates: each event updates the summary as it arrives, without buffering or sorting the full stream.

- Predictable query time: updates and lookups perform a fixed number of hash computations and array accesses, independent of how many items have already been processed.

- Distributed mergeability: two nodes that maintain compatible summaries (same dimensions and hash functions) can combine their local state with bitwise OR, element-wise addition, or element-wise maximum without shipping raw event logs across the network.

The trade-off is that every query carries an explicit error model. Understanding which direction errors can go is essential before placing a probabilistic structure on a production path.

## The Three-Family Map

Most probabilistic data structures used in system design fall into three families, each answering a different question with a distinct error profile.

FamilyQuestion AnsweredCanonical StructuresError DirectionMemory Scaling

Set membershipIs key x in the set?Bloom Filter, Cuckoo FilterOne-sided: false positives only, zero false negativesProportional to target capacity n (bits per key)

Event frequencyHow many times did x appear?Count-Min SketchOne-sided: overestimates only, never underestimatesFixed d × w counter grid

Distinct cardinalityHow many unique items appeared?HyperLogLogTwo-sided: small relative errorFixed register array (12 KB in Redis)

Each family fits a specific class of system design problems:

- Set membership (Bloom and Cuckoo filters): placed in front of expensive storage or network calls to reject absent keys quickly. A negative answer ("not present") is guaranteed accurate, so the caller skips the disk read or remote lookup safely. A positive answer triggers the authoritative lookup, so a false positive costs only one extra read rather than wrong data.

- Event frequency (Count-Min Sketch): used for heavy-hitter detection, trending topics, and traffic-anomaly tracking in streaming pipelines. Hash collisions can inflate a counter, so estimates never fall below the true count.

- Distinct cardinality (HyperLogLog): used for unique-visitor dashboards, distinct-IP counting, and approximate COUNT(DISTINCT) queries in analytics engines. Redis implements HyperLogLog with 16,384 6-bit registers (12 KB total) and a documented standard error of 0.81%, whether the stream contains thousands or billions of distinct elements.

## When to Use Exact vs. Probabilistic Structures

Probabilistic structures are not a drop-in replacement for exact storage. The decision depends on whether the error direction is safe for the caller.

Use an exact structure whenever a single error causes data corruption, financial loss, or a security failure. Account balances, deduplicating payment charges, and checking authorization permissions cannot tolerate false positives or approximate counts.

Use a probabilistic structure when an authoritative fallback absorbs false positives (as in storage-engine read filters) or when an approximate metric drives dashboards, ranking, or capacity alerts where exactness adds no business value.

Key idea. Exact sets and counters grow linearly in memory with unique key count, which makes them impractical at hundreds of millions of keys. Probabilistic data structures trade exactness for mathematically bounded error in compact, mergeable state: Bloom and Cuckoo filters answer set membership with zero false negatives, Count-Min Sketch estimates frequency without undercounting, and HyperLogLog estimates distinct cardinality in fixed register memory.

The next lesson examines the first family in detail, walking through how Bloom filters map keys into a bit array and how to size them for a target false-positive rate.

Explain

Add to Chat

Start QuizLoading

Send feedback
