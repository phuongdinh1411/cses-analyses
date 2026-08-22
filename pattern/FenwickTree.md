---
layout: simple
title: "Fenwick Tree (BIT) Patterns"
permalink: /pattern/fenwick-tree
---

# Fenwick Tree (Binary Indexed Tree) — Comprehensive Guide

A Fenwick tree — also called a **Binary Indexed Tree (BIT)** — gives prefix aggregates with point updates in O(log N) using one flat array and a single bit trick. It does less than a [segment tree](/cses-analyses/pattern/segment-tree) but with far less code and a smaller constant factor. When your aggregate is **invertible** (sum, xor) and you need point-update + prefix/range-query, the BIT is the right tool.

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| Prefix sum + **point update** | Basic BIT | [2](#2-basic-fenwick-tree) |
| Understand the `i & -i` magic | The lowbit trick | [3](#3-the-lowbit-trick) |
| **Range update** + point query | Difference BIT | [5](#5-range-update-point-query) |
| **Range update** + range query | Two-BIT trick | [6](#6-range-update-range-query) |
| Find **k-th element** / order statistic | BIT descent | [7](#7-binary-search-on-a-bit) |
| Prefix **xor** with updates | BIT with xor | [4](#4-the-invertibility-requirement) |
| 2D grid point-update + submatrix sum | 2D BIT | [8](#8-2d-fenwick-tree) |
| Count inversions / smaller-after-self | Value-indexed BIT | [9](#9-common-patterns-collection) |
| Decide BIT vs segment tree | Comparison | [10](#10-fenwick-vs-segment-tree) |

---

## Table of Contents

1. [Why a Fenwick Tree](#1-why-a-fenwick-tree)
2. [Basic Fenwick Tree](#2-basic-fenwick-tree)
3. [The lowbit Trick](#3-the-lowbit-trick)
4. [The Invertibility Requirement](#4-the-invertibility-requirement)
5. [Range Update, Point Query](#5-range-update-point-query)
6. [Range Update, Range Query](#6-range-update-range-query)
7. [Binary Search on a BIT](#7-binary-search-on-a-bit)
8. [2D Fenwick Tree](#8-2d-fenwick-tree)
9. [Common Patterns Collection](#9-common-patterns-collection)
10. [Fenwick vs Segment Tree](#10-fenwick-vs-segment-tree)
11. [Pattern Recognition Cheat Sheet](#11-pattern-recognition-cheat-sheet)

---

## 1. Why a Fenwick Tree

You need prefix sums **and** updates, interleaved:

Concretely: you have an array and must process 10^5 interleaved `update(i, x)` and `sumRange(l, r)` operations. A prefix-sum array answers each query in O(1) but every update forces an O(N) rebuild; a plain array updates in O(1) but each sum is O(N) — both are O(N·Q) overall and blow up. The BIT makes **both** operations O(log N), so the whole workload is O(Q log N).

| Approach | Point update | Prefix query |
|----------|--------------|--------------|
| Plain array | O(1) | O(N) |
| Prefix-sum array | O(N) (rebuild) | O(1) |
| **Fenwick tree** | **O(log N)** | **O(log N)** |
| Segment tree | O(log N) | O(log N) |

Fenwick and segment tree have the same asymptotic cost. The Fenwick wins on **code size** (≈10 lines) and **constant factor** (one array, no recursion, cache-friendly). It loses on **generality**: it can only do invertible aggregates (Section 4).

### The Idea

Index `i` (1-based) is responsible for a range of length `lowbit(i)` ending at `i`, where `lowbit(i) = i & (-i)` is the lowest set bit. A prefix sum walks down by stripping lowest bits; an update walks up by adding them.

```
Responsibility ranges (1-indexed, n=8):

 idx:  1   2   3   4   5   6   7   8
 bit:  1  10  11 100 101 110 111 1000
 len:  1   2   1   4   1   2   1    8

 tree[1] covers a[1]
 tree[2] covers a[1..2]
 tree[3] covers a[3]
 tree[4] covers a[1..4]
 tree[6] covers a[5..6]
 tree[8] covers a[1..8]
```

---

## 2. Basic Fenwick Tree

Point update, prefix sum, range sum. 1-indexed internally; the API below takes 0-indexed positions.

> **Reading the examples:** the diagrams and walks in this guide show the internal **1-indexed** `tree[]`; the code's public methods take **0-indexed** positions and do `i += 1` at the boundary. So a 0-indexed position `p` in the API maps to internal index `p + 1`.

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)      # 1-indexed, index 0 unused

    def update(self, i, delta):        # a[i] += delta  (0-indexed i)
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)              # move to next responsible index (add lowbit)

    def prefix(self, i):               # sum of a[0..i]  (0-indexed i)
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)              # strip lowbit, jump to previous range
        return s

    def range_sum(self, l, r):         # sum of a[l..r] inclusive
        return self.prefix(r) - (self.prefix(l - 1) if l > 0 else 0)
```

### Build in O(N)

Naive build is N updates = O(N log N). Linear build: add each value to its parent.

```python
    @classmethod
    def from_array(cls, data):
        bit = cls(len(data))
        for i, v in enumerate(data):
            bit.tree[i + 1] += v
        for i in range(1, bit.n + 1):
            j = i + (i & (-i))
            if j <= bit.n:
                bit.tree[j] += bit.tree[i]
        return bit
```

### Complexity

| Op | Time |
|----|------|
| Build (linear) | O(N) |
| Point update | O(log N) |
| Prefix / range query | O(log N) |
| Space | O(N) |

### Worked Trace on Real Values

Take `a = [3, 2, -1, 5]` (0-indexed). After building, the internal 1-indexed `tree[]` holds each index's responsibility range:

```
 internal idx:  1   2   3   4
 covers:       a[0] a[0..1] a[2] a[0..3]
 tree[]:        3    5     -1    9

 tree[1] = a[0]              = 3
 tree[2] = a[0] + a[1]       = 3 + 2       = 5
 tree[3] = a[2]              = -1
 tree[4] = a[0]+a[1]+a[2]+a[3] = 3+2-1+5   = 9
```

Now `prefix(2)` (0-indexed → sum of `a[0..2]` = 3 + 2 + (-1) = **4**). The code does `i += 1`, so it descends from internal index 3:

```
i = 3 (011): add tree[3] = -1      strip lowbit(1) -> i = 2
i = 2 (010): add tree[2] =  5      strip lowbit(2) -> i = 0  stop

sum = tree[3] + tree[2] = -1 + 5 = 4  ✓  (matches a[0]+a[1]+a[2])
```

---

## 3. The lowbit Trick

`lowbit(i) = i & (-i)` isolates the **lowest set bit**. Two's complement makes `-i` flip-all-bits-plus-one, so `i & -i` leaves only that lowest 1.

```
 i      = 12 = 0000 1100
-i      =      1111 0100   (two's complement)
 i & -i = 0000 0100 = 4    (the lowbit)
```

### The Two Walks

```
UPDATE (climb): i += lowbit(i)
  a[6] changes (0-indexed) -> internal index 7 (a[6] maps to i = 6 + 1 = 7)
  7 -> 8 -> (past n, stop)

QUERY (descend): i -= lowbit(i)
  prefix up to index 7:
  7 (0111) -> strip -> 6 (0110) -> strip -> 4 (0100) -> strip -> 0 stop
  tree[7] + tree[6] + tree[4]  = a[7] + a[5..6] + a[1..4]  = a[1..7]  ✓
```

Update adds lowbit (goes to the wider range containing you); query subtracts lowbit (jumps to the previous disjoint chunk). The two are exact inverses of each other — that symmetry is why 10 lines suffice.

---

## 4. The Invertibility Requirement

Range query is `prefix(r) - prefix(l-1)`. That **subtraction** is mandatory: a BIT can only answer a range if the operation has an **inverse**.

| Aggregate | Inverse exists? | BIT works? |
|-----------|-----------------|------------|
| Sum | yes (subtract) | ✓ |
| XOR | yes (xor again) | ✓ |
| Count | yes | ✓ |
| Product (no zeros) | yes (divide) | ✓ (careful with 0) |
| **Min / Max** | **no** | ✗ — use segment tree |
| GCD | no | ✗ — use segment tree |

### Prefix XOR Variant

Same code, swap `+` for `^` and identity stays `0` (xor is its own inverse).

```python
class XorBIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, val):          # a[i] ^= val
        i += 1
        while i <= self.n:
            self.tree[i] ^= val
            i += i & (-i)

    def prefix_xor(self, i):
        i += 1; x = 0
        while i > 0:
            x ^= self.tree[i]
            i -= i & (-i)
        return x

    def range_xor(self, l, r):
        return self.prefix_xor(r) ^ (self.prefix_xor(l - 1) if l > 0 else 0)
```

`★ Insight ─────────────────────────────────────`
This is the single most important "when to use" line: **min/max/gcd have no inverse, so a plain BIT cannot do range-min/max — reach for a segment tree instead.** (There is a max-BIT that supports prefix-max with point-increase-only updates, but it can't do arbitrary decreases or true range-max. Don't force it.)
`─────────────────────────────────────────────────`

---

## 5. Range Update, Point Query

Flip the roles using a **difference array** stored in a BIT. To add `x` to `a[l..r]`: `diff[l] += x`, `diff[r+1] -= x`. Then `a[i] = prefix_sum(diff, i)`.

```python
class RangeUpdateBIT:
    def __init__(self, n):
        self.bit = BIT(n)
        self.n = n

    def range_add(self, l, r, x):      # a[l..r] += x
        self.bit.update(l, x)
        if r + 1 < self.n:
            self.bit.update(r + 1, -x)

    def point_query(self, i):          # value at a[i]
        return self.bit.prefix(i)      # prefix of the difference array = current value
```

Query is now the point value, update is the range. Mirror image of the basic BIT.

---

## 6. Range Update, Range Query

The two-BIT trick. Support both range-add and range-sum in O(log N). Derived from expanding the difference-array prefix sum algebraically.

Let `d` be the difference array (`d[l]+=x`, `d[r+1]-=x`). Then:

```
sum(a[1..i]) = sum_{k=1..i} ( (i+1) * d[k]  -  k * d[k] )
             = (i+1) * prefix(B1, i)  -  prefix(B2, i)

where B1 tracks d[k], B2 tracks k*d[k].
```

```python
class RangeRangeBIT:
    def __init__(self, n):
        self.n = n
        self.b1 = BIT(n)               # tracks d[k]
        self.b2 = BIT(n)               # tracks k * d[k]

    def range_add(self, l, r, x):      # a[l..r] += x  (0-indexed inclusive)
        self.b1.update(l, x)
        if r + 1 < self.n: self.b1.update(r + 1, -x)
        self.b2.update(l, x * l)
        if r + 1 < self.n: self.b2.update(r + 1, -x * (r + 1))

    def prefix(self, i):               # sum a[0..i]
        return (i + 1) * self.b1.prefix(i) - self.b2.prefix(i)

    def range_sum(self, l, r):
        return self.prefix(r) - (self.prefix(l - 1) if l > 0 else 0)
```

This does what a lazy segment tree does (range add + range sum) in ~half the code — but **only** for invertible aggregates. For range-assign or range-min, you still need the segment tree.

---

## 7. Binary Search on a BIT

Find the smallest index whose prefix sum reaches `k` in a single O(log N) descent — no O(log²N) query-in-a-binary-search. Walk bits from high to low.

```python
def find_kth(bit, k):
    """Smallest 0-indexed i with prefix(i) >= k. Assumes non-negative values."""
    pos = 0
    log = bit.n.bit_length()
    for b in range(log, -1, -1):
        nxt = pos + (1 << b)
        if nxt <= bit.n and bit.tree[nxt] < k:
            pos = nxt
            k -= bit.tree[nxt]
    return pos            # 0-indexed answer is pos (1-indexed pos+1)
```

Classic use: value-indexed BIT of counts → `find_kth` returns the k-th smallest value present. Same job as the segment-tree descent, fewer lines.

---

## 8. 2D Fenwick Tree

Point update + prefix-rectangle sum on a grid, in O(log M · log N). Nest the climb/descend in both dimensions.

```python
class BIT2D:
    def __init__(self, rows, cols):
        self.R, self.C = rows, cols
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]

    def update(self, r, c, delta):     # grid[r][c] += delta (0-indexed)
        i = r + 1
        while i <= self.R:
            j = c + 1
            while j <= self.C:
                self.tree[i][j] += delta
                j += j & (-j)
            i += i & (-i)

    def prefix(self, r, c):            # sum of grid[0..r][0..c]
        s = 0
        i = r + 1
        while i > 0:
            j = c + 1
            while j > 0:
                s += self.tree[i][j]
                j -= j & (-j)
            i -= i & (-i)
        return s

    def rect_sum(self, r1, c1, r2, c2):   # inclusive rectangle
        return (self.prefix(r2, c2) - self.prefix(r1 - 1, c2)
                - self.prefix(r2, c1 - 1) + self.prefix(r1 - 1, c1 - 1))
```

Inclusion-exclusion on four prefix rectangles gives the submatrix sum — same shape as the [2D prefix-sum](/cses-analyses/pattern/prefix-sum) formula, but now updatable.

---

## 9. Common Patterns Collection

### Count Inversions

Sweep right-to-left over value-ranks; each element asks "how many already-seen values are smaller."

```python
def count_inversions(arr):
    order = sorted(set(arr))
    rank = {v: i for i, v in enumerate(order)}
    bit = BIT(len(order))
    inv = 0
    for x in reversed(arr):
        r = rank[x]
        inv += bit.prefix(r - 1) if r > 0 else 0   # smaller values seen so far
        bit.update(r, 1)
    return inv
```

### Count of Smaller Numbers After Self

Same sweep, collect per-element instead of summing.

### Dynamic Range Sum (CSES)

Basic BIT (Section 2) — read point updates and range queries, dispatch.

### Range Add + Range Sum (CSES "Range Update Queries")

Two-BIT trick (Section 6).

### K-th Remaining Element

Value/position BIT of 1s + `find_kth` descent (Section 7); set leaf to 0 on removal.

---

## 10. Fenwick vs Segment Tree

The core decision this guide exists to answer.

| | Fenwick (BIT) | Segment Tree |
|--|---------------|--------------|
| Aggregates | Invertible only: sum, xor, count | Any associative: sum, min, max, gcd, ... |
| Range min / max | ✗ | ✓ |
| Range update + range query | ✓ (two-BIT trick, invertible only) | ✓ (lazy, any op) |
| Range **assign** (set to x) | ✗ | ✓ (lazy) |
| Code size | ~10 lines | ~40+ lines |
| Constant factor | Smaller (cache-friendly, no recursion) | Larger |
| Persistence | Awkward | Natural |
| k-th descent | ✓ (Section 7) | ✓ |
| 2D | ✓ (clean) | Possible but heavy |

### Decision Flow

```
Need range min / max / gcd?            -> Segment tree (BIT can't invert)
Need range ASSIGN (set all = x)?       -> Segment tree (lazy)
Need persistence / historical query?   -> Segment tree (persistent)
Just sum/xor + point or range updates? -> BIT  (shorter, faster)
2D point update + rectangle sum?       -> 2D BIT
```

**Summary**: reach for the BIT first when the operation is sum/xor — it's less code and faster. The moment you hit min/max/gcd, range-assign, or persistence, switch to a segment tree.

---

## 11. Pattern Recognition Cheat Sheet

### By Problem Signal

| You see... | Reach for | Section |
|------------|-----------|---------|
| "Prefix/range sum with updates" | Basic BIT | [2](#2-basic-fenwick-tree) |
| "Prefix xor with updates" | XOR BIT | [4](#4-the-invertibility-requirement) |
| "Add x to a range, query single point" | Difference BIT | [5](#5-range-update-point-query) |
| "Add x to a range, query range sum" | Two-BIT trick | [6](#6-range-update-range-query) |
| "K-th smallest present / order statistic" | BIT descent | [7](#7-binary-search-on-a-bit) |
| "Count inversions / smaller-after-self" | Value-indexed BIT | [9](#9-common-patterns-collection) |
| "Grid point update + submatrix sum" | 2D BIT | [8](#8-2d-fenwick-tree) |
| "Range **min/max/gcd**" | NOT a BIT — segment tree | [10](#10-fenwick-vs-segment-tree) |
| "Range **assign** to x" | NOT a BIT — segment tree lazy | [10](#10-fenwick-vs-segment-tree) |

### The Two Lines You Must Memorize

```python
i += i & (-i)   # UPDATE: climb to the wider range containing i
i -= i & (-i)   # QUERY:  descend to the previous disjoint chunk
```

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Using a BIT for range min/max | No inverse — use segment tree |
| 0-indexed off-by-one | BIT is 1-indexed internally; `i += 1` at the boundary |
| Index 0 used | Leave `tree[0]` unused; loops break at `i > 0` |
| Range-update but forgot `r+1` decrement | Difference array needs both `+x` at l and `-x` at r+1 |
| O(N log N) build in a tight loop | Use the linear `from_array` build |
| Product BIT with a zero element | Division breaks — guard or use segment tree |

### Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build (linear) | O(N) | O(N) |
| Point update | O(log N) | — |
| Prefix / range query | O(log N) | — |
| Range update (difference / two-BIT) | O(log N) | — |
| k-th descent | O(log N) | — |
| 2D update / query | O(log M · log N) | O(M·N) |

---

## Practice Order

```
Start here
    │
    ▼
  Dynamic Range Sum (CSES, Easy)  ──── Basic BIT: point update + range query (§2)
    │
    ▼
  Range Update Queries (CSES)     ──── Two-BIT trick: range add + range sum (§6)
    │
    ▼
  Count Inversions (LC 493 / CSES) ─── Value-indexed BIT: count smaller-so-far (§9)
    │
    ▼
  K-th / order-statistic descent  ──── find_kth: one O(log N) bit walk (§7)
    │
    ▼
  2D BIT (Hard)                   ──── Nest the walk in both dims + inclusion-exclusion (§8)
```

---

## See Also

- [Segment Tree Patterns](/cses-analyses/pattern/segment-tree) — when you need min/max/gcd, range assign, lazy propagation, or persistence.
- [Prefix Sum Patterns](/cses-analyses/pattern/prefix-sum) — static (no-update) range queries in O(1).
