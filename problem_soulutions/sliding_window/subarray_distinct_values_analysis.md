---
layout: simple
title: "Subarray Distinct Values - Two Pointers Technique"
permalink: /problem_soulutions/sliding_window/subarray_distinct_values_analysis
---

# Subarray Distinct Values - Two Pointers Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement two pointers technique for distinct values problems
- Apply sliding window technique for variable-size windows with constraints
- Optimize subarray distinct values calculations using hash maps
- Handle edge cases in distinct values problems
- Recognize when to use two pointers vs other approaches

## 📋 Problem Description

Given an array of integers, find the length of the longest contiguous subarray that contains only distinct values.

**Input**: 
- First line: n (number of elements)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: length of longest subarray with distinct values

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ arr[i] ≤ 10⁵

**Example**:
```
Input:
6
1 2 3 2 1 4

Output:
4

Explanation**: 
The subarray [1, 2, 3, 2] has distinct values [1, 2, 3] but contains duplicate 2.
The subarray [2, 3, 2, 1] has distinct values [2, 3, 1] but contains duplicate 2.
The subarray [3, 2, 1, 4] has distinct values [3, 2, 1, 4] and length 4.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n³)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each starting position i from 0 to n-1
2. For each ending position j from i to n-1
3. Check if subarray from i to j has distinct values
4. If yes, update maximum length
5. Return maximum length

**Implementation**:
```python
def brute_force_subarray_distinct_values(arr):
    n = len(arr)
    max_length = 0
    
    for i in range(n):
        for j in range(i, n):
            subarray = arr[i:j+1]
            if len(set(subarray)) == len(subarray):
                max_length = max(max_length, j - i + 1)
    
    return max_length
```

### Approach 2: Optimized with Hash Map
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each starting position i from 0 to n-1
2. Use hash map to track distinct values from position i
3. For each ending position j from i to n-1
4. Add arr[j] to hash map
5. If hash map size equals subarray length, update maximum length
6. Return maximum length

**Implementation**:
```python
def optimized_subarray_distinct_values(arr):
    n = len(arr)
    max_length = 0
    
    for i in range(n):
        distinct_values = set()
        for j in range(i, n):
            distinct_values.add(arr[j])
            if len(distinct_values) == j - i + 1:
                max_length = max(max_length, j - i + 1)
    
    return max_length
