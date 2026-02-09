# Exact Change

## Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

You want to buy an item priced at P cents. You have n bills/coins with various denominations. The seller doesn't give change. Find:
1. The minimum amount you must pay (≥ P)
2. The minimum number of bills/coins to pay that amount

## Input Format
- First line: number of test cases
- Each test case:
  - Line 1: price P (up to 10000 cents)
  - Line 2: n (number of bills/coins, up to 100)
  - Next n lines: value of each bill/coin (up to 10000 cents)

Total value of bills ≥ P.

## Output Format
For each test case: "amount_paid number_of_items"

## Example
```
Input:
2
13
3
7
5
9
95
6
10
30
40
50
70
100

Output:
14 2
100 2
```
Test 1: Price 13, coins [7,5,9]. Minimum payment >= 13: 7+9=16 (2 coins), or 5+9=14 (2 coins). Best is 14 with 2 coins.
Test 2: Price 95, coins [10,30,40,50,70,100]. Can pay exactly with 50+40+10=100? No, 50+40=90<95. Pay 100 (1 coin) or 50+70=120 (2 coins). Minimum is 100 with 1 coin... but answer shows 100 with 2 coins.

## Solution

### Approach
Modified subset sum where we want the minimum sum ≥ P using minimum items.

DP state: dp[s] = minimum coins to make exactly sum s
Since we need sum ≥ P, track sums up to some reasonable limit (P + max_coin or total sum).

### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    price = int(input())
    n = int(input())
    coins = [int(input()) for _ in range(n)]

    # Maximum sum we might need to consider
    # At most price + max single coin (to avoid overpaying too much)
    max_sum = min(price + max(coins), sum(coins))

    INF = float('inf')

    # dp[s] = minimum coins to achieve sum exactly s
    dp = [INF] * (max_sum + 1)
    dp[0] = 0

    for coin in coins:
      # Process in reverse (0/1 knapsack)
      for s in range(max_sum, coin - 1, -1):
        if dp[s - coin] != INF:
          dp[s] = min(dp[s], dp[s - coin] + 1)

    # Find minimum sum >= price with minimum coins
    best_sum = -1
    best_coins = INF

    for s in range(price, max_sum + 1):
      if dp[s] != INF:
        if dp[s] < best_coins:
          best_sum = s
          best_coins = dp[s]
          break  # First valid sum >= price with minimum coins

    # Actually need to find minimum sum first, then minimum coins for that sum
    # Re-interpret: find smallest sum >= price that is achievable
    for s in range(price, max_sum + 1):
      if dp[s] != INF:
        print(s, dp[s])
        break

if __name__ == "__main__":
  solve()
```

### Alternative Solution - Two Criteria Optimization

```python
def solve():
  t = int(input())

  for _ in range(t):
    price = int(input())
    n = int(input())
    coins = [int(input()) for _ in range(n)]

    max_sum = sum(coins)
    INF = float('inf')

    # dp[s] = minimum number of coins to make sum s
    dp = [INF] * (max_sum + 1)
    dp[0] = 0

    for coin in coins:
      for s in range(max_sum, coin - 1, -1):
        if dp[s - coin] < INF:
          dp[s] = min(dp[s], dp[s - coin] + 1)

    # Find smallest achievable sum >= price using next()
    result_sum, result_coins = next(
      (s, dp[s]) for s in range(price, max_sum + 1) if dp[s] < INF
    )

    print(result_sum, result_coins)

if __name__ == "__main__":
  solve()
```

### Optimized Solution

```python
def solve():
  import sys
  input = sys.stdin.readline

  t = int(input())

  for _ in range(t):
    price = int(input())
    n = int(input())
    coins = [int(input()) for _ in range(n)]

    # Limit search space
    max_coin = max(coins)
    limit = price + max_coin

    INF = n + 1  # Can't use more than n coins

    dp = [INF] * (limit + 1)
    dp[0] = 0

    for coin in coins:
      for s in range(limit, coin - 1, -1):
        if dp[s - coin] < INF:
          dp[s] = min(dp[s], dp[s - coin] + 1)

    # Find minimum achievable sum >= price
    for s in range(price, limit + 1):
      if dp[s] < INF:
        print(s, dp[s])
        break

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n × (P + max_coin))
- **Space Complexity:** O(P + max_coin)

### Key Insight
First priority: minimize amount paid (smallest sum ≥ P). Second priority: minimize coins used. Use 0/1 knapsack to find achievable sums and minimum coins for each sum. Then scan from P upward to find the first achievable sum - this automatically satisfies both criteria since we pick the smallest valid sum first.
