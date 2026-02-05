---
layout: simple
title: "Company Queries I - Tree Algorithms Problem"
permalink: /problem_soulutions/tree_algorithms/company_queries_i_analysis
difficulty: Medium
tags: [binary-lifting, tree, ancestor-queries, preprocessing]
---

# Company Queries I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES Problem 1687](https://cses.fi/problemset/task/1687) |
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Binary Lifting |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement the binary lifting technique for ancestor queries
- [ ] Preprocess a tree to answer k-th ancestor queries in O(log k) time
- [ ] Recognize when binary lifting is applicable (any problem requiring "jumping" k steps)
- [ ] Build sparse tables for tree structures

---

## Problem Statement

**Problem:** A company has n employees numbered 1 to n, where employee 1 is the general director (root). Each employee except the director has a direct boss. Given q queries, for each query (x, k), find the k-th ancestor of employee x (i.e., the boss k levels above x).

**Input:**
- Line 1: Two integers n and q (number of employees and queries)
- Line 2: n-1 integers describing the boss of employees 2, 3, ..., n
- Next q lines: Two integers x and k (employee and ancestor level)

**Output:**
- For each query, print the k-th ancestor of x, or -1 if it doesn't exist

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 1 <= x <= n
- 1 <= k <= n

### Example

```
Input:
5 3
1 1 2 2
4 1
4 2
4 3

Output:
2
1
-1
```

**Explanation:**
- Employee 4's parent (1st ancestor) is employee 2
- Employee 4's grandparent (2nd ancestor) is employee 1
- Employee 4 has no 3rd ancestor (only 2 levels above), so output -1

The company hierarchy:
```
        1 (Director)
       / \
      2   3
     / \
    4   5
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently find the k-th ancestor when k can be as large as n?

If we traverse parent-by-parent, each query takes O(k) time. With q queries and k up to n, this gives O(q * n) = O(n^2) which is too slow for n = 2 x 10^5.

### The Binary Lifting Insight

**Key Idea:** Any positive integer k can be represented as a sum of powers of 2.

For example: 13 = 8 + 4 + 1 = 2^3 + 2^2 + 2^0

Instead of jumping 1 step at a time, we can jump in powers of 2:
- Jump 8 steps, then 4 steps, then 1 step to reach the 13th ancestor

This requires precomputing "jump tables" where `up[node][j]` = the 2^j-th ancestor of node.

### Breaking Down the Problem

1. **What are we looking for?** The k-th ancestor of a given node
2. **What information do we have?** The parent of each node
3. **What's the relationship?** k-th ancestor = (k-1)-th ancestor's parent

### Analogy

Think of binary lifting like an express elevator system:
- Regular stairs: Go up 1 floor at a time (slow)
- Express elevators: Jump 1, 2, 4, 8, 16... floors at once
- To reach floor 13: Take elevator +8, then +4, then +1

---

## Solution 1: Brute Force (Naive Parent Traversal)

### Idea

For each query, simply walk up the tree k times by following parent pointers.

### Algorithm

1. For query (x, k): Start at node x
2. Follow parent pointers k times
3. If we reach root before k steps, return -1
4. Otherwise, return the node we end up at

### Code

```python
def solve_brute_force(n, q, bosses, queries):
    """
    Brute force: walk up parent pointers k times.

    Time: O(q * n) - worst case O(n) per query
    Space: O(n)
    """
    # parent[i] = direct boss of employee i (1-indexed)
    parent = [0] * (n + 1)
    parent[1] = 0  # root has no parent
    for i in range(2, n + 1):
        parent[i] = bosses[i - 2]

    results = []
    for x, k in queries:
        current = x
        for _ in range(k):
            if current == 0:  # reached beyond root
                current = -1
                break
            current = parent[current]

        results.append(current if current != 0 else -1)

    return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query may traverse up to n nodes |
| Space | O(n) | Parent array storage |

