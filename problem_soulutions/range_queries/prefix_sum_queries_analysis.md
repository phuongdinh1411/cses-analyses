---
layout: simple
title: "Prefix Sum Queries - Segment Tree with Custom Merge"
permalink: /problem_soulutions/range_queries/prefix_sum_queries_analysis
difficulty: Hard
tags: [segment-tree, prefix-sum, range-queries, point-update]
prerequisites: [dynamic_range_sum_queries, static_range_sum_queries]
---

# Prefix Sum Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Prefix Sum Queries](https://cses.fi/problemset/task/2166) |
| **Difficulty** | Hard |
| **Category** | Range Queries / Segment Tree |
| **Time Limit** | 1 second |
| **Key Technique** | Segment Tree with Custom Merge Function |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Design segment trees that store multiple values per node
- [ ] Implement custom merge functions for non-trivial range queries
- [ ] Combine prefix sums with maximum operations in a single structure
- [ ] Handle point updates while maintaining prefix sum properties

---

## Problem Statement

**Problem:** Given an array of n integers, process two types of queries:
1. **Update (type 1):** Change the value at position k to u
2. **Max prefix sum (type 2):** Find the maximum prefix sum in range [a, b]

A prefix sum at position i within range [a, b] is: sum(arr[a], arr[a+1], ..., arr[i]). **Empty prefixes (with sum 0) are allowed**, so the answer is never negative.

**Input:**
- Line 1: n (array size) and q (number of queries)
- Line 2: n integers (the initial array)
- Next q lines: Either "1 k u" (update) or "2 a b" (query)

**Output:** For each type 2 query, output the maximum prefix sum

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- -10^9 <= arr[i], u <= 10^9

### Example

```
Input:
8 4
1 2 -1 3 1 -5 1 4
2 2 6
1 4 -2
2 2 6
2 3 4

Output:
5
2
0
```

**Explanation:**
- Query `2 2 6`: Range [2, -1, 3, 1, -5], prefix sums [2, 1, 4, 5, 0]. Max = 5.
- Update `1 4 -2`: arr[4] becomes -2.
- Query `2 2 6`: Range [2, -1, -2, 1, -5], prefix sums [2, 1, -1, 0, -5]. Max = 2.
- Query `2 3 4`: Range [-1, -2], prefix sums [-1, -3]. Both are negative, so the empty prefix wins: 0.

---

## Intuition: How to Think About This Problem

### The Challenge

> **Key Question:** Why can't we use a simple segment tree with maximum values?

A prefix sum depends on **all elements before it** within the query range. We cannot simply store one value per segment.

### The Key Insight

When merging two segments [L, mid] and [mid+1, R]:
- Max prefix could be entirely in left segment
- OR it could extend through left into right segment

```
Left: sum=5, maxPrefix=7    Right: sum=3, maxPrefix=4

Merged maxPrefix = max(7, 5+4) = 9
                       ^    ^
                  left only | left.sum + right.maxPrefix
```

**Solution:** Store TWO values per node: (total_sum, max_prefix_sum)

---

## Solution 1: Brute Force

For each query, iterate through the range computing prefix sums.

```python
def solve_brute_force(arr, queries):
  results = []
  for query in queries:
    if query[0] == 1:  # Update
      arr[query[1] - 1] = query[2]
    else:  # Query
      a, b = query[1], query[2]
      max_prefix, curr = 0, 0  # empty prefix
      for i in range(a - 1, b):
        curr += arr[i]
        max_prefix = max(max_prefix, curr)
      results.append(max_prefix)
  return results
```

**Complexity:** O(q * n) time, O(1) space - Too slow for constraints.

---

## Solution 2: Segment Tree with Custom Merge

### Node Structure

| Field | Meaning |
|-------|---------|
| `total` | Sum of all elements in this segment |
| `max_prefix` | Maximum prefix sum from segment's left boundary, counting the empty prefix (so always >= 0) |

A leaf with value x is `(x, max(x, 0))`, and an empty segment is `(0, 0)`.

### Merge Function

```python
def merge(left, right):
  total = left.total + right.total
  max_prefix = max(left.max_prefix, left.total + right.max_prefix)
  return (total, max_prefix)
```

### Dry Run Example

Array `[3, -1, 4, -2]`:

```
Tree Structure:
                    [1-4]
                 (sum=4, max=6)
                /              \
           [1-2]               [3-4]
        (sum=2, max=3)      (sum=2, max=4)
         /       \            /       \
       [1]       [2]        [3]       [4]
    (3, 3)    (-1, 0)     (4, 4)   (-2, 0)

Query [2,4]:
  Combine [2] with [3-4]: merge((-1,0), (2,4))
  total = -1 + 2 = 1
  max_prefix = max(0, -1 + 4) = 3

Verify: arr[2..4] = [-1, 4, -2]
  Prefixes: (empty) 0, -1, 3, 1 -> Max = 3  [Correct]
```

