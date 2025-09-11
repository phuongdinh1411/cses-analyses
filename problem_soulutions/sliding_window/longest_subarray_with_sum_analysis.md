---
layout: simple
title: "Longest Subarray with Sum - Two Pointers Technique"
permalink: /problem_soulutions/sliding_window/longest_subarray_with_sum_analysis
---

# Longest Subarray with Sum - Two Pointers Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement two pointers technique for subarray problems
- Apply sliding window technique for variable-size windows
- Optimize subarray sum calculations using prefix sums and hash maps
- Handle edge cases in subarray sum problems
- Recognize when to use two pointers vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Two pointers, sliding window, prefix sums, hash maps
- **Data Structures**: Arrays, hash maps, prefix sums
- **Mathematical Concepts**: Subarray sum optimization, window management
- **Programming Skills**: Array manipulation, two pointers implementation
- **Related Problems**: Maximum subarray sum, subarray with given sum, shortest subarray with sum

## 📋 Problem Description

Given an array of integers and a target sum, find the length of the longest contiguous subarray that sums to the target value. If no such subarray exists, return 0.

**Input**: 
- First line: n (number of elements) and target (target sum)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: length of longest subarray with sum equal to target, or 0 if none exists

**Constraints**:
- 1 ≤ n ≤ 10⁵
- -10⁴ ≤ arr[i] ≤ 10⁴
- -10⁹ ≤ target ≤ 10⁹

**Example**:
```
Input:
6 3
-2 1 -3 4 -1 2

Output:
3

Explanation**: 
The subarray [1, -3, 4] has sum 2, and [4, -1, 2] has sum 5.
The subarray [-2, 1, -3, 4] has sum 0.
The subarray [1, -3, 4, -1, 2] has sum 3 and length 5.
But the longest subarray with sum 3 is [1, -3, 4, -1, 2] with length 5.
Wait, let me recalculate: [1, -3, 4, -1, 2] = 1 + (-3) + 4 + (-1) + 2 = 3 ✓
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays by considering every starting and ending position
- **Complete Coverage**: Guarantees finding the optimal solution by examining all possibilities
- **Simple Implementation**: Straightforward nested loops to generate all subarrays
- **Inefficient**: Time complexity grows quadratically with input size

**Key Insight**: Generate all possible subarrays and calculate their sums to find the longest one with target sum.

**Algorithm**:
- For each starting position i from 0 to n-1
- For each ending position j from i to n-1
- Calculate sum of subarray from i to j
- If sum equals target, update maximum length
- Return maximum length found

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2], target = 3

All subarrays and their sums:
i=0: [-2]=-2, [-2,1]=-1, [-2,1,-3]=-4, [-2,1,-3,4]=0, [-2,1,-3,4,-1]=-1, [-2,1,-3,4,-1,2]=1
i=1: [1]=1, [1,-3]=-2, [1,-3,4]=2, [1,-3,4,-1]=1, [1,-3,4,-1,2]=3  ← Length 5
i=2: [-3]=-3, [-3,4]=1, [-3,4,-1]=0, [-3,4,-1,2]=2
i=3: [4]=4, [4,-1]=3  ← Length 2
i=4: [-1]=-1, [-1,2]=1
i=5: [2]=2

Longest subarray with sum 3: [1, -3, 4, -1, 2] with length 5
```

**Implementation**:
```python
def brute_force_longest_subarray_with_sum(arr, target):
    """
    Find longest subarray with given sum using brute force
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Length of longest subarray with sum equal to target
    """
    n = len(arr)
    max_length = 0
    
    for i in range(n):
        for j in range(i, n):
            # Calculate sum of subarray from i to j
            current_sum = sum(arr[i:j+1])
            if current_sum == target:
                max_length = max(max_length, j - i + 1)
    
    return max_length

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
target = 3
result = brute_force_longest_subarray_with_sum(arr, target)
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
- If sum equals target, update maximum length
- Return maximum length found

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2], target = 3
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
i=1, j=5: prefix[5] - prefix[0] = 1 - (-2) = 3  ← Length 5

i=3, j=4: prefix[4] - prefix[2] = -1 - (-4) = 3  ← Length 2

Longest subarray with sum 3: length 5
```

