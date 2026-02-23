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

Step by step:
j=0: pre=0, need pre[i]=0-3=-3, count[−3]=0.  Store count[0]=1
j=1: pre=1, need pre[i]=1-3=-2, count[−2]=0.  Store count[1]=1
j=2: pre=3, need pre[i]=3-3=0,  count[0]=1 → found 1!  (subarray [1,2])
j=3: pre=6, need pre[i]=6-3=3,  count[3]=1 → found 1!  (subarray [-2,5]? No, [3])
j=4: pre=4, need pre[i]=4-3=1,  count[1]=1 → found 1!  (subarray [3,-2,5]? No, [2,3,-2])
j=5: pre=9, need pre[i]=9-3=6,  count[6]=1 → found 1!  (subarray [-2,5])

Wait, let me re-trace more carefully:

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
    """Count subarrays with sum in [lo, hi]."""
    # count(sum ≤ hi) - count(sum ≤ lo - 1)
    return _count_at_most(a, hi) - _count_at_most(a, lo - 1)

def _count_at_most(a, target):
    """Count subarrays with sum ≤ target. Uses sorted container or merge sort."""
    # For general arrays (with negatives), this requires more advanced DS
    # For non-negative arrays, sliding window works
    pass
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Count subarrays with sum k | O(N) | O(N) |
| Longest subarray with sum k | O(N) | O(N) |

### Why This Is So Powerful

The hash map transforms the "check all pairs (i, j)" approach from O(N²) to O(N). The key insight: **you don't need to enumerate pairs — you just need to count how many earlier prefixes had the right value.**

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
        left = prefix_gcd[i-1] if i > 0 else 0
        right = suffix_gcd[i+1] if i < n-1 else 0
        if left == 0:
            result[i] = right
        elif right == 0:
            result[i] = left
        else:
            result[i] = gcd(left, right)
    return result
```

---

## 9. Prefix Sum on Trees

### The Idea

On trees, we can use prefix sums along root-to-node paths to answer path queries. Two main approaches:

### Approach 1: Euler Tour + Range Prefix Sum

Flatten the tree with Euler tour, then use 1D prefix sums for **subtree** queries.

```
Tree:        0
           / | \
          1  2  3
         / \
        4   5

Euler tour (tin order): [0, 1, 4, 5, 2, 3]
tin:  [0, 1, 4, 2, 3, 5]  (index in euler order... simplified)

Subtree of node 1 = contiguous range in euler array
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

**The prefix sum is the Swiss Army knife of competitive programming.** Almost every "range query" or "subarray counting" problem has a prefix sum hiding inside it. When you see "subarray," "range," "sum," "count," or "divisible" — think prefix sum first.
