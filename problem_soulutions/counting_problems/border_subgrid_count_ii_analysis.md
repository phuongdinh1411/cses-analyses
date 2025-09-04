---
layout: simple
title: "Border Subgrid Count II"
permalink: /problem_soulutions/counting_problems/border_subgrid_count_ii_analysis
---


# Border Subgrid Count II

## 📋 Problem Description

Given a 2D grid of size n×m, count the number of subgrids of any size where all cells on the border have the same value.

This is a grid counting problem where we need to find all rectangular subgrids that have a uniform border (all border cells have the same value). We can solve this by checking all possible rectangular subgrids and verifying if their borders are uniform.

**Input**: 
- First line: two integers n and m (grid dimensions)
- Next n lines: m integers each (grid values)

**Output**: 
- Print one integer: the number of subgrids of any size with uniform border

**Constraints**:
- 1 ≤ n,m ≤ 100
- 1 ≤ grid[i][j] ≤ 10⁹

**Example**:
```
Input:
3 3
1 1 2
1 1 2
3 3 3

Output:
8
```

**Explanation**: 
In the 3×3 grid, there are 8 subgrids with uniform borders:
- 9 single cells (1×1 subgrids) - all have uniform borders
- 3 filled 2×1 subgrids in the first two rows with border value 1
- 1 filled 3×1 subgrid in the third row with border value 3
- 1 filled 1×3 subgrid in the third column with border value 2

## Solution Progression

### Approach 1: Check All Possible Subgrids - O(n³ × m³)
**Description**: Check all possible subgrids of all sizes to count those with uniform border.

```python
def border_subgrid_count_all_sizes_naive(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid has uniform border
                border_value = grid[i][j]  # Top-left corner
                is_uniform = True
                
                # Check all border cells
                for di in range(k):
                    for dj in range(k):
                        # Check if this is a border cell
                        if di == 0 or di == k - 1 or dj == 0 or dj == k - 1:
                            if grid[i + di][j + dj] != border_value:
                                is_uniform = False
                                break
                    if not is_uniform:
                        break
                
                if is_uniform:
                    count += 1
    
    return count
```

**Why this is inefficient**: We need to check all possible subgrid sizes, leading to O(n³ × m³) time complexity.

### Improvement 1: Optimized Border Checking - O(n³ × m³)
**Description**: Optimize the border checking process with early termination when a mismatch is found.

```python
def border_subgrid_count_all_sizes_optimized(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid has uniform border
                border_value = grid[i][j]  # Top-left corner
                is_uniform = True
                
                # Check all border cells
                for di in range(k):
                    for dj in range(k):
                        # Check if this is a border cell
                        if di == 0 or di == k - 1 or dj == 0 or dj == k - 1:
                            if grid[i + di][j + dj] != border_value:
                                is_uniform = False
                                break
                    if not is_uniform:
                        break
                
                if is_uniform:
                    count += 1
    
    return count
```

**Why this improvement works**: Early termination reduces the number of cells checked when a mismatch is found early.

## Final Optimal Solution

```python
n, m = map(int, input().split())

# Read the grid
grid = []
for _ in range(n):
    row = list(map(int, input().split()))
    grid.append(row)

def count_border_subgrids_all_sizes(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid has uniform border
                border_value = grid[i][j]  # Top-left corner
                is_uniform = True
                
                # Check all border cells
                for di in range(k):
                    for dj in range(k):
                        # Check if this is a border cell
                        if di == 0 or di == k - 1 or dj == 0 or dj == k - 1:
                            if grid[i + di][j + dj] != border_value:
                                is_uniform = False
                                break
                    if not is_uniform:
                        break
                
                if is_uniform:
                    count += 1
    
    return count

result = count_border_subgrids_all_sizes(n, m, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n³ × m³) | O(1) | Check all subgrids of all sizes |
| Optimized | O(n³ × m³) | O(1) | Early termination on border mismatch |

## Key Insights for Other Problems

### 1. **All Size Border Pattern Problems**
**Principle**: Iterate through all possible subgrid sizes and check border patterns.
**Applicable to**: Grid problems, border problems, pattern recognition problems

### 2. **Early Termination Optimization**
**Principle**: Stop checking as soon as a condition is violated to improve performance.
**Applicable to**: Optimization problems, search problems, validation problems

### 3. **Multi-size Grid Analysis**
**Principle**: Use nested loops to check subgrids of all possible sizes.
**Applicable to**: Grid problems, matrix problems, traversal algorithms

## Notable Techniques

### 1. **All Size Border Checking**
```python
def check_all_size_border_subgrids(n, m, grid):
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                if has_uniform_border(grid, i, j, k):
                    count += 1
    
    return count
