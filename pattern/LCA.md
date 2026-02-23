---
layout: simple
title: "Lowest Common Ancestor (LCA)"
permalink: /pattern/lca
---

# Lowest Common Ancestor (LCA) — Complete Guide

---

## What Is LCA?

Given a rooted tree and two nodes **u** and **v**, their **Lowest Common Ancestor** is the deepest node that is an ancestor of both.

```
              0
             / \
            1   2
           / \   \
          3   4   5
         / \
        6   7

LCA(6, 4) = 1      (1 is the deepest node above both 6 and 4)
LCA(6, 7) = 3      (3 is parent of both)
LCA(6, 5) = 0      (have to go all the way to root)
LCA(3, 3) = 3      (a node is its own ancestor)
```

### Why Does LCA Matter?

LCA is a **building block** for many tree problems:

| Problem | How LCA helps |
|---------|---------------|
| Distance between u and v | `depth[u] + depth[v] - 2*depth[LCA(u,v)]` |
| Path sum/max/min on trees | Split path at LCA: `u->LCA` + `LCA->v` |
| HLD path queries | `query_path` internally finds LCA while climbing chains |
| Tree diff (version control) | Find common base of two branches |
| Phylogenetic trees (biology) | Find most recent common ancestor of species |

---

## Technique 1: Brute Force (Climb Up)

### Idea

Make u and v the same depth, then climb both up one step at a time until they meet.

```
LCA(6, 4):

Step 1: depth[6]=3, depth[4]=2 -> bring 6 up to depth 2
        6 -> parent[6] = 3

Step 2: now both at depth 2: node 3 and node 4
        3 != 4, climb both:
        3 -> parent[3] = 1
        4 -> parent[4] = 1

Step 3: both are node 1 -> LCA = 1
```

### Implementation

```python
def lca_brute(u, v, parent, depth):
    # step 1: equalize depths
    while depth[u] > depth[v]:
        u = parent[u]
    while depth[v] > depth[u]:
        v = parent[v]

    # step 2: climb together
    while u != v:
        u = parent[u]
        v = parent[v]

    return u
```

### Complexity

| | Time | Space |
|--|------|-------|
| Preprocess | O(N) --- one DFS for parent/depth | O(N) |
| Query | **O(N)** --- worst case climb entire tree | --- |

**Verdict**: Simple but too slow for many queries. A straight-line tree (path graph) always gives O(N).

---

## Technique 2: Binary Lifting

### Idea

Instead of climbing one step at a time, climb in **powers of 2**. Pre-compute `up[node][k]` = the ancestor 2^k steps above `node`.

```
up[node][0] = parent                (1 step  = 2^0)
up[node][1] = grandparent           (2 steps = 2^1)
up[node][2] = great-great-grandpa   (4 steps = 2^2)
...
up[node][k] = up[up[node][k-1]][k-1]   (2^k = 2^(k-1) + 2^(k-1))
```

Think of it like how you'd jump 13 floors in an elevator: jump 8, then 4, then 1 (13 = 1101 in binary).

### Walkthrough

```
Tree:
         0 (depth 0)
         |
         1 (depth 1)
         |
         2 (depth 2)
         |
         3 (depth 3)
         |
         4 (depth 4)

up table:
         k=0(1)  k=1(2)  k=2(4)
node 0:   -1      -1      -1
node 1:    0      -1      -1
node 2:    1       0      -1
node 3:    2       1      -1
node 4:    3       2       0

LCA(4, 2):
  depth[4]=4, depth[2]=2, diff=2
  Climb 4 by 2 steps: up[4][1] = 2
  Now both at node 2 -> LCA = 2
```

### Implementation

```python
import sys
sys.setrecursionlimit(200_000)

LOG = 20  # enough for N up to 10^6

class BinaryLifting:
    def __init__(self, n, adj, root=0):
        self.n = n
        self.adj = adj
        self.depth = [0] * n
        self.up = [[-1] * n for _ in range(LOG)]  # up[k][node]

        self._dfs(root, -1)
        self._build()

    def _dfs(self, node, par):
        self.up[0][node] = par  # parent = 2^0 ancestor
        for nb in self.adj[node]:
            if nb == par:
                continue
            self.depth[nb] = self.depth[node] + 1
            self._dfs(nb, node)

    def _build(self):
        """Fill the binary lifting table bottom-up."""
        for k in range(1, LOG):
            for v in range(self.n):
                mid = self.up[k - 1][v]
                if mid == -1:
                    self.up[k][v] = -1
                else:
                    self.up[k][v] = self.up[k - 1][mid]

    def _lift(self, node, dist):
        """Climb `dist` steps from node."""
        for k in range(LOG):
            if dist & (1 << k):
                node = self.up[k][node]
                if node == -1:
                    return -1
        return node

    def lca(self, u, v):
        # step 1: bring deeper node up
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self._lift(u, self.depth[u] - self.depth[v])

        # step 2: if same, we're done
        if u == v:
            return u

        # step 3: climb both in powers of 2
        for k in range(LOG - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]

        # now u and v are children of the LCA
        return self.up[0][u]
```

