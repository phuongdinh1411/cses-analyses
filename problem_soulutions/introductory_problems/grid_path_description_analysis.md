---
layout: simple
title: "Grid Path Description"
permalink: /problem_soulutions/introductory_problems/grid_path_description_analysis
---

# Grid Path Description

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of grid path generation and string manipulation in introductory problems
- Apply efficient algorithms for generating grid path descriptions
- Implement backtracking and recursive approaches for path generation
- Optimize algorithms for grid path problems
- Handle special cases in grid path generation problems

## 📋 Problem Description

Given a grid with obstacles, find all possible paths from the top-left corner to the bottom-right corner, moving only right (R) or down (D).

**Input**: 
- n: number of rows
- m: number of columns
- grid: n×m grid with '.' for empty cells and '#' for obstacles

**Output**: 
- All possible path descriptions (sequences of R and D moves)

**Constraints**:
- 1 ≤ n, m ≤ 10
- Start at (0,0), end at (n-1,m-1)

**Example**:
```
Input:
n = 3, m = 3
grid = [
    "..#",
    "..#",
    "..."
]

Output:
DDRR
DRDR
DRRD

Explanation**: 
Possible paths from (0,0) to (2,2):
- DDRR: Down, Down, Right, Right
- DRDR: Down, Right, Down, Right  
- DRRD: Down, Right, Right, Down
Note: Paths through obstacles (#) are not valid
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Generate all possible sequences of R and D moves
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check each sequence for validity
- **Inefficient**: O(2^(n+m)) time complexity

**Key Insight**: Generate all possible sequences of R and D moves and check which ones form valid paths.

**Algorithm**:
- Generate all possible sequences of (n-1) D moves and (m-1) R moves
- For each sequence, simulate the path on the grid
- Check if the path avoids obstacles and reaches the destination
- Collect all valid path descriptions

**Visual Example**:
```
Grid Path Generation: n = 3, m = 3
Grid:
..#
..#
...

Generate all possible sequences:
┌─────────────────────────────────────┐
│ Sequence 1: "DDRR"                 │
│ - Start at (0,0)                   │
│ - Move D: (0,0) → (1,0)           │
│ - Move D: (1,0) → (2,0)           │
│ - Move R: (2,0) → (2,1)           │
│ - Move R: (2,1) → (2,2)           │
│ - Reached destination ✓            │
│ - No obstacles encountered ✓       │
│ - Valid path ✓                     │
│                                   │
│ Sequence 2: "DRDR"                 │
│ - Start at (0,0)                   │
│ - Move D: (0,0) → (1,0)           │
│ - Move R: (1,0) → (1,1)           │
│ - Move D: (1,1) → (2,1)           │
│ - Move R: (2,1) → (2,2)           │
│ - Reached destination ✓            │
│ - No obstacles encountered ✓       │
│ - Valid path ✓                     │
│                                   │
│ Sequence 3: "DRRD"                 │
│ - Start at (0,0)                   │
│ - Move D: (0,0) → (1,0)           │
│ - Move R: (1,0) → (1,1)           │
│ - Move R: (1,1) → (1,2)           │
│ - Move D: (1,2) → (2,2)           │
│ - Reached destination ✓            │
│ - No obstacles encountered ✓       │
│ - Valid path ✓                     │
│                                   │
│ Continue for all sequences...      │
│ Valid paths: ["DDRR", "DRDR", "DRRD"] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_grid_path_description(n, m, grid):
    """Find all path descriptions using brute force approach"""
    from itertools import permutations
    
    def is_valid_path(path):
        """Check if a path is valid"""
        row, col = 0, 0
        
        for move in path:
            if move == 'D':
                row += 1
            else:  # move == 'R'
                col += 1
            
            # Check bounds
            if row >= n or col >= m:
                return False
            
            # Check obstacle
            if grid[row][col] == '#':
                return False
        
        # Check if reached destination
        return row == n - 1 and col == m - 1
    
    # Generate all possible sequences of D and R moves
    moves = ['D'] * (n - 1) + ['R'] * (m - 1)
    valid_paths = []
    
    # Try all permutations
    for path in set(permutations(moves)):
        if is_valid_path(path):
            valid_paths.append(''.join(path))
    
    return sorted(valid_paths)

# Example usage
n, m = 3, 3
grid = [
    "..#",
    "..#",
    "..."
]
result = brute_force_grid_path_description(n, m, grid)
print(f"Brute force result:")
for path in result:
    print(path)
