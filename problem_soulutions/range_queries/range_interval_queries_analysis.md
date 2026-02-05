---
layout: simple
title: "Range Interval Queries - Segment Tree with Lazy Propagation"
permalink: /problem_soulutions/range_queries/range_interval_queries_analysis
difficulty: Medium
tags: [segment-tree, lazy-propagation, range-queries, range-updates]
prerequisites: [segment_tree_basics, range_sum_queries]
---

# Range Interval Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Segment Tree with Lazy Propagation |
| **CSES Link** | [Range Update Queries](https://cses.fi/problemset/task/1651) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand lazy propagation and why it is needed for range updates
- [ ] Implement a segment tree that supports both range updates and range queries
- [ ] Apply the "push down" technique to propagate lazy values
- [ ] Recognize when lazy propagation is necessary vs. standard segment tree

---

## Problem Statement

**Problem:** Given an array of integers and multiple queries, process two types of operations efficiently:
1. **Range Update:** Set all elements in range [l, r] to value v
2. **Range Query:** Find the sum of elements in range [l, r]

**Input:**
- Line 1: n (number of elements), q (number of queries)
- Line 2: n integers (the initial array)
- Next q lines: Either "1 l r v" (range update) or "2 l r" (range query)

**Output:**
- For each query of type 2, print the sum of elements in range [l, r]

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- -10^9 <= arr[i], v <= 10^9
- 1 <= l <= r <= n

### Example

```
Input:
5 3
1 2 3 4 5
2 1 3
1 2 4 10
2 1 3

Output:
6
21
```

**Explanation:**
- Query 1: Sum of arr[1..3] = 1 + 2 + 3 = 6
- Update: Set arr[2..4] to 10: [1, 10, 10, 10, 5]
- Query 2: Sum of arr[1..3] = 1 + 10 + 10 = 21

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Why can't we use a simple segment tree?

A standard segment tree handles **point updates** in O(log n). But here we need **range updates** - setting multiple elements at once. Updating each element individually would cost O(n log n) per range update, which is too slow.

### Breaking Down the Problem

1. **What are we looking for?** Sum of elements in a range after multiple range updates
2. **What information do we have?** The ranges to update and query
3. **What's the relationship?** A range update affects all elements in that range uniformly

### The Lazy Propagation Insight

Think of lazy propagation like "procrastination with notes." Instead of immediately updating all affected nodes in the segment tree:
1. Mark the node with a "lazy" tag indicating "all elements below should be set to value v"
2. Only propagate this update when we actually need to visit the children

This defers work until absolutely necessary, reducing updates from O(n) to O(log n).

---

## Solution 1: Brute Force

### Idea

Process each operation directly on the array without any data structure.

### Algorithm

1. For range update: iterate through [l, r] and set each element to v
2. For range query: iterate through [l, r] and sum elements

### Code

```python
def brute_force(arr, queries):
  """
  Brute force solution - direct array manipulation.

  Time: O(q * n) per query
  Space: O(1) extra
  """
  results = []

  for query in queries:
    if query[0] == 1:  # Range update
      l, r, v = query[1] - 1, query[2] - 1, query[3]
      for i in range(l, r + 1):
        arr[i] = v
    else:  # Range query
      l, r = query[1] - 1, query[2] - 1
      results.append(sum(arr[l:r + 1]))

  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each operation touches up to n elements |
| Space | O(1) | No extra space needed |

### Why This Works (But Is Slow)

Correctness is guaranteed - we directly perform what's asked. But with n, q up to 2 x 10^5, this gives 4 x 10^10 operations, which is far too slow.

---

## Solution 2: Segment Tree with Lazy Propagation

### Key Insight

> **The Trick:** Don't update child nodes immediately. Instead, store a "lazy" value at parent nodes and only push it down when needed.

### Data Structure Design

| Component | Purpose |
|-----------|---------|
| `tree[node]` | Sum of elements in this node's range |
| `lazy[node]` | Pending update value (None = no pending update) |

**In plain English:** `lazy[node] = v` means "all elements in this subtree should be set to v, but I haven't done it yet."

### Core Operations

**Push Down (Propagate Lazy Values):**
```
push(node, start, end):
    if lazy[node] is not None:
        tree[node] = lazy[node] * (end - start + 1)  # Apply to current node
        if start != end:  # Pass to children
            lazy[left_child] = lazy[node]
            lazy[right_child] = lazy[node]
        lazy[node] = None  # Clear lazy flag
```

**Why?** Before visiting children, we must ensure current node's value is up-to-date.

### Dry Run Example

Let's trace through with `arr = [1, 2, 3, 4, 5]`:

```
Initial tree structure (sums at each node):
                [15]              <- root: sum of all
               /    \
            [6]      [9]          <- sum of [1,2,3] and [4,5]
           /   \    /   \
         [3]  [3]  [4]  [5]       <- sum of [1,2], [3], [4], [5]
        /  \
      [1]  [2]

Query: Sum of [1, 3] (indices 0-2)
  -> Traverse left subtree: get [6] = 1+2+3 = 6

Update: Set [2, 4] to 10 (indices 1-3)
  -> Mark nodes covering [1,3] with lazy=10
  -> After update, tree logically represents [1, 10, 10, 10, 5]

Query: Sum of [1, 3] (indices 0-2)
  -> Need to read nodes, so push down lazy values
  -> arr[0]=1, arr[1]=10, arr[2]=10
  -> Sum = 1 + 10 + 10 = 21
```

### Visual Diagram

```
Before Update:       After Update (lazy shown):
     [15]                  [?]
    /    \                /    \
  [6]    [9]           [?]    [?]
  /  \   / \           /  \   / \
[3] [3] [4][5]       [1] lazy lazy [5]
                          =10  =10
                     (covering indices 1-3)
```

### Code (Python)

```python
class LazySegmentTree:
  """
  Segment Tree with Lazy Propagation for range set updates and range sum queries.

  Time: O(log n) per operation
  Space: O(n)
  """

  def __init__(self, arr):
    self.n = len(arr)
    self.tree = [0] * (4 * self.n)
    self.lazy = [None] * (4 * self.n)
    self._build(arr, 1, 0, self.n - 1)

  def _build(self, arr, node, start, end):
    if start == end:
      self.tree[node] = arr[start]
    else:
      mid = (start + end) // 2
      self._build(arr, 2 * node, start, mid)
      self._build(arr, 2 * node + 1, mid + 1, end)
      self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

  def _push(self, node, start, end):
    """Push lazy value to current node and propagate to children."""
    if self.lazy[node] is not None:
      self.tree[node] = self.lazy[node] * (end - start + 1)
      if start != end:
        self.lazy[2 * node] = self.lazy[node]
        self.lazy[2 * node + 1] = self.lazy[node]
      self.lazy[node] = None

  def update_range(self, l, r, val):
    """Set all elements in [l, r] to val (0-indexed)."""
    self._update(1, 0, self.n - 1, l, r, val)

  def _update(self, node, start, end, l, r, val):
    self._push(node, start, end)

    if r < start or end < l:  # No overlap
      return

    if l <= start and end <= r:  # Complete overlap
      self.lazy[node] = val
      self._push(node, start, end)
      return

    # Partial overlap - recurse
    mid = (start + end) // 2
    self._update(2 * node, start, mid, l, r, val)
    self._update(2 * node + 1, mid + 1, end, l, r, val)
    self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

  def query_range(self, l, r):
    """Get sum of elements in [l, r] (0-indexed)."""
    return self._query(1, 0, self.n - 1, l, r)

  def _query(self, node, start, end, l, r):
    self._push(node, start, end)

    if r < start or end < l:  # No overlap
      return 0

    if l <= start and end <= r:  # Complete overlap
      return self.tree[node]

    # Partial overlap - recurse
    mid = (start + end) // 2
    left_sum = self._query(2 * node, start, mid, l, r)
    right_sum = self._query(2 * node + 1, mid + 1, end, l, r)
    return left_sum + right_sum


def solve(n, arr, queries):
  st = LazySegmentTree(arr)
  results = []

  for query in queries:
    if query[0] == 1:  # Range update
      l, r, v = query[1] - 1, query[2] - 1, query[3]
      st.update_range(l, r, v)
    else:  # Range query
      l, r = query[1] - 1, query[2] - 1
      results.append(st.query_range(l, r))

  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + q log n) | O(n) build + O(log n) per operation |
