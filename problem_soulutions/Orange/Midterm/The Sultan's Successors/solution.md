# The Sultan's Successors

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

The Sultan of Nubia has no children, so she has decided that the country will be split into up to k separate parts on her death and each part will be inherited by whoever performs best at some test.

To ensure that only highly intelligent people eventually become her successors, the Sultan has devised an ingenious test. In a large hall have been placed k chessboards. Each chessboard has numbers in the range 1 to 99 written on each square and is supplied with 8 jewelled chess queens.

The task facing each potential successor is to place the 8 queens on the chess board in such a way that no queen threatens another one, and so that the numbers on the squares thus selected sum to a number at least as high as one already chosen by the Sultan.

For those unfamiliar with the rules of chess, this implies that each row and column of the board contains exactly one queen, and each diagonal contains no more than one.

## Input Format
- Input will consist of k (the number of boards), on a line by itself
- Followed by k sets of 64 numbers, each set consisting of eight lines of eight numbers
- Each number will be a positive integer less than 100
- There will never be more than 20 boards

## Output Format
Output will consist of k numbers consisting of your k scores, each score on a line by itself and right justified in a field 5 characters wide.

## Solution

### Approach
This is the classic N-Queens problem with a twist - we need to maximize the sum of values on chosen squares.

Use backtracking:
1. Place queens row by row
2. For each row, try each column
3. Check if the position is safe (no queen in same column or diagonals)
4. Track the maximum sum achievable

### Python Solution

```python
def solve():
 def is_safe(queens, row, col):
  """Check if placing a queen at (row, col) is safe"""
  for r in range(row):
   c = queens[r]
   # Same column
   if c == col:
    return False
   # Same diagonal
   if abs(r - row) == abs(c - col):
    return False
  return True

 def backtrack(board, queens, row, current_sum, max_sum):
  """Backtrack to find all valid 8-queens placements"""
  if row == 8:
   return max(max_sum[0], current_sum)

  for col in range(8):
   if is_safe(queens, row, col):
    queens[row] = col
    new_sum = current_sum + board[row][col]
    max_sum[0] = max(max_sum[0], backtrack(board, queens, row + 1, new_sum, max_sum))

  return max_sum[0]

 k = int(input())

 for _ in range(k):
  board = []
  for i in range(8):
   row = list(map(int, input().split()))
   board.append(row)

  queens = [-1] * 8  # queens[i] = column of queen in row i
  max_sum = [0]

  result = backtrack(board, queens, 0, 0, max_sum)

  # Right-justify in field of 5 characters
  print(f"{result:5d}")

if __name__ == "__main__":
 solve()
```

### Optimized Solution with Bitmask

```python
def solve():
 def backtrack(board, row, cols, diag1, diag2, current_sum):
  """
  cols: bitmask of occupied columns
  diag1: bitmask of occupied \ diagonals
  diag2: bitmask of occupied / diagonals
  """
  if row == 8:
   return current_sum

  max_sum = 0
  for col in range(8):
   d1 = row - col + 7  # \ diagonal index (0-14)
   d2 = row + col      # / diagonal index (0-14)

   if not (cols & (1 << col)) and not (diag1 & (1 << d1)) and not (diag2 & (1 << d2)):
    new_sum = backtrack(
     board,
     row + 1,
     cols | (1 << col),
     diag1 | (1 << d1),
     diag2 | (1 << d2),
     current_sum + board[row][col]
    )
    max_sum = max(max_sum, new_sum)

  return max_sum

 k = int(input())

 for _ in range(k):
  board = []
  for i in range(8):
   row = list(map(int, input().split()))
   board.append(row)

  result = backtrack(board, 0, 0, 0, 0, 0)
  print(f"{result:5d}")

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(8!) = O(40320) per board - the number of valid 8-queens configurations is 92
- **Space Complexity:** O(8) for recursion depth

### Key Insight
There are only 92 valid ways to place 8 queens on a chessboard. We enumerate all of them and track the maximum sum.
