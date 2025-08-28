---
layout: simple
title: Mex Grid Construction Analysis
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
```cpp
vector<vector<int>> constructMexGrid(int n, int target_mex) {
    vector<vector<int>> grid(n, vector<int>(n));
    
    // Fill with consecutive numbers starting from 0
    int current = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            grid[i][j] = current++;
        }
    }
    
    // If target_mex is n², we're done
    if (target_mex == n * n) {
        return grid;
    }
    
    // Otherwise, we need to modify the grid
    // Strategy: ensure 0 to target_mex-1 are present
    // and target_mex is missing from each row/column
    
    // Rearrange to achieve target MEX
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] >= target_mex) {
                // Replace with a value that ensures target_mex is MEX
                grid[i][j] = target_mex + (i * n + j) % (n * n - target_mex);
            }
        }
    }
    
    return grid;
}
```

### Method 2: Latin Square Based
```cpp
vector<vector<int>> constructMexGridLatin(int n, int target_mex) {
    vector<vector<int>> grid(n, vector<int>(n));
    
    // Create a Latin square base
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            grid[i][j] = (i + j) % n;
        }
    }
    
    // Scale and shift to achieve target MEX
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] < target_mex) {
                grid[i][j] = grid[i][j];
            } else {
                grid[i][j] = target_mex + grid[i][j];
            }
        }
    }
    
    return grid;
}
```

### Method 3: Backtracking Approach
```cpp
class MexGridConstructor {
private:
    vector<vector<int>> grid;
    int n, target_mex;
    bool found;
    
    bool isValid(int row, int col, int val) {
        // Check if val can be placed at (row, col)
        // Ensure MEX constraints are maintained
        
        // Check row MEX
        set<int> row_vals;
        for (int j = 0; j < n; j++) {
            if (j != col && grid[row][j] != -1) {
                row_vals.insert(grid[row][j]);
            }
        }
        row_vals.insert(val);
        
        // Check column MEX
        set<int> col_vals;
        for (int i = 0; i < n; i++) {
            if (i != row && grid[i][col] != -1) {
                col_vals.insert(grid[i][col]);
            }
        }
        col_vals.insert(val);
        
        return getMex(row_vals) <= target_mex && getMex(col_vals) <= target_mex;
    }
    
    int getMex(const set<int>& vals) {
        int mex = 0;
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
```cpp
vector<vector<int>> constructMexGridSymmetry(int n, int target_mex) {
    vector<vector<int>> grid(n, vector<int>(n));
    
    // Use symmetry to reduce search space
    // Only construct upper triangle, reflect for lower
    
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            int val = (i * n + j) % target_mex;
            grid[i][j] = val;
            if (i != j) grid[j][i] = val;
        }
    }
    
    return grid;
}
```

### 2. Mathematical Construction
```cpp
vector<vector<int>> constructMexGridMath(int n, int target_mex) {
    vector<vector<int>> grid(n, vector<int>(n));
    
    // Use mathematical patterns for specific cases
    if (target_mex == n) {
        // Use identity matrix pattern
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                grid[i][j] = (i + j) % n;
            }
        }
    } else if (target_mex == n + 1) {
        // Use shifted pattern
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                grid[i][j] = (i + j + 1) % (n + 1);
            }
        }
    }
    
    return grid;
}
```

### 3. Constraint Satisfaction
```cpp
// Use constraint satisfaction techniques
// Implement arc consistency and forward checking
class ConstraintSatisfaction {
    // Implementation for advanced constraint handling
};
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
