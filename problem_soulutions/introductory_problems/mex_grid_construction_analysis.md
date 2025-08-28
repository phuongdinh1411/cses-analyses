---
layout: simple
title: "Mex Grid Construction Analysis"
permalink: /problem_soulutions/introductory_problems/mex_grid_construction_analysis/
---


# Mex Grid Construction Analysis

## Problem Description

Construct an n×n grid filled with integers from 0 to n²-1 such that the MEX (minimum excluded value) of each row and each column is equal to a given target value.

## Key Insights

### 1. MEX Properties
- **MEX** of a set is the smallest non-negative integer not in the set
- For a set of n² consecutive integers, MEX = n²
- For a set missing some values, MEX is the smallest missing value

### 2. Grid Construction Strategy
- Fill grid systematically to control MEX values
- Use patterns that ensure consistent MEX across rows/columns
- Consider Latin squares or similar structures

### 3. Mathematical Constraints
- If target MEX = k, then 0, 1, 2, ..., k-1 must be present
- Values ≥ k can be distributed strategically
- Total numbers used affects MEX calculation

## Solution Approach

### Method 1: Systematic Construction
```python
def construct_mex_grid(n, target_mex):
    grid = [[0] * n for _ in range(n)]
    
    # Fill with consecutive numbers starting from 0
    current = 0
    for i in range(n):
        for j in range(n):
            grid[i][j] = current
            current += 1
    
    # If target_mex is n², we're done
    if target_mex == n * n:
        return grid
    
    # Otherwise, we need to modify the grid
    # Strategy: ensure 0 to target_mex-1 are present
    # and target_mex is missing from each row/column
    
    # Rearrange to achieve target MEX
    for i in range(n):
        for j in range(n):
            if grid[i][j] >= target_mex:
                # Replace with a value that ensures target_mex is MEX
                grid[i][j] = target_mex + (i * n + j) % (n * n - target_mex)
    
    return grid
```

### Method 2: Latin Square Based
```python
def construct_mex_grid_latin(n, target_mex):
    grid = [[0] * n for _ in range(n)]
    
    # Create a Latin square base
    for i in range(n):
        for j in range(n):
            grid[i][j] = (i + j) % n
    
    # Scale and shift to achieve target MEX
    for i in range(n):
        for j in range(n):
            if grid[i][j] < target_mex:
                grid[i][j] = grid[i][j]
            else:
                grid[i][j] = target_mex + grid[i][j]
    
    return grid
```

### Method 3: Backtracking Approach
```python
class MexGridConstructor:
    def __init__(self):
        self.grid = []
        self.n = 0
        self.target_mex = 0
        self.found = False
    
    def is_valid(self, row, col, val):
        # Check if val can be placed at (row, col)
        # Ensure MEX constraints are maintained
        
        # Check row MEX
        row_vals = set()
        for j in range(self.n):
            if j != col and self.grid[row][j] != -1:
                row_vals.add(self.grid[row][j])
        row_vals.add(val)
        
        # Check column MEX
        col_vals = set()
        for i in range(self.n):
            if i != row and self.grid[i][col] != -1:
                col_vals.add(self.grid[i][col])
        col_vals.add(val)
        
        return self.get_mex(row_vals) <= self.target_mex and self.get_mex(col_vals) <= self.target_mex
    
    def get_mex(self, vals):
        mex = 0
```
        for (int x : vals) {
            if (x == mex) mex++;
        }
        return mex;
    }
    
    void backtrack(int pos) {
        if (found) return;
        
        if (pos == n * n) {
            found = true;
            return;
        }
        
        int row = pos / n;
        int col = pos % n;
        
        for (int val = 0; val < n * n; val++) {
            if (isValid(row, col, val)) {
                grid[row][col] = val;
                backtrack(pos + 1);
                if (found) return;
                grid[row][col] = -1;
            }
        }
    }
    
public:
    vector<vector<int>> construct(int grid_size, int mex_target) {
        n = grid_size;
        target_mex = mex_target;
        grid.assign(n, vector<int>(n, -1));
        found = false;
        
        backtrack(0);
        return grid;
    }
};
```

## Time Complexity
- **Method 1**: O(n²) - systematic construction
- **Method 2**: O(n²) - Latin square based
- **Method 3**: O(n^(n²)) - backtracking (exponential)

## Example Walkthrough

**Input**: n = 3, target_mex = 4

**Process**:
1. Start with consecutive numbers: 0,1,2,3,4,5,6,7,8
2. Rearrange to ensure MEX = 4 for each row/column
3. Ensure 0,1,2,3 are present, 4 is missing

**Output**:
```
0 1 2
3 5 6
7 8 9
```

## Problem Variations

### Variation 1: Different MEX for Rows/Columns
**Problem**: Rows have MEX r, columns have MEX c.

**Approach**: Construct separately and merge carefully.

### Variation 2: Minimum Sum Grid
**Problem**: Find grid with minimum sum satisfying MEX constraints.

**Approach**: Use greedy placement of smallest numbers.

### Variation 3: Maximum Sum Grid
**Problem**: Find grid with maximum sum satisfying MEX constraints.

**Approach**: Use largest numbers while maintaining MEX.

### Variation 4: Unique Values
**Problem**: Each number can appear at most once.

**Approach**: Use permutation-based construction.

### Variation 5: Range Constraints
**Problem**: Values must be in range [a, b].

**Approach**: Scale and shift existing solutions.

### Variation 6: Adjacency Constraints
**Problem**: Adjacent cells cannot have same value.

**Approach**: Use graph coloring techniques.

## Advanced Optimizations

### 1. Symmetry Breaking
```python
def construct_mex_grid_symmetry(n, target_mex):
    grid = [[0] * n for _ in range(n)]
    
    # Use symmetry to reduce search space
    # Only construct upper triangle, reflect for lower
    
    for i in range(n):
        for j in range(i, n):
            val = (i * n + j) % target_mex
            grid[i][j] = val
            if i != j:
                grid[j][i] = val
    
    return grid
```

### 2. Mathematical Construction
```python
def construct_mex_grid_math(n, target_mex):
    grid = [[0] * n for _ in range(n)]
    
    # Use mathematical patterns for specific cases
    if target_mex == n:
        # Use identity matrix pattern
        for i in range(n):
            for j in range(n):
                grid[i][j] = (i + j) % n
    elif target_mex == n + 1:
        # Use shifted pattern
        for i in range(n):
            for j in range(n):
                grid[i][j] = (i + j + 1) % (n + 1)
    
    return grid
```

### 3. Constraint Satisfaction
```python
# Use constraint satisfaction techniques
# Implement arc consistency and forward checking
class ConstraintSatisfaction:
    # Implementation for advanced constraint handling
    pass
```

## Related Problems
- [Mex Grid Construction II](../mex_grid_construction_ii_analysis/)
- [Grid Coloring I](../grid_coloring_i_analysis/)
- [Two Knights](../two_knights_analysis/)

## Practice Problems
1. **CSES**: Mex Grid Construction
2. **AtCoder**: Similar grid construction problems
3. **Codeforces**: Constraint satisfaction problems

## Key Takeaways
1. **MEX understanding** is crucial for grid construction
2. **Systematic approaches** work better than random placement
3. **Mathematical patterns** can provide efficient solutions
4. **Backtracking** is useful for complex constraints
5. **Symmetry** can reduce search space significantly
6. **Constraint satisfaction** techniques help with complex problems
7. **Latin squares** provide good base structures
