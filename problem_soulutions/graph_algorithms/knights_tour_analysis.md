---
layout: simple
title: CSES Knight's Tour
permalink: /problem_soulutions/graph_algorithms/knights_tour_analysis
---


# CSES Knight's Tour

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Knight's Tour with Constraints**
**Problem**: Find knight's tour with additional constraints (obstacles, forbidden squares, etc.).
```python
def constrained_knights_tour(n, obstacles):
    # obstacles = set of (x, y) coordinates that are forbidden
    
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    board = [[0] * n for _ in range(n)]
    
    def is_valid(x, y):
        return (0 <= x < n and 0 <= y < n and 
                board[x][y] == 0 and (x, y) not in obstacles)
    
    def backtrack(x, y, move_count):
        if move_count == n * n - len(obstacles):
            return True
        
        # Apply Warnsdorff's rule
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                # Count future moves from this position
                future_moves = 0
                for dx2, dy2 in moves:
                    nnx, nny = nx + dx2, ny + dy2
                    if is_valid(nnx, nny):
                        future_moves += 1
                valid_moves.append((nx, ny, future_moves))
        
        # Sort by accessibility (Warnsdorff's rule)
        valid_moves.sort(key=lambda pos: pos[2])
        
        for nx, ny, _ in valid_moves:
            board[nx][ny] = move_count + 1
            if backtrack(nx, ny, move_count + 1):
                return True
            board[nx][ny] = 0
        
        return False
    
    # Find starting position (not in obstacles)
    start_x, start_y = 0, 0
    while (start_x, start_y) in obstacles:
        start_y += 1
        if start_y == n:
            start_y = 0
            start_x += 1
            if start_x == n:
                return None  # No valid starting position
    
    board[start_x][start_y] = 1
    return backtrack(start_x, start_y, 1)
```

#### **Variation 2: Knight's Tour with Costs**
**Problem**: Each square has a cost, find knight's tour with minimum total cost.
```python
def cost_based_knights_tour(n, costs):
    # costs[x][y] = cost of visiting square (x, y)
    
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    board = [[0] * n for _ in range(n)]
    min_cost = float('inf')
    best_tour = None
    
    def backtrack(x, y, move_count, current_cost):
        nonlocal min_cost, best_tour
        
        if move_count == n * n:
            if current_cost < min_cost:
                min_cost = current_cost
                best_tour = [row[:] for row in board]
            return
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if (0 <= nx < n and 0 <= ny < n and 
                board[nx][ny] == 0):
                board[nx][ny] = move_count + 1
                new_cost = current_cost + costs[nx][ny]
                if new_cost < min_cost:  # Pruning
                    backtrack(nx, ny, move_count + 1, new_cost)
                board[nx][ny] = 0
    
    board[0][0] = 1
    backtrack(0, 0, 1, costs[0][0])
    return best_tour, min_cost
```

#### **Variation 3: Knight's Tour with Probabilities**
**Problem**: Each square has a probability of being accessible, find expected knight's tour.
```python
def probabilistic_knights_tour(n, probabilities):
    # probabilities[x][y] = probability that square (x, y) is accessible
    
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    # For probabilistic squares, calculate expected tour length
    expected_length = 0
    
    # Calculate expected accessible squares
    for x in range(n):
        for y in range(n):
            expected_length += probabilities[x][y]
    
    # Find expected tour (simplified approach)
    board = [[0] * n for _ in range(n)]
    
    def expected_tour_length(x, y, visited):
        if len(visited) >= expected_length:
            return len(visited)
        
        max_length = len(visited)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if (0 <= nx < n and 0 <= ny < n and 
                (nx, ny) not in visited):
                # Consider probability of accessibility
                if probabilities[nx][ny] > 0.5:  # Threshold
                    visited.add((nx, ny))
                    length = expected_tour_length(nx, ny, visited)
                    visited.remove((nx, ny))
                    max_length = max(max_length, length)
        
        return max_length
    
    return expected_tour_length(0, 0, {(0, 0)})
```

#### **Variation 4: Knight's Tour with Multiple Knights**
**Problem**: Find tours for multiple knights that don't interfere with each other.
```python
def multiple_knights_tour(n, k):
    # k = number of knights
    
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    boards = [[[0] * n for _ in range(n)] for _ in range(k)]
    
    def is_valid_move(knight, x, y, step):
        if not (0 <= x < n and 0 <= y < n):
            return False
        
        # Check if any knight has visited this square
        for k_idx in range(k):
            if boards[k_idx][x][y] != 0:
                return False
        
        return True
    
    def backtrack(knight, x, y, step):
        if step == (n * n) // k:  # Each knight covers n²/k squares
            if knight == k - 1:  # All knights have completed their tours
                return True
            else:
                # Start next knight
                return backtrack(knight + 1, 0, 0, 1)
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid_move(knight, nx, ny, step + 1):
                boards[knight][nx][ny] = step + 1
                if backtrack(knight, nx, ny, step + 1):
                    return True
                boards[knight][nx][ny] = 0
        
        return False
    
    # Start first knight
    boards[0][0][0] = 1
    return backtrack(0, 0, 1)
```

