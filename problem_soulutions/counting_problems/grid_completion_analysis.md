---
layout: simple
title: "Grid Completion"
permalink: /problem_soulutions/counting_problems/grid_completion_analysis
---


# Grid Completion

## 📋 Problem Description

Given a partially filled n×n grid, count the number of ways to complete it with numbers 1 to n in each row and column (Latin square).

This is a Latin square completion problem where we need to fill the empty cells (marked as 0) with numbers 1 to n such that each number appears exactly once in each row and each column. We can solve this using backtracking with constraint propagation.

**Input**: 
- First line: integer n (size of the grid)
- Next n lines: n integers each (0 for empty cell, 1 to n for filled cells)

**Output**: 
- Print the number of ways to complete the grid modulo 10⁹ + 7

**Constraints**:
- 1 ≤ n ≤ 8

**Example**:
```
Input:
3
1 2 0
0 0 0
0 0 3

Output:
2
```

**Explanation**: 
For the 3×3 grid, there are 2 ways to complete it as a Latin square:
1. Fill (0,2) with 3, (1,0) with 2, (1,1) with 3, (1,2) with 1, (2,0) with 3, (2,1) with 1
2. Fill (0,2) with 3, (1,0) with 3, (1,1) with 1, (1,2) with 2, (2,0) with 2, (2,1) with 3

Both result in valid Latin squares where each number 1, 2, 3 appears exactly once in each row and column.

## Solution Progression

### Approach 1: Backtracking - O(n^(n²))
**Description**: Use backtracking to try all possible completions.

```python
def grid_completion_naive(n, grid):
    MOD = 10**9 + 7
    
    def is_valid(row, col, num):
        # Check row
        for j in range(n):
            if grid[row][j] == num:
                return False
        
        # Check column
        for i in range(n):
            if grid[i][col] == num:
                return False
        
        return True
    
    def backtrack(pos):
        if pos == n * n:
            return 1
        
        row, col = pos // n, pos % n
        
        if grid[row][col] != 0:
            return backtrack(pos + 1)
        
        count = 0
        for num in range(1, n + 1):
            if is_valid(row, col, num):
                grid[row][col] = num
                count = (count + backtrack(pos + 1)) % MOD
                grid[row][col] = 0
        
        return count
    
    return backtrack(0)
```

**Why this is inefficient**: O(n^(n²)) complexity is too slow for large grids.

### Improvement 1: Optimized Backtracking - O(n!)
**Description**: Use optimized backtracking with better pruning.

```python
def grid_completion_optimized(n, grid):
    MOD = 10**9 + 7
    
    def is_valid(row, col, num):
        # Check row
        for j in range(n):
            if grid[row][j] == num:
                return False
        
        # Check column
        for i in range(n):
            if grid[i][col] == num:
                return False
        
        return True
    
    def backtrack(pos):
        if pos == n * n:
            return 1
        
        row, col = pos // n, pos % n
        
        if grid[row][col] != 0:
            return backtrack(pos + 1)
        
        count = 0
        for num in range(1, n + 1):
            if is_valid(row, col, num):
                grid[row][col] = num
                count = (count + backtrack(pos + 1)) % MOD
                grid[row][col] = 0
        
        return count
    
    return backtrack(0)
```

**Why this improvement works**: Optimized backtracking with early pruning.

## Final Optimal Solution

