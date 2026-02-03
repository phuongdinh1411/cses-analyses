---
layout: simple
title: "Grid Completion - Combinatorics Problem"
permalink: /problem_soulutions/counting_problems/grid_completion_analysis
difficulty: Medium
tags: [combinatorics, backtracking, grid, counting]
---

# Grid Completion

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Combinatorics / Backtracking |
| **Time Limit** | 1 second |
| **Key Technique** | Constraint Satisfaction, Latin Square Counting |
| **CSES Link** | [Grid Paths](https://cses.fi/problemset/task/1078) (related) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply backtracking to count valid grid configurations
- [ ] Understand Latin square constraints (unique values per row/column)
- [ ] Use bitmasks to track available values efficiently
- [ ] Recognize when mathematical formulas can replace enumeration

---

## Problem Statement

**Problem:** Given a partially filled n x n grid, count the number of ways to complete it such that each row and column contains each value from 1 to n exactly once.

**Input:**
- Line 1: Integer n (grid dimension)
- Next n lines: Grid values (0 = empty cell)

**Output:**
- Number of valid completions modulo 10^9 + 7

**Constraints:**
- 1 <= n <= 10
- Grid values are in range [0, n] where 0 means empty
- Answer modulo 10^9 + 7

### Example

```
Input:
2
1 0
0 1

Output:
1
```

**Explanation:** The only valid completion is:
```
1 2
2 1
```
Row 1: contains 1, 2. Row 2: contains 2, 1.
Col 1: contains 1, 2. Col 2: contains 2, 1.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** This is a Latin square completion problem. Each row and column must be a permutation of 1 to n.

The problem combines two concepts:
1. **Constraint satisfaction** - each placement must respect row/column uniqueness
2. **Counting** - we need to count ALL valid completions, not just find one

### Breaking Down the Problem

1. **What are we looking for?** Total count of valid grid completions
2. **What information do we have?** Pre-filled cells that constrain valid values
3. **What's the relationship?** Each empty cell has limited valid choices based on its row/column

### Analogies

Think of this like solving multiple Sudoku puzzles simultaneously and counting how many solutions exist. Each empty cell can only use values not already in its row or column.

---

## Solution 1: Brute Force Backtracking

### Idea

Try every possible value (1 to n) for each empty cell. After filling all cells, verify the grid satisfies Latin square constraints.

### Algorithm

1. Find all empty cells in the grid
2. For each empty cell, try values 1 to n
3. After filling all cells, check if grid is valid
4. Count valid completions

### Code

```python
def solve_brute_force(n, grid):
    """
    Brute force: try all values, validate at the end.

    Time: O(n^k * n^2) where k = empty cells
    Space: O(k) for recursion
    """
    MOD = 10**9 + 7
    empty = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == 0]

    def is_valid():
        for i in range(n):
            if len(set(grid[i])) != n:
                return False
            if len(set(grid[j][i] for j in range(n))) != n:
                return False
        return True

    def backtrack(idx):
        if idx == len(empty):
            return 1 if is_valid() else 0

        r, c = empty[idx]
        count = 0
        for val in range(1, n + 1):
            grid[r][c] = val
            count = (count + backtrack(idx + 1)) % MOD
        grid[r][c] = 0
        return count

    return backtrack(0)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^k * n^2) | n choices for k cells, O(n^2) validation |
| Space | O(k) | Recursion depth = number of empty cells |

### Why This Is Slow

We try invalid combinations and only discover them at the end. Most branches are wasted effort.

---

## Solution 2: Optimized Backtracking with Pruning

### Key Insight

> **The Trick:** Validate constraints incrementally. Reject invalid placements immediately instead of at the end.

### Algorithm

1. Track used values for each row and column
2. Before placing a value, check if it's available in both row AND column
3. Only recurse on valid placements

### Dry Run Example

Let's trace through with n = 2, grid = [[1, 0], [0, 1]]:

```
Initial state:
  grid = [[1, 0], [0, 1]]
  empty cells: [(0,1), (1,0)]
  row_used[0] = {1}, row_used[1] = {1}
  col_used[0] = {1}, col_used[1] = {1}

Step 1: Fill cell (0,1)
  Need value not in row_used[0]={1} AND not in col_used[1]={1}
  Available: {2}
  Try val=2: Valid! Place it.
  grid = [[1, 2], [0, 1]]

Step 2: Fill cell (1,0)
  Need value not in row_used[1]={1} AND not in col_used[0]={1}
  Available: {2}
  Try val=2: Valid! Place it.
  grid = [[1, 2], [2, 1]]

All cells filled -> count = 1
```

### Visual Diagram

```
Initial Grid:        After filling:
+---+---+            +---+---+
| 1 | ? |            | 1 | 2 |
+---+---+            +---+---+
| ? | 1 |            | 2 | 1 |
+---+---+            +---+---+

Row constraints:     Column constraints:
Row 0: has {1}       Col 0: has {1}
  -> needs {2}         -> needs {2}
Row 1: has {1}       Col 1: has {1}
  -> needs {2}         -> needs {2}
```

### Code

```python
def solve_optimized(n, grid):
    """
    Backtracking with early pruning.

    Time: O(n! in worst case, much better with constraints)
    Space: O(n) for tracking sets
    """
    MOD = 10**9 + 7

    # Track used values per row and column
    row_used = [set() for _ in range(n)]
    col_used = [set() for _ in range(n)]

    # Initialize with pre-filled values
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0:
                row_used[i].add(grid[i][j])
                col_used[j].add(grid[i][j])

    # Find empty cells
    empty = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == 0]

    def backtrack(idx):
        if idx == len(empty):
            return 1

        r, c = empty[idx]
        count = 0

        for val in range(1, n + 1):
            # Prune: check constraints before recursing
            if val not in row_used[r] and val not in col_used[c]:
                # Place value
                row_used[r].add(val)
                col_used[c].add(val)
                grid[r][c] = val

                count = (count + backtrack(idx + 1)) % MOD

                # Backtrack
                row_used[r].remove(val)
                col_used[c].remove(val)
                grid[r][c] = 0

        return count

    return backtrack(0)
