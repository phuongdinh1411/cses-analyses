# CSES Prefix Sum Queries - Problem Analysis

## Problem Statement
Given an array of n integers, process q queries. Each query is either:
1. Update the value at position k to x
2. Calculate the sum of elements from position a to b

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers a1,a2,…,an: the array.
Then there are q lines describing the queries. Each line has either:
- "1 k x": update the value at position k to x
- "2 a b": calculate the sum from position a to b

### Output
For each sum query, print the sum.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ ai ≤ 10^9
- 1 ≤ k ≤ n
- 1 ≤ a ≤ b ≤ n

### Example
```
Input:
8 4
3 2 4 5 1 1 5 3
2 1 4
1 4 9
2 1 4
2 2 6

Output:
14
20
17
```

## Solution Progression

### Approach 1: Naive Updates and Sums - O(q*n)
**Description**: Update array directly and calculate sums by iterating.

```python
def prefix_sum_queries_naive(n, q, arr, queries):
    results = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            arr[k-1] = x
        else:  # Sum query
            a, b = query[1], query[2]
            total = sum(arr[a-1:b])
            results.append(total)
    
    return results
```

**Why this is inefficient**: Each sum query takes O(n) time, leading to quadratic complexity.

### Improvement 1: Binary Indexed Tree - O(q log n)
**Description**: Use Binary Indexed Tree (Fenwick Tree) for efficient updates and range sums.

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

def prefix_sum_queries_optimized(n, q, arr, queries):
    bit = BIT(n)
    
    # Initialize BIT with array values
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
            total = bit.range_query(a, b)
            results.append(total)
    
    return results
```

**Why this improvement works**: We use a Binary Indexed Tree to support both point updates and range sum queries in O(log n) time each.

## Final Optimal Solution

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

n, q = map(int, input().split())
arr = list(map(int, input().split()))

def process_queries(n, q, arr, queries):
    bit = BIT(n)
    
    # Initialize BIT with array values
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
            total = bit.range_query(a, b)
            results.append(total)
    
    return results

# Read queries
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

result = process_queries(n, q, arr, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q*n) | O(1) | Direct array operations |
| Binary Indexed Tree | O(q log n) | O(n) | Use BIT for efficient updates and queries |

## Key Insights for Other Problems

### 1. **Range Sum Queries**
**Principle**: Use Binary Indexed Tree or Segment Tree for efficient range sum queries with updates.
**Applicable to**: Range problems, query problems, update problems

### 2. **Binary Indexed Tree**
**Principle**: Use BIT for point updates and range queries in logarithmic time.
**Applicable to**: Range problems, update problems, query problems

### 3. **Dynamic Range Queries**
**Principle**: Handle both updates and queries efficiently using specialized data structures.
**Applicable to**: Dynamic problems, range problems, query problems

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
```

### 2. **Range Query**
```python
def range_query(bit, left, right):
    return bit.query(right) - bit.query(left - 1)
```

### 3. **Point Update**
```python
def point_update(bit, index, new_value, old_value):
    bit.update(index, new_value - old_value)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic range sum query problem
2. **Choose approach**: Use Binary Indexed Tree for efficiency
3. **Initialize BIT**: Build BIT from initial array values
4. **Process queries**: Handle updates and sum queries
5. **Update values**: Use point updates in BIT
6. **Calculate sums**: Use range queries in BIT
7. **Return results**: Output sum query results

---

*This analysis shows how to efficiently handle dynamic range sum queries using Binary Indexed Tree.* 