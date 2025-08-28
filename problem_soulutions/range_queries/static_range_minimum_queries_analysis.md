---
layout: simple
title: CSES Static Range Minimum Queries - Problem Analysis
permalink: /problem_soulutions/range_queries/static_range_minimum_queries_analysis/
---

# CSES Static Range Minimum Queries - Problem Analysis

## Problem Statement
Given an array of n integers, process q queries. Each query asks for the minimum value in a range [a,b].

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x1,x2,…,xn: the contents of the array.
Finally, there are q lines describing the queries. Each line has two integers a and b: the range [a,b].

### Output
Print the answer to each query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9
- 1 ≤ a ≤ b ≤ n

### Example
```
Input:
8 4
3 2 4 5 1 1 5 3
2 4
5 6
1 8
3 3

Output:
2
1
1
4
```

## Solution Progression

### Approach 1: Find Minimum for Each Query - O(q × n)
**Description**: For each query, iterate through the range and find the minimum value.

```python
def static_range_min_naive(n, q, arr, queries):
    results = []
    
    for a, b in queries:
        # Convert to 0-indexed
        start, end = a - 1, b - 1
        min_val = float('inf')
        
        for i in range(start, end + 1):
            min_val = min(min_val, arr[i])
        
        results.append(min_val)
    
    return results
```

**Why this is inefficient**: For each query, we need to iterate through the entire range, leading to O(q × n) time complexity.

### Improvement 1: Sparse Table - O(n log n + q)
**Description**: Use sparse table (ST) to preprocess the array for range minimum queries.

```python
def static_range_min_sparse_table(n, q, arr, queries):
    # Build sparse table
    log_n = 20  # Sufficient for n up to 10^6
    st = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        st[0][i] = arr[i]
    
    # Build sparse table
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st[j][i] = min(st[j-1][i], st[j-1][i + (1 << (j-1))])
    
    # Process queries
    results = []
    for a, b in queries:
        # Convert to 0-indexed
        left, right = a - 1, b - 1
        length = right - left + 1
        k = 0
        while (1 << (k + 1)) <= length:
            k += 1
        
        min_val = min(st[k][left], st[k][right - (1 << k) + 1])
        results.append(min_val)
    
    return results
```

**Why this improvement works**: Sparse table allows us to answer range minimum queries in O(1) time by precomputing minimums for all power-of-2 length ranges.

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Range Minimum with Updates**
**Problem**: Allow point updates to the array while still answering range minimum queries efficiently.
```python
def range_min_with_updates(n, q, arr, operations):
    # Use Segment Tree for dynamic RMQ
    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [float('inf')] * (4 * self.n)
            self.build(arr, 1, 0, self.n - 1)
        
        def build(self, arr, node, start, end):
            if start == end:
                self.tree[node] = arr[start]
            else:
                mid = (start + end) // 2
                self.build(arr, 2 * node, start, mid)
                self.build(arr, 2 * node + 1, mid + 1, end)
                self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
        
        def update(self, node, start, end, idx, val):
            if start == end:
                self.tree[node] = val
            else:
                mid = (start + end) // 2
                if idx <= mid:
                    self.update(2 * node, start, mid, idx, val)
                else:
                    self.update(2 * node + 1, mid + 1, end, idx, val)
                self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
        
        def query(self, node, start, end, l, r):
            if r < start or l > end:
                return float('inf')
            if l <= start and end <= r:
                return self.tree[node]
            mid = (start + end) // 2
            return min(self.query(2 * node, start, mid, l, r),
                      self.query(2 * node + 1, mid + 1, end, l, r))
    
    st = SegmentTree(arr)
    results = []
    
    for op in operations:
        if op[0] == 'Q':  # Query
            l, r = op[1], op[2]
            result = st.query(1, 0, n-1, l-1, r-1)
            results.append(result)
        else:  # Update
            idx, val = op[1], op[2]
            st.update(1, 0, n-1, idx-1, val)
            arr[idx-1] = val
    
    return results
```

