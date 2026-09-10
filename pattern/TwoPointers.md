---
layout: simple
title: "Two Pointers Patterns"
permalink: /pattern/two-pointers
---

# Two Pointers Patterns — Comprehensive Guide

The two-pointer technique replaces a nested O(n²) loop with two indices that each sweep the array **once**, giving O(n). The trick is exploiting **structure** — usually sortedness — so that when you move a pointer you can rule out a whole range of possibilities without checking them.

There are three distinct flavors, and confusing them is the main source of bugs. This guide separates them cleanly, then walks 13 LeetCode problems.

---

## From-Scratch Idea: What Makes a Problem Two Pointers

Start with the brute force and ask what it wastes.

To find a pair summing to a target, the obvious code tries every pair: `for i: for j > i`. That is
O(n²), and on a *sorted* array almost all of that work is provably pointless. Put one finger at
each end and look at `a[lo] + a[hi]`:

- Sum too **small**? Every `hi'` below `hi` gives an even smaller sum with this `lo`. So `lo` can
  never pair with anything at or below `hi`... except by growing. **Move `lo` up.** You just
  eliminated an entire column of the O(n²) grid in one comparison.
- Sum too **large**? Symmetrically, **move `hi` down** and eliminate a whole row.

Each comparison retires a row or a column, and there are only `2n` of those, so the scan is O(n).

That is the whole technique, and it generalises past sortedness. The requirement is not "the array
is sorted" — it is:

> **There is an ordering along which the quantity you are testing changes monotonically, so that
> one comparison tells you an entire region cannot contain the answer.**

Sortedness is the most common way to get that guarantee, but not the only one. In Container With
Most Water (§7) the monotone quantity is "the shorter wall caps the area no matter what the other
side does". In Trapping Rain Water (§10) it is "the smaller running maximum decides this column".
In Floyd's cycle detection (§8) the ordering is *time*, and the monotone fact is that the gap
between two pointers moving at different speeds changes by exactly one per step.

### The two questions that identify it

1. **Is there structure that makes one comparison conclusive about a whole range?** Usually:
   sorted input, or a min/max that bounds an outcome. No structure → you need a hash map, sorting
   first, or a different family entirely.
2. **Am I looking for a pair / a partition / an in-place rearrangement, rather than a contiguous
   region under a constraint?** Region under a constraint is
   [Sliding Window](/pattern/sliding-window) — see §15 for the full tie-break.

If both answers are yes, two pointers applies and you are choosing between the three flavors in
§2.

### Why it beats binary search here

Binary search also exploits sortedness, at O(log n) per lookup. For a *single* lookup it wins. But
"find the pair" needs a lookup for every element — O(n log n) — while two pointers gets the whole
sweep in O(n) because each step reuses the position it already earned. When you are going to touch
every element anyway, converging pointers dominate repeated searching.

---

## Master LeetCode Comparison Table

| LC # | Title | Diff | Flavor | The move rule | Cost |
|------|-------|------|--------|---------------|------|
| **167** | Two Sum II (sorted input) | Medium | Opposite ends | sum too small → `lo++`; too big → `hi--` | O(n) / O(1) |
| **125** | Valid Palindrome | Easy | Opposite ends | skip non-alphanumerics, then compare and step both | O(n) / O(1) |
| **977** | Squares of a Sorted Array | Easy | Opposite ends | bigger `abs` end wins, write to the back | O(n) / O(1) |
| **11** | Container With Most Water | Medium | Opposite ends | advance the **shorter** wall — the taller one cannot be improved | O(n) / O(1) |
| **42** | Trapping Rain Water | Hard | Opposite ends + running maxima | advance the side with the **smaller** running max | O(n) / O(1) |
| **15** | 3Sum | Medium | Sort + anchor + converge | fix `i`, two-pointer the suffix, skip duplicates | O(n²) / O(1) |
| **26** | Remove Duplicates from Sorted Array | Easy | Fast–slow | `read` scans, `write` only advances on a new value | O(n) / O(1) |
| **283** | Move Zeroes | Easy | Fast–slow | swap non-zero into `write`, advance | O(n) / O(1) |
| **88** | Merge Sorted Array | Easy | Two reads, one write | fill **backwards** so the write never clobbers an unread slot | O(m+n) / O(1) |
| **75** | Sort Colors (Dutch flag) | Medium | Three-way partition | `lo/mid/hi`; do **not** advance `mid` after swapping with `hi` | O(n) / O(1) |
| **141** | Linked List Cycle | Easy | Fast–slow (Floyd) | speed difference forces a meeting inside any cycle | O(n) / O(1) |
| **142** | Linked List Cycle II | Medium | Fast–slow, two phases | after meeting, restart one pointer at the head at equal speed | O(n) / O(1) |
| **287** | Find the Duplicate Number | Medium | Fast–slow on `i → nums[i]` | LC 142's arithmetic on an implicit linked list | O(n) / O(1) |

Read the **move rule** column top to bottom. Every row is the same sentence in different clothes:
*identify which side is provably not the bottleneck, and retire it.*

---

## Quick Navigation: "I need to..."

