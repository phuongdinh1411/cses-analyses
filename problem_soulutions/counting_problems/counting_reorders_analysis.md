---
layout: simple
title: "Creating Strings - Counting Problem"
permalink: /problem_soulutions/counting_problems/counting_reorders_analysis
difficulty: Medium
tags: [combinatorics, multinomial, factorial, modular-arithmetic]
---

# Creating Strings / Counting Reorders

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Creating Strings I](https://cses.fi/problemset/task/1622) |
| **Difficulty** | Medium |
| **Category** | Combinatorics |
| **Time Limit** | 1 second |
| **Key Technique** | Multinomial Coefficient / Factorial with Division |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Calculate the number of distinct permutations of a string with repeated characters
- [ ] Apply the multinomial coefficient formula: n! / (c1! * c2! * ... * ck!)
- [ ] Implement modular division using Fermat's Little Theorem (modular inverse)
- [ ] Precompute factorials for efficient repeated calculations

---

## Problem Statement

**Problem:** Given a string of n characters (possibly with duplicates), count the number of distinct ways to reorder its characters.

**Input:**
- Line 1: A string s of length n

**Output:**
- The number of distinct reorderings (permutations) modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 10^6
- String contains lowercase letters a-z

### Example

```
Input:
aabac

Output:
20
```

**Explanation:** The string "aabac" has 5 characters with frequencies: a=3, b=1, c=1. The number of distinct permutations is 5! / (3! * 1! * 1!) = 120 / 6 = 20.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How does having duplicate characters affect the count of permutations?

If all characters were unique, we would have n! permutations. But when characters repeat, many of these permutations look identical. We need to divide by the number of ways to arrange identical characters among themselves.

### Breaking Down the Problem

1. **What are we looking for?** The count of distinct arrangements of characters
2. **What information do we have?** The frequency of each character in the string
3. **What's the relationship?** Total permutations divided by redundant orderings of identical characters

### The Multinomial Coefficient Formula

For a string with character frequencies c1, c2, ..., ck (where c1 + c2 + ... + ck = n):

```
Distinct Permutations = n! / (c1! * c2! * ... * ck!)
```

### Analogy

Imagine arranging 5 people in a row where 3 are identical triplets. Without considering identity, there are 5! = 120 ways. But since the triplets are indistinguishable, we've overcounted by 3! = 6 (the ways to arrange triplets among themselves). So the answer is 120/6 = 20.

---

## Solution 1: Brute Force (Generate All Permutations)

### Idea

Generate all permutations and use a set to count unique ones. Only works for small inputs.

### Code

```python
from itertools import permutations

def count_reorders_brute(s):
 """
 Brute force: generate all permutations and count unique ones.

 Time: O(n! * n) - generates n! permutations, each of length n
 Space: O(n! * n) - stores all unique permutations
 """
 unique = set(permutations(s))
 return len(unique)

# Example
print(count_reorders_brute("aabac"))  # Output: 20
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n! * n) | Generates all permutations |
| Space | O(n! * n) | Stores unique permutations |

### Why This Is Impractical

For n = 10, we have 3,628,800 permutations. For n = 20, it's over 10^18. This approach only works for very small strings.

---

## Solution 2: Optimal (Multinomial Coefficient)

### Key Insight

> **The Trick:** Use the formula n! / (c1! * c2! * ... * ck!) with modular arithmetic to compute the answer in O(n) time.

### Algorithm

1. Count the frequency of each character
2. Compute n! (factorial of string length)
3. For each character frequency ci, divide by ci!
4. Use modular inverse for division under modulo

### Modular Inverse

To compute (a / b) mod p, we compute a * b^(-1) mod p, where b^(-1) = b^(p-2) mod p (by Fermat's Little Theorem, when p is prime).

### Dry Run Example

Let's trace through with input `s = "aabac"`:

```
Step 1: Count frequencies
  freq = {'a': 3, 'b': 1, 'c': 1}
  n = 5

Step 2: Compute n!
  5! = 120

Step 3: Divide by each ci!
  Result = 120 / 3! / 1! / 1!
         = 120 / 6 / 1 / 1
         = 20

With modular arithmetic:
  fact[5] = 120
  result = 120
  result = 120 * inverse(6) mod (10^9+7)
         = 120 * 166666668 mod (10^9+7)
         = 20
```

### Visual Diagram

```
String: "aabac"

Character Frequencies:
  a: |||  (3 times)
  b: |    (1 time)
  c: |    (1 time)

Formula:
       n!           5!        120
  ----------- = --------- = ----- = 20
  c_a! * c_b! * c_c!   3! * 1! * 1!    6

Why divide by 3!?
  The 3 'a's can be arranged among themselves in 3! = 6 ways,
  but all these arrangements look the same in the final string.
```

### Code (Python)

```python
def count_reorders(s):
 """
 Count distinct permutations using multinomial coefficient.

 Time: O(n + 26) = O(n)
 Space: O(n) for factorial array
 """
 MOD = 10**9 + 7
 n = len(s)

 # Precompute factorials
 fact = [1] * (n + 1)
 for i in range(1, n + 1):
  fact[i] = fact[i-1] * i % MOD

 # Count character frequencies
 freq = {}
 for c in s:
  freq[c] = freq.get(c, 0) + 1

 # Compute n! / (c1! * c2! * ... * ck!)
 result = fact[n]
 for count in freq.values():
  # Divide by count! using modular inverse
  result = result * pow(fact[count], MOD - 2, MOD) % MOD

 return result

# Example usage
print(count_reorders("aabac"))  # Output: 20
print(count_reorders("aaaa"))   # Output: 1
print(count_reorders("abcd"))   # Output: 24
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + k log MOD) | n for factorial, k characters with O(log MOD) for each inverse |
| Space | O(n) | Factorial array storage |

