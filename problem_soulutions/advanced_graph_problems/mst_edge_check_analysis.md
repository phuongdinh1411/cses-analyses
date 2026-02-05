---
layout: simple
title: "New Roads Queries - MST Edge Check"
permalink: /problem_soulutions/advanced_graph_problems/mst_edge_check_analysis
difficulty: Hard
tags: [mst, kruskal, union-find, graph, lca]
prerequisites: [union-find, mst-basics, binary-lifting]
---

# New Roads Queries (MST Edge Check)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES - New Roads Queries](https://cses.fi/problemset/task/2101) |
| **Difficulty** | Hard |
| **Category** | Graph / MST |
| **Time Limit** | 1 second |
| **Key Technique** | Kruskal's + Union-Find / LCA on MST |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Determine if an edge belongs to some MST using the cycle property
- [ ] Apply Kruskal's algorithm with tie-breaking for edge classification
- [ ] Use LCA queries on the MST to check edge membership
- [ ] Understand the difference between "in some MST" vs "in all MSTs"

---

## Problem Statement

**Problem:** Given a weighted undirected graph, determine for each edge whether it can be part of some Minimum Spanning Tree.

**Input:**
- Line 1: `n m` - number of nodes and edges
- Next m lines: `a b w` - edge from a to b with weight w

**Output:**
- For each edge, output "YES" if it belongs to some MST, "NO" otherwise

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 * 10^5
- 1 <= w <= 10^9

### Example

```
Input:
4 5
1 2 1
2 3 2
3 4 3
4 1 4
2 4 2

Output:
YES
YES
YES
NO
YES
```

**Explanation:**
- Edge (1,2) weight 1: Always in MST (smallest edge)
- Edge (2,3) weight 2: In MST
- Edge (3,4) weight 3: In MST
- Edge (4,1) weight 4: Creates cycle with heavier weight, never in MST
- Edge (2,4) weight 2: Can be in MST (ties with edge 2-3)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When is an edge guaranteed to be in some MST?

An edge (u, v, w) is in **some** MST if and only if it is NOT the unique maximum weight edge in any cycle containing it.

### Breaking Down the Problem

1. **What are we looking for?** Whether each edge can appear in at least one MST
2. **What information do we have?** Complete graph with weighted edges
3. **What's the relationship?** Cycle property of MST - the maximum weight edge in a cycle is not in the MST (unless there are ties)

### The Two Key MST Properties

| Property | Statement | Use |
|----------|-----------|-----|
| **Cut Property** | Minimum weight edge crossing a cut is in some MST | Proves edge inclusion |
| **Cycle Property** | Maximum weight edge in a cycle is NOT in MST (if unique) | Proves edge exclusion |

### Analogies

Think of building a road network: you never need the longest road if there's already a path between two cities using shorter roads. But if two roads have the same length, either could be part of an optimal network.

---

## Solution 1: Kruskal's with Tie-Breaking

### Key Insight

> **The Trick:** Process edges by weight. For edges with the same weight, an edge is in some MST if it connects different components OR if there are ties that could include it.

### Algorithm

1. Sort edges by weight
2. Process edges in groups of same weight
3. For each weight group, mark edges that connect different components
4. Use Union-Find to track connectivity

### Dry Run Example

```
Graph: 1-2(1), 2-3(2), 3-4(3), 4-1(4), 2-4(2)

Initial: Each node is its own component
Components: {1}, {2}, {3}, {4}

Weight 1: Edge (1,2)
  - Connects components {1} and {2}
  - Mark as YES, merge: {1,2}, {3}, {4}

Weight 2: Edges (2,3) and (2,4)
  Process group together:
  - (2,3): Connects {1,2} and {3} -> YES
  - (2,4): Connects {1,2} and {4} -> YES
  - After merging: {1,2,3,4}

Weight 3: Edge (3,4)
  - Both in same component {1,2,3,4}
  - But could we have chosen different edges at weight 2?
  - Actually YES - if we took (2,4) instead of (2,3), we'd need (3,4)

Weight 4: Edge (4,1)
  - Both in same component, no ties available
  - Mark as NO
```

### Code

