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
| Find **max flow / min cut** | Dinic's | [10](#10-network-flow) |
| Find **maximum matching** | Kuhn's augmenting-path DFS | [11](#11-matching) |
| Find **Eulerian path/circuit** | Hierholzer's | [12](#12-eulerian-paths-and-circuits) |
| Solve boolean satisfiability | 2-SAT via SCC | [13](#13-2-sat) |
| Handle **multi-source** shortest path | Multi-source BFS / virtual node | [14](#14-multi-source-and-virtual-nodes) |
| DP on a graph | DP on DAG / shortest path DP | [15](#15-dp-on-graphs) |

---

## How to Identify a Graph Problem

The hardest part of graph problems is usually **realizing it's a graph problem at all**. The word "graph" almost never appears. Instead, the input *is* a graph in disguise. Train your eye on these disguises:

```
The problem gives you...                          → it's a graph where...
─────────────────────────────────────────────────────────────────────────
a grid / matrix / maze / board                    → cell = node, 4/8 neighbors = edges
"prerequisites" / "depends on" / "before"         → task = node, dependency = directed edge
word/string transformations (one letter at a time)→ word = node, one-edit = edge
"x / y = 2.0" equations, currency conversions     → variable = node, ratio = weighted edge
people who "know" / "are friends with" each other → person = node, relation = edge
states reachable by a move (locks, jumps, gene)   → state = node, legal move = edge
"connected" / "province" / "group" / "island"     → connectivity → traversal or Union-Find
```

Once you know it's a graph, route to the right **family** by what the problem *asks*:

```
What does the question want?
    │
    ├── "reach / explore / count regions / shortest hops (unweighted)"
    │        → FAMILY A: Traversal (BFS/DFS/flood fill)          §1, §7, §14
    │
    ├── "cheapest / shortest path with EDGE WEIGHTS"
    │        → FAMILY B: Weighted shortest path                   §2
    │
    ├── "valid order / dependencies / can-finish / detect cycle (directed)"
    │        → FAMILY C: Topological sort / DAG                    §4, §8, §15
    │
    ├── "connect all / are these connected / merge groups / min cost to link"
    │        → FAMILY D: Union-Find & MST                          §3, §9
    │
    ├── "critical edge/node / mutually-reachable groups"
    │        → FAMILY E: Structural analysis (SCC / bridges)       §5, §6
    │
    └── "max flow / matching / visit every edge / 2-var clauses"
             → FAMILY F: Advanced (flow / matching / Euler / 2-SAT) §10–§13
```

`★ Insight ─────────────────────────────────────`
- **Weighted vs unweighted is the first fork.** "Shortest path" alone is ambiguous — if every edge costs the same (grid steps, one-letter changes), BFS is optimal and Dijkstra is overkill. The moment edges carry *different* costs, BFS breaks and you need Family B.
- **"Connected components" has two tools.** If the graph is static and you just explore it once, traversal (Family A) counts components in one pass. If edges *arrive over time* and you must answer "connected now?" between additions, Union-Find (Family D) is the tool. Same question, different pattern, decided by whether the graph is dynamic.
`─────────────────────────────────────────────────`

---

## Master LeetCode Comparison Table

The problems this guide walks through, spanning all six families. Read this table top-to-bottom once — it's the map of what each family *feels like* as a problem statement.

| # | Problem | Family | Difficulty | Graph modeling | Template variant |
|---|---------|--------|-----------|----------------|------------------|
| **200** | Number of Islands | A Traversal | Medium | grid cell = node | flood fill, count launches |
| **994** | Rotting Oranges | A Traversal | Medium | grid cell = node | **multi-source** BFS (§14) |
| **743** | Network Delay Time | B Shortest path | Medium | node = node, weighted | **Dijkstra** (§2.1) |
| **787** | Cheapest Flights ≤ K Stops | B Shortest path | Medium | city = node, weighted | **Bellman-Ford**, bounded rounds (§2.2) |
| **207** | Course Schedule | C Topo/DAG | Medium | course = node, prereq = edge | Kahn's, *can it finish?* (§4.1) |
| **210** | Course Schedule II | C Topo/DAG | Medium | course = node, prereq = edge | Kahn's, *emit the order* (§4.1) |
| **547** | Number of Provinces | D Union-Find | Medium | person = node | **DSU** component count (§9) |
| **1584** | Min Cost to Connect All Points | D MST | Medium | point = node, complete graph | **Kruskal / Prim** (§3) |
| **1192** | Critical Connections | E Structural | Hard | server = node | **bridge-finding** (§6) |
| **332** | Reconstruct Itinerary | F Advanced | Hard | airport = node, ticket = edge | **Hierholzer** Euler path (§12) |

Each row is unpacked as a full walkthrough inside its family's section below.

---

## Table of Contents

0. [Graph Representations](#0-graph-representations)
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
13.5. [Family F Anchor: Advanced Graph Patterns in LeetCode](#135-family-f-anchor-advanced-graph-patterns-in-leetcode)
14. [Multi-Source and Virtual Nodes](#14-multi-source-and-virtual-nodes)
15. [DP on Graphs](#15-dp-on-graphs)
16. [Pattern Recognition Cheat Sheet](#16-pattern-recognition-cheat-sheet)
17. [Common Mistakes](#17-common-mistakes)
18. [Practice Order](#18-practice-order)

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

**Intuition**: you want the fewest hops from a start node. BFS explores in expanding rings — all nodes 1 hop away, then all 2 hops away, and so on — so the first time you reach a node is guaranteed to be along a shortest path. The naive alternative (try every path with DFS and keep the shortest) revisits nodes through longer routes; BFS visits each node exactly once because rings never overlap.

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

**Trace** on this graph (start = 0):

```
    0 --- 1
    |     |
    2 --- 3 --- 4

adj: 0:[1,2]  1:[0,3]  2:[0,3]  3:[1,2,4]  4:[3]

pop 0 (d0)  → set dist[1]=1, dist[2]=1     queue=[1,2]
pop 1 (d1)  → set dist[3]=2                queue=[2,3]
pop 2 (d1)  → 0,3 already seen             queue=[3]
pop 3 (d2)  → set dist[4]=3                queue=[4]
pop 4 (d3)  → done

dist = [0, 1, 1, 2, 3]   (layers: {0} | {1,2} | {3} | {4})
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

### Family A anchor: which LeetCode problems this template solves

BFS/DFS traversal is the workhorse — most "grid" problems are this template with `adj` replaced by "the 4 neighbor cells." The reusable skeleton has three blanks: **what a node is**, **what an edge is**, and **what you do on visit**.

- **Flood fill / count regions** → LC **200** Number of Islands, LC 695 Max Area of Island, LC 130 Surrounded Regions, LC 733 Flood Fill.
- **Shortest hops in unweighted graph** → LC 127 Word Ladder, LC 1091 Shortest Path in Binary Matrix.
- **Multi-source BFS** (seed the queue with *all* sources) → LC **994** Rotting Oranges, LC 542 01 Matrix, LC 286 Walls and Gates.
- **2-coloring** → LC 785 Is Graph Bipartite, LC 886 Possible Bipartition.

### A.1 — Problem 200: Number of Islands

**Difficulty**: Medium

> Given an `m x n` grid of `'1'` (land) and `'0'` (water), return the number of islands. An island is land connected **4-directionally** (up/down/left/right); the grid edges are all water.

The graph is hidden: each `'1'` cell is a node, and two land cells are neighbors if they're adjacent. "Number of islands" = number of connected components. The pattern move: scan every cell; each time you hit an unvisited land cell, that's a **new** island — launch a flood fill that sinks the whole component so it's counted once.

```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    islands = 0

    def flood(r, c):
        # off-grid or water → stop
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'                 # sink it = mark visited
        flood(r + 1, c); flood(r - 1, c)
        flood(r, c + 1); flood(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':        # unvisited land = new component
                islands += 1
                flood(r, c)              # sink the entire island
    return islands
```

```
grid:                    scan order finds land at (0,0) first → island #1,
  1 1 0 0                 flood sinks the whole top-left blob:
  1 1 0 0                   (0,0)→(0,1)→(1,0)→(1,1) all become 0
  0 0 1 0                 scan continues, hits (2,2) → island #2, sink it
  0 0 0 1                 scan continues, hits (3,3) → island #3, sink it

islands = 3
```

The two blanks that make this "just the traversal template": a **node** is a land cell, and **visit** means "sink it and recurse into 4 neighbors." Everything else is the generic component-counting loop.

`★ Insight ─────────────────────────────────────`
- **Sinking = marking visited without a separate `visited` array.** Overwriting `'1'→'0'` is the visited-set, saving O(mn) space. Legitimate because the input is disposable here; if it weren't, use a real `visited` set — same pattern.
- **The outer double loop is the "launch from every component" idiom** from §1's disconnected-components fix, specialized to a grid. Each `flood` call finishes one whole component before the loop can find the next, which is exactly why the counter increments once per island.
`─────────────────────────────────────────────────`

### A.2 — Problem 994: Rotting Oranges

**Difficulty**: Medium

> In an `m x n` grid, each cell is `0` (empty), `1` (fresh orange), or `2` (rotten). Every minute, a rotten orange rots all fresh oranges **4-directionally adjacent** to it. Return the minimum minutes until no fresh orange remains, or `-1` if some fresh orange can never rot.

"Minimum minutes for rot to spread from *all* rotten oranges simultaneously" is the tell for **multi-source BFS**: the rot advances one ring per minute from many sources at once. If you ran BFS from each rotten orange separately you'd overcount; seeding the queue with *every* rotten orange at distance 0 makes them expand in lockstep, and the last ring reached is the answer.

```python
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))   # (row, col, minute) — ALL sources seeded
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        minutes = max(minutes, t)
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2          # rot it (= mark visited at time t+1)
                fresh -= 1
                queue.append((nr, nc, t + 1))

    return minutes if fresh == 0 else -1  # leftover fresh = unreachable
```

```
start (2 = rotten, 1 = fresh):     queue seeds BOTH rotten cells at t=0
  2 1 1                            ┌ (0,0,0)  (2,0,0)   fresh=4
  1 1 0
  0 1 2

t=0 pop (0,0): rot (0,1)@1, (1,0)@1        pop (2,2): rot (1,2)? no(0) / (2,1)@1
t=1 pop (0,1): rot (0,2)@2, (1,1)@2        pop (1,0): (1,1) already; pop (2,1): (1,1) already
t=2 pop (0,2),(1,1) ...                    all fresh consumed

fresh = 0 → answer = 2 minutes
```

`★ Insight ─────────────────────────────────────`
- **Multi-source BFS = single-source BFS with the queue pre-loaded.** No new algorithm — the correctness of "first time reached = shortest distance" (§1) still holds; you've just added a virtual super-source at distance 0 connected to every real source (see §14's virtual-node trick).
- **The `fresh` counter is the `-1` detector.** Any fresh orange in a region no rotten orange can reach never gets decremented, so `fresh > 0` at the end means unreachable. Cheaper than re-scanning the grid.
`─────────────────────────────────────────────────`

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

**Intuition**: with weighted edges, "fewest hops" is no longer "shortest" — a 1-hop edge of weight 100 loses to a 3-hop path of weight 6. Dijkstra greedily finalizes the *closest unfinalized* node: because every edge weight is `≥ 0`, no future path can sneak back and beat a node once it's the global minimum (any detour only adds non-negative weight). That "closest first" guarantee is exactly what breaks with negative edges — a later negative edge could undercut an already-finalized node.

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

**Why it works.** The claim to prove is the invariant the whole algorithm rests on: *when a node
`u` is popped with `d == dist[u]` (i.e. it survives the stale-entry skip), `dist[u]` is already
the true shortest distance and can never improve later.*

Suppose it could. Then some path `P` from the source to `u` is **strictly shorter** than
`dist[u]`. Walk along `P` from the source and stop at the first node `x` that has not been
finalised yet. Such an `x` always exists, because `u` itself is not finalised at the instant we
pop it. Now split `P` at `x`:

```
source  ~~~~~~~~~~~>  x  ~~~~~~~~~~~>  u
        all finalised     non-negative
        so this prefix    so this tail
        costs >= dist[x]  costs >= 0
```

- The prefix ending at `x` runs entirely through finalised nodes, so we have already relaxed our
  way to `x`: that prefix costs **at least `dist[x]`**.
- The tail from `x` to `u` is a sum of **non-negative** weights, so it only adds.
- We just popped `u`, which means `u` had the smallest tentative distance of every unfinalised
  node — and `x` is unfinalised — so **`dist[u] <= dist[x]`**.

Chaining those three: `cost(P) >= dist[x] + 0 >= dist[x] >= dist[u]`. So `P` is not shorter than
`dist[u]` after all, contradicting the assumption. No such `P` exists, and `dist[u]` is final.

Notice exactly where each hypothesis is spent. Non-negativity is used once, in the middle step. Drop
it and the tail from `x` to `u` can be *negative*, so `cost(P)` may fall below `dist[x]`, the chain
snaps, and a finalised node really can improve later. That is the whole reason a single negative
edge breaks Dijkstra — and why the fix is not a patch but a different algorithm (Bellman-Ford, §2.2).

**Trace** (start = 0; edges directed):

```
0 →4→ 1     0 →1→ 2     2 →2→ 1     1 →1→ 3     2 →5→ 3

pop (0,node0)  relax 1: dist[1]=4 push(4,1);  relax 2: dist[2]=1 push(1,2)
pop (1,node2)  relax 1: 1+2=3 < 4 → dist[1]=3 push(3,1);  relax 3: dist[3]=6 push(6,3)
pop (3,node1)  relax 3: 3+1=4 < 6 → dist[3]=4 push(4,3)
pop (4,node1)  outdated (4 > dist[1]=3) → skip
pop (4,node3)  no outgoing improvements
pop (6,node3)  outdated → skip

dist = [0, 3, 1, 4]
```

Check: `dist[1]` via 0→2→1 = 1+2 = 3 ✓;  `dist[3]` via 0→2→1→3 = 1+2+1 = 4 ✓. The stale `(4,node1)` entry is why the `if d > dist[u]: continue` guard exists.

**Common mistake**: Using Dijkstra with negative weights. It fails because a "processed" node might get a shorter path later through a negative edge.

### 2.2 Bellman-Ford

**When**: Negative edge weights allowed. Detects negative cycles.

**Intuition**: Dijkstra's greed breaks with negative edges, so drop the greed and brute-force it. A shortest path uses at most `V-1` edges, so if you *relax every edge* `V-1` times, distances are guaranteed to have propagated all the way. Each full pass lets every shortest path grow by one more edge. If a `V`-th pass *still* improves something, a negative cycle exists (you can loop it forever to keep lowering the cost).

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

**Trace** (4 nodes, start = 0; note the negative edge 2→1):

```
edges (relaxed in this order): (0,1,4)  (0,2,5)  (1,3,-3)  (2,1,-2)
init  dist = [0, ∞, ∞, ∞]

Round 1:
  (0,1,4):  dist[1] = 0+4 = 4
  (0,2,5):  dist[2] = 0+5 = 5
  (1,3,-3): dist[3] = 4-3 = 1
  (2,1,-2): 5-2 = 3 < 4 → dist[1] = 3
  → [0, 3, 5, 1]

Round 2:
  (1,3,-3): 3-3 = 0 < 1 → dist[3] = 0    (others no improvement)
  → [0, 3, 5, 0]
```

Round 2 improved `dist[3]` because round 1 had lowered `dist[1]` to 3 only *after* the (1,3) edge was relaxed — the improvement needed a second pass to propagate. Final: 0→2→1 = 3, 0→2→1→3 = 0. ✓

### 2.3 Floyd-Warshall

**When**: All-pairs shortest paths. Small graph (V <= 500).

**Intuition**: instead of running a single-source algorithm from every node, ask one question repeatedly: "does routing through node `k` shortcut any pair `(i, j)`?" Sweep `k` over every node; after allowing `0..k` as intermediates, `dist[i][j]` is optimal using only those waypoints. When `k` has covered all nodes, every pair is optimal. Three tiny loops replace `V` separate shortest-path runs.

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

**Why it works.** The state is `dp[k][i][j]` = the shortest path from `i` to `j` that is allowed to
use **only nodes `0..k−1` as intermediates**. The recurrence asks one yes/no question — *does
letting node `k` be an intermediate help?*

```
dp[k+1][i][j] = min( dp[k][i][j],              don't route through k
                     dp[k][i][k] + dp[k][k][j] )   do route through k
```

That is correct because any path allowed to use `0..k` either avoids `k` entirely (first term) or
passes through `k` exactly once, splitting into an `i → k` piece and a `k → j` piece that each use
only `0..k−1` (second term).

**Why `k` must be the outermost loop.** Look at what the recurrence consumes: every term on the
right is from layer `k`, and the result is layer `k+1`. The code collapses all layers into a single
`dist` matrix and mutates it in place, which is only safe if, at the moment you compute any
`dist[i][j]` for a given `k`, the two cells you read are still layer-`k` values.

Keeping `k` outermost guarantees exactly that: the entire matrix is upgraded from layer `k` to
layer `k+1` before `k` advances. The two cells you read, `dist[i][k]` and `dist[k][j]`, are also
special — a shortest path from `i` to `k` never needs `k` as an *intermediate*, so those two cells
are identical in layer `k` and layer `k+1`. Overwriting them mid-sweep is harmless.

Move `k` inside, and that breaks. With `for i: for j: for k`, you finish all `k` values for the
pair `(i, j)` before moving to the next pair, so a later pair reads cells that have already jumped
several layers ahead while others are still behind. The result is a matrix of mixed-layer values —
no crash, just wrong answers. A 4-node counterexample:

```
adjacency (∞ = no edge)        correct, k outer        wrong, k innermost
  0    ∞    3    ∞               0    8    3    5        0   ∞    3    5     ← dist[0][1] never found
  ∞    0    9    5               8    0    9    5        8   0    9    5
  9    ∞    0    2               5    5    0    2        5   5    0    2
  3    3    9    0               3    3    6    0        3   3    6    0
```

The true `0 → 1` route is `0 →3→ 2 →2→ 3 →3→ 1`, costing 8. The `i, j, k` version finishes the pair
`(0,1)` first, and at that moment `dist[0][3]` is still `∞` — the `0 → 2 → 3` shortcut that makes
the route possible is not discovered until the pair `(0,3)` comes up later. By then nothing ever
revisits `(0,1)`, so it stays `∞` forever. Getting the loop order wrong does not slow the algorithm
down; it silently answers a different question.

**Trace** one intermediate (`k = 1`) on 3 nodes:

```
edges: 0→1 = 8, 1→2 = 1, 0→2 = 10 (direct, but slow)

        0   1   2                      0   1   2
   0 [  0   8  10 ]              0 [  0   8   9 ]   ← updated
   1 [  ∞   0   1 ]    ─k=1→     1 [  ∞   0   1 ]
   2 [  ∞   ∞   0 ]              2 [  ∞   ∞   0 ]

k=1 asks "is i→1→j cheaper?":
  (0,2): dist[0][1] + dist[1][2] = 8 + 1 = 9 < 10 → dist[0][2] = 9 ✓
  (all other pairs: routing through 1 is ∞ or no gain)
```

Verify: 0→1→2 = 8+1 = 9 beats the direct 0→2 = 10. ✓

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

### Family B anchor: which LeetCode problems these algorithms solve

The whole family answers "cheapest way from A to B when edges cost different amounts." Picking the algorithm is a decision tree on the *weights*, not the problem theme:

- **All weights `≥ 0`, want single-source distances** → **Dijkstra** → LC **743** Network Delay Time, LC 1631 Path With Minimum Effort, LC 1514 Path with Max Probability, LC 778 Swim in Rising Water.
- **A hard cap on number of edges/stops**, or negative weights → **Bellman-Ford** (bounded rounds) → LC **787** Cheapest Flights Within K Stops.
- **All-pairs distances, tiny V (≤ ~400)** → **Floyd-Warshall** → LC 1334 City With Smallest Number of Neighbors.
- **Weights are only 0 or 1** → **0-1 BFS** (deque) → LC 1368 Min Cost to Make at Least One Valid Path.

### B.1 — Problem 743: Network Delay Time

**Difficulty**: Medium

> You have `n` nodes labeled `1..n`. Given `times[i] = (u, v, w)` — a signal from `u` to `v` takes `w` time — and a start node `k`, return the time for *all* nodes to receive the signal, or `-1` if some node never does.

"Signal reaches everyone" = the **maximum** of the shortest-path distances from `k` to every node. Edges carry different delays and all are positive, so this is textbook single-source Dijkstra: compute `dist[]` from `k`, then answer is `max(dist)` (or `-1` if any node is unreachable, i.e. `dist == inf`).

```python
import heapq
from collections import defaultdict

def network_delay_time(times, n, k):
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    dist = {}
    pq = [(0, k)]                      # (distance_so_far, node)
    while pq:
        d, u = heapq.heappop(pq)
        if u in dist:                  # already finalized = stale entry, skip
            continue
        dist[u] = d                    # first pop = shortest (greedy invariant)
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(pq, (d + w, v))

    return max(dist.values()) if len(dist) == n else -1
```

```
times = [(2,1,1),(2,3,1),(3,4,1)], n=4, k=2

pq=[(0,2)]                 pop (0,2)  dist{2:0}  push (1,1),(1,3)
pq=[(1,1),(1,3)]           pop (1,1)  dist{2:0,1:1}   (1 has no out-edges)
pq=[(1,3)]                 pop (1,3)  dist{...,3:1}   push (2,4)
pq=[(2,4)]                 pop (2,4)  dist{...,4:2}

all 4 reached → answer = max(0,1,1,2) = 2
```

`★ Insight ─────────────────────────────────────`
- **"First pop off the heap = finalized" is the whole algorithm.** The `if u in dist: continue` guard replaces a decrease-key operation — you let stale, larger entries sit in the heap and skip them when they surface. This "lazy deletion" is the standard Python Dijkstra idiom (heapq has no decrease-key).
- The problem wording ("time for all to receive") hides a `max` over distances. Recognizing that "everyone is reached by time T" ⇔ `T = max shortest distance` is the modeling step; the rest is the raw template.
`─────────────────────────────────────────────────`

### B.2 — Problem 787: Cheapest Flights Within K Stops

**Difficulty**: Medium

> `n` cities, `flights[i] = (from, to, price)`. Find the cheapest price from `src` to `dst` using **at most `k` stops** (so at most `k + 1` edges). Return `-1` if none.

The "at most `k` stops" cap is the tell that plain Dijkstra is *wrong here*: Dijkstra finalizes a node by cheapest cost, but the globally-cheapest way to reach a city might use too many hops, while a pricier few-hop path is the one you actually need. **Bellman-Ford's edge-count structure fits exactly**: relax all edges `k + 1` times and each round extends every path by one more edge — so after round `i`, `dist[v]` is the cheapest cost reaching `v` using `≤ i` edges. Bounding the rounds bounds the hops for free.

```python
def find_cheapest_price(n, flights, src, dst, k):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0

    for _ in range(k + 1):             # ≤ k stops = ≤ k+1 edges = k+1 rounds
        snapshot = dist[:]             # freeze: relax off LAST round only
        for u, v, w in flights:
            if snapshot[u] + w < dist[v]:
                dist[v] = snapshot[u] + w

    return dist[dst] if dist[dst] != INF else -1
```

```
n=4, flights=[(0,1,100),(1,2,100),(2,0,100),(1,3,600),(2,3,200)]
src=0, dst=3, k=1   → at most 1 stop, so ≤ 2 edges

round 1 (≤1 edge from src):  snapshot all INF except dist[0]=0
   relax 0→1: dist[1]=100
round 2 (≤2 edges):          snapshot = [0,100,INF,INF]
   0→1: 100 (no change)   1→2: dist[2]=200   1→3: dist[3]=700

dist[3]=700   (path 0→1→3, 1 stop). The cheaper 0→1→2→3 = 400 needs 2 stops → excluded.
answer = 700
```

`★ Insight ─────────────────────────────────────`
- **The `snapshot = dist[:]` line is load-bearing.** Without it, one Bellman-Ford round could chain several edges (0→1 *then* 1→2 in the same pass), letting a path use more than the intended number of edges. Freezing the previous round's distances forces "exactly one more edge per round," which is what makes "k rounds = k hops" true.
- This is Bellman-Ford *repurposed*: normally you run `V-1` rounds for correctness; here you run exactly `k+1` rounds because the round count **is** the constraint. Same algorithm, different stopping rule — recognizing that reuse is the pattern lesson.
`─────────────────────────────────────────────────`

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

    # If we couldn't reach every vertex, the graph is disconnected:
    # no spanning tree exists. Returning mst_weight here would be a
    # misleading partial sum, so signal it instead.
    if edges_used < n:
        return None  # or: raise ValueError("graph is disconnected")

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

**Intuition**: a node is safe to output only once everything that must come before it is already out. "Must come before" = incoming edges, so a node with **in-degree 0** has no unmet prerequisites — emit it, then delete it (decrement its neighbors' in-degrees, which may free them up next). Repeat until empty. If nodes remain but none has in-degree 0, they're tangled in a cycle — no valid order exists.

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

**Trace** on this DAG:

```
0 ─┐
   ├─→ 2 ─→ 3
1 ─┘   └──→ 4

in_deg = [0, 0, 2, 1, 1]      queue = [0, 1]     order = []

pop 0 → order=[0];        in_deg[2]: 2→1        queue=[1]
pop 1 → order=[0,1];      in_deg[2]: 1→0 enq 2  queue=[2]
pop 2 → order=[0,1,2];    in_deg[3]:1→0 enq 3, in_deg[4]:1→0 enq 4  queue=[3,4]
pop 3 → order=[0,1,2,3]                          queue=[4]
pop 4 → order=[0,1,2,3,4]                         queue=[]

order = [0, 1, 2, 3, 4]   (every edge points left→right ✓)
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

### Family C anchor: which LeetCode problems this template solves

Topological sort is the answer whenever items have **"must come before"** dependencies. The signal in a problem statement: *prerequisites, dependencies, build order, "before you can X you must Y."* Two questions decide the exact variant:

- **"Is a valid order even possible?"** (just feasibility = no cycle) → Kahn's, check you emitted all `V` nodes → LC **207** Course Schedule, LC 802 Find Eventual Safe States.
- **"Give me the order."** → Kahn's, return the emission list → LC **210** Course Schedule II, LC 269 Alien Dictionary, LC 310 Minimum Height Trees.
- **"Longest chain / max value along dependencies"** → topo order + DP-on-DAG (§15) → LC 329 Longest Increasing Path in a Matrix, LC 1857 Largest Color Value in a Directed Graph.

Both walkthroughs below use **Kahn's algorithm** (BFS with in-degrees): repeatedly remove a node with no remaining prerequisites. It doubles as cycle detection — if you can never empty the queue, some nodes are stuck in a cycle.

### C.1 — Problem 207: Course Schedule

**Difficulty**: Medium

> There are `numCourses` courses `0..numCourses-1`. `prerequisites[i] = (a, b)` means you must take `b` before `a`. Return `True` if you can finish all courses.

"Can you finish?" = "is the prerequisite graph acyclic?" Model each course as a node and each prereq `(a, b)` as a directed edge `b → a` (take `b`, then `a` unlocks). A valid schedule exists iff the graph is a DAG. Kahn's algorithm counts how many courses it can actually emit; if that count equals `numCourses`, no cycle blocked it.

```python
from collections import deque, defaultdict

def can_finish(num_courses, prerequisites):
    adj = defaultdict(list)
    indeg = [0] * num_courses
    for a, b in prerequisites:         # b must come before a  → edge b→a
        adj[b].append(a)
        indeg[a] += 1

    queue = deque(c for c in range(num_courses) if indeg[c] == 0)
    taken = 0
    while queue:
        c = queue.popleft()            # a course with no unmet prereqs
        taken += 1
        for nxt in adj[c]:
            indeg[nxt] -= 1            # one prereq satisfied
            if indeg[nxt] == 0:
                queue.append(nxt)

    return taken == num_courses        # all emitted = acyclic
```

```
numCourses=4, prereqs=[(1,0),(2,0),(3,1),(3,2)]
edges: 0→1, 0→2, 1→3, 2→3     indeg: [0,1,1,2]

queue=[0]           pop 0, taken=1  → indeg 1:0, 2:0  → queue=[1,2]
queue=[1,2]         pop 1, taken=2  → indeg 3:1
queue=[2]           pop 2, taken=3  → indeg 3:0        → queue=[3]
queue=[3]           pop 3, taken=4

taken=4 == numCourses → True
```

```
Cyclic case: prereqs=[(1,0),(0,1)]   edges 0→1, 1→0   indeg [1,1]
queue starts EMPTY (no zero-indegree node) → taken=0 ≠ 2 → False
```

`★ Insight ─────────────────────────────────────`
- **In-degree = "number of unmet prerequisites."** A node is ready exactly when its in-degree hits 0. The queue holds the "ready now" frontier — this is BFS, but on dependency-readiness instead of distance.
- **Cycle detection falls out for free.** Nodes inside a cycle mutually keep each other's in-degree above 0 forever, so they never enter the queue and `taken` falls short. No separate cycle check needed — the count *is* the check.
`─────────────────────────────────────────────────`

### C.2 — Problem 210: Course Schedule II

**Difficulty**: Medium

> Same setup as LC 207, but return *a* valid ordering of all courses (any one), or `[]` if impossible.

Identical graph and identical Kahn's loop — the only change is that you **record the emission order** instead of just counting. The order in which nodes leave the queue *is* a topological order, because a node is only emitted after every prerequisite has already been emitted. If the final list is short (a cycle blocked some nodes), return `[]`.

```python
from collections import deque, defaultdict

def find_order(num_courses, prerequisites):
    adj = defaultdict(list)
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1

    queue = deque(c for c in range(num_courses) if indeg[c] == 0)
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)                # <-- the ONLY change vs LC 207
        for nxt in adj[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == num_courses else []
```

```
numCourses=4, prereqs=[(1,0),(2,0),(3,1),(3,2)]   (same graph as C.1)

emit 0 → order=[0]
emit 1 → order=[0,1]
emit 2 → order=[0,1,2]
emit 3 → order=[0,1,2,3]

len 4 == numCourses → [0,1,2,3]   (also valid: [0,2,1,3])
```

`★ Insight ─────────────────────────────────────`
- **LC 207 and LC 210 are the same algorithm with one extra line.** This is the payoff of learning the *pattern* rather than the problem: "can it be ordered?" and "give the order" differ only by `order.append(c)` vs a counter. Feasibility is just "the order exists."
- **Any zero-indegree node is a legal next pick**, so multiple valid orders exist. If a problem wants a *specific* tie-break (e.g. lexicographically smallest, LC 269-style), swap the `deque` for a heap — the skeleton is untouched.
`─────────────────────────────────────────────────`

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

### Family E anchor: which LeetCode problems this solves

Structural analysis (bridges, articulation points, SCC) answers **"which parts are critical / mutually reachable?"** These are the rarest in interviews but the signal is sharp: *critical connection, single point of failure, "removing this disconnects the graph," strongly connected, mutually reachable.* All are built on **Tarjan's DFS with `disc[]`/`low[]` timestamps** (§6) or its SCC cousin (§5).

- **Edges whose removal disconnects the graph** (bridges) → **Tarjan bridge-finding** → LC **1192** Critical Connections in a Network.
- **Nodes whose removal disconnects the graph** (articulation points) → same DFS, articulation rule (§6).
- **Groups where every node reaches every other** (SCC) → **Tarjan/Kosaraju** (§5), often then condense to a DAG → see the SCC note below.

### E.1 — Problem 1192: Critical Connections in a Network

**Difficulty**: Hard

> `n` servers `0..n-1` connected by undirected `connections`. A *critical connection* is an edge that, if removed, makes some servers unreachable from others. Return all critical connections.

"Edge whose removal disconnects the graph" is the exact definition of a **bridge**. So this Hard problem is just "find all bridges" — no new algorithm, only recognizing the vocabulary. Tarjan's bridge algorithm does one DFS assigning each node a discovery time `disc[u]`, and computes `low[u]` = the earliest node reachable from `u`'s subtree via tree edges plus at most one back edge. An edge `(u, v)` (v a child) is a bridge exactly when `low[v] > disc[u]`: v's subtree has **no** back edge climbing to `u` or above, so cutting `(u,v)` strands it.

```python
from collections import defaultdict

def critical_connections(n, connections):
    adj = defaultdict(list)
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)

    disc = [-1] * n                    # discovery time; -1 = unvisited
    low = [0] * n
    bridges = []
    timer = [0]

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in adj[u]:
            if v == parent:
                continue               # don't bounce back on the edge we came in
            if disc[v] == -1:          # tree edge
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:   # v can't reach u or higher → bridge
                    bridges.append([u, v])
            else:                      # back edge
                low[u] = min(low[u], disc[v])

    dfs(0, -1)                         # graph is connected
    return bridges
```

```
n=4, connections=[[0,1],[1,2],[2,0],[1,3]]

    0 --- 1 --- 3
     \   /
      \ /
       2

DFS from 0: disc=[0,1,2,_]  triangle 0-1-2 has back edge 2→0
  low[2]=disc[0]=0, low[1]=0  → edges in the triangle: low ≤ disc → NOT bridges
  edge 1→3: low[3]=3 > disc[1]=1 → BRIDGE

bridges = [[1,3]]   (cutting 1-3 isolates server 3)
```

`★ Insight ─────────────────────────────────────`
- **`low[v] > disc[u]` is the entire bridge test.** It asks "can v's subtree climb back to u or higher without using edge (u,v)?" If not, that edge is the only lifeline — a bridge. An edge on a cycle always has a back edge saving it, so cycles contain no bridges.
- **Recognizing "critical connection = bridge" is the whole difficulty.** The Hard rating is for knowing the vocabulary maps to a standard algorithm; the code is textbook Tarjan. This is why building a *named-concept* vocabulary (§6) beats memorizing individual problems.
`─────────────────────────────────────────────────`

### E.2 — Note: Strongly Connected Components (condensation)

Clean numbered LC problems for SCC are rare (they hide inside harder problems like LC 1568), so here's the pattern rather than a full walkthrough. **SCC = a maximal set of nodes where every node reaches every other** (only meaningful in *directed* graphs). The high-value move is **condensation**: collapse each SCC into a single super-node. The result is always a **DAG**, which unlocks Family C tools (topological sort, DP-on-DAG) on problems that were cyclic and therefore un-orderable.

```
Directed graph with a cycle:        Condense SCCs → DAG:
  A → B → C → A   (one SCC)           [SCC: A,B,C] → [SCC: D]
        ↓                             now topologically orderable
        D
```

Typical uses: "minimum edges to add so the whole graph is strongly connected" (count condensed-DAG sources/sinks), or running DP over mutually-dependent states after collapsing their cycles. When you see cyclic directed dependencies that block a topo sort, **condense to a DAG first** — that's the reusable idea. See §5 for Tarjan's and Kosaraju's SCC implementations.

`★ Insight ─────────────────────────────────────`
- **Condensation turns "cyclic and unsolvable by topo sort" into "acyclic and solvable."** It's the bridge from Family E back to Family C — whenever a directed problem has cycles, ask "what if each cycle were one node?"
- Both bridges (E.1) and SCC share Tarjan's `disc`/`low` timestamp machinery — learn the timestamp-DFS skeleton once and it powers the entire structural family.
`─────────────────────────────────────────────────`

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

### Family D anchor: which LeetCode problems these solve

Union-Find (§9) and MST (§3) are one family — both are about **grouping nodes by connectivity**, one asking "who's connected?" and the other "connect everyone as cheaply as possible." The statement signal: *provinces, groups, "are these two connected?", redundant connection, connect all points, accounts merge.*

- **Count / test connectivity, edges arrive incrementally** → **Union-Find** → LC **547** Number of Provinces, LC 684 Redundant Connection, LC 721 Accounts Merge, LC 1319 Number of Operations to Make Network Connected.
- **Connect all nodes at minimum total weight** → **MST** (Kruskal = sort edges + Union-Find; Prim = greedy heap) → LC **1584** Min Cost to Connect All Points, LC 1135 Connecting Cities With Minimum Cost, LC 1489 Critical/Pseudo-Critical Edges.

Kruskal is literally "Union-Find + sorted edges," so the two anchors below share one data structure — learn DSU once and MST is nearly free.

### D.1 — Problem 547: Number of Provinces

**Difficulty**: Medium

> `isConnected` is an `n x n` matrix where `isConnected[i][j] == 1` means city `i` and city `j` are directly connected. A province is a group of directly or indirectly connected cities. Return the number of provinces.

"Number of groups of connected things" = number of connected components = the classic Union-Find headline use. Start with `n` singleton groups; for every edge `(i, j)`, `union` them. Each successful union (two *different* roots merging) drops the component count by one. (You could also flood-fill this like LC 200 — but the matrix-of-relationships shape and "indirectly connected" wording is the textbook DSU trigger.)

```python
def find_circle_num(is_connected):
    n = len(is_connected)
    parent = list(range(n))            # each city its own province initially
    count = n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path compression
            x = parent[x]
        return x

    def union(a, b):
        nonlocal count
        ra, rb = find(a), find(b)
        if ra != rb:                   # genuinely separate provinces
            parent[ra] = rb            # no rank here — see the note below
            count -= 1                  # two provinces became one

    for i in range(n):
        for j in range(i + 1, n):      # upper triangle: matrix is symmetric
            if is_connected[i][j]:
                union(i, j)
    return count
```

> **Why no union by rank here, when §9 insists on it?** This version attaches roots arbitrarily and
> still passes, because *path compression alone* already gives O(log n) amortised — and with
> `n <= 200` on this problem, the difference is invisible. The full DSU class in §9 keeps rank
> because the two optimisations together give the near-constant α(n) bound, which starts to matter
> when `n` reaches 10⁵ and an adversarial union order could otherwise build a deep chain before
> compression flattens it. Rule of thumb: write the short version when you are pasting a DSU into
> one function under contest pressure; use the §9 class when the DSU is the load-bearing structure.

```
isConnected = [[1,1,0],
               [1,1,0],
               [0,0,1]]        parent=[0,1,2]  count=3

edge (0,1): find0=0, find1=1, differ → union, parent=[1,1,2] count=2
edge (0,2): value 0 → skip
edge (1,2): value 0 → skip

count = 2  (provinces {0,1} and {2})
```

`★ Insight ─────────────────────────────────────`
- **`count` starts at `n` and only ever decreases — once per genuine merge.** You never recount components at the end; the answer is maintained incrementally. That's the DSU superpower over flood fill: connectivity updates are near-O(1) as edges stream in.
- **The `ra != rb` guard is what makes counting correct.** Unioning two cities already in the same province must NOT decrement `count`. This same guard is exactly how Kruskal (D.2) rejects a cycle-forming edge — one primitive, two uses.
`─────────────────────────────────────────────────`

### D.2 — Problem 1584: Min Cost to Connect All Points

**Difficulty**: Medium

> Given `points` on a 2D plane, the cost to connect two points is their Manhattan distance `|x1-x2| + |y1-y2|`. Return the minimum cost to connect *all* points (so any point is reachable from any other).

"Connect all nodes, minimize total edge weight, result is a tree" is the definition of a **Minimum Spanning Tree**. The graph is *complete* — every pair of points is a candidate edge — so build all `n(n-1)/2` edges, then run **Kruskal**: sort edges cheapest-first and add an edge only if it joins two currently-separate components (the Union-Find `ra != rb` guard again). Stop once `n-1` edges are in the tree.

```python
def min_cost_connect_points(points):
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            w = abs(points[i][0]-points[j][0]) + abs(points[i][1]-points[j][1])
            edges.append((w, i, j))
    edges.sort()                       # Kruskal: consider cheapest edges first

    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, used = 0, 0
    for w, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:                   # adding this edge won't form a cycle
            parent[ri] = rj
            total += w
            used += 1
            if used == n - 1:          # tree complete
                break
    return total
```

```
points = [(0,0),(2,2),(3,10),(5,2),(7,0)]

all edges sorted by weight (Manhattan):
  (0,1)=4 (1,3)=3 (3,4)=4 (0,4)=7 (1,2)=9 ...   → sort: 3,4,4,...

take (1,3)=3   union 1,3          total=3 used=1
take (0,1)=4   union {1,3} & 0    total=7 used=2
take (3,4)=4   union in {0,1,3} & 4  total=11 used=3
take (1,2)=9   union & 2          total=20 used=4 == n-1 → stop

min cost = 20
```

`★ Insight ─────────────────────────────────────`
- **Kruskal = sort edges + Union-Find, nothing more.** The `if ri != rj` cycle check is the identical guard from LC 547 (D.1). "Add the cheapest edge that doesn't create a cycle, `n-1` times" is the entire greedy — recognizing MST as *Union-Find with sorted edges* means D.1 and D.2 collapse to one idea.
- **Complete graph → `O(n²)` edges → Kruskal's sort dominates at `O(n² log n)`.** For dense graphs like this, **Prim with a heap** (§3.2) is often preferred since it never materializes all `n²` edges. Same MST, different edge-selection engine — pick by density.
`─────────────────────────────────────────────────`

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

### Bipartite Matching (Kuhn's augmenting-path algorithm)

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

Kuhn's runs one augmenting-path DFS per left node: **O(V · E)**. Good enough for interview-scale
graphs and for every LC problem that reduces to matching.

### Beyond Kuhn's (not implemented here)

| Need | Algorithm | Why it is not in this guide |
|------|-----------|-----------------------------|
| Faster bipartite matching on large graphs | **Hopcroft-Karp**, O(E·√V) | Only pays off past ~10⁴ nodes; never required for an LC problem |
| Maximum-**weight** bipartite matching (assignment problem) | **Hungarian**, O(V³) | For the small `n ≤ 20` assignment problems that actually appear, use bitmask DP — see [Bitmask DP](/pattern/bitmask-dp-subset-partition) |
| Matching in a **non-bipartite** graph | **Edmonds' blossom** | Genuinely intricate; reach for a library |

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

    # Assign values. Tarjan returns SCCs in REVERSE topological order,
    # so a smaller comp id = later in topological order. Pick the literal
    # that comes later in topo order: x_i = True when comp[i] < comp[i+n].
    values = [comp[i] < comp[i + n] for i in range(n)]
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

## 13.5 Family F Anchor: Advanced Graph Patterns in LeetCode

Family F (flow §10, matching §11, Eulerian §12, 2-SAT §13) is the rarest in interviews, and clean numbered LC problems are scarce — so this family gets **one full walkthrough (Eulerian) plus notes**, since a real LC problem exists for Euler but flow/2-SAT usually appear disguised inside Hard problems. The signals:

- **"Use every edge exactly once," itinerary, reconstruct path** → **Eulerian path**, Hierholzer's algorithm → LC **332** Reconstruct Itinerary, LC 753 Cracking the Safe.
- **"Maximum matching / assignment," bipartite pairing** → **bipartite matching / max-flow** → LC 1349 Maximum Students Taking Exam (flow/matching), LC 1595 Minimum Cost to Connect Two Groups.
- **"Each choice is a boolean with either/or constraints"** → **2-SAT** (§13) — almost never numbered; appears in contest problems.

### F.1 — Problem 332: Reconstruct Itinerary

**Difficulty**: Hard

> Given `tickets[i] = (from, to)` (all departing from `"JFK"`), reconstruct the itinerary that uses **all** tickets exactly once. If multiple valid itineraries exist, return the one with the smallest **lexical** order when read as a single string.

"Use every ticket (edge) exactly once" is the definition of an **Eulerian path**. Model airports as nodes and tickets as directed edges; you want a trail that traverses every edge once. **Hierholzer's algorithm** builds it: greedily walk edges (removing each as you use it) until you get stuck, then splice that dead-end into the route. To get lexical order, always take the **smallest available destination first** — a min-heap or sorted list per node. The trick: append an airport to the result only when it has no more outgoing edges (post-order), then reverse.

```python
from collections import defaultdict
import heapq

def find_itinerary(tickets):
    adj = defaultdict(list)
    for src, dst in tickets:
        heapq.heappush(adj[src], dst)   # min-heap → lexical order

    route = []
    def visit(airport):
        while adj[airport]:             # take smallest dest until stuck
            nxt = heapq.heappop(adj[airport])
            visit(nxt)
        route.append(airport)           # post-order: add when edges exhausted

    visit("JFK")
    return route[::-1]                  # reverse the post-order to get the trail
```

```
tickets = [(JFK,SFO),(JFK,ATL),(SFO,ATL),(ATL,JFK),(ATL,SFO)]
adj (min-heaps):  JFK:[ATL,SFO]  ATL:[JFK,SFO]  SFO:[ATL]

recurse smallest-first: JFK→ATL→JFK→SFO→ATL→SFO (now stuck, no edges left)
post-order appends as each node's edges run out:  SFO, ATL, SFO, JFK, ATL, JFK
reverse → JFK, ATL, JFK, SFO, ATL, SFO

itinerary = ["JFK","ATL","JFK","SFO","ATL","SFO"]
```

`★ Insight ─────────────────────────────────────`
- **Post-order + reverse is what makes Hierholzer correct.** If you appended airports in visit-order, a premature dead-end would land in the middle of your route. Recording a node only when its edges are exhausted, then reversing, automatically splices dead-end loops into the right place.
- **"Use every edge once" ⇒ Eulerian, "use every node once" ⇒ Hamiltonian.** These sound alike but Eulerian is polynomial (Hierholzer) while Hamiltonian is NP-hard. Reading edge-vs-node in the statement picks tractable vs intractable — a critical identification skill.
`─────────────────────────────────────────────────`

### F.2 — Notes: flow, matching, and 2-SAT

**Max-flow / bipartite matching.** When a problem is "assign items in group X to items in group Y under capacity/compatibility limits, maximize pairings," it's **bipartite matching**, solvable as max-flow (add a super-source → X, Y → super-sink, all capacities 1; see §10–§11). LC 1349 (seat students so no two cheat) reduces to maximum independent set on a bipartite-by-column graph = matching. The reusable move: **spot the two disjoint groups + a "one-to-one under constraints" objective**, then reach for matching. Full walkthroughs are rare because most interviews stop short of flow.

**2-SAT.** When every decision is a boolean and constraints are "if A then B" / "at most one of A,B" / "A or B," build the implication graph (§13), find SCCs (§5), and a solution exists iff no variable `x` shares an SCC with `¬x`. This ties Family F back to Family E — **2-SAT is an SCC application**. It almost never appears as a numbered LC problem but is standard in competitive programming.

`★ Insight ─────────────────────────────────────`
- **Advanced graph problems are usually a reduction, not a new algorithm.** "Maximize assignments" → matching → flow; "boolean constraints" → 2-SAT → SCC. The skill is recognizing the reduction; the engine underneath is something from Families A–E.
- Because these are rare and heavy, prioritize them *last* in study — master A–D (interview bread-and-butter) and the structural family E before investing here.
`─────────────────────────────────────────────────`

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

> **Who owns what.** [Dynamic Programming §14](/pattern/dp) is canonical for DP-on-DAG as a *DP
> technique*, including the memoized implicit-DAG framing (LC 329). This section owns the
> graph-side prerequisite that guide does not cover: what to do when your graph has **cycles** —
> condense it into its SCC DAG (§5) first, then DP over the condensation.

### DP on DAG

Process nodes in topological order. Most DP on graphs requires no cycles.

> **Adjacency format.** This one takes a **weighted** list, `adj[u] = [(v, w), ...]`, because a
> longest path adds up edge weights. The path-*counting* version right below takes an
> **unweighted** list, `adj[u] = [v, ...]`. Mixing the two is a fast route to
> `cannot unpack non-iterable int` — check which shape a template wants before you paste it.

```python
from collections import deque

# Longest path in DAG — adj[u] = [(v, w), ...]
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
from collections import deque

def count_paths(adj, n, src, dst):
    # adj[u] = [v, ...] — unweighted, unlike longest_path above.
    # Assumes topological processing order (Kahn's below guarantees it);
    # dp[src]=1 seeds the source. Counts paths in a DAG — a cycle would
    # loop forever (its nodes never reach in-degree 0, so Kahn's skips them).
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

---

## 17. Common Mistakes

| Mistake | Why it breaks | Fix |
|---------|---------------|-----|
| Dijkstra with negative-weight edges | A finalized node can be undercut later by a negative edge — the greedy "closest first" invariant no longer holds | Use Bellman-Ford (negative edges) or Floyd-Warshall (all pairs) |
| Forgetting to mark nodes visited in BFS | The same node gets enqueued once per incoming edge → queue explodes, distances get overwritten, O(V·E) or worse | Set `dist[nb]` / `visited[nb]` at enqueue time, not dequeue time |
| Mixing 0-indexed and 1-indexed node labels | Off-by-one: array of size `n` indexed at `n`, or node 0 left unprocessed | Pick one convention; size arrays `n+1` if the input is 1-indexed |
| Ignoring disconnected components | A single BFS/DFS from one start visits only its component; the rest stay unvisited | Loop `for i in range(n): if not visited[i]: traverse(i)` |
| Recursion-depth overflow on deep graphs (Python) | Recursive DFS hits `RecursionError` on long chains (~10^4+) | Use the iterative stack-based DFS, or raise `sys.setrecursionlimit` |
| Using plain Dijkstra when there's a hop/stop cap (LC 787) | Dijkstra finalizes by cost, so it may lock in a cheap-but-too-many-hops path and miss the pricier legal one | Bellman-Ford with exactly `k+1` rounds; snapshot distances each round so one round = one edge |
| Kahn's topo sort without checking the emitted count | A cycle silently drops nodes; you return a partial order as if valid | Compare `len(order)` (or `taken`) to `V`; short = cycle exists |
| Decrementing MST/DSU component count on a redundant edge | Unioning two nodes already in the same set isn't a real merge; count goes wrong | Only act when `find(a) != find(b)` — the same guard rejects cycle edges in Kruskal |
| Appending airports in visit-order for Eulerian path (LC 332) | A premature dead-end lands mid-route; the trail is wrong | Append in post-order (when edges exhausted) and reverse at the end (Hierholzer) |
| Confusing "every edge once" (Eulerian) with "every node once" (Hamiltonian) | Eulerian is polynomial; Hamiltonian is NP-hard — wrong model = wrong complexity | Read edge-vs-node carefully; edges → Hierholzer, nodes → backtracking/bitmask DP |

---

## 18. Practice Order

Work these in order — each adds exactly one new idea on top of the last.

```
Start here
    │
    ▼
  LC 200  Number of Islands        (Easy)   ── plain BFS/DFS flood fill over a grid
    │
    ▼
  LC 994  Rotting Oranges          (Medium) ── multi-source BFS: seed the queue with ALL sources
    │
    ▼
  LC 207  Course Schedule          (Medium) ── topo sort / cycle detection via in-degrees
    │
    ▼
  LC 743  Network Delay Time       (Medium) ── first weighted graph → Dijkstra
    │
    ▼
  LC 787  Cheapest Flights ≤K Stops (Medium)── Bellman-Ford: relax edges a bounded number of rounds
    │
    ▼
  LC 210  Course Schedule II        (Medium) ── same as 207 + record emission = topological order
    │
    ▼
  LC 547  Number of Provinces       (Medium) ── Union-Find: count connected components as edges arrive
    │
    ▼
  LC 1584 Min Cost Connect Points    (Medium)── MST = Union-Find + sorted edges (Kruskal)
    │
    ▼
  LC 127  Word Ladder               (Hard)   ── model words as nodes, BFS for shortest transform
    │
    ▼
  LC 1192 Critical Connections       (Hard)  ── Tarjan bridges: disc/low timestamps (Family E)
    │
    ▼
  LC 332  Reconstruct Itinerary      (Hard)  ── Eulerian path via Hierholzer (Family F)
```

### The 6 families at a glance

Once the ladder is done, this is the map that turns any new problem into an algorithm:

```
A. Traversal / flood fill    grid, regions, "connected"        → BFS/DFS (§1,§7,§14)   LC 200, 994
B. Weighted shortest path    "cheapest", edge costs differ     → Dijkstra/Bellman (§2) LC 743, 787
C. Topological / DAG order   prerequisites, "before you can"   → Kahn's topo (§4,§8,§15) LC 207, 210
D. Union-Find / MST          provinces, "connect all cheaply"  → DSU / Kruskal (§3,§9)  LC 547, 1584
E. Structural analysis       "critical edge", single failure   → Tarjan disc/low (§5,§6) LC 1192
F. Advanced (flow/euler/2SAT) "use every edge", matching        → Hierholzer/flow (§10-13) LC 332
```

---

## When This Fails

Each graph algorithm has a precondition, and violating it produces a plausible wrong answer
rather than a crash:

- **Dijkstra with negative edges.** Its greedy finalisation assumes distances only grow when you
  extend a path. One negative edge invalidates that. Use Bellman-Ford.
- **Bellman-Ford without the extra pass.** `V−1` rounds compute distances; detecting a negative
  cycle needs one more round and a check for further improvement.
- **Floyd-Warshall with `k` not outermost.** The `k` loop must enclose `i` and `j`, because the
  DP means "shortest path using only intermediates from the first `k` nodes". Swap the order and
  it silently computes something else.
- **Topological sort on a cyclic graph.** Kahn's simply emits fewer than `V` nodes. Always
  compare the processed count against `V` rather than trusting the output.
- **Undirected cycle detection that forgets the parent edge.** Every undirected edge looks like a
  2-cycle, so you must skip the edge you arrived on. The `v == parent` node-skip in §8 handles
  parallel edges correctly *as a multigraph*: a repeated `u—v` is caught on `u`'s second pass over
  its list, and it genuinely is a cycle. The trap is a semantic one — if your input duplicates each
  undirected edge by accident rather than by intent, that "cycle" is an artefact of the input. When
  parallel edges are real data but must not count, skip by edge id instead of by node.
- **Union-Find without both path compression and union by rank/size.** You lose the
  near-constant amortized bound and can degrade to O(n) per operation.

## Self-Test

Answer these from memory, out loud or on paper, *before* looking. Recognition is not
recall: rereading an explanation feels like knowing, and it is not. A question you cannot answer
cold names the exact section to revisit — you do not need to reread the guide.


**1. Why is Dijkstra's greedy choice safe, and what exactly does a negative edge break?**

<details markdown="1">
<summary>Answer</summary>

When the minimum-distance unfinalised node is popped, no other route can beat it — any alternative starts with an already-longer prefix and can only add non-negative weight. A negative edge destroys "can only add", so a finalised node may later be improvable, and Dijkstra never revisits it.

</details>

**2. What does the stale-entry check `if d > dist[u]: continue` do?**

<details markdown="1">
<summary>Answer</summary>

Discards heap entries superseded by a better path found after they were pushed. It is the substitute for decrease-key: instead of updating in place, push a new entry and ignore obsolete ones on the way out.

</details>

**3. How does Bellman-Ford detect a negative cycle?**

<details markdown="1">
<summary>Answer</summary>

After `V−1` relaxation rounds, every shortest path with no cycle is final (a simple path has at most `V−1` edges). Run one more round: any further improvement proves a path with `V` or more edges is still getting shorter, which requires a negative cycle.

</details>

**4. Why must `k` be the outermost loop in Floyd-Warshall?**

<details markdown="1">
<summary>Answer</summary>

`dp[k][i][j]` is the shortest path from `i` to `j` using only nodes `0..k` as intermediates. It is defined in terms of `dp[k−1]`, so every `(i,j)` pair must be updated for intermediate `k` before moving to `k+1`. Any other nesting reads a half-built layer.

</details>

**5. Kahn's algorithm produces a shorter list than expected. What does that mean?**

<details markdown="1">
<summary>Answer</summary>

The graph has a cycle. Nodes inside a cycle never reach in-degree zero, so they are never enqueued. Comparing the processed count against `V` is the standard cycle test.

</details>

**6. What is the bridge condition in Tarjan's algorithm, and why?**

<details markdown="1">
<summary>Answer</summary>

Edge `(u, v)` is a bridge when `low[v] > disc[u]`: nothing in `v`'s subtree can reach `u` or above except through this edge, so removing it disconnects the graph. The articulation-point condition is `low[v] >= disc[u]` — reaching `u` itself is enough to keep the graph connected but still makes `u` critical.

</details>

**7. When updating `low[u]` from a back edge to `v`, do you use `low[v]` or `disc[v]`?**

<details markdown="1">
<summary>Answer</summary>

`disc[v]`. A back edge reaches `v` itself, not wherever `v` could subsequently reach. Using `low[v]` over-propagates and makes real bridges disappear.

</details>

**8. BFS, 0-1 BFS, Dijkstra, Bellman-Ford — pick by weight structure.**

<details markdown="1">
<summary>Answer</summary>

All weights equal → BFS, O(V+E). Weights only 0 and 1 → 0-1 BFS with a deque (push-front on 0, push-back on 1), O(V+E). Arbitrary non-negative → Dijkstra, O((V+E) log V). Any negative → Bellman-Ford, O(VE).

</details>

**9. How is 2-SAT solved with SCCs?**

<details markdown="1">
<summary>Answer</summary>

Build the implication graph: each clause `(a ∨ b)` adds `¬a → b` and `¬b → a`. A solution exists iff no variable shares an SCC with its own negation. When one exists, read it off by setting each variable according to which of `x`, `¬x` comes later in reverse topological order.

</details>

---

## See Also

- [Heap / Priority Queue](/pattern/heap) — the data structure Dijkstra and Prim are built on, including the lazy-deletion trick that replaces decrease-key.
- [Dynamic Programming §14](/pattern/dp) — DP on DAGs from the DP side, with the memoized implicit-DAG framing (LC 329) that §15 only sketches.
- [Tree Patterns](/pattern/tree) — a tree is a connected acyclic graph, and it unlocks techniques (rerooting, LCA, HLD) that general graphs cannot use.
- [Stack & Queue §8](/pattern/stack-queue) — the queue mechanics behind BFS, and the deque behind 0-1 BFS (§2.4).
- [Bitmask DP — Subset Partition](/pattern/bitmask-dp-subset-partition) — TSP and "visit every node" once `V <= 20`.
- [Pattern Decision Map](/pattern/decision-map) — the router: which technique does a cold problem call for?
- [Pattern Mastery Program](/pattern/mastery) — the spaced-repetition schedule, mastery checklist, and drill formats that turn reading into recall.
