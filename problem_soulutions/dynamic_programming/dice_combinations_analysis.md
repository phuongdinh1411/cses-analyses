---
layout: simple
title: "Dice Combinations - Count Ways to Make Sum with Dice"
permalink: /problem_soulutions/dynamic_programming/dice_combinations_analysis
---

# Dice Combinations - Count Ways to Make Sum with Dice

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the fundamental concept of dynamic programming and state transitions
- Apply bottom-up DP to solve counting problems with recurrence relations
- Implement efficient DP solutions using iterative approaches and memoization
- Optimize DP solutions using space-efficient techniques and modular arithmetic
- Handle edge cases in DP problems (base cases, boundary conditions, large numbers)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, recurrence relations, memoization, bottom-up DP
- **Data Structures**: Arrays, DP tables, memoization structures
- **Mathematical Concepts**: Combinatorics, modular arithmetic, recurrence relations, counting principles
- **Programming Skills**: Array manipulation, iterative programming, modular arithmetic, DP implementation
- **Related Problems**: Coin Combinations I (similar DP pattern), Minimizing Coins (DP optimization), Counting Sequences (counting problems)

## Problem Description

Count the number of ways to construct sum n by throwing a dice one or more times. Each throw produces an outcome in {1,2,3,4,5,6}.

**Input**: 
- First line: integer n (target sum to achieve)

**Output**: 
- Print the number of ways to achieve sum n modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 10^6
- Each dice throw produces outcome in {1,2,3,4,5,6}
- Must use one or more dice throws
- Result must be modulo 10^9 + 7
- Count all possible sequences of dice throws

**Example**:
```
Input:
3

Output:
4

Explanation**: 
There are 4 ways to achieve sum 3:
- 1+1+1 (three throws of 1)
- 1+2 (throw 1, then 2)
- 2+1 (throw 2, then 1)
- 3 (single throw of 3)
```

## Visual Example

### Input and Problem Setup
```
Input: n = 3 (target sum)

Dice outcomes: {1, 2, 3, 4, 5, 6}
Goal: Count ways to achieve sum 3 using one or more dice throws
Result: Modulo 10^9 + 7
```

### Dice Combination Analysis
```
For n = 3, let's enumerate all possible ways:

Way 1: Single throw
- Throw 3: [3] → sum = 3 ✓

Way 2: Two throws
- Throw 1, then 2: [1, 2] → sum = 1 + 2 = 3 ✓
- Throw 2, then 1: [2, 1] → sum = 2 + 1 = 3 ✓

Way 3: Three throws
- Throw 1, 1, 1: [1, 1, 1] → sum = 1 + 1 + 1 = 3 ✓

Total: 4 ways
```

### Dynamic Programming Pattern
```
DP State: dp[i] = number of ways to achieve sum i

Base case: dp[0] = 1 (one way to achieve sum 0: empty sequence)

Recurrence: dp[i] = dp[i-1] + dp[i-2] + dp[i-3] + dp[i-4] + dp[i-5] + dp[i-6]

For i = 3:
dp[3] = dp[2] + dp[1] + dp[0] = 2 + 1 + 1 = 4
```

### State Transition Visualization
```
Building DP table for n = 3:

dp[0] = 1 (base case)
dp[1] = dp[0] = 1 (only way: throw 1)
dp[2] = dp[1] + dp[0] = 1 + 1 = 2 (ways: [1,1], [2])
dp[3] = dp[2] + dp[1] + dp[0] = 2 + 1 + 1 = 4 (ways: [1,1,1], [1,2], [2,1], [3])
```

### Key Insight
The solution works by:
1. Using dynamic programming to build solutions from smaller subproblems
2. For each sum i, considering all possible dice outcomes (1-6)
3. Adding the number of ways to achieve sum (i-dice) for each dice outcome
4. Using modular arithmetic to handle large numbers
5. Time complexity: O(n) for filling DP table
6. Space complexity: O(n) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of dice throws
- Use recursive approach to explore all paths
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. For each target sum, try all possible dice outcomes (1-6)
2. Recursively solve for remaining sum after each dice throw
3. Count all valid sequences that reach sum 0
4. Return total count modulo 10^9 + 7

**Visual Example:**
```
Brute force approach: Try all possible dice sequences
For n = 3:

Recursive tree:
                   3
              /    |    |    |    |    \
            2      1    0   -1   -2   -3
          / | \   /|\   |   (invalid)
         1  0 -1  0 -1 -2
        /|   |   (invalid)
       0 -1  1
       |  (invalid)
       1
```

**Implementation:**
```python
def dice_combinations_brute_force(n):
    MOD = 10**9 + 7
    
    def count_ways(target):
        if target == 0:
            return 1
        if target < 0:
            return 0
        
        ways = 0
        for dice in range(1, 7):
            ways += count_ways(target - dice)
        
        return ways % MOD
    
    return count_ways(n)

def solve_dice_combinations_brute_force():
    n = int(input())
    result = dice_combinations_brute_force(n)
    print(result)
```

**Time Complexity:** O(6^n) for trying all possible dice sequences
**Space Complexity:** O(n) for recursion depth

**Why it's inefficient:**
- O(6^n) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large n
- Poor performance with exponential growth

### Approach 2: Recursive with Memoization (Better)

**Key Insights from Memoized Solution:**
- Use memoization to avoid recalculating the same subproblems
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses dynamic programming principles

**Algorithm:**
1. Use memoization to store results of subproblems
2. For each target sum, check if already computed
3. If not computed, recursively solve and store result
4. Return stored result for future use

**Visual Example:**
```
Memoized approach: Store results to avoid recalculation
For n = 3:

First call: count_ways(3)
- Try dice 1: count_ways(2) → not in memo, compute
- Try dice 2: count_ways(1) → not in memo, compute  
- Try dice 3: count_ways(0) → not in memo, compute
- Store result in memo

Subsequent calls reuse memoized results
```

