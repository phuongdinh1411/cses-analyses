---
layout: simple
title: "Forest Queries - 2D Prefix Sums"
permalink: /problem_soulutions/range_queries/forest_queries_analysis
difficulty: Easy
tags: [prefix-sum, 2d-array, range-query]
prerequisites: [static_range_sum_queries]
---

# Forest Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | 2D Prefix Sum |
| **CSES Link** | [Forest Queries](https://cses.fi/problemset/task/1652) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Build a 2D prefix sum array from a grid
- [ ] Apply inclusion-exclusion principle for rectangle queries
- [ ] Answer O(1) range sum queries after O(n^2) preprocessing
- [ ] Handle 1-indexed vs 0-indexed coordinate conversions

---

## Problem Statement

**Problem:** You are given an n x n grid representing a forest. Each cell contains either a tree ('*') or is empty ('.'). Answer q queries, where each query asks: how many trees are in the rectangle from (y1, x1) to (y2, x2)?

**Input:**
- Line 1: Two integers n and q (grid size and number of queries)
- Lines 2 to n+1: n characters each, representing the forest grid
- Lines n+2 to n+q+1: Four integers y1, x1, y2, x2 per line (rectangle corners, 1-indexed)

**Output:**
- q lines: the number of trees in each queried rectangle

**Constraints:**
- 1 <= n <= 1000
- 1 <= q <= 200,000
- 1 <= y1 <= y2 <= n
- 1 <= x1 <= x2 <= n

### Example

```
Input:
4 3
.*..
*.**
**..
****
2 2 3 4
3 1 3 2
1 1 2 2

Output:
3
2
2
```

**Explanation:**
- Query 1 (row 2-3, col 2-4): cells are `.**` and `*..`, containing 3 trees
- Query 2 (row 3, col 1-2): cells are `**`, containing 2 trees
- Query 3 (row 1-2, col 1-2): cells are `.*` and `*.`, containing 2 trees

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we answer many rectangle sum queries efficiently without recalculating from scratch each time?

This is a classic 2D prefix sum problem. Just as 1D prefix sums let us compute range sums in O(1), 2D prefix sums let us compute rectangle sums in O(1) after O(n^2) preprocessing.

### Breaking Down the Problem

1. **What are we looking for?** Count of trees in a rectangle
2. **What information do we have?** A static grid (no updates)
3. **What's the relationship between input and output?** Each query is independent; we need to sum values in a 2D range

### The 2D Prefix Sum Formula

For a prefix sum array where `prefix[i][j]` = sum of all cells from (0,0) to (i-1, j-1):

```
Rectangle Sum from (r1,c1) to (r2,c2) =
    prefix[r2][c2] - prefix[r1-1][c2] - prefix[r2][c1-1] + prefix[r1-1][c1-1]
```

### Visual: Inclusion-Exclusion Principle

```
To get sum of region D:

    c1-1    c2
     |      |
r1-1 +------+------+
     |  A   |  B   |
     +------+------+
r2   |  C   |  D   |
     +------+------+

prefix[r2][c2]     = A + B + C + D  (entire rectangle from origin)
prefix[r1-1][c2]   = A + B          (top portion)
prefix[r2][c1-1]   = A + C          (left portion)
prefix[r1-1][c1-1] = A              (top-left corner)

D = (A+B+C+D) - (A+B) - (A+C) + A
  = prefix[r2][c2] - prefix[r1-1][c2] - prefix[r2][c1-1] + prefix[r1-1][c1-1]
```

We add back `prefix[r1-1][c1-1]` because region A was subtracted twice.

---

## Solution 1: Brute Force

### Idea

For each query, iterate through every cell in the rectangle and count trees.

### Algorithm

1. Parse the grid into a 2D array
2. For each query (y1, x1, y2, x2):
   - Iterate through all cells from row y1 to y2, column x1 to x2
   - Count cells containing trees
3. Output the count

### Code

```python
def solve_brute_force(n, q, grid, queries):
 """
 Brute force: iterate through each rectangle.

 Time: O(q * n^2) per query in worst case
 Space: O(1) extra
 """
 results = []
 for y1, x1, y2, x2 in queries:
  count = 0
  for i in range(y1 - 1, y2):  # Convert to 0-indexed
   for j in range(x1 - 1, x2):
    if grid[i][j] == '*':
     count += 1
  results.append(count)
 return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n^2) | Each query scans up to n^2 cells |
| Space | O(1) | Only counter variable |

### Why This Works (But Is Slow)

This correctly counts trees but with q = 200,000 queries and n = 1000, we could have 200 billion operations - far too slow.

---

## Solution 2: Optimal Solution with 2D Prefix Sum

### Key Insight

> **The Trick:** Precompute cumulative sums so any rectangle sum can be calculated in O(1) using inclusion-exclusion.

### Building the Prefix Sum Array

| State | Meaning |
|-------|---------|
| `prefix[i][j]` | Total trees in rectangle from (0,0) to (i-1, j-1) |

**Building formula:**
```
prefix[i][j] = grid[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]
```

We add the current cell, plus the sum above, plus the sum to the left, minus the overlap (top-left was counted twice).

### Algorithm

1. Create prefix sum array of size (n+1) x (n+1) initialized to 0
2. Build prefix sums row by row
3. For each query, apply inclusion-exclusion formula

### Dry Run Example

Let's trace through with the example grid:

```
Grid (1-indexed):       Binary (tree=1):
  1 2 3 4                 1 2 3 4
1 . * . .               1 0 1 0 0
2 * . * *               2 1 0 1 1
3 * * . .               3 1 1 0 0
4 * * * *               4 1 1 1 1
```

**Building prefix sum array (0-indexed for padding):**

```
Initial: All zeros (5x5 array for n=4)

Step-by-step fill (showing prefix[i][j] values):

     0  1  2  3  4
  0 [0, 0, 0, 0, 0]
  1 [0, 0, 1, 1, 1]   <- Row 1: prefix[1][2] = 0+0+0-0+1 = 1
  2 [0, 1, 1, 2, 3]   <- Row 2: prefix[2][1] = 1+0+0-0+1 = 1
  3 [0, 2, 3, 4, 5]   <- Row 3 processed
  4 [0, 3, 5, 7, 9]   <- Row 4 processed

Final prefix array.
```

**Query 1: (y1=2, x1=2, y2=3, x2=4)**
```
Trees = prefix[3][4] - prefix[1][4] - prefix[3][1] + prefix[1][1]
      = 5 - 1 - 2 + 0
      = 3 trees
```

**Query 2: (y1=3, x1=1, y2=3, x2=2)**
```
Trees = prefix[3][2] - prefix[2][2] - prefix[3][0] + prefix[2][0]
      = 3 - 1 - 0 + 0
      = 2 trees
```

### Code

**Python Solution:**

```python
import sys
input = sys.stdin.readline

def solve():
 n, q = map(int, input().split())

 # Build prefix sum array (1-indexed, with 0-padding)
 prefix = [[0] * (n + 1) for _ in range(n + 1)]

 for i in range(1, n + 1):
  row = input().strip()
  for j in range(1, n + 1):
   tree = 1 if row[j - 1] == '*' else 0
   prefix[i][j] = (tree +
      prefix[i - 1][j] +
      prefix[i][j - 1] -
      prefix[i - 1][j - 1])

 # Answer queries
 results = []
 for _ in range(q):
  y1, x1, y2, x2 = map(int, input().split())
  count = (prefix[y2][x2] -
    prefix[y1 - 1][x2] -
    prefix[y2][x1 - 1] +
    prefix[y1 - 1][x1 - 1])
  results.append(count)

 print('\n'.join(map(str, results)))

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 + q) | O(n^2) preprocessing, O(1) per query |
| Space | O(n^2) | Prefix sum array |

