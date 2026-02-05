---
layout: simple
title: "Range XOR Queries - Prefix XOR"
permalink: /problem_soulutions/range_queries/range_xor_queries_analysis
difficulty: Easy
tags: [prefix-xor, bitwise, range-queries, preprocessing]
prerequisites: [static_range_sum_queries]
---

# Range XOR Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Prefix XOR |
| **CSES Link** | [Range XOR Queries](https://cses.fi/problemset/task/1650) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the XOR self-inverse property: `a ^ a = 0`
- [ ] Build and use prefix XOR arrays for O(1) range queries
- [ ] Apply the prefix technique to bitwise operations
- [ ] Recognize when prefix arrays work (associative + invertible operations)

---

## Problem Statement

**Problem:** Given a static array of n integers and q queries, answer each query asking for the XOR of all elements in a range [a, b].

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers x1, x2, ..., xn (array elements)
- Next q lines: Two integers a and b (1-indexed range boundaries)

**Output:**
- q lines: XOR of elements in range [a, b] for each query

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
3
0
6
4
```

**Explanation:**
- Query [2,4]: 2 ^ 4 ^ 5 = 3
- Query [5,6]: 1 ^ 1 = 0
- Query [1,8]: 3 ^ 2 ^ 4 ^ 5 ^ 1 ^ 1 ^ 5 ^ 3 = 6
- Query [3,3]: 4 (single element)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we answer range XOR queries faster than computing XOR for each query from scratch?

This is the XOR analog of range sum queries. Just like prefix sums allow O(1) range sum queries, **prefix XORs** allow O(1) range XOR queries.

### The XOR Self-Inverse Property

The magic of XOR comes from these properties:
```
a ^ a = 0        (XOR with itself gives 0)
a ^ 0 = a        (XOR with 0 gives itself)
a ^ b ^ a = b    (XOR is self-inverse)
```

### Breaking Down the Problem

1. **What are we looking for?** XOR of elements in range [a, b]
2. **What information do we have?** Static array, multiple queries
3. **Key insight:** If prefix[i] = x1 ^ x2 ^ ... ^ xi, then:
   ```
   range_xor(a, b) = prefix[b] ^ prefix[a-1]
   ```

### Why Does prefix[b] ^ prefix[a-1] Work?

```
prefix[b]   = x1 ^ x2 ^ ... ^ x(a-1) ^ xa ^ ... ^ xb
prefix[a-1] = x1 ^ x2 ^ ... ^ x(a-1)

prefix[b] ^ prefix[a-1] = (x1 ^ x2 ^ ... ^ x(a-1) ^ xa ^ ... ^ xb)
                        ^ (x1 ^ x2 ^ ... ^ x(a-1))
                        = xa ^ ... ^ xb  (common terms cancel out!)
```

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the range and XOR all elements together.

### Algorithm

1. For each query (a, b)
2. Initialize result = 0
3. XOR all elements from index a to b
4. Output the result

### Code

```python
def solve_brute_force(n, arr, queries):
  """
  Brute force: compute XOR for each query independently.

  Time: O(q * n)
  Space: O(1)
  """
  results = []
  for a, b in queries:
    xor_result = 0
    for i in range(a - 1, b):  # Convert to 0-indexed
      xor_result ^= arr[i]
    results.append(xor_result)
  return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans up to n elements |
| Space | O(1) | No extra space needed |

### Why This Is Too Slow

With n, q up to 2 x 10^5, worst case is 4 x 10^10 operations - far too slow for a 1-second time limit.

---

## Solution 2: Optimal - Prefix XOR

### Key Insight

> **The Trick:** Precompute prefix XORs to answer any range query in O(1).

### Prefix Array Definition

| State | Meaning |
|-------|---------|
| `prefix[0]` | 0 (identity element for XOR) |
| `prefix[i]` | arr[0] ^ arr[1] ^ ... ^ arr[i-1] |

**In plain English:** prefix[i] stores the XOR of all elements before index i.

### Range Query Formula

```
range_xor(a, b) = prefix[b] ^ prefix[a-1]
```

**Why?** The elements before index `a` appear in both prefix[b] and prefix[a-1], so they cancel out when XORed together.

### Algorithm

1. Build prefix array: prefix[i] = prefix[i-1] ^ arr[i-1]
2. For each query (a, b): answer = prefix[b] ^ prefix[a-1]

### Dry Run Example

Let's trace through with `arr = [3, 2, 4, 5, 1, 1, 5, 3]`:

```
Building prefix array (1-indexed storage):
  prefix[0] = 0                           (base case)
  prefix[1] = prefix[0] ^ arr[0] = 0 ^ 3 = 3
  prefix[2] = prefix[1] ^ arr[1] = 3 ^ 2 = 1
  prefix[3] = prefix[2] ^ arr[2] = 1 ^ 4 = 5
  prefix[4] = prefix[3] ^ arr[3] = 5 ^ 5 = 0
  prefix[5] = prefix[4] ^ arr[4] = 0 ^ 1 = 1
  prefix[6] = prefix[5] ^ arr[5] = 1 ^ 1 = 0
  prefix[7] = prefix[6] ^ arr[6] = 0 ^ 5 = 5
  prefix[8] = prefix[7] ^ arr[7] = 5 ^ 3 = 6

Final: prefix = [0, 3, 1, 5, 0, 1, 0, 5, 6]

Query [2, 4]: prefix[4] ^ prefix[1] = 0 ^ 3 = 3
Query [5, 6]: prefix[6] ^ prefix[4] = 0 ^ 0 = 0
Query [1, 8]: prefix[8] ^ prefix[0] = 6 ^ 0 = 6
Query [3, 3]: prefix[3] ^ prefix[2] = 5 ^ 1 = 4
```

### Visual Diagram

```
Index:      1    2    3    4    5    6    7    8
Array:     [3]  [2]  [4]  [5]  [1]  [1]  [5]  [3]

prefix[0] = 0
prefix[1] = 3 ─────────────────────────────────────┐
prefix[2] = 3^2 = 1                                │
prefix[3] = 3^2^4 = 5                              │
prefix[4] = 3^2^4^5 = 0 ───────────────────────────┤
                                                   │
Query [2,4] = prefix[4] ^ prefix[1]                │
            = (3^2^4^5) ^ (3)                       │
            = 2^4^5 = 3                             ▼
            └──────────────────────── 3 ^ 3 cancels out!
```

### Code

**Python Solution:**
```python
import sys
input = sys.stdin.readline

def solve():
  n, q = map(int, input().split())
  arr = list(map(int, input().split()))

  # Build prefix XOR array
  prefix = [0] * (n + 1)
  for i in range(n):
    prefix[i + 1] = prefix[i] ^ arr[i]

  # Answer queries
  results = []
  for _ in range(q):
    a, b = map(int, input().split())
    results.append(prefix[b] ^ prefix[a - 1])

  print('\n'.join(map(str, results)))

solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n + q) | O(n) preprocessing + O(1) per query |
| Space | O(n) | Prefix array storage |

---

## Common Mistakes

### Mistake 1: Off-by-One in Prefix Indexing

```python
# WRONG - prefix[a] instead of prefix[a-1]
result = prefix[b] ^ prefix[a]  # Excludes arr[a-1]!

# CORRECT
result = prefix[b] ^ prefix[a - 1]  # Includes all elements from a to b
```

**Problem:** Using prefix[a] excludes the element at position a.
**Fix:** Use prefix[a-1] to include all elements from index a to b.

### Mistake 2: Forgetting 1-Indexed Input

```python
# WRONG - treating input as 0-indexed
result = prefix[b + 1] ^ prefix[a]

# CORRECT - input is already 1-indexed
result = prefix[b] ^ prefix[a - 1]
```

**Problem:** CSES problems typically use 1-indexed input.
**Fix:** Design prefix array to work with 1-indexed queries directly.

**Note:** XOR operations don't cause overflow since the result is bounded by the maximum input value.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | n=1, query [1,1] | arr[0] | prefix[1] ^ prefix[0] = arr[0] ^ 0 = arr[0] |
| Full array | query [1,n] | prefix[n] | prefix[n] ^ prefix[0] = prefix[n] |
| All same values | arr=[5,5,5,5], query [1,4] | 0 | 5^5^5^5 = 0 (even count) |
| All zeros | arr=[0,0,0], query [1,3] | 0 | 0^0^0 = 0 |
| Two elements equal | query [i,i+1] where arr[i]=arr[i+1] | 0 | a^a = 0 |
| Maximum values | arr=[10^9, 10^9] | varies | No overflow with XOR |

---

## When to Use This Pattern

### Use Prefix XOR When:
- Array is static (no updates)
- Multiple range XOR queries on same array
- Need O(1) query time after preprocessing
- Operation has an inverse (XOR is self-inverse: a ^ a = 0)

### Don't Use When:
- Array has updates between queries -> Use Segment Tree or Fenwick Tree
- Single query only -> Brute force is simpler and equally fast
- Operation lacks inverse (e.g., AND, OR, MAX, MIN) -> Need different structures

### Pattern Recognition Checklist:
- [ ] Static array with multiple queries? -> **Prefix technique candidate**
- [ ] Operation is XOR? -> **Prefix XOR works perfectly**
- [ ] Operation is associative and has inverse? -> **Prefix technique applicable**
- [ ] Need updates? -> **Consider Segment Tree or Fenwick Tree instead**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries (CSES)](https://cses.fi/problemset/task/1646) | Same prefix technique with addition |
| [Running Sum of 1d Array (LeetCode)](https://leetcode.com/problems/running-sum-of-1d-array/) | Basic prefix computation |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Static Range Minimum Queries (CSES)](https://cses.fi/problemset/task/1647) | MIN lacks inverse - needs Sparse Table |
| [Subarray Sum Equals K (LeetCode)](https://leetcode.com/problems/subarray-sum-equals-k/) | Prefix sum + hash map combination |
| [XOR Queries of a Subarray (LeetCode)](https://leetcode.com/problems/xor-queries-of-a-subarray/) | Identical problem on LeetCode |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Dynamic Range Sum Queries (CSES)](https://cses.fi/problemset/task/1648) | Fenwick Tree for updates |
| [Range Update Queries (CSES)](https://cses.fi/problemset/task/1651) | Difference arrays / lazy propagation |
| [Maximum XOR Subarray (Various)](https://www.geeksforgeeks.org/find-the-maximum-subarray-xor-in-a-given-array/) | Prefix XOR + Trie for max XOR |

---

## Key Takeaways

1. **The Core Idea:** XOR's self-inverse property (a ^ a = 0) enables prefix-based range queries
2. **Time Optimization:** From O(q * n) brute force to O(n + q) with preprocessing
3. **Space Trade-off:** O(n) extra space for O(1) query time
4. **Pattern:** This is the "prefix technique" applied to XOR - same idea works for any associative operation with an inverse

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why prefix[b] ^ prefix[a-1] gives the range XOR
- [ ] Implement prefix XOR from scratch without looking at solution
- [ ] Handle 1-indexed input correctly
- [ ] Identify when prefix technique works (associative + invertible operations)
- [ ] Solve this problem in under 5 minutes

---

## Additional Resources

- [CP-Algorithms: Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sums.html)
- [CSES Problem Set - Range Queries](https://cses.fi/problemset/list/)
- [Bitwise Operations Reference](https://en.wikipedia.org/wiki/Bitwise_operation)
