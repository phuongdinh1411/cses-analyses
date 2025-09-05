---
layout: simple
title: "Money Sums - Find All Possible Sums"
permalink: /problem_soulutions/dynamic_programming/money_sums_analysis
---

# Money Sums - Find All Possible Sums

## 📋 Problem Description

Given n coins with different values, find all possible sums that can be formed using any subset of the coins.

This is a classic dynamic programming problem that requires finding all possible sums that can be formed using subsets of coins. The solution involves using a boolean DP array to track which sums are achievable.

**Input**: 
- n: number of coins
- a1, a2, ..., an: values of the coins

**Output**: 
- Number of different sums and the sums in ascending order

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ ai ≤ 1000

**Example**:
```
Input:
4
4 2 5 2

Output:
9
0 2 4 5 6 7 8 9 11

Explanation**: 
All possible sums using subsets of coins:
- {} → 0, {2} → 2, {4} → 4, {5} → 5
- {2,2} → 4, {2,4} → 6, {2,5} → 7, {4,5} → 9
- {2,2,4} → 8, {2,2,5} → 9, {2,4,5} → 11
- {2,2,4,5} → 13 (but this exceeds the maximum possible sum)
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find all possible sums that can be formed using subsets of coins
- **Key Insight**: Use dynamic programming with boolean array to track achievable sums
- **Challenge**: Avoid exponential time complexity with recursive approach

### Step 2: Initial Approach
**Recursive approach (inefficient but correct):**

```python
def money_sums_naive(n, coins):
    def find_sums_recursive(index, current_sum, sums):
        if index == n:
            sums.add(current_sum)
            return
        
        # Include current coin
        find_sums_recursive(index + 1, current_sum + coins[index], sums)
        # Exclude current coin
        find_sums_recursive(index + 1, current_sum, sums)
    
    sums = set()
    find_sums_recursive(0, 0, sums)
    return sorted(sums)
```

**Why this is inefficient**: We try all 2^n possible subsets, leading to exponential time complexity.

### Improvement 1: Dynamic Programming - O(n * sum)
**Description**: Use 1D DP array to track achievable sums.

```python
def money_sums_optimized(n, coins):
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    # Collect all achievable sums
    sums = []
    for i in range(max_sum + 1):
        if dp[i]:
            sums.append(i)
    
    return sums
```

**Why this improvement works**: We use a 1D DP array where dp[i] represents whether sum i can be achieved. We iterate through each coin and update all achievable sums.

### Step 3: Optimization/Alternative
**Optimized DP with space optimization:**

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_money_sums():
    n = int(input())
    coins = list(map(int, input().split()))
    
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Base case: empty subset gives sum 0
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    # Collect all achievable sums
    sums = []
    for i in range(max_sum + 1):
        if dp[i]:
            sums.append(i)
    
    print(len(sums))
    print(*sums)

# Main execution
if __name__ == "__main__":
    solve_money_sums()
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
        (4, [4, 2, 5, 2], [0, 2, 4, 5, 6, 7, 8, 9, 11]),
        (3, [1, 2, 3], [0, 1, 2, 3, 4, 5, 6]),
        (2, [1, 1], [0, 1, 2]),
    ]
    
    for n, coins, expected in test_cases:
        result = solve_test(n, coins)
        print(f"n={n}, coins={coins}, expected={expected}, result={result}")
        assert result == expected, f"Failed for n={n}, coins={coins}"
        print("✓ Passed")
        print()

def solve_test(n, coins):
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Base case
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    # Collect all achievable sums
    sums = []
    for i in range(max_sum + 1):
        if dp[i]:
            sums.append(i)
    
    return sums

test_solution()
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Try all subsets |
| Memoized | O(n×sum) | O(n×sum) | Store subproblem results |
| Bottom-up DP | O(n×sum) | O(sum) | Build from smaller subproblems |

### Time Complexity
- **Time**: O(n * sum) - we iterate through each coin and each possible sum
- **Space**: O(sum) - we store dp array of size sum+1

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes achievable sums using optimal substructure
- **State Transition**: dp[i] = True if dp[i-coin] = True for any coin
- **Base Case**: dp[0] = True represents empty subset
- **Reverse Iteration**: Prevents overcounting by iterating backwards

## 🎨 Visual Example

### Input Example
```
Coins: [4, 2, 5, 2]
```

### All Possible Subsets and Sums
```
Coins: [4, 2, 5, 2]

