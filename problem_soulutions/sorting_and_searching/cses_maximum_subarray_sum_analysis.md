---
layout: simple
title: "Maximum Subarray Sum"
permalink: /problem_soulutions/sorting_and_searching/cses_maximum_subarray_sum_analysis
---

# Maximum Subarray Sum

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand Kadane's algorithm and dynamic programming approach to maximum subarray problems
- [ ] **Objective 2**: Apply Kadane's algorithm to efficiently find maximum sum of contiguous subarrays
- [ ] **Objective 3**: Implement efficient maximum subarray algorithms with O(n) time complexity
- [ ] **Objective 4**: Optimize subarray problems using dynamic programming and greedy approaches
- [ ] **Objective 5**: Handle edge cases in maximum subarray problems (all negative numbers, single element, empty arrays)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Kadane's algorithm, dynamic programming, greedy algorithms, subarray problems, maximum sum problems
- **Data Structures**: Arrays, dynamic programming tracking, sum tracking, maximum tracking
- **Mathematical Concepts**: Subarray sums, dynamic programming theory, optimization problems, sum calculations
- **Programming Skills**: Dynamic programming implementation, greedy algorithm implementation, sum calculations, algorithm implementation
- **Related Problems**: Subarray Sum problems, Dynamic programming problems, Maximum sum problems

## Problem Description

**Problem**: Given an array of n integers, find the maximum sum of a subarray.

**Input**: 
- First line: n (size of the array)
- Second line: n integers x₁, x₂, ..., xₙ

**Output**: Maximum subarray sum.

**Example**:
```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
12

Explanation: The subarray [3, -2, 5, 3, -5, 2, 2] has sum 12.
```

## 📊 Visual Example

### Input Array
```
Array: [-1, 3, -2, 5, 3, -5, 2, 2]
Index:   0  1   2  3  4   5  6  7
```

### Kadane's Algorithm Process
```
Step 1: Initialize
┌─────────────────────────────────────┐
│ max_ending_here = 0                 │
│ max_so_far = -∞                     │
└─────────────────────────────────────┘

Step 2: Process each element
┌─────────────────────────────────────┐
│ i=0, arr[0]=-1                     │
│ max_ending_here = max(-1, 0+(-1)) = -1│
│ max_so_far = max(-∞, -1) = -1      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ i=1, arr[1]=3                      │
│ max_ending_here = max(3, -1+3) = 3  │
│ max_so_far = max(-1, 3) = 3        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ i=2, arr[2]=-2                     │
│ max_ending_here = max(-2, 3+(-2)) = 1│
│ max_so_far = max(3, 1) = 3         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ i=3, arr[3]=5                      │
│ max_ending_here = max(5, 1+5) = 6   │
│ max_so_far = max(3, 6) = 6         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ i=4, arr[4]=3                      │
│ max_ending_here = max(3, 6+3) = 9   │
│ max_so_far = max(6, 9) = 9         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ i=5, arr[5]=-5                     │
│ max_ending_here = max(-5, 9+(-5)) = 4│
│ max_so_far = max(9, 4) = 9         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ i=6, arr[6]=2                      │
│ max_ending_here = max(2, 4+2) = 6   │
│ max_so_far = max(9, 6) = 9         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ i=7, arr[7]=2                      │
│ max_ending_here = max(2, 6+2) = 8   │
│ max_so_far = max(9, 8) = 9         │
└─────────────────────────────────────┘
```

### Subarray Verification
```
Let's verify the maximum subarray:

Subarray [1,4]: [3, -2, 5, 3]
- Sum: 3 + (-2) + 5 + 3 = 9

Subarray [1,7]: [3, -2, 5, 3, -5, 2, 2]
- Sum: 3 + (-2) + 5 + 3 + (-5) + 2 + 2 = 8

Subarray [3,4]: [5, 3]
- Sum: 5 + 3 = 8

Subarray [1,4]: [3, -2, 5, 3]
- Sum: 3 + (-2) + 5 + 3 = 9

Maximum sum: 9
```

