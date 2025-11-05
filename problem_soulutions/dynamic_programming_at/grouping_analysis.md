---
layout: simple
title: "Grouping - AtCoder Educational DP Contest Problem U"
permalink: /problem_soulutions/dynamic_programming_at/grouping_analysis
---

# Grouping - AtCoder Educational DP Contest Problem U

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand subset DP with bitmask
- Apply DP to solve grouping problems
- Handle subset optimization with bitmask
- Optimize subset DP solutions

### 📚 **Prerequisites**
- Dynamic Programming, bitmask DP, subset DP
- Arrays, bit manipulation
- Related: Subset problems, grouping problems

## 📋 Problem Description

Given N items and a score matrix, partition items into groups. Score increases when items in same group. Find maximum total score.

**Input**: 
- First line: N (1 ≤ N ≤ 16)
- Next N lines: score matrix a[i][j]

**Output**: 
- Maximum total score

**Constraints**:
- 1 ≤ N ≤ 16
- Score matrix given

## 🔍 Solution Analysis

### Approach: Subset DP with Bitmask

**Key Insight**: Use bitmask to represent subsets. For each subset, try all possible partitions.

**DP State Definition**:
- `dp[mask]` = maximum score for subset represented by mask
- Try partitioning mask into two subsets and combine scores

**Recurrence Relation**:
- `dp[mask] = max(dp[submask] + dp[mask ^ submask])` for all non-empty submask ⊆ mask
- Also add score of entire subset as one group

**Implementation**:
```python
def grouping_max_score(n, score_matrix):
    """
    Subset DP solution for Grouping problem
    
    Args:
        n: number of items
        score_matrix: 2D list of scores
    
    Returns:
        int: maximum total score
    """
    # Precompute score for each subset
    subset_score = [0] * (1 << n)
    for mask in range(1 << n):
        score = 0
        for i in range(n):
            if mask & (1 << i):
                for j in range(i + 1, n):
                    if mask & (1 << j):
                        score += score_matrix[i][j]
        subset_score[mask] = score
    
    # dp[mask] = max score for subset mask
    dp = [0] * (1 << n)
    
    for mask in range(1 << n):
        # Try all submasks
        submask = mask
        while submask:
            dp[mask] = max(dp[mask], dp[submask] + dp[mask ^ submask])
            submask = (submask - 1) & mask
        
        # Also consider entire subset as one group
        dp[mask] = max(dp[mask], subset_score[mask])
    
    return dp[(1 << n) - 1]

# Example usage
n = 3
score_matrix = [
    [0, 10, 20],
    [10, 0, 30],
    [20, 30, 0]
]
result = grouping_max_score(n, score_matrix)
print(f"Maximum score: {result}")
```

**Time Complexity**: O(3^N)
**Space Complexity**: O(2^N)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Subset DP | O(3^N) | O(2^N) | Try all partitions |

### Why This Solution Works
- **Subset Enumeration**: Try all possible partitions
- **Optimal Substructure**: Optimal grouping depends on subgroupings
- **Bitmask**: Efficient subset representation

## 🚀 Related Problems
- Subset optimization problems
- Grouping problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem U](https://atcoder.jp/contests/dp/tasks/dp_u) - Original problem
- Subset DP techniques

