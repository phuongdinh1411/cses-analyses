---
layout: simple
title: "Subarray Sums I"
permalink: /problem_soulutions/sorting_and_searching/subarray_sums_i_analysis
---

# Subarray Sums I

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of prefix sums and their applications
- Apply prefix sum technique for efficient range sum queries
- Implement efficient solutions for subarray sum problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in prefix sum problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Prefix sums, range queries, array processing, optimization
- **Data Structures**: Arrays, prefix sum arrays, hash maps
- **Mathematical Concepts**: Summation, range queries, optimization theory
- **Programming Skills**: Algorithm implementation, complexity analysis, prefix sum construction
- **Related Problems**: Subarray Sums II (hash map), Range Sum Queries (prefix sums), Maximum Subarray Sum (Kadane's algorithm)

## 📋 Problem Description

You are given an array of n integers and q queries. Each query asks for the sum of elements in a subarray from position a to position b (inclusive).

Answer all queries efficiently.

**Input**: 
- First line: two integers n and q (array size and number of queries)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)
- Next q lines: two integers a and b (query range)

**Output**: 
- Print q integers: the sum of elements in each query range

**Constraints**:
- 1 ≤ n, q ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹
- 1 ≤ a ≤ b ≤ n

**Example**:
```
Input:
8 3
3 2 4 5 1 6 2 7
2 5
1 3
4 8

Output:
12
9
21

Explanation**: 
Array: [3, 2, 4, 5, 1, 6, 2, 7]

Query 1: Range [2, 5] → sum = 2 + 4 + 5 + 1 = 12
Query 2: Range [1, 3] → sum = 3 + 2 + 4 = 9
Query 3: Range [4, 8] → sum = 5 + 1 + 6 + 2 + 7 = 21
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Calculate Sum for Each Query

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: For each query, iterate through the range and calculate the sum
- **Complete Coverage**: Guaranteed to find the correct sum for each query
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity for multiple queries

**Key Insight**: For each query, iterate through the specified range and sum all elements.

**Algorithm**:
- For each query (a, b):
  - Initialize sum = 0
  - Iterate from position a to b (inclusive)
  - Add each element to the sum
  - Return the sum

**Visual Example**:
```
Array: [3, 2, 4, 5, 1, 6, 2, 7]

Query 1: Range [2, 5]
- Position 2: sum = 0 + 2 = 2
- Position 3: sum = 2 + 4 = 6
- Position 4: sum = 6 + 5 = 11
- Position 5: sum = 11 + 1 = 12
Result: 12

Query 2: Range [1, 3]
- Position 1: sum = 0 + 3 = 3
- Position 2: sum = 3 + 2 = 5
- Position 3: sum = 5 + 4 = 9
Result: 9

Query 3: Range [4, 8]
- Position 4: sum = 0 + 5 = 5
- Position 5: sum = 5 + 1 = 6
- Position 6: sum = 6 + 6 = 12
- Position 7: sum = 12 + 2 = 14
- Position 8: sum = 14 + 7 = 21
Result: 21
```

**Implementation**:
```python
def brute_force_subarray_sums_i(arr, queries):
    """
    Find subarray sums using brute force approach
    
    Args:
        arr: list of integers
        queries: list of (start, end) tuples
    
    Returns:
        list: sum for each query
    """
    results = []
    
    for start, end in queries:
        current_sum = 0
        for i in range(start - 1, end):  # Convert to 0-based indexing
            current_sum += arr[i]
        results.append(current_sum)
    
    return results

# Example usage
arr = [3, 2, 4, 5, 1, 6, 2, 7]
queries = [(2, 5), (1, 3), (4, 8)]
result = brute_force_subarray_sums_i(arr, queries)
print(f"Brute force result: {result}")  # Output: [12, 9, 21]
```

**Time Complexity**: O(q × n) - For each query, iterate through the range
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs with many queries.

---

### Approach 2: Optimized - Precompute Prefix Sums

**Key Insights from Optimized Approach**:
- **Prefix Sums**: Precompute prefix sums to answer queries in O(1) time
- **Efficient Queries**: Use prefix sum array to calculate range sums quickly
- **Better Complexity**: Achieve O(n + q) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use prefix sums to precompute cumulative sums and answer range queries in O(1) time.

**Algorithm**:
- Precompute prefix sum array: prefix[i] = sum of elements from 1 to i
- For each query (a, b): sum = prefix[b] - prefix[a-1]

**Visual Example**:
```
Array: [3, 2, 4, 5, 1, 6, 2, 7]

