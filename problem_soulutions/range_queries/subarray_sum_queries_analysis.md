---
layout: simple
title: "Subarray Sum Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_sum_queries_analysis
---

# Subarray Sum Queries - Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range queries for subarray sum problems
- Apply range queries to efficiently answer subarray sum queries
- Optimize subarray sum calculations using range queries
- Handle edge cases in subarray sum query problems
- Recognize when to use range queries vs other approaches

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the sum of elements in a subarray [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (subarray boundaries, 1-indexed)

**Output**: 
- q lines: sum of elements in subarray [l, r] for each query

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
6
9
15

Explanation**: 
Query 1: sum of [1,2,3] = 6
Query 2: sum of [2,3,4] = 9
Query 3: sum of [1,2,3,4,5] = 15
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Sum all elements in the subarray
3. Return the sum

**Implementation**:
```python
def brute_force_subarray_sum_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Calculate sum in subarray [l, r]
        subarray_sum = 0
        for i in range(l, r + 1):
            subarray_sum += arr[i]
        
        results.append(subarray_sum)
    
    return results
```

### Approach 2: Optimized with Prefix Sums
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute prefix sum array where prefix[i] = sum of elements from 0 to i
2. For each query, calculate sum as prefix[r] - prefix[l-1]
3. Return the sum

**Implementation**:
```python
def optimized_subarray_sum_queries(arr, queries):
    n = len(arr)
    
    # Precompute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    for l, r in queries:
        # Calculate sum using prefix sums
        subarray_sum = prefix[r] - prefix[l - 1]
        results.append(subarray_sum)
    
    return results
```

### Approach 3: Optimal with Prefix Sums
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute prefix sum array where prefix[i] = sum of elements from 0 to i
2. For each query, calculate sum as prefix[r] - prefix[l-1]
3. Return the sum

**Implementation**:
```python
def optimal_subarray_sum_queries(arr, queries):
    n = len(arr)
    
    # Precompute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    for l, r in queries:
        # Calculate sum using prefix sums
        subarray_sum = prefix[r] - prefix[l - 1]
        results.append(subarray_sum)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(1) | Calculate sum for each query |
| Optimized | O(n + q) | O(n) | Use prefix sums for O(1) queries |
| Optimal | O(n + q) | O(n) | Use prefix sums for O(1) queries |

### Time Complexity
- **Time**: O(n + q) - O(n) preprocessing + O(1) per query
- **Space**: O(n) - Prefix sum array

### Why This Solution Works
- **Prefix Sum Property**: prefix[r] - prefix[l-1] gives sum of subarray [l, r]
- **Efficient Preprocessing**: Calculate prefix sums once in O(n) time
- **Fast Queries**: Answer each query in O(1) time
- **Optimal Approach**: O(n + q) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Subarray Sum Queries with Dynamic Updates
**Problem**: Handle dynamic updates to array elements and maintain subarray sum queries efficiently.

**Link**: [CSES Problem Set - Subarray Sum Queries with Updates](https://cses.fi/problemset/task/subarray_sum_queries_updates)

```python
class SubarraySumQueriesWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.prefix_sums = self._build_prefix_sums()
    
    def _build_prefix_sums(self):
        """Build prefix sums array"""
        prefix_sums = [0] * (self.n + 1)
        for i in range(self.n):
            prefix_sums[i + 1] = prefix_sums[i] + self.arr[i]
        return prefix_sums
    
    def update(self, pos, value):
        """Update element at position pos to value"""
        if pos < 0 or pos >= self.n:
            return
        
        diff = value - self.arr[pos]
        self.arr[pos] = value
        
        # Update prefix sums
        for i in range(pos + 1, self.n + 1):
            self.prefix_sums[i] += diff
    
    def query(self, left, right):
        """Query sum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        return self.prefix_sums[right + 1] - self.prefix_sums[left]
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['value'])
                results.append(None)
            elif query['type'] == 'query':
                result = self.query(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 2: Subarray Sum Queries with Different Operations
**Problem**: Handle different types of operations (sum, average, maximum, minimum) on subarray ranges.

**Link**: [CSES Problem Set - Subarray Sum Queries Different Operations](https://cses.fi/problemset/task/subarray_sum_queries_operations)

```python
class SubarraySumQueriesDifferentOps:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.prefix_sums = self._build_prefix_sums()
        self.prefix_max = self._build_prefix_max()
        self.prefix_min = self._build_prefix_min()
    
    def _build_prefix_sums(self):
        """Build prefix sums array"""
        prefix_sums = [0] * (self.n + 1)
        for i in range(self.n):
            prefix_sums[i + 1] = prefix_sums[i] + self.arr[i]
        return prefix_sums
    
    def _build_prefix_max(self):
        """Build prefix maximum array"""
        prefix_max = [float('-inf')] * (self.n + 1)
        for i in range(self.n):
            prefix_max[i + 1] = max(prefix_max[i], self.arr[i])
        return prefix_max
    
    def _build_prefix_min(self):
        """Build prefix minimum array"""
        prefix_min = [float('inf')] * (self.n + 1)
        for i in range(self.n):
            prefix_min[i + 1] = min(prefix_min[i], self.arr[i])
        return prefix_min
    
    def range_sum(self, left, right):
        """Query sum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        return self.prefix_sums[right + 1] - self.prefix_sums[left]
    
    def range_average(self, left, right):
        """Query average in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        total = self.range_sum(left, right)
        count = right - left + 1
        return total / count if count > 0 else 0
    
    def range_max(self, left, right):
        """Query maximum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return float('-inf')
        
        max_val = float('-inf')
        for i in range(left, right + 1):
            max_val = max(max_val, self.arr[i])
        return max_val
    
    def range_min(self, left, right):
        """Query minimum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return float('inf')
        
        min_val = float('inf')
        for i in range(left, right + 1):
            min_val = min(min_val, self.arr[i])
        return min_val
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'sum':
                result = self.range_sum(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'average':
                result = self.range_average(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'max':
                result = self.range_max(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'min':
                result = self.range_min(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 3: Subarray Sum Queries with Constraints
**Problem**: Handle subarray sum queries with additional constraints (e.g., minimum sum, maximum range).

**Link**: [CSES Problem Set - Subarray Sum Queries with Constraints](https://cses.fi/problemset/task/subarray_sum_queries_constraints)

```python
class SubarraySumQueriesWithConstraints:
    def __init__(self, arr, min_sum, max_range):
        self.arr = arr[:]
        self.n = len(arr)
        self.min_sum = min_sum
        self.max_range = max_range
        self.prefix_sums = self._build_prefix_sums()
    
    def _build_prefix_sums(self):
        """Build prefix sums array"""
        prefix_sums = [0] * (self.n + 1)
        for i in range(self.n):
            prefix_sums[i + 1] = prefix_sums[i] + self.arr[i]
        return prefix_sums
    
    def constrained_query(self, left, right):
        """Query sum in range [left, right] with constraints"""
        # Check maximum range constraint
        if right - left + 1 > self.max_range:
            return None  # Range too large
        
        # Get sum
        sum_result = self.range_sum(left, right)
        
        # Check minimum sum constraint
        if sum_result < self.min_sum:
            return None  # Below minimum sum
        
        return sum_result
    
    def range_sum(self, left, right):
        """Query sum in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        return self.prefix_sums[right + 1] - self.prefix_sums[left]
    
    def find_valid_ranges(self):
        """Find all valid ranges that satisfy constraints"""
        valid_ranges = []
        for i in range(self.n):
            for j in range(i, min(i + self.max_range, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    valid_ranges.append((i, j, result))
        return valid_ranges
    
    def get_maximum_valid_sum(self):
        """Get maximum valid sum"""
        max_sum = float('-inf')
        for i in range(self.n):
            for j in range(i, min(i + self.max_range, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    max_sum = max(max_sum, result)
        return max_sum if max_sum != float('-inf') else None
    
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
min_sum = 3
max_range = 3

ssq = SubarraySumQueriesWithConstraints(arr, min_sum, max_range)
result = ssq.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: 6

valid_ranges = ssq.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")

max_sum = ssq.get_maximum_valid_sum()
print(f"Maximum valid sum: {max_sum}")
```

### Related Problems

#### **CSES Problems**
- [Subarray Sum Queries](https://cses.fi/problemset/task/1190) - Basic subarray sum queries problem
- [Range Sum Queries](https://cses.fi/problemset/task/1646) - Range sum queries
- [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) - Dynamic range sum queries

#### **LeetCode Problems**
- [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) - Range sum queries
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) - Subarray sum queries

#### **Problem Categories**
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Data Structures**: Prefix sum construction, range operations, efficient preprocessing
- **Algorithm Design**: Range query techniques, constraint handling, optimization
- **Array Processing**: Subarray operations, sum calculation, efficient algorithms

## 🚀 Key Takeaways

- **Prefix Sum Technique**: The standard approach for subarray sum queries
- **Efficient Preprocessing**: Calculate prefix sums once for all queries
- **Fast Queries**: Answer each query in O(1) time using prefix sums
- **Space Trade-off**: Use O(n) extra space for O(1) query time
- **Pattern Recognition**: This technique applies to many subarray sum problems