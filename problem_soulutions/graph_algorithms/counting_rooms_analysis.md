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

## 📋 Problem Description

You are given a map of a building, and your task is to count the number of its rooms. The size of the map is n×m squares, and each square is either floor or wall. You can walk left, right, up, and down through the floor squares.

A room is defined as a connected component of floor squares. Two floor squares are connected if you can walk from one to the other using only floor squares, moving in the four cardinal directions.

**Input**: 
- First line: Two integers n and m (height and width of the map)
- Next n lines: m characters each (". " denotes floor, "#" denotes wall)

**Output**: 
- One integer: the number of rooms

**Constraints**:
- 1 ≤ n, m ≤ 1000

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

### 📊 Visual Example

**Input Grid:**
```
########
#..#...#
####.#.#
#..#...#
########

Legend: # = Wall, . = Floor
```

**Grid Visualization:**
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

**Room Identification:**
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

**DFS Traversal Visualization:**
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

**Algorithm Flowchart:**
```
┌─────────────────────────────────────┐
│ Start: Read grid dimensions         │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Read grid and mark walls            │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Initialize room_count = 0           │
│ Initialize visited array            │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ For each cell (i,j):                │
│   If cell is floor and not visited: │
│     room_count++                    │
│     DFS from (i,j)                  │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return room_count                   │
└─────────────────────────────────────┘
```

**DFS Function:**
```
┌─────────────────────────────────────┐
│ DFS(row, col):                      │
│   Mark (row,col) as visited         │
│   For each direction (up,down,left,right):│
│     new_row = row + dr              │
│     new_col = col + dc              │
│     If valid and floor and not visited:│
│       DFS(new_row, new_col)         │
└─────────────────────────────────────┘
```

**Direction Vectors:**
```
Directions: up, down, left, right
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

Example from (1,4):
┌─────────────────────────────────────┐
│ Up: (0,4) - Wall, skip             │
│ Down: (2,4) - Floor, visit         │
│ Left: (1,3) - Floor, visit         │
│ Right: (1,5) - Floor, visit        │
└─────────────────────────────────────┘
```

**Final Result:**
```
Total rooms found: 3
Room 1: 2 squares (top-left)
Room 2: 8 squares (middle)
Room 3: 2 squares (bottom)

Answer: 3
```

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count connected components (rooms) in a grid
- **Key Insight**: Use DFS/BFS to explore each room completely
- **Challenge**: Handle large grids efficiently and avoid revisiting cells

### Step 2: Brute Force Approach
**Use depth-first search to explore each room and mark visited cells:**

```python
def counting_rooms_dfs(n, m, grid):
    def dfs(row, col):
        if (row < 0 or row >= n or col < 0 or col >= m or 
            grid[row][col] == '#' or visited[row][col]):
            return
        
        visited[row][col] = True
        
        # Explore all four directions
        dfs(row + 1, col)  # Down
        dfs(row - 1, col)  # Up
        dfs(row, col + 1)  # Right
        dfs(row, col - 1)  # Left
    
    visited = [[False] * m for _ in range(n)]
    rooms = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                dfs(i, j)
                rooms += 1
    
    return rooms
```

**Complexity**: O(n × m) - optimal for this problem

### Step 3: Optimization
**Use iterative DFS with stack to avoid recursion stack overflow:**

```python
def counting_rooms_iterative_dfs(n, m, grid):
    def dfs_iterative(start_row, start_col):
        stack = [(start_row, start_col)]
        
        while stack:
            row, col = stack.pop()
            
            if (row < 0 or row >= n or col < 0 or col >= m or 
                grid[row][col] == '#' or visited[row][col]):
                continue
            
            visited[row][col] = True
            
            # Add all four directions to stack
            stack.append((row + 1, col))  # Down
            stack.append((row - 1, col))  # Up
            stack.append((row, col + 1))  # Right
            stack.append((row, col - 1))  # Left
    
    visited = [[False] * m for _ in range(n)]
    rooms = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                dfs_iterative(i, j)
                rooms += 1
    
    return rooms
```

