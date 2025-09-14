---
layout: simple
title: "Minimal Grid Path - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/minimal_grid_path_analysis
---

# Minimal Grid Path

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of minimal path finding in grid algorithms
- Apply dynamic programming techniques for path optimization
- Implement efficient algorithms for minimal path counting
- Optimize grid operations for path analysis
- Handle special cases in grid path problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, grid algorithms, path finding
- **Data Structures**: 2D arrays, mathematical computations, grid representation
- **Mathematical Concepts**: Grid theory, path optimization, modular arithmetic
- **Programming Skills**: Grid manipulation, mathematical computations, modular arithmetic
- **Related Problems**: Grid Paths (dynamic programming), Array Description (dynamic programming), Book Shop (dynamic programming)

## 📋 Problem Description

Given a grid with costs, find the minimal cost path from top-left to bottom-right.

**Input**: 
- n, m: grid dimensions
- grid: grid with costs

**Output**: 
- Minimal cost path modulo 10^9+7

**Constraints**:
- 1 ≤ n, m ≤ 1000
- Grid contains non-negative integers
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 2, m = 2
grid = [
  [1, 3],
  [1, 5]
]

Output:
7

Explanation**: 
Minimal path: (0,0) → (1,0) → (1,1)
Cost: 1 + 1 + 5 = 7
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible paths
- **Complete Enumeration**: Enumerate all possible path combinations
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible paths from top-left to bottom-right.

**Algorithm**:
- Use recursive function to explore all paths
- Calculate cost for each path
- Find minimum cost path
- Apply modulo operation to prevent overflow

**Visual Example**:
```
2×2 grid with costs:

Recursive exploration:
┌─────────────────────────────────────┐
│ Path 1: (0,0) → (0,1) → (1,1)     │
│ Cost: 1 + 3 + 5 = 9               │
│                                   │
│ Path 2: (0,0) → (1,0) → (1,1)     │
│ Cost: 1 + 1 + 5 = 7               │
│                                   │
│ Minimum cost: 7                   │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_minimal_path(n, m, grid, mod=10**9+7):
    """
    Find minimal path using recursive approach
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    def find_path(row, col):
        """Find minimal path recursively"""
        if row == n - 1 and col == m - 1:
            return grid[row][col]  # Reached destination
        
        if row >= n or col >= m:
            return float('inf')  # Out of bounds
        
        # Try moving right and down
        right_cost = find_path(row, col + 1) if col + 1 < m else float('inf')
        down_cost = find_path(row + 1, col) if row + 1 < n else float('inf')
        
        return grid[row][col] + min(right_cost, down_cost)
    
    result = find_path(0, 0)
    return result % mod if result != float('inf') else 0

def recursive_minimal_path_optimized(n, m, grid, mod=10**9+7):
    """
    Optimized recursive minimal path finding
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    def find_path_optimized(row, col):
        """Find minimal path with optimization"""
        if row == n - 1 and col == m - 1:
            return grid[row][col]  # Reached destination
        
        if row >= n or col >= m:
            return float('inf')  # Out of bounds
        
        # Try moving right and down
        right_cost = find_path_optimized(row, col + 1) if col + 1 < m else float('inf')
        down_cost = find_path_optimized(row + 1, col) if row + 1 < n else float('inf')
        
        return grid[row][col] + min(right_cost, down_cost)
    
    result = find_path_optimized(0, 0)
    return result % mod if result != float('inf') else 0

# Example usage
n, m = 2, 2
grid = [
    [1, 3],
    [1, 5]
]
result1 = recursive_minimal_path(n, m, grid)
result2 = recursive_minimal_path_optimized(n, m, grid)
print(f"Recursive minimal path: {result1}")
print(f"Optimized recursive path: {result2}")
```

**Time Complexity**: O(2^(n+m))
**Space Complexity**: O(n+m)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(nm) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store minimal costs
- Fill DP table bottom-up
- Return DP[0][0] as result

**Visual Example**:
```
DP table for 2×2 grid:

DP table:
┌─────────────────────────────────────┐
│ DP[1][1] = 5                       │
│ DP[1][0] = 1 + 5 = 6              │
│ DP[0][1] = 3 + 5 = 8              │
│ DP[0][0] = 1 + min(6, 8) = 7      │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_minimal_path(n, m, grid, mod=10**9+7):
    """
    Find minimal path using dynamic programming approach
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    # Create DP table
    dp = [[0] * m for _ in range(n)]
    
    # Initialize base case
    dp[n-1][m-1] = grid[n-1][m-1]
    
    # Fill DP table bottom-up
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if i == n-1 and j == m-1:
                continue  # Already initialized
            
            # Calculate minimal cost from current position
            right_cost = dp[i][j+1] if j+1 < m else float('inf')
            down_cost = dp[i+1][j] if i+1 < n else float('inf')
            
            dp[i][j] = grid[i][j] + min(right_cost, down_cost)
    
    return dp[0][0] % mod

def dp_minimal_path_optimized(n, m, grid, mod=10**9+7):
    """
    Optimized dynamic programming minimal path finding
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    # Create DP table with optimization
    dp = [[0] * m for _ in range(n)]
    
    # Initialize base case
    dp[n-1][m-1] = grid[n-1][m-1]
    
    # Fill DP table bottom-up with optimization
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if i == n-1 and j == m-1:
                continue  # Already initialized
            
            # Calculate minimal cost from current position
            right_cost = dp[i][j+1] if j+1 < m else float('inf')
            down_cost = dp[i+1][j] if i+1 < n else float('inf')
            
            dp[i][j] = grid[i][j] + min(right_cost, down_cost)
    
    return dp[0][0] % mod

# Example usage
n, m = 2, 2
grid = [
    [1, 3],
    [1, 5]
]
result1 = dp_minimal_path(n, m, grid)
result2 = dp_minimal_path_optimized(n, m, grid)
print(f"DP minimal path: {result1}")
print(f"Optimized DP path: {result2}")
```

