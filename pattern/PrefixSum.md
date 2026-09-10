---
layout: simple
title: "Prefix Sum Patterns"
permalink: /pattern/prefix-sum
---

# Prefix Sum Patterns — Comprehensive Guide

Prefix sum is one of the most fundamental techniques in competitive programming. The core idea is **precomputation**: spend O(N) time building an auxiliary array so that subsequent range queries take O(1). But prefix sums go far beyond simple "range sum" — they combine with hash maps, modular arithmetic, difference arrays, 2D grids, XOR, and even trees to solve an enormous variety of problems.

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| Query **sum of subarray** in O(1) | 1D prefix sum | [1](#1-basic-1d-prefix-sum) |
| Query **sum of submatrix** in O(1) | 2D prefix sum | [2](#2-2d-prefix-sum) |
| Count subarrays with **sum = k** | Prefix sum + hash map | [3](#3-prefix-sum--hash-map) |
| Count subarrays **divisible by k** | Prefix sum + modular arithmetic | [4](#4-prefix-sum--modular-arithmetic) |
| Apply **range updates** efficiently | Difference array | [5](#5-difference-array-1d) |
| Apply **2D range updates** | 2D difference array | [6](#6-difference-array-2d) |
| Query **XOR of subarray** | Prefix XOR | [7](#7-prefix-xor) |
| Find **product of array except self** | Prefix & suffix products | [8](#8-prefix--suffix-products) |
| Query **path sums on trees** | Prefix sum on trees | [9](#9-prefix-sum-on-trees) |
| Find subarray with sum in **[lo, hi]** | Prefix sum + binary search / BIT | [10](#10-prefix-sum--binary-search) |
| Handle **multiple dimensions** / bitmask sums | Higher-dimensional prefix sums | [11](#11-higher-dimensional-prefix-sums) |

---

## From-Scratch Idea: What Makes a Problem "Prefix Sum"

Before memorizing 11 variants, understand the one move under all of them. A prefix sum answers a question of the form **"what is the aggregate over a contiguous range?"** by precomputing the aggregate over every *prefix* — every range that starts at the beginning. Then any range `[l, r]` is the difference of two prefixes:

```
answer(l, r) = prefix(r) ⊖ prefix(l-1)
```

where `⊖` is the *inverse* of your combine operation. Sum uses subtraction, XOR uses XOR (its own inverse), product uses division (if no zeros). The whole family is this one equation with different operators.

### The two-question identify test

Ask both. If both are "yes," reach for prefix sum:

1. **Is the query over a contiguous range** (subarray, submatrix, root-to-node path)?
2. **Is the aggregate reversible** — can I "undo" the part before `l`? Sum/XOR/count: yes. Max/min: NO (you cannot un-max), so those need sparse tables or segment trees, not prefix sum.

### The mental shift: from "scan the range" to "difference two endpoints"

The naive approach recomputes the range every query — O(N) per query. Prefix sum spends O(N) *once* so every later query is O(1). The symptom that screams "precompute": **many queries on a static array**, or **counting pairs of positions** that satisfy a range condition.

| Symptom in the problem | Axis you build the prefix over | The trick |
|------------------------|-------------------------------|-----------|
| "sum/xor of `a[l..r]`", many queries | index | `pre[r+1] ⊖ pre[l]` |
| "sum of submatrix", many queries | 2D index | inclusion-exclusion (4 corners) |
| "count subarrays with sum = k" | running sum value | hash map: how many earlier prefixes = `cur - k` |
| "count subarrays sum divisible by k" | running sum **mod k** | count equal remainders |
| "apply many range-adds, read once" | index (inverted) | difference array: `d[l]+=v, d[r+1]-=v` |
| "product/min/gcd of all-but-one" | index, both directions | prefix combined with suffix |

### From-scratch template — the one equation, three operators

```python
# SUM: build once, query O(1)
pre = [0]
for x in a: pre.append(pre[-1] + x)
range_sum = pre[r+1] - pre[l]          # inverse of + is -

# XOR: identical shape, ^ is its own inverse
pre = [0]
for x in a: pre.append(pre[-1] ^ x)
range_xor = pre[r+1] ^ pre[l]          # inverse of ^ is ^

# COUNT-PAIRS: don't store the prefix array — stream it into a hash map
count = {0: 1}                          # the empty prefix is a real start point
cur = 0; ans = 0
for x in a:
    cur += x
    ans += count.get(cur - k, 0)        # earlier prefixes that make a range summing to k
    count[cur] = count.get(cur, 0) + 1
```

`★ Insight ─────────────────────────────────────`
- **`count[0] = 1` is not optional.** It represents the empty prefix (sum 0 before any element). Without it, a subarray that starts at index 0 and sums to `k` is never counted — the single most common prefix-sum bug.
- **The array version and the hash-map version are the same idea at different speeds.** When you need *every* range answered → store the whole prefix array. When you need to *count* ranges hitting a target → stream prefixes into a hash map and never store the array. Same equation, different data structure.
- **Reversibility is the gate.** Sum, XOR, count, and product-without-zeros are invertible, so prefix sum works. Max/min/gcd are NOT invertible over a left-truncated range → use prefix+suffix (§8) or a segment tree, never `pre[r]-pre[l]`.
`─────────────────────────────────────────────────`

### LeetCode ↔ CP translation

| LeetCode framing | CP framing | Same technique |
|------------------|-----------|----------------|
| Range Sum Query — Immutable (303) | Static Range Sum Queries (CSES) | 1D prefix sum (§1) |
| Range Sum Query 2D (304) | Forest Queries (CSES) | 2D prefix sum (§2) |
| Subarray Sum Equals K (560) | — | prefix + hash map (§3) |
| Subarray Sums Divisible by K (974) | Subarray Divisibility (CSES) | prefix mod k (§4) |
| Corporate Flight Bookings (1109) | Range Update Queries (CSES) | difference array (§5) |
| XOR Queries of a Subarray (1310) | Range Xor Queries (CSES) | prefix XOR (§7) |
| Count of Range Sum (327) | — | prefix + ordered structure (§10) |

### Master LeetCode Comparison Table

| LC# | Problem | Technique (§) | Difficulty | What you build the prefix over | The O(1)/O(log) query |
|-----|---------|---------------|------------|-------------------------------|-----------------------|
| 303 | Range Sum Query — Immutable | 1D prefix (§1) | Easy | index → running sum | `pre[r+1] - pre[l]` |
| 304 | Range Sum Query 2D — Immutable | 2D prefix (§2) | Medium | (row, col) → running sum | 4-corner inclusion-exclusion |
| 560 | Subarray Sum Equals K | prefix + hash map (§3) | Medium | running sum value → frequency | `count[cur - k]` |
| 974 | Subarray Sums Divisible by K | prefix mod k (§4) | Medium | running sum **mod k** → frequency | `count[cur % k]` |
| 1109 | Corporate Flight Bookings | difference array (§5) | Medium | index (inverted) → deltas | one prefix-sum sweep at the end |
| 1310 | XOR Queries of a Subarray | prefix XOR (§7) | Medium | index → running XOR | `pre[r+1] ^ pre[l]` |
| 238 | Product of Array Except Self | prefix + suffix (§8) | Medium | index, both directions | `left[i] * right[i]` |
| 327 | Count of Range Sum | prefix + ordered set (§10) | Hard | running sum value, order-queried | count prefixes in `[cur-hi, cur-lo]` |

Each section below now carries a **Walkthrough — LC NNN** with the full problem statement, a pattern-focused solution, an executed trace, and an insight box.

---

## Table of Contents

1. [Basic 1D Prefix Sum](#1-basic-1d-prefix-sum)
2. [2D Prefix Sum](#2-2d-prefix-sum)
3. [Prefix Sum + Hash Map](#3-prefix-sum--hash-map)
4. [Prefix Sum + Modular Arithmetic](#4-prefix-sum--modular-arithmetic)
5. [Difference Array (1D)](#5-difference-array-1d)
6. [Difference Array (2D)](#6-difference-array-2d)
7. [Prefix XOR](#7-prefix-xor)
8. [Prefix & Suffix Products](#8-prefix--suffix-products)
9. [Prefix Sum on Trees](#9-prefix-sum-on-trees)
10. [Prefix Sum + Binary Search](#10-prefix-sum--binary-search)
11. [Higher-Dimensional Prefix Sums](#11-higher-dimensional-prefix-sums)
12. [Common Patterns Collection](#12-common-patterns-collection)
13. [Pattern Recognition Cheat Sheet](#13-pattern-recognition-cheat-sheet)

---

## 1. Basic 1D Prefix Sum

### The Idea

Given an array `a[0..n-1]`, build a prefix sum array where:

```
pre[0] = 0
pre[i] = a[0] + a[1] + ... + a[i-1]
```

Then the sum of any subarray `a[l..r]` (inclusive) is:

```
sum(l, r) = pre[r+1] - pre[l]
```

### Visual Trace

```
Index:    0    1    2    3    4    5
Array:  [ 3,   1,   4,   1,   5,   9 ]

Prefix: [0, 3, 4, 8, 9, 14, 23]
         ^  ^  ^  ^  ^   ^   ^
         |  |  |  |  |   |   sum of all 6
         |  |  |  |  |   sum of first 5
         |  |  |  |  sum of first 4
         |  |  |  sum of first 3
         |  |  sum of first 2
         |  sum of first 1
         empty prefix (sum of 0 elements)

Query: sum(2, 4) = pre[5] - pre[2] = 14 - 4 = 10
                 = a[2] + a[3] + a[4] = 4 + 1 + 5 = 10  ✓
```

### Why `pre` has length `n+1`?

The extra `pre[0] = 0` handles the edge case where `l = 0`. Without it, you'd need a special case. With it, `sum(0, r) = pre[r+1] - pre[0] = pre[r+1]` — clean and uniform.

### Implementation

```python
def build_prefix(a):
    n = len(a)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]
    return pre

def range_sum(pre, l, r):
    """Sum of a[l..r] inclusive."""
    return pre[r + 1] - pre[l]

# Python shortcut using itertools
from itertools import accumulate
def build_prefix_v2(a):
    return [0] + list(accumulate(a))
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(N) | O(N) |
| Query | O(1) | — |

### Classic Problems

1. **Static Range Sum Queries** — Direct application
2. **Maximum subarray sum** — Kadane's is better, but `max(pre[j] - pre[i])` for `j > i` also works
3. **Equilibrium index** — Find index where left sum = right sum

### Walkthrough — LC 303: Range Sum Query — Immutable

> **Statement.** Given an integer array `nums`, handle many queries of the form `sumRange(left, right)` = sum of `nums[left..right]` inclusive. `sumRange` may be called up to 10⁴ times. Implement a class `NumArray(nums)` with method `sumRange(left, right)`.

**This template solves: LC 303, 1480 (Running Sum), 724 (Pivot Index).**

The signal is "**many queries, array never changes**" — precompute in the constructor so each query is O(1). Recomputing the range per call would be O(N) each → O(N·Q) total, too slow.

```python
class NumArray:
    def __init__(self, nums):
        # pre[i] = sum of first i elements; pre[0] = 0 (empty prefix)
        self.pre = [0]
        for x in nums:
            self.pre.append(self.pre[-1] + x)

    def sumRange(self, left, right):
        # sum(left..right) = pre[right+1] - pre[left]
        return self.pre[right + 1] - self.pre[left]
```

**Executed trace** on `nums = [-2, 0, 3, -5, 2, -1]`:

```
nums:   -2   0   3  -5   2  -1
pre:  [0, -2, -2, 1, -4, -2, -3]
       ^   ^   ^  ^   ^   ^   ^
       |   |   |  |   |   |   sum of all 6 = -3
       empty prefix = 0

sumRange(0,2) = pre[3] - pre[0] = 1  - 0  = 1   ✓  (-2+0+3)
sumRange(2,5) = pre[6] - pre[2] = -3 - (-2) = -1 ✓  (3-5+2-1)
sumRange(0,5) = pre[6] - pre[0] = -3 - 0  = -3  ✓
```

`★ Insight ─────────────────────────────────────`
- **The constructor pays O(N) once; every query is a single subtraction.** This is the entire prefix-sum bargain — trade one linear pass for constant-time queries forever after.
- **`pre` has length `n+1`, not `n`.** The leading `pre[0] = 0` is what lets `sumRange(0, r)` use the uniform formula `pre[r+1] - pre[0]` with no special case for `left == 0`. Off-by-one bugs here are the #1 prefix-sum mistake.
- **Negatives are fine.** Sum is invertible regardless of sign, so this exact code works on `[-2, 0, 3, ...]`. (Contrast §10, where binary search on prefixes needs *non-negative* values to keep the prefix array sorted.)
`─────────────────────────────────────────────────`

---

## 2. 2D Prefix Sum

### The Idea

For a 2D grid, precompute the sum of every rectangle from `(0,0)` to `(i,j)`. Then any sub-rectangle sum can be computed in O(1) using **inclusion-exclusion**.

### Building the 2D Prefix Sum

```
pre[i][j] = sum of all grid[r][c] where 0 ≤ r < i, 0 ≤ c < j
```

Formula (1-indexed prefix, 0-indexed grid):

```
pre[i+1][j+1] = grid[i][j] + pre[i][j+1] + pre[i+1][j] - pre[i][j]
```

### Querying a Sub-Rectangle

Sum of grid cells in rectangle `(r1, c1)` to `(r2, c2)` inclusive:

```
sum = pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1]
```

### Visual — Inclusion-Exclusion

```
We want the shaded region:

    c1      c2
     v       v
r1 > ########
     ########
r2 > ########

pre[r2+1][c2+1] includes everything from (0,0) to (r2,c2):

    +-----------+---+
    |     A     | B |
    +-----------+---+  <- r1
    |     C     |###|
    |           |###|
    +-----------+---+  <- r2
         ^         ^
         c1        c2

Answer = Total - A - B - C + overlap(A∩B is empty, but top-left counted)
       = pre[r2+1][c2+1]            (everything)
       - pre[r1][c2+1]              (rows above r1)
       - pre[r2+1][c1]              (cols left of c1)
       + pre[r1][c1]                (top-left corner subtracted twice)
```

### Implementation

```python
def build_2d_prefix(grid):
    R, C = len(grid), len(grid[0])
    pre = [[0] * (C + 1) for _ in range(R + 1)]
    for i in range(R):
        for j in range(C):
            pre[i+1][j+1] = (grid[i][j]
                             + pre[i][j+1]
                             + pre[i+1][j]
                             - pre[i][j])
    return pre

def rect_sum(pre, r1, c1, r2, c2):
    """Sum of grid[r1..r2][c1..c2] inclusive."""
    return (pre[r2+1][c2+1]
            - pre[r1][c2+1]
            - pre[r2+1][c1]
            + pre[r1][c1])
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(R × C) | O(R × C) |
| Query | O(1) | — |

### Classic Problems

1. **Forest Queries (CSES)** — Count trees in sub-rectangle
2. **Maximum sum sub-rectangle** — Combine with Kadane's (O(N³) for N×N)
3. **Counting 1s in binary matrix** — Direct application

### Walkthrough — LC 304: Range Sum Query 2D — Immutable

> **Statement.** Given a 2D matrix, handle many queries `sumRegion(row1, col1, row2, col2)` = sum of all cells in the rectangle with top-left `(row1, col1)` and bottom-right `(row2, col2)` inclusive. Matrix never changes. Implement `NumMatrix(matrix)` and `sumRegion(...)`.

**This template solves: LC 304, 1314 (Matrix Block Sum), 221 (Maximal Square — as a helper).**

Same bargain as 303, one dimension higher. Build a `(R+1)×(C+1)` prefix grid where `pre[i][j]` = sum of everything above-and-left of `(i,j)`. Each query is **four array lookups** via inclusion-exclusion.

```python
class NumMatrix:
    def __init__(self, matrix):
        R, C = len(matrix), len(matrix[0])
        self.pre = [[0] * (C + 1) for _ in range(R + 1)]
        for i in range(R):
            for j in range(C):
                self.pre[i+1][j+1] = (matrix[i][j]
                                      + self.pre[i][j+1]     # region above
                                      + self.pre[i+1][j]     # region left
                                      - self.pre[i][j])      # overlap added twice

    def sumRegion(self, r1, c1, r2, c2):
        p = self.pre
        return (p[r2+1][c2+1]   # whole rectangle from origin to (r2,c2)
                - p[r1][c2+1]   # strip above the query
                - p[r2+1][c1]   # strip left of the query
                + p[r1][c1])    # top-left corner subtracted twice, add back
```

**Executed trace** on the standard LC 304 matrix, `sumRegion(2,1,4,3)`:

```
matrix:                     pre (1-indexed, row 0 / col 0 all zero):
 3 0 1 4 2                    0  0  0  0  0  0
 5 6 3 2 1                    0  3  3  4  8 10
 1 2 0 1 5                    0  8 14 18 24 27
 4 1 0 1 7                    0  9 17 21 28 36
 1 0 3 0 5                    0 13 22 26 34 49
                             0 14 23 30 38 58

sumRegion(2,1,4,3):
  = pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1]
  = pre[5][4]       - pre[2][4]     - pre[5][1]     + pre[2][1]
  = 38              - 24            - 14            + 8
  = 8   ✓   (cells rows 2-4, cols 1-3: 2+0+1 + 1+0+1 + 0+3+0 = 8)
```

(Executed: `sumRegion(2,1,4,3)=8`, `sumRegion(1,1,2,2)=11`, `sumRegion(1,2,2,4)=12` — all correct.)

`★ Insight ─────────────────────────────────────`
- **The `-pre[i][j]` in the build and the `+pre[r1][c1]` in the query are the same correction.** Building sums the "above" and "left" rectangles, which double-count their shared top-left block; the query subtracts two overlapping strips, which double-remove their shared corner. Both fix a double-count — draw the rectangles and the signs are forced.
- **Memorize the query as `bottom-right − top − left + corner`.** The sign pattern `+ − − +` is the 2D analogue of `pre[r+1] − pre[l]`; in 3D it becomes 8 terms with alternating signs (the general N-D inclusion-exclusion).
- **Row-0 and col-0 of `pre` stay all-zero** for the same reason `pre[0]=0` in 1D — it kills the edge cases where the query touches the top row or left column.
`─────────────────────────────────────────────────`

---

## 3. Prefix Sum + Hash Map

### The Core Trick

To count subarrays with sum exactly `k`:

```
If pre[j] - pre[i] = k, then subarray a[i..j-1] has sum k.
So for each j, we need: how many earlier indices i have pre[i] = pre[j] - k?
```

Store prefix sum frequencies in a hash map as you iterate!

### Visual Trace

```
Array:  [1, 2, 3, -2, 5]    k = 3

Index:   0  1  2   3  4
pre:  [0, 1, 3, 6,  4, 9]

j=0: current_sum=0. Initialize count={0: 1}
After a[0]=1: current_sum=1, need 1-3=-2, count[-2]=0. count={0:1, 1:1}
After a[1]=2: current_sum=3, need 3-3=0,  count[0]=1 → +1. count={0:1, 1:1, 3:1}
After a[2]=3: current_sum=6, need 6-3=3,  count[3]=1 → +1. count={0:1, 1:1, 3:1, 6:1}
After a[3]=-2: current_sum=4, need 4-3=1, count[1]=1 → +1. count={0:1, 1:1, 3:1, 6:1, 4:1}
After a[4]=5: current_sum=9, need 9-3=6,  count[6]=1 → +1. count={..., 9:1}

Total = 4 subarrays with sum 3: [1,2], [3], [2,3,-2], [-2,5]  ✓
```

### Implementation

```python
from collections import defaultdict

def subarray_sum_count(a, k):
    """Count subarrays with sum exactly k."""
    count = defaultdict(int)
    count[0] = 1  # empty prefix
    current_sum = 0
    result = 0

    for x in a:
        current_sum += x
        # How many prefixes had sum = current_sum - k?
        result += count[current_sum - k]
        count[current_sum] += 1

    return result
```

### Variation: Longest Subarray with Sum k

```python
def longest_subarray_sum_k(a, k):
    """Find length of longest subarray with sum k."""
    first_occurrence = {0: -1}  # prefix_sum -> earliest index
    current_sum = 0
    best = 0

    for i, x in enumerate(a):
        current_sum += x
        if current_sum - k in first_occurrence:
            best = max(best, i - first_occurrence[current_sum - k])
        # Only store first occurrence (we want longest)
        if current_sum not in first_occurrence:
            first_occurrence[current_sum] = i

    return best
```

### Variation: Count Subarrays with Sum in Range [lo, hi]

```python
def count_sum_in_range(a, lo, hi):
    """Count subarrays with sum in [lo, hi]. Assumes non-negative values."""
    # count(sum <= hi) - count(sum <= lo - 1)
    return _count_at_most(a, hi) - _count_at_most(a, lo - 1)

def _count_at_most(a, target):
    """Count subarrays with sum <= target (non-negative array).

    Sliding window: since all values >= 0, the window sum is monotonic,
    so we shrink from the left whenever it exceeds target. Every valid
    subarray ending at `right` has length (right - left + 1).
    """
    if target < 0:
        return 0
    total = 0
    left = 0
    window = 0
    for right, x in enumerate(a):
        window += x
        while window > target:
            window -= a[left]
            left += 1
        total += right - left + 1
    return total
```

> **Negatives break the window.** With negative values the running sum is no
> longer monotonic, so shrinking from the left is invalid. Use a balanced BST /
> Fenwick tree over prefix sums (count prefixes in a value range) instead —
> see the [Fenwick Tree guide](/pattern/fenwick-tree).

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Count subarrays with sum k | O(N) | O(N) |
| Longest subarray with sum k | O(N) | O(N) |

### Why This Is So Powerful

The hash map transforms the "check all pairs (i, j)" approach from O(N²) to O(N). The key insight: **you don't need to enumerate pairs — you just need to count how many earlier prefixes had the right value.**

### Walkthrough — LC 560: Subarray Sum Equals K

> **Statement.** Given an integer array `nums` and an integer `k`, return the total **number** of contiguous subarrays whose sum equals `k`. Values may be negative, so a sliding window does NOT work.

**This template solves: LC 560, 974 (divisible-by-k twin), 523 (continuous subarray sum), 1248 (nice subarrays — count odds as +1).**

Why not sliding window? Because negatives break monotonicity — growing the window can *decrease* the sum, so you can't decide when to shrink. The prefix + hash map trick sidesteps ordering entirely: it counts, for each right endpoint, how many left endpoints complete a range summing to `k`.

```python
from collections import defaultdict

def subarraySum(nums, k):
    count = defaultdict(int)
    count[0] = 1                 # empty prefix — enables subarrays starting at index 0
    cur = 0
    res = 0
    for x in nums:
        cur += x
        res += count[cur - k]    # earlier prefixes p with cur - p == k
        count[cur] += 1
    return res
```

**Executed trace** on `nums = [1, 1, 1]`, `k = 2`:

```
count = {0:1}, cur=0, res=0

x=1: cur=1. need cur-k = 1-2 = -1 → count[-1]=0. res=0. count={0:1, 1:1}
x=1: cur=2. need 2-2 = 0 → count[0]=1.  res=1. count={0:1, 1:1, 2:1}
x=1: cur=3. need 3-2 = 1 → count[1]=1.  res=2. count={0:1, 1:1, 2:1, 3:1}

Answer = 2  ✓   (subarrays [1,1] at indices 0-1 and 1-2)
```

`★ Insight ─────────────────────────────────────`
- **The hash-map version never materializes the prefix array** — it streams one running sum and a frequency map. This is the mental unlock: "count subarrays with sum = k" is really "for each prefix, how many earlier prefixes sit exactly `k` below me."
- **`res += count[cur-k]` must come BEFORE `count[cur] += 1`.** Recording the current prefix first would let a zero-length subarray (or `k=0` self-match) sneak in. Query the past, then add yourself to it.
- **This is the O(N) escape from the O(N²) pair scan** — and the same skeleton reappears in §4 (swap `cur` for `cur % k`) and §7 (swap `+` for `^`). Learn it once, reuse it three times.
`─────────────────────────────────────────────────`

---

## 4. Prefix Sum + Modular Arithmetic

### The Idea

To count subarrays whose sum is **divisible by k**:

```
sum(l, r) % k == 0
⟺ (pre[r+1] - pre[l]) % k == 0
⟺ pre[r+1] % k == pre[l] % k
```

So we just count **pairs of equal remainders** in the prefix sum array!

### Visual Trace

```
Array:  [4, 5, 0, -2, -3, 1]    k = 5

Index:        0   1  2   3   4  5
prefix sums: [0,  4, 9,  9,  7, 4, 5]
      mod 5: [0,  4, 4,  4,  2, 4, 0]

Group by remainder:
  0: indices {0, 6} → C(2,2) = 1 pair  → subarrays with sum divisible by 5
  4: indices {1, 2, 3, 5} → C(4,2) = 6 pairs
  2: indices {4} → C(1,2) = 0 pairs

Total = 1 + 6 + 0 = 7  ✓
```

### Implementation

```python
def subarrays_divisible_by_k(a, k):
    """Count subarrays with sum divisible by k."""
    count = [0] * k
    count[0] = 1  # empty prefix has sum 0, remainder 0
    current_sum = 0
    result = 0

    for x in a:
        current_sum += x
        rem = current_sum % k
        # In Python, % always returns non-negative for positive k
        result += count[rem]
        count[rem] += 1

    return result
```

### ⚠️ Watch Out: Negative Remainders

In C++/Java, `-7 % 5 = -2`. You need `((x % k) + k) % k` to get a non-negative remainder. **Python handles this correctly** — `(-7) % 5 = 3`.

### Variation: Subarrays Divisible by k with Exactly m Elements

Combine the modular prefix sum with a sliding window or deque to add the length constraint.

### Classic Problems

1. **Subarray Divisibility (CSES)** — Direct application
2. **LeetCode 974: Subarray Sums Divisible by K** — Same pattern
3. **LeetCode 523: Continuous Subarray Sum** — Divisible by k with length ≥ 2

### Walkthrough — LC 974: Subarray Sums Divisible by K

> **Statement.** Given an integer array `nums` and an integer `k`, return the number of contiguous subarrays whose sum is **divisible by k**. Values may be negative.

**This template solves: LC 974, 523 (needs length ≥ 2), and the CSES "Subarray Divisibility".**

The reframe: `sum(l,r) % k == 0` ⟺ `pre[r+1] % k == pre[l] % k`. So a subarray is divisible iff its two endpoint-prefixes share the **same remainder**. Count subarrays = count pairs of equal remainders. The hash map from §3 shrinks to a fixed array of size `k`.

```python
def subarraysDivByK(nums, k):
    count = [0] * k
    count[0] = 1                 # empty prefix has remainder 0
    cur = 0
    res = 0
    for x in nums:
        cur = (cur + x) % k      # Python's % is always non-negative for positive k
        res += count[cur]        # earlier prefixes with the SAME remainder
        count[cur] += 1
    return res
```

**Executed trace** on `nums = [4, 5, 0, -2, -3, 1]`, `k = 5`:

```
count[0..4] = [1,0,0,0,0], cur=0, res=0

x= 4: cur=(0+4)%5=4. count[4]=0 → res=0. count=[1,0,0,0,1]
x= 5: cur=(4+5)%5=4. count[4]=1 → res=1. count=[1,0,0,0,2]
x= 0: cur=(4+0)%5=4. count[4]=2 → res=3. count=[1,0,0,0,3]
x=-2: cur=(4-2)%5=2. count[2]=0 → res=3. count=[1,0,1,0,3]
x=-3: cur=(2-3)%5=4. count[4]=3 → res=6. count=[1,0,1,0,4]   (Python: -1%5 = 4)
x= 1: cur=(4+1)%5=0. count[0]=1 → res=7. count=[2,0,1,0,4]

Answer = 7  ✓
```

`★ Insight ─────────────────────────────────────`
- **"Divisible" turns sum-equality into remainder-equality.** Instead of asking "which earlier prefix equals `cur - k`" (§3), you ask "which earlier prefixes share my remainder" — a strictly stronger grouping that collapses the hash map into a length-`k` array.
- **The negative-modulo trap.** Python guarantees `(-1) % 5 == 4`, so the code above is safe. In C++/Java `-1 % 5 == -1`, which would index out of bounds or miscount — there you must write `((cur % k) + k) % k`. The trace's `x=-3` step (`-1 % 5 → 4`) is exactly where a C++ port silently breaks.
- **LC 523 is the same code with one twist:** it wants a subarray of length ≥ 2, so you store the *first index* each remainder appears (like §3's longest-subarray variant) and check the gap, rather than counting all pairs.
`─────────────────────────────────────────────────`

---

## 5. Difference Array (1D)

### The Idea

The **difference array** is the **inverse** of prefix sum. If prefix sum turns "point values" into "cumulative sums," then the difference array turns "range updates" into "point updates."

```
Prefix sum:     point values  →  range queries (O(1))
Difference:     range updates →  point updates (O(1))
```

Given an array `a`, its difference array is:

```
d[0] = a[0]
d[i] = a[i] - a[i-1]   for i ≥ 1
```

To **add value v to all elements in a[l..r]**:

```
d[l] += v
d[r+1] -= v
```

Then reconstruct `a` by taking prefix sums of `d`.

### Visual Trace

```
Initial: a = [0, 0, 0, 0, 0, 0]   (6 elements)

Operation 1: add 3 to a[1..4]
  d[1] += 3, d[5] -= 3
  d = [0, 3, 0, 0, 0, -3]
  a = [0, 3, 3, 3, 3, 0]  ✓

Operation 2: add 2 to a[0..2]
  d[0] += 2, d[3] -= 2
  d = [2, 3, 0, -2, 0, -3]
  a = [2, 5, 5, 3, 3, 0]  ✓

Operation 3: add -1 to a[2..5]
  d[2] += -1, d[6] -= -1  (d[6] is out of bounds, ignore or use n+1 array)
  d = [2, 3, -1, -2, 0, -3]
  a = [2, 5, 4, 2, 2, -1]  ✓

Reconstruction: prefix sum of d
  a[0] = 2
  a[1] = 2 + 3 = 5
  a[2] = 5 + (-1) = 4
  a[3] = 4 + (-2) = 2
  a[4] = 2 + 0 = 2
  a[5] = 2 + (-3) = -1  ✓
```

### Implementation

```python
def range_add(diff, l, r, v):
    """Add v to all elements in [l, r] inclusive."""
    diff[l] += v
    if r + 1 < len(diff):
        diff[r + 1] -= v

def reconstruct(diff):
    """Convert difference array back to original array."""
    a = [0] * len(diff)
    a[0] = diff[0]
    for i in range(1, len(diff)):
        a[i] = a[i - 1] + diff[i]
    return a

# Usage
n = 6
diff = [0] * n
range_add(diff, 1, 4, 3)    # add 3 to [1..4]
range_add(diff, 0, 2, 2)    # add 2 to [0..2]
range_add(diff, 2, 5, -1)   # add -1 to [2..5]
result = reconstruct(diff)   # [2, 5, 4, 2, 2, -1]
```

### Complexity

| Operation | Time |
|-----------|------|
| Single range update | O(1) |
| Q range updates + reconstruct | O(Q + N) |

### When to Use

- Many range updates, single final query
- "Sweep line" style problems (event start/end)
- Bus schedule problems (passengers boarding/exiting at stops)

### Classic Problems

1. **Range Update Queries (CSES)** — Direct application
2. **Corporate Flight Bookings (LC 1109)** — Range add, then prefix sum
3. **Car Pooling (LC 1094)** — Difference array on timeline

### Walkthrough — LC 1109: Corporate Flight Bookings

> **Statement.** There are `n` flights labeled `1..n`. You're given `bookings` where `bookings[i] = [first, last, seats]` means `seats` seats were booked on **every** flight from `first` to `last` inclusive. Return an array `answer` of length `n` where `answer[i]` is the total seats booked on flight `i+1`.

**This template solves: LC 1109, 1094 (Car Pooling), 370 (Range Addition), and CSES "Range Update Queries".**

The signal is "**apply many range-adds, then read the whole array once**." Applying each booking directly is O(range) → O(n·bookings). The difference array makes each booking O(1): mark a `+seats` where the range starts and a `−seats` just past where it ends, then one prefix-sum sweep reconstructs every flight's total.

```python
def corpFlightBookings(bookings, n):
    diff = [0] * (n + 2)         # 1-indexed flights; +2 guards the r+1 write
    for first, last, seats in bookings:
        diff[first] += seats     # start adding here
        diff[last + 1] -= seats  # stop adding after `last`
    res = [0] * n
    cur = 0
    for i in range(1, n + 1):    # prefix sum of diff = actual per-flight totals
        cur += diff[i]
        res[i - 1] = cur
    return res
```

**Executed trace** on `bookings = [[1,2,10],[2,3,20],[2,5,25]]`, `n = 5`:

```
Apply deltas (index 1..6):
  [1,2,10]: diff[1]+=10, diff[3]-=10
  [2,3,20]: diff[2]+=20, diff[4]-=20
  [2,5,25]: diff[2]+=25, diff[6]-=25

diff (idx 1..6):  10   45  -10  -20    0  -25
                   ^    ^
                flight1  flight2 got +20+25=45

Prefix-sum sweep:
  flight1: cur=0+10        = 10
  flight2: cur=10+45       = 55
  flight3: cur=55-10       = 45
  flight4: cur=45-20       = 25
  flight5: cur=25+0        = 25

answer = [10, 55, 45, 25, 25]  ✓
```

`★ Insight ─────────────────────────────────────`
- **Difference array is prefix sum run backwards.** Prefix sum turns point values into range sums; the difference array turns range *updates* into two point writes, and a final prefix-sum sweep turns them back into point values. They are inverse operations — that's why the reconstruction is literally a prefix sum.
- **`diff[last+1] -= seats` is the "stop" marker.** The `+seats` at `first` leaks rightward forever under prefix sum; the `−seats` at `last+1` cancels it exactly past the range. Sizing the array `n+2` guarantees that write is in-bounds even when `last == n`.
- **O(1) per update is the whole win.** B bookings cost O(B) to record and O(n) to reconstruct — O(B+n) total instead of O(B·n). Whenever you see "add X to a range" repeated many times with a single final read, reach for this.
`─────────────────────────────────────────────────`

---

## 6. Difference Array (2D)

### The Idea

Extend the 1D difference trick to 2D. To add value `v` to all cells in rectangle `(r1, c1)` to `(r2, c2)`:

```
d[r1][c1]     += v
d[r1][c2+1]   -= v
d[r2+1][c1]   -= v
d[r2+1][c2+1] += v
```

Then reconstruct with a **2D prefix sum** over `d`.

### Visual — Why 4 Points?

```
Adding v to the shaded rectangle:

    c1        c2
     +v ...   -v
r1 > ########
     ########
r2 > ########
     -v ...   +v

The +v at (r1,c1) "starts" the addition.
The -v at (r1,c2+1) stops it from spreading right.
The -v at (r2+1,c1) stops it from spreading down.
The +v at (r2+1,c2+1) corrects the double-subtraction at the corner.
```

### Implementation

```python
def range_add_2d(diff, r1, c1, r2, c2, v):
    """Add v to all cells in rectangle (r1,c1)-(r2,c2) inclusive."""
    diff[r1][c1] += v
    if c2 + 1 < len(diff[0]):
        diff[r1][c2 + 1] -= v
    if r2 + 1 < len(diff):
        diff[r2 + 1][c1] -= v
    if r2 + 1 < len(diff) and c2 + 1 < len(diff[0]):
        diff[r2 + 1][c2 + 1] += v

def reconstruct_2d(diff):
    """Convert 2D difference array to original grid."""
    R, C = len(diff), len(diff[0])
    # Row-wise prefix sum
    for i in range(R):
        for j in range(1, C):
            diff[i][j] += diff[i][j - 1]
    # Column-wise prefix sum
    for j in range(C):
        for i in range(1, R):
            diff[i][j] += diff[i - 1][j]
    return diff
```

### Complexity

| Operation | Time |
|-----------|------|
| Single rectangle update | O(1) |
| Q updates + reconstruct | O(Q + R × C) |

### Classic Problems

1. **Forest Queries** variant — Stamp rectangles, then count
2. **2D range increment** — Multiple rectangle operations

---

## 7. Prefix XOR

### The Idea

XOR has the beautiful property that `a ^ a = 0`. So prefix XOR works exactly like prefix sum:

```
pre_xor[0] = 0
pre_xor[i] = a[0] ^ a[1] ^ ... ^ a[i-1]

XOR(l, r) = pre_xor[r+1] ^ pre_xor[l]
```

This works because the common prefix `a[0] ^ ... ^ a[l-1]` cancels out.

### Visual Trace

```
Array:  [3, 1, 5, 2, 4]

Binary:  011  001  101  010  100

Prefix XOR: [000, 011, 010, 111, 101, 001]
             0    3    2    7    5    1

Query: XOR(1, 3) = pre[4] ^ pre[1] = 5 ^ 3 = 101 ^ 011 = 110 = 6
Check: 1 ^ 5 ^ 2 = 001 ^ 101 ^ 010 = 110 = 6  ✓
```

### Implementation

```python
def build_prefix_xor(a):
    n = len(a)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] ^ a[i]
    return pre

def range_xor(pre, l, r):
    """XOR of a[l..r] inclusive."""
    return pre[r + 1] ^ pre[l]
```

### Pattern: Count Subarrays with XOR = k

Same hash map trick as sum = k:

```python
from collections import defaultdict

def count_subarrays_xor_k(a, k):
    """Count subarrays with XOR equal to k."""
    count = defaultdict(int)
    count[0] = 1
    current_xor = 0
    result = 0

    for x in a:
        current_xor ^= x
        # pre[j] ^ pre[i] = k  ⟺  pre[i] = pre[j] ^ k
        result += count[current_xor ^ k]
        count[current_xor] += 1

    return result
```

### Why `current_xor ^ k` Instead of `current_xor - k`?

For sums: `pre[j] - pre[i] = k → pre[i] = pre[j] - k`
For XOR: `pre[j] ^ pre[i] = k → pre[i] = pre[j] ^ k`

XOR is its own inverse! `x ^ k = y ⟺ x = y ^ k`.

### Classic Problems

1. **Range Xor Queries (CSES)** — Direct application
2. **LeetCode 1442: Subarray XOR Triplets** — Count (i,j,k) with XOR splits
3. **Maximum XOR subarray** — Combine with trie

### Walkthrough — LC 1310: XOR Queries of a Subarray

> **Statement.** Given `arr` and a list of `queries` where `queries[i] = [l, r]`, return an array whose `i`-th element is `arr[l] ^ arr[l+1] ^ ... ^ arr[r]` (XOR of the subarray). Many queries, array static.

**This template solves: LC 1310, the CSES "Range Xor Queries", and it's the building block for LC 1442 (count XOR triplets).**

XOR is invertible — it's *its own* inverse (`x ^ x = 0`). So the entire §1 machinery transplants directly: build a prefix-XOR array, and every range is the XOR of two endpoints. The shared prefix `arr[0]^...^arr[l-1]` cancels itself out.

```python
def xorQueries(arr, queries):
    pre = [0]                    # pre[i] = XOR of first i elements
    for x in arr:
        pre.append(pre[-1] ^ x)
    return [pre[r + 1] ^ pre[l] for l, r in queries]
```

**Executed trace** on `arr = [1, 3, 4, 8]`, `queries = [[0,1],[1,2],[0,3],[3,3]]`:

```
arr:        1    3    4    8
pre:  [0,   1,   2,   6,  14]
       ^    ^    ^    ^    ^
       0  0^1  1^3  2^4  6^8

[0,1]: pre[2] ^ pre[0] = 2  ^ 0 = 2    (1^3       = 2)  ✓
[1,2]: pre[3] ^ pre[1] = 6  ^ 1 = 7    (3^4       = 7)  ✓
[0,3]: pre[4] ^ pre[0] = 14 ^ 0 = 14   (1^3^4^8   = 14) ✓
[3,3]: pre[4] ^ pre[3] = 14 ^ 6 = 8    (8         = 8)  ✓

answer = [2, 7, 14, 8]  ✓
```

`★ Insight ─────────────────────────────────────`
- **Prefix sum and prefix XOR are the same template with the operator swapped.** Sum's inverse is subtraction (`pre[r+1] - pre[l]`); XOR's inverse is XOR itself (`pre[r+1] ^ pre[l]`). Any *associative, invertible* operation with an identity element (0 for both +and ^) drops straight into this shape.
- **Why the cancellation works:** `pre[r+1] ^ pre[l]` = `(a₀^…^a_r) ^ (a₀^…^a_{l-1})`. Every term with index `< l` appears twice and vanishes (`x^x=0`), leaving exactly `a_l^…^a_r`. Subtraction cancels the same prefix for sums.
- **"Count subarrays with XOR = k" reuses §3 verbatim** — swap `count[cur-k]` for `count[cur ^ k]`, because `pre[j] ^ pre[i] = k ⟺ pre[i] = pre[j] ^ k`. The hash-map counting trick is operator-agnostic.
`─────────────────────────────────────────────────`

---

## 8. Prefix & Suffix Products

### The Idea

Sometimes you need products instead of sums. The classic problem: **Product of Array Except Self** — compute an array where `result[i]` = product of all elements except `a[i]`, without division.

### Solution: Left and Right Products

```
left[i]  = a[0] × a[1] × ... × a[i-1]    (prefix product)
right[i] = a[i+1] × a[i+2] × ... × a[n-1] (suffix product)
result[i] = left[i] × right[i]
```

### Visual Trace

```
Array:   [1, 2, 3, 4]

Left:    [1, 1, 2, 6]
          ^  ^  ^  ^
          |  |  |  1×2×3
          |  |  1×2
          |  1
          empty product

Right:   [24, 12, 4, 1]
           ^   ^  ^  ^
           |   |  |  empty product
           |   |  4
           |   3×4
           2×3×4

Result:  [24, 12, 8, 6]
          1×24  1×12  2×4  6×1  ✓
```

### Implementation (O(1) Extra Space)

```python
def product_except_self(a):
    n = len(a)
    result = [1] * n

    # Left pass: result[i] = product of a[0..i-1]
    left = 1
    for i in range(n):
        result[i] = left
        left *= a[i]

    # Right pass: multiply by product of a[i+1..n-1]
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= a[i]

    return result
```

### Generalization: Prefix + Suffix for Any Associative Operation

This pattern works for any operation where you can combine left and right parts:
- **Sum except self**: `total_sum - a[i]`
- **Min except self**: `min(prefix_min[i-1], suffix_min[i+1])`
- **GCD except self**: `gcd(prefix_gcd[i-1], suffix_gcd[i+1])`

```python
from math import gcd
from functools import reduce

def gcd_except_self(a):
    n = len(a)
    prefix_gcd = [0] * n
    suffix_gcd = [0] * n

    prefix_gcd[0] = a[0]
    for i in range(1, n):
        prefix_gcd[i] = gcd(prefix_gcd[i-1], a[i])

    suffix_gcd[n-1] = a[n-1]
    for i in range(n-2, -1, -1):
        suffix_gcd[i] = gcd(a[i], suffix_gcd[i+1])

    result = [0] * n
    for i in range(n):
        # Use None (not 0) as "no neighbor" — a real element can be 0,
        # and gcd(0, x) == x would silently corrupt the answer.
        left = prefix_gcd[i-1] if i > 0 else None
        right = suffix_gcd[i+1] if i < n-1 else None
        if left is None:
            result[i] = right
        elif right is None:
            result[i] = left
        else:
            result[i] = gcd(left, right)
    return result
```

### Walkthrough — LC 238: Product of Array Except Self

> **Statement.** Given an integer array `nums`, return `answer` where `answer[i]` = product of all elements **except** `nums[i]`. You must NOT use division, and it should run in O(N). (Follow-up: O(1) extra space beyond the output.)

**This template solves: LC 238, 1013 (partition into equal-sum — prefix/suffix balance), and the general "aggregate of all-but-one" family (sum/min/gcd except self).**

Division would be trivial (`total / nums[i]`) but breaks on a zero. The prefix/suffix idea: `answer[i]` = (product of everything left of `i`) × (product of everything right of `i`). Compute the left products in a forward pass, then fold the right products in a backward pass — reusing the output array so no extra prefix/suffix arrays are needed.

```python
def productExceptSelf(nums):
    n = len(nums)
    res = [1] * n

    left = 1                      # product of nums[0..i-1]
    for i in range(n):
        res[i] = left             # store prefix product BEFORE multiplying in nums[i]
        left *= nums[i]

    right = 1                     # product of nums[i+1..n-1]
    for i in range(n - 1, -1, -1):
        res[i] *= right           # fold in the suffix product
        right *= nums[i]

    return res
```

**Executed trace** on `nums = [1, 2, 3, 4]`:

```
Left pass (res[i] = product of everything before i):
  i=0: res[0]=1;          left=1*1=1
  i=1: res[1]=1;          left=1*2=2
  i=2: res[2]=2;          left=2*3=6
  i=3: res[3]=6;          left=6*4=24
  res = [1, 1, 2, 6]

Right pass (multiply in product of everything after i):
  i=3: res[3]=6*1=6;      right=1*4=4
  i=2: res[2]=2*4=8;      right=4*3=12
  i=1: res[1]=1*12=12;    right=12*2=24
  i=0: res[0]=1*24=24;    right=24*1=24
  res = [24, 12, 8, 6]  ✓
```

`★ Insight ─────────────────────────────────────`
- **Prefix alone can't answer "except self" — you need the mirror.** For a range you difference *one* prefix array; for "everything but position i" you multiply a prefix (left) by a suffix (right). This left×right structure generalizes: sum-except-self = `prefixSum[i-1] + suffixSum[i+1]`, min-except-self = `min(prefixMin, suffixMin)`.
- **The O(1)-space trick is ordering.** Store left-products into the output first, then walk backward accumulating right-products *in a scalar* and multiplying in place. No second array — the output doubles as scratch.
- **Handles zeros for free.** Executed on `[-1,1,0,-3,3]` it returns `[0,0,9,0,0]` — the only nonzero answer is at the single zero's position. Division-based code would divide by zero; prefix/suffix never divides, so zeros are just ordinary factors. That immunity is the whole reason the problem forbids division.
`─────────────────────────────────────────────────`

---

## 9. Prefix Sum on Trees

### The Idea

On trees, we can use prefix sums along root-to-node paths to answer path queries. Two main approaches:

### Approach 1: Euler Tour + Range Prefix Sum

Flatten the tree with Euler tour, then use 1D prefix sums for **subtree** queries.

```
Tree:        0
            / \
           1   2
          / \
         3   4

DFS visit order: 0, 1, 3, 4, 2

Assign tin on enter, tout = last tin used inside the subtree:

  node:   0    1    2    3    4
  tin:    0    1    4    2    3
  tout:   4    3    4    2    3

Subtree of v = the contiguous index range [tin[v], tout[v]].
  Subtree of 1 = [tin[1], tout[1]] = [1, 3]
               = euler indices {1, 2, 3}
               = nodes {1, 3, 4}   ✓  (node 1 and its descendants)

A subtree query then becomes a range prefix-sum query over [tin[v], tout[v]].
```

### Approach 2: Path Prefix Sum with LCA

For path queries `u → v` through LCA:

```
sum(u, v) = sum(root, u) + sum(root, v) - 2 × sum(root, LCA(u,v)) + val[LCA(u,v)]
```

### Approach 3: Difference on Tree (Edge/Node Counting)

To increment all nodes on path `u → v`:

```
diff[u] += 1
diff[v] += 1
diff[LCA(u,v)] -= 1
diff[parent[LCA(u,v)]] -= 1
```

Then DFS to accumulate from leaves to root (subtree sum = answer for each node).

### Implementation — Path Sum with DFS Prefix

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)

def solve_path_queries(n, edges, values, queries):
    """
    Given a tree with node values, answer:
    "What is the sum of values on path u → v?"
    Using depth prefix sums + LCA.
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Precompute depth_sum[v] = sum of values from root to v
    LOG = 20
    depth = [0] * n
    depth_sum = [0] * n
    parent = [[-1] * n for _ in range(LOG)]

    # BFS to set up parent, depth, depth_sum
    from collections import deque
    visited = [False] * n
    queue = deque([0])
    visited[0] = True
    depth_sum[0] = values[0]

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[0][v] = u
                depth[v] = depth[u] + 1
                depth_sum[v] = depth_sum[u] + values[v]
                queue.append(v)

    # Build binary lifting table
    for k in range(1, LOG):
        for v in range(n):
            if parent[k-1][v] != -1:
                parent[k][v] = parent[k-1][parent[k-1][v]]

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        for k in range(LOG):
            if (diff >> k) & 1:
                u = parent[k][u]
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if parent[k][u] != parent[k][v]:
                u = parent[k][u]
                v = parent[k][v]
        return parent[0][u]

    results = []
    for u, v in queries:
        l = lca(u, v)
        # path sum = depth_sum[u] + depth_sum[v] - 2*depth_sum[l] + values[l]
        ans = depth_sum[u] + depth_sum[v] - 2 * depth_sum[l] + values[l]
        results.append(ans)
    return results
```

### Implementation — Difference on Tree (Counting Paths)

```python
def count_paths_through_nodes(n, adj, paths):
    """
    Given paths [(u, v), ...], count how many paths pass through each node.
    Uses difference on tree technique.
    """
    # Setup LCA (assume already built as above)
    # ...

    diff = [0] * n
    for u, v in paths:
        l = lca(u, v)
        diff[u] += 1
        diff[v] += 1
        diff[l] -= 1
        p = parent[0][l]
        if p != -1:
            diff[p] -= 1

    # DFS to accumulate subtree sums
    answer = [0] * n
    def dfs(u, par):
        answer[u] = diff[u]
        for v in adj[u]:
            if v != par:
                dfs(v, u)
                answer[u] += answer[v]

    dfs(0, -1)
    return answer
```

### Classic Problems

1. **Path Queries (CSES)** — Sum on root-to-node paths
2. **Counting Paths (CSES)** — Difference on tree
3. **Distance Queries (CSES)** — Path length using LCA + depth

---

## 10. Prefix Sum + Binary Search

### The Idea

When the array has **non-negative** values, prefix sums are **monotonically non-decreasing**. This means you can binary search on them!

### Pattern: Smallest Subarray with Sum ≥ Target

```python
from bisect import bisect_left

def min_subarray_with_sum_at_least(a, target):
    """
    Find shortest subarray with sum ≥ target.
    Assumes all elements non-negative.
    """
    n = len(a)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]

    best = float('inf')
    for j in range(1, n + 1):
        # Need pre[j] - pre[i] ≥ target → pre[i] ≤ pre[j] - target
        # Find rightmost i with pre[i] ≤ pre[j] - target
        # Since pre is sorted (non-negative elements), use bisect
        threshold = pre[j] - target
        i = bisect_left(pre, threshold + 1, 0, j) - 1
        if i >= 0 and pre[j] - pre[i] >= target:
            best = min(best, j - i)

    return best if best != float('inf') else -1
```

### Pattern: Count Subarrays with Sum in [lo, hi] (Non-Negative)

```python
from bisect import bisect_left, bisect_right

def count_subarrays_sum_in_range(a, lo, hi):
    """
    Count subarrays with sum in [lo, hi].
    Assumes all elements non-negative (prefix sums are sorted).
    """
    n = len(a)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]

    count = 0
    for j in range(1, n + 1):
        # Need lo ≤ pre[j] - pre[i] ≤ hi
        # → pre[j] - hi ≤ pre[i] ≤ pre[j] - lo
        low_bound = pre[j] - hi
        high_bound = pre[j] - lo
        # Count i in [0, j) where low_bound ≤ pre[i] ≤ high_bound
        left = bisect_left(pre, low_bound, 0, j)
        right = bisect_right(pre, high_bound, 0, j)
        count += right - left

    return count
```

### When Negatives Exist: Use SortedList or BIT

If the array can have negative values, prefix sums aren't sorted. Use a **balanced BST** (like `SortedList` from `sortedcontainers`) or a **BIT/Fenwick tree** with coordinate compression.

```python
from sortedcontainers import SortedList

def count_subarrays_sum_in_range_general(a, lo, hi):
    """Works even with negative values."""
    sl = SortedList([0])  # prefix sums seen so far
    current_sum = 0
    count = 0

    for x in a:
        current_sum += x
        # Count previous prefix sums in [current_sum - hi, current_sum - lo]
        left = sl.bisect_left(current_sum - hi)
        right = sl.bisect_right(current_sum - lo)
        count += right - left
        sl.add(current_sum)

    return count
```

### Complexity

| Approach | Time | When |
|----------|------|------|
| Binary search on sorted prefix | O(N log N) | Non-negative arrays |
| SortedList | O(N log N) | Any array |
| BIT + coordinate compression | O(N log N) | Any array |

### Walkthrough — LC 327: Count of Range Sum

> **Statement.** Given an integer array `nums` and two integers `lower` and `upper`, return the number of range sums `sum(i, j)` that lie in `[lower, upper]` inclusive (`i ≤ j`). Values may be negative. `N` up to ~10⁵, so O(N²) is too slow.

**This template solves: LC 327, 315 (count smaller after self), 493 (reverse pairs) — the "count prefixes in a value range" family.**

`sum(i,j) = pre[j+1] - pre[i]` lies in `[lower, upper]` ⟺ `pre[i] ∈ [pre[j+1] - upper, pre[j+1] - lower]`. So as you build prefixes left to right, for each new prefix you count how many **earlier** prefixes fall in that window. With negatives the prefix array isn't sorted, so a plain binary search fails — keep the seen prefixes in an **order-statistic structure** (`SortedList`) that supports range-count in O(log N).

```python
from sortedcontainers import SortedList

def countRangeSum(nums, lower, upper):
    sl = SortedList([0])          # prefix sums seen so far; seed with empty prefix 0
    cur = 0
    cnt = 0
    for x in nums:
        cur += x
        # earlier prefixes p with  cur - upper <= p <= cur - lower
        cnt += sl.bisect_right(cur - lower) - sl.bisect_left(cur - upper)
        sl.add(cur)
    return cnt
```

**Executed trace** on `nums = [-2, 5, -1]`, `lower = -2`, `upper = 2`:

```
sl = [0], cur=0, cnt=0

x=-2: cur=-2. window p in [cur-upper, cur-lower] = [-4, 0].
      sl=[0]: prefixes in [-4,0] → just {0}. cnt += 1 → cnt=1.  add -2 → sl=[-2,0]
x= 5: cur= 3. window [3-2, 3+2] = [1, 5].
      sl=[-2,0]: none in [1,5]. cnt += 0 → cnt=1.  add 3 → sl=[-2,0,3]
x=-1: cur= 2. window [0, 4].
      sl=[-2,0,3]: {0, 3} in [0,4]. cnt += 2 → cnt=3.  add 2

Answer = 3  ✓   (ranges [0,0]=-2, [2,2]=-1, [0,2]=2 all in [-2,2])
```

`★ Insight ─────────────────────────────────────`
- **Negatives are the whole reason this is Hard.** With non-negative values the prefix array is sorted and plain `bisect` on a list suffices (§10's earlier `count_subarrays_sum_in_range`). Negatives destroy the sorted order, forcing a structure that stays sorted under insertion — `SortedList`, a BIT with coordinate compression, or merge-sort-with-counting.
- **The query is still the §3 idea, just made ordered.** §3 asks "how many earlier prefixes *equal* `cur-k`" (a hash map lookup). Here we ask "how many earlier prefixes fall in a *range*" — the same "look back at prefixes" move, upgraded from point-equality to range-count, so the data structure upgrades from hash map to ordered multiset.
- **Seed with `0` for the same reason as `count[0]=1`.** The empty prefix must be present before the loop so ranges starting at index 0 are counted (the trace's first step relies on `0` already being in `sl`).
`─────────────────────────────────────────────────`

---

## 11. Higher-Dimensional Prefix Sums

### Sum over Subsets (SOS) — Bitmask Prefix Sum

The **Sum over Subsets (SOS) DP** computes, for each bitmask `x`:

```
sos[x] = Σ f[y]  for all y that are submasks of x  (y & x == y)
```

This is essentially a prefix sum in each bit dimension.

### Why Is This a Prefix Sum?

Think of a bitmask as coordinates in a multi-dimensional binary space. Each bit is a dimension with values {0, 1}. SOS DP is the N-dimensional analogue of the 2D prefix sum!

```
2D: pre[i][j] = Σ grid[r][c] for r ≤ i, c ≤ j

Bitmask (3 bits = 3D):
sos[101] = f[000] + f[001] + f[100] + f[101]
         = sum over all submasks of 101
```

### SOS DP Implementation

```python
def sum_over_subsets(f, n_bits):
    """
    Compute sos[x] = sum of f[y] for all submasks y of x.
    n_bits: number of bits to consider.
    f: array of size 2^n_bits.
    """
    sos = f[:]  # copy
    for bit in range(n_bits):
        for mask in range(1 << n_bits):
            if mask & (1 << bit):
                sos[mask] += sos[mask ^ (1 << bit)]
    return sos
```

### Visual Trace (2 bits)

```
f = [f[00], f[01], f[10], f[11]] = [1, 2, 3, 4]

Process bit 0:
  mask=00: bit 0 not set, skip
  mask=01: bit 0 set → sos[01] += sos[00] → sos[01] = 2 + 1 = 3
  mask=10: bit 0 not set, skip
  mask=11: bit 0 set → sos[11] += sos[10] → sos[11] = 4 + 3 = 7

After bit 0: sos = [1, 3, 3, 7]

Process bit 1:
  mask=00: bit 1 not set, skip
  mask=01: bit 1 not set, skip
  mask=10: bit 1 set → sos[10] += sos[00] → sos[10] = 3 + 1 = 4
  mask=11: bit 1 set → sos[11] += sos[01] → sos[11] = 7 + 3 = 10

After bit 1: sos = [1, 3, 4, 10]

Verify: sos[11] = f[00] + f[01] + f[10] + f[11] = 1+2+3+4 = 10  ✓
        sos[10] = f[00] + f[10] = 1+3 = 4  ✓
        sos[01] = f[00] + f[01] = 1+2 = 3  ✓
```

### Inverse: Möbius Transform (Inclusion-Exclusion)

To undo SOS (get back from subset sums to original values):

```python
def mobius_inverse(sos, n_bits):
    """Inverse of sum_over_subsets."""
    f = sos[:]
    for bit in range(n_bits):
        for mask in range(1 << n_bits):
            if mask & (1 << bit):
                f[mask] -= f[mask ^ (1 << bit)]
    return f
```

### Sum over Supermasks

Sometimes you need `sos[x] = Σ f[y]` for all `y` that contain `x` as submask (`x & y == x`):

```python
def sum_over_supermasks(f, n_bits):
    sos = f[:]
    for bit in range(n_bits):
        for mask in range(1 << n_bits):
            if not (mask & (1 << bit)):  # bit NOT set
                sos[mask] += sos[mask | (1 << bit)]
    return sos
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| SOS DP | O(N × 2^N) | O(2^N) |

### Classic Problems

1. **SOS DP (CSES)** — Direct application
2. **Compatible pairs** — For each mask, count masks with no overlapping bits
3. **Maximum AND/OR pair** — Find pair with maximum bitwise AND

---

## 12. Common Patterns Collection

### Pattern A: Running Sum / Cumulative Sum

The simplest form — just accumulate as you go.

```python
# Balance never goes negative
def can_complete_circuit(gas, cost):
    """Circular gas station problem."""
    n = len(gas)
    total = 0
    tank = 0
    start = 0
    for i in range(n):
        diff = gas[i] - cost[i]
        total += diff
        tank += diff
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1
```

### Pattern B: Prefix Sum for Counting

Turn "count of X in range" into a prefix sum.

```python
def range_count_zeros(a):
    """Build prefix count of zeros for range queries."""
    n = len(a)
    count_zeros = [0] * (n + 1)
    for i in range(n):
        count_zeros[i + 1] = count_zeros[i] + (1 if a[i] == 0 else 0)

    # Zeros in a[l..r] = count_zeros[r+1] - count_zeros[l]
    return count_zeros
```

### Pattern C: Prefix Sum for String Problems

Count character frequencies in ranges.

```python
def build_char_prefix(s):
    """Build prefix frequency for each character."""
    n = len(s)
    pre = [[0] * 26 for _ in range(n + 1)]
    for i in range(n):
        for c in range(26):
            pre[i + 1][c] = pre[i][c]
        pre[i + 1][ord(s[i]) - ord('a')] += 1
    return pre

def count_char_in_range(pre, l, r, ch):
    """Count occurrences of ch in s[l..r]."""
    c = ord(ch) - ord('a')
    return pre[r + 1][c] - pre[l][c]
```

### Pattern D: Max/Min Prefix and Suffix

Track running maximum or minimum from both ends.

```python
def trapping_rain_water(height):
    """Classic problem: how much water can be trapped?"""
    n = len(height)
    if n == 0:
        return 0

    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])

    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])

    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    return water
```

### Pattern E: Sweep Line + Difference Array

Count overlapping intervals using difference array.

```python
def max_overlapping_intervals(intervals, max_val):
    """Find maximum number of overlapping intervals."""
    diff = [0] * (max_val + 2)
    for start, end in intervals:
        diff[start] += 1
        diff[end + 1] -= 1

    # Prefix sum = count of active intervals at each point
    max_overlap = 0
    current = 0
    for i in range(max_val + 1):
        current += diff[i]
        max_overlap = max(max_overlap, current)
    return max_overlap
```

### Pattern F: Prefix Sum + Two Pointers

For non-negative arrays, find subarrays with exact sum.

```python
def subarray_with_sum(a, target):
    """Find subarray with exact sum (non-negative elements)."""
    current = 0
    left = 0
    for right in range(len(a)):
        current += a[right]
        while current > target and left <= right:
            current -= a[left]
            left += 1
        if current == target:
            return (left, right)
    return None
```

---

## 13. Pattern Recognition Cheat Sheet

### Decision Flowchart

```
"I need to answer range queries..."
   │
   ├── Static array, sum/xor queries?
   │     → Prefix Sum / Prefix XOR — O(N) build, O(1) query
   │
   ├── Static 2D grid, rectangle queries?
   │     → 2D Prefix Sum — O(RC) build, O(1) query
   │
   ├── Many range updates, then read?
   │     → Difference Array — O(1) update, O(N) reconstruct
   │
   ├── Many 2D rectangle updates?
   │     → 2D Difference Array — O(1) update, O(RC) reconstruct
   │
   ├── Count subarrays with sum/xor = k?
   │     → Prefix Sum + Hash Map — O(N)
   │
   ├── Count subarrays divisible by k?
   │     → Prefix Sum mod k + Counting — O(N)
   │
   ├── Product except self?
   │     → Prefix + Suffix Products — O(N)
   │
   ├── Path queries on tree?
   │     → Prefix Sum on Tree + LCA — varies
   │
   ├── Non-negative array, subarray sum in range?
   │     → Prefix Sum + Binary Search — O(N log N)
   │
   └── Bitmask subset sums?
         → SOS DP — O(N × 2^N)
```

### Quick Reference Table

| Problem Type | Technique | Time | Key Insight |
|--------------|-----------|------|-------------|
| Range sum query | 1D prefix sum | O(1) | `pre[r+1] - pre[l]` |
| Rectangle sum | 2D prefix sum | O(1) | Inclusion-exclusion |
| # subarrays sum=k | Prefix + hash map | O(N) | Count `pre[j]-k` |
| # subarrays sum%k=0 | Prefix mod k | O(N) | Equal remainders pair |
| Range update (batch) | Difference array | O(1)/update | Inverse of prefix sum |
| 2D range update | 2D difference | O(1)/update | 4-corner trick |
| Range XOR | Prefix XOR | O(1) | `a^a = 0` cancellation |
| Product except self | Prefix × suffix | O(N) | Left pass + right pass |
| Tree path sum | Depth prefix + LCA | O(log N) | `sum[u]+sum[v]-2*sum[lca]+val[lca]` |
| Subset sums (bitmask) | SOS DP | O(N·2^N) | N-dimensional prefix sum |

### Combining Prefix Sum with Other Techniques

| Combo | Example |
|-------|---------|
| Prefix Sum + Binary Search | Min subarray length with sum ≥ k (non-negative) |
| Prefix Sum + Sliding Window | Two pointers with running sum |
| Prefix Sum + Monotonic Deque | Max subarray sum with length in [a, b] |
| Prefix Sum + Segment Tree | Dynamic range sum with point updates |
| Prefix Sum + BIT (Fenwick) | Online prefix sum with updates |
| Difference Array + Sweep Line | Event counting, interval overlap |
| Prefix Sum + Coordinate Compression | Count inversions, range counting |
| Prefix XOR + Trie | Maximum XOR subarray |

### Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Off-by-one in prefix indexing | Use `n+1` size, `pre[0]=0` convention |
| Forgetting `count[0] = 1` in hash map approach | The empty prefix is a valid subarray start |
| Using prefix sum with updates | Use BIT/Fenwick or segment tree instead |
| Negative modulo in C++/Java | Use `((x % k) + k) % k` |
| Assuming sorted prefix with negatives | Only non-negative arrays give sorted prefix |
| Integer overflow in prefix products | Use modular arithmetic or check bounds |
| 2D inclusion-exclusion sign errors | Draw it out: `+total -top -left +corner` |

### Complexity Summary

| Technique | Build | Query | Update |
|-----------|-------|-------|--------|
| 1D Prefix Sum | O(N) | O(1) | ✗ (static) |
| 2D Prefix Sum | O(RC) | O(1) | ✗ (static) |
| 1D Difference | O(N) | O(N) reconstruct | O(1) |
| 2D Difference | O(RC) | O(RC) reconstruct | O(1) |
| Prefix + HashMap | O(N) | inline | — |
| SOS DP | O(N·2^N) | O(1) | ✗ (static) |
| BIT/Fenwick | O(N) | O(log N) | O(log N) |

---

---

## Practice Order

```
Start here
    │
    ▼
  Running Sum (LC 1480, Easy)          ──── Build a cumulative sum in one pass
    │
    ▼
  Subarray Sum Equals K (LC 560)       ──── Prefix sum + hash map counting (§3)
    │
    ▼
  Range Sum Query 2D Immutable (LC 304) ─── 2D prefix + inclusion-exclusion (§2)
    │
    ▼
  Product of Array Except Self (LC 238) ─── Prefix × suffix, no division (§8)
    │
    ▼
  Continuous Subarray Sum (LC 523)     ──── Prefix mod k, equal remainders (§4)
    │
    ▼
  Count of Range Sum (LC 327, Hard)    ──── Prefix sums + BIT / merge on values (§10)
```

---

**The prefix sum is the Swiss Army knife of competitive programming.** Almost every "range query" or "subarray counting" problem has a prefix sum hiding inside it. When you see "subarray," "range," "sum," "count," or "divisible" — think prefix sum first.

---

## The Prefix Sum Toolbox at a Glance

```
"Aggregate over a contiguous range?"
   │
   ├── QUERY a static array many times
   │     ├── 1D sum/xor        → prefix array, pre[r+1] ⊖ pre[l]     (§1 LC 303, §7 LC 1310)
   │     └── 2D submatrix       → 2D prefix, 4-corner + − − +          (§2 LC 304)
   │
   ├── COUNT subarrays hitting a target
   │     ├── sum == k           → hash map on running sum, count[cur-k]  (§3 LC 560)
   │     ├── sum % k == 0       → array on remainder, count[cur%k]        (§4 LC 974)
   │     ├── xor == k           → hash map, count[cur^k]                  (§7)
   │     └── sum in [lo,hi]      → ordered set / BIT on prefixes          (§10 LC 327)
   │
   ├── UPDATE ranges, read once
   │     ├── 1D range-add        → difference array, d[l]+=v, d[r+1]-=v   (§5 LC 1109)
   │     └── 2D rectangle-add     → 2D difference, 4 corner deltas          (§6)
   │
   ├── AGGREGATE of all-but-one
   │     └── product/min/gcd     → prefix × suffix (mirror pass)            (§8 LC 238)
   │
   └── Higher dimensions / bitmask subsets
         └── sum over submasks   → SOS DP, prefix per bit                  (§11)

THREE MOVES, EVERY TIME:
  1. Pick the AXIS you accumulate over (index / mod value / running sum value / bit).
  2. Pick the COMBINE op and confirm it's INVERTIBLE (+, ^, count — yes; max/min — no).
  3. Reduce the range to a DIFFERENCE of two prefixes (or a count of earlier prefixes).
```

## LeetCode Practice Ladder (the 8 walkthroughs)

```
Start
  │
  ▼
303  (Easy)   ── 1D prefix: build once, query O(1)                       §1
  │
  ▼
1310 (Medium) ── same shape, operator swapped to XOR                     §7
  │
  ▼
560  (Medium) ── prefix + hash map: count subarrays sum = k              §3
  │
  ▼
974  (Medium) ── same map, keyed on remainder (divisible-by-k)           §4
  │
  ▼
238  (Medium) ── prefix × suffix: aggregate of all-but-one               §8
  │
  ▼
1109 (Medium) ── difference array: many range-adds, one read             §5
  │
  ▼
304  (Medium) ── 2D prefix: inclusion-exclusion over a grid              §2
  │
  ▼
327  (Hard)   ── prefix + ordered set: count range sums with negatives   §10
```

---

## When This Fails

Prefix sums answer range queries by *subtracting* two endpoints, so the technique needs an
invertible operation and a static array:

- **Values change between queries.** Rebuilding is O(n) per update. Switch to a
  [Fenwick tree](/pattern/fenwick-tree) for O(log n) updates.
- **The operation has no inverse.** Range min, max, or gcd cannot be recovered by subtraction.
  Use a [segment tree](/pattern/segment-tree), or a sparse table for static RMQ.
- **You want the best region, not all regions.** If the array is non-negative and you want the
  longest or shortest qualifying window, [sliding window](/pattern/sliding-window) is O(n) with
  O(1) space; prefix sums are overkill.
- **Overflow in fixed-width languages.** Prefix sums grow to `n · max`. Python is fine; C++ needs
  `long long`. Modular prefix sums additionally need `((a - b) % m + m) % m` in languages where
  `%` can return a negative.

## Self-Test

Answer these from memory, out loud or on paper, *before* looking. Recognition is not
recall: rereading an explanation feels like knowing, and it is not. A question you cannot answer
cold names the exact section to revisit — you do not need to reread the guide.


**1. What two conditions must hold before you reach for prefix sums?**

<details markdown="1">
<summary>Answer</summary>

The operation must be **invertible** (so `range = prefix(r) − prefix(l−1)` is valid), and the array must be effectively **static** between queries (otherwise each update costs an O(n) rebuild).

</details>

**2. Why is `P` usually sized `n+1` with `P[0] = 0`?**

<details markdown="1">
<summary>Answer</summary>

So that `sum(a[l..r]) = P[r+1] − P[l]` needs no special case at `l = 0`. The extra leading zero removes an entire class of off-by-one bugs; it is worth the one extra slot every time.

</details>

**3. How does the hash-map variant count subarrays summing to k, and why does it work?**

<details markdown="1">
<summary>Answer</summary>

`sum(l..r) = k` is exactly `P[r+1] − P[l] = k`, i.e. `P[l] = P[r+1] − k`. Sweep `r` and keep a map from prefix value to how many times it has occurred; at each step add the count of `P[r+1] − k` seen so far. Seed the map with `{0: 1}` for subarrays that start at index 0.

</details>

**4. What is a difference array, and when is it the right tool?**

<details markdown="1">
<summary>Answer</summary>

The inverse construction: to add `v` over `[l, r]`, write `d[l] += v` and `d[r+1] -= v`, then take a prefix sum of `d` at the end to materialise the array. Right tool for many range *updates* followed by one final read — O(1) per update instead of O(r−l).

</details>

**5. Why does prefix XOR work for subarray-XOR queries, and what makes it possible at all?**

<details markdown="1">
<summary>Answer</summary>

XOR is its own inverse: `x ^ x = 0`. So `xor(l..r) = P[r+1] ^ P[l]`, exactly parallel to subtraction for sums. Invertibility is the whole requirement, and XOR happens to satisfy it in an unusually convenient way.

</details>

**6. What is the 2-D range-sum formula, and where does the correction term come from?**

<details markdown="1">
<summary>Answer</summary>

`sum = P[r2+1][c2+1] − P[r1][c2+1] − P[r2+1][c1] + P[r1][c1]`. Subtracting the top strip and the left strip removes their overlap twice, so the top-left corner has to be added back — plain inclusion–exclusion.

</details>

**7. Prefix sums on a tree: what replaces "subtract the two endpoints"?**

<details markdown="1">
<summary>Answer</summary>

Root-to-node sums plus the LCA. The path sum from `u` to `v` is `P[u] + P[v] − 2·P[lca(u,v)]` (add `val[lca]` back if nodes rather than edges carry the weight). The LCA plays the role the left endpoint plays in an array.

</details>

---

## See Also

- [Fenwick Tree (BIT)](/pattern/fenwick-tree) — the upgrade the moment values change between queries; prefix sums are O(n) to rebuild, a BIT is O(log n) to update.
- [Sliding Window](/pattern/sliding-window) — the cheaper tool when the array is non-negative and you want the *best* window rather than *all* range sums.
- [Binary Search §10](/pattern/binary-search) — `bisect` over a monotone prefix array turns "shortest subarray with sum >= k" into O(n log n).
- [Contribution Counting](/pattern/contribution-counting) — prefix XOR (§7) is the engine behind per-bit contribution counting.
- [Tree Patterns](/pattern/tree) — root-to-node prefix sums (§9) need the traversal and LCA machinery there.
- [Pattern Decision Map](/pattern/decision-map) — the router: which technique does a cold problem call for?
- [Pattern Mastery Program](/pattern/mastery) — the spaced-repetition schedule, mastery checklist, and drill formats that turn reading into recall.

---

*Pattern mastered — stop rescanning the range and start differencing its endpoints. Choose the axis, confirm the operation can be undone, and every range query collapses to arithmetic on two precomputed values.*
