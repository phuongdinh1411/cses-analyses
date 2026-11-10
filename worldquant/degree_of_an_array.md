---
layout: simple
title: "Degree of an Array"
permalink: /worldquant/degree_of_an_array
difficulty: Easy-Medium
tags: [array, hash-map, sliding-window, worldquant]
---

# Degree of an Array

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy-Medium |
| **Category** | Array / Hash Map |
| **Key Technique** | Track first/last occurrence + frequency map |
| **LeetCode** | [697 — Degree of an Array](https://leetcode.com/problems/degree-of-an-array/) |

### Learning Goals
- [ ] Define and compute the "degree" of an array
- [ ] Find the shortest subarray matching the degree in one pass
- [ ] Use hash maps to track first occurrence, last occurrence, and frequency

---

## Problem Statement

The **degree** of an array is defined as the maximum frequency of any one of its elements.

Given a non-empty array `nums` of non-negative integers, find the length of the **shortest contiguous subarray** of `nums` that has the same degree as `nums`.

**Input:**
- An integer array `nums` of length `n`

**Output:**
- A single integer: the length of the shortest subarray with the same degree

**Constraints:**
- `1 <= n <= 50000`
- `0 <= nums[i] <= 49999`

---

## Examples

### Example 1
```
Input:  nums = [1, 2, 2, 3, 1]
Output: 2

Explanation:
Degree = 2 (both 1 and 2 appear twice).
- Shortest subarray containing all 2s: [2,2] → length 2
- Shortest subarray containing all 1s: [1,2,2,3,1] → length 5
Answer = min(2, 5) = 2
```

### Example 2
```
Input:  nums = [1, 2, 2, 3, 1, 4, 2]
Output: 6

Explanation:
Degree = 3 (2 appears 3 times: indices 1,2,6).
Shortest subarray with degree 3 spans index 1 to 6 → length 6.
```

### Example 3
```
Input:  nums = [1]
Output: 1
```

---

## Approach: One-Pass Hash Map

For every element, track:
- `freq[x]` — how many times `x` has appeared
- `first[x]` — the first index where `x` appeared
- `last[x]` — the last index where `x` appeared (updated each time)

The shortest subarray for element `x` to achieve its frequency is:
```
length = last[x] - first[x] + 1
```

At the end, find all elements with `freq[x] == degree` and return the minimum subarray length.

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n) |
| **Space** | O(n) |

---

## Implementation

```python
def find_shortest_subarray(nums: list[int]) -> int:
    freq = {}
    first = {}
    last = {}

    for i, x in enumerate(nums):
        freq[x] = freq.get(x, 0) + 1
        if x not in first:
            first[x] = i
        last[x] = i

    degree = max(freq.values())

    return min(
        last[x] - first[x] + 1
        for x in freq
        if freq[x] == degree
    )
```

---

## Dry Run — Example 2

`nums = [1, 2, 2, 3, 1, 4, 2]`

| Element | freq | first | last | subarray length |
|---------|------|-------|------|-----------------|
| 1 | 2 | 0 | 4 | 5 |
| 2 | 3 | 1 | 6 | **6** |
| 3 | 1 | 3 | 3 | 1 |
| 4 | 1 | 5 | 5 | 1 |

Degree = 3 (only element 2). Shortest subarray = **6** ✅

---

## Edge Cases

| Case | Behaviour |
|---|---|
| All elements distinct | Degree = 1, answer = 1 |
| All elements the same | Degree = n, answer = n |
| Multiple elements tied for degree | Take the min over all tied elements |

---

## Related Problems

| Problem | Note |
|---|---|
| LeetCode 697 — Degree of an Array | This exact problem |
| Sliding Window Maximum/Minimum | Sliding window + extrema |
| Minimum Window Substring | Shortest subarray satisfying a frequency condition |
