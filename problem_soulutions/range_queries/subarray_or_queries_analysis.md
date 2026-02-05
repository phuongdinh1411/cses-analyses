---
layout: simple
title: "Subarray OR Queries - Range Queries Problem"
permalink: /problem_soulutions/range_queries/subarray_or_queries_analysis
difficulty: Medium
tags: [range-queries, segment-tree, sparse-table, bitwise-operations]
---

# Subarray OR Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Segment Tree / Sparse Table |
| **CSES Link** | [Subarray OR Queries](https://cses.fi/problemset/task/2428) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand why bitwise OR is an idempotent operation suitable for sparse tables
- [ ] Implement a segment tree for range OR queries
- [ ] Implement a sparse table for O(1) range queries with O(n log n) preprocessing
- [ ] Choose between segment tree and sparse table based on problem requirements

---

## Problem Statement

**Problem:** Given an array of n integers, process q queries where each query asks for the bitwise OR of all elements in a subarray [l, r].

**Input:**
- Line 1: Two integers n and q (number of elements and queries)
- Line 2: n integers a_1, a_2, ..., a_n
- Next q lines: Two integers l and r for each query (1-indexed)

**Output:**
- For each query, print the bitwise OR of elements in the range [l, r]

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 0 <= a_i <= 10^9
- 1 <= l <= r <= n

### Example

```
Input:
5 3
1 2 3 4 5
1 3
2 4
1 5

Output:
3
7
7
```

**Explanation:**
- Query 1: OR(1, 2, 3) = 1 | 2 | 3 = 01 | 10 | 11 = 11 = 3
- Query 2: OR(2, 3, 4) = 2 | 3 | 4 = 010 | 011 | 100 = 111 = 7
- Query 3: OR(1, 2, 3, 4, 5) = 001 | 010 | 011 | 100 | 101 = 111 = 7

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What property of bitwise OR makes this problem efficiently solvable?

Bitwise OR is **associative** (a | (b | c) = (a | b) | c) and **idempotent** (a | a = a). This means:
1. We can combine results from subranges in any order
2. Overlapping ranges in sparse tables give correct results

### Breaking Down the Problem

1. **What are we looking for?** The bitwise OR of all elements in [l, r]
2. **What information do we have?** Static array with multiple queries
3. **What's the relationship between input and output?** OR accumulates bits - once a bit is set, it stays set

### Analogies

Think of bitwise OR like collecting stamps. Each element has certain "stamps" (set bits). The OR of a range tells you all unique stamps collected from that range. If you have stamps from [1,3] and stamps from [2,4], combining them (even with overlap at [2,3]) still gives you the correct set of all stamps.

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the range and compute the OR directly.

### Algorithm

1. For each query (l, r):
2. Initialize result = 0
3. For each index i from l to r, compute result |= arr[i]
4. Return result

### Code

```python
def solve_brute_force(n, arr, queries):
  """
  Brute force: compute OR for each query by iterating through range.

  Time: O(q * n) per query
  Space: O(1)
  """
  results = []
  for l, r in queries:
    or_result = 0
    for i in range(l - 1, r):  # Convert to 0-indexed
      or_result |= arr[i]
    results.append(or_result)
  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans up to n elements |
| Space | O(1) | Only stores current OR result |

### Why This Works (But Is Slow)

This correctly computes OR by examining every element, but with q = 2*10^5 queries and n = 2*10^5 elements, we get 4*10^10 operations - far too slow.

---

## Solution 2: Segment Tree

### Key Insight

> **The Trick:** Build a segment tree where each node stores the OR of its range. Query any range in O(log n).

### Data Structure

Each node in the segment tree stores the OR of all elements in its range.

| Node Property | Meaning |
|---------------|---------|
| `tree[node]` | OR of all elements in the range covered by this node |

### Merge Operation

```
tree[parent] = tree[left_child] | tree[right_child]
```

**Why?** OR is associative, so combining left and right subtree ORs gives the parent's OR.

### Dry Run Example

Let's trace through building the tree for arr = [1, 2, 3, 4, 5]:

```
Array (0-indexed): [1, 2, 3, 4, 5]
Binary:            [001, 010, 011, 100, 101]

Building segment tree (bottom-up):

Level 0 (leaves):     [1]   [2]   [3]   [4]   [5]   [0]   [0]   [0]
                       8     9    10    11    12    13    14    15

Level 1:           [1|2=3]  [3|4=7]  [5|0=5]  [0|0=0]
                      4        5        6        7

Level 2:          [3|7=7]           [5|0=5]
                     2                  3

Level 3 (root):           [7|5=7]
                             1

Query [2, 4] (1-indexed -> [1, 3] 0-indexed):
  - Start at root, range [0, 7]
  - Go to node 2 (range [0, 3]), need [1, 3]
  - Node 4 (range [0, 1]): partial overlap, need index 1 -> value 2
  - Node 5 (range [2, 3]): fully inside [1, 3] -> value 7
  - Result: 2 | 7 = 7
```

### Visual Diagram

```
                    [7] (root, range [0,7])
                   /   \
               [7]       [5]
              /   \     /   \
           [3]   [7]  [5]   [0]
           / \   / \
         [1] [2][3][4]  ...leaves...
```

### Code

```python
class SegmentTreeOR:
  """
  Segment Tree for range OR queries.

  Time: O(n) build, O(log n) query
  Space: O(n)
  """
  def __init__(self, arr):
    self.n = len(arr)
    self.size = 1
    while self.size < self.n:
      self.size *= 2

    # Tree array: size * 2 for complete binary tree
    self.tree = [0] * (2 * self.size)

    # Fill leaves
    for i in range(self.n):
      self.tree[self.size + i] = arr[i]

    # Build tree bottom-up
    for i in range(self.size - 1, 0, -1):
      self.tree[i] = self.tree[2 * i] | self.tree[2 * i + 1]

  def query(self, l, r):
    """Query OR in range [l, r] (0-indexed)."""
    result = 0
    l += self.size
    r += self.size

    while l <= r:
      if l % 2 == 1:  # l is right child
        result |= self.tree[l]
        l += 1
      if r % 2 == 0:  # r is left child
        result |= self.tree[r]
        r -= 1
      l //= 2
      r //= 2

    return result


def solve_segment_tree(n, arr, queries):
  st = SegmentTreeOR(arr)
  results = []
  for l, r in queries:
    results.append(st.query(l - 1, r - 1))  # Convert to 0-indexed
  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time (Build) | O(n) | Visit each node once |
| Time (Query) | O(log n) | Tree height is log n |
| Space | O(n) | Store 2n nodes |

---

## Solution 3: Sparse Table (Optimal for Static Arrays)

### Key Insight

> **The Trick:** Since OR is idempotent (a | a = a), overlapping ranges give correct results. We can answer queries in O(1)!

### Data Structure

| State | Meaning |
|-------|---------|
| `sparse[i][j]` | OR of 2^j elements starting at index i |

**In plain English:** sparse[i][j] = arr[i] | arr[i+1] | ... | arr[i + 2^j - 1]

### State Transition

```
sparse[i][j] = sparse[i][j-1] | sparse[i + 2^(j-1)][j-1]
```

**Why?** We combine two adjacent blocks of size 2^(j-1) to form a block of size 2^j.

### Query Strategy

For range [l, r], find the largest k where 2^k <= (r - l + 1), then:
```
answer = sparse[l][k] | sparse[r - 2^k + 1][k]
```

The two ranges may overlap, but since OR is idempotent, this is correct!

### Dry Run Example

Building sparse table for arr = [1, 2, 3, 4, 5]:

```
Initial (j=0, blocks of size 1):
sparse[0][0] = 1, sparse[1][0] = 2, sparse[2][0] = 3, sparse[3][0] = 4, sparse[4][0] = 5

j=1 (blocks of size 2):
sparse[0][1] = sparse[0][0] | sparse[1][0] = 1 | 2 = 3
sparse[1][1] = sparse[1][0] | sparse[2][0] = 2 | 3 = 3
sparse[2][1] = sparse[2][0] | sparse[3][0] = 3 | 4 = 7
sparse[3][1] = sparse[3][0] | sparse[4][0] = 4 | 5 = 5

j=2 (blocks of size 4):
sparse[0][2] = sparse[0][1] | sparse[2][1] = 3 | 7 = 7
sparse[1][2] = sparse[1][1] | sparse[3][1] = 3 | 5 = 7

Query [1, 4] (0-indexed [0, 3]):
  Length = 4, k = log2(4) = 2
  Result = sparse[0][2] | sparse[0][2] = 7 | 7 = 7

Query [2, 4] (0-indexed [1, 3]):
  Length = 3, k = log2(3) = 1 (floor)
  Result = sparse[1][1] | sparse[2][1] = 3 | 7 = 7
         (covers [1,2] and [2,3], overlap at index 2 is OK!)
```

### Code

```python
import math

class SparseTableOR:
  """
  Sparse Table for range OR queries.

  Time: O(n log n) build, O(1) query
  Space: O(n log n)
  """
  def __init__(self, arr):
    self.n = len(arr)
    self.LOG = max(1, self.n.bit_length())

    # sparse[i][j] = OR of 2^j elements starting at index i
    self.sparse = [[0] * self.LOG for _ in range(self.n)]

    # Base case: blocks of size 1
    for i in range(self.n):
      self.sparse[i][0] = arr[i]

    # Build sparse table
    for j in range(1, self.LOG):
      for i in range(self.n - (1 << j) + 1):
        self.sparse[i][j] = (self.sparse[i][j-1] |
                  self.sparse[i + (1 << (j-1))][j-1])

    # Precompute log values for O(1) query
    self.log_table = [0] * (self.n + 1)
    for i in range(2, self.n + 1):
      self.log_table[i] = self.log_table[i // 2] + 1

  def query(self, l, r):
    """Query OR in range [l, r] (0-indexed)."""
    length = r - l + 1
    k = self.log_table[length]
    return self.sparse[l][k] | self.sparse[r - (1 << k) + 1][k]


def solve_sparse_table(n, arr, queries):
  st = SparseTableOR(arr)
  results = []
  for l, r in queries:
    results.append(st.query(l - 1, r - 1))  # Convert to 0-indexed
  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time (Build) | O(n log n) | Fill n * log(n) table entries |
| Time (Query) | O(1) | Direct table lookup |
| Space | O(n log n) | Store sparse table |

---

## Common Mistakes

### Mistake 1: Forgetting 1-indexed to 0-indexed Conversion

```python
# WRONG
result = st.query(l, r)  # l, r are 1-indexed from input

# CORRECT
result = st.query(l - 1, r - 1)  # Convert to 0-indexed
```

**Problem:** CSES uses 1-indexed input, but arrays are 0-indexed.
**Fix:** Always subtract 1 from both l and r.

**Problem:** OR of large values can exceed int range in intermediate operations.
**Fix:** Use `long long` for all OR computations.

### Mistake 3: Incorrect Sparse Table Size

```python
# WRONG
LOG = int(math.log2(n))  # Missing +1

# CORRECT
LOG = n.bit_length()  # Correctly handles all sizes
```

**Problem:** Underestimating LOG can cause index out of bounds.
**Fix:** Use `bit_length()` or add 1 to floor(log2(n)).

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element query | `[5], query(1,1)` | 5 | OR of single element is itself |
| All zeros | `[0,0,0], query(1,3)` | 0 | 0 | 0 | 0 = 0 |
| Full range query | `[1,2,3], query(1,3)` | 3 | Tests root of segment tree |
| Adjacent elements | `[1,2], query(1,2)` | 3 | Minimum non-trivial case |
| Large values | `[10^9, 10^9]` | 10^9 | a | a = a (idempotent) |
| Powers of 2 | `[1,2,4,8], query(1,4)` | 15 | All bits set, no overlap |

---

## When to Use This Pattern

### Use Segment Tree When:
- Array has updates (point or range updates)
- Need to support multiple operations (OR, AND, sum)
- Query complexity of O(log n) is acceptable

### Use Sparse Table When:
- Array is static (no updates)
- Operation is idempotent (OR, AND, min, max, GCD)
- Need O(1) query time for many queries
- Memory for O(n log n) is available

### Pattern Recognition Checklist:
- [ ] Static array with range queries? -> **Consider Sparse Table**
- [ ] Idempotent operation (OR, AND, min, max, GCD)? -> **Sparse Table works**
- [ ] Need updates? -> **Must use Segment Tree**
- [ ] Associative but not idempotent (sum, XOR)? -> **Segment Tree or prefix sums**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Basic prefix sum, simpler than segment tree |
| [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) | Sparse table with min operation |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Range Xor Queries](https://cses.fi/problemset/task/1650) | XOR is associative but NOT idempotent, use prefix XOR |
| [Bitwise ORs of Subarrays (LeetCode 898)](https://leetcode.com/problems/bitwise-ors-of-subarrays/) | Count distinct OR values across all subarrays |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Range Update Queries](https://cses.fi/problemset/task/1651) | Lazy propagation in segment tree |
| [Polynomial Queries](https://cses.fi/problemset/task/1736) | Complex lazy propagation |

---

## Key Takeaways

1. **The Core Idea:** Bitwise OR is associative and idempotent, enabling both segment tree and sparse table solutions.
2. **Time Optimization:** From O(q*n) brute force to O(n log n + q) with sparse table.
3. **Space Trade-off:** Sparse table uses O(n log n) space for O(1) queries.
4. **Pattern:** This belongs to the "range query on idempotent operations" pattern.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement segment tree for OR queries from scratch
- [ ] Implement sparse table for OR queries from scratch
- [ ] Explain why overlapping ranges work in sparse tables (idempotency)
- [ ] Choose between segment tree and sparse table based on problem constraints
- [ ] Handle 1-indexed to 0-indexed conversion correctly

---

## Additional Resources

- [CP-Algorithms: Sparse Table](https://cp-algorithms.com/data_structures/sparse-table.html)
- [CP-Algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html)
- [CSES Range Xor Queries](https://cses.fi/problemset/task/1650) - Similar bitwise range query