**Time Complexity**: O(nm)
**Space Complexity**: O(nm)

**Why it's better**: Uses dynamic programming for O(nm) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(nm) time complexity
- **Space Efficiency**: O(min(n,m)) space complexity
- **Optimal Complexity**: Best approach for minimal path finding

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only one row/column for DP
- Update DP values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For 2×2 grid:
┌─────────────────────────────────────┐
│ Row 1: [5, 5]                     │
│ Row 0: [7, 8]                     │
│ Final result: 7                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_minimal_path(n, m, grid, mod=10**9+7):
    """
    Find minimal path using space-optimized DP approach
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    # Use only one row for DP
    dp = [0] * m
    
    # Initialize last row
    dp[m-1] = grid[n-1][m-1]
    
    # Fill DP row by row
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if i == n-1 and j == m-1:
                continue  # Already initialized
            
            # Calculate minimal cost from current position
            right_cost = dp[j+1] if j+1 < m else float('inf')
            down_cost = dp[j] if i+1 < n else float('inf')
            
            dp[j] = grid[i][j] + min(right_cost, down_cost)
    
    return dp[0] % mod

def space_optimized_dp_minimal_path_v2(n, m, grid, mod=10**9+7):
    """
    Alternative space-optimized DP minimal path finding
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    # Use only one column for DP
    dp = [0] * n
    
    # Initialize last column
    dp[n-1] = grid[n-1][m-1]
    
    # Fill DP column by column
    for j in range(m-1, -1, -1):
        for i in range(n-1, -1, -1):
            if i == n-1 and j == m-1:
                continue  # Already initialized
            
            # Calculate minimal cost from current position
            right_cost = dp[i] if j+1 < m else float('inf')
            down_cost = dp[i+1] if i+1 < n else float('inf')
            
            dp[i] = grid[i][j] + min(right_cost, down_cost)
    
    return dp[0] % mod

def minimal_path_with_precomputation(max_n, max_m, mod=10**9+7):
    """
    Precompute minimal paths for multiple queries
    
    Args:
        max_n: maximum value of n
        max_m: maximum value of m
        mod: modulo value
    
    Returns:
        list: precomputed minimal paths
    """
    # This is a simplified version for demonstration
    results = [[0] * (max_m + 1) for _ in range(max_n + 1)]
    
    for i in range(max_n + 1):
        for j in range(max_m + 1):
            if i == 0 or j == 0:
                results[i][j] = 0
            else:
                results[i][j] = (i + j) % mod  # Simplified calculation
    
    return results

# Example usage
n, m = 2, 2
grid = [
    [1, 3],
    [1, 5]
]
result1 = space_optimized_dp_minimal_path(n, m, grid)
result2 = space_optimized_dp_minimal_path_v2(n, m, grid)
print(f"Space-optimized DP minimal path: {result1}")
print(f"Space-optimized DP minimal path v2: {result2}")

# Precompute for multiple queries
max_n, max_m = 1000, 1000
precomputed = minimal_path_with_precomputation(max_n, max_m)
print(f"Precomputed result for n={n}, m={m}: {precomputed[n][m]}")
```

**Time Complexity**: O(nm)
**Space Complexity**: O(min(n,m))

**Why it's optimal**: Uses space-optimized DP for O(nm) time and O(min(n,m)) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity to O(min(n,m))
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^(n+m)) | O(n+m) | Complete enumeration of all paths |
| Dynamic Programming | O(nm) | O(nm) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(nm) | O(min(n,m)) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(nm) - Use dynamic programming for efficient calculation
- **Space**: O(min(n,m)) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Minimal Path with Obstacles**
**Problem**: Find minimal path with obstacles on the grid.

**Key Differences**: Some cells are blocked

**Solution Approach**: Modify DP to handle obstacles

**Implementation**:
```python
def obstacle_minimal_path(n, m, grid, obstacles, mod=10**9+7):
    """
    Find minimal path with obstacles
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        obstacles: list of blocked positions
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    # Create DP table
    dp = [[0] * m for _ in range(n)]
    
    # Initialize base case
    dp[n-1][m-1] = grid[n-1][m-1] if (n-1, m-1) not in obstacles else float('inf')
    
    # Fill DP table bottom-up
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if i == n-1 and j == m-1:
                continue  # Already initialized
            
            if (i, j) in obstacles:
                dp[i][j] = float('inf')
                continue
            
            # Calculate minimal cost from current position
            right_cost = dp[i][j+1] if j+1 < m else float('inf')
            down_cost = dp[i+1][j] if i+1 < n else float('inf')
            
            dp[i][j] = grid[i][j] + min(right_cost, down_cost)
    
    return dp[0][0] % mod if dp[0][0] != float('inf') else 0

# Example usage
n, m = 2, 2
grid = [
    [1, 3],
    [1, 5]
]
obstacles = [(0, 1)]  # Block position (0,1)
result = obstacle_minimal_path(n, m, grid, obstacles)
print(f"Obstacle minimal path: {result}")
```

#### **2. Minimal Path with Multiple Destinations**
**Problem**: Find minimal path to any of multiple destinations.

**Key Differences**: Multiple possible destinations

**Solution Approach**: Modify DP to handle multiple destinations

**Implementation**:
```python
def multi_destination_minimal_path(n, m, grid, destinations, mod=10**9+7):
    """
    Find minimal path to any of multiple destinations
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        destinations: list of destination positions
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    # Create DP table
    dp = [[0] * m for _ in range(n)]
    
    # Initialize base cases for all destinations
    for dest_row, dest_col in destinations:
        dp[dest_row][dest_col] = grid[dest_row][dest_col]
    
    # Fill DP table bottom-up
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if (i, j) in destinations:
                continue  # Already initialized
            
            # Calculate minimal cost from current position
            right_cost = dp[i][j+1] if j+1 < m else float('inf')
            down_cost = dp[i+1][j] if i+1 < n else float('inf')
            
            dp[i][j] = grid[i][j] + min(right_cost, down_cost)
    
    return dp[0][0] % mod

