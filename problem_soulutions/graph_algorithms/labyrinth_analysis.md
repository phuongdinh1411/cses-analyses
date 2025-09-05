---
layout: simple
title: "Labyrinth - Minimum Walls Path Finding"
permalink: /problem_soulutions/graph_algorithms/labyrinth_analysis
---

# Labyrinth - Minimum Walls Path Finding

## 📋 Problem Description

You are given a map of a labyrinth, and your task is to count the number of walls between the upper-left and lower-right corner.

The labyrinth consists of n×m squares, and each square is either wall or floor. You can walk left, right, up, and down through the floor squares.

**Input**: 
- First line: Two integers n and m (height and width of the labyrinth)
- Next n lines: m characters each (". " denotes floor, "#" denotes wall)

**Output**: 
- One integer: minimum number of walls to pass through

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
2
```

**Explanation**: 
- Start at (0,0), end at (4,7)
- Optimal path: (0,0) → (1,1) → (1,2) → (1,3) → (1,4) → (1,5) → (1,6) → (1,7) → (2,7) → (3,7) → (4,7)
- Passes through 2 walls: at (2,7) and (4,7)

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find path with minimum walls between start and end
- **Key Insight**: Use BFS with modified queue to prioritize floors over walls
- **Challenge**: Handle grid navigation and wall counting efficiently

### Step 2: Brute Force Approach
**Try all possible paths and find minimum walls:**

```python
from collections import deque

def labyrinth_bfs(n, m, grid):
    def bfs():
        queue = deque([(0, 0, 0)])  # (row, col, walls)
        visited = [[False] * m for _ in range(n)]
        
        while queue:
            row, col, walls = queue.popleft()
            
            if row == n-1 and col == m-1:
                return walls
            
            if visited[row][col]:
                continue
            
            visited[row][col] = True
            
            # Explore all four directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    not visited[nr][nc]):
                    if grid[nr][nc] == '#':
                        queue.append((nr, nc, walls + 1))
                    else:
                        queue.appendleft((nr, nc, walls))  # Prioritize floors
        
        return -1  # No path found
    
    return bfs()
```

**Complexity**: O(n × m) - optimal for this problem

### Step 3: Optimization
**Use Dijkstra's algorithm with priority queue for better performance:**

```python
import heapq

def labyrinth_dijkstra(n, m, grid):
    def dijkstra():
        pq = [(0, 0, 0)]  # (walls, row, col)
        distances = [[float('inf')] * m for _ in range(n)]
        distances[0][0] = 0
        
        while pq:
            walls, row, col = heapq.heappop(pq)
            
            if row == n-1 and col == m-1:
                return walls
            
            if walls > distances[row][col]:
                continue
            
            # Explore all four directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m:
                    new_walls = walls + (1 if grid[nr][nc] == '#' else 0)
                    if new_walls < distances[nr][nc]:
                        distances[nr][nc] = new_walls
                        heapq.heappush(pq, (new_walls, nr, nc))
        
        return -1  # No path found
    
    return dijkstra()
```

**Why this improvement works**: Dijkstra's algorithm guarantees finding the shortest path with minimum wall count, though it's slightly more complex than BFS.

### Improvement 2: 0-1 BFS - O(n*m)
**Description**: Use 0-1 BFS which is more efficient than Dijkstra's for this problem.

```python
from collections import deque

def labyrinth_01_bfs(n, m, grid):
    def bfs_01():
        queue = deque([(0, 0, 0)])  # (row, col, walls)
        visited = [[False] * m for _ in range(n)]
        
        while queue:
            row, col, walls = queue.popleft()
            
            if row == n-1 and col == m-1:
                return walls
            
            if visited[row][col]:
                continue
            
            visited[row][col] = True
            
            # Explore all four directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    not visited[nr][nc]):
                    if grid[nr][nc] == '#':
                        queue.append((nr, nc, walls + 1))  # Add to end
                    else:
                        queue.appendleft((nr, nc, walls))  # Add to front
        
        return -1  # No path found
    
    return bfs_01()
