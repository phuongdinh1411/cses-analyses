---
layout: simple
title: CSES Dice Combinations - Problem Analysis
permalink: /problem_soulutions/dynamic_programming/dice_combinations_analysis/
---

# CSES Dice Combinations - Problem Analysis

## Problem Statement
Your task is to count the number of ways to construct sum n by throwing a dice one or more times. Each throw produces an outcome in {1,2,3,4,5,6}.

For example, if n=3, there are 4 ways:
- 1+1+1
- 1+2
- 2+1
- 3

### Input
The only input line contains an integer n.

### Output
Print the number of ways modulo 10^9+7.

### Constraints
- 1 ≤ n ≤ 10^6

### Example
```
Input:
3

Output:
4
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(6^n)
**Description**: Try all possible combinations of dice throws recursively.

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
```

**Why this is inefficient**: We're trying all possible combinations of dice throws, which leads to exponential complexity. For each position, we have 6 choices, leading to O(6^n) complexity.

### Improvement 1: Recursive with Memoization - O(n)
**Description**: Use memoization to avoid recalculating the same subproblems.

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
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def dice_combinations_dp(n):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case: one way to make sum 0 (empty combination)
    
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % MOD
    
    return dp[n]
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each sum i, we consider all possible dice values and add the ways to make sum (i-dice).

### Alternative: Optimized DP - O(n)
**Description**: Use a more efficient DP approach with sliding window.

```python
def dice_combinations_optimized(n):
    MOD = 10**9 + 7
    
    if n < 6:
        # Handle small cases directly
        dp = [1, 1, 2, 4, 8, 16]
        return dp[n] if n < len(dp) else 0
    
    # For larger n, use sliding window
    dp = [1, 1, 2, 4, 8, 16]  # Base cases
    
    for i in range(6, n + 1):
        # dp[i] = dp[i-1] + dp[i-2] + ... + dp[i-6]
        next_val = sum(dp[-6:]) % MOD
        dp.append(next_val)
    
    return dp[n]
```

**Why this works**: We can optimize further by recognizing that we only need the last 6 values to calculate the next value, allowing us to use a sliding window approach.

## Final Optimal Solution

```python
n = int(input())
MOD = 10**9 + 7

# dp[i] = number of ways to make sum i
dp = [0] * (n + 1)
dp[0] = 1  # Base case

for i in range(1, n + 1):
    for dice in range(1, 7):
        if i >= dice:
            dp[i] = (dp[i] + dp[i - dice]) % MOD

print(dp[n])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(6^n) | O(n) | Try all combinations |
| Memoization | O(n) | O(n) | Store subproblem results |
| Bottom-Up DP | O(n) | O(n) | Build solution iteratively |
| Optimized DP | O(n) | O(1) | Use sliding window |

## Key Insights for Other Problems

### 1. **Dynamic Programming for Counting**
**Principle**: Use DP to count the number of ways to achieve a target.
**Applicable to**:
- Counting problems
- Combination problems
- Path counting
- Optimization problems

**Example Problems**:
- Dice combinations
- Coin change
- Path counting
- Combination problems

### 2. **Memoization vs Bottom-Up**
**Principle**: Choose between memoization (top-down) and bottom-up DP based on problem characteristics.
**Applicable to**:
- Dynamic programming
- Recursive problems
- Optimization problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- Recursive problems
- Optimization problems
- Algorithm design

### 3. **State Transition**
**Principle**: Define clear state transitions for DP problems.
**Applicable to**:
- Dynamic programming
- State machine problems
- Optimization problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- State machine problems
- Optimization problems
- Algorithm design

### 4. **Modular Arithmetic**
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

## Notable Techniques

### 1. **DP State Definition Pattern**
```python
# Define DP state clearly
dp = [0] * (n + 1)
dp[0] = 1  # Base case
```

### 2. **State Transition Pattern**
```python
# Define state transitions
for i in range(1, n + 1):
    for choice in choices:
        if i >= choice:
            dp[i] = (dp[i] + dp[i - choice]) % MOD
```

### 3. **Memoization Pattern**
```python
# Use memoization for top-down DP
memo = {}
def solve(target):
    if target in memo:
        return memo[target]
    # Calculate result
    memo[target] = result
    return result
```

## Edge Cases to Remember

1. **n = 0**: Return 1 (empty combination)
2. **n = 1**: Return 1 (only one way: throw 1)
3. **n < 6**: Handle small cases directly
4. **Large n**: Use modular arithmetic throughout
5. **Integer overflow**: Take modulo at each step

## Problem-Solving Framework

1. **Identify DP nature**: This is a counting problem with overlapping subproblems
2. **Define state**: dp[i] = number of ways to make sum i
3. **Define transitions**: dp[i] = sum of dp[i-dice] for all dice values
4. **Handle base case**: dp[0] = 1
5. **Use modular arithmetic**: Take modulo at each step

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Different Dice Values**
**Problem**: Instead of {1,2,3,4,5,6}, use dice with values {1,2,3,4,5,6,7,8}.
```python
def dice_combinations_extended(n):
    MOD = 10**9 + 7
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for i in range(1, n + 1):
        for dice in range(1, 9):  # 8-sided dice
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % MOD
    
    return dp[n]
```

#### **Variation 2: Minimum Number of Throws**
**Problem**: Find the minimum number of dice throws needed to make sum n.
```python
def min_dice_throws(n):
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = min(dp[i], dp[i - dice] + 1)
    
    return dp[n] if dp[n] != float('inf') else -1
