---
layout: simple
title: "Rolling Rank in a Sliding Window"
permalink: /worldquant/rolling_rank_in_a_sliding_window
difficulty: Hard
tags: [sliding-window, sorted-container, fenwick-tree, worldquant]
---

# Rolling Rank in a Sliding Window

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Sliding Window / Order Statistics |
| **Key Technique** | Sorted Container (SortedList) or Fenwick Tree |

### Learning Goals
- [ ] Maintain a sorted window efficiently with O(log k) insert/delete
- [ ] Compute rank (position) of each new element within the current window
- [ ] Apply this to cross-sectional ranking in finance

---

## Problem Statement

Given an integer array `nums` and a window size `k`, for each position `i >= k - 1`, return the **1-based rank** of `nums[i]` within the window `nums[i-k+1 .. i]`.

The rank of a value is its position in the sorted (ascending) order of the window. Ties receive the same rank (dense ranking).

**Input:**
- An integer array `nums` of length `n`
- An integer `k` (window size)

**Output:**
- An array of `n - k + 1` integers: the rank of `nums[i]` in its window for each valid `i`

**Constraints:**
- `1 <= k <= n <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## Examples

### Example 1
```
Input:  nums = [3, 1, 4, 1, 5, 9, 2, 6], k = 3
Output: [2, 1, 2, 3, 1, 2]

Window [3,1,4] → sorted [1,3,4] → rank of 4 = 3
Window [1,4,1] → sorted [1,1,4] → rank of 1 = 1 (dense, ties share rank)
Window [4,1,5] → sorted [1,4,5] → rank of 5 = 3... 

Wait, re-reading: rank of the LAST element (nums[i]) in window:
i=2: window=[3,1,4], nums[2]=4 → rank 3 → output[0]=3
i=3: window=[1,4,1], nums[3]=1 → rank 1 → output[1]=1
i=4: window=[4,1,5], nums[4]=5 → rank 3 → output[2]=3
i=5: window=[1,5,9], nums[5]=9 → rank 3 → output[3]=3
i=6: window=[5,9,2], nums[6]=2 → rank 1 → output[4]=1
i=7: window=[9,2,6], nums[7]=6 → rank 2 → output[5]=2

Output: [3, 1, 3, 3, 1, 2]
```

### Example 2
```
Input:  nums = [5, 3, 1, 2, 4], k = 3
Output: [1, 1, 3]

i=2: window=[5,3,1], nums[2]=1 → rank 1
i=3: window=[3,1,2], nums[3]=2 → rank 2
i=4: window=[1,2,4], nums[4]=4 → rank 3

Output: [1, 2, 3]
```

---

## Approach: SortedList

Use a sorted container that supports O(log k) insert, delete, and `bisect_left` for rank lookup.

### Algorithm

```
1. Initialise an empty SortedList.
2. For each i from 0 to n-1:
   a. Insert nums[i] into SortedList.
   b. If i >= k, remove nums[i - k] (sliding out).
   c. If i >= k-1, rank = bisect_right(SortedList, nums[i]).
      (rank = number of elements <= nums[i] = 1-based rank under dense scheme)
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n log k) |
| **Space** | O(k) |

---

## Implementation

```python
from sortedcontainers import SortedList
from bisect import bisect_right

def rolling_rank(nums: list[int], k: int) -> list[int]:
    sl = SortedList()
    result = []

    for i, val in enumerate(nums):
        sl.add(val)
        if i >= k:
            sl.remove(nums[i - k])  # O(log k)
        if i >= k - 1:
            # 1-based dense rank: count of elements <= val
            rank = sl.bisect_right(val)  # O(log k)
            result.append(rank)

    return result
```

---

## Handling Ties — Dense Rank vs Standard Rank

| Rank type | Formula |
|---|---|
| Dense rank (ties share lowest rank) | `bisect_left(sl, val) + 1` |
| Standard rank (ties share average) | `(bisect_left + bisect_right) / 2 + 0.5` |
| "Count ≤ val" rank | `bisect_right(sl, val)` |

For the WorldQuant cross-sectional ranking context, **average rank** for ties is most common:

```python
lo = sl.bisect_left(val)
hi = sl.bisect_right(val)
rank = (lo + hi + 1) / 2  # average rank, 1-based
```

---

## Finance Context

In quantitative finance, this problem appears as:

> "Given a rolling window of stock returns, what is the **percentile rank** of today's return within the past k days?"

This is the basis of **time-series momentum** and **mean-reversion** signals.

```
percentile = rank / k  # normalised to [1/k, 1]
```

---

## Related Problems

| Problem | Note |
|---|---|
| LeetCode 295 — Find Median from Data Stream | Median = rank n/2 |
| Cross-Sectional Rank Transform with Ties and NaN | Rank across assets, not time |
| Minimum Swaps to Sort by Popularity | Sorting and ranking |
