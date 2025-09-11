---
layout: simple
title: "Subarray Maximums - Sliding Window with Deque"
permalink: /problem_soulutions/sliding_window/subarray_maximums_analysis
---

# Subarray Maximums - Sliding Window with Deque

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement deque technique for sliding window maximum problems
- Apply sliding window technique for fixed-size windows with maximum tracking
- Optimize subarray maximum calculations using deque data structure
- Handle edge cases in sliding window maximum problems
- Recognize when to use deque vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sliding window, deque, monotonic data structures
- **Data Structures**: Arrays, deques, stacks
- **Mathematical Concepts**: Subarray maximum optimization, window management
- **Programming Skills**: Array manipulation, deque implementation
- **Related Problems**: Subarray minimums, sliding window problems, monotonic stack

## 📋 Problem Description

Given an array of integers and a window size k, find the maximum element in each sliding window of size k.

**Input**: 
- First line: n (number of elements) and k (window size)
- Second line: n integers separated by spaces

**Output**: 
- n-k+1 integers: maximum element in each sliding window

**Constraints**:
- 1 ≤ k ≤ n ≤ 10⁵
- 1 ≤ arr[i] ≤ 10⁵

**Example**:
```
Input:
6 3
1 3 -1 -3 5 3

Output:
3 3 5 5

Explanation**: 
Window 1: [1, 3, -1] → max = 3
Window 2: [3, -1, -3] → max = 3
Window 3: [-1, -3, 5] → max = 5
Window 4: [-3, 5, 3] → max = 5
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n×k)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each window position i from 0 to n-k
2. Find maximum element in window [i, i+k-1]
3. Add maximum to result
4. Return result

**Implementation**:
```python
def brute_force_subarray_maximums(arr, k):
    n = len(arr)
    result = []
    
    for i in range(n - k + 1):
        window_max = max(arr[i:i+k])
        result.append(window_max)
    
    return result
```

### Approach 2: Optimized with Priority Queue
**Time Complexity**: O(n log k)  
**Space Complexity**: O(k)

**Algorithm**:
1. Use priority queue (max heap) to track elements in current window
2. For each window, add new element and remove old element
3. Get maximum from priority queue
4. Add maximum to result
5. Return result

**Implementation**:
```python
import heapq

def optimized_subarray_maximums(arr, k):
    n = len(arr)
    result = []
    max_heap = []
    
    for i in range(n):
        heapq.heappush(max_heap, -arr[i])
        
        if i >= k - 1:
            result.append(-max_heap[0])
            max_heap.remove(-arr[i - k + 1])
            heapq.heapify(max_heap)
    
    return result
```

### Approach 3: Optimal with Deque
**Time Complexity**: O(n)  
**Space Complexity**: O(k)

**Algorithm**:
1. Use deque to maintain indices of elements in decreasing order
2. For each element, remove indices of smaller elements from back
3. Add current index to back of deque
4. Remove indices outside current window from front
5. Add maximum (front of deque) to result
6. Return result

**Implementation**:
```python
from collections import deque

def optimal_subarray_maximums(arr, k):
    n = len(arr)
    result = []
    dq = deque()
    
    for i in range(n):
        # Remove indices of smaller elements from back
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        
        # Add current index to back
        dq.append(i)
        
        # Remove indices outside current window from front
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Add maximum to result when window is complete
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n×k) | O(1) | Check all elements in each window |
| Optimized | O(n log k) | O(k) | Use priority queue for maximum tracking |
| Optimal | O(n) | O(k) | Use deque to maintain decreasing order |

### Time Complexity
- **Time**: O(n) - Each element is added and removed at most once
- **Space**: O(k) - Deque stores at most k elements

### Why This Solution Works
- **Deque Technique**: Use deque to maintain indices in decreasing order
- **Monotonic Property**: Keep only elements that can be maximum in future windows
- **Window Management**: Remove elements outside current window
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Deque Technique**: The standard approach for sliding window maximum problems
- **Monotonic Data Structure**: Use deque to maintain decreasing order
- **Window Management**: Efficiently remove elements outside current window
- **Space Optimization**: Use indices instead of values to save space
- **Pattern Recognition**: This technique applies to many sliding window maximum problems