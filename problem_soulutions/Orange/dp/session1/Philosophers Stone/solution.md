# Philosophers Stone

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Harry is in a chamber with h×w tiles, each containing some philosopher's stones. He starts at any tile in the first row and moves to the last row, collecting stones along the way.

Movement rules:
- From a tile, he can move to the tile directly below, diagonally below-left, or diagonally below-right

Find the maximum stones Harry can collect.

## Input Format
- T test cases
- Each test case:
  - First line: h (rows), w (columns)
  - Next h lines: w integers (stones on each tile)

## Output Format
For each test case, print the maximum stones collectible.

## Example
```
Input:
1
3 4
1 2 3 4
5 6 7 8
9 10 11 12

Output:
24
```
Harry starts at row 1, column 3 (value 3), moves to row 2 column 3 (value 7), then to row 3 column 4 (value 12). But the optimal path is: start at column 4 (value 4), move diagonally to column 4 (value 8), then to column 4 (value 12) = 24. Or: 3 -> 7 -> 12 = 22. Actually optimal is 4 -> 8 -> 12 = 24.

## Solution

### Approach
Classic DP problem. Let dp[i][j] = max stones collectible reaching tile (i, j).

Transition: dp[i][j] = stones[i][j] + max(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])

Base case: dp[0][j] = stones[0][j] for all j in first row.

Answer: max(dp[h-1][j]) for all j.

### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    h, w = map(int, input().split())
    stones = []
    for _ in range(h):
      row = list(map(int, input().split()))
      stones.append(row)

    # dp[i][j] = max stones to reach (i, j)
    dp = [[0] * w for _ in range(h)]

    # Base case: first row
    for j in range(w):
      dp[0][j] = stones[0][j]

    # Fill DP
    for i in range(1, h):
      for j in range(w):
        # Can come from (i-1, j-1), (i-1, j), (i-1, j+1)
        best = dp[i-1][j]  # directly above

        if j > 0:
          best = max(best, dp[i-1][j-1])  # above-left
        if j < w - 1:
          best = max(best, dp[i-1][j+1])  # above-right

        dp[i][j] = stones[i][j] + best

    # Answer is max in last row
    print(max(dp[h-1]))

if __name__ == "__main__":
  solve()
```

### Space-Optimized Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    h, w = map(int, input().split())
    stones = []
    for _ in range(h):
      row = list(map(int, input().split()))
      stones.append(row)

    # Only need previous row
    prev = stones[0][:]

    for i in range(1, h):
      curr = [0] * w
      for j in range(w):
        best = prev[j]
        if j > 0:
          best = max(best, prev[j-1])
        if j < w - 1:
          best = max(best, prev[j+1])
        curr[j] = stones[i][j] + best
      prev = curr

    print(max(prev))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(h × w) per test case
- **Space Complexity:** O(w) with optimization

### Key Insight
This is a path-finding DP where we want to maximize the sum collected. Each cell can be reached from three cells above it. Process row by row, keeping track of the maximum stones reachable at each position.
