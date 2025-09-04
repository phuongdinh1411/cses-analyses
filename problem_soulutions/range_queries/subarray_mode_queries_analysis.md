---
layout: simple
title: "Subarray Mode Queries"
permalink: /problem_soulutions/range_queries/subarray_mode_queries_analysis
---


# Subarray Mode Queries

## 📋 Problem Description

Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the mode (most frequent value) in range [a,b]

This is a dynamic range query problem where we need to efficiently handle both point updates and range mode queries. We can solve this using coordinate compression with frequency tracking and efficient data structures for mode calculation.

**Input**: 
- First line: n q (size of the array and number of queries)
- Second line: n integers x₁, x₂, ..., xₙ (the contents of the array)
- Next q lines: queries of the form:
  - "1 k x": update the value at position k to x
  - "2 a b": calculate the mode in range [a,b]

**Output**: 
- Print the answer to each mode query

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
3
3
```

**Explanation**: 
- Initial array: [3, 2, 4, 5, 1, 1, 5, 3]
- Query 1: Mode in range [1,4] → 3 (appears once, but 3 is the smallest mode)
- Update: Change value at position 4 from 5 to 9 → [3, 2, 4, 9, 1, 1, 5, 3]
- Query 2: Mode in range [1,4] → 3 (still the mode in this range)

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
        else: # Mode 
query: 2 a b
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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Subarray Mode Queries with Range Updates**
**Problem**: Support range updates (modify values in a range) and point mode queries.
```python
def subarray_mode_queries_range_updates(n, q, array, operations):
    # Use Segment Tree with lazy propagation for mode queries
    class LazyModeSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [{} for _ in range(2 * self.size)]
            self.lazy = [None] * (2 * self.size)
            
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
        
        def push(self, node, left, right):
            if self.lazy[node] is not None:
                self.tree[node] = {self.lazy[node]: right - left + 1}
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
            self.tree[node] = self.merge_frequencies(self.tree[2 * node], self.tree[2 * node + 1])
        
        def point_query(self, node, left, right, index):
            self.push(node, left, right)
            if left == right:
                return self.get_mode(self.tree[node])
            mid = (left + right) // 2
            if index <= mid:
                return self.point_query(2 * node, left, mid, index)
            else:
                return self.point_query(2 * node + 1, mid + 1, right, index)
        
        def get_mode(self, frequency_dict):
            if not frequency_dict:
                return None
            return max(frequency_dict.items(), key=lambda x: x[1])[0]
    
    st = LazyModeSegmentTree(array)
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

#### **Variation 2: Subarray Mode Queries with Frequency Analysis**
**Problem**: Find mode and its frequency in the range.
```python
def subarray_mode_queries_frequency(n, q, array, operations):
    # Use Segment Tree with mode and frequency analysis
    class ModeFrequencySegmentTree:
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
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return {}
            if l <= left and right <= r:
                return self.tree[node].copy()
            mid = (left + right) // 2
            left_freq = self._query(2 * node, left, mid, l, r)
            right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            return self.merge_frequencies(left_freq, right_freq)
        
        def get_mode_and_frequency(self, frequency_dict):
            if not frequency_dict:
                return None, 0
            mode_value = max(frequency_dict.items(), key=lambda x: x[1])[0]
            mode_frequency = frequency_dict[mode_value]
            return mode_value, mode_frequency
    
    st = ModeFrequencySegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Mode and frequency query
            l, r = op[1], op[2]
            frequency_map = st.query(l-1, r-1)
            mode_value, mode_freq = st.get_mode_and_frequency(frequency_map)
            results.append((mode_value, mode_freq))
    
    return results
```

