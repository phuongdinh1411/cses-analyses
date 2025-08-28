---
layout: simple
title: CSES Hotel Queries - Problem Analysis
permalink: /problem_soulutions/range_queries/hotel_queries_analysis/
---

# CSES Hotel Queries - Problem Analysis

## Problem Statement
There are n hotels along a highway. For each group of tourists, you want to assign a hotel with the minimum number of rooms that can accommodate the group. Process q queries where each query asks for the first hotel that can accommodate a group of size x.

### Input
The first input line has two integers n and q: the number of hotels and the number of queries.
The second line has n integers h1,h2,…,hn: the number of rooms in each hotel.
Finally, there are q lines describing the queries. Each line has one integer x: the size of the group.

### Output
Print the answer to each query (1-indexed hotel number, or 0 if no hotel can accommodate).

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ hi ≤ 10^9
- 1 ≤ x ≤ 10^9

### Example
```
Input:
5 3
2 1 4 1 2
4
2
1

Output:
3
1
1
```

## Solution Progression

### Approach 1: Linear Search for Each Query - O(q × n)
**Description**: For each query, iterate through hotels from left to right to find the first one that can accommodate the group.

```python
def hotel_queries_naive(n, q, hotels, queries):
    results = []
    
    for x in queries:
        found = False
        for i in range(n):
            if hotels[i] >= x:
                results.append(i + 1)  # Convert to 1-indexed
                found = True
                break
        if not found:
            results.append(0)
    
    return results
```

**Why this is inefficient**: For each query, we need to iterate through all hotels, leading to O(q × n) time complexity.

### Improvement 1: Segment Tree with Range Maximum - O(n + q log n)
**Description**: Use Segment Tree to find the first hotel with sufficient rooms efficiently.

```python
def hotel_queries_segment_tree(n, q, hotels, queries):
    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [0] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = arr[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
        
        def find_first_ge(self, target):
            # Find the first position with value >= target
            return self._find_first_ge(1, 0, self.size - 1, target)
        
        def _find_first_ge(self, node, left, right, target):
            if left >= self.n:
                return -1
            
            if self.tree[node] < target:
                return -1
            
            if left == right:
                return left if left < self.n else -1
            
            mid = (left + right) // 2
            
            # Check left child first
            if self.tree[2 * node] >= target:
                result = self._find_first_ge(2 * node, left, mid, target)
                if result != -1:
                    return result
            
            # Check right child
            return self._find_first_ge(2 * node + 1, mid + 1, right, target)
    
    # Initialize Segment Tree
    st = SegmentTree(hotels)
    
    results = []
    for x in queries:
        pos = st.find_first_ge(x)
        if pos != -1:
            results.append(pos + 1)  # Convert to 1-indexed
        else:
            results.append(0)
    
    return results
```

**Why this improvement works**: Segment Tree allows us to find the first hotel with sufficient rooms in O(log n) time per query.

## Final Optimal Solution

```python
n, q = map(int, input().split())
hotels = list(map(int, input().split()))

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
    
    def find_first_ge(self, target):
        # Find the first position with value >= target
        return self._find_first_ge(1, 0, self.size - 1, target)
    
    def _find_first_ge(self, node, left, right, target):
        if left >= self.n:
            return -1
        
        if self.tree[node] < target:
            return -1
        
        if left == right:
            return left if left < self.n else -1
        
        mid = (left + right) // 2
        
        # Check left child first
        if self.tree[2 * node] >= target:
            result = self._find_first_ge(2 * node, left, mid, target)
            if result != -1:
                return result
        
        # Check right child
        return self._find_first_ge(2 * node + 1, mid + 1, right, target)

# Initialize Segment Tree
st = SegmentTree(hotels)

# Process queries
for _ in range(q):
    x = int(input())
    pos = st.find_first_ge(x)
    if pos != -1:
        print(pos + 1)  # Convert to 1-indexed
    else:
        print(0)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(1) | Linear search for each query |
| Segment Tree | O(n + q log n) | O(n) | Use Segment Tree for range queries |

## Key Insights for Other Problems

### 1. **First Occurrence Queries**
**Principle**: Use tree-based data structures to find first occurrence efficiently.
**Applicable to**: Search problems, range queries, tree-based algorithms

### 2. **Segment Tree for Range Queries**
**Principle**: Use Segment Tree to answer range queries and find first occurrence in O(log n) time.
**Applicable to**: Range problems, search problems, tree-based data structures

### 3. **Binary Search on Tree**
**Principle**: Use binary search traversal on tree to find first occurrence.
**Applicable to**: Search problems, tree traversal, optimization problems

## Notable Techniques

### 1. **Segment Tree with First Occurrence**
```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
    
    def find_first_ge(self, target):
        return self._find_first_ge(1, 0, self.size - 1, target)
    
    def _find_first_ge(self, node, left, right, target):
        if left >= self.n or self.tree[node] < target:
            return -1
        
        if left == right:
            return left if left < self.n else -1
        
        mid = (left + right) // 2
        
        # Check left child first
        if self.tree[2 * node] >= target:
            result = self._find_first_ge(2 * node, left, mid, target)
            if result != -1:
                return result
        
        # Check right child
        return self._find_first_ge(2 * node + 1, mid + 1, right, target)
```

### 2. **First Occurrence Pattern**
```python
def find_first_occurrence(segment_tree, target):
    return segment_tree.find_first_ge(target)
```

### 3. **Binary Search Traversal**
```python
def binary_search_tree(node, left, right, target):
    if left >= n or tree[node] < target:
        return -1
    
    if left == right:
        return left if left < n else -1
    
    mid = (left + right) // 2
    
    # Check left child first
    if tree[2 * node] >= target:
        result = binary_search_tree(2 * node, left, mid, target)
        if result != -1:
            return result
    
    # Check right child
    return binary_search_tree(2 * node + 1, mid + 1, right, target)
```

## Problem-Solving Framework

1. **Identify query type**: This is a first occurrence query problem
2. **Choose data structure**: Use Segment Tree for efficient range queries
3. **Build Segment Tree**: Create tree from hotel capacities
4. **Process queries**: Find first hotel with sufficient rooms using tree traversal
5. **Handle indexing**: Convert between 0-indexed and 1-indexed as needed

---

*This analysis shows how to efficiently find the first hotel with sufficient rooms using Segment Tree technique.* 