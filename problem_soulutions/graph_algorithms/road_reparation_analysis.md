---
layout: simple
title: "Road Reparation - Minimum Spanning Tree with Kruskal's Algorithm"
permalink: /problem_soulutions/graph_algorithms/road_reparation_analysis
difficulty: Medium
tags: [graph, mst, kruskal, union-find, greedy]
cses_link: https://cses.fi/problemset/task/1675
---

# Road Reparation - Minimum Spanning Tree (MST)

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Connect all cities with minimum total road repair cost |
| Algorithm | Kruskal's Algorithm with Union-Find |
| Time Complexity | O(m log m) |
| Space Complexity | O(n + m) |
| Key Technique | Greedy edge selection + cycle detection |
| Difficulty | Medium |

## Learning Goals

By completing this problem, you will master:

1. **MST Concept**: Understanding what a Minimum Spanning Tree is and why it matters
2. **Kruskal's Algorithm**: Greedy approach to building MST by processing edges in sorted order
3. **Union-Find Data Structure**: Efficient component tracking and cycle detection
4. **Connectivity Check**: Determining when a graph cannot be fully connected

## Problem Statement

There are **n** cities and **m** bidirectional roads. Each road has a repair cost. Find the **minimum total cost** to repair roads such that all cities become connected. If it's impossible to connect all cities, output "IMPOSSIBLE".

**Input Format**:
- First line: n (cities) and m (roads)
- Next m lines: a, b, c (road between cities a and b with cost c)

**Output**: Minimum cost to connect all cities, or "IMPOSSIBLE"

**Constraints**:
- 1 <= n <= 10^5
- 1 <= m <= 2 x 10^5
- 1 <= cost <= 10^9

## What is a Minimum Spanning Tree?

A **Spanning Tree** of a graph is a subgraph that:
- Includes ALL vertices (nodes)
- Is a tree (connected and has no cycles)
- Has exactly **n-1** edges for n vertices

A **Minimum Spanning Tree (MST)** is a spanning tree with the smallest possible sum of edge weights.

```
Original Graph:              MST (total weight = 6):
    1                            1
   /|\                          /|
  3 1 4                        3 1
 /  |  \                      /  |
2---5---3                    2   3
    2

All edges available           Only edges: 1-2(3), 1-3(1), 3-4(2)
```

**Key Properties**:
- An MST connects all n vertices using exactly n-1 edges
- The total weight is minimized
- An MST may not be unique, but all MSTs have the same total weight

## Kruskal's Algorithm

Kruskal's algorithm builds the MST using a **greedy approach**:

### Algorithm Steps

1. **Sort** all edges by weight (ascending)
2. **Initialize** each vertex as its own component (using Union-Find)
3. **Process edges** in sorted order:
   - If the edge connects two DIFFERENT components, add it to MST
   - If both endpoints are in the SAME component, skip it (would create cycle)
4. **Stop** when MST has n-1 edges (all vertices connected)
5. If fewer than n-1 edges added after processing all edges, graph is disconnected

### Why Does Greedy Work? The Cut Property

The **Cut Property** guarantees Kruskal's correctness:

> For any cut (partition of vertices into two sets), the minimum weight edge crossing the cut is safe to include in the MST.

Since we process edges in sorted order, each edge we add is the minimum weight edge that connects two currently disconnected components.

## Visual Algorithm Progression

**Example**: 5 cities, 6 roads

```
Initial State:          Sorted Edges:
                        (1,2,1), (2,3,2), (1,3,3),
  1---3---4             (3,4,4), (4,5,5), (2,4,6)
  |\     /
  1 3   5               Components: {1}, {2}, {3}, {4}, {5}
  |  \ /
  2---5
    2

Step 1: Add edge (1,2) weight=1
  1                     Components: {1,2}, {3}, {4}, {5}
  |                     MST cost: 1
  1                     Edges in MST: 1
  |
  2

Step 2: Add edge (2,3) weight=2
  1---2---3             Components: {1,2,3}, {4}, {5}
      |                 MST cost: 3
      2                 Edges in MST: 2

Step 3: Skip edge (1,3) weight=3
  Would create cycle    Components: {1,2,3}, {4}, {5}
  (1 and 3 already      MST cost: 3
  in same component)    Edges in MST: 2

Step 4: Add edge (3,4) weight=4
  1---2---3---4         Components: {1,2,3,4}, {5}
                        MST cost: 7
                        Edges in MST: 3

Step 5: Add edge (4,5) weight=5
  1---2---3---4---5     Components: {1,2,3,4,5}
                        MST cost: 12
                        Edges in MST: 4 = n-1 (DONE!)

Final MST: edges (1,2), (2,3), (3,4), (4,5) with total cost = 12
```

## Dry Run Example

**Input**:
```
5 6
1 2 3
2 3 5
3 4 2
4 5 4
1 3 7
2 4 1
```

