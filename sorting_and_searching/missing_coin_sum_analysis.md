# CSES Missing Coin Sum - Problem Analysis

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