### Why This Works (But Is Slow)

Correctness is obvious - we literally follow the definition. But with n, q up to 2 x 10^5, this gives 4 x 10^10 operations, far too slow.

---

## Solution 2: Binary Lifting (Optimal)

### Key Insight

> **The Trick:** Precompute `up[x][j]` = the 2^j-th ancestor of x, then decompose any k into powers of 2.

### State Definition

| State | Meaning |
|-------|---------|
| `up[x][j]` | The (2^j)-th ancestor of node x, or 0 if it doesn't exist |

**In plain English:** `up[x][j]` tells us who is exactly 2^j levels above employee x.

### State Transition (Building the Table)

```
up[x][0] = parent[x]                    # 2^0 = 1st ancestor (direct parent)
up[x][j] = up[up[x][j-1]][j-1]          # 2^j-th ancestor = 2^(j-1)-th ancestor of 2^(j-1)-th ancestor
```

**Why?** To go 2^j steps up, first go 2^(j-1) steps, then another 2^(j-1) steps.
- Example: 8th ancestor = 4th ancestor's 4th ancestor

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `up[x][0]` | parent[x] | Direct parent is 2^0 = 1st ancestor |
| `up[1][j]` | 0 (for all j) | Root has no ancestors |

### Algorithm

**Preprocessing:**
1. Initialize `up[x][0] = parent[x]` for all nodes
2. For j from 1 to LOG: `up[x][j] = up[up[x][j-1]][j-1]`

**Query (x, k):**
1. For each bit position j where bit j is set in k:
   - Jump from current node to its 2^j-th ancestor
2. If we ever reach node 0, return -1
3. Return final node

### Dry Run Example

Let's trace through finding the 5th ancestor of node 6 in this tree:

```
Tree structure (parent array for nodes 2-8: [1,1,2,2,3,3,4]):

            1
          /   \
         2     3
        / \   / \
       4   5 6   7
      /
     8

Binary lifting table (LOG = 3, covering up to 2^3 = 8 ancestors):

Node | up[x][0] | up[x][1] | up[x][2]
     |  (2^0=1) | (2^1=2)  | (2^2=4)
-----|----------|----------|----------
  1  |    0     |    0     |    0
  2  |    1     |    0     |    0
  3  |    1     |    0     |    0
  4  |    2     |    1     |    0
  5  |    2     |    1     |    0
  6  |    3     |    1     |    0
  7  |    3     |    1     |    0
  8  |    4     |    2     |    1

Query: Find 5th ancestor of node 6
  k = 5 = 101 in binary = 2^2 + 2^0

Step 1: k = 5, check bit 0 (set)
  - Jump 2^0 = 1 step: node 6 -> up[6][0] = 3
  - current = 3

Step 2: k = 5, check bit 1 (not set)
  - No jump

Step 3: k = 5, check bit 2 (set)
  - Jump 2^2 = 4 steps: node 3 -> up[3][2] = 0
  - current = 0

Result: 0 means no ancestor exists, return -1
```

**Another example: Find 2nd ancestor of node 8**
```
k = 2 = 10 in binary = 2^1

Step 1: k = 2, check bit 0 (not set)
  - No jump, current = 8

Step 2: k = 2, check bit 1 (set)
  - Jump 2^1 = 2 steps: node 8 -> up[8][1] = 2
  - current = 2

Result: 2 (correct: 8's parent is 4, 4's parent is 2)
```

### Visual Diagram

```
Binary Lifting Table Construction:

        1 (root)
       / \
      2   3          up[x][0]: direct parent
     / \   \         up[x][1]: grandparent (parent's parent)
    4   5   6        up[x][2]: great-great-grandparent

For node 4:
  up[4][0] = 2       (parent)
  up[4][1] = up[up[4][0]][0] = up[2][0] = 1  (grandparent)
  up[4][2] = up[up[4][1]][1] = up[1][1] = 0  (no 4th ancestor)

Query k=3 from node 4:
  3 = 11 binary = 2^1 + 2^0

  Start: node 4
  Bit 0 set: jump 2^0 -> up[4][0] = 2
  Bit 1 set: jump 2^1 -> up[2][1] = 0

  Result: -1 (no 3rd ancestor)
```

