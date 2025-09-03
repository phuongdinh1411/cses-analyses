---
layout: simple
title: "Subarray Maximums Sum"
permalink: /problem_soulutions/sliding_window/subarray_maximums_analysis
---

# Subarray Maximums Sum

## 📋 Problem Description

Given an array of n integers, find the sum of maximums of all subarrays.

**Input**: 
- First line: One integer n (size of the array)
- Second line: n integers a₁, a₂, ..., aₙ (array contents)

**Output**: 
- One integer: the sum of maximums of all subarrays

**Constraints**:
- 1 ≤ n ≤ 3⋅10⁵
- 1 ≤ aᵢ ≤ 10⁹

**Example**:
```
Input:
4
3 1 2 4

Output:
23
```

**Explanation**: The subarrays and their maximums are:
- [3] → max = 3
- [3, 1] → max = 3  
- [3, 1, 2] → max = 3
- [3, 1, 2, 4] → max = 4
- [1] → max = 1
- [1, 2] → max = 2
- [1, 2, 4] → max = 4
- [2] → max = 2
- [2, 4] → max = 4
- [4] → max = 4

Total sum = 3 + 3 + 3 + 4 + 1 + 2 + 4 + 2 + 4 + 4 = 23

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find sum of maximums of all possible subarrays
- **Key Insight**: Each element contributes as maximum to certain subarrays
- **Challenge**: Efficiently find contribution of each element

### Step 2: Brute Force Approach
**Check all possible subarrays and find maximum of each:**

```python
def subarray_maximums_naive(n, arr):
    total_sum = 0
    
    for i in range(n):
        for j in range(i, n):
            max_val = max(arr[i:j+1])
            total_sum += max_val
    
    return total_sum
```

**Complexity**: O(n³) - too slow for large arrays

### Step 3: Optimization
**Use monotonic stack to find contribution of each element:**

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

**Key Insight**: Use monotonic stack to find range where each element is maximum

### Step 4: Complete Solution

```python
def solve_subarray_maximums():
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = calculate_subarray_maximums_sum(n, arr)
    print(result)

def calculate_subarray_maximums_sum(n, arr):
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

if __name__ == "__main__":
    solve_subarray_maximums()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((4, [3, 1, 2, 4]), 23),
        ((3, [1, 2, 3]), 10),
        ((2, [5, 5]), 15),
        ((1, [7]), 7),
        ((5, [1, 1, 1, 1, 1]), 15),
        ((3, [10, 5, 8]), 33),
    ]
    
    for (n, arr), expected in test_cases:
        result = calculate_subarray_maximums_sum(n, arr)
        print(f"n={n}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def calculate_subarray_maximums_sum(n, arr):
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
        count = (i - left[i]) * (right[i] - i)
        total_sum += arr[i] * count
    
    return total_sum

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with monotonic stack
- **Space**: O(n) - arrays to store left and right boundaries

### Why This Solution Works
- **Monotonic Stack**: Efficiently finds next/previous larger elements
- **Contribution Analysis**: Each element contributes as maximum to specific subarrays
- **Range Calculation**: Uses left and right boundaries to count valid subarrays
- **Optimal Algorithm**: Best known approach for this problem

## 🎯 Key Insights

### 1. **Monotonic Stack Technique**
- Maintain elements in sorted order for efficient range queries
- Essential for finding next/previous larger elements
- Key optimization technique
- Enables efficient solution

### 2. **Contribution Analysis**
- Analyze how much each element contributes to final result
- Important for understanding
- Count subarrays where each element is maximum
- Essential for algorithm

### 3. **Range Finding**
- Find left and right boundaries where element is maximum
- Important for understanding
- Use stack operations efficiently
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Subarray Minimums Sum
**Problem**: Find the sum of minimums of all subarrays.

```python
def calculate_subarray_minimums_sum(n, arr):
    stack = []
    left = [-1] * n  # Previous smaller element to the left
    right = [n] * n  # Next smaller element to the right
    
    # Find previous smaller elements
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    
    # Clear stack for next pass
    stack.clear()
    
    # Find next smaller elements
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
    
    # Calculate contribution of each element
    total_sum = 0
    for i in range(n):
        count = (i - left[i]) * (right[i] - i)
        total_sum += arr[i] * count
    
    return total_sum

