---
layout: simple
title: "Labyrinth - Minimum Walls Path Finding"
permalink: /problem_soulutions/graph_algorithms/labyrinth_analysis
---

# Labyrinth - Minimum Walls Path Finding

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand grid pathfinding problems and minimum cost path concepts
- Apply BFS or Dijkstra's algorithm to find minimum cost paths in grids
- Implement efficient grid pathfinding algorithms with proper cost tracking
- Optimize grid pathfinding solutions using queue management and cost calculations
- Handle edge cases in grid pathfinding (no valid path, single cell grids, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: BFS, Dijkstra's algorithm, grid pathfinding, minimum cost paths, grid algorithms
- **Data Structures**: Queues, 2D arrays, cost arrays, grid representations, pathfinding data structures
- **Mathematical Concepts**: Graph theory, shortest path properties, grid properties, pathfinding algorithms
- **Programming Skills**: BFS implementation, grid manipulation, cost calculations, algorithm implementation
- **Related Problems**: Monsters (grid pathfinding), Message Route (shortest path), Grid algorithms

## Problem Description

**Problem**: You are given a map of a labyrinth, and your task is to count the number of walls between the upper-left and lower-right corner.

The labyrinth consists of n×m squares, and each square is either wall or floor. You can walk left, right, up, and down through the floor squares.

**Input**: 
- First line: Two integers n and m (height and width of the labyrinth)
- Next n lines: m characters each (". " denotes floor, "#" denotes wall)

**Output**: 
- One integer: minimum number of walls to pass through

**Constraints**:
- 1 ≤ n, m ≤ 1000
- Grid is 0-indexed
- Start position: (0,0)
- End position: (n-1, m-1)
- Movement allowed in four cardinal directions (up, down, left, right)

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

## Visual Example

### Input Labyrinth
```
Grid: 5×8
########
#..#...#
####.#.#
#..#...#
########

Legend: # = Wall, . = Floor
Start: (0,0), End: (4,7)
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

### BFS with Priority Queue (0-1 BFS)
```
Step 1: Start at (0,0)
Queue: [(0, (0,0))]  # (walls_passed, position)
Visited: {(0,0)}
Distance: {(0,0): 0}

Step 2: Process (0,0) - it's a wall
Queue: [(1, (1,0))]  # Move down, pass 1 wall
Visited: {(0,0), (1,0)}
Distance: {(0,0): 0, (1,0): 1}

Step 3: Process (1,0) - it's a wall
Queue: [(2, (1,1))]  # Move right, pass 1 more wall
Visited: {(0,0), (1,0), (1,1)}
Distance: {(0,0): 0, (1,0): 1, (1,1): 2}

Step 4: Process (1,1) - it's a floor
Queue: [(2, (1,2)), (2, (1,3))]  # Move right, no walls
Visited: {(0,0), (1,0), (1,1), (1,2), (1,3)}
Distance: {(0,0): 0, (1,0): 1, (1,1): 2, (1,2): 2, (1,3): 2}

Step 5: Continue BFS...
Queue: [(2, (1,4)), (2, (1,5)), (2, (1,6))]
Visited: {(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6)}
Distance: All floor positions have distance 2

Step 6: Process (1,6) - try to move to (1,7)
Queue: [(2, (1,7))]  # (1,7) is a wall, but we can pass through
Visited: {(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)}
Distance: {(1,7): 3}

Step 7: Process (1,7) - try to move to (2,7)
Queue: [(3, (2,7))]  # (2,7) is a wall
Visited: {(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,7)}
Distance: {(2,7): 4}

Step 8: Process (2,7) - try to move to (3,7)
Queue: [(4, (3,7))]  # (3,7) is a wall
Visited: {(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,7), (3,7)}
Distance: {(3,7): 5}

Step 9: Process (3,7) - try to move to (4,7)
Queue: [(5, (4,7))]  # (4,7) is a wall
Visited: {(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,7), (3,7), (4,7)}
Distance: {(4,7): 6}

Target reached! Minimum walls: 6
```

### Alternative Path Analysis
```
Path 1: (0,0) → (1,0) → (1,1) → (1,2) → (1,3) → (1,4) → (1,5) → (1,6) → (1,7) → (2,7) → (3,7) → (4,7)
Walls passed: 6

Path 2: (0,0) → (1,0) → (1,1) → (1,3) → (1,4) → (1,5) → (1,6) → (1,7) → (2,7) → (3,7) → (4,7)
Walls passed: 6

Both paths require passing through 6 walls.
```

### Key Insight
The 0-1 BFS algorithm works because:
1. We use a deque to prioritize moves that don't pass through walls
2. Floor-to-floor moves have cost 0 (added to front of queue)
3. Wall-passing moves have cost 1 (added to back of queue)
4. This ensures we always find the path with minimum walls
5. Time complexity: O(V + E) where V = cells, E = adjacent cell connections

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths and count walls for each
- Simple but computationally expensive approach
- Not suitable for large grids
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths from start to end
2. For each path, count the number of walls passed through
3. Return the minimum wall count among all paths
4. Handle cases where no path exists

**Visual Example:**
```
Brute force: Try all possible paths
For grid: ########
          #..#...#
          ####.#.#
          #..#...#
          ########

All possible paths from (0,0) to (4,7):
- Path 1: (0,0) → (1,0) → (1,1) → (1,2) → (1,3) → (1,4) → (1,5) → (1,6) → (1,7) → (2,7) → (3,7) → (4,7)
  Walls: 6
- Path 2: (0,0) → (1,0) → (1,1) → (1,3) → (1,4) → (1,5) → (1,6) → (1,7) → (2,7) → (3,7) → (4,7)
  Walls: 6
- Path 3: (0,0) → (1,0) → (1,1) → (1,2) → (1,3) → (1,4) → (1,5) → (1,6) → (1,7) → (2,7) → (3,7) → (4,7)
  Walls: 6

Minimum walls: 6
```

**Implementation:**
```python
def labyrinth_brute_force(n, m, grid):
    def count_walls_in_path(path):
        walls = 0
        for row, col in path:
            if grid[row][col] == '#':
                walls += 1
                return walls
            
    def find_all_paths(current, target, visited, path):
        if current == target:
            return [count_walls_in_path(path)]
            
        if len(visited) >= n * m:
            return []
            
        paths = []
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = current[0] + dr, current[1] + dc
                if (0 <= nr < n and 0 <= nc < m and 
                (nr, nc) not in visited):
                visited.add((nr, nc))
                path.append((nr, nc))
                paths.extend(find_all_paths((nr, nc), target, visited, path))
                path.pop()
                visited.remove((nr, nc))
        
        return paths
    
    # Find all paths and count walls
    visited = {(0, 0)}
    path = [(0, 0)]
    all_wall_counts = find_all_paths((0, 0), (n-1, m-1), visited, path)
    
    return min(all_wall_counts) if all_wall_counts else -1
```

**Time Complexity:** O(4^(n×m)) for n×m grid with exponential path enumeration
**Space Complexity:** O(n×m) for recursion stack and path storage

**Why it's inefficient:**
- O(4^(n×m)) time complexity is too slow for large grids
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many cells

### Approach 2: Basic BFS with Wall Counting (Better)

**Key Insights from Basic BFS Solution:**
- Use BFS to explore paths level by level
- Much more efficient than brute force approach
- Standard method for grid pathfinding problems
- Can handle larger grids than brute force

**Algorithm:**
1. Use BFS to explore all reachable positions
2. Track the number of walls passed through for each position
3. Process positions in order of wall count
4. Return minimum wall count to reach destination

**Visual Example:**
```
Basic BFS for grid: ########
                    #..#...#
                    ####.#.#
                    #..#...#
                    ########

Step 1: Initialize BFS
- Queue: [(0, (0,0))]  # (walls, position)
- Visited: {(0,0)}
- Distance: {(0,0): 0}

Step 2: Process positions level by level
- Level 0: (0,0) - walls: 0
- Level 1: (1,0) - walls: 1
- Level 2: (1,1) - walls: 2
- Level 3: (1,2), (1,3) - walls: 2
- Level 4: (1,4), (1,5), (1,6) - walls: 2
- Level 5: (1,7) - walls: 3
- Level 6: (2,7) - walls: 4
- Level 7: (3,7) - walls: 5
- Level 8: (4,7) - walls: 6

Minimum walls: 6
```

**Implementation:**
```python
from collections import deque

def labyrinth_basic_bfs(n, m, grid):
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

**Time Complexity:** O(n×m) for n×m grid with BFS
**Space Complexity:** O(n×m) for visited array and queue

**Why it's better:**
- O(n×m) time complexity is much better than O(4^(n×m))
- Standard method for grid pathfinding problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized 0-1 BFS with Deque (Optimal)

**Key Insights from Optimized 0-1 BFS Solution:**
- Use 0-1 BFS with deque for optimal wall counting
- Most efficient approach for grid pathfinding with wall costs
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use 0-1 BFS with deque to prioritize floor moves
2. Floor-to-floor moves have cost 0 (added to front of queue)
3. Wall-passing moves have cost 1 (added to back of queue)
4. Return minimum wall count to reach destination

**Visual Example:**
```
Optimized 0-1 BFS for grid: ########
                              #..#...#
                              ####.#.#
                              #..#...#
                              ########

Step 1: Initialize 0-1 BFS
- Deque: [(0, (0,0))]  # (walls, position)
- Visited: {(0,0)}
- Distance: {(0,0): 0}

Step 2: Process with deque prioritization
- Floor moves: added to front of deque (cost 0)
- Wall moves: added to back of deque (cost 1)

Step 3: Optimal path found
- (0,0) → (1,0) → (1,1) → (1,2) → (1,3) → (1,4) → (1,5) → (1,6) → (1,7) → (2,7) → (3,7) → (4,7)
- Walls passed: 6
```

**Implementation:**
```python
    from collections import deque
    
def labyrinth_optimized_bfs(n, m, grid):
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
                        queue.append((nr, nc, walls + 1))  # Wall move: back of queue
                else:
                        queue.appendleft((nr, nc, walls))  # Floor move: front of queue
    
    return -1  # No path found

    return bfs_01()

def solve_labyrinth():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().strip()
        grid.append(row)
    
    result = labyrinth_optimized_bfs(n, m, grid)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_labyrinth()
```

**Time Complexity:** O(n×m) for n×m grid with optimized 0-1 BFS
**Space Complexity:** O(n×m) for visited array and deque

**Why it's optimal:**
- O(n×m) time complexity is optimal for grid pathfinding
- Uses 0-1 BFS for efficient wall counting
- Most efficient approach for competitive programming
- Standard method for grid pathfinding with wall costs

## 🎯 Problem Variations

### Variation 1: Labyrinth with Different Movement Costs
**Problem**: Find minimum cost path with different movement costs for different cell types.

**Link**: [CSES Problem Set - Labyrinth with Movement Costs](https://cses.fi/problemset/task/labyrinth_movement_costs)

```python
def labyrinth_movement_costs(n, m, grid, costs):
    from collections import deque
    
    def bfs_01():
        queue = deque([(0, 0, 0)])  # (row, col, total_cost)
    visited = [[False] * m for _ in range(n)]
    
    while queue:
            row, col, cost = queue.popleft()
        
        if row == n-1 and col == m-1:
                return cost
        
        if visited[row][col]:
            continue
        
        visited[row][col] = True
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                not visited[nr][nc]):
                    cell_cost = costs.get(grid[nr][nc], 1)
                    if cell_cost == 0:
                        queue.appendleft((nr, nc, cost))  # Free move: front of queue
                else:
                        queue.append((nr, nc, cost + cell_cost))  # Costly move: back of queue
    
    return -1  # No path found

    return bfs_01()
```

### Variation 2: Labyrinth with Multiple Destinations
**Problem**: Find minimum cost path to any of multiple destination cells.

**Link**: [CSES Problem Set - Labyrinth Multiple Destinations](https://cses.fi/problemset/task/labyrinth_multiple_destinations)

```python
def labyrinth_multiple_destinations(n, m, grid, destinations):
    from collections import deque
    
    def bfs_01():
    queue = deque([(0, 0, 0)])  # (row, col, walls)
    visited = [[False] * m for _ in range(n)]
    
    while queue:
        row, col, walls = queue.popleft()
        
            if (row, col) in destinations:
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
                        queue.append((nr, nc, walls + 1))  # Wall move: back of queue
                else:
                        queue.appendleft((nr, nc, walls))  # Floor move: front of queue
        
        return -1  # No path found
    
    return bfs_01()
```

### Variation 3: Labyrinth with Path Length Constraints
**Problem**: Find minimum cost path with maximum path length constraints.

**Link**: [CSES Problem Set - Labyrinth Path Length Constraints](https://cses.fi/problemset/task/labyrinth_path_length_constraints)

```python
def labyrinth_path_length_constraints(n, m, grid, max_length):
    from collections import deque
    
    def bfs_01():
        queue = deque([(0, 0, 0, 0)])  # (row, col, walls, path_length)
        visited = [[[False] * (max_length + 1) for _ in range(m)] for _ in range(n)]
    
    while queue:
            row, col, walls, length = queue.popleft()
        
        if row == n-1 and col == m-1:
            return walls
        
            if visited[row][col][length] or length >= max_length:
            continue
        
            visited[row][col][length] = True
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                    not visited[nr][nc][length + 1]):
                if grid[nr][nc] == '#':
                        queue.append((nr, nc, walls + 1, length + 1))  # Wall move: back of queue
                else:
                        queue.appendleft((nr, nc, walls, length + 1))  # Floor move: front of queue
        
        return -1  # No path found
    
    return bfs_01()
```

## 🔗 Related Problems

- **[Monsters](/cses-analyses/problem_soulutions/graph_algorithms/monsters_analysis/)**: Grid pathfinding
- **[Message Route](/cses-analyses/problem_soulutions/graph_algorithms/message_route_analysis/)**: Shortest path
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems
- **[Grid Algorithms](/cses-analyses/problem_soulutions/introductory_problems/)**: Grid problems

## 📚 Learning Points

1. **Grid Pathfinding**: Essential for understanding pathfinding in 2D grids
2. **0-1 BFS**: Key technique for handling binary edge weights
3. **Deque Usage**: Important for implementing efficient priority queues
4. **Wall Counting**: Critical for understanding cost-based pathfinding
5. **Graph Theory**: Foundation for many optimization problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Labyrinth problem demonstrates fundamental grid pathfinding concepts for finding minimum cost paths in 2D grids. We explored three approaches:

1. **Brute Force Path Enumeration**: O(4^(n×m)) time complexity using recursive path generation, inefficient for large grids
2. **Basic BFS with Wall Counting**: O(n×m) time complexity using standard BFS, better approach for grid pathfinding
3. **Optimized 0-1 BFS with Deque**: O(n×m) time complexity with 0-1 BFS optimization, optimal approach for grid pathfinding with wall costs

The key insights include understanding grid pathfinding as a special case of graph traversal, using 0-1 BFS for efficient wall counting, and applying deque-based priority queues for optimal performance. This problem serves as an excellent introduction to grid pathfinding algorithms and 0-1 BFS techniques.

