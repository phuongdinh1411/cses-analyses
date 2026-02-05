---
layout: analysis
title: "School Dance"
difficulty: Hard
tags: [graph, bipartite-matching, max-flow, hopcroft-karp]
cses_link: https://cses.fi/problemset/task/1696
---

# School Dance - Maximum Bipartite Matching

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem Type | Maximum Bipartite Matching |
| Technique | Reduction to Max Flow / Hopcroft-Karp |
| Time Complexity | O(V * E) with Ford-Fulkerson, O(E * sqrt(V)) with Hopcroft-Karp |
| Space Complexity | O(V + E) |
| Key Insight | Bipartite matching reduces to maximum flow in a network |

## Learning Goals

After solving this problem, you will understand:

1. **Bipartite Matching**: How to model pairing problems as bipartite graphs
2. **Reduction to Max Flow**: Converting matching to a flow network with source/sink
3. **Flow Network Construction**: Adding auxiliary nodes and unit capacities
4. **Extracting the Matching**: Recovering actual pairs from flow solution

## Problem Statement

There are **n** boys and **m** girls at a school dance. You are given **k** pairs indicating which boy and girl are willing to dance together.

**Goal**: Find the maximum number of dancing pairs, where each person can dance with at most one partner.

**Input**:
- First line: n, m, k (number of boys, girls, and potential pairs)
- Next k lines: Each contains two integers a and b, meaning boy a and girl b are willing to dance

**Output**:
- First line: The maximum number of dance pairs
- Next lines: Each matched pair (boy girl)

**Constraints**:
- 1 <= n, m <= 500
- 1 <= k <= 1000

**Example**:
```
Input:
4 3 6
1 1
1 2
2 1
2 2
3 1
4 3

Output:
3
1 2
2 1
4 3
```

## Key Insight

Maximum bipartite matching is equivalent to maximum flow in a specially constructed network:

```
                    Max Matching = Max Flow

    Bipartite Graph    -->    Flow Network

    Boys --- Girls     -->    S -> Boys -> Girls -> T
```

The critical observation is that **each person can appear in at most one pair**, which maps perfectly to **unit capacity edges** in a flow network.

## Reduction to Max Flow

### Network Construction

To convert bipartite matching to max flow:

1. **Add Source S**: Connect S to all boys with capacity 1
2. **Add Sink T**: Connect all girls to T with capacity 1
3. **Add Pair Edges**: For each compatible (boy, girl) pair, add edge with capacity 1

```
Flow Network Structure:

         capacity = 1 each
              |
    Source ---+---> Boy 1 ----> Girl 1 ---+---> Sink
              |         \      /          |
              +---> Boy 2 --X--> Girl 2 --+
              |         /      \          |
              +---> Boy 3 ----> Girl 3 ---+
              |                           |
              +---> Boy 4 --------> ... --+
```

### Why This Works

| Property | Matching Constraint | Flow Constraint |
|----------|---------------------|-----------------|
| Boy uses at most 1 | Each boy matched once | Edge S->Boy has capacity 1 |
| Girl uses at most 1 | Each girl matched once | Edge Girl->T has capacity 1 |
| Valid pair | (boy, girl) compatible | Edge exists Boy->Girl |

**Max Flow = Max Matching** because:
- Flow of 1 through Boy->Girl means they are matched
- Unit capacities ensure each person appears in at most one pair

## Visual Diagram

### Original Bipartite Graph

```
    Boys           Girls

    B1 ------------ G1
      \ \        /
       \  \    /
    B2 ---+--X--- G2
          |    \
    B3 ---+
                   G3
    B4 ------------
```

### Converted Flow Network

```
          +----[1]----> B1 --[1]--> G1 --[1]----+
          |              \ \      /              |
          |               \ [1] /                |
    [S] --+----[1]----> B2 -X---> G2 --[1]----+--> [T]
          |                  \                  |
          +----[1]----> B3 ---+                 |
          |                                     |
          +----[1]----> B4 --------> G3 --[1]--+

    [1] = capacity 1
```

## Dry Run

**Input**: n=4, m=3, pairs = [(1,1), (1,2), (2,1), (2,2), (3,1), (4,3)]

**Step 1**: Build flow network
```
Nodes: S=0, Boys=1-4, Girls=5-7, T=8
Edges: S->1,2,3,4 (cap 1), 1->5,6, 2->5,6, 3->5, 4->7, 5,6,7->T (cap 1)
```

**Step 2**: Find augmenting paths
```
Path 1: S -> 1 -> 5 -> T  (flow +1)
Path 2: S -> 2 -> 6 -> T  (flow +1)
Path 3: S -> 4 -> 7 -> T  (flow +1)
Path 4: S -> 3 -> 5 -> ... blocked (G1 already saturated)
```

**Step 3**: Check for augmenting paths via residual graph
```
Try: S -> 3 -> 5 -> 1 (reverse) -> 6 -> ... blocked (G2 saturated by B2)
No more augmenting paths found.
```

