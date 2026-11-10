---
layout: simple
title: "Counting Pairs"
permalink: /worldquant/counting_pairs
difficulty: Medium
tags: [array, two-pointers, sorting, hash-map, worldquant]
---

# Counting Pairs

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Array / Two Pointers |
| **Key Technique** | Sort + Two Pointers or Hash Map |

### Learning Goals
- [ ] Count pairs satisfying a difference constraint in O(n log n)
- [ ] Choose between two-pointer (sorted) and hash-map approaches
- [ ] Handle the WorldQuant variant: pairs where absolute return difference ≤ threshold

---

## Problem Statement

Given an integer array `nums` and an integer `k`, count the number of index pairs `(i, j)` with `i < j` such that:

```
|nums[i] - nums[j]| <= k
```

**Input:**
- An integer array `nums` of length `n`
- An integer `k` (threshold)

**Output:**
- A single integer: the count of valid pairs

**Constraints:**
- `1 <= n <= 10^5`
- `0 <= nums[i] <= 10^9`
- `0 <= k <= 10^9`

---

## Examples

### Example 1
```
Input:  nums = [1, 3, 5, 7], k = 2
Output: 3

Explanation:
Valid pairs (|diff| <= 2):
(1,3): |1-3| = 2 ✅
(3,5): |3-5| = 2 ✅
(5,7): |5-7| = 2 ✅
(1,5): |1-5| = 4 ❌
Count = 3
```

### Example 2
```
Input:  nums = [4, 1, 2, 3], k = 1
Output: 3

Pairs: (1,2), (2,3), (3,4) → 3 pairs
```

### Example 3
```
Input:  nums = [1, 1, 1], k = 0
Output: 3  (all three pairs have difference 0)
```

---

## Approach 1: Sort + Two Pointers — O(n log n)

After sorting, for each right pointer `r`, use a left pointer `l` to find the leftmost index where `nums[r] - nums[l] <= k`. All indices between `l` and `r-1` form valid pairs with `r`.

```python
def count_pairs(nums: list[int], k: int) -> int:
    nums.sort()
    n = len(nums)
    count = 0
    l = 0
    for r in range(1, n):
        while nums[r] - nums[l] > k:
            l += 1
        count += r - l  # pairs (l, r), (l+1, r), ..., (r-1, r)
    return count
```

---

## Approach 2: Binary Search — O(n log n)

For each `r`, binary search for the leftmost `l` such that `nums[r] - nums[l] <= k`.

```python
from bisect import bisect_left

def count_pairs(nums: list[int], k: int) -> int:
    nums.sort()
    count = 0
    for r in range(1, len(nums)):
        l = bisect_left(nums, nums[r] - k, 0, r)
        count += r - l
    return count
```

---

## Dry Run — Example 1

`nums = [1, 3, 5, 7]`, `k = 2` (already sorted)

| r | nums[r] | l | nums[r]-nums[l] | pairs added |
|---|---------|---|-----------------|-------------|
| 1 | 3 | 0 | 3-1=2 ≤ 2 | 1 |
| 2 | 5 | 0 | 5-1=4 > 2 → l=1, 5-3=2 ≤ 2 | 1 |
| 3 | 7 | 1 | 7-3=4 > 2 → l=2, 7-5=2 ≤ 2 | 1 |

Total = **3** ✅

---

## Variant: Count Pairs with Exact Difference k

```python
from collections import Counter

def count_pairs_exact(nums: list[int], k: int) -> int:
    freq = Counter(nums)
    count = 0
    for val in freq:
        if val + k in freq:
            count += freq[val] * freq[val + k]
    if k == 0:
        count = sum(v * (v - 1) // 2 for v in freq.values())
    return count
```

---

## Complexity Summary

| Approach | Time | Space | Best for |
|---|---|---|---|
| Sort + Two Pointers | O(n log n) | O(1) | Range condition `\|diff\| <= k` |
| Binary Search | O(n log n) | O(1) | Same, slightly different code flow |
| Hash Map | O(n) | O(n) | Exact difference `diff == k` |

---

## Related Problems

| Problem | Note |
|---|---|
| LeetCode 532 — K-diff Pairs | Exact difference variant |
| LeetCode 2006 — Count Pairs with Difference k | Direct match |
| Counting Inversions | Count pairs where nums[i] > nums[j] for i < j |
