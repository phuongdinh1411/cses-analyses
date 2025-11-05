---
layout: simple
title: "Permutation - AtCoder Educational DP Contest Problem T"
permalink: /problem_soulutions/dynamic_programming_at/permutation_analysis
---

# Permutation - AtCoder Educational DP Contest Problem T

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand DP with insertion technique
- Apply DP to solve permutation problems
- Handle relative ordering constraints
- Recognize insertion DP patterns

### 📚 **Prerequisites**
- Dynamic Programming, combinatorics, insertion DP
- Arrays, 2D arrays
- Related: Permutation problems, ordering constraints

## 📋 Problem Description

Given a string S of length N-1 with '<' and '>', count permutations P of [1, 2, ..., N] such that P[i] < P[i+1] if S[i] == '<', and P[i] > P[i+1] if S[i] == '>'.

**Input**: 
- First line: N (2 ≤ N ≤ 3000)
- Second line: S (string of length N-1)

**Output**: 
- Count modulo 10^9+7

**Constraints**:
- 2 ≤ N ≤ 3000
- S contains only '<' and '>'

## 🔍 Solution Analysis

### Approach: Insertion DP

**Key Insight**: Build permutation by inserting numbers one by one, tracking relative positions.

**DP State Definition**:
- `dp[i][j]` = number of valid permutations of first i numbers ending with j-th smallest among inserted numbers
- `dp[1][0] = 1` (base case: one number)

**Recurrence Relation**:
- If S[i-1] == '<': `dp[i][j] = sum(dp[i-1][k])` for k < j
- If S[i-1] == '>': `dp[i][j] = sum(dp[i-1][k])` for k >= j
- Use prefix sums for optimization

**Implementation**:
```python
def permutation_count(n, s):
    """
    Insertion DP solution for Permutation problem
    
    Args:
        n: length of permutation
        s: string of constraints
    
    Returns:
        int: count modulo 10^9+7
    """
    MOD = 10**9 + 7
    
    # dp[i][j] = valid permutations of first i numbers ending with j-th smallest
    dp = [[0] * n for _ in range(n + 1)]
    dp[1][0] = 1
    
    for i in range(2, n + 1):
        # Build prefix sums
        prefix = [0] * i
        prefix[0] = dp[i-1][0]
        for j in range(1, i-1):
            prefix[j] = (prefix[j-1] + dp[i-1][j]) % MOD
        
        for j in range(i):
            if s[i-2] == '<':
                # Previous number must be smaller (j-th smallest)
                # Sum all positions < j
                dp[i][j] = prefix[j-1] if j > 0 else 0
            else:  # '>'
                # Previous number must be larger (j-th smallest or larger)
                # Sum all positions >= j
                if j == 0:
                    dp[i][j] = prefix[i-2]
                else:
                    dp[i][j] = (prefix[i-2] - prefix[j-1]) % MOD
    
    return sum(dp[n]) % MOD

# Example usage
n = 4
s = "<><"
result = permutation_count(n, s)
print(f"Count: {result}")
```

**Time Complexity**: O(N^2)
**Space Complexity**: O(N^2)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Insertion DP | O(N^2) | O(N^2) | Build permutation incrementally |

### Why This Solution Works
- **Insertion Technique**: Add numbers one by one
- **Relative Positions**: Track position among inserted numbers
- **Prefix Sums**: Optimize range sum queries

## 🚀 Related Problems
- Permutation problems with constraints
- Ordering problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem T](https://atcoder.jp/contests/dp/tasks/dp_t) - Original problem
- Insertion DP techniques

