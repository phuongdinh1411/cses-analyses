---
layout: simple
title: "Nearest Shops - Multi-Source Shortest Path"
permalink: /problem_soulutions/advanced_graph_problems/nearest_shops_analysis
difficulty: Medium
tags: [dijkstra, multi-source-bfs, shortest-path, graph]
---

# Nearest Shops

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Graph / Shortest Path |
| **Key Technique** | Multi-Source BFS / Dijkstra |
| **CSES Link** | Custom Problem (Similar: [Shortest Routes I](https://cses.fi/problemset/task/1671)) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when multi-source shortest path is needed
- [ ] Implement multi-source BFS for unweighted graphs
- [ ] Implement multi-source Dijkstra for weighted graphs
- [ ] Precompute distances to answer multiple queries in O(1)

---

## Problem Statement

**Problem:** Given a weighted undirected graph with n nodes and m edges, where some nodes are designated as "shops," answer queries asking for the shortest distance from a given node to the nearest shop.

**Input:**
- Line 1: n (nodes), m (edges)
- Next m lines: a b w (edge from a to b with weight w)
- Line m+2: k (number of shops)
- Next line: k shop node IDs
- Next line: q (number of queries)
- Next q lines: query node

**Output:**
- For each query, print the distance to the nearest shop (or -1 if unreachable)

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 x 10^5
- 1 <= k <= n
- 1 <= q <= 10^5
- 1 <= w <= 10^6

### Example

```
Input:
5 6
1 2 2
2 3 3
3 4 1
4 5 2
1 4 4
2 5 1
2
2 4
3
1
3
5

Output:
2
1
1
```

**Explanation:**
- Query 1 (node 1): Nearest shop is node 2, distance = 2
- Query 2 (node 3): Nearest shop is node 4, distance = 1
- Query 3 (node 5): Nearest shop is node 2 via edge 2-5, distance = 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently find the nearest among multiple destinations?

Instead of running shortest path FROM each query node, we flip the problem: run shortest path FROM all shops simultaneously. This is the **multi-source shortest path** pattern.

### Breaking Down the Problem

1. **What are we looking for?** Minimum distance from query node to ANY shop
2. **What information do we have?** Graph structure and shop locations
3. **What's the key insight?** Distance from node X to nearest shop = Distance from nearest shop to X (undirected graph)

### Why Multi-Source Works

```
Instead of:                    We do:
  Query1 -> Shop1               Shop1 -\
  Query1 -> Shop2                       |-> All nodes (one pass)
  Query2 -> Shop1               Shop2 -/
  Query2 -> Shop2
  ... (expensive!)              ... (efficient!)
```

---

## Solution 1: Brute Force (Per-Query BFS/Dijkstra)

### Idea

For each query, run Dijkstra from the query node and find the minimum distance among all shops.

### Code

```python
import heapq
from typing import List, Tuple

def solve_brute_force(n: int, edges: List[Tuple[int,int,int]],
           shops: List[int], queries: List[int]) -> List[int]:
  """
  Brute force: Run Dijkstra for each query.
  Time: O(q * (n + m) log n)
  Space: O(n + m)
  """
  # Build adjacency list (0-indexed)
  adj = [[] for _ in range(n)]
  for a, b, w in edges:
    adj[a-1].append((b-1, w))
    adj[b-1].append((a-1, w))

  shop_set = set(s - 1 for s in shops)  # 0-indexed

  def dijkstra(start: int) -> int:
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
      d, u = heapq.heappop(pq)
      if d > dist[u]:
        continue
      if u in shop_set:
        return d  # Found nearest shop
      for v, w in adj[u]:
        if dist[u] + w < dist[v]:
          dist[v] = dist[u] + w
          heapq.heappush(pq, (dist[v], v))
    return -1

  return [dijkstra(q - 1) for q in queries]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * (n+m) log n) | Dijkstra per query |
| Space | O(n + m) | Graph storage |

### Why This Is Slow

For 10^5 queries, each running Dijkstra on a graph with 10^5 nodes = TLE guaranteed.

---

## Solution 2: Multi-Source Dijkstra (Optimal)

### Key Insight

> **The Trick:** Start Dijkstra from ALL shops simultaneously with distance 0. After one pass, `dist[u]` = distance from u to nearest shop.

### Algorithm

1. Initialize priority queue with ALL shop nodes at distance 0
2. Run standard Dijkstra relaxation
3. After completion, `dist[i]` = shortest distance from node i to any shop
4. Answer each query in O(1)

### Dry Run Example

```
Graph: 1--2--3--4--5  (weights: 1-2=2, 2-3=3, 3-4=1, 4-5=2, 2-5=1)
Shops: {2, 4}

Initial PQ: [(0, 2), (0, 4)]  dist = [inf, 0, inf, 0, inf]

Pop (0, 2):
  - Relax 1: dist[1] = 2      PQ: [(0, 4), (2, 1)]
  - Relax 3: dist[3] = 3      PQ: [(0, 4), (2, 1), (3, 3)]
  - Relax 5: dist[5] = 1      PQ: [(0, 4), (1, 5), (2, 1), (3, 3)]

Pop (0, 4):
  - Relax 3: dist[3] = min(3, 1) = 1  PQ updated
  - Relax 5: dist[5] = min(1, 2) = 1  (no change)

Pop (1, 5): neighbors already have better distances

Pop (2, 1): neighbors already have better distances

Final dist = [2, 0, 1, 0, 1]
             node: 1  2  3  4  5

Query(1) = 2, Query(3) = 1, Query(5) = 1
```

### Visual Diagram

```
Shops marked with [S]

      2           1           2
  1 ----- [S]2 ----- 3 ----- [S]4 ----- 5
              \                         /
               \__________ 1 __________/

Distance propagation from shops:
  Shop 2: reaches 1(dist=2), 3(dist=3), 5(dist=1)
  Shop 4: reaches 3(dist=1), 5(dist=2)

Final distances to nearest shop:
  Node 1: 2 (via shop 2)
  Node 2: 0 (is shop)
  Node 3: 1 (via shop 4)
  Node 4: 0 (is shop)
  Node 5: 1 (via shop 2)
```

### Code (Python)

```python
import heapq
from typing import List, Tuple

def solve_multi_source_dijkstra(n: int, edges: List[Tuple[int,int,int]],
                shops: List[int], queries: List[int]) -> List[int]:
  """
  Multi-source Dijkstra: Start from all shops simultaneously.
  Time: O((n + m) log n + q)
  Space: O(n + m)
  """
  # Build adjacency list (0-indexed)
  adj = [[] for _ in range(n)]
  for a, b, w in edges:
    adj[a-1].append((b-1, w))
    adj[b-1].append((a-1, w))

  # Multi-source Dijkstra
  dist = [float('inf')] * n
  pq = []

  # Initialize: all shops start at distance 0
  for shop in shops:
    dist[shop - 1] = 0
    heapq.heappush(pq, (0, shop - 1))

  # Standard Dijkstra relaxation
  while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]:
      continue
    for v, w in adj[u]:
      if dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
        heapq.heappush(pq, (dist[v], v))

  # Answer queries in O(1) each
  return [dist[q - 1] if dist[q - 1] != float('inf') else -1 for q in queries]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + m) log n + q) | Single Dijkstra + O(1) per query |
