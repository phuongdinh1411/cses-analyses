---
layout: simple
title: "Missing Coin Sum
permalink: /problem_soulutions/sorting_and_searching/missing_coin_sum_analysis/"
---


# Missing Coin Sum

## Problem Statement
Given n coins with values a1,a2,…,an, find the smallest sum that cannot be formed using any subset of the coins.

### Input
The first input line has an integer n: the number of coins.
The second line has n integers a1,a2,…,an: the values of the coins.

### Output
Print one integer: the smallest sum that cannot be formed.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
5
1 2 4 8 16

Output:
32
```

## Solution Progression

### Approach 1: Dynamic Programming - O(n * sum)
**Description**: Use dynamic programming to find all possible sums.

```python
def missing_coin_sum_naive(n, coins):
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True
    
    for coin in coins:
        for i in range(max_sum, coin - 1, -1):
            if dp[i - coin]:
                dp[i] = True
    
    # Find the smallest sum that cannot be formed
    for i in range(1, max_sum + 1):
        if not dp[i]:
            return i
    
    return max_sum + 1
```

**Why this is inefficient**: The time complexity is O(n * sum), which can be very large when the sum of coins is large.

### Improvement 1: Greedy Approach - O(n log n)
**Description**: Sort coins and use greedy approach to find the smallest missing sum.

```python
def missing_coin_sum_optimized(n, coins):
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        # If the current coin is greater than current_sum + 1,
        # then current_sum + 1 cannot be formed
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin
    
    return current_sum + 1
```

**Why this improvement works**: If we can form all sums from 1 to current_sum, and the next coin is at most current_sum + 1, then we can form all sums from 1 to current_sum + coin. If the next coin is greater than current_sum + 1, then current_sum + 1 cannot be formed.

## Final Optimal Solution

```python
n = int(input())
coins = list(map(int, input().split()))

def find_missing_coin_sum(n, coins):
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        # If the current coin is greater than current_sum + 1,
        # then current_sum + 1 cannot be formed
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin
    
    return current_sum + 1

result = find_missing_coin_sum(n, coins)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Dynamic Programming | O(n * sum) | O(sum) | Find all possible sums |
| Greedy | O(n log n) | O(1) | Sort and use greedy approach |

## Key Insights for Other Problems

### 1. **Coin Sum Problems**
**Principle**: Use greedy approach for finding smallest missing sum.
**Applicable to**: Coin problems, subset sum problems, greedy algorithms

### 2. **Greedy Coin Selection**
**Principle**: Sort coins and use greedy approach to determine formable sums.
**Applicable to**: Coin problems, sum problems, greedy algorithms

### 3. **Missing Sum Detection**
**Principle**: Track current formable sum and check if next coin can extend it.
**Applicable to**: Sum problems, missing value problems, range problems

## Notable Techniques

### 1. **Greedy Coin Processing**
```python
def process_coins_greedy(coins):
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin
    
    return current_sum + 1
```

### 2. **Sum Range Tracking**
```python
def track_formable_sums(coins):
    coins.sort()
    formable_range = 0
    
    for coin in coins:
        if coin <= formable_range + 1:
            formable_range += coin
        else:
            break
    
    return formable_range + 1
```

### 3. **Missing Value Detection**
```python
def find_missing_value(sorted_values):
    current_sum = 0
    
    for value in sorted_values:
        if value > current_sum + 1:
            return current_sum + 1
        current_sum += value
    
    return current_sum + 1
```

## Problem-Solving Framework

1. **Identify problem type**: This is a coin sum problem with missing sum detection
2. **Choose approach**: Use greedy approach after sorting
3. **Sort coins**: Sort coins in ascending order
4. **Track formable sum**: Keep track of the largest formable sum
5. **Check next coin**: If next coin is too large, return missing sum
6. **Return result**: Output the smallest missing sum

---

*This analysis shows how to efficiently find the smallest missing coin sum using a greedy approach.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Missing Coin Sum with Limited Coins**
**Problem**: Each coin can be used at most k times.
```python
def missing_coin_sum_limited_usage(n, coins, k):
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        # With k copies of this coin, we can form sums up to k * coin
        max_contribution = k * coin
        
        if coin > current_sum + 1:
            return current_sum + 1
        
        current_sum += max_contribution
    
    return current_sum + 1
```

#### **Variation 2: Missing Coin Sum with Constraints**
**Problem**: Some coins cannot be used together.
```python
def missing_coin_sum_with_constraints(n, coins, constraints):
    # constraints[i] = list of coins that cannot be used with coin i
    coins.sort()
    current_sum = 0
    
    # For each coin, check if it can be used with previously used coins
    used_coins = set()
    
    for i, coin in enumerate(coins):
        # Check if this coin conflicts with any used coin
        can_use = True
        for used_coin in used_coins:
            if used_coin in constraints[i]:
                can_use = False
                break
        
        if can_use:
            if coin > current_sum + 1:
                return current_sum + 1
            current_sum += coin
            used_coins.add(coin)
    
    return current_sum + 1
```

#### **Variation 3: Missing Coin Sum with Weighted Coins**
**Problem**: Each coin has a weight. Find smallest sum that cannot be formed with total weight ≤ W.
```python
def missing_coin_sum_weighted(n, coins, weights, max_weight):
    # Sort coins by value/weight ratio
    coin_data = [(coins[i], weights[i]) for i in range(n)]
    coin_data.sort(key=lambda x: x[0] / x[1], reverse=True)
    
    current_sum = 0
    current_weight = 0
    
    for coin, weight in coin_data:
        if current_weight + weight > max_weight:
            continue
        
        if coin > current_sum + 1:
            return current_sum + 1
        
        current_sum += coin
        current_weight += weight
    
    return current_sum + 1
```

