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

## From-Scratch Idea: What Makes a Problem Binary Search

Most people meet binary search as "find a number in a sorted list." That framing hides 90% of its power. The real engine underneath is one idea:

> **If you can split the search space into a "No" region and a "Yes" region with a clean line between them, you can find that line in O(log N) by asking a yes/no question at the midpoint.**

Everything else is deciding *what* the search space is and *what* the yes/no question is.

### The two-question identify test

Ask these in order. If both pass, it's binary search:

```
1. Is there an ordered axis I can search over?
   - a sorted array's indices             (classic)
   - the range of a possible ANSWER        (min speed 1..max, max length 0..sum)
   - a monotonic function's input          (peak: slope +then-)
   If yes, that axis is your [lo, hi].

2. Can I write a predicate P(x) that is monotonic on that axis?
   monotonic = once it flips, it never flips back:
        F F F F T T T T     (find first True  -> minimize)
        T T T T F F F F     (find last  True  -> maximize)
   If yes, binary search finds the flip in O(log N).
```

The moment you can draw the `F F F T T T` line, the rest is mechanical: shrink toward the boundary.

```
Search space:   lo ──────────────── hi
Predicate:      F  F  F  F | T  T  T  T
                          ^
                    binary search finds THIS line
```

### The mental shift that unlocks everything

"Search a sorted array" is the *special case* where the axis is indices and the predicate is `arr[i] >= target`. "Binary search on answer" is the *general case* where the axis is the answer's numeric range and the predicate is a feasibility check `can_we_do_it_with(x)`. Same machine, different axis.

```
Symptom in the problem                          Axis to search       Predicate P(x)
────────────────────────────────────────────   ──────────────────   ─────────────────────
"find / does it contain X" (sorted)             array indices        arr[mid] vs X
"first/last/count of X" (sorted)                array indices        arr[mid] >= X
"minimize the maximum ___"                      the max value        can split under cap x?
"maximize the minimum ___"                      the min value        can place with gap x?
"minimum speed/capacity/size to finish"         the resource amount  can finish with x?
"Kth smallest / median"                         the value range      count(<= x) >= k?
"peak / mountain"                               array indices        arr[mid] < arr[mid+1]?
"rotated sorted array"                          array indices        which half is sorted?
```

### From-scratch, minimize vs maximize

The whole family is two templates. Pick by which end of the `F/T` line you want:

```
MINIMIZE (first True):  F F F T T T      MAXIMIZE (last True):  T T T F F F
  while lo < hi:                           while lo < hi:
      mid = lo + (hi-lo)//2                    mid = lo + (hi-lo+1)//2   # round UP
      if P(mid): hi = mid                      if P(mid): lo = mid
      else:      lo = mid + 1                  else:      hi = mid - 1
  return lo                                 return lo
```

`★ Insight ─────────────────────────────────────`
- The `+1` in the maximize midpoint is not decoration — it prevents an infinite loop. With `lo = mid` and a 2-element window `[lo, lo+1]`, plain `mid = lo` never advances `lo`; rounding up makes `mid = lo+1`, so the window always shrinks. Skip it and the maximize template hangs forever.
- Almost every "binary search on answer" problem is *disguised* as a scheduling/packing question ("ship in D days", "eat in H hours", "K painters"). The tell is a numeric answer plus a linear-time feasibility check. When you spot that pair, stop looking for a formula — search the answer.
`─────────────────────────────────────────────────`

### LeetCode ↔ CP translation

| CP phrasing | LeetCode phrasing | Same technique |
|-------------|-------------------|----------------|
| lower_bound / upper_bound (STL) | First/Last Position (LC 34) | §2 boundary search |
| Aggressive Cows | Magnetic Force Between Balls (LC 1552) | §3 maximize-the-minimum |
| Painter's Partition / Book Allocation | Split Array Largest Sum (LC 410) | §3 minimize-the-maximum |
| Binary search on real answer | Koko / Divide Chocolate | §3–§4 answer search |

