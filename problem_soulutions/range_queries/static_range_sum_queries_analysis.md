---
layout: simple
title: "Static Range Sum Queries
permalink: /problem_soulutions/range_queries/static_range_sum_queries_analysis/
---

# Static Range Sum Queries

## Problem Statement
Given an array of n integers, process q queries. Each query asks for the sum of values in a range [a,b].

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
11
2
24
4
```

## Solution Progression

### Approach 1: Calculate Sum for Each Query - O(q × n)
**Description**: For each query, iterate through the range and calculate the sum.

```python
def static_range_sum_naive(n, q, arr, queries):
    results = []
    
    for a, b in queries:
        # Convert to 0-indexed
        start, end = a - 1, b - 1
        current_sum = 0
        
        for i in range(start, end + 1):
            current_sum += arr[i]
        
        results.append(current_sum)
    
    return results
```

**Why this is inefficient**: For each query, we need to iterate through the entire range, leading to O(q × n) time complexity.

### Improvement 1: Prefix Sum Array - O(n + q)
**Description**: Precompute prefix sums to answer range queries in O(1) time.

```python
def static_range_sum_prefix_sum(n, q, arr, queries):
    # Build prefix sum array
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    results = []
    for a, b in queries:
        # Convert to 0-indexed and use prefix sum
        start, end = a - 1, b - 1
        sum_range = prefix_sum[end + 1] - prefix_sum[start]
        results.append(sum_range)
    
    return results
```

**Why this improvement works**: Prefix sum allows us to calculate any range sum in O(1) time using the formula: sum[a,b] = prefix[b+1] - prefix[a].

## Final Optimal Solution

```python
n, q = map(int, input().split())
arr = list(map(int, input().split()))

# Build prefix sum array
prefix_sum = [0] * (n + 1)
for i in range(n):
    prefix_sum[i + 1] = prefix_sum[i] + arr[i]

# Process queries
for _ in range(q):
    a, b = map(int, input().split())
    # Convert to 0-indexed and use prefix sum
    start, end = a - 1, b - 1
    sum_range = prefix_sum[end + 1] - prefix_sum[start]
    print(sum_range)
```

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Range Sum with Updates**
**Problem**: Allow point updates to the array while still answering range sum queries efficiently.
```python
def range_sum_with_updates(n, q, arr, operations):
    # Use Binary Indexed Tree (Fenwick Tree) or Segment Tree
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
    
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, arr[i])
    
    results = []
    for op in operations:"
        if op[0] == 'Q':  # Query
            l, r = op[1], op[2]
            results.append(bit.query(r) - bit.query(l - 1))
        else:  # Update
            idx, val = op[1], op[2]
            bit.update(idx, val - arr[idx - 1])
            arr[idx - 1] = val
    
    return results
```

#### **Variation 2: Range Sum with Range Updates**
**Problem**: Support range updates (add value to all elements in range) and point queries.
```python
def range_sum_with_range_updates(n, q, arr, operations):
    # Use difference array for range updates
    diff = [0] * (n + 1)
    diff[0] = arr[0]
    for i in range(1, n):
        diff[i] = arr[i] - arr[i-1]
    
    def range_update(l, r, val):
        diff[l] += val
        if r + 1 < n:
            diff[r + 1] -= val
    
    def point_query(idx):
        result = 0
        for i in range(idx + 1):
            result += diff[i]
        return result
    
    results = []
    for op in operations:
        if op[0] == 'U':  # Range Update
            l, r, val = op[1], op[2], op[3]
            range_update(l, r, val)
        else:  # Point Query
            idx = op[1]
            results.append(point_query(idx))
    
    return results
```

#### **Variation 3: 2D Range Sum Queries**
**Problem**: Given a 2D array, answer range sum queries for rectangular regions.
```python
def range_sum_2d(n, m, q, arr, queries):
    # Build 2D prefix sum
    prefix = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            prefix[i + 1][j + 1] = (prefix[i + 1][j] + 
                                   prefix[i][j + 1] - 
                                   prefix[i][j] + 
                                   arr[i][j])
    
    results = []
    for x1, y1, x2, y2 in queries:
        # Convert to 1-indexed
        sum_rect = (prefix[x2][y2] - prefix[x1-1][y2] - 
                   prefix[x2][y1-1] + prefix[x1-1][y1-1])
        results.append(sum_rect)
    
    return results
