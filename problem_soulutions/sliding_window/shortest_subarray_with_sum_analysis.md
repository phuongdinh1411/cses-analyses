---
layout: simple
title: "Shortest Subarray with Sum - Two Pointers Technique"
permalink: /problem_soulutions/sliding_window/shortest_subarray_with_sum_analysis
---

# Shortest Subarray with Sum - Two Pointers Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement two pointers technique for finding shortest subarrays
- Apply sliding window technique for variable-size windows with constraints
- Optimize subarray sum calculations using prefix sums and hash maps
- Handle edge cases in shortest subarray problems
- Recognize when to use two pointers vs other approaches

## 📋 Problem Description

Given an array of integers and a target sum, find the length of the shortest contiguous subarray that sums to at least the target value. If no such subarray exists, return 0.

**Input**: 
- First line: n (number of elements) and target (target sum)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: length of shortest subarray with sum >= target, or 0 if none exists

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ arr[i] ≤ 10⁴
- 1 ≤ target ≤ 10⁹

**Example**:
```
Input:
6 7
2 3 1 2 4 3

Output:
2

Explanation**: 
The subarray [4, 3] has sum 7 and length 2.
The subarray [2, 3, 1, 2] has sum 8 and length 4.
The shortest subarray with sum >= 7 is [4, 3] with length 2.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays by considering every starting and ending position
- **Complete Coverage**: Guarantees finding the optimal solution by examining all possibilities
- **Simple Implementation**: Straightforward nested loops to generate all subarrays
- **Inefficient**: Time complexity grows quadratically with input size

**Key Insight**: Generate all possible subarrays and calculate their sums to find the shortest one with sum >= target.

**Algorithm**:
- For each starting position i from 0 to n-1
- For each ending position j from i to n-1
- Calculate sum of subarray from i to j
- If sum >= target, update minimum length
- Return minimum length found

**Visual Example**:
```
Array: [2, 3, 1, 2, 4, 3], target = 7

All subarrays and their sums:
i=0: [2]=2, [2,3]=5, [2,3,1]=6, [2,3,1,2]=8  ← Length 4
i=1: [3]=3, [3,1]=4, [3,1,2]=6, [3,1,2,4]=10  ← Length 4
i=2: [1]=1, [1,2]=3, [1,2,4]=7  ← Length 3
i=3: [2]=2, [2,4]=6, [2,4,3]=9  ← Length 3
i=4: [4]=4, [4,3]=7  ← Length 2
i=5: [3]=3

Shortest subarray with sum >= 7: [4, 3] with length 2
```

**Implementation**:
```python
def brute_force_shortest_subarray_with_sum(arr, target):
    """
    Find shortest subarray with sum >= target using brute force
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Length of shortest subarray with sum >= target
    """
    n = len(arr)
    min_length = float('inf')
    
    for i in range(n):
        for j in range(i, n):
            # Calculate sum of subarray from i to j
            current_sum = sum(arr[i:j+1])
            if current_sum >= target:
                min_length = min(min_length, j - i + 1)
    
    return min_length if min_length != float('inf') else 0

# Example usage
arr = [2, 3, 1, 2, 4, 3]
target = 7
result = brute_force_shortest_subarray_with_sum(arr, target)
print(f"Brute force result: {result}")  # Output: 2
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
- If sum >= target, update minimum length
- Return minimum length found

**Visual Example**:
```
Array: [2, 3, 1, 2, 4, 3], target = 7
Prefix: [2, 5, 6, 8, 12, 15]

Subarray sums using prefix:
i=0, j=0: prefix[0] = 2
i=0, j=1: prefix[1] = 5
i=0, j=2: prefix[2] = 6
i=0, j=3: prefix[3] = 8  ← Length 4
i=0, j=4: prefix[4] = 12  ← Length 5
i=0, j=5: prefix[5] = 15  ← Length 6

i=1, j=1: prefix[1] - prefix[0] = 5 - 2 = 3
i=1, j=2: prefix[2] - prefix[0] = 6 - 2 = 4
i=1, j=3: prefix[3] - prefix[0] = 8 - 2 = 6
i=1, j=4: prefix[4] - prefix[0] = 12 - 2 = 10  ← Length 4
i=1, j=5: prefix[5] - prefix[0] = 15 - 2 = 13  ← Length 5

i=2, j=2: prefix[2] - prefix[1] = 6 - 5 = 1
i=2, j=3: prefix[3] - prefix[1] = 8 - 5 = 3
i=2, j=4: prefix[4] - prefix[1] = 12 - 5 = 7  ← Length 3
i=2, j=5: prefix[5] - prefix[1] = 15 - 5 = 10  ← Length 4

i=4, j=5: prefix[5] - prefix[3] = 15 - 8 = 7  ← Length 2

Shortest subarray with sum >= 7: length 2
```

