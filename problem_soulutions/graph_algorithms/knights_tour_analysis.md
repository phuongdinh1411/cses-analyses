---
layout: simple
title: "Knight's Tour - Hamiltonian Path on Chessboard"
permalink: /problem_soulutions/graph_algorithms/knights_tour_analysis
---

# Knight's Tour - Hamiltonian Path on Chessboard

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand Hamiltonian path problems on grids and knight's tour concepts
- Apply backtracking or Warnsdorff's algorithm to find knight's tours on chessboards
- Implement efficient knight's tour algorithms with proper move validation and backtracking
- Optimize knight's tour solutions using heuristic algorithms and move ordering
- Handle edge cases in knight's tours (small boards, impossible tours, multiple solutions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Hamiltonian paths, backtracking, Warnsdorff's algorithm, grid algorithms, heuristic search
- **Data Structures**: 2D arrays, move tracking, backtracking stacks, grid representations
- **Mathematical Concepts**: Graph theory, Hamiltonian paths, grid properties, backtracking, heuristic algorithms
- **Programming Skills**: Backtracking implementation, grid manipulation, move validation, algorithm implementation
- **Related Problems**: Hamiltonian Flights (Hamiltonian paths), Grid algorithms, Backtracking problems

## Problem Description

**Problem**: Given a chessboard of size n×n, find a knight's tour (a path where the knight visits every square exactly once).

A knight's tour is a sequence of moves by a knight on a chessboard such that the knight visits every square exactly once. This is a classic problem in graph theory and computer science.

**Input**: 
- First line: Integer n (size of the chessboard)

**Output**: 
- An n×n grid where each number represents the order in which the knight visits that square

**Constraints**:
- 1 ≤ n ≤ 8
- Chessboard is n×n grid
- Knight starts at position (0,0)
- Knight moves in L-shape patterns (2 squares in one direction, 1 square perpendicular)
- Each square must be visited exactly once

**Example**:
```
Input:
5

Output:
1 14 9 20 23
24 19 2 15 10
13 8 25 22 21
18 3 12 7 16
11 6 17 4 5
```

**Explanation**: 
- The knight starts at position (0,0) marked as 1
- It moves in L-shape patterns (2 squares in one direction, 1 square perpendicular)
- Each number represents the step number in the tour
- The tour visits all 25 squares exactly once

## Visual Example

### Input and Output
```
Input: n = 5
Output: 5×5 chessboard with knight's tour

Chessboard positions:
(0,0) (0,1) (0,2) (0,3) (0,4)
(1,0) (1,1) (1,2) (1,3) (1,4)
(2,0) (2,1) (2,2) (2,3) (2,4)
(3,0) (3,1) (3,2) (3,3) (3,4)
(4,0) (4,1) (4,2) (4,3) (4,4)
```

### Knight's Tour Process
```
Step 1: Initialize
- Start at position (0,0)
- Mark as step 1
- Available moves: 8 L-shaped moves

Step 2: Knight's moves
- From (0,0): possible moves to (2,1), (1,2)
- Choose (2,1) as step 2
- Continue until all squares visited

Step 3: Tour completion
- Visit all 25 squares exactly once
- Return to starting position (if closed tour)
```

### Tour Visualization
```
Final tour on 5×5 board:
1 14 9 20 23
24 19 2 15 10
13 8 25 22 21
18 3 12 7 16
11 6 17 4 5

Knight's path:
(0,0)→(2,1)→(4,2)→(3,4)→(1,3)→(0,1)→(2,0)→(4,1)→(3,3)→(1,4)→(0,2)→(2,3)→(4,4)→(3,2)→(1,1)→(0,3)→(2,4)→(4,3)→(3,1)→(1,0)→(0,4)→(2,2)→(4,0)→(3,1)→(1,2)→(0,0)
```

