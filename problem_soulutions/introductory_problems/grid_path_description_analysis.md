---
layout: simple
title: "Grid Path Description Analysis"
permalink: /problem_soulutions/introductory_problems/grid_path_description_analysis/
---


# Grid Path Description Analysis

## Problem Description

Given a grid path description (string of 'R', 'D', 'L', 'U' for right, down, left, up), find the number of different paths that can be described by this string when starting from the top-left corner of an n×n grid.

## Key Insights

### 1. Path Validation
- Check if the path stays within grid boundaries
- Ensure 0 ≤ x, y < n at each step
- Count only valid paths that don't go out of bounds

### 2. Movement Mapping
- 'R': (x, y) → (x+1, y)
- 'D': (x, y) → (x, y+1)
- 'L': (x, y) → (x-1, y)
- 'U': (x, y) → (x, y-1)

### 3. Dynamic Programming
- Use DP to count valid paths
- State: (position, current index in string)
- Transition: try each possible direction

## Solution Approach

### Method 1: Recursive with Memoization
```python
class Solution:
    def __init__(self):
        self.dp = {}
        self.path = ""
        self.n = 0
    
    def solve(self, x, y, idx):
        if idx == len(self.path):
            return 1
        
        if (x, y, idx) in self.dp:
            return self.dp[(x, y, idx)]
        
        count = 0
        direction = self.path[idx]
        
        if direction == 'R' and x + 1 < self.n:
            count += self.solve(x + 1, y, idx + 1)
        if direction == 'D' and y + 1 < self.n:
            count += self.solve(x, y + 1, idx + 1)
        if direction == 'L' and x - 1 >= 0:
            count += self.solve(x - 1, y, idx + 1)
        if direction == 'U' and y - 1 >= 0:
            count += self.solve(x, y - 1, idx + 1)
        
        self.dp[(x, y, idx)] = count
        return count
    
    def count_paths(self, path_desc, grid_size):
        self.path = path_desc
        self.n = grid_size
        self.dp = {}
        
        return self.solve(0, 0, 0)
```

### Method 2: Iterative DP
```python
def count_paths_iterative(path, n):
    # Initialize 3D DP table: dp[x][y][idx]
    dp = [[[0] * (len(path) + 1) for _ in range(n)] for _ in range(n)]
    
    dp[0][0][0] = 1
    
    for idx in range(len(path)):
        for x in range(n):
            for y in range(n):
                if dp[x][y][idx] == 0:
                    continue
                
                direction = path[idx]
                
                if direction == 'R' and x + 1 < n:
                    dp[x + 1][y][idx + 1] += dp[x][y][idx]
                if direction == 'D' and y + 1 < n:
                    dp[x][y + 1][idx + 1] += dp[x][y][idx]
                if direction == 'L' and x - 1 >= 0:
                    dp[x - 1][y][idx + 1] += dp[x][y][idx]
                if direction == 'U' and y - 1 >= 0:
                    dp[x][y - 1][idx + 1] += dp[x][y][idx]
    
    return dp[0][0][len(path)]
```

## Time Complexity
- **Time**: O(n² × len(path)) - for each position and path index
- **Space**: O(n² × len(path)) - DP table

## Example Walkthrough

**Input**: path = "RDD", n = 3

**Process**:
1. Start at (0, 0)
2. After 'R': (1, 0)
3. After 'D': (1, 1)
4. After 'D': (1, 2) - valid path

**Alternative paths**:
- (0,0) → (1,0) → (1,1) → (2,1) - invalid (out of bounds)
- (0,0) → (1,0) → (1,1) → (0,1) - invalid (out of bounds)

**Output**: 1 (only one valid path)

## Problem Variations

### Variation 1: Multiple Paths
**Problem**: Find all valid paths that match the description.

**Approach**: Use backtracking to generate all paths.

### Variation 2: Weighted Grid
**Problem**: Each cell has a weight. Find path with maximum/minimum weight.

**Approach**: Modify DP to track path weights.

### Variation 3: Constrained Movement
**Problem**: Some directions are forbidden at certain positions.

**Solution**: Add constraints to movement validation.

### Variation 4: Cyclic Grid
**Problem**: Grid wraps around edges (toroidal).

**Approach**: Use modulo arithmetic for boundary checking.

### Variation 5: Path Optimization
**Problem**: Find shortest/longest valid path matching description.

**Approach**: Use BFS or modified DP for path length.

### Variation 6: Probability Paths
**Problem**: Each direction has a probability. Find expected number of valid paths.

**Approach**: Use probability DP with expected values.

## Advanced Optimizations

### 1. State Compression
```python
def count_paths_compressed(path, n):
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1
    
    for dir in path:
        new_dp = [[0] * n for _ in range(n)]
        
        for x in range(n):
            for y in range(n):
                if dp[x][y] == 0:
                    continue
                
                # Apply direction
                nx, ny = x, y
                if dir == 'R':
                    nx += 1
                elif dir == 'D':
                    ny += 1
                elif dir == 'L':
                    nx -= 1
                elif dir == 'U':
                    ny -= 1
                
                if 0 <= nx < n and 0 <= ny < n:
                    new_dp[nx][ny] += dp[x][y]
        
        dp = new_dp
    
    return dp[0][0]
```

### 2. Matrix Exponentiation
```python
# For repeated patterns, use matrix exponentiation
def matrix_multiply(a, b, n):
    result = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    
    return result
```

## Related Problems
- [Grid Paths](../grid_paths_analysis/)
- [Knight Moves Grid](../knight_moves_grid_analysis/)
- [Two Knights](../two_knights_analysis/)

## Practice Problems
1. **CSES**: Grid Path Description
2. **LeetCode**: Similar path counting problems
3. **AtCoder**: Grid-based DP problems

## Key Takeaways
1. **Dynamic Programming** is essential for path counting
2. **Boundary checking** prevents invalid paths
3. **State representation** affects time and space complexity
4. **Memoization** can significantly improve performance
5. **Matrix operations** help with repeated patterns
6. **State compression** reduces memory usage
7. **Path validation** is crucial for correct counting
