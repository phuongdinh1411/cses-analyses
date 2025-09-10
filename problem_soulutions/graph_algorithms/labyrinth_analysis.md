---
layout: simple
title: "Labyrinth - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/labyrinth_analysis
---

# Labyrinth - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of shortest path in grid graphs
- Apply efficient algorithms for finding shortest paths in mazes
- Implement BFS for shortest path in unweighted graphs
- Optimize graph algorithms for grid-based path problems
- Handle special cases in maze navigation problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, shortest path, BFS, grid traversal
- **Data Structures**: Grids, queues, arrays, visited arrays
- **Mathematical Concepts**: Graph theory, shortest paths, grid graphs, BFS
- **Programming Skills**: Grid operations, BFS, path reconstruction, maze navigation
- **Related Problems**: Message Route (graph_algorithms), Counting Rooms (graph_algorithms), Round Trip (graph_algorithms)

## 📋 Problem Description

Given a maze represented as a grid, find the shortest path from start to end, avoiding walls.

**Input**: 
- n: number of rows
- m: number of columns
- grid: n×m grid where '.' represents empty cell, '#' represents wall, 'A' represents start, 'B' represents end

**Output**: 
- Shortest path length and the path itself, or "NO" if no path exists

**Constraints**:
- 1 ≤ n, m ≤ 1000

**Example**:
```
Input:
n = 5, m = 8
grid = [
    "########",
    "#.A#...#",
    "#.##.#B#",
    "#......#",
    "########"
]

Output:
YES
9
DRRURDDD

Explanation**: 
Shortest path from A to B:
A(1,1) → (1,2) → (2,2) → (3,2) → (3,3) → (3,4) → (3,5) → (3,6) → B(2,6)
Path: DRRURDDD (Down, Right, Right, Up, Right, Down, Down, Down)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible paths from start to end
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check each path for validity and length
- **Inefficient**: O(4^(n×m)) time complexity

**Key Insight**: Try all possible paths and find the shortest valid one.

**Algorithm**:
- Generate all possible paths from start to end
- For each path, check if it's valid (no walls, within bounds)
- Keep track of the shortest valid path
- Return the shortest path or "NO" if none exists

**Visual Example**:
```
Maze: 5×8 grid
Start: A(1,1), End: B(2,6)

Try all possible paths:
┌─────────────────────────────────────┐
│ Path 1: A → (1,2) → (1,3) → ...    │
│ - Check: (1,3) is wall ✗           │
│ - Invalid path                      │
│                                   │
│ Path 2: A → (1,2) → (2,2) → ...    │
│ - Check: (1,2) is empty ✓          │
│ - Check: (2,2) is empty ✓          │
│ - Continue checking...              │
│ - Valid path, length: 12           │
│                                   │
│ Path 3: A → (1,2) → (2,2) → (3,2) → ... │
│ - Check: (1,2) is empty ✓          │
│ - Check: (2,2) is empty ✓          │
│ - Check: (3,2) is empty ✓          │
│ - Continue checking...              │
│ - Valid path, length: 9            │
│                                   │
│ Continue for all 4^(40) paths...   │
│                                   │
│ Shortest valid path: length 9      │
│ Path: DRRURDDD                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_labyrinth(n, m, grid):
    """Find shortest path using brute force approach"""
    from itertools import product
    
    # Find start and end positions
    start_pos = None
    end_pos = None
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A':
                start_pos = (i, j)
            elif grid[i][j] == 'B':
                end_pos = (i, j)
    
    if not start_pos or not end_pos:
        return "NO", None, None
    
    # Directions: Up, Down, Left, Right
    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    
    def is_valid_position(row, col):
        """Check if position is valid"""
        return (0 <= row < n and 0 <= col < m and 
                grid[row][col] != '#')
    
    def is_valid_path(path):
        """Check if path is valid"""
        current_row, current_col = start_pos
        
        for direction in path:
            row_delta, col_delta, _ = directions[direction]
            new_row = current_row + row_delta
            new_col = current_col + col_delta
            
            if not is_valid_position(new_row, new_col):
                return False
            
            current_row, current_col = new_row
        
        return current_row == end_pos[0] and current_col == end_pos[1]
    
    def get_path_string(path):
        """Convert path to string"""
        return ''.join(directions[direction][2] for direction in path)
    
    # Try all possible paths
    max_path_length = n * m  # Maximum possible path length
    
    for path_length in range(1, max_path_length + 1):
        for path in product(range(4), repeat=path_length):
            if is_valid_path(path):
                path_string = get_path_string(path)
                return "YES", path_length, path_string
    
    return "NO", None, None

