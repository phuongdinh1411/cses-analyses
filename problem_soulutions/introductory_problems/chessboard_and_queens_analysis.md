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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Place 8 queens on an 8×8 chessboard
- No two queens can threaten each other
- Some squares are blocked and cannot be used
- Count all valid configurations

**Key Observations:**
- Queens threaten each other if they share same row, column, or diagonal
- We need to place exactly one queen per row
- We can use backtracking to try all valid placements

### Step 2: Backtracking Approach
**Idea**: Try placing queens row by row, checking for conflicts.

```python
def solve_queens(blocked):
    def is_safe(row, col):
        # Check if position is blocked
        if blocked[row][col]:
            return False
        
        # Check column conflicts
        for r in range(row):
            if queens[r] == col:
                return False
        
        # Check diagonal conflicts
        for r in range(row):
            if abs(queens[r] - col) == abs(r - row):
                return False
        
        return True
    
    def backtrack(row):
        if row == 8:
            return 1
        
        count = 0
        for col in range(8):
            if is_safe(row, col):
                queens[row] = col
                count += backtrack(row + 1)
                queens[row] = -1
        
        return count
    
    queens = [-1] * 8
    return backtrack(0)
```

**Why this works:**
- We place one queen per row
- Check for conflicts with previously placed queens
- Count all valid configurations

### Step 3: Optimized Solution
**Idea**: Use bit manipulation for faster conflict checking.

```python
def solve_optimized(blocked):
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
```

**Why this is better:**
- Faster conflict checking using bit operations
- More efficient than checking arrays
- Cleaner code structure

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_chessboard_queens():
    # Read blocked squares
    blocked = []
    for _ in range(8):
        row = input().strip()
        blocked.append([c == '*' for c in row])
    
    def backtrack(row, cols, diag1, diag2):
        if row == 8:
            return 1
        
        count = 0
        for col in range(8):
            if blocked[row][col]:
                continue
            
            if cols & (1 << col):
                continue
            if diag1 & (1 << (row + col)):
                continue
            if diag2 & (1 << (row - col + 7)):
                continue
            
            count += backtrack(row + 1, 
                             cols | (1 << col),
                             diag1 | (1 << (row + col)),
                             diag2 | (1 << (row - col + 7)))
        
        return count
    
    return backtrack(0, 0, 0, 0)

# Main execution
if __name__ == "__main__":
    result = solve_chessboard_queens()
    print(result)
```

**Why this works:**
- Efficient backtracking with bit manipulation
- Handles blocked squares correctly
- Counts all valid configurations

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    # Test with empty board
    empty_board = [[False] * 8 for _ in range(8)]
    result = solve_test(empty_board)
    print(f"Empty board: {result} configurations")
    
    # Test with some blocked squares
    blocked_board = [[False] * 8 for _ in range(8)]
    blocked_board[0][0] = True  # Block top-left corner
    result = solve_test(blocked_board)
    print(f"Blocked corner: {result} configurations")

def solve_test(blocked):
    def backtrack(row, cols, diag1, diag2):
        if row == 8:
            return 1
        
        count = 0
        for col in range(8):
            if blocked[row][col]:
                continue
            
            if cols & (1 << col):
                continue
            if diag1 & (1 << (row + col)):
                continue
            if diag2 & (1 << (row - col + 7)):
                continue
            
            count += backtrack(row + 1, 
                             cols | (1 << col),
                             diag1 | (1 << (row + col)),
                             diag2 | (1 << (row - col + 7)))
        
        return count
    
    return backtrack(0, 0, 0, 0)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Worst Case**: O(8!) - we try all possible queen placements
- **Average Case**: Much faster due to early termination
- **Space**: O(8) - recursion depth

### Why This Solution Works
- **Complete**: Tries all valid configurations
- **Efficient**: Uses bit manipulation for fast conflict checking
- **Correct**: Handles all constraints properly

## 🎨 Visual Example

### Input Example
```
Empty 8×8 chessboard (all squares available):
........
........
........
........
........
........
........
........
```

### Chessboard Visualization
```
8×8 Chessboard with coordinates:
   0 1 2 3 4 5 6 7
0  . . . . . . . .
1  . . . . . . . .
2  . . . . . . . .
3  . . . . . . . .
4  . . . . . . . .
5  . . . . . . . .
6  . . . . . . . .
7  . . . . . . . .
```

### Queen Placement Process
```
Row 0: Try placing queen in each column
- Column 0: ✓ (no conflicts)
- Column 1: ✓ (no conflicts)
- ...
- Column 7: ✓ (no conflicts)