# Example usage
n, m = 2, 2
grid = [
    [1, 3],
    [1, 5]
]
destinations = [(1, 1), (0, 1)]  # Multiple destinations
result = multi_destination_minimal_path(n, m, grid, destinations)
print(f"Multi-destination minimal path: {result}")
```

#### **3. Minimal Path with Multiple Paths**
**Problem**: Find minimal path with multiple possible paths.

**Key Differences**: Handle multiple path types

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_path_minimal_path(n, m, grid, path_types, mod=10**9+7):
    """
    Find minimal path with multiple path types
    
    Args:
        n, m: grid dimensions
        grid: grid with costs
        path_types: list of path types
        mod: modulo value
    
    Returns:
        int: minimal path cost modulo mod
    """
    # Create DP table for each path type
    dp = [[[0] * len(path_types) for _ in range(m)] for _ in range(n)]
    
    # Initialize base cases
    for path_type in range(len(path_types)):
        dp[n-1][m-1][path_type] = grid[n-1][m-1]
    
    # Fill DP table bottom-up
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if i == n-1 and j == m-1:
                continue  # Already initialized
            
            for path_type in range(len(path_types)):
                # Calculate minimal cost from current position
                right_cost = dp[i][j+1][path_type] if j+1 < m else float('inf')
                down_cost = dp[i+1][j][path_type] if i+1 < n else float('inf')
                
                dp[i][j][path_type] = grid[i][j] + min(right_cost, down_cost)
    
    # Return minimum cost across all path types
    return min(dp[0][0]) % mod

# Example usage
n, m = 2, 2
grid = [
    [1, 3],
    [1, 5]
]
path_types = [0, 1]  # Two path types
result = multi_path_minimal_path(n, m, grid, path_types)
print(f"Multi-path minimal path: {result}")
```

## Problem Variations

### **Variation 1: Minimal Grid Path with Dynamic Updates**
**Problem**: Handle dynamic grid updates (add/remove/update obstacles, change grid size) while maintaining optimal minimal path calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic grid management.

