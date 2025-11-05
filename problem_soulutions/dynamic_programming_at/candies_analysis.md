---
layout: simple
title: "Candies - AtCoder Educational DP Contest Problem M"
permalink: /problem_soulutions/dynamic_programming_at/candies_analysis
---

# Candies - AtCoder Educational DP Contest Problem M

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand DP with constraints
- Apply prefix sum optimization in DP
- Handle cumulative constraints in DP
- Optimize DP transitions with prefix sums

### 📚 **Prerequisites**
- Dynamic Programming, prefix sums, constraint handling
- Arrays, cumulative sums
- Related: Knapsack problems, constraint DP

## 📋 Problem Description

There are N children and K candies. Child i can receive at most a_i candies. Find the number of ways to distribute K candies to N children, modulo 10^9+7.

**Input**: 
- First line: N, K (1 ≤ N ≤ 100, 0 ≤ K ≤ 10^5)
- Second line: a_1, a_2, ..., a_N (0 ≤ a_i ≤ K)

**Output**: 
- Number of ways modulo 10^9+7

**Constraints**:
- 1 ≤ N ≤ 100
- 0 ≤ K ≤ 10^5
- 0 ≤ a_i ≤ K

## 🔍 Solution Analysis

### Approach: DP with Prefix Sum Optimization

**Key Insight**: Use DP with prefix sums to optimize transitions.

**DP State Definition**:
- `dp[i][j]` = number of ways to distribute j candies to first i children
- `dp[0][0] = 1` (base case: 0 children, 0 candies)

**Recurrence Relation**:
- For child i, can give 0 to min(a_i, j) candies
- `dp[i][j] = sum(dp[i-1][j-k])` for k from 0 to min(a_i, j)
- This is O(K) per state, giving O(N*K^2) total

**Optimization with Prefix Sums**:
- Use prefix sums to compute range sums in O(1)
- `prefix[i][j] = sum(dp[i][0] + dp[i][1] + ... + dp[i][j])`
- `dp[i][j] = prefix[i-1][j] - prefix[i-1][j-a_i-1]` (for j > a_i)

**Implementation**:
```python
def candies_dp(n, k, limits):
    """
    DP with prefix sum optimization for Candies problem
    
    Args:
        n: number of children
        k: number of candies
        limits: list of maximum candies per child
    
    Returns:
        int: number of ways modulo 10^9+7
    """
    MOD = 10**9 + 7
    
    # dp[i][j] = ways to distribute j candies to first i children
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        # Build prefix sum for previous row
        prefix = [0] * (k + 1)
        prefix[0] = dp[i - 1][0]
        for j in range(1, k + 1):
            prefix[j] = (prefix[j - 1] + dp[i - 1][j]) % MOD
        
        # Fill current row using prefix sums
        limit = limits[i - 1]
        for j in range(k + 1):
            # Can give 0 to min(limit, j) candies to child i
            # Sum from dp[i-1][j-limit] to dp[i-1][j]
            start = max(0, j - limit)
            if start == 0:
                dp[i][j] = prefix[j]
            else:
                dp[i][j] = (prefix[j] - prefix[start - 1]) % MOD
    
    return dp[n][k]

# Example usage
n, k = 3, 4
limits = [1, 2, 3]
result = candies_dp(n, k, limits)
print(f"Number of ways: {result}")
```

**Time Complexity**: O(N*K)
**Space Complexity**: O(N*K) or O(K) with space optimization

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive DP | O(N*K^2) | O(N*K) | Slow without optimization |
| Prefix Sum DP | O(N*K) | O(N*K) | Optimize transitions |

### Why This Solution Works
- **Prefix Sums**: Compute range sums efficiently
- **Constraint Handling**: Respect individual child limits
- **DP Optimization**: Reduce transition complexity

## 🚀 Related Problems
- Knapsack variants with constraints
- Distribution problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem M](https://atcoder.jp/contests/dp/tasks/dp_m) - Original problem
- Prefix sum optimization techniques

