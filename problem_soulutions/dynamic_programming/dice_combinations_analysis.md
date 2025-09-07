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

## 📋 Problem Description

Count the number of ways to construct sum n by throwing a dice one or more times. Each throw produces an outcome in {1,2,3,4,5,6}.

This is a classic dynamic programming problem that requires counting the number of ways to achieve a target sum using dice throws. The solution involves using bottom-up DP to build solutions from smaller subproblems.

**Input**: 
- n: target sum to achieve

**Output**: 
- Number of ways to achieve sum n modulo 10⁹+7

**Constraints**:
- 1 ≤ n ≤ 10⁶

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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count the number of ways to achieve a target sum using dice throws
- **Key Insight**: Use dynamic programming to build solutions from smaller subproblems
- **Challenge**: Avoid exponential time complexity with recursive approach

### Step 2: Initial Approach
**Recursive brute force (inefficient but correct):**

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

### Step 3: Optimization/Alternative
**Optimized DP with sliding window:**

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

### Step 4: Complete Solution
**Putting it all together:**

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
        (1, 1),   # 1 way: [1]
        (2, 2),   # 2 ways: [1,1], [2]
        (3, 4),   # 4 ways: [1,1,1], [1,2], [2,1], [3]
        (4, 8),   # 8 ways
        (5, 16),  # 16 ways
    ]
    
    for n, expected in test_cases:
        result = solve_test(n)
        print(f"n={n}, expected={expected}, result={result}")
        assert result == expected, f"Failed for n={n}"
        print("✓ Passed")
        print()

def solve_test(n):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case
    
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % MOD
    
    return dp[n]

test_solution()
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(6^n) | O(n) | Try all combinations |
| Memoized | O(n) | O(n) | Store subproblem results |
| Bottom-up DP | O(n) | O(n) | Build from smaller subproblems |
| Optimized DP | O(n) | O(1) | Sliding window approach |

### Time Complexity
- **Time**: O(n) - we iterate through each sum from 1 to n
- **Space**: O(n) - we store dp array of size n+1

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes combinations using optimal substructure
- **State Transition**: dp[i] = sum of dp[i-dice] for all valid dice values
- **Base Case**: dp[0] = 1 represents empty combination
- **Optimal Approach**: Handles all cases correctly

## 🎨 Visual Example

### Input Example
```
Target Sum: 3
Dice Values: [1, 2, 3, 4, 5, 6]
```

### All Possible Combinations
```
Target: 3, Dice: [1, 2, 3, 4, 5, 6]

All ways to achieve sum 3:
1. 1 + 1 + 1 = 3 (three throws of 1)
2. 1 + 2 = 3 (throw 1, then 2)
3. 2 + 1 = 3 (throw 2, then 1)
4. 3 = 3 (single throw of 3)

Total: 4 ways
```

### DP Table Construction
```
dp[i] = number of ways to achieve sum i

Initial state:
dp = [1, 0, 0, 0]
     0  1  2  3

Base case: dp[0] = 1 (one way to achieve sum 0: no throws)

For each sum i from 1 to 3:
  dp[i] = dp[i-1] + dp[i-2] + dp[i-3] + dp[i-4] + dp[i-5] + dp[i-6]
  (only if i >= dice_value)

dp[1] = dp[0] = 1
dp[2] = dp[1] + dp[0] = 1 + 1 = 2
dp[3] = dp[2] + dp[1] + dp[0] = 2 + 1 + 1 = 4

Final: [1, 1, 2, 4]
Answer: dp[3] = 4 ways
```

### Step-by-Step DP Process
```
Target: 3, Dice: [1, 2, 3, 4, 5, 6]

Step 1: Initialize
dp[0] = 1 (base case)
All other dp[i] = 0

Step 2: Calculate dp[1]
dp[1] = dp[0] = 1
(Can achieve sum 1 by throwing 1)

Step 3: Calculate dp[2]
dp[2] = dp[1] + dp[0] = 1 + 1 = 2
(Can achieve sum 2 by: 1+1 or 2)

Step 4: Calculate dp[3]
dp[3] = dp[2] + dp[1] + dp[0] = 2 + 1 + 1 = 4
(Can achieve sum 3 by: 1+1+1, 1+2, 2+1, or 3)

Final result: dp[3] = 4
```