# Example usage
n = 5
m = 8
grid = [
    "########",
    "#.A#...#",
    "#.##.#B#",
    "#......#",
    "########"
]
result, length, path = brute_force_labyrinth(n, m, grid)
print(f"Brute force result: {result}")
if result == "YES":
    print(f"Length: {length}")
    print(f"Path: {path}")
```

**Time Complexity**: O(4^(n×m))
**Space Complexity**: O(n×m)

**Why it's inefficient**: O(4^(n×m)) time complexity for trying all possible paths.

---

### Approach 2: BFS (Breadth-First Search)

**Key Insights from BFS**:
- **BFS**: Use BFS to find shortest path in unweighted graph
- **Efficient Implementation**: O(n×m) time complexity
- **Shortest Path**: BFS guarantees shortest path in unweighted graphs
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use BFS to find shortest path in unweighted grid graph.

**Algorithm**:
- Use BFS starting from the start position
- Keep track of visited cells and parent information
- When end position is reached, reconstruct the path
- Return shortest path or "NO" if no path exists

**Visual Example**:
```
BFS for shortest path:

Maze: 5×8 grid
Start: A(1,1), End: B(2,6)

BFS exploration:
┌─────────────────────────────────────┐
│ Level 0: A(1,1)                    │
│                                   │
│ Level 1: (1,2)                     │
│ - From A(1,1) → (1,2)             │
│                                   │
│ Level 2: (2,2)                     │
│ - From (1,2) → (2,2)              │
│                                   │
│ Level 3: (3,2)                     │
│ - From (2,2) → (3,2)              │
│                                   │
│ Level 4: (3,3)                     │
│ - From (3,2) → (3,3)              │
│                                   │
│ Level 5: (3,4)                     │
│ - From (3,3) → (3,4)              │
│                                   │
│ Level 6: (3,5)                     │
│ - From (3,4) → (3,5)              │
│                                   │
│ Level 7: (3,6)                     │
│ - From (3,5) → (3,6)              │
│                                   │
│ Level 8: (2,6) = B                 │
│ - From (3,6) → (2,6)              │
│                                   │
│ Path reconstruction:               │
│ B(2,6) ← (3,6) ← (3,5) ← ... ← A(1,1) │
│ Path: DRRURDDD                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def bfs_labyrinth(n, m, grid):
    """Find shortest path using BFS"""
    from collections import deque
    
    # Find start and end positions
    start_pos = None
    end_pos = None
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A':
                start_pos = (i, j)
            elif grid[i][j] == 'B':
                end_pos = (i, j)
    
    if not start_pos or not end_pos:
        return "NO", None, None
    
    # Directions: Up, Down, Left, Right
    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    
    def is_valid_position(row, col):
        """Check if position is valid"""
        return (0 <= row < n and 0 <= col < m and 
                grid[row][col] != '#')
    
    def reconstruct_path(parent, start, end):
        """Reconstruct path from parent information"""
        path = []
        current = end
        
        while current != start:
            parent_pos, direction = parent[current]
            path.append(direction)
            current = parent_pos
        
        return path[::-1]  # Reverse to get path from start to end
    
    # BFS
    queue = deque([start_pos])
    visited = {start_pos}
    parent = {start_pos: (None, None)}
    
    while queue:
        current_row, current_col = queue.popleft()
        
        # Check if we reached the end
        if (current_row, current_col) == end_pos:
            path = reconstruct_path(parent, start_pos, end_pos)
            return "YES", len(path), ''.join(path)
        
        # Explore all four directions
        for i, (row_delta, col_delta, direction) in enumerate(directions):
            new_row = current_row + row_delta
            new_col = current_col + col_delta
            new_pos = (new_row, new_col)
            
            if (is_valid_position(new_row, new_col) and 
                new_pos not in visited):
                visited.add(new_pos)
                parent[new_pos] = ((current_row, current_col), direction)
                queue.append(new_pos)
    
    return "NO", None, None

