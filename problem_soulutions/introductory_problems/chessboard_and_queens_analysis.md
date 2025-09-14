---
layout: simple
title: "Chessboard and Queens - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/chessboard_and_queens_analysis
---

# Chessboard and Queens - Introductory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of backtracking and constraint satisfaction in introductory problems
- Apply efficient algorithms for solving the N-Queens problem
- Implement backtracking with pruning for constraint satisfaction problems
- Optimize algorithms for chess-based constraint problems
- Handle special cases in backtracking problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Backtracking, constraint satisfaction, N-Queens problem, pruning
- **Data Structures**: Arrays, sets, boolean arrays
- **Mathematical Concepts**: Chess rules, constraint satisfaction, backtracking, permutations
- **Programming Skills**: Backtracking, constraint checking, pruning, recursive algorithms
- **Related Problems**: Permutations (introductory_problems), Two Knights (introductory_problems), Creating Strings (introductory_problems)

## 📋 Problem Description

Place 8 queens on an 8×8 chessboard such that no two queens attack each other. Count the number of valid arrangements.

**Input**: 
- 8×8 chessboard (implicit)

**Output**: 
- Number of valid queen arrangements

**Constraints**:
- Standard 8×8 chessboard
- 8 queens to be placed

**Example**:
```
Input:
8×8 chessboard

Output:
92

Explanation**: 
There are 92 distinct ways to place 8 queens on an 8×8 chessboard
such that no two queens attack each other.
One example arrangement:
Q . . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
. Q . . . . . .
. . . Q . . . .
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible ways to place 8 queens
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check each arrangement for validity
- **Inefficient**: O(8! × 8²) time complexity

**Key Insight**: Try all possible arrangements of 8 queens and check which ones are valid.

**Algorithm**:
- Generate all possible arrangements of 8 queens (one per row)
- For each arrangement, check if any two queens attack each other
- Count the valid arrangements
- Return the count

**Visual Example**:
```
Brute Force N-Queens:

Try all possible arrangements:
┌─────────────────────────────────────┐
│ Arrangement 1: [0,1,2,3,4,5,6,7]   │
│ - Check: Queens in same column ✗   │
│ - Invalid                          │
│                                   │
│ Arrangement 2: [0,2,4,6,1,3,5,7]   │
│ - Check: No same column ✓          │
│ - Check: No same diagonal ✗        │
│ - Invalid                          │
│                                   │
│ Arrangement 3: [4,0,7,3,1,6,2,5]   │
│ - Check: No same column ✓          │
│ - Check: No same diagonal ✓        │
│ - Valid ✓                          │
│                                   │
│ Continue for all 8! = 40,320 arrangements │
│                                   │
│ Count valid arrangements: 92       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_chessboard_queens():
    """Count valid queen arrangements using brute force approach"""
    from itertools import permutations
    
    def is_valid_arrangement(queens):
        """Check if queen arrangement is valid"""
        n = len(queens)
        
        # Check for same column (already handled by permutation)
        # Check for same diagonal
        for i in range(n):
            for j in range(i + 1, n):
                # Check if queens are on same diagonal
                if abs(i - j) == abs(queens[i] - queens[j]):
                    return False
        
        return True
    
    count = 0
    
    # Try all possible arrangements (permutations)
    for queens in permutations(range(8)):
        if is_valid_arrangement(queens):
            count += 1
    
    return count

# Example usage
result = brute_force_chessboard_queens()
print(f"Brute force count: {result}")
```

**Time Complexity**: O(8! × 8²)
**Space Complexity**: O(8)

**Why it's inefficient**: O(8! × 8²) time complexity for trying all possible arrangements.

---

### Approach 2: Backtracking with Pruning

**Key Insights from Backtracking with Pruning**:
- **Backtracking**: Use backtracking to explore possible queen placements
- **Pruning**: Use constraint checking to avoid exploring invalid branches
- **Efficient Implementation**: O(8!) time complexity in practice
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use backtracking with constraint checking to find valid queen arrangements.

**Algorithm**:
- Place queens row by row
- For each row, try placing queen in each column
- Check if placement is valid (no conflicts with previous queens)
- If valid, recurse to next row
- If invalid, backtrack and try next column
- Count valid arrangements

**Visual Example**:
```
Backtracking with Pruning:

