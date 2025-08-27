# CSES Two Sets II - Problem Analysis

## Problem Statement
Given a number n, find the number of ways to divide the numbers 1,2,…,n into two sets with equal sums.

### Input
The first input line has an integer n.

### Output
Print the number of ways modulo 10^9+7.

### Constraints
- 1 ≤ n ≤ 500

### Example
```
Input:
7

Output:
4
```

## Solution Progression

### Approach 1: Recursive - O(2^n)
**Description**: Use recursive approach to find all valid partitions.

```python
def two_sets_ii_naive(n):
    def count_partitions(index, sum1, sum2):
        if index == n + 1:
            return 1 if sum1 == sum2 else 0
        
        # Put current number in first set
        ways1 = count_partitions(index + 1, sum1 + index, sum2)
        # Put current number in second set
        ways2 = count_partitions(index + 1, sum1, sum2 + index)
        
        return ways1 + ways2
    
    return count_partitions(1, 0, 0)
```

**Why this is inefficient**: We try all 2^n possible partitions, leading to exponential time complexity.

### Improvement 1: Dynamic Programming - O(n * sum)
**Description**: Use 1D DP array to count ways to achieve target sum.

```python
def two_sets_ii_optimized(n):
    total_sum = n * (n + 1) // 2
    
    # If total sum is odd, no valid partition exists
    if total_sum % 2 != 0:
        return 0
    
    target = total_sum // 2
    MOD = 10**9 + 7
    
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for i in range(1, n + 1):
        for j in range(target, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % MOD
    
    return dp[target]
```

**Why this improvement works**: We use a 1D DP array where dp[i] represents the number of ways to achieve sum i. We iterate through each number and update the ways to achieve each possible sum.

## Final Optimal Solution

```python
n = int(input())

def find_two_sets_ways(n):
    total_sum = n * (n + 1) // 2
    
    # If total sum is odd, no valid partition exists
    if total_sum % 2 != 0:
        return 0
    
    target = total_sum // 2
    MOD = 10**9 + 7
    
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for i in range(1, n + 1):
        for j in range(target, i - 1, -1):
            dp[j] = (dp[j] + dp[j - i]) % MOD
    
    return dp[target]

result = find_two_sets_ways(n)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Try all partitions |
| Dynamic Programming | O(n * sum) | O(sum) | Use 1D DP array |

## Key Insights for Other Problems

### 1. **Partition Problems**
**Principle**: Use 1D DP to count ways to partition elements into sets with equal sums.
**Applicable to**: Partition problems, counting problems, DP problems

### 2. **1D Dynamic Programming**
**Principle**: Use 1D DP array to count ways to achieve target values in partition problems.
**Applicable to**: Partition problems, counting problems, DP problems

### 3. **Equal Sum Partitioning**
**Principle**: Find ways to partition elements so that both sets have equal sums.
**Applicable to**: Partition problems, sum problems, counting problems

## Notable Techniques

### 1. **1D DP Array Construction**
```python
def build_1d_dp_array(target):
    return [0] * (target + 1)
```

### 2. **Sum Update**
```python
def update_ways(dp, num, target, MOD):
    for j in range(target, num - 1, -1):
        dp[j] = (dp[j] + dp[j - num]) % MOD
```

### 3. **Target Calculation**
```python
def calculate_target(n):
    total_sum = n * (n + 1) // 2
    return total_sum // 2 if total_sum % 2 == 0 else -1
```

## Problem-Solving Framework

1. **Identify problem type**: This is a partition counting problem
2. **Choose approach**: Use 1D dynamic programming
3. **Calculate target**: Target sum = total_sum // 2
4. **Check feasibility**: Return 0 if total sum is odd
5. **Define DP state**: dp[i] = ways to achieve sum i
6. **Base case**: dp[0] = 1
7. **Recurrence relation**: dp[j] += dp[j - i] for each number i
8. **Return result**: Output dp[target] modulo 10^9+7

---

*This analysis shows how to efficiently count ways to partition numbers into two equal-sum sets using 1D dynamic programming.* 