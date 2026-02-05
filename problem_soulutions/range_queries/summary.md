---
layout: simple
title: "Range Queries Summary"
permalink: /problem_soulutions/range_queries/summary
---

# Range Queries

Welcome to the Range Queries section! This category covers efficient data structures and algorithms for handling queries on ranges of data.

## Key Concepts & Techniques

### Data Structures

#### Prefix Sum Array
- **When to use**: Static range sum queries, no updates
- **Time**: O(n) preprocessing, O(1) per query
- **Space**: O(n)
- **Applications**: Range sum, range average, cumulative queries
- **Implementation**: `prefix[i] = prefix[i-1] + arr[i]`

#### Segment Tree
- **When to use**: Range queries with updates, flexible operations
- **Time**: O(n) construction, O(log n) per query/update
- **Space**: O(n)
- **Applications**: Range sum/min/max, range updates, custom operations
- **Implementation**: Binary tree with range information at each node

#### Fenwick Tree (Binary Indexed Tree)
- **When to use**: Point updates with range queries, space-efficient
- **Time**: O(n) construction, O(log n) per query/update
- **Space**: O(n)
- **Applications**: Range sum, point updates, inversion counting
- **Implementation**: Array with bit manipulation for indexing

#### Sparse Table
- **When to use**: Static range minimum/maximum queries, no updates
- **Time**: O(n log n) preprocessing, O(1) per query
- **Space**: O(n log n)
- **Applications**: Range minimum/maximum, GCD, range AND/OR
- **Implementation**: 2D array with powers of 2 ranges

#### Sqrt Decomposition
- **When to use**: Simple range queries, easy implementation
- **Time**: O(√n) per query/update
- **Space**: O(√n)
- **Applications**: Range sum, range updates, simple operations
- **Implementation**: Divide array into √n blocks

### Query Types & Operations

#### Range Sum Queries
- **When to use**: Summing elements in a range
- **Data Structure**: Prefix array, segment tree, Fenwick tree
- **Time**: O(1) with prefix, O(log n) with trees
- **Applications**: Subarray sums, cumulative statistics
- **Implementation**: `sum(l,r) = prefix[r] - prefix[l-1]`

#### Range Minimum/Maximum Queries (RMQ)
- **When to use**: Finding min/max in a range
- **Data Structure**: Sparse table, segment tree
- **Time**: O(1) with sparse table, O(log n) with segment tree
- **Applications**: Range statistics, optimization problems
- **Implementation**: Precompute min/max for all power-of-2 ranges

#### Range Update Queries
- **When to use**: Modifying all elements in a range
- **Data Structure**: Segment tree with lazy propagation
- **Time**: O(log n) per update
- **Space**: O(n)
- **Applications**: Range addition, range assignment
- **Implementation**: Defer updates until necessary

#### Point Update Queries
- **When to use**: Modifying single elements
- **Data Structure**: Segment tree, Fenwick tree
- **Time**: O(log n) per update
- **Applications**: Single element changes, dynamic arrays
- **Implementation**: Update leaf and propagate up

### Advanced Techniques

#### Lazy Propagation
- **When to use**: Range updates in segment trees
- **Time**: O(log n) per update, O(log n) per query
- **Space**: O(n)
- **Applications**: Range addition, range multiplication, range assignment
- **Implementation**: Store pending updates at internal nodes

#### Binary Search on Answer
- **When to use**: Finding optimal value in range
- **Time**: O(log n) per search
- **Space**: O(1)
- **Applications**: Finding k-th smallest, optimization problems
- **Implementation**: Binary search with range query check

#### Coordinate Compression
- **When to use**: Large coordinate ranges, discrete values
- **Time**: O(n log n) preprocessing
- **Space**: O(n)
- **Applications**: Large coordinate spaces, discrete optimization
- **Implementation**: Sort and map to smaller range

#### Mo's Algorithm
- **When to use**: Offline range queries, multiple queries
- **Time**: O((n+q)√n) where q is number of queries
- **Space**: O(n)
- **Applications**: Range distinct values, range frequency
- **Implementation**: Sort queries by block, use two pointers

### 2D Range Queries

#### 2D Prefix Sum
- **When to use**: 2D range sum queries, no updates
- **Time**: O(n²) preprocessing, O(1) per query
- **Space**: O(n²)
- **Applications**: Submatrix sums, image processing
- **Implementation**: `prefix[i][j] = prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1] + arr[i][j]`

