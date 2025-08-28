---
layout: simple
title: "Salary Queries
permalink: /problem_soulutions/range_queries/salary_queries_analysis/"
---


# Salary Queries

## Problem Statement
Given an array of n integers representing salaries, process q queries. Each query is either:
1. Update the salary at position k to x
2. Count the number of salaries in range [a,b]

### Input
The first input line has two integers n and q: the size of the array and the number of queries.
The second line has n integers x1,x2,…,xn: the salaries.
Finally, there are q lines describing the queries. Each line has either:"
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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Salary Queries with Range Updates**
**Problem**: Support range updates (modify salaries in a range) and point count queries.
```python
def salary_queries_range_updates(n, q, salaries, operations):
    from bisect import bisect_left, bisect_right
    
    # Collect all unique values for coordinate compression
    all_values = set(salaries.copy())
    for op in operations:
        if op[0] == 'RANGE_UPDATE':
            all_values.add(op[3])  # New salary value
        else:
            all_values.add(op[1])
            all_values.add(op[2])
    
    # Create coordinate mapping
    sorted_values = sorted(all_values)
    value_to_index = {val: idx for idx, val in enumerate(sorted_values)}
    
    class LazyBIT:
        def __init__(self, size):
            self.size = size
            self.tree = [0] * (size + 1)
            self.lazy = [0] * (size + 1)
        
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
        
        def range_update(self, left, right, value):
            # For range updates, we need to update each position
            for i in range(left, right + 1):
                self.update(i, value)
    
    # Initialize BIT
    bit = LazyBIT(len(sorted_values))
    for salary in salaries:
        idx = value_to_index[salary]
        bit.update(idx + 1, 1)
    
    results = []
    for op in operations:
        if op[0] == 'RANGE_UPDATE':  # Range update
            l, r, new_salary = op[1], op[2], op[3]
            new_idx = value_to_index[new_salary]
            
            # Remove old salaries in range
            for i in range(l-1, r):
                old_salary = salaries[i]
                old_idx = value_to_index[old_salary]
                bit.update(old_idx + 1, -1)
            
            # Add new salaries
            for i in range(l-1, r):
                salaries[i] = new_salary
                bit.update(new_idx + 1, 1)
        else:  # Count query
            a, b = op[1], op[2]
            left_idx = bisect_left(sorted_values, a)
            right_idx = bisect_right(sorted_values, b) - 1
            
            if left_idx <= right_idx:
                count = bit.range_query(left_idx + 1, right_idx + 1)
            else:
                count = 0
            results.append(count)
    
    return results
```

#### **Variation 2: Salary Queries with Multiple Ranges**
**Problem**: Support queries for multiple salary ranges simultaneously.
```python
def salary_queries_multiple_ranges(n, q, salaries, operations):
    from bisect import bisect_left, bisect_right
    
    # Collect all unique values
    all_values = set(salaries.copy())
    for op in operations:
        if op[0] == '!':
            all_values.add(op[2])
        else:
            # Multiple ranges
            for i in range(1, len(op), 2):
                all_values.add(op[i])
                all_values.add(op[i+1])
    
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
    
    bit = BIT(len(sorted_values))
    for salary in salaries:
        idx = value_to_index[salary]
        bit.update(idx + 1, 1)
    
    results = []
    for op in operations:
        if op[0] == '!':  # Update
            k, x = op[1], op[2]
            old_salary = salaries[k-1]
            old_idx = value_to_index[old_salary]
            new_idx = value_to_index[x]
            
            bit.update(old_idx + 1, -1)
            bit.update(new_idx + 1, 1)
            salaries[k-1] = x
        else:  # Multiple range count query
            range_counts = []
            for i in range(1, len(op), 2):
                a, b = op[i], op[i+1]
                left_idx = bisect_left(sorted_values, a)
                right_idx = bisect_right(sorted_values, b) - 1
                
                if left_idx <= right_idx:
                    count = bit.range_query(left_idx + 1, right_idx + 1)
                else:
                    count = 0
                range_counts.append(count)
            results.append(range_counts)
    
    return results
```

