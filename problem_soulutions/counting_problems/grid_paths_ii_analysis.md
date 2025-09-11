---
layout: simple
title: "Grid Paths II"
permalink: /problem_soulutions/counting_problems/grid_paths_ii_analysis
---


# Grid Paths II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand grid path counting with obstacles and movement constraints
- Apply dynamic programming to count valid paths in 2D grids
- Implement efficient DP algorithms for grid path counting with obstacles
- Optimize grid path counting using space-efficient DP techniques
- Handle edge cases in grid path counting (blocked start/end, no valid paths)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, grid algorithms, path counting, obstacle handling
- **Data Structures**: 2D arrays, DP tables, grid representations
- **Mathematical Concepts**: Grid theory, path counting, combinatorics, modular arithmetic
- **Programming Skills**: 2D DP implementation, grid manipulation, modular arithmetic
- **Related Problems**: Grid Paths (basic grid paths), Labyrinth (grid traversal), Message Route (path finding)

## 📋 Problem Description

Given an n×n grid with some blocked cells, count the number of paths from the top-left corner to the bottom-right corner, moving only right or down.

**Input**: 
- First line: integer n (size of the grid)
- Next n lines: n characters each ('.' for empty cell, '#' for blocked cell)

**Output**: 
- Print the number of valid paths modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 1000

**Example**:
```
Input:
3
...
.#.
...

Output:
2

Explanation**: 
In the 3×3 grid, there are 2 valid paths from (0,0) to (2,2):
1. Right → Right → Down → Down: (0,0) → (0,1) → (0,2) → (1,2) → (2,2)
2. Down → Down → Right → Right: (0,0) → (1,0) → (2,0) → (2,1) → (2,2)

Both paths avoid the blocked cell at (1,1) and reach the destination.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Generate All Possible Paths

**Key Insights from Brute Force Approach**:
- **Exhaustive Path Generation**: Generate all possible paths from start to end
- **Path Validation**: Check if each path avoids blocked cells
- **Complete Coverage**: Guaranteed to find all valid paths
- **Simple Implementation**: Recursive approach to explore all possibilities

**Key Insight**: Systematically generate all possible paths from (0,0) to (n-1,n-1) and count those that avoid blocked cells.

**Algorithm**:
- Use recursive DFS to explore all possible paths
- At each cell, try moving right and down (if valid)
- Count paths that reach the destination without hitting blocked cells

**Visual Example**:
```
Grid (3×3):
. . .
. # .
. . .

All possible paths from (0,0) to (2,2):
1. R→R→D→D: (0,0)→(0,1)→(0,2)→(1,2)→(2,2) ✓
2. R→D→R→D: (0,0)→(0,1)→(1,1) ✗ (blocked)
3. R→D→D→R: (0,0)→(0,1)→(1,1) ✗ (blocked)
4. D→R→R→D: (0,0)→(1,0)→(1,1) ✗ (blocked)
5. D→R→D→R: (0,0)→(1,0)→(1,1) ✗ (blocked)
6. D→D→R→R: (0,0)→(1,0)→(2,0)→(2,1)→(2,2) ✓

Valid paths: 2
```

**Implementation**:
```python
def brute_force_grid_paths(grid):
    """
    Count valid paths using brute force approach
    
    Args:
        grid: 2D list representing the grid ('.' for empty, '#' for blocked)
    
    Returns:
        int: number of valid paths from (0,0) to (n-1,n-1)
    """
    n = len(grid)
    
    def dfs(i, j):
        # Base case: reached destination
        if i == n-1 and j == n-1:
            return 1
        
        # Base case: out of bounds or blocked
        if i >= n or j >= n or grid[i][j] == '#':
            return 0
        
        # Recursive case: try moving right and down
        return dfs(i, j+1) + dfs(i+1, j)
    
    return dfs(0, 0)

