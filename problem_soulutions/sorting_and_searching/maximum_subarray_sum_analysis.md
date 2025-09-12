---
layout: simple
title: "Maximum Subarray Sum - Kadane's Algorithm"
permalink: /problem_soulutions/sorting_and_searching/maximum_subarray_sum_analysis
---

# Maximum Subarray Sum - Kadane's Algorithm

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the maximum subarray problem and its applications
- Apply Kadane's algorithm for optimal subarray sum calculation
- Implement dynamic programming techniques for optimization problems
- Optimize algorithms using local and global maximum tracking
- Handle edge cases in subarray problems (all negative numbers, single element)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, Kadane's algorithm, prefix sums, sliding window
- **Data Structures**: Arrays, prefix sum arrays
- **Mathematical Concepts**: Optimization, maximum subarray, dynamic programming principles
- **Programming Skills**: Dynamic programming implementation, array manipulation, optimization
- **Related Problems**: Sum of Two Values (optimization), Apartments (greedy), Collecting Numbers (sorting)

## 📋 Problem Description

Given an array of n integers, find the maximum sum of any contiguous subarray. The subarray must contain at least one element.

This is the classic maximum subarray problem that can be solved efficiently using Kadane's algorithm, which is a dynamic programming approach.

**Input**: 
- First line: integer n (number of elements)
- Second line: n integers (the array elements)

**Output**: 
- Print one integer: the maximum subarray sum

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- -10⁹ ≤ a_i ≤ 10⁹

**Example**:
```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
9

Explanation**: 
The maximum subarray sum is 9, achieved by the subarray [3, -2, 5, 3]:
- Subarray [3, -2, 5, 3] has sum: 3 + (-2) + 5 + 3 = 9
- This is the maximum sum among all possible contiguous subarrays
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Subarrays

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible contiguous subarrays
- **Sum Calculation**: For each subarray, calculate its sum
- **Maximum Tracking**: Keep track of the maximum sum found
- **Complete Coverage**: Guaranteed to find the optimal solution

**Key Insight**: Systematically check all possible contiguous subarrays and find the one with maximum sum.

**Algorithm**:
- Use nested loops to generate all possible subarrays
- For each subarray, calculate its sum
- Keep track of the maximum sum found

**Visual Example**:
```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]

All possible subarrays and their sums:
1. [-1]: sum = -1
2. [-1, 3]: sum = 2
3. [-1, 3, -2]: sum = 0
4. [-1, 3, -2, 5]: sum = 5
5. [-1, 3, -2, 5, 3]: sum = 8
6. [-1, 3, -2, 5, 3, -5]: sum = 3
7. [-1, 3, -2, 5, 3, -5, 2]: sum = 5
8. [-1, 3, -2, 5, 3, -5, 2, 2]: sum = 7
9. [3]: sum = 3
10. [3, -2]: sum = 1
11. [3, -2, 5]: sum = 6
12. [3, -2, 5, 3]: sum = 9 ← Maximum
... (continue for all subarrays)

Maximum sum: 9
```

**Implementation**:
```python
def brute_force_max_subarray(arr):
    """
    Find maximum subarray sum using brute force approach
    
    Args:
        arr: list of integers
    
    Returns:
        int: maximum subarray sum
    """
    n = len(arr)
    max_sum = float('-inf')
    
    # Check all possible subarrays
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-1, 3, -2, 5, 3, -5, 2, 2]
result = brute_force_max_subarray(arr)
print(f"Brute force result: {result}")  # Output: 9
```

**Time Complexity**: O(n³) - Check all subarrays and calculate sums
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Cubic time complexity makes it very slow for large inputs.

---

### Approach 2: Optimized - Prefix Sums

**Key Insights from Optimized Approach**:
- **Prefix Sum Array**: Precompute prefix sums for efficient range sum calculation
- **Range Sum Formula**: sum(i,j) = prefix[j] - prefix[i-1]
- **Efficient Calculation**: Calculate subarray sums in O(1) time
- **Reduced Complexity**: Eliminate redundant sum calculations

**Key Insight**: Use prefix sums to calculate subarray sums efficiently, reducing time complexity.

**Algorithm**:
- Compute prefix sum array
- For each possible subarray, use prefix sums to calculate sum in O(1)
- Keep track of maximum sum

**Visual Example**:
```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]