**Sorted edges by weight**: (2,4,1), (3,4,2), (1,2,3), (4,5,4), (2,3,5), (1,3,7)

| Step | Edge | Weight | Action | Components | MST Cost | Edges |
|------|------|--------|--------|------------|----------|-------|
| Init | - | - | - | {1},{2},{3},{4},{5} | 0 | 0 |
| 1 | (2,4) | 1 | Add | {1},{2,4},{3},{5} | 1 | 1 |
| 2 | (3,4) | 2 | Add | {1},{2,3,4},{5} | 3 | 2 |
| 3 | (1,2) | 3 | Add | {1,2,3,4},{5} | 6 | 3 |
| 4 | (4,5) | 4 | Add | {1,2,3,4,5} | 10 | 4 |

**Output**: 10 (MST complete with 4 = n-1 edges)

## Handling Disconnected Graphs

If after processing ALL edges, we have fewer than n-1 edges in MST, the graph is **disconnected**.

```
Example: 4 cities, 2 roads
1---2    3---4

No matter which edges we select, we cannot connect all 4 cities.
Output: IMPOSSIBLE
```

**Detection**: After Kruskal's algorithm, check if `edges_added == n - 1`

## Python Solution

```python
import sys
from typing import List, Tuple

def solve():
  input_data = sys.stdin.read().split()
  idx = 0
  n = int(input_data[idx]); idx += 1
  m = int(input_data[idx]); idx += 1

  edges: List[Tuple[int, int, int]] = []
  for _ in range(m):
    a = int(input_data[idx]); idx += 1
    b = int(input_data[idx]); idx += 1
    c = int(input_data[idx]); idx += 1
    edges.append((c, a, b))  # (weight, u, v) for easy sorting

  # Sort edges by weight
  edges.sort()

  # Union-Find with path compression and union by rank
  parent = list(range(n + 1))
  rank = [0] * (n + 1)

  def find(x: int) -> int:
    if parent[x] != x:
      parent[x] = find(parent[x])  # Path compression
    return parent[x]

  def union(x: int, y: int) -> bool:
    px, py = find(x), find(y)
    if px == py:
      return False  # Same component, would create cycle
    # Union by rank
    if rank[px] < rank[py]:
      px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]:
      rank[px] += 1
    return True

  # Kruskal's algorithm
  mst_cost = 0
  edges_added = 0

  for weight, u, v in edges:
    if union(u, v):
      mst_cost += weight
      edges_added += 1
      if edges_added == n - 1:
        break

  # Check if all cities are connected
  if edges_added == n - 1:
    print(mst_cost)
  else:
    print("IMPOSSIBLE")

if __name__ == "__main__":
  solve()
```

## Kruskal's vs Prim's Algorithm

| Aspect | Kruskal's | Prim's |
|--------|-----------|--------|
| Approach | Edge-centric (process edges globally) | Vertex-centric (grow tree from a vertex) |
| Data Structure | Union-Find | Priority Queue / Min-Heap |
| Time Complexity | O(m log m) | O(m log n) with binary heap |
| Best for | Sparse graphs (m close to n) | Dense graphs (m close to n^2) |
| Implementation | Simpler, sort then iterate | More complex, requires adjacency list |
| Edge Processing | Sorted order globally | Process edges of current frontier |

**When to use which**:
- **Kruskal's**: When edges are already sorted or graph is sparse
- **Prim's**: When graph is dense or stored as adjacency list

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Forgetting IMPOSSIBLE check | Output wrong answer for disconnected graphs | Always check if `edges_added == n - 1` |
| Integer overflow | Sum of edge weights exceeds int range | Use `long long` for cost accumulation |
| 1-indexed vs 0-indexed | Array out of bounds or wrong component | Be consistent; CSES uses 1-indexed |
| Not sorting edges | Algorithm gives wrong answer | Sort by weight before processing |
| Wrong Union-Find | Cycles included or components merged wrongly | Implement find with path compression |

## Complexity Analysis

**Time Complexity: O(m log m)**
- Sorting m edges: O(m log m)
- Processing each edge with Union-Find: O(m * alpha(n)) where alpha is inverse Ackermann
- Since alpha(n) <= 5 for practical n, effectively O(m)
- Total: O(m log m) dominated by sorting

**Space Complexity: O(n + m)**
- Edge storage: O(m)
- Union-Find arrays: O(n)

## Related Problems

- **CSES Building Roads**: Find minimum edges to add to connect graph
- **LeetCode 1584**: Min Cost to Connect All Points
- **LeetCode 1135**: Connecting Cities With Minimum Cost

## Key Takeaways

1. MST connects all vertices with minimum total edge weight using exactly n-1 edges
2. Kruskal's algorithm: sort edges, greedily add edges that don't create cycles
3. Union-Find efficiently tracks components and detects cycles in O(alpha(n))
4. Always check for disconnected graphs by verifying n-1 edges were added
5. Use `long long` for edge weight sums to avoid overflow
