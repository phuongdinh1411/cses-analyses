---
layout: problem-analysis
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
| Input | 8x8 chessboard, starting position (row, column) |
| Output | Sequence of 64 positions covering the entire board |
| Type | Hamiltonian Path on a graph |
| Core Technique | Backtracking with Warnsdorff's Heuristic |

## Learning Goals

After completing this problem, you will understand:
1. **Backtracking with heuristics** - How intelligent move ordering dramatically reduces search space
2. **Warnsdorff's rule** - A greedy heuristic that guides move selection
3. **Pruning strategies** - Early termination of unpromising branches

## Problem Statement

Given an 8x8 chessboard and a starting position, find a sequence of knight moves that visits every square exactly once. A knight moves in an "L" shape: two squares in one direction and one square perpendicular (or vice versa).

**Input**: Starting row `y` and column `x` (1-indexed)
**Output**: 64 positions representing a complete tour, or indicate impossibility

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
    Returns list of (row, col) tuples representing the tour.
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
        if move_num == N * N - 1:
            return True

        # Try moves in Warnsdorff order (lowest degree first)
        for nr, nc in get_sorted_moves(r, c):
            if backtrack(nr, nc, move_num + 1):
                return True

        # Backtrack
        board[r][c] = -1
        return False

    # Solve and extract path
    if backtrack(start_row, start_col, 0):
        path = [None] * (N * N)
        for r in range(N):
            for c in range(N):
                path[board[r][c]] = (r, c)
        return path
    return None


def print_tour(path: list) -> None:
    """Print the tour as required by CSES."""
    if path is None:
        print("NO SOLUTION")
        return
    for r, c in path:
        print(r + 1, c + 1)  # Convert to 1-indexed


# Example usage
if __name__ == "__main__":
    y, x = map(int, input().split())
    tour = solve_knights_tour(y - 1, x - 1)  # Convert to 0-indexed
    print_tour(tour)
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

3. **Off-by-one in indexing**
   - CSES uses 1-indexed input/output
   - Remember to convert when using 0-indexed arrays

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
Starting at (1,1) - top-left corner:

Move 1: (1,1)     Degree of candidates: (2,3)=4, (3,2)=4
                  Both equal, pick first

Move 2: (2,3)     Degree of candidates: (1,1)=visited, (3,1)=3, (4,2)=4...
                  Pick (3,1) with degree 3

Move 3: (3,1)     Continue applying Warnsdorff...

Final board (move numbers):
+----+----+----+----+----+----+----+----+

|  1 | 38 | 55 | 34 |  3 | 36 | 19 | 22 |
+----+----+----+----+----+----+----+----+

| 54 | 47 |  2 | 37 | 20 | 23 |  4 | 17 |
+----+----+----+----+----+----+----+----+

| 39 | 56 | 33 | 46 | 35 | 18 | 21 |  8 |
+----+----+----+----+----+----+----+----+

| 48 | 53 | 40 | 57 | 24 |  7 | 16 |  5 |
+----+----+----+----+----+----+----+----+

| 59 | 32 | 45 | 52 | 41 | 26 |  9 | 14 |
+----+----+----+----+----+----+----+----+

| 44 | 49 | 58 | 25 | 62 | 15 |  6 | 27 |
+----+----+----+----+----+----+----+----+

| 31 | 60 | 51 | 42 | 29 | 10 | 63 | 12 |
+----+----+----+----+----+----+----+----+

| 50 | 43 | 30 | 61 | 64 | 13 | 28 | 11 |
+----+----+----+----+----+----+----+----+
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