Step 1: Compute prefix sums
Prefix: [0, -1, 2, 0, 5, 8, 3, 5, 7]

Step 2: Calculate subarray sums using prefix sums
Subarray [3, -2, 5, 3] (indices 1 to 4):
sum = prefix[5] - prefix[1] = 8 - (-1) = 9

Subarray [5, 3] (indices 3 to 4):
sum = prefix[5] - prefix[3] = 8 - 0 = 8

Maximum sum: 9
```

**Implementation**:
```python
def optimized_max_subarray(arr):
    """
    Find maximum subarray sum using prefix sums
    
    Args:
        arr: list of integers
    
    Returns:
        int: maximum subarray sum
    """
    n = len(arr)
    
    # Compute prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    max_sum = float('-inf')
    
    # Check all possible subarrays
    for i in range(n):
        for j in range(i, n):
            # Calculate sum using prefix sums
            current_sum = prefix[j + 1] - prefix[i]
            max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-1, 3, -2, 5, 3, -5, 2, 2]
result = optimized_max_subarray(arr)
print(f"Optimized result: {result}")  # Output: 9
```

**Time Complexity**: O(n²) - Still check all subarrays, but sum calculation is O(1)
**Space Complexity**: O(n) - For prefix sum array

**Why it's better**: Reduced time complexity by eliminating redundant sum calculations.

---

### Approach 3: Optimal - Kadane's Algorithm

**Key Insights from Optimal Approach**:
- **Dynamic Programming**: Use DP to solve the problem optimally
- **Local vs Global Maximum**: Track both local and global maximum sums
- **Optimal Substructure**: Maximum subarray ending at position i depends on maximum subarray ending at position i-1
- **Linear Complexity**: Achieve O(n) time complexity

**Key Insight**: For each position, decide whether to extend the previous subarray or start a new one based on which gives a larger sum.

**Algorithm**:
- Initialize local and global maximum to first element
- For each subsequent element, update local maximum
- Local maximum = max(current element, local maximum + current element)
- Update global maximum if local maximum is larger

**Visual Example**:
```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]

Kadane's Algorithm:
Initial: local_max = -1, global_max = -1

1. Element 3:
   local_max = max(3, -1 + 3) = max(3, 2) = 3
   global_max = max(-1, 3) = 3

2. Element -2:
   local_max = max(-2, 3 + (-2)) = max(-2, 1) = 1
   global_max = max(3, 1) = 3

3. Element 5:
   local_max = max(5, 1 + 5) = max(5, 6) = 6
   global_max = max(3, 6) = 6

4. Element 3:
   local_max = max(3, 6 + 3) = max(3, 9) = 9
   global_max = max(6, 9) = 9

5. Element -5:
   local_max = max(-5, 9 + (-5)) = max(-5, 4) = 4
   global_max = max(9, 4) = 9

6. Element 2:
   local_max = max(2, 4 + 2) = max(2, 6) = 6
   global_max = max(9, 6) = 9

7. Element 2:
   local_max = max(2, 6 + 2) = max(2, 8) = 8
   global_max = max(9, 8) = 9

Maximum sum: 9
```

**Implementation**:
```python
def optimal_max_subarray(arr):
    """
    Find maximum subarray sum using Kadane's algorithm
    
    Args:
        arr: list of integers
    
    Returns:
        int: maximum subarray sum
    """
    if not arr:
        return 0
    
    # Initialize with first element
    local_max = global_max = arr[0]
    
    # Process remaining elements
    for i in range(1, len(arr)):
        # Decide whether to extend previous subarray or start new one
        local_max = max(arr[i], local_max + arr[i])
        global_max = max(global_max, local_max)
    
    return global_max