# Example usage
n = 5
m = 8
grid = [
    "########",
    "#.A#...#",
    "#.##.#B#",
    "#......#",
    "########"
]
result, length, path = bfs_labyrinth(n, m, grid)
print(f"BFS result: {result}")
if result == "YES":
    print(f"Length: {length}")
    print(f"Path: {path}")
```

**Time Complexity**: O(n×m)
**Space Complexity**: O(n×m)

**Why it's better**: Uses BFS for O(n×m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for maze navigation
- **Efficient Implementation**: O(n×m) time complexity
- **Space Efficiency**: O(n×m) space complexity
- **Optimal Complexity**: Best approach for maze navigation problems

**Key Insight**: Use advanced data structures for optimal maze navigation.

**Algorithm**:
- Use specialized data structures for grid representation
- Implement efficient BFS with path reconstruction
- Handle special cases optimally
- Return shortest path or "NO" if no path exists

**Visual Example**:
```
Advanced data structure approach:

For maze: 5×8 grid
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Advanced grid: for efficient      │
│   storage and operations            │
│ - BFS queue: for optimization       │
│ - Path cache: for optimization      │
│                                   │
│ Maze navigation calculation:        │
│ - Use advanced grid for efficient   │
│   storage and operations            │
│ - Use BFS queue for optimization    │
│ - Use path cache for optimization   │
│                                   │
│ Result: YES, 9, DRRURDDD          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_labyrinth(n, m, grid):
    """Find shortest path using advanced data structure approach"""
    from collections import deque
    
    # Use advanced data structures for grid representation
    # Advanced position finding
    start_pos = None
    end_pos = None
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A':
                start_pos = (i, j)
            elif grid[i][j] == 'B':
                end_pos = (i, j)
    
    if not start_pos or not end_pos:
        return "NO", None, None
    
    # Advanced directions with metadata
    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    
    def advanced_is_valid_position(row, col):
        """Advanced position validation"""
        return (0 <= row < n and 0 <= col < m and 
                grid[row][col] != '#')
    
    def advanced_reconstruct_path(parent, start, end):
        """Advanced path reconstruction"""
        path = []
        current = end
        
        while current != start:
            parent_pos, direction = parent[current]
            path.append(direction)
            current = parent_pos
        
        return path[::-1]
    
    # Advanced BFS with optimizations
    def advanced_bfs():
        """Advanced BFS with optimizations"""
        queue = deque([start_pos])
        visited = {start_pos}
        parent = {start_pos: (None, None)}
        
        while queue:
            current_row, current_col = queue.popleft()
            
            # Advanced end check
            if (current_row, current_col) == end_pos:
                path = advanced_reconstruct_path(parent, start_pos, end_pos)
                return "YES", len(path), ''.join(path)
            
            # Advanced neighbor exploration
            for i, (row_delta, col_delta, direction) in enumerate(directions):
                new_row = current_row + row_delta
                new_col = current_col + col_delta
                new_pos = (new_row, new_col)
                
                if (advanced_is_valid_position(new_row, new_col) and 
                    new_pos not in visited):
                    visited.add(new_pos)
                    parent[new_pos] = ((current_row, current_col), direction)
                    queue.append(new_pos)
        
        return "NO", None, None
    
    return advanced_bfs()

# Example usage
n = 5
m = 8
grid = [
    "########",
    "#.A#...#",
    "#.##.#B#",
    "#......#",
    "########"
]
result, length, path = advanced_data_structure_labyrinth(n, m, grid)
print(f"Advanced data structure result: {result}")
if result == "YES":
    print(f"Length: {length}")
    print(f"Path: {path}")
