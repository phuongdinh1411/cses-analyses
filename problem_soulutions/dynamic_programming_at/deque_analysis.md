---
layout: simple
title: "Deque"
permalink: /problem_soulutions/dynamic_programming_at/deque_analysis
---

# Deque

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand interval DP
- Apply DP to two-player optimization games
- Handle optimal play with DP
- Recognize interval DP patterns

## 📋 Problem Description

There is a deque (double-ended queue) with N integers. Two players take turns. On each turn, a player removes either the leftmost or rightmost element and adds it to their score. Both players play optimally. Find the maximum score difference (first player - second player).

**Input**: 
- First line: N (1 ≤ N ≤ 3000)
- Second line: a_1, a_2, ..., a_N (1 ≤ a_i ≤ 10^9)

**Output**: 
- Maximum score difference

**Constraints**:
- 1 ≤ N ≤ 3000
- 1 ≤ a_i ≤ 10^9

## 🔍 Solution Analysis

### Approach: Interval DP

**Key Insight**: Use interval DP to compute optimal play for each subarray.

**DP State Definition**:
- `dp[i][j]` = maximum score difference (first player - second player) for subarray from index i to j (inclusive)
- When it's first player's turn: maximize score difference
- When it's second player's turn: minimize score difference (or equivalently, maximize negative difference)

**Recurrence Relation**:
- For interval [i, j]:
  - If first player takes left: `a[i] - dp[i+1][j]` (subtract because next is second player's optimal)
  - If first player takes right: `a[j] - dp[i][j-1]`
  - `dp[i][j] = max(a[i] - dp[i+1][j], a[j] - dp[i][j-1])`

**Implementation**:
```python
def deque_game(n, arr):
    """
    Interval DP solution for Deque problem
    
    Args:
        n: number of elements
        arr: list of integers
    
    Returns:
        int: maximum score difference
    """
    # dp[i][j] = max score diff for subarray [i, j]
    dp = [[0] * n for _ in range(n)]
    
    # Base case: single element
    for i in range(n):
        dp[i][i] = arr[i]
    
    # Fill DP table for intervals of increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # First player chooses left or right
            # After first player's move, it's second player's turn
            # So we subtract the optimal value for second player
            take_left = arr[i] - dp[i + 1][j]
            take_right = arr[j] - dp[i][j - 1]
            dp[i][j] = max(take_left, take_right)
    
    return dp[0][n - 1]

# Example usage
n = 4
arr = [10, 80, 90, 30]
result = deque_game(n, arr)
print(f"Score difference: {result}")
```

**Time Complexity**: O(N^2)
**Space Complexity**: O(N^2)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Interval DP | O(N^2) | O(N^2) | Optimal play on intervals |

### Why This Solution Works
- **Interval DP**: Build solution from smaller intervals
- **Optimal Play**: DP finds optimal moves for both players
- **Score Difference**: Track difference rather than individual scores

## 🚀 Related Problems
- [Removal Game](https://cses.fi/problemset/task/1097) - Similar problem
- Interval DP problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem L](https://atcoder.jp/contests/dp/tasks/dp_l) - Original problem
- Interval DP techniques

