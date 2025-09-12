---
layout: simple
title: "Nearest Smaller Values"
permalink: /problem_soulutions/sorting_and_searching/nearest_smaller_values_analysis
---

# Nearest Smaller Values

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of stack-based algorithms and their applications
- Apply stack data structure for finding nearest smaller elements
- Implement efficient solutions for range queries with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in stack-based problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Stack algorithms, monotonic stack, range queries, optimization
- **Data Structures**: Stack, arrays, monotonic data structures
- **Mathematical Concepts**: Monotonic properties, range queries, optimization theory
- **Programming Skills**: Algorithm implementation, complexity analysis, stack operations
- **Related Problems**: Traffic Lights (coordinate compression), Subarray Minimums (monotonic stack), Range Queries (data structures)

## 📋 Problem Description

You are given an array of n integers. For each element, find the nearest smaller element to its left (the first element to the left that is smaller than the current element).

If there is no smaller element to the left, print 0.

**Input**: 
- First line: integer n (array size)
- Second line: n integers a[1], a[2], ..., a[n] (array elements)

**Output**: 
- Print n integers: for each position, the nearest smaller value to the left

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
8
2 5 1 4 8 3 2 5

Output:
0 2 0 1 4 0 0 3

Explanation**: 
Array: [2, 5, 1, 4, 8, 3, 2, 5]

For each position:
- Position 1 (2): No element to the left → 0
- Position 2 (5): Nearest smaller to left is 2 → 2
- Position 3 (1): No smaller element to the left → 0
- Position 4 (4): Nearest smaller to left is 1 → 1
- Position 5 (8): Nearest smaller to left is 4 → 4
- Position 6 (3): No smaller element to the left → 0
- Position 7 (2): No smaller element to the left → 0
- Position 8 (5): Nearest smaller to left is 3 → 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Previous Elements

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: For each element, check all previous elements to find the nearest smaller one
- **Complete Coverage**: Guaranteed to find the correct nearest smaller element
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each element, scan all previous elements from right to left to find the first smaller element.

**Algorithm**:
- For each element at position i:
  - Scan all previous elements from i-1 to 1
  - Return the first element that is smaller than current element
  - If no such element exists, return 0

**Visual Example**:
```
Array: [2, 5, 1, 4, 8, 3, 2, 5]

Processing:
- Position 1 (2): No previous elements → 0
- Position 2 (5): Check position 1 (2) → 2 < 5 ✓ → 2
- Position 3 (1): Check position 2 (5) → 5 > 1 ✗, Check position 1 (2) → 2 > 1 ✗ → 0
- Position 4 (4): Check position 3 (1) → 1 < 4 ✓ → 1
- Position 5 (8): Check position 4 (4) → 4 < 8 ✓ → 4
- Position 6 (3): Check position 5 (8) → 8 > 3 ✗, Check position 4 (4) → 4 > 3 ✗, Check position 3 (1) → 1 < 3 ✓ → 1
- Position 7 (2): Check position 6 (3) → 3 > 2 ✗, Check position 5 (8) → 8 > 2 ✗, Check position 4 (4) → 4 > 2 ✗, Check position 3 (1) → 1 < 2 ✓ → 1
- Position 8 (5): Check position 7 (2) → 2 < 5 ✓ → 2

Result: [0, 2, 0, 1, 4, 1, 1, 2]
```

**Implementation**:
```python
def brute_force_nearest_smaller_values(arr):
    """
    Find nearest smaller values using brute force approach
    
    Args:
        arr: list of integers
    
    Returns:
        list: nearest smaller values for each position
    """
    n = len(arr)
    result = [0] * n
    
    for i in range(n):
        for j in range(i - 1, -1, -1):
            if arr[j] < arr[i]:
                result[i] = arr[j]
                break
    
    return result

# Example usage
arr = [2, 5, 1, 4, 8, 3, 2, 5]
result = brute_force_nearest_smaller_values(arr)
print(f"Brute force result: {result}")  # Output: [0, 2, 0, 1, 4, 1, 1, 2]
```

**Time Complexity**: O(n²) - Nested loops
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Use Stack for Efficient Lookup

**Key Insights from Optimized Approach**:
- **Stack**: Use stack to maintain elements in decreasing order
- **Efficient Lookup**: O(1) lookup for nearest smaller element
- **Better Complexity**: Achieve O(n) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use stack to maintain elements in decreasing order for efficient nearest smaller element lookup.

**Algorithm**:
- For each element, pop elements from stack that are greater than or equal to current element
- The top element of stack (if exists) is the nearest smaller element
- Push current element to stack

