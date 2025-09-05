---
layout: simple
title: "Robot Path Analysis"
permalink: /problem_soulutions/geometry/robot_path_analysis
---


# Robot Path Analysis

## Problem Description

**Problem**: Given a robot starting at position (0,0) and a set of obstacles, find the shortest path to reach a target position while avoiding obstacles.

**Input**: 
- n: number of obstacles
- obstacles: list of (x, y) coordinates representing obstacles
- target: (x, y) coordinates of target position

**Output**: Length of shortest path from (0,0) to target, or -1 if impossible.

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

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find shortest path from origin to target
- Avoid obstacles during movement
- Use geometric algorithms
- Apply pathfinding techniques

**Key Observations:**
- This is a pathfinding problem with obstacles
- Can use BFS for shortest path
- Need to handle obstacle avoidance
- Manhattan distance gives lower bound

### Step 2: Breadth-First Search Approach
**Idea**: Use BFS to find shortest path while avoiding obstacles.

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

**Why this works:**
- BFS guarantees shortest path
- Handles obstacle avoidance
- Efficient implementation
- O(n²) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_robot_path():
    n = int(input())
    obstacles = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        obstacles.append((x, y))
    
    target_x, target_y = map(int, input().split())
    target = (target_x, target_y)
    
    result = robot_path_bfs(obstacles, target)
    print(result)

def robot_path_bfs(obstacles, target):
    from collections import deque
    
    obstacle_set = set(obstacles)
    queue = deque([(0, 0, 0)])
    visited = set()
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
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

# Main execution
if __name__ == "__main__":
    solve_robot_path()
```

**Why this works:**
- Optimal BFS approach
- Handles all edge cases
- Efficient obstacle avoidance
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(1, 1), (2, 2), (3, 1)], (4, 4), 8),
        ([(1, 0), (0, 1)], (1, 1), 2),
        ([(1, 1)], (2, 2), 4),
        ([], (5, 5), 10),
    ]
    
    for obstacles, target, expected in test_cases:
        result = solve_test(obstacles, target)
        print(f"Obstacles: {obstacles}, Target: {target}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(obstacles, target):
    return robot_path_bfs(obstacles, target)

def robot_path_bfs(obstacles, target):
    from collections import deque
    
    obstacle_set = set(obstacles)
    queue = deque([(0, 0, 0)])
    visited = set()
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n²) - BFS visits all reachable positions
- **Space**: O(n²) - visited set and queue storage

### Why This Solution Works
- **Breadth-First Search**: Guarantees shortest path
- **Obstacle Avoidance**: Checks obstacle set before moving
- **Visited Tracking**: Prevents revisiting positions
- **Directional Movement**: 4-directional robot movement

## 🎨 Visual Example

### Input Example
```
3 obstacles: (1,1), (2,2), (3,1)
Target: (4,4)
Start: (0,0)
```

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

### BFS Path Finding
```
Step 1: Start at (0,0)
Queue: [(0,0,0)]
Visited: {(0,0)}

Step 2: Explore neighbors of (0,0)
- (0,1): free, add to queue
- (1,0): free, add to queue
Queue: [(0,1,1), (1,0,1)]
Visited: {(0,0), (0,1), (1,0)}

Step 3: Explore neighbors of (0,1)
- (0,2): free, add to queue
- (1,1): obstacle, skip
Queue: [(1,0,1), (0,2,2)]
Visited: {(0,0), (0,1), (1,0), (0,2)}

Step 4: Explore neighbors of (1,0)
- (1,1): obstacle, skip
- (2,0): free, add to queue
Queue: [(0,2,2), (2,0,2)]
Visited: {(0,0), (0,1), (1,0), (0,2), (2,0)}

Continue until target (4,4) is reached...
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

### BFS Algorithm
```
1. Initialize queue with start position
2. Mark start as visited
3. While queue is not empty:
   a. Dequeue current position
   b. If current is target, return distance
   c. For each neighbor:
      - If not visited and not obstacle:
        - Mark as visited
        - Enqueue with distance + 1
4. Return -1 if target not reachable
```

### Direction Vectors
```
4-directional movement:
- Right: (1, 0)
- Up: (0, 1)
- Left: (-1, 0)
- Down: (0, -1)

8-directional movement (if allowed):
- Add diagonals: (1,1), (-1,1), (-1,-1), (1,-1)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ BFS             │ O(area)      │ O(area)      │ Guaranteed   │
│                 │              │              │ shortest     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dijkstra        │ O(area log area)│ O(area)   │ Weighted     │
│                 │              │              │ edges        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ A* Search       │ O(area log area)│ O(area)   │ Heuristic    │
│                 │              │              │ guided       │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **BFS for Shortest Path**
- Guarantees optimal solution
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Obstacle Avoidance**
- Use set for O(1) lookup
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Geometric Pathfinding**
- Grid-based movement
- Important for understanding
- Fundamental concept
- Essential for problem

## 🎯 Problem Variations

### Variation 1: Robot with Diagonal Movement
**Problem**: Robot can move diagonally (8 directions).

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

# Example usage
obstacles = [(1, 1), (2, 2)]
target = (3, 3)
result = robot_path_diagonal(obstacles, target)
print(f"Diagonal path length: {result}")
```

### Variation 2: Robot with Weighted Movement
**Problem**: Different movement costs for different directions.

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

# Example usage
costs = [2, 1, 2, 1]  # up, right, down, left
result = robot_path_weighted(obstacles, target, costs)
print(f"Weighted path cost: {result}")
```

### Variation 3: Robot with Multiple Targets
**Problem**: Find shortest path visiting multiple targets in any order.

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

# Example usage
targets = [(1, 1), (2, 2), (3, 3)]
result = robot_path_multiple_targets(obstacles, targets)
print(f"Multiple targets path: {result}")
```

### Variation 4: Robot with Dynamic Obstacles
**Problem**: Obstacles appear/disappear over time.

```python
class DynamicRobotPath:
    def __init__(self):
        self.obstacles = set()
        self.time = 0
    
    def add_obstacle(self, x, y, duration):
        self.obstacles.add((x, y, self.time + duration))
    
    def remove_expired_obstacles(self):
        current_obstacles = set()
        for x, y, expire_time in self.obstacles:
            if expire_time > self.time:
                current_obstacles.add((x, y))
        self.obstacles = current_obstacles
    
    def find_path(self, target):
        self.remove_expired_obstacles()
        return robot_path_bfs(self.obstacles, target)
    
    def advance_time(self):
        self.time += 1

# Example usage
robot = DynamicRobotPath()
robot.add_obstacle(1, 1, 5)  # Obstacle at (1,1) for 5 time units
result = robot.find_path((2, 2))
print(f"Dynamic path: {result}")
```

### Variation 5: Robot with A* Search
**Problem**: Use A* algorithm for more efficient pathfinding.

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

# Example usage
result = robot_path_astar(obstacles, target)
print(f"A* path length: {result}")
```

## 🔗 Related Problems

- **[Grid Paths](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar grid pathfinding problems
- **[Shortest Path](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph shortest path problems
- **[Geometry Problems](/cses-analyses/problem_soulutions/geometry/)**: Other geometric algorithms

## 📚 Learning Points

1. **Breadth-First Search**: Essential for shortest path problems
2. **Obstacle Avoidance**: Important for pathfinding algorithms
3. **Geometric Algorithms**: Key for spatial problem solving
4. **Pathfinding Techniques**: Fundamental for robotics and games

---

**This is a great introduction to geometric pathfinding algorithms!** 🎯