---

## Common Mistakes

### Mistake 1: Index Confusion (0 vs 1-indexed)

```python
# WRONG - mixing indices
prefix[i][j] = tree + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]
# But then querying with 0-indexed boundaries

# CORRECT - be consistent
# Either use 1-indexed throughout OR convert at boundaries
```

**Problem:** Off-by-one errors cause wrong rectangle boundaries.
**Fix:** Stick to one indexing scheme. Using 1-indexed prefix array with 0-padding is cleanest.

### Mistake 2: Forgetting to Add Back the Corner

```python
# WRONG - missing the +prefix[y1-1][x1-1]
count = prefix[y2][x2] - prefix[y1-1][x2] - prefix[y2][x1-1]

# CORRECT
count = prefix[y2][x2] - prefix[y1-1][x2] - prefix[y2][x1-1] + prefix[y1-1][x1-1]
```

**Problem:** The top-left region gets subtracted twice.
**Fix:** Always add back the corner using inclusion-exclusion.

### Mistake 3: Array Size Too Small

```python
# WRONG - no room for 0-padding
prefix = [[0] * n for _ in range(n)]

# CORRECT - (n+1) x (n+1) for 0-padding
prefix = [[0] * (n + 1) for _ in range(n + 1)]
```

**Problem:** Index out of bounds when accessing prefix[i-1] or prefix[j-1].
**Fix:** Allocate (n+1) x (n+1) array to handle boundary padding.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single cell (tree) | `1x1 grid with '*'`, query `1 1 1 1` | 1 | Smallest possible query |
| Single cell (empty) | `1x1 grid with '.'`, query `1 1 1 1` | 0 | Empty cell |
| Entire grid | Query covers full n x n | Total tree count | Maximum rectangle |
| Single row | `y1 == y2` | Row slice sum | Degenerates to 1D |
| Single column | `x1 == x2` | Column slice sum | Degenerates to 1D |
| All trees | Grid of all '*' | (y2-y1+1) * (x2-x1+1) | Area of rectangle |
| No trees | Grid of all '.' | 0 | Empty forest |

