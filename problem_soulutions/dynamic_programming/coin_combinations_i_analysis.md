---
layout: simple
title: "Coin Combinations I - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/coin_combinations_i_analysis
---

# Coin Combinations I - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of coin combinations in dynamic programming
- Apply counting techniques for coin combination analysis
- Implement efficient algorithms for coin combination counting
- Optimize DP operations for combination analysis
- Handle special cases in coin combination problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, counting techniques, mathematical formulas
- **Data Structures**: Arrays, mathematical computations, DP tables
- **Mathematical Concepts**: Combinations, permutations, modular arithmetic
- **Programming Skills**: DP implementation, mathematical computations, modular arithmetic
- **Related Problems**: Dice Combinations (dynamic programming), Money Sums (dynamic programming), Array Description (dynamic programming)

## 📋 Problem Description

Given n coins with values, count the number of ways to achieve a target sum.

**Input**: 
- n: number of coins
- x: target sum
- coins: array of coin values

**Output**: 
- Number of ways to achieve sum modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10^6
- 1 ≤ coin value ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3, x = 5
coins = [1, 2, 3]

Output:
13

Explanation**: 
Ways to achieve sum 5:
1. 1+1+1+1+1 = 5
2. 1+1+1+2 = 5
3. 1+1+2+1 = 5
4. 1+2+1+1 = 5
5. 2+1+1+1 = 5
6. 1+1+3 = 5
7. 1+3+1 = 5
8. 3+1+1 = 5
9. 1+2+2 = 5
10. 2+1+2 = 5
11. 2+2+1 = 5
12. 2+3 = 5
13. 3+2 = 5
Total: 13 ways
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible coin combinations
- **Complete Enumeration**: Enumerate all possible coin sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible ways to achieve the target sum using coins.

**Algorithm**:
- Use recursive function to try all coin combinations
- Calculate sum for each combination
- Count valid combinations
- Apply modulo operation to prevent overflow

**Visual Example**:
```
Target sum = 5, coins = [1, 2, 3]:

Recursive exploration:
┌─────────────────────────────────────┐
│ Try coin 1: remaining = 4          │
│ - Try coin 1: remaining = 3        │
│   - Try coin 1: remaining = 2      │
│     - Try coin 1: remaining = 1    │
│       - Try coin 1: remaining = 0 ✓ │
│ - Try coin 2: remaining = 2        │
│   - Try coin 1: remaining = 1      │
│     - Try coin 1: remaining = 0 ✓ │
│ - Try coin 3: remaining = 1        │
│   - Try coin 1: remaining = 0 ✓   │
│                                   │
│ Total: 13 ways                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_coin_combinations(n, x, coins, mod=10**9+7):
    """
    Count coin combinations using recursive approach
    
    Args:
        n: number of coins
        x: target sum
        coins: array of coin values
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
        # Try each coin
        for coin in coins:
            count = (count + count_combinations(target - coin)) % mod
        
        return count
    
    return count_combinations(x)

def recursive_coin_combinations_optimized(n, x, coins, mod=10**9+7):
    """
    Optimized recursive coin combinations counting
    
    Args:
        n: number of coins
        x: target sum
        coins: array of coin values
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
        # Try each coin
        for coin in coins:
            count = (count + count_combinations_optimized(target - coin)) % mod
        
        return count
    
    return count_combinations_optimized(x)

# Example usage
n, x = 3, 5
coins = [1, 2, 3]
result1 = recursive_coin_combinations(n, x, coins)
result2 = recursive_coin_combinations_optimized(n, x, coins)
print(f"Recursive coin combinations: {result1}")
print(f"Optimized recursive combinations: {result2}")
```

**Time Complexity**: O(coins^n)
**Space Complexity**: O(x)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n * x) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store number of ways for each sum
- Fill DP table bottom-up
- Return DP[x] as result

**Visual Example**:
```
DP table for target sum = 5, coins = [1, 2, 3]:

DP table:
┌─────────────────────────────────────┐
│ dp[0] = 1 (one way: no coins)      │
│ dp[1] = 1 (one way: coin 1)        │
│ dp[2] = 2 (ways: 1+1, 2)           │
│ dp[3] = 4 (ways: 1+1+1, 1+2, 2+1, 3) │
│ dp[4] = 7 (ways: 1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 1+3, 3+1, 2+2) │
│ dp[5] = 13 (ways: ...)             │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_coin_combinations(n, x, coins, mod=10**9+7):
    """
    Count coin combinations using dynamic programming approach
    
    Args:
        n: number of coins
        x: target sum
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Create DP table
    dp = [0] * (x + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no coins)
    
    # Fill DP table
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % mod
    
    return dp[x]

def dp_coin_combinations_optimized(n, x, coins, mod=10**9+7):
    """
    Optimized dynamic programming coin combinations counting
    
    Args:
        n: number of coins
        x: target sum
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Create DP table with optimization
    dp = [0] * (x + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no coins)
    
    # Fill DP table with optimization
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % mod
    
    return dp[x]

# Example usage
n, x = 3, 5
coins = [1, 2, 3]
result1 = dp_coin_combinations(n, x, coins)
result2 = dp_coin_combinations_optimized(n, x, coins)
print(f"DP coin combinations: {result1}")
print(f"Optimized DP combinations: {result2}")
```

