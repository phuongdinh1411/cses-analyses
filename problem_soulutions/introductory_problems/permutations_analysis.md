---
layout: simple
title: "Permutations - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/permutations_analysis
difficulty: Easy
tags: [construction, permutation, greedy, even-odd]
---

# Permutations

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Constructive Algorithms |
| **Time Limit** | 1 second |
| **Key Technique** | Even-Odd Separation |
| **CSES Link** | [Permutations](https://cses.fi/problemset/task/1070) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when a construction approach is needed vs enumeration
- [ ] Apply even-odd separation to avoid adjacent value constraints
- [ ] Identify and handle edge cases where no solution exists
- [ ] Construct permutations satisfying adjacency constraints efficiently

---

## Problem Statement

**Problem:** Given a number n, construct a permutation of numbers 1 to n such that no two adjacent elements differ by exactly 1. If no such permutation exists, print "NO SOLUTION".

**Input:**
- Line 1: An integer n

**Output:**
- A permutation of integers 1 to n where no adjacent elements differ by 1, or "NO SOLUTION" if impossible

**Constraints:**
- 1 <= n <= 10^6

### Example

```
Input:
5

Output:
4 2 5 3 1
```

**Explanation:** In the sequence [4, 2, 5, 3, 1]:
- |4 - 2| = 2 (not 1)
- |2 - 5| = 3 (not 1)
- |5 - 3| = 2 (not 1)
- |3 - 1| = 2 (not 1)

All adjacent differences are greater than 1, so this is valid.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we arrange numbers so that consecutive integers never appear next to each other?

The insight is that if we separate even and odd numbers into two groups, they naturally differ by at least 2. For example, any even number and any odd number differ by at least 1, but within each group, consecutive members differ by 2.

### Breaking Down the Problem

1. **What are we looking for?** A permutation where |a[i] - a[i+1]| != 1 for all adjacent pairs
2. **What information do we have?** Just the number n
3. **What is the key observation?** Even numbers (2, 4, 6...) and odd numbers (1, 3, 5...) each form sequences where consecutive members differ by 2

### The Even-Odd Separation Strategy

Think of this like organizing people in a line where neighbors must not be direct relatives:
- Put all even-numbered people on one side: 2, 4, 6, 8...
- Put all odd-numbered people on the other side: 1, 3, 5, 7...
- Now adjacent people in each group differ by 2, and the boundary between groups is safe

---

## Solution: Even-Odd Construction

### Key Insight

> **The Trick:** Print all even numbers first, then all odd numbers (or vice versa). Within each group, consecutive elements differ by 2, and at the boundary between groups, the difference is also not 1.

### Why Does This Work?

Consider the sequence: [even numbers] + [odd numbers]
- Within even numbers: 2, 4, 6... adjacent diff = 2
- Within odd numbers: 1, 3, 5... adjacent diff = 2
- At boundary (last even, first odd): For n=5, boundary is (4, 1), diff = 3

The only issue is when n is small and we cannot avoid having consecutive integers adjacent.

### Edge Case Analysis

Let's analyze small values of n:

| n | Possible? | Reason |
|---|-----------|--------|
| 1 | YES | Only [1], no adjacent pairs to check |
| 2 | NO | [1,2] or [2,1] both have diff = 1 |
| 3 | NO | Any arrangement has consecutive integers adjacent |
| 4 | YES | [2,4,1,3] works |
| 5+ | YES | Even-odd separation always works |

**Why n=2 and n=3 fail:**
- n=2: Only two elements, they must be adjacent, diff = 1
- n=3: With elements {1,2,3}, the element 2 is between 1 and 3. In any arrangement, 2 must be adjacent to either 1 or 3

### Algorithm

1. If n == 1: print "1"
2. If n == 2 or n == 3: print "NO SOLUTION"
3. Otherwise:
   - Print all even numbers from 2 to n
   - Print all odd numbers from 1 to n

### Dry Run Example

Let's trace through with input `n = 8`:

```
Step 1: Check edge cases
  n = 8 >= 4, so solution exists

Step 2: Generate even numbers (2 to 8)
  evens = [2, 4, 6, 8]

Step 3: Generate odd numbers (1 to 7)
  odds = [1, 3, 5, 7]

Step 4: Concatenate
  result = [2, 4, 6, 8, 1, 3, 5, 7]

Verification:
  |2-4| = 2  (ok)
  |4-6| = 2  (ok)
  |6-8| = 2  (ok)
  |8-1| = 7  (ok)  <- boundary
  |1-3| = 2  (ok)
  |3-5| = 2  (ok)
  |5-7| = 2  (ok)

All differences != 1. Valid!
```

### Visual Diagram

```
Numbers 1 to 8:  1  2  3  4  5  6  7  8

Separate by parity:
  Evens:  2 -- 4 -- 6 -- 8
                           \
  Odds:   1 -- 3 -- 5 -- 7

Final arrangement: 2  4  6  8  1  3  5  7
                   |--|--|--|--|--|--|--|
Differences:         2  2  2  7  2  2  2
                   All != 1, valid!
```

### Code

**Python:**
```python
def solve(n):
 """
 Construct permutation where no adjacent elements differ by 1.
 Time: O(n), Space: O(n) for output
 """
 if n == 1:
  return "1"
 if n <= 3:
  return "NO SOLUTION"

 # Even numbers first, then odd numbers
 evens = list(range(2, n + 1, 2))
 odds = list(range(1, n + 1, 2))

 return ' '.join(map(str, evens + odds))

n = int(input())
print(solve(n))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass to generate n numbers |
| Space | O(n) | Output storage (or O(1) if printing directly) |

---

## Alternative Construction: Odds First

We can also print odd numbers first, then even numbers:

```python
def solve_odds_first(n):
 if n == 1:
  return "1"
 if n <= 3:
  return "NO SOLUTION"

 odds = list(range(1, n + 1, 2))
 evens = list(range(2, n + 1, 2))

 return ' '.join(map(str, odds + evens))
```

For n=5: Output would be "1 3 5 2 4"
- |1-3| = 2, |3-5| = 2, |5-2| = 3, |2-4| = 2. All valid!

---

## Common Mistakes

### Mistake 1: Forgetting n=1 Edge Case

```python
# WRONG - returns "NO SOLUTION" for n=1
if n <= 3:
 return "NO SOLUTION"

# CORRECT - n=1 is valid
if n == 1:
 return "1"
if n <= 3:
 return "NO SOLUTION"
```

**Problem:** [1] is a valid permutation with no adjacent pairs to check.

### Mistake 2: Incorrect Boundary Check for n=4

```python
# WRONG - some implementations fail at n=4
if n < 4:  # This includes n=4!
 return "NO SOLUTION"

# CORRECT
if n <= 3:  # Only n=2,3 are impossible
 return "NO SOLUTION"
```

**Problem:** n=4 has valid solutions like [2, 4, 1, 3].

### Mistake 3: Wrong Output Format

```python
# WRONG - printing with commas
print(evens + odds)  # [2, 4, 1, 3]

# CORRECT - space-separated
print(' '.join(map(str, evens + odds)))  # 2 4 1 3
```

### Mistake 4: Printing Numbers in Wrong Order

```python
# WRONG - this creates consecutive numbers adjacent
for i in range(1, n + 1):
 print(i, end=' ')

# CORRECT - separate evens and odds
for i in range(2, n + 1, 2): print(i, end=' ')
for i in range(1, n + 1, 2): print(i, end=' ')
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Minimum valid | n=1 | 1 | Single element, no adjacency to check |
| n=2 | n=2 | NO SOLUTION | [1,2] and [2,1] both have diff=1 |
| n=3 | n=3 | NO SOLUTION | 2 must be adjacent to 1 or 3 |
| n=4 | n=4 | 2 4 1 3 | Smallest n with valid solution (n>1) |
| Large n | n=10^6 | 2 4 ... 1 3 ... | Must handle efficiently |
| n=5 | n=5 | 2 4 1 3 5 or 4 2 5 3 1 | Multiple valid outputs |

---

## When to Use This Pattern

### Use Even-Odd Separation When:
- You need to avoid consecutive integers being adjacent
- The constraint involves differences of exactly 1
- You need to construct a valid arrangement, not enumerate all

### Pattern Recognition Checklist:
- [ ] Need permutation with adjacency constraints? -> **Consider construction**
- [ ] Constraint involves difference = 1? -> **Even-odd separation likely works**
- [ ] Small n edge cases? -> **Always check n=1,2,3 manually**

### Related Techniques:
- **Graph Coloring:** Similar parity-based partitioning
- **Bipartite Matching:** Separating into two non-conflicting groups

---

## Related Problems

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Two Sets (CSES)](https://cses.fi/problemset/task/1092) | Partition into equal sums |
| [Missing Number (CSES)](https://cses.fi/problemset/task/1083) | Find missing element |
| [Repetitions (CSES)](https://cses.fi/problemset/task/1069) | Pattern in sequences |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Creating Strings (CSES)](https://cses.fi/problemset/task/1622) | Generate all permutations |
| [Apple Division (CSES)](https://cses.fi/problemset/task/1623) | Subset enumeration |
| [Gray Code (CSES)](https://cses.fi/problemset/task/2205) | Bit manipulation permutation |

---

## Key Takeaways

1. **The Core Idea:** Separate even and odd numbers to ensure no consecutive integers are adjacent
2. **Edge Cases Matter:** n=1 is valid, but n=2 and n=3 are impossible
3. **Construction vs Enumeration:** This problem asks for any valid permutation, not all of them
4. **Pattern:** Even-odd separation is a powerful technique for adjacency constraints

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why n=2 and n=3 have no solution
- [ ] Implement the even-odd separation approach in under 5 minutes
- [ ] Verify the boundary between even and odd groups works
- [ ] Handle all edge cases correctly (n=1, n=4)
