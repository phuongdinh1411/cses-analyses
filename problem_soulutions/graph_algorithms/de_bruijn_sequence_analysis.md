---
layout: simple
title: "De Bruijn Sequence"
permalink: /problem_soulutions/graph_algorithms/de_bruijn_sequence_analysis
difficulty: Hard
tags: [graph, de-bruijn, eulerian-circuit, string]
cses_link: https://cses.fi/problemset/task/1692
---

# De Bruijn Sequence

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find the shortest binary string containing all n-bit patterns as substrings |
| Input | Integer n (1 <= n <= 15) |
| Output | Binary string of length 2^n + n - 1 |
| Core Technique | Eulerian circuit on de Bruijn graph |
| Time Complexity | O(2^n) |
| Space Complexity | O(2^n) |

## Learning Goals

After studying this problem, you should understand:

1. **De Bruijn Sequence**: A cyclic sequence where every possible n-length substring appears exactly once
2. **Reduction to Eulerian Circuit**: How to model string construction as a graph traversal problem
3. **Hierholzer's Algorithm**: Finding Eulerian circuits efficiently

## Problem Statement

Given an integer n, find the shortest binary string that contains every possible n-bit binary pattern as a substring.

**Example**: For n = 2, the 2-bit patterns are: 00, 01, 10, 11

One valid answer: `00110` (length 5 = 2^2 + 2 - 1)
- Position 0-1: `00`
- Position 1-2: `01`
- Position 2-3: `11`
- Position 3-4: `10`

## Key Insight: Reduction to Eulerian Circuit

The brilliant insight is to model this as a graph problem:

**Graph Construction:**
- **Nodes**: All (n-1)-bit patterns (there are 2^(n-1) nodes)
- **Edges**: Each n-bit pattern becomes a directed edge
- **Edge Rule**: Pattern "abcd" creates edge from "abc" to "bcd", labeled with 'd'

**Why Eulerian Circuit?**
- Each n-bit pattern must appear exactly once -> each edge traversed exactly once
- An Eulerian circuit visits every edge exactly once
- Finding an Eulerian circuit gives us our de Bruijn sequence

## Edge Construction Explained

For an n-bit pattern, we create an edge from its first (n-1) bits to its last (n-1) bits.

**Example for n=3, pattern "011":**
```
Pattern: 0 1 1
         -----
First 2: 0 1     -> Source node: "01"
Last 2:    1 1   -> Target node: "11"
Edge label:  1   -> The last bit
```

Edge: "01" --[1]--> "11"

This edge represents including pattern "011" in our sequence.

## Why Eulerian Circuit Exists

For an Eulerian circuit to exist, every node must have equal in-degree and out-degree.

**Proof for de Bruijn graph:**
- Each node is an (n-1)-bit pattern
- From any node "abc", there are exactly 2 outgoing edges: "abc0" and "abc1"
- To any node "abc", there are exactly 2 incoming edges: "0abc" and "1abc"
- Therefore: in-degree = out-degree = 2 for every node

Since the graph is connected and balanced, an Eulerian circuit always exists.

## Visual Diagram for n=3

```
Nodes: 2-bit patterns (00, 01, 10, 11)
Edges: 3-bit patterns

                    [0]
              +----------+
              |          |
              v          |
        +---[00]---+     |
        |    |     |     |
   [0]  |    |[1]  |     |
        |    v     |     |
        |  [01]----+     |
        |    |           |
        |    |[0]  [1]   |
        |    v      |    |
        +--[10]<----+    |
             |           |
        [0]  |[1]        |
             v           |
           [11]----------+
             |      [0]
             +------+
               [1]

Edges (3-bit patterns):
  000: 00 -> 00    100: 10 -> 00
  001: 00 -> 01    101: 10 -> 01
  010: 01 -> 10    110: 11 -> 10
  011: 01 -> 11    111: 11 -> 11
```

## Building the Result

Once we find an Eulerian circuit, the de Bruijn sequence is:

**Result = Starting node + All edge labels in order**

If circuit visits: 00 -[0]-> 00 -[1]-> 01 -[0]-> 10 -[0]-> 00 ...

Result starts with: "00" + "0" + "1" + "0" + "0" + ...

**Length**: (n-1) for starting node + 2^n edges = 2^n + n - 1

## Dry Run for n=3

**Step 1: Build Graph**
```
Nodes: {00, 01, 10, 11}
Adjacency list (each node -> list of (neighbor, edge_label)):
  00: [(00, '0'), (01, '1')]
  01: [(10, '0'), (11, '1')]
  10: [(00, '0'), (01, '1')]
  11: [(10, '0'), (11, '1')]
```

