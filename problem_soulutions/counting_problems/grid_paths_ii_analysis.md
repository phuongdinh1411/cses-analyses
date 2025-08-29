---
layout: simple
title: "Grid Paths II"
permalink: /cses-analyses/problem_soulutions/counting_problems/grid_paths_ii_analysis
---


# Grid Paths II

## Problem Statement
Given an n×n grid with some blocked cells, count the number of paths from the top-left corner to the bottom-right corner, moving only right or down.

### Input
The first input line has an integer n: the size of the grid.
Then there are n lines describing the grid. Each line has n characters: '.' for empty cell and '#' for blocked cell.

### Output
Print the number of valid paths modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 1000

### Example
```
Input:
3
...
.#.
...

Output:
2
```

## Solution Progression

### Approach 1: Recursive DFS - O(2^(n²))
**Description**: Use recursive DFS to explore all possible paths.

```python
def grid_paths_ii_naive(n, grid):
    MOD = 10**9 + 7
    
    def dfs(i, j):
        if i == n-1 and j == n-1:
            return 1
        
        if i >= n or j >= n or grid[i][j] == '#':
            return 0
        
        return (dfs(i+1, j) + dfs(i, j+1)) % MOD
    
    return dfs(0, 0)
```

**Why this is inefficient**: O(2^(n²)) complexity is too slow for large grids.

### Improvement 1: Dynamic Programming - O(n²)
**Description**: Use DP to avoid recalculating subproblems.

```python
def grid_paths_ii_dp(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case
    if grid[0][0] != '#':
        dp[0][0] = 1
    
    # Fill first row
    for j in range(1, n):
        if grid[0][j] != '#':
            dp[0][j] = dp[0][j-1]
    
    # Fill first column
    for i in range(1, n):
        if grid[i][0] != '#':
            dp[i][0] = dp[i-1][0]
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] != '#':
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]
```

**Why this improvement works**: DP avoids recalculating subproblems, reducing complexity to O(n²).

### Approach 2: Optimized DP - O(n²)
**Description**: Optimize DP with better implementation.

```python
def grid_paths_ii_optimized(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case
    if grid[0][0] != '#':
        dp[0][0] = 1
    
    # Fill the grid
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '#':
                continue
            
            # Add paths from above
            if i > 0:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            
            # Add paths from left
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]
```

**Why this improvement works**: Simplified DP implementation with better readability.

## Final Optimal Solution

```python
n = int(input())
grid = []
for _ in range(n):
    row = input().strip()
    grid.append(row)

def count_grid_paths(n, grid):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of paths from (0,0) to (i,j)
    dp = [[0] * n for _ in range(n)]
    
    # Base case
    if grid[0][0] != '#':
        dp[0][0] = 1
    
    # Fill the grid
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '#':
                continue
            
            # Add paths from above
            if i > 0:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            
            # Add paths from left
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]

result = count_grid_paths(n, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive DFS | O(2^(n²)) | O(n²) | Simple but exponential |
| Dynamic Programming | O(n²) | O(n²) | DP avoids recalculation |
| Optimized DP | O(n²) | O(n²) | Simplified implementation |

## Key Insights for Other Problems

### 1. **Grid Path Counting**
**Principle**: Use dynamic programming to count paths in grids efficiently.
**Applicable to**: Grid problems, path counting problems, DP problems

### 2. **Blocked Cell Handling**
**Principle**: Skip blocked cells in DP calculations.
**Applicable to**: Constraint satisfaction problems, grid optimization problems

### 3. **Modular Arithmetic**
**Principle**: Use modular arithmetic to handle large numbers in counting problems.
**Applicable to**: Large number problems, counting problems, combinatorics problems

## Notable Techniques

### 1. **Grid DP Implementation**
```python
def grid_dp_paths(n, grid, MOD):
    dp = [[0] * n for _ in range(n)]
    
    # Base case
    if grid[0][0] != '#':
        dp[0][0] = 1
    
    # Fill grid
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '#':
                continue
            
            if i > 0:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][n-1]
```

### 2. **Blocked Cell Handling**
```python
def handle_blocked_cells(grid, i, j):
    if grid[i][j] == '#':
        return 0
    return 1
```

### 3. **Path Counting Formula**
```python
def path_counting_formula(dp, i, j, MOD):
    count = 0
    if i > 0:
        count = (count + dp[i-1][j]) % MOD
    if j > 0:
        count = (count + dp[i][j-1]) % MOD
    return count