**Implementation**:
```python
def optimized_shortest_subarray_with_sum(arr, target):
    """
    Find shortest subarray with sum >= target using prefix sums
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Length of shortest subarray with sum >= target
    """
    n = len(arr)
    
    # Calculate prefix sums
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i-1] + arr[i]
    
    min_length = float('inf')
    
    for i in range(n):
        for j in range(i, n):
            # Calculate subarray sum using prefix sums
            if i == 0:
                current_sum = prefix[j]
            else:
                current_sum = prefix[j] - prefix[i-1]
            if current_sum >= target:
                min_length = min(min_length, j - i + 1)
    
    return min_length if min_length != float('inf') else 0

# Example usage
arr = [2, 3, 1, 2, 4, 3]
target = 7
result = optimized_shortest_subarray_with_sum(arr, target)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - Nested loops with O(1) sum calculation
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: Much faster than brute force, but still not optimal.

---

### Approach 3: Optimal with Two Pointers

**Key Insights from Optimal Approach**:
- **Two Pointers Technique**: Use left and right pointers to maintain a sliding window
- **Efficiency Improvement**: Reduce time complexity from O(n²) to O(n)
- **Optimal Complexity**: Achieve O(n) time and O(1) space complexity
- **Greedy Approach**: Expand window when sum is less than target, contract when sum is >= target

**Key Insight**: Use two pointers to maintain a window where we expand right when sum < target and contract left when sum >= target.

**Algorithm**:
- Initialize left pointer to 0 and current sum to 0
- For each right pointer from 0 to n-1:
  - Add arr[right] to current sum
  - While current sum >= target:
    - Update minimum length
    - Subtract arr[left] from current sum
    - Move left pointer right
- Return minimum length found

**Visual Example**:
```
Array: [2, 3, 1, 2, 4, 3], target = 7

left=0, right=0: sum=2 < 7, expand
left=0, right=1: sum=5 < 7, expand
left=0, right=2: sum=6 < 7, expand
left=0, right=3: sum=8 >= 7, min_length=4, contract
left=1, right=3: sum=6 < 7, expand
left=1, right=4: sum=10 >= 7, min_length=4, contract
left=2, right=4: sum=7 >= 7, min_length=3, contract
left=3, right=4: sum=6 < 7, expand
left=3, right=5: sum=9 >= 7, min_length=3, contract
left=4, right=5: sum=7 >= 7, min_length=2, contract
left=5, right=5: sum=3 < 7, expand

Minimum length: 2
```

**Implementation**:
```python
def optimal_shortest_subarray_with_sum(arr, target):
    """
    Find shortest subarray with sum >= target using two pointers
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Length of shortest subarray with sum >= target
    """
    n = len(arr)
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        # Add current element to sum
        current_sum += arr[right]
        
        # Try to minimize window size while maintaining sum >= target
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0

# Example usage
arr = [2, 3, 1, 2, 4, 3]
target = 7
result = optimal_shortest_subarray_with_sum(arr, target)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n) - Each element is added and removed at most once
**Space Complexity**: O(1) - Only using constant extra space

**Why it's optimal**: Best possible time complexity with minimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all possible subarrays |
| Optimized | O(n²) | O(n) | Use prefix sums for faster calculation |
| Optimal | O(n) | O(1) | Use two pointers technique |

### Time Complexity
- **Time**: O(n) - Each element is processed at most twice (added and removed)
- **Space**: O(1) - Only using constant extra space