#### 2D Segment Tree
- **When to use**: 2D range queries with updates
- **Time**: O(n²) construction, O(log² n) per query/update
- **Space**: O(n²)
- **Applications**: 2D range operations, matrix queries
- **Implementation**: Segment tree of segment trees

#### 2D Fenwick Tree
- **When to use**: 2D point updates with range queries
- **Time**: O(n²) construction, O(log² n) per query/update
- **Space**: O(n²)
- **Applications**: 2D range sums, point updates
- **Implementation**: 2D array with 2D bit manipulation

### Specialized Data Structures

#### Persistent Segment Tree
- **When to use**: Version control, time-travel queries
- **Time**: O(log n) per query/update
- **Space**: O(n log n)
- **Applications**: Version history, temporal queries
- **Implementation**: Create new nodes for each update

#### Dynamic Segment Tree
- **When to use**: Large coordinate ranges, sparse data
- **Time**: O(log n) per query/update
- **Space**: O(n log n)
- **Applications**: Large ranges, sparse updates
- **Implementation**: Create nodes on demand

#### Merge Sort Tree
- **When to use**: Range counting, range k-th element
- **Time**: O(n log n) construction, O(log² n) per query
- **Space**: O(n log n)
- **Applications**: Range counting, range statistics
- **Implementation**: Segment tree with sorted arrays

#### Wavelet Tree
- **When to use**: Range k-th element, range counting
- **Time**: O(log n) per query
- **Space**: O(n log n)
- **Applications**: Range statistics, string processing
- **Implementation**: Binary tree based on bit values

### Optimization Techniques

#### Space Optimization
- **Rolling Arrays**: When only previous values needed
  - *When to use*: DP with range queries
  - *Example*: Range DP with rolling array
- **In-place Updates**: Modify array in place
  - *When to use*: When original array not needed
  - *Example*: In-place range updates

#### Time Optimization
- **Batch Processing**: Process multiple queries together
  - *When to use*: Offline queries
  - *Example*: Mo's algorithm for multiple queries
- **Precomputation**: Compute common values once
  - *When to use*: Repeated calculations
  - *Example*: Precompute powers for modular arithmetic

#### Memory Optimization
- **Lazy Allocation**: Allocate memory on demand
  - *When to use*: Sparse data structures
  - *Example*: Dynamic segment tree
- **Memory Pool**: Reuse allocated memory
  - *When to use*: Frequent allocation/deallocation
  - *Example*: Persistent segment tree with memory pool

## Problem Categories

### Static Range Queries
- [Static Range Sum Queries](static_range_sum_queries_analysis) - Basic prefix sums
- [Static Range Minimum Queries](static_range_minimum_queries_analysis) - Sparse table
- [Range XOR Queries](range_xor_queries_analysis) - XOR over ranges

### Dynamic Range Queries
- [Dynamic Range Sum Queries](dynamic_range_sum_queries_analysis) - Segment tree
- [Range Update Queries](range_update_queries_analysis) - Lazy propagation
- [Range Interval Queries](range_interval_queries_analysis) - Interval operations

### 2D Range Queries
- [Forest Queries](forest_queries_analysis) - 2D prefix sums
- [Hotel Queries](hotel_queries_analysis) - 2D range queries

### Subarray Queries
- [Subarray Sum Queries](subarray_sum_queries_analysis) - Subarray sums
- [Subarray Distinct Values Queries](subarray_distinct_values_queries_analysis) - Distinct elements
- [Subarray Minimum Queries](subarray_minimum_queries_analysis) - Minimum in subarray
- [Subarray Maximums](subarray_maximums_analysis) - Maximum in subarray
- [Subarray Mode Queries](subarray_mode_queries_analysis) - Most frequent element
- [Subarray OR Queries](subarray_or_queries_analysis) - Bitwise OR

### Advanced Queries
- [List Removals](list_removals_analysis) - Dynamic array operations
- [Salary Queries](salary_queries_analysis) - Range counting
- [Prefix Sum Queries](prefix_sum_queries_analysis) - Advanced prefix sums
- [Pizzeria Queries](pizzeria_queries_analysis) - Distance queries
- [Visible Buildings Queries](visible_buildings_queries_analysis) - Geometric queries

## Detailed Examples and Implementations

### Classic Range Query Data Structures with Code

