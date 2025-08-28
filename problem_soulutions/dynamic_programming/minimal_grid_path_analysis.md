---
layout: simple
title: "Minimal Grid Path"permalink: /problem_soulutions/dynamic_programming/minimal_grid_path_analysis
---


# Minimal Grid Path

## Problem Statement
Given an n×n grid, find the minimum cost path from the top-left corner to the bottom-right corner. You can only move right or down, and each cell has a cost.

### Input
The first input line has an integer n: the size of the grid.
Then there are n lines. Each line has n integers: the costs of the cells.

### Output
Print one integer: the minimum cost of a path from top-left to bottom-right.

### Constraints
- 1 ≤ n ≤ 1000
- 1 ≤ cost ≤ 10^9

### Example
```
Input:
3
1 2 3
4 5 6
7 8 9

Output:
21
```

## Solution Progression

### Approach 1: Recursive - O(2^(n*n))
**Description**: Use recursive approach to find minimum cost path.

```python
def minimal_grid_path_naive(n, grid):
    def min_path_recursive(i, j):
        if i == n-1 and j == n-1:
            return grid[i][j]
        
        if i >= n or j >= n:
            return float('inf')
        
        return grid[i][j] + min(min_path_recursive(i+1, j), min_path_recursive(i, j+1))
    
    return min_path_recursive(0, 0)
```

**Why this is inefficient**: We have overlapping subproblems, leading to exponential time complexity.

### Improvement 1: Dynamic Programming - O(n²)
**Description**: Use 2D DP table to store results of subproblems.

```python
def minimal_grid_path_optimized(n, grid):
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base case
    dp[n-1][n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            # Can move right
            if j + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i+1][j])
            
            dp[i][j] += grid[i][j]
    
    return dp[0][0]
```

**Why this improvement works**: We use a 2D DP table where dp[i][j] represents the minimum cost to reach cell (i,j) from the destination. We fill the table from bottom-right to top-left.

## Final Optimal Solution

```python
n = int(input())
grid = []
for _ in range(n):
    row = list(map(int, input().split()))
    grid.append(row)

def find_minimal_grid_path(n, grid):
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base case
    dp[n-1][n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            # Can move right
            if j + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i+1][j])
            
            dp[i][j] += grid[i][j]
    
    return dp[0][0]

result = find_minimal_grid_path(n, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^(n*n)) | O(n*n) | Overlapping subproblems |
| Dynamic Programming | O(n²) | O(n²) | Use 2D DP table |

## Key Insights for Other Problems

### 1. **Grid Path Problems**
**Principle**: Use 2D DP to find minimum cost paths in grids.
**Applicable to**: Grid problems, path problems, optimization problems

### 2. **2D Dynamic Programming**
**Principle**: Use 2D DP table to store results of subproblems for grid traversal.
**Applicable to**: Grid problems, traversal problems, DP problems

### 3. **Minimum Cost Path**
**Principle**: Find the minimum cost path by considering all possible moves.
**Applicable to**: Path problems, optimization problems, grid problems

## Notable Techniques

### 1. **2D DP Table Construction**
```python
def build_2d_dp_table(n):
    return [[float('inf')] * n for _ in range(n)]
```

### 2. **Grid Path Recurrence**
```python
def grid_path_recurrence(dp, grid, i, j, n):
    if i == n-1 and j == n-1:
        return grid[i][j]
    
    min_cost = float('inf')
    
    # Move right
    if j + 1 < n:
        min_cost = min(min_cost, dp[i][j+1])
    
    # Move down
    if i + 1 < n:
        min_cost = min(min_cost, dp[i+1][j])
    
    return grid[i][j] + min_cost
```

### 3. **DP Table Filling**
```python
def fill_dp_table(grid, n):
    dp = build_2d_dp_table(n)
    dp[n-1][n-1] = grid[n-1][n-1]
    
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            dp[i][j] = grid_path_recurrence(dp, grid, i, j, n)
    
    return dp[0][0]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a minimum cost grid path problem
