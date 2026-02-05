---
layout: simple
title: "Minimizing Coins"
permalink: /problem_solutions/dynamic_programming/minimizing_coins_analysis
difficulty: Easy
tags: [dp, optimization, 1d-dp, coin-change]
prerequisites: [coin_combinations_i]
cses_link: https://cses.fi/problemset/task/1634
---

# Minimizing Coins

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find minimum number of coins to make sum x |
| Type | Optimization DP (minimize) |
| Pattern | 1D DP with unbounded choices |
| Key Operation | `min()` over all coin choices |
| Time Complexity | O(n * x) |
| Space Complexity | O(x) |

## Learning Goals

By completing this problem, you will understand:

1. **Optimization DP vs Counting DP**: Using `min()` instead of `sum()` for optimization problems
2. **Handling "Impossible" Cases**: Using infinity and converting to -1 for output
3. **Unbounded Knapsack Pattern**: Each coin can be used unlimited times
4. **Base Case Design**: Why dp[0] = 0 is the correct initialization

## Problem Statement

Given n coin denominations and a target sum x, find the minimum number of coins needed to form the sum. Each coin can be used unlimited times.

**Input:**
- First line: n (number of coins), x (target sum)
- Second line: n coin values

**Output:**
- Minimum number of coins needed, or -1 if impossible

**Constraints:**
- 1 <= n <= 100
- 1 <= x <= 10^6
- 1 <= coin_value <= 10^6

**Example:**
```
Input:
3 11
1 5 7

Output:
3

Explanation: 11 = 7 + 2*2 is not optimal
             11 = 5 + 5 + 1 = 3 coins (optimal)
```

## Intuition

This is the classic "Coin Change" problem - but for **optimization** (finding minimum), not counting.

**Key Insight:** Unlike Coin Combinations I where we count ways using `sum()`, here we find the minimum using `min()`.

| Problem Type | Operation | What we track |
|--------------|-----------|---------------|
| Counting (Coin Combinations) | `dp[i] += dp[i-c]` | Number of ways |
| Optimization (Minimizing Coins) | `dp[i] = min(dp[i], dp[i-c] + 1)` | Minimum coins |

**Why +1?** When we use a coin of value c to reach sum i, we're adding 1 coin to the solution for sum (i-c).

## DP State Definition

```
dp[i] = minimum number of coins needed to make sum i
        OR infinity if sum i is impossible to achieve
```

**In plain language:** For each sum from 0 to x, what's the fewest coins we need?

## State Transition

For each sum i and each coin c where c <= i:

```
dp[i] = min(dp[i], dp[i - c] + 1)
```

**Translation:** "To make sum i using coin c, I need 1 coin (the coin c itself) plus the minimum coins to make the remaining sum (i - c)."

## Base Case

```
dp[0] = 0  // Zero coins needed to make sum zero
dp[1...x] = infinity  // Initially, all sums are "impossible"
```

**Why infinity?** We use infinity (not -1) during computation because:
- `min(infinity, valid_value)` = `valid_value` (correct behavior)
- `min(-1, valid_value)` = `-1` (wrong behavior!)

## Detailed Dry Run

**Example:** coins = [1, 3, 4], target x = 6

**Initialization:**
```
dp[0] = 0
dp[1..6] = INF (infinity)

Index:  0    1    2    3    4    5    6
dp:    [0] [INF][INF][INF][INF][INF][INF]
```

**Processing each sum:**

```
i = 1: Try coins [1, 3, 4]
  - coin 1: dp[1] = min(INF, dp[0] + 1) = min(INF, 1) = 1
  - coin 3: skip (3 > 1)
  - coin 4: skip (4 > 1)
  dp[1] = 1

i = 2: Try coins [1, 3, 4]
  - coin 1: dp[2] = min(INF, dp[1] + 1) = min(INF, 2) = 2
  - coin 3: skip (3 > 2)
  - coin 4: skip (4 > 2)
  dp[2] = 2

i = 3: Try coins [1, 3, 4]
  - coin 1: dp[3] = min(INF, dp[2] + 1) = min(INF, 3) = 3
  - coin 3: dp[3] = min(3, dp[0] + 1) = min(3, 1) = 1  <-- Better!
  - coin 4: skip (4 > 3)
  dp[3] = 1

i = 4: Try coins [1, 3, 4]
  - coin 1: dp[4] = min(INF, dp[3] + 1) = min(INF, 2) = 2
  - coin 3: dp[4] = min(2, dp[1] + 1) = min(2, 2) = 2
  - coin 4: dp[4] = min(2, dp[0] + 1) = min(2, 1) = 1  <-- Better!
  dp[4] = 1

i = 5: Try coins [1, 3, 4]
  - coin 1: dp[5] = min(INF, dp[4] + 1) = min(INF, 2) = 2
  - coin 3: dp[5] = min(2, dp[2] + 1) = min(2, 3) = 2
  - coin 4: dp[5] = min(2, dp[1] + 1) = min(2, 2) = 2
  dp[5] = 2

i = 6: Try coins [1, 3, 4]
  - coin 1: dp[6] = min(INF, dp[5] + 1) = min(INF, 3) = 3
  - coin 3: dp[6] = min(3, dp[3] + 1) = min(3, 2) = 2  <-- Better!
  - coin 4: dp[6] = min(2, dp[2] + 1) = min(2, 3) = 2
  dp[6] = 2
```

