# LCS of three strings

## Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Given three strings X, Y, and Z, find the length of their longest common subsequence.

## Input Format
- T test cases
- Each test case:
  - First line: n, m, k (lengths of X, Y, Z)
  - Second line: three space-separated strings X, Y, Z

## Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N, M, K ≤ 100

## Output Format
For each test case, print the LCS length.

## Solution

### Approach
Extend the 2D LCS DP to 3D:
- dp[i][j][k] = LCS length of X[:i], Y[:j], Z[:k]
- If X[i-1] == Y[j-1] == Z[k-1]: dp[i][j][k] = dp[i-1][j-1][k-1] + 1
- Else: dp[i][j][k] = max(dp[i-1][j][k], dp[i][j-1][k], dp[i][j][k-1])

### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, m, k = map(int, input().split())
    parts = input().split()
    X, Y, Z = parts[0], parts[1], parts[2]

    # 3D DP
    dp = [[[0] * (k + 1) for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
      for j in range(1, m + 1):
        for l in range(1, k + 1):
          if X[i-1] == Y[j-1] == Z[l-1]:
            dp[i][j][l] = dp[i-1][j-1][l-1] + 1
          else:
            dp[i][j][l] = max(dp[i-1][j][l],
                    dp[i][j-1][l],
                    dp[i][j][l-1])

    print(dp[n][m][k])

if __name__ == "__main__":
  solve()
```

### Space-Optimized Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, m, k = map(int, input().split())
    parts = input().split()
    X, Y, Z = parts[0], parts[1], parts[2]

    # Only need 2 layers: current and previous for first dimension
    prev = [[0] * (k + 1) for _ in range(m + 1)]
    curr = [[0] * (k + 1) for _ in range(m + 1)]

    for i in range(1, n + 1):
      # Also need prev_j for second dimension
      prev_j = [0] * (k + 1)

      for j in range(1, m + 1):
        prev_l = 0
        for l in range(1, k + 1):
          if X[i-1] == Y[j-1] == Z[l-1]:
            curr[j][l] = prev[j-1][l-1] + 1
          else:
            curr[j][l] = max(prev[j][l],
                    curr[j-1][l],
                    curr[j][l-1])

      prev, curr = curr, [[0] * (k + 1) for _ in range(m + 1)]

    print(prev[m][k])

if __name__ == "__main__":
  solve()
```

### Recursive Solution with Memoization

```python
import sys
sys.setrecursionlimit(1000000)

def solve():
  t = int(input())

  for _ in range(t):
    n, m, k = map(int, input().split())
    parts = input().split()
    X, Y, Z = parts[0], parts[1], parts[2]

    memo = {}

    def lcs(i, j, l):
      if i == 0 or j == 0 or l == 0:
        return 0

      if (i, j, l) in memo:
        return memo[(i, j, l)]

      if X[i-1] == Y[j-1] == Z[l-1]:
        result = lcs(i-1, j-1, l-1) + 1
      else:
        result = max(lcs(i-1, j, l), lcs(i, j-1, l), lcs(i, j, l-1))

      memo[(i, j, l)] = result
      return result

    print(lcs(n, m, k))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n × m × k)
- **Space Complexity:** O(n × m × k), can be reduced to O(m × k)

### Key Insight
The 3-string LCS is a natural extension of 2-string LCS to 3D. When all three characters match, we extend the LCS. Otherwise, we try excluding one character at a time from each string and take the maximum.