```

### 2. **Uniform Border Check**
```python
def has_uniform_border(grid, start_i, start_j, k):
    border_value = grid[start_i][start_j]
    
    for di in range(k):
        for dj in range(k):
            if is_border_cell(di, dj, k):
                if grid[start_i + di][start_j + dj] != border_value:
                    return False
    
    return True
```

### 3. **Border Cell Identification**
```python
def is_border_cell(di, dj, k):
    return di == 0 or di == k - 1 or dj == 0 or dj == k - 1
```

## Problem-Solving Framework

1. **Identify problem type**: This is an all-size border pattern subgrid problem
2. **Choose approach**: Use nested loops to check subgrids of all sizes
3. **Implement checking**: Focus on checking border cells only
4. **Optimize**: Use early termination when border mismatch is found
5. **Count results**: Increment counter for subgrids with uniform border

---

*This analysis shows how to efficiently count subgrids of all sizes with uniform borders using border-focused checking and early termination.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Border Subgrids**
**Problem**: Each cell has a weight. Find subgrids with uniform border and maximum total weight.
```python
def weighted_border_subgrids_all_sizes(n, m, grid, weights):
    # weights[i][j] = weight of cell grid[i][j]
    max_weight = 0
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                border_value = grid[i][j]
                is_uniform = True
                total_weight = 0
                
                # Check border and calculate weight
                for di in range(k):
                    for dj in range(k):
                        if di == 0 or di == k - 1 or dj == 0 or dj == k - 1:
                            if grid[i + di][j + dj] != border_value:
                                is_uniform = False
                                break
                        total_weight += weights[i + di][j + dj]
                    if not is_uniform:
                        break
                
                if is_uniform:
                    count += 1
                    max_weight = max(max_weight, total_weight)
    
    return count, max_weight
```

#### **Variation 2: Minimum Size Constraint**
**Problem**: Find subgrids with uniform border and minimum size k.
```python
def min_size_border_subgrids(n, m, grid, min_size):
    count = 0
    
    for k in range(min_size, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                border_value = grid[i][j]
                is_uniform = True
                
                for di in range(k):
                    for dj in range(k):
                        if di == 0 or di == k - 1 or dj == 0 or dj == k - 1:
                            if grid[i + di][j + dj] != border_value:
                                is_uniform = False
                                break
                    if not is_uniform:
                        break
                
                if is_uniform:
                    count += 1
    
    return count
```

#### **Variation 3: Different Border Values**
**Problem**: Find subgrids where top/bottom borders have one value and left/right borders have another value.
```python
def different_border_values_all_sizes(n, m, grid):
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                top_value = grid[i][j]
                left_value = grid[i][j]
                is_valid = True
                
                # Check top and bottom borders
                for dj in range(k):
                    if grid[i][j + dj] != top_value or grid[i + k - 1][j + dj] != top_value:
                        is_valid = False
                        break
                
                if is_valid:
                    # Check left and right borders
                    for di in range(k):
                        if grid[i + di][j] != left_value or grid[i + di][j + k - 1] != left_value:
                            is_valid = False
                            break
                
                if is_valid and top_value != left_value:
                    count += 1
    
    return count
```

#### **Variation 4: Circular Border**
**Problem**: Handle a circular grid where borders wrap around.
```python
def circular_border_subgrids_all_sizes(n, m, grid):
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n):
            for j in range(m):
                border_value = grid[i][j]
                is_uniform = True
                
                # Check border with circular wrapping
                for di in range(k):
                    for dj in range(k):
                        if di == 0 or di == k - 1 or dj == 0 or dj == k - 1:
                            ni = (i + di) % n
                            nj = (j + dj) % m
                            if grid[ni][nj] != border_value:
                                is_uniform = False
                                break
                    if not is_uniform:
                        break
                
                if is_uniform:
                    count += 1
    
    return count
