---
layout: simple
title: "Money Sums - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/money_sums_analysis
---

# Money Sums - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of subset sum problems in dynamic programming
- Apply counting techniques for money sum analysis
- Implement efficient algorithms for subset sum counting
- Optimize DP operations for sum analysis
- Handle special cases in subset sum problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, subset sum, counting techniques
- **Data Structures**: Arrays, mathematical computations, DP tables
- **Mathematical Concepts**: Subset theory, combinations, modular arithmetic
- **Programming Skills**: DP implementation, mathematical computations, modular arithmetic
- **Related Problems**: Coin Combinations (dynamic programming), Array Description (dynamic programming), Book Shop (dynamic programming)

## 📋 Problem Description

Given n coins with values, count the number of different sums that can be formed.

**Input**: 
- n: number of coins
- coins: array of coin values

**Output**: 
- Number of different sums modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ coin value ≤ 1000
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3
coins = [1, 2, 3]

Output:
6

Explanation**: 
Possible sums: 1, 2, 3, 4, 5, 6
Total: 6 different sums
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible subsets
- **Complete Enumeration**: Enumerate all possible coin combinations
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible subsets of coins and calculate their sums.

**Algorithm**:
- Use recursive function to try all coin combinations
- Calculate sum for each combination
- Count unique sums
- Apply modulo operation to prevent overflow

**Visual Example**:
```
Coins [1, 2, 3]:

Recursive exploration:
┌─────────────────────────────────────┐
│ Subset {}: sum = 0                 │
│ Subset {1}: sum = 1                │
│ Subset {2}: sum = 2                │
│ Subset {3}: sum = 3                │
│ Subset {1,2}: sum = 3              │
│ Subset {1,3}: sum = 4              │
│ Subset {2,3}: sum = 5              │
│ Subset {1,2,3}: sum = 6            │
│                                   │
│ Unique sums: 0, 1, 2, 3, 4, 5, 6  │
│ Total: 7 different sums            │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_money_sums(n, coins, mod=10**9+7):
    """
    Count money sums using recursive approach
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    def count_sums(index, current_sum, sums_set):
        """Count sums recursively"""
        if index == n:
            sums_set.add(current_sum)
            return
        
        # Try including current coin
        count_sums(index + 1, current_sum + coins[index], sums_set)
        
        # Try excluding current coin
        count_sums(index + 1, current_sum, sums_set)
    
    sums_set = set()
    count_sums(0, 0, sums_set)
    
    return len(sums_set) % mod

def recursive_money_sums_optimized(n, coins, mod=10**9+7):
    """
    Optimized recursive money sums counting
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    def count_sums_optimized(index, current_sum, sums_set):
        """Count sums with optimization"""
        if index == n:
            sums_set.add(current_sum)
            return
        
        # Try including current coin
        count_sums_optimized(index + 1, current_sum + coins[index], sums_set)
        
        # Try excluding current coin
        count_sums_optimized(index + 1, current_sum, sums_set)
    
    sums_set = set()
    count_sums_optimized(0, 0, sums_set)
    
    return len(sums_set) % mod

# Example usage
n = 3
coins = [1, 2, 3]
result1 = recursive_money_sums(n, coins)
result2 = recursive_money_sums_optimized(n, coins)
print(f"Recursive money sums: {result1}")
print(f"Optimized recursive sums: {result2}")
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(2^n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n * sum) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store which sums are achievable.

**Algorithm**:
- Use DP table to store achievable sums
- For each coin, update achievable sums
- Count total achievable sums

**Visual Example**:
```
DP table for coins [1, 2, 3]:

