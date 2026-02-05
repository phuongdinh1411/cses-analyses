---
layout: simple
title: "Functional Graph Distribution - Counting Problem"
permalink: /problem_soulutions/counting_problems/functional_graph_distribution_analysis
difficulty: Medium
tags: [counting, graph-theory, modular-arithmetic, combinatorics]
---

# Functional Graph Distribution

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Counting / Graph Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Modular Exponentiation |
| **CSES Link** | - |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand what a functional graph is and its properties
- [ ] Apply modular exponentiation for large power calculations
- [ ] Count combinatorial structures using multiplication principle
- [ ] Handle modular arithmetic to prevent overflow

---

## Problem Statement

**Problem:** Count the number of functional graphs with n nodes. A functional graph is a directed graph where each node has exactly one outgoing edge.

**Input:**
- Line 1: A single integer n (number of nodes)

**Output:**
- The number of functional graphs modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 10^6

### Example

```
Input:
3

Output:
27
```

**Explanation:** Each of the 3 nodes can point to any of the 3 nodes (including itself). Total = 3 x 3 x 3 = 27.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How many ways can we assign one outgoing edge to each node?

A functional graph has a simple property: every node has exactly one outgoing edge. This means for each node, we independently choose one of n possible destinations.

### Breaking Down the Problem

1. **What are we counting?** All possible functional graphs with n labeled nodes.
2. **What choice does each node have?** Each node can point to any of the n nodes.
3. **Are the choices independent?** Yes, each node's choice is independent.

### Analogies

Think of this like n people each pointing to someone in the room (including themselves). Each person has n choices, and their choices don't affect each other. Total arrangements = n^n.

### Visual Understanding

```
n = 3 nodes: {1, 2, 3}

Each node picks one target:
  Node 1 -> can point to {1, 2, 3}  (3 choices)
  Node 2 -> can point to {1, 2, 3}  (3 choices)
  Node 3 -> can point to {1, 2, 3}  (3 choices)

Total combinations = 3 x 3 x 3 = 27

Some example graphs:
  Graph A: 1->1, 2->2, 3->3  (all self-loops)
  Graph B: 1->2, 2->3, 3->1  (single cycle)
  Graph C: 1->2, 2->1, 3->3  (cycle + self-loop)
```

---

## Solution 1: Brute Force (Enumeration)

### Idea

Generate all possible functional graphs by trying every combination of edge assignments.

### Algorithm

1. For each node from 1 to n, iterate through all possible targets (1 to n)
2. Count each valid assignment
3. Return total count modulo 10^9 + 7

### Code

```python
def count_functional_graphs_brute(n, mod=10**9+7):
    """
    Brute force: enumerate all functional graphs.

    Time: O(n^n) - generates all combinations
    Space: O(n) - recursion depth
    """
    def generate(node):
        if node == n:
            return 1
        count = 0
        for target in range(n):
            count = (count + generate(node + 1)) % mod
        return count

    return generate(0)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^n) | Enumerate all n^n possible graphs |
| Space | O(n) | Recursion stack depth |

### Why This Works (But Is Slow)

This correctly counts all functional graphs but is impractical for n > 10. We need a mathematical formula.

---

## Solution 2: Optimal Solution (Mathematical Formula)

### Key Insight

> **The Trick:** Since each of n nodes independently chooses from n targets, the total count is simply n^n.

### Mathematical Derivation

```
Total functional graphs = (choices for node 1) x (choices for node 2) x ... x (choices for node n)
                       = n x n x n x ... x n  (n times)
                       = n^n
```

### Algorithm

1. Compute n^n using fast modular exponentiation
2. Return result modulo 10^9 + 7

### Dry Run Example

Let's trace through with n = 3:

```
Compute 3^3 mod (10^9 + 7):

Using binary exponentiation:
  exp = 3 = 11 in binary

  Initialize: result = 1, base = 3

  Iteration 1 (exp = 3, binary: 11):
    exp is odd -> result = 1 * 3 = 3
    exp = 3 >> 1 = 1
    base = 3 * 3 = 9

  Iteration 2 (exp = 1, binary: 1):
    exp is odd -> result = 3 * 9 = 27
    exp = 1 >> 1 = 0
    base = 9 * 9 = 81

  exp = 0, stop

Answer: 27
```

### Visual Diagram

```
Binary Exponentiation for 3^3:

3^3 = 3^(1+2) = 3^1 * 3^2

     3^1 = 3
     3^2 = 9
     -----------
     3^3 = 3 * 9 = 27
```

### Code

**Python:**
```python
def count_functional_graphs(n, mod=10**9+7):
    """
    Optimal solution using modular exponentiation.

    Time: O(log n)
    Space: O(1)
    """
    return pow(n, n, mod)


