---
layout: simple
title: "Minimum Subarray Sum - Modified Kadane's Algorithm"
permalink: /problem_soulutions/sliding_window/minimum_subarray_sum_analysis
difficulty: Medium
tags: [dynamic-programming, kadane, subarray, greedy]
---

# Minimum Subarray Sum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Dynamic Programming / Array |
| **Time Limit** | 1 second |
| **Key Technique** | Modified Kadane's Algorithm |
| **CSES Link** | [Maximum Subarray Sum](https://cses.fi/problemset/task/1643) (variant) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply modified Kadane's algorithm to find minimum subarray sum
- [ ] Recognize the duality between maximum and minimum subarray problems
- [ ] Make optimal local decisions (extend vs. restart) at each step
- [ ] Achieve O(n) time and O(1) space for subarray optimization problems

---

## Problem Statement

**Problem:** Given an array of integers, find the contiguous subarray (containing at least one number) which has the smallest sum and return its sum.

**Input:**
- Line 1: n (number of elements)
- Line 2: n integers separated by spaces

**Output:**
- Single integer: minimum sum of any contiguous subarray

**Constraints:**
- 1 <= n <= 10^5
- -10^4 <= arr[i] <= 10^4

### Example

```
Input:
6
-2 1 -3 4 -1 2

Output:
-4
```

**Explanation:** The subarray `[-2, 1, -3]` has sum = -2 + 1 + (-3) = -4, which is the minimum among all contiguous subarrays.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** At each position, should we extend the current subarray or start fresh?

This is the **inverse of the classic Maximum Subarray problem**. Instead of keeping sums positive, we want to keep sums negative to minimize the total.

### Breaking Down the Problem

1. **What are we looking for?** The minimum sum of any contiguous subarray
2. **What information do we have?** Array of integers (positive, negative, or zero)
3. **What's the relationship?** At each position, the minimum ending there is either:
   - Just the current element (start fresh), OR
   - Current element + previous minimum (extend)

### Analogies

Think of this like tracking your worst spending streak. At each day, you decide: "Should I count this as part of my current bad streak, or is starting fresh worse?"

**Key Insight for Kadane's:**
- For **maximum**: Reset when sum goes negative (can't help)
- For **minimum**: Reset when sum goes positive (can't hurt more)

---

## Solution 1: Brute Force

### Idea

Check all possible subarrays and track the minimum sum found.

### Algorithm

1. For each starting index i (0 to n-1)
2. For each ending index j (i to n-1)
3. Calculate sum of subarray [i..j]
4. Update minimum if current sum is smaller

### Code

```python
def min_subarray_brute(arr):
  """
  Brute force: Check all subarrays.
  Time: O(n^2), Space: O(1)
  """
  n = len(arr)
  min_sum = float('inf')

  for i in range(n):
    current_sum = 0
    for j in range(i, n):
      current_sum += arr[j]
      min_sum = min(min_sum, current_sum)

  return min_sum
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Two nested loops |
| Space | O(1) | Only tracking current and min sum |

### Why This Works (But Is Slow)

Correctness is guaranteed because we examine every possible subarray. However, for n = 10^5, this gives 10^10 operations - far too slow.

---

## Solution 2: Optimal - Modified Kadane's Algorithm

### Key Insight

> **The Trick:** At each position, decide whether extending the current subarray or starting fresh gives a smaller sum.

### DP State Definition

| State | Meaning |
|-------|---------|
| `current_min` | Minimum sum of subarray **ending at current position** |
| `global_min` | Minimum sum found **anywhere so far** |

**In plain English:** `current_min` answers "What's the smallest sum I can achieve if the subarray must end here?"

### State Transition

```
current_min = min(arr[i], current_min + arr[i])
```

**Why?**
- `arr[i]` = Start a new subarray here
- `current_min + arr[i]` = Extend the previous minimum subarray

We pick whichever gives the smaller value.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `current_min` | arr[0] | First element is the only option |
| `global_min` | arr[0] | Best we've seen so far |

### Algorithm

1. Initialize `current_min = global_min = arr[0]`
2. For each element from index 1 to n-1:
   - `current_min = min(arr[i], current_min + arr[i])`
   - `global_min = min(global_min, current_min)`
3. Return `global_min`

### Dry Run Example

Let's trace through with input `arr = [-2, 1, -3, 4, -1, 2]`:

```
Initial state:
  current_min = -2
  global_min = -2

Step 1: arr[1] = 1
  Option A: Start fresh = 1
  Option B: Extend = -2 + 1 = -1
  current_min = min(1, -1) = -1
  global_min = min(-2, -1) = -2

Step 2: arr[2] = -3
  Option A: Start fresh = -3
  Option B: Extend = -1 + (-3) = -4
  current_min = min(-3, -4) = -4    <-- Extending is better!
  global_min = min(-2, -4) = -4     <-- New minimum found!

Step 3: arr[3] = 4
  Option A: Start fresh = 4
  Option B: Extend = -4 + 4 = 0
  current_min = min(4, 0) = 0       <-- Extending still better
  global_min = min(-4, 0) = -4

Step 4: arr[4] = -1
  Option A: Start fresh = -1
  Option B: Extend = 0 + (-1) = -1
  current_min = min(-1, -1) = -1    <-- Same either way
  global_min = min(-4, -1) = -4

Step 5: arr[5] = 2
  Option A: Start fresh = 2
  Option B: Extend = -1 + 2 = 1
  current_min = min(2, 1) = 1
  global_min = min(-4, 1) = -4

Final answer: -4
```

### Visual Diagram

```
Array: [-2,  1, -3,  4, -1,  2]
Index:   0   1   2   3   4   5

current_min at each step:
        -2  -1  -4   0  -1   1
             ↓   ↓
            These form the minimum subarray

Minimum subarray: [-2, 1, -3] = -4
                   └────────┘
```

### Code

```python
def min_subarray_sum(arr):
  """
  Modified Kadane's algorithm for minimum subarray sum.

  Time: O(n) - single pass
  Space: O(1) - only two variables
  """
  if not arr:
    return 0

  current_min = global_min = arr[0]

  for i in range(1, len(arr)):
    # Decide: extend current subarray or start new
    current_min = min(arr[i], current_min + arr[i])
    # Update global minimum
    global_min = min(global_min, current_min)

  return global_min


# CSES-style I/O
def solve():
  n = int(input())
  arr = list(map(int, input().split()))
  print(min_subarray_sum(arr))

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass through array |
| Space | O(1) | Only two variables regardless of input size |

---

## Common Mistakes

### Mistake 1: Confusing with Maximum Subarray Logic

```python
# WRONG - This finds MAXIMUM, not minimum
current = max(arr[i], current + arr[i])
```

**Problem:** Using `max` instead of `min` finds the maximum subarray sum.
**Fix:** Use `min` for minimum subarray sum.

### Mistake 2: Not Handling Single Element Arrays

```python
# WRONG - Crashes on empty array
def min_subarray(arr):
  current_min = global_min = arr[0]  # IndexError if empty!
```

**Problem:** No check for empty input.
**Fix:** Add `if not arr: return 0` at the start.

**Problem:** With n=10^5 elements of magnitude 10^4, sum can reach 10^9.
**Fix:** Use `long long` for sum variables.

### Mistake 4: Wrong Initialization

```python
# WRONG - Initializing to 0
current_min = 0
global_min = 0
```

**Problem:** If all elements are positive, minimum is the smallest element, not 0.
**Fix:** Initialize with `arr[0]`.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `[5]` | 5 | Only one choice |
| All negative | `[-1, -2, -3]` | -6 | Entire array |
| All positive | `[1, 2, 3]` | 1 | Smallest single element |
| Mixed | `[-2, 1, -3]` | -4 | Optimal subarray spans multiple |
| Single negative | `[-5]` | -5 | Only one choice |
| Zero present | `[0, -1, 0]` | -1 | Zero doesn't help minimize |
| Large values | `[-10^4] * 10^5` | -10^9 | Check for overflow |

---

## When to Use This Pattern

### Use Modified Kadane's When:
- Finding minimum/maximum contiguous subarray sum
- Need O(n) time and O(1) space
- Subarray must be contiguous (no skipping elements)
- Looking for optimal substructure with local decisions

### Don't Use When:
- Non-contiguous subsequence allowed (use different DP)
- Need to find the actual subarray indices (need extra tracking)
- Multiple constraints (length, specific values)
- Need all subarrays with minimum sum

### Pattern Recognition Checklist:
- [ ] Looking for min/max of **contiguous** subarray? -> **Kadane's**
- [ ] Can extend or restart at each position? -> **Kadane's**
- [ ] Need O(n) single-pass solution? -> **Kadane's**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Maximum Subarray Sum (CSES)](https://cses.fi/problemset/task/1643) | Classic Kadane's - learn the pattern |
| [Maximum Subarray (LeetCode 53)](https://leetcode.com/problems/maximum-subarray/) | Same problem, max instead of min |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Track both min and max products |
| [Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) | Array wraps around |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Subarray Sums I (CSES)](https://cses.fi/problemset/task/1660) | Count subarrays with target sum |
| [Subarray Sums II (CSES)](https://cses.fi/problemset/task/1661) | Handle negative numbers |
| [Subarray Divisibility (CSES)](https://cses.fi/problemset/task/1662) | Modular arithmetic with prefix sums |

---

## Key Takeaways

1. **The Core Idea:** At each position, choose whether to extend the current subarray or start fresh - pick whichever gives the smaller (for min) or larger (for max) sum.

2. **Time Optimization:** From O(n^2) brute force to O(n) by avoiding redundant recalculations.

3. **Space Trade-off:** No extra space needed - O(1) with just two variables.

4. **Pattern:** This is a **greedy/DP hybrid** - optimal substructure with local greedy choices.

5. **Duality:** Maximum and minimum subarray problems are mirrors - just swap `max` and `min`.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why we use `min(arr[i], current_min + arr[i])`
- [ ] Convert between maximum and minimum versions
- [ ] Handle all edge cases (empty, single element, all same sign)
- [ ] Implement in both Python and C++ in under 5 minutes

---

## Complexity Comparison

| Approach | Time | Space | When to Use |
|----------|------|-------|-------------|
| Brute Force | O(n^2) | O(1) | Understanding only |
| Prefix Sum | O(n^2) | O(n) | Need all subarray sums |
| **Kadane's** | **O(n)** | **O(1)** | **Optimal for min/max subarray** |