---

## Master LeetCode Comparison Table

One row per anchored walkthrough. Read it as: *what am I actually searching over, and what's the yes/no question at the midpoint?*

| LC # | Problem | Technique (§) | Difficulty | Search space | Predicate P(mid) |
|------|---------|---------------|------------|--------------|------------------|
| **704** | Binary Search | Classic (§1) | Easy | array indices | `arr[mid] == target` (3-way) |
| **34** | Find First & Last Position | Lower/Upper bound (§2) | Medium | array indices | `arr[mid] >= target` |
| **875** | Koko Eating Bananas | BS on answer, minimize (§3) | Medium | speed `1 .. max(pile)` | can finish in `h` hours at speed mid? |
| **410** | Split Array Largest Sum | BS on answer, minimize-max (§3) | Hard | cap `max(nums) .. sum(nums)` | can split into ≤ k parts under cap mid? |
| **162** | Find Peak Element | Peak / slope (§5) | Medium | array indices | `arr[mid] < arr[mid+1]` (rising?) |
| **33** | Search in Rotated Sorted Array | Rotated (§6) | Medium | array indices | which half `[lo..mid]` / `[mid..hi]` is sorted? |
| **4** | Median of Two Sorted Arrays | Partition (§7) | Hard | partition index in shorter array | is `left1 ≤ right2 and left2 ≤ right1`? |

Each row is worked in full — statement, pattern-focused solution, ASCII trace, and an insight — in its section below.

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

#### Walkthrough — LC 704 Binary Search

> Given a sorted array `nums` of distinct integers and a `target`, return its index, or `-1` if absent. Must run in O(log n).

**This template solves: LC 704 (Binary Search), LC 35 (Search Insert Position — return `lo` instead of `-1`), LC 374 (Guess Number — the `pick` API is the 3-way compare).**

The pattern-focused view: the axis is **indices**, the question is a **3-way compare** (`==` / `<` / `>`) at the midpoint. Distinct + sorted means the `==` case can return immediately; the other two cases each throw away half.

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1     # inclusive both ends -> use lo <= hi
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1          # target is strictly right of mid
        else:
            hi = mid - 1          # target is strictly left of mid
    return -1
```

```
nums = [-1, 0, 3, 5, 9, 12], target = 9

lo=0 hi=5 mid=2 nums[2]=3  < 9 -> lo=3
lo=3 hi=5 mid=4 nums[4]=9  == 9 -> return 4

target = 2
lo=0 hi=5 mid=2 nums[2]=3  > 2 -> hi=1
lo=0 hi=1 mid=0 nums[0]=-1 < 2 -> lo=1
lo=1 hi=1 mid=1 nums[1]=0  < 2 -> lo=2
lo=2 hi=1 -> lo > hi -> return -1
```

`★ Insight ─────────────────────────────────────`
- Classic (`lo <= hi`, exclude mid with `±1`) and boundary search (`lo < hi`, keep mid with `hi = mid`) are *different loops*, not interchangeable styles. Classic can terminate mid-loop on an exact hit; boundary search always runs the window down to one element. Mixing the two — e.g. `lo <= hi` with `hi = mid` — is the classic infinite-loop bug.
- With distinct values the 3-way compare is safe. The instant duplicates appear and you want *which* copy, the exact-match loop is ambiguous — switch to §2's lower/upper bound.
`─────────────────────────────────────────────────`

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

#### Walkthrough — LC 34 Find First and Last Position

> Given a sorted array `nums`, find the starting and ending index of a given `target`. Return `[-1, -1]` if not found. Must run in O(log n).

**This template solves: LC 34 (First & Last Position), LC 35 (Search Insert = `lower_bound`), LC 278 (First Bad Version = `lower_bound` on an implicit boolean array), LC 74 (via row `lower_bound`).**

The pattern-focused view: this is **two boundary searches**, not one. `lower_bound` finds the first index `>= target` (the left edge); `upper_bound` finds the first index `> target` (one past the right edge). The whole problem is those two lines plus a presence check.

```python
def searchRange(nums, target):
    lo = lower_bound(nums, target)                 # first index >= target
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]                            # target absent
    hi = upper_bound(nums, target) - 1             # last index == target
    return [lo, hi]
