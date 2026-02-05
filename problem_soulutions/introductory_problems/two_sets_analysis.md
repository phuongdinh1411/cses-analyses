---
layout: simple
title: "Two Sets - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/two_sets_analysis
difficulty: Easy
tags: [math, greedy, construction, partition]
prerequisites: []
cses_link: https://cses.fi/problemset/task/1092
---

# Two Sets

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Introductory / Math |
| **Time Limit** | 1 second |
| **Key Technique** | Mathematical analysis + Greedy construction |
| **CSES Link** | [Two Sets](https://cses.fi/problemset/task/1092) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Determine when equal-sum partitioning of {1, 2, ..., n} is possible using divisibility rules
- [ ] Apply the formula for triangular numbers: n*(n+1)/2
- [ ] Construct a valid partition using a greedy approach
- [ ] Understand the n % 4 pattern for partition feasibility

---

## Problem Statement

**Problem:** Given an integer n, divide the numbers 1, 2, ..., n into two sets of equal sum. If this is possible, print the contents of both sets. Otherwise, print "NO".

**Input:**
- Line 1: A single integer n

**Output:**
- If division is not possible: Print "NO"
- If division is possible:
  - Print "YES"
  - Print the size of the first set and its elements
  - Print the size of the second set and its elements

**Constraints:**
- 1 <= n <= 10^6

### Example 1

```
Input:
7

Output:
YES
4
1 2 4 7
3
3 5 6
```

**Explanation:** Set 1 = {1, 2, 4, 7} has sum 1+2+4+7 = 14. Set 2 = {3, 5, 6} has sum 3+5+6 = 14. Both sets have equal sum.

### Example 2

```
Input:
6

Output:
NO
```

**Explanation:** Total sum = 1+2+3+4+5+6 = 21, which is odd. Cannot split into two equal sums.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** When can we split {1, 2, ..., n} into two sets with equal sum?

The total sum of numbers from 1 to n is given by the triangular number formula:
```
Total Sum = n * (n + 1) / 2
```

For two sets to have equal sums, each set must have sum = Total Sum / 2.

**This is only possible when Total Sum is even.**

### Breaking Down the Problem

1. **What are we looking for?** Two sets whose elements partition {1, 2, ..., n} with equal sums.
2. **What information do we have?** The value of n.
3. **What's the relationship between input and output?**
   - If n*(n+1)/2 is odd -> impossible (print "NO")
   - If n*(n+1)/2 is even -> construct the partition (print "YES" + sets)

### The n % 4 Pattern

Let's analyze when the total sum is even:

| n | n*(n+1)/2 | Total Sum | Even? | n % 4 |
|---|-----------|-----------|-------|-------|
| 1 | 1*2/2 | 1 | No | 1 |
| 2 | 2*3/2 | 3 | No | 2 |
| 3 | 3*4/2 | 6 | Yes | 3 |
| 4 | 4*5/2 | 10 | Yes | 0 |
| 5 | 5*6/2 | 15 | No | 1 |
| 6 | 6*7/2 | 21 | No | 2 |
| 7 | 7*8/2 | 28 | Yes | 3 |
| 8 | 8*9/2 | 36 | Yes | 0 |

**Pattern:** The total sum is even if and only if **n % 4 == 0** or **n % 4 == 3**.

**Why?** For n*(n+1)/2 to be even:
- Either n is divisible by 4, OR
- (n+1) is divisible by 4 (i.e., n % 4 == 3)

### Greedy Construction Strategy

Once we know a partition exists, we need to construct it. The greedy approach:

1. Target sum for each set = n*(n+1)/4
2. Start from the largest number n and work down
3. If adding a number to set 1 doesn't exceed target, add it to set 1
4. Otherwise, add it to set 2

This works because at each step, we're making progress toward the target without exceeding it.

---

## Solution: Greedy Construction

### Key Insight

> **The Trick:** Greedily assign numbers from largest to smallest to Set 1 until we reach exactly half the total sum.

### Algorithm

1. Calculate total_sum = n * (n + 1) / 2
2. If total_sum is odd, output "NO" and exit
3. Set target = total_sum / 2
4. Initialize two empty sets
5. For i from n down to 1:
   - If i <= target: add i to Set 1 and subtract i from target
   - Else: add i to Set 2
6. Output both sets

### Dry Run Example

Let's trace through with n = 7:

```
Initial state:
  Total sum = 7 * 8 / 2 = 28
  Target = 28 / 2 = 14
  Set1 = [], Set2 = []
  remaining_target = 14

Step 1: Process i = 7
  7 <= 14? YES
  Add 7 to Set1, remaining_target = 14 - 7 = 7
  Set1 = [7], Set2 = []

Step 2: Process i = 6
  6 <= 7? YES
  Add 6 to Set1, remaining_target = 7 - 6 = 1
  Set1 = [7, 6], Set2 = []

Step 3: Process i = 5
  5 <= 1? NO
  Add 5 to Set2
  Set1 = [7, 6], Set2 = [5]

Step 4: Process i = 4
  4 <= 1? NO
  Add 4 to Set2
  Set1 = [7, 6], Set2 = [5, 4]

Step 5: Process i = 3
  3 <= 1? NO
  Add 3 to Set2
  Set1 = [7, 6], Set2 = [5, 4, 3]

Step 6: Process i = 2
  2 <= 1? NO
  Add 2 to Set2
  Set1 = [7, 6], Set2 = [5, 4, 3, 2]

Step 7: Process i = 1
  1 <= 1? YES
  Add 1 to Set1, remaining_target = 1 - 1 = 0
  Set1 = [7, 6, 1], Set2 = [5, 4, 3, 2]

Final verification:
  Set1 sum = 7 + 6 + 1 = 14
  Set2 sum = 5 + 4 + 3 + 2 = 14
  Both equal! Valid partition found.
```

### Visual Diagram

```
Numbers: 1  2  3  4  5  6  7
         |  |  |  |  |  |  |
         v  v  v  v  v  v  v
Target = 14

Greedy from right to left:
  7 -> Set1 (target left: 14-7=7)
  6 -> Set1 (target left: 7-6=1)
  5 -> Set2 (5 > 1)
  4 -> Set2 (4 > 1)
  3 -> Set2 (3 > 1)
  2 -> Set2 (2 > 1)
  1 -> Set1 (target left: 1-1=0)

Result:
  Set1: {1, 6, 7}  sum = 14
  Set2: {2, 3, 4, 5}  sum = 14
```

### Code

#### Python

```python
def two_sets(n: int) -> None:
    """
    Divide {1, 2, ..., n} into two sets with equal sum.

    Time: O(n)
    Space: O(n) for storing the two sets
    """
    total_sum = n * (n + 1) // 2

    # Check if partition is possible
    if total_sum % 2 == 1:
        print("NO")
        return

    target = total_sum // 2
    set1 = []
    set2 = []

    # Greedy: assign from largest to smallest
    for i in range(n, 0, -1):
        if i <= target:
            set1.append(i)
            target -= i
        else:
            set2.append(i)

    # Output result
    print("YES")
    print(len(set1))
    print(*set1)
    print(len(set2))
    print(*set2)


# Main
if __name__ == "__main__":
    n = int(input())
    two_sets(n)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through numbers n to 1 |
| Space | O(n) | Store up to n numbers in two sets |

---

## Alternative Solution: Pattern-Based Construction

For cases where n % 4 == 0 or n % 4 == 3, we can use a pattern-based approach that groups consecutive numbers.

### Key Observation

When n % 4 == 0 or n % 4 == 3, we can pair numbers cleverly:
- Pair (1, 2) with (3, 4): 1+4 = 5, 2+3 = 5
- Pair (5, 6) with (7, 8): 5+8 = 13, 6+7 = 13

### Pattern for n % 4 == 0

Group every 4 consecutive numbers {4k-3, 4k-2, 4k-1, 4k}:
- Set 1 gets: 4k-3 and 4k (first and last)
- Set 2 gets: 4k-2 and 4k-1 (middle two)

Sum in Set 1: (4k-3) + 4k = 8k - 3
Sum in Set 2: (4k-2) + (4k-1) = 8k - 3

Equal for each group!

### Pattern for n % 4 == 3

Handle numbers 1, 2, 3 specially:
- Set 1 gets: 1, 2
- Set 2 gets: 3

Then apply the n % 4 == 0 pattern for remaining numbers 4 to n.

### Code (Pattern-Based)

```python
def two_sets_pattern(n: int) -> None:
    """
    Pattern-based construction for Two Sets problem.

    Time: O(n)
    Space: O(n)
    """
    total_sum = n * (n + 1) // 2

    if total_sum % 2 == 1:
        print("NO")
        return

    set1 = []
    set2 = []

    start = 1

    # Handle n % 4 == 3 case specially
    if n % 4 == 3:
        set1.extend([1, 2])
        set2.append(3)
        start = 4

    # Process groups of 4
    for i in range(start, n + 1, 4):
        # Group: i, i+1, i+2, i+3
        set1.extend([i, i + 3])      # First and last
        set2.extend([i + 1, i + 2])  # Middle two

    print("YES")
    print(len(set1))
    print(*set1)
    print(len(set2))
    print(*set2)


if __name__ == "__main__":
    n = int(input())
    two_sets_pattern(n)
```

---

## Common Mistakes

### Mistake 1: Forgetting the n % 4 Check

```python
# WRONG - Only checking if n is even
if n % 2 == 0:
    # This is incorrect! n=2 has sum 3 which is odd
    construct_partition()
```

**Problem:** n=2 has total sum 3, which is odd and impossible to partition.
**Fix:** Check if n*(n+1)/2 is even, or equivalently, if n % 4 == 0 or n % 4 == 3.

### Mistake 2: Integer Overflow

**Problem:** For n = 10^6, n*(n+1) exceeds int range.
**Fix:** Use long long in C++ or Python's arbitrary precision integers.

### Mistake 3: Incorrect Output Format

```python
# WRONG - Wrong output order
print(len(set1), set1)  # Should be on separate lines

# CORRECT
print(len(set1))
print(*set1)
```

**Problem:** CSES expects specific output format with sizes and elements on separate lines.
**Fix:** Follow the exact output format specified in the problem.

### Mistake 4: Greedy Going in Wrong Direction

```python
# WRONG - Starting from 1
for i in range(1, n + 1):
    if i <= target:
        set1.append(i)
        target -= i

# This fails because small numbers fill up before we can add large ones
```

**Problem:** Starting from small numbers, we might add too many before we can fit larger ones.
**Fix:** Always iterate from n down to 1 for the greedy approach.

---

## Edge Cases

| Case | Input (n) | Total Sum | n % 4 | Output | Reason |
|------|-----------|-----------|-------|--------|--------|
| Smallest impossible | 1 | 1 | 1 | NO | Odd sum |
| Small impossible | 2 | 3 | 2 | NO | Odd sum |
| Smallest possible | 3 | 6 | 3 | YES: {1,2} {3} | Even sum |
| n % 4 == 0 | 4 | 10 | 0 | YES: {1,4} {2,3} | Even sum |
| Large n % 4 == 1 | 5 | 15 | 1 | NO | Odd sum |
| Large n % 4 == 2 | 6 | 21 | 2 | NO | Odd sum |
| Large n % 4 == 3 | 7 | 28 | 3 | YES | Even sum |
| Large n % 4 == 0 | 8 | 36 | 0 | YES | Even sum |

---

## When to Use This Pattern

### Use This Approach When:
- You need to partition a range of consecutive integers
- The problem asks for construction (finding an actual partition)
- You can determine feasibility using a simple mathematical condition

### Don't Use When:
- You need to count the number of partitions (use DP instead - see Two Sets II)
- The elements are not consecutive integers
- The problem involves minimizing difference (different approach needed)

### Pattern Recognition Checklist:
- [ ] Partitioning consecutive integers {1, ..., n}? -> Check n % 4 pattern
- [ ] Need to construct actual sets? -> Use greedy from largest to smallest
- [ ] Need to count partitions? -> Use subset sum DP (Two Sets II)
- [ ] Elements have arbitrary values? -> Different problem (subset sum / partition)

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Missing Number](https://cses.fi/problemset/task/1083) | Uses triangular number formula |
| [Permutations](https://cses.fi/problemset/task/1070) | Basic construction problem |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Apple Division](https://cses.fi/problemset/task/1623) | Arbitrary weights, minimize difference |
| [Coin Piles](https://cses.fi/problemset/task/1754) | Different mathematical condition |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Two Sets II](https://cses.fi/problemset/task/1093) | Count ways using DP |
| [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Boolean DP, arbitrary elements |
| [Money Sums](https://cses.fi/problemset/task/1745) | Find all achievable sums |

---

## Key Takeaways

1. **Mathematical Foundation:** Total sum n*(n+1)/2 must be even for equal partition
2. **n % 4 Pattern:** Partition possible only when n % 4 == 0 or n % 4 == 3
3. **Greedy Construction:** Process from largest to smallest for correct partition
4. **Verification:** Sum of both sets should equal n*(n+1)/4 each

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why n % 4 determines partition feasibility
- [ ] Implement the greedy construction without looking at the solution
- [ ] Handle the output format correctly
- [ ] Solve the problem in under 5 minutes

---

## Additional Resources

- [CP-Algorithms: Triangular Numbers](https://cp-algorithms.com/algebra/triangular-numbers.html)
- [CSES Two Sets](https://cses.fi/problemset/task/1092) - Partition into equal sums
- [Two Sets II Analysis](../dynamic_programming/two_sets_ii_analysis) - Counting version of this problem
