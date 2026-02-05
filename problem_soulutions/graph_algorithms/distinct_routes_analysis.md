---
layout: problem_analysis
title: "Distinct Routes"
difficulty: Hard
tags: [graph, max-flow, ford-fulkerson, bfs]
cses_link: https://cses.fi/problemset/task/1711
---

# Distinct Routes

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find maximum number of routes from city 1 to city n |
| Constraint | Each flight (edge) can be used at most once |
| Core Concept | Maximum flow with unit capacity edges |
| Key Insight | Max flow = Max edge-disjoint paths |
| Algorithm | Ford-Fulkerson with BFS (Edmonds-Karp) |

## Learning Goals

After completing this problem, you will understand:
1. **Max Flow = Edge-Disjoint Paths**: The maximum flow in a network with unit capacities equals the maximum number of edge-disjoint paths
2. **Ford-Fulkerson Method**: Finding augmenting paths to increase flow iteratively
3. **Edmonds-Karp Algorithm**: Using BFS to find shortest augmenting paths for better complexity
4. **Path Reconstruction**: How to extract actual paths from the flow network

## Problem Statement

Given n cities and m one-way flights between them, find the maximum number of distinct routes from city 1 to city n such that each flight is used at most once. Output the routes.

**Input:**
- First line: n (cities), m (flights)
- Next m lines: a, b (flight from city a to city b)

**Output:**
- First line: k (maximum number of routes)
- For each route: number of cities in route, followed by the cities

**Constraints:**
- 2 <= n <= 500
- 1 <= m <= 1000

**Example:**
```
Input:
4 5
1 2
2 4
1 3
3 4
1 4

Output:
3
2 1 4
3 1 2 4
3 1 3 4
```

## Key Insight: Max Flow and Edge-Disjoint Paths

This problem is equivalent to finding the **maximum flow** in a network where each edge has **capacity 1**.

**Why?** Each unit of flow from source to sink represents one path. Since each edge has capacity 1, each edge can only be part of one path. Therefore:

> **Maximum Flow = Maximum Number of Edge-Disjoint Paths**

```
         Capacity 1 on all edges

    [1] -----> [2]
     |  \       |
     |   \      |
     v    v     v
    [3] -----> [4]

Flow interpretation:
- Send 1 unit: 1 -> 4 (direct)
- Send 1 unit: 1 -> 2 -> 4
- Send 1 unit: 1 -> 3 -> 4
Total flow = 3 = 3 edge-disjoint paths
```

## Algorithm: Ford-Fulkerson with BFS (Edmonds-Karp)

### Core Idea

1. **Initialize**: Set flow on all edges to 0
2. **Find Augmenting Path**: Use BFS to find a path from source (1) to sink (n) with available capacity
3. **Augment Flow**: Push 1 unit of flow along this path (mark edges as used)
4. **Handle Reverse Edges**: Add capacity to reverse edges (allows flow cancellation)
5. **Repeat**: Until no augmenting path exists
6. **Reconstruct Paths**: Trace flow from source to sink

### Why BFS (Edmonds-Karp)?

Using BFS guarantees we find the **shortest augmenting path**, which provides:
- Better time complexity: O(V * E^2) vs O(E * max_flow) for DFS
- More predictable performance

### Residual Graph Concept

For each edge (u, v) with capacity c:
- **Forward edge**: Remaining capacity = c - flow(u,v)
- **Reverse edge**: Capacity = flow(u,v) (allows undoing flow)

```
Original edge:     u ---[cap=1]---> v
After flow of 1:   u ---[cap=0]---> v   (forward: full)
                   u <--[cap=1]--- v    (reverse: can undo)
```

## Visual Walkthrough

### Initial Graph
```
Cities: 1, 2, 3, 4
Flights: 1->2, 2->4, 1->3, 3->4, 1->4

        +---[2]---+
        |         |
       (1)       (1)
        |         |
    [1]-+         +->[4]
        |         |
       (1)       (1)
        |         |
        +---[3]---+
        |
       (1)
        |
        +---------->

(number) = capacity = 1
```

### Finding Augmenting Paths

**Path 1: BFS finds 1 -> 4 (shortest)**
```
[1] =========> [4]

Flow: 1
Edge 1->4 now used (capacity 0)
```

**Path 2: BFS finds 1 -> 2 -> 4**
```
[1] ---> [2] ---> [4]

Flow: 2
Edges 1->2, 2->4 now used
```

**Path 3: BFS finds 1 -> 3 -> 4**
```
[1] ---> [3] ---> [4]

Flow: 3
Edges 1->3, 3->4 now used
```

**No more augmenting paths exist. Maximum flow = 3**

## Dry Run

**Input:**
```
n=4, m=5
Edges: (1,2), (2,4), (1,3), (3,4), (1,4)
```

**Step-by-step:**

| Step | Action | BFS Path Found | Flow | Used Edges |
|------|--------|----------------|------|------------|
| 0 | Initialize | - | 0 | {} |
| 1 | BFS from 1 | 1 -> 4 | 1 | {1->4} |
| 2 | BFS from 1 | 1 -> 2 -> 4 | 2 | {1->4, 1->2, 2->4} |
| 3 | BFS from 1 | 1 -> 3 -> 4 | 3 | {1->4, 1->2, 2->4, 1->3, 3->4} |
| 4 | BFS from 1 | None found | 3 | - |