#### 1. Segment Tree Implementation
```python
class SegmentTree:
  def __init__(self, data, operation, default_value):
    self.n = len(data)
    self.operation = operation
    self.default_value = default_value
    self.tree = [default_value] * (4 * self.n)
    self.build(data, 0, 0, self.n - 1)
  
  def build(self, data, node, start, end):
    if start == end:
      self.tree[node] = data[start]
    else:
      mid = (start + end) // 2
      self.build(data, 2 * node + 1, start, mid)
      self.build(data, 2 * node + 2, mid + 1, end)
      self.tree[node] = self.operation(
        self.tree[2 * node + 1], 
        self.tree[2 * node + 2]
      )
  
  def update(self, index, value):
    self._update(0, 0, self.n - 1, index, value)
  
  def _update(self, node, start, end, index, value):
    if start == end:
      self.tree[node] = value
    else:
      mid = (start + end) // 2
      if index <= mid:
        self._update(2 * node + 1, start, mid, index, value)
      else:
        self._update(2 * node + 2, mid + 1, end, index, value)
      self.tree[node] = self.operation(
        self.tree[2 * node + 1], 
        self.tree[2 * node + 2]
      )
  
  def query(self, left, right):
    return self._query(0, 0, self.n - 1, left, right)
  
  def _query(self, node, start, end, left, right):
    if right < start or end < left:
      return self.default_value
    
    if left <= start and end <= right:
      return self.tree[node]
    
    mid = (start + end) // 2
    left_result = self._query(2 * node + 1, start, mid, left, right)
    right_result = self._query(2 * node + 2, mid + 1, end, left, right)
    return self.operation(left_result, right_result)

# Usage examples
def range_sum_segment_tree(data):
  return SegmentTree(data, lambda x, y: x + y, 0)

def range_min_segment_tree(data):
  return SegmentTree(data, min, float('inf'))

def range_max_segment_tree(data):
  return SegmentTree(data, max, float('-inf'))
```

#### 2. Lazy Propagation Segment Tree
```python
class LazySegmentTree:
  def __init__(self, data, operation, default_value, lazy_operation, lazy_default):
    self.n = len(data)
    self.operation = operation
    self.default_value = default_value
    self.lazy_operation = lazy_operation
    self.lazy_default = lazy_default
    self.tree = [default_value] * (4 * self.n)
    self.lazy = [lazy_default] * (4 * self.n)
    self.build(data, 0, 0, self.n - 1)
  
  def build(self, data, node, start, end):
    if start == end:
      self.tree[node] = data[start]
    else:
      mid = (start + end) // 2
      self.build(data, 2 * node + 1, start, mid)
      self.build(data, 2 * node + 2, mid + 1, end)
      self.tree[node] = self.operation(
        self.tree[2 * node + 1], 
        self.tree[2 * node + 2]
      )
  
  def push_lazy(self, node, start, end):
    if self.lazy[node] != self.lazy_default:
      # Apply lazy update to current node
      self.tree[node] = self.lazy_operation(
        self.tree[node], 
        self.lazy[node], 
        end - start + 1
      )
      
      # Propagate to children if not leaf
      if start != end:
        self.lazy[2 * node + 1] = self.lazy_operation(
          self.lazy[2 * node + 1], 
          self.lazy[node], 
          1
        )
        self.lazy[2 * node + 2] = self.lazy_operation(
          self.lazy[2 * node + 2], 
          self.lazy[node], 
          1
        )
      
      self.lazy[node] = self.lazy_default
  
  def range_update(self, left, right, value):
    self._range_update(0, 0, self.n - 1, left, right, value)
  
  def _range_update(self, node, start, end, left, right, value):
    self.push_lazy(node, start, end)
    
    if right < start or end < left:
      return
    
    if left <= start and end <= right:
      self.lazy[node] = value
      self.push_lazy(node, start, end)
      return
    
    mid = (start + end) // 2
    self._range_update(2 * node + 1, start, mid, left, right, value)
    self._range_update(2 * node + 2, mid + 1, end, left, right, value)
    
    self.push_lazy(2 * node + 1, start, mid)
    self.push_lazy(2 * node + 2, mid + 1, end)
    self.tree[node] = self.operation(
      self.tree[2 * node + 1], 
      self.tree[2 * node + 2]
    )
  
  def range_query(self, left, right):
    return self._range_query(0, 0, self.n - 1, left, right)
  
  def _range_query(self, node, start, end, left, right):
    self.push_lazy(node, start, end)
    
    if right < start or end < left:
      return self.default_value
    
    if left <= start and end <= right:
      return self.tree[node]
    
    mid = (start + end) // 2
    left_result = self._range_query(2 * node + 1, start, mid, left, right)
    right_result = self._range_query(2 * node + 2, mid + 1, end, left, right)
    return self.operation(left_result, right_result)

# Usage for range sum with range updates
def range_sum_lazy_segment_tree(data):
  return LazySegmentTree(
    data, 
    lambda x, y: x + y,  # operation
    0,                   # default_value
    lambda x, y, size: x + y * size,  # lazy_operation
    0                    # lazy_default
  )
```

