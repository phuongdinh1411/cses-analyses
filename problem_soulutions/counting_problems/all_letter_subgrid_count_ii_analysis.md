---
layout: simple
title: "All Letter Subgrid Count II"
permalink: /problem_soulutions/counting_problems/all_letter_subgrid_count_ii_analysis
---


# All Letter Subgrid Count II

## 📋 Problem Description

Given a 2D grid of size n×m containing letters, count the number of subgrids of any size that contain all letters from 'A' to 'Z' (case insensitive).

This is a grid counting problem where we need to find all rectangular subgrids that contain all 26 letters of the alphabet. We can solve this by checking all possible rectangular subgrids and verifying if they contain all letters.

**Input**: 
- First line: two integers n and m (grid dimensions)
- Next n lines: m characters each (letters in the grid)

**Output**: 
- Print one integer: the number of subgrids of any size containing all letters A-Z

**Constraints**:
- 1 ≤ n,m ≤ 100
- Grid contains only letters A-Z and a-z

**Example**:
```
Input:
3 3
ABC
DEF
GHI

Output:
0
```

**Explanation**: 
In the 3×3 grid, there are no subgrids that contain all 26 letters A-Z. The grid only contains 9 different letters (A, B, C, D, E, F, G, H, I), which is less than the required 26 letters.

## Solution Progression

### Approach 1: Check All Possible Subgrids - O(n³ × m³ × 26)
**Description**: Check all possible subgrids of all sizes to count those that contain all letters A-Z.

```python
def all_letter_subgrid_count_all_sizes_naive(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid contains all letters
                letters = set()
                
                for di in range(k):
                    for dj in range(k):
                        letter = grid[i + di][j + dj].upper()
                        letters.add(letter)
                
                # Check if all 26 letters are present
                if len(letters) == 26:
                    count += 1
    
    return count
```

**Why this is inefficient**: We need to check all possible subgrid sizes, leading to O(n³ × m³ × 26) time complexity.

### Improvement 1: Optimized Letter Counting - O(n³ × m³)
**Description**: Optimize the letter counting process by using a boolean array instead of a set.

```python
def all_letter_subgrid_count_all_sizes_optimized(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid contains all letters
                letters = [False] * 26
                
                for di in range(k):
                    for dj in range(k):
                        letter = ord(grid[i + di][j + dj].upper()) - ord('A')
                        letters[letter] = True
                
                # Check if all 26 letters are present
                if all(letters):
                    count += 1
    
    return count
```

**Why this improvement works**: Using a boolean array instead of a set reduces the time complexity for checking if all letters are present.

## Final Optimal Solution

```python
n, m = map(int, input().split())

# Read the grid
grid = []
for _ in range(n):
    row = input().strip()
    grid.append(row)

def count_all_letter_subgrids_all_sizes(n, m, grid):
    count = 0
    
    # Try all possible subgrid sizes
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid contains all letters
                letters = [False] * 26
                
                for di in range(k):
                    for dj in range(k):
                        letter = ord(grid[i + di][j + dj].upper()) - ord('A')
                        letters[letter] = True
                
                # Check if all 26 letters are present
                if all(letters):
                    count += 1
    
    return count

result = count_all_letter_subgrids_all_sizes(n, m, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n³ × m³ × 26) | O(k²) | Use set to track letters |
| Optimized | O(n³ × m³) | O(26) | Use boolean array for letters |

## Key Insights for Other Problems

### 1. **All Size Letter Counting**
**Principle**: Iterate through all possible subgrid sizes and check letter composition.
**Applicable to**: Grid problems, letter problems, counting problems

### 2. **Boolean Array Optimization**
**Principle**: Use boolean arrays instead of sets for efficient letter tracking.
**Applicable to**: Character frequency problems, set problems, optimization problems

### 3. **Multi-size Grid Analysis**
**Principle**: Use nested loops to check subgrids of all possible sizes.
**Applicable to**: Grid problems, matrix problems, traversal algorithms

## Notable Techniques

### 1. **All Size Letter Checking**
```python
def check_all_size_letter_subgrids(n, m, grid):
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                if has_all_letters_in_subgrid(grid, i, j, k):
                    count += 1
    
    return count
