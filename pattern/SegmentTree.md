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
| Bitwise OR | `a | b` | `0` |

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

```python
def count_inversions(arr):
    # compress values to ranks 0..m-1
    ranks = {v: i for i, v in enumerate(sorted(set(arr)))}
    m = len(ranks)
    st = SegTreeIterative([0] * m)    # counts per value
    inversions = 0
    for x in reversed(arr):
        r = ranks[x]
        inversions += st.query(0, r - 1) if r > 0 else 0  # already-seen smaller values
        st.update(r, st.query(r, r) + 1)                  # record this value
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