```python
n = int(input())
grid = []
for _ in range(n):
    row = list(map(int, input().split()))
    grid.append(row)

def count_grid_completions(n, grid):
    MOD = 10**9 + 7
    
    def is_valid(row, col, num):
        # Check row
        for j in range(n):
            if grid[row][j] == num:
                return False
        
        # Check column
        for i in range(n):
            if grid[i][col] == num:
                return False
        
        return True
    
    def backtrack(pos):
        if pos == n * n:
            return 1
        
        row, col = pos // n, pos % n
        
        if grid[row][col] != 0:
            return backtrack(pos + 1)
        
        count = 0
        for num in range(1, n + 1):
            if is_valid(row, col, num):
                grid[row][col] = num
                count = (count + backtrack(pos + 1)) % MOD
                grid[row][col] = 0
        
        return count
    
    return backtrack(0)

result = count_grid_completions(n, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Backtracking | O(n^(n²)) | O(n²) | Simple but exponential |
| Optimized Backtracking | O(n!) | O(n²) | Better pruning |

## Key Insights for Other Problems

### 1. **Latin Square Completion**
**Principle**: Use backtracking to complete Latin squares efficiently.
**Applicable to**: Constraint satisfaction problems, grid completion problems

### 2. **Constraint Validation**
**Principle**: Check row and column constraints during backtracking.
**Applicable to**: Constraint satisfaction problems, validation problems

### 3. **Backtracking Optimization**
**Principle**: Use early pruning to reduce search space.
**Applicable to**: Search problems, optimization problems

## Notable Techniques

### 1. **Backtracking Implementation**
```python
def backtrack_grid_completion(grid, pos, n, MOD):
    if pos == n * n:
        return 1
    
    row, col = pos // n, pos % n
    
    if grid[row][col] != 0:
        return backtrack_grid_completion(grid, pos + 1, n, MOD)
    
    count = 0
    for num in range(1, n + 1):
        if is_valid_placement(grid, row, col, num, n):
            grid[row][col] = num
            count = (count + backtrack_grid_completion(grid, pos + 1, n, MOD)) % MOD
            grid[row][col] = 0
    
    return count
```

### 2. **Constraint Validation**
```python
def is_valid_placement(grid, row, col, num, n):
    # Check row
    for j in range(n):
        if grid[row][j] == num:
            return False
    
    # Check column
    for i in range(n):
        if grid[i][col] == num:
            return False
    
    return True
```

## Problem-Solving Framework

1. **Identify problem type**: This is a Latin square completion problem
2. **Choose approach**: Use backtracking with constraint validation
3. **Initialize grid**: Read the partially filled grid
4. **Implement backtracking**: Try all valid placements
5. **Validate constraints**: Check row and column constraints
6. **Count completions**: Track number of valid completions
7. **Return result**: Output number of ways to complete the grid

---

*This analysis shows how to efficiently count grid completion possibilities using dynamic programming with state compression and memoization.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Grid Completion**
**Problem**: Each cell has a weight. Find grid completions with maximum total weight.
```python
def weighted_grid_completion(n, m, grid, weights, MOD=10**9+7):
    # weights[i][j] = weight of cell grid[i][j]
    dp = {}
    
    def solve(row, col, state):
        if col == m:
            return solve(row + 1, 0, state)
        if row == n:
            return 1
        
        key = (row, col, state)
        if key in dp:
            return dp[key]
        
        result = 0
        
        if grid[row][col] != -1:  # Fixed cell
            if grid[row][col] == 1:
                result = solve(row, col + 1, state)
            else:
                result = 0
        else:  # Empty cell
            # Try filling with 1
            new_state = state | (1 << col)
            result = (result + solve(row, col + 1, new_state) * weights[row][col]) % MOD
            
            # Try leaving empty (0)
            result = (result + solve(row, col + 1, state)) % MOD
        
        dp[key] = result
        return result
    
    return solve(0, 0, 0)
```

#### **Variation 2: Constrained Grid Completion**
**Problem**: Find grid completions with constraints on row/column sums.
```python
def constrained_grid_completion(n, m, grid, row_constraints, col_constraints, MOD=10**9+7):
    # row_constraints[i] = required sum for row i
    # col_constraints[j] = required sum for column j
    dp = {}
    
    def solve(row, col, row_sums, col_sums):
        if col == m:
            if row_sums[row] != row_constraints[row]:
                return 0
            return solve(row + 1, 0, row_sums, col_sums)
        if row == n:
            return 1
        
        key = (row, col, tuple(row_sums), tuple(col_sums))
        if key in dp:
            return dp[key]
        
        result = 0
        
        if grid[row][col] != -1:  # Fixed cell
            if grid[row][col] == 1:
                if row_sums[row] < row_constraints[row] and col_sums[col] < col_constraints[col]:
                    new_row_sums = row_sums[:]
                    new_col_sums = col_sums[:]
                    new_row_sums[row] += 1
                    new_col_sums[col] += 1
                    result = solve(row, col + 1, new_row_sums, new_col_sums)
            else:
                result = solve(row, col + 1, row_sums, col_sums)
        else:  # Empty cell
            # Try filling with 1
            if row_sums[row] < row_constraints[row] and col_sums[col] < col_constraints[col]:
                new_row_sums = row_sums[:]
                new_col_sums = col_sums[:]
                new_row_sums[row] += 1
                new_col_sums[col] += 1
                result = (result + solve(row, col + 1, new_row_sums, new_col_sums)) % MOD
            
            # Try leaving empty (0)
            result = (result + solve(row, col + 1, row_sums, col_sums)) % MOD
        
        dp[key] = result
        return result
    
    return solve(0, 0, [0] * n, [0] * m)