```

```
nums = [5, 7, 7, 8, 8, 10], target = 8

lower_bound(8):
  lo=0 hi=6 mid=3 nums[3]=8 >= 8 -> hi=3
  lo=0 hi=3 mid=1 nums[1]=7 <  8 -> lo=2
  lo=2 hi=3 mid=2 nums[2]=7 <  8 -> lo=3
  lo=hi=3 -> 3            (first 8 is at index 3)

upper_bound(8):
  lo=0 hi=6 mid=3 nums[3]=8 <= 8 -> lo=4
  lo=4 hi=6 mid=5 nums[5]=10 > 8 -> hi=5
  lo=4 hi=5 mid=4 nums[4]=8 <= 8 -> lo=5
  lo=hi=5 -> 5            (one past the last 8)

answer = [3, 5-1] = [3, 4]

target = 6:
  lower_bound(6) = 1, nums[1]=7 != 6 -> [-1, -1]
```

`★ Insight ─────────────────────────────────────`
- The only difference between `lower_bound` and `upper_bound` is `<` vs `<=` in the comparison. That single character slides the whole `F/T` boundary by exactly the run of equal elements — which is *why* `upper - lower` counts occurrences. Internalize this and you never memorize four separate boundary functions again.
- Presence must be checked *after* `lower_bound`: it returns an insertion point even when the target is absent, so `nums[lo] == target` (guarded by `lo < len`) is the real "found it" test. Forgetting the guard is the top LC 34 wrong-answer on absent targets.
`─────────────────────────────────────────────────`

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

We binary-search the answer = the largest subarray sum we allow (the "cap").
For a given cap, greedily fill parts left to right, starting a new part
whenever adding the next element would exceed the cap; count the parts.

cap = 17: [7,2,5]=14, next +10=24 > 17 -> new part [10]=10,
          next +8=18 > 17 -> new part [8]=8  =>  3 parts > 2  -> too small
cap = 18: [7,2,5]=14, next +10=24 > 18 -> new part [10,8]=18  =>  2 parts <= 2  -> works

Feasible caps form a monotonic suffix (works for 18 and up, fails below),
so binary search finds the smallest feasible cap = 18.
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

#### Walkthrough — LC 875 Koko Eating Bananas

> Koko has `piles` of bananas and `h` hours before the guards return. Each hour she picks one pile and eats up to `speed` bananas from it (if the pile is smaller, she finishes it and stops for that hour). Return the **minimum** integer `speed` so she eats all bananas within `h` hours.

**This template solves: LC 875 (Koko), LC 1011 (Ship Packages in D Days — same shape, capacity instead of speed), LC 1283 (Smallest Divisor), LC 1482 (Min Days to Make Bouquets).**

The pattern-focused view: you cannot compute the speed with a formula, but for *any* candidate speed you can check feasibility in O(n). Feasibility is monotonic — faster is never worse — so the `F/T` line exists and binary search finds it.

```
speed:   1   2   3   4   5   ...
feasible? F   F   F   T   T        <- eat everything within h hours?
                    ^
              minimum feasible speed = answer
```

```python
import math

def minEatingSpeed(piles, h):
    def can_finish(speed):
        # ceil(pile/speed) hours per pile (a partial pile still costs a full hour)
        return sum(math.ceil(p / speed) for p in piles) <= h

    lo, hi = 1, max(piles)          # speed 0 is impossible; max(pile) always finishes in n hours
    while lo < hi:                  # boundary search -> find first True
        mid = lo + (hi - lo) // 2
        if can_finish(mid):
            hi = mid                # mid works, maybe slower still works
        else:
            lo = mid + 1            # too slow, need faster
    return lo
```

```
piles = [3,6,7,11], h = 8

