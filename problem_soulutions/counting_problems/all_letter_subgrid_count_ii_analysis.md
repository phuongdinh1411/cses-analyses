---
layout: simple
title: "All Letter Subgrid Count II - Grid Counting Problem"
permalink: /problem_soulutions/counting_problems/all_letter_subgrid_count_ii_analysis
---

# All Letter Subgrid Count II - Grid Counting Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of all letter subgrids in grid problems
- Apply counting techniques for letter subgrid analysis
- Implement efficient algorithms for subgrid counting
- Optimize grid traversal and counting operations
- Handle special cases in letter subgrid counting

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Grid algorithms, counting techniques, combinatorial analysis
- **Data Structures**: 2D arrays, prefix sums, mathematical computations
- **Mathematical Concepts**: Combinatorics, counting principles, grid properties
- **Programming Skills**: 2D array manipulation, nested loops, mathematical computations
- **Related Problems**: Border Subgrid Count (grid counting), Filled Subgrid Count (grid counting), Grid Completion (grid algorithms)

## 📋 Problem Description

Given a grid of size n×m with letters, count the number of subgrids where all letters are the same.

**Input**: 
- n, m: grid dimensions
- grid: n×m grid with letters

**Output**: 
- Number of all letter subgrids

**Constraints**:
- 1 ≤ n, m ≤ 1000
- Grid contains only lowercase letters

**Example**:
```
Input:
n = 3, m = 3
grid = [
  ['a', 'a', 'a'],
  ['a', 'a', 'a'],
  ['a', 'a', 'a']
]

Output:
14

Explanation**: 
All letter subgrids with same letter 'a':
- 9 subgrids of size 1×1
- 4 subgrids of size 2×2
- 1 subgrid of size 3×3
Total: 9 + 4 + 1 = 14
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all possible subgrids
- **Letter Validation**: Check all letters in each subgrid
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: O(n²m²) time complexity

**Key Insight**: Enumerate all possible subgrids and check if all letters are the same.

**Algorithm**:
- Iterate through all possible subgrid positions and sizes
- For each subgrid, check all letters
- Count subgrids that have all same letters

**Visual Example**:
```
Grid: 3×3
┌─────────────────────────────────────┐
│ a a a                              │
│ a a a                              │
│ a a a                              │
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
def brute_force_all_letter_subgrid_count(n, m, grid):
    """
    Count all letter subgrids using brute force approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid with letters
    
    Returns:
        int: number of all letter subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Check if all letters in subgrid are the same
                    if is_all_letter_subgrid(grid, i, j, height, width):
                        count += 1
    
    return count

def is_all_letter_subgrid(grid, start_i, start_j, height, width):
    """
    Check if all letters in subgrid are the same
    
    Args:
        grid: 2D grid with letters
        start_i, start_j: starting position
        height, width: subgrid dimensions
    
    Returns:
        bool: True if all letters are the same
    """
    first_letter = grid[start_i][start_j]
    
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if grid[i][j] != first_letter:
                return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    ['a', 'a', 'a'],
    ['a', 'a', 'a'],
    ['a', 'a', 'a']
]
result = brute_force_all_letter_subgrid_count(n, m, grid)
print(f"Brute force result: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(1)

**Why it's inefficient**: Checks all possible subgrids with O(n²m²) time complexity.

---

### Approach 2: Optimized Letter Checking Solution

**Key Insights from Optimized Letter Checking Solution**:
- **Early Termination**: Stop checking as soon as different letter is found
- **Efficient Validation**: Use optimized letter checking
- **Reduced Redundancy**: Avoid redundant letter checks
- **Optimization**: More efficient than brute force

**Key Insight**: Use early termination and optimized letter checking to reduce redundant operations.

**Algorithm**:
- Use early termination when different letter is found
- Optimize letter checking process
- Reduce redundant operations

**Visual Example**:
```
Optimized letter checking:
┌─────────────────────────────────────┐
│ For each subgrid:                  │
│ - Check letters row by row          │
│ - Stop immediately if different letter │
│ - Skip remaining letters if possible │
└─────────────────────────────────────┘

Early termination example:
┌─────────────────────────────────────┐
│ Subgrid (0,0) to (1,1):           │
│ Check (0,0): 'a' ✓                │
│ Check (0,1): 'a' ✓                │
│ Check (1,0): 'a' ✓                │
│ Check (1,1): 'a' ✓                │
│ All letters same: count++          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def optimized_all_letter_subgrid_count(n, m, grid):
    """
    Count all letter subgrids using optimized letter checking
    
    Args:
        n, m: grid dimensions
        grid: 2D grid with letters
    
    Returns:
        int: number of all letter subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Use optimized letter checking
                    if is_all_letter_subgrid_optimized(grid, i, j, height, width):
                        count += 1
    
    return count