```

**Why this improvement works**: 0-1 BFS is optimal for this problem since we have only two types of edges (0 and 1), making it more efficient than Dijkstra's.

### Alternative: A* Search - O(n*m * log(n*m))
**Description**: Use A* search with Manhattan distance heuristic for potentially faster search.

```python
import heapq

def labyrinth_astar(n, m, grid):
    def manhattan_distance(row, col):
        return abs(n-1 - row) + abs(m-1 - col)
    
    def astar():
        pq = [(manhattan_distance(0, 0), 0, 0, 0)]  # (f, walls, row, col)
        distances = [[float('inf')] * m for _ in range(n)]
        distances[0][0] = 0
        
        while pq:
            f, walls, row, col = heapq.heappop(pq)
            
            if row == n-1 and col == m-1:
                return walls
            
            if walls > distances[row][col]:
                continue
            
            # Explore all four directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m:
                    new_walls = walls + (1 if grid[nr][nc] == '#' else 0)
                    if new_walls < distances[nr][nc]:
                        distances[nr][nc] = new_walls
                        h = manhattan_distance(nr, nc)
                        heapq.heappush(pq, (new_walls + h, new_walls, nr, nc))
        
        return -1  # No path found
    
    return astar()
```

**Why this works**: A* search uses a heuristic to guide the search toward the goal, potentially reducing the number of nodes explored.

### Step 4: Complete Solution

```python
def solve_labyrinth():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    
    result = bfs_01(n, m, grid)
    print(result if result != -1 else "IMPOSSIBLE")

def bfs_01(n, m, grid):
    from collections import deque
    
    queue = deque([(0, 0, 0)])  # (row, col, walls)
    visited = [[False] * m for _ in range(n)]
    
    while queue:
        row, col, walls = queue.popleft()
        
        if row == n-1 and col == m-1:
            return walls
        
        if visited[row][col]:
            continue
        
        visited[row][col] = True
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                not visited[nr][nc]):
                if grid[nr][nc] == '#':
                    queue.append((nr, nc, walls + 1))  # Add to end
                else:
                    queue.appendleft((nr, nc, walls))  # Add to front
    
    return -1  # No path found

if __name__ == "__main__":
    solve_labyrinth()
```

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
        ]), 2),
        ((3, 3, [
            ".#.",
            "#.#",
            ".#."
        ]), 2),
        ((2, 2, [
            "..",
            ".."
        ]), 0),  # No walls
        ((2, 2, [
            "##",
            "##"
        ]), -1),  # Impossible
    ]
    
    for (n, m, grid), expected in test_cases:
        result = bfs_01(n, m, grid)
        print(f"n={n}, m={m}, grid:")
        for row in grid:
            print(f"  {row}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def bfs_01(n, m, grid):
    from collections import deque
    
    queue = deque([(0, 0, 0)])  # (row, col, walls)
    visited = [[False] * m for _ in range(n)]
    
    while queue:
        row, col, walls = queue.popleft()
        
        if row == n-1 and col == m-1:
            return walls
        
        if visited[row][col]:
            continue
        
        visited[row][col] = True
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                not visited[nr][nc]):
                if grid[nr][nc] == '#':
                    queue.append((nr, nc, walls + 1))  # Add to end
                else:
                    queue.appendleft((nr, nc, walls))  # Add to front
    
    return -1  # No path found

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n × m) - single pass through grid
- **Space**: O(n × m) - visited array and queue

### Why This Solution Works
- **0-1 BFS**: Optimal for problems with binary edge weights
- **Modified Queue**: Prioritizes floors over walls
- **Grid Navigation**: Efficient 4-directional movement
- **Optimal Algorithm**: Best known approach for this problem
## 🎯 Problem Variations

### Variation 1: Labyrinth with Diagonal Movement
**Problem**: Allow diagonal movement in addition to 4-directional movement.

```python
def labyrinth_diagonal(n, m, grid):
    """Find minimum walls with diagonal movement allowed"""
    from collections import deque
    
    queue = deque([(0, 0, 0)])  # (row, col, walls)
    visited = [[False] * m for _ in range(n)]
    
    # 8 directions: 4 cardinal + 4 diagonal
    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1),  # Cardinal
        (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
    ]
    
    while queue:
        row, col, walls = queue.popleft()
        
        if row == n-1 and col == m-1:
            return walls
        
        if visited[row][col]:
            continue
        
        visited[row][col] = True
        
        # Explore all eight directions
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                not visited[nr][nc]):
                if grid[nr][nc] == '#':
                    queue.append((nr, nc, walls + 1))
                else:
                    queue.appendleft((nr, nc, walls))
    
    return -1

