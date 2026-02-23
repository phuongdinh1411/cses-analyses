---
layout: simple
title: "Graph Problem Patterns"
permalink: /pattern/graph
---

# Graph Problem Patterns — Comprehensive Guide

Graphs model relationships: cities connected by roads, users in a social network, tasks with dependencies. This guide covers **every major graph technique** for competitive programming and interviews.

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| Traverse / explore a graph | BFS / DFS | [1](#1-graph-traversals) |
| Find **shortest path** | Dijkstra / Bellman-Ford / Floyd / 0-1 BFS | [2](#2-shortest-paths) |
| Find **minimum spanning tree** | Kruskal / Prim | [3](#3-minimum-spanning-tree) |
| Process nodes in **dependency order** | Topological Sort | [4](#4-topological-sort) |
| Find **strongly connected components** | Tarjan / Kosaraju | [5](#5-strongly-connected-components) |
| Find **bridges / articulation points** | Tarjan's bridge-finding | [6](#6-bridges-and-articulation-points) |
| Check if graph is **bipartite** | BFS/DFS 2-coloring | [7](#7-bipartite-graphs) |
| Detect **cycles** | DFS coloring / Union-Find | [8](#8-cycle-detection) |
| Manage **connected components** dynamically | Union-Find (DSU) | [9](#9-union-find-dsu) |
| Find **max flow / min cut** | Ford-Fulkerson / Dinic's | [10](#10-network-flow) |
| Find **maximum matching** | Hopcroft-Karp / Hungarian | [11](#11-matching) |
| Find **Eulerian path/circuit** | Hierholzer's | [12](#12-eulerian-paths-and-circuits) |
| Solve boolean satisfiability | 2-SAT via SCC | [13](#13-2-sat) |
| Handle **multi-source** shortest path | Multi-source BFS / virtual node | [14](#14-multi-source-and-virtual-nodes) |
| DP on a graph | DP on DAG / shortest path DP | [15](#15-dp-on-graphs) |

---

## Table of Contents

1. [Graph Traversals](#1-graph-traversals)
2. [Shortest Paths](#2-shortest-paths)
3. [Minimum Spanning Tree](#3-minimum-spanning-tree)
4. [Topological Sort](#4-topological-sort)
5. [Strongly Connected Components](#5-strongly-connected-components)
6. [Bridges and Articulation Points](#6-bridges-and-articulation-points)
7. [Bipartite Graphs](#7-bipartite-graphs)
8. [Cycle Detection](#8-cycle-detection)
9. [Union-Find (DSU)](#9-union-find-dsu)
10. [Network Flow](#10-network-flow)
11. [Matching](#11-matching)
12. [Eulerian Paths and Circuits](#12-eulerian-paths-and-circuits)
13. [2-SAT](#13-2-sat)
14. [Multi-Source and Virtual Nodes](#14-multi-source-and-virtual-nodes)
15. [DP on Graphs](#15-dp-on-graphs)
16. [Pattern Recognition Cheat Sheet](#16-pattern-recognition-cheat-sheet)

---

## 0. Graph Representations

Before anything, know how to store a graph.

### Adjacency List (most common)

```python
# Unweighted
n = 5
adj = [[] for _ in range(n)]
adj[0].append(1)  # edge 0 -> 1
adj[1].append(0)  # undirected: add both

# Weighted
adj[0].append((1, 10))  # edge 0 -> 1, weight 10
```

### Adjacency Matrix

```python
# Good for dense graphs or Floyd-Warshall
INF = float('inf')
dist = [[INF] * n for _ in range(n)]
dist[0][1] = 10  # edge 0 -> 1, weight 10
for i in range(n):
    dist[i][i] = 0
```

### Edge List

```python
# Good for Kruskal's (sort by weight)
edges = [(weight, u, v), ...]
edges.sort()
```

### When to Use Which

| Representation | Space | Check edge? | Iterate neighbors | Best for |
|---------------|-------|-------------|-------------------|----------|
| Adjacency List | O(V+E) | O(degree) | O(degree) | Most problems |
| Adjacency Matrix | O(V^2) | O(1) | O(V) | Dense, Floyd-Warshall |
| Edge List | O(E) | O(E) | O(E) | Kruskal's, edge sorting |

---

## 1. Graph Traversals

### BFS (Breadth-First Search)

Explores level by level. Finds **shortest path in unweighted graphs**.

```python
from collections import deque

def bfs(start, adj, n):
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    parent = [-1] * n

    while queue:
        node = queue.popleft()
        for nb in adj[node]:
            if dist[nb] == -1:
                dist[nb] = dist[node] + 1
                parent[nb] = node
                queue.append(nb)

    return dist, parent
```

### DFS (Depth-First Search)

Explores as deep as possible. Used for cycle detection, topological sort, SCC, bridges.

```python
def dfs(start, adj, n):
    visited = [False] * n
    order = []  # visit order

    def visit(node):
        visited[node] = True
        order.append(node)
        for nb in adj[node]:
            if not visited[nb]:
                visit(nb)

    visit(start)
    return order
```

### Iterative DFS (for large graphs in Python)

```python
def dfs_iterative(start, adj, n):
    visited = [False] * n
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if visited[node]:
            continue
        visited[node] = True
        order.append(node)
        for nb in adj[node]:
            if not visited[nb]:
                stack.append(nb)

    return order
```

### BFS vs DFS

| | BFS | DFS |
|--|-----|-----|
| Data structure | Queue | Stack / recursion |
| Finds shortest path? | Yes (unweighted) | No |
| Memory | O(width of graph) | O(depth of graph) |
| Use for | Shortest path, level-order | Cycle detection, topo sort, SCC |

---

## 2. Shortest Paths

The most important graph family. Five algorithms for different situations.

### Algorithm Selection Guide

```
What kind of graph?
    |
    +-- Unweighted? --> BFS  O(V + E)
    |
    +-- Non-negative weights? --> Dijkstra  O((V + E) log V)
    |
    +-- Negative weights, no negative cycle? --> Bellman-Ford  O(VE)
    |
    +-- All pairs? --> Floyd-Warshall  O(V^3)
    |
    +-- Weights are only 0 and 1? --> 0-1 BFS  O(V + E)
    |
    +-- DAG? --> Topological Sort + relaxation  O(V + E)
```

### 2.1 Dijkstra's Algorithm

**When**: Non-negative edge weights, single source.

```python
import heapq

def dijkstra(start, adj, n):
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]  # (distance, node)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue  # outdated entry, skip
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist
```

**Why it works**: Always processes the unvisited node with the smallest distance. Since all weights are non-negative, once a node is processed, its distance is final.

**Common mistake**: Using Dijkstra with negative weights. It fails because a "processed" node might get a shorter path later through a negative edge.

### 2.2 Bellman-Ford

**When**: Negative edge weights allowed. Detects negative cycles.

```python
def bellman_ford(start, edges, n):
    dist = [float('inf')] * n
    dist[start] = 0

    # relax all edges N-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # check for negative cycles (Nth iteration)
    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, has_negative_cycle
```

**Why N-1 iterations?** The shortest path has at most N-1 edges. Each iteration relaxes paths of one more edge. If the Nth iteration still improves something, there's a negative cycle.

### 2.3 Floyd-Warshall

**When**: All-pairs shortest paths. Small graph (V <= 500).

```python
def floyd_warshall(n, dist):
    """dist[i][j] = weight of edge i->j (INF if no edge, 0 for i==i)."""
    for k in range(n):          # intermediate node
        for i in range(n):      # source
            for j in range(n):  # destination
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

**Why it works**: `dp[i][j][k]` = shortest path from i to j using only nodes 0..k as intermediates. The three nested loops consider each possible intermediate node.

**Bonus**: Detect negative cycles by checking if `dist[i][i] < 0` for any i.

### 2.4 0-1 BFS

**When**: Edge weights are only **0 or 1**. Like BFS but uses a deque.

```python
from collections import deque

def bfs_01(start, adj, n):
    dist = [float('inf')] * n
    dist[start] = 0
    dq = deque([start])

    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)  # weight 0: high priority (front)
                else:
                    dq.append(v)      # weight 1: low priority (back)

    return dist
```

**Why it works**: Weight-0 edges don't increase distance, so those neighbors should be processed at the same "level" as the current node (front of deque). Weight-1 edges go to the next level (back of deque). This is exactly BFS with two levels of priority.

### 2.5 Shortest Path on DAG

**When**: Directed acyclic graph. Process in topological order.

```python
from collections import deque

def shortest_path_dag(adj, n, start):
    # topological sort
    in_deg = [0] * n
    for u in range(n):
        for v, w in adj[u]:
            in_deg[v] += 1
    queue = deque(i for i in range(n) if in_deg[i] == 0)
    topo = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v, w in adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    # relax in topo order
    dist = [float('inf')] * n
    dist[start] = 0
    for u in topo:
        if dist[u] == float('inf'):
            continue
        for v, w in adj[u]:
            dist[v] = min(dist[v], dist[u] + w)

    return dist
```

### Shortest Path Summary

| Algorithm | Time | Space | Weights | Negative cycle? |
|-----------|------|-------|---------|----------------|
| BFS | O(V+E) | O(V) | Unweighted | N/A |
| Dijkstra | O((V+E)log V) | O(V) | Non-negative | N/A |
| Bellman-Ford | O(VE) | O(V) | Any | Detects |
| Floyd-Warshall | O(V^3) | O(V^2) | Any | Detects |
| 0-1 BFS | O(V+E) | O(V) | 0 or 1 | N/A |
| DAG relaxation | O(V+E) | O(V) | Any (DAG) | N/A (no cycles) |

---

## 3. Minimum Spanning Tree

**Problem**: Connect all nodes with minimum total edge weight.

### 3.1 Kruskal's Algorithm

**Idea**: Sort edges by weight, greedily add the lightest edge that doesn't create a cycle. Uses Union-Find.

```python
def kruskal(n, edges):
    """edges = [(weight, u, v), ...]"""
    edges.sort()
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a == b:
            return False
        if rank[a] < rank[b]:
            a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]:
            rank[a] += 1
        return True

    mst_weight = 0
    mst_edges = []
    for w, u, v in edges:
        if union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break

    return mst_weight, mst_edges
```

### 3.2 Prim's Algorithm

**Idea**: Grow the MST from a starting node. Always add the lightest edge connecting the MST to a non-MST node.

```python
import heapq

def prim(adj, n, start=0):
    visited = [False] * n
    pq = [(0, start)]  # (weight, node)
    mst_weight = 0
    edges_used = 0

    while pq and edges_used < n:
        w, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        mst_weight += w
        edges_used += 1
        for v, weight in adj[u]:
            if not visited[v]:
                heapq.heappush(pq, (weight, v))

    return mst_weight
```

### Kruskal vs Prim

| | Kruskal | Prim |
|--|---------|------|
| Time | O(E log E) | O((V+E) log V) |
| Best for | Sparse graphs (E ~ V) | Dense graphs (E ~ V^2) |
| Data structure | Union-Find | Priority Queue |
| Edge list needed | Yes | No (adjacency list) |

### MST Properties

| Property | Explanation |
|----------|-------------|
| Cut Property | Lightest edge crossing any cut is in MST |
| Cycle Property | Heaviest edge in any cycle is NOT in MST |
| Uniqueness | MST is unique if all edge weights are distinct |
| N-1 edges | MST of N nodes always has exactly N-1 edges |

---

## 4. Topological Sort

**Problem**: Order nodes so that for every edge u -> v, u comes before v. Only works on **DAGs** (directed acyclic graphs).

### 4.1 Kahn's Algorithm (BFS-based)

```python
from collections import deque

def topo_sort_kahn(adj, n):
    in_deg = [0] * n
    for u in range(n):
        for v in adj[u]:
            in_deg[v] += 1

    queue = deque(i for i in range(n) if in_deg[i] == 0)
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    if len(order) != n:
        return None  # cycle detected!
    return order
```

### 4.2 DFS-based

```python
def topo_sort_dfs(adj, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    order = []
    has_cycle = [False]

    def dfs(u):
        if has_cycle[0]:
            return
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                has_cycle[0] = True  # back edge = cycle
                return
            if color[v] == WHITE:
                dfs(v)
        color[u] = BLACK
        order.append(u)

    for i in range(n):
        if color[i] == WHITE:
            dfs(i)

    if has_cycle[0]:
        return None
    return order[::-1]  # reverse post-order
```

### Applications

| Application | How topo sort helps |
|-------------|-------------------|
| Course scheduling | Prerequisites form a DAG |
| Build systems (Make) | Dependencies must be built first |
| Shortest/longest path in DAG | Relax edges in topo order |
| DP on DAG | Process states in topo order |
| Cycle detection (directed) | If topo sort fails, cycle exists |

---

## 5. Strongly Connected Components

**Problem**: Find maximal groups where every node can reach every other node in a **directed graph**.

```
    1 --> 2 --> 5 --> 6
    ^    /      ^    /
    |   v       |   v
    4 <-3       8 <-7

SCC 1: {1, 2, 3, 4}   (cycle: 1->2->3->4->1)
SCC 2: {5, 6, 7, 8}   (cycle: 5->6->7->8->5)
```

### 5.1 Kosaraju's Algorithm

**Idea**: Two DFS passes. First on original graph (get finish order), then on reversed graph (in reverse finish order).

```python
def kosaraju(adj, n):
    # Step 1: DFS on original, record finish order
    visited = [False] * n
    finish_order = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        finish_order.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    # Step 2: build reverse graph
    rev = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            rev[v].append(u)

    # Step 3: DFS on reverse in reverse finish order
    visited = [False] * n
    sccs = []

    def dfs2(u, component):
        visited[u] = True
        component.append(u)
        for v in rev[u]:
            if not visited[v]:
                dfs2(v, component)

    for u in reversed(finish_order):
        if not visited[u]:
            component = []
            dfs2(u, component)
            sccs.append(component)

    return sccs
```

### 5.2 Tarjan's Algorithm

**Idea**: Single DFS. Track discovery time and the lowest reachable discovery time (low-link). When `low[u] == disc[u]`, node u is the root of an SCC.

```python
def tarjan_scc(adj, n):
    disc = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    stack = []
    timer = [0]
    sccs = []

    def dfs(u):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        stack.append(u)
        on_stack[u] = True

        for v in adj[u]:
            if disc[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], disc[v])

        # if u is root of SCC
        if low[u] == disc[u]:
            component = []
            while True:
                v = stack.pop()
                on_stack[v] = False
                component.append(v)
                if v == u:
                    break
            sccs.append(component)

    for i in range(n):
        if disc[i] == -1:
            dfs(i)

    return sccs
```

### SCC Condensation

After finding SCCs, collapse each SCC into a single node to get a **DAG**. This DAG is useful for many problems.

```python
def condense(adj, n, sccs):
    comp = [0] * n  # which SCC each node belongs to
    for i, scc in enumerate(sccs):
        for node in scc:
            comp[node] = i

    m = len(sccs)
    dag = [set() for _ in range(m)]
    for u in range(n):
        for v in adj[u]:
            if comp[u] != comp[v]:
                dag[comp[u]].add(comp[v])

    return dag, comp
```

### Applications

| Application | How SCC helps |
|-------------|---------------|
| 2-SAT | Variables in same SCC must have same value |
| Reachability | Condense to DAG, then process DAG |
| Minimum edges to make strongly connected | Condense + count sources/sinks |

---

## 6. Bridges and Articulation Points

### Bridge

An edge whose removal **disconnects** the graph.

### Articulation Point

A node whose removal disconnects the graph.

```
    1 --- 2 --- 5 --- 6
    |    /      |    /
    |   /       |   /
    3 -/        7 -/
         ^
    bridge: 2-5 (removing it disconnects the two halves)
    articulation points: 2, 5
```

### Finding Bridges

```python
def find_bridges(adj, n):
    disc = [-1] * n
    low = [0] * n
    timer = [0]
    bridges = []

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1

        for v in adj[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
            else:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)

    return bridges
```

### Finding Articulation Points

```python
def find_articulation_points(adj, n):
    disc = [-1] * n
    low = [0] * n
    timer = [0]
    is_ap = [False] * n

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0

        for v in adj[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])

                # Case 1: u is root and has 2+ children
                if parent == -1 and children > 1:
                    is_ap[u] = True
                # Case 2: u is not root and no back edge from v's subtree
                #         goes above u
                if parent != -1 and low[v] >= disc[u]:
                    is_ap[u] = True
            else:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)

    return [i for i in range(n) if is_ap[i]]
```

### Understanding `low[v]`

`low[v]` = the earliest discovery time reachable from v's subtree via back edges. If `low[v] > disc[u]`, no back edge from v's subtree reaches above u, so edge u-v is a bridge.

```
disc:     0    1    2    3
          u -- a -- b -- c
          |              |
          +--------------+  (back edge c -> u)

low[c] = 0 (can reach u via back edge)
low[b] = 0 (inherits from c)
low[a] = 0 (inherits from b)

Edge u-a: low[a]=0 not > disc[u]=0  -> NOT a bridge (correct: back edge saves it)
```

---

## 7. Bipartite Graphs

**Problem**: Can we 2-color the graph such that no adjacent nodes share a color?

```
Bipartite:           Not bipartite:
  1 --- 2              1 --- 2
  |     |              |   / |
  3 --- 4              3 --- 4
                       (odd cycle 1-2-3)
```

### Check + Color

```python
from collections import deque

def is_bipartite(adj, n):
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return False, None

    return True, color
```

### Key Property

A graph is bipartite **if and only if** it contains no odd-length cycle.

### Applications

| Application | Connection |
|-------------|-----------|
| Task assignment (workers to jobs) | Bipartite matching |
| Graph coloring (2 colors) | Bipartite check |
| Building teams (no conflicts) | 2-coloring |
| Maximum independent set on bipartite | Konig's theorem |

---

## 8. Cycle Detection

### Directed Graph: DFS Coloring

Three states: WHITE (unvisited), GRAY (in current DFS path), BLACK (finished).

```python
def has_cycle_directed(adj, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(u):
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                return True   # back edge = cycle!
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    return any(color[i] == WHITE and dfs(i) for i in range(n))
```

**Back edge** (GRAY -> GRAY) = cycle. Cross edge (GRAY -> BLACK) = no cycle.

### Undirected Graph: DFS with Parent

```python
def has_cycle_undirected(adj, n):
    visited = [False] * n

    def dfs(u, parent):
        visited[u] = True
        for v in adj[u]:
            if v == parent:
                continue
            if visited[v]:
                return True   # already visited and not parent = cycle
            if dfs(v, u):
                return True
        return False

    return any(not visited[i] and dfs(i, -1) for i in range(n))
```

### Undirected Graph: Union-Find

```python
def has_cycle_uf(edges, n):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return True   # already connected = cycle
        parent[pu] = pv

    return False
```

### Finding the Actual Cycle

```python
def find_cycle_directed(adj, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    parent = [-1] * n
    cycle_start = cycle_end = -1

    def dfs(u):
        nonlocal cycle_start, cycle_end
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                cycle_start = v
                cycle_end = u
                return True
            if color[v] == WHITE:
                parent[v] = u
                if dfs(v):
                    return True
        color[u] = BLACK
        return False

    for i in range(n):
        if color[i] == WHITE and dfs(i):
            break

    if cycle_start == -1:
        return []

    # reconstruct
    cycle = [cycle_start]
    v = cycle_end
    while v != cycle_start:
        cycle.append(v)
        v = parent[v]
    cycle.reverse()
    return cycle
```

---

## 9. Union-Find (DSU)

**Problem**: Dynamically merge sets and check if two elements are in the same set.

### Implementation

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        # union by rank
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        self.components -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def get_size(self, a):
        return self.size[self.find(a)]
```

### Complexity

| Operation | Time |
|-----------|------|
| find | O(alpha(N)) ~ O(1) amortized |
| union | O(alpha(N)) ~ O(1) amortized |

`alpha(N)` is the inverse Ackermann function --- grows so slowly it's effectively constant (alpha(10^80) = 4).

### Applications

| Problem | DSU usage |
|---------|----------|
| Kruskal's MST | Check if edge creates cycle |
| Dynamic connectivity | Are u and v connected? |
| Number of components | Track `components` counter |
| Cycle detection (undirected) | Union returns false = cycle |
| Offline LCA (Tarjan's) | Merge subtrees during DFS |

### Weighted DSU

Track extra info along edges (e.g., distance to root, parity):

```python
class WeightedDSU:
    """Track relative weights: weight[x] = 'distance' from x to root."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.weight = [0] * n  # weight[x] = relative weight to parent

    def find(self, x):
        if self.parent[x] == x:
            return x, 0
        root, w = self.find(self.parent[x])
        self.parent[x] = root
        self.weight[x] += w
        return root, self.weight[x]

    def union(self, a, b, w):
        """Declare: weight[a] - weight[b] = w"""
        root_a, wa = self.find(a)
        root_b, wb = self.find(b)
        if root_a == root_b:
            return wa - wb == w  # check consistency
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
            wa, wb = wb, wa
            w = -w
        self.parent[root_b] = root_a
        self.weight[root_b] = wa - wb - w
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True
```

---

## 10. Network Flow

**Problem**: Find the maximum flow from source s to sink t through a network of capacitated edges.

### Max Flow / Min Cut Theorem

**Max flow = Min cut**. The maximum flow equals the minimum total capacity of edges that, if removed, disconnect s from t.

### Dinic's Algorithm

The most practical max-flow algorithm. Runs in O(V^2 * E), but much faster in practice.

```python
from collections import deque

class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        self.graph[u].append([v, cap, len(self.graph[v])])      # forward
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])    # reverse

    def bfs(self, s, t, level):
        level[:] = [-1] * self.n
        level[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v, cap, _ in self.graph[u]:
                if cap > 0 and level[v] == -1:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[t] != -1

    def dfs(self, u, t, flow, level, iter_):
        if u == t:
            return flow
        while iter_[u] < len(self.graph[u]):
            v, cap, rev = self.graph[u][iter_[u]]
            if cap > 0 and level[v] == level[u] + 1:
                d = self.dfs(v, t, min(flow, cap), level, iter_)
                if d > 0:
                    self.graph[u][iter_[u]][1] -= d
                    self.graph[v][rev][1] += d
                    return d
            iter_[u] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        level = [0] * self.n
        while self.bfs(s, t, level):
            iter_ = [0] * self.n
            while True:
                d = self.dfs(s, t, float('inf'), level, iter_)
                if d == 0:
                    break
                flow += d
        return flow
```

### Common Flow Reductions

| Problem | Reduction |
|---------|----------|
| Maximum bipartite matching | Max flow from source to left, left to right, right to sink |
| Minimum vertex cut | Split each node into in-node and out-node with capacity 1 |
| Edge-disjoint paths | Each edge capacity = 1 |
| Project selection | Min cut with profits/costs |

---

## 11. Matching

### Bipartite Matching (Kuhn's / Hungarian)

**Problem**: Find the maximum set of edges with no shared endpoints in a bipartite graph.

```python
def max_bipartite_matching(adj_left, n_left, n_right):
    """adj_left[u] = list of right nodes that left node u can match with."""
    match_right = [-1] * n_right

    def dfs(u, visited):
        for v in adj_left[u]:
            if not visited[v]:
                visited[v] = True
                if match_right[v] == -1 or dfs(match_right[v], visited):
                    match_right[v] = u
                    return True
        return False

    matching = 0
    for u in range(n_left):
        visited = [False] * n_right
        if dfs(u, visited):
            matching += 1

    return matching
```

### Konig's Theorem (Bipartite Only)

```
Maximum Matching = Minimum Vertex Cover
                 = Total Nodes - Maximum Independent Set
```

### General Matching

For non-bipartite graphs, use **Edmond's blossom algorithm** (complex, usually use a library).

---

## 12. Eulerian Paths and Circuits

### Definitions

| | Visits every **edge** exactly once |
|--|---|
| **Eulerian Circuit** | Starts and ends at the same node |
| **Eulerian Path** | Starts and ends at different nodes |

### Existence Conditions

| Graph type | Eulerian Circuit | Eulerian Path |
|-----------|-----------------|---------------|
| Undirected | All vertices have even degree | Exactly 0 or 2 vertices have odd degree |
| Directed | in-degree = out-degree for all | At most 1 node with out-in=1 (start), at most 1 with in-out=1 (end) |

### Hierholzer's Algorithm

```python
def find_eulerian_circuit(adj, n):
    """adj[u] = deque of neighbors (consumed during traversal)."""
    from collections import deque

    # convert adjacency list to deques for O(1) popleft
    adj_deque = [deque(adj[i]) for i in range(n)]

    stack = [0]  # start node
    circuit = []

    while stack:
        u = stack[-1]
        if adj_deque[u]:
            v = adj_deque[u].popleft()
            stack.append(v)
        else:
            circuit.append(stack.pop())

    return circuit[::-1]
```

For **directed** graphs, consume `adj_deque[u].popleft()` and mark edges. For **undirected**, need to mark edges as used (by index) to avoid traversing both directions.

---

## 13. 2-SAT

**Problem**: Given boolean variables and clauses of the form (x OR y), find a satisfying assignment.

### Reduction to SCC

Each variable x has two nodes: x and NOT x. Each clause (a OR b) becomes two implications:

```
(a OR b) = (NOT a -> b) AND (NOT b -> a)
```

Build an implication graph, find SCCs. If x and NOT x are in the same SCC, no solution exists.

```python
def solve_2sat(n, clauses):
    """
    n: number of variables (0 to n-1)
    clauses: list of (a, b) where a, b are literals
             positive literal i means x_i = True
             negative literal ~i (stored as n+i) means x_i = False
    """
    # node mapping: variable i -> node i (True), node n+i (False)
    total = 2 * n
    adj = [[] for _ in range(total)]

    def neg(x):
        return x + n if x < n else x - n

    for a, b in clauses:
        # (a OR b) -> (NOT a -> b) AND (NOT b -> a)
        adj[neg(a)].append(b)
        adj[neg(b)].append(a)

    # find SCCs (using Kosaraju's or Tarjan's)
    sccs = tarjan_scc(adj, total)

    # assign SCC ids
    comp = [0] * total
    for i, scc in enumerate(sccs):
        for node in scc:
            comp[node] = i

    # check satisfiability
    for i in range(n):
        if comp[i] == comp[i + n]:
            return None  # x and NOT x in same SCC -> unsatisfiable

    # assign values: if comp[i] > comp[i+n], x_i = True
    # (Tarjan returns SCCs in reverse topological order)
    values = [comp[i] > comp[i + n] for i in range(n)]
    return values
```

### Common 2-SAT Encodings

| Constraint | Clause(s) |
|-----------|----------|
| x must be True | (x OR x) |
| x OR y | (x OR y) |
| x AND y | (x OR x) AND (y OR y) |
| x XOR y | (x OR y) AND (NOT x OR NOT y) |
| x = y | (x OR NOT y) AND (NOT x OR y) |
| x implies y | (NOT x OR y) |
| At most one of x,y | (NOT x OR NOT y) |

---

## 14. Multi-Source and Virtual Nodes

### Multi-Source BFS

**Problem**: Find the shortest distance from **any source** to each node.

Simply start BFS with all sources in the queue at distance 0.

```python
from collections import deque

def multi_source_bfs(sources, adj, n):
    dist = [-1] * n
    queue = deque()
    for s in sources:
        dist[s] = 0
        queue.append(s)

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    return dist
```

### Virtual Source / Sink

**Problem**: Shortest path from any of multiple sources, or max flow with multiple sources/sinks.

**Trick**: Create a virtual node connected to all sources (weight 0). Run single-source algorithm from virtual node.

```
Real graph:            With virtual source:

  S1    S2    S3         V (virtual)
  |     |     |         /|\
  v     v     v        / | \
  A --- B --- C      S1  S2  S3   (0-weight edges)
                      |   |   |
                      A   B   C
```

```python
# Add virtual source node n, connect to all real sources
virtual = n
adj.append([])
for s in sources:
    adj[virtual].append((s, 0))
dist = dijkstra(virtual, adj, n + 1)
```

---

## 15. DP on Graphs

### DP on DAG

Process nodes in topological order. Most DP on graphs requires no cycles.

```python
# Longest path in DAG
def longest_path(adj, n):
    in_deg = [0] * n
    for u in range(n):
        for v, w in adj[u]:
            in_deg[v] += 1

    queue = deque(i for i in range(n) if in_deg[i] == 0)
    dp = [0] * n

    while queue:
        u = queue.popleft()
        for v, w in adj[u]:
            dp[v] = max(dp[v], dp[u] + w)
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    return max(dp)
```

### Counting Paths in DAG

```python
def count_paths(adj, n, src, dst):
    in_deg = [0] * n
    for u in range(n):
        for v in adj[u]:
            in_deg[v] += 1

    queue = deque(i for i in range(n) if in_deg[i] == 0)
    dp = [0] * n
    dp[src] = 1

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            dp[v] += dp[u]
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    return dp[dst]
```

### Shortest Path as DP

Dijkstra is essentially DP with a priority queue:

```
dp[v] = min(dp[u] + weight(u, v)) for all edges (u, v)
```

Bellman-Ford is the brute-force DP:

```
dp[k][v] = min cost to reach v using at most k edges
dp[k][v] = min(dp[k-1][u] + weight(u, v)) for all edges
```

### DP on Graph with Cycles: SCC Condensation

If the graph has cycles, condense SCCs into a DAG first, then run DP on the DAG.

```
1. Find SCCs
2. Condense into DAG (each SCC = one super-node)
3. Compute value for each super-node (e.g., sum of node values in SCC)
4. Run DP on DAG
```

---

## 16. Pattern Recognition Cheat Sheet

### By Problem Type

| You see... | Think... | Section |
|------------|----------|---------|
| "Shortest path" (unweighted) | BFS | 1 |
| "Shortest path" (weighted, non-negative) | Dijkstra | 2 |
| "Shortest path" (negative weights) | Bellman-Ford | 2 |
| "All pairs shortest path" | Floyd-Warshall | 2 |
| "Minimum cost to connect all nodes" | MST (Kruskal/Prim) | 3 |
| "Order tasks with dependencies" | Topological Sort | 4 |
| "Find cycles in directed graph" | DFS coloring or Topo Sort | 8 |
| "Groups where everyone can reach everyone" | SCC (Tarjan/Kosaraju) | 5 |
| "Critical edges / nodes" | Bridges / Articulation Points | 6 |
| "Can we 2-color?" or "split into two groups" | Bipartite check | 7 |
| "Dynamic connectivity" | Union-Find (DSU) | 9 |
| "Maximum flow" or "minimum cut" | Network Flow (Dinic's) | 10 |
| "Maximum matching" | Kuhn's / Hopcroft-Karp | 11 |
| "Visit every edge once" | Eulerian path/circuit | 12 |
| "Boolean satisfiability (2 vars per clause)" | 2-SAT via SCC | 13 |
| "Multiple starting points" | Multi-source BFS / virtual node | 14 |
| "Longest path" or "count paths" | DP on DAG | 15 |

### By Constraint Size

| V, E range | Feasible algorithms |
|------------|-------------------|
| V <= 500 | Floyd-Warshall O(V^3), Brute force |
| V <= 5,000 | Bellman-Ford O(VE), O(V^2) matching |
| V <= 10^5, E <= 10^5 | Dijkstra, BFS, DFS, Topo Sort, SCC, DSU |
| V <= 10^5, E <= 10^6 | Same as above (watch constant factors) |
| V <= 10^6 | BFS/DFS only, simple DSU |

### Algorithm Complexity Reference

| Algorithm | Time | Space |
|-----------|------|-------|
| BFS / DFS | O(V + E) | O(V) |
| Dijkstra | O((V + E) log V) | O(V) |
| Bellman-Ford | O(VE) | O(V) |
| Floyd-Warshall | O(V^3) | O(V^2) |
| 0-1 BFS | O(V + E) | O(V) |
| Kruskal | O(E log E) | O(V) |
| Prim | O((V + E) log V) | O(V) |
| Topological Sort | O(V + E) | O(V) |
| SCC (Tarjan/Kosaraju) | O(V + E) | O(V) |
| Bridges / APs | O(V + E) | O(V) |
| Bipartite Check | O(V + E) | O(V) |
| DSU (per operation) | O(alpha(V)) | O(V) |
| Dinic's Max Flow | O(V^2 E) | O(V + E) |
| Kuhn's Matching | O(V E) | O(V) |
| Hierholzer (Euler) | O(E) | O(E) |
| 2-SAT | O(V + E) | O(V) |

### Decision Flowchart

```
What is the problem about?
    |
    +-- Finding shortest distances?
    |       |
    |       +-- Unweighted? --> BFS
    |       +-- Non-negative weights? --> Dijkstra
    |       +-- Negative weights? --> Bellman-Ford
    |       +-- All pairs (V <= 500)? --> Floyd-Warshall
    |       +-- Weights 0 or 1? --> 0-1 BFS
    |       +-- DAG? --> Topo sort + relax
    |
    +-- Connecting components?
    |       |
    |       +-- Minimum cost? --> MST (Kruskal/Prim)
    |       +-- Dynamic union/check? --> DSU
    |
    +-- Ordering / dependencies?
    |       |
    |       +-- Linear order? --> Topological Sort
    |       +-- Satisfiability? --> 2-SAT
    |
    +-- Structural analysis?
    |       |
    |       +-- Strongly connected groups? --> SCC
    |       +-- Critical edges? --> Bridges
    |       +-- Critical nodes? --> Articulation Points
    |       +-- Two-colorable? --> Bipartite check
    |       +-- Has cycle? --> DFS coloring / DSU
    |
    +-- Optimization on edges?
    |       |
    |       +-- Maximum flow? --> Dinic's
    |       +-- Maximum matching? --> Kuhn's / Hopcroft-Karp
    |       +-- Visit every edge once? --> Eulerian (Hierholzer)
    |
    +-- Counting / DP?
            |
            +-- Has cycles? --> Condense SCCs to DAG, then DP
            +-- DAG? --> DP in topological order
```
