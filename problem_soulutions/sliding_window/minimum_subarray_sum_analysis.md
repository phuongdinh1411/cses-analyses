---
layout: simple
title: "Minimum Subarray Sum - Modified Kadane's Algorithm"
permalink: /problem_soulutions/sliding_window/minimum_subarray_sum_analysis
---

# Minimum Subarray Sum - Modified Kadane's Algorithm

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement modified Kadane's algorithm for minimum subarray sum
- Apply dynamic programming concepts to find minimum subarray problems
- Optimize space complexity from O(n) to O(1) for minimum subarray problems
- Handle edge cases in minimum subarray problems (all positive numbers, single element)
- Recognize the relationship between maximum and minimum subarray algorithms

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, sliding window technique, Kadane's algorithm
- **Data Structures**: Arrays, prefix sums
- **Mathematical Concepts**: Minimum sum optimization, dynamic programming principles
- **Programming Skills**: Array manipulation, dynamic programming implementation
- **Related Problems**: Maximum subarray sum, subarray with given sum, maximum product subarray

## 📋 Problem Description

Given an array of integers, find the contiguous subarray (containing at least one number) which has the smallest sum and return its sum.

**Input**: 
- First line: n (number of elements)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: minimum sum of any contiguous subarray

**Constraints**:
- 1 ≤ n ≤ 10⁵
- -10⁴ ≤ arr[i] ≤ 10⁴

**Example**:
```
Input:
6
-2 1 -3 4 -1 2

Output:
-4

Explanation**: 
The subarray [-3] has the minimum sum of -3, but the subarray [-2, 1, -3] has sum -4.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays by considering every starting and ending position
- **Complete Coverage**: Guarantees finding the optimal solution by examining all possibilities
- **Simple Implementation**: Straightforward nested loops to generate all subarrays
- **Inefficient**: Time complexity grows quadratically with input size

**Key Insight**: Generate all possible subarrays and calculate their sums to find the minimum.

**Algorithm**:
- For each starting position i from 0 to n-1
- For each ending position j from i to n-1
- Calculate sum of subarray from i to j
- Keep track of minimum sum found

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2]

All subarrays and their sums:
i=0: [-2]=-2, [-2,1]=-1, [-2,1,-3]=-4, [-2,1,-3,4]=0, [-2,1,-3,4,-1]=-1, [-2,1,-3,4,-1,2]=1
i=1: [1]=1, [1,-3]=-2, [1,-3,4]=2, [1,-3,4,-1]=1, [1,-3,4,-1,2]=3
i=2: [-3]=-3, [-3,4]=1, [-3,4,-1]=0, [-3,4,-1,2]=2
i=3: [4]=4, [4,-1]=3, [4,-1,2]=5
i=4: [-1]=-1, [-1,2]=1
i=5: [2]=2

Minimum sum: -4
```

**Implementation**:
```python
def brute_force_minimum_subarray_sum(arr):
    """
    Find minimum subarray sum using brute force approach
    
    Args:
        arr: List of integers
    
    Returns:
        int: Minimum sum of any contiguous subarray
    """
    n = len(arr)
    min_sum = float('inf')
    
    for i in range(n):
        for j in range(i, n):
            # Calculate sum of subarray from i to j
            current_sum = sum(arr[i:j+1])
            min_sum = min(min_sum, current_sum)
    
    return min_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
result = brute_force_minimum_subarray_sum(arr)
print(f"Brute force result: {result}")  # Output: -4
```

**Time Complexity**: O(n³) - Nested loops plus sum calculation
**Space Complexity**: O(1) - Only using constant extra space

**Why it's inefficient**: Triple nested operations make it too slow for large inputs.

---

### Approach 2: Optimized with Prefix Sums

**Key Insights from Optimized Approach**:
- **Prefix Sum Optimization**: Use prefix sums to calculate subarray sums in O(1) time
- **Efficiency Improvement**: Reduce time complexity from O(n³) to O(n²)
- **Space Trade-off**: Use O(n) extra space for prefix sums to speed up calculations
- **Better Performance**: Significantly faster than brute force for larger inputs

**Key Insight**: Precompute prefix sums to eliminate the need to recalculate subarray sums.

**Algorithm**:
- Calculate prefix sum array where prefix[i] = sum of elements from 0 to i
- For each starting position i, for each ending position j
- Calculate subarray sum as prefix[j] - prefix[i-1] (or prefix[j] if i=0)
- Keep track of minimum sum found

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2]
Prefix: [-2, -1, -4, 0, -1, 1]

Subarray sums using prefix:
i=0, j=0: prefix[0] = -2
i=0, j=1: prefix[1] = -1
i=0, j=2: prefix[2] = -4  ← Minimum sum
i=0, j=3: prefix[3] = 0
i=0, j=4: prefix[4] = -1
i=0, j=5: prefix[5] = 1