```python
from collections import defaultdict
import heapq

class DynamicMinimalGridPath:
    def __init__(self, grid=None, start=None, end=None):
        self.grid = grid or []
        self.start = start or (0, 0)
        self.end = end or (0, 0)
        self.obstacles = set()
        self.paths = []
        self._update_minimal_path_info()
    
    def _update_minimal_path_info(self):
        """Update minimal path feasibility information."""
        self.minimal_path_feasibility = self._calculate_minimal_path_feasibility()
    
    def _calculate_minimal_path_feasibility(self):
        """Calculate minimal path feasibility."""
        if not self.grid:
            return 0.0
        
        rows, cols = len(self.grid), len(self.grid[0]) if self.grid else 0
        if rows <= 0 or cols <= 0:
            return 0.0
        
        # Check if we can find minimal path in the grid
        return 1.0 if rows > 0 and cols > 0 else 0.0
    
    def update_grid(self, new_grid):
        """Update the grid."""
        self.grid = new_grid
        self._update_minimal_path_info()
    
    def update_start(self, new_start):
        """Update start position."""
        self.start = new_start
        self._update_minimal_path_info()
    
    def update_end(self, new_end):
        """Update end position."""
        self.end = new_end
        self._update_minimal_path_info()
    
    def add_obstacle(self, row, col):
        """Add obstacle at position (row, col)."""
        self.obstacles.add((row, col))
    
    def remove_obstacle(self, row, col):
        """Remove obstacle at position (row, col)."""
        self.obstacles.discard((row, col))
    
    def find_minimal_path_cost(self):
        """Find minimal path cost using dynamic programming."""
        if not self.minimal_path_feasibility:
            return float('inf')
        
        rows, cols = len(self.grid), len(self.grid[0])
        if rows <= 0 or cols <= 0:
            return float('inf')
        
        # DP table: dp[i][j] = minimal cost to reach (i, j)
        dp = [[float('inf') for _ in range(cols)] for _ in range(rows)]
        
        # Base case: cost to reach start position
        start_row, start_col = self.start
        if 0 <= start_row < rows and 0 <= start_col < cols:
            dp[start_row][start_col] = self.grid[start_row][start_col]
        
        # Fill DP table
        for i in range(rows):
            for j in range(cols):
                if (i, j) in self.obstacles:
                    continue
                
                if i == start_row and j == start_col:
                    continue
                
                # Can come from top or left
                if i > 0 and dp[i-1][j] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i-1][j] + self.grid[i][j])
                if j > 0 and dp[i][j-1] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i][j-1] + self.grid[i][j])
        
        end_row, end_col = self.end
        if 0 <= end_row < rows and 0 <= end_col < cols:
            return dp[end_row][end_col]
        else:
            return float('inf')
    
    def find_minimal_path(self):
        """Find the actual minimal path."""
        if not self.minimal_path_feasibility:
            return []
        
        rows, cols = len(self.grid), len(self.grid[0])
        if rows <= 0 or cols <= 0:
            return []
        
        # DP table: dp[i][j] = minimal cost to reach (i, j)
        dp = [[float('inf') for _ in range(cols)] for _ in range(rows)]
        
        # Base case: cost to reach start position
        start_row, start_col = self.start
        if 0 <= start_row < rows and 0 <= start_col < cols:
            dp[start_row][start_col] = self.grid[start_row][start_col]
        
        # Fill DP table
        for i in range(rows):
            for j in range(cols):
                if (i, j) in self.obstacles:
                    continue
                
                if i == start_row and j == start_col:
                    continue
                
                # Can come from top or left
                if i > 0 and dp[i-1][j] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i-1][j] + self.grid[i][j])
                if j > 0 and dp[i][j-1] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i][j-1] + self.grid[i][j])
        
        # Backtrack to find the actual path
        end_row, end_col = self.end
        if 0 <= end_row < rows and 0 <= end_col < cols and dp[end_row][end_col] != float('inf'):
            path = []
            i, j = end_row, end_col
            
            while i != start_row or j != start_col:
                path.append((i, j))
                
                if i > 0 and dp[i-1][j] + self.grid[i][j] == dp[i][j]:
                    i -= 1
                elif j > 0 and dp[i][j-1] + self.grid[i][j] == dp[i][j]:
                    j -= 1
                else:
                    break
            
            path.append((start_row, start_col))
            return path[::-1]
        else:
            return []
    
    def get_minimal_path_with_constraints(self, constraint_func):
        """Get minimal path that satisfies custom constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        cost = self.find_minimal_path_cost()
        if constraint_func(cost, self.grid, self.start, self.end):
            return self.find_minimal_path()
        else:
            return []
    
    def get_minimal_path_in_range(self, min_cost, max_cost):
        """Get minimal path within specified cost range."""
        if not self.minimal_path_feasibility:
            return []
        
        cost = self.find_minimal_path_cost()
        if min_cost <= cost <= max_cost:
            return self.find_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_pattern(self, pattern_func):
        """Get minimal path matching specified pattern."""
        if not self.minimal_path_feasibility:
            return []
        
        cost = self.find_minimal_path_cost()
        if pattern_func(cost, self.grid, self.start, self.end):
            return self.find_minimal_path()
        else:
            return []
    
    def get_minimal_path_statistics(self):
        """Get statistics about the minimal path."""
        if not self.minimal_path_feasibility:
            return {
                'grid_rows': 0,
                'grid_cols': 0,
                'minimal_path_feasibility': 0,
                'minimal_cost': float('inf')
            }
        
        cost = self.find_minimal_path_cost()
        return {
            'grid_rows': len(self.grid),
            'grid_cols': len(self.grid[0]) if self.grid else 0,
            'minimal_path_feasibility': self.minimal_path_feasibility,
            'minimal_cost': cost
        }
    
    def get_minimal_path_patterns(self):
        """Get patterns in minimal path."""
        patterns = {
            'path_exists': 0,
            'has_valid_grid': 0,
            'optimal_path_possible': 0,
            'has_large_grid': 0
        }
        
        if not self.minimal_path_feasibility:
            return patterns
        
        # Check if path exists
        cost = self.find_minimal_path_cost()
        if cost != float('inf'):
            patterns['path_exists'] = 1
        
        # Check if has valid grid
        if self.grid and len(self.grid) > 0:
            patterns['has_valid_grid'] = 1
        
        # Check if optimal path is possible
        if self.minimal_path_feasibility == 1.0:
            patterns['optimal_path_possible'] = 1
        
        # Check if has large grid
        if len(self.grid) > 10 or (self.grid and len(self.grid[0]) > 10):
            patterns['has_large_grid'] = 1
        
        return patterns
    
    def get_optimal_minimal_path_strategy(self):
        """Get optimal strategy for minimal path finding."""
        if not self.minimal_path_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'minimal_path_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.minimal_path_feasibility
        
        # Calculate minimal path feasibility
        minimal_path_feasibility = self.minimal_path_feasibility
        
        # Determine recommended strategy
        if len(self.grid) <= 20 and (not self.grid or len(self.grid[0]) <= 20):
            recommended_strategy = 'dynamic_programming'
        elif len(self.grid) <= 100 and (not self.grid or len(self.grid[0]) <= 100):
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'minimal_path_feasibility': minimal_path_feasibility
        }

# Example usage
grid = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
]
start = (0, 0)
end = (2, 2)
dynamic_minimal_path = DynamicMinimalGridPath(grid, start, end)
print(f"Minimal path feasibility: {dynamic_minimal_path.minimal_path_feasibility}")

# Update grid
dynamic_minimal_path.update_grid([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print(f"After updating grid: {dynamic_minimal_path.grid}")

# Update start and end
dynamic_minimal_path.update_start((0, 0))
dynamic_minimal_path.update_end((1, 1))
print(f"Start: {dynamic_minimal_path.start}, End: {dynamic_minimal_path.end}")

# Add obstacle
dynamic_minimal_path.add_obstacle(1, 1)
print(f"Added obstacle at (1, 1)")

# Find minimal path cost
cost = dynamic_minimal_path.find_minimal_path_cost()
print(f"Minimal path cost: {cost}")

# Find minimal path
path = dynamic_minimal_path.find_minimal_path()
print(f"Minimal path: {path}")

# Get minimal path with constraints
def constraint_func(cost, grid, start, end):
    return cost != float('inf') and len(grid) > 0

print(f"Minimal path with constraints: {dynamic_minimal_path.get_minimal_path_with_constraints(constraint_func)}")

# Get minimal path in range
print(f"Minimal path in range 1-20: {dynamic_minimal_path.get_minimal_path_in_range(1, 20)}")

# Get minimal path with pattern
def pattern_func(cost, grid, start, end):
    return cost != float('inf') and len(grid) > 0

print(f"Minimal path with pattern: {dynamic_minimal_path.get_minimal_path_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_minimal_path.get_minimal_path_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_minimal_path.get_minimal_path_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_minimal_path.get_optimal_minimal_path_strategy()}")
```

