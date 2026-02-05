---
layout: simple
title: "Maximum Subarray Sum"
permalink: /problem_soulutions/sorting_and_searching/maximum_subarray_sum_analysis
difficulty: Easy
tags: [dp, kadane, subarray]
cses_link: https://cses.fi/problemset/task/1643
---

# Maximum Subarray Sum

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find maximum sum of any contiguous subarray |
| Input | n integers (can be negative) |
| Output | Maximum subarray sum |
| Constraints | 1 <= n <= 2x10^5, -10^9 <= a_i <= 10^9 |
| Key Algorithm | Kadane's Algorithm |
| Time Complexity | O(n) |
| Space Complexity | O(1) |

## Learning Goals

By the end of this analysis, you will understand:
- **Kadane's Algorithm**: The classic O(n) solution for maximum subarray sum
- **Optimal Substructure**: How the maximum subarray ending at position i relates to position i-1
- **Local vs Global Decisions**: When to extend vs start fresh

## Problem Statement

Given an array of n integers (which can include negative numbers), find the maximum sum of any contiguous subarray. The subarray must contain at least one element.

**Example:**
```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
9

Explanation: The subarray [3, -2, 5, 3] has sum = 9
```

## Key Insight

At each position i, we face a simple choice:
1. **Extend** the previous subarray by adding arr[i]
2. **Start fresh** with a new subarray beginning at arr[i]

The decision is straightforward: if the previous subarray sum is negative, it can only hurt us - so we start fresh. Otherwise, we extend.

## Kadane's Algorithm

The algorithm maintains two values:
- `current_sum`: Maximum subarray sum ending at current position
- `max_sum`: Global maximum found so far

**Core Logic:**
```
current_sum = max(arr[i], current_sum + arr[i])
max_sum = max(max_sum, current_sum)
```

## Why It Works

Consider position i with `current_sum` representing the best subarray ending at i-1:

- If `current_sum < 0`: Adding it to arr[i] makes the sum smaller than arr[i] alone
  - Better to start fresh: `current_sum = arr[i]`

- If `current_sum >= 0`: Adding it to arr[i] can only help or stay the same
  - Extend the subarray: `current_sum = current_sum + arr[i]`

This greedy choice at each step leads to the optimal global solution.

## Handling All-Negative Arrays

A common pitfall: initializing `max_sum = 0` fails when all elements are negative.

```
Array: [-3, -1, -4, -2]
Wrong answer (with max_sum = 0): 0
Correct answer: -1 (the maximum single element)
```

**Solution:** Initialize both `current_sum` and `max_sum` to the first element.

## Visual Diagram: Algorithm Progression

```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]
Index:   0  1   2  3  4   5  6  7

Step-by-step visualization:

Index 0: arr[i] = -1
         current_sum = -1 (start)
         max_sum = -1
         Subarray: [-1]

Index 1: arr[i] = 3
         current_sum = max(3, -1+3) = max(3, 2) = 3
         max_sum = max(-1, 3) = 3
         Subarray: [3] (started fresh since -1 < 0)

Index 2: arr[i] = -2
         current_sum = max(-2, 3+(-2)) = max(-2, 1) = 1
         max_sum = max(3, 1) = 3
         Subarray: [3, -2]

Index 3: arr[i] = 5
         current_sum = max(5, 1+5) = max(5, 6) = 6
         max_sum = max(3, 6) = 6
         Subarray: [3, -2, 5]

Index 4: arr[i] = 3
         current_sum = max(3, 6+3) = max(3, 9) = 9
         max_sum = max(6, 9) = 9
         Subarray: [3, -2, 5, 3]  <-- Maximum found!

Index 5: arr[i] = -5
         current_sum = max(-5, 9+(-5)) = max(-5, 4) = 4
         max_sum = max(9, 4) = 9
         Subarray: [3, -2, 5, 3, -5]

Index 6: arr[i] = 2
         current_sum = max(2, 4+2) = max(2, 6) = 6
         max_sum = max(9, 6) = 9
         Subarray: [3, -2, 5, 3, -5, 2]

Index 7: arr[i] = 2
         current_sum = max(2, 6+2) = max(2, 8) = 8
         max_sum = max(9, 8) = 9
         Subarray: [3, -2, 5, 3, -5, 2, 2]

Final Answer: 9
```

## Dry Run with Negative Numbers

```
Array: [-2, -3, 4, -1, -2, 1, 5, -3]

| i | arr[i] | current_sum calculation      | current_sum | max_sum |
|---|--------|------------------------------|-------------|---------|
| 0 | -2     | (initialize)                 | -2          | -2      |
| 1 | -3     | max(-3, -2+(-3)) = max(-3,-5)| -3          | -2      |
| 2 |  4     | max(4, -3+4) = max(4, 1)     | 4           | 4       |
| 3 | -1     | max(-1, 4+(-1)) = max(-1, 3) | 3           | 4       |
| 4 | -2     | max(-2, 3+(-2)) = max(-2, 1) | 1           | 4       |
| 5 |  1     | max(1, 1+1) = max(1, 2)      | 2           | 4       |
| 6 |  5     | max(5, 2+5) = max(5, 7)      | 7           | 7       |
| 7 | -3     | max(-3, 7+(-3)) = max(-3, 4) | 4           | 7       |

Answer: 7 (subarray [4, -1, -2, 1, 5])
```

## Python Implementation

```python
def max_subarray_sum(arr):
  """
  Find maximum subarray sum using Kadane's algorithm.

  Args:
    arr: List of integers (can be negative)

  Returns:
    Maximum sum of any contiguous subarray
  """
  if not arr:
    return 0

  current_sum = max_sum = arr[0]

  for i in range(1, len(arr)):
    # Either extend previous subarray or start fresh
    current_sum = max(arr[i], current_sum + arr[i])
    max_sum = max(max_sum, current_sum)

  return max_sum


# CSES solution with input handling
def solve():
  n = int(input())
  arr = list(map(int, input().split()))
  print(max_subarray_sum(arr))


if __name__ == "__main__":
  solve()
```

## Common Mistakes

### Mistake 1: Initializing max_sum to 0

```python
# WRONG - fails for all-negative arrays
max_sum = 0
current_sum = 0
for x in arr:
  current_sum = max(x, current_sum + x)
  max_sum = max(max_sum, current_sum)

# Array: [-5, -2, -3] -> Returns 0 (wrong!)
# Correct answer: -2
```

**Fix:** Initialize to `arr[0]`, not 0.

### Mistake 2: Forgetting to handle empty arrays

```python
# WRONG - crashes on empty input
current_sum = max_sum = arr[0]  # IndexError!
```

**Fix:** Add an empty array check at the start.

### Mistake 3: Using int instead of long long (C++)

With constraints up to 2x10^5 elements and values up to 10^9, the sum can exceed 32-bit integer range.

## Complexity Analysis

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through the array |
| Space | O(1) | Only two variables maintained |

This is optimal - we must read each element at least once, so O(n) time is the best possible.

## Related Problems

- **Maximum Subarray Sum II** (CSES): Find max sum with length constraints
- **Maximum Circular Subarray Sum**: Handle wrap-around subarrays
- **Maximum Product Subarray**: Similar approach but for products