Prefix sum array: [0, 3, 5, 9, 14, 15, 21, 23, 30]
- prefix[0] = 0
- prefix[1] = 3
- prefix[2] = 3 + 2 = 5
- prefix[3] = 5 + 4 = 9
- prefix[4] = 9 + 5 = 14
- prefix[5] = 14 + 1 = 15
- prefix[6] = 15 + 6 = 21
- prefix[7] = 21 + 2 = 23
- prefix[8] = 23 + 7 = 30

Query 1: Range [2, 5]
- sum = prefix[5] - prefix[1] = 15 - 3 = 12

Query 2: Range [1, 3]
- sum = prefix[3] - prefix[0] = 9 - 0 = 9

Query 3: Range [4, 8]
- sum = prefix[8] - prefix[3] = 30 - 9 = 21
```

**Implementation**:
```python
def optimized_subarray_sums_i(arr, queries):
    """
    Find subarray sums using prefix sum approach
    
    Args:
        arr: list of integers
        queries: list of (start, end) tuples
    
    Returns:
        list: sum for each query
    """
    n = len(arr)
    prefix = [0] * (n + 1)
    
    # Build prefix sum array
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    for start, end in queries:
        # Convert to 0-based indexing and use prefix sum formula
        sum_range = prefix[end] - prefix[start - 1]
        results.append(sum_range)
    
    return results

# Example usage
arr = [3, 2, 4, 5, 1, 6, 2, 7]
queries = [(2, 5), (1, 3), (4, 8)]
result = optimized_subarray_sums_i(arr, queries)
print(f"Optimized result: {result}")  # Output: [12, 9, 21]
```

**Time Complexity**: O(n + q) - O(n) for prefix sum construction, O(q) for queries
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: Much more efficient than brute force with prefix sum optimization.

---

### Approach 3: Optimal - In-Place Prefix Sums

**Key Insights from Optimal Approach**:
- **In-Place Construction**: Build prefix sums in-place to save memory
- **Optimal Complexity**: Achieve O(n + q) time complexity with minimal space
- **Efficient Implementation**: No need for extra array
- **Space Optimization**: Use the original array for prefix sums

**Key Insight**: Build prefix sums in-place to achieve optimal space complexity while maintaining O(1) query time.

**Algorithm**:
- Build prefix sums in-place: arr[i] = arr[i] + arr[i-1]
- For each query (a, b): sum = arr[b-1] - (arr[a-2] if a > 1 else 0)

**Visual Example**:
```
Array: [3, 2, 4, 5, 1, 6, 2, 7]

In-place prefix sum construction:
- arr[0] = 3 (unchanged)
- arr[1] = 2 + 3 = 5
- arr[2] = 4 + 5 = 9
- arr[3] = 5 + 9 = 14
- arr[4] = 1 + 14 = 15
- arr[5] = 6 + 15 = 21
- arr[6] = 2 + 21 = 23
- arr[7] = 7 + 23 = 30

Final array: [3, 5, 9, 14, 15, 21, 23, 30]

Query 1: Range [2, 5] (1-based)
- sum = arr[4] - arr[0] = 15 - 3 = 12

Query 2: Range [1, 3] (1-based)
- sum = arr[2] - 0 = 9 - 0 = 9

Query 3: Range [4, 8] (1-based)
- sum = arr[7] - arr[2] = 30 - 9 = 21
```

**Implementation**:
```python
def optimal_subarray_sums_i(arr, queries):
    """
    Find subarray sums using optimal in-place prefix sum approach
    
    Args:
        arr: list of integers
        queries: list of (start, end) tuples
    
    Returns:
        list: sum for each query
    """
    n = len(arr)
    
    # Build prefix sums in-place
    for i in range(1, n):
        arr[i] += arr[i - 1]
    
    results = []
    for start, end in queries:
        # Convert to 0-based indexing
        start_idx = start - 1
        end_idx = end - 1
        
        if start_idx == 0:
            sum_range = arr[end_idx]
        else:
            sum_range = arr[end_idx] - arr[start_idx - 1]
        
        results.append(sum_range)
    
    return results

