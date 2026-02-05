---
layout: simple
title: "Apple Division - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/apple_division_analysis
difficulty: Easy
tags: [bitmask, subset-enumeration, brute-force, optimization]
prerequisites: []
---

# Apple Division

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Introductory / Bitmask |
| **Time Limit** | 1 second |
| **Key Technique** | Bitmask Subset Enumeration |
| **CSES Link** | [Apple Division](https://cses.fi/problemset/task/1623) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Enumerate all 2^n subsets using bitmask representation
- [ ] Use bit manipulation to check if an element belongs to a subset
- [ ] Understand when brute force O(2^n) is acceptable based on constraints
- [ ] Apply the partition problem pattern to minimize difference between two groups

---

## Problem Statement

**Problem:** Given n apples with weights, divide them into two groups such that the difference between the total weights of the two groups is minimized.

**Input:**
- Line 1: Integer n (number of apples)
- Line 2: n integers p_1, p_2, ..., p_n (weights of apples)

**Output:**
- Minimum possible absolute difference between the two groups

**Constraints:**
- 1 <= n <= 20
- 1 <= p_i <= 10^9

### Example

```
Input:
5
3 2 7 4 1

Output:
1
```

**Explanation:**
- Group 1: {3, 4, 1} with sum = 8
- Group 2: {2, 7} with sum = 9
- Difference: |8 - 9| = 1

This is the minimum possible difference.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** With n <= 20, we have at most 2^20 = ~1 million subsets. Can we check all of them?

Yes! When n is small (typically n <= 20-25), we can enumerate all possible subsets. Each apple either goes to Group 1 or Group 2, giving us 2^n possible divisions.

### Breaking Down the Problem

1. **What are we looking for?** The minimum absolute difference between two groups
2. **What information do we have?** Weights of n apples
3. **What's the relationship?** If Group 1 has sum S1, Group 2 has sum (Total - S1), difference = |2*S1 - Total|

### Why Bitmask?

A bitmask of n bits can represent which apples go to Group 1:
- Bit i = 1: Apple i goes to Group 1
- Bit i = 0: Apple i goes to Group 2

For n = 3: mask = 5 (binary: 101) means apples 0 and 2 in Group 1, apple 1 in Group 2.

---

## Solution: Bitmask Enumeration

### Key Insight

> **The Trick:** Enumerate all 2^n subsets using integers 0 to 2^n - 1 as bitmasks. For each subset, compute the sum and track the minimum difference.

### Algorithm

1. Compute total sum of all apples
2. For each mask from 0 to 2^n - 1:
   - Calculate sum of apples where bit is set (Group 1)
   - Group 2 sum = Total - Group 1 sum
   - Update minimum difference
3. Return minimum difference

### Dry Run Example

Let's trace through with input `n = 4, weights = [3, 2, 7, 4]`:

```
Total sum = 3 + 2 + 7 + 4 = 16

mask = 0 (binary: 0000)
  Group 1: {} -> sum1 = 0
  Group 2: {3,2,7,4} -> sum2 = 16
  diff = |0 - 16| = 16
  min_diff = 16

mask = 1 (binary: 0001)
  Group 1: {3} -> sum1 = 3
  Group 2: {2,7,4} -> sum2 = 13
  diff = |3 - 13| = 10
  min_diff = 10

mask = 5 (binary: 0101)
  Group 1: {3, 7} -> sum1 = 10
  Group 2: {2, 4} -> sum2 = 6
  diff = |10 - 6| = 4
  min_diff = 4

mask = 6 (binary: 0110)
  Group 1: {2, 7} -> sum1 = 9
  Group 2: {3, 4} -> sum2 = 7
  diff = |9 - 7| = 2
  min_diff = 2

... continue for all 16 masks ...

Final answer: 2
```

### Visual Diagram

```
Apples: [3, 2, 7, 4]  (indices 0, 1, 2, 3)

mask = 6 = 0110 in binary

Bit position:  3  2  1  0
Binary:        0  1  1  0
Apple weight:  4  7  2  3
               |  |  |  |
               v  v  v  v
Group 2       G1 G1 G2

Group 1: indices 1,2 -> weights 2,7 -> sum = 9
Group 2: indices 0,3 -> weights 3,4 -> sum = 7
Difference: |9 - 7| = 2
```

### Code

#### Python Solution

```python
def solve():
    n = int(input())
    weights = list(map(int, input().split()))

    total = sum(weights)
    min_diff = total  # worst case: all in one group

    # Enumerate all 2^n subsets
    for mask in range(1 << n):
        group1_sum = 0

        # Calculate sum for Group 1 (bits that are set)
        for i in range(n):
            if mask & (1 << i):
                group1_sum += weights[i]

        # Group 2 sum is total - group1_sum
        group2_sum = total - group1_sum

        # Update minimum difference
        diff = abs(group1_sum - group2_sum)
        min_diff = min(min_diff, diff)

    print(min_diff)

solve()
```

##### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n * n) | 2^n subsets, each taking O(n) to compute sum |
| Space | O(n) | Only store the weights array |

**Note:** For n = 20, this is approximately 20 million operations, which runs comfortably under 1 second.

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** Each weight can be up to 10^9, and sum of 20 weights can be 2 * 10^10, exceeding int range.
**Fix:** Use `long long` in C++ or Python handles big integers automatically.

### Mistake 2: Forgetting Absolute Value

**Problem:** Difference can be negative if group2 > group1.
**Fix:** Always take absolute value when computing difference.

### Mistake 3: Not Enumerating All Subsets

**Problem:** Missing mask = 0 (all apples in Group 2) could miss valid partitions.
**Fix:** Start enumeration from 0.

### Mistake 4: Wrong Bit Check

**Problem:** Using `==` instead of `&` gives wrong subset membership.
**Fix:** Use bitwise AND to check if bit is set.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single apple | `n=1, [5]` | 5 | One group empty, other has 5 |
| Two equal | `n=2, [5,5]` | 0 | Perfect split possible |
| All same | `n=4, [3,3,3,3]` | 0 | Split into {3,3} and {3,3} |
| Large weights | `n=2, [10^9, 10^9]` | 0 | Test long long handling |
| Odd total | `n=3, [1,2,4]` | 1 | Cannot get 0 difference |
| Maximum n | `n=20, [various]` | varies | Test performance |

---

## When to Use This Pattern

### Use Bitmask Enumeration When:
- n is small (typically n <= 20-25)
- You need to consider all possible subsets
- The problem involves partitioning elements into groups
- No greedy or DP optimization is apparent

### Don't Use When:
- n is large (n > 25) - 2^n becomes too slow
- Sum values are small enough for DP approach
- Problem has special structure allowing greedy solution

### Pattern Recognition Checklist:
- [ ] Small n constraint (n <= 20)? -> **Consider bitmask enumeration**
- [ ] Need to split into two groups? -> **Partition problem pattern**
- [ ] Minimize/maximize some property over all subsets? -> **Enumerate all 2^n subsets**

### Time Limit Guidelines:

| n | 2^n | Feasibility |
|---|-----|-------------|
| 15 | 32,768 | Very fast |
| 20 | 1,048,576 | Fast |
| 25 | 33,554,432 | Borderline |
| 30 | 1,073,741,824 | Too slow |

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Weird Algorithm](https://cses.fi/problemset/task/1068) | Basic implementation practice |
| [Bit Strings](https://cses.fi/problemset/task/1617) | Understanding powers of 2 |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Two Sets](https://cses.fi/problemset/task/1092) | Partition into equal sums, uses math |
| [Chessboard and Queens](https://cses.fi/problemset/task/1624) | Bitmask for different constraint type |
| [Grid Paths](https://cses.fi/problemset/task/1625) | Exhaustive enumeration with pruning |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Meet in the Middle](https://cses.fi/problemset/task/1628) | Split enumeration for n up to 40 |
| [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | DP approach for larger n |
| [Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/) | Similar partition, different framing |

---

## Key Takeaways

1. **The Core Idea:** Use bitmask to represent subset membership and enumerate all 2^n possibilities
2. **Time Optimization:** For this problem size, brute force IS the optimal approach
3. **Space Trade-off:** O(n) space is sufficient; no need to store all subsets
4. **Pattern:** Classic subset enumeration - applicable when n <= 20

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why O(2^n) is acceptable here but not for larger n
- [ ] Write the bitmask enumeration loop from memory
- [ ] Correctly use bit operations: `1 << i`, `mask & (1 << i)`
- [ ] Identify partition problems in disguise
- [ ] Handle integer overflow for large weight sums

---

## Additional Resources

- [CP-Algorithms: Bit Manipulation](https://cp-algorithms.com/algebra/bit-manipulation.html)
- [CSES Apple Division](https://cses.fi/problemset/task/1623) - Subset sum with brute force
- [Bitmask Tutorial - TopCoder](https://www.topcoder.com/thrive/articles/A%20bit%20of%20fun:%20fun%20with%20bits)