lo=1 hi=11 mid=6  hours = 1+1+2+2 = 6  <= 8  feasible -> hi=6
lo=1 hi=6  mid=3  hours = 1+2+3+4 = 10 > 8   no       -> lo=4
lo=4 hi=6  mid=5  hours = 1+2+2+3 = 8  <= 8  feasible -> hi=5
lo=4 hi=5  mid=4  hours = 1+2+2+3 = 8  <= 8  feasible -> hi=4
lo=hi=4 -> answer 4
```

`★ Insight ─────────────────────────────────────`
- The search space is the **answer's numeric range** `[1, max(pile)]`, not the array. This is the leap from "binary search *in* data" to "binary search *on* the answer." The array is only touched inside the O(n) predicate.
- Total cost is `O(n log(max_value))` — the `log` is over the *value range*, not the array length. That's why these problems accept huge value bounds (10^9) but modest `n`: the log of a billion is only 30.
`─────────────────────────────────────────────────`

#### Walkthrough — LC 410 Split Array Largest Sum

> Split `nums` into `k` non-empty **contiguous** subarrays. Minimize the largest subarray sum among the splits. Return that minimized largest sum.

**This template solves: LC 410 (Split Array), LC 1011 (Ship in D Days — identical greedy predicate), LC 875 (Koko — same answer-search skeleton), LC 1231 (Divide Chocolate — the maximize twin).**

The pattern-focused view (uses the `split_array` code from §3 Example 2): search the **cap** = the largest sum you allow any part to reach. For a given cap, greedily fill parts left to right; count how many you need. Fewer-or-equal-to-`k` parts means the cap is feasible. Feasibility is monotonic in the cap.

```
cap:   ...14  15  16  17  18  19...
parts:      3   3   3   3   2   2      <- parts needed at this cap (k=2)
feasible?   F   F   F   F   T   T      (parts <= k)
                            ^
                    minimum feasible cap = answer
