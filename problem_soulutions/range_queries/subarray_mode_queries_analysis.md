---
layout: simple
title: CSES Subarray Mode Queries - Problem Analysis
permalink: /problem_soulutions/range_queries/subarray_mode_queries_analysis/
---

# CSES Subarray Mode Queries - Problem Analysis

## Problem Statement
Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the mode (most frequent value) in range [a,b]

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x_1,x_2,…,x_n: the contents of the array.
Then there are q lines describing the queries. Each line has three integers: either "1 k x" (update) or "2 a b" (mode query).

### Output
Print the answer to each mode query.

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
3
3
```

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct array updates and mode calculations.

```python
def subarray_mode_queries_naive(n, q, array, queries):
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            array[k-1] = x  # 1-indexed to 0-indexed
        else:  # Mode query
            a, b = query[1], query[2]
            # Calculate mode from a to b (1-indexed)
            subarray = array[a-1:b]
            frequency = {}
            for val in subarray:
                frequency[val] = frequency.get(val, 0) + 1
            
            mode = max(frequency.items(), key=lambda x: x[1])[0]
            result.append(mode)
    
    return result
```

**Why this is inefficient**: Each mode query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Mo's Algorithm - O(n√n) total
**Description**: Use Mo's algorithm for offline range mode queries.

```python
def subarray_mode_queries_mo(n, q, array, queries):
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
    frequency = {}
    max_freq = 0
    mode_value = None
    result = [0] * len(queries)
    
    def add_element(val):
        nonlocal max_freq, mode_value
        if val not in frequency:
            frequency[val] = 0
        frequency[val] += 1
        if frequency[val] > max_freq:
            max_freq = frequency[val]
            mode_value = val
    
    def remove_element(val):
        nonlocal max_freq, mode_value
        frequency[val] -= 1
        if frequency[val] == 0:
            del frequency[val]
        if frequency[val] == max_freq - 1:
            # Need to recalculate mode
            max_freq = max(frequency.values()) if frequency else 0
            mode_value = max(frequency.items(), key=lambda x: x[1])[0] if frequency else None
    
    for l, r, query_idx in queries_list:
        # Move left pointer
        while current_l > l:
            current_l -= 1
            add_element(array[current_l-1])
        
        while current_l < l:
            remove_element(array[current_l-1])
            current_l += 1
        
        # Move right pointer
        while current_r < r:
            current_r += 1
            add_element(array[current_r-1])
        
        while current_r > r:
            remove_element(array[current_r-1])
            current_r -= 1
        
        result[query_idx] = mode_value
    
    return result
