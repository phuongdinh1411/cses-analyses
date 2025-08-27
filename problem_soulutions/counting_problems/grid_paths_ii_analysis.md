# CSES Grid Paths II - Problem Analysis

## Problem Statement
Given an n×n grid with some blocked cells, count the number of paths from the top-left corner to the bottom-right corner, moving only right or down.

### Input
The first input line has an integer n: the size of the grid.
Then there are n lines describing the grid. Each line has n characters: '.' for empty cell and '#' for blocked cell.

### Output
Print the number of valid paths modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 1000

### Example
```
Input:
3
...
.#.
...

Output:
2
```

## Solution Progression

### Approach 1: Recursive DFS - O(2^(n²))
**Description**: Use recursive DFS to explore all possible paths.

```python
def grid_paths_ii_naive(n, grid):
    MOD = 10**9 + 7
    
    def dfs(i, j):
        if i == n-1 and j == n-1:
            return 1
        
        if i >= n or j >= n or grid[i][j] == '#':
            return 0
        
        return (dfs(i+1, j) + dfs(i, j+1)) % MOD
    
    return dfs(0, 0)
```

**Why this is inefficient**: O(2^(n²)) complexity is too slow for large grids.

### Improvement 1: Dynamic Programming - O(n²)
**Description**: Use DP to avoid recalculating subproblems.

```python
def grid_paths_ii_dp(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case
    if grid[0][0] != '#':
        dp[0][0] = 1
    
    # Fill first row
    for j in range(1, n):
        if grid[0][j] != '#':
            dp[0][j] = dp[0][j-1]
    
    # Fill first column
    for i in range(1, n):
        if grid[i][0] != '#':
            dp[i][0] = dp[i-1][0]
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] != '#':
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]
```

**Why this improvement works**: DP avoids recalculating subproblems, reducing complexity to O(n²).

### Approach 2: Optimized DP - O(n²)
**Description**: Optimize DP with better implementation.

```python
def grid_paths_ii_optimized(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case
    if grid[0][0] != '#':
        dp[0][0] = 1
    
    # Fill the grid
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '#':
                continue
            
            # Add paths from above
            if i > 0:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            
            # Add paths from left
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]
```

**Why this improvement works**: Simplified DP implementation with better readability.

## Final Optimal Solution

```python
n = int(input())
grid = []
for _ in range(n):
    row = input().strip()
    grid.append(row)

def count_grid_paths(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case
    if grid[0][0] != '#':
        dp[0][0] = 1
    
    # Fill the grid
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '#':
                continue
            
            # Add paths from above
            if i > 0:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            
            # Add paths from left
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]

result = count_grid_paths(n, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive DFS | O(2^(n²)) | O(n²) | Simple but exponential |
| Dynamic Programming | O(n²) | O(n²) | DP avoids recalculation |
| Optimized DP | O(n²) | O(n²) | Simplified implementation |

## Key Insights for Other Problems

### 1. **Grid Path Counting**
**Principle**: Use dynamic programming to count paths in grids efficiently.
**Applicable to**: Grid problems, path counting problems, DP problems

### 2. **Blocked Cell Handling**
**Principle**: Skip blocked cells in DP calculations.
**Applicable to**: Constraint satisfaction problems, grid optimization problems

### 3. **Modular Arithmetic**
**Principle**: Use modular arithmetic to handle large numbers in counting problems.
**Applicable to**: Large number problems, counting problems, combinatorics problems

## Notable Techniques

### 1. **Grid DP Implementation**
```python
def grid_dp_paths(n, grid, MOD):
    dp = [[0] * n for _ in range(n)]
    
    # Base case
    if grid[0][0] != '#':
        dp[0][0] = 1
    
    # Fill grid
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '#':
                continue
            
            if i > 0:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]
```

### 2. **Blocked Cell Handling**
```python
def handle_blocked_cells(grid, i, j):
    if grid[i][j] == '#':
        return 0
    return 1
```

### 3. **Path Counting Formula**
```python
def path_counting_formula(dp, i, j, MOD):
    count = 0
    if i > 0:
        count = (count + dp[i-1][j]) % MOD
    if j > 0:
        count = (count + dp[i][j-1]) % MOD
    return count
```

## Problem-Solving Framework

1. **Identify problem type**: This is a grid path counting problem with blocked cells
2. **Choose approach**: Use dynamic programming
3. **Initialize DP table**: Create 2D DP array
4. **Handle base case**: Set starting position
5. **Fill DP table**: Calculate paths for each cell
6. **Handle blocked cells**: Skip blocked cells in calculations
7. **Return result**: Output number of paths to bottom-right corner

---

*This analysis shows how to efficiently count paths in a grid with blocked cells using dynamic programming.* 