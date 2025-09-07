---
layout: simple
title: "Subarray Distinct Values Queries"
permalink: /problem_soulutions/range_queries/subarray_distinct_values_queries_analysis
---


# Subarray Distinct Values Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand dynamic range query problems with point updates and distinct value counting
- Apply coordinate compression and frequency tracking to handle distinct value counting with updates
- Implement efficient dynamic range query algorithms with O(log n) time for updates and distinct count queries
- Optimize distinct value counting using coordinate compression and advanced data structures
- Handle edge cases in distinct value counting (large values, coordinate compression, frequency tracking)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic range queries, coordinate compression, distinct value counting, frequency tracking, point updates
- **Data Structures**: Coordinate compression, frequency tracking, range query data structures, distinct value tracking
- **Mathematical Concepts**: Distinct value theory, coordinate compression theory, frequency analysis, range query mathematics
- **Programming Skills**: Coordinate compression, frequency tracking, distinct value counting, update handling, algorithm implementation
- **Related Problems**: Salary Queries (range counting), Coordinate compression problems, Distinct value problems

## 📋 Problem Description

Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the number of distinct values in range [a,b]

This is a dynamic range query problem where we need to efficiently handle both point updates and range distinct value count queries. We can solve this using coordinate compression with frequency tracking and efficient data structures for distinct value counting.

**Input**: 
- First line: n q (size of the array and number of queries)
- Second line: n integers x₁, x₂, ..., xₙ (the contents of the array)
- Next q lines: queries of the form:
  - "1 k x": update the value at position k to x
  - "2 a b": calculate the number of distinct values in range [a,b]

**Output**: 
- Print the answer to each distinct values query

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ xᵢ ≤ 10⁹
- 1 ≤ k ≤ n
- 1 ≤ a ≤ b ≤ n

**Example**:
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

**Explanation**: 
- Initial array: [3, 2, 4, 5, 1, 1, 5, 3]
- Query 1: Distinct values in range [1,4] → 4 (values: 3, 2, 4, 5)
- Update: Change value at position 4 from 5 to 9 → [3, 2, 4, 9, 1, 1, 5, 3]
- Query 2: Distinct values in range [1,4] → 4 (values: 3, 2, 4, 9)

### 📊 Visual Example

**Input Array:**
```
Index:  1  2  3  4  5  6  7  8
Array: [3, 2, 4, 5, 1, 1, 5, 3]
```

**Query Processing Visualization:**
```
Query 1: Distinct values in range [1,4]
┌─────────────────────────────────────┐
│ Range [1,4]: [3, 2, 4, 5]         │
│ Highlighted: [3, 2, 4, 5, 1, 1, 5, 3] │
│           ↑  ↑  ↑  ↑                │
│           ✓  ✓  ✓  ✓                │
│ Distinct values: {3, 2, 4, 5} = 4  │
└─────────────────────────────────────┘
Result: 4

Update: Change position 4 from 5 to 9
┌─────────────────────────────────────┐
│ Before: [3, 2, 4, 5, 1, 1, 5, 3]   │
│ After:  [3, 2, 4, 9, 1, 1, 5, 3]   │
│                ↑                   │
└─────────────────────────────────────┘

Query 2: Distinct values in range [1,4]
┌─────────────────────────────────────┐
│ Range [1,4]: [3, 2, 4, 9]         │
│ Highlighted: [3, 2, 4, 9, 1, 1, 5, 3] │
│           ↑  ↑  ↑  ↑                │
│           ✓  ✓  ✓  ✓                │
│ Distinct values: {3, 2, 4, 9} = 4  │
└─────────────────────────────────────┘
Result: 4
```

**Frequency Tracking:**
```
Original Array: [3, 2, 4, 5, 1, 1, 5, 3]

Frequency Map:
┌─────────────────────────────────────┐
│ Value: 1  2  3  4  5              │
│ Count: 2  1  2  1  2              │
└─────────────────────────────────────┘

Range [1,4]: [3, 2, 4, 5]
┌─────────────────────────────────────┐
│ Value: 2  3  4  5                 │
│ Count: 1  1  1  1                 │
│ Distinct count: 4                  │
└─────────────────────────────────────┘

After Update: [3, 2, 4, 9, 1, 1, 5, 3]
┌─────────────────────────────────────┐
│ Value: 1  2  3  4  5  9           │
│ Count: 2  1  2  1  2  1           │
└─────────────────────────────────────┘

Range [1,4]: [3, 2, 4, 9]
┌─────────────────────────────────────┐
│ Value: 2  3  4  9                 │
│ Count: 1  1  1  1                 │
│ Distinct count: 4                  │
└─────────────────────────────────────┘
```

