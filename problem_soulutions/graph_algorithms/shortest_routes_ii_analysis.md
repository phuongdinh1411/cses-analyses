---
layout: simple
title: "Shortest Routes II - Floyd-Warshall Algorithm"
permalink: /problem_soulutions/graph_algorithms/shortest_routes_ii_analysis
difficulty: Medium
tags: [graph, floyd-warshall, shortest-path, all-pairs, dp]
cses_link: https://cses.fi/problemset/task/1672
---

# Shortest Routes II - Floyd-Warshall Algorithm

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find shortest paths between all pairs of cities |
| Algorithm | Floyd-Warshall |
| Time Complexity | O(n^3) |
| Space Complexity | O(n^2) |
| Difficulty | Medium |
| Key Technique | Dynamic Programming on graphs |

## Learning Goals

After completing this problem, you will understand:
1. **Floyd-Warshall Algorithm** - The classic all-pairs shortest path algorithm
2. **All-Pairs Shortest Path** - Computing shortest distances between every pair of nodes
3. **DP on Graphs** - How dynamic programming principles apply to graph problems
4. **When to use Floyd-Warshall** - Recognizing problems suited for this approach

## Problem Statement

You are given a graph with **n cities** and **m bidirectional roads**. Each road has a length.

Your task is to process **q queries**. In each query, you need to find the shortest path length between two given cities.

**Input:**
- First line: n (cities), m (roads), q (queries)
- Next m lines: a, b, c (road between cities a and b with length c)
- Next q lines: a, b (find shortest path from a to b)

**Output:**
- For each query, print the shortest path length, or -1 if no path exists.

**Constraints:**
- 1 <= n <= 500
- 1 <= m <= n^2
- 1 <= q <= 100,000
- 1 <= a, b <= n
- 1 <= c <= 10^9

## Key Insight: The Intermediate Node Idea

The core insight of Floyd-Warshall is elegantly simple:

**For every pair (i, j), try using each node k as an intermediate stop.**

```
dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

This asks: "Is it shorter to go directly from i to j, or to go through k?"

## Why This Works: Building Up Allowed Intermediates

The algorithm considers paths that can use progressively more intermediate nodes:

```
Round k=1: Paths can only use node 1 as intermediate
Round k=2: Paths can use nodes {1, 2} as intermediates
Round k=3: Paths can use nodes {1, 2, 3} as intermediates
...
Round k=n: Paths can use any node as intermediate (optimal paths!)
```

**Mathematical Interpretation:**
- Let dist_k[i][j] = shortest path from i to j using only nodes {1, 2, ..., k} as intermediates
- Either the optimal path uses k: dist_k[i][j] = dist_{k-1}[i][k] + dist_{k-1}[k][j]
- Or it doesn't use k: dist_k[i][j] = dist_{k-1}[i][j]
- Take the minimum: dist_k[i][j] = min(dist_{k-1}[i][j], dist_{k-1}[i][k] + dist_{k-1}[k][j])

## The Algorithm: Three Nested Loops

```
for k = 1 to n:           // Try each intermediate node
    for i = 1 to n:       // For each source
        for j = 1 to n:   // For each destination
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

## CRITICAL: Loop Order Matters!

**k MUST be the outermost loop!**

Why? Because when we update dist[i][j] using node k, we need dist[i][k] and dist[k][j] to already represent the best paths using nodes {1, ..., k-1}.

```
CORRECT:                    WRONG:
for k:                      for i:
    for i:                      for j:
        for j:                      for k:
            update                      update

The wrong order gives incorrect results because we might use
dist[i][k] before it has been properly optimized!
```

## Initialization

```python
# Initialize distance matrix
dist = [[INF] * (n+1) for _ in range(n+1)]

# Distance to self is 0
for i in range(1, n+1):
 dist[i][i] = 0

# Direct edges (take minimum if multiple edges)
for a, b, c in edges:
 dist[a][b] = min(dist[a][b], c)
 dist[b][a] = min(dist[b][a], c)  # Bidirectional
```