# Example usage
arr = [-1, 3, -2, 5, 3, -5, 2, 2]
result = optimal_max_subarray(arr)
print(f"Optimal result: {result}")  # Output: 9
```

**Time Complexity**: O(n) - Single pass through array
**Space Complexity**: O(1) - Constant extra space

**Why it's optimal**: Linear time complexity with optimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all subarrays |
| Prefix Sums | O(n²) | O(n) | Efficient range sum calculation |
| Kadane's Algorithm | O(n) | O(1) | Dynamic programming approach |

### Time Complexity
- **Time**: O(n) - Single pass through array
- **Space**: O(1) - Constant extra space

### Why This Solution Works
- **Dynamic Programming**: Optimal substructure property holds
- **Local Decision**: At each step, make optimal local decision
- **Global Tracking**: Maintain global maximum throughout the process
- **Optimal Approach**: Kadane's algorithm provides the best possible time complexity

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Maximum Subarray Sum with Constraints
**Problem**: Find maximum subarray sum with additional constraints (e.g., minimum length, maximum length).

**Link**: [CSES Problem Set - Maximum Subarray Sum with Constraints](https://cses.fi/problemset/task/maximum_subarray_sum_constraints)

```python
def maximum_subarray_sum_constraints(arr, min_length, max_length):
    """
    Find maximum subarray sum with length constraints
    """
    n = len(arr)
    max_sum = float('-inf')
    
    # Use sliding window approach
    for start in range(n):
        current_sum = 0
        for end in range(start, min(start + max_length, n)):
            current_sum += arr[end]
            
            # Check if subarray meets length requirements
            if end - start + 1 >= min_length:
                max_sum = max(max_sum, current_sum)
    
    return max_sum

def maximum_subarray_sum_constraints_optimized(arr, min_length, max_length):
    """
    Optimized version using prefix sums
    """
    n = len(arr)
    prefix_sums = [0] * (n + 1)
    
    # Calculate prefix sums
    for i in range(n):
        prefix_sums[i + 1] = prefix_sums[i] + arr[i]
    
    max_sum = float('-inf')
    
    # Check all valid subarrays
    for start in range(n):
        for end in range(start + min_length - 1, min(start + max_length, n)):
            subarray_sum = prefix_sums[end + 1] - prefix_sums[start]
            max_sum = max(max_sum, subarray_sum)
    
    return max_sum
