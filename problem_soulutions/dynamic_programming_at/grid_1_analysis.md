---
layout: simple
title: "Grid 1 - 2D Grid DP Problem"
permalink: /problem_soulutions/dynamic_programming_at/grid_1_analysis
difficulty: Easy
tags: [dp, grid, path-counting, 2d-dp]
---

# Grid 1

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [AtCoder DP Contest - Problem H](https://atcoder.jp/contests/dp/tasks/dp_h) |
| **Difficulty** | Easy |
| **Category** | Dynamic Programming (2D Grid) |
| **Time Limit** | 2 seconds |
| **Key Technique** | Grid DP with Obstacle Handling |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply dynamic programming on 2D grids
- [ ] Handle obstacles (blocked cells) in grid path counting
- [ ] Optimize space from O(H*W) to O(W) using rolling arrays
- [ ] Recognize the grid path counting pattern in related problems

---

## Problem Statement

**Problem:** Count the number of paths from the top-left corner to the bottom-right corner of a grid, where you can only move right or down, avoiding walls.

**Input:**
- Line 1: H W (grid dimensions)
- Lines 2 to H+1: W characters each ('.' = road, '#' = wall)

**Output:**
- Number of valid paths modulo 10^9 + 7

**Constraints:**
- 2 <= H, W <= 1000
- Starting cell (1,1) and ending cell (H,W) are always roads

### Example

```
Input:
3 4
..#.
....
#...

Output:
3
```

**Explanation:** The grid looks like:
```
. . # .
. . . .
# . . .
```

Three valid paths exist:
1. Right -> Down -> Right -> Right -> Down
2. Down -> Right -> Right -> Right -> Down
3. Down -> Right -> Down -> Right -> Right

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we count paths without enumerating all of them?

The number of paths to any cell equals the sum of paths to cells that can reach it. Since we can only move right or down, a cell (i,j) can only be reached from (i-1,j) or (i,j-1).

### Breaking Down the Problem

1. **What are we looking for?** Total number of distinct paths from (0,0) to (H-1,W-1)
2. **What information do we have?** Grid with passable cells and walls
3. **What's the relationship?** `paths(i,j) = paths(i-1,j) + paths(i,j-1)` if cell is passable

### Analogies

Think of water flowing from the top-left corner. At each intersection, the water splits into streams going right and down. Walls block the flow. The total water reaching the bottom-right is the sum of all streams that made it through.

---

## Solution 1: Brute Force (Recursion)

### Idea

Recursively explore all paths by trying both directions (right and down) at each cell.

### Code

```python
def solve_recursive(h, w, grid):
  """Brute force recursive solution. TLE for large inputs."""
  MOD = 10**9 + 7

  def count_paths(i, j):
    if i >= h or j >= w or grid[i][j] == '#':
      return 0
    if i == h - 1 and j == w - 1:
      return 1
    return (count_paths(i + 1, j) + count_paths(i, j + 1)) % MOD

  return count_paths(0, 0)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^(H+W)) | Each cell branches into 2 choices |
| Space | O(H+W) | Recursion stack depth |

### Why This Works (But Is Slow)

Correctness is guaranteed because we explore every possible path. However, we recalculate the same subproblems exponentially many times.

---

## Solution 2: Optimal Solution (Bottom-Up DP)

### Key Insight

> **The Trick:** `dp[i][j]` stores the count of paths to reach cell (i,j). Build the answer iteratively from (0,0) to (H-1,W-1).

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Number of paths from (0,0) to (i,j) |

**In plain English:** For each cell, store how many different ways we can reach it from the start.

### State Transition

```
dp[i][j] = dp[i-1][j] + dp[i][j-1]  (if grid[i][j] == '.')
dp[i][j] = 0                         (if grid[i][j] == '#')
```

**Why?** To reach (i,j), we must come from either above (i-1,j) or left (i,j-1). The total paths is the sum of both.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0][0]` | 1 | One way to be at start (do nothing) |
| Wall cell | 0 | Cannot pass through walls |
| Out of bounds | 0 | Treat as inaccessible |

### Dry Run Example

Let's trace through with a simpler 2x3 grid:

```
Input:
2 3
...
.#.

Grid visualization (0-indexed):
     j=0  j=1  j=2
i=0   .    .    .
i=1   .    #    .

Step-by-step DP construction:

Initial: dp[0][0] = 1 (starting position)

Processing row 0 (first row):
  dp[0][0] = 1           (base case)
  dp[0][1] = 0 + 1 = 1   (from left only)
  dp[0][2] = 0 + 1 = 1   (from left only)

Processing row 1 (second row):
  dp[1][0] = 1 + 0 = 1   (from top only)
  dp[1][1] = 0           (wall - blocked!)
  dp[1][2] = 1 + 0 = 1   (from top only, left is wall)

Final DP table:
     j=0  j=1  j=2
i=0   1    1    1
i=1   1    #    1

Answer: dp[1][2] = 1
```

**Trace the single valid path:**
```
(0,0) -> (0,1) -> (0,2) -> (1,2)
  R       R       D
```
The wall at (1,1) blocks the path going down first then right.

### Code

**Python Solution:**
```python
def solve(h, w, grid):
  """
  Count paths in grid with obstacles.

  Time: O(H * W)
  Space: O(H * W)
  """
  MOD = 10**9 + 7

  # Handle edge case: start or end is a wall
  if grid[0][0] == '#' or grid[h-1][w-1] == '#':
    return 0

  dp = [[0] * w for _ in range(h)]
  dp[0][0] = 1

  for i in range(h):
    for j in range(w):
      if grid[i][j] == '#':
        dp[i][j] = 0
      elif i == 0 and j == 0:
        continue  # Already initialized
      else:
        from_top = dp[i-1][j] if i > 0 else 0
        from_left = dp[i][j-1] if j > 0 else 0
        dp[i][j] = (from_top + from_left) % MOD

  return dp[h-1][w-1]

# Input handling
h, w = map(int, input().split())
grid = [input().strip() for _ in range(h)]
print(solve(h, w, grid))
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(H * W) | Visit each cell exactly once |
| Space | O(H * W) | Store DP table for all cells |

---

## Solution 3: Space-Optimized DP

### Key Insight

Since we only need the previous row to compute the current row, we can reduce space to O(W).

**Python:**
```python
def solve_optimized(h, w, grid):
  MOD = 10**9 + 7
  if grid[0][0] == '#' or grid[h-1][w-1] == '#':
    return 0
  dp = [0] * w
  for i in range(h):
    for j in range(w):
      if grid[i][j] == '#':
        dp[j] = 0
      elif i == 0 and j == 0:
        dp[j] = 1
      else:
        from_left = dp[j-1] if j > 0 else 0
        dp[j] = (dp[j] + from_left) % MOD  # dp[j] has value from row above
  return dp[w-1]
```

**Complexity:** Time O(H*W), Space O(W)

---

## Common Mistakes

### Mistake 1: Forgetting to Check Start/End Cells

```python
# WRONG - crashes or gives wrong answer if start is wall
dp[0][0] = 1

# CORRECT
if grid[0][0] == '#' or grid[h-1][w-1] == '#':
  return 0
dp[0][0] = 1
```

### Mistake 3: Not Resetting Wall Cells in Space-Optimized Version

```python
# WRONG - wall cell retains value from previous row
if grid[i][j] == '#':
  continue  # dp[j] keeps old value!

# CORRECT - explicitly set to 0
if grid[i][j] == '#':
  dp[j] = 0
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Start is wall | `grid[0][0] = '#'` | 0 | Cannot begin journey |
| End is wall | `grid[H-1][W-1] = '#'` | 0 | Cannot reach destination |
| Path blocked | Wall separating start from end | 0 | No valid path exists |
| No walls | All cells are '.' | C(H+W-2, H-1) | Standard grid path count |
| Single cell | H=1, W=1 | 1 | Already at destination |
| Single row | H=1 | 1 or 0 | Only rightward movement |

---

## When to Use This Pattern

### Use This Approach When:
- Counting paths in a 2D grid with movement constraints
- Movement is restricted to certain directions (right/down, or 4/8 directions)
- Grid contains obstacles that block paths
- Answer needs to be computed modulo a large prime

### Don't Use When:
- Finding shortest path (use BFS instead)
- Finding minimum cost path (use Dijkstra or DP with min)
- Grid is very sparse (consider graph representation)
- Need to reconstruct the actual path (need parent tracking)

### Pattern Recognition Checklist:
- [ ] Grid-based problem with path counting? **Consider Grid DP**
- [ ] Only certain movement directions allowed? **Standard grid DP applies**
- [ ] Obstacles present? **Set dp[obstacle] = 0**
- [ ] Very large grid with few obstacles? **Consider combinatorics with inclusion-exclusion**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Unique Paths (LC 62)](https://leetcode.com/problems/unique-paths/) | Same problem without obstacles |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Unique Paths II (LC 63)](https://leetcode.com/problems/unique-paths-ii/) | Nearly identical problem |
| [CSES Grid Paths](https://cses.fi/problemset/task/1638) | Same concept, different platform |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Grid 2 (AtCoder DP Y)](https://atcoder.jp/contests/dp/tasks/dp_y) | Sparse obstacles, combinatorics |
| [Minimum Path Sum (LC 64)](https://leetcode.com/problems/minimum-path-sum/) | Optimization instead of counting |
| [Cherry Pickup (LC 741)](https://leetcode.com/problems/cherry-pickup/) | Two simultaneous paths |

---

## Key Takeaways

1. **The Core Idea:** Path count to any cell = sum of path counts from cells that can reach it
2. **Time Optimization:** DP avoids recounting by storing intermediate results
3. **Space Trade-off:** O(W) space suffices since we only need the previous row
4. **Pattern:** This is the foundation for all grid DP problems

**Practice Checklist:** Before moving on, ensure you can solve this without looking at the solution, explain the recurrence relation, and implement the space-optimized version.
