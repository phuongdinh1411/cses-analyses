---
layout: simple
title: "Cycle Finding - Negative Cycle Detection with Bellman-Ford"
permalink: /problem_soulutions/graph_algorithms/cycle_finding_analysis
difficulty: Medium
tags: [graph, bellman-ford, negative-cycle, shortest-path]
cses_link: https://cses.fi/problemset/task/1197
---

# Cycle Finding - Negative Cycle Detection with Bellman-Ford

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find a negative cycle in a directed weighted graph |
| Algorithm | Bellman-Ford with cycle extraction |
| Time Complexity | O(n * m) |
| Space Complexity | O(n) |
| Key Insight | If relaxation occurs on nth iteration, negative cycle exists |

## Learning Goals

By completing this problem, you will understand:
1. **Bellman-Ford Algorithm**: How to find shortest paths with negative edge weights
2. **Negative Cycle Detection**: Why n-1 relaxations are sufficient and what the nth means
3. **Cycle Extraction**: How to trace back and reconstruct the actual negative cycle

## Problem Statement

Given a directed graph with `n` nodes and `m` weighted edges, find a negative cycle or report that none exists.

**Input:**
- First line: `n` (nodes) and `m` (edges)
- Next `m` lines: `a b c` representing edge from `a` to `b` with weight `c`

**Output:**
- If negative cycle exists: Print "YES" and the cycle vertices
- Otherwise: Print "NO"

**Constraints:**
- 1 <= n <= 2500
- 1 <= m <= 5000
- -10^9 <= edge weight <= 10^9

## Bellman-Ford Algorithm Basics

### Core Idea

Bellman-Ford finds shortest paths by **relaxing all edges repeatedly**:

```
Relaxation: If dist[u] + weight(u,v) < dist[v], update dist[v]
```

### Why n-1 Relaxations?

A shortest path in a graph with `n` nodes has **at most n-1 edges** (visiting each node once).

```
Iteration 1: Finds shortest paths using at most 1 edge
Iteration 2: Finds shortest paths using at most 2 edges
...
Iteration n-1: Finds shortest paths using at most n-1 edges
```

After `n-1` iterations, all shortest paths are found (if no negative cycle).

### The Key Insight for Negative Cycles

**If we can still relax an edge on the nth iteration, a negative cycle exists.**

Why? Because:
- Without negative cycles, n-1 iterations are sufficient
- If relaxation is still possible, we can keep reducing distances indefinitely
- This only happens when there's a cycle with total negative weight

## Finding the Actual Cycle

### The Tricky Part

When edge `(u, v)` relaxes on the nth iteration:
- Node `v` might NOT be on the cycle itself
- Node `v` might just be **reachable from** the cycle

**Visual Example:**
```
    Negative Cycle          Node v (relaxed)
    +-----------+
    |           |
    v           |
   [1]--(-5)-->[2]--(-3)-->[3]---->(4)---->(5)
    ^           |                           |
    |           |                           v
    +----(2)----+                    (v gets relaxed
                                     but not on cycle)
```

### Solution: Follow Parents n Times

To guarantee we're ON the cycle (not just reachable from it):

```
1. When edge (u,v) relaxes on nth iteration, start from v
2. Follow parent pointers n times (guaranteed to reach cycle)
3. From that node, trace the cycle back to itself
```

**Why n times?** The path from cycle to v has at most n-1 edges, so going back n steps guarantees we're on the cycle.

## Visual Diagram

```
Example Graph with Negative Cycle:

        1
       /|\
    (2) | (-4)
     /  |  \
    v   |   v
   [2]  |  [3]
    |   |   |
 (-3)   |  (1)
    |   |   |
    v   |   v
   [4]--+  [5]
      \   /
    (3)\ /(2)
        v
       [6]

Edges: (1,2,2), (1,3,-4), (2,4,-3), (3,5,1), (4,1,3), (5,6,2), (4,6,3)

Negative Cycle: 1 -> 2 -> 4 -> 1
Total weight: 2 + (-3) + 3 = 2  (NOT negative)

Let's use: 1 -> 3 -> 5 with different weights for negative cycle:
Edges: (1,2,1), (2,3,-2), (3,1,-1)
Cycle: 1 -> 2 -> 3 -> 1 = 1 + (-2) + (-1) = -2 (NEGATIVE!)
```

## Dry Run: Step-by-Step Example

**Graph:**
```
Nodes: 4
Edges:
  1 -> 2 (weight: 1)
  2 -> 3 (weight: -2)
  3 -> 4 (weight: 2)
  4 -> 2 (weight: -2)

Negative cycle: 2 -> 3 -> 4 -> 2 = -2 + 2 + (-2) = -2
```

**Initialization:**
```
dist = [0, INF, INF, INF, INF]  (1-indexed, node 1 as source)
parent = [-1, -1, -1, -1, -1]
```

**Iteration 1 (relaxing all edges):**
```
Edge (1,2,1):  dist[2] = min(INF, 0+1) = 1,    parent[2] = 1
Edge (2,3,-2): dist[3] = min(INF, 1-2) = -1,   parent[3] = 2
Edge (3,4,2):  dist[4] = min(INF, -1+2) = 1,   parent[4] = 3
Edge (4,2,-2): dist[2] = min(1, 1-2) = -1,     parent[2] = 4

dist = [0, INF, -1, -1, 1]
```