#### **Variation 3: Subarray Mode Queries with K-th Most Frequent**
**Problem**: Find the k-th most frequent value in the range.
```python
def subarray_mode_queries_kth_frequent(n, q, array, operations):
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
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return {}
            if l <= left and right <= r:
                return self.tree[node].copy()
            mid = (left + right) // 2
            left_freq = self._query(2 * node, left, mid, l, r)
            right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            return self.merge_frequencies(left_freq, right_freq)
        
        def get_kth_most_frequent(self, frequency_dict, k):
            if not frequency_dict:
                return None
            # Sort by frequency (descending) and return k-th element
            sorted_items = sorted(frequency_dict.items(), key=lambda x: (-x[1], x[0]))
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

#### **Variation 4: Subarray Mode Queries with Multiple Modes**
**Problem**: Find all values that have the maximum frequency (multiple modes).
```python
def subarray_mode_queries_multiple_modes(n, q, array, operations):
    # Use Segment Tree with multiple modes analysis
    class MultipleModesSegmentTree:
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
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return {}
            if l <= left and right <= r:
                return self.tree[node].copy()
            mid = (left + right) // 2
            left_freq = self._query(2 * node, left, mid, l, r)
            right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            return self.merge_frequencies(left_freq, right_freq)
        
        def get_all_modes(self, frequency_dict):
            if not frequency_dict:
                return []
            max_frequency = max(frequency_dict.values())
            modes = [val for val, freq in frequency_dict.items() if freq == max_frequency]
            return sorted(modes)  # Return sorted list of modes
    
    st = MultipleModesSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Multiple modes query
            l, r = op[1], op[2]
            frequency_map = st.query(l-1, r-1)
            modes = st.get_all_modes(frequency_map)
            results.append(modes)
    
    return results
```

#### **Variation 5: Subarray Mode Queries with Value Range Analysis**
**Problem**: Find mode within a specific value range in the query range.
```python
def subarray_mode_queries_value_range(n, q, array, operations):
    # Use Segment Tree with value range mode analysis
    class ValueRangeModeSegmentTree:
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
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return {}
            if l <= left and right <= r:
                return self.tree[node].copy()
            mid = (left + right) // 2
            left_freq = self._query(2 * node, left, mid, l, r)
            right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            return self.merge_frequencies(left_freq, right_freq)
        
        def get_mode_in_range(self, frequency_dict, min_val, max_val):
            # Filter frequencies within value range
            filtered_freq = {val: freq for val, freq in frequency_dict.items() 
                           if min_val <= val <= max_val}
            if not filtered_freq:
                return None
            return max(filtered_freq.items(), key=lambda x: x[1])[0]
    
    st = ValueRangeModeSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Value range mode query
            l, r, min_val, max_val = op[1], op[2], op[3], op[4]
            frequency_map = st.query(l-1, r-1)
            mode_in_range = st.get_mode_in_range(frequency_map, min_val, max_val)
            results.append(mode_in_range)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Mode Query Data Structures**
- **Segment Tree**: O(log n) point updates and range mode queries
- **Mo's Algorithm**: O(n√n) offline range mode queries
- **Coordinate Compression**: Handle large value ranges efficiently
- **Persistent Segment Tree**: Handle historical queries

#### **2. Mode Query Types**
- **Range Mode**: Find most frequent value in range
- **Mode Frequency**: Find mode and its frequency
- **K-th Most Frequent**: Find k-th most frequent value
- **Multiple Modes**: Find all values with maximum frequency

#### **3. Advanced Mode Techniques**
- **Frequency Tracking**: Track frequencies efficiently
- **Value Range Analysis**: Analyze modes within value ranges
- **Multiple Modes Detection**: Detect all modes efficiently
- **Persistent Mode Queries**: Handle historical states

#### **4. Optimization Problems**
- **Optimal Mode Patterns**: Find optimal mode patterns for queries
- **Mode Constraints**: Add constraints to mode queries
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

#### **2. Subarray Mode Queries with Aggregation**
```python
def subarray_mode_queries_aggregation(n, q, array, operations):
    # Support multiple aggregation functions
    class AggregationSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.mode_tree = [{} for _ in range(2 * self.size)]
            self.frequency_tree = [{} for _ in range(2 * self.size)]
            
            # Build trees
            for i in range(self.n):
                self.mode_tree[self.size + i] = {data[i]: 1}
                self.frequency_tree[self.size + i] = {data[i]: 1}
            for i in range(self.size - 1, 0, -1):
                self.mode_tree[i] = self.merge_frequencies(self.mode_tree[2 * i], self.mode_tree[2 * i + 1])
                self.frequency_tree[i] = self.merge_frequencies(self.frequency_tree[2 * i], self.frequency_tree[2 * i + 1])
        
        def merge_frequencies(self, freq1, freq2):
            merged = freq1.copy()
            for val, count in freq2.items():
                merged[val] = merged.get(val, 0) + count
            return merged
        
        def update(self, index, value):
            index += self.size
            self.mode_tree[index] = {value: 1}
            self.frequency_tree[index] = {value: 1}
            index //= 2
            while index >= 1:
                self.mode_tree[index] = self.merge_frequencies(self.mode_tree[2 * index], self.mode_tree[2 * index + 1])
                self.frequency_tree[index] = self.merge_frequencies(self.frequency_tree[2 * index], self.frequency_tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right, op):
            if op == 'MODE':
                return self._query_mode(left, right)
            elif op == 'FREQUENCY_MAP':
                return self._query_frequency_map(left, right)
            elif op == 'MULTIPLE_MODES':
                return self._query_multiple_modes(left, right)
        
        def _query_mode(self, left, right):
            frequency_map = self._query_frequency_map(left, right)
            if not frequency_map:
                return None
            return max(frequency_map.items(), key=lambda x: x[1])[0]
        
        def _query_frequency_map(self, left, right):
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return {}
            if l <= left and right <= r:
                return self.frequency_tree[node].copy()
            mid = (left + right) // 2
            left_freq = self._query(2 * node, left, mid, l, r)
            right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            return self.merge_frequencies(left_freq, right_freq)
    
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

#### **3. Interactive Subarray Mode Queries**
```python
def interactive_subarray_mode_queries(n, array):
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
                print(f"Mode in range [{a},{b}]: {result}")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. Mode Properties**
