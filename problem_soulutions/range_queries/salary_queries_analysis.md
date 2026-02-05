---
layout: simple
title: "Salary Queries - Dynamic Range Counting with Coordinate Compression"
permalink: /problem_soulutions/range_queries/salary_queries_analysis
difficulty: Hard
tags: [BIT, Fenwick Tree, Coordinate Compression, Range Queries, Dynamic Updates]
---

# Salary Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [CSES Problem Set - Salary Queries](https://cses.fi/problemset/task/1144) |
| **Difficulty** | Hard |
| **Category** | Range Queries |
| **Time Limit** | 1.0 seconds |
| **Key Technique** | Coordinate Compression + Binary Indexed Tree (BIT) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand when and how to apply coordinate compression to handle large value ranges
- [ ] Implement a Binary Indexed Tree (BIT/Fenwick Tree) for dynamic frequency counting
- [ ] Combine coordinate compression with BIT for efficient range counting with updates
- [ ] Handle point updates and range queries in O(log n) time

---

## Problem Statement

**Problem:** You have n employees with given salaries. Process q queries where each query either:
1. Updates an employee's salary to a new value
2. Counts how many employees have salaries in the range [a, b]

**Input:**
- Line 1: n q (number of employees and queries)
- Line 2: n integers p1, p2, ..., pn (initial salaries)
- Next q lines: Either "! k x" (update salary of employee k to x) or "? a b" (count salaries in [a, b])

**Output:**
- For each "? a b" query, print the count of employees with salary in range [a, b]

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 1 <= pi, x <= 10^9
- 1 <= k <= n
- 1 <= a <= b <= 10^9

### Example

```
Input:
5 3
3 6 4 4 1
? 1 4
! 3 5
? 1 4

Output:
4
3
```

**Explanation:**
- Initial salaries: [3, 6, 4, 4, 1]
- Query 1 "? 1 4": Salaries in [1,4] are {3, 4, 4, 1} = 4 employees
- Update "! 3 5": Change employee 3's salary from 4 to 5. Now: [3, 6, 5, 4, 1]
- Query 2 "? 1 4": Salaries in [1,4] are {3, 4, 1} = 3 employees

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently count elements in a range when values can be updated?

The challenge is twofold: (1) salaries can be up to 10^9, making direct array indexing impossible, and (2) we need dynamic updates. This screams for **coordinate compression** to reduce the value space, combined with a **Binary Indexed Tree** for efficient updates and queries.

### Breaking Down the Problem

1. **What are we looking for?** Count of salaries in range [a, b] after each query
2. **What information do we have?** Initial salaries and a sequence of updates/queries
3. **What's the relationship between input and output?** Each range query returns count of salaries that fall within the bounds

### The Two Key Insights

**Insight 1: Coordinate Compression**
- Salaries can be 1 to 10^9, but we only have n + q unique values at most
- Compress all possible salary values to range [1, 2*(n+q)]
- This allows us to use array-based data structures

**Insight 2: BIT for Frequency Counting**
- Maintain frequency of each compressed salary value in a BIT
- Query count in [a, b] = prefix_sum(b) - prefix_sum(a-1)
- Update: decrease count at old salary, increase count at new salary

---

## Solution 1: Brute Force

### Idea

For each query, scan through all salaries and count those in range.

### Code

```python
def solve_brute_force():
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    salaries = list(map(int, input().split()))

    results = []
    for _ in range(q):
        query = input().split()
        if query[0] == '?':
            a, b = int(query[1]), int(query[2])
            count = sum(1 for s in salaries if a <= s <= b)
            results.append(count)
        else:  # '!'
            k, x = int(query[1]), int(query[2])
            salaries[k - 1] = x  # 1-indexed to 0-indexed

    print('\n'.join(map(str, results)))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans all n salaries |
| Space | O(n) | Store salaries array |

### Why This Works (But Is Slow)

Correctness is guaranteed because we examine every salary for each query. However, with n, q up to 2x10^5, we get 4x10^10 operations - far too slow.

---

## Solution 2: Optimal Solution (Coordinate Compression + BIT)

### Key Insight

> **The Trick:** Compress all unique salary values to a contiguous range, then use a BIT to track frequency of each compressed value. Range count becomes a difference of two prefix sums.

### Data Structure: Binary Indexed Tree (BIT)

| Operation | Complexity | Description |
|-----------|------------|-------------|
| `update(i, delta)` | O(log n) | Add delta to position i |
| `query(i)` | O(log n) | Get prefix sum [1, i] |
| `range_query(l, r)` | O(log n) | Get sum in range [l, r] |

### Algorithm

1. **Collect all values**: Initial salaries, update values, and query boundaries
2. **Coordinate compress**: Map all values to [1, total_unique_values]
3. **Initialize BIT**: Add 1 at each initial salary's compressed position
4. **Process queries**:
   - For "? a b": Return BIT.query(compress(b)) - BIT.query(compress(a-1))
   - For "! k x": BIT.update(old_pos, -1); BIT.update(new_pos, +1)

### Coordinate Compression Details

```
Original values:  [3, 6, 4, 4, 1, 5, 1, 4]  (salaries + query bounds)
Sorted unique:    [1, 3, 4, 5, 6]
Compressed:       {1:1, 3:2, 4:3, 5:4, 6:5}

