# Mancunian and K-Ordered LCS

## Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 512MB

## Problem Statement

Find the k-ordered LCS of two sequences. A k-ordered LCS is the LCS of two sequences if you are allowed to change at most k elements in the first sequence to any value you wish.

## Input Format
- First line: N, M, and k (lengths of sequences and parameter)
- Second line: N integers (first sequence)
- Third line: M integers (second sequence)

## Constraints
- 1 ≤ N, M ≤ 2000
- 1 ≤ k ≤ 5
- 1 ≤ element ≤ 10⁹

## Output Format
Print the length of k-ordered LCS.

## Solution

### Approach
Use DP with an additional dimension for the number of changes used.
- `dp[i][j][c]` = length of LCS considering first i elements of seq1, first j elements of seq2, using c changes
- If we change element i to match element j, we use one change

### Python Solution

```python
def solve():
  n, m, k = map(int, input().split())
  a = list(map(int, input().split()))
  b = list(map(int, input().split()))

  # dp[i][j][c] = max LCS length using first i of a, first j of b, with c changes
  # c changes means we changed c elements in a to match elements in b

  dp = [[[-1] * (k + 2) for _ in range(m + 1)] for _ in range(n + 1)]

  # Base case
  for i in range(n + 1):
    for c in range(k + 2):
      dp[i][0][c] = 0
  for j in range(m + 1):
    for c in range(k + 2):
      dp[0][j][c] = 0

  for i in range(1, n + 1):
    for j in range(1, m + 1):
      for c in range(k + 1):
        # Option 1: Don't include a[i-1] in LCS
        dp[i][j][c] = max(dp[i][j][c], dp[i-1][j][c])

        # Option 2: Don't include b[j-1] in LCS
        dp[i][j][c] = max(dp[i][j][c], dp[i][j-1][c])

        # Option 3: Match a[i-1] with b[j-1]
        if a[i-1] == b[j-1]:
          dp[i][j][c] = max(dp[i][j][c], dp[i-1][j-1][c] + 1)

        # Option 4: Change a[i-1] to b[j-1] (costs 1 change)
        if c > 0:
          dp[i][j][c] = max(dp[i][j][c], dp[i-1][j-1][c-1] + 1)

  print(max(dp[n][m][c] for c in range(k + 1)))

if __name__ == "__main__":
  solve()
```

### Optimized Solution

```python
def solve():
  n, m, k = map(int, input().split())
  a = list(map(int, input().split()))
  b = list(map(int, input().split()))

  # dp[j][c] for space optimization
  INF = float('-inf')

  dp = [[0] * (k + 1) for _ in range(m + 1)]

  for i in range(1, n + 1):
    new_dp = [[0] * (k + 1) for _ in range(m + 1)]

    for j in range(1, m + 1):
      for c in range(k + 1):
        # Skip a[i-1]
        new_dp[j][c] = max(new_dp[j][c], dp[j][c])
        # Skip b[j-1]
        new_dp[j][c] = max(new_dp[j][c], new_dp[j-1][c])

        # Natural match
        if a[i-1] == b[j-1]:
          new_dp[j][c] = max(new_dp[j][c], dp[j-1][c] + 1)

        # Use a change
        if c > 0:
          new_dp[j][c] = max(new_dp[j][c], dp[j-1][c-1] + 1)

    dp = new_dp

  print(max(dp[m]))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × M × K)
- **Space Complexity:** O(M × K) with optimization

### Key Insight
This extends classical LCS by allowing k "free" matches where we pretend a[i] equals any b[j] we want. Each such pretend match costs one of our k changes.
