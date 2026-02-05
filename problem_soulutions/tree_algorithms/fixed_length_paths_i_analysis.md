---
layout: simple
title: "Fixed Length Paths I - Tree Algorithm Problem"
permalink: /problem_soulutions/tree_algorithms/fixed_length_paths_i_analysis
difficulty: Hard
tags: [centroid-decomposition, tree, divide-and-conquer, path-counting]
prerequisites: [tree_diameter, tree_distances_i]
---

# Fixed Length Paths I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Centroid Decomposition |
| **CSES Link** | [Fixed Length Paths I](https://cses.fi/problemset/task/2080) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand centroid decomposition and its application to tree path problems
- [ ] Implement efficient O(n log n) path counting using divide-and-conquer
- [ ] Count paths passing through a specific node without double counting
- [ ] Apply the "count through centroid" technique to similar tree problems

---

## Problem Statement

**Problem:** Given a tree of n nodes, count the number of distinct paths that consist of exactly k edges.

**Input:**
- Line 1: Two integers n and k (number of nodes and target path length)
- Lines 2 to n: Two integers a and b describing an edge between nodes a and b

**Output:**
- A single integer: the number of paths with exactly k edges

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= k <= n - 1
- 1 <= a, b <= n

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

**Explanation:**

Tree structure:
```
    1
    |
    2
    |
    3
   / \
  4   5
```

Paths of exactly 2 edges:
1. 1 -> 2 -> 3
2. 2 -> 3 -> 4
3. 2 -> 3 -> 5
4. 4 -> 3 -> 5

Total: 4 paths

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently count all paths of length k in a tree?

The naive approach of checking all O(n^2) pairs is too slow. The key insight is that every path in a tree either:
1. Lies entirely within a subtree, OR
2. Passes through some specific node (connecting two different subtrees)

This suggests a **divide-and-conquer** approach using **centroid decomposition**.

### Breaking Down the Problem

1. **What are we looking for?** Paths with exactly k edges
2. **What information do we have?** Tree structure with n-1 edges
3. **What is the relationship between input and output?** Each valid path consists of two "half-paths" from some node, where the sum of their lengths equals k

### The Centroid Decomposition Insight

A **centroid** of a tree is a node whose removal splits the tree into subtrees, each with at most n/2 nodes.

**Key Insight:** For any path in the tree, there exists exactly one centroid (in the centroid decomposition hierarchy) that the path passes through. This means:

1. Find the centroid of the current tree
2. Count all paths of length k that pass through this centroid
3. Remove the centroid and recursively solve for each remaining subtree
4. Since each path is counted exactly once (at its "highest" centroid), we avoid double counting

---

## Solution 1: Brute Force (DFS from Every Node)

### Idea

For each node, run a DFS to count all nodes at distance exactly k. Sum up and divide by 2 (since each path is counted from both endpoints).

### Algorithm

1. Build adjacency list
2. For each node, DFS to find nodes at distance k
3. Count total and divide by 2

### Code

```python
def solve_brute_force(n, k, edges):
 """
 Brute force: DFS from every node.

 Time: O(n^2)
 Space: O(n)
 """
 from collections import defaultdict

 graph = defaultdict(list)
 for a, b in edges:
  graph[a].append(b)
  graph[b].append(a)

 count = 0

 def dfs(node, parent, depth):
  nonlocal count
  if depth == k:
   count += 1
   return
  for neighbor in graph[node]:
   if neighbor != parent:
    dfs(neighbor, node, depth + 1)

 for start in range(1, n + 1):
  dfs(start, -1, 0)

 # Each path counted twice (from both endpoints)
 return count // 2
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | DFS from each of n nodes, each taking O(n) |
| Space | O(n) | Recursion stack depth |

### Why This Works (But Is Slow)

Correctness is guaranteed because we explore all possible paths. However, for n = 2 * 10^5, O(n^2) operations will timeout.

---

## Solution 2: Optimal - Centroid Decomposition

### Key Insight

> **The Trick:** Use centroid decomposition to ensure each path is counted exactly once, achieving O(n log n) complexity.

When we process a centroid:
1. Compute distances from centroid to all nodes in its current subtree
2. For each subtree, count how many paths of length k pass through the centroid
3. Use a frequency array: if we have `cnt[d]` nodes at distance d, and we see a node at distance d', we can form `cnt[k - d']` paths of length k

### Algorithm

1. **Find Centroid:** Calculate subtree sizes and find the node where all subtrees have <= n/2 nodes
2. **Count Paths Through Centroid:**
   - Process each subtree one by one
   - Before processing a subtree, we have `cnt[d]` = count of nodes at distance d from centroid (from previously processed subtrees)
   - For each node at distance d' in current subtree, add `cnt[k - d']` to answer
   - After processing, add current subtree's distances to cnt array
3. **Recurse:** Mark centroid as removed and recurse on each subtree

### Dry Run Example

Let's trace through with the example: n=5, k=2

```
Tree:
    1
    |
    2
    |
    3
   / \
  4   5

Step 1: Find centroid of entire tree
  Subtree sizes from node 1: {1:5, 2:4, 3:3, 4:1, 5:1}
  Centroid = node 3 (removing it gives subtrees of size 2, 1, 1)

Step 2: Count paths through centroid (node 3)
  Initialize: cnt = [1, 0, 0, ...]  (cnt[0]=1 for centroid itself)
  answer = 0

  Process subtree rooted at 2 (going up):
    Node 2: distance 1 from centroid
      - Check cnt[k-1] = cnt[1] = 0, add 0
    Node 1: distance 2 from centroid
      - Check cnt[k-2] = cnt[0] = 1, add 1 to answer
    Update cnt: cnt[1]++, cnt[2]++
    cnt = [1, 1, 1, ...]
    answer = 1 (path 1-2-3)

  Process subtree rooted at 4:
    Node 4: distance 1 from centroid
      - Check cnt[k-1] = cnt[1] = 1, add 1 to answer
    Update cnt: cnt[1]++
    cnt = [1, 2, 1, ...]
    answer = 2 (added path 4-3-2)

  Process subtree rooted at 5:
    Node 5: distance 1 from centroid
      - Check cnt[k-1] = cnt[1] = 2, add 2 to answer
    cnt = [1, 3, 1, ...]
    answer = 4 (added paths 5-3-2 and 5-3-4)

Step 3: Recurse on subtrees (after removing centroid 3)
  Subtree {1,2}: centroid is 2
    - Only path would need length 2, but max distance is 1
    - No additional paths

  Subtrees {4} and {5}: single nodes, no paths

Final answer: 4
```

### Visual Diagram

```
Centroid Decomposition Process:

Original Tree:          After finding centroid 3:
    1
    |                       Subtree 1: 1-2 (size 2)
    2                       Subtree 2: 4   (size 1)
    |                       Subtree 3: 5   (size 1)
   [3] <-- centroid
   / \
  4   5

Counting at centroid 3:
  cnt array tracks distances from centroid

  dist=0: [3]
  dist=1: [2, 4, 5]
  dist=2: [1]

  Paths of length k=2:
  - dist 0 + dist 2: 3 to 1 via 2   (1 path)
  - dist 1 + dist 1: 2-3-4, 2-3-5, 4-3-5 (3 paths)

  Total: 4 paths
```

### Code (Python)

```python
import sys
from collections import defaultdict

def solve(n, k, edges):
 """
 Centroid Decomposition solution.

 Time: O(n log n)
 Space: O(n)
 """
 sys.setrecursionlimit(300000)

 # Build adjacency list
 graph = defaultdict(list)
 for a, b in edges:
  graph[a].append(b)
  graph[b].append(a)

 removed = [False] * (n + 1)
 subtree_size = [0] * (n + 1)
 answer = 0

 def get_subtree_size(node, parent):
  """Calculate subtree sizes for centroid finding."""
  subtree_size[node] = 1
  for neighbor in graph[node]:
   if neighbor != parent and not removed[neighbor]:
    get_subtree_size(neighbor, node)
    subtree_size[node] += subtree_size[neighbor]

 def find_centroid(node, parent, tree_size):
  """Find centroid of the current tree."""
  for neighbor in graph[node]:
   if neighbor != parent and not removed[neighbor]:
    if subtree_size[neighbor] > tree_size // 2:
     return find_centroid(neighbor, node, tree_size)
  return node

 def count_paths(node, parent, dist, cnt):
  """
  Count paths and collect distances.
  Returns list of distances from centroid for nodes in this subtree.
  """
  nonlocal answer

  if dist > k:
   return []

  distances = [dist]

  # Count paths: current node pairs with nodes at distance (k - dist)
  if k - dist >= 0 and k - dist < len(cnt):
   answer += cnt[k - dist]

  for neighbor in graph[node]:
   if neighbor != parent and not removed[neighbor]:
    distances.extend(count_paths(neighbor, node, dist + 1, cnt))

  return distances

 def solve_centroid(node):
  """Process tree rooted at node using centroid decomposition."""
  get_subtree_size(node, -1)
  centroid = find_centroid(node, -1, subtree_size[node])
  removed[centroid] = True

  # cnt[d] = number of nodes at distance d from centroid (from processed subtrees)
  cnt = [0] * (k + 2)
  cnt[0] = 1  # centroid itself at distance 0

  for neighbor in graph[centroid]:
   if not removed[neighbor]:
    # Count paths and get distances for this subtree
    distances = count_paths(neighbor, centroid, 1, cnt)

    # Add these distances to cnt for future subtrees
    for d in distances:
     if d <= k:
      cnt[d] += 1

  # Recurse on subtrees
  for neighbor in graph[centroid]:
   if not removed[neighbor]:
    solve_centroid(neighbor)

 solve_centroid(1)
 return answer


def main():
 input_data = sys.stdin.read().split()
 idx = 0
 n = int(input_data[idx]); idx += 1
 k = int(input_data[idx]); idx += 1

 edges = []
 for _ in range(n - 1):
  a = int(input_data[idx]); idx += 1
  b = int(input_data[idx]); idx += 1
  edges.append((a, b))

 print(solve(n, k, edges))


if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Each node visited O(log n) times across all centroid levels |
| Space | O(n) | Adjacency list, recursion stack, and cnt array |

---

## Common Mistakes

### Mistake 1: Double Counting Paths

```python
# WRONG: Counting paths within the same subtree
for neighbor in graph[centroid]:
 distances = get_all_distances(neighbor)
 for d in distances:
  answer += cnt[k - d]  # This counts paths within same subtree!
 for d in distances:
  cnt[d] += 1
```

**Problem:** If we add distances to cnt before processing all subtrees correctly, we might count paths that stay within the same subtree.

**Fix:** Process subtrees one by one. Only count against nodes from *previously* processed subtrees, then add current subtree to cnt.

### Mistake 2: Forgetting to Reset the Removed Array

```python
# WRONG: Not properly handling the removed array
def solve_centroid(node):
 centroid = find_centroid(node)
 removed[centroid] = True
 # ... process ...
 removed[centroid] = False  # DON'T do this!
```

**Problem:** The centroid should stay removed for the entire decomposition. Resetting it causes infinite recursion or incorrect counting.

**Fix:** Once a centroid is removed, it stays removed. The recursion naturally handles separate subtrees.

### Mistake 3: Not Handling Distance > k

```python
# WRONG: Not checking bounds
def count_paths(node, parent, dist, cnt):
 answer += cnt[k - dist]  # IndexError if dist > k!
```

**Problem:** When dist > k, we get k - dist < 0, causing index errors.

**Fix:** Check `if dist > k: return` at the start, or check bounds before array access.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| k = 1 (all edges) | n=5, k=1, line graph | 4 | Every edge is a path of length 1 |
| Star graph | n=5, k=2, center connected to all | 6 | C(4,2) = 6 paths through center |
| k = n-1 (diameter) | Line graph, k=n-1 | 1 | Only one path spans entire tree |
| k larger than diameter | k > tree diameter | 0 | No path can be that long |
| Two nodes | n=2, k=1 | 1 | Single edge |

---

## When to Use This Pattern

### Use Centroid Decomposition When:
- Counting or finding paths in a tree with specific properties
- Problem involves pairs of nodes where path between them matters
- You need O(n log n) or O(n log^2 n) complexity for tree path queries
- Answering multiple queries about tree paths

### Do Not Use When:
- Simple tree DP suffices (single-pass solutions)
- Problem only involves ancestor-descendant relationships (use LCA instead)
- Tree has special structure (e.g., binary tree with simpler solutions)

### Pattern Recognition Checklist:
- [ ] Problem involves paths in an unrooted tree? --> **Consider Centroid Decomposition**
- [ ] Need to count/find paths with specific length/weight? --> **Centroid Decomposition**
- [ ] Need to pair nodes from different subtrees? --> **Centroid Decomposition**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Tree Diameter](https://cses.fi/problemset/task/1131) | Basic tree path concepts |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | DFS for distances in trees |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Fixed Length Paths II](https://cses.fi/problemset/task/2081) | Count paths with length in range [k1, k2] |
| [Tree Distances II](https://cses.fi/problemset/task/1133) | Sum of distances (rerooting technique) |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Centroid Path Decomposition](https://codeforces.com/problemset/problem/321/C) | Building centroid tree |
| [Race (IOI 2011)](https://oj.uz/problem/view/IOI11_race) | Weighted paths with centroid decomposition |

---

## Key Takeaways

1. **The Core Idea:** Centroid decomposition ensures each path is counted exactly once by processing it at the "highest" centroid it passes through.

2. **Time Optimization:** From O(n^2) brute force to O(n log n) by exploiting the property that removing a centroid creates subtrees of size <= n/2.

3. **Space Trade-off:** We use O(n) extra space for the cnt array and removed markers, which is acceptable.

4. **Pattern:** This is the canonical "count paths through a node" pattern using divide-and-conquer on trees.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why centroid decomposition achieves O(n log n) complexity
- [ ] Implement centroid finding (subtree size calculation + finding balanced node)
- [ ] Correctly count paths without double counting same-subtree paths
- [ ] Handle edge cases (k=1, k larger than diameter)
- [ ] Implement in both Python and C++ within 15 minutes

---

## Additional Resources

- [CP-Algorithms: Centroid Decomposition](https://cp-algorithms.com/graph/centroid-decomposition.html)
- [CSES Fixed-Length Paths I](https://cses.fi/problemset/task/2080) - Count paths of length k
- [Centroid Decomposition Tutorial (Codeforces)](https://codeforces.com/blog/entry/52492)
