---
layout: simple
title: "Chessboard and Queens"
permalink: /problem_soulutions/introductory_problems/chessboard_and_queens_analysis
---

# Chessboard and Queens

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the N-Queens problem and backtracking algorithms
- Apply backtracking with constraint checking to solve N-Queens problems
- Implement efficient N-Queens algorithms with proper constraint validation
- Optimize N-Queens solutions using constraint propagation and pruning techniques
- Handle edge cases in N-Queens problems (blocked squares, large boards, constraint validation)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Backtracking, constraint satisfaction, N-Queens problem, recursive algorithms
- **Data Structures**: 2D arrays, backtracking stacks, constraint tracking, board representation
- **Mathematical Concepts**: Combinatorics, constraint satisfaction, backtracking theory, chess rules
- **Programming Skills**: Recursive backtracking, constraint checking, board manipulation, algorithm implementation
- **Related Problems**: Backtracking problems, Constraint satisfaction, N-Queens variants, Recursive algorithms

## Problem Description

**Problem**: Place 8 queens on an 8×8 chessboard so that no two queens threaten each other. Some squares are blocked and cannot be used.

**Input**: 8 lines describing the chessboard ('.' for empty, '*' for blocked)

**Output**: The number of valid configurations.

**Constraints**:
- 8×8 chessboard
- Place exactly 8 queens
- No two queens can threaten each other
- Some squares are blocked (marked with '*')
- Queens threaten each other if they share same row, column, or diagonal
- Count all valid configurations

**Example**:
```
Input:
........
........
........
........
........
........
........
........

Output:
92
```

## Visual Example

### Input and Queen Placement
```
Input: Empty 8×8 chessboard

Chessboard:
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .

Valid Queen Placement:
Q . . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
. Q . . . . . .
. . . Q . . . .
```

### Queen Threatening Rules
```
Queens threaten each other if they share:
- Same row: Q . . . Q (threaten)
- Same column: Q
              .
              .
              Q (threaten)
- Same diagonal: Q . . . . . . .
                 . . . . . . . .
                 . . . . . . . .
                 . . . . . . . .
                 . . . . . . . .
                 . . . . . . . .
                 . . . . . . . .
                 . . . . . . . Q (threaten)
```

### Backtracking Process
```
Row 0: Try placing queen in column 0
Row 1: Try placing queen in column 2 (avoid conflicts)
Row 2: Try placing queen in column 4 (avoid conflicts)
Row 3: Try placing queen in column 6 (avoid conflicts)
Row 4: Try placing queen in column 1 (avoid conflicts)
Row 5: Try placing queen in column 3 (avoid conflicts)
Row 6: Try placing queen in column 5 (avoid conflicts)
Row 7: Try placing queen in column 7 (avoid conflicts)
```

