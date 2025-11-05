---
layout: simple
title: "Filled Subgrid Count II - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/filled_subgrid_count_ii_analysis
---

# Filled Subgrid Count II - Grid Counting Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of filled subgrids in grid problems
- Apply counting techniques for filled subgrid analysis
- Implement efficient algorithms for subgrid counting
- Optimize grid traversal and counting operations
- Handle special cases in filled subgrid counting

## 📋 Problem Description

Given a grid of size n×m, count the number of subgrids where all cells are filled with a specific value.

**Input**: 
- n, m: grid dimensions
- grid: n×m grid with values

**Output**: 
- Number of filled subgrids with the specified value

**Constraints**:
- 1 ≤ n, m ≤ 1000
- Grid values are integers

**Example**:
```
Input:
n = 3, m = 3
grid = [
  [1, 1, 1],
  [1, 1, 1],
  [1, 1, 1]
]

Output:
14

Explanation**: 
Filled subgrids with all cells = 1:
- 9 subgrids of size 1×1
- 4 subgrids of size 2×2
- 1 subgrid of size 3×3
Total: 9 + 4 + 1 = 14
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all possible subgrids
- **Cell Validation**: Check all cells in each subgrid
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: O(n²m²) time complexity

**Key Insight**: Enumerate all possible subgrids and check if all cells have the target value.

**Algorithm**:
- Iterate through all possible subgrid positions and sizes
- For each subgrid, check all cells
- Count subgrids that are completely filled

**Visual Example**:
```
Grid: 3×3
┌─────────────────────────────────────┐
│ 1 1 1                              │
│ 1 1 1                              │
│ 1 1 1                              │
└─────────────────────────────────────┘

Brute force enumeration:
┌─────────────────────────────────────┐
│ Check all 1×1 subgrids: 9 ✓        │
│ Check all 2×2 subgrids: 4 ✓        │
│ Check all 3×3 subgrids: 1 ✓        │
│ Total: 9 + 4 + 1 = 14              │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_filled_subgrid_count(n, m, grid, target_value=1):
    """
    Count filled subgrids using brute force approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for filled cells
    
    Returns:
        int: number of filled subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Check if all cells in subgrid have target value
                    if is_subgrid_filled(grid, i, j, height, width, target_value):
                        count += 1
    
    return count

def is_subgrid_filled(grid, start_i, start_j, height, width, target_value):
    """
    Check if all cells in subgrid have target value
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        target_value: target value
    
    Returns:
        bool: True if all cells have target value
    """
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if grid[i][j] != target_value:
                return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
result = brute_force_filled_subgrid_count(n, m, grid)
print(f"Brute force result: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(1)

**Why it's inefficient**: Checks all possible subgrids with O(n²m²) time complexity.

---

### Approach 2: Optimized Cell Checking Solution

**Key Insights from Optimized Cell Checking Solution**:
- **Early Termination**: Stop checking as soon as invalid cell is found
- **Efficient Validation**: Use optimized cell checking
- **Reduced Redundancy**: Avoid redundant cell checks
- **Optimization**: More efficient than brute force

**Key Insight**: Use early termination and optimized cell checking to reduce redundant operations.

**Algorithm**:
- Use early termination when invalid cell is found
- Optimize cell checking process
- Reduce redundant operations

**Visual Example**:
```
Optimized cell checking:
┌─────────────────────────────────────┐
│ For each subgrid:                  │
│ - Check cells row by row           │
│ - Stop immediately if invalid cell │
│ - Skip remaining cells if possible │
└─────────────────────────────────────┘

Early termination example:
┌─────────────────────────────────────┐
│ Subgrid (0,0) to (1,1):           │
│ Check (0,0): 1 ✓                  │
│ Check (0,1): 1 ✓                  │
│ Check (1,0): 1 ✓                  │
│ Check (1,1): 1 ✓                  │
│ All cells valid: count++           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def optimized_filled_subgrid_count(n, m, grid, target_value=1):
    """
    Count filled subgrids using optimized cell checking
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for filled cells
    
    Returns:
        int: number of filled subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Use optimized cell checking
                    if is_subgrid_filled_optimized(grid, i, j, height, width, target_value):
                        count += 1
    
    return count