# Example usage
grid = [
    ".#.",
    "#.#",
    ".#."
]
result = labyrinth_diagonal(3, 3, grid)
print(f"Diagonal movement result: {result}")
```

### Variation 2: Labyrinth with Multiple Goals
**Problem**: Find minimum walls to reach any of multiple goal positions.

```python
def labyrinth_multiple_goals(n, m, grid, goals):
    """Find minimum walls to reach any goal position"""
    from collections import deque
    
    queue = deque([(0, 0, 0)])  # (row, col, walls)
    visited = [[False] * m for _ in range(n)]
    
    while queue:
        row, col, walls = queue.popleft()
        
        # Check if current position is a goal
        if (row, col) in goals:
            return walls
        
        if visited[row][col]:
            continue
        
        visited[row][col] = True
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                not visited[nr][nc]):
                if grid[nr][nc] == '#':
                    queue.append((nr, nc, walls + 1))
                else:
                    queue.appendleft((nr, nc, walls))
    
    return -1

# Example usage
goals = [(1, 1), (3, 3), (4, 4)]
result = labyrinth_multiple_goals(5, 5, grid, goals)
print(f"Multiple goals result: {result}")
```

### Variation 3: Labyrinth with Weighted Walls
**Problem**: Different walls have different costs to pass through.

```python
def labyrinth_weighted_walls(n, m, grid, wall_costs):
    """Find minimum cost with weighted walls"""
    import heapq
    
    pq = [(0, 0, 0)]  # (cost, row, col)
    distances = [[float('inf')] * m for _ in range(n)]
    distances[0][0] = 0
    
    while pq:
        cost, row, col = heapq.heappop(pq)
        
        if row == n-1 and col == m-1:
            return cost
        
        if cost > distances[row][col]:
            continue
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m):
                if grid[nr][nc] == '#':
                    wall_cost = wall_costs.get((nr, nc), 1)
                    new_cost = cost + wall_cost
                else:
                    new_cost = cost
                
                if new_cost < distances[nr][nc]:
                    distances[nr][nc] = new_cost
                    heapq.heappush(pq, (new_cost, nr, nc))
    
    return distances[n-1][m-1] if distances[n-1][m-1] != float('inf') else -1

# Example usage
wall_costs = {(1, 1): 3, (2, 2): 5, (3, 3): 2}
result = labyrinth_weighted_walls(5, 5, grid, wall_costs)
print(f"Weighted walls result: {result}")
```

### Variation 4: Labyrinth with Time Constraints
**Problem**: Find path with minimum walls within a time limit.

```python
def labyrinth_time_constrained(n, m, grid, time_limit):
    """Find minimum walls within time constraint"""
    from collections import deque
    
    queue = deque([(0, 0, 0, 0)])  # (row, col, walls, time)
    visited = [[False] * m for _ in range(n)]
    
    while queue:
        row, col, walls, time = queue.popleft()
        
        if row == n-1 and col == m-1:
            return walls
        
        if time >= time_limit or visited[row][col]:
            continue
        
        visited[row][col] = True
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                not visited[nr][nc]):
                new_time = time + 1
                if grid[nr][nc] == '#':
                    queue.append((nr, nc, walls + 1, new_time))
                else:
                    queue.appendleft((nr, nc, walls, new_time))
    
    return -1