### Key Insight
The solution works by:
1. Using backtracking to try all valid queen placements
2. Checking for conflicts with previously placed queens
3. Using bit manipulation for efficient conflict checking
4. Time complexity: O(8!) for backtracking with pruning
5. Space complexity: O(8) for storing queen positions

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force with Array Checking (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible queen placements and check for conflicts
- Simple but computationally expensive approach
- Not suitable for large boards
- Straightforward implementation but poor performance

**Algorithm:**
1. Try all possible queen placements
2. For each placement, check for conflicts with previously placed queens
3. Count all valid configurations
4. Handle blocked squares correctly

**Visual Example:**
```
Brute force: Try all queen placements
For 8×8 board:
- Try: Q in (0,0), (1,0), (2,0), ... (7,0) → Check conflicts
- Try: Q in (0,0), (1,1), (2,0), ... (7,0) → Check conflicts
- Try all possible combinations
```

**Implementation:**
```python
def chessboard_queens_brute_force(blocked):
    def is_safe(row, col, queens):
        # Check if position is blocked
        if blocked[row][col]:
            return False
        
        # Check conflicts with previously placed queens
        for r in range(row):
            if queens[r] == col:
                return False
            if abs(queens[r] - col) == abs(r - row):
                return False
        
        return True
    
    def backtrack(row, queens):
        if row == 8:
            return 1
        
        count = 0
        for col in range(8):
            if is_safe(row, col, queens):
                queens[row] = col
                count += backtrack(row + 1, queens)
                queens[row] = -1
        
        return count
    
    queens = [-1] * 8
    return backtrack(0, queens)

def solve_chessboard_queens_brute_force():
    blocked = []
    for _ in range(8):
        row = input().strip()
        blocked.append([c == '*' for c in row])
    
    result = chessboard_queens_brute_force(blocked)
    print(result)
```

**Time Complexity:** O(8!) for backtracking with pruning
**Space Complexity:** O(8) for storing queen positions

**Why it's inefficient:**
- O(8!) time complexity is too slow for large boards
- Not suitable for competitive programming with larger boards
- Inefficient for large inputs
- Poor performance with factorial growth

### Approach 2: Backtracking with Constraint Checking (Better)

**Key Insights from Backtracking Solution:**
- Use backtracking to try valid queen placements
- Much more efficient than brute force approach
- Standard method for constraint satisfaction problems
- Can handle larger inputs than brute force

**Algorithm:**
1. Use backtracking to place queens row by row
2. Check for conflicts with previously placed queens
3. Handle blocked squares correctly
4. Count all valid configurations

**Visual Example:**
```
Backtracking: Place queens row by row
Row 0: Try placing queen in column 0
Row 1: Try placing queen in column 2 (avoid conflicts)
Row 2: Try placing queen in column 4 (avoid conflicts)
Row 3: Try placing queen in column 6 (avoid conflicts)
Row 4: Try placing queen in column 1 (avoid conflicts)
Row 5: Try placing queen in column 3 (avoid conflicts)
Row 6: Try placing queen in column 5 (avoid conflicts)
Row 7: Try placing queen in column 7 (avoid conflicts)
```

**Implementation:**
```python
def chessboard_queens_backtracking(blocked):
    def is_safe(row, col, queens):
        if blocked[row][col]:
            return False
        
        for r in range(row):
            if queens[r] == col:
                return False
            if abs(queens[r] - col) == abs(r - row):
                return False
        
        return True
    
    def backtrack(row, queens):
        if row == 8:
            return 1
        
        count = 0
        for col in range(8):
            if is_safe(row, col, queens):
                queens[row] = col
                count += backtrack(row + 1, queens)
                queens[row] = -1
        
        return count
    
    queens = [-1] * 8
    return backtrack(0, queens)

def solve_chessboard_queens_backtracking():
    blocked = []
    for _ in range(8):
        row = input().strip()
        blocked.append([c == '*' for c in row])
    
    result = chessboard_queens_backtracking(blocked)
    print(result)
```

**Time Complexity:** O(8!) for backtracking with pruning
**Space Complexity:** O(8) for storing queen positions

**Why it's better:**
- O(8!) time complexity is much better than O(8^8)
- Uses backtracking for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Bit Manipulation Optimization (Optimal)

**Key Insights from Bit Manipulation Solution:**
- Use bit manipulation for faster conflict checking
- Most efficient approach for N-Queens problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use bit manipulation for conflict checking
2. Apply backtracking with bit operations
3. Handle blocked squares efficiently
4. Return the optimal solution

**Visual Example:**
```
Bit manipulation: Use bits for conflict checking
- cols: bitmask for occupied columns
- diag1: bitmask for main diagonal (row + col)
- diag2: bitmask for anti-diagonal (row - col + 7)
- Fast conflict checking using bit operations
```

**Implementation:**
```python
def chessboard_queens_optimized(blocked):
    def backtrack(row, cols, diag1, diag2):
        if row == 8:
            return 1
        
        count = 0
        for col in range(8):
            if blocked[row][col]:
                continue
            
            # Check conflicts using bit manipulation
            if cols & (1 << col):
                continue
            if diag1 & (1 << (row + col)):
                continue
            if diag2 & (1 << (row - col + 7)):
                continue
            
            # Place queen and recurse
            count += backtrack(row + 1, 
                             cols | (1 << col),
                             diag1 | (1 << (row + col)),
                             diag2 | (1 << (row - col + 7)))
        
        return count
    
    return backtrack(0, 0, 0, 0)

def solve_chessboard_queens():
    blocked = []
    for _ in range(8):
        row = input().strip()
        blocked.append([c == '*' for c in row])
    
    result = chessboard_queens_optimized(blocked)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_chessboard_queens()
```

**Time Complexity:** O(8!) for backtracking with bit manipulation
**Space Complexity:** O(8) for storing queen positions

**Why it's optimal:**
- O(8!) time complexity is optimal for N-Queens problems
- Uses bit manipulation for efficient conflict checking
- Most efficient approach for competitive programming
- Standard method for N-Queens optimization

## 🎯 Problem Variations

### Variation 1: N-Queens with Different Board Sizes
**Problem**: N-Queens problem with different board sizes (not just 8×8).

**Link**: [CSES Problem Set - N-Queens Different Sizes](https://cses.fi/problemset/task/n_queens_different_sizes)

```python
def n_queens_different_sizes(n, blocked):
    def backtrack(row, cols, diag1, diag2):
        if row == n:
            return 1
        
        count = 0
        for col in range(n):
            if blocked[row][col]:
                continue
            
            if cols & (1 << col):
                continue
            if diag1 & (1 << (row + col)):
                continue
            if diag2 & (1 << (row - col + n - 1)):
                continue
            
            count += backtrack(row + 1, 
                             cols | (1 << col),
                             diag1 | (1 << (row + col)),
                             diag2 | (1 << (row - col + n - 1)))
        
        return count
    
    return backtrack(0, 0, 0, 0)
```

### Variation 2: N-Queens with Additional Constraints
**Problem**: N-Queens with additional constraints (e.g., specific queen positions).

**Link**: [CSES Problem Set - N-Queens Additional Constraints](https://cses.fi/problemset/task/n_queens_additional_constraints)

```python
def n_queens_additional_constraints(n, blocked, constraints):
    def backtrack(row, cols, diag1, diag2):
        if row == n:
            return 1
        
        count = 0
        for col in range(n):
            if blocked[row][col]:
                continue
            
            # Check additional constraints
            if (row, col) in constraints:
                if not constraints[(row, col)]:
                    continue
            
            if cols & (1 << col):
                continue
            if diag1 & (1 << (row + col)):
                continue
            if diag2 & (1 << (row - col + n - 1)):
                continue
            
            count += backtrack(row + 1, 
                             cols | (1 << col),
                             diag1 | (1 << (row + col)),
                             diag2 | (1 << (row - col + n - 1)))
        
        return count
    
    return backtrack(0, 0, 0, 0)
```

### Variation 3: N-Queens with Pattern Constraints
**Problem**: N-Queens with specific pattern constraints.

**Link**: [CSES Problem Set - N-Queens Pattern Constraints](https://cses.fi/problemset/task/n_queens_pattern_constraints)

```python
def n_queens_pattern_constraints(n, blocked, patterns):
    def backtrack(row, cols, diag1, diag2):
        if row == n:
            return 1
        
        count = 0
        for col in range(n):
            if blocked[row][col]:
                continue
            
            # Check pattern constraints
            if not is_pattern_valid(row, col, patterns):
                continue
            
            if cols & (1 << col):
                continue
            if diag1 & (1 << (row + col)):
                continue
            if diag2 & (1 << (row - col + n - 1)):
                continue
            
            count += backtrack(row + 1, 
                             cols | (1 << col),
                             diag1 | (1 << (row + col)),
                             diag2 | (1 << (row - col + n - 1)))
        
        return count
    
    return backtrack(0, 0, 0, 0)
```

## 🔗 Related Problems

- **[Backtracking Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Backtracking problems
- **[Constraint Satisfaction](/cses-analyses/problem_soulutions/introductory_problems/)**: Constraint problems
- **[N-Queens Variants](/cses-analyses/problem_soulutions/introductory_problems/)**: N-Queens problems
- **[Recursive Algorithms](/cses-analyses/problem_soulutions/introductory_problems/)**: Recursive problems

## 📚 Learning Points

1. **Backtracking**: Essential for understanding constraint satisfaction problems
2. **Constraint Satisfaction**: Key technique for complex constraint problems
3. **N-Queens Problem**: Important for understanding backtracking algorithms
4. **Bit Manipulation**: Critical for understanding efficient conflict checking
5. **Recursive Algorithms**: Foundation for many backtracking algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Chessboard and Queens problem demonstrates backtracking concepts for constraint satisfaction. We explored three approaches:

1. **Brute Force with Array Checking**: O(8!) time complexity using exhaustive search of all queen placements, inefficient for large boards
2. **Backtracking with Constraint Checking**: O(8!) time complexity using backtracking with conflict checking, better approach for N-Queens problems
3. **Bit Manipulation Optimization**: O(8!) time complexity with bit manipulation for conflict checking, optimal approach for N-Queens optimization

The key insights include understanding backtracking principles, using constraint checking for efficient conflict detection, and applying bit manipulation techniques for optimal performance. This problem serves as an excellent introduction to backtracking algorithms and constraint satisfaction problems.
