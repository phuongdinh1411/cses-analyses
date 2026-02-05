---
layout: simple
title: "MEX Grid Construction - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/mex_grid_construction_analysis
difficulty: Medium
tags: [mex, grid, construction, constraint-satisfaction, math]
---

# MEX Grid Construction

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Construction / Math |
| **Time Limit** | 1 second |
| **Key Technique** | Constraint Satisfaction + MEX Properties |
| **CSES Link** | - |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand MEX (Minimum Excluded Value) and compute it efficiently
- [ ] Apply constraint satisfaction to grid construction problems
- [ ] Recognize when grid constraints are impossible to satisfy
- [ ] Construct valid grids using mathematical analysis

---

## Problem Statement

**Problem:** Given an n x n grid, construct a grid filled with non-negative integers such that the MEX of each row equals a given target value m. The MEX (Minimum Excluded Value) is the smallest non-negative integer not present in a set.

**Input:** Two integers n and m (grid size and target MEX)

**Output:** Print n lines with n space-separated integers, or "IMPOSSIBLE" if no solution exists.

**Constraints:** 1 <= n <= 1000, 0 <= m <= n

### Examples

```
Input: 3 2          Input: 2 3
Output:             Output:
0 1 3               IMPOSSIBLE
0 1 4
0 1 5
```

**Explanation:** For n=3, m=2: each row contains {0,1} but not 2, so MEX=2. For n=2, m=3: impossible since rows need {0,1,2} but only have 2 columns.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** What must be present in a row to achieve MEX = m?

For a row to have MEX = m:
1. It must contain all values from 0 to m-1 (so MEX is at least m)
2. It must NOT contain the value m (so MEX is exactly m)

### Key Constraint

```
For MEX = m in a row of length n:
- Need m required values: {0, 1, 2, ..., m-1}
- These m values must fit in n columns
- Therefore: m <= n (necessary and sufficient condition)
```

### Analogy

Think of MEX like checking parking spots numbered 0, 1, 2, ...:
- MEX is the first empty spot
- To achieve MEX = m, fill spots 0 through m-1 and leave spot m empty

---

## Solution: Mathematical Construction

### Key Insight

> **The Trick:** If m <= n, place {0, 1, ..., m-1} in each row and fill remaining cells with values > m.

### Algorithm

1. If m > n, return "IMPOSSIBLE"
2. For each row: fill columns 0 to m-1 with values 0 to m-1
3. Fill remaining columns with distinct values > m
4. Output the grid

### Dry Run Example

With n = 3, m = 2:

```
Check: m=2 <= n=3? YES

Row 0: [0, 1] + [3] = [0, 1, 3]  -> MEX = 2
Row 1: [0, 1] + [4] = [0, 1, 4]  -> MEX = 2
Row 2: [0, 1] + [5] = [0, 1, 5]  -> MEX = 2
```

### Visual Diagram

```
Target MEX = 2, Grid 3x3

Required (0 to m-1):     Fill remaining (> m):
+---+---+---+            +---+---+---+

| 0 | 1 | ? |    -->     | 0 | 1 | 3 |
| 0 | 1 | ? |            | 0 | 1 | 4 |
| 0 | 1 | ? |            | 0 | 1 | 5 |
+---+---+---+            +---+---+---+
```

### Code

#### Python

```python
def mex_grid_construction(n: int, m: int) -> None:
    """
    Construct n x n grid where each row has MEX = m.
    Time: O(n^2), Space: O(n^2)
    """
    if m > n:
        print("IMPOSSIBLE")
        return

    filler = m + 1
    for row in range(n):
        current_row = list(range(m))  # Values 0 to m-1
        for _ in range(m, n):
            current_row.append(filler)
            filler += 1
        print(*current_row)

if __name__ == "__main__":
    n, m = map(int, input().split())
    mex_grid_construction(n, m)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Fill n x n grid cells |
| Space | O(1) | Output directly, no storage needed |

---

## Common Mistakes

### Mistake 1: Missing Feasibility Check

```python
# WRONG
def wrong(n, m):
    for row in range(n):
        print(*list(range(m)) + [m+1]*(n-m))  # Crashes if m > n

# CORRECT
if m > n:
    print("IMPOSSIBLE")
    return
```

### Mistake 2: Including m in the Row

```python
# WRONG - gives MEX > m
row = list(range(m + 1))  # Includes m!

# CORRECT
row = list(range(m))  # Only 0 to m-1
```

### Mistake 3: Filler Values Include m

```python
# WRONG - filler starts at m
filler = m  # MEX becomes > m!

# CORRECT - skip m
filler = m + 1
```

---

## Edge Cases

| Case | Input (n, m) | Output | Reason |
|------|--------------|--------|--------|
| m = 0 | (3, 0) | Grid with no zeros | MEX = 0 means 0 absent |
| m = n | (3, 3) | 0 1 2 per row | Exactly fits |
| m > n | (2, 3) | IMPOSSIBLE | Cannot fit {0,1,2} |
| n = 1, m = 0 | (1, 0) | 1 | Single cell > 0 |
| n = 1, m = 1 | (1, 1) | 0 | Single cell = 0 |

---

## When to Use This Pattern

### Use When:
- Constructing grids with row/column MEX constraints
- Constraints involve specific values present/absent
- Each row/column can be constructed independently

### Don't Use When:
- MEX constraints on BOTH rows AND columns (more complex)
- Values must be unique across entire grid
- Problem asks for counting valid grids (use DP)

### Pattern Recognition:
- [ ] MEX problem? -> Smallest missing non-negative integer
- [ ] Construction? -> Check feasibility first
- [ ] Row-only constraints? -> Rows are independent

---

## Related Problems

### Easier (Do First)

| Problem | Why It Helps |
|---------|--------------|
| [Missing Number](https://cses.fi/problemset/task/1083) | Finding missing values |
| [Permutations](https://cses.fi/problemset/task/1070) | Basic construction |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Chessboard and Queens](https://cses.fi/problemset/task/1624) | Grid with conflict constraints |
| [Grid Paths](https://cses.fi/problemset/task/1638) | Grid traversal |

### Harder (Do After)

| Problem | New Concept |
|---------|-------------|
| MEX Grid Construction II | Dual row/column constraints |
| [Codeforces MEX Problems](https://codeforces.com/problemset?tags=constructive) | Advanced MEX constructions |

---

## Key Takeaways

1. **MEX Definition:** Smallest non-negative integer not in a set
2. **Feasibility:** For MEX = m with n columns, need m <= n
3. **Construction:** Include {0..m-1}, exclude m, fill rest with values > m
4. **Edge Case:** m = 0 means no zeros in any row

---

## Practice Checklist

- [ ] Explain MEX and compute it for a given set
- [ ] Determine when construction is impossible
- [ ] Implement without looking at the solution
- [ ] Handle m = 0 correctly
- [ ] Solve in under 10 minutes
