---
layout: simple
title: "Maximum Subarray Sum - Kadane's Algorithm"
permalink: /problem_soulutions/sliding_window/maximum_subarray_sum_analysis
---

# Maximum Subarray Sum - Kadane's Algorithm

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement Kadane's algorithm for maximum subarray sum
- Apply dynamic programming concepts to sliding window problems
- Optimize space complexity from O(n) to O(1) for maximum subarray problems
- Handle edge cases in subarray problems (all negative numbers, single element)
- Recognize when to use Kadane's algorithm vs other approaches

## 📋 Problem Description

Given an array of integers, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

**Input**: 
- First line: n (number of elements)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: maximum sum of any contiguous subarray

**Constraints**:
- 1 ≤ n ≤ 10⁵
- -10⁴ ≤ arr[i] ≤ 10⁴

**Example**:
```
Input:
6
-2 1 -3 4 -1 2

Output:
5

Explanation**: 
The subarray [4, -1, 2] has the maximum sum of 5.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays by considering every starting and ending position
- **Complete Coverage**: Guarantees finding the optimal solution by examining all possibilities
- **Simple Implementation**: Straightforward nested loops to generate all subarrays
- **Inefficient**: Time complexity grows quadratically with input size

**Key Insight**: Generate all possible subarrays and calculate their sums to find the maximum.

**Algorithm**:
- For each starting position i from 0 to n-1
- For each ending position j from i to n-1
- Calculate sum of subarray from i to j
- Keep track of maximum sum found

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2]

All subarrays and their sums:
i=0: [-2]=-2, [-2,1]=-1, [-2,1,-3]=-4, [-2,1,-3,4]=0, [-2,1,-3,4,-1]=-1, [-2,1,-3,4,-1,2]=1
i=1: [1]=1, [1,-3]=-2, [1,-3,4]=2, [1,-3,4,-1]=1, [1,-3,4,-1,2]=3
i=2: [-3]=-3, [-3,4]=1, [-3,4,-1]=0, [-3,4,-1,2]=2
i=3: [4]=4, [4,-1]=3, [4,-1,2]=5  ← Maximum sum
i=4: [-1]=-1, [-1,2]=1
i=5: [2]=2

Maximum sum: 5
```

**Implementation**:
```python
def brute_force_maximum_subarray_sum(arr):
    """
    Find maximum subarray sum using brute force approach
    
    Args:
        arr: List of integers
    
    Returns:
        int: Maximum sum of any contiguous subarray
    """
    n = len(arr)
    max_sum = float('-inf')
    
    for i in range(n):
        for j in range(i, n):
            # Calculate sum of subarray from i to j
            current_sum = sum(arr[i:j+1])
            max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
result = brute_force_maximum_subarray_sum(arr)
print(f"Brute force result: {result}")  # Output: 5
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
- Keep track of maximum sum found

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2]
Prefix: [-2, -1, -4, 0, -1, 1]

Subarray sums using prefix:
i=0, j=0: prefix[0] = -2
i=0, j=1: prefix[1] = -1
i=0, j=2: prefix[2] = -4
i=0, j=3: prefix[3] = 0
i=0, j=4: prefix[4] = -1
i=0, j=5: prefix[5] = 1

i=1, j=1: prefix[1] - prefix[0] = -1 - (-2) = 1
i=1, j=2: prefix[2] - prefix[0] = -4 - (-2) = -2
i=1, j=3: prefix[3] - prefix[0] = 0 - (-2) = 2
i=1, j=4: prefix[4] - prefix[0] = -1 - (-2) = 1
i=1, j=5: prefix[5] - prefix[0] = 1 - (-2) = 3

i=3, j=5: prefix[5] - prefix[2] = 1 - (-4) = 5  ← Maximum sum
```