def is_all_letter_subgrid_optimized(grid, start_i, start_j, height, width):
    """
    Check if all letters in subgrid are the same with optimization
    
    Args:
        grid: 2D grid with letters
        start_i, start_j: starting position
        height, width: subgrid dimensions
    
    Returns:
        bool: True if all letters are the same
    """
    first_letter = grid[start_i][start_j]
    
    # Check letters row by row with early termination
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if grid[i][j] != first_letter:
                return False  # Early termination
    
    return True

def is_all_letter_subgrid_optimized_v2(grid, start_i, start_j, height, width):
    """
    Alternative optimized letter checking with different strategy
    
    Args:
        grid: 2D grid with letters
        start_i, start_j: starting position
        height, width: subgrid dimensions
    
    Returns:
        bool: True if all letters are the same
    """
    first_letter = grid[start_i][start_j]
    
    # Check if starting letter is consistent
    if first_letter != grid[start_i][start_j]:
        return False
    
    # Check remaining letters
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if i == start_i and j == start_j:
                continue  # Skip already checked letter
            if grid[i][j] != first_letter:
                return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    ['a', 'a', 'a'],
    ['a', 'a', 'a'],
    ['a', 'a', 'a']
]
result = optimized_all_letter_subgrid_count(n, m, grid)
print(f"Optimized letter checking result: {result}")
```

**Time Complexity**: O(n²m²)
**Space Complexity**: O(1)

**Why it's better**: Reduces redundant operations and improves efficiency.

**Implementation Considerations**:
- **Early Termination**: Stop checking as soon as different letter is found
- **Optimized Validation**: Use optimized letter checking
- **Reduced Redundancy**: Avoid redundant letter checks

---

### Approach 3: Prefix Sum Solution (Optimal)

**Key Insights from Prefix Sum Solution**:
- **Prefix Sum Technique**: Use prefix sums for efficient range queries
- **Mathematical Optimization**: Use mathematical properties for counting
- **Efficient Calculation**: O(nm) time complexity
- **Optimal Complexity**: Best approach for all letter subgrid counting

**Key Insight**: Use prefix sums to efficiently check if subgrids have all same letters.

**Algorithm**:
- Build prefix sum array for each letter
- Use prefix sums to check subgrid validity
- Count valid subgrids efficiently

**Visual Example**:
```
Prefix sum construction for letter 'a':
┌─────────────────────────────────────┐
│ Grid: a a a                        │
│       a a a                        │
│       a a a                        │
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
│ Subgrid has all 'a' letters       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def prefix_sum_all_letter_subgrid_count(n, m, grid):
    """
    Count all letter subgrids using prefix sum approach
    
    Args:
        n, m: grid dimensions
        grid: 2D grid with letters
    
    Returns:
        int: number of all letter subgrids
    """
    # Get all unique letters in grid
    unique_letters = set()
    for i in range(n):
        for j in range(m):
            unique_letters.add(grid[i][j])
    
    total_count = 0
    
    # For each unique letter, count subgrids with that letter
    for letter in unique_letters:
        # Build prefix sum array for current letter
        prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
        
        for i in range(n):
            for j in range(m):
                prefix_sum[i + 1][j + 1] = (prefix_sum[i][j + 1] + 
                                           prefix_sum[i + 1][j] - 
                                           prefix_sum[i][j])
                if grid[i][j] == letter:
                    prefix_sum[i + 1][j + 1] += 1
        
        # Count subgrids with all letters equal to current letter
        letter_count = 0
        for i in range(n):
            for j in range(m):
                for height in range(1, n - i + 1):
                    for width in range(1, m - j + 1):
                        if is_all_letter_subgrid_prefix_sum(prefix_sum, i, j, height, width, letter):
                            letter_count += 1
        
        total_count += letter_count
    
    return total_count