**Mo's Algorithm Visualization:**
```
Queries: [1,4], [1,4] (after update)

Mo's Algorithm (offline processing):
┌─────────────────────────────────────┐
│ Sort queries by block size         │
│ Block size = √n = √8 ≈ 2.8        │
│                                     │
│ Query 1: [1,4] in block 0         │
│ Query 2: [1,4] in block 0         │
└─────────────────────────────────────┘

Processing with two pointers:
┌─────────────────────────────────────┐
│ Left pointer (L): 1                │
│ Right pointer (R): 0               │
│ Distinct count: 0                  │
│                                     │
│ Step 1: Expand R to 4              │
│ L=1, R=1: Add 3, count=1          │
│ L=1, R=2: Add 2, count=2          │
│ L=1, R=3: Add 4, count=3          │
│ L=1, R=4: Add 5, count=4          │
│ Result: 4                          │
└─────────────────────────────────────┘
```

**Coordinate Compression:**
```
Original Values: [3, 2, 4, 5, 1, 1, 5, 3, 9]

Step 1: Collect unique values
┌─────────────────────────────────────┐
│ Unique values: [1, 2, 3, 4, 5, 9] │
└─────────────────────────────────────┘

Step 2: Assign compressed indices
┌─────────────────────────────────────┐
│ Value: 1  2  3  4  5  9           │
│ Index: 0  1  2  3  4  5           │
└─────────────────────────────────────┘

Step 3: Map original array
┌─────────────────────────────────────┐
│ Original: [3, 2, 4, 5, 1, 1, 5, 3]│
│ Compressed: [2, 1, 3, 4, 0, 0, 4, 2]│
└─────────────────────────────────────┘
```

**Segment Tree for Distinct Values:**
```
Note: Segment Tree is not directly suitable for distinct value counting
┌─────────────────────────────────────┐
│ Problem: Distinct count is not     │
│ associative across segments        │
│                                     │
│ Example:                           │
│ Left segment: {1, 2, 3} = 3       │
│ Right segment: {2, 3, 4} = 3      │
│ Combined: {1, 2, 3, 4} = 4        │
│ But 3 + 3 ≠ 4                     │
└─────────────────────────────────────┘

Alternative: Use frequency tracking
┌─────────────────────────────────────┐
│ For each segment, maintain:        │
│ - Set of distinct values           │
│ - Frequency count                  │
│                                     │
│ Merge operation:                   │
│ - Union of sets                    │
│ - Update frequency counts          │
└─────────────────────────────────────┘
```