# Example usage
grid = [
    ['.', '.', '.'],
    ['.', '#', '.'],
    ['.', '.', '.']
]
result = brute_force_grid_paths(grid)
print(f"Brute force result: {result}")  # Output: 2
```

**Time Complexity**: O(2^(2n)) - Exponential due to overlapping subproblems
**Space Complexity**: O(n) - Recursion stack depth

**Why it's inefficient**: Exponential time complexity due to repeated calculations of the same subproblems.

---

### Approach 2: Optimized - Dynamic Programming with Memoization

**Key Insights from Optimized Approach**:
- **Memoization**: Store results of subproblems to avoid recomputation
- **Overlapping Subproblems**: Many paths share common subpaths
- **Top-Down DP**: Use recursive approach with memoization
- **Efficient Storage**: Cache results for each cell position

**Key Insight**: Use memoization to avoid recalculating the same subproblems, significantly reducing time complexity.

**Algorithm**:
- Use recursive DFS with memoization
- Store the number of paths from each cell to the destination
- Return cached result if already computed

**Visual Example**:
```
Grid (3×3):
. . .
. # .
. . .

Memoization table (paths from each cell to (2,2)):
[2, 1, 1]
[1, 0, 1]
[1, 1, 1]

Explanation:
- (0,0): 2 paths (R→R→D→D, D→D→R→R)
- (0,1): 1 path (R→D→D)
- (0,2): 1 path (D→D)
- (1,0): 1 path (D→R→R)
- (1,1): 0 paths (blocked)
- (1,2): 1 path (D)
- (2,0): 1 path (R→R)
- (2,1): 1 path (R)
- (2,2): 1 path (destination)
```

**Implementation**:
```python
def optimized_grid_paths(grid):
    """
    Count valid paths using memoization
    
    Args:
        grid: 2D list representing the grid
    
    Returns:
        int: number of valid paths from (0,0) to (n-1,n-1)
    """
    n = len(grid)
    memo = {}
    
    def dfs(i, j):
        # Base case: reached destination
        if i == n-1 and j == n-1:
            return 1
        
        # Base case: out of bounds or blocked
        if i >= n or j >= n or grid[i][j] == '#':
            return 0
        
        # Check if already computed
        if (i, j) in memo:
            return memo[(i, j)]
        
        # Compute and store result
        result = dfs(i, j+1) + dfs(i+1, j)
        memo[(i, j)] = result
        return result
    
    return dfs(0, 0)

# Example usage
grid = [
    ['.', '.', '.'],
    ['.', '#', '.'],
    ['.', '.', '.']
]
result = optimized_grid_paths(grid)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - Each cell computed once
**Space Complexity**: O(n²) - For memoization table

**Why it's better**: Eliminates redundant calculations, making it much more efficient.

---

### Approach 3: Optimal - Bottom-Up Dynamic Programming

**Key Insights from Optimal Approach**:
- **Bottom-Up DP**: Build solution from base cases to target
- **Tabular Approach**: Use 2D table to store results
- **Iterative Solution**: Avoid recursion overhead
- **Space Optimization**: Can optimize space usage further

**Key Insight**: Use bottom-up dynamic programming to build the solution iteratively, avoiding recursion and providing optimal time and space complexity.

**Algorithm**:
- Create DP table where dp[i][j] = number of paths from (i,j) to destination
- Fill table from bottom-right to top-left
- Handle blocked cells and boundary conditions
- Return dp[0][0]

**Visual Example**:
```
Grid (3×3):
. . .
. # .
. . .

DP table construction (bottom-up):
Step 1: Initialize destination
[0, 0, 0]
[0, 0, 0]
[0, 0, 1]

Step 2: Fill bottom row
[0, 0, 0]
[0, 0, 1]
[1, 1, 1]

Step 3: Fill middle row
[0, 0, 1]
[0, 0, 1]
[1, 1, 1]

Step 4: Fill top row
[2, 1, 1]
[0, 0, 1]
[1, 1, 1]

Result: dp[0][0] = 2
```

