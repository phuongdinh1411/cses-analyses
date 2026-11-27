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

**Step 2: Hierholzer's Algorithm** (exactly what the code below does: try edge '0' first, then '1')
```
at 00: take edge '0' -> 00   stack = [00, 00]
at 00: take edge '1' -> 01   stack = [00, 00, 01]
at 01: take edge '0' -> 10   stack = [00, 00, 01, 10]
at 10: take edge '0' -> 00   stack = [00, 00, 01, 10, 00]
at 00: stuck, pop            path = [00]
at 10: take edge '1' -> 01   stack = [00, 00, 01, 10, 01]
at 01: take edge '1' -> 11   stack = [00, 00, 01, 10, 01, 11]
at 11: take edge '0' -> 10   stack = [00, 00, 01, 10, 01, 11, 10]
at 10: stuck, pop            path = [00, 10]
at 11: take edge '1' -> 11   stack = [00, 00, 01, 10, 01, 11, 11]
now every edge is used: pop the rest
                             path = [00, 10, 11, 11, 01, 10, 01, 00, 00]
```

The first walk got stuck back at 00 with edges still unused at 10. Hierholzer resumes from the deepest node that still has an unused edge and splices that detour into the circuit. That is the whole algorithm.

**Step 3: Build Result**
```
Circuit (path reversed): 00 -> 00 -> 01 -> 10 -> 01 -> 11 -> 11 -> 10 -> 00
Edge labels (last bit):        0     1     0     1     1     1     0     0

Result: "00" + "01011100" = "0001011100"

Check, all 8 windows of length 3 are distinct:
  000 001 010 101 011 111 110 100
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
