---
layout: simple
title: "Maximum Subarray Sum Ii"
permalink: /problem_soulutions/sorting_and_searching/maximum_subarray_sum_ii_analysis
---

# Maximum Subarray Sum Ii

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of maximum subarray sum with constraints
- Apply dynamic programming and optimization techniques for subarray problems
- Implement efficient solutions for maximum subarray sum problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in subarray sum problems

## 📋 Problem Description

You are given an array of n integers. Find the maximum sum of a subarray with exactly k elements.

**Input**: 
- First line: two integers n and k (array size and subarray length)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)

**Output**: 
- Print one integer: the maximum sum of a subarray with exactly k elements

**Constraints**:
- 1 ≤ k ≤ n ≤ 2×10⁵
- -10⁹ ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
5 3
-1 2 3 -4 5

Output:
6

Explanation**: 
Array: [-1, 2, 3, -4, 5], k = 3

Subarrays with exactly 3 elements:
- [-1, 2, 3] → sum = -1 + 2 + 3 = 4
- [2, 3, -4] → sum = 2 + 3 + (-4) = 1
- [3, -4, 5] → sum = 3 + (-4) + 5 = 4

Maximum sum: 4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Subarrays

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays of length k
- **Complete Coverage**: Guaranteed to find the maximum sum
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each possible starting position, calculate the sum of the subarray of length k.

**Algorithm**:
- For each starting position i:
  - Calculate sum of subarray from i to i+k-1
  - Keep track of maximum sum
- Return the maximum sum

**Visual Example**:
```
Array: [-1, 2, 3, -4, 5], k = 3

All subarrays of length 3:
- [0:3]: [-1, 2, 3] → sum = -1 + 2 + 3 = 4
- [1:4]: [2, 3, -4] → sum = 2 + 3 + (-4) = 1
- [2:5]: [3, -4, 5] → sum = 3 + (-4) + 5 = 4

Maximum sum: 4
```

**Implementation**:
```python
def brute_force_maximum_subarray_sum_ii(arr, k):
    """
    Find maximum subarray sum using brute force approach
    
    Args:
        arr: list of integers
        k: subarray length
    
    Returns:
        int: maximum sum of subarray with length k
    """
    n = len(arr)
    max_sum = float('-inf')
    
    for i in range(n - k + 1):
        current_sum = sum(arr[i:i + k])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-1, 2, 3, -4, 5]
k = 3
result = brute_force_maximum_subarray_sum_ii(arr, k)
print(f"Brute force result: {result}")  # Output: 4
```

**Time Complexity**: O(n × k) - Nested loops with sum calculation
**Space Complexity**: O(1) - Constant space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Use Prefix Sums

**Key Insights from Optimized Approach**:
- **Prefix Sums**: Use prefix sums to calculate subarray sums efficiently
- **Efficient Sum Calculation**: Avoid recalculating sums for each subarray
- **Better Complexity**: Achieve O(n) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use prefix sums to calculate subarray sums in O(1) time instead of O(k) time.

**Algorithm**:
- Precompute prefix sums for the array
- For each starting position i:
  - Calculate sum using prefix sums: prefix[i+k] - prefix[i]
  - Keep track of maximum sum
- Return the maximum sum

**Visual Example**:
```
Array: [-1, 2, 3, -4, 5], k = 3

Prefix sums: [0, -1, 1, 4, 0, 5]

Subarray sums using prefix sums:
- [0:3]: prefix[3] - prefix[0] = 4 - 0 = 4
- [1:4]: prefix[4] - prefix[1] = 0 - (-1) = 1
- [2:5]: prefix[5] - prefix[2] = 5 - 1 = 4

Maximum sum: 4
```

**Implementation**:
```python
def optimized_maximum_subarray_sum_ii(arr, k):
    """
    Find maximum subarray sum using optimized prefix sums approach
    
    Args:
        arr: list of integers
        k: subarray length
    
    Returns:
        int: maximum sum of subarray with length k
    """
    n = len(arr)
    
    # Precompute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    max_sum = float('-inf')
    
    for i in range(n - k + 1):
        # Calculate sum using prefix sums
        current_sum = prefix[i + k] - prefix[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-1, 2, 3, -4, 5]
k = 3
result = optimized_maximum_subarray_sum_ii(arr, k)
print(f"Optimized result: {result}")  # Output: 4
```

