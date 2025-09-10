---
layout: simple
title: "Grid Paths II"
permalink: /problem_soulutions/counting_problems/grid_paths_ii_analysis
---


# Grid Paths II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand grid path counting with obstacles and movement constraints
- Apply dynamic programming to count valid paths in 2D grids
- Implement efficient DP algorithms for grid path counting with obstacles
- Optimize grid path counting using space-efficient DP techniques
- Handle edge cases in grid path counting (blocked start/end, no valid paths)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, grid algorithms, path counting, obstacle handling
- **Data Structures**: 2D arrays, DP tables, grid representations
- **Mathematical Concepts**: Grid theory, path counting, combinatorics, modular arithmetic
- **Programming Skills**: 2D DP implementation, grid manipulation, modular arithmetic
- **Related Problems**: Grid Paths (basic grid paths), Labyrinth (grid traversal), Message Route (path finding)

## 📋 Problem Description

Given an n×n grid with some blocked cells, count the number of paths from the top-left corner to the bottom-right corner, moving only right or down.

**Input**: 
- First line: integer n (size of the grid)
- Next n lines: n characters each ('.' for empty cell, '#' for blocked cell)

**Output**: 
- Print the number of valid paths modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 1000

**Example**:
```
Input:
3
...
.#.
...

Output:
2

Explanation**: 
In the 3×3 grid, there are 2 valid paths from (0,0) to (2,2):
1. Right → Right → Down → Down: (0,0) → (0,1) → (0,2) → (1,2) → (2,2)
2. Down → Down → Right → Right: (0,0) → (1,0) → (2,0) → (2,1) → (2,2)

Both paths avoid the blocked cell at (1,1) and reach the destination.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Generate All Possible Paths

**Key Insights from Brute Force Approach**:
- **Exhaustive Path Generation**: Generate all possible paths from start to end
- **Path Validation**: Check if each path avoids blocked cells
- **Complete Coverage**: Guaranteed to find all valid paths
- **Simple Implementation**: Recursive approach to explore all possibilities

**Key Insight**: Systematically generate all possible paths from (0,0) to (n-1,n-1) and count those that avoid blocked cells.

**Algorithm**:
- Use recursive DFS to explore all possible paths
- At each cell, try moving right and down (if valid)
- Count paths that reach the destination without hitting blocked cells

**Visual Example**:
```
Grid (3×3):
. . .
. # .
. . .

All possible paths from (0,0) to (2,2):
1. R→R→D→D: (0,0)→(0,1)→(0,2)→(1,2)→(2,2) ✓
2. R→D→R→D: (0,0)→(0,1)→(1,1) ✗ (blocked)
3. R→D→D→R: (0,0)→(0,1)→(1,1) ✗ (blocked)
4. D→R→R→D: (0,0)→(1,0)→(1,1) ✗ (blocked)
5. D→R→D→R: (0,0)→(1,0)→(1,1) ✗ (blocked)
6. D→D→R→R: (0,0)→(1,0)→(2,0)→(2,1)→(2,2) ✓

Valid paths: 2
```

**Implementation**:
```python
def brute_force_grid_paths(grid):
    """
    Count valid paths using brute force approach
    
    Args:
        grid: 2D list representing the grid ('.' for empty, '#' for blocked)
    
    Returns:
        int: number of valid paths from (0,0) to (n-1,n-1)
    """
    n = len(grid)
    
    def dfs(i, j):
        # Base case: reached destination
        if i == n-1 and j == n-1:
            return 1
        
        # Base case: out of bounds or blocked
        if i >= n or j >= n or grid[i][j] == '#':
            return 0
        
        # Recursive case: try moving right and down
        return dfs(i, j+1) + dfs(i+1, j)
    
    return dfs(0, 0)

# Example usage
grid = [
    ['.', '.', '.'],
    ['.', '#', '.'],
    ['.', '.', '.']
]
result = brute_force_grid_paths(grid)
print(f"Brute force result: {result}")  # Output: 2
```

**Time Complexity**: O(2^(2n)) - Exponential due to overlapping subproblems
**Space Complexity**: O(n) - Recursion stack depth

**Why it's inefficient**: Exponential time complexity due to repeated calculations of the same subproblems.

---

### Approach 2: Optimized - Dynamic Programming with Memoization

**Key Insights from Optimized Approach**:
- **Memoization**: Store results of subproblems to avoid recomputation
- **Overlapping Subproblems**: Many paths share common subpaths
- **Top-Down DP**: Use recursive approach with memoization
- **Efficient Storage**: Cache results for each cell position

**Key Insight**: Use memoization to avoid recalculating the same subproblems, significantly reducing time complexity.

**Algorithm**:
- Use recursive DFS with memoization
- Store the number of paths from each cell to the destination
- Return cached result if already computed

**Visual Example**:
```
Grid (3×3):
. . .
. # .
. . .

