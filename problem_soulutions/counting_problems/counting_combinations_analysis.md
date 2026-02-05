---
layout: simple
title: "Binomial Coefficients - Mathematics Problem"
permalink: /problem_soulutions/counting_problems/counting_combinations_analysis
difficulty: Medium
tags: [combinatorics, modular-arithmetic, math, precomputation]
---

# Binomial Coefficients

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Binomial Coefficients](https://cses.fi/problemset/task/1079) |
| **Difficulty** | Medium |
| **Category** | Mathematics / Combinatorics |
| **Time Limit** | 1 second |
| **Key Technique** | Modular Inverse + Precomputation |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Compute C(n,k) efficiently using factorials and modular inverse
- [ ] Apply Fermat's Little Theorem for modular division
- [ ] Precompute factorials and inverse factorials for multiple queries
- [ ] Handle large numbers with modular arithmetic

---

## Problem Statement

**Problem:** Given n queries, for each query compute the binomial coefficient C(a,b) modulo 10^9+7.

**Input:**
- Line 1: n - number of queries
- Lines 2 to n+1: Two integers a and b

**Output:**
- For each query, print C(a,b) mod (10^9+7)

**Constraints:**
- 1 <= n <= 10^5
- 0 <= b <= a <= 10^6

### Example

```
Input:
3
5 3
8 4
100 50

Output:
10
70
538992043
```

**Explanation:** C(5,3) = 5!/(3! * 2!) = 120/(6 * 2) = 10

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we compute C(n,k) = n!/(k!(n-k)!) when n is large and we need results modulo a prime?

The formula involves division, but modular arithmetic does not support direct division. We need **modular inverse** to convert division into multiplication.

### Breaking Down the Problem

1. **What are we looking for?** C(n,k) mod p where p = 10^9+7
2. **What information do we have?** n, k, and p is prime
3. **What's the relationship?** C(n,k) = n! * (k!)^(-1) * ((n-k)!)^(-1) mod p

### The Key Insight

Since p is prime, by **Fermat's Little Theorem**: a^(p-1) = 1 (mod p)

Therefore: a^(-1) = a^(p-2) (mod p)

This lets us compute modular inverse using fast exponentiation!

---

## Solution 1: Naive Approach (Per Query)

### Idea

For each query, compute factorials and modular inverse directly.

### Code

```python
def mod_inverse(a, p):
 """Compute a^(-1) mod p using Fermat's Little Theorem."""
 return pow(a, p - 2, p)

def factorial(n, p):
 """Compute n! mod p."""
 result = 1
 for i in range(2, n + 1):
  result = (result * i) % p
 return result

def nCr_naive(n, k, p=10**9 + 7):
 """Compute C(n,k) mod p - naive per-query approach."""
 if k > n or k < 0:
  return 0

 num = factorial(n, p)
 denom = (factorial(k, p) * factorial(n - k, p)) % p
 return (num * mod_inverse(denom, p)) % p
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * q) | n factorial per query, q queries |
| Space | O(1) | No precomputation |

### Why This Works (But Is Slow)

Correct for single queries but recomputes factorials repeatedly. With 10^5 queries and n up to 10^6, this is too slow (TLE).

---

## Solution 2: Optimal Solution (Precomputation)

### Key Insight

> **The Trick:** Precompute all factorials and their modular inverses once, then answer each query in O(1).

### Precomputation Strategy

1. **fact[i]** = i! mod p
2. **inv_fact[i]** = (i!)^(-1) mod p

Then: C(n,k) = fact[n] * inv_fact[k] * inv_fact[n-k] mod p

### Computing Inverse Factorials Efficiently

Instead of computing each inverse separately (O(n log p) total), use this trick:

```
inv_fact[n] = (n!)^(-1)  (compute using pow)
inv_fact[n-1] = inv_fact[n] * n  (since (n-1)!^(-1) = n!^(-1) * n)
inv_fact[n-2] = inv_fact[n-1] * (n-1)
...and so on
```

This gives O(n) precomputation for inverses.

### Dry Run Example

Let's trace through with query C(5,3):

```
Precomputed arrays (for small n):
  fact = [1, 1, 2, 6, 24, 120]  (0! to 5!)
  inv_fact = corresponding inverses

Query: C(5,3)
  n = 5, k = 3

  Step 1: Get fact[5] = 120
  Step 2: Get inv_fact[3] = inverse of 6
  Step 3: Get inv_fact[5-3] = inv_fact[2] = inverse of 2

  Result = 120 * inv(6) * inv(2) mod p
         = 120 / 6 / 2 mod p
         = 10
```

### Visual Diagram

```
Formula: C(n,k) = n! / (k! * (n-k)!)

         fact[n]
         -------
C(n,k) = fact[k] * fact[n-k]

       = fact[n] * inv_fact[k] * inv_fact[n-k]
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
         All precomputed -> O(1) per query
```

### Algorithm

1. Precompute fact[0..MAX_N]
2. Compute inv_fact[MAX_N] using Fermat's theorem
3. Compute inv_fact[MAX_N-1..0] backwards
4. For each query: return fact[n] * inv_fact[k] * inv_fact[n-k] mod p

### Code (Python)

```python
import sys
input = sys.stdin.readline

def solve():
 MOD = 10**9 + 7
 MAX_N = 10**6 + 1

 # Precompute factorials
 fact = [1] * MAX_N
 for i in range(1, MAX_N):
  fact[i] = (fact[i-1] * i) % MOD

 # Precompute inverse factorials
 inv_fact = [1] * MAX_N
 inv_fact[MAX_N - 1] = pow(fact[MAX_N - 1], MOD - 2, MOD)
 for i in range(MAX_N - 2, -1, -1):
  inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % MOD

 def nCr(n, k):
  if k > n or k < 0:
   return 0
  return (fact[n] * inv_fact[k] % MOD) * inv_fact[n - k] % MOD

 # Process queries
 q = int(input())
 results = []
 for _ in range(q):
  a, b = map(int, input().split())
  results.append(nCr(a, b))

 print('\n'.join(map(str, results)))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(MAX_N + q) | O(MAX_N) precomputation, O(1) per query |
| Space | O(MAX_N) | Two arrays of size MAX_N |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** Multiplying three large numbers overflows even `long long`.
**Fix:** Apply modulo after each multiplication.

### Mistake 2: Computing Inverse Wrong

```python
# WRONG - regular division
result = fact[n] // fact[k] // fact[n-k]

# CORRECT - modular inverse
result = fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD
```

**Problem:** Integer division gives wrong result in modular arithmetic.
**Fix:** Always use modular inverse for division under mod.

### Mistake 3: Forgetting Edge Case k > n

```python
# WRONG - crashes or wrong answer
def nCr(n, k):
 return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD

# CORRECT - handle invalid input
def nCr(n, k):
 if k > n or k < 0:
  return 0
 return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD
```

### Mistake 4: Wrong Inverse Computation Direction

```python
# WRONG - forward computation needs pow for each
for i in range(MAX_N):
 inv_fact[i] = pow(fact[i], MOD-2, MOD)  # O(n log p)

# CORRECT - backward computation in O(n)
inv_fact[MAX_N-1] = pow(fact[MAX_N-1], MOD-2, MOD)
for i in range(MAX_N-2, -1, -1):
 inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| k = 0 | C(5,0) | 1 | Only one way to choose nothing |
| k = n | C(5,5) | 1 | Only one way to choose all |
| k > n | C(3,5) | 0 | Impossible to choose more than available |
| n = 0 | C(0,0) | 1 | Empty set has one subset (itself) |
| Large n | C(10^6, 5*10^5) | [computed] | Tests precomputation efficiency |

---

## When to Use This Pattern

### Use Precomputed Factorials When:
- Multiple queries for C(n,k) with different n, k values
- n is bounded (e.g., n <= 10^6)
- Modulus is a prime number
- Need O(1) per query after preprocessing

### Don't Use When:
- Single query only (direct computation is fine)
- n is extremely large (> 10^7) - memory constraint
- Modulus is not prime (use extended Euclidean algorithm instead)
- Need exact values without modulo (use big integers)

### Pattern Recognition Checklist:
- [ ] Need C(n,k) mod prime? -> **Precompute fact + inv_fact**
- [ ] Multiple queries? -> **Must precompute**
- [ ] n very large but few queries? -> **Consider Lucas theorem**
- [ ] Modulus not prime? -> **Use extended GCD for inverse**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Exponentiation](https://cses.fi/problemset/task/1095) | Learn fast power (needed for inverse) |
| [Exponentiation II](https://cses.fi/problemset/task/1712) | Modular exponentiation practice |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Creating Strings II](https://cses.fi/problemset/task/1715) | Multinomial coefficients |
| [Distributing Apples](https://cses.fi/problemset/task/1716) | Stars and bars (C(n+k-1, k-1)) |
| [Bracket Sequences I](https://cses.fi/problemset/task/2064) | Catalan numbers using combinations |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Bracket Sequences II](https://cses.fi/problemset/task/2187) | Constrained Catalan |
| [Counting Necklaces](https://cses.fi/problemset/task/2209) | Burnside's lemma |
| [Counting Grids](https://cses.fi/problemset/task/2210) | Advanced counting |

---

## Key Takeaways

1. **The Core Idea:** Use Fermat's Little Theorem to compute modular inverse, enabling "division" under modulo.

2. **Time Optimization:** Precompute factorials and inverse factorials once, answer queries in O(1).

3. **Space Trade-off:** O(MAX_N) space for O(1) query time - essential for multiple queries.

4. **Pattern:** This is the standard template for any problem involving binomial coefficients mod prime.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why we need modular inverse instead of regular division
- [ ] Derive the backward formula for computing inverse factorials
- [ ] Implement the solution without looking at code
- [ ] Identify problems that reduce to computing C(n,k)

---

## Additional Resources

- [CP-Algorithms: Binomial Coefficients](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- [CP-Algorithms: Modular Inverse](https://cp-algorithms.com/algebra/module-inverse.html)
- [CSES Binomial Coefficients](https://cses.fi/problemset/task/1079) - nCr computation
