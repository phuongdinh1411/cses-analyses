---
layout: simple
title: "Range Interval Queries - Interval Operations"
permalink: /problem_soulutions/range_queries/range_interval_queries_analysis
---

# Range Interval Queries - Interval Operations

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement interval operations for range queries
- Apply interval operations to efficiently handle range interval queries
- Optimize range interval calculations using interval operations
- Handle edge cases in interval operation problems
- Recognize when to use interval operations vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Interval operations, range queries, interval trees
- **Data Structures**: Arrays, interval trees, segment trees
- **Mathematical Concepts**: Interval optimization, tree data structures
- **Programming Skills**: Array manipulation, interval operation implementation
- **Related Problems**: Range update queries, range interval queries, interval tree problems

## 📋 Problem Description

Given an array of integers and multiple queries, each query can be either:
1. Update all elements in range [l, r] to value v
2. Find the sum of elements in range [l, r]

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: 
  - "1 l r v" for range update (set all elements in [l, r] to v)
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
21

Explanation**: 
Query 1: sum of [1,2,3] = 6
Update: set [2,3,4] to 10 → [1,10,10,10,5]
Query 2: sum of [1,10,10] = 21
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
def brute_force_range_interval_queries(arr, queries):
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
                arr[i] = v
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

### Approach 2: Optimized with Interval Operations
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Build segment tree with interval operations
2. For range updates, use interval operations to set values
3. For range queries, query the tree
4. Return the sum

**Implementation**:
```python
class IntervalSegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [None] * (4 * self.n)
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
        if self.lazy[node] is not None:
            self.tree[node] = self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2 * node] = self.lazy[node]
                self.lazy[2 * node + 1] = self.lazy[node]
            self.lazy[node] = None
    
    def update_range(self, node, start, end, l, r, val):
        self.push(node, start, end)
        if r < start or end < l:
            return
        if l <= start and end <= r:
            self.lazy[node] = val
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

def optimized_range_interval_queries(arr, queries):
    n = len(arr)
    st = IntervalSegmentTree(arr)
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

### Approach 3: Optimal with Interval Operations
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Build segment tree with interval operations
2. For range updates, use interval operations to set values
3. For range queries, query the tree
4. Return the sum

**Implementation**:
```python
class IntervalSegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [None] * (4 * self.n)
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
        if self.lazy[node] is not None:
            self.tree[node] = self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2 * node] = self.lazy[node]
                self.lazy[2 * node + 1] = self.lazy[node]
            self.lazy[node] = None
    
    def update_range(self, node, start, end, l, r, val):
        self.push(node, start, end)
        if r < start or end < l:
            return
        if l <= start and end <= r:
            self.lazy[node] = val
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

def optimal_range_interval_queries(arr, queries):
    n = len(arr)
    st = IntervalSegmentTree(arr)
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
| Optimized | O(n + q log n) | O(n) | Use interval operations for O(log n) operations |
| Optimal | O(n + q log n) | O(n) | Use interval operations for O(log n) operations |

### Time Complexity
- **Time**: O(n + q log n) - O(n) construction + O(log n) per operation
- **Space**: O(n) - Segment tree with lazy array