**Iteration 2:**
```
Edge (1,2,1):  dist[2] = min(-1, 0+1) = -1     (no change)
Edge (2,3,-2): dist[3] = min(-1, -1-2) = -3,   parent[3] = 2
Edge (3,4,2):  dist[4] = min(1, -3+2) = -1,    parent[4] = 3
Edge (4,2,-2): dist[2] = min(-1, -1-2) = -3,   parent[2] = 4

dist = [0, INF, -3, -3, -1]
```

**Iteration 3:**
```
Edge (2,3,-2): dist[3] = min(-3, -3-2) = -5,   parent[3] = 2
Edge (3,4,2):  dist[4] = min(-1, -5+2) = -3,   parent[4] = 3
Edge (4,2,-2): dist[2] = min(-3, -3-2) = -5,   parent[2] = 4

dist = [0, INF, -5, -5, -3]
```

**Iteration 4 (nth iteration - checking for negative cycle):**
```
Edge (4,2,-2): dist[2] = min(-5, -3-2) = -5    (STILL CAN RELAX!)

Negative cycle detected! Node involved: 2
```

**Extracting the cycle:**
```
Start at node 2, follow parents n=4 times:
2 -> parent[2]=4 -> parent[4]=3 -> parent[3]=2 -> parent[2]=4

After 4 steps, we're at node 4 (guaranteed on cycle)

Now trace cycle from node 4:
4 -> parent[4]=3 -> parent[3]=2 -> parent[2]=4 (back to start!)

Cycle found: 4 -> 3 -> 2 -> 4
Or equivalently: 2 -> 4 -> 3 -> 2
```

## Python Solution

```python
def find_negative_cycle(n, edges):
  """
  Find a negative cycle using Bellman-Ford algorithm.

  Args:
    n: Number of nodes (1-indexed)
    edges: List of (u, v, w) tuples representing directed edges

  Returns:
    List of nodes forming the cycle, or None if no negative cycle
  """
  INF = float('inf')
  dist = [0] * (n + 1)  # Start with all zeros (virtual source to all)
  parent = [-1] * (n + 1)

  # Run n iterations (n-1 for shortest paths, 1 more to detect cycle)
  last_relaxed = -1

  for iteration in range(n):
    last_relaxed = -1
    for u, v, w in edges:
      if dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
        parent[v] = u
        last_relaxed = v

  # No relaxation on nth iteration means no negative cycle
  if last_relaxed == -1:
    return None

  # Find a node that is definitely on the cycle
  # Go back n steps to ensure we're on the cycle
  node_on_cycle = last_relaxed
  for _ in range(n):
    node_on_cycle = parent[node_on_cycle]

  # Extract the cycle
  cycle = []
  current = node_on_cycle
  while True:
    cycle.append(current)
    current = parent[current]
    if current == node_on_cycle:
      break

  cycle.append(node_on_cycle)  # Complete the cycle
  cycle.reverse()  # Correct order

  return cycle


def solve():
  """Main solution function."""
  import sys
  input = sys.stdin.readline

  n, m = map(int, input().split())
  edges = []
  for _ in range(m):
    a, b, c = map(int, input().split())
    edges.append((a, b, c))

  cycle = find_negative_cycle(n, edges)

  if cycle is None:
    print("NO")
  else:
    print("YES")
    print(' '.join(map(str, cycle)))


if __name__ == "__main__":
  solve()
```

## Common Mistakes

### 1. Not Handling "Node Leads to Cycle" Case

**Wrong Approach:**
```python
# WRONG: Assuming last_relaxed is ON the cycle
cycle_start = last_relaxed
```

**Correct Approach:**
```python
# CORRECT: Follow parents n times to ensure we're on cycle
node_on_cycle = last_relaxed
for _ in range(n):
  node_on_cycle = parent[node_on_cycle]
```

### 2. Integer Overflow

With edge weights up to 10^9 and potentially n*weight additions, use `long long` in C++ or handle large integers in Python.

### 3. Not Initializing Distances Properly

**Issue:** If you initialize `dist[1] = 0` and others to INF, you might miss negative cycles not reachable from node 1.

**Solution:** Initialize all distances to 0 (conceptually, add a virtual source connected to all nodes with weight 0).

### 4. Wrong Cycle Direction

The parent pointers go backward. Remember to reverse the cycle for correct output order.

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Bellman-Ford (n iterations) | O(n * m) | O(n) |
| Finding node on cycle | O(n) | O(1) |
| Extracting cycle | O(n) | O(n) |
| **Total** | **O(n * m)** | **O(n)** |

## Related Problems

### CSES Problems
- [High Score](https://cses.fi/problemset/task/1673) - Longest path with negative cycles
- [Shortest Routes I](https://cses.fi/problemset/task/1671) - Dijkstra's algorithm

### LeetCode Problems
- [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) - Bellman-Ford variant with limited iterations
- [Network Delay Time](https://leetcode.com/problems/network-delay-time/) - Shortest path basics

## Key Takeaways

1. **Bellman-Ford** works with negative edges, unlike Dijkstra
2. **n-1 iterations** find all shortest paths (without negative cycles)
3. **nth iteration relaxation** proves negative cycle exists
4. **Follow parents n times** to guarantee landing on the actual cycle
5. **Initialize dist to 0** for all nodes to detect cycles anywhere in graph