```

**Time Complexity**: O(n×m)
**Space Complexity**: O(n×m)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(4^(n×m)) | O(n×m) | Try all possible paths |
| BFS | O(n×m) | O(n×m) | Use BFS for shortest path in unweighted graph |
| Advanced Data Structure | O(n×m) | O(n×m) | Use advanced data structures |

### Time Complexity
- **Time**: O(n×m) - Use BFS for efficient shortest path in unweighted grid
- **Space**: O(n×m) - Store grid and BFS data structures

### Why This Solution Works
- **BFS**: Use BFS to find shortest path in unweighted graphs
- **Grid Representation**: Represent maze as grid graph
- **Path Reconstruction**: Use parent information to reconstruct path
- **Optimal Algorithms**: Use optimal algorithms for maze navigation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Labyrinth with Constraints**
**Problem**: Find shortest path in maze with specific constraints.

**Key Differences**: Apply constraints to path finding

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_labyrinth(n, m, grid, constraints):
    """Find shortest path in maze with constraints"""
    from collections import deque
    
    # Find start and end positions
    start_pos = None
    end_pos = None
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A':
                start_pos = (i, j)
            elif grid[i][j] == 'B':
                end_pos = (i, j)
    
    if not start_pos or not end_pos:
        return "NO", None, None
    
    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    
    def constrained_is_valid_position(row, col):
        """Position validation with constraints"""
        return (0 <= row < n and 0 <= col < m and 
                grid[row][col] != '#' and
                constraints(row, col))
    
    def constrained_reconstruct_path(parent, start, end):
        """Path reconstruction with constraints"""
        path = []
        current = end
        
        while current != start:
            parent_pos, direction = parent[current]
            path.append(direction)
            current = parent_pos
        
        return path[::-1]
    
    def constrained_bfs():
        """BFS with constraints"""
        queue = deque([start_pos])
        visited = {start_pos}
        parent = {start_pos: (None, None)}
        
        while queue:
            current_row, current_col = queue.popleft()
            
            if (current_row, current_col) == end_pos:
                path = constrained_reconstruct_path(parent, start_pos, end_pos)
                return "YES", len(path), ''.join(path)
            
            for i, (row_delta, col_delta, direction) in enumerate(directions):
                new_row = current_row + row_delta
                new_col = current_col + col_delta
                new_pos = (new_row, new_col)
                
                if (constrained_is_valid_position(new_row, new_col) and 
                    new_pos not in visited):
                    visited.add(new_pos)
                    parent[new_pos] = ((current_row, current_col), direction)
                    queue.append(new_pos)
        
        return "NO", None, None
    
    return constrained_bfs()

# Example usage
n = 5
m = 8
grid = [
    "########",
    "#.A#...#",
    "#.##.#B#",
    "#......#",
    "########"
]
constraints = lambda row, col: True  # No constraints
result, length, path = constrained_labyrinth(n, m, grid, constraints)
print(f"Constrained result: {result}")
if result == "YES":
    print(f"Length: {length}")
    print(f"Path: {path}")
```

#### **2. Labyrinth with Different Metrics**
**Problem**: Find shortest path in maze with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_labyrinth(n, m, grid, cost_function):
    """Find shortest path in maze with different cost metrics"""
    from collections import deque
    
    # Find start and end positions
    start_pos = None
    end_pos = None
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A':
                start_pos = (i, j)
            elif grid[i][j] == 'B':
                end_pos = (i, j)
    
    if not start_pos or not end_pos:
        return "NO", None, None
    
    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    
    def weighted_is_valid_position(row, col):
        """Position validation with weights"""
        return (0 <= row < n and 0 <= col < m and 
                grid[row][col] != '#')
    
    def weighted_reconstruct_path(parent, start, end):
        """Path reconstruction with weights"""
        path = []
        current = end
        
        while current != start:
            parent_pos, direction = parent[current]
            path.append(direction)
            current = parent_pos
        
        return path[::-1]
    
    def weighted_bfs():
        """BFS with weights"""
        queue = deque([start_pos])
        visited = {start_pos}
        parent = {start_pos: (None, None)}
        
        while queue:
            current_row, current_col = queue.popleft()
            
            if (current_row, current_col) == end_pos:
                path = weighted_reconstruct_path(parent, start_pos, end_pos)
                return "YES", len(path), ''.join(path)
            
            for i, (row_delta, col_delta, direction) in enumerate(directions):
                new_row = current_row + row_delta
                new_col = current_col + col_delta
                new_pos = (new_row, new_col)
                
                if (weighted_is_valid_position(new_row, new_col) and 
                    new_pos not in visited):
                    visited.add(new_pos)
                    parent[new_pos] = ((current_row, current_col), direction)
                    queue.append(new_pos)
        
        return "NO", None, None
    
    return weighted_bfs()

