---
layout: simple
title: "Counting Rooms - Connected Components in Grid"
permalink: /problem_soulutions/graph_algorithms/counting_rooms_analysis
---

# Counting Rooms - Connected Components in Grid

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand connected components in grids and flood fill algorithms
- Apply DFS or BFS to find connected components in 2D grids
- Implement efficient connected component algorithms with proper grid traversal
- Optimize connected component solutions using visited arrays and grid representations
- Handle edge cases in grid connected components (empty grids, single cells, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: DFS, BFS, connected components, flood fill, grid traversal
- **Data Structures**: 2D arrays, visited arrays, queues/stacks, grid representations
- **Mathematical Concepts**: Graph theory, connected components, grid properties, traversal algorithms
- **Programming Skills**: Grid manipulation, DFS/BFS implementation, visited tracking, algorithm implementation
- **Related Problems**: Labyrinth (grid traversal), Message Route (graph traversal), Building Roads (connected components)

## Problem Description11    qProblem**: You are given a map of a building, and your task is to count the number of its rooms. The size of the map is n×m squares, and each square is either floor or wall. You can walk left, right, up, and down through the floor squares.

A room is defined as a connected component of floor squares. Two floor squares are connected if you can walk from one to the other using only floor squares, moving in the four cardinal directions.

**Input**: 
- First line: Two integers n and m (height and width of the map)
- Next n lines: m characters each (". " denotes floor, "#" denotes wall)

**Output**: 
- One integer: the number of rooms

**Constraints**:
- 1 ≤ n, m ≤ 1000
- Grid contains only '.' (floor) and '#' (wall) characters
- Movement is allowed in four cardinal directions (up, down, left, right)
- Grid is 0-indexed

**Example**:
```
Input:
5 8
########
#..#...#
####.#.#
#..#...#
########

Output:
3
```

**Explanation**: 
- The building has 3 rooms (connected components of floor squares)
- Room 1: Top-left area with 2 floor squares
- Room 2: Middle area with 6 floor squares  
- Room 3: Bottom area with 2 floor squares
- Each room is separated by walls

## Visual Example

### Input Grid
```
########
#..#...#
####.#.#
#..#...#
########

Legend: # = Wall, . = Floor
```

### Grid Visualization
```
Row 0: ########
Row 1: #..#...#
Row 2: ####.#.#
Row 3: #..#...#
Row 4: ########

Floor positions:
Row 1: (1,1), (1,3), (1,4), (1,5), (1,6)
Row 2: (2,4), (2,6)
Row 3: (3,1), (3,3), (3,4), (3,5), (3,6)
```

### Room Identification
```
Room 1: Top-left area
┌─────────────────────────────────────┐
│ Positions: (1,1), (1,3)            │
│ Connected: Yes (adjacent)           │
│ Size: 2 floor squares               │
└─────────────────────────────────────┘

Room 2: Middle area
┌─────────────────────────────────────┐
│ Positions: (1,4), (1,5), (1,6),    │
│           (2,4), (2,6), (3,4),     │
│           (3,5), (3,6)             │
│ Connected: Yes (all reachable)      │
│ Size: 8 floor squares               │
└─────────────────────────────────────┘

Room 3: Bottom area
┌─────────────────────────────────────┐
│ Positions: (3,1), (3,3)            │
│ Connected: Yes (adjacent)           │
│ Size: 2 floor squares               │
└─────────────────────────────────────┘
```

### DFS Traversal Visualization
```
Start DFS from (1,1):
┌─────────────────────────────────────┐
│ Visit (1,1) → Mark as visited      │
│ Check neighbors: (0,1), (2,1),     │
│                 (1,0), (1,2)       │
│ Valid: (1,3) → Visit (1,3)         │
│ Mark (1,3) as visited              │
│ Check neighbors of (1,3): None     │
│ Room 1 complete: 2 squares          │
└─────────────────────────────────────┘

Start DFS from (1,4):
┌─────────────────────────────────────┐
│ Visit (1,4) → Mark as visited      │
│ Check neighbors: (1,5), (1,6),     │
│                 (2,4), (3,4)       │
│ Visit (1,5), (1,6), (2,4), (3,4)   │
│ Continue DFS from each...           │
│ Room 2 complete: 8 squares          │
└─────────────────────────────────────┘

Start DFS from (3,1):
┌─────────────────────────────────────┐
│ Visit (3,1) → Mark as visited      │
│ Check neighbors: (3,3) → Visit     │
│ Mark (3,3) as visited              │
│ Room 3 complete: 2 squares          │
└─────────────────────────────────────┘
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Connected Components (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of floor cells to form rooms
- Check if each combination forms a valid connected component
- Simple but computationally expensive approach
- Not suitable for large grids

**Algorithm:**
1. Generate all possible combinations of floor cells
2. Check if each combination forms a valid connected component
3. Count the maximum number of valid rooms
4. Return the room count

**Visual Example:**
```
Brute force: Try all possible room combinations
For grid: ########
         #..#...#
         ####.#.#
         #..#...#
         ########

All possible room combinations:
- Room 1: {(1,1), (1,3)} → Valid connected component
- Room 2: {(1,4), (1,5), (1,6), (2,4), (2,6), (3,4), (3,5), (3,6)} → Valid connected component
- Room 3: {(3,1), (3,3)} → Valid connected component

Total rooms: 3
```

**Implementation:**
```python
def counting_rooms_brute_force(n, m, grid):
    from itertools import combinations
    
    # Find all floor cells
    floor_cells = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.':
                floor_cells.append((i, j))
    
    max_rooms = 0
    
    # Try all possible combinations of floor cells
    for k in range(1, len(floor_cells) + 1):
        for cell_set in combinations(floor_cells, k):
            if is_valid_room(cell_set, grid):
                max_rooms = max(max_rooms, count_connected_components(cell_set))
    
    return max_rooms

def is_valid_room(cell_set, grid):
    # Check if all cells in the set are floor cells
    for i, j in cell_set:
        if grid[i][j] != '.':
            return False
    return True

def count_connected_components(cell_set):
    # Count connected components in the cell set
    visited = set()
    components = 0
    
    for cell in cell_set:
        if cell not in visited:
            components += 1
            dfs_component(cell, cell_set, visited)
    
    return components

def dfs_component(start, cell_set, visited):
    stack = [start]
    visited.add(start)
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while stack:
        i, j = stack.pop()
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if (ni, nj) in cell_set and (ni, nj) not in visited:
                visited.add((ni, nj))
                stack.append((ni, nj))
```

**Time Complexity:** O(2^(n×m) × (n + m)) for checking all combinations
**Space Complexity:** O(n × m) for storing cell sets

**Why it's inefficient:**
- Exponential time complexity O(2^(n×m))
- Not suitable for large grids
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: DFS Connected Components (Better)

**Key Insights from DFS Solution:**
- Use DFS to find connected components of floor cells
- Mark visited cells to avoid revisiting
- Much more efficient than brute force approach
- Standard method for connected component problems

**Algorithm:**
1. Initialize visited array and room count
2. For each unvisited floor cell, start DFS
3. Mark all reachable floor cells as visited
4. Increment room count for each DFS call
5. Return total room count

**Visual Example:**
```
DFS algorithm for grid: ########
                        #..#...#
                        ####.#.#
                        #..#...#
                        ########

Step 1: Initialize
- visited = [[False, False, ...], ...]
- room_count = 0

Step 2: Find unvisited floor cells
- (1,1) - unvisited floor → Start DFS
- DFS from (1,1): visit (1,1), (1,3)
- room_count = 1

Step 3: Find next unvisited floor cell
- (1,4) - unvisited floor → Start DFS
- DFS from (1,4): visit (1,4), (1,5), (1,6), (2,4), (2,6), (3,4), (3,5), (3,6)
- room_count = 2

Step 4: Find next unvisited floor cell
- (3,1) - unvisited floor → Start DFS
- DFS from (3,1): visit (3,1), (3,3)
- room_count = 3

Step 5: No more unvisited floor cells
- Total rooms: 3
```

**Implementation:**
```python
def counting_rooms_dfs(n, m, grid):
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    def dfs(i, j):
        if (i < 0 or i >= n or j < 0 or j >= m or 
            visited[i][j] or grid[i][j] == '#'):
            return
        
        visited[i][j] = True
        
        # Visit all four directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in directions:
            dfs(i + di, j + dj)
    
    # Find all rooms
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                room_count += 1
                dfs(i, j)
    
    return room_count
```

**Time Complexity:** O(n × m) for visiting each cell once
**Space Complexity:** O(n × m) for visited array and recursion stack

**Why it's better:**
- Linear time complexity O(n × m)
- Simple and intuitive approach
- Standard method for connected component problems
- Suitable for competitive programming

### Approach 3: Optimized DFS with Iterative Implementation (Optimal)

**Key Insights from Optimized DFS Solution:**
- Use iterative DFS with stack to avoid recursion overhead
- Optimize memory usage and stack space
- Most efficient approach for connected component problems
- Standard method in competitive programming

**Algorithm:**
1. Initialize visited array and room count
2. For each unvisited floor cell, start iterative DFS
3. Use stack to track cells to visit
4. Mark all reachable floor cells as visited
5. Increment room count for each DFS call
6. Return total room count

**Visual Example:**
```
Optimized DFS algorithm for grid: ########
                                   #..#...#
                                   ####.#.#
                                   #..#...#
                                   ########

Step 1: Initialize
- visited = [[False, False, ...], ...]
- room_count = 0

Step 2: Find unvisited floor cells
- (1,1) - unvisited floor → Start iterative DFS
- Stack: [(1,1)]
- Visit (1,1), (1,3)
- room_count = 1

Step 3: Find next unvisited floor cell
- (1,4) - unvisited floor → Start iterative DFS
- Stack: [(1,4), (1,5), (1,6), (2,4), (2,6), (3,4), (3,5), (3,6)]
- Visit all cells in stack
- room_count = 2

Step 4: Find next unvisited floor cell
- (3,1) - unvisited floor → Start iterative DFS
- Stack: [(3,1), (3,3)]
- Visit all cells in stack
- room_count = 3

Step 5: No more unvisited floor cells
- Total rooms: 3
```

**Implementation:**
```python
def counting_rooms_optimized(n, m, grid):
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def dfs_iterative(start_i, start_j):
        stack = [(start_i, start_j)]
        visited[start_i][start_j] = True
        
        while stack:
            i, j = stack.pop()
            
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < n and 0 <= nj < m and 
                    not visited[ni][nj] and grid[ni][nj] == '.'):
                    visited[ni][nj] = True
                    stack.append((ni, nj))
    
    # Find all rooms
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                room_count += 1
                dfs_iterative(i, j)
    
    return room_count