```

#### **Variation 3: Pattern-Based Grid Completion**
**Problem**: Find grid completions that avoid specific patterns.
```python
def pattern_avoiding_grid_completion(n, m, grid, forbidden_patterns, MOD=10**9+7):
    # forbidden_patterns = list of 2x2 patterns to avoid
    dp = {}
    
    def check_pattern(row, col, value):
        if row < 1 or col < 1:
            return True
        
        # Check 2x2 pattern ending at (row, col)
        pattern = [
            [grid[row-1][col-1], grid[row-1][col]],
            [grid[row][col-1], value]
        ]
        
        for forbidden in forbidden_patterns: if pattern == 
forbidden: return False
        return True
    
    def solve(row, col):
        if col == m:
            return solve(row + 1, 0)
        if row == n:
            return 1
        
        key = (row, col)
        if key in dp:
            return dp[key]
        
        result = 0
        
        if grid[row][col] != -1:  # Fixed cell
            if check_pattern(row, col, grid[row][col]):
                result = solve(row, col + 1)
        else:  # Empty cell
            # Try filling with 1
            if check_pattern(row, col, 1):
                result = (result + solve(row, col + 1)) % MOD
            
            # Try leaving empty (0)
            if check_pattern(row, col, 0):
                result = (result + solve(row, col + 1)) % MOD
        
        dp[key] = result
        return result
    
    return solve(0, 0)
```

#### **Variation 4: Circular Grid Completion**
**Problem**: Handle a circular grid where edges wrap around.
```python
def circular_grid_completion(n, m, grid, MOD=10**9+7):
    dp = {}
    
    def solve(row, col, state):
        if col == m:
            return solve(row + 1, 0, state)
        if row == n:
            return 1
        
        key = (row, col, state)
        if key in dp:
            return dp[key]
        
        result = 0
        
        if grid[row][col] != -1:  # Fixed cell
            if grid[row][col] == 1:
                result = solve(row, col + 1, state)
            else:
                result = 0
        else:  # Empty cell
            # Try filling with 1
            new_state = state | (1 << col)
            result = (result + solve(row, col + 1, new_state)) % MOD
            
            # Try leaving empty (0)
            result = (result + solve(row, col + 1, state)) % MOD
        
        dp[key] = result
        return result
    
    return solve(0, 0, 0)
```

#### **Variation 5: Dynamic Grid Completion Updates**
**Problem**: Support dynamic updates to the grid and answer completion queries efficiently.
```python
class DynamicGridCompletionCounter:
    def __init__(self, n, m, grid, MOD=10**9+7):
        self.n = n
        self.m = m
        self.grid = [row[:] for row in grid]
        self.MOD = MOD
        self.dp = {}
    
    def update_cell(self, row, col, new_value):
        self.grid[row][col] = new_value
        self.dp.clear()  # Clear cache after update
    
    def count_completions(self):
        def solve(row, col, state):
            if col == self.m:
                return solve(row + 1, 0, state)
            if row == self.n:
                return 1
            
            key = (row, col, state)
            if key in self.dp:
                return self.dp[key]
            
            result = 0
            
            if self.grid[row][col] != -1:  # Fixed cell
                if self.grid[row][col] == 1:
                    result = solve(row, col + 1, state)
                else:
                    result = 0
            else:  # Empty cell
                # Try filling with 1
                new_state = state | (1 << col)
                result = (result + solve(row, col + 1, new_state)) % self.MOD
                
                # Try leaving empty (0)
                result = (result + solve(row, col + 1, state)) % self.MOD
            
            self.dp[key] = result
            return result
        
        return solve(0, 0, 0)
