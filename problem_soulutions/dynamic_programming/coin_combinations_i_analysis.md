---
layout: simple
title: "Coin Combinations I - Count Ways to Make Sum"
permalink: /problem_soulutions/dynamic_programming/coin_combinations_i_analysis
---

# Coin Combinations I - Count Ways to Make Sum

## 📋 Problem Description

Given a money system with n coins of different values, count the number of distinct ways to produce a sum x using the available coins.

This is a classic dynamic programming problem that requires counting the number of ways to make a target sum using available coins. The solution involves using bottom-up DP to build solutions from smaller subproblems.

**Input**: 
- n, x: number of coins and target sum
- c1, c2, ..., cn: values of each coin

**Output**: 
- Number of distinct ways modulo 10⁹+7

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10⁶
- 1 ≤ ci ≤ 10⁶

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

### 📊 Visual Example

**Input:**
```
Coins: [2, 3, 5]
Target Sum: 9
```

**All Possible Combinations:**
```
┌─────────────────────────────────────┐
│ Combination 1: 2+2+5 = 9           │
│ Order: 2+2+5, 2+5+2, 5+2+2        │
│ Count: 3 ways                      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Combination 2: 3+3+3 = 9           │
│ Order: 3+3+3                       │
│ Count: 1 way                       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Combination 3: 2+2+2+3 = 9         │
│ Order: 2+2+2+3, 2+2+3+2, 2+3+2+2, │
│        3+2+2+2                     │
│ Count: 4 ways                      │
└─────────────────────────────────────┘

Total: 3 + 1 + 4 = 8 ways
```

**Dynamic Programming Table:**
```
dp[i] = number of ways to make sum i

Coins: [2, 3, 5]
Target: 9

┌─────────────────────────────────────┐
│ dp[0] = 1 (empty sum)              │
│ dp[1] = 0 (no way to make 1)       │
│ dp[2] = 1 (using coin 2)           │
│ dp[3] = 1 (using coin 3)           │
│ dp[4] = 1 (using coins 2+2)        │
│ dp[5] = 1 (using coin 5)           │
│ dp[6] = 2 (using 2+2+2 or 3+3)     │
│ dp[7] = 2 (using 2+2+3 or 2+5)     │
│ dp[8] = 3 (using 2+2+2+2, 2+3+3, 3+5)│
│ dp[9] = 4 (using 2+2+5, 3+3+3, 2+2+2+3)│
└─────────────────────────────────────┘
```

**DP State Transition:**
```
For each coin c in [2, 3, 5]:
    For each sum i from c to target:
        dp[i] += dp[i - c]

Step-by-step:
┌─────────────────────────────────────┐
│ Coin 2:                            │
│ dp[2] += dp[0] = 1                 │
│ dp[3] += dp[1] = 0                 │
│ dp[4] += dp[2] = 1                 │
│ dp[5] += dp[3] = 1                 │
│ dp[6] += dp[4] = 1                 │
│ dp[7] += dp[5] = 1                 │
│ dp[8] += dp[6] = 2                 │
│ dp[9] += dp[7] = 2                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Coin 3:                            │
│ dp[3] += dp[0] = 1                 │
│ dp[4] += dp[1] = 0                 │
│ dp[5] += dp[2] = 1                 │
│ dp[6] += dp[3] = 2                 │
│ dp[7] += dp[4] = 1                 │
│ dp[8] += dp[5] = 2                 │
│ dp[9] += dp[6] = 4                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Coin 5:                            │
│ dp[5] += dp[0] = 1                 │
│ dp[6] += dp[1] = 0                 │
│ dp[7] += dp[2] = 1                 │
│ dp[8] += dp[3] = 1                 │
│ dp[9] += dp[4] = 1                 │
└─────────────────────────────────────┘
```

**Algorithm Flowchart:**
```
┌─────────────────────────────────────┐
│ Start: Read coins and target sum    │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Initialize dp[0] = 1                │
│ dp[1] to dp[target] = 0            │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ For each coin c:                    │
│   For sum i from c to target:       │
│     dp[i] += dp[i - c]             │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return dp[target]                   │
└─────────────────────────────────────┘
```