# Example usage
result = labyrinth_time_constrained(5, 5, grid, 10)
print(f"Time constrained result: {result}")
```

### Variation 5: Dynamic Labyrinth
**Problem**: Maintain minimum walls as the labyrinth changes dynamically.

```python
class DynamicLabyrinth:
    def __init__(self, n, m, initial_grid):
        self.n = n
        self.m = m
        self.grid = [list(row) for row in initial_grid]
        self.min_walls = None
    
    def update_cell(self, row, col, new_value):
        """Update a cell in the labyrinth"""
        if 0 <= row < self.n and 0 <= col < self.m:
            self.grid[row][col] = new_value
            self.min_walls = None  # Reset cached result
    
    def get_min_walls(self):
        """Get current minimum walls"""
        if self.min_walls is None:
            self.min_walls = self._calculate_min_walls()
        return self.min_walls
    
    def _calculate_min_walls(self):
        """Calculate minimum walls using 0-1 BFS"""
        from collections import deque
        
        queue = deque([(0, 0, 0)])
        visited = [[False] * self.m for _ in range(self.n)]
        
        while queue:
            row, col, walls = queue.popleft()
            
            if row == self.n-1 and col == self.m-1:
                return walls
            
            if visited[row][col]:
                continue
            
            visited[row][col] = True
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < self.n and 0 <= nc < self.m and 
                    not visited[nr][nc]):
                    if self.grid[nr][nc] == '#':
                        queue.append((nr, nc, walls + 1))
                    else:
                        queue.appendleft((nr, nc, walls))
        
        return -1
    
    def get_grid(self):
        """Get current grid state"""
        return [''.join(row) for row in self.grid]

# Example usage
initial_grid = [
    ".#.",
    "#.#",
    ".#."
]
labyrinth = DynamicLabyrinth(3, 3, initial_grid)
print(f"Initial min walls: {labyrinth.get_min_walls()}")

labyrinth.update_cell(1, 1, '.')
print(f"After updating (1,1) to floor: {labyrinth.get_min_walls()}")

labyrinth.update_cell(0, 1, '#')
print(f"After updating (0,1) to wall: {labyrinth.get_min_walls()}")
```
---

## 🔗 Related Problems

- **[Grid Navigation](/cses-analyses/problem_soulutions/graph_algorithms/)**: Grid-based pathfinding problems
- **[Shortest Path](/cses-analyses/problem_soulutions/graph_algorithms/)**: Path optimization problems
- **[BFS/DFS](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph traversal problems

## 📚 Learning Points

1. **0-1 BFS**: Essential for problems with binary edge weights
2. **Grid Navigation**: Important for 2D grid problems
3. **Modified Queue**: Key technique for prioritizing certain paths
4. **Path Optimization**: Critical for finding optimal routes
5. **Graph Representation**: Foundation for efficient algorithm implementation

---

**This is a great introduction to grid-based pathfinding and 0-1 BFS!** 🎯

## 🎨 Visual Example

### Input Example
```
5×8 labyrinth:
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
Start: (0,0), End: (4,7)
```

### 0-1 BFS Process
```
Step 1: Start from (0,0)
- Deque: [(0,0,0)] (row, col, walls)
- Visited: {(0,0)}
- Distance: 0

Step 2: Process (0,0)
- Explore neighbors: (0,1), (1,0)
- (0,1): Wall, add to back of deque: [(0,1,1)]
- (1,0): Wall, add to back of deque: [(0,1,1), (1,0,1)]
- Deque: [(0,1,1), (1,0,1)]

Step 3: Process (0,1) - Wall
- Explore neighbors: (0,0), (0,2), (1,1)
- (0,0): Already visited
- (0,2): Wall, add to back: [(1,0,1), (0,2,2)]
- (1,1): Floor, add to front: [(1,1,1), (1,0,1), (0,2,2)]
- Deque: [(1,1,1), (1,0,1), (0,2,2)]

