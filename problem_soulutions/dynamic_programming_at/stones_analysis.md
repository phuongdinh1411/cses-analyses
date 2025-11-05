---
layout: simple
title: "Stones - AtCoder Educational DP Contest Problem K"
permalink: /problem_soulutions/dynamic_programming_at/stones_analysis
---

# Stones - AtCoder Educational DP Contest Problem K

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand game theory DP
- Apply DP to solve impartial game problems
- Recognize winning/losing positions
- Handle game theory with DP

### 📚 **Prerequisites**
- Dynamic Programming, game theory, Grundy numbers
- Arrays, bit manipulation
- Related: Game theory problems, Nim game

## 📋 Problem Description

There are N stones. Two players take turns. On each turn, a player can remove a_1, a_2, ..., or a_K stones. The player who cannot make a move loses. Determine if the first player wins given N stones.

**Input**: 
- First line: N, K (1 ≤ N ≤ 10^5, 1 ≤ K ≤ 100)
- Second line: a_1, a_2, ..., a_K (1 ≤ a_i ≤ N)

**Output**: 
- Print "First" if first player wins, "Second" otherwise

**Constraints**:
- 1 ≤ N ≤ 10^5
- 1 ≤ K ≤ 100
- 1 ≤ a_i ≤ N

## 🔍 Solution Analysis

### Approach: Game Theory DP

**Key Insight**: Use DP to determine winning/losing positions.

**DP State Definition**:
- `dp[i]` = True if position i is winning, False if losing
- `dp[0]` = False (no stones, losing position)

**Recurrence Relation**:
- `dp[i] = True` if there exists a move a_j such that `dp[i - a_j] = False`
- `dp[i] = False` if for all moves a_j, `dp[i - a_j] = True`

**Implementation**:
```python
def stones_game(n, k, moves):
    """
    Game theory DP solution for Stones problem
    
    Args:
        n: number of stones
        k: number of possible moves
        moves: list of possible moves
    
    Returns:
        str: "First" or "Second"
    """
    # dp[i] = True if position i is winning
    dp = [False] * (n + 1)
    
    # Base case: 0 stones is losing
    dp[0] = False
    
    # Fill DP table
    for i in range(1, n + 1):
        # Check if any move leads to losing position
        for move in moves:
            if move <= i and not dp[i - move]:
                dp[i] = True
                break
    
    return "First" if dp[n] else "Second"

# Example usage
n, k = 8, 3
moves = [2, 3, 5]
result = stones_game(n, k, moves)
print(result)  # Output: First or Second
```

**Time Complexity**: O(N*K)
**Space Complexity**: O(N)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Game Theory DP | O(N*K) | O(N) | Winning/losing positions |

### Why This Solution Works
- **Optimal Play**: DP finds optimal moves
- **Winning Position**: Can force opponent to losing position
- **Losing Position**: All moves lead to winning positions for opponent

## 🚀 Related Problems
- Nim game variants
- Game theory DP problems

## 🔗 Additional Resources
- [AtCoder DP Contest Problem K](https://atcoder.jp/contests/dp/tasks/dp_k) - Original problem
- Game theory algorithms