Row 1: Try placing queen in each column
- Column 0: ✗ (conflict with row 0, column 0)
- Column 1: ✗ (conflict with row 0, column 1)
- Column 2: ✓ (no conflicts)
- ...

Row 2: Try placing queen in each column
- Check conflicts with queens in rows 0 and 1
- Continue until all 8 queens are placed
```

### Conflict Detection
```
Queen at (row, col) conflicts with:
1. Same column: col
2. Main diagonal: row + col
3. Anti-diagonal: row - col + 7

Example: Queen at (2, 3)
- Column conflicts: column 3
- Main diagonal: positions where row + col = 5
- Anti-diagonal: positions where row - col = -1
```

### Backtracking Example
```
Step 1: Place queen at (0, 0)
Q . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .

Step 2: Place queen at (1, 2)
Q . . . . . . .
. . Q . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .

Step 3: Try placing queen at (2, 4)
Q . . . . . . .
. . Q . . . . .
. . . . Q . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .

Continue until all 8 queens are placed...
```

### Bit Manipulation
```
Use bit masks to track conflicts:

Columns:    00000000 (no columns occupied)
Main diag:  00000000 (no main diagonals occupied)
Anti-diag:  00000000 (no anti-diagonals occupied)

After placing queen at (0, 0):
Columns:    00000001 (column 0 occupied)
Main diag:  00000001 (main diagonal 0 occupied)
Anti-diag:  10000000 (anti-diagonal 7 occupied)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Backtracking    │ O(8!)        │ O(8)         │ Try all      │
│                 │              │              │ valid        │
│                 │              │              │ placements   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bit Manipulation│ O(8!)        │ O(1)         │ Fast conflict│
│                 │              │              │ checking     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Constraint      │ O(8!)        │ O(8)         │ Prune        │
│ Propagation     │              │              │ invalid      │
│                 │              │              │ branches     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Backtracking Pattern**
- Place one queen per row
- Check conflicts with previously placed queens
- Backtrack when no valid placement is possible

### 2. **Conflict Detection**
- **Column conflicts**: Use bit mask for occupied columns
- **Diagonal conflicts**: Use bit masks for both diagonals
- **Blocked squares**: Check before placing queen

### 3. **Bit Manipulation**
- Use bits to represent occupied positions
- Fast conflict checking with bitwise operations
- Efficient state representation

## 🎯 Problem Variations

### Variation 1: N-Queens Problem
**Problem**: Place N queens on N×N board without conflicts.

```python
def n_queens(n):
    def backtrack(row, cols, diag1, diag2):
        if row == n:
            return 1
        
        count = 0
        for col in range(n):
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

### Variation 2: Weighted Queens
**Problem**: Each square has a weight. Find placement with maximum total weight.

```python
def weighted_queens(weights):
    def backtrack(row, cols, diag1, diag2, current_weight):
        if row == 8:
            return current_weight
        
        max_weight = 0
        for col in range(8):
            if cols & (1 << col):
                continue
            if diag1 & (1 << (row + col)):
                continue
            if diag2 & (1 << (row - col + 7)):
                continue
            
            weight = backtrack(row + 1, 
                             cols | (1 << col),
                             diag1 | (1 << (row + col)),
                             diag2 | (1 << (row - col + 7)),
                             current_weight + weights[row][col])
            max_weight = max(max_weight, weight)
        
        return max_weight
    
    return backtrack(0, 0, 0, 0, 0)
```

### Variation 3: Minimum Queens
**Problem**: Find minimum number of queens to cover all squares.

```python
def minimum_queens(board):
    # This is a more complex problem requiring different approach
    # Similar to minimum dominating set problem
    pass
```

### Variation 4: Queens with Different Powers
**Problem**: Some queens can move like rooks, others like bishops.

```python
def mixed_queens(board, queen_types):
    # queen_types[i] = type of queen in row i
    # Different conflict checking for different queen types
    pass
```

## 🔗 Related Problems

- **[Two Knights](/cses-analyses/problem_soulutions/introductory_problems/two_knights_analysis)**: Chess piece placement
- **[Permutations](/cses-analyses/problem_soulutions/introductory_problems/permutations_analysis)**: Backtracking problems
- **[Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)**: Constraint satisfaction

## 📚 Learning Points

1. **Backtracking**: Systematic search with pruning
2. **Bit Manipulation**: Efficient state representation
3. **Constraint Satisfaction**: Handling multiple constraints
4. **Optimization**: Early termination and pruning

---

**This is a great introduction to backtracking and constraint satisfaction problems!** 🎯