# CSES Minimal Grid Path - Problem Analysis

## Problem Statement
Given an n×n grid, find the minimum cost path from the top-left corner to the bottom-right corner. You can only move right or down, and each cell has a cost.

### Input
The first input line has an integer n: the size of the grid.
Then there are n lines. Each line has n integers: the costs of the cells.

### Output
Print one integer: the minimum cost of a path from top-left to bottom-right.

### Constraints
- 1 ≤ n ≤ 1000
- 1 ≤ cost ≤ 10^9

### Example
```
Input:
3
1 2 3
4 5 6
7 8 9

Output:
21
```

## Solution Progression

### Approach 1: Recursive - O(2^(n*n))
**Description**: Use recursive approach to find minimum cost path.

```python
def minimal_grid_path_naive(n, grid):
    def min_path_recursive(i, j):
        if i == n-1 and j == n-1:
            return grid[i][j]
        
        if i >= n or j >= n:
            return float('inf')
        
        return grid[i][j] + min(min_path_recursive(i+1, j), min_path_recursive(i, j+1))
    
    return min_path_recursive(0, 0)
```

**Why this is inefficient**: We have overlapping subproblems, leading to exponential time complexity.

### Improvement 1: Dynamic Programming - O(n²)
**Description**: Use 2D DP table to store results of subproblems.

```python
def minimal_grid_path_optimized(n, grid):
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base case
    dp[n-1][n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            # Can move right
            if j + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i+1][j])
            
            dp[i][j] += grid[i][j]
    
    return dp[0][0]
```

**Why this improvement works**: We use a 2D DP table where dp[i][j] represents the minimum cost to reach cell (i,j) from the destination. We fill the table from bottom-right to top-left.

## Final Optimal Solution

```python
n = int(input())
grid = []
for _ in range(n):
    row = list(map(int, input().split()))
    grid.append(row)

def find_minimal_grid_path(n, grid):
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base case
    dp[n-1][n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            # Can move right
            if j + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i+1][j])
            
            dp[i][j] += grid[i][j]
    
    return dp[0][0]

result = find_minimal_grid_path(n, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^(n*n)) | O(n*n) | Overlapping subproblems |
| Dynamic Programming | O(n²) | O(n²) | Use 2D DP table |

## Key Insights for Other Problems

### 1. **Grid Path Problems**
**Principle**: Use 2D DP to find minimum cost paths in grids.
**Applicable to**: Grid problems, path problems, optimization problems

### 2. **2D Dynamic Programming**
**Principle**: Use 2D DP table to store results of subproblems for grid traversal.
**Applicable to**: Grid problems, traversal problems, DP problems

### 3. **Minimum Cost Path**
**Principle**: Find the minimum cost path by considering all possible moves.
**Applicable to**: Path problems, optimization problems, grid problems

## Notable Techniques

### 1. **2D DP Table Construction**
```python
def build_2d_dp_table(n):
    return [[float('inf')] * n for _ in range(n)]
```

### 2. **Grid Path Recurrence**
```python
def grid_path_recurrence(dp, grid, i, j, n):
    if i == n-1 and j == n-1:
        return grid[i][j]
    
    min_cost = float('inf')
    
    # Move right
    if j + 1 < n:
        min_cost = min(min_cost, dp[i][j+1])
    
    # Move down
    if i + 1 < n:
        min_cost = min(min_cost, dp[i+1][j])
    
    return grid[i][j] + min_cost
```

### 3. **DP Table Filling**
```python
def fill_dp_table(grid, n):
    dp = build_2d_dp_table(n)
    dp[n-1][n-1] = grid[n-1][n-1]
    
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            dp[i][j] = grid_path_recurrence(dp, grid, i, j, n)
    
    return dp[0][0]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a minimum cost grid path problem
2. **Choose approach**: Use 2D dynamic programming
3. **Define DP state**: dp[i][j] = minimum cost to reach (i,j) from destination
4. **Base case**: dp[n-1][n-1] = grid[n-1][n-1]
5. **Recurrence relation**: dp[i][j] = grid[i][j] + min(dp[i+1][j], dp[i][j+1])
6. **Fill DP table**: Iterate from bottom-right to top-left
7. **Return result**: Output dp[0][0]

---

*This analysis shows how to efficiently find the minimum cost path in a grid using 2D dynamic programming.* 