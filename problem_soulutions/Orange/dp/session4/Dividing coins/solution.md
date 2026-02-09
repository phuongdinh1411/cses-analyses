# Dividing coins

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 5000ms
- **Memory Limit:** 512MB

## Problem Statement

Divide a bag of coins between two people as fairly as possible. Minimize the absolute difference between the total values each person receives.

## Input Format
- First line: n (number of test cases)
- Each test case:
  - Line 1: m (number of coins, m ≤ 100)
  - Line 2: m coin values (1 to 500 cents each)

## Output Format
For each test case, print the minimum possible difference.

## Example
```
Input:
2
3
2 3 5
4
1 2 3 4

Output:
0
0
```
Test 1: Coins [2, 3, 5] sum to 10. Split as {5} vs {2,3}: 5 vs 5, difference = 0.
Test 2: Coins [1, 2, 3, 4] sum to 10. Split as {1,4} vs {2,3}: 5 vs 5, difference = 0.

## Solution

### Approach
This is the Partition Problem - a variant of subset sum.

Let total = sum of all coins. We want to find subset with sum closest to total/2. The minimum difference will be total - 2 * (closest sum to total/2).

Use DP to find all achievable sums up to total/2.

### Python Solution

```python
def solve():
  n = int(input())

  for _ in range(n):
    m = int(input())
    coins = list(map(int, input().split()))

    total = sum(coins)
    target = total // 2

    # dp[i] = True if sum i is achievable
    dp = [False] * (target + 1)
    dp[0] = True

    for coin in coins:
      # Process in reverse to avoid using same coin twice
      for s in range(target, coin - 1, -1):
        dp[s] = dp[s] or dp[s - coin]

    # Find largest achievable sum <= target using next with reversed range
    best = next(s for s in range(target, -1, -1) if dp[s])

    # Minimum difference
    print(total - 2 * best)

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Bitset

```python
def solve():
  n = int(input())

  for _ in range(n):
    m = int(input())
    coins = list(map(int, input().split()))

    total = sum(coins)
    target = total // 2

    # Use integer as bitset for achievable sums
    achievable = 1  # bit 0 set = sum 0 achievable

    for coin in coins:
      achievable |= (achievable << coin)

    # Mask to only consider sums <= target
    mask = (1 << (target + 1)) - 1
    achievable &= mask

    # Find highest set bit
    best = achievable.bit_length() - 1

    print(total - 2 * best)

if __name__ == "__main__":
  solve()
```

### Recursive Solution with Memoization

```python
def solve():
  n = int(input())

  for _ in range(n):
    m = int(input())
    coins = list(map(int, input().split()))

    total = sum(coins)
    target = total // 2

    memo = {}

    def can_make(idx, remaining):
      if remaining == 0:
        return True
      if idx == m or remaining < 0:
        return False

      if (idx, remaining) in memo:
        return memo[(idx, remaining)]

      result = can_make(idx + 1, remaining) or \
          can_make(idx + 1, remaining - coins[idx])

      memo[(idx, remaining)] = result
      return result

    # Find largest achievable sum
    for s in range(target, -1, -1):
      if can_make(0, s):
        print(total - 2 * s)
        break

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(m × total)
- **Space Complexity:** O(total)

### Key Insight
To minimize difference when splitting into two groups, find a subset with sum as close to total/2 as possible. If one group has sum S, the other has total - S, difference is |total - 2S|. This is minimized when S is closest to total/2. Use 0/1 knapsack DP to find achievable sums.
