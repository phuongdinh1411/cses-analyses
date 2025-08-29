---
layout: simple
title: "Range Queries"
permalink: /cses-analyses/problem_soulutions/range_queries
---

# Range Queries

Welcome to the Range Queries section! This category focuses on efficiently answering queries about ranges or intervals in arrays and data structures.

## Overview

Range Queries help you master:
- **Efficient data structures** for range operations
- **Query processing** and optimization techniques
- **Lazy propagation** and update strategies
- **Advanced algorithms** for complex range problems

## Topics Covered

### 📊 **Basic Range Operations**
- **Static Range Sum Queries** - Prefix sums
- **Static Range Minimum Queries** - Sparse table
- **Dynamic Range Sum Queries** - Binary indexed tree
- **Dynamic Range Update Queries** - Difference array

### 🔍 **Advanced Range Queries**
- **Range XOR Queries** - XOR properties with BIT
- **Range Interval Queries** - Interval data structures
- **Forest Queries** - 2D range queries
- **Hotel Queries** - Binary search with range queries

### 📈 **Complex Range Problems**
- **Salary Queries** - Order statistic tree
- **List Removals** - Dynamic array with queries
- **Pizzeria Queries** - 2D range queries
- **Subarray Sum Queries** - Segment tree with lazy propagation

### 🔢 **Specialized Range Algorithms**
- **Subarray Distinct Values Queries** - Mo's algorithm
- **Subarray Minimum Queries** - Monotonic stack
- **Subarray Mode Queries** - Frequency analysis
- **Subarray OR Queries** - Bit manipulation
- **Visible Buildings Queries** - Monotonic stack

## Learning Path

### 🟢 **Beginner Level** (Start Here)
1. **Static Range Sum Queries** - Prefix sums
2. **Static Range Minimum Queries** - Sparse table
3. **Dynamic Range Sum Queries** - Binary indexed tree
4. **Dynamic Range Update Queries** - Difference array

### 🟡 **Intermediate Level**
1. **Range XOR Queries** - XOR with BIT
2. **Range Interval Queries** - Interval trees
3. **Forest Queries** - 2D prefix sums
4. **Hotel Queries** - Binary search + range queries

### 🔴 **Advanced Level**
1. **Salary Queries** - Order statistic tree
2. **Subarray Sum Queries** - Segment tree with lazy propagation
3. **Subarray Distinct Values Queries** - Mo's algorithm
4. **Visible Buildings Queries** - Monotonic stack

## Key Concepts

### 📊 **Data Structures**
- **Prefix Sums**: `O(1)` range sum queries, `O(n)` updates
- **Binary Indexed Tree (Fenwick)**: `O(log n)` queries and updates
- **Segment Tree**: `O(log n)` queries and updates, supports lazy propagation
- **Sparse Table**: `O(1)` range min/max queries, static data

### 🔄 **Update Strategies**
- **Point Updates**: Update single element
- **Range Updates**: Update entire range efficiently
- **Lazy Propagation**: Defer updates until needed
- **Difference Array**: Efficient range updates

### 🎯 **Query Types**
- **Aggregation**: Sum, min, max, count
- **Existence**: Contains element, distinct values
- **Order Statistics**: k-th smallest element
- **Geometric**: 2D range queries

## Algorithmic Techniques

### 📊 **Prefix Sums**
```python
def prefix_sum(arr):
    n = len(arr)
    prefix = [0] * (n + 1)
    
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    return prefix

def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

### 🌳 **Binary Indexed Tree**
```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, idx, val):
        while idx <= self.n:
            self.tree[idx] += val
            idx += idx & -idx
    
    def query(self, idx):
        result = 0
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & -idx
        return result
    
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)
```

### 🏗️ **Segment Tree**
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        
        # Build tree
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    
    def update(self, idx, val):
        idx += self.size
        self.tree[idx] = val
        idx //= 2
        while idx >= 1:
            self.tree[idx] = self.tree[2 * idx] + self.tree[2 * idx + 1]
            idx //= 2
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result = 0
        while left <= right:
            if left % 2 == 1:
                result += self.tree[left]
                left += 1
            if right % 2 == 0:
                result += self.tree[right]
                right -= 1
            left //= 2
            right //= 2
        return result
```

### 🔍 **Sparse Table (RMQ)**
```python
class SparseTable:
    def __init__(self, arr):
        self.n = len(arr)
        self.k = 20  # log2(10^6) ≈ 20
        self.st = [[0] * self.n for _ in range(self.k)]
        
        # Initialize first row
        for i in range(self.n):
            self.st[0][i] = arr[i]
        
        # Build sparse table
        for j in range(1, self.k):
            for i in range(self.n - (1 << j) + 1):
                self.st[j][i] = min(self.st[j-1][i], 
                                   self.st[j-1][i + (1 << (j-1))])
    
    def query(self, left, right):
        length = right - left + 1
        k = 0
        while (1 << (k + 1)) <= length:
            k += 1
        return min(self.st[k][left], 
                   self.st[k][right - (1 << k) + 1])
```

### 🎯 **Mo's Algorithm**
```python
def mo_algorithm(queries, arr):
    block_size = int(len(arr) ** 0.5)
    
    # Sort queries by block
    def get_block(x):
        return x // block_size
    
    queries.sort(key=lambda q: (get_block(q[0]), q[1]))
    
    current_l, current_r = 0, -1
    current_ans = 0
    answers = [0] * len(queries)
    
    for i, (left, right) in enumerate(queries):
        # Expand/shrink window
        while current_l > left:
            current_l -= 1
            current_ans += arr[current_l]
        while current_r < right:
            current_r += 1
            current_ans += arr[current_r]
        while current_l < left:
            current_ans -= arr[current_l]
            current_l += 1
        while current_r > right:
            current_ans -= arr[current_r]
            current_r -= 1
        
        answers[i] = current_ans
    
    return answers
```

## Common Range Query Patterns

### 📊 **1D Range Queries**
- **Static**: Prefix sums, sparse table
- **Dynamic**: Binary indexed tree, segment tree
- **Aggregation**: Sum, min, max, count, mode

### 🏗️ **2D Range Queries**
- **2D Prefix Sums**: `O(1)` queries, `O(n²)` preprocessing
- **2D Binary Indexed Tree**: `O(log² n)` queries and updates
- **2D Segment Tree**: `O(log² n)` queries and updates

### 🔄 **Range Updates**
- **Difference Array**: `O(1)` range updates, `O(n)` point queries
- **Lazy Propagation**: `O(log n)` range updates and queries
- **Persistent Data Structures**: Handle multiple versions

## Tips for Success

1. **Choose Data Structure**: Match complexity requirements with appropriate DS
2. **Handle Edge Cases**: Empty ranges, single elements, boundary conditions
3. **Optimize Updates**: Use lazy propagation for range updates
4. **Consider Space**: Sparse table vs segment tree trade-offs
5. **Use Specialized Algorithms**: Mo's for offline queries, persistent DS for history

## Related Topics

After mastering range queries, explore:
- **Advanced Graph Problems** - Range queries on trees
- **String Algorithms** - Pattern matching with range queries
- **Competitive Programming** - Complex optimization problems
- **Data Structures** - Advanced tree and graph structures

---

*Ready to master efficient query processing? Start with the beginner problems and build your range query skills!* 