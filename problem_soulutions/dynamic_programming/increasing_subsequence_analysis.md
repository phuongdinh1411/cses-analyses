---
layout: simple
title: "Increasing Subsequence - CSES Problem Analysis"
permalink: /problem_soulutions/dynamic_programming/increasing_subsequence_analysis
difficulty: Medium
tags: [dp, lis, binary-search, subsequence]
prerequisites: []
cses_link: https://cses.fi/problemset/task/1145
---

# Increasing Subsequence (Longest Increasing Subsequence)

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find the length of the longest strictly increasing subsequence |
| Input | Array of n integers |
| Output | Length of LIS |
| Constraints | 1 <= n <= 2x10^5, values up to 10^9 |
| Key Technique | Binary search optimization |
| Time Complexity | O(n log n) optimal, O(n^2) naive |

## Learning Goals

After studying this problem, you should be able to:
1. Implement the O(n^2) DP solution for LIS
2. Understand why and how to optimize to O(n log n) using binary search
3. Know when to use `bisect_left` vs `bisect_right`
4. Apply the LIS pattern to related problems

## Problem Statement

Given an array of n integers, find the length of the longest strictly increasing subsequence.

A subsequence is obtained by deleting some (possibly zero) elements without changing the order of remaining elements.

**Example:**
```
Input:
n = 8
arr = [7, 3, 5, 3, 6, 2, 9, 8]

Output: 4

Explanation:
One LIS is [3, 5, 6, 9] with length 4.
Other valid LIS: [3, 5, 6, 8]
```

## Intuition

The key insight for the DP solution:

**dp[i] = length of the longest increasing subsequence that ENDS at index i**

Why "ends at"? Because to extend a subsequence, we need to know what the last element is. If we track subsequences ending at each position, we can easily check if the current element can extend any previous subsequence.

## O(n^2) Solution: Classic DP

### DP Definition

- **State:** `dp[i]` = length of LIS ending at `arr[i]`
- **Base case:** `dp[i] = 1` (each element alone is a subsequence of length 1)
- **Transition:** For each `j < i` where `arr[j] < arr[i]`:
  ```
  dp[i] = max(dp[i], dp[j] + 1)
  ```
- **Answer:** `max(dp[0], dp[1], ..., dp[n-1])`

### Why This Works

For each position `i`, we look at all previous positions `j`. If `arr[j] < arr[i]`, we can extend the LIS ending at `j` by appending `arr[i]`. We take the maximum over all such possibilities.

### Detailed Dry Run

```
arr = [7, 3, 5, 3, 6, 2, 9, 8]
idx =  0  1  2  3  4  5  6  7

Initialize: dp = [1, 1, 1, 1, 1, 1, 1, 1]

i=0 (arr[0]=7): No previous elements
  dp = [1, 1, 1, 1, 1, 1, 1, 1]

i=1 (arr[1]=3): Check j=0
  arr[0]=7 > 3? No, cannot extend
  dp = [1, 1, 1, 1, 1, 1, 1, 1]

i=2 (arr[2]=5): Check j=0,1
  j=0: arr[0]=7 > 5? No
  j=1: arr[1]=3 < 5? Yes! dp[2] = max(1, dp[1]+1) = 2
  dp = [1, 1, 2, 1, 1, 1, 1, 1]

i=3 (arr[3]=3): Check j=0,1,2
  j=0: 7 > 3? No
  j=1: 3 < 3? No (strictly increasing!)
  j=2: 5 > 3? No
  dp = [1, 1, 2, 1, 1, 1, 1, 1]

i=4 (arr[4]=6): Check j=0,1,2,3
  j=0: 7 > 6? No
  j=1: 3 < 6? Yes! dp[4] = max(1, 1+1) = 2
  j=2: 5 < 6? Yes! dp[4] = max(2, 2+1) = 3
  j=3: 3 < 6? Yes! dp[4] = max(3, 1+1) = 3
  dp = [1, 1, 2, 1, 3, 1, 1, 1]

i=5 (arr[5]=2): Check j=0..4
  No arr[j] < 2
  dp = [1, 1, 2, 1, 3, 1, 1, 1]

i=6 (arr[6]=9): Check j=0..5
  j=0: 7 < 9? Yes! dp[6] = max(1, 1+1) = 2
  j=1: 3 < 9? Yes! dp[6] = max(2, 1+1) = 2
  j=2: 5 < 9? Yes! dp[6] = max(2, 2+1) = 3
  j=3: 3 < 9? Yes! dp[6] = max(3, 1+1) = 3
  j=4: 6 < 9? Yes! dp[6] = max(3, 3+1) = 4
  j=5: 2 < 9? Yes! dp[6] = max(4, 1+1) = 4
  dp = [1, 1, 2, 1, 3, 1, 4, 1]

i=7 (arr[7]=8): Check j=0..6
  Best extension from j=4 (arr[4]=6, dp[4]=3): dp[7] = 4
  dp = [1, 1, 2, 1, 3, 1, 4, 4]

Answer: max(dp) = 4
```

### O(n^2) Code

```python
def lis_n_squared(arr):
  """
  O(n^2) DP solution for Longest Increasing Subsequence

  Time: O(n^2)
  Space: O(n)
  """
  n = len(arr)
  if n == 0:
    return 0

  # dp[i] = length of LIS ending at index i
  dp = [1] * n

  for i in range(1, n):
    for j in range(i):
      if arr[j] < arr[i]:  # Strictly increasing
        dp[i] = max(dp[i], dp[j] + 1)

  return max(dp)


# Example
arr = [7, 3, 5, 3, 6, 2, 9, 8]
print(lis_n_squared(arr))  # Output: 4
```

## O(n log n) Solution: Binary Search Optimization