#### 3. Fenwick Tree (Binary Indexed Tree)
```python
class FenwickTree:
  def __init__(self, size):
    self.n = size
    self.tree = [0] * (self.n + 1)
  
  def update(self, index, delta):
    index += 1  # 1-indexed
    while index <= self.n:
      self.tree[index] += delta
      index += index & (-index)
  
  def query(self, index):
    index += 1  # 1-indexed
    result = 0
    while index > 0:
      result += self.tree[index]
      index -= index & (-index)
    return result
  
  def range_query(self, left, right):
    return self.query(right) - self.query(left - 1)
  
  def range_update(self, left, right, delta):
    self.update(left, delta)
    self.update(right + 1, -delta)

class FenwickTree2D:
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]
  
  def update(self, row, col, delta):
    row += 1
    col += 1
    i = row
    while i <= self.rows:
      j = col
      while j <= self.cols:
        self.tree[i][j] += delta
        j += j & (-j)
      i += i & (-i)
  
  def query(self, row, col):
    row += 1
    col += 1
    result = 0
    i = row
    while i > 0:
      j = col
      while j > 0:
        result += self.tree[i][j]
        j -= j & (-j)
      i -= i & (-i)
    return result
  
  def range_query(self, row1, col1, row2, col2):
    return (self.query(row2, col2) - 
        self.query(row1 - 1, col2) - 
        self.query(row2, col1 - 1) + 
        self.query(row1 - 1, col1 - 1))
```

#### 4. Sparse Table for Range Minimum/Maximum
```python
class SparseTable:
  def __init__(self, data, operation, default_value):
    self.n = len(data)
    self.operation = operation
    self.default_value = default_value
    self.log = [0] * (self.n + 1)
    
    # Precompute logarithms
    for i in range(2, self.n + 1):
      self.log[i] = self.log[i // 2] + 1
    
    # Build sparse table
    self.k = self.log[self.n] + 1
    self.st = [[default_value] * self.k for _ in range(self.n)]
    
    for i in range(self.n):
      self.st[i][0] = data[i]
    
    for j in range(1, self.k):
      for i in range(self.n - (1 << j) + 1):
        self.st[i][j] = self.operation(
          self.st[i][j - 1],
          self.st[i + (1 << (j - 1))][j - 1]
        )
  
  def query(self, left, right):
    length = right - left + 1
    k = self.log[length]
    return self.operation(
      self.st[left][k],
      self.st[right - (1 << k) + 1][k]
    )

# Usage examples
def range_min_sparse_table(data):
  return SparseTable(data, min, float('inf'))

def range_max_sparse_table(data):
  return SparseTable(data, max, float('-inf'))

def range_gcd_sparse_table(data):
  return SparseTable(data, gcd, 0)
```

### Advanced Range Query Techniques

#### 1. Mo's Algorithm for Offline Queries
```python
class MoAlgorithm:
  def __init__(self, queries, array):
    self.queries = queries
    self.array = array
    self.n = len(array)
    self.block_size = int(self.n ** 0.5)
    
    # Sort queries by block, then by right endpoint
    self.queries.sort(key=lambda q: (
      q[0] // self.block_size,
      q[1] if (q[0] // self.block_size) % 2 == 0 else -q[1]
    ))
  
  def solve(self):
    current_l = 0
    current_r = -1
    current_ans = 0
    results = [0] * len(self.queries)
    
    for i, (left, right) in enumerate(self.queries):
      # Expand range
      while current_l > left:
        current_l -= 1
        current_ans += self.add(current_l)
      
      while current_r < right:
        current_r += 1
        current_ans += self.add(current_r)
      
      # Contract range
      while current_l < left:
        current_ans -= self.remove(current_l)
        current_l += 1
      
      while current_r > right:
        current_ans -= self.remove(current_r)
        current_r -= 1
      
      results[i] = current_ans
    
    return results
  
  def add(self, index):
    # Implement based on problem requirements
    return self.array[index]
  
  def remove(self, index):
    # Implement based on problem requirements
    return self.array[index]

def distinct_elements_mo(array, queries):
  class DistinctElementsMo(MoAlgorithm):
    def __init__(self, queries, array):
      super().__init__(queries, array)
      self.freq = {}
      self.distinct_count = 0
    
    def add(self, index):
      element = self.array[index]
      if self.freq.get(element, 0) == 0:
        self.distinct_count += 1
      self.freq[element] = self.freq.get(element, 0) + 1
      return 0
    
    def remove(self, index):
      element = self.array[index]
      self.freq[element] -= 1
      if self.freq[element] == 0:
        self.distinct_count -= 1
      return 0
    
    def solve(self):
      current_l = 0
      current_r = -1
      results = [0] * len(self.queries)
      
      for i, (left, right) in enumerate(self.queries):
        while current_l > left:
          current_l -= 1
          self.add(current_l)
        
        while current_r < right:
          current_r += 1
          self.add(current_r)
        
        while current_l < left:
          self.remove(current_l)
          current_l += 1
        
        while current_r > right:
          self.remove(current_r)
          current_r -= 1
        
        results[i] = self.distinct_count
      
      return results
  
  return DistinctElementsMo(queries, array).solve()
```