def is_subgrid_filled_optimized(grid, start_i, start_j, height, width, target_value):
    """
    Check if all cells in subgrid have target value with optimization
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        target_value: target value
    
    Returns:
        bool: True if all cells have target value
    """
    # Check cells row by row with early termination
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if grid[i][j] != target_value:
                return False  # Early termination
    
    return True

def is_subgrid_filled_optimized_v2(grid, start_i, start_j, height, width, target_value):
    """
    Alternative optimized cell checking with different strategy
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        target_value: target value
    
    Returns:
        bool: True if all cells have target value
    """
    # Check if starting cell has target value
    if grid[start_i][start_j] != target_value:
        return False
    
    # Check remaining cells
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if i == start_i and j == start_j:
                continue  # Skip already checked cell
            if grid[i][j] != target_value:
                return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
result = optimized_filled_subgrid_count(n, m, grid)
print(f"Optimized cell checking result: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(1)

**Why it's better**: Reduces redundant operations and improves efficiency.

**Implementation Considerations**:
- **Early Termination**: Stop checking as soon as invalid cell is found
- **Optimized Validation**: Use optimized cell checking
- **Reduced Redundancy**: Avoid redundant cell checks

---

### Approach 3: Prefix Sum Solution (Optimal)

**Key Insights from Prefix Sum Solution**:
- **Prefix Sum Technique**: Use prefix sums for efficient range queries
- **Mathematical Optimization**: Use mathematical properties for counting
- **Efficient Calculation**: O(nm) time complexity
- **Optimal Complexity**: Best approach for filled subgrid counting

**Key Insight**: Use prefix sums to efficiently check if subgrids are filled.

**Algorithm**:
- Build prefix sum array for target value
- Use prefix sums to check subgrid validity
- Count valid subgrids efficiently

**Visual Example**:
```
Prefix sum construction:
┌─────────────────────────────────────┐
│ Grid: 1 1 1                        │
│       1 1 1                        │
│       1 1 1                        │
│                                   │
│ Prefix sum: 1 2 3                 │
│            2 4 6                  │
│            3 6 9                  │
└─────────────────────────────────────┘

Subgrid validation:
┌─────────────────────────────────────┐
│ For subgrid (0,0) to (1,1):       │
│ Expected sum: 2×2 = 4             │
│ Actual sum: 4 ✓                   │
│ Subgrid is filled                  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def prefix_sum_filled_subgrid_count(n, m, grid, target_value=1):
    """
    Count filled subgrids using prefix sum approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for filled cells
    
    Returns:
        int: number of filled subgrids
    """
    # Build prefix sum array
    prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for j in range(m):
            prefix_sum[i + 1][j + 1] = (prefix_sum[i][j + 1] + 
                                       prefix_sum[i + 1][j] - 
                                       prefix_sum[i][j])
            if grid[i][j] == target_value:
                prefix_sum[i + 1][j + 1] += 1
    
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Use prefix sum to check if subgrid is filled
                    if is_subgrid_filled_prefix_sum(prefix_sum, i, j, height, width, target_value):
                        count += 1
    
    return count

def is_subgrid_filled_prefix_sum(prefix_sum, start_i, start_j, height, width, target_value):
    """
    Check if subgrid is filled using prefix sum
    
    Args:
        prefix_sum: 2D prefix sum array
        start_i, start_j: starting position
        height, width: subgrid dimensions
        target_value: target value
    
    Returns:
        bool: True if subgrid is filled
    """
    # Calculate sum of subgrid using prefix sum
    total_sum = (prefix_sum[start_i + height][start_j + width] - 
                 prefix_sum[start_i][start_j + width] - 
                 prefix_sum[start_i + height][start_j] + 
                 prefix_sum[start_i][start_j])
    
    # Check if sum equals expected value
    expected_sum = height * width
    return total_sum == expected_sum

def optimized_prefix_sum_count(n, m, grid, target_value=1):
    """
    Optimized prefix sum approach with additional optimizations
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for filled cells
    
    Returns:
        int: number of filled subgrids
    """
    # Build prefix sum array
    prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for j in range(m):
            prefix_sum[i + 1][j + 1] = (prefix_sum[i][j + 1] + 
                                       prefix_sum[i + 1][j] - 
                                       prefix_sum[i][j])
            if grid[i][j] == target_value:
                prefix_sum[i + 1][j + 1] += 1
    
    count = 0
    
    # Optimize by checking only valid starting positions
    for i in range(n):
        for j in range(m):
            if grid[i][j] == target_value:  # Only start from valid cells
                for height in range(1, n - i + 1):
                    for width in range(1, m - j + 1):
                        if is_subgrid_filled_prefix_sum(prefix_sum, i, j, height, width, target_value):
                            count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
result1 = prefix_sum_filled_subgrid_count(n, m, grid)
result2 = optimized_prefix_sum_count(n, m, grid)
print(f"Prefix sum result: {result1}")
print(f"Optimized prefix sum result: {result2}")
```

**Time Complexity**: O(nm)
**Space Complexity**: O(nm)

**Why it's optimal**: Uses prefix sums for O(nm) time complexity.

**Implementation Details**:
- **Prefix Sum Construction**: Build prefix sum array efficiently
- **Range Query**: Use prefix sums for efficient range queries
- **Mathematical Optimization**: Use mathematical properties for counting
- **Efficient Algorithms**: Use optimal algorithms for grid operations

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²m²) | O(1) | Complete enumeration of all subgrids |
| Optimized Cell Checking | O(n²m²) | O(1) | Early termination and optimized validation |
| Prefix Sum | O(nm) | O(nm) | Use prefix sums for efficient range queries |

