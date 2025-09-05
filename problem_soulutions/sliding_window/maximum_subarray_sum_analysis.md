---
layout: simple
title: "Maximum Subarray Sum Analysis"
permalink: /problem_soulutions/sliding_window/maximum_subarray_sum_analysis
---


# Maximum Subarray Sum Analysis

## Problem Description

**Problem**: Given an array of n integers, find the maximum sum of a subarray.

**Input**: 
- n: the size of the array
- arr: array of n integers

**Output**: The maximum sum of any subarray.

**Example**:
```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
11

Explanation: 
The subarray [3, -2, 5, 3] has the maximum sum of 11.
Other subarrays have smaller sums.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the maximum sum among all possible subarrays
- Handle negative numbers properly
- Use efficient algorithms to avoid brute force
- Consider edge cases like all negative numbers

**Key Observations:**
- Subarrays can have any length from 1 to n
- Negative numbers can be part of the optimal solution
- We need to track both current and global maximum
- Kadane's algorithm is optimal for this problem

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays and calculate their sums.

```python
def max_subarray_sum_naive(n, arr):
    max_sum = float('-inf')
    
    for i in range(n):
        for j in range(i, n):
            current_sum = sum(arr[i:j+1])
            max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this is inefficient:**
- Time complexity: O(n³)
- Lots of redundant calculations
- Not scalable for large inputs
- Inefficient sum calculation

### Step 3: Optimization with Kadane's Algorithm
**Idea**: Use Kadane's algorithm to efficiently track the maximum sum ending at each position.

```python
def max_subarray_sum_kadane(n, arr):
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far
```

**Why this improvement works:**
- Time complexity: O(n)
- Efficiently tracks maximum sum ending at each position
- Handles negative numbers correctly
- Single pass through the array

### Step 4: Alternative Approach with Prefix Sum
**Idea**: Use prefix sum to calculate subarray sums efficiently.

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

**Why this works:**
- Prefix sum allows us to find subarray sums in constant time
- Time complexity: O(n)
- Good alternative approach
- Useful for understanding prefix sum technique

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_maximum_subarray_sum():
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = find_maximum_subarray_sum(n, arr)
    print(result)

def find_maximum_subarray_sum(n, arr):
    """Find maximum subarray sum using Kadane's algorithm"""
    if not arr:
        return 0
    
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

# Main execution
if __name__ == "__main__":
    solve_maximum_subarray_sum()
```

**Why this works:**
- Optimal Kadane's algorithm approach
- Handles all edge cases correctly
- Efficient single-pass solution
- Clear and readable code
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([8, -1, 3, -2, 5, 3, -5, 2, 2], 11),
        ([1, 2, 3, 4, 5], 15),
        ([-1, -2, -3, -4], -1),
        ([1], 1),
        ([0, 0, 0, 0], 0),
    ]
    
    for arr, expected in test_cases:
        result = find_maximum_subarray_sum(len(arr), arr)
        print(f"arr: {arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_maximum_subarray_sum(n, arr):
    if not arr:
        return 0
    
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array
- **Space**: O(1) - only using a few variables

### Why This Solution Works
- **Kadane's Algorithm**: Efficiently finds maximum subarray sum
- **Single Pass**: Processes each element only once
- **Optimal Algorithm**: Best known approach for this problem
- **Edge Case Handling**: Properly handles all negative arrays

## 🎨 Visual Example

### Input Example
```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]
```

### All Possible Subarrays
```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]
Index:   0  1   2  3  4   5  6  7

All subarrays and their sums:
Length 1: [-1]=-1, [3]=3, [-2]=-2, [5]=5, [3]=3, [-5]=-5, [2]=2, [2]=2
Length 2: [-1,3]=2, [3,-2]=1, [-2,5]=3, [5,3]=8, [3,-5]=-2, [-5,2]=-3, [2,2]=4
Length 3: [-1,3,-2]=0, [3,-2,5]=6, [-2,5,3]=6, [5,3,-5]=3, [3,-5,2]=0, [-5,2,2]=-1
Length 4: [-1,3,-2,5]=5, [3,-2,5,3]=9, [-2,5,3,-5]=1, [5,3,-5,2]=5, [3,-5,2,2]=2
Length 5: [-1,3,-2,5,3]=8, [3,-2,5,3,-5]=4, [-2,5,3,-5,2]=3, [5,3,-5,2,2]=7
Length 6: [-1,3,-2,5,3,-5]=3, [3,-2,5,3,-5,2]=6, [-2,5,3,-5,2,2]=5
Length 7: [-1,3,-2,5,3,-5,2]=5, [3,-2,5,3,-5,2,2]=8
Length 8: [-1,3,-2,5,3,-5,2,2]=7

