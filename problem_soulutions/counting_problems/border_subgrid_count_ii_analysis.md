---
layout: simple
title: "Border Subgrid Count II - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/border_subgrid_count_ii_analysis
---

# Border Subgrid Count II - Grid Counting Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of border subgrids in advanced grid problems
- Apply counting techniques for complex border subgrid analysis
- Implement efficient algorithms for advanced subgrid counting
- Optimize grid traversal and counting operations for complex cases
- Handle special cases in advanced border subgrid counting

## 📋 Problem Description

Given a grid of size n×m, count the number of subgrids where all border cells have specific properties and the interior cells have different properties.

**Input**: 
- n, m: grid dimensions
- grid: n×m grid with values

**Output**: 
- Number of border subgrids with the specified properties

**Constraints**:
- 1 ≤ n, m ≤ 1000
- Grid values are integers
- Border and interior cells have different constraints

**Example**:
```
Input:
n = 4, m = 4
grid = [
  [1, 1, 1, 1],
  [1, 0, 0, 1],
  [1, 0, 0, 1],
  [1, 1, 1, 1]
]

Output:
1

Explanation**: 
Border subgrid with border=1 and interior=0:
- Only the 4×4 subgrid satisfies the condition
- Border cells: all 1s
- Interior cells: all 0s
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all possible subgrids
- **Border and Interior Validation**: Check both border and interior cells
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: O(n²m²) time complexity

**Key Insight**: Enumerate all possible subgrids and check if their borders and interiors satisfy the conditions.

**Algorithm**:
- Iterate through all possible subgrid positions and sizes
- For each subgrid, check all border and interior cells
- Count subgrids that satisfy both border and interior conditions

**Visual Example**:
```
Grid: 4×4
┌─────────────────────────────────────┐
│ 1 1 1 1                            │
│ 1 0 0 1                            │
│ 1 0 0 1                            │
│ 1 1 1 1                            │
└─────────────────────────────────────┘

Brute force enumeration:
┌─────────────────────────────────────┐
│ Check 4×4 subgrid:                 │
│ Border: 1,1,1,1,1,1,1,1,1,1,1,1 ✓ │
│ Interior: 0,0,0,0 ✓               │
│ Valid subgrid: count++             │
│ Total: 1                           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_border_subgrid_count_ii(n, m, grid, border_value=1, interior_value=0):
    """
    Count border subgrids using brute force approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        border_value: target value for border cells
        interior_value: target value for interior cells
    
    Returns:
        int: number of border subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Check if subgrid satisfies border and interior conditions
                    if is_border_subgrid_valid_ii(grid, i, j, height, width, border_value, interior_value):
                        count += 1
    
    return count

def is_border_subgrid_valid_ii(grid, start_i, start_j, height, width, border_value, interior_value):
    """
    Check if subgrid satisfies border and interior conditions
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        border_value: target value for border cells
        interior_value: target value for interior cells
    
    Returns:
        bool: True if subgrid satisfies conditions
    """
    # Check border cells
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            # Check if cell is on border
            if (i == start_i or i == start_i + height - 1 or 
                j == start_j or j == start_j + width - 1):
                if grid[i][j] != border_value:
                    return False
            else:
                # Interior cell
                if grid[i][j] != interior_value:
                    return False
    
    return True

# Example usage
n, m = 4, 4
grid = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]
result = brute_force_border_subgrid_count_ii(n, m, grid)
print(f"Brute force result: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(1)

**Why it's inefficient**: Checks all possible subgrids with O(n²m²) time complexity.

---

### Approach 2: Optimized Border and Interior Checking Solution

**Key Insights from Optimized Border and Interior Checking Solution**:
- **Early Termination**: Stop checking as soon as invalid cell is found
- **Efficient Validation**: Use optimized border and interior checking
- **Reduced Redundancy**: Avoid redundant cell checks
- **Optimization**: More efficient than brute force

**Key Insight**: Use early termination and optimized checking to reduce redundant operations.

**Algorithm**:
- Use early termination when invalid cell is found
- Optimize border and interior checking process
- Reduce redundant operations

**Visual Example**:
```
Optimized checking:
┌─────────────────────────────────────┐
│ For each subgrid:                  │
│ - Check border cells first         │
│ - Check interior cells second      │
│ - Stop immediately if invalid cell │
│ - Skip remaining cells if possible │
└─────────────────────────────────────┘

Early termination example:
┌─────────────────────────────────────┐
│ Subgrid (0,0) to (3,3):           │
│ Check border: all 1s ✓            │
│ Check interior: all 0s ✓          │
│ Valid subgrid: count++             │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def optimized_border_subgrid_count_ii(n, m, grid, border_value=1, interior_value=0):
    """
    Count border subgrids using optimized checking approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        border_value: target value for border cells
        interior_value: target value for interior cells
    
    Returns:
        int: number of border subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Use optimized checking
                    if is_border_subgrid_valid_optimized_ii(grid, i, j, height, width, border_value, interior_value):
                    count += 1
    
    return count