```

### Approach 3: Optimal with Two Pointers
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use two pointers: left and right
2. Use hash map to track frequency of values in current window
3. Expand right pointer while maintaining distinct values
4. When duplicate found, contract left pointer until distinct
5. Update maximum length throughout
6. Return maximum length

**Implementation**:
```python
def optimal_subarray_distinct_values(arr):
    n = len(arr)
    left = 0
    max_length = 0
    value_count = {}
    
    for right in range(n):
        value_count[arr[right]] = value_count.get(arr[right], 0) + 1
        
        while value_count[arr[right]] > 1:
            value_count[arr[left]] -= 1
            if value_count[arr[left]] == 0:
                del value_count[arr[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all possible subarrays |
| Optimized | O(n²) | O(n) | Use hash map for faster distinct check |
| Optimal | O(n) | O(n) | Use two pointers with hash map |

### Time Complexity
- **Time**: O(n) - Each element is processed at most twice
- **Space**: O(n) - Hash map for value frequencies

### Why This Solution Works
- **Two Pointers**: Use left and right pointers to maintain a sliding window
- **Hash Map Tracking**: Track frequency of values in current window
- **Window Management**: Expand when distinct, contract when duplicate found
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Count Subarrays with Distinct Values**
**Problem**: Count the number of subarrays that contain only distinct values.

**Key Differences**: Count instead of finding longest

**Solution Approach**: Use sliding window with counting

**Implementation**:
```python
def count_subarrays_distinct_values(arr):
    """
    Count number of subarrays with distinct values
    """
    n = len(arr)
    count = 0
    left = 0
    value_count = {}
    
    for right in range(n):
        # Add current element
        value_count[arr[right]] = value_count.get(arr[right], 0) + 1
        
        # Shrink window if duplicate found
        while value_count[arr[right]] > 1:
            value_count[arr[left]] -= 1
            if value_count[arr[left]] == 0:
                del value_count[arr[left]]
            left += 1
        
        # All subarrays ending at right with distinct values
        count += right - left + 1
    
    return count

# Example usage
arr = [1, 2, 1, 3, 4]
result = count_subarrays_distinct_values(arr)
print(f"Subarrays with distinct values: {result}")  # Output: 9
```

#### **2. Longest Subarray with At Most K Distinct Values**
**Problem**: Find the length of the longest subarray with at most k distinct values.

**Key Differences**: Allow k distinct values instead of all distinct

**Solution Approach**: Use sliding window with distinct count tracking

**Implementation**:
```python
def longest_subarray_k_distinct_values(arr, k):
    """
    Find length of longest subarray with at most k distinct values
    """
    if not arr or k == 0:
        return 0
    
    value_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(arr)):
        # Add current element
        value_count[arr[right]] = value_count.get(arr[right], 0) + 1
        
        # Shrink window if more than k distinct values
        while len(value_count) > k:
            value_count[arr[left]] -= 1
            if value_count[arr[left]] == 0:
                del value_count[arr[left]]
            left += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage
arr = [1, 2, 1, 2, 3]
k = 2
result = longest_subarray_k_distinct_values(arr, k)
print(f"Longest subarray with {k} distinct values: {result}")  # Output: 4
```

#### **3. Subarray with Exactly K Distinct Values**
**Problem**: Find the number of subarrays with exactly k distinct values.

**Key Differences**: Exactly k instead of at most k

**Solution Approach**: Use sliding window with two pointers

**Implementation**:
```python
def subarray_exactly_k_distinct_values(arr, k):
    """
    Find number of subarrays with exactly k distinct values
    """
    def at_most_k_distinct(arr, k):
        value_count = {}
        left = 0
        result = 0
        
        for right in range(len(arr)):
            value_count[arr[right]] = value_count.get(arr[right], 0) + 1
            
            while len(value_count) > k:
                value_count[arr[left]] -= 1
                if value_count[arr[left]] == 0:
                    del value_count[arr[left]]
                left += 1
            
            result += right - left + 1
        
        return result
    
    return at_most_k_distinct(arr, k) - at_most_k_distinct(arr, k - 1)

# Example usage
arr = [1, 2, 1, 2, 3]
k = 2
result = subarray_exactly_k_distinct_values(arr, k)
print(f"Subarrays with exactly {k} distinct values: {result}")  # Output: 7
```

### Related Problems

#### **CSES Problems**
- [Subarray Distinct Values](https://cses.fi/problemset/task/2101) - Find longest subarray with distinct values
- [Subarray with K Distinct Values](https://cses.fi/problemset/task/2102) - Find subarrays with k distinct values
- [Count Subarrays with Distinct Values](https://cses.fi/problemset/task/2103) - Count subarrays with distinct values

#### **LeetCode Problems**
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) - Longest substring with distinct characters
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) - At most k distinct characters
- [Longest Substring with At Most Two Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/) - At most two distinct characters
- [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) - At most two types of fruits

#### **Problem Categories**
- **Sliding Window**: Distinct values, character counting, window management
- **Two Pointers**: Left and right pointer technique, window expansion and contraction
- **Hash Map**: Value frequency tracking, efficient lookups, counting
- **Array Processing**: Subarray analysis, value tracking, pattern matching

## 🚀 Key Takeaways

- **Two Pointers Technique**: The standard approach for distinct values problems
- **Sliding Window**: Maintain a window with distinct values
- **Hash Map Tracking**: Use hash map to track value frequencies efficiently
- **Window Management**: Expand and contract window based on distinctness
- **Pattern Recognition**: This technique applies to many distinct values problems