Step 4: Process (1,1) - Floor
- Explore neighbors: (1,0), (1,2), (0,1), (2,1)
- (1,0): Wall, add to back: [(1,0,1), (0,2,2), (1,0,2)]
- (1,2): Floor, add to front: [(1,2,1), (1,0,1), (0,2,2), (1,0,2)]
- (0,1): Already visited
- (2,1): Wall, add to back: [(1,0,1), (0,2,2), (1,0,2), (2,1,2)]
- Deque: [(1,2,1), (1,0,1), (0,2,2), (1,0,2), (2,1,2)]

Continue until reaching (4,7)...
```

### Optimal Path Visualization
```
########
#S..#...#
####.#.#
#..#...E#
########

Path: S(0,0) → (1,1) → (1,2) → (1,3) → (1,4) → (1,5) → (1,6) → (1,7) → (2,7) → (3,7) → E(4,7)

Walls passed through: 2
- Wall at (2,7)
- Wall at (4,7)
```

### 0-1 BFS vs Dijkstra Comparison
```
0-1 BFS (Deque):
- Weight 0: Add to front of deque
- Weight 1: Add to back of deque
- Time: O(n×m)
- Space: O(n×m)

Dijkstra (Priority Queue):
- All weights: Add to priority queue
- Time: O(n×m log(n×m))
- Space: O(n×m)
```

### Distance Array Visualization
```
Distance array (5×8):
Row 0: [0,1,2,3,4,5,6,7]
Row 1: [1,1,1,1,1,1,1,2]
Row 2: [2,2,2,2,2,2,2,2]
Row 3: [3,3,3,3,3,3,3,2]
Row 4: [4,4,4,4,4,4,4,2]

Minimum walls to reach (4,7): 2
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ 0-1 BFS         │ O(n×m)       │ O(n×m)       │ Deque with   │
│                 │              │              │ front/back   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dijkstra        │ O(n×m log(n×m))│ O(n×m)     │ Priority     │
│                 │              │              │ queue        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ BFS with Walls  │ O(n×m)       │ O(n×m)       │ Modified     │
│                 │              │              │ BFS          │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## Key Insights for Other Problems

### 1. **Shortest Path with Weighted Edges**
**Principle**: Use appropriate shortest path algorithms based on edge weights and problem constraints.
**Applicable to**:
- Shortest path problems
- Weighted graphs
- Grid problems
- Path finding

**Example Problems**:
- Shortest path
- Weighted graphs
- Grid problems
- Path finding

### 2. **0-1 BFS for Binary Weights**
**Principle**: Use 0-1 BFS when edges have only two possible weights (0 and 1).
**Applicable to**:
- Binary weight graphs
- Shortest path problems
- Grid problems
- Algorithm optimization

**Example Problems**:
- Binary weight graphs
- Shortest path problems
- Grid problems
- Algorithm optimization

### 3. **Priority Queue vs Deque**
**Principle**: Choose between priority queue and deque based on edge weight characteristics.
**Applicable to**:
- Graph algorithms
- Shortest path
- Algorithm design
- Performance optimization

**Example Problems**:
- Graph algorithms
- Shortest path
- Algorithm design
- Performance optimization

### 4. **Heuristic Search**
**Principle**: Use heuristic functions to guide search algorithms toward the goal.
**Applicable to**:
- Search algorithms
- Path finding
- Optimization problems
- Algorithm design

**Example Problems**:
- Search algorithms
- Path finding
- Optimization problems
- Algorithm design

## Notable Techniques

### 1. **0-1 BFS Pattern**
```python
from collections import deque
def bfs_01():
    queue = deque([(start, 0)])
    while queue:
        node, cost = queue.popleft()
        for neighbor in graph[node]:
            new_cost = cost + weight
            if weight == 0:
                queue.appendleft((neighbor, new_cost))
            else:
                queue.append((neighbor, new_cost))
```

