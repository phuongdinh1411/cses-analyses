---
layout: simple
title: "Slimes - AtCoder Educational DP Contest Problem N"
permalink: /problem_soulutions/dynamic_programming_at/slimes_analysis
---

# Slimes - AtCoder Educational DP Contest Problem N

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand interval DP for merging problems
- Apply DP to solve minimum cost merging
- Recognize interval DP patterns
- Optimize interval DP computations

### 📚 **Prerequisites**
- Dynamic Programming, interval DP, prefix sums
- Arrays, 2D arrays
- Related: Matrix chain multiplication, interval problems

## 📋 Problem Description

There are N slimes in a line. The i-th slime has size a_i. When two adjacent slimes of sizes x and y merge, they become one slime of size x+y, and the cost is x+y. Find the minimum total cost to merge all slimes into one.

**Input**: 
- First line: N (2 ≤ N ≤ 400)
- Second line: a_1, a_2, ..., a_N (1 ≤ a_i ≤ 10^9)

**Output**: 
- Minimum total cost

**Constraints**:
- 2 ≤ N ≤ 400
- 1 ≤ a_i ≤ 10^9

## 🔍 Solution Analysis

### Approach: Interval DP with Prefix Sums

**Key Insight**: Use interval DP to find optimal merge order. The cost of merging interval [i, j] is the sum of all elements in that interval.

**DP State Definition**:
- `dp[i][j]` = minimum cost to merge slimes from index i to j (inclusive)
- `dp[i][i] = 0` (single slime, no cost)
- Answer: `dp[0][N-1]`

**Recurrence Relation**:
- To merge interval [i, j], we need to split it at some point k
- `dp[i][j] = min(dp[i][k] + dp[k+1][j] + sum(i to j))` for all k in [i, j-1]
- Use prefix sums to compute sum(i to j) in O(1)

**Implementation**:
```python
def slimes_merge(n, sizes):
    """
    Interval DP solution for Slimes problem
    
    Args:
        n: number of slimes
        sizes: list of slime sizes
    
    Returns:
        int: minimum total cost
    """
    # Prefix sums for efficient range sum queries
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + sizes[i]
    
    # dp[i][j] = min cost to merge slimes [i, j]
    dp = [[0] * n for _ in range(n)]
    
    # Fill DP for intervals of increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            
            # Try all possible split points
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + (prefix[j + 1] - prefix[i])
                dp[i][j] = min(dp[i][j], cost)
    
    return dp[0][n - 1]

# Example usage
n = 4
sizes = [10, 20, 30, 40]
result = slimes_merge(n, sizes)
print(f"Minimum cost: {result}")
```

**Time Complexity**: O(N^3)
**Space Complexity**: O(N^2)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Interval DP | O(N^3) | O(N^2) | Optimal merge order |

### Why This Solution Works
- **Optimal Substructure**: Optimal merge of [i,j] depends on optimal merges of subintervals
- **Interval DP**: Build solution from smaller intervals
- **Prefix Sums**: Efficient range sum computation

## 🚀 Related Problems
- Matrix Chain Multiplication - Similar structure
- [Removal Game](https://cses.fi/problemset/task/1097) - Similar interval DP

## 🔗 Additional Resources
- [AtCoder DP Contest Problem N](https://atcoder.jp/contests/dp/tasks/dp_n) - Original problem
- Interval DP techniques