The O(n^2) solution is too slow for n = 2x10^5. We need O(n log n).

### Key Idea: The `tails` Array

Maintain an array `tails` where:
- `tails[i]` = **smallest ending element** of all increasing subsequences of length `i+1`

**Why "smallest"?** A smaller ending element gives us more room to extend the subsequence later!

### The Invariant

`tails` is always **sorted in increasing order**.

Why? If we have an increasing subsequence of length k ending at value x, and another of length k+1 ending at value y, then y > x (otherwise we could replace the last element of the longer subsequence with x to get a better subsequence).

### Algorithm

For each element `num` in the array:
1. Binary search for the position where `num` should go in `tails`
2. Use `bisect_left` to find the first position where `tails[pos] >= num`
3. If `pos == len(tails)`: `num` is larger than all elements, extend the array
4. Otherwise: replace `tails[pos]` with `num` (we found a better ending!)

### Why Does This Work?

- When we append: We've found a longer increasing subsequence
- When we replace: We've found a subsequence of the same length but with a smaller ending element (better for future extensions)

The length of `tails` at the end equals the LIS length.

**Important:** `tails` does NOT contain an actual LIS! It contains the smallest ending elements for each length.

### Detailed Dry Run of O(n log n)

```
arr = [7, 3, 5, 3, 6, 2, 9, 8]

tails = []

Process 7:
  bisect_left([], 7) = 0
  pos == len(tails), append
  tails = [7]

Process 3:
  bisect_left([7], 3) = 0
  3 < 7, replace tails[0]
  tails = [3]

Process 5:
  bisect_left([3], 5) = 1
  pos == len(tails), append
  tails = [3, 5]

Process 3:
  bisect_left([3, 5], 3) = 0
  3 == tails[0], replace (no change)
  tails = [3, 5]

Process 6:
  bisect_left([3, 5], 6) = 2
  pos == len(tails), append
  tails = [3, 5, 6]

Process 2:
  bisect_left([3, 5, 6], 2) = 0
  2 < 3, replace tails[0]
  tails = [2, 5, 6]

Process 9:
  bisect_left([2, 5, 6], 9) = 3
  pos == len(tails), append
  tails = [2, 5, 6, 9]

Process 8:
  bisect_left([2, 5, 6, 9], 8) = 3
  8 < 9, replace tails[3]
  tails = [2, 5, 6, 8]

Final tails = [2, 5, 6, 8]
Answer = len(tails) = 4
```

Note: `[2, 5, 6, 8]` is NOT necessarily a valid LIS from our array! The actual LIS could be `[3, 5, 6, 8]` or `[3, 5, 6, 9]`. The `tails` array only gives us the length.

### O(n log n) Code

```python
import bisect

def lis_nlogn(arr):
  """
  O(n log n) solution using binary search

  tails[i] = smallest ending element of all LIS of length i+1

  Time: O(n log n)
  Space: O(n)
  """
  tails = []

  for num in arr:
    # Find position where num should go
    pos = bisect.bisect_left(tails, num)

    if pos == len(tails):
      # num is larger than all elements in tails
      tails.append(num)
    else:
      # Found a better (smaller) ending for length pos+1
      tails[pos] = num

  return len(tails)


# Example
arr = [7, 3, 5, 3, 6, 2, 9, 8]
print(lis_nlogn(arr))  # Output: 4
```

## Why bisect_left (lower_bound) and NOT bisect_right?

This is crucial for **strictly increasing** subsequences:

- `bisect_left(tails, num)` finds the first position where `tails[pos] >= num`
- `bisect_right(tails, num)` finds the first position where `tails[pos] > num`

For strictly increasing (`<`):
- If `num` equals some `tails[pos]`, we want to **replace** it, not extend
- `bisect_left` returns that position, allowing replacement
- `bisect_right` would skip past it, incorrectly extending

**Example:** `tails = [2, 5]`, `num = 5`
- `bisect_left([2, 5], 5) = 1` -> replace `tails[1]` (correct, no change)
- `bisect_right([2, 5], 5) = 2` -> append (WRONG! [2,5,5] is not strictly increasing)

For non-strictly increasing (`<=`), you would use `bisect_right`.

## Common Mistakes

1. **Using `bisect_right` instead of `bisect_left`**
   - For strictly increasing LIS, always use `bisect_left` / `lower_bound`

2. **Thinking `tails` is the actual LIS**
   - `tails` only tells us the length, not the actual subsequence
   - To reconstruct the LIS, you need additional bookkeeping

3. **Off-by-one errors with `tails` indexing**
   - `tails[i]` = smallest ending of LIS of length `i+1` (0-indexed)

4. **Forgetting to handle empty array**
   - Always check for `n == 0`

5. **Wrong comparison for strictly vs non-strictly increasing**
   - Strictly increasing: `arr[j] < arr[i]`
   - Non-strictly increasing: `arr[j] <= arr[i]`

## Complexity Analysis

| Solution | Time | Space | When to Use |
|----------|------|-------|-------------|
| O(n^2) DP | O(n^2) | O(n) | n <= 5000, need actual LIS |
| O(n log n) | O(n log n) | O(n) | Large n, only need length |

## Related Problems

### CSES Problems
- [Towers](https://cses.fi/problemset/task/1073) - LIS variant with stacking
- [Increasing Subsequence](https://cses.fi/problemset/task/1145) - This problem

### LeetCode Problems
- [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) - Classic LIS
- [354. Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) - 2D LIS
- [673. Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) - Count all LIS
- [1964. Find Longest Valid Obstacle Course](https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/) - LIS variant

### Key Patterns
- **LIS** is a fundamental DP pattern
- Many problems reduce to finding LIS in a transformed array
- The O(n log n) technique using binary search is essential for competitive programming
