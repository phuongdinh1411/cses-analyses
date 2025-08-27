# CSES Removal Game - Problem Analysis

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
            return 0
        
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