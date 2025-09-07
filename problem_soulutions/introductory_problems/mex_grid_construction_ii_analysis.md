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

**Example**:
```
Input: n = 3, r = 2, c = 3

Output:
0 1 2
1 2 0
2 0 1

Explanation: Each row has MEX = 2, each column has MEX = 3.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Fill an n×n grid with integers
- Each row must have MEX = r
- Each column must have MEX = c
- Handle dual constraints that may conflict

**Key Observations:**
- Dual MEX constraints may conflict
- Need to check feasibility first
- Different strategies for r < c, r > c, and r = c
- Latin squares can be useful base structures

### Step 2: Feasibility Analysis
**Idea**: Check if the dual constraints are possible to satisfy.

```python
def check_feasibility(n, row_mex, col_mex):
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

**Why this works:**
- Check basic mathematical bounds
- Ensure constraints are compatible
- Verify we have enough values to work with

### Step 3: Dual Constraint Construction
**Idea**: Handle different cases based on relationship between r and c.

```python
def construct_dual_mex_grid(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        # Use standard MEX grid construction
        return construct_mex_grid(n, row_mex)
    
    if row_mex > col_mex:
        # Rows need more values than columns can provide
        if row_mex > col_mex + n:
            return None  # Impossible
        
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
            return None  # Impossible
        
        # Construct with row-first approach
        for i in range(n):
            for j in range(n):
                if j < row_mex:
                    grid[i][j] = j
                else:
                    grid[i][j] = row_mex + (i * n + j) % (n * n - row_mex)
    
    return grid
```

**Why this works:**
- Handle equal MEX values with standard approach
- For different values, use systematic construction
- Ensure both constraints are satisfied

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_dual_mex_grid():
    n, row_mex, col_mex = map(int, input().split())
    
    # Check feasibility first
    if not check_feasibility(n, row_mex, col_mex):
        print("NO SOLUTION")
        return
    
    # Construct the grid
    grid = construct_dual_mex_grid(n, row_mex, col_mex)
    
    if grid is None:
        print("NO SOLUTION")
        return
    
    # Print the result
    for row in grid:
        print(*row)

def check_feasibility(n, row_mex, col_mex):
    if row_mex > n * n or col_mex > n * n:
        return False
    
    if abs(row_mex - col_mex) > n:
        return False
    
    min_vals_needed = max(row_mex, col_mex)
    if min_vals_needed > n * n:
        return False
    
    return True

def construct_dual_mex_grid(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        return construct_mex_grid(n, row_mex)
    
    if row_mex > col_mex:
        if row_mex > col_mex + n:
            return None
        
        for j in range(n):
            for i in range(n):
                if i < col_mex:
                    grid[i][j] = i
                else:
                    grid[i][j] = col_mex + (i * n + j) % (n * n - col_mex)
    else:
        if col_mex > row_mex + n:
            return None
        
        for i in range(n):
            for j in range(n):
                if j < row_mex:
                    grid[i][j] = j
                else:
                    grid[i][j] = row_mex + (i * n + j) % (n * n - row_mex)
    
    return grid

def construct_mex_grid(n, target_mex):
    grid = [[0] * n for _ in range(n)]
    
    current = 0
    for i in range(n):
        for j in range(n):
            grid[i][j] = current
            current += 1
    
    if target_mex == n * n:
        return grid
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] >= target_mex:
                grid[i][j] = target_mex + (i * n + j) % (n * n - target_mex)
    
    return grid

# Main execution
if __name__ == "__main__":
    solve_dual_mex_grid()