### Visual DP Table
```
Sum:    0  1  2  3
Initial:1  0  0  0

After dp[1]:
        1  1  0  0

After dp[2]:
        1  1  2  0

After dp[3]:
        1  1  2  4
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(6^n)       │ O(n)         │ Try all      │
│                 │              │              │ combinations │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP Bottom-up    │ O(n)         │ O(n)         │ Build from   │
│                 │              │              │ smaller sums │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP Top-down     │ O(n)         │ O(n)         │ Memoization  │
│                 │              │              │ with recursion│
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Mathematical    │ O(n)         │ O(1)         │ Fibonacci-   │
│                 │              │              │ like sequence│
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Dice Combinations Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: target   │
              │ sum n           │
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
              │ For i = 1 to n: │
              │ dp[i] = sum of  │
              │ dp[i-dice] for  │
              │ all dice values │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return dp[n]    │
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

### Variation 1: Dice with Different Values
**Problem**: Each dice has different possible values.

```python
def dice_combinations_custom(n, dice_values):
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case
    
    for i in range(1, n + 1):
        for dice in dice_values:
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % MOD
    
    return dp[n]

# Example usage
dice_values = [1, 2, 3, 4, 5, 6, 8, 10]  # Custom dice values
result = dice_combinations_custom(10, dice_values)
print(f"Ways to make sum 10: {result}")
```

### Variation 2: Limited Number of Throws
**Problem**: Find ways to achieve sum with at most k throws.

```python
def dice_combinations_with_limit(n, max_throws):
    MOD = 10**9 + 7
    
    # dp[i][j] = ways to make sum i with exactly j throws
    dp = [[0] * (max_throws + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(n + 1):
        for j in range(max_throws + 1):
            if dp[i][j] > 0:  # If this state is reachable
                for dice in range(1, 7):
                    if i + dice <= n and j + 1 <= max_throws:
                        dp[i + dice][j + 1] = (dp[i + dice][j + 1] + dp[i][j]) % MOD
    
    # Sum all ways with at most max_throws
    total_ways = 0
    for j in range(max_throws + 1):
        total_ways = (total_ways + dp[n][j]) % MOD
    
    return total_ways

# Example usage
result = dice_combinations_with_limit(10, 3)
print(f"Ways to make sum 10 with at most 3 throws: {result}")
```

### Variation 3: Probability of Achieving Sum
**Problem**: Find probability of achieving sum n.

```python
def dice_probability(n, max_throws):
    MOD = 10**9 + 7
    
    # dp[i][j] = ways to make sum i with exactly j throws
    dp = [[0] * (max_throws + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # Base case
    
    for i in range(n + 1):
        for j in range(max_throws + 1):
            if dp[i][j] > 0:
                for dice in range(1, 7):
                    if i + dice <= n and j + 1 <= max_throws:
                        dp[i + dice][j + 1] = (dp[i + dice][j + 1] + dp[i][j]) % MOD
    
    # Calculate probability
    favorable_outcomes = sum(dp[n][j] for j in range(max_throws + 1))
    total_outcomes = 6 ** max_throws  # Total possible outcomes
    
    # For large numbers, use modular inverse
    def mod_inverse(a, m):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            return None  # Modular inverse doesn't exist
        return (x % m + m) % m
    
    if total_outcomes == 0:
        return 0
    
    # Calculate (favorable_outcomes * mod_inverse(total_outcomes, MOD)) % MOD
    inv_total = mod_inverse(total_outcomes, MOD)
    if inv_total is None:
        return 0
    
    probability = (favorable_outcomes * inv_total) % MOD
    return probability

# Example usage
prob = dice_probability(10, 3)
print(f"Probability of achieving sum 10 in 3 throws: {prob}")
```

### Variation 4: Expected Value of Sum
**Problem**: Find expected value of sum after k throws.

```python
def expected_dice_sum(k):
    # Expected value of single throw = (1+2+3+4+5+6)/6 = 3.5
    expected_single = 3.5
    
    # Expected value after k throws = k * expected_single
    expected_total = k * expected_single
    
    return expected_total

def expected_dice_sum_dp(k):
    # Using DP to calculate expected value
    MOD = 10**9 + 7
    
    # dp[i] = expected value after i throws
    dp = [0.0] * (k + 1)
    dp[0] = 0  # Base case
    
    for i in range(1, k + 1):
        # For each throw, expected value increases by 3.5
        dp[i] = dp[i-1] + 3.5
    
    return dp[k]

# Example usage
expected = expected_dice_sum(5)
print(f"Expected sum after 5 throws: {expected}")
```

### Variation 5: Variance and Standard Deviation
**Problem**: Find variance and standard deviation of sum after k throws.

```python
def dice_statistics(k):
    # For single throw:
    # Mean = 3.5
    # Variance = E[X²] - (E[X])² = (1²+2²+3²+4²+5²+6²)/6 - 3.5² = 2.9167
    
    mean_single = 3.5
    variance_single = 2.9167
    
    # For k independent throws:
    mean_total = k * mean_single
    variance_total = k * variance_single
    std_dev_total = variance_total ** 0.5
    
    return {
        'mean': mean_total,
        'variance': variance_total,
        'std_dev': std_dev_total
    }

# Example usage
stats = dice_statistics(10)
print(f"After 10 throws:")
print(f"Mean: {stats['mean']}")
print(f"Variance: {stats['variance']}")
print(f"Standard Deviation: {stats['std_dev']}")
```

## 🔗 Related Problems

- **[Coin Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar counting problems
- **[Minimizing Coins](/cses-analyses/problem_soulutions/dynamic_programming/)**: Optimization problems
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/)**: Sum-related problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for counting problems
2. **State Transitions**: Important for DP formulation
3. **Modular Arithmetic**: Important for handling large numbers
4. **Combinatorics**: Important for understanding counting

---

**This is a great introduction to dynamic programming for counting problems!** 🎯

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(6^n) | O(n) | Try all combinations |
| Memoization | O(n) | O(n) | Store subproblem results |
| Bottom-Up DP | O(n) | O(n) | Build solution iteratively |
| Optimized DP | O(n) | O(1) | Use sliding window |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Dynamic Programming**: Build solutions from smaller subproblems
- **Dice Problems**: Classic DP problem with optimal substructure
- **Sliding Window**: Optimize space complexity for rolling calculations
- **Modular Arithmetic**: Handle large numbers with modulo operations

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Dice Combinations with Different Dice**
```python
def dice_combinations_custom_dice(n, dice_values):
    # Handle dice combinations with custom dice values
    
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case
    
    for i in range(1, n + 1):
        for dice in dice_values:
            if i >= dice:
                dp[i] = (dp[i] + dp[i - dice]) % MOD
    
    return dp[n]
```

#### **2. Dice Combinations with Minimum Throws**
```python
def dice_combinations_minimum_throws(n):
    # Handle dice combinations with minimum number of throws
    
    MOD = 10**9 + 7
    
    # dp[i] = number of ways to make sum i with minimum throws
    dp = [0] * (n + 1)
    min_throws = [float('inf')] * (n + 1)
    
    dp[0] = 1
    min_throws[0] = 0
    
    for i in range(1, n + 1):
        for dice in range(1, 7):
            if i >= dice:
                if min_throws[i - dice] + 1 < min_throws[i]:
                    min_throws[i] = min_throws[i - dice] + 1
                    dp[i] = dp[i - dice]
                elif min_throws[i - dice] + 1 == min_throws[i]:
                    dp[i] = (dp[i] + dp[i - dice]) % MOD
    
    return dp[n] if min_throws[n] != float('inf') else 0
```

#### **3. Dice Combinations with Dynamic Updates**
```python
def dice_combinations_dynamic(operations):
    # Handle dice combinations with dynamic dice updates
    
    dice_values = [1, 2, 3, 4, 5, 6]
    n = 0
    dp = [0] * (10**6 + 1)
    dp[0] = 1
    MOD = 10**9 + 7
    
    for operation in operations:
        if operation[0] == 'add_dice':
            # Add new dice value
            dice = operation[1]
            dice_values.append(dice)
            
            # Update DP array
            for i in range(dice, n + 1):
                dp[i] = (dp[i] + dp[i - dice]) % MOD
        
        elif operation[0] == 'set_target':
            # Set target sum
            n = operation[1]
            
            # Recalculate DP array
            dp = [0] * (n + 1)
            dp[0] = 1
            
            for dice in dice_values:
                for i in range(dice, n + 1):
                    dp[i] = (dp[i] + dp[i - dice]) % MOD
        
        elif operation[0] == 'query':
            # Return current number of ways
            yield dp[n] if n < len(dp) else 0
    
    return list(dice_combinations_dynamic(operations))
```

## 🔗 Related Problems

### Links to Similar Problems
- **Dynamic Programming**: Coin change, knapsack problems
- **Counting Problems**: Ways to make sums, combinations
- **Optimization**: Minimum throws, maximum value
- **Combinatorics**: Permutations and combinations

## 📚 Learning Points

### Key Takeaways
- **Dynamic programming** is essential for counting problems
- **Sliding window** can optimize space complexity
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
    for choice in choices: if i >= 
choice: dp[i] = (dp[i] + dp[i - choice]) % MOD
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
            print(f"Current sum: {current_sum}, 
Throws: {throws}")
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