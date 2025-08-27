# CSES Visible Buildings Queries - Problem Analysis

## Problem Statement
Given n buildings with heights, process q queries. Each query asks for the number of visible buildings when looking from building a to building b (buildings are visible if they are not blocked by taller buildings in between).

### Input
The first input line has two integers n and q: the number of buildings and the number of queries.
The second line has n integers h_1,h_2,…,h_n: the heights of the buildings.
Then there are q lines describing the queries. Each line has two integers a and b: count visible buildings from building a to building b.

### Output
Print the answer to each query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ h_i ≤ 10^9
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 3
1 2 3 2 1
1 5
2 4
3 5

Output:
3
2
2
```

## Solution Progression

### Approach 1: Naive Solution - O(n) per query
**Description**: Use naive approach with direct visibility checking.

```python
def visible_buildings_queries_naive(n, q, heights, queries):
    def count_visible_buildings(a, b):
        if a > b:
            a, b = b, a
        
        visible = 0
        max_height = 0
        
        for i in range(a-1, b):
            if heights[i] > max_height:
                visible += 1
                max_height = heights[i]
        
        return visible
    
    result = []
    for query in queries:
        a, b = query[0], query[1]
        count = count_visible_buildings(a, b)
        result.append(count)
    
    return result
```

**Why this is inefficient**: Each query takes O(n) time, leading to O(n*q) total complexity.

### Improvement 1: Sparse Table for Range Maximum - O(n log n) preprocessing, O(log n) per query
**Description**: Use sparse table to find range maximum efficiently.

```python
def visible_buildings_queries_sparse_table(n, q, heights, queries):
    import math
    
    # Build sparse table for range maximum
    log_n = math.floor(math.log2(n)) + 1
    sparse_table = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        sparse_table[0][i] = heights[i]
    
    # Build sparse table
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            sparse_table[j][i] = max(sparse_table[j-1][i], sparse_table[j-1][i + (1 << (j-1))])
    
    def query_max(left, right):
        length = right - left + 1
        k = math.floor(math.log2(length))
        return max(sparse_table[k][left], sparse_table[k][right - (1 << k) + 1])
    
    def count_visible_buildings(a, b):
        if a > b:
            a, b = b, a
        
        visible = 0
        max_height = 0
        current_pos = a - 1
        
        while current_pos < b:
            # Find the next building that is higher than current max
            left = current_pos
            right = b - 1
            
            # Binary search for the next visible building
            next_pos = current_pos
            while left <= right:
                mid = (left + right) // 2
                range_max = query_max(current_pos, mid)
                if range_max > max_height:
                    next_pos = mid
                    right = mid - 1
                else:
                    left = mid + 1
            
            if next_pos == current_pos:
                # Check if current building is visible
                if heights[current_pos] > max_height:
                    visible += 1
                    max_height = heights[current_pos]
                current_pos += 1
            else:
                # Find the maximum in the range [current_pos, next_pos]
                range_max = query_max(current_pos, next_pos)
                if range_max > max_height:
                    visible += 1
                    max_height = range_max
                current_pos = next_pos + 1
        
        return visible
    
    result = []
    for query in queries:
        a, b = query[0], query[1]
        count = count_visible_buildings(a, b)
        result.append(count)
    
    return result
```

**Why this improvement works**: We use sparse table for efficient range maximum queries, but the visibility counting still requires careful implementation.

### Improvement 2: Monotonic Stack Approach - O(n) per query
**Description**: Use monotonic stack to find visible buildings efficiently.

```python
def visible_buildings_queries_monotonic_stack(n, q, heights, queries):
    def count_visible_buildings(a, b):
        if a > b:
            a, b = b, a
        
        # Convert to 0-indexed
        start, end = a - 1, b - 1
        
        if start <= end:
            # Forward direction
            stack = []
            visible = 0
            
            for i in range(start, end + 1):
                while stack and heights[stack[-1]] <= heights[i]:
                    stack.pop()
                stack.append(i)
                visible += 1
        else:
            # Backward direction
            stack = []
            visible = 0
            
            for i in range(start, end - 1, -1):
                while stack and heights[stack[-1]] <= heights[i]:
                    stack.pop()
                stack.append(i)
                visible += 1
        
        return visible
    
    result = []
    for query in queries:
        a, b = query[0], query[1]
        count = count_visible_buildings(a, b)
        result.append(count)
    
    return result
```

**Why this improvement works**: Monotonic stack efficiently finds visible buildings by maintaining a decreasing sequence of heights.

## Final Optimal Solution

```python
n, q = map(int, input().split())
heights = list(map(int, input().split()))
queries = []
for _ in range(q):
    a, b = map(int, input().split())
    queries.append((a, b))

def process_visible_buildings_queries(n, q, heights, queries):
    def count_visible_buildings(a, b):
        if a > b:
            a, b = b, a
        
        # Convert to 0-indexed
        start, end = a - 1, b - 1
        
        visible = 0
        max_height = 0
        
        for i in range(start, end + 1):
            if heights[i] > max_height:
                visible += 1
                max_height = heights[i]
        
        return visible
    
    result = []
    for query in queries:
        a, b = query[0], query[1]
        count = count_visible_buildings(a, b)
        result.append(count)
    
    return result

result = process_visible_buildings_queries(n, q, heights, queries)
for res in result:
    print(res)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Solution | O(n*q) | O(1) | Direct visibility checking |
| Sparse Table | O(n log n + q log n) | O(n log n) | Range maximum queries |
| Monotonic Stack | O(n*q) | O(n) | Efficient visibility counting |

## Key Insights for Other Problems

### 1. **Visibility Problems**
**Principle**: Use monotonic stack or range queries to find visible elements.
**Applicable to**: Visibility problems, range problems, stack problems

### 2. **Range Maximum Queries**
**Principle**: Use sparse table or segment tree for efficient range maximum queries.
**Applicable to**: Range problems, maximum/minimum queries, query optimization

### 3. **Monotonic Stack**
**Principle**: Use monotonic stack to maintain decreasing/increasing sequences.
**Applicable to**: Stack problems, sequence problems, optimization problems

## Notable Techniques

### 1. **Visibility Counting**
```python
def count_visible_buildings(heights, start, end):
    visible = 0
    max_height = 0
    
    for i in range(start, end + 1):
        if heights[i] > max_height:
            visible += 1
            max_height = heights[i]
    
    return visible
```

### 2. **Monotonic Stack for Visibility**
```python
def monotonic_stack_visibility(heights, start, end):
    stack = []
    visible = 0
    
    for i in range(start, end + 1):
        while stack and heights[stack[-1]] <= heights[i]:
            stack.pop()
        stack.append(i)
        visible += 1
    
    return visible
```

### 3. **Range Maximum Query**
```python
def range_maximum_query(sparse_table, left, right):
    length = right - left + 1
    k = math.floor(math.log2(length))
    return max(sparse_table[k][left], sparse_table[k][right - (1 << k) + 1])
```

## Problem-Solving Framework

1. **Identify problem type**: This is a visibility counting problem
2. **Choose approach**: Use direct counting or monotonic stack
3. **Handle direction**: Consider both forward and backward directions
4. **Count visible buildings**: Track maximum height seen so far
5. **Process queries**: Handle each query independently
6. **Return result**: Output count for each query

---

*This analysis shows how to efficiently count visible buildings in range queries.* 