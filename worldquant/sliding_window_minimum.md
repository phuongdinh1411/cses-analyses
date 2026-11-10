---
layout: simple
title: "Sliding Window Minimum"
permalink: /worldquant/sliding_window_minimum
difficulty: Medium
tags: [sliding-window, monotonic-deque, array, worldquant]
---

# Sliding Window Minimum

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sliding Window |
| **Key Technique** | Monotonic Deque |

### Learning Goals
- [ ] Implement a monotonic increasing deque for range-minimum queries
- [ ] Produce the minimum of every window in O(n) total time
- [ ] Distinguish from the "Maximum of Sliding Window Minimums" variant

---

## Problem Statement

Given an array of `n` integers and a window size `k`, find the **minimum element** in each sliding window of size `k` as it moves from left to right.

**Input:**
- An integer array `nums` of length `n`
- An integer `k` (window size)

**Output:**
- An array of `n - k + 1` integers: the minimum of each window

**Constraints:**
- `1 <= k <= n <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## Examples

### Example 1
```
Input:  nums = [2, 1, 4, 5, 3, 4, 1, 2], k = 3
Output: [1, 1, 3, 3, 1, 1]

Window [2,1,4]     → 1
Window [1,4,5]     → 1
Window [4,5,3]     → 3
Window [5,3,4]     → 3
Window [3,4,1]     → 1
Window [4,1,2]     → 1
```

### Example 2
```
Input:  nums = [3, 1, 2], k = 2
Output: [1, 1]
```

---

## Approach: Monotonic Deque

Maintain a deque of indices whose values are in **increasing order**. The front is always the minimum of the current window.

### Algorithm

```
For each index i:
  1. Pop from the BACK while nums[back] >= nums[i]   (maintain increasing order)
  2. Push i to the back
  3. Pop from the FRONT if front index is outside window (index <= i - k)
  4. When i >= k-1, record nums[front] as the window minimum
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n) — each element pushed/popped at most once |
| **Space** | O(k) |

---

## Implementation

```python
from collections import deque

def sliding_window_minimum(nums: list[int], k: int) -> list[int]:
    dq = deque()   # stores indices; values in increasing order
    result = []

    for i, val in enumerate(nums):
        # Remove larger values from the back
        while dq and nums[dq[-1]] >= val:
            dq.pop()
        dq.append(i)

        # Remove out-of-window indices from the front
        if dq[0] <= i - k:
            dq.popleft()

        # Record once the first full window is formed
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

---

## Dry Run — Example 1

`nums = [2,1,4,5,3,4,1,2]`, `k = 3`

| i | val | Deque (indices) | Output |
|---|-----|-----------------|--------|
| 0 | 2 | [0] | — |
| 1 | 1 | [1] | — |
| 2 | 4 | [1,2] | **1** |
| 3 | 5 | [1,2,3] | **1** |
| 4 | 3 | [1→evict,4] wait: 1 out? i-k=1, dq[0]=1 ≤ 1 → evict → [4] | **3** |
| 5 | 4 | [4,5] | **3** |
| 6 | 1 | [6] | **1** |
| 7 | 2 | [6,7] | **1** |

Output: `[1, 1, 3, 3, 1, 1]` ✅

---

## Variant Comparison

| Problem | Deque Order | Output |
|---|---|---|
| Sliding Window Minimum | Increasing | Per-window min array |
| Sliding Window Maximum | Decreasing | Per-window max array |
| Maximum of Sliding Window Minimums | Increasing + running max | Single global max |

---

## Related Problems

| Problem | Note |
|---|---|
| [Maximum of Sliding Window Minimums](/worldquant/maximum_of_sliding_window_minimums) | Global max of all window mins |
| LeetCode 239 — Sliding Window Maximum | Symmetric with decreasing deque |
| Rolling Rank in a Sliding Window | Rank instead of min/max |
