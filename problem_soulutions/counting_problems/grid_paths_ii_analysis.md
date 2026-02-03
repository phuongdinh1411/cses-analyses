---
layout: simple
title: "Grid Paths II - Counting Problem"
permalink: /problem_soulutions/counting_problems/grid_paths_ii_analysis
difficulty: Medium
tags: [dynamic-programming, grid, counting, obstacles]
prerequisites: [grid_paths]
---

# Grid Paths II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Dynamic Programming |
| **Time Limit** | 1 second |
| **Key Technique** | Grid DP with Obstacles |
| **CSES Link** | [Grid Paths II](https://cses.fi/problemset/task/1638) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply dynamic programming to count paths in a 2D grid with obstacles
- [ ] Handle blocked cells by setting their DP value to zero
- [ ] Optimize space complexity from O(n^2) to O(n) using a rolling array
- [ ] Recognize the grid path counting pattern in similar problems

---

## Problem Statement

**Problem:** Given an n x n grid where some cells are blocked, count the number of paths from the top-left corner (1,1) to the bottom-right corner (n,n). You can only move right or down.

**Input:**
- Line 1: integer n (grid size)
- Lines 2 to n+1: n characters each ('.' = empty, '*' = blocked)

**Output:**
- Number of valid paths modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 1000

### Example

```
Input:
4
....
.*..
..*.
....

Output:
3
```

**Explanation:** The three valid paths from (1,1) to (4,4) avoiding obstacles:
1. Right -> Right -> Right -> Down -> Down -> Down
2. Down -> Right -> Right -> Down -> Down -> Right
3. Down -> Down -> Right -> Right -> Down -> Right

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How does adding obstacles change the basic grid path counting problem?

Without obstacles, the number of paths to any cell (i,j) is the sum of paths to (i-1,j) and (i,j-1). With obstacles, we simply set the path count to 0 for any blocked cell, which naturally propagates through the DP computation.

### Breaking Down the Problem

1. **What are we counting?** Paths from top-left to bottom-right using only right/down moves
2. **How do obstacles affect paths?** A blocked cell cannot be part of any path, so dp[i][j] = 0
3. **What's the recurrence?** dp[i][j] = dp[i-1][j] + dp[i][j-1] (if cell is not blocked)

### Analogy

Imagine water flowing from the top-left corner. It can only flow right or down. Obstacles are like dams that block flow completely. The amount of water reaching the bottom-right is the sum of all possible flow paths.

---

## Solution 1: Brute Force (DFS)

### Idea

Try all possible paths using recursion. At each cell, branch into two choices: go right or go down.

### Algorithm

1. Start at (0,0)
2. If current cell is blocked or out of bounds, return 0
3. If reached destination, return 1
4. Recursively count paths going right + paths going down

### Code

```python
def count_paths_brute(grid):
    """
    Brute force DFS solution.
    Time: O(2^(2n)) - exponential
    Space: O(n) - recursion depth
    """
    n = len(grid)

    def dfs(i, j):
        if i >= n or j >= n or grid[i][j] == '*':
            return 0
        if i == n - 1 and j == n - 1:
            return 1
        return dfs(i + 1, j) + dfs(i, j + 1)

    return dfs(0, 0)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^(2n)) | Each cell branches into 2 paths |
| Space | O(n) | Maximum recursion depth |

### Why This Works (But Is Slow)

The recursion explores all valid paths, but recomputes the same subproblems many times. For example, paths through (2,3) are recalculated for every path that reaches (2,3).

---

## Solution 2: Optimal Solution (Bottom-Up DP)

### Key Insight

> **The Trick:** The number of paths to cell (i,j) only depends on paths to (i-1,j) and (i,j-1). Process cells in order so dependencies are always computed first.

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i][j]` | Number of paths from (0,0) to (i,j) avoiding obstacles |

**In plain English:** dp[i][j] answers "How many ways can I reach cell (i,j) from the start?"

### State Transition

```
dp[i][j] = 0                           if grid[i][j] == '*'
dp[i][j] = dp[i-1][j] + dp[i][j-1]     otherwise
```

**Why?** Every path to (i,j) must come from either above (i-1,j) or left (i,j-1). Blocked cells contribute 0 paths.

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0][0]` | 1 if empty, 0 if blocked | Starting point has 1 way to reach itself |
| First row | Propagate from left | Can only come from the left |
| First column | Propagate from above | Can only come from above |

### Algorithm

1. Initialize dp[0][0] = 1 (if not blocked)
2. Fill first row: dp[0][j] = dp[0][j-1] if empty
3. Fill first column: dp[i][0] = dp[i-1][0] if empty
4. Fill rest: dp[i][j] = dp[i-1][j] + dp[i][j-1] if empty
5. Return dp[n-1][n-1]

### Dry Run Example

Let's trace through with a simple 3x3 grid:

```
Grid (0-indexed):
. . .    (row 0)
. * .    (row 1, obstacle at (1,1))
. . .    (row 2)

