---
layout: simple
title: "Forest Queries - 2D Prefix Sums"
permalink: /problem_soulutions/range_queries/forest_queries_analysis
---

# Forest Queries - 2D Prefix Sums

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement 2D prefix sums for 2D range queries
- Apply 2D prefix sums to efficiently answer 2D range sum queries
- Optimize 2D range sum calculations using 2D prefix sums
- Handle edge cases in 2D prefix sum problems
- Recognize when to use 2D prefix sums vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2D prefix sums, 2D range queries, 2D data structures
- **Data Structures**: 2D arrays, 2D prefix sum arrays
- **Mathematical Concepts**: 2D range sum optimization, 2D cumulative sums
- **Programming Skills**: 2D array manipulation, 2D prefix sum implementation
- **Related Problems**: Static range sum queries, hotel queries, 2D range query problems

## 📋 Problem Description

Given a 2D grid of integers and multiple queries, each query asks for the sum of elements in a 2D range [x1, y1] to [x2, y2]. The grid is static (no updates).

**Input**: 
- First line: n (grid size) and q (number of queries)
- Next n lines: n integers each (grid values)
- Next q lines: x1 y1 x2 y2 (2D range boundaries, 1-indexed)

**Output**: 
- q lines: sum of elements in 2D range [x1, y1] to [x2, y2] for each query

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ q ≤ 2×10⁵
- -10⁹ ≤ grid[i][j] ≤ 10⁹
- 1 ≤ x1 ≤ x2 ≤ n, 1 ≤ y1 ≤ y2 ≤ n

**Example**:
```
Input:
3 2
1 2 3
4 5 6
7 8 9
1 1 2 2
2 2 3 3

Output:
12
28

Explanation**: 
Query 1: sum of [1,2; 4,5] = 1+2+4+5 = 12
Query 2: sum of [5,6; 8,9] = 5+6+8+9 = 28
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n²)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the 2D range [x1, y1] to [x2, y2]
2. Sum all elements in the 2D range
3. Return the sum

**Implementation**:
```python
def brute_force_forest_queries(grid, queries):
    n = len(grid)
    results = []
    
    for x1, y1, x2, y2 in queries:
        # Convert to 0-indexed
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1
        
        # Calculate sum in 2D range [x1, y1] to [x2, y2]
        range_sum = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                range_sum += grid[i][j]
        
        results.append(range_sum)
    
    return results
```

### Approach 2: Optimized with 2D Prefix Sums
**Time Complexity**: O(n² + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Precompute 2D prefix sum array where prefix[i][j] = sum of elements from (0,0) to (i,j)
2. For each query, calculate sum using 2D prefix sums
3. Return the sum

**Implementation**:
```python
def optimized_forest_queries(grid, queries):
    n = len(grid)
    
    # Precompute 2D prefix sums
    prefix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            prefix[i + 1][j + 1] = (prefix[i][j + 1] + 
                                   prefix[i + 1][j] - 
                                   prefix[i][j] + 
                                   grid[i][j])
    
    results = []
    for x1, y1, x2, y2 in queries:
        # Calculate sum using 2D prefix sums
        range_sum = (prefix[x2][y2] - 
                    prefix[x1 - 1][y2] - 
                    prefix[x2][y1 - 1] + 
                    prefix[x1 - 1][y1 - 1])
        results.append(range_sum)
    
    return results
```

### Approach 3: Optimal with 2D Prefix Sums
**Time Complexity**: O(n² + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Precompute 2D prefix sum array where prefix[i][j] = sum of elements from (0,0) to (i,j)
2. For each query, calculate sum using 2D prefix sums
3. Return the sum

**Implementation**:
```python
def optimal_forest_queries(grid, queries):
    n = len(grid)
    
    # Precompute 2D prefix sums
    prefix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            prefix[i + 1][j + 1] = (prefix[i][j + 1] + 
                                   prefix[i + 1][j] - 
                                   prefix[i][j] + 
                                   grid[i][j])
    
    results = []
    for x1, y1, x2, y2 in queries:
        # Calculate sum using 2D prefix sums
        range_sum = (prefix[x2][y2] - 
                    prefix[x1 - 1][y2] - 
                    prefix[x2][y1 - 1] + 
                    prefix[x1 - 1][y1 - 1])
        results.append(range_sum)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n²) | O(1) | Calculate sum for each query |
| Optimized | O(n² + q) | O(n²) | Use 2D prefix sums for O(1) queries |
| Optimal | O(n² + q) | O(n²) | Use 2D prefix sums for O(1) queries |

### Time Complexity
- **Time**: O(n² + q) - O(n²) preprocessing + O(1) per query
- **Space**: O(n²) - 2D prefix sum array

### Why This Solution Works
- **2D Prefix Sum Property**: prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1] gives sum of 2D range
- **Efficient Preprocessing**: Calculate 2D prefix sums once in O(n²) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n² + q) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **2D Prefix Sum Technique**: The standard approach for 2D range sum queries
- **Efficient Preprocessing**: Calculate 2D prefix sums once for all queries
- **Fast Queries**: Answer each query in O(1) time using 2D prefix sums
- **Space Trade-off**: Use O(n²) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many 2D range query problems