---
layout: simple
title: "Money Sums"
permalink: /problem_soulutions/dynamic_programming/money_sums_analysis
difficulty: Easy
tags: [dp, subset-sum, boolean-dp]
prerequisites: [coin_combinations_ii]
cses_link: https://cses.fi/problemset/task/1745
---

# Money Sums

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find all distinct sums achievable using given coins |
| Input | n coins with values x_1, x_2, ..., x_n |
| Output | Count of distinct sums + sorted list of all sums |
| Constraints | 1 <= n <= 100, 1 <= x_i <= 1000 |
| Time Limit | 1.00 s |

## Learning Goals

By solving this problem, you will learn:
- **Boolean DP**: Using True/False states instead of counts
- **Subset Sum Pattern**: Classic DP pattern for achievability problems
- **Extracting Results from DP**: Collecting all valid states after DP completes

## Problem Statement

You have n coins with certain values. Your task is to find all money sums you can create using these coins.

**Input**: First line: integer n. Second line: n integers x_1, x_2, ..., x_n (coin values).

**Output**: First line: number of distinct sums. Second line: all sums in increasing order.

**Example**:
```
Input:
4
4 2 5 2

Output:
9
2 4 5 6 7 8 9 11 13
```

**Explanation**: With coins [4, 2, 5, 2], we can make sums: 2, 4, 5, 6 (4+2), 7 (5+2), 8 (4+2+2), 9 (4+5), 11 (4+5+2), 13 (4+5+2+2).

## Intuition

This is a **subset sum** problem where we need to find ALL achievable sums, not just check if one specific sum is possible.

**Key Insight**: Use a boolean DP array where `dp[s] = True` means sum `s` can be achieved.

Unlike counting problems, we only care about **can or cannot** - a binary decision for each possible sum.

## DP State Definition

```
dp[s] = True/False
```

**Meaning**: Can we make sum `s` using some subset of the given coins?

- `dp[0] = True` (empty subset makes sum 0)
- `dp[s] = True` if there exists a coin `c` such that `dp[s-c]` was True before adding coin `c`

**Final Answer**: All indices `s` where `dp[s] = True` (excluding 0)

## State Transition

For each coin `c`, we can extend any existing achievable sum `s-c` to reach sum `s`:

```
dp[s] = dp[s] OR dp[s - c]
```

**Critical**: Process sums in **REVERSE order** (high to low) to ensure each coin is used at most once.

## Algorithm

```
1. Initialize dp[0] = True, all others False
2. For each coin c:
      For s from max_sum down to c:  # REVERSE iteration
          if dp[s - c] is True:
              dp[s] = True
3. Collect all s where dp[s] = True (s > 0)
4. Output count and sorted list
```

**Why reverse iteration?**
- Forward iteration would allow using the same coin multiple times
- Reverse ensures when we check `dp[s-c]`, it reflects state WITHOUT current coin

## Dry Run Example

**Input**: coins = [4, 2, 5], max_sum = 11

**Initial State**: `dp = [T, F, F, F, F, F, F, F, F, F, F, F]` (index 0-11)

**Process coin 4**:
```
s=11: dp[7]=F, skip
s=10: dp[6]=F, skip
...
s=4:  dp[0]=T, set dp[4]=T

dp = [T, F, F, F, T, F, F, F, F, F, F, F]
```

**Process coin 2**:
```
s=11: dp[9]=F, skip
...
s=6:  dp[4]=T, set dp[6]=T
...
s=4:  dp[2]=F, skip
s=3:  dp[1]=F, skip
s=2:  dp[0]=T, set dp[2]=T

dp = [T, F, T, F, T, F, T, F, F, F, F, F]
Achievable: {2, 4, 6}
```

**Process coin 5**:
```
s=11: dp[6]=T, set dp[11]=T
s=10: dp[5]=F, skip
s=9:  dp[4]=T, set dp[9]=T
s=8:  dp[3]=F, skip
s=7:  dp[2]=T, set dp[7]=T
s=6:  dp[1]=F, skip (already T)
s=5:  dp[0]=T, set dp[5]=T

dp = [T, F, T, F, T, T, T, T, F, T, F, T]
Achievable: {2, 4, 5, 6, 7, 9, 11}
```

**Output**: 7 distinct sums: 2 4 5 6 7 9 11

## Implementation

### Python Solution

```python
def solve():
 n = int(input())
 coins = list(map(int, input().split()))

 max_sum = sum(coins)
 dp = [False] * (max_sum + 1)
 dp[0] = True

 for coin in coins:
  # Iterate in REVERSE to use each coin only once
  for s in range(max_sum, coin - 1, -1):
   if dp[s - coin]:
    dp[s] = True

 # Collect all achievable sums (excluding 0)
 result = [s for s in range(1, max_sum + 1) if dp[s]]

 print(len(result))
 print(' '.join(map(str, result)))

solve()
```

### Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n * S) | n coins, S = sum of all coins (max 100,000) |
| Space | O(S) | 1D DP array of size S |

Where S = x_1 + x_2 + ... + x_n <= 100 * 1000 = 100,000

## Common Mistakes

### 1. Forward Iteration (WRONG)

```python
# WRONG: Uses each coin multiple times
for coin in coins:
 for s in range(coin, max_sum + 1):  # Forward = WRONG
  if dp[s - coin]:
   dp[s] = True
```

This allows using the same coin multiple times because `dp[s-coin]` may have been updated in the current iteration.

### 2. Forgetting to Exclude Sum 0

```python
# WRONG: Includes 0 in result
result = [s for s in range(max_sum + 1) if dp[s]]
```

The problem asks for money sums you can CREATE, implying positive sums only.

### 3. Not Sorting Output

The output must be in increasing order. While our approach naturally produces sorted output (iterating 1 to max_sum), be careful if using a set.

### 4. Integer Overflow in C++

Max sum can be 100,000 - use appropriate data types. Using `int` is fine here.

## Edge Cases

| Case | Input | Output |
|------|-------|--------|
| Single coin | n=1, coins=[5] | 1 sum: 5 |
| All same coins | n=3, coins=[2,2,2] | 3 sums: 2,4,6 |
| Large sum | n=100, all coins=1000 | Sums 1000 to 100000 |
| Duplicate coins | n=4, coins=[1,1,2,2] | 6 sums: 1,2,3,4,5,6 |

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | LeetCode | Check if specific sum achievable |
| [Coin Change](https://leetcode.com/problems/coin-change/) | LeetCode | Minimum coins for target (unlimited coins) |
| [Target Sum](https://leetcode.com/problems/target-sum/) | LeetCode | Count ways with +/- operations |
| [Coin Combinations II](https://cses.fi/problemset/task/1636) | CSES | Count ways (unlimited coins) |

## Key Takeaways

1. **Boolean DP** is simpler than counting - just True/False states
2. **Reverse iteration** is crucial for 0/1 knapsack-style problems
3. **Subset sum** is a fundamental pattern - recognize it in variations
4. The answer extraction step (collecting True indices) is straightforward but don't forget it
