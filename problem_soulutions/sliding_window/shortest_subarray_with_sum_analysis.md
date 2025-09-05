---
layout: simple
title: "Shortest Subarray with Sum Analysis"
permalink: /problem_soulutions/sliding_window/shortest_subarray_with_sum_analysis
---


# Shortest Subarray with Sum Analysis

## Problem Description

**Problem**: Given an array of n integers, find the length of the shortest subarray with sum at least x.

**Input**: 
- n: the size of the array
- x: the required minimum sum
- arr: array of n integers

**Output**: The length of the shortest subarray with sum at least x, or -1 if no such subarray exists.

**Example**:
```
Input:
5 7
2 1 3 5 2

Output:
2

Explanation: 
The subarray [3, 5] has sum 8 ≥ 7 and length 2.
This is the shortest subarray that meets the requirement.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the shortest subarray that sums to at least x
- Handle positive numbers efficiently
- Use sliding window technique for optimization
- Consider edge cases like no valid subarray

**Key Observations:**
- Subarrays can have any length from 1 to n
- Need to track cumulative sums efficiently
- Sliding window works well for positive numbers
- Binary search is an alternative approach

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays to find the shortest one with sum at least x.

```python
def shortest_subarray_naive(n, x, arr):
    min_length = float('inf')
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum >= x:
                min_length = min(min_length, j - i + 1)
                break
    
    return min_length if min_length != float('inf') else -1
