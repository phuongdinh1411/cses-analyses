---
layout: simple
title: "Subarray Minimums - Sliding Window with Deque"
permalink: /problem_soulutions/sliding_window/subarray_minimums_analysis
---

# Subarray Minimums - Sliding Window with Deque

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement deque technique for sliding window minimum problems
- Apply sliding window technique for fixed-size windows with minimum tracking
- Optimize subarray minimum calculations using deque data structure
- Handle edge cases in sliding window minimum problems
- Recognize when to use deque vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sliding window, deque, monotonic data structures
- **Data Structures**: Arrays, deques, stacks
- **Mathematical Concepts**: Subarray minimum optimization, window management
- **Programming Skills**: Array manipulation, deque implementation
- **Related Problems**: Subarray maximums, sliding window problems, monotonic stack

## 📋 Problem Description

Given an array of integers and a window size k, find the minimum element in each sliding window of size k.

**Input**: 
- First line: n (number of elements) and k (window size)
- Second line: n integers separated by spaces

**Output**: 
- n-k+1 integers: minimum element in each sliding window

**Constraints**:
- 1 ≤ k ≤ n ≤ 10⁵
- 1 ≤ arr[i] ≤ 10⁵

**Example**:
```
Input:
6 3
1 3 -1 -3 5 3

Output:
-1 -3 -3 -3

Explanation**: 
Window 1: [1, 3, -1] → min = -1
Window 2: [3, -1, -3] → min = -3
Window 3: [-1, -3, 5] → min = -3
Window 4: [-3, 5, 3] → min = -3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n×k)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each window position i from 0 to n-k
2. Find minimum element in window [i, i+k-1]
3. Add minimum to result
4. Return result

**Implementation**:
```python
def brute_force_subarray_minimums(arr, k):
    n = len(arr)
    result = []
    
    for i in range(n - k + 1):
        window_min = min(arr[i:i+k])
        result.append(window_min)
    
    return result
```

### Approach 2: Optimized with Priority Queue
**Time Complexity**: O(n log k)  
**Space Complexity**: O(k)

**Algorithm**:
1. Use priority queue (min heap) to track elements in current window
2. For each window, add new element and remove old element
3. Get minimum from priority queue
4. Add minimum to result
5. Return result

**Implementation**:
```python
import heapq

def optimized_subarray_minimums(arr, k):
    n = len(arr)
    result = []
    min_heap = []
    
    for i in range(n):
        heapq.heappush(min_heap, arr[i])
        
        if i >= k - 1:
            result.append(min_heap[0])
            min_heap.remove(arr[i - k + 1])
            heapq.heapify(min_heap)
    
    return result
```

### Approach 3: Optimal with Deque
**Time Complexity**: O(n)  
**Space Complexity**: O(k)

**Algorithm**:
1. Use deque to maintain indices of elements in increasing order
2. For each element, remove indices of larger elements from back
3. Add current index to back of deque
4. Remove indices outside current window from front
5. Add minimum (front of deque) to result
6. Return result

**Implementation**:
```python
from collections import deque

def optimal_subarray_minimums(arr, k):
    n = len(arr)
    result = []
    dq = deque()
    
    for i in range(n):
        # Remove indices of larger elements from back
        while dq and arr[dq[-1]] >= arr[i]:
            dq.pop()
        
        # Add current index to back
        dq.append(i)
        
        # Remove indices outside current window from front
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Add minimum to result when window is complete
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n×k) | O(1) | Check all elements in each window |
| Optimized | O(n log k) | O(k) | Use priority queue for minimum tracking |
| Optimal | O(n) | O(k) | Use deque to maintain increasing order |

### Time Complexity
- **Time**: O(n) - Each element is added and removed at most once
- **Space**: O(k) - Deque stores at most k elements

### Why This Solution Works
- **Deque Technique**: Use deque to maintain indices in increasing order
- **Monotonic Property**: Keep only elements that can be minimum in future windows
- **Window Management**: Remove elements outside current window
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Deque Technique**: The standard approach for sliding window minimum problems
- **Monotonic Data Structure**: Use deque to maintain increasing order
- **Window Management**: Efficiently remove elements outside current window
- **Space Optimization**: Use indices instead of values to save space
- **Pattern Recognition**: This technique applies to many sliding window minimum problems