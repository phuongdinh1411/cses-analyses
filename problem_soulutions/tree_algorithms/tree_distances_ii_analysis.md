---
layout: simple
title: "Tree Distances II - Rerooting DP"
permalink: /problem_soulutions/tree_algorithms/tree_distances_ii_analysis
difficulty: Medium
tags: [tree-dp, rerooting, dfs, distance-sum]
prerequisites: [tree_traversal, subtree_size]
---

# Tree Distances II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES 1133 - Tree Distances II](https://cses.fi/problemset/task/1133) |
| **Difficulty** | Medium |
| **Category** | Tree DP / Rerooting |
| **Time Limit** | 1 second |
| **Key Technique** | Rerooting DP (Two-Pass DFS) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement the rerooting DP technique
- [ ] Calculate subtree sizes and aggregate values in a single DFS pass
- [ ] Transform root-specific DP values to all-node answers in O(n) time
- [ ] Recognize problems where rerooting DP applies

---

## Problem Statement

**Problem:** Given a tree with n nodes, for each node calculate the sum of distances to all other nodes.

**Input:**
- Line 1: n (number of nodes)
- Next n-1 lines: Two integers a, b representing an edge

**Output:**
- n integers: For each node 1 to n, print the sum of distances to all other nodes

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
6
9
5
8
8
```

**Explanation:**
- Node 1: dist(1,2)=1, dist(1,3)=1, dist(1,4)=2, dist(1,5)=2 => sum = 6
- Node 2: dist(2,1)=1, dist(2,3)=2, dist(2,4)=3, dist(2,5)=3 => sum = 9
- Node 3: dist(3,1)=1, dist(3,2)=2, dist(3,4)=1, dist(3,5)=1 => sum = 5
- Node 4: dist(4,1)=2, dist(4,2)=3, dist(4,3)=1, dist(4,5)=2 => sum = 8
- Node 5: dist(5,1)=2, dist(5,2)=3, dist(5,3)=1, dist(5,4)=2 => sum = 8

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** If we know the answer for one node, can we efficiently compute it for adjacent nodes?

The naive approach runs BFS/DFS from each node: O(n^2). For n = 2x10^5, this is too slow. The key insight is that when we "move" from node u to an adjacent node v, the distances change in a predictable way.

### Breaking Down the Problem

1. **What are we looking for?** Sum of distances from each node to all others
2. **What information helps?** Subtree sizes tell us how many nodes get closer/farther when rerooting
3. **What's the relationship?** Moving root from u to v: nodes in v's subtree get 1 closer, all others get 1 farther

### The Rerooting Insight

When we move the root from node `u` to its child `v`:
- All `subtree_size[v]` nodes in v's subtree become 1 step **closer**
- All `n - subtree_size[v]` other nodes become 1 step **farther**

Therefore:
```
answer[v] = answer[u] - subtree_size[v] + (n - subtree_size[v])
answer[v] = answer[u] + n - 2 * subtree_size[v]
```

---

## Solution 1: Brute Force

### Idea

Run BFS from each node to compute distances to all other nodes, then sum them.

### Algorithm

1. Build adjacency list
2. For each node, run BFS to find all distances
3. Sum distances for each starting node

### Code

```python
def solve_brute_force(n, edges):
 """
 Brute force: BFS from each node.

 Time: O(n^2)
 Space: O(n)
 """
 from collections import deque, defaultdict

 adj = defaultdict(list)
 for a, b in edges:
  adj[a].append(b)
  adj[b].append(a)

 results = []
 for start in range(1, n + 1):
  queue = deque([(start, 0)])
  visited = {start}
  total = 0

  while queue:
   node, dist = queue.popleft()
   total += dist
   for neighbor in adj[node]:
    if neighbor not in visited:
     visited.add(neighbor)
     queue.append((neighbor, dist + 1))

  results.append(total)

 return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | BFS is O(n), done n times |
| Space | O(n) | Queue and visited set |

### Why This Works (But Is Slow)

BFS correctly finds shortest paths in unweighted graphs. However, repeating it n times is inefficient for large n.

---

## Solution 2: Optimal - Rerooting DP

### Key Insight

> **The Trick:** Compute the answer for root (node 1) first, then propagate to all other nodes by adjusting based on how subtree sizes affect distances.

### Two-Pass Algorithm

**Pass 1 (Post-order DFS):** Compute for each node:
- `subtree_size[v]`: Number of nodes in subtree rooted at v
- `subtree_dist[v]`: Sum of distances from v to all nodes in its subtree

**Pass 2 (Pre-order DFS):** Propagate answers:
- Start with `answer[root] = subtree_dist[root]`
- For each child: `answer[child] = answer[parent] + n - 2 * subtree_size[child]`

### State Definition