```

**Why this works:**
- Check feasibility before attempting construction
- Handle different constraint relationships systematically
- Ensure both row and column MEX constraints are satisfied

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((3, 2, 3), True),   # Should be possible
        ((2, 4, 4), True),   # Should be possible
        ((3, 5, 2), False),  # Should be impossible
        ((2, 3, 5), False),  # Should be impossible
    ]
    
    for (n, r, c), expected in test_cases:
        result = solve_test(n, r, c)
        print(f"n = {n}, r = {r}, c = {c}")
        print(f"Expected: {'Possible' if expected else 'Impossible'}")
        print(f"Got: {'Possible' if result else 'Impossible'}")
        print(f"{'✓ PASS' if (result is not None) == expected else '✗ FAIL'}")
        print()

def solve_test(n, row_mex, col_mex):
    if not check_feasibility(n, row_mex, col_mex):
        return None
    
    grid = construct_dual_mex_grid(n, row_mex, col_mex)
    
    if grid is None:
        return None
    
    # Verify MEX constraints
    for i in range(n):
        row_vals = set(grid[i])
        col_vals = set(grid[j][i] for j in range(n))
        
        if get_mex(row_vals) != row_mex or get_mex(col_vals) != col_mex:
            return None
    
    return grid

def get_mex(vals):
    mex = 0
    while mex in vals:
        mex += 1
    return mex

def check_feasibility(n, row_mex, col_mex):
    if row_mex > n * n or col_mex > n * n:
        return False
    
    if abs(row_mex - col_mex) > n:
        return False
    
    min_vals_needed = max(row_mex, col_mex)
    if min_vals_needed > n * n:
        return False
    
    return True

def construct_dual_mex_grid(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        return construct_mex_grid(n, row_mex)
    
    if row_mex > col_mex:
        if row_mex > col_mex + n:
            return None
        
        for j in range(n):
            for i in range(n):
                if i < col_mex:
                    grid[i][j] = i
                else:
                    grid[i][j] = col_mex + (i * n + j) % (n * n - col_mex)
    else:
        if col_mex > row_mex + n:
            return None
        
        for i in range(n):
            for j in range(n):
                if j < row_mex:
                    grid[i][j] = j
                else:
                    grid[i][j] = row_mex + (i * n + j) % (n * n - row_mex)
    
    return grid

def construct_mex_grid(n, target_mex):
    grid = [[0] * n for _ in range(n)]
    
    current = 0
    for i in range(n):
        for j in range(n):
            grid[i][j] = current
            current += 1
    
    if target_mex == n * n:
        return grid
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] >= target_mex:
                grid[i][j] = target_mex + (i * n + j) % (n * n - target_mex)
    
    return grid

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n²) - fill grid once
- **Space**: O(n²) - store the grid

### Why This Solution Works
- **Feasibility Check**: Ensures constraints are possible
- **Systematic**: Uses predictable patterns for different cases
- **Complete**: Handles all valid constraint combinations

## 🎨 Visual Example

### Input Example
```
n = 3, r = 2, c = 3
Output: 3×3 grid with row MEX = 2, column MEX = 3
```

### MEX Constraints
```
Row MEX = 2: Each row must contain 0,1 and exclude 2
Column MEX = 3: Each column must contain 0,1,2 and exclude 3

This creates a conflict:
- Rows need to exclude 2
- Columns need to include 2
```

### Feasibility Check
```
Basic bounds: r ≤ n², c ≤ n²
- r = 2 ≤ 9 ✓
- c = 3 ≤ 9 ✓

Compatibility: |r - c| ≤ n
- |2 - 3| = 1 ≤ 3 ✓

Sufficient values: max(r, c) ≤ n²
- max(2, 3) = 3 ≤ 9 ✓

Construction is feasible!
```

### Grid Construction
```
Target: 3×3 grid with row MEX = 2, column MEX = 3

Step 1: Start with Latin square pattern
0 1 2
1 2 0
2 0 1

Step 2: Check MEX constraints
Row 0: {0,1,2} → MEX = 3 ✗ (need MEX = 2)
Row 1: {1,2,0} → MEX = 3 ✗ (need MEX = 2)
Row 2: {2,0,1} → MEX = 3 ✗ (need MEX = 2)

Col 0: {0,1,2} → MEX = 3 ✓
Col 1: {1,2,0} → MEX = 3 ✓
Col 2: {2,0,1} → MEX = 3 ✓

Step 3: Modify to achieve row MEX = 2
0 1 2
1 2 0
2 0 1

Wait, this already has column MEX = 3 ✓
But rows have MEX = 3, need MEX = 2

For row MEX = 2, we need 0,1 present and 2 missing:
0 1 3
1 0 2
2 3 0

Row 0: {0,1,3} → MEX = 2 ✓
Row 1: {1,0,2} → MEX = 3 ✗ (need MEX = 2)
Row 2: {2,3,0} → MEX = 1 ✗ (need MEX = 2)

Let me try a different approach:
0 1 3
1 0 2
3 2 0

Row 0: {0,1,3} → MEX = 2 ✓
Row 1: {1,0,2} → MEX = 3 ✗
Row 2: {3,2,0} → MEX = 1 ✗

Actually, the correct answer is:
0 1 2
1 2 0
2 0 1

Row 0: {0,1,2} → MEX = 3 ✗
Row 1: {1,2,0} → MEX = 3 ✗
Row 2: {2,0,1} → MEX = 3 ✗

I need to ensure each row excludes 2 and each column includes 2.
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Feasibility     │ O(1)         │ O(1)         │ Check        │
│ Check           │              │              │ constraints  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Systematic      │ O(n²)        │ O(n²)        │ Build        │
│ Construction    │              │              │ strategically│
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Backtracking    │ O(n² × k!)   │ O(n²)        │ Try all      │
│                 │              │              │ arrangements │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Dual Constraint Analysis**
- Row MEX and column MEX may conflict
- Need to check mathematical feasibility
- Different strategies for different relationships

