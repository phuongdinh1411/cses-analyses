---
layout: simple
title: "Bitmask Techniques"
permalink: /pattern/bitmask
---

# Bitmask Techniques — Comprehensive Pattern Guide

---

## What Are Bitmask Techniques?

Bitmask techniques use binary representations and bitwise operations to efficiently solve problems involving:

1. **Subsets and combinations**: Representing sets as binary numbers
2. **State compression**: Encoding complex states in integers
3. **Fast set operations**: Using bitwise AND, OR, XOR for O(1) operations
4. **Dynamic programming**: Tracking "which elements have been processed"

**Key Idea**: An n-bit integer can represent a subset of n elements, where bit i indicates whether element i is included.

```
Example: Set {0, 1, 2, 3}, subset {0, 2, 3}
Binary: 1101 (reading right to left: positions 0, 2, 3 are set)
Decimal: 13

All subsets of {0, 1, 2}:
000 (0) = {}
001 (1) = {0}
010 (2) = {1}
011 (3) = {0, 1}
100 (4) = {2}
101 (5) = {0, 2}
110 (6) = {1, 2}
111 (7) = {0, 1, 2}
```

**When to use bitmask**: n ≤ 20-24 elements (2^20 ≈ 1 million states)

---

## Quick Navigation: I need to...

