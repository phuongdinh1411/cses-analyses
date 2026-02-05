---
layout: simple
title: "All Letter Subgrid Count I - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/all_letter_subgrid_count_i_analysis
difficulty: Medium
tags: [grid, counting, set, subgrid, enumeration]
prerequisites: [basic_grid_traversal, set_operations]
---

# All Letter Subgrid Count I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Grid Counting / Enumeration |
| **Time Limit** | 1 second |
| **Key Technique** | Subgrid Enumeration + Set Tracking |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Enumerate all possible subgrids in an n x m grid efficiently
- [ ] Use sets to track distinct elements in a rectangular region
- [ ] Apply incremental counting to avoid redundant recomputation
- [ ] Understand when O(n^2 * m^2) is acceptable vs. when optimization is needed

---

## Problem Statement

**Problem:** Given a grid of lowercase letters, count the number of subgrids (rectangular regions) that contain ALL unique letters present in the entire grid.

**Input:**
- Line 1: Two integers n and m (grid dimensions)
- Next n lines: A string of m lowercase letters

**Output:**
- Single integer: count of valid subgrids (modulo 10^9 + 7)

**Constraints:**
- 1 <= n, m <= 100
- Grid contains lowercase letters a-z

### Example

```
Input:
2 3
abc
def

Output:
1
```

**Explanation:** The grid contains 6 unique letters: {a, b, c, d, e, f}. The only subgrid containing all 6 letters is the entire 2x3 grid itself.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we systematically check all rectangular regions?

A subgrid is defined by four boundaries: top row, bottom row, left column, right column. We need to enumerate all valid combinations and check if each contains all required letters.

### Breaking Down the Problem

1. **What are we looking for?** Count of subgrids containing all unique letters
2. **What information do we have?** An n x m character grid
3. **What's the relationship?** A subgrid is valid if its letter set equals the grid's total letter set

### Analogies

Think of this problem like searching for rectangular windows on a map. You need to find all windows large enough to see every landmark (letter) at least once.

---

## Solution 1: Brute Force Enumeration

### Idea

Enumerate all possible subgrids using four nested loops. For each subgrid, collect all letters and check if the set matches all unique letters in the grid.

### Algorithm

1. Find all unique letters in the entire grid
2. For each possible (top, left, bottom, right) combination:
   - Collect all letters in that subgrid
   - If the set contains all unique letters, increment count

### Code

**Python:**
```python
def count_all_letter_subgrids(n, m, grid):
 """
 Brute force: enumerate all subgrids, check each for completeness.

 Time: O(n^2 * m^2 * n * m) - 6 nested loops
 Space: O(k) where k = number of unique letters
 """
 MOD = 10**9 + 7

 # Find all unique letters in grid
 all_letters = set()
 for row in grid:
  for ch in row:
   all_letters.add(ch)
 target_count = len(all_letters)

 result = 0

 # Enumerate all subgrids: O(n^2 * m^2)
 for top in range(n):
  for left in range(m):
   for bottom in range(top, n):
    for right in range(left, m):
     # Collect letters in this subgrid: O(n * m)
     letters = set()
     for i in range(top, bottom + 1):
      for j in range(left, right + 1):
       letters.add(grid[i][j])

     if len(letters) == target_count:
      result = (result + 1) % MOD

 return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 * m^3) | 4 loops for boundaries + 2 loops to scan subgrid |
| Space | O(26) = O(1) | At most 26 letters in set |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every possible subgrid. However, we redundantly scan the same cells multiple times for overlapping subgrids.

---

## Solution 2: Optimized with Incremental Set Building

### Key Insight

> **The Trick:** When expanding a subgrid to the right, only add the new column's letters instead of rescanning the entire subgrid.

### Algorithm

1. Fix top and bottom rows
2. For each left boundary, incrementally expand right
3. When expanding right by one column, only scan that new column
4. Maintain a running set of letters

### Dry Run Example

Let's trace through with input:
```
Grid:
a b c
d e f

All unique letters: {a, b, c, d, e, f} (count = 6)
```

```
Fix top=0, bottom=1:

  left=0, right=0:
    Subgrid: [a]    letters={a,d} -> 2 letters, need 6, NOT valid
             [d]

  left=0, right=1:
    Subgrid: [a b]  letters={a,b,d,e} -> 4 letters, NOT valid
             [d e]

  left=0, right=2:
    Subgrid: [a b c]  letters={a,b,c,d,e,f} -> 6 letters, VALID! count=1
             [d e f]

  left=1, right=1:
    Subgrid: [b]    letters={b,e} -> 2 letters, NOT valid
             [e]

  left=1, right=2:
    Subgrid: [b c]  letters={b,c,e,f} -> 4 letters, NOT valid
             [e f]

  left=2, right=2:
    Subgrid: [c]    letters={c,f} -> 2 letters, NOT valid
             [f]