### Code

**Python Implementation:**

```python
import sys
from typing import List, Tuple
sys.setrecursionlimit(300000)

def solve_binary_lifting(n: int, q: int, bosses: List[int], queries: List[Tuple[int, int]]) -> List[int]:
    """
    Binary lifting solution for k-th ancestor queries.

    Time: O((n + q) * log n) - O(n log n) preprocessing, O(log n) per query
    Space: O(n * log n) - binary lifting table
    """
    LOG = 18  # log2(2 * 10^5) < 18

    # up[x][j] = 2^j-th ancestor of node x (0 means no ancestor)
    up = [[0] * LOG for _ in range(n + 1)]

    # Base case: up[x][0] = parent[x]
    up[1][0] = 0  # root has no parent
    for i in range(2, n + 1):
        up[i][0] = bosses[i - 2]

    # Build table: up[x][j] = up[up[x][j-1]][j-1]
    for j in range(1, LOG):
        for x in range(1, n + 1):
            if up[x][j - 1] != 0:
                up[x][j] = up[up[x][j - 1]][j - 1]

    # Answer queries
    results = []
    for x, k in queries:
        current = x
        for j in range(LOG):
            if current == 0:
                break
            if k & (1 << j):  # if bit j is set in k
                current = up[current][j]

        results.append(current if current != 0 else -1)

    return results


def main():
    """Main function to read input and output results."""
    input_data = sys.stdin.read().split()
    idx = 0

    n, q = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2

    bosses = [int(input_data[idx + i]) for i in range(n - 1)]
    idx += n - 1

    queries = []
    for _ in range(q):
        x, k = int(input_data[idx]), int(input_data[idx + 1])
        queries.append((x, k))
        idx += 2

    results = solve_binary_lifting(n, q, bosses, queries)
    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | O(n log n) preprocessing + O(log n) per query |
| Space | O(n log n) | Binary lifting table with n nodes and log n levels |

---

## Common Mistakes

### Mistake 1: Wrong Table Dimension

```python
# WRONG: LOG too small
LOG = 10  # Only handles k up to 1024

# CORRECT: LOG should cover max possible depth
LOG = 18  # Handles k up to 2^18 > 2 * 10^5
```

**Problem:** If LOG is too small, queries with large k will give wrong answers.
**Fix:** Use LOG = ceil(log2(n)) + 1, or safely use LOG = 20 for n <= 10^6.

### Mistake 2: Off-by-One in Parent Array

```python
# WRONG: Using 0-indexed parent array with 1-indexed nodes
for i in range(2, n + 1):
    up[i][0] = bosses[i - 1]  # Index error!

# CORRECT: bosses has n-1 elements for nodes 2 to n
for i in range(2, n + 1):
    up[i][0] = bosses[i - 2]  # bosses[0] is parent of node 2
```

**Problem:** Input gives parents for nodes 2, 3, ..., n in order.
**Fix:** Carefully handle the offset between node index and array index.

### Mistake 3: Not Handling "No Ancestor" Case

```python
# WRONG: Not checking for 0 during traversal
for j in range(LOG):
    if k & (1 << j):
        current = up[current][j]
# May access up[0][j] which is undefined

# CORRECT: Stop when we reach 0
for j in range(LOG):
    if current == 0:
        break
    if k & (1 << j):
        current = up[current][j]
```

**Problem:** Once current becomes 0 (no ancestor), we must stop.
**Fix:** Add early termination check.

### Mistake 4: Confusing 0 and -1

```python
# WRONG: Returning 0 as "no ancestor"
return current  # 0 is ambiguous if node 0 existed

