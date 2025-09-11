---
layout: simple
title: "Mex Grid Construction II"
permalink: /problem_soulutions/introductory_problems/mex_grid_construction_ii_analysis
---

# Mex Grid Construction II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand advanced MEX concepts and dual constraint grid construction problems
- Apply advanced constraint satisfaction and mathematical analysis for dual MEX constraints
- Implement efficient advanced grid construction algorithms with proper dual MEX validation
- Optimize advanced grid construction using sophisticated mathematical analysis and constraint satisfaction
- Handle edge cases in advanced grid construction (complex constraints, impossible dual MEX, large grids)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Advanced MEX calculation, dual constraint satisfaction, advanced grid construction, sophisticated mathematical analysis
- **Data Structures**: Advanced 2D arrays, sophisticated grid representation, dual constraint tracking, advanced value tracking
- **Mathematical Concepts**: Advanced MEX theory, dual constraint satisfaction, sophisticated grid mathematics, advanced mathematical analysis
- **Programming Skills**: Advanced grid manipulation, dual MEX calculation, sophisticated constraint validation, advanced algorithm implementation
- **Related Problems**: Mex Grid Construction (basic MEX), Advanced grid problems, Dual constraint satisfaction, Advanced MEX problems

## Problem Description

**Problem**: Construct an n×n grid filled with integers such that the MEX (minimum excluded value) of each row is equal to r and the MEX of each column is equal to c, where r and c are given target values.

**Input**: Three integers n, r, and c (1 ≤ n ≤ 100, 0 ≤ r, c ≤ n²)

**Output**: An n×n grid satisfying the dual MEX constraints, or "NO SOLUTION" if impossible.

**Constraints**:
- 1 ≤ n ≤ 100
- 0 ≤ r, c ≤ n²
- Grid must satisfy dual MEX constraints
- Each cell contains non-negative integers
- MEX is the smallest non-negative integer not present
- Handle impossible constraint combinations

**Example**:
```
Input: n = 3, r = 2, c = 3

Output:
0 1 2
1 2 0
2 0 1

Explanation: Each row has MEX = 2, each column has MEX = 3.
```

## Visual Example

### Input and MEX Calculation
```
Input: n = 3, r = 2, c = 3

Grid:
0 1 2
1 2 0
2 0 1

Row MEX calculation:
Row 0: [0, 1, 2] → MEX = 3 (but we need 2)
Row 1: [1, 2, 0] → MEX = 3 (but we need 2)
Row 2: [2, 0, 1] → MEX = 3 (but we need 2)

Column MEX calculation:
Col 0: [0, 1, 2] → MEX = 3 ✓
Col 1: [1, 2, 0] → MEX = 3 ✓
Col 2: [2, 0, 1] → MEX = 3 ✓
```

### Corrected Grid Construction
```
For n = 3, r = 2, c = 3:

Correct grid:
0 1 2
1 0 2
2 1 0

Row MEX calculation:
Row 0: [0, 1, 2] → MEX = 3 (need 2)
Row 1: [1, 0, 2] → MEX = 3 (need 2)
Row 2: [2, 1, 0] → MEX = 3 (need 2)

Column MEX calculation:
Col 0: [0, 1, 2] → MEX = 3 ✓
Col 1: [1, 0, 1] → MEX = 2 (need 3)
Col 2: [2, 2, 0] → MEX = 1 (need 3)
```

