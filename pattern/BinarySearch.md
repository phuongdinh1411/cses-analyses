---
layout: simple
title: "Binary Search Patterns"
permalink: /pattern/binary-search
---

# Binary Search Patterns — Comprehensive Guide

Binary search is not just "find a number in a sorted array." It's a general technique for narrowing down a search space by half at each step. Once you see it as **searching for a boundary** rather than searching for a value, an enormous class of problems opens up.

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| Find exact value in sorted array | Classic binary search | [1](#1-classic-binary-search) |
| Find **first** occurrence / insertion point | Lower bound | [2](#2-lower-bound-and-upper-bound) |
| Find **last** occurrence | Upper bound | [2](#2-lower-bound-and-upper-bound) |
| Find min/max value satisfying a condition | Binary search on answer | [3](#3-binary-search-on-answer) |
| Search on **real numbers** | Floating-point binary search | [4](#4-binary-search-on-real-numbers) |
| Find **peak** in mountain array | Binary search on bitonic | [5](#5-peak-finding) |
| Search in **rotated** sorted array | Modified binary search | [6](#6-rotated-sorted-array) |
| Find Kth smallest / **median** | Binary search on value | [7](#7-kth-smallest-and-median) |
| Minimize **maximum** or maximize **minimum** | Binary search on answer | [3](#3-binary-search-on-answer) |
| Optimize on **unimodal** function | Ternary search | [8](#8-ternary-search) |
| Search in **2D sorted** matrix | Row/column binary search | [9](#9-binary-search-on-2d) |
| Use Python's **bisect** module | bisect_left / bisect_right | [10](#10-pythons-bisect-module) |

---

## Table of Contents

1. [Classic Binary Search](#1-classic-binary-search)
2. [Lower Bound and Upper Bound](#2-lower-bound-and-upper-bound)
3. [Binary Search on Answer](#3-binary-search-on-answer)
4. [Binary Search on Real Numbers](#4-binary-search-on-real-numbers)
5. [Peak Finding](#5-peak-finding)
6. [Rotated Sorted Array](#6-rotated-sorted-array)
7. [Kth Smallest and Median](#7-kth-smallest-and-median)
8. [Ternary Search](#8-ternary-search)
9. [Binary Search on 2D](#9-binary-search-on-2d)
10. [Python's bisect Module](#10-pythons-bisect-module)
11. [Common Patterns Collection](#11-common-patterns-collection)
12. [Pattern Recognition Cheat Sheet](#12-pattern-recognition-cheat-sheet)

---

## 1. Classic Binary Search

### The Idea

Repeatedly cut the search space in half. Requires a **sorted** or **monotonic** property.

```
Find 7 in [1, 3, 5, 7, 9, 11, 13]

Step 1: lo=0, hi=6, mid=3, arr[3]=7  -> found!

Find 6:
Step 1: lo=0, hi=6, mid=3, arr[3]=7  -> 6 < 7, search left
Step 2: lo=0, hi=2, mid=1, arr[1]=3  -> 6 > 3, search right
Step 3: lo=2, hi=2, mid=2, arr[2]=5  -> 6 > 5, search right
Step 4: lo=3, hi=2  -> lo > hi, not found
```

### Implementation

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoids overflow (matters in C++/Java)

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1  # not found
```

### The #1 Source of Bugs

Off-by-one errors. The key rules:

| Choice | When |
|--------|------|
| `lo <= hi` | Searching for exact match; search space can be a single element |
| `lo < hi` | Searching for a boundary; loop ends with `lo == hi` = answer |
| `mid = lo + (hi - lo) // 2` | Always use this instead of `(lo + hi) // 2` to prevent overflow |
| `lo = mid + 1` | Exclude mid from left search (mid is too small) |
| `hi = mid - 1` | Exclude mid from right search (mid is too large) |
| `hi = mid` | Include mid (it might be the answer) --- used with `lo < hi` |

---

## 2. Lower Bound and Upper Bound

The **most useful** binary search variants. Instead of finding an exact match, find a **boundary**.

### Mental Model

Think of the array as having a property that flips from False to True (or vice versa). Binary search finds where the flip happens.

```
arr:    [1, 3, 5, 5, 5, 7, 9]
target: 5

"Is arr[i] >= 5?"
         F  F  T  T  T  T  T
              ^
              lower_bound = 2 (first True)

"Is arr[i] > 5?"
         F  F  F  F  F  T  T
                       ^
                       upper_bound = 5 (first True)
```

### Lower Bound (First >= target)

Returns the **leftmost** position where target could be inserted to maintain sorted order. Also: first occurrence of target.

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)  # note: hi = len(arr), not len(arr)-1

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1    # mid is too small, exclude it
        else:
            hi = mid         # mid might be the answer, keep it

    return lo  # first index where arr[index] >= target
```

### Upper Bound (First > target)

Returns the position **after** the last occurrence of target.

```python
def upper_bound(arr, target):
    lo, hi = 0, len(arr)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:
            lo = mid + 1    # mid is <= target, exclude it
        else:
            hi = mid         # mid is > target, might be the answer

    return lo  # first index where arr[index] > target
```

### Derived Queries

| Query | Implementation |
|-------|---------------|
| First occurrence of x | `lb = lower_bound(arr, x)` then check `arr[lb] == x` |
| Last occurrence of x | `upper_bound(arr, x) - 1` then check value |
| Count of x | `upper_bound(arr, x) - lower_bound(arr, x)` |
| First element > x | `upper_bound(arr, x)` |
| Last element < x | `lower_bound(arr, x) - 1` |
| First element >= x | `lower_bound(arr, x)` |
| Last element <= x | `upper_bound(arr, x) - 1` |
| Element closest to x | Compare `arr[lb]` and `arr[lb-1]` |

### Trace: First and Last Occurrence

```
arr = [1, 2, 2, 2, 3, 4], target = 2

lower_bound(arr, 2):
  lo=0, hi=6
  mid=3, arr[3]=2 >= 2 -> hi=3
  mid=1, arr[1]=2 >= 2 -> hi=1
  mid=0, arr[0]=1 < 2  -> lo=1
  lo=hi=1 -> return 1  (first occurrence)

upper_bound(arr, 2):
  lo=0, hi=6
  mid=3, arr[3]=2 <= 2 -> lo=4
  mid=5, arr[5]=4 > 2  -> hi=5
  mid=4, arr[4]=3 > 2  -> hi=4
  lo=hi=4 -> return 4  (first position AFTER last 2)

Last occurrence: upper_bound - 1 = 3
Count of 2s: 4 - 1 = 3
```

---

## 3. Binary Search on Answer

The most powerful pattern. When you can't search in an array but can **check if an answer is feasible**.

### The Framework

```
"Find the minimum X such that condition(X) is True"

condition(X):
  ... too small ...  F F F F F T T T T T  ... large enough ...
                                ^
                          answer is here (first True)

Binary search finds this boundary.
```

```python
def binary_search_on_answer(lo, hi, condition):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if condition(mid):
            hi = mid         # mid works, try smaller
        else:
            lo = mid + 1     # mid doesn't work, need bigger

    return lo  # minimum value where condition is True
```

### Example 1: Minimum Days to Make M Bouquets

**Problem**: N flowers bloom on given days. Need M bouquets of K adjacent flowers. What's the minimum day?

```python
def min_days_bouquets(bloom_day, m, k):
    n = len(bloom_day)
    if m * k > n:
        return -1

    def can_make(day):
        """Can we make m bouquets by this day?"""
        bouquets = 0
        consecutive = 0
        for i in range(n):
            if bloom_day[i] <= day:
                consecutive += 1
                if consecutive == k:
                    bouquets += 1
                    consecutive = 0
            else:
                consecutive = 0
        return bouquets >= m

    lo, hi = min(bloom_day), max(bloom_day)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_make(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Example 2: Minimize Maximum (Split Array)

**Problem**: Split array into K subarrays to minimize the maximum subarray sum.

```
arr = [7, 2, 5, 10, 8], k = 2

If max_sum = 18: [7,2,5] and [10,8] -> sums 14, 18 -> works (2 splits)
If max_sum = 17: can't split into <= 2 parts with each <= 17?
  [7,2,5] and [10,8=18] > 17 -> need 3 parts -> doesn't work
  Actually [7,2,5,10=24] > 17 too... let's trace properly
  [7,2,5]=14 ok, [10]=10 ok, [8]=8 ok -> 3 parts > 2 -> doesn't work

If max_sum = 18: [7,2,5]=14, [10,8]=18 -> 2 parts -> works!
```

```python
def split_array(nums, k):
    def can_split(max_sum):
        """Can we split into <= k parts, each with sum <= max_sum?"""
        parts = 1
        current = 0
        for num in nums:
            if current + num > max_sum:
                parts += 1
                current = num
                if parts > k:
                    return False
            else:
                current += num
        return True

    lo = max(nums)          # at minimum, max_sum >= largest single element
    hi = sum(nums)          # at maximum, everything in one part
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_split(mid):
            hi = mid        # this works, try smaller
        else:
            lo = mid + 1    # need larger max_sum
    return lo
```

### Example 3: Maximize Minimum (Aggressive Cows)

**Problem**: Place K cows in N stalls to maximize the minimum distance between any two cows.

```python
def aggressive_cows(stalls, k):
    stalls.sort()

    def can_place(min_dist):
        """Can we place k cows with at least min_dist between each?"""
        count = 1
        last = stalls[0]
        for i in range(1, len(stalls)):
            if stalls[i] - last >= min_dist:
                count += 1
                last = stalls[i]
                if count >= k:
                    return True
        return False

    lo, hi = 1, stalls[-1] - stalls[0]
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # round UP to avoid infinite loop
        if can_place(mid):
            lo = mid         # this works, try bigger (maximize!)
        else:
            hi = mid - 1     # too big, need smaller
    return lo
```

**Note the difference**: When **maximizing**, we set `lo = mid` (keep current if it works). To avoid infinite loops, use `mid = lo + (hi - lo + 1) // 2` (round up).

### Minimize vs Maximize Template

```python
# MINIMIZE: find smallest X where condition is True
# F F F F T T T T -> find first T
while lo < hi:
    mid = lo + (hi - lo) // 2
    if condition(mid):
        hi = mid
    else:
        lo = mid + 1

# MAXIMIZE: find largest X where condition is True
# T T T T F F F F -> find last T
while lo < hi:
    mid = lo + (hi - lo + 1) // 2   # round UP!
    if condition(mid):
        lo = mid
    else:
        hi = mid - 1
```

### Common "Binary Search on Answer" Problems

| Problem | What to binary search | Condition |
|---------|----------------------|-----------|
| Split array, minimize max sum | max subarray sum | Can split into <= K parts? |
| Koko eating bananas | eating speed | Can finish in H hours? |
| Ship packages in D days | ship capacity | Can ship all in D days? |
| Aggressive cows | min distance | Can place K cows? |
| Painter's partition | max section length | Can paint with K painters? |
| Find median of two sorted arrays | partition point | Left half <= right half? |
| Minimum time to complete tasks | time | Can all tasks finish? |
| Allocate books to students | max pages | Can distribute to K students? |

---

## 4. Binary Search on Real Numbers

When the answer is a real number, use a fixed number of iterations instead of `lo < hi` (which may not converge for floats).

### Template

```python
def binary_search_float(lo, hi, condition, iterations=100):
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if condition(mid):
            hi = mid
        else:
            lo = mid
    return lo  # or hi, or (lo + hi) / 2
```

100 iterations give precision of about `(hi - lo) / 2^100`, which is far beyond `float64` precision.

### Example: Square Root

```python
def sqrt(x, eps=1e-9):
    lo, hi = 0, max(1, x)
    for _ in range(100):
        mid = (lo + hi) / 2
        if mid * mid > x:
            hi = mid
        else:
            lo = mid
    return lo
```

### Example: Rope Cutting

**Problem**: Given N ropes of various lengths, cut exactly K pieces of equal length. Maximize the length of each piece.

```python
def max_rope_length(ropes, k):
    lo, hi = 0, max(ropes)

    for _ in range(100):
        mid = (lo + hi) / 2
        # how many pieces of length mid can we cut?
        pieces = sum(int(r / mid) for r in ropes)
        if pieces >= k:
            lo = mid     # can cut k pieces, try longer
        else:
            hi = mid     # too few pieces, try shorter

    return lo
```

### Why Fixed Iterations?

Floating-point `lo < hi` may never terminate due to precision issues. With 100 iterations, the interval shrinks by a factor of 2^100 --- more than enough for any practical precision requirement.

---

## 5. Peak Finding

### Peak Element in Array

**Problem**: Find any local maximum (element greater than both neighbors).

```
arr: [1, 3, 5, 4, 2]
          ^  ^
         rising  falling -> peak at index 2 (value 5)
```

```python
def find_peak(arr):
    lo, hi = 0, len(arr) - 1

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1    # peak is to the right (still rising)
        else:
            hi = mid         # peak is here or to the left (falling)

    return lo  # lo == hi == peak index
```

**Why it works**: If `arr[mid] < arr[mid+1]`, the slope is going up, so there must be a peak to the right (even if the array goes up then wraps around, the right boundary or the end of the array guarantees a peak). If `arr[mid] >= arr[mid+1]`, the slope is going down, so there's a peak at mid or to the left.

### Mountain Array (Bitonic)

Find peak in a strictly increasing then strictly decreasing array. Same algorithm.

```python
def peak_of_mountain(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

### Search in Mountain Array

First find the peak. Then binary search both halves.

```python
def search_mountain(arr, target):
    # find peak
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    peak = lo

    # search ascending half [0, peak]
    result = binary_search(arr, target, 0, peak, ascending=True)
    if result != -1:
        return result

    # search descending half [peak+1, n-1]
    return binary_search(arr, target, peak + 1, len(arr) - 1, ascending=False)

def binary_search(arr, target, lo, hi, ascending=True):
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        if ascending:
            if arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        else:
            if arr[mid] > target:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

---

## 6. Rotated Sorted Array

### The Structure

```
Original:  [1, 2, 3, 4, 5, 6, 7]
Rotated:   [4, 5, 6, 7, 1, 2, 3]
                      ^
                   rotation point (minimum)
```

### Find Minimum (Rotation Point)

```python
def find_min_rotated(arr):
    lo, hi = 0, len(arr) - 1

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] > arr[hi]:
            lo = mid + 1    # min is to the right
        else:
            hi = mid         # min is here or to the left

    return lo  # index of minimum element
```

**Why compare with `arr[hi]`?**
- If `arr[mid] > arr[hi]`: the rotation point is between mid+1 and hi
- If `arr[mid] <= arr[hi]`: the right half is sorted, rotation point is at mid or left

### Search in Rotated Array (No Duplicates)

```python
def search_rotated(arr, target):
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid

        # determine which half is sorted
        if arr[lo] <= arr[mid]:
            # left half is sorted
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # right half is sorted
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1
```

### Search in Rotated Array (With Duplicates)

Duplicates break the `arr[lo] <= arr[mid]` check. When `arr[lo] == arr[mid] == arr[hi]`, we can't tell which side is sorted. Shrink both sides.

```python
def search_rotated_dups(arr, target):
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return True

        # can't determine sorted side
        if arr[lo] == arr[mid] == arr[hi]:
            lo += 1
            hi -= 1
        elif arr[lo] <= arr[mid]:
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return False
```

Worst case with duplicates: O(N) (e.g., `[1,1,1,1,1,1,2,1,1]`).

---

## 7. Kth Smallest and Median

### Kth Smallest in Sorted Matrix

**Problem**: N x N matrix where each row and column is sorted. Find the Kth smallest element.

```python
def kth_smallest_matrix(matrix, k):
    n = len(matrix)

    def count_less_equal(target):
        """Count elements <= target using the sorted structure."""
        count = 0
        row, col = n - 1, 0  # start bottom-left
        while row >= 0 and col < n:
            if matrix[row][col] <= target:
                count += row + 1  # all elements above in this column
                col += 1
            else:
                row -= 1
        return count

    lo, hi = matrix[0][0], matrix[n-1][n-1]
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if count_less_equal(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Median of Two Sorted Arrays

**Problem**: Find the median of two sorted arrays in O(log(min(m,n))).

```python
def find_median(nums1, nums2):
    # ensure nums1 is shorter
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2

    lo, hi = 0, m
    while lo <= hi:
        i = lo + (hi - lo) // 2  # partition point in nums1
        j = half - i              # partition point in nums2

        # values at partition boundaries
        left1 = nums1[i-1] if i > 0 else float('-inf')
        left2 = nums2[j-1] if j > 0 else float('-inf')
        right1 = nums1[i] if i < m else float('inf')
        right2 = nums2[j] if j < n else float('inf')

        if left1 <= right2 and left2 <= right1:
            # correct partition
            if (m + n) % 2 == 1:
                return max(left1, left2)
            return (max(left1, left2) + min(right1, right2)) / 2
        elif left1 > right2:
            hi = i - 1  # too many from nums1
        else:
            lo = i + 1  # too few from nums1

    return 0
```

### How It Works

```
nums1: [1, 3, | 8, 9]      i = 2 (take 2 from nums1)
nums2: [2, | 5, 6, 7, 10]   j = 3 (take 3 from nums2)

Left half:  {1, 3, 2, 5, 6}   max = 6
Right half: {8, 9, 7, 10}     min = 7

Check: left1=3 <= right2=7 ✓  and  left2=6 <= right1=8 ✓
       -> correct partition!

Wait, we need half = (4+5+1)//2 = 5 elements in left half.
i=2 from nums1, j=3 from nums2 -> 5 total ✓

Median (odd total) = max(left1, left2) = max(3, 6) = 6...
Actually let me recalculate. Sorted: [1,2,3,5,6,7,8,9,10], median = 6. ✓
```

---

## 8. Ternary Search

### When to Use

Binary search works for monotonic functions. **Ternary search** works for **unimodal** functions (one peak or one valley).

```
Unimodal (one peak):          Unimodal (one valley):
     *                              *         *
    * *                              *       *
   *   *                              *     *
  *     *                              *   *
 *       *                              * *
*         *                              *
```

### Finding Maximum of Unimodal Function

```python
def ternary_search_max(f, lo, hi, iterations=200):
    """Find x in [lo, hi] that maximizes f(x)."""
    for _ in range(iterations):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            lo = m1    # max is in [m1, hi]
        else:
            hi = m2    # max is in [lo, m2]
    return (lo + hi) / 2
```

### Finding Minimum of Unimodal Function

```python
def ternary_search_min(f, lo, hi, iterations=200):
    """Find x in [lo, hi] that minimizes f(x)."""
    for _ in range(iterations):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            hi = m2    # min is in [lo, m2]
        else:
            lo = m1    # min is in [m1, hi]
    return (lo + hi) / 2
```

### Integer Ternary Search

```python
def ternary_search_int(f, lo, hi):
    """Find integer x in [lo, hi] that maximizes f(x)."""
    while hi - lo > 2:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3
        if f(m1) < f(m2):
            lo = m1 + 1
        else:
            hi = m2 - 1
    # check remaining candidates
    best = lo
    for x in range(lo, hi + 1):
        if f(x) > f(best):
            best = x
    return best
```

### Ternary vs Binary Search

| | Binary Search | Ternary Search |
|--|--------------|----------------|
| Function shape | Monotonic (always increasing or decreasing) | Unimodal (one peak or valley) |
| Queries per iteration | 1 | 2 |
| Reduction per iteration | 1/2 | 1/3 |
| Convergence | ~log2(N) steps | ~log(3/2)(N) steps |
| Prefer | When you can reframe as boundary search | When function is truly unimodal |

**Tip**: Many ternary search problems can be converted to binary search by searching for the "derivative = 0" point (where the function changes from increasing to decreasing).

---

## 9. Binary Search on 2D

### Search in Row-Sorted and Column-Sorted Matrix

**Problem**: Each row is sorted left to right, each column sorted top to bottom. Find target.

```python
def search_2d_staircase(matrix, target):
    """O(M + N) staircase search starting from top-right."""
    if not matrix:
        return False
    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1  # top-right corner

    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] < target:
            row += 1     # need bigger, go down
        else:
            col -= 1     # need smaller, go left

    return False
```

### Search in Fully Sorted Matrix

**Problem**: Rows are sorted, and first element of each row > last element of previous row. Treat as a flat sorted array.

```python
def search_2d_flat(matrix, target):
    """O(log(M*N)) - treat as 1D sorted array."""
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return False
```

### Count Elements Less Than X in Sorted Matrix

Used as a building block for Kth smallest (Section 7).

```python
def count_less_equal(matrix, target):
    """O(M + N) using staircase from bottom-left."""
    count = 0
    row, col = len(matrix) - 1, 0
    while row >= 0 and col < len(matrix[0]):
        if matrix[row][col] <= target:
            count += row + 1
            col += 1
        else:
            row -= 1
    return count
```

---

## 10. Python's bisect Module

Python's standard library has optimized binary search. Use it.

### Key Functions

```python
from bisect import bisect_left, bisect_right, insort

arr = [1, 3, 5, 5, 5, 7, 9]

bisect_left(arr, 5)     # 2  (leftmost position to insert 5 = lower_bound)
bisect_right(arr, 5)    # 5  (rightmost position to insert 5 = upper_bound)
bisect_left(arr, 4)     # 2  (where 4 would go)
bisect_right(arr, 4)    # 2  (same for 4, since 4 not present)

insort(arr, 4)          # arr becomes [1, 3, 4, 5, 5, 5, 7, 9] (insert in sorted order)
```

### Mapping to Our Functions

| Our function | Python equivalent |
|-------------|-------------------|
| `lower_bound(arr, x)` | `bisect_left(arr, x)` |
| `upper_bound(arr, x)` | `bisect_right(arr, x)` |
| First occurrence of x | `i = bisect_left(arr, x); arr[i] == x` |
| Last occurrence of x | `i = bisect_right(arr, x) - 1; arr[i] == x` |
| Count of x | `bisect_right(arr, x) - bisect_left(arr, x)` |
| Insert maintaining order | `insort(arr, x)` (O(N) due to shifting) |

### Custom Key (Python 3.10+)

```python
from bisect import bisect_left

# search by a key function
data = [(1, 'a'), (3, 'b'), (5, 'c'), (7, 'd')]
keys = [x[0] for x in data]
idx = bisect_left(keys, 4)  # 2

# or with key parameter (Python 3.10+)
idx = bisect_left(data, 4, key=lambda x: x[0])
```

---

## 11. Common Patterns Collection

### Find First Bad Version

```python
def first_bad_version(n, is_bad):
    lo, hi = 1, n
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if is_bad(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Capacity to Ship Packages

```python
def ship_within_days(weights, days):
    def can_ship(capacity):
        d, current = 1, 0
        for w in weights:
            if current + w > capacity:
                d += 1
                current = w
            else:
                current += w
        return d <= days

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_ship(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Koko Eating Bananas

```python
import math

def min_eating_speed(piles, h):
    def can_finish(speed):
        return sum(math.ceil(p / speed) for p in piles) <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_finish(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Find Smallest Divisor Given a Threshold

```python
import math

def smallest_divisor(nums, threshold):
    def total_sum(divisor):
        return sum(math.ceil(n / divisor) for n in nums)

    lo, hi = 1, max(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if total_sum(mid) <= threshold:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

## 12. Pattern Recognition Cheat Sheet

### By Problem Type

| You see... | Pattern | Template |
|------------|---------|----------|
| "Find in sorted array" | Classic BS | `lo <= hi`, exact match |
| "First/last occurrence" | Lower/upper bound | `lo < hi`, boundary search |
| "Minimize the maximum" | BS on answer (minimize) | `condition(mid) -> hi=mid` |
| "Maximize the minimum" | BS on answer (maximize) | `condition(mid) -> lo=mid` (round up!) |
| "Minimum speed/capacity/size" | BS on answer (minimize) | Check feasibility |
| "Sorted + rotated" | Modified BS | Determine sorted half first |
| "Peak / mountain" | BS on slope | Compare `mid` with `mid+1` |
| "Real-valued answer" | Float BS | Fixed 100 iterations |
| "Kth smallest" | BS on value | Count elements <= mid |
| "Optimize unimodal function" | Ternary search | Two midpoints per iteration |

### The Universal Template

Almost every binary search problem fits one of these two templates:

```python
# Template 1: MINIMIZE (find first True)
# F F F F T T T T
def minimize(lo, hi, condition):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if condition(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

# Template 2: MAXIMIZE (find last True)
# T T T T F F F F
def maximize(lo, hi, condition):
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2   # round UP
        if condition(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Infinite loop (lo never advances) | Use `mid = lo + (hi - lo + 1) // 2` when `lo = mid` |
| Off-by-one on boundaries | Decide: is `hi` inclusive or exclusive? Be consistent |
| Wrong comparison direction | Draw the F/T boundary and check which side you're shrinking |
| Integer overflow in `(lo+hi)/2` | Always use `lo + (hi - lo) // 2` |
| Float BS doesn't converge | Use fixed iterations (100) instead of `while lo < hi` |
| Forgetting edge cases | Check: empty array, single element, all same, target not present |

### Complexity Summary

| Pattern | Time | Space |
|---------|------|-------|
| Classic binary search | O(log N) | O(1) |
| Lower/upper bound | O(log N) | O(1) |
| BS on answer | O(log(range) * check) | O(1) |
| Float BS | O(iterations * check) | O(1) |
| Rotated array search | O(log N) | O(1) |
| 2D matrix search | O(M + N) or O(log(MN)) | O(1) |
| Ternary search | O(log(range) * 2 evals) | O(1) |