**Key Insight Visualization:**
```
To make sum i using coin c:
- We need to make sum (i - c) first
- Then add coin c to get sum i
- Total ways = ways to make (i - c)

Example: To make sum 9 using coin 2:
- Need to make sum 7 first
- Then add coin 2 to get sum 9
- Ways to make 9 = ways to make 7
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count the number of ways to make a target sum using available coins
- **Key Insight**: Use dynamic programming to build solutions from smaller subproblems
- **Challenge**: Avoid exponential time complexity with recursive approach

### Step 2: Initial Approach
**Recursive brute force (inefficient but correct):**

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

### Step 3: Optimization/Alternative
**Bottom-up dynamic programming:**

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

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each sum i, we consider all coin values and add the ways to make sum (i-coin).

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_coin_combinations_i():
    n, x = map(int, input().split())
    coins = list(map(int, input().split()))
    
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case: one way to make sum 0 (empty combination)
    
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    print(dp[x])

# Main execution
if __name__ == "__main__":
    solve_coin_combinations_i()
```

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (3, 9, [2, 3, 5], 8),
        (2, 5, [1, 2], 8),
        (3, 6, [1, 2, 3], 7),
        (4, 10, [1, 2, 5, 10], 11),
    ]
    
    for n, x, coins, expected in test_cases:
        result = solve_test(n, x, coins)
        print(f"n={n}, x={x}, coins={coins}, expected={expected}, result={result}")
        assert result == expected, f"Failed for n={n}, x={x}, coins={coins}"
        print("✓ Passed")
        print()

def solve_test(n, x, coins):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case
    
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x]

test_solution()
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(n^x) | O(x) | Try all combinations |
| Memoized | O(n×x) | O(x) | Store subproblem results |
| Bottom-up DP | O(n×x) | O(x) | Build from smaller subproblems |

### Time Complexity
- **Time**: O(n*x) - we iterate through each sum and each coin
- **Space**: O(x) - we store dp array of size x+1

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes combinations using optimal substructure
- **State Transition**: dp[i] = sum of dp[i-coin] for all valid coins
- **Base Case**: dp[0] = 1 represents empty combination
- **Optimal Approach**: Handles all cases correctly

## 🎨 Visual Example

### Input Example
```
Coins: [2, 3, 5]
Target Sum: 9
```

### All Possible Combinations
```
Target: 9, Coins: [2, 3, 5]

All ways to make sum 9:
1. 2 + 2 + 5 = 9
2. 2 + 5 + 2 = 9  
3. 5 + 2 + 2 = 9
4. 3 + 3 + 3 = 9
5. 2 + 2 + 2 + 3 = 9
6. 2 + 2 + 3 + 2 = 9
7. 2 + 3 + 2 + 2 = 9
8. 3 + 2 + 2 + 2 = 9

Total: 8 ways
```

### DP Table Construction
```
dp[i] = number of ways to make sum i

Initial state:
dp = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     0  1  2  3  4  5  6  7  8  9

Base case: dp[0] = 1 (one way to make sum 0: use no coins)

For each coin, update all possible sums:

Coin 2:
dp[2] += dp[0] = 1
dp[3] += dp[1] = 0
dp[4] += dp[2] = 1
dp[5] += dp[3] = 0
dp[6] += dp[4] = 1
dp[7] += dp[5] = 0
dp[8] += dp[6] = 1
dp[9] += dp[7] = 0

After coin 2: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

Coin 3:
dp[3] += dp[0] = 1
dp[4] += dp[1] = 1
dp[5] += dp[2] = 2
dp[6] += dp[3] = 1
dp[7] += dp[4] = 2
dp[8] += dp[5] = 2
dp[9] += dp[6] = 2

After coin 3: [1, 0, 1, 1, 1, 2, 1, 2, 2, 2]

Coin 5:
dp[5] += dp[0] = 3
dp[6] += dp[1] = 1
dp[7] += dp[2] = 3
dp[8] += dp[3] = 3
dp[9] += dp[4] = 4

Final: [1, 0, 1, 1, 1, 3, 1, 3, 3, 4]

Answer: dp[9] = 4 ways
```

### Step-by-Step DP Process
```
Target: 9, Coins: [2, 3, 5]

Step 1: Initialize
dp[0] = 1 (base case)
All other dp[i] = 0

Step 2: Process coin 2
For each sum i from 2 to 9:
  dp[i] += dp[i-2]

Step 3: Process coin 3  
For each sum i from 3 to 9:
  dp[i] += dp[i-3]

Step 4: Process coin 5
For each sum i from 5 to 9:
  dp[i] += dp[i-5]

Final result: dp[9] = 4
```

