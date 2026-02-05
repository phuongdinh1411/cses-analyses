---
layout: simple
title: "Nested Ranges Count - Sorting Problem"
permalink: /problem_soulutions/sorting_and_searching/nested_ranges_count_analysis
difficulty: Hard
tags: [sorting, coordinate-compression, fenwick-tree, bit]
prerequisites: [nested_ranges_check]
---

# Nested Ranges Count

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Coordinate Compression + Fenwick Tree (BIT) |
| **CSES Link** | [Nested Ranges Count](https://cses.fi/problemset/task/2169) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply coordinate compression to handle large value ranges
- [ ] Use Fenwick Tree (BIT) for efficient prefix counting
- [ ] Design sorting strategies for range containment problems
- [ ] Count both "contains" and "contained by" relationships efficiently

---

## Problem Statement

**Problem:** Given n ranges, for each range count:
1. How many other ranges it **contains** (a range [a,b] contains [c,d] if a <= c and d <= b)
2. How many other ranges **contain** it

**Input:**
- Line 1: Integer n (number of ranges)
- Lines 2 to n+1: Two integers x and y (start and end of range)

**Output:**
- Line 1: n integers - for each range, how many ranges it contains
- Line 2: n integers - for each range, how many ranges contain it

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= x <= y <= 10^9

### Example

```
Input:
4
1 6
2 4
3 5
7 8

Output:
2 0 0 0
0 1 1 0
```

**Explanation:**

```
Range [1,6] contains [2,4] and [3,5] -> contains 2
Range [2,4] is contained by [1,6] -> contained by 1
Range [3,5] is contained by [1,6] -> contained by 1
Range [7,8] is disjoint from others -> 0 in both
```

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently count ranges contained within each range?

The brute force O(n^2) approach checks all pairs, but we can do better by:
1. **Sorting** ranges so that potential containers come before contained ranges
2. **Using BIT** to count how many valid end points we have seen

### Breaking Down the Problem

1. **What are we looking for?** For each range, count of contained/containing ranges
2. **What information do we have?** Start and end points of all ranges
3. **What's the relationship?** Range [a,b] contains [c,d] iff a <= c AND d <= b

### The Key Insight

If we sort ranges by **start ascending** (and by **end descending** for ties):
- When we process range i, all ranges j with smaller start have been seen
- Among those, count ranges where end[j] <= end[i] (they are contained by i)

We use a **Fenwick Tree** to efficiently count how many end points <= current end.

---

## Solution 1: Brute Force

### Idea

Check every pair of ranges for containment relationship.

### Algorithm

1. For each range i, iterate through all other ranges j
2. Check if i contains j (a[i] <= a[j] AND b[j] <= b[i])
3. Count both directions

### Code

```python
def brute_force(ranges):
  """
  Brute force: check all pairs.

  Time: O(n^2)
  Space: O(n)
  """
  n = len(ranges)
  contains = [0] * n
  contained_by = [0] * n

  for i in range(n):
    for j in range(n):
      if i == j:
        continue
      # Check if range i contains range j
      if ranges[i][0] <= ranges[j][0] and ranges[j][1] <= ranges[i][1]:
        contains[i] += 1
        contained_by[j] += 1

  # Divide by 2 since we count each relationship twice
  return contains, contained_by
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Check all n^2 pairs |
| Space | O(n) | Store counts |

### Why This Works (But Is Slow)

Correctness is guaranteed since we check every possible pair. However, with n up to 2 x 10^5, this gives 4 x 10^10 operations - far too slow.

---

## Solution 2: Optimal - Sorting + Fenwick Tree (BIT)

### Key Insight

> **The Trick:** Sort by start point, then use BIT to count valid end points we have seen.

### Why Fenwick Tree?

A Fenwick Tree (Binary Indexed Tree) supports:
- **Point update:** Add 1 at position i in O(log n)
- **Prefix query:** Count elements <= i in O(log n)

This is exactly what we need: "count how many ranges with smaller start have end <= current end."

### Coordinate Compression

Since end values can be up to 10^9 but we only have n <= 2 x 10^5 ranges, we compress coordinates:

```
Original ends: [6, 4, 5, 8] -> Sorted unique: [4, 5, 6, 8]
Compressed:    [3, 1, 2, 4] (1-indexed positions)
```

### Algorithm

**For "contains" count:**
1. Sort ranges by (start ASC, end DESC) with original indices
2. Process in order; for each range:
   - Query BIT: how many ends <= current end? (these ranges are contained by current)
   - Update BIT: add current end
3. Handle ties (same start) carefully

**For "contained_by" count:**
1. Sort ranges by (start DESC, end ASC)
2. Similar logic but reversed

### Dry Run Example

Let's trace through with ranges: `[1,6], [2,4], [3,5], [7,8]`

**Step 1: Coordinate Compression**
```
All end values: [6, 4, 5, 8]
Sorted unique:  [4, 5, 6, 8]
Mapping: 4->1, 5->2, 6->3, 8->4

Compressed ranges:
  [1,6] idx=0 -> end compressed = 3
  [2,4] idx=1 -> end compressed = 1
  [3,5] idx=2 -> end compressed = 2
  [7,8] idx=3 -> end compressed = 4
```

**Step 2: Sort for "contains" (start ASC, end DESC)**
```
Sorted order: [1,6], [2,4], [3,5], [7,8]
              idx=0   idx=1   idx=2   idx=3
```

**Step 3: Process with BIT for "contains"**
```
BIT initially: [0, 0, 0, 0, 0] (1-indexed)

Process [1,6] (compressed end = 3):
  Query(3) = 0 (no ends <= 3 seen yet)
  contains[0] = 0
  Update BIT at position 3: BIT adds 1
  BIT: [0, 0, 0, 1, 0]

Process [2,4] (compressed end = 1):
  Query(1) = 0
  contains[1] = 0
  Update BIT at position 1
  BIT: [0, 1, 0, 1, 0]

Process [3,5] (compressed end = 2):
  Query(2) = 1 (position 1 has value)
  But wait - [2,4] has start=2, [3,5] has start=3
  So [3,5] does NOT contain [2,4] (3 > 2)
  contains[2] = 0
  Update BIT at position 2

Process [7,8] (compressed end = 4):
  Query(4) = 3 (all previous ends)
  But [7,8] doesn't contain any (starts 1,2,3 < 7)
  contains[3] = 0
```

Wait - our dry run shows we need to be more careful. Let me correct the algorithm:

**Corrected Algorithm for "contains":**
- Sort by (start ASC, end DESC)
- When processing range with start=s, ranges with SAME start and LARGER end come first
- These larger-end ranges contain the current one
- We need to count ranges that current range contains = ranges with start >= current.start AND end <= current.end

Actually, let me re-approach. For "contains":
- Sort by (end ASC, start DESC)
- Process in order. For range [a,b], count ranges with start > a that we've seen

**Revised Dry Run:**

```
For counting how many ranges each range CONTAINS:

Sort by (start ASC, end DESC):
  [1,6], [2,4], [3,5], [7,8]

BIT tracks: ends of ranges we've processed (with smaller or equal start)

Process [1,6]:
  BIT empty, contains[0] += 0
  Add end=6 to BIT

Process [2,4]:
  Query: ends <= 4? We have [6], so 0 ends <= 4
  contains[1] += 0
  Add end=4 to BIT

Process [3,5]:
  Query: ends <= 5? We have [6,4], one end (4) <= 5
  contains[2] += 1? NO! [3,5] doesn't contain [2,4] since 2 < 3
  ...this approach counts [2,4] wrongly
```

The key insight is: we need to count ranges where start >= current.start AND end <= current.end. Let me use the correct approach:

**Correct Approach:**
1. For "contains": Sort by (start ASC, end DESC). Process ranges. When ranges have same start, larger end should process FIRST (it might contain smaller ends). Use BIT to count ends.
2. For "contained_by": Sort by (start DESC, end ASC). Similar logic reversed.

### Visual Diagram

```
Ranges on number line:
   1   2   3   4   5   6   7   8
   [===============]              [1,6] contains [2,4] and [3,5]
       [=====]                    [2,4]
           [=====]                [3,5]
                       [===]      [7,8]

After sorting by (start ASC, end DESC):
  [1,6] -> [2,4] -> [3,5] -> [7,8]

BIT counts ends seen so far:
  At [1,6]: no ends seen, contains = 0
  At [2,4]: end 6 seen but 6 > 4, contains = 0
  At [3,5]: ends [6,4] seen, 4 <= 5, but [2,4] has start=2 < 3
            Need to track that [1,6] doesn't apply (start 1 < 2)

Key: When starts differ, we CAN'T use simple prefix count!
     When start is same, end DESC means bigger end processes first.
```

### Handling Equal Starts

For ranges with **equal start**, the one with **larger end** contains the smaller ones:
- Sort by (start ASC, end DESC)
- Ranges with same start: larger end comes first
- It counts smaller ends as "contained"

For ranges with **different starts**, we process in start order and use BIT on ends.

### Code

```python
class FenwickTree:
  """Binary Indexed Tree for prefix sums."""

  def __init__(self, n):
    self.n = n
    self.tree = [0] * (n + 1)

  def update(self, i, delta=1):
    """Add delta at position i (1-indexed)."""
    while i <= self.n:
      self.tree[i] += delta
      i += i & (-i)  # Add lowest set bit

  def query(self, i):
    """Sum of elements from 1 to i."""
    total = 0
    while i > 0:
      total += self.tree[i]
      i -= i & (-i)  # Remove lowest set bit
    return total


def solve(n, ranges):
  """
  Count nested ranges using sorting + Fenwick Tree.

  Time: O(n log n)
  Space: O(n)
  """
  # Coordinate compression for end values
  ends = sorted(set(r[1] for r in ranges))
  compress = {v: i + 1 for i, v in enumerate(ends)}  # 1-indexed
  m = len(ends)

  contains = [0] * n
  contained_by = [0] * n

  # For "contained_by": sort by (start ASC, end DESC)
  # Ranges processed earlier have smaller/equal start
  # Among those with same start, larger end comes first
  indexed = [(ranges[i][0], -ranges[i][1], i) for i in range(n)]
  indexed.sort()

  bit = FenwickTree(m)

  for start, neg_end, idx in indexed:
    end = -neg_end
    comp_end = compress[end]
    # Count ranges with start <= current.start and end >= current.end
    # Those are ranges that CONTAIN the current range
    # Query: total seen - count of ends < current end
    # = count of ends >= current end
    contained_by[idx] = bit.query(m) - bit.query(comp_end - 1)
    bit.update(comp_end)

  # For "contains": sort by (start DESC, end ASC)
  # Process in reverse start order
  indexed = [(-ranges[i][0], ranges[i][1], i) for i in range(n)]
  indexed.sort()

  bit = FenwickTree(m)

  for neg_start, end, idx in indexed:
    comp_end = compress[end]
    # Count ranges with start >= current.start and end <= current.end
    # Those are ranges that current CONTAINS
    # Query: count of ends <= current end
    contains[idx] = bit.query(comp_end)
    bit.update(comp_end)

  return contains, contained_by


def main():
  import sys
  input_data = sys.stdin.read().split()
  ptr = 0
  n = int(input_data[ptr]); ptr += 1

  ranges = []
  for _ in range(n):
    x = int(input_data[ptr]); ptr += 1
    y = int(input_data[ptr]); ptr += 1
    ranges.append((x, y))

  contains, contained_by = solve(n, ranges)
  print(' '.join(map(str, contains)))
  print(' '.join(map(str, contained_by)))


if __name__ == "__main__":
  main()
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Sorting + n BIT operations (each O(log n)) |
| Space | O(n) | BIT array + coordinate compression map |

---

## Common Mistakes

### Mistake 1: Forgetting Coordinate Compression

```python
# WRONG: end values can be up to 10^9
bit = FenwickTree(10**9)  # Memory limit exceeded!

# CORRECT: compress to range [1, n]
ends = sorted(set(r[1] for r in ranges))
compress = {v: i + 1 for i, v in enumerate(ends)}
bit = FenwickTree(len(ends))
```

**Problem:** BIT size must match the range of values, not the raw values.
**Fix:** Always compress coordinates when values can be large.

### Mistake 2: Wrong Sorting Tiebreaker

```python
# WRONG: arbitrary tiebreaker
indexed.sort(key=lambda x: x[0])

# CORRECT: specific tiebreaker for correct counting
# For contained_by: (start ASC, end DESC)
indexed.sort(key=lambda x: (x[0], -x[1]))
```

**Problem:** Without proper tiebreaking, ranges with same start are processed in wrong order.
**Fix:** Use (start ASC, end DESC) for contained_by; (start DESC, end ASC) for contains.

### Mistake 3: Off-by-One in BIT

```python
# WRONG: 0-indexed BIT
compress = {v: i for i, v in enumerate(ends)}  # 0-indexed

# CORRECT: 1-indexed for BIT
compress = {v: i + 1 for i, v in enumerate(ends)}  # 1-indexed
```

**Problem:** Fenwick Tree operations assume 1-indexed arrays.
**Fix:** Always use 1-indexed positions in BIT.

### Mistake 4: Wrong Query Direction

```python
# WRONG: querying wrong range
# For contained_by: want ends >= current end
count = bit.query(comp_end)  # This gives ends <= current

# CORRECT:
count = bit.query(m) - bit.query(comp_end - 1)  # Ends >= current
```

**Problem:** Need to count ends >= current, not ends <= current.
**Fix:** Use complement: total - (ends < current) = ends >= current.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single range | `n=1, [(1,5)]` | `0` and `0` | No other ranges to compare |
| All identical | `n=3, [(1,5),(1,5),(1,5)]` | `0 0 0` and `0 0 0` | Equal ranges don't contain each other (need strict) |
| Nested chain | `[(1,6),(2,5),(3,4)]` | `2 1 0` and `0 1 2` | Each contains/is contained by others in chain |
| All disjoint | `[(1,2),(3,4),(5,6)]` | `0 0 0` and `0 0 0` | No overlaps |
| Same start | `[(1,5),(1,3),(1,2)]` | `2 1 0` and `0 1 2` | Same start, different ends |
| Same end | `[(1,5),(3,5),(4,5)]` | `2 1 0` and `0 1 2` | Different starts, same end |

---

## When to Use This Pattern

### Use This Approach When:
- Counting containment/dominance relationships between intervals
- Need O(n log n) time instead of O(n^2)
- Values are large but count of items is manageable (coordinate compression)
- Problems involving "count elements satisfying condition seen so far"

### Don't Use When:
- Simple overlap detection (use sorting alone)
- Need actual nested ranges, not counts (use check version)
- Online queries with updates (consider segment tree with lazy propagation)

### Pattern Recognition Checklist:
- [ ] Need to count items with property <= or >= threshold? -> **Consider BIT**
- [ ] Values too large for direct indexing? -> **Apply coordinate compression**
- [ ] Processing elements in order and counting past elements? -> **Sorting + BIT**
- [ ] 2D dominance counting (x1 <= x2 AND y1 <= y2)? -> **This exact pattern**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Nested Ranges Check (CSES)](https://cses.fi/problemset/task/2168) | Same problem but boolean output |
| [Dynamic Range Sum Queries (CSES)](https://cses.fi/problemset/task/1648) | Learn BIT basics |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Restaurant Customers (CSES)](https://cses.fi/problemset/task/1619) | Sweep line on ranges |
| [Josephus Problem II (CSES)](https://cses.fi/problemset/task/2163) | BIT for order statistics |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Distinct Values Queries (CSES)](https://cses.fi/problemset/task/1734) | Offline queries + BIT |
| [Inversion Count](https://www.spoj.com/problems/INVCNT/) | Classic BIT application |

### LeetCode Related

| Problem | Connection |
|---------|------------|
| [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | BIT for counting |
| [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | 2D containment (LIS approach) |

---

## Key Takeaways

1. **The Core Idea:** Sort ranges strategically, use BIT to count valid endpoints seen so far
2. **Time Optimization:** From O(n^2) brute force to O(n log n) with sorting + BIT
3. **Space Trade-off:** O(n) for BIT and coordinate compression map
4. **Pattern:** 2D dominance counting - sorting one dimension, BIT on the other

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement Fenwick Tree from scratch (update and query)
- [ ] Apply coordinate compression to large value ranges
- [ ] Determine correct sorting order for containment problems
- [ ] Solve this problem without looking at the solution
- [ ] Explain why the tiebreaker in sorting matters

---

## Additional Resources

- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CSES Nested Ranges Count](https://cses.fi/problemset/task/2169) - Count range containment
- [TopCoder: Binary Indexed Trees](https://www.topcoder.com/community/competitive-programming/tutorials/binary-indexed-trees/)
