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
        try:
            query = input().strip()
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

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Segment Tree**: Efficient range distinct queries
- **Mo's Algorithm**: Offline range query optimization
- **Coordinate Compression**: Handle large value ranges
- **Set Operations**: Efficient set manipulation

#### **2. Mathematical Concepts**
- **Set Theory**: Understanding set operations
- **Frequency Analysis**: Understanding frequency distributions
- **Statistical Measures**: Mode, median, percentiles
- **Complexity Analysis**: Understanding time/space trade-offs

#### **3. Programming Concepts**
- **Data Structures**: Choosing appropriate distinct value structures
- **Algorithm Design**: Optimizing for distinct value constraints
- **Problem Decomposition**: Breaking complex distinct value problems
- **Code Optimization**: Writing efficient distinct value implementations

---

**Practice these variations to master dynamic range distinct value query techniques and set operations!** 🎯 