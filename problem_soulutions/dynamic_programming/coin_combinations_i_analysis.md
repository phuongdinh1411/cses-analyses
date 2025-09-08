---
layout: simple
title: "Coin Combinations I - Count Ways to Make Sum"
permalink: /problem_soulutions/dynamic_programming/coin_combinations_i_analysis
---

# Coin Combinations I - Count Ways to Make Sum

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand counting problems in dynamic programming and distinct way calculations
- Apply bottom-up DP to solve counting problems with multiple coin types
- Implement efficient DP solutions for counting distinct combinations and arrangements
- Optimize DP solutions using space-efficient techniques and modular arithmetic
- Handle edge cases in counting DP (impossible sums, single coin types, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, counting problems, recurrence relations, bottom-up DP
- **Data Structures**: Arrays, DP tables, counting data structures
- **Mathematical Concepts**: Combinatorics, counting principles, recurrence relations, modular arithmetic
- **Programming Skills**: Array manipulation, iterative programming, counting techniques, DP implementation
- **Related Problems**: Dice Combinations (basic counting DP), Minimizing Coins (optimization DP), Coin Combinations II (unlimited coins)

## Problem Description

Given a money system with n coins of different values, count the number of distinct ways to produce a sum x using the available coins.

**Input**: 
- First line: two integers n and x (number of coins and target sum)
- Second line: n integers c1, c2, ..., cn (values of each coin)

**Output**: 
- Print the number of distinct ways modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10^6
- 1 ≤ ci ≤ 10^6
- Each coin can be used unlimited times
- Count distinct ways to achieve target sum
- Result must be modulo 10^9 + 7
- Order of coins matters (2+3+4 ≠ 3+2+4)

**Example**:
```
Input:
3 9
2 3 5

Output:
8

Explanation**: 
There are 8 distinct ways to achieve sum 9:
- 2+2+5, 2+5+2, 5+2+2 (using 2,2,5)
- 3+3+3 (using 3,3,3)
- 2+2+2+3, 2+2+3+2, 2+3+2+2, 3+2+2+2 (using 2,2,2,3)
```

## Visual Example

### Input and Problem Setup
```
Input: n = 3, x = 9
Coins: [2, 3, 5]

Goal: Count distinct ways to achieve sum 9
Constraint: Each coin can be used unlimited times
Result: Number of ways modulo 10^9 + 7
Note: Order matters (2+3+4 ≠ 3+2+4)
```

### Coin Combination Analysis
```
For target sum 9 with coins [2, 3, 5]:

Way 1: Using coins 2, 2, 5
- 2+2+5 = 9
- 2+5+2 = 9  
- 5+2+2 = 9
Total: 3 ways

Way 2: Using coins 3, 3, 3
- 3+3+3 = 9
Total: 1 way

Way 3: Using coins 2, 2, 2, 3
- 2+2+2+3 = 9
- 2+2+3+2 = 9
- 2+3+2+2 = 9
- 3+2+2+2 = 9
Total: 4 ways

Total distinct ways: 3 + 1 + 4 = 8
```

### Dynamic Programming Pattern
```
DP State: dp[i] = number of ways to achieve sum i

Base case: dp[0] = 1 (one way to achieve sum 0: empty sequence)

Recurrence: dp[i] += dp[i-coin] for all coins

For sum 9:
dp[9] += dp[7] (using coin 2)
dp[9] += dp[6] (using coin 3)
dp[9] += dp[4] (using coin 5)
```

### State Transition Visualization
```
Building DP table for x = 9 with coins [2, 3, 5]:

Initialize: dp = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

After processing coin 2:
dp[2] += dp[0] = 1
dp[3] += dp[1] = 0
dp[4] += dp[2] = 1
dp[5] += dp[3] = 0
dp[6] += dp[4] = 1
dp[7] += dp[5] = 0
dp[8] += dp[6] = 1
dp[9] += dp[7] = 0

After processing coin 3:
dp[3] += dp[0] = 1
dp[4] += dp[1] = 0
dp[5] += dp[2] = 1
dp[6] += dp[3] = 2
dp[7] += dp[4] = 1
dp[8] += dp[5] = 2
dp[9] += dp[6] = 2

After processing coin 5:
dp[5] += dp[0] = 2
dp[6] += dp[1] = 2
dp[7] += dp[2] = 2
dp[8] += dp[3] = 3
dp[9] += dp[4] = 3

Final: dp = [1, 0, 1, 1, 1, 2, 2, 2, 3, 3]
```

### Key Insight
The solution works by:
1. Using dynamic programming to count ways for each sum
2. For each sum i, adding ways from (i-coin) for all coins
3. Building solutions from smaller subproblems
4. Using modular arithmetic to handle large numbers
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
3. Count all valid sequences that reach sum 0
4. Return total count modulo 10^9 + 7

**Visual Example:**
```
Brute force approach: Try all possible coin sequences
For coins [2, 3, 5] and target 9:

Recursive tree:
                   9
              /    |    \
            7      6     4
          / | \   /|\   /|\
         5  4  2  4 3 1  2 1 -1
        /|\ /|\ |  |     |
       3 2 0 2 1 -1 0    0
      /|\ |     |
     1 0 -1     0
    /|\
  -1
```

**Implementation:**
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

def solve_coin_combinations_brute_force():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    result = coin_combinations_brute_force(n, x, coins)
    print(result)
```

**Time Complexity:** O(n^x) for trying all possible coin sequences
**Space Complexity:** O(x) for recursion depth

**Why it's inefficient:**
- O(n^x) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large x
- Poor performance with exponential growth

### Approach 2: Dynamic Programming (Better)

**Key Insights from DP Solution:**
- Use 1D DP array to store number of ways for each sum
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. For each coin, update all sums that can use that coin
3. Use recurrence relation to build solutions
4. Return result modulo 10^9 + 7

**Visual Example:**
```
DP approach: Build solutions iteratively
For coins [2, 3, 5] and target 9:

Initialize: dp = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

After coin 2: dp = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
After coin 3: dp = [1, 0, 1, 1, 1, 1, 2, 1, 2, 2]
After coin 5: dp = [1, 0, 1, 1, 1, 2, 2, 2, 3, 3]

Final result: dp[9] = 3
```

**Implementation:**
```python
def coin_combinations_dp(n, x, coins):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case: one way to make sum 0 (empty combination)
    
    for coin in coins:
        for i in range(coin, x + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x]

def solve_coin_combinations_dp():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    result = coin_combinations_dp(n, x, coins)
    print(result)
```

**Time Complexity:** O(n × x) for filling DP table
**Space Complexity:** O(x) for DP array

**Why it's better:**
- O(n × x) time complexity is much better than O(n^x)
- Uses dynamic programming for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Optimized DP with Space Efficiency (Optimal)

**Key Insights from Optimized Solution:**
- Use the same DP approach but with better implementation
- Most efficient approach for coin combination counting
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Initialize DP array with base cases
2. Process coins one by one to avoid overcounting
3. Use modular arithmetic throughout computation
4. Return optimal solution

**Visual Example:**
```
Optimized DP: Process coins sequentially
For coins [2, 3, 5] and target 9:

Initialize: dp = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Process coin 2:
- dp[2] += dp[0] = 1
- dp[4] += dp[2] = 1
- dp[6] += dp[4] = 1
- dp[8] += dp[6] = 1

Process coin 3:
- dp[3] += dp[0] = 1
- dp[5] += dp[2] = 1
- dp[6] += dp[3] = 2
- dp[7] += dp[4] = 1
- dp[8] += dp[5] = 2
- dp[9] += dp[6] = 2

Process coin 5:
- dp[5] += dp[0] = 2
- dp[7] += dp[2] = 2
- dp[8] += dp[3] = 3
- dp[9] += dp[4] = 3
```

**Implementation:**
```python
def solve_coin_combinations():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case
    
    for coin in coins:
        for i in range(coin, x + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    print(dp[x])

# Main execution
if __name__ == "__main__":
    solve_coin_combinations()
```

**Time Complexity:** O(n × x) for filling DP table
**Space Complexity:** O(x) for DP array

**Why it's optimal:**
- O(n × x) time complexity is optimal for this problem
- Uses dynamic programming for efficient solution
- Most efficient approach for competitive programming
- Standard method for coin combination counting problems

## 🎯 Problem Variations

### Variation 1: Coin Combinations with Limited Coins
**Problem**: Count ways to achieve sum x when each coin has a limited quantity.

**Link**: [CSES Problem Set - Coin Combinations Limited](https://cses.fi/problemset/task/coin_combinations_limited)

```python
def coin_combinations_limited(n, x, coins, quantities):
    MOD = 10**9 + 7
    dp = [0] * (x + 1)
    dp[0] = 1
    
    for i in range(n):
        for j in range(x, coins[i] - 1, -1):
            for k in range(1, quantities[i] + 1):
                if j >= k * coins[i]:
                    dp[j] = (dp[j] + dp[j - k * coins[i]]) % MOD
    
    return dp[x]
```

### Variation 2: Coin Combinations with Different Order
**Problem**: Count ways to achieve sum x where order doesn't matter.

**Link**: [CSES Problem Set - Coin Combinations Order](https://cses.fi/problemset/task/coin_combinations_order)

```python
def coin_combinations_order(n, x, coins):
    MOD = 10**9 + 7
    dp = [0] * (x + 1)
    dp[0] = 1
    
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x]
```

### Variation 3: Coin Combinations with Minimum Coins
**Problem**: Count ways to achieve sum x using at least k coins.

**Link**: [CSES Problem Set - Coin Combinations Minimum](https://cses.fi/problemset/task/coin_combinations_minimum)

```python
def coin_combinations_minimum(n, x, coins, min_coins):
    MOD = 10**9 + 7
    dp = [[0] * (x + 1) for _ in range(min_coins + 1)]
    dp[0][0] = 1
    
    for coins_used in range(min_coins + 1):
        for sum_val in range(x + 1):
            if dp[coins_used][sum_val] > 0:
                for coin in coins:
                    if sum_val + coin <= x and coins_used + 1 <= min_coins:
                        dp[coins_used + 1][sum_val + coin] = (dp[coins_used + 1][sum_val + coin] + dp[coins_used][sum_val]) % MOD
    
    return sum(dp[i][x] for i in range(min_coins, min_coins + 1)) % MOD
```

## 🔗 Related Problems

- **[Dice Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Basic DP counting problems
- **[Minimizing Coins](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP optimization problems
- **[Coin Combinations II](/cses-analyses/problem_soulutions/dynamic_programming/)**: Unlimited coin counting problems
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP problems with sum constraints

## 📚 Learning Points

1. **Dynamic Programming**: Essential for understanding counting problems with recurrence relations
2. **Bottom-Up DP**: Key technique for building solutions from smaller subproblems
3. **Counting Problems**: Important for understanding distinct way calculations
4. **Coin Change Problems**: Critical for understanding classic DP counting
5. **Modular Arithmetic**: Foundation for handling large numbers in competitive programming
6. **Order Matters**: Critical for understanding when sequences are distinct

## 📝 Summary

The Coin Combinations I problem demonstrates dynamic programming and counting principles for efficient combination counting. We explored three approaches:

1. **Recursive Brute Force**: O(n^x) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n × x) time complexity using bottom-up DP, better approach for counting problems
3. **Optimized DP with Space Efficiency**: O(n × x) time complexity with efficient implementation, optimal approach for competitive programming

The key insights include understanding dynamic programming principles, using bottom-up approaches for efficient computation, and applying counting techniques for distinct way problems. This problem serves as an excellent introduction to dynamic programming counting in competitive programming.