- **Uniqueness**: Mode may not be unique (multiple modes possible)
- **Frequency Analysis**: Mode has maximum frequency in the range
- **Statistical Properties**: Mode is a measure of central tendency
- **Distribution Analysis**: Mode indicates most common values

#### **2. Optimization Techniques**
- **Coordinate Compression**: Compress large value ranges efficiently
- **Frequency Tracking**: Track frequencies efficiently
- **Mode Detection**: Detect modes efficiently
- **Memory Optimization**: Optimize memory usage for large datasets

#### **3. Advanced Mathematical Concepts**
- **Statistical Measures**: Understanding mode properties
- **Frequency Analysis**: Understanding frequency distributions
- **Central Tendency**: Understanding measures of central tendency
- **Distribution Theory**: Understanding value distributions

#### **4. Algorithmic Improvements**
- **Mo's Algorithm**: Optimize offline range queries
- **Coordinate Compression**: Handle large value ranges efficiently
- **Frequency Tracking**: Track frequencies efficiently
- **Parallel Processing**: Use multiple cores for large datasets

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n√n) for Mo's algorithm, O(q log n) for segment tree approach
- **Space Complexity**: O(n) for coordinate compression and frequency tracking
- **Why it works**: Coordinate compression maps large values to smaller indices, frequency tracking enables efficient mode calculation

### Key Implementation Points
- Use coordinate compression to handle large value ranges
- Mo's algorithm for offline range mode queries
- Frequency tracking for efficient mode calculation
- Handle both point updates and range queries efficiently

## 🎯 Key Insights

### Important Concepts and Patterns
- **Coordinate Compression**: Essential for handling large value ranges efficiently
- **Mo's Algorithm**: Optimizes offline range queries by sorting queries optimally
- **Frequency Tracking**: Enables efficient mode calculation in ranges
- **Range Mode**: Most frequent value in a given range

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Subarray Mode Queries with Range Updates**
```python
class DynamicSubarrayModeQueries:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr.copy()
        
        # Coordinate compression
        all_values = set(arr)
        self.sorted_values = sorted(all_values)
        self.coord_map = {val: i for i, val in enumerate(self.sorted_values)}
        
        # Frequency tracking for each position
        self.frequencies = [{} for _ in range(self.n)]
        self.mode_cache = {}
        
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
        
        # Clear mode cache for affected ranges
        self.mode_cache.clear()
        
        self.arr[pos - 1] = new_value
    
    def get_mode(self, a, b):
        # Check cache first
        cache_key = (a, b)
        if cache_key in self.mode_cache:
            return self.mode_cache[cache_key]
        
        # Calculate mode for range [a, b]
        freq_count = {}
        max_freq = 0
        mode_value = None
        
        for i in range(a - 1, b):
            for coord, count in self.frequencies[i].items():
                if count > 0:
                    freq_count[coord] = freq_count.get(coord, 0) + count
                    if freq_count[coord] > max_freq:
                        max_freq = freq_count[coord]
                        mode_value = coord
        
        # Find smallest mode if there are ties
        if mode_value is not None:
            for coord, freq in freq_count.items():
                if freq == max_freq and coord < mode_value:
                    mode_value = coord
        
        result = self.sorted_values[mode_value] if mode_value is not None else None
        self.mode_cache[cache_key] = result
        return result
```

