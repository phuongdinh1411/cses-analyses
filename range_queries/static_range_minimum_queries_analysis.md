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