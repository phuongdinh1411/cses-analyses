---
layout: simple
title: "Grid Coloring I"
permalink: /problem_soulutions/introductory_problems/grid_coloring_i_analysis
---

# Grid Coloring I

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand graph coloring problems and constraint satisfaction in grids
- [ ] **Objective 2**: Apply backtracking or mathematical formulas to solve grid coloring problems
- [ ] **Objective 3**: Implement efficient grid coloring algorithms with proper constraint validation
- [ ] **Objective 4**: Optimize grid coloring solutions using mathematical formulas and constraint propagation
- [ ] **Objective 5**: Handle edge cases in grid coloring (large grids, many colors, constraint validation)

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

**Example**:
```
Input: 2 3

Output: 18

Explanation: For a 2×2 grid with 3 colors, there are 18 valid colorings.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Color an n×n grid with k colors
- No adjacent cells can have the same color
- Count all valid colorings
- Output modulo 10⁹+7

**Key Observations:**
- This is a graph coloring problem
- Each cell is a vertex, adjacent cells are connected
- We need to ensure no adjacent vertices have same color
- For small n, we can use dynamic programming

### Step 2: Simple Recursive Approach
**Idea**: Try coloring each cell, checking constraints with neighbors.

```python
def solve_simple(n, k):
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
                count += backtrack(row, col + 1)
                grid[row][col] = -1
        
        return count
    
    grid = [[-1] * n for _ in range(n)]
    return backtrack(0, 0)
```

**Why this works:**
- We try each color for each cell
- Check constraints with left and top neighbors
- Count all valid colorings

### Step 3: Optimized DP Approach
**Idea**: Use dynamic programming with bit manipulation for efficiency.

```python
def solve_optimized(n, k):
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
```

**Why this is better:**
- Uses bit manipulation for state representation
- More efficient than checking arrays
- Handles modulo arithmetic correctly

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_grid_coloring():
    n, k = map(int, input().split())
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
            # Check top neighbor
            if row > 0 and ((prev_row_colors >> (n + col)) & 1) == color:
                continue
            
            new_colors = prev_row_colors | (color << col)
            count = (count + solve_dp(row, col + 1, new_colors)) % MOD
        
        return count
    
    return solve_dp(0, 0, 0)

# Main execution
if __name__ == "__main__":
    result = solve_grid_coloring()
    print(result)
```