#### **Variation 2: Range Minimum with Range Updates**
**Problem**: Support range updates (set all elements in range to a value) and point queries.
```python
def range_min_with_range_updates(n, q, arr, operations):
    # Use Segment Tree with lazy propagation
    class LazySegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [float('inf')] * (4 * self.n)
            self.lazy = [None] * (4 * self.n)
            self.build(arr, 1, 0, self.n - 1)
        
        def build(self, arr, node, start, end):
            if start == end:
                self.tree[node] = arr[start]
            else:
                mid = (start + end) // 2
                self.build(arr, 2 * node, start, mid)
                self.build(arr, 2 * node + 1, mid + 1, end)
                self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
        
        def push(self, node, start, end):
            if self.lazy[node] is not None:
                self.tree[node] = self.lazy[node]
                if start != end:
                    self.lazy[2 * node] = self.lazy[node]
                    self.lazy[2 * node + 1] = self.lazy[node]
                self.lazy[node] = None
        
        def range_update(self, node, start, end, l, r, val):
            self.push(node, start, end)
            if r < start or l > end:
                return
            if l <= start and end <= r:
                self.lazy[node] = val
                self.push(node, start, end)
                return
            mid = (start + end) // 2
            self.range_update(2 * node, start, mid, l, r, val)
            self.range_update(2 * node + 1, mid + 1, end, l, r, val)
            self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])
        
        def point_query(self, node, start, end, idx):
            self.push(node, start, end)
            if start == end:
                return self.tree[node]
            mid = (start + end) // 2
            if idx <= mid:
                return self.point_query(2 * node, start, mid, idx)
            else:
                return self.point_query(2 * node + 1, mid + 1, end, idx)
    
    st = LazySegmentTree(arr)
    results = []
    
    for op in operations:
        if op[0] == 'U':  # Range Update
            l, r, val = op[1], op[2], op[3]
            st.range_update(1, 0, n-1, l-1, r-1, val)
        else:  # Point Query
            idx = op[1]
            result = st.point_query(1, 0, n-1, idx-1)
            results.append(result)
    
    return results
```

#### **Variation 3: 2D Range Minimum Queries**
**Problem**: Given a 2D array, answer range minimum queries for rectangular regions.
```python
def range_min_2d(n, m, q, arr, queries):
    # Build 2D sparse table
    log_n, log_m = 20, 20
    st = [[[[0] * m for _ in range(n)] for _ in range(log_m)] for _ in range(log_n)]
    
    # Initialize first row and column
    for i in range(n):
        for j in range(m):
            st[0][0][i][j] = arr[i][j]
    
    # Build sparse table for rows
    for i in range(n):
        for j in range(1, log_m):
            for k in range(m - (1 << j) + 1):
                st[0][j][i][k] = min(st[0][j-1][i][k], 
                                   st[0][j-1][i][k + (1 << (j-1))])
    
    # Build sparse table for columns
    for j in range(log_m):
        for i in range(1, log_n):
            for k in range(n - (1 << i) + 1):
                for l in range(m):
                    st[i][j][k][l] = min(st[i-1][j][k][l], 
                                       st[i-1][j][k + (1 << (i-1))][l])
    
    results = []
    for x1, y1, x2, y2 in queries:
        # Convert to 0-indexed
        x1, y1, x2, y2 = x1-1, y1-1, x2-1, y2-1
        
        # Find logarithms
        log_x = 0
        while (1 << (log_x + 1)) <= (x2 - x1 + 1):
            log_x += 1
        log_y = 0
        while (1 << (log_y + 1)) <= (y2 - y1 + 1):
            log_y += 1
        
        # Query 2D sparse table
        min_val = min(
            st[log_x][log_y][x1][y1],
            st[log_x][log_y][x1][y2 - (1 << log_y) + 1],
            st[log_x][log_y][x2 - (1 << log_x) + 1][y1],
            st[log_x][log_y][x2 - (1 << log_x) + 1][y2 - (1 << log_y) + 1]
        )
        results.append(min_val)
    
    return results
```

#### **Variation 4: Range Minimum with K-th Smallest**
**Problem**: Find the k-th smallest element in a range instead of the minimum.
```python
def kth_smallest_in_range(n, q, arr, queries):
    # Use persistent segment tree or Mo's algorithm
    # For simplicity, use sorted list approach
    def kth_smallest_naive(l, r, k):
        # Convert to 0-indexed
        start, end = l - 1, r - 1
        # Extract range and sort
        range_elements = sorted(arr[start:end+1])
        return range_elements[k-1] if k <= len(range_elements) else -1
    
    results = []
    for l, r, k in queries:
        result = kth_smallest_naive(l, r, k)
        results.append(result)
    
    return results
```