### Visual DP Table
```
Sum:    0  1  2  3  4  5  6  7  8  9
Initial:1  0  0  0  0  0  0  0  0  0

After coin 2:
        1  0  1  0  1  0  1  0  1  0
        │  │  │  │  │  │  │  │  │  │
        │  │  │  │  │  │  │  │  │  │
        ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼
        1  0  1  0  1  0  1  0  1  0

After coin 3:
        1  0  1  1  1  2  1  2  2  2
        │  │  │  │  │  │  │  │  │  │
        │  │  │  │  │  │  │  │  │  │
        ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼
        1  0  1  1  1  2  1  2  2  2

After coin 5:
        1  0  1  1  1  3  1  3  3  4
        │  │  │  │  │  │  │  │  │  │
        │  │  │  │  │  │  │  │  │  │
        ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼
        1  0  1  1  1  3  1  3  3  4
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(k^n)       │ O(n)         │ Try all      │
│                 │              │              │ combinations │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP (Order       │ O(n×x)       │ O(x)         │ Build from   │
│ Matters)        │              │              │ smaller sums │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP (Order       │ O(n×x)       │ O(x)         │ Avoid        │
│ Doesn't Matter) │              │              │ duplicates   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Mathematical    │ O(n×x)       │ O(x)         │ Generating   │
│                 │              │              │ functions    │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Coin Combinations Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: coins,   │
              │ target sum      │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize      │
              │ dp[0] = 1       │
              │ dp[i] = 0       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each coin   │
              │ in coins:       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For sum i from  │
              │ coin to target: │
              │ dp[i] += dp[i-  │
              │ coin]           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return dp[      │
              │ target]         │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Dynamic Programming for Counting**
- Count ways to achieve target using smaller subproblems
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **State Transition**
- Clear definition of how to build larger solutions from smaller ones
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Modular Arithmetic**
- Handle large numbers efficiently
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Coin Combinations with Limited Supply
**Problem**: Each coin has a limited number available.

```python
def coin_combinations_limited_supply(n, x, coins, quantities):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case
    
    for i in range(1, x + 1):
        for j, coin in enumerate(coins):
            for k in range(1, quantities[j] + 1):
                if i >= k * coin:
                    dp[i] = (dp[i] + dp[i - k * coin]) % MOD
    
    return dp[x]

# Example usage
coins = [2, 3, 5]
quantities = [3, 2, 1]  # 3 coins of value 2, 2 coins of value 3, 1 coin of value 5
result = coin_combinations_limited_supply(3, 9, coins, quantities)
print(f"Ways to make sum 9: {result}")
```

### Variation 2: Coin Combinations with Order Constraints
**Problem**: Coins must be used in a specific order.

```python
def coin_combinations_ordered(n, x, coins):
    MOD = 10**9 + 7
    
    # dp[i][j] = ways to make sum i using first j coins
    dp = [[0] * (n + 1) for _ in range(x + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(x + 1):
        for j in range(n + 1):
            if dp[i][j] > 0:  # If this state is reachable
                # Don't use coin j
                if j + 1 <= n:
                    dp[i][j + 1] = (dp[i][j + 1] + dp[i][j]) % MOD
                # Use coin j
                if j < n and i + coins[j] <= x:
                    dp[i + coins[j]][j] = (dp[i + coins[j]][j] + dp[i][j]) % MOD
    
    return dp[x][n]

# Example usage
coins = [2, 3, 5]
result = coin_combinations_ordered(3, 9, coins)
print(f"Ways to make sum 9: {result}")
```

### Variation 3: Coin Combinations with Probability
**Problem**: Each coin has a probability of success.

```python
def coin_combinations_probability(n, x, coins, probabilities):
    MOD = 10**9 + 7
    
    # dp[i] = expected number of ways to make sum i
    dp = [0.0] * (x + 1)
    dp[0] = 1.0  # Base case
    
    for i in range(1, x + 1):
        for j, coin in enumerate(coins):
            if i >= coin:
                dp[i] += dp[i - coin] * probabilities[j]
    
    return dp[x]

# Example usage
coins = [2, 3, 5]
probabilities = [0.9, 0.8, 0.7]  # probability of each coin being valid
result = coin_combinations_probability(3, 9, coins, probabilities)
print(f"Expected ways to make sum 9: {result}")
```

### Variation 4: Coin Combinations with Weights
**Problem**: Each coin has a weight, find weighted combinations.

```python
def coin_combinations_weighted(n, x, coins, weights):
    MOD = 10**9 + 7
    
    # dp[i] = weighted sum of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case
    
    for i in range(1, x + 1):
        for j, coin in enumerate(coins):
            if i >= coin:
                dp[i] = (dp[i] + dp[i - coin] * weights[j]) % MOD
    
    return dp[x]

# Example usage
coins = [2, 3, 5]
weights = [2, 3, 1]  # weight of each coin
result = coin_combinations_weighted(3, 9, coins, weights)
print(f"Weighted ways to make sum 9: {result}")
```

### Variation 5: Coin Combinations with Dynamic Programming Optimization
**Problem**: Optimize the DP solution for better performance.

```python
def coin_combinations_optimized(n, x, coins):
    MOD = 10**9 + 7
    
    # Sort coins for better performance
    coins.sort()
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case
    
    # Use early termination and better memory access
    for i in range(1, x + 1):
        for coin in coins:
            if coin > i:
                break  # Early termination
            dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x]

# Example usage
coins = [5, 3, 2]  # Unsorted
result = coin_combinations_optimized(3, 9, coins)
print(f"Ways to make sum 9: {result}")
```

## 🔗 Related Problems

- **[Dice Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar counting problems
- **[Minimizing Coins](/cses-analyses/problem_soulutions/dynamic_programming/)**: Optimization problems
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: Sum-related problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for counting problems
2. **State Transitions**: Important for DP formulation
3. **Modular Arithmetic**: Important for handling large numbers
4. **Combinatorics**: Important for understanding counting

---

**This is a great introduction to dynamic programming for counting problems!** 🎯

```python
def coin_combinations_dp(n, x, coins):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case: one way to make sum 0 (empty combination)
    
    for i in range(1, x + 1):
        for coin in coins: if i >= 
coin: dp[i] = (dp[i] + dp[i - coin]) % MOD
    
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
        for coin in coins: if coin > 
i: break  # Early termination since coins are sorted
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
    for coin in coins: if i >= 
coin: dp[i] = (dp[i] + dp[i - coin]) % MOD

print(dp[x])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^x) | O(x) | Try all combinations |
| Memoization | O(n*x) | O(x) | Store subproblem results |
| Bottom-Up DP | O(n*x) | O(x) | Build solution iteratively |
| Optimized DP | O(n*x) | O(x) | Early termination with sorting |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Dynamic Programming**: Build solutions from smaller subproblems
- **Coin Change**: Classic DP problem with optimal substructure
- **Bottom-up Approach**: Iterative solution building
- **Modular Arithmetic**: Handle large numbers with modulo operations

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Coin Combinations with Limited Coins**
```python
def coin_combinations_limited(n, x, coins, limits):
    # Handle coin combinations with limited number of each coin
    
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (x + 1)
    dp[0] = 1  # Base case
    
    for i in range(n):
        coin = coins[i]
        limit = limits[i]
        
        # Process this coin type
        for j in range(x, coin - 1, -1):
            for k in range(1, min(limit + 1, j // coin + 1)):
                if j >= k * coin:
                    dp[j] = (dp[j] + dp[j - k * coin]) % MOD
    
    return dp[x]
```

