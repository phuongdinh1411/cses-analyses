---
layout: simple
title: "Static Range Minimum Queries - Sparse Table"
permalink: /problem_soulutions/range_queries/static_range_minimum_queries_analysis
---

# Static Range Minimum Queries - Sparse Table

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement sparse table technique for range minimum queries
- Apply sparse table to efficiently answer static range minimum queries
- Optimize range minimum calculations using sparse table
- Handle edge cases in sparse table problems
- Recognize when to use sparse table vs other approaches

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the minimum element in a range [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (range boundaries, 1-indexed)

**Output**: 
- q lines: minimum element in range [l, r] for each query

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
1. For each query, iterate through the range [l, r]
2. Find minimum element in the range
3. Return the minimum

**Implementation**:
```python
def brute_force_static_range_minimum_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Find minimum in range [l, r]
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
2. For each query, find the largest power of 2 that fits in the range
3. Use sparse table to find minimum in O(1) time
4. Return the minimum

**Implementation**:
```python
def optimized_static_range_minimum_queries(arr, queries):
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
2. For each query, find the largest power of 2 that fits in the range
3. Use sparse table to find minimum in O(1) time
4. Return the minimum

**Implementation**:
```python
def optimal_static_range_minimum_queries(arr, queries):
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

### Variation 1: Static Range Minimum Queries with Different Operations
**Problem**: Handle different types of operations (minimum, maximum, GCD, LCM) on static ranges.

**Link**: [CSES Problem Set - Static Range Minimum Queries Different Operations](https://cses.fi/problemset/task/static_range_minimum_queries_operations)

```python
class StaticRangeQueriesDifferentOps:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.log_n = self._log2(self.n)
        self.st_min = self._build_sparse_table_min()
        self.st_max = self._build_sparse_table_max()
        self.st_gcd = self._build_sparse_table_gcd()
        self.st_lcm = self._build_sparse_table_lcm()
    
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
    
    def _build_sparse_table_gcd(self):
        """Build sparse table for GCD queries"""
        st = [[0] * (self.log_n + 1) for _ in range(self.n)]
        
        # Initialize for length 1
        for i in range(self.n):
            st[i][0] = self.arr[i]
        
        # Build for lengths 2^j
        for j in range(1, self.log_n + 1):
            for i in range(self.n - (1 << j) + 1):
                st[i][j] = self._gcd(st[i][j-1], st[i + (1 << (j-1))][j-1])
        
        return st
    
    def _build_sparse_table_lcm(self):
        """Build sparse table for LCM queries"""
        st = [[0] * (self.log_n + 1) for _ in range(self.n)]
        
        # Initialize for length 1
        for i in range(self.n):
            st[i][0] = self.arr[i]
        
        # Build for lengths 2^j
        for j in range(1, self.log_n + 1):
            for i in range(self.n - (1 << j) + 1):
                st[i][j] = self._lcm(st[i][j-1], st[i + (1 << (j-1))][j-1])
        
        return st
    
    def _gcd(self, a, b):
        """Calculate GCD of two numbers"""
        while b:
            a, b = b, a % b
        return a
    
    def _lcm(self, a, b):
        """Calculate LCM of two numbers"""
        return (a * b) // self._gcd(a, b)
    
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
    
    def range_gcd(self, left, right):
        """Query GCD in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        length = right - left + 1
        j = self._log2(length)
        return self._gcd(self.st_gcd[left][j], self.st_gcd[right - (1 << j) + 1][j])
    
    def range_lcm(self, left, right):
        """Query LCM in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 1
        
        length = right - left + 1
        j = self._log2(length)
        return self._lcm(self.st_lcm[left][j], self.st_lcm[right - (1 << j) + 1][j])
```

### Variation 2: Static Range Minimum Queries with Range Updates
**Problem**: Handle range updates and maintain static range minimum queries efficiently.

**Link**: [CSES Problem Set - Static Range Minimum Queries with Updates](https://cses.fi/problemset/task/static_range_minimum_queries_updates)

```python
class StaticRangeMinQueriesWithUpdates:
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
    
    def range_update(self, left, right, value):
        """Update range [left, right] to value"""
        for i in range(left, right + 1):
            self.arr[i] = value
        
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
                self.range_update(query['left'], query['right'], query['value'])
                results.append(None)
            elif query['type'] == 'query':
                result = self.range_min(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 3: Static Range Minimum Queries with Constraints
**Problem**: Handle static range minimum queries with additional constraints (e.g., maximum value, minimum range).

**Link**: [CSES Problem Set - Static Range Minimum Queries with Constraints](https://cses.fi/problemset/task/static_range_minimum_queries_constraints)

```python
class StaticRangeMinQueriesWithConstraints:
    def __init__(self, arr, max_value, min_range):
        self.arr = arr[:]
        self.n = len(arr)
        self.max_value = max_value
        self.min_range = min_range
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
        # Check minimum range constraint
        if right - left + 1 < self.min_range:
            return None  # Invalid range length
        
        # Get minimum
        min_value = self.range_min(left, right)
        
        # Check maximum value constraint
        if min_value > self.max_value:
            return None  # Exceeds maximum value
        
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
            for j in range(i + self.min_range - 1, self.n):
                result = self.constrained_query(i, j)
                if result is not None:
                    valid_ranges.append((i, j, result))
        return valid_ranges
    
    def get_maximum_valid_minimum(self):
        """Get maximum valid minimum"""
        max_min = float('-inf')
        for i in range(self.n):
            for j in range(i + self.min_range - 1, self.n):
                result = self.constrained_query(i, j)
                if result is not None:
                    max_min = max(max_min, result)
        return max_min if max_min != float('-inf') else None

# Example usage
arr = [1, 2, 3, 4, 5]
max_value = 4
min_range = 2

srmq = StaticRangeMinQueriesWithConstraints(arr, max_value, min_range)
result = srmq.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: 1

valid_ranges = srmq.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")
```

### Related Problems

#### **CSES Problems**
- [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) - Basic static range minimum queries problem
- [Static Range Sum Queries](https://cses.fi/problemset/task/1646) - Static range sum queries
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Dynamic range sum queries

#### **LeetCode Problems**
- [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) - Range sum queries
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) - Sliding window maximum

#### **Problem Categories**
- **Sparse Tables**: Range minimum/maximum queries, efficient preprocessing, fast queries
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Data Structures**: Sparse table construction, range operations, efficient preprocessing
- **Algorithm Design**: Sparse table techniques, range optimization, constraint handling

## 🚀 Key Takeaways

- **Sparse Table Technique**: The standard approach for static range minimum queries
- **Efficient Preprocessing**: Calculate sparse table once for all queries
- **Fast Queries**: Answer each query in O(1) time using sparse table
- **Space Trade-off**: Use O(n log n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many static range query problems