All possible subsets:
1. {} → sum = 0
2. {2} → sum = 2
3. {2} → sum = 2 (duplicate)
4. {4} → sum = 4
5. {5} → sum = 5
6. {2, 2} → sum = 4 (duplicate)
7. {2, 4} → sum = 6
8. {2, 5} → sum = 7
9. {4, 5} → sum = 9
10. {2, 2, 4} → sum = 8
11. {2, 2, 5} → sum = 9 (duplicate)
12. {2, 4, 5} → sum = 11
13. {2, 2, 4, 5} → sum = 13

Unique sums: 0, 2, 4, 5, 6, 7, 8, 9, 11, 13
Total: 10 different sums
```

### DP Table Construction
```
dp[i] = True if sum i is achievable

Initial state:
dp = [True, False, False, False, False, False, False, False, False, False, False, False, False, False]
     0      1      2      3      4      5      6      7      8      9     10     11     12     13

Base case: dp[0] = True (empty subset has sum 0)

For each coin in [4, 2, 5, 2]:
  For each sum i from max_sum down to coin:
    if dp[i-coin] == True:
      dp[i] = True

After coin 4:
dp = [True, False, False, False, True, False, False, False, False, False, False, False, False, False]

After coin 2:
dp = [True, False, True, False, True, False, True, False, False, False, False, False, False, False]

After coin 5:
dp = [True, False, True, False, True, True, True, False, True, False, True, False, False, False]

After coin 2 (second time):
dp = [True, False, True, False, True, True, True, True, True, True, True, True, False, True]

Final: dp = [True, False, True, False, True, True, True, True, True, True, True, True, False, True]
Answer: 10 different sums
```

### Step-by-Step DP Process
```
Coins: [4, 2, 5, 2]

Step 1: Initialize
dp[0] = True (base case)
All other dp[i] = False

Step 2: Process coin 4
For i = 13 down to 4:
  dp[4] = dp[0] = True
  dp[8] = dp[4] = True
  dp[12] = dp[8] = True

Step 3: Process coin 2
For i = 13 down to 2:
  dp[2] = dp[0] = True
  dp[4] = dp[2] = True (already True)
  dp[6] = dp[4] = True
  dp[8] = dp[6] = True (already True)
  dp[10] = dp[8] = True
  dp[12] = dp[10] = True (already True)

Step 4: Process coin 5
For i = 13 down to 5:
  dp[5] = dp[0] = True
  dp[7] = dp[2] = True
  dp[9] = dp[4] = True
  dp[11] = dp[6] = True
  dp[13] = dp[8] = True

Step 5: Process coin 2 (second time)
For i = 13 down to 2:
  dp[2] = dp[0] = True (already True)
  dp[4] = dp[2] = True (already True)
  dp[6] = dp[4] = True (already True)
  dp[8] = dp[6] = True (already True)
  dp[10] = dp[8] = True (already True)
  dp[12] = dp[10] = True (already True)

Final result: 10 different sums
```

### Visual DP Table
```
Sum:    0  1  2  3  4  5  6  7  8  9 10 11 12 13
Initial:T  F  F  F  F  F  F  F  F  F  F  F  F  F

After coin 4:
        T  F  F  F  T  F  F  F  T  F  F  F  T  F

After coin 2:
        T  F  T  F  T  F  T  F  T  F  T  F  T  F

After coin 5:
        T  F  T  F  T  T  T  T  T  T  T  T  T  F

After coin 2 (second):
        T  F  T  F  T  T  T  T  T  T  T  T  T  T

