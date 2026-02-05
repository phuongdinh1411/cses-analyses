---
layout: simple
title: "Planets Queries II - Distance in Functional Graphs"
permalink: /problem_soulutions/graph_algorithms/planets_queries_ii_analysis
difficulty: Hard
tags: [graph, functional-graph, binary-lifting, cycle]
cses_link: https://cses.fi/problemset/task/1160
---

# Planets Queries II - Distance in Functional Graphs

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find minimum teleports from planet a to reach planet b |
| Input | n planets with teleporters, q queries (a, b) |
| Output | Minimum steps from a to b, or -1 if unreachable |
| Constraints | n, q <= 2x10^5 |
| Core Technique | Binary Lifting + Cycle Detection |
| Time Complexity | O(n log n) preprocess, O(log n) per query |

## Learning Goals

1. **Distance in Functional Graphs**: Computing shortest path when each node has exactly one successor
2. **Handling Cycles**: Detecting cycles and computing distances within/around them
3. **Binary Lifting for Distance**: Using binary lifting to check if b lies on the path from a

## Problem Statement

You are given n planets numbered 1 to n. Each planet i has a teleporter to planet t[i]. For q queries (a, b), find the minimum teleportations from a to b, or -1 if unreachable.

**Example**:
```
Input: n=4, t=[2,1,4,3], queries: (1,2), (3,1)
Output: 1, -1

Explanation:
- 1->2 (1 step), planets 1,2 form cycle
- 3->4->3... never reaches 1 (different component)
```

## Key Insight: Reachability in Functional Graphs

In a functional graph, from node a you can only reach nodes "ahead" on your path:

```
a --> x1 --> x2 --> ... --> [cycle entry] --> c1 --> c2 --> ... (repeats)

Reachable from a: all nodes on this path (tail + cycle)
NOT reachable: any other node
```

## Cases to Handle

```
CASE 1: Both in same cycle
  Distance = (pos_b - pos_a + cycle_len) % cycle_len

CASE 2: a on tail, b in cycle (same component)
  Distance = dist_to_cycle(a) + distance_in_cycle(entry, b)

CASE 3: Both on tail (b between a and cycle)
  Distance = dist_to_cycle(a) - dist_to_cycle(b)
  (verify b is actually on path from a)

CASE 4: Unreachable (-1)
  - Different components
  - a in cycle, b on tail
  - b is "behind" a on tail (farther from cycle)
```

## Visual Diagram

```
Example: t = [2, 1, 4, 4] (1-indexed)

    1 <--> 2  (cycle, length 2)

    3 --> 4   (4 self-loop)
          ^
          |
         cycle

Node info:
  1: in_cycle, pos=0, cycle_id=0
  2: in_cycle, pos=1, cycle_id=0
  3: tail, dist=1, entry=4, cycle_id=1
  4: in_cycle, pos=0, cycle_id=1
```

## Dry Run

```
Input: n=4, t=[2, 1, 4, 4]

Query (1, 2): Both in cycle 0
  dist = (1 - 0 + 2) % 2 = 1

Query (2, 1): Both in cycle 0
  dist = (0 - 1 + 2) % 2 = 1

Query (3, 4): 3=tail, 4=cycle
  dist_to_cycle[3] = 1, entry = 4 = b
  dist = 1 + 0 = 1

Query (1, 3): 1=cycle, 3=tail
  Cannot reach tail from cycle: -1

Query (3, 2): Different components
  cycle_id[3]=1, cycle_id[2]=0: -1
```

## Python Solution