i=1, j=1: prefix[1] - prefix[0] = -1 - (-2) = 1
i=1, j=2: prefix[2] - prefix[0] = -4 - (-2) = -2
i=1, j=3: prefix[3] - prefix[0] = 0 - (-2) = 2
i=1, j=4: prefix[4] - prefix[0] = -1 - (-2) = 1
i=1, j=5: prefix[5] - prefix[0] = 1 - (-2) = 3

Minimum sum: -4
```

**Implementation**:
```python
def optimized_minimum_subarray_sum(arr):
    """
    Find minimum subarray sum using prefix sums
    
    Args:
        arr: List of integers
    
    Returns:
        int: Minimum sum of any contiguous subarray
    """
    n = len(arr)
    
    # Calculate prefix sums
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i-1] + arr[i]
    
    min_sum = float('inf')
    
    for i in range(n):
        for j in range(i, n):
            # Calculate subarray sum using prefix sums
            if i == 0:
                current_sum = prefix[j]
            else:
                current_sum = prefix[j] - prefix[i-1]
            min_sum = min(min_sum, current_sum)
    
    return min_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
result = optimized_minimum_subarray_sum(arr)
print(f"Optimized result: {result}")  # Output: -4
```

**Time Complexity**: O(n²) - Nested loops with O(1) sum calculation
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: Much faster than brute force, but still not optimal.

---

### Approach 3: Optimal with Modified Kadane's Algorithm

**Key Insights from Optimal Approach**:
- **Dynamic Programming**: Use optimal substructure property of minimum subarray problem
- **Local vs Global Minimum**: Track both current subarray sum and global minimum
- **Greedy Decision**: Start new subarray when current sum becomes positive
- **Optimal Complexity**: Achieve O(n) time and O(1) space complexity

**Key Insight**: At each position, decide whether to extend the current subarray or start a new one.

**Algorithm**:
- Initialize current_sum and min_sum to first element
- For each element from index 1 to n-1:
  - Update current_sum = min(arr[i], current_sum + arr[i])
  - Update min_sum = min(min_sum, current_sum)
- Return min_sum

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2]

Step 0: current_sum = -2, min_sum = -2
Step 1: arr[1] = 1
        current_sum = min(1, -2 + 1) = min(1, -1) = -1
        min_sum = min(-2, -1) = -2
Step 2: arr[2] = -3
        current_sum = min(-3, -1 + (-3)) = min(-3, -4) = -4
        min_sum = min(-2, -4) = -4
Step 3: arr[3] = 4
        current_sum = min(4, -4 + 4) = min(4, 0) = 0
        min_sum = min(-4, 0) = -4
Step 4: arr[4] = -1
        current_sum = min(-1, 0 + (-1)) = min(-1, -1) = -1
        min_sum = min(-4, -1) = -4
Step 5: arr[5] = 2
        current_sum = min(2, -1 + 2) = min(2, 1) = 1
        min_sum = min(-4, 1) = -4

Final result: -4
```

**Implementation**:
```python
def optimal_minimum_subarray_sum(arr):
    """
    Find minimum subarray sum using modified Kadane's algorithm
    
    Args:
        arr: List of integers
    
    Returns:
        int: Minimum sum of any contiguous subarray
    """
    if not arr:
        return 0
    
    current_sum = min_sum = arr[0]
    
    for i in range(1, len(arr)):
        # Either extend current subarray or start new one
        current_sum = min(arr[i], current_sum + arr[i])
        # Update global minimum
        min_sum = min(min_sum, current_sum)
    
    return min_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
result = optimal_minimum_subarray_sum(arr)
print(f"Optimal result: {result}")  # Output: -4
```

**Time Complexity**: O(n) - Single pass through the array
**Space Complexity**: O(1) - Only using constant extra space

**Why it's optimal**: Best possible time complexity with minimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all possible subarrays |
| Optimized | O(n²) | O(n) | Use prefix sums for faster calculation |
| Optimal | O(n) | O(1) | Use dynamic programming with modified Kadane's algorithm |

### Time Complexity
- **Time**: O(n) - Single pass through the array
- **Space**: O(1) - Only using constant extra space

### Why This Solution Works
- **Optimal Substructure**: Minimum subarray ending at position i can be computed from minimum subarray ending at position i-1
- **Greedy Choice**: Start new subarray when current sum becomes positive
- **Dynamic Programming**: Use previous results to compute current result efficiently
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Modified Kadane's Algorithm**: The standard approach for minimum subarray sum problems
- **Dynamic Programming**: Use optimal substructure to avoid redundant calculations
- **Space Optimization**: Can achieve O(1) space complexity with careful implementation
- **Edge Cases**: Handle arrays with all positive numbers and single element arrays
- **Pattern Recognition**: This algorithm pattern applies to many subarray optimization problems