```

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

class GridCompletion {
    int n;
    vector<vector<int>> grid;
    vector<int> row_mask, col_mask;  // Bitmasks for used values
    vector<pair<int,int>> empty_cells;

public:
    int solve(int n_, vector<vector<int>>& g) {
        n = n_;
        grid = g;
        row_mask.assign(n, 0);
        col_mask.assign(n, 0);

        // Initialize masks and find empty cells
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 0) {
                    empty_cells.push_back({i, j});
                } else {
                    row_mask[i] |= (1 << grid[i][j]);
                    col_mask[j] |= (1 << grid[i][j]);
                }
            }
        }

        return backtrack(0);
    }

private:
    int backtrack(int idx) {
        if (idx == (int)empty_cells.size()) {
            return 1;
        }

        int r = empty_cells[idx].first;
        int c = empty_cells[idx].second;
        int used = row_mask[r] | col_mask[c];
        long long count = 0;

        for (int val = 1; val <= n; val++) {
            if (!(used & (1 << val))) {  // Value not used
                row_mask[r] |= (1 << val);
                col_mask[c] |= (1 << val);

                count = (count + backtrack(idx + 1)) % MOD;

                row_mask[r] ^= (1 << val);
                col_mask[c] ^= (1 << val);
            }
        }

        return count;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<int>> grid(n, vector<int>(n));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> grid[i][j];
        }
    }

    GridCompletion solver;
    cout << solver.solve(n, grid) << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n^k) worst case | But heavily pruned in practice |
| Space | O(n + k) | Row/col tracking + recursion depth |

---

## Common Mistakes

### Mistake 1: Forgetting to Backtrack

```python
# WRONG
row_used[r].add(val)
count = (count + backtrack(idx + 1)) % MOD
# Missing: row_used[r].remove(val)
```

**Problem:** State persists across branches, corrupting the search.
**Fix:** Always undo changes after recursive call returns.

### Mistake 2: Checking Constraints After Placement

```python
# WRONG - inefficient
grid[r][c] = val
if is_valid_so_far():  # Check AFTER placing
    count += backtrack(idx + 1)