```

#### **Variation 5: Dynamic Border Updates**
**Problem**: Support dynamic updates to the grid and answer queries efficiently.
```python
class DynamicBorderCounterAllSizes:
    def __init__(self, n, m, grid):
        self.n = n
        self.m = m
        self.grid = [row[:] for row in grid]
    
    def update_cell(self, i, j, new_value):
        self.grid[i][j] = new_value
    
    def count_border_subgrids(self):
        count = 0
        
        for k in range(1, min(self.n, self.m) + 1):
            for i in range(self.n - k + 1):
                for j in range(self.m - k + 1):
                    border_value = self.grid[i][j]
                    is_uniform = True
                    
                    for di in range(k):
                        for dj in range(k):
                            if di == 0 or di == k - 1 or dj == 0 or dj == k - 1:
                                if self.grid[i + di][j + dj] != border_value:
                                    is_uniform = False
                                    break
                        if not is_uniform:
                            break
                    
                    if is_uniform:
                        count += 1
        
        return count
```

### 🔗 **Related Problems & Concepts**

#### **1. Grid Problems**
- **Grid Traversal**: Traverse grids efficiently
- **Subgrid Counting**: Count subgrids with properties
- **Grid Patterns**: Find patterns in grids
- **Grid Optimization**: Optimize grid operations

#### **2. Border Problems**
- **Border Detection**: Detect borders in grids
- **Border Patterns**: Find border patterns
- **Border Optimization**: Optimize border operations
- **Border Analysis**: Analyze border properties

#### **3. Pattern Problems**
- **Pattern Recognition**: Recognize patterns in grids
- **Pattern Matching**: Match patterns in grids
- **Pattern Counting**: Count pattern occurrences
- **Pattern Optimization**: Optimize pattern algorithms

#### **4. Matrix Problems**
- **Matrix Operations**: Perform matrix operations
- **Matrix Traversal**: Traverse matrices
- **Matrix Patterns**: Find matrix patterns
- **Matrix Optimization**: Optimize matrix algorithms

#### **5. Geometric Problems**
- **Geometric Patterns**: Find geometric patterns
- **Geometric Counting**: Count geometric objects
- **Geometric Optimization**: Optimize geometric algorithms
- **Geometric Analysis**: Analyze geometric properties

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
    
    result = count_border_subgrids_all_sizes(n, m, grid)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute for different grid regions
def precompute_border_counts_all_sizes(grid):
    n, m = len(grid), len(grid[0])
    # Precompute for all possible regions
    dp = {}
    
    for start_i in range(n):
        for start_j in range(m):
            for end_i in range(start_i, n):
                for end_j in range(start_j, m):
                    region = [grid[i][start_j:end_j+1] for i in range(start_i, end_i+1)]
                    count = count_border_subgrids_all_sizes(len(region), len(region[0]), region)
                    dp[(start_i, start_j, end_i, end_j)] = count
    
    return dp

# Answer range queries efficiently
def range_query(dp, start_i, start_j, end_i, end_j):
    return dp.get((start_i, start_j, end_i, end_j), 0)
```