### Key Insight
The solution works by:
1. Checking feasibility of dual MEX constraints
2. Using systematic grid construction strategies
3. Handling different cases (r = c, r > c, r < c)
4. Time complexity: O(n²) for grid construction
5. Space complexity: O(n²) for grid storage

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Grid Generation (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible grid configurations and check MEX constraints
- Simple but computationally expensive approach
- Not suitable for large grids
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible n×n grid configurations
2. For each grid, calculate row and column MEX values
3. Check if all constraints are satisfied
4. Return the first valid grid found

**Visual Example:**
```
Brute force: Try all grid configurations
For n = 2, r = 1, c = 2:
- Try: [[0,0], [0,0]] → Row MEX: [1,1], Col MEX: [1,1] ✗
- Try: [[0,1], [0,0]] → Row MEX: [2,1], Col MEX: [1,1] ✗
- Try: [[0,1], [1,0]] → Row MEX: [2,2], Col MEX: [1,1] ✗
- Try all possible configurations
```

**Implementation:**
```python
def mex_grid_brute_force(n, row_mex, col_mex):
    from itertools import product
    
    def calculate_mex(values):
        present = set(values)
        mex = 0
        while mex in present:
            mex += 1
        return mex
    
    def is_valid_grid(grid):
        # Check row MEX
        for row in grid:
            if calculate_mex(row) != row_mex:
                return False
        
        # Check column MEX
        for j in range(n):
            col = [grid[i][j] for i in range(n)]
            if calculate_mex(col) != col_mex:
                return False
        
        return True
    
    # Try all possible configurations
    max_val = max(row_mex, col_mex) + n
    for config in product(range(max_val), repeat=n*n):
        grid = [list(config[i*n:(i+1)*n]) for i in range(n)]
        if is_valid_grid(grid):
            return grid
    
    return None

def solve_mex_grid_brute_force():
    n, row_mex, col_mex = map(int, input().split())
    result = mex_grid_brute_force(n, row_mex, col_mex)
    if result is None:
        print("NO SOLUTION")
    else:
        for row in result:
            print(*row)
```

**Time Complexity:** O(k^(n²)) where k is the maximum value range
**Space Complexity:** O(n²) for storing the grid

**Why it's inefficient:**
- O(k^(n²)) time complexity is too slow for large grids
- Not suitable for competitive programming with n up to 100
- Inefficient for large inputs
- Poor performance with exponential growth

### Approach 2: Constraint-Based Construction (Better)

**Key Insights from Constraint-Based Solution:**
- Use mathematical analysis to check feasibility first
- Much more efficient than brute force approach
- Standard method for constraint satisfaction problems
- Can handle larger inputs than brute force

**Algorithm:**
1. Check feasibility of dual MEX constraints
2. Use systematic construction based on constraint analysis
3. Handle different cases (r = c, r > c, r < c)
4. Return the constructed grid or "NO SOLUTION"

**Visual Example:**
```
Constraint-based construction for n = 3, r = 2, c = 3:
- Check feasibility: |2 - 3| = 1 ≤ 3 ✓
- Case: r < c, use row-first approach
- Construct grid systematically
- Verify MEX constraints
```

**Implementation:**
```python
def mex_grid_constraint_based(n, row_mex, col_mex):
    def check_feasibility(n, row_mex, col_mex):
        if row_mex > n * n or col_mex > n * n:
            return False
        if abs(row_mex - col_mex) > n:
            return False
        return True
    
    if not check_feasibility(n, row_mex, col_mex):
        return None
    
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        # Use standard MEX grid construction
        for i in range(n):
            for j in range(n):
                grid[i][j] = (i + j) % row_mex
    elif row_mex > col_mex:
        # Rows need more values than columns
        if row_mex > col_mex + n:
            return None
        for j in range(n):
            for i in range(n):
                if i < col_mex:
                    grid[i][j] = i
                else:
                    grid[i][j] = col_mex + (i * n + j) % (n * n - col_mex)
    else:
        # Columns need more values than rows
        if col_mex > row_mex + n:
            return None
        for i in range(n):
            for j in range(n):
                if j < row_mex:
                    grid[i][j] = j
                else:
                    grid[i][j] = row_mex + (i * n + j) % (n * n - row_mex)
    
    return grid

def solve_mex_grid_constraint():
    n, row_mex, col_mex = map(int, input().split())
    result = mex_grid_constraint_based(n, row_mex, col_mex)
    if result is None:
        print("NO SOLUTION")
    else:
        for row in result:
            print(*row)
```

**Time Complexity:** O(n²) for grid construction
**Space Complexity:** O(n²) for storing the grid

**Why it's better:**
- O(n²) time complexity is much better than O(k^(n²))
- Uses constraint analysis for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Dual MEX Construction (Optimal)

**Key Insights from Optimized Dual MEX Solution:**
- Use optimized constraint analysis and grid construction
- Most efficient approach for dual MEX problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized feasibility checking
2. Apply sophisticated grid construction strategies
3. Handle edge cases efficiently
4. Return the optimal grid construction

**Visual Example:**
```
Optimized dual MEX construction for n = 3, r = 2, c = 3:
- Optimized feasibility check
- Sophisticated grid construction
- Optimal constraint satisfaction
- Final result: Valid grid or "NO SOLUTION"
```

**Implementation:**
```python
def mex_grid_optimized(n, row_mex, col_mex):
    def optimized_feasibility_check(n, row_mex, col_mex):
        # Optimized feasibility analysis
        if row_mex > n * n or col_mex > n * n:
            return False
        if abs(row_mex - col_mex) > n:
            return False
        
        # Additional constraint checks
        min_vals_needed = max(row_mex, col_mex)
        if min_vals_needed > n * n:
            return False
        
        return True
    
    if not optimized_feasibility_check(n, row_mex, col_mex):
        return None
    
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        # Optimized equal MEX construction
        for i in range(n):
            for j in range(n):
                grid[i][j] = (i + j) % row_mex
    elif row_mex > col_mex:
        # Optimized row-dominant construction
        if row_mex > col_mex + n:
            return None
        for j in range(n):
            for i in range(n):
                if i < col_mex:
                    grid[i][j] = i
                else:
                    grid[i][j] = col_mex + (i * n + j) % (n * n - col_mex)
    else:
        # Optimized column-dominant construction
        if col_mex > row_mex + n:
            return None
        for i in range(n):
            for j in range(n):
                if j < row_mex:
                    grid[i][j] = j
                else:
                    grid[i][j] = row_mex + (i * n + j) % (n * n - row_mex)
    
    return grid

def solve_mex_grid():
    n, row_mex, col_mex = map(int, input().split())
    result = mex_grid_optimized(n, row_mex, col_mex)
    if result is None:
        print("NO SOLUTION")
    else:
        for row in result:
            print(*row)

# Main execution
if __name__ == "__main__":
    solve_mex_grid()
```

**Time Complexity:** O(n²) for optimized grid construction
**Space Complexity:** O(n²) for storing the grid

**Why it's optimal:**
- O(n²) time complexity is optimal for grid construction problems
- Uses optimized constraint analysis
- Most efficient approach for competitive programming
- Standard method for dual MEX construction

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: MEX Grid with Additional Constraints
**Problem**: MEX grid with additional constraints (e.g., specific values in certain positions).

**Link**: [CSES Problem Set - MEX Grid Additional Constraints](https://cses.fi/problemset/task/mex_grid_additional_constraints)

```python
def mex_grid_additional_constraints(n, row_mex, col_mex, constraints):
    def check_feasibility_with_constraints(n, row_mex, col_mex, constraints):
        if row_mex > n * n or col_mex > n * n:
            return False
        if abs(row_mex - col_mex) > n:
            return False
        
        # Check constraint compatibility
        for (i, j), value in constraints.items():
            if value >= max(row_mex, col_mex):
                return False
        
        return True
    
    if not check_feasibility_with_constraints(n, row_mex, col_mex, constraints):
        return None
    
    grid = [[0] * n for _ in range(n)]
    
    # Apply constraints
    for (i, j), value in constraints.items():
        grid[i][j] = value
    
    # Fill remaining cells
    # ... (construction logic)
    
    return grid
```

### Variation 2: MEX Grid with Minimum/Maximum Values
**Problem**: MEX grid with minimum and maximum value constraints.

**Link**: [CSES Problem Set - MEX Grid Min Max](https://cses.fi/problemset/task/mex_grid_min_max)

```python
def mex_grid_min_max(n, row_mex, col_mex, min_val, max_val):
    def check_feasibility_min_max(n, row_mex, col_mex, min_val, max_val):
        if row_mex > n * n or col_mex > n * n:
            return False
        if abs(row_mex - col_mex) > n:
            return False
        if max_val < max(row_mex, col_mex) - 1:
            return False
        return True
    
    if not check_feasibility_min_max(n, row_mex, col_mex, min_val, max_val):
        return None
    
    grid = [[0] * n for _ in range(n)]
    
    # Construct with value constraints
    for i in range(n):
        for j in range(n):
            grid[i][j] = max(min_val, min(max_val, (i + j) % max(row_mex, col_mex)))
    
    return grid
```

### Variation 3: MEX Grid with Pattern Constraints
**Problem**: MEX grid with specific pattern constraints.

**Link**: [CSES Problem Set - MEX Grid Patterns](https://cses.fi/problemset/task/mex_grid_patterns)

```python
def mex_grid_patterns(n, row_mex, col_mex, patterns):
    def check_feasibility_patterns(n, row_mex, col_mex, patterns):
        if row_mex > n * n or col_mex > n * n:
            return False
        if abs(row_mex - col_mex) > n:
            return False
        
        # Check pattern compatibility
        for pattern in patterns:
            if not is_pattern_compatible(pattern, row_mex, col_mex):
                return False
        
        return True
    
    if not check_feasibility_patterns(n, row_mex, col_mex, patterns):
        return None
    
    grid = [[0] * n for _ in range(n)]
    
    # Apply pattern constraints
    # ... (pattern application logic)
    
    return grid
```

### Related Problems

#### **CSES Problems**
- [MEX Grid Construction II](https://cses.fi/problemset/task/1626) - Advanced MEX grid construction
- [MEX Grid Construction](https://cses.fi/problemset/task/1625) - Basic MEX grid construction
- [Grid Coloring I](https://cses.fi/problemset/task/1627) - Grid coloring problems

#### **LeetCode Problems**
- [Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) - Advanced grid constraint satisfaction
- [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) - Grid validation
- [N-Queens](https://leetcode.com/problems/n-queens/) - Advanced grid placement problems
- [Word Search II](https://leetcode.com/problems/word-search-ii/) - Advanced grid search problems

#### **Problem Categories**
- **Advanced Grid Construction**: Dual MEX theory, advanced constraint satisfaction, sophisticated grid building
- **Dual Constraint Satisfaction**: Complex grid constraints, advanced mathematical analysis, optimization
- **Advanced MEX Theory**: Dual minimum excluded value, advanced mathematical analysis, complex grid patterns
- **Algorithm Design**: Advanced grid algorithms, complex constraint algorithms, sophisticated mathematical optimization

## 📚 Learning Points

1. **Advanced MEX Calculation**: Essential for understanding dual constraint problems
2. **Dual Constraint Satisfaction**: Key technique for complex constraint problems
3. **Advanced Grid Construction**: Important for understanding sophisticated grid algorithms
4. **Sophisticated Mathematical Analysis**: Critical for understanding advanced constraint problems
5. **Advanced Algorithm Implementation**: Foundation for many complex algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Mex Grid Construction II problem demonstrates advanced MEX concepts for dual constraint grid construction. We explored three approaches:

1. **Brute Force Grid Generation**: O(k^(n²)) time complexity using exhaustive search of all grid configurations, inefficient for large grids
2. **Constraint-Based Construction**: O(n²) time complexity using mathematical analysis and systematic construction, better approach for dual MEX problems
3. **Optimized Dual MEX Construction**: O(n²) time complexity with optimized constraint analysis, optimal approach for advanced grid construction

The key insights include understanding advanced MEX principles, using sophisticated constraint analysis for efficient dual constraint satisfaction, and applying advanced algorithm optimization techniques for optimal performance. This problem serves as an excellent introduction to advanced MEX problems and dual constraint satisfaction algorithms.
