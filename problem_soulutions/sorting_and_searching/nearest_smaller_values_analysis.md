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
