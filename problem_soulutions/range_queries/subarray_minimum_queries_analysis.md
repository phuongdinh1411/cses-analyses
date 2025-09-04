---
layout: simple
title: "Subarray Minimum Queries"
permalink: /problem_soulutions/range_queries/subarray_minimum_queries_analysis
---


# Subarray Minimum Queries

## 📋 Problem Description

Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the minimum value in range [a,b]

This is a dynamic range query problem where we need to efficiently handle both point updates and range minimum queries. We can solve this using a Segment Tree with lazy propagation for efficient range minimum queries and updates.

**Input**: 
- First line: n q (size of the array and number of queries)
- Second line: n integers x₁, x₂, ..., xₙ (the contents of the array)
- Next q lines: queries of the form:
  - "1 k x": update the value at position k to x
  - "2 a b": calculate the minimum value in range [a,b]

**Output**: 
- Print the answer to each minimum query

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
2
2
```

**Explanation**: 
- Initial array: [3, 2, 4, 5, 1, 1, 5, 3]
- Query 1: Minimum in range [1,4] → 2 (minimum of 3, 2, 4, 5)
- Update: Change value at position 4 from 5 to 9 → [3, 2, 4, 9, 1, 1, 5, 3]
- Query 2: Minimum in range [1,4] → 2 (minimum of 3, 2, 4, 9)

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct array updates and minimum calculations.

```python
def subarray_minimum_queries_naive(n, q, array, queries):
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            array[k-1] = x  # 1-indexed to 0-indexed
        else:  # Minimum query
            a, b = query[1], query[2]
            # Calculate minimum from a to b (1-indexed)
            min_val = min(array[a-1:b])
            result.append(min_val)
    
    return result