### 2. **Dijkstra's Pattern**
```python
import heapq
def dijkstra():
    pq = [(0, start)]
    distances = [float('inf')] * n
    while pq:
        dist, node = heapq.heappop(pq)
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
```

### 3. **Grid Path Finding Pattern**
```python
# Define directions
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for dr, dc in directions:
    nr, nc = row + dr, col + dc
    if valid_cell(nr, nc):
        # Process neighbor
```

## Edge Cases to Remember

1. **No path exists**: Return -1 or "IMPOSSIBLE"
2. **Start/end is wall**: Handle properly
3. **Single cell grid**: Handle edge case
4. **Large grid**: Use efficient algorithm
5. **Boundary conditions**: Check grid boundaries

## Problem-Solving Framework

1. **Identify path finding nature**: This is a shortest path problem with weighted edges
2. **Choose algorithm**: Use 0-1 BFS for binary weights
3. **Handle edge weights**: Walls have weight 1, floors have weight 0
4. **Use appropriate data structure**: Deque for 0-1 BFS
5. **Check path existence**: Handle case where no path exists

---

*This analysis shows how to efficiently solve shortest path problems in grids with weighted edges using appropriate graph algorithms.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Labyrinth with Costs**
**Variation**: Each wall has a different cost to break through.
**Approach**: Use Dijkstra's algorithm with cost tracking.
```python
def cost_based_labyrinth(n, m, grid, costs):
    # costs[i][j] = cost to break wall at position (i, j)
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    dist = [[float('inf')] * m for _ in range(n)]
    dist[0][0] = 0
    
    pq = [(0, 0, 0)]  # (cost, row, col)
    
    while pq:
        cost, row, col = heapq.heappop(pq)
        
        if row == n-1 and col == m-1:
            return cost
        
        if cost > dist[row][col]:
            continue
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < m:
                wall_cost = costs[nr][nc] if grid[nr][nc] == '#' else 0
                new_cost = cost + wall_cost
                
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(pq, (new_cost, nr, nc))
    
    return -1
```

#### 2. **Labyrinth with Constraints**
**Variation**: Limited number of walls can be broken.
**Approach**: Use BFS with state tracking.
```python
def constrained_labyrinth(n, m, grid, max_walls):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited = set()
    queue = deque([(0, 0, 0, 0)])  # (row, col, walls_broken, steps)
    
    while queue:
        row, col, walls, steps = queue.popleft()
        
        if row == n-1 and col == m-1:
            return steps
        
        state = (row, col, walls)
        if state in visited:
            continue
        visited.add(state)
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < m:
                if grid[nr][nc] == '.':
                    queue.append((nr, nc, walls, steps + 1))
                elif grid[nr][nc] == '#' and walls < max_walls:
                    queue.append((nr, nc, walls + 1, steps + 1))
    
    return -1
```

#### 3. **Labyrinth with Probabilities**
**Variation**: Each wall has a probability of being breakable.
**Approach**: Use Monte Carlo simulation or expected value calculation.
```python
def probabilistic_labyrinth(n, m, grid, probabilities):
    # probabilities[i][j] = probability wall at (i,j) can be broken
    
    def monte_carlo_simulation(trials=1000):
        successful_paths = 0
        
        for _ in range(trials):
            if can_reach_end_with_probabilities(n, m, grid, probabilities):
                successful_paths += 1
        
        return successful_paths / trials
    
    def can_reach_end_with_probabilities(n, m, grid, probs):
        # Simplified simulation - in practice would use more sophisticated approach
        visited = [[False] * m for _ in range(n)]
        return dfs_with_probabilities(0, 0, n, m, grid, probs, visited)
    
    return monte_carlo_simulation()
```