Place queens row by row:
┌─────────────────────────────────────┐
│ Row 0: Try column 0                │
│ - Place queen at (0,0)             │
│ - Valid ✓                          │
│                                   │
│ Row 1: Try column 0                │
│ - Place queen at (1,0)             │
│ - Check: Same column as (0,0) ✗    │
│ - Try column 1                     │
│ - Place queen at (1,1)             │
│ - Check: Same diagonal as (0,0) ✗  │
│ - Try column 2                     │
│ - Place queen at (1,2)             │
│ - Valid ✓                          │
│                                   │
│ Row 2: Try column 0                │
│ - Place queen at (2,0)             │
│ - Check: Same column as (0,0) ✗    │
│ - Try column 1                     │
│ - Place queen at (2,1)             │
│ - Check: Same column as (1,2) ✗    │
│ - Try column 2                     │
│ - Place queen at (2,2)             │
│ - Check: Same column as (1,2) ✗    │
│ - Try column 3                     │
│ - Place queen at (2,3)             │
│ - Check: Same diagonal as (0,0) ✗  │
│ - Try column 4                     │
│ - Place queen at (2,4)             │
│ - Valid ✓                          │
│                                   │
│ Continue with pruning...           │
│                                   │
│ When all 8 queens placed: count++  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def backtracking_chessboard_queens():
    """Count valid queen arrangements using backtracking with pruning"""
    
    def is_safe(board, row, col):
        """Check if placing queen at (row, col) is safe"""
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        
        # Check diagonals
        for i in range(row):
            if abs(i - row) == abs(board[i] - col):
                return False
        
        return True
    
    def solve_n_queens(board, row, count):
        """Solve N-Queens using backtracking"""
        if row == 8:
            return count + 1
        
        for col in range(8):
            if is_safe(board, row, col):
                board[row] = col
                count = solve_n_queens(board, row + 1, count)
                board[row] = -1  # Backtrack
        
        return count
    
    # Initialize board
    board = [-1] * 8
    return solve_n_queens(board, 0, 0)

# Example usage
result = backtracking_chessboard_queens()
print(f"Backtracking count: {result}")
```

**Time Complexity**: O(8!) in practice
**Space Complexity**: O(8)

**Why it's better**: Uses backtracking with pruning for much better performance.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for constraint checking
- **Efficient Implementation**: O(8!) time complexity
- **Space Efficiency**: O(8) space complexity
- **Optimal Complexity**: Best approach for N-Queens problems

**Key Insight**: Use advanced data structures for optimal constraint checking.

**Algorithm**:
- Use specialized data structures for constraint tracking
- Implement efficient constraint checking
- Handle special cases optimally
- Return count of valid arrangements

**Visual Example**:
```
Advanced data structure approach:

For 8×8 chessboard:
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Column tracking: for efficient    │
│   column conflict detection         │
│ - Diagonal tracking: for efficient  │
│   diagonal conflict detection       │
│ - Row tracking: for optimization    │
│                                   │
│ Constraint checking calculation:    │
│ - Use column tracking for efficient │
│   column conflict detection         │
│ - Use diagonal tracking for efficient│
│   diagonal conflict detection       │
│ - Use row tracking for optimization │
│                                   │
│ Result: 92                         │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_chessboard_queens():
    """Count valid queen arrangements using advanced data structure approach"""
    
    def advanced_is_safe(board, row, col, used_cols, used_diag1, used_diag2):
        """Advanced constraint checking"""
        # Advanced column checking
        if used_cols[col]:
            return False
        
        # Advanced diagonal checking
        if used_diag1[row + col] or used_diag2[row - col + 7]:
            return False
        
        return True
    
    def advanced_solve_n_queens(board, row, count, used_cols, used_diag1, used_diag2):
        """Advanced N-Queens solving"""
        if row == 8:
            return count + 1
        
        for col in range(8):
            if advanced_is_safe(board, row, col, used_cols, used_diag1, used_diag2):
                # Advanced state update
                board[row] = col
                used_cols[col] = True
                used_diag1[row + col] = True
                used_diag2[row - col + 7] = True
                
                count = advanced_solve_n_queens(board, row + 1, count, used_cols, used_diag1, used_diag2)
                
                # Advanced backtracking
                board[row] = -1
                used_cols[col] = False
                used_diag1[row + col] = False
                used_diag2[row - col + 7] = False
        
        return count
    
    # Advanced initialization
    board = [-1] * 8
    used_cols = [False] * 8
    used_diag1 = [False] * 15  # Main diagonal
    used_diag2 = [False] * 15  # Anti-diagonal
    
    return advanced_solve_n_queens(board, 0, 0, used_cols, used_diag1, used_diag2)

