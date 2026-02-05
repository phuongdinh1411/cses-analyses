---
layout: simple
title: "Static Range Minimum Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_minimum_queries_analysis
difficulty: Easy
tags: [sparse-table, range-queries, preprocessing, rmq]
prerequisites: []
---

# Static Range Minimum Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Sparse Table / RMQ |
| **CSES Link** | [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement the Sparse Table data structure
- [ ] Recognize problems suitable for Range Minimum Query (RMQ)
- [ ] Apply idempotent function optimization for O(1) queries
- [ ] Trade space for query speed with preprocessing

---

## Problem Statement

**Problem:** Given a static array of n integers and q queries, answer each query asking for the minimum element in a given range [a, b].

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers representing the array elements
- Next q lines: Two integers a and b representing query range (1-indexed)

**Output:**
- For each query, print the minimum element in range [a, b]

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

> **Key Question:** How can we answer range minimum queries faster than scanning the entire range each time?

The key insight is that minimum is an **idempotent** function: min(a, a) = a. This means overlapping ranges give the same answer, allowing us to precompute answers for power-of-2 length ranges and combine two overlapping ranges to answer any query in O(1).

### Breaking Down the Problem

1. **What are we looking for?** The minimum value within a given range
2. **What information do we have?** Static array (no updates), multiple queries
3. **What's the relationship between input and output?** min(range) can be computed from overlapping sub-ranges

### Analogies

Think of this like having pre-computed "summary cards" for your bookshelf. Instead of scanning all books to find the shortest one in a section, you have cards saying "shortest book in positions 1-2", "shortest in 1-4", "shortest in 1-8", etc. Any range query can be answered by looking at just two overlapping cards.

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the range and find the minimum element.

### Algorithm

1. Read the query range [l, r]
2. Iterate from index l to r
3. Track and return the minimum value found

### Code

```python
def solve_brute_force(arr, queries):
 """
 Brute force solution - scan each query range.

 Time: O(q * n) per query
 Space: O(1)
 """
 results = []
 for l, r in queries:
  min_val = arr[l - 1]  # Convert to 0-indexed
  for i in range(l - 1, r):
   min_val = min(min_val, arr[i])
  results.append(min_val)
 return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans up to n elements |
| Space | O(1) | No extra space needed |

### Why This Works (But Is Slow)

Correctness is guaranteed since we examine every element in the range. However, with q = 2 x 10^5 queries and n = 2 x 10^5 elements, this results in 4 x 10^10 operations - far too slow.

---

## Solution 2: Optimal Solution (Sparse Table)

### Key Insight

> **The Trick:** Precompute minimum for all ranges of power-of-2 lengths. Any range [l, r] can be covered by at most two overlapping power-of-2 ranges, and since min is idempotent, overlap does not affect the answer.

### Sparse Table Definition

| State | Meaning |
|-------|---------|
| `st[i][j]` | Minimum value in range starting at index i with length 2^j |

**In plain English:** st[i][j] stores the minimum of 2^j consecutive elements starting from position i.

### State Transition

```
st[i][j] = min(st[i][j-1], st[i + 2^(j-1)][j-1])
```

**Why?** A range of length 2^j can be split into two halves of length 2^(j-1). The minimum of the whole range is the minimum of the two halves.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `st[i][0]` | arr[i] | Range of length 2^0 = 1 contains only arr[i] |

### Algorithm

1. Build sparse table: For each power j from 1 to log(n), compute st[i][j] using previous power
2. For each query [l, r]: Find k = floor(log2(r - l + 1)), answer = min(st[l][k], st[r - 2^k + 1][k])

### Dry Run Example

Let's trace through with input `arr = [3, 2, 4, 5, 1, 1, 5, 3]`:

```
Building Sparse Table:

j = 0 (length 1): Copy array values
  st[0][0] = 3, st[1][0] = 2, st[2][0] = 4, st[3][0] = 5
  st[4][0] = 1, st[5][0] = 1, st[6][0] = 5, st[7][0] = 3

j = 1 (length 2): min of consecutive pairs
  st[0][1] = min(st[0][0], st[1][0]) = min(3, 2) = 2
  st[1][1] = min(st[1][0], st[2][0]) = min(2, 4) = 2
  st[2][1] = min(st[2][0], st[3][0]) = min(4, 5) = 4
  st[3][1] = min(st[3][0], st[4][0]) = min(5, 1) = 1
  st[4][1] = min(st[4][0], st[5][0]) = min(1, 1) = 1
  st[5][1] = min(st[5][0], st[6][0]) = min(1, 5) = 1
  st[6][1] = min(st[6][0], st[7][0]) = min(5, 3) = 3

j = 2 (length 4): min of length-2 ranges
  st[0][2] = min(st[0][1], st[2][1]) = min(2, 4) = 2
  st[1][2] = min(st[1][1], st[3][1]) = min(2, 1) = 1
  st[2][2] = min(st[2][1], st[4][1]) = min(4, 1) = 1
  st[3][2] = min(st[3][1], st[5][1]) = min(1, 1) = 1
  st[4][2] = min(st[4][1], st[6][1]) = min(1, 3) = 1

j = 3 (length 8): min of length-4 ranges
  st[0][3] = min(st[0][2], st[4][2]) = min(2, 1) = 1

Query [2, 4] (0-indexed: [1, 3]):
  length = 3, k = floor(log2(3)) = 1
  answer = min(st[1][1], st[3-2+1][1]) = min(st[1][1], st[2][1]) = min(2, 4) = 2

Query [1, 8] (0-indexed: [0, 7]):
  length = 8, k = floor(log2(8)) = 3
  answer = min(st[0][3], st[7-8+1][3]) = min(st[0][3], st[0][3]) = min(1, 1) = 1
```

### Visual Diagram

```
Array: [3, 2, 4, 5, 1, 1, 5, 3]
Index:  0  1  2  3  4  5  6  7

Sparse Table Visualization:
j=0: [3] [2] [4] [5] [1] [1] [5] [3]   <- length 1
j=1: [2]   [2]   [4]   [1]   [1]   [1]   [3]   <- length 2
j=2: [2]       [1]       [1]       [1]       <- length 4
j=3: [1]                                      <- length 8

Query [2,4] (indices 1-3, length 3):
        [2, 4, 5]
         ├──┤     st[1][1] = 2 (covers indices 1-2)
            ├──┤  st[2][1] = 4 (covers indices 2-3)
         └──┴──┘  Overlapping is OK! min(2, 4) = 2
```

### Code

```python
import math

def solve_sparse_table(arr, queries):
 """
 Optimal solution using Sparse Table.

 Time: O(n log n) preprocessing + O(1) per query
 Space: O(n log n)
 """
 n = len(arr)
 if n == 0:
  return []

 # Calculate log values for O(1) query
 LOG = max(1, n.bit_length())

 # Build sparse table
 st = [[0] * LOG for _ in range(n)]

 # Base case: length 1
 for i in range(n):
  st[i][0] = arr[i]

 # Fill for lengths 2^j
 for j in range(1, LOG):
  for i in range(n - (1 << j) + 1):
   st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])

 # Precompute log2 values for O(1) lookup
 log2 = [0] * (n + 1)
 for i in range(2, n + 1):
  log2[i] = log2[i // 2] + 1

 # Answer queries
 results = []
 for l, r in queries:
  l -= 1  # Convert to 0-indexed
  r -= 1
  length = r - l + 1
  k = log2[length]
  results.append(min(st[l][k], st[r - (1 << k) + 1][k]))

 return results


# Main function for CSES submission
def main():
 import sys
 input = sys.stdin.readline

 n, q = map(int, input().split())
 arr = list(map(int, input().split()))

 queries = []
 for _ in range(q):
  a, b = map(int, input().split())
  queries.append((a, b))

 results = solve_sparse_table(arr, queries)
 print('\n'.join(map(str, results)))


if __name__ == "__main__":
 main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n + q) | O(n log n) preprocessing, O(1) per query |