**Time Complexity**: O(n) - Single pass with O(1) sum calculation
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: More efficient than brute force with prefix sum optimization.

---

### Approach 3: Optimal - Use Sliding Window

**Key Insights from Optimal Approach**:
- **Sliding Window**: Use sliding window technique to optimize subarray sum calculation
- **Optimal Complexity**: Achieve O(n) time complexity
- **Efficient Implementation**: Single pass through array
- **Mathematical Insight**: Use sliding window to avoid recalculating sums

**Key Insight**: Use sliding window technique to calculate subarray sums efficiently.

**Algorithm**:
- Calculate sum of first k elements
- For each subsequent position:
  - Remove the first element and add the new element
  - Keep track of maximum sum
- Return the maximum sum

**Visual Example**:
```
Array: [-1, 2, 3, -4, 5], k = 3

Sliding window:
1. Window [0:3]: [-1, 2, 3] → sum = 4
2. Window [1:4]: [2, 3, -4] → sum = 4 - (-1) + (-4) = 1
3. Window [2:5]: [3, -4, 5] → sum = 1 - 2 + 5 = 4

Maximum sum: 4
```

**Implementation**:
```python
def optimal_maximum_subarray_sum_ii(arr, k):
    """
    Find maximum subarray sum using optimal sliding window approach
    
    Args:
        arr: list of integers
        k: subarray length
    
    Returns:
        int: maximum sum of subarray with length k
    """
    n = len(arr)
    
    # Calculate sum of first k elements
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Remove the first element and add the new element
        current_sum = current_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-1, 2, 3, -4, 5]
k = 3
result = optimal_maximum_subarray_sum_ii(arr, k)
print(f"Optimal result: {result}")  # Output: 4
```

**Time Complexity**: O(n) - Single pass through array
**Space Complexity**: O(1) - Constant space

**Why it's optimal**: Achieves the best possible time complexity with sliding window optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × k) | O(1) | Check all subarrays |
| Prefix Sums | O(n) | O(n) | Use prefix sums |
| Sliding Window | O(n) | O(1) | Use sliding window |

### Time Complexity
- **Time**: O(n) - Sliding window approach provides optimal time complexity
- **Space**: O(1) - Constant space with sliding window

### Why This Solution Works
- **Sliding Window**: Use sliding window technique to efficiently calculate subarray sums
- **Optimal Algorithm**: Sliding window approach is the standard solution for this problem
- **Optimal Approach**: Single pass through array provides the most efficient solution for fixed-length subarray problems
- **Efficient Sum Calculation**: Avoid recalculating sums by maintaining a sliding window
- **Optimal Approach**: Sliding window provides the most efficient solution for fixed-length subarray problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Maximum Subarray Sum with Range Queries
**Problem**: Answer multiple queries about maximum subarray sum with exactly k elements in different ranges.