**Result**: Max flow = 3

**Extract matching from flow**:
- Boy 1 -> Girl 1 (or Boy 1 -> Girl 2 depending on path order)
- Boy 2 -> Girl 2 (or Girl 1)
- Boy 4 -> Girl 3

## Alternative Algorithms

### Hopcroft-Karp Algorithm

Specifically designed for bipartite matching with better complexity:

- **Time**: O(E * sqrt(V)) - faster for sparse graphs
- **Idea**: Find multiple augmenting paths of the same length simultaneously using BFS + DFS
- **Advantage**: Fewer iterations than basic Ford-Fulkerson

### Hungarian Algorithm

For **weighted** bipartite matching (assignment problem):

- **Time**: O(V^3)
- **Use Case**: When pairs have different costs/preferences

For this unweighted problem, max flow or Hopcroft-Karp is preferred.

## Python Solution

```python
from collections import deque

def solve():
  n, m, k = map(int, input().split())

  # Node numbering: 0=source, 1..n=boys, n+1..n+m=girls, n+m+1=sink
  source = 0
  sink = n + m + 1
  total_nodes = n + m + 2

  # Adjacency list for flow network
  adj = [[] for _ in range(total_nodes)]
  capacity = {}

  def add_edge(u, v, cap):
    adj[u].append(v)
    adj[v].append(u)
    capacity[(u, v)] = cap
    capacity[(v, u)] = 0  # Reverse edge for residual graph

  # Source to all boys
  for boy in range(1, n + 1):
    add_edge(source, boy, 1)

  # All girls to sink
  for girl in range(n + 1, n + m + 1):
    add_edge(girl, sink, 1)

  # Compatible pairs
  for _ in range(k):
    a, b = map(int, input().split())
    boy_node = a
    girl_node = n + b
    add_edge(boy_node, girl_node, 1)

  def bfs():
    """Find augmenting path using BFS"""
    parent = [-1] * total_nodes
    visited = [False] * total_nodes
    visited[source] = True
    queue = deque([source])

    while queue:
      u = queue.popleft()
      for v in adj[u]:
        if not visited[v] and capacity.get((u, v), 0) > 0:
          visited[v] = True
          parent[v] = u
          if v == sink:
            return parent
          queue.append(v)
    return None

  def max_flow():
    """Edmonds-Karp (BFS-based Ford-Fulkerson)"""
    total_flow = 0

    while True:
      parent = bfs()
      if parent is None:
        break

      # Find bottleneck
      path_flow = float('inf')
      v = sink
      while v != source:
        u = parent[v]
        path_flow = min(path_flow, capacity[(u, v)])
        v = u

      # Update residual capacities
      v = sink
      while v != source:
        u = parent[v]
        capacity[(u, v)] -= path_flow
        capacity[(v, u)] += path_flow
        v = u

      total_flow += path_flow

    return total_flow

  result = max_flow()
  print(result)

  # Extract actual matching from residual graph
  for boy in range(1, n + 1):
    for girl in range(n + 1, n + m + 1):
      # If reverse edge has capacity 1, flow went through this edge
      if capacity.get((girl, boy), 0) == 1:
        print(boy, girl - n)
        break

if __name__ == "__main__":
  solve()
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Wrong node numbering | Source/sink overlap with boys/girls | Use distinct ranges: S=0, boys=1..n, girls=n+1..n+m, T=n+m+1 |
| Missing reverse edges | Cannot find augmenting paths | Always add reverse edge with capacity 0 |
| Wrong capacity direction | Flow goes backwards | S->boys, boys->girls, girls->T (not reversed) |
| Forgetting to extract pairs | Only output count | Check residual graph: reverse edge capacity = flow |
| Using capacity > 1 | Multiple matches per person | All edges must have capacity exactly 1 |
| 1-indexed vs 0-indexed | Off-by-one errors | Be consistent; problem uses 1-indexed |

## Complexity Analysis

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|-----------------|------------------|----------|
| Ford-Fulkerson (DFS) | O(V * E) | O(V + E) | Simple implementation |
| Edmonds-Karp (BFS) | O(V * E^2) | O(V + E) | Guaranteed termination |
| Hopcroft-Karp | O(E * sqrt(V)) | O(V + E) | Large bipartite graphs |
| Dinic's Algorithm | O(V^2 * E) | O(V + E) | General max flow |

For this problem with V = n + m <= 1000 and E = k <= 1000:
- **Edmonds-Karp**: O(V * E) = O(1000 * 1000) = O(10^6) - fast enough
- **Hopcroft-Karp**: O(E * sqrt(V)) = O(1000 * 32) = O(32000) - even faster

## Related Problems

- **CSES Download Speed** (1694): Pure max flow problem
- **CSES Police Chase** (1695): Min cut = max flow
- **LeetCode 785**: Is Graph Bipartite?
- **LeetCode 1066**: Campus Bikes II (weighted matching)