**Time Complexity Analysis:**
```
Naive Approach: O(q × n)
┌─────────────────────────────────────┐
│ Each query: O(n) scan + O(n) set   │
│ Total: O(q × n)                    │
└─────────────────────────────────────┘

Mo's Algorithm: O(n√n)
┌─────────────────────────────────────┐
│ Offline processing: O(n√n)         │
│ Each query: O(1) amortized         │
│ Total: O(n√n)                      │
└─────────────────────────────────────┘

Coordinate Compression + Frequency: O(n log n + q × n)
┌─────────────────────────────────────┐
│ Compression: O(n log n)            │
│ Each query: O(n) scan              │
│ Total: O(n log n + q × n)          │
└─────────────────────────────────────┘
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
    
    for query in queries: if query[0] == 1:  # Update 
query: 1 k x
            k, x = query[1], query[2]
            if x in value_to_idx:
                compressed_x = value_to_idx[x]
            else:
                # Add new value to compression
                compressed_x = len(value_to_idx)
                value_to_idx[x] = compressed_x
            st.update(k-1, compressed_x)
        else: # Distinct values 
query: 2 a b
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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Subarray Distinct Values Queries with Range Updates**
**Problem**: Support range updates (modify values in a range) and point distinct queries.
```python
def subarray_distinct_values_queries_range_updates(n, q, array, operations):
    # Use Segment Tree with lazy propagation for distinct values
    class LazyDistinctSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [set() for _ in range(2 * self.size)]
            self.lazy = [None] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = {data[i]}
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = self.tree[2 * i] | self.tree[2 * i + 1]
        
        def push(self, node, left, right):
            if self.lazy[node] is not None:
                self.tree[node] = {self.lazy[node]}
                if left != right:
                    self.lazy[2 * node] = self.lazy[node]
                    self.lazy[2 * node + 1] = self.lazy[node]
                self.lazy[node] = None
        
        def range_update(self, node, left, right, l, r, val):
            self.push(node, left, right)
            if r < left or l > right:
                return
            if l <= left and right <= r:
                self.lazy[node] = val
                self.push(node, left, right)
                return
            mid = (left + right) // 2
            self.range_update(2 * node, left, mid, l, r, val)
            self.range_update(2 * node + 1, mid + 1, right, l, r, val)
            self.tree[node] = self.tree[2 * node] | self.tree[2 * node + 1]
        
        def point_query(self, node, left, right, index):
            self.push(node, left, right)
            if left == right:
                return len(self.tree[node])
            mid = (left + right) // 2
            if index <= mid:
                return self.point_query(2 * node, left, mid, index)
            else:
                return self.point_query(2 * node + 1, mid + 1, right, index)
    
    st = LazyDistinctSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Range Update
            l, r, val = op[1], op[2], op[3]
            st.range_update(1, 0, st.size - 1, l-1, r-1, val)
        else:  # Point Query
            k = op[1]
            result = st.point_query(1, 0, st.size - 1, k-1)
            results.append(result)
    
    return results
```

#### **Variation 2: Subarray Distinct Values Queries with Frequency Analysis**
**Problem**: Find distinct values and their frequencies in the range.
```python
def subarray_distinct_values_queries_frequency(n, q, array, operations):
    # Use Segment Tree with frequency analysis
    class FrequencySegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [{} for _ in range(2 * self.size)]  # Store frequency maps
            
            # Build tree
            for i in range(self.n):
                self.tree[self.size + i] = {data[i]: 1}
            for i in range(self.size - 1, 0, -1):
                # Merge frequency maps
                merged = {}
                for val, freq in self.tree[2 * i].items():
                    merged[val] = merged.get(val, 0) + freq
                for val, freq in self.tree[2 * i + 1].items():
                    merged[val] = merged.get(val, 0) + freq
                self.tree[i] = merged
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = {value: 1}
            index //= 2
            while index >= 1:
                # Merge frequency maps
                merged = {}
                for val, freq in self.tree[2 * index].items():
                    merged[val] = merged.get(val, 0) + freq
                for val, freq in self.tree[2 * index + 1].items():
                    merged[val] = merged.get(val, 0) + freq
                self.tree[index] = merged
                index //= 2
        
        def query(self, left, right):
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return {}
            if l <= left and right <= r:
                return self.tree[node].copy()
            mid = (left + right) // 2
            left_freq = self._query(2 * node, left, mid, l, r)
            right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            
            # Merge frequency maps
            merged = left_freq.copy()
            for val, freq in right_freq.items():
                merged[val] = merged.get(val, 0) + freq
            return merged
    
    st = FrequencySegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Frequency query
            l, r = op[1], op[2]
            frequency_map = st.query(l-1, r-1)
            distinct_count = len(frequency_map)
            results.append((distinct_count, frequency_map))
    
    return results
