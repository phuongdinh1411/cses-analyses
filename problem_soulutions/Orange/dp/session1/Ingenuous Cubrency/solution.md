# Ingenuous Cubrency

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

People in Cubeland use cubic coins. Not only the unit of currency is called a cube but also the coins are shaped like cubes and their values are cubes. Coins with values of all cubic numbers up to 9261 (= 21³), i.e., coins with the denominations of 1, 8, 27, ..., up to 9261 cubes, are available in Cubeland.

Your task is to count the number of ways to pay a given amount using cubic coins of Cubeland.

For example, there are 3 ways to pay 21 cubes:
- Twenty one 1-cube coins
- One 8-cube coin and thirteen 1-cube coins
- Two 8-cube coins and five 1-cube coins

## Input Format
- Input consists of lines each containing an integer amount to be paid.
- All amounts are positive and less than 10000.

## Output Format
For each of the given amounts, output one line containing the number of ways to pay the given amount using the coins available in Cubeland.

## Example
```
Input:
10
21

Output:
2
3
```
For amount 10: Two ways - ten 1-cube coins, or one 8-cube coin and two 1-cube coins.
For amount 21: Three ways - as described in the problem statement.

## Solution

### Approach
This is a classic coin change counting problem (unbounded knapsack variant). We have coins with values 1³, 2³, 3³, ..., 21³ and need to count the number of ways to make a given amount.

Use dynamic programming where `dp[i]` = number of ways to make amount `i`.

### Python Solution

```python
def solve():
  # Precompute cubic coins: 1, 8, 27, 64, ..., 9261
  coins = [i**3 for i in range(1, 22)]  # 1^3 to 21^3

  # Precompute dp for all amounts up to 10000
  MAX_AMOUNT = 10000
  dp = [0] * (MAX_AMOUNT + 1)
  dp[0] = 1  # One way to make 0: use no coins

  # For each coin, update all amounts that can use it
  for coin in coins:
    for amount in range(coin, MAX_AMOUNT + 1):
      dp[amount] += dp[amount - coin]

  # Process queries
  import sys
  for line in sys.stdin:
    n = int(line.strip())
    print(dp[n])

if __name__ == "__main__":
  solve()
```

### Alternative Solution (Per-Query)

```python
def count_ways(amount):
  coins = [i**3 for i in range(1, 22)]

  dp = [0] * (amount + 1)
  dp[0] = 1

  for coin in coins:
    if coin > amount:
      break
    for i in range(coin, amount + 1):
      dp[i] += dp[i - coin]

  return dp[amount]

def solve():
  while True:
    try:
      n = int(input())
      print(count_ways(n))
    except EOFError:
      break

if __name__ == "__main__":
  solve()
```

### Solution with Memoization

```python
from functools import lru_cache

def solve():
  coins = tuple(i**3 for i in range(1, 22))

  @lru_cache(maxsize=None)
  def count(amount, idx):
    if amount == 0:
      return 1
    if amount < 0 or idx >= len(coins):
      return 0

    # Don't use current coin OR use it (and stay at same index for unlimited use)
    return count(amount, idx + 1) + count(amount - coins[idx], idx)

  while True:
    try:
      n = int(input())
      print(count(n, 0))
    except EOFError:
      break

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × K) where N is the amount and K is the number of coin types (21)
- **Space Complexity:** O(N) for the dp array

### Key Insight
This is the classic "coin change ways" problem. The key to counting combinations (not permutations) is to iterate over coins in the outer loop and amounts in the inner loop. This ensures each combination is counted exactly once by enforcing an ordering on coin usage.

The coins are: 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197, 2744, 3375, 4096, 4913, 5832, 6859, 8000, 9261
