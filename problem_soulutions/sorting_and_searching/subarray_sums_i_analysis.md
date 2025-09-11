---
layout: simple
title: "Subarray Sums I"
permalink: /problem_soulutions/sorting_and_searching/subarray_sums_i_analysis
---

# Subarray Sums I

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of prefix sums and their applications
- Apply prefix sum technique for efficient range sum queries
- Implement efficient solutions for subarray sum problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in prefix sum problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Prefix sums, range queries, array processing, optimization
- **Data Structures**: Arrays, prefix sum arrays, hash maps
- **Mathematical Concepts**: Summation, range queries, optimization theory
- **Programming Skills**: Algorithm implementation, complexity analysis, prefix sum construction
- **Related Problems**: Subarray Sums II (hash map), Range Sum Queries (prefix sums), Maximum Subarray Sum (Kadane's algorithm)

## 📋 Problem Description

You are given an array of n integers and q queries. Each query asks for the sum of elements in a subarray from position a to position b (inclusive).

Answer all queries efficiently.

**Input**: 
- First line: two integers n and q (array size and number of queries)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)
- Next q lines: two integers a and b (query range)

**Output**: 
- Print q integers: the sum of elements in each query range

**Constraints**:
- 1 ≤ n, q ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹
- 1 ≤ a ≤ b ≤ n

**Example**:
```
Input:
8 3
3 2 4 5 1 6 2 7
2 5
1 3
4 8

Output:
12
9
21

Explanation**: 
Array: [3, 2, 4, 5, 1, 6, 2, 7]

Query 1: Range [2, 5] → sum = 2 + 4 + 5 + 1 = 12
Query 2: Range [1, 3] → sum = 3 + 2 + 4 = 9
Query 3: Range [4, 8] → sum = 5 + 1 + 6 + 2 + 7 = 21
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Calculate Sum for Each Query

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: For each query, iterate through the range and calculate the sum
- **Complete Coverage**: Guaranteed to find the correct sum for each query
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity for multiple queries

**Key Insight**: For each query, iterate through the specified range and sum all elements.

**Algorithm**:
- For each query (a, b):
  - Initialize sum = 0
  - Iterate from position a to b (inclusive)
  - Add each element to the sum
  - Return the sum

**Visual Example**:
```
Array: [3, 2, 4, 5, 1, 6, 2, 7]

Query 1: Range [2, 5]
- Position 2: sum = 0 + 2 = 2
- Position 3: sum = 2 + 4 = 6
- Position 4: sum = 6 + 5 = 11
- Position 5: sum = 11 + 1 = 12
Result: 12

Query 2: Range [1, 3]
- Position 1: sum = 0 + 3 = 3
- Position 2: sum = 3 + 2 = 5
- Position 3: sum = 5 + 4 = 9
Result: 9

Query 3: Range [4, 8]
- Position 4: sum = 0 + 5 = 5
- Position 5: sum = 5 + 1 = 6
- Position 6: sum = 6 + 6 = 12
- Position 7: sum = 12 + 2 = 14
- Position 8: sum = 14 + 7 = 21
Result: 21
```

**Implementation**:
```python
def brute_force_subarray_sums_i(arr, queries):
    """
    Find subarray sums using brute force approach
    
    Args:
        arr: list of integers
        queries: list of (start, end) tuples
    
    Returns:
        list: sum for each query
    """
    results = []
    
    for start, end in queries:
        current_sum = 0
        for i in range(start - 1, end):  # Convert to 0-based indexing
            current_sum += arr[i]
        results.append(current_sum)
    
    return results

# Example usage
arr = [3, 2, 4, 5, 1, 6, 2, 7]
queries = [(2, 5), (1, 3), (4, 8)]
result = brute_force_subarray_sums_i(arr, queries)
print(f"Brute force result: {result}")  # Output: [12, 9, 21]
```

**Time Complexity**: O(q × n) - For each query, iterate through the range
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs with many queries.

---

### Approach 2: Optimized - Precompute Prefix Sums

**Key Insights from Optimized Approach**:
- **Prefix Sums**: Precompute prefix sums to answer queries in O(1) time
- **Efficient Queries**: Use prefix sum array to calculate range sums quickly
- **Better Complexity**: Achieve O(n + q) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use prefix sums to precompute cumulative sums and answer range queries in O(1) time.

**Algorithm**:
- Precompute prefix sum array: prefix[i] = sum of elements from 1 to i
- For each query (a, b): sum = prefix[b] - prefix[a-1]

**Visual Example**:
```
Array: [3, 2, 4, 5, 1, 6, 2, 7]

Prefix sum array: [0, 3, 5, 9, 14, 15, 21, 23, 30]
- prefix[0] = 0
- prefix[1] = 3
- prefix[2] = 3 + 2 = 5
- prefix[3] = 5 + 4 = 9
- prefix[4] = 9 + 5 = 14
- prefix[5] = 14 + 1 = 15
- prefix[6] = 15 + 6 = 21
- prefix[7] = 21 + 2 = 23
- prefix[8] = 23 + 7 = 30