```

### 2. **Letter Presence Check**
```python
def has_all_letters_in_subgrid(grid, start_i, start_j, k):
    letters = [False] * 26
    
    for di in range(k):
        for dj in range(k):
            letter = ord(grid[start_i + di][start_j + dj].upper()) - ord('A')
            letters[letter] = True
    
    return all(letters)
```

### 3. **Multi-size Traversal Pattern**
```python
def traverse_all_letter_sizes(n, m, grid):
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check letter composition in subgrid of size k×k
                pass
```

## Problem-Solving Framework

1. **Identify problem type**: This is an all-size letter counting subgrid problem
2. **Choose approach**: Use nested loops to check subgrids of all sizes
3. **Implement checking**: Use boolean array to track letter presence efficiently
4. **Optimize**: Use boolean array instead of set for letter tracking
5. **Count results**: Increment counter for subgrids with all letters

---

*This analysis shows how to efficiently count subgrids of all sizes containing all letters using boolean array tracking.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Letter Subgrids**
**Problem**: Each letter has a weight. Find subgrids containing all letters with maximum total weight.
```python
def weighted_all_letter_subgrids(n, m, grid, weights):
    # weights[letter] = weight of the letter
    max_weight = 0
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                letters = [False] * 26
                total_weight = 0
                
                for di in range(k):
                    for dj in range(k):
                        letter = ord(grid[i + di][j + dj].upper()) - ord('A')
                        if not letters[letter]:
                            letters[letter] = True
                            total_weight += weights[letter]
                
                if all(letters):
                    count += 1
                    max_weight = max(max_weight, total_weight)
    
    return count, max_weight
```

#### **Variation 2: Minimum Size Constraint**
**Problem**: Find subgrids containing all letters with minimum size k.
```python
def min_size_all_letter_subgrids(n, m, grid, min_size):
    count = 0
    
    for k in range(min_size, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                letters = [False] * 26
                
                for di in range(k):
                    for dj in range(k):
                        letter = ord(grid[i + di][j + dj].upper()) - ord('A')
                        letters[letter] = True
                
                if all(letters):
                    count += 1
    
    return count
```

#### **Variation 3: Exact Letter Count**
**Problem**: Find subgrids containing exactly k different letters (not necessarily all 26).
```python
def exact_letter_count_subgrids(n, m, grid, k):
    count = 0
    
    for size in range(1, min(n, m) + 1):
        for i in range(n - size + 1):
            for j in range(m - size + 1):
                letters = set()
                
                for di in range(size):
                    for dj in range(size):
                        letter = grid[i + di][j + dj].upper()
                        letters.add(letter)
                
                if len(letters) == k:
                    count += 1
    
    return count
```

#### **Variation 4: Circular Grid**
**Problem**: Handle a circular grid where edges wrap around.
```python
def circular_all_letter_subgrids(n, m, grid):
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n):
            for j in range(m):
                letters = [False] * 26
                
                for di in range(k):
                    for dj in range(k):
                        # Handle circular wrapping
                        ni = (i + di) % n
                        nj = (j + dj) % m
                        letter = ord(grid[ni][nj].upper()) - ord('A')
                        letters[letter] = True
                
                if all(letters):
                    count += 1
    
    return count
```

#### **Variation 5: Dynamic Grid Updates**
**Problem**: Support dynamic updates to the grid and answer queries efficiently.
```python
class DynamicAllLetterCounter:
    def __init__(self, n, m, grid):
        self.n = n
        self.m = m
        self.grid = [row[:] for row in grid]
    
    def update_cell(self, i, j, new_letter):
        self.grid[i][j] = new_letter
    
    def count_all_letter_subgrids(self):
        count = 0
        
        for k in range(1, min(self.n, self.m) + 1):
            for i in range(self.n - k + 1):
                for j in range(self.m - k + 1):
                    letters = [False] * 26
                    
                    for di in range(k):
                        for dj in range(k):
                            letter = ord(self.grid[i + di][j + dj].upper()) - ord('A')
                            letters[letter] = True
                    
                    if all(letters):
                        count += 1
        
        return count
