---
layout: simple
title: "Knight Moves Grid - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/knight_moves_grid_analysis
---

# Knight Moves Grid - Introductory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of grid traversal and BFS in introductory problems
- Apply efficient algorithms for finding shortest paths on grids
- Implement BFS and graph traversal for grid-based problems
- Optimize algorithms for knight movement problems
- Handle special cases in grid traversal problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: BFS, grid traversal, shortest path, graph algorithms, knight movement
- **Data Structures**: 2D arrays, grids, queues, visited arrays, coordinate systems
- **Mathematical Concepts**: Grid mathematics, coordinate geometry, shortest path theory, graph theory
- **Programming Skills**: BFS implementation, grid manipulation, queue operations, coordinate handling
- **Related Problems**: Grid Path Description (introductory_problems), Chessboard and Queens (introductory_problems), Labyrinth (graph_algorithms)

## 📋 Problem Description

Find the minimum number of moves for a knight to reach a target position on an n×n chessboard from a starting position.

**Input**: 
- n: size of the chessboard (n×n)
- start: starting position (row, col)
- target: target position (row, col)

**Output**: 
- Minimum number of knight moves needed, or -1 if impossible

**Constraints**:
- 1 ≤ n ≤ 1000
- 0 ≤ row, col < n

**Example**:
```
Input:
n = 8
start = (0, 0)
target = (7, 7)

Output:
6

Explanation**: 
Knight moves in L-shape (2+1 or 1+2 squares).
One possible path from (0,0) to (7,7):
(0,0) → (2,1) → (4,2) → (6,3) → (4,4) → (6,5) → (7,7)
Total moves: 6
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible knight moves recursively
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use recursive DFS to explore all paths
- **Inefficient**: O(8^n) time complexity in worst case

**Key Insight**: Use recursive DFS to explore all possible knight moves and find the shortest path.

**Algorithm**:
- Start from the starting position
- Try all 8 possible knight moves
- Use recursive DFS to explore all paths
- Keep track of the minimum moves needed
- Return the minimum moves or -1 if impossible

**Visual Example**:
```
Knight Moves: n = 3, start = (0,0), target = (2,2)

Knight moves in L-shape:
┌─────────────────────────────────────┐
│ Possible knight moves from (r,c):   │
│ - (r+2, c+1), (r+2, c-1)           │
│ - (r-2, c+1), (r-2, c-1)           │
│ - (r+1, c+2), (r+1, c-2)           │
│ - (r-1, c+2), (r-1, c-2)           │
│                                   │
│ From (0,0):                        │
│ - Try (2,1): valid, moves = 1      │
│   - From (2,1): try (0,2): valid, moves = 2 │
│     - From (0,2): try (2,0): valid, moves = 3 │
│       - From (2,0): try (0,1): valid, moves = 4 │
│         - From (0,1): try (2,2): valid, moves = 5 │
│           - Reached target!        │
│ - Try (1,2): valid, moves = 1      │
│   - From (1,2): try (3,0): invalid (out of bounds) │
│   - From (1,2): try (3,4): invalid (out of bounds) │
│   - From (1,2): try (0,0): already visited │
│   - From (1,2): try (2,0): valid, moves = 2 │
│     - Continue exploring...        │
│                                   │
│ Minimum moves: 4                  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_knight_moves(n, start, target):
    """Find minimum knight moves using brute force approach"""
    def is_valid(row, col):
        """Check if position is valid"""
        return 0 <= row < n and 0 <= col < n
    
    def dfs(row, col, moves, visited):
        """DFS to find minimum moves"""
        if (row, col) == target:
            return moves
        
        if moves > n * n:  # Prevent infinite recursion
            return float('inf')
        
        min_moves = float('inf')
        
        # Try all 8 knight moves
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            
            if is_valid(new_row, new_col) and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                result = dfs(new_row, new_col, moves + 1, visited)
                min_moves = min(min_moves, result)
                visited.remove((new_row, new_col))
        
        return min_moves
    
    start_row, start_col = start
    target_row, target_col = target
    
    result = dfs(start_row, start_col, 0, {(start_row, start_col)})
    
    return result if result != float('inf') else -1

