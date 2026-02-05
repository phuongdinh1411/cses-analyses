---
layout: simple
title: "Tree Traversals - Counting Problem"
permalink: /problem_soulutions/counting_problems/tree_traversals_analysis
difficulty: Hard
tags: [counting, combinatorics, binary-tree, catalan-numbers, dp]
---

# Tree Traversals (Counting)

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1674](https://cses.fi/problemset/task/1674) |
| **Difficulty** | Hard |
| **Category** | Counting / Combinatorics |
| **Time Limit** | 1 second |
| **Key Technique** | Catalan Numbers, Tree DP, Factorial Counting |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how tree structure constrains traversal orderings
- [ ] Apply Catalan numbers to count valid binary tree configurations
- [ ] Use factorial counting for sibling permutations in rooted trees
- [ ] Implement modular arithmetic for large counting results

---

## Problem Statement

**Problem:** Given a rooted tree structure, count the number of distinct traversal orderings possible, or given traversal sequences, count how many unique trees produce them.

**Input:**
- Line 1: Integer n (number of nodes)
- Following lines: Tree structure (edges or parent array)

**Output:**
- Number of distinct traversal orderings modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 2 * 10^5

### Example

```
Input:
5
1 1 2 2

Tree Structure:
       1
      / \
     2   3
    / \
   4   5

Output:
4
```

**Explanation:** Node 1 has 2 children (2, 3) that can be visited in 2! = 2 orders. Node 2 has 2 children (4, 5) that can be visited in 2! = 2 orders. Total: 2 * 2 = 4 distinct traversals.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What determines the number of valid traversal orderings for a tree?

The number of traversal orderings depends on how many ways we can order the children of each node. For each node with k children, there are k! ways to arrange them.

### Breaking Down the Problem

1. **What are we looking for?** Total distinct DFS orderings of the tree
2. **What information do we have?** Tree structure with parent-child relationships
3. **What's the relationship?** Product of factorials of children counts

### Key Insight

For a rooted tree where children can be visited in any order:

```
Total orderings = Product of (children_count[v])! for all nodes v
```

### Visual Example

```
       1 (2 children)
      / \
     2   3 (0 children)
    / \
   4   5 (0 children each)

Node 1: 2 children -> 2! = 2 orderings
Node 2: 2 children -> 2! = 2 orderings
Node 3: 0 children -> 0! = 1 ordering
Total: 2 * 2 * 1 = 4 orderings
```

---

## Solution 1: Brute Force (Enumeration)

### Idea

Generate all possible traversal orderings by trying every permutation of children at each node.

### Algorithm

1. Build adjacency list from parent array
2. For each node, generate all permutations of children
3. Recursively count all valid orderings

### Code

```python
from itertools import permutations

def count_traversals_brute(n, parents):
  """
  Brute force: enumerate all orderings.

  Time: O(n! * n) in worst case
  Space: O(n)
  """
  # Build adjacency list
  children = [[] for _ in range(n + 1)]
  for i, p in enumerate(parents, start=2):
    children[p].append(i)

  def count_orderings(node):
    if not children[node]:
      return 1

    total = 0
    for perm in permutations(children[node]):
      product = 1
      for child in perm:
        product *= count_orderings(child)
      total += product
    return total

  return count_orderings(1)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n! * n) | Exponential due to permutation enumeration |
| Space | O(n) | Recursion stack depth |

### Why This Works (But Is Slow)

Correctly enumerates all orderings but factorial growth makes it impractical for n > 10.

---

## Solution 2: Optimal (Factorial Product)

### Key Insight

> **The Trick:** Instead of enumerating, multiply factorials of children counts.

For each node, the number of ways to order its children is `(number of children)!`. The total orderings is the product across all nodes.

### Formula

```
answer = Product of factorial(children_count[v]) for all v
       = factorial(c1) * factorial(c2) * ... * factorial(cn)
```

### Algorithm

1. Build tree from parent array
2. Count children for each node
3. Compute product of factorials (with modular arithmetic)

### Dry Run Example

```
Input: n=5, parents=[1, 1, 2, 2]

Step 1: Build children lists
  Node 1: children = [2, 3]  (count = 2)
  Node 2: children = [4, 5]  (count = 2)
  Node 3: children = []      (count = 0)
  Node 4: children = []      (count = 0)
  Node 5: children = []      (count = 0)

Step 2: Compute factorials
  fact[0] = 1
  fact[1] = 1
  fact[2] = 2

Step 3: Multiply
  result = fact[2] * fact[2] * fact[0] * fact[0] * fact[0]
         = 2 * 2 * 1 * 1 * 1
         = 4

Output: 4
```

### Code (Python)

```python
def count_traversals(n, parents):
  """
  Count tree traversal orderings using factorial product.

  Time: O(n)
  Space: O(n)
  """
  MOD = 10**9 + 7

  # Precompute factorials
  fact = [1] * (n + 1)
  for i in range(1, n + 1):
    fact[i] = fact[i-1] * i % MOD

  # Count children for each node
  children_count = [0] * (n + 1)
  for i, p in enumerate(parents, start=2):
    children_count[p] += 1

  # Compute product of factorials
  result = 1
  for v in range(1, n + 1):
    result = result * fact[children_count[v]] % MOD

  return result


def solve():
  n = int(input())
  if n == 1:
    print(1)
    return
  parents = list(map(int, input().split()))
  print(count_traversals(n, parents))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass for factorials, single pass for counting |
| Space | O(n) | Factorial array and children counts |

---

## Common Mistakes

### Mistake 1: Forgetting Modular Arithmetic

```python
# WRONG - Integer overflow for large n
result = 1
for v in range(1, n + 1):
  result *= factorial(children_count[v])  # Overflows!

# CORRECT - Apply modulo at each step
result = 1
for v in range(1, n + 1):
  result = result * fact[children_count[v]] % MOD
```

**Problem:** Factorials grow extremely fast; 21! exceeds 64-bit integers.
**Fix:** Always apply modulo after each multiplication.

### Mistake 2: Off-by-One in Parent Indexing

```python
# WRONG - Parents are for nodes 2..n, not 1..n
for i, p in enumerate(parents):  # i starts at 0
  children_count[p] += 1

# CORRECT - Parents start at node 2
for i, p in enumerate(parents, start=2):
  children_count[p] += 1
```

**Problem:** Node 1 is the root with no parent in input.
**Fix:** Enumerate from 2 when processing parent array.

### Mistake 3: Not Handling Single Node Case

```python
# WRONG - Empty parent array causes error
parents = list(map(int, input().split()))  # Empty for n=1

# CORRECT - Handle n=1 separately
if n == 1:
  print(1)
  return
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n=1 | 1 | Only one trivial ordering |
| Linear chain | n=5, each node has 1 child | 1 | 1! * 1! * 1! * 1! = 1 |
| Star graph | n=5, root has 4 children | 24 | 4! = 24 |
| Binary tree | Each node has 0 or 2 children | 2^k | Product of 2! for internal nodes |
| Large n | n=200000 | (computed) | Must use modular arithmetic |

---

## When to Use This Pattern

### Use This Approach When:
- Counting orderings of tree traversals
- Computing permutations with tree constraints
- Problems involving child ordering independence

### Don't Use When:
- Tree structure is constrained (e.g., BST with ordering)
- Specific traversal order required (preorder/inorder/postorder)
- Need actual traversal sequences, not just count

### Pattern Recognition Checklist:
- [ ] Each node's children can be visited in any order? -> **Factorial product**
- [ ] Counting binary trees from traversal? -> **Catalan numbers**
- [ ] Counting labeled trees? -> **Cayley's formula (n^(n-2))**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subordinates](https://cses.fi/problemset/task/1674) | Basic tree traversal and subtree counting |
| [Tree Diameter](https://cses.fi/problemset/task/1131) | DFS on trees fundamentals |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Counting Paths](https://cses.fi/problemset/task/1136) | Counting with LCA constraints |
| [Bracket Sequences I](https://cses.fi/problemset/task/2064) | Catalan number application |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Bracket Sequences II](https://cses.fi/problemset/task/2187) | Constrained Catalan counting |
| [Counting Necklaces](https://cses.fi/problemset/task/2209) | Burnside's lemma for symmetry |

---

## Key Takeaways

1. **The Core Idea:** Tree traversal orderings = product of factorials of children counts
2. **Time Optimization:** O(n!) enumeration -> O(n) factorial product
3. **Space Trade-off:** O(n) for factorial precomputation
4. **Pattern:** Combinatorial counting with tree structure constraints

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the factorial product formula from first principles
- [ ] Implement modular factorial computation
- [ ] Handle edge cases (n=1, linear chain, star graph)
- [ ] Explain why children orderings are independent

---

## Additional Resources

- [CP-Algorithms: Catalan Numbers](https://cp-algorithms.com/combinatorics/catalan-numbers.html)
- [CSES Problem Set - Tree Algorithms](https://cses.fi/problemset/list/)
- [Modular Arithmetic Tutorial](https://cp-algorithms.com/algebra/module-inverse.html)