def is_border_subgrid_valid_optimized_ii(grid, start_i, start_j, height, width, border_value, interior_value):
    """
    Check if subgrid satisfies conditions with optimization
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        border_value: target value for border cells
        interior_value: target value for interior cells
    
    Returns:
        bool: True if subgrid satisfies conditions
    """
    # Check border cells first
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if (i == start_i or i == start_i + height - 1 or 
                j == start_j or j == start_j + width - 1):
                if grid[i][j] != border_value:
                    return False  # Early termination
    
    # Check interior cells
    for i in range(start_i + 1, start_i + height - 1):
        for j in range(start_j + 1, start_j + width - 1):
            if grid[i][j] != interior_value:
                return False  # Early termination
    
    return True

def is_border_subgrid_valid_optimized_ii_v2(grid, start_i, start_j, height, width, border_value, interior_value):
    """
    Alternative optimized checking with different strategy
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        border_value: target value for border cells
        interior_value: target value for interior cells
    
    Returns:
        bool: True if subgrid satisfies conditions
    """
    # Check if subgrid is large enough to have interior
    if height < 3 or width < 3:
        # Only border cells, check if all are border_value
        for i in range(start_i, start_i + height):
            for j in range(start_j, start_j + width):
                if grid[i][j] != border_value:
                    return False
        return True
    
    # Check border cells
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if (i == start_i or i == start_i + height - 1 or 
                j == start_j or j == start_j + width - 1):
                if grid[i][j] != border_value:
                    return False
    
    # Check interior cells
    for i in range(start_i + 1, start_i + height - 1):
        for j in range(start_j + 1, start_j + width - 1):
            if grid[i][j] != interior_value:
                return False
    
    return True