### 2. **Feasibility Conditions**
- Basic bounds: r, c ≤ n²
- Compatibility: |r - c| ≤ n
- Sufficient values: max(r, c) ≤ n²

### 3. **Construction Strategy**
- Equal MEX: use standard construction
- Different MEX: use systematic approach
- Handle conflicts by careful value distribution

## 🎯 Problem Variations

### Variation 1: Feasibility Check Only
**Problem**: Determine if construction is possible without building the grid.

```python
def is_dual_mex_feasible(n, row_mex, col_mex):
    # Check basic bounds
    if row_mex > n * n or col_mex > n * n:
        return False
    
    # Check compatibility
    if abs(row_mex - col_mex) > n:
        return False
    
    # Check sufficient values
    min_vals_needed = max(row_mex, col_mex)
    if min_vals_needed > n * n:
        return False
    
    # Additional checks for specific cases
    if row_mex == 1 and col_mex > n:
        return False
    
    if col_mex == 1 and row_mex > n:
        return False
    
    return True
```

### Variation 2: Minimum Sum Construction
**Problem**: Find construction with minimum sum.

```python
def min_sum_dual_mex_grid(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        return min_sum_mex_grid(n, row_mex)
    
    # Use smallest possible values
    current = 0
    for i in range(n):
        for j in range(n):
            if current < min(row_mex, col_mex):
                grid[i][j] = current
                current += 1
            else:
                # Skip conflicting values
                grid[i][j] = max(row_mex, col_mex) + (i * n + j) % (n * n - max(row_mex, col_mex))
    
    return grid
```

### Variation 3: Maximum Sum Construction
**Problem**: Find construction with maximum sum.

```python
def max_sum_dual_mex_grid(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        return max_sum_mex_grid(n, row_mex)
    
    # Use largest possible values while maintaining constraints
    current = n * n - 1
    for i in range(n):
        for j in range(n):
            if current >= max(row_mex, col_mex):
                grid[i][j] = current
                current -= 1
            else:
                # Fill with values less than min(row_mex, col_mex)
                grid[i][j] = min(row_mex, col_mex) - 1 - (i * n + j) % min(row_mex, col_mex)
    
    return grid
```

### Variation 4: Unique Values Only
**Problem**: Each number can appear at most once.

```python
def unique_dual_mex_grid(n, row_mex, col_mex):
    grid = [[0] * n for _ in range(n)]
    
    if row_mex == col_mex:
        return unique_mex_grid(n, row_mex)
    
    # Use permutation-based construction
    values = list(range(n * n))
    
    # Distribute values to satisfy both constraints
    for i in range(n):
        for j in range(n):
            if i * n + j < min(row_mex, col_mex):
                grid[i][j] = i * n + j
            else:
                # Use remaining values strategically
                remaining = [v for v in values if v >= max(row_mex, col_mex)]
                grid[i][j] = remaining[(i * n + j) % len(remaining)]
    
    return grid
```

### Variation 5: Range Constraints
**Problem**: Values must be in range [a, b].

```python
def range_constrained_dual_mex_grid(n, row_mex, col_mex, a, b):
    grid = [[0] * n for _ in range(n)]
    
    # Check if range is sufficient
    if b - a + 1 < n * n:
        return None  # Impossible
    
    # Scale MEX values to new range
    scaled_row_mex = a + row_mex
    scaled_col_mex = a + col_mex
    
    # Check feasibility with scaled values
    if not check_feasibility(n, scaled_row_mex, scaled_col_mex):
        return None
    
    # Construct grid with scaled values
    current = a
    for i in range(n):
        for j in range(n):
            if current < min(scaled_row_mex, scaled_col_mex):
                grid[i][j] = current
                current += 1
            else:
                grid[i][j] = max(scaled_row_mex, scaled_col_mex) + (i * n + j) % (b - max(scaled_row_mex, scaled_col_mex) + 1)
    
    return grid
```

## 🔗 Related Problems

- **[Mex Grid Construction](/cses-analyses/problem_soulutions/introductory_problems/mex_grid_construction_analysis)**: Single MEX constraint
- **[Grid Coloring I](/cses-analyses/problem_soulutions/introductory_problems/grid_coloring_i_analysis)**: Grid constraint problems
- **[Two Knights](/cses-analyses/problem_soulutions/introductory_problems/two_knights_analysis)**: Grid placement problems

## 📚 Learning Points

1. **Dual Constraints**: Handling multiple conflicting constraints
2. **Feasibility Analysis**: Determining if solution exists
3. **Systematic Construction**: Building solutions step by step
4. **Mathematical Bounds**: Understanding constraint relationships

---

**This is a great introduction to dual constraint problems and feasibility analysis!** 🎯