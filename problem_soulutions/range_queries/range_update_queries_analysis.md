---
layout: simple
title: "Range Update Queries - Lazy Propagation"
permalink: /problem_soulutions/range_queries/range_update_queries_analysis
---

# Range Update Queries - Lazy Propagation

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement lazy propagation for range updates
- Apply lazy propagation to efficiently handle range update queries
- Optimize range update calculations using lazy propagation
- Handle edge cases in lazy propagation problems
- Recognize when to use lazy propagation vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Segment tree, lazy propagation, range updates
- **Data Structures**: Arrays, segment trees, lazy arrays
- **Mathematical Concepts**: Range update optimization, tree data structures
- **Programming Skills**: Array manipulation, lazy propagation implementation
- **Related Problems**: Dynamic range sum queries, range interval queries, segment tree problems

## 📋 Problem Description

Given an array of integers and multiple queries, each query can be either:
1. Update all elements in range [l, r] by adding value v
2. Find the sum of elements in range [l, r]

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: 
  - "1 l r v" for range update (add v to all elements in [l, r])
  - "2 l r" for query (sum of range [l, r])

**Output**: 
- For each query of type 2, print the sum of elements in range [l, r]

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- -10⁹ ≤ arr[i] ≤ 10⁹
- 1 ≤ l ≤ r ≤ n

**Example**:
```
Input:
5 3
1 2 3 4 5
2 1 3
1 2 4 10
2 1 3

Output:
6
26

Explanation**: 
Query 1: sum of [1,2,3] = 6
Update: add 10 to [2,3,4] → [1,12,13,14,5]
Query 2: sum of [1,12,13] = 26
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, if it's a range update, update all elements in range
2. If it's a range query, iterate through the range and sum elements
3. Return the sum

**Implementation**:
```python
def brute_force_range_update_queries(arr, queries):
    n = len(arr)
    results = []
    
    for query in queries:
        if query[0] == 1:  # Range update
            l, r, v = query[1], query[2], query[3]
            # Convert to 0-indexed
            l -= 1
            r -= 1
            
            # Update all elements in range [l, r]
            for i in range(l, r + 1):
                arr[i] += v
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

### Approach 2: Optimized with Lazy Propagation
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Build segment tree with lazy propagation
2. For range updates, use lazy propagation to defer updates
3. For range queries, propagate lazy updates and query
4. Return the sum

**Implementation**:
```python
class LazySegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(arr, 1, 0, self.n - 1)
    
    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build(arr, 2 * node, start, mid)
            self.build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def push(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0
    
    def update_range(self, node, start, end, l, r, val):
        self.push(node, start, end)
        if r < start or end < l:
            return
        if l <= start and end <= r:
            self.lazy[node] += val
            self.push(node, start, end)
            return
        mid = (start + end) // 2
        self.update_range(2 * node, start, mid, l, r, val)
        self.update_range(2 * node + 1, mid + 1, end, l, r, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def query_range(self, node, start, end, l, r):
        self.push(node, start, end)
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self.query_range(2 * node, start, mid, l, r) + 
                self.query_range(2 * node + 1, mid + 1, end, l, r))

def optimized_range_update_queries(arr, queries):
    n = len(arr)
    st = LazySegmentTree(arr)
    results = []
    
    for query in queries:
        if query[0] == 1:  # Range update
            l, r, v = query[1], query[2], query[3]
            # Convert to 0-indexed
            l -= 1
            r -= 1
            st.update_range(1, 0, n - 1, l, r, v)
        else:  # Range query
            l, r = query[1], query[2]
            # Convert to 0-indexed
            l -= 1
            r -= 1
            range_sum = st.query_range(1, 0, n - 1, l, r)
            results.append(range_sum)
    
    return results
```

### Approach 3: Optimal with Lazy Propagation
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Build segment tree with lazy propagation
2. For range updates, use lazy propagation to defer updates
3. For range queries, propagate lazy updates and query
4. Return the sum

