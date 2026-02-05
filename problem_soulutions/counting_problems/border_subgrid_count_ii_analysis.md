---
layout: simple
title: "Border Subgrid Count II - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/border_subgrid_count_ii_analysis
difficulty: Hard
tags: [grid, prefix-sum, counting, 2d-arrays]
---

# Border Subgrid Count II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Grid Counting / 2D Prefix Sums |
| **Time Limit** | 1.0 seconds |
| **Key Technique** | 2D Prefix Sum, Range Queries |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Distinguish between border cells and interior cells in a subgrid
- [ ] Build and query 2D prefix sums for multiple value types
- [ ] Apply early termination to optimize brute force validation
- [ ] Recognize when prefix sums convert O(hw) validation to O(1)

---

## Problem Statement

**Problem:** Given an n x m grid, count all subgrids where border cells equal a specific value and interior cells equal a different value.

**Input:**
- Line 1: Two integers n and m (grid dimensions)
- Lines 2 to n+1: m integers per row representing the grid

**Output:**
- A single integer: the count of valid border subgrids

**Constraints:**
- 1 <= n, m <= 1000
- Grid values are integers (typically 0 or 1)

### Example

```
Input:
4 4
1 1 1 1
1 0 0 1
1 0 0 1
1 1 1 1

Output:
1
```

**Explanation:** Only the 4x4 subgrid satisfies the condition:
- Border cells (perimeter): all 1s
- Interior cells (2x2 center): all 0s

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently verify both border AND interior conditions for every possible subgrid?

The challenge is that a naive check of every cell in every subgrid is O(n^2 * m^2 * n * m). We need to validate border and interior regions in O(1) time using prefix sums.

### Breaking Down the Problem

1. **What are we counting?** Subgrids where border = value_b and interior = value_i
2. **What defines a border?** First/last row and first/last column of the subgrid
3. **What defines interior?** All cells not on the border (requires height >= 3 and width >= 3)

### Visual Understanding

```
Subgrid structure (4x5):
+---+---+---+---+---+

| B | B | B | B | B |  <- Top border
+---+---+---+---+---+

| B | I | I | I | B |  <- Interior with side borders
+---+---+---+---+---+

| B | I | I | I | B |  <- Interior with side borders
+---+---+---+---+---+

| B | B | B | B | B |  <- Bottom border
+---+---+---+---+---+

B = Border cell (must equal border_value)
I = Interior cell (must equal interior_value)

Border count = 2*(h + w) - 4 = 2*(4 + 5) - 4 = 14
Interior count = (h-2)*(w-2) = 2*3 = 6
```

---

## Solution 1: Brute Force

### Idea

Check every possible subgrid by iterating through all cells and validating border/interior conditions.

### Algorithm

1. Enumerate all top-left corners (i, j)
2. Enumerate all heights and widths
3. For each subgrid, check all border and interior cells

### Code

```python
def count_border_subgrids_brute(n, m, grid, border_val=1, interior_val=0):
  """
  Brute force: check all subgrids by examining each cell.

  Time: O(n^2 * m^2 * n * m) worst case
  Space: O(1)
  """
  count = 0
  for i in range(n):
    for j in range(m):
      for h in range(1, n - i + 1):
        for w in range(1, m - j + 1):
          if is_valid_subgrid(grid, i, j, h, w, border_val, interior_val):
            count += 1
  return count

def is_valid_subgrid(grid, r, c, h, w, border_val, interior_val):
  """Check if subgrid has valid border and interior."""
  for i in range(r, r + h):
    for j in range(c, c + w):
      is_border = (i == r or i == r + h - 1 or j == c or j == c + w - 1)
      if is_border:
        if grid[i][j] != border_val:
          return False
      else:
        if grid[i][j] != interior_val:
          return False
  return True
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^4 * m^2) | Four nested loops + O(nm) validation |
| Space | O(1) | No extra space |

### Why This Is Slow

Each subgrid validation scans up to n*m cells. With O(n^2 * m^2) subgrids, this becomes impractical for n, m = 1000.

---

## Solution 2: Optimal - 2D Prefix Sums

### Key Insight

> **The Trick:** Build two prefix sum arrays - one for border values, one for interior values. Then validate any rectangular region in O(1).

### Prefix Sum Concept

A 2D prefix sum allows us to compute the sum of any rectangle in O(1):
```
sum(r1, c1, r2, c2) = prefix[r2+1][c2+1] - prefix[r1][c2+1]
                    - prefix[r2+1][c1] + prefix[r1][c1]
```

### Algorithm

1. Build prefix sum for cells matching `border_val`
2. Build prefix sum for cells matching `interior_val`
3. For each subgrid, use prefix sums to count matching cells
4. Compare counts against expected border/interior sizes

### Dry Run Example

```
Grid (4x4):            border_val = 1, interior_val = 0
1 1 1 1
1 0 0 1
1 0 0 1
1 1 1 1

Check subgrid from (0,0) with height=4, width=4:

Step 1: Calculate expected counts
  Border cells = 2*(4+4) - 4 = 12
  Interior cells = (4-2)*(4-2) = 4

Step 2: Query prefix sums
  Total 1s in entire grid = 12 (using border_prefix)
  Total 0s in interior region (1,1) to (2,2) = 4 (using interior_prefix)

Step 3: Validate
  All 12 border positions have value 1? YES (12 == 12)
  All 4 interior positions have value 0? YES (4 == 4)

