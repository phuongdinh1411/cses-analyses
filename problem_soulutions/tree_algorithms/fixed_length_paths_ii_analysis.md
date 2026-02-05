---
layout: simple
title: "Fixed Length Paths II - Tree Algorithm Problem"
permalink: /problem_soulutions/tree_algorithms/fixed_length_paths_ii_analysis
difficulty: Hard
tags: [centroid-decomposition, fenwick-tree, tree-algorithms, divide-and-conquer]
prerequisites: [tree_diameter, fixed_length_paths_i]
---

# Fixed Length Paths II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Centroid Decomposition + Fenwick Tree (BIT) |
| **CSES Link** | [https://cses.fi/problemset/task/2081](https://cses.fi/problemset/task/2081) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply centroid decomposition to efficiently process tree path queries
- [ ] Use Fenwick Tree (BIT) for range counting with efficient updates
- [ ] Combine divide-and-conquer with data structures for O(n log^2 n) complexity

---

## Problem Statement

**Problem:** Given a tree with n nodes, count the number of distinct paths with length in [k1, k2].

**Input:**
- Line 1: Three integers n, k1, k2
- Lines 2 to n: Two integers a, b (an edge)

**Output:**
- Number of paths with length in range [k1, k2]

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= k1 <= k2 <= n - 1

### Example

```
Input:
5 2 3
1 2
2 3
3 4
4 5

Output:
5
```

**Explanation:**

```
Tree: 1 --- 2 --- 3 --- 4 --- 5

Paths of length 2: (1,3), (2,4), (3,5) = 3 paths
Paths of length 3: (1,4), (2,5) = 2 paths
Total = 5
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count paths of varying lengths without checking all O(n^2) pairs?

**Centroid decomposition** allows divide-and-conquer on trees. Every path either passes through the centroid or lies entirely within a subtree after removing it.

### The Key Insight

1. Find centroid (node whose removal creates subtrees of size <= n/2)
2. Count all paths passing through this centroid using BIT for range queries
3. Remove centroid and recursively solve for each subtree

For paths in range [k1, k2]: when processing a node at depth d, the partner must be at depth in [k1-d, k2-d]. BIT enables O(log n) range queries.

---

## Solution 1: Brute Force

### Idea

For each pair of nodes, compute distance using BFS and count if in [k1, k2].

### Code

```python
def solve_brute_force(n, k1, k2, edges):
 """
 Time: O(n^2), Space: O(n)
 """
 from collections import defaultdict, deque

 adj = defaultdict(list)
 for a, b in edges:
  adj[a].append(b)
  adj[b].append(a)

 count = 0
 for start in range(1, n + 1):
  dist = [-1] * (n + 1)
  dist[start] = 0
  queue = deque([start])

  while queue:
   u = queue.popleft()
   for v in adj[u]:
    if dist[v] == -1:
     dist[v] = dist[u] + 1
     queue.append(v)
     if k1 <= dist[v] <= k2:
      count += 1

 return count // 2  # Each path counted twice
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | BFS from each node |
| Space | O(n) | Distance array and queue |

---

## Solution 2: Optimal (Centroid Decomposition + BIT)

### Key Insight

> **The Trick:** Use centroid decomposition to count each path exactly once when it passes through some centroid. Use BIT for O(log n) range queries.

### Dry Run Example

```
Input: n=5, k1=2, k2=3, tree: 1-2-3-4-5

Step 1: Find centroid = 3

Step 2: Process centroid 3
  Left subtree (via 2): depths = [1, 2]  (nodes 2, 1)
  Right subtree (via 4): depths = [1, 2] (nodes 4, 5)

  Add left depths to BIT, then query for right:
    d=1: query [1,2] -> 2 matches (pairs with depth 1,2)
    d=2: query [0,1] -> 1 match (pair with depth 1)
  Paths through centroid: 3

Step 3: Recurse - remaining subtrees have no paths in [2,3]

Total = 5 paths: (1,3), (2,4), (3,5) at length 2; (1,4), (2,5) at length 3
```

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve(n, k1, k2, edges):
 adj = [[] for _ in range(n + 1)]
 for a, b in edges:
  adj[a].append(b)
  adj[b].append(a)

 bit = [0] * (n + 2)

 def bit_update(i, delta):
  i += 1
  while i <= n + 1:
   bit[i] += delta
   i += i & (-i)

 def bit_query(i):
  if i < 0: return 0
  i = min(i + 1, n + 1)
  s = 0
  while i > 0:
   s += bit[i]
   i -= i & (-i)
  return s

 def bit_range(lo, hi):
  return 0 if lo > hi else bit_query(hi) - bit_query(lo - 1)

 removed = [False] * (n + 1)
 size = [0] * (n + 1)

 def get_size(u, p):
  size[u] = 1
  for v in adj[u]:
   if v != p and not removed[v]:
    get_size(v, u)
    size[u] += size[v]

 def get_centroid(u, p, tree_size):
  for v in adj[u]:
   if v != p and not removed[v] and size[v] > tree_size // 2:
    return get_centroid(v, u, tree_size)
  return u

 def get_depths(u, p, d, depths):
  if d > k2: return
  depths.append(d)
  for v in adj[u]:
   if v != p and not removed[v]:
    get_depths(v, u, d + 1, depths)

 result = 0

 def process(u):
  nonlocal result
  get_size(u, -1)
  c = get_centroid(u, -1, size[u])
  removed[c] = True

  max_d = 0
  for v in adj[c]:
   if removed[v]: continue
   depths = []
   get_depths(v, c, 1, depths)

   for d in depths:
    lo, hi = max(0, k1 - d), k2 - d
    if hi >= 0:
     result += bit_range(lo, hi)

   for d in depths:
    bit_update(d, 1)
    max_d = max(max_d, d)

  for d in range(max_d + 1):
   v = bit_range(d, d)
   if v > 0: bit_update(d, -v)

  for v in adj[c]:
   if not removed[v]:
    process(v)

 process(1)
 return result

def main():
 data = sys.stdin.read().split()
 n, k1, k2 = int(data[0]), int(data[1]), int(data[2])
 edges = [(int(data[3+2*i]), int(data[4+2*i])) for i in range(n-1)]
 print(solve(n, k1, k2, edges))

if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log^2 n) | O(log n) decomposition levels, O(log n) BIT ops per node |
| Space | O(n) | Adjacency list, BIT, recursion stack |

