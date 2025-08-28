---
layout: simple
title: "All Letter Subgrid Count I"
permalink: /problem_soulutions/counting_problems/all_letter_subgrid_count_i_analysis
---


# All Letter Subgrid Count I

## Problem Statement
Given a 2D grid of size n×m containing letters, count the number of subgrids of size k×k that contain all letters from 'A' to 'Z' (case insensitive).

### Input
The first input line has three integers n, m, and k: the dimensions of the grid and the size of subgrids to count.
Then there are n lines describing the grid. Each line has m characters: the letters in the grid.

### Output
Print one integer: the number of k×k subgrids containing all letters A-Z.

### Constraints
- 1 ≤ n,m ≤ 100
- 1 ≤ k ≤ min(n,m)
- Grid contains only letters A-Z and a-z

### Example
```
Input:
3 3 2
ABC
DEF
GHI

Output:
0
```

## Solution Progression

### Approach 1: Check All Subgrids - O(n × m × k² × 26)
**Description**: Check all possible k×k subgrids to count those that contain all letters A-Z.

```python
def all_letter_subgrid_count_naive(n, m, k, grid):
    count = 0
    
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

**Why this is inefficient**: For each subgrid, we need to check all k² cells and count unique letters, leading to O(n × m × k² × 26) time complexity.

### Improvement 1: Optimized Letter Counting - O(n × m × k²)
**Description**: Optimize the letter counting process by using a boolean array instead of a set.

```python
def all_letter_subgrid_count_optimized(n, m, k, grid):
    count = 0
    
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
n, m, k = map(int, input().split())

# Read the grid
grid = []
for _ in range(n):
    row = input().strip()
    grid.append(row)

def count_all_letter_subgrids(n, m, k, grid):
    count = 0
    
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

result = count_all_letter_subgrids(n, m, k, grid)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n × m × k² × 26) | O(k²) | Use set to track letters |
| Optimized | O(n × m × k²) | O(26) | Use boolean array for letters |

## Key Insights for Other Problems

### 1. **Letter Counting Problems**
**Principle**: Use boolean arrays or bit manipulation to efficiently track letter presence.
**Applicable to**: String problems, counting problems, character frequency problems

### 2. **Subgrid Letter Analysis**
**Principle**: Check all cells in a subgrid to determine letter composition.
**Applicable to**: Grid problems, subgrid problems, letter analysis problems

### 3. **Complete Set Checking**
**Principle**: Use efficient data structures to check if all required elements are present.
**Applicable to**: Set problems, completeness problems, validation problems

## Notable Techniques

### 1. **Letter Tracking with Boolean Array**
```python
def check_all_letters(grid, start_i, start_j, k):
    letters = [False] * 26
    
    for di in range(k):
        for dj in range(k):
            letter = ord(grid[start_i + di][start_j + dj].upper()) - ord('A')
            letters[letter] = True
    
    return all(letters)
```

### 2. **Letter Frequency Counting**
```python
def count_letters_in_subgrid(grid, start_i, start_j, k):
    letters = [0] * 26
    
    for di in range(k):
        for dj in range(k):
            letter = ord(grid[start_i + di][start_j + dj].upper()) - ord('A')
            letters[letter] += 1
    
    return letters
```

### 3. **Complete Set Check**
```python
def has_all_letters(letters_array):
    return all(letters_array)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a letter counting subgrid problem
2. **Choose approach**: Use boolean array to track letter presence efficiently
3. **Implement checking**: Check all cells in subgrid for letter composition
4. **Optimize**: Use boolean array instead of set for letter tracking
5. **Count results**: Increment counter for subgrids with all letters

---

*This analysis shows how to efficiently count subgrids containing all letters using boolean array tracking.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Letter Subgrids**
**Problem**: Each letter has a weight. Find k×k subgrids containing all letters with maximum total weight.
```python
def weighted_all_letter_subgrids(n, m, k, grid, weights):
    # weights[letter] = weight of the letter
    max_weight = 0
    count = 0
    
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

