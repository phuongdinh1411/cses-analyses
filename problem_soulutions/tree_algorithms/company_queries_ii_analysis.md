---
layout: simple
title: "Company Queries II - LCA with Binary Lifting"
permalink: /problem_soulutions/tree_algorithms/company_queries_ii_analysis
difficulty: Medium
tags: [tree, lca, binary-lifting, preprocessing]
prerequisites: [company_queries_i_analysis]
---

# Company Queries II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Binary Lifting for LCA |
| **CSES Link** | [Company Queries II](https://cses.fi/problemset/task/1688) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement the Lowest Common Ancestor (LCA) algorithm
- [ ] Use binary lifting to preprocess ancestor information in O(n log n)
- [ ] Answer LCA queries in O(log n) time
- [ ] Apply depth equalization as a preprocessing step for LCA

---

## Problem Statement

**Problem:** Given a company hierarchy (rooted tree) with n employees, answer q queries asking for the lowest common boss of two employees.

**Input:**
- Line 1: Two integers n and q (number of employees, number of queries)
- Line 2: n-1 integers describing the boss of employees 2, 3, ..., n (employee 1 is the general director)
- Next q lines: Two integers a and b (find LCA of employees a and b)

**Output:**
- For each query, print the lowest common boss of employees a and b

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 1 <= a, b <= n

### Example

```
Input:
5 3
1 1 2 2
4 5
2 3
1 4

Output:
2
1
1
```

**Explanation:**
- Query (4, 5): Both 4 and 5 report to employee 2, so LCA = 2
- Query (2, 3): Both report directly to employee 1, so LCA = 1
- Query (1, 4): Employee 1 is an ancestor of 4, so LCA = 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we find the nearest common ancestor of two nodes efficiently?

The LCA of two nodes is the deepest node that is an ancestor of both. A naive approach traverses up from both nodes (O(n) per query). Binary lifting allows jumps in powers of 2, reducing query time to O(log n).

### The Binary Lifting Insight

Think of it like climbing floors: instead of one step at a time, use an elevator that jumps 8, 4, 2, or 1 floors. To climb 13 floors (13 = 8 + 4 + 1), take three jumps instead of thirteen steps.

```
Tree structure for the example:
        1 (CEO)
       / \
      2   3
     / \
    4   5

Depths: node 1 = 0, nodes 2,3 = 1, nodes 4,5 = 2
```

---

## Solution 1: Brute Force

### Algorithm

1. Compute depth of all nodes
2. For query (a, b), bring the deeper node up to match depths
3. Move both nodes up one step at a time until they meet

### Code

```python
def solve_brute_force(n, parents, queries):
    """
    Time: O(q * n) - each query may traverse O(n) ancestors
    Space: O(n)
    """
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = parents[i - 2]

    depth = [0] * (n + 1)
    for i in range(2, n + 1):
        node = i
        while node != 0:
            depth[i] += 1
            node = parent[node]
        depth[i] -= 1

    def lca(a, b):
        while depth[a] > depth[b]: a = parent[a]
        while depth[b] > depth[a]: b = parent[b]
        while a != b:
            a, b = parent[a], parent[b]
        return a

    return [lca(a, b) for a, b in queries]
```

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query traverses up to O(n) ancestors |
| Space | O(n) | Parent and depth arrays |

---

## Solution 2: Optimal - Binary Lifting

### Key Insight

> **The Trick:** Precompute the 2^k-th ancestor for every node. Any jump can be decomposed into powers of 2.

### Data Structure

| Array | Meaning |
|-------|---------|
| `up[k][node]` | The 2^k-th ancestor of node (0 if doesn't exist) |
| `depth[node]` | Distance from node to root |

### LCA Algorithm

1. **Equalize depths:** bring the deeper node up using binary jumps
2. **Check equality:** if nodes are equal, return (one is ancestor of other)
3. **Binary search for LCA:** jump both nodes up together, stopping just before they meet
4. **Return parent:** the LCA is the parent of where they stopped

### Dry Run Example

```
Tree:       1 (depth 0)
           / \
          2   3 (depth 1)
         / \
        4   5 (depth 2)

Binary lifting table:
up[0][1..5] = [0, 1, 1, 2, 2]  (direct parents)
up[1][1..5] = [0, 0, 0, 1, 1]  (2nd ancestors)

Query: LCA(4, 5)
  depth[4] = depth[5] = 2 (already equal)
  k=1: up[1][4]=1, up[1][5]=1 (equal, don't jump)
  k=0: up[0][4]=2, up[0][5]=2 (equal, don't jump)
  Return up[0][4] = 2
```

### Code (Python)

```python
import sys
from collections import deque
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    if n == 1:
        for _ in range(q): print(1)
        return

    parents = list(map(int, input().split()))
    LOG = 18
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        parent[i] = parents[i - 2]

    # Compute depths using BFS
    depth = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        children[parent[i]].append(i)

    queue = deque([1])
    while queue:
        node = queue.popleft()
        for child in children[node]:
            depth[child] = depth[node] + 1
            queue.append(child)

    # Build binary lifting table
    up = [[0] * (n + 1) for _ in range(LOG)]
    for i in range(1, n + 1):
        up[0][i] = parent[i]
    for k in range(1, LOG):
        for i in range(1, n + 1):
            up[k][i] = up[k-1][up[k-1][i]]

    def lca(a, b):
        if depth[a] < depth[b]: a, b = b, a
        diff = depth[a] - depth[b]
        for k in range(LOG):
            if diff & (1 << k): a = up[k][a]
        if a == b: return a
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a, b = up[k][a], up[k][b]
        return up[0][a]

    results = []
    for _ in range(q):
        a, b = map(int, input().split())
        results.append(str(lca(a, b)))
    print('\n'.join(results))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | O(n log n) preprocessing, O(log n) per query |
| Space | O(n log n) | Binary lifting table |

---

## Common Mistakes

### Mistake 1: Wrong Loop Order

```python
# WRONG - checking from k=0 to LOG-1
for k in range(LOG):
    if up[k][a] != up[k][b]:
        a, b = up[k][a], up[k][b]
```

**Problem:** Must make largest jumps first that don't overshoot the LCA.
**Fix:** Iterate from LOG-1 down to 0.

### Mistake 2: Missing Ancestor Check

```python
# WRONG - missing early return after depth equalization
diff = depth[a] - depth[b]
for k in range(LOG):
    if diff & (1 << k): a = up[k][a]
# Should check: if a == b: return a
```

**Fix:** Add `if a == b: return a` after depth equalization.

### Mistake 3: LOG Too Small

```python
LOG = 10  # WRONG - only handles n up to 1024
```

**Fix:** For n = 2 x 10^5, use LOG = 18 (2^18 = 262144 > 200000).

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Same node | LCA(3, 3) | 3 | Node is its own LCA |
| One is ancestor | LCA(1, 5) | 1 | Root is ancestor of all |
| Siblings | LCA(4, 5) | 2 | Direct parent is LCA |
| Deep tree | Chain of n nodes | Varies | Tests binary lifting efficiency |
| Star tree | All connect to root | 1 | LCA is always root |

---

## When to Use This Pattern

### Use Binary Lifting LCA When:
- Need to answer multiple LCA queries efficiently
- Tree is static (no structural changes)
- Also need k-th ancestor queries (Company Queries I)

### Don't Use When:
- Only one or few LCA queries (brute force is simpler)
- Tree structure changes dynamically (use Link-Cut Trees)
- Memory is very constrained (consider Euler tour + sparse table)

### Pattern Recognition:
- [ ] Finding common ancestor of two nodes? --> **Binary Lifting LCA**
- [ ] Need distance between two nodes? --> **LCA + depths**: `depth[a] + depth[b] - 2*depth[lca(a,b)]`
- [ ] Path queries on tree? --> **Often involves LCA**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Company Queries I](https://cses.fi/problemset/task/1687) | Learn binary lifting for k-th ancestor first |
| [Subordinates](https://cses.fi/problemset/task/1674) | Basic tree DFS and subtree concepts |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Distance Queries](https://cses.fi/problemset/task/1135) | Uses LCA to compute tree distances |
| [Counting Paths](https://cses.fi/problemset/task/1136) | LCA + difference arrays on paths |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Path Queries II](https://cses.fi/problemset/task/2134) | LCA + Heavy-Light Decomposition |
| [LCA (LeetCode)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Different tree representation |

---

## Key Takeaways

1. **Core Idea:** Precompute 2^k ancestors to enable O(log n) jumps up the tree
2. **Time Optimization:** From O(n) per query to O(log n) via binary decomposition
3. **Space Trade-off:** O(n log n) extra space for the binary lifting table
4. **Pattern:** Binary lifting is fundamental for many tree path problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement binary lifting table construction from scratch
- [ ] Explain why we iterate k from LOG-1 to 0 in the LCA step
- [ ] Derive the space and time complexity
- [ ] Extend to compute distance: `depth[a] + depth[b] - 2*depth[lca(a,b)]`

---

## Additional Resources

- [CP-Algorithms: LCA with Binary Lifting](https://cp-algorithms.com/graph/lca_binary_lifting.html)
- [CSES Company Queries II](https://cses.fi/problemset/task/1688) - LCA queries
