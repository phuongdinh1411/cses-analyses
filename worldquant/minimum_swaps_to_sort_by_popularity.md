---
layout: simple
title: "Minimum Swaps to Sort by Popularity"
permalink: /worldquant/minimum_swaps_to_sort_by_popularity
difficulty: Medium
tags: [array, permutation, cycle-detection, worldquant]
---

# Minimum Swaps to Sort by Popularity

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Array / Permutation |
| **Key Technique** | Cycle Detection in Permutation Graph |

### Learning Goals
- [ ] Model a sorting problem as a permutation graph
- [ ] Count the minimum swaps needed using cycle lengths
- [ ] Handle duplicate popularity scores correctly

---

## Problem Statement

You are given an array `popularity` of `n` integers representing the popularity scores of `n` assets. Find the **minimum number of swaps** required to sort the array in **non-decreasing** order.

A swap is defined as exchanging the values at any two indices.

**Input:**
- An integer array `popularity` of length `n`

**Output:**
- A single integer: the minimum number of swaps to sort the array

**Constraints:**
- `1 <= n <= 10^5`
- `0 <= popularity[i] <= 10^9`
- Values may contain duplicates

---

## Examples

### Example 1
```
Input:  popularity = [4, 3, 1, 2]
Output: 3

Explanation:
Sorted target: [1, 2, 3, 4]
Swap index 0 and 2: [1, 3, 4, 2]
Swap index 1 and 3: [1, 2, 4, 3]
Swap index 2 and 3: [1, 2, 3, 4]
3 swaps total.
```

### Example 2
```
Input:  popularity = [2, 3, 4, 1, 5]
Output: 3
```

### Example 3
```
Input:  popularity = [1, 2, 3, 4, 5]
Output: 0  (already sorted)
```

---

## Approach: Cycle Detection

### Key Insight

Build the **permutation** `P` where `P[i]` = the index that element `i` should move to in the sorted order. The minimum swaps = `n - (number of cycles in P)`.

For a cycle of length `L`, you need `L - 1` swaps to fix it.

### Algorithm

```
1. Create pairs (value, original_index) and sort by value.
2. Build the target permutation: sorted_pos[i] = where element at position i should go.
3. Use a visited array to find all cycles.
4. For each unvisited node, traverse its cycle; add (cycle_length - 1) to answer.
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(n log n) — dominated by sorting |
| **Space** | O(n) |

---

## Implementation

```python
def min_swaps_to_sort(popularity: list[int]) -> int:
    n = len(popularity)
    # Pair each value with its original index, sort by value
    indexed = sorted(enumerate(popularity), key=lambda x: x[1])

    visited = [False] * n
    swaps = 0

    for i in range(n):
        if visited[i] or indexed[i][0] == i:
            visited[i] = True
            continue
        # Traverse the cycle starting at i
        cycle_len = 0
        j = i
        while not visited[j]:
            visited[j] = True
            j = indexed[j][0]
            cycle_len += 1
        swaps += cycle_len - 1

    return swaps
```

---

## Dry Run — Example 1

`popularity = [4, 3, 1, 2]`

After sorting: `[(2,1), (3,2), (1,3), (0,4)]` → sorted values `[1,2,3,4]` came from indices `[2,3,1,0]`

Permutation: position `0 → 2 → 1 → 3 → 0` — one cycle of length 4.

Swaps = 4 - 1 = **3** ✅

---

## Handling Duplicates

When values repeat, multiple valid sorted orders exist. Break ties by **original index** to guarantee a consistent permutation:

```python
indexed = sorted(enumerate(popularity), key=lambda x: (x[1], x[0]))
```

---

## Related Problems

| Problem | Link |
|---|---|
| Minimum Swaps to Sort (LeetCode 2459) | Classic variant |
| Rolling Rank in a Sliding Window | Rank maintenance |
