---
layout: simple
title: "Subarray with K Distinct - Two Pointers Technique"
permalink: /problem_soulutions/sliding_window/subarray_with_k_distinct_analysis
---

# Subarray with K Distinct - Two Pointers Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement two pointers technique for K distinct values problems
- Apply sliding window technique for variable-size windows with constraints
- Optimize subarray distinct values calculations using hash maps
- Handle edge cases in K distinct values problems
- Recognize when to use two pointers vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Two pointers, sliding window, hash maps, distinct values
- **Data Structures**: Arrays, hash maps, sets
- **Mathematical Concepts**: Subarray distinct values optimization, window management
- **Programming Skills**: Array manipulation, two pointers implementation
- **Related Problems**: Subarray distinct values, longest substring without repeating, sliding window problems

## 📋 Problem Description

Given an array of integers and a value k, find the length of the longest contiguous subarray that contains exactly k distinct values.

**Input**: 
- First line: n (number of elements) and k (number of distinct values)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: length of longest subarray with exactly k distinct values

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ k ≤ n
- 1 ≤ arr[i] ≤ 10⁵

**Example**:
```
Input:
6 2
1 2 3 2 1 4

Output:
4

Explanation**: 
The subarray [2, 3, 2, 1] has exactly 2 distinct values [2, 3, 1] but contains 3 distinct values.
The subarray [3, 2, 1, 4] has exactly 2 distinct values [3, 2, 1] but contains 3 distinct values.
The subarray [2, 3, 2, 1] has exactly 2 distinct values [2, 3, 1] but contains 3 distinct values.
Wait, let me recalculate: [2, 3, 2, 1] has distinct values [2, 3, 1] = 3 distinct values ≠ 2
The subarray [2, 3, 2] has exactly 2 distinct values [2, 3] and length 3.
The subarray [3, 2, 1] has exactly 2 distinct values [3, 2, 1] but contains 3 distinct values.
The subarray [2, 1, 4] has exactly 2 distinct values [2, 1, 4] but contains 3 distinct values.
Actually, let me fix the example:
```

Let me fix the example:

**Example**:
```
Input:
6 2
1 2 3 2 1 4

Output:
3

Explanation**: 
The subarray [2, 3, 2] has exactly 2 distinct values [2, 3] and length 3.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n³)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each starting position i from 0 to n-1
2. For each ending position j from i to n-1
3. Check if subarray from i to j has exactly k distinct values
4. If yes, update maximum length
5. Return maximum length

**Implementation**:
```python
def brute_force_subarray_with_k_distinct(arr, k):
    n = len(arr)
    max_length = 0
    
    for i in range(n):
        for j in range(i, n):
            subarray = arr[i:j+1]
            if len(set(subarray)) == k:
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
5. If hash map size equals k, update maximum length
6. Return maximum length

**Implementation**:
```python
def optimized_subarray_with_k_distinct(arr, k):
    n = len(arr)
    max_length = 0
    
    for i in range(n):
        distinct_values = set()
        for j in range(i, n):
            distinct_values.add(arr[j])
            if len(distinct_values) == k:
                max_length = max(max_length, j - i + 1)
    
    return max_length
```

### Approach 3: Optimal with Two Pointers
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use two pointers: left and right
2. Use hash map to track frequency of values in current window
3. Expand right pointer while maintaining at most k distinct values
4. When more than k distinct values, contract left pointer
5. Update maximum length when exactly k distinct values
6. Return maximum length

**Implementation**:
```python
def optimal_subarray_with_k_distinct(arr, k):
    n = len(arr)
    left = 0
    max_length = 0
    value_count = {}
    
    for right in range(n):
        value_count[arr[right]] = value_count.get(arr[right], 0) + 1
        
        while len(value_count) > k:
            value_count[arr[left]] -= 1
            if value_count[arr[left]] == 0:
                del value_count[arr[left]]
            left += 1
        
        if len(value_count) == k:
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
- **Window Management**: Expand when <= k distinct, contract when > k distinct
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Two Pointers Technique**: The standard approach for K distinct values problems
- **Sliding Window**: Maintain a window with at most k distinct values
- **Hash Map Tracking**: Use hash map to track value frequencies efficiently
- **Window Management**: Expand and contract window based on distinct count
- **Pattern Recognition**: This technique applies to many K distinct values problems