---
layout: simple
title: "Dynamic Range Sum Queries - Range Queries"
permalink: /problem_soulutions/range_queries/dynamic_range_sum_queries_analysis
difficulty: Medium
tags: [segment-tree, fenwick-tree, BIT, range-queries, point-update]
prerequisites: [static_range_sum_queries]
---

# Dynamic Range Sum Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Segment Tree / Fenwick Tree (BIT) |
| **CSES Link** | [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the difference between static and dynamic range queries
- [ ] Implement a Fenwick Tree (BIT) for point updates and prefix sums
- [ ] Implement a Segment Tree for point updates and range queries
- [ ] Choose between BIT and Segment Tree based on problem requirements
- [ ] Handle 1-indexed vs 0-indexed conversions correctly

---

## Problem Statement

**Problem:** Given an array of n integers, process q queries of two types:
1. **Update:** Set the value at position k to u
2. **Query:** Calculate the sum of elements in range [a, b]

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers (initial array values)
- Next q lines: Either `1 k u` (update) or `2 a b` (sum query)

**Output:**
- For each type 2 query, print the sum of elements in the given range

**Constraints:**
- 1 <= n, q <= 2 * 10^5
- 1 <= a_i <= 10^9
- 1 <= k <= n
- 1 <= a <= b <= n

### Example

```
Input:
8 4
3 2 4 5 1 1 5 3
2 1 4
2 5 6
1 3 1
2 1 4

Output:
14
2
11
```

**Explanation:**
- Query 1: sum([3,2,4,5]) = 14
- Query 2: sum([1,1]) = 2
- Update: arr[3] = 1 (was 4)
- Query 3: sum([3,2,1,5]) = 11

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently update elements AND query range sums?

The naive approach (O(n) per query) is too slow when we have up to 200,000 queries. We need a data structure that supports both operations in O(log n) time.

### Breaking Down the Problem

1. **What are we looking for?** Sum of elements in arbitrary ranges, with values that change
2. **What information do we have?** Initial array, sequence of updates and queries
3. **What's the relationship?** Each query depends on all previous updates

### Two Data Structure Options

| Feature | Fenwick Tree (BIT) | Segment Tree |
|---------|-------------------|--------------|
| Code complexity | Simpler | More complex |
| Space | O(n) | O(4n) |
| Constants | Faster in practice | Slightly slower |
| Flexibility | Point update + prefix sum | Any associative operation |

**For this problem:** Both work well. BIT is preferred for its simplicity.

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the range and sum elements directly.

### Code

```python
def solve_brute_force(n, arr, queries):
 results = []
 for query in queries:
  if query[0] == 1:  # Update
   k, u = query[1], query[2]
   arr[k - 1] = u  # Convert to 0-indexed
  else:  # Sum query
   a, b = query[1], query[2]
   results.append(sum(arr[a-1:b]))
 return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans up to n elements |
| Space | O(1) | No extra space beyond input |

### Why This Is Too Slow

With n = q = 200,000, we'd have 4 * 10^10 operations - far too slow for a 1-second limit.

---

## Solution 2: Fenwick Tree (Binary Indexed Tree)

### Key Insight

> **The Trick:** Use binary representation of indices to create a tree structure where each node stores a partial sum, enabling O(log n) updates and prefix queries.

### How BIT Works

The BIT uses a clever observation: any range sum [1, r] can be computed by adding O(log n) precomputed partial sums.

For index i, the BIT stores the sum of elements in range [i - LSB(i) + 1, i], where LSB(i) is the lowest set bit.

```
Index (binary):  1(001)  2(010)  3(011)  4(100)  5(101)  6(110)  7(111)  8(1000)
LSB:                1       2       1       4       1       2       1       8
Range covered:    [1,1]   [1,2]   [3,3]   [1,4]   [5,5]   [5,6]   [7,7]   [1,8]
```

### Algorithm

**For prefix sum query(r):**
1. Start with sum = 0, index = r
2. Add BIT[index] to sum
3. Move to index - LSB(index)
4. Repeat until index = 0

**For point update(k, delta):**
1. Start with index = k
2. Add delta to BIT[index]
3. Move to index + LSB(index)
4. Repeat while index <= n

### Dry Run Example

Let's trace through with `arr = [3, 2, 4, 5, 1, 1, 5, 3]`:

```
Initial BIT construction:
Index:    1    2    3    4    5    6    7    8
Value:    3    2    4    5    1    1    5    3
BIT:      3    5    4   14    1    2    5   24
         [1,1][1,2][3,3][1,4][5,5][5,6][7,7][1,8]

Query: sum(1, 4)
  = prefix(4) - prefix(0)
  = BIT[4] + BIT[0]  (4 -> 0 in one step since LSB(4)=4)
  = 14 + 0 = 14

Query: sum(5, 6)
  = prefix(6) - prefix(4)
  prefix(6): BIT[6] + BIT[4] = 2 + 14 = 16
  prefix(4): BIT[4] = 14
  = 16 - 14 = 2

Update: arr[3] = 1 (delta = 1 - 4 = -3)
  Update BIT[3]: 4 + (-3) = 1
  Update BIT[4]: 14 + (-3) = 11  (3 + LSB(3) = 4)
  Update BIT[8]: 24 + (-3) = 21  (4 + LSB(4) = 8)

BIT after update:
Index:    1    2    3    4    5    6    7    8
BIT:      3    5    1   11    1    2    5   21

Query: sum(1, 4)
  = prefix(4) = BIT[4] = 11
```

### Code (Python)

```python
import sys
from typing import List

def solve():
 input_data = sys.stdin.read().split()
 idx = 0
 n, q = int(input_data[idx]), int(input_data[idx + 1])
 idx += 2

 arr = [0] + [int(input_data[idx + i]) for i in range(n)]  # 1-indexed
 idx += n

 # Build BIT
 bit = [0] * (n + 1)
 for i in range(1, n + 1):
  bit[i] += arr[i]
  j = i + (i & -i)
  if j <= n:
   bit[j] += bit[i]

 def prefix_sum(r: int) -> int:
  """Sum of elements [1, r]"""
  total = 0
  while r > 0:
   total += bit[r]
   r -= r & -r  # Remove lowest set bit
  return total

 def update(k: int, delta: int) -> None:
  """Add delta to position k"""
  while k <= n:
   bit[k] += delta
   k += k & -k  # Add lowest set bit

 results = []
 for _ in range(q):
  query_type = int(input_data[idx])
  if query_type == 1:  # Update
   k, u = int(input_data[idx + 1]), int(input_data[idx + 2])
   delta = u - arr[k]
   arr[k] = u
   update(k, delta)
   idx += 3
  else:  # Sum query
   a, b = int(input_data[idx + 1]), int(input_data[idx + 2])
   results.append(prefix_sum(b) - prefix_sum(a - 1))
   idx += 3

 print('\n'.join(map(str, results)))

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | Build: O(n), each operation: O(log n) |
| Space | O(n) | BIT array of size n + 1 |

---

## Solution 3: Segment Tree

### When to Use Segment Tree Over BIT

Use Segment Tree when you need:
- Range updates (not just point updates)
- Non-invertible operations (min, max, GCD)
- More complex range queries

### Code (Python)

```python
import sys
from typing import List

class SegmentTree:
 def __init__(self, arr: List[int]):
  self.n = len(arr)
  self.tree = [0] * (4 * self.n)
  self._build(arr, 1, 0, self.n - 1)

 def _build(self, arr: List[int], node: int, start: int, end: int) -> None:
  if start == end:
   self.tree[node] = arr[start]
  else:
   mid = (start + end) // 2
   self._build(arr, 2 * node, start, mid)
   self._build(arr, 2 * node + 1, mid + 1, end)
   self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

 def update(self, idx: int, val: int) -> None:
  self._update(1, 0, self.n - 1, idx, val)

 def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
  if start == end:
   self.tree[node] = val
  else:
   mid = (start + end) // 2
   if idx <= mid:
    self._update(2 * node, start, mid, idx, val)
   else:
    self._update(2 * node + 1, mid + 1, end, idx, val)
   self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

 def query(self, l: int, r: int) -> int:
  return self._query(1, 0, self.n - 1, l, r)

 def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
  if r < start or end < l:
   return 0
  if l <= start and end <= r:
   return self.tree[node]
  mid = (start + end) // 2
  return (self._query(2 * node, start, mid, l, r) +
    self._query(2 * node + 1, mid + 1, end, l, r))

def solve():
 input_data = sys.stdin.read().split()
 idx = 0
 n, q = int(input_data[idx]), int(input_data[idx + 1])
 idx += 2

 arr = [int(input_data[idx + i]) for i in range(n)]
 idx += n

 st = SegmentTree(arr)
 results = []

 for _ in range(q):
  query_type = int(input_data[idx])
  if query_type == 1:  # Update (1-indexed input)
   k, u = int(input_data[idx + 1]) - 1, int(input_data[idx + 2])
   st.update(k, u)
   idx += 3
  else:  # Sum query (1-indexed input)
   a, b = int(input_data[idx + 1]) - 1, int(input_data[idx + 2]) - 1
   results.append(st.query(a, b))
   idx += 3

 print('\n'.join(map(str, results)))

if __name__ == "__main__":
 solve()
```

---

## Common Mistakes

### Mistake 1: Index Off-by-One

```python
# WRONG: Forgetting 1-indexed input
st.update(k, u)  # k is 1-indexed from input!

# CORRECT
st.update(k - 1, u)  # Convert to 0-indexed
```

### Mistake 2: Integer Overflow

### Mistake 3: BIT Update Delta vs Value

```python
# WRONG: Using value instead of delta
def update(k, new_value):
 bit[k] = new_value  # BIT stores partial sums, not direct values!

# CORRECT: Update with delta
def update(k, new_value):
 delta = new_value - arr[k]
 arr[k] = new_value
 # Add delta to BIT nodes
```

### Mistake 4: Segment Tree Size

```python
# WRONG: Tree too small
tree = [0] * (2 * n)

# CORRECT: Allocate 4n for safety
tree = [0] * (4 * n)  # Accounts for all levels of recursion
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Single element | n=1, query [1,1] | arr[1] | Minimal case |
| Full range | query [1,n] | total sum | Tests entire array |
| Single point query | query [k,k] | arr[k] | Range of length 1 |
| Large values | arr[i] = 10^9 | Correct sum | Integer overflow check |
| Many updates same position | Multiple updates to index k | Final value | Cumulative updates |

---

## When to Use This Pattern

### Use Fenwick Tree (BIT) When:
- Point updates + prefix/range sum queries
- Operations are invertible (addition, XOR)
- Code simplicity is preferred
- Memory efficiency matters

### Use Segment Tree When:
- Need range updates (use lazy propagation)
- Operations are not invertible (min, max, GCD)
- Need to store more complex information per node
- Problem requires segment tree specific operations

### Pattern Recognition Checklist:
- [ ] Dynamic updates to array elements? Consider BIT/Segment Tree
- [ ] Range queries after updates? BIT or Segment Tree
- [ ] Only point updates + range sum? BIT is simpler
- [ ] Range updates needed? Segment Tree with lazy propagation

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Prefix sums without updates |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Dynamic Range Minimum Queries](https://cses.fi/problemset/task/1649) | Min instead of sum (requires Segment Tree) |
| [Range Update Queries](https://cses.fi/problemset/task/1651) | Range updates instead of point updates |
| [Range Sum Query - Mutable (LC 307)](https://leetcode.com/problems/range-sum-query-mutable/) | Same problem on LeetCode |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Range Updates and Sums](https://cses.fi/problemset/task/1735) | Lazy propagation |
| [Polynomial Queries](https://cses.fi/problemset/task/1736) | Complex range updates |
| [Range Queries and Copies](https://cses.fi/problemset/task/1737) | Persistent data structures |

---

## Key Takeaways

1. **The Core Idea:** Use tree-based data structures to precompute partial results, enabling O(log n) operations
2. **Time Optimization:** From O(n) per query to O(log n) using BIT or Segment Tree
3. **Space Trade-off:** O(n) extra space for the tree structure
4. **Pattern:** Dynamic range queries - when both updates and queries are frequent

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement BIT from scratch without reference
- [ ] Implement Segment Tree from scratch without reference
- [ ] Explain how the lowest set bit trick works in BIT
- [ ] Convert between 0-indexed and 1-indexed correctly
- [ ] Choose BIT vs Segment Tree based on problem requirements

---

## Additional Resources

- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CP-Algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html)
- [CSES Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Point update range query
