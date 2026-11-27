---
layout: simple
title: "Knight's Tour"
difficulty: Hard
tags: [graph, backtracking, warnsdorff, heuristic]
cses_link: https://cses.fi/problemset/task/1689
---

# Knight's Tour

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find a path for a knight to visit all squares exactly once |
| Input | Starting square `x y` (column, then row; 1-indexed) |
| Output | 8x8 grid of move numbers 1..64 |
| Type | Hamiltonian Path on a graph |
| Core Technique | Backtracking with Warnsdorff's Heuristic |

## Learning Goals

After completing this problem, you will understand:
1. **Backtracking with heuristics** - How intelligent move ordering dramatically reduces search space
2. **Warnsdorff's rule** - A greedy heuristic that guides move selection
3. **Pruning strategies** - Early termination of unpromising branches

## Problem Statement

Given an 8x8 chessboard and a starting position, find a sequence of knight moves that visits every square exactly once. A knight moves in an "L" shape: two squares in one direction and one square perpendicular (or vice versa).

**Input**: One line with two integers `x y` (1 <= x, y <= 8): the starting **column** x and **row** y.
**Output**: An 8x8 grid: row y, column x holds 1, and each square holds the move number (1..64) on which the knight visits it. Any valid tour is accepted; a tour exists from every square.

```
Input:
2 1

Output:
4 1 6 19 30 27 16 41
7 20 3 26 17 40 31 28
2 5 18 39 58 29 42 15
21 8 25 56 43 54 59 32
24 45 22 63 38 57 14 53
9 48 37 44 55 62 33 60
46 23 50 11 64 35 52 13
49 10 47 36 51 12 61 34
```

Here `2 1` means column 2 of the top row, which is why 1 sits in the second cell of the first line. This is the grid the code below prints; the CSES sample shows a different, equally valid tour.

## The 8 Knight Moves

A knight at position (r, c) can move to exactly 8 possible squares:

```
    The 8 possible knight moves from position (r, c):

         (-2,-1)     (-2,+1)
              \       /
               +-----+
    (-1,-2) -- |  K  | -- (-1,+2)
               +-----+
    (+1,-2) -- |     | -- (+1,+2)
               +-----+
              /       \
         (+2,-1)     (+2,+1)

    Move offsets: (dr, dc)
    1. (-2, -1)    5. (+1, -2)
    2. (-2, +1)    6. (+1, +2)
    3. (-1, -2)    7. (+2, -1)
    4. (-1, +2)    8. (+2, +1)
```

## Approach 1: Brute Force Backtracking

### Algorithm

Try all 8 knight moves at each step. When stuck (no valid moves but board not complete), backtrack and try the next option.

```
Brute Force Backtracking:

Step 1: Start at given position, mark visited
Step 2: Try each of 8 moves in fixed order
Step 3: If move valid (on board, unvisited):
        - Mark new square visited
        - Recurse from new position
        - If recursion succeeds, done!
        - Otherwise, unmark and try next move
Step 4: If all moves fail, backtrack
```

### Why Brute Force is Too Slow

- At each of 64 squares, up to 8 choices
- Worst case: O(8^64) states to explore
- Even with pruning for invalid moves, exponential blowup
- An 8x8 board has 26,534,728,821,064 possible tours!

## Approach 2: Warnsdorff's Heuristic (Key Optimization)

### The Core Idea

**Warnsdorff's Rule**: Always move to the square with the FEWEST onward moves available.

### Why Warnsdorff Works

```
Without heuristic:            With Warnsdorff:

  +--+--+--+--+--+            +--+--+--+--+--+
  |  |  |  |  |  |            |  |  |  |  |  |
  +--+--+--+--+--+            +--+--+--+--+--+
  |  |  |XX|  |  |  Knight    |  |  |  |  |  |
  +--+--+--+--+--+  goes to   +--+--+--+--+--+
  |  |  |  |  |  |  center    |  |XX|  |  |  |  Knight goes
  +--+--+--+--+--+  first     +--+--+--+--+--+  to corner
  |  |  |  |  |  |  (more     |  |  |  |  |  |  first (fewer
  +--+--+--+--+--+  options)  +--+--+--+--+--+  options)

  Problem: Corners get        Benefit: Visit
  "painted into" -            constrained squares
  hard to reach later!        early, keep options open
```

**Intuition**: Squares with few exits (corners, edges) become impossible to reach if left for later. By visiting them early, we avoid "painting ourselves into a corner."

### Degree Calculation

For each candidate move, count how many unvisited squares it can reach:

```
Example: Knight at position K, considering moves A, B, C

  +--+--+--+--+--+--+--+--+
  |  |  | A|  |  |  |  |  |   A can reach: 2 squares (degree=2)
  +--+--+--+--+--+--+--+--+
  |  |  |  |  | B|  |  |  |   B can reach: 5 squares (degree=5)
  +--+--+--+--+--+--+--+--+
  |  |  |  | K|  |  |  |  |   C can reach: 4 squares (degree=4)
  +--+--+--+--+--+--+--+--+
  |  | C|  |  |  |  |  |  |
  +--+--+--+--+--+--+--+--+

  Warnsdorff chooses: A (lowest degree = 2)
```