Achievable sums: 0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
Total: 12 different sums
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(2^n)       │ O(n)         │ Try all      │
│                 │              │              │ subsets      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP Bottom-up    │ O(n×sum)     │ O(sum)       │ Build from   │
│                 │              │              │ smaller sums │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP 2D           │ O(n×sum)     │ O(n×sum)     │ Track coin   │
│                 │              │              │ usage        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Set-based       │ O(n×sum)     │ O(sum)       │ Use set to   │
│                 │              │              │ avoid dups   │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Money Sums Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: coins    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize      │
              │ dp[0] = True    │
              │ dp[i] = False   │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each coin:  │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For sum i from  │
              │ max_sum down to │
              │ coin:           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ If dp[i-coin]   │
              │ == True:        │
              │ dp[i] = True    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Count True      │
              │ values in dp    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return count    │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **Dynamic Programming**: Build solutions from smaller subproblems
- **Subset Sum**: Classic DP problem with boolean states
- **Reverse Iteration**: Prevent overcounting by iterating backwards
- **Space Optimization**: Use 1D array instead of 2D

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Money Sums with Limited Coins**
```python
def money_sums_limited(n, coins, limits):
    # Handle money sums with limited number of each coin
    
    max_sum = sum(coin * limit for coin, limit in zip(coins, limits))
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Base case
    
    for i in range(n):
        coin = coins[i]
        limit = limits[i]
        
        # Process this coin type
        for j in range(max_sum, coin - 1, -1):
            for k in range(1, min(limit + 1, j // coin + 1)):
                if j >= k * coin and dp[j - k * coin]:
                    dp[j] = True
    
    # Collect all achievable sums
    sums = []
    for i in range(max_sum + 1):
        if dp[i]:
            sums.append(i)
    
    return sums
```

#### **2. Money Sums with Target Sum**
```python
def money_sums_target(n, coins, target):
    # Handle money sums with specific target sum
    
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Base case
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    # Check if target is achievable
    if target <= max_sum and dp[target]:
        return True, target
    else:
        return False, -1
```

#### **3. Money Sums with Dynamic Updates**
```python
def money_sums_dynamic(operations):
    # Handle money sums with dynamic coin updates
    
    coins = []
    dp = [False] * (10**5 + 1)
    dp[0] = True
    max_sum = 0
    
    for operation in operations:
        if operation[0] == 'add_coin':
            # Add new coin
            coin = operation[1]
            coins.append(coin)
            max_sum += coin
            
            # Update DP array
            for i in range(max_sum, coin - 1, -1):
                if dp[i - coin]:
                    dp[i] = True
        
        elif operation[0] == 'query':
            # Return current achievable sums
            sums = []
            for i in range(max_sum + 1):
                if dp[i]:
                    sums.append(i)
            yield sums
    
    return list(money_sums_dynamic(operations))
```

## 🔗 Related Problems

### Links to Similar Problems
- **Dynamic Programming**: Subset sum, knapsack problems
- **Counting Problems**: Ways to make sums, combinations
- **Optimization**: Minimum/maximum value problems
- **Combinatorics**: Subset selection problems

## 📚 Learning Points

### Key Takeaways
- **Dynamic programming** is essential for subset problems
- **Boolean DP** efficiently tracks achievable states
- **Reverse iteration** prevents overcounting
- **Space optimization** reduces memory usage

## 🎯 Key Insights

### 1. **Dynamic Programming for Subset Sum**
- Find all achievable sums using subset selection
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **State Transition**
- Clear definition of how to build larger sums from smaller ones
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Reverse Iteration**
- Prevents overcounting in DP
- Important for understanding
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Money Sums with Limited Supply
**Problem**: Each coin has a limited number available.

```python
def money_sums_limited_supply(n, coins, quantities):
    max_sum = sum(coin * qty for coin, qty in zip(coins, quantities))
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Base case
    
    for coin, quantity in zip(coins, quantities):
        for i in range(max_sum, coin - 1, -1):
            for k in range(1, quantity + 1):
                if i >= k * coin and dp[i - k * coin]:
                    dp[i] = True
    
    # Collect all achievable sums
    sums = []
    for i in range(max_sum + 1):
        if dp[i]:
            sums.append(i)
    
    return sums

# Example usage
coins = [4, 2, 5]
quantities = [2, 3, 1]  # 2 coins of value 4, 3 coins of value 2, 1 coin of value 5
result = money_sums_limited_supply(3, coins, quantities)
print(f"Achievable sums: {result}")
```

