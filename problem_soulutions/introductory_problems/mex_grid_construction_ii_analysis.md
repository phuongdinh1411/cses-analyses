---
layout: simple
title: "Mex Grid Construction II Analysis"
permalink: /problem_soulutions/introductory_problems/mex_grid_construction_ii_analysis
---


# Mex Grid Construction II Analysis

## Problem Description

Construct an n×n grid filled with integers such that the MEX (minimum excluded value) of each row is equal to r and the MEX of each column is equal to c, where r and c are given target values.

## Key Insights

### 1. Dual MEX Constraints
- **Row MEX**: Each row must have MEX = r
- **Column MEX**: Each column must have MEX = c
- **Conflict resolution**: Rows and columns may have conflicting requirements

### 2. Feasibility Conditions
- If r > c: Each row needs values 0 to r-1, but columns can only have MEX ≤ c
- If c > r: Each column needs values 0 to c-1, but rows can only have MEX ≤ r
- If r = c: Standard MEX grid construction

### 3. Construction Strategy
- Use different approaches based on relationship between r and c
- Consider Latin squares with modifications
- Use systematic placement to satisfy both constraints

## Solution Approach

### Method 1: Dual Constraint Construction
```python
def construct_dual_mex_grid(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        # Use standard MEX grid construction
        return construct_mex_grid(n, row_mex)
    
    if row_mex > col_mex:
        # Rows need more values than columns can provide
        # This is generally impossible for large differences
        if row_mex > col_mex + n:
            return []  # Impossible
        
        # Construct with column-first approach
        for j in range(n):
            for i in range(n):
                if i < col_mex:
                    grid[i][j] = i
                else:
                    grid[i][j] = col_mex + (i * n + j) % (n * n - col_mex)
    else:
        # Columns need more values than rows can provide
        if col_mex > row_mex + n:
            return []  # Impossible
        
        # Construct with row-first approach
        for i in range(n):
            for j in range(n):
                if j < row_mex:
                    grid[i][j] = j
                else:
                    grid[i][j] = row_mex + (i * n + j) % (n * n - row_mex)
    
    return grid
```

### Method 2: Latin Square Modification
```python
def construct_dual_mex_latin(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    # Start with Latin square
    for i in range(n):
        for j in range(n):
            grid[i][j] = (i + j) % n
    
    # Modify to satisfy dual constraints
    for i in range(n):
        for j in range(n):
            val = grid[i][j]
            
            # Adjust for row MEX
            if val >= row_mex:
                val = row_mex + (val - row_mex) % (n - row_mex)
            
            # Adjust for column MEX
            if val >= col_mex:
                val = col_mex + (val - col_mex) % (n - col_mex)
            
            grid[i][j] = val
    
    return grid
```

### Method 3: Backtracking with Dual Constraints
```python
class DualMexConstructor:
    def __init__(self):
        self.grid = []
        self.n = 0
        self.row_mex = 0
        self.col_mex = 0
        self.found = False
    
    def is_valid(self, row, col, val):
        # Check row MEX constraint
        row_vals = set()
        for j in range(self.n):
            if j != col and self.grid[row][j] != -1:
                row_vals.add(self.grid[row][j])
            }
        }
        row_vals.insert(val);
        if (getMex(row_vals) > row_mex) return false;
        
        // Check column MEX constraint
        set<int> col_vals;
        for (int i = 0; i < n; i++) {
            if (i != row && grid[i][col] != -1) {
                col_vals.insert(grid[i][col]);
            }
        }
        col_vals.insert(val);
        if (getMex(col_vals) > col_mex) return false;
        
        return true;
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
        
        for (int val = 0; val < max(row_mex, col_mex) + n; val++) {
            if (isValid(row, col, val)) {
                grid[row][col] = val;
                backtrack(pos + 1);
                if (found) return;
                grid[row][col] = -1;
            }
        }
    }
    
public:
    vector<vector<int>> construct(int grid_size, int r_mex, int c_mex) {
        n = grid_size;
        row_mex = r_mex;
        col_mex = c_mex;
        grid.assign(n, vector<int>(n, -1));
        found = false;
        
        backtrack(0);
        return found ? grid : vector<vector<int>>();
    }
};
```