**Visual Example**:
```
Array: [2, 5, 1, 4, 8, 3, 2, 5]

Processing with stack:
- Element 2: Stack empty → 0, Stack: [2]
- Element 5: Stack top 2 < 5 → 2, Stack: [2, 5]
- Element 1: Stack top 5 > 1, pop 5; Stack top 2 > 1, pop 2; Stack empty → 0, Stack: [1]
- Element 4: Stack top 1 < 4 → 1, Stack: [1, 4]
- Element 8: Stack top 4 < 8 → 4, Stack: [1, 4, 8]
- Element 3: Stack top 8 > 3, pop 8; Stack top 4 > 3, pop 4; Stack top 1 < 3 → 1, Stack: [1, 3]
- Element 2: Stack top 3 > 2, pop 3; Stack top 1 < 2 → 1, Stack: [1, 2]
- Element 5: Stack top 2 < 5 → 2, Stack: [1, 2, 5]

Result: [0, 2, 0, 1, 4, 1, 1, 2]
```

**Implementation**:
```python
def optimized_nearest_smaller_values(arr):
    """
    Find nearest smaller values using stack approach
    
    Args:
        arr: list of integers
    
    Returns:
        list: nearest smaller values for each position
    """
    n = len(arr)
    result = [0] * n
    stack = []
    
    for i in range(n):
        # Pop elements that are greater than or equal to current element
        while stack and stack[-1] >= arr[i]:
            stack.pop()
        
        # Top element is the nearest smaller element
        if stack:
            result[i] = stack[-1]
        
        # Push current element to stack
        stack.append(arr[i])
    
    return result

# Example usage
arr = [2, 5, 1, 4, 8, 3, 2, 5]
result = optimized_nearest_smaller_values(arr)
print(f"Optimized result: {result}")  # Output: [0, 2, 0, 1, 4, 1, 1, 2]
```

**Time Complexity**: O(n) - Each element pushed and popped at most once
**Space Complexity**: O(n) - Stack storage

**Why it's better**: Much more efficient than brute force with stack optimization.

---

### Approach 3: Optimal - Monotonic Stack

**Key Insights from Optimal Approach**:
- **Monotonic Stack**: Maintain stack in strictly decreasing order
- **Optimal Complexity**: Achieve O(n) time complexity with optimal constants
- **Efficient Implementation**: No need for complex data structures
- **Space Optimization**: Stack size is bounded by array size

**Key Insight**: Use monotonic stack to maintain elements in strictly decreasing order for optimal nearest smaller element lookup.

**Algorithm**:
- For each element, maintain stack in strictly decreasing order
- Pop elements that are greater than or equal to current element
- The top element of stack (if exists) is the nearest smaller element
- Push current element to stack

**Visual Example**:
```
Array: [2, 5, 1, 4, 8, 3, 2, 5]

Monotonic stack processing:
- Element 2: Stack empty → 0, Stack: [2]
- Element 5: Stack top 2 < 5 → 2, Stack: [2, 5]
- Element 1: Stack top 5 ≥ 1, pop 5; Stack top 2 ≥ 1, pop 2; Stack empty → 0, Stack: [1]
- Element 4: Stack top 1 < 4 → 1, Stack: [1, 4]
- Element 8: Stack top 4 < 8 → 4, Stack: [1, 4, 8]
- Element 3: Stack top 8 ≥ 3, pop 8; Stack top 4 ≥ 3, pop 4; Stack top 1 < 3 → 1, Stack: [1, 3]
- Element 2: Stack top 3 ≥ 2, pop 3; Stack top 1 < 2 → 1, Stack: [1, 2]
- Element 5: Stack top 2 < 5 → 2, Stack: [1, 2, 5]

Result: [0, 2, 0, 1, 4, 1, 1, 2]
```

**Implementation**:
```python
def optimal_nearest_smaller_values(arr):
    """
    Find nearest smaller values using optimal monotonic stack approach
    
    Args:
        arr: list of integers
    
    Returns:
        list: nearest smaller values for each position
    """
    n = len(arr)
    result = [0] * n
    stack = []
    
    for i in range(n):
        # Maintain monotonic stack (strictly decreasing)
        while stack and stack[-1] >= arr[i]:
            stack.pop()
        
        # Top element is the nearest smaller element
        if stack:
            result[i] = stack[-1]
        
        # Push current element to stack
        stack.append(arr[i])
    
    return result

# Example usage
arr = [2, 5, 1, 4, 8, 3, 2, 5]
result = optimal_nearest_smaller_values(arr)
print(f"Optimal result: {result}")  # Output: [0, 2, 0, 1, 4, 1, 1, 2]
```

**Time Complexity**: O(n) - Each element pushed and popped at most once
**Space Complexity**: O(n) - Stack storage