Maximum sum: 9 (subarray [3, -2, 5, 3])
```

### Kadane's Algorithm Process
```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]

Initialize:
max_ending_here = 0
max_so_far = -∞

Step 1: i=0, arr[0]=-1
max_ending_here = max(-1, 0 + (-1)) = max(-1, -1) = -1
max_so_far = max(-∞, -1) = -1

Step 2: i=1, arr[1]=3
max_ending_here = max(3, -1 + 3) = max(3, 2) = 3
max_so_far = max(-1, 3) = 3

Step 3: i=2, arr[2]=-2
max_ending_here = max(-2, 3 + (-2)) = max(-2, 1) = 1
max_so_far = max(3, 1) = 3

Step 4: i=3, arr[3]=5
max_ending_here = max(5, 1 + 5) = max(5, 6) = 6
max_so_far = max(3, 6) = 6

Step 5: i=4, arr[4]=3
max_ending_here = max(3, 6 + 3) = max(3, 9) = 9
max_so_far = max(6, 9) = 9

Step 6: i=5, arr[5]=-5
max_ending_here = max(-5, 9 + (-5)) = max(-5, 4) = 4
max_so_far = max(9, 4) = 9

Step 7: i=6, arr[6]=2
max_ending_here = max(2, 4 + 2) = max(2, 6) = 6
max_so_far = max(9, 6) = 9

Step 8: i=7, arr[7]=2
max_ending_here = max(2, 6 + 2) = max(2, 8) = 8
max_so_far = max(9, 8) = 9

Final result: 9
```

### Visual Kadane's Algorithm
```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]
Index:   0  1   2  3  4   5  6  7

Step-by-step tracking:
i=0: max_ending_here=-1, max_so_far=-1
i=1: max_ending_here=3,  max_so_far=3
i=2: max_ending_here=1,  max_so_far=3
i=3: max_ending_here=6,  max_so_far=6
i=4: max_ending_here=9,  max_so_far=9  ← Maximum found
i=5: max_ending_here=4,  max_so_far=9
i=6: max_ending_here=6,  max_so_far=9
i=7: max_ending_here=8,  max_so_far=9

Optimal subarray: [3, -2, 5, 3] with sum = 9
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n³)        │ O(1)         │ Check all    │
│                 │              │              │ subarrays    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Optimized       │ O(n²)        │ O(1)         │ Use prefix   │
│ Brute Force     │              │              │ sums         │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Kadane's        │ O(n)         │ O(1)         │ Dynamic      │
│ Algorithm       │              │              │ programming  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Divide &        │ O(n log n)   │ O(log n)     │ Recursive    │
│ Conquer         │              │              │ approach     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Maximum Subarray Sum Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: array    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize:     │
              │ max_ending_here │
              │ = 0             │
              │ max_so_far =    │
              │ -∞              │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each        │
              │ element:        │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ max_ending_here │
              │ = max(arr[i],   │
              │ max_ending_here │
              │ + arr[i])       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ max_so_far =    │
              │ max(max_so_far, │
              │ max_ending_here)│
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return          │
              │ max_so_far      │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Kadane's Algorithm**
- Track maximum sum ending at each position
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Dynamic Programming**
- Build solution from smaller subproblems
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Negative Number Handling**
- Negative numbers can be part of optimal solution
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Maximum Subarray with Length Constraint
**Problem**: Find maximum sum of subarrays with length at least k.

```python
def find_maximum_subarray_with_min_length(n, arr, k):
    if k > n:
        return 0
    
    # Calculate prefix sum
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    max_sum = float('-inf')
    min_prefix = 0
    
    for i in range(k, n + 1):
        max_sum = max(max_sum, prefix_sum[i] - min_prefix)
        min_prefix = min(min_prefix, prefix_sum[i - k + 1])
    
    return max_sum

# Example usage
result = find_maximum_subarray_with_min_length(8, [-1, 3, -2, 5, 3, -5, 2, 2], 3)
print(f"Maximum subarray sum with min length 3: {result}")
```