### Why Step 3 Works

```
LCA(6, 5) in this tree:

              0
             / \
            1   2
           / \   \
          3   4   5
         / \
        6   7

After equalizing depth: u=3, v=5 (both depth 2)

k=2: up[2][3]=? (4 steps up from 3 -- doesn't exist) = -1
     up[2][5]=? = -1
     Equal (-1 == -1), DON'T jump. (would overshoot)

k=1: up[1][3]=0, up[1][5]=0
     Equal (0 == 0), DON'T jump. (would land ON the LCA)

k=0: up[0][3]=1, up[0][5]=2
     Different! Jump: u=1, v=2

Now up[0][1] = up[0][2] = 0 -> LCA = 0
```

**Key insight**: We deliberately **don't** jump when ancestors match. We want to land **just below** the LCA, then go up one final step. This avoids overshooting.

### Complexity

| | Time | Space |
|--|------|-------|
| Preprocess | O(N log N) | O(N log N) |
| Query | **O(log N)** | --- |

**Verdict**: The most popular technique. Great balance of simplicity and speed. Works online (queries arrive one by one).

---

## Technique 3: Euler Tour + Sparse Table (RMQ)

### Idea

Reduce LCA to a **Range Minimum Query** problem. Then solve RMQ with a sparse table for O(1) queries.

**The reduction**:
1. Do an Euler Tour, recording nodes as you enter AND revisit them
2. LCA(u, v) = the shallowest node between the first occurrence of u and v in the tour

```
Tree:         0
             / \
            1   2
           / \
          3   4

Euler Tour (record every visit):
Visit:  0  1  3  1  4  1  0  2  0
Depth:  0  1  2  1  2  1  0  1  0
Index:  0  1  2  3  4  5  6  7  8

First occurrence:
  first[0]=0, first[1]=1, first[2]=7, first[3]=2, first[4]=4

LCA(3, 4):
  first[3]=2, first[4]=4
  Look at depths in range [2..4]: depths = [2, 1, 2]
  Minimum depth = 1 at index 3 -> node 1
  LCA = 1

LCA(3, 2):
  first[3]=2, first[2]=7
  Depths in [2..7]: [2, 1, 2, 1, 0, 1]
  Minimum depth = 0 at index 6 -> node 0
  LCA = 0
```

### Why Does This Work?

Between visiting u for the first time and v for the first time, the DFS must **pass through their LCA**. The LCA is the shallowest point in that range because:
- DFS goes deeper into subtrees (away from LCA)
- The only way to get from u's subtree to v's subtree is to come back up through LCA

### Implementation

```python
import sys
sys.setrecursionlimit(200_000)

class SparseTable:
    """Range Minimum Query in O(1) with O(N log N) preprocessing."""
    def __init__(self, arr):
        n = len(arr)
        self.log = [0] * (n + 1)
        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1
        k = self.log[n] + 1
        self.table = [list(range(n)) for _ in range(k)]
        # table[j][i] = index of minimum in arr[i..i+2^j-1]
        self.arr = arr
        for j in range(1, k):
            for i in range(n - (1 << j) + 1):
                l = self.table[j - 1][i]
                r = self.table[j - 1][i + (1 << (j - 1))]
                self.table[j][i] = l if arr[l] <= arr[r] else r

    def query(self, l, r):
        """Index of minimum value in arr[l..r]."""
        j = self.log[r - l + 1]
        left = self.table[j][l]
        right = self.table[j][r - (1 << j) + 1]
        return left if self.arr[left] <= self.arr[right] else right


class LCA_EulerTour:
    def __init__(self, n, adj, root=0):
        self.n = n
        self.adj = adj
        self.depth = [0] * n
        self.euler = []       # euler tour sequence
        self.euler_depth = [] # depth at each position in tour
        self.first = [0] * n  # first occurrence of node in euler tour

        self._dfs(root, -1)
        self.sparse = SparseTable(self.euler_depth)

    def _dfs(self, node, par):
        self.first[node] = len(self.euler)
        self.euler.append(node)
        self.euler_depth.append(self.depth[node])

        for nb in self.adj[node]:
            if nb == par:
                continue
            self.depth[nb] = self.depth[node] + 1
            self._dfs(nb, node)
            # revisit current node after returning from child
            self.euler.append(node)
            self.euler_depth.append(self.depth[node])

    def lca(self, u, v):
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l, r = r, l
        idx = self.sparse.query(l, r)
        return self.euler[idx]
```

