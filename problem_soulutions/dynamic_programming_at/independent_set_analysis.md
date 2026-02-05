---
layout: simple
title: "Independent Set - Tree DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/independent_set_analysis
difficulty: Medium
tags: [tree-dp, dfs, counting, modular-arithmetic]
---

# Independent Set

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [AtCoder DP Contest - Problem P](https://atcoder.jp/contests/dp/tasks/dp_p) |
| **Difficulty** | Medium |
| **Category** | Tree DP |
| **Time Limit** | 2 seconds |
| **Key Technique** | Tree DP with Binary State |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the tree DP paradigm with state transitions between parent and children
- [ ] Define DP states based on node selection (selected/not selected)
- [ ] Combine results from multiple subtrees using multiplication
- [ ] Apply modular arithmetic in counting problems

---

## Problem Statement

**Problem:** Given a tree with N vertices, color each vertex either black or white such that no two adjacent vertices are both black. Count the number of valid colorings modulo 10^9 + 7.

**Input:**
- Line 1: N (number of vertices)
- Lines 2 to N: Two integers x_i, y_i representing an edge

**Output:**
- Number of valid colorings modulo 10^9 + 7

**Constraints:**
- 1 <= N <= 10^5
- The graph is a tree (connected, N-1 edges, no cycles)

### Example

```
Input:
3
1 2
2 3

Output:
5
```

**Explanation:** The valid colorings for a path of 3 nodes (1-2-3) are:
- WWW (all white)
- BWW (node 1 black)
- WBW (node 2 black) - NOT valid, since if 2 is black, 1 and 3 must be white
- WWB (node 3 black)
- BWB (nodes 1 and 3 black)
- WBW is actually valid (only node 2 is black)

Wait, let me recalculate: WWW, BWW, WBW, WWB, BWB = 5 colorings. Correct!

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count colorings on a tree where adjacent nodes have constraints?

This is a classic **Tree DP** problem. The key insight is that a tree has a hierarchical structure - if we root the tree, each subtree's valid colorings depend only on the color of its root node. This independence between subtrees (given the root's color) allows us to multiply counts.

### Breaking Down the Problem

1. **What are we looking for?** Total count of valid black/white colorings
2. **What information do we have?** Tree structure with N nodes
3. **What's the relationship?** If a node is black, all its children must be white. If a node is white, children can be either color.

### Analogies

Think of this like seating arrangements at a family dinner where certain relatives cannot sit next to each other. If grandpa (parent node) wears a black suit, none of his children can wear black. But if grandpa wears white, each child independently chooses their color.

---

## Solution: Tree DP with Binary State

### Key Insight

> **The Trick:** For each node, track two values: count of valid subtree colorings when this node is white, and when this node is black. Combine children's counts using multiplication (independent choices).

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[v][0]` | Number of valid colorings for subtree rooted at v, where v is WHITE |
| `dp[v][1]` | Number of valid colorings for subtree rooted at v, where v is BLACK |

**In plain English:** For each node, we separately count how many ways to color its entire subtree assuming the node itself is white vs black.

### State Transition

```
dp[v][0] = PRODUCT of (dp[child][0] + dp[child][1]) for all children
dp[v][1] = PRODUCT of (dp[child][0]) for all children
```

**Why?**
- If v is **WHITE**: Each child can be white OR black independently, so we multiply (white + black) counts
- If v is **BLACK**: Each child MUST be white (no two adjacent blacks), so we multiply only white counts

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| Leaf node, white | dp[leaf][0] = 1 | One way: color it white |
| Leaf node, black | dp[leaf][1] = 1 | One way: color it black |

### Algorithm

1. Build adjacency list from edges
2. Root the tree at any node (typically node 1)
3. DFS from root, computing dp values bottom-up
4. For each node, combine children's dp values using the transition formula
5. Answer = dp[root][0] + dp[root][1]

### Dry Run Example

Let's trace through with the example tree: 1 - 2 - 3 (path graph)

```
Tree structure (rooted at 1):
    1
    |
    2
    |
    3

DFS traversal: Visit 1 -> Visit 2 -> Visit 3 -> Return to 2 -> Return to 1

Step 1: Process node 3 (leaf)
  dp[3][0] = 1  (white)
  dp[3][1] = 1  (black)

Step 2: Process node 2 (has child 3)
  dp[2][0] = dp[3][0] + dp[3][1] = 1 + 1 = 2
            (if 2 is white, child 3 can be white or black)
  dp[2][1] = dp[3][0] = 1
            (if 2 is black, child 3 must be white)

Step 3: Process node 1 (has child 2)
  dp[1][0] = dp[2][0] + dp[2][1] = 2 + 1 = 3
            (if 1 is white, child 2 can be white or black)
  dp[1][1] = dp[2][0] = 2
            (if 1 is black, child 2 must be white)

Final answer: dp[1][0] + dp[1][1] = 3 + 2 = 5
```

### Visual Diagram

```
Tree:  1 --- 2 --- 3

Valid colorings (W=white, B=black):
  Node:   1   2   3
  -----   -   -   -
  1.      W   W   W   (all white)
  2.      W   W   B   (only 3 black)
  3.      W   B   W   (only 2 black)
  4.      B   W   W   (only 1 black)
  5.      B   W   B   (1 and 3 black, 2 white)

  Total: 5 valid colorings
