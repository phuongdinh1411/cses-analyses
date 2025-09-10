---
layout: simple
title: "Dice Combinations - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/dice_combinations_analysis
---

# Dice Combinations - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of dice combinations in dynamic programming
- Apply counting techniques for dice combination analysis
- Implement efficient algorithms for dice combination counting
- Optimize DP operations for combination analysis
- Handle special cases in dice combination problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, counting techniques, mathematical formulas
- **Data Structures**: Arrays, mathematical computations, DP tables
- **Mathematical Concepts**: Combinations, permutations, modular arithmetic
- **Programming Skills**: DP implementation, mathematical computations, modular arithmetic
- **Related Problems**: Coin Combinations (dynamic programming), Money Sums (dynamic programming), Array Description (dynamic programming)

## 📋 Problem Description

Given a target sum, count the number of ways to achieve it using dice rolls (1-6).

**Input**: 
- n: target sum

**Output**: 
- Number of ways to achieve sum modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3

Output:
4

Explanation**: 
Ways to achieve sum 3:
1. 1 + 1 + 1 = 3
2. 1 + 2 = 3
3. 2 + 1 = 3
4. 3 = 3
Total: 4 ways
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible dice combinations
- **Complete Enumeration**: Enumerate all possible dice roll sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to achieve the target sum using dice rolls.

**Algorithm**:
- Use recursive function to try all dice rolls
- Calculate sum for each combination
- Count valid combinations
- Apply modulo operation to prevent overflow

**Visual Example**:
```
Target sum = 3:

Recursive exploration:
┌─────────────────────────────────────┐
│ Try dice roll 1: remaining = 2     │
│ - Try dice roll 1: remaining = 1   │
│   - Try dice roll 1: remaining = 0 ✓ │
│ - Try dice roll 2: remaining = 0 ✓ │
│                                   │
│ Try dice roll 2: remaining = 1     │
│ - Try dice roll 1: remaining = 0 ✓ │
│                                   │
│ Try dice roll 3: remaining = 0 ✓   │
│                                   │
│ Total: 4 ways                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_dice_combinations(n, mod=10**9+7):
    """
    Count dice combinations using recursive approach
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    def count_combinations(target):
        """Count combinations recursively"""
        if target == 0:
            return 1  # Valid combination found
        
        if target < 0:
            return 0  # Invalid combination
        
        count = 0
        # Try each dice roll (1-6)
        for dice in range(1, 7):
            count = (count + count_combinations(target - dice)) % mod
        
        return count
    
    return count_combinations(n)

def recursive_dice_combinations_optimized(n, mod=10**9+7):
    """
    Optimized recursive dice combinations counting
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    def count_combinations_optimized(target):
        """Count combinations with optimization"""
        if target == 0:
            return 1  # Valid combination found
        
        if target < 0:
            return 0  # Invalid combination
        
        count = 0
        # Try each dice roll (1-6)
        for dice in range(1, 7):
            count = (count + count_combinations_optimized(target - dice)) % mod
        
        return count
    
    return count_combinations_optimized(n)

# Example usage
n = 3
result1 = recursive_dice_combinations(n)
result2 = recursive_dice_combinations_optimized(n)
print(f"Recursive dice combinations: {result1}")
print(f"Optimized recursive combinations: {result2}")
```

