---
layout: simple
title: "Dynamic Programming"
permalink: /cses-analyses/problem_soulutions/dynamic_programming/
---

# Dynamic Programming

Welcome to the Dynamic Programming section! This category focuses on optimization problems that can be solved by breaking them down into overlapping subproblems.

## Overview

Dynamic Programming problems help you master:
- **Optimal substructure** and overlapping subproblems
- **State definition** and transition functions
- **Memoization** and tabulation techniques
- **Space and time optimization** strategies

## Topics Covered

### 💰 **Coin & Money Problems**
- **Coin Combinations I** - Counting ways to make sum
- **Coin Combinations II** - Counting distinct combinations
- **Minimizing Coins** - Minimum coins to make sum
- **Money Sums** - All possible sums from coins
- **Two Sets II** - Partitioning with equal sums

### 📊 **Array & Sequence Problems**
- **Array Description** - Counting valid arrays with constraints
- **Increasing Subsequence** - Longest increasing subsequence
- **Longest Common Subsequence** - Classic LCS problem
- **Removing Digits** - Minimum digits to remove for divisibility

### 🎯 **Grid & Path Problems**
- **Grid Paths** - Counting paths in grid
- **Minimal Grid Path** - Minimum cost path
- **Rectangle Cutting** - Optimal rectangle partitioning

### 🎮 **Game Theory & Optimization**
- **Removal Game** - Optimal game strategy
- **Book Shop** - Knapsack with constraints
- **Counting Towers** - Combinatorial counting with DP

### 🔢 **Mathematical DP**
- **Dice Combinations** - Counting dice roll combinations
- **Edit Distance** - String similarity measurement

## Learning Path

### 🟢 **Beginner Level** (Start Here)
1. **Dice Combinations** - Basic DP with simple transitions
2. **Coin Combinations I** - Classic counting DP
3. **Grid Paths** - 2D DP with simple state
4. **Minimizing Coins** - Greedy vs DP approach

### 🟡 **Intermediate Level**
1. **Coin Combinations II** - Avoiding duplicate counting
2. **Increasing Subsequence** - 1D DP with binary search
3. **Money Sums** - Subset sum with DP
4. **Array Description** - Complex state transitions

### 🔴 **Advanced Level**
1. **Longest Common Subsequence** - Classic string DP
2. **Edit Distance** - String alignment problems
3. **Removal Game** - Game theory with DP
4. **Two Sets II** - Partitioning optimization

## Key Concepts

### 🧠 **DP Fundamentals**
- **Optimal substructure**: Solutions to subproblems are optimal
- **Overlapping subproblems**: Same subproblems solved multiple times
- **State definition**: What information to store for each subproblem
- **Transition function**: How to compute current state from previous states

### 💾 **Implementation Techniques**
- **Memoization**: Top-down approach with caching
- **Tabulation**: Bottom-up approach with iteration
- **Space optimization**: Reducing memory usage
- **State compression**: Using bitmasks for small states

### 🎯 **Problem-Solving Patterns**
- **Prefix sums** for range queries
- **Sliding window** for subarray problems
- **Binary search** within DP
- **Greedy choices** in DP transitions

## Algorithmic Techniques

### 💰 **Coin Change Problems**
```python
# Coin Combinations I - Counting ways
def coin_combinations(coins, target):
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, target + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[target]

# Minimizing Coins - Minimum coins needed
def minimizing_coins(coins, target):
    dp = [float('inf')] * (target + 1)
    dp[0] = 0
    
    for i in range(1, target + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[target] if dp[target] != float('inf') else -1
```

### 📊 **Longest Increasing Subsequence**
```python
def longest_increasing_subsequence(arr):
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Optimized with binary search
def lis_optimized(arr):
    import bisect
    lis = []
    
    for num in arr:
        idx = bisect.bisect_left(lis, num)
        if idx == len(lis):
            lis.append(num)
        else:
            lis[idx] = num
    
    return len(lis)
```

### 🎮 **Game Theory DP**
```python
# Removal Game - Optimal strategy
def removal_game(arr):
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if i == j:
                dp[i][j] = arr[i]
            else:
                dp[i][j] = max(
                    arr[i] - dp[i + 1][j],
                    arr[j] - dp[i][j - 1]
                )
    
    total = sum(arr)
    return (total + dp[0][n - 1]) // 2
```

## Common DP Patterns

### 🔢 **1D DP**
- **State**: `dp[i]` represents solution for subproblem ending at index `i`
- **Transition**: `dp[i] = f(dp[j])` where `j < i`
- **Examples**: LIS, coin change, Fibonacci

### 📊 **2D DP**
- **State**: `dp[i][j]` represents solution for subproblem with two parameters
- **Transition**: `dp[i][j] = f(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`
- **Examples**: LCS, edit distance, grid paths

### 🎯 **State Compression**
- **Bitmask DP**: Use integers to represent sets
- **Rolling arrays**: Reuse arrays to save space
- **Coordinate compression**: Map large coordinates to small indices

## Tips for Success

1. **Identify DP**: Look for optimal substructure and overlapping subproblems
2. **Define State**: Clearly define what `dp[i]` represents
3. **Find Transitions**: Determine how to compute current state from previous states
4. **Handle Base Cases**: Initialize the DP array correctly
5. **Optimize Space**: Use rolling arrays or state compression when possible

## Related Topics

After mastering dynamic programming, explore:
- **Graph Algorithms** - Shortest paths and network flow
- **Range Queries** - Efficient query processing
- **Advanced Algorithms** - Complex optimization techniques
- **Competitive Programming** - Advanced problem-solving strategies

---

*Ready to master optimization? Start with the beginner problems and build your DP skills!* 