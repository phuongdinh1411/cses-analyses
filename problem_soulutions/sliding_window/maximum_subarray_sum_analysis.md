---
layout: simple
title: "Maximum Subarray Sum - Kadane's Algorithm"
permalink: /problem_soulutions/sliding_window/maximum_subarray_sum_analysis
difficulty: Easy
tags: [dynamic-programming, greedy, array, kadanes-algorithm]
---

# Maximum Subarray Sum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Maximum Subarray Sum](https://cses.fi/problemset/task/1643) |
| **Difficulty** | Easy |
| **Category** | Dynamic Programming / Greedy |
| **Time Limit** | 1 second |
| **Key Technique** | Kadane's Algorithm |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Implement Kadane's algorithm for maximum subarray sum in O(n) time
- [ ] Understand the "extend or restart" decision pattern in DP
- [ ] Handle edge cases with all-negative arrays
- [ ] Recognize problems where Kadane's algorithm applies

---

## Problem Statement

**Problem:** Given an array of n integers, find the maximum sum of a contiguous subarray.

**Input:**
- Line 1: Integer n (size of the array)
- Line 2: n integers x_1, x_2, ..., x_n

**Output:**
- Maximum sum of any contiguous subarray

**Constraints:**
- 1 <= n <= 2 * 10^5
- -10^9 <= x_i <= 10^9

### Example

```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
9
```

**Explanation:** The subarray [3, -2, 5, 3] has the maximum sum of 9.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** At each position, should we continue the current subarray or start fresh?

The core insight is that a negative running sum never helps. If our current sum becomes negative, any future elements would be better off starting a new subarray rather than carrying the negative baggage.

### Breaking Down the Problem

1. **What are we looking for?** Maximum sum among all contiguous subarrays
2. **What information do we have?** An array of integers (positive and negative)
3. **What's the relationship?** Each position can either extend the previous best or start new

### Analogy

Think of it like tracking your bank balance on a trip. If you go into debt (negative balance), it's better to "restart" with fresh money than to keep carrying that debt forward. Each day you decide: continue with current balance, or start over?

---

## Solution 1: Brute Force

### Idea

Check every possible subarray by trying all start and end positions.

### Algorithm

1. For each starting index i from 0 to n-1
2. For each ending index j from i to n-1
3. Calculate sum of arr[i..j] and track the maximum

### Code

**Python:**
```python
def max_subarray_brute(arr):
  """
  Brute force: check all subarrays.
  Time: O(n^2), Space: O(1)
  """
  n = len(arr)
  max_sum = arr[0]

  for i in range(n):
    current_sum = 0
    for j in range(i, n):
      current_sum += arr[j]
      max_sum = max(max_sum, current_sum)

  return max_sum
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Nested loops over all pairs |
| Space | O(1) | Only tracking current and max sum |

### Why This Works (But Is Slow)

This guarantees correctness by exhaustively checking every subarray. However, O(n^2) is too slow for n = 2 * 10^5.

---

## Solution 2: Kadane's Algorithm (Optimal)

### Key Insight

> **The Trick:** At each position, the best subarray ending here is either:
> (1) extending the previous best, or (2) starting fresh from the current element.

### DP State Definition

| State | Meaning |
|-------|---------|
| `current_sum` | Maximum sum of subarray ending at current position |
| `max_sum` | Global maximum sum found so far |

**In plain English:** We track the "best subarray ending here" and update our overall answer.

### State Transition

```
current_sum = max(arr[i], current_sum + arr[i])
```

**Why?** If `current_sum + arr[i] < arr[i]`, then `current_sum < 0`. A negative prefix hurts us, so we discard it and start fresh.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `current_sum` | arr[0] | First element is its own subarray |
| `max_sum` | arr[0] | Initial best is the first element |

### Algorithm

1. Initialize `current_sum = max_sum = arr[0]`
2. For each element from index 1 to n-1:
   - `current_sum = max(arr[i], current_sum + arr[i])`
   - `max_sum = max(max_sum, current_sum)`
3. Return `max_sum`

### Dry Run Example

Input: `[-1, 3, -2, 5, 3, -5, 2, 2]`

```
Index 0: arr[0] = -1
  current_sum = -1
  max_sum = -1

Index 1: arr[1] = 3
  current_sum = max(3, -1 + 3) = max(3, 2) = 3  [start fresh]
  max_sum = max(-1, 3) = 3

Index 2: arr[2] = -2
  current_sum = max(-2, 3 + (-2)) = max(-2, 1) = 1  [extend]
  max_sum = max(3, 1) = 3

Index 3: arr[3] = 5
  current_sum = max(5, 1 + 5) = max(5, 6) = 6  [extend]
  max_sum = max(3, 6) = 6

Index 4: arr[4] = 3
  current_sum = max(3, 6 + 3) = max(3, 9) = 9  [extend]
  max_sum = max(6, 9) = 9

Index 5: arr[5] = -5
  current_sum = max(-5, 9 + (-5)) = max(-5, 4) = 4  [extend]
  max_sum = max(9, 4) = 9

