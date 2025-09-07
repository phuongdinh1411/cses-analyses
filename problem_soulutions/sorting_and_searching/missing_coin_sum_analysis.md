---
layout: simple
title: "Missing Coin Sum"
permalink: /problem_soulutions/sorting_and_searching/missing_coin_sum_analysis
---

# Missing Coin Sum

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand coin sum problems and greedy algorithms for finding missing sums
- Apply greedy algorithms with sorting to find the smallest unattainable sum
- Implement efficient coin sum algorithms with O(n log n) time complexity
- Optimize coin sum problems using sorting and greedy selection techniques
- Handle edge cases in coin sum problems (single coin, all coins same value, large sums)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Greedy algorithms, sorting algorithms, coin sum problems, subset sum problems, missing sum problems
- **Data Structures**: Arrays, sorting, sum tracking, coin tracking
- **Mathematical Concepts**: Coin sum theory, subset sum mathematics, greedy mathematics, sum analysis
- **Programming Skills**: Sorting implementation, greedy algorithm implementation, sum calculation, algorithm implementation
- **Related Problems**: Coin Change problems, Subset Sum problems, Greedy algorithm problems

## Problem Description

**Problem**: Given n coins with values a₁, a₂, ..., aₙ, find the smallest sum that cannot be formed using any subset of the coins.

**Input**: 
- First line: n (number of coins)
- Second line: n integers a₁, a₂, ..., aₙ (values of the coins)

**Output**: Smallest sum that cannot be formed.

**Example**:
```
Input:
5
1 2 4 8 16

Output:
32

Explanation: 
Coins: [1, 2, 4, 8, 16]
Possible sums: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
Smallest missing sum: 32
```

## 📊 Visual Example

### Input Coins
```
Coins: [1, 2, 4, 8, 16]
Index:  0  1  2  3  4
```

### Greedy Algorithm Process
```
Step 1: Sort coins (already sorted)
Coins: [1, 2, 4, 8, 16]

Step 2: Process each coin
┌─────────────────────────────────────┐
│ Current sum: 0                      │
│ Can form sums: [0]                  │
└─────────────────────────────────────┘

Coin 1 (value=1): 1 ≤ 0+1 ✓
┌─────────────────────────────────────┐
│ Current sum: 0 + 1 = 1              │
│ Can form sums: [0, 1]               │
└─────────────────────────────────────┘

Coin 2 (value=2): 2 ≤ 1+1 ✓
┌─────────────────────────────────────┐
│ Current sum: 1 + 2 = 3              │
│ Can form sums: [0, 1, 2, 3]         │
└─────────────────────────────────────┘

Coin 3 (value=4): 4 ≤ 3+1 ✓
┌─────────────────────────────────────┐
│ Current sum: 3 + 4 = 7              │
│ Can form sums: [0, 1, 2, 3, 4, 5, 6, 7]│
└─────────────────────────────────────┘

Coin 4 (value=8): 8 ≤ 7+1 ✓
┌─────────────────────────────────────┐
│ Current sum: 7 + 8 = 15             │
│ Can form sums: [0, 1, 2, ..., 15]   │
└─────────────────────────────────────┘

Coin 5 (value=16): 16 ≤ 15+1 ✓
┌─────────────────────────────────────┐
│ Current sum: 15 + 16 = 31           │
│ Can form sums: [0, 1, 2, ..., 31]   │
└─────────────────────────────────────┘

Final result: 31 + 1 = 32
```

### Sum Formation Examples
```
Using coins [1, 2, 4, 8, 16]:

Sum 1: [1]
Sum 2: [2]
Sum 3: [1, 2]
Sum 4: [4]
Sum 5: [1, 4]
Sum 6: [2, 4]
Sum 7: [1, 2, 4]
Sum 8: [8]
...
Sum 31: [1, 2, 4, 8, 16]

Cannot form sum 32 with any combination!
```

### Why Greedy Works
```
Key Insight: If we can form all sums from 0 to current_sum,
             and next coin ≤ current_sum + 1,
             then we can form all sums from 0 to current_sum + next_coin

Proof intuition:
- We can form sums 0 to current_sum
- Adding next coin allows us to form sums next_coin to current_sum + next_coin
- If next_coin ≤ current_sum + 1, there's no gap
- If next_coin > current_sum + 1, then current_sum + 1 is missing
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find all possible sums using coin subsets
- Identify the smallest sum that cannot be formed
- Use any combination of coins (including empty subset)

**Key Observations:**
- Sort coins for greedy approach
- If we can form sums 1 to current_sum, and next coin ≤ current_sum + 1, we can extend range
- If next coin > current_sum + 1, then current_sum + 1 is missing
- Greedy approach works optimally

### Step 2: Brute Force Approach
**Idea**: Use dynamic programming to find all possible sums.

```python
def missing_coin_sum_brute_force(n, coins):
    max_sum = sum(coins)
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Empty subset has sum 0
    
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

**Why this works:**
- Checks all possible coin combinations
- Uses dynamic programming for efficiency
- Guarantees correct answer
- O(n * sum) time complexity

### Step 3: Greedy Optimization
**Idea**: Sort coins and use greedy approach to find the smallest missing sum.