#### **Variation 3: Salary Queries with Weighted Counting**
**Problem**: Each salary has a weight, count weighted sum in salary ranges.
```python
def salary_queries_weighted(n, q, salaries, weights, operations):
    from bisect import bisect_left, bisect_right
    
    # Collect all unique values
    all_values = set(salaries.copy())
    for op in operations:
        if op[0] == '!':
            all_values.add(op[2])
        else:
            all_values.add(op[1])
            all_values.add(op[2])
    
    # Create coordinate mapping
    sorted_values = sorted(all_values)
    value_to_index = {val: idx for idx, val in enumerate(sorted_values)}
    
    class WeightedBIT:
        def __init__(self, size):
            self.size = size
            self.count_tree = [0] * (size + 1)
            self.weight_tree = [0] * (size + 1)
        
        def update(self, index, count_change, weight_change):
            while index <= self.size:
                self.count_tree[index] += count_change
                self.weight_tree[index] += weight_change
                index += index & -index
        
        def query_count(self, index):
            result = 0
            while index > 0:
                result += self.count_tree[index]
                index -= index & -index
            return result
        
        def query_weight(self, index):
            result = 0
            while index > 0:
                result += self.weight_tree[index]
                index -= index & -index
            return result
        
        def range_query(self, left, right):
            count = self.query_count(right) - self.query_count(left - 1)
            weight = self.query_weight(right) - self.query_weight(left - 1)
            return count, weight
    
    bit = WeightedBIT(len(sorted_values))
    for i, salary in enumerate(salaries):
        idx = value_to_index[salary]
        bit.update(idx + 1, 1, weights[i])
    
    results = []
    for op in operations:
        if op[0] == '!':  # Update
            k, x = op[1], op[2]
            old_salary = salaries[k-1]
            old_idx = value_to_index[old_salary]
            new_idx = value_to_index[x]
            
            bit.update(old_idx + 1, -1, -weights[k-1])
            bit.update(new_idx + 1, 1, weights[k-1])
            salaries[k-1] = x
        else:  # Weighted count query
            a, b = op[1], op[2]
            left_idx = bisect_left(sorted_values, a)
            right_idx = bisect_right(sorted_values, b) - 1
            
            if left_idx <= right_idx:
                count, total_weight = bit.range_query(left_idx + 1, right_idx + 1)
            else:
                count, total_weight = 0, 0
            results.append((count, total_weight))
    
    return results
```

#### **Variation 4: Salary Queries with Historical Data**
**Problem**: Support queries about salary distribution at different points in time.
```python
def salary_queries_historical(n, q, salaries, operations):
    from bisect import bisect_left, bisect_right
    
    # Collect all unique values
    all_values = set(salaries.copy())
    for op in operations:
        if op[0] == '!':
            all_values.add(op[2])
        else:
            all_values.add(op[1])
            all_values.add(op[2])
    
    # Create coordinate mapping
    sorted_values = sorted(all_values)
    value_to_index = {val: idx for idx, val in enumerate(sorted_values)}
    
    class HistoricalBIT:
        def __init__(self, size):
            self.size = size
            self.history = []  # Store historical states
            self.current_tree = [0] * (size + 1)
        
        def save_state(self):
            self.history.append(self.current_tree.copy())
        
        def restore_state(self, time):
            if time < len(self.history):
                self.current_tree = self.history[time].copy()
        
        def update(self, index, value):
            while index <= self.size:
                self.current_tree[index] += value
                index += index & -index
        
        def query(self, index):
            result = 0
            while index > 0:
                result += self.current_tree[index]
                index -= index & -index
            return result
        
        def range_query(self, left, right):
            return self.query(right) - self.query(left - 1)
    
    bit = HistoricalBIT(len(sorted_values))
    
    # Initialize with initial salaries
    for salary in salaries:
        idx = value_to_index[salary]
        bit.update(idx + 1, 1)
    bit.save_state()  # Save initial state
    
    results = []
    for op in operations:
        if op[0] == '!':  # Update
            k, x = op[1], op[2]
            old_salary = salaries[k-1]
            old_idx = value_to_index[old_salary]
            new_idx = value_to_index[x]
            
            bit.update(old_idx + 1, -1)
            bit.update(new_idx + 1, 1)
            salaries[k-1] = x
            bit.save_state()  # Save state after update
        else:  # Historical query
            time, a, b = op[1], op[2], op[3]
            bit.restore_state(time)
            
            left_idx = bisect_left(sorted_values, a)
            right_idx = bisect_right(sorted_values, b) - 1
            
            if left_idx <= right_idx:
                count = bit.range_query(left_idx + 1, right_idx + 1)
            else:
                count = 0
            results.append(count)
    
    return results
```