#### **Variation 5: Knight's Tour with Time Constraints**
**Problem**: Each move takes time, find knight's tour that completes within time limit.
```python
def timed_knights_tour(n, time_limit, move_times):
    # move_times[(dx, dy)] = time required for move (dx, dy)
    
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    board = [[0] * n for _ in range(n)]
    best_tour = None
    max_squares = 0
    
    def backtrack(x, y, move_count, current_time):
        nonlocal best_tour, max_squares
        
        if current_time > time_limit:
            return
        
        if move_count > max_squares:
            max_squares = move_count
            best_tour = [row[:] for row in board]
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            move_time = move_times.get((dx, dy), 1)
            
            if (0 <= nx < n and 0 <= ny < n and 
                board[nx][ny] == 0 and 
                current_time + move_time <= time_limit):
                board[nx][ny] = move_count + 1
                backtrack(nx, ny, move_count + 1, current_time + move_time)
                board[nx][ny] = 0
    
    board[0][0] = 1
    backtrack(0, 0, 1, 0)
    return best_tour, max_squares
```

### 🔗 **Related Problems & Concepts**

#### **1. Tour Problems**
- **Hamiltonian Path**: Find path visiting each vertex once
- **Hamiltonian Cycle**: Find cycle visiting each vertex once
- **Eulerian Path**: Find path using each edge once
- **Eulerian Cycle**: Find cycle using each edge once

#### **2. Pathfinding Problems**
- **Shortest Path**: Find shortest path between points
- **Longest Path**: Find longest path in graph
- **Path with Constraints**: Find path satisfying constraints
- **Multiple Paths**: Find multiple non-interfering paths

#### **3. Backtracking Problems**
- **N-Queens**: Place queens on chessboard
- **Sudoku**: Fill grid with numbers
- **Graph Coloring**: Color graph vertices
- **Subset Sum**: Find subset with given sum

#### **4. Optimization Problems**
- **Traveling Salesman**: Find shortest tour visiting all cities
- **Vehicle Routing**: Route vehicles optimally
- **Scheduling**: Schedule tasks optimally
- **Resource Allocation**: Allocate resources optimally

#### **5. Algorithmic Techniques**
- **Backtracking**: Systematic search with pruning
- **Heuristics**: Rules to guide search
- **Pruning**: Eliminate unpromising branches
- **Memoization**: Cache computed results

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Board Sizes**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    result = knights_tour_warnsdorff(n)
    if result:
        print("YES")
        for row in result:
            print(*row)
    else:
        print("NO")
```

#### **2. Range Queries on Knight's Tour**
```python
def range_knights_tour_queries(n, queries):
    # queries = [(start_x, start_y), ...] - find tour starting from each position
    
    results = []
    for start_x, start_y in queries:
        result = knights_tour_from_start(n, start_x, start_y)
        results.append(result)
    
    return results
```

#### **3. Interactive Knight's Tour Problems**
```python
def interactive_knights_tour():
    n = int(input("Enter board size: "))
    print(f"Finding knight's tour on {n}x{n} board...")
    
    result = knights_tour_warnsdorff(n)
    if result:
        print("Tour found!")
        for i, row in enumerate(result):
            print(f"Row {i}: {row}")
    else:
        print("No tour exists!")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Hamiltonian Graphs**: Graphs with Hamiltonian cycles
- **Tour Theory**: Mathematical theory of tours
- **Path Theory**: Theory of paths in graphs
- **Cycle Theory**: Theory of cycles in graphs

#### **2. Combinatorics**
- **Tour Enumeration**: Count different tours
- **Path Counting**: Count paths with properties
- **Permutation Theory**: Study of permutations
- **Combinatorial Optimization**: Optimize combinatorial structures

#### **3. Algorithmic Analysis**
- **Search Space Analysis**: Analyze size of search space
- **Pruning Effectiveness**: Measure effectiveness of pruning
- **Heuristic Analysis**: Analyze heuristic performance
- **Complexity Theory**: Study computational complexity

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Backtracking**: Systematic search algorithms
- **Graph Algorithms**: BFS, DFS, pathfinding algorithms
- **Search Algorithms**: A*, IDA*, beam search
- **Optimization Algorithms**: Genetic algorithms, simulated annealing

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Combinatorics**: Counting and enumeration techniques
- **Optimization Theory**: Mathematical optimization principles
- **Complexity Theory**: Computational complexity analysis

#### **3. Programming Concepts**
- **Recursion**: Recursive problem solving
- **State Management**: Managing search state
- **Pruning Techniques**: Eliminating search branches
- **Algorithm Optimization**: Improving algorithm performance

---

*This analysis demonstrates efficient backtracking techniques and shows various extensions for knight's tour problems.* 