**Path Reconstruction:**
- From node 1, trace edges with flow = 1
- Path 1: 1 -> 4
- Path 2: 1 -> 2 -> 4
- Path 3: 1 -> 3 -> 4

**Output:**
```
3
2 1 4
3 1 2 4
3 1 3 4
```

## Implementation

### Python Solution

```python
from collections import deque, defaultdict

def solve():
  n, m = map(int, input().split())

  # Adjacency list with edge indices
  # For each edge, store (to, capacity, reverse_edge_index)
  graph = defaultdict(list)

  def add_edge(u, v, cap):
    # Forward edge
    graph[u].append([v, cap, len(graph[v])])
    # Reverse edge (capacity 0 initially)
    graph[v].append([u, 0, len(graph[u]) - 1])

  for _ in range(m):
    a, b = map(int, input().split())
    add_edge(a, b, 1)

  def bfs():
    """Find augmenting path using BFS, return parent array"""
    parent = {1: None}  # node -> (prev_node, edge_index)
    queue = deque([1])

    while queue:
      u = queue.popleft()
      if u == n:
        return parent

      for i, (v, cap, _) in enumerate(graph[u]):
        if cap > 0 and v not in parent:
          parent[v] = (u, i)
          queue.append(v)

    return None

  # Ford-Fulkerson with BFS (Edmonds-Karp)
  max_flow = 0

  while True:
    parent = bfs()
    if parent is None:
      break

    # Augment flow along path (always 1 for unit capacity)
    max_flow += 1

    # Update residual capacities
    v = n
    while parent[v] is not None:
      u, edge_idx = parent[v]
      rev_idx = graph[u][edge_idx][2]

      # Decrease forward edge capacity
      graph[u][edge_idx][1] -= 1
      # Increase reverse edge capacity
      graph[v][rev_idx][1] += 1

      v = u

  # Reconstruct paths
  paths = []
  for _ in range(max_flow):
    path = [1]
    curr = 1

    while curr != n:
      for i, (v, cap, rev_idx) in enumerate(graph[curr]):
        # Check if this edge was used (reverse has capacity)
        if graph[v][rev_idx][1] > 0 and cap == 0:
          # Remove one unit of flow from this edge
          graph[v][rev_idx][1] -= 1
          path.append(v)
          curr = v
          break

    paths.append(path)

  # Output
  print(max_flow)
  for path in paths:
    print(len(path), *path)

solve()
```

### Common Mistakes

### 1. Not Handling Reverse Edges Properly

**Wrong:**
```python
# Only tracking forward edges
if edge_used[u][v]:
  continue
```

**Correct:**
```python
# Must use residual graph with reverse edges
# Reverse edges allow "undoing" flow decisions
graph[v].append([u, 0, len(graph[u]) - 1])  # Reverse edge
```

**Why it matters:** Without reverse edges, the algorithm cannot correct suboptimal flow decisions and may find fewer paths than actually exist.

### 2. Incorrect Path Reconstruction

**Wrong:** Trying to reconstruct paths during the flow computation.

**Correct:** First compute maximum flow, then trace edges with flow from source to sink separately.

### 3. Forgetting to Handle Multiple Edges

If there are multiple edges between the same pair of nodes, each must be treated as a separate edge with its own capacity.

### 4. Off-by-One Errors in 1-indexed Problems

CSES uses 1-indexed cities. Ensure your arrays are sized appropriately (MAXN = n+1).

## Advanced Algorithms

For larger graphs or when better complexity is needed:

| Algorithm | Time Complexity | Notes |
|-----------|----------------|-------|
| Edmonds-Karp | O(V * E^2) | BFS-based, used here |
| Dinic's | O(V^2 * E) | Uses level graphs |
| Push-Relabel | O(V^2 * E) or O(V^3) | Different approach |

**Dinic's Algorithm** is often preferred for competitive programming due to:
- Better practical performance
- O(E * sqrt(V)) for unit capacity graphs (like this problem)

## Complexity Analysis

**Time Complexity: O(V * E^2)**
- Each BFS: O(E)
- Maximum flow is at most E (each augmenting path uses at least one edge)
- But Edmonds-Karp guarantees at most O(V * E) augmentations
- Total: O(V * E) augmentations * O(E) per BFS = O(V * E^2)

**Space Complexity: O(V + E)**
- Graph storage: O(E) edges
- BFS queue and parent array: O(V)

**For this problem's constraints (n <= 500, m <= 1000):**
- Worst case: 500 * 1000^2 = 5 * 10^8 operations
- In practice, much faster due to early termination
- Edmonds-Karp handles these constraints comfortably

## Related Problems

- **CSES Flight Routes Check**: Connectivity verification
- **CSES Police Chase**: Minimum cut (dual of max flow)
- **CSES School Dance**: Bipartite matching (special case of max flow)