def solve_counting_rooms():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().strip()
        grid.append(row)
    
    result = counting_rooms_optimized(n, m, grid)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_counting_rooms()
```

**Time Complexity:** O(n × m) for visiting each cell once
**Space Complexity:** O(n × m) for visited array and stack

**Why it's optimal:**
- O(n × m) time complexity is optimal for grid traversal
- Uses iterative DFS to avoid recursion overhead
- Most efficient approach for competitive programming
- Standard method for connected component problems

## 🎯 Problem Variations

### Variation 1: Counting Rooms with Different Movement Rules
**Problem**: Count rooms with different movement rules (8-directional, diagonal movement).

**Link**: [CSES Problem Set - Counting Rooms with Diagonal Movement](https://cses.fi/problemset/task/counting_rooms_diagonal)

```python
def counting_rooms_diagonal(n, m, grid):
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    # 8-directional movement (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    def dfs_iterative(start_i, start_j):
        stack = [(start_i, start_j)]
        visited[start_i][start_j] = True
        
        while stack:
            i, j = stack.pop()
            
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < n and 0 <= nj < m and 
                    not visited[ni][nj] and grid[ni][nj] == '.'):
                    visited[ni][nj] = True
                    stack.append((ni, nj))
    
    # Find all rooms
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                room_count += 1
                dfs_iterative(i, j)
    
    return room_count
