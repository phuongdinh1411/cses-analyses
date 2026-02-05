---
layout: simple
title: "Tree Traversals - Tree Algorithm"
permalink: /problem_soulutions/advanced_graph_problems/tree_traversals_analysis
difficulty: Medium
tags: [tree, dfs, recursion, binary-tree]
---

# Tree Traversals

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1674](https://cses.fi/problemset/task/1674) |
| **Difficulty** | Medium |
| **Category** | Tree Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | DFS, Recursion, Tree Reconstruction |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the three main tree traversal orders (preorder, inorder, postorder)
- [ ] Reconstruct a binary tree from two traversal sequences
- [ ] Implement recursive and iterative tree traversal algorithms
- [ ] Convert between different tree representations

---

## Problem Statement

**Problem:** You are given a rooted tree with n nodes. Your task is to determine the subtree sizes for each node.

**Input:**
- Line 1: Integer n (number of nodes)
- Line 2: For each node 2, 3, ..., n, its parent

**Output:**
- n integers: the subtree size for each node

**Constraints:**
- 1 <= n <= 2 * 10^5

### Example

```
Input:
5
1 1 2 2

Output:
5 3 1 1 1
```

**Explanation:**
- Node 1 is the root with subtree size 5 (all nodes)
- Node 2 has children 4, 5, so subtree size is 3
- Nodes 3, 4, 5 are leaves with subtree size 1

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently compute subtree sizes?

The key insight is that a node's subtree size equals 1 (itself) plus the sum of all its children's subtree sizes. This naturally leads to a bottom-up DFS approach.

### Breaking Down the Problem

1. **What are we looking for?** Size of subtree rooted at each node
2. **What information do we have?** Parent of each node
3. **What's the relationship?** `subtree_size[node] = 1 + sum(subtree_size[child] for child in children)`

### Tree Traversal Types

```
       1
      / \
     2   3
    / \
   4   5

Preorder (Root-Left-Right):  1, 2, 4, 5, 3
Inorder (Left-Root-Right):   4, 2, 5, 1, 3
Postorder (Left-Right-Root): 4, 5, 2, 3, 1
```

---

## Solution 1: Recursive DFS

### Idea

Build an adjacency list from parent information, then run DFS from the root. For each node, recursively compute the subtree size of all children and sum them up.

### Algorithm

1. Build adjacency list from parent array
2. Run DFS starting from root (node 1)
3. For each node, return 1 + sum of children's subtree sizes

### Code (Python)

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve():
    n = int(input())
    if n == 1:
        print(1)
        return

    parents = list(map(int, input().split()))

    # Build adjacency list
    children = defaultdict(list)
    for i, p in enumerate(parents):
        children[p].append(i + 2)  # Node i+2 has parent p

    subtree_size = [0] * (n + 1)

    def dfs(node):
        subtree_size[node] = 1
        for child in children[node]:
            dfs(child)
            subtree_size[node] += subtree_size[child]

    dfs(1)
    print(' '.join(map(str, subtree_size[1:])))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Visit each node exactly once |
| Space | O(n) | Adjacency list and recursion stack |

---

## Solution 2: Iterative DFS (Avoids Stack Overflow)

### Key Insight

> **The Trick:** Use an explicit stack with state tracking to avoid recursion limits

### Algorithm

1. Use a stack storing (node, visited_flag)
2. First visit: push node back with visited=true, then push all children
3. Second visit: compute subtree size from children

### Code (Python)

```python
def solve_iterative():
    n = int(input())
    if n == 1:
        print(1)
        return

    parents = list(map(int, input().split()))

    # Build adjacency list
    children = [[] for _ in range(n + 1)]
    for i, p in enumerate(parents):
        children[p].append(i + 2)

    subtree_size = [0] * (n + 1)

    # Iterative DFS using stack
    stack = [(1, False)]  # (node, is_processed)

    while stack:
        node, processed = stack.pop()

        if processed:
            # All children processed, compute subtree size
            subtree_size[node] = 1 + sum(subtree_size[c] for c in children[node])
        else:
            # Push self for processing after children
            stack.append((node, True))
            # Push children
            for child in children[node]:
                stack.append((child, False))

    print(' '.join(map(str, subtree_size[1:])))

solve_iterative()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Visit each node exactly twice |
| Space | O(n) | Explicit stack instead of call stack |

---

## Dry Run Example

Let's trace through with input `n = 5, parents = [1, 1, 2, 2]`:

```
Building tree:
  Node 2's parent is 1
  Node 3's parent is 1
  Node 4's parent is 2
  Node 5's parent is 2

Tree structure:
       1
      / \
     2   3
    / \
   4   5

DFS traversal (postorder for subtree sizes):
  Visit 4: size[4] = 1 (leaf)
  Visit 5: size[5] = 1 (leaf)
  Visit 2: size[2] = 1 + size[4] + size[5] = 1 + 1 + 1 = 3
  Visit 3: size[3] = 1 (leaf)
  Visit 1: size[1] = 1 + size[2] + size[3] = 1 + 3 + 1 = 5

Output: 5 3 1 1 1
```

---

## Common Mistakes

### Mistake 1: Not Increasing Recursion Limit (Python)

```python
# WRONG - will crash for deep trees
def dfs(node):
    ...

# CORRECT - increase recursion limit
import sys
sys.setrecursionlimit(300000)
```

**Problem:** Python's default recursion limit is ~1000
**Fix:** Set recursion limit or use iterative approach

### Mistake 2: Off-by-One in Node Indexing

```python
# WRONG - nodes are 1-indexed
for i, p in enumerate(parents):
    children[p].append(i)  # Should be i+2

# CORRECT
for i, p in enumerate(parents):
    children[p].append(i + 2)  # Node indices start at 2
```

**Problem:** The parent array describes nodes 2 through n
**Fix:** Remember that index i in parents corresponds to node i+2

### Mistake 3: Forgetting Base Case

```python
# WRONG - crashes when n=1
parents = list(map(int, input().split()))  # Empty input!

# CORRECT
if n == 1:
    print(1)
    return
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | `n=1` | `1` | Root is only node |
| Linear chain | `n=4, parents=[1,2,3]` | `4 3 2 1` | Each node has one child |
| Star graph | `n=4, parents=[1,1,1]` | `4 1 1 1` | Root connected to all |
| Binary tree | `n=7, parents=[1,1,2,2,3,3]` | `7 3 3 1 1 1 1` | Complete binary tree |

---

## When to Use This Pattern

### Use This Approach When:
- Computing properties that depend on subtree information
- Processing tree nodes in bottom-up order
- Need to aggregate information from children to parents

### Don't Use When:
- Information flows top-down (use BFS or preorder DFS)
- Need level-order processing (use BFS)
- Graph has cycles (it's not a tree)

### Pattern Recognition Checklist:
- [ ] Need subtree aggregation? --> **Postorder DFS**
- [ ] Need path from root? --> **Preorder DFS with state**
- [ ] Need level-by-level? --> **BFS**
- [ ] Need parent info at each node? --> **DFS with parent parameter**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subordinates](https://cses.fi/problemset/task/1674) | This exact problem |
| [Tree Matching](https://cses.fi/problemset/task/1130) | Basic tree DP |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Tree Diameter](https://cses.fi/problemset/task/1131) | Find longest path |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Compute max distance from each node |
| [Tree Distances II](https://cses.fi/problemset/task/1133) | Sum of distances from each node |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Company Queries I](https://cses.fi/problemset/task/1687) | Binary lifting for LCA |
| [Company Queries II](https://cses.fi/problemset/task/1688) | LCA queries |
| [Distance Queries](https://cses.fi/problemset/task/1135) | LCA + distance calculation |

---

## Key Takeaways

1. **The Core Idea:** Subtree properties are computed bottom-up using postorder traversal
2. **Time Optimization:** Single DFS pass achieves O(n) - no better complexity exists
3. **Space Trade-off:** Iterative DFS uses explicit stack, avoids recursion limits
4. **Pattern:** This is the foundation for tree DP problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement DFS for subtree size computation
- [ ] Convert between recursive and iterative DFS
- [ ] Identify postorder vs preorder traversal needs
- [ ] Handle edge cases (single node, linear chain)
- [ ] Solve in under 10 minutes

---

## Additional Resources

- [CP-Algorithms: Tree Algorithms](https://cp-algorithms.com/graph/tree-oi.html)
- [CSES Tree Traversals](https://cses.fi/problemset/task/1702) - Reconstruct tree from traversals
- [Competitive Programmer's Handbook - Tree Algorithms](https://cses.fi/book/book.pdf)