def count_functional_graphs_manual(n, mod=10**9+7):
    """
    Manual implementation of modular exponentiation.
    Useful for understanding or languages without built-in mod pow.
    """
    if n == 0:
        return 1

    result = 1
    base = n % mod
    exp = n

    while exp > 0:
        if exp & 1:  # exp is odd
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod

    return result


# Main
n = int(input())
print(count_functional_graphs(n))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(log n) | Binary exponentiation |
| Space | O(1) | Only a few variables |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** Result overflows long long very quickly.
**Fix:** Apply modulo at each multiplication step, or use fast exponentiation.

### Mistake 2: Wrong Exponentiation Base

```python
# WRONG - computes 2^n instead of n^n
result = pow(2, n, mod)
```

**Problem:** Using wrong base in exponentiation.
**Fix:** Base and exponent should both be n for this problem.

### Mistake 3: Not Handling n = 0

```python
# WRONG - 0^0 needs special handling
def solve(n):
    return pow(n, n, mod)  # 0^0 is undefined mathematically
```

**Problem:** Edge case for n = 0 (depends on problem interpretation).
**Fix:** Define 0^0 = 1 for combinatorial purposes (empty graph).

```python
# CORRECT
def solve(n, mod=10**9+7):
    if n == 0:
        return 1
    return pow(n, n, mod)
```

### Mistake 4: Using Slow Exponentiation

```python
# WRONG - O(n) time, too slow
result = 1
for _ in range(n):
    result = (result * n) % mod
```

**Problem:** Linear time is too slow for n up to 10^6.
**Fix:** Use O(log n) binary exponentiation.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single node | n = 1 | 1 | Only one graph: node points to itself |
| Two nodes | n = 2 | 4 | 2^2 = 4 possible graphs |
| Large n | n = 10^6 | [computed value] | Tests modular arithmetic |
| Edge: n = 0 | n = 0 | 1 | Convention: empty graph counts as 1 |

---

## When to Use This Pattern

### Use This Approach When:
- Counting structures where each element makes independent choices
- The answer involves computing a^b mod m for large a, b
- You see the multiplication principle: "n ways for each of m things"

### Don't Use When:
- Choices are dependent (need DP or inclusion-exclusion)
- Counting labeled vs unlabeled structures matters
- You need to enumerate actual graphs, not just count them

### Pattern Recognition Checklist:
- [ ] Each element has k independent choices? -> **Total = k^n**
- [ ] Need to compute large exponents mod m? -> **Binary exponentiation**
- [ ] Counting ordered sequences/functions? -> **Multiplication principle**

---

## Related Problems

### Easier (Do These First)

| Problem | Link | Why It Helps |
|---------|------|--------------|
| Exponentiation | [CSES 1095](https://cses.fi/problemset/task/1095) | Basic modular exponentiation |
| Creating Strings | [CSES 1622](https://cses.fi/problemset/task/1622) | Basic counting/enumeration |

### Similar Difficulty

| Problem | Link | Key Difference |
|---------|------|----------------|
| Counting Divisors | [CSES 1713](https://cses.fi/problemset/task/1713) | Different counting formula |
| Binomial Coefficients | [CSES 1079](https://cses.fi/problemset/task/1079) | Uses factorials and inverses |

### Harder (Do These After)

| Problem | Link | New Concept |
|---------|------|-------------|
| Counting Sequences | [CSES 2228](https://cses.fi/problemset/task/2228) | More complex counting |
| Graph Counting | [Counting Tilings (CSES)](https://cses.fi/problemset/task/2181) | Labeled graph enumeration |
| Planets Cycles | [CSES 1751](https://cses.fi/problemset/task/1751) | Functional graph traversal |

---

## Key Takeaways

1. **The Core Idea:** Functional graph count = n^n because each node independently chooses one of n targets.
2. **Time Optimization:** Binary exponentiation reduces O(n) to O(log n).
3. **Space Trade-off:** O(1) space with no enumeration needed.
4. **Pattern:** This is a direct application of the multiplication principle in combinatorics.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why functional graph count equals n^n
- [ ] Implement binary exponentiation from scratch
- [ ] Handle modular arithmetic correctly to avoid overflow
- [ ] Recognize when a problem requires counting with the multiplication principle

---

## Additional Resources

- [CP-Algorithms: Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [CP-Algorithms: Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html)
- [CSES Planets Cycles](https://cses.fi/problemset/task/1751) - Functional graph traversal
- [Functional Graph - Wikipedia](https://en.wikipedia.org/wiki/Functional_graph)