```

### 🔗 **Related Problems & Concepts**

#### **1. Grid Problems**
- **Grid Traversal**: Traverse grids efficiently
- **Subgrid Counting**: Count subgrids with properties
- **Grid Patterns**: Find patterns in grids
- **Grid Optimization**: Optimize grid operations

#### **2. Letter Problems**
- **Letter Frequency**: Count letter frequencies
- **Letter Patterns**: Find letter patterns
- **Letter Permutations**: Arrange letters
- **Letter Matching**: Match letter patterns

#### **3. Counting Problems**
- **Combinatorial Counting**: Count combinations
- **Inclusion-Exclusion**: Use inclusion-exclusion principle
- **Dynamic Counting**: Count with dynamic updates
- **Range Counting**: Count in ranges

#### **4. Matrix Problems**
- **Matrix Operations**: Perform matrix operations
- **Matrix Traversal**: Traverse matrices
- **Matrix Patterns**: Find matrix patterns
- **Matrix Optimization**: Optimize matrix algorithms

#### **5. String Problems**
- **String Matching**: Match string patterns
- **String Counting**: Count string occurrences
- **String Permutations**: Arrange strings
- **String Optimization**: Optimize string operations

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().strip()
        grid.append(row)
    
    result = count_all_letter_subgrids_all_sizes(n, m, grid)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute for different grid regions
def precompute_all_letter_counts(grid):
    n, m = len(grid), len(grid[0])
    # Precompute for all possible regions
    dp = {}
    
    for start_i in range(n):
        for start_j in range(m):
            for end_i in range(start_i, n):
                for end_j in range(start_j, m):
                    region = [grid[i][start_j:end_j+1] for i in range(start_i, end_i+1)]
                    count = count_all_letter_subgrids_all_sizes(len(region), len(region[0]), region)
                    dp[(start_i, start_j, end_i, end_j)] = count
    
    return dp

# Answer range queries efficiently
def range_query(dp, start_i, start_j, end_i, end_j):
    return dp.get((start_i, start_j, end_i, end_j), 0)
```

#### **3. Interactive Problems**
```python
# Interactive grid analyzer
def interactive_grid_analyzer():
    n = int(input("Enter grid height: "))
    m = int(input("Enter grid width: "))
    grid = []
    
    print("Enter grid rows:")
    for i in range(n):
        row = input(f"Row {i+1}: ").strip()
        grid.append(row)
    
    print("Grid:", grid)
    
    while True:
        query = input("Enter query (count/weighted/min_size/exact/circular/exit): ")
        if query == "exit":
            break
        
        if query == "count":
            result = count_all_letter_subgrids_all_sizes(n, m, grid)
            print(f"All letter subgrids: {result}")
        elif query == "weighted":
            weights = {}
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                weight = int(input(f"Enter weight for {letter}: "))
                weights[letter] = weight
            count, max_weight = weighted_all_letter_subgrids(n, m, grid, weights)
            print(f"Count: {count}, Max 
weight: {max_weight}")
        elif query == "min_size":
            min_size = int(input("Enter minimum size: "))
            result = min_size_all_letter_subgrids(n, m, grid, min_size)
            print(f"Subgrids with min size {min_size}: {result}")
        elif query == "exact":
            k = int(input("Enter exact letter count: "))
            result = exact_letter_count_subgrids(n, m, grid, k)
            print(f"Subgrids with exactly {k} letters: {result}")
        elif query == "circular":
            result = circular_all_letter_subgrids(n, m, grid)
            print(f"Circular all letter subgrids: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Grid Combinations**: Count grid combinations
- **Letter Arrangements**: Arrange letters in grids
- **Subgrid Partitions**: Partition grids into subgrids
- **Inclusion-Exclusion**: Count using inclusion-exclusion

#### **2. Number Theory**
- **Grid Patterns**: Mathematical patterns in grids
- **Letter Sequences**: Sequences of letters
- **Modular Arithmetic**: Grid operations with modular arithmetic
- **Number Sequences**: Sequences in grid counting

#### **3. Optimization Theory**
- **Grid Optimization**: Optimize grid operations
- **Letter Optimization**: Optimize letter counting
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Grid Traversal**: Efficient grid traversal algorithms
- **Letter Counting**: Letter frequency counting algorithms
## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n² × m² × 26) for checking all rectangular subgrids
- **Space Complexity**: O(26) for storing letter frequencies
- **Why it works**: We iterate through all possible rectangular subgrids and check if they contain all 26 letters

### Key Implementation Points
- Iterate through all possible rectangular subgrids
- Use a set or array to track which letters are present
- Check if all 26 letters are present in each subgrid
- Handle case insensitivity by converting to uppercase

## 🎯 Key Insights

### Important Concepts and Patterns
- **Grid Traversal**: Systematic way to check all rectangular subgrids
- **Letter Frequency**: Efficient way to track which letters are present
- **Subgrid Counting**: Counting patterns in 2D grids
- **Character Set Operations**: Working with sets of characters

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. All Letter Subgrid Count with Size Constraints**
```python
def all_letter_subgrid_count_with_size_constraints(n, m, grid, size_constraints):
    # Count subgrids with all letters and size constraints
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
                # Check if this k×k subgrid contains all letters
                letters = set()
                for row in range(i, i + k):
                    for col in range(j, j + k):
                        letters.add(grid[row][col].upper())
                
                if len(letters) == 26:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