```

#### **Variation 4: Range Sum with Non-overlapping Constraints**
**Problem**: Find the maximum sum of k non-overlapping ranges.
```python
def max_non_overlapping_ranges(n, k, arr):
    # Use dynamic programming
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # dp[i][j] = max sum using j ranges ending at position i
    dp = [[-float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(k + 1):
            # Don't use current position
            dp[i][j] = dp[i-1][j]
            
            # Use current position as end of range
            if j > 0:
                for start in range(i):
                    range_sum = prefix[i] - prefix[start]
                    dp[i][j] = max(dp[i][j], dp[start][j-1] + range_sum)
    
    return max(dp[n][j] for j in range(k + 1))
```

#### **Variation 5: Range Sum with Circular Array**
**Problem**: Handle range sum queries on a circular array where ranges can wrap around.
```python
def circular_range_sum(n, q, arr, queries):
    # Duplicate array to handle circular queries
    extended = arr + arr
    prefix = [0] * (2 * n + 1)
    for i in range(2 * n):
        prefix[i + 1] = prefix[i] + extended[i]
    
    results = []
    for l, r in queries:
        # Convert to 0-indexed
        start, end = l - 1, r - 1
        
        if end < n:  # Normal range
            sum_range = prefix[end + 1] - prefix[start]
        else:  # Wrapping range
            sum_range = prefix[end + 1] - prefix[start]
        
        results.append(sum_range)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Range Query Data Structures**
- **Prefix Sum Array**: O(n) preprocessing, O(1) queries
- **Binary Indexed Tree**: O(n log n) preprocessing, O(log n) updates/queries
- **Segment Tree**: O(n) preprocessing, O(log n) updates/queries
- **Sparse Table**: O(n log n) preprocessing, O(1) queries (for RMQ)

#### **2. Dynamic Range Problems**
- **Range Minimum Query**: Find minimum in range
- **Range Maximum Query**: Find maximum in range
- **Range GCD Query**: Find GCD of range
- **Range XOR Query**: Find XOR of range

#### **3. Advanced Range Techniques**
- **Mo's Algorithm**: Offline range queries with sqrt decomposition
- **Persistent Segment Tree**: Handle historical queries
- **2D Range Queries**: Extend to multiple dimensions
- **Range Updates**: Efficiently update ranges

#### **4. Optimization Problems**
- **Maximum Subarray Sum**: Find maximum sum of any subarray
- **K-th Largest Sum**: Find k-th largest subarray sum
- **Range Sum with Constraints**: Add additional constraints
- **Weighted Range Sum**: Elements have weights

#### **5. Competitive Programming Patterns**
- **Sliding Window**: Optimize range queries
- **Two Pointers**: Efficient range processing
- **Binary Search**: Find optimal ranges
- **Greedy**: Optimize range selection

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    
    # Build prefix sum
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Process queries
    for _ in range(q):
        l, r = map(int, input().split())
        result = prefix[r] - prefix[l-1]
        print(result)
```

#### **2. Range Queries with Aggregation**
```python
def range_aggregation(n, q, arr, queries):
    # Support multiple aggregation functions
    prefix_sum = [0] * (n + 1)
    prefix_min = [float('inf')] * (n + 1)
    prefix_max = [-float('inf')] * (n + 1)
    
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
        prefix_min[i + 1] = min(prefix_min[i], arr[i])
        prefix_max[i + 1] = max(prefix_max[i], arr[i])
    
    results = []
    for l, r, op in queries:
        if op == 'SUM':
            result = prefix_sum[r] - prefix_sum[l-1]
        elif op == 'MIN':
            result = min(arr[i] for i in range(l-1, r))
        elif op == 'MAX':
            result = max(arr[i] for i in range(l-1, r))
        results.append(result)
    
    return results
```

#### **3. Interactive Range Queries**
```python
def interactive_range_queries(n, arr):
    # Handle interactive queries
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    while True:
        try:
            query = input().strip()
            if query == 'END':
                break
            
            l, r = map(int, query.split())
            result = prefix[r] - prefix[l-1]
            print(f"Sum[{l},{r}] = {result}")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. Range Sum Properties**
- **Commutativity**: sum(a,b) + sum(c,d) = sum(c,d) + sum(a,b)
- **Associativity**: (sum(a,b) + sum(c,d)) + sum(e,f) = sum(a,b) + (sum(c,d) + sum(e,f))
- **Distributivity**: k * sum(a,b) = sum of k copies of range
- **Linearity**: sum(a,b) + sum(c,d) = sum(a,d) - sum(b+1,c-1) (if ranges overlap)

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
- **Prefix Sum**: Fundamental range query technique
- **Binary Indexed Tree**: Efficient point updates and range queries
- **Segment Tree**: Versatile range query data structure
- **Sparse Table**: Static range minimum/maximum queries

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

**Practice these variations to master range query techniques and data structures!** 🎯
    a, b = map(int, input().split())
    # Convert to 0-indexed
    start, end = a - 1, b - 1
    # Calculate range sum using prefix sum
    sum_range = prefix_sum[end + 1] - prefix_sum[start]
    print(sum_range)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(1) | Calculate sum for each query |
| Prefix Sum | O(n + q) | O(n) | Precompute prefix sums |

## Key Insights for Other Problems

### 1. **Range Sum Queries**
**Principle**: Use prefix sum array to answer range sum queries in O(1) time.
**Applicable to**: Range sum problems, cumulative sum problems, query optimization

### 2. **Static Range Queries**
**Principle**: Preprocess data to answer multiple queries efficiently.
**Applicable to**: Static data structures, query problems, preprocessing techniques

### 3. **Prefix Sum Technique**
**Principle**: Build cumulative sum array to enable fast range calculations.
**Applicable to**: Sum problems, range problems, cumulative calculations

## Notable Techniques

### 1. **Prefix Sum Construction**
```python
def build_prefix_sum(arr):
    n = len(arr)
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    return prefix_sum
```

### 2. **Range Sum Query**
```python
def range_sum_query(prefix_sum, left, right):
    # Convert to 0-indexed if needed
    return prefix_sum[right + 1] - prefix_sum[left]
```

### 3. **1-indexed to 0-indexed Conversion**
```python
def convert_indices(a, b):
    # Convert from 1-indexed to 0-indexed
    return a - 1, b - 1
```

## Problem-Solving Framework

1. **Identify query type**: This is a static range sum query problem
2. **Choose preprocessing**: Use prefix sum array for O(1) query time
3. **Build prefix sum**: Create cumulative sum array in O(n) time
4. **Process queries**: Answer each query in O(1) time using prefix sum
5. **Handle indexing**: Convert between 1-indexed and 0-indexed as needed

---

*This analysis shows how to efficiently answer static range sum queries using prefix sum technique.* 