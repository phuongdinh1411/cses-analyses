---
layout: simple
title: "Grid Coloring I - Backtracking Problem"
permalink: /problem_soulutions/introductory_problems/grid_coloring_i_analysis
difficulty: Easy
tags: [backtracking, grid, constraint-satisfaction, recursion]
---

# Grid Coloring I

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Backtracking |
| **Time Limit** | 1 second |
| **Key Technique** | Backtracking with Constraint Checking |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize when backtracking is appropriate for constraint satisfaction problems
- [ ] Implement backtracking with early pruning using constraint checking
- [ ] Understand how to model grid-based problems as search problems
- [ ] Apply the pattern of "try, validate, recurse or backtrack"

---

## Problem Statement

**Problem:** Color an n x n grid using k colors such that no two adjacent cells (sharing an edge) have the same color. Output any valid coloring, or "NO" if impossible.

**Input:**
- Line 1: Two integers n and k - grid size and number of colors

**Output:**
- n lines of n integers each representing the grid coloring (colors numbered 1 to k)
- Or "NO" if no valid coloring exists

**Constraints:**
- 1 <= n <= 10
- 1 <= k <= 4

### Example

```
Input:
3 3

Output:
1 2 1
2 3 2
1 2 1
```

**Explanation:** Each cell is colored with one of 3 colors. No two horizontally or vertically adjacent cells share the same color. For example, cell (0,0)=1 is adjacent to (0,1)=2 and (1,0)=2, all different.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we systematically explore all possible colorings while avoiding invalid states early?

This is a classic constraint satisfaction problem. We need to assign colors to cells such that constraints (no adjacent same colors) are satisfied. Backtracking allows us to explore possibilities and prune invalid branches early.

### Breaking Down the Problem

1. **What are we looking for?** A valid assignment of colors 1 to k for each cell in the n x n grid.
2. **What information do we have?** Grid dimensions, number of colors, and adjacency constraints.
3. **What's the relationship between input and output?** We need at least 2 colors for any n > 1 (checkerboard pattern works).

### Analogies

Think of this problem like solving a simplified Sudoku. Instead of 9 different constraints per cell, we only check 2: the left and top neighbors. We fill in cells one by one, backing up when we hit a dead end.

---

## Solution 1: Brute Force

### Idea

Generate all possible color assignments for the grid, then check each one for validity.

### Algorithm

1. Generate all k^(n*n) possible colorings
2. For each coloring, verify no adjacent cells share colors
3. Return the first valid coloring found

### Code

```python
def solve_brute_force(n, k):
    """
    Brute force: try all colorings, validate each.

    Time: O(k^(n^2) * n^2)
    Space: O(n^2)
    """
    def is_valid(grid):
        for i in range(n):
            for j in range(n):
                if j + 1 < n and grid[i][j] == grid[i][j + 1]:
                    return False
                if i + 1 < n and grid[i][j] == grid[i + 1][j]:
                    return False
        return True

    def generate(grid, pos):
        if pos == n * n:
            return grid if is_valid(grid) else None

        row, col = pos // n, pos % n
        for color in range(1, k + 1):
            grid[row][col] = color
            result = generate(grid, pos + 1)
            if result:
                return result
        return None

    grid = [[0] * n for _ in range(n)]
    return generate(grid, 0)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(k^(n^2) * n^2) | k^(n^2) colorings, O(n^2) validation each |
| Space | O(n^2) | Store the grid |

### Why This Works (But Is Slow)

We explore every possible coloring, so we are guaranteed to find a solution if one exists. However, we do not prune invalid partial solutions, wasting time exploring branches that are already invalid.

---

## Solution 2: Optimal Solution (Backtracking with Pruning)

### Key Insight

> **The Trick:** Check constraints immediately when placing a color. If a cell conflicts with its already-colored neighbors, skip that color without exploring further.

### Algorithm

1. Process cells in row-major order (left to right, top to bottom)
2. For each cell, try colors 1 to k
3. Before placing a color, check only left and top neighbors (already colored)
4. If valid, recurse to the next cell
5. If all colors fail, backtrack

### Dry Run Example

Let's trace through with input `n = 3, k = 2`:

```
Initial state: Empty 3x3 grid

