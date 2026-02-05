---
layout: simple
title: "Subordinates - Tree DP Problem"
permalink: /problem_soulutions/tree_algorithms/subordinates_analysis
difficulty: Easy
tags: [tree-dp, dfs, subtree-counting]
prerequisites: [basic-tree-traversal, dfs]
---

# Subordinates

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Tree DP |
| **Time Limit** | 1 second |
| **Key Technique** | DFS / Subtree Counting |
| **CSES Link** | [Subordinates](https://cses.fi/problemset/task/1674) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how to count nodes in subtrees using DFS
- [ ] Apply post-order traversal for bottom-up tree DP
- [ ] Build and traverse rooted trees from parent arrays
- [ ] Recognize the fundamental tree DP pattern: `dp[node] = 1 + sum(dp[children])`

---

## Problem Statement

**Problem:** Given a company with n employees (numbered 1 to n), where employee 1 is the general director and every other employee has a direct boss, find the number of subordinates for each employee.

**Input:**
- Line 1: Integer n (number of employees)
- Line 2: n-1 integers, where the i-th integer is the boss of employee i+1

**Output:**
- n integers: the number of subordinates for each employee (employees in their subtree, not counting themselves)

**Constraints:**
- 1 <= n <= 2 x 10^5

### Example

```
Input:
5
1 1 2 2

Output:
4 2 0 0 0
```

**Explanation:**
```
Tree structure (employee hierarchy):
        1 (director)
       / \
      2   3
     / \
    4   5

Subordinate counts:
- Employee 1: 4 subordinates (2, 3, 4, 5)
- Employee 2: 2 subordinates (4, 5)
- Employee 3: 0 subordinates (leaf)
- Employee 4: 0 subordinates (leaf)
- Employee 5: 0 subordinates (leaf)
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count all nodes below a given node in a tree?

This is the most fundamental tree DP problem. The insight is that the subtree size of any node equals 1 (itself) plus the sum of subtree sizes of all its children. We use DFS to compute this bottom-up.

### Breaking Down the Problem

1. **What are we looking for?** The count of subordinates (subtree size - 1) for each node
2. **What information do we have?** Parent of each node (except root)
3. **What's the relationship?** `subordinates[node] = sum(subtree_size[child])` for all children

### Analogies

Think of this like counting all employees in a department: you count yourself plus everyone in each sub-department under you. You need to know the counts from below before you can compute your own count.

---

## Solution 1: Brute Force (DFS from each node)

### Idea

For each node, perform a separate DFS to count all nodes in its subtree.

### Algorithm

1. Build adjacency list from parent array
2. For each node 1 to n, run DFS counting reachable nodes
3. Subtract 1 (don't count the node itself)

### Code

```python
def solve_brute_force(n, parents):
    """
    Brute force: DFS from each node.

    Time: O(n^2)
    Space: O(n)
    """
    # Build adjacency list (children only)
    children = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        children[parents[i - 2]].append(i)

    def count_subtree(node):
        count = 1
        for child in children[node]:
            count += count_subtree(child)
        return count

    result = []
    for i in range(1, n + 1):
        result.append(count_subtree(i) - 1)  # subtract self

    return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | DFS for each of n nodes |
| Space | O(n) | Recursion stack + adjacency list |

### Why This Works (But Is Slow)

Each DFS correctly counts all descendants, but we're recomputing the same subtrees multiple times. Node 1's DFS visits all nodes, then node 2's DFS revisits its entire subtree, etc.

---

## Solution 2: Optimal Solution (Single DFS)

### Key Insight

> **The Trick:** Use post-order DFS to compute subtree sizes bottom-up in a single pass.

When we return from a child's DFS call, we already know its subtree size. We just accumulate these values.

### DP State Definition

| State | Meaning |
|-------|---------|
| `subtree[v]` | Total number of nodes in the subtree rooted at v (including v) |

**In plain English:** `subtree[v]` counts v itself plus all descendants.

### State Transition

```
subtree[v] = 1 + sum(subtree[c]) for all children c of v
```

**Why?** A node's subtree contains itself (1) plus all nodes in each child's subtree.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| Leaf node | 1 | Only contains itself |

### Algorithm

1. Build children list from parent array
2. Run single DFS from root (node 1)
3. In post-order: `subtree[node] = 1 + sum(subtree[children])`
4. Output `subtree[i] - 1` for each node (subordinates = subtree - self)

### Dry Run Example

Let's trace through with `n = 5, parents = [1, 1, 2, 2]`:

```
Tree structure:
      1
     / \
    2   3
   / \
  4   5

Children lists:
  1 -> [2, 3]
  2 -> [4, 5]
  3 -> []
  4 -> []
  5 -> []

DFS traversal (post-order processing):

Call dfs(1):
  Call dfs(2):
    Call dfs(4):
      No children, return subtree[4] = 1
    Call dfs(5):
      No children, return subtree[5] = 1
    subtree[2] = 1 + subtree[4] + subtree[5] = 1 + 1 + 1 = 3
  Call dfs(3):
    No children, return subtree[3] = 1
  subtree[1] = 1 + subtree[2] + subtree[3] = 1 + 3 + 1 = 5

Final subtree sizes: [5, 3, 1, 1, 1]
Subordinates (subtract 1): [4, 2, 0, 0, 0]
```

### Visual Diagram

```
Post-order processing (bottom-up):

        1 [5]        <- Process last: 1 + 3 + 1 = 5
       / \
      2   3          <- subtree[2]=3, subtree[3]=1
     [3] [1]
     / \
    4   5            <- Process first: both return 1
   [1] [1]

Arrows show computation order (leaves -> root)
```

### Code (Python)

```python
import sys
from collections import defaultdict

def solve(n, parents):
    """
    Optimal solution using single post-order DFS.

    Time: O(n) - each node visited once
    Space: O(n) - recursion stack + children list
    """
    # Build children list
    children = defaultdict(list)
    for i in range(2, n + 1):
        boss = parents[i - 2]
        children[boss].append(i)

    subtree = [0] * (n + 1)

    def dfs(node):
        subtree[node] = 1  # count self
        for child in children[node]:
            dfs(child)
            subtree[node] += subtree[child]

    sys.setrecursionlimit(300000)
    dfs(1)

    # Output subordinates (subtree size - 1)
    return [subtree[i] - 1 for i in range(1, n + 1)]


def main():
    n = int(input())
    if n == 1:
        print(0)
        return
    parents = list(map(int, input().split()))
    result = solve(n, parents)
    print(' '.join(map(str, result)))


if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Each node visited exactly once |
| Space | O(n) | Children list + recursion stack (worst case: linear tree) |

---

## Common Mistakes

### Mistake 1: Forgetting to Subtract Self

```python
# WRONG - outputs subtree size, not subordinate count
print(subtree[i])

# CORRECT - subordinates = subtree size - 1
print(subtree[i] - 1)
```

**Problem:** The problem asks for subordinates (employees below), not total subtree size.
**Fix:** Always subtract 1 from subtree size.

### Mistake 2: Stack Overflow on Deep Trees

```python
# WRONG - default recursion limit is ~1000
def dfs(node):
    ...
```

**Problem:** Python's default recursion limit causes stack overflow on deep trees.
**Fix:** Add `sys.setrecursionlimit(300000)` or use iterative DFS.

### Mistake 3: Wrong Parent Indexing

```python
# WRONG - parents array is 0-indexed for employees 2 to n
boss = parents[i]  # off by one!

# CORRECT
boss = parents[i - 2]  # employee i's boss is at index i-2
```

**Problem:** The input gives bosses for employees 2, 3, ..., n (not 1, 2, ..., n-1).
**Fix:** Employee i+1's boss is at index i-1 in 0-indexed array.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1 | `0` | Director has no subordinates |
| Linear chain | 1->2->3->4 | `3 2 1 0` | Each node has all below as subordinates |
| Star tree | 1->(2,3,4,5) | `4 0 0 0 0` | Only root has subordinates |
| Binary tree | Balanced | Powers of 2 pattern | Subtrees double at each level up |
| Maximum n | n=200000 | Must run in <1s | Test time complexity |

---

## When to Use This Pattern

### Use This Approach When:
- Computing aggregate values over subtrees (size, sum, max, etc.)
- Problems involving hierarchical structures (org charts, file systems)
- Bottom-up computation where children's values determine parent's value

### Don't Use When:
- The tree is given as edges (not parent pointers) - need to root it first
- You need top-down information (use pre-order DFS instead)
- Queries on arbitrary tree paths (use LCA or tree decomposition)

### Pattern Recognition Checklist:
- [ ] Each node's answer depends on its children's answers? -> **Post-order DFS**
- [ ] Tree is rooted with parent pointers? -> **Direct children list construction**
- [ ] Need subtree aggregates? -> **This exact pattern**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| Basic DFS traversal | Understand tree traversal fundamentals |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Find farthest node from each node |
| [Tree Distances II](https://cses.fi/problemset/task/1133) | Sum of distances to all other nodes |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Company Queries I](https://cses.fi/problemset/task/1687) | k-th ancestor queries (binary lifting) |
| [Company Queries II](https://cses.fi/problemset/task/1688) | LCA queries |
| [Distance Queries](https://cses.fi/problemset/task/1135) | Distance between arbitrary nodes |

---

## Key Takeaways

1. **The Core Idea:** Subtree size = 1 + sum of children's subtree sizes
2. **Time Optimization:** Single DFS instead of DFS from each node (O(n) vs O(n^2))
3. **Space Trade-off:** O(n) space for children list enables O(n) time
4. **Pattern:** This is the foundational tree DP pattern - master it before moving to harder tree problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why post-order DFS works for this problem
- [ ] Handle the recursion limit issue in Python
- [ ] Implement in both Python and C++ in under 10 minutes

---

## Additional Resources

- [CP-Algorithms: Tree DP](https://cp-algorithms.com/graph/tree_dp.html)
- [CSES Subordinates](https://cses.fi/problemset/task/1674) - Count subtree nodes
