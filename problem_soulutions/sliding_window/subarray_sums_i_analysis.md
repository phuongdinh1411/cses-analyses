---
layout: simple
title: "Subarray Sums I - Hash Map Technique"
permalink: /problem_soulutions/sliding_window/subarray_sums_i_analysis
---

# Subarray Sums I - Hash Map Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement hash map technique for counting subarray sums
- Apply prefix sum concept to efficiently count subarrays with given sum
- Optimize subarray sum counting using hash maps
- Handle edge cases in subarray sum counting problems
- Recognize when to use hash maps vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Hash maps, prefix sums, subarray problems, counting
- **Data Structures**: Arrays, hash maps, prefix sums
- **Mathematical Concepts**: Subarray sum optimization, prefix sum properties, counting
- **Programming Skills**: Array manipulation, hash map implementation, counting
- **Related Problems**: Maximum subarray sum, subarray with given sum, longest subarray with sum

## 📋 Problem Description

Given an array of integers and a target sum, count the number of contiguous subarrays that sum to the target value.

**Input**: 
- First line: n (number of elements) and target (target sum)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: number of subarrays with sum equal to target

**Constraints**:
- 1 ≤ n ≤ 10⁵
- -10⁴ ≤ arr[i] ≤ 10⁴
- -10⁹ ≤ target ≤ 10⁹

**Example**:
```
Input:
6 7
1 4 20 3 10 5

Output:
1

Explanation**: 
The subarray [20, 3, 10] has sum 33.
The subarray [3, 10, 5] has sum 18.
The subarray [4, 20, 3, 10] has sum 37.
The subarray [1, 4, 20, 3, 10] has sum 38.
The subarray [1, 4, 20, 3, 10, 5] has sum 43.
Wait, let me recalculate: [1, 4, 20, 3, 10, 5] = 1 + 4 + 20 + 3 + 10 + 5 = 43
But we need sum = 7. Let me check: [1, 4, 20, 3, 10, 5] = 43 ≠ 7
Actually, let me fix the example:
```

Let me fix the example:

**Example**:
```
Input:
6 33
1 4 20 3 10 5

Output:
1

Explanation**: 
The subarray [20, 3, 10] has sum 33.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays by considering every starting and ending position
- **Complete Coverage**: Guarantees finding all solutions by examining all possibilities
- **Simple Implementation**: Straightforward nested loops to generate all subarrays
- **Inefficient**: Time complexity grows quadratically with input size

**Key Insight**: Generate all possible subarrays and calculate their sums to count those equal to target.

**Algorithm**:
- Initialize counter to 0
- For each starting position i from 0 to n-1
- For each ending position j from i to n-1
- Calculate sum of subarray from i to j
- If sum equals target, increment counter
- Return counter

**Visual Example**:
```
Array: [1, 4, 20, 3, 10, 5], target = 33

All subarrays and their sums:
i=0: [1]=1, [1,4]=5, [1,4,20]=25, [1,4,20,3]=28, [1,4,20,3,10]=38, [1,4,20,3,10,5]=43
i=1: [4]=4, [4,20]=24, [4,20,3]=27, [4,20,3,10]=37, [4,20,3,10,5]=42
i=2: [20]=20, [20,3]=23, [20,3,10]=33  ← Count: 1
i=3: [3]=3, [3,10]=13, [3,10,5]=18
i=4: [10]=10, [10,5]=15
i=5: [5]=5

Total count: 1
```

**Implementation**:
```python
def brute_force_subarray_sums_i(arr, target):
    """
    Count subarrays with given sum using brute force
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Number of subarrays with sum equal to target
    """
    n = len(arr)
    count = 0
    
    for i in range(n):
        for j in range(i, n):
            # Calculate sum of subarray from i to j
            current_sum = sum(arr[i:j+1])
            if current_sum == target:
                count += 1
    
    return count

# Example usage
arr = [1, 4, 20, 3, 10, 5]
target = 33
result = brute_force_subarray_sums_i(arr, target)
print(f"Brute force result: {result}")  # Output: 1
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
- Initialize counter to 0
- For each starting position i, for each ending position j
- Calculate subarray sum as prefix[j] - prefix[i-1] (or prefix[j] if i=0)
- If sum equals target, increment counter
- Return counter

**Visual Example**:
```
Array: [1, 4, 20, 3, 10, 5], target = 33
Prefix: [1, 5, 25, 28, 38, 43]

Subarray sums using prefix:
i=0, j=0: prefix[0] = 1
i=0, j=1: prefix[1] = 5
i=0, j=2: prefix[2] = 25
i=0, j=3: prefix[3] = 28
i=0, j=4: prefix[4] = 38
i=0, j=5: prefix[5] = 43

i=1, j=1: prefix[1] - prefix[0] = 5 - 1 = 4
i=1, j=2: prefix[2] - prefix[0] = 25 - 1 = 24
i=1, j=3: prefix[3] - prefix[0] = 28 - 1 = 27
i=1, j=4: prefix[4] - prefix[0] = 38 - 1 = 37
i=1, j=5: prefix[5] - prefix[0] = 43 - 1 = 42

i=2, j=2: prefix[2] - prefix[1] = 25 - 5 = 20
i=2, j=3: prefix[3] - prefix[1] = 28 - 5 = 23
i=2, j=4: prefix[4] - prefix[1] = 38 - 5 = 33  ← Count: 1

Total count: 1
```