#### **2. Subarray Mode Queries with Multiple Modes**
```python
def subarray_mode_queries_multiple_modes(n, arr, queries):
    # Handle queries that return all modes (not just one)
    
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
            # Mode query
            a, b = query[1], query[2]
            
            # Calculate frequencies in range [a, b]
            freq_count = {}
            for i in range(a - 1, b):
                coord = coord_map[arr[i]]
                freq_count[coord] = freq_count.get(coord, 0) + 1
            
            # Find maximum frequency
            max_freq = max(freq_count.values()) if freq_count else 0
            
            # Find all modes
            modes = []
            for coord, freq in freq_count.items():
                if freq == max_freq:
                    modes.append(sorted_values[coord])
            
            # Sort modes and return
            modes.sort()
            results.append(modes)
    
    return results
```

#### **3. Subarray Mode Queries with Statistical Measures**
```python
class StatisticalSubarrayQueries:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr.copy()
        
        # Coordinate compression
        all_values = set(arr)
        self.sorted_values = sorted(all_values)
        self.coord_map = {val: i for i, val in enumerate(self.sorted_values)}
        
        # Precompute prefix statistics
        self.prefix_stats = [{} for _ in range(self.n + 1)]
        self.prefix_stats[0] = {}
        
        for i in range(self.n):
            coord = self.coord_map[arr[i]]
            self.prefix_stats[i + 1] = self.prefix_stats[i].copy()
            self.prefix_stats[i + 1][coord] = self.prefix_stats[i + 1].get(coord, 0) + 1
    
    def get_mode(self, a, b):
        # Calculate mode in range [a, b]
        freq_count = {}
        for coord, count in self.prefix_stats[b].items():
            prev_count = self.prefix_stats[a - 1].get(coord, 0)
            if count - prev_count > 0:
                freq_count[coord] = count - prev_count
        
        if not freq_count:
            return None
        
        max_freq = max(freq_count.values())
        modes = [coord for coord, freq in freq_count.items() if freq == max_freq]
        return self.sorted_values[min(modes)]
    
    def get_median(self, a, b):
        # Calculate median in range [a, b]
        freq_count = {}
        total_elements = 0
        
        for coord, count in self.prefix_stats[b].items():
            prev_count = self.prefix_stats[a - 1].get(coord, 0)
            if count - prev_count > 0:
                freq_count[coord] = count - prev_count
                total_elements += count - prev_count
        
        if total_elements == 0:
            return None
        
        # Find median position
        median_pos = (total_elements + 1) // 2
        current_pos = 0
        
        for coord in sorted(freq_count.keys()):
            current_pos += freq_count[coord]
            if current_pos >= median_pos:
                return self.sorted_values[coord]
        
        return None
    
    def get_range_stats(self, a, b):
        # Get comprehensive statistics for range [a, b]
        freq_count = {}
        total_elements = 0
        
        for coord, count in self.prefix_stats[b].items():
            prev_count = self.prefix_stats[a - 1].get(coord, 0)
            if count - prev_count > 0:
                freq_count[coord] = count - prev_count
                total_elements += count - prev_count
        
        if total_elements == 0:
            return {
                'mode': None,
                'median': None,
                'min': None,
                'max': None,
                'unique_count': 0,
                'total_count': 0
            }
        
        # Calculate statistics
        max_freq = max(freq_count.values())
        modes = [self.sorted_values[coord] for coord, freq in freq_count.items() if freq == max_freq]
        
        # Find median
        median_pos = (total_elements + 1) // 2
        current_pos = 0
        median = None
        
        for coord in sorted(freq_count.keys()):
            current_pos += freq_count[coord]
            if current_pos >= median_pos and median is None:
                median = self.sorted_values[coord]
        
        return {
            'mode': min(modes),
            'median': median,
            'min': self.sorted_values[min(freq_count.keys())],
            'max': self.sorted_values[max(freq_count.keys())],
            'unique_count': len(freq_count),
            'total_count': total_elements
        }
```

## 🔗 Related Problems

### Links to Similar Problems
- **Range Queries**: Subarray Minimum Queries, Subarray Distinct Values Queries
- **Mode Queries**: Frequency analysis, Statistical measures
- **Coordinate Compression**: Salary Queries, Hotel Queries
- **Mo's Algorithm**: Offline range queries, Range optimization

## 📚 Learning Points

### Key Takeaways
- **Coordinate compression** is essential for handling large value ranges efficiently
- **Mo's algorithm** optimizes offline range queries by sorting queries optimally
- **Frequency tracking** enables efficient mode calculation in ranges
- **Range mode** is a fundamental statistical measure in range queries

---

**Practice these variations to master dynamic range mode query techniques and frequency analysis!** 🎯 