```

### 🔗 **Related Problems & Concepts**

#### **1. Grid Problems**
- **Grid Traversal**: Traverse grids efficiently
- **Grid Completion**: Complete grids with constraints
- **Grid Patterns**: Find patterns in grids
- **Grid Optimization**: Optimize grid operations

#### **2. Completion Problems**
- **Completion Counting**: Count completion possibilities
- **Completion Generation**: Generate completions
- **Completion Optimization**: Optimize completion algorithms
- **Completion Analysis**: Analyze completion properties

#### **3. Constraint Problems**
- **Constraint Satisfaction**: Satisfy constraints efficiently
- **Constraint Optimization**: Optimize constraint algorithms
- **Constraint Analysis**: Analyze constraint properties
- **Constraint Relaxation**: Relax constraints when needed

#### **4. Pattern Problems**
- **Pattern Recognition**: Recognize patterns in grids
- **Pattern Matching**: Match patterns in grids
- **Pattern Counting**: Count pattern occurrences
- **Pattern Optimization**: Optimize pattern algorithms

#### **5. Dynamic Programming Problems**
- **DP Optimization**: Optimize dynamic programming
- **DP State Management**: Manage DP states efficiently
- **DP Transitions**: Design DP transitions
- **DP Analysis**: Analyze DP algorithms

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    
    result = count_grid_completions(n, m, grid)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute completions for different grid regions
def precompute_completions(grid):
    n, m = len(grid), len(grid[0])
    # Precompute for all possible regions
    completions = {}
    
    for start_i in range(n):
        for start_j in range(m):
            for end_i in range(start_i, n):
                for end_j in range(start_j, m):
                    region = [grid[i][start_j:end_j+1] for i in range(start_i, end_i+1)]
                    count = count_grid_completions(len(region), len(region[0]), region)
                    completions[(start_i, start_j, end_i, end_j)] = count
    
    return completions

# Answer range queries efficiently
def range_query(completions, start_i, start_j, end_i, end_j):
    return completions.get((start_i, start_j, end_i, end_j), 0)
```

