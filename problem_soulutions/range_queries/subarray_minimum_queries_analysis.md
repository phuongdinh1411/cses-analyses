---
layout: simple
title: "Subarray Minimum Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_minimum_queries_analysis
---

# Subarray Minimum Queries - Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range queries for subarray minimum problems
- Apply range queries to efficiently answer subarray minimum queries
- Optimize subarray minimum calculations using range queries
- Handle edge cases in subarray minimum query problems
- Recognize when to use range queries vs other approaches

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the minimum element in a subarray [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (subarray boundaries, 1-indexed)

**Output**: 
- q lines: minimum element in subarray [l, r] for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- -10⁹ ≤ arr[i] ≤ 10⁹
- 1 ≤ l ≤ r ≤ n

**Example**:
```
Input:
5 3
1 2 3 4 5
1 3
2 4
1 5

Output:
1
2
1

Explanation**: 
Query 1: minimum of [1,2,3] = 1
Query 2: minimum of [2,3,4] = 2
Query 3: minimum of [1,2,3,4,5] = 1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Find minimum element in the subarray
3. Return the minimum

**Implementation**:
```python
def brute_force_subarray_minimum_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Find minimum in subarray [l, r]
        min_val = float('inf')
        for i in range(l, r + 1):
            min_val = min(min_val, arr[i])
        
        results.append(min_val)
    
    return results
```

### Approach 2: Optimized with Sparse Table
**Time Complexity**: O(n log n + q)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute sparse table where st[i][j] = minimum in range [i, i + 2^j - 1]
2. For each query, use sparse table to find minimum in O(1) time
3. Return the minimum

**Implementation**:
```python
def optimized_subarray_minimum_queries(arr, queries):
    n = len(arr)
    
    # Precompute sparse table
    log_n = 0
    while (1 << log_n) <= n:
        log_n += 1
    
    st = [[0] * log_n for _ in range(n)]
    
    # Initialize for length 1
    for i in range(n):
        st[i][0] = arr[i]
    
    # Fill sparse table
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1])
    
    results = []
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Find largest power of 2 that fits in range
        length = r - l + 1
        k = 0
        while (1 << (k + 1)) <= length:
            k += 1
        
        # Query minimum using sparse table
        min_val = min(st[l][k], st[r - (1 << k) + 1][k])
        results.append(min_val)
    
    return results
```

### Approach 3: Optimal with Sparse Table
**Time Complexity**: O(n log n + q)  
**Space Complexity**: O(n log n)

**Algorithm**:
1. Precompute sparse table where st[i][j] = minimum in range [i, i + 2^j - 1]
2. For each query, use sparse table to find minimum in O(1) time
3. Return the minimum

**Implementation**:
```python
def optimal_subarray_minimum_queries(arr, queries):
    n = len(arr)
    
    # Precompute sparse table
    log_n = 0
    while (1 << log_n) <= n:
        log_n += 1
    
    st = [[0] * log_n for _ in range(n)]
    
    # Initialize for length 1
    for i in range(n):
        st[i][0] = arr[i]
    
    # Fill sparse table
    for j in range(1, log_n):
        for i in range(n - (1 << j) + 1):
            st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1])
    
    results = []
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Find largest power of 2 that fits in range
        length = r - l + 1
        k = 0
        while (1 << (k + 1)) <= length:
            k += 1
        
        # Query minimum using sparse table
        min_val = min(st[l][k], st[r - (1 << k) + 1][k])
        results.append(min_val)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Find minimum for each query |
| Optimized | O(n log n + q) | O(n log n) | Use sparse table for O(1) queries |
| Optimal | O(n log n + q) | O(n log n) | Use sparse table for O(1) queries |

### Time Complexity
- **Time**: O(n log n + q) - O(n log n) preprocessing + O(1) per query
- **Space**: O(n log n) - Sparse table

### Why This Solution Works
- **Sparse Table Property**: st[i][j] stores minimum in range [i, i + 2^j - 1]
- **Efficient Preprocessing**: Calculate sparse table in O(n log n) time
- **Fast Queries**: Answer each query in O(1) time using sparse table
- **Optimal Approach**: O(n log n + q) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Subarray Minimum Queries with Dynamic Updates
**Problem**: Handle dynamic updates to array elements and maintain subarray minimum queries efficiently.