| Space | O(n + m) | Graph + distance array |

---

## Common Mistakes

### Mistake 1: Running Dijkstra Per Query

```python
# WRONG: TLE for large q
for query in queries:
  answer = dijkstra(query)  # O((n+m) log n) each time!
```

**Problem:** O(q * (n+m) log n) is too slow.
**Fix:** Use multi-source Dijkstra to precompute all distances once.

### Mistake 2: Forgetting to Skip Stale Entries

```python
# WRONG: May process same node multiple times
while pq:
  d, u = heapq.heappop(pq)
  # Missing: if d > dist[u]: continue
  for v, w in adj[u]:
    ...
```

**Problem:** Without this check, we process outdated (larger) distances.
**Fix:** Always skip if the popped distance exceeds current known distance.

### Mistake 3: Using BFS for Weighted Graphs

```python
# WRONG: BFS doesn't work for weighted edges
from collections import deque
queue = deque(shops)
while queue:
  u = queue.popleft()
  for v, w in adj[u]:
    if dist[v] > dist[u] + w:  # BFS can't handle this correctly
      dist[v] = dist[u] + w
      queue.append(v)
```

**Problem:** BFS processes nodes in order added, not by distance.
**Fix:** Use priority queue (Dijkstra) for weighted graphs, or use 0-1 BFS if weights are only 0 and 1.