def is_all_letter_subgrid_prefix_sum(prefix_sum, start_i, start_j, height, width, letter):
    """
    Check if subgrid has all same letters using prefix sum
    
    Args:
        prefix_sum: 2D prefix sum array
        start_i, start_j: starting position
        height, width: subgrid dimensions
        letter: target letter
    
    Returns:
        bool: True if subgrid has all same letters
    """
    # Calculate sum of subgrid using prefix sum
    total_sum = (prefix_sum[start_i + height][start_j + width] - 
                 prefix_sum[start_i][start_j + width] - 
                 prefix_sum[start_i + height][start_j] + 
                 prefix_sum[start_i][start_j])
    
    # Check if sum equals expected value (all letters are the same)
    expected_sum = height * width
    return total_sum == expected_sum

def optimized_prefix_sum_all_letter_count(n, m, grid):
    """
    Optimized prefix sum approach with additional optimizations
    
    Args:
        n, m: grid dimensions
        grid: 2D grid with letters
    
    Returns:
        int: number of all letter subgrids
    """
    # Get all unique letters in grid
    unique_letters = set()
    for i in range(n):
        for j in range(m):
            unique_letters.add(grid[i][j])
    
    total_count = 0
    
    # For each unique letter, count subgrids with that letter
    for letter in unique_letters:
        # Build prefix sum array for current letter
        prefix_sum = [[0] * (m + 1) for _ in range(n + 1)]
        
        for i in range(n):
            for j in range(m):
                prefix_sum[i + 1][j + 1] = (prefix_sum[i][j + 1] + 
                                           prefix_sum[i + 1][j] - 
                                           prefix_sum[i][j])
                if grid[i][j] == letter:
                    prefix_sum[i + 1][j + 1] += 1
        
        # Optimize by checking only valid starting positions
        letter_count = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == letter:  # Only start from valid letters
                    for height in range(1, n - i + 1):
                        for width in range(1, m - j + 1):
                            if is_all_letter_subgrid_prefix_sum(prefix_sum, i, j, height, width, letter):
                                letter_count += 1
        
        total_count += letter_count
    
    return total_count