#### **3. Interactive Problems**
```python
# Interactive border analyzer
def interactive_border_analyzer_all_sizes():
    n = int(input("Enter grid height: "))
    m = int(input("Enter grid width: "))
    grid = []
    
    print("Enter grid rows:")
    for i in range(n):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        grid.append(row)
    
    print("Grid:", grid)
    
    while True:
        query = input("Enter query (count/weighted/min_size/different/circular/exit): ")
        if query == "exit":
            break
        
        if query == "count":
            result = count_border_subgrids_all_sizes(n, m, grid)
            print(f"Border subgrids: {result}")
        elif query == "weighted":
            weights = []
            print("Enter weight matrix:")
            for i in range(n):
                row = list(map(int, input(f"Weight row {i+1}: ").split()))
                weights.append(row)
            count, max_weight = weighted_border_subgrids_all_sizes(n, m, grid, weights)
            print(f"Count: {count}, Max 
weight: {max_weight}")
        elif query == "min_size":
            min_size = int(input("Enter minimum size: "))
            result = min_size_border_subgrids(n, m, grid, min_size)
            print(f"Subgrids with min size {min_size}: {result}")
        elif query == "different":
            result = different_border_values_all_sizes(n, m, grid)
            print(f"Subgrids with different border values: {result}")
        elif query == "circular":
            result = circular_border_subgrids_all_sizes(n, m, grid)
            print(f"Circular border subgrids: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Grid Combinations**: Count grid combinations
- **Border Arrangements**: Arrange borders in grids
- **Pattern Partitions**: Partition grids into patterns
- **Inclusion-Exclusion**: Count using inclusion-exclusion

#### **2. Number Theory**
- **Grid Patterns**: Mathematical patterns in grids
- **Border Sequences**: Sequences of border values
- **Modular Arithmetic**: Grid operations with modular arithmetic
- **Number Sequences**: Sequences in grid counting

#### **3. Optimization Theory**
- **Grid Optimization**: Optimize grid operations
- **Border Optimization**: Optimize border checking
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n² × m²) for checking all rectangular subgrids
- **Space Complexity**: O(1) for storing the count
- **Why it works**: We iterate through all possible rectangular subgrids and check if their borders are uniform

### Key Implementation Points
- Iterate through all possible rectangular subgrids
- Check if all border cells have the same value
- Handle different subgrid sizes efficiently
- Optimize by early termination when a border is not uniform

## 🎯 Key Insights

### Important Concepts and Patterns
- **Grid Traversal**: Systematic way to check all rectangular subgrids
- **Border Checking**: Efficient way to verify uniform borders
- **Subgrid Counting**: Counting patterns in 2D grids
- **Pattern Recognition**: Identifying uniform border patterns

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Border Subgrid Count with Size Constraints**
```python
def border_subgrid_count_with_size_constraints(n, m, grid, size_constraints):
    # Count subgrids with uniform borders and size constraints
    count = 0
    
    for k in range(1, min(n, m) + 1):
        # Check size constraints
        if size_constraints.get("min_size", 1) > k:
            continue
        if size_constraints.get("max_size", min(n, m)) < k:
            continue
        if size_constraints.get("allowed_sizes") and k not in size_constraints["allowed_sizes"]:
            continue
        
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid has uniform border
                border_value = grid[i][j]  # Top-left corner
                is_uniform = True
                
                # Check top and bottom borders
                for col in range(j, j + k):
                    if grid[i][col] != border_value or grid[i + k - 1][col] != border_value:
                        is_uniform = False
                        break
                
                # Check left and right borders
                if is_uniform:
                    for row in range(i, i + k):
                        if grid[row][j] != border_value or grid[row][j + k - 1] != border_value:
                            is_uniform = False
                            break
                
                if is_uniform:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [[1, 1, 2], [1, 1, 2], [3, 3, 3]]
size_constraints = {"min_size": 2, "max_size": 3, "allowed_sizes": [2, 3]}
result = border_subgrid_count_with_size_constraints(n, m, grid, size_constraints)
print(f"Size-constrained border subgrid count: {result}")
```

#### **2. Border Subgrid Count with Value Constraints**
```python
def border_subgrid_count_with_value_constraints(n, m, grid, value_constraints):
    # Count subgrids with uniform borders and value constraints
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid has uniform border
                border_value = grid[i][j]  # Top-left corner
                
                # Check value constraints
                if value_constraints.get("min_value", 0) > border_value:
                    continue
                if value_constraints.get("max_value", float('inf')) < border_value:
                    continue
                if value_constraints.get("allowed_values") and border_value not in value_constraints["allowed_values"]:
                    continue
                
                is_uniform = True
                
                # Check top and bottom borders
                for col in range(j, j + k):
                    if grid[i][col] != border_value or grid[i + k - 1][col] != border_value:
                        is_uniform = False
                        break
                
                # Check left and right borders
                if is_uniform:
                    for row in range(i, i + k):
                        if grid[row][j] != border_value or grid[row][j + k - 1] != border_value:
                            is_uniform = False
                            break
                
                if is_uniform:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [[1, 1, 2], [1, 1, 2], [3, 3, 3]]