**Implementation**:
```python
def optimized_maximum_subarray_sum(arr):
    """
    Find maximum subarray sum using prefix sums
    
    Args:
        arr: List of integers
    
    Returns:
        int: Maximum sum of any contiguous subarray
    """
    n = len(arr)
    
    # Calculate prefix sums
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i-1] + arr[i]
    
    max_sum = float('-inf')
    
    for i in range(n):
        for j in range(i, n):
            # Calculate subarray sum using prefix sums
            if i == 0:
                current_sum = prefix[j]
            else:
                current_sum = prefix[j] - prefix[i-1]
            max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
result = optimized_maximum_subarray_sum(arr)
print(f"Optimized result: {result}")  # Output: 5
```

**Time Complexity**: O(n²) - Nested loops with O(1) sum calculation
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: Much faster than brute force, but still not optimal.

---

### Approach 3: Optimal with Kadane's Algorithm

**Key Insights from Optimal Approach**:
- **Dynamic Programming**: Use optimal substructure property of maximum subarray problem
- **Local vs Global Maximum**: Track both current subarray sum and global maximum
- **Greedy Decision**: Start new subarray when current sum becomes negative
- **Optimal Complexity**: Achieve O(n) time and O(1) space complexity

**Key Insight**: At each position, decide whether to extend the current subarray or start a new one.

**Algorithm**:
- Initialize current_sum and max_sum to first element
- For each element from index 1 to n-1:
  - Update current_sum = max(arr[i], current_sum + arr[i])
  - Update max_sum = max(max_sum, current_sum)
- Return max_sum

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2]

Step 0: current_sum = -2, max_sum = -2
Step 1: arr[1] = 1
        current_sum = max(1, -2 + 1) = max(1, -1) = 1
        max_sum = max(-2, 1) = 1
Step 2: arr[2] = -3
        current_sum = max(-3, 1 + (-3)) = max(-3, -2) = -2
        max_sum = max(1, -2) = 1
Step 3: arr[3] = 4
        current_sum = max(4, -2 + 4) = max(4, 2) = 4
        max_sum = max(1, 4) = 4
Step 4: arr[4] = -1
        current_sum = max(-1, 4 + (-1)) = max(-1, 3) = 3
        max_sum = max(4, 3) = 4
Step 5: arr[5] = 2
        current_sum = max(2, 3 + 2) = max(2, 5) = 5
        max_sum = max(4, 5) = 5

Final result: 5
```

**Implementation**:
```python
def optimal_maximum_subarray_sum(arr):
    """
    Find maximum subarray sum using Kadane's algorithm
    
    Args:
        arr: List of integers
    
    Returns:
        int: Maximum sum of any contiguous subarray
    """
    if not arr:
        return 0
    
    current_sum = max_sum = arr[0]
    
    for i in range(1, len(arr)):
        # Either extend current subarray or start new one
        current_sum = max(arr[i], current_sum + arr[i])
        # Update global maximum
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
result = optimal_maximum_subarray_sum(arr)
print(f"Optimal result: {result}")  # Output: 5
```

**Time Complexity**: O(n) - Single pass through the array
**Space Complexity**: O(1) - Only using constant extra space

**Why it's optimal**: Best possible time complexity with minimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all possible subarrays |
| Optimized | O(n²) | O(n) | Use prefix sums for faster calculation |
| Optimal | O(n) | O(1) | Use dynamic programming with Kadane's algorithm |

### Time Complexity
- **Time**: O(n) - Single pass through the array
- **Space**: O(1) - Only using constant extra space

### Why This Solution Works
- **Optimal Substructure**: Maximum subarray ending at position i can be computed from maximum subarray ending at position i-1
- **Greedy Choice**: Start new subarray when current sum becomes negative
- **Dynamic Programming**: Use previous results to compute current result efficiently
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Maximum Subarray Product**
**Problem**: Find the contiguous subarray within an array that has the largest product.

**Key Differences**: Uses multiplication instead of addition, requires handling negative numbers differently

**Solution Approach**: Track both maximum and minimum products at each position

**Implementation**:
```python
def max_subarray_product(arr):
    """
    Find maximum subarray product using dynamic programming
    """
    if not arr:
        return 0
    
    max_prod = min_prod = result = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i] < 0:
            max_prod, min_prod = min_prod, max_prod
        
        max_prod = max(arr[i], max_prod * arr[i])
        min_prod = min(arr[i], min_prod * arr[i])
        result = max(result, max_prod)
    
    return result

