---
layout: simple
title: "Minimizing Coins - Minimum Coins to Make Sum"
permalink: /problem_soulutions/dynamic_programming/minimizing_coins_analysis
---

# Minimizing Coins - Minimum Coins to Make Sum

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand optimization problems in dynamic programming and minimum value calculations
- Apply bottom-up DP to solve optimization problems with recurrence relations
- Implement efficient DP solutions for finding minimum values and optimal solutions
- Optimize DP solutions using space-efficient techniques and handle impossible cases
- Handle edge cases in optimization DP (impossible sums, single coin solutions, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, optimization problems, recurrence relations, bottom-up DP
- **Data Structures**: Arrays, DP tables, optimization data structures
- **Mathematical Concepts**: Optimization, recurrence relations, minimum value problems, modular arithmetic
- **Programming Skills**: Array manipulation, iterative programming, optimization techniques, DP implementation
- **Related Problems**: Dice Combinations (basic DP), Coin Combinations I (counting DP), Money Sums (DP variations)

## Problem Description

Given a money system with n coins of different values, find the minimum number of coins needed to produce a sum x.

**Input**: 
- First line: integers n and x (number of coins and target sum)
- Second line: n integers c1, c2, ..., cn (values of each coin)

**Output**: 
- Print the minimum number of coins needed, or -1 if impossible

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10^6
- 1 ≤ ci ≤ 10^6
- Each coin can be used unlimited times
- Find minimum number of coins to achieve target sum
- Return -1 if target sum cannot be achieved

**Example**:
```
Input:
3 6
1 3 4

Output:
2

Explanation**: 
We can achieve sum 6 with:
- 1+1+4 (3 coins)
- 3+3 (2 coins) ← minimum
The answer is 2 coins.
```

## Visual Example

### Input and Problem Setup
```
Input: n = 3, x = 6
Coins: [1, 3, 4]

Goal: Find minimum number of coins to achieve sum 6
Constraint: Each coin can be used unlimited times
Result: Minimum coins needed or -1 if impossible
```

### Coin Combination Analysis
```
For target sum 6 with coins [1, 3, 4]:

Option 1: Using coin 1
- 1+1+1+1+1+1 = 6 (6 coins)

Option 2: Using coin 3
- 3+3 = 6 (2 coins) ← minimum

Option 3: Using coin 4
- 4+1+1 = 6 (3 coins)

Option 4: Mixed combinations
- 1+1+4 = 6 (3 coins)
- 3+1+1+1 = 6 (4 coins)

Minimum: 2 coins (using two coin 3s)
```

### Dynamic Programming Pattern
```
DP State: dp[i] = minimum coins needed for sum i

Base case: dp[0] = 0 (0 coins needed for sum 0)

Recurrence: dp[i] = min(dp[i], 1 + dp[i-coin]) for all coins

For sum 6:
dp[6] = min(dp[6], 1 + dp[5])  // using coin 1
dp[6] = min(dp[6], 1 + dp[3])  // using coin 3
dp[6] = min(dp[6], 1 + dp[2])  // using coin 4
```

### State Transition Visualization
```
Building DP table for x = 6 with coins [1, 3, 4]:

dp[0] = 0 (base case)
dp[1] = min(∞, 1 + dp[0]) = 1 (using coin 1)
dp[2] = min(∞, 1 + dp[1]) = 2 (using coin 1)
dp[3] = min(∞, 1 + dp[2], 1 + dp[0]) = 1 (using coin 3)
dp[4] = min(∞, 1 + dp[3], 1 + dp[1], 1 + dp[0]) = 1 (using coin 4)
dp[5] = min(∞, 1 + dp[4], 1 + dp[2], 1 + dp[1]) = 2 (using coin 4 + coin 1)
dp[6] = min(∞, 1 + dp[5], 1 + dp[3], 1 + dp[2]) = 2 (using coin 3 + coin 3)
```

### Key Insight
The solution works by:
1. Using dynamic programming to find minimum coins for each sum
2. For each sum i, trying all possible coins and taking minimum
3. Building solutions from smaller subproblems
4. Handling impossible cases by returning -1
5. Time complexity: O(n × x) for filling DP table
6. Space complexity: O(x) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of coins
- Use recursive approach to explore all paths
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. For each target sum, try all possible coins
2. Recursively solve for remaining sum after using each coin
3. Keep track of minimum coins found
4. Return minimum or -1 if impossible

**Visual Example:**
```
Brute force approach: Try all possible coin combinations
For coins [1, 3, 4] and target 6:

Recursive tree:
                   6
              /    |    \
            5      3     2
          / | \   /|\   /|\
         4  2  1  2 0 -1 1 0 -1
        /|\ /|\ |  |     |
       3 1 0 1 0 -1 0    0
      /|\ |     |
     2 0 -1     0
    /|\
   1 0 -1
  /|\
 0 -1
```

**Implementation:**
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

def solve_minimizing_coins_brute_force():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    result = minimizing_coins_brute_force(n, x, coins)
    print(result)
```

**Time Complexity:** O(n^x) for trying all possible coin combinations
**Space Complexity:** O(x) for recursion depth

**Why it's inefficient:**
- O(n^x) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large x
- Poor performance with exponential growth

### Approach 2: Dynamic Programming (Better)

**Key Insights from DP Solution:**
- Use 1D DP array to store minimum coins for each sum
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. For each sum, try all possible coins
3. Update minimum coins needed using recurrence relation
4. Return optimal solution or -1 if impossible

**Visual Example:**
```
DP approach: Build solutions iteratively
For coins [1, 3, 4] and target 6:

Initialize: dp = [0, ∞, ∞, ∞, ∞, ∞, ∞]

i = 1: dp[1] = min(∞, 1 + dp[0]) = 1
i = 2: dp[2] = min(∞, 1 + dp[1]) = 2
i = 3: dp[3] = min(∞, 1 + dp[2], 1 + dp[0]) = 1
i = 4: dp[4] = min(∞, 1 + dp[3], 1 + dp[1], 1 + dp[0]) = 1
i = 5: dp[5] = min(∞, 1 + dp[4], 1 + dp[2], 1 + dp[1]) = 2
i = 6: dp[6] = min(∞, 1 + dp[5], 1 + dp[3], 1 + dp[2]) = 2

Final: dp = [0, 1, 2, 1, 1, 2, 2]
```

**Implementation:**
```python
def minimizing_coins_dp(n, x, coins):
    # dp[i] = minimum coins needed for sum i
    dp = [float('inf')] * (x + 1)
    dp[0] = 0  # Base case: 0 coins needed for sum 0
    
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], 1 + dp[i - coin])
    
    return dp[x] if dp[x] != float('inf') else -1

