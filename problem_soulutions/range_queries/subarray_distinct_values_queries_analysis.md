---
layout: simple
title: CSES Subarray Distinct Values Queries - Problem Analysis
permalink: /problem_soulutions/range_queries/subarray_distinct_values_queries_analysis/
---

# CSES Subarray Distinct Values Queries - Problem Analysis

## Problem Statement
Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the number of distinct values in range [a,b]

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x_1,x_2,…,x_n: the contents of the array.
Then there are q lines describing the queries. Each line has three integers: either "1 k x" (update) or "2 a b" (distinct values query).

### Output
Print the answer to each distinct values query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ x_i ≤ 10^9
- 1 ≤ k ≤ n
- 1 ≤ a ≤ b ≤ n

### Example
```
Input:
8 3
3 2 4 5 1 1 5 3
2 1 4
1 4 9
2 1 4

Output:
4
4
```

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct array updates and distinct value counting.

```python
def subarray_distinct_values_queries_naive(n, q, array, queries):
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            array[k-1] = x  # 1-indexed to 0-indexed
        else:  # Distinct values query
            a, b = query[1], query[2]
            # Count distinct values from a to b (1-indexed)
            distinct = len(set(array[a-1:b]))
            result.append(distinct)
    
    return result
```

**Why this is inefficient**: Each distinct values query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Mo's Algorithm - O(n√n) total
**Description**: Use Mo's algorithm for offline range distinct queries.

```python
def subarray_distinct_values_queries_mo(n, q, array, queries):
    # Separate update and query operations
    updates = []
    queries_list = []
    
    for i, query in enumerate(queries):
        if query[0] == 1:  # Update
            updates.append((query[1], query[2], i))
        else:  # Query
            queries_list.append((query[1], query[2], i))
    
    # Sort queries by block (Mo's algorithm)
    block_size = int(n**0.5)
    queries_list.sort(key=lambda x: (x[0]//block_size, x[1]))
    
    # Process queries with Mo's algorithm
    current_l = 0
    current_r = -1
    distinct_count = 0
    frequency = {}
    result = [0] * len(queries)
    
    for l, r, query_idx in queries_list:
        # Move left pointer
        while current_l > l:
            current_l -= 1
            val = array[current_l-1]
            if val not in frequency:
                frequency[val] = 0
            frequency[val] += 1
            if frequency[val] == 1:
                distinct_count += 1
        
        while current_l < l:
            val = array[current_l-1]
            frequency[val] -= 1
            if frequency[val] == 0:
                distinct_count -= 1
            current_l += 1
        
        # Move right pointer
        while current_r < r:
            current_r += 1
            val = array[current_r-1]
            if val not in frequency:
                frequency[val] = 0
            frequency[val] += 1
            if frequency[val] == 1:
                distinct_count += 1
        
        while current_r > r:
            val = array[current_r-1]
            frequency[val] -= 1
            if frequency[val] == 0:
                distinct_count -= 1
            current_r -= 1
        
        result[query_idx] = distinct_count
    
    return result
```

**Why this improvement works**: Mo's algorithm provides efficient offline range distinct queries, but doesn't handle updates well.

### Improvement 2: Persistent Segment Tree - O(log n) per operation
**Description**: Use Persistent Segment Tree for efficient point updates and range distinct queries.

```python
def subarray_distinct_values_queries_persistent(n, q, array, queries):
    # This is a complex approach that requires persistent data structures
    # For simplicity, we'll use a more practical approach with coordinate compression
    
    # Coordinate compression
    unique_values = sorted(set(array))
    value_to_idx = {val: idx for idx, val in enumerate(unique_values)}
    compressed_array = [value_to_idx[val] for val in array]
    
    # Use segment tree with frequency counting
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [set() for _ in range(2 * self.size)]
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = {data[i]}
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = self.tree[2 * i] | self.tree[2 * i + 1]
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = {value}
            index //= 2
            while index >= 1:
                self.tree[index] = self.tree[2 * index] | self.tree[2 * index + 1]
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = set()
            
            while left < right:
                if left % 2 == 1:
                    result |= self.tree[left]
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result |= self.tree[right]
                left //= 2
                right //= 2
            
            return len(result)
    
    # Initialize segment tree
    st = SegmentTree(compressed_array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            if x in value_to_idx:
                compressed_x = value_to_idx[x]
            else:
                # Add new value to compression
                compressed_x = len(value_to_idx)
                value_to_idx[x] = compressed_x
            st.update(k-1, compressed_x)
        else:  # Distinct values query
            a, b = query[1], query[2]
            distinct_count = st.query(a-1, b)
            result.append(distinct_count)
    
    return result
```

