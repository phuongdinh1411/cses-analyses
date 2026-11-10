---
layout: simple
title: "Maximum of Sliding Window Minimums"
permalink: /problem_soulutions/sliding_window/maximum_of_sliding_window_minimums
difficulty: Medium
tags: [sliding-window, monotonic-deque, array, worldquant]
---

# Maximum of Sliding Window Minimums

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window |
| **Key Technique** | Monotonic Deque |
| **Related** | Sliding Window Minimum, Subarray Minimums |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Extend the sliding window minimum pattern to answer global queries
- [ ] Use a monotonic deque to compute per-window minimums in O(n)
- [ ] Track a running maximum over a stream of computed values
- [ ] Recognise "max of mins" / "min of maxs" patterns in interview problems

---

## Problem Statement

Given an integer array `nums` and an integer `k`, slide a window of size `k` across the array from left to right. For each window position, find the **minimum** value within that window. Return the **maximum** value among all those window minimums.

**Input:**
- An integer array `nums` of length `n`
- An integer `k` (window size)

**Output:**
- A single integer: the maximum of all window minimums

**Constraints:**
- `1 <= k <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

---

## Examples

### Example 1

```
Input:  nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
Output: 3

Explanation:
Window position             Min
[1  3  -1] -3  5  3  6  7  →  -1
 1 [3  -1  -3] 5  3  6  7  →  -3
 1  3 [-1  -3  5] 3  6  7  →  -3
 1  3  -1 [-3  5  3] 6  7  →  -3
 1  3  -1  -3 [5  3  6] 7  →   3
 1  3  -1  -3  5 [3  6  7] →   3

Window minimums = [-1, -3, -3, -3, 3, 3]
Maximum of minimums = 3
```

### Example 2

```
Input:  nums = [4, 2, 1, 3, 5], k = 2
Output: 3

Explanation:
Window minimums = [2, 1, 1, 3]
Maximum of minimums = 3
```

### Example 3

```
Input:  nums = [1], k = 1
Output: 1
```

---

## Approach: Monotonic Deque + Running Max

### Key Insight

This is a two-step problem:
1. Compute the **minimum of each window** efficiently using a monotonic deque → O(n)
2. Track the **maximum** of those minimums as they are produced → O(1) per window

The monotonic deque maintains indices of elements in **increasing order** of their values. The front of the deque always holds the index of the current window's minimum.

### Algorithm

```
1. Initialise an empty deque and result = -infinity
2. For each index i from 0 to n-1:
   a. Remove indices from the back of the deque while nums[deque.back] >= nums[i]
      (maintain increasing order — larger values can never be the minimum)
   b. Append i to the back of the deque
   c. Remove the front of the deque if it is outside the window (index <= i - k)
   d. Once the first full window is reached (i >= k-1):
      - current window minimum = nums[deque.front]
      - update result = max(result, window minimum)
3. Return result
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n) — each element enters and leaves the deque at most once |
| **Space** | O(k) — at most k indices in the deque at any time |

---

## Implementation

### Python

```python
from collections import deque

def max_of_sliding_window_minimums(nums: list[int], k: int) -> int:
    dq = deque()   # stores indices, values in increasing order
    result = float('-inf')

    for i, val in enumerate(nums):
        # Maintain increasing order: pop larger values from the back
        while dq and nums[dq[-1]] >= val:
            dq.pop()
        dq.append(i)

        # Remove indices that have fallen outside the window
        if dq[0] <= i - k:
            dq.popleft()

        # Start recording once the first full window is complete
        if i >= k - 1:
            result = max(result, nums[dq[0]])

    return result
```

### Java

```java
import java.util.ArrayDeque;
import java.util.Deque;

public int maxOfSlidingWindowMinimums(int[] nums, int k) {
    Deque<Integer> dq = new ArrayDeque<>();
    int result = Integer.MIN_VALUE;

    for (int i = 0; i < nums.length; i++) {
        while (!dq.isEmpty() && nums[dq.peekLast()] >= nums[i])
            dq.pollLast();
        dq.offerLast(i);

        if (dq.peekFirst() <= i - k)
            dq.pollFirst();

        if (i >= k - 1)
            result = Math.max(result, nums[dq.peekFirst()]);
    }
    return result;
}
```

---

## Dry Run — Example 1

`nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`

| i | val | Deque (indices) | Window min | result |
|---|-----|-----------------|------------|--------|
| 0 | 1   | [0]             | —          | -∞     |
| 1 | 3   | [0, 1]          | —          | -∞     |
| 2 | -1  | [2]             | -1         | -1     |
| 3 | -3  | [3]             | -3         | -1     |
| 4 | 5   | [3, 4]          | -3         | -1     |
| 5 | 3   | [3, 5]          | -3         | -1     |
| 6 | 6   | [3, 5, 6]       | -3 → evict 3 → [5,6] → min=3 | 3 |
| 7 | 7   | [5, 6, 7]       | 3          | **3**  |

Final answer: **3** ✅

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Removing from the back when `nums[back] > val` instead of `>= val` | Use `>=` to handle duplicates correctly |
| Checking the window boundary with `< i - k` instead of `<= i - k` | Use `<=` — the window starts at `i - k + 1`, so index `i - k` is out |
| Starting to update result before the first full window (i < k-1) | Guard with `if i >= k - 1` |

---

## Related Problems

| Problem | Relationship |
|---|---|
| [Sliding Window Minimum](/problem_soulutions/sliding_window/subarray_minimums_analysis) | Core building block of this problem |
| [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Symmetric — flip deque to decreasing order |
| [Subarray Minimums](/problem_soulutions/sliding_window/subarray_minimums_analysis) | Sum of all subarray minimums (different direction) |
| Min of Sliding Window Maximums | Flip both steps: per-window max → global min |

---

## Follow-up Questions

1. **What if you need all window minimums as a list?** → Remove the outer `max` and collect each window min into a result array.
2. **What if k = 1?** → Every window is a single element; the answer is simply `max(nums)`.
3. **What if k = n?** → There is only one window; the answer is `min(nums)`.
4. **Can you solve it without a deque?** → Yes, with a sparse table for static range-minimum queries in O(n log n) preprocessing + O(1) per query, but the deque approach is simpler here.
