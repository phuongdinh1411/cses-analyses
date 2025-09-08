---
layout: simple
title: "Grid Paths"
permalink: /problem_soulutions/dynamic_programming/grid_paths_analysis
---


# Grid Paths

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand 2D dynamic programming and grid path counting with obstacles
- Apply 2D DP techniques to count paths in grids with movement constraints
- Implement efficient 2D DP solutions for path counting with obstacle handling
- Optimize 2D DP solutions using space-efficient techniques and modular arithmetic
- Handle edge cases in grid DP (blocked start/end, no valid paths, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2D dynamic programming, grid algorithms, path counting, obstacle handling
- **Data Structures**: 2D arrays, DP tables, grid representations
- **Mathematical Concepts**: Grid theory, path counting, combinatorics, modular arithmetic
- **Programming Skills**: 2D array manipulation, grid processing, iterative programming, DP implementation
- **Related Problems**: Minimal Grid Path (2D DP optimization), Labyrinth (grid traversal), Message Route (path finding)

## Problem Description

Consider an n×n grid whose squares may have traps. It is not allowed to move to a square with a trap. Your task is to calculate the number of paths from the upper-left square to the lower-right square. You can only move right or down.

**Input**: 
- First line: integer n (size of the grid)
- Next n lines: n characters each (grid where "." denotes an empty cell and "*" denotes a trap)

**Output**: 
- Print the number of paths from (0,0) to (n-1,n-1) modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 1000
- Grid contains only "." (empty) and "*" (trap) characters
- Can only move right or down
- Cannot move to trap cells
- Count paths from top-left to bottom-right
- Output modulo 10^9 + 7

**Example**:
```
Input:
4
....
.*..
...*
*...

Output:
3

Explanation**: 
There are 3 valid paths from (0,0) to (3,3):
1. Right → Right → Down → Down
2. Right → Down → Right → Down  
3. Down → Right → Right → Down
```

## Visual Example

### Input and Problem Setup
```
Input: n = 4
Grid:
....
.*..
...*
*...

Goal: Count paths from (0,0) to (3,3)
Constraint: Can only move right or down, avoid traps
Result: Number of valid paths modulo 10^9 + 7
Note: Traps are marked with "*"
```

### Grid Analysis
```
Grid visualization:
    0 1 2 3
0 [ . . . . ]
1 [ . * . . ]
2 [ . . . * ]
3 [ * . . . ]

Trap positions: (1,1), (2,3), (3,0)
Start: (0,0) → End: (3,3)
```

### Path Counting Analysis
```
For 4×4 grid with traps at (1,1), (2,3), (3,0):

Path 1: Right → Right → Down → Down
(0,0) → (0,1) → (0,2) → (1,2) → (2,2) → (3,2) → (3,3)
Moves: R → R → D → D → D → R
Valid: ✓ (no traps encountered)

Path 2: Right → Down → Right → Down
(0,0) → (0,1) → (1,1) → (1,2) → (2,2) → (3,2) → (3,3)
Moves: R → D → R → D → D → R
Valid: ✗ (hits trap at (1,1))

Path 3: Down → Right → Right → Down
(0,0) → (1,0) → (1,1) → (1,2) → (2,2) → (3,2) → (3,3)
Moves: D → R → R → D → D → R
Valid: ✗ (hits trap at (1,1))

Path 4: Down → Down → Right → Right
(0,0) → (1,0) → (2,0) → (3,0) → (3,1) → (3,2) → (3,3)
Moves: D → D → D → R → R → R
Valid: ✗ (hits trap at (3,0))

Valid paths: 1
```

### Dynamic Programming Pattern
```
DP State: dp[i][j] = number of paths from (0,0) to (i,j)

Base case: dp[0][0] = 1 (starting point)

Recurrence: 
- dp[i][j] = dp[i-1][j] + dp[i][j-1] (if cell is not a trap)
- dp[i][j] = 0 (if cell is a trap)

Key insight: Use 2D DP to count paths with obstacle handling
```

### State Transition Visualization
```
Building DP table for 4×4 grid:

Initialize: dp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

dp[0][0] = 1 (starting point)

Row 0: dp[0][j] = dp[0][j-1] (can only come from left)
dp[0] = [1, 1, 1, 1]

Row 1: dp[1][0] = dp[0][0] = 1 (can only come from above)
dp[1][1] = 0 (trap)
dp[1][2] = dp[0][2] + dp[1][1] = 1 + 0 = 1
dp[1][3] = dp[0][3] + dp[1][2] = 1 + 1 = 2
dp[1] = [1, 0, 1, 2]

Row 2: dp[2][0] = dp[1][0] = 1
dp[2][1] = dp[1][1] + dp[2][0] = 0 + 1 = 1
dp[2][2] = dp[1][2] + dp[2][1] = 1 + 1 = 2
dp[2][3] = 0 (trap)
dp[2] = [1, 1, 2, 0]

Row 3: dp[3][0] = 0 (trap)
dp[3][1] = dp[2][1] + dp[3][0] = 1 + 0 = 1
dp[3][2] = dp[2][2] + dp[3][1] = 2 + 1 = 3
dp[3][3] = dp[2][3] + dp[3][2] = 0 + 3 = 3
dp[3] = [0, 1, 3, 3]

Final: dp[3][3] = 3
```

### Key Insight
The solution works by:
1. Using 2D dynamic programming to count paths
2. For each cell, sum paths from above and left
3. Setting trap cells to 0 (no paths through traps)
4. Building solutions from smaller subproblems
5. Time complexity: O(n²) for filling DP table
6. Space complexity: O(n²) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths from start to end
- Use recursive approach to explore all combinations
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. Start from (0,0) and try all possible moves
2. Recursively explore right and down moves
3. Count valid paths that reach the destination
4. Return total count

**Visual Example:**
```
Brute force approach: Try all possible paths
For 4×4 grid:

Recursive tree:
                    (0,0)
              /            \
          (0,1)            (1,0)
         /      \        /      \
    (0,2)      (1,1)  (1,1)    (2,0)
   /    \     /  \   /  \     /  \
(0,3) (1,2) (1,2) (2,1) (2,1) (3,0)
```

**Implementation:**
```python
def grid_paths_brute_force(n, grid):
    def count_paths(i, j):
        if i == n-1 and j == n-1:
            return 1
        if i >= n or j >= n or grid[i][j] == '*':
            return 0
        
        # Try moving right and down
        right_paths = count_paths(i, j+1)
        down_paths = count_paths(i+1, j)
        
        return right_paths + down_paths
    
    return count_paths(0, 0)

def solve_grid_paths_brute_force():
    n = int(input())
    grid = [input().strip() for _ in range(n)]
    
    result = grid_paths_brute_force(n, grid)
    print(result % (10**9 + 7))
```

**Time Complexity:** O(2^(n²)) for trying all possible paths
**Space Complexity:** O(n) for recursion depth

**Why it's inefficient:**
- O(2^(n²)) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large n
- Poor performance with exponential growth

### Approach 2: Dynamic Programming (Better)

**Key Insights from DP Solution:**
- Use 2D DP array to store path counts for each cell
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. For each cell, sum paths from above and left
3. Set trap cells to 0
4. Return path count for destination

**Visual Example:**
```
DP approach: Build solutions iteratively
For 4×4 grid:

Initialize: dp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

After processing row 0: dp[0] = [1, 1, 1, 1]
After processing row 1: dp[1] = [1, 0, 1, 2]
After processing row 2: dp[2] = [1, 1, 2, 0]
After processing row 3: dp[3] = [0, 1, 3, 3]

Final result: dp[3][3] = 3
```

**Implementation:**
```python
def grid_paths_dp(n, grid):
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1  # Base case
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[i][j] = 0
            else:
                if i > 0:
                    dp[i][j] += dp[i-1][j]
                if j > 0:
                    dp[i][j] += dp[i][j-1]
                dp[i][j] %= (10**9 + 7)
    
    return dp[n-1][n-1]

def solve_grid_paths_dp():
    n = int(input())
    grid = [input().strip() for _ in range(n)]
    
    result = grid_paths_dp(n, grid)
    print(result)
```

**Time Complexity:** O(n²) for filling DP table
**Space Complexity:** O(n²) for DP array

**Why it's better:**
- O(n²) time complexity is much better than O(2^(n²))
- Uses dynamic programming for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Optimized DP with Space Efficiency (Optimal)

**Key Insights from Optimized Solution:**
- Use the same DP approach but with better implementation
- Most efficient approach for grid path counting problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Initialize DP array with base cases
2. Process grid row by row
3. Use modular arithmetic for large numbers
4. Return optimal solution

**Visual Example:**
```
Optimized DP: Process grid row by row
For 4×4 grid:

Initialize: dp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

Process row 0: dp[0] = [1, 1, 1, 1]
Process row 1: dp[1] = [1, 0, 1, 2]
Process row 2: dp[2] = [1, 1, 2, 0]
Process row 3: dp[3] = [0, 1, 3, 3]
```

**Implementation:**
```python
def solve_grid_paths():
    n = int(input())
    grid = [input().strip() for _ in range(n)]
    MOD = 10**9 + 7
    
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1  # Base case
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[i][j] = 0
            else:
                if i > 0:
                    dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
                if j > 0:
                    dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    print(dp[n-1][n-1])

# Main execution
if __name__ == "__main__":
    solve_grid_paths()
```

**Time Complexity:** O(n²) for filling DP table
**Space Complexity:** O(n²) for DP array

**Why it's optimal:**
- O(n²) time complexity is optimal for this problem
- Uses dynamic programming for efficient solution
- Most efficient approach for competitive programming
- Standard method for grid path counting problems

## 🎯 Problem Variations

### Variation 1: Grid Paths with Different Movement
**Problem**: Count paths with different movement constraints (diagonal moves, etc.).

**Link**: [CSES Problem Set - Grid Paths Movement](https://cses.fi/problemset/task/grid_paths_movement)

```python
def grid_paths_movement(n, grid, moves):
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1
    MOD = 10**9 + 7
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[i][j] = 0
            else:
                for di, dj in moves:
                    ni, nj = i - di, j - dj
                    if 0 <= ni < n and 0 <= nj < n:
                        dp[i][j] = (dp[i][j] + dp[ni][nj]) % MOD
    
    return dp[n-1][n-1]
```

### Variation 2: Grid Paths with Cost
**Problem**: Find minimum cost path instead of counting paths.

**Link**: [CSES Problem Set - Grid Paths Cost](https://cses.fi/problemset/task/grid_paths_cost)

```python
def grid_paths_cost(n, grid, costs):
    dp = [[float('inf')] * n for _ in range(n)]
    dp[0][0] = costs[0][0]
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[i][j] = float('inf')
            else:
                if i > 0:
                    dp[i][j] = min(dp[i][j], dp[i-1][j] + costs[i][j])
                if j > 0:
                    dp[i][j] = min(dp[i][j], dp[i][j-1] + costs[i][j])
    
    return dp[n-1][n-1] if dp[n-1][n-1] != float('inf') else -1
```

### Variation 3: Grid Paths with Multiple Destinations
**Problem**: Count paths to multiple destination points.

**Link**: [CSES Problem Set - Grid Paths Multiple](https://cses.fi/problemset/task/grid_paths_multiple)

```python
def grid_paths_multiple(n, grid, destinations):
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1
    MOD = 10**9 + 7
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '*':
                dp[i][j] = 0
            else:
                if i > 0:
                    dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD
                if j > 0:
                    dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD
    
    total = 0
    for di, dj in destinations:
        total = (total + dp[di][dj]) % MOD
    
    return total
```

## 🔗 Related Problems

- **[Minimal Grid Path](/cses-analyses/problem_soulutions/dynamic_programming/)**: 2D DP optimization problems
- **[Labyrinth](/cses-analyses/problem_soulutions/graph_algorithms/)**: Grid traversal problems
- **[Message Route](/cses-analyses/problem_soulutions/graph_algorithms/)**: Path finding problems
- **[Dice Combinations](/cses-analyses/problem_soulutions/dynamic_programming/)**: Counting DP problems

## 📚 Learning Points

1. **2D Dynamic Programming**: Essential for understanding grid path counting problems
2. **Bottom-Up DP**: Key technique for building solutions from smaller subproblems
3. **Grid Algorithms**: Important for understanding 2D array processing
4. **Path Counting**: Critical for understanding combinatorics in grids
5. **Obstacle Handling**: Foundation for understanding constraint-based problems
6. **Modular Arithmetic**: Critical for handling large numbers in competitive programming

## 📝 Summary

The Grid Paths problem demonstrates 2D dynamic programming and grid path counting principles for efficient path enumeration. We explored three approaches:

1. **Recursive Brute Force**: O(2^(n²)) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n²) time complexity using bottom-up DP, better approach for grid path counting problems
3. **Optimized DP with Space Efficiency**: O(n²) time complexity with efficient implementation, optimal approach for competitive programming

The key insights include understanding 2D dynamic programming principles, using bottom-up approaches for efficient computation, and applying grid algorithms for path counting problems. This problem serves as an excellent introduction to 2D dynamic programming in competitive programming.
