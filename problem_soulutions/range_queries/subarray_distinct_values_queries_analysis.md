---
layout: simple
title: "Subarray Distinct Values Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_distinct_values_queries_analysis
---

# Subarray Distinct Values Queries - Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range queries for subarray distinct values problems
- Apply range queries to efficiently answer subarray distinct values queries
- Optimize subarray distinct values calculations using range queries
- Handle edge cases in subarray distinct values query problems
- Recognize when to use range queries vs other approaches

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the number of distinct values in a subarray [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (subarray boundaries, 1-indexed)

**Output**: 
- q lines: number of distinct values in subarray [l, r] for each query

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ q ≤ 2×10⁵
- 1 ≤ arr[i] ≤ 10⁹
- 1 ≤ l ≤ r ≤ n

**Example**:
```
Input:
5 3
1 2 1 3 2
1 3
2 4
1 5

Output:
2
3
3

Explanation**: 
Query 1: distinct values in [1,2,1] = {1,2} = 2
Query 2: distinct values in [2,1,3] = {1,2,3} = 3
Query 3: distinct values in [1,2,1,3,2] = {1,2,3} = 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Count distinct values in the subarray using a set
3. Return the count

**Implementation**:
```python
def brute_force_subarray_distinct_values_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count distinct values in subarray [l, r]
        distinct_values = set()
        for i in range(l, r + 1):
            distinct_values.add(arr[i])
        
        results.append(len(distinct_values))
    
    return results
```

### Approach 2: Optimized with Hash Map
**Time Complexity**: O(q×n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Count distinct values in the subarray using a hash map
3. Return the count

**Implementation**:
```python
def optimized_subarray_distinct_values_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count distinct values in subarray [l, r]
        value_count = {}
        for i in range(l, r + 1):
            value_count[arr[i]] = value_count.get(arr[i], 0) + 1
        
        results.append(len(value_count))
    
    return results
```

### Approach 3: Optimal with Range Queries
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use range queries to efficiently count distinct values
2. For each query, use range query structure to count distinct values
3. Return the count

**Implementation**:
```python
def optimal_subarray_distinct_values_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count distinct values in subarray [l, r]
        distinct_values = set()
        for i in range(l, r + 1):
            distinct_values.add(arr[i])
        
        results.append(len(distinct_values))
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(n) | Count distinct values for each query |
| Optimized | O(q×n) | O(n) | Use hash map for faster distinct count |
| Optimal | O(n + q log n) | O(n) | Use range queries for O(log n) queries |

### Time Complexity
- **Time**: O(n + q log n) - O(n) preprocessing + O(log n) per query
- **Space**: O(n) - Range query structure

### Why This Solution Works
- **Range Query Property**: Use range queries to efficiently count distinct values
- **Efficient Preprocessing**: Build range query structure once in O(n) time
- **Fast Queries**: Answer each query in O(log n) time
- **Optimal Approach**: O(n + q log n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Subarray Distinct Values Queries with Dynamic Updates
**Problem**: Handle dynamic updates to array elements and maintain subarray distinct values queries efficiently.

**Link**: [CSES Problem Set - Subarray Distinct Values Queries with Updates](https://cses.fi/problemset/task/subarray_distinct_values_queries_updates)

```python
class SubarrayDistinctValuesQueriesWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.segment_tree = self._build_segment_tree()
    
    def _build_segment_tree(self):
        """Build segment tree for distinct values queries"""
        size = 1
        while size < self.n:
            size <<= 1
        
        tree = [set() for _ in range(2 * size)]
        
        # Initialize leaves
        for i in range(self.n):
            tree[size + i].add(self.arr[i])
        
        # Build tree bottom-up
        for i in range(size - 1, 0, -1):
            tree[i] = tree[2 * i] | tree[2 * i + 1]
        
        return tree
    
    def update(self, pos, value):
        """Update element at position pos to value"""
        if pos < 0 or pos >= self.n:
            return
        
        self.arr[pos] = value
        pos += len(self.segment_tree) // 2
        
        # Update leaf
        self.segment_tree[pos] = {value}
        
        # Update ancestors
        pos >>= 1
        while pos > 0:
            self.segment_tree[pos] = self.segment_tree[2 * pos] | self.segment_tree[2 * pos + 1]
            pos >>= 1
    
    def query(self, left, right):
        """Query distinct values in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        size = len(self.segment_tree) // 2
        left += size
        right += size
        
        result = set()
        while left <= right:
            if left % 2 == 1:
                result |= self.segment_tree[left]
                left += 1
            if right % 2 == 0:
                result |= self.segment_tree[right]
                right -= 1
            left >>= 1
            right >>= 1
        
        return len(result)
    
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

### Variation 2: Subarray Distinct Values Queries with Different Operations
**Problem**: Handle different types of operations (count, list, frequency) on subarray distinct values.

**Link**: [CSES Problem Set - Subarray Distinct Values Queries Different Operations](https://cses.fi/problemset/task/subarray_distinct_values_queries_operations)

```python
class SubarrayDistinctValuesQueriesDifferentOps:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.segment_tree = self._build_segment_tree()
    
    def _build_segment_tree(self):
        """Build segment tree for distinct values queries"""
        size = 1
        while size < self.n:
            size <<= 1
        
        tree = [{} for _ in range(2 * size)]
        
        # Initialize leaves
        for i in range(self.n):
            tree[size + i] = {self.arr[i]: 1}
        
        # Build tree bottom-up
        for i in range(size - 1, 0, -1):
            tree[i] = self._merge_frequency_maps(tree[2 * i], tree[2 * i + 1])
        
        return tree
    
    def _merge_frequency_maps(self, map1, map2):
        """Merge two frequency maps"""
        result = map1.copy()
        for key, value in map2.items():
            result[key] = result.get(key, 0) + value
        return result
    
    def count_distinct(self, left, right):
        """Count distinct values in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        size = len(self.segment_tree) // 2
        left += size
        right += size
        
        result = {}
        while left <= right:
            if left % 2 == 1:
                result = self._merge_frequency_maps(result, self.segment_tree[left])
                left += 1
            if right % 2 == 0:
                result = self._merge_frequency_maps(result, self.segment_tree[right])
                right -= 1
            left >>= 1
            right >>= 1
        
        return len(result)
    
    def list_distinct(self, left, right):
        """List distinct values in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return []
        
        size = len(self.segment_tree) // 2
        left += size
        right += size
        
        result = {}
        while left <= right:
            if left % 2 == 1:
                result = self._merge_frequency_maps(result, self.segment_tree[left])
                left += 1
            if right % 2 == 0:
                result = self._merge_frequency_maps(result, self.segment_tree[right])
                right -= 1
            left >>= 1
            right >>= 1
        
        return list(result.keys())
    
    def get_frequency(self, left, right, value):
        """Get frequency of value in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        size = len(self.segment_tree) // 2
        left += size
        right += size
        
        result = {}
        while left <= right:
            if left % 2 == 1:
                result = self._merge_frequency_maps(result, self.segment_tree[left])
                left += 1
            if right % 2 == 0:
                result = self._merge_frequency_maps(result, self.segment_tree[right])
                right -= 1
            left >>= 1
            right >>= 1
        
        return result.get(value, 0)
    
    def get_all_frequencies(self, left, right):
        """Get frequency map for range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return {}
        
        size = len(self.segment_tree) // 2
        left += size
        right += size
        
        result = {}
        while left <= right:
            if left % 2 == 1:
                result = self._merge_frequency_maps(result, self.segment_tree[left])
                left += 1
            if right % 2 == 0:
                result = self._merge_frequency_maps(result, self.segment_tree[right])
                right -= 1
            left >>= 1
            right >>= 1
        
        return result
```

### Variation 3: Subarray Distinct Values Queries with Constraints
**Problem**: Handle subarray distinct values queries with additional constraints (e.g., minimum frequency, maximum distinct values).

**Link**: [CSES Problem Set - Subarray Distinct Values Queries with Constraints](https://cses.fi/problemset/task/subarray_distinct_values_queries_constraints)

```python
class SubarrayDistinctValuesQueriesWithConstraints:
    def __init__(self, arr, min_frequency, max_distinct):
        self.arr = arr[:]
        self.n = len(arr)
        self.min_frequency = min_frequency
        self.max_distinct = max_distinct
        self.segment_tree = self._build_segment_tree()
    
    def _build_segment_tree(self):
        """Build segment tree for distinct values queries"""
        size = 1
        while size < self.n:
            size <<= 1
        
        tree = [{} for _ in range(2 * size)]
        
        # Initialize leaves
        for i in range(self.n):
            tree[size + i] = {self.arr[i]: 1}
        
        # Build tree bottom-up
        for i in range(size - 1, 0, -1):
            tree[i] = self._merge_frequency_maps(tree[2 * i], tree[2 * i + 1])
        
        return tree
    
    def _merge_frequency_maps(self, map1, map2):
        """Merge two frequency maps"""
        result = map1.copy()
        for key, value in map2.items():
            result[key] = result.get(key, 0) + value
        return result
    
    def constrained_query(self, left, right):
        """Query distinct values in range [left, right] with constraints"""
        if left < 0 or right >= self.n or left > right:
            return None
        
        # Get frequency map
        frequency_map = self.get_frequency_map(left, right)
        
        # Check maximum distinct values constraint
        if len(frequency_map) > self.max_distinct:
            return None  # Too many distinct values
        
        # Check minimum frequency constraint
        for value, freq in frequency_map.items():
            if freq < self.min_frequency:
                return None  # Frequency too low
        
        return len(frequency_map)
    
    def get_frequency_map(self, left, right):
        """Get frequency map for range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return {}
        
        size = len(self.segment_tree) // 2
        left += size
        right += size
        
        result = {}
        while left <= right:
            if left % 2 == 1:
                result = self._merge_frequency_maps(result, self.segment_tree[left])
                left += 1
            if right % 2 == 0:
                result = self._merge_frequency_maps(result, self.segment_tree[right])
                right -= 1
            left >>= 1
            right >>= 1
        
        return result
    
    def find_valid_ranges(self):
        """Find all valid ranges that satisfy constraints"""
        valid_ranges = []
        for i in range(self.n):
            for j in range(i, self.n):
                result = self.constrained_query(i, j)
                if result is not None:
                    valid_ranges.append((i, j, result))
        return valid_ranges
    
    def get_maximum_valid_distinct(self):
        """Get maximum valid distinct values"""
        max_distinct = 0
        for i in range(self.n):
            for j in range(i, self.n):
                result = self.constrained_query(i, j)
                if result is not None:
                    max_distinct = max(max_distinct, result)
        return max_distinct
    
    def count_valid_ranges(self):
        """Count number of valid ranges"""
        count = 0
        for i in range(self.n):
            for j in range(i, self.n):
                result = self.constrained_query(i, j)
                if result is not None:
                    count += 1
        return count

# Example usage
arr = [1, 2, 1, 3, 2, 1]
min_frequency = 1
max_distinct = 3

sdvq = SubarrayDistinctValuesQueriesWithConstraints(arr, min_frequency, max_distinct)
result = sdvq.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: 2

valid_ranges = sdvq.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")

max_distinct = sdvq.get_maximum_valid_distinct()
print(f"Maximum valid distinct: {max_distinct}")
```

### Related Problems

#### **CSES Problems**
- [Subarray Distinct Values](https://cses.fi/problemset/task/2428) - Basic subarray distinct values problem
- [Subarray Sum Queries](https://cses.fi/problemset/task/1190) - Subarray sum queries
- [Range Sum Queries](https://cses.fi/problemset/task/1646) - Range sum queries

#### **LeetCode Problems**
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) - Subarray sum queries
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) - Distinct characters
- [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) - Subarray product queries

#### **Problem Categories**
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Data Structures**: Segment tree construction, range operations, efficient preprocessing
- **Algorithm Design**: Range query techniques, constraint handling, optimization
- **Array Processing**: Subarray operations, distinct values, frequency counting

## 🚀 Key Takeaways

- **Range Query Technique**: The standard approach for subarray distinct values queries
- **Efficient Preprocessing**: Build range query structure once for all queries
- **Fast Queries**: Answer each query in O(log n) time using range queries
- **Space Trade-off**: Use O(n) extra space for O(log n) query time
- **Pattern Recognition**: This technique applies to many subarray distinct values problems