Step 1: Cell (0,0)
  Try color 1 -> No neighbors to check -> Place 1
  Grid: [1, 0, 0]
        [0, 0, 0]
        [0, 0, 0]

Step 2: Cell (0,1)
  Try color 1 -> Left neighbor is 1 -> CONFLICT
  Try color 2 -> Left neighbor is 1 -> OK -> Place 2
  Grid: [1, 2, 0]
        [0, 0, 0]
        [0, 0, 0]

Step 3: Cell (0,2)
  Try color 1 -> Left neighbor is 2 -> OK -> Place 1
  Grid: [1, 2, 1]
        [0, 0, 0]
        [0, 0, 0]

Step 4: Cell (1,0)
  Try color 1 -> Top neighbor is 1 -> CONFLICT
  Try color 2 -> Top neighbor is 1 -> OK -> Place 2
  Grid: [1, 2, 1]
        [2, 0, 0]
        [0, 0, 0]

Step 5: Cell (1,1)
  Try color 1 -> Left=2 OK, Top=2 OK -> Place 1
  Grid: [1, 2, 1]
        [2, 1, 0]
        [0, 0, 0]

... continue until complete ...

Final Grid:
  [1, 2, 1]
  [2, 1, 2]
  [1, 2, 1]
```

### Visual Diagram

```
Color placement order:    Constraint check pattern:

  1 -> 2 -> 3               For cell X, check:
  |
  v                           [T]     T = Top neighbor
  4 -> 5 -> 6               [L][X]   L = Left neighbor
  |
  v                         Only 2 checks needed per cell!
  7 -> 8 -> 9
```

### Code

**Python Solution:**

```python
def solve_optimal(n, k):
    """
    Backtracking with constraint checking.

    Time: O(k^(n^2)) worst case, much better in practice
    Space: O(n^2) for grid + O(n^2) recursion stack
    """
    def is_safe(row, col, color):
        # Check left neighbor
        if col > 0 and grid[row][col - 1] == color:
            return False
        # Check top neighbor
        if row > 0 and grid[row - 1][col] == color:
            return False
        return True

    def solve(row, col):
        # Base case: filled entire grid
        if row == n:
            return True

        # Move to next row if current row complete
        next_row, next_col = (row, col + 1) if col + 1 < n else (row + 1, 0)

        # Try each color
        for color in range(1, k + 1):
            if is_safe(row, col, color):
                grid[row][col] = color
                if solve(next_row, next_col):
                    return True
                grid[row][col] = 0  # Backtrack

        return False

    # Special case: need at least 2 colors for n > 1
    if n > 1 and k < 2:
        return None

    grid = [[0] * n for _ in range(n)]
    return grid if solve(0, 0) else None


def main():
    n, k = map(int, input().split())
    result = solve_optimal(n, k)

    if result is None:
        print("NO")
    else:
        for row in result:
            print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
```

**C++ Solution:**

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, k;
vector<vector<int>> grid;

bool is_safe(int row, int col, int color) {
    // Check left neighbor
    if (col > 0 && grid[row][col - 1] == color) return false;
    // Check top neighbor
    if (row > 0 && grid[row - 1][col] == color) return false;
    return true;
}

bool solve(int row, int col) {
    // Base case: filled entire grid
    if (row == n) return true;

    // Calculate next position
    int next_row = (col + 1 < n) ? row : row + 1;
    int next_col = (col + 1 < n) ? col + 1 : 0;

    // Try each color
    for (int color = 1; color <= k; color++) {
        if (is_safe(row, col, color)) {
            grid[row][col] = color;
            if (solve(next_row, next_col)) return true;
            grid[row][col] = 0;  // Backtrack
        }
    }
    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k;

    // Special case: need at least 2 colors for n > 1
    if (n > 1 && k < 2) {
        cout << "NO\n";
        return 0;
    }

    grid.assign(n, vector<int>(n, 0));

    if (solve(0, 0)) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                cout << grid[i][j] << (j < n - 1 ? " " : "\n");
            }
        }
    } else {
        cout << "NO\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(k^(n^2)) | Worst case: all branches explored |
| Space | O(n^2) | Grid storage + recursion depth |

**In practice:** The algorithm runs much faster due to early pruning. For a 10x10 grid with 4 colors, solutions are found almost instantly because valid paths are abundant.

---

## Common Mistakes

### Mistake 1: Checking All Four Neighbors

```python
# WRONG - checking neighbors not yet colored
def is_safe(row, col, color):
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < n and 0 <= nc < n:
            if grid[nr][nc] == color:  # Bottom/right not yet filled!
                return False