---

## Common Mistakes

### Mistake 1: Forgetting Modular Inverse

```python
# WRONG - Integer division doesn't work with modular arithmetic
result = fact[n]
for count in freq.values():
 result = result // fact[count]  # WRONG!
result %= MOD
```

**Problem:** Division and modulo don't commute. (a // b) % MOD != (a % MOD) // (b % MOD)

**Fix:** Use modular inverse: multiply by b^(MOD-2) instead of dividing by b.

### Mistake 2: Overflow in Factorial Computation

**Problem:** Factorial grows extremely fast and overflows even 64-bit integers.

**Fix:** Take modulo at each step: `fact[i] = fact[i-1] * i % MOD;`

### Mistake 3: Not Handling Single Character

```python
# Edge case: all characters are the same
s = "aaaa"
# n! / n! = 1 (only one way to arrange identical items)
```

**Problem:** Some implementations crash or return wrong values for edge cases.

**Fix:** The formula naturally handles this: 4! / 4! = 1.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single character | `"a"` | 1 | Only one arrangement |
| All same | `"aaaa"` | 1 | 4!/4! = 1 |
| All unique | `"abcd"` | 24 | 4!/1!^4 = 24 |
| Two characters | `"ab"` | 2 | 2!/1!/1! = 2 |
| Long repeated | `"aabb"` | 6 | 4!/(2!*2!) = 6 |
| Max length | n = 10^6 | Large number | Test efficiency |

---

## When to Use This Pattern

### Use This Approach When:
- Counting distinct arrangements of items with repetitions
- You need to compute permutations with duplicate elements
- The problem involves distributing identical items into distinct positions

### Don't Use When:
- You need to actually generate all permutations (use backtracking)
- Items have order constraints (use DP)
- Dealing with circular permutations (different formula)

### Pattern Recognition Checklist:
- [ ] Counting arrangements? --> **Consider multinomial coefficient**
- [ ] Items have duplicates? --> **Divide by duplicate factorials**
- [ ] Need modular arithmetic? --> **Use Fermat's Little Theorem for inverse**

---

## Related Problems

### Easier (Do These First)

| Problem | Link | Why It Helps |
|---------|------|--------------|
| Creating Strings I | [CSES 1622](https://cses.fi/problemset/task/1622) | Generate permutations for small n |
| Binomial Coefficients | [CSES 1079](https://cses.fi/problemset/task/1079) | Practice modular inverse |

### Similar Difficulty

| Problem | Link | Key Difference |
|---------|------|----------------|
| Distributing Apples | [CSES 1716](https://cses.fi/problemset/task/1716) | Stars and bars technique |
| Bracket Sequences I | [CSES 2064](https://cses.fi/problemset/task/2064) | Catalan numbers |

### Harder (Do These After)

| Problem | Link | New Concept |
|---------|------|-------------|
| Bracket Sequences II | [CSES 2187](https://cses.fi/problemset/task/2187) | Counting with constraints |
| Counting Necklaces | [CSES 2209](https://cses.fi/problemset/task/2209) | Burnside's lemma |

---

## Key Takeaways

1. **The Core Idea:** Count distinct permutations by dividing total permutations by the permutations of identical elements.

2. **Formula:** For string with frequencies c1, c2, ..., ck: Answer = n! / (c1! * c2! * ... * ck!)

3. **Modular Arithmetic:** Use Fermat's Little Theorem for modular inverse: a^(-1) = a^(p-2) mod p

4. **Time Optimization:** Precompute factorials to avoid redundant calculations.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the multinomial coefficient formula from first principles
- [ ] Implement modular inverse using fast exponentiation
- [ ] Explain why we divide by the factorial of each frequency
- [ ] Handle edge cases (single char, all same, all unique)
- [ ] Solve in O(n) time with O(n) space

---

## Additional Resources

- [CP-Algorithms: Modular Inverse](https://cp-algorithms.com/algebra/module-inverse.html)
- [CP-Algorithms: Factorial & Combinations](https://cp-algorithms.com/combinatorics/binomial-coefficients.html)
- [CSES Creating Strings](https://cses.fi/problemset/task/1715) - Permutation counting