size_constraints = {"min_size": 2, "max_size": 3, "allowed_sizes": [2, 3]}
result = all_letter_subgrid_count_with_size_constraints(n, m, grid, size_constraints)
print(f"Size-constrained all-letter subgrid count: {result}")
```

#### **2. All Letter Subgrid Count with Letter Constraints**
```python
def all_letter_subgrid_count_with_letter_constraints(n, m, grid, letter_constraints):
    # Count subgrids with all letters and letter constraints
    count = 0
    
    for k in range(1, min(n, m) + 1):
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid contains all letters
                letters = set()
                for row in range(i, i + k):
                    for col in range(j, j + k):
                        letters.add(grid[row][col].upper())
                
                # Check letter constraints
                if letter_constraints.get("required_letters"):
                    if not all(letter in letters for letter in letter_constraints["required_letters"]):
                        continue
                if letter_constraints.get("forbidden_letters"):
                    if any(letter in letters for letter in letter_constraints["forbidden_letters"]):
                        continue
                
                if len(letters) == 26:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
letter_constraints = {"required_letters": ["A", "B"], "forbidden_letters": []}
result = all_letter_subgrid_count_with_letter_constraints(n, m, grid, letter_constraints)
print(f"Letter-constrained all-letter subgrid count: {result}")
```

#### **3. All Letter Subgrid Count with Position Constraints**
```python
def all_letter_subgrid_count_with_position_constraints(n, m, grid, position_constraints):
    # Count subgrids with all letters and position constraints
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
                
                # Check if this k×k subgrid contains all letters
                letters = set()
                for row in range(i, i + k):
                    for col in range(j, j + k):
                        letters.add(grid[row][col].upper())
                
                if len(letters) == 26:
                    count += 1
    
    return count

# Example usage
n, m = 3, 3
grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
position_constraints = {"min_row": 0, "max_row": 2, "min_col": 0, "max_col": 2}
result = all_letter_subgrid_count_with_position_constraints(n, m, grid, position_constraints)
print(f"Position-constrained all-letter subgrid count: {result}")
```

#### **4. All Letter Subgrid Count with Statistics**
```python
def all_letter_subgrid_count_with_statistics(n, m, grid):
    # Count subgrids with all letters and provide statistics
    count = 0
    size_counts = {}
    positions = []
    
    for k in range(1, min(n, m) + 1):
        size_counts[k] = 0
        
        for i in range(n - k + 1):
            for j in range(m - k + 1):
                # Check if this k×k subgrid contains all letters
                letters = set()
                for row in range(i, i + k):
                    for col in range(j, j + k):
                        letters.add(grid[row][col].upper())
                
                if len(letters) == 26:
                    count += 1
                    size_counts[k] += 1
                    positions.append((i, j, k))
    
    statistics = {
        "total_count": count,
        "size_distribution": size_counts,
        "positions": positions,
        "has_all_letters": count > 0
    }
    
    return count, statistics

# Example usage
n, m = 3, 3
grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
count, stats = all_letter_subgrid_count_with_statistics(n, m, grid)
print(f"All-letter subgrid count: {count}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Grid Algorithms**: Grid traversal, Grid counting
- **String Algorithms**: Character counting, String analysis
- **Subgrid Problems**: Subgrid analysis, Subgrid optimization
- **Counting Problems**: Subset counting, Path counting

## 📚 Learning Points

### Key Takeaways
- **Grid traversal** is essential for checking all possible subgrids
- **Character set operations** are efficient for tracking letter presence
- **Subgrid counting** is a fundamental grid analysis technique
- **Case insensitivity** should be handled consistently

---

*This analysis demonstrates efficient all-letter subgrid counting techniques and shows various extensions for grid and letter problems.* 