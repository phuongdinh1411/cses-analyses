---
layout: simple
title: "Tree Diameter - Finding the Longest Path in a Tree"
permalink: /problem_soulutions/tree_algorithms/tree_diameter_analysis
difficulty: Medium
tags: [tree, dfs, bfs, diameter, graph]
prerequisites: [tree_traversal, dfs_basics]
---

# Tree Diameter

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Two-BFS / Tree DP |
| **CSES Link** | [Tree Diameter](https://cses.fi/problemset/task/1131) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand tree diameter and why it exists uniquely
- [ ] Apply the two-BFS/DFS technique to find farthest nodes
- [ ] Implement tree DP to compute diameter in a single pass
- [ ] Recognize when a problem reduces to finding tree diameter

---

## Problem Statement

**Problem:** Given a tree with n nodes, find the diameter - the maximum number of edges in any path between two nodes.

**Input:**
- Line 1: Integer n (number of nodes)
- Lines 2 to n: Two integers a and b (edge between nodes a and b)

**Output:**
- Print one integer: the diameter of the tree

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= a, b <= n

### Example

```
Input:
5
1 2
1 3
3 4
3 5

Output:
3
```

**Explanation:** The tree looks like:
```
    1
   / \
  2   3
     / \
    4   5
```
The longest path is 2 -> 1 -> 3 -> 4 (or 2 -> 1 -> 3 -> 5), with 3 edges.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently find the longest path without checking all pairs?

The diameter always passes through some node as its "highest point." If we find an endpoint of the diameter first, we can find the other endpoint with a single traversal.

### Breaking Down the Problem

1. **What are we looking for?** The maximum distance between any two nodes.
2. **What information do we have?** Tree structure (n-1 edges connecting n nodes).
3. **What's the relationship?** In a tree, there's exactly one path between any two nodes.

### The Two Key Insights

**Insight 1 (Two-BFS):** Start BFS from any node. The farthest node found is one endpoint of the diameter. BFS again from that node gives the diameter.

**Insight 2 (Tree DP):** For each node, track the two longest paths going down through its children. The diameter through that node is their sum.

---

## Solution 1: Brute Force

### Idea

Check all pairs of nodes and find the path length between them.

### Algorithm

1. Build adjacency list from edges
2. For each pair (i, j), use BFS to find distance
3. Track and return maximum distance

### Code

```python
from collections import deque

def brute_force_diameter(n, edges):
  """
  Brute force: Check all pairs.

  Time: O(n^3) - n^2 pairs, O(n) BFS each
  Space: O(n)
  """
  adj = [[] for _ in range(n + 1)]
  for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)

  def bfs_distance(start, end):
    queue = deque([(start, 0)])
    visited = [False] * (n + 1)
    visited[start] = True
    while queue:
      node, dist = queue.popleft()
      if node == end:
        return dist
      for neighbor in adj[node]:
        if not visited[neighbor]:
          visited[neighbor] = True
          queue.append((neighbor, dist + 1))
    return 0

  max_diameter = 0
  for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
      max_diameter = max(max_diameter, bfs_distance(i, j))
  return max_diameter
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3) | n^2 pairs, each BFS takes O(n) |
| Space | O(n) | Adjacency list and visited array |

### Why This Works (But Is Slow)

Correctness is guaranteed by exhaustive search, but cubic time makes it impractical for n = 200,000.

---

## Solution 2: Two-BFS Approach

### Key Insight

> **The Trick:** The farthest node from ANY starting node is always an endpoint of some diameter path.

### Why Does This Work?

Proof sketch: Suppose we start at node S and find the farthest node A. If A is not a diameter endpoint, let (X, Y) be the actual diameter. Since tree paths are unique, the path S->A must share some portion with X->Y. But then A would be farther from S than Y is from S, contradicting that X->Y is the diameter.

### Algorithm

1. BFS from node 1 to find farthest node (call it A)
2. BFS from A to find farthest node (call it B)
3. Distance from A to B is the diameter

### Dry Run Example

```
Tree: 1-2, 1-3, 3-4, 3-5

Step 1: BFS from node 1
  Node 1: distance 0
  Node 2: distance 1
  Node 3: distance 1
  Node 4: distance 2
  Node 5: distance 2
  Farthest: node 4 (distance 2)

Step 2: BFS from node 4
  Node 4: distance 0
  Node 3: distance 1
  Node 1: distance 2
  Node 5: distance 2
  Node 2: distance 3
  Farthest: node 2 (distance 3)

Diameter = 3
```

### Visual Diagram

```
BFS from 1:           BFS from 4:
    1 (0)                 1 (2)
   / \                   / \
  2   3                 2   3
 (1) (1)               (3) (1)
     / \                   / \
    4   5                 4   5
   (2) (2)               (0) (2)

Farthest: 4           Farthest: 2
                      Diameter: 3
```

### Code (Python)

```python
from collections import deque

def solve():
  n = int(input())
  if n == 1:
    print(0)
    return

  adj = [[] for _ in range(n + 1)]
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  def bfs(start):
    """Return (farthest_node, distance_to_it)"""
    dist = [-1] * (n + 1)
    dist[start] = 0
    queue = deque([start])
    farthest, max_dist = start, 0

    while queue:
      node = queue.popleft()
      for neighbor in adj[node]:
        if dist[neighbor] == -1:
          dist[neighbor] = dist[node] + 1
          queue.append(neighbor)
          if dist[neighbor] > max_dist:
            max_dist = dist[neighbor]
            farthest = neighbor
    return farthest, max_dist

  # First BFS: find one endpoint
  endpoint, _ = bfs(1)
  # Second BFS: find diameter
  _, diameter = bfs(endpoint)
  print(diameter)

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Two BFS traversals, each O(n) |
| Space | O(n) | Adjacency list and distance array |

---

## Solution 3: Tree DP (Single DFS)

### Key Insight

> **The Trick:** The diameter passes through some node as its "peak." At each node, combine the two longest downward paths.

### DP State Definition

| State | Meaning |
|-------|---------|
| `depth[v]` | Longest path going down from node v |

**In plain English:** Track the maximum depth reachable from each node through its subtree.

### State Transition

At each node, the diameter passing through it equals:
```
diameter_through_node = max_child_depth + second_max_child_depth
```

We update the global answer with this value and return `max_child_depth + 1` to the parent.

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
  n = int(input())
  if n == 1:
    print(0)
    return

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  diameter = 0

  def dfs(node, parent):
    nonlocal diameter
    max1 = max2 = 0  # Two longest paths down

    for child in adj[node]:
      if child != parent:
        child_depth = dfs(child, node) + 1
        if child_depth > max1:
          max2 = max1
          max1 = child_depth
        elif child_depth > max2:
          max2 = child_depth

    diameter = max(diameter, max1 + max2)
    return max1

  dfs(1, -1)
  print(diameter)

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single DFS traversal |
| Space | O(n) | Adjacency list + recursion stack |

---

## Common Mistakes

### Mistake 1: Stack Overflow in DFS

```python
# WRONG - default recursion limit is ~1000
def dfs(node, parent):
  ...
```

**Problem:** Python's default recursion limit causes crashes for large trees.
**Fix:** Add `sys.setrecursionlimit(300000)` or use iterative DFS.

### Mistake 2: Forgetting Single Node Case

```python
# WRONG - crashes when n=1 (no edges to read)
for _ in range(n - 1):
  a, b = map(int, input().split())
```

**Problem:** When n=1, there are 0 edges, and the diameter is 0.
**Fix:** Handle `n == 1` as a special case returning 0.

### Mistake 3: Using Wrong Graph Indexing

**Problem:** Off-by-one errors when nodes are numbered 1 to n.
**Fix:** Use `adj[n + 1]` or convert to 0-indexed.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1, no edges | 0 | No path exists |
| Two nodes | n=2, edge 1-2 | 1 | Only one edge |
| Linear tree | 1-2-3-4-5 | 4 | Path is the whole tree |
| Star graph | 1 connected to 2,3,4,5 | 2 | Any leaf-to-leaf path |
| Balanced binary | Complete binary tree | 2*height | Through root |

---

## When to Use This Pattern

### Use Two-BFS/DFS When:
- Finding the actual diameter endpoints matters
- You need to find the diameter path itself
- The tree is given as an edge list

### Use Tree DP When:
- You need to compute related values (e.g., all node eccentricities)
- The problem involves subtree computations
- You want to extend to weighted edges easily

### Pattern Recognition Checklist:
- [ ] Finding longest path in a tree? -> **Tree Diameter**
- [ ] Need farthest node from a source? -> **Single BFS**
- [ ] Computing something for each subtree? -> **Tree DP**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subordinates (CSES 1674)](https://cses.fi/problemset/task/1674) | Basic tree DFS |
| [Tree Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | BFS on trees |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Tree Distances I (CSES 1132)](https://cses.fi/problemset/task/1132) | Max distance from each node |
| [Tree Distances II (CSES 1133)](https://cses.fi/problemset/task/1133) | Sum of distances from each node |
| [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Weighted nodes instead of edges |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Centroid Decomposition](https://cses.fi/problemset/task/2079) | Tree decomposition |
| [Tree Queries (CSES 1135)](https://cses.fi/problemset/task/1135) | LCA and path queries |

---

## Key Takeaways

1. **The Core Idea:** Tree diameter can be found in O(n) using either two-BFS or tree DP.
2. **Two-BFS:** Intuitive - find an endpoint, then find the farthest from it.
3. **Tree DP:** Elegant - at each node, combine the two longest downward paths.
4. **Pattern:** This is a fundamental tree algorithm; many problems reduce to it.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement two-BFS solution from memory
- [ ] Implement tree DP solution from memory
- [ ] Explain why two-BFS works (proof sketch)
- [ ] Handle edge cases (n=1, linear tree, star graph)
- [ ] Extend to weighted edges (replace +1 with edge weight)
