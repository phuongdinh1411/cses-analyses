---
layout: simple
title: "Edge Contribution & Rerooting — Tree Distance Patterns"
permalink: /pattern/edge-contribution
---

# Edge Contribution & Rerooting — Tree Distance Patterns

A comprehensive walkthrough of the edge contribution technique and rerooting DP, from the core insight to 5 LeetCode problems that use it.

---

## Pattern Overview

**Trigger**: "Sum of distances / costs between pairs in a tree"

All problems share:
- **Edge-centric thinking**: don't iterate over pairs, iterate over edges
- **Subtree sizes via DFS**: one post-order DFS gives `sub[v]` for every node
- **Rerooting** (optional): compute answer for root, then derive all others in O(1) per edge

Three main flavors:

```
Edge Contribution            Rerooting DP               Edge Contribution + Groups
(single aggregate)           (per-node answer)           (grouped pairs)

answer = Σ f(sub[v])         answer[v] = adjust(u→v)    answer = Σ_g left[g]×right[g]

979 Coins                    834 Sum of Distances        Same-Color Distances
2049 Highest Score           2858 Edge Reversals
```

---

## Table of Contents

1. [Core Insight: Think Per Edge, Not Per Pair](#1-core-insight-think-per-edge-not-per-pair)
2. [The Bridge Analogy](#2-the-bridge-analogy)
3. [Computing Subtree Sizes](#3-computing-subtree-sizes)
4. [Rerooting Template](#4-rerooting-template)
5. [Problem 834 — Sum of Distances in Tree](#5-problem-834--sum-of-distances-in-tree)
6. [Problem 979 — Distribute Coins in Binary Tree](#6-problem-979--distribute-coins-in-binary-tree)
7. [Problem 2049 — Count Nodes With the Highest Score](#7-problem-2049--count-nodes-with-the-highest-score)
8. [Problem 2858 — Minimum Edge Reversals](#8-problem-2858--minimum-edge-reversals)
9. [Grouped Edge Contribution — Same-Color Distances](#9-grouped-edge-contribution--same-color-distances)
10. [Master Comparison Table](#10-master-comparison-table)
11. [How to Identify This Pattern](#11-how-to-identify-this-pattern)

---

## 1. Core Insight: Think Per Edge, Not Per Pair

The naive way to compute "sum of distances between all pairs" is O(n²) — BFS from every node. The edge contribution technique does it in O(n).

### The key mental flip

Instead of asking **"for each pair, what is their distance?"**, ask **"for each edge, how many pairs cross it?"**

```
Sum of distances = Σ         dist(u, v)
                  (u,v) pairs

                = Σ         (number of edges on path u→v)
                  (u,v)

Swap summation order:

                = Σ         (number of pairs whose path crosses this edge)
                  edges e
```

Every edge in a tree is a **bridge** — removing it splits the tree into exactly two parts. A pair crosses an edge if and only if the two nodes are in different parts.

---

## 2. The Bridge Analogy

```
         0(A)
        / \
      1(A)  2(B)        Each edge is a toll bridge.
      / \     \         Every pair on opposite sides
    3(B) 4(A)  5(B)     must pay $1 to cross.
```

Cut edge 0-1:

```
Left:  {1, 3, 4}    3 nodes
Right: {0, 2, 5}    3 nodes

ALL-pairs crossing:  3 × 3 = 9 pairs
Same-group pairs:
  Group A: 2 left × 1 right = 2
  Group B: 1 left × 2 right = 2
```

The bridge's contribution depends on what you're counting (all pairs, same-group pairs, coin flow, etc.).

---

## 3. Computing Subtree Sizes

The foundation of every problem in this family: root the tree, compute subtree sizes bottom-up.

```python
adj = [[] for _ in range(n)]
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)

sub = [1] * n  # each node counts as 1

def dfs(u, parent):
    for v in adj[u]:
        if v == parent:
            continue
        dfs(v, u)
        sub[u] += sub[v]

dfs(0, -1)
```

After this DFS:
- `sub[v]` = number of nodes in v's subtree (including v)
- Removing edge (parent, v) splits tree into `sub[v]` and `n - sub[v]`

```
       0
      /|\
     1 2 3        sub = [6, 1, 3, 1, 2, 1]
       |
       4          Removing edge 0-2:
       |            Left  = {2, 4, 5} → sub[2] = 3
       5            Right = {0, 1, 3} → n - sub[2] = 3
```

---

## 4. Rerooting Template

When you need `answer[i]` for **every** node as root:

```
Pass 1 (bottom-up): compute answer[root] using edge contribution
Pass 2 (top-down):  for each edge (u → child v), derive answer[v] from answer[u]
```

```python
# Pass 1: compute answer[0]
def dfs1(u, parent):
    for v in adj[u]:
        if v == parent:
            continue
        dfs1(v, u)
        sub[u] += sub[v]
        answer[0] += contribution(v)  # problem-specific

dfs1(0, -1)

# Pass 2: reroot
def dfs2(u, parent):
    for v in adj[u]:
        if v == parent:
            continue
        answer[v] = adjust(answer[u], v)  # problem-specific
        dfs2(v, u)

dfs2(0, -1)
```

The only thing that changes between problems is `contribution()` and `adjust()`.

---

## 5. Problem 834 — Sum of Distances in Tree

**Difficulty**: Hard

> Return array where `answer[i]` = sum of distances from node i to all other nodes.

### Key Idea

**Pass 1**: `answer[0] = Σ sub[v]` for all non-root v. Each node in v's subtree crosses edge (parent, v) to reach root 0, adding 1 to distance.

```
       0           answer[0] = sub[1] + sub[2] + sub[3] + sub[4] + sub[5]
      /|\                    = 1 + 3 + 1 + 2 + 1 = 8
     1 2 3
       |           Each node contributes 1 per edge on its path to root
       4           = its depth. So Σ sub[v] = Σ depth(node).
       |
       5
```

**Pass 2**: Moving root from u to child v:

```
Nodes in sub[v]:     distance decreases by 1 → subtract sub[v]
Nodes NOT in sub[v]: distance increases by 1 → add (n - sub[v])

answer[v] = answer[u] - sub[v] + (n - sub[v])
```

### Solution

```python
class Solution:
    def sumOfDistancesInTree(self, n: int, edges: list[list[int]]) -> list[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        sub = [1] * n
        answer = [0] * n

        # Pass 1: root at 0
        def dfs1(u, parent):
            for v in adj[u]:
                if v == parent:
                    continue
                dfs1(v, u)
                sub[u] += sub[v]
                answer[0] += sub[v]

        dfs1(0, -1)

        # Pass 2: reroot
        def dfs2(u, parent):
            for v in adj[u]:
                if v == parent:
                    continue
                answer[v] = answer[u] - sub[v] + (n - sub[v])
                dfs2(v, u)

        dfs2(0, -1)

        return answer
```

### Trace

```
       0
      /|\
     1 2 3
       |
       4
       |
       5

Pass 1: sub = [6, 1, 3, 1, 2, 1], answer[0] = 8

Pass 2:
  answer[1] = 8 - 1 + 5 = 12
  answer[2] = 8 - 3 + 3 = 8
  answer[3] = 8 - 1 + 5 = 12
  answer[4] = 8 - 2 + 4 = 10   (from node 2)
  answer[5] = 10 - 1 + 5 = 14  (from node 4)

answer = [8, 12, 8, 12, 10, 14]
```

**Complexity**: O(n) time, O(n) space

---

## 6. Problem 979 — Distribute Coins in Binary Tree

**Difficulty**: Medium

> Binary tree, each node has some coins, total = n. Move coins so each node has exactly 1. Minimize total moves (1 move = 1 coin across 1 edge).

### Key Idea

For each edge, compute **excess** of the child's subtree:

```
excess = (coins in subtree) - (nodes in subtree)

excess > 0 → subtree has extra, must export
excess < 0 → subtree needs coins, must import
excess = 0 → self-sufficient
```

Moves across edge = `|excess|`. Because the tree has only **one** edge connecting each subtree to the rest, all surplus/deficit must flow through it.

```
       0(0)           Node 1: excess = 3-1 = +2 (2 extra)
      / \             Node 2: excess = 0-1 = -1 (needs 1)
    1(3)  2(0)
                      Edge 0-1: |+2| = 2 moves
                      Edge 0-2: |-1| = 1 move
                      Total = 3
```

### Solution

```python
class Solution:
    def distributeCoins(self, root: TreeNode) -> int:
        self.moves = 0

        def dfs(node):
            if not node:
                return 0

            left_excess = dfs(node.left)
            right_excess = dfs(node.right)

            self.moves += abs(left_excess)
            self.moves += abs(right_excess)

            return node.val + left_excess + right_excess - 1

        dfs(root)
        return self.moves
```

### Why `return node.val + left_excess + right_excess - 1`

```
excess of subtree = (coins in subtree) - (nodes in subtree)

For a leaf:       val - 1
For internal:     val + left_coins + right_coins - (1 + left_nodes + right_nodes)
                = val - 1 + (left_coins - left_nodes) + (right_coins - right_nodes)
                = val - 1 + left_excess + right_excess
```

No need to track coins and nodes separately — just propagate excess.

**Complexity**: O(n) time, O(h) space (h = tree height)

---

## 7. Problem 2049 — Count Nodes With the Highest Score

**Difficulty**: Medium

> Binary tree given as parents[]. Remove node v → tree splits into up to 3 parts. Score = product of part sizes. Count how many nodes achieve the max score.

### Key Idea

Removing node v creates:

```
Part 1: left subtree   → sub[left_child]     (0 if no left child)
Part 2: right subtree  → sub[right_child]    (0 if no right child)
Part 3: everything else → n - sub[v]          (0 if v is root)

Score = product of non-zero parts
```

One DFS for `sub[]`, then O(1) per node to compute score.

### Solution

```python
class Solution:
    def countHighestScoreNodes(self, parents: list[int]) -> int:
        n = len(parents)

        children = [[] for _ in range(n)]
        for i in range(1, n):
            children[parents[i]].append(i)

        sub = [1] * n

        def dfs(u):
            for v in children[u]:
                dfs(v)
                sub[u] += sub[v]

        dfs(0)

        max_score = 0
        count = 0

        for v in range(n):
            score = 1
            for c in children[v]:
                score *= sub[c]
            rest = n - sub[v]
            if rest > 0:
                score *= rest

            if score > max_score:
                max_score = score
                count = 1
            elif score == max_score:
                count += 1

        return count
```

### Trace

```
       0
      / \
     1   2       sub = [5, 3, 1, 1, 1]
    / \
   3   4

Scores:
  Node 0: sub[1]×sub[2]     = 3×1     = 3   (root, no "rest")
  Node 1: sub[3]×sub[4]×rest = 1×1×2  = 2
  Node 2: rest               = 4       = 4
  Node 3: rest               = 4       = 4
  Node 4: rest               = 4       = 4

Max = 4, count = 3
```

**Complexity**: O(n) time, O(n) space

---

## 8. Problem 2858 — Minimum Edge Reversals

**Difficulty**: Hard

> Directed tree. For each node i, find minimum edge reversals so every node can reach i.

### Key Idea

**Pass 1**: Root at 0. For each directed edge, if it points **away** from root → must reverse (cost 1). If it points **toward** root → already correct (cost 0).

**Pass 2**: Reroot. Moving root from u to child v, only the edge between them flips:

```
Edge pointed toward u (cost 0 for u) → now points away from v (cost 1 for v)
Edge pointed away from u (cost 1 for u) → now points toward v (cost 0 for v)

answer[v] = answer[u] - 2w + 1

  w=0 (was good for u): answer[v] = answer[u] + 1  (lost a good edge)
  w=1 (was bad for u):  answer[v] = answer[u] - 1  (gained a good edge)
```

### Building the adjacency list

```python
for u, v in edges:
    adj[u].append((v, 1))   # original u→v: if v is child, wrong direction → cost 1
    adj[v].append((u, 0))   # reverse v→u: if u is child, right direction → cost 0
```

The weight means: "if I traverse this direction (parent → child), how much does this edge cost?"

### Solution

```python
class Solution:
    def minEdgeReversals(self, n: int, edges: list[list[int]]) -> list[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append((v, 1))
            adj[v].append((u, 0))

        answer = [0] * n

        # Pass 1: root at 0
        def dfs1(u, parent):
            for v, w in adj[u]:
                if v == parent:
                    continue
                answer[0] += w
                dfs1(v, u)

        dfs1(0, -1)

        # Pass 2: reroot
        def dfs2(u, parent):
            for v, w in adj[u]:
                if v == parent:
                    continue
                answer[v] = answer[u] - 2 * w + 1
                dfs2(v, u)

        dfs2(0, -1)

        return answer
```

### Trace

```
Directed: 2→0, 2→1, 1→3

Rooted at 0:
       0
       |  w=0  (edge 2→0 points toward root)
       2
       |  w=1  (edge 2→1 points away from root)
       1
       |  w=1  (edge 1→3 points away from root)
       3

Pass 1: answer[0] = 0 + 1 + 1 = 2

Pass 2:
  answer[2] = 2 - 2(0) + 1 = 3
  answer[1] = 3 - 2(1) + 1 = 2
  answer[3] = 2 - 2(1) + 1 = 1

answer = [2, 2, 3, 1]
```

**Complexity**: O(n) time, O(n) space

---

## 9. Grouped Edge Contribution — Same-Color Distances

> Tree with colored nodes. Find total distance between all same-color pairs.

### Key Idea

For each edge (parent → child v), the edge splits the tree. For each color g:

```
left  = sub[v][g]           (nodes of color g in v's subtree)
right = total[g] - sub[v][g] (nodes of color g elsewhere)

contribution = left × right
```

### Solution

```python
def sumOfGroupDistances(n, edges, groups):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    total = defaultdict(int)
    for g in groups:
        total[g] += 1

    sub = [None] * n
    answer = 0

    def dfs(u, parent):
        nonlocal answer
        sub[u] = defaultdict(int)
        sub[u][groups[u]] = 1

        for v in adj[u]:
            if v == parent:
                continue
            dfs(v, u)

            for g, cnt in sub[v].items():
                answer += cnt * (total[g] - cnt)

            for g, cnt in sub[v].items():
                sub[u][g] += cnt

    dfs(0, -1)
    return answer
```

### Why no double counting

Each edge is processed exactly once. A pair that crosses 4 edges gets counted once at each of those 4 edges, contributing 4 total — which equals its distance.

```
Pair (3, 5), distance = 4:
  Counted at edge 1→3: +1
  Counted at edge 0→1: +1
  Counted at edge 0→2: +1
  Counted at edge 2→5: +1
  Total contribution = 4 = dist(3, 5) ✓
```

**Complexity**: O(n × G) time where G = distinct groups, O(n × G) space

---

## 10. Master Comparison Table

| Problem | DFS Computes | Per-Edge Formula | Combine | Rerooting? | Time |
|---------|-------------|------------------|---------|------------|------|
| **834** Distances | `sub[v]` | `sub[v] × (n - sub[v])` | sum | Yes: `ans[v] = ans[u] - sub[v] + (n-sub[v])` | O(n) |
| **979** Coins | `excess[v]` | `\|excess[v]\|` | sum | No (single answer) | O(n) |
| **2049** Score | `sub[v]` | `Π(sub[child]) × (n-sub[v])` | product | No (compute per node) | O(n) |
| **2858** Reversals | `cost[v]` | `w` (0 or 1 per edge) | sum | Yes: `ans[v] = ans[u] - 2w + 1` | O(n) |
| **Grouped** | `sub[v][g]` | `sub[v][g] × (total[g]-sub[v][g])` | sum over g | No (single answer) | O(nG) |

### What stays the same

```
1. Root the tree
2. Post-order DFS to compute subtree info
3. Use subtree info to compute edge contributions
4. (Optional) Reroot to get per-node answers
```

### What changes

| | 834 | 979 | 2049 | 2858 | Grouped |
|---|---|---|---|---|---|
| **Subtree info** | size | excess | size | reversal cost | per-group count |
| **Edge formula** | L × R | \|excess\| | product of parts | 0 or 1 | L[g] × R[g] |
| **Reroot** | yes | no | no | yes | no |

---

## 11. How to Identify This Pattern

### Trigger: Tree + distances/costs between nodes

```
See "tree" + any of these?
  └── "sum of distances"         → Edge contribution + rerooting (834)
  └── "move items to balance"    → Edge contribution with excess (979)
  └── "remove node, split tree"  → Subtree sizes, compute per part (2049)
  └── "reverse edges to reach"   → Directed edge cost + rerooting (2858)
  └── "distance between groups"  → Grouped edge contribution
```

### The Universal Steps

```
1. Root the tree at any node

2. Post-order DFS to compute sub[v]
        │
        └── sub[v] = subtree size / excess / group counts / ...

3. For each edge (parent → child v):
        │
        └── contribution = f(sub[v], n - sub[v])
                           ──────   ──────────
                           v's side  other side

4. (If need per-node answer) Reroot:
        │
        └── answer[v] = adjust(answer[u], sub[v])
            Only the edge between u and v changes,
            everything else stays the same.
```

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Double counting worry | Not a bug — pair crossing k edges SHOULD contribute k (= its distance) |
| Forgetting to handle root in rerooting | Root has no parent edge; rest = 0 for root in score problems |
| Directed edges: wrong cost direction | `adj[u].append((v, 1))` and `adj[v].append((u, 0))` — cost is "if going parent→child" |
| Stack overflow on large trees | Use `sys.setrecursionlimit(n + 10)` or convert to iterative |
| Grouped: merging before counting | Always count edge contribution BEFORE merging child into parent |

---

## Practice Order

```
Start here
    │
    ▼
  834 (Hard)  ──── Core pattern: edge contribution + rerooting
    │
    ▼
  979 (Medium) ─── Edge contribution with "excess" flow
    │
    ▼
  2049 (Medium) ── Subtree sizes → per-node product
    │
    ▼
  2858 (Hard)  ─── Directed edges + rerooting with cost
    │
    ▼
  Grouped      ─── Per-group edge contribution with merge
  Distances
```

---

*Pattern mastered — same DFS backbone, different per-edge formulas and optional rerooting.*