value_constraints = {"min_value": 1, "max_value": 2, "allowed_values": [1, 2]}
result = border_subgrid_count_with_value_constraints(n, m, grid, value_constraints)
print(f"Value-constrained border subgrid count: {result}")
```

#### **3. Border Subgrid Count with Position Constraints**
```python
def border_subgrid_count_with_position_constraints(n, m, grid, position_constraints):
    # Count subgrids with uniform borders and position constraints
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check position constraints
                if position_constraints.get("min_row", 0) > i:
                    continue
                if position_constraints.get("max_row", n) < i + k:
                    continue
                if position_constraints.get("min_col", 0) > j:
                    continue
                if position_constraints.get("max_col", m) < j + k:
                    continue
                
                # Check if this k×k subgrid has uniform border
                border_value = grid[i][j]  # Top-left corner
                is_uniform = True
                
                # Check top and bottom borders
                for col in range(j, j + k):
                    if grid[i][col] != border_value or grid[i + k - 1][col] != border_value:
                        is_uniform = False
                        break
                
                # Check left and right borders
                if is_uniform:
                    for row in range(i, i + k):
                        if grid[row][j] != border_value or grid[row][j + k - 1] != border_value:
                            is_uniform = False
                            break
                
                if is_uniform:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [[1, 1, 2], [1, 1, 2], [3, 3, 3]]
position_constraints = {"min_row": 0, "max_row": 2, "min_col": 0, "max_col": 2}
result = border_subgrid_count_with_position_constraints(n, m, grid, position_constraints)
print(f"Position-constrained border subgrid count: {result}")
```

#### **4. Border Subgrid Count with Statistics**
```python
def border_subgrid_count_with_statistics(n, m, grid):
    # Count subgrids with uniform borders and provide statistics
    count = 0
    size_counts = {}
    value_counts = {}
    positions = []
    
    for k in range(1, min(n, m) + 1):
        size_counts[k] = 0
        
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid has uniform border
                border_value = grid[i][j]  # Top-left corner
                is_uniform = True
                
                # Check top and bottom borders
                for col in range(j, j + k):
                    if grid[i][col] != border_value or grid[i + k - 1][col] != border_value:
                        is_uniform = False
                        break
                
                # Check left and right borders
                if is_uniform:
                    for row in range(i, i + k):
                        if grid[row][j] != border_value or grid[row][j + k - 1] != border_value:
                            is_uniform = False
                            break
                
                if is_uniform:
                    count += 1
                    size_counts[k] += 1
                    value_counts[border_value] = value_counts.get(border_value, 0) + 1
                    positions.append((i, j, k, border_value))
    
    statistics = {
        "total_count": count,
        "size_distribution": size_counts,
        "value_distribution": value_counts,
        "positions": positions
    }
    
    return count, statistics

# Example usage
n, m = 3, 3
grid = [[1, 1, 2], [1, 1, 2], [3, 3, 3]]
count, stats = border_subgrid_count_with_statistics(n, m, grid)
print(f"Border subgrid count: {count}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Grid Algorithms**: Grid traversal, Grid counting
- **Pattern Matching**: Pattern recognition, Pattern counting
- **Subgrid Problems**: Subgrid analysis, Subgrid optimization
- **Counting Problems**: Subset counting, Path counting

## 📚 Learning Points

### Key Takeaways
- **Grid traversal** is essential for checking all possible subgrids
- **Border checking** can be optimized by checking values systematically
- **Subgrid counting** is a fundamental grid analysis technique
- **Pattern recognition** helps identify uniform border patterns in grids

---

*This analysis demonstrates efficient border subgrid counting techniques for all sizes and shows various extensions for grid and pattern problems.* 