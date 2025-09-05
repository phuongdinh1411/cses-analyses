---
layout: simple
title: "Minimal Grid Path"
permalink: /problem_soulutions/dynamic_programming/minimal_grid_path_analysis
---


# Minimal Grid Path

## Problem Description

**Problem**: Given an n×n grid, find the minimum cost path from the top-left corner to the bottom-right corner. You can only move right or down, and each cell has a cost.

**Input**: 
- n: size of the grid
- grid: n×n grid with costs for each cell

**Output**: Minimum cost of a path from top-left to bottom-right.

**Example**:
```
Input:
3
1 2 3
4 5 6
7 8 9

Output:
21

Explanation: 
The minimum cost path is: 1 → 2 → 6 → 9 = 1 + 2 + 6 + 9 = 18
Wait, let me recalculate: 1 → 2 → 3 → 6 → 9 = 1 + 2 + 3 + 6 + 9 = 21
Actually, the optimal path is: 1 → 2 → 3 → 6 → 9 = 21
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

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_minimal_grid_path():
    n = int(input())
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # dp[i][j] = minimum cost to reach (i,j) from destination
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
    
    print(dp[0][0])

# Main execution
if __name__ == "__main__":
    solve_minimal_grid_path()
```

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 21),
        (2, [[1, 2], [3, 4]], 7),
        (1, [[5]], 5),
        (2, [[1, 1], [1, 1]], 3),
    ]
    
    for n, grid, expected in test_cases:
        result = solve_test(n, grid)
        print(f"n={n}, grid={grid}, expected={expected}, result={result}")
        assert result == expected, f"Failed for n={n}, grid={grid}"
        print("✓ Passed")
        print()

def solve_test(n, grid):
    # dp[i][j] = minimum cost to reach (i,j) from destination
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n²) - we fill a 2D DP table
- **Space**: O(n²) - we store the entire DP table

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes minimum cost paths using optimal substructure
- **State Transition**: dp[i][j] = grid[i][j] + min(dp[i+1][j], dp[i][j+1])
- **Base Case**: dp[n-1][n-1] = grid[n-1][n-1]
- **Optimal Substructure**: Optimal solution can be built from smaller subproblems

## 🎨 Visual Example

### Input Example
```
Grid (3×3):
1 2 3
4 5 6
7 8 9
```

### All Possible Paths
```
Grid: [1, 2, 3]
      [4, 5, 6]
      [7, 8, 9]

All possible paths from (0,0) to (2,2):
Path 1: 1 → 2 → 3 → 6 → 9 = 1 + 2 + 3 + 6 + 9 = 21
Path 2: 1 → 2 → 5 → 6 → 9 = 1 + 2 + 5 + 6 + 9 = 23
Path 3: 1 → 2 → 5 → 8 → 9 = 1 + 2 + 5 + 8 + 9 = 25
Path 4: 1 → 4 → 5 → 6 → 9 = 1 + 4 + 5 + 6 + 9 = 25
Path 5: 1 → 4 → 5 → 8 → 9 = 1 + 4 + 5 + 8 + 9 = 27
Path 6: 1 → 4 → 7 → 8 → 9 = 1 + 4 + 7 + 8 + 9 = 29

Minimum cost: 21 (Path 1)
```

### DP Table Construction
```
Grid: [1, 2, 3]
      [4, 5, 6]
      [7, 8, 9]

DP Table (bottom-up approach):
Step 1: Initialize base case
dp[2][2] = grid[2][2] = 9

Step 2: Fill last row (can only move right)
dp[2][1] = grid[2][1] + dp[2][2] = 8 + 9 = 17
dp[2][0] = grid[2][0] + dp[2][1] = 7 + 17 = 24

Step 3: Fill last column (can only move down)
dp[1][2] = grid[1][2] + dp[2][2] = 6 + 9 = 15
dp[0][2] = grid[0][2] + dp[1][2] = 3 + 15 = 18

Step 4: Fill remaining cells
dp[1][1] = grid[1][1] + min(dp[2][1], dp[1][2]) = 5 + min(17, 15) = 5 + 15 = 20
dp[1][0] = grid[1][0] + min(dp[2][0], dp[1][1]) = 4 + min(24, 20) = 4 + 20 = 24
dp[0][1] = grid[0][1] + min(dp[1][1], dp[0][2]) = 2 + min(20, 18) = 2 + 18 = 20
dp[0][0] = grid[0][0] + min(dp[1][0], dp[0][1]) = 1 + min(24, 20) = 1 + 20 = 21

Final DP Table:
[21, 20, 18]
[24, 20, 15]
[24, 17,  9]
```