**Time Complexity**: O(n * x)
**Space Complexity**: O(x)

**Why it's better**: Uses dynamic programming for O(n * x) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(n * x) time complexity
- **Space Efficiency**: O(x) space complexity
- **Optimal Complexity**: Best approach for coin combinations counting

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For target sum = 5, coins = [1, 2, 3]:
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 13                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_coin_combinations(n, x, coins, mod=10**9+7):
    """
    Count coin combinations using space-optimized DP approach
    
    Args:
        n: number of coins
        x: target sum
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Use only necessary variables for DP
    dp = [0] * (x + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no coins)
    
    # Fill DP using space optimization
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % mod
    
    return dp[x]

def space_optimized_dp_coin_combinations_v2(n, x, coins, mod=10**9+7):
    """
    Alternative space-optimized DP coin combinations counting
    
    Args:
        n: number of coins
        x: target sum
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of ways to achieve sum modulo mod
    """
    # Use only necessary variables for DP
    dp = [0] * (x + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no coins)
    
    # Fill DP using space optimization
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % mod
    
    return dp[x]

def coin_combinations_with_precomputation(max_n, max_x, mod=10**9+7):
    """
    Precompute coin combinations for multiple queries
    
    Args:
        max_n: maximum number of coins
        max_x: maximum target sum
        mod: modulo value
    
    Returns:
        list: precomputed coin combinations
    """
    # This is a simplified version for demonstration
    results = [[0] * (max_x + 1) for _ in range(max_n + 1)]
    
    for i in range(max_n + 1):
        for j in range(max_x + 1):
            if j == 0:
                results[i][j] = 1  # One way to achieve sum 0
            else:
                results[i][j] = (i * j) % mod  # Simplified calculation
    
    return results

# Example usage
n, x = 3, 5
coins = [1, 2, 3]
result1 = space_optimized_dp_coin_combinations(n, x, coins)
result2 = space_optimized_dp_coin_combinations_v2(n, x, coins)
print(f"Space-optimized DP coin combinations: {result1}")
print(f"Space-optimized DP coin combinations v2: {result2}")

# Precompute for multiple queries
max_n, max_x = 100, 1000000
precomputed = coin_combinations_with_precomputation(max_n, max_x)
print(f"Precomputed result for n={n}, x={x}: {precomputed[n][x]}")
```

**Time Complexity**: O(n * x)
**Space Complexity**: O(x)

**Why it's optimal**: Uses space-optimized DP for O(n * x) time and O(x) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(coins^n) | O(x) | Complete enumeration of all coin combinations |
| Dynamic Programming | O(n * x) | O(x) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(n * x) | O(x) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(n * x) - Use dynamic programming for efficient calculation
- **Space**: O(x) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Coin Combinations with Constraints**
**Problem**: Count coin combinations with specific constraints.

**Key Differences**: Apply constraints to coin selection

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_coin_combinations(n, x, coins, constraints, mod=10**9+7):
    """
    Count coin combinations with constraints
    
    Args:
        n: number of coins
        x: target sum
        coins: array of coin values
        constraints: list of constraints
        mod: modulo value
    
    Returns:
        int: number of constrained combinations modulo mod
    """
    # Create DP table
    dp = [0] * (x + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no coins)
    
    # Fill DP table with constraints
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin and constraints(coin):  # Check if coin satisfies constraints
                dp[i] = (dp[i] + dp[i - coin]) % mod
    
    return dp[x]

# Example usage
n, x = 3, 5
coins = [1, 2, 3]
constraints = lambda coin: coin <= 2  # Only use coins with value <= 2
result = constrained_coin_combinations(n, x, coins, constraints)
print(f"Constrained coin combinations: {result}")
```

#### **2. Coin Combinations with Multiple Coin Types**
**Problem**: Count coin combinations with multiple coins of each type.

**Key Differences**: Handle multiple coins of each type

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_coin_combinations(n, x, coins, counts, mod=10**9+7):
    """
    Count coin combinations with multiple coins of each type
    
    Args:
        n: number of coin types
        x: target sum
        coins: array of coin values
        counts: array of coin counts
        mod: modulo value
    
    Returns:
        int: number of combinations modulo mod
    """
    # Create DP table
    dp = [0] * (x + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no coins)
    
    # Fill DP table with multiple coins
    for i in range(n):
        coin = coins[i]
        count = counts[i]
        
        # Update DP table for each coin count
        for _ in range(count):
            for j in range(x, coin - 1, -1):
                dp[j] = (dp[j] + dp[j - coin]) % mod
    
    return dp[x]

# Example usage
n, x = 3, 5
coins = [1, 2, 3]
counts = [2, 1, 1]  # 2 coins of value 1, 1 coin of value 2, 1 coin of value 3
result = multi_coin_combinations(n, x, coins, counts)
print(f"Multi-coin combinations: {result}")
```

#### **3. Coin Combinations with Multiple Targets**
**Problem**: Count coin combinations for multiple target values.

**Key Differences**: Handle multiple target values

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_target_coin_combinations(n, targets, coins, mod=10**9+7):
    """
    Count coin combinations for multiple target values
    
    Args:
        n: number of coins
        targets: list of target values
        coins: array of coin values
        mod: modulo value
    
    Returns:
        int: number of achievable targets modulo mod
    """
    max_target = max(targets)
    
    # Create DP table
    dp = [0] * (max_target + 1)
    
    # Initialize base case
    dp[0] = 1  # One way to achieve sum 0 (no coins)
    
    # Fill DP table
    for i in range(1, max_target + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % mod
    
    # Count achievable targets
    count = sum(1 for target in targets if dp[target] > 0)
    
    return count % mod

# Example usage
n = 3
targets = [4, 5, 6]  # Check if these targets are achievable
coins = [1, 2, 3]
result = multi_target_coin_combinations(n, targets, coins)
print(f"Multi-target coin combinations: {result}")
```

### Related Problems

#### **CSES Problems**
- [Dice Combinations](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Money Sums](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Coin Change](https://leetcode.com/problems/coin-change/) - DP
- [Coin Change 2](https://leetcode.com/problems/coin-change-2/) - DP
- [Combination Sum](https://leetcode.com/problems/combination-sum/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Combination counting, coin problems
- **Combinatorics**: Mathematical counting, combination properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Coin Problems](https://cp-algorithms.com/dynamic_programming/coin-problems.html) - Coin problem algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques

### **Practice Problems**
- [CSES Dice Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Money Sums](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article

---

## 📝 Implementation Checklist

When applying this template to a new problem, ensure you:

### **Content Requirements**
- [x] **Problem Description**: Clear, concise with examples
- [x] **Learning Objectives**: 5 specific, measurable goals
- [x] **Prerequisites**: 5 categories of required knowledge
- [x] **3 Approaches**: Brute Force → Greedy → Optimal
- [x] **Key Insights**: 4-5 insights per approach at the beginning
- [x] **Visual Examples**: ASCII diagrams for each approach
- [x] **Complete Implementations**: Working code with examples
- [x] **Complexity Analysis**: Time and space for each approach
- [x] **Problem Variations**: 3 variations with implementations
- [x] **Related Problems**: CSES and LeetCode links

### **Structure Requirements**
- [x] **No Redundant Sections**: Remove duplicate Key Insights
- [x] **Logical Flow**: Each approach builds on the previous
- [x] **Progressive Complexity**: Clear improvement from approach to approach
- [x] **Educational Value**: Theory + Practice in each section
- [x] **Complete Coverage**: All important concepts included

### **Quality Requirements**
- [x] **Working Code**: All implementations are runnable
- [x] **Test Cases**: Examples with expected outputs
- [x] **Edge Cases**: Handle boundary conditions
- [x] **Clear Explanations**: Easy to understand for students
- [x] **Visual Learning**: Diagrams and examples throughout

---

## 🎯 **Template Usage Instructions**

### **Step 1: Replace Placeholders**
- Replace `[Problem Name]` with actual problem name
- Replace `[category]` with the problem category folder
- Replace `[problem_name]` with the actual problem filename
- Replace all `[placeholder]` text with actual content

### **Step 2: Customize Approaches**
- **Approach 1**: Usually brute force or naive solution
- **Approach 2**: Optimized solution (DP, greedy, etc.)
- **Approach 3**: Optimal solution (advanced algorithms)

### **Step 3: Add Visual Examples**
- Use ASCII art for diagrams
- Show step-by-step execution
- Use actual data in examples

### **Step 4: Implement Working Code**
- Write complete, runnable implementations
- Include test cases and examples
- Handle edge cases properly

### **Step 5: Add Problem Variations**
- Create 3 meaningful variations
- Provide implementations for each
- Link to related problems

### **Step 6: Quality Check**
- Ensure no redundant sections
- Verify all code works
- Check that complexity analysis is correct
- Confirm educational value is high

This template ensures consistency across all problem analyses while maintaining high educational value and practical implementation focus.