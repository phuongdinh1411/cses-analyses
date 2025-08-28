---
layout: simple
title: CSES Range Update Queries - Problem Analysis
permalink: /problem_soulutions/range_queries/range_update_queries_analysis/
---

# CSES Range Update Queries - Problem Analysis

## Problem Statement
Given an array of n integers, process q queries. Each query is either:
1. Add x to all values in range [a,b]
2. Print the value at position k

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x1,x2,…,xn: the contents of the array.
Finally, there are q lines describing the queries. Each line has either:
- "1 a b x": add x to all values in range [a,b]
- "2 k": print the value at position k

### Output
Print the answer to each query of type 2.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9
- 1 ≤ a ≤ b ≤ n
- 1 ≤ k ≤ n

### Example
```
Input:
8 3
3 2 4 5 1 1 5 3
1 2 4 2
2 3
2 4

Output:
6
7
```

## Solution Progression

### Approach 1: Update Array for Each Range Update - O(q × n)
**Description**: For each range update, iterate through the range and add x to each element. For queries, simply return the value.

```python
def range_update_naive(n, q, arr, queries):
    results = []
    
    for query in queries:
        if query[0] == 1:  # Range update
            a, b, x = query[1], query[2], query[3]
            start, end = a - 1, b - 1
            for i in range(start, end + 1):
                arr[i] += x
        else:  # Point query
            k = query[1]
            results.append(arr[k-1])
    
    return results
```

**Why this is inefficient**: For each range update, we need to iterate through the entire range, leading to O(q × n) time complexity.

### Improvement 1: Difference Array (Lazy Propagation) - O(n + q)
**Description**: Use difference array to handle range updates efficiently and answer point queries in O(1) time.

```python
def range_update_difference_array(n, q, arr, queries):
    # Build difference array
    diff = [0] * (n + 1)
    diff[0] = arr[0]
    for i in range(1, n):
        diff[i] = arr[i] - arr[i-1]
    
    results = []
    for query in queries:
        if query[0] == 1:  # Range update
            a, b, x = query[1], query[2], query[3]
            # Convert to 0-indexed
            start, end = a - 1, b - 1
            # Update difference array
            diff[start] += x
            if end + 1 < n:
                diff[end + 1] -= x
        else:  # Point query
            k = query[1]
            # Convert to 0-indexed
            pos = k - 1
            # Calculate current value using difference array
            current_value = 0
            for i in range(pos + 1):
                current_value += diff[i]
            results.append(current_value)
    
    return results
```

**Why this improvement works**: Difference array allows us to perform range updates in O(1) time and answer point queries efficiently.

## Final Optimal Solution

```python
n, q = map(int, input().split())
arr = list(map(int, input().split()))

# Build difference array
diff = [0] * (n + 1)
diff[0] = arr[0]
for i in range(1, n):
    diff[i] = arr[i] - arr[i-1]

# Process queries
for _ in range(q):
    query = list(map(int, input().split()))
    
    if query[0] == 1:  # Range update
        a, b, x = query[1], query[2], query[3]
        # Convert to 0-indexed
        start, end = a - 1, b - 1
        # Update difference array
        diff[start] += x
        if end + 1 < n:
            diff[end + 1] -= x
    else:  # Point query
        k = query[1]
        # Convert to 0-indexed
        pos = k - 1
        # Calculate current value using difference array
        current_value = 0
        for i in range(pos + 1):
            current_value += diff[i]
        print(current_value)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(1) | Update array for each range update |
| Difference Array | O(n + q) | O(n) | Use difference array for range updates |

## Key Insights for Other Problems

### 1. **Range Update Queries**
**Principle**: Use difference array to handle range updates efficiently.
**Applicable to**: Range update problems, lazy propagation, query optimization

### 2. **Difference Array Technique**
**Principle**: Store differences between consecutive elements to enable fast range updates.
**Applicable to**: Range problems, update problems, difference techniques

### 3. **Lazy Propagation**
**Principle**: Defer updates until they are actually needed for queries.
**Applicable to**: Range problems, update problems, optimization techniques

## Notable Techniques

### 1. **Difference Array Construction**
```python
def build_difference_array(arr):
    n = len(arr)
    diff = [0] * (n + 1)
    diff[0] = arr[0]
    for i in range(1, n):
        diff[i] = arr[i] - arr[i-1]
    return diff
```

### 2. **Range Update Pattern**
```python
def range_update(diff, left, right, value):
    diff[left] += value
    if right + 1 < len(diff):
        diff[right + 1] -= value
```

### 3. **Point Query Pattern**
```python
def point_query(diff, position):
    current_value = 0
    for i in range(position + 1):
        current_value += diff[i]
    return current_value
```

## Problem-Solving Framework

1. **Identify query type**: This is a range update and point query problem
2. **Choose data structure**: Use difference array for efficient range updates
3. **Build difference array**: Create difference array from initial array
4. **Process queries**: Handle range updates and point queries using difference array
5. **Handle indexing**: Convert between 1-indexed and 0-indexed as needed

---

*This analysis shows how to efficiently handle range update queries using difference array technique.* 