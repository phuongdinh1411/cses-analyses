---
layout: simple
title: "Filled Subgrid Count II - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/filled_subgrid_count_ii_analysis
difficulty: Medium
tags: [prefix-sum, 2d-array, counting, grid]
prerequisites: [prefix_sums, basic_2d_arrays]
---

# Filled Subgrid Count II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Grid / Counting |
| **Time Limit** | 1 second |
| **Key Technique** | 2D Prefix Sum |
| **CSES Link** | - |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Build and query 2D prefix sum arrays efficiently
- [ ] Use O(1) range sum queries to validate subgrid properties
- [ ] Recognize when prefix sums optimize brute force grid enumeration
- [ ] Apply inclusion-exclusion principle for 2D queries

---

## Problem Statement

**Problem:** Given an n x m grid, count the number of rectangular subgrids where all cells contain a target value (typically 1).

**Input:**
- Line 1: Two integers n, m (grid dimensions)
- Next n lines: m integers each (grid values)

**Output:**
- A single integer: the count of completely filled subgrids

**Constraints:**
- 1 <= n, m <= 1000
- Grid values are integers (0 or 1)

### Example

```
Input:
3 3
1 1 1
1 1 1
1 1 1

Output:
14
```

**Explanation:**
- 9 subgrids of size 1x1 (each cell)
- 4 subgrids of size 2x2
- 1 subgrid of size 3x3
- Total: 9 + 4 + 1 = 14

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we quickly check if ALL cells in a rectangle have value 1?

If we sum all values in a rectangle, a subgrid of size h x w is completely filled with 1s if and only if the sum equals h * w.

### Breaking Down the Problem

1. **What are we looking for?** Count of all-1 rectangular subgrids
2. **What information do we have?** Grid of 0s and 1s
3. **What's the relationship?** Sum of subgrid = area means all cells are 1

### Analogies

Think of this like checking if a chocolate bar is complete - instead of checking each square individually, weigh the whole piece. If weight equals (rows x cols x unit_weight), nothing is missing.

---

## Solution 1: Brute Force

### Idea

Enumerate all possible subgrids and check each cell individually.

### Algorithm

1. For each top-left corner (i, j)
2. For each possible height and width
3. Check every cell in the subgrid
4. Count if all cells equal target value

### Code

```python
def count_filled_subgrids_brute(grid):
    """
    Brute force: check all subgrids cell by cell.
    Time: O(n^2 * m^2 * n * m) = O(n^3 * m^3)
    Space: O(1)
    """
    n, m = len(grid), len(grid[0])
    count = 0

    for i in range(n):
        for j in range(m):
            for h in range(1, n - i + 1):
                for w in range(1, m - j + 1):
                    if all(grid[i+di][j+dj] == 1
                           for di in range(h) for dj in range(w)):
                        count += 1
    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 * m^3) | 4 loops for position/size + 2 loops to check |
| Space | O(1) | No extra storage |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every cell. However, we redundantly recompute sums for overlapping regions.

---

## Solution 2: Optimal with 2D Prefix Sum

### Key Insight

> **The Trick:** Precompute a 2D prefix sum array to answer "sum of rectangle" queries in O(1).

### 2D Prefix Sum Definition

| State | Meaning |
|-------|---------|
| `prefix[i][j]` | Sum of all cells from (0,0) to (i-1, j-1) |

**In plain English:** `prefix[i][j]` stores the total of the rectangle with top-left at origin and bottom-right at (i-1, j-1).

### Building the Prefix Sum

```
prefix[i][j] = grid[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]
```

**Why?** Inclusion-exclusion: add top and left rectangles, subtract overlap, add current cell.

### Querying a Rectangle Sum

For rectangle from (r1, c1) to (r2, c2):
```
sum = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]
```

### Dry Run Example

Let's trace through with a 2x2 grid of all 1s:

```
Grid:           Prefix Sum (1-indexed):
1 1             0 0 0
1 1             0 1 2
                0 2 4

Building prefix[2][2]:
  prefix[2][2] = grid[1][1] + prefix[1][2] + prefix[2][1] - prefix[1][1]
               = 1 + 2 + 2 - 1 = 4

Query rectangle (0,0) to (1,1):
  sum = prefix[2][2] - prefix[0][2] - prefix[2][0] + prefix[0][0]
      = 4 - 0 - 0 + 0 = 4
  Expected for 2x2 all-ones: 2*2 = 4  [Match!]
```

### Visual Diagram

```
2D Prefix Sum Construction:

  Grid         prefix[i][j] = sum of shaded region
  +---+---+
  | 1 | 1 |    prefix[2][2] includes:
  +---+---+    +===+===+
  | 1 | 1 |    | X | X |
  +---+---+    +===+===+
               | X | X |
               +===+===+

Range Query using Inclusion-Exclusion:

  To get sum of [r1,c1] to [r2,c2]:

  +-------+-------+
  |   A   |   B   |
  +-------+-------+  Answer = Total - A - C + D
  |   C   | Query |  (D subtracted twice, add back)
  +-------+-------+
