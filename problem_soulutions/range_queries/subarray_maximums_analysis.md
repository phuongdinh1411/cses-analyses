---
layout: simple
title: "Subarray Maximums - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_maximums_analysis
---

# Subarray Maximums - Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range queries for subarray maximum problems
- Apply range queries to efficiently answer subarray maximum queries
- Optimize subarray maximum calculations using range queries
- Handle edge cases in subarray maximum query problems
- Recognize when to use range queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Range queries, subarray maximum problems, sparse tables
- **Data Structures**: Arrays, sparse tables, range query structures
- **Mathematical Concepts**: Subarray maximum optimization, range query optimization
- **Programming Skills**: Array manipulation, range query implementation
- **Related Problems**: Subarray sum queries, subarray minimum queries, range query problems

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the maximum element in a subarray [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (subarray boundaries, 1-indexed)

**Output**: 
- q lines: maximum element in subarray [l, r] for each query

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
3
4
5

Explanation**: 
Query 1: maximum of [1,2,3] = 3
Query 2: maximum of [2,3,4] = 4
Query 3: maximum of [1,2,3,4,5] = 5
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Find maximum element in the subarray
3. Return the maximum

**Implementation**:
```python
def brute_force_subarray_maximums(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Find maximum in subarray [l, r]
        max_val = float('-inf')
        for i in range(l, r + 1):
            max_val = max(max_val, arr[i])
        
        results.append(max_val)
    
    return results
```

### Approach 2: Optimized with Sparse Table
**Time Complexity**: O(n log n + q)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute sparse table where st[i][j] = maximum in range [i, i + 2^j - 1]
2. For each query, use sparse table to find maximum in O(1) time
3. Return the maximum

**Implementation**:
```python
def optimized_subarray_maximums(arr, queries):
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
            st[i][j] = max(st[i][j-1], st[i + (1 << (j-1))][j-1])
    
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
        
        # Query maximum using sparse table
        max_val = max(st[l][k], st[r - (1 << k) + 1][k])
        results.append(max_val)
    
    return results
```

### Approach 3: Optimal with Sparse Table
**Time Complexity**: O(n log n + q)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute sparse table where st[i][j] = maximum in range [i, i + 2^j - 1]
2. For each query, use sparse table to find maximum in O(1) time
3. Return the maximum

**Implementation**:
```python
def optimal_subarray_maximums(arr, queries):
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
            st[i][j] = max(st[i][j-1], st[i + (1 << (j-1))][j-1])
    
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
        
        # Query maximum using sparse table
        max_val = max(st[l][k], st[r - (1 << k) + 1][k])
        results.append(max_val)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Find maximum for each query |
| Optimized | O(n log n + q) | O(n log n) | Use sparse table for O(1) queries |
| Optimal | O(n log n + q) | O(n log n) | Use sparse table for O(1) queries |

### Time Complexity
- **Time**: O(n log n + q) - O(n log n) preprocessing + O(1) per query
- **Space**: O(n log n) - Sparse table

### Why This Solution Works
- **Sparse Table Property**: st[i][j] stores maximum in range [i, i + 2^j - 1]
- **Efficient Preprocessing**: Calculate sparse table in O(n log n) time
- **Fast Queries**: Answer each query in O(1) time using sparse table
- **Optimal Approach**: O(n log n + q) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Sparse Table Technique**: The standard approach for subarray maximum queries
- **Efficient Preprocessing**: Calculate sparse table once for all queries
- **Fast Queries**: Answer each query in O(1) time using sparse table
- **Space Trade-off**: Use O(n log n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many subarray maximum problems