### Variation 2: Maximum Subarray with Circular Array
**Problem**: Find maximum subarray sum in a circular array.

```python
def find_maximum_circular_subarray_sum(n, arr):
    # Case 1: Maximum subarray doesn't wrap around
    max_normal = find_maximum_subarray_sum(n, arr)
    
    # Case 2: Maximum subarray wraps around
    # Find minimum subarray sum and subtract from total
    total_sum = sum(arr)
    min_subarray_sum = find_minimum_subarray_sum(n, arr)
    max_wrapped = total_sum - min_subarray_sum
    
    return max(max_normal, max_wrapped)

def find_minimum_subarray_sum(n, arr):
    min_so_far = float('inf')
    min_ending_here = 0
    
    for num in arr:
        min_ending_here = min(num, min_ending_here + num)
        min_so_far = min(min_so_far, min_ending_here)
    
    return min_so_far

# Example usage
result = find_maximum_circular_subarray_sum(8, [-1, 3, -2, 5, 3, -5, 2, 2])
print(f"Maximum circular subarray sum: {result}")
```

### Variation 3: Maximum Subarray with K Negations
**Problem**: Find maximum subarray sum after negating at most k elements.

```python
def find_maximum_subarray_with_k_negations(n, arr, k):
    # Use sliding window to find best k elements to negate
    max_sum = find_maximum_subarray_sum(n, arr)
    
    if k == 0:
        return max_sum
    
    # Find k smallest elements to negate
    sorted_arr = sorted(arr)
    for i in range(min(k, len(sorted_arr))):
        if sorted_arr[i] < 0:
            # Negating a negative number makes it positive
            max_sum += 2 * abs(sorted_arr[i])
    
    return max_sum

# Example usage
result = find_maximum_subarray_with_k_negations(8, [-1, 3, -2, 5, 3, -5, 2, 2], 2)
print(f"Maximum subarray sum with 2 negations: {result}")
```

### Variation 4: Maximum Subarray with Range Queries
**Problem**: Answer queries about maximum subarray sum in specific ranges.

```python
def maximum_subarray_sum_queries(n, arr, queries):
    """Answer maximum subarray sum queries for specific ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append(0)
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            max_sum = find_maximum_subarray_sum_in_range(len(subarray), subarray)
            results.append(max_sum)
    
    return results

def find_maximum_subarray_sum_in_range(n, arr):
    """Find maximum subarray sum in a specific range"""
    if not arr:
        return 0
    
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for num in arr:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

# Example usage
queries = [(0, 4), (1, 6), (2, 7)]
result = maximum_subarray_sum_queries(8, [-1, 3, -2, 5, 3, -5, 2, 2], queries)
print(f"Range query results: {result}")
```

### Variation 5: Maximum Subarray with Constraints
**Problem**: Find maximum subarray sum where no two adjacent elements are negative.

```python
def find_maximum_constrained_subarray_sum(n, arr):
    max_so_far = float('-inf')
    max_ending_here = 0
    last_negative = -1
    
    for i, num in enumerate(arr):
        if num < 0:
            if last_negative == i - 1:
                # Two consecutive negative numbers, reset
                max_ending_here = num
            else:
                max_ending_here = max(num, max_ending_here + num)
            last_negative = i
        else:
            max_ending_here = max(num, max_ending_here + num)
        
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

# Example usage
result = find_maximum_constrained_subarray_sum(8, [-1, 3, -2, 5, 3, -5, 2, 2])
print(f"Maximum constrained subarray sum: {result}")
```

## 🔗 Related Problems

- **[Fixed Length Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Fixed-size subarray problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray sum problems
- **[Sliding Window Advertisement](/cses-analyses/problem_soulutions/sliding_window/)**: Window-based problems

## 📚 Learning Points

1. **Kadane's Algorithm**: Essential for maximum subarray problems
2. **Dynamic Programming**: Important for building optimal solutions
3. **Negative Number Handling**: Key for understanding edge cases
4. **Single Pass Optimization**: Important for efficient algorithms

---

**This is a great introduction to maximum subarray sum problems!** 🎯
    
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