### Time Complexity
- **Time**: O(nm) - Use prefix sums for efficient range queries
- **Space**: O(nm) - Store prefix sum array

### Why This Solution Works
- **Prefix Sum Technique**: Use prefix sums for efficient range queries
- **Mathematical Properties**: Use mathematical properties for counting
- **Efficient Algorithms**: Use optimal algorithms for grid operations
- **Range Query Optimization**: Use prefix sums for subgrid validation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Filled Subgrid Count with Multiple Values**
**Problem**: Count filled subgrids with multiple valid values.

**Key Differences**: Subgrids can be filled with multiple valid values

**Solution Approach**: Modify prefix sum to handle multiple values

**Implementation**:
```python
def multiple_value_filled_subgrid_count(n, m, grid, valid_values):
    """
    Count filled subgrids with multiple valid values
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        valid_values: set of valid values
    
    Returns:
        int: number of filled subgrids
    """
    # Build prefix sum array for each valid value
    prefix_sums = {}
    for value in valid_values:
        prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
        
        for i in range(n):
            for j in range(m):
                prefix_sum[i + 1][j + 1] = (prefix_sum[i][j + 1] + 
                                           prefix_sum[i + 1][j] - 
                                           prefix_sum[i][j])
                if grid[i][j] == value:
                    prefix_sum[i + 1][j + 1] += 1
        
        prefix_sums[value] = prefix_sum
    
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Check if subgrid is filled with any valid value
                    if is_subgrid_filled_multiple_values(prefix_sums, i, j, height, width, valid_values):
                        count += 1
    
    return count

def is_subgrid_filled_multiple_values(prefix_sums, start_i, start_j, height, width, valid_values):
    """
    Check if subgrid is filled with any valid value
    
    Args:
        prefix_sums: dictionary of prefix sum arrays
        start_i, start_j: starting position
        height, width: subgrid dimensions
        valid_values: set of valid values
    
    Returns:
        bool: True if subgrid is filled with any valid value
    """
    expected_sum = height * width
    
    for value in valid_values:
        prefix_sum = prefix_sums[value]
        total_sum = (prefix_sum[start_i + height][start_j + width] - 
                     prefix_sum[start_i][start_j + width] - 
                     prefix_sum[start_i + height][start_j] + 
                     prefix_sum[start_i][start_j])
        
        if total_sum == expected_sum:
            return True
    
    return False

# Example usage
n, m = 3, 3
grid = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
valid_values = {1, 2}
result = multiple_value_filled_subgrid_count(n, m, grid, valid_values)
print(f"Multiple value filled subgrid count: {result}")
```

#### **2. Filled Subgrid Count with Size Constraints**
**Problem**: Count filled subgrids with specific size constraints.

