---
layout: simple
title: "Segment Tree Patterns"
permalink: /pattern/segment-tree
---

# Segment Tree Patterns — Comprehensive Guide

A segment tree answers **range queries** and applies **updates** on an array in O(log N) each. The core idea: recursively split the array into halves, store an aggregate (sum, min, max, gcd, ...) for every segment, and reuse those aggregates instead of rescanning. Once you see it as a **mergeable-aggregate over a recursive split**, everything from range-sum to range-assign-with-lazy becomes one skeleton with a different `combine` function.

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| Query range sum/min/max with **point updates** | Basic segment tree | [2](#2-basic-segment-tree-recursive) |
| Write it **short and fast** | Iterative segment tree | [3](#3-iterative-segment-tree) |
| Swap sum for min/max/gcd without rewriting | The merge abstraction | [4](#4-the-merge-abstraction) |
| Apply an **update to a whole range** | Lazy propagation | [5](#5-lazy-propagation-range-updates) |
| **Range assign** (set all to x) + range query | Lazy with assignment | [5](#5-lazy-propagation-range-updates) |
| Find **first index** with prefix condition | Descent on the tree | [6](#6-binary-search-on-the-tree) |
| Count / query on **values** not indices | Segment tree over value domain | [7](#7-segment-tree-on-values) |
| Handle values too large to index | Coordinate compression | [7](#7-segment-tree-on-values) |
| Query historical versions | Persistent segment tree | [8](#8-persistent-segment-tree) |
| Just count inversions / order-stats | BIT (Fenwick) alternative | [9](#9-when-to-use-a-bit-instead) |
| See full **worked LeetCode solutions** | 307 / 699 / 327 walkthroughs | [9.5](#95-worked-leetcode-problems) |

---

## Table of Contents

1. [Why a Segment Tree](#1-why-a-segment-tree)
2. [Basic Segment Tree (Recursive)](#2-basic-segment-tree-recursive)
3. [Iterative Segment Tree](#3-iterative-segment-tree)
4. [The Merge Abstraction](#4-the-merge-abstraction)
5. [Lazy Propagation (Range Updates)](#5-lazy-propagation-range-updates)
6. [Binary Search on the Tree](#6-binary-search-on-the-tree)
7. [Segment Tree on Values](#7-segment-tree-on-values)
8. [Persistent Segment Tree](#8-persistent-segment-tree)
9. [When to Use a BIT Instead](#9-when-to-use-a-bit-instead)
9.5. [Worked LeetCode Problems](#95-worked-leetcode-problems)
10. [Common Patterns Collection](#10-common-patterns-collection)
11. [Pattern Recognition Cheat Sheet](#11-pattern-recognition-cheat-sheet)

---

## 1. Why a Segment Tree

### The Problem It Solves

You have an array and a mix of two operations, interleaved:

- **Update**: change element(s).
- **Query**: aggregate over a range `[l, r]` (sum, min, max, gcd, ...).

| Approach | Update | Range query |
|----------|--------|-------------|
| Plain array | O(1) | O(N) |
| Prefix sums | O(N) (rebuild) | O(1) |
| **Segment tree** | **O(log N)** | **O(log N)** |

Prefix sums are unbeatable when there are **no updates**. The moment updates interleave with queries, prefix sums die (every update forces an O(N) rebuild), and the segment tree wins.

### The Structure

Each node covers a contiguous range. Root covers `[0, n-1]`. A node covering `[l, r]` with `l != r` splits at `mid = (l+r)/2` into `[l, mid]` and `[mid+1, r]`. Leaves cover single elements.

```
array = [5, 3, 7, 9, 6, 2]   (sum tree)

                    [0,5]=32
                   /        \
            [0,2]=15        [3,5]=17
           /      \         /      \
      [0,1]=8   [2,2]=7  [3,4]=15  [5,5]=2
      /    \             /    \
  [0,0]=5 [1,1]=3   [3,3]=9 [4,4]=6
```

A range query decomposes `[l, r]` into O(log N) node ranges that exactly tile it. That's the whole trick.

### Master LeetCode Comparison Table

The five representative segment-tree problems, ordered by the sub-pattern they force. Read the "Tree indexed by" column first — it is the single fork that decides everything else.

| LC # | Problem | Difficulty | Tree indexed by | Node stores | Update kind | Query answers | Sub-pattern (§) |
|------|---------|-----------|-----------------|-------------|-------------|---------------|-----------------|
| **307** | Range Sum Query - Mutable | Medium | array position | sum | point assign | range sum | Basic point-update (§2/§3) |
| **699** | Falling Squares | Hard | compressed x | max height | range assign-max (lazy) | range max | Lazy propagation (§5) |
| **715** | Range Module | Hard | compressed x | covered? | range assign 0/1 (lazy) | range all-covered? | Lazy assign (§5) |
| **327** | Count of Range Sums | Hard | **prefix value** | count | point +1 | count in value range | Tree on values (§7) |
| **1649** | Create Sorted Array | Hard | **element value** | count | point +1 | count smaller / larger | Tree on values (§7) |

`★ Insight ─────────────────────────────────────`
Two problems (307, 699) index by **position** — the leaf is array slot `i`. Two (327, 1649) index by **value** — the leaf is "how many elements equal value `v` seen so far", and the array position is thrown away. That axis choice is the whole design decision: position-indexed answers "aggregate over a slice"; value-indexed answers "how many seen so far are smaller/larger/in-range". Same tree, opposite meaning of the index. The counting (value-indexed) rows can all be done with a shorter [BIT](/pattern/fenwick-tree) instead — reach for the segment tree only when you also need min/max/assign or range-updates.
`─────────────────────────────────────────────────`

---

## 2. Basic Segment Tree (Recursive)

Point update, range query. The clearest version to learn first.

```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)   # 4N is a safe upper bound
        if self.n:
            self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, lo, hi):
        if lo == hi:
            self.tree[node] = data[lo]
            return
        mid = (lo + hi) // 2
        self._build(data, 2 * node, lo, mid)
        self._build(data, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, i, val):
        self._update(1, 0, self.n - 1, i, val)

    def _update(self, node, lo, hi, i, val):
        if lo == hi:
            self.tree[node] = val        # set index i to val
            return
        mid = (lo + hi) // 2
        if i <= mid:
            self._update(2 * node, lo, mid, i, val)
        else:
            self._update(2 * node + 1, mid + 1, hi, i, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, node, lo, hi, l, r):
        if r < lo or hi < l:             # node range fully outside query
            return 0                     # identity for sum
        if l <= lo and hi <= r:          # node range fully inside query
            return self.tree[node]
        mid = (lo + hi) // 2
        return (self._query(2 * node, lo, mid, l, r) +
                self._query(2 * node + 1, mid + 1, hi, l, r))
```

### The Three Cases in Query

Every recursive query node hits exactly one of these:

```
query [l, r] vs node [lo, hi]:

  Case A: no overlap     ->  return identity (0 for sum)
      [lo...hi]  [l...r]

  Case B: total overlap  ->  return stored aggregate (stop, don't recurse)
      [l ... lo...hi ... r]

  Case C: partial overlap ->  recurse into both children, combine
      [lo ... [l...] ... hi]
```

### Why `4 * n`?

The recursion tree is not perfectly balanced when `n` is not a power of two. Node indices can reach up to `~2 * next_power_of_two(n)`, and `4 * n` is a simple safe over-allocation. If you round `n` up to a power of two first, `2 * n` suffices.

### Complexity

| Op | Time |
|----|------|
| Build | O(N) |
| Point update | O(log N) |
| Range query | O(log N) |
| Space | O(N) |

---

## 3. Iterative Segment Tree

The bottom-up iterative form is shorter, ~2x faster (no recursion overhead), and the standard in competitive programming. It stores leaves at `tree[n .. 2n-1]` and internal nodes at `tree[1 .. n-1]`.

```python
class SegTreeIterative:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        # place leaves
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        # build internal nodes bottom-up
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, i, val):
        i += self.n
        self.tree[i] = val
        i //= 2
        while i >= 1:
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
            i //= 2

    def query(self, l, r):
        """Sum over [l, r] inclusive."""
        res = 0
        l += self.n
        r += self.n + 1          # half-open [l, r+1)
        while l < r:
            if l & 1:            # l is a right child -> include, move right
                res += self.tree[l]
                l += 1
            if r & 1:            # r is a right child -> its left sibling is in range
                r -= 1
                res += self.tree[r]
            l //= 2
            r //= 2
        return res
```

### The Climb

```
Query [2, 4] on n=6, leaves at indices 6..11:

l = 6+2 = 8, r = 6+4+1 = 11
  l=8 even, r=11 odd -> r=10, res += tree[10]; l=4, r=5
  l=4 even, r=5  odd -> r=4,  res += tree[4];  l=2, r=2
  l == r -> stop
```

The two odd-index checks are the whole algorithm: an odd index means "you are a right child, so your parent would over-cover the range — grab yourself and step inward."

### Trade-offs vs Recursive

| | Recursive | Iterative |
|--|-----------|-----------|
| Speed | Slower (call overhead) | ~2x faster |
| Readability | Higher | Lower (index tricks) |
| Lazy propagation | Natural | Awkward (do lazy recursively) |
| Line count | More | Fewer |

**Rule of thumb**: iterative for point-update + range-query hot loops; recursive when you need lazy propagation.

---

## 4. The Merge Abstraction

Sum, min, max, gcd — all the same tree, differing only in the **combine function** and its **identity**. Factor those two out and one class handles every variant.

```python
class SegTree:
    def __init__(self, data, combine, identity):
        self.n = len(data)
        self.combine = combine       # e.g. min, max, lambda a,b: a+b, math.gcd
        self.identity = identity     # neutral element for combine
        self.tree = [identity] * (2 * self.n)
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = combine(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, val):
        i += self.n
        self.tree[i] = val
        i >>= 1
        while i:
            self.tree[i] = self.combine(self.tree[2 * i], self.tree[2 * i + 1])
            i >>= 1

    def query(self, l, r):
        resl = resr = self.identity
        l += self.n
        r += self.n + 1
        while l < r:
            if l & 1:
                resl = self.combine(resl, self.tree[l]); l += 1
            if r & 1:
                r -= 1; resr = self.combine(self.tree[r], resr)
            l >>= 1; r >>= 1
        return self.combine(resl, resr)
```

### Identity Elements

| Operation | combine | identity |
|-----------|---------|----------|
| Sum | `a + b` | `0` |
| Min | `min(a, b)` | `+inf` |
| Max | `max(a, b)` | `-inf` |
| GCD | `math.gcd(a, b)` | `0` |
| Product | `a * b` | `1` |
| Bitwise AND | `a & b` | `~0` (all ones) |
| Bitwise OR | `a \| b` | `0` |

### Why Two Accumulators (`resl`, `resr`)?

For **non-commutative** merges (matrix product, string concatenation, "max subarray" structs) order matters. Left-side nodes must combine left-to-right and right-side nodes right-to-left, then join. For sum/min/max it doesn't matter, but keeping both accumulators makes the template correct for all cases.

`★ Insight ─────────────────────────────────────`
The requirement is that `combine` be **associative**. It need not be commutative. Sum/min/max/gcd are both. But "merge two max-subarray structs" (holding total, best-prefix, best-suffix, best-answer) is associative-only — and the two-accumulator query above handles it correctly where a single accumulator would not.
`─────────────────────────────────────────────────`

---

## 5. Lazy Propagation (Range Updates)

Point update is O(log N). But a **range update** ("add 5 to every element in `[l, r]`") touched naively is O(N log N). Lazy propagation defers the work: mark a node "this whole subtree owes an update" and only push it down when a query actually descends into that subtree. Range update becomes O(log N).

### The Two Lazy Flavors

1. **Range add**: `a[i] += x` for all `i` in `[l, r]`. Lazy value accumulates additively.
2. **Range assign**: `a[i] = x` for all `i` in `[l, r]`. Lazy value overwrites; needs a "has pending assign" marker.

### Range Add + Range Sum

```python
class LazySegTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)   # pending "+x" for this node's whole range
        if self.n:
            self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, lo, hi):
        if lo == hi:
            self.tree[node] = data[lo]
            return
        mid = (lo + hi) // 2
        self._build(data, 2 * node, lo, mid)
        self._build(data, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _apply(self, node, lo, hi, val):
        """Apply a pending +val to this whole node range."""
        self.tree[node] += val * (hi - lo + 1)   # sum grows by val per element
        self.lazy[node] += val                   # remember to push to children

    def _push_down(self, node, lo, hi):
        if self.lazy[node]:
            mid = (lo + hi) // 2
            self._apply(2 * node, lo, mid, self.lazy[node])
            self._apply(2 * node + 1, mid + 1, hi, self.lazy[node])
            self.lazy[node] = 0

    def update(self, l, r, val):
        self._update(1, 0, self.n - 1, l, r, val)

    def _update(self, node, lo, hi, l, r, val):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            self._apply(node, lo, hi, val)       # whole node covered: mark lazy, stop
            return
        self._push_down(node, lo, hi)
        mid = (lo + hi) // 2
        self._update(2 * node, lo, mid, l, r, val)
        self._update(2 * node + 1, mid + 1, hi, l, r, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, node, lo, hi, l, r):
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return self.tree[node]
        self._push_down(node, lo, hi)
        mid = (lo + hi) // 2
        return (self._query(2 * node, lo, mid, l, r) +
                self._query(2 * node + 1, mid + 1, hi, l, r))
```

### The Three Lazy Primitives

Every lazy segment tree is these three functions. Get them right, the rest is boilerplate:

| Function | Job |
|----------|-----|
| `_apply(node, lo, hi, val)` | Apply an update to a node's aggregate **and** record it in `lazy` |
| `_push_down(node)` | Move this node's pending lazy to both children, then clear it |
| pull-up (`tree[node] = combine(children)`) | Recompute aggregate after children change |

**Order matters**: always `_push_down` **before** recursing into children on a partial overlap, and pull-up **after**.

### Range Assign Variant

Assignment overwrites rather than accumulates, so you need a sentinel meaning "no pending assign" (assign of `0` is a real value, so a separate flag or `None` is required).

> **Note — this is a patch on top of `LazySegTree` above, not standalone code.** It replaces `_apply`/`_push_down` and additionally requires a `self.has_lazy = [False] * (4 * self.n)` array added in `__init__` (the assign-marker). Pasting these two methods alone will `AttributeError` on `self.has_lazy`.

```python
    def _apply_assign(self, node, lo, hi, val):
        self.tree[node] = val * (hi - lo + 1)
        self.lazy[node] = val
        self.has_lazy[node] = True

    def _push_down(self, node, lo, hi):
        if self.has_lazy[node]:
            mid = (lo + hi) // 2
            self._apply_assign(2 * node, lo, mid, self.lazy[node])
            self._apply_assign(2 * node + 1, mid + 1, hi, self.lazy[node])
            self.has_lazy[node] = False
```

### Combining Add + Assign

If a problem mixes both (assign then add), an assign must **clear** any pending add on that node, and a later add stacks on top. Keep two lazy fields plus an assign flag; when applying assign, reset the add lazy to the added amount. This is fiddly — draw the state machine before coding.

---

## 6. Binary Search on the Tree

"Find the first index `i` where prefix-sum reaches `k`" or "leftmost position with value `>= x`". Instead of querying prefixes in O(log^2 N), **descend** the tree in a single O(log N) walk, deciding left-vs-right at each node.

### Find First Prefix Sum >= k

```python
def find_first_ge(self, k):
    """Smallest index i such that sum(a[0..i]) >= k. Assumes non-negative values."""
    if self.tree[1] < k:
        return -1                       # total sum too small
    node, lo, hi = 1, 0, self.n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if self.tree[2 * node] >= k:    # answer is in left subtree
            node, hi = 2 * node, mid
        else:
            k -= self.tree[2 * node]    # consume left, go right
            node, lo = 2 * node + 1, mid + 1
    return lo
```

### Why This Beats Binary-Search-Over-Query

The naive way binary searches the index and calls `query(0, mid)` each step: O(log N) steps × O(log N) per query = O(log^2 N). The descent fuses them into one O(log N) walk because the tree already stores the prefix aggregates you'd otherwise recompute.

Classic use: the CSES-style "list removal / k-th remaining element" problem — build a tree of 1s, and `find_first_ge(k)` finds the k-th surviving position, then set that leaf to 0.

---

## 7. Segment Tree on Values

Build the tree indexed by **value** (or value-rank), not array position. Leaf `v` holds "how many elements equal `v`" (or a sum, etc.). Range query then answers value-range questions: count of elements in `[a, b]`, k-th smallest, number of inversions.

### Count Inversions

> **Which tree / assign vs add:** this uses `SegTreeIterative` from Section 3, whose `update(i, val)` **assigns** (overwrites) leaf `i`. Because it has no "+=" operation, we emulate an increment by reading the current count and assigning `count + 1` (`st.update(r, st.query(r, r) + 1)`). If you swap in a tree whose `update` *adds* a delta, drop the read and just do `st.update(r, 1)`.

```python
def count_inversions(arr):
    # compress values to ranks 0..m-1
    ranks = {v: i for i, v in enumerate(sorted(set(arr)))}
    m = len(ranks)
    st = SegTreeIterative([0] * m)    # counts per value; update() ASSIGNS, not adds
    inversions = 0
    for x in reversed(arr):
        r = ranks[x]
        inversions += st.query(0, r - 1) if r > 0 else 0  # already-seen smaller values
        st.update(r, st.query(r, r) + 1)                  # assign count+1 (emulated increment)
    return inversions
```

### Coordinate Compression

Values can be up to 1e9 but there are only N of them. Map them to `0..N-1` by sorting the distinct values — then a tree of size N indexes them. This is the standard companion to value-indexed segment trees (and BITs).

```python
def compress(arr):
    order = sorted(set(arr))
    rank = {v: i for i, v in enumerate(order)}
    return [rank[v] for v in arr], order   # order[i] recovers original value
```

`★ Insight ─────────────────────────────────────`
Inversions, "count smaller after self", k-th order statistic, and "range count of values" are all the *same* value-indexed tree with a different query. Recognizing the value-domain reframing is the actual skill; the tree is just plumbing. A BIT (Section 9) does the counting versions with less code.
`─────────────────────────────────────────────────`

---

## 8. Persistent Segment Tree

A persistent tree keeps **every past version** accessible. Each update creates O(log N) new nodes (the path from root to leaf) and shares the rest with the previous version. N updates cost O(N log N) space total.

### The Idea

```
Update index i: copy only the root-to-leaf path.
Every off-path child pointer is reused from the old version.

  version k        version k+1
      root_k          root_{k+1}   (new)
     /    \           /       \
    L      R   -->   L'(new)   R    (R shared!)
   ...              ...
```

### Node-Pointer Implementation

```python
class PersistentSegTree:
    def __init__(self, n):
        self.n = n
        self.left = [0]      # child pointers, index 0 = null node
        self.right = [0]
        self.val = [0]

    def _new(self, l, r, v):
        self.left.append(l); self.right.append(r); self.val.append(v)
        return len(self.val) - 1

    def build(self, lo, hi):
        if lo == hi:
            return self._new(0, 0, 0)
        mid = (lo + hi) // 2
        l = self.build(lo, mid)
        r = self.build(mid + 1, hi)
        return self._new(l, r, self.val[l] + self.val[r])

    def update(self, prev, lo, hi, i, delta):
        """Return root of a NEW version with a[i] += delta, sharing prev's untouched nodes."""
        if lo == hi:
            return self._new(0, 0, self.val[prev] + delta)
        mid = (lo + hi) // 2
        if i <= mid:
            l = self.update(self.left[prev], lo, mid, i, delta)
            r = self.right[prev]                     # shared
        else:
            l = self.left[prev]                      # shared
            r = self.update(self.right[prev], mid + 1, hi, i, delta)
        return self._new(l, r, self.val[l] + self.val[r])

    def query(self, node, lo, hi, l, r):
        if r < lo or hi < l or node == 0:
            return 0
        if l <= lo and hi <= r:
            return self.val[node]
        mid = (lo + hi) // 2
        return (self.query(self.left[node], lo, mid, l, r) +
                self.query(self.right[node], mid + 1, hi, l, r))
```

### Killer Application: K-th Smallest in a Range

Store a prefix of versions (version `i` = value-counts of `a[0..i-1]`). To answer "k-th smallest in `a[l..r]`", walk **two versions simultaneously** (`root[r+1]` minus `root[l]`) and descend by count — O(log N) per query, no updates needed. This is the standard offline range-kth-order-statistic solution.

---

## 9. When to Use a BIT Instead

A **Binary Indexed Tree (Fenwick)** does prefix-sum + point-update in O(log N) with far less code. If your problem only needs those two, prefer it. Full treatment (range-update BIT, 2D BIT, k-th descent): [Fenwick Tree Patterns](/cses-analyses/pattern/fenwick-tree).

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)     # 1-indexed

    def update(self, i, delta):       # a[i] += delta  (0-indexed i)
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)             # add lowest set bit

    def prefix(self, i):              # sum of a[0..i]  (0-indexed i)
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)             # strip lowest set bit
        return s

    def range_sum(self, l, r):
        return self.prefix(r) - (self.prefix(l - 1) if l > 0 else 0)
```

### Segment Tree vs BIT

| | BIT (Fenwick) | Segment Tree |
|--|---------------|--------------|
| Operations | Prefix-sum-style (invertible: sum, xor) | Any associative merge (min, max, gcd, ...) |
| Range min/max | ✗ (not invertible) | ✓ |
| Range update + range query | Harder (two BITs trick) | Natural (lazy) |
| Code size | Tiny | Larger |
| Constant factor | Smaller | Larger |
| Persistence | Awkward | Natural |

**Decision**: sum/xor + point updates → BIT. Min/max/gcd, range assign, or "first index where..." → segment tree.

---

## 9.5 Worked LeetCode Problems

Three problems, one per core sub-pattern from the [Master Comparison Table](#master-leetcode-comparison-table): a position-indexed point-update tree (307), a lazy range-assign tree (699), and a value-indexed count tree (327). Every solution below was executed against the LeetCode canonical answers before being written here.

### Problem 307 — Range Sum Query - Mutable

**Difficulty**: Medium

**Statement.** Given an integer array `nums`, support two operations any number of times, interleaved: `update(index, val)` sets `nums[index] = val`, and `sumRange(left, right)` returns the sum of `nums[left..right]` inclusive.

This is the "hello world" of segment trees — and the exact problem [FenwickTree §9.5](/pattern/fenwick-tree#95-worked-leetcode-problems) also solves, which is the whole lesson: **when the aggregate is just a sum, a BIT is shorter. The segment tree earns its extra code only when you need min/max/assign.** We use the iterative tree from Section 3 because point-update + range-sum is exactly its sweet spot.

```python
class NumArray:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (2 * self.n)
        for i, v in enumerate(nums):            # leaves live at [n, 2n)
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):      # build internal nodes bottom-up
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index, val):
        i = index + self.n
        self.tree[i] = val                      # ASSIGN the leaf (not += a delta)
        i //= 2
        while i >= 1:                            # re-pull every ancestor
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
            i //= 2

    def sumRange(self, left, right):
        res = 0
        l, r = left + self.n, right + self.n + 1  # half-open [l, r)
        while l < r:
            if l & 1: res += self.tree[l]; l += 1
            if r & 1: r -= 1; res += self.tree[r]
            l //= 2; r //= 2
        return res
```

**Trace** on `nums = [1, 3, 5]` (leaves at indices 3,4,5; internal 1,2):

```
build:  tree[3..5] = 1,3,5
        tree[2] = tree[4]+tree[5] = 3+5 = 8
        tree[1] = tree[2]+tree[3] = 8+1 = 9

sumRange(0,2): l=3, r=6
  l=3 odd  -> res=1, l=4        (leaf 0 grabbed directly)
  l=4 even, r=6 even
  l=2, r=3
  l=2 even, r=3 odd -> r=2, res += tree[2]=8 -> res=9
  l=1, r=1 stop  => 9   ✓

update(1, 2): leaf 4 = 2; tree[2]=2+5=7; tree[1]=7+1=8
sumRange(0,2) now => 8   ✓
```

`★ Insight ─────────────────────────────────────`
The point-update here **assigns** (`self.tree[i] = val`) — unlike a BIT, whose `update` adds a *delta* and therefore needs `delta = val - old[index]` plus a shadow copy of the array. The segment-tree leaf holds the absolute value, so it can overwrite in place with no shadow array. That is a small but real ergonomic win of the iterative segment tree over a BIT for the "set element = value" flavor of update.
`─────────────────────────────────────────────────`

### Problem 699 — Falling Squares

**Difficulty**: Hard

**Statement.** Squares drop one at a time onto a number line. Square `i` is given as `positions[i] = [left, sideLength]`, occupying the interval `[left, left + sideLength - 1]` horizontally. A falling square lands on top of the tallest surface currently under any part of its footprint (the ground is height 0), so its new top height is `(max height under footprint) + sideLength`. After each drop, report the tallest stack seen so far. Return the list of running maxima.

This is the canonical LeetCode teacher for **lazy range-assign-max**. Coordinates go up to 1e8, so we coordinate-compress the endpoints first (Section 7's companion technique), then run a recursive lazy tree whose merge is `max`.

```python
def fallingSquares(positions):
    xs = set()                                   # compress interval endpoints
    for l, s in positions:
        xs.add(l); xs.add(l + s - 1)
    order = sorted(xs)
    idx = {v: i for i, v in enumerate(order)}
    n = len(order)
    tree = [0] * (4 * n)
    lazy = [0] * (4 * n)                          # pending "height is at least this"

    def apply(node, val):
        tree[node] = max(tree[node], val)        # pull-up merge AND lazy-merge are both max
        lazy[node] = max(lazy[node], val)
    def push(node):
        if lazy[node]:
            apply(2 * node, lazy[node]); apply(2 * node + 1, lazy[node])
            lazy[node] = 0
    def update(node, lo, hi, l, r, val):
        if r < lo or hi < l: return
        if l <= lo and hi <= r:
            apply(node, val); return             # whole node covered: assign-max, stop
        push(node); mid = (lo + hi) // 2
        update(2 * node, lo, mid, l, r, val)
        update(2 * node + 1, mid + 1, hi, l, r, val)
        tree[node] = max(tree[2 * node], tree[2 * node + 1])
    def query(node, lo, hi, l, r):
        if r < lo or hi < l: return 0
        if l <= lo and hi <= r: return tree[node]
        push(node); mid = (lo + hi) // 2
        return max(query(2 * node, lo, mid, l, r),
                   query(2 * node + 1, mid + 1, hi, l, r))

    res = []; best = 0
    for l, s in positions:
        a, b = idx[l], idx[l + s - 1]
        newh = query(1, 0, n - 1, a, b) + s      # land on tallest under footprint
        update(1, 0, n - 1, a, b, newh)          # raise the whole footprint to newh
        best = max(best, newh)
        res.append(best)
    return res
```

**Trace** on `positions = [[1,2],[2,3],[6,1]]`:

```
endpoints: sq0 [1,2], sq1 [2,4], sq2 [6,6]  ->  compressed {1,2,4,6}

sq0 [1,2]: query footprint = 0, newh = 0+2 = 2, assign-max 2 over [1,2]. best=2
sq1 [2,4]: query footprint (covers x=2, held by sq0 at h=2) = 2,
           newh = 2+3 = 5, assign-max 5 over [2,4].                 best=5
sq2 [6,6]: query footprint = 0 (empty column), newh = 0+1 = 1.      best=5
=> [2, 5, 5]   ✓
```

`★ Insight ─────────────────────────────────────`
Assign-max is the *easy* lazy flavor: `max` is idempotent, so a leftover stale lazy re-applied to a node changes nothing, and `0` is a safe "no pending" sentinel — no `has_lazy` flag needed (contrast the assign-*sum* variant in §5, where lazy `0` is ambiguous with "assign the value 0"). The problem shape "each new item sits on the current max under its span, then raises that span" — stacking boxes, booking the tallest hotel floor in a range — is the fingerprint that says lazy assign-max.
`─────────────────────────────────────────────────`

### Problem 327 — Count of Range Sums

**Difficulty**: Hard

**Statement.** Given an integer array `nums` and two integers `lower` and `upper`, return the number of range sums `S(i, j) = nums[i] + ... + nums[j]` (with `i <= j`) that lie in `[lower, upper]` inclusive.

The reframe is the whole solution. With prefix sums `P[0..n]`, a range sum `S(i,j) = P[j+1] - P[i]`. Counting `lower <= P[j+1] - P[i] <= upper` over all `i <= j` becomes: sweep the prefixes left to right, and for each new prefix `p`, count how many **already-seen** prefixes `P[i]` satisfy `p - upper <= P[i] <= p - lower`. That is a value-range count over a value-indexed tree — Section 7's pattern, done here with the shorter BIT counting form.

```python
from bisect import bisect_left, bisect_right

def countRangeSum(nums, lower, upper):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)

    order = sorted(set(prefix))                  # compress prefix VALUES
    rank = {v: i for i, v in enumerate(order)}
    m = len(order)
    tree = [0] * (m + 1)                         # value-indexed count BIT (1-indexed)

    def upd(i):
        i += 1
        while i <= m: tree[i] += 1; i += i & (-i)
    def qpre(i):                                 # count inserted with rank in [0, i]
        i += 1; s = 0
        while i > 0: s += tree[i]; i -= i & (-i)
        return s
    def qrange(loval, hival):                    # count inserted prefix values in [loval, hival]
        li = bisect_left(order, loval)           # first rank whose value >= loval
        ri = bisect_right(order, hival) - 1      # last  rank whose value <= hival
        if li > ri: return 0
        return qpre(ri) - (qpre(li - 1) if li > 0 else 0)

    count = 0
    for p in prefix:
        count += qrange(p - upper, p - lower)    # earlier prefixes making a valid range END here
        upd(rank[p])                             # then register p as a candidate start
    return count
```

**Trace** on `nums = [-2, 5, -1]`, `lower = -2`, `upper = 2`:

```
prefix = [0, -2, 3, 2]

p=0:  need earlier P[i] in [0-2, 0+2]=[-2,2] -> none inserted yet -> 0.   insert 0
p=-2: need P[i] in [-4, 0]        -> {0} qualifies                -> +1.  insert -2
p=3:  need P[i] in [1, 5]         -> {0,-2}? none in [1,5]        -> 0.    insert 3
p=2:  need P[i] in [0, 4]         -> {0, 3} qualify (0 and 3)     -> +2.   insert 2
total = 3   ✓   (ranges [0,0]=-2, [2,2]=-1, [0,2]=2)
```

`★ Insight ─────────────────────────────────────`
The counting axis is the **prefix value**, not the array index — the tree never knows where in the array a prefix came from, only its magnitude. The `i <= j` (earlier-index) constraint is enforced purely by **when** you insert: query for the answer *before* inserting the current prefix, so only strictly-earlier prefixes are in the tree. That "query-then-insert" ordering is the same trick behind counting inversions and "count smaller after self" — the sweep direction encodes the index constraint for free. And because we only count (never min/max), a BIT replaces the segment tree with less code.
`─────────────────────────────────────────────────`

---

## 10. Common Patterns Collection

### Range Sum with Point Updates (CSES "Dynamic Range Sum Queries")

Basic tree (Section 2) or BIT (Section 9). Read updates and `?` queries, dispatch.

### Range Minimum with Point Updates (CSES "Dynamic Range Minimum Queries")

Same skeleton, `combine = min`, `identity = +inf` (Section 4).

### Range Add + Range Sum (CSES "Range Update Queries")

Lazy propagation, range-add flavor (Section 5).

### Range Assign + Range Sum

Lazy propagation, assign flavor with a `has_lazy` flag (Section 5).

### K-th Element / Order Statistics

Value-indexed tree with count leaves + `find_first_ge` descent (Sections 6, 7).

### Count of Smaller Numbers After Self / Inversions

Value-indexed tree or BIT, sweep right-to-left (Section 7).

### Longest / Max-Subarray in Range

Store a struct per node `(total, best_prefix, best_suffix, best)`; merge is associative but not commutative — use the two-accumulator query (Section 4).

```python
def merge(a, b):
    total = a.total + b.total
    best_prefix = max(a.best_prefix, a.total + b.best_prefix)
    best_suffix = max(b.best_suffix, b.total + a.best_suffix)
    best = max(a.best, b.best, a.best_suffix + b.best_prefix)
    return Node(total, best_prefix, best_suffix, best)
```

---

## 11. Pattern Recognition Cheat Sheet

### By Problem Signal

| You see... | Reach for | Section |
|------------|-----------|---------|
| "Range sum, updates in between" | Basic tree / BIT | [2](#2-basic-segment-tree-recursive), [9](#9-when-to-use-a-bit-instead) |
| "Range min / max / gcd + updates" | Merge abstraction | [4](#4-the-merge-abstraction) |
| "Add x to all in [l, r]" | Lazy (range add) | [5](#5-lazy-propagation-range-updates) |
| "Set all in [l, r] to x" | Lazy (range assign) | [5](#5-lazy-propagation-range-updates) |
| "First index where prefix >= k" | Tree descent | [6](#6-binary-search-on-the-tree) |
| "K-th smallest / count in value range" | Value-indexed tree | [7](#7-segment-tree-on-values) |
| "Count inversions / smaller-after-self" | Value tree or BIT | [7](#7-segment-tree-on-values), [9](#9-when-to-use-a-bit-instead) |
| "K-th smallest in a range, many queries" | Persistent tree | [8](#8-persistent-segment-tree) |
| "Values up to 1e9, only N distinct" | Coordinate compression first | [7](#7-segment-tree-on-values) |

### The Universal Skeleton

Every segment tree is:

```
build:  leaf = data;  internal = combine(left, right)
update: change leaf (or mark lazy);  pull up ancestors
query:  tile [l, r] with O(log N) fully-covered nodes;  combine them
```

The only things that change between variants:

1. **combine** function + its **identity**
2. whether you carry **lazy** (range updates)
3. whether the index axis is **position** or **value**

### Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Array too small | Allocate `4 * n` (recursive) or `2 * n` (iterative) |
| Forgetting to push lazy before recursing | Always `_push_down` on partial overlap |
| Forgetting to pull up after child update | Recompute `tree[node]` after recursion |
| Assign-lazy of value 0 ignored | Use a separate `has_lazy` flag, not `lazy == 0` |
| Using BIT for range min | BIT needs invertible ops; min isn't — use segment tree |
| Non-commutative merge with one accumulator | Keep `resl` and `resr` separate |
| Off-by-one in iterative query | Query range is half-open `[l, r+1)` |

### Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(N) | O(N) |
| Point update | O(log N) | — |
| Range query | O(log N) | — |
| Range update (lazy) | O(log N) | — |
| Tree descent (find first) | O(log N) | — |
| Persistent update | O(log N) time, O(log N) new nodes | O(N log N) total |
| K-th in range (persistent) | O(log N) per query | O(N log N) |

---

## Practice Order

```
Start here
    │
    ▼
  307  (Easy)   ──── Range Sum Query Mutable: the basic point-update + range-sum tree (§2)
    │
    ▼
  RMQ  build/query ── Range Minimum Query: same skeleton, combine=min, identity=+inf (§4)
    │
    ▼
  315  (Hard*)  ──── Count of Smaller After Self: value-indexed tree, sweep right→left (§7)
    │              (*Hard-tagged but a gentle intro to the value-domain reframe)
    ▼
  Range-add lazy ──── Range Sum with range update: lazy propagation, add flavor (§5)
    │
    ▼
  732  (Hard)   ──── My Calendar III: lazy range-add + coordinate compression (§5, §7)
    │
    ▼
  699  (Hard)   ──── Falling Squares: lazy range-ASSIGN + compression, max query (§5, §7)
```

Worked in full in [§9.5](#95-worked-leetcode-problems): **307** (point-update, §2/§3), **699** (lazy assign-max, §5), **327** (value-indexed count, §7).

---

*Pattern mastered — one skeleton (build = combine children, update = change leaf then pull up, query = tile the range with O(log N) covered nodes), and two questions: (1) do I need lazy, i.e. range-updates? (2) is my index axis position or value? Sum-only, no range-update, invertible → a [BIT](/pattern/fenwick-tree) is shorter; min/max/assign/range-update → the segment tree is why you're here.*
