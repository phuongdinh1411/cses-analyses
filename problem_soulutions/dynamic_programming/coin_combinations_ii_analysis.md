---
layout: simple
title: CSES Coin Combinations II - Problem Analysis
permalink: /problem_soulutions/dynamic_programming/coin_combinations_ii_analysis/
---

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Coin Combinations with Limited Supply**
**Problem**: Each coin can only be used a limited number of times.
```python
def coin_combinations_ii_limited_supply(n, x, coins, limits):
    # limits[i] = maximum times coin i can be used
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to make sum i using first j coins
    dp = [[0] * (n + 1) for _ in range(x + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(x + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i][j-1]  # Don't use coin j
            for k in range(1, limits[j-1] + 1):
                if i >= k * coins[j-1]:
                    dp[i][j] = (dp[i][j] + dp[i - k * coins[j-1]][j-1]) % MOD
    
    return dp[x][n]
```

#### **Variation 2: Coin Combinations with Minimum Coins**
**Problem**: Find combinations that use at least k coins.
```python
def coin_combinations_ii_minimum_coins(n, x, coins, min_coins):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to make sum i using exactly j coins
    dp = [[0] * (x + 1) for _ in range(x + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(x + 1):
        for j in range(x + 1):
            for coin in coins:
                if i >= coin and j > 0:
                    dp[i][j] = (dp[i][j] + dp[i - coin][j - 1]) % MOD
    
    # Sum all ways with at least min_coins
    result = 0
    for j in range(min_coins, x + 1):
        result = (result + dp[x][j]) % MOD
    
    return result
```

#### **Variation 3: Coin Combinations with Maximum Coins**
**Problem**: Find combinations that use at most k coins.
```python
def coin_combinations_ii_maximum_coins(n, x, coins, max_coins):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of ways to make sum i using exactly j coins
    dp = [[0] * (max_coins + 1) for _ in range(x + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(x + 1):
        for j in range(max_coins + 1):
            for coin in coins:
                if i >= coin and j > 0:
                    dp[i][j] = (dp[i][j] + dp[i - coin][j - 1]) % MOD
    
    # Sum all ways with at most max_coins
    result = 0
    for j in range(max_coins + 1):
        result = (result + dp[x][j]) % MOD
    
    return result
```

#### **Variation 4: Coin Combinations with Costs**
**Problem**: Each coin has a cost, find combinations with minimum total cost.
```python
def coin_combinations_ii_with_costs(n, x, coins, costs):
    # costs[i] = cost of using coin i
    
    # dp[i] = minimum cost to make sum i
    dp = [float('inf')] * (x + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, x + 1):
        for j, coin in enumerate(coins):
            if i >= coin:
                dp[i] = min(dp[i], costs[j] + dp[i - coin])
    
    return dp[x] if dp[x] != float('inf') else -1
```

#### **Variation 5: Coin Combinations with Probabilities**
**Problem**: Each coin has a probability of being used, find expected number of combinations.
```python
def coin_combinations_ii_with_probabilities(n, x, coins, probabilities):
    # probabilities[i] = probability of using coin i
    
    # dp[i] = expected number of ways to make sum i
    dp = [0.0] * (x + 1)
    dp[0] = 1.0  # Base case
    
    for i in range(1, x + 1):
        for j, coin in enumerate(coins):
            if i >= coin:
                dp[i] += dp[i - coin] * probabilities[j]
    
    return dp[x]
```

### 🔗 **Related Problems & Concepts**

#### **1. Knapsack Problems**
- **0/1 Knapsack**: Each item can be used at most once
- **Unbounded Knapsack**: Unlimited copies of each item
- **Fractional Knapsack**: Can take fractions of items
- **Multiple Knapsack**: Multiple knapsacks with constraints

#### **2. Dynamic Programming Patterns**
- **1D DP**: Single state variable (target sum)
- **2D DP**: Two state variables (target sum, additional constraint)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Counting Problems**
- **Combinatorial Counting**: Count valid combinations
- **Inclusion-Exclusion**: Count with constraints
- **Generating Functions**: Algebraic approach to counting
- **Burnside's Lemma**: Count orbits under group actions

#### **4. Optimization Problems**
- **Minimum Cost**: Find minimum cost solution
- **Maximum Value**: Find maximum value solution
- **Resource Allocation**: Optimal use of limited resources
- **Scheduling**: Optimal arrangement of tasks

#### **5. Algorithmic Techniques**
- **Greedy Algorithms**: Heuristic optimization
- **Branch and Bound**: Exact optimization
- **Dynamic Programming**: Optimal substructure
- **Linear Programming**: Mathematical optimization

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    result = coin_combinations_ii_dp(n, x, coins)
    print(result)
```

#### **2. Range Queries on Coin Combinations**
```python
def range_coin_combinations_ii_queries(n, coins, queries):
    # Precompute for all sums up to max_x
    max_x = max(query[1] for query in queries)
    dp = [0] * (max_x + 1)
    dp[0] = 1
    
    for i in range(1, max_x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    # Answer queries
    for l, r in queries:
        total = sum(dp[i] for i in range(l, r + 1)) % MOD
        print(total)
```

#### **3. Interactive Coin Combination Problems**
```python
def interactive_coin_combination_ii_game():
    n, x = map(int, input("Enter n and x: ").split())
    coins = list(map(int, input("Enter coins: ").split()))
    
    print(f"Coins: {coins}")
    print(f"Target sum: {x}")
    
    player_guess = int(input("Enter number of ways: "))
    actual_ways = coin_combinations_ii_dp(n, x, coins)
    
    if player_guess == actual_ways:
        print("Correct!")
    else:
        print(f"Wrong! Number of ways is {actual_ways}")
```

### 🧮 **Mathematical Extensions**

#### **1. Generating Functions**
- **Power Series**: Represent combinations as polynomial coefficients
- **Recurrence Relations**: Find closed-form solutions
- **Asymptotic Analysis**: Analyze behavior for large sums
- **Combinatorial Identities**: Prove mathematical relationships

#### **2. Advanced DP Techniques**
- **Digit DP**: Count combinations with specific properties
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split problems into subproblems
- **Persistent Data Structures**: Maintain combination history

#### **3. Combinatorial Analysis**
- **Partition Theory**: Mathematical study of partitions
- **Composition Theory**: Study of ordered partitions
- **Generating Functions**: Algebraic approach to counting
- **Asymptotic Analysis**: Behavior for large numbers

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Knapsack Algorithms**: 0/1, unbounded, fractional
- **Subset Sum**: Find subsets with given sum
- **Partition Problems**: Divide set into equal parts
- **Scheduling Algorithms**: Optimal task arrangement

#### **2. Mathematical Concepts**
- **Combinatorics**: Counting principles and techniques
- **Number Theory**: Properties of integers
- **Linear Algebra**: Matrix operations and transformations
- **Probability Theory**: Random processes and outcomes

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Modular Arithmetic**: Handling large numbers efficiently

---

*This analysis demonstrates the power of dynamic programming for unordered combination problems and shows various extensions and applications.* 