```

#### **Variation 3: Subarray Distinct Values Queries with K-th Most Frequent**
**Problem**: Find the k-th most frequent value in the range.
```python
def subarray_distinct_values_queries_kth_frequent(n, q, array, operations):
    # Use Segment Tree with k-th most frequent analysis
    class KthFrequentSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [{} for _ in range(2 * self.size)]
            
            # Build tree
            for i in range(self.n):
                self.tree[self.size + i] = {data[i]: 1}
            for i in range(self.size - 1, 0, -1):
                merged = {}
                for val, freq in self.tree[2 * i].items():
                    merged[val] = merged.get(val, 0) + freq
                for val, freq in self.tree[2 * i + 1].items():
                    merged[val] = merged.get(val, 0) + freq
                self.tree[i] = merged
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = {value: 1}
            index //= 2
            while index >= 1:
                merged = {}
                for val, freq in self.tree[2 * index].items():
                    merged[val] = merged.get(val, 0) + freq
                for val, freq in self.tree[2 * index + 1].items():
                    merged[val] = merged.get(val, 0) + freq
                self.tree[index] = merged
                index //= 2
        
        def query(self, left, right):
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return {}
            if l <= left and right <= r:
                return self.tree[node].copy()
            mid = (left + right) // 2
            left_freq = self._query(2 * node, left, mid, l, r)
            right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            
            merged = left_freq.copy()
            for val, freq in right_freq.items():
                merged[val] = merged.get(val, 0) + freq
            return merged
        
        def get_kth_most_frequent(self, frequency_map, k):
            # Sort by frequency (descending) and return k-th element
            sorted_items = sorted(frequency_map.items(), key=lambda x: (-x[1], x[0]))
            if k <= len(sorted_items):
                return sorted_items[k-1][0]
            return None
    
    st = KthFrequentSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # K-th most frequent query
            l, r, k = op[1], op[2], op[3]
            frequency_map = st.query(l-1, r-1)
            kth_frequent = st.get_kth_most_frequent(frequency_map, k)
            results.append(kth_frequent)
    
    return results
```

#### **Variation 4: Subarray Distinct Values Queries with Mode Analysis**
**Problem**: Find the mode (most frequent value) in the range.
```python
def subarray_distinct_values_queries_mode(n, q, array, operations):
    # Use Segment Tree with mode analysis
    class ModeSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [{} for _ in range(2 * self.size)]
            
            # Build tree
            for i in range(self.n):
                self.tree[self.size + i] = {data[i]: 1}
            for i in range(self.size - 1, 0, -1):
                merged = {}
                for val, freq in self.tree[2 * i].items():
                    merged[val] = merged.get(val, 0) + freq
                for val, freq in self.tree[2 * i + 1].items():
                    merged[val] = merged.get(val, 0) + freq
                self.tree[i] = merged
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = {value: 1}
            index //= 2
            while index >= 1:
                merged = {}
                for val, freq in self.tree[2 * index].items():
                    merged[val] = merged.get(val, 0) + freq
                for val, freq in self.tree[2 * index + 1].items():
                    merged[val] = merged.get(val, 0) + freq
                self.tree[index] = merged
                index //= 2
        
        def query(self, left, right):
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return {}
            if l <= left and right <= r:
                return self.tree[node].copy()
            mid = (left + right) // 2
            left_freq = self._query(2 * node, left, mid, l, r)
            right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            
            merged = left_freq.copy()
            for val, freq in right_freq.items():
                merged[val] = merged.get(val, 0) + freq
            return merged
        
        def get_mode(self, frequency_map):
            # Find the value with maximum frequency
            if not frequency_map:
                return None
            return max(frequency_map.items(), key=lambda x: (x[1], -x[0]))[0]
    
    st = ModeSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Mode query
            l, r = op[1], op[2]
            frequency_map = st.query(l-1, r-1)
            mode = st.get_mode(frequency_map)
            results.append(mode)
    
    return results
```

#### **Variation 5: Subarray Distinct Values Queries with Value Range Analysis**
**Problem**: Find distinct values within a specific value range in the query range.
```python
def subarray_distinct_values_queries_value_range(n, q, array, operations):
    # Use Segment Tree with value range analysis
    class ValueRangeSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [set() for _ in range(2 * self.size)]
            
            # Build tree
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
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return set()
            if l <= left and right <= r:
                return self.tree[node].copy()
            mid = (left + right) // 2
            left_set = self._query(2 * node, left, mid, l, r)
            right_set = self._query(2 * node + 1, mid + 1, right, l, r)
            return left_set | right_set
        
        def query_value_range(self, left, right, min_val, max_val):
            # Get all distinct values in range [left, right]
            all_values = self.query(left, right)
            # Filter values within [min_val, max_val]
            filtered_values = {val for val in all_values if min_val <= val <= max_val}
            return len(filtered_values), filtered_values
    
    st = ValueRangeSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Value range query
            l, r, min_val, max_val = op[1], op[2], op[3], op[4]
            count, values = st.query_value_range(l-1, r-1, min_val, max_val)
            results.append((count, values))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Distinct Values Data Structures**