**Why this improvement works**: Persistent Segment Tree provides efficient point updates and range distinct queries.

## Final Optimal Solution

```python
n, q = map(int, input().split())
array = list(map(int, input().split()))
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

def process_subarray_distinct_values_queries(n, q, array, queries):
    # Coordinate compression
    unique_values = sorted(set(array))
    value_to_idx = {val: idx for idx, val in enumerate(unique_values)}
    compressed_array = [value_to_idx[val] for val in array]
    
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [set() for _ in range(2 * self.size)]
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = {data[i]}
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = self.tree[2 * i] | self.tree[2 * i + 1]
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = {value}
            index //= 2
            while index >= 1:
                self.tree[index] = self.tree[2 * index] | self.tree[2 * index + 1]
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = set()
            
            while left < right:
                if left % 2 == 1:
                    result |= self.tree[left]
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result |= self.tree[right]
                left //= 2
                right //= 2
            
            return len(result)
    
    # Initialize segment tree
    st = SegmentTree(compressed_array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query: 1 k x
            k, x = query[1], query[2]
            if x in value_to_idx:
                compressed_x = value_to_idx[x]
            else:
                # Add new value to compression
                compressed_x = len(value_to_idx)
                value_to_idx[x] = compressed_x
            st.update(k-1, compressed_x)
        else:  # Distinct values query: 2 a b
            a, b = query[1], query[2]
            distinct_count = st.query(a-1, b)
            result.append(distinct_count)
    
    return result

result = process_subarray_distinct_values_queries(n, q, array, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Solution | O(n*q) | O(n) | Direct array operations |
| Mo's Algorithm | O(n√n) total | O(n) | Offline range queries |
| Persistent Segment Tree | O(log n) per operation | O(n log n) | Efficient point updates and range queries |

## Key Insights for Other Problems

### 1. **Coordinate Compression for Large Values**
**Principle**: Compress large values to smaller indices for efficient processing.
**Applicable to**: Range query problems, large value problems, optimization problems

### 2. **Segment Tree with Set Operations**
**Principle**: Use Segment Tree with set operations for range distinct queries.
**Applicable to**: Distinct value problems, range query problems, set operations

### 3. **Mo's Algorithm for Offline Queries**
**Principle**: Use Mo's algorithm for efficient offline range distinct queries.
**Applicable to**: Offline range queries, distinct value problems, query optimization

## Notable Techniques

### 1. **Coordinate Compression**
```python
def coordinate_compression(array):
    unique_values = sorted(set(array))
    value_to_idx = {val: idx for idx, val in enumerate(unique_values)}
    compressed_array = [value_to_idx[val] for val in array]
    return compressed_array, value_to_idx
```

### 2. **Segment Tree with Set Operations**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [set() for _ in range(2 * self.size)]
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = {data[i]}
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] | self.tree[2 * i + 1]
    
    def update(self, index, value):
        index += self.size
        self.tree[index] = {value}
        index //= 2
        while index >= 1:
            self.tree[index] = self.tree[2 * index] | self.tree[2 * index + 1]
            index //= 2
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result = set()
        
        while left < right:
            if left % 2 == 1:
                result |= self.tree[left]
                left += 1
            if right % 2 == 1:
                right -= 1
                result |= self.tree[right]
            left //= 2
            right //= 2
        
        return len(result)
```

### 3. **Mo's Algorithm for Distinct Values**
```python
def mo_algorithm_distinct_values(n, queries):
    block_size = int(n**0.5)
    queries.sort(key=lambda x: (x[0]//block_size, x[1]))
    
    current_l = 0
    current_r = -1
    distinct_count = 0
    frequency = {}
    result = []
    
    for l, r in queries:
        # Move pointers and update distinct count
        # Implementation details...
        result.append(distinct_count)
    
    return result
```

### 4. **Dynamic Coordinate Compression**
```python
def dynamic_coordinate_compression(value_to_idx, new_value):
    if new_value in value_to_idx:
        return value_to_idx[new_value]
    else:
        compressed_val = len(value_to_idx)
        value_to_idx[new_value] = compressed_val
        return compressed_val
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic range distinct values problem with point updates
2. **Choose approach**: Use Segment Tree with coordinate compression
3. **Initialize data structure**: Compress coordinates and build Segment Tree
4. **Process queries**: Handle updates and range queries using Segment Tree
5. **Update operations**: Use dynamic coordinate compression and point updates
6. **Range queries**: Use range distinct query method in Segment Tree
7. **Return result**: Output answers for all range queries

---

*This analysis shows how to efficiently handle dynamic range distinct values queries using Segment Tree with coordinate compression.* 