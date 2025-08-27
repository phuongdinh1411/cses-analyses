# CSES Prefix Sum Queries - Problem Analysis

## Problem Statement
Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the sum of values in range [a,b]

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x_1,x_2,…,x_n: the contents of the array.
Then there are q lines describing the queries. Each line has three integers: either "1 k x" (update) or "2 a b" (sum query).

### Output
Print the answer to each sum query.

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
14
18
```

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct array updates and sum calculations.

```python
def prefix_sum_queries_naive(n, q, array, queries):
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            array[k-1] = x  # 1-indexed to 0-indexed
        else:  # Sum query
            a, b = query[1], query[2]
            # Calculate sum from a to b (1-indexed)
            total = sum(array[a-1:b])
            result.append(total)
    
    return result
```

**Why this is inefficient**: Each sum query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Prefix Sum with Recalculation - O(n) per update, O(1) per query
**Description**: Use prefix sum array that gets recalculated after each update.

```python
def prefix_sum_queries_prefix(n, q, array, queries):
    # Build prefix sum array
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + array[i]
    
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            old_val = array[k-1]
            array[k-1] = x
            
            # Recalculate prefix sum from position k onwards
            diff = x - old_val
            for i in range(k, n + 1):
                prefix[i] += diff
        else:  # Sum query
            a, b = query[1], query[2]
            total = prefix[b] - prefix[a-1]
            result.append(total)
    
    return result
```

**Why this improvement works**: We use prefix sum for O(1) range sum queries, but updates still require O(n) time to recalculate.

### Improvement 2: Binary Indexed Tree (Fenwick Tree) - O(log n) per operation
**Description**: Use Binary Indexed Tree for efficient point updates and range sum queries.

```python
def prefix_sum_queries_bit(n, q, array, queries):
    class BIT:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        
        def update(self, index, val):
            while index <= self.n:
                self.tree[index] += val
                index += index & -index
        
        def query(self, index):
            total = 0
            while index > 0:
                total += self.tree[index]
                index -= index & -index
            return total
        
        def range_query(self, left, right):
            return self.query(right) - self.query(left - 1)
    
    # Initialize BIT
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, array[i])
    
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            old_val = array[k-1]
            array[k-1] = x
            bit.update(k, x - old_val)
        else:  # Sum query
            a, b = query[1], query[2]
            total = bit.range_query(a, b)
            result.append(total)
    
    return result
```

**Why this improvement works**: Binary Indexed Tree provides O(log n) time for both updates and range queries.

## Final Optimal Solution

```python
n, q = map(int, input().split())
array = list(map(int, input().split()))
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

def process_prefix_sum_queries(n, q, array, queries):
    class BIT:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        
        def update(self, index, val):
            while index <= self.n:
                self.tree[index] += val
                index += index & -index
        
        def query(self, index):
            total = 0
            while index > 0:
                total += self.tree[index]
                index -= index & -index
            return total
        
        def range_query(self, left, right):
            return self.query(right) - self.query(left - 1)
    
    # Initialize Binary Indexed Tree
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, array[i])
    
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query: 1 k x
            k, x = query[1], query[2]
            old_val = array[k-1]
            array[k-1] = x
            bit.update(k, x - old_val)
        else:  # Sum query: 2 a b
            a, b = query[1], query[2]
            total = bit.range_query(a, b)
            result.append(total)
    
    return result

result = process_prefix_sum_queries(n, q, array, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Solution | O(n*q) | O(1) | Direct array operations |
| Prefix Sum | O(n) per update, O(1) per query | O(n) | Prefix sum with recalculation |
| Binary Indexed Tree | O(log n) per operation | O(n) | Efficient point updates and range queries |

## Key Insights for Other Problems

### 1. **Binary Indexed Tree (Fenwick Tree)**
**Principle**: Use BIT for efficient point updates and range sum queries.
**Applicable to**: Range sum problems, point update problems, dynamic range queries

### 2. **Point Updates with Range Queries**
**Principle**: Use data structures that support both point updates and range queries efficiently.
**Applicable to**: Dynamic range problems, update-query problems, array problems

### 3. **Prefix Sum Optimization**
**Principle**: Use prefix sums for static range queries, but need better structures for dynamic updates.
**Applicable to**: Range sum problems, array problems, query optimization

## Notable Techniques

### 1. **Binary Indexed Tree Implementation**
```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, index, val):
        while index <= self.n:
            self.tree[index] += val
            index += index & -index
    
    def query(self, index):
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & -index
        return total
    
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)
```

### 2. **Point Update and Range Query**
```python
def point_update_range_query(n, array, queries):
    bit = BIT(n)
    for i in range(n):
        bit.update(i + 1, array[i])
    
    result = []
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            old_val = array[k-1]
            array[k-1] = x
            bit.update(k, x - old_val)
        else:  # Range query
            a, b = query[1], query[2]
            result.append(bit.range_query(a, b))
    
    return result
```

### 3. **Efficient Range Operations**
```python
def efficient_range_operations(n, operations):
    bit = BIT(n)
    result = []
    
    for op in operations:
        if op[0] == 1:  # Point update
            bit.update(op[1], op[2])
        else:  # Range query
            result.append(bit.range_query(op[1], op[2]))
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic range sum problem with point updates
2. **Choose approach**: Use Binary Indexed Tree for efficient operations
3. **Initialize data structure**: Build BIT from initial array
4. **Process queries**: Handle updates and range queries using BIT
5. **Update operations**: Use point updates in BIT
6. **Range queries**: Use range query method in BIT
7. **Return result**: Output answers for all range queries

---

*This analysis shows how to efficiently handle dynamic range sum queries using Binary Indexed Tree.* 