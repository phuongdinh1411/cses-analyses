---
layout: simple
title: "Coin Combinations II"
permalink: /problem_soulutions/dynamic_programming/coin_combinations_ii_analysis
---


# Coin Combinations II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the difference between ordered and unordered combinations in DP
- Apply DP techniques to count unordered combinations and avoid duplicate counting
- Implement efficient DP solutions for combination counting with order constraints
- Optimize DP solutions using space-efficient techniques and modular arithmetic
- Handle edge cases in combination DP (impossible sums, single coin types, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, combination counting, order constraints, bottom-up DP
- **Data Structures**: Arrays, DP tables, combination data structures
- **Mathematical Concepts**: Combinatorics, combination counting, order principles, modular arithmetic
- **Programming Skills**: Array manipulation, iterative programming, combination techniques, DP implementation
- **Related Problems**: Coin Combinations I (ordered combinations), Dice Combinations (basic counting DP), Minimizing Coins (optimization DP)

## Problem Description

Given a money system with n coins of different values, count the number of distinct unordered ways to produce a sum x using the available coins (order doesn't matter).

**Input**: 
- First line: two integers n and x (number of coins and target sum)
- Second line: n integers c1, c2, ..., cn (values of each coin)

**Output**: 
- Print the number of distinct unordered ways modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10^6
- 1 ≤ ci ≤ 10^6
- Each coin can be used unlimited times
- Count distinct unordered ways to achieve target sum
- Result must be modulo 10^9 + 7
- Order of coins doesn't matter (2+3+4 = 3+2+4)

**Example**:
```
Input:
3 9
2 3 5

Output:
3

Explanation**: 
There are 3 distinct unordered ways to achieve sum 9:
- 2+2+5
- 3+3+3
- 2+2+2+3
Note: The order of coins doesn't matter, so 2+2+5 and 5+2+2 are considered the same.
```

## Visual Example

### Input and Problem Setup
```
Input: n = 3, x = 9
Coins: [2, 3, 5]

Goal: Count distinct unordered ways to achieve sum 9
Constraint: Each coin can be used unlimited times
Result: Number of ways modulo 10^9 + 7
Note: Order doesn't matter (2+3+4 = 3+2+4)
```

### Coin Combination Analysis
```
For target sum 9 with coins [2, 3, 5]:

Way 1: Using coins 2, 2, 5
- 2+2+5 = 9
- 2+5+2 = 9 (same as above, order doesn't matter)
- 5+2+2 = 9 (same as above, order doesn't matter)
Total: 1 way (unordered)

Way 2: Using coins 3, 3, 3
- 3+3+3 = 9
Total: 1 way

Way 3: Using coins 2, 2, 2, 3
- 2+2+2+3 = 9
- 2+2+3+2 = 9 (same as above, order doesn't matter)
- 2+3+2+2 = 9 (same as above, order doesn't matter)
- 3+2+2+2 = 9 (same as above, order doesn't matter)
Total: 1 way (unordered)

Total distinct unordered ways: 1 + 1 + 1 = 3
```

### Dynamic Programming Pattern
```
DP State: dp[i] = number of ways to achieve sum i (unordered)

Base case: dp[0] = 1 (one way to achieve sum 0: empty sequence)

Recurrence: dp[i] += dp[i-coin] for all coins (processed in order)

Key insight: Process coins in sorted order to ensure non-decreasing sequences
```

### State Transition Visualization
```
Building DP table for x = 9 with coins [2, 3, 5] (sorted):

Initialize: dp = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

After processing coin 2:
dp[2] += dp[0] = 1
dp[4] += dp[2] = 1
dp[6] += dp[4] = 1
dp[8] += dp[6] = 1

After processing coin 3:
dp[3] += dp[0] = 1
dp[5] += dp[2] = 1
dp[6] += dp[3] = 2
dp[7] += dp[4] = 1
dp[8] += dp[5] = 2
dp[9] += dp[6] = 2

After processing coin 5:
dp[5] += dp[0] = 2
dp[7] += dp[2] = 2
dp[8] += dp[3] = 3
dp[9] += dp[4] = 3

Final: dp = [1, 0, 1, 1, 1, 2, 2, 2, 3, 3]
```

### Key Insight
The solution works by:
1. Using dynamic programming to count ways for each sum
2. Processing coins in sorted order to ensure non-decreasing sequences
3. For each sum i, adding ways from (i-coin) for all coins
4. Building solutions from smaller subproblems
5. Using modular arithmetic to handle large numbers
6. Time complexity: O(n × x) for filling DP table
7. Space complexity: O(x) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of coins
- Use recursive approach to explore all paths
- Ensure non-decreasing order to avoid duplicates
- Simple but computationally expensive approach

**Algorithm:**
1. For each target sum, try all possible coins
2. Recursively solve for remaining sum after using each coin
3. Ensure coins are used in non-decreasing order
4. Count all valid sequences that reach sum 0
5. Return total count modulo 10^9 + 7

**Visual Example:**
```
Brute force approach: Try all possible coin combinations
For coins [2, 3, 5] and target 9:

Recursive tree with non-decreasing constraint:
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

def solve_coin_combinations_ii_brute_force():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    result = coin_combinations_ii_brute_force(n, x, coins)
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
- Use 1D DP array to store number of ways for each sum
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. Process coins in sorted order to ensure non-decreasing sequences
3. For each coin, update all sums that can use that coin
4. Use recurrence relation to build solutions
5. Return result modulo 10^9 + 7

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
def coin_combinations_ii_dp(n, x, coins):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i (unordered)
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case: one way to make sum 0 (empty combination)
    
    # Sort coins to ensure non-decreasing order
    coins.sort()
    
    for coin in coins:
        for i in range(coin, x + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x]

def solve_coin_combinations_ii_dp():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    result = coin_combinations_ii_dp(n, x, coins)
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
- Most efficient approach for unordered coin combination counting
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Initialize DP array with base cases
2. Sort coins to ensure non-decreasing order
3. Process coins one by one to avoid overcounting
4. Use modular arithmetic throughout computation
5. Return optimal solution

**Visual Example:**
```
Optimized DP: Process coins sequentially in sorted order
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
def solve_coin_combinations_ii():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i (unordered)
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case
    
    # Sort coins to ensure non-decreasing order
    coins.sort()
    
    for coin in coins:
        for i in range(coin, x + 1):
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    print(dp[x])

# Main execution
if __name__ == "__main__":
    solve_coin_combinations_ii()
```

**Time Complexity:** O(n × x) for filling DP table
**Space Complexity:** O(x) for DP array

**Why it's optimal:**
- O(n × x) time complexity is optimal for this problem
- Uses dynamic programming for efficient solution
- Most efficient approach for competitive programming
- Standard method for unordered coin combination counting problems

## 🎯 Problem Variations

### Variation 1: Coin Combinations with Limited Coins
**Problem**: Count unordered ways to achieve sum x when each coin has a limited quantity.

**Link**: [CSES Problem Set - Coin Combinations Limited](https://cses.fi/problemset/task/coin_combinations_limited)

```python
def coin_combinations_ii_limited(n, x, coins, quantities):
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
**Problem**: Count unordered ways to achieve sum x with specific ordering constraints.

**Link**: [CSES Problem Set - Coin Combinations Order](https://cses.fi/problemset/task/coin_combinations_order)

```python
def coin_combinations_ii_order(n, x, coins):
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
**Problem**: Count unordered ways to achieve sum x using at least k coins.

**Link**: [CSES Problem Set - Coin Combinations Minimum](https://cses.fi/problemset/task/coin_combinations_minimum)

```python
def coin_combinations_ii_minimum(n, x, coins, min_coins):
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

- **[Coin Combinations I](/cses-analyses/problem_soulutions/dynamic_programming/)**: Ordered coin combination counting problems
- **[Dice Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Basic DP counting problems
- **[Minimizing Coins](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP optimization problems
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP problems with sum constraints

## 📚 Learning Points

1. **Dynamic Programming**: Essential for understanding unordered combination counting with recurrence relations
2. **Bottom-Up DP**: Key technique for building solutions from smaller subproblems
3. **Order Constraints**: Important for understanding when order matters vs. doesn't matter
4. **Coin Change Problems**: Critical for understanding classic DP counting variations
5. **Modular Arithmetic**: Foundation for handling large numbers in competitive programming
6. **Non-decreasing Sequences**: Critical for avoiding duplicate counting in unordered problems

## 📝 Summary

The Coin Combinations II problem demonstrates dynamic programming and unordered combination counting principles for efficient combination counting. We explored three approaches:

1. **Recursive Brute Force**: O(n^x) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n × x) time complexity using bottom-up DP, better approach for unordered counting problems
3. **Optimized DP with Space Efficiency**: O(n × x) time complexity with efficient implementation, optimal approach for competitive programming

The key insights include understanding dynamic programming principles, using bottom-up approaches for efficient computation, and applying unordered counting techniques for distinct way problems. This problem serves as an excellent introduction to dynamic programming unordered counting in competitive programming.
