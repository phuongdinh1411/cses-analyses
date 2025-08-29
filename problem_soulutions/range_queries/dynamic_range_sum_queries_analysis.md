---
layout: simple
title: "Dynamic Range Sum Queries"
permalink: /cses-analyses/problem_soulutions/range_queries/dynamic_range_sum_queries_analysis
---


# Dynamic Range Sum Queries

## Problem Statement
Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the sum of values in range [a,b]

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x1,x2,…,xn: the contents of the array.
Finally, there are q lines describing the queries. Each line has either:
- "1 k x": update the value at position k to x
- "2 a b": calculate the sum of values in range [a,b]

### Output
Print the answer to each sum query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9
- 1 ≤ k,a,b ≤ n

### Example
```
Input:
8 3
3 2 4 5 1 1 5 3
2 1 4
1 4 9
2 1 4

Output:
14
18
```

## Solution Progression

### Approach 1: Recalculate After Each Update - O(q × n)
**Description**: For each sum query, iterate through the range and calculate the sum. For updates, simply modify the array.

```python
def dynamic_range_sum_naive(n, q, arr, queries):
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            arr[k-1] = x  # Convert to 0-indexed
        else:  # Sum query
            a, b = query[1], query[2]
            start, end = a - 1, b - 1
            current_sum = sum(arr[start:end+1])
            results.append(current_sum)
    
    return results
```

**Why this is inefficient**: For each sum query, we need to iterate through the entire range, leading to O(q × n) time complexity.

### Improvement 1: Binary Indexed Tree (Fenwick Tree) - O(n log n + q log n)
**Description**: Use Binary Indexed Tree to support both point updates and range sum queries efficiently.

```python
def dynamic_range_sum_binary_indexed_tree(n, q, arr, queries):
    class BIT:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        
        def update(self, index, value):
            while index <= self.n:
                self.tree[index] += value
                index += index & -index
        
        def query(self, index):
            result = 0
            while index > 0:
                result += self.tree[index]
                index -= index & -index
            return result
        
        def range_query(self, left, right):
            return self.query(right) - self.query(left - 1)
    
    # Initialize BIT
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    results = []
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            old_val = arr[k-1]
            bit.update(k, x - old_val)
            arr[k-1] = x
        else:  # Sum query
            a, b = query[1], query[2]
            sum_range = bit.range_query(a, b)
            results.append(sum_range)
    
    return results
```

**Why this improvement works**: Binary Indexed Tree allows us to perform both point updates and range sum queries in O(log n) time.

## Final Optimal Solution

```python
n, q = map(int, input().split())
arr = list(map(int, input().split()))

class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, index, value):
        while index <= self.n:
            self.tree[index] += value
            index += index & -index
    
    def query(self, index):
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result
    
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)

# Initialize BIT
bit = BIT(n)
for i in range(n):
    bit.update(i + 1, arr[i])

# Process queries
for _ in range(q):
    query = list(map(int, input().split()))
    
    if query[0] == 1:  # Update
        k, x = query[1], query[2]
        old_val = arr[k-1]
        bit.update(k, x - old_val)
        arr[k-1] = x
    else:  # Sum query
        a, b = query[1], query[2]
        sum_range = bit.range_query(a, b)
        print(sum_range)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(1) | Recalculate after each update |
| Binary Indexed Tree | O(n log n + q log n) | O(n) | Use BIT for dynamic updates |

## Key Insights for Other Problems

### 1. **Dynamic Range Queries**
**Principle**: Use data structures that support both updates and queries efficiently.
**Applicable to**: Dynamic problems, range queries with updates, online algorithms

### 2. **Binary Indexed Tree (Fenwick Tree)**
**Principle**: Use BIT for point updates and range sum queries in O(log n) time.
**Applicable to**: Range sum problems, dynamic arrays, query problems

### 3. **Point Update vs Range Update**
**Principle**: Choose appropriate data structure based on update type (point vs range).
**Applicable to**: Update problems, query optimization, data structure selection

## Notable Techniques

### 1. **Binary Indexed Tree Implementation**
```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, index, value):
        while index <= self.n:
            self.tree[index] += value
            index += index & -index
    
    def query(self, index):
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result
    
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)
```

### 2. **Point Update Pattern**
```python
def point_update(bit, index, new_value, old_value):
    bit.update(index, new_value - old_value)
```

### 3. **Range Query Pattern**
```python
def range_sum_query(bit, left, right):
    return bit.range_query(left, right)