**Implementation:**
```python
def dice_combinations_memoization(n):
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
        for dice in range(1, 7):
            ways += count_ways(target - dice)
        
        memo[target] = ways % MOD
        return memo[target]
    
    return count_ways(n)

def solve_dice_combinations_memoization():
    n = int(input())
    result = dice_combinations_memoization(n)
    print(result)
```

**Time Complexity:** O(n) for computing each subproblem once
**Space Complexity:** O(n) for memoization storage

**Why it's better:**
- O(n) time complexity is much better than O(6^n)
- Uses memoization for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Bottom-Up Dynamic Programming (Optimal)

**Key Insights from Bottom-Up DP Solution:**
- Use iterative approach to build solutions from smaller subproblems
- Most efficient approach for dynamic programming problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Initialize DP array with base case
2. Iteratively fill DP array from smaller to larger sums
3. For each sum i, consider all dice outcomes and add ways from (i-dice)
4. Use modular arithmetic to handle large numbers

**Visual Example:**
```
Bottom-up DP: Build solutions iteratively
For n = 3:

Initialize: dp = [1, 0, 0, 0] (dp[0] = 1)

i = 1: dp[1] = dp[0] = 1
i = 2: dp[2] = dp[1] + dp[0] = 1 + 1 = 2  
i = 3: dp[3] = dp[2] + dp[1] + dp[0] = 2 + 1 + 1 = 4

Final: dp = [1, 1, 2, 4]
```

**Implementation:**
```python
def solve_dice_combinations():
    n = int(input())
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case: one way to make sum 0 (empty combination)
    
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % MOD
    
    print(dp[n])

# Main execution
if __name__ == "__main__":
    solve_dice_combinations()
```

**Time Complexity:** O(n) for filling DP table
**Space Complexity:** O(n) for DP array

**Why it's optimal:**
- O(n) time complexity is optimal for this problem
- Uses bottom-up dynamic programming for efficient solution
- Most efficient approach for competitive programming
- Standard method for counting problems with recurrence relations

## 🎯 Problem Variations

### Variation 1: Dice Combinations with Different Dice
**Problem**: Count ways to achieve sum n using dice with different numbers of faces.

**Link**: [CSES Problem Set - Dice Combinations Extended](https://cses.fi/problemset/task/dice_combinations_extended)

```python
def dice_combinations_extended(n, dice_faces):
    MOD = 10**9 + 7
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for i in range(1, n + 1):
        for face in dice_faces:
            if i >= face:
                dp[i] = (dp[i] + dp[i - face]) % MOD
    
    return dp[n]
```

### Variation 2: Dice Combinations with Minimum Throws
**Problem**: Count ways to achieve sum n using at least k dice throws.

**Link**: [CSES Problem Set - Dice Combinations Minimum Throws](https://cses.fi/problemset/task/dice_combinations_minimum_throws)

```python
def dice_combinations_minimum_throws(n, min_throws):
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(min_throws + 1)]
    dp[0][0] = 1
    
    for throws in range(1, min_throws + 1):
        for sum_val in range(1, n + 1):
            for dice in range(1, 7):
                if sum_val >= dice:
                    dp[throws][sum_val] = (dp[throws][sum_val] + dp[throws-1][sum_val-dice]) % MOD
    
    return dp[min_throws][n]
```

### Variation 3: Dice Combinations with Maximum Throws
**Problem**: Count ways to achieve sum n using at most k dice throws.

**Link**: [CSES Problem Set - Dice Combinations Maximum Throws](https://cses.fi/problemset/task/dice_combinations_maximum_throws)

```python
def dice_combinations_maximum_throws(n, max_throws):
    MOD = 10**9 + 7
    dp = [[0] * (n + 1) for _ in range(max_throws + 1)]
    dp[0][0] = 1
    
    for throws in range(1, max_throws + 1):
        for sum_val in range(n + 1):
            dp[throws][sum_val] = dp[throws-1][sum_val]  # Don't throw
            for dice in range(1, 7):
                if sum_val >= dice:
                    dp[throws][sum_val] = (dp[throws][sum_val] + dp[throws-1][sum_val-dice]) % MOD
    
    return sum(dp[throws][n] for throws in range(max_throws + 1)) % MOD
```

## 🔗 Related Problems

- **[Coin Combinations I](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar DP pattern for counting combinations
- **[Minimizing Coins](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP optimization problems
- **[Counting Sequences](/cses-analyses/problem_soulutions/dynamic_programming/)**: Counting problems with DP
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP problems with sum constraints

## 📚 Learning Points

1. **Dynamic Programming**: Essential for understanding counting problems with recurrence relations
2. **Bottom-Up DP**: Key technique for building solutions from smaller subproblems
3. **Memoization**: Important for optimizing recursive solutions
4. **Modular Arithmetic**: Critical for handling large numbers in competitive programming
5. **State Transitions**: Foundation for understanding DP recurrence relations
6. **Counting Principles**: Critical for understanding combinatorial problems

## 📝 Summary

The Dice Combinations problem demonstrates dynamic programming and counting principles for efficient combination counting. We explored three approaches:

1. **Recursive Brute Force**: O(6^n) time complexity using recursive exploration, inefficient due to exponential growth
2. **Recursive with Memoization**: O(n) time complexity using memoization, better approach for recursive problems
3. **Bottom-Up Dynamic Programming**: O(n) time complexity with iterative DP, optimal approach for competitive programming

The key insights include understanding dynamic programming principles, using bottom-up approaches for efficient computation, and applying modular arithmetic for large number handling. This problem serves as an excellent introduction to dynamic programming and counting problems in competitive programming.
