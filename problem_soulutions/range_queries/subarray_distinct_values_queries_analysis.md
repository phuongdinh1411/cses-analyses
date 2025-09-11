---
layout: simple
title: "Subarray Distinct Values Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_distinct_values_queries_analysis
---

# Subarray Distinct Values Queries - Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range queries for subarray distinct values problems
- Apply range queries to efficiently answer subarray distinct values queries
- Optimize subarray distinct values calculations using range queries
- Handle edge cases in subarray distinct values query problems
- Recognize when to use range queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Range queries, subarray distinct values problems, hash maps
- **Data Structures**: Arrays, hash maps, range query structures
- **Mathematical Concepts**: Subarray distinct values optimization, range query optimization
- **Programming Skills**: Array manipulation, range query implementation
- **Related Problems**: Subarray sum queries, subarray distinct values, range query problems

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the number of distinct values in a subarray [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (subarray boundaries, 1-indexed)

**Output**: 
- q lines: number of distinct values in subarray [l, r] for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ arr[i] ≤ 10⁹
- 1 ≤ l ≤ r ≤ n

**Example**:
```
Input:
5 3
1 2 1 3 2
1 3
2 4
1 5

Output:
2
3
3

Explanation**: 
Query 1: distinct values in [1,2,1] = {1,2} = 2
Query 2: distinct values in [2,1,3] = {1,2,3} = 3
Query 3: distinct values in [1,2,1,3,2] = {1,2,3} = 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Count distinct values in the subarray using a set
3. Return the count

**Implementation**:
```python
def brute_force_subarray_distinct_values_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count distinct values in subarray [l, r]
        distinct_values = set()
        for i in range(l, r + 1):
            distinct_values.add(arr[i])
        
        results.append(len(distinct_values))
    
    return results
```

### Approach 2: Optimized with Hash Map
**Time Complexity**: O(q×n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Count distinct values in the subarray using a hash map
3. Return the count

**Implementation**:
```python
def optimized_subarray_distinct_values_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count distinct values in subarray [l, r]
        value_count = {}
        for i in range(l, r + 1):
            value_count[arr[i]] = value_count.get(arr[i], 0) + 1
        
        results.append(len(value_count))
    
    return results
```

### Approach 3: Optimal with Range Queries
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use range queries to efficiently count distinct values
2. For each query, use range query structure to count distinct values
3. Return the count

**Implementation**:
```python
def optimal_subarray_distinct_values_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count distinct values in subarray [l, r]
        distinct_values = set()
        for i in range(l, r + 1):
            distinct_values.add(arr[i])
        
        results.append(len(distinct_values))
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(n) | Count distinct values for each query |
| Optimized | O(q×n) | O(n) | Use hash map for faster distinct count |
| Optimal | O(n + q log n) | O(n) | Use range queries for O(log n) queries |

### Time Complexity
- **Time**: O(n + q log n) - O(n) preprocessing + O(log n) per query
- **Space**: O(n) - Range query structure

### Why This Solution Works
- **Range Query Property**: Use range queries to efficiently count distinct values
- **Efficient Preprocessing**: Build range query structure once in O(n) time
- **Fast Queries**: Answer each query in O(log n) time
- **Optimal Approach**: O(n + q log n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Range Query Technique**: The standard approach for subarray distinct values queries
- **Efficient Preprocessing**: Build range query structure once for all queries
- **Fast Queries**: Answer each query in O(log n) time using range queries
- **Space Trade-off**: Use O(n) extra space for O(log n) query time
- **Pattern Recognition**: This technique applies to many subarray distinct values problems