```

## Problem-Solving Framework

1. **Identify query type**: This is a dynamic range sum query problem with point updates
2. **Choose data structure**: Use Binary Indexed Tree for efficient updates and queries
3. **Initialize BIT**: Build the tree from the initial array
4. **Process queries**: Handle updates and sum queries using BIT operations
5. **Handle indexing**: Convert between 1-indexed and 0-indexed as needed

---

*This analysis shows how to efficiently handle dynamic range sum queries using Binary Indexed Tree technique.*

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Range Updates with Point Queries**
**Problem**: Support range updates (add value to all elements in range) and point queries.
```python
def range_updates_point_queries(n, q, arr, queries):
    # Use difference array for range updates
    diff = [0] * (n + 1)
    diff[0] = arr[0]
    for i in range(1, n):
        diff[i] = arr[i] - arr[i-1]
    
    class BIT:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        
        def update(self, index, value):
            while index <= self.n:
                self.tree[index] += value
                index += index & -index
        
        def query(self, index):
            result = 0
            while index > 0:
                result += self.tree[index]
                index -= index & -index
            return result
    
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, diff[i])
    
    results = []
    for query in queries:
        if query[0] == 1:  # Range Update
            l, r, val = query[1], query[2], query[3]
            bit.update(l, val)
            if r + 1 <= n:
                bit.update(r + 1, -val)
        else:  # Point Query
            idx = query[1]
            result = bit.query(idx)
            results.append(result)
    
    return results
```

#### **Variation 2: Range Updates with Range Queries**
**Problem**: Support both range updates and range sum queries efficiently.
```python
def range_updates_range_queries(n, q, arr, queries):
    # Use Segment Tree with lazy propagation
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
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
        
        def range_query(self, node, start, end, l, r):
            self.push(node, start, end)
            if r < start or l > end:
                return 0
            if l <= start and end <= r:
                return self.tree[node]
            mid = (start + end) // 2
            return (self.range_query(2 * node, start, mid, l, r) +
                   self.range_query(2 * node + 1, mid + 1, end, l, r))
    
    st = LazySegmentTree(arr)
    results = []
    
    for query in queries:
        if query[0] == 1:  # Range Update
            l, r, val = query[1], query[2], query[3]
            st.range_update(1, 0, n-1, l-1, r-1, val)
        else:  # Range Query
            l, r = query[1], query[2]
            result = st.range_query(1, 0, n-1, l-1, r-1)
            results.append(result)
    
    return results
```

#### **Variation 3: Dynamic Range Sum with Modulo**
**Problem**: Handle large numbers by working with modulo arithmetic.
```python
def dynamic_range_sum_modulo(n, q, arr, queries, mod=10**9 + 7):
    class BIT:
        def __init__(self, n, mod):
            self.n = n
            self.mod = mod
            self.tree = [0] * (n + 1)
        
        def update(self, index, value):
            value %= self.mod
            while index <= self.n:
                self.tree[index] = (self.tree[index] + value) % self.mod
                index += index & -index
        
        def query(self, index):
            result = 0
            while index > 0:
                result = (result + self.tree[index]) % self.mod
                index -= index & -index
            return result
        
        def range_query(self, left, right):
            return (self.query(right) - self.query(left - 1)) % self.mod
    
    bit = BIT(n, mod)
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    results = []
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            old_val = arr[k-1]
            bit.update(k, x - old_val)
            arr[k-1] = x
        else:  # Sum query
            a, b = query[1], query[2]
            sum_range = bit.range_query(a, b)
            results.append(sum_range)
    
    return results
```

#### **Variation 4: Dynamic Range Sum with Multiple Arrays**
**Problem**: Handle multiple arrays and support operations across them.
```python
def multi_array_range_sum(n, m, q, arrays, queries):
    # Handle m arrays, each of size n
    bits = []
    for arr in arrays:
        bit = BIT(n)
        for i in range(n):
            bit.update(i + 1, arr[i])
        bits.append(bit)
    
    results = []
    for query in queries:
        if query[0] == 1:  # Update
            array_idx, k, x = query[1], query[2], query[3]
            old_val = arrays[array_idx][k-1]
            bits[array_idx].update(k, x - old_val)
            arrays[array_idx][k-1] = x
        else:  # Sum query across multiple arrays
            a, b, array_indices = query[1], query[2], query[3:]
            total_sum = 0
            for idx in array_indices:
                total_sum += bits[idx].range_query(a, b)
            results.append(total_sum)
    
    return results
```

#### **Variation 5: Dynamic Range Sum with Constraints**
**Problem**: Add constraints like maximum range size or minimum sum threshold.
```python
def constrained_range_sum(n, q, arr, queries, max_range=100, min_sum=0):
    class BIT:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        
        def update(self, index, value):
            while index <= self.n:
                self.tree[index] += value
                index += index & -index
        
        def query(self, index):
            result = 0
            while index > 0:
                result += self.tree[index]
                index -= index & -index
            return result
        
        def range_query(self, left, right):
            return self.query(right) - self.query(left - 1)
    
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    results = []
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            old_val = arr[k-1]
            bit.update(k, x - old_val)
            arr[k-1] = x
        else:  # Constrained Sum query
            a, b = query[1], query[2]
            if b - a + 1 > max_range:
                results.append(-1)  # Range too large
            else:
                sum_range = bit.range_query(a, b)
                if sum_range >= min_sum:
                    results.append(sum_range)
                else:
                    results.append(-1)  # Sum too small
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Dynamic Range Query Data Structures**
- **Binary Indexed Tree**: O(log n) point updates and range queries
- **Segment Tree**: O(log n) range updates and range queries
- **Lazy Segment Tree**: Efficient range updates with lazy propagation
- **Persistent Segment Tree**: Handle historical queries

