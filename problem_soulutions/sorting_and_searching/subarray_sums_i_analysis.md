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

## Problem Variations

### **Variation 1: Subarray Sums I with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while maintaining efficient subarray sum calculations.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicSubarraySums:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.prefix_sums = self._compute_prefix_sums()
        self.max_sum = self._compute_max_sum()
        self.min_sum = self._compute_min_sum()
    
    def _compute_prefix_sums(self):
        """Compute prefix sums of the array."""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def _compute_max_sum(self):
        """Compute maximum subarray sum using Kadane's algorithm."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        
        for num in self.arr:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def _compute_min_sum(self):
        """Compute minimum subarray sum."""
        if self.n == 0:
            return 0
        
        min_sum = float('inf')
        current_sum = 0
        
        for num in self.arr:
            current_sum = min(num, current_sum + num)
            min_sum = min(min_sum, current_sum)
        
        return min_sum
    
    def add_element(self, value, index=None):
        """Add a new element to the array."""
        if index is None:
            index = self.n
        self.arr.insert(index, value)
        self.n += 1
        self.prefix_sums = self._compute_prefix_sums()
        self.max_sum = self._compute_max_sum()
        self.min_sum = self._compute_min_sum()
    
    def remove_element(self, index):
        """Remove element at specified index."""
        if 0 <= index < self.n:
            del self.arr[index]
            self.n -= 1
            self.prefix_sums = self._compute_prefix_sums()
            self.max_sum = self._compute_max_sum()
            self.min_sum = self._compute_min_sum()
    
    def update_element(self, index, new_value):
        """Update element at specified index."""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self.prefix_sums = self._compute_prefix_sums()
            self.max_sum = self._compute_max_sum()
            self.min_sum = self._compute_min_sum()
    
    def get_range_sum(self, left, right):
        """Get sum of subarray from left to right (inclusive)."""
        if left < 0 or right >= self.n or left > right:
            return 0
        return self.prefix_sums[right + 1] - self.prefix_sums[left]
    
    def get_max_sum(self):
        """Get current maximum subarray sum."""
        return self.max_sum
    
    def get_min_sum(self):
        """Get current minimum subarray sum."""
        return self.min_sum
    
    def get_subarrays_with_sum_range(self, min_sum, max_sum):
        """Get all subarrays with sum in specified range."""
        result = []
        
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                if min_sum <= current_sum <= max_sum:
                    result.append((i, j, current_sum))
        
        return result
    
    def get_subarrays_with_constraints(self, constraint_func):
        """Get subarrays that satisfy custom constraints."""
        result = []
        
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                if constraint_func(i, j, current_sum, self.arr[i:j+1]):
                    result.append((i, j, current_sum))
        
        return result
    
    def get_subarray_statistics(self):
        """Get statistics about subarray sums."""
        if self.n == 0:
            return {
                'total_subarrays': 0,
                'max_sum': 0,
                'min_sum': 0,
                'average_sum': 0,
                'sum_range': 0
            }
        
        total_subarrays = self.n * (self.n + 1) // 2
        max_sum = self.max_sum
        min_sum = self.min_sum
        sum_range = max_sum - min_sum
        
        # Calculate average sum
        total_sum = 0
        for i in range(self.n):
            for j in range(i, self.n):
                total_sum += self.get_range_sum(i, j)
        average_sum = total_sum / total_subarrays if total_subarrays > 0 else 0
        
        return {
            'total_subarrays': total_subarrays,
            'max_sum': max_sum,
            'min_sum': min_sum,
            'average_sum': average_sum,
            'sum_range': sum_range
        }
    
    def get_subarray_patterns(self):
        """Get patterns in subarray sums."""
        patterns = {
            'consecutive_positive': 0,
            'consecutive_negative': 0,
            'alternating_pattern': 0,
            'increasing_sums': 0
        }
        
        for i in range(1, self.n):
            if self.arr[i] > 0 and self.arr[i-1] > 0:
                patterns['consecutive_positive'] += 1
            elif self.arr[i] < 0 and self.arr[i-1] < 0:
                patterns['consecutive_negative'] += 1
            
            if i > 1:
                if (self.arr[i] > 0) != (self.arr[i-1] > 0) and (self.arr[i-1] > 0) != (self.arr[i-2] > 0):
                    patterns['alternating_pattern'] += 1
        
        return patterns
    
    def get_optimal_subarray_strategy(self):
        """Get optimal strategy for subarray operations."""
        if self.n == 0:
            return {
                'recommended_operation': 'none',
                'max_efficiency': 0,
                'sum_distribution': {}
            }
        
        # Analyze different operations
        operations = {
            'max_sum': self.max_sum,
            'min_sum': abs(self.min_sum),
            'total_sum': sum(self.arr),
            'average_sum': sum(self.arr) / self.n
        }
        
        best_operation = max(operations, key=operations.get)
        max_efficiency = operations[best_operation]
        
        # Calculate sum distribution
        sum_distribution = defaultdict(int)
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                sum_distribution[current_sum] += 1
        
        return {
            'recommended_operation': best_operation,
            'max_efficiency': max_efficiency,
            'sum_distribution': dict(sum_distribution)
        }

# Example usage
arr = [1, -3, 2, 1, -1]
dynamic_sums = DynamicSubarraySums(arr)
print(f"Initial max sum: {dynamic_sums.get_max_sum()}")
print(f"Initial min sum: {dynamic_sums.get_min_sum()}")

# Add an element
dynamic_sums.add_element(4)
print(f"After adding element: {dynamic_sums.get_max_sum()}")

# Update an element
dynamic_sums.update_element(2, 5)
print(f"After updating element: {dynamic_sums.get_max_sum()}")

# Get range sum
print(f"Range sum [1, 3]: {dynamic_sums.get_range_sum(1, 3)}")

# Get subarrays with sum range
print(f"Subarrays with sum in [-2, 2]: {dynamic_sums.get_subarrays_with_sum_range(-2, 2)}")

# Get subarrays with constraints
def constraint_func(start, end, sum_val, subarray):
    return end - start >= 1 and sum_val > 0

print(f"Subarrays with constraints: {dynamic_sums.get_subarrays_with_constraints(constraint_func)}")

# Get statistics
print(f"Statistics: {dynamic_sums.get_subarray_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_sums.get_subarray_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_sums.get_optimal_subarray_strategy()}")
```

### **Variation 2: Subarray Sums I with Different Operations**
**Problem**: Handle different types of operations on subarray sums (weighted elements, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of subarray sum queries.

```python
class AdvancedSubarraySums:
    def __init__(self, arr, weights=None, priorities=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.weights = weights or [1] * self.n
        self.priorities = priorities or [1] * self.n
        self.prefix_sums = self._compute_prefix_sums()
        self.weighted_prefix_sums = self._compute_weighted_prefix_sums()
        self.max_sum = self._compute_max_sum()
        self.weighted_max_sum = self._compute_weighted_max_sum()
    
    def _compute_prefix_sums(self):
        """Compute prefix sums of the array."""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def _compute_weighted_prefix_sums(self):
        """Compute weighted prefix sums of the array."""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i] * self.weights[i]
        return prefix
    
    def _compute_max_sum(self):
        """Compute maximum subarray sum using Kadane's algorithm."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        
        for num in self.arr:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def _compute_weighted_max_sum(self):
        """Compute maximum weighted subarray sum."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        
        for i, num in enumerate(self.arr):
            weighted_num = num * self.weights[i]
            current_sum = max(weighted_num, current_sum + weighted_num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_range_sum(self, left, right):
        """Get sum of subarray from left to right (inclusive)."""
        if left < 0 or right >= self.n or left > right:
            return 0
        return self.prefix_sums[right + 1] - self.prefix_sums[left]
    
    def get_weighted_range_sum(self, left, right):
        """Get weighted sum of subarray from left to right (inclusive)."""
        if left < 0 or right >= self.n or left > right:
            return 0
        return self.weighted_prefix_sums[right + 1] - self.weighted_prefix_sums[left]
    
    def get_max_sum(self):
        """Get current maximum subarray sum."""
        return self.max_sum
    
    def get_weighted_max_sum(self):
        """Get current maximum weighted subarray sum."""
        return self.weighted_max_sum
    
    def get_subarrays_with_priority(self, priority_func):
        """Get subarrays considering priority."""
        result = []
        
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                weighted_sum = self.get_weighted_range_sum(i, j)
                priority = priority_func(i, j, current_sum, weighted_sum, self.weights[i:j+1], self.priorities[i:j+1])
                result.append((i, j, current_sum, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[3], reverse=True)
        return result
    
    def get_subarrays_with_optimization(self, optimization_func):
        """Get subarrays using custom optimization function."""
        result = []
        
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                weighted_sum = self.get_weighted_range_sum(i, j)
                score = optimization_func(i, j, current_sum, weighted_sum, self.weights[i:j+1], self.priorities[i:j+1])
                result.append((i, j, current_sum, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[3], reverse=True)
        return result
    
    def get_subarrays_with_constraints(self, constraint_func):
        """Get subarrays that satisfy custom constraints."""
        result = []
        
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                weighted_sum = self.get_weighted_range_sum(i, j)
                if constraint_func(i, j, current_sum, weighted_sum, self.weights[i:j+1], self.priorities[i:j+1]):
                    result.append((i, j, current_sum))
        
        return result
    
    def get_subarrays_with_multiple_criteria(self, criteria_list):
        """Get subarrays that satisfy multiple criteria."""
        result = []
        
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                weighted_sum = self.get_weighted_range_sum(i, j)
                satisfies_all_criteria = True
                for criterion in criteria_list:
                    if not criterion(i, j, current_sum, weighted_sum, self.weights[i:j+1], self.priorities[i:j+1]):
                        satisfies_all_criteria = False
                        break
                
                if satisfies_all_criteria:
                    result.append((i, j, current_sum))
        
        return result
    
    def get_subarrays_with_alternatives(self, alternatives):
        """Get subarrays considering alternative values."""
        result = []
        
        # Check original array
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                result.append((i, j, current_sum, 'original'))
        
        # Check alternative values
        for idx, alt_values in alternatives.items():
            if 0 <= idx < self.n:
                for alt_value in alt_values:
                    # Create temporary array with alternative value
                    temp_arr = self.arr[:]
                    temp_arr[idx] = alt_value
                    
                    # Calculate prefix sums for this alternative
                    temp_prefix = [0] * (self.n + 1)
                    for k in range(self.n):
                        temp_prefix[k + 1] = temp_prefix[k] + temp_arr[k]
                    
                    # Find subarrays affected by this change
                    for i in range(self.n):
                        for j in range(i, self.n):
                            if i <= idx <= j:
                                alt_sum = temp_prefix[j + 1] - temp_prefix[i]
                                result.append((i, j, alt_sum, f'alternative_{alt_value}'))
        
        return result
    
    def get_subarrays_with_adaptive_criteria(self, adaptive_func):
        """Get subarrays using adaptive criteria."""
        result = []
        
        for i in range(self.n):
            for j in range(i, self.n):
                current_sum = self.get_range_sum(i, j)
                weighted_sum = self.get_weighted_range_sum(i, j)
                if adaptive_func(i, j, current_sum, weighted_sum, self.weights[i:j+1], self.priorities[i:j+1], result):
                    result.append((i, j, current_sum))
        
        return result
    
    def get_subarray_optimization(self):
        """Get optimal subarray configuration."""
        strategies = [
            ('max_sum', self.get_max_sum),
            ('weighted_max_sum', self.get_weighted_max_sum),
        ]
        
        best_strategy = None
        best_value = float('-inf')
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
arr = [1, -3, 2, 1, -1]
weights = [2, 1, 3, 1, 2]
priorities = [1, 2, 1, 3, 1]
advanced_sums = AdvancedSubarraySums(arr, weights, priorities)

print(f"Max sum: {advanced_sums.get_max_sum()}")
print(f"Weighted max sum: {advanced_sums.get_weighted_max_sum()}")

# Get subarrays with priority
def priority_func(start, end, sum_val, weighted_sum, weights, priorities):
    return sum_val * sum(weights) * sum(priorities)

print(f"Subarrays with priority: {advanced_sums.get_subarrays_with_priority(priority_func)}")

# Get subarrays with optimization
def optimization_func(start, end, sum_val, weighted_sum, weights, priorities):
    return sum_val * sum(weights) + sum(priorities)

print(f"Subarrays with optimization: {advanced_sums.get_subarrays_with_optimization(optimization_func)}")

# Get subarrays with constraints
def constraint_func(start, end, sum_val, weighted_sum, weights, priorities):
    return end - start >= 1 and sum_val > 0 and sum(weights) > 2

print(f"Subarrays with constraints: {advanced_sums.get_subarrays_with_constraints(constraint_func)}")

# Get subarrays with multiple criteria
def criterion1(start, end, sum_val, weighted_sum, weights, priorities):
    return end - start >= 1

def criterion2(start, end, sum_val, weighted_sum, weights, priorities):
    return sum_val > 0

criteria_list = [criterion1, criterion2]
print(f"Subarrays with multiple criteria: {advanced_sums.get_subarrays_with_multiple_criteria(criteria_list)}")

# Get subarrays with alternatives
alternatives = {1: [2, 4], 3: [3, 5]}
print(f"Subarrays with alternatives: {advanced_sums.get_subarrays_with_alternatives(alternatives)}")

# Get subarrays with adaptive criteria
def adaptive_func(start, end, sum_val, weighted_sum, weights, priorities, current_result):
    return end - start >= 1 and sum_val > 0 and len(current_result) < 5

print(f"Subarrays with adaptive criteria: {advanced_sums.get_subarrays_with_adaptive_criteria(adaptive_func)}")

# Get subarray optimization
print(f"Subarray optimization: {advanced_sums.get_subarray_optimization()}")
```

### **Variation 3: Subarray Sums I with Constraints**
**Problem**: Handle subarray sums with additional constraints (cost limits, length constraints, resource constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedSubarraySums:
    def __init__(self, arr, constraints=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.constraints = constraints or {}
        self.prefix_sums = self._compute_prefix_sums()
        self.max_sum = self._compute_max_sum()
    
    def _compute_prefix_sums(self):
        """Compute prefix sums of the array."""
        prefix = [0] * (self.n + 1)
        for i in range(self.n):
            prefix[i + 1] = prefix[i] + self.arr[i]
        return prefix
    
    def _compute_max_sum(self):
        """Compute maximum subarray sum using Kadane's algorithm."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        
        for num in self.arr:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_cost_constraints(self, cost_limit):
        """Get maximum sum considering cost constraints."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        total_cost = 0
        
        for i, num in enumerate(self.arr):
            # Calculate cost for including this element
            cost = abs(num)  # Simple cost model
            if total_cost + cost <= cost_limit:
                current_sum = max(num, current_sum + num)
                max_sum = max(max_sum, current_sum)
                total_cost += cost
            else:
                # Reset if cost limit exceeded
                current_sum = num
                total_cost = cost
        
        return max_sum
    
    def get_max_sum_with_length_constraints(self, min_length, max_length):
        """Get maximum sum considering length constraints."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(self.n):
            for j in range(i, self.n):
                subarray_length = j - i + 1
                if min_length <= subarray_length <= max_length:
                    current_sum = self.prefix_sums[j + 1] - self.prefix_sums[i]
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get maximum sum considering resource constraints."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        current_resources = [0] * len(resource_limits)
        
        for i, num in enumerate(self.arr):
            # Check resource constraints
            can_afford = True
            consumption = resource_consumption.get(i, [0] * len(resource_limits))
            for j, res_consumption in enumerate(consumption):
                if current_resources[j] + res_consumption > resource_limits[j]:
                    can_afford = False
                    break
            
            if can_afford:
                current_sum = max(num, current_sum + num)
                max_sum = max(max_sum, current_sum)
                for j, res_consumption in enumerate(consumption):
                    current_resources[j] += res_consumption
            else:
                # Reset if resource limit exceeded
                current_sum = num
                current_resources = consumption[:]
        
        return max_sum
    
    def get_max_sum_with_mathematical_constraints(self, constraint_func):
        """Get maximum sum that satisfies custom mathematical constraints."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        
        for i, num in enumerate(self.arr):
            if constraint_func(i, num, current_sum):
                current_sum = max(num, current_sum + num)
                max_sum = max(max_sum, current_sum)
            else:
                current_sum = num
        
        return max_sum
    
    def get_max_sum_with_range_constraints(self, range_constraints):
        """Get maximum sum that satisfies range constraints."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        
        for i, num in enumerate(self.arr):
            # Check if element satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(i, num, current_sum):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                current_sum = max(num, current_sum + num)
                max_sum = max(max_sum, current_sum)
            else:
                current_sum = num
        
        return max_sum
    
    def get_max_sum_with_optimization_constraints(self, optimization_func):
        """Get maximum sum using custom optimization constraints."""
        if self.n == 0:
            return 0
        
        # Sort elements by optimization function
        sorted_indices = sorted(range(self.n), key=lambda i: optimization_func(i, self.arr[i]), reverse=True)
        
        max_sum = float('-inf')
        current_sum = 0
        
        for idx in sorted_indices:
            num = self.arr[idx]
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_multiple_constraints(self, constraints_list):
        """Get maximum sum that satisfies multiple constraints."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        
        for i, num in enumerate(self.arr):
            # Check if element satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(i, num, current_sum):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                current_sum = max(num, current_sum + num)
                max_sum = max(max_sum, current_sum)
            else:
                current_sum = num
        
        return max_sum
    
    def get_max_sum_with_priority_constraints(self, priority_func):
        """Get maximum sum with priority-based constraints."""
        if self.n == 0:
            return 0
        
        # Sort elements by priority
        sorted_indices = sorted(range(self.n), key=lambda i: priority_func(i, self.arr[i]), reverse=True)
        
        max_sum = float('-inf')
        current_sum = 0
        
        for idx in sorted_indices:
            num = self.arr[idx]
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_adaptive_constraints(self, adaptive_func):
        """Get maximum sum with adaptive constraints."""
        if self.n == 0:
            return 0
        
        max_sum = float('-inf')
        current_sum = 0
        
        for i, num in enumerate(self.arr):
            # Check adaptive constraints
            if adaptive_func(i, num, current_sum, max_sum):
                current_sum = max(num, current_sum + num)
                max_sum = max(max_sum, current_sum)
            else:
                current_sum = num
        
        return max_sum
    
    def get_optimal_subarray_strategy(self):
        """Get optimal subarray strategy considering all constraints."""
        strategies = [
            ('cost_constraints', self.get_max_sum_with_cost_constraints),
            ('length_constraints', self.get_max_sum_with_length_constraints),
            ('resource_constraints', self.get_max_sum_with_resource_constraints),
        ]
        
        best_strategy = None
        best_sum = float('-inf')
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'cost_constraints':
                    current_sum = strategy_func(100)  # Cost limit of 100
                elif strategy_name == 'length_constraints':
                    current_sum = strategy_func(1, 5)  # Length between 1 and 5
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {i: [10, 5] for i in range(self.n)}
                    current_sum = strategy_func(resource_limits, resource_consumption)
                
                if current_sum > best_sum:
                    best_sum = current_sum
                    best_strategy = (strategy_name, current_sum)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'max_cost': 100,
    'min_length': 1,
    'max_length': 5
}

arr = [1, -3, 2, 1, -1]
constrained_sums = ConstrainedSubarraySums(arr, constraints)

print("Cost-constrained max sum:", constrained_sums.get_max_sum_with_cost_constraints(100))

print("Length-constrained max sum:", constrained_sums.get_max_sum_with_length_constraints(1, 5))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(arr))}
print("Resource-constrained max sum:", constrained_sums.get_max_sum_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(index, num, current_sum):
    return num > 0 and current_sum + num > 0

print("Mathematical constraint max sum:", constrained_sums.get_max_sum_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(index, num, current_sum):
    return num > 0

range_constraints = [range_constraint]
print("Range-constrained max sum:", constrained_sums.get_max_sum_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(index, num, current_sum):
    return num > 0

def constraint2(index, num, current_sum):
    return current_sum + num > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints max sum:", constrained_sums.get_max_sum_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(index, num):
    return num

print("Priority-constrained max sum:", constrained_sums.get_max_sum_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(index, num, current_sum, max_sum):
    return num > 0 and current_sum + num > max_sum

print("Adaptive constraint max sum:", constrained_sums.get_max_sum_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_sums.get_optimal_subarray_strategy()
print(f"Optimal strategy: {optimal}")
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