| I need to... | Technique | Numbered LC | Jump to |
|--------------|-----------|-------------|---------|
| List every subset of `n` items | Subset enumeration | **78** Subsets | [§2](#2-subset-enumeration-techniques) · [walkthrough](#problem-78--subsets) |
| Split items into `k` fair groups / buckets | Subset DP over groups | **2305** Fair Distribution, **698** Partition to K | [§3](#3-bitmask-dp-patterns) · [walkthrough](#problem-2305--fair-distribution-of-cookies) |
| Assign `n` workers to `n` jobs, min cost | Assignment DP `dp[mask]` | **698** (disguise) | [§3 Pattern 2](#pattern-2-assignment-problem) |
| Visit ALL nodes, cost depends on where I am now | TSP `dp[mask][last]` | **847** Shortest Path Visiting All Nodes | [§3 Pattern 1](#pattern-1-traveling-salesman-problem-tsp) · [walkthrough](#problem-847--shortest-path-visiting-all-nodes) |
| Aggregate a value over all submasks of every mask | SOS DP | **1178** Valid Words for Puzzles | [§5](#5-sos-sum-over-subsets-dp) · [walkthrough](#problem-1178--number-of-valid-words-for-each-puzzle) |
| Find max XOR of a subset | XOR (linear) basis | **1707** Max XOR With Element | [§5 max_xor_subset](#5-sos-sum-over-subsets-dp) |
| Tile a grid / narrow board | Profile DP `dp[col][profile]` | **1349** Max Students | [§6 Template 3](#template-3-profile-dp-grid-problems) |

**The one split that matters**: are you manipulating **the bits of ONE number** (bit tricks — §1, §4) or is **the set of chosen items itself the DP state key** (bitmask DP — §3, §5)? Different skill, same syntax.

---

## Master LeetCode Comparison Table

| LC # | Title | Diff | State | Transition (one-liner) | Cost |
|------|-------|------|-------|------------------------|------|
| **78** | Subsets | Easy | `mask ∈ [0, 2^n)` | bit `i` set → include `nums[i]` | O(2^n · n) |
| **698** | Partition to K Equal Sum Subsets | Medium | `dp[mask]` = filled amount of current bucket (mod target) | add unused item if it fits current bucket | O(2^n · n) |
| **2305** | Fair Distribution of Cookies | Medium | `dp[j][mask]` = min unfairness giving `mask` to first `j` kids | give kid `j` some submask `s` of `mask` | O(k · 3^n) |
| **847** | Shortest Path Visiting All Nodes | Hard | `(node, mask)` = at `node`, visited set `mask` | BFS to neighbor, `mask │ (1<<nb)` | O(2^n · n²) |
| **1178** | Number of Valid Words for Each Puzzle | Hard | `cnt[wordmask]` frequency | sum `cnt[sub]` over submasks of puzzle containing first letter | O(W·7 + P·2^7) |

Read the **State** column top to bottom: `mask` alone (78, 698) → `dp[j][mask]` splitting a set (2305) → `(node, mask)` position + set (847) → precomputed masks queried by submask (1178). That progression *is* the learning ladder — each row adds one dimension to what the mask tracks.

---

## Table of Contents

1. [Fundamental Bit Operations](#1-fundamental-bit-operations)
2. [Subset Enumeration Techniques](#2-subset-enumeration-techniques)
3. [Bitmask DP Patterns](#3-bitmask-dp-patterns)
4. [Advanced Bit Tricks](#4-advanced-bit-tricks)
5. [SOS (Sum Over Subsets) DP](#5-sos-sum-over-subsets-dp)
6. [Common Problem Templates](#6-common-problem-templates)
7. [Practice Problems](#7-practice-problems)

---

## Why This Pattern Exists

When `n ≤ ~20` and you must track **which** subset of items is chosen/visited — not just *how many* — a bitmask encodes the subset as the bits of a single integer. Then `2^n` possible subsets become plain array indices, and set operations (union, intersection, membership) become one machine instruction.

Concrete examples:

- **TSP**: `mask` = set of cities already visited, so `dp[mask][i]` is "cheapest tour visiting exactly those cities, ending at `i`."
- **Assignment**: `mask` = set of workers already assigned, so `dp[mask]` is "cheapest way to assign those workers to the first `popcount(mask)` jobs."

The size limit is the whole point: `2^20 ≈ 1,000,000` states is fine, but `2^25` (≈ 33M) starts to hurt and factorial enumeration (`20! ≈ 2.4×10^18`) is hopeless. A bitmask turns an exponential *enumeration* into an exponential *table* you fill once.

`★ Insight ─────────────────────────────────────`
- The bitmask is not the algorithm — it is the **state key**. You still need a DP recurrence (or search) over those keys. Bitmask just makes "the set of used elements" a cheap, hashable index.
- Reach for it only when the *identity* of the chosen elements matters. If you only need a count or a sum, a cheaper 1-D DP usually beats `2^n`.
`─────────────────────────────────────────────────`

---

## 1. Fundamental Bit Operations

### Basic Operations

```python
# ============================================
# CHECK, SET, CLEAR, TOGGLE
# ============================================

mask = 0b10110  # Binary: 10110

# Check if bit n is set
def is_set(mask, n):
    return bool(mask & (1 << n))

# Set bit n to 1
def set_bit(mask, n):
    return mask | (1 << n)

# Clear bit n (set to 0)
def clear_bit(mask, n):
    return mask & ~(1 << n)

# Toggle bit n
def toggle_bit(mask, n):
    return mask ^ (1 << n)

# Example
n = 2
print(f"Is bit {n} set in {bin(mask)}? {is_set(mask, n)}")  # True
mask = clear_bit(mask, n)
print(f"After clearing bit {n}: {bin(mask)}")  # 0b10010
```

### Counting and Finding Bits

```python
# ============================================
# POPCOUNT, LOWEST BIT, TRAILING ZEROS
# ============================================

# Count number of set bits (popcount)
def popcount_builtin(mask):
    return bin(mask).count('1')

def popcount_kernighan(mask):
    """Brian Kernighan's algorithm - O(number of set bits)"""
    count = 0
    while mask:
        mask &= mask - 1  # Remove lowest set bit
        count += 1
    return count

# Get the lowest set bit
def lowest_bit(mask):
    return mask & -mask
    # Example: 10110 & -10110 = 00010

# Remove the lowest set bit
def remove_lowest_bit(mask):
    return mask & (mask - 1)
    # Example: 10110 → 10100

# Count trailing zeros (position of lowest set bit)
def count_trailing_zeros(mask):
    if mask == 0:
        return 32  # Or 64 for 64-bit
    return (mask & -mask).bit_length() - 1

# Position of rightmost set bit (1-indexed)
def rightmost_bit_position(mask):
    return (mask & -mask).bit_length()

# Examples
mask = 0b10110
print(f"Popcount: {popcount_builtin(mask)}")  # 3
print(f"Lowest bit: {bin(lowest_bit(mask))}")  # 0b10
print(f"Trailing zeros: {count_trailing_zeros(mask)}")  # 1
```

### Checking Properties

```python
# ============================================
# CHECKING BITMASK PROPERTIES
# ============================================

# Check if power of 2 (exactly one bit set)
def is_power_of_2(mask):
    return mask > 0 and (mask & (mask - 1)) == 0

# Check if two masks are disjoint (no common bits)
def are_disjoint(mask1, mask2):
    return (mask1 & mask2) == 0

# Check if mask1 is subset of mask2
def is_subset(mask1, mask2):
    return (mask1 & mask2) == mask1

# Get bits in mask1 but not in mask2
def difference(mask1, mask2):
    return mask1 & ~mask2

# Get all bits up to position n
def all_bits(n):
    return (1 << n) - 1
    # Example: n=5 → 0b11111 (31)

# Examples
print(is_power_of_2(8))  # True
print(is_power_of_2(6))  # False
print(are_disjoint(0b1100, 0b0011))  # True
print(is_subset(0b0101, 0b1101))  # True
```

`★ Insight ─────────────────────────────────────`
- `x & -x` isolates the **lowest set bit** because two's-complement negation flips-then-adds-1, so `-x` matches `x` above the lowest 1 (all flipped) and the lowest 1 aligns. This one identity powers popcount (Kernighan), trailing-zero count, and Fenwick tree index stepping — learn it once, reuse everywhere.
- `x & (x-1)` clears the lowest set bit; `x & (x+1)`-style tricks turn bits on. The `is_subset(a, b) == ((a & b) == a)` test is the membership check bitmask DP leans on constantly — "is this smaller set contained in that one" in one AND.
`─────────────────────────────────────────────────`

---

## 2. Subset Enumeration Techniques

### Iterate All Subsets

```python
# ============================================
# ENUMERATE ALL 2^n SUBSETS
# ============================================

def enumerate_all_subsets(n):
    """Generate all subsets of {0, 1, ..., n-1}"""
    for mask in range(1 << n):
        subset = [i for i in range(n) if mask & (1 << i)]
        yield mask, subset

# Example: All subsets of {0, 1, 2}
for mask, subset in enumerate_all_subsets(3):
    print(f"{mask:03b} → {subset}")

# Output:
# 000 → []
# 001 → [0]
# 010 → [1]
# 011 → [0, 1]
# 100 → [2]
# 101 → [0, 2]
# 110 → [1, 2]
# 111 → [0, 1, 2]
```

### Iterate All Submasks

```python
# ============================================
# ENUMERATE ALL SUBMASKS OF A MASK
# ============================================

def enumerate_submasks(mask):
    """
    Generate all submasks of mask in descending order.

    Key technique: submask = (submask - 1) & mask
    Time: O(2^k) where k = popcount(mask)
    """
    submask = mask
    while submask > 0:
        yield submask
        submask = (submask - 1) & mask

# Example: Submasks of 0b1011 (11)
mask = 0b1011
print(f"Submasks of {bin(mask)}:")
for submask in enumerate_submasks(mask):
    print(f"  {submask:04b} ({submask})")

# Output:
# Submasks of 0b1011:
#   1011 (11)
#   1010 (10)
#   1001 (9)
#   1000 (8)
#   0011 (3)
#   0010 (2)
#   0001 (1)

# Including empty submask
def enumerate_submasks_with_zero(mask):
    """Include the empty submask (0)"""
    submask = mask
    while True:
        yield submask
        if submask == 0:
            break
        submask = (submask - 1) & mask
```

### Iterate All Submask Pairs

```python
# ============================================
# ENUMERATE ALL WAYS TO PARTITION A MASK
# ============================================

def enumerate_submask_pairs(mask):
    """
    Generate all ways to partition mask into two non-empty parts.
    Returns (submask, complement) pairs.
    """
    submask = mask
    while submask > 0:
        complement = mask ^ submask  # mask XOR submask
        if complement > 0:  # Both must be non-empty
            yield (submask, complement)
        submask = (submask - 1) & mask

# Optimization: Avoid duplicate pairs
def enumerate_unique_submask_pairs(mask):
    """Generate unique pairs where submask <= complement"""
    submask = mask
    while submask > 0:
        complement = mask ^ submask
        if submask <= complement and complement > 0:
            yield (submask, complement)
        submask = (submask - 1) & mask

# Example: Partition 0b111 (7)
mask = 0b111
print("All partitions:")
for s1, s2 in enumerate_unique_submask_pairs(mask):
    print(f"  {s1:03b} | {s2:03b}")

# Output:
#   001 | 110
#   010 | 101
#   011 | 100
```

### Iterate k-Element Subsets (Gosper's Hack)

```python
# ============================================
# ENUMERATE ALL k-ELEMENT SUBSETS
# ============================================

def next_combination(mask):
    """
    Get next mask with same number of bits set.
    Gosper's hack - generates combinations in lexicographic order.
    """
    c = mask & -mask  # Rightmost set bit
    r = mask + c      # Add it
    return (((r ^ mask) >> 2) // c) | r

def enumerate_k_subsets(n, k):
    """Generate all C(n, k) subsets of size k from {0, 1, ..., n-1}"""
    if k == 0:
        yield 0
        return

    mask = (1 << k) - 1  # Start with k rightmost bits set
    limit = 1 << n

    while mask < limit:
        yield mask
        mask = next_combination(mask)

# Example: All 3-element subsets of 5 elements
print("All 3-element subsets of {0,1,2,3,4}:")
for mask in enumerate_k_subsets(5, 3):
    elements = [i for i in range(5) if mask & (1 << i)]
    print(f"  {mask:05b} → {elements}")

# Output:
#   00111 → [0, 1, 2]
#   01011 → [0, 1, 3]
#   01101 → [0, 2, 3]
#   01110 → [1, 2, 3]
#   10011 → [0, 1, 4]
#   ... (total of C(5,3) = 10 subsets)
```

### Problem 78 — Subsets

**Difficulty**: Easy · **This template solves**: the [Iterate All Subsets](#2-subset-enumeration-techniques) template.

> Given an integer array `nums` of **unique** elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets.

The bitmask insight: there are exactly `2^n` subsets, and the integers `0 .. 2^n - 1` are in **bijection** with them. Integer `mask` encodes the subset "take `nums[i]` iff bit `i` is set." So a single `for mask in range(1 << n)` loop enumerates the entire power set — no recursion, no backtracking bookkeeping.

```python
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        out = []
        for mask in range(1 << n):
            out.append([nums[i] for i in range(n) if mask & (1 << i)])
        return out
```

**Trace** on `nums = [1, 2, 3]` (bit 0 → 1, bit 1 → 2, bit 2 → 3):

```
mask  binary   bits set        subset
 0    000      —               []
 1    001      0               [1]
 2    010      1               [2]
 3    011      0,1             [1, 2]
 4    100      2               [3]
 5    101      0,2             [1, 3]
 6    110      1,2             [2, 3]
 7    111      0,1,2           [1, 2, 3]
                                → 2^3 = 8 subsets
```

`★ Insight ─────────────────────────────────────`
- The mask-as-subset bijection is why bitmask beats recursion here: the loop counter `mask` *is* the subset. Bit order gives a free, deterministic ordering — no visited set, no dedup.
- This only works because elements are **unique**. If `nums` has duplicates, two different masks can yield the same multiset — then you sort + skip, or count occurrences, because the bijection breaks.
`─────────────────────────────────────────────────`

---

## 3. Bitmask DP Patterns

### Pattern 1: Traveling Salesman Problem (TSP)

**Problem**: Visit all n cities exactly once, minimize total distance.

**State**: `dp[mask][i]` = minimum cost to visit cities in `mask`, ending at city `i`

```python
def tsp(dist, n):
    """
    Traveling Salesman Problem using bitmask DP.

    State: dp[mask][i] = min cost to visit cities in mask, ending at city i
    Transition: Try going from city i to unvisited city j

    Time: O(2^n * n^2)
    Space: O(2^n * n)
    """
    INF = float('inf')
    # dp[mask][i] = min cost to reach state (mask, i)
    dp = [[INF] * n for _ in range(1 << n)]

    # Base case: start at city 0
    dp[1][0] = 0

    # Fill DP table
    for mask in range(1 << n):
        for u in range(n):
            # Skip if city u not in mask or unreachable
            if not (mask & (1 << u)) or dp[mask][u] == INF:
                continue

            # Try going to unvisited city v
            for v in range(n):
                if mask & (1 << v):  # v already visited
                    continue

                next_mask = mask | (1 << v)
                dp[next_mask][v] = min(dp[next_mask][v],
                                      dp[mask][u] + dist[u][v])

    # Return minimum cost ending at any city (or add return to start)
    full_mask = (1 << n) - 1
    return min(dp[full_mask][i] for i in range(n))

# Example usage
dist = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
print(f"Minimum TSP cost: {tsp(dist, 4)}")
```

### Problem 847 — Shortest Path Visiting All Nodes

**Difficulty**: Hard · **This template solves**: the [TSP `dp[mask][last]`](#pattern-1-traveling-salesman-problem-tsp) state, in BFS form.

> Undirected connected graph of `n` nodes. Return the length of the shortest path that visits **every** node. You may start and stop at any node, revisit nodes, and reuse edges.

This is TSP's cousin: the state is still `(mask, last)` = "visited set `mask`, currently standing on `last`." But because every edge has weight 1 and you may **revisit**, the shortest path is a plain BFS over that state space — the first time BFS reaches any `(full_mask, *)` is the answer. Revisiting means `mask` can stay the same while `node` changes, so this isn't a Hamiltonian path (each node once); it's "cover all nodes, steps minimized."

```python
from collections import deque

class Solution:
    def shortestPathLength(self, graph: list[list[int]]) -> int:
        n = len(graph)
        if n == 1:
            return 0
        full = (1 << n) - 1
        # Start BFS from EVERY node simultaneously (multi-source).
        seen = set()
        q = deque()
        for i in range(n):
            q.append((i, 1 << i, 0))   # (node, visited mask, dist)
            seen.add((i, 1 << i))

        while q:
            node, mask, dist = q.popleft()
            if mask == full:
                return dist
            for nb in graph[node]:
                nm = mask | (1 << nb)
                if (nb, nm) not in seen:
                    seen.add((nb, nm))
                    q.append((nb, nm, dist + 1))
        return -1
```

**Trace** on `graph = [[1,2,3],[0],[0],[0]]` — a star with hub 0 and leaves 1, 2, 3. `full = 1111`.

```
Start (dist 0): (0,0001) (1,0010) (2,0100) (3,1000)   all seeded

dist 1: from 0 → 1,2,3   gives (1,0011)(2,0101)(3,1001)
        from 1 → 0       gives (0,0011)
        from 2 → 0       gives (0,0101)
        from 3 → 0       gives (0,1001)
dist 2: (0,0011)→2,3: (2,0111)(3,1011);  (0,0101)→…(3,1101); (0,1001)→…(2,1101)
        also leaves push back to hub, growing masks
dist 3: reach (0,0111)→3 = (3,1111) ✓  → return 3?  No — hub must be re-entered.

Path 1→0→2→0→3 visits {1,0,2,3}=full in 4 steps → answer 4.
```

Running the code returns **4**: to cover all leaves you must bounce through the hub between each, so the state `(0, 0111)` is reached at dist 3, then step to `(3, 1111)` at dist 4.

`★ Insight ─────────────────────────────────────`
- Two encodings of the SAME state. Weighted TSP fills a `dp[mask][last]` table (Pattern 1). Unit-weight "visit all" uses BFS over `(mask, last)` — BFS *is* the DP, dequeue order guarantees the first full-mask hit is shortest.
- **Multi-source start** is the trick that makes "start anywhere" free: seed all `n` start states at dist 0 instead of running `n` separate BFS runs. The `2^n · n` state count is the ceiling, so BFS is O(2^n · n²) with the neighbor loop.
`─────────────────────────────────────────────────`

### Pattern 2: Assignment Problem

**Problem**: Assign n workers to n jobs, minimize total cost.

**State**: `dp[mask]` = minimum cost to assign workers in `mask` to first k jobs

```python
def min_cost_assignment(cost, n):
    """
    Assign n workers to n jobs to minimize cost.

    State: dp[mask] = min cost to assign workers in mask to jobs 0..k-1
           where k = popcount(mask)

    Time: O(2^n * n)
    Space: O(2^n)
    """
    INF = float('inf')
    dp = [INF] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        if dp[mask] == INF:
            continue

        # Number of jobs already assigned
        jobs_assigned = bin(mask).count('1')

        # Try assigning next job to each unassigned worker
        for worker in range(n):
            if mask & (1 << worker):  # Worker already assigned
                continue

            next_mask = mask | (1 << worker)
            dp[next_mask] = min(dp[next_mask],
                               dp[mask] + cost[worker][jobs_assigned])

    return dp[(1 << n) - 1]

# Example: 3 workers, 3 jobs
cost = [
    [9, 2, 7],  # Worker 0's cost for jobs 0, 1, 2
    [6, 4, 3],  # Worker 1's cost
    [5, 8, 1]   # Worker 2's cost
]
print(f"Minimum assignment cost: {min_cost_assignment(cost, 3)}")
# Optimal: Worker 0→Job 1 (2), Worker 1→Job 0 (6), Worker 2→Job 2 (1) = 9
```

**Trace on the 3×3 matrix above.** `dp[mask]` = min cost to assign the workers in `mask`, where `jobs_assigned = popcount(mask)` is the *next* job index to fill. Bit `w` set = worker `w` used.

```
cost = [[9,2,7],    # worker 0 → jobs 0,1,2
        [6,4,3],    # worker 1
        [5,8,1]]    # worker 2

dp[000] = 0                          (nothing assigned, next job = 0)

# popcount 0 → fill job 0
dp[001] = cost[0][0] = 9              (worker 0 → job 0)
dp[010] = cost[1][0] = 6              (worker 1 → job 0)
dp[100] = cost[2][0] = 5              (worker 2 → job 0)

# popcount 1 → fill job 1
dp[011] = min(9+cost[1][1]=13, 6+cost[0][1]=8) = 8    (w0,w1 used)
dp[101] = min(9+cost[2][1]=17, 5+cost[0][1]=7) = 7    (w0,w2 used)
dp[110] = min(6+cost[2][1]=14, 5+cost[1][1]=9) = 9    (w1,w2 used)

# popcount 2 → fill job 2
dp[111] = min(dp[011]+cost[2][2]=8+1=9,
              dp[101]+cost[1][2]=7+3=10,
              dp[110]+cost[0][2]=9+7=16) = 9

answer = dp[111] = 9
```

The winning path is `dp[010]=6` (w1→job0) → `dp[011]=8` (w0→job1, +2) → `dp[111]=9` (w2→job2, +1), i.e. worker 1→job 0, worker 0→job 1, worker 2→job 2 — exactly the optimum in the comment.

### Pattern 3: Partition DP

**Problem**: Merge/partition items optimally (like the merge lists problem).

**State**: `dp[mask]` = minimum cost to merge all items in `mask`

```python
def optimal_partition_dp(items, n):
    """
    Generic partition DP template.
    Find optimal way to partition/merge items.

    State: dp[mask] = (min_cost, merged_result)
    Transition: Try all ways to split mask into two parts

    Time: O(3^n) - for each mask, enumerate all submasks
    Space: O(2^n)
    """
    # dp[mask] = (cost, data)
    dp = {}

    # Base cases: single items
    for i in range(n):
        dp[1 << i] = (0, items[i])

    # Process all masks in increasing order of popcount
    for mask in range(1, 1 << n):
        if mask in dp:  # Base case
            continue

        min_cost = float('inf')
        best_result = None

        # Try all ways to partition mask
        submask = mask
        while submask > 0:
            complement = mask ^ submask

            # Both parts must be non-empty and computed
            if complement > 0 and submask in dp and complement in dp:
                cost1, data1 = dp[submask]
                cost2, data2 = dp[complement]

                # Cost to merge these two parts
                merge_cost = compute_merge_cost(data1, data2)
                total_cost = cost1 + cost2 + merge_cost

                if total_cost < min_cost:
                    min_cost = total_cost
                    best_result = merge_data(data1, data2)

            submask = (submask - 1) & mask

        if best_result is not None:
            dp[mask] = (min_cost, best_result)

    full_mask = (1 << n) - 1
    return dp[full_mask][0]

# Helper functions (problem-specific)
def compute_merge_cost(data1, data2):
    # Example: cost based on sizes and medians
    return len(data1) + len(data2) + abs(median(data1) - median(data2))

def merge_data(data1, data2):
    # Merge sorted lists, concatenate, etc.
    return sorted(data1 + data2)
```

### Problem 698 — Partition to K Equal Sum Subsets

**Difficulty**: Medium · **This template solves**: the [Assignment `dp[mask]`](#pattern-2-assignment-problem) state (which items used) with a "fill one bucket at a time" transition.

> Given `nums` and integer `k`, return `true` if you can divide `nums` into `k` **non-empty** subsets whose sums are all equal.

If a valid split exists, every bucket sums to `target = sum(nums) / k`. The state `dp[mask]` answers "using exactly the items in `mask`, what is the fill level of the bucket currently being built, taken mod `target`?" Adding items greedily fills bucket 1 to `target`, then `mod target` resets to 0 and the next item starts bucket 2 — so `k` separate buckets are tracked implicitly by the running total, never as `k` explicit sets.

```python
class Solution:
    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        total = sum(nums)
        if total % k:
            return False
        target = total // k
        n = len(nums)
        nums.sort(reverse=True)
        if nums[0] > target:
            return False

        full = (1 << n) - 1
        # dp[mask] = fill level of current bucket (mod target) using items in mask; -1 = unreachable
        dp = [-1] * (1 << n)
        dp[0] = 0
        for mask in range(1 << n):
            if dp[mask] == -1:
                continue
            for i in range(n):
                if mask & (1 << i):
                    continue
                if dp[mask] + nums[i] <= target:          # item fits current bucket
                    nxt = mask | (1 << i)
                    if dp[nxt] == -1:
                        dp[nxt] = (dp[mask] + nums[i]) % target
        return dp[full] == 0
```

**Trace** on `nums = [4,3,2,3,5,2,1]`, `k = 4` → `total = 20`, `target = 5`. A bucket closes each time the running sum hits 5 (mod 5 → 0). Reaching `dp[full] == 0` means all items placed with the last bucket exactly closed:

```
5            = {5}
4+1          = {4,1}
3+2          = {3,2}
3+2          = {3,2}          four buckets, each sums to 5 → dp[1111111] = 0 → True
```

`canPartitionKSubsets([1,2,3,4], 3)` → `total = 10`, not divisible by 3 → `False` immediately.

`★ Insight ─────────────────────────────────────`
- The `% target` is the whole trick: one scalar tracks *which bucket* you're filling AND *how full* it is. When the running total crosses a multiple of `target`, the modulo silently "starts the next bucket" — so `dp[mask]` needs only `2^n` entries, not `2^n · k`.
- Sort descending + prune `nums[0] > target` kills the exponential early: the biggest item must fit in a bucket, and large-first packing fails fast. Same idea powers the backtracking solution, but here it just trims the DP.
`─────────────────────────────────────────────────`

### Problem 2305 — Fair Distribution of Cookies

**Difficulty**: Medium · **This template solves**: the [Partition DP](#pattern-3-partition-dp) submask enumeration — split a set among `k` recipients.

> You have `n` bags of cookies (`cookies[i]`). Distribute **all** bags to `k` children; each bag goes to one child. A child's *unfairness* is the total cookies they get. Minimize the **maximum** unfairness across the `k` children.

Now the mask is "the set of bags still to hand out," and we hand child `j` some **submask** `s` of what's left. State `dp[j][mask]` = min possible max-unfairness after giving bags `mask` to the first `j` children. For each child, enumerate every submask `s` of `mask` as that child's haul.

```python
class Solution:
    def distributeCookies(self, cookies: list[int], k: int) -> int:
        n = len(cookies)
        full = (1 << n) - 1

        # Precompute sum of every submask in O(2^n) via lowest-bit recurrence.
        tot = [0] * (1 << n)
        for mask in range(1, 1 << n):
            low = mask & -mask
            i = low.bit_length() - 1
            tot[mask] = tot[mask ^ low] + cookies[i]

        INF = float('inf')
        dp = [[INF] * (1 << n) for _ in range(k + 1)]
        dp[0][0] = 0
        for j in range(1, k + 1):
            for mask in range(1 << n):
                s = mask
                while True:                     # every submask s of mask = child j's haul
                    if dp[j - 1][mask ^ s] != INF:
                        dp[j][mask] = min(dp[j][mask], max(dp[j - 1][mask ^ s], tot[s]))
                    if s == 0:
                        break
                    s = (s - 1) & mask
        return dp[k][full]
```

**Trace** on `cookies = [8,15,10,20,8]`, `k = 2`. Total = 61. Best split hands one child three bags summing to 30 and the other two summing to 31 → max = **31** (returned). With `k = 3` on `[6,1,3,2,2,4,1,2]` the optimum max is **7**.

`★ Insight ─────────────────────────────────────`
- 698 fixed each group's target and asked feasibility; 2305 has no target and **minimizes the max** — so the objective is `max(previous_children, this_child)`, not a sum. Same submask machinery, different combine operator.
- The `tot[mask] = tot[mask ^ lowbit] + cookies[i]` precompute is the reusable idiom: subset sums for all `2^n` masks in O(2^n), by peeling the lowest set bit off an already-computed smaller mask. The submask loop then costs O(3^n) overall (each mask visits its submasks).
`─────────────────────────────────────────────────`

### Pattern 4: Maximum Independent Set

**Problem**: Select maximum subset with no two adjacent elements.

```python
def max_independent_set(adj, n):
    """
    Find maximum independent set in a graph.

    State: dp[mask] = max independent set size for nodes in mask
    Constraint: No two selected nodes can be adjacent

    Time: O(2^n * n^2)
    Space: O(2^n)
    """
    dp = [0] * (1 << n)

    # Check all subsets
    for mask in range(1 << n):
        # Check if mask is an independent set
        is_independent = True
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            for j in range(i + 1, n):
                if not (mask & (1 << j)):
                    continue
                if adj[i][j]:  # i and j are adjacent
                    is_independent = False
                    break
            if not is_independent:
                break

        if is_independent:
            dp[mask] = bin(mask).count('1')
        else:
            # Try removing one node
            for i in range(n):
                if mask & (1 << i):
                    dp[mask] = max(dp[mask], dp[mask ^ (1 << i)])

    return dp[(1 << n) - 1]

# Example: Graph with 4 nodes
adj = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
]
print(f"Max independent set size: {max_independent_set(adj, 4)}")
# Optimal: nodes {0, 3} or {1, 2}, size = 2
```

---

## 4. Advanced Bit Tricks

### Isolation and Manipulation

```python
# ============================================
# ISOLATE AND MANIPULATE SPECIFIC BITS
# ============================================

# Isolate rightmost 1-bit
def rightmost_1(x):
    return x & -x
    # 10110 → 00010

# Isolate rightmost 0-bit (turn it to 1)
def rightmost_0(x):
    return ~x & (x + 1)
    # 10101 → 00010

# Turn off rightmost 1-bit
def turn_off_rightmost_1(x):
    return x & (x - 1)
    # 10110 → 10100

# Turn on rightmost 0-bit
def turn_on_rightmost_0(x):
    return x | (x + 1)
    # 10101 → 10111

# Isolate rightmost block of 1s
def rightmost_block(x):
    return x ^ (x - 1)
    # 10111000 → 00000111 (last block of 1s)

# Turn off rightmost block of 1s
def turn_off_block(x):
    return x & (x + 1)
    # 10111000 → 10000000
```

### Swap and Reverse

```python
# ============================================
# SWAP AND REVERSE BITS
# ============================================

def swap_bits(x, i, j):
    """Swap bits at positions i and j"""
    if ((x >> i) & 1) != ((x >> j) & 1):
        x ^= (1 << i) | (1 << j)
    return x

def reverse_bits(x, width=32):
    """Reverse bits of a number"""
    result = 0
    for _ in range(width):
        result = (result << 1) | (x & 1)
        x >>= 1
    return result

# Example
x = 0b10110
print(f"Original: {x:05b}")
x = swap_bits(x, 1, 3)
print(f"After swapping bits 1 and 3: {x:05b}")

x = 0b10110
print(f"Reversed (5 bits): {reverse_bits(x, 5):05b}")
```

### Gray Code

```python
# ============================================
# GRAY CODE GENERATION
# ============================================

def gray_code(n):
    """
    Generate all 2^n Gray codes.
    Gray code: Adjacent codes differ by exactly 1 bit.

    Formula: gray(i) = i XOR (i >> 1)
    """
    return [i ^ (i >> 1) for i in range(1 << n)]

def inverse_gray(gray):
    """Convert Gray code back to binary"""
    binary = gray
    gray >>= 1
    while gray:
        binary ^= gray
        gray >>= 1
    return binary

# Example: 3-bit Gray codes
codes = gray_code(3)
print("Gray codes:")
for i, code in enumerate(codes):
    print(f"{i:03b} → {code:03b} (Gray)")

# Verify adjacent codes differ by 1 bit
for i in range(len(codes) - 1):
    diff = codes[i] ^ codes[i + 1]
    assert bin(diff).count('1') == 1, "Not a valid Gray code!"
```

---

## 5. SOS (Sum Over Subsets) DP

### Standard SOS DP

**Problem**: For each mask, compute sum of values over all its submasks.

**Naive**: O(3^n) - for each mask, enumerate all submasks
**SOS DP**: O(n × 2^n) - much faster!

```python
def sos_dp(arr, n):
    """
    Sum Over Subsets DP.

    For each mask, compute: dp[mask] = Σ arr[submask] for all submasks of mask

    Key idea: Build up by considering one bit at a time.
    For bit i, dp[mask] = dp[mask with bit i off] + (dp[mask] if bit i is set)

    Time: O(n * 2^n)
    Space: O(2^n)
    """
    # Initialize with original array
    dp = arr[:]

    # For each bit position
    for i in range(n):
        # For each mask
        for mask in range(1 << n):
            # If bit i is set in mask
            if mask & (1 << i):
                # Add contribution from mask with bit i turned off
                dp[mask] += dp[mask ^ (1 << i)]

    return dp

# Example: Count number of submasks for each mask
n = 4
count = [1] * (1 << n)  # Each mask has itself as a submask
result = sos_dp(count, n)

print("Number of submasks (including self):")
for mask in range(1 << n):
    print(f"{mask:04b} ({mask:2d}) has {result[mask]:2d} submasks")

# Verification
for mask in range(1 << n):
    expected = 1 << bin(mask).count('1')  # 2^k where k = popcount
    assert result[mask] == expected
```

### Problem 1178 — Number of Valid Words for Each Puzzle

**Difficulty**: Hard · **This template solves**: [submask enumeration](#iterate-all-submasks) as a "sum over submasks" query (the problem SOS DP generalizes).

> A word is **valid** for a puzzle if (1) it contains the puzzle's **first** letter, and (2) every letter of the word appears in the puzzle. For each puzzle, return how many words are valid. (Only lowercase a–z; a puzzle has 7 distinct letters.)

Represent each word by a 26-bit mask of its distinct letters (order/count irrelevant). A word is valid for puzzle `P` iff `wordmask` is a **submask** of `puzzlemask` **and** contains the first-letter bit. Since a puzzle has only 7 letters, it has just `2^7 = 128` submasks — so for each puzzle, enumerate its submasks and sum the precomputed word-frequency of each.

```python
from collections import Counter

class Solution:
    def findNumOfValidWords(self, words: list[str], puzzles: list[str]) -> list[int]:
        cnt = Counter()
        for w in words:
            m = 0
            for c in w:
                m |= 1 << (ord(c) - 97)   # distinct-letter mask
            cnt[m] += 1

        res = []
        for p in puzzles:
            first = 1 << (ord(p[0]) - 97)
            pmask = 0
            for c in p:
                pmask |= 1 << (ord(c) - 97)

            total = 0
            sub = pmask                    # enumerate submasks of the 7-letter puzzle
            while True:
                if sub & first:            # must contain first letter
                    total += cnt.get(sub, 0)
                if sub == 0:
                    break
                sub = (sub - 1) & pmask
            res.append(total)
        return res
```

**Trace** the counting idea on puzzle `"aboveyz"` (first letter `a`). Its letter set is `{a,b,e,o,v,y,z}`. Word `"aaaa"` → mask `{a}`, which is a submask containing `a` → counts. Word `"asas"` → mask `{a,s}`; `s` ∉ puzzle → not a submask → excluded. Over the sample the result is `[1, 1, 3, 2, 4, 0]`.

`★ Insight ─────────────────────────────────────`
- Flip the naive "for each word, test each puzzle" (O(W·P)) into "for each puzzle, look up submasks" (O(P · 2^7)). The bound comes from the *puzzle* side being fixed at 7 letters — the submask count is constant, independent of word count.
- The `if sub & first` guard replaces condition (1). Every submask of `pmask` automatically satisfies condition (2), so the two rules collapse to one submask walk plus a single bit test — the same shape SOS DP would compute in bulk if puzzles shared masks.
`─────────────────────────────────────────────────`

### Inverse SOS (Sum Over Supersets)

```python
def superset_dp(arr, n):
    """
    For each mask, compute sum over all supersets.

    Time: O(n * 2^n)
    """
    dp = arr[:]

    for i in range(n):
        for mask in range(1 << n):
            # If bit i is NOT set
            if not (mask & (1 << i)):
                # Add contribution from mask with bit i turned on
                dp[mask] += dp[mask | (1 << i)]

    return dp

# Example
n = 3
arr = [i for i in range(1 << n)]
result = superset_dp(arr, n)

print("Sum over supersets:")
for mask in range(1 << n):
    print(f"{mask:03b}: sum = {result[mask]}")
```

### Applications of SOS DP

```python
# ============================================
# APPLICATION 1: COUNT SUBSETS WITH PROPERTY
# ============================================

def count_subsets_with_and_zero(arr, n):
    """
    Count pairs (i, j) where arr[i] & arr[j] == 0.

    Approach: For each arr[i], count how many arr[j] are subsets of ~arr[i]
    """
    max_val = max(arr)
    bits = max_val.bit_length()

    # Count frequency of each value
    freq = [0] * (1 << bits)
    for x in arr:
        freq[x] += 1

    # SOS DP to get count of all submasks
    sos = sos_dp(freq, bits)

    # For each element, count compatible elements
    count = 0
    for x in arr:
        complement = ((1 << bits) - 1) ^ x  # All bits flipped
        count += sos[complement]
        if x == 0:  # Don't count self-pair
            count -= 1

    return count // 2  # Each pair counted twice


# ============================================
# APPLICATION 2: MAXIMUM XOR SUBSET
# ============================================

def max_xor_subset(nums):
    """
    Find subset with maximum XOR value.
    Uses Gaussian elimination on bit vectors.

    Time: O(n * log(MAX))
    """
    basis = []

    for num in nums:
        cur = num
        # Try to reduce cur using existing basis vectors
        for b in basis:
            cur = min(cur, cur ^ b)

        if cur != 0:
            basis.append(cur)
            basis.sort(reverse=True)

    # Greedily build the max XOR: take a basis vector only if it
    # turns ON a bit that is still off (i.e. increases the result).
    # basis is sorted high-bit-first, so this locks in every high bit.
    result = 0
    for b in basis:
        result = max(result, result ^ b)

    return result
```

---

## 6. Common Problem Templates

### Template 1: Subset Selection DP

```python
def subset_selection_template(items, n):
    """
    Choose optimal subset of items.

    State: dp[mask] = optimal value for subset represented by mask
    """
    dp = [0] * (1 << n)

    # Base case
    dp[0] = 0  # Empty subset

    # Fill DP table
    for mask in range(1 << n):
        # Option 1: Try adding each item not in mask
        for i in range(n):
            if mask & (1 << i):
                continue

            next_mask = mask | (1 << i)
            dp[next_mask] = max(dp[next_mask],
                               dp[mask] + items[i])

        # Option 2: Transition from submasks
        # dp[mask] = max over all submasks

    return dp[(1 << n) - 1]
```

### Template 2: Position-Based DP

```python
def position_based_template(items, n):
    """
    Track both subset AND current position.

    State: dp[mask][pos] = optimal value for subset mask, currently at pos
    Common in TSP, Hamiltonian path problems.
    """
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]

    # Base case: start at each position
    for i in range(n):
        dp[1 << i][i] = items[i]

    # Fill DP table
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue

            # Try going to next position
            for next_pos in range(n):
                if mask & (1 << next_pos):
                    continue

                next_mask = mask | (1 << next_pos)
                transition_cost = cost(last, next_pos)
                dp[next_mask][next_pos] = min(
                    dp[next_mask][next_pos],
                    dp[mask][last] + transition_cost
                )

    # Return best ending position
    full_mask = (1 << n) - 1
    return min(dp[full_mask])
```

### Template 3: Profile DP (Grid Problems)

```python
def profile_dp_template(n, m):
    """
    Use bitmask to represent state of one dimension (column/row).
    Common in tiling problems.

    State: dp[col][profile] = ways to tile up to column col
           profile = bitmask representing which cells extend to next column

    Time: O(n * m * 2^m)
    """
    dp = [{} for _ in range(m + 1)]
    dp[0][0] = 1  # Base: empty grid

    for col in range(m):
        for profile, ways in dp[col].items():
            # Generate next profiles by filling current column
            fill_column(n, col, profile, 0, 0, ways, dp[col + 1])

    # Final state: no cells extending beyond last column
    return dp[m].get(0, 0)

def fill_column(rows, col, cur_profile, row, next_profile, ways, next_dp):
    """Recursively fill one column, generating next profile."""
    if row == rows:
        # Finished filling this column
        next_dp[next_profile] = next_dp.get(next_profile, 0) + ways
        return

    if cur_profile & (1 << row):
        # Cell already filled from previous column
        fill_column(rows, col, cur_profile, row + 1,
                   next_profile, ways, next_dp)
    else:
        # Option 1: Place vertical tile (occupies this and next row)
        if row + 1 < rows and not (cur_profile & (1 << (row + 1))):
            fill_column(rows, col, cur_profile | (1 << (row + 1)),
                       row + 2, next_profile, ways, next_dp)

        # Option 2: Place horizontal tile (extends to next column)
        fill_column(rows, col, cur_profile, row + 1,
                   next_profile | (1 << row), ways, next_dp)
```

---

## 7. Practice Problems

### Beginner Level

| LC # | Problem | Technique | Key move |
|------|---------|-----------|----------|
| **78** | Subsets | Subset enumeration | `for mask in range(1<<n)` |
| **461** | Hamming Distance | Bit counting | `popcount(a ^ b)` |
| **136** | Single Number | XOR properties | `a ^ a = 0`, XOR all |
| **231** | Power of Two | Bit check | `n & (n-1) == 0` |
| **338** | Counting Bits | DP on bits | `dp[i] = dp[i>>1] + (i&1)` |

### Intermediate Level

| LC # | Problem | Technique | Key move |
|------|---------|-----------|----------|
| **698** | Partition to K Equal Sum Subsets | Bitmask DP | `dp[mask]` = bucket fill mod target |
| **2305** | Fair Distribution of Cookies | Submask partition DP | split `mask` among `k`, min-max |
| **1125** | Smallest Sufficient Team | Subset-cover DP | `dp[skillmask]` = min team |
| **473** | Matchsticks to Square | Bitmask DP (k=4) | 698 with fixed `k=4` |

### Advanced Level

| LC # | Problem | Technique | Key move |
|------|---------|-----------|----------|
| **847** | Shortest Path Visiting All Nodes | TSP `dp[mask][last]` | multi-source BFS over `(mask,node)` |
| **943** | Find the Shortest Superstring | TSP + overlap weights | `dp[mask][last]` on overlaps |
| **1178** | Number of Valid Words for Each Puzzle | Submask / SOS query | submasks of 7-letter puzzle |
| **1349** | Maximum Students Taking Exam | Profile DP | `dp[row][seatmask]`, check adjacency |
| **1707** | Maximum XOR With an Element From Array | XOR (linear) basis / trie | greedy high-bit basis |

---

## Complexity Quick Reference

| Technique | Time Complexity | Use Case |
|-----------|-----------------|----------|
| Iterate all subsets | O(2^n) | Basic enumeration |
| Iterate all submasks | O(3^n) total | Partition problems |
| SOS DP | O(n × 2^n) | Sum over subsets |
| Gosper's hack | O(C(n,k)) | k-element subsets |
| TSP DP | O(2^n × n²) | Shortest Hamiltonian path |
| Assignment DP | O(2^n × n) | Matching problems |
| Profile DP | O(n × m × 2^m) | Grid tiling |

**Practical Limits**:
- n ≤ 20: Safe for most bitmask DP (2^20 ≈ 1M)
- n ≤ 22: Feasible with optimization (2^22 ≈ 4M)
- n ≤ 24: Cutting edge (2^24 ≈ 16M, need good constants)
- n > 24: Consider meet-in-the-middle or other techniques

---

## Which Bitmask Pattern Do I Need?

| The task is... | Pattern | State / loop | Cost |
|----------------|---------|--------------|------|
| List every subset of `n` items | **Subset enumeration** | `for mask in range(1<<n)` | O(2^n) |
| Pick a best subset under per-item values/constraints | **Subset-sum / value DP** | `dp[mask]`, add one bit at a time | O(2^n · n) |
| Order all items (visit/assign in sequence), cost depends on last | **TSP / permutation-over-mask** | `dp[mask][last]` | O(2^n · n²) |
| Split a set into two groups and recurse on each | **Submask enumeration** | `sub = (sub-1) & mask` | O(3^n) total |
| Aggregate a value over all submasks of every mask | **SOS DP** | bit-by-bit sweep | O(n · 2^n) |

Quick tell: if only *which items* matters → `dp[mask]`; if *the order/last item* matters → `dp[mask][last]`; if you must *partition* a set → submask loop.

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `1 << n` vs `1 << (n-1)` off-by-one | full mask wrong / last item dropped | full set is `(1 << n) - 1`; there are `1 << n` masks (`0 .. 2^n-1`) |
| Missing parentheses in `mask >> i & 1` | wrong bit tested — `&` binds *looser* than `>>` here, but relational/`in` mixes bite you | always write `(mask >> i) & 1` |
| Iterating submasks with `while sub > 0` | the empty submask `0` is skipped | use the `while True: ... if sub==0: break; sub=(sub-1)&mask` form when `0` matters |
| Wrong submask step (e.g. `sub-1` alone) | visits masks that aren't submasks | the step is exactly `sub = (sub - 1) & mask` |
| Integer vs set confusion | `mask + (1<<i)` when bit `i` may already be set corrupts state | add with OR: `mask | (1 << i)`; test with `(mask >> i) & 1` |
| Forgetting the base case | `dp[full]` stays `INF` | set `dp[0]=0` (subset DP) or `dp[1<<start][start]=0` (TSP) |

---

## Key Takeaways

1. **Bitmask = Subset**: n-bit integer represents subset of n elements
2. **Submask enumeration** is O(3^n) total: `submask = (submask - 1) & mask`
3. **SOS DP** reduces O(3^n) to O(n × 2^n) for subset aggregation
4. **Common patterns**:
   - Selection: dp[mask]
   - Ordering: dp[mask][pos]
   - Partitioning: enumerate submask pairs
5. **Bit tricks** provide O(1) set operations
6. **Practical limit**: n ≤ 20-24 elements

**When to use**:
- Small n (≤ 20-24)
- Need to track "which elements used"
- Subset/combination problems
- Optimization over all possible states

**When NOT to use**:
- Large n (> 25)
- Continuous/infinite state space
- Problems better solved with greedy/graph algorithms

---

## Additional Resources

- **CSES**: Hamiltonian Flights, Elevator Rides
- **Codeforces**: Bitmask DP tutorial by -is-this-fft-
- **CP Handbook**: Chapter on Bitmask DP
- **AtCoder DP Contest**: Problems M, O, X use bitmasks

---

## THREE MOVES BEHIND EVERY BITMASK PROBLEM

```
1. ENCODE   — make the mask the state key
              "which items are chosen/visited" = the bits of one integer.
              n ≤ ~20, and identity (not just count) must matter.

2. TRANSITION — add one bit, or split into submasks
              dp[mask]        : add an unused item      mask | (1 << i)
              dp[mask][last]  : move to a new position   (order matters)
              submask loop    : hand a group away        s = (s-1) & mask

3. AGGREGATE — sum / min / max / count over masks
              feasibility (698), min-max (2305), shortest (847),
              count-over-submasks (1178, SOS).
```

**Decision in one line**: only *which items* matters → `dp[mask]`; *order or current position* matters → `dp[mask][last]`; must *partition* a set → submask loop; *aggregate over all submasks* → SOS DP.

---

*Pattern mastered — stop enumerating permutations; let the bits of one integer be the set, and fill the table once.* 🚀