**Implementation**:
```python
class LazySegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(arr, 1, 0, self.n - 1)
    
    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build(arr, 2 * node, start, mid)
            self.build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def push(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0
    
    def update_range(self, node, start, end, l, r, val):
        self.push(node, start, end)
        if r < start or end < l:
            return
        if l <= start and end <= r:
            self.lazy[node] += val
            self.push(node, start, end)
            return
        mid = (start + end) // 2
        self.update_range(2 * node, start, mid, l, r, val)
        self.update_range(2 * node + 1, mid + 1, end, l, r, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def query_range(self, node, start, end, l, r):
        self.push(node, start, end)
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self.query_range(2 * node, start, mid, l, r) + 
                self.query_range(2 * node + 1, mid + 1, end, l, r))

def optimal_range_update_queries(arr, queries):
    n = len(arr)
    st = LazySegmentTree(arr)
    results = []
    
    for query in queries:
        if query[0] == 1:  # Range update
            l, r, v = query[1], query[2], query[3]
            # Convert to 0-indexed
            l -= 1
            r -= 1
            st.update_range(1, 0, n - 1, l, r, v)
        else:  # Range query
            l, r = query[1], query[2]
            # Convert to 0-indexed
            l -= 1
            r -= 1
            range_sum = st.query_range(1, 0, n - 1, l, r)
            results.append(range_sum)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Update and query each element |
| Optimized | O(n + q log n) | O(n) | Use lazy propagation for O(log n) operations |
| Optimal | O(n + q log n) | O(n) | Use lazy propagation for O(log n) operations |

### Time Complexity
- **Time**: O(n + q log n) - O(n) construction + O(log n) per operation
- **Space**: O(n) - Segment tree with lazy array

### Why This Solution Works
- **Lazy Propagation**: Defer updates until they are needed
- **Efficient Updates**: Update ranges in O(log n) time
- **Fast Queries**: Query ranges in O(log n) time
- **Optimal Approach**: O(n + q log n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Range Update Queries with Point Queries
**Problem**: Handle range updates and answer point queries (single element values).

**Link**: [CSES Problem Set - Range Update Point Queries](https://cses.fi/problemset/task/range_update_point_queries)

```python
class RangeUpdatePointQueries:
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
    
    def point_query(self, index):
        """Query value at index"""
        return self._point_query(0, 0, self.n - 1, index)
    
    def _point_query(self, node, start, end, index):
        """Internal point query function"""
        self._push_lazy(node, start, end)
        
        if start == end:
            return self.tree[node]
        
        mid = (start + end) // 2
        if index <= mid:
            return self._point_query(2 * node + 1, start, mid, index)
        else:
            return self._point_query(2 * node + 2, mid + 1, end, index)
```

### Variation 2: Range Update Queries with Range Queries
**Problem**: Handle range updates and answer range sum queries efficiently.

**Link**: [CSES Problem Set - Range Update Range Queries](https://cses.fi/problemset/task/range_update_range_queries)

```python
class RangeUpdateRangeQueries:
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

### Variation 3: Range Update Queries with Constraints
**Problem**: Handle range updates with additional constraints (e.g., maximum update value, minimum range size).

**Link**: [CSES Problem Set - Range Update Queries with Constraints](https://cses.fi/problemset/task/range_update_queries_constraints)

```python
class RangeUpdateQueriesWithConstraints:
    def __init__(self, arr, max_update_value, min_range_size):
        self.n = len(arr)
        self.max_update_value = max_update_value
        self.min_range_size = min_range_size
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
    
    def constrained_range_update(self, left, right, value):
        """Update range [left, right] by adding value with constraints"""
        # Check minimum range size constraint
        if right - left + 1 < self.min_range_size:
            return False  # Invalid range size
        
        # Check maximum update value constraint
        if value > self.max_update_value:
            return False  # Exceeds maximum update value
        
        self._range_update(0, 0, self.n - 1, left, right, value)
        return True
    
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

### Related Problems

#### **CSES Problems**
- [Range Update Queries](https://cses.fi/problemset/task/1651) - Basic range update queries problem
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Dynamic range sum with updates
- [Range Sum Queries II](https://cses.fi/problemset/task/1649) - Range sum with updates

#### **LeetCode Problems**
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates
- [Range Sum Query 2D - Mutable](https://leetcode.com/problems/range-sum-query-2d-mutable/) - 2D range sum with updates
- [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) - Range query with updates

#### **Problem Categories**
- **Lazy Propagation**: Range updates, efficient update propagation, segment trees
- **Segment Trees**: Range operations, update handling, query processing
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Algorithm Design**: Lazy propagation techniques, range optimization, update handling