```

### Variation 2: Counting Rooms with Size Constraints
**Problem**: Count rooms with minimum or maximum size constraints.

**Link**: [CSES Problem Set - Counting Rooms with Size Constraints](https://cses.fi/problemset/task/counting_rooms_size_constraints)

```python
def counting_rooms_size_constraints(n, m, grid, min_size, max_size):
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def dfs_iterative(start_i, start_j):
        stack = [(start_i, start_j)]
        visited[start_i][start_j] = True
        room_size = 1
        
        while stack:
            i, j = stack.pop()
            
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < n and 0 <= nj < m and 
                    not visited[ni][nj] and grid[ni][nj] == '.'):
                    visited[ni][nj] = True
                    stack.append((ni, nj))
                    room_size += 1
        
        return room_size
    
    # Find all rooms with size constraints
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                room_size = dfs_iterative(i, j)
                if min_size <= room_size <= max_size:
                    room_count += 1
    
    return room_count
```

### Variation 3: Counting Rooms with Different Cell Types
**Problem**: Count rooms with different types of cells (multiple floor types).

**Link**: [CSES Problem Set - Counting Rooms with Multiple Cell Types](https://cses.fi/problemset/task/counting_rooms_multiple_types)

```python
def counting_rooms_multiple_types(n, m, grid, floor_types):
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def dfs_iterative(start_i, start_j, cell_type):
        stack = [(start_i, start_j)]
        visited[start_i][start_j] = True
        
        while stack:
            i, j = stack.pop()
            
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < n and 0 <= nj < m and 
                    not visited[ni][nj] and grid[ni][nj] == cell_type):
                    visited[ni][nj] = True
                    stack.append((ni, nj))
    
    # Find all rooms for each floor type
    for cell_type in floor_types:
        for i in range(n):
            for j in range(m):
                if grid[i][j] == cell_type and not visited[i][j]:
                    room_count += 1
                    dfs_iterative(i, j, cell_type)
    
    return room_count