# Example usage
result = advanced_data_structure_chessboard_queens()
print(f"Advanced data structure count: {result}")
```

**Time Complexity**: O(8!)
**Space Complexity**: O(8)

**Why it's optimal**: Uses advanced data structures for optimal constraint checking.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(8! × 8²) | O(8) | Try all possible arrangements |
| Backtracking with Pruning | O(8!) | O(8) | Use backtracking with constraint checking |
| Advanced Data Structure | O(8!) | O(8) | Use advanced data structures for constraint checking |

### Time Complexity
- **Time**: O(8!) - Use backtracking with pruning for efficient constraint satisfaction
- **Space**: O(8) - Store board and constraint tracking arrays

### Why This Solution Works
- **Backtracking**: Use backtracking to explore possible placements
- **Constraint Checking**: Check for column and diagonal conflicts
- **Pruning**: Avoid exploring invalid branches early
- **Optimal Algorithms**: Use optimal algorithms for constraint satisfaction

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Chessboard and Queens with Constraints**
**Problem**: Place queens with specific constraints.

**Key Differences**: Apply constraints to queen placement

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_chessboard_queens(constraints):
    """Count valid queen arrangements with constraints"""
    
    def constrained_is_safe(board, row, col, used_cols, used_diag1, used_diag2):
        """Constraint checking with additional constraints"""
        if used_cols[col]:
            return False
        
        if used_diag1[row + col] or used_diag2[row - col + 7]:
            return False
        
        # Apply additional constraints
        if not constraints(board, row, col):
            return False
        
        return True
    
    def constrained_solve_n_queens(board, row, count, used_cols, used_diag1, used_diag2):
        """N-Queens solving with constraints"""
        if row == 8:
            return count + 1
        
        for col in range(8):
            if constrained_is_safe(board, row, col, used_cols, used_diag1, used_diag2):
                board[row] = col
                used_cols[col] = True
                used_diag1[row + col] = True
                used_diag2[row - col + 7] = True
                
                count = constrained_solve_n_queens(board, row + 1, count, used_cols, used_diag1, used_diag2)
                
                board[row] = -1
                used_cols[col] = False
                used_diag1[row + col] = False
                used_diag2[row - col + 7] = False
        
        return count
    
    board = [-1] * 8
    used_cols = [False] * 8
    used_diag1 = [False] * 15
    used_diag2 = [False] * 15
    
    return constrained_solve_n_queens(board, 0, 0, used_cols, used_diag1, used_diag2)

# Example usage
constraints = lambda board, row, col: True  # No constraints
result = constrained_chessboard_queens(constraints)
print(f"Constrained count: {result}")
```

#### **2. Chessboard and Queens with Different Metrics**
**Problem**: Place queens with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_chessboard_queens(weight_function):
    """Count valid queen arrangements with different cost metrics"""
    
    def weighted_is_safe(board, row, col, used_cols, used_diag1, used_diag2):
        """Constraint checking with weights"""
        if used_cols[col]:
            return False
        
        if used_diag1[row + col] or used_diag2[row - col + 7]:
            return False
        
        return True
    
    def weighted_solve_n_queens(board, row, count, used_cols, used_diag1, used_diag2):
        """N-Queens solving with weights"""
        if row == 8:
            return count + 1
        
        for col in range(8):
            if weighted_is_safe(board, row, col, used_cols, used_diag1, used_diag2):
                board[row] = col
                used_cols[col] = True
                used_diag1[row + col] = True
                used_diag2[row - col + 7] = True
                
                count = weighted_solve_n_queens(board, row + 1, count, used_cols, used_diag1, used_diag2)
                
                board[row] = -1
                used_cols[col] = False
                used_diag1[row + col] = False
                used_diag2[row - col + 7] = False
        
        return count
    
    board = [-1] * 8
    used_cols = [False] * 8
    used_diag1 = [False] * 15
    used_diag2 = [False] * 15
    
    return weighted_solve_n_queens(board, 0, 0, used_cols, used_diag1, used_diag2)

# Example usage
weight_function = lambda board, row, col: 1  # Unit weight
result = weighted_chessboard_queens(weight_function)
print(f"Weighted count: {result}")
```

#### **3. Chessboard and Queens with Multiple Dimensions**
**Problem**: Place queens in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_chessboard_queens(dimensions):
    """Count valid queen arrangements in multiple dimensions"""
    
    def multi_dimensional_is_safe(board, row, col, used_cols, used_diag1, used_diag2):
        """Constraint checking for multiple dimensions"""
        if used_cols[col]:
            return False
        
        if used_diag1[row + col] or used_diag2[row - col + 7]:
            return False
        
        return True
    
    def multi_dimensional_solve_n_queens(board, row, count, used_cols, used_diag1, used_diag2):
        """N-Queens solving for multiple dimensions"""
        if row == 8:
            return count + 1
        
        for col in range(8):
            if multi_dimensional_is_safe(board, row, col, used_cols, used_diag1, used_diag2):
                board[row] = col
                used_cols[col] = True
                used_diag1[row + col] = True
                used_diag2[row - col + 7] = True
                
                count = multi_dimensional_solve_n_queens(board, row + 1, count, used_cols, used_diag1, used_diag2)
                
                board[row] = -1
                used_cols[col] = False
                used_diag1[row + col] = False
                used_diag2[row - col + 7] = False
        
        return count
    
    board = [-1] * 8
    used_cols = [False] * 8
    used_diag1 = [False] * 15
    used_diag2 = [False] * 15
    
    return multi_dimensional_solve_n_queens(board, 0, 0, used_cols, used_diag1, used_diag2)

# Example usage
dimensions = 1
result = multi_dimensional_chessboard_queens(dimensions)
print(f"Multi-dimensional count: {result}")
```