#### **Variation 5: Range Minimum with Frequency**
**Problem**: Find the minimum value in a range and also return its frequency.
```python
def range_min_with_frequency(n, q, arr, queries):
    # Use segment tree storing (min_val, frequency)
    class MinFreqSegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [(float('inf'), 0)] * (4 * self.n)
            self.build(arr, 1, 0, self.n - 1)
        
        def build(self, arr, node, start, end):
            if start == end:
                self.tree[node] = (arr[start], 1)
            else:
                mid = (start + end) // 2
                self.build(arr, 2 * node, start, mid)
                self.build(arr, 2 * node + 1, mid + 1, end)
                
                left_min, left_freq = self.tree[2 * node]
                right_min, right_freq = self.tree[2 * node + 1]
                
                if left_min < right_min:
                    self.tree[node] = (left_min, left_freq)
                elif right_min < left_min:
                    self.tree[node] = (right_min, right_freq)
                else:
                    self.tree[node] = (left_min, left_freq + right_freq)
        
        def query(self, node, start, end, l, r):
            if r < start or l > end:
                return (float('inf'), 0)
            if l <= start and end <= r:
                return self.tree[node]
            mid = (start + end) // 2
            left_result = self.query(2 * node, start, mid, l, r)
            right_result = self.query(2 * node + 1, mid + 1, end, l, r)
            
            if left_result[0] < right_result[0]:
                return left_result
            elif right_result[0] < left_result[0]:
                return right_result
            else:
                return (left_result[0], left_result[1] + right_result[1])
    
    st = MinFreqSegmentTree(arr)
    results = []
    
    for l, r in queries:
        min_val, freq = st.query(1, 0, n-1, l-1, r-1)
        results.append((min_val, freq))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Range Query Data Structures**
- **Sparse Table**: O(n log n) preprocessing, O(1) queries (static)
- **Segment Tree**: O(n) preprocessing, O(log n) queries (dynamic)
- **Binary Indexed Tree**: Not suitable for RMQ
- **Cartesian Tree**: Alternative approach for RMQ

#### **2. Dynamic Range Problems**
- **Range Maximum Query**: Find maximum in range
- **Range Sum Query**: Find sum in range
- **Range GCD Query**: Find GCD of range
- **Range XOR Query**: Find XOR of range

#### **3. Advanced Range Techniques**
- **Lazy Propagation**: Efficient range updates
- **Persistent Segment Tree**: Handle historical queries
- **2D Range Queries**: Extend to multiple dimensions
- **Mo's Algorithm**: Offline range queries

#### **4. Optimization Problems**
- **Sliding Window Minimum**: Find minimum in sliding window
- **K-th Smallest Element**: Find k-th smallest in range
- **Range Minimum with Updates**: Dynamic RMQ
- **Range Minimum with Constraints**: Add additional constraints

#### **5. Competitive Programming Patterns**
- **Monotonic Stack**: Efficient minimum tracking
- **Two Pointers**: Optimize range processing
- **Binary Search**: Find optimal ranges
- **Greedy**: Optimize range selection

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    
    # Build sparse table
    log_n = 20
    st = [[0] * n for _ in range(log_n)]
    for i in range(n):
        st[0][i] = arr[i]
    
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st[j][i] = min(st[j-1][i], st[j-1][i + (1 << (j-1))])
    
    # Process queries
    for _ in range(q):
        l, r = map(int, input().split())
        length = r - l + 1
        k = 0
        while (1 << (k + 1)) <= length:
            k += 1
        result = min(st[k][l-1], st[k][r - (1 << k)])
        print(result)
```

#### **2. Range Queries with Aggregation**
```python
def range_aggregation_rmq(n, q, arr, queries):
    # Support multiple aggregation functions
    log_n = 20
    st_min = [[0] * n for _ in range(log_n)]
    st_max = [[0] * n for _ in range(log_n)]
    
    for i in range(n):
        st_min[0][i] = arr[i]
        st_max[0][i] = arr[i]
    
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st_min[j][i] = min(st_min[j-1][i], st_min[j-1][i + (1 << (j-1))])
            st_max[j][i] = max(st_max[j-1][i], st_max[j-1][i + (1 << (j-1))])
    
    results = []
    for l, r, op in queries:
        length = r - l + 1
        k = 0
        while (1 << (k + 1)) <= length:
            k += 1
        
        if op == 'MIN':
            result = min(st_min[k][l-1], st_min[k][r - (1 << k)])
        elif op == 'MAX':
            result = max(st_max[k][l-1], st_max[k][r - (1 << k)])
        results.append(result)
    
    return results
```

