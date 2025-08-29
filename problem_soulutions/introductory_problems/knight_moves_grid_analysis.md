---
layout: simple
title: "Knight Moves Grid Analysis"
permalink: /cses-analyses/problem_soulutions/introductory_problems/knight_moves_grid_analysis
---


# Knight Moves Grid Analysis

## Problem Description

Given an n×n grid, find the minimum number of moves for a knight to reach from the top-left corner to the bottom-right corner. A knight moves in an L-shape: 2 squares in one direction and 1 square perpendicular to that direction.

## Key Insights

### 1. BFS Approach
- Use Breadth-First Search to find shortest path
- Knight has 8 possible moves from any position
- Track visited positions to avoid cycles
- Use queue to process positions level by level

### 2. Knight Movement Pattern
- From position (x, y), knight can move to:
  - (x+2, y+1), (x+2, y-1)
  - (x-2, y+1), (x-2, y-1)
  - (x+1, y+2), (x+1, y-2)
  - (x-1, y+2), (x-1, y-2)

### 3. Boundary Conditions
- Check if new position is within grid bounds
- Ensure 0 ≤ x, y < n for n×n grid
- Handle edge cases for small grids

## Solution Approach

### Method 1: BFS with Queue
```python
from collections import deque

def knight_moves(n):
    if n == 1:
        return 0
    if n == 2:
        return -1  # Impossible
    
    visited = [[False] * n for _ in range(n)]
    queue = deque([(0, 0, 0)])  # (x, y, moves)
    visited[0][0] = True
    
    # Knight's 8 possible moves
    dx = [-2, -2, -1, -1, 1, 1, 2, 2]
    dy = [-1, 1, -2, 2, -2, 2, -1, 1]
    
    while queue:
        x, y, current_moves = queue.popleft()
        
        if x == n-1 and y == n-1:
            return current_moves
        
        for i in range(8):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if (0 <= nx < n and 0 <= ny < n and 
                not visited[nx][ny]):
                visited[nx][ny] = True
                queue.append((nx, ny, current_moves + 1))
    
    return -1  # Impossible
```

### Method 2: Mathematical Approach
```python
def knight_moves_mathematical(n):
    if n == 1:
        return 0
    if n == 2:
        return -1
    if n == 3:
        return 2
    if n == 4:
        return 2
    if n == 5:
        return 4
    if n == 6:
        return 4
    
    # For larger grids, use mathematical formula
    return (n + 1) // 2
```

## Time Complexity
- **Time**: O(n²) - worst case we visit all cells
- **Space**: O(n²) - visited array

## Example Walkthrough

**Input**: n = 5

**Process**:
1. Start at (0, 0)
2. Move to (2, 1) in 1 move
3. Move to (4, 2) in 2 moves
4. Move to (3, 4) in 3 moves
5. Move to (1, 3) in 4 moves
6. Move to (0, 1) in 5 moves
7. Move to (2, 2) in 6 moves
8. Move to (4, 3) in 7 moves
9. Move to (3, 1) in 8 moves
10. Move to (1, 0) in 9 moves
11. Move to (3, 1) in 10 moves
12. Move to (4, 3) in 11 moves
13. Move to (2, 4) in 12 moves
14. Move to (0, 3) in 13 moves
15. Move to (2, 2) in 14 moves
16. Move to (4, 1) in 15 moves
17. Move to (3, 3) in 16 moves
18. Move to (1, 4) in 17 moves
19. Move to (3, 2) in 18 moves
20. Move to (4, 4) in 19 moves

**Output**: 4 (optimal path)

## Problem Variations

### Variation 1: Weighted Grid
**Problem**: Each cell has a cost. Find minimum cost path.

**Approach**: Use Dijkstra's algorithm instead of BFS.

### Variation 2: Multiple Knights
**Problem**: Find minimum moves for k knights to reach destination.

**Approach**: Use multi-source BFS or state representation.

### Variation 3: Obstacles
**Problem**: Some cells are blocked. Find valid path.

**Solution**: Skip blocked cells in BFS exploration.

### Variation 4: Different Piece Types
**Problem**: Use different chess pieces (rook, bishop, queen).

**Approach**: Modify movement patterns for each piece.

### Variation 5: Circular Grid
**Problem**: Grid wraps around edges (toroidal).

**Solution**: Use modulo arithmetic for boundary checking.

### Variation 6: 3D Grid
**Problem**: Knight moves in 3D space.

**Approach**: Extend to 3D coordinates and movement patterns.

## Advanced Optimizations

### 1. Bidirectional BFS
```python
from collections import deque

def bidirectional_bfs(n):
    if n == 1:
        return 0
    if n == 2:
        return -1
    
    start_visited = set()
    end_visited = set()
    start_queue = deque([(0, 0, 0)])  # (x, y, moves)
    end_queue = deque([(n-1, n-1, 0)])
    
    start_visited.add((0, 0))
    end_visited.add((n-1, n-1))
    
    # Continue with bidirectional search...
    # This can significantly reduce search space
```

### 2. A* Search
```python
import heapq

def a_star_search(n):
    pq = [(0, 0, 0)]  # (f_score, x, y)
    g_score = [[float('inf')] * n for _ in range(n)]
    
    g_score[0][0] = 0
    
    # Continue with A* search...
    # Uses heuristic to guide search more efficiently
```

## Related Problems
- [Grid Paths](/cses-analyses/problem_soulutions/grid_path_description_analysis)
- [Two Knights](/cses-analyses/problem_soulutions/two_knights_analysis)
- [Labyrinth](/cses-analyses/problem_soulutions/graph_algorithms/labyrinth_analysis)

## Practice Problems
1. **CSES**: Knight Moves Grid
2. **LeetCode**: Similar BFS problems
3. **AtCoder**: Grid-based shortest path problems

## Key Takeaways
1. **BFS** is optimal for unweighted shortest path
2. **Boundary checking** is crucial for grid problems
3. **Movement patterns** must be carefully implemented
4. **Mathematical insights** can optimize for specific cases
5. **Bidirectional search** can improve performance
6. **State representation** is important for variations
7. **Edge cases** like small grids need special handling