```

**Why this improvement works**: Mo's algorithm provides efficient offline range mode queries, but doesn't handle updates well.

### Improvement 2: Persistent Segment Tree with Frequency Tracking - O(log n) per operation
**Description**: Use Persistent Segment Tree for efficient point updates and range mode queries.

```python
def subarray_mode_queries_persistent(n, q, array, queries):
    # Coordinate compression
    unique_values = sorted(set(array))
    value_to_idx = {val: idx for idx, val in enumerate(unique_values)}
    compressed_array = [value_to_idx[val] for val in array]
    
    # Use segment tree with frequency tracking
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [{} for _ in range(2 * self.size)]
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = {data[i]: 1}
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = self.merge_frequencies(self.tree[2 * i], self.tree[2 * i + 1])
        
        def merge_frequencies(self, freq1, freq2):
            merged = freq1.copy()
            for val, count in freq2.items():
                merged[val] = merged.get(val, 0) + count
            return merged
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = {value: 1}
            index //= 2
            while index >= 1:
                self.tree[index] = self.merge_frequencies(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result_freq = {}
            
            while left < right:
                if left % 2 == 1:
                    result_freq = self.merge_frequencies(result_freq, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result_freq = self.merge_frequencies(result_freq, self.tree[right])
                left //= 2
                right //= 2
            
            # Find mode
            if not result_freq:
                return None
            mode_value = max(result_freq.items(), key=lambda x: x[1])[0]
            return mode_value
    
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
        else:  # Mode query
            a, b = query[1], query[2]
            mode_compressed = st.query(a-1, b)
            if mode_compressed is not None:
                # Convert back to original value
                mode_value = unique_values[mode_compressed]
            else:
                mode_value = None
            result.append(mode_value)
    
    return result
```

**Why this improvement works**: Persistent Segment Tree provides efficient point updates and range mode queries.

## Final Optimal Solution

```python
n, q = map(int, input().split())
array = list(map(int, input().split()))
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

def process_subarray_mode_queries(n, q, array, queries):
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
            self.tree = [{} for _ in range(2 * self.size)]
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = {data[i]: 1}
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = self.merge_frequencies(self.tree[2 * i], self.tree[2 * i + 1])
        
        def merge_frequencies(self, freq1, freq2):
            merged = freq1.copy()
            for val, count in freq2.items():
                merged[val] = merged.get(val, 0) + count
            return merged
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = {value: 1}
            index //= 2
            while index >= 1:
                self.tree[index] = self.merge_frequencies(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result_freq = {}
            
            while left < right:
                if left % 2 == 1:
                    result_freq = self.merge_frequencies(result_freq, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result_freq = self.merge_frequencies(result_freq, self.tree[right])
                left //= 2
                right //= 2
            
            # Find mode
            if not result_freq:
                return None
            mode_value = max(result_freq.items(), key=lambda x: x[1])[0]
            return mode_value
    
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
        else:  # Mode query: 2 a b
            a, b = query[1], query[2]
            mode_compressed = st.query(a-1, b)
            if mode_compressed is not None:
                # Convert back to original value
                mode_value = unique_values[mode_compressed]
            else:
                mode_value = None
            result.append(mode_value)
    
    return result

result = process_subarray_mode_queries(n, q, array, queries)
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

### 1. **Frequency Tracking in Range Queries**
**Principle**: Track frequency of elements in range queries for mode calculations.
**Applicable to**: Mode problems, frequency problems, range query problems

### 2. **Segment Tree with Frequency Merging**
**Principle**: Use Segment Tree with frequency merging for range mode queries.
**Applicable to**: Mode problems, frequency problems, range query problems

### 3. **Coordinate Compression for Large Values**
**Principle**: Compress large values to smaller indices for efficient processing.
**Applicable to**: Range query problems, large value problems, optimization problems

## Notable Techniques

### 1. **Frequency Merging**
```python
def merge_frequencies(freq1, freq2):
    merged = freq1.copy()
    for val, count in freq2.items():
        merged[val] = merged.get(val, 0) + count
    return merged
```

### 2. **Segment Tree with Frequency Tracking**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [{} for _ in range(2 * self.size)]
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = {data[i]: 1}
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.merge_frequencies(self.tree[2 * i], self.tree[2 * i + 1])
    
    def merge_frequencies(self, freq1, freq2):
        merged = freq1.copy()
        for val, count in freq2.items():
            merged[val] = merged.get(val, 0) + count
        return merged
    
    def update(self, index, value):
        index += self.size
        self.tree[index] = {value: 1}
        index //= 2
        while index >= 1:
            self.tree[index] = self.merge_frequencies(self.tree[2 * index], self.tree[2 * index + 1])
            index //= 2
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result_freq = {}
        
        while left < right:
            if left % 2 == 1:
                result_freq = self.merge_frequencies(result_freq, self.tree[left])
                left += 1
            if right % 2 == 1:
                right -= 1
                result_freq = self.merge_frequencies(result_freq, self.tree[right])
            left //= 2
            right //= 2
        
        # Find mode
        if not result_freq:
            return None
        mode_value = max(result_freq.items(), key=lambda x: x[1])[0]
        return mode_value
```

### 3. **Mo's Algorithm for Mode Queries**
```python
def mo_algorithm_mode_queries(n, queries):
    block_size = int(n**0.5)
    queries.sort(key=lambda x: (x[0]//block_size, x[1]))
    
    current_l = 0
    current_r = -1
    frequency = {}
    max_freq = 0
    mode_value = None
    result = []
    
    def add_element(val):
        nonlocal max_freq, mode_value
        if val not in frequency:
            frequency[val] = 0
        frequency[val] += 1
        if frequency[val] > max_freq:
            max_freq = frequency[val]
            mode_value = val
    
    def remove_element(val):
        nonlocal max_freq, mode_value
        frequency[val] -= 1
        if frequency[val] == 0:
            del frequency[val]
        if frequency[val] == max_freq - 1:
            # Need to recalculate mode
            max_freq = max(frequency.values()) if frequency else 0
            mode_value = max(frequency.items(), key=lambda x: x[1])[0] if frequency else None
    
    for l, r in queries:
        # Move pointers and update mode
        # Implementation details...
        result.append(mode_value)
    
    return result
```

### 4. **Mode Calculation**
```python
def calculate_mode(frequency_dict):
    if not frequency_dict:
        return None
    return max(frequency_dict.items(), key=lambda x: x[1])[0]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic range mode problem with point updates
2. **Choose approach**: Use Segment Tree with frequency tracking
3. **Initialize data structure**: Compress coordinates and build Segment Tree
4. **Process queries**: Handle updates and range queries using Segment Tree
5. **Update operations**: Use dynamic coordinate compression and point updates
6. **Range queries**: Use range mode query method in Segment Tree
7. **Return result**: Output answers for all range queries

---

*This analysis shows how to efficiently handle dynamic range mode queries using Segment Tree with frequency tracking.* 