#### **Variation 5: Salary Queries with Percentile Ranges**
**Problem**: Support queries for salary percentiles and percentile-based ranges.
```python
def salary_queries_percentiles(n, q, salaries, operations):
    from bisect import bisect_left, bisect_right
    
    # Collect all unique values
    all_values = set(salaries.copy())
    for op in operations:
        if op[0] == '!':
            all_values.add(op[2])
        else:
            all_values.add(op[1])
            all_values.add(op[2])
    
    # Create coordinate mapping
    sorted_values = sorted(all_values)
    value_to_index = {val: idx for idx, val in enumerate(sorted_values)}
    
    class PercentileBIT:
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
        
        def find_percentile(self, percentile):
            # Find the value at given percentile
            target_count = int(percentile * self.query(self.size) / 100)
            
            left, right = 1, self.size
            while left < right:
                mid = (left + right) // 2
                count = self.query(mid)
                if count < target_count:
                    left = mid + 1
                else:
                    right = mid
            
            return sorted_values[left - 1] if left <= len(sorted_values) else -1
        
        def range_query(self, left, right):
            return self.query(right) - self.query(left - 1)
    
    bit = PercentileBIT(len(sorted_values))
    for salary in salaries:
        idx = value_to_index[salary]
        bit.update(idx + 1, 1)
    
    results = []
    for op in operations:
        if op[0] == '!':  # Update
            k, x = op[1], op[2]
            old_salary = salaries[k-1]
            old_idx = value_to_index[old_salary]
            new_idx = value_to_index[x]
            
            bit.update(old_idx + 1, -1)
            bit.update(new_idx + 1, 1)
            salaries[k-1] = x
        elif op[0] == 'PERCENTILE':  # Percentile query
            percentile = op[1]
            value = bit.find_percentile(percentile)
            results.append(value)
        else:  # Percentile range query
            p1, p2 = op[1], op[2]
            v1 = bit.find_percentile(p1)
            v2 = bit.find_percentile(p2)
            
            if v1 != -1 and v2 != -1:
                left_idx = bisect_left(sorted_values, v1)
                right_idx = bisect_right(sorted_values, v2) - 1
                count = bit.range_query(left_idx + 1, right_idx + 1)
            else:
                count = 0
            results.append(count)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Range Count Data Structures**
- **Binary Indexed Tree**: O(log n) range count queries
- **Segment Tree**: O(log n) range count with lazy propagation
- **Sparse Table**: O(1) queries but static
- **Persistent Segment Tree**: Handle historical queries

#### **2. Coordinate Compression Techniques**
- **Value Mapping**: Map large values to small indices
- **Discrete Values**: Handle discrete value ranges
- **Dynamic Compression**: Handle dynamic value sets
- **Multi-dimensional Compression**: Handle multiple dimensions

#### **3. Advanced Range Counting**
- **Weighted Counting**: Elements have weights
- **Multiple Ranges**: Query multiple ranges simultaneously
- **Percentile Queries**: Find percentiles and percentile ranges
- **Historical Queries**: Query data at different time points

#### **4. Optimization Problems**
- **Optimal Range Selection**: Find optimal ranges for queries
- **Range with Constraints**: Add additional constraints
- **Compression Optimization**: Optimize compression techniques
- **Query Optimization**: Optimize query patterns

#### **5. Competitive Programming Patterns**
- **Binary Search**: Find optimal ranges
- **Two Pointers**: Efficient range processing
- **Sliding Window**: Optimize consecutive ranges
- **Offline Processing**: Process queries in optimal order

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    salaries = list(map(int, input().split()))
    
    # Coordinate compression setup
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
    
    # Process with coordinate compression and BIT
    # ... (implementation)
```

#### **2. Salary Queries with Aggregation**
```python
def salary_queries_aggregation(n, q, salaries, operations):
    from bisect import bisect_left, bisect_right
    
    # Coordinate compression setup
    all_values = set(salaries.copy())
    for op in operations:
        if op[0] == '!':
            all_values.add(op[2])
        else:
            all_values.add(op[1])
            all_values.add(op[2])
    
    sorted_values = sorted(all_values)
    value_to_index = {val: idx for idx, val in enumerate(sorted_values)}
    
    class AggregationBIT:
        def __init__(self, size):
            self.size = size
            self.count_tree = [0] * (size + 1)
            self.sum_tree = [0] * (size + 1)
            self.min_tree = [float('inf')] * (size + 1)
            self.max_tree = [-float('inf')] * (size + 1)
        
        def update(self, index, count_change, value):
            while index <= self.size:
                self.count_tree[index] += count_change
                self.sum_tree[index] += value * count_change
                if count_change > 0:
                    self.min_tree[index] = min(self.min_tree[index], value)
                    self.max_tree[index] = max(self.max_tree[index], value)
                index += index & -index
        
        def query_count(self, index):
            result = 0
            while index > 0:
                result += self.count_tree[index]
                index -= index & -index
            return result
        
        def query_sum(self, index):
            result = 0
            while index > 0:
                result += self.sum_tree[index]
                index -= index & -index
            return result
        
        def range_query(self, left, right, op):
            if op == 'COUNT':
                return self.query_count(right) - self.query_count(left - 1)
            elif op == 'SUM':
                return self.query_sum(right) - self.query_sum(left - 1)
            elif op == 'AVERAGE':
                count = self.query_count(right) - self.query_count(left - 1)
                total = self.query_sum(right) - self.query_sum(left - 1)
                return total / count if count > 0 else 0
    
    bit = AggregationBIT(len(sorted_values))
    for salary in salaries:
        idx = value_to_index[salary]
        bit.update(idx + 1, 1, salary)
    
    results = []
    for op in operations:
        if op[0] == '!':  # Update
            k, x = op[1], op[2]
            old_salary = salaries[k-1]
            old_idx = value_to_index[old_salary]
            new_idx = value_to_index[x]
            
            bit.update(old_idx + 1, -1, old_salary)
            bit.update(new_idx + 1, 1, x)
            salaries[k-1] = x
        else:  # Aggregation query
            a, b, query_type = op[1], op[2], op[3]
            left_idx = bisect_left(sorted_values, a)
            right_idx = bisect_right(sorted_values, b) - 1
            
            if left_idx <= right_idx:
                result = bit.range_query(left_idx + 1, right_idx + 1, query_type)
            else:
                result = 0
            results.append(result)
    
    return results
```

