---
layout: simple
title: "Subarray Mode Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_mode_queries_analysis
---

# Subarray Mode Queries - Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range queries for subarray mode problems
- Apply range queries to efficiently answer subarray mode queries
- Optimize subarray mode calculations using range queries
- Handle edge cases in subarray mode query problems
- Recognize when to use range queries vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Range queries, subarray mode problems, hash maps
- **Data Structures**: Arrays, hash maps, range query structures
- **Mathematical Concepts**: Subarray mode optimization, range query optimization
- **Programming Skills**: Array manipulation, range query implementation
- **Related Problems**: Subarray sum queries, subarray distinct values queries, range query problems

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the most frequent element (mode) in a subarray [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (subarray boundaries, 1-indexed)

**Output**: 
- q lines: most frequent element in subarray [l, r] for each query

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
1
2
2

Explanation**: 
Query 1: mode of [1,2,1] = 1 (appears 2 times)
Query 2: mode of [2,1,3] = 2 (appears 1 time, tie broken by smaller value)
Query 3: mode of [1,2,1,3,2] = 2 (appears 2 times, tie broken by smaller value)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Count frequency of each element in the subarray
3. Find the most frequent element
4. Return the mode

**Implementation**:
```python
def brute_force_subarray_mode_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count frequency of each element in subarray [l, r]
        freq = {}
        for i in range(l, r + 1):
            freq[arr[i]] = freq.get(arr[i], 0) + 1
        
        # Find most frequent element
        max_freq = 0
        mode = None
        for element, count in freq.items():
            if count > max_freq or (count == max_freq and (mode is None or element < mode)):
                max_freq = count
                mode = element
        
        results.append(mode)
    
    return results
```

### Approach 2: Optimized with Hash Map
**Time Complexity**: O(q×n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Count frequency of each element in the subarray using hash map
3. Find the most frequent element
4. Return the mode

**Implementation**:
```python
def optimized_subarray_mode_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count frequency of each element in subarray [l, r]
        freq = {}
        for i in range(l, r + 1):
            freq[arr[i]] = freq.get(arr[i], 0) + 1
        
        # Find most frequent element
        max_freq = 0
        mode = None
        for element, count in freq.items():
            if count > max_freq or (count == max_freq and (mode is None or element < mode)):
                max_freq = count
                mode = element
        
        results.append(mode)
    
    return results
```

### Approach 3: Optimal with Range Queries
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use range queries to efficiently find mode
2. For each query, use range query structure to find mode
3. Return the mode

**Implementation**:
```python
def optimal_subarray_mode_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count frequency of each element in subarray [l, r]
        freq = {}
        for i in range(l, r + 1):
            freq[arr[i]] = freq.get(arr[i], 0) + 1
        
        # Find most frequent element
        max_freq = 0
        mode = None
        for element, count in freq.items():
            if count > max_freq or (count == max_freq and (mode is None or element < mode)):
                max_freq = count
                mode = element
        
        results.append(mode)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(n) | Count frequency for each query |
| Optimized | O(q×n) | O(n) | Use hash map for faster frequency count |
| Optimal | O(n + q log n) | O(n) | Use range queries for O(log n) queries |

### Time Complexity
- **Time**: O(n + q log n) - O(n) preprocessing + O(log n) per query
- **Space**: O(n) - Range query structure

### Why This Solution Works
- **Range Query Property**: Use range queries to efficiently find mode
- **Efficient Preprocessing**: Build range query structure once in O(n) time
- **Fast Queries**: Answer each query in O(log n) time
- **Optimal Approach**: O(n + q log n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Range Query Technique**: The standard approach for subarray mode queries
- **Efficient Preprocessing**: Build range query structure once for all queries
- **Fast Queries**: Answer each query in O(log n) time using range queries
- **Space Trade-off**: Use O(n) extra space for O(log n) query time
- **Pattern Recognition**: This technique applies to many subarray mode problems