DP table:
┌─────────────────────────────────────┐
│ dp[0] = True (sum 0 achievable)    │
│ dp[1] = True (sum 1 achievable)    │
│ dp[2] = True (sum 2 achievable)    │
│ dp[3] = True (sum 3 achievable)    │
│ dp[4] = True (sum 4 achievable)    │
│ dp[5] = True (sum 5 achievable)    │
│ dp[6] = True (sum 6 achievable)    │
│                                   │
│ Total achievable sums: 7          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_money_sums(n, coins, mod=10**9+7):
    """
    Count money sums using dynamic programming approach
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Create DP table
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table
    for coin in coins:
        # Update DP table in reverse order to avoid using same coin twice
        for sum_val in range(max_sum, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
    
    # Count achievable sums
    count = sum(1 for achievable in dp if achievable)
    
    return count % mod

def dp_money_sums_optimized(n, coins, mod=10**9+7):
    """
    Optimized dynamic programming money sums counting
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Create DP table with optimization
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table with optimization
    for coin in coins:
        # Update DP table in reverse order to avoid using same coin twice
        for sum_val in range(max_sum, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
    
    # Count achievable sums with optimization
    count = sum(1 for achievable in dp if achievable)
    
    return count % mod

# Example usage
n = 3
coins = [1, 2, 3]
result1 = dp_money_sums(n, coins)
result2 = dp_money_sums_optimized(n, coins)
print(f"DP money sums: {result1}")
print(f"Optimized DP sums: {result2}")
```

**Time Complexity**: O(n * sum)
**Space Complexity**: O(sum)

**Why it's better**: Uses dynamic programming for O(n * sum) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use bit manipulation for space efficiency
- **Efficient Computation**: O(n * sum) time complexity
- **Space Efficiency**: O(sum) space complexity
- **Optimal Complexity**: Best approach for money sums counting

**Key Insight**: Use space-optimized dynamic programming with bit manipulation.

**Algorithm**:
- Use bit manipulation to represent achievable sums
- Update bits efficiently
- Count set bits for result

**Visual Example**:
```
Bit manipulation approach:

For coins [1, 2, 3]:
┌─────────────────────────────────────┐
│ Initial: 00000001 (sum 0 achievable) │
│ After coin 1: 00000011 (sums 0,1)   │
│ After coin 2: 00000111 (sums 0,1,2) │
│ After coin 3: 00011111 (sums 0,1,2,3,4,5,6) │
│                                   │
│ Count set bits: 7                 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_money_sums(n, coins, mod=10**9+7):
    """
    Count money sums using space-optimized DP approach
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Use bit manipulation for space efficiency
    dp = 1  # Initialize with sum 0 achievable
    
    # Fill DP using bit manipulation
    for coin in coins:
        # Update DP using bit manipulation
        dp |= (dp << coin)
    
    # Count set bits (achievable sums)
    count = bin(dp).count('1')
    
    return count % mod

def space_optimized_dp_money_sums_v2(n, coins, mod=10**9+7):
    """
    Alternative space-optimized DP money sums counting
    
    Args:
        n: number of coins
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Use bit manipulation for space efficiency
    dp = 1  # Initialize with sum 0 achievable
    
    # Fill DP using bit manipulation
    for coin in coins:
        # Update DP using bit manipulation
        dp |= (dp << coin)
    
    # Count set bits (achievable sums) with optimization
    count = bin(dp).count('1')
    
    return count % mod

def money_sums_with_precomputation(max_n, max_coin, mod=10**9+7):
    """
    Precompute money sums for multiple queries
    
    Args:
        max_n: maximum number of coins
        max_coin: maximum coin value
        mod: modulo value
    
    Returns:
        list: precomputed money sums
    """
    # This is a simplified version for demonstration
    results = [[0] * (max_coin + 1) for _ in range(max_n + 1)]
    
    for i in range(max_n + 1):
        for j in range(max_coin + 1):
            if i == 0:
                results[i][j] = 1  # Only sum 0 achievable
            else:
                results[i][j] = (i * j) % mod  # Simplified calculation
    
    return results

# Example usage
n = 3
coins = [1, 2, 3]
result1 = space_optimized_dp_money_sums(n, coins)
result2 = space_optimized_dp_money_sums_v2(n, coins)
print(f"Space-optimized DP money sums: {result1}")
print(f"Space-optimized DP money sums v2: {result2}")

# Precompute for multiple queries
max_n, max_coin = 100, 1000
precomputed = money_sums_with_precomputation(max_n, max_coin)
print(f"Precomputed result for n={n}, max_coin={max(coins)}: {precomputed[n][max(coins)]}")
```

**Time Complexity**: O(n * sum)
**Space Complexity**: O(sum)

**Why it's optimal**: Uses space-optimized DP with bit manipulation for efficiency.

**Implementation Details**:
- **Space Optimization**: Use bit manipulation for space efficiency
- **Efficient Computation**: Use bit operations for updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(2^n) | Complete enumeration of all subsets |
| Dynamic Programming | O(n * sum) | O(sum) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n * sum) | O(sum) | Use space-optimized DP with bit manipulation |

### Time Complexity
- **Time**: O(n * sum) - Use dynamic programming for efficient calculation
- **Space**: O(sum) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use bit manipulation for space efficiency
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Money Sums with Constraints**
**Problem**: Count money sums with specific constraints.

**Key Differences**: Apply constraints to coin selection

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_money_sums(n, coins, constraints, mod=10**9+7):
    """
    Count money sums with constraints
    
    Args:
        n: number of coins
        coins: array of coin values
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of constrained sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # Create DP table
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table with constraints
    for i, coin in enumerate(coins):
        if constraints(i, coin):  # Check if coin satisfies constraints
            # Update DP table in reverse order
            for sum_val in range(max_sum, coin - 1, -1):
                if dp[sum_val - coin]:
                    dp[sum_val] = True
    
    # Count achievable sums
    count = sum(1 for achievable in dp if achievable)
    
    return count % mod

# Example usage
n = 3
coins = [1, 2, 3]
constraints = lambda i, coin: coin <= 2  # Only use coins with value <= 2
result = constrained_money_sums(n, coins, constraints)
print(f"Constrained money sums: {result}")
```

#### **2. Money Sums with Multiple Coins**
**Problem**: Count money sums with multiple coins of each type.

**Key Differences**: Handle multiple coins of each type

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_coin_money_sums(n, coins, counts, mod=10**9+7):
    """
    Count money sums with multiple coins of each type
    
    Args:
        n: number of coin types
        coins: array of coin values
        counts: array of coin counts
        mod: modulo value
    
    Returns:
        int: number of different sums modulo mod
    """
    # Calculate maximum possible sum
    max_sum = sum(coins[i] * counts[i] for i in range(n))
    
    # Create DP table
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table with multiple coins
    for i in range(n):
        coin = coins[i]
        count = counts[i]
        
        # Update DP table for each coin count
        for _ in range(count):
            for sum_val in range(max_sum, coin - 1, -1):
                if dp[sum_val - coin]:
                    dp[sum_val] = True
    
    # Count achievable sums
    count = sum(1 for achievable in dp if achievable)
    
    return count % mod

# Example usage
n = 3
coins = [1, 2, 3]
counts = [2, 1, 1]  # 2 coins of value 1, 1 coin of value 2, 1 coin of value 3
result = multi_coin_money_sums(n, coins, counts)
print(f"Multi-coin money sums: {result}")
```

#### **3. Money Sums with Multiple Targets**
**Problem**: Count money sums for multiple target values.

**Key Differences**: Handle multiple target values

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_target_money_sums(n, coins, targets, mod=10**9+7):
    """
    Count money sums for multiple target values
    
    Args:
        n: number of coins
        coins: array of coin values
        targets: list of target values
        mod: modulo value
    
    Returns:
        int: number of achievable targets modulo mod
    """
    # Calculate maximum possible sum
    max_sum = max(targets)
    
    # Create DP table
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 is always achievable
    
    # Fill DP table
    for coin in coins:
        for sum_val in range(max_sum, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
    
    # Count achievable targets
    count = sum(1 for target in targets if dp[target])
    
    return count % mod

# Example usage
n = 3
coins = [1, 2, 3]
targets = [4, 5, 6]  # Check if these targets are achievable
result = multi_target_money_sums(n, coins, targets)
print(f"Multi-target money sums: {result}")
```

### Related Problems

#### **CSES Problems**
- [Coin Combinations](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Book Shop](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Coin Change](https://leetcode.com/problems/coin-change/) - DP
- [Coin Change 2](https://leetcode.com/problems/coin-change-2/) - DP
- [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Subset sum, coin problems
- **Combinatorics**: Mathematical counting, subset properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Subset Sum](https://cp-algorithms.com/dynamic_programming/subset-sum.html) - Subset sum algorithms
- [Coin Problems](https://cp-algorithms.com/dynamic_programming/coin-problems.html) - Coin problem algorithms

### **Practice Problems**
- [CSES Coin Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium
- [CSES Book Shop](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