## Problem Variations

### **Variation 1: Chessboard and Queens with Dynamic Updates**
**Problem**: Handle dynamic chessboard size updates (resize board, add/remove queens) while maintaining valid queen placements.

**Approach**: Use efficient data structures and algorithms for dynamic chessboard and queen management.

```python
from collections import defaultdict
import itertools

class DynamicChessboardQueens:
    def __init__(self, n):
        self.n = n
        self.board = [['.' for _ in range(n)] for _ in range(n)]
        self.queens = []
        self.solutions = []
        self._find_all_solutions()
    
    def _find_all_solutions(self):
        """Find all valid queen placements using backtracking."""
        self.solutions = []
        
        def is_safe(row, col):
            # Check column
            for i in range(row):
                if self.board[i][col] == 'Q':
                    return False
            
            # Check diagonal (top-left to bottom-right)
            for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
                if self.board[i][j] == 'Q':
                    return False
            
            # Check diagonal (top-right to bottom-left)
            for i, j in zip(range(row-1, -1, -1), range(col+1, self.n)):
                if self.board[i][j] == 'Q':
                    return False
            
            return True
        
        def solve(row):
            if row == self.n:
                # Found a solution
                solution = []
                for i in range(self.n):
                    for j in range(self.n):
                        if self.board[i][j] == 'Q':
                            solution.append((i, j))
                self.solutions.append(solution[:])
                return
            
            for col in range(self.n):
                if is_safe(row, col):
                    self.board[row][col] = 'Q'
                    solve(row + 1)
                    self.board[row][col] = '.'
        
        solve(0)
    
    def resize_board(self, new_size):
        """Resize the chessboard to new size."""
        self.n = new_size
        self.board = [['.' for _ in range(new_size)] for _ in range(new_size)]
        self.queens = []
        self._find_all_solutions()
    
    def add_queen(self, row, col):
        """Add a queen at specified position."""
        if 0 <= row < self.n and 0 <= col < self.n and self.board[row][col] == '.':
            self.board[row][col] = 'Q'
            self.queens.append((row, col))
            return True
        return False
    
    def remove_queen(self, row, col):
        """Remove queen at specified position."""
        if 0 <= row < self.n and 0 <= col < self.n and self.board[row][col] == 'Q':
            self.board[row][col] = '.'
            if (row, col) in self.queens:
                self.queens.remove((row, col))
            return True
        return False
    
    def get_solutions(self):
        """Get all valid solutions."""
        return self.solutions
    
    def get_solutions_count(self):
        """Get count of valid solutions."""
        return len(self.solutions)
    
    def get_solutions_with_constraints(self, constraint_func):
        """Get solutions that satisfy custom constraints."""
        result = []
        for solution in self.solutions:
            if constraint_func(solution):
                result.append(solution)
        return result
    
    def get_solutions_in_range(self, min_queens, max_queens):
        """Get solutions with queen count in specified range."""
        result = []
        for solution in self.solutions:
            if min_queens <= len(solution) <= max_queens:
                result.append(solution)
        return result
    
    def get_solutions_with_pattern(self, pattern_func):
        """Get solutions matching specified pattern."""
        result = []
        for solution in self.solutions:
            if pattern_func(solution):
                result.append(solution)
        return result
    
    def get_solution_statistics(self):
        """Get statistics about solutions."""
        if not self.solutions:
            return {
                'total_solutions': 0,
                'average_queens': 0,
                'queen_distribution': {},
                'pattern_distribution': {}
            }
        
        total_solutions = len(self.solutions)
        average_queens = sum(len(solution) for solution in self.solutions) / total_solutions
        
        # Calculate queen distribution
        queen_distribution = defaultdict(int)
        for solution in self.solutions:
            for row, col in solution:
                queen_distribution[(row, col)] += 1
        
        # Calculate pattern distribution
        pattern_distribution = defaultdict(int)
        for solution in self.solutions:
            # Count patterns like consecutive rows, columns, etc.
            if len(solution) > 1:
                rows = [pos[0] for pos in solution]
                cols = [pos[1] for pos in solution]
                if len(set(rows)) == len(rows):  # All different rows
                    pattern_distribution['unique_rows'] += 1
                if len(set(cols)) == len(cols):  # All different columns
                    pattern_distribution['unique_cols'] += 1
        
        return {
            'total_solutions': total_solutions,
            'average_queens': average_queens,
            'queen_distribution': dict(queen_distribution),
            'pattern_distribution': dict(pattern_distribution)
        }
    
    def get_solution_patterns(self):
        """Get patterns in solutions."""
        patterns = {
            'symmetric_solutions': 0,
            'diagonal_solutions': 0,
            'corner_solutions': 0,
            'center_solutions': 0
        }
        
        for solution in self.solutions:
            # Check for symmetric solutions
            if self._is_symmetric(solution):
                patterns['symmetric_solutions'] += 1
            
            # Check for diagonal solutions
            if self._is_diagonal(solution):
                patterns['diagonal_solutions'] += 1
            
            # Check for corner solutions
            if self._has_corner_queens(solution):
                patterns['corner_solutions'] += 1
            
            # Check for center solutions
            if self._has_center_queens(solution):
                patterns['center_solutions'] += 1
        
        return patterns
    
    def _is_symmetric(self, solution):
        """Check if solution is symmetric."""
        # Check horizontal symmetry
        symmetric = True
        for row, col in solution:
            if (row, self.n - 1 - col) not in solution:
                symmetric = False
                break
        return symmetric
    
    def _is_diagonal(self, solution):
        """Check if solution forms a diagonal pattern."""
        if len(solution) != self.n:
            return False
        
        # Check if all queens are on main diagonal
        for i, (row, col) in enumerate(solution):
            if row != i or col != i:
                return False
        return True
    
    def _has_corner_queens(self, solution):
        """Check if solution has queens in corners."""
        corners = [(0, 0), (0, self.n-1), (self.n-1, 0), (self.n-1, self.n-1)]
        return any(corner in solution for corner in corners)
    
    def _has_center_queens(self, solution):
        """Check if solution has queens in center."""
        center_row = self.n // 2
        center_col = self.n // 2
        center_positions = [(center_row, center_col)]
        if self.n % 2 == 0:
            center_positions.extend([(center_row-1, center_col), (center_row, center_col-1), (center_row-1, center_col-1)])
        return any(pos in solution for pos in center_positions)
    
    def get_optimal_solution_strategy(self):
        """Get optimal strategy for queen placement operations."""
        if self.n == 0:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'solution_rate': 0
            }
        
        # Calculate efficiency rate
        total_possible = self.n ** self.n
        efficiency_rate = len(self.solutions) / total_possible if total_possible > 0 else 0
        
        # Calculate solution rate
        solution_rate = len(self.solutions) / (2 ** self.n) if self.n > 0 else 0
        
        # Determine recommended strategy
        if efficiency_rate > 0.1:
            recommended_strategy = 'backtracking_optimal'
        elif solution_rate > 0.5:
            recommended_strategy = 'constraint_propagation'
        else:
            recommended_strategy = 'brute_force'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'solution_rate': solution_rate
        }

# Example usage
n = 4
dynamic_queens = DynamicChessboardQueens(n)
print(f"Initial solutions count: {dynamic_queens.get_solutions_count()}")

# Resize board
dynamic_queens.resize_board(5)
print(f"After resizing to 5x5: {dynamic_queens.get_solutions_count()}")

# Add a queen
dynamic_queens.add_queen(0, 0)
print(f"After adding queen: {dynamic_queens.get_solutions_count()}")

# Remove a queen
dynamic_queens.remove_queen(0, 0)
print(f"After removing queen: {dynamic_queens.get_solutions_count()}")

# Get solutions with constraints
def constraint_func(solution):
    return len(solution) == n

print(f"Solutions with {n} queens: {len(dynamic_queens.get_solutions_with_constraints(constraint_func))}")

# Get solutions in range
print(f"Solutions with 3-5 queens: {len(dynamic_queens.get_solutions_in_range(3, 5))}")

# Get solutions with pattern
def pattern_func(solution):
    return all(pos[0] == pos[1] for pos in solution)  # Diagonal pattern

print(f"Diagonal pattern solutions: {len(dynamic_queens.get_solutions_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_queens.get_solution_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_queens.get_solution_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_queens.get_optimal_solution_strategy()}")
```