```

**Why this is inefficient**: Each minimum query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Segment Tree - O(log n) per operation
**Description**: Use Segment Tree for efficient point updates and range minimum queries.

```python
def subarray_minimum_queries_segment(n, q, array, queries):
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = value
            index //= 2
            while index >= 1:
                self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.tree[right])
                left //= 2
                right //= 2
            
            return result
    
    # Initialize segment tree
    st = SegmentTree(array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            st.update(k-1, x)  # Convert to 0-indexed
        else:  # Minimum query
            a, b = query[1], query[2]
            min_val = st.query(a-1, b)  # Convert to 0-indexed, right exclusive
            result.append(min_val)
    
    return result
```

**Why this improvement works**: Segment Tree provides O(log n) time for both updates and range minimum queries.

### Improvement 2: Sparse Table (for static queries) - O(1) per query, O(n log n) preprocessing
**Description**: Use Sparse Table for static range minimum queries (no updates).

```python
def subarray_minimum_queries_sparse(n, q, array, queries):
    # Build sparse table for range minimum queries
    log_n = 20  # Sufficient for n up to 10^6
    sparse = [[0] * n for _ in range(log_n)]
    
    # Base case: sparse[0][i] = array[i]
    for i in range(n):
        sparse[0][i] = array[i]
    
    # Build sparse table
    for k in range(1, log_n):
        for i in range(n - (1 << k) + 1):
            sparse[k][i] = min(sparse[k-1][i], sparse[k-1][i + (1 << (k-1))])
    
    # Precompute log values
    log_table = [0] * (n + 1)
    for i in range(2, n + 1):
        log_table[i] = log_table[i // 2] + 1
    
    def range_min(left, right):
        length = right - left + 1
        k = log_table[length]
        return min(sparse[k][left], sparse[k][right - (1 << k) + 1])
    
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query - not supported in sparse table
            # Would need to rebuild sparse table in O(n log n)
            pass
        else:  # Minimum query
            a, b = query[1], query[2]
            min_val = range_min(a-1, b-1)  # Convert to 0-indexed
            result.append(min_val)
    
    return result
```

**Why this improvement works**: Sparse Table provides O(1) range minimum queries, but doesn't support efficient updates.

## Final Optimal Solution

```python
n, q = map(int, input().split())
array = list(map(int, input().split()))
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

def process_subarray_minimum_queries(n, q, array, queries):
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = value
            index //= 2
            while index >= 1:
                self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.tree[right])
                left //= 2
                right //= 2
            
            return result
    
    # Initialize segment tree
    st = SegmentTree(array)
    result = []
    
    for query in queries: if query[0] == 1:  # Update 
query: 1 k x
            k, x = query[1], query[2]
            st.update(k-1, x)  # Convert to 0-indexed
        else: # Minimum 
query: 2 a b
            a, b = query[1], query[2]
            min_val = st.query(a-1, b)  # Convert to 0-indexed, right exclusive
            result.append(min_val)
    
    return result

result = process_subarray_minimum_queries(n, q, array, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Solution | O(n*q) | O(1) | Direct array operations |
| Segment Tree | O(log n) per operation | O(n) | Efficient point updates and range queries |
| Sparse Table | O(n log n) preprocessing, O(1) per query | O(n log n) | Static range queries only |

## Key Insights for Other Problems

### 1. **Segment Tree for Dynamic Range Queries**
**Principle**: Use Segment Tree for efficient point updates and range queries.
**Applicable to**: Dynamic range problems, update-query problems, array problems

### 2. **Range Minimum/Maximum Queries**
**Principle**: Use appropriate data structures for range minimum/maximum operations.
**Applicable to**: Range query problems, optimization problems, array problems

### 3. **Sparse Table for Static Queries**
**Principle**: Use Sparse Table for static range queries when updates are not needed.
**Applicable to**: Static range problems, preprocessing-heavy problems, query optimization

## Notable Techniques

### 1. **Segment Tree Implementation**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [float('inf')] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
    
    def update(self, index, value):
        index += self.size
        self.tree[index] = value
        index //= 2
        while index >= 1:
            self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
            index //= 2
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result = float('inf')
        
        while left < right:
            if left % 2 == 1:
                result = min(result, self.tree[left])
                left += 1
            if right % 2 == 1:
                right -= 1
                result = min(result, self.tree[right])
            left //= 2
            right //= 2
        
        return result
```

### 2. **Point Update and Range Query**
```python
def point_update_range_min_query(n, array, queries):
    st = SegmentTree(array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            st.update(k-1, x)
        else:  # Range query
            a, b = query[1], query[2]
            result.append(st.query(a-1, b))
    
    return result
```

### 3. **Sparse Table for Static Range Queries**
```python
def build_sparse_table(array):
    n = len(array)
    log_n = 20
    sparse = [[0] * n for _ in range(log_n)]
    
    # Base case
    for i in range(n):
        sparse[0][i] = array[i]
    
    # Build sparse table
    for k in range(1, log_n):
        for i in range(n - (1 << k) + 1):
            sparse[k][i] = min(sparse[k-1][i], sparse[k-1][i + (1 << (k-1))])
    
    return sparse

def range_min_query(sparse, left, right, log_table):
    length = right - left + 1
    k = log_table[length]
    return min(sparse[k][left], sparse[k][right - (1 << k) + 1])
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic range minimum problem with point updates
2. **Choose approach**: Use Segment Tree for efficient operations
3. **Initialize data structure**: Build Segment Tree from initial array
4. **Process queries**: Handle updates and range queries using Segment Tree
5. **Update operations**: Use point updates in Segment Tree
6. **Range queries**: Use range query method in Segment Tree
7. **Return result**: Output answers for all range queries

---

*This analysis shows how to efficiently handle dynamic range minimum queries using Segment Tree.*

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Subarray Minimum Queries with Range Updates**
**Problem**: Support range updates (modify values in a range) and point minimum queries.
```python
def subarray_minimum_queries_range_updates(n, q, array, operations):
    # Use Segment Tree with lazy propagation
    class LazySegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            self.lazy = [None] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def push(self, node, left, right):
            if self.lazy[node] is not None:
                self.tree[node] = self.lazy[node]
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
            self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
        
        def point_query(self, node, left, right, index):
            self.push(node, left, right)
            if left == right:
                return self.tree[node]
            mid = (left + right) // 2
            if index <= mid:
                return self.point_query(2 * node, left, mid, index)
            else:
                return self.point_query(2 * node + 1, mid + 1, right, index)
    
    st = LazySegmentTree(array)
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

#### **Variation 2: Subarray Minimum Queries with Multiple Criteria**
**Problem**: Each element has multiple attributes, find minimum based on different criteria.
```python
def subarray_minimum_queries_multiple_criteria(n, q, array, criteria, operations):
    # Use Segment Tree with multiple criteria
    class MultiCriteriaSegmentTree:
        def __init__(self, data, criteria):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.trees = {}
            
            # Build separate trees for each criterion
            for criterion in criteria:
                self.trees[criterion] = [float('inf')] * (2 * self.size)
                for i in range(self.n):
                    self.trees[criterion][self.size + i] = data[i][criterion]
                for i in range(self.size - 1, 0, -1):
                    self.trees[criterion][i] = min(self.trees[criterion][2 * i], 
                                                 self.trees[criterion][2 * i + 1])
        
        def update(self, index, value_dict):
            index += self.size
            for criterion, value in value_dict.items():
                self.trees[criterion][index] = value
            index //= 2
            while index >= 1:
                for criterion in self.trees:
                    self.trees[criterion][index] = min(self.trees[criterion][2 * index], 
                                                     self.trees[criterion][2 * index + 1])
                index //= 2
        
        def query(self, left, right, criterion):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.trees[criterion][left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.trees[criterion][right])
                left //= 2
                right //= 2
            
            return result
    
    st = MultiCriteriaSegmentTree(array, criteria)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, value_dict = op[1], op[2]
            st.update(k-1, value_dict)
        else:  # Multi-criteria query
            l, r, criterion = op[1], op[2], op[3]
            result = st.query(l-1, r-1, criterion)
            results.append(result)
    
    return results
```

#### **Variation 3: Subarray Minimum Queries with Sliding Window**
**Problem**: Find minimum in sliding windows of fixed size k.
```python
def subarray_minimum_queries_sliding_window(n, q, array, operations):
    # Use Segment Tree for sliding window minimum
    class SlidingWindowSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            
            # Build tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = value
            index //= 2
            while index >= 1:
                self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.tree[right])
                left //= 2
                right //= 2
            
            return result
        
        def sliding_window_min(self, window_size):
            # Find minimum for each sliding window of size window_size
            results = []
            for i in range(self.n - window_size + 1):
                min_val = self.query(i, i + window_size)
                results.append(min_val)
            return results
    
    st = SlidingWindowSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Sliding window query
            window_size = op[1]
            window_mins = st.sliding_window_min(window_size)
            results.append(window_mins)
    
    return results
```

#### **Variation 4: Subarray Minimum Queries with Frequency Counting**
**Problem**: Find minimum value and count how many times it appears in the range.
```python
def subarray_minimum_queries_with_frequency(n, q, array, operations):
    # Use Segment Tree with minimum value and frequency
    class MinFreqSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.min_tree = [float('inf')] * (2 * self.size)
            self.freq_tree = [0] * (2 * self.size)
            
            # Build trees
            for i in range(self.n):
                self.min_tree[self.size + i] = data[i]
                self.freq_tree[self.size + i] = 1
            for i in range(self.size - 1, 0, -1):
                left_min = self.min_tree[2 * i]
                right_min = self.min_tree[2 * i + 1]
                if left_min < right_min:
                    self.min_tree[i] = left_min
                    self.freq_tree[i] = self.freq_tree[2 * i]
                elif right_min < left_min:
                    self.min_tree[i] = right_min
                    self.freq_tree[i] = self.freq_tree[2 * i + 1]
                else:
                    self.min_tree[i] = left_min
                    self.freq_tree[i] = self.freq_tree[2 * i] + self.freq_tree[2 * i + 1]
        
        def update(self, index, value):
            index += self.size
            self.min_tree[index] = value
            index //= 2
            while index >= 1:
                left_min = self.min_tree[2 * index]
                right_min = self.min_tree[2 * index + 1]
                if left_min < right_min:
                    self.min_tree[index] = left_min
                    self.freq_tree[index] = self.freq_tree[2 * index]
                elif right_min < left_min:
                    self.min_tree[index] = right_min
                    self.freq_tree[index] = self.freq_tree[2 * index + 1]
                else:
                    self.min_tree[index] = left_min
                    self.freq_tree[index] = self.freq_tree[2 * index] + self.freq_tree[2 * index + 1]
                index //= 2
        
        def query(self, left, right):
            return self._query(1, 0, self.size - 1, left, right)
        
        def _query(self, node, left, right, l, r):
            if r < left or l > right:
                return float('inf'), 0
            if l <= left and right <= r:
                return self.min_tree[node], self.freq_tree[node]
            mid = (left + right) // 2
            left_min, left_freq = self._query(2 * node, left, mid, l, r)
            right_min, right_freq = self._query(2 * node + 1, mid + 1, right, l, r)
            
            if left_min < right_min:
                return left_min, left_freq
            elif right_min < left_min:
                return right_min, right_freq
            else:
                return left_min, left_freq + right_freq
    
    st = MinFreqSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # Min with frequency query
            l, r = op[1], op[2]
            min_val, freq = st.query(l-1, r-1)
            results.append((min_val, freq))
    
    return results
```

#### **Variation 5: Subarray Minimum Queries with K-th Minimum**
**Problem**: Find the k-th minimum value in a range.
```python
def subarray_minimum_queries_kth_minimum(n, q, array, operations):
    # Use Segment Tree with k-th minimum support
    class KthMinSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [[] for _ in range(2 * self.size)]
            
            # Build tree with sorted lists
            for i in range(self.n):
                self.tree[self.size + i] = [data[i]]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = sorted(self.tree[2 * i] + self.tree[2 * i + 1])
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = [value]
            index //= 2
            while index >= 1:
                self.tree[index] = sorted(self.tree[2 * index] + self.tree[2 * index + 1])
                index //= 2
        
        def query_kth_min(self, left, right, k):
            return self._query_kth_min(1, 0, self.size - 1, left, right, k)
        
        def _query_kth_min(self, node, left, right, l, r, k):
            if r < left or l > right:
                return []
            if l <= left and right <= r:
                return self.tree[node][:k] if k <= len(self.tree[node]) else self.tree[node]
            mid = (left + right) // 2
            left_result = self._query_kth_min(2 * node, left, mid, l, r, k)
            right_result = self._query_kth_min(2 * node + 1, mid + 1, right, l, r, k)
            
            # Merge and return k smallest elements
            merged = sorted(left_result + right_result)
            return merged[:k] if k <= len(merged) else merged
    
    st = KthMinSegmentTree(array)
    results = []
    
    for op in operations:
        if op[0] == 1:  # Update
            k, x = op[1], op[2]
            st.update(k-1, x)
        else:  # K-th minimum query
            l, r, k = op[1], op[2], op[3]
            kth_mins = st.query_kth_min(l-1, r-1, k)
            results.append(kth_mins)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Range Minimum Data Structures**
- **Segment Tree**: O(log n) point updates and range queries
- **Sparse Table**: O(1) queries but static
- **Monotonic Stack**: Efficient minimum tracking
- **Cartesian Tree**: Alternative minimum representation

#### **2. Range Query Types**
- **Range Minimum**: Find minimum in range
- **Range Maximum**: Find maximum in range
- **K-th Minimum**: Find k-th smallest element
- **Frequency Counting**: Count occurrences of minimum

#### **3. Advanced Range Techniques**
- **Lazy Propagation**: Efficient range updates
- **Sliding Window**: Optimize consecutive ranges
- **Multi-criteria Queries**: Handle multiple attributes
- **Persistent Data Structures**: Handle historical states

#### **4. Optimization Problems**
- **Optimal Range Selection**: Find optimal ranges for queries
- **Range with Constraints**: Add additional constraints
- **K-th Order Statistics**: Find k-th element efficiently
- **Frequency Analysis**: Analyze element distributions

#### **5. Competitive Programming Patterns**
- **Binary Search**: Find optimal ranges
- **Two Pointers**: Efficient range processing
- **Monotonic Stack**: Track minimums efficiently
- **Offline Processing**: Process queries in optimal order

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    array = list(map(int, input().split()))
    
    st = SegmentTree(array)
    for _ in range(q):
        query = list(map(int, input().split()))
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            st.update(k-1, x)
        else:  # Query
            a, b = query[1], query[2]
            result = st.query(a-1, b-1)
            print(result)
```

#### **2. Subarray Minimum Queries with Aggregation**
```python
def subarray_minimum_queries_aggregation(n, q, array, operations):
    # Support multiple aggregation functions
    class AggregationSegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.min_tree = [float('inf')] * (2 * self.size)
            self.max_tree = [-float('inf')] * (2 * self.size)
            self.sum_tree = [0] * (2 * self.size)
            
            # Build trees
            for i in range(self.n):
                self.min_tree[self.size + i] = data[i]
                self.max_tree[self.size + i] = data[i]
                self.sum_tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.min_tree[i] = min(self.min_tree[2 * i], self.min_tree[2 * i + 1])
                self.max_tree[i] = max(self.max_tree[2 * i], self.max_tree[2 * i + 1])
                self.sum_tree[i] = self.sum_tree[2 * i] + self.sum_tree[2 * i + 1]
        
        def update(self, index, value):
            index += self.size
            self.min_tree[index] = value
            self.max_tree[index] = value
            self.sum_tree[index] = value
            index //= 2
            while index >= 1:
                self.min_tree[index] = min(self.min_tree[2 * index], self.min_tree[2 * index + 1])
                self.max_tree[index] = max(self.max_tree[2 * index], self.max_tree[2 * index + 1])
                self.sum_tree[index] = self.sum_tree[2 * index] + self.sum_tree[2 * index + 1]
                index //= 2
        
        def query(self, left, right, op):
            if op == 'MIN':
                return self._query_min(left, right)
            elif op == 'MAX':
                return self._query_max(left, right)
            elif op == 'SUM':
                return self._query_sum(left, right)
        
        def _query_min(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.min_tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.min_tree[right])
                left //= 2
                right //= 2
            return result
    
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

#### **3. Interactive Subarray Minimum Queries**
```python
def interactive_subarray_minimum_queries(n, array):
    # Handle interactive queries
    st = SegmentTree(array)
    
    while True: 
try: query = input().strip()
            if query == 'END':
                break
            
            parts = query.split()
            if parts[0] == 'UPDATE':
                k, x = int(parts[1]), int(parts[2])
                st.update(k-1, x)
                print(f"Updated position {k} to {x}")
            elif parts[0] == 'QUERY':
                a, b = int(parts[1]), int(parts[2])
                result = st.query(a-1, b-1)
                print(f"Minimum in range [{a},{b}]: {result}")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. Range Minimum Properties**
- **Idempotency**: min(min(a,b), min(c,d)) = min(a,b,c,d)
- **Commutativity**: min(a,b) = min(b,a)
- **Associativity**: min(min(a,b), c) = min(a, min(b,c))
- **Monotonicity**: If a ≤ b, then min(a,c) ≤ min(b,c)

#### **2. Optimization Techniques**
- **Early Termination**: Stop if minimum is found
- **Binary Search**: Find ranges with specific minimums
- **Caching**: Store frequently accessed minimums
- **Compression**: Handle sparse arrays efficiently

#### **3. Advanced Mathematical Concepts**
- **Order Statistics**: Understanding minimum properties
- **Monotonic Stack**: Efficient minimum tracking
- **Cartesian Tree**: Alternative minimum representation
- **LCA Reduction**: Reduce range minimum to LCA problem

#### **4. Algorithmic Improvements**
- **Block Decomposition**: Divide array into blocks
- **Lazy Propagation**: Efficient range updates
- **Compression**: Handle sparse arrays efficiently
- **Parallel Processing**: Use multiple cores for large datasets

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(log n) per query and update
- **Space Complexity**: O(n) for segment tree
- **Why it works**: Segment tree enables efficient range minimum queries and point updates in O(log n) time

### Key Implementation Points
- Use segment tree for efficient range minimum queries
- Handle point updates efficiently
- Segment tree supports both range queries and point updates
- Lazy propagation for range updates if needed

## 🎯 Key Insights

### Important Concepts and Patterns
- **Segment Tree**: Essential for efficient range minimum queries
- **Range Minimum**: Most efficient way to find minimum in a range
- **Point Updates**: Update single elements efficiently
- **Range Queries**: Query minimum value in any range

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Subarray Minimum Queries with Range Updates**
```python
class RangeUpdateMinimumQueries:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr.copy()
        
        # Segment tree with lazy propagation
        self.tree = [float('inf')] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        
        self.build(1, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.arr[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node, start, mid)
            self.build(2 * node + 1, mid + 1, end)
            self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
    
    def push_lazy(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node]
            
            if start != end:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
            
            self.lazy[node] = 0
    
    def range_update(self, node, start, end, l, r, val):
        self.push_lazy(node, start, end)
        
        if start > end or start > r or end < l:
            return
        
        if start >= l and end <= r:
            self.lazy[node] += val
            self.push_lazy(node, start, end)
            return
        
        mid = (start + end) // 2
        self.range_update(2 * node, start, mid, l, r, val)
        self.range_update(2 * node + 1, mid + 1, end, l, r, val)
        
        self.push_lazy(2 * node, start, mid)
        self.push_lazy(2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
    
    def range_minimum(self, node, start, end, l, r):
        self.push_lazy(node, start, end)
        
        if start > end or start > r or end < l:
            return float('inf')
        
        if start >= l and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_min = self.range_minimum(2 * node, start, mid, l, r)
        right_min = self.range_minimum(2 * node + 1, mid + 1, end, l, r)
        
        return min(left_min, right_min)
    
    def point_update(self, node, start, end, pos, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if pos <= mid:
                self.point_update(2 * node, start, mid, pos, val)
            else:
                self.point_update(2 * node + 1, mid + 1, end, pos, val)
            self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
```

#### **2. Subarray Minimum Queries with K-th Minimum**
```python
class KthMinimumQueries:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr.copy()
        
        # Coordinate compression
        all_values = set(arr)
        self.sorted_values = sorted(all_values)
        self.coord_map = {val: i for i, val in enumerate(self.sorted_values)}
        
        # Segment tree for frequency counting
        self.tree = [0] * (4 * len(self.sorted_values))
        
        # Initialize with original values
        for val in arr:
            self.update_frequency(1, 0, len(self.sorted_values) - 1, self.coord_map[val], 1)
    
    def update_frequency(self, node, start, end, pos, delta):
        if start == end:
            self.tree[node] += delta
        else:
            mid = (start + end) // 2
            if pos <= mid:
                self.update_frequency(2 * node, start, mid, pos, delta)
            else:
                self.update_frequency(2 * node + 1, mid + 1, end, pos, delta)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def find_kth_minimum(self, node, start, end, k):
        if start == end:
            return self.sorted_values[start]
        
        mid = (start + end) // 2
        left_count = self.tree[2 * node]
        
        if k <= left_count:
            return self.find_kth_minimum(2 * node, start, mid, k)
        else:
            return self.find_kth_minimum(2 * node + 1, mid + 1, end, k - left_count)
    
    def range_kth_minimum(self, a, b, k):
        # Get all values in range [a, b]
        range_values = self.arr[a-1:b]
        
        # Count frequencies
        freq_count = {}
        for val in range_values:
            coord = self.coord_map[val]
            freq_count[coord] = freq_count.get(coord, 0) + 1
        
        # Find k-th minimum
        sorted_coords = sorted(freq_count.keys())
        current_count = 0
        
        for coord in sorted_coords:
            current_count += freq_count[coord]
            if current_count >= k:
                return self.sorted_values[coord]
        
        return None
```

#### **3. Subarray Minimum Queries with Multiple Operations**
```python
class MultiOperationMinimumQueries:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr.copy()
        
        # Segment trees for different operations
        self.min_tree = [float('inf')] * (4 * self.n)
        self.max_tree = [float('-inf')] * (4 * self.n)
        self.sum_tree = [0] * (4 * self.n)
        
        self.build(1, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.min_tree[node] = self.arr[start]
            self.max_tree[node] = self.arr[start]
            self.sum_tree[node] = self.arr[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node, start, mid)
            self.build(2 * node + 1, mid + 1, end)
            
            self.min_tree[node] = min(self.min_tree[2 * node], self.min_tree[2 * node + 1])
            self.max_tree[node] = max(self.max_tree[2 * node], self.max_tree[2 * node + 1])
            self.sum_tree[node] = self.sum_tree[2 * node] + self.sum_tree[2 * node + 1]
    
    def range_minimum(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return float('inf')
        
        if start >= l and end <= r:
            return self.min_tree[node]
        
        mid = (start + end) // 2
        left_min = self.range_minimum(2 * node, start, mid, l, r)
        right_min = self.range_minimum(2 * node + 1, mid + 1, end, l, r)
        
        return min(left_min, right_min)
    
    def range_maximum(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return float('-inf')
        
        if start >= l and end <= r:
            return self.max_tree[node]
        
        mid = (start + end) // 2
        left_max = self.range_maximum(2 * node, start, mid, l, r)
        right_max = self.range_maximum(2 * node + 1, mid + 1, end, l, r)
        
        return max(left_max, right_max)
    
    def range_sum(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return 0
        
        if start >= l and end <= r:
            return self.sum_tree[node]
        
        mid = (start + end) // 2
        left_sum = self.range_sum(2 * node, start, mid, l, r)
        right_sum = self.range_sum(2 * node + 1, mid + 1, end, l, r)
        
        return left_sum + right_sum
    
    def get_range_stats(self, a, b):
        # Get comprehensive statistics for range [a, b]
        min_val = self.range_minimum(1, 0, self.n - 1, a - 1, b - 1)
        max_val = self.range_maximum(1, 0, self.n - 1, a - 1, b - 1)
        sum_val = self.range_sum(1, 0, self.n - 1, a - 1, b - 1)
        count = b - a + 1
        avg_val = sum_val / count if count > 0 else 0
        
        return {
            'min': min_val,
            'max': max_val,
            'sum': sum_val,
            'count': count,
            'average': avg_val
        }
```

## 🔗 Related Problems

### Links to Similar Problems
- **Range Queries**: Static Range Minimum Queries, Range Update Queries
- **Segment Tree**: Range Sum Queries, Range XOR Queries
- **Minimum Queries**: Range minimum, Point updates
- **Data Structures**: Segment tree, Sparse table

## 📚 Learning Points

### Key Takeaways
- **Segment tree** is essential for efficient range minimum queries
- **Range minimum** can be computed efficiently using segment trees
- **Point updates** are handled efficiently in segment trees
- **Range queries** are fundamental operations in competitive programming

---

**Practice these variations to master dynamic range minimum query techniques and segment tree operations!** 🎯 