**Why this improvement works**: Iterative DFS avoids potential stack overflow for very large grids and can be more efficient in some cases.

### Improvement 2: BFS with Queue - O(n*m)
**Description**: Use breadth-first search with a queue for level-by-level exploration.

```python
from collections import deque

def counting_rooms_bfs(n, m, grid):
    def bfs(start_row, start_col):
        queue = deque([(start_row, start_col)])
        
        while queue:
            row, col = queue.popleft()
            
            if (row < 0 or row >= n or col < 0 or col >= m or 
                grid[row][col] == '#' or visited[row][col]):
                continue
            
            visited[row][col] = True
            
            # Add all four directions to queue
            queue.append((row + 1, col))  # Down
            queue.append((row - 1, col))  # Up
            queue.append((row, col + 1))  # Right
            queue.append((row, col - 1))  # Left
    
    visited = [[False] * m for _ in range(n)]
    rooms = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                bfs(i, j)
                rooms += 1
    
    return rooms
```

**Why this improvement works**: BFS explores the room level by level, which can be more memory-efficient for very large rooms.

### Alternative: Union-Find (Disjoint Set) - O(n*m * α(n*m))
**Description**: Use union-find data structure to connect adjacent floor cells.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

def counting_rooms_union_find(n, m, grid):
    uf = UnionFind(n * m)
    
    # Connect adjacent floor cells
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                continue
            
            current = i * m + j
            
            # Check all four directions
            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ni, nj = i + di, j + dj
                if (0 <= ni < n and 0 <= nj < m and 
                    grid[ni][nj] == '.'):
                    neighbor = ni * m + nj
                    uf.union(current, neighbor)
    
    # Count unique components
    components = set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.':
                components.add(uf.find(i * m + j))
    
    return len(components)
```

**Why this works**: Union-find connects all adjacent floor cells into components, and the number of unique components gives us the number of rooms.

## Final Optimal Solution

```python
n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

def dfs(row, col):
    if (row < 0 or row >= n or col < 0 or col >= m or 
        grid[row][col] == '#' or visited[row][col]):
        return
    
    visited[row][col] = True
    
    # Explore all four directions
    dfs(row + 1, col)  # Down
    dfs(row - 1, col)  # Up
    dfs(row, col + 1)  # Right
    dfs(row, col - 1)  # Left

visited = [[False] * m for _ in range(n)]
rooms = 0

for i in range(n):
    for j in range(m):
        if grid[i][j] == '.' and not visited[i][j]:
            dfs(i, j)
            rooms += 1