2. **Choose approach**: Use 2D dynamic programming
3. **Define DP state**: dp[i][j] = minimum cost to reach (i,j) from destination
4. **Base case**: dp[n-1][n-1] = grid[n-1][n-1]
5. **Recurrence relation**: dp[i][j] = grid[i][j] + min(dp[i+1][j], dp[i][j+1])
6. **Fill DP table**: Iterate from bottom-right to top-left
7. **Return result**: Output dp[0][0]

---

*This analysis shows how to efficiently find the minimum cost path in a grid using 2D dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Maximum Cost Path**
**Problem**: Find the maximum cost path from top-left to bottom-right.
```python
def maximal_grid_path(n, grid):
    dp = [[float('-inf')] * n for _ in range(n)]
    
    # Base case
    dp[n-1][n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            # Can move right
            if j + 1 < n:
                dp[i][j] = max(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n:
                dp[i][j] = max(dp[i][j], dp[i+1][j])
            
            dp[i][j] += grid[i][j]
    
    return dp[0][0]
```

#### **Variation 2: Grid Path with Diagonal Moves**
**Problem**: Allow diagonal moves (down-right) in addition to right and down.
```python
def grid_path_with_diagonals(n, grid):
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base case
    dp[n-1][n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            # Can move right
            if j + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i+1][j])
            
            # Can move diagonally (down-right)
            if i + 1 < n and j + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i+1][j+1])
            
            dp[i][j] += grid[i][j]
    
    return dp[0][0]
```

#### **Variation 3: Grid Path with Obstacles**
**Problem**: Some cells are blocked (infinite cost), find minimum cost path avoiding obstacles.
```python
def grid_path_with_obstacles(n, grid, obstacles):
    # obstacles[i][j] = True if cell (i,j) is blocked
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base case
    if not obstacles[n-1][n-1]:
        dp[n-1][n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue
            
            if obstacles[i][j]:
                continue
            
            # Can move right
            if j + 1 < n and not obstacles[i][j+1]:
                dp[i][j] = min(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n and not obstacles[i+1][j]:
                dp[i][j] = min(dp[i][j], dp[i+1][j])
            
            if dp[i][j] != float('inf'):
                dp[i][j] += grid[i][j]
    
    return dp[0][0] if dp[0][0] != float('inf') else -1
```

#### **Variation 4: Grid Path with Limited Moves**
**Problem**: Find minimum cost path using at most k moves.
```python
def grid_path_with_move_limit(n, grid, k):
    # dp[i][j][moves] = min cost to reach (i,j) using exactly 'moves' steps
    dp = [[[float('inf')] * (k + 1) for _ in range(n)] for _ in range(n)]
    
    # Base case
    dp[0][0][0] = grid[0][0]
    
    # Fill DP table
    for moves in range(k):
        for i in range(n):
            for j in range(n):
                if dp[i][j][moves] == float('inf'):
                    continue
                
                # Move right
                if j + 1 < n:
                    dp[i][j+1][moves+1] = min(dp[i][j+1][moves+1], 
                                             dp[i][j][moves] + grid[i][j+1])
                
                # Move down
                if i + 1 < n:
                    dp[i+1][j][moves+1] = min(dp[i+1][j][moves+1], 
                                             dp[i][j][moves] + grid[i+1][j])
    
    # Find minimum cost with at most k moves
    min_cost = float('inf')
    for moves in range(k + 1):
        min_cost = min(min_cost, dp[n-1][n-1][moves])
    
    return min_cost if min_cost != float('inf') else -1
```

#### **Variation 5: Grid Path with Multiple Destinations**
**Problem**: Find minimum cost path to any of multiple destination cells.
```python
def grid_path_multiple_destinations(n, grid, destinations):
    # destinations = list of (i,j) coordinates
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base cases for all destinations
    for i, j in destinations:
        dp[i][j] = grid[i][j]
    
    # Fill from destinations to top-left
    for i in range(n):
        for j in range(n):
            if (i, j) in destinations:
                continue
            
            # Can move right
            if j + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i+1][j])
            
            if dp[i][j] != float('inf'):
                dp[i][j] += grid[i][j]
    
    return dp[0][0]
```

