---
layout: simple
title: "Minimum Subarray Sum Analysis"
permalink: /problem_soulutions/sliding_window/minimum_subarray_sum_analysis
---


# Minimum Subarray Sum Analysis

## Problem Description

**Problem**: Given an array of n integers, find the minimum sum of a subarray.

**Input**: 
- n: the size of the array
- arr: array of n integers

**Output**: The minimum sum of any subarray.

**Example**:
```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
-5

Explanation: 
The subarray [-5] has the minimum sum of -5.
Other subarrays have larger sums.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the minimum sum among all possible subarrays
- Handle negative numbers properly
- Use efficient algorithms to avoid brute force
- Consider edge cases like all positive numbers

**Key Observations:**
- Subarrays can have any length from 1 to n
- Negative numbers can significantly reduce the sum
- We need to track both current and global minimum
- Modified Kadane's algorithm is optimal for this problem

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays and calculate their sums.

```python
def min_subarray_sum_naive(n, arr):
    min_sum = float('inf')
    
    for i in range(n):
        for j in range(i, n):
            current_sum = sum(arr[i:j+1])
            min_sum = min(min_sum, current_sum)
    
    return min_sum
```

**Why this is inefficient:**
- Time complexity: O(n³)
- Lots of redundant calculations
- Not scalable for large inputs
- Inefficient sum calculation

### Step 3: Optimization with Modified Kadane's Algorithm
**Idea**: Use modified Kadane's algorithm to efficiently track the minimum sum ending at each position.

```python
def min_subarray_sum_kadane(n, arr):
    min_so_far = float('inf')
    min_ending_here = 0
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far
```

**Why this improvement works:**
- Time complexity: O(n)
- Efficiently tracks minimum sum ending at each position
- Handles negative numbers correctly
- Single pass through the array

### Step 4: Alternative Approach with Prefix Sum
**Idea**: Use prefix sum to calculate subarray sums efficiently.

```python
def min_subarray_sum_sliding_window(n, arr):
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    min_sum = float('inf')
    max_prefix = 0
    
    for i in range(1, n + 1):
        min_sum = min(min_sum, prefix_sum[i] - max_prefix)
        max_prefix = max(max_prefix, prefix_sum[i])
    
    return min_sum
```

**Why this works:**
- Prefix sum allows us to find subarray sums in constant time
- Time complexity: O(n)
- Good alternative approach
- Useful for understanding prefix sum technique

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_minimum_subarray_sum():
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = find_minimum_subarray_sum(n, arr)
    print(result)

def find_minimum_subarray_sum(n, arr):
    """Find minimum subarray sum using modified Kadane's algorithm"""
    if not arr:
        return 0
    
    min_so_far = float('inf')
    min_ending_here = 0
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far

# Main execution
if __name__ == "__main__":
    solve_minimum_subarray_sum()
```

