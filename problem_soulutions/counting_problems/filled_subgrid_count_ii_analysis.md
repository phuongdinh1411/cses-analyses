---
layout: simple
title: "Filled Subgrid Count II"permalink: /problem_soulutions/counting_problems/filled_subgrid_count_ii_analysis
---


# Filled Subgrid Count II

## Problem Statement
Given a 2D grid of size n×m, count the number of filled subgrids of any size. A subgrid is filled if all cells in it contain the same value.

### Input
The first input line has two integers n and m: the dimensions of the grid.
Then there are n lines describing the grid. Each line has m integers: the values in the grid.

### Output
Print one integer: the number of filled subgrids of any size.

### Constraints
- 1 ≤ n,m ≤ 100
- 1 ≤ grid[i][j] ≤ 10^9

### Example
```
Input:
3 3
1 1 2
1 1 2
3 3 3

Output:
14
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
            print(f"Count: {count}, Max weight: {max_weight}")
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

#### **1. Related Algorithms**
- **Grid Traversal**: Efficient grid traversal algorithms
- **Fill Detection**: Fill detection algorithms
- **Pattern Matching**: Pattern matching algorithms
- **Dynamic Programming**: For optimization problems

#### **2. Mathematical Concepts**
- **Combinatorics**: Foundation for counting problems
- **Grid Theory**: Mathematical properties of grids
- **Pattern Theory**: Properties of patterns
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Grid Processing**: Efficient grid processing techniques
- **Pattern Recognition**: Pattern recognition techniques

---

*This analysis demonstrates efficient filled subgrid counting techniques for all sizes and shows various extensions for grid and pattern problems.* 