#### **Variation 2: Minimum Letter Frequency**
**Problem**: Find k×k subgrids where each letter appears at least f times.
```python
def min_frequency_all_letter_subgrids(n, m, k, grid, min_freq):
    count = 0
    
    for i in range(n - k + 1):
        for j in range(m - k + 1):
            letters = [0] * 26
            
            for di in range(k):
                for dj in range(k):
                    letter = ord(grid[i + di][j + dj].upper()) - ord('A')
                    letters[letter] += 1
            
            # Check if all letters appear at least min_freq times
            if all(freq >= min_freq for freq in letters):
                count += 1
    
    return count
```

#### **Variation 3: Exact Letter Count**
**Problem**: Find k×k subgrids containing exactly c different letters (not necessarily all 26).
```python
def exact_letter_count_subgrids(n, m, k, grid, c):
    count = 0
    
    for i in range(n - k + 1):
        for j in range(m - k + 1):
            letters = set()
            
            for di in range(k):
                for dj in range(k):
                    letter = grid[i + di][j + dj].upper()
                    letters.add(letter)
            
            if len(letters) == c:
                count += 1
    
    return count
```

#### **Variation 4: Circular Grid**
**Problem**: Handle a circular grid where edges wrap around for k×k subgrids.
```python
def circular_all_letter_subgrids(n, m, k, grid):
    count = 0
    
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
    def __init__(self, n, m, k, grid):
        self.n = n
        self.m = m
        self.k = k
        self.grid = [row[:] for row in grid]
    
    def update_cell(self, i, j, new_letter):
        self.grid[i][j] = new_letter
    
    def count_all_letter_subgrids(self):
        count = 0
        
        for i in range(self.n - self.k + 1):
            for j in range(self.m - self.k + 1):
                letters = [False] * 26
                
                for di in range(self.k):
                    for dj in range(self.k):
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
    n, m, k = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().strip()
        grid.append(row)
    
    result = count_all_letter_subgrids(n, m, k, grid)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute for different grid regions
def precompute_all_letter_counts(grid, k):
    n, m = len(grid), len(grid[0])
    # Precompute for all possible regions
    dp = {}
    
    for start_i in range(n - k + 1):
        for start_j in range(m - k + 1):
            region = [grid[i][start_j:start_j+k] for i in range(start_i, start_i+k)]
            count = count_all_letter_subgrids(k, k, k, region)
            dp[(start_i, start_j)] = count
    
    return dp

# Answer range queries efficiently
def range_query(dp, start_i, start_j):
    return dp.get((start_i, start_j), 0)
```

#### **3. Interactive Problems**
```python
# Interactive grid analyzer
def interactive_grid_analyzer():
    n = int(input("Enter grid height: "))
    m = int(input("Enter grid width: "))
    k = int(input("Enter subgrid size: "))
    grid = []
    
    print("Enter grid rows:")
    for i in range(n):
        row = input(f"Row {i+1}: ").strip()
        grid.append(row)
    
    print("Grid:", grid)
    
    while True:
        query = input("Enter query (count/weighted/min_freq/exact/circular/exit): ")
        if query == "exit":
            break
        
        if query == "count":
            result = count_all_letter_subgrids(n, m, k, grid)
            print(f"All letter subgrids: {result}")
        elif query == "weighted":
            weights = {}
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                weight = int(input(f"Enter weight for {letter}: "))
                weights[letter] = weight
            count, max_weight = weighted_all_letter_subgrids(n, m, k, grid, weights)
            print(f"Count: {count}, Max 
weight: {max_weight}")
        elif query == "min_freq":
            min_freq = int(input("Enter minimum frequency: "))
            result = min_frequency_all_letter_subgrids(n, m, k, grid, min_freq)
            print(f"Subgrids with min frequency {min_freq}: {result}")
        elif query == "exact":
            c = int(input("Enter exact letter count: "))
            result = exact_letter_count_subgrids(n, m, k, grid, c)
            print(f"Subgrids with exactly {c} letters: {result}")
        elif query == "circular":
            result = circular_all_letter_subgrids(n, m, k, grid)
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
- **Subgrid Algorithms**: Algorithms for subgrid operations
- **Dynamic Programming**: For optimization problems

#### **2. Mathematical Concepts**
- **Combinatorics**: Foundation for counting problems
- **Grid Theory**: Mathematical properties of grids
- **Letter Theory**: Properties of letter arrangements
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Grid Processing**: Efficient grid processing techniques
- **String Manipulation**: String and character processing

---

*This analysis demonstrates efficient letter subgrid counting techniques and shows various extensions for grid and letter problems.* 