---
layout: simple
title: "Planets Queries I"
permalink: /problem_soulutions/graph_algorithms/planets_queries_i_analysis
difficulty: Medium
tags: [graph, binary-lifting, functional-graph, sparse-table]
cses_link: https://cses.fi/problemset/task/1750
---

# Planets Queries I

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find destination after k teleports in a functional graph |
| Input | n planets, each with one outgoing teleporter; q queries (x, k) |
| Output | Planet reached after k teleports from planet x |
| Constraints | n, q <= 2x10^5, k <= 10^9 |
| Core Technique | Binary Lifting (Sparse Table for successors) |
| Time Complexity | O(n log k) preprocessing, O(log k) per query |

## Learning Goals

1. **Binary Lifting Technique**: Precompute jumps of powers of 2 for fast k-th successor queries
2. **Functional Graphs**: Understand graphs where each node has exactly one outgoing edge
3. **Sparse Table for Successors**: Build a table where `jump[i][j]` = node reached from i after 2^j steps
4. **Bit Decomposition**: Answer queries by decomposing k into sum of powers of 2

## Problem Statement

You are given n planets numbered 1 to n. Each planet i has a teleporter that leads to planet t[i].

Given q queries, each query (x, k) asks: starting from planet x, which planet do you reach after using teleporters exactly k times?

**Input Format**:
```
n q
t[1] t[2] ... t[n]
x[1] k[1]
x[2] k[2]
...
x[q] k[q]
```

**Example**:
```
Input:
4 3
2 1 1 4
1 2
3 4
4 1

Output:
1
2
4
```

**Explanation**:
- Query (1, 2): 1 -> 2 -> 1, answer is 1
- Query (3, 4): 3 -> 1 -> 2 -> 1 -> 2, answer is 2
- Query (4, 1): 4 -> 4, answer is 4

## Key Insight: Binary Lifting

The naive approach of following k edges takes O(k) per query - too slow when k up to 10^9.

**Core Idea**: Precompute `jump[i][j]` = planet reached from planet i after exactly 2^j teleports.

Then any k can be expressed as sum of powers of 2, allowing O(log k) query time.

### Building the Jump Table

```
jump[i][0] = t[i]                           (direct successor)
jump[i][j] = jump[jump[i][j-1]][j-1]        (for j >= 1)
```

The recurrence says: to jump 2^j steps, first jump 2^(j-1) steps, then jump 2^(j-1) steps again.

## Visual Diagram: Binary Lifting Table

Consider planets with teleporters: t = [2, 3, 1, 4] (1-indexed)

```
Planet connections:
    1 --> 2 --> 3 --> 1 (cycle)
    4 --> 4 (self-loop)

Binary Lifting Table:
+--------+--------+--------+--------+--------+

| Planet | j=0    | j=1    | j=2    | j=3    |
|        | (2^0=1)| (2^1=2)| (2^2=4)| (2^3=8)|
+--------+--------+--------+--------+--------+

|   1    |   2    |   3    |   2    |   2    |
|   2    |   3    |   1    |   3    |   3    |
|   3    |   1    |   2    |   1    |   1    |
|   4    |   4    |   4    |   4    |   4    |
+--------+--------+--------+--------+--------+

Building jump[1][2] (4 steps from planet 1):
  jump[1][2] = jump[jump[1][1]][1]
             = jump[3][1]
             = 2

Verification: 1 -> 2 -> 3 -> 1 -> 2 (4 steps lands on 2)
```

## Answering Queries: Bit Decomposition

To find destination after k steps from planet x:

```
For each bit position j where bit j of k is set:
    x = jump[x][j]
Return x
```

**Example**: Query (1, 5) where k=5 = 101 in binary = 2^0 + 2^2

```
Start: x = 1
k = 5 = 101 (binary)

Bit 0 is set: x = jump[1][0] = 2
Bit 1 not set: skip
Bit 2 is set: x = jump[2][2] = 3

Answer: 3

Verification: 1 -> 2 -> 3 -> 1 -> 2 -> 3 (5 steps)
```

## Dry Run

**Input**:
```
n=4, q=2
t = [2, 1, 1, 4]  (1-indexed)
Queries: (1, 3), (3, 5)
```

**Step 1: Build jump table** (LOG = 30 for k up to 10^9)