#### **2. Coin Combinations with Minimum Coins**
```python
def coin_combinations_minimum(n, x, coins):
    # Handle coin combinations with minimum number of coins
    
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i with minimum coins
    dp = [0] * (x + 1)
    min_coins = [float('inf')] * (x + 1)
    
    dp[0] = 1
    min_coins[0] = 0
    
    for i in range(1, x + 1):
        for coin in coins:
            if i >= coin:
                if min_coins[i - coin] + 1 < min_coins[i]:
                    min_coins[i] = min_coins[i - coin] + 1
                    dp[i] = dp[i - coin]
                elif min_coins[i - coin] + 1 == min_coins[i]:
                    dp[i] = (dp[i] + dp[i - coin]) % MOD
    
    return dp[x] if min_coins[x] != float('inf') else 0
```

#### **3. Coin Combinations with Dynamic Updates**
```python
def coin_combinations_dynamic(operations):
    # Handle coin combinations with dynamic coin updates
    
    coins = []
    x = 0
    dp = [0] * (10**6 + 1)
    dp[0] = 1
    MOD = 10**9 + 7
    
    for operation in operations:
        if operation[0] == 'add_coin':
            # Add new coin
            coin = operation[1]
            coins.append(coin)
            
            # Update DP array
            for i in range(coin, x + 1):
                dp[i] = (dp[i] + dp[i - coin]) % MOD
        
        elif operation[0] == 'set_target':
            # Set target sum
            x = operation[1]
            
            # Recalculate DP array
            dp = [0] * (x + 1)
            dp[0] = 1
            
            for coin in coins:
                for i in range(coin, x + 1):
                    dp[i] = (dp[i] + dp[i - coin]) % MOD
        
        elif operation[0] == 'query':
            # Return current number of ways
            yield dp[x] if x < len(dp) else 0
    
    return list(coin_combinations_dynamic(operations))
```

## 🔗 Related Problems

### Links to Similar Problems
- **Dynamic Programming**: Coin change, knapsack problems
- **Counting Problems**: Ways to make sums, combinations
- **Optimization**: Minimum coins, maximum value
- **Combinatorics**: Permutations and combinations

## 📚 Learning Points

### Key Takeaways
- **Dynamic programming** is essential for counting problems
- **Bottom-up approach** is often more efficient than top-down
- **State transitions** should be carefully designed
- **Modular arithmetic** prevents integer overflow

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
    for choice in choices: if i >= 
choice: dp[i] = (dp[i] + dp[i - choice]) % MOD
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
        for coin in coins: if i >= 
coin: dp[i] = (dp[i] + dp[i - coin]) % MOD
    
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