Index 6: arr[6] = 2
  current_sum = max(2, 4 + 2) = max(2, 6) = 6  [extend]
  max_sum = max(9, 6) = 9

Index 7: arr[7] = 2
  current_sum = max(2, 6 + 2) = max(2, 8) = 8  [extend]
  max_sum = max(9, 8) = 9

Result: 9  (subarray [3, -2, 5, 3])
```

### Visual Diagram

```
Array:  [-1]  [3]  [-2]  [5]  [3]  [-5]  [2]  [2]
         |    |     |    |    |     |    |    |
         v    v     v    v    v     v    v    v
curr:   -1    3     1    6    9     4    6    8
max:    -1    3     3    6    9     9    9    9
              |___________|
              Maximum subarray: [3, -2, 5, 3] = 9
```

### Code

**Python:**
```python
import sys
input = sys.stdin.readline

def solve():
  n = int(input())
  arr = list(map(int, input().split()))

  current_sum = max_sum = arr[0]

  for i in range(1, n):
    current_sum = max(arr[i], current_sum + arr[i])
    max_sum = max(max_sum, current_sum)

  print(max_sum)

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through the array |
| Space | O(1) | Only two variables needed |

---

## Common Mistakes

### Mistake 1: Initializing to 0

```python
# WRONG
current_sum = 0
max_sum = 0

# CORRECT
current_sum = arr[0]
max_sum = arr[0]
```

**Problem:** If all elements are negative, the answer would incorrectly be 0.
**Fix:** Initialize with the first element, not 0.

**Problem:** With n = 2*10^5 and values up to 10^9, sum can reach 2*10^14.
**Fix:** Use `long long` in C++ for the sum variables.

### Mistake 3: Empty Subarray Assumption

```python
# WRONG: Assuming empty subarray with sum 0 is valid
max_sum = max(0, max_sum)

# CORRECT: Problem requires at least one element
# Don't modify max_sum after the loop
```

**Problem:** The problem requires a non-empty subarray.
**Fix:** The answer is the maximum sum found, even if negative.

### Mistake 4: Wrong Update Order

```python
# WRONG
max_sum = max(max_sum, current_sum)  # Updated before current_sum changes
current_sum = max(arr[i], current_sum + arr[i])

# CORRECT
current_sum = max(arr[i], current_sum + arr[i])
max_sum = max(max_sum, current_sum)  # Update after
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `1, [5]` | 5 | Only one subarray possible |
| All negative | `3, [-5, -2, -3]` | -2 | Must pick least negative |
| All positive | `3, [1, 2, 3]` | 6 | Whole array is optimal |
| Mix with zero | `4, [-1, 0, -2, 3]` | 3 | Zero doesn't hurt |
| Large values | `2, [10^9, 10^9]` | 2*10^9 | Test overflow handling |

---

## When to Use This Pattern

### Use Kadane's Algorithm When:
- Finding maximum/minimum sum of contiguous subarray
- Problem has "extend or restart" structure
- Need O(n) time complexity
- Subarray must be non-empty and contiguous

### Don't Use When:
- Subarray has length constraints (use sliding window)
- Looking for subarray with specific sum (use prefix sums + hash map)
- Need the actual subarray indices (need to track start/end)
- Elements can be rearranged (not a subarray problem)

### Pattern Recognition Checklist:
- [ ] Contiguous subarray required? -> Consider Kadane's
- [ ] Optimize sum/product? -> Consider Kadane's variant
- [ ] Length constraint on subarray? -> Use sliding window instead
- [ ] All elements non-negative? -> Whole array is answer (trivial)

---

## Related Problems

### Same Technique (CSES)

| Problem | Key Difference |
|---------|----------------|
| [Maximum Subarray Sum II](https://cses.fi/problemset/task/1644) | Subarray length between a and b |

### Related Concepts (CSES)

| Problem | Technique Connection |
|---------|---------------------|
| [Subarray Sums I](https://cses.fi/problemset/task/1661) | Prefix sums + hash map |
| [Subarray Sums II](https://cses.fi/problemset/task/1662) | Prefix sums with negative numbers |
| [Subarray Divisibility](https://cses.fi/problemset/task/1662) | Prefix sums modulo n |

### Harder Extensions

| Problem | New Concept |
|---------|-------------|
| Maximum Product Subarray | Track min and max (negatives flip sign) |
| Maximum Circular Subarray | Kadane's + total sum - min subarray |
| K Maximum Subarrays | Priority queue or DP |

---

## Key Takeaways

1. **The Core Idea:** At each position, decide to extend or restart based on whether the running sum is positive
2. **Time Optimization:** From O(n^2) brute force to O(n) by reusing previous computation
3. **Space Trade-off:** No extra space needed beyond two variables
4. **Pattern:** "Extend or restart" is a common DP pattern for subarray problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement Kadane's algorithm from memory in under 5 minutes
- [ ] Explain why we restart when current_sum becomes negative
- [ ] Handle the all-negative array case correctly
- [ ] Extend the solution to also return the subarray indices
- [ ] Recognize when a problem can be solved with this pattern
