# Maximum Profit

## Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

## Problem Statement

Given stock prices for N days and at most K transactions allowed, find the maximum profit. A transaction is buying then selling. You cannot buy a new stock until the previous transaction is completed.

## Input Format
- First line: T (number of test cases)
- For each test case:
  - First line: K (max transactions)
  - Second line: N (number of days)
  - Third line: N prices

## Constraints
- 1 ≤ T ≤ 100
- 0 < K ≤ 10
- 2 ≤ N ≤ 30
- 0 ≤ A[i] ≤ 1000

## Output Format
Print maximum profit (0 if no profit possible).

## Solution

### Approach
Use DP with states: `dp[t][d]` = max profit using at most t transactions up to day d.

For each day, either:
1. Don't trade: `dp[t][d] = dp[t][d-1]`
2. Complete a transaction: buy on day j, sell on day d
   `dp[t][d] = max(dp[t-1][j-1] + price[d] - price[j])` for all j < d

### Python Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  k = int(input())
  n = int(input())
  prices = list(map(int, input().split()))

  if n <= 1 or k == 0:
   print(0)
   continue

  # If k >= n/2, we can do unlimited transactions
  if k >= n // 2:
   profit = sum(max(0, prices[i+1] - prices[i]) for i in range(n-1))
   print(profit)
   continue

  # DP approach
  # dp[t][d] = max profit with at most t transactions ending on or before day d
  dp = [[0] * n for _ in range(k + 1)]

  for t in range(1, k + 1):
   max_diff = -prices[0]  # max of (dp[t-1][j] - prices[j])

   for d in range(1, n):
    # Don't sell on day d
    dp[t][d] = dp[t][d-1]

    # Sell on day d (bought on some earlier day j)
    dp[t][d] = max(dp[t][d], prices[d] + max_diff)

    # Update max_diff for future days
    max_diff = max(max_diff, dp[t-1][d] - prices[d])

  print(dp[k][n-1])

if __name__ == "__main__":
 solve()
```

### Alternative Solution (Clearer DP)

```python
def solve():
 T = int(input())

 for _ in range(T):
  k = int(input())
  n = int(input())
  prices = list(map(int, input().split()))

  if n <= 1:
   print(0)
   continue

  # dp[i][j][0] = max profit at day i with j transactions, not holding
  # dp[i][j][1] = max profit at day i with j transactions, holding

  INF = float('inf')
  dp = [[[-INF, -INF] for _ in range(k + 2)] for _ in range(n + 1)]
  dp[0][0][0] = 0

  for i in range(n):
   for j in range(k + 1):
    # Not holding stock
    if dp[i][j][0] > -INF:
     # Stay not holding
     dp[i+1][j][0] = max(dp[i+1][j][0], dp[i][j][0])
     # Buy stock
     dp[i+1][j][1] = max(dp[i+1][j][1], dp[i][j][0] - prices[i])

    # Holding stock
    if dp[i][j][1] > -INF:
     # Stay holding
     dp[i+1][j][1] = max(dp[i+1][j][1], dp[i][j][1])
     # Sell stock (complete transaction)
     dp[i+1][j+1][0] = max(dp[i+1][j+1][0], dp[i][j][1] + prices[i])

  ans = max(dp[n][j][0] for j in range(k + 1))
  print(max(0, ans))

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × K)
- **Space Complexity:** O(N × K)

### Key Insight
This is the "Best Time to Buy and Sell Stock" problem with at most K transactions. The optimized DP tracks `max_diff` to avoid an O(N²) inner loop, reducing complexity from O(N²K) to O(NK).