```

### Code

```python
def count_filled_subgrids(grid):
    """
    Optimal solution using 2D prefix sum.
    Time: O(n^2 * m^2) for enumeration, O(1) per query
    Space: O(n * m) for prefix array
    """
    n, m = len(grid), len(grid[0])

    # Build prefix sum (1-indexed for easier boundary handling)
    prefix = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            prefix[i+1][j+1] = (grid[i][j] + prefix[i][j+1]
                               + prefix[i+1][j] - prefix[i][j])

    def range_sum(r1, c1, r2, c2):
        """Get sum of rectangle from (r1,c1) to (r2,c2) inclusive."""
        return (prefix[r2+1][c2+1] - prefix[r1][c2+1]
                - prefix[r2+1][c1] + prefix[r1][c1])

    count = 0
    for i in range(n):
        for j in range(m):
            for h in range(1, n - i + 1):
                for w in range(1, m - j + 1):
                    total = range_sum(i, j, i + h - 1, j + w - 1)
                    if total == h * w:  # All cells are 1
                        count += 1
    return count


# Main function for CSES submission
def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0
    n, m = int(input_data[idx]), int(input_data[idx+1])
    idx += 2

    grid = []
    for i in range(n):
        row = [int(input_data[idx + j]) for j in range(m)]
        grid.append(row)
        idx += m

    print(count_filled_subgrids(grid))

if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 * m^2) | Four nested loops, O(1) per check |
| Space | O(n * m) | Prefix sum array storage |

---

## Common Mistakes

### Mistake 1: Off-by-One in Prefix Array Indexing

```python
# WRONG - forgetting 1-indexed offset
prefix[i][j] = grid[i][j] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]

# CORRECT - use 1-indexed prefix with 0-indexed grid
prefix[i+1][j+1] = grid[i][j] + prefix[i][j+1] + prefix[i+1][j] - prefix[i][j]
```

**Problem:** Index out of bounds or incorrect sums.
**Fix:** Use (n+1) x (m+1) prefix array with 1-based indexing.

### Mistake 2: Wrong Inclusion-Exclusion Formula

```python
# WRONG - missing subtraction
sum = prefix[r2][c2] - prefix[r1][c2] - prefix[r2][c1]

# CORRECT - add back doubly-subtracted corner
sum = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]
```

**Problem:** Incorrect range sum calculation.
**Fix:** Remember to add back the top-left corner (subtracted twice).

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| All zeros | 2x2 grid of 0s | 0 | No filled subgrids |
| All ones | 3x3 grid of 1s | 14 | All possible subgrids valid |
| Single cell (1) | 1x1 grid with 1 | 1 | One 1x1 subgrid |
| Single cell (0) | 1x1 grid with 0 | 0 | No valid subgrids |
| Single row | 1x5 of all 1s | 15 | 5+4+3+2+1 = 15 |
| Checkerboard | Alternating 0/1 | count of 1s | Only 1x1 subgrids valid |

---

## When to Use This Pattern

### Use 2D Prefix Sum When:
- You need multiple range sum queries on a static grid
- Checking if subgrid contains all same values
- Computing subgrid averages, counts, or sums
- Problems involving "rectangular region" properties

### Don't Use When:
- Grid is modified between queries (use 2D BIT/Segment Tree)
- Only need single query (direct computation is simpler)
- Looking for specific patterns beyond sums (use different technique)

### Pattern Recognition Checklist:
- [ ] Need sum/count in rectangular region? **2D Prefix Sum**
- [ ] Many queries on same grid? **Prefix Sum**
- [ ] Check if all cells in region equal X? **Sum == X * area**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | 1D prefix sum basics |
| [Subarray Sums I](https://cses.fi/problemset/task/1660) | 1D prefix sum application |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Forest Queries](https://cses.fi/problemset/task/1652) | 2D prefix sum, simpler query |
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | 1D variant with hash map |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) | Updates require segment tree |
| [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Stack-based histogram approach |

---

## Key Takeaways

1. **The Core Idea:** Use 2D prefix sums to answer rectangular range queries in O(1)
2. **Time Optimization:** From O(n^3 m^3) brute force to O(n^2 m^2) with prefix sums
3. **Space Trade-off:** O(nm) extra space for O(1) query time
4. **Pattern:** "Check property of all rectangles" often benefits from prefix sums

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a 2D prefix sum array from scratch
- [ ] Derive the inclusion-exclusion formula for range queries
- [ ] Identify problems where 2D prefix sum applies
- [ ] Handle 1-indexed vs 0-indexed conversions correctly

---

## Additional Resources

- [CP-Algorithms: 2D Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sum.html)
- [CSES Forest Queries](https://cses.fi/problemset/task/1652) - 2D prefix sum technique
- [Visualgo: Prefix Sum](https://visualgo.net/en/prefixsum)
