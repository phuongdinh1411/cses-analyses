---
layout: simple
title: "Download Speed"
permalink: /problem_soulutions/graph_algorithms/download_speed_analysis
difficulty: Hard
tags: [graph, max-flow, ford-fulkerson, edmonds-karp]
cses_link: https://cses.fi/problemset/task/1694
---

# Download Speed

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find maximum data transfer rate from source to sink |
| Type | Maximum Flow |
| Difficulty | Hard |
| Key Algorithm | Edmonds-Karp (Ford-Fulkerson with BFS) |
| Time Complexity | O(VE^2) |
| Space Complexity | O(V^2) |

## Learning Goals

By completing this problem, you will understand:

1. **Maximum Flow Concept**: How to model network bandwidth as a flow problem
2. **Residual Graphs**: Tracking remaining capacity after using some flow
3. **Augmenting Paths**: Finding paths that can carry additional flow
4. **Ford-Fulkerson Method**: The general framework for max flow algorithms
5. **Edmonds-Karp Algorithm**: Using BFS to guarantee polynomial time complexity

## Problem Statement

You have a network of `n` computers numbered 1 to n. Computer 1 is the server and computer n is your computer. There are `m` connections between computers, each with a maximum bandwidth (data transfer capacity).

**Goal**: Find the maximum rate at which data can be transferred from computer 1 to computer n.

**Input**:
- First line: n (computers) and m (connections)
- Next m lines: a, b, c meaning connection from a to b with bandwidth c

**Output**: Maximum data transfer rate from 1 to n

**Constraints**:
- 1 <= n <= 500
- 1 <= m <= 1000
- 1 <= a, b <= n
- 1 <= c <= 10^9

## Core Concepts

### What is Maximum Flow?

Maximum flow finds the greatest amount of "flow" that can be sent from a source to a sink through a network where each edge has a capacity limit.

Key properties:
- **Capacity Constraint**: Flow on edge (u,v) cannot exceed its capacity
- **Flow Conservation**: For non-source/sink nodes, inflow = outflow
- **Skew Symmetry**: flow(u,v) = -flow(v,u)

### Residual Graph

The residual graph shows remaining capacity after some flow is used.

For each edge (u,v) with capacity c and current flow f:
- **Forward edge**: remaining capacity = c - f
- **Backward edge**: remaining capacity = f (allows "undoing" flow)

```
Original Graph:          After sending 3 units:    Residual Graph:

   [A]---5--->[B]         [A]--3/5-->[B]           [A]---2--->[B]
                                                       <---3---

   Capacity: 5            Flow: 3                  Forward: 5-3=2
                                                   Backward: 3 (reverse)
```

### Why Backward Edges?

Backward edges allow the algorithm to "undo" previous decisions. Without them, a greedy choice might block the optimal solution.

```
Example where backward edges are essential:

        2
    A-------->B
    |         |
  3 |         | 3
    v         v
    S         T
    |         |
  3 |         | 2
    v         v
    C-------->D
        3

Without backward edges: Path S->A->B->T uses 2, Path S->C->D->T uses 2
Total: 4

With backward edges: Can find path S->A->B->D->T (uses B->D backward)
Then S->C->D->T uses forward edge
Total: 5 (optimal)
```

## Ford-Fulkerson Algorithm

The Ford-Fulkerson method repeatedly finds augmenting paths until none exist.

### Algorithm Steps

```
1. Initialize: flow = 0 for all edges
2. Build residual graph from original capacities
3. While augmenting path exists from source to sink:
   a. Find path P in residual graph
   b. Find bottleneck = min capacity along P
   c. Augment flow by bottleneck:
      - Subtract bottleneck from forward edges
      - Add bottleneck to backward edges
   d. Add bottleneck to total flow
4. Return total flow
```

### Edmonds-Karp: BFS for Path Finding

Using BFS (instead of DFS) guarantees O(VE^2) complexity because:
- BFS finds shortest augmenting path (by edge count)
- Each edge becomes critical (bottleneck) at most O(V) times
- At most O(E) edges, so O(VE) augmentations
- Each BFS takes O(E), total: O(VE^2)

## Visual Walkthrough

### Example Network

```
Input:
4 5
1 2 6
1 3 4
2 3 2
2 4 3
3 4 5

Network Structure:
          6
    [1]------>[2]
     |  \      |
   4 |   \ 2   | 3
     v    v    v
    [3]------>[4]
          5
```

### Dry Run

**Initial State**:
```
Residual capacities:
1->2: 6    2->3: 2    3->4: 5
1->3: 4    2->4: 3
Total flow: 0
```

**Iteration 1**: BFS finds path 1 -> 2 -> 4
```
Path: 1 -> 2 -> 4
Bottleneck: min(6, 3) = 3

Update residual graph:
1->2: 6-3=3    2->1: 0+3=3
2->4: 3-3=0    4->2: 0+3=3

Total flow: 0 + 3 = 3
```

**Iteration 2**: BFS finds path 1 -> 3 -> 4
```
Path: 1 -> 3 -> 4
Bottleneck: min(4, 5) = 4

Update residual graph:
1->3: 4-4=0    3->1: 0+4=4
3->4: 5-4=1    4->3: 0+4=4

Total flow: 3 + 4 = 7
```

