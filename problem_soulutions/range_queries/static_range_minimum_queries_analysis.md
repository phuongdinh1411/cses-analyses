---
layout: simple
title: "Static Range Minimum Queries - Sparse Table"
permalink: /problem_soulutions/range_queries/static_range_minimum_queries_analysis
---

# Static Range Minimum Queries - Sparse Table

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement sparse table technique for range minimum queries
- Apply sparse table to efficiently answer static range minimum queries
- Optimize range minimum calculations using sparse table
- Handle edge cases in sparse table problems
- Recognize when to use sparse table vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sparse table, range minimum queries, static data structures
- **Data Structures**: Arrays, 2D arrays, sparse tables
- **Mathematical Concepts**: Range minimum optimization, binary representation
- **Programming Skills**: Array manipulation, sparse table implementation
- **Related Problems**: Static range sum queries, dynamic range minimum queries, range maximum queries

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the minimum element in a range [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (range boundaries, 1-indexed)

**Output**: 
- q lines: minimum element in range [l, r] for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- -10⁹ ≤ arr[i] ≤ 10⁹
- 1 ≤ l ≤ r ≤ n

**Example**:
```
Input:
5 3
1 2 3 4 5
1 3
2 4
1 5

Output:
1
2
1

Explanation**: 
Query 1: minimum of [1,2,3] = 1
Query 2: minimum of [2,3,4] = 2
Query 3: minimum of [1,2,3,4,5] = 1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the range [l, r]
2. Find minimum element in the range
3. Return the minimum

**Implementation**:
```python
def brute_force_static_range_minimum_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Find minimum in range [l, r]
        min_val = float('inf')
        for i in range(l, r + 1):
            min_val = min(min_val, arr[i])
        
        results.append(min_val)
    
    return results
```

### Approach 2: Optimized with Sparse Table
**Time Complexity**: O(n log n + q)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute sparse table where st[i][j] = minimum in range [i, i + 2^j - 1]
2. For each query, find the largest power of 2 that fits in the range
3. Use sparse table to find minimum in O(1) time
4. Return the minimum

**Implementation**:
```python
def optimized_static_range_minimum_queries(arr, queries):
    n = len(arr)
    
    # Precompute sparse table
    log_n = 0
    while (1 << log_n) <= n:
        log_n += 1
    
    st = [[0] * log_n for _ in range(n)]
    
    # Initialize for length 1
    for i in range(n):
        st[i][0] = arr[i]
    
    # Fill sparse table
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1])
    
    results = []
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Find largest power of 2 that fits in range
        length = r - l + 1
        k = 0
        while (1 << (k + 1)) <= length:
            k += 1
        
        # Query minimum using sparse table
        min_val = min(st[l][k], st[r - (1 << k) + 1][k])
        results.append(min_val)
    
    return results
```

### Approach 3: Optimal with Sparse Table
**Time Complexity**: O(n log n + q)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute sparse table where st[i][j] = minimum in range [i, i + 2^j - 1]
2. For each query, find the largest power of 2 that fits in the range
3. Use sparse table to find minimum in O(1) time
4. Return the minimum

**Implementation**:
```python
def optimal_static_range_minimum_queries(arr, queries):
    n = len(arr)
    
    # Precompute sparse table
    log_n = 0
    while (1 << log_n) <= n:
        log_n += 1
    
    st = [[0] * log_n for _ in range(n)]
    
    # Initialize for length 1
    for i in range(n):
        st[i][0] = arr[i]
    
    # Fill sparse table
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1])
    
    results = []
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Find largest power of 2 that fits in range
        length = r - l + 1
        k = 0
        while (1 << (k + 1)) <= length:
            k += 1
        
        # Query minimum using sparse table
        min_val = min(st[l][k], st[r - (1 << k) + 1][k])
        results.append(min_val)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Find minimum for each query |
| Optimized | O(n log n + q) | O(n log n) | Use sparse table for O(1) queries |
| Optimal | O(n log n + q) | O(n log n) | Use sparse table for O(1) queries |

### Time Complexity
- **Time**: O(n log n + q) - O(n log n) preprocessing + O(1) per query
- **Space**: O(n log n) - Sparse table

### Why This Solution Works
- **Sparse Table Property**: st[i][j] stores minimum in range [i, i + 2^j - 1]
- **Efficient Preprocessing**: Calculate sparse table in O(n log n) time
- **Fast Queries**: Answer each query in O(1) time using sparse table
- **Optimal Approach**: O(n log n + q) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Sparse Table Technique**: The standard approach for static range minimum queries
- **Efficient Preprocessing**: Calculate sparse table once for all queries
- **Fast Queries**: Answer each query in O(1) time using sparse table
- **Space Trade-off**: Use O(n log n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many static range query problems