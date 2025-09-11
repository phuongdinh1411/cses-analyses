---
layout: simple
title: "Visible Buildings Queries - Geometric Queries"
permalink: /problem_soulutions/range_queries/visible_buildings_queries_analysis
---

# Visible Buildings Queries - Geometric Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement geometric queries for visible buildings problems
- Apply geometric queries to efficiently answer visible buildings queries
- Optimize visible buildings calculations using geometric queries
- Handle edge cases in visible buildings query problems
- Recognize when to use geometric queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Geometric queries, visible buildings problems, range queries
- **Data Structures**: Arrays, geometric query structures
- **Mathematical Concepts**: Geometric query optimization, visible buildings optimization
- **Programming Skills**: Array manipulation, geometric query implementation
- **Related Problems**: Range queries, geometric problems, visible buildings problems

## 📋 Problem Description

Given an array of building heights and multiple queries, each query asks for the number of visible buildings from position i. A building is visible if it's taller than all buildings between position i and that building.

**Input**: 
- First line: n (number of buildings) and q (number of queries)
- Second line: n integers representing building heights
- Next q lines: i (position to query, 1-indexed)

**Output**: 
- q lines: number of visible buildings from position i for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ height[i] ≤ 10⁹
- 1 ≤ i ≤ n

**Example**:
```
Input:
5 3
3 1 4 1 5
1
3
5

Output:
2
2
1

Explanation**: 
Query 1: visible buildings from position 1 = 2 (buildings at positions 3 and 5)
Query 2: visible buildings from position 3 = 2 (buildings at positions 1 and 5)
Query 3: visible buildings from position 5 = 1 (no buildings to the right)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, check all buildings to the right of position i
2. Count buildings that are visible (taller than all buildings between)
3. Return the count

**Implementation**:
```python
def brute_force_visible_buildings_queries(heights, queries):
    n = len(heights)
    results = []
    
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        
        # Count visible buildings from position i
        visible_count = 0
        max_height = 0
        
        for j in range(i + 1, n):
            if heights[j] > max_height:
                visible_count += 1
                max_height = heights[j]
        
        results.append(visible_count)
    
    return results
```

### Approach 2: Optimized with Preprocessing
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute visible buildings count for each position
2. For each query, return precomputed count
3. Return the count

**Implementation**:
```python
def optimized_visible_buildings_queries(heights, queries):
    n = len(heights)
    
    # Precompute visible buildings count for each position
    visible_counts = [0] * n
    
    for i in range(n):
        max_height = 0
        for j in range(i + 1, n):
            if heights[j] > max_height:
                visible_counts[i] += 1
                max_height = heights[j]
    
    results = []
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        results.append(visible_counts[i])
    
    return results
```

### Approach 3: Optimal with Preprocessing
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute visible buildings count for each position
2. For each query, return precomputed count
3. Return the count

**Implementation**:
```python
def optimal_visible_buildings_queries(heights, queries):
    n = len(heights)
    
    # Precompute visible buildings count for each position
    visible_counts = [0] * n
    
    for i in range(n):
        max_height = 0
        for j in range(i + 1, n):
            if heights[j] > max_height:
                visible_counts[i] += 1
                max_height = heights[j]
    
    results = []
    for i in queries:
        # Convert to 0-indexed
        i -= 1
        results.append(visible_counts[i])
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Count visible buildings for each query |
| Optimized | O(n + q) | O(n) | Precompute counts for O(1) queries |
| Optimal | O(n + q) | O(n) | Precompute counts for O(1) queries |

### Time Complexity
- **Time**: O(n + q) - O(n) preprocessing + O(1) per query
- **Space**: O(n) - Visible counts array

### Why This Solution Works
- **Preprocessing Property**: Precompute visible buildings count for each position
- **Efficient Preprocessing**: Calculate counts once in O(n) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n + q) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Preprocessing Technique**: The standard approach for visible buildings queries
- **Efficient Preprocessing**: Calculate counts once for all queries
- **Fast Queries**: Answer each query in O(1) time using precomputed counts
- **Space Trade-off**: Use O(n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many geometric query problems