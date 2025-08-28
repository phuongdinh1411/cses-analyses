---
layout: simple
title: CSES Salary Queries - Problem Analysis
permalink: /problem_soulutions/range_queries/salary_queries_analysis/
---

# CSES Salary Queries - Problem Analysis

## Problem Statement
Given an array of n integers representing salaries, process q queries. Each query is either:
1. Update the salary at position k to x
2. Count the number of salaries in range [a,b]

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x1,x2,…,xn: the salaries.
Finally, there are q lines describing the queries. Each line has either:
- "! k x": update the salary at position k to x
- "? a b": count salaries in range [a,b]

### Output
Print the answer to each count query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9
- 1 ≤ k ≤ n
- 1 ≤ a ≤ b ≤ 10^9

### Example
```
Input:
5 3
3 7 2 2 5
? 2 3
! 3 6
? 2 3

Output:
2
1
```

## Solution Progression

### Approach 1: Linear Search for Each Query - O(q × n)
**Description**: For each count query, iterate through the array and count salaries in the range. For updates, simply modify the array.

```python
def salary_queries_naive(n, q, salaries, queries):
    results = []
    
    for query in queries:
        if query[0] == '!':  # Update
            k, x = query[1], query[2]
            salaries[k-1] = x  # Convert to 0-indexed
        else:  # Count query
            a, b = query[1], query[2]
            count = 0
            for salary in salaries:
                if a <= salary <= b:
                    count += 1
            results.append(count)
    
    return results
```

**Why this is inefficient**: For each count query, we need to iterate through the entire array, leading to O(q × n) time complexity.

### Improvement 1: Coordinate Compression with Binary Indexed Tree - O(n log n + q log n)
**Description**: Use coordinate compression and Binary Indexed Tree to handle range count queries efficiently.

```python
def salary_queries_coordinate_compression(n, q, salaries, queries):
    from bisect import bisect_left, bisect_right
    
    # Collect all unique values for coordinate compression
    all_values = set(salaries.copy())
    for query in queries:
        if query[0] == '!':
            all_values.add(query[2])
        else:
            all_values.add(query[1])
            all_values.add(query[2])
    
    # Create coordinate mapping
    sorted_values = sorted(all_values)
    value_to_index = {val: idx for idx, val in enumerate(sorted_values)}
    
    class BIT:
        def __init__(self, size):
            self.size = size
            self.tree = [0] * (size + 1)
        
        def update(self, index, value):
            while index <= self.size:
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
    bit = BIT(len(sorted_values))
    for salary in salaries:
        idx = value_to_index[salary]
        bit.update(idx + 1, 1)  # Convert to 1-indexed
    
    results = []
    for query in queries:
        if query[0] == '!':  # Update
            k, x = query[1], query[2]
            old_salary = salaries[k-1]
            old_idx = value_to_index[old_salary]
            new_idx = value_to_index[x]
            
            # Remove old salary
            bit.update(old_idx + 1, -1)
            # Add new salary
            bit.update(new_idx + 1, 1)
            salaries[k-1] = x
        else:  # Count query
            a, b = query[1], query[2]
            # Find indices for range [a, b]
            left_idx = bisect_left(sorted_values, a)
            right_idx = bisect_right(sorted_values, b) - 1
            
            if left_idx <= right_idx:
                count = bit.range_query(left_idx + 1, right_idx + 1)
            else:
                count = 0
            results.append(count)
    
    return results
```

**Why this improvement works**: Coordinate compression reduces the range of values, and Binary Indexed Tree allows efficient range count queries.

## Final Optimal Solution

```python
n, q = map(int, input().split())
salaries = list(map(int, input().split()))

from bisect import bisect_left, bisect_right

# Collect all unique values for coordinate compression
all_values = set(salaries.copy())
queries = []
for _ in range(q):
    query = input().split()
    if query[0] == '!':
        k, x = int(query[1]), int(query[2])
        all_values.add(x)
    else:
        a, b = int(query[1]), int(query[2])
        all_values.add(a)
        all_values.add(b)
    queries.append(query)

# Create coordinate mapping
sorted_values = sorted(all_values)
value_to_index = {val: idx for idx, val in enumerate(sorted_values)}

class BIT:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)
    
    def update(self, index, value):
        while index <= self.size:
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
bit = BIT(len(sorted_values))
for salary in salaries:
    idx = value_to_index[salary]
    bit.update(idx + 1, 1)  # Convert to 1-indexed

# Process queries
for query in queries:
    if query[0] == '!':  # Update
        k, x = int(query[1]), int(query[2])
        old_salary = salaries[k-1]
        old_idx = value_to_index[old_salary]
        new_idx = value_to_index[x]
        
        # Remove old salary
        bit.update(old_idx + 1, -1)
        # Add new salary
        bit.update(new_idx + 1, 1)
        salaries[k-1] = x
    else:  # Count query
        a, b = int(query[1]), int(query[2])
        # Find indices for range [a, b]
        left_idx = bisect_left(sorted_values, a)
        right_idx = bisect_right(sorted_values, b) - 1
        
        if left_idx <= right_idx:
            count = bit.range_query(left_idx + 1, right_idx + 1)
        else:
            count = 0
        print(count)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(1) | Linear search for each query |
| Coordinate Compression + BIT | O(n log n + q log n) | O(n) | Use coordinate compression and BIT |

## Key Insights for Other Problems

### 1. **Range Count Queries**
**Principle**: Use coordinate compression to handle large value ranges efficiently.
**Applicable to**: Range count problems, coordinate compression, query optimization

### 2. **Coordinate Compression**
**Principle**: Map large value ranges to smaller indices for efficient processing.
**Applicable to**: Large value problems, range problems, compression techniques

### 3. **Binary Indexed Tree for Counting**
**Principle**: Use BIT to efficiently count elements in ranges.
**Applicable to**: Counting problems, range problems, tree-based data structures

## Notable Techniques

### 1. **Coordinate Compression Implementation**
```python
def coordinate_compression(values):
    sorted_values = sorted(set(values))
    value_to_index = {val: idx for idx, val in enumerate(sorted_values)}
    return value_to_index, sorted_values
```

### 2. **Range Count Query**
```python
def range_count_query(bit, sorted_values, value_to_index, a, b):
    from bisect import bisect_left, bisect_right
    
    left_idx = bisect_left(sorted_values, a)
    right_idx = bisect_right(sorted_values, b) - 1
    
    if left_idx <= right_idx:
        return bit.range_query(left_idx + 1, right_idx + 1)
    else:
        return 0
```

### 3. **Update Pattern**
```python
def update_salary(bit, value_to_index, old_salary, new_salary):
    old_idx = value_to_index[old_salary]
    new_idx = value_to_index[new_salary]
    
    bit.update(old_idx + 1, -1)
    bit.update(new_idx + 1, 1)
```

## Problem-Solving Framework

1. **Identify query type**: This is a dynamic range count query problem
2. **Choose data structure**: Use coordinate compression and Binary Indexed Tree
3. **Compress coordinates**: Map large values to smaller indices
4. **Initialize BIT**: Build tree from compressed values
5. **Process queries**: Handle updates and count queries using compressed indices

---

*This analysis shows how to efficiently handle dynamic range count queries using coordinate compression and Binary Indexed Tree technique.* 