# Example usage
arr = [2, 3, -2, 4]
result = max_subarray_product(arr)
print(f"Maximum subarray product: {result}")  # Output: 6
```

#### **2. Maximum Sum Circular Subarray**
**Problem**: Find the maximum sum of a non-empty subarray of a circular array.

**Key Differences**: Array is circular, need to consider wraparound cases

**Solution Approach**: Use Kadane's algorithm for both linear and circular cases

**Implementation**:
```python
def max_sum_circular_subarray(arr):
    """
    Find maximum sum in circular subarray
    """
    def kadane(arr):
        current_sum = max_sum = arr[0]
        for i in range(1, len(arr)):
            current_sum = max(arr[i], current_sum + arr[i])
            max_sum = max(max_sum, current_sum)
        return max_sum
    
    # Case 1: Maximum sum in linear array
    linear_max = kadane(arr)
    
    # Case 2: Maximum sum in circular array
    total_sum = sum(arr)
    inverted_arr = [-x for x in arr]
    circular_max = total_sum + kadane(inverted_arr)
    
    return max(linear_max, circular_max) if circular_max != 0 else linear_max

# Example usage
arr = [5, -3, 5]
result = max_sum_circular_subarray(arr)
print(f"Maximum circular subarray sum: {result}")  # Output: 10
```

#### **3. Maximum Sum of K Non-Overlapping Subarrays**
**Problem**: Find the maximum sum of k non-overlapping contiguous subarrays.

**Key Differences**: Need to find k separate subarrays instead of one

**Solution Approach**: Use dynamic programming with 2D state

**Implementation**:
```python
def max_sum_k_subarrays(arr, k):
    """
    Find maximum sum of k non-overlapping subarrays
    """
    n = len(arr)
    if k > n:
        return 0
    
    # dp[i][j] = maximum sum of j subarrays ending at position i
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    for j in range(1, k + 1):
        for i in range(j, n + 1):
            # Option 1: Don't include current element
            dp[i][j] = dp[i-1][j]
            
            # Option 2: Include current element in j-th subarray
            current_sum = 0
            for l in range(i, 0, -1):
                current_sum += arr[l-1]
                dp[i][j] = max(dp[i][j], dp[l-1][j-1] + current_sum)
    
    return dp[n][k]

# Example usage
arr = [1, 2, 1, 2, 6, 7, 5, 1]
k = 2
result = max_sum_k_subarrays(arr, k)
print(f"Maximum sum of {k} subarrays: {result}")  # Output: 23
```

### Related Problems

#### **CSES Problems**
- [Maximum Subarray Sum](https://cses.fi/problemset/task/1643) - Find maximum sum of contiguous subarray
- [Maximum Subarray Sum II](https://cses.fi/problemset/task/1644) - Find maximum sum of subarray with length constraints
- [Subarray Sums I](https://cses.fi/problemset/task/1661) - Count subarrays with given sum
- [Subarray Sums II](https://cses.fi/problemset/task/1662) - Count subarrays with given sum (with constraints)

#### **LeetCode Problems**
- [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) - Classic Kadane's algorithm problem
- [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) - Maximum subarray product
- [Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) - Circular array variant
- [Maximum Sum of 3 Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/) - Multiple subarrays

#### **Problem Categories**
- **Dynamic Programming**: Maximum subarray sum, maximum product subarray, circular subarray
- **Sliding Window**: Subarray with given sum, longest subarray with sum
- **Array Processing**: Subarray sums, subarray distinct values, subarray maximums

## 🚀 Key Takeaways

- **Kadane's Algorithm**: The standard approach for maximum subarray sum problems
- **Dynamic Programming**: Use optimal substructure to avoid redundant calculations
- **Space Optimization**: Can achieve O(1) space complexity with careful implementation
- **Edge Cases**: Handle arrays with all negative numbers and single element arrays
- **Pattern Recognition**: This algorithm pattern applies to many subarray optimization problems