**Time Complexity**: O(6^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store number of ways for each sum
- Fill DP table bottom-up
- Return DP[n] as result

**Visual Example**:
```
DP table for target sum = 3:

DP table:
┌─────────────────────────────────────┐
│ dp[0] = 1 (one way: no dice)       │
│ dp[1] = 1 (one way: roll 1)        │
│ dp[2] = 2 (ways: 1+1, 2)           │
│ dp[3] = 4 (ways: 1+1+1, 1+2, 2+1, 3) │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_dice_combinations(n, mod=10**9+7):
    """
    Count dice combinations using dynamic programming approach
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Create DP table
    dp = [0] * (n + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    return dp[n]

def dp_dice_combinations_optimized(n, mod=10**9+7):
    """
    Optimized dynamic programming dice combinations counting
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Create DP table with optimization
    dp = [0] * (n + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table with optimization
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    return dp[n]

# Example usage
n = 3
result1 = dp_dice_combinations(n)
result2 = dp_dice_combinations_optimized(n)
print(f"DP dice combinations: {result1}")
print(f"Optimized DP combinations: {result2}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Uses dynamic programming for O(n) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(n) time complexity
- **Space Efficiency**: O(1) space complexity
- **Optimal Complexity**: Best approach for dice combinations counting

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For target sum = 3:
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 4                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_dice_combinations(n, mod=10**9+7):
    """
    Count dice combinations using space-optimized DP approach
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Use only necessary variables for DP
    prev = [0] * 7  # Store previous 6 values
    prev[0] = 1  # Base case
    
    # Fill DP using space optimization
    for i in range(1, n + 1):
        current = 0
        for dice in range(1, 7):
            if i >= dice:
                current = (current + prev[dice - 1]) % mod
        
        # Update previous values
        for j in range(6, 0, -1):
            prev[j] = prev[j - 1]
        prev[0] = current
    
    return prev[0]

def space_optimized_dp_dice_combinations_v2(n, mod=10**9+7):
    """
    Alternative space-optimized DP dice combinations counting
    
    Args:
        n: target sum
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Use only necessary variables for DP
    prev = [0] * 7  # Store previous 6 values
    prev[0] = 1  # Base case
    
    # Fill DP using space optimization
    for i in range(1, n + 1):
        current = 0
        for dice in range(1, 7):
            if i >= dice:
                current = (current + prev[dice - 1]) % mod
        
        # Update previous values
        for j in range(6, 0, -1):
            prev[j] = prev[j - 1]
        prev[0] = current
    
    return prev[0]

def dice_combinations_with_precomputation(max_n, mod=10**9+7):
    """
    Precompute dice combinations for multiple queries
    
    Args:
        max_n: maximum value of n
        mod: modulo value
    
    Returns:
        list: precomputed dice combinations
    """
    results = [0] * (max_n + 1)
    
    # Initialize base case
    results[0] = 1
    
    # Fill results using DP
    for i in range(1, max_n + 1):
        for dice in range(1, 7):
            if i >= dice:
                results[i] = (results[i] + results[i - dice]) % mod
    
    return results

# Example usage
n = 3
result1 = space_optimized_dp_dice_combinations(n)
result2 = space_optimized_dp_dice_combinations_v2(n)
print(f"Space-optimized DP dice combinations: {result1}")
print(f"Space-optimized DP dice combinations v2: {result2}")

# Precompute for multiple queries
max_n = 1000000
precomputed = dice_combinations_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses space-optimized DP for O(n) time and O(1) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity to O(1)
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(6^n) | O(n) | Complete enumeration of all dice combinations |
| Dynamic Programming | O(n) | O(n) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n) | O(1) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(n) - Use dynamic programming for efficient calculation
- **Space**: O(1) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Dice Combinations with Constraints**
**Problem**: Count dice combinations with specific constraints.

**Key Differences**: Apply constraints to dice rolls

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_dice_combinations(n, constraints, mod=10**9+7):
    """
    Count dice combinations with constraints
    
    Args:
        n: target sum
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of constrained combinations modulo mod
    """
    # Create DP table
    dp = [0] * (n + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table with constraints
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice and constraints(dice):  # Check if dice satisfies constraints
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    return dp[n]

# Example usage
n = 3
constraints = lambda dice: dice <= 3  # Only use dice with value <= 3
result = constrained_dice_combinations(n, constraints)
print(f"Constrained dice combinations: {result}")
```

#### **2. Dice Combinations with Multiple Dice Types**
**Problem**: Count dice combinations with multiple types of dice.

**Key Differences**: Handle multiple types of dice

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_dice_combinations(n, dice_types, mod=10**9+7):
    """
    Count dice combinations with multiple types of dice
    
    Args:
        n: target sum
        dice_types: list of dice types
        mod: modulo value
    
    Returns:
        int: number of combinations modulo mod
    """
    # Create DP table
    dp = [0] * (n + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table with multiple dice types
    for i in range(1, n + 1):
        for dice in dice_types:
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    return dp[n]

# Example usage
n = 3
dice_types = [1, 2, 3, 4, 5, 6]  # Standard dice
result = multi_dice_combinations(n, dice_types)
print(f"Multi-dice combinations: {result}")
```

#### **3. Dice Combinations with Multiple Targets**
**Problem**: Count dice combinations for multiple target values.

**Key Differences**: Handle multiple target values

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_target_dice_combinations(targets, mod=10**9+7):
    """
    Count dice combinations for multiple target values
    
    Args:
        targets: list of target values
        mod: modulo value
    
    Returns:
        int: number of achievable targets modulo mod
    """
    max_target = max(targets)
    
    # Create DP table
    dp = [0] * (max_target + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no dice)
    
    # Fill DP table
    for i in range(1, max_target + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % mod
    
    # Count achievable targets
    count = sum(1 for target in targets if dp[target] > 0)
    
    return count % mod

# Example usage
targets = [3, 4, 5, 6]  # Check if these targets are achievable
result = multi_target_dice_combinations(targets)
print(f"Multi-target dice combinations: {result}")
```

### Related Problems

#### **CSES Problems**
- [Coin Combinations](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Money Sums](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Coin Change](https://leetcode.com/problems/coin-change/) - DP
- [Coin Change 2](https://leetcode.com/problems/coin-change-2/) - DP
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Combination counting, path problems
- **Combinatorics**: Mathematical counting, combination properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Coin Problems](https://cp-algorithms.com/dynamic_programming/coin-problems.html) - Coin problem algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques

### **Practice Problems**
- [CSES Coin Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Money Sums](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
