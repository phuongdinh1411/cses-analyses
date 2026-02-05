---
layout: simple
title: "Static Range Minimum Queries - Sparse Table"
permalink: /problem_soulutions/range_queries/static_range_minimum_queries_analysis
difficulty: Medium
tags: [sparse-table, range-queries, rmq, preprocessing]
prerequisites: [prefix_sums, bit_manipulation]
---

# Static Range Minimum Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Sparse Table |
| **CSES Link** | [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the Sparse Table data structure and its construction
- [ ] Apply Sparse Table to answer Range Minimum Queries (RMQ) in O(1) time
- [ ] Recognize when Sparse Table is preferred over Segment Trees
- [ ] Implement efficient preprocessing using dynamic programming on intervals

---

## Problem Statement

**Problem:** Given a static array of n integers, answer q queries. Each query asks for the minimum value in a given range [a, b].

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers (the array elements)
- Next q lines: Two integers a and b (1-indexed range boundaries)

**Output:**
- For each query, print the minimum value in range [a, b]

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 1 <= x_i <= 10^9
- 1 <= a <= b <= n

### Example

```
Input:
8 4
3 2 4 5 1 1 5 3
2 4
5 6
1 8
3 3

Output:
2
1
1
4
```

**Explanation:**
- Query [2,4]: Elements are [2, 4, 5], minimum = 2
- Query [5,6]: Elements are [1, 1], minimum = 1
- Query [1,8]: All elements, minimum = 1
- Query [3,3]: Single element [4], minimum = 4

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we precompute information to answer arbitrary range minimum queries in O(1)?

The key insight is that minimum is an **idempotent** operation: min(a, a) = a. This means we can overlap ranges without affecting the result. Unlike sum queries where overlapping causes double-counting, taking the minimum of overlapping ranges still gives the correct answer.

### Breaking Down the Problem

1. **What are we looking for?** The minimum element in any arbitrary range [l, r]
2. **What information do we have?** A static array (no updates)
3. **What's the relationship between input and output?** We need fast random access to precomputed minimums over power-of-2 length ranges

### Analogies

Think of a Sparse Table like having pre-solved answers for ranges of specific sizes (1, 2, 4, 8, ...). When someone asks "what's the minimum from position 3 to 10?", instead of scanning all 8 elements, we can combine two pre-solved answers: one covering positions 3-6 (length 4) and one covering positions 7-10 (length 4). Since they overlap and minimum doesn't mind overlap, we get the answer instantly.

---

## Solution 1: Brute Force

### Idea

For each query, iterate through all elements in the range and find the minimum.

### Algorithm

1. Read the query range [l, r]
2. Initialize result as infinity
3. Scan from index l to r, tracking minimum
4. Return the minimum found

### Code

```python
def solve_brute_force(arr, queries):
 """
 Brute force solution - scan each range.

 Time: O(q * n) per query set
 Space: O(1) auxiliary
 """
 results = []
 for l, r in queries:
  min_val = float('inf')
  for i in range(l - 1, r):  # Convert to 0-indexed
   min_val = min(min_val, arr[i])
  results.append(min_val)
 return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans up to n elements |
| Space | O(1) | No additional space needed |

### Why This Works (But Is Slow)

This approach correctly finds the minimum by exhaustive search, but with q and n both up to 2 x 10^5, we'd have up to 4 x 10^10 operations - far too slow.

---

## Solution 2: Optimal Solution - Sparse Table

### Key Insight

> **The Trick:** Precompute minimums for all ranges of length 2^k. Any range [l, r] can be covered by at most two overlapping power-of-2 ranges.

### Data Structure Definition

| State | Meaning |
|-------|---------|
| `st[i][j]` | Minimum value in range [i, i + 2^j - 1] |
| `log[len]` | Floor of log2(len), precomputed for quick lookup |

**In plain English:** `st[i][j]` stores the minimum of 2^j consecutive elements starting at index i.

### State Transition

```
st[i][j] = min(st[i][j-1], st[i + 2^(j-1)][j-1])
```

**Why?** A range of length 2^j can be split into two halves of length 2^(j-1). The minimum of the whole range is the minimum of the two halves.

### Visual Diagram: Building the Sparse Table

```
Array: [3, 2, 4, 5, 1, 1, 5, 3]
Index:  0  1  2  3  4  5  6  7

j=0 (length 1): Each element itself
st[i][0] = arr[i]
[3] [2] [4] [5] [1] [1] [5] [3]

j=1 (length 2): Pairs of adjacent elements
st[i][1] = min(st[i][0], st[i+1][0])
[2]  [2]  [4]  [1]  [1]  [1]  [3]
 |    |    |    |    |    |    |
3,2  2,4  4,5  5,1  1,1  1,5  5,3

j=2 (length 4): Groups of 4 elements
st[i][2] = min(st[i][1], st[i+2][1])
[2]   [1]   [1]   [1]   [1]
 |     |     |     |     |
3,2,  2,4,  4,5,  5,1,  1,1,
4,5   5,1   1,1   1,5   5,3

j=3 (length 8): Entire array
st[0][3] = min(st[0][2], st[4][2]) = min(2, 1) = 1
```

### Query Process: Answering [l, r]

```
Query [2, 7] (0-indexed: [1, 6])
Length = 6
k = floor(log2(6)) = 2  (largest power of 2 <= 6 is 4)

Cover with two ranges of length 4:
Range 1: [1, 4] = st[1][2] = 1
Range 2: [3, 6] = st[3][2] = 1  (6 - 4 + 1 = 3)

        Indices: 0  1  2  3  4  5  6  7
        Array:  [3, 2, 4, 5, 1, 1, 5, 3]
                   |--------|           Range 1: st[1][2]
                         |--------|     Range 2: st[3][2]
                   ^-----------^
                   Query range [1,6]

Answer = min(1, 1) = 1
```

### Dry Run Example

Let's trace through with input `n = 8, arr = [3, 2, 4, 5, 1, 1, 5, 3]`:

```
Building Sparse Table:

Step 1: Initialize j=0 (length 1)
  st[0][0]=3, st[1][0]=2, st[2][0]=4, st[3][0]=5
  st[4][0]=1, st[5][0]=1, st[6][0]=5, st[7][0]=3

Step 2: Build j=1 (length 2)
  st[0][1] = min(st[0][0], st[1][0]) = min(3,2) = 2
  st[1][1] = min(st[1][0], st[2][0]) = min(2,4) = 2
  st[2][1] = min(st[2][0], st[3][0]) = min(4,5) = 4
  st[3][1] = min(st[3][0], st[4][0]) = min(5,1) = 1
  st[4][1] = min(st[4][0], st[5][0]) = min(1,1) = 1
  st[5][1] = min(st[5][0], st[6][0]) = min(1,5) = 1
  st[6][1] = min(st[6][0], st[7][0]) = min(5,3) = 3

Step 3: Build j=2 (length 4)
  st[0][2] = min(st[0][1], st[2][1]) = min(2,4) = 2
  st[1][2] = min(st[1][1], st[3][1]) = min(2,1) = 1
  st[2][2] = min(st[2][1], st[4][1]) = min(4,1) = 1
  st[3][2] = min(st[3][1], st[5][1]) = min(1,1) = 1
  st[4][2] = min(st[4][1], st[6][1]) = min(1,3) = 1

Step 4: Build j=3 (length 8)
  st[0][3] = min(st[0][2], st[4][2]) = min(2,1) = 1

Query [2, 4] (0-indexed: [1, 3]):
  length = 3, k = floor(log2(3)) = 1
  left_range:  st[1][1] = 2  (covers [1,2])
  right_range: st[2][1] = 4  (covers [2,3])
  Answer = min(2, 4) = 2
```

### Code (Python)

```python
import sys
from math import log2

def solve():
 input_data = sys.stdin.read().split()
 idx = 0
 n, q = int(input_data[idx]), int(input_data[idx + 1])
 idx += 2

 arr = [int(input_data[idx + i]) for i in range(n)]
 idx += n

 # Precompute log values
 LOG = [0] * (n + 1)
 for i in range(2, n + 1):
  LOG[i] = LOG[i // 2] + 1

 # Build sparse table
 K = LOG[n] + 1
 st = [[0] * K for _ in range(n)]

 # Initialize for length 1 (j = 0)
 for i in range(n):
  st[i][0] = arr[i]

 # Build for lengths 2^j
 for j in range(1, K):
  for i in range(n - (1 << j) + 1):
   st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])

 # Answer queries
 results = []
 for _ in range(q):
  l, r = int(input_data[idx]) - 1, int(input_data[idx + 1]) - 1
  idx += 2

  length = r - l + 1
  k = LOG[length]
  ans = min(st[l][k], st[r - (1 << k) + 1][k])
  results.append(ans)

 print('\n'.join(map(str, results)))

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time (Build) | O(n log n) | Fill n x log(n) table |
| Time (Query) | O(1) | Two table lookups and min |
| Space | O(n log n) | Sparse table storage |