```

## 🔗 Related Problems

- **[Labyrinth](/cses-analyses/problem_soulutions/graph_algorithms/labyrinth_analysis/)**: Grid traversal problems
- **[Message Route](/cses-analyses/problem_soulutions/graph_algorithms/message_route_analysis/)**: Graph traversal problems
- **[Building Roads](/cses-analyses/problem_soulutions/graph_algorithms/building_roads_analysis/)**: Connected component problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Connected Components**: Essential for analyzing graph connectivity
2. **DFS/BFS**: Key techniques for graph traversal and connected component finding
3. **Grid Traversal**: Important skill for 2D grid problems
4. **Visited Tracking**: Critical for avoiding infinite loops in graph algorithms
5. **Iterative vs Recursive**: Understanding trade-offs between different implementations
6. **Graph Theory**: Foundation for many optimization problems

## 📝 Summary

The Counting Rooms problem demonstrates fundamental connected component concepts for analyzing grid connectivity. We explored three approaches:

1. **Brute Force Connected Components**: O(2^(n×m) × (n + m)) time complexity using exhaustive search, inefficient for large grids
2. **DFS Connected Components**: O(n × m) time complexity using recursive DFS, optimal and intuitive approach
3. **Optimized DFS with Iterative Implementation**: O(n × m) time complexity using iterative DFS, most efficient approach

The key insights include understanding connected components as graph connectivity problems, using DFS/BFS for efficient component finding, and applying grid traversal techniques for 2D problems. This problem serves as an excellent introduction to connected component algorithms and grid traversal techniques.