| Space | O(n log n) | Sparse table stores n * log(n) values |

---

## Common Mistakes

### Mistake 1: Off-by-One in Sparse Table Construction

**Problem:** The range [i, i + 2^j - 1] needs i + 2^j - 1 < n, which means i + 2^j <= n.
**Fix:** Use `<=` instead of `<` in the loop condition.

### Mistake 2: Wrong Query Formula

```python
# WRONG: Incorrect second range start
answer = min(st[l][k], st[r - (1 << k)][k])  # Bug!

# CORRECT
answer = min(st[l][k], st[r - (1 << k) + 1][k])
```

**Problem:** The second range should start at `r - 2^k + 1` to end exactly at r.
**Fix:** Add the +1 to ensure coverage of index r.

### Mistake 3: Forgetting 0-indexing Conversion

```python
# WRONG: Using 1-indexed values directly
results.append(min(st[l][k], st[r - (1 << k) + 1][k]))

# CORRECT: Convert first
l -= 1
r -= 1
results.append(min(st[l][k], st[r - (1 << k) + 1][k]))
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `n=1, query [1,1]` | arr[0] | Range contains only one element |
| Entire array | `query [1, n]` | global minimum | Maximum range query |
| Same element range | `query [i, i]` | arr[i-1] | Single element query |
| All same values | `[5,5,5,5]` | 5 | Any range returns same value |
| Descending array | `[5,4,3,2,1]` | rightmost in range | Minimum is at end of any range |

---

## When to Use This Pattern

### Use Sparse Table When:
- Array is static (no updates)
- Need to answer many range queries
- Query operation is idempotent (min, max, gcd)
- Need O(1) query time after preprocessing

### Don't Use When:
- Array has point updates (use Segment Tree instead)
- Query operation is not idempotent (sum requires Segment Tree)
- Memory is extremely limited (Sparse Table uses O(n log n) space)
- Only a few queries (brute force may be simpler)

### Pattern Recognition Checklist:
- [ ] Static array? -> **Consider Sparse Table**
- [ ] Idempotent operation (min/max/gcd)? -> **Sparse Table works**
- [ ] Need updates? -> **Use Segment Tree instead**
- [ ] Need sum queries? -> **Use Prefix Sums or Segment Tree**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Simpler range query with prefix sums |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Range Minimum Query (SPOJ)](https://www.spoj.com/problems/RMQSQ/) | Same problem, different judge |
| [Range Maximum Query](https://cses.fi/problemset/task/1647) | Same technique, different operation |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Dynamic Range Minimum Queries](https://cses.fi/problemset/task/1649) | Adds point updates, needs Segment Tree |
| [Range Update Queries](https://cses.fi/problemset/task/1651) | Range updates with lazy propagation |
| [Hotel Queries](https://cses.fi/problemset/task/1143) | Segment Tree with custom query |

---

## Key Takeaways

1. **The Core Idea:** Precompute answers for power-of-2 ranges; any range can be covered by two overlapping precomputed ranges.
2. **Time Optimization:** From O(n) per query to O(1) per query using O(n log n) preprocessing.
3. **Space Trade-off:** Use O(n log n) extra space to achieve O(1) query time.
4. **Pattern:** This is the classic Range Minimum Query (RMQ) problem, foundational for competitive programming.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a sparse table from scratch without reference
- [ ] Explain why overlapping ranges work for min but not for sum
- [ ] Calculate the time and space complexity
- [ ] Implement in both Python and C++ within 10 minutes

---

## Additional Resources

- [CP-Algorithms: Sparse Table](https://cp-algorithms.com/data_structures/sparse-table.html)
- [CSES Static Range Minimum Queries](https://cses.fi/problemset/task/1647) - Static RMQ problem
- [TopCoder Tutorial on RMQ](https://www.topcoder.com/thrive/articles/Range%20Minimum%20Query%20and%20Lowest%20Common%20Ancestor)
