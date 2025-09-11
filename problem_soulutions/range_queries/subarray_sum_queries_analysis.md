---
layout: simple
title: "Subarray Sum Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_sum_queries_analysis
---

# Subarray Sum Queries - Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range queries for subarray sum problems
- Apply range queries to efficiently answer subarray sum queries
- Optimize subarray sum calculations using range queries
- Handle edge cases in subarray sum query problems
- Recognize when to use range queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Range queries, subarray sum problems, prefix sums
- **Data Structures**: Arrays, prefix sum arrays, range query structures
- **Mathematical Concepts**: Subarray sum optimization, range query optimization
- **Programming Skills**: Array manipulation, range query implementation
- **Related Problems**: Static range sum queries, dynamic range sum queries, subarray problems

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the sum of elements in a subarray [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (subarray boundaries, 1-indexed)

**Output**: 
- q lines: sum of elements in subarray [l, r] for each query

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
6
9
15

Explanation**: 
Query 1: sum of [1,2,3] = 6
Query 2: sum of [2,3,4] = 9
Query 3: sum of [1,2,3,4,5] = 15
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Sum all elements in the subarray
3. Return the sum

**Implementation**:
```python
def brute_force_subarray_sum_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Calculate sum in subarray [l, r]
        subarray_sum = 0
        for i in range(l, r + 1):
            subarray_sum += arr[i]
        
        results.append(subarray_sum)
    
    return results
```

### Approach 2: Optimized with Prefix Sums
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute prefix sum array where prefix[i] = sum of elements from 0 to i
2. For each query, calculate sum as prefix[r] - prefix[l-1]
3. Return the sum

**Implementation**:
```python
def optimized_subarray_sum_queries(arr, queries):
    n = len(arr)
    
    # Precompute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    for l, r in queries:
        # Calculate sum using prefix sums
        subarray_sum = prefix[r] - prefix[l - 1]
        results.append(subarray_sum)
    
    return results
```

### Approach 3: Optimal with Prefix Sums
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute prefix sum array where prefix[i] = sum of elements from 0 to i
2. For each query, calculate sum as prefix[r] - prefix[l-1]
3. Return the sum

**Implementation**:
```python
def optimal_subarray_sum_queries(arr, queries):
    n = len(arr)
    
    # Precompute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    for l, r in queries:
        # Calculate sum using prefix sums
        subarray_sum = prefix[r] - prefix[l - 1]
        results.append(subarray_sum)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Calculate sum for each query |
| Optimized | O(n + q) | O(n) | Use prefix sums for O(1) queries |
| Optimal | O(n + q) | O(n) | Use prefix sums for O(1) queries |

### Time Complexity
- **Time**: O(n + q) - O(n) preprocessing + O(1) per query
- **Space**: O(n) - Prefix sum array

### Why This Solution Works
- **Prefix Sum Property**: prefix[r] - prefix[l-1] gives sum of subarray [l, r]
- **Efficient Preprocessing**: Calculate prefix sums once in O(n) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n + q) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Prefix Sum Technique**: The standard approach for subarray sum queries
- **Efficient Preprocessing**: Calculate prefix sums once for all queries
- **Fast Queries**: Answer each query in O(1) time using prefix sums
- **Space Trade-off**: Use O(n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many subarray sum problems