Result: Valid subgrid, count++
```

### Code

```python
def count_border_subgrids_optimal(n, m, grid, border_val=1, interior_val=0):
  """
  Optimal solution using 2D prefix sums.

  Time: O(n^2 * m^2) for enumeration, O(1) per validation
  Space: O(n * m) for prefix sum arrays
  """
  # Build prefix sums
  border_ps = build_prefix_sum(n, m, grid, border_val)
  interior_ps = build_prefix_sum(n, m, grid, interior_val)

  count = 0
  for i in range(n):
    for j in range(m):
      for h in range(1, n - i + 1):
        for w in range(1, m - j + 1):
          if is_valid_with_prefix(border_ps, interior_ps,
                      i, j, h, w):
            count += 1
  return count

def build_prefix_sum(n, m, grid, target):
  """Build 2D prefix sum for cells equal to target."""
  ps = [[0] * (m + 1) for _ in range(n + 1)]
  for i in range(n):
    for j in range(m):
      ps[i+1][j+1] = (ps[i][j+1] + ps[i+1][j] - ps[i][j]
             + (1 if grid[i][j] == target else 0))
  return ps

def query_sum(ps, r1, c1, r2, c2):
  """Query rectangle sum using prefix sums."""
  return ps[r2+1][c2+1] - ps[r1][c2+1] - ps[r2+1][c1] + ps[r1][c1]

def is_valid_with_prefix(border_ps, interior_ps, r, c, h, w):
  """Validate subgrid using prefix sums."""
  # Total border_val count in entire subgrid
  total_border = query_sum(border_ps, r, c, r + h - 1, c + w - 1)

  # Small subgrids (no interior) - all cells are border
  if h < 3 or w < 3:
    expected = h * w
    return total_border == expected

  # Calculate expected border cells
  expected_border = 2 * (h + w) - 4

  # Check interior region
  interior_count = query_sum(interior_ps, r + 1, c + 1, r + h - 2, c + w - 2)
  expected_interior = (h - 2) * (w - 2)

  return total_border == expected_border + interior_count and \
     interior_count == expected_interior
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2 * m^2) | Enumerate all subgrids, O(1) validation each |
| Space | O(n * m) | Two prefix sum arrays |

---

## Common Mistakes

### Mistake 1: Wrong Interior Region Indices

```python
# WRONG - off by one error
interior = query_sum(ps, r, c, r + h - 1, c + w - 1)  # This is entire grid!

# CORRECT - interior starts at (r+1, c+1) and ends at (r+h-2, c+w-2)
interior = query_sum(ps, r + 1, c + 1, r + h - 2, c + w - 2)
```

**Problem:** Interior region excludes the border, not the entire subgrid.
**Fix:** Interior spans from (r+1, c+1) to (r+h-2, c+w-2).

### Mistake 2: Forgetting Small Subgrids Have No Interior

```python
# WRONG - accessing invalid interior region
interior = query_sum(ps, r + 1, c + 1, r + h - 2, c + w - 2)  # Invalid if h < 3

# CORRECT - check size first
if h < 3 or w < 3:
  return all_cells_are_border
```

**Problem:** A 2x2 or 1xN subgrid has no interior cells.
**Fix:** Handle small subgrids as special cases.

### Mistake 3: Border Count Formula Error

```python
# WRONG
border_count = 2 * h + 2 * w  # Overcounts corners

# CORRECT
border_count = 2 * (h + w) - 4  # Subtract 4 corners counted twice
```

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| 1x1 grid | `[[1]]` | 1 | Single cell is its own border |
| All same value | `[[1,1],[1,1]]` | Count all | Every subgrid valid if border=1, interior=1 |
| No valid subgrids | `[[0,0],[0,0]]` | 0 | No border_val=1 exists |
| Minimum with interior | 3x3 | Check | Smallest grid with 1 interior cell |
| Large grid | 1000x1000 | Varies | Test performance |

---

## When to Use This Pattern

### Use 2D Prefix Sums When:
- Counting cells with specific values in rectangular regions
- Multiple queries over the same grid
- O(1) range sum is critical for performance

### Alternative Approaches:
- **Early termination brute force**: When most subgrids fail quickly
- **Sparse grids**: When target values are rare, enumerate positions instead

### Pattern Recognition Checklist:
- [ ] Need to sum/count values in rectangles? → **2D Prefix Sum**
- [ ] Multiple conditions on different regions? → **Multiple prefix arrays**
- [ ] Need O(1) validation per subgrid? → **Prefix sum queries**

---

## Related Problems

### CSES Problems

| Problem | Technique |
|---------|-----------|
| [Forest Queries](https://cses.fi/problemset/task/1652) | Basic 2D prefix sum |
| [Subarray Sums I](https://cses.fi/problemset/task/1660) | 1D prefix sum + hash map |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [LeetCode: Maximal Square](https://leetcode.com/problems/maximal-square/) | DP instead of counting |
| [LeetCode: Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d-immutable/) | Pure prefix sum queries |
| [LeetCode: Number of Submatrices That Sum to Target](https://leetcode.com/problems/number-of-submatrices-that-sum-to-target/) | Prefix sum + hash map |

---

## Key Takeaways

1. **Core Idea:** Use separate prefix sums for border and interior values to validate in O(1)
2. **Time Optimization:** Reduce validation from O(hw) to O(1) per subgrid
3. **Space Trade-off:** O(nm) space enables O(1) queries
4. **Border Formula:** Border cells = 2*(h + w) - 4, Interior = (h-2)*(w-2)

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Build a 2D prefix sum array from scratch
- [ ] Query any rectangular region in O(1)
- [ ] Correctly identify border vs interior cells
- [ ] Handle edge cases (small subgrids, empty interiors)

---

## Additional Resources

- [CP-Algorithms: 2D Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sums.html)
- [CSES Forest Queries II](https://cses.fi/problemset/task/1739) - 2D range updates
