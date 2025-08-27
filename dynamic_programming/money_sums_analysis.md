# CSES Money Sums - Problem Analysis

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