def solve_minimizing_coins_dp():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    result = minimizing_coins_dp(n, x, coins)
    print(result)
```

**Time Complexity:** O(n × x) for filling DP table
**Space Complexity:** O(x) for DP array

**Why it's better:**
- O(n × x) time complexity is much better than O(n^x)
- Uses dynamic programming for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Optimized DP with Early Termination (Optimal)

**Key Insights from Optimized Solution:**
- Sort coins to enable early termination
- Most efficient approach for coin change problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Sort coins for better performance
2. Initialize DP array with base cases
3. For each sum, try coins in sorted order
4. Use early termination when coin value exceeds current sum
5. Return optimal solution or -1 if impossible

**Visual Example:**
```
Optimized DP: Use sorted coins with early termination
For coins [1, 3, 4] (sorted) and target 6:

Initialize: dp = [0, ∞, ∞, ∞, ∞, ∞, ∞]

i = 1: Try coin 1 → dp[1] = min(∞, 1 + dp[0]) = 1
i = 2: Try coin 1 → dp[2] = min(∞, 1 + dp[1]) = 2
i = 3: Try coin 1 → dp[3] = min(∞, 1 + dp[2]) = 3
       Try coin 3 → dp[3] = min(3, 1 + dp[0]) = 1
i = 4: Try coin 1 → dp[4] = min(∞, 1 + dp[3]) = 2
       Try coin 3 → dp[4] = min(2, 1 + dp[1]) = 2
       Try coin 4 → dp[4] = min(2, 1 + dp[0]) = 1
