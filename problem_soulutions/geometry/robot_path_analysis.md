---
layout: simple
title: "Robot Path Analysis"
permalink: /problem_soulutions/geometry/robot_path_analysis
---


# Robot Path Analysis

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand pathfinding problems and obstacle avoidance in geometric environments
- Apply pathfinding algorithms like A* or Dijkstra's algorithm for obstacle avoidance
- Implement efficient pathfinding algorithms with obstacle detection and avoidance
- Optimize pathfinding using geometric properties and coordinate transformations
- Handle edge cases in pathfinding (no valid path, obstacles blocking all routes, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Pathfinding algorithms, A* algorithm, Dijkstra's algorithm, obstacle avoidance, geometric algorithms
- **Data Structures**: Priority queues, grids, obstacle maps, path data structures, geometric data structures
- **Mathematical Concepts**: Distance calculations, path optimization, coordinate geometry, geometric pathfinding
- **Programming Skills**: Pathfinding implementation, obstacle detection, coordinate manipulation, geometric computations
- **Related Problems**: Labyrinth (pathfinding), Message Route (shortest path), Grid Paths (path counting), Geometric algorithms

## Problem Description

**Problem**: Given a robot starting at position (0,0) and a set of obstacles, find the shortest path to reach a target position while avoiding obstacles.

**Input**: 
- n: number of obstacles
- obstacles: list of (x, y) coordinates representing obstacles
- target: (x, y) coordinates of target position

**Output**: Length of shortest path from (0,0) to target, or -1 if impossible.

**Constraints**:
- 1 ≤ n ≤ 1000
- -1000 ≤ x, y ≤ 1000 for all coordinates
- Robot can only move in 4 directions: up, down, left, right
- Robot cannot move through obstacles
- Robot cannot move outside the coordinate bounds

**Example**:
```
Input:
n = 3
obstacles = [(1, 1), (2, 2), (3, 1)]
target = (4, 4)

Output:
8

Explanation: 
Shortest path: (0,0) → (0,1) → (0,2) → (0,3) → (0,4) → (1,4) → (2,4) → (3,4) → (4,4)
Length = 8 units
```

## Visual Example

### Grid Visualization
```
Y
4 | . . . . T
3 | . . . . .
2 | . O . . .
1 | . O . O .
0 | S . . . .
  +---+---+---+---+---+
    0   1   2   3   4  X

S = Start (0,0)
T = Target (4,4)
O = Obstacle
. = Free space
```

### Shortest Path
```
Y
4 | . . . . T
3 | . . . . .
2 | . O . . .
1 | . O . O .
0 | S . . . .
  +---+---+---+---+---+
    0   1   2   3   4  X

Shortest path: (0,0) → (0,1) → (0,2) → (0,3) → (0,4) → (1,4) → (2,4) → (3,4) → (4,4)
Length: 8 units
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Recursive Brute Force Solution:**
- Try all possible paths from start to target
- Use recursion to explore all directions
- Check for obstacles and boundaries at each step
- Return minimum path length among all valid paths

**Algorithm:**
1. Start from current position
2. If current position is target, return 0
3. If current position is obstacle or out of bounds, return infinity
4. Recursively try all 4 directions
5. Return 1 + minimum of all valid recursive calls

**Visual Example:**
```
Y
4 | . . . . T
3 | . . . . .
2 | . O . . .
1 | . O . O .
0 | S . . . .
  +---+---+---+---+---+
    0   1   2   3   4  X

Recursive exploration from (0,0):
- Try (0,1): valid, recurse
- Try (1,0): valid, recurse
- Try (0,-1): invalid (out of bounds)
- Try (-1,0): invalid (out of bounds)
```

**Implementation:**
```python
def robot_path_recursive(obstacles, target, current=(0, 0), visited=None):
    if visited is None:
        visited = set()
    
    x, y = current
    
    # Base cases
    if current == target:
        return 0
    
    if current in obstacles or current in visited:
        return float('inf')
    
    if x < 0 or y < 0 or x > 1000 or y > 1000:
        return float('inf')
    
    # Mark current position as visited
    visited.add(current)
    
    # Try all 4 directions
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    min_path = float('inf')
    
    for dx, dy in directions:
        next_pos = (x + dx, y + dy)
        if next_pos not in visited:
            path_length = robot_path_recursive(obstacles, target, next_pos, visited.copy())
            min_path = min(min_path, path_length)
    
    return 1 + min_path if min_path != float('inf') else float('inf')
```

**Time Complexity:** O(4^n) where n is the maximum distance to target
**Space Complexity:** O(n) for recursion stack

**Why it's inefficient:**
- Exponential time complexity due to exploring all possible paths
- Redundant calculations for the same positions
- No memoization to avoid repeated work

### Approach 2: Breadth-First Search (Better)

**Key Insights from BFS Solution:**
- BFS guarantees shortest path in unweighted graphs
- Use queue to explore positions level by level
- Mark visited positions to avoid cycles
- Stop as soon as target is reached

**Algorithm:**
1. Initialize queue with start position and distance 0
2. While queue is not empty:
   - Dequeue current position and distance
   - If current position is target, return distance
   - Mark current position as visited
   - Add all valid neighbors to queue with distance + 1
3. Return -1 if target is unreachable

**Visual Example:**
```
Y
4 | . . . . T
3 | . . . . .
2 | . O . . .
1 | . O . O .
0 | S . . . .
  +---+---+---+---+---+
    0   1   2   3   4  X

BFS Level 0: (0,0) - distance 0
BFS Level 1: (0,1), (1,0) - distance 1
BFS Level 2: (0,2), (1,1), (2,0) - distance 2
BFS Level 3: (0,3), (2,1), (3,0) - distance 3
...
```

**Implementation:**
```python
def robot_path_bfs(obstacles, target):
    from collections import deque
    
    # Convert obstacles to set for O(1) lookup
    obstacle_set = set(obstacles)
    
    # BFS queue: (x, y, distance)
    queue = deque([(0, 0, 0)])
    visited = set()
    
    # 4 directions: up, right, down, left
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        x, y, dist = queue.popleft()
        
        if (x, y) == target:
            return dist
        
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        
        # Try all 4 directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (nx, ny) not in obstacle_set and (nx, ny) not in visited:
                queue.append((nx, ny, dist + 1))
    
    return -1  # Target unreachable
```

**Time Complexity:** O(area) where area is the maximum reachable area
**Space Complexity:** O(area) for queue and visited set

**Why it's better:**
- Guarantees shortest path
- Polynomial time complexity
- Efficient obstacle avoidance
- Clear and implementable

### Approach 3: A* Search (Optimal)

**Key Insights from A* Search Solution:**
- Use heuristic function to guide search towards target
- Combine actual distance (g) with estimated distance (h)
- Use priority queue to always expand most promising nodes
- Manhattan distance provides good heuristic for grid problems

**Algorithm:**
1. Initialize priority queue with start position, g=0, f=heuristic
2. While queue is not empty:
   - Pop node with lowest f-score
   - If current position is target, return g-score
   - Mark current position as visited
   - For each neighbor:
     - Calculate new g-score (current g + 1)
     - Calculate h-score (Manhattan distance to target)
     - Calculate f-score (g + h)
     - Add to queue if not visited and not obstacle
3. Return -1 if target is unreachable

**Visual Example:**
```
Y
4 | . . . . T
3 | . . . . .
2 | . O . . .
1 | . O . O .
0 | S . . . .
  +---+---+---+---+---+
    0   1   2   3   4  X

A* Search with Manhattan distance heuristic:
- From (0,0): h = |0-4| + |0-4| = 8, f = 0 + 8 = 8
- From (0,1): h = |0-4| + |1-4| = 7, f = 1 + 7 = 8
- From (1,0): h = |1-4| + |0-4| = 7, f = 1 + 7 = 8
```

**Implementation:**
```python
def robot_path_astar(obstacles, target):
    import heapq
    
    obstacle_set = set(obstacles)
    
    # Priority queue: (f_score, g_score, x, y)
    # f_score = g_score + heuristic
    queue = [(0, 0, 0, 0)]
    visited = set()
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        f_score, g_score, x, y = heapq.heappop(queue)
        
        if (x, y) == target:
            return g_score
        
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (nx, ny) not in obstacle_set and (nx, ny) not in visited:
                new_g = g_score + 1
                h = abs(nx - target[0]) + abs(ny - target[1])  # Manhattan distance
                f = new_g + h
                heapq.heappush(queue, (f, new_g, nx, ny))
    
    return -1
```

**Time Complexity:** O(area log area) in worst case, but much better in practice
**Space Complexity:** O(area) for priority queue and visited set

**Why it's optimal:**
- Finds shortest path with fewer node expansions than BFS
- Heuristic guides search towards target
- More efficient for large search spaces
- Industry standard for pathfinding problems

## 🎯 Problem Variations

### Variation 1: Robot with Diagonal Movement
**Problem**: Robot can move diagonally (8 directions).

**Link**: [CSES Problem Set - Robot Path with Diagonal Movement](https://cses.fi/problemset/task/robot_path_diagonal)

```python
def robot_path_diagonal(obstacles, target):
    from collections import deque
    
    obstacle_set = set(obstacles)
    queue = deque([(0, 0, 0)])
    visited = set()
    
    # 8 directions including diagonals
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    while queue:
        x, y, dist = queue.popleft()
        
        if (x, y) == target:
            return dist
        
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (nx, ny) not in obstacle_set and (nx, ny) not in visited:
                queue.append((nx, ny, dist + 1))
    
    return -1
```

### Variation 2: Robot with Weighted Movement
**Problem**: Different movement costs for different directions.

**Link**: [CSES Problem Set - Robot Path with Weighted Movement](https://cses.fi/problemset/task/robot_path_weighted)

```python
def robot_path_weighted(obstacles, target, costs):
    from collections import deque
    
    obstacle_set = set(obstacles)
    queue = deque([(0, 0, 0)])  # (x, y, total_cost)
    visited = set()
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        x, y, cost = queue.popleft()
        
        if (x, y) == target:
            return cost
        
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        
        for i, (dx, dy) in enumerate(directions):
            nx, ny = x + dx, y + dy
            
            if (nx, ny) not in obstacle_set and (nx, ny) not in visited:
                new_cost = cost + costs[i]
                queue.append((nx, ny, new_cost))
    
    return -1
```

### Variation 3: Robot with Multiple Targets
**Problem**: Find shortest path visiting multiple targets in any order.

**Link**: [CSES Problem Set - Robot Path with Multiple Targets](https://cses.fi/problemset/task/robot_path_multiple_targets)

```python
def robot_path_multiple_targets(obstacles, targets):
    from itertools import permutations
    
    def path_to_target(start, end):
        return robot_path_bfs(obstacles, end, start)
    
    min_total = float('inf')
    
    # Try all possible orders of visiting targets
    for target_order in permutations(targets):
        current = (0, 0)
        total_dist = 0
        
        for target in target_order:
            dist = path_to_target(current, target)
            if dist == -1:
                break
            total_dist += dist
            current = target
        else:
            min_total = min(min_total, total_dist)
    
    return min_total if min_total != float('inf') else -1
```

## 🔗 Related Problems

- **[Labyrinth](/cses-analyses/problem_soulutions/graph_algorithms/labyrinth_analysis/)**: Grid pathfinding with obstacles
- **[Message Route](/cses-analyses/problem_soulutions/graph_algorithms/message_route_analysis/)**: Shortest path in graphs
- **[Grid Paths](/cses-analyses/problem_soulutions/dynamic_programming/grid_paths_analysis/)**: Counting paths in grids
- **[Shortest Routes I](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_i_analysis/)**: Single-source shortest paths
- **[Shortest Routes II](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_ii_analysis/)**: All-pairs shortest paths

## 📚 Learning Points

1. **Breadth-First Search**: Essential for shortest path problems in unweighted graphs
2. **Obstacle Avoidance**: Important technique for pathfinding algorithms
3. **Geometric Algorithms**: Key for spatial problem solving and robotics
4. **Pathfinding Techniques**: Fundamental for game development and robotics
5. **A* Search**: Advanced pathfinding with heuristic guidance
6. **Grid-based Movement**: Common pattern in many algorithmic problems

## 📝 Summary

The Robot Path problem demonstrates fundamental pathfinding concepts using geometric algorithms. We explored three approaches:

1. **Recursive Brute Force**: Exponential time complexity, explores all possible paths
2. **Breadth-First Search**: Guarantees shortest path, polynomial time complexity
3. **A* Search**: Optimal pathfinding with heuristic guidance, most efficient in practice

The key insights include using BFS for shortest path guarantees, efficient obstacle avoidance with set data structures, and the power of heuristic-guided search in A* algorithm. This problem serves as an excellent introduction to pathfinding algorithms and geometric problem-solving techniques.