### 🔗 **Related Problems & Concepts**

#### **1. Grid Path Problems**
- **Unique Paths**: Count paths from top-left to bottom-right
- **Unique Paths II**: Count paths avoiding obstacles
- **Minimum Path Sum**: Find minimum sum path
- **Maximum Path Sum**: Find maximum sum path

#### **2. Dynamic Programming Patterns**
- **2D DP**: Two state variables (row, column)
- **3D DP**: Three state variables (row, column, additional constraint)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Graph Theory**
- **Shortest Path**: Find shortest path in weighted graph
- **Dijkstra's Algorithm**: Single-source shortest path
- **Floyd-Warshall**: All-pairs shortest path
- **Bellman-Ford**: Shortest path with negative weights

#### **4. Optimization Problems**
- **Minimum Cost**: Find minimum cost solution
- **Maximum Value**: Find maximum value solution
- **Resource Allocation**: Optimal use of limited resources
- **Scheduling**: Optimal arrangement of tasks

#### **5. Algorithmic Techniques**
- **Breadth-First Search**: Level-by-level traversal
- **Depth-First Search**: Recursive traversal
- **A* Search**: Heuristic-based pathfinding
- **Dynamic Programming**: Optimal substructure

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    result = find_minimal_grid_path(n, grid)
    print(result)
```

#### **2. Range Queries on Grid Paths**
```python
def range_grid_path_queries(n, grid, queries):
    # Precompute for all subgrids
    dp = [[[float('inf')] * n for _ in range(n)] for _ in range(n)]
    
    # Fill DP for all possible subgrids
    for start_i in range(n):
        for start_j in range(n):
            for end_i in range(start_i, n):
                for end_j in range(start_j, n):
                    # Calculate min path for subgrid (start_i,start_j) to (end_i,end_j)
                    pass
    
    # Answer queries
    for start_i, start_j, end_i, end_j in queries:
        print(dp[start_i][start_j][end_i][end_j])
```

#### **3. Interactive Grid Problems**
```python
def interactive_grid_game():
    n = int(input())
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    
    print("Grid:")
    for row in grid:
        print(row)
    
    # Player tries to find min path
    player_guess = int(input("Enter minimum path cost: "))
    actual_cost = find_minimal_grid_path(n, grid)
    
    if player_guess == actual_cost:
        print("Correct!")
    else:
        print(f"Wrong! Actual minimum cost is {actual_cost}")
```

### 🧮 **Mathematical Extensions**

#### **1. Path Counting**
- **Catalan Numbers**: Count valid paths in grid
- **Combinatorial Paths**: Count paths with specific properties
- **Lattice Paths**: Paths in integer lattice
- **Dyck Paths**: Paths that never go below diagonal

#### **2. Advanced DP Techniques**
- **Digit DP**: Count paths with specific digit properties
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split grid into subgrids
- **Persistent Data Structures**: Maintain path history

#### **3. Geometric Interpretations**
- **Manhattan Distance**: L1 distance in grid
- **Euclidean Distance**: L2 distance in continuous space
- **Chebyshev Distance**: L∞ distance in grid
- **Taxicab Geometry**: Distance in grid world

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Dijkstra's Algorithm**: Single-source shortest path
- **Floyd-Warshall**: All-pairs shortest path
- **A* Search**: Heuristic-based pathfinding
- **Bellman-Ford**: Shortest path with negative weights

#### **2. Mathematical Concepts**
- **Graph Theory**: Study of graphs and networks
- **Combinatorics**: Counting paths and combinations
- **Optimization Theory**: Finding optimal solutions
- **Geometry**: Spatial relationships and distances

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Algorithm Design**: Creating efficient solutions

---

*This analysis demonstrates the power of dynamic programming for grid path problems and shows various extensions and applications.* 