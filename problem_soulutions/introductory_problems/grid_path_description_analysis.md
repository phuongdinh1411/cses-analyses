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

### Pruning Rules

| Rule | Check | Why it is safe |
|------|-------|----------------|
| **Early arrival** | Standing on the lower-left corner before step 48 → return 0 | The path must end there, so it can never leave again |
| **Split** | Blocked ahead *and* behind, but both sides free (or the rotated case) → return 0 | The unvisited cells are now cut into two parts; a single path can only finish one of them |

"Blocked" means a wall or an already visited cell. Padding the 7x7 board with a border of permanently visited cells turns walls into ordinary visited cells, so one check covers both cases and no bounds tests are needed.

### Algorithm

1. Start at the top-left corner, marked visited.
2. On entering a cell: apply the early-arrival check, then the split check.
3. Try the forced move if `path[step]` is a letter, otherwise all four; recurse into unvisited cells and unmark on return.
4. Count 1 when the corner is reached at exactly step 48.

### Visual Diagram: The Split Check

```
  # = visited or wall     . = unvisited     X = current cell

  . . . # . . .
  . . . X . . .      Up and down are blocked, left and right are free.
  . . . # . . .      The visited path plus the walls form a barrier through
                     X's column, so the free cells on the left and on the
                     right are now separate parts. X can finish one of them
                     but never come back for the other -> return 0
```

The most common trigger is running into the board edge: the path walks along row 2 straight into the right wall, cells above and below are still unvisited, and the wall blocks "ahead".

### Code

```python
import sys


def count_paths(path: str) -> int:
  # 9x9 grid: the 7x7 board plus a border of permanently visited cells,
  # so neighbor checks never need bounds tests.
  vis = [[r in (0, 8) or c in (0, 8) for c in range(9)] for r in range(9)]
  moves = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
  all_moves = list(moves.values())

  def dfs(r: int, c: int, step: int) -> int:
    if r == 7 and c == 1:              # lower-left corner
      return 1 if step == 48 else 0    # arriving early wastes the path
    # Split check: blocked ahead and behind but free on both sides (or the
    # mirror case) cuts the unvisited cells into two parts -> dead end.
    if vis[r - 1][c] and vis[r + 1][c] and not vis[r][c - 1] and not vis[r][c + 1]:
      return 0
    if vis[r][c - 1] and vis[r][c + 1] and not vis[r - 1][c] and not vis[r + 1][c]:
      return 0
    total = 0
    for dr, dc in ([moves[path[step]]] if path[step] != '?' else all_moves):
      nr, nc = r + dr, c + dc
      if not vis[nr][nc]:
        vis[nr][nc] = True
        total += dfs(nr, nc, step + 1)
        vis[nr][nc] = False
    return total

  vis[1][1] = True
  return dfs(1, 1, 0)


def main():
  print(count_paths(sys.stdin.readline().strip()))


if __name__ == "__main__":
  main()
```

#### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | Exponential, heavily pruned | Measured in CPython: about 0.7 s for the sample, about 10 s for 48 `?` (88418 paths). The naive version is many orders of magnitude slower |
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
**Fix:** Add the split check and the early-arrival check from the optimal solution.

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
| Forced first move | `D` + 47 `?` | 45647 | Paths starting down (starting right gives 42771; together 88418) |
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
