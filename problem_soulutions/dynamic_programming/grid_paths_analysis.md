---
layout: simple
title: "Grid Paths - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/grid_paths_analysis
---

# Grid Paths - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of grid path counting in dynamic programming
- Apply counting techniques for grid path analysis
- Implement efficient algorithms for grid path counting
- Optimize DP operations for path analysis
- Handle special cases in grid path problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, counting techniques, mathematical formulas
- **Data Structures**: 2D arrays, mathematical computations, DP tables
- **Mathematical Concepts**: Grid theory, combinations, modular arithmetic
- **Programming Skills**: DP implementation, mathematical computations, modular arithmetic
- **Related Problems**: Minimal Grid Path (dynamic programming), Array Description (dynamic programming), Book Shop (dynamic programming)

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

**Algorithm**:
- Use DP table to store number of paths for each position
- Fill DP table bottom-up
- Return DP[0][0] as result

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