| State | Meaning |
|-------|---------|
| `subtree_size[v]` | Number of nodes in subtree rooted at v |
| `subtree_dist[v]` | Sum of distances from v to all descendants |
| `answer[v]` | Sum of distances from v to ALL nodes in tree |

### State Transition

**Pass 1 (building subtree info):**
```
subtree_size[v] = 1 + sum(subtree_size[child] for all children)
subtree_dist[v] = sum(subtree_dist[child] + subtree_size[child] for all children)
```

**Pass 2 (rerooting):**
```
answer[child] = answer[parent] + n - 2 * subtree_size[child]
```

**Why the rerooting formula works:**
- When moving from parent to child, `subtree_size[child]` nodes get 1 closer (-subtree_size[child])
- The remaining `n - subtree_size[child]` nodes get 1 farther (+n - subtree_size[child])
- Net change: `-subtree_size[child] + n - subtree_size[child] = n - 2 * subtree_size[child]`

### Dry Run Example

Let's trace through the example tree:

```
Tree structure:
      1
     / \
    2   3
       / \
      4   5

Edges: (1,2), (1,3), (3,4), (3,5)
```

**Pass 1: Post-order DFS from root=1**

```
Processing order: 2, 4, 5, 3, 1

Node 2 (leaf):
  subtree_size[2] = 1
  subtree_dist[2] = 0

Node 4 (leaf):
  subtree_size[4] = 1
  subtree_dist[4] = 0

Node 5 (leaf):
  subtree_size[5] = 1
  subtree_dist[5] = 0

Node 3 (parent of 4, 5):
  subtree_size[3] = 1 + 1 + 1 = 3
  subtree_dist[3] = (0 + 1) + (0 + 1) = 2
  (Each child contributes: its subtree_dist + its subtree_size)

Node 1 (root, parent of 2, 3):
  subtree_size[1] = 1 + 1 + 3 = 5
  subtree_dist[1] = (0 + 1) + (2 + 3) = 6
```

**Pass 2: Pre-order DFS (rerooting)**

```
answer[1] = subtree_dist[1] = 6

Move to node 2:
  answer[2] = answer[1] + n - 2*subtree_size[2]
            = 6 + 5 - 2*1 = 9

Move to node 3:
  answer[3] = answer[1] + n - 2*subtree_size[3]
            = 6 + 5 - 2*3 = 5

Move to node 4 (from node 3):
  answer[4] = answer[3] + n - 2*subtree_size[4]
            = 5 + 5 - 2*1 = 8

Move to node 5 (from node 3):
  answer[5] = answer[3] + n - 2*subtree_size[5]
            = 5 + 5 - 2*1 = 8

Final answers: [6, 9, 5, 8, 8]
```

### Visual Diagram

```
Rerooting from Node 1 to Node 3:

Before (root = 1):          After (root = 3):
      1*                          1
     / \                         / \
    2   3                       2   3*
       / \                         / \
      4   5                       4   5

Moving root 1 -> 3:
- Nodes {3,4,5} (subtree_size[3]=3) get CLOSER by 1: -3
- Nodes {1,2} (n - subtree_size[3]=2) get FARTHER by 1: +2
- Net change: -3 + 2 = -1
- Or using formula: n - 2*subtree_size[3] = 5 - 6 = -1
- answer[3] = answer[1] + (-1) = 6 - 1 = 5
```

### Code (Python)

```python
import sys
from collections import defaultdict

def solve(n, edges):
 """
 Rerooting DP solution.

 Time: O(n) - two DFS passes
 Space: O(n) - adjacency list and arrays
 """
 if n == 1:
  print(0)
  return

 # Build adjacency list
 adj = defaultdict(list)
 for a, b in edges:
  adj[a].append(b)
  adj[b].append(a)

 subtree_size = [0] * (n + 1)
 subtree_dist = [0] * (n + 1)
 answer = [0] * (n + 1)

 # Pass 1: Calculate subtree sizes and distances (iterative)
 parent = [0] * (n + 1)
 order = []
 visited = [False] * (n + 1)
 stack = [1]

 while stack:
  node = stack.pop()
  if visited[node]:
   continue
  visited[node] = True
  order.append(node)
  for neighbor in adj[node]:
   if not visited[neighbor]:
    parent[neighbor] = node
    stack.append(neighbor)

 # Process in reverse order (post-order)
 for node in reversed(order):
  subtree_size[node] = 1
  subtree_dist[node] = 0
  for neighbor in adj[node]:
   if neighbor != parent[node]:
    subtree_size[node] += subtree_size[neighbor]
    subtree_dist[node] += subtree_dist[neighbor] + subtree_size[neighbor]

 # Pass 2: Rerooting (process in order)
 answer[1] = subtree_dist[1]
 for node in order:
  for neighbor in adj[node]:
   if neighbor != parent[node]:
    answer[neighbor] = answer[node] + n - 2 * subtree_size[neighbor]

 # Output
 for i in range(1, n + 1):
  print(answer[i])


def main():
 input_data = sys.stdin.read().split()
 idx = 0
 n = int(input_data[idx]); idx += 1

 edges = []
 for _ in range(n - 1):
  a = int(input_data[idx]); idx += 1
  b = int(input_data[idx]); idx += 1
  edges.append((a, b))

 solve(n, edges)


if __name__ == "__main__":
 sys.setrecursionlimit(300000)
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Two linear passes over the tree |
| Space | O(n) | Adjacency list and DP arrays |

---

## Common Mistakes

### Mistake 1: Wrong Rerooting Formula

```python
# WRONG - forgetting the relationship
answer[child] = answer[parent] - subtree_size[child]