---

## When to Use This Pattern

### Use 2D Prefix Sum When:
- Grid is static (no updates after preprocessing)
- Many range/rectangle sum queries
- Need O(1) query time
- Can afford O(n^2) space and preprocessing

### Don't Use When:
- Grid has frequent updates (use 2D Fenwick Tree or 2D Segment Tree)
- Only a few queries (brute force may be simpler)
- Need range max/min (prefix sums only work for sum-like operations)
- Space is very constrained

### Pattern Recognition Checklist:
- [ ] Static 2D grid? -> **Consider 2D prefix sum**
- [ ] Multiple rectangle queries? -> **2D prefix sum is ideal**
- [ ] Updates between queries? -> **Use 2D Fenwick/Segment Tree instead**
- [ ] Need count/sum in rectangle? -> **2D prefix sum works**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries (CSES)](https://cses.fi/problemset/task/1646) | 1D prefix sum foundation |
| [Range Sum Query - Immutable (LC 303)](https://leetcode.com/problems/range-sum-query-immutable/) | 1D prefix sum practice |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Range Sum Query 2D - Immutable (LC 304)](https://leetcode.com/problems/range-sum-query-2d-immutable/) | Same technique, integer grid |
| [Forest Queries II (CSES)](https://cses.fi/problemset/task/1739) | Adds point updates (needs 2D BIT) |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Range Sum Query 2D - Mutable (LC 308)](https://leetcode.com/problems/range-sum-query-2d-mutable/) | 2D Fenwick Tree for updates |
| [Max Sum of Rectangle No Larger Than K (LC 363)](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/) | 2D prefix sum + binary search |

---

## Key Takeaways

1. **The Core Idea:** Precompute cumulative sums to answer rectangle queries in O(1)
2. **Time Optimization:** From O(q * n^2) brute force to O(n^2 + q) with preprocessing
3. **Space Trade-off:** Use O(n^2) space for the prefix array to gain O(1) query time
4. **Pattern:** 2D extension of prefix sums using inclusion-exclusion principle

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a 2D prefix sum array from scratch
- [ ] Apply the inclusion-exclusion formula without looking it up
- [ ] Handle 1-indexed input correctly
- [ ] Explain why we add back the corner term
- [ ] Implement in both Python and C++ in under 10 minutes
