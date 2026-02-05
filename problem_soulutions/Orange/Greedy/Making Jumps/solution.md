# Making Jumps

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

A knight is a piece used in the game of chess. The chessboard itself is a square array of cells. Each time a knight moves, its resulting position is two rows and one column, or two columns and one row away from its starting position. Thus a knight starting on row r, column c - which we'll denote as (r, c) - can move to any of the squares (r-2, c-1), (r-2, c+1), (r-1, c-2), (r-1, c+2), (r+1, c-2), (r+1, c+2), (r+2, c-1), or (r+2, c+1). Of course, the knight may not move to any square that is not on the board.

Suppose the chessboard is not square, but instead has rows with variable numbers of columns, and with each row offset zero or more columns to the right of the row above it. How many of the squares in such a modified chessboard can a knight, starting in the upper left square (marked with an asterisk), not reach in any number of moves without resting in any square more than once?

If necessary, the knight is permitted to pass over regions that are outside the borders of the modified chessboard, but as usual, it can only move to squares that are within the borders of the board.

## Input Format
- Each test case starts with the number of rows n (1 ≤ n ≤ 10).
- For each row, there are two integers: the offset (number of cells to skip) and the number of cells in that row.
- Input is terminated when n = 0.

## Output Format
For each test case, print "Case X, Y squares can not be reached." where X is the case number and Y is the number of unreachable squares.

## Solution

### Approach
This is a backtracking/DFS problem. We need to:
1. Build the board representation with offsets
2. Use DFS/backtracking to explore all possible paths from the starting position
3. Track visited squares and count maximum reachable squares
4. The answer is total squares minus maximum reachable squares

### Python Solution with Backtracking

```python
def solve():
  # Knight move offsets
  moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
      (1, -2), (1, 2), (2, -1), (2, 1)]

  case_num = 0

  while True:
    n = int(input())
    if n == 0:
      break

    case_num += 1

    # Read board configuration
    rows = []
    total_squares = 0

    for i in range(n):
      offset, count = map(int, input().split())
      rows.append((offset, count))
      total_squares += count

    # Create board: board[r] contains set of valid columns for row r
    board = []
    for offset, count in rows:
      board.append(set(range(offset, offset + count)))

    # Find starting position (first cell in first row)
    start_r, start_c = 0, rows[0][0]

    # DFS with backtracking to find maximum reachable
    max_reached = [0]

    def is_valid(r, c):
      return 0 <= r < n and c in board[r]

    def dfs(r, c, visited):
      max_reached[0] = max(max_reached[0], len(visited))

      for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if is_valid(nr, nc) and (nr, nc) not in visited:
          visited.add((nr, nc))
          dfs(nr, nc, visited)
          visited.remove((nr, nc))

    visited = {(start_r, start_c)}
    dfs(start_r, start_c, visited)

    unreachable = total_squares - max_reached[0]
    print(f"Case {case_num}, {unreachable} squares can not be reached.")

if __name__ == "__main__":
  solve()
```

### Optimized Solution with Pruning

```python
def solve():
  moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
      (1, -2), (1, 2), (2, -1), (2, 1)]

  case_num = 0

  while True:
    n = int(input())
    if n == 0:
      break

    case_num += 1

    # Read board
    rows = []
    total_squares = 0
    max_col = 0

    for i in range(n):
      offset, count = map(int, input().split())
      rows.append((offset, count))
      total_squares += count
      max_col = max(max_col, offset + count)

    # Create 2D grid for faster lookup
    # grid[r][c] = True if cell exists
    grid = [[False] * max_col for _ in range(n)]
    for r, (offset, count) in enumerate(rows):
      for c in range(offset, offset + count):
        grid[r][c] = True

    start_r, start_c = 0, rows[0][0]
    max_reached = [0]

    def is_valid(r, c):
      return 0 <= r < n and 0 <= c < max_col and grid[r][c]

    def dfs(r, c, count, visited):
      max_reached[0] = max(max_reached[0], count)

      # Early termination if we've reached all squares
      if count == total_squares:
        return

      for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if is_valid(nr, nc) and not visited[nr][nc]:
          visited[nr][nc] = True
          dfs(nr, nc, count + 1, visited)
          visited[nr][nc] = False

    visited = [[False] * max_col for _ in range(n)]
    visited[start_r][start_c] = True
    dfs(start_r, start_c, 1, visited)

    unreachable = total_squares - max_reached[0]
    print(f"Case {case_num}, {unreachable} squares can not be reached.")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(8^S) in worst case where S is total squares, but pruning significantly reduces this
- **Space Complexity:** O(S) for visited array and recursion stack

### Key Insight
This is a Hamiltonian path variant - we want to find the longest path visiting each square at most once. Backtracking explores all possible paths, and we keep track of the maximum number of squares reached. The answer is the total squares minus this maximum.