**Implementation**:
```python
def optimized_subarray_sums_i(arr, target):
    """
    Count subarrays with given sum using prefix sums
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Number of subarrays with sum equal to target
    """
    n = len(arr)
    
    # Calculate prefix sums
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i-1] + arr[i]
    
    count = 0
    
    for i in range(n):
        for j in range(i, n):
            # Calculate subarray sum using prefix sums
            if i == 0:
                current_sum = prefix[j]
            else:
                current_sum = prefix[j] - prefix[i-1]
            if current_sum == target:
                count += 1
    
    return count

# Example usage
arr = [1, 4, 20, 3, 10, 5]
target = 33
result = optimized_subarray_sums_i(arr, target)
print(f"Optimized result: {result}")  # Output: 1
```

**Time Complexity**: O(n²) - Nested loops with O(1) sum calculation
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: Much faster than brute force, but still not optimal.

---

### Approach 3: Optimal with Hash Map

**Key Insights from Optimal Approach**:
- **Hash Map Optimization**: Use hash map to store prefix sums and their frequencies
- **Efficiency Improvement**: Reduce time complexity from O(n²) to O(n)
- **Space Trade-off**: Use O(n) extra space for hash map to achieve linear time
- **Optimal Performance**: Best possible time complexity for this problem

**Key Insight**: Use hash map to count how many times each prefix sum occurs, then for each current prefix sum, count how many previous prefix sums give us the target.

**Algorithm**:
- Initialize hash map with {0: 1} to handle subarrays starting from index 0
- Initialize counter to 0 and prefix sum to 0
- For each element in the array:
  - Add current element to prefix sum
  - If (prefix_sum - target) exists in hash map, add its frequency to counter
  - Increment frequency of current prefix sum in hash map
- Return counter

**Visual Example**:
```
Array: [1, 4, 20, 3, 10, 5], target = 33
Hash map: {0: 1}

i=0: prefix_sum = 1
     Look for 1 - 33 = -32 in hash map (not found)
     Hash map: {0: 1, 1: 1}

i=1: prefix_sum = 5
     Look for 5 - 33 = -28 in hash map (not found)
     Hash map: {0: 1, 1: 1, 5: 1}

i=2: prefix_sum = 25
     Look for 25 - 33 = -8 in hash map (not found)
     Hash map: {0: 1, 1: 1, 5: 1, 25: 1}

i=3: prefix_sum = 28
     Look for 28 - 33 = -5 in hash map (not found)
     Hash map: {0: 1, 1: 1, 5: 1, 25: 1, 28: 1}

i=4: prefix_sum = 38
     Look for 38 - 33 = 5 in hash map (found with frequency 1)
     Count += 1
     Hash map: {0: 1, 1: 1, 5: 1, 25: 1, 28: 1, 38: 1}

i=5: prefix_sum = 43
     Look for 43 - 33 = 10 in hash map (not found)
     Hash map: {0: 1, 1: 1, 5: 1, 25: 1, 28: 1, 38: 1, 43: 1}

Total count: 1
```

**Implementation**:
```python
def optimal_subarray_sums_i(arr, target):
    """
    Count subarrays with given sum using hash map
    
    Args:
        arr: List of integers
        target: Target sum
    
    Returns:
        int: Number of subarrays with sum equal to target
    """
    n = len(arr)
    prefix_sum_map = {0: 1}  # Handle subarrays starting from index 0
    prefix_sum = 0
    count = 0
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Count how many previous prefix sums give us the target
        if prefix_sum - target in prefix_sum_map:
            count += prefix_sum_map[prefix_sum - target]
        
        # Increment frequency of current prefix sum
        prefix_sum_map[prefix_sum] = prefix_sum_map.get(prefix_sum, 0) + 1
    
    return count

# Example usage
arr = [1, 4, 20, 3, 10, 5]
target = 33
result = optimal_subarray_sums_i(arr, target)
print(f"Optimal result: {result}")  # Output: 1
```

**Time Complexity**: O(n) - Single pass through the array
**Space Complexity**: O(n) - Hash map for prefix sums

**Why it's optimal**: Best possible time complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all possible subarrays |
| Optimized | O(n²) | O(n) | Use prefix sums for faster calculation |
| Optimal | O(n) | O(n) | Use hash map to count prefix sum frequencies |

### Time Complexity
- **Time**: O(n) - Single pass through the array
- **Space**: O(n) - Hash map for prefix sums

### Why This Solution Works
- **Hash Map Counting**: Use hash map to count frequencies of prefix sums
- **Prefix Sum Property**: If prefix[j] - prefix[i] = target, then subarray from i+1 to j has sum target
- **Frequency Counting**: Count how many times each prefix sum occurs
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Hash Map Counting**: The standard approach for counting subarray sums
- **Prefix Sum Property**: Use prefix sums to efficiently calculate subarray sums
- **Frequency Tracking**: Track frequencies of prefix sums to count valid subarrays
- **Edge Cases**: Handle subarrays starting from index 0 with {0: 1} initialization
- **Pattern Recognition**: This technique applies to many subarray sum counting problems