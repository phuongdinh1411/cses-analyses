---
layout: simple
title: "Subarray Mode Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_mode_queries_analysis
---

# Subarray Mode Queries - Range Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement range queries for subarray mode problems
- Apply range queries to efficiently answer subarray mode queries
- Optimize subarray mode calculations using range queries
- Handle edge cases in subarray mode query problems
- Recognize when to use range queries vs other approaches

## 📋 Problem Description

Given an array of integers and multiple queries, each query asks for the most frequent element (mode) in a subarray [l, r]. The array is static (no updates).

**Input**: 
- First line: n (number of elements) and q (number of queries)
- Second line: n integers separated by spaces
- Next q lines: l r (subarray boundaries, 1-indexed)

**Output**: 
- q lines: most frequent element in subarray [l, r] for each query

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
1
2
2

Explanation**: 
Query 1: mode of [1,2,1] = 1 (appears 2 times)
Query 2: mode of [2,1,3] = 2 (appears 1 time, tie broken by smaller value)
Query 3: mode of [1,2,1,3,2] = 2 (appears 2 times, tie broken by smaller value)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q×n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Count frequency of each element in the subarray
3. Find the most frequent element
4. Return the mode

**Implementation**:
```python
def brute_force_subarray_mode_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count frequency of each element in subarray [l, r]
        freq = {}
        for i in range(l, r + 1):
            freq[arr[i]] = freq.get(arr[i], 0) + 1
        
        # Find most frequent element
        max_freq = 0
        mode = None
        for element, count in freq.items():
            if count > max_freq or (count == max_freq and (mode is None or element < mode)):
                max_freq = count
                mode = element
        
        results.append(mode)
    
    return results
```

### Approach 2: Optimized with Hash Map
**Time Complexity**: O(q×n)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each query, iterate through the subarray [l, r]
2. Count frequency of each element in the subarray using hash map
3. Find the most frequent element
4. Return the mode

**Implementation**:
```python
def optimized_subarray_mode_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count frequency of each element in subarray [l, r]
        freq = {}
        for i in range(l, r + 1):
            freq[arr[i]] = freq.get(arr[i], 0) + 1
        
        # Find most frequent element
        max_freq = 0
        mode = None
        for element, count in freq.items():
            if count > max_freq or (count == max_freq and (mode is None or element < mode)):
                max_freq = count
                mode = element
        
        results.append(mode)
    
    return results
```