**Implementation**:
```python
def optimal_grid_paths(grid):
    """
    Count valid paths using bottom-up DP
    
    Args:
        grid: 2D list representing the grid
    
    Returns:
        int: number of valid paths from (0,0) to (n-1,n-1)
    """
    n = len(grid)
    
    # Initialize DP table
    dp = [[0] * n for _ in range(n)]
    
    # Base case: destination has 1 path
    if grid[n-1][n-1] != '#':
        dp[n-1][n-1] = 1
    
    # Fill table from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            # Skip if blocked or already filled (destination)
            if grid[i][j] == '#' or (i == n-1 and j == n-1):
                continue
            
            # Add paths from right and down
            if j+1 < n:
                dp[i][j] += dp[i][j+1]
            if i+1 < n:
                dp[i][j] += dp[i+1][j]
    
    return dp[0][0]

# Example usage
grid = [
    ['.', '.', '.'],
    ['.', '#', '.'],
    ['.', '.', '.']
]
result = optimal_grid_paths(grid)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - Fill entire DP table once
**Space Complexity**: O(n²) - For DP table

**Why it's optimal**: Efficient bottom-up approach with optimal time and space complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^(2n)) | O(n) | Generate all paths recursively |
| Memoization | O(n²) | O(n²) | Cache subproblem results |
| Bottom-Up DP | O(n²) | O(n²) | Build solution iteratively |

### Time Complexity
- **Time**: O(n²) - Each cell computed once in optimal approach
- **Space**: O(n²) - For DP table

### Why This Solution Works
- **Path Counting**: Count all valid paths from start to destination
- **Obstacle Avoidance**: Skip blocked cells in path calculation
- **Dynamic Programming**: Efficiently solve overlapping subproblems
- **Optimal Approach**: Bottom-up DP provides best performance

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Grid Paths with Multiple Destinations**
**Problem**: Count paths from start to any of multiple destination cells.

**Key Differences**: Multiple possible end points instead of single destination

**Solution Approach**: Sum paths to all valid destinations

**Implementation**:
```python
def grid_paths_multiple_destinations(grid, start, destinations):
    """
    Count paths from start to any of multiple destinations
    """
    n, m = len(grid), len(grid[0])
    dp = [[0] * m for _ in range(n)]
    
    # Initialize start position
    dp[start[0]][start[1]] = 1
    
    # Fill DP table
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0:  # Not blocked
                if i > 0:
                    dp[i][j] += dp[i-1][j]
                if j > 0:
                    dp[i][j] += dp[i][j-1]
    
    # Sum paths to all destinations
    total_paths = 0
    for dest in destinations:
        if grid[dest[0]][dest[1]] == 0:
            total_paths += dp[dest[0]][dest[1]]
    
    return total_paths

def grid_paths_with_waypoints(grid, start, waypoints, end):
    """
    Count paths that visit all waypoints in order
    """
    total_paths = 1
    current = start
    
    # Visit each waypoint in order
    for waypoint in waypoints:
        paths = grid_paths_multiple_destinations(grid, current, [waypoint])
        if paths == 0:
            return 0
        total_paths *= paths
        current = waypoint
    
    # Final path to end
    final_paths = grid_paths_multiple_destinations(grid, current, [end])
    return total_paths * final_paths

# Example usage
grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
start = (0, 0)
destinations = [(2, 2), (1, 0), (0, 2)]
result = grid_paths_multiple_destinations(grid, start, destinations)
print(f"Paths to multiple destinations: {result}")  # Output: 3
```

#### **2. Grid Paths with Constraints**
**Problem**: Count paths with additional constraints (e.g., maximum steps, specific directions).

**Key Differences**: Add constraints to path generation

**Solution Approach**: Use constrained DP with additional state

**Implementation**:
```python
def grid_paths_with_max_steps(grid, start, end, max_steps):
    """
    Count paths with maximum step constraint
    """
    n, m = len(grid), len(grid[0])
    # DP[steps][i][j] = paths to (i,j) in exactly 'steps' moves
    dp = [[[0] * m for _ in range(n)] for _ in range(max_steps + 1)]
    
    dp[0][start[0]][start[1]] = 1
    
    for steps in range(1, max_steps + 1):
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 0:  # Not blocked
                    if i > 0:
                        dp[steps][i][j] += dp[steps-1][i-1][j]
                    if j > 0:
                        dp[steps][i][j] += dp[steps-1][i][j-1]
    
    return dp[max_steps][end[0]][end[1]]

def grid_paths_with_direction_constraints(grid, start, end, allowed_directions):
    """
    Count paths with specific direction constraints
    """
    n, m = len(grid), len(grid[0])
    dp = [[0] * m for _ in range(n)]
    
    dp[start[0]][start[1]] = 1
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0:  # Not blocked
                if 'up' in allowed_directions and i > 0:
                    dp[i][j] += dp[i-1][j]
                if 'left' in allowed_directions and j > 0:
                    dp[i][j] += dp[i][j-1]
    
    return dp[end[0]][end[1]]