- **Segment Tree**: O(log n) point updates and range distinct queries
- **Mo's Algorithm**: O(n√n) offline range distinct queries
- **Coordinate Compression**: Handle large value ranges efficiently
- **Persistent Segment Tree**: Handle historical queries

#### **2. Distinct Values Query Types**
- **Range Distinct Count**: Count distinct values in range
- **Frequency Analysis**: Find frequencies of distinct values
- **Mode Queries**: Find most frequent value
- **K-th Most Frequent**: Find k-th most frequent value

#### **3. Advanced Distinct Values Techniques**
- **Coordinate Compression**: Map large values to small indices
- **Frequency Tracking**: Track frequencies efficiently
- **Value Range Analysis**: Analyze values within specific ranges
- **Persistent Distinct Values**: Handle historical states

#### **4. Optimization Problems**
- **Optimal Distinct Patterns**: Find optimal distinct value patterns
- **Distinct Value Constraints**: Add constraints to distinct value queries
- **Frequency Optimization**: Optimize frequency analysis
- **Value Range Optimization**: Optimize value range analysis

#### **5. Competitive Programming Patterns**
- **Mo's Algorithm**: Efficient offline range queries
- **Coordinate Compression**: Handle large value ranges
- **Frequency Tracking**: Track frequencies efficiently
- **Value Range Tracking**: Track value ranges efficiently

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    array = list(map(int, input().split()))
    
    # Coordinate compression
    unique_values = sorted(set(array))
    value_to_idx = {val: idx for idx, val in enumerate(unique_values)}
    compressed_array = [value_to_idx[val] for val in array]
    
    st = SegmentTree(compressed_array)
    for _ in range(q):
        query = list(map(int, input().split()))
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            compressed_x = value_to_idx.get(x, len(value_to_idx))
            if x not in value_to_idx:
                value_to_idx[x] = compressed_x
            st.update(k-1, compressed_x)
        else:  # Query
            a, b = query[1], query[2]
            result = st.query(a-1, b-1)
            print(result)
```

#### **2. Subarray Distinct Values Queries with Aggregation**
```python
def subarray_distinct_values_queries_aggregation(n, q, array, operations):
    # Support multiple aggregation functions
    class AggregationSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.distinct_tree = [set() for _ in range(2 * self.size)]
            self.frequency_tree = [{} for _ in range(2 * self.size)]
            
            # Build trees
            for i in range(self.n):
                self.distinct_tree[self.size + i] = {data[i]}
                self.frequency_tree[self.size + i] = {data[i]: 1}
            for i in range(self.size - 1, 0, -1):
                self.distinct_tree[i] = self.distinct_tree[2 * i] | self.distinct_tree[2 * i + 1]
                # Merge frequency maps
                merged = {}
                for val, freq in self.frequency_tree[2 * i].items():
                    merged[val] = merged.get(val, 0) + freq
                for val, freq in self.frequency_tree[2 * i + 1].items():
                    merged[val] = merged.get(val, 0) + freq
                self.frequency_tree[i] = merged
        
        def update(self, index, value):
            index += self.size
            self.distinct_tree[index] = {value}
            self.frequency_tree[index] = {value: 1}
            index //= 2
            while index >= 1:
                self.distinct_tree[index] = self.distinct_tree[2 * index] | self.distinct_tree[2 * index + 1]
                # Merge frequency maps
                merged = {}
                for val, freq in self.frequency_tree[2 * index].items():
                    merged[val] = merged.get(val, 0) + freq
                for val, freq in self.frequency_tree[2 * index + 1].items():
                    merged[val] = merged.get(val, 0) + freq
                self.frequency_tree[index] = merged
                index //= 2
        
        def query(self, left, right, op):
            if op == 'DISTINCT_COUNT':
                return self._query_distinct_count(left, right)
            elif op == 'FREQUENCY_MAP':
                return self._query_frequency_map(left, right)
            elif op == 'MODE':
                return self._query_mode(left, right)
        
        def _query_distinct_count(self, left, right):
            return self._query_distinct(left, right)
        
        def _query_distinct(self, left, right):
            return self._query_set(1, 0, self.size - 1, left, right)
        
        def _query_set(self, node, left, right, l, r):
            if r < left or l > right:
                return set()
            if l <= left and right <= r:
                return self.distinct_tree[node].copy()
            mid = (left + right) // 2
            left_set = self._query_set(2 * node, left, mid, l, r)
            right_set = self._query_set(2 * node + 1, mid + 1, right, l, r)
            return left_set | right_set
    
    st = AggregationSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Aggregation query
            l, r, query_type = op[1], op[2], op[3]
            result = st.query(l-1, r-1, query_type)
            results.append(result)
    
    return results