### Code (Python)

```python
import sys

def solve():
  data = sys.stdin.read().split()
  idx = 0
  n, q = int(data[idx]), int(data[idx+1]); idx += 2

  arr = [0] + [int(data[idx+i]) for i in range(n)]; idx += n
  tree = [(0, 0)] * (4 * n)

  def merge(l, r):
    return (l[0] + r[0], max(l[1], l[0] + r[1]))

  def build(node, start, end):
    if start == end:
      tree[node] = (arr[start], max(arr[start], 0))
      return
    mid = (start + end) // 2
    build(2*node, start, mid)
    build(2*node+1, mid+1, end)
    tree[node] = merge(tree[2*node], tree[2*node+1])

  def update(node, start, end, pos, val):
    if start == end:
      tree[node] = (val, max(val, 0))
      return
    mid = (start + end) // 2
    if pos <= mid:
      update(2*node, start, mid, pos, val)
    else:
      update(2*node+1, mid+1, end, pos, val)
    tree[node] = merge(tree[2*node], tree[2*node+1])

  def query(node, start, end, l, r):
    if r < start or end < l:
      return (0, 0)
    if l <= start and end <= r:
      return tree[node]
    mid = (start + end) // 2
    return merge(query(2*node, start, mid, l, r),
          query(2*node+1, mid+1, end, l, r))

  build(1, 1, n)
  results = []

  for _ in range(q):
    t = int(data[idx]); idx += 1
    if t == 1:
      k, u = int(data[idx]), int(data[idx+1]); idx += 2
      update(1, 1, n, k, u)
    else:
      a, b = int(data[idx]), int(data[idx+1]); idx += 2
      results.append(query(1, 1, n, a, b)[1])

  print('\n'.join(map(str, results)))

if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | Build O(n), each operation O(log n) |
| Space | O(n) | Segment tree with 4n nodes |

---

## Common Mistakes

### Mistake 1: Storing Only Max Element

```python
# WRONG
def merge(left, right):
  return max(left, right)  # Finds max element, not max prefix sum
```

**Fix:** Store (total, max_prefix) tuple.

### Mistake 2: Wrong Merge Order

```python
# WRONG - order matters!
max_prefix = max(right[1], right[0] + left[1])  # Reversed!
```

**Fix:** Use `max(left.max_prefix, left.total + right.max_prefix)`.

### Mistake 3: Forgetting the Empty Prefix

```python
# WRONG - a range of only negatives returns a negative answer
tree[node] = (x, x)
return (0, float('-inf'))  # out of range

# CORRECT - CSES allows the empty prefix (sum 0)
tree[node] = (x, max(x, 0))
return (0, 0)  # out of range
```

**Fix:** Count the empty prefix in every node; then `(0, 0)` is also the correct identity. On the sample, query `2 3 4` must print 0, not -1.

### Mistake 4: Integer Overflow (C++)

Values up to 10^9, sums can reach 2 x 10^14. Use `long long`.

---

## Edge Cases

| Case | Input | Output | Why |
|------|-------|--------|-----|
| Single element | `query [1,1]` | max(arr[1], 0) | One element or the empty prefix |
| All negative | `[-5,-3,-1]` | 0 | Empty prefix best |
| All positive | `[1,2,3]` | 6 | Full range best |
| Large values | 10^9 | Use long long | Overflow prevention |

---

## When to Use This Pattern

**Use when:**
- Need max/min prefix sums over arbitrary ranges
- Point updates required
- O(log n) query complexity needed

**Don't use when:**
- Static queries only (sparse table simpler)
- Need max subarray sum (different segment tree structure)
- Range updates (need lazy propagation)

---

## Related Problems

### Easier (Do First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Basic prefix sums |
| [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) | Segment tree basics |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Range Update Queries](https://cses.fi/problemset/task/1651) | Lazy propagation |
| [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Kadane's algorithm |

### Harder (Do After)

| Problem | New Concept |
|---------|-------------|
| [Polynomial Queries](https://cses.fi/problemset/task/1736) | Complex lazy propagation |
| [Range Updates and Sums](https://cses.fi/problemset/task/1735) | Multiple update types |

---

## Key Takeaways

1. **Core Idea:** Store (total_sum, max_prefix_sum) per node for correct merging
2. **Time:** O(n) brute force per query -> O(log n) with segment tree
3. **Space:** O(4n) enables O(log n) operations
4. **Pattern:** When simple aggregation fails, ask "what extra info enables correct merging?"

---

## Practice Checklist

- [ ] Explain why both sum AND max_prefix are needed
- [ ] Derive the merge function from first principles
- [ ] Handle identity element correctly
- [ ] Extend to similar problems (max suffix sum)