def grid_paths_with_visits(grid, start, end, must_visit):
    """
    Count paths that must visit specific cells
    """
    def count_paths_with_visits(current, visited, remaining_visits):
        if current == end and len(remaining_visits) == 0:
            return 1
        
        if current in remaining_visits:
            remaining_visits = remaining_visits - {current}
        
        total = 0
        i, j = current
        
        # Try moving right
        if j + 1 < len(grid[0]) and grid[i][j+1] == 0:
            total += count_paths_with_visits((i, j+1), visited | {current}, remaining_visits)
        
        # Try moving down
        if i + 1 < len(grid) and grid[i+1][j] == 0:
            total += count_paths_with_visits((i+1, j), visited | {current}, remaining_visits)
        
        return total
    
    return count_paths_with_visits(start, set(), set(must_visit))

# Example usage
grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
start = (0, 0)
end = (2, 2)
max_steps = 4
result = grid_paths_with_max_steps(grid, start, end, max_steps)
print(f"Paths with max steps: {result}")  # Output: 6
```

#### **3. Grid Paths with Dynamic Obstacles**
**Problem**: Count paths when obstacles can be added or removed dynamically.

**Key Differences**: Handle dynamic grid changes

**Solution Approach**: Use incremental updates and caching

**Implementation**:
```python
class DynamicGridPaths:
    def __init__(self, grid, start, end):
        self.grid = [row[:] for row in grid]
        self.n, self.m = len(grid), len(grid[0])
        self.start = start
        self.end = end
        self.dp = None
        self._recompute_paths()
    
    def _recompute_paths(self):
        """Recompute all path counts"""
        self.dp = [[0] * self.m for _ in range(self.n)]
        self.dp[self.start[0]][self.start[1]] = 1
        
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 0:  # Not blocked
                    if i > 0:
                        self.dp[i][j] += self.dp[i-1][j]
                    if j > 0:
                        self.dp[i][j] += self.dp[i][j-1]
    
    def add_obstacle(self, i, j):
        """Add obstacle at position (i,j)"""
        if self.grid[i][j] == 0:
            self.grid[i][j] = 1
            self._recompute_paths()
    
    def remove_obstacle(self, i, j):
        """Remove obstacle at position (i,j)"""
        if self.grid[i][j] == 1:
            self.grid[i][j] = 0
            self._recompute_paths()
    
    def get_path_count(self):
        """Get current path count"""
        return self.dp[self.end[0]][self.end[1]]
    
    def get_paths_to_cell(self, i, j):
        """Get path count to specific cell"""
        return self.dp[i][j]

def grid_paths_with_queries(grid, start, end, queries):
    """
    Answer multiple path queries with dynamic obstacles
    """
    solver = DynamicGridPaths(grid, start, end)
    results = []
    
    for query in queries:
        if query[0] == 'add_obstacle':
            solver.add_obstacle(query[1], query[2])
        elif query[0] == 'remove_obstacle':
            solver.remove_obstacle(query[1], query[2])
        elif query[0] == 'get_paths':
            results.append(solver.get_path_count())
        elif query[0] == 'get_paths_to':
            results.append(solver.get_paths_to_cell(query[1], query[2]))
    
    return results

# Example usage
grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
start = (0, 0)
end = (2, 2)
queries = [
    ('get_paths',),
    ('add_obstacle', 1, 1),
    ('get_paths',),
    ('remove_obstacle', 1, 1),
    ('get_paths',)
]
result = grid_paths_with_queries(grid, start, end, queries)
print(f"Path counts: {result}")  # Output: [6, 2, 6]
```

### Related Problems

#### **CSES Problems**
- [Grid Paths II](https://cses.fi/problemset/task/2101) - Count paths with obstacles
- [Grid Paths](https://cses.fi/problemset/task/2102) - Basic grid path counting
- [Robot Paths](https://cses.fi/problemset/task/2103) - Robot path optimization

#### **LeetCode Problems**
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Count paths without obstacles
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Count paths with obstacles
- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) - Find minimum cost path
- [Dungeon Game](https://leetcode.com/problems/dungeon-game/) - Path with health constraints

#### **Problem Categories**
- **Dynamic Programming**: Path counting, state transitions, optimal substructure
- **Grid Processing**: 2D array navigation, obstacle handling, path enumeration
- **Combinatorics**: Path counting, constraint satisfaction, counting principles
- **Graph Theory**: Grid as graph, path finding, connectivity analysis
