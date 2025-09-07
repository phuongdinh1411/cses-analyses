---
layout: simple
title: "Filled Subgrid Count II"
permalink: /problem_soulutions/counting_problems/filled_subgrid_count_ii_analysis
---


# Filled Subgrid Count II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand advanced subgrid analysis for variable-sized rectangular subgrids
- Apply efficient algorithms for counting uniform subgrids of any size
- Implement optimized subgrid counting using advanced sliding window techniques
- Optimize subgrid counting using mathematical formulas and advanced pattern analysis
- Handle edge cases in advanced subgrid counting (large grids, complex uniformity patterns)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Advanced subgrid algorithms, sliding window, pattern analysis, grid algorithms
- **Data Structures**: 2D arrays, sliding window data structures, advanced pattern matching structures
- **Mathematical Concepts**: Grid theory, pattern analysis, combinatorics, advanced uniformity properties
- **Programming Skills**: 2D array manipulation, advanced sliding window implementation, pattern checking
- **Related Problems**: Filled Subgrid Count I (basic version), All Letter Subgrid Count I (subgrid analysis), Forest Queries (grid queries)

## 📋 Problem Description

Given a 2D grid of size n×m, count the number of filled subgrids of any size. A subgrid is filled if all cells in it contain the same value.

This is a grid counting problem where we need to find all rectangular subgrids that are filled (all cells have the same value). We can solve this by checking all possible rectangular subgrids and verifying if they are filled.

**Input**: 
- First line: two integers n and m (grid dimensions)
- Next n lines: m integers each (grid values)

**Output**: 
- Print one integer: the number of filled subgrids of any size

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
14
```

**Explanation**: 
In the 3×3 grid, there are 14 filled subgrids:
- 9 single cells (1×1 subgrids)
- 3 filled 2×1 subgrids in the first two rows
- 1 filled 3×1 subgrid in the third row
- 1 filled 1×3 subgrid in the third column

### 📊 Visual Example

**Input Grid:**
```
   0   1   2
0 [1] [1] [2]
1 [1] [1] [2]
2 [3] [3] [3]
```

**All Possible Filled Subgrids:**
```
Subgrid 1: 1×1 at (0,0)
┌─────────────────────────────────────┐
│ [1]                                │
│ Values: 1                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 2: 1×1 at (0,1)
┌─────────────────────────────────────┐
│ [1]                                │
│ Values: 1                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 3: 1×1 at (0,2)
┌─────────────────────────────────────┐
│ [2]                                │
│ Values: 2                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 4: 1×1 at (1,0)
┌─────────────────────────────────────┐
│ [1]                                │
│ Values: 1                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 5: 1×1 at (1,1)
┌─────────────────────────────────────┐
│ [1]                                │
│ Values: 1                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 6: 1×1 at (1,2)
┌─────────────────────────────────────┐
│ [2]                                │
│ Values: 2                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 7: 1×1 at (2,0)
┌─────────────────────────────────────┐
│ [3]                                │
│ Values: 3                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 8: 1×1 at (2,1)
┌─────────────────────────────────────┐
│ [3]                                │
│ Values: 3                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 9: 1×1 at (2,2)
┌─────────────────────────────────────┐
│ [3]                                │
│ Values: 3                          │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 10: 2×1 at (0,0) to (1,0)
┌─────────────────────────────────────┐
│ [1]                                │
│ [1]                                │
│ Values: 1, 1                       │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 11: 2×1 at (0,1) to (1,1)
┌─────────────────────────────────────┐
│ [1]                                │
│ [1]                                │
│ Values: 1, 1                       │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 12: 2×1 at (0,2) to (1,2)
┌─────────────────────────────────────┐
│ [2]                                │
│ [2]                                │
│ Values: 2, 2                       │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 13: 3×1 at (2,0) to (2,2)
┌─────────────────────────────────────┐
│ [3] [3] [3]                        │
│ Values: 3, 3, 3                    │
│ All values same: ✓                 │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘

Subgrid 14: 1×3 at (0,2) to (2,2)
┌─────────────────────────────────────┐
│ [2]                                │
│ [2]                                │
│ [3]                                │
│ Values: 2, 2, 3                    │
│ All values same: ✗                 │
│ Not filled subgrid ✗               │
└─────────────────────────────────────┘
```

**Filled Subgrid Analysis:**
```
For a subgrid to be filled:
┌─────────────────────────────────────┐
│ - All cells must have the same value│
│ - No variation in cell values       │
│ - Uniform throughout the subgrid    │
└─────────────────────────────────────┘

Example with 2×1 subgrid from (0,0) to (1,0):
┌─────────────────────────────────────┐
│ [1]                                │
│ [1]                                │
│                                     │
│ Cell values:                        │
│ - (0,0): 1                         │
│ - (1,0): 1                         │
│ All values: 1 ✓                    │
└─────────────────────────────────────┘
```

**Algorithm Flowchart:**
```
┌─────────────────────────────────────┐
│ Start: Read grid                   │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ For each possible subgrid:         │
│   Extract all cell values          │
│   Check if all values are same     │
│   If yes: count++                  │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return total count                  │
└─────────────────────────────────────┘
```

**Key Insight Visualization:**
```
For any subgrid:
┌─────────────────────────────────────┐
│ - Extract all cell values           │
│ - Check if all values are equal     │
│ - If yes, subgrid is filled         │
└─────────────────────────────────────┘

Example with 3×1 subgrid:
┌─────────────────────────────────────┐
│ [3] [3] [3]                        │
│                                     │
│ All values: 3 ✓                    │
│ Filled subgrid ✓                   │
└─────────────────────────────────────┘
```

**Optimized Approach:**
```
Instead of checking all subgrids, we can:
1. Use sliding window technique
2. Maintain value information
3. Update values when moving the window
4. Check if all values are equal