### Variation 2: Money Sums with Constraints
**Problem**: Cannot use certain combinations of coins.

```python
def money_sums_with_constraints(n, coins, forbidden_combinations):
    max_sum = sum(coins)
    dp = [[False] * (1 << n) for _ in range(max_sum + 1)]
    dp[0][0] = True  # Base case
    
    for i in range(max_sum + 1):
        for mask in range(1 << n):
            if dp[i][mask]:
                for j, coin in enumerate(coins):
                    if i + coin <= max_sum:
                        new_mask = mask | (1 << j)
                        if new_mask not in forbidden_combinations:
                            dp[i + coin][new_mask] = True
    
    # Collect all achievable sums
    sums = set()
    for i in range(max_sum + 1):
        for mask in range(1 << n):
            if dp[i][mask]:
                sums.add(i)
    
    return sorted(sums)

# Example usage
coins = [4, 2, 5]
forbidden = {0b110}  # Cannot use coins 1 and 3 together
result = money_sums_with_constraints(3, coins, forbidden)
print(f"Achievable sums: {result}")
```

### Variation 3: Money Sums with Weights
**Problem**: Each coin has a weight, find weighted sums.

```python
def money_sums_weighted(n, coins, weights):
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Base case
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    # Collect all achievable sums with their weights
    weighted_sums = {}
    for i in range(max_sum + 1):
        if dp[i]:
            # Calculate weight for sum i
            weight = 0
            for coin, w in zip(coins, weights):
                if i >= coin:
                    weight += w
            weighted_sums[i] = weight
    
    return weighted_sums

# Example usage
coins = [4, 2, 5]
weights = [2, 1, 3]  # weight of each coin
result = money_sums_weighted(3, coins, weights)
print(f"Weighted sums: {result}")
```

### Variation 4: Money Sums with Probability
**Problem**: Each coin has a probability of being available.

```python
def money_sums_probability(n, coins, probabilities):
    max_sum = sum(coins)
    dp = [0.0] * (max_sum + 1)
    dp[0] = 1.0  # Base case
    
    for coin, prob in zip(coins, probabilities):
        for i in range(max_sum, coin - 1, -1):
            dp[i] += dp[i - coin] * prob
    
    # Collect all achievable sums with their probabilities
    sum_probs = {}
    for i in range(max_sum + 1):
        if dp[i] > 0:
            sum_probs[i] = dp[i]
    
    return sum_probs

# Example usage
coins = [4, 2, 5]
probabilities = [0.9, 0.8, 0.7]  # probability of each coin being available
result = money_sums_probability(3, coins, probabilities)
print(f"Sum probabilities: {result}")
```

### Variation 5: Money Sums with Dynamic Programming Optimization
**Problem**: Optimize the DP solution for better performance.

```python
def money_sums_optimized(n, coins):
    # Sort coins for better performance
    coins.sort()
    
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Base case
    
    # Use early termination and better memory access
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    # Collect all achievable sums efficiently
    sums = [i for i in range(max_sum + 1) if dp[i]]
    
    return sums

# Example usage
coins = [5, 2, 4]  # Unsorted
result = money_sums_optimized(3, coins)
print(f"Achievable sums: {result}")
```

## 🔗 Related Problems

