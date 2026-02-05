---
layout: simple
title: "Tournament Graph Count - Combinatorics Problem"
permalink: /problem_soulutions/counting_problems/tournament_graph_distribution_analysis
difficulty: Medium
tags: [combinatorics, graph-theory, modular-arithmetic, binary-exponentiation]
---

# Tournament Graph Count

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Combinatorics / Graph Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Modular Exponentiation |
| **CSES Link** | - |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand tournament graphs and their properties
- [ ] Apply combinatorial counting to graph structures
- [ ] Implement binary exponentiation for large powers
- [ ] Handle modular arithmetic to prevent overflow

---

## Problem Statement

**Problem:** Given n players, count the number of distinct tournament graphs. A tournament graph is a complete directed graph where every pair of vertices has exactly one directed edge between them.

**Input:**
- Line 1: A single integer n (number of players)

**Output:**
- The number of distinct tournament graphs modulo 10^9+7

**Constraints:**
- 1 <= n <= 10^6

### Example

```
Input:
3

Output:
8
```

**Explanation:** With 3 players, there are 3 edges (between each pair). Each edge can point in 2 directions. Total tournaments = 2^3 = 8.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How many ways can we orient edges in a complete graph?

A tournament is simply a complete graph where we choose a direction for each edge. Since there are C(n,2) = n(n-1)/2 edges and each edge has 2 possible directions, the answer is 2^(n(n-1)/2).

### Breaking Down the Problem

1. **What are we counting?** Distinct tournament graphs on n vertices
2. **What defines a tournament?** Direction of each edge in a complete graph
3. **What's the formula?** 2^(number of edges) = 2^(n(n-1)/2)

### Visual Analogy

Think of n teams in a round-robin tournament. Each pair plays exactly once, and one team must win. We're counting all possible outcomes for the entire tournament.

```
n = 3 players: A, B, C

All possible tournaments:
Tournament 1: A->B, A->C, B->C  (A beats all)
Tournament 2: A->B, A->C, C->B
Tournament 3: A->B, C->A, B->C
Tournament 4: A->B, C->A, C->B  (C beats A, A beats B)
Tournament 5: B->A, A->C, B->C  (B beats A, both beat C)
Tournament 6: B->A, A->C, C->B  (cyclic: B->A->C->B)
Tournament 7: B->A, C->A, B->C  (B beats all)
Tournament 8: B->A, C->A, C->B  (C beats all)

Total: 8 = 2^3
```

---

## Solution 1: Brute Force (Enumeration)

### Idea

Generate all possible edge direction assignments and count them.

### Algorithm

1. List all edges in the complete graph
2. For each edge, try both directions
3. Count total valid tournaments

### Code

```python
def count_tournaments_brute(n):
 """
 Brute force: enumerate all edge directions.

 Time: O(2^(n^2))
 Space: O(n^2)
 """
 if n <= 1:
  return 1

 num_edges = n * (n - 1) // 2
 return 2 ** num_edges  # Simplified enumeration count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^(n^2)) | Exponential in number of edges |
| Space | O(n^2) | Store edge list |

### Why This Is Slow

For n=1000, we have ~500,000 edges. Computing 2^500000 directly is infeasible.

---

## Solution 2: Optimal (Modular Exponentiation)

### Key Insight

> **The Trick:** Use binary exponentiation to compute 2^k mod m in O(log k) time.

### Formula Derivation

```
Number of edges = C(n,2) = n(n-1)/2
Each edge has 2 choices
Answer = 2^(n(n-1)/2) mod (10^9+7)
```

### Dry Run Example

Let's trace through with n = 4:

```
Step 1: Calculate number of edges
  edges = 4 * 3 / 2 = 6

Step 2: Compute 2^6 using binary exponentiation
  exp = 6 = 110 in binary

  Initialize: result = 1, base = 2

  Iteration 1: exp = 6 (110), bit 0 = 0
    exp is even, skip multiplication
    base = 2 * 2 = 4
    exp = 3

  Iteration 2: exp = 3 (11), bit 0 = 1
    result = 1 * 4 = 4
    base = 4 * 4 = 16
    exp = 1

  Iteration 3: exp = 1 (1), bit 0 = 1
    result = 4 * 16 = 64
    base = 16 * 16 = 256
    exp = 0

Step 3: Result = 64

Answer: 64 tournament graphs with 4 players
```

### Visual: Binary Exponentiation

```
Computing 2^6:
  6 = 4 + 2 = 2^2 + 2^1

  2^6 = 2^4 * 2^2
      = 16 * 4
      = 64