```

### Variation 2: Maximum Subarray Sum with Updates
**Problem**: Handle dynamic updates to the array and maintain maximum subarray sum.

**Link**: [CSES Problem Set - Maximum Subarray Sum with Updates](https://cses.fi/problemset/task/maximum_subarray_sum_updates)

```python
class MaximumSubarraySumWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.max_sum = self._calculate_max_sum()
    
    def _calculate_max_sum(self):
        """Calculate maximum subarray sum using Kadane's algorithm"""
        max_ending_here = max_so_far = self.arr[0]
        
        for i in range(1, self.n):
            max_ending_here = max(self.arr[i], max_ending_here + self.arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        self.arr[index] = new_value
        self.max_sum = self._calculate_max_sum()
    
    def get_max_sum(self):
        """Get current maximum subarray sum"""
        return self.max_sum
    
    def get_max_sum_range(self, start, end):
        """Get maximum subarray sum in range [start, end]"""
        max_ending_here = max_so_far = self.arr[start]
        
        for i in range(start + 1, end + 1):
            max_ending_here = max(self.arr[i], max_ending_here + self.arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
```

### Variation 3: Maximum Subarray Sum with Circular Array
**Problem**: Find maximum subarray sum in a circular array (array is circular).

**Link**: [CSES Problem Set - Maximum Subarray Sum Circular](https://cses.fi/problemset/task/maximum_subarray_sum_circular)

```python
def maximum_subarray_sum_circular(arr):
    """
    Find maximum subarray sum in circular array
    """
    n = len(arr)
    
    # Case 1: Maximum subarray doesn't wrap around
    max_sum_no_wrap = kadane_algorithm(arr)
    
    # Case 2: Maximum subarray wraps around
    # This means the minimum subarray is in the middle
    # So max_sum = total_sum - min_sum
    
    total_sum = sum(arr)
    min_sum = kadane_algorithm([-x for x in arr])  # Find minimum subarray
    max_sum_wrap = total_sum + min_sum  # Add because we negated
    
    # Handle edge case where all elements are negative
    if max_sum_wrap == 0:
        return max_sum_no_wrap
    
    return max(max_sum_no_wrap, max_sum_wrap)

def kadane_algorithm(arr):
    """Standard Kadane's algorithm"""
    max_ending_here = max_so_far = arr[0]
    
    for i in range(1, len(arr)):
        max_ending_here = max(arr[i], max_ending_here + arr[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

def maximum_subarray_sum_circular_optimized(arr):
    """
    Optimized version for circular array
    """
    n = len(arr)
    
    # Calculate maximum subarray sum without wrapping
    max_sum_no_wrap = kadane_algorithm(arr)
    
    # Calculate total sum and minimum subarray sum
    total_sum = sum(arr)
    min_sum = kadane_algorithm([-x for x in arr])
    
    # Maximum sum with wrapping
    max_sum_wrap = total_sum + min_sum if min_sum != 0 else max_sum_no_wrap
    
    return max(max_sum_no_wrap, max_sum_wrap)
```

## Problem Variations

### **Variation 1: Maximum Subarray Sum with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove elements, change values) while maintaining efficient maximum subarray sum queries.

**Approach**: Use segment trees or balanced binary search trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicMaximumSubarraySum:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.max_sum = 0
        self._calculate_max_sum()
    
    def _calculate_max_sum(self):
        """Calculate maximum subarray sum using Kadane's algorithm."""
        if not self.arr:
            self.max_sum = 0
            return
        
        max_ending_here = max_so_far = self.arr[0]
        
        for i in range(1, len(self.arr)):
            max_ending_here = max(self.arr[i], max_ending_here + self.arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        self.max_sum = max_so_far
    
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
    
    def get_max_sum(self):
        """Get current maximum subarray sum."""
        return self.max_sum
    
    def get_max_subarray(self):
        """Get the actual maximum subarray."""
        if not self.arr:
            return []
        
        max_ending_here = max_so_far = self.arr[0]
        start = end = 0
        temp_start = 0
        
        for i in range(1, len(self.arr)):
            if max_ending_here < 0:
                max_ending_here = self.arr[i]
                temp_start = i
            else:
                max_ending_here += self.arr[i]
            
            if max_ending_here > max_so_far:
                max_so_far = max_ending_here
                start = temp_start
                end = i
        
        return self.arr[start:end+1]
    
    def get_max_sum_range(self, start, end):
        """Get maximum subarray sum in range [start, end]."""
        if start < 0 or end >= self.n or start > end:
            return 0
        
        max_ending_here = max_so_far = self.arr[start]
        
        for i in range(start + 1, end + 1):
            max_ending_here = max(self.arr[i], max_ending_here + self.arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
    
    def get_max_sum_with_length_constraint(self, min_length, max_length):
        """Get maximum subarray sum with length constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            for j in range(i, min(i + max_length, len(self.arr))):
                current_sum += self.arr[j]
                if j - i + 1 >= min_length:
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_value_constraint(self, min_value, max_value):
        """Get maximum subarray sum with value constraints."""
        if not self.arr:
            return 0
        
        # Filter array to only include values within constraints
        filtered_arr = [x for x in self.arr if min_value <= x <= max_value]
        
        if not filtered_arr:
            return 0
        
        max_ending_here = max_so_far = filtered_arr[0]
        
        for i in range(1, len(filtered_arr)):
            max_ending_here = max(filtered_arr[i], max_ending_here + filtered_arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far

# Example usage
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
dynamic_max_sum = DynamicMaximumSubarraySum(arr)
print(f"Initial max sum: {dynamic_max_sum.get_max_sum()}")

# Update a value
dynamic_max_sum.update_value(1, 5)
print(f"After update: {dynamic_max_sum.get_max_sum()}")

# Add element
dynamic_max_sum.add_element(3)
print(f"After adding 3: {dynamic_max_sum.get_max_sum()}")

# Get max subarray
print(f"Max subarray: {dynamic_max_sum.get_max_subarray()}")

# Get max sum in range
print(f"Max sum in range [2, 6]: {dynamic_max_sum.get_max_sum_range(2, 6)}")

# Get max sum with length constraint
print(f"Max sum with length [2, 4]: {dynamic_max_sum.get_max_sum_with_length_constraint(2, 4)}")

# Get max sum with value constraint
print(f"Max sum with values [-1, 5]: {dynamic_max_sum.get_max_sum_with_value_constraint(-1, 5)}")
```

### **Variation 2: Maximum Subarray Sum with Different Operations**
**Problem**: Handle different types of operations on maximum subarray sum (circular arrays, 2D arrays, multiple constraints).

**Approach**: Use advanced data structures for efficient multi-dimensional and constraint-based queries.

```python
class AdvancedMaximumSubarraySum:
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
    
    def get_max_sum_circular(self):
        """Get maximum subarray sum in circular array."""
        # Case 1: Maximum subarray doesn't wrap around
        max_sum_no_wrap = self._kadane_algorithm(self.arr)
        
        # Case 2: Maximum subarray wraps around
        # This means the minimum subarray is in the middle
        total_sum = sum(self.arr)
        min_sum = self._kadane_algorithm([-x for x in self.arr])
        max_sum_wrap = total_sum + min_sum
        
        # Handle edge case where all elements are negative
        if max_sum_wrap == 0:
            return max_sum_no_wrap
        
        return max(max_sum_no_wrap, max_sum_wrap)
    
    def _kadane_algorithm(self, arr):
        """Standard Kadane's algorithm."""
        if not arr:
            return 0
        
        max_ending_here = max_so_far = arr[0]
        
        for i in range(1, len(arr)):
            max_ending_here = max(arr[i], max_ending_here + arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
    
    def get_max_sum_2d(self, matrix):
        """Get maximum subarray sum in 2D matrix."""
        if not matrix or not matrix[0]:
            return 0
        
        rows, cols = len(matrix), len(matrix[0])
        max_sum = float('-inf')
        
        # Try all possible left and right columns
        for left in range(cols):
            temp = [0] * rows
            for right in range(left, cols):
                # Add current column to temp array
                for i in range(rows):
                    temp[i] += matrix[i][right]
                
                # Apply Kadane's algorithm to temp array
                current_sum = self._kadane_algorithm(temp)
                max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_k_negations(self, k):
        """Get maximum subarray sum with at most k negations."""
        if not self.arr:
            return 0
        
        # Use dynamic programming
        # dp[i][j] = maximum sum ending at position i with j negations
        dp = [[float('-inf')] * (k + 1) for _ in range(self.n)]
        
        # Initialize first element
        dp[0][0] = self.arr[0]
        if k > 0:
            dp[0][1] = -self.arr[0]
        
        for i in range(1, self.n):
            for j in range(k + 1):
                # Don't negate current element
                if dp[i-1][j] != float('-inf'):
                    dp[i][j] = max(self.arr[i], dp[i-1][j] + self.arr[i])
                
                # Negate current element
                if j > 0 and dp[i-1][j-1] != float('-inf'):
                    dp[i][j] = max(dp[i][j], max(-self.arr[i], dp[i-1][j-1] + (-self.arr[i])))
        
        return max(max(row) for row in dp)
    
    def get_max_sum_with_deletions(self, deletions_allowed):
        """Get maximum subarray sum with at most deletions_allowed deletions."""
        if not self.arr:
            return 0
        
        # Use dynamic programming
        # dp[i][j] = maximum sum ending at position i with j deletions
        dp = [[float('-inf')] * (deletions_allowed + 1) for _ in range(self.n)]
        
        # Initialize first element
        dp[0][0] = self.arr[0]
        if deletions_allowed > 0:
            dp[0][1] = 0  # Delete first element
        
        for i in range(1, self.n):
            for j in range(deletions_allowed + 1):
                # Don't delete current element
                if dp[i-1][j] != float('-inf'):
                    dp[i][j] = max(self.arr[i], dp[i-1][j] + self.arr[i])
                
                # Delete current element
                if j > 0 and dp[i-1][j-1] != float('-inf'):
                    dp[i][j] = max(dp[i][j], dp[i-1][j-1])
        
        return max(max(row) for row in dp)
    
    def get_max_sum_with_swaps(self, swaps_allowed):
        """Get maximum subarray sum with at most swaps_allowed swaps."""
        if not self.arr:
            return 0
        
        # Use dynamic programming
        # dp[i][j] = maximum sum ending at position i with j swaps
        dp = [[float('-inf')] * (swaps_allowed + 1) for _ in range(self.n)]
        
        # Initialize first element
        dp[0][0] = self.arr[0]
        
        for i in range(1, self.n):
            for j in range(swaps_allowed + 1):
                # Don't swap current element
                if dp[i-1][j] != float('-inf'):
                    dp[i][j] = max(self.arr[i], dp[i-1][j] + self.arr[i])
                
                # Swap current element with previous
                if j > 0 and i > 0 and dp[i-1][j-1] != float('-inf'):
                    dp[i][j] = max(dp[i][j], max(self.arr[i-1], dp[i-1][j-1] + self.arr[i-1]))
        
        return max(max(row) for row in dp)
    
    def get_max_sum_with_modulo(self, modulo):
        """Get maximum subarray sum with modulo operation."""
        if not self.arr:
            return 0
        
        # Use dynamic programming with modulo
        max_ending_here = max_so_far = self.arr[0] % modulo
        
        for i in range(1, len(self.arr)):
            max_ending_here = max(self.arr[i] % modulo, (max_ending_here + self.arr[i]) % modulo)
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
    
    def get_max_sum_with_absolute_difference(self, target_difference):
        """Get maximum subarray sum where absolute difference between min and max is at most target_difference."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            min_val = max_val = self.arr[i]
            
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                min_val = min(min_val, self.arr[j])
                max_val = max(max_val, self.arr[j])
                
                if max_val - min_val <= target_difference:
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_frequency_constraint(self, max_frequency):
        """Get maximum subarray sum where no element appears more than max_frequency times."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            frequency = {}
            
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                frequency[self.arr[j]] = frequency.get(self.arr[j], 0) + 1
                
                if all(freq <= max_frequency for freq in frequency.values()):
                    max_sum = max(max_sum, current_sum)
                else:
                    break
        
        return max_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
advanced_max_sum = AdvancedMaximumSubarraySum(arr)

print(f"Max sum circular: {advanced_max_sum.get_max_sum_circular()}")

# 2D matrix example
matrix = [
    [1, 2, -1, -4, -20],
    [-8, -3, 4, 2, 1],
    [3, 8, 10, 1, 3],
    [-4, -1, 1, 7, -6]
]
print(f"Max sum 2D: {advanced_max_sum.get_max_sum_2d(matrix)}")

print(f"Max sum with 2 negations: {advanced_max_sum.get_max_sum_with_k_negations(2)}")
print(f"Max sum with 1 deletion: {advanced_max_sum.get_max_sum_with_deletions(1)}")
print(f"Max sum with 1 swap: {advanced_max_sum.get_max_sum_with_swaps(1)}")
print(f"Max sum with modulo 7: {advanced_max_sum.get_max_sum_with_modulo(7)}")
print(f"Max sum with difference <= 3: {advanced_max_sum.get_max_sum_with_absolute_difference(3)}")
print(f"Max sum with frequency <= 2: {advanced_max_sum.get_max_sum_with_frequency_constraint(2)}")
```

### **Variation 3: Maximum Subarray Sum with Constraints**
**Problem**: Handle maximum subarray sum with additional constraints (time limits, value ranges, length constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedMaximumSubarraySum:
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
    
    def get_max_sum_with_time_constraints(self, time_limit):
        """Get maximum subarray sum considering time constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        start_time = 0
        
        for i in range(len(self.arr)):
            current_sum = 0
            current_time = start_time
            
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                current_time += 1
                
                if current_time <= time_limit:
                    max_sum = max(max_sum, current_sum)
                else:
                    break
        
        return max_sum
    
    def get_max_sum_with_value_constraints(self, min_value, max_value):
        """Get maximum subarray sum with value constraints."""
        if not self.arr:
            return 0
        
        # Filter array to only include values within constraints
        filtered_arr = [x for x in self.arr if min_value <= x <= max_value]
        
        if not filtered_arr:
            return 0
        
        max_ending_here = max_so_far = filtered_arr[0]
        
        for i in range(1, len(filtered_arr)):
            max_ending_here = max(filtered_arr[i], max_ending_here + filtered_arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        
        return max_so_far
    
    def get_max_sum_with_length_constraints(self, min_length, max_length):
        """Get maximum subarray sum with length constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            for j in range(i, min(i + max_length, len(self.arr))):
                current_sum += self.arr[j]
                if j - i + 1 >= min_length:
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_sum_constraints(self, min_sum, max_sum):
        """Get maximum subarray sum with sum constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                if min_sum <= current_sum <= max_sum:
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_parity_constraints(self, parity_type):
        """Get maximum subarray sum with parity constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                
                if parity_type == 'even' and current_sum % 2 == 0:
                    max_sum = max(max_sum, current_sum)
                elif parity_type == 'odd' and current_sum % 2 == 1:
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_mathematical_constraints(self, constraint_func):
        """Get maximum subarray sum with custom mathematical constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                
                if constraint_func(current_sum):
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_range_constraints(self, range_constraints):
        """Get maximum subarray sum with range constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                
                # Check if current subarray satisfies all range constraints
                satisfies_constraints = True
                for constraint in range_constraints:
                    if not constraint(i, j, current_sum):
                        satisfies_constraints = False
                        break
                
                if satisfies_constraints:
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_max_sum_with_optimization_constraints(self, optimization_func):
        """Get maximum subarray sum with optimization constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        best_subarray = None
        
        for i in range(len(self.arr)):
            current_sum = 0
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                
                if current_sum > max_sum:
                    max_sum = current_sum
                    best_subarray = (i, j, current_sum)
        
        if best_subarray:
            return optimization_func(best_subarray)
        
        return 0
    
    def get_max_sum_with_multiple_constraints(self, constraints_list):
        """Get maximum subarray sum with multiple constraints."""
        if not self.arr:
            return 0
        
        max_sum = float('-inf')
        
        for i in range(len(self.arr)):
            current_sum = 0
            for j in range(i, len(self.arr)):
                current_sum += self.arr[j]
                
                # Check if current subarray satisfies all constraints
                satisfies_all_constraints = True
                for constraint in constraints_list:
                    if not constraint(i, j, current_sum):
                        satisfies_all_constraints = False
                        break
                
                if satisfies_all_constraints:
                    max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def get_optimal_max_sum_strategy(self):
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
                    current_sum = strategy_func(10)  # 10 time units
                elif strategy_name == 'value_constraints':
                    current_sum = strategy_func(-5, 5)  # Values between -5 and 5
                elif strategy_name == 'length_constraints':
                    current_sum = strategy_func(2, 5)  # Length between 2 and 5
                elif strategy_name == 'sum_constraints':
                    current_sum = strategy_func(-10, 10)  # Sum between -10 and 10
                
                if current_sum > best_sum:
                    best_sum = current_sum
                    best_strategy = (strategy_name, current_sum)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_value': -5,
    'max_value': 5,
    'min_length': 2,
    'max_length': 5
}

arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
constrained_max_sum = ConstrainedMaximumSubarraySum(arr, constraints)

print("Time-constrained max sum:", constrained_max_sum.get_max_sum_with_time_constraints(5))
print("Value-constrained max sum:", constrained_max_sum.get_max_sum_with_value_constraints(-3, 3))
print("Length-constrained max sum:", constrained_max_sum.get_max_sum_with_length_constraints(2, 4))
print("Sum-constrained max sum:", constrained_max_sum.get_max_sum_with_sum_constraints(-5, 5))
print("Even parity max sum:", constrained_max_sum.get_max_sum_with_parity_constraints('even'))

# Custom mathematical constraint
def custom_constraint(sum_val):
    return sum_val % 3 == 0

print("Custom constraint max sum:", constrained_max_sum.get_max_sum_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(start, end, sum_val):
    return end - start + 1 >= 2 and sum_val > 0

range_constraints = [range_constraint]
print("Range-constrained max sum:", constrained_max_sum.get_max_sum_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(start, end, sum_val):
    return end - start + 1 >= 2

def constraint2(start, end, sum_val):
    return sum_val > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints max sum:", constrained_max_sum.get_max_sum_with_multiple_constraints(constraints_list))

# Optimal strategy
optimal = constrained_max_sum.get_optimal_max_sum_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Maximum Subarray Sum](https://cses.fi/problemset/task/1643) - Basic maximum subarray sum problem
- [Maximum Subarray Sum II](https://cses.fi/problemset/task/1644) - Advanced maximum subarray sum problem
- [Subarray Sums I](https://cses.fi/problemset/task/1660) - Subarray sum queries

#### **LeetCode Problems**
- [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) - Basic maximum subarray sum
- [Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) - Circular array variant
- [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) - Maximum product variant
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) - Subarray sum with target

#### **Problem Categories**
- **Dynamic Programming**: Kadane's algorithm, optimal substructure, local decisions
- **Array Processing**: Subarray problems, prefix sums, sliding window techniques
- **Optimization**: Maximum sum problems, constraint satisfaction, optimization algorithms
- **Algorithm Design**: Dynamic programming algorithms, greedy strategies, optimization techniques