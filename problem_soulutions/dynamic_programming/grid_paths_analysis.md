---
layout: simple
title: "Grid Paths - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/grid_paths_analysis
---

# Grid Paths

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of grid path counting in dynamic programming
- Apply counting techniques for grid path analysis
- Implement efficient algorithms for grid path counting
- Optimize DP operations for path analysis
- Handle special cases in grid path problems

## 📋 Problem Description

Given an n×n grid, count the number of paths from top-left to bottom-right (only moving right and down).

**Input**: 
- n: grid size

**Output**: 
- Number of paths modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 1000
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3

Output:
6

Explanation**: 
Paths from (0,0) to (2,2) in 3×3 grid:
1. Right → Right → Down → Down
2. Right → Down → Right → Down
3. Right → Down → Down → Right
4. Down → Right → Right → Down
5. Down → Right → Down → Right
6. Down → Down → Right → Right
Total: 6 paths
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible paths
- **Complete Enumeration**: Enumerate all possible path sequences
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible paths from top-left to bottom-right.

**Algorithm**:
- Use recursive function to try all path combinations
- Count valid paths
- Apply modulo operation to prevent overflow

**Visual Example**:
```
3×3 grid:

Recursive exploration:
┌─────────────────────────────────────┐
│ From (0,0):                        │
│ - Move right to (0,1)              │
│   - Move right to (0,2)            │
│     - Move down to (1,2)           │
│       - Move down to (2,2) ✓       │
│   - Move down to (1,1)             │
│     - Move right to (1,2)          │
│       - Move down to (2,2) ✓       │
│     - Move down to (2,1)           │
│       - Move right to (2,2) ✓      │
│ - Move down to (1,0)               │
│   - Move right to (1,1)            │
│     - Move right to (1,2)          │
│       - Move down to (2,2) ✓       │
│     - Move down to (2,1)           │
│       - Move right to (2,2) ✓      │
│   - Move down to (2,0)             │
│     - Move right to (2,1)          │
│       - Move right to (2,2) ✓      │
│                                   │
│ Total: 6 paths                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_grid_paths(n, mod=10**9+7):
    """
    Count grid paths using recursive approach
    
    Args:
        n: grid size
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    def count_paths(row, col):
        """Count paths recursively"""
        if row == n - 1 and col == n - 1:
            return 1  # Reached destination
        
        if row >= n or col >= n:
            return 0  # Out of bounds
        
        # Try moving right and down
        right_paths = count_paths(row, col + 1)
        down_paths = count_paths(row + 1, col)
        
        return (right_paths + down_paths) % mod
    
    return count_paths(0, 0)

def recursive_grid_paths_optimized(n, mod=10**9+7):
    """
    Optimized recursive grid paths counting
    
    Args:
        n: grid size
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    def count_paths_optimized(row, col):
        """Count paths with optimization"""
        if row == n - 1 and col == n - 1:
            return 1  # Reached destination
        
        if row >= n or col >= n:
            return 0  # Out of bounds
        
        # Try moving right and down
        right_paths = count_paths_optimized(row, col + 1)
        down_paths = count_paths_optimized(row + 1, col)
        
        return (right_paths + down_paths) % mod
    
    return count_paths_optimized(0, 0)

# Example usage
n = 3
result1 = recursive_grid_paths(n)
result2 = recursive_grid_paths_optimized(n)
print(f"Recursive grid paths: {result1}")
print(f"Optimized recursive grid paths: {result2}")
```

**Time Complexity**: O(2^(2n))
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(n²) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

#### 📌 **DP State Definition**

**What does `dp[i][j]` represent?**
- `dp[i][j]` = **number of paths** from the top-left corner (0,0) to position (i,j) in the grid
- This is a 2D DP array where:
  - First dimension `i` = row index (0 to n-1)
  - Second dimension `j` = column index (0 to n-1)
- `dp[i][j]` stores the count of all possible paths from the starting position to cell (i,j)

**In plain language:**
- For each cell (i,j) in the grid, we count how many different paths exist from the top-left corner to that cell
- You can only move right or down, so each path is a sequence of right/down moves
- `dp[0][0]` = 1 path (starting position, no moves needed)
- `dp[n-1][n-1]` = number of paths from start to destination (this is our final answer)

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Subproblem**
- What are we trying to count? The number of paths from top-left (0,0) to bottom-right (n-1, n-1).
- What information do we need? For each position (i,j), we need to know how many paths exist from (0,0) to (i,j).

