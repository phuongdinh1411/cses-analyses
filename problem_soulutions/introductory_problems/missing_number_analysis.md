---
layout: simple
title: "Missing Number - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/missing_number_analysis
difficulty: Easy
tags: [math, xor, array, sum-formula]
---

# Missing Number

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Math / Bit Manipulation |
| **Time Limit** | 1 second |
| **Key Technique** | Sum Formula / XOR |
| **CSES Link** | [Missing Number](https://cses.fi/problemset/task/1083) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply the arithmetic sum formula n(n+1)/2 to solve missing element problems
- [ ] Use XOR properties to find a single missing element without overflow
- [ ] Choose between sum formula and XOR based on constraints
- [ ] Handle potential integer overflow in mathematical computations

---

## Problem Statement

**Problem:** You are given all numbers from 1 to n except one. Your task is to find the missing number.

**Input:**
- Line 1: An integer n (the range is 1 to n)
- Line 2: n-1 distinct integers, each between 1 and n

**Output:**
- The missing number

**Constraints:**
- 2 <= n <= 2 * 10^5

### Example

```
Input:
5
2 3 1 5

Output:
4
```

**Explanation:** The numbers from 1 to 5 are {1, 2, 3, 4, 5}. We have {1, 2, 3, 5}, so 4 is missing.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** If we know what the complete set should sum to, how can we find what is missing?

The sum of numbers 1 to n is n(n+1)/2. If one number is missing, the difference between the expected sum and the actual sum gives us the missing number.

Alternatively, XOR has a special property: a XOR a = 0. If we XOR all numbers from 1 to n with all given numbers, every number that appears twice cancels out, leaving only the missing number.

### Breaking Down the Problem

1. **What are we looking for?** The single number missing from the sequence 1 to n
2. **What information do we have?** All n-1 numbers that are present
3. **What is the relationship?** Missing = Expected - Actual (for sum) or Missing = XOR of all (for XOR)

---

## Solution 1: Sum Formula Approach

### Idea

Calculate the expected sum of 1 to n using the formula n(n+1)/2, then subtract the sum of given numbers.

### Code

**Python:**
```python
def find_missing_sum(n, arr):
  """
  Time: O(n), Space: O(1)
  """
  expected_sum = n * (n + 1) // 2
  actual_sum = sum(arr)
  return expected_sum - actual_sum

n = int(input())
arr = list(map(int, input().split()))
print(find_missing_sum(n, arr))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass to compute sum |
| Space | O(1) | Only storing sums |

---

## Solution 2: XOR Approach

### Key Insight

> **The Trick:** XOR of a number with itself is 0, and XOR is both commutative and associative.

If we XOR all numbers from 1 to n together, then XOR with all given numbers, each number that appears twice will cancel out (a XOR a = 0), leaving only the missing number.

### Dry Run Example

Let's trace through with input `n = 5, arr = [2, 3, 1, 5]`:

```
Initial: result = 0

XOR with 1 to n:
  result = 0 ^ 1 = 1
  result = 1 ^ 2 = 3
  result = 3 ^ 3 = 0
  result = 0 ^ 4 = 4
  result = 4 ^ 5 = 1

XOR with given array [2, 3, 1, 5]:
  result = 1 ^ 2 = 3
  result = 3 ^ 3 = 0
  result = 0 ^ 1 = 1
  result = 1 ^ 5 = 4

Answer: 4
```

### Visual Diagram

```
Numbers 1-5:    1   2   3   4   5
Given array:    1   2   3   -   5
XOR pairs:     1^1 2^2 3^3     5^5  = 0 each

Unpaired:              4  -> Answer!
```

### Code

**Python:**
```python
def find_missing_xor(n, arr):
  """
  Time: O(n), Space: O(1)
  """
  result = 0
  for i in range(1, n + 1):
    result ^= i
  for num in arr:
    result ^= num
  return result

n = int(input())
arr = list(map(int, input().split()))
print(find_missing_xor(n, arr))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Two passes through data |
| Space | O(1) | Only storing a single integer |

---

## Common Mistakes

### Mistake 1: Integer Overflow with Sum Formula

**Problem:** For n = 2*10^5, the sum is approximately 2*10^10, exceeding int range.

### Mistake 2: 1-Indexed vs 0-Indexed Confusion

```python
# WRONG - starting from 0
for i in range(n):  # 0 to n-1
  result ^= i

# CORRECT - numbers are 1 to n
for i in range(1, n + 1):  # 1 to n
  result ^= i
```

### Mistake 3: Reading Wrong Number of Inputs

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Missing 1 | n=5, arr=[2,3,4,5] | 1 | First number missing |
| Missing n | n=5, arr=[1,2,3,4] | 5 | Last number missing |
| Minimum n | n=2, arr=[1] | 2 | Smallest valid input |
| Large n | n=200000, arr=[1..199999] | 200000 | Test overflow handling |

---

## When to Use This Pattern

### Use Sum Formula When:
- The language has arbitrary precision integers (Python)
- You want the most intuitive solution

### Use XOR When:
- You want to avoid overflow concerns entirely
- Interviewer asks for an alternative approach

### Pattern Recognition Checklist:
- [ ] One element missing from a consecutive sequence? -> **Sum formula or XOR**
- [ ] Two elements missing? -> **Sum + Sum of squares**
- [ ] Finding duplicate instead of missing? -> **Same techniques apply**

---

## Related Problems

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Repetitions](https://cses.fi/problemset/task/1069) | Pattern recognition in strings |
| [Increasing Array](https://cses.fi/problemset/task/1094) | Array manipulation with math |
| [LeetCode 268: Missing Number](https://leetcode.com/problems/missing-number/) | Same problem, 0-indexed |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [LeetCode 287: Find Duplicate](https://leetcode.com/problems/find-the-duplicate-number/) | Floyd's cycle detection |
| [LeetCode 645: Set Mismatch](https://leetcode.com/problems/set-mismatch/) | Find both missing and duplicate |

---

## Key Takeaways

1. **The Core Idea:** Use mathematical properties (sum formula or XOR) to find what is missing
2. **Sum Formula:** Simple but requires overflow handling for large inputs
3. **XOR Approach:** Elegant and overflow-free, leveraging a^a=0 property
4. **Both are O(n) time, O(1) space:** Equally efficient, choose based on context

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement the sum formula approach without looking at the solution
- [ ] Implement the XOR approach and explain why it works
- [ ] Identify potential overflow issues and how to fix them
- [ ] Solve this problem in under 5 minutes
