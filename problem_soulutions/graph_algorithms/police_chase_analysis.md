---
layout: problem-analysis
title: "Police Chase"
difficulty: Hard
tags: [graph, max-flow, min-cut, ford-fulkerson]
cses_link: https://cses.fi/problemset/task/1695
---

# Police Chase

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find minimum streets to block to disconnect crossing 1 from crossing n |
| Type | Minimum Cut (dual of Maximum Flow) |
| Key Theorem | Max-Flow Min-Cut Theorem |
| Time Complexity | O(V * E^2) using Edmonds-Karp |
| Space Complexity | O(V^2) for adjacency matrix |

## Learning Goals

After completing this problem, you will understand:

1. **Max-Flow Min-Cut Theorem**: The value of the maximum flow equals the capacity of the minimum cut
2. **Finding actual cut edges**: How to identify which edges form the minimum cut after running max flow
3. **Residual graph analysis**: Using BFS/DFS on residual graph to partition vertices into S and T sets
4. **Flow network modeling**: Converting graph problems into flow problems with unit capacities

## Problem Statement

Kaaleppi has just robbed a bank and is trying to escape from the police. The city has `n` crossings and `m` streets between them. Your task is to find the **minimum number of streets** that must be blocked so that the robber cannot reach crossing `n` from crossing 1.

**Input:**
- First line: integers `n` and `m` (2 <= n <= 500, 1 <= m <= 1000)
- Next `m` lines: two integers `a` and `b` describing a street between crossings `a` and `b`

**Output:**
- First line: minimum number `k` of streets to block
- Next `k` lines: the blocked streets (any valid solution)

**Example:**
```
Input:
4 5
1 2
1 3
2 3
2 4
3 4

Output:
2
1 2
1 3
```

## Key Insight: Max-Flow Min-Cut Theorem

The fundamental insight is the **Max-Flow Min-Cut Theorem**:

> In any flow network, the value of the maximum flow from source to sink equals the capacity of the minimum cut separating source from sink.

For this problem:
- **Source** = crossing 1 (bank location)
- **Sink** = crossing n (escape destination)
- **Edge capacity** = 1 (each street can be blocked once)
- **Max flow value** = minimum number of streets to block

## Algorithm

### Step 1: Run Max Flow Algorithm

Use Ford-Fulkerson (with BFS = Edmonds-Karp) to find maximum flow from node 1 to node n.

### Step 2: Find the Minimum Cut

After max flow completes, the residual graph reveals the cut:

1. **BFS/DFS from source** in the residual graph (only follow edges with remaining capacity > 0)
2. **Set S** = all nodes reachable from source
3. **Set T** = all remaining nodes (including sink)

### Step 3: Identify Cut Edges

Cut edges are original edges `(u, v)` where:
- `u` is in set S (reachable from source)
- `v` is in set T (not reachable from source)
- The edge is **saturated** (residual capacity from u to v is 0)

## Why This Works

```
After running max flow:

Original Graph              Residual Graph
    1 -----> 2                  1 - - -> 2
    |        |                  |        |
    v        v                  x        v
    3 -----> 4                  3 -----> 4

Saturated edges (capacity used up) form the bottleneck.
In residual graph, we cannot reach nodes beyond saturated edges.

S = {1}          (reachable from source)
T = {2, 3, 4}    (not reachable)

Cut edges: (1,2) and (1,3) - both saturated, cross from S to T
```

The saturated edges are exactly where flow "gets stuck" - removing them disconnects source from sink.

## Visual Diagram

```
EXAMPLE: n=4, m=5

Initial Graph (all capacities = 1):

       [1]----(1)---->[2]
        |              |
       (1)            (1)
        |              |
        v              v
       [3]----(1)---->[4]
        \              ^
         \----(1)-----/

After Max Flow = 2:

       [1]- - -(0)- - >[2]     (saturated, residual=0)
        |              |
       (0)            (1)
        |              |
        v              v
       [3]----(1)---->[4]
                       ^
          (0: saturated)

Flow paths found:
  Path 1: 1 -> 2 -> 4  (flow = 1)
  Path 2: 1 -> 3 -> 4  (flow = 1)

Residual Graph Analysis:
  - BFS from node 1
  - Can reach: {1} only (edges to 2 and 3 are saturated)
  - S = {1}, T = {2, 3, 4}

Minimum Cut Edges:
  - Edge (1,2): u=1 in S, v=2 in T, saturated -> CUT
  - Edge (1,3): u=1 in S, v=3 in T, saturated -> CUT

Answer: Block streets 1-2 and 1-3
```

## Dry Run