---

## Common Mistakes

### Mistake 1: Incorrect BIT Cleanup

```python
# WRONG - O(n) per centroid makes total O(n^2)
bit = [0] * (n + 2)
```

**Fix:** Only clear depths actually used.

### Mistake 2: Counting Intra-Subtree Paths

```python
# WRONG - counts paths within same subtree
all_depths = []
for v in adj[centroid]:
 get_depths(v, centroid, 1, all_depths)
# Then counting pairs in all_depths
```

**Fix:** Process subtrees sequentially, query BIT before adding new depths.

### Mistake 3: Missing Depth 0

**Problem:** Paths from node at depth d to centroid (depth 0) not counted.
**Fix:** Initialize BIT[0]=1 or handle separately when k1 <= d <= k2.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Single edge | n=2, k1=1, k2=1 | 1 | One path |
| Star graph | n=5, k1=2, k2=2 | 6 | C(4,2)=6 through center |
| k1 = k2 | n=5, k1=2, k2=2 | varies | Exact length only |
| Large k1 | n=5, k1=10, k2=10 | 0 | No path >= n |

---

## When to Use This Pattern

### Use Centroid Decomposition + BIT When:
- Counting/summing over all paths in a tree
- Path length constraints involve ranges
- Need better than O(n^2) complexity

### Pattern Recognition Checklist:
- [ ] Counting paths in tree? Consider centroid decomposition
- [ ] Range constraints on length? Add BIT/segment tree
- [ ] Combining subtree info? Process subtrees sequentially

---

## Related Problems

### Easier (Do First)

| Problem | Why It Helps |
|---------|--------------|
| [Fixed Length Paths I (CSES 2080)](https://cses.fi/problemset/task/2080) | Exact length k, simpler |
| [Tree Diameter (CSES 1131)](https://cses.fi/problemset/task/1131) | Basic tree traversal |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Path Queries II (CSES 2134)](https://cses.fi/problemset/task/2134) | Different operations |

### Harder (Do After)

| Problem | New Concept |
|---------|-------------|
| [Distance Queries (CSES 1135)](https://cses.fi/problemset/task/1135) | LCA + preprocessing |

---

## Key Takeaways

1. **Core Idea:** Centroid decomposition ensures every path passes through exactly one centroid
2. **Time Optimization:** O(n^2) to O(n log^2 n) via centroid decomposition + BIT
3. **Pattern:** Canonical template for "path counting in range" problems

---

## Additional Resources

- [CP-Algorithms: Centroid Decomposition](https://cp-algorithms.com/graph/centroid-decomposition.html)
- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
