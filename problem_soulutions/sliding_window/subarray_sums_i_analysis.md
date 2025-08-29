---
layout: simple
title: "Subarray Sums I"
permalink: /cses-analyses/problem_soulutions/sliding_window/subarray_sums_i_analysis
---


# Subarray Sums I

## Problem Statement
Given an array of n integers, your task is to find the number of subarrays with sum x.

### Input
The first input line has two integers n and x: the size of the array and the required sum.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the number of subarrays with sum x.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- −10^9 ≤ x,ai ≤ 10^9

### Example
```
Input:
5 7
2 -1 3 5 -2

Output:
2
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n²)
**Description**: Check all possible subarrays to find those with sum x.

```python
def subarray_sums_naive(n, x, arr):
    count = 0
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == x:
                count += 1
    
    return count
```

**Why this is inefficient**: Quadratic time complexity for large arrays.

### Improvement 1: Prefix Sum with Hash Map - O(n)
**Description**: Use prefix sum and hash map to find subarrays with target sum.

```python
def subarray_sums_prefix_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count
```

**Why this improvement works**: Prefix sum allows us to find subarrays with target sum in constant time using hash map.

### Alternative: Sliding Window (for positive numbers) - O(n)
**Description**: Use sliding window technique for arrays with positive numbers.

```python
def subarray_sums_sliding_window(n, x, arr):
    # This works only for positive numbers
    left = 0
    current_sum = 0
    count = 0
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum > x and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == x:
            count += 1
    
    return count
```

**Why this works**: Sliding window efficiently finds subarrays with target sum for positive numbers.

## Final Optimal Solution

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

def subarray_sums_prefix_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        count += sum_count[prefix_sum - x]
        sum_count[prefix_sum] += 1
    
    return count

result = subarray_sums_prefix_sum(n, x, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n²) | O(1) | Check all subarrays |
| Prefix Sum | O(n) | O(n) | Use hash map for prefix sums |
| Sliding Window | O(n) | O(1) | For positive numbers only |

## Key Insights for Other Problems

### 1. **Subarray Sum Problems**
**Principle**: Use prefix sum and hash map to efficiently find subarrays with target sum.
**Applicable to**:
- Subarray sum problems
- Range sum queries
- Two pointer problems
- Hash map applications

**Example Problems**:
- Subarray sum problems
- Range sum queries
- Two pointer problems
- Hash map applications

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

### 3. **Hash Map for Frequency**
**Principle**: Use hash map to track frequency of prefix sums for efficient lookup.
**Applicable to**:
- Frequency counting
- Hash map applications
- Algorithm design
- Problem solving

**Example Problems**:
- Frequency counting
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
def find_subarrays_with_sum(arr, target):
    from collections import defaultdict
    
    prefix_sum = 0
    count = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1
    
    for num in arr:
        prefix_sum += num
        count += sum_count[prefix_sum - target]
        sum_count[prefix_sum] += 1
    
    return count
```

### 2. **Sliding Window Pattern**
```python
def sliding_window_subarray_sum(arr, target):
    left = 0
    current_sum = 0
    count = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > target and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == target:
            count += 1
    
    return count
```

### 3. **Two Pointer Technique**
```python
def two_pointer_subarray_sum(arr, target):
    left = 0
    current_sum = 0
    count = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right: if current_sum == 
target: count += 1
            current_sum -= arr[left]
            left += 1
    
    return count
```

## Edge Cases to Remember

1. **Empty subarray**: Consider sum 0
2. **Negative numbers**: Use prefix sum approach
3. **Zero target**: Handle carefully
4. **Large numbers**: Use appropriate data types
5. **No valid subarrays**: Return 0

## Problem-Solving Framework

1. **Identify subarray nature**: This is a subarray sum problem
2. **Choose approach**: Use prefix sum with hash map for efficiency
3. **Track prefix sums**: Maintain running sum and frequency
4. **Count subarrays**: Use hash map to find target sum differences
5. **Return result**: Return the count of valid subarrays

---

*This analysis shows how to efficiently find subarrays with target sum using prefix sum and hash map techniques.*