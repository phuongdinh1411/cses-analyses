---
layout: simple
title: "Trailing Zeros - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/trailing_zeros_analysis
difficulty: Easy
tags: [math, factorial, prime-factorization, legendres-formula]
---

# Trailing Zeros

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [https://cses.fi/problemset/task/1618](https://cses.fi/problemset/task/1618) |
| **Difficulty** | Easy |
| **Category** | Math / Number Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Legendre's Formula (Prime Factorization) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand why trailing zeros come from factors of 10 (= 2 x 5)
- [ ] Apply Legendre's formula to count prime factors in factorials
- [ ] Recognize that counting 5s is sufficient (since 2s are always more abundant)
- [ ] Handle large inputs without computing the actual factorial

---

## Problem Statement

**Problem:** Given an integer n, calculate the number of trailing zeros in n! (n factorial).

**Input:**
- A single integer n

**Output:**
- The number of trailing zeros in n!

**Constraints:**
- 1 <= n <= 10^9

### Example

```
Input:
20

Output:
4
```

**Explanation:** 20! = 2,432,902,008,176,640,000 has 4 trailing zeros.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What creates a trailing zero? A trailing zero appears when a number is divisible by 10.

Since 10 = 2 x 5, each trailing zero requires one factor of 2 and one factor of 5 in the factorial's prime factorization.

### Breaking Down the Problem

1. **What are we looking for?** The count of trailing zeros in n!
2. **What information do we have?** The value of n
3. **What's the relationship between input and output?** Trailing zeros = min(count of 2s, count of 5s) in prime factorization of n!

### The Key Insight

In any factorial, there are always more factors of 2 than factors of 5. Consider:
- Even numbers contribute 2s: 2, 4, 6, 8, 10, ...
- Multiples of 5 contribute 5s: 5, 10, 15, 20, ...

Since every other number is even but only every fifth number is a multiple of 5, **counting factors of 5 is sufficient**.

### Why We Need Legendre's Formula

Simply counting multiples of 5 up to n (i.e., n/5) is NOT enough!

Numbers like 25 = 5^2 contribute TWO factors of 5, 125 = 5^3 contributes THREE, and so on.

**Legendre's Formula:** The number of times prime p divides n! is:

```
floor(n/p) + floor(n/p^2) + floor(n/p^3) + ...
```

For trailing zeros, we apply this with p = 5:

```
trailing_zeros = floor(n/5) + floor(n/25) + floor(n/125) + floor(n/625) + ...
```

---

## Solution: Legendre's Formula

### Algorithm

1. Initialize count = 0
2. Start with power_of_5 = 5
3. While power_of_5 <= n:
   - Add n // power_of_5 to count
   - Multiply power_of_5 by 5
4. Return count

### Dry Run Example

Let's trace through with input `n = 100`:

```
Initial state:
  count = 0
  power_of_5 = 5

Iteration 1: power_of_5 = 5
  100 / 5 = 20 multiples of 5: {5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100}
  count = 0 + 20 = 20
  power_of_5 = 5 * 5 = 25

Iteration 2: power_of_5 = 25
  100 / 25 = 4 multiples of 25: {25, 50, 75, 100}
  These contribute an EXTRA factor of 5 each
  count = 20 + 4 = 24
  power_of_5 = 25 * 5 = 125

Iteration 3: power_of_5 = 125
  125 > 100, loop terminates

Final answer: 24 trailing zeros
```

**Verification:** 100! ends with exactly 24 zeros.

### Visual Diagram

```
n = 100

Factors of 5 in each multiple:
  5:   5^1  -> 1 factor
  10:  5^1  -> 1 factor
  ...
  25:  5^2  -> 2 factors (counted in both n/5 AND n/25)
  ...
  50:  5^2  -> 2 factors
  ...
  125: 5^3  -> 3 factors (but 125 > 100, not included)

Sum: floor(100/5) + floor(100/25) + floor(100/125) + ...
   = 20 + 4 + 0 + ...
   = 24
```

### Code (Python)

```python
def trailing_zeros(n: int) -> int:
 """
 Count trailing zeros in n! using Legendre's formula.

 Time: O(log_5(n)) - we divide by 5 each iteration
 Space: O(1) - only using a few variables
 """
 count = 0
 power_of_5 = 5

 while power_of_5 <= n:
  count += n // power_of_5
  power_of_5 *= 5

 return count


def main():
 n = int(input())
 print(trailing_zeros(n))


if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(log n) | We multiply power_of_5 by 5 each iteration, so at most log_5(n) iterations |
| Space | O(1) | Only using a constant number of variables |

---

## Common Mistakes

### Mistake 1: Only Counting Multiples of 5

```python
# WRONG
def trailing_zeros_wrong(n):
 return n // 5  # Misses extra factors from 25, 125, etc.
```

**Problem:** This only counts numbers divisible by 5 once, but 25 contributes 2 fives, 125 contributes 3, etc.

**Fix:** Use Legendre's formula to count all powers of 5.

**Example:** For n = 25:
- Wrong answer: 25 // 5 = 5
- Correct answer: 25//5 + 25//25 = 5 + 1 = 6

### Mistake 2: Integer Overflow

**Problem:** For n up to 10^9, power_of_5 can exceed INT_MAX.

**Fix:** Use `long long` for power_of_5.

### Mistake 3: Counting Both 2s and 5s

```python
# UNNECESSARY
def trailing_zeros_overcomplicated(n):
 count_2 = sum(n // (2**i) for i in range(1, 32) if 2**i <= n)
 count_5 = sum(n // (5**i) for i in range(1, 14) if 5**i <= n)
 return min(count_2, count_5)
```

**Problem:** While mathematically correct, this is unnecessary work.

**Fix:** Only count 5s - there are always more 2s than 5s in any factorial.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Small n | `n = 1` | 0 | 1! = 1 has no trailing zeros |
| n less than 5 | `n = 4` | 0 | 4! = 24 has no trailing zeros |
| Exactly 5 | `n = 5` | 1 | 5! = 120 has 1 trailing zero |
| Power of 5 | `n = 25` | 6 | 25 contributes extra factor |
| Large n | `n = 10^9` | 249999998 | Must handle without overflow |

---

## When to Use This Pattern

### Use Legendre's Formula When:
- Counting factors of a prime in n!
- Problems involving factorial divisibility
- Questions about trailing zeros in any base (not just 10)

### Variations:
- **Trailing zeros in base B:** Factor B into primes, count limiting prime
- **Largest power of p dividing n!:** Direct application of Legendre's formula
- **Find minimum n such that n! has k trailing zeros:** Binary search + Legendre's

### Pattern Recognition Checklist:
- [ ] Problem involves factorial? -> Consider prime factorization
- [ ] Need to count specific prime factors in n!? -> Use Legendre's formula
- [ ] Trailing zeros in base 10? -> Count factors of 5
- [ ] Trailing zeros in base B? -> Factor B, count the limiting prime

---

## Related Problems

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [LeetCode 172: Factorial Trailing Zeroes](https://leetcode.com/problems/factorial-trailing-zeroes/) | Same problem, smaller constraints |
| [CSES: Counting Divisors](https://cses.fi/problemset/task/1713) | Counting divisors instead of prime factors |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES: Common Divisors](https://cses.fi/problemset/task/1081) | GCD and factorization |
| [LeetCode 793: Preimage Size of Factorial Zeroes](https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/) | Inverse problem using binary search |
| [SPOJ: FACTCG2 - Factorial Trailing Zeros](https://www.spoj.com/problems/FACTCG2/) | Extended constraints |

---

## Key Takeaways

1. **The Core Idea:** Trailing zeros come from factors of 10 = 2 x 5, and since 2s are abundant, count only 5s
2. **Legendre's Formula:** Count of prime p in n! = sum of floor(n/p^k) for k = 1, 2, 3, ...
3. **Time Complexity:** O(log n) - extremely efficient for any input size
4. **Common Trap:** Do not forget higher powers of 5 (25, 125, 625, ...)

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why counting 5s is sufficient (not 2s and 5s)
- [ ] Derive Legendre's formula from first principles
- [ ] Calculate trailing zeros for n = 1000 by hand
- [ ] Implement the solution in under 5 minutes
- [ ] Extend to trailing zeros in other bases

---

## Additional Resources

- [CP-Algorithms: Factorial Divisors](https://cp-algorithms.com/algebra/factorial-divisors.html)
- [Wikipedia: Legendre's Formula](https://en.wikipedia.org/wiki/Legendre%27s_formula)
- [CSES Trailing Zeros](https://cses.fi/problemset/task/1618) - Legendre's formula