### Complexity

| | Time | Space |
|--|------|-------|
| Preprocess | O(N log N) --- Euler tour O(N) + sparse table O(N log N) | O(N log N) |
| Query | **O(1)** | --- |

**Verdict**: Fastest query time. Ideal when you have millions of queries and can afford the preprocessing.

---

## Technique 4: HLD-Based LCA

### Idea

If you already have HLD built, LCA falls out naturally --- it's what `query_path` does when climbing chains!

```python
def lca(self, u, v):
    while self.chain_head[u] != self.chain_head[v]:
        if self.depth[self.chain_head[u]] < self.depth[self.chain_head[v]]:
            u, v = v, u
        u = self.parent[self.chain_head[u]]

    # same chain -- shallower node is the LCA
    return u if self.depth[u] <= self.depth[v] else v
```

That's it --- the same chain-climbing loop, but instead of querying the segment tree, you just return the shallower node at the end.

### Complexity

| | Time | Space |
|--|------|-------|
| Preprocess | O(N) --- two DFS passes | O(N) |
| Query | **O(log N)** | --- |

**Verdict**: Free if you already have HLD. No extra data structures needed.

---

## Technique 5: Tarjan's Offline LCA

### Idea

If you have **all queries upfront** (offline), process them during a single DFS using **Union-Find (DSU)**.

```
After finishing a subtree, union it with its parent.
When both nodes of a query are visited, the answer is
the current "find" representative of one of them.
```

### Implementation

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1


def tarjan_lca(n, adj, root, queries):
    """
    queries: list of (u, v, query_index)
    Returns: list of LCA answers in query order
    """
    dsu = DSU(n)
    ancestor = list(range(n))  # ancestor[find(x)] = current LCA candidate
    visited = [False] * n
    answers = [0] * len(queries)

    # group queries by node
    query_map = [[] for _ in range(n)]
    for u, v, idx in queries:
        query_map[u].append((v, idx))
        query_map[v].append((u, idx))

    def dfs(node, par):
        visited[node] = True

        for nb in adj[node]:
            if nb == par:
                continue
            dfs(nb, node)
            dsu.union(node, nb)
            ancestor[dsu.find(node)] = node  # after union, node is the ancestor

        # check queries involving this node
        for other, idx in query_map[node]:
            if visited[other]:
                answers[idx] = ancestor[dsu.find(other)]

    dfs(root, -1)
    return answers
```

### How It Works --- Traced

```
Tree:        0
            / \
           1   2
          / \
         3   4

Query: LCA(3, 4)

DFS order: 0 -> 1 -> 3 (leaf, backtrack) -> 4 (leaf, backtrack) -> 1 done -> 2

After visiting 3:
  visited[3] = True
  union(1, 3), ancestor[find(1)] = 1

Visit 4:
  visited[4] = True
  Check query (3, 4): visited[3]? Yes!
    answer = ancestor[find(3)] = ancestor[find(1)] = 1
```

The key insight: when you visit node 4 and check node 3, the DSU has already merged 3 into 1's set (because we backtracked from 3). So `find(3)` leads to 1, which is exactly the LCA.

### Complexity

| | Time | Space |
|--|------|-------|
| Total | **O((N + Q) a(N))** ~ O(N + Q) | O(N + Q) |

**Verdict**: Optimal for offline. Nearly linear. But can't handle queries that arrive one at a time.

---

## All Techniques Compared

```
                    Preprocess    Query      Space      Online?   Extra DS
                    ----------    -----      -----      -------   --------
