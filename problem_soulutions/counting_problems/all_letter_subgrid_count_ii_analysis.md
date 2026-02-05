---
layout: simple
title: "All Letter Subgrid Count II - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/all_letter_subgrid_count_ii_analysis
difficulty: Medium
tags: [grid, counting, prefix-sum, 2d-array]
prerequisites: [prefix_sums, 2d_arrays]
---

# All Letter Subgrid Count II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Grid Counting |
| **Time Limit** | 1 second |
| **Key Technique** | Prefix Sums / Histogram Method |
| **CSES Link** | - |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply prefix sums to 2D grid problems
- [ ] Count uniform subgrids efficiently using histogram techniques
- [ ] Recognize when to use monotonic stack for counting problems
- [ ] Optimize O(n^4) brute force to O(n^2) or better

---

## Problem Statement

**Problem:** Given an n x m grid of lowercase letters, count all rectangular subgrids where every cell contains the same letter.

**Input:**
- Line 1: Two integers n and m (grid dimensions)
- Next n lines: Strings of length m representing the grid

**Output:**
- Single integer: the count of uniform subgrids

**Constraints:**
- 1 <= n, m <= 1000
- Grid contains only lowercase letters 'a'-'z'

### Example

```
Input:
3 3
aaa
aaa
aaa

Output:
14
```

**Explanation:**
- 9 subgrids of size 1x1 (each cell)
- 4 subgrids of size 2x2 (all contain 'a')
- 1 subgrid of size 3x3 (entire grid)
- Total: 9 + 4 + 1 = 14

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we avoid checking every possible subgrid explicitly?

The insight is to fix two rows and count how many valid subgrids exist between them. For each pair of rows, we track "heights" of consecutive matching columns.

### Breaking Down the Problem

1. **What are we looking for?** All rectangles where every cell has the same letter
2. **What information do we have?** An n x m character grid
3. **What's the relationship?** A valid subgrid requires all cells in a rectangular region to match

### Analogies

Think of this like counting rectangles in a histogram. For each column, track how many consecutive rows (from top) have the same letter. Then use histogram techniques to count rectangles.

---

## Solution 1: Brute Force

### Idea

Check every possible subgrid by iterating over all top-left corners and all dimensions.

### Algorithm

1. For each top-left corner (i, j)
2. For each possible height and width
3. Check if all cells in the subgrid match
4. Increment count if valid

### Code

```python
def count_uniform_subgrids_brute(grid):
    """
    Brute force: check every subgrid.

    Time: O(n^2 * m^2 * n * m) worst case
    Space: O(1)
    """
    n, m = len(grid), len(grid[0])
    count = 0

    for i in range(n):
        for j in range(m):
            for h in range(1, n - i + 1):
                for w in range(1, m - j + 1):
                    letter = grid[i][j]
                    valid = True
                    for di in range(h):
                        for dj in range(w):
                            if grid[i + di][j + dj] != letter:
                                valid = False
                                break
                        if not valid:
                            break
                    if valid:
                        count += 1
    return count
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^3 * m^3) | Six nested loops in worst case |
| Space | O(1) | No extra storage |

### Why This Works (But Is Slow)

Correctness is guaranteed by exhaustive checking, but the complexity is far too high for n, m = 1000.

---

## Solution 2: Height Array + Counting (Optimal)

### Key Insight

> **The Trick:** For each position, precompute the "height" of consecutive identical letters going upward. Then for each row, count rectangles using a histogram approach.

### Algorithm

1. Build a height array: `height[i][j]` = number of consecutive identical letters ending at (i, j) going upward
2. For each row, iterate left to right tracking segments of matching letters
3. Use arithmetic formula to count rectangles in each segment

### Dry Run Example

Let's trace through with a 3x3 grid of all 'a':

```
Grid:         Height array (consecutive up):
a a a         1 1 1
a a a    ->   2 2 2
a a a         3 3 3

Processing row 2 (heights = [3, 3, 3]):
  - All columns have same letter 'a'
  - Segment width = 3, heights = [3, 3, 3]
  - Count rectangles using histogram method
```

For a segment with uniform heights h and width w:
- Number of rectangles = h * (w * (w + 1) / 2)

For varying heights, use stack-based approach or segment analysis.

### Visual Diagram

```
Height calculation:
     col 0  col 1  col 2
row 0:  1      1      1     (first row, all heights = 1)
row 1:  2      2      2     (same letter above, height++)
row 2:  3      3      3     (same letter above, height++)

Counting rectangles at row 2:
- 1x1: 3 cells
- 1x2: 2 pairs horizontally
- 1x3: 1 triple horizontally
- 2x1, 2x2, 2x3: extend upward
- 3x1, 3x2, 3x3: extend further
```

### Code

```python
def count_uniform_subgrids(grid):
    """
    Optimal solution using height arrays.

    Time: O(n * m)
    Space: O(m)
    """
    if not grid or not grid[0]:
        return 0

    n, m = len(grid), len(grid[0])
    height = [0] * m  # height of consecutive same-letter cells
    prev_char = [''] * m  # letter at previous row
    total = 0

    for i in range(n):
        # Update heights for current row
        for j in range(m):
            if grid[i][j] == prev_char[j]:
                height[j] += 1
            else:
                height[j] = 1
                prev_char[j] = grid[i][j]

        # Count rectangles ending at row i
        j = 0
        while j < m:
            # Find segment of same letter
            letter = grid[i][j]
            start = j
            min_height = height[j]

            while j < m and grid[i][j] == letter:
                min_height = min(min_height, height[j])
                # Count rectangles with this cell as bottom-right
                # Using stack approach for general case
                j += 1

            # For segment [start, j), count all uniform rectangles
            total += count_segment_rectangles(height, start, j)

    return total