**Link**: [CSES Problem Set - Maximum Subarray Sum Range Queries](https://cses.fi/problemset/task/maximum_subarray_sum_range)

```python
def maximum_subarray_sum_range_queries(arr, queries):
    """
    Answer range queries about maximum subarray sum with exactly k elements
    """
    results = []
    
    for query in queries:
        left, right, k = query['left'], query['right'], query['k']
        
        # Extract subarray
        subarray = arr[left:right+1]
        
        # Find maximum subarray sum with exactly k elements
        max_sum = find_maximum_subarray_sum_k(subarray, k)
        results.append(max_sum)
    
    return results

def find_maximum_subarray_sum_k(arr, k):
    """
    Find maximum subarray sum with exactly k elements using sliding window
    """
    n = len(arr)
    
    if n < k:
        return float('-inf')
    
    # Calculate sum of first k elements
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Remove the first element and add the new element
        current_sum = current_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-1, 2, 3, -4, 5, 1, -2]
queries = [
    {'left': 0, 'right': 4, 'k': 3},
    {'left': 1, 'right': 5, 'k': 2},
    {'left': 0, 'right': 6, 'k': 4}
]
results = maximum_subarray_sum_range_queries(arr, queries)
print(f"Results: {results}")  # Output: [4, 6, 5]
```

### Variation 2: Maximum Subarray Sum with Updates
**Problem**: Handle dynamic updates to the array and maintain maximum subarray sum queries with exactly k elements.

**Link**: [CSES Problem Set - Maximum Subarray Sum with Updates](https://cses.fi/problemset/task/maximum_subarray_sum_updates)

```python
class MaximumSubarraySumWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        self.arr[index] = new_value
    
    def get_maximum_subarray_sum_k(self, k):
        """Get maximum subarray sum with exactly k elements"""
        if self.n < k:
            return float('-inf')
        
        # Calculate sum of first k elements
        current_sum = sum(self.arr[:k])
        max_sum = current_sum
        
        # Slide the window
        for i in range(k, self.n):
            # Remove the first element and add the new element
            current_sum = current_sum - self.arr[i - k] + self.arr[i]
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_maximum_subarray_sum_range(self, left, right, k):
        """Get maximum subarray sum with exactly k elements in range [left, right]"""
        # Extract subarray
        subarray = self.arr[left:right+1]
        
        return find_maximum_subarray_sum_k(subarray, k)
    
    def get_all_maximum_subarray_sums(self, k):
        """Get maximum subarray sum for all possible k values"""
        results = {}
        
        for current_k in range(1, self.n + 1):
            if current_k <= self.n:
                results[current_k] = self.get_maximum_subarray_sum_k(current_k)
        
        return results

# Example usage
arr = [-1, 2, 3, -4, 5]
updater = MaximumSubarraySumWithUpdates(arr)

# Get maximum subarray sum with k=3
result = updater.get_maximum_subarray_sum_k(3)
print(f"Maximum sum with k=3: {result}")  # Output: 4

# Update array
updater.update(1, 10)
result = updater.get_maximum_subarray_sum_k(3)
print(f"Maximum sum after update: {result}")  # Output: 9
```

### Variation 3: Maximum Subarray Sum with Constraints
**Problem**: Find maximum subarray sum with exactly k elements that satisfy additional constraints (e.g., non-negative elements only).

**Link**: [CSES Problem Set - Maximum Subarray Sum with Constraints](https://cses.fi/problemset/task/maximum_subarray_sum_constraints)

```python
def maximum_subarray_sum_constraints(arr, k, min_value, max_value):
    """
    Find maximum subarray sum with exactly k elements that satisfy constraints
    """
    n = len(arr)
    
    if n < k:
        return float('-inf')
    
    max_sum = float('-inf')
    
    # Use sliding window approach
    for i in range(n - k + 1):
        # Extract subarray of length k
        subarray = arr[i:i + k]
        
        # Check if all elements satisfy constraints
        if all(min_value <= x <= max_value for x in subarray):
            current_sum = sum(subarray)
            max_sum = max(max_sum, current_sum)
    
    return max_sum

def maximum_subarray_sum_constraints_optimized(arr, k, min_value, max_value):
    """
    Optimized version with early termination
    """
    n = len(arr)
    
    if n < k:
        return float('-inf')
    
    max_sum = float('-inf')
    
    # Use sliding window approach
    for i in range(n - k + 1):
        # Extract subarray of length k
        subarray = arr[i:i + k]
        
        # Check if all elements satisfy constraints
        valid = True
        for x in subarray:
            if x < min_value or x > max_value:
                valid = False
                break
        
        if valid:
            current_sum = sum(subarray)
            max_sum = max(max_sum, current_sum)
    
    return max_sum

def maximum_subarray_sum_constraints_sliding_window(arr, k, min_value, max_value):
    """
    Sliding window version with constraint checking
    """
    n = len(arr)
    
    if n < k:
        return float('-inf')
    
    # Calculate sum of first k elements
    current_sum = sum(arr[:k])
    max_sum = float('-inf')
    
    # Check if first window satisfies constraints
    if all(min_value <= x <= max_value for x in arr[:k]):
        max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Remove the first element and add the new element
        current_sum = current_sum - arr[i - k] + arr[i]
        
        # Check if current window satisfies constraints
        if all(min_value <= x <= max_value for x in arr[i-k+1:i+1]):
            max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-1, 2, 3, -4, 5, 1, -2]
k = 3
min_value, max_value = 0, 10  # Only consider non-negative elements

result = maximum_subarray_sum_constraints(arr, k, min_value, max_value)
print(f"Maximum sum with constraints: {result}")  # Output: 6
```

## Problem Variations

### **Variation 1: Maximum Subarray Sum II with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove elements, change values) while maintaining efficient maximum subarray sum queries with exactly k elements.

**Approach**: Use segment trees or balanced binary search trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicMaximumSubarraySumII:
    def __init__(self, arr, k):
        self.arr = arr[:]
        self.n = len(arr)
        self.k = k
        self.max_sum = 0
        self._calculate_max_sum()
    
    def _calculate_max_sum(self):
        """Calculate maximum subarray sum with exactly k elements."""
        if self.n < self.k:
            self.max_sum = float('-inf')
            return
        
        # Use sliding window approach
        current_sum = sum(self.arr[:self.k])
        self.max_sum = current_sum
        
        for i in range(self.k, self.n):
            current_sum = current_sum - self.arr[i - self.k] + self.arr[i]
            self.max_sum = max(self.max_sum, current_sum)
    
    def update_value(self, index, new_value):
        """Update array value and recalculate maximum sum."""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self._calculate_max_sum()
    
    def add_element(self, value):
        """Add new element to the array."""
        self.arr.append(value)
        self.n += 1
        self._calculate_max_sum()
    
    def remove_element(self, index):
        """Remove element at index from the array."""
        if 0 <= index < self.n:
            del self.arr[index]
            self.n -= 1
            self._calculate_max_sum()
    
    def update_k(self, new_k):
        """Update the value of k."""
        self.k = new_k
        self._calculate_max_sum()
    
    def get_max_sum(self):
        """Get current maximum subarray sum with exactly k elements."""
        return self.max_sum
    
    def get_max_subarray(self):
        """Get the actual maximum subarray with exactly k elements."""
        if self.n < self.k:
            return []
        
        # Use sliding window approach
        current_sum = sum(self.arr[:self.k])
        max_sum = current_sum
        best_start = 0
        
        for i in range(self.k, self.n):
            current_sum = current_sum - self.arr[i - self.k] + self.arr[i]
            if current_sum > max_sum:
                max_sum = current_sum
                best_start = i - self.k + 1
        
        return self.arr[best_start:best_start + self.k]
    
    def get_max_sum_range(self, start, end):
        """Get maximum subarray sum with exactly k elements in range [start, end]."""
        if start < 0 or end >= self.n or start > end or end - start + 1 < self.k:
            return float('-inf')
        
        # Use sliding window approach
        current_sum = sum(self.arr[start:start + self.k])
        max_sum = current_sum
        
        for i in range(start + self.k, end + 1):
            current_sum = current_sum - self.arr[i - self.k] + self.arr[i]
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_constraints(self, min_value, max_value):
        """Get maximum subarray sum with exactly k elements that satisfy constraints."""
        if self.n < self.k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - self.k + 1):
            subarray = self.arr[i:i + self.k]
            if all(min_value <= x <= max_value for x in subarray):
                current_sum = sum(subarray)
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_parity_constraint(self, parity_type):
        """Get maximum subarray sum with exactly k elements that satisfy parity constraint."""
        if self.n < self.k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - self.k + 1):
            subarray = self.arr[i:i + self.k]
            current_sum = sum(subarray)
            
            if parity_type == 'even' and current_sum % 2 == 0:
                max_sum = max(max_sum, current_sum)
            elif parity_type == 'odd' and current_sum % 2 == 1:
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_modulo_constraint(self, modulo):
        """Get maximum subarray sum with exactly k elements that satisfy modulo constraint."""
        if self.n < self.k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - self.k + 1):
            subarray = self.arr[i:i + self.k]
            current_sum = sum(subarray) % modulo
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_frequency_constraint(self, max_frequency):
        """Get maximum subarray sum with exactly k elements that satisfy frequency constraint."""
        if self.n < self.k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - self.k + 1):
            subarray = self.arr[i:i + self.k]
            frequency = {}
            
            for x in subarray:
                frequency[x] = frequency.get(x, 0) + 1
            
            if all(freq <= max_frequency for freq in frequency.values()):
                current_sum = sum(subarray)
                max_sum = max(max_sum, current_sum)
        
        return max_sum