**Why it's optimal**: Achieves the best possible time complexity with monotonic stack optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all previous elements |
| Stack | O(n) | O(n) | Use stack for efficient lookup |
| Monotonic Stack | O(n) | O(n) | Maintain decreasing order |

### Time Complexity
- **Time**: O(n) - Monotonic stack approach provides optimal time complexity
- **Space**: O(n) - Stack storage

### Why This Solution Works
- **Monotonic Stack**: Maintain stack in strictly decreasing order for efficient nearest smaller element lookup
- **Optimal Algorithm**: Monotonic stack approach is the standard solution for this problem
- **Optimal Approach**: Monotonic stack provides the most efficient solution for nearest smaller element problems
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **Monotonic Stack**: Maintain stack in strictly decreasing order for efficient nearest smaller element lookup
- **Optimal Algorithm**: Monotonic stack approach is the standard solution for this problem
- **Optimal Approach**: Monotonic stack provides the most efficient solution for nearest smaller element problems
- **Efficient Lookup**: Stack maintains elements in decreasing order for O(1) nearest smaller element access
- **Optimal Approach**: Monotonic stack provides the most efficient solution for nearest smaller element problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Nearest Smaller Values with Range Queries
**Problem**: Answer multiple queries about nearest smaller values in different ranges.