**Iteration 3**: BFS finds path 1 -> 2 -> 3 -> 4
```
Path: 1 -> 2 -> 3 -> 4
Bottleneck: min(3, 2, 1) = 1

Update residual graph:
1->2: 3-1=2    2->1: 3+1=4
2->3: 2-1=1    3->2: 0+1=1
3->4: 1-1=0    4->3: 4+1=5

Total flow: 7 + 1 = 8
```

**Iteration 4**: No augmenting path exists
```
BFS from 1 cannot reach 4 (all paths blocked)
Algorithm terminates

Maximum Flow: 8
```

**Final Flow Distribution**:
```
Edge 1->2: 4 units (capacity 6)
Edge 1->3: 4 units (capacity 4)
Edge 2->3: 1 unit  (capacity 2)
Edge 2->4: 3 units (capacity 3)
Edge 3->4: 5 units (capacity 5)

Verification:
- Outflow from 1: 4 + 4 = 8
- Inflow to 4: 3 + 5 = 8
```

## Implementation

### Python Solution

```python
from collections import deque

def max_flow(n, edges):
 """
 Find maximum flow from node 1 to node n.
 Uses Edmonds-Karp algorithm (Ford-Fulkerson with BFS).
 """
 # Build adjacency list and capacity matrix
 # Using dict for capacity to handle parallel edges
 adj = [[] for _ in range(n + 1)]
 capacity = {}

 for u, v, c in edges:
  # Add forward edge
  if (u, v) not in capacity:
   adj[u].append(v)
   adj[v].append(u)  # Reverse edge for residual graph
   capacity[(u, v)] = 0
   capacity[(v, u)] = 0
  capacity[(u, v)] += c  # Handle multiple edges between same nodes

 def bfs():
  """Find augmenting path using BFS. Returns (path, bottleneck)."""
  parent = [-1] * (n + 1)
  visited = [False] * (n + 1)
  visited[1] = True
  queue = deque([1])

  while queue:
   node = queue.popleft()
   if node == n:
    break

   for neighbor in adj[node]:
    if not visited[neighbor] and capacity[(node, neighbor)] > 0:
     visited[neighbor] = True
     parent[neighbor] = node
     queue.append(neighbor)

  # No path found
  if parent[n] == -1:
   return None, 0

  # Reconstruct path and find bottleneck
  path = []
  bottleneck = float('inf')
  current = n

  while current != 1:
   prev = parent[current]
   path.append((prev, current))
   bottleneck = min(bottleneck, capacity[(prev, current)])
   current = prev

  return path, bottleneck

 total_flow = 0

 while True:
  path, bottleneck = bfs()
  if path is None:
   break

  # Update residual capacities
  for u, v in path:
   capacity[(u, v)] -= bottleneck
   capacity[(v, u)] += bottleneck

  total_flow += bottleneck

 return total_flow


def solve():
 n, m = map(int, input().split())
 edges = []
 for _ in range(m):
  a, b, c = map(int, input().split())
  edges.append((a, b, c))

 print(max_flow(n, edges))


if __name__ == "__main__":
 solve()
```

### Common Mistakes

### 1. Forgetting Reverse Edges

**Wrong**:
```python
# Only adding forward edge
adj[u].append(v)
capacity[(u, v)] = c
```

**Correct**:
```python
# Must add both directions for residual graph
adj[u].append(v)
adj[v].append(u)
capacity[(u, v)] = c
capacity[(v, u)] = 0  # Reverse edge starts with 0 capacity
```

### 2. Integer Overflow

With capacities up to 10^9 and potentially 500 * 1000 total flow:
- Maximum flow can be around 5 * 10^11
- Use `long long` in C++ or Python's arbitrary precision

**Wrong** (C++):
**Correct**:
### 3. Not Handling Parallel Edges

Multiple edges between same nodes should have capacities added:

**Wrong**:
```python
capacity[(u, v)] = c  # Overwrites previous edge
```

**Correct**:
```python
capacity[(u, v)] += c  # Accumulates parallel edges
```

### 4. Incorrect Residual Update

**Wrong**:
```python
# Only updating forward edge
capacity[(u, v)] -= bottleneck
```

**Correct**:
```python
# Must update both directions
capacity[(u, v)] -= bottleneck  # Reduce forward
capacity[(v, u)] += bottleneck  # Increase backward
```

## Complexity Analysis

| Operation | Complexity | Explanation |
|-----------|------------|-------------|
| BFS | O(E) | Visits each edge once |
| Augmentations | O(VE) | Each edge saturates O(V) times with BFS |
| Total Time | O(VE^2) | O(VE) augmentations, each O(E) |
| Space | O(V^2) | Capacity matrix |

For this problem:
- V = 500, E = 1000
- O(VE^2) = O(500 * 1000^2) = O(5 * 10^8)
- Fits within time limit with efficient implementation

## Key Takeaways

1. **Max flow = min cut**: The maximum flow equals the minimum cut capacity
2. **Residual graph** enables finding augmenting paths after initial flow
3. **Backward edges** allow algorithm to "correct" suboptimal choices
4. **BFS guarantees** O(VE^2) time (Edmonds-Karp)
5. **Handle large values** with appropriate data types
