---
layout: simple
title: "Minimum Path Sum in Grid"
difficulty: Easy
tags: [dp, 2d-dp, grid, optimization]
prerequisites: [grid_paths]
cses_link: https://cses.fi/problemset/task/1638
permalink: /problem_soulutions/dynamic_programming/minimal_grid_path_analysis
---

# Minimum Path Sum in Grid

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem Type | 2D Dynamic Programming |
| Difficulty | Easy |
| Key Technique | Grid DP with min() optimization |
| Time Complexity | O(n * m) |
| Space Complexity | O(n) optimized, O(n * m) basic |

## Learning Goals

By completing this problem, you will learn:
- How to apply DP for optimization problems on grids
- The difference between using `min()` vs `sum()` in DP transitions
- How to trace back and reconstruct the optimal path
- Space optimization techniques for 2D DP

## Problem Statement

Given an `n x n` grid where each cell contains a non-negative integer representing its cost, find a path from the top-left corner `(0,0)` to the bottom-right corner `(n-1,n-1)` that minimizes the total sum of costs along the path. You can only move **right** or **down**.

**Example:**
```
Input: n = 3
Grid:
  1  3  1
  1  5  1
  4  2  1

Output: 7
Path: (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2)
Costs: 1 + 3 + 1 + 1 + 1 = 7
```

**Constraints:**
- 1 <= n <= 1000
- 0 <= grid[i][j] <= 10^6

## Intuition

The key insight is that to reach any cell `(i,j)`, we must come from either:
- The cell above: `(i-1, j)`
- The cell to the left: `(i, j-1)`

To minimize the total cost to reach `(i,j)`, we should come from whichever predecessor has the smaller accumulated cost, then add the current cell's value.

This is the **optimal substructure** property: the optimal solution to the whole problem contains optimal solutions to subproblems.

## DP State Definition

```
dp[i][j] = minimum sum to reach cell (i, j) starting from (0, 0)
```

The answer will be `dp[n-1][n-1]`.

## State Transition

For any cell `(i,j)` where `i > 0` and `j > 0`:

```
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
```

We take the minimum cost from either coming from above or from the left.

## Base Cases

```
dp[0][0] = grid[0][0]                    # Starting cell

dp[0][j] = dp[0][j-1] + grid[0][j]       # First row: can only come from left
dp[i][0] = dp[i-1][0] + grid[i][0]       # First column: can only come from above
```

## Visual Diagram

For the example grid, here is how the DP table is filled:

```
Original Grid:          DP Table (minimum cost to reach):
  1  3  1                 1  4  5
  1  5  1       -->       2  7  6
  4  2  1                 6  8  7

Step-by-step fill:
dp[0][0] = 1
dp[0][1] = 1 + 3 = 4
dp[0][2] = 4 + 1 = 5
dp[1][0] = 1 + 1 = 2
dp[1][1] = 5 + min(4, 2) = 5 + 2 = 7
dp[1][2] = 1 + min(5, 7) = 1 + 5 = 6
dp[2][0] = 2 + 4 = 6
dp[2][1] = 2 + min(7, 6) = 2 + 6 = 8
dp[2][2] = 1 + min(6, 8) = 1 + 6 = 7

Answer: dp[2][2] = 7
```

## Detailed Dry Run

**Grid:**
```
Row 0: [1, 3, 1]
Row 1: [1, 5, 1]
Row 2: [4, 2, 1]
```

| Step | Cell | From Above | From Left | Calculation | dp[i][j] |
|------|------|------------|-----------|-------------|----------|
| 1 | (0,0) | - | - | grid[0][0] | 1 |
| 2 | (0,1) | - | dp[0][0]=1 | 1 + 3 | 4 |
| 3 | (0,2) | - | dp[0][1]=4 | 4 + 1 | 5 |
| 4 | (1,0) | dp[0][0]=1 | - | 1 + 1 | 2 |
| 5 | (1,1) | dp[0][1]=4 | dp[1][0]=2 | min(4,2) + 5 | 7 |
| 6 | (1,2) | dp[0][2]=5 | dp[1][1]=7 | min(5,7) + 1 | 6 |
| 7 | (2,0) | dp[1][0]=2 | - | 2 + 4 | 6 |
| 8 | (2,1) | dp[1][1]=7 | dp[2][0]=6 | min(7,6) + 2 | 8 |
| 9 | (2,2) | dp[1][2]=6 | dp[2][1]=8 | min(6,8) + 1 | 7 |

