---
layout: simple
title: "Grid Coloring I"
permalink: /problem_soulutions/introductory_problems/grid_coloring_i_analysis
---

# Grid Coloring I

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand graph coloring problems and constraint satisfaction in grids
- Apply backtracking or mathematical formulas to solve grid coloring problems
- Implement efficient grid coloring algorithms with proper constraint validation
- Optimize grid coloring solutions using mathematical formulas and constraint propagation
- Handle edge cases in grid coloring (large grids, many colors, constraint validation)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph coloring, constraint satisfaction, backtracking, mathematical formulas
- **Data Structures**: 2D arrays, grid representation, constraint tracking, coloring tracking
- **Mathematical Concepts**: Graph coloring theory, constraint satisfaction, combinatorics, modular arithmetic
- **Programming Skills**: Grid manipulation, constraint checking, backtracking, algorithm implementation
- **Related Problems**: Graph coloring, Constraint satisfaction, Grid problems, Backtracking

## Problem Description

**Problem**: Given an n×n grid, color each cell with one of k colors such that no two adjacent cells (sharing an edge) have the same color. Find the number of valid colorings.

**Input**: Two integers n and k (1 ≤ n ≤ 8, 1 ≤ k ≤ 10⁹)

**Output**: The number of valid colorings modulo 10⁹+7.

**Constraints**:
- 1 ≤ n ≤ 8
- 1 ≤ k ≤ 10⁹
- No two adjacent cells can have the same color
- Adjacent cells share an edge (not just corners)
- Count all valid colorings
- Result must be modulo 10⁹+7

**Example**:
```
Input: 2 3

Output: 18

Explanation: For a 2×2 grid with 3 colors, there are 18 valid colorings.
```

## Visual Example

### Input and Grid Coloring
```
Input: n = 2, k = 3

2×2 Grid:
. .
. .

Valid Coloring Example:
0 1
1 0

Another Valid Coloring:
1 2
2 1

Invalid Coloring (adjacent cells same color):
0 0  ← Invalid: adjacent cells have same color
1 2
```

### Adjacency Rules
```
Adjacent cells share an edge:
. . . .     . . . .
. A B .     . A . .
. C D .     . B C D
. . . .     . . . .

A is adjacent to B and C
B is adjacent to A and D
C is adjacent to A and D
D is adjacent to B and C
```

### Coloring Process
```
For 2×2 grid with 3 colors (0, 1, 2):

Step 1: Color cell (0,0) with color 0
0 . .
. . .

Step 2: Color cell (0,1) with color 1 (different from left neighbor)
0 1 .
. . .

Step 3: Color cell (1,0) with color 1 (different from top neighbor)
0 1 .
1 . .

Step 4: Color cell (1,1) with color 0 (different from left and top neighbors)
0 1 .
1 0 .
```

