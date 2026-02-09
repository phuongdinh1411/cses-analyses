# OR in Matrix

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

## Problem Statement

Define logical OR on {0, 1}: result is 1 if either or both values are 1, otherwise 0.

Nam has matrix A of m×n with elements 0 or 1. He creates matrix B where:
- B[i][j] = A[i][1] OR A[i][2] OR ... OR A[i][n] (OR of row i) AND A[1][j] OR A[2][j] OR ... OR A[m][j] (OR of column j)

Actually: B[i][j] = OR of all elements in row i AND column j of matrix A.

Given matrix B, find if matrix A exists that produces B.

## Input Format
- First line: m, n (dimensions)
- Next m lines: n integers (matrix B, each element is 0 or 1)

## Output Format
Print "NO" if no valid A exists. Otherwise print "YES" and a valid matrix A.

## Example
```
Input:
2 2
1 0
0 0

Output:
YES
1 0
0 0
```
With A = [[1,0],[0,0]], we compute B: B[0][0] = (1 OR 0) OR (1 OR 0) = 1, B[0][1] = (1 OR 0) OR (0 OR 0) = 1... Actually this needs to produce B[0][1]=0, so row 0 and col 1 of A must be all zeros. The valid A is [[1,0],[0,0]] which produces B=[[1,0],[0,0]].

## Solution

### Approach
Key observations:
1. If B[i][j] = 0, then both row i of A and column j of A must be all zeros
2. If B[i][j] = 1, then at least one element in row i OR column j of A must be 1

Strategy:
1. Start with A filled with 1s
2. For each B[i][j] = 0, set entire row i and column j of A to 0
3. Verify: compute B' from A and check if B' = B

### Python Solution

```python
def solve():
  m, n = map(int, input().split())
  B = [list(map(int, input().split())) for _ in range(m)]

  # Initialize A with all 1s
  A = [[1] * n for _ in range(m)]

  # For each B[i][j] = 0, entire row i and column j of A must be 0
  for i in range(m):
    for j in range(n):
      if B[i][j] == 0:
        A[i] = [0] * n  # Set row i to all 0s
        for k in range(m):
          A[k][j] = 0  # Set column j to all 0s

  # Precompute row OR and column OR using any()
  row_or = [any(A[i]) for i in range(m)]
  col_or = [any(A[i][j] for i in range(m)) for j in range(n)]

  # Verify: B'[i][j] = row_or[i] | col_or[j]
  valid = all(
    (row_or[i] or col_or[j]) == B[i][j]
    for i in range(m)
    for j in range(n)
  )

  if valid:
    print("YES")
    for row in A:
      print(' '.join(map(str, row)))
  else:
    print("NO")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  m, n = map(int, input().split())
  B = [list(map(int, input().split())) for _ in range(m)]

  # For B[i][j] = 0: row i and col j in A must be all 0s
  # For B[i][j] = 1: at least one of row i or col j in A must have a 1

  zero_rows = set()
  zero_cols = set()

  zero_rows = {i for i in range(m) for j in range(n) if B[i][j] == 0}
  zero_cols = {j for i in range(m) for j in range(n) if B[i][j] == 0}

  # Build A: 1 unless in zero_row or zero_col
  A = [[0 if i in zero_rows or j in zero_cols else 1
    for j in range(n)] for i in range(m)]

  # Verify
  row_or = [any(row) for row in A]
  col_or = [any(A[i][j] for i in range(m)) for j in range(n)]

  valid = all(
    (1 if (row_or[i] or col_or[j]) else 0) == B[i][j]
    for i in range(m)
    for j in range(n)
  )

  if not valid:
    print("NO")
    return

  print("YES")
  for row in A:
    print(' '.join(map(str, row)))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(m × n)
- **Space Complexity:** O(m × n)

### Key Insight
B[i][j] = 0 forces all of row i and column j in A to be 0. After marking these constraints, fill remaining cells with 1. Then verify the constructed A produces B. If B[i][j] = 1 but all of row i and column j are forced to 0, no solution exists.