def count_segment_rectangles(height, start, end):
    """
    Count rectangles in a horizontal segment where all cells
    have the same letter. Uses monotonic stack.
    """
    count = 0
    stack = []  # (index, height)

    for j in range(start, end + 1):
        h = height[j] if j < end else 0
        width = 0

        while stack and stack[-1][1] >= h:
            idx, prev_h = stack.pop()
            width += (j - idx) if not stack else (j - stack[-1][0] - 1)
            # Rectangles with height exactly prev_h
            segment_width = j - idx
            count += (prev_h - h) * segment_width * (segment_width + 1) // 2

        if width > 0 or not stack:
            stack.append((j - width if width else j, h))

    return count
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n * m) | Each cell processed once, stack ops amortized O(1) |
| Space | O(m) | Height array and stack |

---

## Common Mistakes

### Mistake 1: Not Resetting Height on Letter Change

```python
# WRONG
for j in range(m):
    height[j] += 1  # Always incrementing

# CORRECT
for j in range(m):
    if grid[i][j] == prev_char[j]:
        height[j] += 1
    else:
        height[j] = 1  # Reset when letter changes
        prev_char[j] = grid[i][j]
```

**Problem:** Heights must reset when the letter changes.
**Fix:** Track the previous letter and reset height to 1 on change.

### Mistake 2: Off-by-One in Segment Boundaries

```python
# WRONG
while j < m and grid[i][j] == letter:
    process(j)
# Forgot to handle last element properly

# CORRECT
for j in range(start, end + 1):  # Include sentinel
    h = height[j] if j < end else 0  # Sentinel forces stack flush
```

**Problem:** Not properly closing out rectangles at segment end.
**Fix:** Use a sentinel value (height 0) to force final processing.

### Mistake 3: Integer Overflow

```python
# WRONG (in languages with fixed-size integers)
count += width * (width + 1) / 2 * height

# CORRECT (C++)
count += (long long)width * (width + 1) / 2 * height
```

**Problem:** With n, m = 1000, counts can exceed 32-bit integers.
**Fix:** Use 64-bit integers (long long in C++, Python handles automatically).

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single cell | `1x1 grid "a"` | 1 | Only one 1x1 subgrid |
| All same letter | `n x m grid of 'a'` | n*m*(n+1)*(m+1)/4 | Formula for counting all rectangles |
| Alternating letters | `"ababab..."` | n*m | Only 1x1 subgrids valid |
| Single row | `1 x m grid` | m*(m+1)/2 | All horizontal substrings of uniform char |
| Single column | `n x 1 grid` | n*(n+1)/2 | All vertical substrings of uniform char |

---

## When to Use This Pattern

### Use This Approach When:
- Counting rectangles/subgrids with uniform properties
- 2D problems reducible to 1D histogram problems
- Need to optimize from O(n^4) to O(n^2) or better

### Don't Use When:
- Subgrids have complex constraints (not just uniformity)
- Need to enumerate actual subgrids, not just count
- Problem has different structure (consider DP or other approaches)

### Pattern Recognition Checklist:
- [ ] Counting rectangles in a grid? -> **Consider height arrays**
- [ ] Uniform regions? -> **Height resets on value change**
- [ ] Need O(n^2) or better? -> **Histogram + stack technique**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [CSES - Rectangle Cutting](https://cses.fi/problemset/task/1744) | Basic 2D DP grid problem |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES - Counting Rooms](https://cses.fi/problemset/task/1192) | Grid counting with flood fill |
| [LeetCode - Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Find largest, not count all |
| [LeetCode - Count Submatrices With All Ones](https://leetcode.com/problems/count-submatrices-with-all-ones/) | Binary grid version |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES - Grid Paths](https://cses.fi/problemset/task/1078) | Grid path counting with constraints |
| [LeetCode - Number of Submatrices That Sum to Target](https://leetcode.com/problems/number-of-submatrices-that-sum-to-target/) | Prefix sums + hash map in 2D |

---

## Key Takeaways

1. **The Core Idea:** Convert 2D rectangle counting to 1D histogram problems by fixing rows
2. **Time Optimization:** From O(n^4) brute force to O(n*m) using height arrays and monotonic stack
3. **Space Trade-off:** O(m) extra space for height tracking enables linear time per row
4. **Pattern:** Histogram-based rectangle counting is a powerful technique for grid problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement the height array construction correctly
- [ ] Apply the monotonic stack histogram technique
- [ ] Handle letter boundaries (reset heights appropriately)
- [ ] Calculate rectangle counts using the formula w*(w+1)/2 for uniform segments

---

## Additional Resources

- [CP-Algorithms: Maximum Rectangle in Histogram](https://cp-algorithms.com/data_structures/stack_max_count.html)
- [CSES Forest Queries](https://cses.fi/problemset/task/1652) - 2D prefix sums
- [Monotonic Stack Tutorial](https://leetcode.com/problems/largest-rectangle-in-histogram/solutions/28902/5ms-o-n-java-solution-explained-beats-96/)
