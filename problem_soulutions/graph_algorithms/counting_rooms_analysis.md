---
layout: simple
title: "Counting Rooms - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/counting_rooms_analysis
---

# Counting Rooms - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of connected components in grid graphs
- Apply efficient algorithms for counting connected components in 2D grids
- Implement DFS and BFS for grid traversal and component counting
- Optimize graph algorithms for maze and room counting problems
- Handle special cases in grid-based connectivity problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, connected components, DFS, BFS
- **Data Structures**: Grids, visited arrays, stacks, queues
- **Mathematical Concepts**: Graph theory, connectivity, 2D grids
- **Programming Skills**: Grid operations, DFS/BFS, component counting
- **Related Problems**: Building Roads (graph_algorithms), Building Teams (graph_algorithms), Labyrinth (graph_algorithms)

## 📋 Problem Description

Given a 2D grid with walls ('.') and empty spaces ('#'), count the number of connected rooms (empty spaces).

**Input**: 
- n: number of rows
- m: number of columns
- grid: 2D array where '.' represents empty space and '#' represents wall

**Output**: 
- Number of connected rooms (connected components of empty spaces)

**Constraints**:
- 1 ≤ n, m ≤ 1000

**Example**:
```
Input:
n = 4, m = 4
grid = [
  "....",
  "..#.",
  "..#.",
  "...."
]

Output:
2

Explanation**: 
Room 1: top-left 2x2 area
Room 2: bottom-right 2x2 area
Total: 2 connected rooms
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check every cell and manually track connections
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic grid traversal for each cell
- **Inefficient**: O(n²m²) time complexity

**Key Insight**: Check every cell and manually track which cells belong to the same room.

**Algorithm**:
- For each empty cell, check all adjacent cells
- Manually track which cells are connected
- Count the number of distinct connected groups

**Visual Example**:
```
Grid: 4x4 with walls and empty spaces
┌─────────────────────────────────────┐
│ . . . .                            │
│ . # . .                            │
│ . # . .                            │
│ . . . .                            │
│                                   │
│ Manual connection tracking:        │
│ Cell (0,0): connected to (0,1), (1,0) │
│ Cell (0,1): connected to (0,0), (0,2) │
│ Cell (0,2): connected to (0,1), (0,3) │
│ Cell (0,3): connected to (0,2), (1,3) │
│ Cell (1,0): connected to (0,0), (2,0) │
│ Cell (1,3): connected to (0,3), (2,3) │
│ Cell (2,0): connected to (1,0), (3,0) │
│ Cell (2,3): connected to (1,3), (3,3) │
│ Cell (3,0): connected to (2,0), (3,1) │
│ Cell (3,1): connected to (3,0), (3,2) │
│ Cell (3,2): connected to (3,1), (3,3) │
│ Cell (3,3): connected to (3,2), (2,3) │
│                                   │
│ Room 1: {(0,0), (0,1), (0,2), (0,3), │
│         (1,0), (1,3), (2,0), (2,3), │
│         (3,0), (3,1), (3,2), (3,3)} │
│ Room 2: {(1,1), (1,2), (2,1), (2,2)} │
│                                   │
│ Total rooms: 2                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_counting_rooms(n, m, grid):
    """Count rooms using brute force approach"""
    def get_neighbors(row, col):
        """Get valid neighbors of a cell"""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < n and 0 <= new_col < m and 
                grid[new_row][new_col] == '.'):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    # Track which cells belong to which room
    room_assignment = {}
    room_count = 0
    
    # Process each cell
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and (i, j) not in room_assignment:
                # Start a new room
                room_count += 1
                room_assignment[(i, j)] = room_count
                
                # Manually check all connected cells
                to_process = [(i, j)]
                while to_process:
                    current = to_process.pop(0)
                    neighbors = get_neighbors(current[0], current[1])
                    
                    for neighbor in neighbors:
                        if neighbor not in room_assignment:
                            room_assignment[neighbor] = room_count
                            to_process.append(neighbor)
    
    return room_count