```python
import sys
from collections import defaultdict
input = sys.stdin.readline

class UnionFind:
 def __init__(self, n):
  self.parent = list(range(n))
  self.rank = [0] * n

 def find(self, x):
  if self.parent[x] != x:
   self.parent[x] = self.find(self.parent[x])
  return self.parent[x]

 def union(self, x, y):
  px, py = self.find(x), self.find(y)
  if px == py:
   return False
  if self.rank[px] < self.rank[py]:
   px, py = py, px
  self.parent[py] = px
  if self.rank[px] == self.rank[py]:
   self.rank[px] += 1
  return True

 def connected(self, x, y):
  return self.find(x) == self.find(y)

def solve():
 n, m = map(int, input().split())
 edges = []
 for i in range(m):
  a, b, w = map(int, input().split())
  edges.append((w, a - 1, b - 1, i))  # (weight, u, v, original_index)

 # Sort by weight
 edges.sort()

 result = ['NO'] * m
 uf = UnionFind(n)

 # Process edges in groups of same weight
 i = 0
 while i < m:
  j = i
  # Find all edges with same weight
  while j < m and edges[j][0] == edges[i][0]:
   j += 1

  # Check which edges in this group connect different components
  for k in range(i, j):
   w, u, v, idx = edges[k]
   if not uf.connected(u, v):
    result[idx] = 'YES'

  # Now union all edges in this weight group
  for k in range(i, j):
   w, u, v, idx = edges[k]
   uf.union(u, v)

  i = j

 print('\n'.join(result))

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(m log m) | Sorting edges dominates |
| Space | O(n + m) | Union-Find + edge storage |

---

## Solution 2: LCA-Based Approach (For Online Queries)

### Key Insight

> **The Trick:** Build one MST, then for each edge (u,v,w), check if w <= max edge weight on the path from u to v in the MST.

### Algorithm

1. Build MST using Kruskal's
2. Build tree structure with LCA preprocessing
3. For each non-MST edge (u,v,w):
   - Find max weight on path u->v in MST
   - Edge is in some MST if w <= max_weight (equality means ties)

### Code

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200005)
input = sys.stdin.readline

LOG = 18

def solve():
 n, m = map(int, input().split())
 edges = []
 for i in range(m):
  a, b, w = map(int, input().split())
  edges.append((w, a - 1, b - 1, i))

 # Build MST using Kruskal's
 parent = list(range(n))

 def find(x):
  if parent[x] != x:
   parent[x] = find(parent[x])
  return parent[x]

 def union(x, y):
  px, py = find(x), find(y)
  if px == py:
   return False
  parent[px] = py
  return True

 sorted_edges = sorted(edges)
 mst_adj = defaultdict(list)
 in_mst = set()

 for w, u, v, idx in sorted_edges:
  if union(u, v):
   mst_adj[u].append((v, w))
   mst_adj[v].append((u, w))
   in_mst.add(idx)

 # Build LCA structure with max edge tracking
 depth = [0] * n
 up = [[0] * n for _ in range(LOG)]
 max_edge = [[0] * n for _ in range(LOG)]  # max edge weight to 2^k ancestor

 def dfs(u, p, d, edge_w):
  depth[u] = d
  up[0][u] = p
  max_edge[0][u] = edge_w
  for k in range(1, LOG):
   up[k][u] = up[k-1][up[k-1][u]]
   max_edge[k][u] = max(max_edge[k-1][u], max_edge[k-1][up[k-1][u]])
  for v, w in mst_adj[u]:
   if v != p:
    dfs(v, u, d + 1, w)

 # Handle disconnected components
 for start in range(n):
  if depth[start] == 0 and (start == 0 or not mst_adj[start]):
   if mst_adj[start] or start == 0:
    dfs(start, start, 1, 0)

 def get_max_on_path(u, v):
  if depth[u] < depth[v]:
   u, v = v, u

  result = 0
  diff = depth[u] - depth[v]

  for k in range(LOG):
   if (diff >> k) & 1:
    result = max(result, max_edge[k][u])
    u = up[k][u]

  if u == v:
   return result

  for k in range(LOG - 1, -1, -1):
   if up[k][u] != up[k][v]:
    result = max(result, max_edge[k][u], max_edge[k][v])
    u, v = up[k][u], up[k][v]

  result = max(result, max_edge[0][u], max_edge[0][v])
  return result

 # Answer queries
 result = ['NO'] * m
 for w, u, v, idx in edges:
  if idx in in_mst:
   result[idx] = 'YES'
  elif depth[u] > 0 and depth[v] > 0:
   max_w = get_max_on_path(u, v)
   if w <= max_w:
    result[idx] = 'YES'

 print('\n'.join(result))

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(m log n) | MST + LCA preprocessing + queries |
| Space | O(n log n) | LCA table storage |

---

## Common Mistakes

### Mistake 1: Not Handling Tie-Breaking

```python
# WRONG - treats ties as "not in MST"
for w, u, v, idx in sorted_edges:
 if uf.union(u, v):
  result[idx] = 'YES'
 else:
  result[idx] = 'NO'  # Wrong! Edge might be in a different MST
