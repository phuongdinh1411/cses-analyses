---
layout: simple
title: "Subarray with Given Sum"
permalink: /cses-analyses/problem_soulutions/sliding_window/subarray_with_given_sum_analysis
---


# Subarray with Given Sum

## Problem Statement
Given an array of n integers and a target sum x, your task is to find if there exists a subarray with sum x.

### Input
The first input line has two integers n and x: the size of the array and the target sum.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print "YES" if there exists a subarray with sum x, otherwise print "NO".

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- −10^9 ≤ x,ai ≤ 10^9

### Example
```
Input:
5 7
2 -1 3 5 -2

Output:
YES
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n²)
**Description**: Check all possible subarrays to find one with sum x.

```python
def subarray_with_sum_naive(n, x, arr):
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == x:
                return True
    return False
```

**Why this is inefficient**: Quadratic time complexity for large arrays.

### Improvement 1: Prefix Sum with Hash Set - O(n)
**Description**: Use prefix sum and hash set to find subarray with target sum.

```python
def subarray_with_sum_prefix_sum(n, x, arr):
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in seen_sums:
            return True
        
        seen_sums.add(prefix_sum)
    
    return False
```

**Why this improvement works**: Prefix sum allows us to find subarrays with target sum in constant time using hash set.

### Alternative: Sliding Window (for positive numbers) - O(n)
**Description**: Use sliding window technique for arrays with positive numbers.

```python
def subarray_with_sum_sliding_window(n, x, arr):
    # This works only for positive numbers
    left = 0
    current_sum = 0
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum > x and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == x:
            return True
    
    return False
```

**Why this works**: Sliding window efficiently finds subarrays with target sum for positive numbers.

## Final Optimal Solution

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

def subarray_with_sum_prefix_sum(n, x, arr):
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)  # Empty subarray has sum 0
    
    for num in arr:
        prefix_sum += num
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in seen_sums:
            return True
        
        seen_sums.add(prefix_sum)
    
    return False

result = subarray_with_sum_prefix_sum(n, x, arr)
print("YES" if result else "NO")
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n²) | O(1) | Check all subarrays |
| Prefix Sum | O(n) | O(n) | Use hash set for prefix sums |
| Sliding Window | O(n) | O(1) | For positive numbers only |

## Key Insights for Other Problems

### 1. **Subarray Existence Problems**
**Principle**: Use prefix sum and hash set to efficiently check for subarray existence.
**Applicable to**:
- Subarray existence problems
- Subarray sum problems
- Hash set applications
- Algorithm design

**Example Problems**:
- Subarray existence problems
- Subarray sum problems
- Hash set applications
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

### 3. **Hash Set for Existence**
**Principle**: Use hash set to efficiently check for existence of prefix sums.
**Applicable to**:
- Existence checking
- Hash set applications
- Algorithm design
- Problem solving

**Example Problems**:
- Existence checking
- Hash set applications
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

### 1. **Prefix Sum with Hash Set Pattern**
```python
def check_subarray_exists(arr, target):
    prefix_sum = 0
    seen_sums = set()
    seen_sums.add(0)
    
    for num in arr:
        prefix_sum += num
        
        if prefix_sum - target in seen_sums:
            return True
        
        seen_sums.add(prefix_sum)
    
    return False
```

### 2. **Sliding Window Pattern**
```python
def sliding_window_subarray_exists(arr, target):
    left = 0
    current_sum = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > target and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == target:
            return True
    
    return False
```

### 3. **Two Pointer Technique**
```python
def two_pointer_subarray_exists(arr, target):
    left = 0
    current_sum = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right: if current_sum == 
target: return True
            current_sum -= arr[left]
            left += 1
    
    return False
```

## Edge Cases to Remember

1. **No valid subarray**: Return "NO"
2. **Empty subarray**: Consider sum 0
3. **Negative numbers**: Use prefix sum approach
4. **Zero target**: Handle carefully
5. **Large numbers**: Use appropriate data types

## Problem-Solving Framework

1. **Identify subarray nature**: This is a subarray existence problem
2. **Choose approach**: Use prefix sum with hash set for efficiency
3. **Track prefix sums**: Maintain running sum and seen sums
4. **Check existence**: Use hash set to find target sum differences
5. **Return result**: Return "YES" or "NO" based on existence

---

*This analysis shows how to efficiently check for subarray existence with target sum using prefix sum and hash set techniques.* 