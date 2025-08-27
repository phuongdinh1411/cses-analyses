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

---

*This analysis shows how to efficiently solve counting problems using dynamic programming.* 