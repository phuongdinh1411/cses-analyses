---
layout: simple
title: "Static Range Sum Queries - Prefix Sums"
permalink: /problem_soulutions/range_queries/static_range_sum_queries_analysis
---

# Static Range Sum Queries - Prefix Sums

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement prefix sum technique for range queries
- Apply prefix sums to efficiently answer static range sum queries
- Optimize range sum calculations using prefix sum arrays
- Handle edge cases in prefix sum problems
- Recognize when to use prefix sums vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Prefix sums, range queries, static data structures
- **Data Structures**: Arrays, prefix sum arrays
- **Mathematical Concepts**: Range sum optimization, cumulative sums
- **Programming Skills**: Array manipulation, prefix sum implementation
- **Related Problems**: Dynamic range sum queries, range update queries, subarray sum queries

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the sum of elements in a range [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (range boundaries, 1-indexed)

**Output**: 
- q lines: sum of elements in range [l, r] for each query

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
1. For each query, iterate through the range [l, r]
2. Sum all elements in the range
3. Return the sum

**Implementation**:
```python
def brute_force_static_range_sum_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Calculate sum in range [l, r]
        range_sum = 0
        for i in range(l, r + 1):
            range_sum += arr[i]
        
        results.append(range_sum)
    
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
def optimized_static_range_sum_queries(arr, queries):
    n = len(arr)
    
    # Precompute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    for l, r in queries:
        # Calculate sum using prefix sums
        range_sum = prefix[r] - prefix[l - 1]
        results.append(range_sum)
    
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
def optimal_static_range_sum_queries(arr, queries):
    n = len(arr)
    
    # Precompute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    for l, r in queries:
        # Calculate sum using prefix sums
        range_sum = prefix[r] - prefix[l - 1]
        results.append(range_sum)
    
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
- **Prefix Sum Property**: prefix[r] - prefix[l-1] gives sum of range [l, r]
- **Efficient Preprocessing**: Calculate prefix sums once in O(n) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n + q) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. 2D Range Sum Queries**
**Problem**: Given a 2D matrix, answer queries for sum of elements in a rectangular region.

**Key Differences**: 2D instead of 1D, requires 2D prefix sums

**Solution Approach**: Use 2D prefix sum array

**Implementation**:
```python
def range_sum_2d(matrix, queries):
    """
    Answer 2D range sum queries using 2D prefix sums
    """
    rows, cols = len(matrix), len(matrix[0])
    
    # Build 2D prefix sum array
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(rows):
        for j in range(cols):
            prefix[i + 1][j + 1] = (prefix[i][j + 1] + 
                                   prefix[i + 1][j] - 
                                   prefix[i][j] + 
                                   matrix[i][j])
    
    results = []
    for x1, y1, x2, y2 in queries:
        # Calculate sum using 2D prefix sums
        sum_val = (prefix[x2][y2] - 
                  prefix[x1 - 1][y2] - 
                  prefix[x2][y1 - 1] + 
                  prefix[x1 - 1][y1 - 1])
        results.append(sum_val)
    
    return results

# Example usage
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
queries = [(1, 1, 2, 2), (1, 1, 3, 3)]
result = range_sum_2d(matrix, queries)
print(f"2D range sums: {result}")  # Output: [12, 45]
```

#### **2. Range XOR Queries**
**Problem**: Answer queries for XOR of elements in a range.

**Key Differences**: XOR operation instead of sum

**Solution Approach**: Use prefix XOR array

**Implementation**:
```python
def range_xor_queries(arr, queries):
    """
    Answer range XOR queries using prefix XOR
    """
    n = len(arr)
    
    # Build prefix XOR array
    prefix_xor = [0] * (n + 1)
    for i in range(n):
        prefix_xor[i + 1] = prefix_xor[i] ^ arr[i]
    
    results = []
    for l, r in queries:
        # Calculate XOR using prefix XOR
        xor_result = prefix_xor[r] ^ prefix_xor[l - 1]
        results.append(xor_result)
    
    return results

# Example usage
arr = [1, 2, 3, 4, 5]
queries = [(1, 3), (2, 4), (1, 5)]
result = range_xor_queries(arr, queries)
print(f"Range XOR results: {result}")  # Output: [0, 5, 1]
```

#### **3. Range Maximum Queries**
**Problem**: Answer queries for maximum element in a range.

**Key Differences**: Maximum instead of sum, requires different data structure

**Solution Approach**: Use sparse table for O(1) queries

**Implementation**:
```python
def range_maximum_queries(arr, queries):
    """
    Answer range maximum queries using sparse table
    """
    n = len(arr)
    
    # Build sparse table
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

# Example usage
arr = [1, 3, 2, 4, 5]
queries = [(1, 3), (2, 4), (1, 5)]
result = range_maximum_queries(arr, queries)
print(f"Range maximums: {result}")  # Output: [3, 4, 5]
```

### Related Problems

#### **CSES Problems**
- [Static Range Sum Queries](https://cses.fi/problemset/task/1646) - Basic prefix sum queries
- [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) - Range minimum queries with sparse table
- [Range XOR Queries](https://cses.fi/problemset/task/1650) - Range XOR queries with prefix XOR
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Range sum with updates using segment tree

#### **LeetCode Problems**
- [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) - Basic prefix sum
- [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) - 2D prefix sum
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates
- [Range Sum Query 2D - Mutable](https://leetcode.com/problems/range-sum-query-2d-mutable/) - 2D range sum with updates

#### **Problem Categories**
- **Prefix Sums**: Static range sum, 2D range sum, range XOR, range AND/OR
- **Sparse Table**: Range minimum/maximum, range GCD, range AND/OR
- **Segment Tree**: Dynamic range queries, range updates, custom operations
- **Binary Indexed Tree**: Point updates with range queries, inversion counting

## 🚀 Key Takeaways

- **Prefix Sum Technique**: The standard approach for static range sum queries
- **Efficient Preprocessing**: Calculate prefix sums once for all queries
- **Fast Queries**: Answer each query in O(1) time using prefix sums
- **Space Trade-off**: Use O(n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many static range query problems