```

```python
def splitArray(nums, k):
    def can_split(cap):                 # feasible if <= k parts each with sum <= cap
        parts, current = 1, 0
        for x in nums:
            if current + x > cap:
                parts += 1
                current = x
                if parts > k:
                    return False
            else:
                current += x
        return True

    lo, hi = max(nums), sum(nums)       # cap >= biggest element; cap <= whole array in one part
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_split(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

```
nums = [7,2,5,10,8], k = 2

lo=10 hi=32 mid=21  parts: [7,2,5]=14,+10=24>21 new[10,8]=18 -> 2 parts <=2  feasible -> hi=21
lo=10 hi=21 mid=15  parts: [7,2,5]=14,+10>15 new[10]=10,+8>15 new[8] -> 3 >2 no -> lo=16
lo=16 hi=21 mid=18  parts: [7,2,5]=14,+10>18 new[10,8]=18 -> 2 parts <=2  feasible -> hi=18
lo=16 hi=18 mid=17  parts: [7,2,5]=14,+10>17 new[10]=10,+8>17 new[8] -> 3 >2 no -> lo=18
lo=hi=18 -> answer 18
```

`★ Insight ─────────────────────────────────────`
- `lo` and `hi` are not arbitrary: `lo = max(nums)` because no cap smaller than the biggest single element can ever fit that element; `hi = sum(nums)` because one part holding everything always works. Tight bounds like these are half the correctness — a too-low `lo` breaks the predicate's monotonicity guarantee.
- "Minimize the maximum" and "maximize the minimum" (Aggressive Cows, §3 Example 3) are mirror images: same greedy feasibility check, opposite template (minimize keeps `hi = mid`; maximize keeps `lo = mid` with the round-up midpoint). Recognizing the mirror halves what you have to memorize.
`─────────────────────────────────────────────────`

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

> **Assumption:** this relies on adjacent elements never being equal (`arr[i] != arr[i+1]`, as LC 162 guarantees). With flat plateaus the `<` vs `>=` comparison is no longer a clean monotonic predicate on each half, and a single comparison can point the wrong way.

#### Walkthrough — LC 162 Find Peak Element

> A peak is an element strictly greater than its neighbors. Given `nums` where `nums[i] != nums[i+1]` and imaginary `-∞` sentinels beyond both ends, return the index of **any** peak, in O(log n).

**This template solves: LC 162 (Find Peak Element), LC 852 (Peak Index in a Mountain Array — guaranteed single peak), LC 1901 (Find a Peak Element II — the 2D version binary-searches columns).**

The pattern-focused view: there is no sorted array here, yet binary search still applies — because the **slope** gives a monotonic-enough signal. If `nums[mid] < nums[mid+1]`, you are on a rising slope; a peak must exist somewhere to the right (the array can only rise so long before it must turn down, bounded by the `-∞` sentinel). Otherwise you are at a peak or on a falling slope, so a peak sits at `mid` or to its left.

```
climbing right guarantees a peak ahead:
  nums[mid] < nums[mid+1]   ->  ...  /peak    search right, lo = mid+1
  nums[mid] > nums[mid+1]   ->  peak\  ...     search here/left, hi = mid
```

```python
def findPeakElement(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1        # rising -> peak strictly to the right
        else:
            hi = mid            # falling or at peak -> peak here or left
    return lo                   # lo == hi is a peak
```

```
nums = [1, 2, 1, 3, 5, 6, 4]      (index 1 and index 5 are both peaks)

lo=0 hi=6 mid=3 nums[3]=3 < nums[4]=5  rising -> lo=4
lo=4 hi=6 mid=5 nums[5]=6 > nums[6]=4  falling -> hi=5
lo=4 hi=5 mid=4 nums[4]=5 < nums[5]=6  rising -> lo=5
lo=hi=5 -> return 5   (nums[5]=6 is a peak)
```

`★ Insight ─────────────────────────────────────`
- Binary search does **not** require a globally sorted array — it requires a *monotonic decision*. "Am I on a rising slope?" is monotone-usable even on a jagged array, because whichever way you throw is guaranteed to still contain a peak. This is the same reasoning that powers rotated-array search (§6): find a locally decidable direction, not a global order.
- The algorithm finds *a* peak, not *the* peak, and which one depends on the midpoint path (here it lands on index 5, not the also-valid index 1). When a problem needs a *specific* peak, binary-search-on-slope is the wrong tool — you need a full scan or extra structure.
`─────────────────────────────────────────────────`

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

#### Walkthrough — LC 33 Search in Rotated Sorted Array

> A sorted array of **distinct** integers was rotated at some unknown pivot (e.g. `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`). Given `target`, return its index or `-1`, in O(log n).

**This template solves: LC 33 (Search Rotated), LC 81 (Search Rotated II — add the `arr[lo]==arr[mid]==arr[hi]` shrink for duplicates), LC 153 (Find Minimum in Rotated — the pivot-finding half of the same idea).**

The pattern-focused view: a rotated array is **two sorted runs**. At any `mid`, at least one of the halves `[lo..mid]` or `[mid..hi]` is fully sorted — you can tell which by comparing `arr[lo]` with `arr[mid]`. Once you know the sorted half, a simple range check says whether the target lives there; if yes, recurse into it, else the other half.

```
[4, 5, 6, 7, 0, 1, 2]        target = 0
 lo         mid        hi

arr[lo]=4 <= arr[mid]=7  -> LEFT half [4..7] is sorted
is 0 in [4,7)? no  -> go RIGHT
```

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:            # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                 # target inside sorted left
            else:
                lo = mid + 1                 # must be in the other half
        else:                                # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1                 # target inside sorted right
            else:
                hi = mid - 1
    return -1
```

```
nums = [4,5,6,7,0,1,2], target = 0

lo=0 hi=6 mid=3 nums[3]=7  left [4..7] sorted; 0 in [4,7)? no -> lo=4
lo=4 hi=6 mid=5 nums[5]=1  left [0..1] sorted (nums[4]=0<=1); 0 in [0,1)? yes -> hi=4
lo=4 hi=4 mid=4 nums[4]=0  == 0 -> return 4

target = 3
lo=0 hi=6 mid=3 nums[3]=7  left sorted; 3 in [4,7)? no -> lo=4
lo=4 hi=6 mid=5 nums[5]=1  left [0..1] sorted; 3 in [0,1)? no -> lo=6
lo=6 hi=6 mid=6 nums[6]=2  right sorted; 3 in (2,2]? no -> hi=5
lo=6 hi=5 -> return -1
```

`★ Insight ─────────────────────────────────────`
- The key move is `nums[lo] <= nums[mid]` deciding *which half is sorted* — because inside a sorted half a plain range check `[low, high)` is a reliable predicate, restoring monotonicity locally even though the whole array isn't sorted. You binary-search the half you can reason about, not the half the target might be in.
- Use `<=` (not `<`) in `nums[lo] <= nums[mid]`: when `lo == mid` (2-element window) the left "half" is the single element `nums[lo]`, which is trivially sorted. Dropping the equals here is a subtle 2-element bug. With duplicates this test breaks entirely — that's why LC 81 adds the `arr[lo]==arr[mid]==arr[hi]` shrink and degrades to O(n).
`─────────────────────────────────────────────────`

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
nums1: [1, 3, | 8, 9]       i = 2 (take 2 from nums1)
nums2: [2, 5, 6, | 7, 10]    j = 3 (take 3 from nums2)

Total = 9 (odd), half = (4 + 5 + 1) // 2 = 5 elements in the left half.
i = 2 from nums1 + j = 3 from nums2 = 5 ✓

Left half:  {1, 3} ∪ {2, 5, 6}   left1 = 3, left2 = 6
Right half: {8, 9} ∪ {7, 10}     right1 = 8, right2 = 7

Check: left1 = 3 <= right2 = 7 ✓  and  left2 = 6 <= right1 = 8 ✓
       -> correct partition!

Median (odd total) = max(left1, left2) = max(3, 6) = 6
Sanity check on the merged sort [1,2,3,5,6,7,8,9,10]: median = 6 ✓
```

#### Walkthrough — LC 4 Median of Two Sorted Arrays

> Given two sorted arrays `nums1`, `nums2`, return the median of the combined set in **O(log(min(m,n)))**. (Merging is O(m+n) — too slow for the required bound.)

**This template solves: LC 4 (Median of Two Sorted Arrays). The partition idea also underlies LC 1439 (Kth smallest in a sorted matrix of rows) and any "find the split that balances two sorted halves" problem.**

The pattern-focused view (uses the `find_median` code in §7): don't search for the median *value* — search for a **partition** of the shorter array. Cut `nums1` after `i` elements and `nums2` after `j = half - i`. The cut is correct when everything on the left is ≤ everything on the right, which reduces to two cross-checks: `left1 <= right2` and `left2 <= right1`. That correctness condition is **monotonic in `i`** (too-large `left1` means shrink `i`; too-small means grow it), so binary search finds the right cut.

```
partition puts exactly half the elements on the left:
    nums1: [ .. i .. | .. ]      left1 = nums1[i-1]   right1 = nums1[i]
    nums2: [ .. j .. | .. ]      left2 = nums2[j-1]   right2 = nums2[j]

correct when:   left1 <= right2   AND   left2 <= right1
too big left1 -> move i left (hi=i-1);  too small -> move i right (lo=i+1)
```

```
nums1 = [1, 3],  nums2 = [2]        m=1 after swap? no, nums1 shorter stays
(swap so nums1 is shorter: nums1=[2], nums2=[1,3]);  m=1 n=2  half=(3+1)//2=2

lo=0 hi=1:
  i=0 j=2  left1=-inf right1=2  left2=nums2[1]=3 right2=+inf
     left1(-inf)<=right2(+inf) ok; left2(3)<=right1(2)? NO -> lo=i+1=1
lo=1 hi=1:
  i=1 j=1  left1=nums1[0]=2 right1=+inf  left2=nums2[0]=1 right2=nums2[1]=3
     2<=3 ok; 1<=+inf ok -> correct partition
  total=3 odd -> median = max(left1,left2) = max(2,1) = 2 ✓
```

`★ Insight ─────────────────────────────────────`
- The clever reframing: the answer isn't a *position in one array*, it's a *balance point across both*. Fixing `i` forces `j = half - i`, so one binary search over the shorter array (`hi = m`, hence `O(log min(m,n))`) pins down both cuts at once. Searching the value range would be `O(log(max_value))` and clumsier.
- The `±inf` sentinels for out-of-range `left`/`right` are what let the two cross-checks work uniformly at the array edges — no special-casing empty halves. Sentinels turning boundary conditions into ordinary comparisons is a recurring binary-search trick (also the imaginary `-∞` ends in LC 162).
`─────────────────────────────────────────────────`

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

---

## Practice Order

```
Start here
    │
    ▼
  704  (Easy)   ──── Classic BS: exact match on a sorted array (lo <= hi)
    │
    ▼
  278  (Easy)   ──── First Bad Version: find the F→T boundary (lo < hi)
    │
    ▼
   33  (Medium) ──── Search in Rotated Sorted Array: pick the sorted half first
    │
    ▼
  153  (Medium) ──── Find Minimum in Rotated Sorted Array: compare mid with arr[hi]
    │
    ▼
  875  (Medium) ──── Koko Eating Bananas: binary-search-on-ANSWER, not on the array
    │
    ▼
    4  (Hard)   ──── Median of Two Sorted Arrays: binary search the partition point
```

---

## The Binary Search Toolbox at a Glance

```
                        Is there an ordered axis + a monotonic yes/no question?
                                              │
              ┌───────────────────────────────┼───────────────────────────────┐
              │                                │                               │
        axis = indices                  axis = answer range              axis = slope/structure
        of a sorted array               (a number you pick)              (not globally sorted)
              │                                │                               │
   ┌──────────┼──────────┐          ┌──────────┼──────────┐            ┌────────┼────────┐
   │          │          │          │          │          │            │        │        │
 exact     first/last  Kth /     minimize   maximize   real-       peak /    rotated   partition
 match     /count      median    the max    the min    valued      slope     array     two arrays
 (§1)      (§2)        (§7)       (§3)       (§3)       (§4)        (§5)      (§6)      (§7)
 LC 704    LC 34       LC 4       LC 410     Agg.Cows   sqrt/rope   LC 162    LC 33     LC 4
           lo<=target  count(<=x) hi=mid     lo=mid     100 iters   mid vs    which     balance
                       >= k                  (round↑)               mid+1     half?     the cut

 THREE MOVES, EVERY TIME
 1. define [lo, hi]          - indices, or the answer's numeric range
 2. write monotonic P(mid)   - F F F T T T (minimize) or T T T F F F (maximize)
 3. shrink toward the line    - minimize: if P -> hi=mid ; maximize: if P -> lo=mid (round up)
```

## LeetCode Practice Ladder (the 7 walkthroughs)

```
704  Binary Search .............. classic 3-way compare, lo <= hi
 │
 ▼
34   First & Last Position ...... lower_bound + upper_bound; presence check
 │
 ▼
162  Find Peak Element .......... binary search on SLOPE (no sorted array)
 │
 ▼
33   Search Rotated ............. decide which half is sorted, then range-check
 │
 ▼
875  Koko Eating Bananas ........ binary search on the ANSWER + feasibility
 │
 ▼
410  Split Array Largest Sum .... minimize-the-maximum via greedy predicate
 │
 ▼
4    Median of Two Sorted ....... search the PARTITION that balances both halves
```

---

*Pattern mastered — stop hunting for a value in the data and start hunting for the line between "no" and "yes." Define the axis, make the question monotonic, and every step throws away half of what's left.*