### Step-by-Step DP Process
```
Grid: [1, 2, 3]
      [4, 5, 6]
      [7, 8, 9]

Step 1: Base case
dp[2][2] = 9

Step 2: Last row
dp[2][1] = 8 + 9 = 17
dp[2][0] = 7 + 17 = 24

Step 3: Last column
dp[1][2] = 6 + 9 = 15
dp[0][2] = 3 + 15 = 18

Step 4: Middle cells
dp[1][1] = 5 + min(17, 15) = 5 + 15 = 20
dp[1][0] = 4 + min(24, 20) = 4 + 20 = 24
dp[0][1] = 2 + min(20, 18) = 2 + 18 = 20
dp[0][0] = 1 + min(24, 20) = 1 + 20 = 21
```

### Visual DP Table
```
Grid:      DP Table:
[1, 2, 3]  [21, 20, 18]
[4, 5, 6]  [24, 20, 15]
[7, 8, 9]  [24, 17,  9]

Each cell shows minimum cost to reach (2,2) from that position
```

### Optimal Path Reconstruction
```
Starting from dp[0][0] = 21:
- Current: (0,0), cost = 21
- Next: min(dp[1][0]=24, dp[0][1]=20) → choose (0,1)
- Current: (0,1), cost = 20
- Next: min(dp[1][1]=20, dp[0][2]=18) → choose (0,2)
- Current: (0,2), cost = 18
- Next: min(dp[1][2]=15, dp[0][3]=∞) → choose (1,2)
- Current: (1,2), cost = 15
- Next: min(dp[2][2]=9, dp[1][3]=∞) → choose (2,2)
- Current: (2,2), cost = 9

Optimal path: (0,0) → (0,1) → (0,2) → (1,2) → (2,2)
Values: 1 → 2 → 3 → 6 → 9
Total cost: 1 + 2 + 3 + 6 + 9 = 21
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(2^(n²))    │ O(n²)        │ Try all      │
│                 │              │              │ paths        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Memoized        │ O(n²)        │ O(n²)        │ Cache        │
│ Recursion       │              │              │ results      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bottom-up DP    │ O(n²)        │ O(n²)        │ Build from   │
│                 │              │              │ base cases   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Space-optimized │ O(n²)        │ O(n)         │ Use only     │
│ DP              │              │              │ current row  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Minimal Grid Path Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: grid     │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize DP   │
              │ table           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Set base case:  │
              │ dp[n-1][n-1] =  │
              │ grid[n-1][n-1]  │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Fill last row   │
              │ and column      │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each cell   │
              │ (i,j):          │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ dp[i][j] =      │
              │ grid[i][j] +    │
              │ min(dp[i+1][j], │
              │ dp[i][j+1])     │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return dp[0][0] │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Dynamic Programming for Grid Problems**
- Find optimal substructure in grid problems
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **2D DP Table**
- Use 2D table for grid positions
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Minimum Cost Path**
- Find optimal paths in geometric structures
- Important for understanding
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Minimal Grid Path with Different Movement Rules
**Problem**: Allow diagonal movement or more directions.

```python
def minimal_grid_path_with_diagonals(n, grid):
    # dp[i][j] = minimum cost to reach (i,j) from destination
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
            
            # Can move diagonally
            if i + 1 < n and j + 1 < n:
                dp[i][j] = min(dp[i][j], dp[i+1][j+1])
            
            dp[i][j] += grid[i][j]
    
    return dp[0][0]