**Step 2: Hierholzer's Algorithm**
```
Start at node "00"
Stack: [00]
Path: []

Iteration 1: At 00, go to 01 via edge '1'
  Stack: [00, 01], Path: []

Iteration 2: At 01, go to 11 via edge '1'
  Stack: [00, 01, 11], Path: []

Iteration 3: At 11, go to 11 via edge '1'
  Stack: [00, 01, 11, 11], Path: []

Iteration 4: At 11, go to 10 via edge '0'
  Stack: [00, 01, 11, 11, 10], Path: []

Iteration 5: At 10, go to 01 via edge '1'
  Stack: [00, 01, 11, 11, 10, 01], Path: []

Iteration 6: At 01, go to 10 via edge '0'
  Stack: [00, 01, 11, 11, 10, 01, 10], Path: []

Iteration 7: At 10, go to 00 via edge '0'
  Stack: [00, 01, 11, 11, 10, 01, 10, 00], Path: []

Iteration 8: At 00, go to 00 via edge '0'
  Stack: [00, 01, 11, 11, 10, 01, 10, 00, 00], Path: []

Iteration 9: At 00, no more edges, pop to path
  Stack: [00, 01, 11, 11, 10, 01, 10, 00], Path: [(00, -)]

Continue popping until stack empty...
```

**Step 3: Build Result**
```
Path (reversed): 00 -> 00 -> 01 -> 10 -> 01 -> 10 -> 11 -> 11 -> 00
Edge labels:         0    1    0    1    0    1    1    0

Result: "00" + "01010110" = "0001010110"
        ^^^^   ^^^^^^^^
        start  edge labels

Verify: Contains all 3-bit patterns:
  000 at pos 0, 001 at pos 1, 010 at pos 2, 101 at pos 3
  010 at pos 4, 101 at pos 5, 011 at pos 6, 110 at pos 7

Wait - we have duplicates! Let me recalculate...
```

**Correct traversal (one valid circuit):**
```
00 -[0]-> 00 -[1]-> 01 -[1]-> 11 -[1]-> 11 -[0]-> 10 -[1]-> 01 -[0]-> 10 -[0]-> 00

Result: "00" + "01110100" = "0001110100"
```

## Python Implementation

```python
def solve():
  n = int(input())

  if n == 1:
    print("01")
    return

  # Number of (n-1)-bit patterns (nodes)
  num_nodes = 1 << (n - 1)
  mask = num_nodes - 1  # Mask for (n-1) bits

  # Each node has edges to node*2 % num_nodes (append 0)
  # and (node*2 + 1) % num_nodes (append 1)
  # We track which edges are used: edge_used[node][0] and edge_used[node][1]
  edge_used = [[False, False] for _ in range(num_nodes)]

  # Hierholzer's algorithm
  stack = [0]  # Start from node 0 (all zeros)
  path = []

  while stack:
    node = stack[-1]
    # Try edge 0, then edge 1
    if not edge_used[node][0]:
      edge_used[node][0] = True
      next_node = (node << 1) & mask  # Append 0
      stack.append(next_node)
    elif not edge_used[node][1]:
      edge_used[node][1] = True
      next_node = ((node << 1) | 1) & mask  # Append 1
      stack.append(next_node)
    else:
      path.append(stack.pop())

  # Reverse path to get correct order
  path.reverse()

  # Build result: start with first node in binary, then append edge bits
  result = []
  # First node as (n-1)-bit string
  first_node = path[0]
  for i in range(n - 2, -1, -1):
    result.append('0' if (first_node >> i) & 1 == 0 else '1')

  # For each edge in path, append the last bit of destination
  for i in range(1, len(path)):
    result.append('1' if path[i] & 1 else '0')

  print(''.join(result))

solve()
```

## Why This Works

**Correctness Proof:**

1. **Each n-bit pattern appears exactly once:**
   - Each n-bit pattern is represented by exactly one edge in the graph
   - An Eulerian circuit traverses each edge exactly once
   - Therefore, each pattern appears exactly once as a substring

2. **The result is the shortest possible:**
   - There are 2^n different n-bit patterns
   - Any string containing all of them must have at least 2^n + n - 1 characters
   - Our construction achieves exactly this length

3. **Every window of n bits is unique:**
   - When we traverse edge from node A to node B, we're adding a character
   - The n-bit window at that position is: last (n-1) bits of A + edge label
   - This exactly corresponds to the edge (the n-bit pattern)
   - Since each edge is traversed once, each window is unique

**Intuition:**
- The (n-1)-bit nodes represent "context" - what we've seen recently
- Each edge extends the context by one bit while maintaining the window size
- The Eulerian circuit ensures we use every possible extension exactly once

## Complexity Analysis

| Operation | Complexity |
|-----------|------------|
| Graph construction | O(2^n) nodes and edges |
| Hierholzer's algorithm | O(2^n) - visits each edge once |
| Result construction | O(2^n) |
| **Total Time** | **O(2^n)** |
| **Total Space** | **O(2^n)** for edge tracking |

## Related Problems

- [CSES Teleporters Path](https://cses.fi/problemset/task/1693) - Eulerian path
- [CSES Mail Delivery](https://cses.fi/problemset/task/1691) - Eulerian circuit
- [LeetCode 753: Cracking the Safe](https://leetcode.com/problems/cracking-the-safe/) - Same concept, different framing