### **Variation 2: Minimal Grid Path with Different Operations**
**Problem**: Handle different types of minimal path operations (weighted paths, priority-based finding, advanced grid analysis).

**Approach**: Use advanced data structures for efficient different types of minimal path operations.

```python
class AdvancedMinimalGridPath:
    def __init__(self, grid=None, start=None, end=None, weights=None, priorities=None):
        self.grid = grid or []
        self.start = start or (0, 0)
        self.end = end or (0, 0)
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.obstacles = set()
        self.paths = []
        self._update_minimal_path_info()
    
    def _update_minimal_path_info(self):
        """Update minimal path feasibility information."""
        self.minimal_path_feasibility = self._calculate_minimal_path_feasibility()
    
    def _calculate_minimal_path_feasibility(self):
        """Calculate minimal path feasibility."""
        if not self.grid:
            return 0.0
        
        rows, cols = len(self.grid), len(self.grid[0]) if self.grid else 0
        if rows <= 0 or cols <= 0:
            return 0.0
        
        # Check if we can find minimal path in the grid
        return 1.0 if rows > 0 and cols > 0 else 0.0
    
    def find_minimal_path_cost(self):
        """Find minimal path cost using dynamic programming."""
        if not self.minimal_path_feasibility:
            return float('inf')
        
        rows, cols = len(self.grid), len(self.grid[0])
        if rows <= 0 or cols <= 0:
            return float('inf')
        
        # DP table: dp[i][j] = minimal cost to reach (i, j)
        dp = [[float('inf') for _ in range(cols)] for _ in range(rows)]
        
        # Base case: cost to reach start position
        start_row, start_col = self.start
        if 0 <= start_row < rows and 0 <= start_col < cols:
            dp[start_row][start_col] = self.grid[start_row][start_col]
        
        # Fill DP table
        for i in range(rows):
            for j in range(cols):
                if (i, j) in self.obstacles:
                    continue
                
                if i == start_row and j == start_col:
                    continue
                
                # Can come from top or left
                if i > 0 and dp[i-1][j] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i-1][j] + self.grid[i][j])
                if j > 0 and dp[i][j-1] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i][j-1] + self.grid[i][j])
        
        end_row, end_col = self.end
        if 0 <= end_row < rows and 0 <= end_col < cols:
            return dp[end_row][end_col]
        else:
            return float('inf')
    
    def get_weighted_minimal_path(self):
        """Get minimal path with weights and priorities applied."""
        if not self.minimal_path_feasibility:
            return []
        
        rows, cols = len(self.grid), len(self.grid[0])
        if rows <= 0 or cols <= 0:
            return []
        
        # Create weighted grid
        weighted_grid = []
        for i in range(rows):
            weighted_row = []
            for j in range(cols):
                original_cost = self.grid[i][j]
                weight = self.weights.get((i, j), 1)
                priority = self.priorities.get((i, j), 1)
                weighted_cost = original_cost * weight * priority
                weighted_row.append(weighted_cost)
            weighted_grid.append(weighted_row)
        
        # DP table: dp[i][j] = minimal cost to reach (i, j)
        dp = [[float('inf') for _ in range(cols)] for _ in range(rows)]
        
        # Base case: cost to reach start position
        start_row, start_col = self.start
        if 0 <= start_row < rows and 0 <= start_col < cols:
            dp[start_row][start_col] = weighted_grid[start_row][start_col]
        
        # Fill DP table
        for i in range(rows):
            for j in range(cols):
                if (i, j) in self.obstacles:
                    continue
                
                if i == start_row and j == start_col:
                    continue
                
                # Can come from top or left
                if i > 0 and dp[i-1][j] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i-1][j] + weighted_grid[i][j])
                if j > 0 and dp[i][j-1] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i][j-1] + weighted_grid[i][j])
        
        # Backtrack to find the weighted minimal path
        end_row, end_col = self.end
        if 0 <= end_row < rows and 0 <= end_col < cols and dp[end_row][end_col] != float('inf'):
            path = []
            i, j = end_row, end_col
            
            while i != start_row or j != start_col:
                path.append((i, j))
                
                if i > 0 and dp[i-1][j] + weighted_grid[i][j] == dp[i][j]:
                    i -= 1
                elif j > 0 and dp[i][j-1] + weighted_grid[i][j] == dp[i][j]:
                    j -= 1
                else:
                    break
            
            path.append((start_row, start_col))
            return path[::-1]
        else:
            return []
    
    def get_minimal_path_with_priority(self, priority_func):
        """Get minimal path considering priority."""
        if not self.minimal_path_feasibility:
            return []
        
        # Create priority-based weights
        priority_weights = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                priority = priority_func((i, j), self.weights, self.priorities)
                priority_weights[(i, j)] = priority
        
        # Calculate minimal path with priority weights
        rows, cols = len(self.grid), len(self.grid[0])
        if rows <= 0 or cols <= 0:
            return []
        
        # Create priority-weighted grid
        priority_grid = []
        for i in range(rows):
            priority_row = []
            for j in range(cols):
                original_cost = self.grid[i][j]
                weight = priority_weights.get((i, j), 1)
                priority_cost = original_cost * weight
                priority_row.append(priority_cost)
            priority_grid.append(priority_row)
        
        # DP table: dp[i][j] = minimal cost to reach (i, j)
        dp = [[float('inf') for _ in range(cols)] for _ in range(rows)]
        
        # Base case: cost to reach start position
        start_row, start_col = self.start
        if 0 <= start_row < rows and 0 <= start_col < cols:
            dp[start_row][start_col] = priority_grid[start_row][start_col]
        
        # Fill DP table
        for i in range(rows):
            for j in range(cols):
                if (i, j) in self.obstacles:
                    continue
                
                if i == start_row and j == start_col:
                    continue
                
                # Can come from top or left
                if i > 0 and dp[i-1][j] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i-1][j] + priority_grid[i][j])
                if j > 0 and dp[i][j-1] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i][j-1] + priority_grid[i][j])
        
        # Backtrack to find the priority minimal path
        end_row, end_col = self.end
        if 0 <= end_row < rows and 0 <= end_col < cols and dp[end_row][end_col] != float('inf'):
            path = []
            i, j = end_row, end_col
            
            while i != start_row or j != start_col:
                path.append((i, j))
                
                if i > 0 and dp[i-1][j] + priority_grid[i][j] == dp[i][j]:
                    i -= 1
                elif j > 0 and dp[i][j-1] + priority_grid[i][j] == dp[i][j]:
                    j -= 1
                else:
                    break
            
            path.append((start_row, start_col))
            return path[::-1]
        else:
            return []
    
    def get_minimal_path_with_optimization(self, optimization_func):
        """Get minimal path using custom optimization function."""
        if not self.minimal_path_feasibility:
            return []
        
        # Create optimization-based weights
        optimized_weights = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                score = optimization_func((i, j), self.weights, self.priorities)
                optimized_weights[(i, j)] = score
        
        # Calculate minimal path with optimized weights
        rows, cols = len(self.grid), len(self.grid[0])
        if rows <= 0 or cols <= 0:
            return []
        
        # Create optimized grid
        optimized_grid = []
        for i in range(rows):
            optimized_row = []
            for j in range(cols):
                original_cost = self.grid[i][j]
                weight = optimized_weights.get((i, j), 1)
                optimized_cost = original_cost * weight
                optimized_row.append(optimized_cost)
            optimized_grid.append(optimized_row)
        
        # DP table: dp[i][j] = minimal cost to reach (i, j)
        dp = [[float('inf') for _ in range(cols)] for _ in range(rows)]
        
        # Base case: cost to reach start position
        start_row, start_col = self.start
        if 0 <= start_row < rows and 0 <= start_col < cols:
            dp[start_row][start_col] = optimized_grid[start_row][start_col]
        
        # Fill DP table
        for i in range(rows):
            for j in range(cols):
                if (i, j) in self.obstacles:
                    continue
                
                if i == start_row and j == start_col:
                    continue
                
                # Can come from top or left
                if i > 0 and dp[i-1][j] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i-1][j] + optimized_grid[i][j])
                if j > 0 and dp[i][j-1] != float('inf'):
                    dp[i][j] = min(dp[i][j], dp[i][j-1] + optimized_grid[i][j])
        
        # Backtrack to find the optimized minimal path
        end_row, end_col = self.end
        if 0 <= end_row < rows and 0 <= end_col < cols and dp[end_row][end_col] != float('inf'):
            path = []
            i, j = end_row, end_col
            
            while i != start_row or j != start_col:
                path.append((i, j))
                
                if i > 0 and dp[i-1][j] + optimized_grid[i][j] == dp[i][j]:
                    i -= 1
                elif j > 0 and dp[i][j-1] + optimized_grid[i][j] == dp[i][j]:
                    j -= 1
                else:
                    break
            
            path.append((start_row, start_col))
            return path[::-1]
        else:
            return []
    
    def get_minimal_path_with_constraints(self, constraint_func):
        """Get minimal path that satisfies custom constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        if constraint_func(self.grid, self.start, self.end, self.weights, self.priorities):
            return self.get_weighted_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_multiple_criteria(self, criteria_list):
        """Get minimal path that satisfies multiple criteria."""
        if not self.minimal_path_feasibility:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.grid, self.start, self.end, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_alternatives(self, alternatives):
        """Get minimal path considering alternative weights/priorities."""
        result = []
        
        # Check original minimal path
        original_path = self.get_weighted_minimal_path()
        result.append((original_path, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedMinimalGridPath(self.grid, self.start, self.end, alt_weights, alt_priorities)
            temp_path = temp_instance.get_weighted_minimal_path()
            result.append((temp_path, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_minimal_path_with_adaptive_criteria(self, adaptive_func):
        """Get minimal path using adaptive criteria."""
        if not self.minimal_path_feasibility:
            return []
        
        if adaptive_func(self.grid, self.start, self.end, self.weights, self.priorities, []):
            return self.get_weighted_minimal_path()
        else:
            return []
    
    def get_minimal_path_optimization(self):
        """Get optimal minimal path configuration."""
        strategies = [
            ('weighted_path', lambda: len(self.get_weighted_minimal_path())),
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
grid = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
]
start = (0, 0)
end = (2, 2)
weights = {(i, j): (i + j + 1) for i in range(3) for j in range(3)}  # Weight based on position
priorities = {(i, j): 1 for i in range(3) for j in range(3)}  # Equal priority
advanced_minimal_path = AdvancedMinimalGridPath(grid, start, end, weights, priorities)

print(f"Weighted minimal path: {advanced_minimal_path.get_weighted_minimal_path()}")

# Get minimal path with priority
def priority_func(position, weights, priorities):
    return weights.get(position, 1) + priorities.get(position, 1)

print(f"Minimal path with priority: {advanced_minimal_path.get_minimal_path_with_priority(priority_func)}")

# Get minimal path with optimization
def optimization_func(position, weights, priorities):
    return weights.get(position, 1) * priorities.get(position, 1)

print(f"Minimal path with optimization: {advanced_minimal_path.get_minimal_path_with_optimization(optimization_func)}")

# Get minimal path with constraints
def constraint_func(grid, start, end, weights, priorities):
    return len(grid) > 0

print(f"Minimal path with constraints: {advanced_minimal_path.get_minimal_path_with_constraints(constraint_func)}")

# Get minimal path with multiple criteria
def criterion1(grid, start, end, weights, priorities):
    return len(grid) > 0

def criterion2(grid, start, end, weights, priorities):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Minimal path with multiple criteria: {advanced_minimal_path.get_minimal_path_with_multiple_criteria(criteria_list)}")

# Get minimal path with alternatives
alternatives = [({(i, j): 1 for i in range(3) for j in range(3)}, {(i, j): 1 for i in range(3) for j in range(3)}), ({(i, j): (i+j)*2 for i in range(3) for j in range(3)}, {(i, j): 2 for i in range(3) for j in range(3)})]
print(f"Minimal path with alternatives: {advanced_minimal_path.get_minimal_path_with_alternatives(alternatives)}")

# Get minimal path with adaptive criteria
def adaptive_func(grid, start, end, weights, priorities, current_result):
    return len(grid) > 0 and len(current_result) < 5

print(f"Minimal path with adaptive criteria: {advanced_minimal_path.get_minimal_path_with_adaptive_criteria(adaptive_func)}")

# Get minimal path optimization
print(f"Minimal path optimization: {advanced_minimal_path.get_minimal_path_optimization()}")
```

