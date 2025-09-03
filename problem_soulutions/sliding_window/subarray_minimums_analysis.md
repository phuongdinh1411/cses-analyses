---
layout: simple
title: "Subarray Minimums Sum"
permalink: /problem_soulutions/sliding_window/subarray_minimums_analysis
---

# Subarray Minimums Sum

## 📋 Problem Description

Given an array of n integers, find the sum of minimums of all subarrays.

**Input**: 
- First line: One integer n (size of the array)
- Second line: n integers a₁, a₂, ..., aₙ (array contents)

**Output**: 
- One integer: the sum of minimums of all subarrays

**Constraints**:
- 1 ≤ n ≤ 3⋅10⁵
- 1 ≤ aᵢ ≤ 10⁹

**Example**:
```
Input:
4
3 1 2 4

Output:
17
```

**Explanation**: The subarrays and their minimums are:
- [3] → min = 3
- [3, 1] → min = 1  
- [3, 1, 2] → min = 1
- [3, 1, 2, 4] → min = 1
- [1] → min = 1
- [1, 2] → min = 1
- [1, 2, 4] → min = 1
- [2] → min = 2
- [2, 4] → min = 2
- [4] → min = 4

Total sum = 3 + 1 + 1 + 1 + 1 + 1 + 1 + 2 + 2 + 4 = 17

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find sum of minimums of all possible subarrays
- **Key Insight**: Each element contributes as minimum to certain subarrays
- **Challenge**: Efficiently find contribution of each element

### Step 2: Brute Force Approach
**Check all possible subarrays and find minimum of each:**

```python
def subarray_minimums_naive(n, arr):
    total_sum = 0
    
    for i in range(n):
        for j in range(i, n):
            min_val = min(arr[i:j+1])
            total_sum += min_val
    
    return total_sum
```

**Complexity**: O(n³) - too slow for large arrays

### Step 3: Optimization
**Use monotonic stack to find contribution of each element:**

```python
def subarray_minimums_monotonic_stack(n, arr):
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
        # Number of subarrays where arr[i] is the minimum
        count = (i - left[i]) * (right[i] - i)
        total_sum += arr[i] * count
    
    return total_sum
```

**Key Insight**: Use monotonic stack to find range where each element is minimum

### Step 4: Complete Solution

```python
def solve_subarray_minimums():
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = calculate_subarray_minimums_sum(n, arr)
    print(result)

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
        # Number of subarrays where arr[i] is the minimum
        count = (i - left[i]) * (right[i] - i)
        total_sum += arr[i] * count
    
    return total_sum

if __name__ == "__main__":
    solve_subarray_minimums()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((4, [3, 1, 2, 4]), 17),
        ((3, [1, 2, 3]), 6),
        ((2, [5, 5]), 10),
        ((1, [7]), 7),
        ((5, [1, 1, 1, 1, 1]), 15),
        ((3, [10, 5, 8]), 23),
    ]
    
    for (n, arr), expected in test_cases:
        result = calculate_subarray_minimums_sum(n, arr)
        print(f"n={n}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def calculate_subarray_minimums_sum(n, arr):
    stack = []
    left = [-1] * n
    right = [n] * n
    
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with monotonic stack
- **Space**: O(n) - arrays to store left and right boundaries

### Why This Solution Works
- **Monotonic Stack**: Efficiently finds next/previous smaller elements
- **Contribution Analysis**: Each element contributes as minimum to specific subarrays
- **Range Calculation**: Uses left and right boundaries to count valid subarrays
- **Optimal Algorithm**: Best known approach for this problem

## 🎯 Key Insights

### 1. **Monotonic Stack Technique**
- Maintain elements in sorted order for efficient range queries
- Essential for finding next/previous smaller elements
- Key optimization technique
- Enables efficient solution

### 2. **Contribution Analysis**
- Analyze how much each element contributes to final result
- Important for understanding
- Count subarrays where each element is minimum
- Essential for algorithm

### 3. **Range Finding**
- Find left and right boundaries where element is minimum
- Important for understanding
- Use stack operations efficiently
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Subarray Maximums Sum
**Problem**: Find the sum of maximums of all subarrays.

```python
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
        count = (i - left[i]) * (right[i] - i)
        total_sum += arr[i] * count
    
    return total_sum

# Example usage
result = calculate_subarray_maximums_sum(4, [3, 1, 2, 4])
print(f"Subarray maximums sum: {result}")
```

### Variation 2: Subarray Minimums with Length Constraint
**Problem**: Find sum of minimums of subarrays with length at least k.

```python
def calculate_subarray_minimums_with_length_constraint(n, k, arr):
    stack = []
    left = [-1] * n
    right = [n] * n
    
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
result = calculate_subarray_minimums_with_length_constraint(4, 2, [3, 1, 2, 4])
print(f"Subarray minimums sum with length >= 2: {result}")
```

### Variation 3: Subarray Minimums with Sum Constraint
**Problem**: Find sum of minimums of subarrays with sum at most S.

```python
def calculate_subarray_minimums_with_sum_constraint(n, S, arr):
    stack = []
    left = [-1] * n
    right = [n] * n
    
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
result = calculate_subarray_minimums_with_sum_constraint(4, 10, [3, 1, 2, 4])
print(f"Subarray minimums sum with sum <= 10: {result}")
```

### Variation 4: Subarray Minimums with Range Queries
**Problem**: Answer queries about sum of minimums of subarrays in specific ranges.

```python
def subarray_minimums_range_queries(n, arr, queries):
    """Answer queries about sum of minimums of subarrays in ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append(0)
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            subarray_sum = calculate_subarray_minimums_sum_in_range(len(subarray), subarray)
            results.append(subarray_sum)
    
    return results

def calculate_subarray_minimums_sum_in_range(n, arr):
    """Calculate sum of minimums of subarrays in a specific range"""
    stack = []
    left = [-1] * n
    right = [n] * n
    
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
queries = [(0, 2), (1, 3), (0, 3)]
result = subarray_minimums_range_queries(4, [3, 1, 2, 4], queries)
print(f"Range query results: {result}")
```

### Variation 5: Subarray Minimums with Kth Minimum
**Problem**: Find sum of kth minimums of all subarrays.

```python
def calculate_subarray_kth_minimums_sum(n, k, arr):
    """Calculate sum of kth minimums of all subarrays"""
    from heapq import heappush, heappop
    
    total_sum = 0
    
    for i in range(n):
        for j in range(i, n):
            # Extract subarray
            subarray = arr[i:j+1]
            
            # Find kth minimum using min heap
            if len(subarray) >= k:
                heap = []
                for num in subarray:
                    heappush(heap, num)
                
                # Get kth minimum
                for _ in range(k):
                    kth_min = heappop(heap)
                
                total_sum += kth_min
    
    return total_sum

# Example usage
result = calculate_subarray_kth_minimums_sum(4, 2, [3, 1, 2, 4])
print(f"Sum of 2nd minimums: {result}")
```

## 🔗 Related Problems

- **[Subarray Maximums](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray maximum problems
- **[Sliding Window Minimum](/cses-analyses/problem_soulutions/sliding_window/)**: Window minimum problems
- **[Monotonic Stack Problems](/cses-analyses/problem_soulutions/)**: Stack-based problems

## 📚 Learning Points

1. **Monotonic Stack**: Essential for finding next/previous smaller/larger elements
2. **Contribution Analysis**: Important for understanding how each element contributes
3. **Range Finding**: Key for efficient subarray counting
4. **Stack Operations**: Important for maintaining monotonic properties

---

**This is a great introduction to monotonic stack and contribution analysis!** 🎯