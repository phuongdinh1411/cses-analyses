# CSES Pizzeria Queries - Problem Analysis

## Problem Statement
Given n buildings in a line, each with a pizzeria, process q queries. Each query is either:
1. Update the price of pizzeria at building k to x
2. Find the minimum price of a pizzeria in range [a,b]

### Input
The first input line has two integers n and q: the number of buildings and the number of queries.
The second line has n integers p_1,p_2,…,p_n: the initial prices of pizzerias.
Then there are q lines describing the queries. Each line has three integers: either "1 k x" (update) or "2 a b" (minimum query).

### Output
Print the answer to each minimum query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ p_i ≤ 10^9
- 1 ≤ k ≤ n
- 1 ≤ a ≤ b ≤ n

### Example
```
Input:
5 3
1 2 3 4 5
2 1 3
1 2 0
2 1 3

Output:
1
0
```

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct array updates and minimum calculations.

```python
def pizzeria_queries_naive(n, q, prices, queries):
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query
            k, x = query[1], query[2]
            prices[k-1] = x  # 1-indexed to 0-indexed
        else:  # Minimum query
            a, b = query[1], query[2]
            # Find minimum in range [a,b] (1-indexed)
            min_price = min(prices[a-1:b])
            result.append(min_price)
    
    return result
```

**Why this is inefficient**: Each minimum query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Segment Tree - O(log n) per operation
**Description**: Use segment tree for efficient point updates and range minimum queries.

```python
def pizzeria_queries_segment_tree(n, q, prices, queries):
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
    st = SegmentTree(prices)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query: 1 k x
            k, x = query[1], query[2]
            st.update(k-1, x)  # Convert to 0-indexed
        else:  # Minimum query: 2 a b
            a, b = query[1], query[2]
            min_price = st.query(a-1, b)  # Convert to 0-indexed, right exclusive
            result.append(min_price)
    
    return result
```

**Why this improvement works**: Segment tree provides O(log n) time for both updates and range minimum queries.

## Final Optimal Solution

```python
n, q = map(int, input().split())
prices = list(map(int, input().split()))
queries = []
for _ in range(q):
    query = list(map(int, input().split()))
    queries.append(query)

def process_pizzeria_queries(n, q, prices, queries):
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
    st = SegmentTree(prices)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update query: 1 k x
            k, x = query[1], query[2]
            st.update(k-1, x)  # Convert to 0-indexed
        else:  # Minimum query: 2 a b
            a, b = query[1], query[2]
            min_price = st.query(a-1, b)  # Convert to 0-indexed, right exclusive
            result.append(min_price)
    
    return result

result = process_pizzeria_queries(n, q, prices, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Solution | O(n*q) | O(1) | Direct array operations |
| Segment Tree | O(log n) per operation | O(n) | Efficient point updates and range minimum queries |

## Key Insights for Other Problems

### 1. **Segment Tree**
**Principle**: Use segment tree for efficient point updates and range queries.
**Applicable to**: Range minimum/maximum problems, point update problems, dynamic range queries

### 2. **Range Minimum Queries**
**Principle**: Use segment tree to find minimum value in any range efficiently.
**Applicable to**: Range minimum problems, optimization problems, query problems

### 3. **Point Updates with Range Queries**
**Principle**: Use data structures that support both point updates and range queries efficiently.
**Applicable to**: Dynamic range problems, update-query problems, array problems

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
def point_update_range_min(n, array, queries):
    st = SegmentTree(array)
    result = []
    
    for query in queries:
        if query[0] == 1:  # Update
            k, x = query[1], query[2]
            st.update(k-1, x)
        else:  # Range minimum query
            a, b = query[1], query[2]
            result.append(st.query(a-1, b))
    
    return result
```

### 3. **Efficient Range Operations**
```python
def efficient_range_min_queries(n, operations):
    st = SegmentTree([0] * n)
    result = []
    
    for op in operations:
        if op[0] == 1:  # Point update
            st.update(op[1]-1, op[2])
        else:  # Range minimum query
            result.append(st.query(op[1]-1, op[2]))
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic range minimum problem with point updates
2. **Choose approach**: Use segment tree for efficient operations
3. **Initialize data structure**: Build segment tree from initial array
4. **Process queries**: Handle updates and range minimum queries using segment tree
5. **Update operations**: Use point updates in segment tree
6. **Range queries**: Use range minimum query method in segment tree
7. **Return result**: Output answers for all range minimum queries

---

*This analysis shows how to efficiently handle dynamic range minimum queries using segment tree.* 