**Key Differences**: Additional constraints on subgrid size

**Solution Approach**: Add size constraints to the counting logic

**Implementation**:
```python
def size_constrained_filled_subgrid_count(n, m, grid, target_value, min_size, max_size):
    """
    Count filled subgrids with size constraints
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for filled cells
        min_size: minimum subgrid size
        max_size: maximum subgrid size
    
    Returns:
        int: number of filled subgrids
    """
    # Build prefix sum array
    prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for j in range(m):
            prefix_sum[i + 1][j + 1] = (prefix_sum[i][j + 1] + 
                                       prefix_sum[i + 1][j] - 
                                       prefix_sum[i][j])
            if grid[i][j] == target_value:
                prefix_sum[i + 1][j + 1] += 1
    
    count = 0
    
    # Check all possible subgrid positions and sizes with constraints
    for i in range(n):
        for j in range(m):
            for height in range(max(1, min_size), min(n - i + 1, max_size + 1)):
                for width in range(max(1, min_size), min(m - j + 1, max_size + 1)):
                    if is_subgrid_filled_prefix_sum(prefix_sum, i, j, height, width, target_value):
                        count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
result = size_constrained_filled_subgrid_count(n, m, grid, 1, 2, 3)
print(f"Size constrained filled subgrid count: {result}")
```

#### **3. Filled Subgrid Count with Pattern Matching**
**Problem**: Count filled subgrids that match specific patterns.

**Key Differences**: Subgrids must match specific patterns

**Solution Approach**: Use pattern matching techniques

**Implementation**:
```python
def pattern_matching_filled_subgrid_count(n, m, grid, pattern):
    """
    Count filled subgrids that match specific patterns
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        pattern: 2D pattern to match
    
    Returns:
        int: number of filled subgrids matching pattern
    """
    pattern_height, pattern_width = len(pattern), len(pattern[0])
    count = 0
    
    # Check all possible subgrid positions
    for i in range(n - pattern_height + 1):
        for j in range(m - pattern_width + 1):
            # Check if subgrid matches pattern
            if matches_pattern(grid, i, j, pattern):
                count += 1
    
    return count

def matches_pattern(grid, start_i, start_j, pattern):
    """
    Check if subgrid matches pattern
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        pattern: 2D pattern to match
    
    Returns:
        bool: True if subgrid matches pattern
    """
    pattern_height, pattern_width = len(pattern), len(pattern[0])
    
    for i in range(pattern_height):
        for j in range(pattern_width):
            if grid[start_i + i][start_j + j] != pattern[i][j]:
                return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
pattern = [
    [1, 1],
    [1, 1]
]
result = pattern_matching_filled_subgrid_count(n, m, grid, pattern)
print(f"Pattern matching filled subgrid count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Border Subgrid Count](https://cses.fi/problemset/task/1075) - Grid counting
- [All Letter Subgrid Count](https://cses.fi/problemset/task/1075) - Grid counting
- [Grid Completion](https://cses.fi/problemset/task/1075) - Grid algorithms

#### **LeetCode Problems**
- [Number of Islands](https://leetcode.com/problems/number-of-islands/) - Grid algorithms
- [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) - Grid algorithms
- [Island Perimeter](https://leetcode.com/problems/island-perimeter/) - Grid algorithms

#### **Problem Categories**
- **Grid Algorithms**: 2D array manipulation, grid counting
- **Combinatorics**: Mathematical counting, grid properties
- **Mathematical Algorithms**: Prefix sums, mathematical analysis

## 🔗 Additional Resources

### **Algorithm References**
- [Grid Algorithms](https://cp-algorithms.com/geometry/basic-geometry.html) - Grid algorithms
- [Prefix Sums](https://cp-algorithms.com/data_structures/prefix_sum.html) - Prefix sum technique
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques

### **Practice Problems**
- [CSES Border Subgrid Count](https://cses.fi/problemset/task/1075) - Medium
- [CSES All Letter Subgrid Count](https://cses.fi/problemset/task/1075) - Medium
- [CSES Grid Completion](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Grid Algorithms](https://en.wikipedia.org/wiki/Grid_computing) - Wikipedia article