```

## Problem-Solving Framework

1. **Identify problem type**: This is a grid path counting problem with blocked cells
2. **Choose approach**: Use dynamic programming
3. **Initialize DP table**: Create 2D DP array
4. **Handle base case**: Set starting position
5. **Fill DP table**: Calculate paths for each cell
6. **Handle blocked cells**: Skip blocked cells in calculations
7. **Return result**: Output number of paths to bottom-right corner

---

*This analysis shows how to efficiently count grid paths using dynamic programming with state compression and memoization for large grids.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Grid Paths**
**Problem**: Each cell has a weight. Find paths with maximum total weight.
```python
def weighted_grid_paths(n, m, weights, MOD=10**9+7):
    # weights[i][j] = weight of cell (i, j)
    dp = [[0] * m for _ in range(n)]
    dp[0][0] = weights[0][0]
    
    # Fill first row
    for j in range(1, m):
        dp[0][j] = (dp[0][j-1] + weights[0][j]) % MOD
    
    # Fill first column
    for i in range(1, n):
        dp[i][0] = (dp[i-1][0] + weights[i][0]) % MOD
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = (dp[i-1][j] + dp[i][j-1] + weights[i][j]) % MOD
    
    return dp[n-1][m-1]
```

#### **Variation 2: Constrained Grid Paths**
**Problem**: Find paths that avoid certain cells or follow specific constraints.
```python
def constrained_grid_paths(n, m, blocked_cells, MOD=10**9+7):
    # blocked_cells = set of (i, j) coordinates that cannot be visited
    dp = [[0] * m for _ in range(n)]
    
    # Check if start is blocked
    if (0, 0) not in blocked_cells:
        dp[0][0] = 1
    
    # Fill first row
    for j in range(1, m):
        if (0, j) not in blocked_cells:
            dp[0][j] = dp[0][j-1]
    
    # Fill first column
    for i in range(1, n):
        if (i, 0) not in blocked_cells:
            dp[i][0] = dp[i-1][0]
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, m):
            if (i, j) not in blocked_cells:
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][m-1]
```

#### **Variation 3: Diagonal Grid Paths**
**Problem**: Allow diagonal moves in addition to right and down.
```python
def diagonal_grid_paths(n, m, MOD=10**9+7):
    dp = [[0] * m for _ in range(n)]
    dp[0][0] = 1
    
    # Fill first row
    for j in range(1, m):
        dp[0][j] = dp[0][j-1]
    
    # Fill first column
    for i in range(1, n):
        dp[i][0] = dp[i-1][0]
    
    # Fill rest of the grid with diagonal moves
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = (dp[i-1][j] + dp[i][j-1] + dp[i-1][j-1]) % MOD
    
    return dp[n-1][m-1]
```

#### **Variation 4: Circular Grid Paths**
**Problem**: Handle a circular grid where edges wrap around.
```python
def circular_grid_paths(n, m, MOD=10**9+7):
    dp = [[0] * m for _ in range(n)]
    dp[0][0] = 1
    
    # Fill first row with circular wrapping
    for j in range(1, m):
        dp[0][j] = dp[0][j-1]
    # Add wrap-around from last column to first
    dp[0][0] = (dp[0][0] + dp[0][m-1]) % MOD
    
    # Fill first column with circular wrapping
    for i in range(1, n):
        dp[i][0] = dp[i-1][0]
    # Add wrap-around from last row to first
    dp[0][0] = (dp[0][0] + dp[n-1][0]) % MOD
    
    # Fill rest of the grid
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    return dp[n-1][m-1]
```

#### **Variation 5: Dynamic Grid Path Updates**
**Problem**: Support dynamic updates to blocked cells and answer path queries efficiently.
```python
class DynamicGridPathCounter:
    def __init__(self, n, m, MOD=10**9+7):
        self.n = n
        self.m = m
        self.MOD = MOD
        self.blocked_cells = set()
        self.dp = None
        self._compute_paths()
    
    def add_blocked_cell(self, i, j):
        self.blocked_cells.add((i, j))
        self._compute_paths()
    
    def remove_blocked_cell(self, i, j):
        if (i, j) in self.blocked_cells:
            self.blocked_cells.remove((i, j))
            self._compute_paths()
    
    def _compute_paths(self):
        self.dp = [[0] * self.m for _ in range(self.n)]
        
        # Check if start is blocked
        if (0, 0) not in self.blocked_cells:
            self.dp[0][0] = 1
        
        # Fill first row
        for j in range(1, self.m):
            if (0, j) not in self.blocked_cells:
                self.dp[0][j] = self.dp[0][j-1]
        
        # Fill first column
        for i in range(1, self.n):
            if (i, 0) not in self.blocked_cells:
                self.dp[i][0] = self.dp[i-1][0]
        
        # Fill rest of the grid
        for i in range(1, self.n):
            for j in range(1, self.m):
                if (i, j) not in self.blocked_cells:
                    self.dp[i][j] = (self.dp[i-1][j] + self.dp[i][j-1]) % self.MOD
    
    def get_path_count(self):
        return self.dp[self.n-1][self.m-1]
