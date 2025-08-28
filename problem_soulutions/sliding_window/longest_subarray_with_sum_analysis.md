---
layout: simple
title: CSES Longest Subarray with Sum - Problem Analysis
permalink: /problem_soulutions/sliding_window/longest_subarray_with_sum_analysis/
---

# CSES Longest Subarray with Sum - Problem Analysis

## Problem Statement
Given an array of n integers, your task is to find the length of the longest subarray with sum x.

### Input
The first input line has two integers n and x: the size of the array and the required sum.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the length of the longest subarray with sum x, or -1 if no such subarray exists.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- −10^9 ≤ x,ai ≤ 10^9

### Example
```
Input:
5 7
2 -1 3 5 -2

Output:
3
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n²)
**Description**: Check all possible subarrays to find the longest one with sum x.

```python
def longest_subarray_naive(n, x, arr):
    max_length = -1
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == x:
                max_length = max(max_length, j - i + 1)
    
    return max_length
```

**Why this is inefficient**: Quadratic time complexity for large arrays.

### Improvement 1: Prefix Sum with Hash Map - O(n)
**Description**: Use prefix sum and hash map to find the longest subarray with target sum.

```python
def longest_subarray_prefix_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1  # Empty subarray has sum 0 at index -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in sum_indices:
            length = i - sum_indices[prefix_sum - x]
            max_length = max(max_length, length)
        
        # Only update if we haven't seen this prefix sum before
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length
```

**Why this improvement works**: Prefix sum allows us to find subarrays with target sum in constant time using hash map.

### Alternative: Sliding Window (for positive numbers) - O(n)
**Description**: Use sliding window technique for arrays with positive numbers.

```python
def longest_subarray_sliding_window(n, x, arr):
    # This works only for positive numbers
    left = 0
    current_sum = 0
    max_length = -1
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum > x and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == x:
            max_length = max(max_length, right - left + 1)
    
    return max_length
```

**Why this works**: Sliding window efficiently finds the longest subarray with target sum for positive numbers.

## Final Optimal Solution

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

def longest_subarray_prefix_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1  # Empty subarray has sum 0 at index -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in sum_indices:
            length = i - sum_indices[prefix_sum - x]
            max_length = max(max_length, length)
        
        # Only update if we haven't seen this prefix sum before
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length

result = longest_subarray_prefix_sum(n, x, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n²) | O(1) | Check all subarrays |
| Prefix Sum | O(n) | O(n) | Use hash map for prefix sums |
| Sliding Window | O(n) | O(1) | For positive numbers only |

## Key Insights for Other Problems

### 1. **Longest Subarray Problems**
**Principle**: Use prefix sum and hash map to efficiently find the longest subarray with target sum.
**Applicable to**:
- Longest subarray problems
- Subarray sum problems
- Hash map applications
- Algorithm design

**Example Problems**:
- Longest subarray problems
- Subarray sum problems
- Hash map applications
- Algorithm design

### 2. **Prefix Sum Technique**
**Principle**: Use prefix sum to convert range queries to point queries.
**Applicable to**:
- Range sum problems
- Subarray problems
- Cumulative sum problems
- Algorithm design

**Example Problems**:
- Range sum problems
- Subarray problems
- Cumulative sum problems
- Algorithm design

### 3. **Hash Map for Index Tracking**
**Principle**: Use hash map to track the first occurrence of each prefix sum for longest subarray.
**Applicable to**:
- Index tracking
- Hash map applications
- Algorithm design
- Problem solving

**Example Problems**:
- Index tracking
- Hash map applications
- Algorithm design
- Problem solving

### 4. **Sliding Window Applications**
**Principle**: Use sliding window for problems involving contiguous subarrays with constraints.
**Applicable to**:
- Contiguous subarray problems
- Two pointer problems
- Window-based problems
- Algorithm design

**Example Problems**:
- Contiguous subarray problems
- Two pointer problems
- Window-based problems
- Algorithm design

## Notable Techniques

### 1. **Prefix Sum with Hash Map Pattern**
```python
def find_longest_subarray_with_sum(arr, target):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1
    
    for i in range(len(arr)):
        prefix_sum += arr[i]
        
        if prefix_sum - target in sum_indices:
            length = i - sum_indices[prefix_sum - target]
            max_length = max(max_length, length)
        
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length
```

### 2. **Sliding Window Pattern**
```python
def sliding_window_longest_subarray(arr, target):
    left = 0
    current_sum = 0
    max_length = -1
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > target and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == target:
            max_length = max(max_length, right - left + 1)
    
    return max_length
```

### 3. **Two Pointer Technique**
```python
def two_pointer_longest_subarray(arr, target):
    left = 0
    current_sum = 0
    max_length = -1
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right:
            if current_sum == target:
                max_length = max(max_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return max_length
```

## Edge Cases to Remember

1. **No valid subarray**: Return -1
2. **Empty subarray**: Consider sum 0
3. **Negative numbers**: Use prefix sum approach
4. **Zero target**: Handle carefully
5. **Large numbers**: Use appropriate data types

## Problem-Solving Framework

1. **Identify subarray nature**: This is a longest subarray sum problem
2. **Choose approach**: Use prefix sum with hash map for efficiency
3. **Track prefix sums**: Maintain running sum and first occurrence indices
4. **Find longest**: Use hash map to find target sum differences
5. **Return result**: Return the length of longest valid subarray

---

*This analysis shows how to efficiently find the longest subarray with target sum using prefix sum and hash map techniques.* 