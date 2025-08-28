---
layout: simple
title: "Grid Paths
permalink: /problem_soulutions/dynamic_programming/grid_paths_analysis/"
---


# Grid Paths

## Problem Statement
Consider an n×n grid whose squares may have traps. It is not allowed to move to a square with a trap.

Your task is to calculate the number of paths from the upper-left square to the lower-right square. You can only move right or down.

### Input
The first input line has an integer n: the size of the grid."
After this, there are n lines that describe the grid. Each line has n characters: "." denotes an empty cell, and "*" denotes a trap.

### Output
Print the number of paths modulo 10^9+7.

### Constraints
- 1 ≤ n ≤ 1000

### Example
```
Input:
4
....
.*..
...*
*...

Output:
3
```

## Solution Progression

### Approach 1: Recursive Brute Force - O(2^(n²))
**Description**: Try all possible paths recursively.

```python
def grid_paths_brute_force(n, grid):
    MOD = 10**9 + 7
    
    def count_paths(row, col):
        if row == n-1 and col == n-1:
            return 1
        if row >= n or col >= n or grid[row][col] == '*':
            return 0
        
        # Move right and down
        right = count_paths(row, col + 1)
        down = count_paths(row + 1, col)
        
        return (right + down) % MOD
    
    return count_paths(0, 0)
```

**Why this is inefficient**: We're trying all possible paths, which leads to exponential complexity. For each position, we have 2 choices (right or down), leading to O(2^(n²)) complexity.

### Improvement 1: Recursive with Memoization - O(n²)
**Description**: Use memoization to avoid recalculating the same subproblems.

```python
def grid_paths_memoization(n, grid):
    MOD = 10**9 + 7
    memo = {}
    
    def count_paths(row, col):
        if (row, col) in memo:
            return memo[(row, col)]
        
        if row == n-1 and col == n-1:
            return 1
        if row >= n or col >= n or grid[row][col] == '*':
            return 0
        
        # Move right and down
        right = count_paths(row, col + 1)
        down = count_paths(row + 1, col)
        
        memo[(row, col)] = (right + down) % MOD
        return memo[(row, col)]
    
    return count_paths(0, 0)
```

**Why this improvement works**: By storing the results of subproblems in a memo dictionary, we avoid recalculating the same values multiple times. Each subproblem is solved only once, leading to O(n²) complexity.

### Improvement 2: Bottom-Up Dynamic Programming - O(n²)
**Description**: Use iterative DP to build the solution from smaller subproblems.

```python
def grid_paths_dp(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case: starting position
    if grid[0][0] != '*':
        dp[0][0] = 1
    
    # Fill first row
    for j in range(1, n):
        if grid[0][j] != '*':
            dp[0][j] = dp[0][j-1]
    
    # Fill first column
    for i in range(1, n):
        if grid[i][0] != '*':
            dp[i][0] = dp[i-1][0]
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] != '*':
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]
```

**Why this improvement works**: We build the solution iteratively by solving smaller subproblems first. For each cell, we add the paths from the cell above and the cell to the left.

### Alternative: Optimized DP with Boundary Handling - O(n²)
**Description**: Use a more efficient DP approach with better boundary handling.

```python
def grid_paths_optimized(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Initialize with boundary conditions
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[i][j] = 0
            elif i == 0 and j == 0:
                dp[i][j] = 1
            elif i == 0:
                dp[i][j] = dp[i][j-1]
            elif j == 0:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]
```

**Why this works**: This approach handles all boundary conditions in a single loop, making it more concise and efficient.

## Final Optimal Solution

