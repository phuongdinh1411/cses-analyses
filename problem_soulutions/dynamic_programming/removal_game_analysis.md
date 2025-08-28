---
layout: simple
title: "Removal Game
permalink: /problem_soulutions/dynamic_programming/removal_game_analysis/
---

# Removal Game

## Problem Statement
Given an array of n integers, two players take turns removing elements from either end of the array. Each player wants to maximize their total score. Find the maximum score difference between the first and second player.

### Input
The first input line has an integer n: the size of the array.
The second line has n integers a1,a2,…,an: the array.

### Output
Print one integer: the maximum score difference.

### Constraints
- 1 ≤ n ≤ 5000
- -10^9 ≤ ai ≤ 10^9

### Example
```
Input:
4
4 5 1 3

Output:
5
```

## Solution Progression

### Approach 1: Recursive - O(2^n)
**Description**: Use recursive approach to find optimal play.

```python
def removal_game_naive(n, arr):
    def optimal_play(left, right, turn):
        if left > right:
            return 0"
        if turn == 0:  # First player's turn
            return max(arr[left] + optimal_play(left + 1, right, 1),
                      arr[right] + optimal_play(left, right - 1, 1))
        else:  # Second player's turn
            return min(-arr[left] + optimal_play(left + 1, right, 0),
                      -arr[right] + optimal_play(left, right - 1, 0))
    
    return optimal_play(0, n - 1, 0)
```

**Why this is inefficient**: We have overlapping subproblems, leading to exponential time complexity.

### Improvement 1: Dynamic Programming - O(n²)
**Description**: Use 2D DP table to store results of subproblems.

```python
def removal_game_optimized(n, arr):
    dp = [[0] * n for _ in range(n)]
    
    # Fill diagonal (single element)
    for i in range(n):
        dp[i][i] = arr[i]
    
    # Fill for subarrays of increasing length
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            dp[left][right] = max(arr[left] - dp[left + 1][right],
                                arr[right] - dp[left][right - 1])
    
    return dp[0][n - 1]
```

**Why this improvement works**: We use a 2D DP table where dp[left][right] represents the maximum score difference when playing optimally on subarray arr[left:right+1]. We fill the table using the recurrence relation.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

def find_removal_game_score(n, arr):
    dp = [[0] * n for _ in range(n)]
    
    # Fill diagonal (single element)
    for i in range(n):
        dp[i][i] = arr[i]
    
    # Fill for subarrays of increasing length
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            dp[left][right] = max(arr[left] - dp[left + 1][right],
                                arr[right] - dp[left][right - 1])
    
    return dp[0][n - 1]

