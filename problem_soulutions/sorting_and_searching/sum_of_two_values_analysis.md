---
layout: simple
title: "Sum of Two Values"
permalink: /problem_soulutions/sorting_and_searching/sum_of_two_values_analysis
difficulty: Easy
tags: [hash-map, two-pointers, two-sum]
cses_link: https://cses.fi/problemset/task/1640
---

# Sum of Two Values

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find two distinct positions with elements summing to target |
| Input | n integers and target sum x |
| Output | Two 1-indexed positions, or "IMPOSSIBLE" |
| Constraints | 2 <= n <= 2x10^5, 1 <= x, a_i <= 10^9 |
| Key Insight | Use hash map for O(1) complement lookup |

## Learning Goals

1. **Hash Map for Complement Lookup**: Store seen values and check if `target - current` exists
2. **Two-Pointer Alternative**: Sort with indices, use pointers from both ends
3. **Trade-offs**: O(n) hash map vs O(n log n) two-pointer approach

## Problem Statement

Given an array of `n` integers and a target sum `x`, find two **distinct** positions `i` and `j` such that `a[i] + a[j] = x`. Return 1-indexed positions or "IMPOSSIBLE" if no solution exists.

**Example:**
```
Input:  n=4, x=8, array=[2, 7, 5, 1]
Output: 2 4

Explanation: a[2] + a[4] = 7 + 1 = 8
```

---

## Approach 1: Hash Map (Optimal for Time)

### Key Idea
For each element, check if its **complement** (`x - element`) has been seen before.

### Algorithm
```
1. Create empty hash map: value -> index
2. For each element at index i:
   a. Calculate complement = x - arr[i]
   b. If complement in map: return (map[complement], i)
   c. Else: add arr[i] -> i to map
3. Return "IMPOSSIBLE"
```

### Visual Walkthrough
```
Array: [2, 7, 5, 1], Target: 8

Step 1: Process 2 (index 0)
        complement = 8 - 2 = 6
        6 not in map -> add {2: 0}
        Map: {2: 0}

Step 2: Process 7 (index 1)
        complement = 8 - 7 = 1
        1 not in map -> add {7: 1}
        Map: {2: 0, 7: 1}

Step 3: Process 5 (index 2)
        complement = 8 - 5 = 3
        3 not in map -> add {5: 2}
        Map: {2: 0, 7: 1, 5: 2}

Step 4: Process 1 (index 3)
        complement = 8 - 1 = 7
        7 FOUND in map at index 1!
        Return (1+1, 3+1) = (2, 4)
```

### Complexity
- **Time**: O(n) - single pass through array
- **Space**: O(n) - hash map storage

### Python Implementation
```python
def solve():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))

    seen = {}  # value -> index

    for i, num in enumerate(arr):
        complement = x - num
        if complement in seen:
            print(seen[complement] + 1, i + 1)
            return
        seen[num] = i

    print("IMPOSSIBLE")

solve()
```

---

## Approach 2: Two Pointers (Optimal for Space in Some Cases)

### Key Idea
Sort the array while preserving original indices. Use two pointers from opposite ends.

### Algorithm
```
1. Create pairs: (value, original_index)
2. Sort pairs by value
3. Initialize left = 0, right = n-1
4. While left < right:
   a. sum = pairs[left].value + pairs[right].value
   b. If sum == x: return original indices
   c. If sum < x: left++
   d. If sum > x: right--
5. Return "IMPOSSIBLE"
```

### Visual Walkthrough
```
Array: [2, 7, 5, 1], Target: 8

Step 1: Create indexed pairs
        [(2,0), (7,1), (5,2), (1,3)]

Step 2: Sort by value
        [(1,3), (2,0), (5,2), (7,1)]
         L                      R

Step 3: Two-pointer search
        L=0, R=3: sum = 1 + 7 = 8 = target
        Found! Original indices: 3 and 1
        Output: (2, 4) in sorted order with 1-indexing
```

### Pointer Movement Diagram
```
Target = 8

[(1,3), (2,0), (5,2), (7,1)]
  L                      R     sum=1+7=8  FOUND!

If sum < target: move L right (increase sum)
If sum > target: move R left  (decrease sum)
```

### Complexity
- **Time**: O(n log n) - dominated by sorting
- **Space**: O(n) - storing indexed pairs

### Python Implementation
```python
def solve():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))

    # Create (value, original_index) pairs
    indexed = [(arr[i], i) for i in range(n)]
    indexed.sort()

    left, right = 0, n - 1

    while left < right:
        current_sum = indexed[left][0] + indexed[right][0]

        if current_sum == x:
            i1, i2 = indexed[left][1], indexed[right][1]
            print(min(i1, i2) + 1, max(i1, i2) + 1)
            return
        elif current_sum < x:
            left += 1
        else:
            right -= 1

    print("IMPOSSIBLE")

solve()
```

---

## Dry Run Example

**Input:** n=5, x=12, array=[3, 9, 5, 7, 2]

### Hash Map Approach
```
i=0: num=3, complement=9, map={} -> not found, map={3:0}
i=1: num=9, complement=3, map={3:0} -> FOUND at index 0!
Output: 1 2
```

### Two-Pointer Approach
```
Indexed: [(3,0), (9,1), (5,2), (7,3), (2,4)]
Sorted:  [(2,4), (3,0), (5,2), (7,3), (9,1)]
          L                            R

L=0, R=4: 2+9=11 < 12 -> L++
L=1, R=4: 3+9=12 = 12 -> FOUND!
Original indices: 0 and 1
Output: 1 2
```

---

## When to Use Which Approach

| Criteria | Hash Map | Two Pointers |
|----------|----------|--------------|
| Time Complexity | O(n) | O(n log n) |
| Space Complexity | O(n) | O(n) |
| Best for | General case | Already sorted input |
| Worst case | Hash collisions | Sorting overhead |
| Implementation | Simpler | Slightly more complex |

**Recommendation:**
- Use **Hash Map** for most cases (faster)
- Use **Two Pointers** when array is already sorted or memory is critical

---

## Common Mistakes

### 1. Returning Same Index Twice
```python
# WRONG: allows same element twice
if arr[i] + arr[i] == x:
    return (i, i)  # Invalid!

# CORRECT: ensure distinct indices
if complement in seen and seen[complement] != i:
    return (seen[complement], i)
```

### 2. 0-indexed vs 1-indexed Output
```python
# WRONG: returning 0-indexed
print(i, j)

# CORRECT: CSES expects 1-indexed
print(i + 1, j + 1)
```

### 3. Not Handling "IMPOSSIBLE" Case
```python
# WRONG: no fallback
for i, num in enumerate(arr):
    if complement in seen:
        return ...

# CORRECT: explicit IMPOSSIBLE output
print("IMPOSSIBLE")
```

### 4. Adding to Map Before Checking (Two Sum = Same Element)
```python
# WRONG: might match element with itself when x = 2*arr[i]
seen[num] = i
if complement in seen:  # Could find itself!
    ...

# CORRECT: check first, then add
if complement in seen:
    ...
seen[num] = i
```

---

## Complexity Summary

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute Force | O(n^2) | O(1) | Check all pairs |
| Hash Map | O(n) | O(n) | Best time complexity |
| Two Pointers | O(n log n) | O(n) | Sorting dominates |

---

## Related Problems

- [CSES Sum of Three Values](https://cses.fi/problemset/task/1641)
- [CSES Sum of Four Values](https://cses.fi/problemset/task/1642)
- [LeetCode Two Sum](https://leetcode.com/problems/two-sum/)
- [LeetCode Two Sum II - Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
