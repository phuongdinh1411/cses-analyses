# CSES Subarray Minimum Queries - Problem Analysis

## Problem Statement
Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the minimum value in range [a,b]

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x_1,x_2,…,x_n: the contents of the array.
Then there are q lines describing the queries. Each line has three integers: either "1 k x" (update) or "2 a b" (minimum query).

### Output
Print the answer to each minimum query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ x_i ≤ 10^9
- 1 ≤ k ≤ n
- 1 ≤ a ≤ b ≤ n

### Example
```
Input:
8 3
3 2 4 5 1 1 5 3
2 1 4
1 4 9
2 1 4

Output:
2
2
```

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct array updates and minimum calculations.

```python
def subarray_minimum_queries_naive(n, q, array, queries):
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            array[k-1] = x  # 1-indexed to 0-indexed
        else:  # Minimum query
            a, b = query[1], query[2]
            # Calculate minimum from a to b (1-indexed)
            min_val = min(array[a-1:b])
            result.append(min_val)
    
    return result
```

**Why this is inefficient**: Each minimum query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Segment Tree - O(log n) per operation
**Description**: Use Segment Tree for efficient point updates and range minimum queries.

```python
def subarray_minimum_queries_segment(n, q, array, queries):
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = value
            index //= 2
            while index >= 1:
                self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.tree[right])
                left //= 2
                right //= 2
            
            return result
    
    # Initialize segment tree
    st = SegmentTree(array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            st.update(k-1, x)  # Convert to 0-indexed
        else:  # Minimum query
            a, b = query[1], query[2]
            min_val = st.query(a-1, b)  # Convert to 0-indexed, right exclusive
            result.append(min_val)
    
    return result
```

**Why this improvement works**: Segment Tree provides O(log n) time for both updates and range minimum queries.

### Improvement 2: Sparse Table (for static queries) - O(1) per query, O(n log n) preprocessing
**Description**: Use Sparse Table for static range minimum queries (no updates).

```python
def subarray_minimum_queries_sparse(n, q, array, queries):
    # Build sparse table for range minimum queries
    log_n = 20  # Sufficient for n up to 10^6
    sparse = [[0] * n for _ in range(log_n)]
    
    # Base case: sparse[0][i] = array[i]
    for i in range(n):
        sparse[0][i] = array[i]
    
    # Build sparse table
    for k in range(1, log_n):
        for i in range(n - (1 << k) + 1):
            sparse[k][i] = min(sparse[k-1][i], sparse[k-1][i + (1 << (k-1))])
    
    # Precompute log values
    log_table = [0] * (n + 1)
    for i in range(2, n + 1):
        log_table[i] = log_table[i // 2] + 1
    
    def range_min(left, right):
        length = right - left + 1
        k = log_table[length]
        return min(sparse[k][left], sparse[k][right - (1 << k) + 1])
    
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query - not supported in sparse table
            # Would need to rebuild sparse table in O(n log n)
            pass
        else:  # Minimum query
            a, b = query[1], query[2]
            min_val = range_min(a-1, b-1)  # Convert to 0-indexed
            result.append(min_val)
    
    return result
```

**Why this improvement works**: Sparse Table provides O(1) range minimum queries, but doesn't support efficient updates.

## Final Optimal Solution

```python
n, q = map(int, input().split())
array = list(map(int, input().split()))
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

def process_subarray_minimum_queries(n, q, array, queries):
    class SegmentTree:
        def __init__(self, data):
            self.n = len(data)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.tree = [float('inf')] * (2 * self.size)
            
            # Build the tree
            for i in range(self.n):
                self.tree[self.size + i] = data[i]
            for i in range(self.size - 1, 0, -1):
                self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
        
        def update(self, index, value):
            index += self.size
            self.tree[index] = value
            index //= 2
            while index >= 1:
                self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
                index //= 2
        
        def query(self, left, right):
            left += self.size
            right += self.size
            result = float('inf')
            
            while left < right:
                if left % 2 == 1:
                    result = min(result, self.tree[left])
                    left += 1
                if right % 2 == 1:
                    right -= 1
                    result = min(result, self.tree[right])
                left //= 2
                right //= 2
            
            return result
    
    # Initialize segment tree
    st = SegmentTree(array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query: 1 k x
            k, x = query[1], query[2]
            st.update(k-1, x)  # Convert to 0-indexed
        else:  # Minimum query: 2 a b
            a, b = query[1], query[2]
            min_val = st.query(a-1, b)  # Convert to 0-indexed, right exclusive
            result.append(min_val)
    
    return result

result = process_subarray_minimum_queries(n, q, array, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Solution | O(n*q) | O(1) | Direct array operations |
| Segment Tree | O(log n) per operation | O(n) | Efficient point updates and range queries |
| Sparse Table | O(n log n) preprocessing, O(1) per query | O(n log n) | Static range queries only |

## Key Insights for Other Problems

### 1. **Segment Tree for Dynamic Range Queries**
**Principle**: Use Segment Tree for efficient point updates and range queries.
**Applicable to**: Dynamic range problems, update-query problems, array problems

### 2. **Range Minimum/Maximum Queries**
**Principle**: Use appropriate data structures for range minimum/maximum operations.
**Applicable to**: Range query problems, optimization problems, array problems

### 3. **Sparse Table for Static Queries**
**Principle**: Use Sparse Table for static range queries when updates are not needed.
**Applicable to**: Static range problems, preprocessing-heavy problems, query optimization

## Notable Techniques

### 1. **Segment Tree Implementation**
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [float('inf')] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
    
    def update(self, index, value):
        index += self.size
        self.tree[index] = value
        index //= 2
        while index >= 1:
            self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])
            index //= 2
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result = float('inf')
        
        while left < right:
            if left % 2 == 1:
                result = min(result, self.tree[left])
                left += 1
            if right % 2 == 1:
                right -= 1
                result = min(result, self.tree[right])
            left //= 2
            right //= 2
        
        return result
```

### 2. **Point Update and Range Query**
```python
def point_update_range_min_query(n, array, queries):
    st = SegmentTree(array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            st.update(k-1, x)
        else:  # Range query
            a, b = query[1], query[2]
            result.append(st.query(a-1, b))
    
    return result
```

### 3. **Sparse Table for Static Range Queries**
```python
def build_sparse_table(array):
    n = len(array)
    log_n = 20
    sparse = [[0] * n for _ in range(log_n)]
    
    # Base case
    for i in range(n):
        sparse[0][i] = array[i]
    
    # Build sparse table
    for k in range(1, log_n):
        for i in range(n - (1 << k) + 1):
            sparse[k][i] = min(sparse[k-1][i], sparse[k-1][i + (1 << (k-1))])
    
    return sparse

def range_min_query(sparse, left, right, log_table):
    length = right - left + 1
    k = log_table[length]
    return min(sparse[k][left], sparse[k][right - (1 << k) + 1])
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic range minimum problem with point updates
2. **Choose approach**: Use Segment Tree for efficient operations
3. **Initialize data structure**: Build Segment Tree from initial array
4. **Process queries**: Handle updates and range queries using Segment Tree
5. **Update operations**: Use point updates in Segment Tree
6. **Range queries**: Use range query method in Segment Tree
7. **Return result**: Output answers for all range queries

---

*This analysis shows how to efficiently handle dynamic range minimum queries using Segment Tree.* 