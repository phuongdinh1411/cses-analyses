---
layout: simple
title: "Prefix Sum Queries - Dynamic Range Sums"
permalink: /problem_soulutions/graph_algorithms/prefix_sum_queries_analysis
---

# Prefix Sum Queries - Dynamic Range Sums

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand dynamic range query problems and prefix sum concepts
- Apply Binary Indexed Trees or Segment Trees to handle dynamic range sum queries
- Implement efficient dynamic range query algorithms with proper data structure usage
- Optimize dynamic range queries using advanced data structures and query processing
- Handle edge cases in dynamic range queries (large ranges, frequent updates, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Binary Indexed Trees, Segment Trees, dynamic range queries, prefix sums, query optimization
- **Data Structures**: BIT, segment trees, range query data structures, update tracking
- **Mathematical Concepts**: Range queries, prefix sums, tree data structures, query optimization
- **Programming Skills**: BIT implementation, segment tree implementation, range query processing, algorithm implementation
- **Related Problems**: Range query problems, Data structure problems, Query optimization

## Problem Description

**Problem**: Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the sum of elements from position a to b

This is a classic dynamic range query problem that requires efficient handling of both point updates and range sum queries. The solution involves using advanced data structures like Binary Indexed Trees or Segment Trees.

**Input**: 
- First line: Two integers n and q (size of array and number of queries)
- Second line: n integers a₁, a₂, …, aₙ (the array)
- Next q lines: Queries (either "1 k x" for updates or "2 a b" for sums)

**Output**: 
- For each sum query, print the sum

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ aᵢ ≤ 10⁹
- 1 ≤ k ≤ n
- 1 ≤ a ≤ b ≤ n
- Array is 1-indexed
- Updates and queries are mixed

**Example**:
```
Input:
8 4
3 2 4 5 1 1 5 3
2 1 4
1 4 9
2 1 4
2 2 6

Output:
14
20
17
```

**Explanation**: 
- Query 1: Sum of elements from position 1 to 4 = 3+2+4+5 = 14
- Query 2: Update position 4 to value 9
- Query 3: Sum of elements from position 1 to 4 = 3+2+4+9 = 20
- Query 4: Sum of elements from position 2 to 6 = 2+4+9+1+1 = 17

## Visual Example

### Input Array and Queries
```
Array: [3, 2, 4, 5, 1, 1, 5, 3]
Queries:
1. Sum range [1,4]: 3+2+4+5 = 14
2. Update position 4 to 9
3. Sum range [1,4]: 3+2+4+9 = 20
4. Sum range [2,6]: 2+4+9+1+1 = 17
```

### Binary Indexed Tree (Fenwick Tree) Process
```
Step 1: Initialize BIT
Array: [3, 2, 4, 5, 1, 1, 5, 3]
BIT:   [0, 3, 5, 4, 14, 1, 2, 5, 24]

Step 2: Process queries

Query 1: Sum range [1,4]
- Sum(4) = BIT[4] = 14
- Sum(0) = 0
- Range sum = 14 - 0 = 14

Query 2: Update position 4 to 9
- Old value: 5, New value: 9
- Difference: 9 - 5 = 4
- Update BIT at position 4: add 4
- BIT: [0, 3, 5, 4, 18, 1, 2, 5, 28]

Query 3: Sum range [1,4]
- Sum(4) = BIT[4] = 18
- Sum(0) = 0
- Range sum = 18 - 0 = 18

Query 4: Sum range [2,6]
- Sum(6) = BIT[6] + BIT[4] = 2 + 18 = 20
- Sum(1) = BIT[1] = 3
- Range sum = 20 - 3 = 17
```

### Key Insight
Binary Indexed Tree works by:
1. Using binary representation for efficient updates
2. Each node stores sum of a range ending at that position
3. Update: O(log n) time complexity
4. Query: O(log n) time complexity
5. Space complexity: O(n)

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Array Updates (Inefficient)

**Key Insights from Brute Force Solution:**
- Update array directly and calculate sums by iterating
- Simple but computationally expensive approach
- Not suitable for large inputs with many queries
- Straightforward implementation but poor performance

**Algorithm:**
1. For each update query, directly modify the array
2. For each sum query, iterate through the range and calculate sum
3. Return the results for all sum queries

**Visual Example:**
```
Brute force: Direct array updates and range iteration
For array: [3, 2, 4, 5, 1, 1, 5, 3]

Query 1: Sum range [1,4]
- Iterate through positions 1 to 4
- Sum = 3 + 2 + 4 + 5 = 14

Query 2: Update position 4 to 9
- Array becomes: [3, 2, 4, 9, 1, 1, 5, 3]

Query 3: Sum range [1,4]
- Iterate through positions 1 to 4
- Sum = 3 + 2 + 4 + 9 = 20

Query 4: Sum range [2,6]
- Iterate through positions 2 to 6
- Sum = 2 + 4 + 9 + 1 + 1 = 17
```

**Implementation:**
```python
def prefix_sum_queries_brute_force(n, q, arr, queries):
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            arr[k-1] = x
        else:  # Sum query
            a, b = query[1], query[2]
            total = sum(arr[a-1:b])
            results.append(total)
    
    return results
```

**Time Complexity:** O(q × n) for q queries with O(n) range sum
**Space Complexity:** O(1) for additional space

**Why it's inefficient:**
- O(q × n) time complexity is too slow for large inputs
- Not suitable for competitive programming
- Inefficient for frequent range queries
- Poor performance with large arrays

### Approach 2: Prefix Sum Array (Better)

**Key Insights from Prefix Sum Solution:**
- Precompute prefix sums for O(1) range queries
- Handle updates by rebuilding prefix array
- Better than brute force but still not optimal
- Good for static arrays with few updates

**Algorithm:**
1. Build prefix sum array from original array
2. For each update, rebuild the entire prefix sum array
3. For each sum query, use prefix sum array for O(1) calculation

**Visual Example:**
```
Prefix sum approach for array: [3, 2, 4, 5, 1, 1, 5, 3]

Step 1: Build prefix sum array
Original: [3, 2, 4, 5, 1, 1, 5, 3]
Prefix:   [3, 5, 9, 14, 15, 16, 21, 24]

Query 1: Sum range [1,4]
- Range sum = prefix[4] - prefix[0] = 14 - 0 = 14

Query 2: Update position 4 to 9
- Rebuild prefix array: [3, 5, 9, 18, 19, 20, 25, 28]

Query 3: Sum range [1,4]
- Range sum = prefix[4] - prefix[0] = 18 - 0 = 18

Query 4: Sum range [2,6]
- Range sum = prefix[6] - prefix[1] = 20 - 3 = 17
```

**Implementation:**
```python
def prefix_sum_queries_prefix_array(n, q, arr, queries):
    def build_prefix():
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + arr[i]
        return prefix
    
    prefix = build_prefix()
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            arr[k-1] = x
            prefix = build_prefix()  # Rebuild prefix array
        else:  # Sum query
            a, b = query[1], query[2]
            total = prefix[b] - prefix[a-1]
            results.append(total)
    
    return results
```

**Time Complexity:** O(q × n) for q queries with O(n) prefix rebuild
**Space Complexity:** O(n) for prefix array

**Why it's better:**
- O(1) range sum queries after prefix computation
- Better than brute force for range queries
- Still not optimal for frequent updates
- Suitable for static arrays

### Approach 3: Binary Indexed Tree (Optimal)

**Key Insights from Binary Indexed Tree Solution:**
- Use Binary Indexed Tree for efficient updates and queries
- Both update and query operations in O(log n) time
- Most efficient approach for dynamic range queries
- Standard method in competitive programming

**Algorithm:**
1. Initialize Binary Indexed Tree with array values
2. For each update, use BIT update operation
3. For each sum query, use BIT range query operation

**Visual Example:**
```
Binary Indexed Tree approach for array: [3, 2, 4, 5, 1, 1, 5, 3]

Step 1: Initialize BIT
Array: [3, 2, 4, 5, 1, 1, 5, 3]
BIT:   [0, 3, 5, 4, 14, 1, 2, 5, 24]

Query 1: Sum range [1,4]
- Sum(4) = BIT[4] = 14
- Sum(0) = 0
- Range sum = 14 - 0 = 14

Query 2: Update position 4 to 9
- Old value: 5, New value: 9
- Difference: 9 - 5 = 4
- Update BIT at position 4: add 4
- BIT: [0, 3, 5, 4, 18, 1, 2, 5, 28]

Query 3: Sum range [1,4]
- Sum(4) = BIT[4] = 18
- Sum(0) = 0
- Range sum = 18 - 0 = 18

Query 4: Sum range [2,6]
- Sum(6) = BIT[6] + BIT[4] = 2 + 18 = 20
- Sum(1) = BIT[1] = 3
- Range sum = 20 - 3 = 17
```

**Implementation:**
```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, index, value):
        while index <= self.n:
            self.tree[index] += value
            index += index & -index
    
    def query(self, index):
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result
    
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)

def prefix_sum_queries_optimized(n, q, arr, queries):
    bit = BIT(n)
    
    # Initialize BIT with array values
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            old_val = arr[k-1]
            bit.update(k, x - old_val)
            arr[k-1] = x
        else:  # Sum query
            a, b = query[1], query[2]
            total = bit.range_query(a, b)
            results.append(total)
    
    return results

def solve_prefix_sum_queries():
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        query = list(map(int, input().split()))
        queries.append(query)
    
    results = prefix_sum_queries_optimized(n, q, arr, queries)
    for result in results:
        print(result)

# Main execution
if __name__ == "__main__":
    solve_prefix_sum_queries()
```

**Time Complexity:** O(q × log n) for q queries with O(log n) operations
**Space Complexity:** O(n) for BIT

**Why it's optimal:**
- O(log n) time complexity for both updates and queries
- Most efficient approach for dynamic range queries
- Standard method in competitive programming
- Optimal for large inputs with many queries

## 🎯 Problem Variations

### Variation 1: Range Sum with Different Update Operations
**Problem**: Handle range sum queries with different types of update operations.

**Link**: [CSES Problem Set - Range Sum with Update Operations](https://cses.fi/problemset/task/range_sum_update_operations)

```python
def prefix_sum_queries_update_operations(n, q, arr, queries):
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, index, value):
        while index <= self.n:
            self.tree[index] += value
            index += index & -index
    
    def query(self, index):
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result
    
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)

    bit = BIT(n)
    
    # Initialize BIT with array values
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            old_val = arr[k-1]
            bit.update(k, x - old_val)
            arr[k-1] = x
        elif query[0] == 2:  # Add to range
            a, b, x = query[1], query[2], query[3]
            for i in range(a, b + 1):
                bit.update(i, x)
        else:  # Sum query
            a, b = query[1], query[2]
            total = bit.range_query(a, b)
            results.append(total)
    
    return results
```

### Variation 2: Range Sum with Multiple Arrays
**Problem**: Handle range sum queries across multiple arrays.

**Link**: [CSES Problem Set - Range Sum Multiple Arrays](https://cses.fi/problemset/task/range_sum_multiple_arrays)

```python
def prefix_sum_queries_multiple_arrays(n, q, arrays, queries):
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, index, value):
            while index <= self.n:
                self.tree[index] += value
                index += index & -index
        
        def query(self, index):
            result = 0
            while index > 0:
                result += self.tree[index]
                index -= index & -index
            return result
        
        def range_query(self, left, right):
            return self.query(right) - self.query(left - 1)
    
    # Create BIT for each array
    bits = []
    for arr in arrays:
        bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, arr[i])
        bits.append(bit)
    
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            array_idx, k, x = query[1], query[2], query[3]
            old_val = arrays[array_idx][k-1]
            bits[array_idx].update(k, x - old_val)
            arrays[array_idx][k-1] = x
        else:  # Sum query
            array_idx, a, b = query[1], query[2], query[3]
            total = bits[array_idx].range_query(a, b)
            results.append(total)
    
    return results
```

### Variation 3: Range Sum with Range Updates
**Problem**: Handle range sum queries with range update operations.

**Link**: [CSES Problem Set - Range Sum Range Updates](https://cses.fi/problemset/task/range_sum_range_updates)

```python
def prefix_sum_queries_range_updates(n, q, arr, queries):
    class BIT:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        
        def update(self, index, value):
            while index <= self.n:
                self.tree[index] += value
                index += index & -index
        
        def query(self, index):
            result = 0
            while index > 0:
                result += self.tree[index]
                index -= index & -index
            return result
        
        def range_query(self, left, right):
            return self.query(right) - self.query(left - 1)
    
    bit = BIT(n)
    
    # Initialize BIT with array values
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    results = []
    
    for query in queries:
        if query[0] == 1:  # Range update
            a, b, x = query[1], query[2], query[3]
            for i in range(a, b + 1):
                bit.update(i, x)
        else:  # Sum query
            a, b = query[1], query[2]
            total = bit.range_query(a, b)
            results.append(total)
    
    return results
```

## 🔗 Related Problems

- **[Static Range Sum Queries](/cses-analyses/problem_soulutions/range_queries/static_range_sum_queries_analysis/)**: Static range sum problems
- **[Dynamic Range Sum Queries](/cses-analyses/problem_soulutions/range_queries/dynamic_range_sum_queries_analysis/)**: Dynamic range sum problems
- **[Range Update Queries](/cses-analyses/problem_soulutions/range_queries/range_update_queries_analysis/)**: Range update problems
- **[Range Queries](/cses-analyses/problem_soulutions/range_queries/)**: Range query problems

## 📚 Learning Points

1. **Dynamic Range Queries**: Essential for analyzing range sum problems with updates
2. **Binary Indexed Tree**: Key data structure for efficient range queries
3. **Prefix Sums**: Foundation for range sum calculations
4. **Update Operations**: Important for maintaining data structure consistency
5. **Query Optimization**: Critical for competitive programming performance
6. **Data Structures**: Foundation for many optimization problems

## 📝 Summary

The Prefix Sum Queries problem demonstrates fundamental dynamic range query concepts for analyzing range sum problems with updates. We explored three approaches:

1. **Brute Force Array Updates**: O(q × n) time complexity using direct array updates, inefficient for large inputs
2. **Prefix Sum Array**: O(q × n) time complexity using prefix sum rebuilding, better approach for static arrays
3. **Binary Indexed Tree**: O(q × log n) time complexity using BIT operations, optimal approach for dynamic range queries

The key insights include understanding dynamic range queries as optimization problems, using Binary Indexed Trees for efficient updates and queries, and applying prefix sum concepts for range calculations. This problem serves as an excellent introduction to dynamic range query algorithms and data structure optimization techniques.

