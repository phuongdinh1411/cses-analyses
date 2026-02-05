---
layout: simple
title: "Two Sets II"
permalink: /problem_soulutions/dynamic_programming/two_sets_ii_analysis
difficulty: Medium
tags: [dp, subset-sum, counting, partition]
prerequisites: [money_sums]
cses_link: https://cses.fi/problemset/task/1093
---

# Two Sets II

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Count ways to partition {1, 2, ..., n} into two subsets with equal sum |
| Input | Integer n (1 <= n <= 500) |
| Output | Number of ways modulo 10^9 + 7 |
| Core Technique | Subset sum counting DP |
| Time Complexity | O(n * target) where target = n*(n+1)/4 |
| Space Complexity | O(target) |

## Learning Goals

After solving this problem, you will understand:
1. **Subset sum counting** - Counting number of ways to achieve a target sum
2. **Partition problem** - Dividing elements into equal-sum groups
3. **Handling symmetry** - Dividing by 2 to avoid double-counting partitions

## Problem Statement

Given a number n, count the number of ways to partition the set {1, 2, ..., n} into two subsets with equal sum.

### Example: n = 7

```
Set: {1, 2, 3, 4, 5, 6, 7}
Total sum = 1+2+3+4+5+6+7 = 28
Each subset needs sum = 28/2 = 14

Valid partitions (showing one subset, other is complement):
- {1, 6, 7} and {2, 3, 4, 5}     -> 1+6+7 = 14, 2+3+4+5 = 14
- {2, 5, 7} and {1, 3, 4, 6}     -> 2+5+7 = 14, 1+3+4+6 = 14
- {3, 4, 7} and {1, 2, 5, 6}     -> 3+4+7 = 14, 1+2+5+6 = 14
- {1, 2, 4, 7} and {3, 5, 6}     -> 1+2+4+7 = 14, 3+5+6 = 14
- {1, 3, 4, 6} and {2, 5, 7}     -> same as above (counted twice)
... and so on

Answer: 4
```

## Key Insight

**Mathematical Foundation:**
- Total sum of {1, 2, ..., n} = n * (n + 1) / 2
- If total sum is odd, partitioning into equal sums is **impossible** -> return 0
- If total sum is even, target sum for each subset = total / 2

**Problem Reduction:**
This reduces to: **Count the number of ways to select a subset of {1, 2, ..., n} that sums to target**

This is a classic subset sum counting problem!

## DP State Definition

```
dp[s] = number of ways to form sum s using some subset of numbers considered so far
```

**Base case:** `dp[0] = 1` (one way to form sum 0: select nothing)

**Transition:** For each number i from 1 to n:
```
dp[s] = dp[s] + dp[s - i]   for all s from target down to i
```

**Why iterate in reverse?** To ensure each number is used at most once (0/1 knapsack pattern).

## Critical Step: Divide by 2

**Important:** Each partition is counted twice!
- Selecting {1, 6, 7} for set A means {2, 3, 4, 5} is set B
- Selecting {2, 3, 4, 5} for set A means {1, 6, 7} is set B
- These are the SAME partition!

**Final answer = dp[target] / 2**

For modular arithmetic, use modular multiplicative inverse:
```
answer = dp[target] * inverse(2) % MOD
inverse(2) = pow(2, MOD-2, MOD)  # Fermat's little theorem
```

## Detailed Dry Run: n = 7

```
Total sum = 7 * 8 / 2 = 28 (even, so possible)
Target = 28 / 2 = 14

Initial: dp[0] = 1, all others = 0

After processing i=1:
  dp[1] = dp[1] + dp[0] = 0 + 1 = 1
  dp = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

After processing i=2:
  dp[2] = dp[2] + dp[0] = 0 + 1 = 1
  dp[3] = dp[3] + dp[1] = 0 + 1 = 1
  dp = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

After processing i=3:
  dp[3] += dp[0] -> dp[3] = 1 + 1 = 2  (ways: {3}, {1,2})
  dp[4] += dp[1] -> dp[4] = 0 + 1 = 1
  dp[5] += dp[2] -> dp[5] = 0 + 1 = 1
  dp[6] += dp[3] -> dp[6] = 0 + 1 = 1  (before update, dp[3]=1)
  dp = [1, 1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

... continue for i=4,5,6,7 ...

After processing i=7:
  dp[14] = 8 (raw count of subsets summing to 14)

Final answer = 8 / 2 = 4
```

## Solution Code

### Python

```python
def two_sets_ii(n: int) -> int:
 MOD = 10**9 + 7

 # Calculate total sum
 total = n * (n + 1) // 2

 # If odd, impossible to partition equally
 if total % 2 == 1:
  return 0

 target = total // 2

 # dp[s] = number of ways to achieve sum s
 dp = [0] * (target + 1)
 dp[0] = 1  # One way to form sum 0

 # Process each number from 1 to n
 for i in range(1, n + 1):
  # Iterate in reverse to avoid using same number twice
  for s in range(target, i - 1, -1):
   dp[s] = (dp[s] + dp[s - i]) % MOD

 # Divide by 2 to account for symmetry (A,B) = (B,A)
 # Use modular inverse: inv(2) = 2^(MOD-2) mod MOD
 inv2 = pow(2, MOD - 2, MOD)
 return (dp[target] * inv2) % MOD


# Example usage
if __name__ == "__main__":
 n = int(input())
 print(two_sets_ii(n))
```

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Forgetting to divide by 2 | Each partition (A,B) is counted as both (A,B) and (B,A) | Multiply by modular inverse of 2 |
| Forward iteration in DP | Same number gets used multiple times | Iterate from target down to i |
| Integer overflow | n*(n+1)/2 can exceed int for large n | Use long long for total sum |
| Wrong modular inverse | Using regular division in modular arithmetic | Use Fermat's theorem: inv = pow(2, MOD-2, MOD) |
| Not checking odd sum | Total sum might be odd | Return 0 immediately if total % 2 == 1 |

## Edge Cases

| Input | Total Sum | Output | Reason |
|-------|-----------|--------|--------|
| n = 1 | 1 (odd) | 0 | Cannot partition odd sum equally |
| n = 2 | 3 (odd) | 0 | Cannot partition odd sum equally |
| n = 3 | 6 (even) | 1 | Only {1,2} and {3} works |
| n = 7 | 28 (even) | 4 | See dry run above |

**Pattern:** Answer is 0 when n % 4 == 1 or n % 4 == 2 (total sum is odd in these cases).

## Complexity Analysis

- **Time:** O(n * target) = O(n * n^2/4) = O(n^3/4)
  - For n = 500: approximately 31 million operations
- **Space:** O(target) = O(n^2/4)
  - For n = 500: approximately 62,500 integers

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | LeetCode | Boolean DP (can/cannot), not counting |
| [Money Sums](https://cses.fi/problemset/task/1745) | CSES | Find all achievable sums |
| [Minimizing Coins](https://cses.fi/problemset/task/1634) | CSES | Minimize count, not enumerate ways |
| [Target Sum](https://leetcode.com/problems/target-sum/) | LeetCode | + and - operations |

## Key Takeaways

1. **Subset sum counting** is a fundamental DP pattern
2. **Reverse iteration** ensures each element is used at most once
3. **Symmetry handling** - always check if your count includes duplicates
4. **Modular inverse** is essential for division in modular arithmetic