| I need to... | Flavor | Section |
|--------------|--------|---------|
| Find a **pair** in a sorted array (sum = target) | Opposite ends | [3](#3-opposite-ends--converging) |
| **Container** area between two walls | Opposite ends | [7](#7-problem-11--container-with-most-water) |
| **Trapping rain water** (water above every bar) | Opposite ends + running maxima | [10](#10-problem-42--trapping-rain-water) |
| Remove duplicates / move zeros **in place** | Fast–slow (same direction) | [4](#4-fastslow--same-direction) |
| Detect a **cycle** in a linked list | Fast–slow (Floyd) | [8](#8-problem-141--linked-list-cycle-floyds) |
| **Partition** an array (Dutch flag, quicksort) | Three pointers | [5](#5-partition--three-way) |
| **k-sum** (3Sum, 4Sum) | Sort + opposite ends | [6](#6-problem-15--3sum) |
| Merge **from both ends of one** array into a sorted result | Opposite ends | [9](#9-problem-977--squares-of-a-sorted-array) |
| Merge **two** sorted arrays in place | Two reads, one write, back-to-front | [11](#11-problem-88--merge-sorted-array) |
| Check a **palindrome**, skipping non-alphanumerics | Opposite ends | [12](#12-problem-125--valid-palindrome) |
| Find where a linked-list cycle **begins** | Fast–slow, phase two | [13](#13-problem-142--linked-list-cycle-ii) |

---

## Table of Contents

1. [The Core Idea: Structure Lets You Skip](#1-the-core-idea-structure-lets-you-skip)
2. [The Three Flavors](#2-the-three-flavors)
3. [Opposite Ends — Converging](#3-opposite-ends--converging)
4. [Fast–Slow — Same Direction](#4-fastslow--same-direction)
5. [Partition — Three-Way](#5-partition--three-way)
6. [Problem 15 — 3Sum](#6-problem-15--3sum)
7. [Problem 11 — Container With Most Water](#7-problem-11--container-with-most-water)
8. [Problem 141 — Linked List Cycle (Floyd's)](#8-problem-141--linked-list-cycle-floyds)
9. [Problem 977 — Squares of a Sorted Array](#9-problem-977--squares-of-a-sorted-array)
10. [Problem 42 — Trapping Rain Water](#10-problem-42--trapping-rain-water)
11. [Problem 88 — Merge Sorted Array](#11-problem-88--merge-sorted-array)
12. [Problem 125 — Valid Palindrome](#12-problem-125--valid-palindrome)
13. [Problem 142 — Linked List Cycle II](#13-problem-142--linked-list-cycle-ii)
14. [Master Comparison Table](#14-master-comparison-table)
15. [Two Pointers vs. Sliding Window](#15-two-pointers-vs-sliding-window)
16. [How to Identify This Pattern](#16-how-to-identify-this-pattern)
17. [Practice Order](#17-practice-order)
18. [Pattern Recognition Cheat Sheet](#18-pattern-recognition-cheat-sheet)

---

## 1. The Core Idea: Structure Lets You Skip

Consider "does a **sorted** array contain two numbers summing to `target`?"

```
nums = [2, 7, 11, 15], target = 9
```

Brute force checks all pairs: O(n²). But sortedness gives a shortcut. Put one pointer at each end:

```
lo=0 (2)                         hi=3 (15)
sum = 2 + 15 = 17 > 9   → 15 is too big with ANY partner ≥ 2, so hi--
sum = 2 + 11 = 13 > 9   → hi--
sum = 2 + 7  = 9  = 9   → found!
```

The key: when `sum > target`, the largest element can't be part of any valid pair (its smallest possible partner already overshoots), so we discard it — one comparison eliminates a whole column of the O(n²) matrix.

`★ Insight ─────────────────────────────────────`
- Each move of a pointer **permanently discards** one row or column of the pair matrix. n moves, n² pairs eliminated — that's the O(n²) → O(n) collapse.
- This only works because the array is sorted: `sum` responds *monotonically* to pointer moves (move `lo` right → sum up; move `hi` left → sum down). No monotonic response, no skipping, no two pointers. That's why so many two-pointer problems begin with "sort first."
`─────────────────────────────────────────────────`

---

## 2. The Three Flavors

```
OPPOSITE ENDS               FAST–SLOW                  PARTITION (3-way)
converge inward             same direction, gap        low / mid / high

lo →         ← hi           slow →                     [ <p │ =p │ ? │ >p ]
[ · · · · · · · ]                 fast →→               lo    mid    hi
                            [ · · · · · · · ]
target/pair problems        in-place filter,           Dutch national flag,
on sorted data              cycle detection            quicksort partition
```

| Flavor | Pointers start | Movement | Typical use |
|--------|----------------|----------|-------------|
| **Opposite ends** | `lo=0`, `hi=n-1` | toward each other | pair sum, container, palindrome, reverse |
| **Fast–slow** | both at start | same direction, different speeds/conditions | dedup in place, move zeros, cycle detect |
| **Partition** | 2–3 pointers | sweep + swap | Dutch flag, quickselect |

---

## 3. Opposite Ends — Converging

**Problem (LC 167)**: two-sum on a **sorted** array, return 1-indexed positions.

```python
def two_sum_sorted(numbers, target):
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]
        elif s < target:
            lo += 1        # need a bigger sum → raise the low end
        else:
            hi -= 1        # need a smaller sum → lower the high end
    return []
```

Same skeleton solves **LC 125 (valid palindrome)** — compare `s[lo]` vs `s[hi]`, move both inward — and **LC 344 (reverse string)** — swap `s[lo], s[hi]` then move both.

```
Palindrome check "racecar":
lo=0 'r' == hi=6 'r' ✓  move both
lo=1 'a' == hi=5 'a' ✓
lo=2 'c' == hi=4 'c' ✓
lo=3 == hi=3           stop → palindrome
```

---

## 4. Fast–Slow — Same Direction

**Problem (LC 26)**: remove duplicates from a sorted array in place, return new length.

`slow` marks the write position (end of the deduped prefix); `fast` scans ahead looking for the next new value.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0                       # last unique element sits here
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]  # write the new unique value
    return slow + 1
```

```
nums = [1,1,2,2,3]

fast=1 (1) == nums[slow=0] (1)   skip
fast=2 (2) != 1   slow→1, nums[1]=2   → [1,2,2,2,3]
fast=3 (2) == nums[1] (2)   skip
fast=4 (3) != 2   slow→2, nums[2]=3   → [1,2,3,2,3]

length = slow+1 = 3, array prefix [1,2,3]
```

**LC 283 (move zeroes)** is the same shape: `slow` is the write position for non-zeros, `fast` scans; swap on non-zero.

`★ Insight ─────────────────────────────────────`
- Fast–slow "same direction" is really a **read pointer / write pointer** split. `fast` reads every element; `slow` only advances when something deserves to be kept. The region `[0..slow]` is always the finished result — an invariant you can lean on.
- This is how you get O(1) extra space: you overwrite the input in place rather than building a new array.
`─────────────────────────────────────────────────`

---

## 5. Partition — Three-Way

**Problem (LC 75, Dutch National Flag)**: sort an array of 0s, 1s, 2s in one pass, in place.

Three pointers carve the array into four zones: `[0..low)` all 0s, `[low..mid)` all 1s, `[mid..high]` unknown, `(high..end]` all 2s.

```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1                    # already in place
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                   # do NOT advance mid — swapped-in value unexamined
```

```
nums = [2,0,2,1,1,0]

mid=0 val2 swap high=5  [0,0,2,1,1,2] high→4
mid=0 val0 swap low=0   [0,0,2,1,1,2] low→1 mid→1
mid=1 val0 swap low=1   [0,0,2,1,1,2] low→2 mid→2
mid=2 val2 swap high=4  [0,0,1,1,2,2] high→3
mid=2 val1              mid→3
mid=3 val1              mid→4  (mid>high stop)

[0,0,1,1,2,2] ✓
```

`★ Insight ─────────────────────────────────────`
- The asymmetry is deliberate: after swapping from `high`, `mid` does **not** advance because the value that came from the right end hasn't been classified yet. After swapping from `low`, it's safe to advance both — the value from `low` is already known to be a 1 (everything before `mid` is 0s and 1s).
- Getting `mid++` wrong on the `==2` branch is the classic Dutch-flag bug. Trace one swap by hand to lock it in.
`─────────────────────────────────────────────────`

---

## 6. Problem 15 — 3Sum

**Difficulty**: Medium

> Find all unique triplets that sum to 0.

Sort, then fix each element and run an **opposite-ends** two-pointer for the remaining pair. Sorting is what unlocks both the two-pointer sweep and easy duplicate-skipping.

```python
def three_sum(nums):
    nums.sort()
    n = len(nums)
    result = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue                       # skip duplicate anchor
        if nums[i] > 0:
            break                          # smallest is positive → no zero sum left
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                # skip duplicate pair members
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1
    return result
```

```
nums sorted = [-4,-1,-1,0,1,2]

i=0 (-4)  lo=1 hi=5: -4-1+2=-3<0 lo++; ... no triplet
i=1 (-1)  lo=2 hi=5: -1-1+2=0 → [-1,-1,2]; lo++hi--
                     -1+0+1=0 → [-1,0,1]
i=2 (-1)  duplicate of i=1 → skip
...
result = [[-1,-1,2], [-1,0,1]]
```

The whole thing is O(n²): one outer loop × one linear two-pointer sweep. **LC 16 (3Sum Closest)** and **LC 18 (4Sum)** extend the same idea — add another fixed loop for 4Sum.

---

## 7. Problem 11 — Container With Most Water

**Difficulty**: Medium

> Heights `[i]`; pick two lines forming a container. Maximize area = `min(h[lo], h[hi]) × (hi - lo)`.

Opposite ends. Area is bounded by the **shorter** wall, so always move the shorter one — moving the taller can never help.

```python
def max_area(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        area = min(height[lo], height[hi]) * (hi - lo)
        best = max(best, area)
        if height[lo] < height[hi]:
            lo += 1        # shorter wall limits us; only raising it can help
        else:
            hi -= 1
    return best
```

```
height = [1,8,6,2,5,4,8,3,7]

lo=0(1) hi=8(7) area=min(1,7)*8=8   move lo (shorter)
lo=1(8) hi=8(7) area=min(8,7)*7=49  move hi
lo=1(8) hi=7(3) area=3*6=18         move hi
lo=1(8) hi=6(8) area=8*5=40         move hi
... best stays 49

best = 49
```

`★ Insight ─────────────────────────────────────`
- Why moving the shorter wall is safe: the width always shrinks as pointers converge. The only way to *beat* the current area is a taller minimum wall. Moving the taller wall keeps the same (shorter) limiter and a smaller width → strictly worse. So the shorter wall is the only move with upside. This "prune the provably-worse move" reasoning is the heart of opposite-ends two pointers.
`─────────────────────────────────────────────────`

---

## 8. Problem 141 — Linked List Cycle (Floyd's)

**Difficulty**: Easy (but the reasoning is deep)

> Does a linked list contain a cycle?

Fast–slow on a linked list: `slow` steps 1, `fast` steps 2. If there's a cycle, `fast` laps `slow` and they meet; if not, `fast` hits the end.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

```
1 → 2 → 3 → 4 → 5 ─┐
        ↑──────────┘   (5 points back to 3)

step  slow  fast
 1     2     3
 2     3     5
 3     4     4    ← meet → cycle
```

`★ Insight ─────────────────────────────────────`
- Why they *must* meet inside a cycle: once both are in the loop, `fast` gains one position on `slow` every step. The gap shrinks by exactly 1 each step in a finite cycle, so it hits 0 — they collide. No cycle → `fast` reaches `None` first.
- **Finding the cycle start** (LC 142): after they meet, reset one pointer to `head` and advance both by 1; they meet at the entry. This falls out of the distance algebra of the meeting point — a classic follow-up worth memorizing.
`─────────────────────────────────────────────────`

---

## 9. Problem 977 — Squares of a Sorted Array

**Difficulty**: Easy

> Given a sorted array (may contain negatives), return the sorted squares.

Squaring breaks sortedness because large negatives become large positives. The largest square is always at one of the **two ends**, so fill the result from the back using opposite-ends pointers.

```python
def sorted_squares(nums):
    n = len(nums)
    result = [0] * n
    lo, hi = 0, n - 1
    for pos in range(n - 1, -1, -1):     # fill largest-first
        if abs(nums[lo]) > abs(nums[hi]):
            result[pos] = nums[lo] ** 2
            lo += 1
        else:
            result[pos] = nums[hi] ** 2
            hi -= 1
    return result
```

```
nums = [-4,-1,0,3,10]

pos=4  |−4|=4 vs |10|=10 → hi: 100, hi→3
pos=3  |−4|=4 vs |3|=3   → lo: 16,  lo→1
pos=2  |−1|=1 vs |3|=3   → hi: 9,   hi→2
pos=1  |−1|=1 vs |0|=0   → lo: 1,   lo→2
pos=0  lo==hi (0)        → 0

result = [0,1,9,16,100]
```

A merge-from-the-ends trick: the two ends are the two "largest square" candidates, and each step commits the bigger one.

---

## 10. Problem 42 — Trapping Rain Water

> Given `height[i]` = the height of bar `i` (width 1 each), compute how much rain water is trapped
> between the bars. `[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`.

The reframe that unlocks it: **stop thinking about pools and think about one column at a time.**
Water sitting above bar `i` is bounded by the tallest bar to its left and the tallest to its
right — the shorter of those two is the water line:

```
water[i] = min(maxLeft[i], maxRight[i]) - height[i]      (clamped at 0)
```

The obvious implementation precomputes both prefix-max arrays in O(n) space. The two-pointer
version gets it in O(1) space by exploiting one observation: **you only need the smaller of the
two maxima to be certain.** If `maxLeft < maxRight`, then whatever happens on the right cannot
lower the water line at the left pointer — `maxLeft` already decides it. So you can safely settle
the left column and advance.

```python
def trap(height):
    if not height:
        return 0
    lo, hi = 0, len(height) - 1
    max_left, max_right = height[lo], height[hi]
    total = 0

    while lo < hi:
        if max_left <= max_right:
            lo += 1
            max_left = max(max_left, height[lo])
            total += max_left - height[lo]      # never negative: max_left >= height[lo]
        else:
            hi -= 1
            max_right = max(max_right, height[hi])
            total += max_right - height[hi]
    return total
```

```
height = [0,1,0,2,1,0,1,3,2,1,2,1]

lo=0 hi=11  maxL=0  maxR=1   maxL<=maxR -> lo=1,  maxL=1, water += 1-1 = 0   total=0
lo=1 hi=11  maxL=1  maxR=1   maxL<=maxR -> lo=2,  maxL=1, water += 1-0 = 1   total=1
lo=2 hi=11  maxL=1  maxR=1   maxL<=maxR -> lo=3,  maxL=2, water += 2-2 = 0   total=1
lo=3 hi=11  maxL=2  maxR=1   maxL> maxR -> hi=10, maxR=2, water += 2-2 = 0   total=1
lo=3 hi=10  maxL=2  maxR=2   maxL<=maxR -> lo=4,  maxL=2, water += 2-1 = 1   total=2
lo=4 hi=10  maxL=2  maxR=2   maxL<=maxR -> lo=5,  maxL=2, water += 2-0 = 2   total=4
lo=5 hi=10  maxL=2  maxR=2   maxL<=maxR -> lo=6,  maxL=2, water += 2-1 = 1   total=5
lo=6 hi=10  maxL=2  maxR=2   maxL<=maxR -> lo=7,  maxL=3, water += 3-3 = 0   total=5
lo=7 hi=10  maxL=3  maxR=2   maxL> maxR -> hi=9,  maxR=2, water += 2-1 = 1   total=6
lo=7 hi=9   maxL=3  maxR=2   maxL> maxR -> hi=8,  maxR=2, water += 2-2 = 0   total=6
lo=7 hi=8   maxL=3  maxR=2   maxL> maxR -> hi=7   loop ends

answer = 6  ✓
```

**Complexity**: O(n) time, O(1) space.

`★ Insight ─────────────────────────────────────`
- The move rule is the same one as Container With Most Water (§7), for the same reason: **advance the pointer whose side is provably the binding constraint.** In §7 that is the shorter wall; here it is the smaller running maximum. Recognising "the smaller side decides, so it is safe to retire it" is the whole two-pointer discipline in one sentence.
- Note what you never compute: the actual right-maximum array. You only ever need to *know which side is smaller*, not its exact future value. Two pointers repeatedly trades "know everything" for "know enough to make one safe move."
`─────────────────────────────────────────────────`

Three more ways to solve this — prefix-max arrays, a monotonic stack filling horizontal layers, and
a DP formulation — are in [Stack & Queue §10](/pattern/stack-queue).

---

## 11. Problem 88 — Merge Sorted Array

> `nums1` has length `m + n`: its first `m` slots hold sorted values and the last `n` are zero
> padding. `nums2` holds `n` sorted values. Merge `nums2` into `nums1` **in place**.

The naive merge writes front-to-back into a new array. In place, that would overwrite `nums1`
values you have not read yet. **Fill from the back instead**: the largest remaining element goes
into the last unwritten slot, and that slot is always at or beyond both read pointers, so nothing
is ever clobbered.

This is three pointers moving in the same direction: two reads (`i` into `nums1`, `j` into
`nums2`) and one write (`k`).

```python
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1

    while j >= 0:                       # only nums2 can still be unplaced
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
```

```
nums1 = [1,2,3,0,0,0], m=3   nums2 = [2,5,6], n=3

i=2 j=2 k=5:  nums1[2]=3 vs nums2[2]=6  ->  take 6   nums1=[1,2,3,0,0,6]  j=1 k=4
i=2 j=1 k=4:  nums1[2]=3 vs nums2[1]=5  ->  take 5   nums1=[1,2,3,0,5,6]  j=0 k=3
i=2 j=0 k=3:  nums1[2]=3 vs nums2[0]=2  ->  take 3   nums1=[1,2,3,3,5,6]  i=1 k=2
i=1 j=0 k=2:  nums1[1]=2 vs nums2[0]=2  ->  take 2 (from nums2, ties go right)
                                                     nums1=[1,2,2,3,5,6]  j=-1 k=1
j < 0  ->  stop. nums1[0..1] = [1,2] are already correct.

answer = [1,2,2,3,5,6]  ✓
```

**Complexity**: O(m + n) time, O(1) extra space.

`★ Insight ─────────────────────────────────────`
- **Why the loop condition is `j >= 0` and not `i >= 0 and j >= 0`:** if `nums2` runs out first, every remaining `nums1` value is already in its final position — there is nothing to move. If `nums1` runs out first, the rest of `nums2` still has to be copied down. The asymmetry is real, and writing the symmetric condition is the classic bug here.
- **Direction is the entire trick.** In-place array surgery almost always wants the direction in which the write pointer stays ahead of every read pointer. Ask "which end is safe to write into?" before writing a line.
`─────────────────────────────────────────────────`

---

## 12. Problem 125 — Valid Palindrome

> Return `true` if a string is a palindrome, considering only alphanumeric characters and
> ignoring case. `"A man, a plan, a canal: Panama"` → `true`.

Textbook converging pointers, with one wrinkle: the pointers must **skip characters that do not
count** before every comparison. Do the filtering inside the loop rather than building a cleaned
copy, and the space stays O(1).

```python
def is_palindrome(s):
    lo, hi = 0, len(s) - 1

    while lo < hi:
        while lo < hi and not s[lo].isalnum():      # guard lo < hi in BOTH skips
            lo += 1
        while lo < hi and not s[hi].isalnum():
            hi -= 1
        if s[lo].lower() != s[hi].lower():
            return False
        lo += 1
        hi -= 1

    return True
```

```
s = "A man, a plan, a canal: Panama"

lo=0  'A'   hi=29 'a'    a == a  ->  lo=1  hi=28
lo=1  ' '   skip -> lo=2 'm'
                    hi=28 'm'    m == m  ->  lo=3  hi=27
lo=3  'a'   hi=27 'a'    a == a  ->  lo=4  hi=26
lo=4  'n'   hi=26 'n'    n == n  ->  ...
... every comparison matches, pointers cross ...
answer = True  ✓

s = "race a car"
lo=0 'r' vs hi=9 'r'  ok
lo=1 'a' vs hi=8 'a'  ok
lo=2 'c' vs hi=7 'c'  ok
lo=3 'e' vs hi=6 'a'  ->  mismatch, return False  ✓
```

**Complexity**: O(n) time, O(1) space. Each pointer only ever advances, so the inner `while` loops
are amortized O(1) — the two skips together do at most `n` steps across the whole run.

`★ Insight ─────────────────────────────────────`
- **The `lo < hi` guard inside the skip loops is not optional.** On an input with no alphanumeric characters at all (`",.;"`), dropping it walks `lo` straight past the end of the string. Any time a two-pointer loop contains a nested advance, that nested loop needs the same bound as the outer one.
- Variant worth knowing: LC 680 (Valid Palindrome II) allows deleting **one** character. On the first mismatch, the answer is "is `s[lo+1..hi]` *or* `s[lo..hi-1]` a clean palindrome?" — one mismatch means at most two sub-checks, so it stays O(n).
`─────────────────────────────────────────────────`

---

## 13. Problem 142 — Linked List Cycle II

> Return the node where a cycle *begins*, or `None` if there is no cycle. O(1) space.

§8 established that fast and slow meet inside the cycle. This problem asks for something sharper:
*where the cycle starts*. The answer is a small piece of arithmetic that looks like magic and is
not.

Let `L` be the distance from the head to the cycle entry, `C` the cycle length, and `k` the
distance from the entry to the meeting point. When they meet:

```
slow travelled:  L + k                 (+ possibly some full loops, which cancel mod C)
fast travelled:  L + k + nC            for some n >= 1
fast = 2 * slow  ->  L + k + nC = 2(L + k)  ->  nC = L + k  ->  L = nC - k
```

`L = nC − k` says: **the distance from the head to the entry equals the distance from the meeting
point onward to the entry** (going `n` laps and stopping `k` short). So put one pointer back at
the head, leave the other at the meeting point, advance both one step at a time, and they collide
exactly at the entry.

```python
def detect_cycle(head):
    slow = fast = head

    while fast and fast.next:               # phase 1: find a meeting point
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None                         # fell off the end: no cycle

    slow = head                             # phase 2: walk both at speed 1
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow
```

```
list: 3 -> 2 -> 0 -> -4 -> (back to 2)
index: 0    1    2     3        entry = index 1, so L = 1, C = 3

phase 1:
  slow=3(0) fast=3(0)
  slow=2(1) fast=0(2)
  slow=0(2) fast=0(2)   meet at index 2, so k = 1

  check: L = nC - k  ->  1 = 1*3 - 1 - 1?   nC = L + k = 2 ... n is not an integer here
  because the very first step already put fast inside the loop. The identity holds
  modulo C: (L + k) mod C == 0 is what phase 2 actually relies on.

phase 2:
  slow=3(0) fast=0(2)
  slow=2(1) fast=-4(3)   not equal
  ... continue ...
  they collide at index 1  ->  node 2  ✓
```

**Complexity**: O(n) time, O(1) space.

`★ Insight ─────────────────────────────────────`
- **Two phases, two different speeds.** Phase 1 needs the speed *difference* (that is what guarantees a meeting inside a cycle). Phase 2 needs equal speeds (that is what makes the distance identity collide them at the entry). Mixing up which phase uses which is the standard error.
- The `while ... else` is doing real work here: Python runs the `else` only when the loop exits *without* `break`, which is exactly the no-cycle case. Written with a flag variable it is three lines longer and no clearer.
- Same arithmetic solves LC 287 (Find the Duplicate Number): treat `i -> nums[i]` as a linked list; the duplicate value is the node where that list's cycle begins.
`─────────────────────────────────────────────────`

---

## 14. Master Comparison Table

| Problem | Flavor | Pointers | Move rule | Precondition |
|---------|--------|----------|-----------|--------------|
| **167** Two Sum II | Opposite ends | `lo, hi` | sum<t → lo++; sum>t → hi-- | sorted |
| **125** Palindrome | Opposite ends | `lo, hi` | both inward if match | — |
| **11** Container | Opposite ends | `lo, hi` | move shorter wall | — |
| **15** 3Sum | Sort + opposite | `i` + `lo, hi` | fix i, sweep pair | sorted |
| **26** Dedup | Fast–slow | `slow, fast` | write on new value | sorted |
| **283** Move zeroes | Fast–slow | `slow, fast` | write on non-zero | — |
| **75** Sort colors | Partition | `low, mid, high` | swap by value | — |
| **141** Cycle | Fast–slow | `slow, fast` | ×1 vs ×2 speed | linked list |
| **977** Sorted squares | Opposite ends | `lo, hi` | bigger \|·\| fills back | sorted |

---

## 15. Two Pointers vs. Sliding Window

They look similar — both use two indices — but the intent differs:

```
SLIDING WINDOW                      TWO POINTERS (opposite ends)

both pointers move FORWARD          pointers move TOWARD each other
region between them = the answer    the PAIR at the pointers = the answer
resizes on a running constraint     converges by pruning provably-bad moves
"longest/shortest subarray"         "find a pair / partition"
```

| Question | Answer → technique |
|----------|--------------------|
| Do both pointers only move forward, and is the *region between them* what I care about? | **Sliding window** |
| Do pointers start at opposite ends and converge? | **Two pointers (opposite ends)** |
| Is one pointer reading while another writes, same direction? | **Two pointers (fast–slow)** |

`★ Insight ─────────────────────────────────────`
- Sliding window is technically a same-direction two-pointer where the *gap* is the object of interest. The community treats them as separate patterns because the *reasoning* differs: windows reason about a maintained region under a constraint; opposite-ends pointers reason about pruning half the search space per move on sorted data. Recognizing which mental model applies is faster than memorizing code.
`─────────────────────────────────────────────────`

---

## 16. How to Identify This Pattern

### Trigger checklist

```
Is the input SORTED (or worth sorting)?
  ├── "find a pair/triplet summing to X"     → opposite ends (§3, §6)
  ├── "max area / trapping / two walls"      → opposite ends (§7)
  └── "squares / merge two sorted"           → opposite ends fill (§9)

In-place array modification, O(1) space?
  ├── "remove / dedup / move elements"       → fast–slow (§4)
  └── "sort into ≤3 categories"              → partition (§5)

Linked list?
  └── "detect cycle / find middle / nth"     → fast–slow (§8)
```

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Forgetting to sort first | Opposite-ends pair problems need sorted input |
| Not skipping duplicates in k-sum | Skip equal anchors and equal pair members (§6) |
| Advancing `mid` after high-swap in Dutch flag | Don't — the swapped-in value is unexamined (§5) |
| `while fast.next` without `fast` null check | `while fast and fast.next` — fast can be `None` |
| Using two pointers on unsorted data for pair-sum | No monotonic response → use a hash set instead |

---

## 17. Practice Order

```
Start here
    │
    ▼
  167 (Easy)   ──── Opposite ends: the converge-on-sorted mechanic
    │
    ▼
  26 (Easy)    ──── Fast–slow: read pointer vs write pointer
    │
    ▼
  977 (Easy)   ──── Opposite ends filling a result from the back
    │
    ▼
  11 (Medium)  ──── Prune the provably-worse move
    │
    ▼
  75 (Medium)  ──── Three-way partition (Dutch flag)
    │
    ▼
  15 (Medium)  ──── Sort + fixed anchor + two-pointer sweep
    │
    ▼
  125 (Easy)   ──── Converging with a skip rule (guard the inner loops)
    │
    ▼
  88 (Easy*)   ──── Direction matters: fill backwards to avoid clobbering
    │
    ▼
  11 (Medium)  ──── Prune the provably-worse move
    │
    ▼
  75 (Medium)  ──── Three-way partition (Dutch flag)
    │
    ▼
  15 (Medium)  ──── Sort + fixed anchor + two-pointer sweep
    │
    ▼
  141 (Easy*)  ──── Floyd's cycle detection (easy code, deep why)
    │
    ▼
  142 (Medium) ──── The distance identity: L = nC - k
    │
    ▼
  42 (Hard)    ──── The capstone: same move rule as 11, harder to see
```

---

## 18. Pattern Recognition Cheat Sheet

### Signal → flavor

| You see in the problem statement | Reach for | Because |
|----------------------------------|-----------|---------|
| "sorted array" + "find a pair / triplet summing to" | Opposite ends | Sortedness makes the sum respond monotonically to each move |
| "in place", "O(1) extra space", "return the new length" | Fast–slow | A write pointer trailing a read pointer is the in-place idiom |
| "without using extra space" on a **linked list** | Fast–slow (Floyd) | You cannot index a list; speed difference is the only free structure |
| "partition into three groups", "sort 0s, 1s, 2s" | Three-way (Dutch flag) | One pass, three regions, three pointers |
| "maximum area / water between" | Opposite ends with a min-bound | The shorter side caps the outcome, so it is safe to retire |
| "merge two sorted ..." with in-place output | Two reads, one write, backwards | Backwards keeps the write ahead of both reads |
| "longest / shortest subarray such that ..." | **Not this pattern** → [Sliding Window](/pattern/sliding-window) | You want a region under a constraint, not a pair |
| Unsorted + "find a pair summing to k" | **Not this pattern** → hash map, O(n) | Without order, no comparison is conclusive about a range |

### Bug checklist

Run these five questions over any two-pointer loop before you submit:

1. **Is the loop condition `lo < hi` or `lo <= hi`?** Converging-for-a-pair wants `<` (an element cannot pair with itself). Scanning every position wants `<=`.
2. **Does every branch advance a pointer?** A branch that changes no index is an infinite loop.
3. **Do nested skip loops carry the same bound as the outer loop?** See §12 — this is the classic overrun.
4. **After swapping with the far pointer, should the near pointer advance?** In Dutch flag, no: the value you swapped in from `hi` has not been examined yet.
5. **Do duplicates need skipping?** In 3Sum, failing to skip equal values emits duplicate triplets even though the algorithm is otherwise correct.

---

## The Two-Pointer Toolbox at a Glance

```
                        Two indices, one pass
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   OPPOSITE ENDS            FAST–SLOW               THREE-WAY
   lo=0, hi=n-1             both start left         lo, mid, hi
   move inward              different speeds        one pass, 3 regions
        │                        │                        │
   need: monotone           need: a rate            need: 3-valued key
   response to a move            difference
        │                        │                        │
   167  two-sum sorted      26   dedup in place     75   Dutch flag
   125  palindrome          283  move zeroes        quicksort partition
   977  sorted squares      141  cycle detect
   11   container           142  cycle entry
   42   trapping water      287  duplicate number
   15   3Sum (+ anchor)
```

**The one question that picks the flavor**: do the pointers *converge* (answer is a pair or a
bounded region), *chase* (one lags to mark a boundary, or one outruns to detect a cycle), or
*partition* (three regions grown simultaneously)?

---

## When This Fails

Two pointers needs an ordering along which one comparison rules out a whole region. It breaks
when that ordering is absent or is destroyed:

- **Unsorted input, "find a pair summing to k".** No comparison is conclusive about any range.
  Use a hash map for O(n), or sort first and pay O(n log n).
- **Negative numbers with a "sum at least k" window.** Extending the region no longer increases
  the sum, so the monotonicity argument collapses. Move to prefix sums plus a monotonic deque —
  [Sliding Window §13](/pattern/sliding-window).
- **You need the original indices but the algorithm requires sorting.** Sorting destroys them.
  Sort `(value, index)` pairs, or use a hash map instead (this is why LC 1 is not a two-pointer
  problem while LC 167 is).
- **The answer is a non-contiguous subsequence.** Two pointers only ever produces a pair, a
  contiguous region, or a partition. Subsequences are [DP](/pattern/dp).

## Self-Test

Answer these from memory, out loud or on paper, *before* looking. Recognition is not
recall: rereading an explanation feels like knowing, and it is not. A question you cannot answer
cold names the exact section to revisit — you do not need to reread the guide.


**1. What property must hold for two converging pointers to be correct?**

<details markdown="1">
<summary>Answer</summary>

Moving a pointer must let you rule out an entire row or column of the O(n²) pair space. Concretely: from the current comparison you can prove that one of the two current elements cannot be part of any answer with anything still in range, so retiring it loses nothing. Sortedness is the usual source of that guarantee, but it is not the only one.

</details>

**2. In Container With Most Water, why is it safe to advance the *shorter* wall?**

<details markdown="1">
<summary>Answer</summary>

Area is `min(h[lo], h[hi]) * (hi - lo)`. Keeping the shorter wall and moving the taller one strictly shrinks the width while the height stays capped by that same shorter wall — so every such pair is worse than the one you already measured. The shorter wall can never improve while it stays, so retire it.

</details>

**3. In Dutch-flag partitioning, why must `mid` not advance after swapping with `hi`?**

<details markdown="1">
<summary>Answer</summary>

The value swapped in from `hi` has never been examined. Advancing past it skips classifying it. After swapping with `lo`, by contrast, the incoming value is already known to be in the low group, so `mid` may advance.

</details>

**4. Floyd's cycle detection: why do the pointers meet, and where is the cycle *entry*?**

<details markdown="1">
<summary>Answer</summary>

Inside a cycle the gap between a speed-2 and a speed-1 pointer closes by exactly one per step, so it must reach zero — they meet. For the entry: with `L` = head-to-entry and `k` = entry-to-meeting-point, `fast = 2 * slow` gives `L ≡ −k (mod C)`. So restarting one pointer at the head and walking both at speed 1 collides exactly at the entry.

</details>

**5. Why fill backwards when merging two sorted arrays in place?**

<details markdown="1">
<summary>Answer</summary>

Writing front-to-back would overwrite `nums1` entries you have not read yet. Filling from the back means the write index is always at or beyond both read indices, so nothing is clobbered.

</details>

**6. Why is the loop condition in LC 88 `while j >= 0` rather than `while i >= 0 and j >= 0`?**

<details markdown="1">
<summary>Answer</summary>

If `nums2` is exhausted, the remaining `nums1` values are already in their final positions — no work left. If `nums1` is exhausted first, the rest of `nums2` still has to be copied. The asymmetry is real, and the symmetric condition is the classic bug.

</details>

**7. What breaks in a palindrome check if you omit `lo < hi` from the inner skip loops?**

<details markdown="1">
<summary>Answer</summary>

On input with no alphanumeric characters at all, the skip walks straight past the end of the string. Any nested advance inside a two-pointer loop needs the same bound as the outer loop.

</details>

**8. Name the three flavours and the one question that distinguishes them.**

<details markdown="1">
<summary>Answer</summary>

Opposite-ends (converging), fast–slow (same direction, different rates), and three-way partition. The question: do the pointers *converge* on a pair or bounded region, *chase* to mark a boundary or detect a cycle, or *partition* the array into three growing regions?

</details>

---

## See Also

- [Sliding Window](/pattern/sliding-window) — the sibling technique; §15 is the tie-breaker between them.
- [Binary Search](/pattern/binary-search) — the other technique that exploits sortedness. Two pointers is O(n) after sorting; binary search is O(log n) per lookup. Pairs beat search when you scan every element anyway.
- [Stack & Queue §10](/pattern/stack-queue) — trapping rain water solved three more ways, including the monotonic stack that fills water layer by layer.
- [Prefix Sum](/pattern/prefix-sum) — what to use when the array has negatives and the two-pointer monotonicity argument collapses.
- [Pattern Decision Map](/pattern/decision-map) — the router: which technique does a cold problem call for?
- [Pattern Mastery Program](/pattern/mastery) — the spaced-repetition schedule, mastery checklist, and drill formats that turn reading into recall.

---

*Pattern mastered — structure lets one comparison discard many, so two sweeping pointers replace a nested loop.*