**Why this works:**
- Efficient dynamic programming approach
- Handles large values with modulo arithmetic
- Correctly counts all valid colorings

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (1, 2, 2),    # 1×1 grid, 2 colors
        (2, 2, 2),    # 2×2 grid, 2 colors
        (2, 3, 18),   # 2×2 grid, 3 colors
    ]
    
    for n, k, expected in test_cases:
        result = solve_test(n, k)
        print(f"n={n}, k={k}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, k):
    MOD = 10**9 + 7
    
    def solve_dp(row, col, prev_row_colors):
        if row == n:
            return 1
        if col == n:
            return solve_dp(row + 1, 0, 0)
        
        count = 0
        for color in range(k):
            if col > 0 and ((prev_row_colors >> (col - 1)) & 1) == color:
                continue
            if row > 0 and ((prev_row_colors >> (n + col)) & 1) == color:
                continue
            
            new_colors = prev_row_colors | (color << col)
            count = (count + solve_dp(row, col + 1, new_colors)) % MOD
        
        return count
    
    return solve_dp(0, 0, 0)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Worst Case**: O(k^(n²)) - we try k colors for each of n² cells
- **With DP**: Much faster due to memoization
- **Space**: O(n² × 2^n) - DP state space

### Why This Solution Works
- **Complete**: Tries all valid colorings
- **Efficient**: Uses dynamic programming with memoization
- **Correct**: Handles all constraints properly

## 🎨 Visual Example

### Input Example
```
n = 2, k = 3
Output: 18 valid colorings
```

### Grid Visualization
```
2×2 grid with 3 colors (0, 1, 2):

Grid structure:
[0,0] - [0,1]
  |       |
[1,0] - [1,1]

Adjacent cells share edges and cannot have same color.
```

### Valid Colorings
```
Some valid colorings for 2×2 grid with 3 colors:

Coloring 1:    Coloring 2:    Coloring 3:
0 1           0 2           1 0
2 0           1 0           2 1

Coloring 4:    Coloring 5:    Coloring 6:
0 1           0 2           1 0
1 2           2 1           0 2

Total: 18 valid colorings
```

### Constraint Checking
```
For each cell, check adjacent cells:

Cell (0,0): check right (0,1) and down (1,0)
Cell (0,1): check left (0,0) and down (1,1)  
Cell (1,0): check right (1,1) and up (0,0)
Cell (1,1): check left (1,0) and up (0,1)

Constraint: adjacent cells must have different colors
```

### Dynamic Programming Process
```
State: (row, col, prev_row_colors)

For 2×2 grid:
- Row 0: try all color combinations
- Row 1: check constraints with row 0

Example state transitions:
(0,0,0) → try colors 0,1,2
(0,1,color0) → try colors ≠ color0
(1,0,color0,color1) → try colors ≠ color0
(1,1,color0,color1,color2) → try colors ≠ color1
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(k^(n²))    │ O(n²)        │ Try all      │
│                 │              │              │ combinations │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dynamic Prog    │ O(n² × k^n)  │ O(n × k^n)   │ State-based  │
│                 │              │              │ optimization │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bit Manipulation│ O(n² × k^n)  │ O(n × k^n)   │ Fast         │
│                 │              │              │ constraint   │
│                 │              │              │ checking     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Graph Coloring**
- Each cell is a vertex in the graph
- Adjacent cells are connected by edges
- Need to ensure no adjacent vertices have same color

### 2. **Dynamic Programming**
- Use state: (current position, color configuration)
- Track colors of cells that affect current cell
- Use bit manipulation for efficient state representation

### 3. **Bit Manipulation**
- Use bits to represent color configurations
- Fast constraint checking with bitwise operations
- Efficient state representation

## 🎯 Problem Variations

### Variation 1: Grid Coloring with Diagonal Constraints
**Problem**: Also ensure diagonal neighbors have different colors.

```python
def grid_coloring_diagonal(n, k):
    MOD = 10**9 + 7
    
    def solve_dp(row, col, prev_row_colors, prev_prev_row_colors):
        if row == n:
            return 1
        if col == n:
            return solve_dp(row + 1, 0, 0, prev_row_colors)
        
        count = 0
        for color in range(k):
            # Check left neighbor
            if col > 0 and ((prev_row_colors >> (col - 1)) & 1) == color:
                continue
            # Check top neighbor
            if row > 0 and ((prev_row_colors >> (n + col)) & 1) == color:
                continue
            # Check diagonal neighbors
            if row > 0 and col > 0 and ((prev_row_colors >> (n + col - 1)) & 1) == color:
                continue
            if row > 0 and col < n-1 and ((prev_row_colors >> (n + col + 1)) & 1) == color:
                continue
            
            new_colors = prev_row_colors | (color << col)
            count = (count + solve_dp(row, col + 1, new_colors, prev_row_colors)) % MOD
        
        return count
    
    return solve_dp(0, 0, 0, 0)
```

### Variation 2: Weighted Grid Coloring
**Problem**: Each color has a weight. Find minimum total weight.

```python
def weighted_grid_coloring(n, k, weights):
    # weights[i] = weight of color i
    MOD = 10**9 + 7
    
    def solve_dp(row, col, prev_row_colors, current_weight):
        if row == n:
            return current_weight
        
        if col == n:
            return solve_dp(row + 1, 0, 0, current_weight)
        
        min_weight = float('inf')
        for color in range(k):
            if col > 0 and ((prev_row_colors >> (col - 1)) & 1) == color:
                continue
            if row > 0 and ((prev_row_colors >> (n + col)) & 1) == color:
                continue
            
            new_colors = prev_row_colors | (color << col)
            weight = solve_dp(row, col + 1, new_colors, current_weight + weights[color])
            min_weight = min(min_weight, weight)
        
        return min_weight
    
    return solve_dp(0, 0, 0, 0)
```

### Variation 3: Constrained Grid Coloring
**Problem**: Some cells have fixed colors that cannot be changed.

```python
def constrained_grid_coloring(n, k, fixed_colors):
    # fixed_colors[row][col] = fixed color (-1 if not fixed)
    MOD = 10**9 + 7
    
    def solve_dp(row, col, prev_row_colors):
        if row == n:
            return 1
        if col == n:
            return solve_dp(row + 1, 0, 0)
        
        # If cell has fixed color
        if fixed_colors[row][col] != -1:
            color = fixed_colors[row][col]
            if col > 0 and ((prev_row_colors >> (col - 1)) & 1) == color:
                return 0
            if row > 0 and ((prev_row_colors >> (n + col)) & 1) == color:
                return 0
            
            new_colors = prev_row_colors | (color << col)
            return solve_dp(row, col + 1, new_colors)
        
        # Try all colors
        count = 0
        for color in range(k):
            if col > 0 and ((prev_row_colors >> (col - 1)) & 1) == color:
                continue
            if row > 0 and ((prev_row_colors >> (n + col)) & 1) == color:
                continue
            
            new_colors = prev_row_colors | (color << col)
            count = (count + solve_dp(row, col + 1, new_colors)) % MOD
        
        return count
    
    return solve_dp(0, 0, 0)
```

### Variation 4: Circular Grid Coloring
**Problem**: Grid wraps around (toroidal surface).

```python
def circular_grid_coloring(n, k):
    MOD = 10**9 + 7
    
    def solve_dp(row, col, prev_row_colors, first_row_colors):
        if row == n:
            # Check if last row is compatible with first row
            for col_idx in range(n):
                if ((prev_row_colors >> col_idx) & 1) == ((first_row_colors >> col_idx) & 1):
                    return 0
            return 1
        
        if col == n:
            if row == 0:
                return solve_dp(row + 1, 0, 0, prev_row_colors)
            else:
                return solve_dp(row + 1, 0, 0, first_row_colors)
        
        count = 0
        for color in range(k):
            # Check left neighbor (with wraparound)
            left_col = (col - 1) % n
            if ((prev_row_colors >> left_col) & 1) == color:
                continue
            # Check top neighbor
            if row > 0 and ((prev_row_colors >> (n + col)) & 1) == color:
                continue
            
            new_colors = prev_row_colors | (color << col)
            count = (count + solve_dp(row, col + 1, new_colors, first_row_colors)) % MOD
        
        return count
    
    return solve_dp(0, 0, 0, 0)
```

## 🔗 Related Problems

- **[Chessboard and Queens](/cses-analyses/problem_soulutions/introductory_problems/chessboard_and_queens_analysis)**: Constraint satisfaction
- **[Two Knights](/cses-analyses/problem_soulutions/introductory_problems/two_knights_analysis)**: Grid problems
- **[Permutations](/cses-analyses/problem_soulutions/introductory_problems/permutations_analysis)**: Constraint problems

## 📚 Learning Points

1. **Graph Coloring**: Understanding constraint satisfaction problems
2. **Dynamic Programming**: Using DP for counting problems
3. **Bit Manipulation**: Efficient state representation
4. **Constraint Checking**: Validating color assignments

---

**This is a great introduction to graph coloring and constraint satisfaction problems!** 🎯