```python
n = int(input())
grid = [input().strip() for _ in range(n)]
MOD = 10**9 + 7

# dp[i][j] = number of paths from (0,0) to (i,j)
dp = [[0] * n for _ in range(n)]

# Base case: starting position
if grid[0][0] != '*':
    dp[0][0] = 1

# Fill first row
for j in range(1, n):
    if grid[0][j] != '*':
        dp[0][j] = dp[0][j-1]

# Fill first column
for i in range(1, n):
    if grid[i][0] != '*':
        dp[i][0] = dp[i-1][0]

# Fill rest of the grid
for i in range(1, n):
    for j in range(1, n):
        if grid[i][j] != '*':
            dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD

print(dp[n-1][n-1])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^(n²)) | O(n²) | Try all paths |
| Memoization | O(n²) | O(n²) | Store subproblem results |
| Bottom-Up DP | O(n²) | O(n²) | Build solution iteratively |
| Optimized DP | O(n²) | O(n²) | Efficient boundary handling |

## Key Insights for Other Problems

### 1. **Dynamic Programming for Path Counting**
**Principle**: Use DP to count the number of paths in grid problems.
**Applicable to**:
- Grid problems
- Path counting
- Matrix problems
- Graph problems

**Example Problems**:
- Grid paths
- Path counting
- Matrix problems
- Graph problems

### 2. **Grid-Based DP**
**Principle**: Use 2D DP arrays for grid-based problems.
**Applicable to**:
- Grid problems
- Matrix problems
- 2D dynamic programming
- Spatial problems

**Example Problems**:
- Grid problems
- Matrix problems
- 2D dynamic programming
- Spatial problems

### 3. **Boundary Condition Handling**
**Principle**: Handle boundary conditions carefully in grid-based problems.
**Applicable to**:
- Grid problems
- Matrix problems
- Boundary conditions
- Algorithm design

**Example Problems**:
- Grid problems
- Matrix problems
- Boundary conditions
- Algorithm design

### 4. **State Definition for Grid Problems**
**Principle**: Define states that capture the essential information for grid-based problems.
**Applicable to**:
- Dynamic programming
- Grid problems
- State machine problems
- Algorithm design

**Example Problems**:
- Dynamic programming
- Grid problems
- State machine problems
- Algorithm design

## Notable Techniques

### 1. **2D DP State Definition Pattern**
```python
# Define 2D DP state for grid problems
dp = [[0] * n for _ in range(n)]
dp[0][0] = 1  # Base case
```

### 2. **Grid Traversal Pattern**
```python
# Fill grid row by row and column by column
for i in range(n):
    for j in range(n):
        if condition:
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

### 3. **Boundary Handling Pattern**
```python
# Handle boundary conditions
if i == 0 and j == 0:
    dp[i][j] = 1
elif i == 0:
    dp[i][j] = dp[i][j-1]
elif j == 0:
    dp[i][j] = dp[i-1][j]
else:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

## Edge Cases to Remember

1. **n = 1**: Handle single cell grid
2. **All cells are traps**: Return 0
3. **Start or end is trap**: Return 0
4. **Large grid**: Use efficient DP approach
5. **Boundary conditions**: Handle first row and column separately

## Problem-Solving Framework

1. **Identify grid nature**: This is a grid-based path counting problem
2. **Define state**: dp[i][j] = number of paths to (i,j)
3. **Define transitions**: dp[i][j] = dp[i-1][j] + dp[i][j-1]
4. **Handle base case**: dp[0][0] = 1
5. **Handle traps**: Set dp[i][j] = 0 for trap cells

---

*This analysis shows how to efficiently solve grid-based path counting problems using dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Grid Paths with Diagonal Moves**
**Problem**: Allow diagonal moves (down-right) in addition to right and down.
```python
def grid_paths_with_diagonals(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case: starting position
    if grid[0][0] != '*':
        dp[0][0] = 1
    
    # Fill first row
    for j in range(1, n):
        if grid[0][j] != '*':
            dp[0][j] = dp[0][j-1]
    
    # Fill first column
    for i in range(1, n):
        if grid[i][0] != '*':
            dp[i][0] = dp[i-1][0]
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] != '*':
                dp[i][j] = (dp[i-1][j] + dp[i][j-1] + dp[i-1][j-1]) % MOD
    
    return dp[n-1][n-1]
```

#### **Variation 2: Grid Paths with Costs**
**Problem**: Each cell has a cost, find minimum cost path.
```python
def grid_paths_with_costs(n, grid, costs):
    # costs[i][j] = cost of cell (i,j)
    
    # dp[i][j] = minimum cost to reach (i,j)
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base case: starting position
    if grid[0][0] != '*':
        dp[0][0] = costs[0][0]
    
    # Fill first row
    for j in range(1, n):
        if grid[0][j] != '*':
            dp[0][j] = dp[0][j-1] + costs[0][j]
    
    # Fill first column
    for i in range(1, n):
        if grid[i][0] != '*':
            dp[i][0] = dp[i-1][0] + costs[i][0]
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] != '*':
                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + costs[i][j]
    
    return dp[n-1][n-1] if dp[n-1][n-1] != float('inf') else -1
```

#### **Variation 3: Grid Paths with Multiple Destinations**
**Problem**: Find paths to any of multiple destination cells.
```python
def grid_paths_multiple_destinations(n, grid, destinations):
    # destinations = list of (i,j) coordinates
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case: starting position
    if grid[0][0] != '*':
        dp[0][0] = 1
    
    # Fill first row
    for j in range(1, n):
        if grid[0][j] != '*':
            dp[0][j] = dp[0][j-1]
    
    # Fill first column
    for i in range(1, n):
        if grid[i][0] != '*':
            dp[i][0] = dp[i-1][0]
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] != '*':
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    # Sum paths to all destinations
    total_paths = 0
    for i, j in destinations:
        total_paths = (total_paths + dp[i][j]) % MOD
    
    return total_paths