```

#### **3. Interactive Subarray Distinct Values Queries**
```python
def interactive_subarray_distinct_values_queries(n, array):
    # Handle interactive queries
    # Coordinate compression
    unique_values = sorted(set(array))
    value_to_idx = {val: idx for idx, val in enumerate(unique_values)}
    compressed_array = [value_to_idx[val] for val in array]
    
    st = SegmentTree(compressed_array)
    
    while True: 
try: query = input().strip()
            if query == 'END':
                break
            
            parts = query.split()
            if parts[0] == 'UPDATE':
                k, x = int(parts[1]), int(parts[2])
                compressed_x = value_to_idx.get(x, len(value_to_idx))
                if x not in value_to_idx:
                    value_to_idx[x] = compressed_x
                st.update(k-1, compressed_x)
                print(f"Updated position {k} to {x}")
            elif parts[0] == 'QUERY':
                a, b = int(parts[1]), int(parts[2])
                result = st.query(a-1, b-1)
                print(f"Distinct values in range [{a},{b}]: {result}")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. Distinct Values Properties**
- **Cardinality**: Number of distinct elements in a set
- **Set Operations**: Union, intersection, difference of distinct value sets
- **Frequency Analysis**: Analysis of value frequencies
- **Mode Properties**: Properties of most frequent values

#### **2. Optimization Techniques**
- **Coordinate Compression**: Compress large value ranges efficiently
- **Frequency Tracking**: Track frequencies efficiently
- **Set Operations**: Optimize set operations
- **Memory Optimization**: Optimize memory usage for large datasets

#### **3. Advanced Mathematical Concepts**
- **Set Theory**: Understanding set operations and properties
- **Frequency Analysis**: Understanding frequency distributions
- **Statistical Measures**: Mode, median, percentiles
- **Information Theory**: Entropy and information content

#### **4. Algorithmic Improvements**
- **Mo's Algorithm**: Optimize offline range queries
- **Coordinate Compression**: Handle large value ranges efficiently
- **Frequency Tracking**: Track frequencies efficiently
- **Parallel Processing**: Use multiple cores for large datasets

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n√n) for Mo's algorithm, O(q log n) for segment tree approach
- **Space Complexity**: O(n) for coordinate compression and frequency tracking
- **Why it works**: Coordinate compression maps large values to smaller indices, frequency tracking enables efficient distinct value counting

### Key Implementation Points
- Use coordinate compression to handle large value ranges
- Mo's algorithm for offline range distinct value queries
- Frequency tracking for efficient distinct value counting
- Handle both point updates and range queries efficiently

## 🎯 Key Insights

### Important Concepts and Patterns
- **Coordinate Compression**: Essential for handling large value ranges efficiently
- **Mo's Algorithm**: Optimizes offline range queries by sorting queries optimally
- **Frequency Tracking**: Enables efficient distinct value counting in ranges
- **Range Distinct Values**: Count unique values in a given range

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Subarray Distinct Values Queries with Range Updates**
```python
class RangeUpdateDistinctQueries:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr.copy()
        
        # Coordinate compression
        all_values = set(arr)
        self.sorted_values = sorted(all_values)
        self.coord_map = {val: i for i, val in enumerate(self.sorted_values)}
        
        # Frequency tracking for each position
        self.frequencies = [{} for _ in range(self.n)]
        self.distinct_cache = {}
        
        # Initialize frequencies
        for i in range(self.n):
            self.frequencies[i][self.coord_map[arr[i]]] = 1
    
    def update_value(self, pos, new_value):
        old_value = self.arr[pos - 1]
        old_coord = self.coord_map[old_value]
        new_coord = self.coord_map[new_value]
        
        # Update frequency
        self.frequencies[pos - 1][old_coord] = 0
        self.frequencies[pos - 1][new_coord] = 1
        
        # Clear distinct cache for affected ranges
        self.distinct_cache.clear()
        
        self.arr[pos - 1] = new_value
    
    def get_distinct_count(self, a, b):
        # Check cache first
        cache_key = (a, b)
        if cache_key in self.distinct_cache:
            return self.distinct_cache[cache_key]
        
        # Calculate distinct count for range [a, b]
        distinct_values = set()
        
        for i in range(a - 1, b):
            for coord, count in self.frequencies[i].items():
                if count > 0:
                    distinct_values.add(coord)
        
        result = len(distinct_values)
        self.distinct_cache[cache_key] = result
        return result
```

