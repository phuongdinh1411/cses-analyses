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

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, Kadane's algorithm, optimization, subarray problems
- **Data Structures**: Arrays, DP tables, prefix sums
- **Mathematical Concepts**: Optimization, subarray theory, dynamic programming theory
- **Programming Skills**: Algorithm implementation, complexity analysis, DP optimization
- **Related Problems**: Maximum Subarray Sum (Kadane's algorithm), Subarray Sums II (counting), Array Division (optimization)

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
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
