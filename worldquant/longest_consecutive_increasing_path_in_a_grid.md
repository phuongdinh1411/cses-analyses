---
layout: simple
title: "Longest Consecutive-Increasing Path in a Grid"
permalink: /worldquant/longest_consecutive_increasing_path_in_a_grid
difficulty: Medium
tags: [dfs, memoization, grid, dp, worldquant]
---

# Longest Consecutive-Increasing Path in a Grid

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Graph / DFS / DP on Grid |
| **Key Technique** | DFS with memoization (top-down DP) |

### Learning Goals
- [ ] Apply DFS with memoization on a 2D grid
- [ ] Recognise that the DAG structure (strictly increasing) prevents cycles
- [ ] Find the longest path in a DAG efficiently

### In 60 seconds
- **Pattern:** DFS + memoization on a DAG
- **Key insight:** Edges only go to a neighbour with value + 1, so the grid is a DAG and `best[cell] = 1 + max(best[next])` can be cached.
- **Complexity:** O(R·C) time and space
- **Trap:** Deep recursion on long paths: use the iterative value-descending version or raise the recursion limit.

> **Say this in the interview:** "Strictly increasing edges mean no cycles, so memoized DFS visits each cell once."

---

## Problem Statement

Given an `m x n` integer grid, find the length of the **longest path** where:
1. Each step moves to an **adjacent cell** (up, down, left, right — no diagonals)
2. Each cell's value must be **exactly 1 more** than the previous cell

Return the length of the longest such path (a single cell has length 1).

**Input:**
- A 2D integer grid of size `m x n`

**Output:**
- A single integer: the length of the longest consecutive-increasing path

**Constraints:**
- `1 <= m, n <= 200`
- `0 <= grid[i][j] <= 10^6`

---

## Examples

### Example 1
```
Input:
grid = [[1, 2, 3],
        [6, 5, 4],
        [7, 8, 9]]

Output: 9

Explanation:
Path: 1→2→3→4→5→6→7→8→9 (snake through the grid)
```

### Example 2
```
Input:
grid = [[3, 4, 5],
        [3, 2, 6],
        [2, 2, 1]]

Output: 4

Path: (0,0)=3 → (0,1)=4 → (0,2)=5 → (1,2)=6
The 2 at (1,1) reaches the 3 at (1,0), but that 3 has no adjacent 4, so that path stops at length 2.
```

### Example 3
```
Input:
grid = [[1]]
Output: 1
```

---

## Approach: DFS + Memoization

Because the path is **strictly consecutive-increasing** (each step = +1), the grid defines a **DAG** — no cycles are possible. We can safely apply top-down DP.

`dp[r][c]` = length of the longest consecutive-increasing path starting at `(r, c)`.

### Recurrence

```
dp[r][c] = 1 + max(dp[nr][nc])
           for each (nr, nc) adjacent to (r, c)
           where grid[nr][nc] == grid[r][c] + 1
```

Base case: if no valid neighbour exists, `dp[r][c] = 1`.

### Algorithm

```
1. Initialise memo table of size m x n with 0.
2. For each cell (r, c), call dfs(r, c) if not yet computed.
3. dfs(r, c):
   a. If memo[r][c] != 0, return it.
   b. best = 1
   c. For each of 4 directions:
      if in bounds and grid[nr][nc] == grid[r][c] + 1:
        best = max(best, 1 + dfs(nr, nc))
   d. memo[r][c] = best; return best
4. Return max over all cells.
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(m × n) — each cell computed once |
| **Space** | O(m × n) memo table + up to O(m × n) recursion depth |

---

## Implementation

```python
def longest_consecutive_path(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    memo = [[0] * n for _ in range(m)]
    DIRS = [(0,1),(0,-1),(1,0),(-1,0)]

    def dfs(r, c):
        if memo[r][c]:
            return memo[r][c]
        best = 1
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                if grid[nr][nc] == grid[r][c] + 1:
                    best = max(best, 1 + dfs(nr, nc))
        memo[r][c] = best
        return best

    return max(dfs(r, c) for r in range(m) for c in range(n))
```

**Recursion depth:** a snake-shaped path can be `m × n = 40,000` cells long, far beyond Python's default recursion limit (1000). Either raise it with `sys.setrecursionlimit` (and risk the C stack) or use the iterative version below.

### Iterative version (no recursion)

Every step goes from value `v` to `v + 1`, so processing cells in **decreasing** value order guarantees each neighbour's answer is ready.

```python
def longest_consecutive_path_iter(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[1] * n for _ in range(m)]
    cells = sorted(((grid[r][c], r, c) for r in range(m) for c in range(n)), reverse=True)
    for v, r, c in cells:
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == v + 1:
                dp[r][c] = max(dp[r][c], 1 + dp[nr][nc])
    return max(map(max, dp))
```

Time O(mn log mn) for the sort, space O(mn).

---

## Dry Run — Example 1

```
grid = [[1,2,3],
        [6,5,4],
        [7,8,9]]
```

Starting at (0,0)=1:
- (0,0)=1 → (0,1)=2 → (0,2)=3 → (1,2)=4 → (1,1)=5 → (1,0)=6 → (2,0)=7 → (2,1)=8 → (2,2)=9

`dp[0][0] = 9` → answer = **9** ✅

---

## Variant: Longest Increasing Path (any positive step)

If the constraint is `grid[next] > grid[curr]` (not necessarily +1), the same DFS + memo approach works. This is LeetCode 329.

```python
# sketch: inside dfs, replace the == grid[r][c] + 1 test with
if grid[nr][nc] > grid[r][c]:
    best = max(best, 1 + dfs(nr, nc))
```

---

## Related Problems

| Problem | Note |
|---|---|
| LeetCode 329 — Longest Increasing Path in a Matrix | Any increase, not just +1 |
| LeetCode 2328 — Number of Increasing Paths | Count of all increasing paths |
| Three-Way Equal-Value Partition | Different grid/string partition problem |
