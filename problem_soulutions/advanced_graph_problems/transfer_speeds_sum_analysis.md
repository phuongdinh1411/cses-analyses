---
layout: simple
title: "Download Speed - Maximum Flow Problem"
permalink: /problem_soulutions/advanced_graph_problems/download_speed_analysis
difficulty: Hard
tags: [max-flow, edmonds-karp, ford-fulkerson, bfs, network-flow]
---

# Download Speed (Maximum Flow)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES Problem Set - Download Speed](https://cses.fi/problemset/task/1694) |
| **Difficulty** | Hard |
| **Category** | Graph / Network Flow |
| **Time Limit** | 1 second |
| **Key Technique** | Edmonds-Karp (BFS-based Max Flow) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the maximum flow problem and its applications
- [ ] Implement the Edmonds-Karp algorithm using BFS
- [ ] Build and manipulate residual graphs for flow networks
- [ ] Identify when a problem can be modeled as network flow

---

## Problem Statement

**Problem:** Given a network of computers with n nodes and m connections, find the maximum data transfer speed from computer 1 (source) to computer n (sink). Each connection has a limited capacity.

**Input:**
- Line 1: Two integers n (nodes) and m (edges)
- Lines 2 to m+1: Three integers a, b, c - connection from a to b with capacity c

**Output:**
- Single integer: maximum possible data transfer speed

**Constraints:**
- 1 <= n <= 500
- 1 <= m <= 1000
- 1 <= a, b <= n
- 1 <= c <= 10^9

### Example

```
Input:
4 5
1 2 3
2 4 2
1 3 4
3 4 5
4 1 3

Output:
6
```

**Explanation:** Maximum flow of 6 units: path 1->2->4 carries 2 units, path 1->3->4 carries 4 units. Total = 6.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we maximize "stuff" flowing from point A to point B through a network?

This is a classic **Maximum Flow** problem. Think of water flowing through pipes - each pipe has a maximum capacity, and we want to maximize the total water reaching the destination.

### Breaking Down the Problem

1. **What are we looking for?** Maximum total flow from source (node 1) to sink (node n)
2. **What constraints exist?** Each edge can only carry up to its capacity
3. **What's the key insight?** Keep finding paths with available capacity and push flow through them

### The Ford-Fulkerson Method

The core idea is simple:
1. Find ANY path from source to sink with available capacity
2. Push as much flow as possible through that path
3. Repeat until no more paths exist

**Edmonds-Karp** improves this by always finding the SHORTEST path (using BFS), guaranteeing O(VE^2) complexity.

---

## Solution: Edmonds-Karp Algorithm

### Key Insight

> **The Trick:** Use BFS to find augmenting paths in the residual graph. The residual graph tracks remaining capacity AND allows "undoing" previous flow decisions.

### Residual Graph Concept

| Term | Meaning |
|------|---------|
| `capacity[u][v]` | Maximum flow allowed from u to v |
| `flow[u][v]` | Current flow from u to v |
| `residual[u][v]` | Remaining capacity = capacity - flow |
| **Reverse edge** | residual[v][u] = flow[u][v] (allows canceling flow) |

**In plain English:** The residual graph shows how much MORE flow we can push, including the option to "undo" previous flow decisions.

### Algorithm

1. Initialize all flows to 0
2. While there exists a path from source to sink in residual graph (BFS):
   - Find the minimum capacity along the path (bottleneck)
   - Push that amount of flow along the path
   - Update residual capacities (decrease forward, increase backward)
3. Return total flow pushed

### Dry Run Example

Let's trace through with the example input:

```
Network:
    3 --> 2
   /|     |
  4 |     | 2
 /  |     v
1   |     4
 \  v    /
  4 --> 5
    3

Initial residual capacities:
  1->2: 3, 1->3: 4
  2->4: 2
  3->4: 5

Iteration 1: BFS finds path 1->2->4
  Bottleneck = min(3, 2) = 2
  Push 2 units, Total flow = 2
  Update: 1->2 residual = 1, 2->1 residual = 2
          2->4 residual = 0, 4->2 residual = 2

Iteration 2: BFS finds path 1->3->4
  Bottleneck = min(4, 5) = 4
  Push 4 units, Total flow = 6
  Update: 1->3 residual = 0, 3->1 residual = 4
          3->4 residual = 1, 4->3 residual = 4

Iteration 3: BFS finds no path from 1 to 4
  (1->2 has capacity 1 but 2->4 is full)
  (1->3 is full)

Final answer: 6
```

### Visual Diagram

```
Initial Network:          After Max Flow:
    [3]                       [1]  (residual)
  1 ---> 2                  1 ---> 2
  |      |                  |      |
[4]    [2]                [0]    [0]
  |      |                  |      |
  v      v                  v      v
  3 ---> 4                  3 ---> 4
    [5]                       [1]

Flow assignment:
  1->2: 2 units
  1->3: 4 units
  2->4: 2 units
  3->4: 4 units
  Total: 6 units
```

### Python Implementation

