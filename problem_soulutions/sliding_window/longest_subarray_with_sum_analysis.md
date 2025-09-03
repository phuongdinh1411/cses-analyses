---
layout: simple
title: "Longest Subarray with Sum Analysis"
permalink: /problem_soulutions/sliding_window/longest_subarray_with_sum_analysis
---


# Longest Subarray with Sum Analysis

## Problem Description

**Problem**: Given an array of n integers, find the length of the longest subarray with sum x.

**Input**: 
- n: the size of the array
- x: the required sum
- arr: array of n integers

**Output**: The length of the longest subarray with sum x, or -1 if no such subarray exists.

**Example**:
```
Input:
5 7
2 -1 3 5 -2

Output:
3

Explanation: 
The subarray [2, -1, 3, 5, -2] has sum 7 and length 3.
Other subarrays with sum 7 may exist but this is the longest.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the longest subarray that sums to a target value x
- Handle both positive and negative numbers
- Use efficient algorithms to avoid brute force
- Consider edge cases like no valid subarray

**Key Observations:**
- Subarrays can have any length from 1 to n
- Need to track cumulative sums efficiently
- Hash map can help find target sums quickly
- Sliding window works for positive numbers only

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays to find the longest one with sum x.

```python
def longest_subarray_naive(n, x, arr):
    max_length = -1
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == x:
                max_length = max(max_length, j - i + 1)
    
    return max_length
```

**Why this is inefficient:**
- Time complexity: O(n²)
- Lots of redundant calculations
- Not scalable for large inputs
- Inefficient sum calculation

### Step 3: Optimization with Prefix Sum and Hash Map
**Idea**: Use prefix sum and hash map to find the longest subarray with target sum.

```python
def longest_subarray_prefix_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1  # Empty subarray has sum 0 at index -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in sum_indices:
            length = i - sum_indices[prefix_sum - x]
            max_length = max(max_length, length)
        # Only update if we haven't seen this prefix sum before
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length
```

**Why this improvement works:**
- Time complexity: O(n)
- Prefix sum allows constant time subarray sum calculation
- Hash map tracks previous prefix sums efficiently
- Handles both positive and negative numbers

### Step 4: Alternative Approach with Sliding Window
**Idea**: Use sliding window technique for arrays with positive numbers.

```python
def longest_subarray_sliding_window(n, x, arr):
    # This works only for positive numbers
    left = 0
    current_sum = 0
    max_length = -1
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum > x and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == x:
            max_length = max(max_length, right - left + 1)
    
    return max_length
```

**Why this works:**
- Sliding window efficiently maintains valid sum
- Time complexity: O(n)
- Good for positive number arrays
- Limited applicability but very efficient

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_longest_subarray_with_sum():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = find_longest_subarray_with_sum(n, x, arr)
    print(result)

def find_longest_subarray_with_sum(n, x, arr):
    """Find length of longest subarray with sum x using prefix sum and hash map"""
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1  # Empty subarray has sum 0 at index -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # If we have seen (prefix_sum - x) before, we found a subarray with sum x
        if prefix_sum - x in sum_indices:
            length = i - sum_indices[prefix_sum - x]
            max_length = max(max_length, length)
        
        # Only update if we haven't seen this prefix sum before
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length

# Main execution
if __name__ == "__main__":
    solve_longest_subarray_with_sum()
```