```

**Why this is inefficient:**
- Time complexity: O(n²)
- Lots of redundant calculations
- Not scalable for large inputs
- Inefficient sum calculation

### Step 3: Optimization with Sliding Window
**Idea**: Use sliding window technique to find the shortest subarray with sum at least x.

```python
def shortest_subarray_sliding_window(n, x, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Shrink window while sum is at least x
        while current_sum >= x and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1
```

**Why this improvement works:**
- Time complexity: O(n)
- Efficiently maintains constraint of sum at least x
- Single pass through the array
- Optimal algorithm for positive numbers

### Step 4: Alternative Approach with Binary Search
**Idea**: Use binary search with prefix sum to find the shortest subarray.

```python
def shortest_subarray_binary_search(n, x, arr):
    def check_length(length):
        # Check if there exists a subarray of given length with sum >= x
        current_sum = sum(arr[:length])
        if current_sum >= x:
            return True
        
        for i in range(length, n):
            current_sum = current_sum - arr[i - length] + arr[i]
            if current_sum >= x:
                return True
        
        return False
    
    # Binary search on the answer
    left, right = 1, n
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if check_length(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    
    return result
```

**Why this works:**
- Binary search on the answer space
- Time complexity: O(n log n)
- Good alternative approach
- Useful for understanding binary search technique

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_shortest_subarray_with_sum():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = find_shortest_subarray_with_sum(n, x, arr)
    print(result)

def find_shortest_subarray_with_sum(n, x, arr):
    """Find length of shortest subarray with sum at least x using sliding window"""
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Shrink window while sum is at least x
        while current_sum >= x and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1

# Main execution
if __name__ == "__main__":
    solve_shortest_subarray_with_sum()
```

**Why this works:**
- Optimal sliding window algorithm approach
- Handles all edge cases correctly
- Efficient sum calculation
- Clear and readable code
    
    while left <= right:
        mid = (left + right) // 2
        if check_length(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    
    return result

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 7, [2, 1, 3, 5, 2]), 2),
        ((4, 6, [1, 2, 3, 4]), 2),
        ((3, 10, [1, 2, 3]), -1),
        ((2, 5, [1, 4]), 2),
        ((1, 1, [1]), 1),
    ]
    
    for (n, x, arr), expected in test_cases:
        result = find_shortest_subarray_with_sum(n, x, arr)
        print(f"n={n}, x={x}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_shortest_subarray_with_sum(n, x, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum >= x and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with sliding window
- **Space**: O(1) - only using a few variables

### Why This Solution Works
- **Sliding Window**: Efficiently finds shortest subarray with sum at least x
- **Window Contraction**: Shrinks window while maintaining constraint
- **Optimal Algorithm**: Best known approach for positive numbers
- **Edge Case Handling**: Properly handles no valid subarray case

## 🎨 Visual Example

### Input Example
```
Input: n=5, x=7, arr=[2, 1, 3, 5, 2]
Output: 2 (shortest subarray with sum ≥ 7)
```

### Array Visualization
```
Array: [2, 1, 3, 5, 2]
Index:  0  1  2  3  4
```

### Sliding Window Process
```
Target: sum ≥ 7, find shortest length

left=0, right=0: window=[2], sum=2 < 7
left=0, right=1: window=[2,1], sum=3 < 7
left=0, right=2: window=[2,1,3], sum=6 < 7
left=0, right=3: window=[2,1,3,5], sum=11 ≥ 7 ✓
  Current length: 4
  Try to shrink: left=1, window=[1,3,5], sum=9 ≥ 7 ✓
  Try to shrink: left=2, window=[3,5], sum=8 ≥ 7 ✓
  Try to shrink: left=3, window=[5], sum=5 < 7 ✗
  Best so far: length 2
left=2, right=4: window=[3,5,2], sum=10 ≥ 7 ✓
  Current length: 3
  Try to shrink: left=3, window=[5,2], sum=7 ≥ 7 ✓
  Try to shrink: left=4, window=[2], sum=2 < 7 ✗
  Best so far: length 2

Shortest length: 2
```

### Step-by-Step Window Movement
```
Initial: left=0, right=0, sum=0, min_len=∞

Step 1: right=0, add arr[0]=2
- sum=2, window=[2]
- sum < 7, continue

Step 2: right=1, add arr[1]=1  
- sum=3, window=[2,1]
- sum < 7, continue

Step 3: right=2, add arr[2]=3
- sum=6, window=[2,1,3]
- sum < 7, continue

Step 4: right=3, add arr[3]=5
- sum=11, window=[2,1,3,5]
- sum ≥ 7 ✓, length=4
- Try shrinking: remove arr[0]=2
- sum=9, window=[1,3,5], length=3
- sum ≥ 7 ✓, try shrinking: remove arr[1]=1
- sum=8, window=[3,5], length=2
- sum ≥ 7 ✓, try shrinking: remove arr[2]=3
- sum=5, window=[5], length=1
- sum < 7 ✗, stop shrinking
- min_len = min(∞, 2) = 2

Step 5: right=4, add arr[4]=2
- sum=10, window=[3,5,2]
- sum ≥ 7 ✓, length=3
- Try shrinking: remove arr[2]=3
- sum=7, window=[5,2], length=2
- sum ≥ 7 ✓, try shrinking: remove arr[3]=5
- sum=2, window=[2], length=1
- sum < 7 ✗, stop shrinking
- min_len = min(2, 2) = 2

Final result: 2
```

### Window States Visualization
```
left=0, right=0: [2]           sum=2  < 7
left=0, right=1: [2,1]         sum=3  < 7
left=0, right=2: [2,1,3]       sum=6  < 7
left=0, right=3: [2,1,3,5]     sum=11 ≥ 7 ✓ length=4
left=1, right=3: [1,3,5]       sum=9  ≥ 7 ✓ length=3
left=2, right=3: [3,5]         sum=8  ≥ 7 ✓ length=2 ← shortest
left=3, right=3: [5]           sum=5  < 7
left=2, right=4: [3,5,2]       sum=10 ≥ 7 ✓ length=3
left=3, right=4: [5,2]         sum=7  ≥ 7 ✓ length=2
left=4, right=4: [2]           sum=2  < 7

Shortest subarray: [3,5] with length 2
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sliding Window  │ O(n)         │ O(1)         │ Two pointers │
│                 │              │              │ for window   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(1)         │ Check all    │
│                 │              │              │ subarrays    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Binary Search   │ O(n log n)   │ O(1)         │ Search for   │
│                 │              │              │ each length  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Sliding Window Technique**
- Use two pointers to maintain a valid window
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Window Contraction**
- Shrink window while maintaining constraint
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Positive Number Constraint**
- Sliding window works well for positive numbers
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Shortest Subarray with Sum Exactly K
**Problem**: Find shortest subarray with sum exactly k.

```python
def find_shortest_subarray_with_exact_sum(n, k, arr):
    from collections import defaultdict
    
    prefix_sum = 0
    min_length = float('inf')
    sum_indices = defaultdict(int)
    sum_indices[0] = -1
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum - k in sum_indices:
            length = i - sum_indices[prefix_sum - k]
            min_length = min(min_length, length)
        
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = i
    
    return min_length if min_length != float('inf') else -1

# Example usage
result = find_shortest_subarray_with_exact_sum(5, 7, [2, 1, 3, 5, 2])
print(f"Shortest subarray with exact sum 7: {result}")
```

### Variation 2: Shortest Subarray with Sum in Range
**Problem**: Find shortest subarray with sum in range [L, R].

```python
def find_shortest_subarray_with_sum_in_range(n, L, R, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Shrink window while sum is in range
        while current_sum >= L and left <= right:
            if current_sum <= R:
                min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1

# Example usage
result = find_shortest_subarray_with_sum_in_range(5, 5, 10, [2, 1, 3, 5, 2])
print(f"Shortest subarray with sum in [5, 10]: {result}")
```

### Variation 3: Shortest Subarray with Sum and Length Constraints
**Problem**: Find shortest subarray with sum at least x and length at most k.

```python
def find_shortest_subarray_with_constraints(n, x, k, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        # Shrink window while maintaining constraints
        while current_sum >= x and left <= right:
            if right - left + 1 <= k:
                min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1

# Example usage
result = find_shortest_subarray_with_constraints(5, 7, 3, [2, 1, 3, 5, 2])
print(f"Shortest subarray with sum >= 7 and length <= 3: {result}")
```

### Variation 4: Shortest Subarray with Sum and Character Constraints
**Problem**: Find shortest subarray with sum at least x where all elements are positive.

```python
def find_shortest_subarray_with_positive_constraints(n, x, arr):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        if arr[right] <= 0:
            # Reset window if we encounter non-positive number
            left = right + 1
            current_sum = 0
            continue
            
        current_sum += arr[right]
        
        while current_sum >= x and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1

# Example usage
result = find_shortest_subarray_with_positive_constraints(5, 7, [2, 1, 3, 5, 2])
print(f"Shortest subarray with sum >= 7 and all positive: {result}")
```

### Variation 5: Shortest Subarray with Sum and Range Queries
**Problem**: Answer queries about shortest subarray with sum at least x in specific ranges.

```python
def shortest_subarray_sum_queries(n, x, arr, queries):
    """Answer shortest subarray queries for specific ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= n:
            results.append(-1)
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            min_length = find_shortest_subarray_with_sum_in_range(len(subarray), x, subarray)
            results.append(min_length)
    
    return results

def find_shortest_subarray_with_sum_in_range(n, x, arr):
    """Find shortest subarray with sum at least x in a specific range"""
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum >= x and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1

# Example usage
queries = [(0, 4), (1, 3), (2, 4)]
result = shortest_subarray_sum_queries(5, 7, [2, 1, 3, 5, 2], queries)
print(f"Range query results: {result}")
```

## 🔗 Related Problems

- **[Longest Subarray with Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Longest subarray problems
- **[Fixed Length Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Fixed-size subarray problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray sum problems

## 📚 Learning Points

1. **Sliding Window Technique**: Essential for shortest subarray problems
2. **Window Contraction**: Important for maintaining constraints
3. **Binary Search Alternative**: Key for understanding different approaches
4. **Edge Case Handling**: Important for robust solutions

---

**This is a great introduction to shortest subarray with sum problems!** 🎯

## Notable Techniques

### 1. **Sliding Window Pattern**
```python
def sliding_window_shortest_subarray(arr, target):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1
```

### 2. **Binary Search on Answer Pattern**
```python
def binary_search_on_answer(arr, target):
    def check_length(length):
        # Check if length is valid
        pass
    
    left, right = 1, len(arr)
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if check_length(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    
    return result
```

### 3. **Two Pointer Technique**
```python
def two_pointer_shortest_subarray(arr, target):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('inf') else -1
```

## Edge Cases to Remember

1. **No valid subarray**: Return -1
2. **Single element**: Check if it's >= x
3. **All elements < x**: Return -1
4. **Sum of all elements < x**: Return -1
5. **Large numbers**: Use appropriate data types

## Problem-Solving Framework

1. **Identify subarray nature**: This is a shortest subarray sum problem
2. **Choose approach**: Use sliding window for efficiency
3. **Maintain constraint**: Keep sum >= x while minimizing length
4. **Track minimum**: Update minimum length when constraint is satisfied
5. **Return result**: Return the shortest valid length

---

*This analysis shows how to efficiently find the shortest subarray with sum at least x using sliding window technique.* 