| Space | O(n) | Tree and lazy arrays each use O(n) |

---

## Common Mistakes

### Mistake 1: Forgetting to Push Before Accessing Children

```python
# WRONG
def _update(self, node, start, end, l, r, val):
  if r < start or end < l:
    return
  # Missing push() here!
  if l <= start and end <= r:
    ...
```

**Problem:** Children may have stale values from previous lazy updates.
**Fix:** Always call `push()` at the start of update and query operations.

### Mistake 2: Not Pushing Before Returning Node Value

```python
# WRONG
def _query(self, node, start, end, l, r):
  if l <= start and end <= r:
    return self.tree[node]  # May be stale!
```

**Problem:** The node value might not reflect pending lazy updates.
**Fix:** Call `push()` before accessing `tree[node]`.

### Mistake 3: Confusing Range Set vs Range Add

```python
# WRONG (for range SET)
self.tree[node] += val * (end - start + 1)

# CORRECT (for range SET)
self.tree[node] = val * (end - start + 1)
```

**Problem:** Range SET replaces values; range ADD accumulates.
**Fix:** Use `=` for set operations, `+=` for add operations.

**Problem:** Sum of 2 x 10^5 elements, each up to 10^9, exceeds int range.
**Fix:** Use `long long` for tree and lazy arrays.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | n=1, query [1,1] | arr[0] | Leaf node query |
| Full range query | query [1, n] | sum of all | Root node value |
| Adjacent updates | update [1,3], then [4,5] | Separate updates | Non-overlapping ranges |
| Overlapping updates | update [1,5], then [3,7] | Later update wins | Complete overwrite in overlap |
| Query after no updates | Just queries | Original sums | Initial array values |
| Large values | arr[i] = 10^9 | Use long long | Prevent overflow |