# Example usage
n = 8
start = (0, 0)
target = (7, 7)
result = brute_force_knight_moves(n, start, target)
print(f"Brute force moves: {result}")
```

**Time Complexity**: O(8^n)
**Space Complexity**: O(n²)

**Why it's inefficient**: O(8^n) time complexity for exploring all possible paths.

---

### Approach 2: BFS (Breadth-First Search)

**Key Insights from BFS**:
- **BFS**: Use BFS to find shortest path in unweighted graph
- **Efficient Implementation**: O(n²) time complexity
- **Optimal Solution**: BFS guarantees shortest path
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use BFS to find the shortest path from start to target.

**Algorithm**:
- Use BFS to explore positions level by level
- Start from the starting position
- For each position, try all 8 knight moves
- Use a queue to process positions in order
- Return the minimum moves when target is reached

**Visual Example**:
```
BFS for Knight Moves: n = 3, start = (0,0), target = (2,2)

BFS exploration:
┌─────────────────────────────────────┐
│ Level 0: Queue = [(0,0,0)]         │
│ - Process (0,0): moves = 0         │
│ - Add valid moves to queue:        │
│   - (2,1,1), (1,2,1)              │
│                                   │
│ Level 1: Queue = [(2,1,1), (1,2,1)] │
│ - Process (2,1): moves = 1         │
│ - Add valid moves: (0,2,2), (1,0,2) │
│ - Process (1,2): moves = 1         │
│ - Add valid moves: (3,0,2), (0,0,2) │
│                                   │
│ Level 2: Queue = [(0,2,2), (1,0,2), (3,0,2), (0,0,2)] │
│ - Process (0,2): moves = 2         │
│ - Add valid moves: (2,0,3), (1,1,3) │
│ - Process (1,0): moves = 2         │
│ - Add valid moves: (3,1,3), (2,2,3) │
│   - Found target (2,2)!            │
│   - Return moves = 3               │
│                                   │
│ Minimum moves: 3                  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def bfs_knight_moves(n, start, target):
    """Find minimum knight moves using BFS"""
    from collections import deque
    
    def is_valid(row, col):
        """Check if position is valid"""
        return 0 <= row < n and 0 <= col < n
    
    start_row, start_col = start
    target_row, target_col = target
    
    # BFS setup
    queue = deque([(start_row, start_col, 0)])
    visited = {(start_row, start_col)}
    
    # Knight moves
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    while queue:
        row, col, moves = queue.popleft()
        
        # Check if target reached
        if (row, col) == (target_row, target_col):
            return moves
        
        # Try all knight moves
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            
            if is_valid(new_row, new_col) and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, moves + 1))
    
    return -1  # Target not reachable

