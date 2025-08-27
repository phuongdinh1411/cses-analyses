# CSES Knight's Tour - Problem Analysis

## Problem Statement
Given a chessboard of size n×n, find a knight's tour (a path where the knight visits every square exactly once).

### Input
The first input line has one integer n: the size of the chessboard.

### Output
Print the knight's tour as an n×n grid where each number represents the order in which the knight visits that square.

### Constraints
- 1 ≤ n ≤ 8

### Example
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

## Solution Progression

### Approach 1: Backtracking with Warnsdorff's Rule - O(n²)
**Description**: Use backtracking with Warnsdorff's rule to find knight's tour.

```python
def knights_tour_naive(n):
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
    
    def warnsdorff_rule(x, y):
        # Sort moves by number of valid moves from next position
        valid_moves = get_valid_moves(x, y)
        valid_moves.sort(key=lambda pos: len(get_valid_moves(pos[0], pos[1])))
        return valid_moves
    
    def backtrack(x, y, move_count):
        if move_count == n * n:
            return True
        
        # Get moves sorted by Warnsdorff's rule
        next_moves = warnsdorff_rule(x, y)
        
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

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Backtracking with Warnsdorff's Rule - O(n²)
**Description**: Use optimized backtracking with better Warnsdorff's rule implementation.

```python
def knights_tour_optimized(n):
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
                valid_moves.append((nx, ny, count_valid_moves(nx, ny)))
        
        # Sort by number of valid moves (Warnsdorff's rule)
        valid_moves.sort(key=lambda pos: pos[2])
        return [(x, y) for x, y, _ in valid_moves]
    
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
    
    # Start from (0, 0)
    board[0][0] = 1
    if backtrack(0, 0, 1):
        return board
    else:
        return None
```

**Why this improvement works**: We use optimized backtracking with Warnsdorff's rule to find knight's tour efficiently.

## Final Optimal Solution

```python
n = int(input())

def find_knights_tour(n):
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
                valid_moves.append((nx, ny, count_valid_moves(nx, ny)))
        
        # Sort by number of valid moves (Warnsdorff's rule)
        valid_moves.sort(key=lambda pos: pos[2])
        return [(x, y) for x, y, _ in valid_moves]
    
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
    
    # Start from (0, 0)
    board[0][0] = 1
    if backtrack(0, 0, 1):
        return board
    else:
        return None

result = find_knights_tour(n)
if result:
    for row in result:
        print(*row)
else:
    print("No solution exists")
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Backtracking with Warnsdorff's | O(n²) | O(n²) | Use Warnsdorff's rule for optimization |
| Optimized Backtracking | O(n²) | O(n²) | Optimized backtracking implementation |

## Key Insights for Other Problems

### 1. **Knight's Tour**
**Principle**: Use backtracking with Warnsdorff's rule to find knight's tour.
**Applicable to**: Tour problems, path problems, backtracking problems

### 2. **Warnsdorff's Rule**
**Principle**: Choose moves that lead to positions with fewer valid moves.
**Applicable to**: Tour problems, path problems, optimization problems

### 3. **Backtracking with Heuristics**
**Principle**: Use heuristics to guide backtracking search.
**Applicable to**: Search problems, optimization problems, constraint problems

## Notable Techniques

### 1. **Knight's Tour Backtracking**
```python
def knights_tour_backtracking(n):
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    board = [[0] * n for _ in range(n)]
    
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == 0
    
    def backtrack(x, y, move_count):
        if move_count == n * n:
            return True
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                board[nx][ny] = move_count + 1
                if backtrack(nx, ny, move_count + 1):
                    return True
                board[nx][ny] = 0
        
        return False
    
    board[0][0] = 1
    return backtrack(0, 0, 1)
```

### 2. **Warnsdorff's Rule Implementation**
```python
def warnsdorff_rule(n, board, x, y, moves):
    def count_moves(nx, ny):
        count = 0
        for dx, dy in moves:
            nnx, nny = nx + dx, ny + dy
            if 0 <= nnx < n and 0 <= nny < n and board[nnx][nny] == 0:
                count += 1
        return count
    
    valid_moves = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0:
            valid_moves.append((nx, ny, count_moves(nx, ny)))
    
    valid_moves.sort(key=lambda pos: pos[2])
    return [(x, y) for x, y, _ in valid_moves]
```

### 3. **Move Validation**
```python
def validate_moves(n, board, x, y, moves):
    valid_moves = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0:
            valid_moves.append((nx, ny))
    return valid_moves
```

## Problem-Solving Framework

1. **Identify problem type**: This is a knight's tour problem
2. **Choose approach**: Use backtracking with Warnsdorff's rule
3. **Define moves**: Specify all possible knight moves
4. **Initialize board**: Create empty chessboard
5. **Implement backtracking**: Use recursive backtracking with move validation
6. **Apply Warnsdorff's rule**: Sort moves by accessibility
7. **Return result**: Output tour or indicate no solution

---

*This analysis shows how to efficiently find knight's tour using backtracking with Warnsdorff's rule.* 