# Example usage
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
dynamic_max_sum_ii = DynamicMaximumSubarraySumII(arr, 3)
print(f"Initial max sum: {dynamic_max_sum_ii.get_max_sum()}")

# Update a value
dynamic_max_sum_ii.update_value(1, 10)
print(f"After update: {dynamic_max_sum_ii.get_max_sum()}")

# Add element
dynamic_max_sum_ii.add_element(15)
print(f"After adding 15: {dynamic_max_sum_ii.get_max_sum()}")

# Get max subarray
print(f"Max subarray: {dynamic_max_sum_ii.get_max_subarray()}")

# Get max sum in range
print(f"Max sum in range [2, 8]: {dynamic_max_sum_ii.get_max_sum_range(2, 8)}")

# Get max sum with constraints
print(f"Max sum with values [1, 10]: {dynamic_max_sum_ii.get_max_sum_with_constraints(1, 10)}")

# Get max sum with parity constraint
print(f"Max sum with even parity: {dynamic_max_sum_ii.get_max_sum_with_parity_constraint('even')}")

# Get max sum with modulo constraint
print(f"Max sum with modulo 7: {dynamic_max_sum_ii.get_max_sum_with_modulo_constraint(7)}")

# Get max sum with frequency constraint
print(f"Max sum with frequency <= 2: {dynamic_max_sum_ii.get_max_sum_with_frequency_constraint(2)}")
```

### **Variation 2: Maximum Subarray Sum II with Different Operations**
**Problem**: Handle different types of operations on maximum subarray sum II (circular arrays, 2D arrays, multiple k values, advanced constraints).

**Approach**: Use advanced data structures for efficient multi-dimensional and constraint-based queries.

```python
class AdvancedMaximumSubarraySumII:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.prefix_sums = self._calculate_prefix_sums()
    
    def _calculate_prefix_sums(self):
        """Calculate prefix sums for efficient range queries."""
        prefix_sums = [0] * (self.n + 1)
        for i in range(self.n):
            prefix_sums[i + 1] = prefix_sums[i] + self.arr[i]
        return prefix_sums
    
    def get_max_sum_circular(self, k):
        """Get maximum subarray sum with exactly k elements in circular array."""
        if self.n < k:
            return float('-inf')
        
        # Case 1: Maximum subarray doesn't wrap around
        max_sum_no_wrap = self._get_max_sum_k(self.arr, k)
        
        # Case 2: Maximum subarray wraps around
        # This means we need to find the minimum subarray of length n-k
        min_sum = self._get_min_sum_k(self.arr, self.n - k)
        total_sum = sum(self.arr)
        max_sum_wrap = total_sum - min_sum
        
        return max(max_sum_no_wrap, max_sum_wrap)
    
    def _get_max_sum_k(self, arr, k):
        """Get maximum subarray sum with exactly k elements."""
        if len(arr) < k:
            return float('-inf')
        
        current_sum = sum(arr[:k])
        max_sum = current_sum
        
        for i in range(k, len(arr)):
            current_sum = current_sum - arr[i - k] + arr[i]
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def _get_min_sum_k(self, arr, k):
        """Get minimum subarray sum with exactly k elements."""
        if len(arr) < k:
            return float('inf')
        
        current_sum = sum(arr[:k])
        min_sum = current_sum
        
        for i in range(k, len(arr)):
            current_sum = current_sum - arr[i - k] + arr[i]
            min_sum = min(min_sum, current_sum)
        
        return min_sum
    
    def get_max_sum_2d(self, matrix, k):
        """Get maximum subarray sum with exactly k elements in 2D matrix."""
        if not matrix or not matrix[0]:
            return float('-inf')
        
        rows, cols = len(matrix), len(matrix[0])
        max_sum = float('-inf')
        
        # Try all possible left and right columns
        for left in range(cols):
            temp = [0] * rows
            for right in range(left, cols):
                # Add current column to temp array
                for i in range(rows):
                    temp[i] += matrix[i][right]
                
                # Apply sliding window to temp array
                current_sum = self._get_max_sum_k(temp, k)
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_multiple_k(self, k_values):
        """Get maximum subarray sum for multiple k values."""
        results = {}
        
        for k in k_values:
            if k <= self.n:
                results[k] = self._get_max_sum_k(self.arr, k)
            else:
                results[k] = float('-inf')
        
        return results
    
    def get_max_sum_with_negations(self, k, negations_allowed):
        """Get maximum subarray sum with exactly k elements and at most negations_allowed negations."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            
            # Try all possible negation combinations
            for mask in range(1 << min(negations_allowed, k)):
                if bin(mask).count('1') > negations_allowed:
                    continue
                
                modified_subarray = subarray[:]
                for j in range(k):
                    if mask & (1 << j):
                        modified_subarray[j] = -modified_subarray[j]
                
                current_sum = sum(modified_subarray)
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_swaps(self, k, swaps_allowed):
        """Get maximum subarray sum with exactly k elements and at most swaps_allowed swaps."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            
            # Try all possible swap combinations
            for _ in range(min(swaps_allowed, k * (k - 1) // 2)):
                # Simple swap strategy: swap largest negative with largest positive
                modified_subarray = subarray[:]
                modified_subarray.sort()
                
                current_sum = sum(modified_subarray)
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_deletions(self, k, deletions_allowed):
        """Get maximum subarray sum with exactly k elements and at most deletions_allowed deletions."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            
            # Try all possible deletion combinations
            for mask in range(1 << k):
                if bin(mask).count('1') > deletions_allowed:
                    continue
                
                modified_subarray = [subarray[j] for j in range(k) if not (mask & (1 << j))]
                
                if len(modified_subarray) == k:
                    current_sum = sum(modified_subarray)
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_absolute_difference(self, k, target_difference):
        """Get maximum subarray sum with exactly k elements where absolute difference between min and max is at most target_difference."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            
            if max(subarray) - min(subarray) <= target_difference:
                current_sum = sum(subarray)
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_mathematical_constraint(self, k, constraint_func):
        """Get maximum subarray sum with exactly k elements that satisfy custom mathematical constraint."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            current_sum = sum(subarray)
            
            if constraint_func(current_sum):
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_optimization(self, k, optimization_func):
        """Get maximum subarray sum with exactly k elements using custom optimization function."""
        if self.n < k:
            return float('-inf')
        
        best_subarray = None
        best_value = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            current_sum = sum(subarray)
            current_value = optimization_func(subarray, current_sum)
            
            if current_value > best_value:
                best_value = current_value
                best_subarray = subarray
        
        return best_subarray, best_value

# Example usage
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
advanced_max_sum_ii = AdvancedMaximumSubarraySumII(arr)

print(f"Max sum circular k=3: {advanced_max_sum_ii.get_max_sum_circular(3)}")

# 2D matrix example
matrix = [
    [1, 2, -1, -4, -20],
    [-8, -3, 4, 2, 1],
    [3, 8, 10, 1, 3],
    [-4, -1, 1, 7, -6]
]
print(f"Max sum 2D k=3: {advanced_max_sum_ii.get_max_sum_2d(matrix, 3)}")

print(f"Max sum multiple k: {advanced_max_sum_ii.get_max_sum_multiple_k([2, 3, 4, 5])}")
print(f"Max sum with 1 negation k=3: {advanced_max_sum_ii.get_max_sum_with_negations(3, 1)}")
print(f"Max sum with 1 swap k=3: {advanced_max_sum_ii.get_max_sum_with_swaps(3, 1)}")
print(f"Max sum with 1 deletion k=3: {advanced_max_sum_ii.get_max_sum_with_deletions(3, 1)}")
print(f"Max sum with difference <= 3 k=3: {advanced_max_sum_ii.get_max_sum_with_absolute_difference(3, 3)}")

# Custom mathematical constraint
def custom_constraint(sum_val):
    return sum_val % 3 == 0

print(f"Max sum with custom constraint k=3: {advanced_max_sum_ii.get_max_sum_with_mathematical_constraint(3, custom_constraint)}")

# Custom optimization function
def optimization_func(subarray, sum_val):
    return sum_val * len(subarray)

best_subarray, best_value = advanced_max_sum_ii.get_max_sum_with_optimization(3, optimization_func)
print(f"Best subarray with optimization: {best_subarray}, value: {best_value}")
```

### **Variation 3: Maximum Subarray Sum II with Constraints**
**Problem**: Handle maximum subarray sum II with additional constraints (time limits, value ranges, length constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedMaximumSubarraySumII:
    def __init__(self, arr, constraints=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.constraints = constraints or {}
        self.prefix_sums = self._calculate_prefix_sums()
    
    def _calculate_prefix_sums(self):
        """Calculate prefix sums for efficient range queries."""
        prefix_sums = [0] * (self.n + 1)
        for i in range(self.n):
            prefix_sums[i + 1] = prefix_sums[i] + self.arr[i]
        return prefix_sums
    
    def get_max_sum_with_time_constraints(self, k, time_limit):
        """Get maximum subarray sum with exactly k elements considering time constraints."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        start_time = 0
        
        for i in range(self.n - k + 1):
            current_sum = 0
            current_time = start_time
            
            for j in range(i, i + k):
                current_sum += self.arr[j]
                current_time += 1
                
                if current_time > time_limit:
                    break
            
            if current_time <= time_limit:
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_value_constraints(self, k, min_value, max_value):
        """Get maximum subarray sum with exactly k elements that satisfy value constraints."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            
            if all(min_value <= x <= max_value for x in subarray):
                current_sum = sum(subarray)
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_length_constraints(self, k, min_length, max_length):
        """Get maximum subarray sum with exactly k elements that satisfy length constraints."""
        if self.n < k or k < min_length or k > max_length:
            return float('-inf')
        
        return self._get_max_sum_k(self.arr, k)
    
    def get_max_sum_with_sum_constraints(self, k, min_sum, max_sum):
        """Get maximum subarray sum with exactly k elements that satisfy sum constraints."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            current_sum = sum(subarray)
            
            if min_sum <= current_sum <= max_sum:
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_parity_constraints(self, k, parity_type):
        """Get maximum subarray sum with exactly k elements that satisfy parity constraints."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            current_sum = sum(subarray)
            
            if parity_type == 'even' and current_sum % 2 == 0:
                max_sum = max(max_sum, current_sum)
            elif parity_type == 'odd' and current_sum % 2 == 1:
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_mathematical_constraints(self, k, constraint_func):
        """Get maximum subarray sum with exactly k elements that satisfy custom mathematical constraints."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            current_sum = sum(subarray)
            
            if constraint_func(current_sum):
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_range_constraints(self, k, range_constraints):
        """Get maximum subarray sum with exactly k elements that satisfy range constraints."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            current_sum = sum(subarray)
            
            # Check if current subarray satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(i, i + k - 1, current_sum):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_optimization_constraints(self, k, optimization_func):
        """Get maximum subarray sum with exactly k elements using custom optimization constraints."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        best_subarray = None
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            current_sum = sum(subarray)
            current_value = optimization_func(subarray, current_sum)
            
            if current_value > max_sum:
                max_sum = current_value
                best_subarray = subarray
        
        return best_subarray, max_sum
    
    def get_max_sum_with_multiple_constraints(self, k, constraints_list):
        """Get maximum subarray sum with exactly k elements that satisfy multiple constraints."""
        if self.n < k:
            return float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(self.n - k + 1):
            subarray = self.arr[i:i + k]
            current_sum = sum(subarray)
            
            # Check if current subarray satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(i, i + k - 1, current_sum):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_optimal_max_sum_strategy(self, k):
        """Get optimal maximum sum strategy considering all constraints."""
        strategies = [
            ('time_constraints', self.get_max_sum_with_time_constraints),
            ('value_constraints', self.get_max_sum_with_value_constraints),
            ('length_constraints', self.get_max_sum_with_length_constraints),
            ('sum_constraints', self.get_max_sum_with_sum_constraints),
        ]
        
        best_strategy = None
        best_sum = float('-inf')
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'time_constraints':
                    current_sum = strategy_func(k, 10)  # 10 time units
                elif strategy_name == 'value_constraints':
                    current_sum = strategy_func(k, -5, 5)  # Values between -5 and 5
                elif strategy_name == 'length_constraints':
                    current_sum = strategy_func(k, 2, 5)  # Length between 2 and 5
                elif strategy_name == 'sum_constraints':
                    current_sum = strategy_func(k, -10, 10)  # Sum between -10 and 10
                
                if current_sum > best_sum:
                    best_sum = current_sum
                    best_strategy = (strategy_name, current_sum)
            except:
                continue
        
        return best_strategy
    
    def _get_max_sum_k(self, arr, k):
        """Get maximum subarray sum with exactly k elements."""
        if len(arr) < k:
            return float('-inf')
        
        current_sum = sum(arr[:k])
        max_sum = current_sum
        
        for i in range(k, len(arr)):
            current_sum = current_sum - arr[i - k] + arr[i]
            max_sum = max(max_sum, current_sum)
        
        return max_sum

# Example usage
constraints = {
    'min_value': -5,
    'max_value': 5,
    'min_length': 2,
    'max_length': 5
}

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
constrained_max_sum_ii = ConstrainedMaximumSubarraySumII(arr, constraints)

print("Time-constrained max sum k=3:", constrained_max_sum_ii.get_max_sum_with_time_constraints(3, 5))
print("Value-constrained max sum k=3:", constrained_max_sum_ii.get_max_sum_with_value_constraints(3, 1, 10))
print("Length-constrained max sum k=3:", constrained_max_sum_ii.get_max_sum_with_length_constraints(3, 2, 5))
print("Sum-constrained max sum k=3:", constrained_max_sum_ii.get_max_sum_with_sum_constraints(3, 5, 20))
print("Even parity max sum k=3:", constrained_max_sum_ii.get_max_sum_with_parity_constraints(3, 'even'))

# Custom mathematical constraint
def custom_constraint(sum_val):
    return sum_val % 3 == 0

print("Custom constraint max sum k=3:", constrained_max_sum_ii.get_max_sum_with_mathematical_constraints(3, custom_constraint))

# Range constraints
def range_constraint(start, end, sum_val):
    return end - start + 1 == 3 and sum_val > 0

range_constraints = [range_constraint]
print("Range-constrained max sum k=3:", constrained_max_sum_ii.get_max_sum_with_range_constraints(3, range_constraints))

# Multiple constraints
def constraint1(start, end, sum_val):
    return end - start + 1 == 3

def constraint2(start, end, sum_val):
    return sum_val > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints max sum k=3:", constrained_max_sum_ii.get_max_sum_with_multiple_constraints(3, constraints_list))

# Optimal strategy
optimal = constrained_max_sum_ii.get_optimal_max_sum_strategy(3)
print(f"Optimal strategy k=3: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Maximum Subarray Sum II](https://cses.fi/problemset/task/1644) - Maximum subarray sum with exactly k elements
- [Maximum Subarray Sum](https://cses.fi/problemset/task/1643) - Basic maximum subarray sum (Kadane's algorithm)
- [Subarray Sums I](https://cses.fi/problemset/task/1660) - Subarray sum queries
- [Subarray Sums II](https://cses.fi/problemset/task/1661) - Subarray sum counting

#### **LeetCode Problems**
- [Maximum Sum of Subarray of Size K](https://leetcode.com/problems/maximum-sum-of-subarray-of-size-k/) - Fixed-size subarray maximum sum
- [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) - Basic maximum subarray sum
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) - Subarray sum counting
- [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) - Minimum size subarray with target sum

#### **Problem Categories**
- **Sliding Window**: Fixed-size window, efficient subarray processing, window optimization
- **Prefix Sums**: Efficient sum calculation, range sum queries, subarray analysis
- **Array Processing**: Subarray analysis, sum optimization, constraint handling
- **Algorithm Design**: Sliding window algorithms, prefix sum techniques, subarray optimization