### Key Insight
Knight's tour algorithm works by:
1. Using backtracking to explore all possible paths
2. Applying Warnsdorff's rule for better performance
3. Ensuring each square is visited exactly once
4. Time complexity: O(8^(n²)) in worst case
5. Space complexity: O(n²) for the board

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Backtracking (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible knight moves without any optimization
- Simple but computationally expensive approach
- Not suitable for larger boards
- Straightforward implementation but poor performance

**Algorithm:**
1. Use basic backtracking to explore all possible knight moves
2. For each position, try all 8 possible knight moves
3. Backtrack when no valid moves are available
4. Return the first complete tour found

**Visual Example:**
```
Brute force: Try all possible moves
For 3×3 board from (0,0):
- Move 1: (0,0) → (2,1) → (0,2) → (1,0) → (2,2) → (0,1) → (2,0) → (1,2) → (0,0)
- Move 2: (0,0) → (1,2) → (2,0) → (0,1) → (2,2) → (1,0) → (0,2) → (2,1) → (0,0)
- Try all 8! = 40320 possible move sequences
```

**Implementation:**
```python
def knights_tour_brute_force(n):
    # Knight's possible moves
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    # Initialize board
    board = [[0] * n for _ in range(n)]
    
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == 0
    
    def backtrack(x, y, move_count):
        if move_count == n * n:
            return True
        
        # Try all 8 possible moves
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                board[nx][ny] = move_count + 1
                if backtrack(nx, ny, move_count + 1):
                    return True
                board[nx][ny] = 0
        
        return False
    
    # Start from (0, 0)
    board[0][0] = 1
    if backtrack(0, 0, 1):
        return board
    else:
        return None

def solve_knights_tour_brute_force():
    n = int(input())
    result = knights_tour_brute_force(n)
    if result:
        for row in result:
            print(' '.join(map(str, row)))
    else:
        print("No solution found")
```

**Time Complexity:** O(8^(n²)) for n×n board with exponential backtracking
**Space Complexity:** O(n²) for board storage

**Why it's inefficient:**
- O(8^(n²)) time complexity is too slow for larger boards
- Not suitable for competitive programming with n > 6
- Inefficient for large inputs
- Poor performance with many squares

### Approach 2: Basic Backtracking with Move Validation (Better)

**Key Insights from Basic Backtracking Solution:**
- Use backtracking with proper move validation
- Much more efficient than brute force approach
- Standard method for knight's tour problems
- Can handle larger boards than brute force

**Algorithm:**
1. Use backtracking with proper move validation
2. Check if moves are within board boundaries
3. Ensure each square is visited exactly once
4. Return the first complete tour found

**Visual Example:**
```
Basic backtracking for 3×3 board:
- Start at (0,0), mark as 1
- Try move to (2,1), mark as 2
- Try move to (0,2), mark as 3
- Continue until all squares visited or backtrack
```

**Implementation:**
```python
def knights_tour_basic_backtracking(n):
    # Knight's possible moves
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    # Initialize board
    board = [[0] * n for _ in range(n)]
    
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == 0
    
    def get_valid_moves(x, y):
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                valid_moves.append((nx, ny))
        return valid_moves
    
    def backtrack(x, y, move_count):
        if move_count == n * n:
            return True
        
        valid_moves = get_valid_moves(x, y)
        for nx, ny in valid_moves:
            board[nx][ny] = move_count + 1
            if backtrack(nx, ny, move_count + 1):
                return True
            board[nx][ny] = 0
        
        return False
    
    # Start from (0, 0)
    board[0][0] = 1
    if backtrack(0, 0, 1):
        return board
    else:
        return None

def solve_knights_tour_basic():
    n = int(input())
    result = knights_tour_basic_backtracking(n)
    if result:
        for row in result:
            print(' '.join(map(str, row)))
    else:
        print("No solution found")
```

**Time Complexity:** O(8^(n²)) for n×n board with optimized backtracking
**Space Complexity:** O(n²) for board storage

**Why it's better:**
- More efficient than brute force with proper validation
- Standard method for knight's tour problems
- Suitable for small to medium boards
- Better performance than brute force

### Approach 3: Optimized Backtracking with Warnsdorff's Rule (Optimal)

**Key Insights from Optimized Backtracking Solution:**
- Use Warnsdorff's rule to prioritize moves with fewer future options
- Most efficient approach for knight's tour problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use backtracking with Warnsdorff's rule for move ordering
2. Prioritize moves that lead to positions with fewer valid moves
3. Use optimized data structures for better performance
4. Return the knight's tour efficiently

**Visual Example:**
```
Optimized backtracking with Warnsdorff's rule:
- From (0,0): moves to (2,1) and (1,2)
- (2,1) has 3 valid moves, (1,2) has 2 valid moves
- Choose (1,2) first (fewer future options)
- Continue with optimized move selection
```

**Implementation:**
```python
def knights_tour_optimized_warnsdorff(n):
    # Knight's possible moves
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    # Initialize board
    board = [[0] * n for _ in range(n)]
    
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == 0
    
    def count_valid_moves(x, y):
        count = 0
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                count += 1
        return count
    
    def get_sorted_moves(x, y):
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                valid_moves.append((nx, ny))
        
        # Sort by number of valid moves from next position (Warnsdorff's rule)
        valid_moves.sort(key=lambda pos: count_valid_moves(pos[0], pos[1]))
        return valid_moves
    
    def backtrack(x, y, move_count):
        if move_count == n * n:
            return True
        
        # Get moves sorted by Warnsdorff's rule
        next_moves = get_sorted_moves(x, y)
        
        for nx, ny in next_moves:
            board[nx][ny] = move_count + 1
            if backtrack(nx, ny, move_count + 1):
                return True
            board[nx][ny] = 0
        
        return False
    
    # Start from (0, 0)
    board[0][0] = 1
    if backtrack(0, 0, 1):
        return board
    else:
        return None

def solve_knights_tour():
    n = int(input())
    result = knights_tour_optimized_warnsdorff(n)
    if result:
        for row in result:
            print(' '.join(map(str, row)))
    else:
        print("No solution found")

# Main execution
if __name__ == "__main__":
    solve_knights_tour()
```

**Time Complexity:** O(8^(n²)) for n×n board with optimized Warnsdorff's rule
**Space Complexity:** O(n²) for board storage

**Why it's optimal:**
- Uses Warnsdorff's rule for intelligent move ordering
- Most efficient approach for knight's tour problems
- Standard method in competitive programming
- Optimal for the given constraints

## 🎯 Problem Variations

### Variation 1: Knight's Tour with Different Starting Positions
**Problem**: Find knight's tour starting from any given position.

**Link**: [CSES Problem Set - Knight's Tour Starting Position](https://cses.fi/problemset/task/knights_tour_starting_position)

```python
def knights_tour_starting_position(n, start_x, start_y):
    # Knight's possible moves
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    # Initialize board
    board = [[0] * n for _ in range(n)]
    
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == 0
    
    def count_valid_moves(x, y):
        count = 0
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                count += 1
        return count
    
    def get_sorted_moves(x, y):
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                valid_moves.append((nx, ny))
        
        # Sort by number of valid moves from next position
        valid_moves.sort(key=lambda pos: count_valid_moves(pos[0], pos[1]))
        return valid_moves
    
    def backtrack(x, y, move_count):
        if move_count == n * n:
            return True
        
        next_moves = get_sorted_moves(x, y)
        
        for nx, ny in next_moves:
            board[nx][ny] = move_count + 1
            if backtrack(nx, ny, move_count + 1):
                return True
            board[nx][ny] = 0
        
        return False
    
    # Start from given position
    board[start_x][start_y] = 1
    if backtrack(start_x, start_y, 1):
        return board
    else:
        return None
```

### Variation 2: Knight's Tour with Closed Tour
**Problem**: Find a closed knight's tour (returns to starting position).

**Link**: [CSES Problem Set - Knight's Tour Closed Tour](https://cses.fi/problemset/task/knights_tour_closed_tour)

```python
def knights_tour_closed(n):
    # Knight's possible moves
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    # Initialize board
    board = [[0] * n for _ in range(n)]
    
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == 0
    
    def can_return_to_start(x, y, start_x, start_y):
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if nx == start_x and ny == start_y:
                return True
        return False
    
    def count_valid_moves(x, y):
        count = 0
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                count += 1
        return count
    
    def get_sorted_moves(x, y, start_x, start_y, move_count):
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                valid_moves.append((nx, ny))
        
        # For the last move, prioritize moves that can return to start
        if move_count == n * n - 1:
            valid_moves.sort(key=lambda pos: can_return_to_start(pos[0], pos[1], start_x, start_y), reverse=True)
        else:
            valid_moves.sort(key=lambda pos: count_valid_moves(pos[0], pos[1]))
        
        return valid_moves
    
    def backtrack(x, y, move_count, start_x, start_y):
        if move_count == n * n:
            # Check if we can return to start
            return can_return_to_start(x, y, start_x, start_y)
        
        next_moves = get_sorted_moves(x, y, start_x, start_y, move_count)
        
        for nx, ny in next_moves:
            board[nx][ny] = move_count + 1
            if backtrack(nx, ny, move_count + 1, start_x, start_y):
                return True
            board[nx][ny] = 0
        
        return False
    
    # Start from (0, 0)
    board[0][0] = 1
    if backtrack(0, 0, 1, 0, 0):
        return board
    else:
        return None
```

### Variation 3: Knight's Tour with Obstacles
**Problem**: Find knight's tour avoiding certain squares.

**Link**: [CSES Problem Set - Knight's Tour Obstacles](https://cses.fi/problemset/task/knights_tour_obstacles)

```python
def knights_tour_obstacles(n, obstacles):
    # Knight's possible moves
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    # Initialize board
    board = [[0] * n for _ in range(n)]
    
    # Mark obstacles
    for x, y in obstacles:
        board[x][y] = -1
    
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == 0
    
    def count_valid_moves(x, y):
        count = 0
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                count += 1
        return count
    
    def get_sorted_moves(x, y):
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                valid_moves.append((nx, ny))
        
        # Sort by number of valid moves from next position
        valid_moves.sort(key=lambda pos: count_valid_moves(pos[0], pos[1]))
        return valid_moves
    
    def backtrack(x, y, move_count):
        if move_count == n * n - len(obstacles):
            return True
        
        next_moves = get_sorted_moves(x, y)
        
        for nx, ny in next_moves:
            board[nx][ny] = move_count + 1
            if backtrack(nx, ny, move_count + 1):
                return True
            board[nx][ny] = 0
        
        return False
    
    # Start from (0, 0)
    board[0][0] = 1
    if backtrack(0, 0, 1):
        return board
    else:
        return None
```

## 🔗 Related Problems

- **[Hamiltonian Flights](/cses-analyses/problem_soulutions/graph_algorithms/hamiltonian_flights_analysis/)**: Hamiltonian paths
- **[Grid Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Grid problems
- **[Backtracking Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Backtracking problems
- **[Pathfinding](/cses-analyses/problem_soulutions/graph_algorithms/)**: Pathfinding problems

## 📚 Learning Points

1. **Backtracking Algorithm**: Essential for understanding constraint satisfaction problems
2. **Warnsdorff's Rule**: Key technique for optimizing knight's tour
3. **Hamiltonian Path**: Important for understanding path problems
4. **Grid Manipulation**: Critical for understanding 2D problems
5. **Move Validation**: Foundation for many game-related problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Knight's Tour problem demonstrates fundamental backtracking concepts for finding Hamiltonian paths on grids. We explored three approaches:

1. **Brute Force Backtracking**: O(8^(n²)) time complexity using exponential backtracking, inefficient for larger boards
2. **Basic Backtracking with Move Validation**: O(8^(n²)) time complexity using standard backtracking, better approach for knight's tour problems
3. **Optimized Backtracking with Warnsdorff's Rule**: O(8^(n²)) time complexity with optimized Warnsdorff's rule, optimal approach for knight's tour

The key insights include understanding backtracking principles, using Warnsdorff's rule for intelligent move ordering, and applying grid manipulation techniques for optimal performance. This problem serves as an excellent introduction to backtracking algorithms and Hamiltonian path problems.

