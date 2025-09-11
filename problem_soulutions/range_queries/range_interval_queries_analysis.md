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

## 🚀 Key Takeaways

- **Interval Operations Technique**: The standard approach for range interval queries
- **Efficient Updates**: Update ranges in O(log n) time using interval operations
- **Fast Queries**: Answer range queries in O(log n) time
- **Space Trade-off**: Use O(n) extra space for O(log n) operations
- **Pattern Recognition**: This technique applies to many range interval problems