```

### 🔗 **Related Problems & Concepts**

#### **1. Grid Problems**
- **Grid Traversal**: Traverse grids efficiently
- **Grid Paths**: Find paths in grids
- **Grid Patterns**: Find patterns in grids
- **Grid Optimization**: Optimize grid operations

#### **2. Path Problems**
- **Path Counting**: Count paths efficiently
- **Path Generation**: Generate paths
- **Path Optimization**: Optimize path algorithms
- **Path Analysis**: Analyze path properties

#### **3. Dynamic Programming Problems**
- **DP Optimization**: Optimize dynamic programming
- **DP State Management**: Manage DP states efficiently
- **DP Transitions**: Design DP transitions
- **DP Analysis**: Analyze DP algorithms

#### **4. Constraint Problems**
- **Constraint Satisfaction**: Satisfy constraints efficiently
- **Constraint Optimization**: Optimize constraint algorithms
- **Constraint Analysis**: Analyze constraint properties
- **Constraint Relaxation**: Relax constraints when needed

#### **5. Counting Problems**
- **Counting Algorithms**: Efficient counting algorithms
- **Counting Optimization**: Optimize counting operations
- **Counting Analysis**: Analyze counting properties
- **Counting Techniques**: Various counting techniques

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    
    result = count_grid_paths(n, m)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute paths for different grid regions
def precompute_paths(max_n, max_m, MOD=10**9+7):
    dp = [[0] * (max_m + 1) for _ in range(max_n + 1)]
    
    # Base case
    dp[0][0] = 1
    
    # Fill DP table
    for i in range(max_n + 1):
        for j in range(max_m + 1):
            if i == 0 and j == 0:
                continue
            if i > 0:
                dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
            if j > 0:
                dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    return dp

# Answer range queries efficiently
def range_query(dp, n, m):
    return dp[n][m]
```

#### **3. Interactive Problems**
```python
# Interactive grid path analyzer
def interactive_grid_path_analyzer():
    n = int(input("Enter grid height: "))
    m = int(input("Enter grid width: "))
    
    print(f"Grid size: {n}x{m}")
    
    while True:
        query = input("Enter query (paths/weighted/constrained/diagonal/circular/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "paths":
            result = count_grid_paths(n, m)
            print(f"Grid paths: {result}")
        elif query == "weighted":
            weights = []
            print("Enter weight matrix:")
            for i in range(n):
                row = list(map(int, input(f"Weight row {i+1}: ").split()))
                weights.append(row)
            result = weighted_grid_paths(n, m, weights)
            print(f"Weighted paths: {result}")
        elif query == "constrained":
            blocked_cells = set()
            num_blocked = int(input("Enter number of blocked cells: "))
            print("Enter blocked cell coordinates:")
            for _ in range(num_blocked):
                i, j = map(int, input().split())
                blocked_cells.add((i, j))
            result = constrained_grid_paths(n, m, blocked_cells)
            print(f"Constrained paths: {result}")
        elif query == "diagonal":
            result = diagonal_grid_paths(n, m)
            print(f"Diagonal paths: {result}")
        elif query == "circular":
            result = circular_grid_paths(n, m)
            print(f"Circular paths: {result}")
        elif query == "dynamic":
            counter = DynamicGridPathCounter(n, m)
            print(f"Initial paths: {counter.get_path_count()}")
            
            while True:
                cmd = input("Enter command (add/remove/count/back): ")
                if cmd == "back":
                    break
                elif cmd == "add":
                    i, j = map(int, input("Enter blocked cell coordinates: ").split())
                    counter.add_blocked_cell(i, j)
                    print("Cell blocked")
                elif cmd == "remove":
                    i, j = map(int, input("Enter unblocked cell coordinates: ").split())
                    counter.remove_blocked_cell(i, j)
                    print("Cell unblocked")
                elif cmd == "count":
                    result = counter.get_path_count()
                    print(f"Current paths: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Path Combinations**: Count path combinations
- **Grid Arrangements**: Arrange paths in grids
- **Pattern Partitions**: Partition grids into patterns
- **Inclusion-Exclusion**: Count using inclusion-exclusion

#### **2. Number Theory**
- **Grid Patterns**: Mathematical patterns in grids
- **Path Sequences**: Sequences of path counts
- **Modular Arithmetic**: Grid operations with modular arithmetic
- **Number Sequences**: Sequences in grid counting

#### **3. Optimization Theory**
- **Grid Optimization**: Optimize grid operations
- **Path Optimization**: Optimize path algorithms
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Dynamic Programming**: Efficient DP algorithms
- **Grid Traversal**: Grid traversal algorithms
- **Path Finding**: Path finding algorithms
- **Constraint Satisfaction**: Constraint satisfaction algorithms

#### **2. Mathematical Concepts**
- **Combinatorics**: Foundation for counting problems
- **Grid Theory**: Mathematical properties of grids
- **Path Theory**: Properties of paths
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Grid Processing**: Efficient grid processing techniques
- **Path Analysis**: Path analysis techniques

---

*This analysis demonstrates efficient grid path counting techniques and shows various extensions for grid and path problems.* 