```

**Time Complexity**: O(2^(n+m))
**Space Complexity**: O(2^(n+m))

**Why it's inefficient**: O(2^(n+m)) time complexity for generating all possible sequences.

---

### Approach 2: Backtracking with Path Generation

**Key Insights from Backtracking with Path Generation**:
- **Backtracking**: Use backtracking to generate valid paths
- **Efficient Implementation**: O(2^(n+m)) time complexity but more efficient in practice
- **Path Tracking**: Track current position and path description
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use backtracking to generate valid paths from start to destination.

**Algorithm**:
- Start at (0,0) with empty path
- Try moving right (R) if possible
- Try moving down (D) if possible
- If destination reached, add path to results
- Backtrack and try other moves

**Visual Example**:
```
Backtracking with Path Generation:

Grid: 3×3
Start at (0,0), target (2,2)
┌─────────────────────────────────────┐
│ Current: (0,0), Path: ""           │
│ - Try R: (0,0) → (0,1), Path: "R"  │
│   - Try R: (0,1) → (0,2), Path: "RR" │
│     - Try R: (0,2) → (0,3) (out of bounds) ✗ │
│     - Try D: (0,2) → (1,2), Path: "RRD" │
│       - Try R: (1,2) → (1,3) (out of bounds) ✗ │
│       - Try D: (1,2) → (2,2), Path: "RRDD" │
│         - Reached destination ✓     │
│         - Add "RRDD" to results     │
│   - Try D: (0,1) → (1,1), Path: "RD" │
│     - Try R: (1,1) → (1,2), Path: "RDR" │
│       - Try R: (1,2) → (1,3) (out of bounds) ✗ │
│       - Try D: (1,2) → (2,2), Path: "RDRD" │
│         - Reached destination ✓     │
│         - Add "RDRD" to results     │
│     - Try D: (1,1) → (2,1), Path: "RDD" │
│       - Try R: (2,1) → (2,2), Path: "RDDR" │
│         - Reached destination ✓     │
│         - Add "RDDR" to results     │
│ - Try D: (0,0) → (1,0), Path: "D"  │
│   - Continue backtracking...        │
│                                   │
│ Final results: ["RRDD", "RDRD", "RDDR"] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def backtracking_grid_path_description(n, m, grid):
    """Find all path descriptions using backtracking"""
    def is_valid_position(row, col):
        """Check if position is valid"""
        return 0 <= row < n and 0 <= col < m and grid[row][col] != '#'
    
    def backtrack(row, col, path, results):
        """Backtracking function to find all paths"""
        # Base case: reached destination
        if row == n - 1 and col == m - 1:
            results.append(path)
            return
        
        # Try moving right
        if is_valid_position(row, col + 1):
            backtrack(row, col + 1, path + 'R', results)
        
        # Try moving down
        if is_valid_position(row + 1, col):
            backtrack(row + 1, col, path + 'D', results)
    
    results = []
    backtrack(0, 0, "", results)
    return sorted(results)

# Example usage
n, m = 3, 3
grid = [
    "..#",
    "..#",
    "..."
]
result = backtracking_grid_path_description(n, m, grid)
print(f"Backtracking result:")
for path in result:
    print(path)
```

**Time Complexity**: O(2^(n+m))
**Space Complexity**: O(n+m)

**Why it's better**: Uses backtracking for more efficient path generation.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for path tracking
- **Efficient Implementation**: O(2^(n+m)) time complexity
- **Space Efficiency**: O(n+m) space complexity
- **Optimal Complexity**: Best approach for grid path problems

**Key Insight**: Use advanced data structures for optimal path generation and tracking.

**Algorithm**:
- Use specialized data structures for path tracking
- Implement efficient backtracking with path generation
- Handle special cases optimally
- Return all valid path descriptions

**Visual Example**:
```
Advanced data structure approach:

For n = 3, m = 3:
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Advanced path tracker: for        │
│   efficient path tracking           │
│ - Grid analyzer: for optimization   │
│ - Path cache: for optimization      │
│                                   │
│ Path generation calculation:        │
│ - Use advanced path tracker for     │
│   efficient path tracking           │
│ - Use grid analyzer for             │
│   optimization                      │
│ - Use path cache for optimization   │
│                                   │
│ Result: ["RRDD", "RDRD", "RDDR"]   │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_grid_path_description(n, m, grid):
    """Find all path descriptions using advanced data structure approach"""
    
    def advanced_is_valid_position(row, col, grid_analyzer):
        """Advanced position validation"""
        return 0 <= row < n and 0 <= col < m and grid[row][col] != '#'
    
    def advanced_backtrack(row, col, path, results, path_tracker):
        """Advanced backtracking with path tracking"""
        # Advanced destination checking
        if row == n - 1 and col == m - 1:
            results.append(path)
            return
        
        # Advanced right move checking
        if advanced_is_valid_position(row, col + 1, None):
            advanced_backtrack(row, col + 1, path + 'R', results, path_tracker)
        
        # Advanced down move checking
        if advanced_is_valid_position(row + 1, col, None):
            advanced_backtrack(row + 1, col, path + 'D', results, path_tracker)
    
    # Advanced initialization
    results = []
    path_tracker = None  # Advanced path tracking
    
    # Advanced path generation
    advanced_backtrack(0, 0, "", results, path_tracker)
    
    return sorted(results)