---

## Common Mistakes

### Mistake 1: Incorrect Log Calculation

```python
# WRONG - using ceiling instead of floor
k = math.ceil(math.log2(length))

# CORRECT - need floor to ensure 2^k <= length
k = int(math.log2(length))  # or use precomputed table
```

**Problem:** Using ceiling can give k where 2^k > length, causing out-of-bounds access.
**Fix:** Always use floor(log2) or precompute a log table.

### Mistake 2: Wrong Second Range Start Index

```python
# WRONG
right_start = r - (1 << k)

# CORRECT
right_start = r - (1 << k) + 1
```

**Problem:** The range [right_start, right_start + 2^k - 1] must end at r.
**Fix:** If it ends at r, then right_start = r - 2^k + 1.

### Mistake 3: Forgetting 1-Indexed to 0-Indexed Conversion

```python
# WRONG - using 1-indexed directly
ans = min(st[l][k], st[r - (1 << k) + 1][k])

# CORRECT - convert first
l -= 1
r -= 1
ans = min(st[l][k], st[r - (1 << k) + 1][k])
```

**Problem:** CSES uses 1-indexed input; accessing st[n] causes index out of bounds.
**Fix:** Always convert to 0-indexed before table access.

### Mistake 4: Insufficient Table Size

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `n=1, query [1,1]` | arr[0] | Range of size 1 |
| Entire array | `query [1,n]` | Global minimum | Uses largest precomputed range |
| Adjacent elements | `query [i,i+1]` | min(arr[i], arr[i+1]) | Uses j=1 level |
| Same value repeated | `[5,5,5,5]` | 5 | All minimums are 5 |
| All distinct | `[1,2,3,...,n]` | Leftmost in range | First element for sorted ascending |

