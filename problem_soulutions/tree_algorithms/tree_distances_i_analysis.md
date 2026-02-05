---
layout: simple
title: "Tree Distances I - Tree Algorithms Problem"
permalink: /problem_soulutions/tree_algorithms/tree_distances_i_analysis
difficulty: Medium
tags: [tree, dfs, diameter, graph]
prerequisites: [tree_basics, dfs_traversal]
---

# Tree Distances I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Tree Diameter + BFS/DFS |
| **CSES Link** | [Tree Distances I](https://cses.fi/problemset/task/1132) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the relationship between tree diameter and maximum node distances
- [ ] Apply the "farthest node" property: the farthest node from any node is always a diameter endpoint
- [ ] Implement efficient O(n) tree traversal to compute distances from multiple sources
- [ ] Use the two-BFS/DFS technique to find tree diameter endpoints

---

## Problem Statement

**Problem:** Given a tree with n nodes, find the maximum distance from each node to any other node in the tree.

**Input:**
- Line 1: n (number of nodes)
- Lines 2 to n: Two integers a and b representing an edge between nodes a and b

**Output:**
- n integers: the maximum distance from node i to any other node (for i = 1, 2, ..., n)

**Constraints:**
- 1 <= n <= 2 x 10^5

### Example

```
Input:
5
1 2
1 3
3 4
3 5

Output:
2 3 2 3 3
```

**Explanation:**
- Node 1: Farthest nodes are 4 and 5 (distance 2)
- Node 2: Farthest nodes are 4 and 5 (distance 3)
- Node 3: Farthest nodes are 2 (distance 2)
- Node 4: Farthest node is 2 (distance 3)
- Node 5: Farthest node is 2 (distance 3)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we find the farthest node from every node without doing n separate BFS traversals?

The crucial insight is that **the farthest node from any node in a tree is always one of the two endpoints of the diameter**. The diameter is the longest path in the tree.

### Breaking Down the Problem

1. **What are we looking for?** For each node, the maximum distance to any other node.
2. **What information do we have?** The tree structure (nodes and edges).
3. **What's the relationship between input and output?** The farthest node from any node v is always one of the diameter endpoints.

### Why the Diameter Property Works

Consider any node v in the tree. Let (A, B) be the diameter endpoints. We claim that the farthest node from v is either A or B.

**Proof by contradiction:** Suppose the farthest node from v is C, where C is neither A nor B. Then the path from A to v to C would be longer than the path from A to B (since v to C > v to A or v to B), contradicting that (A, B) is the diameter.

```
        A (diameter endpoint)
        |
        x
       / \
      v   ...
       \
        y
        |
        B (diameter endpoint)

For any node v, max(dist(v,A), dist(v,B)) = farthest distance from v
```

---

## Solution 1: Brute Force

### Idea

For each node, run BFS to find the distance to all other nodes and take the maximum.

### Algorithm

1. Build adjacency list from edges
2. For each node i from 1 to n:
   - Run BFS starting from node i
   - Track maximum distance reached
3. Output maximum distances

### Code

```python
def solve_brute_force(n, edges):
    """
    Brute force: BFS from each node.

    Time: O(n^2)
    Space: O(n)
    """
    from collections import deque, defaultdict

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    results = []
    for start in range(1, n + 1):
        queue = deque([(start, 0)])
        visited = {start}
        max_dist = 0

        while queue:
            node, dist = queue.popleft()
            max_dist = max(max_dist, dist)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        results.append(max_dist)

    return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | BFS takes O(n) for each of n nodes |
| Space | O(n) | Queue and visited set |

### Why This Works (But Is Slow)

BFS correctly finds shortest paths in unweighted graphs. However, with n up to 200,000 nodes, O(n^2) is too slow (~40 billion operations).

---

## Solution 2: Optimal Solution (Diameter-Based)

### Key Insight

> **The Trick:** The farthest node from any node is always one of the two diameter endpoints. So we only need 3 BFS/DFS traversals instead of n.

### Algorithm

1. **Find first diameter endpoint (A):** Run BFS/DFS from any node (e.g., node 1). The farthest node found is one endpoint of the diameter.
2. **Find second diameter endpoint (B):** Run BFS/DFS from A. The farthest node is the other endpoint B. Also record distances from A to all nodes.
3. **Calculate distances from B:** Run BFS/DFS from B to get distances from B to all nodes.
4. **Answer for each node:** max(dist_from_A[i], dist_from_B[i])

### Dry Run Example

Let's trace through with the example tree:

```
Tree structure:
      1
     / \
    2   3
       / \
      4   5

Edges: (1,2), (1,3), (3,4), (3,5)
```

**Step 1: Find first diameter endpoint**
```
BFS from node 1:
  dist[1] = 0
  dist[2] = 1, dist[3] = 1
  dist[4] = 2, dist[5] = 2

Farthest node from 1: node 4 or 5 (distance 2)
Let A = 4
```

**Step 2: Find second diameter endpoint and distances from A**
```
BFS from node 4 (A):
  dist_from_A[4] = 0
  dist_from_A[3] = 1
  dist_from_A[1] = 2, dist_from_A[5] = 2
  dist_from_A[2] = 3

Farthest node from 4: node 2 (distance 3)
B = 2
Diameter length = 3
```

**Step 3: Calculate distances from B**
```
BFS from node 2 (B):
  dist_from_B[2] = 0
  dist_from_B[1] = 1
  dist_from_B[3] = 2
  dist_from_B[4] = 3, dist_from_B[5] = 3
```

**Step 4: Calculate answers**
```
Node 1: max(dist_from_A[1], dist_from_B[1]) = max(2, 1) = 2
Node 2: max(dist_from_A[2], dist_from_B[2]) = max(3, 0) = 3
Node 3: max(dist_from_A[3], dist_from_B[3]) = max(1, 2) = 2
Node 4: max(dist_from_A[4], dist_from_B[4]) = max(0, 3) = 3
Node 5: max(dist_from_A[5], dist_from_B[5]) = max(2, 3) = 3

Output: 2 3 2 3 3
```

### Visual Diagram

```
Tree:        Distances from A=4:    Distances from B=2:    Answer:
    1             2                      1                   2
   / \           / \                    / \                 / \
  2   3         3   1                  0   2               3   2
     / \           / \                    / \                 / \
    4   5         0   2                  3   3               3   3
```

### Code (Python)

```python
import sys
from collections import defaultdict, deque

def solve():
    input = sys.stdin.readline
    n = int(input())

    graph = defaultdict(list)
    for _ in range(n - 1):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    def bfs(start):
        """Returns (distances array, farthest node)"""
        dist = [-1] * (n + 1)
        dist[start] = 0
        queue = deque([start])
        farthest = start

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
                    if dist[neighbor] > dist[farthest]:
                        farthest = neighbor

        return dist, farthest

    # Step 1: Find first diameter endpoint
    _, endpoint_a = bfs(1)

    # Step 2: Find second endpoint and distances from A
    dist_from_a, endpoint_b = bfs(endpoint_a)

    # Step 3: Get distances from B
    dist_from_b, _ = bfs(endpoint_b)

    # Step 4: Answer is max of distances to both endpoints
    result = []
    for i in range(1, n + 1):
        result.append(max(dist_from_a[i], dist_from_b[i]))

    print(' '.join(map(str, result)))

if __name__ == "__main__":
    sys.setrecursionlimit(300000)
    solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Three BFS traversals, each O(n) |
| Space | O(n) | Adjacency list and distance arrays |

---

## Common Mistakes

### Mistake 1: Forgetting to Handle Single Node

```python
# WRONG - crashes on n=1
_, endpoint_a = bfs(1)  # Works
dist_from_a, endpoint_b = bfs(endpoint_a)  # endpoint_a = 1, still works

# But make sure BFS handles empty adjacency list!
```

**Problem:** With n=1, there are no edges, so the answer should be 0.
**Fix:** The algorithm naturally handles this since BFS from node 1 gives distance 0.

### Mistake 2: Using DFS with Deep Recursion

```python
# WRONG - stack overflow for n=200000
def dfs(node, parent, dist):
    # ... recursive calls
    for child in graph[node]:
        if child != parent:
            dfs(child, node, dist + 1)  # May cause stack overflow!
```

**Problem:** Python's default recursion limit (~1000) is too small.
**Fix:** Either increase recursion limit or use iterative BFS.

### Mistake 3: Not Resetting Distance Array

**Problem:** Distance array contains garbage or values from previous BFS.
**Fix:** Always initialize distances to -1 before each BFS.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1 | 0 | No other nodes to reach |
| Line graph | 1-2-3-4-5 | 4 3 2 3 4 | Endpoints have max distance |
| Star graph | 1 connected to 2,3,4,5 | 2 2 2 2 2 | All leaves equidistant |
| Two nodes | n=2, edge (1,2) | 1 1 | Simple case |

---

## When to Use This Pattern

### Use This Approach When:
- Finding farthest distances from all nodes in a tree
- Problems involving tree diameter
- Need to identify "extreme" nodes in a tree structure

### Don't Use When:
- Graph has cycles (not a tree)
- Edge weights are non-uniform (need different algorithm)
- Looking for shortest paths (this finds longest)

### Pattern Recognition Checklist:
- [ ] Is the graph a tree (n nodes, n-1 edges, connected)?
- [ ] Do you need maximum/farthest distance?
- [ ] Is the answer related to diameter endpoints?

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Tree Diameter](https://cses.fi/problemset/task/1131) | Simpler version - just find diameter length |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Tree Distances II](https://cses.fi/problemset/task/1133) | Sum of distances instead of max (uses rerooting DP) |
| [Diameter of Binary Tree (LeetCode 543)](https://leetcode.com/problems/diameter-of-binary-tree/) | Binary tree version |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Sum of Distances in Tree (LeetCode 834)](https://leetcode.com/problems/sum-of-distances-in-tree/) | Rerooting technique for sum queries |
| [Tree Matching](https://cses.fi/problemset/task/1130) | Tree DP for matching problems |

---

## Key Takeaways

1. **The Core Idea:** The farthest node from any node is always a diameter endpoint.
2. **Time Optimization:** Reduced from O(n^2) to O(n) by leveraging diameter property.
3. **Space Trade-off:** O(n) space for distance arrays is necessary and optimal.
4. **Pattern:** "Find diameter endpoints first" is a common pattern for tree distance problems.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why the farthest node is always a diameter endpoint
- [ ] Implement the 3-BFS solution from scratch
- [ ] Handle edge cases (single node, line graph, star graph)
- [ ] Solve this problem in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Tree Diameter](https://cp-algorithms.com/graph/tree_diameter.html)
- [CSES Problem Set - Tree Algorithms](https://cses.fi/problemset/list/)
