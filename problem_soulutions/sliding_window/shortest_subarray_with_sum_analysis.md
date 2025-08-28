---
layout: simple
title: "Shortest Subarray with Sum"permalink: /problem_soulutions/sliding_window/shortest_subarray_with_sum_analysis
---


# Shortest Subarray with Sum

## Problem Statement
Given an array of n integers, your task is to find the length of the shortest subarray with sum at least x.

### Input
The first input line has two integers n and x: the size of the array and the required sum.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the length of the shortest subarray with sum at least x, or -1 if no such subarray exists.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ x,ai ≤ 10^9

### Example
```
Input:
5 7
2 1 3 5 2

Output:
2
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n²)
**Description**: Check all possible subarrays to find the shortest one with sum at least x.

```python
def shortest_subarray_naive(n, x, arr):
    min_length = float('inf')
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum >= x:
                min_length = min(min_length, j - i + 1)
                break
    
    return min_length if min_length != float('inf') else -1
```

**Why this is inefficient**: Quadratic time complexity for large arrays.

### Improvement 1: Sliding Window - O(n)
**Description**: Use sliding window technique to find the shortest subarray with sum at least x.

```python
def shortest_subarray_sliding_window(n, x, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Shrink window while sum is at least x
        while current_sum >= x and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1
```

**Why this improvement works**: Sliding window efficiently maintains the constraint of sum at least x.

### Alternative: Binary Search with Prefix Sum - O(n log n)
**Description**: Use binary search with prefix sum to find the shortest subarray.

```python
def shortest_subarray_binary_search(n, x, arr):
    def check_length(length):
        # Check if there exists a subarray of given length with sum >= x
        current_sum = sum(arr[:length])
        if current_sum >= x:
            return True
        
        for i in range(length, n):
            current_sum = current_sum - arr[i - length] + arr[i]
            if current_sum >= x:
                return True
        
        return False
    
    # Binary search on the answer
    left, right = 1, n
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if check_length(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    
    return result
```

**Why this works**: Binary search efficiently finds the shortest valid length.

## Final Optimal Solution

```python
n, x = map(int, input().split())
arr = list(map(int, input().split()))

def shortest_subarray_sliding_window(n, x, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Shrink window while sum is at least x
        while current_sum >= x and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1

result = shortest_subarray_sliding_window(n, x, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n²) | O(1) | Check all subarrays |
| Sliding Window | O(n) | O(1) | Use sliding window |
| Binary Search | O(n log n) | O(1) | Binary search on answer |

## Key Insights for Other Problems

### 1. **Shortest Subarray Problems**
**Principle**: Use sliding window to efficiently find the shortest subarray satisfying constraints.
**Applicable to**:
- Shortest subarray problems
- Subarray sum problems
- Window-based problems
- Algorithm design

**Example Problems**:
- Shortest subarray problems
- Subarray sum problems
- Window-based problems
- Algorithm design

### 2. **Sliding Window Technique**
**Principle**: Use sliding window to maintain constraints while expanding and contracting the window.
**Applicable to**:
- Window-based problems
- Subarray problems
- Two pointer problems
- Algorithm design

**Example Problems**:
- Window-based problems
- Subarray problems
- Two pointer problems
- Algorithm design

### 3. **Binary Search on Answer**
**Principle**: Use binary search to find the optimal answer when direct computation is expensive.
**Applicable to**:
- Optimization problems
- Binary search applications
- Algorithm design
- Problem solving

**Example Problems**:
- Optimization problems
- Binary search applications
- Algorithm design
- Problem solving

### 4. **Two Pointer Applications**
**Principle**: Use two pointers to maintain a valid window that satisfies the given constraints.
**Applicable to**:
- Two pointer problems
- Window-based problems
- Subarray problems
- Algorithm design

**Example Problems**:
- Two pointer problems
- Window-based problems
- Subarray problems
- Algorithm design

## Notable Techniques

### 1. **Sliding Window Pattern**
```python
def sliding_window_shortest_subarray(arr, target):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1
```

### 2. **Binary Search on Answer Pattern**
```python
def binary_search_on_answer(arr, target):
    def check_length(length):
        # Check if length is valid
        pass
    
    left, right = 1, len(arr)
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if check_length(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    
    return result
```

### 3. **Two Pointer Technique**
```python
def two_pointer_shortest_subarray(arr, target):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1
```

## Edge Cases to Remember

1. **No valid subarray**: Return -1
2. **Single element**: Check if it's >= x
3. **All elements < x**: Return -1
4. **Sum of all elements < x**: Return -1
5. **Large numbers**: Use appropriate data types

## Problem-Solving Framework

1. **Identify subarray nature**: This is a shortest subarray sum problem
2. **Choose approach**: Use sliding window for efficiency
3. **Maintain constraint**: Keep sum >= x while minimizing length
4. **Track minimum**: Update minimum length when constraint is satisfied
5. **Return result**: Return the shortest valid length

---

*This analysis shows how to efficiently find the shortest subarray with sum at least x using sliding window technique.* 