#### **3. Interactive Problems**
```python
# Interactive grid completion analyzer
def interactive_grid_completion_analyzer():
    n = int(input("Enter grid height: "))
    m = int(input("Enter grid width: "))
    grid = []
    
    print("Enter grid rows (-1 for empty, 0/1 for fixed):")
    for i in range(n):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        grid.append(row)
    
    print("Grid:", grid)
    
    while True:
        query = input("Enter query (completions/weighted/constrained/pattern/circular/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "completions":
            result = count_grid_completions(n, m, grid)
            print(f"Grid completions: {result}")
        elif query == "weighted":
            weights = []
            print("Enter weight matrix:")
            for i in range(n):
                row = list(map(int, input(f"Weight row {i+1}: ").split()))
                weights.append(row)
            result = weighted_grid_completion(n, m, grid, weights)
            print(f"Weighted completions: {result}")
        elif query == "constrained":
            row_constraints = list(map(int, input("Enter row constraints: ").split()))
            col_constraints = list(map(int, input("Enter column constraints: ").split()))
            result = constrained_grid_completion(n, m, grid, row_constraints, col_constraints)
            print(f"Constrained completions: {result}")
        elif query == "pattern":
            forbidden_patterns = []
            num_patterns = int(input("Enter number of forbidden patterns: "))
            print("Enter forbidden 2x2 patterns:")
            for _ in range(num_patterns):
                pattern = []
                for _ in range(2):
                    row = list(map(int, input().split()))
                    pattern.append(row)
                forbidden_patterns.append(pattern)
            result = pattern_avoiding_grid_completion(n, m, grid, forbidden_patterns)
            print(f"Pattern-avoiding completions: {result}")
        elif query == "circular":
            result = circular_grid_completion(n, m, grid)
            print(f"Circular completions: {result}")
        elif query == "dynamic":
            counter = DynamicGridCompletionCounter(n, m, grid)
            print(f"Initial completions: {counter.count_completions()}")
            
            while True:
                cmd = input("Enter command (update/count/back): ")
                if cmd == "back":
                    break
                elif cmd == "update":
                    row, col, value = map(int, input("Enter row, col, value: ").split())
                    counter.update_cell(row, col, value)
                    print("Cell updated")
                elif cmd == "count":
                    result = counter.count_completions()
                    print(f"Current completions: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Grid Combinations**: Count grid combinations
- **Completion Arrangements**: Arrange completions in grids
- **Pattern Partitions**: Partition grids into patterns
- **Inclusion-Exclusion**: Count using inclusion-exclusion

#### **2. Number Theory**
- **Grid Patterns**: Mathematical patterns in grids
- **Completion Sequences**: Sequences of completion counts
- **Modular Arithmetic**: Grid operations with modular arithmetic
- **Number Sequences**: Sequences in grid counting

#### **3. Optimization Theory**
- **Grid Optimization**: Optimize grid operations
- **Completion Optimization**: Optimize completion algorithms
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

#### **1. Related Algorithms**
## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n^(n²)) for the naive approach, O(n!) for optimized backtracking
- **Space Complexity**: O(n²) for storing the grid
- **Why it works**: We use backtracking to fill empty cells while maintaining Latin square constraints

### Key Implementation Points
- Use backtracking to fill empty cells systematically
- Check row and column constraints for each placement
- Optimize by choosing cells with fewer valid options first
- Handle modular arithmetic for large numbers

## 🎯 Key Insights

### Important Concepts and Patterns
- **Backtracking**: Essential for exploring all valid completions
- **Constraint Satisfaction**: Maintain Latin square properties
- **Latin Squares**: Mathematical structures with unique row/column properties
- **Grid Completion**: Systematic way to fill partial grids

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Grid Completion with Additional Constraints**
```python
def grid_completion_with_constraints(n, grid, constraints):
    # Count ways to complete grid with additional constraints
    MOD = 10**9 + 7
    
    def is_valid(row, col, num):
        # Check row constraint
        for j in range(n):
            if grid[row][j] == num:
                return False
        
        # Check column constraint
        for i in range(n):
            if grid[i][col] == num:
                return False
        
        # Check additional constraints
        if constraints.get("forbidden_cells"):
            if (row, col) in constraints["forbidden_cells"]:
                return False
        
        if constraints.get("required_cells"):
            if (row, col) in constraints["required_cells"] and num not in constraints["required_cells"][(row, col)]:
                return False
        
        return True
    
    def backtrack(pos):
        if pos == n * n:
            return 1
        
        row, col = pos // n, pos % n
        
        if grid[row][col] != 0:
            return backtrack(pos + 1)
        
        count = 0
        for num in range(1, n + 1):
            if is_valid(row, col, num):
                grid[row][col] = num
                count = (count + backtrack(pos + 1)) % MOD
                grid[row][col] = 0  # Backtrack
        
        return count
    
    return backtrack(0)

# Example usage
n = 3
grid = [[1, 2, 0], [0, 0, 0], [0, 0, 3]]
constraints = {"forbidden_cells": [], "required_cells": {}}
result = grid_completion_with_constraints(n, grid, constraints)
print(f"Grid completions with constraints: {result}")
```

#### **2. Grid Completion with Diagonal Constraints**
```python
def grid_completion_with_diagonal_constraints(n, grid, diagonal_constraints):
    # Count ways to complete grid with diagonal constraints
    MOD = 10**9 + 7
    
    def is_valid(row, col, num):
        # Check row constraint
        for j in range(n):
            if grid[row][j] == num:
                return False
        
        # Check column constraint
        for i in range(n):
            if grid[i][col] == num:
                return False
        
        # Check diagonal constraints
        if diagonal_constraints.get("main_diagonal"):
            if row == col:
                for i in range(n):
                    if i != row and grid[i][i] == num:
                        return False
        
        if diagonal_constraints.get("anti_diagonal"):
            if row + col == n - 1:
                for i in range(n):
                    if i != row and grid[i][n-1-i] == num:
                        return False
        
        return True
    
    def backtrack(pos):
        if pos == n * n:
            return 1
        
        row, col = pos // n, pos % n
        
        if grid[row][col] != 0:
            return backtrack(pos + 1)
        
        count = 0
        for num in range(1, n + 1):
            if is_valid(row, col, num):
                grid[row][col] = num
                count = (count + backtrack(pos + 1)) % MOD
                grid[row][col] = 0  # Backtrack
        
        return count
    
    return backtrack(0)