print(rooms)

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 8, [
            "########",
            "#..#...#",
            "####.#.#",
            "#..#...#",
            "########"
        ]), 3),
        ((3, 3, [
            "...",
            "...",
            "..."
        ]), 1),  # One large room
        ((3, 3, [
            "###",
            "###",
            "###"
        ]), 0),  # No rooms
        ((2, 2, [
            ".#",
            "#."
        ]), 2),  # Two small rooms
    ]
    
    for (n, m, grid), expected in test_cases:
        result = count_rooms(n, m, grid)
        print(f"n={n}, m={m}, grid:")
        for row in grid:
            print(f"  {row}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def count_rooms(n, m, grid):
    def dfs_iterative(start_row, start_col):
        stack = [(start_row, start_col)]
        
        while stack:
            row, col = stack.pop()
            
            if (row < 0 or row >= n or col < 0 or col >= m or 
                grid[row][col] == '#' or visited[row][col]):
                continue
            
            visited[row][col] = True
            
            # Add all four directions to stack
            stack.append((row + 1, col))  # Down
            stack.append((row - 1, col))  # Up
            stack.append((row, col + 1))  # Right
            stack.append((row, col - 1))  # Left
    
    visited = [[False] * m for _ in range(n)]
    rooms = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                dfs_iterative(i, j)
                rooms += 1
    
    return rooms

test_solution()
```
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n × m) - single pass through grid
- **Space**: O(n × m) - visited array and stack storage

### Why This Solution Works
- **DFS/BFS**: Optimal for finding connected components
- **Grid Traversal**: Efficient 4-directional movement
- **Visited Tracking**: Prevents revisiting cells
- **Component Counting**: Increments counter for each new room

## 🎨 Visual Example

### Input Example
```
5×8 grid:
########
#..#...#
####.#.#
#..#...#
########
```

### Grid Visualization
```
Row 0: ########
Row 1: #..#...#
Row 2: ####.#.#
Row 3: #..#...#
Row 4: ########

Legend: # = Wall, . = Floor
```

### Room Identification
```
Room 1 (Top-left): 2 floor squares
########
#..*....#  ← Room 1: (1,1), (1,2)
####.#.#
#..#...#
########

Room 2 (Middle): 6 floor squares
########
#..#...#
####.#.#
#..*....#  ← Room 2: (3,1), (3,2), (3,4), (3,5), (3,6), (2,5)
########

Room 3 (Bottom): 2 floor squares
########
#..#...#
####.#.#
#..#...#
########
```

### DFS Traversal Process
```
Step 1: Start DFS from (1,1)
- Visit (1,1), mark as visited
- Explore neighbors: (1,2), (0,1), (2,1)
- (0,1) is wall, skip
- (2,1) is wall, skip
- Visit (1,2), mark as visited
- No more unvisited floor neighbors
- Room 1 complete: 2 squares

Step 2: Start DFS from (3,1) (unvisited floor)
- Visit (3,1), mark as visited
- Explore neighbors: (3,2), (2,1), (4,1)
- (2,1) is wall, skip
- (4,1) is wall, skip
- Visit (3,2), mark as visited
- Continue exploring...
- Room 2 complete: 6 squares

Step 3: Start DFS from (3,4) (unvisited floor)
- Visit (3,4), mark as visited
- Explore neighbors...
- Room 3 complete: 2 squares

Total Rooms: 3
```

### 4-Directional Movement
```
For each floor cell (r, c), explore:
- Up: (r-1, c)
- Down: (r+1, c)
- Left: (r, c-1)
- Right: (r, c+1)

Example from (3,1):
- Up (2,1): Wall, skip
- Down (4,1): Wall, skip
- Left (3,0): Wall, skip
- Right (3,2): Floor, visit
```

### Visited Tracking
```
Visited array (5×8):
Row 0: [T,T,T,T,T,T,T,T]  (all walls)
Row 1: [T,F,F,T,T,T,T,T]  (visited floor cells)
Row 2: [T,T,T,T,T,F,T,T]  (visited floor cells)
Row 3: [T,F,F,T,F,F,F,T]  (visited floor cells)
Row 4: [T,T,T,T,T,T,T,T]  (all walls)

T = Visited, F = Not visited
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DFS Recursive   │ O(n×m)       │ O(n×m)       │ Recursive    │
│                 │              │              │ exploration  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ BFS Iterative   │ O(n×m)       │ O(n×m)       │ Queue-based  │
│                 │              │              │ exploration  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Union-Find      │ O(n×m·α(n×m))│ O(n×m)       │ Efficient    │
│                 │              │              │ connectivity │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Connected Components in Grids**
- Use graph traversal algorithms to find connected components in grid-based problems
- Important for understanding
- Enables efficient room counting
- Essential for algorithm

### 2. **DFS vs BFS for Graph Traversal**
- Choose between DFS and BFS based on problem requirements and constraints
- Important for understanding
- Provides flexibility in approach
- Essential for optimization

### 3. **Grid Representation**
- Represent grids as graphs where adjacent cells are connected nodes
- Important for understanding
- Enables graph algorithm application
- Essential for implementation

### 4. **Union-Find for Connectivity**
- Use union-find data structure to efficiently handle connectivity queries
- Important for understanding
- Provides alternative approach
- Essential for advanced solutions

## 🎯 Problem Variations

### Variation 1: Counting Rooms with Diagonal Movement
**Problem**: Allow diagonal movement in addition to 4-directional movement.

## Notable Techniques

### 1. **DFS Pattern**
```python
def dfs(row, col):
    if not valid_cell(row, col) or visited[row][col]:
        return
    visited[row][col] = True
    for dr, dc in directions:
        dfs(row + dr, col + dc)
```

### 2. **BFS Pattern**
```python
from collections import deque
def bfs(start_row, start_col):
    queue = deque([(start_row, start_col)])
    visited[start_row][start_col] = True
    
    while queue:
        row, col = queue.popleft()
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if valid_cell(new_row, new_col) and not visited[new_row][new_col]:
                visited[new_row][new_col] = True
                queue.append((new_row, new_col))
```

### 3. **Union-Find Pattern**
```python
class UnionFind:
    def __init__(self, n, m):
        self.parent = list(range(n * m))
        self.rank = [0] * (n * m)
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
```

## Problem-Solving Framework

1. **Identify problem type**: This is a connected components problem in a grid
2. **Choose approach**: Use DFS, BFS, or Union-Find
3. **Initialize**: Set up visited array and grid representation
4. **Traverse grid**: Visit each unvisited cell
5. **Count components**: Increment counter for each new component
6. **Handle boundaries**: Check grid boundaries and walls
7. **Return result**: Output total number of rooms

---

*This analysis shows how to efficiently count connected components in grid-based problems using graph traversal algorithms.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Counting Rooms with Costs**
**Problem**: Each room has a cost to enter, find total cost to visit all rooms.
```python
def cost_based_counting_rooms(n, m, grid, costs):
    # costs[i][j] = cost to enter room at position (i, j)
    
    visited = [[False] * m for _ in range(n)]
    total_cost = 0
    room_count = 0
    
    def dfs(row, col):
        if (row < 0 or row >= n or col < 0 or col >= m or 
            grid[row][col] == '#' or visited[row][col]):
            return 0
        
        visited[row][col] = True
        room_cost = costs[row][col]
        
        # Explore all four directions
        total = room_cost
        total += dfs(row + 1, col)  # Down
        total += dfs(row - 1, col)  # Up
        total += dfs(row, col + 1)  # Right
        total += dfs(row, col - 1)  # Left
        
        return total
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                component_cost = dfs(i, j)
                total_cost += component_cost
                room_count += 1
    
    return room_count, total_cost
```

#### **Variation 2: Counting Rooms with Constraints**
**Problem**: Count rooms with constraints on room size or connectivity.
```python
def constrained_counting_rooms(n, m, grid, constraints):
    # constraints = {'min_size': x, 'max_size': y, 'min_rooms': z}
    
    visited = [[False] * m for _ in range(n)]
    room_sizes = []
    
    def dfs(row, col):
        if (row < 0 or row >= n or col < 0 or col >= m or 
            grid[row][col] == '#' or visited[row][col]):
            return 0
        
        visited[row][col] = True
        size = 1
        
        # Explore all four directions
        size += dfs(row + 1, col)  # Down
        size += dfs(row - 1, col)  # Up
        size += dfs(row, col + 1)  # Right
        size += dfs(row, col - 1)  # Left
        
        return size
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                room_size = dfs(i, j)
                
                # Apply size constraints
                if 'min_size' in constraints and room_size < constraints['min_size']:
                    continue
                if 'max_size' in constraints and room_size > constraints['max_size']:
                    continue
                
                room_sizes.append(room_size)
    
    # Check minimum rooms constraint
    if 'min_rooms' in constraints and len(room_sizes) < constraints['min_rooms']:
        return -1  # Constraint violated
    
    return len(room_sizes), room_sizes
```

#### **Variation 3: Counting Rooms with Probabilities**
**Problem**: Each cell has a probability of being accessible, find expected number of rooms.
```python
def probabilistic_counting_rooms(n, m, grid, probabilities):
    # probabilities[i][j] = probability that cell (i, j) is accessible
    
    # Use Monte Carlo simulation
    import random
    
    def simulate_room_counting():
        # Randomly sample accessible cells
        accessible_grid = [['#'] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if grid[i][j] == '.' and random.random() < probabilities[i][j]:
                    accessible_grid[i][j] = '.'
        
        # Count rooms in accessible grid
        visited = [[False] * m for _ in range(n)]
        room_count = 0
        
        def dfs(row, col):
            if (row < 0 or row >= n or col < 0 or col >= m or 
                accessible_grid[row][col] == '#' or visited[row][col]):
                return
            
            visited[row][col] = True
            
            # Explore all four directions
            dfs(row + 1, col)  # Down
            dfs(row - 1, col)  # Up
            dfs(row, col + 1)  # Right
            dfs(row, col - 1)  # Left
        
        for i in range(n):
            for j in range(m):
                if accessible_grid[i][j] == '.' and not visited[i][j]:
                    dfs(i, j)
                    room_count += 1
        
        return room_count
    
    # Run multiple simulations
    num_simulations = 1000
    total_rooms = 0
    
    for _ in range(num_simulations):
        room_count = simulate_room_counting()
        total_rooms += room_count
    
    expected_rooms = total_rooms / num_simulations
    return expected_rooms
```

#### **Variation 4: Counting Rooms with Multiple Criteria**
**Problem**: Count rooms considering multiple criteria (size, cost, connectivity).
```python
def multi_criteria_counting_rooms(n, m, grid, criteria):
    # criteria = {'size_weight': x, 'cost_weight': y, 'connectivity_weight': z}
    
    visited = [[False] * m for _ in range(n)]
    room_data = []
    
    def dfs(row, col):
        if (row < 0 or row >= n or col < 0 or col >= m or 
            grid[row][col] == '#' or visited[row][col]):
            return 0, 0, 0
        
        visited[row][col] = True
        size = 1
        cost = criteria.get('costs', {}).get((row, col), 0)
        connectivity = 0
        
        # Count connections
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (0 <= row + dr < n and 0 <= col + dc < m and 
                grid[row + dr][col + dc] == '.'):
                connectivity += 1
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            s, c, conn = dfs(row + dr, col + dc)
            size += s
            cost += c
            connectivity += conn
        
        return size, cost, connectivity
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                size, cost, connectivity = dfs(i, j)
                
                # Calculate weighted score
                score = (size * criteria.get('size_weight', 1) + 
                        cost * criteria.get('cost_weight', 1) + 
                        connectivity * criteria.get('connectivity_weight', 1))
                
                room_data.append((size, cost, connectivity, score))
    
    return len(room_data), room_data
```

#### **Variation 5: Counting Rooms with Dynamic Updates**
**Problem**: Handle dynamic updates to the grid and count rooms after each update.
```python
def dynamic_counting_rooms(n, m, initial_grid, updates):
    # updates = [(row, col, new_value), ...]
    
    grid = [row[:] for row in initial_grid]
    results = []
    
    for row, col, new_value in updates:
        # Update grid
        grid[row][col] = new_value
        
        # Count rooms
        visited = [[False] * m for _ in range(n)]
        room_count = 0
        
        def dfs(r, c):
            if (r < 0 or r >= n or c < 0 or c >= m or 
                grid[r][c] == '#' or visited[r][c]):
                return
            
            visited[r][c] = True
            
            # Explore all four directions
            dfs(r + 1, c)  # Down
            dfs(r - 1, c)  # Up
            dfs(r, c + 1)  # Right
            dfs(r, c - 1)  # Left
        
        for i in range(n):
            for j in range(m):
                if grid[i][j] == '.' and not visited[i][j]:
                    dfs(i, j)
                    room_count += 1
        
        results.append(room_count)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Grid Problems**
- **Grid Traversal**: Traverse grids efficiently
- **Connected Components**: Find connected components in grids
- **Flood Fill**: Fill connected regions in grids
- **Grid Representation**: Represent grids as graphs

#### **2. Connected Components Problems**
- **Component Counting**: Count connected components
- **Component Analysis**: Analyze component properties
- **Component Traversal**: Traverse connected components
- **Component Optimization**: Optimize component algorithms

#### **3. Graph Traversal Problems**
- **DFS/BFS**: Graph traversal algorithms
- **Path Finding**: Find paths in graphs
- **Graph Exploration**: Explore graph structures
- **Traversal Optimization**: Optimize traversal algorithms

#### **4. Spatial Problems**
- **Spatial Analysis**: Analyze spatial relationships
- **Spatial Connectivity**: Analyze spatial connectivity
- **Spatial Optimization**: Optimize spatial algorithms
- **Spatial Data Structures**: Efficient spatial data structures

#### **5. Algorithmic Techniques**
- **Union-Find**: Efficient connectivity data structure
- **Flood Fill**: Fill connected regions
- **Component Detection**: Detect connected components
- **Grid Algorithms**: Specialized grid algorithms

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Grids**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().strip()
        grid.append(row)
    
    result = count_rooms(n, m, grid)
    print(result)
```

#### **2. Range Queries on Grid Regions**
```python
def range_room_queries(n, m, grid, queries):
    # queries = [(start_row, end_row, start_col, end_col), ...]
    
    results = []
    for start_row, end_row, start_col, end_col in queries:
        # Extract subgrid
        subgrid = []
        for i in range(start_row, end_row + 1):
            subgrid.append(grid[i][start_col:end_col + 1])
        
        result = count_rooms(len(subgrid), len(subgrid[0]), subgrid)
        results.append(result)
    
    return results
```

#### **3. Interactive Room Counting Problems**
```python
def interactive_counting_rooms():
    n = int(input("Enter number of rows: "))
    m = int(input("Enter number of columns: "))
    print("Enter grid (use '.' for rooms, '#' for walls):")
    grid = []
    for _ in range(n):
        row = input().strip()
        grid.append(row)
    
    result = count_rooms(n, m, grid)
    print(f"Number of rooms: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Grid Graph Theory**: Mathematical theory of grid graphs
- **Component Theory**: Mathematical theory of connected components
- **Traversal Theory**: Mathematical theory of graph traversal
- **Connectivity Theory**: Mathematical theory of connectivity

#### **2. Spatial Theory**
- **Spatial Analysis**: Mathematical spatial analysis
- **Spatial Connectivity**: Mathematical spatial connectivity
- **Spatial Optimization**: Mathematical spatial optimization
- **Spatial Algorithms**: Mathematical spatial algorithms

#### **3. Optimization Theory**
- **Component Optimization**: Mathematical component optimization
- **Traversal Optimization**: Mathematical traversal optimization
- **Grid Optimization**: Mathematical grid optimization
- **Spatial Optimization**: Mathematical spatial optimization

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **DFS/BFS**: Graph traversal algorithms
- **Union-Find**: Efficient connectivity data structure
- **Flood Fill**: Fill connected regions
- **Grid Algorithms**: Specialized grid algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Spatial Theory**: Mathematical spatial theory
- **Optimization Theory**: Mathematical optimization techniques
- **Connectivity Theory**: Mathematical connectivity theory

#### **3. Programming Concepts**
- **Grid Representations**: Efficient grid representations
- **Traversal Techniques**: Efficient traversal techniques
- **Component Detection**: Efficient component detection
- **Spatial Data Structures**: Efficient spatial data structures

---

*This analysis demonstrates efficient grid traversal techniques and shows various extensions for counting rooms problems.*

---

## 🔗 Related Problems

- **[Connected Components](/cses-analyses/problem_soulutions/graph_algorithms/)**: Component counting problems
- **[Grid Traversal](/cses-analyses/problem_soulutions/graph_algorithms/)**: Grid-based pathfinding problems
- **[DFS/BFS](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph traversal problems

## 📚 Learning Points

1. **Connected Components**: Essential for grid analysis problems
2. **Graph Traversal**: Important for component exploration
3. **Grid Representation**: Key technique for spatial problems
4. **DFS vs BFS**: Critical for algorithm choice
5. **Union-Find**: Foundation for connectivity problems

---

**This is a great introduction to connected components and grid traversal!** 🎯 