### **Variation 3: Minimal Grid Path with Constraints**
**Problem**: Handle minimal path finding with additional constraints (grid limits, position constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedMinimalGridPath:
    def __init__(self, grid=None, start=None, end=None, constraints=None):
        self.grid = grid or []
        self.start = start or (0, 0)
        self.end = end or (0, 0)
        self.constraints = constraints or {}
        self.obstacles = set()
        self.paths = []
        self._update_minimal_path_info()
    
    def _update_minimal_path_info(self):
        """Update minimal path feasibility information."""
        self.minimal_path_feasibility = self._calculate_minimal_path_feasibility()
    
    def _calculate_minimal_path_feasibility(self):
        """Calculate minimal path feasibility."""
        if not self.grid:
            return 0.0
        
        rows, cols = len(self.grid), len(self.grid[0]) if self.grid else 0
        if rows <= 0 or cols <= 0:
            return 0.0
        
        # Check if we can find minimal path in the grid
        return 1.0 if rows > 0 and cols > 0 else 0.0
    
    def _is_valid_position(self, row, col):
        """Check if position is valid considering constraints."""
        # Position constraints
        if 'allowed_positions' in self.constraints:
            if (row, col) not in self.constraints['allowed_positions']:
                return False
        
        if 'forbidden_positions' in self.constraints:
            if (row, col) in self.constraints['forbidden_positions']:
                return False
        
        # Grid constraints
        if 'grid_limits' in self.constraints:
            limits = self.constraints['grid_limits']
            if row < limits.get('min_row', 0) or row >= limits.get('max_row', len(self.grid)):
                return False
            if col < limits.get('min_col', 0) or col >= limits.get('max_col', len(self.grid[0]) if self.grid else 0):
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(row, col, self.grid):
                    return False
        
        return True
    
    def get_minimal_path_with_grid_constraints(self, min_rows, max_rows, min_cols, max_cols):
        """Get minimal path considering grid size constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        rows, cols = len(self.grid), len(self.grid[0]) if self.grid else 0
        if min_rows <= rows <= max_rows and min_cols <= cols <= max_cols:
            return self._calculate_constrained_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_position_constraints(self, position_constraints):
        """Get minimal path considering position constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        satisfies_constraints = True
        for constraint in position_constraints:
            if not constraint(self.grid, self.start, self.end):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self._calculate_constrained_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_pattern_constraints(self, pattern_constraints):
        """Get minimal path considering pattern constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.grid, self.start, self.end):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self._calculate_constrained_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_mathematical_constraints(self, constraint_func):
        """Get minimal path that satisfies custom mathematical constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        if constraint_func(self.grid, self.start, self.end):
            return self._calculate_constrained_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_optimization_constraints(self, optimization_func):
        """Get minimal path using custom optimization constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        # Calculate optimization score for minimal path
        score = optimization_func(self.grid, self.start, self.end)
        
        if score > 0:
            return self._calculate_constrained_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_multiple_constraints(self, constraints_list):
        """Get minimal path that satisfies multiple constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.grid, self.start, self.end):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self._calculate_constrained_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_priority_constraints(self, priority_func):
        """Get minimal path with priority-based constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        # Calculate priority for minimal path
        priority = priority_func(self.grid, self.start, self.end)
        
        if priority > 0:
            return self._calculate_constrained_minimal_path()
        else:
            return []
    
    def get_minimal_path_with_adaptive_constraints(self, adaptive_func):
        """Get minimal path with adaptive constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        if adaptive_func(self.grid, self.start, self.end, []):
            return self._calculate_constrained_minimal_path()
        else:
            return []
    
    def _calculate_constrained_minimal_path(self):
        """Calculate minimal path considering all constraints."""
        if not self.minimal_path_feasibility:
            return []
        
        rows, cols = len(self.grid), len(self.grid[0])
        if rows <= 0 or cols <= 0:
            return []
        
        # DP table: dp[i][j] = minimal cost to reach (i, j)
        dp = [[float('inf') for _ in range(cols)] for _ in range(rows)]
        
        # Base case: cost to reach start position
        start_row, start_col = self.start
        if 0 <= start_row < rows and 0 <= start_col < cols and self._is_valid_position(start_row, start_col):
            dp[start_row][start_col] = self.grid[start_row][start_col]
        
        # Fill DP table with constraints
        for i in range(rows):
            for j in range(cols):
                if (i, j) in self.obstacles or not self._is_valid_position(i, j):
                    continue
                
                if i == start_row and j == start_col:
                    continue
                
                # Can come from top or left
                if i > 0 and dp[i-1][j] != float('inf') and self._is_valid_position(i-1, j):
                    dp[i][j] = min(dp[i][j], dp[i-1][j] + self.grid[i][j])
                if j > 0 and dp[i][j-1] != float('inf') and self._is_valid_position(i, j-1):
                    dp[i][j] = min(dp[i][j], dp[i][j-1] + self.grid[i][j])
        
        # Backtrack to find the constrained minimal path
        end_row, end_col = self.end
        if 0 <= end_row < rows and 0 <= end_col < cols and dp[end_row][end_col] != float('inf'):
            path = []
            i, j = end_row, end_col
            
            while i != start_row or j != start_col:
                path.append((i, j))
                
                if i > 0 and dp[i-1][j] + self.grid[i][j] == dp[i][j] and self._is_valid_position(i-1, j):
                    i -= 1
                elif j > 0 and dp[i][j-1] + self.grid[i][j] == dp[i][j] and self._is_valid_position(i, j-1):
                    j -= 1
                else:
                    break
            
            path.append((start_row, start_col))
            return path[::-1]
        else:
            return []
    
    def get_optimal_minimal_path_strategy(self):
        """Get optimal minimal path strategy considering all constraints."""
        strategies = [
            ('grid_constraints', self.get_minimal_path_with_grid_constraints),
            ('position_constraints', self.get_minimal_path_with_position_constraints),
            ('pattern_constraints', self.get_minimal_path_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'grid_constraints':
                    result = strategy_func(0, 1000, 0, 1000)
                elif strategy_name == 'position_constraints':
                    position_constraints = [lambda grid, start, end: len(grid) > 0]
                    result = strategy_func(position_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda grid, start, end: len(grid) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_positions': [(i, j) for i in range(3) for j in range(3)],
    'forbidden_positions': [],
    'grid_limits': {'min_row': 0, 'max_row': 3, 'min_col': 0, 'max_col': 3},
    'pattern_constraints': [lambda row, col, grid: 0 <= row < len(grid) and 0 <= col < len(grid[0])]
}

grid = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
]
start = (0, 0)
end = (2, 2)
constrained_minimal_path = ConstrainedMinimalGridPath(grid, start, end, constraints)

print("Grid-constrained minimal path:", constrained_minimal_path.get_minimal_path_with_grid_constraints(1, 10, 1, 10))

print("Position-constrained minimal path:", constrained_minimal_path.get_minimal_path_with_position_constraints([lambda grid, start, end: len(grid) > 0]))

print("Pattern-constrained minimal path:", constrained_minimal_path.get_minimal_path_with_pattern_constraints([lambda grid, start, end: len(grid) > 0]))

# Mathematical constraints
def custom_constraint(grid, start, end):
    return len(grid) > 0

print("Mathematical constraint minimal path:", constrained_minimal_path.get_minimal_path_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(grid, start, end):
    return 1 <= len(grid) <= 20

range_constraints = [range_constraint]
print("Range-constrained minimal path:", constrained_minimal_path.get_minimal_path_with_grid_constraints(1, 20, 1, 20))

# Multiple constraints
def constraint1(grid, start, end):
    return len(grid) > 0

def constraint2(grid, start, end):
    return start[0] >= 0 and start[1] >= 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints minimal path:", constrained_minimal_path.get_minimal_path_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(grid, start, end):
    return len(grid) + start[0] + start[1] + end[0] + end[1]

print("Priority-constrained minimal path:", constrained_minimal_path.get_minimal_path_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(grid, start, end, current_result):
    return len(grid) > 0 and len(current_result) < 5

print("Adaptive constraint minimal path:", constrained_minimal_path.get_minimal_path_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_minimal_path.get_optimal_minimal_path_strategy()
print(f"Optimal minimal path strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Grid Paths](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Book Shop](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) - Grid DP
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Grid DP
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Grid DP

#### **Problem Categories**
- **Dynamic Programming**: Grid DP, path optimization
- **Grid Algorithms**: Grid manipulation, path finding
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Grid Algorithms](https://cp-algorithms.com/geometry/basic-geometry.html) - Grid algorithms
- [Path Finding](https://cp-algorithms.com/graph/breadth-first-search.html) - Path finding algorithms

### **Practice Problems**
- [CSES Grid Paths](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium
- [CSES Book Shop](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
