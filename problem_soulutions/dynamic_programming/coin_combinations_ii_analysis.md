# CSES Coin Combinations II - Problem Analysis

## Problem Statement
Consider a money system consisting of n coins. Each coin has a positive integer value. Your task is to calculate the number of distinct ordered ways you can produce a sum of money x using the available coins.

For example, if the coins are {2,3,5} and the desired sum is 9, there are 3 ways:
- 2+2+5
- 3+3+3
- 2+2+2+3

Note: The order of coins doesn't matter in this problem.

### Input
The first input line has two integers n and x: the number of coins and the desired sum of money.
The second line has n distinct integers c1,c2,…,cn: the value of each coin.

### Output
Print one integer: the number of ways modulo 10^9+7.

### Constraints
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10^6
- 1 ≤ ci ≤ 10^6

### Example
```
Input:
3 9
2 3 5

Output:
3
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(n^x)
**Description**: Try all possible combinations of coins recursively, ensuring no duplicates.

```python
def coin_combinations_ii_brute_force(n, x, coins):
    MOD = 10**9 + 7
    
    def count_ways(target, last_coin):
        if target == 0:
            return 1
        if target < 0:
            return 0
        
        ways = 0
        for coin in coins:
            if coin >= last_coin:  # Ensure non-decreasing order
                ways += count_ways(target - coin, coin)
        
        return ways % MOD
    
    return count_ways(x, 0)
```

**Why this is inefficient**: We're trying all possible combinations of coins, which leads to exponential complexity. For each target, we try all coin values, leading to O(n^x) complexity.

### Improvement 1: Recursive with Memoization - O(n*x)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def coin_combinations_ii_memoization(n, x, coins):
    MOD = 10**9 + 7
    memo = {}
    
    def count_ways(target, last_coin):
        if (target, last_coin) in memo:
            return memo[(target, last_coin)]
        
        if target == 0:
            return 1
        if target < 0:
            return 0
        
        ways = 0
        for coin in coins:
            if coin >= last_coin:  # Ensure non-decreasing order
                ways += count_ways(target - coin, coin)
        
        memo[(target, last_coin)] = ways % MOD
        return memo[(target, last_coin)]
    
    return count_ways(x, 0)
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n*x) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n*x)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def coin_combinations_ii_dp(n, x, coins):
    MOD = 10**9 + 7
    
    # Sort coins to ensure non-decreasing order
    coins.sort()
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case: one way to make sum 0 (empty combination)
    
    # Process coins in order to avoid duplicates
    for coin in coins:
        for i in range(coin, x + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x]
```

**Why this improvement works**: We process coins in sorted order and build the solution iteratively. By processing each coin separately, we ensure that we don't count the same combination multiple times.

### Alternative: 2D DP Approach - O(n*x)
**Description**: Use a 2D DP approach to explicitly track coin usage.

```python
def coin_combinations_ii_2d_dp(n, x, coins):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to make sum i using coins up to index j
    dp = [[0] * n for _ in range(x + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(x + 1):
        for j in range(n):
            if i == 0:
                dp[i][j] = 1
            elif j == 0:
                if i % coins[0] == 0:
                    dp[i][j] = 1
            else:
                dp[i][j] = dp[i][j-1]  # Don't use current coin
                if i >= coins[j]:
                    dp[i][j] = (dp[i][j] + dp[i - coins[j]][j]) % MOD
    
    return dp[x][n-1]
```

**Why this works**: This approach explicitly tracks which coins are used, ensuring we don't count duplicates.

## Final Optimal Solution

```python
n, x = map(int, input().split())
coins = list(map(int, input().split()))
MOD = 10**9 + 7

# Sort coins to ensure non-decreasing order
coins.sort()

# dp[i] = number of ways to make sum i
dp = [0] * (x + 1)
dp[0] = 1  # Base case

# Process coins in order to avoid duplicates
for coin in coins:
    for i in range(coin, x + 1):
        dp[i] = (dp[i] + dp[i - coin]) % MOD

print(dp[x])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^x) | O(x) | Try all combinations |
| Memoization | O(n*x) | O(n*x) | Store subproblem results |
| Bottom-Up DP | O(n*x) | O(x) | Build solution iteratively |
| 2D DP | O(n*x) | O(n*x) | Explicit coin tracking |

## Key Insights for Other Problems

### 1. **Order vs Unordered Combinations**
**Principle**: Distinguish between problems where order matters and where it doesn't.
**Applicable to**:
- Counting problems
- Combination problems
- Permutation problems
- Algorithm design

**Example Problems**:
- Coin combinations (unordered)
- Path counting (ordered)
- Subset problems
- Combination problems

### 2. **Duplicate Avoidance in DP**
**Principle**: Use specific ordering or tracking to avoid counting duplicates.
**Applicable to**:
- Dynamic programming
- Counting problems
- Combination problems
- Algorithm design

**Example Problems**:
- Coin combinations
- Subset sum
- Combination problems
- Counting problems

### 3. **Coin Processing Order**
**Principle**: Process coins in a specific order to ensure unique combinations.
**Applicable to**:
- Coin problems
- Combination problems
- Dynamic programming
- Algorithm design

**Example Problems**:
- Coin change
- Combination problems
- Dynamic programming
- Algorithm design

### 4. **State Definition for Unordered Problems**
**Principle**: Define states that naturally avoid counting duplicates.
**Applicable to**:
- Dynamic programming
- Counting problems
- State machine problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- Counting problems
- State machine problems
- Algorithm design

## Notable Techniques

### 1. **Coin Processing Pattern**
```python
# Process coins in order to avoid duplicates
coins.sort()
for coin in coins:
    for i in range(coin, target + 1):
        dp[i] = (dp[i] + dp[i - coin]) % MOD
```

### 2. **State Definition Pattern**
```python
# Define DP state for unordered combinations
dp = [0] * (target + 1)
dp[0] = 1  # Base case
```

### 3. **Duplicate Avoidance Pattern**
```python
# Use ordering to avoid duplicates
for coin in sorted_coins:
    # Process coin in non-decreasing order
```

## Edge Cases to Remember

1. **x = 0**: Return 1 (empty combination)
2. **No coins available**: Return 0
3. **Single coin**: Handle efficiently
4. **Large x**: Use efficient DP approach
5. **Coin values larger than target**: Handle properly

## Problem-Solving Framework

1. **Identify unordered nature**: This is an unordered combination problem
2. **Define state**: dp[i] = number of ways to make sum i
3. **Process coins in order**: Sort coins and process sequentially
4. **Handle base case**: dp[0] = 1
5. **Use modular arithmetic**: Take modulo at each step

---

*This analysis shows how to efficiently solve unordered combination problems using dynamic programming.* 