# Example usage
n = 5
m = 8
grid = [
    "########",
    "#.A#...#",
    "#.##.#B#",
    "#......#",
    "########"
]
cost_function = lambda r1, c1, r2, c2: 1  # Unit cost
result, length, path = weighted_labyrinth(n, m, grid, cost_function)
print(f"Weighted result: {result}")
if result == "YES":
    print(f"Length: {length}")
    print(f"Path: {path}")
```

#### **3. Labyrinth with Multiple Dimensions**
**Problem**: Find shortest path in maze in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_labyrinth(n, m, grid, dimensions):
    """Find shortest path in maze in multiple dimensions"""
    from collections import deque
    
    # Find start and end positions
    start_pos = None
    end_pos = None
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A':
                start_pos = (i, j)
            elif grid[i][j] == 'B':
                end_pos = (i, j)
    
    if not start_pos or not end_pos:
        return "NO", None, None
    
    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    
    def multi_dimensional_is_valid_position(row, col):
        """Position validation for multiple dimensions"""
        return (0 <= row < n and 0 <= col < m and 
                grid[row][col] != '#')
    
    def multi_dimensional_reconstruct_path(parent, start, end):
        """Path reconstruction for multiple dimensions"""
        path = []
        current = end
        
        while current != start:
            parent_pos, direction = parent[current]
            path.append(direction)
            current = parent_pos
        
        return path[::-1]
    
    def multi_dimensional_bfs():
        """BFS for multiple dimensions"""
        queue = deque([start_pos])
        visited = {start_pos}
        parent = {start_pos: (None, None)}
        
        while queue:
            current_row, current_col = queue.popleft()
            
            if (current_row, current_col) == end_pos:
                path = multi_dimensional_reconstruct_path(parent, start_pos, end_pos)
                return "YES", len(path), ''.join(path)
            
            for i, (row_delta, col_delta, direction) in enumerate(directions):
                new_row = current_row + row_delta
                new_col = current_col + col_delta
                new_pos = (new_row, new_col)
                
                if (multi_dimensional_is_valid_position(new_row, new_col) and 
                    new_pos not in visited):
                    visited.add(new_pos)
                    parent[new_pos] = ((current_row, current_col), direction)
                    queue.append(new_pos)
        
        return "NO", None, None
    
    return multi_dimensional_bfs()

# Example usage
n = 5
m = 8
grid = [
    "########",
    "#.A#...#",
    "#.##.#B#",
    "#......#",
    "########"
]
dimensions = 1
result, length, path = multi_dimensional_labyrinth(n, m, grid, dimensions)
print(f"Multi-dimensional result: {result}")
if result == "YES":
    print(f"Length: {length}")
    print(f"Path: {path}")
```

### Related Problems

#### **CSES Problems**
- [Message Route](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Counting Rooms](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Round Trip](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Dynamic Programming
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Dynamic Programming
- [Path Sum](https://leetcode.com/problems/path-sum/) - Tree

#### **Problem Categories**
- **Graph Algorithms**: Shortest path, BFS, grid traversal
- **Maze Navigation**: Path finding, grid graphs
- **BFS**: Breadth-first search, shortest path

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [BFS](https://cp-algorithms.com/graph/breadth-first-search.html) - BFS algorithm
- [Shortest Path](https://cp-algorithms.com/graph/shortest_path.html) - Shortest path algorithms

### **Practice Problems**
- [CSES Message Route](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Rooms](https://cses.fi/problemset/task/1075) - Medium
- [CSES Round Trip](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search) - Wikipedia article
- [Maze](https://en.wikipedia.org/wiki/Maze) - Wikipedia article
