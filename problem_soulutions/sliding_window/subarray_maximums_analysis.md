---
layout: simple
title: "Subarray Maximums
permalink: /problem_soulutions/sliding_window/subarray_maximums_analysis/
---

# Subarray Maximums

## Problem Statement
Given an array of n integers, your task is to find the sum of maximums of all subarrays.

### Input
The first input line has an integer n: the size of the array.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the sum of maximums of all subarrays.

### Constraints
- 1 ≤ n ≤ 3⋅10^5
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
4
3 1 2 4

Output:
23
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n³)
**Description**: Check all possible subarrays and find the maximum of each.

```python
def subarray_maximums_naive(n, arr):
    total_sum = 0
    
    for i in range(n):
        for j in range(i, n):
            max_val = max(arr[i:j+1])
            total_sum += max_val
    
    return total_sum
```

**Why this is inefficient**: Cubic time complexity for large arrays.

### Improvement 1: Monotonic Stack - O(n)
**Description**: Use monotonic stack to find the contribution of each element as maximum.

```python
def subarray_maximums_monotonic_stack(n, arr):
    stack = []
    left = [-1] * n  # Previous larger element to the left
    right = [n] * n  # Next larger element to the right
    
    # Find previous larger elements
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    
    # Clear stack for next pass
    stack.clear()
    
    # Find next larger elements
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
    
    # Calculate contribution of each element
    total_sum = 0
    for i in range(n):
        # Number of subarrays where arr[i] is the maximum
        count = (i - left[i]) * (right[i] - i)
        total_sum += arr[i] * count
    
    return total_sum
```

**Why this improvement works**: Monotonic stack efficiently finds the range where each element is the maximum.

### Alternative: Sliding Window with Deque - O(n)
**Description**: Use sliding window with deque to find maximums in each window.

```python
def subarray_maximums_sliding_window(n, arr):
    from collections import deque
    
    total_sum = 0
    
    for window_size in range(1, n + 1):
        dq = deque()
        
        # Process first window
        for i in range(window_size):
            while dq and arr[dq[-1]] <= arr[i]:
                dq.pop()
            dq.append(i)
        
        # Process remaining windows
        for i in range(window_size, n):
            total_sum += arr[dq[0]]  # Maximum of previous window
            
            # Remove elements outside current window
            while dq and dq[0] <= i - window_size:
                dq.popleft()
            
            # Add current element
            while dq and arr[dq[-1]] <= arr[i]:
                dq.pop()
            dq.append(i)
        
        # Add maximum of last window
        if dq:
            total_sum += arr[dq[0]]
    
    return total_sum
```

**Why this works**: Sliding window with deque efficiently finds maximums in each window size.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

def subarray_maximums_monotonic_stack(n, arr):
    stack = []
    left = [-1] * n  # Previous larger element to the left
    right = [n] * n  # Next larger element to the right
    
    # Find previous larger elements
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    
    # Clear stack for next pass
    stack.clear()
    
    # Find next larger elements
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
    
    # Calculate contribution of each element
    total_sum = 0
    for i in range(n):
        # Number of subarrays where arr[i] is the maximum
        count = (i - left[i]) * (right[i] - i)
        total_sum += arr[i] * count
    
    return total_sum

result = subarray_maximums_monotonic_stack(n, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n³) | O(1) | Check all subarrays |
| Monotonic Stack | O(n) | O(n) | Use stack for range finding |
| Sliding Window | O(n²) | O(n) | Use deque for window maximums |

## Key Insights for Other Problems

### 1. **Subarray Maximum Problems**
**Principle**: Use monotonic stack to efficiently find the range where each element is the maximum.
**Applicable to**:
- Subarray maximum problems
- Range maximum queries
- Monotonic stack applications
- Algorithm design

**Example Problems**:
- Subarray maximum problems
- Range maximum queries
- Monotonic stack applications
- Algorithm design

### 2. **Monotonic Stack Technique**
**Principle**: Use monotonic stack to maintain elements in sorted order for efficient range queries.
**Applicable to**:
- Range queries
- Next/previous larger/smaller elements
- Algorithm design
- Problem solving

**Example Problems**:
- Range queries
- Next/previous larger/smaller elements
- Algorithm design
- Problem solving

### 3. **Contribution Analysis**
**Principle**: Analyze how much each element contributes to the final result.
**Applicable to**:
- Sum problems
- Contribution analysis
- Algorithm design
- Problem solving

**Example Problems**:
- Sum problems
- Contribution analysis
- Algorithm design
- Problem solving

### 4. **Sliding Window with Deque**
**Principle**: Use deque to efficiently maintain minimum/maximum in sliding windows.
**Applicable to**:
- Window-based problems
- Deque applications
- Algorithm design
- Problem solving

**Example Problems**:
- Window-based problems
- Deque applications
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **Monotonic Stack Pattern**
```python
def monotonic_stack_range_finding(arr):
    n = len(arr)
    stack = []
    left = [-1] * n
    right = [n] * n
    
    # Find previous larger elements
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    
    # Find next larger elements
    stack.clear()
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
    
    return left, right
```

### 2. **Sliding Window with Deque Pattern**
```python
def sliding_window_maximum(arr, k):
    from collections import deque
    
    dq = deque()
    result = []
    
    for i in range(len(arr)):
        # Remove elements outside window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove smaller elements from back
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result
```

### 3. **Contribution Calculation Pattern**
```python
def calculate_element_contribution(arr, left, right):
    total_contribution = 0
    
    for i in range(len(arr)):
        # Count subarrays where arr[i] is maximum
        count = (i - left[i]) * (right[i] - i)
        total_contribution += arr[i] * count
    
    return total_contribution
```

## Edge Cases to Remember

1. **All same elements**: Each element contributes equally
2. **Strictly decreasing**: Each element is maximum of its own subarray
3. **Strictly increasing**: Last element is maximum of all subarrays
4. **Single element**: Return the element itself
5. **Large numbers**: Use appropriate data types

## Problem-Solving Framework

1. **Identify maximum nature**: This is a subarray maximum problem
2. **Choose approach**: Use monotonic stack for efficiency
3. **Find ranges**: Find where each element is the maximum
4. **Calculate contribution**: Count subarrays where each element is maximum
5. **Sum contributions**: Return the total sum

---

*This analysis shows how to efficiently find the sum of maximums of all subarrays using monotonic stack technique.*"