Time complexity: O(n³×m³) → O(n²×m²)
```

**Sliding Window Technique:**
```
For each row, slide a window of varying sizes:
┌─────────────────────────────────────┐
│ Row 0: [1] → [1,1] → [1,1,2]      │
│ Row 1: [1] → [1,1] → [1,1,2]      │
│ Row 2: [3] → [3,3] → [3,3,3]      │
│                                     │
│ For each window position:          │
│   Update cell values               │
│   Check if all values same         │
└─────────────────────────────────────┘
```

**Value Tracking:**
```
For each subgrid:
┌─────────────────────────────────────┐
│ Initialize values:                  │
│ values = []                        │
│                                     │
│ For each cell in subgrid:          │
│   value = grid[i][j]              │
│   values.append(value)             │
│                                     │
│ Check if all values equal          │
└─────────────────────────────────────┘
```

## Solution Progression

### Approach 1: Check All Possible Subgrids - O(n³ × m³)
**Description**: Check all possible subgrids of all sizes to count those that are filled.

```python
def filled_subgrid_count_all_sizes_naive(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid is filled
                first_value = grid[i][j]
                is_filled = True
                
                for di in range(k):
                    for dj in range(k):
                        if grid[i + di][j + dj] != first_value:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
    
    return count
```

**Why this is inefficient**: We need to check all possible subgrid sizes, leading to O(n³ × m³) time complexity.

### Improvement 1: Optimized Checking with Early Termination - O(n³ × m³)
**Description**: Optimize the checking process with early termination when a mismatch is found.

```python
def filled_subgrid_count_all_sizes_optimized(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid is filled
                first_value = grid[i][j]
                is_filled = True
                
                # Check each cell in the subgrid
                for di in range(k):
                    for dj in range(k):
                        if grid[i + di][j + dj] != first_value:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
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

def count_all_filled_subgrids(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid is filled
                first_value = grid[i][j]
                is_filled = True
                
                # Check each cell in the subgrid
                for di in range(k):
                    for dj in range(k):
                        if grid[i + di][j + dj] != first_value:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
    
    return count

result = count_all_filled_subgrids(n, m, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n³ × m³) | O(1) | Check all subgrids of all sizes |
| Optimized | O(n³ × m³) | O(1) | Early termination on mismatch |

## Key Insights for Other Problems

### 1. **All Size Subgrid Counting**
**Principle**: Iterate through all possible subgrid sizes and check each one.
**Applicable to**: Grid problems, subgrid problems, counting problems

### 2. **Early Termination Optimization**
**Principle**: Stop checking as soon as a condition is violated to improve performance.
**Applicable to**: Optimization problems, search problems, validation problems

### 3. **Multi-size Grid Traversal**
**Principle**: Use nested loops to check subgrids of all possible sizes.
**Applicable to**: Grid problems, matrix problems, traversal algorithms

## Notable Techniques

### 1. **All Size Subgrid Checking**
```python
def check_all_size_subgrids(n, m, grid):
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                if is_filled_subgrid(grid, i, j, k):
                    count += 1
    
    return count
```

### 2. **Filled Subgrid Check**
```python
def is_filled_subgrid(grid, start_i, start_j, k):
    first_value = grid[start_i][start_j]
    
    for di in range(k):
        for dj in range(k):
            if grid[start_i + di][start_j + dj] != first_value:
                return False
    
    return True
```

### 3. **Multi-size Traversal Pattern**
```python
def traverse_all_sizes(n, m):
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Process subgrid of size k×k starting at (i, j)
                pass
```

## Problem-Solving Framework

1. **Identify problem type**: This is an all-size subgrid counting problem
2. **Choose approach**: Use nested loops to check subgrids of all sizes
3. **Implement checking**: Check if all cells in subgrid have the same value
4. **Optimize**: Use early termination when mismatch is found
5. **Count results**: Increment counter for each filled subgrid

---

*This analysis shows how to efficiently count filled subgrids of all sizes using systematic grid traversal and early termination.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Filled Subgrids All Sizes**
**Problem**: Each cell has a weight. Find filled subgrids of all sizes with maximum total weight.
```python
def weighted_filled_subgrids_all_sizes(n, m, grid, weights):
    # weights[i][j] = weight of cell grid[i][j]
    max_weight = 0
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                is_filled = True
                total_weight = 0
                
                for di in range(k):
                    for dj in range(k):
                        if grid[i + di][j + dj] == 0:
                            is_filled = False
                            break
                        total_weight += weights[i + di][j + dj]
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
                    max_weight = max(max_weight, total_weight)
    
    return count, max_weight
```

#### **Variation 2: Minimum Size Constraint**
**Problem**: Find filled subgrids with minimum size k.
```python
def min_size_filled_subgrids(n, m, grid, min_size):
    count = 0
    
    for k in range(min_size, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                is_filled = True
                
                for di in range(k):
                    for dj in range(k):
                        if grid[i + di][j + dj] == 0:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
    
    return count
```

#### **Variation 3: Different Fill Values All Sizes**
**Problem**: Find subgrids of all sizes filled with a specific value v.
```python
def value_filled_subgrids_all_sizes(n, m, grid, target_value):
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                is_filled = True
                
                for di in range(k):
                    for dj in range(k):
                        if grid[i + di][j + dj] != target_value:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
    
    return count
```

#### **Variation 4: Circular Filled Subgrids All Sizes**
**Problem**: Handle a circular grid where subgrids of all sizes wrap around.
```python
def circular_filled_subgrids_all_sizes(n, m, grid):
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n):
            for j in range(m):
                is_filled = True
                
                for di in range(k):
                    for dj in range(k):
                        ni = (i + di) % n
                        nj = (j + dj) % m
                        if grid[ni][nj] == 0:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
    
    return count
```

#### **Variation 5: Dynamic Filled Subgrid Updates All Sizes**
**Problem**: Support dynamic updates to the grid and answer filled subgrid queries efficiently for all sizes.
```python
class DynamicFilledSubgridCounterAllSizes:
    def __init__(self, n, m, grid):
        self.n = n
        self.m = m
        self.grid = [row[:] for row in grid]
    
    def update_cell(self, i, j, new_value):
        self.grid[i][j] = new_value
    
    def count_filled_subgrids_all_sizes(self):
        count = 0
        
        for k in range(1, min(self.n, self.m) + 1):
            for i in range(self.n - k + 1):
                for j in range(self.m - k + 1):
                    is_filled = True
                    
                    for di in range(k):
                        for dj in range(k):
                            if self.grid[i + di][j + dj] == 0:
                                is_filled = False
                                break
                        if not is_filled:
                            break
                    
                    if is_filled:
                        count += 1
        
        return count
```

### 🔗 **Related Problems & Concepts**

#### **1. Grid Problems**
- **Grid Traversal**: Traverse grids efficiently
- **Subgrid Counting**: Count subgrids with properties
- **Grid Patterns**: Find patterns in grids
- **Grid Optimization**: Optimize grid operations

#### **2. Fill Problems**
- **Fill Detection**: Detect filled regions in grids
- **Fill Patterns**: Find fill patterns
- **Fill Optimization**: Optimize fill operations
- **Fill Analysis**: Analyze fill properties

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
    
    result = count_filled_subgrids_all_sizes(n, m, grid)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute filled subgrid counts for different grid regions
def precompute_filled_counts_all_sizes(grid):
    n, m = len(grid), len(grid[0])
    # Precompute for all possible regions
    filled_counts = {}
    
    for start_i in range(n):
        for start_j in range(m):
            for end_i in range(start_i, n):
                for end_j in range(start_j, m):
                    region = [grid[i][start_j:end_j+1] for i in range(start_i, end_i+1)]
                    count = count_filled_subgrids_all_sizes(len(region), len(region[0]), region)
                    filled_counts[(start_i, start_j, end_i, end_j)] = count
    
    return filled_counts

# Answer range queries efficiently
def range_query(filled_counts, start_i, start_j, end_i, end_j):
    return filled_counts.get((start_i, start_j, end_i, end_j), 0)
```

#### **3. Interactive Problems**
```python
# Interactive filled subgrid analyzer for all sizes
def interactive_filled_analyzer_all_sizes():
    n = int(input("Enter grid height: "))
    m = int(input("Enter grid width: "))
    grid = []
    
    print("Enter grid rows:")
    for i in range(n):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        grid.append(row)
    
    print("Grid:", grid)
    
    while True:
        query = input("Enter query (count/weighted/min_size/value/circular/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "count":
            result = count_filled_subgrids_all_sizes(n, m, grid)
            print(f"Filled subgrids of all sizes: {result}")
        elif query == "weighted":
            weights = []
            print("Enter weight matrix:")
            for i in range(n):
                row = list(map(int, input(f"Weight row {i+1}: ").split()))
                weights.append(row)
            count, max_weight = weighted_filled_subgrids_all_sizes(n, m, grid, weights)
            print(f"Count: {count}, Max 
weight: {max_weight}")
        elif query == "min_size":
            min_size = int(input("Enter minimum size: "))
            result = min_size_filled_subgrids(n, m, grid, min_size)
            print(f"Filled subgrids with min size {min_size}: {result}")
        elif query == "value":
            target_value = int(input("Enter target value: "))
            result = value_filled_subgrids_all_sizes(n, m, grid, target_value)
            print(f"Subgrids filled with {target_value}: {result}")
        elif query == "circular":
            result = circular_filled_subgrids_all_sizes(n, m, grid)
            print(f"Circular filled subgrids: {result}")
        elif query == "dynamic":
            counter = DynamicFilledSubgridCounterAllSizes(n, m, grid)
            print(f"Initial filled subgrids: {counter.count_filled_subgrids_all_sizes()}")
            
            while True:
                cmd = input("Enter command (update/count/back): ")
                if cmd == "back":
                    break
                elif cmd == "update":
                    i, j, value = map(int, input("Enter i, j, value: ").split())
                    counter.update_cell(i, j, value)
                    print("Cell updated")
                elif cmd == "count":
                    result = counter.count_filled_subgrids_all_sizes()
                    print(f"Filled subgrids: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Grid Combinations**: Count grid combinations
- **Fill Arrangements**: Arrange fills in grids
- **Pattern Partitions**: Partition grids into patterns
- **Inclusion-Exclusion**: Count using inclusion-exclusion

#### **2. Number Theory**
- **Grid Patterns**: Mathematical patterns in grids
- **Fill Sequences**: Sequences of fill values
- **Modular Arithmetic**: Grid operations with modular arithmetic
- **Number Sequences**: Sequences in grid counting

#### **3. Optimization Theory**
- **Grid Optimization**: Optimize grid operations
- **Fill Optimization**: Optimize fill checking
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n² × m²) for checking all rectangular subgrids
- **Space Complexity**: O(1) for storing the count
- **Why it works**: We iterate through all possible rectangular subgrids and check if they are filled

### Key Implementation Points
- Iterate through all possible rectangular subgrids
- Check if all cells in each subgrid have the same value
- Handle different subgrid sizes efficiently
- Optimize by early termination when a subgrid is not filled

## 🎯 Key Insights

### Important Concepts and Patterns
- **Grid Traversal**: Systematic way to check all rectangular subgrids
- **Fill Detection**: Efficient way to verify if a subgrid is filled
- **Subgrid Counting**: Counting patterns in 2D grids
- **Pattern Recognition**: Identifying filled patterns

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Filled Subgrid Count with Size Constraints**
```python
def filled_subgrid_count_with_size_constraints(n, m, grid, size_constraints):
    # Count filled subgrids with constraints on size
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
                # Check if this k×k subgrid is filled
                first_value = grid[i][j]
                is_filled = True
                
                for row in range(i, i + k):
                    for col in range(j, j + k):
                        if grid[row][col] != first_value:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [[1, 1, 2], [1, 1, 2], [3, 3, 3]]
size_constraints = {"min_size": 2, "max_size": 3, "allowed_sizes": [2, 3]}
result = filled_subgrid_count_with_size_constraints(n, m, grid, size_constraints)
print(f"Size-constrained filled subgrid count: {result}")
```

#### **2. Filled Subgrid Count with Value Constraints**
```python
def filled_subgrid_count_with_value_constraints(n, m, grid, value_constraints):
    # Count filled subgrids with constraints on values
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid is filled
                first_value = grid[i][j]
                
                # Check value constraints
                if value_constraints.get("min_value", 0) > first_value:
                    continue
                if value_constraints.get("max_value", float('inf')) < first_value:
                    continue
                if value_constraints.get("allowed_values") and first_value not in value_constraints["allowed_values"]:
                    continue
                
                is_filled = True
                for row in range(i, i + k):
                    for col in range(j, j + k):
                        if grid[row][col] != first_value:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [[1, 1, 2], [1, 1, 2], [3, 3, 3]]
value_constraints = {"min_value": 1, "max_value": 2, "allowed_values": [1, 2]}
result = filled_subgrid_count_with_value_constraints(n, m, grid, value_constraints)
print(f"Value-constrained filled subgrid count: {result}")
```

#### **3. Filled Subgrid Count with Position Constraints**
```python
def filled_subgrid_count_with_position_constraints(n, m, grid, position_constraints):
    # Count filled subgrids with constraints on position
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
                
                # Check if this k×k subgrid is filled
                first_value = grid[i][j]
                is_filled = True
                
                for row in range(i, i + k):
                    for col in range(j, j + k):
                        if grid[row][col] != first_value:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [[1, 1, 2], [1, 1, 2], [3, 3, 3]]
position_constraints = {"min_row": 0, "max_row": 2, "min_col": 0, "max_col": 2}
result = filled_subgrid_count_with_position_constraints(n, m, grid, position_constraints)
print(f"Position-constrained filled subgrid count: {result}")
```

#### **4. Filled Subgrid Count with Statistics**
```python
def filled_subgrid_count_with_statistics(n, m, grid):
    # Count filled subgrids and provide statistics
    count = 0
    size_counts = {}
    value_counts = {}
    positions = []
    
    for k in range(1, min(n, m) + 1):
        size_counts[k] = 0
        
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid is filled
                first_value = grid[i][j]
                is_filled = True
                
                for row in range(i, i + k):
                    for col in range(j, j + k):
                        if grid[row][col] != first_value:
                            is_filled = False
                            break
                    if not is_filled:
                        break
                
                if is_filled:
                    count += 1
                    size_counts[k] += 1
                    value_counts[first_value] = value_counts.get(first_value, 0) + 1
                    positions.append((i, j, k, first_value))
    
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
count, stats = filled_subgrid_count_with_statistics(n, m, grid)
print(f"Filled subgrid count: {count}")
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
- **Fill detection** can be optimized by checking values systematically
- **Subgrid counting** is a fundamental grid analysis technique
- **Pattern recognition** helps identify filled patterns in grids

---

*This analysis demonstrates efficient filled subgrid counting techniques for all sizes and shows various extensions for grid and pattern problems.* 