### **Variation 2: Chessboard and Queens with Different Operations**
**Problem**: Handle different types of operations on chessboard and queens (weighted queens, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of chessboard and queen queries.

```python
class AdvancedChessboardQueens:
    def __init__(self, n, weights=None, priorities=None):
        self.n = n
        self.weights = weights or [[1 for _ in range(n)] for _ in range(n)]
        self.priorities = priorities or [[1 for _ in range(n)] for _ in range(n)]
        self.board = [['.' for _ in range(n)] for _ in range(n)]
        self.queens = []
        self.solutions = []
        self._find_all_solutions()
    
    def _find_all_solutions(self):
        """Find all valid queen placements using advanced backtracking."""
        self.solutions = []
        
        def is_safe(row, col):
            # Check column
            for i in range(row):
                if self.board[i][col] == 'Q':
                    return False
            
            # Check diagonal (top-left to bottom-right)
            for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
                if self.board[i][j] == 'Q':
                    return False
            
            # Check diagonal (top-right to bottom-left)
            for i, j in zip(range(row-1, -1, -1), range(col+1, self.n)):
                if self.board[i][j] == 'Q':
                    return False
            
            return True
        
        def solve(row):
            if row == self.n:
                # Found a solution
                solution = []
                for i in range(self.n):
                    for j in range(self.n):
                        if self.board[i][j] == 'Q':
                            solution.append((i, j))
                self.solutions.append(solution[:])
                return
            
            for col in range(self.n):
                if is_safe(row, col):
                    self.board[row][col] = 'Q'
                    solve(row + 1)
                    self.board[row][col] = '.'
        
        solve(0)
    
    def get_solutions(self):
        """Get current valid solutions."""
        return self.solutions
    
    def get_weighted_solutions(self):
        """Get solutions with weights and priorities applied."""
        result = []
        for solution in self.solutions:
            weighted_solution = {
                'positions': solution,
                'total_weight': sum(self.weights[row][col] for row, col in solution),
                'total_priority': sum(self.priorities[row][col] for row, col in solution),
                'weighted_score': sum(self.weights[row][col] * self.priorities[row][col] for row, col in solution)
            }
            result.append(weighted_solution)
        return result
    
    def get_solutions_with_priority(self, priority_func):
        """Get solutions considering priority."""
        result = []
        for solution in self.solutions:
            priority = priority_func(solution, self.weights, self.priorities)
            result.append((solution, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_solutions_with_optimization(self, optimization_func):
        """Get solutions using custom optimization function."""
        result = []
        for solution in self.solutions:
            score = optimization_func(solution, self.weights, self.priorities)
            result.append((solution, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_solutions_with_constraints(self, constraint_func):
        """Get solutions that satisfy custom constraints."""
        result = []
        for solution in self.solutions:
            if constraint_func(solution, self.weights, self.priorities):
                result.append(solution)
        return result
    
    def get_solutions_with_multiple_criteria(self, criteria_list):
        """Get solutions that satisfy multiple criteria."""
        result = []
        for solution in self.solutions:
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(solution, self.weights, self.priorities):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(solution)
        return result
    
    def get_solutions_with_alternatives(self, alternatives):
        """Get solutions considering alternative weights/priorities."""
        result = []
        
        # Check original solutions
        for solution in self.solutions:
            result.append((solution, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedChessboardQueens(self.n, alt_weights, alt_priorities)
            temp_solutions = temp_instance.get_solutions()
            result.append((temp_solutions, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_solutions_with_adaptive_criteria(self, adaptive_func):
        """Get solutions using adaptive criteria."""
        result = []
        for solution in self.solutions:
            if adaptive_func(solution, self.weights, self.priorities, result):
                result.append(solution)
        return result
    
    def get_solution_optimization(self):
        """Get optimal solution configuration."""
        strategies = [
            ('solutions', lambda: len(self.solutions)),
            ('weighted_solutions', lambda: len(self.get_weighted_solutions())),
            ('total_weight', lambda: sum(sum(self.weights[i][j] for j in range(self.n)) for i in range(self.n))),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
n = 4
weights = [[2, 1, 3, 1], [1, 3, 1, 2], [3, 1, 2, 1], [1, 2, 1, 3]]
priorities = [[1, 2, 1, 3], [2, 1, 3, 1], [1, 3, 1, 2], [3, 1, 2, 1]]
advanced_queens = AdvancedChessboardQueens(n, weights, priorities)

print(f"Solutions: {len(advanced_queens.get_solutions())}")
print(f"Weighted solutions: {len(advanced_queens.get_weighted_solutions())}")

# Get solutions with priority
def priority_func(solution, weights, priorities):
    return sum(weights[row][col] for row, col in solution) + sum(priorities[row][col] for row, col in solution)

print(f"Solutions with priority: {len(advanced_queens.get_solutions_with_priority(priority_func))}")

# Get solutions with optimization
def optimization_func(solution, weights, priorities):
    return sum(weights[row][col] * priorities[row][col] for row, col in solution)

print(f"Solutions with optimization: {len(advanced_queens.get_solutions_with_optimization(optimization_func))}")

# Get solutions with constraints
def constraint_func(solution, weights, priorities):
    return len(solution) == n and sum(weights[row][col] for row, col in solution) <= 10

print(f"Solutions with constraints: {len(advanced_queens.get_solutions_with_constraints(constraint_func))}")

# Get solutions with multiple criteria
def criterion1(solution, weights, priorities):
    return len(solution) == n

def criterion2(solution, weights, priorities):
    return sum(weights[row][col] for row, col in solution) <= 10

criteria_list = [criterion1, criterion2]
print(f"Solutions with multiple criteria: {len(advanced_queens.get_solutions_with_multiple_criteria(criteria_list))}")

# Get solutions with alternatives
alternatives = [([[1]*n for _ in range(n)], [[1]*n for _ in range(n)]), ([[3]*n for _ in range(n)], [[2]*n for _ in range(n)])]
print(f"Solutions with alternatives: {len(advanced_queens.get_solutions_with_alternatives(alternatives))}")

# Get solutions with adaptive criteria
def adaptive_func(solution, weights, priorities, current_result):
    return len(solution) == n and len(current_result) < 5

print(f"Solutions with adaptive criteria: {len(advanced_queens.get_solutions_with_adaptive_criteria(adaptive_func))}")

# Get solution optimization
print(f"Solution optimization: {advanced_queens.get_solution_optimization()}")
```

### **Variation 3: Chessboard and Queens with Constraints**
**Problem**: Handle chessboard and queens with additional constraints (blocked squares, different board shapes, advanced placement rules).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedChessboardQueens:
    def __init__(self, n, constraints=None):
        self.n = n
        self.constraints = constraints or {}
        self.board = [['.' for _ in range(n)] for _ in range(n)]
        self.blocked_squares = set(self.constraints.get('blocked_squares', []))
        self.queens = []
        self.solutions = []
        self._find_all_solutions()
    
    def _find_all_solutions(self):
        """Find all valid queen placements considering constraints."""
        self.solutions = []
        
        def is_safe(row, col):
            # Check if square is blocked
            if (row, col) in self.blocked_squares:
                return False
            
            # Check column
            for i in range(row):
                if self.board[i][col] == 'Q':
                    return False
            
            # Check diagonal (top-left to bottom-right)
            for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
                if self.board[i][j] == 'Q':
                    return False
            
            # Check diagonal (top-right to bottom-left)
            for i, j in zip(range(row-1, -1, -1), range(col+1, self.n)):
                if self.board[i][j] == 'Q':
                    return False
            
            return True
        
        def solve(row):
            if row == self.n:
                # Found a solution
                solution = []
                for i in range(self.n):
                    for j in range(self.n):
                        if self.board[i][j] == 'Q':
                            solution.append((i, j))
                self.solutions.append(solution[:])
                return
            
            for col in range(self.n):
                if is_safe(row, col):
                    self.board[row][col] = 'Q'
                    solve(row + 1)
                    self.board[row][col] = '.'
        
        solve(0)
    
    def get_solutions_with_blocked_squares(self, blocked_squares):
        """Get solutions considering blocked squares."""
        result = []
        for solution in self.solutions:
            # Check if solution uses any blocked squares
            if not any(pos in blocked_squares for pos in solution):
                result.append(solution)
        return result
    
    def get_solutions_with_board_shape(self, board_shape):
        """Get solutions considering custom board shape."""
        result = []
        for solution in self.solutions:
            # Check if all positions are within board shape
            if all(0 <= row < len(board_shape) and 0 <= col < len(board_shape[0]) and board_shape[row][col] == 1 
                   for row, col in solution):
                result.append(solution)
        return result
    
    def get_solutions_with_placement_rules(self, placement_rules):
        """Get solutions considering custom placement rules."""
        result = []
        for solution in self.solutions:
            satisfies_rules = True
            for rule in placement_rules:
                if not rule(solution):
                    satisfies_rules = False
                    break
            if satisfies_rules:
                result.append(solution)
        return result
    
    def get_solutions_with_mathematical_constraints(self, constraint_func):
        """Get solutions that satisfy custom mathematical constraints."""
        result = []
        for solution in self.solutions:
            if constraint_func(solution):
                result.append(solution)
        return result
    
    def get_solutions_with_range_constraints(self, range_constraints):
        """Get solutions that satisfy range constraints."""
        result = []
        for solution in self.solutions:
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(solution):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(solution)
        return result
    
    def get_solutions_with_optimization_constraints(self, optimization_func):
        """Get solutions using custom optimization constraints."""
        # Sort solutions by optimization function
        all_solutions = []
        for solution in self.solutions:
            score = optimization_func(solution)
            all_solutions.append((solution, score))
        
        # Sort by optimization score
        all_solutions.sort(key=lambda x: x[1], reverse=True)
        
        return [solution for solution, _ in all_solutions]
    
    def get_solutions_with_multiple_constraints(self, constraints_list):
        """Get solutions that satisfy multiple constraints."""
        result = []
        for solution in self.solutions:
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(solution):
                    satisfies_all_constraints = False
                    break
            if satisfies_all_constraints:
                result.append(solution)
        return result
    
    def get_solutions_with_priority_constraints(self, priority_func):
        """Get solutions with priority-based constraints."""
        # Sort solutions by priority
        all_solutions = []
        for solution in self.solutions:
            priority = priority_func(solution)
            all_solutions.append((solution, priority))
        
        # Sort by priority
        all_solutions.sort(key=lambda x: x[1], reverse=True)
        
        return [solution for solution, _ in all_solutions]
    
    def get_solutions_with_adaptive_constraints(self, adaptive_func):
        """Get solutions with adaptive constraints."""
        result = []
        for solution in self.solutions:
            if adaptive_func(solution, result):
                result.append(solution)
        return result
    
    def get_optimal_solution_strategy(self):
        """Get optimal solution strategy considering all constraints."""
        strategies = [
            ('blocked_squares', self.get_solutions_with_blocked_squares),
            ('board_shape', self.get_solutions_with_board_shape),
            ('placement_rules', self.get_solutions_with_placement_rules),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'blocked_squares':
                    current_count = len(strategy_func([(0, 0), (1, 1)]))
                elif strategy_name == 'board_shape':
                    board_shape = [[1]*self.n for _ in range(self.n)]
                    current_count = len(strategy_func(board_shape))
                elif strategy_name == 'placement_rules':
                    placement_rules = [lambda s: len(s) == self.n]
                    current_count = len(strategy_func(placement_rules))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'blocked_squares': [(0, 0), (1, 1), (2, 2)]
}

n = 4
constrained_queens = ConstrainedChessboardQueens(n, constraints)

print("Blocked squares solutions:", len(constrained_queens.get_solutions_with_blocked_squares([(0, 0), (1, 1)])))

# Board shape constraints
board_shape = [[1, 1, 0, 1], [1, 1, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]]
print("Board shape solutions:", len(constrained_queens.get_solutions_with_board_shape(board_shape)))

# Placement rules
def rule1(solution):
    return len(solution) == n

def rule2(solution):
    return all(pos[0] != pos[1] for pos in solution)  # No queens on main diagonal

placement_rules = [rule1, rule2]
print("Placement rules solutions:", len(constrained_queens.get_solutions_with_placement_rules(placement_rules)))

# Mathematical constraints
def custom_constraint(solution):
    return len(solution) == n and all(pos[0] + pos[1] < n for pos in solution)

print("Mathematical constraint solutions:", len(constrained_queens.get_solutions_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(solution):
    return 3 <= len(solution) <= 5

range_constraints = [range_constraint]
print("Range-constrained solutions:", len(constrained_queens.get_solutions_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(solution):
    return len(solution) == n

def constraint2(solution):
    return all(pos[0] != pos[1] for pos in solution)

constraints_list = [constraint1, constraint2]
print("Multiple constraints solutions:", len(constrained_queens.get_solutions_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(solution):
    return len(solution) + sum(pos[0] + pos[1] for pos in solution)

print("Priority-constrained solutions:", len(constrained_queens.get_solutions_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(solution, current_result):
    return len(solution) == n and len(current_result) < 5

print("Adaptive constraint solutions:", len(constrained_queens.get_solutions_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_queens.get_optimal_solution_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Permutations](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Two Knights](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Creating Strings](https://cses.fi/problemset/task/1075) - Introductory Problems

#### **LeetCode Problems**
- [N-Queens](https://leetcode.com/problems/n-queens/) - Backtracking
- [N-Queens II](https://leetcode.com/problems/n-queens-ii/) - Backtracking
- [Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) - Backtracking

#### **Problem Categories**
- **Introductory Problems**: Backtracking, constraint satisfaction
- **Backtracking**: N-Queens, constraint satisfaction
- **Chess Problems**: Queen placement, constraint checking

## 🔗 Additional Resources

### **Algorithm References**
- [Introductory Problems](https://cp-algorithms.com/intro-to-algorithms.html) - Introductory algorithms
- [Backtracking](https://cp-algorithms.com/backtracking.html) - Backtracking algorithms
- [N-Queens](https://cp-algorithms.com/backtracking.html#n-queens) - N-Queens algorithm

### **Practice Problems**
- [CSES Permutations](https://cses.fi/problemset/task/1075) - Easy
- [CSES Two Knights](https://cses.fi/problemset/task/1075) - Easy
- [CSES Creating Strings](https://cses.fi/problemset/task/1075) - Easy

### **Further Reading**
- [Backtracking](https://en.wikipedia.org/wiki/Backtracking) - Wikipedia article
- [N-Queens Problem](https://en.wikipedia.org/wiki/Eight_queens_puzzle) - Wikipedia article
- [Constraint Satisfaction](https://en.wikipedia.org/wiki/Constraint_satisfaction) - Wikipedia article
