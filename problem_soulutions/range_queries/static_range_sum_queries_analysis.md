---
layout: simple
title: "Static Range Sum Queries - Prefix Sums"
permalink: /problem_soulutions/range_queries/static_range_sum_queries_analysis
difficulty: Easy
tags: [prefix-sum, range-queries, arrays]
---

# Static Range Sum Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Prefix Sums |
| **CSES Link** | [Static Range Sum Queries](https://cses.fi/problemset/task/1646) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and implement the prefix sum technique
- [ ] Answer range sum queries in O(1) time after O(n) preprocessing
- [ ] Handle 1-indexed vs 0-indexed array conversions correctly
- [ ] Recognize when prefix sums are applicable to a problem

---

## Problem Statement

**Problem:** Given an array of n integers, answer q queries. Each query asks for the sum of elements in a range [a, b].

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers x_1, x_2, ..., x_n (the array elements)
- Next q lines: Two integers a and b (1-indexed range boundaries)

**Output:**
- q lines: The sum of elements in range [a, b] for each query

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
11
2
24
4
```

**Explanation:**
- Query [2,4]: arr[2] + arr[3] + arr[4] = 2 + 4 + 5 = 11
- Query [5,6]: arr[5] + arr[6] = 1 + 1 = 2
- Query [1,8]: Sum of all elements = 3+2+4+5+1+1+5+3 = 24
- Query [3,3]: arr[3] = 4

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we avoid recalculating sums from scratch for every query?

The naive approach recalculates the sum for each query by iterating through the range. With q queries and ranges up to size n, this gives O(q x n) time - too slow when both q and n are up to 2 x 10^5.

### The Prefix Sum Insight

If we precompute cumulative sums, any range sum becomes a simple subtraction:

```
sum(a, b) = prefix[b] - prefix[a-1]
```

Where `prefix[i]` = sum of elements from index 1 to i.

### Analogy

Think of prefix sums like odometer readings. To find the distance traveled between two points, you subtract the starting reading from the ending reading - no need to re-drive the route.

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the range and sum all elements.

### Code

```python
def solve_brute_force(n, arr, queries):
 """
 Brute force: sum each range directly.

 Time: O(q * n)
 Space: O(1)
 """
 results = []
 for a, b in queries:
  total = 0
  for i in range(a - 1, b):  # Convert to 0-indexed
   total += arr[i]
  results.append(total)
 return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | For each of q queries, sum up to n elements |
| Space | O(1) | No extra space beyond output |

### Why This Is Too Slow

With n = q = 2 x 10^5, we perform up to 4 x 10^10 operations - far exceeding the typical 10^8 operations per second limit.

---

## Solution 2: Prefix Sums (Optimal)

### Key Insight

> **The Trick:** Precompute cumulative sums so any range sum is just one subtraction.

### How Prefix Sums Work

| Array Index | 1 | 2 | 3 | 4 | 5 |
|-------------|---|---|---|---|---|
| **arr** | 3 | 2 | 4 | 5 | 1 |
| **prefix** | 3 | 5 | 9 | 14 | 15 |

`prefix[i]` stores the sum of arr[1..i].

### Range Sum Formula

```
sum(a, b) = prefix[b] - prefix[a-1]
```

**Why?** `prefix[b]` includes everything from 1 to b. Subtracting `prefix[a-1]` removes elements 1 to a-1, leaving exactly elements a to b.

### Dry Run Example

Let's trace through with `arr = [3, 2, 4, 5, 1]` and query `(2, 4)`:

```
Step 1: Build prefix array (1-indexed, prefix[0] = 0)
  prefix[0] = 0
  prefix[1] = prefix[0] + arr[1] = 0 + 3 = 3
  prefix[2] = prefix[1] + arr[2] = 3 + 2 = 5
  prefix[3] = prefix[2] + arr[3] = 5 + 4 = 9
  prefix[4] = prefix[3] + arr[4] = 9 + 5 = 14
  prefix[5] = prefix[4] + arr[5] = 14 + 1 = 15

  Final: prefix = [0, 3, 5, 9, 14, 15]

Step 2: Answer query (2, 4)
  sum(2, 4) = prefix[4] - prefix[1]
            = 14 - 3
            = 11

  Verify: arr[2] + arr[3] + arr[4] = 2 + 4 + 5 = 11  (Correct!)
```

### Visual Diagram

```
Array:     [3]  [2]  [4]  [5]  [1]
Index:      1    2    3    4    5

Prefix:    [3]  [5]  [9]  [14] [15]
            |         |    |
            |         +----+---> Query (2,4): prefix[4] - prefix[1]
            |              |                  = 14 - 3 = 11
            +--------------+
```

### Code (Python)

```python
import sys
input = sys.stdin.readline

def solve():
 n, q = map(int, input().split())
 arr = list(map(int, input().split()))

 # Build prefix sum array (1-indexed)
 prefix = [0] * (n + 1)
 for i in range(n):
  prefix[i + 1] = prefix[i] + arr[i]

 # Answer queries
 results = []
 for _ in range(q):
  a, b = map(int, input().split())
  results.append(prefix[b] - prefix[a - 1])

 print('\n'.join(map(str, results)))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + q) | O(n) to build prefix array, O(1) per query |
| Space | O(n) | Prefix array of size n+1 |

---

## Common Mistakes

### Mistake 1: Integer Overflow

**Problem:** Each element can be up to 10^9, and n up to 2 x 10^5. Max sum = 2 x 10^14, exceeding int range.

**Fix:** Use `long long` in C++ or Python's native arbitrary precision integers.

### Mistake 2: Off-by-One Indexing

```python
# WRONG - forgetting that queries are 1-indexed
sum = prefix[b] - prefix[a]  # Missing one element!

# CORRECT
sum = prefix[b] - prefix[a - 1]
```

**Problem:** If a=2, b=4, we want elements at indices 2, 3, 4. Using `prefix[a]` would exclude element at index a.

**Fix:** Always subtract `prefix[a-1]` to include the element at index a.

### Mistake 3: Forgetting prefix[0] = 0

```python
# WRONG - starting prefix from index 1 without base case
prefix[1] = arr[0]

# CORRECT - explicit base case
prefix[0] = 0
prefix[1] = prefix[0] + arr[0]
```

**Problem:** When a=1, we need `prefix[0]` to exist and equal 0.

---

## Edge Cases

| Case | Input | Output | Why |
|------|-------|--------|-----|
| Single element query | a = b = 3 | arr[3] | prefix[3] - prefix[2] = arr[3] |
| Full array | a = 1, b = n | Total sum | prefix[n] - prefix[0] = prefix[n] |
| First element | a = b = 1 | arr[1] | prefix[1] - prefix[0] = arr[1] |
| Large values | x_i = 10^9, n = 2x10^5 | Up to 2x10^14 | Requires long long |

---

## When to Use This Pattern

### Use Prefix Sums When:
- Array is static (no updates between queries)
- Need to answer multiple range sum queries
- Operation is associative and has an inverse (sum, XOR)
- O(n) preprocessing is acceptable

### Don't Use When:
- Array has updates between queries (use Segment Tree or BIT)
- Need range minimum/maximum (use Sparse Table or Segment Tree)
- Single query only (brute force is simpler)

### Pattern Recognition Checklist:
- [ ] Multiple range queries on static data? --> **Prefix Sums**
- [ ] Range sum with point updates? --> **Fenwick Tree / BIT**
- [ ] Range sum with range updates? --> **Segment Tree with Lazy Propagation**
- [ ] Range min/max queries? --> **Sparse Table or Segment Tree**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Range Sum Query - Immutable (LC 303)](https://leetcode.com/problems/range-sum-query-immutable/) | Same concept, good for practice |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Range XOR Queries (CSES)](https://cses.fi/problemset/task/1650) | XOR instead of sum |
| [Range Sum Query 2D - Immutable (LC 304)](https://leetcode.com/problems/range-sum-query-2d-immutable/) | 2D prefix sums |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Dynamic Range Sum Queries (CSES)](https://cses.fi/problemset/task/1648) | Updates require Segment Tree |
| [Static Range Minimum Queries (CSES)](https://cses.fi/problemset/task/1647) | Min requires Sparse Table |
| [Subarray Sum Equals K (LC 560)](https://leetcode.com/problems/subarray-sum-equals-k/) | Prefix sums + hash map |

---

## Key Takeaways

1. **The Core Idea:** Precompute cumulative sums to answer any range query in O(1)
2. **Time Optimization:** From O(q x n) brute force to O(n + q) with preprocessing
3. **Space Trade-off:** O(n) extra space enables O(1) queries
4. **Pattern:** Foundation for many range query techniques (2D prefix sums, difference arrays)

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a prefix sum array correctly (including the 0 base case)
- [ ] Convert between 0-indexed and 1-indexed seamlessly
- [ ] Identify overflow risks and use appropriate data types
- [ ] Implement both Python and C++ versions from memory