```

**Problem:** When multiple edges have the same weight, any of them could be in some MST.
**Fix:** Process edges in weight groups and check connectivity before any unions in that group.

### Mistake 2: Checking After Union

```python
# WRONG - checks after modifying union-find
for k in range(i, j):
 w, u, v, idx = edges[k]
 uf.union(u, v)  # Modifies structure!
 if not uf.connected(u, v):  # Always false after union!
  result[idx] = 'YES'
```

**Problem:** Union modifies the structure before checking.
**Fix:** Check all edges first, then union all edges.

### Mistake 3: Off-by-One Indexing

```python
# WRONG - 0-indexed when problem uses 1-indexed
a, b, w = map(int, input().split())
edges.append((w, a, b, i))  # Should subtract 1 from a and b
```

---

## Edge Cases

| Case | Input Example | Expected | Why |
|------|---------------|----------|-----|
| Single edge | n=2, m=1, (1,2,5) | YES | Only edge, must be in MST |
| All same weight | All edges weight=1 | All YES | Any spanning tree is MST |
| Disconnected graph | Two components | Check per component | Each component has own MST |
| Self-loop | Edge (1,1,w) | NO | Self-loops never in spanning tree |
| Parallel edges | Multiple (1,2,w) | Lightest YES | Only minimum weight parallel edge |

---

## When to Use This Pattern

### Use Kruskal's + Tie-Breaking When:
- You need to check ALL edges at once
- Offline processing is acceptable
- Simple implementation preferred

### Use LCA-Based Approach When:
- Queries come online
- You already have the MST built
- Need to answer many queries efficiently

### Pattern Recognition Checklist:
- [ ] Checking edge membership in MST? -> **Consider both approaches**
- [ ] Need "in some MST" vs "in all MSTs"? -> **Tie-breaking distinguishes these**
- [ ] Online queries on tree paths? -> **LCA with max edge tracking**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Road Reparation](https://cses.fi/problemset/task/1675) | Basic MST with Kruskal's |
| [Building Roads](https://cses.fi/problemset/task/1666) | Union-Find basics |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Company Queries II](https://cses.fi/problemset/task/1688) | LCA queries on tree |
| [Distance Queries](https://cses.fi/problemset/task/1135) | Path queries with LCA |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Path Queries II](https://cses.fi/problemset/task/2134) | Heavy-light decomposition |
| [New Roads Queries](https://cses.fi/problemset/task/2101) | Time-based connectivity |

---

## Key Takeaways

1. **Core Idea:** An edge is in some MST if it's not the unique maximum in any cycle
2. **Tie-Breaking:** Edges with equal weight to a "needed" edge can also be in some MST
3. **Two Approaches:** Kruskal's with grouping (offline) or LCA on MST (online)
4. **Pattern:** MST edge membership = cycle property + handling ties

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement Kruskal's with proper tie-breaking
- [ ] Explain why tie-breaking is necessary
- [ ] Use LCA to query maximum edge on a path
- [ ] Distinguish "in some MST" from "in all MSTs"

---

## Additional Resources

- [CP-Algorithms: MST Kruskal](https://cp-algorithms.com/graph/mst_kruskal.html)
- [CP-Algorithms: LCA Binary Lifting](https://cp-algorithms.com/graph/lca_binary_lifting.html)
- [CSES Road Reparation](https://cses.fi/problemset/task/1675) - Basic MST problem