**Why this works:**
- Optimal modified Kadane's algorithm approach
- Handles all edge cases correctly
- Efficient single-pass solution
- Clear and readable code
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([8, -1, 3, -2, 5, 3, -5, 2, 2], -5),
        ([1, 2, 3, 4, 5], 1),
        ([-1, -2, -3, -4], -10),
        ([1], 1),
        ([0, 0, 0, 0], 0),
    ]
    
    for arr, expected in test_cases:
        result = find_minimum_subarray_sum(len(arr), arr)
        print(f"arr: {arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_minimum_subarray_sum(n, arr):
    if not arr:
        return 0
    
    min_so_far = float('inf')
    min_ending_here = 0
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array
- **Space**: O(1) - only using a few variables

### Why This Solution Works
- **Modified Kadane's Algorithm**: Efficiently finds minimum subarray sum
- **Single Pass**: Processes each element only once
- **Optimal Algorithm**: Best known approach for this problem
- **Edge Case Handling**: Properly handles all positive arrays

## 🎯 Key Insights

### 1. **Modified Kadane's Algorithm**
- Track minimum sum ending at each position
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Dynamic Programming**
- Build solution from smaller subproblems
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Negative Number Handling**
- Negative numbers can significantly reduce the sum
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Minimum Subarray with Length Constraint
**Problem**: Find minimum sum of subarrays with length at least k.

```python
def find_minimum_subarray_with_min_length(n, arr, k):
    if k > n:
        return 0
    
    # Calculate prefix sum
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    min_sum = float('inf')
    max_prefix = 0
    
    for i in range(k, n + 1):
        min_sum = min(min_sum, prefix_sum[i] - max_prefix)
        max_prefix = max(max_prefix, prefix_sum[i - k + 1])
    
    return min_sum

# Example usage
result = find_minimum_subarray_with_min_length(8, [-1, 3, -2, 5, 3, -5, 2, 2], 3)
print(f"Minimum subarray sum with min length 3: {result}")
```

### Variation 2: Minimum Subarray with Circular Array
**Problem**: Find minimum subarray sum in a circular array.

```python
def find_minimum_circular_subarray_sum(n, arr):
    # Case 1: Minimum subarray doesn't wrap around
    min_normal = find_minimum_subarray_sum(n, arr)
    
    # Case 2: Minimum subarray wraps around
    # Find maximum subarray sum and subtract from total
    total_sum = sum(arr)
    max_subarray_sum = find_maximum_subarray_sum(n, arr)
    min_wrapped = total_sum - max_subarray_sum
    
    return min(min_normal, min_wrapped)

def find_maximum_subarray_sum(n, arr):
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

# Example usage
result = find_minimum_circular_subarray_sum(8, [-1, 3, -2, 5, 3, -5, 2, 2])
print(f"Minimum circular subarray sum: {result}")
```

### Variation 3: Minimum Subarray with K Negations
**Problem**: Find minimum subarray sum after negating at most k elements.

```python
def find_minimum_subarray_with_k_negations(n, arr, k):
    # Use sliding window to find best k elements to negate
    min_sum = find_minimum_subarray_sum(n, arr)
    
    if k == 0:
        return min_sum
    
    # Find k largest elements to negate
    sorted_arr = sorted(arr, reverse=True)
    for i in range(min(k, len(sorted_arr))):
        if sorted_arr[i] > 0:
            # Negating a positive number makes it negative
            min_sum -= 2 * sorted_arr[i]
    
    return min_sum

# Example usage
result = find_minimum_subarray_with_k_negations(8, [-1, 3, -2, 5, 3, -5, 2, 2], 2)
print(f"Minimum subarray sum with 2 negations: {result}")
```

### Variation 4: Minimum Subarray with Range Queries
**Problem**: Answer queries about minimum subarray sum in specific ranges.

```python
def minimum_subarray_sum_queries(n, arr, queries):
    """Answer minimum subarray sum queries for specific ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append(0)
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            min_sum = find_minimum_subarray_sum_in_range(len(subarray), subarray)
            results.append(min_sum)
    
    return results

def find_minimum_subarray_sum_in_range(n, arr):
    """Find minimum subarray sum in a specific range"""
    if not arr:
        return 0
    
    min_so_far = float('inf')
    min_ending_here = 0
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far

# Example usage
queries = [(0, 4), (1, 6), (2, 7)]
result = minimum_subarray_sum_queries(8, [-1, 3, -2, 5, 3, -5, 2, 2], queries)
print(f"Range query results: {result}")
```

### Variation 5: Minimum Subarray with Constraints
**Problem**: Find minimum subarray sum where no two adjacent elements are positive.

```python
def find_minimum_constrained_subarray_sum(n, arr):
    min_so_far = float('inf')
    min_ending_here = 0
    last_positive = -1
    
    for i, num in enumerate(arr):
        if num > 0:
            if last_positive == i - 1:
                # Two consecutive positive numbers, reset
                min_ending_here = num
            else:
                min_ending_here = min(num, min_ending_here + num)
            last_positive = i
        else:
            min_ending_here = min(num, min_ending_here + num)
        
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far

# Example usage
result = find_minimum_constrained_subarray_sum(8, [-1, 3, -2, 5, 3, -5, 2, 2])
print(f"Minimum constrained subarray sum: {result}")
```

## 🔗 Related Problems

- **[Maximum Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Maximum subarray problems
- **[Fixed Length Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Fixed-size subarray problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray sum problems

## 📚 Learning Points

1. **Modified Kadane's Algorithm**: Essential for minimum subarray problems
2. **Dynamic Programming**: Important for building optimal solutions
3. **Negative Number Handling**: Key for understanding edge cases
4. **Single Pass Optimization**: Important for efficient algorithms

---

**This is a great introduction to minimum subarray sum problems!** 🎯
    
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    min_sum = float('inf')
    max_prefix = 0
    
    for i in range(1, n + 1):
        min_sum = min(min_sum, prefix_sum[i] - max_prefix)
        max_prefix = max(max_prefix, prefix_sum[i])
    
    return min_sum
```

### 3. **Sliding Window Pattern**
```python
def sliding_window_min_subarray(arr):
    left = 0
    current_sum = 0
    min_sum = float('inf')
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > 0 and left <= right:
            current_sum -= arr[left]
            left += 1
        
        min_sum = min(min_sum, current_sum)
    
    return min_sum
```

## Edge Cases to Remember

1. **All positive numbers**: Return the minimum positive number
2. **All negative numbers**: Return the sum of all elements
3. **Single element**: Return the element itself
4. **Large numbers**: Use appropriate data types
5. **Zero elements**: Handle appropriately

## Problem-Solving Framework

1. **Identify subarray nature**: This is a minimum subarray sum problem
2. **Choose approach**: Use modified Kadane's algorithm for efficiency
3. **Track minimum**: Maintain minimum sum ending at each position
4. **Update global minimum**: Update global minimum when needed
5. **Return result**: Return the minimum subarray sum

---

*This analysis shows how to efficiently find the minimum subarray sum using modified Kadane's algorithm.* 