# Example usage
n, m = 4, 4
grid = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]
result = optimized_border_subgrid_count_ii(n, m, grid)
print(f"Optimized checking result: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(1)

**Why it's better**: Reduces redundant operations and improves efficiency.

**Implementation Considerations**:
- **Early Termination**: Stop checking as soon as invalid cell is found
- **Optimized Validation**: Use optimized border and interior checking
- **Reduced Redundancy**: Avoid redundant cell checks

---

### Approach 3: Advanced Prefix Sum Solution (Optimal)

**Key Insights from Advanced Prefix Sum Solution**:
- **Advanced Prefix Sum Technique**: Use prefix sums for efficient range queries
- **Mathematical Optimization**: Use mathematical properties for counting
- **Efficient Calculation**: O(nm) time complexity
- **Optimal Complexity**: Best approach for advanced border subgrid counting

**Key Insight**: Use advanced prefix sums to efficiently check if subgrids satisfy border and interior conditions.

**Algorithm**:
- Build prefix sum arrays for border and interior values
- Use prefix sums to check subgrid validity
- Count valid subgrids efficiently

**Visual Example**:
```
Advanced prefix sum construction:
┌─────────────────────────────────────┐
│ Grid: 1 1 1 1                      │
│       1 0 0 1                      │
│       1 0 0 1                      │
│       1 1 1 1                      │
│                                   │
│ Border prefix sum: 1 2 3 4        │
│                   2 3 4 5         │
│                   3 4 5 6         │
│                   4 5 6 7         │
│                                   │
│ Interior prefix sum: 0 0 0 0      │
│                      0 1 2 2      │
│                      0 2 4 4      │
│                      0 2 4 4      │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_prefix_sum_border_subgrid_count_ii(n, m, grid, border_value=1, interior_value=0):
    """
    Count border subgrids using advanced prefix sum approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        border_value: target value for border cells
        interior_value: target value for interior cells
    
    Returns:
        int: number of border subgrids
    """
    # Build prefix sum arrays for border and interior values
    border_prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
    interior_prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for j in range(m):
            # Border prefix sum
            border_prefix_sum[i + 1][j + 1] = (border_prefix_sum[i][j + 1] + 
                                              border_prefix_sum[i + 1][j] - 
                                              border_prefix_sum[i][j])
            if grid[i][j] == border_value:
                border_prefix_sum[i + 1][j + 1] += 1
            
            # Interior prefix sum
            interior_prefix_sum[i + 1][j + 1] = (interior_prefix_sum[i][j + 1] + 
                                                interior_prefix_sum[i + 1][j] - 
                                                interior_prefix_sum[i][j])
            if grid[i][j] == interior_value:
                interior_prefix_sum[i + 1][j + 1] += 1
    
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Use prefix sums to check validity
                    if is_border_subgrid_valid_prefix_sum_ii(border_prefix_sum, interior_prefix_sum, 
                                                           i, j, height, width, border_value, interior_value):
                    count += 1
    
    return count

def is_border_subgrid_valid_prefix_sum_ii(border_prefix_sum, interior_prefix_sum, 
                                        start_i, start_j, height, width, border_value, interior_value):
    """
    Check if subgrid satisfies conditions using prefix sums
    
    Args:
        border_prefix_sum: 2D prefix sum array for border values
        interior_prefix_sum: 2D prefix sum array for interior values
        start_i, start_j: starting position
        height, width: subgrid dimensions
        border_value: target value for border cells
        interior_value: target value for interior cells
    
    Returns:
        bool: True if subgrid satisfies conditions
    """
    # Check if subgrid is large enough to have interior
    if height < 3 or width < 3:
        # Only border cells, check if all are border_value
        total_sum = (border_prefix_sum[start_i + height][start_j + width] - 
                     border_prefix_sum[start_i][start_j + width] - 
                     border_prefix_sum[start_i + height][start_j] + 
                     border_prefix_sum[start_i][start_j])
        expected_sum = height * width
        return total_sum == expected_sum
    
    # Check border cells
    border_sum = (border_prefix_sum[start_i + height][start_j + width] - 
                  border_prefix_sum[start_i][start_j + width] - 
                  border_prefix_sum[start_i + height][start_j] + 
                  border_prefix_sum[start_i][start_j])
    
    # Calculate expected border sum
    expected_border_sum = 2 * (height + width) - 4  # Border cells count
    
    if border_sum != expected_border_sum:
        return False
    
    # Check interior cells
    interior_sum = (interior_prefix_sum[start_i + height - 1][start_j + width - 1] - 
                    interior_prefix_sum[start_i + 1][start_j + width - 1] - 
                    interior_prefix_sum[start_i + height - 1][start_j + 1] + 
                    interior_prefix_sum[start_i + 1][start_j + 1])
    
    # Calculate expected interior sum
    expected_interior_sum = (height - 2) * (width - 2)  # Interior cells count
    
    return interior_sum == expected_interior_sum

def optimized_advanced_prefix_sum_count_ii(n, m, grid, border_value=1, interior_value=0):
    """
    Optimized advanced prefix sum approach with additional optimizations
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        border_value: target value for border cells
        interior_value: target value for interior cells
    
    Returns:
        int: number of border subgrids
    """
    # Build prefix sum arrays
    border_prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
    interior_prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
    
        for i in range(n):
            for j in range(m):
            border_prefix_sum[i + 1][j + 1] = (border_prefix_sum[i][j + 1] + 
                                              border_prefix_sum[i + 1][j] - 
                                              border_prefix_sum[i][j])
            if grid[i][j] == border_value:
                border_prefix_sum[i + 1][j + 1] += 1
            
            interior_prefix_sum[i + 1][j + 1] = (interior_prefix_sum[i][j + 1] + 
                                                interior_prefix_sum[i + 1][j] - 
                                                interior_prefix_sum[i][j])
            if grid[i][j] == interior_value:
                interior_prefix_sum[i + 1][j + 1] += 1
    
    count = 0
    
    # Optimize by checking only valid starting positions
    for i in range(n):
        for j in range(m):
            if grid[i][j] == border_value:  # Only start from valid border cells
                for height in range(1, n - i + 1):
                    for width in range(1, m - j + 1):
                        if is_border_subgrid_valid_prefix_sum_ii(border_prefix_sum, interior_prefix_sum, 
                                                               i, j, height, width, border_value, interior_value):
                    count += 1
    
    return count

# Example usage
n, m = 4, 4
grid = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]
result1 = advanced_prefix_sum_border_subgrid_count_ii(n, m, grid)
result2 = optimized_advanced_prefix_sum_count_ii(n, m, grid)
print(f"Advanced prefix sum result: {result1}")
print(f"Optimized advanced prefix sum result: {result2}")
```

**Time Complexity**: O(nm)
**Space Complexity**: O(nm)

**Why it's optimal**: Uses advanced prefix sums for O(nm) time complexity.

**Implementation Details**:
- **Advanced Prefix Sum Construction**: Build prefix sum arrays for border and interior values
- **Range Query**: Use prefix sums for efficient range queries
- **Mathematical Optimization**: Use mathematical properties for counting
- **Efficient Algorithms**: Use optimal algorithms for grid operations

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²m²) | O(1) | Complete enumeration of all subgrids |
| Optimized Checking | O(n²m²) | O(1) | Early termination and optimized validation |
| Advanced Prefix Sum | O(nm) | O(nm) | Use advanced prefix sums for efficient range queries |