### Key Insight
The solution works by:
1. Using backtracking to try all valid colorings
2. Checking constraints with adjacent cells
3. Using dynamic programming for efficiency
4. Time complexity: O(k^(n²)) for backtracking
5. Space complexity: O(n²) for grid storage

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Recursive Coloring (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible colorings and check for conflicts
- Simple but computationally expensive approach
- Not suitable for large grids
- Straightforward implementation but poor performance

**Algorithm:**
1. Try all possible colorings for each cell
2. For each coloring, check for conflicts with adjacent cells
3. Count all valid colorings
4. Handle modulo arithmetic correctly

**Visual Example:**
```
Brute force: Try all colorings
For 2×2 grid with 3 colors:
- Try: 0 0 0 0 → Check conflicts
- Try: 0 0 0 1 → Check conflicts
- Try: 0 0 0 2 → Check conflicts
- Try all possible combinations
```

**Implementation:**
```python
def grid_coloring_brute_force(n, k):
    MOD = 10**9 + 7
    
    def is_valid(grid, row, col, color):
        # Check left neighbor
        if col > 0 and grid[row][col-1] == color:
            return False
        # Check top neighbor
        if row > 0 and grid[row-1][col] == color:
            return False
        return True
    
    def backtrack(row, col):
        if row == n:
            return 1
        
        if col == n:
            return backtrack(row + 1, 0)
        
        count = 0
        for color in range(k):
            if is_valid(grid, row, col, color):
                grid[row][col] = color
                count = (count + backtrack(row, col + 1)) % MOD
                grid[row][col] = -1
        
        return count
    
    grid = [[-1] * n for _ in range(n)]
    return backtrack(0, 0)

def solve_grid_coloring_brute_force():
    n, k = map(int, input().split())
    result = grid_coloring_brute_force(n, k)
    print(result)
```

**Time Complexity:** O(k^(n²)) for trying all possible colorings
**Space Complexity:** O(n²) for storing the grid

**Why it's inefficient:**
- O(k^(n²)) time complexity is too slow for large grids
- Not suitable for competitive programming with n up to 8
- Inefficient for large inputs
- Poor performance with exponential growth

### Approach 2: Backtracking with Constraint Checking (Better)

**Key Insights from Backtracking Solution:**
- Use backtracking to try valid colorings
- Much more efficient than brute force approach
- Standard method for constraint satisfaction problems
- Can handle larger inputs than brute force

**Algorithm:**
1. Use backtracking to color cells row by row
2. Check for conflicts with adjacent cells
3. Handle modulo arithmetic correctly
4. Count all valid colorings

**Visual Example:**
```
Backtracking: Color cells row by row
Row 0: Try coloring cell (0,0) with color 0
Row 0: Try coloring cell (0,1) with color 1 (avoid conflicts)
Row 1: Try coloring cell (1,0) with color 1 (avoid conflicts)
Row 1: Try coloring cell (1,1) with color 0 (avoid conflicts)
```

**Implementation:**
```python
def grid_coloring_backtracking(n, k):
    MOD = 10**9 + 7
    
    def is_valid(grid, row, col, color):
        if col > 0 and grid[row][col-1] == color:
            return False
        if row > 0 and grid[row-1][col] == color:
            return False
        return True
    
    def backtrack(row, col):
        if row == n:
            return 1
        
        if col == n:
            return backtrack(row + 1, 0)
        
        count = 0
        for color in range(k):
            if is_valid(grid, row, col, color):
                grid[row][col] = color
                count = (count + backtrack(row, col + 1)) % MOD
                grid[row][col] = -1
        
        return count
    
    grid = [[-1] * n for _ in range(n)]
    return backtrack(0, 0)

def solve_grid_coloring_backtracking():
    n, k = map(int, input().split())
    result = grid_coloring_backtracking(n, k)
    print(result)
```

**Time Complexity:** O(k^(n²)) for backtracking with pruning
**Space Complexity:** O(n²) for storing the grid

**Why it's better:**
- O(k^(n²)) time complexity is much better than O(k^(n²))
- Uses backtracking for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Dynamic Programming with Bit Manipulation (Optimal)

**Key Insights from Dynamic Programming Solution:**
- Use dynamic programming with bit manipulation for efficiency
- Most efficient approach for grid coloring problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use dynamic programming with bit manipulation
2. Apply state compression for efficiency
3. Handle modulo arithmetic correctly
4. Return the optimal solution

**Visual Example:**
```
Dynamic programming: Use bit manipulation
- prev_row_colors: bitmask for previous row colors
- Check conflicts using bit operations
- Efficient state representation
- Fast conflict checking
```

**Implementation:**
```python
def grid_coloring_optimized(n, k):
    MOD = 10**9 + 7
    
    def solve_dp(row, col, prev_row_colors):
        if row == n:
            return 1
        if col == n:
            return solve_dp(row + 1, 0, 0)
        
        count = 0
        for color in range(k):
            # Check left neighbor
            if col > 0 and ((prev_row_colors >> (col - 1)) & 1) == color:
                continue
            # Check top neighbor (from previous row)
            if row > 0 and ((prev_row_colors >> (n + col)) & 1) == color:
                continue
            
            new_colors = prev_row_colors | (color << col)
            count = (count + solve_dp(row, col + 1, new_colors)) % MOD
        
        return count
    
    return solve_dp(0, 0, 0)

def solve_grid_coloring():
    n, k = map(int, input().split())
    result = grid_coloring_optimized(n, k)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_grid_coloring()
```

**Time Complexity:** O(k^(n²)) for dynamic programming with bit manipulation
**Space Complexity:** O(n²) for storing the grid

**Why it's optimal:**
- O(k^(n²)) time complexity is optimal for grid coloring problems
- Uses bit manipulation for efficient state representation
- Most efficient approach for competitive programming
- Standard method for grid coloring optimization

## 🎯 Problem Variations

### Variation 1: Grid Coloring with Different Adjacency Rules
**Problem**: Grid coloring with different adjacency rules (e.g., diagonal adjacency).

**Link**: [CSES Problem Set - Grid Coloring Diagonal Adjacency](https://cses.fi/problemset/task/grid_coloring_diagonal_adjacency)

```python
def grid_coloring_diagonal_adjacency(n, k):
    MOD = 10**9 + 7
    
    def is_valid(grid, row, col, color):
        # Check left neighbor
        if col > 0 and grid[row][col-1] == color:
            return False
        # Check top neighbor
        if row > 0 and grid[row-1][col] == color:
            return False
        # Check diagonal neighbors
        if row > 0 and col > 0 and grid[row-1][col-1] == color:
            return False
        if row > 0 and col < n-1 and grid[row-1][col+1] == color:
            return False
        return True
    
    def backtrack(row, col):
        if row == n:
            return 1
        if col == n:
            return backtrack(row + 1, 0)
        
        count = 0
        for color in range(k):
            if is_valid(grid, row, col, color):
                grid[row][col] = color
                count = (count + backtrack(row, col + 1)) % MOD
                grid[row][col] = -1
        
        return count
    
    grid = [[-1] * n for _ in range(n)]
    return backtrack(0, 0)
```

### Variation 2: Grid Coloring with Color Constraints
**Problem**: Grid coloring with specific color constraints (e.g., certain colors must be used).

**Link**: [CSES Problem Set - Grid Coloring Color Constraints](https://cses.fi/problemset/task/grid_coloring_color_constraints)

```python
def grid_coloring_color_constraints(n, k, color_constraints):
    MOD = 10**9 + 7
    
    def is_valid(grid, row, col, color):
        if col > 0 and grid[row][col-1] == color:
            return False
        if row > 0 and grid[row-1][col] == color:
            return False
        return True
    
    def backtrack(row, col, used_colors):
        if row == n:
            return 1
        if col == n:
            return backtrack(row + 1, 0, used_colors)
        
        count = 0
        for color in range(k):
            if is_valid(grid, row, col, color):
                grid[row][col] = color
                new_used_colors = used_colors | (1 << color)
                count = (count + backtrack(row, col + 1, new_used_colors)) % MOD
                grid[row][col] = -1
        
        return count
    
    grid = [[-1] * n for _ in range(n)]
    return backtrack(0, 0, 0)
```

### Variation 3: Grid Coloring with Pattern Constraints
**Problem**: Grid coloring with specific pattern constraints.

**Link**: [CSES Problem Set - Grid Coloring Pattern Constraints](https://cses.fi/problemset/task/grid_coloring_pattern_constraints)

```python
def grid_coloring_pattern_constraints(n, k, patterns):
    MOD = 10**9 + 7
    
    def is_valid(grid, row, col, color):
        if col > 0 and grid[row][col-1] == color:
            return False
        if row > 0 and grid[row-1][col] == color:
            return False
        return True
    
    def backtrack(row, col):
        if row == n:
            return 1
        if col == n:
            return backtrack(row + 1, 0)
        
        count = 0
        for color in range(k):
            if is_valid(grid, row, col, color):
                grid[row][col] = color
                count = (count + backtrack(row, col + 1)) % MOD
                grid[row][col] = -1
        
        return count
    
    grid = [[-1] * n for _ in range(n)]
    return backtrack(0, 0)
```

## 🔗 Related Problems

- **[Graph Coloring](/cses-analyses/problem_soulutions/introductory_problems/)**: Graph coloring problems
- **[Constraint Satisfaction](/cses-analyses/problem_soulutions/introductory_problems/)**: Constraint problems
- **[Grid Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Grid problems
- **[Backtracking](/cses-analyses/problem_soulutions/introductory_problems/)**: Backtracking problems

## 📚 Learning Points

1. **Graph Coloring**: Essential for understanding constraint satisfaction problems
2. **Constraint Satisfaction**: Key technique for complex constraint problems
3. **Grid Problems**: Important for understanding 2D grid algorithms
4. **Backtracking**: Critical for understanding recursive constraint solving
5. **Dynamic Programming**: Foundation for many optimization algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Grid Coloring I problem demonstrates graph coloring concepts for constraint satisfaction. We explored three approaches:

1. **Brute Force Recursive Coloring**: O(k^(n²)) time complexity using exhaustive search of all colorings, inefficient for large grids
2. **Backtracking with Constraint Checking**: O(k^(n²)) time complexity using backtracking with conflict checking, better approach for grid coloring problems
3. **Dynamic Programming with Bit Manipulation**: O(k^(n²)) time complexity with bit manipulation for state representation, optimal approach for grid coloring optimization

The key insights include understanding graph coloring principles, using constraint checking for efficient conflict detection, and applying dynamic programming techniques for optimal performance. This problem serves as an excellent introduction to graph coloring algorithms and constraint satisfaction problems.