```python
import sys

def solve():
  data = sys.stdin.read().split()
  idx = 0
  n, q = int(data[idx]), int(data[idx + 1])
  idx += 2
  t = [int(data[idx + i]) - 1 for i in range(n)]
  idx += n

  LOG = 18
  jump = [[0] * n for _ in range(LOG)]
  for i in range(n):
    jump[0][i] = t[i]
  for j in range(1, LOG):
    for i in range(n):
      jump[j][i] = jump[j-1][jump[j-1][i]]

  color = [0] * n
  in_cycle = [False] * n
  cycle_id = [-1] * n
  cycle_pos = [-1] * n
  cycle_len = [0] * n
  dist_to_cycle = [0] * n
  cycle_entry = [-1] * n
  num_cycles = 0

  for start in range(n):
    if color[start]: continue
    path = []
    node = start
    while color[node] == 0:
      color[node] = 1
      path.append(node)
      node = t[node]

    if color[node] == 1:
      csi = path.index(node)
      clen = len(path) - csi
      for i in range(csi, len(path)):
        cn = path[i]
        in_cycle[cn] = True
        cycle_id[cn] = num_cycles
        cycle_pos[cn] = i - csi
        cycle_len[cn] = clen
        cycle_entry[cn] = cn
        color[cn] = 2
      for i in range(csi - 1, -1, -1):
        tn = path[i]
        cycle_id[tn] = num_cycles
        dist_to_cycle[tn] = csi - i
        cycle_entry[tn] = path[csi]
        cycle_len[tn] = clen
        color[tn] = 2
      num_cycles += 1
    else:
      for i in range(len(path) - 1, -1, -1):
        tn = path[i]
        nxt = t[tn]
        cycle_id[tn] = cycle_id[nxt]
        dist_to_cycle[tn] = dist_to_cycle[nxt] + 1
        cycle_entry[tn] = cycle_entry[nxt]
        cycle_len[tn] = cycle_len[nxt]
        color[tn] = 2

  def kth(node, k):
    for j in range(LOG):
      if k & (1 << j):
        node = jump[j][node]
    return node

  results = []
  for _ in range(q):
    a, b = int(data[idx]) - 1, int(data[idx + 1]) - 1
    idx += 2

    if a == b:
      results.append(0)
    elif cycle_id[a] != cycle_id[b]:
      results.append(-1)
    elif not in_cycle[b]:
      if not in_cycle[a]:
        d = dist_to_cycle[a] - dist_to_cycle[b]
        results.append(d if d > 0 and kth(a, d) == b else -1)
      else:
        results.append(-1)
    elif in_cycle[a]:
      d = (cycle_pos[b] - cycle_pos[a] + cycle_len[a]) % cycle_len[a]
      results.append(d if d else cycle_len[a])
    else:
      d1 = dist_to_cycle[a]
      d2 = (cycle_pos[b] - cycle_pos[cycle_entry[a]] + cycle_len[a]) % cycle_len[a]
      results.append(d1 + d2)

  print('\n'.join(map(str, results)))

if __name__ == "__main__":
  solve()
```

## Complexity Analysis

| Phase | Time | Space |
|-------|------|-------|
| Binary Lifting | O(n log n) | O(n log n) |
| Cycle Detection | O(n) | O(n) |
| Per Query | O(log n) | O(1) |
| **Total** | **O(n log n + q log n)** | **O(n log n)** |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not checking different components | Return -1 if cycle_id differs |
| Returning cycle_len when a == b | Return 0 for same node |
| Cycle nodes trying to reach tail | Return -1 (impossible) |
| Wrong cycle distance formula | Use (pos_b - pos_a + len) % len |
| Not verifying tail reachability | Use kth_successor to confirm |

## Key Takeaways

1. **Functional graphs = rho-shaped**: tail leading to exactly one cycle
2. **Reachability is one-directional**: only forward on your path
3. **Precompute everything**: cycle membership, position, distance to cycle
4. **Binary lifting dual use**: fast k-th successor + reachability verification

## Related Problems

| Problem | Key Difference |
|---------|----------------|
| [Planets Queries I](https://cses.fi/problemset/task/1750) | k-th successor, no reachability |
| [Planets Cycles](https://cses.fi/problemset/task/1751) | Cycle length computation |
| [Company Queries I](https://cses.fi/problemset/task/1687) | Trees, no cycles |