# CORRECT
answer[child] = answer[parent] + n - 2 * subtree_size[child]
```

**Problem:** Only accounting for nodes getting closer, not those getting farther.
**Fix:** Remember both effects: closer nodes (-subtree_size) AND farther nodes (+n-subtree_size).

### Mistake 2: Integer Overflow

**Problem:** With n = 2x10^5 nodes, distances can sum to ~10^10.
**Fix:** Use `long long` in C++ or Python's native integers.

### Mistake 3: Incorrect Subtree Calculation

```python
# WRONG - including parent in subtree
for neighbor in adj[node]:
 subtree_size[node] += subtree_size[neighbor]

# CORRECT - exclude parent
for neighbor in adj[node]:
 if neighbor != parent[node]:
  subtree_size[node] += subtree_size[neighbor]
```

**Problem:** Parent is not part of the subtree.
**Fix:** Always check `neighbor != parent` when processing children.

### Mistake 4: Stack Overflow with Recursion

```python
# WRONG - recursive DFS on deep trees
def dfs(node, parent):
 for child in adj[node]:
  if child != parent:
   dfs(child, node)  # May overflow for n=200000

# CORRECT - use iterative approach or increase recursion limit
sys.setrecursionlimit(300000)
```

**Problem:** Deep trees (like a line) cause stack overflow.
**Fix:** Use iterative DFS or set appropriate recursion limits.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1 | 0 | No other nodes to reach |
| Two nodes | n=2, edge (1,2) | 1, 1 | Each node is distance 1 from the other |
| Line graph | 1-2-3-4-5 | 10,7,6,7,10 | Nodes at ends have largest sums |
| Star graph | 1 connected to 2,3,4,5 | 4,6,6,6,6 | Center has minimum sum |
| Large n | n=200000 | varies | Test for TLE and overflow |

---

## When to Use This Pattern

### Use Rerooting DP When:
- Computing a value for each node that depends on entire tree structure
- The value changes predictably when "moving" the root to an adjacent node
- Naive approach would require O(n) work per node (O(n^2) total)

### Common Rerooting Problems:
- Sum of distances from each node (this problem)
- Number of nodes within distance k from each node
- Minimum/maximum distance to a leaf from each node
- Tree centroids and related problems

### Pattern Recognition Checklist:
- [ ] Need to compute something for EVERY node? --> Consider rerooting
- [ ] Can you compute it easily for ONE root? --> First pass
- [ ] Does moving root change answer predictably? --> Second pass (reroot)

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Tree Diameter](https://cses.fi/problemset/task/1131) | Basic tree DFS, understanding distances |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Max distance from each node, simpler rerooting |
| [Subtree Sizes](practice) | Foundation for computing subtree_size array |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Sum of Distances in Tree (LC 834)](https://leetcode.com/problems/sum-of-distances-in-tree/) | Same problem on LeetCode |
| [Count Nodes Equal to Sum of Descendants (LC 1973)](https://leetcode.com/problems/count-nodes-equal-to-sum-of-descendants/) | Subtree sums, similar technique |
| [Subordinates](https://cses.fi/problemset/task/1674) | Subtree counting |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Tree Matching](https://cses.fi/problemset/task/1130) | Tree DP with more complex states |
| [Path Queries II](https://cses.fi/problemset/task/2134) | Heavy-Light Decomposition |
| [Distance Queries](https://cses.fi/problemset/task/1135) | LCA + distance calculations |

---

## Key Takeaways

1. **Core Idea:** Rerooting DP computes answers for all nodes in O(n) by leveraging how answers change when moving the root.

2. **Two-Pass Structure:** First pass builds subtree information bottom-up; second pass propagates answers top-down.

3. **The Formula:** When moving from parent to child: `answer[child] = answer[parent] + n - 2*subtree_size[child]`

4. **Pattern:** This technique applies whenever you need node-specific aggregates that depend on tree structure.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why the rerooting formula works
- [ ] Implement both passes of the algorithm from scratch
- [ ] Handle edge cases (n=1, line graphs, star graphs)
- [ ] Identify other problems where rerooting DP applies
- [ ] Solve this problem in under 15 minutes