```

**Implementation:**
```python
def solve_minimizing_coins():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    # Sort coins for better performance
    coins.sort()
    
    # dp[i] = minimum coins needed for sum i
    dp = [float('inf')] * (x + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, x + 1):
        for coin in coins:
            if coin > i:
                break  # Early termination since coins are sorted
            dp[i] = min(dp[i], 1 + dp[i - coin])
    
    result = dp[x] if dp[x] != float('inf') else -1
    print(result)

# Main execution
if __name__ == "__main__":
    solve_minimizing_coins()
```

**Time Complexity:** O(n × x) for filling DP table with early termination
**Space Complexity:** O(x) for DP array

**Why it's optimal:**
- O(n × x) time complexity is optimal for this problem
- Uses early termination for better practical performance
- Most efficient approach for competitive programming
- Standard method for coin change optimization problems

## 🎯 Problem Variations

### Variation 1: Coin Change with Limited Coins
**Problem**: Find minimum coins needed when each coin has a limited quantity.

**Link**: [CSES Problem Set - Coin Change Limited](https://cses.fi/problemset/task/coin_change_limited)

```python
def coin_change_limited(n, x, coins, quantities):
    dp = [float('inf')] * (x + 1)
    dp[0] = 0
    
    for i in range(n):
        for j in range(x, coins[i] - 1, -1):
            for k in range(1, quantities[i] + 1):
                if j >= k * coins[i]:
                    dp[j] = min(dp[j], k + dp[j - k * coins[i]])
    
    return dp[x] if dp[x] != float('inf') else -1
```

### Variation 2: Coin Change with Different Denominations
**Problem**: Find minimum coins needed with coins of different denominations.

**Link**: [CSES Problem Set - Coin Change Denominations](https://cses.fi/problemset/task/coin_change_denominations)

```python
def coin_change_denominations(n, x, coins):
    dp = [float('inf')] * (x + 1)
    dp[0] = 0
    
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], 1 + dp[i - coin])
    
    return dp[x] if dp[x] != float('inf') else -1
```

### Variation 3: Coin Change with Maximum Coins
**Problem**: Find minimum coins needed with a maximum limit on total coins.

**Link**: [CSES Problem Set - Coin Change Maximum](https://cses.fi/problemset/task/coin_change_maximum)

```python
def coin_change_maximum(n, x, coins, max_coins):
    dp = [[float('inf')] * (x + 1) for _ in range(max_coins + 1)]
    dp[0][0] = 0
    
    for coins_used in range(max_coins + 1):
        for sum_val in range(x + 1):
            if dp[coins_used][sum_val] != float('inf'):
                for coin in coins:
                    if sum_val + coin <= x and coins_used + 1 <= max_coins:
                        dp[coins_used + 1][sum_val + coin] = min(
                            dp[coins_used + 1][sum_val + coin],
                            dp[coins_used][sum_val] + 1
                        )
    
    return min(dp[i][x] for i in range(max_coins + 1)) if any(dp[i][x] != float('inf') for i in range(max_coins + 1)) else -1
```

## 🔗 Related Problems

- **[Dice Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Basic DP counting problems
- **[Coin Combinations I](/cses-analyses/problem_soulutions/dynamic_programming/)**: Counting DP problems
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP problems with sum constraints
- **[Removing Digits](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP optimization problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for understanding optimization problems with recurrence relations
2. **Bottom-Up DP**: Key technique for building solutions from smaller subproblems
3. **Optimization Problems**: Important for understanding minimum value calculations
4. **Coin Change Problems**: Critical for understanding classic DP optimization
5. **Early Termination**: Foundation for optimizing DP solutions
6. **Impossible Cases**: Critical for handling edge cases in optimization problems

## 📝 Summary

The Minimizing Coins problem demonstrates dynamic programming and optimization concepts for efficient minimum value calculation. We explored three approaches:

1. **Recursive Brute Force**: O(n^x) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n × x) time complexity using bottom-up DP, better approach for optimization problems
3. **Optimized DP with Early Termination**: O(n × x) time complexity with early termination, optimal approach for competitive programming

The key insights include understanding dynamic programming principles, using bottom-up approaches for efficient computation, and applying optimization techniques for minimum value problems. This problem serves as an excellent introduction to dynamic programming optimization in competitive programming.
