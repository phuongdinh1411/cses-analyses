---
layout: simple
title: "Dynamic Range Sum Queries - Segment Tree"
permalink: /problem_soulutions/range_queries/dynamic_range_sum_queries_analysis
---

# Dynamic Range Sum Queries - Segment Tree

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement segment tree for dynamic range queries
- Apply segment tree to efficiently handle range sum queries with updates
- Optimize range sum calculations using segment tree
- Handle edge cases in segment tree problems
- Recognize when to use segment tree vs other approaches

## 📋 Problem Description

Given an array of integers and multiple queries, each query can be either:
1. Update an element at position i to value v
2. Find the sum of elements in range [l, r]

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: 
  - "1 i v" for update (set arr[i] = v)
  - "2 l r" for query (sum of range [l, r])

**Output**: 
- For each query of type 2, print the sum of elements in range [l, r]

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- -10⁹ ≤ arr[i] ≤ 10⁹
- 1 ≤ i ≤ n, 1 ≤ l ≤ r ≤ n

**Example**:
```
Input:
5 3
1 2 3 4 5
2 1 3
1 2 10
2 1 3

Output:
6
14

Explanation**: 
Query 1: sum of [1,2,3] = 6
Update: arr[2] = 10
Query 2: sum of [1,10,3] = 14
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, if it's an update, update the array
2. If it's a range query, iterate through the range and sum elements
3. Return the sum

**Implementation**:
```python
def brute_force_dynamic_range_sum_queries(arr, queries):
    n = len(arr)
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            i, v = query[1], query[2]
            arr[i - 1] = v  # Convert to 0-indexed
        else:  # Range query
            l, r = query[1], query[2]
            # Convert to 0-indexed
            l -= 1
            r -= 1
            
            # Calculate sum in range [l, r]
            range_sum = 0
            for i in range(l, r + 1):
                range_sum += arr[i]
            
            results.append(range_sum)
    
    return results
```

### Approach 2: Optimized with Segment Tree
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Build segment tree where each node stores sum of its range
2. For updates, update the tree in O(log n) time
3. For range queries, query the tree in O(log n) time
4. Return the sum

**Implementation**:
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.build(arr, 1, 0, self.n - 1)
    
    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build(arr, 2 * node, start, mid)
            self.build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node, start, mid, idx, val)
            else:
                self.update(2 * node + 1, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self.query(2 * node, start, mid, l, r) + 
                self.query(2 * node + 1, mid + 1, end, l, r))

def optimized_dynamic_range_sum_queries(arr, queries):
    n = len(arr)
    st = SegmentTree(arr)
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            i, v = query[1], query[2]
            st.update(1, 0, n - 1, i - 1, v)  # Convert to 0-indexed
        else:  # Range query
            l, r = query[1], query[2]
            # Convert to 0-indexed
            l -= 1
            r -= 1
            
            range_sum = st.query(1, 0, n - 1, l, r)
            results.append(range_sum)
    
    return results
```

### Approach 3: Optimal with Segment Tree
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Build segment tree where each node stores sum of its range
2. For updates, update the tree in O(log n) time
3. For range queries, query the tree in O(log n) time
4. Return the sum

**Implementation**:
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.build(arr, 1, 0, self.n - 1)
    
    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build(arr, 2 * node, start, mid)
            self.build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node, start, mid, idx, val)
            else:
                self.update(2 * node + 1, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self.query(2 * node, start, mid, l, r) + 
                self.query(2 * node + 1, mid + 1, end, l, r))

def optimal_dynamic_range_sum_queries(arr, queries):
    n = len(arr)
    st = SegmentTree(arr)
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            i, v = query[1], query[2]
            st.update(1, 0, n - 1, i - 1, v)  # Convert to 0-indexed
        else:  # Range query
            l, r = query[1], query[2]
            # Convert to 0-indexed
            l -= 1
            r -= 1
            
            range_sum = st.query(1, 0, n - 1, l, r)
            results.append(range_sum)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Calculate sum for each query |
| Optimized | O(n + q log n) | O(n) | Use segment tree for O(log n) operations |
| Optimal | O(n + q log n) | O(n) | Use segment tree for O(log n) operations |

### Time Complexity
- **Time**: O(n + q log n) - O(n) construction + O(log n) per operation
- **Space**: O(n) - Segment tree