**Implementation**:
```python
def optimized_longest_subarray_with_sum(arr, target):
    """
    Find longest subarray with given sum using prefix sums
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Length of longest subarray with sum equal to target
    """
    n = len(arr)
    
    # Calculate prefix sums
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i-1] + arr[i]
    
    max_length = 0
    
    for i in range(n):
        for j in range(i, n):
            # Calculate subarray sum using prefix sums
            if i == 0:
                current_sum = prefix[j]
            else:
                current_sum = prefix[j] - prefix[i-1]
            if current_sum == target:
                max_length = max(max_length, j - i + 1)
    
    return max_length

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
target = 3
result = optimized_longest_subarray_with_sum(arr, target)
print(f"Optimized result: {result}")  # Output: 5
```

**Time Complexity**: O(n²) - Nested loops with O(1) sum calculation
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: Much faster than brute force, but still not optimal.

---

### Approach 3: Optimal with Hash Map

**Key Insights from Optimal Approach**:
- **Hash Map Optimization**: Use hash map to store prefix sums and their first occurrence indices
- **Efficiency Improvement**: Reduce time complexity from O(n²) to O(n)
- **Space Trade-off**: Use O(n) extra space for hash map to achieve linear time
- **Optimal Performance**: Best possible time complexity for this problem

**Key Insight**: Use hash map to find if there exists a prefix sum that, when subtracted from current prefix sum, gives the target.

**Algorithm**:
- Initialize hash map with {0: -1} to handle subarrays starting from index 0
- Calculate prefix sum as we iterate through the array
- For each position, check if (current_prefix_sum - target) exists in hash map
- If it exists, update maximum length
- Store current prefix sum and its index in hash map (only first occurrence)

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2], target = 3
Hash map: {0: -1}

i=0: prefix_sum = -2
     Look for -2 - 3 = -5 in hash map (not found)
     Hash map: {0: -1, -2: 0}

i=1: prefix_sum = -1
     Look for -1 - 3 = -4 in hash map (not found)
     Hash map: {0: -1, -2: 0, -1: 1}

i=2: prefix_sum = -4
     Look for -4 - 3 = -7 in hash map (not found)
     Hash map: {0: -1, -2: 0, -1: 1, -4: 2}

i=3: prefix_sum = 0
     Look for 0 - 3 = -3 in hash map (not found)
     Hash map: {0: -1, -2: 0, -1: 1, -4: 2, 0: 3}

i=4: prefix_sum = -1
     Look for -1 - 3 = -4 in hash map (found at index 2)
     Length = 4 - 2 = 2
     Hash map: {0: -1, -2: 0, -1: 1, -4: 2, 0: 3}

i=5: prefix_sum = 1
     Look for 1 - 3 = -2 in hash map (found at index 0)
     Length = 5 - 0 = 5  ← Maximum length
     Hash map: {0: -1, -2: 0, -1: 1, -4: 2, 0: 3, 1: 5}

Maximum length: 5
```

**Implementation**:
```python
def optimal_longest_subarray_with_sum(arr, target):
    """
    Find longest subarray with given sum using hash map
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Length of longest subarray with sum equal to target
    """
    n = len(arr)
    prefix_sum_map = {0: -1}  # Handle subarrays starting from index 0
    prefix_sum = 0
    max_length = 0
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Check if there exists a prefix sum that gives us the target
        if prefix_sum - target in prefix_sum_map:
            length = i - prefix_sum_map[prefix_sum - target]
            max_length = max(max_length, length)
        
        # Store first occurrence of this prefix sum
        if prefix_sum not in prefix_sum_map:
            prefix_sum_map[prefix_sum] = i
    
    return max_length

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
target = 3
result = optimal_longest_subarray_with_sum(arr, target)
print(f"Optimal result: {result}")  # Output: 5
```

**Time Complexity**: O(n) - Single pass through the array
**Space Complexity**: O(n) - Hash map for prefix sums

**Why it's optimal**: Best possible time complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all possible subarrays |
| Optimized | O(n²) | O(n) | Use prefix sums for faster calculation |
| Optimal | O(n) | O(n) | Use hash map to find target prefix sums |

### Time Complexity
- **Time**: O(n) - Single pass through the array
- **Space**: O(n) - Hash map for prefix sums

### Why This Solution Works
- **Hash Map Lookup**: Use hash map to find if target prefix sum exists in O(1) time
- **Prefix Sum Property**: If prefix[j] - prefix[i] = target, then subarray from i+1 to j has sum target
- **First Occurrence**: Store only first occurrence of each prefix sum to get maximum length
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Hash Map Technique**: The standard approach for subarray sum problems
- **Prefix Sum Property**: Use prefix sums to efficiently calculate subarray sums
- **First Occurrence**: Store only first occurrence to maximize subarray length
- **Edge Cases**: Handle subarrays starting from index 0 with {0: -1} initialization
- **Pattern Recognition**: This technique applies to many subarray sum problems