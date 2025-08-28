---
layout: simple
title: "Minimum Subarray Sum
permalink: /problem_soulutions/sliding_window/minimum_subarray_sum_analysis/
---

# Minimum Subarray Sum

## Problem Statement
Given an array of n integers, your task is to find the minimum sum of a subarray.

### Input
The first input line has an integer n: the size of the array.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the minimum sum of a subarray.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- −10^9 ≤ ai ≤ 10^9

### Example
```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
-5
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n³)
**Description**: Check all possible subarrays and find the minimum sum.

```python
def min_subarray_sum_naive(n, arr):"
    min_sum = float('inf')
    
    for i in range(n):
        for j in range(i, n):
            current_sum = sum(arr[i:j+1])
            min_sum = min(min_sum, current_sum)
    
    return min_sum
```

**Why this is inefficient**: Cubic time complexity for large arrays.

### Improvement 1: Modified Kadane's Algorithm - O(n)
**Description**: Use modified Kadane's algorithm to find the minimum subarray sum efficiently.

```python
def min_subarray_sum_kadane(n, arr):
    min_so_far = float('inf')
    min_ending_here = 0
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far
```

**Why this improvement works**: Modified Kadane's algorithm efficiently tracks the minimum sum ending at each position.

### Alternative: Sliding Window with Prefix Sum - O(n)
**Description**: Use sliding window with prefix sum to find minimum subarray sum.

```python
def min_subarray_sum_sliding_window(n, arr):
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    min_sum = float('inf')
    max_prefix = 0
    
    for i in range(1, n + 1):
        min_sum = min(min_sum, prefix_sum[i] - max_prefix)
        max_prefix = max(max_prefix, prefix_sum[i])
    
    return min_sum
```

**Why this works**: Prefix sum allows us to find subarray sums efficiently.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

def min_subarray_sum_kadane(n, arr):
    min_so_far = float('inf')
    min_ending_here = 0
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far

result = min_subarray_sum_kadane(n, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n³) | O(1) | Check all subarrays |
| Modified Kadane's | O(n) | O(1) | Track minimum ending at each position |
| Sliding Window | O(n) | O(n) | Use prefix sum |

## Key Insights for Other Problems

### 1. **Minimum Subarray Problems**
**Principle**: Use modified Kadane's algorithm to efficiently find the minimum subarray sum.
**Applicable to**:
- Minimum subarray problems
- Subarray sum problems
- Dynamic programming
- Algorithm design

**Example Problems**:
- Minimum subarray problems
- Subarray sum problems
- Dynamic programming
- Algorithm design

### 2. **Modified Kadane's Algorithm**
**Principle**: Track the minimum sum ending at each position to find the global minimum.
**Applicable to**:
- Subarray sum problems
- Dynamic programming
- Algorithm design
- Problem solving

**Example Problems**:
- Subarray sum problems
- Dynamic programming
- Algorithm design
- Problem solving

### 3. **Prefix Sum Technique**
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

### 4. **Dynamic Programming Applications**
**Principle**: Use dynamic programming to build solutions from smaller subproblems.
**Applicable to**:
- Dynamic programming
- Optimization problems
- Algorithm design
- Problem solving

**Example Problems**:
- Dynamic programming
- Optimization problems
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **Modified Kadane's Algorithm Pattern**
```python
def modified_kadane_algorithm(arr):
    min_so_far = float('inf')
    min_ending_here = 0
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far
```

### 2. **Prefix Sum Pattern**
```python
def prefix_sum_min_subarray(arr):
    n = len(arr)
    prefix_sum = [0] * (n + 1)
    
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    min_sum = float('inf')
    max_prefix = 0
    
    for i in range(1, n + 1):
        min_sum = min(min_sum, prefix_sum[i] - max_prefix)
        max_prefix = max(max_prefix, prefix_sum[i])
    
    return min_sum
```

### 3. **Sliding Window Pattern**
```python
def sliding_window_min_subarray(arr):
    left = 0
    current_sum = 0
    min_sum = float('inf')
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > 0 and left <= right:
            current_sum -= arr[left]
            left += 1
        
        min_sum = min(min_sum, current_sum)
    
    return min_sum
```

## Edge Cases to Remember

1. **All positive numbers**: Return the minimum positive number
2. **All negative numbers**: Return the sum of all elements
3. **Single element**: Return the element itself
4. **Large numbers**: Use appropriate data types
5. **Zero elements**: Handle appropriately

## Problem-Solving Framework

1. **Identify subarray nature**: This is a minimum subarray sum problem
2. **Choose approach**: Use modified Kadane's algorithm for efficiency
3. **Track minimum**: Maintain minimum sum ending at each position
4. **Update global minimum**: Update global minimum when needed
5. **Return result**: Return the minimum subarray sum

---

*This analysis shows how to efficiently find the minimum subarray sum using modified Kadane's algorithm.* 