```
j=0 (direct successors):
  jump[1][0] = 2
  jump[2][0] = 1
  jump[3][0] = 1
  jump[4][0] = 4

j=1 (2 steps):
  jump[1][1] = jump[jump[1][0]][0] = jump[2][0] = 1
  jump[2][1] = jump[jump[2][0]][0] = jump[1][0] = 2
  jump[3][1] = jump[jump[3][0]][0] = jump[1][0] = 2
  jump[4][1] = jump[jump[4][0]][0] = jump[4][0] = 4

j=2 (4 steps):
  jump[1][2] = jump[jump[1][1]][1] = jump[1][1] = 1
  jump[2][2] = jump[jump[2][1]][1] = jump[2][1] = 2
  jump[3][2] = jump[jump[3][1]][1] = jump[2][1] = 2
  jump[4][2] = jump[jump[4][1]][1] = jump[4][1] = 4
```

**Step 2: Answer queries**

Query (1, 3): k=3 = 11 in binary
- Bit 0 set: x = jump[1][0] = 2
- Bit 1 set: x = jump[2][1] = 2
- Answer: 2
- Verify: 1 -> 2 -> 1 -> 2

Query (3, 5): k=5 = 101 in binary
- Bit 0 set: x = jump[3][0] = 1
- Bit 2 set: x = jump[1][2] = 1
- Answer: 1
- Verify: 3 -> 1 -> 2 -> 1 -> 2 -> 1

## Python Solution

```python
import sys
from math import log2

def solve():
  input_data = sys.stdin.read().split()
  idx = 0

  n, q = int(input_data[idx]), int(input_data[idx + 1])
  idx += 2

  # Read teleporter destinations (convert to 0-indexed)
  t = [int(input_data[idx + i]) - 1 for i in range(n)]
  idx += n

  # LOG = number of bits needed for max k (10^9 < 2^30)
  LOG = 30

  # Build binary lifting table
  # jump[j][i] = destination from planet i after 2^j teleports
  jump = [[0] * n for _ in range(LOG)]

  # Base case: j=0, direct successors
  for i in range(n):
    jump[0][i] = t[i]

  # Fill table: jump 2^j = jump 2^(j-1) twice
  for j in range(1, LOG):
    for i in range(n):
      jump[j][i] = jump[j - 1][jump[j - 1][i]]

  # Answer queries
  results = []
  for _ in range(q):
    x, k = int(input_data[idx]) - 1, int(input_data[idx + 1])
    idx += 2

    # Decompose k into powers of 2
    for j in range(LOG):
      if k & (1 << j):
        x = jump[j][x]

    results.append(x + 1)  # Convert back to 1-indexed

  print('\n'.join(map(str, results)))

if __name__ == "__main__":
  solve()
```

## Complexity Analysis

| Phase | Time | Space |
|-------|------|-------|
| Preprocessing | O(n * log k) | O(n * log k) |
| Per Query | O(log k) | O(1) |
| Total | O(n log k + q log k) | O(n log k) |

With n, q = 2x10^5 and log k = 30:
- Preprocessing: ~6x10^6 operations
- All queries: ~6x10^6 operations
- Memory: ~6x10^6 integers (~24 MB)

## Common Mistakes

1. **Off-by-one in LOG calculation**
   - Wrong: `LOG = (int)log2(max_k)` may round down
   - Right: Use `LOG = 30` for k up to 10^9, or calculate `ceil(log2(max_k + 1))`

2. **Not handling k=0**
   - When k=0, answer is x itself (no teleports)
   - The bit decomposition loop naturally handles this (no bits set)

3. **1-indexed vs 0-indexed confusion**
   - CSES uses 1-indexed planets
   - Be consistent throughout: convert early, convert back at output

4. **Integer overflow with 1 << j**
   - In C++, use `1LL << j` if j can be >= 31
   - For this problem, k <= 10^9, so `1 << 30` suffices (but be careful)

5. **Wrong recurrence direction**
   - Wrong: `jump[i][j] = jump[jump[i][j-1]][j]`
   - Right: `jump[i][j] = jump[jump[i][j-1]][j-1]`

## Related Problems

| Problem | Technique | Key Difference |
|---------|-----------|----------------|
| [Planets Queries II](https://cses.fi/problemset/task/1160) | Binary Lifting + Cycle Detection | Find if y is reachable from x |
| [Company Queries I](https://cses.fi/problemset/task/1687) | Binary Lifting on Tree | k-th ancestor in rooted tree |
| [Company Queries II](https://cses.fi/problemset/task/1688) | Binary Lifting for LCA | Lowest Common Ancestor |
| [LeetCode 1483](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) | Binary Lifting | k-th ancestor with -1 for invalid |

## Key Takeaways

1. **Binary Lifting** is the go-to technique for k-th successor/ancestor queries
2. **Functional graphs** (each node has exactly one outgoing edge) always lead to cycles
3. **Preprocessing trade-off**: O(n log k) extra space enables O(log k) queries
4. **Bit manipulation**: Any integer k can be decomposed into O(log k) powers of 2