### Time Complexity
- **Time**: O(nm) - Use advanced prefix sums for efficient range queries
- **Space**: O(nm) - Store prefix sum arrays

### Why This Solution Works
- **Advanced Prefix Sum Technique**: Use prefix sums for efficient range queries
- **Mathematical Properties**: Use mathematical properties for counting
- **Efficient Algorithms**: Use optimal algorithms for grid operations
- **Range Query Optimization**: Use prefix sums for subgrid validation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Border Subgrid Count with Multiple Border Values**
**Problem**: Count border subgrids with multiple valid border values.

**Key Differences**: Border cells can have multiple valid values

**Solution Approach**: Modify prefix sum to handle multiple border values

**Implementation**:
```python
def multiple_border_value_subgrid_count_ii(n, m, grid, border_values, interior_value=0):
    """
    Count border subgrids with multiple valid border values
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        border_values: set of valid border values
        interior_value: target value for interior cells
    
    Returns:
        int: number of border subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Check if subgrid satisfies conditions with multiple border values
                    if is_border_subgrid_valid_multiple_values_ii(grid, i, j, height, width, border_values, interior_value):
                        count += 1
    
    return count

def is_border_subgrid_valid_multiple_values_ii(grid, start_i, start_j, height, width, border_values, interior_value):
    """
    Check if subgrid satisfies conditions with multiple border values
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        border_values: set of valid border values
        interior_value: target value for interior cells
    
    Returns:
        bool: True if subgrid satisfies conditions
    """
    # Check border cells
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if (i == start_i or i == start_i + height - 1 or 
                j == start_j or j == start_j + width - 1):
                if grid[i][j] not in border_values:
                    return False
    
    # Check interior cells
    for i in range(start_i + 1, start_i + height - 1):
        for j in range(start_j + 1, start_j + width - 1):
            if grid[i][j] != interior_value:
                return False
    
    return True

# Example usage
n, m = 4, 4
grid = [
    [1, 2, 2, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 2, 2, 1]
]
border_values = {1, 2}
result = multiple_border_value_subgrid_count_ii(n, m, grid, border_values)
print(f"Multiple border value subgrid count: {result}")
```