## Python Implementation

```python
def min_path_sum(grid):
  """Find minimum path sum from top-left to bottom-right."""
  n = len(grid)
  if n == 0:
    return 0
  m = len(grid[0])

  # Create DP table
  dp = [[0] * m for _ in range(n)]

  # Base case
  dp[0][0] = grid[0][0]

  # Fill first row
  for j in range(1, m):
    dp[0][j] = dp[0][j-1] + grid[0][j]

  # Fill first column
  for i in range(1, n):
    dp[i][0] = dp[i-1][0] + grid[i][0]

  # Fill rest of the table
  for i in range(1, n):
    for j in range(1, m):
      dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

  return dp[n-1][m-1]


# Example usage
grid = [
  [1, 3, 1],
  [1, 5, 1],
  [4, 2, 1]
]
print(min_path_sum(grid))  # Output: 7
```

## Path Reconstruction

To find the actual path (not just the minimum cost), backtrack from the destination:

```python
def min_path_sum_with_path(grid):
  """Find minimum path sum and return the actual path."""
  n, m = len(grid), len(grid[0])
  dp = [[0] * m for _ in range(n)]

  # Fill DP table (same as before)
  dp[0][0] = grid[0][0]
  for j in range(1, m):
    dp[0][j] = dp[0][j-1] + grid[0][j]
  for i in range(1, n):
    dp[i][0] = dp[i-1][0] + grid[i][0]
  for i in range(1, n):
    for j in range(1, m):
      dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

  # Backtrack to find path
  path = []
  i, j = n - 1, m - 1
  while i > 0 or j > 0:
    path.append((i, j))
    if i == 0:
      j -= 1
    elif j == 0:
      i -= 1
    elif dp[i-1][j] < dp[i][j-1]:
      i -= 1
    else:
      j -= 1
  path.append((0, 0))

  return dp[n-1][m-1], path[::-1]
```

## Space Optimization to O(n)

Since each row only depends on the current row and the previous row, we can reduce space to O(n):

```python
def min_path_sum_optimized(grid):
  """Space-optimized O(n) solution."""
  n, m = len(grid), len(grid[0])

  # Use single row
  dp = [0] * m

  for i in range(n):
    for j in range(m):
      if i == 0 and j == 0:
        dp[j] = grid[0][0]
      elif i == 0:
        dp[j] = dp[j-1] + grid[i][j]
      elif j == 0:
        dp[j] = dp[j] + grid[i][j]
      else:
        dp[j] = grid[i][j] + min(dp[j], dp[j-1])

  return dp[m-1]
```

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Forgetting base cases | First row/col have only one incoming direction | Initialize first row and column separately |
| Using `max()` instead of `min()` | Problem asks for minimum path | Use `min(dp[i-1][j], dp[i][j-1])` |
| Off-by-one errors | Grid indices start at 0 | Iterate from 1 to n-1 for inner cells |
| Not including start cell | Start cell cost matters | `dp[0][0] = grid[0][0]` |

## Counting Paths vs Minimum Path

| Aspect | Counting Paths | Minimum Path Sum |
|--------|----------------|------------------|
| DP State | Number of ways to reach (i,j) | Min cost to reach (i,j) |
| Transition | `dp[i][j] = dp[i-1][j] + dp[i][j-1]` | `dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]` |
| Base Case | `dp[0][0] = 1` | `dp[0][0] = grid[0][0]` |
| Operation | Addition (counting) | min() + Addition (optimization) |

## Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Recursive (brute force) | O(2^(n+m)) | O(n+m) |
| DP with 2D table | O(n * m) | O(n * m) |
| DP space-optimized | O(n * m) | O(m) |

## Related Problems

- **LeetCode 64**: Minimum Path Sum (identical problem)
- **LeetCode 62**: Unique Paths (counting variant)
- **LeetCode 63**: Unique Paths II (with obstacles)
- **CSES Grid Paths**: https://cses.fi/problemset/task/1638 (counting paths variant)