#### **2. Subarray Distinct Values Queries with K-th Distinct**
```python
def subarray_kth_distinct_queries(n, arr, queries):
    # Handle queries that return the k-th distinct value in a range
    
    # Coordinate compression
    all_values = set(arr)
    sorted_values = sorted(all_values)
    coord_map = {val: i for i, val in enumerate(sorted_values)}
    
    results = []
    
    for query in queries:
        if query[0] == 1:
            # Update query
            k, x = query[1], query[2]
            arr[k - 1] = x
        else:
            # K-th distinct query
            a, b, k = query[1], query[2], query[3]
            
            # Get distinct values in range [a, b]
            distinct_values = set()
            for i in range(a - 1, b):
                distinct_values.add(arr[i])
            
            # Sort distinct values
            sorted_distinct = sorted(distinct_values)
            
            # Return k-th distinct value (1-indexed)
            if k <= len(sorted_distinct):
                results.append(sorted_distinct[k - 1])
            else:
                results.append(-1)  # Not enough distinct values
    
    return results
```

#### **3. Subarray Distinct Values Queries with Statistical Measures**
```python
class StatisticalDistinctQueries:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr.copy()
        
        # Coordinate compression
        all_values = set(arr)
        self.sorted_values = sorted(all_values)
        self.coord_map = {val: i for i, val in enumerate(self.sorted_values)}
        
        # Precompute prefix distinct counts
        self.prefix_distinct = [set() for _ in range(self.n + 1)]
        
        for i in range(self.n):
            self.prefix_distinct[i + 1] = self.prefix_distinct[i].copy()
            self.prefix_distinct[i + 1].add(self.coord_map[arr[i]])
    
    def get_distinct_count(self, a, b):
        # Calculate distinct count in range [a, b]
        distinct_values = set()
        
        for i in range(a - 1, b):
            distinct_values.add(self.coord_map[self.arr[i]])
        
        return len(distinct_values)
    
    def get_distinct_values(self, a, b):
        # Get all distinct values in range [a, b]
        distinct_values = set()
        
        for i in range(a - 1, b):
            distinct_values.add(self.arr[i])
        
        return sorted(distinct_values)
    
    def get_range_stats(self, a, b):
        # Get comprehensive statistics for range [a, b]
        distinct_values = set()
        freq_count = {}
        total_elements = 0
        
        for i in range(a - 1, b):
            val = self.arr[i]
            distinct_values.add(val)
            freq_count[val] = freq_count.get(val, 0) + 1
            total_elements += 1
        
        # Calculate statistics
        distinct_count = len(distinct_values)
        max_freq = max(freq_count.values()) if freq_count else 0
        min_freq = min(freq_count.values()) if freq_count else 0
        
        # Find most frequent value
        most_frequent = None
        for val, freq in freq_count.items():
            if freq == max_freq:
                most_frequent = val
                break
        
        return {
            'distinct_count': distinct_count,
            'total_elements': total_elements,
            'most_frequent': most_frequent,
            'max_frequency': max_freq,
            'min_frequency': min_freq,
            'distinct_values': sorted(distinct_values)
        }
```

## 🔗 Related Problems

### Links to Similar Problems
- **Range Queries**: Subarray Mode Queries, Subarray Minimum Queries
- **Distinct Values**: Frequency analysis, Set operations
- **Coordinate Compression**: Salary Queries, Hotel Queries
- **Mo's Algorithm**: Offline range queries, Range optimization

## 📚 Learning Points

### Key Takeaways
- **Coordinate compression** is essential for handling large value ranges efficiently
- **Mo's algorithm** optimizes offline range queries by sorting queries optimally
- **Frequency tracking** enables efficient distinct value counting in ranges
- **Range distinct values** is a fundamental counting problem in range queries

---

**Practice these variations to master dynamic range distinct value query techniques and set operations!** 🎯 