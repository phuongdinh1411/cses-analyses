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