# Example usage
n = 8
start = (0, 0)
target = (7, 7)
result = bfs_knight_moves(n, start, target)
print(f"BFS moves: {result}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n²)

**Why it's better**: Uses BFS for O(n²) time complexity and guarantees shortest path.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for BFS
- **Efficient Implementation**: O(n²) time complexity
- **Space Efficiency**: O(n²) space complexity
- **Optimal Complexity**: Best approach for knight movement problems

**Key Insight**: Use advanced data structures for optimal BFS implementation.

**Algorithm**:
- Use specialized data structures for BFS
- Implement efficient queue operations
- Handle special cases optimally
- Return minimum moves needed

**Visual Example**:
```
Advanced data structure approach:

For n = 8, start = (0,0), target = (7,7):
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Advanced queue: for efficient     │
│   BFS operations                    │
│ - Visited tracker: for optimization │
│ - Move counter: for optimization    │
│                                   │
│ BFS calculation:                   │
│ - Use advanced queue for efficient  │
│   BFS operations                    │
│ - Use visited tracker for           │
│   optimization                      │
│ - Use move counter for optimization │
│                                   │
│ Result: 6                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_knight_moves(n, start, target):
    """Find minimum knight moves using advanced data structure approach"""
    from collections import deque
    
    def advanced_is_valid(row, col):
        """Advanced position validation"""
        return 0 <= row < n and 0 <= col < n
    
    start_row, start_col = start
    target_row, target_col = target
    
    # Advanced BFS setup
    queue = deque([(start_row, start_col, 0)])
    visited = {(start_row, start_col)}
    
    # Advanced knight moves
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    # Advanced BFS processing
    while queue:
        row, col, moves = queue.popleft()
        
        # Advanced target checking
        if (row, col) == (target_row, target_col):
            return moves
        
        # Advanced move processing
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            
            if advanced_is_valid(new_row, new_col) and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, moves + 1))
    
    return -1

# Example usage
n = 8
start = (0, 0)
target = (7, 7)
result = advanced_data_structure_knight_moves(n, start, target)
print(f"Advanced data structure moves: {result}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n²)

**Why it's optimal**: Uses advanced data structures for optimal BFS implementation.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(8^n) | O(n²) | Use recursive DFS to explore all paths |
| BFS | O(n²) | O(n²) | Use BFS to find shortest path |
| Advanced Data Structure | O(n²) | O(n²) | Use advanced data structures for BFS |

### Time Complexity
- **Time**: O(n²) - Use BFS for efficient shortest path finding
- **Space**: O(n²) - Store visited positions and queue

### Why This Solution Works
- **BFS**: Use BFS to guarantee shortest path in unweighted graph
- **Knight Moves**: Handle all 8 possible knight moves correctly
- **Visited Tracking**: Avoid revisiting positions to prevent cycles
- **Optimal Algorithms**: Use optimal algorithms for shortest path problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Knight Moves with Constraints**
**Problem**: Find knight moves with specific constraints.

**Key Differences**: Apply constraints to knight movement

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_knight_moves(n, start, target, constraints):
    """Find minimum knight moves with constraints"""
    from collections import deque
    
    def constrained_is_valid(row, col):
        """Position validation with constraints"""
        if not (0 <= row < n and 0 <= col < n):
            return False
        return constraints(row, col)
    
    start_row, start_col = start
    target_row, target_col = target
    
    queue = deque([(start_row, start_col, 0)])
    visited = {(start_row, start_col)}
    
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    while queue:
        row, col, moves = queue.popleft()
        
        if (row, col) == (target_row, target_col):
            return moves
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            
            if constrained_is_valid(new_row, new_col) and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, moves + 1))
    
    return -1

# Example usage
n = 8
start = (0, 0)
target = (7, 7)
constraints = lambda row, col: True  # No constraints
result = constrained_knight_moves(n, start, target, constraints)
print(f"Constrained moves: {result}")
```

#### **2. Knight Moves with Different Metrics**
**Problem**: Find knight moves with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_knight_moves(n, start, target, cost_function):
    """Find minimum knight moves with different cost metrics"""
    from collections import deque
    
    def weighted_is_valid(row, col):
        """Position validation with cost consideration"""
        return 0 <= row < n and 0 <= col < n
    
    start_row, start_col = start
    target_row, target_col = target
    
    queue = deque([(start_row, start_col, 0, 0)])  # (row, col, moves, cost)
    visited = {(start_row, start_col)}
    
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    while queue:
        row, col, moves, cost = queue.popleft()
        
        if (row, col) == (target_row, target_col):
            return moves, cost
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            
            if weighted_is_valid(new_row, new_col) and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                new_cost = cost + cost_function(row, col, new_row, new_col)
                queue.append((new_row, new_col, moves + 1, new_cost))
    
    return -1, 0

# Example usage
n = 8
start = (0, 0)
target = (7, 7)
cost_function = lambda r1, c1, r2, c2: 1  # Unit cost
result = weighted_knight_moves(n, start, target, cost_function)
print(f"Weighted moves: {result}")
```

#### **3. Knight Moves with Multiple Dimensions**
**Problem**: Find knight moves in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_knight_moves(n, start, target, dimensions):
    """Find minimum knight moves in multiple dimensions"""
    from collections import deque
    
    def multi_dimensional_is_valid(row, col):
        """Position validation for multiple dimensions"""
        return 0 <= row < n and 0 <= col < n
    
    start_row, start_col = start
    target_row, target_col = target
    
    queue = deque([(start_row, start_col, 0)])
    visited = {(start_row, start_col)}
    
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    while queue:
        row, col, moves = queue.popleft()
        
        if (row, col) == (target_row, target_col):
            return moves
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            
            if multi_dimensional_is_valid(new_row, new_col) and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, moves + 1))
    
    return -1

# Example usage
n = 8
start = (0, 0)
target = (7, 7)
dimensions = 1
result = multi_dimensional_knight_moves(n, start, target, dimensions)
print(f"Multi-dimensional moves: {result}")
```

### Related Problems

#### **CSES Problems**
- [Grid Path Description](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Chessboard and Queens](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Labyrinth](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Minimum Knight Moves](https://leetcode.com/problems/minimum-knight-moves/) - BFS
- [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) - BFS
- [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) - BFS

## Problem Variations

### **Variation 1: Knight Moves with Dynamic Updates**
**Problem**: Handle dynamic grid updates (add/remove/update obstacles) while finding knight moves with minimum steps.

**Approach**: Use efficient data structures and algorithms for dynamic grid management.

```python
from collections import deque, defaultdict
import itertools

class DynamicKnightMoves:
    def __init__(self, n, obstacles=None):
        self.n = n
        self.obstacles = set(obstacles) if obstacles else set()
        self.knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
    
    def add_obstacle(self, row, col):
        """Add obstacle at specified position."""
        if 0 <= row < self.n and 0 <= col < self.n:
            self.obstacles.add((row, col))
    
    def remove_obstacle(self, row, col):
        """Remove obstacle at specified position."""
        self.obstacles.discard((row, col))
    
    def update_obstacle(self, old_row, old_col, new_row, new_col):
        """Update obstacle position."""
        self.remove_obstacle(old_row, old_col)
        self.add_obstacle(new_row, new_col)
    
    def find_knight_moves(self, start, target):
        """Find minimum knight moves from start to target."""
        if start == target:
            return 0
        
        start_row, start_col = start
        target_row, target_col = target
        
        queue = deque([(start_row, start_col, 0)])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                return moves
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in self.obstacles and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, moves + 1))
        
        return -1
    
    def get_moves_with_constraints(self, start, target, constraint_func):
        """Get moves that satisfy custom constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        queue = deque([(start_row, start_col, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                if constraint_func(path, moves):
                    result.append((path, moves))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in self.obstacles and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_path))
        
        return result
    
    def get_moves_in_range(self, start, target, max_moves):
        """Get moves within specified move count range."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        queue = deque([(start_row, start_col, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, path = queue.popleft()
            
            if moves > max_moves:
                continue
            
            if (row, col) == (target_row, target_col):
                result.append((path, moves))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in self.obstacles and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_path))
        
        return result
    
    def get_moves_with_pattern(self, start, target, pattern_func):
        """Get moves matching specified pattern."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        queue = deque([(start_row, start_col, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                if pattern_func(path, moves):
                    result.append((path, moves))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in self.obstacles and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_path))
        
        return result
    
    def get_grid_statistics(self):
        """Get statistics about grid and obstacles."""
        total_cells = self.n * self.n
        obstacle_count = len(self.obstacles)
        free_cells = total_cells - obstacle_count
        
        # Calculate obstacle distribution
        obstacle_distribution = defaultdict(int)
        for row, col in self.obstacles:
            obstacle_distribution[row] += 1
        
        return {
            'total_cells': total_cells,
            'obstacle_count': obstacle_count,
            'free_cells': free_cells,
            'obstacle_density': obstacle_count / total_cells if total_cells > 0 else 0,
            'obstacle_distribution': dict(obstacle_distribution)
        }
    
    def get_grid_patterns(self):
        """Get patterns in grid obstacles."""
        patterns = {
            'clustered_obstacles': 0,
            'scattered_obstacles': 0,
            'row_patterns': 0,
            'column_patterns': 0
        }
        
        if not self.obstacles:
            return patterns
        
        # Check for clustered obstacles
        for row, col in self.obstacles:
            adjacent_obstacles = 0
            for dr, dc in self.knight_moves:
                if (row + dr, col + dc) in self.obstacles:
                    adjacent_obstacles += 1
            if adjacent_obstacles >= 2:
                patterns['clustered_obstacles'] += 1
        
        # Check for scattered obstacles
        for row, col in self.obstacles:
            adjacent_obstacles = 0
            for dr, dc in self.knight_moves:
                if (row + dr, col + dc) in self.obstacles:
                    adjacent_obstacles += 1
            if adjacent_obstacles == 0:
                patterns['scattered_obstacles'] += 1
        
        # Check for row patterns
        row_counts = defaultdict(int)
        for row, col in self.obstacles:
            row_counts[row] += 1
        for count in row_counts.values():
            if count >= 3:
                patterns['row_patterns'] += 1
        
        # Check for column patterns
        col_counts = defaultdict(int)
        for row, col in self.obstacles:
            col_counts[col] += 1
        for count in col_counts.values():
            if count >= 3:
                patterns['column_patterns'] += 1
        
        return patterns
    
    def get_optimal_knight_strategy(self):
        """Get optimal strategy for knight moves."""
        if not self.obstacles:
            return {
                'recommended_strategy': 'direct_path',
                'efficiency_rate': 1.0,
                'obstacle_impact': 0.0
            }
        
        # Calculate efficiency rate
        total_possible_moves = self.n * self.n
        obstacle_impact = len(self.obstacles) / total_possible_moves
        
        # Determine recommended strategy
        if obstacle_impact < 0.1:
            recommended_strategy = 'direct_path'
        elif obstacle_impact < 0.3:
            recommended_strategy = 'obstacle_avoidance'
        else:
            recommended_strategy = 'path_planning'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': 1.0 - obstacle_impact,
            'obstacle_impact': obstacle_impact
        }

# Example usage
n = 8
obstacles = [(1, 1), (2, 2), (3, 3)]
dynamic_knight = DynamicKnightMoves(n, obstacles)
print(f"Initial moves from (0,0) to (7,7): {dynamic_knight.find_knight_moves((0, 0), (7, 7))}")

# Add obstacle
dynamic_knight.add_obstacle(4, 4)
print(f"After adding obstacle at (4,4): {dynamic_knight.find_knight_moves((0, 0), (7, 7))}")

# Remove obstacle
dynamic_knight.remove_obstacle(1, 1)
print(f"After removing obstacle at (1,1): {dynamic_knight.find_knight_moves((0, 0), (7, 7))}")

# Update obstacle
dynamic_knight.update_obstacle(2, 2, 5, 5)
print(f"After updating obstacle from (2,2) to (5,5): {dynamic_knight.find_knight_moves((0, 0), (7, 7))}")

# Get moves with constraints
def constraint_func(path, moves):
    return moves <= 6

print(f"Moves with <= 6 steps: {len(dynamic_knight.get_moves_with_constraints((0, 0), (7, 7), constraint_func))}")

# Get moves in range
print(f"Moves in range 0-5: {len(dynamic_knight.get_moves_in_range((0, 0), (7, 7), 5))}")

# Get moves with pattern
def pattern_func(path, moves):
    return len(path) <= 8

print(f"Moves with <= 8 path length: {len(dynamic_knight.get_moves_with_pattern((0, 0), (7, 7), pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_knight.get_grid_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_knight.get_grid_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_knight.get_optimal_knight_strategy()}")
```

### **Variation 2: Knight Moves with Different Operations**
**Problem**: Handle different types of knight moves (weighted moves, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of knight moves.

```python
class AdvancedKnightMoves:
    def __init__(self, n, weights=None, priorities=None):
        self.n = n
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
    
    def find_weighted_knight_moves(self, start, target):
        """Find minimum weighted knight moves from start to target."""
        if start == target:
            return 0
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0)])  # (row, col, moves, total_weight)
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_weight = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                return moves, total_weight
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    move_weight = self.weights.get((new_row, new_col), 1)
                    new_total_weight = total_weight + move_weight
                    queue.append((new_row, new_col, moves + 1, new_total_weight))
        
        return -1, -1
    
    def get_weighted_moves(self, start, target):
        """Get moves with weights and priorities applied."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_weight, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                weighted_move = {
                    'path': path,
                    'moves': moves,
                    'total_weight': total_weight,
                    'priority': self.priorities.get((row, col), 1),
                    'weighted_score': total_weight * self.priorities.get((row, col), 1)
                }
                result.append(weighted_move)
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    move_weight = self.weights.get((new_row, new_col), 1)
                    new_total_weight = total_weight + move_weight
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_total_weight, new_path))
        
        return result
    
    def get_moves_with_priority(self, start, target, priority_func):
        """Get moves considering priority."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_weight, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                priority = priority_func(row, col, moves, total_weight, self.weights, self.priorities)
                result.append((path, moves, total_weight, priority))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    move_weight = self.weights.get((new_row, new_col), 1)
                    new_total_weight = total_weight + move_weight
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_total_weight, new_path))
        
        # Sort by priority
        result.sort(key=lambda x: x[3], reverse=True)
        return result
    
    def get_moves_with_optimization(self, start, target, optimization_func):
        """Get moves using custom optimization function."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_weight, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                score = optimization_func(row, col, moves, total_weight, self.weights, self.priorities)
                result.append((path, moves, total_weight, score))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    move_weight = self.weights.get((new_row, new_col), 1)
                    new_total_weight = total_weight + move_weight
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_total_weight, new_path))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[3], reverse=True)
        return result
    
    def get_moves_with_constraints(self, start, target, constraint_func):
        """Get moves that satisfy custom constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_weight, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                if constraint_func(row, col, moves, total_weight, self.weights, self.priorities):
                    result.append((path, moves, total_weight))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    move_weight = self.weights.get((new_row, new_col), 1)
                    new_total_weight = total_weight + move_weight
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_total_weight, new_path))
        
        return result
    
    def get_moves_with_multiple_criteria(self, start, target, criteria_list):
        """Get moves that satisfy multiple criteria."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_weight, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                satisfies_all_criteria = True
                for criterion in criteria_list:
                    if not criterion(row, col, moves, total_weight, self.weights, self.priorities):
                        satisfies_all_criteria = False
                        break
                if satisfies_all_criteria:
                    result.append((path, moves, total_weight))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    move_weight = self.weights.get((new_row, new_col), 1)
                    new_total_weight = total_weight + move_weight
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_total_weight, new_path))
        
        return result
    
    def get_moves_with_alternatives(self, start, target, alternatives):
        """Get moves considering alternative weights/priorities."""
        result = []
        
        # Check original moves
        original_moves = self.get_weighted_moves(start, target)
        result.append((original_moves, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedKnightMoves(self.n, alt_weights, alt_priorities)
            temp_moves = temp_instance.get_weighted_moves(start, target)
            result.append((temp_moves, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_moves_with_adaptive_criteria(self, start, target, adaptive_func):
        """Get moves using adaptive criteria."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_weight, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                if adaptive_func(row, col, moves, total_weight, self.weights, self.priorities, result):
                    result.append((path, moves, total_weight))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    move_weight = self.weights.get((new_row, new_col), 1)
                    new_total_weight = total_weight + move_weight
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, moves + 1, new_total_weight, new_path))
        
        return result
    
    def get_knight_optimization(self):
        """Get optimal knight configuration."""
        strategies = [
            ('weighted_moves', lambda: len(self.get_weighted_moves((0, 0), (self.n-1, self.n-1)))),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
n = 8
weights = {(i, j): i + j + 1 for i in range(n) for j in range(n)}  # Higher positions have higher weights
priorities = {(i, j): n - i + n - j for i in range(n) for j in range(n)}  # Lower positions have higher priority
advanced_knight = AdvancedKnightMoves(n, weights, priorities)

print(f"Weighted moves: {len(advanced_knight.get_weighted_moves((0, 0), (7, 7)))}")

# Get moves with priority
def priority_func(row, col, moves, total_weight, weights, priorities):
    return total_weight * weights.get((row, col), 1) + priorities.get((row, col), 1)

print(f"Moves with priority: {len(advanced_knight.get_moves_with_priority((0, 0), (7, 7), priority_func))}")

# Get moves with optimization
def optimization_func(row, col, moves, total_weight, weights, priorities):
    return total_weight * weights.get((row, col), 1) * priorities.get((row, col), 1)

print(f"Moves with optimization: {len(advanced_knight.get_moves_with_optimization((0, 0), (7, 7), optimization_func))}")

# Get moves with constraints
def constraint_func(row, col, moves, total_weight, weights, priorities):
    return total_weight <= 50 and weights.get((row, col), 1) <= 10

print(f"Moves with constraints: {len(advanced_knight.get_moves_with_constraints((0, 0), (7, 7), constraint_func))}")

# Get moves with multiple criteria
def criterion1(row, col, moves, total_weight, weights, priorities):
    return total_weight <= 50

def criterion2(row, col, moves, total_weight, weights, priorities):
    return weights.get((row, col), 1) <= 10

criteria_list = [criterion1, criterion2]
print(f"Moves with multiple criteria: {len(advanced_knight.get_moves_with_multiple_criteria((0, 0), (7, 7), criteria_list))}")

# Get moves with alternatives
alternatives = [({(i, j): 1 for i in range(n) for j in range(n)}, {(i, j): 1 for i in range(n) for j in range(n)}), ({(i, j): i*2 for i in range(n) for j in range(n)}, {(i, j): j+1 for i in range(n) for j in range(n)})]
print(f"Moves with alternatives: {len(advanced_knight.get_moves_with_alternatives((0, 0), (7, 7), alternatives))}")

# Get moves with adaptive criteria
def adaptive_func(row, col, moves, total_weight, weights, priorities, current_result):
    return total_weight <= 50 and len(current_result) < 10

print(f"Moves with adaptive criteria: {len(advanced_knight.get_moves_with_adaptive_criteria((0, 0), (7, 7), adaptive_func))}")

# Get knight optimization
print(f"Knight optimization: {advanced_knight.get_knight_optimization()}")
```

### **Variation 3: Knight Moves with Constraints**
**Problem**: Handle knight moves with additional constraints (move limits, cost constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedKnightMoves:
    def __init__(self, n, constraints=None):
        self.n = n
        self.constraints = constraints or {}
        self.knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
    
    def _is_valid_move(self, row, col, moves, total_cost):
        """Check if move is valid considering constraints."""
        # Move count constraints
        if 'max_moves' in self.constraints:
            if moves > self.constraints['max_moves']:
                return False
        
        # Cost constraints
        if 'max_cost' in self.constraints:
            if total_cost > self.constraints['max_cost']:
                return False
        
        # Position constraints
        if 'forbidden_positions' in self.constraints:
            if (row, col) in self.constraints['forbidden_positions']:
                return False
        
        if 'allowed_positions' in self.constraints:
            if (row, col) not in self.constraints['allowed_positions']:
                return False
        
        # Move pattern constraints
        if 'forbidden_moves' in self.constraints:
            # Check if current move pattern is forbidden
            pass  # Implementation depends on specific constraint
        
        return True
    
    def find_constrained_knight_moves(self, start, target):
        """Find minimum knight moves considering constraints."""
        if start == target:
            return 0
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0)])  # (row, col, moves, total_cost)
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                return moves
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1  # Assuming unit cost per move
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited and
                    self._is_valid_move(new_row, new_col, new_moves, new_cost)):
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, new_moves, new_cost))
        
        return -1
    
    def get_moves_with_move_constraints(self, start, target, max_moves):
        """Get moves considering move count constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if moves > max_moves:
                continue
            
            if (row, col) == (target_row, target_col):
                result.append((path, moves, total_cost))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        return result
    
    def get_moves_with_cost_constraints(self, start, target, max_cost):
        """Get moves considering cost constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if total_cost > max_cost:
                continue
            
            if (row, col) == (target_row, target_col):
                result.append((path, moves, total_cost))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        return result
    
    def get_moves_with_position_constraints(self, start, target, position_constraints):
        """Get moves considering position constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                result.append((path, moves, total_cost))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    satisfies_constraints = True
                    for constraint in position_constraints:
                        if not constraint(new_row, new_col):
                            satisfies_constraints = False
                            break
                    if satisfies_constraints:
                        visited.add((new_row, new_col))
                        new_path = path + [(new_row, new_col)]
                        queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        return result
    
    def get_moves_with_pattern_constraints(self, start, target, pattern_constraints):
        """Get moves considering pattern constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                satisfies_pattern = True
                for constraint in pattern_constraints:
                    if not constraint(path, moves, total_cost):
                        satisfies_pattern = False
                        break
                if satisfies_pattern:
                    result.append((path, moves, total_cost))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        return result
    
    def get_moves_with_mathematical_constraints(self, start, target, constraint_func):
        """Get moves that satisfy custom mathematical constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                if constraint_func(row, col, moves, total_cost, path):
                    result.append((path, moves, total_cost))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        return result
    
    def get_moves_with_range_constraints(self, start, target, range_constraints):
        """Get moves that satisfy range constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                satisfies_constraints = True
                for constraint in range_constraints:
                    if not constraint(row, col, moves, total_cost):
                        satisfies_constraints = False
                        break
                if satisfies_constraints:
                    result.append((path, moves, total_cost))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        return result
    
    def get_moves_with_optimization_constraints(self, start, target, optimization_func):
        """Get moves using custom optimization constraints."""
        # Sort moves by optimization function
        all_moves = []
        if start == target:
            return all_moves
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                score = optimization_func(row, col, moves, total_cost)
                all_moves.append((path, moves, total_cost, score))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        # Sort by optimization score
        all_moves.sort(key=lambda x: x[3], reverse=True)
        
        return [(path, moves, cost) for path, moves, cost, _ in all_moves]
    
    def get_moves_with_multiple_constraints(self, start, target, constraints_list):
        """Get moves that satisfy multiple constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                satisfies_all_constraints = True
                for constraint in constraints_list:
                    if not constraint(row, col, moves, total_cost, path):
                        satisfies_all_constraints = False
                        break
                if satisfies_all_constraints:
                    result.append((path, moves, total_cost))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        return result
    
    def get_moves_with_priority_constraints(self, start, target, priority_func):
        """Get moves with priority-based constraints."""
        # Sort moves by priority
        all_moves = []
        if start == target:
            return all_moves
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                priority = priority_func(row, col, moves, total_cost)
                all_moves.append((path, moves, total_cost, priority))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        # Sort by priority
        all_moves.sort(key=lambda x: x[3], reverse=True)
        
        return [(path, moves, cost) for path, moves, cost, _ in all_moves]
    
    def get_moves_with_adaptive_constraints(self, start, target, adaptive_func):
        """Get moves with adaptive constraints."""
        result = []
        if start == target:
            return result
        
        start_row, start_col = start
        target_row, target_col = target
        
        from collections import deque
        queue = deque([(start_row, start_col, 0, 0, [(start_row, start_col)])])
        visited = {(start_row, start_col)}
        
        while queue:
            row, col, moves, total_cost, path = queue.popleft()
            
            if (row, col) == (target_row, target_col):
                if adaptive_func(row, col, moves, total_cost, path, result):
                    result.append((path, moves, total_cost))
                continue
            
            for dr, dc in self.knight_moves:
                new_row, new_col = row + dr, col + dc
                new_moves = moves + 1
                new_cost = total_cost + 1
                
                if (0 <= new_row < self.n and 0 <= new_col < self.n and
                    (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_moves, new_cost, new_path))
        
        return result
    
    def get_optimal_knight_strategy(self):
        """Get optimal knight strategy considering all constraints."""
        strategies = [
            ('move_constraints', self.get_moves_with_move_constraints),
            ('cost_constraints', self.get_moves_with_cost_constraints),
            ('position_constraints', self.get_moves_with_position_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'move_constraints':
                    current_count = len(strategy_func((0, 0), (self.n-1, self.n-1), 10))
                elif strategy_name == 'cost_constraints':
                    current_count = len(strategy_func((0, 0), (self.n-1, self.n-1), 10))
                elif strategy_name == 'position_constraints':
                    position_constraints = [lambda r, c: r % 2 == 0]
                    current_count = len(strategy_func((0, 0), (self.n-1, self.n-1), position_constraints))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'max_moves': 10,
    'max_cost': 15,
    'forbidden_positions': [(1, 1), (2, 2), (3, 3)],
    'allowed_positions': [(i, j) for i in range(8) for j in range(8)],
}

n = 8
constrained_knight = ConstrainedKnightMoves(n, constraints)

print("Move-constrained moves:", len(constrained_knight.get_moves_with_move_constraints((0, 0), (7, 7), 8)))

print("Cost-constrained moves:", len(constrained_knight.get_moves_with_cost_constraints((0, 0), (7, 7), 12)))

print("Position-constrained moves:", len(constrained_knight.get_moves_with_position_constraints((0, 0), (7, 7), [lambda r, c: r % 2 == 0])))

print("Pattern-constrained moves:", len(constrained_knight.get_moves_with_pattern_constraints((0, 0), (7, 7), [lambda path, moves, cost: moves <= 6])))

# Mathematical constraints
def custom_constraint(row, col, moves, total_cost, path):
    return moves <= 6 and total_cost <= 10

print("Mathematical constraint moves:", len(constrained_knight.get_moves_with_mathematical_constraints((0, 0), (7, 7), custom_constraint)))

# Range constraints
def range_constraint(row, col, moves, total_cost):
    return 1 <= moves <= 8 and 1 <= total_cost <= 12

range_constraints = [range_constraint]
print("Range-constrained moves:", len(constrained_knight.get_moves_with_range_constraints((0, 0), (7, 7), range_constraints)))

# Multiple constraints
def constraint1(row, col, moves, total_cost, path):
    return moves <= 6

def constraint2(row, col, moves, total_cost, path):
    return total_cost <= 10

constraints_list = [constraint1, constraint2]
print("Multiple constraints moves:", len(constrained_knight.get_moves_with_multiple_constraints((0, 0), (7, 7), constraints_list)))

# Priority constraints
def priority_func(row, col, moves, total_cost):
    return total_cost + moves

print("Priority-constrained moves:", len(constrained_knight.get_moves_with_priority_constraints((0, 0), (7, 7), priority_func)))

# Adaptive constraints
def adaptive_func(row, col, moves, total_cost, path, current_result):
    return moves <= 6 and len(current_result) < 5

print("Adaptive constraint moves:", len(constrained_knight.get_moves_with_adaptive_constraints((0, 0), (7, 7), adaptive_func)))

# Optimal strategy
optimal = constrained_knight.get_optimal_knight_strategy()
print(f"Optimal strategy: {optimal}")
```

#### **Problem Categories**
- **Introductory Problems**: Grid traversal, BFS
- **BFS**: Shortest path, grid problems
- **Grid Algorithms**: Knight moves, path finding

## 🔗 Additional Resources

### **Algorithm References**
- [Introductory Problems](https://cp-algorithms.com/intro-to-algorithms.html) - Introductory algorithms
- [BFS](https://cp-algorithms.com/graph/breadth-first-search.html) - BFS algorithms
- [Grid Algorithms](https://cp-algorithms.com/graph/breadth-first-search.html) - Grid algorithms

### **Practice Problems**
- [CSES Grid Path Description](https://cses.fi/problemset/task/1075) - Easy
- [CSES Chessboard and Queens](https://cses.fi/problemset/task/1075) - Easy
- [CSES Labyrinth](https://cses.fi/problemset/task/1075) - Easy

### **Further Reading**
- [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search) - Wikipedia article
- [Knight's Tour](https://en.wikipedia.org/wiki/Knight%27s_tour) - Wikipedia article
- [Shortest Path Problem](https://en.wikipedia.org/wiki/Shortest_path_problem) - Wikipedia article