#### **3. Interactive Range Queries**
```python
def interactive_rmq(n, arr):
    # Handle interactive queries
    log_n = 20
    st = [[0] * n for _ in range(log_n)]
    for i in range(n):
        st[0][i] = arr[i]
    
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st[j][i] = min(st[j-1][i], st[j-1][i + (1 << (j-1))])
    
    while True:
        try:
            query = input().strip()
            if query == 'END':
                break
            
            l, r = map(int, query.split())
            length = r - l + 1
            k = 0
            while (1 << (k + 1)) <= length:
                k += 1
            result = min(st[k][l-1], st[k][r - (1 << k)])
            print(f"Min[{l},{r}] = {result}")
            
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
- **Sliding Window**: Optimize for consecutive ranges
- **Caching**: Store frequently accessed ranges

#### **3. Advanced Mathematical Concepts**
- **Monotonic Stack**: Efficient minimum tracking
- **Cartesian Tree**: Alternative RMQ representation
- **LCA Reduction**: Reduce RMQ to LCA problem
- **Fourier Transform**: Fast range operations using FFT

#### **4. Algorithmic Improvements**
- **Block Decomposition**: Divide array into blocks
- **Lazy Propagation**: Efficient range updates
- **Compression**: Handle sparse arrays efficiently
- **Parallel Processing**: Use multiple cores for large datasets

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sparse Table**: Static range minimum/maximum queries
- **Segment Tree**: Dynamic range queries with updates
- **Binary Indexed Tree**: Efficient point updates and range queries
- **Cartesian Tree**: Alternative approach for RMQ

#### **2. Mathematical Concepts**
- **Minimum/Maximum**: Understanding range properties
- **Monotonicity**: Using monotonic properties
- **Optimization**: Finding optimal ranges
- **Complexity Analysis**: Understanding time/space trade-offs

#### **3. Programming Concepts**
- **Data Structures**: Choosing appropriate structures
- **Algorithm Design**: Optimizing for specific constraints
- **Problem Decomposition**: Breaking complex problems
- **Code Optimization**: Writing efficient implementations

---

**Practice these variations to master range minimum query techniques and data structures!** 🎯

## Final Optimal Solution

```python
n, q = map(int, input().split())
arr = list(map(int, input().split()))

# Build sparse table
log_n = 20
st = [[0] * n for _ in range(log_n)]

# Initialize first row
for i in range(n):
    st[0][i] = arr[i]

# Build sparse table
for j in range(1, log_n):
    for i in range(n - (1 << j) + 1):
        st[j][i] = min(st[j-1][i], st[j-1][i + (1 << (j-1))])

# Process queries
for _ in range(q):
    a, b = map(int, input().split())
    # Convert to 0-indexed
    left, right = a - 1, b - 1
    length = right - left + 1
    
    # Find the largest power of 2 that fits in the range
    k = 0
    while (1 << (k + 1)) <= length:
        k += 1
    
    # Query the sparse table
    min_val = min(st[k][left], st[k][right - (1 << k) + 1])
    print(min_val)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(1) | Find minimum for each query |
| Sparse Table | O(n log n + q) | O(n log n) | Precompute for power-of-2 ranges |

## Key Insights for Other Problems

### 1. **Range Minimum Queries (RMQ)**
**Principle**: Use sparse table to answer range minimum queries in O(1) time.
**Applicable to**: RMQ problems, range queries, static data structures

### 2. **Sparse Table Technique**
**Principle**: Precompute answers for all power-of-2 length ranges to enable fast queries.
**Applicable to**: Range queries, static preprocessing, query optimization

### 3. **Power-of-2 Decomposition**
**Principle**: Decompose any range into overlapping power-of-2 length ranges.
**Applicable to**: Range problems, query problems, decomposition techniques

## Notable Techniques

### 1. **Sparse Table Construction**
```python
def build_sparse_table(arr):
    n = len(arr)
    log_n = 20
    st = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        st[0][i] = arr[i]
    
    # Build sparse table
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st[j][i] = min(st[j-1][i], st[j-1][i + (1 << (j-1))])
    
    return st
```

### 2. **Range Minimum Query**
```python
def range_min_query(st, left, right):
    length = right - left + 1
    k = 0
    while (1 << (k + 1)) <= length:
        k += 1
    
    return min(st[k][left], st[k][right - (1 << k) + 1])
```

### 3. **Log Calculation**
```python
def log2(n):
    k = 0
    while (1 << (k + 1)) <= n:
        k += 1
    return k
```

## Problem-Solving Framework

1. **Identify query type**: This is a static range minimum query problem
2. **Choose preprocessing**: Use sparse table for O(1) query time
3. **Build sparse table**: Precompute minimums for power-of-2 ranges
4. **Process queries**: Answer each query using overlapping power-of-2 ranges
5. **Handle indexing**: Convert between 1-indexed and 0-indexed as needed

---

*This analysis shows how to efficiently answer static range minimum queries using sparse table technique.* 