**Link**: [CSES Problem Set - Subarray Minimum Queries with Updates](https://cses.fi/problemset/task/subarray_minimum_queries_updates)

```python
class SubarrayMinimumQueriesWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.log_n = self._log2(self.n)
        self.st = self._build_sparse_table()
    
    def _log2(self, n):
        """Calculate log2 of n"""
        result = 0
        while (1 << result) <= n:
            result += 1
        return result - 1
    
    def _build_sparse_table(self):
        """Build sparse table for minimum queries"""
        st = [[0] * (self.log_n + 1) for _ in range(self.n)]
        
        # Initialize for length 1
        for i in range(self.n):
            st[i][0] = self.arr[i]
        
        # Build for lengths 2^j
        for j in range(1, self.log_n + 1):
            for i in range(self.n - (1 << j) + 1):
                st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1])
        
        return st
    
    def update(self, pos, value):
        """Update element at position pos to value"""
        if pos < 0 or pos >= self.n:
            return
        
        self.arr[pos] = value
        
        # Rebuild sparse table
        self.st = self._build_sparse_table()
    
    def range_min(self, left, right):
        """Query minimum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return float('inf')
        
        length = right - left + 1
        j = self._log2(length)
        return min(self.st[left][j], self.st[right - (1 << j) + 1][j])
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['value'])
                results.append(None)
            elif query['type'] == 'query':
                result = self.range_min(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 2: Subarray Minimum Queries with Different Operations
**Problem**: Handle different types of operations (minimum, maximum, sum) on subarray ranges.

**Link**: [CSES Problem Set - Subarray Minimum Queries Different Operations](https://cses.fi/problemset/task/subarray_minimum_queries_operations)

```python
class SubarrayMinimumQueriesDifferentOps:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.log_n = self._log2(self.n)
        self.st_min = self._build_sparse_table_min()
        self.st_max = self._build_sparse_table_max()
        self.st_sum = self._build_sparse_table_sum()
    
    def _log2(self, n):
        """Calculate log2 of n"""
        result = 0
        while (1 << result) <= n:
            result += 1
        return result - 1
    
    def _build_sparse_table_min(self):
        """Build sparse table for minimum queries"""
        st = [[0] * (self.log_n + 1) for _ in range(self.n)]
        
        # Initialize for length 1
        for i in range(self.n):
            st[i][0] = self.arr[i]
        
        # Build for lengths 2^j
        for j in range(1, self.log_n + 1):
            for i in range(self.n - (1 << j) + 1):
                st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1])
        
        return st
    
    def _build_sparse_table_max(self):
        """Build sparse table for maximum queries"""
        st = [[0] * (self.log_n + 1) for _ in range(self.n)]
        
        # Initialize for length 1
        for i in range(self.n):
            st[i][0] = self.arr[i]
        
        # Build for lengths 2^j
        for j in range(1, self.log_n + 1):
            for i in range(self.n - (1 << j) + 1):
                st[i][j] = max(st[i][j-1], st[i + (1 << (j-1))][j-1])
        
        return st
    
    def _build_sparse_table_sum(self):
        """Build sparse table for sum queries"""
        st = [[0] * (self.log_n + 1) for _ in range(self.n)]
        
        # Initialize for length 1
        for i in range(self.n):
            st[i][0] = self.arr[i]
        
        # Build for lengths 2^j
        for j in range(1, self.log_n + 1):
            for i in range(self.n - (1 << j) + 1):
                st[i][j] = st[i][j-1] + st[i + (1 << (j-1))][j-1]
        
        return st
    
    def range_min(self, left, right):
        """Query minimum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return float('inf')
        
        length = right - left + 1
        j = self._log2(length)
        return min(self.st_min[left][j], self.st_min[right - (1 << j) + 1][j])
    
    def range_max(self, left, right):
        """Query maximum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return float('-inf')
        
        length = right - left + 1
        j = self._log2(length)
        return max(self.st_max[left][j], self.st_max[right - (1 << j) + 1][j])
    
    def range_sum(self, left, right):
        """Query sum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        total = 0
        while left <= right:
            length = right - left + 1
            j = self._log2(length)
            total += self.st_sum[left][j]
            left += (1 << j)
        
        return total
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'min':
                result = self.range_min(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'max':
                result = self.range_max(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'sum':
                result = self.range_sum(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 3: Subarray Minimum Queries with Constraints
**Problem**: Handle subarray minimum queries with additional constraints (e.g., minimum value, maximum range).

**Link**: [CSES Problem Set - Subarray Minimum Queries with Constraints](https://cses.fi/problemset/task/subarray_minimum_queries_constraints)

```python
class SubarrayMinimumQueriesWithConstraints:
    def __init__(self, arr, min_value, max_range):
        self.arr = arr[:]
        self.n = len(arr)
        self.min_value = min_value
        self.max_range = max_range
        self.log_n = self._log2(self.n)
        self.st = self._build_sparse_table()
    
    def _log2(self, n):
        """Calculate log2 of n"""
        result = 0
        while (1 << result) <= n:
            result += 1
        return result - 1
    
    def _build_sparse_table(self):
        """Build sparse table for minimum queries"""
        st = [[0] * (self.log_n + 1) for _ in range(self.n)]
        
        # Initialize for length 1
        for i in range(self.n):
            st[i][0] = self.arr[i]
        
        # Build for lengths 2^j
        for j in range(1, self.log_n + 1):
            for i in range(self.n - (1 << j) + 1):
                st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1])
        
        return st
    
    def constrained_query(self, left, right):
        """Query minimum in range [left, right] with constraints"""
        # Check maximum range constraint
        if right - left + 1 > self.max_range:
            return None  # Range too large
        
        # Get minimum
        min_value = self.range_min(left, right)
        
        # Check minimum value constraint
        if min_value < self.min_value:
            return None  # Below minimum value
        
        return min_value
    
    def range_min(self, left, right):
        """Query minimum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return float('inf')
        
        length = right - left + 1
        j = self._log2(length)
        return min(self.st[left][j], self.st[right - (1 << j) + 1][j])
    
    def find_valid_ranges(self):
        """Find all valid ranges that satisfy constraints"""
        valid_ranges = []
        for i in range(self.n):
            for j in range(i, min(i + self.max_range, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    valid_ranges.append((i, j, result))
        return valid_ranges
    
    def get_minimum_valid_minimum(self):
        """Get minimum valid minimum"""
        min_min = float('inf')
        for i in range(self.n):
            for j in range(i, min(i + self.max_range, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    min_min = min(min_min, result)
        return min_min if min_min != float('inf') else None
    
    def count_valid_ranges(self):
        """Count number of valid ranges"""
        count = 0
        for i in range(self.n):
            for j in range(i, min(i + self.max_range, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    count += 1
        return count

# Example usage
arr = [1, 2, 3, 4, 5]
min_value = 2
max_range = 3

smq = SubarrayMinimumQueriesWithConstraints(arr, min_value, max_range)
result = smq.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: 1

valid_ranges = smq.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")

min_min = smq.get_minimum_valid_minimum()
print(f"Minimum valid minimum: {min_min}")
```

### Related Problems

#### **CSES Problems**
- [Subarray Minimum Queries](https://cses.fi/problemset/task/1647) - Basic subarray minimum queries problem
- [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) - Static range minimum queries
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Dynamic range sum queries

#### **LeetCode Problems**
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) - Sliding window maximum
- [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) - Range sum queries
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates

#### **Problem Categories**
- **Sparse Tables**: Range minimum/maximum queries, efficient preprocessing, fast queries
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Data Structures**: Sparse table construction, range operations, efficient preprocessing
- **Algorithm Design**: Sparse table techniques, range optimization, constraint handling

## 🚀 Key Takeaways

- **Sparse Table Technique**: The standard approach for subarray minimum queries
- **Efficient Preprocessing**: Calculate sparse table once for all queries
- **Fast Queries**: Answer each query in O(1) time using sparse table
- **Space Trade-off**: Use O(n log n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many subarray minimum problems