```

#### **Variation 3: Count Ways with Maximum Throws**
**Problem**: Count ways to make sum n using at most k dice throws.
```python
def dice_combinations_with_limit(n, k):
    MOD = 10**9 + 7
    # dp[i][j] = ways to make sum i using exactly j throws
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(n + 1):
        for j in range(k + 1):
            for dice in range(1, 7):
                if i >= dice and j > 0:
                    dp[i][j] = (dp[i][j] + dp[i - dice][j - 1]) % MOD
    
    # Sum all ways with at most k throws
    result = 0
    for j in range(k + 1):
        result = (result + dp[n][j]) % MOD
    return result
```

#### **Variation 4: Unbounded vs Bounded Dice**
**Problem**: What if you can only use each dice value a limited number of times?
```python
def bounded_dice_combinations(n, limits):
    # limits[i] = max times you can use dice value i+1
    MOD = 10**9 + 7
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for dice in range(1, 7):
        for i in range(n, dice - 1, -1):  # Process backwards
            for count in range(1, limits[dice - 1] + 1):
                if i >= dice * count:
                    dp[i] = (dp[i] + dp[i - dice * count]) % MOD
    
    return dp[n]
```

#### **Variation 5: Probability of Reaching Sum**
**Problem**: What's the probability of reaching sum n with fair dice?
```python
def dice_probability(n, max_throws=100):
    # dp[i][j] = probability of reaching sum i in j throws
    dp = [[0.0] * (max_throws + 1) for _ in range(n + 1)]
    dp[0][0] = 1.0
    
    for j in range(max_throws):
        for i in range(n + 1):
            if dp[i][j] > 0:
                for dice in range(1, 7):
                    if i + dice <= n:
                        dp[i + dice][j + 1] += dp[i][j] / 6.0
    
    # Sum probabilities of reaching n in any number of throws
    return sum(dp[n][j] for j in range(max_throws + 1))
```

### 🔗 **Related Problems & Concepts**

#### **1. Coin Change Problems**
- **Unbounded Knapsack**: Use unlimited coins of each denomination
- **Bounded Knapsack**: Limited number of each coin type
- **Minimum Coins**: Find minimum coins needed
- **All Possible Combinations**: Count all ways to make change

#### **2. Dynamic Programming Patterns**
- **1D DP**: Single state variable (sum)
- **2D DP**: Two state variables (sum, number of items)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Combinatorics Problems**
- **Permutations**: Order matters
- **Combinations**: Order doesn't matter
- **Partitions**: Ways to partition a number
- **Catalan Numbers**: Special counting sequences

#### **4. Optimization Problems**
- **Shortest Path**: Minimum steps to reach target
- **Longest Path**: Maximum steps to reach target
- **Resource Allocation**: Optimal use of limited resources
- **Scheduling**: Optimal arrangement of tasks

#### **5. Probability & Statistics**
- **Expected Value**: Average outcome over many trials
- **Variance**: Spread of outcomes
- **Markov Chains**: State transition probabilities
- **Monte Carlo**: Simulation-based probability estimation

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    # n = target sum, k = max throws
    result = dice_combinations_with_limit(n, k)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute for range [1, max_n]
def precompute_dice_combinations(max_n):
    MOD = 10**9 + 7
    dp = [0] * (max_n + 1)
    dp[0] = 1
    
    for i in range(1, max_n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % MOD
    
    return dp

# Answer range queries
def range_query(l, r, dp):
    return sum(dp[i] for i in range(l, r + 1))
```

#### **3. Interactive Problems**
```python
# Interactive dice game
def interactive_dice_game():
    target = int(input())
    current_sum = 0
    throws = 0
    
    while current_sum < target:
        dice = int(input())  # Player chooses dice value
        if 1 <= dice <= 6:
            current_sum += dice
            throws += 1
            print(f"Current sum: {current_sum}, Throws: {throws}")
        else:
            print("Invalid dice value!")
    
    print(f"Reached target in {throws} throws!")
```

### 🧮 **Mathematical Extensions**

#### **1. Generating Functions**
- **Power Series**: Represent combinations as polynomial coefficients
- **Recurrence Relations**: Find closed-form solutions
- **Asymptotic Analysis**: Analyze behavior for large n
- **Combinatorial Identities**: Prove mathematical relationships

#### **2. Number Theory Connections**
- **Modular Arithmetic**: Work with large numbers
- **Prime Factorization**: Analyze divisibility properties
- **Chinese Remainder Theorem**: Solve modular equations
- **Euler's Totient Function**: Count coprime numbers

#### **3. Advanced DP Techniques**
- **Digit DP**: Count numbers with specific properties
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split problems into subproblems
- **Persistent Data Structures**: Maintain history of states

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Knapsack Algorithms**: 0/1, unbounded, fractional
- **Subset Sum**: Find subsets with given sum
- **Partition Problems**: Divide set into equal parts
- **Scheduling Algorithms**: Optimal task arrangement

#### **2. Mathematical Concepts**
- **Combinatorics**: Counting principles and techniques
- **Probability Theory**: Random processes and outcomes
- **Number Theory**: Properties of integers
- **Linear Algebra**: Matrix operations and transformations

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Modular Arithmetic**: Handling large numbers efficiently

---

*This analysis demonstrates the power of dynamic programming for counting problems and shows various extensions and applications.* 