#### **2. Update Types**
- **Point Updates**: Update single element
- **Range Updates**: Update all elements in range
- **Incremental Updates**: Add value to elements
- **Set Updates**: Set elements to specific value

#### **3. Query Types**
- **Range Sum**: Sum of elements in range
- **Range Minimum/Maximum**: Min/max in range
- **Range GCD**: GCD of elements in range
- **Range XOR**: XOR of elements in range

#### **4. Advanced Techniques**
- **Lazy Propagation**: Defer updates until needed
- **Persistent Data Structures**: Maintain history
- **2D Range Queries**: Extend to multiple dimensions
- **Offline Processing**: Process queries in optimal order

#### **5. Optimization Problems**
- **Maximum Subarray Sum**: Find maximum sum subarray
- **K-th Largest Sum**: Find k-th largest subarray sum
- **Range Sum with Constraints**: Add additional constraints
- **Weighted Range Sum**: Elements have weights

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    for _ in range(q):
        query = list(map(int, input().split()))
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            old_val = arr[k-1]
            bit.update(k, x - old_val)
            arr[k-1] = x
        else:  # Sum query
            a, b = query[1], query[2]
            result = bit.range_query(a, b)
            print(result)
```

#### **2. Range Queries with Aggregation**
```python
def range_aggregation_dynamic(n, q, arr, queries):
    # Support multiple aggregation functions
    class MultiBIT:
        def __init__(self, n):
            self.n = n
            self.sum_tree = [0] * (n + 1)
            self.min_tree = [float('inf')] * (n + 1)
            self.max_tree = [-float('inf')] * (n + 1)
        
        def update(self, index, value):
            while index <= self.n:
                self.sum_tree[index] += value
                self.min_tree[index] = min(self.min_tree[index], value)
                self.max_tree[index] = max(self.max_tree[index], value)
                index += index & -index
        
        def query_sum(self, index):
            result = 0
            while index > 0:
                result += self.sum_tree[index]
                index -= index & -index
            return result
        
        def range_query(self, left, right, op):
            if op == 'SUM':
                return self.query_sum(right) - self.query_sum(left - 1)
            # Add min/max queries as needed
    
    bit = MultiBIT(n)
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    results = []
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            old_val = arr[k-1]
            bit.update(k, x - old_val)
            arr[k-1] = x
        else:  # Range Query
            l, r, op = query[1], query[2], query[3]
            result = bit.range_query(l, r, op)
            results.append(result)
    
    return results
```

#### **3. Interactive Dynamic Queries**
```python
def interactive_dynamic_queries(n, arr):
    # Handle interactive queries
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    while True: 
try: query = input().strip()
            if query == 'END':
                break
            
            parts = query.split()
            if parts[0] == 'UPDATE':
                k, x = int(parts[1]), int(parts[2])
                old_val = arr[k-1]
                bit.update(k, x - old_val)
                arr[k-1] = x
                print(f"Updated position {k} to {x}")
            elif parts[0] == 'SUM':
                l, r = int(parts[1]), int(parts[2])
                result = bit.range_query(l, r)
                print(f"Sum[{l},{r}] = {result}")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. Dynamic Range Sum Properties**
- **Linearity**: sum(a,b) + sum(c,d) = sum(a,d) - sum(b+1,c-1) (if ranges overlap)
- **Additivity**: sum(a,b) + sum(b+1,c) = sum(a,c)
- **Commutativity**: sum(a,b) + sum(c,d) = sum(c,d) + sum(a,b)
- **Associativity**: (sum(a,b) + sum(c,d)) + sum(e,f) = sum(a,b) + (sum(c,d) + sum(e,f))

#### **2. Optimization Techniques**
- **Early Termination**: Stop if sum exceeds threshold
- **Binary Search**: Find ranges with specific sums
- **Sliding Window**: Optimize for consecutive ranges
- **Caching**: Store frequently accessed ranges

#### **3. Advanced Mathematical Concepts**
- **Modular Arithmetic**: Handle large numbers with modulo
- **Matrix Operations**: Extend to matrix range queries
- **Polynomial Evaluation**: Range sum as polynomial evaluation
- **Fourier Transform**: Fast range operations using FFT

#### **4. Algorithmic Improvements**
- **Block Decomposition**: Divide array into blocks
- **Lazy Propagation**: Efficient range updates
- **Compression**: Handle sparse arrays efficiently
- **Parallel Processing**: Use multiple cores for large datasets

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Binary Indexed Tree**: Efficient point updates and range queries
- **Segment Tree**: Versatile range query data structure
- **Lazy Propagation**: Efficient range updates
- **Persistent Data Structures**: Handle historical queries

#### **2. Mathematical Concepts**
- **Summation**: Understanding range sum properties
- **Modular Arithmetic**: Handling large numbers
- **Optimization**: Finding optimal ranges
- **Complexity Analysis**: Understanding time/space trade-offs

#### **3. Programming Concepts**
- **Data Structures**: Choosing appropriate structures
- **Algorithm Design**: Optimizing for specific constraints
- **Problem Decomposition**: Breaking complex problems
- **Code Optimization**: Writing efficient implementations

---

**Practice these variations to master dynamic range query techniques and data structures!** 🎯 