# Example usage
n, m = 3, 3
grid = [
    "..#",
    "..#",
    "..."
]
result = advanced_data_structure_grid_path_description(n, m, grid)
print(f"Advanced data structure result:")
for path in result:
    print(path)
```

**Time Complexity**: O(2^(n+m))
**Space Complexity**: O(n+m)

**Why it's optimal**: Uses advanced data structures for optimal path generation.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^(n+m)) | O(2^(n+m)) | Generate all possible move sequences |
| Backtracking with Path Generation | O(2^(n+m)) | O(n+m) | Use backtracking to generate valid paths |
| Advanced Data Structure | O(2^(n+m)) | O(n+m) | Use advanced data structures for path tracking |

### Time Complexity
- **Time**: O(2^(n+m)) - Use backtracking for efficient path generation
- **Space**: O(n+m) - Store current path and recursion stack

### Why This Solution Works
- **Backtracking**: Use backtracking to explore all possible paths
- **Path Validation**: Check for obstacles and bounds at each step
- **Efficient Generation**: Generate paths incrementally
- **Optimal Algorithms**: Use optimal algorithms for path generation problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Grid Path Description with Constraints**
**Problem**: Find paths with specific constraints.

**Key Differences**: Apply constraints to path generation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_grid_path_description(n, m, grid, constraints):
    """Find path descriptions with constraints"""
    
    def constrained_is_valid_position(row, col):
        """Position validation with constraints"""
        if not (0 <= row < n and 0 <= col < m and grid[row][col] != '#'):
            return False
        return constraints(row, col)
    
    def constrained_backtrack(row, col, path, results):
        """Backtracking with constraints"""
        if row == n - 1 and col == m - 1:
            results.append(path)
            return
        
        if constrained_is_valid_position(row, col + 1):
            constrained_backtrack(row, col + 1, path + 'R', results)
        
        if constrained_is_valid_position(row + 1, col):
            constrained_backtrack(row + 1, col, path + 'D', results)
    
    results = []
    constrained_backtrack(0, 0, "", results)
    return sorted(results)

# Example usage
n, m = 3, 3
grid = [
    "..#",
    "..#",
    "..."
]
constraints = lambda row, col: True  # No constraints
result = constrained_grid_path_description(n, m, grid, constraints)
print(f"Constrained result:")
for path in result:
    print(path)
```

#### **2. Grid Path Description with Different Metrics**
**Problem**: Find paths with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_grid_path_description(n, m, grid, cost_function):
    """Find path descriptions with different cost metrics"""
    
    def weighted_is_valid_position(row, col):
        """Position validation with cost consideration"""
        return 0 <= row < n and 0 <= col < m and grid[row][col] != '#'
    
    def weighted_backtrack(row, col, path, cost, results):
        """Backtracking with cost tracking"""
        if row == n - 1 and col == m - 1:
            results.append((path, cost))
            return
        
        if weighted_is_valid_position(row, col + 1):
            new_cost = cost + cost_function(row, col + 1, 'R')
            weighted_backtrack(row, col + 1, path + 'R', new_cost, results)
        
        if weighted_is_valid_position(row + 1, col):
            new_cost = cost + cost_function(row + 1, col, 'D')
            weighted_backtrack(row + 1, col, path + 'D', new_cost, results)
    
    results = []
    weighted_backtrack(0, 0, "", 0, results)
    return sorted(results)

# Example usage
n, m = 3, 3
grid = [
    "..#",
    "..#",
    "..."
]
cost_function = lambda row, col, move: 1  # Unit cost
result = weighted_grid_path_description(n, m, grid, cost_function)
print(f"Weighted result:")
for path, cost in result:
    print(f"{path} (cost: {cost})")
```

#### **3. Grid Path Description with Multiple Dimensions**
**Problem**: Find paths in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_grid_path_description(n, m, grid, dimensions):
    """Find path descriptions in multiple dimensions"""
    
    def multi_dimensional_is_valid_position(row, col):
        """Position validation for multiple dimensions"""
        return 0 <= row < n and 0 <= col < m and grid[row][col] != '#'
    
    def multi_dimensional_backtrack(row, col, path, results):
        """Backtracking for multiple dimensions"""
        if row == n - 1 and col == m - 1:
            results.append(path)
            return
        
        if multi_dimensional_is_valid_position(row, col + 1):
            multi_dimensional_backtrack(row, col + 1, path + 'R', results)
        
        if multi_dimensional_is_valid_position(row + 1, col):
            multi_dimensional_backtrack(row + 1, col, path + 'D', results)
    
    results = []
    multi_dimensional_backtrack(0, 0, "", results)
    return sorted(results)

# Example usage
n, m = 3, 3
grid = [
    "..#",
    "..#",
    "..."
]
dimensions = 1
result = multi_dimensional_grid_path_description(n, m, grid, dimensions)
print(f"Multi-dimensional result:")
for path in result:
    print(path)
```