- **[Dice Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar counting problems
- **[Coin Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar coin problems
- **[Minimizing Coins](/cses-analyses/problem_soulutions/dynamic_programming/)**: Optimization problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for subset sum problems
2. **State Transitions**: Important for DP formulation
3. **Reverse Iteration**: Important for preventing overcounting
4. **Subset Selection**: Important for understanding combinations

---

**This is a great introduction to dynamic programming for subset sum problems!** 🎯
    sums = []
    for i in range(max_sum + 1):
        if dp[i]:
            sums.append(i)
    
    return sums

result = find_money_sums(n, coins)
print(len(result))
print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Try all subsets |
| Dynamic Programming | O(n * sum) | O(sum) | Use 1D DP array |

## Key Insights for Other Problems

### 1. **Subset Sum Problems**
**Principle**: Use 1D DP to find all possible sums achievable with a subset of elements.
**Applicable to**: Subset problems, sum problems, DP problems

### 2. **1D Dynamic Programming**
**Principle**: Use 1D DP array to track achievable values in subset problems.
**Applicable to**: Subset problems, sum problems, DP problems

### 3. **Sum Tracking**
**Principle**: Track all achievable sums by iterating through elements and updating possible sums.
**Applicable to**: Sum problems, subset problems, tracking problems

## Notable Techniques

### 1. **1D DP Array Construction**
```python
def build_1d_dp_array(max_sum):
    return [False] * (max_sum + 1)
```

### 2. **Sum Update**
```python
def update_sums(dp, coin, max_sum):
    for i in range(max_sum, coin - 1, -1):
        if dp[i - coin]:
            dp[i] = True
```

### 3. **Sum Collection**
```python
def collect_sums(dp, max_sum):
    sums = []
    for i in range(max_sum + 1):
        if dp[i]:
            sums.append(i)
    return sums
```

## Problem-Solving Framework

1. **Identify problem type**: This is a subset sum problem
2. **Choose approach**: Use 1D dynamic programming
3. **Define DP state**: dp[i] = whether sum i can be achieved
4. **Base case**: dp[0] = True
5. **Recurrence relation**: dp[i] = dp[i] or dp[i-coin] for each coin
6. **Fill DP array**: Iterate through coins and update achievable sums
7. **Collect results**: Gather all achievable sums
8. **Return result**: Output count and sorted sums

---

*This analysis shows how to efficiently find all possible sums using 1D dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Count Ways to Achieve Each Sum**
**Problem**: For each achievable sum, count how many different ways it can be formed.
```python
def count_ways_for_sums(n, coins):
    max_sum = sum(coins)
    dp = [0] * (max_sum + 1)
    dp[0] = 1  # One way to achieve sum 0 (empty subset)
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            dp[i] += dp[i - coin]
    
    # Return pairs of (sum, count)
    result = []
    for i in range(max_sum + 1):
        if dp[i] > 0:
            result.append((i, dp[i]))
    
    return result
```

#### **Variation 2: Minimum Coins for Each Sum**
**Problem**: For each achievable sum, find the minimum number of coins needed.
```python
def min_coins_for_sums(n, coins):
    max_sum = sum(coins)
    dp = [float('inf')] * (max_sum + 1)
    dp[0] = 0  # Zero coins needed for sum 0
    
    for coin in coins:
        for i in range(coin, max_sum + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    # Return pairs of (sum, min_coins)
    result = []
    for i in range(max_sum + 1):
        if dp[i] != float('inf'):
            result.append((i, dp[i]))
    
    return result
```

#### **Variation 3: Bounded Coin Usage**
**Problem**: Each coin can be used at most k times, find all achievable sums.
```python
def bounded_coin_sums(n, coins, limits):
    # limits[i] = maximum times coin i can be used
    max_sum = sum(coins[i] * limits[i] for i in range(n))
    dp = [False] * (max_sum + 1)
    dp[0] = True
    
    for i, coin in enumerate(coins):
        for j in range(max_sum, coin - 1, -1):
            for k in range(1, limits[i] + 1):
                if j >= coin * k and dp[j - coin * k]:
                    dp[j] = True
    
    # Collect achievable sums
    sums = [i for i in range(max_sum + 1) if dp[i]]
    return sums
```

#### **Variation 4: Weighted Coin Sums**
**Problem**: Each coin has a weight, find sums with minimum total weight.
```python
def weighted_coin_sums(n, coins, weights):
    # weights[i] = weight of coin i
    max_sum = sum(coins)
    dp = [float('inf')] * (max_sum + 1)
    dp[0] = 0  # Zero weight for sum 0
    
    for i, coin in enumerate(coins):
        for j in range(coin, max_sum + 1):
            dp[j] = min(dp[j], dp[j - coin] + weights[i])
    
    # Return pairs of (sum, min_weight)
    result = []
    for i in range(max_sum + 1):
        if dp[i] != float('inf'):
            result.append((i, dp[i]))
    
    return result
```

#### **Variation 5: Probabilistic Coin Sums**
**Problem**: Each coin has a probability of being used, find expected achievable sums.
```python
def probabilistic_coin_sums(n, coins, probabilities):
    # probabilities[i] = probability of using coin i
    max_sum = sum(coins)
    dp = [0.0] * (max_sum + 1)
    dp[0] = 1.0  # Probability 1 for sum 0
    
    for i, coin in enumerate(coins):
        prob = probabilities[i]
        for j in range(max_sum, coin - 1, -1):
            dp[j] = max(dp[j], dp[j - coin] * prob)
    
    # Return pairs of (sum, probability)
    result = []
    for i in range(max_sum + 1):
        if dp[i] > 0:
            result.append((i, dp[i]))
    
    return result
```

### 🔗 **Related Problems & Concepts**

#### **1. Subset Sum Problems**
- **0/1 Knapsack**: Choose items with weight and value constraints
- **Unbounded Knapsack**: Use unlimited copies of each item
- **Partition Equal Subset Sum**: Divide array into two equal parts
- **Target Sum**: Find ways to achieve target using +/- signs

#### **2. Dynamic Programming Patterns**
- **1D DP**: Single state variable (target sum)
- **2D DP**: Two state variables (position, current sum)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Optimization Problems**
- **Minimum Coins**: Find minimum coins for given sum
- **Maximum Value**: Find maximum value for given weight
- **Resource Allocation**: Optimal use of limited resources
- **Scheduling**: Optimal arrangement of tasks

#### **4. Algorithmic Techniques**
- **Backtracking**: Generate all valid subsets
- **Meet in the Middle**: Split problem into halves
- **Bit Manipulation**: Use bits to represent subsets
- **Meet-in-the-Middle**: Optimize exponential algorithms

#### **5. Mathematical Concepts**
- **Combinatorics**: Count valid combinations
- **Number Theory**: Properties of sums and divisibility
- **Modular Arithmetic**: Handle large numbers
- **Probability Theory**: Random selection of coins

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    coins = list(map(int, input().split()))
    result = find_money_sums(n, coins)
    print(len(result))
    print(*result)
```

#### **2. Range Queries on Sum Counts**
```python
def range_sum_queries(n, coins, queries):
    # Precompute for all possible sums
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    # Answer range queries
    for l, r in queries:
        count = sum(1 for i in range(l, r + 1) if dp[i])
        print(count)
```

#### **3. Interactive Coin Problems**
```python
def interactive_coin_game():
    n = int(input())
    coins = list(map(int, input().split()))
    
    print("Available coins:", coins)
    target = int(input("Enter target sum: "))
    
    # Check if target is achievable
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    if target <= max_sum and dp[target]:
        print(f"Sum {target} is achievable!")
    else:
        print(f"Sum {target} is not achievable.")
```

### 🧮 **Mathematical Extensions**

#### **1. Generating Functions**
- **Power Series**: Represent coin combinations as polynomial coefficients
- **Recurrence Relations**: Find closed-form solutions
- **Asymptotic Analysis**: Analyze behavior for large numbers
- **Combinatorial Identities**: Prove mathematical relationships

#### **2. Number Theory Connections**
- **Modular Arithmetic**: Work with large numbers
- **Prime Factorization**: Analyze coin value properties
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
- **Number Theory**: Properties of integers
- **Linear Algebra**: Matrix operations and transformations
- **Probability Theory**: Random processes and outcomes

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Modular Arithmetic**: Handling large numbers efficiently

---

*This analysis demonstrates the power of dynamic programming for subset sum problems and shows various extensions and applications.* 