```python
from collections import deque

def max_flow(n, edges):
 """
 Edmonds-Karp algorithm for maximum flow.

 Time: O(V * E^2)
 Space: O(V^2) for adjacency matrix
 """
 # Build adjacency matrix for capacities
 capacity = [[0] * (n + 1) for _ in range(n + 1)]
 adj = [[] for _ in range(n + 1)]

 for a, b, c in edges:
  capacity[a][b] += c  # Handle multiple edges
  if b not in adj[a]:
   adj[a].append(b)
  if a not in adj[b]:
   adj[b].append(a)  # Reverse edge for residual

 def bfs(source, sink, parent):
  """Find augmenting path using BFS."""
  visited = [False] * (n + 1)
  queue = deque([source])
  visited[source] = True

  while queue:
   u = queue.popleft()
   for v in adj[u]:
    if not visited[v] and capacity[u][v] > 0:
     visited[v] = True
     parent[v] = u
     if v == sink:
      return True
     queue.append(v)
  return False

 source, sink = 1, n
 total_flow = 0
 parent = [-1] * (n + 1)

 while bfs(source, sink, parent):
  # Find bottleneck
  path_flow = float('inf')
  v = sink
  while v != source:
   u = parent[v]
   path_flow = min(path_flow, capacity[u][v])
   v = u

  # Update capacities along path
  v = sink
  while v != source:
   u = parent[v]
   capacity[u][v] -= path_flow
   capacity[v][u] += path_flow
   v = u

  total_flow += path_flow
  parent = [-1] * (n + 1)  # Reset parent

 return total_flow

# Read input
n, m = map(int, input().split())
edges = []
for _ in range(m):
 a, b, c = map(int, input().split())
 edges.append((a, b, c))

print(max_flow(n, edges))
```

### Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(V * E^2) | BFS runs O(VE) times, each BFS is O(E) |
| Space | O(V^2) | Adjacency matrix for capacities |

---

## Common Mistakes

### Mistake 1: Forgetting Reverse Edges

```python
# WRONG - Only forward edges
capacity[a][b] = c

# CORRECT - Initialize reverse edge for residual
capacity[a][b] += c
adj[a].append(b)
adj[b].append(a)  # Reverse edge needed!
```

**Problem:** Without reverse edges, we cannot "undo" flow decisions.
**Fix:** Always add both directions to adjacency list; reverse edge starts with 0 capacity.

### Mistake 2: Not Handling Multiple Edges

```python
# WRONG - Overwrites previous edge
capacity[a][b] = c

# CORRECT - Accumulate capacities
capacity[a][b] += c
```

**Problem:** Multiple edges between same nodes should add up.
**Fix:** Use += instead of = when setting capacity.

### Mistake 3: Integer Overflow

**Problem:** Capacities up to 10^9, total flow can exceed int range.
**Fix:** Use `long long` for capacity and flow variables.

### Mistake 4: Not Resetting Parent Array

```python
# WRONG - Reuses stale parent information
while bfs(source, sink, parent):
 # ... process path ...
 # parent array still has old values!

# CORRECT - Reset before each BFS
while bfs(source, sink, parent):
 # ... process path ...
 parent = [-1] * (n + 1)  # Reset!
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Direct path | 2 nodes, 1 edge | Edge capacity | Simple single path |
| No path | Disconnected graph | 0 | No flow possible |
| Multiple edges | Same a,b | Sum of capacities | Parallel pipes |
| Cycle in graph | Graph with cycles | Valid max flow | Algorithm handles this |
| Large capacities | c = 10^9 | Use long long | Overflow prevention |
| Self-loop | a = b | Ignore or handle | Usually no effect on flow |

---

## When to Use This Pattern

### Use Max Flow When:
- Finding maximum "throughput" in a network
- Matching problems (bipartite matching = max flow)
- Finding minimum cut (equal to max flow by duality)
- Resource allocation with capacity constraints

### Don't Use When:
- Simple shortest path is needed (use Dijkstra/BFS)
- No capacity constraints exist
- Problem is about minimum cost (use Min-Cost Max-Flow instead)

### Pattern Recognition Checklist:
- [ ] Does the problem involve "maximum transfer/throughput"? -> **Max Flow**
- [ ] Is it about matching items in two groups? -> **Bipartite Matching via Max Flow**
- [ ] Finding minimum edges to disconnect? -> **Min Cut = Max Flow**

---

## Related Problems

### Prerequisites (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [CSES - Labyrinth](https://cses.fi/problemset/task/1193) | BFS fundamentals |
| [CSES - Shortest Routes I](https://cses.fi/problemset/task/1671) | Graph traversal basics |

### Similar Difficulty (CSES Graph Problems)

| Problem | Key Concept |
|---------|-------------|
| [CSES - Police Chase](https://cses.fi/problemset/task/1695) | Min Cut (dual of Max Flow) |
| [CSES - School Dance](https://cses.fi/problemset/task/1696) | Bipartite Matching via Max Flow |
| [CSES - Distinct Routes](https://cses.fi/problemset/task/1711) | Edge-disjoint paths |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES - Coin Grid](https://cses.fi/problemset/task/1709) | Min vertex cover |
| Min-Cost Max-Flow problems | Cost optimization with flow |

---

## Key Takeaways

1. **The Core Idea:** Keep finding paths with available capacity and push flow until no paths remain.
2. **Residual Graph:** The key data structure - tracks remaining capacity AND allows undoing flow.
3. **Why BFS?** Edmonds-Karp uses BFS to guarantee polynomial time O(VE^2).
4. **Reverse Edges:** Critical for allowing the algorithm to "change its mind" about flow decisions.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain what a residual graph is and why reverse edges are needed
- [ ] Implement Edmonds-Karp from scratch in under 15 minutes
- [ ] Identify max flow problems in disguise (matching, min cut)
- [ ] Handle edge cases: multiple edges, large capacities, disconnected graphs

---

## Additional Resources

- [CP-Algorithms: Maximum Flow](https://cp-algorithms.com/graph/edmonds_karp.html)
- [CP-Algorithms: Min-Cut Max-Flow Theorem](https://cp-algorithms.com/graph/min_cut.html)
- [CSES Download Speed](https://cses.fi/problemset/task/1694) - Maximum flow problem
- [Visualgo - Network Flow](https://visualgo.net/en/maxflow)