When querying [1, 4]:
  compress(4) = 3, compress(1-1) = compress(0) = 0
  Answer = BIT.query(3) - BIT.query(0)
```

### Dry Run Example

Let's trace through with input: n=5, q=3, salaries=[3,6,4,4,1]

```
Step 1: Collect all values
  Initial salaries: [3, 6, 4, 4, 1]
  Query 1 bounds: [1, 4]
  Update value: [5]
  Query 2 bounds: [1, 4]
  All values: [1, 3, 4, 5, 6]

Step 2: Coordinate compression
  Sorted unique: [1, 3, 4, 5, 6]
  Mapping: {1->1, 3->2, 4->3, 5->4, 6->5}

Step 3: Initialize BIT
  BIT after adding salaries [3,6,4,4,1]:
  Position (compressed): 1  2  3  4  5
  Frequency:             1  1  2  0  1
  (salary 1 appears 1x, salary 3 appears 1x, salary 4 appears 2x, salary 6 appears 1x)

Step 4: Process queries

Query "? 1 4":
  compress(4) = 3, compress(0) = 0
  count = BIT.prefix(3) - BIT.prefix(0)
        = (1+1+2) - 0 = 4

Query "! 3 5":
  Employee 3's old salary = 4, new salary = 5
  compress(4) = 3, compress(5) = 4
  BIT.update(3, -1)  -> frequency at 3 becomes 1
  BIT.update(4, +1)  -> frequency at 4 becomes 1
  Current state: salaries = [3, 6, 5, 4, 1]

Query "? 1 4":
  compress(4) = 3, compress(0) = 0
  count = BIT.prefix(3) - BIT.prefix(0)
        = (1+1+1) - 0 = 3

Output: 4, 3
```

### Visual Diagram

```
Coordinate Compression:

Value Space:     1  2  3  4  5  6  ...  10^9
                 |     |  |  |  |
                 v     v  v  v  v
Compressed:      1     2  3  4  5    (only 5 unique values)


BIT Structure (after initialization):
Index:           1     2     3     4     5
Frequency:       1     1     2     0     1
                 ^     ^     ^           ^
                 |     |     |           |
              sal=1  sal=3  sal=4     sal=6

Range Query [1,4]:
  = prefix_sum(compressed(4)) - prefix_sum(compressed(0))
  = prefix_sum(3) - prefix_sum(0)
  = 4 - 0 = 4 employees
```

### Code

**Python Solution:**

```python
import sys
from bisect import bisect_left

def main():
    input = sys.stdin.readline

    n, q = map(int, input().split())
    salaries = list(map(int, input().split()))

    # Read all queries first
    queries = []
    for _ in range(q):
        line = input().split()
        if line[0] == '?':
            queries.append(('?', int(line[1]), int(line[2])))
        else:
            queries.append(('!', int(line[1]), int(line[2])))

    # Collect all values for coordinate compression
    all_values = set(salaries)
    for query in queries:
        if query[0] == '?':
            all_values.add(query[1])
            all_values.add(query[2])
        else:
            all_values.add(query[2])

    # Create sorted list for compression
    sorted_values = sorted(all_values)

    # Compress function: map value to 1-indexed position
    def compress(val):
        return bisect_left(sorted_values, val) + 1

    # BIT implementation
    size = len(sorted_values) + 2
    bit = [0] * size

    def update(i, delta):
        while i < size:
            bit[i] += delta
            i += i & (-i)

    def query(i):
        total = 0
        while i > 0:
            total += bit[i]
            i -= i & (-i)
        return total

    def range_query(l, r):
        if l > r:
            return 0
        return query(r) - query(l - 1)

    # Initialize BIT with initial salaries
    current_salaries = salaries[:]
    for sal in salaries:
        update(compress(sal), 1)

    # Process queries
    results = []
    for q_type, a, b in queries:
        if q_type == '?':
            # Count salaries in range [a, b]
            l = compress(a)
            r = compress(b)
            results.append(range_query(l, r))
        else:
            # Update salary of employee a to b
            k, new_sal = a, b
            old_sal = current_salaries[k - 1]

            # Update BIT: remove old, add new
            update(compress(old_sal), -1)
            update(compress(new_sal), 1)

            # Update current salary
            current_salaries[k - 1] = new_sal

    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n+q) log(n+q)) | Sorting + each operation is O(log n) |