# Example usage
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = minimal_grid_path_with_diagonals(3, grid)
print(f"Minimal path with diagonals: {result}")
```

### Variation 2: Minimal Grid Path with Obstacles
**Problem**: Some cells are blocked and cannot be traversed.

```python
def minimal_grid_path_with_obstacles(n, grid, obstacles):
    # dp[i][j] = minimum cost to reach (i,j) from destination
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base case
    if (n-1, n-1) not in obstacles:
        dp[n-1][n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if (i, j) in obstacles:
                continue
            
            if i == n-1 and j == n-1:
                continue
            
            # Can move right
            if j + 1 < n and (i, j+1) not in obstacles:
                dp[i][j] = min(dp[i][j], dp[i][j+1])
            
            # Can move down
            if i + 1 < n and (i+1, j) not in obstacles:
                dp[i][j] = min(dp[i][j], dp[i+1][j])
            
            if dp[i][j] != float('inf'):
                dp[i][j] += grid[i][j]
    
    return dp[0][0] if dp[0][0] != float('inf') else -1

# Example usage
obstacles = {(1, 1)}  # Cell (1,1) is blocked
result = minimal_grid_path_with_obstacles(3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], obstacles)
print(f"Minimal path with obstacles: {result}")
```

### Variation 3: Minimal Grid Path with Multiple Destinations
**Problem**: Find minimum cost paths to multiple destination points.

```python
def minimal_grid_path_multiple_destinations(n, grid, destinations):
    # dp[i][j] = minimum cost to reach (i,j) from any destination
    dp = [[float('inf')] * n for _ in range(n)]
    
    # Base cases: all destinations
    for dest_i, dest_j in destinations:
        dp[dest_i][dest_j] = grid[dest_i][dest_j]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
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
    
    return dp[0][0] if dp[0][0] != float('inf') else -1

# Example usage
destinations = [(1, 1), (2, 2)]
result = minimal_grid_path_multiple_destinations(3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], destinations)
print(f"Minimal path to multiple destinations: {result}")
```

### Variation 4: Minimal Grid Path with Step Constraints
**Problem**: Find minimum cost path with maximum number of steps.

```python
def minimal_grid_path_with_steps(n, grid, max_steps):
    # dp[i][j][k] = minimum cost to reach (i,j) in exactly k steps
    dp = [[[float('inf')] * (max_steps + 1) for _ in range(n)] for _ in range(n)]
    
    # Base case: starting position
    dp[0][0][0] = grid[0][0]
    
    # Fill DP table
    for step in range(max_steps):
        for i in range(n):
            for j in range(n):
                if dp[i][j][step] != float('inf'):
                    # Move right
                    if j + 1 < n:
                        dp[i][j+1][step+1] = min(dp[i][j+1][step+1], dp[i][j][step] + grid[i][j+1])
                    
                    # Move down
                    if i + 1 < n:
                        dp[i+1][j][step+1] = min(dp[i+1][j][step+1], dp[i][j][step] + grid[i+1][j])
    
    return dp[n-1][n-1][max_steps] if dp[n-1][n-1][max_steps] != float('inf') else -1

# Example usage
result = minimal_grid_path_with_steps(3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 4)
print(f"Minimal path with step constraint: {result}")
```

### Variation 5: Minimal Grid Path with Dynamic Programming Optimization
**Problem**: Optimize the DP solution for better performance.

```python
def optimized_minimal_grid_path(n, grid):
    # Use 1D DP array to save space
    dp = [float('inf')] * n
    
    # Base case: last row
    dp[n-1] = grid[n-1][n-1]
    
    # Fill from bottom-right to top-left
    for i in range(n-1, -1, -1):
        new_dp = [float('inf')] * n
        
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                new_dp[j] = grid[i][j]
                continue
            
            # Can move right
            if j + 1 < n:
                new_dp[j] = min(new_dp[j], new_dp[j+1])
            
            # Can move down
            if i + 1 < n:
                new_dp[j] = min(new_dp[j], dp[j])
            
            if new_dp[j] != float('inf'):
                new_dp[j] += grid[i][j]
        
        dp = new_dp
    
    return dp[0]

# Example usage
result = optimized_minimal_grid_path(3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"Optimized minimal path: {result}")
```

## 🔗 Related Problems

- **[Dynamic Programming Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar DP problems
- **[Grid Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar grid problems
- **[Path Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: General path problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for grid path optimization problems
2. **2D DP Tables**: Important for grid positions
3. **Minimum Cost Path**: Important for understanding optimal paths
4. **Space Optimization**: Important for performance improvement

---

**This is a great introduction to dynamic programming for grid path optimization problems!** 🎯

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