# CORRECT: Convert 0 to -1 for output
return current if current != 0 else -1
```

**Problem:** We use 0 internally to mean "no ancestor", but output expects -1.
**Fix:** Translate internal representation to expected output format.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Root has no k-th ancestor | x=1, k=1 | -1 | Root has no parent |
| k = 0 | x=5, k=0 | 5 | 0th ancestor is the node itself (handle if required) |
| k > depth of node | x=4, k=10 (depth=2) | -1 | Not enough ancestors |
| k exactly equals depth | x=4, k=2 (root at depth 2) | 1 | Returns the root |
| Linear tree (chain) | n nodes in chain, k=n-1 | 1 | Maximum depth case |
| Star tree | All nodes connect to root | x=i, k=2 | -1 for any k >= 2 |

---

## When to Use This Pattern

### Use Binary Lifting When:
- You need to find k-th ancestors for multiple queries
- k can be large (close to n), making O(k) per query too slow
- You need to preprocess once and answer many queries
- Combined with LCA algorithms (Lowest Common Ancestor)
- Path queries on trees that require "jumping" to ancestors

### Don't Use When:
- Only a few queries with small k (naive is simpler)
- The tree changes dynamically (need Link-Cut Trees instead)
- You only need parent or immediate ancestors (direct array lookup)
- Memory is extremely constrained (table uses O(n log n) space)

### Pattern Recognition Checklist:
- [ ] Need to find k-th ancestor? -> **Binary Lifting**
- [ ] Need LCA of two nodes? -> **Binary Lifting + depth comparison**
- [ ] Need to query path between two nodes? -> **Binary Lifting to LCA + path processing**
- [ ] Multiple ancestor queries on static tree? -> **Definitely Binary Lifting**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subordinates (CSES 1674)](https://cses.fi/problemset/task/1674) | Basic tree traversal and subtree size |
| [Tree Distances I (CSES 1132)](https://cses.fi/problemset/task/1132) | Understanding tree depth and distance |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Company Queries II (CSES 1688)](https://cses.fi/problemset/task/1688) | Uses binary lifting for LCA queries |
| [Distance Queries (CSES 1135)](https://cses.fi/problemset/task/1135) | Combines LCA with path distance |
| [Kth Ancestor of Tree Node (LC 1483)](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) | Same problem on LeetCode |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Path Queries II (CSES 1138)](https://cses.fi/problemset/task/1138) | Binary lifting with segment trees on paths |
| [Planets Queries II (CSES 1160)](https://cses.fi/problemset/task/1160) | Binary lifting on functional graphs |
| [Cycle Finding (CSES 1751)](https://cses.fi/problemset/task/1751) | Detecting cycles using similar jumping technique |

---

## Key Takeaways

1. **The Core Idea:** Precompute 2^j-th ancestors to answer any k-th ancestor query by decomposing k into powers of 2.

2. **Time Optimization:** Reduced from O(k) per query to O(log k) by leveraging binary representation.

3. **Space Trade-off:** Uses O(n log n) extra space to store the jump table, which enables O(log n) queries.

4. **Pattern:** Binary lifting is a "sparse table" technique for trees, analogous to how sparse tables work for range queries on arrays.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build the binary lifting table correctly with proper base cases
- [ ] Query k-th ancestor by iterating through bits of k
- [ ] Explain why `up[x][j] = up[up[x][j-1]][j-1]` works
- [ ] Handle edge cases (root queries, k > depth)
- [ ] Extend this to LCA computation (Company Queries II)
- [ ] Implement in both Python and C++ within 15 minutes

---

## Additional Resources

- [CP-Algorithms: Binary Lifting](https://cp-algorithms.com/graph/lca_binary_lifting.html)
- [CSES Company Queries I](https://cses.fi/problemset/task/1687) - K-th ancestor query
- [Competitive Programmer's Handbook - Chapter 18](https://cses.fi/book/book.pdf)