```
Input: n=4, m=5
Streets: (1,2), (1,3), (2,3), (2,4), (3,4)

Step 1: Initialize capacities (undirected = both directions)
  cap[1][2] = cap[2][1] = 1
  cap[1][3] = cap[3][1] = 1
  cap[2][3] = cap[3][2] = 1
  cap[2][4] = cap[4][2] = 1
  cap[3][4] = cap[4][3] = 1

Step 2: Find augmenting paths (BFS)

  Iteration 1:
    BFS finds path: 1 -> 2 -> 4
    Bottleneck = min(cap[1][2], cap[2][4]) = min(1,1) = 1
    Update: cap[1][2]=0, cap[2][1]=1, cap[2][4]=0, cap[4][2]=1
    Total flow = 1

  Iteration 2:
    BFS finds path: 1 -> 3 -> 4
    Bottleneck = min(cap[1][3], cap[3][4]) = min(1,1) = 1
    Update: cap[1][3]=0, cap[3][1]=1, cap[3][4]=0, cap[4][3]=1
    Total flow = 2

  Iteration 3:
    BFS from 1: can only reach {1} (cap[1][2]=0, cap[1][3]=0)
    No path to 4. Max flow complete.

Step 3: Find minimum cut
    BFS in residual graph from node 1:
    - From 1: cap[1][2]=0, cap[1][3]=0 -> cannot proceed
    - S = {1}
    - T = {2, 3, 4}

Step 4: Identify cut edges
    Check all original edges (u,v) where u in S, v in T:
    - (1,2): 1 in S, 2 in T, cap[1][2]=0 -> CUT EDGE
    - (1,3): 1 in S, 3 in T, cap[1][3]=0 -> CUT EDGE

Output:
  2
  1 2
  1 3
```

## Python Solution

```python
from collections import deque

def solve():
    n, m = map(int, input().split())

    # Adjacency list and capacity matrix
    adj = [[] for _ in range(n + 1)]
    cap = [[0] * (n + 1) for _ in range(n + 1)]

    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
        adj[a].append(b)
        adj[b].append(a)
        cap[a][b] += 1
        cap[b][a] += 1

    source, sink = 1, n

    def bfs():
        """Find augmenting path using BFS, return parent array"""
        parent = [-1] * (n + 1)
        parent[source] = source
        queue = deque([source])

        while queue:
            u = queue.popleft()
            if u == sink:
                break
            for v in adj[u]:
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    queue.append(v)

        return parent if parent[sink] != -1 else None

    # Edmonds-Karp: Find max flow
    max_flow = 0
    while True:
        parent = bfs()
        if not parent:
            break

        # Find bottleneck
        flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            flow = min(flow, cap[u][v])
            v = u

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= flow
            cap[v][u] += flow
            v = u

        max_flow += flow

    # Find nodes reachable from source in residual graph
    reachable = [False] * (n + 1)
    reachable[source] = True
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not reachable[v] and cap[u][v] > 0:
                reachable[v] = True
                queue.append(v)

    # Find cut edges: from reachable to non-reachable
    cut_edges = []
    for a, b in edges:
        if reachable[a] and not reachable[b]:
            cut_edges.append((a, b))
        elif reachable[b] and not reachable[a]:
            cut_edges.append((b, a))

    print(len(cut_edges))
    for a, b in cut_edges:
        print(a, b)

solve()
```

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Finding cut edges by checking flow instead of reachability | Multiple edges might carry flow but not be in min cut | Use BFS on residual graph to find S/T partition |
| Only checking one direction for undirected edges | Missing cut edges in reverse direction | Check both (a,b) and (b,a) for reachability |
| Using original capacities instead of residual | Doesn't reflect the actual bottleneck | Always use residual capacities after max flow |
| Outputting all saturated edges | Some saturated edges are not in the cut | Only edges crossing S to T boundary are cut edges |
| Not handling parallel edges | Capacities may be > 1 for multiple streets | Use `cap[a][b]++` instead of `cap[a][b] = 1` |

## Complexity Analysis

| Phase | Time | Space |
|-------|------|-------|
| Build graph | O(m) | O(n^2) |
| Max flow (Edmonds-Karp) | O(V * E^2) | O(n^2) |
| Find reachable set | O(V + E) | O(n) |
| Find cut edges | O(m) | O(m) |
| **Total** | **O(V * E^2)** | **O(n^2)** |

## Related Problems

| Problem | Link | Relation |
|---------|------|----------|
| Download Speed | [CSES 1694](https://cses.fi/problemset/task/1694) | Pure max flow without finding cut edges |
| School Dance | [CSES 1696](https://cses.fi/problemset/task/1696) | Max flow for bipartite matching |
| Distinct Routes | [CSES 1711](https://cses.fi/problemset/task/1711) | Finding actual flow paths |