## Implementation

### Python Solution

```python
def solve_knights_tour(start_row: int, start_col: int) -> list:
  """
  Find knight's tour on 8x8 board starting from (start_row, start_col).
  Uses Warnsdorff's heuristic for efficient solving.
  Returns the board: board[r][c] = move number (1..64), or None.
  """
  N = 8

  # The 8 possible knight moves
  MOVES = [
    (-2, -1), (-2, +1), (-1, -2), (-1, +2),
    (+1, -2), (+1, +2), (+2, -1), (+2, +1)
  ]

  board = [[-1] * N for _ in range(N)]

  def is_valid(r: int, c: int) -> bool:
    """Check if position is on board and unvisited."""
    return 0 <= r < N and 0 <= c < N and board[r][c] == -1

  def count_degree(r: int, c: int) -> int:
    """Count available moves from position (Warnsdorff's degree)."""
    count = 0
    for dr, dc in MOVES:
      if is_valid(r + dr, c + dc):
        count += 1
    return count

  def get_sorted_moves(r: int, c: int) -> list:
    """Get valid moves sorted by degree (Warnsdorff's heuristic)."""
    candidates = []
    for dr, dc in MOVES:
      nr, nc = r + dr, c + dc
      if is_valid(nr, nc):
        degree = count_degree(nr, nc)
        candidates.append((degree, nr, nc))
    # Sort by degree (fewest onward moves first)
    candidates.sort()
    return [(nr, nc) for _, nr, nc in candidates]

  def backtrack(r: int, c: int, move_num: int) -> bool:
    """Recursive backtracking with Warnsdorff ordering."""
    board[r][c] = move_num

    # Base case: all squares visited
    if move_num == N * N:
      return True

    # Try moves in Warnsdorff order (lowest degree first)
    for nr, nc in get_sorted_moves(r, c):
      if backtrack(nr, nc, move_num + 1):
        return True

    # Backtrack
    board[r][c] = -1
    return False

  return board if backtrack(start_row, start_col, 1) else None


if __name__ == "__main__":
  x, y = map(int, input().split())          # column first, then row
  board = solve_knights_tour(y - 1, x - 1)  # 0-indexed (row, col)
  for row in board:
    print(" ".join(map(str, row)))
```

### Complexity Analysis

| Approach | Time Complexity | Space Complexity | Practical Performance |
|----------|----------------|------------------|----------------------|
| Brute Force | O(8^64) worst | O(64) | Too slow |
| Warnsdorff | O(8^64) worst | O(64) | Nearly linear in practice |

**Key insight**: While worst-case is still exponential, Warnsdorff's heuristic is so effective that it typically finds a solution on the first try without any backtracking!

## Common Mistakes

1. **Not implementing the heuristic**
   - Pure backtracking without Warnsdorff is far too slow for 8x8
   - Will time out on judge

2. **Wrong move offsets**
   - Knight moves are (+/-1, +/-2) and (+/-2, +/-1)
   - Common error: using (+/-1, +/-1) or (+/-2, +/-2)

3. **Swapping x and y, or printing coordinates**
   - CSES gives `x y` = column, then row, so the start is `board[y-1][x-1]`
   - The answer is the 8x8 grid of move numbers, not a list of 64 squares

4. **Forgetting to backtrack**
   - Must reset board[r][c] = -1 when returning false
   - Otherwise the visited state corrupts future attempts

5. **Not sorting moves properly**
   - Must sort by degree of destination, not current position
   - Sorting should be ascending (lowest degree first)

## Why Warnsdorff Often Finds Solution Without Backtracking

For an 8x8 board, Warnsdorff's heuristic is remarkably effective:
- Empirically succeeds without backtracking ~76% of starting positions
- The remaining cases need minimal backtracking
- This is because the heuristic naturally avoids dead-ends

The intuition: By always visiting the most constrained squares first, we ensure that no square becomes unreachable. It is a greedy strategy that happens to work exceptionally well for this specific problem.

## Visual: Complete Example

```
Input "1 1": start in the top-left corner (row 1, column 1).

Move 1 -> 2: the two candidates (row 2, col 3) and (row 3, col 2) both have
             degree 5; the tie goes to the first in sorted order, (row 2, col 3).
Each later move again picks the unvisited neighbour with the fewest exits.

Final board printed by the code (move numbers):
 1 16 31 40  3 18 21 56
30 39  2 17 42 55  4 19
15 32 41 46 53 20 57 22
38 29 48 43 58 45 54  5
33 14 37 52 47 60 23 62
28 49 34 59 44 63  6  9
13 36 51 26 11  8 61 24
50 27 12 35 64 25 10  7
```

## Summary

| Concept | Key Point |
|---------|-----------|
| Problem Type | Hamiltonian path on implicit graph |
| Core Algorithm | Backtracking |
| Key Optimization | Warnsdorff's heuristic |
| Heuristic Rule | Move to square with fewest onward moves |
| Why It Works | Avoids stranding constrained squares |
| Practical Note | Often finds solution without backtracking |