**Why this works:**
- Optimal prefix sum + hash map algorithm approach
- Handles all edge cases correctly
- Efficient sum calculation
- Clear and readable code
            max_length = max(max_length, right - left + 1)
    
    return max_length

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 7, [2, -1, 3, 5, -2]), 3),
        ((4, 6, [1, 2, 3, 4]), 2),
        ((3, 0, [1, -1, 0]), 3),
        ((2, 5, [1, 4]), 2),
        ((1, 1, [1]), 1),
    ]
    
    for (n, x, arr), expected in test_cases:
        result = find_longest_subarray_with_sum(n, x, arr)
        print(f"n={n}, x={x}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_longest_subarray_with_sum(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum - x in sum_indices:
            length = i - sum_indices[prefix_sum - x]
            max_length = max(max_length, length)
        
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with prefix sum
- **Space**: O(n) - hash map to store prefix sum indices

### Why This Solution Works
- **Prefix Sum**: Efficiently calculates subarray sums
- **Hash Map**: Tracks first occurrence of each prefix sum
- **Optimal Algorithm**: Best known approach for this problem
- **Edge Case Handling**: Properly handles no valid subarray case

## 🎯 Key Insights

### 1. **Prefix Sum Technique**
- Convert range queries to point queries
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Hash Map for Index Tracking**
- Track first occurrence of each prefix sum
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Longest Subarray Optimization**
- Only update hash map for first occurrence
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Longest Subarray with Sum at Most K
**Problem**: Find longest subarray with sum at most k.

```python
def find_longest_subarray_with_sum_at_most_k(n, k, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = 0
    sum_indices = defaultdict(int)
    sum_indices[0] = -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Find the smallest prefix sum >= (prefix_sum - k)
        target = prefix_sum - k
        for prev_sum, prev_idx in sum_indices.items():
            if prev_sum >= target:
                length = i - prev_idx
                max_length = max(max_length, length)
        
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length

# Example usage
result = find_longest_subarray_with_sum_at_most_k(5, 7, [2, -1, 3, 5, -2])
print(f"Longest subarray with sum at most 7: {result}")
```

### Variation 2: Longest Subarray with Sum in Range
**Problem**: Find longest subarray with sum in range [L, R].

```python
def find_longest_subarray_with_sum_in_range(n, L, R, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = 0
    sum_indices = defaultdict(int)
    sum_indices[0] = -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Check if any previous prefix sum gives us a sum in [L, R]
        for prev_sum, prev_idx in sum_indices.items():
            current_sum = prefix_sum - prev_sum
            if L <= current_sum <= R:
                length = i - prev_idx
                max_length = max(max_length, length)
        
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length

# Example usage
result = find_longest_subarray_with_sum_in_range(5, 5, 10, [2, -1, 3, 5, -2])
print(f"Longest subarray with sum in [5, 10]: {result}")
```

### Variation 3: Longest Subarray with Even Sum
**Problem**: Find longest subarray with even sum.

```python
def find_longest_subarray_with_even_sum(n, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = 0
    even_indices = defaultdict(int)
    odd_indices = defaultdict(int)
    even_indices[0] = -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum % 2 == 0:
            # Even sum, look for previous even prefix sum
            if prefix_sum in even_indices:
                length = i - even_indices[prefix_sum]
                max_length = max(max_length, length)
            even_indices[prefix_sum] = i
        else:
            # Odd sum, look for previous odd prefix sum
            if prefix_sum in odd_indices:
                length = i - odd_indices[prefix_sum]
                max_length = max(max_length, length)
            odd_indices[prefix_sum] = i
    
    return max_length

# Example usage
result = find_longest_subarray_with_even_sum(5, [2, -1, 3, 5, -2])
print(f"Longest subarray with even sum: {result}")
```

### Variation 4: Longest Subarray with Sum and Length Constraints
**Problem**: Find longest subarray with sum x and length at least k.

```python
def find_longest_subarray_with_sum_and_length(n, x, k, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum - x in sum_indices:
            length = i - sum_indices[prefix_sum - x]
            if length >= k:
                max_length = max(max_length, length)
        
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length

# Example usage
result = find_longest_subarray_with_sum_and_length(5, 7, 2, [2, -1, 3, 5, -2])
print(f"Longest subarray with sum 7 and length >= 2: {result}")
```

### Variation 5: Longest Subarray with Sum and Character Constraints
**Problem**: Find longest subarray with sum x where no two adjacent elements are negative.

```python
def find_longest_subarray_with_sum_and_constraints(n, x, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1
    last_negative = -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Check constraint: no two adjacent negative elements
        if arr[i] < 0:
            if last_negative == i - 1:
                # Two consecutive negative numbers, reset
                sum_indices.clear()
                sum_indices[0] = i - 1
                prefix_sum = arr[i]
            last_negative = i
        
        if prefix_sum - x in sum_indices:
            length = i - sum_indices[prefix_sum - x]
            max_length = max(max_length, length)
        
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length

# Example usage
result = find_longest_subarray_with_sum_and_constraints(5, 7, [2, -1, 3, 5, -2])
print(f"Longest subarray with sum 7 and constraints: {result}")
```

## 🔗 Related Problems

- **[Maximum Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Maximum subarray problems
- **[Fixed Length Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Fixed-size subarray problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray sum problems

## 📚 Learning Points

1. **Prefix Sum Technique**: Essential for subarray sum problems
2. **Hash Map for Index Tracking**: Important for longest subarray optimization
3. **Range Query Optimization**: Key for efficient subarray operations
4. **Edge Case Handling**: Important for robust solutions

---

**This is a great introduction to longest subarray with sum problems!** 🎯
    from collections import defaultdict
    
    prefix_sum = 0
    max_length = -1
    sum_indices = defaultdict(int)
    sum_indices[0] = -1
    
    for i in range(len(arr)):
        prefix_sum += arr[i]
        
        if prefix_sum - target in sum_indices:
            length = i - sum_indices[prefix_sum - target]
            max_length = max(max_length, length)
        
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return max_length
```

### 2. **Sliding Window Pattern**
```python
def sliding_window_longest_subarray(arr, target):
    left = 0
    current_sum = 0
    max_length = -1
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > target and left <= right:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == target:
            max_length = max(max_length, right - left + 1)
    
    return max_length
```

### 3. **Two Pointer Technique**
```python
def two_pointer_longest_subarray(arr, target):
    left = 0
    current_sum = 0
    max_length = -1
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right: if current_sum == 
target: max_length = max(max_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return max_length
```

## Edge Cases to Remember

1. **No valid subarray**: Return -1
2. **Empty subarray**: Consider sum 0
3. **Negative numbers**: Use prefix sum approach
4. **Zero target**: Handle carefully
5. **Large numbers**: Use appropriate data types

## Problem-Solving Framework

1. **Identify subarray nature**: This is a longest subarray sum problem
2. **Choose approach**: Use prefix sum with hash map for efficiency
3. **Track prefix sums**: Maintain running sum and first occurrence indices
4. **Find longest**: Use hash map to find target sum differences
5. **Return result**: Return the length of longest valid subarray

---

*This analysis shows how to efficiently find the longest subarray with target sum using prefix sum and hash map techniques.* 