---
layout: simple
title: "Coin Combinations I"permalink: /problem_soulutions/dynamic_programming/coin_combinations_i_analysis
---


# Coin Combinations I

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Coin Combinations with Limited Supply**
**Problem**: Each coin can only be used a limited number of times.
```python
def coin_combinations_limited_supply(n, x, coins, limits):
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

#### **Variation 2: Coin Combinations with Order Constraint**
**Problem**: Coins must be used in non-decreasing order.
```python
def coin_combinations_ordered(n, x, coins):
    MOD = 10**9 + 7
    
    # Sort coins to ensure non-decreasing order
    coins.sort()
    
    # dp[i][j] = number of ways to make sum i using coins up to index j
    dp = [[0] * n for _ in range(x + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(x + 1):
        for j in range(n):
            if j > 0:
                dp[i][j] = dp[i][j-1]  # Don't use coin j
            if i >= coins[j]:
                dp[i][j] = (dp[i][j] + dp[i - coins[j]][j]) % MOD
    
    return dp[x][n-1]
```

#### **Variation 3: Coin Combinations with Minimum Coins**
**Problem**: Find combinations that use at least k coins.
```python
def coin_combinations_minimum_coins(n, x, coins, min_coins):
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

#### **Variation 4: Coin Combinations with Costs**
**Problem**: Each coin has a cost, find combinations with minimum total cost.
```python
def coin_combinations_with_costs(n, x, coins, costs):
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
def coin_combinations_with_probabilities(n, x, coins, probabilities):
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
    result = coin_combinations_dp(n, x, coins)
    print(result)
```

#### **2. Range Queries on Coin Combinations**
```python
def range_coin_combinations_queries(n, coins, queries):
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
def interactive_coin_combination_game():
    n, x = map(int, input("Enter n and x: ").split())
    coins = list(map(int, input("Enter coins: ").split()))
    
    print(f"Coins: {coins}")
    print(f"Target sum: {x}")
    
    player_guess = int(input("Enter number of ways: "))
    actual_ways = coin_combinations_dp(n, x, coins)
    
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

*This analysis demonstrates the power of dynamic programming for counting problems and shows various extensions and applications.* 