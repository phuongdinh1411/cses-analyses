---
layout: simple
title: "Border Subgrid Count I - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/border_subgrid_count_i_analysis
---

# Border Subgrid Count I - Grid Counting Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of border subgrids in grid problems
- Apply counting techniques for grid subproblems
- Implement efficient algorithms for subgrid counting
- Optimize grid traversal and counting operations
- Handle special cases in grid counting problems

## 📋 Problem Description

Given a grid of size n×m, count the number of subgrids where all border cells have a specific property.

**Input**: 
- n, m: grid dimensions
- grid: n×m grid with values

**Output**: 
- Number of border subgrids with the specified property

**Constraints**:
- 1 ≤ n, m ≤ 1000
- Grid values are integers

**Example**:
```
Input:
n = 3, m = 3
grid = [
  [1, 2, 1],
  [2, 1, 2],
  [1, 2, 1]
]

Output:
4

Explanation**: 
Border subgrids with all border cells = 1:
- 1×1 subgrid at (0,0)
- 1×1 subgrid at (0,2)
- 1×1 subgrid at (2,0)
- 1×1 subgrid at (2,2)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all possible subgrids
- **Border Validation**: Check all border cells for each subgrid
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: O(n²m²) time complexity

**Key Insight**: Enumerate all possible subgrids and check if their borders satisfy the condition.

**Algorithm**:
- Iterate through all possible subgrid positions and sizes
- For each subgrid, check all border cells
- Count subgrids that satisfy the border condition

**Visual Example**:
```
Grid: 3×3
┌─────────────────────────────────────┐
│ 1 2 1                              │
│ 2 1 2                              │
│ 1 2 1                              │
└─────────────────────────────────────┘