| Space | O(n+q) | BIT size + compressed values storage |

---

## Common Mistakes

### Mistake 1: Not Pre-collecting All Values

```python
# WRONG - compressing on-the-fly
def compress(val, sorted_values):
    sorted_values.append(val)
    sorted_values.sort()  # Expensive and changes indices!
    return sorted_values.index(val) + 1
```

**Problem:** Coordinate compression must be done upfront with all values known.
**Fix:** Read all queries first, collect all values, then create a fixed mapping.

### Mistake 2: Off-by-One in Range Query

```python
# WRONG
def range_query(l, r):
    return query(r) - query(l)  # Missing element at l!

# CORRECT
def range_query(l, r):
    return query(r) - query(l - 1)  # Includes element at l
```

**Problem:** BIT prefix sum is inclusive, so [l, r] = prefix(r) - prefix(l-1).

### Mistake 3: Forgetting to Track Current Salaries

```python
# WRONG - using original array
old_sal = salaries[k - 1]  # Never updated!

# CORRECT - maintain current state
current_salaries = salaries[:]
# ... in update:
old_sal = current_salaries[k - 1]
current_salaries[k - 1] = new_sal
```

**Problem:** Must track current salary to know what to decrement in BIT.

### Mistake 4: Handling Query Bounds Not in Original Data

```python
# WRONG - query bound 7 not in salaries [3,6,4,4,1]
compress[7]  # KeyError!

# CORRECT - include ALL query bounds in compression
all_values.add(query_a)
all_values.add(query_b)
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single employee | n=1, salaries=[5], ? 1 10 | 1 | Only employee is in range |
| Empty range | salaries=[5,10], ? 6 9 | 0 | No salaries in range |
| All same salary | salaries=[5,5,5], ? 5 5 | 3 | All match exactly |
| Update to same value | ! k x where x == current | No change | BIT: -1 then +1 at same pos |
| Query at boundaries | ? 10^9 10^9 | 0 or 1 | Large value handling |
| Consecutive updates | Multiple ! to same employee | Track latest | Only current value matters |

---

## When to Use This Pattern

### Use Coordinate Compression + BIT When:
- Value range is large (up to 10^9) but unique values are limited
- You need both point updates and range queries
- Queries ask for count/sum in a range
- Updates modify individual elements

### Don't Use When:
- Values are already in small range (direct BIT suffices)
- No updates needed (just sort + binary search)
- Need range updates (use lazy segment tree instead)
- Need to query actual elements, not counts

### Pattern Recognition Checklist:
- [ ] Large value range with point updates? -> **Coordinate Compression**
- [ ] Need prefix sums with updates? -> **BIT**
- [ ] Count elements in range? -> **Frequency BIT**
- [ ] Range updates needed? -> **Consider Segment Tree with Lazy Propagation**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries (CSES 1646)](https://cses.fi/problemset/task/1646) | Basic prefix sum concept |
| [Dynamic Range Sum Queries (CSES 1648)](https://cses.fi/problemset/task/1648) | BIT fundamentals |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Range Update Queries (CSES 1651)](https://cses.fi/problemset/task/1651) | Range updates instead of point updates |
| [Distinct Values Queries (CSES 1734)](https://cses.fi/problemset/task/1734) | Count distinct values in range |
| [Range Sum Query - Mutable (LeetCode 307)](https://leetcode.com/problems/range-sum-query-mutable/) | Sum instead of count |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Polynomial Queries (CSES 1736)](https://cses.fi/problemset/task/1736) | Complex range updates |
| [Count of Range Sum (LeetCode 327)](https://leetcode.com/problems/count-of-range-sum/) | Merge sort approach for range count |
| [Range Frequency Queries (LeetCode 2080)](https://leetcode.com/problems/range-frequency-queries/) | Frequency in subarray |

---

## Key Takeaways

1. **The Core Idea:** Coordinate compression maps large value space to manageable indices; BIT handles dynamic frequency tracking
2. **Time Optimization:** From O(q*n) brute force to O((n+q) log(n+q)) using BIT
3. **Space Trade-off:** O(n+q) space for BIT enables O(log n) operations
4. **Pattern:** This is the "Dynamic Range Counting" pattern - compression + frequency BIT

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why coordinate compression is necessary for this problem
- [ ] Implement a BIT from scratch with update and query operations
- [ ] Trace through the algorithm on a small example
- [ ] Identify similar problems that use this pattern
- [ ] Solve this problem in under 20 minutes

---

## Additional Resources

- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CSES Salary Queries](https://cses.fi/problemset/task/1144) - Count elements in range with updates
- [Coordinate Compression Tutorial](https://usaco.guide/silver/sorting-custom)
