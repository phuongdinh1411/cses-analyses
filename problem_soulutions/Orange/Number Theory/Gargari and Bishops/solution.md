# Gargari and Bishops

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

## Problem Statement

Place two bishops on an n×n chessboard such that:
1. No cell is attacked by both bishops
2. Sum of values of all attacked cells is maximized

Bishops attack along diagonals. A cell is attacked if it's on any diagonal of a bishop.

## Input Format
- First line: n (2 ≤ n ≤ 2000)
- Next n lines: n integers aij (0 ≤ aij ≤ 10^9) - cell values

## Output Format
- Line 1: Maximum total value
- Line 2: x1, y1, x2, y2 (positions of two bishops, 1-indexed)

## Solution

### Approach
Two diagonals through (i, j):
- Main diagonal: i - j (constant)
- Anti-diagonal: i + j (constant)

Two bishops don't share cells if they're on diagonals of different "parity":
- Bishop 1 on cell where (i + j) is even
- Bishop 2 on cell where (i + j) is odd

Precompute sum of each diagonal, then for each cell compute total attack value. Find best cell for each parity.

### Python Solution

```python
def solve():
  n = int(input())
  board = []
  for _ in range(n):
    row = list(map(int, input().split()))
    board.append(row)

  # Diagonal sums
  # Main diagonal: indexed by i - j (range: -(n-1) to n-1)
  # Anti diagonal: indexed by i + j (range: 0 to 2n-2)

  main_diag = {}  # i - j -> sum
  anti_diag = {}  # i + j -> sum

  for i in range(n):
    for j in range(n):
      d1 = i - j
      d2 = i + j

      main_diag[d1] = main_diag.get(d1, 0) + board[i][j]
      anti_diag[d2] = anti_diag.get(d2, 0) + board[i][j]

  # For each cell, compute bishop value (don't double count the cell itself)
  # bishop_value[i][j] = main_diag[i-j] + anti_diag[i+j] - board[i][j]

  best_even = (-1, -1, -1)  # (value, i, j)
  best_odd = (-1, -1, -1)

  for i in range(n):
    for j in range(n):
      val = main_diag[i - j] + anti_diag[i + j] - board[i][j]
      parity = (i + j) % 2

      if parity == 0:
        if val > best_even[0]:
          best_even = (val, i, j)
      else:
        if val > best_odd[0]:
          best_odd = (val, i, j)

  total = best_even[0] + best_odd[0]
  # Convert to 1-indexed
  x1, y1 = best_even[1] + 1, best_even[2] + 1
  x2, y2 = best_odd[1] + 1, best_odd[2] + 1

  print(total)
  print(x1, y1, x2, y2)

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  n = int(input())
  board = [list(map(int, input().split())) for _ in range(n)]

  # Diagonal sums using arrays
  # Main: i - j + (n-1) maps to range [0, 2n-2]
  # Anti: i + j maps to range [0, 2n-2]

  main = [0] * (2 * n - 1)
  anti = [0] * (2 * n - 1)

  for i in range(n):
    for j in range(n):
      main[i - j + n - 1] += board[i][j]
      anti[i + j] += board[i][j]

  # Find best positions for each parity
  best = [(-1, 0, 0), (-1, 0, 0)]  # [even_parity, odd_parity]

  for i in range(n):
    for j in range(n):
      score = main[i - j + n - 1] + anti[i + j] - board[i][j]
      parity = (i + j) % 2

      if score > best[parity][0]:
        best[parity] = (score, i + 1, j + 1)

  total = best[0][0] + best[1][0]
  print(total)
  print(best[0][1], best[0][2], best[1][1], best[1][2])

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n²)
- **Space Complexity:** O(n)

### Key Insight
Two bishops on cells with different (i+j) parity never share diagonals. Precompute sum for each diagonal, then for each cell compute total attack value in O(1). This avoids O(n³) brute force. The cell itself appears in both its diagonals, so subtract it once to avoid double-counting.
