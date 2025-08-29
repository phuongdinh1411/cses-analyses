---
layout: simple
title: "Grid Coloring I Analysis"
permalink: /problem_soulutions/introductory_problems/grid_coloring_i_analysis
---


# Grid Coloring I Analysis

## Problem Description

Given an n×n grid, color each cell with one of k colors such that no two adjacent cells (sharing an edge) have the same color. Find the number of valid colorings.

## Key Insights

### 1. Graph Coloring Problem
- Each cell is a vertex in the graph
- Adjacent cells are connected by edges
- Need to color vertices so no adjacent vertices have same color
- This is a classic graph coloring problem

### 2. Chromatic Number
- Minimum number of colors needed: 2 (for grid)
- Maximum number of colors: n² (each cell different color)
- For k colors, count all valid colorings

### 3. Dynamic Programming
- Use DP with state: (current position, color configuration)
- Track colors of cells that affect current cell
- Use bit manipulation for efficient state representation

## Solution Approach

### Method 1: Recursive with Memoization
```python
class Solution:
    def __init__(self):
        self.dp = {}
        self.n = 0
        self.k = 0
    
    def solve(self, row, col, prev_colors):
        if row == self.n:
            return 1
        if col == self.n:
            return self.solve(row + 1, 0, 0)
        
        state = (row, col, prev_colors)
        if state in self.dp:
            return self.dp[state]
        
        count = 0
        
        # Try each color
        for color in range(self.k):
            valid = True
            
            # Check left neighbor
            if col > 0 and ((prev_colors >> (col - 1)) & 1) == color:
                valid = False
            
            # Check top neighbor
            if row > 0 and ((prev_colors >> (self.n + col)) & 1) == color:
                valid = False
            
            if valid:
                new_prev = prev_colors
                new_prev |= (color << col)
                count += self.solve(row, col + 1, new_prev)
        
        self.dp[state] = count
        return count
    
    def count_colorings(self, grid_size, num_colors):
        self.n = grid_size
        self.k = num_colors
        self.dp = {}
        
        return self.solve(0, 0, 0)
```

### Method 2: Iterative DP
```python
def count_colorings_iterative(n, k):
    dp = [[0] * (1 << n) for _ in range(n * n + 1)]
    dp[0][0] = 1
    
    for pos in range(n * n):
        row = pos // n
        col = pos % n
        
        for mask in range(1 << n):
            if dp[pos][mask] == 0:
                continue
            
            for color in range(k):
                valid = True
                
                # Check left neighbor
                if col > 0 and ((mask >> (col - 1)) & 1) == color:
                    valid = False
                
                # Check top neighbor (stored in different part of mask)
                if row > 0 and ((mask >> (n + col)) & 1) == color:
                    valid = False
                
                if valid:
                    new_mask = mask
                    new_mask |= (color << col)
                    dp[pos + 1][new_mask] += dp[pos][mask]
    
    return dp[n * n][0]
```

## Time Complexity
- **Time**: O(n² × k × 2^n) - for each position, color, and state
- **Space**: O(n² × 2^n) - DP table

## Example Walkthrough

**Input**: n = 2, k = 3

**Process**:
1. Start with empty grid
2. Color (0,0) with color 0
3. Color (0,1) with color 1 (different from left)
4. Color (1,0) with color 1 (different from top)
5. Color (1,1) with color 0 (different from left and top)

**Valid colorings**:
```
0 1    0 2    1 0    1 2    2 0    2 1
1 0    1 2    0 1    0 2    1 2    1 0
```

**Output**: 6 valid colorings

## Problem Variations

### Variation 1: Fixed Colors
**Problem**: Some cells have pre-assigned colors.

**Approach**: Modify DP to respect fixed colors.

### Variation 2: Weighted Coloring
**Problem**: Each color has a weight. Find minimum/maximum weight coloring.

**Approach**: Track total weight in DP state.

### Variation 3: Connectivity Constraints
**Problem**: Cells of same color must form connected components.

**Approach**: Use union-find to track connectivity.

### Variation 4: Circular Grid
**Problem**: Grid wraps around edges (toroidal).

**Solution**: Modify boundary checking for circular adjacency.

### Variation 5: Diagonal Constraints
**Problem**: Diagonal cells cannot have same color.

**Approach**: Add diagonal checking to validation.

### Variation 6: Color Frequency
**Problem**: Each color must appear exactly k times.

**Approach**: Track color frequencies in DP state.

## Advanced Optimizations

### 1. Symmetry Breaking
```python
def count_colorings_symmetry(n, k):
    # Use symmetry to reduce search space
    # Only consider canonical colorings
    dp = [[0] * (1 << n) for _ in range(n * n + 1)]
    
    # Start with canonical first row
    for color in range(k):
        dp[n][1 << color] = 1
    
    # Continue with rest of grid...
    return dp[n * n][0]
```

### 2. Inclusion-Exclusion
```python
def count_colorings_inclusion_exclusion(n, k):
    total = 1
    for i in range(n * n):
        total *= k
    
    # Subtract invalid colorings using inclusion-exclusion
    for mask in range(1, 1 << (n * n)):
        # Count colorings violating edges in mask
        # Add/subtract based on parity
        pass
    
    return total
```

### 3. Matrix Tree Theorem
```python
# For special cases, use matrix tree theorem
# Count spanning trees in dual graph
def count_colorings_matrix_tree(n, k):
    # Construct Laplacian matrix
    # Count spanning trees
    # Multiply by k^(number of components)
    pass
```

## Related Problems
- [Grid Coloring II](/cses-analyses/problem_soulutions/grid_coloring_ii_analysis)
- [Chessboard and Queens](/cses-analyses/problem_soulutions/introductory_problems/chessboard_and_queens_analysis)
- [Two Knights](/cses-analyses/problem_soulutions/introductory_problems/two_knights_analysis)

## Practice Problems
1. ****: Grid Coloring I
2. **LeetCode**: Similar graph coloring problems
3. **AtCoder**: Constraint satisfaction problems

## Key Takeaways
1. **Graph coloring** is a fundamental algorithmic problem
2. **Dynamic Programming** with state compression is essential
3. **Bit manipulation** helps represent color configurations efficiently
4. **Symmetry breaking** can significantly reduce search space
5. **Inclusion-exclusion** provides alternative counting approach
6. **Matrix operations** help with special cases
7. **Constraint validation** must be carefully implemented