Query 1: Range [2, 5]
- sum = prefix[5] - prefix[1] = 15 - 3 = 12

Query 2: Range [1, 3]
- sum = prefix[3] - prefix[0] = 9 - 0 = 9

Query 3: Range [4, 8]
- sum = prefix[8] - prefix[3] = 30 - 9 = 21
```

**Implementation**:
```python
def optimized_subarray_sums_i(arr, queries):
    """
    Find subarray sums using prefix sum approach
    
    Args:
        arr: list of integers
        queries: list of (start, end) tuples
    
    Returns:
        list: sum for each query
    """
    n = len(arr)
    prefix = [0] * (n + 1)
    
    # Build prefix sum array
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    for start, end in queries:
        # Convert to 0-based indexing and use prefix sum formula
        sum_range = prefix[end] - prefix[start - 1]
        results.append(sum_range)
    
    return results

# Example usage
arr = [3, 2, 4, 5, 1, 6, 2, 7]
queries = [(2, 5), (1, 3), (4, 8)]
result = optimized_subarray_sums_i(arr, queries)
print(f"Optimized result: {result}")  # Output: [12, 9, 21]
```

**Time Complexity**: O(n + q) - O(n) for prefix sum construction, O(q) for queries
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: Much more efficient than brute force with prefix sum optimization.

---

### Approach 3: Optimal - In-Place Prefix Sums

**Key Insights from Optimal Approach**:
- **In-Place Construction**: Build prefix sums in-place to save memory
- **Optimal Complexity**: Achieve O(n + q) time complexity with minimal space
- **Efficient Implementation**: No need for extra array
- **Space Optimization**: Use the original array for prefix sums

**Key Insight**: Build prefix sums in-place to achieve optimal space complexity while maintaining O(1) query time.

**Algorithm**:
- Build prefix sums in-place: arr[i] = arr[i] + arr[i-1]
- For each query (a, b): sum = arr[b-1] - (arr[a-2] if a > 1 else 0)

**Visual Example**:
```
Array: [3, 2, 4, 5, 1, 6, 2, 7]

In-place prefix sum construction:
- arr[0] = 3 (unchanged)
- arr[1] = 2 + 3 = 5
- arr[2] = 4 + 5 = 9
- arr[3] = 5 + 9 = 14
- arr[4] = 1 + 14 = 15
- arr[5] = 6 + 15 = 21
- arr[6] = 2 + 21 = 23
- arr[7] = 7 + 23 = 30

Final array: [3, 5, 9, 14, 15, 21, 23, 30]

Query 1: Range [2, 5] (1-based)
- sum = arr[4] - arr[0] = 15 - 3 = 12

Query 2: Range [1, 3] (1-based)
- sum = arr[2] - 0 = 9 - 0 = 9

Query 3: Range [4, 8] (1-based)
- sum = arr[7] - arr[2] = 30 - 9 = 21
```

**Implementation**:
```python
def optimal_subarray_sums_i(arr, queries):
    """
    Find subarray sums using optimal in-place prefix sum approach
    
    Args:
        arr: list of integers
        queries: list of (start, end) tuples
    
    Returns:
        list: sum for each query
    """
    n = len(arr)
    
    # Build prefix sums in-place
    for i in range(1, n):
        arr[i] += arr[i - 1]
    
    results = []
    for start, end in queries:
        # Convert to 0-based indexing
        start_idx = start - 1
        end_idx = end - 1
        
        if start_idx == 0:
            sum_range = arr[end_idx]
        else:
            sum_range = arr[end_idx] - arr[start_idx - 1]
        
        results.append(sum_range)
    
    return results

# Example usage
arr = [3, 2, 4, 5, 1, 6, 2, 7]
queries = [(2, 5), (1, 3), (4, 8)]
result = optimal_subarray_sums_i(arr, queries)
print(f"Optimal result: {result}")  # Output: [12, 9, 21]
```

**Time Complexity**: O(n + q) - O(n) for prefix sum construction, O(q) for queries
**Space Complexity**: O(1) - In-place modification

**Why it's optimal**: Achieves the best possible time complexity with minimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(1) | Calculate sum for each query |
| Prefix Sums | O(n + q) | O(n) | Precompute prefix sums |
| In-Place | O(n + q) | O(1) | Build prefix sums in-place |

### Time Complexity
- **Time**: O(n + q) - Prefix sum approach provides optimal time complexity
- **Space**: O(1) - In-place modification

### Why This Solution Works
- **Prefix Sums**: Precompute cumulative sums to answer range queries in O(1) time
- **Optimal Algorithm**: Prefix sum approach is the standard solution for range sum queries
- **Optimal Approach**: In-place prefix sums provide the most efficient solution for subarray sum problems
