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

### In 60 seconds
- **Pattern:** Sorted window (SortedList / Fenwick tree)
- **Key insight:** Keep the window sorted; today's rank is `bisect_left(window, x) + 1`.
- **Complexity:** O(n log k) with `SortedList`; O(n·k) worst case with `list` + `insort`
- **Trap:** Calling `bisect_left + 1` "dense" rank — it is min rank; dense needs distinct counts.

> **Say this in the interview:** "A sorted window turns rank into a binary search, and removals keep it O(log k) per step."

---

## Problem Statement

Given an integer array `nums` and a window size `k`, for each position `i >= k - 1`, return the **1-based rank** of `nums[i]` within the window `nums[i-k+1 .. i]`.

The rank of a value is `1 + (number of window elements strictly less than it)`. Ties share the lowest rank ("min" or competition ranking, `pandas.rank(method="min")`).

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
Output: [3, 1, 3, 3, 1, 2]

i=2: window [3,1,4], today 4 → 2 smaller → rank 3
i=3: window [1,4,1], today 1 → 0 smaller → rank 1 (ties with the other 1)
i=4: window [4,1,5], today 5 → rank 3
i=5: window [1,5,9], today 9 → rank 3
i=6: window [5,9,2], today 2 → rank 1
i=7: window [9,2,6], today 6 → rank 2
```

### Example 2
```
Input:  nums = [5, 3, 1, 2, 4], k = 3
Output: [1, 2, 3]
```

---

## Approach: sorted window

Brute force re-sorts each window: O(n·k log k). Instead keep the window in a sorted container that supports O(log k) insert, delete, and binary search.

### Algorithm

```
For each i:
  1. add nums[i]
  2. if i >= k: remove nums[i - k]
  3. if i >= k - 1: rank = bisect_left(window, nums[i]) + 1
```

### Complexity

| | `SortedList` | `list` + `bisect.insort` (stdlib only) |
|---|---|---|
| **Time** | O(n log k) | O(n·k) worst case (insert/delete shift elements) |
| **Space** | O(k) | O(k) |

---

## Implementation

```python
from sortedcontainers import SortedList

def rolling_rank(nums: list[int], k: int) -> list[int]:
    sl = SortedList()
    result = []
    for i, val in enumerate(nums):
        sl.add(val)
        if i >= k:
            sl.remove(nums[i - k])
        if i >= k - 1:
            result.append(sl.bisect_left(val) + 1)
    return result
```

If `sortedcontainers` is not allowed, a stdlib version is short and fast enough for moderate `k`:

```python
from bisect import bisect_left, insort

def rolling_rank_stdlib(nums: list[int], k: int) -> list[int]:
    window: list[int] = []
    result = []
    for i, val in enumerate(nums):
        insort(window, val)
        if i >= k:
            del window[bisect_left(window, nums[i - k])]
        if i >= k - 1:
            result.append(bisect_left(window, val) + 1)
    return result
```

For large `k` without third-party packages, use a Fenwick tree over coordinate-compressed values: O(n log n).

---

## Handling Ties

With `lo = bisect_left(sl, val)` and `hi = bisect_right(sl, val)`:

| Tie method (pandas name) | Formula |
|---|---|
| `min` (this problem) | `lo + 1` |
| `max` | `hi` |
| `average` (common for factor ranks) | `(lo + 1 + hi) / 2` |
| `dense` | `1 + number of distinct values < val` (needs a sorted set of distinct keys plus a counter) |

---

## Finance Context

In quantitative finance, this problem appears as:

> "Given a rolling window of stock returns, what is the **percentile rank** of today's return within the past k days?"

This is the basis of **time-series momentum** and **mean-reversion** signals.

```
percentile = rank / k  # in [1/k, 1]; use (rank - 1) / (k - 1) for [0, 1]
```

---

## Related Problems

| Problem | Note |
|---|---|
| LeetCode 295 — Find Median from Data Stream | Median = rank n/2 |
| Cross-Sectional Rank Transform with Ties and NaN | Rank across assets, not time |
| Minimum Swaps to Sort by Popularity | Sorting and ranking |