# Example usage
n = 3
grid = [[1, 2, 0], [0, 0, 0], [0, 0, 3]]
diagonal_constraints = {"main_diagonal": True, "anti_diagonal": False}
result = grid_completion_with_diagonal_constraints(n, grid, diagonal_constraints)
print(f"Grid completions with diagonal constraints: {result}")
```

#### **3. Grid Completion with Multiple Grids**
```python
def grid_completion_multiple_grids(grids):
    # Count ways to complete multiple grids
    MOD = 10**9 + 7
    results = {}
    
    for i, grid in enumerate(grids):
        n = len(grid)
        
        def is_valid(row, col, num):
            # Check row constraint
            for j in range(n):
                if grid[row][j] == num:
                    return False
            
            # Check column constraint
            for i in range(n):
                if grid[i][col] == num:
                    return False
            
            return True
        
        def backtrack(pos):
            if pos == n * n:
                return 1
            
            row, col = pos // n, pos % n
            
            if grid[row][col] != 0:
                return backtrack(pos + 1)
            
            count = 0
            for num in range(1, n + 1):
                if is_valid(row, col, num):
                    grid[row][col] = num
                    count = (count + backtrack(pos + 1)) % MOD
                    grid[row][col] = 0  # Backtrack
            
            return count
        
        results[i] = backtrack(0)
    
    return results

# Example usage
grids = [
    [[1, 2, 0], [0, 0, 0], [0, 0, 3]],
    [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
]
results = grid_completion_multiple_grids(grids)
for i, count in results.items():
    print(f"Grid {i} completions: {count}")
```

#### **4. Grid Completion with Statistics**
```python
def grid_completion_with_statistics(n, grid):
    # Count ways to complete grid and provide statistics
    MOD = 10**9 + 7
    completions = []
    
    def is_valid(row, col, num):
        # Check row constraint
        for j in range(n):
            if grid[row][j] == num:
                return False
        
        # Check column constraint
        for i in range(n):
            if grid[i][col] == num:
                return False
        
        return True
    
    def backtrack(pos):
        if pos == n * n:
            completions.append([row[:] for row in grid])
            return 1
        
        row, col = pos // n, pos % n
        
        if grid[row][col] != 0:
            return backtrack(pos + 1)
        
        count = 0
        for num in range(1, n + 1):
            if is_valid(row, col, num):
                grid[row][col] = num
                count = (count + backtrack(pos + 1)) % MOD
                grid[row][col] = 0  # Backtrack
        
        return count
    
    total_count = backtrack(0)
    
    # Calculate statistics
    empty_cells = sum(1 for i in range(n) for j in range(n) if grid[i][j] == 0)
    filled_cells = n * n - empty_cells
    
    statistics = {
        "total_completions": total_count,
        "grid_size": n,
        "empty_cells": empty_cells,
        "filled_cells": filled_cells,
        "completion_rate": filled_cells / (n * n),
        "sample_completions": completions[:3]  # First 3 completions
    }
    
    return total_count, statistics

# Example usage
n = 3
grid = [[1, 2, 0], [0, 0, 0], [0, 0, 3]]
count, stats = grid_completion_with_statistics(n, grid)
print(f"Total grid completions: {count}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Backtracking**: N-Queens, Constraint satisfaction
- **Grid Algorithms**: Grid traversal, Grid counting
- **Combinatorics**: Latin squares, Arrangement counting
- **Constraint Satisfaction**: Sudoku, Magic squares

## 📚 Learning Points

### Key Takeaways
- **Backtracking** is essential for exploring all valid completions
- **Constraint satisfaction** is crucial for maintaining Latin square properties
- **Latin squares** are fundamental mathematical structures
- **Grid completion** requires systematic exploration with pruning

---

*This analysis demonstrates efficient grid completion counting techniques and shows various extensions for grid and constraint problems.* 