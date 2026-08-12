---
layout: simple
title: "Two Pointers Patterns"
permalink: /pattern/two-pointers
---

# Two Pointers Patterns — Comprehensive Guide

The two-pointer technique replaces a nested O(n²) loop with two indices that each sweep the array **once**, giving O(n). The trick is exploiting **structure** — usually sortedness — so that when you move a pointer you can rule out a whole range of possibilities without checking them.

There are three distinct flavors, and confusing them is the main source of bugs. This guide separates them cleanly, then walks 9 LeetCode problems.

---

## Quick Navigation: "I need to..."

| I need to... | Flavor | Section |
|--------------|--------|---------|
| Find a **pair** in a sorted array (sum = target) | Opposite ends | [3](#3-opposite-ends--converging) |
| **Container / trapping** area problems | Opposite ends | [7](#7-problem-11--container-with-most-water) |
| Remove duplicates / move zeros **in place** | Fast–slow (same direction) | [4](#4-fast-slow--same-direction) |
| Detect a **cycle** in a linked list | Fast–slow (Floyd) | [8](#8-problem-141--linked-list-cycle-floyds) |
| **Partition** an array (Dutch flag, quicksort) | Three pointers | [5](#5-partition--three-way) |
| **k-sum** (3Sum, 4Sum) | Sort + opposite ends | [6](#6-problem-15--3sum) |
| Merge two sorted arrays | Parallel pointers | [9](#9-problem-977--squares-of-a-sorted-array) |

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
10. [Master Comparison Table](#10-master-comparison-table)
11. [Two Pointers vs. Sliding Window](#11-two-pointers-vs-sliding-window)
12. [How to Identify This Pattern](#12-how-to-identify-this-pattern)
13. [Practice Order](#13-practice-order)

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

## 10. Master Comparison Table

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

## 11. Two Pointers vs. Sliding Window

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

## 12. How to Identify This Pattern

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

## 13. Practice Order

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
  141 (Easy*)  ──── Floyd's cycle detection (easy code, deep why)
```

---

*Pattern mastered — structure lets one comparison discard many, so two sweeping pointers replace a nested loop.*