Step 1: Initialize dp[0][0] = 1
dp = [1, 0, 0]
     [0, 0, 0]
     [0, 0, 0]

Step 2: Fill first row (propagate from left)
dp[0][1] = dp[0][0] = 1
dp[0][2] = dp[0][1] = 1
dp = [1, 1, 1]
     [0, 0, 0]
     [0, 0, 0]

Step 3: Fill first column (propagate from above)
dp[1][0] = dp[0][0] = 1
dp[2][0] = dp[1][0] = 1
dp = [1, 1, 1]
     [1, 0, 0]
     [1, 0, 0]

Step 4: Fill remaining cells row by row
(1,1): blocked -> stays 0
(1,2): dp[0][2] + dp[1][1] = 1 + 0 = 1
dp = [1, 1, 1]
     [1, 0, 1]
     [1, 0, 0]

(2,1): dp[1][1] + dp[2][0] = 0 + 1 = 1
(2,2): dp[1][2] + dp[2][1] = 1 + 1 = 2
dp = [1, 1, 1]
     [1, 0, 1]
     [1, 1, 2]  <- Final answer: 2 paths

The 2 paths are:
  Path 1: (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2)
  Path 2: (0,0) -> (1,0) -> (2,0) -> (2,1) -> (2,2)
```

### Code (Python)

```python
import sys
input = sys.stdin.readline

def solve():
    MOD = 10**9 + 7
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    # Edge case: start or end blocked
    if grid[0][0] == '*' or grid[n-1][n-1] == '*':
        print(0)
        return

    # DP table
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1

    # Fill first row
    for j in range(1, n):
        if grid[0][j] == '.':
            dp[0][j] = dp[0][j-1]

    # Fill first column
    for i in range(1, n):
        if grid[i][0] == '.':
            dp[i][0] = dp[i-1][0]

    # Fill rest of the table
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] == '.':
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD

    print(dp[n-1][n-1])

solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<string> grid(n);
    for (int i = 0; i < n; i++) {
        cin >> grid[i];
    }

    // Edge case: start or end blocked
    if (grid[0][0] == '*' || grid[n-1][n-1] == '*') {
        cout << 0 << "\n";
        return 0;
    }

    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    dp[0][0] = 1;

    // Fill first row
    for (int j = 1; j < n; j++) {
        if (grid[0][j] == '.') {
            dp[0][j] = dp[0][j-1];
        }
    }

    // Fill first column
    for (int i = 1; i < n; i++) {
        if (grid[i][0] == '.') {
            dp[i][0] = dp[i-1][0];
        }
    }

    // Fill rest
    for (int i = 1; i < n; i++) {
        for (int j = 1; j < n; j++) {
            if (grid[i][j] == '.') {
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD;
            }
        }
    }

    cout << dp[n-1][n-1] << "\n";
    return 0;
}
```

### Space-Optimized Solution (O(n) space)

Since each row only depends on the previous row, we can use a single array:

```python
def solve_optimized():
    MOD = 10**9 + 7
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    if grid[0][0] == '*' or grid[n-1][n-1] == '*':
        print(0)
        return

    dp = [0] * n
    dp[0] = 1

    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[j] = 0
            elif j > 0:
                dp[j] = (dp[j] + dp[j-1]) % MOD

    print(dp[n-1])
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^2) | Visit each cell once |
| Space | O(n^2) or O(n) | Full DP table or rolling array |

---