result = find_removal_game_score(n, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Overlapping subproblems |
| Dynamic Programming | O(n²) | O(n²) | Use 2D DP table |

## Key Insights for Other Problems

### 1. **Game Theory Problems**
**Principle**: Use 2D DP to find optimal play in two-player games.
**Applicable to**: Game problems, optimization problems, DP problems

### 2. **2D Dynamic Programming**
**Principle**: Use 2D DP table to store results of subproblems for game optimization.
**Applicable to**: Game problems, optimization problems, DP problems

### 3. **Optimal Play**
**Principle**: Find optimal play by considering all possible moves and choosing the best outcome.
**Applicable to**: Game problems, optimization problems, strategy problems

## Notable Techniques

### 1. **2D DP Table Construction**
```python
def build_2d_dp_table(n):
    return [[0] * n for _ in range(n)]
```

### 2. **Game Recurrence**
```python
def game_recurrence(dp, arr, left, right):
    if left == right:
        return arr[left]
    
    return max(arr[left] - dp[left + 1][right],
              arr[right] - dp[left][right - 1])
```

### 3. **DP Table Filling**
```python
def fill_dp_table(arr, n):
    dp = build_2d_dp_table(n)
    
    # Fill diagonal
    for i in range(n):
        dp[i][i] = arr[i]
    
    # Fill for increasing lengths
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            dp[left][right] = game_recurrence(dp, arr, left, right)
    
    return dp[0][n - 1]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a two-player game optimization problem
2. **Choose approach**: Use 2D dynamic programming
3. **Define DP state**: dp[left][right] = optimal score difference for subarray arr[left:right+1]
4. **Base case**: dp[i][i] = arr[i]
5. **Recurrence relation**: dp[left][right] = max(arr[left] - dp[left+1][right], arr[right] - dp[left][right-1])
6. **Fill DP table**: Iterate through subarrays of increasing length
7. **Return result**: Output dp[0][n-1]

---

*This analysis shows how to efficiently find the optimal play in a two-player removal game using 2D dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: K-Player Removal Game**
**Problem**: Extend to k players taking turns removing elements from either end.
```python
def k_player_removal_game(n, arr, k):
    # dp[left][right][player] = optimal score for player on subarray arr[left:right+1]
    dp = [[[0] * k for _ in range(n)] for _ in range(n)]
    
    # Fill diagonal (single element)
    for i in range(n):
        dp[i][i][0] = arr[i]
    
    # Fill for subarrays of increasing length
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            for player in range(k):
                next_player = (player + 1) % k
                dp[left][right][player] = max(
                    arr[left] - dp[left + 1][right][next_player],
                    arr[right] - dp[left][right - 1][next_player]
                )
    
    return dp[0][n - 1][0]
```

#### **Variation 2: Removal Game with Constraints**
**Problem**: Players can only remove elements if they satisfy certain constraints (e.g., even numbers only).
```python
def constrained_removal_game(n, arr, constraint_func):
    dp = [[0] * n for _ in range(n)]
    
    # Fill diagonal
    for i in range(n):
        if constraint_func(arr[i]):
            dp[i][i] = arr[i]
    
    # Fill for subarrays of increasing length
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            
            left_move = 0
            right_move = 0
            
            if constraint_func(arr[left]):
                left_move = arr[left] - dp[left + 1][right]
            if constraint_func(arr[right]):
                right_move = arr[right] - dp[left][right - 1]
            
            dp[left][right] = max(left_move, right_move)
    
    return dp[0][n - 1]
```

#### **Variation 3: Removal Game with Probabilities**
**Problem**: Elements have probabilities of being removed, find expected score difference.
```python
def probabilistic_removal_game(n, arr, probabilities):
    # probabilities[i] = probability of successfully removing arr[i]
    dp = [[0.0] * n for _ in range(n)]
    
    # Fill diagonal
    for i in range(n):
        dp[i][i] = arr[i] * probabilities[i]
    
    # Fill for subarrays of increasing length
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            
            left_expected = probabilities[left] * (arr[left] - dp[left + 1][right])
            right_expected = probabilities[right] * (arr[right] - dp[left][right - 1])
            
            dp[left][right] = max(left_expected, right_expected)
    
    return dp[0][n - 1]
```

#### **Variation 4: Removal Game with Costs**
**Problem**: Each removal has a cost, find optimal play considering costs.
```python
def removal_game_with_costs(n, arr, costs):
    # costs[i] = cost to remove arr[i]
    dp = [[0] * n for _ in range(n)]
    
    # Fill diagonal
    for i in range(n):
        dp[i][i] = arr[i] - costs[i]
    
    # Fill for subarrays of increasing length
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            
            left_score = (arr[left] - costs[left]) - dp[left + 1][right]
            right_score = (arr[right] - costs[right]) - dp[left][right - 1]
            
            dp[left][right] = max(left_score, right_score)
    
    return dp[0][n - 1]
```

#### **Variation 5: Removal Game with Memory**
**Problem**: Players remember previous moves and can use this information strategically.
```python
def removal_game_with_memory(n, arr, memory_size):
    # dp[left][right][last_moves] = optimal score with memory of last moves
    dp = {}
    
    def solve(left, right, last_moves):
        if left > right:
            return 0
        
        state = (left, right, tuple(last_moves))
        if state in dp:
            return dp[state]
        
        # Consider strategic moves based on memory
        left_score = arr[left] - solve(left + 1, right, last_moves[1:] + [left])
        right_score = arr[right] - solve(left, right - 1, last_moves[1:] + [right])
        
        dp[state] = max(left_score, right_score)
        return dp[state]
    
    return solve(0, n - 1, [0] * memory_size)
```

### 🔗 **Related Problems & Concepts**

#### **1. Game Theory Problems**
- **Nim Game**: Remove objects from heaps
- **Grundy Numbers**: Calculate game positions
- **Minimax Algorithm**: Find optimal play
- **Alpha-Beta Pruning**: Optimize game tree search

#### **2. Dynamic Programming Patterns**
- **2D DP**: Two state variables (left, right)
- **Game DP**: Store optimal play for each position
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Optimization Problems**
- **Maximization**: Find maximum possible score
- **Minimization**: Find minimum possible loss
- **Zero-Sum Games**: One player's gain equals other's loss
- **Strategic Planning**: Plan multiple moves ahead

#### **4. Algorithmic Techniques**
- **Recursive Backtracking**: Try all possible moves
- **Memoization**: Cache computed results
- **Bottom-Up DP**: Build solution iteratively
- **State Space Search**: Explore all possible game states

#### **5. Mathematical Concepts**
- **Combinatorial Game Theory**: Mathematical study of games
- **Optimal Strategy**: Best possible play
- **Expected Value**: Average outcome over many games
- **Probability Theory**: Random elements in games

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    result = removal_game_optimal(n, arr)
    print(result)
```

#### **2. Range Queries on Game Results**
```python
def range_game_queries(n, arr, queries):
    # Precompute for all subarrays
    dp = [[0] * n for _ in range(n)]
    
    # Fill DP table (same as original solution)
    for i in range(n):
        dp[i][i] = arr[i]
    
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            dp[left][right] = max(arr[left] - dp[left + 1][right],
                                arr[right] - dp[left][right - 1])
    
    # Answer queries
    for l, r in queries:
        print(dp[l][r])
```

#### **3. Interactive Game Problems**
```python
def interactive_removal_game():
    n = int(input())
    arr = list(map(int, input().split()))
    
    print("You play first. Choose left (0) or right (1):")
    while True:
        choice = int(input())
        if choice == 0:  # Left
            score = arr[0]
            arr = arr[1:]
        else:  # Right
            score = arr[-1]
            arr = arr[:-1]
        
        print(f"Your score: {score}, Remaining: {arr}")
        
        if not arr:
            break
        
        # Computer plays optimally
        if len(arr) == 1:
            computer_score = arr[0]
            arr = []
        else:
            if arr[0] - optimal_play(arr[1:]) > arr[-1] - optimal_play(arr[:-1]):
                computer_score = arr[0]
                arr = arr[1:]
            else:
                computer_score = arr[-1]
                arr = arr[:-1]
        
        print(f"Computer score: {computer_score}, Remaining: {arr}")
```

### 🧮 **Mathematical Extensions**

#### **1. Game Theory Analysis**
- **Nash Equilibrium**: Stable strategy profiles
- **Mixed Strategies**: Probabilistic play
- **Perfect Information**: All players know all information
- **Imperfect Information**: Hidden information

#### **2. Advanced DP Techniques**
- **Digit DP**: Count winning positions
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split games into subgames
- **Persistent Data Structures**: Maintain game history

#### **3. Combinatorial Analysis**
- **Grundy Numbers**: Calculate game positions
- **Sprague-Grundy Theorem**: Decompose games
- **P-Positions**: Previous player wins
- **N-Positions**: Next player wins

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Minimax Algorithm**: Find optimal play in games
- **Alpha-Beta Pruning**: Optimize game tree search
- **Monte Carlo Tree Search**: Heuristic game playing
- **Negamax**: Simplified minimax for zero-sum games

#### **2. Mathematical Concepts**
- **Combinatorial Game Theory**: Mathematical study of games
- **Probability Theory**: Random elements in games
- **Optimization Theory**: Finding best strategies
- **Decision Theory**: Making optimal choices

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Recursion**: Natural way to model games
- **State Space Search**: Exploring all possibilities

---

*This analysis demonstrates the power of dynamic programming for game theory problems and shows various extensions and applications.* 