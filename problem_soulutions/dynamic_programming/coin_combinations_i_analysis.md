# CSES Coin Combinations I - Problem Analysis

## Problem Statement
Consider a money system consisting of n coins. Each coin has a positive integer value. Your task is to calculate the number of distinct ways you can produce a sum of money x using the available coins.

For example, if the coins are {2,3,5} and the desired sum is 9, there are 8 ways:
- 2+2+5
- 2+5+2
- 5+2+2
- 3+3+3
- 2+2+2+3
- 2+2+3+2
- 2+3+2+2
- 3+2+2+2

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
8
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(n^x)
**Description**: Try all possible combinations of coins recursively.

```python
def coin_combinations_brute_force(n, x, coins):
    MOD = 10**9 + 7
    
    def count_ways(target):
        if target == 0:
            return 1
        if target < 0:
            return 0
        
        ways = 0
        for coin in coins:
            ways += count_ways(target - coin)
        
        return ways % MOD
    
    return count_ways(x)
```

**Why this is inefficient**: We're trying all possible combinations of coins, which leads to exponential complexity. For each target, we try all coin values, leading to O(n^x) complexity.

### Improvement 1: Recursive with Memoization - O(n*x)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def coin_combinations_memoization(n, x, coins):
    MOD = 10**9 + 7
    memo = {}
    
    def count_ways(target):
        if target in memo:
            return memo[target]
        
        if target == 0:
            return 1
        if target < 0:
            return 0
        
        ways = 0
        for coin in coins:
            ways += count_ways(target - coin)
        
        memo[target] = ways % MOD
        return memo[target]
    
    return count_ways(x)
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n*x) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n*x)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def coin_combinations_dp(n, x, coins):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case: one way to make sum 0 (empty combination)
    
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x]
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each sum i, we consider all possible coins and add the ways to make sum (i-coin).

### Alternative: Optimized DP with Ordering - O(n*x)
**Description**: Use an optimized DP approach that considers coin ordering.

```python
def coin_combinations_optimized(n, x, coins):
    MOD = 10**9 + 7
    
    # Sort coins for potential optimization
    coins.sort()
    
    dp = [0] * (x + 1)
    dp[0] = 1
    
    for i in range(1, x + 1):
        for coin in coins:
            if coin > i:
                break  # Early termination since coins are sorted
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x]
```

**Why this works**: By sorting the coins, we can terminate early when a coin value exceeds the current target, potentially reducing the number of iterations.

## Final Optimal Solution

```python
n, x = map(int, input().split())
coins = list(map(int, input().split()))
MOD = 10**9 + 7

# dp[i] = number of ways to make sum i
dp = [0] * (x + 1)
dp[0] = 1  # Base case

for i in range(1, x + 1):
    for coin in coins:
        if i >= coin:
            dp[i] = (dp[i] + dp[i - coin]) % MOD

print(dp[x])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^x) | O(x) | Try all combinations |
| Memoization | O(n*x) | O(x) | Store subproblem results |
| Bottom-Up DP | O(n*x) | O(x) | Build solution iteratively |
| Optimized DP | O(n*x) | O(x) | Early termination with sorting |

## Key Insights for Other Problems

### 1. **Dynamic Programming for Counting**
**Principle**: Use DP to count the number of ways to achieve a target.
**Applicable to**:
- Counting problems
- Combination problems
- Path counting
- Optimization problems

**Example Problems**:
- Coin combinations
- Path counting
- Combination problems
- Counting problems

### 2. **Order Matters vs Order Doesn't Matter**
**Principle**: Distinguish between problems where order matters and where it doesn't.
**Applicable to**:
- Counting problems
- Combination problems
- Permutation problems
- Algorithm design

**Example Problems**:
- Coin combinations (order matters)
- Subset sum (order doesn't matter)
- Permutation problems
- Combination problems

### 3. **Modular Arithmetic in Counting**
**Principle**: Use modular arithmetic to handle large numbers in counting problems.
**Applicable to**:
- Large number problems
- Counting problems
- Modular arithmetic
- Algorithm optimization

**Example Problems**:
- Large number calculations
- Counting problems
- Modular arithmetic
- Algorithm optimization

### 4. **State Transition for Counting**
**Principle**: Define clear state transitions for counting problems in DP.
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

### 1. **DP State Definition Pattern**
```python
# Define DP state for counting
dp = [0] * (target + 1)
dp[0] = 1  # Base case
```

### 2. **State Transition Pattern**
```python
# Define state transitions for counting
for i in range(1, target + 1):
    for choice in choices:
        if i >= choice:
            dp[i] = (dp[i] + dp[i - choice]) % MOD
```

### 3. **Modular Arithmetic Pattern**
```python
# Use modular arithmetic for large numbers
MOD = 10**9 + 7
dp[i] = (dp[i] + dp[i - choice]) % MOD
```

## Edge Cases to Remember

1. **x = 0**: Return 1 (empty combination)
2. **No coins available**: Return 0
3. **Single coin**: Handle efficiently
4. **Large x**: Use efficient DP approach
5. **Coin values larger than target**: Handle properly

## Problem-Solving Framework

1. **Identify counting nature**: This is a counting problem with overlapping subproblems
2. **Define state**: dp[i] = number of ways to make sum i
3. **Define transitions**: dp[i] = sum of dp[i-coin] for all coins
4. **Handle base case**: dp[0] = 1
5. **Use modular arithmetic**: Take modulo at each step

---

*This analysis shows how to efficiently solve counting problems using dynamic programming.* 