Final count = 1
```

### Visual Diagram

```
Grid:     a b c
          d e f

Expanding right from (0,0) to (1,2):

Step 1: [a]     Step 2: [a b]    Step 3: [a b c]
        [d]             [d e]            [d e f]

        {a,d}           {a,b,d,e}        {a,b,c,d,e,f}
        2 letters       4 letters        6 letters = ALL!
```

### Code

**Python:**
```python
def count_all_letter_subgrids_optimized(n, m, grid):
 """
 Optimized: incrementally build set when expanding right.

 Time: O(n^2 * m^2) - still 4 loops but no inner scanning
 Space: O(26) = O(1)
 """
 MOD = 10**9 + 7

 # Find all unique letters
 all_letters = set()
 for row in grid:
  for ch in row:
   all_letters.add(ch)
 target_count = len(all_letters)

 result = 0

 # Fix top and bottom rows
 for top in range(n):
  for bottom in range(top, n):
   # For this row range, slide window across columns
   for left in range(m):
    letters = set()
    for right in range(left, m):
     # Only add the new column
     for i in range(top, bottom + 1):
      letters.add(grid[i][right])

     if len(letters) == target_count:
      result = (result + 1) % MOD

 return result
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 * m^2) | 4 loops, column scan is amortized |
| Space | O(26) = O(1) | At most 26 letters in set |

---

## Common Mistakes

### Mistake 1: Forgetting to Reset the Set

```python
# WRONG - set accumulates across different left boundaries
letters = set()
for left in range(m):
 for right in range(left, m):
  # letters still has old values!
  for i in range(top, bottom + 1):
   letters.add(grid[i][right])
```

**Problem:** The set is not reset when starting a new left boundary.
**Fix:** Reset `letters = set()` inside the left loop, not outside.

### Mistake 2: Wrong Loop Order

```python
# WRONG - bottom should depend on top
for top in range(n):
 for bottom in range(n):  # Should start from top!
  ...
```

**Problem:** Creates invalid subgrids where bottom < top.
**Fix:** Use `for bottom in range(top, n)`.

### Mistake 3: Not Applying Modulo

```python
# WRONG - may overflow for large results
if len(letters) == target_count:
 result += 1  # Should be (result + 1) % MOD
```

**Problem:** Result can exceed integer limits.
**Fix:** Apply modulo at each addition.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single cell | 1x1 grid "a" | 1 | Only one letter, one subgrid |
| All same letter | 2x2 "aa/aa" | 4 | Every subgrid contains 'a' |
| All different | 1x3 "abc" | 1 | Only full row has all 3 |
| No valid subgrid | Large sparse grid | 0 | Some letter not reachable |

---

## When to Use This Pattern

### Use This Approach When:
- Grid dimensions are small (n, m <= 100)
- Need to count subgrids satisfying a property checkable via set membership
- The property depends on distinct elements, not frequencies

### Don't Use When:
- Grid is very large (n, m > 500) - need more optimization
- You need exact frequency counts (use frequency arrays instead)
- Looking for submatrices with sum constraints (use prefix sums)

### Pattern Recognition Checklist:
- [ ] Counting rectangular regions? -> Consider 4-loop enumeration
- [ ] Need distinct elements? -> Use set operations
- [ ] Small grid (n,m <= 100)? -> O(n^2 * m^2) is acceptable
- [ ] Large grid? -> Consider 2D prefix sums or advanced techniques

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Subarray Distinct Values](https://cses.fi/problemset/task/2428) | 1D version of distinct counting |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Counting Tilings](https://cses.fi/problemset/task/2181) | Grid DP with bitmask |
| [Counting Grids](https://cses.fi/problemset/task/2210) | Different grid counting variant |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| 2D Range Distinct Query | Persistent data structures |
| Maximum Subgrid with K Distinct | Binary search + 2D sliding window |

---

## Key Takeaways

1. **The Core Idea:** Enumerate all subgrids using 4 boundary parameters
2. **Time Optimization:** Build sets incrementally when expanding boundaries
3. **Space Trade-off:** O(1) extra space using constant-size letter sets
4. **Pattern:** Grid enumeration with set-based property checking

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Enumerate all subgrids correctly using 4 nested loops
- [ ] Explain why incremental set building improves performance
- [ ] Handle the modulo operation correctly
- [ ] Identify when this O(n^2 * m^2) approach is acceptable

---

## Additional Resources

- [CP-Algorithms: 2D Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sums.html)
- [CSES Forest Queries](https://cses.fi/problemset/task/1652) - 2D prefix sum queries
- [Subgrid Problems on USACO Guide](https://usaco.guide/)
