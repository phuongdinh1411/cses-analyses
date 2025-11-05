---
layout: simple
title: "Matching"
permalink: /problem_soulutions/dynamic_programming_at/matching_analysis
---

# Matching

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand bitmask DP
- Apply DP to solve matching/assignment problems
- Recognize when to use bitmask DP
- Optimize bitmask DP solutions

## 📋 Problem Description

There are N men and N women. For each pair (i, j), there is a compatibility value a[i][j]. Find the number of ways to match each man with a woman such that all pairs are compatible, modulo 10^9+7.

**Input**: 
- First line: N (1 ≤ N ≤ 21)
- Next N lines: N integers a[i][j] (0 or 1)

**Output**: 
- Number of matchings modulo 10^9+7

**Constraints**:
- 1 ≤ N ≤ 21
- a[i][j] is 0 or 1

## 🔍 Solution Analysis

### Approach: Bitmask DP

**Key Insight**: Use bitmask to represent which women have been matched. Match men one by one.

**DP State Definition**:
- `dp[mask]` = number of ways to match first popcount(mask) men with women represented by mask
- `mask` is a bitmask where bit j is set if woman j is matched
- Answer: `dp[(1 << N) - 1]` (all women matched)

**Recurrence Relation**:
- For man i (i = popcount(mask)), try matching with each unmatched woman j
- `dp[mask | (1 << j)] += dp[mask]` if a[i][j] == 1

**Implementation**:
```python
def matching_count(n, compatibility):
    """
    Bitmask DP solution for Matching problem
    
    Args:
        n: number of men/women
        compatibility: 2D list, compatibility[i][j] = 1 if compatible
    
    Returns:
        int: number of matchings modulo 10^9+7
    """
    MOD = 10**9 + 7
    
    # dp[mask] = ways to match first popcount(mask) men with women in mask
    dp = [0] * (1 << n)
    dp[0] = 1  # Base case: no matches yet
    
    # Process each mask
    for mask in range(1 << n):
        # Current man index = number of matched women
        man_idx = bin(mask).count('1')
        
        if man_idx >= n:
            continue
        
        # Try matching current man with each unmatched woman
        for woman in range(n):
            if (mask >> woman) & 1:  # Already matched
                continue
            
            if compatibility[man_idx][woman] == 1:
                new_mask = mask | (1 << woman)
                dp[new_mask] = (dp[new_mask] + dp[mask]) % MOD
    
    return dp[(1 << n) - 1]

# Example usage
n = 3
compatibility = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
result = matching_count(n, compatibility)
print(f"Number of matchings: {result}")
```

**Time Complexity**: O(N * 2^N)
**Space Complexity**: O(2^N)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bitmask DP | O(N * 2^N) | O(2^N) | Represent state with bitmask |

### Why This Solution Works
- **State Compression**: Bitmask represents subset of matched women
- **Optimal Substructure**: Matching depends on previous matchings
- **DP Optimization**: Avoid recomputing same states

## 🚀 Related Problems
- Assignment problems
- Bipartite matching variants
- Subset DP problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem O](https://atcoder.jp/contests/dp/tasks/dp_o) - Original problem
- Bitmask DP techniques