## Common Mistakes

### Mistake 1: Forgetting to Check Start/End

```python
# WRONG - crashes or gives wrong answer if start blocked
dp[0][0] = 1
for i in range(n):
    for j in range(n):
        ...

# CORRECT
if grid[0][0] == '*' or grid[n-1][n-1] == '*':
    print(0)
    return
dp[0][0] = 1
```

**Problem:** If start or end is blocked, there are 0 paths.
**Fix:** Check and handle this edge case first.

### Mistake 2: Wrong Obstacle Character

```python
# WRONG - using '#' instead of '*'
if grid[i][j] == '#':
    dp[i][j] = 0

# CORRECT - CSES uses '*' for obstacles
if grid[i][j] == '*':
    dp[i][j] = 0
```

**Problem:** Different problems use different characters for obstacles.
**Fix:** Read the problem statement carefully for the exact format.

### Mistake 3: Integer Overflow (C++)

```cpp
// WRONG - may overflow before mod
dp[i][j] = dp[i-1][j] + dp[i][j-1];
dp[i][j] %= MOD;

// CORRECT - use long long and mod during addition
dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD;
```

### Mistake 4: Not Handling First Row/Column Correctly

```python
# WRONG - doesn't stop propagation after obstacle
for j in range(1, n):
    dp[0][j] = dp[0][j-1]  # Missing obstacle check!

# CORRECT
for j in range(1, n):
    if grid[0][j] == '.':
        dp[0][j] = dp[0][j-1]
    # else dp[0][j] stays 0
```

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Start blocked | `*...` | 0 | Cannot begin |
| End blocked | `...*` | 0 | Cannot finish |
| Single cell empty | n=1, `.` | 1 | Already at destination |
| Single cell blocked | n=1, `*` | 0 | Blocked |
| Full row blocked | Row of `*` | 0 | No path through |
| Full column blocked | Column of `*` | 0 | No path through |
| No obstacles | All `.` | C(2n-2, n-1) | Catalan-related |

---

## When to Use This Pattern

### Use Grid DP When:
- Counting paths in a 2D grid with movement constraints
- Grid has obstacles or varying cell costs
- Can only move in limited directions (right, down, etc.)
- Subproblems overlap (same cell reached via different paths)

### Don't Use When:
- Need to find the actual path (use backtracking or parent pointers)
- Movements can go in all 4 directions (use BFS/DFS instead)
- Need shortest path with weights (use Dijkstra)

### Pattern Recognition Checklist:
- [ ] Grid with restricted movement? -> **Grid DP**
- [ ] Counting paths, not finding one? -> **Grid DP**
- [ ] Obstacles blocking some cells? -> **Set dp[blocked] = 0**
- [ ] Need space optimization? -> **Use rolling array**

---

## Related Problems

### Easier (Do These First)

| Problem | Link | Why It Helps |
|---------|------|--------------|
| Grid Paths | [CSES 1638](https://cses.fi/problemset/task/1638) | Same problem, simpler constraints |

### Similar Difficulty

| Problem | Link | Key Difference |
|---------|------|----------------|
| Edit Distance | [CSES 1639](https://cses.fi/problemset/task/1639) | Grid DP with different transitions |
| Rectangle Cutting | [CSES 1744](https://cses.fi/problemset/task/1744) | 2D DP optimization |

### Harder (Do These After)

| Problem | Link | New Concept |
|---------|------|-------------|
| Book Shop | [CSES 1158](https://cses.fi/problemset/task/1158) | Knapsack DP |
| Projects | [CSES 1140](https://cses.fi/problemset/task/1140) | DP with sorting |

---

## Key Takeaways

1. **The Core Idea:** Paths to (i,j) = paths from above + paths from left; blocked cells contribute 0
2. **Time Optimization:** DP reduces exponential brute force to O(n^2)
3. **Space Trade-off:** Can reduce from O(n^2) to O(n) with rolling array
4. **Pattern:** Classic grid DP - fundamental for many 2D counting problems

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why blocked cells propagate correctly through DP
- [ ] Implement the space-optimized O(n) solution
- [ ] Handle all edge cases (blocked start/end, single cell)
- [ ] Implement in both Python and C++ in under 15 minutes