---

## When to Use This Pattern

### Use Lazy Propagation When:
- You have **range updates** (updating multiple elements at once)
- Updates apply a **uniform operation** to all elements in range (set, add, multiply)
- You need both updates and queries to be O(log n)

### Don't Use When:
- Only point updates are needed (standard segment tree suffices)
- Updates are not uniform (each element updated differently)
- Simple prefix sums can solve the problem (no updates, or only append)

### Pattern Recognition Checklist:
- [ ] Range updates present? --> Consider lazy propagation
- [ ] Updates uniform across range? --> Lazy propagation applies
- [ ] Need O(log n) for both update and query? --> Segment tree with lazy
- [ ] Only range queries, no updates? --> Sparse table or prefix sums

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Understand prefix sums |
| [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) | Basic segment tree with point updates |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Range Update Queries (CSES)](https://cses.fi/problemset/task/1651) | Range add instead of range set |
| [Range Sum Query - Mutable (LC 307)](https://leetcode.com/problems/range-sum-query-mutable/) | Point updates only |
| [Polynomial Queries (CSES)](https://cses.fi/problemset/task/1736) | More complex lazy propagation |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Range Minimum Queries II (CSES)](https://cses.fi/problemset/task/1649) | Lazy propagation for min queries |
| [Range Sum Query 2D - Mutable (LC 308)](https://leetcode.com/problems/range-sum-query-2d-mutable/) | 2D segment tree |
| [Salary Queries (CSES)](https://cses.fi/problemset/task/1144) | Segment tree with coordinate compression |

---

## Key Takeaways

1. **The Core Idea:** Defer range updates by storing "lazy" tags and only propagate when needed
2. **Time Optimization:** From O(n) per range update to O(log n) using lazy propagation
3. **Space Trade-off:** O(n) extra space for lazy array enables O(log n) operations
4. **Pattern:** Lazy propagation is essential for any range update + range query problem

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why lazy propagation is needed (vs. standard segment tree)
- [ ] Implement push/propagate operation correctly
- [ ] Handle both range SET and range ADD variants
- [ ] Identify when lazy propagation is overkill

---

## Additional Resources

- [CP-Algorithms: Segment Tree with Lazy Propagation](https://cp-algorithms.com/data_structures/segment_tree.html#lazy-propagation)
- [CSES Problem Set - Range Queries](https://cses.fi/problemset/list/)
- [Codeforces EDU: Segment Tree](https://codeforces.com/edu/course/2/lesson/4)
