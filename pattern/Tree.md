---
layout: simple
title: "Tree Problem Patterns"
permalink: /pattern/tree
---

# Tree Problem Patterns — Comprehensive Guide

Trees are everywhere in competitive programming. This guide covers **every major technique** for solving tree problems, organized by what kind of query or operation you need to perform.

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| Traverse a tree | DFS / BFS | [1](#1-tree-traversals) |
| Query values in a **subtree** | Euler Tour + Segment Tree | [2](#2-euler-tour-subtree-queries) |
| Query values on a **path** | HLD + Segment Tree | [3](#3-heavy-light-decomposition-path-queries) |
| Find **Lowest Common Ancestor** | Binary Lifting / Euler+RMQ | [4](#4-lowest-common-ancestor) |
| Compute DP for **every node as root** | Rerooting DP | [5](#5-rerooting-dp) |
| Find **diameter / center** of tree | Two-BFS or Tree DP | [6](#6-tree-diameter-and-center) |
| Answer **distance-based** queries | Centroid Decomposition | [7](#7-centroid-decomposition) |
| Merge child info efficiently | Small-to-Large (DSU on Tree) | [8](#8-small-to-large-merging-dsu-on-tree) |
| Compute DP on subtrees | Tree DP | [9](#9-tree-dp-patterns) |
| Work with only **key nodes** | Virtual Tree | [10](#10-virtual-tree-auxiliary-tree) |
| Count/encode labeled trees | Prufer Sequence | [11](#11-prufer-sequence) |
| Check if two trees are **identical** | Tree Hashing | [12](#12-tree-hashing-and-isomorphism) |

---

## Table of Contents

1. [Tree Traversals](#1-tree-traversals)
2. [Euler Tour (Subtree Queries)](#2-euler-tour-subtree-queries)
3. [Heavy-Light Decomposition (Path Queries)](#3-heavy-light-decomposition-path-queries)
4. [Lowest Common Ancestor](#4-lowest-common-ancestor)
5. [Rerooting DP](#5-rerooting-dp)
6. [Tree Diameter and Center](#6-tree-diameter-and-center)
7. [Centroid Decomposition](#7-centroid-decomposition)
8. [Small-to-Large Merging (DSU on Tree)](#8-small-to-large-merging-dsu-on-tree)
9. [Tree DP Patterns](#9-tree-dp-patterns)
10. [Virtual Tree (Auxiliary Tree)](#10-virtual-tree-auxiliary-tree)
11. [Prufer Sequence](#11-prufer-sequence)
12. [Tree Hashing and Isomorphism](#12-tree-hashing-and-isomorphism)
13. [Pattern Recognition Cheat Sheet](#13-pattern-recognition-cheat-sheet)

---

## 1. Tree Traversals

The foundation of everything. Every tree technique starts with a traversal.

### DFS (Depth-First Search)

Goes deep before going wide. The workhorse of tree algorithms.

```python
def dfs(node, parent, adj):
    # PRE-ORDER: process node before children
    print(f"Enter {node}")

    for child in adj[node]:
        if child == parent:
            continue
        dfs(child, node, adj)

    # POST-ORDER: process node after children
    print(f"Leave {node}")
```

```
Tree:       1
           / \
          2   3
         / \
        4   5

Pre-order:  1, 2, 4, 5, 3  (enter order — top down)
Post-order: 4, 5, 2, 3, 1  (leave order — bottom up)
```

### BFS (Breadth-First Search)

Goes level by level. Used for shortest paths in unweighted trees.

```python
from collections import deque

def bfs(root, adj):
    dist = [-1] * len(adj)
    dist[root] = 0
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for child in adj[node]:
            if dist[child] == -1:
                dist[child] = dist[node] + 1
                queue.append(child)
    return dist
```

### When to Use Which

| DFS | BFS |
|-----|-----|
| Subtree computations | Level-order processing |
| Path problems | Shortest distance (unweighted) |
| Euler tour, HLD, LCA | Finding tree diameter |
| Most tree DP | Multi-source BFS on trees |

### Iterative DFS (for large trees in Python)

```python
def dfs_iterative(root, adj):
    parent = [-1] * len(adj)
    order = []  # stores nodes in DFS pre-order
    stack = [(root, -1, False)]

    while stack:
        node, par, visited = stack.pop()
        if visited:
            # POST-ORDER work here
            continue
        parent[node] = par
        order.append(node)
        stack.append((node, par, True))  # for post-order
        for child in adj[node]:
            if child != par:
                stack.append((child, node, False))
    return order, parent
```

---

## 2. Euler Tour (Subtree Queries)

**Problem type**: "Query/update all nodes in the subtree of X"

### The Idea

DFS assigns each node an **enter time** (`tin`) and **exit time** (`tout`). A node's entire subtree falls within `[tin[node], tout[node]]` in the flattened array.

```
Tree:        0
            / \
           1   2
          / \
         3   4

DFS order:  0 -> 1 -> 3 -> 4 -> 2

tin:   [0, 1, 4, 2, 3]
tout:  [4, 3, 4, 2, 3]

Flat array: [0] [1] [3] [4] [2]
             0   1   2   3   4

Subtree of 1: tin[1]=1, tout[1]=3 -> range [1..3] -> nodes 1,3,4  ✓
```

### Implementation

```python
class EulerTour:
    def __init__(self, n, adj, root=0):
        self.tin = [0] * n
        self.tout = [0] * n
        self.timer = 0
        self.parent = [-1] * n
        self._dfs(root, -1, adj)

    def _dfs(self, node, par, adj):
        self.parent[node] = par
        self.tin[node] = self.timer
        self.timer += 1
        for child in adj[node]:
            if child != par:
                self._dfs(child, node, adj)
        self.tout[node] = self.timer - 1

    def is_ancestor(self, u, v):
        """O(1) ancestor check."""
        return self.tin[u] <= self.tin[v] <= self.tout[u]

    def subtree_range(self, node):
        """Range in flat array covering node's subtree."""
        return self.tin[node], self.tout[node]
```

### Combine with Segment Tree

```python
# Subtree sum query
seg.query(tin[node], tout[node])

# Update node value
seg.update(tin[node], new_value)

# Update all nodes in subtree (lazy segment tree)
seg.range_update(tin[node], tout[node], delta)
```

### What Euler Tour Can Do

| Operation | How | Complexity |
|-----------|-----|------------|
| Subtree sum/min/max | Segment tree on [tin, tout] | O(log N) |
| Subtree update | Lazy segment tree | O(log N) |
| Is u ancestor of v? | `tin[u] <= tin[v] <= tout[u]` | O(1) |
| Subtree size | `tout[u] - tin[u] + 1` | O(1) |
| LCA (with RMQ) | Min depth in Euler tour range | O(1) |

---

## 3. Heavy-Light Decomposition (Path Queries)

**Problem type**: "Query/update all nodes on the path from X to Y"

### The Idea

Decompose the tree into **heavy chains** (paths following the heaviest child). Each chain maps to a contiguous range in a flat array. Path queries break into O(log N) chain segments.

```
Tree:        0
            / \
      heavy/   \light
          1     2
    heavy/ \light
        3    4
  heavy/
      5

Chain A: 0->1->3->5  (contiguous in array)
Chain B: 4
Chain C: 2
```

### Implementation

```python
class HLD:
    def __init__(self, n, adj, root=0):
        self.n = n
        self.adj = adj
        self.parent = [-1] * n
        self.depth = [0] * n
        self.subtree_size = [1] * n
        self.heavy_child = [-1] * n
        self.chain_head = [0] * n
        self.pos = [0] * n
        self.timer = 0

        self._dfs_size(root, -1)
        self.chain_head[root] = root
        self._dfs_hld(root)

    def _dfs_size(self, node, par):
        self.parent[node] = par
        self.depth[node] = 0 if par == -1 else self.depth[par] + 1
        self.subtree_size[node] = 1
        max_size = 0
        for nb in self.adj[node]:
            if nb == par:
                continue
            self._dfs_size(nb, node)
            self.subtree_size[node] += self.subtree_size[nb]
            if self.subtree_size[nb] > max_size:
                max_size = self.subtree_size[nb]
                self.heavy_child[node] = nb

    def _dfs_hld(self, node):
        self.pos[node] = self.timer
        self.timer += 1
        hc = self.heavy_child[node]
        if hc != -1:
            self.chain_head[hc] = self.chain_head[node]
            self._dfs_hld(hc)
        for nb in self.adj[node]:
            if nb == self.parent[node] or nb == hc:
                continue
            self.chain_head[nb] = nb
            self._dfs_hld(nb)

    def query_path(self, u, v, seg):
        """Sum on path u->v using a segment tree."""
        result = 0
        while self.chain_head[u] != self.chain_head[v]:
            if self.depth[self.chain_head[u]] < self.depth[self.chain_head[v]]:
                u, v = v, u
            result += seg.query(self.pos[self.chain_head[u]], self.pos[u])
            u = self.parent[self.chain_head[u]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        result += seg.query(self.pos[u], self.pos[v])
        return result

    def lca(self, u, v):
        """LCA as a bonus from HLD."""
        while self.chain_head[u] != self.chain_head[v]:
            if self.depth[self.chain_head[u]] < self.depth[self.chain_head[v]]:
                u, v = v, u
            u = self.parent[self.chain_head[u]]
        return u if self.depth[u] <= self.depth[v] else v
```

### What HLD Can Do

| Operation | Complexity |
|-----------|------------|
| Path sum/min/max query | O(log^2 N) |
| Path update | O(log^2 N) |
| LCA | O(log N) |
| Subtree query (bonus!) | O(log N) via `pos[node]..pos[node]+size-1` |

### Euler Tour vs HLD

| | Euler Tour | HLD |
|--|-----------|-----|
| Subtree queries | Yes (native) | Yes (bonus) |
| Path queries | No | Yes (native) |
| Build complexity | O(N) | O(N) |
| Query complexity | O(log N) | O(log^2 N) |

**Rule of thumb**: Need only subtree queries? Euler Tour is simpler. Need path queries (or both)? Use HLD.

---

## 4. Lowest Common Ancestor

**Problem type**: "Find the deepest common ancestor of two nodes"

See the detailed [LCA Pattern Guide](/pattern/lca) for full coverage. Summary:

### Binary Lifting (Most Common)

```python
LOG = 20

class LCA:
    def __init__(self, n, adj, root=0):
        self.depth = [0] * n
        self.up = [[-1] * n for _ in range(LOG)]
        self._dfs(root, -1, adj)
        self._build()

    def _dfs(self, node, par, adj):
        self.up[0][node] = par
        for nb in adj[node]:
            if nb != par:
                self.depth[nb] = self.depth[node] + 1
                self._dfs(nb, node, adj)

    def _build(self):
        for k in range(1, LOG):
            for v in range(len(self.depth)):
                mid = self.up[k-1][v]
                self.up[k][v] = -1 if mid == -1 else self.up[k-1][mid]

    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        diff = self.depth[u] - self.depth[v]
        for k in range(LOG):
            if diff & (1 << k):
                u = self.up[k][u]
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        return self.up[0][u]

    def dist(self, u, v):
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]
```

### Technique Comparison

| Method | Preprocess | Query | Best for |
|--------|-----------|-------|----------|
| Binary Lifting | O(N log N) | O(log N) | General purpose, simple |
| Euler Tour + Sparse Table | O(N log N) | O(1) | Many queries |
| HLD | O(N) | O(log N) | Already using HLD |
| Tarjan's (offline) | O(N + Q) | Amortized O(1) | All queries known upfront |

---

## 5. Rerooting DP

**Problem type**: "Compute some value for every node as if it were the root"

### The Problem

Normal tree DP computes the answer rooted at one node. Rerooting computes the answer for **all N roots** in O(N) total (not O(N^2)).

```
"For each node, what is the farthest node from it?"
"For each node, what is the sum of distances to all other nodes?"

Naive: run tree DP N times -> O(N^2)
Rerooting: 2 DFS passes -> O(N)
```

### The Idea

```
Phase 1 (DFS down): Compute dp_down[node] = answer from node's subtree
Phase 2 (DFS up):   Compute dp_up[node] = answer from everything OUTSIDE node's subtree
Final:              answer[node] = combine(dp_down[node], dp_up[node])
```

```
         0            dp_down[2]: info from subtree of 2
        / \           dp_up[2]:   info from 0's other children + above 0
       1   2
      / \   \
     3   4   5

answer[2] = combine(dp_down[2], dp_up[2])
           = answer as if 2 were the root
```

### Example: Sum of Distances to All Nodes

**Problem**: For each node, find the sum of distances to all other nodes.

```python
def sum_of_distances(n, adj):
    subtree_size = [1] * n
    dp_down = [0] * n   # sum of distances within subtree
    answer = [0] * n

    # Phase 1: DFS down (post-order)
    def dfs_down(node, par):
        for child in adj[node]:
            if child == par:
                continue
            dfs_down(child, node)
            subtree_size[node] += subtree_size[child]
            dp_down[node] += dp_down[child] + subtree_size[child]
            #                                  ^^^^^^^^^^^^^^^^^^
            #                   each node in child's subtree is 1 edge farther

    # Phase 2: DFS up (pre-order)
    def dfs_up(node, par):
        answer[node] = dp_down[node]  # will add dp_up contribution
        if par != -1:
            # dp_up = parent's answer minus our subtree's contribution
            # then add 1 for each node outside our subtree
            outside = answer[par] - (dp_down[node] + subtree_size[node])
            answer[node] += outside + (n - subtree_size[node])

        for child in adj[node]:
            if child != par:
                dfs_up(child, node)

    dfs_down(0, -1)
    answer[0] = dp_down[0]
    dfs_up(0, -1)
    return answer
```

### Example: Farthest Node from Each Node (Tree Distances I)

```python
def farthest_from_each(n, adj):
    # dp_down[node] = [longest_path, second_longest_path] going downward
    dp_down = [[0, 0] for _ in range(n)]
    dp_down_child = [[-1, -1] for _ in range(n)]  # which child gave longest
    dp_up = [0] * n

    def dfs_down(node, par):
        for child in adj[node]:
            if child == par:
                continue
            dfs_down(child, node)
            d = dp_down[child][0] + 1
            if d > dp_down[node][0]:
                dp_down[node][1] = dp_down[node][0]
                dp_down_child[node][1] = dp_down_child[node][0]
                dp_down[node][0] = d
                dp_down_child[node][0] = child
            elif d > dp_down[node][1]:
                dp_down[node][1] = d
                dp_down_child[node][1] = child

    def dfs_up(node, par):
        for child in adj[node]:
            if child == par:
                continue
            # if child gave the longest path, use second longest
            if dp_down_child[node][0] == child:
                best_down = dp_down[node][1]
            else:
                best_down = dp_down[node][0]
            dp_up[child] = 1 + max(dp_up[node], best_down)
            dfs_up(child, node)

    dfs_down(0, -1)
    dfs_up(0, -1)
    return [max(dp_down[i][0], dp_up[i]) for i in range(n)]
```

### Rerooting Template

```
1. Define what dp_down[node] computes (info from subtree)
2. Define what dp_up[node] computes (info from outside subtree)
3. DFS 1 (post-order): compute dp_down for all nodes
4. DFS 2 (pre-order): compute dp_up using parent's dp_down + dp_up
   KEY: when computing dp_up[child], remove child's contribution from
        parent's dp_down (to avoid double-counting)
5. answer[node] = combine(dp_down[node], dp_up[node])
```

---

## 6. Tree Diameter and Center

### Diameter: Longest Path in Tree

**Method 1: Two BFS/DFS** (simplest)

```python
from collections import deque

def tree_diameter(n, adj):
    def bfs_farthest(start):
        dist = [-1] * n
        dist[start] = 0
        queue = deque([start])
        farthest = start
        while queue:
            node = queue.popleft()
            for nb in adj[node]:
                if dist[nb] == -1:
                    dist[nb] = dist[node] + 1
                    queue.append(nb)
                    if dist[nb] > dist[farthest]:
                        farthest = nb
        return farthest, dist

    # Step 1: BFS from any node to find one endpoint
    u, _ = bfs_farthest(0)
    # Step 2: BFS from u to find the other endpoint + diameter
    v, dist = bfs_farthest(u)
    return dist[v]  # diameter
```

**Why does this work?** Starting from any node, the farthest node must be an endpoint of some diameter. From that endpoint, the farthest node gives the other endpoint.

**Method 2: Tree DP** (also finds the node where diameter passes through)

```python
def diameter_dp(n, adj):
    diameter = [0]

    def dfs(node, par):
        first = second = 0  # two longest downward paths
        for child in adj[node]:
            if child == par:
                continue
            d = dfs(child, node) + 1
            if d > first:
                second = first
                first = d
            elif d > second:
                second = d
        diameter[0] = max(diameter[0], first + second)
        return first

    dfs(0, -1)
    return diameter[0]
```

### Center of Tree

The center is the node(s) that minimize the maximum distance to any other node. It's always 1 or 2 nodes, located at the **middle of the diameter**.

```python
def tree_center(n, adj):
    """Peel leaves layer by layer until 1-2 nodes remain."""
    if n <= 2:
        return list(range(n))

    degree = [len(adj[i]) for i in range(n)]
    # for trees: adjust for undirected adjacency
    leaves = deque(i for i in range(n) if degree[i] <= 1)
    remaining = n

    while remaining > 2:
        new_leaves = deque()
        for leaf in leaves:
            remaining -= 1
            for nb in adj[leaf]:
                degree[nb] -= 1
                if degree[nb] == 1:
                    new_leaves.append(nb)
        leaves = new_leaves

    return list(leaves)
```

This is essentially **topological peeling**: remove all leaves, then remove the new leaves, repeat until 1-2 nodes remain.

---

## 7. Centroid Decomposition

**Problem type**: "For each node, count/query something based on **distances** to other nodes"

### The Idea

The **centroid** of a tree is the node whose removal splits the tree into subtrees each of size <= N/2.

Centroid decomposition recursively finds centroids to build a **centroid tree** of depth O(log N). Every path in the original tree passes through the LCA in the centroid tree.

```
Original:           Centroid Tree (depth O(log N)):
    1                       3
   / \                    / | \
  2   3                  1  5  6
     / \                /     \
    4   5              2       4
   /
  6

Centroid of full tree = 3
Centroid of {1,2} = 1 (or 2)
Centroid of {4,5,6} = 5 (or 4)
```

### Finding the Centroid

```python
def find_centroid(node, par, adj, subtree_size, tree_size):
    for child in adj[node]:
        if child == par and subtree_size[child] > tree_size // 2:
            # this subtree is too big, centroid is in there
            return find_centroid(child, node, adj, subtree_size, tree_size)
    return node
```

More robust version:

```python
def centroid_decomposition(n, adj):
    subtree_size = [0] * n
    removed = [False] * n
    centroid_parent = [-1] * n

    def get_size(node, par):
        subtree_size[node] = 1
        for child in adj[node]:
            if child != par and not removed[child]:
                get_size(child, node)
                subtree_size[node] += subtree_size[child]
        return subtree_size[node]

    def get_centroid(node, par, tree_size):
        for child in adj[node]:
            if child != par and not removed[child]:
                if subtree_size[child] > tree_size // 2:
                    return get_centroid(child, node, tree_size)
        return node

    def build(node, par):
        size = get_size(node, -1)
        centroid = get_centroid(node, -1, size)
        removed[centroid] = True
        centroid_parent[centroid] = par

        for child in adj[centroid]:
            if not removed[child]:
                build(child, centroid)

    build(0, -1)
    return centroid_parent
```

### Example: Count Pairs with Distance = K

```python
def count_pairs_distance_k(n, adj, k):
    """Count pairs (u,v) where dist(u,v) = k."""
    removed = [False] * n
    subtree_size = [0] * n
    total = 0

    def get_size(node, par):
        subtree_size[node] = 1
        for child in adj[node]:
            if child != par and not removed[child]:
                get_size(child, node)
                subtree_size[node] += subtree_size[child]

    def get_centroid(node, par, tree_size):
        for child in adj[node]:
            if child != par and not removed[child]:
                if subtree_size[child] > tree_size // 2:
                    return get_centroid(child, node, tree_size)
        return node

    def get_depths(node, par, depth, depths):
        depths.append(depth)
        for child in adj[node]:
            if child != par and not removed[child]:
                get_depths(child, node, depth + 1, depths)

    def solve(node):
        nonlocal total
        get_size(node, -1)
        centroid = get_centroid(node, -1, subtree_size[node])
        removed[centroid] = True

        # count paths passing through centroid
        seen = {0: 1}  # distances from centroid already counted
        for child in adj[centroid]:
            if removed[child]:
                continue
            depths = []
            get_depths(child, centroid, 1, depths)
            # count pairs: one from this subtree, one from previous subtrees
            for d in depths:
                need = k - d
                if need >= 0 and need in seen:
                    total += seen[need]
            # add this subtree's depths to seen
            for d in depths:
                seen[d] = seen.get(d, 0) + 1

        for child in adj[centroid]:
            if not removed[child]:
                solve(child)

    solve(0)
    return total
```

### Why Centroid Decomposition Works

Every path between two nodes passes through their LCA in the centroid tree. Since the centroid tree has depth O(log N), each node is involved in at most O(log N) centroid computations.

| Operation | Without CD | With CD |
|-----------|-----------|---------|
| Count pairs at distance K | O(N^2) | O(N log N) |
| Closest marked node query | O(N) per query | O(log^2 N) per query |
| Update + distance queries | O(N) per query | O(log^2 N) per query |

---

## 8. Small-to-Large Merging (DSU on Tree)

**Problem type**: "For each node, answer a query about its subtree" — especially when maintaining a **data structure** (set, map, frequency array) per subtree.

### The Idea

Naive approach: each node has its own set. After computing children, merge all child sets into the parent. This is O(N^2) worst case.

**Small-to-large trick**: Always merge the **smaller** set into the **larger** one. Each element is moved at most O(log N) times (because each move at least doubles the set size it joins).

```
        1 (want: set of colors in subtree)
       / \
      2   3
     /|    \
    4 5     6

Without optimization: merge 4,5 into 2, then merge 2,3,6 into 1
  If sizes are uneven, one merge could be O(N)

With small-to-large: always merge smaller into bigger
  Each color moves at most O(log N) times across all merges
```

### Example: Distinct Colors in Each Subtree

```python
def distinct_colors(n, adj, colors):
    """For each node, count distinct colors in its subtree."""
    answer = [0] * n

    # Each node owns a set. We'll pass sets up the tree.
    node_set = [None] * n

    def dfs(node, par):
        node_set[node] = {colors[node]}

        for child in adj[node]:
            if child == par:
                continue
            dfs(child, node)

            # small-to-large merge
            if len(node_set[child]) > len(node_set[node]):
                node_set[node], node_set[child] = node_set[child], node_set[node]

            # merge smaller into larger
            node_set[node].update(node_set[child])
            node_set[child] = None  # free memory

        answer[node] = len(node_set[node])

    dfs(0, -1)
    return answer
```

### Euler Tour + Offline Approach (Alternative)

For "distinct values in subtree" problems, you can also:
1. Flatten tree with Euler Tour
2. Process subtree ranges `[tin[v], tout[v]]` using offline techniques (Mo's algorithm)

### Complexity

| Approach | Time | Space |
|----------|------|-------|
| Naive merge | O(N^2) | O(N) |
| Small-to-large | **O(N log N)** | O(N) |
| Euler Tour + Mo's | O(N sqrt(N)) | O(N) |

---

## 9. Tree DP Patterns

A collection of the most common tree DP patterns.

### Pattern 1: Subtree Aggregation

```
dp[node] = f(dp[children])
Direction: post-order (bottom up)
```

**Example: Subtree Sum**

```python
def subtree_sum(node, par, adj, val):
    total = val[node]
    for child in adj[node]:
        if child != par:
            total += subtree_sum(child, node, adj, val)
    return total
```

### Pattern 2: Select/Skip (Independent Set)

```
dp[node][0] = best when node is NOT selected
dp[node][1] = best when node IS selected

dp[node][0] = sum(max(dp[child][0], dp[child][1]))
dp[node][1] = val[node] + sum(dp[child][0])
```

```python
def max_independent_set(n, adj, val, root=0):
    dp = [[0, 0] for _ in range(n)]

    def dfs(node, par):
        dp[node][1] = val[node]
        for child in adj[node]:
            if child == par:
                continue
            dfs(child, node)
            dp[node][0] += max(dp[child][0], dp[child][1])
            dp[node][1] += dp[child][0]

    dfs(root, -1)
    return max(dp[root])
```

### Pattern 3: Matching on Tree

```
dp[node][0] = max matching in subtree, node is NOT matched
dp[node][1] = max matching in subtree, node IS matched (to one child)

dp[node][0] = sum(max(dp[child][0], dp[child][1]))
dp[node][1] = max over children c of:
              (dp[c][0] + 1) + sum(max(dp[other][0], dp[other][1]))
```

```python
def max_matching(n, adj, root=0):
    dp = [[0, 0] for _ in range(n)]

    def dfs(node, par):
        sum_unmatched = 0
        for child in adj[node]:
            if child == par:
                continue
            dfs(child, node)
            sum_unmatched += max(dp[child][0], dp[child][1])

        dp[node][0] = sum_unmatched

        # try matching node with each child
        for child in adj[node]:
            if child == par:
                continue
            gain = dp[child][0] + 1 - max(dp[child][0], dp[child][1])
            dp[node][1] = max(dp[node][1], sum_unmatched + gain)

    dfs(root, -1)
    return max(dp[root])
```

### Pattern 4: Coloring / Partition

```
dp[node][color] = ways to color subtree with node = color

dp[node][c] = product(sum(dp[child][c'] for valid c') for each child)
```

### Pattern 5: Path Through Node

Track the two longest paths through each node to find diameter or similar.

```python
def paths_through_node(n, adj, root=0):
    """For each node, find the longest path passing through it."""
    best = [0] * n

    def dfs(node, par):
        first = second = 0
        for child in adj[node]:
            if child == par:
                continue
            d = dfs(child, node) + 1
            if d > first:
                first, second = d, first
            elif d > second:
                second = d
        best[node] = first + second  # longest path through this node
        return first  # longest downward path

    dfs(root, -1)
    return best
```

### Tree DP Summary

| Pattern | States | Common Problems |
|---------|--------|----------------|
| Subtree aggregation | dp[node] | Subtree sum, size, count |
| Select/Skip | dp[node][0/1] | Independent set, house robber on tree |
| Matching | dp[node][0/1] | Maximum matching |
| Coloring | dp[node][color] | Chromatic polynomial, valid colorings |
| Path through node | first/second longest | Diameter, longest path |
| Rerooting | dp_down + dp_up | Answer for every root |

---

## 10. Virtual Tree (Auxiliary Tree)

**Problem type**: "Given Q queries, each involving a small subset of K nodes, answer something about the tree structure connecting them"

### The Idea

Instead of working on the full N-node tree, build a **virtual tree** containing only:
- The K query nodes
- Their pairwise LCAs

This reduces the tree to at most **2K - 1 nodes**.

```
Full tree (10 nodes):        Virtual tree for nodes {3, 7, 9}:

         1                           1
        / \                         / \
       2   3                       3   5
      / \                              \
     4   5                              8
    /   / \                              \
   6   7   8                              9
      /     \
     9      10

Only 5 nodes: {1, 3, 5, 8, 9}  (query nodes + LCAs)
```

### Building a Virtual Tree

```python
def build_virtual_tree(query_nodes, tin, lca_func):
    """
    query_nodes: list of node IDs
    tin: euler tour enter times
    lca_func: function that computes LCA of two nodes
    Returns: adjacency list of virtual tree
    """
    # Step 1: sort by tin
    nodes = sorted(query_nodes, key=lambda x: tin[x])

    # Step 2: add LCAs of consecutive pairs
    all_nodes = list(nodes)
    for i in range(len(nodes) - 1):
        l = lca_func(nodes[i], nodes[i + 1])
        all_nodes.append(l)

    # Step 3: deduplicate and sort by tin
    all_nodes = sorted(set(all_nodes), key=lambda x: tin[x])

    # Step 4: add LCAs from stack-based construction
    stack = [all_nodes[0]]
    vtree = {node: [] for node in all_nodes}

    for i in range(1, len(all_nodes)):
        node = all_nodes[i]
        l = lca_func(node, stack[-1])

        if l != stack[-1]:
            while len(stack) > 1 and tin[stack[-2]] >= tin[l]:
                vtree[stack[-2]].append(stack[-1])
                stack.pop()
            if stack[-1] != l:
                vtree[l].append(stack[-1])
                stack[-1] = l

        stack.append(node)

    while len(stack) > 1:
        vtree[stack[-2]].append(stack[-1])
        stack.pop()

    return vtree, stack[0]  # virtual tree adj + root
```

### When to Use

- K << N (small query set, large tree)
- Multiple queries, each on a different subset
- Need to run tree DP only on relevant nodes

---

## 11. Prufer Sequence

A way to **encode** a labeled tree of N nodes as a sequence of N-2 numbers.

### Tree to Prufer Sequence

```
Tree:  1 - 3 - 2 - 4
              |
              5

Repeatedly remove the leaf with the smallest label, record its neighbor:

Remove 1 (leaf), neighbor = 3  -> sequence: [3]
Remove 4 (leaf), neighbor = 2  -> sequence: [3, 2]
Remove 5 (leaf), neighbor = 3  -> sequence: [3, 2, 3]
Remaining: {2, 3}              -> stop (N-2 = 3 elements)

Prufer sequence: [3, 2, 3]
```

```python
def tree_to_prufer(n, adj):
    degree = [len(adj[i]) for i in range(n)]
    sequence = []
    leaf = -1
    # find smallest leaf
    for i in range(n):
        if degree[i] == 1:
            leaf = i
            break

    ptr = leaf
    for _ in range(n - 2):
        # find neighbor of current leaf
        for nb in adj[ptr]:
            if degree[nb] > 0:
                neighbor = nb
                break
        sequence.append(neighbor)
        degree[ptr] = 0
        degree[neighbor] -= 1

        if degree[neighbor] == 1 and neighbor < ptr:
            ptr = neighbor  # optimization: this neighbor is now a leaf
        else:
            ptr += 1
            while ptr < n and degree[ptr] != 1:
                ptr += 1

    return sequence
```

### Prufer Sequence to Tree

```python
def prufer_to_tree(sequence):
    n = len(sequence) + 2
    degree = [1] * n
    for x in sequence:
        degree[x] += 1

    edges = []
    ptr = 0
    while degree[ptr] != 1:
        ptr += 1

    leaf = ptr
    for x in sequence:
        edges.append((leaf, x))
        degree[leaf] -= 1
        degree[x] -= 1
        if degree[x] == 1 and x < ptr:
            leaf = x
        else:
            ptr += 1
            while ptr < n and degree[ptr] != 1:
                ptr += 1
            leaf = ptr

    edges.append((leaf, n - 1))
    return edges
```

### Key Properties

| Property | Value |
|----------|-------|
| Number of labeled trees on N nodes | **N^(N-2)** (Cayley's formula) |
| Node i appears in Prufer sequence | degree(i) - 1 times |
| Leaves of the tree | Nodes NOT in the sequence |
| Bijection | Every sequence of N-2 values in [0, N-1] gives a unique tree |

---

## 12. Tree Hashing and Isomorphism

**Problem type**: "Are these two trees structurally identical?" or "Find all subtrees with the same structure"

### The Idea

Assign each subtree a **hash** based on its children's hashes (sorted). Two subtrees are isomorphic if and only if they have the same hash.

```
     1            5
    / \          / \
   2   3        6   7
  /            /
 4            8

Subtree at 2: hash of (hash(4)) = H_chain2
Subtree at 6: hash of (hash(8)) = H_chain2  (same structure!)
```

### Implementation

```python
from collections import defaultdict

def tree_hash(n, adj, root=0):
    """Compute a canonical hash for each subtree."""
    memo = {}  # tuple -> unique id
    counter = [0]
    node_hash = [0] * n

    def get_id(signature):
        if signature not in memo:
            memo[signature] = counter[0]
            counter[0] += 1
        return memo[signature]

    def dfs(node, par):
        child_hashes = []
        for child in adj[node]:
            if child == par:
                continue
            dfs(child, node)
            child_hashes.append(node_hash[child])
        child_hashes.sort()  # canonical ordering
        node_hash[node] = get_id(tuple(child_hashes))

    dfs(root, -1)
    return node_hash
```

### Rooted vs Unrooted Isomorphism

**Rooted**: Hash from the given root. Two rooted trees are isomorphic if root hashes match.

**Unrooted**: Root both trees at their **center** (the center is unique up to 2 nodes). If 2 centers, try both. Compare hashes.

```python
def are_isomorphic(adj1, adj2):
    n1, n2 = len(adj1), len(adj2)
    if n1 != n2:
        return False

    centers1 = tree_center(n1, adj1)
    centers2 = tree_center(n2, adj2)

    for c1 in centers1:
        h1 = tree_hash(n1, adj1, c1)
        for c2 in centers2:
            h2 = tree_hash(n2, adj2, c2)
            if h1[c1] == h2[c2]:
                return True
    return False
```

---

## 13. Pattern Recognition Cheat Sheet

### By Query Type

| Query | Technique | Complexity |
|-------|-----------|------------|
| Subtree sum/min/max | Euler Tour + Segment Tree | O(log N) |
| Subtree update | Euler Tour + Lazy Segment Tree | O(log N) |
| Path sum/min/max | HLD + Segment Tree | O(log^2 N) |
| Path update | HLD + Lazy Segment Tree | O(log^2 N) |
| LCA query | Binary Lifting / Euler+RMQ | O(log N) / O(1) |
| Distance(u, v) | LCA + depth | O(log N) |
| Answer for all roots | Rerooting DP | O(N) total |
| Count pairs at distance K | Centroid Decomposition | O(N log N) |
| Distinct values in subtree | DSU on Tree / Mo's | O(N log N) |
| Is u ancestor of v? | Euler Tour tin/tout | O(1) |
| Tree diameter | Two-BFS or DP | O(N) |
| Tree isomorphism | Tree hashing at center | O(N) |

### By Problem Keywords

| You see... | Think... |
|------------|----------|
| "subtree query" | Euler Tour |
| "path query" | HLD |
| "distance between nodes" | LCA |
| "for every node as root" | Rerooting DP |
| "farthest node" | Tree Diameter + Rerooting |
| "count paths with property" | Centroid Decomposition |
| "distinct in subtree" | DSU on Tree |
| "maximum independent set" | Tree DP (select/skip) |
| "tree matching" | Tree DP (match/unmatch) |
| "same structure" | Tree Hashing |
| "labeled tree counting" | Cayley's formula / Prufer |
| "small subset of nodes" | Virtual Tree |

### Technique Compatibility

Multiple techniques are often combined:

```
Euler Tour + Segment Tree         -> subtree queries with updates
HLD + Segment Tree                -> path queries with updates
HLD + LCA                         -> path queries (LCA is free with HLD)
Centroid Decomp + BIT/Fenwick     -> distance-based queries with updates
Binary Lifting + Path aggregation -> weighted path queries
Rerooting DP + Tree DP            -> answer for all roots
Virtual Tree + Tree DP            -> DP on selected subset efficiently
```

### Decision Flowchart

```
What do you need to query?
    |
    +-- Subtree? --> Euler Tour + Segment Tree
    |
    +-- Path? --> HLD + Segment Tree
    |
    +-- LCA? --> Binary Lifting (simple) or Euler+Sparse (O(1))
    |
    +-- Every root? --> Rerooting DP
    |
    +-- Distance-based counting? --> Centroid Decomposition
    |
    +-- Merging child data structures? --> Small-to-Large
    |
    +-- Subtree DP value? --> Tree DP (select/skip or aggregate)
    |
    +-- Only K << N nodes matter? --> Virtual Tree
```