Brute Force         O(N)          O(N)       O(N)       Yes       None
Binary Lifting      O(N log N)    O(log N)   O(N log N) Yes       Lifting table
Euler + Sparse      O(N log N)    O(1)       O(N log N) Yes       Sparse table
HLD                 O(N)          O(log N)   O(N)       Yes       HLD arrays
Tarjan (offline)    O(N+Q)        O(1)*      O(N+Q)     No        DSU
```

*Tarjan's amortized over all queries

### Which to Pick?

```
                   +-- Yes --- Have all queries upfront?
                   |            |
                   |      +- Yes --> Tarjan's offline (fastest total)
                   |      +- No  --> continue below
                   |
Start -------------+
                   |
                   +-- Online queries needed
                         |
                   +-----+-----+
                   |           |
              Few queries?   Many queries?
              (Q < N)        (Q >> N)
                   |           |
                   v           v
             Binary Lifting   Euler + Sparse Table
             (simple, log N)  (O(1) per query)

              Already have HLD? --> Use HLD's LCA (it's free)
```

---

## LCA Variations & Applications

### Variation 1: Distance Between Nodes

```
dist(u, v) = depth[u] + depth[v] - 2 * depth[LCA(u, v)]

       0 (depth 0)
      / \
     1   2 (depth 1)
    / \
   3   4 (depth 2)

dist(3, 2):
  LCA(3,2) = 0
  dist = 2 + 1 - 2*0 = 3
  path: 3 -> 1 -> 0 -> 2 (3 edges)
```

### Variation 2: Kth Ancestor

*"What is the ancestor K steps above node u?"*

Binary lifting gives this directly:

```python
def kth_ancestor(self, u, k):
    for bit in range(LOG):
        if k & (1 << bit):
            u = self.up[bit][u]
            if u == -1:
                return -1
    return u
```

### Variation 3: Kth Node on Path

*"What is the Kth node on the path from u to v?"*

```python
def kth_on_path(self, u, v, k):
    lca = self.lca(u, v)
    dist_u = self.depth[u] - self.depth[lca]  # u to LCA
    dist_v = self.depth[v] - self.depth[lca]  # v to LCA

    if k <= dist_u:
        # on the u -> LCA side
        return self.kth_ancestor(u, k)
    else:
        # on the LCA -> v side
        return self.kth_ancestor(v, dist_u + dist_v - k)
```

```
Path: 6 -> 3 -> 1 -> 4,  k=2 (0-indexed)

dist_u (6->LCA=1) = 2
dist_v (4->LCA=1) = 1

k=2 <= dist_u=2 -> kth_ancestor(6, 2) = 1
k=3 > dist_u=2  -> kth_ancestor(4, 2+1-3) = kth_ancestor(4, 0) = 4
```

### Variation 4: Path Max/Min/Sum

*"What is the maximum edge weight on the path from u to v?"*

Split at LCA and query each half:

```
Path u -> v splits into:  u -> LCA -> v

max_on_path(u, v) = max(
    max_on_path(u, LCA),   // climbing from u to LCA
    max_on_path(v, LCA)    // climbing from v to LCA
)
```

With **binary lifting**, store max weight for each power-of-2 jump:

```python
# max_edge[k][node] = max edge weight in the 2^k steps above node
# built alongside up[k][node]
```

### Variation 5: LCA on Weighted Trees

Same algorithms work. Just store edge weights and combine them during lifting/tour.

### Variation 6: LCA of Multiple Nodes

*"LCA of nodes {a, b, c, d}?"*

Sort by Euler Tour `tin`, then LCA of the set = LCA of consecutive pairs:

```python
def lca_set(nodes):
    nodes.sort(key=lambda x: tin[x])
    result = nodes[0]
    for i in range(1, len(nodes)):
        result = lca(result, nodes[i])
    return result
```

### Variation 7: Virtual Tree (Auxiliary Tree)

When you have Q queries on specific nodes, build a **virtual tree** containing only the query nodes and their pairwise LCAs. Reduces an N-node tree to at most 2Q nodes.

---

## Quick Reference Table

| Problem | Technique | Complexity |
|---------|-----------|------------|
| LCA query (online, simple) | Binary Lifting | O(log N) |
| LCA query (online, fastest) | Euler Tour + Sparse Table | O(1) |
| LCA query (offline batch) | Tarjan's + DSU | O(N + Q) |
| Distance(u, v) | LCA + depth | O(LCA query) |
| Kth ancestor | Binary Lifting | O(log N) |
| Kth node on path | LCA + Kth ancestor | O(log N) |
| Path max/sum | Binary Lifting with weights | O(log N) |
| Path query with updates | HLD + Segment Tree | O(log^2 N) |
| LCA of K nodes | Sort by tin + pairwise LCA | O(K log N) |