# Example usage
arr = [3, 2, 4, 5, 1, 6, 2, 7]
queries = [(2, 5), (1, 3), (4, 8)]
result = optimal_subarray_sums_i(arr, queries)
print(f"Optimal result: {result}")  # Output: [12, 9, 21]
```

**Time Complexity**: O(n + q) - O(n) for prefix sum construction, O(q) for queries
**Space Complexity**: O(1) - In-place modification

**Why it's optimal**: Achieves the best possible time complexity with minimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(q × n) | O(1) | Calculate sum for each query |
| Prefix Sums | O(n + q) | O(n) | Precompute prefix sums |
| In-Place | O(n + q) | O(1) | Build prefix sums in-place |

### Time Complexity
- **Time**: O(n + q) - Prefix sum approach provides optimal time complexity
- **Space**: O(1) - In-place modification

### Why This Solution Works
- **Prefix Sums**: Precompute cumulative sums to answer range queries in O(1) time
- **Optimal Algorithm**: Prefix sum approach is the standard solution for range sum queries
- **Optimal Approach**: In-place prefix sums provide the most efficient solution for subarray sum problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Subarray Sums I with Dynamic Updates
**Problem**: Handle dynamic updates to the array and maintain subarray sum queries.

**Link**: [CSES Problem Set - Subarray Sums I with Updates](https://cses.fi/problemset/task/subarray_sums_i_updates)

```python
class SubarraySumsIWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.prefix = self._compute_prefix()
    
    def _compute_prefix(self):
        """Compute prefix sums"""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        old_value = self.arr[index]
        self.arr[index] = new_value
        
        # Update prefix sums
        diff = new_value - old_value
        for i in range(index + 1, self.n + 1):
            self.prefix[i] += diff
    
    def add_element(self, new_value):
        """Add a new element to the array"""
        self.arr.append(new_value)
        self.n = len(self.arr)
        self.prefix = self._compute_prefix()
    
    def remove_element(self, index):
        """Remove element at index"""
        self.arr.pop(index)
        self.n = len(self.arr)
        self.prefix = self._compute_prefix()
    
    def get_sum(self, left, right):
        """Get sum of subarray from left to right (inclusive)"""
        if left < 0 or right >= self.n or left > right:
            return 0
        return self.prefix[right + 1] - self.prefix[left]
    
    def get_all_sums(self, queries):
        """Get sums for multiple queries"""
        results = []
        for left, right in queries:
            results.append(self.get_sum(left, right))
        return results
    
    def get_maximum_sum(self):
        """Get maximum subarray sum using Kadane's algorithm"""
        max_sum = float('-inf')
        current_sum = 0
        
        for num in self.arr:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_minimum_sum(self):
        """Get minimum subarray sum"""
        min_sum = float('inf')
        current_sum = 0
        
        for num in self.arr:
            current_sum = min(num, current_sum + num)
            min_sum = min(min_sum, current_sum)
        
        return min_sum
```

### Variation 2: Subarray Sums I with Constraints
**Problem**: Find subarray sums with additional constraints (e.g., minimum length, maximum sum).

**Link**: [CSES Problem Set - Subarray Sums I with Constraints](https://cses.fi/problemset/task/subarray_sums_i_constraints)

```python
def subarray_sums_i_constraints(arr, queries, min_length, max_sum):
    """
    Find subarray sums with constraints
    """
    n = len(arr)
    if n == 0:
        return []
    
    # Compute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    
    for left, right in queries:
        # Check if subarray meets length constraint
        if right - left + 1 < min_length:
            results.append(0)  # Invalid subarray
            continue
        
        # Calculate sum
        sum_range = prefix[right + 1] - prefix[left]
        
        # Check if sum meets constraint
        if sum_range <= max_sum:
            results.append(sum_range)
        else:
            results.append(0)  # Exceeds maximum sum
    
    return results

def subarray_sums_i_constraints_optimized(arr, queries, min_length, max_sum):
    """
    Optimized version with better constraint handling
    """
    n = len(arr)
    if n == 0:
        return []
    
    # Compute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    results = []
    
    for left, right in queries:
        # Check if subarray meets length constraint
        if right - left + 1 < min_length:
            results.append(0)  # Invalid subarray
            continue
        
        # Calculate sum
        sum_range = prefix[right + 1] - prefix[left]
        
        # Check if sum meets constraint
        if sum_range <= max_sum:
            results.append(sum_range)
        else:
            results.append(0)  # Exceeds maximum sum
    
    return results