```python
def missing_coin_sum_greedy(n, coins):
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

**Why this is better:**
- O(n log n) time complexity
- Uses greedy insight
- Much more efficient
- Handles large constraints

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_missing_coin_sum():
    n = int(input())
    coins = list(map(int, input().split()))
    
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        # If the current coin is greater than current_sum + 1,
        # then current_sum + 1 cannot be formed
        if coin > current_sum + 1:
            print(current_sum + 1)
            return
        current_sum += coin
    
    print(current_sum + 1)

# Main execution
if __name__ == "__main__":
    solve_missing_coin_sum()
```

**Why this works:**
- Optimal greedy approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (5, [1, 2, 4, 8, 16], 32),
        (3, [1, 2, 4], 8),
        (2, [1, 3], 2),
        (1, [1], 2),
        (4, [1, 1, 1, 1], 5),
    ]
    
    for n, coins, expected in test_cases:
        result = solve_test(n, coins)
        print(f"n={n}, coins={coins}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, coins):
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin
    
    return current_sum + 1

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting + linear scan
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Greedy Strategy**: Sort coins and process in order
- **Range Extension**: If we can form 1 to current_sum, and next coin ≤ current_sum + 1, we can extend to current_sum + coin
- **Gap Detection**: If next coin > current_sum + 1, then current_sum + 1 is missing
- **Optimal Approach**: No better solution possible

## 🎯 Key Insights

### 1. **Greedy Strategy**
- Sort coins in ascending order
- Process coins sequentially
- Extend possible sum range
- Key insight for optimization

### 2. **Range Extension**
- If we can form sums 1 to current_sum
- And next coin ≤ current_sum + 1
- Then we can form sums 1 to current_sum + coin
- Crucial for understanding

### 3. **Gap Detection**
- If next coin > current_sum + 1
- Then current_sum + 1 cannot be formed
- This is the smallest missing sum
- Important for correctness

## 🎯 Problem Variations

### Variation 1: Limited Coin Usage
**Problem**: Each coin can be used at most k times.

```python
def missing_coin_sum_limited_usage(n, coins, k):
    coins.sort()
    current_sum = 0
    
    for coin in coins:
        # Check if we can extend the range with limited usage
        max_extension = coin * k
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += max_extension
    
    return current_sum + 1
```

### Variation 2: Negative Coin Values
**Problem**: Some coins can have negative values.

```python
def missing_coin_sum_negative(n, coins):
    # Separate positive and negative coins
    positive = [c for c in coins if c > 0]
    negative = [c for c in coins if c < 0]
    
    positive.sort()
    negative.sort(reverse=True)  # Sort in descending order
    
    # Find smallest missing positive sum
    current_sum = 0
    for coin in positive:
        if coin > current_sum + 1:
            return current_sum + 1
        current_sum += coin
    
    # Consider negative coins
    min_negative_sum = sum(negative)
    if min_negative_sum < 0:
        # We can form negative sums, so we need to check if 1 can be formed
        if 1 not in positive and abs(min_negative_sum) < 1:
            return 1
    
    return current_sum + 1
```

### Variation 3: Coin Constraints
**Problem**: Some coins cannot be used together.

```python
def missing_coin_sum_with_constraints(n, coins, constraints):
    # constraints[i] = list of coins that cannot be used with coin i
    coins.sort()
    current_sum = 0
    
    for i, coin in enumerate(coins):
        # Check if this coin can be used with previously used coins
        can_use = True
        for j in range(i):
            if j in constraints[i]:
                can_use = False
                break
        
        if can_use:
            if coin > current_sum + 1:
                return current_sum + 1
            current_sum += coin
    
    return current_sum + 1
```

### Variation 4: Dynamic Coin Addition
**Problem**: Support adding new coins dynamically.

```python
class DynamicCoinSum:
    def __init__(self):
        self.coins = []
        self.current_sum = 0
    
    def add_coin(self, coin_value):
        self.coins.append(coin_value)
        self.coins.sort()
        
        # Recalculate current_sum
        self.current_sum = 0
        for coin in self.coins:
            if coin > self.current_sum + 1:
                break
            self.current_sum += coin
        
        return self.get_missing_sum()
    
    def get_missing_sum(self):
        return self.current_sum + 1
    
    def get_coin_count(self):
        return len(self.coins)
```

### Variation 5: Multiple Missing Sums
**Problem**: Find the k smallest missing sums.

```python
def k_smallest_missing_sums(n, coins, k):
    coins.sort()
    current_sum = 0
    missing_sums = []
    
    for coin in coins:
        # Find all missing sums between current_sum + 1 and coin - 1
        for missing in range(current_sum + 1, coin):
            missing_sums.append(missing)
            if len(missing_sums) >= k:
                return missing_sums[:k]
        
        current_sum += coin
    
    # Add remaining missing sums after all coins
    for i in range(k - len(missing_sums)):
        missing_sums.append(current_sum + 1 + i)
    
    return missing_sums[:k]
```

## 🔗 Related Problems

- **[Two Sets](/cses-analyses/problem_soulutions/introductory_problems/two_sets_analysis)**: Subset sum problems
- **[Apple Division](/cses-analyses/problem_soulutions/introductory_problems/apple_division_analysis)**: Partition problems
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/money_sums_analysis)**: Dynamic programming subset sum

## 📚 Learning Points

1. **Greedy Strategy**: Sort and process elements sequentially for optimal results
2. **Range Extension**: Understand how to extend possible ranges efficiently
3. **Gap Detection**: Identify the smallest missing value in a sequence
4. **Subset Sum Problems**: Common pattern in competitive programming

---

**This is a great introduction to greedy algorithms and subset sum problems!** 🎯 