#### **Variation 4: Missing Coin Sum with Dynamic Updates**
**Problem**: Support adding and removing coins dynamically.
```python
class DynamicMissingCoinSum:
    def __init__(self):
        self.coins = []
        self.current_sum = 0
    
    def add_coin(self, coin):
        # Insert coin in sorted order
        import bisect
        pos = bisect.bisect_left(self.coins, coin)
        self.coins.insert(pos, coin)
        
        # Recalculate current_sum
        self.current_sum = 0
        for c in self.coins:
            if c > self.current_sum + 1:
                break
            self.current_sum += c
        
        return self.current_sum + 1
    
    def remove_coin(self, index):
        if 0 <= index < len(self.coins):
            self.coins.pop(index)
            
            # Recalculate current_sum
            self.current_sum = 0
            for coin in self.coins:
                if coin > self.current_sum + 1:
                    break
                self.current_sum += coin
        
        return self.current_sum + 1
    
    def get_missing_sum(self):
        return self.current_sum + 1
```

#### **Variation 5: Missing Coin Sum with Modulo Constraints**
**Problem**: Find smallest sum that cannot be formed modulo m.
```python
def missing_coin_sum_modulo(n, coins, m):
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        if coin > current_sum + 1:
            return (current_sum + 1) % m
        current_sum += coin
    
    return (current_sum + 1) % m
```

### 🔗 **Related Problems & Concepts**

#### **1. Greedy Algorithm Problems**
- **Fractional Knapsack**: Fill knapsack optimally
- **Activity Selection**: Select maximum activities
- **Huffman Coding**: Build optimal prefix codes"
- **Dijkstra's Algorithm**: Find shortest paths

#### **2. Dynamic Programming Problems**
- **Coin Change**: Minimum coins to make amount
- **Subset Sum**: Find subset with given sum
- **Knapsack Problem**: Fill knapsack optimally
- **Partition Problem**: Partition array into equal sums

#### **3. Mathematical Problems**
- **Number Theory**: Properties of numbers
- **Combinatorics**: Counting and arrangement
- **Optimization**: Mathematical optimization
- **Algorithm Analysis**: Complexity and correctness

#### **4. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Integer Programming**: Discrete optimization
- **Combinatorial Optimization**: Optimize discrete structures
- **Approximation Algorithms**: Find approximate solutions

#### **5. Algorithm Problems**
- **Sorting Algorithms**: Various sorting techniques
- **Search Algorithms**: Efficient search techniques
- **Binary Search**: Find optimal solution
- **Greedy Algorithms**: Local optimal choices

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    coins = list(map(int, input().split()))
    
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        if coin > current_sum + 1:
            break
        current_sum += coin
    
    print(current_sum + 1)
```

#### **2. Range Queries**
```python
# Precompute missing coin sums for different subarrays
def precompute_missing_sums(coins):
    n = len(coins)
    missing_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            subarray = coins[i:j+1]
            subarray.sort()
            current_sum = 0
            
            for coin in subarray:
                if coin > current_sum + 1:
                    break
                current_sum += coin
            
            missing_matrix[i][j] = current_sum + 1
    
    return missing_matrix

# Answer queries about missing coin sums for subarrays
def missing_sum_query(missing_matrix, l, r):
    return missing_matrix[l][r]
```

#### **3. Interactive Problems**
```python
# Interactive missing coin sum finder
def interactive_missing_coin_sum():
    n = int(input("Enter number of coins: "))
    coins = list(map(int, input("Enter coin values: ").split()))
    
    print(f"Coins: {coins}")
    
    coins.sort()
    print(f"Sorted coins: {coins}")
    
    current_sum = 0
    print(f"Initial current_sum: {current_sum}")
    
    for i, coin in enumerate(coins):
        print(f"\nProcessing coin {coin} at position {i}")
        
        if coin > current_sum + 1:
            print(f"Coin {coin} > {current_sum + 1}, so {current_sum + 1} cannot be formed")
            break
        
        current_sum += coin
        print(f"Updated current_sum: {current_sum}")
        print(f"Can form all sums from 1 to {current_sum}")
    
    result = current_sum + 1
    print(f"\nSmallest sum that cannot be formed: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Number Theory**
- **Properties of Sums**: Properties of number sums
- **Divisibility**: Properties of divisibility
- **Modular Arithmetic**: Working with remainders
- **Prime Factorization**: Breaking numbers into primes

#### **2. Combinatorics**
- **Subset Sums**: Counting subset sums
- **Partitions**: Number partitions
- **Combinations**: Counting combinations
- **Permutations**: Counting permutations

#### **3. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Greedy Correctness**: Proving greedy choice property
- **Optimal Substructure**: Proving optimal substructure
- **Lower Bounds**: Establishing problem lower bounds

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Greedy Algorithms**: Local optimal choices
- **Dynamic Programming**: Optimal substructure
- **Sorting Algorithms**: Various sorting techniques
- **Binary Search**: Efficient search techniques

#### **2. Mathematical Concepts**
- **Number Theory**: Properties of numbers
- **Combinatorics**: Counting and arrangement
- **Optimization**: Mathematical optimization theory
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Greedy Algorithm Design**: Problem-solving strategies
- **Dynamic Programming**: Optimal substructure
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Performance evaluation

---

*This analysis demonstrates greedy algorithm techniques and shows various extensions for mathematical problems.* 