---

## When to Use This Pattern

### Use Sparse Table When:
- Array is **static** (no updates)
- Need O(1) query time after preprocessing
- Operation is **idempotent** (min, max, GCD, AND, OR)
- Many queries on the same array (q is large)

### Don't Use Sparse Table When:
- Array has **updates** (use Segment Tree instead)
- Operation is **not idempotent** (sum, product - use Segment Tree)
- Memory is very limited (Sparse Table uses O(n log n) space)
- Only a few queries (brute force might be simpler)

### Pattern Recognition Checklist:
- [ ] Static array with no updates? --> **Sparse Table candidate**
- [ ] Idempotent operation (min, max, gcd)? --> **Sparse Table works**
- [ ] Need O(1) queries? --> **Sparse Table is optimal**
- [ ] Need to handle updates? --> **Use Segment Tree instead**

---

## Sparse Table vs Segment Tree

| Aspect | Sparse Table | Segment Tree |
|--------|--------------|--------------|
| Build Time | O(n log n) | O(n) |
| Query Time | O(1) | O(log n) |
| Update | Not supported | O(log n) |
| Space | O(n log n) | O(n) |
| Best For | Static RMQ | Dynamic RMQ |

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries (CSES)](https://cses.fi/problemset/task/1646) | Simpler prefix sum approach |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Range Minimum Query (SPOJ)](https://www.spoj.com/problems/RMQSQ/) | Same concept, different judge |
| [Static Range Maximum (variant)](https://cses.fi/problemset/task/1647) | Use max instead of min |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Dynamic Range Minimum Queries (CSES)](https://cses.fi/problemset/task/1649) | Adds point updates - need Segment Tree |
| [Range Update Queries (CSES)](https://cses.fi/problemset/task/1651) | Range updates with lazy propagation |
| [LCA using Sparse Table](https://cses.fi/problemset/task/1688) | Sparse Table on Euler tour for LCA |

---

## Key Takeaways

1. **The Core Idea:** Precompute minimums for all power-of-2 length ranges; any query can be answered by overlapping at most two such ranges.

2. **Time Optimization:** From O(n) per query to O(1) per query by spending O(n log n) preprocessing time.

3. **Space Trade-off:** Use O(n log n) extra space to achieve O(1) query time.

4. **Pattern:** Sparse Table is the go-to data structure for static RMQ and other idempotent range operations.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why overlapping ranges work for min but not for sum
- [ ] Build a Sparse Table from scratch without reference
- [ ] Derive the query formula: min(st[l][k], st[r - 2^k + 1][k])
- [ ] Implement in both Python and C++ under 15 minutes
- [ ] Identify problems where Sparse Table is better than Segment Tree

---

## Additional Resources

- [CP-Algorithms: Sparse Table](https://cp-algorithms.com/data_structures/sparse-table.html)
- [CSES Problem Set - Range Queries](https://cses.fi/problemset/list/)
- [TopCoder: Range Minimum Query and Lowest Common Ancestor](https://www.topcoder.com/thrive/articles/Range%20Minimum%20Query%20and%20Lowest%20Common%20Ancestor)
