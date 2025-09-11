---
layout: simple
title: "Hotel Queries - 2D Range Queries"
permalink: /problem_soulutions/range_queries/hotel_queries_analysis
---

# Hotel Queries - 2D Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement 2D range queries for hotel problems
- Apply 2D range queries to efficiently answer hotel queries
- Optimize hotel query calculations using 2D range queries
- Handle edge cases in hotel query problems
- Recognize when to use 2D range queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2D range queries, hotel problems, 2D data structures
- **Data Structures**: 2D arrays, 2D range query structures
- **Mathematical Concepts**: 2D range query optimization, hotel optimization
- **Programming Skills**: 2D array manipulation, 2D range query implementation
- **Related Problems**: Forest queries, 2D range query problems, hotel problems

## 📋 Problem Description

Given a 2D grid representing hotel rooms and multiple queries, each query asks for the number of available rooms in a 2D range [x1, y1] to [x2, y2]. The grid is static (no updates).

**Input**: 
- First line: n (grid size) and q (number of queries)
- Next n lines: n integers each (room availability: 1 = available, 0 = occupied)
- Next q lines: x1 y1 x2 y2 (2D range boundaries, 1-indexed)

**Output**: 
- q lines: number of available rooms in 2D range [x1, y1] to [x2, y2] for each query

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ q ≤ 2×10⁵
- 0 ≤ grid[i][j] ≤ 1
- 1 ≤ x1 ≤ x2 ≤ n, 1 ≤ y1 ≤ y2 ≤ n

**Example**:
```
Input:
3 2
1 0 1
0 1 0
1 1 1
1 1 2 2
2 2 3 3

Output:
2
3

Explanation**: 
Query 1: available rooms in [1,0; 0,1] = 1+0+0+1 = 2
Query 2: available rooms in [1,0; 1,1] = 1+0+1+1 = 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n²)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the 2D range [x1, y1] to [x2, y2]
2. Count available rooms in the 2D range
3. Return the count

**Implementation**:
```python
def brute_force_hotel_queries(grid, queries):
    n = len(grid)
    results = []
    
    for x1, y1, x2, y2 in queries:
        # Convert to 0-indexed
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1
        
        # Count available rooms in 2D range [x1, y1] to [x2, y2]
        count = 0
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                if grid[i][j] == 1:
                    count += 1
        
        results.append(count)
    
    return results
```

### Approach 2: Optimized with 2D Prefix Sums
**Time Complexity**: O(n² + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Precompute 2D prefix sum array where prefix[i][j] = count of available rooms from (0,0) to (i,j)
2. For each query, calculate count using 2D prefix sums
3. Return the count

**Implementation**:
```python
def optimized_hotel_queries(grid, queries):
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
        # Calculate count using 2D prefix sums
        count = (prefix[x2][y2] - 
                prefix[x1 - 1][y2] - 
                prefix[x2][y1 - 1] + 
                prefix[x1 - 1][y1 - 1])
        results.append(count)
    
    return results
```

### Approach 3: Optimal with 2D Prefix Sums
**Time Complexity**: O(n² + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Precompute 2D prefix sum array where prefix[i][j] = count of available rooms from (0,0) to (i,j)
2. For each query, calculate count using 2D prefix sums
3. Return the count

**Implementation**:
```python
def optimal_hotel_queries(grid, queries):
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
        # Calculate count using 2D prefix sums
        count = (prefix[x2][y2] - 
                prefix[x1 - 1][y2] - 
                prefix[x2][y1 - 1] + 
                prefix[x1 - 1][y1 - 1])
        results.append(count)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n²) | O(1) | Count available rooms for each query |
| Optimized | O(n² + q) | O(n²) | Use 2D prefix sums for O(1) queries |
| Optimal | O(n² + q) | O(n²) | Use 2D prefix sums for O(1) queries |

### Time Complexity
- **Time**: O(n² + q) - O(n²) preprocessing + O(1) per query
- **Space**: O(n²) - 2D prefix sum array

### Why This Solution Works
- **2D Prefix Sum Property**: prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1] gives count of available rooms in 2D range
- **Efficient Preprocessing**: Calculate 2D prefix sums once in O(n²) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n² + q) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **2D Prefix Sum Technique**: The standard approach for 2D range count queries
- **Efficient Preprocessing**: Calculate 2D prefix sums once for all queries
- **Fast Queries**: Answer each query in O(1) time using 2D prefix sums
- **Space Trade-off**: Use O(n²) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many 2D range count problems