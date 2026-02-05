---
layout: simple
title: "Counting Permutations - Combinatorics Problem"
permalink: /problem_soulutions/counting_problems/counting_permutations_analysis
difficulty: Easy
tags: [combinatorics, factorial, modular-arithmetic, math]
---

# Counting Permutations

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Combinatorics / Math |
| **Time Limit** | 1 second |
| **Key Technique** | Factorial with Modular Arithmetic |
| **CSES Link** | [Creating Strings I](https://cses.fi/problemset/task/1622) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand permutation formulas: n! and n!/(n-r)!
- [ ] Apply modular arithmetic to prevent integer overflow
- [ ] Precompute factorials for efficient multiple queries
- [ ] Calculate modular inverse using Fermat's Little Theorem

---

## Problem Statement

**Problem:** Given n distinct elements, count the number of ways to arrange them in a sequence.

**Input:**
- Line 1: Integer n (number of elements)

**Output:**
- Number of permutations P(n) = n! modulo 10^9+7

**Constraints:**
- 1 <= n <= 10^6
- Output modulo 10^9+7

### Example

```
Input:
4

Output:
24
```

**Explanation:** 4! = 4 x 3 x 2 x 1 = 24 distinct arrangements.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How many ways can we fill n positions with n distinct elements?

The answer comes from the **multiplication principle**: for the first position we have n choices, for the second position we have (n-1) choices, and so on.

### Breaking Down the Problem

1. **What are we looking for?** Total number of distinct arrangements
2. **What information do we have?** Number of elements n
3. **What's the relationship?** P(n) = n x (n-1) x (n-2) x ... x 1 = n!

### Analogies

Think of this like seating n people in n chairs:
- First chair: any of n people can sit
- Second chair: any of remaining (n-1) people
- Continue until all chairs are filled

---

## Solution 1: Brute Force (Naive Factorial)

### Idea

Directly multiply 1 x 2 x 3 x ... x n without considering overflow.

### Algorithm

1. Initialize result = 1
2. Multiply result by each number from 1 to n
3. Return result

### Code

**Python:**
```python
def factorial_naive(n):
 """
 Naive factorial calculation (overflows for large n).

 Time: O(n)
 Space: O(1)
 """
 result = 1
 for i in range(1, n + 1):
  result *= i
 return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single loop from 1 to n |
| Space | O(1) | Only stores result |

### Why This Works (But Fails)

Correctness is guaranteed by the factorial definition, but **integer overflow** occurs for n > 20 (64-bit) or n > 12 (32-bit). We need modular arithmetic.

---

## Solution 2: Optimal Solution (Modular Factorial)

### Key Insight

> **The Trick:** Apply modulo at each multiplication step to prevent overflow while maintaining correctness.

Mathematical property: `(a * b) mod m = ((a mod m) * (b mod m)) mod m`

### Algorithm

1. Initialize result = 1
2. For each i from 1 to n:
   - result = (result * i) % MOD
3. Return result

### Dry Run Example

Let's trace through with input `n = 4, MOD = 10^9+7`:

```
Initial: result = 1

Step 1: i = 1
  result = (1 * 1) % MOD = 1

Step 2: i = 2
  result = (1 * 2) % MOD = 2

Step 3: i = 3
  result = (2 * 3) % MOD = 6

Step 4: i = 4
  result = (6 * 4) % MOD = 24

Final answer: 24
```

### Visual Diagram

```
Permutation Counting for n = 4:

Position:    [1st] [2nd] [3rd] [4th]
Choices:       4  x  3  x  2  x  1  = 24

Calculation with modular arithmetic:
   1 --> 1*1=1 --> 1*2=2 --> 2*3=6 --> 6*4=24
   ^                                     ^
 start                                result
```

### Code

**Python:**
```python
def count_permutations(n, mod=10**9 + 7):
 """
 Calculate n! with modular arithmetic.

 Time: O(n)
 Space: O(1)
 """
 result = 1
 for i in range(1, n + 1):
  result = (result * i) % mod
 return result


# For multiple queries: precompute factorials
def precompute_factorials(max_n, mod=10**9 + 7):
 """
 Precompute factorials for efficient queries.

 Time: O(max_n)
 Space: O(max_n)
 """
 fact = [1] * (max_n + 1)
 for i in range(1, max_n + 1):
  fact[i] = (fact[i - 1] * i) % mod
 return fact


# Example usage
if __name__ == "__main__":
 n = int(input())
 print(count_permutations(n))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass computing factorial |
| Space | O(1) | Constant space for single query |
| Space | O(n) | Linear space with precomputation |

---

## Solution 3: nPr - Partial Permutations

### Key Insight

> **Extended Formula:** When selecting r items from n: P(n,r) = n! / (n-r)!

This requires computing **modular inverse** using Fermat's Little Theorem:
- For prime p: a^(-1) = a^(p-2) mod p

### Code

**Python:**
```python
def mod_pow(base, exp, mod):
 """Fast modular exponentiation."""
 result = 1
 base %= mod
 while exp > 0:
  if exp & 1:
   result = (result * base) % mod
  exp >>= 1
  base = (base * base) % mod
 return result


def mod_inverse(a, mod):
 """Modular inverse using Fermat's Little Theorem."""
 return mod_pow(a, mod - 2, mod)


def nPr(n, r, mod=10**9 + 7):
 """
 Calculate P(n,r) = n! / (n-r)!

 Time: O(n) or O(1) with precomputation
 Space: O(1)
 """
 if r > n:
  return 0

 result = 1
 for i in range(n - r + 1, n + 1):
  result = (result * i) % mod
 return result


# Alternative with precomputed factorials
def nPr_precomputed(n, r, fact, inv_fact, mod=10**9 + 7):
 """P(n,r) with precomputed factorials and inverses."""
 if r > n:
  return 0
 return (fact[n] * inv_fact[n - r]) % mod
```

---

## Common Mistakes

### Mistake 1: Forgetting Modulo at Each Step

```python
# WRONG - Overflow occurs
def factorial_wrong(n, mod):
 result = 1
 for i in range(1, n + 1):
  result *= i
 return result % mod  # Too late! Overflow already happened
```

**Problem:** Integer overflow before the modulo operation.
**Fix:** Apply modulo at each multiplication step.

### Mistake 2: Using Wrong Modular Inverse

```python
# WRONG - Integer division doesn't work in modular arithmetic
def nPr_wrong(n, r, mod):
 return (factorial(n) // factorial(n - r)) % mod
```

**Problem:** Division in modular arithmetic requires modular inverse.
**Fix:** Use `a * mod_inverse(b)` instead of `a / b`.

### Mistake 3: Not Handling Edge Cases

```python
# WRONG - Crashes on n = 0
def factorial_wrong(n, mod):
 result = 1
 for i in range(1, n + 1):  # Correct loop but...
  result = (result * i) % mod
 return result  # Works, but consider 0! = 1 explicitly
```

**Fix:** Explicitly handle n = 0 case if needed.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Zero elements | n = 0 | 1 | 0! = 1 by definition |
| Single element | n = 1 | 1 | 1! = 1 |
| Small n | n = 5 | 120 | 5! = 120 |
| Large n | n = 10^6 | (computed) | Must use modular arithmetic |
| P(n,r) where r > n | P(3,5) | 0 | Invalid - not enough elements |

---

## When to Use This Pattern

### Use This Approach When:
- Counting arrangements of distinct objects
- Computing binomial coefficients (which use factorials)
- Problems asking for "number of ways" with large answers
- Multiple queries requiring factorial values

### Don't Use When:
- Elements have repetitions (use multinomial formula)
- Circular arrangements (use (n-1)!)
- Need to generate actual permutations (use backtracking)

### Pattern Recognition Checklist:
- [ ] Counting arrangements? -> **Factorial / Permutation**
- [ ] Answer needs modulo? -> **Modular arithmetic required**
- [ ] Multiple queries? -> **Precompute factorials**
- [ ] Division involved? -> **Modular inverse needed**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Creating Strings I](https://cses.fi/problemset/task/1622) | Generate actual permutations |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Binomial Coefficients](https://cses.fi/problemset/task/1079) | C(n,r) uses factorials and inverse |
| [Distributing Apples](https://cses.fi/problemset/task/1716) | Stars and bars with factorials |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Bracket Sequences I](https://cses.fi/problemset/task/2064) | Catalan numbers using factorials |
| [Counting Necklaces](https://cses.fi/problemset/task/2209) | Burnside's lemma with permutations |
| [Creating Strings II](https://cses.fi/problemset/task/1715) | Permutations with repetitions |

---

## Key Takeaways

1. **The Core Idea:** n! counts arrangements, computed iteratively with modular arithmetic
2. **Time Optimization:** Precompute factorials for O(1) per query
3. **Space Trade-off:** O(n) space for precomputation saves repeated calculation
4. **Pattern:** Modular arithmetic is essential for large counting problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Calculate n! with modular arithmetic without looking at code
- [ ] Explain why modulo must be applied at each step
- [ ] Implement modular inverse using Fermat's Little Theorem
- [ ] Compute nPr efficiently with or without precomputation
- [ ] Identify when factorial/permutation formulas apply

---

## Additional Resources

- [CP-Algorithms: Factorial](https://cp-algorithms.com/algebra/factorial-divisors.html)
- [CP-Algorithms: Modular Inverse](https://cp-algorithms.com/algebra/module-inverse.html)
- [CSES Problem Set - Mathematics](https://cses.fi/problemset/list/)
