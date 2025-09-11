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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Sliding Window Maximum**
**Problem**: Find the maximum element in each sliding window of size k.

**Key Differences**: General sliding window maximum problem

**Solution Approach**: Use deque to maintain decreasing order

**Implementation**:
```python
def sliding_window_maximum(nums, k):
    """
    Find maximum element in each sliding window of size k
    """
    if not nums or k == 0:
        return []
    
    from collections import deque
    dq = deque()  # Store indices
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices of elements smaller than current
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # Add maximum to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Example usage
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = sliding_window_maximum(nums, k)
print(f"Sliding window maximums: {result}")  # Output: [3, 3, 5, 5, 6, 7]
```

#### **2. Sliding Window Minimum**
**Problem**: Find the minimum element in each sliding window of size k.

**Key Differences**: Minimum instead of maximum

**Solution Approach**: Use deque to maintain increasing order

**Implementation**:
```python
def sliding_window_minimum(nums, k):
    """
    Find minimum element in each sliding window of size k
    """
    if not nums or k == 0:
        return []
    
    from collections import deque
    dq = deque()  # Store indices
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices of elements larger than current
        while dq and nums[dq[-1]] >= nums[i]:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # Add minimum to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Example usage
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = sliding_window_minimum(nums, k)
print(f"Sliding window minimums: {result}")  # Output: [-1, -3, -3, -3, 3, 3]
```

#### **3. Sliding Window Median**
**Problem**: Find the median element in each sliding window of size k.

**Key Differences**: Median instead of maximum/minimum

**Solution Approach**: Use two heaps to maintain median

**Implementation**:
```python
def sliding_window_median(nums, k):
    """
    Find median element in each sliding window of size k
    """
    import heapq
    
    def get_median(max_heap, min_heap, k):
        if k % 2 == 1:
            return -max_heap[0][0]
        else:
            return (-max_heap[0][0] + min_heap[0][0]) / 2
    
    max_heap = []  # Max heap (use negative values)
    min_heap = []  # Min heap
    result = []
    
    for i in range(len(nums)):
        # Add current element
        if not max_heap or nums[i] <= -max_heap[0][0]:
            heapq.heappush(max_heap, (-nums[i], i))
        else:
            heapq.heappush(min_heap, (nums[i], i))
        
        # Balance heaps
        if len(max_heap) > len(min_heap) + 1:
            val, idx = heapq.heappop(max_heap)
            heapq.heappush(min_heap, (-val, idx))
        elif len(min_heap) > len(max_heap) + 1:
            val, idx = heapq.heappop(min_heap)
            heapq.heappush(max_heap, (-val, idx))
        
        # Remove elements outside window
        while max_heap and max_heap[0][1] <= i - k:
            heapq.heappop(max_heap)
        while min_heap and min_heap[0][1] <= i - k:
            heapq.heappop(min_heap)
        
        # Add median to result when window is complete
        if i >= k - 1:
            result.append(get_median(max_heap, min_heap, k))
    
    return result

# Example usage
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = sliding_window_median(nums, k)
print(f"Sliding window medians: {result}")  # Output: [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
```

### Related Problems

#### **CSES Problems**
- [Sliding Window Advertisement](https://cses.fi/problemset/task/2101) - Find maximum impressions in sliding window
- [Sliding Window Maximum](https://cses.fi/problemset/task/2102) - Find maximum element in sliding window
- [Sliding Window Minimum](https://cses.fi/problemset/task/2103) - Find minimum element in sliding window

#### **LeetCode Problems**
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) - Classic sliding window maximum
- [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) - Median in sliding window
- [Maximum Sum of 3 Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/) - Multiple subarrays
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) - K distinct characters

#### **Problem Categories**
- **Sliding Window**: Window maximum/minimum, window statistics, window optimization
- **Deque**: Monotonic data structure, efficient window management
- **Heap**: Window median, priority queue operations
- **Array Processing**: Window operations, element tracking, statistics

## 🚀 Key Takeaways

- **Deque Technique**: The standard approach for sliding window maximum problems
- **Monotonic Data Structure**: Use deque to maintain decreasing order
- **Window Management**: Efficiently remove impressions outside current window
- **Space Optimization**: Use indices instead of values to save space
- **Pattern Recognition**: This technique applies to many sliding window maximum problems