grid[r][c] = 0
```

**Problem:** We place invalid values and then check. Wastes time.
**Fix:** Check BEFORE placing (early pruning).

### Mistake 3: Wrong Modulo Application

```python
# WRONG
return count % MOD  # Only at the end

# CORRECT
count = (count + backtrack(idx + 1)) % MOD  # At each addition
```

**Problem:** Integer overflow before final modulo (especially in C++).
**Fix:** Apply modulo at each addition step.

### Mistake 4: Not Handling Pre-filled Conflicts

```python
# WRONG - doesn't check if initial grid is valid
def solve(n, grid):
    # Start backtracking immediately...
```

**Problem:** If pre-filled values already violate constraints, answer should be 0.
**Fix:** Validate initial grid before counting.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| Empty grid n=1 | `[[0]]` | 1 | Only fill: [[1]] |
| Already complete | `[[1,2],[2,1]]` | 1 | No empty cells, valid |
| Invalid pre-fill | `[[1,1],[0,0]]` | 0 | Row 0 has duplicate 1 |
| Single empty | `[[1,0],[2,0]]` n=2 | 1 | Forced: [[1,2],[2,1]] |
| All empty n=2 | `[[0,0],[0,0]]` | 2 | Two Latin squares of order 2 |
| Large empty n=4 | All zeros | 576 | 4! * 4! / corrections |

---

## When to Use This Pattern

### Use Backtracking When:
- Grid size is small (n <= 10)
- Constraints allow significant pruning
- You need to count ALL solutions, not just one
- No closed-form mathematical formula exists

### Use Bitmasks When:
- n is small enough (n <= 20 for single int, n <= 64 for long long)
- Need fast membership testing
- Constraint checking is the bottleneck

### Consider Mathematical Formulas When:
- Grid is completely empty (counting Latin squares)
- Problem has known combinatorial structure
- n is too large for enumeration

### Pattern Recognition Checklist:
- [ ] Unique values per row? -> Latin square constraints
- [ ] Need all solutions? -> Backtracking with counting
- [ ] Small n with complex constraints? -> Bitmask DP
- [ ] Large n, simple structure? -> Mathematical formula

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Creating Strings](https://cses.fi/problemset/task/1622) | Basic backtracking and permutations |
| [Chessboard and Queens](https://cses.fi/problemset/task/1624) | Grid + backtracking + constraint checking |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Grid Paths](https://cses.fi/problemset/task/1078) | Fixed start/end, path counting |
| [Apple Division](https://cses.fi/problemset/task/1623) | Subset enumeration with backtracking |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Counting Tilings](https://cses.fi/problemset/task/2181) | Bitmask DP on grid |
| [Hamiltonian Flights](https://cses.fi/problemset/task/1690) | Bitmask DP with constraints |

---

## Key Takeaways

1. **The Core Idea:** Track used values per row/column to prune invalid branches early
2. **Time Optimization:** Validate constraints before recursing, not after
3. **Space Trade-off:** O(n) tracking sets enable O(1) constraint checking
4. **Pattern:** Constraint satisfaction + counting = backtracking with pruning

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement backtracking with proper state management (add/remove)
- [ ] Use bitmasks for efficient constraint tracking
- [ ] Identify Latin square problems by their row/column uniqueness property
- [ ] Calculate complexity based on branching factor and pruning
- [ ] Handle edge cases (invalid input, already complete, single solution)

---

## Additional Resources

- [CP-Algorithms: Generating Permutations](https://cp-algorithms.com/combinatorics/generating_permutations.html)
- [Wikipedia: Latin Square](https://en.wikipedia.org/wiki/Latin_square)
- [CSES Grid Paths](https://cses.fi/problemset/task/1638) - Grid-based counting
