---
layout: simple
title: CSES Sliding Window Advertisement - Problem Analysis
permalink: /problem_soulutions/sliding_window/sliding_window_advertisement_analysis/
---

# CSES Sliding Window Advertisement - Problem Analysis

## Problem Statement
Given an array of n integers and a window size k, find the maximum sum of any subarray of size k.

### Input
The first input line has two integers n and k: the size of the array and the window size.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the maximum sum of any subarray of size k.

### Constraints
- 1 ≤ k ≤ n ≤ 2⋅10^5
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
5 3
1 2 3 4 5

Output:
12
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n × k)
**Description**: Check all possible subarrays of size k to find the maximum sum.

```python
def sliding_window_sum_naive(n, k, arr):
    max_sum = float('-inf')
    
    for i in range(n - k + 1):
        current_sum = sum(arr[i:i+k])
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this is inefficient**: For each window, we recalculate the sum from scratch, leading to O(n × k) time complexity.

### Improvement 1: Sliding Window with Running Sum - O(n)
**Description**: Use sliding window technique to maintain a running sum and avoid recalculating.

```python
def sliding_window_sum_optimal(n, k, arr):
    # Calculate sum of first window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Add new element and remove old element
        current_sum = current_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this improvement works**: Instead of recalculating the sum for each window, we maintain a running sum by adding the new element and subtracting the old element.

## Final Optimal Solution

```python
n, k = map(int, input().split())
arr = list(map(int, input().split()))

def sliding_window_sum_optimal(n, k, arr):
    # Calculate sum of first window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Add new element and remove old element
        current_sum = current_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

result = sliding_window_sum_optimal(n, k, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n × k) | O(1) | Recalculate sum for each window |
| Sliding Window | O(n) | O(1) | Maintain running sum |

## Key Insights for Other Problems

### 1. **Fixed Window Size Problems**
**Principle**: Use sliding window to efficiently process fixed-size windows without recalculating.
**Applicable to**: Fixed window problems, subarray problems, sliding window applications

### 2. **Running Sum Technique**
**Principle**: Maintain a running sum/count to avoid recalculating for each window.
**Applicable to**: Sum problems, average problems, sliding window optimizations

### 3. **Window Maintenance**
**Principle**: Add new elements and remove old elements to maintain the current window state.
**Applicable to**: Window-based problems, stream processing, real-time algorithms

## Notable Techniques

### 1. **Sliding Window Sum Pattern**
```python
def sliding_window_sum_pattern(arr, k):
    if len(arr) < k:
        return 0
    
    # Initialize first window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide window
    for i in range(k, len(arr)):
        current_sum = current_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

### 2. **Generic Sliding Window Pattern**
```python
def generic_sliding_window(arr, k):
    if len(arr) < k:
        return 0
    
    # Initialize window
    window_sum = sum(arr[:k])
    result = window_sum
    
    # Slide window
    for i in range(k, len(arr)):
        window_sum = window_sum + arr[i] - arr[i - k]
        result = max(result, window_sum)  # or min, or other operation
    
    return result
```

## Problem-Solving Framework

1. **Identify window size**: This is a fixed-size window problem (size k)
2. **Choose approach**: Use sliding window with running sum for efficiency
3. **Initialize window**: Calculate sum of first k elements
4. **Slide window**: Add new element, remove old element, update result
5. **Return maximum**: Track the maximum sum found

---

*This analysis shows how to efficiently find the maximum sum of any subarray of fixed size k using sliding window technique.* 