**Final DP Table:**
```
Index:  0   1   2   3   4   5   6
dp:    [0] [1] [2] [1] [1] [2] [2]
                         ^
                    Answer: dp[6] = 2 (coins: 3 + 3)
```

## Implementation

### Python Solution

```python
def minimizing_coins(n, x, coins):
 """
 Find minimum coins to make sum x.

 Args:
  n: number of coin types
  x: target sum
  coins: list of coin values

 Returns:
  Minimum coins needed, or -1 if impossible
 """
 INF = float('inf')

 # dp[i] = minimum coins to make sum i
 dp = [INF] * (x + 1)
 dp[0] = 0  # Base case: 0 coins for sum 0

 # Build up solutions for sums 1 to x
 for i in range(1, x + 1):
  for coin in coins:
   if coin <= i and dp[i - coin] != INF:
    dp[i] = min(dp[i], dp[i - coin] + 1)

 # Convert infinity to -1 for impossible case
 return dp[x] if dp[x] != INF else -1


def main():
 line1 = input().split()
 n, x = int(line1[0]), int(line1[1])
 coins = list(map(int, input().split()))

 print(minimizing_coins(n, x, coins))


if __name__ == "__main__":
 main()
```

### Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Initialize dp with 0 | All values stay 0, wrong answer | Initialize with infinity |
| Initialize dp with -1 | `min(-1, x)` always returns -1 | Use infinity for computation |
| Forget `dp[0] = 0` | No valid base case to build from | Always set `dp[0] = 0` |
| Return dp[x] directly | Returns infinity instead of -1 | Check and convert to -1 |
| Integer overflow with INF | INF + 1 might overflow | Check `dp[i-coin] != INF` before adding |
| Using `INT_MAX` as INF | `INT_MAX + 1` overflows | Use `1e9` or check before adding |

## Edge Cases

| Case | Input | Output | Explanation |
|------|-------|--------|-------------|
| Target is 0 | x = 0 | 0 | Zero coins needed for sum zero |
| Single coin exact match | coins=[5], x=5 | 1 | One coin suffices |
| Impossible case | coins=[3,5], x=1 | -1 | Cannot make 1 with coins 3 and 5 |
| Need many small coins | coins=[1], x=1000000 | 1000000 | Must use 1 million coins of value 1 |
| Large coin values | coins=[1000000], x=1 | -1 | Coin too large for target |
| Greedy fails | coins=[1,3,4], x=6 | 2 | Greedy picks 4+1+1=3, optimal is 3+3=2 |

## Why Greedy Fails

A common mistake is to try a greedy approach (always pick the largest coin). Consider:
- coins = [1, 3, 4], x = 6
- Greedy: 4 + 1 + 1 = 3 coins
- Optimal: 3 + 3 = 2 coins

The greedy approach fails because using the largest coin doesn't always lead to the minimum total.

## Complexity Analysis

**Time Complexity:** O(n * x)
- For each sum from 1 to x, we check all n coins
- Total: x * n operations

**Space Complexity:** O(x)
- We store one DP value for each sum from 0 to x

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Coin Change](https://leetcode.com/problems/coin-change/) | LeetCode 322 | Identical problem |
| [Coin Change 2](https://leetcode.com/problems/coin-change-2/) | LeetCode 518 | Count ways instead of minimize |
| [Coin Combinations I](https://cses.fi/problemset/task/1635) | CSES | Count ordered ways |
| [Coin Combinations II](https://cses.fi/problemset/task/1636) | CSES | Count unordered ways |
| [Money Sums](https://cses.fi/problemset/task/1745) | CSES | Find all achievable sums |

## Key Takeaways

1. **Optimization vs Counting:** Use `min()` for optimization problems, `sum()` for counting
2. **Infinity for Impossible:** Use infinity during computation, convert to -1 only at output
3. **Base Case Matters:** `dp[0] = 0` is essential - zero coins for zero sum
4. **Greedy Fails:** Dynamic programming is needed; greedy doesn't work for general coin sets
5. **Overflow Prevention:** Check for infinity before adding to avoid integer overflow