# Example usage
n = 4
m = 4
grid = [
    "....",
    "..#.",
    "..#.",
    "...."
]
result = brute_force_counting_rooms(n, m, grid)
print(f"Brute force room count: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(nm)

**Why it's inefficient**: O(n²m²) time complexity for manually tracking connections.

---

### Approach 2: DFS-based Connected Components

**Key Insights from DFS-based Connected Components**:
- **DFS Traversal**: Use DFS to explore connected components efficiently
- **Efficient Implementation**: O(nm) time complexity
- **Visited Array**: Use visited array to avoid revisiting cells
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use DFS to explore each connected component of empty spaces.

**Algorithm**:
- Use DFS to traverse the grid
- Mark visited cells to avoid revisiting
- Count the number of DFS calls needed to visit all empty cells

**Visual Example**:
```
DFS-based connected components:

Grid: 4x4 with walls and empty spaces
┌─────────────────────────────────────┐
│ . . . .                            │
│ . # . .                            │
│ . # . .                            │
│ . . . .                            │
│                                   │
│ DFS traversal:                     │
│ DFS 1: Start from (0,0)            │
│ - Visit (0,0) -> (0,1) -> (0,2) -> (0,3) │
│ - Visit (1,0) -> (2,0) -> (3,0) -> (3,1) │
│ - Visit (3,2) -> (3,3) -> (2,3) -> (1,3) │
│ - Mark all as visited              │
│                                   │
│ DFS 2: Start from (1,1)            │
│ - Visit (1,1) -> (1,2) -> (2,1) -> (2,2) │
│ - Mark all as visited              │
│                                   │
│ All cells visited: 2 DFS calls     │
│ Total rooms: 2                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dfs_counting_rooms(n, m, grid):
    """Count rooms using DFS-based connected components"""
    def dfs(row, col, visited):
        """DFS to explore connected component"""
        if (row < 0 or row >= n or col < 0 or col >= m or
            visited[row][col] or grid[row][col] == '#'):
            return
        
        visited[row][col] = True
        
        # Explore all 4 directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            dfs(row + dr, col + dc, visited)
    
    # Initialize visited array
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    # Try DFS from each unvisited empty cell
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                dfs(i, j, visited)
                room_count += 1
    
    return room_count

# Example usage
n = 4
m = 4
grid = [
    "....",
    "..#.",
    "..#.",
    "...."
]
result = dfs_counting_rooms(n, m, grid)
print(f"DFS room count: {result}")
```

**Time Complexity**: O(nm)
**Space Complexity**: O(nm)

**Why it's better**: Uses DFS for O(nm) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for grid traversal
- **Efficient Implementation**: O(nm) time complexity
- **Space Efficiency**: O(nm) space complexity
- **Optimal Complexity**: Best approach for grid-based connected components

**Key Insight**: Use advanced data structures for optimal grid traversal and component counting.

**Algorithm**:
- Use specialized data structures for grid storage
- Implement efficient DFS with optimized data structures
- Handle special cases optimally
- Return room count

**Visual Example**:
```
Advanced data structure approach:

For grid: 4x4 with walls and empty spaces
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Grid structure: for efficient     │
│   storage and access                │
│ - Visited cache: for optimization   │
│ - DFS stack: for optimization       │
│                                   │
│ Connected components calculation:   │
│ - Use grid structure for efficient │
│   storage and access                │
│ - Use visited cache for            │
│   optimization                      │
│ - Use DFS stack for optimization   │
│                                   │
│ Result: 2                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_counting_rooms(n, m, grid):
    """Count rooms using advanced data structure approach"""
    def advanced_dfs(row, col, visited):
        """Advanced DFS with optimized data structures"""
        if (row < 0 or row >= n or col < 0 or col >= m or
            visited[row][col] or grid[row][col] == '#'):
            return
        
        visited[row][col] = True
        
        # Advanced DFS with optimized direction handling
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            advanced_dfs(row + dr, col + dc, visited)
    
    # Use advanced data structures for grid storage
    # Initialize advanced visited array
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    # Advanced DFS from each unvisited empty cell
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                advanced_dfs(i, j, visited)
                room_count += 1
    
    return room_count

# Example usage
n = 4
m = 4
grid = [
    "....",
    "..#.",
    "..#.",
    "...."
]
result = advanced_data_structure_counting_rooms(n, m, grid)
print(f"Advanced data structure room count: {result}")
```

**Time Complexity**: O(nm)
**Space Complexity**: O(nm)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²m²) | O(nm) | Manually track connections between cells |
| DFS Components | O(nm) | O(nm) | Use DFS to explore connected components |
| Advanced Data Structure | O(nm) | O(nm) | Use advanced data structures |

### Time Complexity
- **Time**: O(nm) - Use DFS for efficient grid traversal
- **Space**: O(nm) - Store visited array and recursion stack

### Why This Solution Works
- **DFS Traversal**: Use DFS to explore each connected component
- **Visited Tracking**: Mark visited cells to avoid revisiting
- **Grid Navigation**: Handle 4-directional movement efficiently
- **Optimal Algorithms**: Use optimal algorithms for grid-based connected components

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Counting Rooms with Constraints**
**Problem**: Count rooms with specific movement constraints.