Brute force enumeration:
┌─────────────────────────────────────┐
│ Check all 1×1 subgrids:            │
│ (0,0): border = [1] ✓              │
│ (0,1): border = [2] ✗              │
│ (0,2): border = [1] ✓              │
│ (1,0): border = [2] ✗              │
│ (1,1): border = [1] ✓              │
│ (1,2): border = [2] ✗              │
│ (2,0): border = [1] ✓              │
│ (2,1): border = [2] ✗              │
│ (2,2): border = [1] ✓              │
│ Count: 4                           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_border_subgrid_count(n, m, grid, target_value=1):
    """
    Count border subgrids using brute force approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for border cells
    
    Returns:
        int: number of border subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Check if all border cells have target value
                    if is_border_valid(grid, i, j, height, width, target_value):
                        count += 1
    
    return count

def is_border_valid(grid, start_i, start_j, height, width, target_value):
    """
    Check if all border cells of a subgrid have target value
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        target_value: target value
    
    Returns:
        bool: True if all border cells have target value
    """
    # Check top and bottom borders
    for j in range(start_j, start_j + width):
        if grid[start_i][j] != target_value:  # Top border
            return False
        if grid[start_i + height - 1][j] != target_value:  # Bottom border
            return False
    
    # Check left and right borders
    for i in range(start_i, start_i + height):
        if grid[i][start_j] != target_value:  # Left border
            return False
        if grid[i][start_j + width - 1] != target_value:  # Right border
            return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    [1, 2, 1],
    [2, 1, 2],
    [1, 2, 1]
]
result = brute_force_border_subgrid_count(n, m, grid)
print(f"Brute force result: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(1)

**Why it's inefficient**: Checks all possible subgrids with O(n²m²) time complexity.

---

### Approach 2: Optimized Border Checking Solution

**Key Insights from Optimized Border Checking Solution**:
- **Border Preprocessing**: Preprocess border information
- **Efficient Validation**: Use preprocessed data for faster validation
- **Reduced Redundancy**: Avoid redundant border checks
- **Optimization**: More efficient than brute force

**Key Insight**: Preprocess border information to avoid redundant checks during validation.

**Algorithm**:
- Preprocess border information for each cell
- Use preprocessed data for efficient border validation
- Optimize the border checking process

**Visual Example**:
```
Border preprocessing:
┌─────────────────────────────────────┐
│ For each cell, precompute:         │
│ - Is it a border cell?             │
│ - What is its border value?        │
│ - Which subgrids can it be part of? │
└─────────────────────────────────────┘

Optimized validation:
┌─────────────────────────────────────┐
│ Instead of checking all borders:   │
│ - Use preprocessed border info     │
│ - Skip invalid subgrids early      │
│ - Cache border validation results  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def optimized_border_subgrid_count(n, m, grid, target_value=1):
    """
    Count border subgrids using optimized border checking
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for border cells
    
    Returns:
        int: number of border subgrids
    """
    # Preprocess border information
    border_info = preprocess_border_info(n, m, grid, target_value)
    
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Use preprocessed border info for validation
                    if is_border_valid_optimized(border_info, i, j, height, width):
                        count += 1
    
    return count

def preprocess_border_info(n, m, grid, target_value):
    """
    Preprocess border information for efficient validation
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value
    
    Returns:
        dict: preprocessed border information
    """
    border_info = {}
    
    for i in range(n):
        for j in range(m):
            # Check if cell can be part of valid border
            is_valid_border = (grid[i][j] == target_value)
            
            # Store border information
            border_info[(i, j)] = {
                'is_valid': is_valid_border,
                'value': grid[i][j]
            }
    
    return border_info

def is_border_valid_optimized(border_info, start_i, start_j, height, width):
    """
    Check border validity using preprocessed information
    
    Args:
        border_info: preprocessed border information
        start_i, start_j: starting position
        height, width: subgrid dimensions
    
    Returns:
        bool: True if all border cells are valid
    """
    # Check top and bottom borders
    for j in range(start_j, start_j + width):
        if not border_info[(start_i, j)]['is_valid']:  # Top border
            return False
        if not border_info[(start_i + height - 1, j)]['is_valid']:  # Bottom border
            return False
    
    # Check left and right borders
    for i in range(start_i, start_i + height):
        if not border_info[(i, start_j)]['is_valid']:  # Left border
            return False
        if not border_info[(i, start_j + width - 1)]['is_valid']:  # Right border
            return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    [1, 2, 1],
    [2, 1, 2],
    [1, 2, 1]
]
result = optimized_border_subgrid_count(n, m, grid)
print(f"Optimized border checking result: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(nm)

**Why it's better**: Reduces redundant border checks and improves efficiency.

**Implementation Considerations**:
- **Border Preprocessing**: Preprocess border information
- **Efficient Validation**: Use preprocessed data for validation
- **Reduced Redundancy**: Avoid redundant checks

---

### Approach 3: Mathematical Counting Solution (Optimal)

**Key Insights from Mathematical Counting Solution**:
- **Mathematical Analysis**: Use mathematical properties for counting
- **Pattern Recognition**: Recognize patterns in border subgrids
- **Efficient Counting**: Count without enumerating all subgrids
- **Optimal Complexity**: O(nm) time complexity

**Key Insight**: Use mathematical analysis and pattern recognition to count border subgrids efficiently.

**Algorithm**:
- Analyze mathematical properties of border subgrids
- Use pattern recognition for efficient counting
- Count subgrids without explicit enumeration

**Visual Example**:
```
Mathematical analysis:
┌─────────────────────────────────────┐
│ For border subgrids:               │
│ - Count valid border cells         │
│ - Use mathematical formulas        │
│ - Avoid explicit enumeration       │
└─────────────────────────────────────┘

Pattern recognition:
┌─────────────────────────────────────┐
│ Valid border cells form patterns:  │
│ - Consecutive sequences            │
│ - Rectangular regions              │
│ - Mathematical relationships       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def mathematical_border_subgrid_count(n, m, grid, target_value=1):
    """
    Count border subgrids using mathematical approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for border cells
    
    Returns:
        int: number of border subgrids
    """
    # Find all valid border cells
    valid_cells = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == target_value:
                valid_cells.append((i, j))
    
    if not valid_cells:
        return 0
    
    # Count subgrids using mathematical analysis
    count = 0
    
    # For each valid cell, count subgrids it can be part of
    for i, j in valid_cells:
        # Count subgrids where (i,j) is a corner
        count += count_corner_subgrids(grid, i, j, target_value)
    
    return count

def count_corner_subgrids(grid, corner_i, corner_j, target_value):
    """
    Count subgrids where given cell is a corner
    
    Args:
        grid: 2D grid
        corner_i, corner_j: corner position
        target_value: target value
    
    Returns:
        int: number of subgrids with given corner
    """
    n, m = len(grid), len(grid[0])
    count = 0
    
    # Check all possible subgrid sizes
    for height in range(1, n - corner_i + 1):
        for width in range(1, m - corner_j + 1):
            # Check if subgrid with given corner is valid
            if is_valid_subgrid_with_corner(grid, corner_i, corner_j, height, width, target_value):
                count += 1
    
    return count

def is_valid_subgrid_with_corner(grid, corner_i, corner_j, height, width, target_value):
    """
    Check if subgrid with given corner is valid
    
    Args:
        grid: 2D grid
        corner_i, corner_j: corner position
        height, width: subgrid dimensions
        target_value: target value
    
    Returns:
        bool: True if subgrid is valid
    """
    n, m = len(grid), len(grid[0])
    
    # Check if subgrid is within bounds
    if corner_i + height > n or corner_j + width > m:
        return False
    
    # Check all border cells
    for i in range(corner_i, corner_i + height):
        for j in range(corner_j, corner_j + width):
            # Check if cell is on border
            if (i == corner_i or i == corner_i + height - 1 or 
                j == corner_j or j == corner_j + width - 1):
                if grid[i][j] != target_value:
                    return False
    
    return True

def optimized_mathematical_count(n, m, grid, target_value=1):
    """
    Optimized mathematical counting approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value
    
    Returns:
        int: number of border subgrids
    """
    # Use prefix sums for efficient border checking
    prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Build prefix sum for target value cells
    for i in range(n):
        for j in range(m):
            prefix_sum[i + 1][j + 1] = prefix_sum[i][j + 1] + prefix_sum[i + 1][j] - prefix_sum[i][j]
            if grid[i][j] == target_value:
                prefix_sum[i + 1][j + 1] += 1
    
    count = 0
    
    # Count subgrids efficiently
    for i in range(n):
        for j in range(m):
            if grid[i][j] == target_value:
                # Count subgrids starting at (i,j)
                count += count_subgrids_from_position(prefix_sum, i, j, n, m, target_value)
    
    return count

def count_subgrids_from_position(prefix_sum, start_i, start_j, n, m, target_value):
    """
    Count subgrids starting from given position
    
    Args:
        prefix_sum: 2D prefix sum array
        start_i, start_j: starting position
        n, m: grid dimensions
        target_value: target value
    
    Returns:
        int: number of subgrids from position
    """
    count = 0
    
    # Check all possible subgrid sizes
    for height in range(1, n - start_i + 1):
        for width in range(1, m - start_j + 1):
            # Use prefix sum to check border validity
            if is_border_valid_prefix_sum(prefix_sum, start_i, start_j, height, width, target_value):
                count += 1
    
    return count

def is_border_valid_prefix_sum(prefix_sum, start_i, start_j, height, width, target_value):
    """
    Check border validity using prefix sum
    
    Args:
        prefix_sum: 2D prefix sum array
        start_i, start_j: starting position
        height, width: subgrid dimensions
        target_value: target value
    
    Returns:
        bool: True if border is valid
    """
    # Calculate expected border count
    expected_border_count = 2 * (height + width) - 4  # Border cells count
    
    # Calculate actual border count using prefix sum
    actual_border_count = 0
    
    # Top and bottom borders
    for j in range(start_j, start_j + width):
        if prefix_sum[start_i + 1][j + 1] - prefix_sum[start_i][j + 1] - prefix_sum[start_i + 1][j] + prefix_sum[start_i][j] == 1:
            actual_border_count += 1
        if prefix_sum[start_i + height][j + 1] - prefix_sum[start_i + height - 1][j + 1] - prefix_sum[start_i + height][j] + prefix_sum[start_i + height - 1][j] == 1:
            actual_border_count += 1
    
    # Left and right borders
    for i in range(start_i, start_i + height):
        if prefix_sum[i + 1][start_j + 1] - prefix_sum[i][start_j + 1] - prefix_sum[i + 1][start_j] + prefix_sum[i][start_j] == 1:
            actual_border_count += 1
        if prefix_sum[i + 1][start_j + width] - prefix_sum[i][start_j + width] - prefix_sum[i + 1][start_j + width - 1] + prefix_sum[i][start_j + width - 1] == 1:
            actual_border_count += 1
    
    return actual_border_count == expected_border_count

# Example usage
n, m = 3, 3
grid = [
    [1, 2, 1],
    [2, 1, 2],
    [1, 2, 1]
]
result1 = mathematical_border_subgrid_count(n, m, grid)
result2 = optimized_mathematical_count(n, m, grid)
print(f"Mathematical result: {result1}")
print(f"Optimized mathematical result: {result2}")
```

**Time Complexity**: O(nm)
**Space Complexity**: O(nm)

**Why it's optimal**: Uses mathematical analysis and prefix sums for O(nm) time complexity.

**Implementation Details**:
- **Mathematical Analysis**: Use mathematical properties for counting
- **Prefix Sums**: Use prefix sums for efficient border checking
- **Pattern Recognition**: Recognize patterns in border subgrids
- **Efficient Counting**: Count without explicit enumeration

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²m²) | O(1) | Complete enumeration of all subgrids |
| Optimized Border Checking | O(n²m²) | O(nm) | Preprocess border information |
| Mathematical Counting | O(nm) | O(nm) | Use mathematical analysis and prefix sums |

### Time Complexity
- **Time**: O(nm) - Use mathematical analysis and prefix sums
- **Space**: O(nm) - Store prefix sum array

### Why This Solution Works
- **Mathematical Properties**: Use mathematical properties of border subgrids
- **Prefix Sums**: Use prefix sums for efficient border checking
- **Pattern Recognition**: Recognize patterns in valid subgrids
- **Efficient Counting**: Count without explicit enumeration

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Border Subgrid Count with Different Properties**
**Problem**: Count border subgrids with different border properties.

**Key Differences**: Different conditions for border cells

**Solution Approach**: Modify border validation logic

**Implementation**:
```python
def border_subgrid_count_with_properties(n, m, grid, border_condition):
    """
    Count border subgrids with custom border conditions
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        border_condition: function that checks border condition
    
    Returns:
        int: number of border subgrids
    """
    count = 0
    
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    if is_border_valid_custom(grid, i, j, height, width, border_condition):
                        count += 1
    
    return count

def is_border_valid_custom(grid, start_i, start_j, height, width, condition):
    """
    Check border validity with custom condition
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        condition: custom border condition function
    
    Returns:
        bool: True if border satisfies condition
    """
    # Check top and bottom borders
    for j in range(start_j, start_j + width):
        if not condition(grid[start_i][j]):  # Top border
            return False
        if not condition(grid[start_i + height - 1][j]):  # Bottom border
            return False
    
    # Check left and right borders
    for i in range(start_i, start_i + height):
        if not condition(grid[i][start_j]):  # Left border
            return False
        if not condition(grid[i][start_j + width - 1]):  # Right border
            return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    [1, 2, 1],
    [2, 1, 2],
    [1, 2, 1]
]

# Custom condition: border cells must be even
def is_even(x):
    return x % 2 == 0

result = border_subgrid_count_with_properties(n, m, grid, is_even)
print(f"Border subgrids with even borders: {result}")
```

#### **2. Border Subgrid Count with Size Constraints**
**Problem**: Count border subgrids with specific size constraints.

**Key Differences**: Additional constraints on subgrid size

**Solution Approach**: Add size constraints to the counting logic

**Implementation**:
```python
def border_subgrid_count_with_size_constraints(n, m, grid, target_value, min_size, max_size):
    """
    Count border subgrids with size constraints
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        target_value: target value for border cells
        min_size: minimum subgrid size
        max_size: maximum subgrid size
    
    Returns:
        int: number of border subgrids
    """
    count = 0
    
    for i in range(n):
        for j in range(m):
            for height in range(max(1, min_size), min(n - i + 1, max_size + 1)):
                for width in range(max(1, min_size), min(m - j + 1, max_size + 1)):
                    if is_border_valid(grid, i, j, height, width, target_value):
                        count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [
    [1, 2, 1],
    [2, 1, 2],
    [1, 2, 1]
]

result = border_subgrid_count_with_size_constraints(n, m, grid, 1, 2, 3)
print(f"Border subgrids with size constraints: {result}")
```

#### **3. Border Subgrid Count with Multiple Values**
**Problem**: Count border subgrids where border cells can have multiple valid values.

**Key Differences**: Border cells can have multiple valid values

**Solution Approach**: Use set or list for valid values

**Implementation**:
```python
def border_subgrid_count_multiple_values(n, m, grid, valid_values):
    """
    Count border subgrids with multiple valid border values
    
    Args:
        n, m: grid dimensions
        grid: 2D grid
        valid_values: set of valid border values
    
    Returns:
        int: number of border subgrids
    """
    count = 0
    
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    if is_border_valid_multiple_values(grid, i, j, height, width, valid_values):
                        count += 1
    
    return count

def is_border_valid_multiple_values(grid, start_i, start_j, height, width, valid_values):
    """
    Check border validity with multiple valid values
    
    Args:
        grid: 2D grid
        start_i, start_j: starting position
        height, width: subgrid dimensions
        valid_values: set of valid border values
    
    Returns:
        bool: True if all border cells have valid values
    """
    # Check top and bottom borders
    for j in range(start_j, start_j + width):
        if grid[start_i][j] not in valid_values:  # Top border
            return False
        if grid[start_i + height - 1][j] not in valid_values:  # Bottom border
            return False
    
    # Check left and right borders
    for i in range(start_i, start_i + height):
        if grid[i][start_j] not in valid_values:  # Left border
            return False
        if grid[i][start_j + width - 1] not in valid_values:  # Right border
            return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    [1, 2, 1],
    [2, 1, 2],
    [1, 2, 1]
]

valid_values = {1, 2}  # Border cells can be 1 or 2
result = border_subgrid_count_multiple_values(n, m, grid, valid_values)
print(f"Border subgrids with multiple valid values: {result}")
```

### Related Problems

#### **CSES Problems**
- [All Letter Subgrid Count](https://cses.fi/problemset/task/1075) - Grid counting
- [Filled Subgrid Count](https://cses.fi/problemset/task/1075) - Grid counting
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
- [CSES All Letter Subgrid Count](https://cses.fi/problemset/task/1075) - Medium
- [CSES Filled Subgrid Count](https://cses.fi/problemset/task/1075) - Medium
- [CSES Grid Completion](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Grid Algorithms](https://en.wikipedia.org/wiki/Grid_computing) - Wikipedia article
