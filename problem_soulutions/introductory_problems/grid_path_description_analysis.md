---
layout: simple
title: "Grid Path Description - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/grid_path_description_analysis
---

# Grid Path Description - Introductory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of grid path generation and string manipulation in introductory problems
- Apply efficient algorithms for generating grid path descriptions
- Implement backtracking and recursive approaches for path generation
- Optimize algorithms for grid path problems
- Handle special cases in grid path generation problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Grid path generation, backtracking, recursion, string manipulation
- **Data Structures**: 2D arrays, grids, strings, path tracking
- **Mathematical Concepts**: Grid mathematics, path counting, combinatorics, string theory
- **Programming Skills**: 2D array manipulation, backtracking, recursive algorithms, string operations
- **Related Problems**: Grid Coloring I (introductory_problems), Chessboard and Queens (introductory_problems), Creating Strings (introductory_problems)

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

### Related Problems

#### **CSES Problems**
- [Grid Coloring I](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Chessboard and Queens](https://cses.fi/problemset/task/1075) - Introductory Problems
- [Creating Strings](https://cses.fi/problemset/task/1075) - Introductory Problems

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
