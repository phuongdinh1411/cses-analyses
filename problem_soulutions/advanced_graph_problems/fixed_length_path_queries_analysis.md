---
layout: simple
title: "Fixed-Length Paths - Advanced Graph Problem"
permalink: /problem_soulutions/advanced_graph_problems/fixed_length_path_queries_analysis
difficulty: Hard
tags: [centroid-decomposition, tree, divide-and-conquer, counting]
---

# Fixed-Length Paths

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Tree / Divide and Conquer |
| **Time Limit** | 1 second |
| **Key Technique** | Centroid Decomposition |
| **CSES Link** | [https://cses.fi/problemset/task/2080](https://cses.fi/problemset/task/2080) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement centroid decomposition on trees
- [ ] Count paths of specific lengths efficiently in trees
- [ ] Apply divide-and-conquer on tree structures
- [ ] Optimize path counting using subtree separation

---

## Problem Statement

**Problem:** Given a tree of n nodes, count the number of distinct paths that contain exactly k edges.

**Input:**
- Line 1: Two integers n and k (number of nodes, target path length)
- Lines 2 to n: Two integers a and b describing edges

**Output:**
- Single integer: the number of paths with exactly k edges

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= k <= n - 1
- The graph is a tree (connected, n-1 edges, no cycles)

### Example

```
Input:
5 2
1 2
2 3
3 4
3 5

Output:
4
```

**Explanation:** The tree looks like:
```
    1 - 2 - 3 - 4
            |
            5
```
Paths with exactly 2 edges: (1,2,3), (2,3,4), (2,3,5), (4,3,5) = 4 paths.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently count paths of a specific length in a tree?

A naive approach would check all pairs of nodes, but that is O(n^2). The key insight is that every path in a tree either passes through a "central" node or stays entirely within a subtree. This is the foundation of **centroid decomposition**.

### Breaking Down the Problem

1. **What are we looking for?** Paths with exactly k edges.
2. **What makes trees special?** There is exactly one path between any two nodes.
3. **How can we divide the problem?** Split at the centroid and count paths that go through it.

### Analogies

Think of the centroid as the "capital city" of a country. Any long journey either passes through the capital or stays within one region. By removing the capital and recursively solving for each region, we efficiently cover all paths.

---

## Solution 1: Brute Force DFS

### Idea

For every pair of nodes, compute the path length using BFS/DFS and count pairs with distance k.

### Algorithm

1. For each node u, run BFS to find distances to all other nodes
2. Count pairs where distance equals k
3. Divide by 2 (each path counted twice)

### Code

```python
from collections import deque

def solve_brute_force(n, k, edges):
  """
  Brute force: BFS from each node.
  Time: O(n^2)
  Space: O(n)
  """
  adj = [[] for _ in range(n + 1)]
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
          if dist[v] == k:
            count += 1
          if dist[v] < k:
            queue.append(v)

  return count // 2
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | BFS from each of n nodes |
| Space | O(n) | Distance array and queue |

### Why This Works (But Is Slow)

Correctness is guaranteed because we enumerate all pairs. However, for n = 2*10^5, O(n^2) is too slow (4*10^10 operations).

---

## Solution 2: Centroid Decomposition (Optimal)

### Key Insight

> **The Trick:** Decompose the tree by repeatedly finding and removing centroids. For each centroid, count paths passing through it by combining depths from different subtrees.

### What is a Centroid?

A **centroid** of a tree is a node whose removal results in no subtree having more than n/2 nodes. Every tree has at least one centroid.

### Algorithm Overview

1. Find the centroid of the current tree
2. Count all paths of length k that pass through the centroid
3. Remove the centroid and recursively solve for each subtree
4. Sum all counts

### Counting Paths Through Centroid

For paths passing through centroid c:
- Compute depth of each node from c
- A path of length k consists of two segments: depth d1 from one subtree and depth d2 from another, where d1 + d2 = k
- Use a count array to track how many nodes are at each depth
- Process subtrees one by one, combining with previously seen depths

### Dry Run Example

```
Tree:       1 - 2 - 3 - 4
                    |
                    5
Target k = 2

Step 1: Find centroid
  Sizes: node 3 has subtrees of size 2, 1, 1
  Centroid = 3 (removing it gives subtrees <= n/2)

Step 2: Count paths through centroid 3
  Subtree 1 (via edge 3-2): depths = {1: node 2, 2: node 1}
  Subtree 2 (via edge 3-4): depths = {1: node 4}
  Subtree 3 (via edge 3-5): depths = {1: node 5}

  Process Subtree 1:
    cnt = [1,0,0,...] (only centroid at depth 0)
    Nodes at depth 1: need depth k-1=1 in cnt -> cnt[1]=0
    Nodes at depth 2: need depth k-2=0 in cnt -> cnt[0]=1 -> count += 1
    Update cnt: cnt[1]+=1, cnt[2]+=1 -> cnt = [1,1,1,...]

  Process Subtree 2:
    Nodes at depth 1: need depth 1 in cnt -> cnt[1]=1 -> count += 1
    Update cnt: cnt[1]+=1 -> cnt = [1,2,1,...]

  Process Subtree 3:
    Nodes at depth 1: need depth 1 in cnt -> cnt[1]=2 -> count += 2

  Paths through centroid 3: 1 + 1 + 2 = 4

Step 3: Remove centroid 3, recurse on subtrees
  Subtrees {1,2}, {4}, {5} have no paths of length 2

Total: 4 paths
```

### Visual Diagram

```
Original Tree:
    1 - 2 - 3 - 4       Centroid = 3
            |
            5

Paths of length 2 through centroid 3:
  1 -- 2 -- [3]           depth 2 + depth 0 = 2  (node 1 to centroid)
  [3] -- 2 -- 1           Same path

  2 -- [3] -- 4           depth 1 + depth 1 = 2
  2 -- [3] -- 5           depth 1 + depth 1 = 2
  4 -- [3] -- 5           depth 1 + depth 1 = 2

Wait, let's recount properly:
  Path (1,2,3): uses 2 edges  -> depth of 1 from centroid = 2, depth of 3 = 0
  But we want paths, not just to centroid.

  Paths passing through 3:
    1-2-3-4: length 3 (no)
    1-2-3-5: length 3 (no)
    1-2-3: length 2 (yes) - but this ends at centroid
    2-3-4: length 2 (yes)
    2-3-5: length 2 (yes)
    4-3-5: length 2 (yes)

Correct count: 4 paths of length 2
```

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve(n, k, edges):
  """
  Centroid decomposition solution.
  Time: O(n log n)
  Space: O(n)
  """
  adj = [[] for _ in range(n + 1)]
  for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)

  removed = [False] * (n + 1)
  subtree_size = [0] * (n + 1)
  result = 0

  def get_subtree_size(u, parent):
    subtree_size[u] = 1
    for v in adj[u]:
      if v != parent and not removed[v]:
        get_subtree_size(v, u)
        subtree_size[u] += subtree_size[v]

  def get_centroid(u, parent, tree_size):
    for v in adj[u]:
      if v != parent and not removed[v]:
        if subtree_size[v] > tree_size // 2:
          return get_centroid(v, u, tree_size)
    return u

  def get_depths(u, parent, depth, depths):
    if depth > k:
      return
    depths.append(depth)
    for v in adj[u]:
      if v != parent and not removed[v]:
        get_depths(v, u, depth + 1, depths)

  def count_paths(centroid):
    nonlocal result
    cnt = [0] * (k + 2)
    cnt[0] = 1  # centroid itself at depth 0

    for neighbor in adj[centroid]:
      if removed[neighbor]:
        continue

      depths = []
      get_depths(neighbor, centroid, 1, depths)

      # Count paths combining this subtree with previous subtrees
      for d in depths:
        if k - d >= 0 and k - d <= k:
          result += cnt[k - d]

      # Add depths from this subtree to cnt
      for d in depths:
        if d <= k:
          cnt[d] += 1

  def decompose(u):
    get_subtree_size(u, -1)
    centroid = get_centroid(u, -1, subtree_size[u])
    removed[centroid] = True

    count_paths(centroid)

    for v in adj[centroid]:
      if not removed[v]:
        decompose(v)

  decompose(1)
  return result

# Read input
def main():
  input_data = sys.stdin.read().split()
  idx = 0
  n, k = int(input_data[idx]), int(input_data[idx + 1])
  idx += 2
  edges = []
  for _ in range(n - 1):
    a, b = int(input_data[idx]), int(input_data[idx + 1])
    edges.append((a, b))
    idx += 2
  print(solve(n, k, edges))

if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Each node processed O(log n) times across decomposition levels |
| Space | O(n) | Adjacency list, arrays, recursion stack |

---

## Common Mistakes

### Mistake 1: Not Handling Removed Nodes

**Problem:** After removing a centroid, we must skip it in future traversals.
**Fix:** Always check `!removed[v]` when traversing neighbors.

### Mistake 2: Counting Paths Within Same Subtree

**Problem:** This counts paths where both endpoints are in the same subtree (not passing through centroid).
**Fix:** Count matches first, then add to the frequency array.

### Mistake 3: Off-by-One in Depth Limit

**Problem:** Collecting depths greater than k wastes time and memory.
**Fix:** Return early if `depth > k`.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| k = 1 | Tree with any edges | Number of edges | Every edge is a path of length 1 |
| Linear tree | 1-2-3-...-n, k=n-1 | 1 | Only one path of maximum length |
| Star graph | Center connected to n-1 leaves, k=2 | C(n-1, 2) | All pairs of leaves |
| k > n-1 | Any tree | 0 | No path can have more than n-1 edges |
| Single node | n=1, k=1 | 0 | No edges exist |

---

## When to Use This Pattern

### Use Centroid Decomposition When:
- Counting or finding paths in a tree with specific properties
- Querying distances between pairs of nodes
- Problems involving "paths passing through" a node
- Need O(n log n) or O(n log^2 n) solution on trees

### Do Not Use When:
- The graph is not a tree (has cycles)
- Simple BFS/DFS suffices (single source queries)
- Problem requires path reconstruction (not just counting)

### Pattern Recognition Checklist:
- [ ] Is the graph a tree? -> **Consider centroid decomposition**
- [ ] Counting paths with specific length/property? -> **Centroid decomposition**
- [ ] Need to combine information from different subtrees? -> **Centroid decomposition**
- [ ] O(n^2) is too slow but tree structure exists? -> **Centroid decomposition**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Basic tree traversal and distances |
| [Tree Diameter](https://cses.fi/problemset/task/1131) | Finding longest path in tree |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Fixed-Length Paths II](https://cses.fi/problemset/task/2081) | Count paths with length in range [k1, k2] |
| [Tree Distances II](https://cses.fi/problemset/task/1133) | Sum of distances, different technique |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Path Queries II](https://cses.fi/problemset/task/2134) | HLD with segment tree |
| [Centroid decomposition with updates](https://codeforces.com/problemset/problem/342/E) | Dynamic centroid queries |

---

## Key Takeaways

1. **The Core Idea:** Decompose tree by centroids; count paths passing through each centroid by combining depths from different subtrees.
2. **Time Optimization:** From O(n^2) brute force to O(n log n) by exploiting tree structure.
3. **Space Trade-off:** O(n) space for tracking depths and counts.
4. **Pattern:** Divide-and-conquer on trees using centroid decomposition.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Find the centroid of a tree in O(n) time
- [ ] Explain why each node is processed O(log n) times total
- [ ] Implement centroid decomposition without looking at the solution
- [ ] Apply this technique to count paths with other properties

---

## Additional Resources

- [CP-Algorithms: Centroid Decomposition](https://cp-algorithms.com/graph/centroid-decomposition.html)
- [USACO Guide: Centroid Decomposition](https://usaco.guide/plat/centroid)
- [Codeforces Tutorial](https://codeforces.com/blog/entry/81661)
