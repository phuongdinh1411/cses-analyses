---
layout: simple
title: "Sushi"
permalink: /problem_soulutions/dynamic_programming_at/sushi_analysis
---

# Sushi

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand expectation DP with state compression
- Apply DP to expectation value problems
- Handle state transitions with multiple outcomes
- Optimize expectation DP computations

## 📋 Problem Description

There are N plates of sushi. Each plate has 0, 1, 2, or 3 pieces of sushi. Taro chooses one plate uniformly at random. If the chosen plate has at least one piece, he eats one piece from it. Otherwise, he does nothing. This process repeats until all plates are empty. Find the expected number of operations.

**Input**: 
- First line: N (1 ≤ N ≤ 300)
- Second line: a_1, a_2, ..., a_N (0 ≤ a_i ≤ 3)

**Output**: 
- Expected number of operations (with absolute error ≤ 10^-9)

**Constraints**:
- 1 ≤ N ≤ 300
- 0 ≤ a_i ≤ 3

## 🔍 Solution Analysis

### Approach: Expectation DP with State Compression

**Key Insight**: Use DP with state compression. Instead of tracking each plate individually, track counts of plates with 0, 1, 2, 3 pieces.

**DP State Definition**:
- `dp[i][j][k]` = expected number of operations when there are i plates with 1 piece, j plates with 2 pieces, k plates with 3 pieces
- State compression: Only need (i, j, k) since plates with 0 pieces don't affect transitions

**Recurrence Relation**:
- `dp[i][j][k] = 1 + (i/N) * dp[i-1][j][k] + (j/N) * dp[i+1][j-1][k] + (k/N) * dp[i][j+1][k-1] + ((N-i-j-k)/N) * dp[i][j][k]`
- Rearrange: `dp[i][j][k] = (N + i*dp[i-1][j][k] + j*dp[i+1][j-1][k] + k*dp[i][j+1][k-1]) / (i+j+k)`

**Implementation**:
```python
def sushi_expectation(n, plates):
    """
    Expectation DP solution for Sushi problem
    
    Args:
        n: number of plates
        plates: list of sushi counts per plate
    
    Returns:
        float: expected number of operations
    """
    # Count plates with 1, 2, 3 pieces
    count_1 = sum(1 for a in plates if a == 1)
    count_2 = sum(1 for a in plates if a == 2)
    count_3 = sum(1 for a in plates if a == 3)
    
    # dp[i][j][k] = expected operations with i plates of 1, j of 2, k of 3
    memo = {}
    
    def expected_ops(i, j, k):
        if (i, j, k) in memo:
            return memo[(i, j, k)]
        
        # Base case: all plates empty
        if i == 0 and j == 0 and k == 0:
            return 0.0
        
        # Calculate expected value
        total_non_empty = i + j + k
        if total_non_empty == 0:
            return 0.0
        
        result = n  # One operation
        
        # From 1-piece plate: becomes 0-piece
        if i > 0:
            result += i * expected_ops(i - 1, j, k)
        
        # From 2-piece plate: becomes 1-piece
        if j > 0:
            result += j * expected_ops(i + 1, j - 1, k)
        
        # From 3-piece plate: becomes 2-piece
        if k > 0:
            result += k * expected_ops(i, j + 1, k - 1)
        
        result /= total_non_empty
        memo[(i, j, k)] = result
        return result
    
    return expected_ops(count_1, count_2, count_3)

# Example usage
n = 3
plates = [1, 2, 3]
result = sushi_expectation(n, plates)
print(f"Expected operations: {result:.6f}")
```

**Time Complexity**: O(N^3) - State space is O(N^3)
**Space Complexity**: O(N^3) - Memoization table

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Expectation DP | O(N^3) | O(N^3) | State compression by counts |

### Why This Solution Works
- **State Compression**: Track counts instead of individual plates
- **Expectation DP**: Use linearity of expectation
- **Memoization**: Cache computed states

## 🚀 Related Problems
- [Coins](https://atcoder.jp/contests/dp/tasks/dp_i) - Probability DP
- Expectation value problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem J](https://atcoder.jp/contests/dp/tasks/dp_j) - Original problem
- Expectation DP techniques