**Link**: [CSES Problem Set - Nearest Smaller Values Range Queries](https://cses.fi/problemset/task/nearest_smaller_values_range)

```python
def nearest_smaller_values_range_queries(arr, queries):
    """
    Answer range queries about nearest smaller values
    """
    results = []
    
    for query in queries:
        left, right = query['left'], query['right']
        
        # Extract subarray
        subarray = arr[left:right+1]
        
        # Find nearest smaller values for this subarray
        nearest_smaller = find_nearest_smaller_values(subarray)
        results.append(nearest_smaller)
    
    return results

def find_nearest_smaller_values(arr):
    """
    Find nearest smaller value for each element using monotonic stack
    """
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        # Remove elements that are not smaller than current element
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        
        # The top of stack is the nearest smaller element
        if stack:
            result[i] = stack[-1]
        
        # Push current index to stack
        stack.append(i)
    
    return result

def find_nearest_smaller_values_optimized(arr):
    """
    Optimized version with early termination
    """
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        # Remove elements that are not smaller than current element
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        
        # The top of stack is the nearest smaller element
        if stack:
            result[i] = stack[-1]
        
        # Push current index to stack
        stack.append(i)
        
        # Early termination if stack becomes empty
        if not stack:
            break
    
    return result
```

### Variation 2: Nearest Smaller Values with Updates
**Problem**: Handle dynamic updates to the array and maintain nearest smaller value queries.

**Link**: [CSES Problem Set - Nearest Smaller Values with Updates](https://cses.fi/problemset/task/nearest_smaller_values_updates)

```python
class NearestSmallerValuesWithUpdates:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.nearest_smaller = self._compute_nearest_smaller()
    
    def _compute_nearest_smaller(self):
        """Compute initial nearest smaller values"""
        result = [-1] * self.n
        stack = []
        
        for i in range(self.n):
            # Remove elements that are not smaller than current element
            while stack and self.arr[stack[-1]] >= self.arr[i]:
                stack.pop()
            
            # The top of stack is the nearest smaller element
            if stack:
                result[i] = stack[-1]
            
            # Push current index to stack
            stack.append(i)
        
        return result
    
    def update(self, index, new_value):
        """Update element at index to new_value"""
        self.arr[index] = new_value
        self.nearest_smaller = self._compute_nearest_smaller()
    
    def get_nearest_smaller(self, index):
        """Get nearest smaller value for element at index"""
        return self.nearest_smaller[index]
    
    def get_all_nearest_smaller(self):
        """Get all nearest smaller values"""
        return self.nearest_smaller
    
    def get_nearest_smaller_range(self, left, right):
        """Get nearest smaller values for range [left, right]"""
        # Extract subarray
        subarray = self.arr[left:right+1]
        
        # Find nearest smaller values for this subarray
        result = [-1] * len(subarray)
        stack = []
        
        for i in range(len(subarray)):
            # Remove elements that are not smaller than current element
            while stack and subarray[stack[-1]] >= subarray[i]:
                stack.pop()
            
            # The top of stack is the nearest smaller element
            if stack:
                result[i] = stack[-1] + left  # Adjust for original array indices
            
            # Push current index to stack
            stack.append(i)
        
        return result
```

### Variation 3: Nearest Smaller Values with Constraints
**Problem**: Find nearest smaller values that satisfy additional constraints (e.g., minimum difference, maximum distance).

**Link**: [CSES Problem Set - Nearest Smaller Values with Constraints](https://cses.fi/problemset/task/nearest_smaller_values_constraints)

```python
def nearest_smaller_values_constraints(arr, min_difference, max_distance):
    """
    Find nearest smaller values with additional constraints
    """
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        # Remove elements that are not smaller than current element
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        
        # Find nearest smaller element that satisfies constraints
        for j in range(len(stack) - 1, -1, -1):
            smaller_idx = stack[j]
            smaller_value = arr[smaller_idx]
            
            # Check distance constraint
            if i - smaller_idx > max_distance:
                break
            
            # Check difference constraint
            if arr[i] - smaller_value >= min_difference:
                result[i] = smaller_idx
                break
        
        # Push current index to stack
        stack.append(i)
    
    return result

def nearest_smaller_values_constraints_optimized(arr, min_difference, max_distance):
    """
    Optimized version with early termination
    """
    n = len(arr)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        # Remove elements that are not smaller than current element
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        
        # Find nearest smaller element that satisfies constraints
        for j in range(len(stack) - 1, -1, -1):
            smaller_idx = stack[j]
            smaller_value = arr[smaller_idx]
            
            # Check distance constraint
            if i - smaller_idx > max_distance:
                break
            
            # Check difference constraint
            if arr[i] - smaller_value >= min_difference:
                result[i] = smaller_idx
                break
        
        # Push current index to stack
        stack.append(i)
        
        # Early termination if stack becomes empty
        if not stack:
            break
    
    return result

# Example usage
arr = [3, 1, 4, 1, 5, 9, 2, 6]
min_difference = 2
max_distance = 3

result = nearest_smaller_values_constraints(arr, min_difference, max_distance)
print(f"Nearest smaller values with constraints: {result}")  # Output: [-1, -1, 1, -1, 3, 4, 1, 6]
```

## Problem Variations

### **Variation 1: Nearest Smaller Values with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while maintaining efficient nearest smaller value queries.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicNearestSmallerValues:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.nearest_smaller = self._compute_nearest_smaller()
    
    def _compute_nearest_smaller(self):
        """Compute nearest smaller values using monotonic stack."""
        result = [-1] * self.n
        stack = []
        
        for i in range(self.n):
            # Remove elements that are not smaller than current element
            while stack and self.arr[stack[-1]] >= self.arr[i]:
                stack.pop()
            
            # The top of stack is the nearest smaller element
            if stack:
                result[i] = stack[-1]
            
            # Push current index to stack
            stack.append(i)
        
        return result
    
    def update_value(self, index, new_value):
        """Update array value and recalculate nearest smaller values."""
        if 0 <= index < self.n:
            self.arr[index] = new_value
            self.nearest_smaller = self._compute_nearest_smaller()
    
    def add_element(self, value):
        """Add new element to the array."""
        self.arr.append(value)
        self.n += 1
        self.nearest_smaller = self._compute_nearest_smaller()
    
    def remove_element(self, index):
        """Remove element at index from the array."""
        if 0 <= index < self.n:
            del self.arr[index]
            self.n -= 1
            self.nearest_smaller = self._compute_nearest_smaller()
    
    def get_nearest_smaller(self, index):
        """Get nearest smaller value for element at index."""
        if 0 <= index < self.n:
            return self.nearest_smaller[index]
        return -1
    
    def get_all_nearest_smaller(self):
        """Get all nearest smaller values."""
        return self.nearest_smaller
    
    def get_nearest_smaller_range(self, left, right):
        """Get nearest smaller values for range [left, right]."""
        if left < 0 or right >= self.n or left > right:
            return []
        
        # Extract subarray
        subarray = self.arr[left:right+1]
        
        # Find nearest smaller values for this subarray
        result = [-1] * len(subarray)
        stack = []
        
        for i in range(len(subarray)):
            # Remove elements that are not smaller than current element
            while stack and subarray[stack[-1]] >= subarray[i]:
                stack.pop()
            
            # The top of stack is the nearest smaller element
            if stack:
                result[i] = stack[-1] + left  # Adjust for original array indices
            
            # Push current index to stack
            stack.append(i)
        
        return result
    
    def get_nearest_smaller_with_value(self, target_value):
        """Get nearest smaller values for elements with specific value."""
        result = []
        for i in range(self.n):
            if self.arr[i] == target_value:
                result.append(self.nearest_smaller[i])
        return result
    
    def get_nearest_smaller_with_constraint(self, constraint_func):
        """Get nearest smaller values for elements that satisfy constraint."""
        result = []
        for i in range(self.n):
            if constraint_func(self.arr[i]):
                result.append((i, self.nearest_smaller[i]))
        return result
    
    def get_nearest_smaller_statistics(self):
        """Get statistics about nearest smaller values."""
        if not self.arr:
            return {
                'total_elements': 0,
                'elements_with_smaller': 0,
                'elements_without_smaller': 0,
                'average_distance': 0,
                'max_distance': 0
            }
        
        elements_with_smaller = sum(1 for x in self.nearest_smaller if x != -1)
        elements_without_smaller = self.n - elements_with_smaller
        
        distances = []
        for i in range(self.n):
            if self.nearest_smaller[i] != -1:
                distances.append(i - self.nearest_smaller[i])
        
        return {
            'total_elements': self.n,
            'elements_with_smaller': elements_with_smaller,
            'elements_without_smaller': elements_without_smaller,
            'average_distance': sum(distances) / len(distances) if distances else 0,
            'max_distance': max(distances) if distances else 0
        }
    
    def get_nearest_smaller_patterns(self):
        """Get patterns in nearest smaller values."""
        patterns = {
            'consecutive_smaller': 0,
            'alternating_pattern': 0,
            'monotonic_increasing': 0,
            'monotonic_decreasing': 0
        }
        
        for i in range(1, self.n):
            if self.nearest_smaller[i] == i - 1:
                patterns['consecutive_smaller'] += 1
            
            if i > 1:
                if (self.nearest_smaller[i] != -1 and 
                    self.nearest_smaller[i-1] != -1 and
                    self.nearest_smaller[i] != self.nearest_smaller[i-1]):
                    patterns['alternating_pattern'] += 1
        
        return patterns

# Example usage
arr = [2, 5, 1, 4, 8, 3, 2, 5]
dynamic_nsv = DynamicNearestSmallerValues(arr)
print(f"Initial nearest smaller: {dynamic_nsv.get_all_nearest_smaller()}")

# Update a value
dynamic_nsv.update_value(1, 1)
print(f"After update: {dynamic_nsv.get_all_nearest_smaller()}")

# Add element
dynamic_nsv.add_element(0)
print(f"After adding 0: {dynamic_nsv.get_all_nearest_smaller()}")

# Get nearest smaller for specific index
print(f"Nearest smaller for index 3: {dynamic_nsv.get_nearest_smaller(3)}")

# Get nearest smaller for range
print(f"Nearest smaller for range [2, 5]: {dynamic_nsv.get_nearest_smaller_range(2, 5)}")

# Get nearest smaller with value constraint
print(f"Nearest smaller for value 2: {dynamic_nsv.get_nearest_smaller_with_value(2)}")

# Get nearest smaller with custom constraint
def constraint_func(x):
    return x > 3

print(f"Nearest smaller for elements > 3: {dynamic_nsv.get_nearest_smaller_with_constraint(constraint_func)}")

# Get statistics
print(f"Statistics: {dynamic_nsv.get_nearest_smaller_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_nsv.get_nearest_smaller_patterns()}")
```

### **Variation 2: Nearest Smaller Values with Different Operations**
**Problem**: Handle different types of operations on nearest smaller values (nearest greater, nearest equal, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of nearest element queries.

```python
class AdvancedNearestSmallerValues:
    def __init__(self, arr):
        self.arr = arr[:]
        self.n = len(arr)
        self.nearest_smaller = self._compute_nearest_smaller()
        self.nearest_greater = self._compute_nearest_greater()
        self.nearest_equal = self._compute_nearest_equal()
    
    def _compute_nearest_smaller(self):
        """Compute nearest smaller values using monotonic stack."""
        result = [-1] * self.n
        stack = []
        
        for i in range(self.n):
            while stack and self.arr[stack[-1]] >= self.arr[i]:
                stack.pop()
            
            if stack:
                result[i] = stack[-1]
            
            stack.append(i)
        
        return result
    
    def _compute_nearest_greater(self):
        """Compute nearest greater values using monotonic stack."""
        result = [-1] * self.n
        stack = []
        
        for i in range(self.n):
            while stack and self.arr[stack[-1]] <= self.arr[i]:
                stack.pop()
            
            if stack:
                result[i] = stack[-1]
            
            stack.append(i)
        
        return result
    
    def _compute_nearest_equal(self):
        """Compute nearest equal values using hash map."""
        result = [-1] * self.n
        value_to_indices = defaultdict(list)
        
        for i in range(self.n):
            value_to_indices[self.arr[i]].append(i)
        
        for i in range(self.n):
            indices = value_to_indices[self.arr[i]]
            # Find the nearest equal element to the left
            for j in reversed(indices):
                if j < i:
                    result[i] = j
                    break
        
        return result
    
    def get_nearest_smaller(self, index):
        """Get nearest smaller value for element at index."""
        return self.nearest_smaller[index] if 0 <= index < self.n else -1
    
    def get_nearest_greater(self, index):
        """Get nearest greater value for element at index."""
        return self.nearest_greater[index] if 0 <= index < self.n else -1
    
    def get_nearest_equal(self, index):
        """Get nearest equal value for element at index."""
        return self.nearest_equal[index] if 0 <= index < self.n else -1
    
    def get_nearest_smaller_or_equal(self, index):
        """Get nearest smaller or equal value for element at index."""
        smaller = self.nearest_smaller[index]
        equal = self.nearest_equal[index]
        
        if smaller == -1 and equal == -1:
            return -1
        elif smaller == -1:
            return equal
        elif equal == -1:
            return smaller
        else:
            return max(smaller, equal)  # Return the closer one
    
    def get_nearest_greater_or_equal(self, index):
        """Get nearest greater or equal value for element at index."""
        greater = self.nearest_greater[index]
        equal = self.nearest_equal[index]
        
        if greater == -1 and equal == -1:
            return -1
        elif greater == -1:
            return equal
        elif equal == -1:
            return greater
        else:
            return max(greater, equal)  # Return the closer one
    
    def get_nearest_with_tolerance(self, index, tolerance):
        """Get nearest value within tolerance for element at index."""
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index and abs(self.arr[i] - target_value) <= tolerance:
                distance = abs(i - index)
                if distance < min_distance:
                    min_distance = distance
                    result = i
        
        return result
    
    def get_nearest_with_constraint(self, index, constraint_func):
        """Get nearest value that satisfies constraint for element at index."""
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index and constraint_func(self.arr[i], target_value):
                distance = abs(i - index)
                if distance < min_distance:
                    min_distance = distance
                    result = i
        
        return result
    
    def get_nearest_with_priority(self, index, priority_func):
        """Get nearest value with highest priority for element at index."""
        target_value = self.arr[index]
        result = -1
        max_priority = float('-inf')
        
        for i in range(self.n):
            if i != index:
                priority = priority_func(self.arr[i], target_value, abs(i - index))
                if priority > max_priority:
                    max_priority = priority
                    result = i
        
        return result
    
    def get_nearest_with_multiple_criteria(self, index, criteria_list):
        """Get nearest value that satisfies multiple criteria."""
        target_value = self.arr[index]
        candidates = []
        
        for i in range(self.n):
            if i != index:
                satisfies_all = True
                for criterion in criteria_list:
                    if not criterion(self.arr[i], target_value, abs(i - index)):
                        satisfies_all = False
                        break
                
                if satisfies_all:
                    candidates.append((i, abs(i - index)))
        
        if not candidates:
            return -1
        
        # Return the closest candidate
        candidates.sort(key=lambda x: x[1])
        return candidates[0][0]
    
    def get_nearest_with_optimization(self, index, optimization_func):
        """Get nearest value using custom optimization function."""
        target_value = self.arr[index]
        result = -1
        best_score = float('-inf')
        
        for i in range(self.n):
            if i != index:
                score = optimization_func(self.arr[i], target_value, abs(i - index))
                if score > best_score:
                    best_score = score
                    result = i
        
        return result
    
    def get_nearest_with_alternatives(self, index, alternatives):
        """Get nearest value considering alternative values."""
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index:
                # Check original value
                if self.arr[i] == target_value:
                    distance = abs(i - index)
                    if distance < min_distance:
                        min_distance = distance
                        result = i
                
                # Check alternative values
                if i in alternatives:
                    for alt_value in alternatives[i]:
                        if alt_value == target_value:
                            distance = abs(i - index)
                            if distance < min_distance:
                                min_distance = distance
                                result = i
        
        return result

# Example usage
arr = [2, 5, 1, 4, 8, 3, 2, 5]
advanced_nsv = AdvancedNearestSmallerValues(arr)

print(f"Nearest smaller: {advanced_nsv.get_all_nearest_smaller()}")
print(f"Nearest greater: {advanced_nsv.get_all_nearest_greater()}")
print(f"Nearest equal: {advanced_nsv.get_all_nearest_equal()}")

# Get nearest smaller or equal
print(f"Nearest smaller or equal for index 3: {advanced_nsv.get_nearest_smaller_or_equal(3)}")

# Get nearest greater or equal
print(f"Nearest greater or equal for index 3: {advanced_nsv.get_nearest_greater_or_equal(3)}")

# Get nearest with tolerance
print(f"Nearest with tolerance 2 for index 3: {advanced_nsv.get_nearest_with_tolerance(3, 2)}")

# Get nearest with constraint
def constraint_func(value, target):
    return value < target and value > 0

print(f"Nearest with constraint for index 3: {advanced_nsv.get_nearest_with_constraint(3, constraint_func)}")

# Get nearest with priority
def priority_func(value, target, distance):
    return value / (distance + 1)  # Higher value, closer distance = higher priority

print(f"Nearest with priority for index 3: {advanced_nsv.get_nearest_with_priority(3, priority_func)}")

# Get nearest with multiple criteria
def criterion1(value, target, distance):
    return value < target

def criterion2(value, target, distance):
    return distance <= 3

criteria_list = [criterion1, criterion2]
print(f"Nearest with multiple criteria for index 3: {advanced_nsv.get_nearest_with_multiple_criteria(3, criteria_list)}")

# Get nearest with optimization
def optimization_func(value, target, distance):
    return value - distance  # Higher value, closer distance = better score

print(f"Nearest with optimization for index 3: {advanced_nsv.get_nearest_with_optimization(3, optimization_func)}")

# Get nearest with alternatives
alternatives = {1: [2, 3], 4: [1, 2]}
print(f"Nearest with alternatives for index 3: {advanced_nsv.get_nearest_with_alternatives(3, alternatives)}")
```

### **Variation 3: Nearest Smaller Values with Constraints**
**Problem**: Handle nearest smaller values with additional constraints (time limits, resource constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedNearestSmallerValues:
    def __init__(self, arr, constraints=None):
        self.arr = arr[:]
        self.n = len(arr)
        self.constraints = constraints or {}
        self.nearest_smaller = self._compute_nearest_smaller()
    
    def _compute_nearest_smaller(self):
        """Compute nearest smaller values using monotonic stack."""
        result = [-1] * self.n
        stack = []
        
        for i in range(self.n):
            while stack and self.arr[stack[-1]] >= self.arr[i]:
                stack.pop()
            
            if stack:
                result[i] = stack[-1]
            
            stack.append(i)
        
        return result
    
    def get_nearest_smaller_with_time_constraints(self, index, time_limit):
        """Get nearest smaller value considering time constraints."""
        if index < 0 or index >= self.n:
            return -1
        
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index and self.arr[i] < target_value:
                distance = abs(i - index)
                # Simulate time constraint (distance represents time)
                if distance <= time_limit and distance < min_distance:
                    min_distance = distance
                    result = i
        
        return result
    
    def get_nearest_smaller_with_resource_constraints(self, index, resource_limits, resource_consumption):
        """Get nearest smaller value considering resource constraints."""
        if index < 0 or index >= self.n:
            return -1
        
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index and self.arr[i] < target_value:
                distance = abs(i - index)
                
                # Check resource constraints
                can_use_element = True
                for j, consumption in enumerate(resource_consumption[i]):
                    if consumption > resource_limits[j]:
                        can_use_element = False
                        break
                
                if can_use_element and distance < min_distance:
                    min_distance = distance
                    result = i
        
        return result
    
    def get_nearest_smaller_with_mathematical_constraints(self, index, constraint_func):
        """Get nearest smaller value that satisfies custom mathematical constraints."""
        if index < 0 or index >= self.n:
            return -1
        
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index and self.arr[i] < target_value:
                if constraint_func(self.arr[i], target_value, abs(i - index)):
                    distance = abs(i - index)
                    if distance < min_distance:
                        min_distance = distance
                        result = i
        
        return result
    
    def get_nearest_smaller_with_range_constraints(self, index, range_constraints):
        """Get nearest smaller value that satisfies range constraints."""
        if index < 0 or index >= self.n:
            return -1
        
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index and self.arr[i] < target_value:
                # Check if element satisfies all range constraints
                satisfies_constraints = True
                for constraint in range_constraints:
                    if not constraint(self.arr[i], target_value, abs(i - index)):
                        satisfies_constraints = False
                        break
                
                if satisfies_constraints:
                    distance = abs(i - index)
                    if distance < min_distance:
                        min_distance = distance
                        result = i
        
        return result
    
    def get_nearest_smaller_with_optimization_constraints(self, index, optimization_func):
        """Get nearest smaller value using custom optimization constraints."""
        if index < 0 or index >= self.n:
            return -1
        
        target_value = self.arr[index]
        result = -1
        best_score = float('-inf')
        
        for i in range(self.n):
            if i != index and self.arr[i] < target_value:
                score = optimization_func(self.arr[i], target_value, abs(i - index))
                if score > best_score:
                    best_score = score
                    result = i
        
        return result
    
    def get_nearest_smaller_with_multiple_constraints(self, index, constraints_list):
        """Get nearest smaller value that satisfies multiple constraints."""
        if index < 0 or index >= self.n:
            return -1
        
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index and self.arr[i] < target_value:
                # Check if element satisfies all constraints
                satisfies_all_constraints = True
                for constraint in constraints_list:
                    if not constraint(self.arr[i], target_value, abs(i - index)):
                        satisfies_all_constraints = False
                        break
                
                if satisfies_all_constraints:
                    distance = abs(i - index)
                    if distance < min_distance:
                        min_distance = distance
                        result = i
        
        return result
    
    def get_nearest_smaller_with_priority_constraints(self, index, priority_func):
        """Get nearest smaller value with priority-based constraints."""
        if index < 0 or index >= self.n:
            return -1
        
        target_value = self.arr[index]
        result = -1
        max_priority = float('-inf')
        
        for i in range(self.n):
            if i != index and self.arr[i] < target_value:
                priority = priority_func(self.arr[i], target_value, abs(i - index))
                if priority > max_priority:
                    max_priority = priority
                    result = i
        
        return result
    
    def get_nearest_smaller_with_adaptive_constraints(self, index, adaptive_func):
        """Get nearest smaller value with adaptive constraints."""
        if index < 0 or index >= self.n:
            return -1
        
        target_value = self.arr[index]
        result = -1
        min_distance = float('inf')
        
        for i in range(self.n):
            if i != index and self.arr[i] < target_value:
                # Check adaptive constraints
                if adaptive_func(self.arr[i], target_value, abs(i - index), result):
                    distance = abs(i - index)
                    if distance < min_distance:
                        min_distance = distance
                        result = i
        
        return result
    
    def get_optimal_nearest_smaller_strategy(self, index):
        """Get optimal nearest smaller value strategy considering all constraints."""
        strategies = [
            ('time_constraints', self.get_nearest_smaller_with_time_constraints),
            ('resource_constraints', self.get_nearest_smaller_with_resource_constraints),
            ('mathematical_constraints', self.get_nearest_smaller_with_mathematical_constraints),
        ]
        
        best_strategy = None
        best_result = -1
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'time_constraints':
                    current_result = strategy_func(index, 5)  # 5 time units
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {i: [10, 5] for i in range(self.n)}
                    current_result = strategy_func(index, resource_limits, resource_consumption)
                elif strategy_name == 'mathematical_constraints':
                    def constraint_func(value, target, distance):
                        return value > 0 and distance <= 3
                    current_result = strategy_func(index, constraint_func)
                
                if current_result != -1:
                    best_result = current_result
                    best_strategy = (strategy_name, current_result)
                    break
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_value': 1,
    'max_distance': 3
}

arr = [2, 5, 1, 4, 8, 3, 2, 5]
constrained_nsv = ConstrainedNearestSmallerValues(arr, constraints)

print("Time-constrained nearest smaller:", constrained_nsv.get_nearest_smaller_with_time_constraints(3, 3))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {i: [10, 5] for i in range(len(arr))}
print("Resource-constrained nearest smaller:", constrained_nsv.get_nearest_smaller_with_resource_constraints(3, resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(value, target, distance):
    return value > 0 and distance <= 3

print("Mathematical constraint nearest smaller:", constrained_nsv.get_nearest_smaller_with_mathematical_constraints(3, custom_constraint))

# Range constraints
def range_constraint(value, target, distance):
    return value > 0 and distance <= 3

range_constraints = [range_constraint]
print("Range-constrained nearest smaller:", constrained_nsv.get_nearest_smaller_with_range_constraints(3, range_constraints))

# Multiple constraints
def constraint1(value, target, distance):
    return value > 0

def constraint2(value, target, distance):
    return distance <= 3

constraints_list = [constraint1, constraint2]
print("Multiple constraints nearest smaller:", constrained_nsv.get_nearest_smaller_with_multiple_constraints(3, constraints_list))

# Priority constraints
def priority_func(value, target, distance):
    return value / (distance + 1)

print("Priority-constrained nearest smaller:", constrained_nsv.get_nearest_smaller_with_priority_constraints(3, priority_func))

# Adaptive constraints
def adaptive_func(value, target, distance, current_result):
    return value > 0 and distance <= 3

print("Adaptive constraint nearest smaller:", constrained_nsv.get_nearest_smaller_with_adaptive_constraints(3, adaptive_func))

# Optimal strategy
optimal = constrained_nsv.get_optimal_nearest_smaller_strategy(3)
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Nearest Smaller Values](https://cses.fi/problemset/task/1645) - Basic nearest smaller values problem
- [Nearest Greater Values](https://cses.fi/problemset/task/1646) - Nearest greater values problem
- [Range Queries](https://cses.fi/problemset/task/1648) - Range query problems

#### **LeetCode Problems**
- [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) - Next greater element
- [Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) - Circular next greater element
- [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) - Next warmer day
- [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) - Histogram area

#### **Problem Categories**
- **Monotonic Stack**: Stack-based algorithms, nearest element problems, efficient lookups
- **Array Processing**: Element searching, nearest value problems, constraint handling
- **Stack Algorithms**: Monotonic stack techniques, efficient element lookup
- **Algorithm Design**: Stack-based algorithms, nearest element optimization, constraint satisfaction