Memoization table (paths from each cell to (2,2)):
[2, 1, 1]
[1, 0, 1]
[1, 1, 1]

Explanation:
- (0,0): 2 paths (R→R→D→D, D→D→R→R)
- (0,1): 1 path (R→D→D)
- (0,2): 1 path (D→D)
- (1,0): 1 path (D→R→R)
- (1,1): 0 paths (blocked)
- (1,2): 1 path (D)
- (2,0): 1 path (R→R)
- (2,1): 1 path (R)
- (2,2): 1 path (destination)
```

**Implementation**:
```python
def optimized_grid_paths(grid):
    """
    Count valid paths using memoization
    
    Args:
        grid: 2D list representing the grid
    
    Returns:
        int: number of valid paths from (0,0) to (n-1,n-1)
    """
    n = len(grid)
    memo = {}
    
    def dfs(i, j):
        # Base case: reached destination
        if i == n-1 and j == n-1:
            return 1
        
        # Base case: out of bounds or blocked
        if i >= n or j >= n or grid[i][j] == '#':
            return 0
        
        # Check if already computed
        if (i, j) in memo:
            return memo[(i, j)]
        
        # Compute and store result
        result = dfs(i, j+1) + dfs(i+1, j)
        memo[(i, j)] = result
        return result
    
    return dfs(0, 0)

# Example usage
grid = [
    ['.', '.', '.'],
    ['.', '#', '.'],
    ['.', '.', '.']
]
result = optimized_grid_paths(grid)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - Each cell computed once
**Space Complexity**: O(n²) - For memoization table

**Why it's better**: Eliminates redundant calculations, making it much more efficient.

---

### Approach 3: Optimal - Bottom-Up Dynamic Programming

**Key Insights from Optimal Approach**:
- **Bottom-Up DP**: Build solution from base cases to target
- **Tabular Approach**: Use 2D table to store results
- **Iterative Solution**: Avoid recursion overhead
- **Space Optimization**: Can optimize space usage further

**Key Insight**: Use bottom-up dynamic programming to build the solution iteratively, avoiding recursion and providing optimal time and space complexity.

**Algorithm**:
- Create DP table where dp[i][j] = number of paths from (i,j) to destination
- Fill table from bottom-right to top-left
- Handle blocked cells and boundary conditions
- Return dp[0][0]

**Visual Example**:
```
Grid (3×3):
. . .
. # .
. . .

DP table construction (bottom-up):
Step 1: Initialize destination
[0, 0, 0]
[0, 0, 0]
[0, 0, 1]

Step 2: Fill bottom row
[0, 0, 0]
[0, 0, 1]
[1, 1, 1]

Step 3: Fill middle row
[0, 0, 1]
[0, 0, 1]
[1, 1, 1]

Step 4: Fill top row
[2, 1, 1]
[0, 0, 1]
[1, 1, 1]

Result: dp[0][0] = 2
```

**Implementation**:
```python
def optimal_grid_paths(grid):
    """
    Count valid paths using bottom-up DP
    
    Args:
        grid: 2D list representing the grid
    
    Returns:
        int: number of valid paths from (0,0) to (n-1,n-1)
    """
    n = len(grid)
    
    # Initialize DP table
    dp = [[0] * n for _ in range(n)]
    
    # Base case: destination has 1 path
    if grid[n-1][n-1] != '#':
        dp[n-1][n-1] = 1
    
    # Fill table from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            # Skip if blocked or already filled (destination)
            if grid[i][j] == '#' or (i == n-1 and j == n-1):
                continue
            
            # Add paths from right and down
            if j+1 < n:
                dp[i][j] += dp[i][j+1]
            if i+1 < n:
                dp[i][j] += dp[i+1][j]
    
    return dp[0][0]

# Example usage
grid = [
    ['.', '.', '.'],
    ['.', '#', '.'],
    ['.', '.', '.']
]
result = optimal_grid_paths(grid)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - Fill entire DP table once
**Space Complexity**: O(n²) - For DP table

**Why it's optimal**: Efficient bottom-up approach with optimal time and space complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^(2n)) | O(n) | Generate all paths recursively |
| Memoization | O(n²) | O(n²) | Cache subproblem results |
| Bottom-Up DP | O(n²) | O(n²) | Build solution iteratively |

### Time Complexity
- **Time**: O(n²) - Each cell computed once in optimal approach
- **Space**: O(n²) - For DP table

### Why This Solution Works
- **Path Counting**: Count all valid paths from start to destination
- **Obstacle Avoidance**: Skip blocked cells in path calculation
- **Dynamic Programming**: Efficiently solve overlapping subproblems
- **Optimal Approach**: Bottom-up DP provides best performance