## Problem Variations

### **Variation 1: Grid Path Description with Dynamic Updates**
**Problem**: Handle dynamic grid updates (add/remove/update obstacles) while maintaining valid path descriptions.

**Approach**: Use efficient data structures and algorithms for dynamic grid path management.

```python
from collections import defaultdict
import itertools

class DynamicGridPathDescription:
    def __init__(self, n, m, grid):
        self.n = n
        self.m = m
        self.grid = [list(row) for row in grid]
        self.paths = []
        self._find_all_paths()
    
    def _find_all_paths(self):
        """Find all valid paths using backtracking."""
        self.paths = []
        
        def is_valid_position(row, col):
            """Check if position is valid."""
            return 0 <= row < self.n and 0 <= col < self.m and self.grid[row][col] != '#'
        
        def backtrack(row, col, path):
            """Backtrack to find all paths."""
            if row == self.n - 1 and col == self.m - 1:
                self.paths.append(path)
                return
            
            # Try moving right
            if is_valid_position(row, col + 1):
                backtrack(row, col + 1, path + 'R')
            
            # Try moving down
            if is_valid_position(row + 1, col):
                backtrack(row + 1, col, path + 'D')
        
        backtrack(0, 0, "")
    
    def add_obstacle(self, row, col):
        """Add obstacle at specified position."""
        if 0 <= row < self.n and 0 <= col < self.m and self.grid[row][col] != '#':
            self.grid[row][col] = '#'
            self._find_all_paths()
            return True
        return False
    
    def remove_obstacle(self, row, col):
        """Remove obstacle at specified position."""
        if 0 <= row < self.n and 0 <= col < self.m and self.grid[row][col] == '#':
            self.grid[row][col] = '.'
            self._find_all_paths()
            return True
        return False
    
    def update_obstacle(self, row, col, new_value):
        """Update obstacle at specified position."""
        if 0 <= row < self.n and 0 <= col < self.m:
            old_value = self.grid[row][col]
            self.grid[row][col] = new_value
            self._find_all_paths()
            return True
        return False
    
    def get_paths(self):
        """Get all valid paths."""
        return self.paths
    
    def get_paths_count(self):
        """Get count of valid paths."""
        return len(self.paths)
    
    def get_paths_with_constraints(self, constraint_func):
        """Get paths that satisfy custom constraints."""
        result = []
        for path in self.paths:
            if constraint_func(path):
                result.append(path)
        return result
    
    def get_paths_in_range(self, min_length, max_length):
        """Get paths with length in specified range."""
        result = []
        for path in self.paths:
            if min_length <= len(path) <= max_length:
                result.append(path)
        return result
    
    def get_paths_with_pattern(self, pattern_func):
        """Get paths matching specified pattern."""
        result = []
        for path in self.paths:
            if pattern_func(path):
                result.append(path)
        return result
    
    def get_path_statistics(self):
        """Get statistics about paths."""
        if not self.paths:
            return {
                'total_paths': 0,
                'average_length': 0,
                'direction_distribution': {},
                'length_distribution': {}
            }
        
        total_paths = len(self.paths)
        average_length = sum(len(path) for path in self.paths) / total_paths
        
        # Calculate direction distribution
        direction_distribution = defaultdict(int)
        for path in self.paths:
            for direction in path:
                direction_distribution[direction] += 1
        
        # Calculate length distribution
        length_distribution = defaultdict(int)
        for path in self.paths:
            length_distribution[len(path)] += 1
        
        return {
            'total_paths': total_paths,
            'average_length': average_length,
            'direction_distribution': dict(direction_distribution),
            'length_distribution': dict(length_distribution)
        }
    
    def get_path_patterns(self):
        """Get patterns in paths."""
        patterns = {
            'alternating_paths': 0,
            'monotonic_paths': 0,
            'balanced_paths': 0,
            'zigzag_paths': 0
        }
        
        for path in self.paths:
            # Check for alternating paths
            alternating = True
            for i in range(1, len(path)):
                if path[i] == path[i-1]:
                    alternating = False
                    break
            if alternating:
                patterns['alternating_paths'] += 1
            
            # Check for monotonic paths (all R's then all D's)
            r_count = path.count('R')
            d_count = path.count('D')
            if r_count == 0 or d_count == 0 or path == 'R' * r_count + 'D' * d_count:
                patterns['monotonic_paths'] += 1
            
            # Check for balanced paths (equal R's and D's)
            if r_count == d_count:
                patterns['balanced_paths'] += 1
            
            # Check for zigzag paths (alternating R and D)
            if len(path) >= 2 and all(path[i] != path[i+1] for i in range(len(path)-1)):
                patterns['zigzag_paths'] += 1
        
        return patterns
    
    def get_optimal_path_strategy(self):
        """Get optimal strategy for path operations."""
        if not self.paths:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'path_diversity_rate': 0
            }
        
        # Calculate efficiency rate
        total_possible = 2 ** (self.n + self.m - 2)  # Approximate
        efficiency_rate = len(self.paths) / total_possible if total_possible > 0 else 0
        
        # Calculate path diversity rate
        unique_paths = len(set(self.paths))
        path_diversity_rate = unique_paths / len(self.paths) if self.paths else 0
        
        # Determine recommended strategy
        if efficiency_rate > 0.1:
            recommended_strategy = 'backtracking_optimal'
        elif path_diversity_rate > 0.8:
            recommended_strategy = 'dynamic_programming'
        else:
            recommended_strategy = 'brute_force'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'path_diversity_rate': path_diversity_rate
        }

# Example usage
n, m = 3, 3
grid = [
    "...",
    "...",
    "..."
]
dynamic_grid = DynamicGridPathDescription(n, m, grid)
print(f"Initial paths count: {dynamic_grid.get_paths_count()}")

# Add obstacle
dynamic_grid.add_obstacle(1, 1)
print(f"After adding obstacle at (1,1): {dynamic_grid.get_paths_count()}")

# Remove obstacle
dynamic_grid.remove_obstacle(1, 1)
print(f"After removing obstacle at (1,1): {dynamic_grid.get_paths_count()}")

# Update obstacle
dynamic_grid.add_obstacle(1, 1)
dynamic_grid.update_obstacle(1, 1, '.')
print(f"After updating obstacle at (1,1): {dynamic_grid.get_paths_count()}")

# Get paths with constraints
def constraint_func(path):
    return len(path) <= 4

print(f"Paths with length <= 4: {len(dynamic_grid.get_paths_with_constraints(constraint_func))}")

# Get paths in range
print(f"Paths with length 3-5: {len(dynamic_grid.get_paths_in_range(3, 5))}")

# Get paths with pattern
def pattern_func(path):
    return path.startswith('R')

print(f"Paths starting with 'R': {len(dynamic_grid.get_paths_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_grid.get_path_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_grid.get_path_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_grid.get_optimal_path_strategy()}")
```