## Visual Diagram: Path Improvement

Consider finding the shortest path from A to D:

```
Initial Graph:
    A ---5--- B
    |         |
    2         1
    |         |
    C ---1--- D

Initial distances (direct edges only):
        A    B    C    D
    A   0    5    2    INF
    B   5    0   INF   1
    C   2   INF   0    1
    D  INF   1    1    0

After k=A (use A as intermediate):
- No improvement (A is endpoint, not useful as intermediate for others)

After k=B (use B as intermediate):
- dist[A][D] = min(INF, dist[A][B] + dist[B][D]) = min(INF, 5+1) = 6
        A    B    C    D
    A   0    5    2    6    <-- improved!
    B   5    0   INF   1
    C   2   INF   0    1
    D   6    1    1    0    <-- improved!

After k=C (use C as intermediate):
- dist[A][D] = min(6, dist[A][C] + dist[C][D]) = min(6, 2+1) = 3
- dist[B][C] = min(INF, dist[B][A] + dist[A][C]) = min(INF, 5+2) = 7
        A    B    C    D
    A   0    5    2    3    <-- improved!
    B   5    0    7    1
    C   2    7    0    1
    D   3    1    1    0    <-- improved!

After k=D (use D as intermediate):
- dist[B][C] = min(7, dist[B][D] + dist[D][C]) = min(7, 1+1) = 2
        A    B    C    D
    A   0    5    2    3
    B   5    0    2    1    <-- improved!
    C   2    2    0    1    <-- improved!
    D   3    1    1    0

Final: Shortest A to D is 3 (path: A -> C -> D)
```

## Dry Run: 4-Node Example

```
Input:
n=4, m=4
Edges: (1,2,5), (1,3,9), (2,3,2), (2,4,7)

Step 1: Initialize
        1    2    3    4
    1   0    5    9   INF
    2   5    0    2    7
    3   9    2    0   INF
    4  INF   7   INF   0

Step 2: k=1 (paths through node 1)
- Check dist[2][3] via 1: dist[2][1]+dist[1][3] = 5+9 = 14 > 2, no change
- Check dist[2][4] via 1: dist[2][1]+dist[1][4] = 5+INF = INF, no change
- Check dist[3][4] via 1: dist[3][1]+dist[1][4] = 9+INF = INF, no change
No changes.

Step 3: k=2 (paths through node 2)
- dist[1][3] via 2: dist[1][2]+dist[2][3] = 5+2 = 7 < 9, UPDATE!
- dist[1][4] via 2: dist[1][2]+dist[2][4] = 5+7 = 12 < INF, UPDATE!
- dist[3][4] via 2: dist[3][2]+dist[2][4] = 2+7 = 9 < INF, UPDATE!

        1    2    3    4
    1   0    5    7   12
    2   5    0    2    7
    3   7    2    0    9
    4  12    7    9    0

Step 4: k=3 (paths through node 3)
- dist[1][4] via 3: dist[1][3]+dist[3][4] = 7+9 = 16 > 12, no change
- dist[2][4] via 3: dist[2][3]+dist[3][4] = 2+9 = 11 > 7, no change
No changes.

Step 5: k=4 (paths through node 4)
- No improvements possible.

Final distance matrix:
        1    2    3    4
    1   0    5    7   12
    2   5    0    2    7
    3   7    2    0    9
    4  12    7    9    0
```

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
 n, m, q = map(int, input().split())

 INF = float('inf')

 # Initialize distance matrix
 dist = [[INF] * (n + 1) for _ in range(n + 1)]

 # Distance to self is 0
 for i in range(1, n + 1):
  dist[i][i] = 0

 # Read edges (take minimum if multiple edges between same nodes)
 for _ in range(m):
  a, b, c = map(int, input().split())
  dist[a][b] = min(dist[a][b], c)
  dist[b][a] = min(dist[b][a], c)

 # Floyd-Warshall: k MUST be outermost loop
 for k in range(1, n + 1):
  for i in range(1, n + 1):
   for j in range(1, n + 1):
    if dist[i][k] != INF and dist[k][j] != INF:
     dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

 # Process queries
 result = []
 for _ in range(q):
  a, b = map(int, input().split())
  if dist[a][b] == INF:
   result.append(-1)
  else:
   result.append(dist[a][b])

 print('\n'.join(map(str, result)))