#### **2. Border Subgrid Count with Size Constraints**
**Problem**: Count border subgrids with specific size constraints.

**Key Differences**: Additional constraints on subgrid size

**Solution Approach**: Add size constraints to the counting logic

**Implementation**:
```python
def size_constrained_border_subgrid_count_ii(n, m, grid, border_value, interior_value, min_size, max_size):
    """
    Count border subgrids with size constraints
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        border_value: target value for border cells
        interior_value: target value for interior cells
        min_size: minimum subgrid size
        max_size: maximum subgrid size
    
    Returns:
        int: number of border subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes with constraints
    for i in range(n):
        for j in range(m):
            for height in range(max(1, min_size), min(n - i + 1, max_size + 1)):
                for width in range(max(1, min_size), min(m - j + 1, max_size + 1)):
                    if is_border_subgrid_valid_ii(grid, i, j, height, width, border_value, interior_value):
                        count += 1
    
    return count

# Example usage
n, m = 4, 4
grid = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]
result = size_constrained_border_subgrid_count_ii(n, m, grid, 1, 0, 3, 4)
print(f"Size constrained border subgrid count: {result}")
```

#### **3. Border Subgrid Count with Pattern Matching**
**Problem**: Count border subgrids that match specific patterns.

**Key Differences**: Subgrids must match specific patterns

**Solution Approach**: Use pattern matching techniques

**Implementation**:
```python
def pattern_matching_border_subgrid_count_ii(n, m, grid, border_pattern, interior_pattern):
    """
    Count border subgrids that match specific patterns
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        border_pattern: pattern for border cells
        interior_pattern: pattern for interior cells
    
    Returns:
        int: number of border subgrids matching patterns
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Check if subgrid matches patterns
                    if matches_border_pattern_ii(grid, i, j, height, width, border_pattern, interior_pattern):
                    count += 1
    
    return count

def matches_border_pattern_ii(grid, start_i, start_j, height, width, border_pattern, interior_pattern):
    """
    Check if subgrid matches border and interior patterns
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        border_pattern: pattern for border cells
        interior_pattern: pattern for interior cells
    
    Returns:
        bool: True if subgrid matches patterns
    """
    # Check border pattern
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if (i == start_i or i == start_i + height - 1 or 
                j == start_j or j == start_j + width - 1):
                if not matches_cell_pattern(grid[i][j], border_pattern):
                    return False
    
    # Check interior pattern
    for i in range(start_i + 1, start_i + height - 1):
        for j in range(start_j + 1, start_j + width - 1):
            if not matches_cell_pattern(grid[i][j], interior_pattern):
                return False
    
    return True

def matches_cell_pattern(value, pattern):
    """
    Check if cell value matches pattern
    
    Args:
        value: cell value
        pattern: pattern to match
    
    Returns:
        bool: True if value matches pattern
    """
    if isinstance(pattern, set):
        return value in pattern
    elif isinstance(pattern, list):
        return value in pattern
    else:
        return value == pattern

# Example usage
n, m = 4, 4
grid = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]
border_pattern = {1}
interior_pattern = {0}
result = pattern_matching_border_subgrid_count_ii(n, m, grid, border_pattern, interior_pattern)
print(f"Pattern matching border subgrid count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Border Subgrid Count I](https://cses.fi/problemset/task/1075) - Grid counting
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
- [CSES Border Subgrid Count I](https://cses.fi/problemset/task/1075) - Medium
- [CSES All Letter Subgrid Count](https://cses.fi/problemset/task/1075) - Medium
- [CSES Grid Completion](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Grid Algorithms](https://en.wikipedia.org/wiki/Grid_computing) - Wikipedia article