```

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200005)

def solve():
 MOD = 10**9 + 7

 n = int(input())

 # Build adjacency list
 graph = defaultdict(list)
 for _ in range(n - 1):
  x, y = map(int, input().split())
  graph[x].append(y)
  graph[y].append(x)

 # dp[v][0] = ways with v white, dp[v][1] = ways with v black
 dp = [[1, 1] for _ in range(n + 1)]

 def dfs(v, parent):
  for child in graph[v]:
   if child == parent:
    continue
   dfs(child, v)

   # If v is white, child can be white or black
   dp[v][0] = dp[v][0] * (dp[child][0] + dp[child][1]) % MOD
   # If v is black, child must be white
   dp[v][1] = dp[v][1] * dp[child][0] % MOD

 dfs(1, -1)
 print((dp[1][0] + dp[1][1]) % MOD)

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N) | Visit each node once, O(1) work per edge |
| Space | O(N) | Adjacency list + DP array + recursion stack |

---

## Common Mistakes

### Mistake 1: Forgetting Modular Arithmetic

```python
# WRONG - overflow or wrong answer
dp[v][0] = dp[v][0] * (dp[child][0] + dp[child][1])

# CORRECT
dp[v][0] = dp[v][0] * (dp[child][0] + dp[child][1]) % MOD
```

**Problem:** Without modulo, values overflow (especially in C++) or become too large.
**Fix:** Apply modulo after every multiplication.

### Mistake 2: Not Skipping Parent in DFS

```python
# WRONG - infinite loop or wrong traversal
def dfs(v):
 for child in graph[v]:
  dfs(child)

# CORRECT
def dfs(v, parent):
 for child in graph[v]:
  if child == parent:
   continue
  dfs(child, v)
```

**Problem:** In an undirected tree, each edge appears twice. Without tracking parent, DFS goes back to parent.
**Fix:** Pass parent to DFS and skip it when iterating neighbors.

### Mistake 3: Wrong Transition Order

```python
# WRONG - using updated dp[v] values incorrectly
dp[v][0] = dp[child][0] + dp[child][1]  # Overwrites instead of multiplies

# CORRECT - multiply into existing value
dp[v][0] = dp[v][0] * (dp[child][0] + dp[child][1]) % MOD
```

**Problem:** Each child's contribution should multiply, not replace.
**Fix:** Initialize dp[v][0] = dp[v][1] = 1, then multiply for each child.

### Mistake 4: Recursion Limit (Python)

```python
# WRONG - default recursion limit is ~1000
def dfs(v, parent):
 ...

# CORRECT - increase limit for N up to 10^5
import sys
sys.setrecursionlimit(200005)
```

**Problem:** Python's default recursion limit causes RuntimeError on deep trees.
**Fix:** Set recursion limit to at least 2*N.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | N=1, no edges | 2 | Can be white or black |
| Two nodes | N=2, edge (1,2) | 3 | WW, WB, BW (not BB) |
| Star graph | Center with k leaves | 2^k + 1 | Center white: 2^k ways; Center black: 1 way |
| Path graph | N nodes in a line | Fibonacci-like | dp grows like Fibonacci sequence |
| Complete binary tree | Balanced tree | Large count | Test modular arithmetic correctness |

---

## When to Use This Pattern

### Use Tree DP with Binary State When:
- Problem involves trees with constraints between adjacent nodes
- Each node has two possible states (selected/not, colored/not, etc.)
- Subtree results can be combined independently
- Counting or optimizing over all valid configurations

### Don't Use When:
- Graph has cycles (not a tree) - use different DP or graph algorithms
- State depends on non-adjacent nodes - may need different formulation
- Problem requires backtracking to find actual configuration - need to store choices

### Pattern Recognition Checklist:
- [ ] Is the structure a tree? -> **Tree DP is likely applicable**
- [ ] Does each node have binary choice? -> **Use dp[node][0/1] states**
- [ ] Are subtrees independent given parent's state? -> **Multiply children's contributions**
- [ ] Is it a counting problem with modulo? -> **Apply modular arithmetic throughout**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [AtCoder DP-G: Longest Path](https://atcoder.jp/contests/dp/tasks/dp_g) | Basic tree/DAG DP |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES Tree Matching](https://cses.fi/problemset/task/1130) | Maximize matched edges instead of counting |
| [CSES Tree Distances I](https://cses.fi/problemset/task/1132) | Distance computation, not counting |
| [AtCoder DP-V: Subtree](https://atcoder.jp/contests/dp/tasks/dp_v) | Re-rooting technique extension |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES Finding a Centroid](https://cses.fi/problemset/task/1648) | Centroid decomposition |
| [AtCoder DP-V: Subtree](https://atcoder.jp/contests/dp/tasks/dp_v) | Rerooting DP for all roots |

---

## Key Takeaways

1. **The Core Idea:** Track two DP values per node (white/black count), combine children by multiplication
2. **Time Optimization:** Bottom-up DFS processes each node once, achieving O(N) time
3. **Space Trade-off:** O(N) space for DP array, enabling O(1) combination per child
4. **Pattern:** Binary-state Tree DP with multiplicative combination of independent subtrees

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why children's contributions are multiplied (independence)
- [ ] Extend to weighted version (maximum weight independent set)
- [ ] Implement iterative version using topological order on rooted tree

---

## Additional Resources

- [CP-Algorithms: Tree DP](https://cp-algorithms.com/graph/tree_dp.html)
- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp)
- [CSES Tree Matching](https://cses.fi/problemset/task/1130) - Tree DP problem
