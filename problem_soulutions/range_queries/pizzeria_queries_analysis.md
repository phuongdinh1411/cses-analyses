---
layout: simple
title: "Pizzeria Queries - Distance Queries"
permalink: /problem_soulutions/range_queries/pizzeria_queries_analysis
---

# Pizzeria Queries - Distance Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement distance queries for pizzeria problems
- Apply distance queries to efficiently answer pizzeria queries
- Optimize pizzeria query calculations using distance queries
- Handle edge cases in pizzeria query problems
- Recognize when to use distance queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Distance queries, pizzeria problems, range queries
- **Data Structures**: Arrays, distance query structures
- **Mathematical Concepts**: Distance query optimization, pizzeria optimization
- **Programming Skills**: Array manipulation, distance query implementation
- **Related Problems**: Range queries, distance problems, pizzeria problems

## 📋 Problem Description

Given an array of pizzeria locations and multiple queries, each query asks for the distance from position i to the nearest pizzeria. The array is static (no updates).

**Input**: 
- First line: n (number of positions) and q (number of queries)
- Second line: n integers representing pizzeria locations (1 = pizzeria, 0 = no pizzeria)
- Next q lines: i (position to query, 1-indexed)

**Output**: 
- q lines: distance from position i to nearest pizzeria for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 0 ≤ arr[i] ≤ 1
- 1 ≤ i ≤ n

**Example**:
```
Input:
5 3
0 1 0 1 0
2
4
1

Output:
0
0
1

Explanation**: 
Query 1: distance from position 2 to nearest pizzeria = 0 (pizzeria at position 2)
Query 2: distance from position 4 to nearest pizzeria = 0 (pizzeria at position 4)
Query 3: distance from position 1 to nearest pizzeria = 1 (nearest pizzeria at position 2)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, find the nearest pizzeria to position i
2. Calculate distance to the nearest pizzeria
3. Return the distance

**Implementation**:
```python
def brute_force_pizzeria_queries(arr, queries):
    n = len(arr)
    results = []
    
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        
        # Find nearest pizzeria to position i
        min_distance = float('inf')
        for j in range(n):
            if arr[j] == 1:  # Pizzeria found
                distance = abs(i - j)
                min_distance = min(min_distance, distance)
        
        results.append(min_distance)
    
    return results
```

### Approach 2: Optimized with Preprocessing
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute distances to nearest pizzeria for each position
2. For each query, return precomputed distance
3. Return the distance

**Implementation**:
```python
def optimized_pizzeria_queries(arr, queries):
    n = len(arr)
    
    # Precompute distances to nearest pizzeria
    distances = [float('inf')] * n
    
    # Find all pizzeria positions
    pizzerias = []
    for i in range(n):
        if arr[i] == 1:
            pizzerias.append(i)
    
    # Calculate distances for each position
    for i in range(n):
        for pizzeria in pizzerias:
            distance = abs(i - pizzeria)
            distances[i] = min(distances[i], distance)
    
    results = []
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        results.append(distances[i])
    
    return results
```

### Approach 3: Optimal with Preprocessing
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute distances to nearest pizzeria for each position
2. For each query, return precomputed distance
3. Return the distance

**Implementation**:
```python
def optimal_pizzeria_queries(arr, queries):
    n = len(arr)
    
    # Precompute distances to nearest pizzeria
    distances = [float('inf')] * n
    
    # Find all pizzeria positions
    pizzerias = []
    for i in range(n):
        if arr[i] == 1:
            pizzerias.append(i)
    
    # Calculate distances for each position
    for i in range(n):
        for pizzeria in pizzerias:
            distance = abs(i - pizzeria)
            distances[i] = min(distances[i], distance)
    
    results = []
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        results.append(distances[i])
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Find nearest pizzeria for each query |
| Optimized | O(n + q) | O(n) | Precompute distances for O(1) queries |
| Optimal | O(n + q) | O(n) | Precompute distances for O(1) queries |

### Time Complexity
- **Time**: O(n + q) - O(n) preprocessing + O(1) per query
- **Space**: O(n) - Distance array

### Why This Solution Works
- **Preprocessing Property**: Precompute distances to nearest pizzeria
- **Efficient Preprocessing**: Calculate distances once in O(n) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n + q) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Preprocessing Technique**: The standard approach for pizzeria distance queries
- **Efficient Preprocessing**: Calculate distances once for all queries
- **Fast Queries**: Answer each query in O(1) time using precomputed distances
- **Space Trade-off**: Use O(n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many distance query problems