### Key Insight
```
Kadane's Algorithm:
- At each position, decide whether to extend the current subarray
  or start a new one
- If extending gives a better result, extend
- Otherwise, start fresh from current element
- Keep track of the maximum seen so far
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the maximum sum of any contiguous subarray
- Subarray must be consecutive elements
- Can include negative numbers
- Need to handle all possible subarrays

**Key Observations:**
- Can use dynamic programming approach
- At each position, decide to extend or start new subarray
- Kadane's algorithm is optimal
- Need to handle negative numbers correctly

### Step 2: Brute Force Approach
**Idea**: Try all possible subarrays and calculate their sums.

```python
def max_subarray_brute_force(arr):
    n = len(arr)
    max_sum = float('-inf')
    
    for start in range(n):
        for end in range(start, n):
            # Calculate sum of subarray from start to end
            current_sum = 0
            for i in range(start, end + 1):
                current_sum += arr[i]
            max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this works:**
- Checks all possible subarrays
- Guaranteed to find the maximum
- Simple to understand and implement

### Step 3: Prefix Sum Optimization
**Idea**: Use prefix sums to calculate subarray sums efficiently.

```python
def max_subarray_prefix_sum(arr):
    n = len(arr)
    
    # Calculate prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    max_sum = float('-inf')
    
    for start in range(n):
        for end in range(start, n):
            # Sum of subarray from start to end = prefix[end+1] - prefix[start]
            current_sum = prefix[end + 1] - prefix[start]
            max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this is better:**
- Prefix sums allow O(1) subarray sum calculation
- Reduces complexity from O(n³) to O(n²)
- Still checks all subarrays but more efficiently

### Step 4: Kadane's Algorithm
**Idea**: Use dynamic programming to find maximum in single pass.

```python
def max_subarray_kadane(arr):
    n = len(arr)
    
    max_ending_here = arr[0]  # Maximum sum ending at current position
    max_so_far = arr[0]       # Maximum sum found so far
    
    for i in range(1, n):
        # Either extend the previous subarray or start a new one
        max_ending_here = max(arr[i], max_ending_here + arr[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far
```

**Why this is optimal:**
- Single pass through array: O(n) time
- At each position, decide to extend or start new
- Dynamic programming approach
- Handles negative numbers correctly

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_maximum_subarray_sum():
    n = int(input())
    arr = list(map(int, input().split()))
    
    # Kadane's algorithm
    max_ending_here = arr[0]
    max_so_far = arr[0]
    
    for i in range(1, n):
        max_ending_here = max(arr[i], max_ending_here + arr[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    print(max_so_far)

# Main execution
if __name__ == "__main__":
    solve_maximum_subarray_sum()
```

**Why this works:**
- Optimal time complexity O(n)
- Handles all edge cases
- Simple and efficient implementation

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([-1, 3, -2, 5, 3, -5, 2, 2], 12),
        ([-2, -3, 4, -1, -2, 1, 5, -3], 7),
        ([1, 2, 3, 4, 5], 15),
        ([-1, -2, -3, -4], -1),
        ([5], 5),
    ]
    
    for arr, expected in test_cases:
        result = solve_test(arr)
        print(f"Array: {arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(arr):
    n = len(arr)
    
    max_ending_here = arr[0]
    max_so_far = arr[0]
    
    for i in range(1, n):
        max_ending_here = max(arr[i], max_ending_here + arr[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through array
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Dynamic Programming**: Optimal substructure
- **Greedy Choice**: Extend or start new at each position
- **Correctness**: Guaranteed to find maximum subarray

## 🎯 Key Insights

### 1. **Kadane's Algorithm**
- At each position, decide to extend or start new
- `max_ending_here = max(arr[i], max_ending_here + arr[i])`
- Track global maximum separately
- Handles negative numbers correctly

### 2. **Dynamic Programming**
- Optimal substructure: solution depends on subproblems
- Overlapping subproblems: reuse previous results
- Bottom-up approach: build solution iteratively

### 3. **Greedy Choice**
- Always choose the better option at each step
- Either extend current subarray or start new one
- This greedy choice leads to optimal solution

## 🎯 Problem Variations

### Variation 1: Maximum Subarray with Length Constraint
**Problem**: Find maximum subarray sum with minimum/maximum length constraints.

```python
def max_subarray_with_length_constraint(arr, min_len, max_len):
    n = len(arr)
    
    # Use sliding window approach
    max_sum = float('-inf')
    current_sum = 0
    window_start = 0
    
    for window_end in range(n):
        current_sum += arr[window_end]
        
        # Shrink window if it exceeds max_len
        while window_end - window_start + 1 > max_len:
            current_sum -= arr[window_start]
            window_start += 1
        
        # Check if window meets minimum length
        if window_end - window_start + 1 >= min_len:
            max_sum = max(max_sum, current_sum)
    
    return max_sum
```

### Variation 2: Maximum Subarray with Non-negative Constraint
**Problem**: Find maximum subarray sum where all elements are non-negative.

```python
def max_subarray_non_negative(arr):
    n = len(arr)
    
    max_sum = 0
    current_sum = 0
    
    for i in range(n):
        if arr[i] >= 0:
            current_sum += arr[i]
            max_sum = max(max_sum, current_sum)
        else:
            current_sum = 0  # Reset if negative
    
    return max_sum
```

### Variation 3: Maximum Subarray with Circular Array
**Problem**: Array is circular. Find maximum subarray sum.

```python
def max_subarray_circular(arr):
    n = len(arr)
    
    # Case 1: Maximum subarray doesn't wrap around
    max_normal = kadane_algorithm(arr)
    
    # Case 2: Maximum subarray wraps around
    # This is equivalent to total sum - minimum subarray sum
    total_sum = sum(arr)
    min_subarray = kadane_algorithm([-x for x in arr])
    max_wrapped = total_sum + min_subarray
    
    return max(max_normal, max_wrapped)

def kadane_algorithm(arr):
    n = len(arr)
    max_ending_here = arr[0]
    max_so_far = arr[0]
    
    for i in range(1, n):
        max_ending_here = max(arr[i], max_ending_here + arr[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far
```

### Variation 4: Maximum Subarray with K Negations
**Problem**: Find maximum subarray sum after negating at most k elements.

```python
def max_subarray_with_k_negations(arr, k):
    n = len(arr)
    
    # Use sliding window with priority queue
    from heapq import heappush, heappop
    
    max_sum = float('-inf')
    current_sum = 0
    negations = []
    
    for i in range(n):
        current_sum += arr[i]
        
        # If element is negative, consider negating it
        if arr[i] < 0:
            heappush(negations, arr[i])
        
        # If we have too many negations, remove the smallest
        while len(negations) > k:
            smallest_neg = heappop(negations)
            current_sum -= 2 * smallest_neg  # Remove negation
        
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

### Variation 5: Maximum Subarray with Target Sum
**Problem**: Find subarray with sum closest to target.

```python
def subarray_closest_to_target(arr, target):
    n = len(arr)
    
    # Use prefix sums and binary search
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    closest_sum = float('inf')
    closest_diff = float('inf')
    
    for start in range(n):
        for end in range(start, n):
            current_sum = prefix[end + 1] - prefix[start]
            diff = abs(current_sum - target)
            
            if diff < closest_diff:
                closest_diff = diff
                closest_sum = current_sum
    
    return closest_sum
```

## 🔗 Related Problems

- **[Subarray Sums I](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_sums_i_analysis)**: Subarray sum problems
- **[Subarray Sums II](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_sums_ii_analysis)**: Advanced subarray problems
- **[Array Division](/cses-analyses/problem_soulutions/sorting_and_searching/array_division_analysis)**: Array optimization

## 📚 Learning Points

1. **Kadane's Algorithm**: Classic dynamic programming approach
2. **Dynamic Programming**: Optimal substructure and overlapping subproblems
3. **Greedy Algorithms**: Making optimal local choices
4. **Array Processing**: Efficient array manipulation techniques

---

**This is a great introduction to dynamic programming and Kadane's algorithm!** 🎯 