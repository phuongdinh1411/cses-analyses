# CSES Maximum Subarray Sum - Problem Analysis

## Problem Statement
Given an array of n integers, your task is to find the maximum sum of a subarray.

### Input
The first input line has an integer n: the size of the array.
The second line has n integers a1,a2,…,an: the contents of the array.

### Output
Print one integer: the maximum sum of a subarray.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- −10^9 ≤ ai ≤ 10^9

### Example
```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
11
```

## Solution Progression

### Approach 1: Check All Subarrays - O(n³)
**Description**: Check all possible subarrays and find the maximum sum.

```python
def max_subarray_sum_naive(n, arr):
    max_sum = float('-inf')
    
    for i in range(n):
        for j in range(i, n):
            current_sum = sum(arr[i:j+1])
            max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this is inefficient**: Cubic time complexity for large arrays.

### Improvement 1: Kadane's Algorithm - O(n)
**Description**: Use Kadane's algorithm to find the maximum subarray sum efficiently.

```python
def max_subarray_sum_kadane(n, arr):
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far
```

**Why this improvement works**: Kadane's algorithm efficiently tracks the maximum sum ending at each position.

### Alternative: Sliding Window with Prefix Sum - O(n)
**Description**: Use sliding window with prefix sum to find maximum subarray sum.

```python
def max_subarray_sum_sliding_window(n, arr):
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    max_sum = float('-inf')
    min_prefix = 0
    
    for i in range(1, n + 1):
        max_sum = max(max_sum, prefix_sum[i] - min_prefix)
        min_prefix = min(min_prefix, prefix_sum[i])
    
    return max_sum
```

**Why this works**: Prefix sum allows us to find subarray sums efficiently.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

def max_subarray_sum_kadane(n, arr):
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

result = max_subarray_sum_kadane(n, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n³) | O(1) | Check all subarrays |
| Kadane's | O(n) | O(1) | Track maximum ending at each position |
| Sliding Window | O(n) | O(n) | Use prefix sum |

## Key Insights for Other Problems

### 1. **Maximum Subarray Problems**
**Principle**: Use Kadane's algorithm to efficiently find the maximum subarray sum.
**Applicable to**:
- Maximum subarray problems
- Subarray sum problems
- Dynamic programming
- Algorithm design

**Example Problems**:
- Maximum subarray problems
- Subarray sum problems
- Dynamic programming
- Algorithm design

### 2. **Kadane's Algorithm**
**Principle**: Track the maximum sum ending at each position to find the global maximum.
**Applicable to**:
- Subarray sum problems
- Dynamic programming
- Algorithm design
- Problem solving

**Example Problems**:
- Subarray sum problems
- Dynamic programming
- Algorithm design
- Problem solving

### 3. **Prefix Sum Technique**
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

### 4. **Dynamic Programming Applications**
**Principle**: Use dynamic programming to build solutions from smaller subproblems.
**Applicable to**:
- Dynamic programming
- Optimization problems
- Algorithm design
- Problem solving

**Example Problems**:
- Dynamic programming
- Optimization problems
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **Kadane's Algorithm Pattern**
```python
def kadane_algorithm(arr):
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far
```

### 2. **Prefix Sum Pattern**
```python
def prefix_sum_max_subarray(arr):
    n = len(arr)
    prefix_sum = [0] * (n + 1)
    
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    max_sum = float('-inf')
    min_prefix = 0
    
    for i in range(1, n + 1):
        max_sum = max(max_sum, prefix_sum[i] - min_prefix)
        min_prefix = min(min_prefix, prefix_sum[i])
    
    return max_sum
```

### 3. **Sliding Window Pattern**
```python
def sliding_window_max_subarray(arr):
    left = 0
    current_sum = 0
    max_sum = float('-inf')
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum < 0 and left <= right:
            current_sum -= arr[left]
            left += 1
        
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

## Edge Cases to Remember

1. **All negative numbers**: Return the maximum negative number
2. **All positive numbers**: Return the sum of all elements
3. **Single element**: Return the element itself
4. **Large numbers**: Use appropriate data types
5. **Zero elements**: Handle appropriately

## Problem-Solving Framework

1. **Identify subarray nature**: This is a maximum subarray sum problem
2. **Choose approach**: Use Kadane's algorithm for efficiency
3. **Track maximum**: Maintain maximum sum ending at each position
4. **Update global maximum**: Update global maximum when needed
5. **Return result**: Return the maximum subarray sum

---

*This analysis shows how to efficiently find the maximum subarray sum using Kadane's algorithm.* 