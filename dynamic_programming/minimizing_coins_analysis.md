# CSES Minimizing Coins - Problem Analysis

## Problem Statement
Consider a money system consisting of n coins. Each coin has a positive integer value. Your task is to produce a sum of money x using the available coins in such a way that the number of coins is minimal.

For example, if the coins are {1,3,4} and the desired sum is 6, there are two ways:
- 1+1+4 (3 coins)
- 3+3 (2 coins)

The answer is 2.

### Input
The first input line has two integers n and x: the number of coins and the desired sum of money.
The second line has n distinct integers c1,c2,…,cn: the value of each coin.

### Output
Print one integer: the minimum number of coins. If it is not possible to produce the desired sum, print −1.

### Constraints
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10^6
- 1 ≤ ci ≤ 10^6

### Example
```
Input:
3 6
1 3 4

Output:
2
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(n^x)
**Description**: Try all possible combinations of coins recursively.

```python
def minimizing_coins_brute_force(n, x, coins):
    def min_coins(target):
        if target == 0:
            return 0
        if target < 0:
            return float('inf')
        
        min_count = float('inf')
        for coin in coins:
            result = min_coins(target - coin)
            if result != float('inf'):
                min_count = min(min_count, 1 + result)
        
        return min_count
    
    result = min_coins(x)
    return result if result != float('inf') else -1
```

**Why this is inefficient**: We're trying all possible combinations of coins, which leads to exponential complexity. For each target, we try all coin values, leading to O(n^x) complexity.

### Improvement 1: Recursive with Memoization - O(n*x)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def minimizing_coins_memoization(n, x, coins):
    memo = {}
    
    def min_coins(target):
        if target in memo:
            return memo[target]
        
        if target == 0:
            return 0
        if target < 0:
            return float('inf')
        
        min_count = float('inf')
        for coin in coins:
            result = min_coins(target - coin)
            if result != float('inf'):
                min_count = min(min_count, 1 + result)
        
        memo[target] = min_count
        return memo[target]
    
    result = min_coins(x)
    return result if result != float('inf') else -1
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n*x) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n*x)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def minimizing_coins_dp(n, x, coins):
    # dp[i] = minimum number of coins needed for sum i
    dp = [float('inf')] * (x + 1)
    dp[0] = 0  # Base case: 0 coins needed for sum 0
    
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], 1 + dp[i - coin])
    
    return dp[x] if dp[x] != float('inf') else -1
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each sum i, we consider all possible coins and find the minimum number of coins needed.

### Alternative: Optimized DP with Early Termination - O(n*x)
**Description**: Use an optimized DP approach with early termination.

```python
def minimizing_coins_optimized(n, x, coins):
    # Sort coins for potential optimization
    coins.sort()
    
    dp = [float('inf')] * (x + 1)
    dp[0] = 0
    
    for i in range(1, x + 1):
        for coin in coins:
            if coin > i:
                break  # Early termination since coins are sorted
            dp[i] = min(dp[i], 1 + dp[i - coin])
    
    return dp[x] if dp[x] != float('inf') else -1
```

**Why this works**: By sorting the coins, we can terminate early when a coin value exceeds the current target, potentially reducing the number of iterations.

## Final Optimal Solution

```python
n, x = map(int, input().split())
coins = list(map(int, input().split()))

# dp[i] = minimum number of coins needed for sum i
dp = [float('inf')] * (x + 1)
dp[0] = 0  # Base case

for i in range(1, x + 1):
    for coin in coins:
        if i >= coin:
            dp[i] = min(dp[i], 1 + dp[i - coin])

result = dp[x]
print(result if result != float('inf') else -1)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^x) | O(x) | Try all combinations |
| Memoization | O(n*x) | O(x) | Store subproblem results |
| Bottom-Up DP | O(n*x) | O(x) | Build solution iteratively |
| Optimized DP | O(n*x) | O(x) | Early termination with sorting |

## Key Insights for Other Problems

### 1. **Dynamic Programming for Optimization**
**Principle**: Use DP to find optimal solutions for problems with overlapping subproblems.
**Applicable to**:
- Optimization problems
- Minimization problems
- Path finding
- Resource allocation

**Example Problems**:
- Coin change
- Shortest path
- Knapsack problem
- Optimization problems

### 2. **State Definition for DP**
**Principle**: Define clear states that capture the essential information for solving the problem.
**Applicable to**:
- Dynamic programming
- State machine problems
- Optimization problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- State machine problems
- Optimization problems
- Algorithm design

### 3. **Handling Impossible Cases**
**Principle**: Use special values (like infinity) to represent impossible cases in DP.
**Applicable to**:
- Dynamic programming
- Optimization problems
- Error handling
- Algorithm design

**Example Problems**:
- Dynamic programming
- Optimization problems
- Error handling
- Algorithm design

### 4. **Early Termination**
**Principle**: Use early termination techniques to optimize DP solutions.
**Applicable to**:
- Algorithm optimization
- Performance improvement
- Dynamic programming
- Search algorithms

**Example Problems**:
- Algorithm optimization
- Performance improvement
- Dynamic programming
- Search algorithms

## Notable Techniques

### 1. **DP State Definition Pattern**
```python
# Define DP state for optimization
dp = [float('inf')] * (target + 1)
dp[0] = 0  # Base case
```

### 2. **State Transition Pattern**
```python
# Define state transitions for minimization
for i in range(1, target + 1):
    for choice in choices:
        if i >= choice:
            dp[i] = min(dp[i], 1 + dp[i - choice])
```

### 3. **Impossible Case Handling**
```python
# Handle impossible cases
result = dp[target]
return result if result != float('inf') else -1
```

## Edge Cases to Remember

1. **x = 0**: Return 0 (no coins needed)
2. **No solution possible**: Return -1
3. **Single coin**: Handle efficiently
4. **Large x**: Use efficient DP approach
5. **Coin values larger than target**: Handle properly

## Problem-Solving Framework

1. **Identify optimization nature**: This is a minimization problem with overlapping subproblems
2. **Define state**: dp[i] = minimum coins needed for sum i
3. **Define transitions**: dp[i] = min(dp[i], 1 + dp[i-coin]) for all coins
4. **Handle base case**: dp[0] = 0
5. **Handle impossible cases**: Use infinity and check for -1

---

*This analysis shows how to efficiently solve optimization problems using dynamic programming.* 