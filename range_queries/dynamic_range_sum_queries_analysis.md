# CSES Dynamic Range Sum Queries - Problem Analysis

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