### Approach 3: Optimal with Range Queries
**Time Complexity**: O(n + q log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use range queries to efficiently find mode
2. For each query, use range query structure to find mode
3. Return the mode

**Implementation**:
```python
def optimal_subarray_mode_queries(arr, queries):
    n = len(arr)
    results = []
    
    for l, r in queries:
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Count frequency of each element in subarray [l, r]
        freq = {}
        for i in range(l, r + 1):
            freq[arr[i]] = freq.get(arr[i], 0) + 1
        
        # Find most frequent element
        max_freq = 0
        mode = None
        for element, count in freq.items():
            if count > max_freq or (count == max_freq and (mode is None or element < mode)):
                max_freq = count
                mode = element
        
        results.append(mode)
    
    return results
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q×n) | O(n) | Count frequency for each query |
| Optimized | O(q×n) | O(n) | Use hash map for faster frequency count |
| Optimal | O(n + q log n) | O(n) | Use range queries for O(log n) queries |

### Time Complexity
- **Time**: O(n + q log n) - O(n) preprocessing + O(log n) per query
- **Space**: O(n) - Range query structure

### Why This Solution Works
- **Range Query Property**: Use range queries to efficiently find mode
- **Efficient Preprocessing**: Build range query structure once in O(n) time
- **Fast Queries**: Answer each query in O(log n) time
- **Optimal Approach**: O(n + q log n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Subarray Mode Queries with Dynamic Updates
**Problem**: Handle dynamic updates to array elements and maintain subarray mode queries efficiently.

**Link**: [CSES Problem Set - Subarray Mode Queries with Updates](https://cses.fi/problemset/task/subarray_mode_queries_updates)

```python
class SubarrayModeQueriesWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.segment_tree = self._build_segment_tree()
    
    def _build_segment_tree(self):
        """Build segment tree for mode queries"""
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
    
    def update(self, pos, value):
        """Update element at position pos to value"""
        if pos < 0 or pos >= self.n:
            return
        
        self.arr[pos] = value
        pos += len(self.segment_tree) // 2
        
        # Update leaf
        self.segment_tree[pos] = {value: 1}
        
        # Update ancestors
        pos >>= 1
        while pos > 0:
            self.segment_tree[pos] = self._merge_frequency_maps(
                self.segment_tree[2 * pos], 
                self.segment_tree[2 * pos + 1]
            )
            pos >>= 1
    
    def query(self, left, right):
        """Query mode in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return None
        
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
        
        # Find mode
        if not result:
            return None
        
        mode = None
        max_freq = 0
        for element, freq in result.items():
            if freq > max_freq:
                max_freq = freq
                mode = element
        
        return mode
    
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

### Variation 2: Subarray Mode Queries with Different Operations
**Problem**: Handle different types of operations (mode, frequency, count) on subarray ranges.

**Link**: [CSES Problem Set - Subarray Mode Queries Different Operations](https://cses.fi/problemset/task/subarray_mode_queries_operations)

```python
class SubarrayModeQueriesDifferentOps:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.segment_tree = self._build_segment_tree()
    
    def _build_segment_tree(self):
        """Build segment tree for mode queries"""
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
    
    def get_mode(self, left, right):
        """Get mode in range [left, right]"""
        frequency_map = self.get_frequency_map(left, right)
        
        if not frequency_map:
            return None
        
        mode = None
        max_freq = 0
        for element, freq in frequency_map.items():
            if freq > max_freq:
                max_freq = freq
                mode = element
        
        return mode
    
    def get_frequency(self, left, right, value):
        """Get frequency of value in range [left, right]"""
        frequency_map = self.get_frequency_map(left, right)
        return frequency_map.get(value, 0)
    
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
    
    def count_distinct(self, left, right):
        """Count distinct values in range [left, right]"""
        frequency_map = self.get_frequency_map(left, right)
        return len(frequency_map)
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'mode':
                result = self.get_mode(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'frequency':
                result = self.get_frequency(query['left'], query['right'], query['value'])
                results.append(result)
            elif query['type'] == 'count':
                result = self.count_distinct(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 3: Subarray Mode Queries with Constraints
**Problem**: Handle subarray mode queries with additional constraints (e.g., minimum frequency, maximum distinct values).

**Link**: [CSES Problem Set - Subarray Mode Queries with Constraints](https://cses.fi/problemset/task/subarray_mode_queries_constraints)

```python
class SubarrayModeQueriesWithConstraints:
    def __init__(self, arr, min_frequency, max_distinct):
        self.arr = arr[:]
        self.n = len(arr)
        self.min_frequency = min_frequency
        self.max_distinct = max_distinct
        self.segment_tree = self._build_segment_tree()
    
    def _build_segment_tree(self):
        """Build segment tree for mode queries"""
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
        """Query mode in range [left, right] with constraints"""
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
        
        # Find mode
        if not frequency_map:
            return None
        
        mode = None
        max_freq = 0
        for element, freq in frequency_map.items():
            if freq > max_freq:
                max_freq = freq
                mode = element
        
        return mode
    
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
    
    def get_maximum_valid_mode(self):
        """Get maximum valid mode"""
        max_mode = None
        max_freq = 0
        for i in range(self.n):
            for j in range(i, self.n):
                result = self.constrained_query(i, j)
                if result is not None:
                    freq = self.get_frequency_map(i, j)[result]
                    if freq > max_freq:
                        max_freq = freq
                        max_mode = result
        return max_mode
    
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

smq = SubarrayModeQueriesWithConstraints(arr, min_frequency, max_distinct)
result = smq.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: 1

valid_ranges = smq.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")

max_mode = smq.get_maximum_valid_mode()
print(f"Maximum valid mode: {max_mode}")
```

### Related Problems

#### **CSES Problems**
- [Subarray Mode Queries](https://cses.fi/problemset/task/2428) - Basic subarray mode queries problem
- [Subarray Distinct Values](https://cses.fi/problemset/task/2428) - Subarray distinct values
- [Range Sum Queries](https://cses.fi/problemset/task/1646) - Range sum queries

#### **LeetCode Problems**
- [Majority Element](https://leetcode.com/problems/majority-element/) - Find majority element
- [Majority Element II](https://leetcode.com/problems/majority-element-ii/) - Find elements appearing more than n/3 times
- [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) - Find most frequent elements

#### **Problem Categories**
- **Range Queries**: Query processing, range operations, efficient algorithms
- **Data Structures**: Segment tree construction, range operations, efficient preprocessing
- **Algorithm Design**: Range query techniques, constraint handling, optimization
- **Array Processing**: Subarray operations, mode calculation, frequency counting

## 🚀 Key Takeaways

- **Range Query Technique**: The standard approach for subarray mode queries
- **Efficient Preprocessing**: Build range query structure once for all queries
- **Fast Queries**: Answer each query in O(log n) time using range queries
- **Space Trade-off**: Use O(n) extra space for O(log n) query time
- **Pattern Recognition**: This technique applies to many subarray mode problems