```

**Problem:** In row-major order, right and bottom neighbors are not yet colored. Checking them is unnecessary and may cause bugs.

**Fix:** Only check top and left neighbors (already colored).

### Mistake 2: Not Handling k = 1 for n > 1

```python
# WRONG - will loop forever or return invalid result
def solve(n, k):
    grid = [[0] * n for _ in range(n)]
    # ... backtracking without special case check
```

**Problem:** With only 1 color and n > 1, adjacent cells must share colors, which is impossible.

**Fix:** Check `if n > 1 and k < 2: return None` at the start.

### Mistake 3: Forgetting to Backtrack

```python
# WRONG - grid state corrupted after failed branch
for color in range(1, k + 1):
    if is_safe(row, col, color):
        grid[row][col] = color
        if solve(next_row, next_col):
            return True
        # Missing: grid[row][col] = 0
```

**Problem:** Without resetting the cell, failed attempts leave stale values that corrupt future attempts.

**Fix:** Always reset `grid[row][col] = 0` after a failed recursive call.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single cell | n=1, k=1 | `1` | Any color works for 1x1 |
| Minimum colors | n=2, k=2 | Valid 2x2 grid | Checkerboard pattern |
| Impossible | n=2, k=1 | NO | Adjacent cells must differ |
| Maximum grid | n=10, k=4 | Valid 10x10 grid | Plenty of colors |
| k > 4 | n=3, k=4 | Valid grid | Extra colors, easier |

---

## When to Use This Pattern

### Use This Approach When:
- You need to find ANY valid assignment satisfying constraints
- The search space can be pruned by checking partial solutions
- Constraints are local (depend on neighboring elements)
- Problem size is small enough for exponential worst case

### Don't Use When:
- You need to count ALL solutions (use DP or math)
- The problem has optimal substructure (use DP instead)
- Constraints are global and cannot prune early
- Problem size is too large (n > 15 for exponential algorithms)

### Pattern Recognition Checklist:
- [ ] Assigning values to positions with constraints? -> **Backtracking**
- [ ] Can validate partial solutions? -> **Add pruning**
- [ ] Need any solution, not optimal? -> **Backtracking is ideal**
- [ ] Grid/board with local constraints? -> **Classic backtracking setup**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Chessboard and Queens](https://cses.fi/problemset/task/1624) | Similar backtracking on grid |
| [Creating Strings](https://cses.fi/problemset/task/1622) | Backtracking for permutations |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [N-Queens](https://leetcode.com/problems/n-queens/) | More complex constraints (diagonals) |
| [Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) | Multiple constraint types |
| [Word Search](https://leetcode.com/problems/word-search/) | Path finding with backtracking |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [N-Queens II](https://leetcode.com/problems/n-queens-ii/) | Counting all solutions |
| [Graph Coloring](https://cp-algorithms.com/graph/coloring.html) | Generalized to arbitrary graphs |
| [Hamiltonian Path](https://cses.fi/problemset/task/1690) | Backtracking with bitmask DP |

---

## Key Takeaways

1. **The Core Idea:** Fill cells one by one, checking constraints against already-filled neighbors, and backtrack on conflicts.
2. **Time Optimization:** Early pruning transforms exponential worst case into practical efficiency.
3. **Space Trade-off:** Only O(n^2) space needed; recursion stack bounded by grid size.
4. **Pattern:** Classic constraint satisfaction via backtracking with local validation.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why we only check top and left neighbors
- [ ] Identify when backtracking will be efficient vs. too slow
- [ ] Implement the solution in under 10 minutes

---

## Additional Resources

- [CP-Algorithms: Backtracking](https://cp-algorithms.com/combinatorics/generating_combinations.html)
- [CSES Problem Set - Introductory Problems](https://cses.fi/problemset/)
- [Graph Coloring - Wikipedia](https://en.wikipedia.org/wiki/Graph_coloring)