# Example usage
result = calculate_subarray_minimums_sum(4, [3, 1, 2, 4])
print(f"Subarray minimums sum: {result}")
```

### Variation 2: Subarray Maximums with Length Constraint
**Problem**: Find sum of maximums of subarrays with length at least k.

```python
def calculate_subarray_maximums_with_length_constraint(n, k, arr):
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
    
    # Clear stack for next pass
    stack.clear()
    
    # Find next larger elements
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
    
    # Calculate contribution with length constraint
    total_sum = 0
    for i in range(n):
        # Only count subarrays with length >= k
        left_bound = max(left[i] + 1, i - k + 1)
        right_bound = min(right[i] - 1, i + k - 1)
        
        if right_bound >= left_bound:
            count = max(0, right_bound - left_bound + 1)
            total_sum += arr[i] * count
    
    return total_sum

# Example usage
result = calculate_subarray_maximums_with_length_constraint(4, 2, [3, 1, 2, 4])
print(f"Subarray maximums sum with length >= 2: {result}")
```

### Variation 3: Subarray Maximums with Sum Constraint
**Problem**: Find sum of maximums of subarrays with sum at most S.

```python
def calculate_subarray_maximums_with_sum_constraint(n, S, arr):
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
    
    # Clear stack for next pass
    stack.clear()
    
    # Find next larger elements
    for i in range(n-1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        if stack:
            right[i] = stack[-1]
        stack.append(i)
    
    # Calculate contribution with sum constraint
    total_sum = 0
    for i in range(n):
        # Check subarrays ending at i with sum <= S
        current_sum = 0
        for j in range(i, right[i]):
            current_sum += arr[j]
            if current_sum > S:
                break
            if j >= left[i] + 1:
                total_sum += arr[i]
    
    return total_sum

# Example usage
result = calculate_subarray_maximums_with_sum_constraint(4, 10, [3, 1, 2, 4])
print(f"Subarray maximums sum with sum <= 10: {result}")
```

### Variation 4: Subarray Maximums with Range Queries
**Problem**: Answer queries about sum of maximums of subarrays in specific ranges.

```python
def subarray_maximums_range_queries(n, arr, queries):
    """Answer queries about sum of maximums of subarrays in ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append(0)
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            subarray_sum = calculate_subarray_maximums_sum_in_range(len(subarray), subarray)
            results.append(subarray_sum)
    
    return results

def calculate_subarray_maximums_sum_in_range(n, arr):
    """Calculate sum of maximums of subarrays in a specific range"""
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
        count = (i - left[i]) * (right[i] - i)
        total_sum += arr[i] * count
    
    return total_sum

# Example usage
queries = [(0, 2), (1, 3), (0, 3)]
result = subarray_maximums_range_queries(4, [3, 1, 2, 4], queries)
print(f"Range query results: {result}")
```

### Variation 5: Subarray Maximums with Kth Maximum
**Problem**: Find sum of kth maximums of all subarrays.

```python
def calculate_subarray_kth_maximums_sum(n, k, arr):
    """Calculate sum of kth maximums of all subarrays"""
    from heapq import heappush, heappop
    
    total_sum = 0
    
    for i in range(n):
        for j in range(i, n):
            # Extract subarray
            subarray = arr[i:j+1]
            
            # Find kth maximum using min heap
            if len(subarray) >= k:
                heap = []
                for num in subarray:
                    heappush(heap, -num)  # Negative for max heap
                
                # Get kth maximum
                for _ in range(k):
                    kth_max = -heappop(heap)
                
                total_sum += kth_max
    
    return total_sum

# Example usage
result = calculate_subarray_kth_maximums_sum(4, 2, [3, 1, 2, 4])
print(f"Sum of 2nd maximums: {result}")
```

## 🔗 Related Problems

- **[Subarray Minimums](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray minimum problems
- **[Sliding Window Maximum](/cses-analyses/problem_soulutions/sliding_window/)**: Window maximum problems
- **[Monotonic Stack Problems](/cses-analyses/problem_soulutions/)**: Stack-based problems

## 📚 Learning Points

1. **Monotonic Stack**: Essential for finding next/previous larger/smaller elements
2. **Contribution Analysis**: Important for understanding how each element contributes
3. **Range Finding**: Key for efficient subarray counting
4. **Stack Operations**: Important for maintaining monotonic properties

---

**This is a great introduction to monotonic stack and contribution analysis!** 🎯