### Mistake 4: Integer Overflow

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Query node is a shop | shops=[2], query=2 | 0 | Distance to itself |
| Unreachable node | Disconnected graph | -1 | No path exists |
| Single node graph | n=1, shops=[1] | 0 | Trivial case |
| All nodes are shops | shops=[1,2,3,...,n] | 0 for all | Every node is distance 0 |
| Large weights | w = 10^6 | Use long long | Prevent overflow |

---

## When to Use This Pattern

### Use Multi-Source BFS/Dijkstra When:
- Multiple source points, need distance to nearest source
- Many queries about "nearest X" type questions
- Finding influence zones or Voronoi-like regions

### Don't Use When:
- Only one query (single-source Dijkstra is simpler)
- Need path reconstruction to each source separately
- Graph is dynamic (sources change frequently)

### Pattern Recognition Checklist:
- [ ] Multiple "special" nodes (sources/destinations)?
- [ ] Need distance FROM query TO nearest special node?
- [ ] Many queries on same graph?
- [ ] --> **Consider Multi-Source Shortest Path**

---

## Related Problems

### CSES Problems

| Problem | Link | Relevance |
|---------|------|-----------|
| Shortest Routes I | [cses.fi/problemset/task/1671](https://cses.fi/problemset/task/1671) | Single-source Dijkstra |
| Shortest Routes II | [cses.fi/problemset/task/1672](https://cses.fi/problemset/task/1672) | All-pairs Floyd-Warshall |
| Flight Routes | [cses.fi/problemset/task/1196](https://cses.fi/problemset/task/1196) | K shortest paths |
| High Score | [cses.fi/problemset/task/1673](https://cses.fi/problemset/task/1673) | Longest path with negative detection |

### LeetCode Problems

| Problem | Key Difference |
|---------|----------------|
| [01 Matrix](https://leetcode.com/problems/01-matrix/) | Multi-source BFS on grid |
| [Walls and Gates](https://leetcode.com/problems/walls-and-gates/) | Multi-source BFS with obstacles |
| [Shortest Path to Get Food](https://leetcode.com/problems/shortest-path-to-get-food/) | Multiple destinations |
| [As Far from Land as Possible](https://leetcode.com/problems/as-far-from-land-as-possible/) | Multi-source BFS, find maximum |

---

## Key Takeaways

1. **The Core Idea:** Flip the problem - start from destinations, not sources
2. **Time Optimization:** O(q * (n+m) log n) -> O((n+m) log n + q)
3. **Space Trade-off:** O(n) extra for precomputed distances
4. **Pattern:** Multi-source shortest path for nearest-destination queries

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why multi-source works for "nearest" queries
- [ ] Implement multi-source Dijkstra from scratch
- [ ] Identify when to use BFS vs Dijkstra (weighted vs unweighted)
- [ ] Handle edge cases (unreachable nodes, overflow)
- [ ] Solve this in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Dijkstra](https://cp-algorithms.com/graph/dijkstra.html)
- [CP-Algorithms: 0-1 BFS](https://cp-algorithms.com/graph/01_bfs.html)
- [Multi-Source BFS Explanation](https://cp-algorithms.com/graph/breadth-first-search.html)