#### **3. Interactive Salary Queries**
```python
def interactive_salary_queries(n, salaries):
    from bisect import bisect_left, bisect_right
    
    # Coordinate compression setup
    all_values = set(salaries.copy())
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
    
    bit = BIT(len(sorted_values))
    for salary in salaries:
        idx = value_to_index[salary]
        bit.update(idx + 1, 1)
    
    while True:
        try:
            query = input().strip()
            if query == 'END':
                break
            
            parts = query.split()
            if parts[0] == 'UPDATE':
                k, x = int(parts[1]), int(parts[2])
                old_salary = salaries[k-1]
                old_idx = value_to_index[old_salary]
                new_idx = value_to_index[x]
                
                bit.update(old_idx + 1, -1)
                bit.update(new_idx + 1, 1)
                salaries[k-1] = x
                print(f"Updated salary at position {k} to {x}")
            elif parts[0] == 'COUNT':
                a, b = int(parts[1]), int(parts[2])
                left_idx = bisect_left(sorted_values, a)
                right_idx = bisect_right(sorted_values, b) - 1
                
                if left_idx <= right_idx:
                    count = bit.range_query(left_idx + 1, right_idx + 1)
                else:
                    count = 0
                print(f"Count of salaries in range [{a},{b}]: {count}")
            
        except EOFError:
            break
```

### 🧮 **Mathematical Extensions**

#### **1. Range Count Properties**
- **Additivity**: count(a,b) + count(c,d) = count(a,d) - count(b+1,c-1) (if ranges overlap)
- **Commutativity**: count(a,b) + count(c,d) = count(c,d) + count(a,b)
- **Associativity**: (count(a,b) + count(c,d)) + count(e,f) = count(a,b) + (count(c,d) + count(e,f))
- **Monotonicity**: If a ≤ b ≤ c ≤ d, then count(a,b) ≤ count(c,d)

#### **2. Optimization Techniques**
- **Early Termination**: Stop if count exceeds threshold
- **Binary Search**: Find ranges with specific counts
- **Caching**: Store frequently accessed counts
- **Compression**: Handle sparse ranges efficiently

#### **3. Advanced Mathematical Concepts**
- **Order Statistics**: Understanding count properties
- **Percentiles**: Finding percentiles efficiently
- **Histograms**: Building frequency distributions
- **Statistical Measures**: Mean, median, mode calculations

#### **4. Algorithmic Improvements**
- **Block Decomposition**: Divide array into blocks
- **Lazy Propagation**: Efficient range updates
- **Compression**: Handle sparse arrays efficiently
- **Parallel Processing**: Use multiple cores for large datasets

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Binary Indexed Tree**: Efficient range count queries
- **Coordinate Compression**: Handle large value ranges
- **Segment Tree**: Dynamic range operations
- **Order Statistics**: Find k-th element efficiently

#### **2. Mathematical Concepts**
- **Range Counting**: Understanding count properties
- **Coordinate Compression**: Mapping large values
- **Percentiles**: Statistical measures
- **Complexity Analysis**: Understanding time/space trade-offs

#### **3. Programming Concepts**
- **Data Structures**: Choosing appropriate count structures
- **Algorithm Design**: Optimizing for count constraints
- **Problem Decomposition**: Breaking complex count problems
- **Code Optimization**: Writing efficient count implementations

---

**Practice these variations to master range count query techniques and coordinate compression!** 🎯 