```

#### **Variation 4: Grid Paths with Constraints**
**Problem**: Add constraints like maximum steps or specific patterns.
```python
def grid_paths_with_constraints(n, grid, max_steps):
    MOD = 10**9 + 7
    
    # dp[i][j][steps] = number of paths to (i,j) using exactly 'steps' moves
    dp = [[[0] * (max_steps + 1) for _ in range(n)] for _ in range(n)]
    
    # Base case: starting position
    if grid[0][0] != '*':
        dp[0][0][0] = 1
    
    # Fill DP table
    for steps in range(max_steps):
        for i in range(n):
            for j in range(n):
                if dp[i][j][steps] > 0:
                    # Move right
                    if j + 1 < n and grid[i][j+1] != '*':
                        dp[i][j+1][steps+1] = (dp[i][j+1][steps+1] + dp[i][j][steps]) % MOD
                    # Move down
                    if i + 1 < n and grid[i+1][j] != '*':
                        dp[i+1][j][steps+1] = (dp[i+1][j][steps+1] + dp[i][j][steps]) % MOD
    
    return dp[n-1][n-1][max_steps]
```

#### **Variation 5: Grid Paths with Probabilities**
**Problem**: Each move has a probability of success, find expected number of paths.
```python
def grid_paths_with_probabilities(n, grid, move_prob):
    # move_prob = probability of successful move
    
    # dp[i][j] = expected number of paths to (i,j)
    dp = [[0.0] * n for _ in range(n)]
    
    # Base case: starting position
    if grid[0][0] != '*':
        dp[0][0] = 1.0
    
    # Fill first row
    for j in range(1, n):
        if grid[0][j] != '*':
            dp[0][j] = dp[0][j-1] * move_prob
    
    # Fill first column
    for i in range(1, n):
        if grid[i][0] != '*':
            dp[i][0] = dp[i-1][0] * move_prob
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] != '*':
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) * move_prob
    
    return dp[n-1][n-1]
```

### 🔗 **Related Problems & Concepts**

#### **1. Grid Path Problems**
- **Unique Paths**: Count paths without obstacles
- **Unique Paths II**: Count paths with obstacles
- **Minimum Path Sum**: Find minimum cost path
- **Maximum Path Sum**: Find maximum value path

#### **2. Dynamic Programming Patterns**
- **2D DP**: Two state variables (row, column)
- **3D DP**: Three state variables (row, column, additional constraint)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Graph Theory**
- **Shortest Path**: Find shortest path in graph
- **Path Counting**: Count paths between vertices
- **Grid Graphs**: Special case of graphs
- **Directed Acyclic Graphs**: DAG path counting

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
    grid = [input().strip() for _ in range(n)]
    result = grid_paths_dp(n, grid)
    print(result)
```

#### **2. Range Queries on Grid Paths**
```python
def range_grid_path_queries(n, grid, queries):
    # Precompute for all subgrids
    dp = [[[0] * n for _ in range(n)] for _ in range(n)]
    
    # Fill DP for all possible subgrids
    for start_i in range(n):
        for start_j in range(n):
            for end_i in range(start_i, n):
                for end_j in range(start_j, n):
                    # Calculate paths for subgrid (start_i,start_j) to (end_i,end_j)
                    pass
    
    # Answer queries
    for start_i, start_j, end_i, end_j in queries:
        print(dp[start_i][start_j][end_i][end_j])
```

#### **3. Interactive Grid Problems**
```python
def interactive_grid_game():
    n = int(input("Enter grid size: "))
    grid = []
    for _ in range(n):
        row = input("Enter row: ")
        grid.append(row)
    
    print("Grid:")
    for row in grid:
        print(row)
    
    player_guess = int(input("Enter number of paths: "))
    actual_paths = grid_paths_dp(n, grid)
    
    if player_guess == actual_paths:
        print("Correct!")
    else:
        print(f"Wrong! Number of paths is {actual_paths}")
```

### 🧮 **Mathematical Extensions**

#### **1. Path Counting**
- **Catalan Numbers**: Count valid paths in grid
- **Combinatorial Paths**: Count paths with specific properties
- **Lattice Paths**: Paths in integer lattice
- **Dyck Paths**: Paths that never go below diagonal

#### **2. Advanced DP Techniques**
- **Digit DP**: Count paths with specific properties
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