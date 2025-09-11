---
layout: simple
title: "Sliding Window Advertisement - Real-world Application"
permalink: /problem_soulutions/sliding_window/sliding_window_advertisement_analysis
---

# Sliding Window Advertisement - Real-world Application

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement sliding window technique for real-world applications
- Apply sliding window technique for time-based data analysis
- Optimize advertisement placement calculations using sliding window
- Handle edge cases in real-world sliding window problems
- Recognize when to use sliding window vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sliding window, time-based data analysis, optimization
- **Data Structures**: Arrays, queues, time series data
- **Mathematical Concepts**: Time-based optimization, window management
- **Programming Skills**: Array manipulation, sliding window implementation
- **Related Problems**: Fixed length subarray sum, sliding window problems, time series analysis

## 📋 Problem Description

Given a time series of advertisement impressions and a time window, find the maximum number of impressions in any sliding window of the given size.

**Input**: 
- First line: n (number of time points) and k (window size)
- Second line: n integers representing impressions at each time point

**Output**: 
- n-k+1 integers: maximum impressions in each sliding window

**Constraints**:
- 1 ≤ k ≤ n ≤ 10⁵
- 1 ≤ impressions[i] ≤ 10⁵

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
2. Find maximum impressions in window [i, i+k-1]
3. Add maximum to result
4. Return result

**Implementation**:
```python
def brute_force_sliding_window_advertisement(impressions, k):
    n = len(impressions)
    result = []
    
    for i in range(n - k + 1):
        window_max = max(impressions[i:i+k])
        result.append(window_max)
    
    return result
```

### Approach 2: Optimized with Priority Queue
**Time Complexity**: O(n log k)  
**Space Complexity**: O(k)

**Algorithm**:
1. Use priority queue (max heap) to track impressions in current window
2. For each window, add new impression and remove old impression
3. Get maximum from priority queue
4. Add maximum to result
5. Return result

**Implementation**:
```python
import heapq

def optimized_sliding_window_advertisement(impressions, k):
    n = len(impressions)
    result = []
    max_heap = []
    
    for i in range(n):
        heapq.heappush(max_heap, -impressions[i])
        
        if i >= k - 1:
            result.append(-max_heap[0])
            max_heap.remove(-impressions[i - k + 1])
            heapq.heapify(max_heap)
    
    return result
```

### Approach 3: Optimal with Deque
**Time Complexity**: O(n)  
**Space Complexity**: O(k)

**Algorithm**:
1. Use deque to maintain indices of impressions in decreasing order
2. For each impression, remove indices of smaller impressions from back
3. Add current index to back of deque
4. Remove indices outside current window from front
5. Add maximum (front of deque) to result
6. Return result

**Implementation**:
```python
from collections import deque

def optimal_sliding_window_advertisement(impressions, k):
    n = len(impressions)
    result = []
    dq = deque()
    
    for i in range(n):
        # Remove indices of smaller impressions from back
        while dq and impressions[dq[-1]] <= impressions[i]:
            dq.pop()
        
        # Add current index to back
        dq.append(i)
        
        # Remove indices outside current window from front
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Add maximum to result when window is complete
        if i >= k - 1:
            result.append(impressions[dq[0]])
    
    return result
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n×k) | O(1) | Check all impressions in each window |
| Optimized | O(n log k) | O(k) | Use priority queue for maximum tracking |
| Optimal | O(n) | O(k) | Use deque to maintain decreasing order |

### Time Complexity
- **Time**: O(n) - Each impression is added and removed at most once
- **Space**: O(k) - Deque stores at most k elements

### Why This Solution Works
- **Deque Technique**: Use deque to maintain indices in decreasing order
- **Monotonic Property**: Keep only impressions that can be maximum in future windows
- **Window Management**: Remove impressions outside current window
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Key Takeaways

- **Deque Technique**: The standard approach for sliding window maximum problems
- **Monotonic Data Structure**: Use deque to maintain decreasing order
- **Window Management**: Efficiently remove impressions outside current window
- **Space Optimization**: Use indices instead of values to save space
- **Pattern Recognition**: This technique applies to many sliding window maximum problems