**Step 2: Define the DP State** (See DP State Definition section above)
- We use `dp[i][j]` to represent the number of paths to position (i,j) (already defined above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[i][j]`?
- To reach (i,j), we can only come from:
  - **Top**: position (i-1, j) if `i > 0`
  - **Left**: position (i, j-1) if `j > 0`
- Therefore: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`
- We sum the paths from both possible previous positions.

**Step 4: Determine Base Cases**
- `dp[0][0] = 1`: There is exactly one way to be at the starting position (by not moving)
- For boundary positions: `dp[0][j] = 1` (only can come from left) and `dp[i][0] = 1` (only can come from top)

**Step 5: Identify the Answer**
- The answer is `dp[n-1][n-1]` - the number of paths to the destination

#### 📊 **Visual DP Table Construction**

For `n = 3`:
```
Step-by-step DP table filling (from top-left to bottom-right):

Initial state:
dp[0][0] = 1  (base case: starting position)

First row (can only come from left):
dp[0][1] = dp[0][0] = 1
dp[0][2] = dp[0][1] = 1

First column (can only come from top):
dp[1][0] = dp[0][0] = 1
dp[2][0] = dp[1][0] = 1

Internal positions:
dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2
dp[1][2] = dp[0][2] + dp[1][1] = 1 + 2 = 3
dp[2][1] = dp[1][1] + dp[2][0] = 2 + 1 = 3
dp[2][2] = dp[1][2] + dp[2][1] = 3 + 3 = 6

Final DP table:
    0  1  2
0   1  1  1
1   1  2  3
2   1  3  6

Answer: dp[2][2] = 6
```

**Algorithm**:
- Initialize `dp[0][0] = 1`
- Fill first row: `dp[0][j] = dp[0][j-1]` for `j > 0`
- Fill first column: `dp[i][0] = dp[i-1][0]` for `i > 0`
- For each position (i,j) where `i > 0` and `j > 0`:
  - `dp[i][j] = dp[i-1][j] + dp[i][j-1]`
- Return `dp[n-1][n-1]`

**Visual Example**:
```
DP table for 3×3 grid:

DP table:
┌─────────────────────────────────────┐
│ dp[2][2] = 1 (destination)         │
│ dp[2][1] = 1 (only right)          │
│ dp[2][0] = 1 (only right)          │
│ dp[1][2] = 1 (only down)           │
│ dp[1][1] = 2 (right + down)        │
│ dp[1][0] = 3 (right + down)        │
│ dp[0][2] = 1 (only down)           │
│ dp[0][1] = 3 (right + down)        │
│ dp[0][0] = 6 (right + down)        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_grid_paths(n, mod=10**9+7):
    """
    Count grid paths using dynamic programming approach
    
    Args:
        n: grid size
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    # Create DP table
    dp = [[0] * n for _ in range(n)]
    
    # Initialize base case
    dp[n-1][n-1] = 1  # Destination
    
    # Fill DP table bottom-up
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue  # Already initialized
            
            # Calculate paths from current position
            right_paths = dp[i][j+1] if j+1 < n else 0
            down_paths = dp[i+1][j] if i+1 < n else 0
            
            dp[i][j] = (right_paths + down_paths) % mod
    
    return dp[0][0]

def dp_grid_paths_optimized(n, mod=10**9+7):
    """
    Optimized dynamic programming grid paths counting
    
    Args:
        n: grid size
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    # Create DP table with optimization
    dp = [[0] * n for _ in range(n)]
    
    # Initialize base case
    dp[n-1][n-1] = 1  # Destination
    
    # Fill DP table bottom-up with optimization
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue  # Already initialized
            
            # Calculate paths from current position
            right_paths = dp[i][j+1] if j+1 < n else 0
            down_paths = dp[i+1][j] if i+1 < n else 0
            
            dp[i][j] = (right_paths + down_paths) % mod
    
    return dp[0][0]

# Example usage
n = 3
result1 = dp_grid_paths(n)
result2 = dp_grid_paths_optimized(n)
print(f"DP grid paths: {result1}")
print(f"Optimized DP grid paths: {result2}")
```

**Time Complexity**: O(n²)
**Space Complexity**: O(n²)

**Why it's better**: Uses dynamic programming for O(n²) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Mathematical Solution (Optimal)

**Key Insights from Mathematical Solution**:
- **Mathematical Formula**: Use combination formula for grid paths
- **Efficient Computation**: O(n) time complexity
- **Space Efficiency**: O(1) space complexity
- **Optimal Complexity**: Best approach for grid path counting

**Key Insight**: Use mathematical formula that the number of paths equals C(2n-2, n-1).

**Algorithm**:
- Use combination formula: C(2n-2, n-1)
- Calculate combination efficiently
- Apply modulo operation

**Visual Example**:
```
Mathematical formula:

For n×n grid:
┌─────────────────────────────────────┐
│ Total moves: 2n-2 (n-1 right, n-1 down) │
│ Number of paths = C(2n-2, n-1)     │
│ For n=3: C(4,2) = 6               │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def mathematical_grid_paths(n, mod=10**9+7):
    """
    Count grid paths using mathematical approach
    
    Args:
        n: grid size
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    def combination(n, k, mod):
        """Calculate C(n,k) modulo mod"""
        if k > n or k < 0:
            return 0
        
        # Use the formula: C(n,k) = n! / (k! * (n-k)!)
        # But calculate it efficiently using modular arithmetic
        result = 1
        for i in range(k):
            result = (result * (n - i)) % mod
            result = (result * pow(i + 1, mod - 2, mod)) % mod
        
        return result
    
    # Number of paths = C(2n-2, n-1)
    return combination(2*n - 2, n - 1, mod)

def mathematical_grid_paths_v2(n, mod=10**9+7):
    """
    Alternative mathematical approach using built-in functions
    
    Args:
        n: grid size
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    import math
    
    # Use built-in combination with modular arithmetic
    return math.comb(2*n - 2, n - 1) % mod

def mathematical_grid_paths_optimized(n, mod=10**9+7):
    """
    Optimized mathematical grid paths counting
    
    Args:
        n: grid size
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    def fast_combination(n, k, mod):
        """Fast combination calculation with optimizations"""
        if k > n or k < 0:
            return 0
        
        # Optimize by using smaller k
        k = min(k, n - k)
        
        result = 1
        for i in range(k):
            result = (result * (n - i)) % mod
            result = (result * pow(i + 1, mod - 2, mod)) % mod
        
        return result
    
    # Number of paths = C(2n-2, n-1)
    return fast_combination(2*n - 2, n - 1, mod)

# Example usage
n = 3
result1 = mathematical_grid_paths(n)
result2 = mathematical_grid_paths_v2(n)
result3 = mathematical_grid_paths_optimized(n)
print(f"Mathematical grid paths: {result1}")
print(f"Mathematical grid paths v2: {result2}")
print(f"Optimized mathematical grid paths: {result3}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses mathematical formula for O(n) time and O(1) space complexity.

**Implementation Details**:
- **Mathematical Formula**: Use C(2n-2, n-1) formula for grid paths
- **Efficient Computation**: Use optimized combination calculation
- **Space Efficiency**: Use only necessary variables
- **Modular Arithmetic**: Use efficient modular arithmetic

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^(2n)) | O(n) | Complete enumeration of all paths |
| Dynamic Programming | O(n²) | O(n²) | Use DP to avoid recalculating subproblems |
| Mathematical | O(n) | O(1) | Use C(2n-2, n-1) formula with modular arithmetic |

### Time Complexity
- **Time**: O(n) - Use mathematical formula for efficient calculation
- **Space**: O(1) - Use mathematical approach

### Why This Solution Works
- **Mathematical Formula**: Use C(2n-2, n-1) formula for grid paths
- **Efficient Computation**: Use optimized combination calculation
- **Space Efficiency**: Use only necessary variables
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Grid Paths with Obstacles**
**Problem**: Count grid paths with obstacles on the grid.

**Key Differences**: Some cells are blocked

**Solution Approach**: Modify DP to handle obstacles

**Implementation**:
```python
def obstacle_grid_paths(n, obstacles, mod=10**9+7):
    """
    Count grid paths with obstacles
    
    Args:
        n: grid size
        obstacles: list of blocked positions
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    # Create DP table
    dp = [[0] * n for _ in range(n)]
    
    # Initialize base case
    if (n-1, n-1) not in obstacles:
        dp[n-1][n-1] = 1  # Destination
    
    # Fill DP table bottom-up
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue  # Already initialized
            
            if (i, j) in obstacles:
                dp[i][j] = 0  # Blocked cell
                continue
            
            # Calculate paths from current position
            right_paths = dp[i][j+1] if j+1 < n else 0
            down_paths = dp[i+1][j] if i+1 < n else 0
            
            dp[i][j] = (right_paths + down_paths) % mod
    
    return dp[0][0]

# Example usage
n = 3
obstacles = [(1, 1)]  # Block position (1,1)
result = obstacle_grid_paths(n, obstacles)
print(f"Obstacle grid paths: {result}")
```

#### **2. Grid Paths with Different Costs**
**Problem**: Count grid paths with different costs for moves.

**Key Differences**: Different costs for different moves

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def cost_grid_paths(n, costs, mod=10**9+7):
    """
    Count grid paths with different costs
    
    Args:
        n: grid size
        costs: 2D array of costs
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    # Create DP table
    dp = [[0] * n for _ in range(n)]
    
    # Initialize base case
    dp[n-1][n-1] = 1  # Destination
    
    # Fill DP table bottom-up
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == n-1 and j == n-1:
                continue  # Already initialized
            
            # Calculate paths from current position
            right_paths = dp[i][j+1] if j+1 < n else 0
            down_paths = dp[i+1][j] if i+1 < n else 0
            
            dp[i][j] = (right_paths + down_paths) % mod
    
    return dp[0][0]

# Example usage
n = 3
costs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Cost matrix
result = cost_grid_paths(n, costs)
print(f"Cost grid paths: {result}")
```

#### **3. Grid Paths with Multiple Destinations**
**Problem**: Count grid paths to multiple destinations.

**Key Differences**: Handle multiple destinations

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_destination_grid_paths(n, destinations, mod=10**9+7):
    """
    Count grid paths to multiple destinations
    
    Args:
        n: grid size
        destinations: list of destination positions
        mod: modulo value
    
    Returns:
        int: number of paths modulo mod
    """
    # Create DP table
    dp = [[0] * n for _ in range(n)]
    
    # Initialize base cases for all destinations
    for dest_row, dest_col in destinations:
        dp[dest_row][dest_col] = 1
    
    # Fill DP table bottom-up
    for i in range(n-1, -1, -1):
        for j in range(n-1, -1, -1):
            if (i, j) in destinations:
                continue  # Already initialized
            
            # Calculate paths from current position
            right_paths = dp[i][j+1] if j+1 < n else 0
            down_paths = dp[i+1][j] if i+1 < n else 0
            
            dp[i][j] = (right_paths + down_paths) % mod
    
    return dp[0][0]

# Example usage
n = 3
destinations = [(2, 2), (1, 2), (2, 1)]  # Multiple destinations
result = multi_destination_grid_paths(n, destinations)
print(f"Multi-destination grid paths: {result}")
```

## Problem Variations

### **Variation 1: Grid Paths with Dynamic Updates**
**Problem**: Handle dynamic grid updates (add/remove/update obstacles) while maintaining optimal path counting efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic grid management.

```python
from collections import defaultdict

class DynamicGridPaths:
    def __init__(self, rows=None, cols=None, obstacles=None):
        self.rows = rows or 0
        self.cols = cols or 0
        self.obstacles = obstacles or set()
        self.paths = []
        self._update_grid_paths_info()
    
    def _update_grid_paths_info(self):
        """Update grid paths feasibility information."""
        self.grid_paths_feasibility = self._calculate_grid_paths_feasibility()
    
    def _calculate_grid_paths_feasibility(self):
        """Calculate grid paths feasibility."""
        if self.rows <= 0 or self.cols <= 0:
            return 0.0
        
        # Check if we can find paths in the grid
        return 1.0 if self.rows > 0 and self.cols > 0 else 0.0
    
    def update_grid_size(self, new_rows, new_cols):
        """Update grid dimensions."""
        self.rows = new_rows
        self.cols = new_cols
        self._update_grid_paths_info()
    
    def add_obstacle(self, row, col):
        """Add obstacle at position (row, col)."""
        self.obstacles.add((row, col))
    
    def remove_obstacle(self, row, col):
        """Remove obstacle at position (row, col)."""
        self.obstacles.discard((row, col))
    
    def count_paths(self):
        """Count number of paths from (0,0) to (rows-1, cols-1) using dynamic programming."""
        if not self.grid_paths_feasibility:
            return 0
        
        # DP table: dp[i][j] = number of paths to reach (i, j)
        dp = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Base case: one path to reach (0, 0)
        if (0, 0) not in self.obstacles:
            dp[0][0] = 1
        
        # Fill DP table
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) in self.obstacles:
                    dp[i][j] = 0
                    continue
                
                if i == 0 and j == 0:
                    continue
                
                # Can come from top or left
                if i > 0:
                    dp[i][j] += dp[i-1][j]
                if j > 0:
                    dp[i][j] += dp[i][j-1]
        
        return dp[self.rows-1][self.cols-1]
    
    def get_paths_with_constraints(self, constraint_func):
        """Get paths that satisfies custom constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        count = self.count_paths()
        if constraint_func(count, self.rows, self.cols):
            return self._generate_paths()
        else:
            return []
    
    def get_paths_in_range(self, min_paths, max_paths):
        """Get paths within specified count range."""
        if not self.grid_paths_feasibility:
            return []
        
        count = self.count_paths()
        if min_paths <= count <= max_paths:
            return self._generate_paths()
        else:
            return []
    
    def get_paths_with_pattern(self, pattern_func):
        """Get paths matching specified pattern."""
        if not self.grid_paths_feasibility:
            return []
        
        count = self.count_paths()
        if pattern_func(count, self.rows, self.cols):
            return self._generate_paths()
        else:
            return []
    
    def _generate_paths(self):
        """Generate all possible paths from (0,0) to (rows-1, cols-1)."""
        if not self.grid_paths_feasibility:
            return []
        
        paths = []
        
        def backtrack(row, col, current_path):
            if row == self.rows - 1 and col == self.cols - 1:
                paths.append(current_path[:])
                return
            
            if (row, col) in self.obstacles:
                return
            
            # Move right
            if col + 1 < self.cols:
                current_path.append((row, col + 1))
                backtrack(row, col + 1, current_path)
                current_path.pop()
            
            # Move down
            if row + 1 < self.rows:
                current_path.append((row + 1, col))
                backtrack(row + 1, col, current_path)
                current_path.pop()
        
        backtrack(0, 0, [(0, 0)])
        return paths
    
    def get_grid_paths_statistics(self):
        """Get statistics about the grid paths."""
        if not self.grid_paths_feasibility:
            return {
                'rows': 0,
                'cols': 0,
                'grid_paths_feasibility': 0,
                'path_count': 0
            }
        
        count = self.count_paths()
        return {
            'rows': self.rows,
            'cols': self.cols,
            'grid_paths_feasibility': self.grid_paths_feasibility,
            'path_count': count
        }
    
    def get_grid_paths_patterns(self):
        """Get patterns in grid paths."""
        patterns = {
            'paths_exist': 0,
            'has_valid_grid': 0,
            'optimal_paths_possible': 0,
            'has_large_grid': 0
        }
        
        if not self.grid_paths_feasibility:
            return patterns
        
        # Check if paths exist
        if self.grid_paths_feasibility == 1.0:
            patterns['paths_exist'] = 1
        
        # Check if has valid grid
        if self.rows > 0 and self.cols > 0:
            patterns['has_valid_grid'] = 1
        
        # Check if optimal paths are possible
        if self.grid_paths_feasibility == 1.0:
            patterns['optimal_paths_possible'] = 1
        
        # Check if has large grid
        if self.rows > 10 or self.cols > 10:
            patterns['has_large_grid'] = 1
        
        return patterns
    
    def get_optimal_grid_paths_strategy(self):
        """Get optimal strategy for grid paths counting."""
        if not self.grid_paths_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'grid_paths_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.grid_paths_feasibility
        
        # Calculate grid paths feasibility
        grid_paths_feasibility = self.grid_paths_feasibility
        
        # Determine recommended strategy
        if self.rows <= 20 and self.cols <= 20:
            recommended_strategy = 'dynamic_programming'
        elif self.rows <= 100 and self.cols <= 100:
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'grid_paths_feasibility': grid_paths_feasibility
        }

# Example usage
rows = 3
cols = 3
obstacles = {(1, 1)}  # Obstacle at center
dynamic_grid_paths = DynamicGridPaths(rows, cols, obstacles)
print(f"Grid paths feasibility: {dynamic_grid_paths.grid_paths_feasibility}")

# Update grid size
dynamic_grid_paths.update_grid_size(4, 4)
print(f"After updating grid size: {dynamic_grid_paths.rows}x{dynamic_grid_paths.cols}")

# Add obstacle
dynamic_grid_paths.add_obstacle(2, 2)
print(f"Added obstacle at (2, 2)")

# Count paths
count = dynamic_grid_paths.count_paths()
print(f"Number of paths: {count}")

# Get paths with constraints
def constraint_func(count, rows, cols):
    return count > 0 and rows > 0 and cols > 0

print(f"Paths with constraints: {len(dynamic_grid_paths.get_paths_with_constraints(constraint_func))}")

# Get paths in range
print(f"Paths in range 1-100: {len(dynamic_grid_paths.get_paths_in_range(1, 100))}")

# Get paths with pattern
def pattern_func(count, rows, cols):
    return count > 0 and rows > 0 and cols > 0

print(f"Paths with pattern: {len(dynamic_grid_paths.get_paths_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_grid_paths.get_grid_paths_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_grid_paths.get_grid_paths_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_grid_paths.get_optimal_grid_paths_strategy()}")
```

### **Variation 2: Grid Paths with Different Operations**
**Problem**: Handle different types of grid path operations (weighted paths, priority-based path finding, advanced grid analysis).

**Approach**: Use advanced data structures for efficient different types of grid path operations.

```python
class AdvancedGridPaths:
    def __init__(self, rows=None, cols=None, weights=None, priorities=None):
        self.rows = rows or 0
        self.cols = cols or 0
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.paths = []
        self._update_grid_paths_info()
    
    def _update_grid_paths_info(self):
        """Update grid paths feasibility information."""
        self.grid_paths_feasibility = self._calculate_grid_paths_feasibility()
    
    def _calculate_grid_paths_feasibility(self):
        """Calculate grid paths feasibility."""
        if self.rows <= 0 or self.cols <= 0:
            return 0.0
        
        # Check if we can find paths in the grid
        return 1.0 if self.rows > 0 and self.cols > 0 else 0.0
    
    def count_paths(self):
        """Count number of paths from (0,0) to (rows-1, cols-1) using dynamic programming."""
        if not self.grid_paths_feasibility:
            return 0
        
        # DP table: dp[i][j] = number of paths to reach (i, j)
        dp = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Base case: one path to reach (0, 0)
        dp[0][0] = 1
        
        # Fill DP table
        for i in range(self.rows):
            for j in range(self.cols):
                if i == 0 and j == 0:
                    continue
                
                # Can come from top or left
                if i > 0:
                    dp[i][j] += dp[i-1][j]
                if j > 0:
                    dp[i][j] += dp[i][j-1]
        
        return dp[self.rows-1][self.cols-1]
    
    def get_weighted_paths(self):
        """Get paths with weights and priorities applied."""
        if not self.grid_paths_feasibility:
            return []
        
        # Create weighted grid
        weighted_grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                weight = self.weights.get((i, j), 1)
                priority = self.priorities.get((i, j), 1)
                weighted_score = weight * priority
                row.append(weighted_score)
            weighted_grid.append(row)
        
        # Generate paths with weighted scores
        paths = []
        
        def backtrack(row, col, current_path, current_score):
            if row == self.rows - 1 and col == self.cols - 1:
                paths.append((current_path[:], current_score))
                return
            
            # Move right
            if col + 1 < self.cols:
                new_score = current_score + weighted_grid[row][col + 1]
                current_path.append((row, col + 1))
                backtrack(row, col + 1, current_path, new_score)
                current_path.pop()
            
            # Move down
            if row + 1 < self.rows:
                new_score = current_score + weighted_grid[row + 1][col]
                current_path.append((row + 1, col))
                backtrack(row + 1, col, current_path, new_score)
                current_path.pop()
        
        backtrack(0, 0, [(0, 0)], weighted_grid[0][0])
        return paths
    
    def get_paths_with_priority(self, priority_func):
        """Get paths considering priority."""
        if not self.grid_paths_feasibility:
            return []
        
        # Create priority-based weights
        priority_weights = {}
        for i in range(self.rows):
            for j in range(self.cols):
                priority = priority_func((i, j), self.weights, self.priorities)
                priority_weights[(i, j)] = priority
        
        # Generate paths with priority weights
        paths = []
        
        def backtrack(row, col, current_path, current_priority):
            if row == self.rows - 1 and col == self.cols - 1:
                paths.append((current_path[:], current_priority))
                return
            
            # Move right
            if col + 1 < self.cols:
                new_priority = current_priority + priority_weights.get((row, col + 1), 1)
                current_path.append((row, col + 1))
                backtrack(row, col + 1, current_path, new_priority)
                current_path.pop()
            
            # Move down
            if row + 1 < self.rows:
                new_priority = current_priority + priority_weights.get((row + 1, col), 1)
                current_path.append((row + 1, col))
                backtrack(row + 1, col, current_path, new_priority)
                current_path.pop()
        
        backtrack(0, 0, [(0, 0)], priority_weights.get((0, 0), 1))
        return paths
    
    def get_paths_with_optimization(self, optimization_func):
        """Get paths using custom optimization function."""
        if not self.grid_paths_feasibility:
            return []
        
        # Create optimization-based weights
        optimized_weights = {}
        for i in range(self.rows):
            for j in range(self.cols):
                score = optimization_func((i, j), self.weights, self.priorities)
                optimized_weights[(i, j)] = score
        
        # Generate paths with optimized weights
        paths = []
        
        def backtrack(row, col, current_path, current_score):
            if row == self.rows - 1 and col == self.cols - 1:
                paths.append((current_path[:], current_score))
                return
            
            # Move right
            if col + 1 < self.cols:
                new_score = current_score + optimized_weights.get((row, col + 1), 1)
                current_path.append((row, col + 1))
                backtrack(row, col + 1, current_path, new_score)
                current_path.pop()
            
            # Move down
            if row + 1 < self.rows:
                new_score = current_score + optimized_weights.get((row + 1, col), 1)
                current_path.append((row + 1, col))
                backtrack(row + 1, col, current_path, new_score)
                current_path.pop()
        
        backtrack(0, 0, [(0, 0)], optimized_weights.get((0, 0), 1))
        return paths
    
    def get_paths_with_constraints(self, constraint_func):
        """Get paths that satisfies custom constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        if constraint_func(self.rows, self.cols, self.weights, self.priorities):
            return self.get_weighted_paths()
        else:
            return []
    
    def get_paths_with_multiple_criteria(self, criteria_list):
        """Get paths that satisfies multiple criteria."""
        if not self.grid_paths_feasibility:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.rows, self.cols, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_paths()
        else:
            return []
    
    def get_paths_with_alternatives(self, alternatives):
        """Get paths considering alternative weights/priorities."""
        result = []
        
        # Check original paths
        original_paths = self.get_weighted_paths()
        result.append((original_paths, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedGridPaths(self.rows, self.cols, alt_weights, alt_priorities)
            temp_paths = temp_instance.get_weighted_paths()
            result.append((temp_paths, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_paths_with_adaptive_criteria(self, adaptive_func):
        """Get paths using adaptive criteria."""
        if not self.grid_paths_feasibility:
            return []
        
        if adaptive_func(self.rows, self.cols, self.weights, self.priorities, []):
            return self.get_weighted_paths()
        else:
            return []
    
    def get_grid_paths_optimization(self):
        """Get optimal grid paths configuration."""
        strategies = [
            ('weighted_paths', lambda: len(self.get_weighted_paths())),
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
rows = 3
cols = 3
weights = {(i, j): (i + j + 1) for i in range(rows) for j in range(cols)}  # Weight based on position
priorities = {(i, j): (i * j + 1) for i in range(rows) for j in range(cols)}  # Priority based on position
advanced_grid_paths = AdvancedGridPaths(rows, cols, weights, priorities)

print(f"Weighted paths: {len(advanced_grid_paths.get_weighted_paths())}")

# Get paths with priority
def priority_func(position, weights, priorities):
    return weights.get(position, 1) + priorities.get(position, 1)

print(f"Paths with priority: {len(advanced_grid_paths.get_paths_with_priority(priority_func))}")

# Get paths with optimization
def optimization_func(position, weights, priorities):
    return weights.get(position, 1) * priorities.get(position, 1)

print(f"Paths with optimization: {len(advanced_grid_paths.get_paths_with_optimization(optimization_func))}")

# Get paths with constraints
def constraint_func(rows, cols, weights, priorities):
    return rows > 0 and cols > 0

print(f"Paths with constraints: {len(advanced_grid_paths.get_paths_with_constraints(constraint_func))}")

# Get paths with multiple criteria
def criterion1(rows, cols, weights, priorities):
    return rows > 0

def criterion2(rows, cols, weights, priorities):
    return cols > 0

criteria_list = [criterion1, criterion2]
print(f"Paths with multiple criteria: {len(advanced_grid_paths.get_paths_with_multiple_criteria(criteria_list))}")

# Get paths with alternatives
alternatives = [({(i, j): 1 for i in range(rows) for j in range(cols)}, {(i, j): 1 for i in range(rows) for j in range(cols)}), ({(i, j): (i+j)*2 for i in range(rows) for j in range(cols)}, {(i, j): (i*j)+1 for i in range(rows) for j in range(cols)})]
print(f"Paths with alternatives: {advanced_grid_paths.get_paths_with_alternatives(alternatives)}")

# Get paths with adaptive criteria
def adaptive_func(rows, cols, weights, priorities, current_result):
    return rows > 0 and cols > 0 and len(current_result) < 5

print(f"Paths with adaptive criteria: {len(advanced_grid_paths.get_paths_with_adaptive_criteria(adaptive_func))}")

# Get grid paths optimization
print(f"Grid paths optimization: {advanced_grid_paths.get_grid_paths_optimization()}")
```

### **Variation 3: Grid Paths with Constraints**
**Problem**: Handle grid path counting with additional constraints (grid limits, movement constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedGridPaths:
    def __init__(self, rows=None, cols=None, constraints=None):
        self.rows = rows or 0
        self.cols = cols or 0
        self.constraints = constraints or {}
        self.paths = []
        self._update_grid_paths_info()
    
    def _update_grid_paths_info(self):
        """Update grid paths feasibility information."""
        self.grid_paths_feasibility = self._calculate_grid_paths_feasibility()
    
    def _calculate_grid_paths_feasibility(self):
        """Calculate grid paths feasibility."""
        if self.rows <= 0 or self.cols <= 0:
            return 0.0
        
        # Check if we can find paths in the grid
        return 1.0 if self.rows > 0 and self.cols > 0 else 0.0
    
    def _is_valid_move(self, from_pos, to_pos):
        """Check if move is valid considering constraints."""
        # Movement constraints
        if 'allowed_moves' in self.constraints:
            if (from_pos, to_pos) not in self.constraints['allowed_moves']:
                return False
        
        if 'forbidden_moves' in self.constraints:
            if (from_pos, to_pos) in self.constraints['forbidden_moves']:
                return False
        
        # Position constraints
        if 'allowed_positions' in self.constraints:
            if to_pos not in self.constraints['allowed_positions']:
                return False
        
        if 'forbidden_positions' in self.constraints:
            if to_pos in self.constraints['forbidden_positions']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(from_pos, to_pos):
                    return False
        
        return True
    
    def get_paths_with_grid_constraints(self, min_rows, max_rows, min_cols, max_cols):
        """Get paths considering grid size constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        if min_rows <= self.rows <= max_rows and min_cols <= self.cols <= max_cols:
            return self._generate_constrained_paths()
        else:
            return []
    
    def get_paths_with_movement_constraints(self, movement_constraints):
        """Get paths considering movement constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        satisfies_constraints = True
        for constraint in movement_constraints:
            if not constraint(self.rows, self.cols):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self._generate_constrained_paths()
        else:
            return []
    
    def get_paths_with_pattern_constraints(self, pattern_constraints):
        """Get paths considering pattern constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.rows, self.cols):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self._generate_constrained_paths()
        else:
            return []
    
    def get_paths_with_mathematical_constraints(self, constraint_func):
        """Get paths that satisfies custom mathematical constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        if constraint_func(self.rows, self.cols):
            return self._generate_constrained_paths()
        else:
            return []
    
    def get_paths_with_optimization_constraints(self, optimization_func):
        """Get paths using custom optimization constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        # Calculate optimization score for paths
        score = optimization_func(self.rows, self.cols)
        
        if score > 0:
            return self._generate_constrained_paths()
        else:
            return []
    
    def get_paths_with_multiple_constraints(self, constraints_list):
        """Get paths that satisfies multiple constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.rows, self.cols):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self._generate_constrained_paths()
        else:
            return []
    
    def get_paths_with_priority_constraints(self, priority_func):
        """Get paths with priority-based constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        # Calculate priority for paths
        priority = priority_func(self.rows, self.cols)
        
        if priority > 0:
            return self._generate_constrained_paths()
        else:
            return []
    
    def get_paths_with_adaptive_constraints(self, adaptive_func):
        """Get paths with adaptive constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        if adaptive_func(self.rows, self.cols, []):
            return self._generate_constrained_paths()
        else:
            return []
    
    def _generate_constrained_paths(self):
        """Generate all possible paths considering constraints."""
        if not self.grid_paths_feasibility:
            return []
        
        paths = []
        
        def backtrack(row, col, current_path):
            if row == self.rows - 1 and col == self.cols - 1:
                paths.append(current_path[:])
                return
            
            # Move right
            if col + 1 < self.cols:
                from_pos = (row, col)
                to_pos = (row, col + 1)
                if self._is_valid_move(from_pos, to_pos):
                    current_path.append(to_pos)
                    backtrack(row, col + 1, current_path)
                    current_path.pop()
            
            # Move down
            if row + 1 < self.rows:
                from_pos = (row, col)
                to_pos = (row + 1, col)
                if self._is_valid_move(from_pos, to_pos):
                    current_path.append(to_pos)
                    backtrack(row + 1, col, current_path)
                    current_path.pop()
        
        backtrack(0, 0, [(0, 0)])
        return paths
    
    def get_optimal_grid_paths_strategy(self):
        """Get optimal grid paths strategy considering all constraints."""
        strategies = [
            ('grid_constraints', self.get_paths_with_grid_constraints),
            ('movement_constraints', self.get_paths_with_movement_constraints),
            ('pattern_constraints', self.get_paths_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'grid_constraints':
                    result = strategy_func(0, 1000, 0, 1000)
                elif strategy_name == 'movement_constraints':
                    movement_constraints = [lambda rows, cols: rows > 0 and cols > 0]
                    result = strategy_func(movement_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda rows, cols: rows > 0 and cols > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_moves': [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 1), (0, 2)), ((0, 1), (1, 1)), ((1, 0), (1, 1)), ((1, 0), (2, 0)), ((0, 2), (1, 2)), ((1, 1), (1, 2)), ((1, 1), (2, 1)), ((2, 0), (2, 1)), ((1, 2), (2, 2)), ((2, 1), (2, 2))],
    'forbidden_moves': [],
    'allowed_positions': [(i, j) for i in range(3) for j in range(3)],
    'forbidden_positions': [],
    'pattern_constraints': [lambda from_pos, to_pos: from_pos[0] <= to_pos[0] and from_pos[1] <= to_pos[1]]
}

rows = 3
cols = 3
constrained_grid_paths = ConstrainedGridPaths(rows, cols, constraints)

print("Grid-constrained paths:", len(constrained_grid_paths.get_paths_with_grid_constraints(1, 10, 1, 10)))

print("Movement-constrained paths:", len(constrained_grid_paths.get_paths_with_movement_constraints([lambda rows, cols: rows > 0 and cols > 0])))

print("Pattern-constrained paths:", len(constrained_grid_paths.get_paths_with_pattern_constraints([lambda rows, cols: rows > 0 and cols > 0])))

# Mathematical constraints
def custom_constraint(rows, cols):
    return rows > 0 and cols > 0

print("Mathematical constraint paths:", len(constrained_grid_paths.get_paths_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(rows, cols):
    return 1 <= rows <= 10 and 1 <= cols <= 10

range_constraints = [range_constraint]
print("Range-constrained paths:", len(constrained_grid_paths.get_paths_with_grid_constraints(1, 10, 1, 10)))

# Multiple constraints
def constraint1(rows, cols):
    return rows > 0

def constraint2(rows, cols):
    return cols > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints paths:", len(constrained_grid_paths.get_paths_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(rows, cols):
    return rows + cols

print("Priority-constrained paths:", len(constrained_grid_paths.get_paths_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(rows, cols, current_result):
    return rows > 0 and cols > 0 and len(current_result) < 5

print("Adaptive constraint paths:", len(constrained_grid_paths.get_paths_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_grid_paths.get_optimal_grid_paths_strategy()
print(f"Optimal grid paths strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Minimal Grid Path](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Array Description](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Book Shop](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Grid DP
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Grid DP
- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) - Grid DP

#### **Problem Categories**
- **Dynamic Programming**: Grid DP, path counting
- **Combinatorics**: Mathematical counting, combination properties
- **Mathematical Algorithms**: Modular arithmetic, optimization

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Grid Algorithms](https://cp-algorithms.com/geometry/basic-geometry.html) - Grid algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques

### **Practice Problems**
- [CSES Minimal Grid Path](https://cses.fi/problemset/task/1075) - Medium
- [CSES Array Description](https://cses.fi/problemset/task/1075) - Medium
- [CSES Book Shop](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
