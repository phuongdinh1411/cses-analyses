---
layout: simple
title: "Money Sums
permalink: /problem_soulutions/dynamic_programming/money_sums_analysis/"
---


# Money Sums

## Problem Statement
Given n coins with values a1,a2,…,an, find all possible sums that can be formed using any subset of the coins.

### Input
The first input line has an integer n: the number of coins.
The second line has n integers a1,a2,…,an: the values of the coins.

### Output
Print the number of different sums and the sums in ascending order.

### Constraints
- 1 ≤ n ≤ 100
- 1 ≤ ai ≤ 1000

### Example
```
Input:
4
4 2 5 2

Output:
9
0 2 4 5 6 7 8 9 11
```

## Solution Progression

### Approach 1: Recursive - O(2^n)
**Description**: Use recursive approach to find all possible sums.

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

## Final Optimal Solution

```python
n = int(input())
coins = list(map(int, input().split()))

def find_money_sums(n, coins):
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
    max_sum = sum(coins)"
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