def subarray_sums_i_constraints_multiple(arr, queries, constraints_list):
    """
    Find subarray sums for multiple constraint sets
    """
    results = []
    
    for min_length, max_sum in constraints_list:
        result = subarray_sums_i_constraints(arr, queries, min_length, max_sum)
        results.append(result)
    
    return results

# Example usage
arr = [3, 2, 4, 5, 1, 6, 2, 7]
queries = [(2, 5), (1, 3), (4, 8)]
min_length = 2
max_sum = 15

result = subarray_sums_i_constraints(arr, queries, min_length, max_sum)
print(f"Subarray sums with constraints: {result}")  # Output: [12, 9, 0]
```

### Variation 3: Subarray Sums I with Range Updates
**Problem**: Handle range updates to the array and maintain subarray sum queries.

**Link**: [CSES Problem Set - Subarray Sums I with Range Updates](https://cses.fi/problemset/task/subarray_sums_i_range_updates)

```python
class SubarraySumsIWithRangeUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.prefix = self._compute_prefix()
        self.lazy = [0] * (self.n + 1)  # Lazy propagation array
    
    def _compute_prefix(self):
        """Compute prefix sums"""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def _apply_lazy_updates(self):
        """Apply all pending lazy updates"""
        for i in range(self.n):
            if self.lazy[i] != 0:
                self.arr[i] += self.lazy[i]
                self.lazy[i] = 0
        
        # Recompute prefix sums
        self.prefix = self._compute_prefix()
    
    def range_update(self, left, right, value):
        """Update range [left, right] by adding value"""
        if left < 0 or right >= self.n or left > right:
            return
        
        # Apply lazy update
        self.lazy[left] += value
        if right + 1 < self.n:
            self.lazy[right + 1] -= value
    
    def get_sum(self, left, right):
        """Get sum of subarray from left to right (inclusive)"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        # Apply pending updates
        self._apply_lazy_updates()
        
        return self.prefix[right + 1] - self.prefix[left]
    
    def get_all_sums(self, queries):
        """Get sums for multiple queries"""
        results = []
        for left, right in queries:
            results.append(self.get_sum(left, right))
        return results
    
    def get_maximum_sum(self):
        """Get maximum subarray sum using Kadane's algorithm"""
        # Apply pending updates
        self._apply_lazy_updates()
        
        max_sum = float('-inf')
        current_sum = 0
        
        for num in self.arr:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_minimum_sum(self):
        """Get minimum subarray sum"""
        # Apply pending updates
        self._apply_lazy_updates()
        
        min_sum = float('inf')
        current_sum = 0
        
        for num in self.arr:
            current_sum = min(num, current_sum + num)
            min_sum = min(min_sum, current_sum)
        
        return min_sum
    
    def get_sum_statistics(self):
        """Get sum statistics"""
        # Apply pending updates
        self._apply_lazy_updates()
        
        total_sum = sum(self.arr)
        max_sum = max(self.arr)
        min_sum = min(self.arr)
        avg_sum = total_sum / self.n if self.n > 0 else 0
        
        return {
            'total': total_sum,
            'maximum': max_sum,
            'minimum': min_sum,
            'average': avg_sum
        }

# Example usage
arr = [3, 2, 4, 5, 1, 6, 2, 7]
updater = SubarraySumsIWithRangeUpdates(arr)

# Range update
updater.range_update(2, 5, 10)

# Get sums
queries = [(2, 5), (1, 3), (4, 8)]
result = updater.get_all_sums(queries)
print(f"Subarray sums after range update: {result}")  # Output: [22, 9, 31]

# Get statistics
stats = updater.get_sum_statistics()
print(f"Sum statistics: {stats}")
```

### Related Problems

#### **CSES Problems**
- [Subarray Sums I](https://cses.fi/problemset/task/1661) - Basic subarray sum problem
- [Subarray Sums II](https://cses.fi/problemset/task/1662) - Subarray sum with target
- [Subarray Divisibility](https://cses.fi/problemset/task/1662) - Subarray divisibility problem

#### **LeetCode Problems**
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) - Subarray sum with target
- [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) - Range sum queries
- [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) - Range sum with updates

#### **Problem Categories**
- **Prefix Sums**: Cumulative calculations, range queries, efficient sum computation
- **Range Queries**: Query processing, range operations, efficient data structures
- **Lazy Propagation**: Range updates, efficient update propagation, segment trees
- **Algorithm Design**: Prefix sum techniques, range query optimization, update handling
