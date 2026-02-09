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

## Example
```
Input:
4
1 1 1 1
2 1 1 0
1 1 1 0
1 0 0 1

Output:
12
2 2 3 2
```
A 4x4 board with given values. Placing bishops at (2,2) and (3,2) maximizes the total attacked cell values to 12. The bishops are on different diagonal parities so they don't share any attacked cells.

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
from collections import defaultdict

def solve():
  n = int(input())
  # Use list comprehension to read board
  board = [list(map(int, input().split())) for _ in range(n)]

  # Use defaultdict for diagonal sums
  main_diag = defaultdict(int)  # i - j -> sum
  anti_diag = defaultdict(int)  # i + j -> sum

  for i in range(n):
    for j in range(n):
      main_diag[i - j] += board[i][j]
      anti_diag[i + j] += board[i][j]

  # Track best positions for each parity
  best_even = (-1, -1, -1)  # (value, i, j)
  best_odd = (-1, -1, -1)

  for i in range(n):
    for j in range(n):
      val = main_diag[i - j] + anti_diag[i + j] - board[i][j]
      parity = (i + j) % 2

      # Simplified conditional assignment
      if parity == 0 and val > best_even[0]:
        best_even = (val, i, j)
      elif parity == 1 and val > best_odd[0]:
        best_odd = (val, i, j)

  total = best_even[0] + best_odd[0]
  # Tuple unpacking and 1-indexed conversion
  _, i1, j1 = best_even
  _, i2, j2 = best_odd

  print(total)
  print(i1 + 1, j1 + 1, i2 + 1, j2 + 1)

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