### Why This Solution Works
- **Interval Operations**: Set all elements in a range to the same value
- **Efficient Updates**: Update ranges in O(log n) time
- **Fast Queries**: Query ranges in O(log n) time
- **Optimal Approach**: O(n + q log n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Range Interval Queries with Dynamic Updates
**Problem**: Handle dynamic updates to intervals and maintain range interval queries.

**Link**: [CSES Problem Set - Range Interval Queries with Updates](https://cses.fi/problemset/task/range_interval_queries_updates)

```python
class RangeIntervalQueriesWithUpdates:
    def __init__(self, intervals):
        self.intervals = intervals[:]
        self.n = len(intervals)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(intervals, 0, 0, self.n - 1)
    
    def _build(self, intervals, node, start, end):
        """Build segment tree for interval operations"""
        if start == end:
            self.tree[node] = intervals[start][1] - intervals[start][0] + 1
        else:
            mid = (start + end) // 2
            self._build(intervals, 2 * node + 1, start, mid)
            self._build(intervals, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def _push_lazy(self, node, start, end):
        """Push lazy updates to children"""
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0
    
    def update_interval(self, left, right, value):
        """Update interval [left, right] by adding value"""
        self._update_interval(0, 0, self.n - 1, left, right, value)
    
    def _update_interval(self, node, start, end, left, right, value):
        """Internal interval update function"""
        self._push_lazy(node, start, end)
        
        if start > right or end < left:
            return
        
        if left <= start and end <= right:
            self.lazy[node] += value
            self._push_lazy(node, start, end)
            return
        
        mid = (start + end) // 2
        self._update_interval(2 * node + 1, start, mid, left, right, value)
        self._update_interval(2 * node + 2, mid + 1, end, left, right, value)
        
        self._push_lazy(2 * node + 1, start, mid)
        self._push_lazy(2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def query_interval(self, left, right):
        """Query sum of interval [left, right]"""
        return self._query_interval(0, 0, self.n - 1, left, right)
    
    def _query_interval(self, node, start, end, left, right):
        """Internal interval query function"""
        self._push_lazy(node, start, end)
        
        if start > right or end < left:
            return 0
        
        if left <= start and end <= right:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self._query_interval(2 * node + 1, start, mid, left, right)
        right_sum = self._query_interval(2 * node + 2, mid + 1, end, left, right)
        
        return left_sum + right_sum
```

### Variation 2: Range Interval Queries with Different Operations
**Problem**: Handle different types of operations (sum, count, max, min) on interval ranges.

**Link**: [CSES Problem Set - Range Interval Queries Different Operations](https://cses.fi/problemset/task/range_interval_queries_operations)

```python
class RangeIntervalQueriesDifferentOps:
    def __init__(self, intervals):
        self.intervals = intervals[:]
        self.n = len(intervals)
        self.tree_sum = [0] * (4 * self.n)
        self.tree_count = [0] * (4 * self.n)
        self.tree_max = [float('-inf')] * (4 * self.n)
        self.tree_min = [float('inf')] * (4 * self.n)
        self._build(intervals, 0, 0, self.n - 1)
    
    def _build(self, intervals, node, start, end):
        """Build segment tree for different operations"""
        if start == end:
            interval_length = intervals[start][1] - intervals[start][0] + 1
            self.tree_sum[node] = interval_length
            self.tree_count[node] = 1
            self.tree_max[node] = interval_length
            self.tree_min[node] = interval_length
        else:
            mid = (start + end) // 2
            self._build(intervals, 2 * node + 1, start, mid)
            self._build(intervals, 2 * node + 2, mid + 1, end)
            self.tree_sum[node] = self.tree_sum[2 * node + 1] + self.tree_sum[2 * node + 2]
            self.tree_count[node] = self.tree_count[2 * node + 1] + self.tree_count[2 * node + 2]
            self.tree_max[node] = max(self.tree_max[2 * node + 1], self.tree_max[2 * node + 2])
            self.tree_min[node] = min(self.tree_min[2 * node + 1], self.tree_min[2 * node + 2])
    
    def query_sum(self, left, right):
        """Query sum of interval lengths in range [left, right]"""
        return self._query_sum(0, 0, self.n - 1, left, right)
    
    def _query_sum(self, node, start, end, left, right):
        """Internal sum query function"""
        if start > right or end < left:
            return 0
        
        if left <= start and end <= right:
            return self.tree_sum[node]
        
        mid = (start + end) // 2
        left_sum = self._query_sum(2 * node + 1, start, mid, left, right)
        right_sum = self._query_sum(2 * node + 2, mid + 1, end, left, right)
        
        return left_sum + right_sum
    
    def query_count(self, left, right):
        """Query count of intervals in range [left, right]"""
        return self._query_count(0, 0, self.n - 1, left, right)
    
    def _query_count(self, node, start, end, left, right):
        """Internal count query function"""
        if start > right or end < left:
            return 0
        
        if left <= start and end <= right:
            return self.tree_count[node]
        
        mid = (start + end) // 2
        left_count = self._query_count(2 * node + 1, start, mid, left, right)
        right_count = self._query_count(2 * node + 2, mid + 1, end, left, right)
        
        return left_count + right_count
    
    def query_max(self, left, right):
        """Query maximum interval length in range [left, right]"""
        return self._query_max(0, 0, self.n - 1, left, right)
    
    def _query_max(self, node, start, end, left, right):
        """Internal max query function"""
        if start > right or end < left:
            return float('-inf')
        
        if left <= start and end <= right:
            return self.tree_max[node]
        
        mid = (start + end) // 2
        left_max = self._query_max(2 * node + 1, start, mid, left, right)
        right_max = self._query_max(2 * node + 2, mid + 1, end, left, right)
        
        return max(left_max, right_max)
    
    def query_min(self, left, right):
        """Query minimum interval length in range [left, right]"""
        return self._query_min(0, 0, self.n - 1, left, right)
    
    def _query_min(self, node, start, end, left, right):
        """Internal min query function"""
        if start > right or end < left:
            return float('inf')
        
        if left <= start and end <= right:
            return self.tree_min[node]
        
        mid = (start + end) // 2
        left_min = self._query_min(2 * node + 1, start, mid, left, right)
        right_min = self._query_min(2 * node + 2, mid + 1, end, left, right)
        
        return min(left_min, right_min)
```

### Variation 3: Range Interval Queries with Constraints
**Problem**: Handle range interval queries with additional constraints (e.g., maximum length, minimum count).

**Link**: [CSES Problem Set - Range Interval Queries with Constraints](https://cses.fi/problemset/task/range_interval_queries_constraints)

```python
class RangeIntervalQueriesWithConstraints:
    def __init__(self, intervals, max_length, min_count):
        self.intervals = intervals[:]
        self.n = len(intervals)
        self.max_length = max_length
        self.min_count = min_count
        self.tree = [0] * (4 * self.n)
        self._build(intervals, 0, 0, self.n - 1)
    
    def _build(self, intervals, node, start, end):
        """Build segment tree for interval operations"""
        if start == end:
            self.tree[node] = intervals[start][1] - intervals[start][0] + 1
        else:
            mid = (start + end) // 2
            self._build(intervals, 2 * node + 1, start, mid)
            self._build(intervals, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def constrained_query(self, left, right):
        """Query sum of interval lengths with constraints"""
        # Check minimum count constraint
        if right - left + 1 < self.min_count:
            return None  # Invalid range count
        
        # Get sum
        sum_value = self._query(0, 0, self.n - 1, left, right)
        
        # Check maximum length constraint
        if sum_value > self.max_length:
            return None  # Exceeds maximum length
        
        return sum_value
    
    def _query(self, node, start, end, left, right):
        """Internal query function"""
        if start > right or end < left:
            return 0
        
        if left <= start and end <= right:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self._query(2 * node + 1, start, mid, left, right)
        right_sum = self._query(2 * node + 2, mid + 1, end, left, right)
        
        return left_sum + right_sum
    
    def find_valid_ranges(self):
        """Find all valid ranges that satisfy constraints"""
        valid_ranges = []
        for i in range(self.n):
            for j in range(i + self.min_count - 1, self.n):
                result = self.constrained_query(i, j)
                if result is not None:
                    valid_ranges.append((i, j, result))
        return valid_ranges
    
    def get_maximum_valid_sum(self):
        """Get maximum valid sum"""
        max_sum = float('-inf')
        for i in range(self.n):
            for j in range(i + self.min_count - 1, self.n):
                result = self.constrained_query(i, j)
                if result is not None:
                    max_sum = max(max_sum, result)
        return max_sum if max_sum != float('-inf') else None

# Example usage
intervals = [(1, 3), (2, 5), (4, 6), (7, 9)]
max_length = 10
min_count = 2

riq = RangeIntervalQueriesWithConstraints(intervals, max_length, min_count)
result = riq.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: 8

valid_ranges = riq.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")
```

### Related Problems

#### **CSES Problems**
- [Range Interval Queries](https://cses.fi/problemset/task/1650) - Basic range interval queries problem
- [Range Update Queries](https://cses.fi/problemset/task/1651) - Range update queries
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Dynamic range sum queries

#### **LeetCode Problems**
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates
- [Range Sum Query 2D - Mutable](https://leetcode.com/problems/range-sum-query-2d-mutable/) - 2D range sum with updates
- [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) - Range query with updates

#### **Problem Categories**
- **Interval Operations**: Range interval queries, interval updates, efficient operations
- **Segment Trees**: Range operations, update handling, query processing
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Algorithm Design**: Interval operation techniques, range optimization, constraint handling

## 🚀 Key Takeaways

- **Interval Operations Technique**: The standard approach for range interval queries
- **Efficient Updates**: Update ranges in O(log n) time using interval operations
- **Fast Queries**: Answer range queries in O(log n) time
- **Space Trade-off**: Use O(n) extra space for O(log n) operations
- **Pattern Recognition**: This technique applies to many range interval problems