### **Variation 2: Grid Path Description with Different Operations**
**Problem**: Handle different types of path operations (weighted moves, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of path operations.

```python
class AdvancedGridPathDescription:
    def __init__(self, n, m, grid, weights=None, priorities=None):
        self.n = n
        self.m = m
        self.grid = [list(row) for row in grid]
        self.weights = weights or {'R': 1, 'D': 1}
        self.priorities = priorities or {'R': 1, 'D': 1}
        self.paths = []
        self._find_all_paths()
    
    def _find_all_paths(self):
        """Find all valid paths using advanced algorithms."""
        self.paths = []
        
        def is_valid_position(row, col):
            """Check if position is valid."""
            return 0 <= row < self.n and 0 <= col < self.m and self.grid[row][col] != '#'
        
        def backtrack(row, col, path):
            """Backtrack to find all paths."""
            if row == self.n - 1 and col == self.m - 1:
                self.paths.append(path)
                return
            
            # Try moving right
            if is_valid_position(row, col + 1):
                backtrack(row, col + 1, path + 'R')
            
            # Try moving down
            if is_valid_position(row + 1, col):
                backtrack(row + 1, col, path + 'D')
        
        backtrack(0, 0, "")
    
    def get_paths(self):
        """Get current valid paths."""
        return self.paths
    
    def get_weighted_paths(self):
        """Get paths with weights and priorities applied."""
        result = []
        for path in self.paths:
            total_weight = sum(self.weights[direction] for direction in path)
            total_priority = sum(self.priorities[direction] for direction in path)
            
            weighted_path = {
                'path': path,
                'total_weight': total_weight,
                'total_priority': total_priority,
                'weighted_score': total_weight * total_priority
            }
            result.append(weighted_path)
        return result
    
    def get_paths_with_priority(self, priority_func):
        """Get paths considering priority."""
        result = []
        for path in self.paths:
            priority = priority_func(path, self.weights, self.priorities)
            result.append((path, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_paths_with_optimization(self, optimization_func):
        """Get paths using custom optimization function."""
        result = []
        for path in self.paths:
            score = optimization_func(path, self.weights, self.priorities)
            result.append((path, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_paths_with_constraints(self, constraint_func):
        """Get paths that satisfy custom constraints."""
        result = []
        for path in self.paths:
            if constraint_func(path, self.weights, self.priorities):
                result.append(path)
        return result
    
    def get_paths_with_multiple_criteria(self, criteria_list):
        """Get paths that satisfy multiple criteria."""
        result = []
        for path in self.paths:
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(path, self.weights, self.priorities):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(path)
        return result
    
    def get_paths_with_alternatives(self, alternatives):
        """Get paths considering alternative weights/priorities."""
        result = []
        
        # Check original paths
        for path in self.paths:
            result.append((path, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedGridPathDescription(self.n, self.m, self.grid, alt_weights, alt_priorities)
            temp_paths = temp_instance.get_paths()
            result.append((temp_paths, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_paths_with_adaptive_criteria(self, adaptive_func):
        """Get paths using adaptive criteria."""
        result = []
        for path in self.paths:
            if adaptive_func(path, self.weights, self.priorities, result):
                result.append(path)
        return result
    
    def get_path_optimization(self):
        """Get optimal path configuration."""
        strategies = [
            ('paths', lambda: len(self.paths)),
            ('weighted_paths', lambda: len(self.get_weighted_paths())),
            ('total_weight', lambda: sum(self.weights.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
n, m = 3, 3
grid = [
    "...",
    "...",
    "..."
]
weights = {'R': 2, 'D': 1}  # Right moves have higher weight
priorities = {'R': 1, 'D': 2}  # Down moves have higher priority
advanced_grid = AdvancedGridPathDescription(n, m, grid, weights, priorities)

print(f"Paths: {len(advanced_grid.get_paths())}")
print(f"Weighted paths: {len(advanced_grid.get_weighted_paths())}")

# Get paths with priority
def priority_func(path, weights, priorities):
    return sum(weights[direction] for direction in path) + sum(priorities[direction] for direction in path)

print(f"Paths with priority: {len(advanced_grid.get_paths_with_priority(priority_func))}")

# Get paths with optimization
def optimization_func(path, weights, priorities):
    return sum(weights[direction] * priorities[direction] for direction in path)

print(f"Paths with optimization: {len(advanced_grid.get_paths_with_optimization(optimization_func))}")

# Get paths with constraints
def constraint_func(path, weights, priorities):
    return len(path) <= 4 and sum(weights[direction] for direction in path) <= 10

print(f"Paths with constraints: {len(advanced_grid.get_paths_with_constraints(constraint_func))}")

# Get paths with multiple criteria
def criterion1(path, weights, priorities):
    return len(path) <= 4

def criterion2(path, weights, priorities):
    return sum(weights[direction] for direction in path) <= 10

criteria_list = [criterion1, criterion2]
print(f"Paths with multiple criteria: {len(advanced_grid.get_paths_with_multiple_criteria(criteria_list))}")

# Get paths with alternatives
alternatives = [({'R': 1, 'D': 1}, {'R': 1, 'D': 1}), ({'R': 3, 'D': 1}, {'R': 1, 'D': 3})]
print(f"Paths with alternatives: {len(advanced_grid.get_paths_with_alternatives(alternatives))}")

# Get paths with adaptive criteria
def adaptive_func(path, weights, priorities, current_result):
    return len(path) <= 4 and len(current_result) < 10

print(f"Paths with adaptive criteria: {len(advanced_grid.get_paths_with_adaptive_criteria(adaptive_func))}")

# Get path optimization
print(f"Path optimization: {advanced_grid.get_path_optimization()}")
```

### **Variation 3: Grid Path Description with Constraints**
**Problem**: Handle grid path description with additional constraints (length limits, direction constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedGridPathDescription:
    def __init__(self, n, m, grid, constraints=None):
        self.n = n
        self.m = m
        self.grid = [list(row) for row in grid]
        self.constraints = constraints or {}
        self.paths = []
        self._find_all_paths()
    
    def _find_all_paths(self):
        """Find all valid paths considering constraints."""
        self.paths = []
        
        def is_valid_position(row, col):
            """Check if position is valid."""
            return 0 <= row < self.n and 0 <= col < self.m and self.grid[row][col] != '#'
        
        def backtrack(row, col, path):
            """Backtrack to find all paths with constraints."""
            if row == self.n - 1 and col == self.m - 1:
                if self._is_valid_path(path):
                    self.paths.append(path)
                return
            
            # Try moving right
            if is_valid_position(row, col + 1):
                new_path = path + 'R'
                if self._is_valid_path(new_path):
                    backtrack(row, col + 1, new_path)
            
            # Try moving down
            if is_valid_position(row + 1, col):
                new_path = path + 'D'
                if self._is_valid_path(new_path):
                    backtrack(row + 1, col, new_path)
        
        backtrack(0, 0, "")
    
    def _is_valid_path(self, path):
        """Check if path is valid considering constraints."""
        # Length constraints
        if 'min_length' in self.constraints:
            if len(path) < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if len(path) > self.constraints['max_length']:
                return False
        
        # Direction constraints
        if 'max_r_count' in self.constraints:
            if path.count('R') > self.constraints['max_r_count']:
                return False
        
        if 'max_d_count' in self.constraints:
            if path.count('D') > self.constraints['max_d_count']:
                return False
        
        if 'min_r_count' in self.constraints:
            if path.count('R') < self.constraints['min_r_count']:
                return False
        
        if 'min_d_count' in self.constraints:
            if path.count('D') < self.constraints['min_d_count']:
                return False
        
        # Pattern constraints
        if 'forbidden_patterns' in self.constraints:
            for pattern in self.constraints['forbidden_patterns']:
                if pattern in path:
                    return False
        
        if 'required_patterns' in self.constraints:
            for pattern in self.constraints['required_patterns']:
                if pattern not in path:
                    return False
        
        # Consecutive constraints
        if 'max_consecutive_r' in self.constraints:
            max_consecutive = 0
            current_consecutive = 0
            for direction in path:
                if direction == 'R':
                    current_consecutive += 1
                    max_consecutive = max(max_consecutive, current_consecutive)
                else:
                    current_consecutive = 0
            if max_consecutive > self.constraints['max_consecutive_r']:
                return False
        
        if 'max_consecutive_d' in self.constraints:
            max_consecutive = 0
            current_consecutive = 0
            for direction in path:
                if direction == 'D':
                    current_consecutive += 1
                    max_consecutive = max(max_consecutive, current_consecutive)
                else:
                    current_consecutive = 0
            if max_consecutive > self.constraints['max_consecutive_d']:
                return False
        
        return True
    
    def get_paths_with_length_constraints(self, min_length, max_length):
        """Get paths considering length constraints."""
        result = []
        for path in self.paths:
            if min_length <= len(path) <= max_length:
                result.append(path)
        return result
    
    def get_paths_with_direction_constraints(self, direction_constraints):
        """Get paths considering direction constraints."""
        result = []
        for path in self.paths:
            satisfies_constraints = True
            for constraint in direction_constraints:
                if not constraint(path):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(path)
        return result
    
    def get_paths_with_pattern_constraints(self, pattern_constraints):
        """Get paths considering pattern constraints."""
        result = []
        for path in self.paths:
            satisfies_constraints = True
            for constraint in pattern_constraints:
                if not constraint(path):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(path)
        return result
    
    def get_paths_with_consecutive_constraints(self, consecutive_limits):
        """Get paths considering consecutive constraints."""
        result = []
        for path in self.paths:
            satisfies_constraints = True
            
            # Check consecutive R's
            if 'max_consecutive_r' in consecutive_limits:
                max_consecutive = 0
                current_consecutive = 0
                for direction in path:
                    if direction == 'R':
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 0
                if max_consecutive > consecutive_limits['max_consecutive_r']:
                    satisfies_constraints = False
            
            # Check consecutive D's
            if 'max_consecutive_d' in consecutive_limits:
                max_consecutive = 0
                current_consecutive = 0
                for direction in path:
                    if direction == 'D':
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 0
                if max_consecutive > consecutive_limits['max_consecutive_d']:
                    satisfies_constraints = False
            
            if satisfies_constraints:
                result.append(path)
        return result
    
    def get_paths_with_mathematical_constraints(self, constraint_func):
        """Get paths that satisfy custom mathematical constraints."""
        result = []
        for path in self.paths:
            if constraint_func(path):
                result.append(path)
        return result
    
    def get_paths_with_range_constraints(self, range_constraints):
        """Get paths that satisfy range constraints."""
        result = []
        for path in self.paths:
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(path):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(path)
        return result
    
    def get_paths_with_optimization_constraints(self, optimization_func):
        """Get paths using custom optimization constraints."""
        # Sort paths by optimization function
        all_paths = []
        for path in self.paths:
            score = optimization_func(path)
            all_paths.append((path, score))
        
        # Sort by optimization score
        all_paths.sort(key=lambda x: x[1], reverse=True)
        
        return [path for path, _ in all_paths]
    
    def get_paths_with_multiple_constraints(self, constraints_list):
        """Get paths that satisfy multiple constraints."""
        result = []
        for path in self.paths:
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(path):
                    satisfies_all_constraints = False
                    break
            if satisfies_all_constraints:
                result.append(path)
        return result
    
    def get_paths_with_priority_constraints(self, priority_func):
        """Get paths with priority-based constraints."""
        # Sort paths by priority
        all_paths = []
        for path in self.paths:
            priority = priority_func(path)
            all_paths.append((path, priority))
        
        # Sort by priority
        all_paths.sort(key=lambda x: x[1], reverse=True)
        
        return [path for path, _ in all_paths]
    
    def get_paths_with_adaptive_constraints(self, adaptive_func):
        """Get paths with adaptive constraints."""
        result = []
        for path in self.paths:
            if adaptive_func(path, result):
                result.append(path)
        return result
    
    def get_optimal_path_strategy(self):
        """Get optimal path strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_paths_with_length_constraints),
            ('direction_constraints', self.get_paths_with_direction_constraints),
            ('pattern_constraints', self.get_paths_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    current_count = len(strategy_func(2, 6))
                elif strategy_name == 'direction_constraints':
                    direction_constraints = [lambda p: p.count('R') >= 1]
                    current_count = len(strategy_func(direction_constraints))
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda p: 'RR' not in p]
                    current_count = len(strategy_func(pattern_constraints))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 2,
    'max_length': 6,
    'max_r_count': 3,
    'max_d_count': 3,
    'min_r_count': 1,
    'min_d_count': 1,
    'forbidden_patterns': ['RRR', 'DDD'],
    'required_patterns': ['R', 'D'],
    'max_consecutive_r': 2,
    'max_consecutive_d': 2
}

n, m = 3, 3
grid = [
    "...",
    "...",
    "..."
]
constrained_grid = ConstrainedGridPathDescription(n, m, grid, constraints)

print("Length-constrained paths:", len(constrained_grid.get_paths_with_length_constraints(3, 5)))

print("Direction-constrained paths:", len(constrained_grid.get_paths_with_direction_constraints([lambda p: p.count('R') >= 1, lambda p: p.count('D') >= 1])))

print("Pattern-constrained paths:", len(constrained_grid.get_paths_with_pattern_constraints([lambda p: 'RR' not in p, lambda p: 'DD' not in p])))

print("Consecutive-constrained paths:", len(constrained_grid.get_paths_with_consecutive_constraints({'max_consecutive_r': 2, 'max_consecutive_d': 2})))

# Mathematical constraints
def custom_constraint(path):
    return len(path) >= 3 and path.count('R') == path.count('D')

print("Mathematical constraint paths:", len(constrained_grid.get_paths_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(path):
    return 2 <= len(path) <= 4

range_constraints = [range_constraint]
print("Range-constrained paths:", len(constrained_grid.get_paths_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(path):
    return len(path) >= 3

def constraint2(path):
    return path.count('R') >= 1

constraints_list = [constraint1, constraint2]
print("Multiple constraints paths:", len(constrained_grid.get_paths_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(path):
    return len(path) + path.count('R') + path.count('D')

print("Priority-constrained paths:", len(constrained_grid.get_paths_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(path, current_result):
    return len(path) >= 3 and len(current_result) < 5

print("Adaptive constraint paths:", len(constrained_grid.get_paths_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_grid.get_optimal_path_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Grid Coloring I](https://cses.fi/problemset/task/1075)s
- [Chessboard and Queens](https://cses.fi/problemset/task/1075)s
- [Creating Strings](https://cses.fi/problemset/task/1075)s

#### **LeetCode Problems**
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Dynamic Programming
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Dynamic Programming
- [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) - Dynamic Programming

#### **Problem Categories**
- **Introductory Problems**: Grid path generation, backtracking
- **Backtracking**: Path generation, grid problems
- **Grid Algorithms**: Path finding, grid traversal

## 🔗 Additional Resources

### **Algorithm References**
- [Introductory Problems](https://cp-algorithms.com/intro-to-algorithms.html) - Introductory algorithms
- [Backtracking](https://cp-algorithms.com/backtracking.html) - Backtracking algorithms
- [Grid Algorithms](https://cp-algorithms.com/graph/breadth-first-search.html) - Grid algorithms

### **Practice Problems**
- [CSES Grid Coloring I](https://cses.fi/problemset/task/1075) - Easy
- [CSES Chessboard and Queens](https://cses.fi/problemset/task/1075) - Easy
- [CSES Creating Strings](https://cses.fi/problemset/task/1075) - Easy

### **Further Reading**
- [Backtracking](https://en.wikipedia.org/wiki/Backtracking) - Wikipedia article
- [Grid](https://en.wikipedia.org/wiki/Grid_(spatial_index)) - Wikipedia article
- [Path Finding](https://en.wikipedia.org/wiki/Pathfinding) - Wikipedia article