#### 4. **Labyrinth with Multiple Exits**
**Variation**: Multiple possible exit points with different values.
**Approach**: Find shortest path to each exit and choose best.
```python
def multiple_exits_labyrinth(n, m, grid, exits):
    # exits = [(row, col, value), ...]
    
    def find_shortest_to_exit(start_row, start_col, exit_row, exit_col):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        visited = [[False] * m for _ in range(n)]
        queue = deque([(start_row, start_col, 0)])
        
        while queue:
            row, col, steps = queue.popleft()
            
            if row == exit_row and col == exit_col:
                return steps
            
            if visited[row][col]:
                continue
            visited[row][col] = True
            
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == '.':
                    queue.append((nr, nc, steps + 1))
        
        return float('inf')
    
    best_value = 0
    for exit_row, exit_col, value in exits:
        steps = find_shortest_to_exit(0, 0, exit_row, exit_col)
        if steps != float('inf'):
            best_value = max(best_value, value - steps)
    
    return best_value
```

#### 5. **Labyrinth with Dynamic Walls**
**Variation**: Walls can appear/disappear based on time or conditions.
**Approach**: Use time-based state tracking or dynamic programming.
```python
def dynamic_walls_labyrinth(n, m, grid, wall_schedule):
    # wall_schedule[(row, col)] = [(start_time, end_time), ...]
    
    def is_wall_at_time(row, col, time):
        if grid[row][col] == '#':
            return True
        if (row, col) in wall_schedule:
            for start, end in wall_schedule[(row, col)]:
                if start <= time <= end:
                    return True
        return False
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited = set()
    queue = deque([(0, 0, 0)])  # (row, col, time)
    
    while queue:
        row, col, time = queue.popleft()
        
        if row == n-1 and col == m-1:
            return time
        
        state = (row, col, time)
        if state in visited:
            continue
        visited.add(state)
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < m:
                if not is_wall_at_time(nr, nc, time + 1):
                    queue.append((nr, nc, time + 1))
    
    return -1
```

### Related Problems & Concepts

#### 1. **Path Finding Problems**
- **Shortest Path**: Dijkstra's, Bellman-Ford, Floyd-Warshall
- **Grid Path Finding**: BFS, DFS, A* search
- **Maze Problems**: Wall following, flood fill
- **Navigation**: GPS routing, robot navigation

#### 2. **Graph Theory**
- **Connectivity**: Strongly connected components
- **Flow Networks**: Maximum flow, minimum cut
- **Matching**: Bipartite matching, stable marriage
- **Coloring**: Graph coloring, bipartite graphs

#### 3. **Dynamic Programming**
- **Grid DP**: Path counting, minimum cost paths
- **State Compression**: Bit manipulation for states
- **Memoization**: Caching recursive solutions
- **Optimal Substructure**: Breaking down problems

#### 4. **Search Algorithms**
- **Breadth-First Search**: Level-by-level exploration
- **Depth-First Search**: Recursive exploration
- **A* Search**: Heuristic-guided search
- **Iterative Deepening**: Memory-efficient search

#### 5. **Optimization Problems**
- **Shortest Path**: Minimum distance/cost
- **Resource Allocation**: Limited resources
- **Scheduling**: Time-based constraints
- **Network Flow**: Maximum throughput

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict time constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large datasets
- **Edge Cases**: Robust error handling

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient array processing
- **Sliding Window**: Optimal subarray problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Combinatorics**
- **Path Counting**: Number of valid paths
- **Permutations**: Order of moves
- **Combinations**: Choice of walls to break
- **Catalan Numbers**: Valid path sequences

#### 2. **Probability Theory**
- **Expected Values**: Average path length
- **Markov Chains**: State transitions
- **Random Walks**: Stochastic processes
- **Monte Carlo**: Simulation methods

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime numbers

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Grid and graph problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Grid Problems**: Maze navigation, path finding
- **Graph Problems**: Shortest path, connectivity
- **Dynamic Programming**: State optimization
- **Search Problems**: BFS, DFS, A* search 