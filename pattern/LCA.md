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

## Quick Navigation: I need to...

| I need to... | Technique | Jump to |
|--------------|-----------|---------|
| Find LCA in a **binary-tree-node** form, one query | Recursive "found below me?" | [Walkthrough — LC 236](#walkthrough--lc-236-lca-of-a-binary-tree) |
| Find LCA in a **BST**, exploit ordering | Walk down until values split | [Walkthrough — LC 235](#walkthrough--lc-235-lca-of-a-bst) |
| Answer **many** LCA queries on a big tree (online) | Binary Lifting | [Technique 2](#technique-2-binary-lifting) |
| Answer LCA in **O(1)** after preprocess | Euler Tour + Sparse Table | [Technique 3](#technique-3-euler-tour--sparse-table-rmq) |
| Answer **all** queries given upfront (offline) | Tarjan + DSU | [Technique 5](#technique-5-tarjans-offline-lca) |
| Get the **Kth ancestor** of a node | Binary Lifting table alone | [Walkthrough — LC 1483](#walkthrough--lc-1483-kth-ancestor-of-a-tree-node) |
| Get **directions** (L/R/U) between two tree nodes | Root-paths, strip common prefix | [Walkthrough — LC 2096](#walkthrough--lc-2096-step-by-step-directions) |
| LCA of the **deepest leaves** | One DFS returning (depth, node) | [Walkthrough — LC 1123](#walkthrough--lc-1123-lca-of-deepest-leaves) |
| Distance / Kth-on-path / path max | LCA + depth arithmetic | [Variations](#lca-variations--applications) |

---

## From-Scratch Idea: What Makes a Problem an LCA Problem

Every LCA problem is secretly the same question: **"where do two downward paths from the root first diverge?"** The LCA is the last node they share. Everything else — distance, path max, Kth-on-path, directions — is bookkeeping hung off that one meeting point.

### The Identify Test (two questions)

**Question 1 — is there a "meeting point of two nodes" somewhere?** Look for the words: *distance between two nodes*, *path from u to v*, *common ancestor*, *split a tree path*, *shared prefix of two root-paths*. If two tree nodes need to be related through their shared history, that shared history is the LCA.

**Question 2 — how is the tree handed to me, and how many queries?** This picks the *technique*, not whether it's LCA:

```
                     +-- binary TreeNode pointer, ONE query
                     |        |
                     |   +- it's a BST (ordered)? --> walk down until split   (LC 235)
                     |   +- plain binary tree?     --> recursive "found below me?" (LC 236)
                     |   +- want deepest-leaves / directions / path?
                     |             --> one tailored DFS (LC 1123 / 2096)
How is the tree ----+
given + #queries?    |
                     +-- adjacency list, MANY queries
                              |
                        +-----+------------------+
                        |                        |
                   online (arrive 1-by-1)   offline (all upfront)
                        |                        |
                  +-----+------+            Tarjan + DSU  (LC-rare, CP staple)
                  |            |
             Q moderate    Q >> N, need O(1)
             Binary        Euler Tour +
             Lifting       Sparse Table
             (LC 1483)     (CP)
```

`★ Insight ─────────────────────────────────────`
The single most useful triage question is **"pointer or adjacency list?"** LeetCode almost always hands you a `TreeNode` and asks *one* query — so the winning move is a clever O(N) DFS with **no preprocessing** (236, 235, 1123, 2096). Competitive programming hands you an adjacency list and *Q* queries — now preprocessing (binary lifting / Euler+sparse) amortizes and dominates. Reaching for binary lifting on a single-query `TreeNode` problem is over-engineering; reaching for recursion on 10⁵ queries is a TLE.
`─────────────────────────────────────────────────`

### The Mental Shift: What "Ancestor" Really Buys You

| Symptom in the problem | What the LCA gives you | The trick |
|------------------------|------------------------|-----------|
| "distance between u and v" | the turning point of the path | `depth[u]+depth[v]-2*depth[LCA]` |
| "path from u to v" (sum/max) | two straight climbs | split at LCA, climb each half |
| "Kth node on the path u→v" | which half k lands in | compare k to `depth[u]-depth[LCA]` |
| "directions u→v as L/R/U" | shared root-prefix length | `U`×(up-steps) then dest's suffix |
| "common ancestor of a whole set" | pairwise reduction | sort by tin, fold `lca` over the set |
| "deepest leaves' ancestor" | the fork above the tallest subtrees | DFS returns `(height, node)`; tie ⇒ this node |

### LeetCode ↔ Classic (CP) Translation

| LeetCode framing | Classic / CP name | Same underlying move |
|------------------|-------------------|----------------------|
| LC 236 LCA of Binary Tree | "LCA by DFS folding" | post-order returns "did I see u or v below?" |
| LC 235 LCA of a BST | "search-tree LCA" | ordering replaces the fold — one downward walk |
| LC 1483 Kth Ancestor | "binary lifting / pointer jumping" | jump by set bits of k in the `up[k][]` table |
| LC 2096 Directions | "root-to-node path + LCA" | strip common prefix = climb to LCA |
| LC 1123 Deepest-leaves LCA | "height-augmented DFS" | subtree-height DP with node carried up |
| CSES *Company Queries II* | "binary-lifting LCA" | exactly Technique 2 |
| CSES *Distance Queries* | "LCA + depth" | Variation 1 |

---

## Master LeetCode Comparison Table

| LC # | Problem | Technique | Difficulty | Tree given as | Core move |
|------|---------|-----------|------------|---------------|-----------|
| [235](#walkthrough--lc-235-lca-of-a-bst) | LCA of a BST | Ordered walk-down | Medium | `TreeNode` (BST) | go left/right until `u,v` straddle `root` |
| [236](#walkthrough--lc-236-lca-of-a-binary-tree) | LCA of a Binary Tree | Recursive fold | Medium | `TreeNode` | both sides return non-null ⇒ here is LCA |
| [1123](#walkthrough--lc-1123-lca-of-deepest-leaves) | LCA of Deepest Leaves | Height-augmented DFS | Medium | `TreeNode` | DFS returns `(height, lca)`; equal heights ⇒ node |
| [2096](#walkthrough--lc-2096-step-by-step-directions) | Directions Between Nodes | Root-paths + prefix strip | Medium | `TreeNode` | `U`×(len(pu)−common) + pv-suffix |
| [1483](#walkthrough--lc-1483-kth-ancestor-of-a-tree-node) | Kth Ancestor | Binary lifting (table only) | Hard | parent array | jump by set bits of `k` |
| [Technique 2](#technique-2-binary-lifting) | Company Queries II (CSES) | Binary lifting LCA | — | adjacency | equalize depth, climb both in powers of 2 |

Notice the split: the top four are single-DFS, **no table**; the bottom two build the `up[k][]` lifting table. Same problem family, two entirely different toolkits — chosen by *how the tree arrives*.

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

## The LeetCode World: Pointer-Form, One Query (No Preprocessing)

Before the heavy CP machinery, meet the four problems LeetCode actually asks. All hand you a `TreeNode` and ask **one** query, so the winning answer is a single O(N) DFS — no `up[][]` table, no sparse table. These four cover the entire "clever DFS" family.

### Walkthrough — LC 236 LCA of a Binary Tree

**This template solves: LC 236, and is the parent skeleton for 1123, 1644, 1650.**

> **Problem.** Given the root of a binary tree and two node values `p` and `q` (both guaranteed present), return their lowest common ancestor. Nodes are *not* ordered — no BST property to exploit.

The move: a post-order DFS that returns **"did I find p or q at/below me?"** — represented by returning the found node itself (or `None`).

```python
def lowestCommonAncestor(root, p, q):
    if not root or root.val == p or root.val == q:
        return root                       # base: I AM one of the targets (or dead end)
    left  = lowestCommonAncestor(root.left,  p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root                       # p on one side, q on the other -> I'm the LCA
    return left or right                  # both targets are down ONE side -> bubble it up
```

The one subtle line is `if root.val == p or q: return root` — if `q` sits *below* `p`, we return `p` the moment we hit it and never descend further; `p` correctly bubbles up as the answer.

```
Tree:            3
               /   \
              5     1
            /  \   / \
           6    2 0   8
               / \
              7   4

LCA(6, 4):
  dfs(3): left=dfs(5), right=dfs(1)
    dfs(5): left=dfs(6), right=dfs(2)
      dfs(6): val==6? yes (6 is a target)  -> return node 6
      dfs(2): left=dfs(7)->None, right=dfs(4)->node 4
              left(None) or right(4)       -> return node 4
      dfs(5): left=6, right=4  BOTH non-null -> return node 5   <-- LCA
    dfs(1): finds neither -> None
  dfs(3): left=5, right=None -> return 5
Answer: 5
```

`★ Insight ─────────────────────────────────────`
The return value carries two meanings at once: "the LCA if I found it" **or** "one of the targets, still looking for its partner." They never conflict because the instant *both* children return non-null, that node is the LCA and it returns itself — the search stops climbing with a real answer. This is why no visited-set or parent-pointer is needed: the call stack *is* the upward path, and the fold happens on the way back up. It's O(N) time, O(H) stack.
`─────────────────────────────────────────────────`

### Walkthrough — LC 235 LCA of a BST

**This template solves: LC 235, 1257 (as a subroutine), 270-style ordered searches.**

> **Problem.** Same as 236, but the tree is a **binary search tree** (left subtree < node < right subtree). Return the LCA of `p` and `q`.

The BST ordering kills the recursion entirely: the LCA is the *first* node where `p` and `q` fall on **opposite sides** (or where one equals the node). Just walk down.

```python
def lowestCommonAncestor(root, p, q):
    while root:
        if p < root.val and q < root.val:
            root = root.left            # both smaller -> LCA is left
        elif p > root.val and q > root.val:
            root = root.right           # both larger  -> LCA is right
        else:
            return root                 # they straddle root (or one == root) -> LCA
```

```
BST:             6
               /   \
              2     8
            /  \   / \
           0    4 7   9
              /  \
             3    5

LCA(2, 8): 2<6 and 8>6? straddle -> return 6
LCA(2, 4): 2<6 and 4<6 -> go left to 2; now p==root(2) -> return 2
LCA(3, 5): both <6 -> 2; both >2 -> 4; 3<4 and 5>4 straddle -> return 4
```

`★ Insight ─────────────────────────────────────`
The BST version is O(H) time and **O(1) space** — no stack, no recursion — because ordering replaces the "search both subtrees and fold" of LC 236 with a single deterministic turn at each node. The lesson generalizes: whenever a structure carries an *ordering invariant*, you can often trade a two-branch search for a one-branch walk. The straddle condition `not(both < ) and not(both > )` is the same "p and q first diverge here" idea 236 discovers by folding — the BST just lets you see the divergence directly.
`─────────────────────────────────────────────────`

### Walkthrough — LC 1123 LCA of Deepest Leaves

**This template solves: LC 1123, 865 (identical problem, different number).**

> **Problem.** Return the LCA of the tree's **deepest leaves**. If there's one deepest leaf, it's its own answer; if several, return the deepest node that is an ancestor of all of them.

Augment the DFS to return a **pair** `(height, lca_so_far)`. At each node, compare the two subtree heights: whichever is deeper owns the answer; on a **tie**, *this node* is the fork above both deepest sides — so it becomes the LCA.

```python
def lcaDeepestLeaves(root):
    def dfs(node):
        if not node:
            return (0, None)
        lh, ln = dfs(node.left)
        rh, rn = dfs(node.right)
        if lh == rh:
            return (lh + 1, node)       # tie: deepest leaves on BOTH sides -> node is their LCA
        return (lh + 1, ln) if lh > rh else (rh + 1, rn)   # deeper side carries its LCA up
    return dfs(root)[1]
```

```
Tree:            3
               /   \
              5     1
            /  \   / \
           6    2 0   8
               / \
              7   4          <- deepest leaves are 7 and 4 (depth 3)

dfs(7)=(1,7)  dfs(4)=(1,4)
dfs(2): lh==rh==1 (tie) -> (2, node 2)        <- fork above 7 and 4
dfs(6)=(1,6)
dfs(5): left=(1,6), right=(2,node2); right deeper -> (3, node 2)
dfs(1): children depth 1 each (tie) -> (2, node 1)
dfs(3): left=(3,node2), right=(2,node1); left deeper -> (3, node 2)
Answer: node 2
```

`★ Insight ─────────────────────────────────────`
This is LCA reframed as a **subtree-height DP**: the "two nodes" whose ancestor you want aren't given — they're implicitly *all the deepest leaves*, and the tie condition (`lh == rh`) is exactly "the deepest leaves live on both sides of me, so I'm their meeting point." Carrying `(height, node)` up in one pass is the same augment-the-recursion trick as tree-DP returning `(rob, skip)` pairs — the return type grows to hold both the measurement (height) and the answer (node), so a single post-order fold computes both.
`─────────────────────────────────────────────────`

### Walkthrough — LC 2096 Step-By-Step Directions

**This template solves: LC 2096, and the "path to node" subroutine reused across tree problems.**

> **Problem.** Given a binary tree with unique values and two values `startValue`, `destValue`, return the shortest path as a string of `'L'` (left child), `'R'` (right child), `'U'` (to parent). E.g. `"UURL"`.

Insight: the path from `start` to `dest` goes **up to their LCA, then down** to dest. So find each node's root-path as an L/R string, strip the common prefix (that prefix *is* the path to the LCA), replace start's remaining suffix with `'U'`s (climbing), and append dest's remaining suffix.

```python
def getDirections(root, startValue, destValue):
    def find(node, target, path):
        if not node: return False
        if node.val == target: return True
        path.append('L')
        if find(node.left, target, path): return True
        path[-1] = 'R'
        if find(node.right, target, path): return True
        path.pop()
        return False

    ps, pd = [], []
    find(root, startValue, ps)     # root -> start, as L/R
    find(root, destValue, pd)      # root -> dest,  as L/R
    i = 0
    while i < len(ps) and i < len(pd) and ps[i] == pd[i]:
        i += 1                     # skip shared prefix = path down to the LCA
    return 'U' * (len(ps) - i) + ''.join(pd[i:])
```

```
Tree:        5
           /   \
          1     2
        /      / \
       3      6   7

path(root->3) = "LL"      path(root->6) = "RL"
common prefix = ""  (they diverge at the root -> LCA is 5)
start suffix "LL" -> "UU"  (climb 3 up to 5)
dest  suffix "RL"          (descend 5 down to 6)
Answer: "UU" + "RL" = "UURL"
```

`★ Insight ─────────────────────────────────────`
"Directions between two nodes" is LCA in disguise: the **length of the shared prefix of the two root-paths equals the depth of the LCA**, and stripping it *is* finding the LCA without ever naming it. Every step of `start`'s path below the LCA becomes a `'U'` (you must climb it), and every step of `dest`'s path below the LCA is copied verbatim (you descend it). This "path = up to LCA, then down" decomposition is the same one behind distance (`Variation 1`) and path-sum queries — 2096 just asks for the moves instead of the count.
`─────────────────────────────────────────────────`

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

LOG = 20  # binary-lifting table depth: 2^20 > 10^6, so it covers N up to ~10^6

class BinaryLifting:
    def __init__(self, n, adj, root=0):
        self.n = n
        self.adj = adj
        self.depth = [0] * n
        self.up = [[-1] * n for _ in range(LOG)]  # up[k][node]

        self._dfs(root, -1)   # MUST run first: fills up[0] (parents) and depth[]
        self._build()         # then this fills up[1..LOG-1] FROM up[0]; order is not optional

    def _dfs(self, node, par):
        self.up[0][node] = par  # parent = 2^0 ancestor
        for nb in self.adj[node]:
            if nb == par:
                continue
            self.depth[nb] = self.depth[node] + 1
            self._dfs(nb, node)

    def _build(self):
        """Fill the binary lifting table bottom-up.

        Precondition: _dfs (or _dfs_iter) has already filled up[0][*] (parents)
        and depth[*]. This reads up[0] to derive every higher level, so calling
        it before the DFS produces an all -1 table.
        """
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

> **Recursion-depth caveat.** The `LOG = 20` table handles the *ancestor jumps*
> for N up to ~10⁶, but the recursive `_dfs` above does **not** — a skewed tree
> (a long path) has depth up to N, which overflows Python's C stack far below
> 10⁶ (and even the raised `setrecursionlimit`). For large or adversarial inputs
> convert `_dfs` to an explicit stack:
>
> ```python
> def _dfs_iter(self, root):
>     stack = [(root, -1)]
>     while stack:
>         node, par = stack.pop()
>         self.up[0][node] = par
>         for nb in self.adj[node]:
>             if nb != par:
>                 self.depth[nb] = self.depth[node] + 1
>                 stack.append((nb, node))
> ```

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

### Walkthrough — LC 1483 Kth Ancestor of a Tree Node

**This template solves: LC 1483 directly; the same `up[k][]` table then powers every LCA query above.**

> **Problem.** You're given `n` nodes labelled `0..n-1` and a `parent` array (`parent[i]` = parent of `i`, root's parent `= -1`). Implement `TreeAncestor(n, parent)` and `getKthAncestor(node, k)` returning the node `k` steps above `node`, or `-1` if it doesn't exist. Up to ~5×10⁴ queries.

This is binary lifting with the **LCA half deleted** — pure ancestor jumping. Build `up[k][v]` exactly as Technique 2 does, then `getKthAncestor` climbs by the set bits of `k`.

```python
LOG = 20   # 2^20 > 5*10^4 comfortably

class TreeAncestor:
    def __init__(self, n, parent):
        self.up = [[-1] * n for _ in range(LOG)]
        for v in range(n):
            self.up[0][v] = parent[v]            # 2^0 ancestor = direct parent
        for k in range(1, LOG):
            for v in range(n):
                mid = self.up[k - 1][v]
                self.up[k][v] = -1 if mid == -1 else self.up[k - 1][mid]

    def getKthAncestor(self, node, k):
        for b in range(LOG):
            if node == -1:
                return -1                        # fell off the root
            if k & (1 << b):
                node = self.up[b][node]
        return node
```

```
parent = [-1, 0, 0, 1, 1, 2, 2]

Tree:        0
           /   \
          1     2
         / \   / \
        3   4 5   6

up[0] (parent):   [-1, 0, 0, 1, 1, 2, 2]
up[1] (grandpa):  [-1,-1,-1, 0, 0, 0, 0]   (up[0][up[0][v]])

getKthAncestor(3, 1): k=1 = binary 1 -> bit0 set -> node = up[0][3] = 1   -> 1
getKthAncestor(5, 2): k=2 = binary 10 -> bit1 set -> node = up[1][5] = 0  -> 0
getKthAncestor(6, 3): k=3 = binary 11 -> bit0: up[0][6]=2; bit1: up[1][2]=-1 -> -1
```

`★ Insight ─────────────────────────────────────`
`k` steps up = the **binary decomposition of k**: 13 = 8+4+1, so climb `up[3]`, then `up[2]`, then `up[0]` — three table lookups instead of 13 parent hops. This is *exactly* step 1 of the LCA (`_lift` equalizes depth by the same set-bit climb); LC 1483 is that half in isolation, which is why mastering it hands you binary-lifting LCA almost for free. The `-1` guard inside the loop is the one correctness trap: once you fall off the root, every further jump must short-circuit or you index garbage.
`─────────────────────────────────────────────────`

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

`★ Insight ─────────────────────────────────────`
This is the great reduction: **LCA becomes Range-Minimum-Query on depths.** The Euler tour linearizes the tree so that "the fork between u and v" turns into "the shallowest entry between two array positions" — and RMQ is a solved, O(1)-query problem via sparse table. Whenever a tree question can be flattened by a tour (tin/tout, Euler), ask whether the tree operation becomes a *range* operation on the flat array; subtree-sum→range-sum and LCA→range-min are the two canonical wins.
`─────────────────────────────────────────────────`

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
        # Each row starts as the identity [0,1,...,n-1]. For j>0 the build loop
        # below only fills i in [0, n-2^j], so tail cells i > n-2^j keep this
        # stale value — but query() never reads them (its two windows are always
        # fully in-range), so they are harmless. (Init to [0]*n if it bothers you.)
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

`★ Insight ─────────────────────────────────────`
Tarjan flips the cost model: instead of *per-query* work, you pay **once** during a single DFS and every query is answered the instant its second endpoint is visited. The DSU represent­ative of an already-finished subtree *is* the ancestor where that subtree reattaches — so `find(other)` reads the LCA directly. The catch (and why it's offline-only): you must know all queries before the DFS, because each is answered opportunistically at the moment both endpoints happen to be seen. Trade online flexibility for near-linear O((N+Q)·α(N)) total.
`─────────────────────────────────────────────────`

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

---

## Common Pitfalls

| Pitfall | Why it bites | Fix |
|---------|--------------|-----|
| Confusing **depth** with **height** | Binary lifting climbs by `depth[u] - depth[v]`; height (distance to deepest leaf) is a different quantity and gives wrong jumps. | Root has depth 0, children depth+1. Only depth is used for equalizing. |
| Not equalizing depths before lifting both | Step 3 assumes `u` and `v` sit at the **same depth**; skip step 1 and the parallel climb compares mismatched levels. | Always bring the deeper node up first (`_lift(u, depth[u]-depth[v])`), then climb both. |
| Off-by-one in the `LOG` bound | `LOG` must satisfy `2^LOG > N` (or `>= max depth`). Too small and a far ancestor is unreachable; the highest jump silently caps out. | Pick `LOG = ceil(log2(N)) + 1`; here `LOG=20` covers N up to ~10⁶. |
| Building the table before the DFS | `_build` reads `up[0]` (parents); running it first yields an all `-1` table and every LCA returns garbage. | Run `_dfs`/`_dfs_iter` first, then `_build`. |
| 0- vs 1-indexed nodes | Mixing an input that is 1-indexed with a 0-indexed `up`/`depth` array reads the wrong rows or overruns by one. | Decide once; if input is 1-indexed either shift to 0 or size arrays `n+1`. |
| Not handling `u == v` or ancestor-of case | If `v` is already an ancestor of `u`, after step 1 `u == v` and step 3 must be skipped. | Return early: `if u == v: return u` before the parallel climb. |

---

## Practice Order

```
Start here
    │
    ▼
  236  (Easy)   ──── LCA of a Binary Tree: recursive "found u/v below me?" — no preprocessing
    │
    ▼
  235  (Easy)   ──── LCA of a BST: exploit ordering — walk down until u,v split
    │
    ▼
  build up[][] ──── Binary-lifting table: DFS for parent/depth, then double each level
    │
    ▼
  1483 (Hard*) ──── Kth Ancestor of a Tree Node: pure lifting, jump by set bits of k
    │              (*builds directly on the table above)
    ▼
  dist(u,v)    ──── Distance via LCA: depth[u]+depth[v]-2*depth[LCA]
    │
    ▼
  path queries (Hard) ── Path max/sum, updates: lift with weights, or HLD + segtree
```

---

## The LCA Toolbox at a Glance

```
Two nodes need relating through shared history?  -> it's LCA
   │
   ├─ Tree given as a TreeNode pointer, ONE query  (LeetCode default)
   │     │
   │     ├─ BST (ordered)?          -> walk down until they straddle      LC 235   O(H), O(1) space
   │     ├─ plain binary tree?      -> recursive fold "found below me?"   LC 236   O(N)
   │     ├─ deepest-leaves' LCA?    -> DFS returns (height, node), tie⇒node LC 1123
   │     └─ directions / Kth-on-path/ distance?
   │            -> root-paths, strip common prefix (= the LCA)            LC 2096
   │
   └─ Tree given as adjacency list, MANY queries    (competitive default)
         │
         ├─ Kth ancestor only?      -> build up[k][], jump by set bits     LC 1483
         ├─ online, Q moderate      -> Binary Lifting LCA                  Technique 2   O(log N)/q
         ├─ online, Q >> N, want O(1) -> Euler Tour + Sparse Table         Technique 3   O(1)/q
         ├─ all queries upfront     -> Tarjan + DSU                        Technique 5   O(N+Q)
         └─ already built HLD?       -> HLD's chain-climb IS the LCA        Technique 4   free
```

### THREE MOVES BEHIND EVERY LCA

1. **Equalize** — bring the deeper node up so both sit at the same depth (climb / lift / prefix-strip).
2. **Meet** — climb both together until they land on the same node (fold / walk / range-min / union).
3. **Reuse** — hang distance, path-sum/max, Kth-on-path, and directions off that single meeting point.

### LeetCode Practice Ladder (the walkthroughs)

```
235 (Med)  BST — ordered walk-down, O(1) space
236 (Med)  Binary tree — the recursive fold everyone must know
1123 (Med) Deepest leaves — augment the DFS to (height, node)
2096 (Med) Directions — LCA as shared-prefix stripping
1483 (Hard) Kth Ancestor — build the binary-lifting table
 ↓
Company Queries II / Distance Queries (CSES) — lifting LCA + depth arithmetic
```

*Pattern mastered — stop re-climbing the tree one step at a time; find the one node where two paths diverge and let distance, path, and directions fall out of it.*