## Time Complexity
- **Method 1**: O(n²) - systematic construction
- **Method 2**: O(n²) - Latin square modification
- **Method 3**: O(n^(n²)) - backtracking (exponential)

## Example Walkthrough

**Input**: n = 3, row_mex = 2, col_mex = 3

**Process**:
1. Start with Latin square: 0,1,2,1,2,0,2,0,1
2. Modify for row MEX = 2: ensure each row has 0,1
3. Modify for column MEX = 3: ensure each column has 0,1,2

**Output**:
```
0 1 2
1 2 0
2 0 1
```

## Problem Variations

### Variation 1: Feasibility Check
**Problem**: Determine if construction is possible.

**Approach**: Check mathematical constraints and bounds.

### Variation 2: Minimum Sum Construction
**Problem**: Find construction with minimum sum.

**Approach**: Use greedy placement of smallest numbers.

### Variation 3: Maximum Sum Construction
**Problem**: Find construction with maximum sum.

**Approach**: Use largest numbers while maintaining constraints.

### Variation 4: Unique Values
**Problem**: Each number can appear at most once.

**Approach**: Use permutation-based construction.

### Variation 5: Range Constraints
**Problem**: Values must be in range [a, b].

**Approach**: Scale and shift existing solutions.

### Variation 6: Adjacency Constraints
**Problem**: Adjacent cells cannot have same value.

**Approach**: Combine with graph coloring techniques.

## Advanced Optimizations

### 1. Feasibility Analysis
```python
def is_feasible(n, row_mex, col_mex):
    # Check if construction is possible
    
    # Basic bounds
    if row_mex > n * n or col_mex > n * n:
        return False
    
    # Check if constraints are compatible
    if abs(row_mex - col_mex) > n:
        return False
    
    # Check if we have enough distinct values
    min_vals_needed = max(row_mex, col_mex)
    if min_vals_needed > n * n:
        return False
    
    return True
```

### 2. Mathematical Construction
```python
def construct_dual_mex_math(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    # Use mathematical patterns for specific cases
    if row_mex == col_mex:
        # Use standard construction
        return construct_mex_grid(n, row_mex)
    
    if row_mex == 1 and col_mex == n: # Special 
case: rows have MEX 1, columns have MEX n
        for i in range(n):
            for j in range(n):
                grid[i][j] = j
    
    if row_mex == n and col_mex == 1:
        # Special case: rows have MEX n, columns have MEX 1
        for i in range(n):
            for j in range(n):
                grid[i][j] = i
    
    return grid
```

### 3. Constraint Propagation
```python
class ConstraintPropagator:
    # Implement constraint propagation for faster backtracking
    # Use arc consistency and forward checking
    # Maintain domain reduction for each cell
    pass
```

## Related Problems
- [Mex Grid Construction](/cses-analyses/problem_soulutions/introductory_problems/mex_grid_construction_analysis)
- [Grid Coloring I](/cses-analyses/problem_soulutions/introductory_problems/grid_coloring_i_analysis)
- [Two Knights](/cses-analyses/problem_soulutions/introductory_problems/two_knights_analysis)

## Practice Problems
1. ****: Mex Grid Construction II
2. **AtCoder**: Similar dual constraint problems
3. **Codeforces**: Constraint satisfaction problems

## Key Takeaways
1. **Dual constraints** require careful analysis of feasibility
2. **Mathematical bounds** help determine possibility
3. **Systematic construction** works better than random placement
4. **Backtracking** is useful for complex constraint combinations
5. **Latin squares** provide good base structures
6. **Constraint propagation** can speed up search
7. **Special cases** often have elegant solutions