#### 2. Coordinate Compression
```python
def coordinate_compression(coordinates):
  """Compress coordinates to 0-based indices"""
  sorted_coords = sorted(set(coordinates))
  coord_map = {coord: idx for idx, coord in enumerate(sorted_coords)}
  return [coord_map[coord] for coord in coordinates], sorted_coords

def range_sum_with_compression(queries, coordinates):
  """Handle range queries with coordinate compression"""
  # Extract all unique coordinates
  all_coords = set()
  for query in queries:
    all_coords.add(query[0])
    all_coords.add(query[1])
  
  # Compress coordinates
  sorted_coords = sorted(all_coords)
  coord_map = {coord: idx for idx, coord in enumerate(sorted_coords)}
  
  # Build Fenwick tree
  n = len(sorted_coords)
  fenwick = FenwickTree(n)
  
  results = []
  for query_type, *args in queries:
    if query_type == 'update':
      pos, value = args
      compressed_pos = coord_map[pos]
      fenwick.update(compressed_pos, value)
    elif query_type == 'query':
      left, right = args
      compressed_left = coord_map[left]
      compressed_right = coord_map[right]
      result = fenwick.range_query(compressed_left, compressed_right)
      results.append(result)
  
  return results
```

## Tips for Success

1. **Master Prefix Sums**: Foundation for range queries
2. **Understand Segment Trees**: Most versatile structure
3. **Learn Lazy Propagation**: Essential for updates
4. **Practice Implementation**: Code data structures
5. **Study Advanced Techniques**: Mo's algorithm, persistent structures
6. **Handle Edge Cases**: Empty ranges, single elements

## Common Pitfalls to Avoid

1. **Off-by-One Errors**: In range boundaries
2. **Memory Limits**: With large arrays
3. **Time Limits**: With inefficient updates
4. **Integer Overflow**: In sum calculations

## Advanced Topics

### Segment Tree Variations
- **Persistent Segment Tree**: Version control
- **Dynamic Segment Tree**: Space optimization
- **2D Segment Tree**: Matrix operations
- **Merge Sort Tree**: Range counting

### Optimization Techniques
- **Memory Optimization**: Space-efficient structures
- **Update Optimization**: Lazy propagation
- **Query Optimization**: Binary search
- **Batch Processing**: Offline algorithms

### Special Cases
- **Empty Ranges**: Handling edge cases
- **Large Numbers**: Modular arithmetic
- **Dynamic Ranges**: Online updates
- **Multiple Operations**: Combined queries

## 📚 **Additional Learning Resources**

### **LeetCode Pattern Integration**
For interview preparation and pattern recognition, complement your CSES learning with these LeetCode resources:

- **[Awesome LeetCode Resources](https://github.com/ashishps1/awesome-leetcode-resources)** - Comprehensive collection of LeetCode patterns, templates, and curated problem lists
- **[Prefix Sum Pattern](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Essential prefix sum and range query techniques
- **[Segment Tree Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Advanced data structure patterns for range operations

### **Related LeetCode Problems**
Practice these LeetCode problems to reinforce range query and data structure concepts:

- **Prefix Sum Pattern**: [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/), [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)
- **Binary Indexed Tree**: [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/), [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)
- **Segment Tree**: [Range Sum Query 2D - Mutable](https://leetcode.com/problems/range-sum-query-2d-mutable/), [My Calendar I](https://leetcode.com/problems/my-calendar-i/)
- **Sparse Table**: [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/), [Range Addition](https://leetcode.com/problems/range-addition/)

---

Ready to start? Begin with [Static Range Sum Queries](static_range_sum_queries_analysis) and work your way through the problems in order of difficulty!