Iteration:     exp    bit   result   base
Initial:       6      -     1        2
After iter 1:  3      0     1        4
After iter 2:  1      1     4        16
After iter 3:  0      1     64       256
```

### Code (Python)

```python
def count_tournaments(n: int, mod: int = 10**9 + 7) -> int:
 """
 Count tournament graphs using modular exponentiation.

 Time: O(log(n^2)) = O(log n)
 Space: O(1)
 """
 if n <= 1:
  return 1

 exponent = n * (n - 1) // 2
 return pow(2, exponent, mod)


def mod_pow(base: int, exp: int, mod: int) -> int:
 """
 Binary exponentiation: compute base^exp mod m.

 Time: O(log exp)
 Space: O(1)
 """
 result = 1
 base %= mod

 while exp > 0:
  if exp & 1:  # If exp is odd
   result = result * base % mod
  base = base * base % mod
  exp >>= 1

 return result


# Main solution
def solve():
 n = int(input())
 print(count_tournaments(n))


if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(log n) | Binary exponentiation on exponent ~n^2 |
| Space | O(1) | Only scalar variables |

---

## Common Mistakes

### Mistake 1: Integer Overflow in Exponent Calculation

**Problem:** For n = 10^6, n * (n-1) exceeds int range.
**Fix:** Cast to long long before multiplication.

### Mistake 2: Forgetting Edge Cases

```python
# WRONG - crashes or wrong for n=0 or n=1
def count_tournaments(n):
 return pow(2, n * (n-1) // 2, MOD)

# CORRECT - handle edge cases
def count_tournaments(n):
 if n <= 1:
  return 1
 return pow(2, n * (n-1) // 2, MOD)
```

**Problem:** n=0 or n=1 should return 1 (one trivial tournament).

### Mistake 3: Wrong Modular Arithmetic

```python
# WRONG - applying mod incorrectly
result = (2 ** exponent) % MOD  # Very slow for large exponent!

# CORRECT - use three-argument pow
result = pow(2, exponent, MOD)  # Fast modular exponentiation
```

**Problem:** Computing 2^exponent first creates a huge number.
**Fix:** Use built-in modular pow or implement binary exponentiation.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single player | n = 1 | 1 | No edges, one trivial tournament |
| No players | n = 0 | 1 | Empty tournament |
| Two players | n = 2 | 2 | One edge, two directions |
| Three players | n = 3 | 8 | 2^3 = 8 |
| Large n | n = 10^6 | varies | Must use modular exponentiation |

---

## When to Use This Pattern

### Use Modular Exponentiation When:
- Computing large powers with modulo
- Counting arrangements where each choice is independent
- Problems involving 2^k or a^k mod m

### Pattern Recognition Checklist:
- [ ] Does each choice multiply independently? Consider powers
- [ ] Is the exponent very large? Use binary exponentiation
- [ ] Need result mod p? Apply mod at each step

### Related Formulas

| Structure | Count Formula |
|-----------|---------------|
| Tournament graphs on n vertices | 2^(n(n-1)/2) |
| Labeled graphs on n vertices | 2^(n(n-1)/2) |
| Binary strings of length n | 2^n |
| Subsets of n elements | 2^n |

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Exponentiation](https://cses.fi/problemset/task/1095) | Basic modular exponentiation |
| [Exponentiation II](https://cses.fi/problemset/task/1712) | Modular exponentiation with Fermat |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Counting Bits](https://cses.fi/problemset/task/1146) | Counting with binary properties |
| [Bracket Sequences I](https://cses.fi/problemset/task/2064) | Combinatorial counting |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Graph Counting](https://cses.fi/problemset/task/2415) | More complex graph counting |
| [Distributing Apples](https://cses.fi/problemset/task/1716) | Stars and bars counting |

---

## Key Takeaways

1. **Core Idea:** Tournament count = 2^(edges) where edges = n(n-1)/2
2. **Time Optimization:** Binary exponentiation reduces O(k) to O(log k)
3. **Space Trade-off:** O(1) space by computing iteratively
4. **Pattern:** Independent binary choices lead to 2^n counting

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the formula 2^(n(n-1)/2) from scratch
- [ ] Implement binary exponentiation without reference
- [ ] Handle overflow with proper type casting
- [ ] Explain why modular arithmetic is applied at each step

---

## Additional Resources

- [CP-Algorithms: Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [Tournament Graph - Wikipedia](https://en.wikipedia.org/wiki/Tournament_(graph_theory))
- [CSES Exponentiation](https://cses.fi/problemset/task/1095) - Modular exponentiation