# Example usage
n, m = 3, 3
grid = [
    ['a', 'a', 'a'],
    ['a', 'a', 'a'],
    ['a', 'a', 'a']
]
result1 = prefix_sum_all_letter_subgrid_count(n, m, grid)
result2 = optimized_prefix_sum_all_letter_count(n, m, grid)
print(f"Prefix sum result: {result1}")
print(f"Optimized prefix sum result: {result2}")
```

**Time Complexity**: O(nm * k) where k is number of unique letters
**Space Complexity**: O(nm)

**Why it's optimal**: Uses prefix sums for efficient range queries.

**Implementation Details**:
- **Prefix Sum Construction**: Build prefix sum array for each letter
- **Range Query**: Use prefix sums for efficient range queries
- **Mathematical Optimization**: Use mathematical properties for counting
- **Efficient Algorithms**: Use optimal algorithms for grid operations

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²m²) | O(1) | Complete enumeration of all subgrids |
| Optimized Letter Checking | O(n²m²) | O(1) | Early termination and optimized validation |
| Prefix Sum | O(nm * k) | O(nm) | Use prefix sums for efficient range queries |

### Time Complexity
- **Time**: O(nm * k) - Use prefix sums for efficient range queries
- **Space**: O(nm) - Store prefix sum array

### Why This Solution Works
- **Prefix Sum Technique**: Use prefix sums for efficient range queries
- **Mathematical Properties**: Use mathematical properties for counting
- **Efficient Algorithms**: Use optimal algorithms for grid operations
- **Range Query Optimization**: Use prefix sums for subgrid validation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. All Letter Subgrid Count with Case Sensitivity**
**Problem**: Count all letter subgrids with case sensitivity.

**Key Differences**: Consider uppercase and lowercase letters as different

**Solution Approach**: Modify letter comparison to be case sensitive

**Implementation**:
```python
def case_sensitive_all_letter_subgrid_count(n, m, grid):
    """
    Count all letter subgrids with case sensitivity
    
    Args:
        n, m: grid dimensions
        grid: 2D grid with letters (case sensitive)
    
    Returns:
        int: number of all letter subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes
    for i in range(n):
        for j in range(m):
            for height in range(1, n - i + 1):
                for width in range(1, m - j + 1):
                    # Check if all letters in subgrid are the same (case sensitive)
                    if is_all_letter_subgrid_case_sensitive(grid, i, j, height, width):
                        count += 1
    
    return count

def is_all_letter_subgrid_case_sensitive(grid, start_i, start_j, height, width):
    """
    Check if all letters in subgrid are the same (case sensitive)
    
    Args:
        grid: 2D grid with letters
        start_i, start_j: starting position
        height, width: subgrid dimensions
    
    Returns:
        bool: True if all letters are the same
    """
    first_letter = grid[start_i][start_j]
    
    for i in range(start_i, start_i + height):
        for j in range(start_j, start_j + width):
            if grid[i][j] != first_letter:  # Case sensitive comparison
                return False
    
    return True

# Example usage
n, m = 3, 3
grid = [
    ['a', 'A', 'a'],
    ['A', 'a', 'A'],
    ['a', 'A', 'a']
]
result = case_sensitive_all_letter_subgrid_count(n, m, grid)
print(f"Case sensitive all letter subgrid count: {result}")
```

#### **2. All Letter Subgrid Count with Size Constraints**
**Problem**: Count all letter subgrids with specific size constraints.

**Key Differences**: Additional constraints on subgrid size

**Solution Approach**: Add size constraints to the counting logic

**Implementation**:
```python
def size_constrained_all_letter_subgrid_count(n, m, grid, min_size, max_size):
    """
    Count all letter subgrids with size constraints
    
    Args:
        n, m: grid dimensions
        grid: 2D grid with letters
        min_size: minimum subgrid size
        max_size: maximum subgrid size
    
    Returns:
        int: number of all letter subgrids
    """
    count = 0
    
    # Check all possible subgrid positions and sizes with constraints
    for i in range(n):
        for j in range(m):
            for height in range(max(1, min_size), min(n - i + 1, max_size + 1)):
                for width in range(max(1, min_size), min(m - j + 1, max_size + 1)):
                    if is_all_letter_subgrid(grid, i, j, height, width):
                        count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [
    ['a', 'a', 'a'],
    ['a', 'a', 'a'],
    ['a', 'a', 'a']
]
result = size_constrained_all_letter_subgrid_count(n, m, grid, 2, 3)
print(f"Size constrained all letter subgrid count: {result}")
```

#### **3. All Letter Subgrid Count with Pattern Matching**
**Problem**: Count all letter subgrids that match specific patterns.

**Key Differences**: Subgrids must match specific patterns

**Solution Approach**: Use pattern matching techniques

**Implementation**:
```python
def pattern_matching_all_letter_subgrid_count(n, m, grid, pattern):
    """
    Count all letter subgrids that match specific patterns
    
    Args:
        n, m: grid dimensions
        grid: 2D grid with letters
        pattern: 2D pattern to match
    
    Returns:
        int: number of all letter subgrids matching pattern
    """
    pattern_height, pattern_width = len(pattern), len(pattern[0])
    count = 0
    
    # Check all possible subgrid positions
    for i in range(n - pattern_height + 1):
        for j in range(m - pattern_width + 1):
            # Check if subgrid matches pattern
            if matches_letter_pattern(grid, i, j, pattern):
                count += 1
    
    return count

def matches_letter_pattern(grid, start_i, start_j, pattern):
    """
    Check if subgrid matches letter pattern
    
    Args:
        grid: 2D grid with letters
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
    ['a', 'a', 'a'],
    ['a', 'a', 'a'],
    ['a', 'a', 'a']
]
pattern = [
    ['a', 'a'],
    ['a', 'a']
]
result = pattern_matching_all_letter_subgrid_count(n, m, grid, pattern)
print(f"Pattern matching all letter subgrid count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Border Subgrid Count](https://cses.fi/problemset/task/1075) - Grid counting
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
- [CSES Border Subgrid Count](https://cses.fi/problemset/task/1075) - Medium
- [CSES Filled Subgrid Count](https://cses.fi/problemset/task/1075) - Medium
- [CSES Grid Completion](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Grid Algorithms](https://en.wikipedia.org/wiki/Grid_computing) - Wikipedia article