### Why This Solution Works
- **Segment Tree Property**: Each node stores sum of its range
- **Efficient Updates**: Update in O(log n) time by traversing tree
- **Fast Queries**: Query in O(log n) time by combining node values
- **Optimal Approach**: O(n + q log n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Dynamic Range Sum with Range Updates
**Problem**: Handle range updates (add value to all elements in range) and maintain range sum queries.

**Link**: [CSES Problem Set - Dynamic Range Sum with Range Updates](https://cses.fi/problemset/task/dynamic_range_sum_range_updates)

```python
class DynamicRangeSumWithRangeUpdates:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(arr, 0, 0, self.n - 1)
    
    def _build(self, arr, node, start, end):
        """Build segment tree"""
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self._build(arr, 2 * node + 1, start, mid)
            self._build(arr, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def _push_lazy(self, node, start, end):
        """Push lazy updates to children"""
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0
    
    def range_update(self, left, right, value):
        """Update range [left, right] by adding value"""
        self._range_update(0, 0, self.n - 1, left, right, value)
    
    def _range_update(self, node, start, end, left, right, value):
        """Internal range update function"""
        self._push_lazy(node, start, end)
        
        if start > right or end < left:
            return
        
        if left <= start and end <= right:
            self.lazy[node] += value
            self._push_lazy(node, start, end)
            return
        
        mid = (start + end) // 2
        self._range_update(2 * node + 1, start, mid, left, right, value)
        self._range_update(2 * node + 2, mid + 1, end, left, right, value)
        
        self._push_lazy(2 * node + 1, start, mid)
        self._push_lazy(2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def range_query(self, left, right):
        """Query sum of range [left, right]"""
        return self._range_query(0, 0, self.n - 1, left, right)
    
    def _range_query(self, node, start, end, left, right):
        """Internal range query function"""
        self._push_lazy(node, start, end)
        
        if start > right or end < left:
            return 0
        
        if left <= start and end <= right:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self._range_query(2 * node + 1, start, mid, left, right)
        right_sum = self._range_query(2 * node + 2, mid + 1, end, left, right)
        
        return left_sum + right_sum
```

### Variation 2: Dynamic Range Sum with Multiple Operations
**Problem**: Handle multiple types of operations (point updates, range updates, range queries) efficiently.

**Link**: [CSES Problem Set - Dynamic Range Sum Multiple Operations](https://cses.fi/problemset/task/dynamic_range_sum_multiple_ops)

```python
class DynamicRangeSumMultipleOps:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(arr, 0, 0, self.n - 1)
    
    def _build(self, arr, node, start, end):
        """Build segment tree"""
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self._build(arr, 2 * node + 1, start, mid)
            self._build(arr, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def point_update(self, index, value):
        """Update element at index to value"""
        self._point_update(0, 0, self.n - 1, index, value)
    
    def _point_update(self, node, start, end, index, value):
        """Internal point update function"""
        if start == end:
            self.tree[node] = value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._point_update(2 * node + 1, start, mid, index, value)
            else:
                self._point_update(2 * node + 2, mid + 1, end, index, value)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def range_query(self, left, right):
        """Query sum of range [left, right]"""
        return self._range_query(0, 0, self.n - 1, left, right)
    
    def _range_query(self, node, start, end, left, right):
        """Internal range query function"""
        if start > right or end < left:
            return 0
        
        if left <= start and end <= right:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self._range_query(2 * node + 1, start, mid, left, right)
        right_sum = self._range_query(2 * node + 2, mid + 1, end, left, right)
        
        return left_sum + right_sum
```

### Variation 3: Dynamic Range Sum with Constraints
**Problem**: Handle range sum queries with additional constraints (e.g., maximum sum, minimum length).

**Link**: [CSES Problem Set - Dynamic Range Sum with Constraints](https://cses.fi/problemset/task/dynamic_range_sum_constraints)

```python
class DynamicRangeSumWithConstraints:
    def __init__(self, arr, max_sum, min_length):
        self.n = len(arr)
        self.max_sum = max_sum
        self.min_length = min_length
        self.tree = [0] * (4 * self.n)
        self._build(arr, 0, 0, self.n - 1)
    
    def _build(self, arr, node, start, end):
        """Build segment tree"""
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self._build(arr, 2 * node + 1, start, mid)
            self._build(arr, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def constrained_range_query(self, left, right):
        """Query sum of range [left, right] with constraints"""
        # Check minimum length constraint
        if right - left + 1 < self.min_length:
            return None  # Invalid range
        
        # Get sum
        sum_value = self._range_query(0, 0, self.n - 1, left, right)
        
        # Check maximum sum constraint
        if sum_value > self.max_sum:
            return None  # Exceeds maximum sum
        
        return sum_value
    
    def _range_query(self, node, start, end, left, right):
        """Internal range query function"""
        if start > right or end < left:
            return 0
        
        if left <= start and end <= right:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self._range_query(2 * node + 1, start, mid, left, right)
        right_sum = self._range_query(2 * node + 2, mid + 1, end, left, right)
        
        return left_sum + right_sum
```

### Related Problems

#### **CSES Problems**
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Basic dynamic range sum problem
- [Range Update Queries](https://cses.fi/problemset/task/1651) - Range update queries
- [Range Sum Queries II](https://cses.fi/problemset/task/1649) - Range sum with updates

#### **LeetCode Problems**
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates
- [Range Sum Query 2D - Mutable](https://leetcode.com/problems/range-sum-query-2d-mutable/) - 2D range sum with updates
- [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) - Range query with updates

#### **Problem Categories**
- **Segment Trees**: Dynamic range queries, range updates, lazy propagation
- **Binary Indexed Trees**: Point updates, range queries, efficient data structures
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Algorithm Design**: Segment tree techniques, lazy propagation, range optimization