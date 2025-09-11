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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Subarray Minimums with Range Updates**
**Problem**: Find minimum element in each subarray of size k, with range update operations.

**Key Differences**: Array can be updated between queries

**Solution Approach**: Use segment tree with lazy propagation

**Implementation**:
```python
def subarray_minimums_with_updates(arr, k, updates):
    """
    Find minimum element in each subarray of size k with range updates
    """
    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [float('inf')] * (4 * self.n)
            self.lazy = [0] * (4 * self.n)
            self.build(arr, 0, 0, self.n - 1)
        
        def build(self, arr, node, start, end):
            if start == end:
                self.tree[node] = arr[start]
            else:
                mid = (start + end) // 2
                self.build(arr, 2 * node + 1, start, mid)
                self.build(arr, 2 * node + 2, mid + 1, end)
                self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])
        
        def update_range(self, node, start, end, l, r, val):
            if self.lazy[node] != 0:
                self.tree[node] += self.lazy[node]
                if start != end:
                    self.lazy[2 * node + 1] += self.lazy[node]
                    self.lazy[2 * node + 2] += self.lazy[node]
                self.lazy[node] = 0
            
            if start > end or start > r or end < l:
                return
            
            if start >= l and end <= r:
                self.tree[node] += val
                if start != end:
                    self.lazy[2 * node + 1] += val
                    self.lazy[2 * node + 2] += val
            else:
                mid = (start + end) // 2
                self.update_range(2 * node + 1, start, mid, l, r, val)
                self.update_range(2 * node + 2, mid + 1, end, l, r, val)
                self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])
        
        def query_range(self, node, start, end, l, r):
            if start > end or start > r or end < l:
                return float('inf')
            
            if self.lazy[node] != 0:
                self.tree[node] += self.lazy[node]
                if start != end:
                    self.lazy[2 * node + 1] += self.lazy[node]
                    self.lazy[2 * node + 2] += self.lazy[node]
                self.lazy[node] = 0
            
            if start >= l and end <= r:
                return self.tree[node]
            
            mid = (start + end) // 2
            return min(
                self.query_range(2 * node + 1, start, mid, l, r),
                self.query_range(2 * node + 2, mid + 1, end, l, r)
            )
    
    st = SegmentTree(arr)
    results = []
    
    for update in updates:
        if update[0] == 'update':
            l, r, val = update[1], update[2], update[3]
            st.update_range(0, 0, st.n - 1, l, r, val)
        else:  # query
            results.append(st.query_range(0, 0, st.n - 1, 0, k - 1))
    
    return results

# Example usage
arr = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
updates = [('query',), ('update', 0, 2, 2), ('query',)]
result = subarray_minimums_with_updates(arr, k, updates)
print(f"Subarray minimums with updates: {result}")
```

#### **2. Subarray Minimums with Frequency**
**Problem**: Find minimum element in each subarray of size k, along with its frequency.

**Key Differences**: Also track frequency of minimum element

**Solution Approach**: Use deque with frequency tracking

**Implementation**:
```python
def subarray_minimums_with_frequency(arr, k):
    """
    Find minimum element and its frequency in each subarray of size k
    """
    from collections import deque
    
    dq = deque()  # Store (value, frequency) pairs
    result = []
    
    for i in range(len(arr)):
        # Remove elements outside current window
        while dq and dq[0][1] <= i - k:
            dq.popleft()
        
        # Remove elements larger than current
        while dq and dq[-1][0] >= arr[i]:
            dq.pop()
        
        # Add current element
        dq.append((arr[i], i))
        
        # Add minimum to result when window is complete
        if i >= k - 1:
            min_val = dq[0][0]
            # Count frequency of minimum in current window
            freq = sum(1 for j in range(i - k + 1, i + 1) if arr[j] == min_val)
            result.append((min_val, freq))
    
    return result

# Example usage
arr = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = subarray_minimums_with_frequency(arr, k)
print(f"Subarray minimums with frequency: {result}")
```

#### **3. Subarray Minimums with Index**
**Problem**: Find minimum element in each subarray of size k, along with its index.

**Key Differences**: Also track index of minimum element

**Solution Approach**: Use deque with index tracking

**Implementation**:
```python
def subarray_minimums_with_index(arr, k):
    """
    Find minimum element and its index in each subarray of size k
    """
    from collections import deque
    
    dq = deque()  # Store indices
    result = []
    
    for i in range(len(arr)):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices of elements larger than current
        while dq and arr[dq[-1]] >= arr[i]:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # Add minimum and its index to result when window is complete
        if i >= k - 1:
            min_idx = dq[0]
            result.append((arr[min_idx], min_idx))
    
    return result

# Example usage
arr = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = subarray_minimums_with_index(arr, k)
print(f"Subarray minimums with index: {result}")
```

### Related Problems

#### **CSES Problems**
- [Subarray Minimums](https://cses.fi/problemset/task/2101) - Find minimum element in each subarray
- [Sliding Window Minimum](https://cses.fi/problemset/task/2102) - Classic sliding window minimum
- [Range Minimum Queries](https://cses.fi/problemset/task/2103) - Range minimum queries

#### **LeetCode Problems**
- [Sliding Window Minimum](https://leetcode.com/problems/sliding-window-minimum/) - Classic sliding window minimum
- [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) - Minimum window substring
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) - K distinct characters
- [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) - Subarray product

#### **Problem Categories**
- **Sliding Window**: Window minimum, window statistics, window optimization
- **Deque**: Monotonic data structure, efficient window management
- **Segment Tree**: Range updates, range queries, lazy propagation
- **Array Processing**: Window operations, element tracking, statistics

## 🚀 Key Takeaways

- **Deque Technique**: The standard approach for sliding window minimum problems
- **Monotonic Data Structure**: Use deque to maintain increasing order
- **Window Management**: Efficiently remove elements outside current window
- **Space Optimization**: Use indices instead of values to save space
- **Pattern Recognition**: This technique applies to many sliding window minimum problems