### Why This Solution Works
- **Two Pointers**: Use left and right pointers to maintain a sliding window
- **Greedy Approach**: Expand when sum < target, contract when sum >= target
- **Optimal Window**: Each valid window is checked exactly once
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Shortest Subarray with Sum At Least Target**
**Problem**: Find the length of the shortest subarray with sum at least target.

**Key Differences**: At least target instead of exactly target

**Solution Approach**: Use sliding window with sum tracking

**Implementation**:
```python
def shortest_subarray_sum_at_least(arr, target):
    """
    Find length of shortest subarray with sum at least target
    """
    n = len(arr)
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Try to shrink window while sum is at least target
        while current_sum >= target and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0

# Example usage
arr = [2, 3, 1, 2, 4, 3]
target = 7
result = shortest_subarray_sum_at_least(arr, target)
print(f"Shortest subarray with sum >= {target}: {result}")  # Output: 2
```

#### **2. Shortest Subarray with Sum At Most Target**
**Problem**: Find the length of the shortest subarray with sum at most target.

**Key Differences**: At most target instead of exactly target

**Solution Approach**: Use sliding window with sum tracking

**Implementation**:
```python
def shortest_subarray_sum_at_most(arr, target):
    """
    Find length of shortest subarray with sum at most target
    """
    n = len(arr)
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Shrink window if sum exceeds target
        while current_sum > target and left <= right:
            current_sum -= arr[left]
            left += 1
        
        # Update minimum length if current sum is valid
        if current_sum <= target:
            min_length = min(min_length, right - left + 1)
    
    return min_length if min_length != float('inf') else 0

# Example usage
arr = [2, 3, 1, 2, 4, 3]
target = 5
result = shortest_subarray_sum_at_most(arr, target)
print(f"Shortest subarray with sum <= {target}: {result}")  # Output: 1
```

#### **3. Shortest Subarray with Sum in Range**
**Problem**: Find the length of the shortest subarray with sum in range [min_sum, max_sum].

**Key Differences**: Sum must be within a range instead of exact value

**Solution Approach**: Use sliding window with range checking

**Implementation**:
```python
def shortest_subarray_sum_in_range(arr, min_sum, max_sum):
    """
    Find length of shortest subarray with sum in range [min_sum, max_sum]
    """
    n = len(arr)
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Shrink window if sum exceeds max_sum
        while current_sum > max_sum and left <= right:
            current_sum -= arr[left]
            left += 1
        
        # Check if current sum is in valid range
        if min_sum <= current_sum <= max_sum:
            min_length = min(min_length, right - left + 1)
    
    return min_length if min_length != float('inf') else 0

# Example usage
arr = [2, 3, 1, 2, 4, 3]
min_sum, max_sum = 4, 7
result = shortest_subarray_sum_in_range(arr, min_sum, max_sum)
print(f"Shortest subarray with sum in [{min_sum}, {max_sum}]: {result}")  # Output: 2
```

### Related Problems

#### **CSES Problems**
- [Shortest Subarray with Sum](https://cses.fi/problemset/task/2101) - Find shortest subarray with given sum
- [Minimum Size Subarray Sum](https://cses.fi/problemset/task/2102) - Find minimum length subarray with sum >= target
- [Subarray Sums I](https://cses.fi/problemset/task/2103) - Count subarrays with given sum

#### **LeetCode Problems**
- [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) - Minimum length subarray with sum >= target
- [Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) - Shortest subarray with sum >= k
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) - Count subarrays with sum k
- [Maximum Size Subarray Sum Equals k](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/) - Maximum length subarray with sum k

#### **Problem Categories**
- **Sliding Window**: Variable-size windows, sum optimization, window management
- **Two Pointers**: Left and right pointer technique, window expansion and contraction
- **Array Processing**: Subarray analysis, sum calculation, length optimization
- **Greedy**: Greedy strategy for minimizing window size, optimal substructure

## 🚀 Key Takeaways

- **Two Pointers Technique**: The standard approach for shortest subarray problems
- **Sliding Window**: Maintain a window that satisfies the constraint
- **Greedy Strategy**: Always try to minimize window size while maintaining validity
- **Space Optimization**: Can achieve O(1) space complexity with careful implementation
- **Pattern Recognition**: This technique applies to many shortest subarray problems