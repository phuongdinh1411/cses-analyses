---
layout: simple
title: "Grid Paths - Backtracking with Pruning"
permalink: /problem_soulutions/introductory_problems/grid_path_description_analysis
difficulty: Hard
tags: [backtracking, pruning, grid, dfs, hamiltonian-path]
prerequisites: []
---

# Grid Paths

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Problem Link** | [CSES 1625 - Grid Paths](https://cses.fi/problemset/task/1625) |
| **Difficulty** | Hard |
| **Category** | Backtracking / Pruning |
| **Time Limit** | 1 second |
| **Key Technique** | Backtracking with Aggressive Pruning |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Implement backtracking to enumerate paths in a grid
- [ ] Apply pruning techniques to dramatically reduce search space
- [ ] Recognize when a partial solution cannot lead to a valid complete solution
- [ ] Understand the importance of early termination in exponential search spaces

---

## Problem Statement

**Problem:** Count the number of paths in a 7x7 grid that:
1. Start from the top-left corner (0, 0)
2. End at the bottom-left corner (6, 0)
3. Visit every square exactly once (48 moves total)
4. Follow a given 48-character path description

The path description uses:
- `D` = move down
- `U` = move up
- `L` = move left
- `R` = move right
- `?` = can move in any direction

**Input:**
- A single line containing a 48-character string

**Output:**
- The number of valid paths matching the description

**Constraints:**
- Grid size is fixed at 7x7 (49 cells)
- Path length is exactly 48 moves
- Each cell must be visited exactly once

### Example

```
Input:
??????R??????U??????????????????????????LD????D?

Output:
201
```

**Explanation:** There are 201 different ways to traverse the 7x7 grid visiting all cells exactly once, where the path follows the given constraints (R at position 7, U at position 14, etc.).

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we efficiently count Hamiltonian paths with constraints?

This is a classic backtracking problem where we explore all possible paths, but the key insight is that **naive backtracking is too slow**. A 7x7 grid with 48 moves and 4 choices per move could theoretically explore 4^48 states - far too many. The solution requires aggressive pruning to cut off dead-end paths early.

### Breaking Down the Problem

1. **What are we looking for?** Count of valid Hamiltonian paths from (0,0) to (6,0)
2. **What information do we have?** A 48-character string constraining some moves
3. **What's the relationship?** Each `?` allows any direction; fixed characters must be followed exactly

### Analogies

Think of this like navigating a maze where you must step on every tile exactly once. If you ever box yourself into a corner before visiting all tiles, that path is invalid. The pruning techniques are like having a sixth sense that tells you "this path is doomed" before you waste time exploring it.

---

## Solution 1: Naive Backtracking (TLE)

### Idea

Try all possible paths recursively, only counting those that visit all 49 cells and end at (6, 0).

### Algorithm

1. Start at (0, 0), mark as visited
2. For each move in the path string:
   - If it's a specific direction, try only that direction
   - If it's `?`, try all 4 directions
3. Skip invalid moves (out of bounds or already visited)
4. If we've made 48 moves and are at (6, 0), increment count

### Code

```python
def solve_naive(path: str) -> int:
    """
    Naive backtracking without pruning.

    Time: O(4^48) worst case - TOO SLOW
    Space: O(49) for visited array and recursion stack
    """
    n = 7
    visited = [[False] * n for _ in range(n)]
    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def dfs(row: int, col: int, step: int) -> int:
        # Base case: completed all 48 moves
        if step == 48:
            return 1 if row == 6 and col == 0 else 0

        count = 0
        moves = directions.keys() if path[step] == '?' else [path[step]]

        for move in moves:
            dr, dc = directions[move]
            nr, nc = row + dr, col + dc

            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                visited[nr][nc] = True
                count += dfs(nr, nc, step + 1)
                visited[nr][nc] = False

        return count

    visited[0][0] = True
    return dfs(0, 0, 0)
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(4^48) | Exponential - explores too many paths |
| Space | O(n^2) | Grid visited array + recursion depth |

### Why This Works (But Is Too Slow)

This solution is correct but will time out. Without pruning, it explores many paths that are doomed to fail - paths that box themselves into corners or split the unvisited region into disconnected parts.

---

## Solution 2: Backtracking with Pruning (Optimal)

### Key Insight

> **The Trick:** Prune paths that cannot possibly visit all remaining cells. If we detect a dead end early, we can skip millions of useless recursive calls.

### Pruning Strategies

| Pruning Rule | Description |
|--------------|-------------|
| **Connectivity** | If moving would split unvisited cells into disconnected regions, prune |
| **Dead End** | If next cell has only one unvisited neighbor (and isn't the end), we must go there |
| **Wall Hug** | If we hit a wall and both parallel cells are unvisited, we've split the region |

### Algorithm

1. Start at (0, 0), mark as visited
2. For each step, apply pruning rules before recursing:
   - **Pruning 1:** If we can go straight but would create a split, prune
   - **Pruning 2:** If the current move is forced (dead-end neighbor), take it
3. Recurse on valid moves, backtrack after

### Dry Run Example

Let's trace through a small portion with input `???????...`:

```
Initial state:
  Grid 7x7, start at (0,0), step=0
  visited[0][0] = True

Step 0: path[0] = '?', can move D or R (U and L are out of bounds)

  Try R: Move to (0,1)
    Check pruning: Does this split the grid? No.
    visited[0][1] = True
    Continue to step 1...

  Try D: Move to (1,0)
    Check pruning: Does this split the grid? No.
    visited[1][0] = True
    Continue to step 1...

Step 1: At (0,1), path[1] = '?', can move D, L, R

  Try L: Would go back to (0,0) - already visited, skip
  Try R: Move to (0,2)
    PRUNING CHECK:
    - Cell above (0,2) is wall
    - Cell (1,1) and (1,2) are both unvisited
    - If we go right along the wall, we might split the grid
    Continue checking...

  [Process continues with pruning eliminating bad paths early]

...

Final step (step 47):
  Must be at (6,0) to count as valid path
  If yes: return 1
  If no: return 0
```

### Visual Diagram: Pruning in Action

```
Pruning Scenario - Hitting a wall:

Current position: X
Unvisited cells:  .
Visited cells:    #
Wall:             |

  | . . . . . . |     If X moves RIGHT along the top wall:
  | # X . . . . |
  | # . . . . . |     Cells below (marked *) become disconnected
  | # * . . . . |     from cells to the right!
  | # * . . . . |
  | # * . . . . |     PRUNE THIS PATH - it cannot succeed
  | # * . . . . |
```

### Code

```python
def solve_optimal(path: str) -> int:
    """
    Backtracking with pruning optimizations.

    Time: O(~exponential but heavily pruned) - passes within time limit
    Space: O(n^2) for visited array
    """
    n = 7
    visited = [[False] * n for _ in range(n)]

    # Direction mappings
    dir_map = {'U': 0, 'D': 1, 'L': 2, 'R': 3}
    dr = [-1, 1, 0, 0]  # U, D, L, R
    dc = [0, 0, -1, 1]
    opposite = [1, 0, 3, 2]  # opposite directions

    def is_valid(r: int, c: int) -> bool:
        return 0 <= r < n and 0 <= c < n and not visited[r][c]

    def dfs(row: int, col: int, step: int) -> int:
        # Base case: completed path
        if step == 48:
            return 1 if row == 6 and col == 0 else 0

        # Reached destination too early
        if row == 6 and col == 0:
            return 0

        count = 0

        # Determine which directions to try
        if path[step] != '?':
            directions = [dir_map[path[step]]]
        else:
            directions = range(4)

        for d in directions:
            nr, nc = row + dr[d], col + dc[d]

            if not is_valid(nr, nc):
                continue

            # PRUNING 1: Check if we hit a wall and would split the grid
            # If moving parallel to a wall and both perpendicular cells are unvisited,
            # we're creating a dead end

            # Check perpendicular directions
            perp1 = (d + 2) % 4 if d < 2 else (d + 2) % 4
            perp2 = (d + 3) % 4 if d < 2 else (d + 1) % 4

            # Simplified connectivity pruning:
            # If the cell ahead in current direction is blocked/visited,
            # but cells on both sides of current position are unvisited,
            # we're splitting the grid

            # Left-right or up-down checks
            if d < 2:  # Moving U or D (vertical)
                left_valid = is_valid(row, col - 1)
                right_valid = is_valid(row, col + 1)
                ahead_blocked = not is_valid(row + 2*dr[d], col)

                if left_valid and right_valid and ahead_blocked:
                    continue
            else:  # Moving L or R (horizontal)
                up_valid = is_valid(row - 1, col)
                down_valid = is_valid(row + 1, col)
                ahead_blocked = not is_valid(row, col + 2*dc[d])

                if up_valid and down_valid and ahead_blocked:
                    continue

            # PRUNING 2: Can't go through and neighbor cells form dead end
            # Count unvisited neighbors of (nr, nc)
            unvisited_neighbors = 0
            for d2 in range(4):
                nnr, nnc = nr + dr[d2], nc + dc[d2]
                if is_valid(nnr, nnc):
                    unvisited_neighbors += 1

            # If moving to a cell that would have 0 unvisited neighbors
            # and it's not the final destination
            if unvisited_neighbors == 0 and not (nr == 6 and nc == 0 and step == 47):
                continue

            visited[nr][nc] = True
            count += dfs(nr, nc, step + 1)
            visited[nr][nc] = False

        return count

    visited[0][0] = True
    return dfs(0, 0, 0)


# Main function for CSES submission
def main():
    path = input().strip()
    print(solve_optimal(path))

if __name__ == "__main__":
    main()
```

### C++ Solution

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 7;
bool visited[N][N];
string path;
int dr[] = {-1, 1, 0, 0};  // U, D, L, R
int dc[] = {0, 0, -1, 1};

bool isValid(int r, int c) {
    return r >= 0 && r < N && c >= 0 && c < N && !visited[r][c];
}

int charToDir(char c) {
    if (c == 'U') return 0;
    if (c == 'D') return 1;
    if (c == 'L') return 2;
    return 3;  // R
}

int dfs(int row, int col, int step) {
    // Base case: completed all moves
    if (step == 48) {
        return (row == 6 && col == 0) ? 1 : 0;
    }

    // Reached end too early
    if (row == 6 && col == 0) {
        return 0;
    }

    int count = 0;

    for (int d = 0; d < 4; d++) {
        // Skip if path specifies a different direction
        if (path[step] != '?' && d != charToDir(path[step])) {
            continue;
        }

        int nr = row + dr[d];
        int nc = col + dc[d];

        if (!isValid(nr, nc)) continue;

        // PRUNING 1: Wall-split detection
        if (d < 2) {  // Vertical move (U or D)
            bool leftValid = isValid(row, col - 1);
            bool rightValid = isValid(row, col + 1);
            bool aheadBlocked = !isValid(row + 2*dr[d], col);
            if (leftValid && rightValid && aheadBlocked) continue;
        } else {  // Horizontal move (L or R)
            bool upValid = isValid(row - 1, col);
            bool downValid = isValid(row + 1, col);
            bool aheadBlocked = !isValid(row, col + 2*dc[d]);
            if (upValid && downValid && aheadBlocked) continue;
        }

        // PRUNING 2: Dead-end detection
        int neighbors = 0;
        for (int d2 = 0; d2 < 4; d2++) {
            if (isValid(nr + dr[d2], nc + dc[d2])) {
                neighbors++;
            }
        }
        if (neighbors == 0 && !(nr == 6 && nc == 0 && step == 47)) {
            continue;
        }

        visited[nr][nc] = true;
        count += dfs(nr, nc, step + 1);
        visited[nr][nc] = false;
    }

    return count;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> path;

    memset(visited, false, sizeof(visited));
    visited[0][0] = true;

    cout << dfs(0, 0, 0) << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | ~O(exponential, heavily pruned) | Pruning reduces from 4^48 to manageable |
| Space | O(n^2) | 7x7 visited array + O(48) recursion stack |

---

## Common Mistakes

### Mistake 1: Missing Pruning Conditions

```python
# WRONG - No pruning, will TLE
def dfs(row, col, step):
    if step == 48:
        return 1 if (row, col) == (6, 0) else 0

    count = 0
    for d in range(4):
        nr, nc = row + dr[d], col + dc[d]
        if is_valid(nr, nc):
            visited[nr][nc] = True
            count += dfs(nr, nc, step + 1)  # Explores too many dead ends
            visited[nr][nc] = False
    return count
```

**Problem:** Without pruning, the algorithm explores paths that are guaranteed to fail.
**Fix:** Add wall-split and dead-end pruning as shown in the optimal solution.

### Mistake 2: Forgetting to Check Early Termination

```python
# WRONG - Doesn't check if we reach (6,0) too early
def dfs(row, col, step):
    if step == 48:
        return 1 if (row, col) == (6, 0) else 0
    # Missing: if (row, col) == (6, 0): return 0
```

**Problem:** If we reach the end cell before step 48, we haven't visited all cells.
**Fix:** Add early termination check: `if row == 6 and col == 0: return 0`

### Mistake 3: Incorrect Direction Mapping

```python
# WRONG - Swapped directions
dr = [1, -1, 0, 0]   # Wrong: D and U swapped
dc = [0, 0, 1, -1]   # Wrong: R and L swapped
```

**Problem:** Grid coordinates have row 0 at top, so U should decrease row.
**Fix:** Verify: U=(-1,0), D=(1,0), L=(0,-1), R=(0,1)

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| All wildcards | `????????????????...` (48 ?'s) | 88418 | Total Hamiltonian paths from (0,0) to (6,0) |
| Forced first move | `D???????????????...` | ~half of total | Restricts to paths starting down |
| Impossible path | `UUUUUUUUUUUUUUUUUUUU...` | 0 | Can't go up from row 0 |
| Single valid path | Fully specified valid path | 1 | Only one path matches |

---

## When to Use This Pattern

### Use Backtracking with Pruning When:
- Exhaustive search is required but naive approach is too slow
- Partial solutions can be validated/invalidated efficiently
- Problem has a tree-like solution space with dead ends
- Constraints are tight (like visiting all cells exactly once)

### Don't Use When:
- Problem has polynomial-time DP solution
- Greedy approach works
- The search space cannot be meaningfully pruned

### Pattern Recognition Checklist:
- [ ] Need to count/enumerate all valid configurations? -> **Consider backtracking**
- [ ] Many partial solutions lead to dead ends? -> **Add pruning**
- [ ] Grid with "visit all cells" constraint? -> **Check connectivity pruning**
- [ ] Path description with wildcards? -> **Branch on wildcards, follow fixed moves**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Chessboard and Queens (CSES 1624)](https://cses.fi/problemset/task/1624) | Basic backtracking on grid |
| [N-Queens (LeetCode 51)](https://leetcode.com/problems/n-queens/) | Classic backtracking |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Unique Paths III (LeetCode 980)](https://leetcode.com/problems/unique-paths-iii/) | Visit all cells, obstacles present |
| [Word Search II (LeetCode 212)](https://leetcode.com/problems/word-search-ii/) | Backtracking with trie pruning |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Sudoku Solver (LeetCode 37)](https://leetcode.com/problems/sudoku-solver/) | Constraint propagation |
| [Knight's Tour](https://en.wikipedia.org/wiki/Knight%27s_tour) | Warnsdorff's heuristic |

---

## Key Takeaways

1. **The Core Idea:** Backtracking explores all possibilities, but pruning eliminates dead ends early
2. **Time Optimization:** From 4^48 to ~millions of states through connectivity and dead-end pruning
3. **Space Trade-off:** O(n^2) space for visited array enables O(1) cell lookup
4. **Pattern:** Hamiltonian path enumeration with constraint satisfaction

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why naive backtracking times out on this problem
- [ ] Describe the wall-split pruning condition
- [ ] Implement the solution without looking at the code
- [ ] Trace through a small example showing pruning in action
- [ ] Identify similar problems that benefit from backtracking with pruning

---

## Additional Resources

- [CSES Grid Paths](https://cses.fi/problemset/task/1625) - Backtracking on grid
- [CP-Algorithms: Backtracking](https://cp-algorithms.com/others/backtracking.html)
- [Hamiltonian Path - Wikipedia](https://en.wikipedia.org/wiki/Hamiltonian_path)