solve()
```

## Detecting Negative Cycles

Floyd-Warshall can detect negative cycles. After running the algorithm:

```python
# Check for negative cycles
def has_negative_cycle(dist, n):
 for i in range(1, n + 1):
  if dist[i][i] < 0:
   return True
 return False
```

**Why?** If dist[i][i] < 0, there's a path from i back to i with negative total weight - a negative cycle!

```
If a negative cycle exists through node k:
    dist[k][k] will become negative because:
    dist[k][k] = min(0, dist[k][...] + dist[...][k])
    where the path through the cycle has negative weight.
```

**Note:** The CSES problem guarantees non-negative weights, so this isn't needed here.

## Common Mistakes

### 1. Wrong Loop Order
```python
# WRONG - will give incorrect results!
for i in range(1, n + 1):
 for j in range(1, n + 1):
  for k in range(1, n + 1):
   dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

# CORRECT - k must be outermost
for k in range(1, n + 1):
 for i in range(1, n + 1):
  for j in range(1, n + 1):
   dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

### 2. Integer Overflow with Infinity
```python
# WRONG - can overflow when adding two large values
dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
# If dist[i][k] = INF and dist[k][j] = INF, sum might overflow!

# CORRECT - check for INF before adding
if dist[i][k] != INF and dist[k][j] != INF:
 dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

In C++, use `long long` and set INF = 1e18 (not INT_MAX which causes overflow).

### 3. Forgetting Multiple Edges
```python
# WRONG - overwrites previous edge
dist[a][b] = c

# CORRECT - take minimum of multiple edges
dist[a][b] = min(dist[a][b], c)
```

### 4. Off-by-One with 1-indexed Input
```python
# WRONG if input is 1-indexed
dist = [[INF] * n for _ in range(n)]  # indices 0 to n-1

# CORRECT for 1-indexed input
dist = [[INF] * (n + 1) for _ in range(n + 1)]  # indices 0 to n
```

## When to Use Floyd-Warshall

**Use Floyd-Warshall when:**
- You need shortest paths between ALL pairs of nodes
- n is small (n <= 500)
- You have many queries asking for different source-destination pairs
- Negative edge weights are present (but no negative cycles)
- Simple implementation is preferred over Dijkstra from every node

**Don't use Floyd-Warshall when:**
- n is large (> 500) - O(n^3) becomes too slow
- You only need single-source shortest paths - use Dijkstra or Bellman-Ford
- Graph is sparse and n is moderate - running Dijkstra from each node might be faster

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n^3) | Three nested loops, each iterating n times |
| Space | O(n^2) | Storing the distance matrix |
| Query Time | O(1) | After preprocessing, each query is a simple lookup |

**Why O(n^3) is acceptable here:**
- n <= 500, so n^3 = 125,000,000 operations
- Each operation is simple (comparison and addition)
- Fits within typical 1-2 second time limits

## Related Problems

| Problem | Key Difference |
|---------|----------------|
| Shortest Routes I | Single-source shortest path (use Dijkstra) |
| Flight Discount | Single discount available (modified Dijkstra) |
| Cycle Finding | Detect negative cycles (Bellman-Ford or Floyd-Warshall) |

## Summary

Floyd-Warshall is the go-to algorithm for all-pairs shortest paths when:
1. n is small enough for O(n^3)
2. You need distances between many/all pairs
3. Negative edges might exist (but not negative cycles)

**Key points to remember:**
- **k (intermediate) must be the outermost loop**
- Initialize dist[i][i] = 0 and dist[i][j] = edge weight or INF
- Guard against overflow when using INF
- The algorithm naturally handles multiple edges (take minimum during input)
- After the algorithm, dist[a][b] gives the shortest path from a to b