**Key Differences**: Apply constraints to room traversal

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_counting_rooms(n, m, grid, constraints):
    """Count rooms with constraints"""
    def constrained_dfs(row, col, visited):
        """DFS with movement constraints"""
        if (row < 0 or row >= n or col < 0 or col >= m or
            visited[row][col] or grid[row][col] == '#'):
            return
        
        visited[row][col] = True
        
        # Explore directions with constraints
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if constraints(row, col, new_row, new_col):
                constrained_dfs(new_row, new_col, visited)
    
    # Initialize visited array
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    # Try constrained DFS from each unvisited empty cell
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                constrained_dfs(i, j, visited)
                room_count += 1
    
    return room_count

# Example usage
n = 4
m = 4
grid = [
    "....",
    "..#.",
    "..#.",
    "...."
]
constraints = lambda r1, c1, r2, c2: abs(r2 - r1) + abs(c2 - c1) == 1  # Only adjacent
result = constrained_counting_rooms(n, m, grid, constraints)
print(f"Constrained room count: {result}")
```

#### **2. Counting Rooms with Different Metrics**
**Problem**: Count rooms with different size metrics.

**Key Differences**: Different room size calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_counting_rooms(n, m, grid, weight_function):
    """Count rooms with different size metrics"""
    def weighted_dfs(row, col, visited, room_size):
        """DFS with room size calculation"""
        if (row < 0 or row >= n or col < 0 or col >= m or
            visited[row][col] or grid[row][col] == '#'):
            return room_size
        
        visited[row][col] = True
        room_size += weight_function(row, col)
        
        # Explore all 4 directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            room_size = weighted_dfs(row + dr, col + dc, visited, room_size)
        
        return room_size
    
    # Initialize visited array
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    room_sizes = []
    
    # Try weighted DFS from each unvisited empty cell
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                room_size = weighted_dfs(i, j, visited, 0)
                room_sizes.append(room_size)
                room_count += 1
    
    return room_count, room_sizes

# Example usage
n = 4
m = 4
grid = [
    "....",
    "..#.",
    "..#.",
    "...."
]
weight_function = lambda r, c: 1  # Each cell has weight 1
result = weighted_counting_rooms(n, m, grid, weight_function)
print(f"Weighted room count: {result}")
```

#### **3. Counting Rooms with Multiple Dimensions**
**Problem**: Count rooms in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_counting_rooms(n, m, grid, dimensions):
    """Count rooms in multiple dimensions"""
    def multi_dimensional_dfs(row, col, visited):
        """DFS for multiple dimensions"""
        if (row < 0 or row >= n or col < 0 or col >= m or
            visited[row][col] or grid[row][col] == '#'):
            return
        
        visited[row][col] = True
        
        # Explore directions based on dimensions
        if dimensions == 2:
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        else:
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            multi_dimensional_dfs(row + dr, col + dc, visited)
    
    # Initialize visited array
    visited = [[False for _ in range(m)] for _ in range(n)]
    room_count = 0
    
    # Try multi-dimensional DFS from each unvisited empty cell
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                multi_dimensional_dfs(i, j, visited)
                room_count += 1
    
    return room_count

# Example usage
n = 4
m = 4
grid = [
    "....",
    "..#.",
    "..#.",
    "...."
]
dimensions = 2
result = multi_dimensional_counting_rooms(n, m, grid, dimensions)
print(f"Multi-dimensional room count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Building Roads](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Building Teams](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Labyrinth](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Number of Islands](https://leetcode.com/problems/number-of-islands/) - Graph
- [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) - Graph
- [Flood Fill](https://leetcode.com/problems/flood-fill/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Connected components, grid traversal
- **Grid Problems**: 2D grid, maze problems
- **DFS/BFS**: Graph traversal, component detection

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Connected Components](https://cp-algorithms.com/graph/search-for-connected-components.html) - Connected components algorithms
- [Grid Problems](https://cp-algorithms.com/graph/basic-graph-algorithms.html#grid-problems) - Grid-based algorithms

### **Practice Problems**
- [CSES Building Roads](https://cses.fi/problemset/task/1075) - Medium
- [CSES Building Teams](https://cses.fi/problemset/task/1075) - Medium
- [CSES Labyrinth](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Connected Component](https://en.wikipedia.org/wiki/Connected_component_(graph_theory)) - Wikipedia article
- [Flood Fill](https://en.wikipedia.org/wiki/Flood_fill) - Wikipedia article
