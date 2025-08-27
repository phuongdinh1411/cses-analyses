# CSES Maximum Subarray Sum - Problem Analysis

## Problem Statement
Given an array of n integers, your task is to find the maximum sum of a subarray.

### Input
The first input line has an integer n: the size of the array.
The second line has n integers x1,x2,…,xn: the contents of the array.

### Output
Print one integer: the maximum subarray sum.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- −10^9 ≤ xi ≤ 10^9

### Example
```
Input:
8
-1 3 -2 5 3 -5 2 2

Output:
12
```

## Solution Progression

### Approach 1: Brute Force - O(n³)
**Description**: Try all possible subarrays and calculate their sums.

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

**Why this is inefficient**: We're calculating the sum of each subarray from scratch, leading to O(n³) complexity. For each start and end position, we sum all elements in between.

### Improvement 1: Prefix Sum - O(n²)
**Description**: Use prefix sums to calculate subarray sums in O(1) time.

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

**Why this improvement works**: Prefix sums allow us to calculate any subarray sum in O(1) time using the formula `sum(arr[start:end+1]) = prefix[end+1] - prefix[start]`. This reduces the inner loop complexity from O(n) to O(1).

### Improvement 2: Kadane's Algorithm - O(n)
**Description**: Use dynamic programming to find the maximum subarray sum in a single pass.

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

**Why this improvement works**: At each position, we decide whether to extend the current subarray or start a new one. If extending gives a better result, we extend; otherwise, we start fresh. This gives us the optimal solution in O(n) time.

### Alternative: Divide and Conquer - O(n log n)
**Description**: Divide the array into halves, solve recursively, and combine results.

```python
def max_subarray_divide_conquer(arr):
    def max_subarray_helper(left, right):
        if left == right:
            return arr[left]
        
        mid = (left + right) // 2
        
        # Find maximum subarray in left half
        left_max = max_subarray_helper(left, mid)
        
        # Find maximum subarray in right half
        right_max = max_subarray_helper(mid + 1, right)
        
        # Find maximum subarray crossing the middle
        # Left part: from mid to left
        left_sum = 0
        left_crossing_max = float('-inf')
        for i in range(mid, left - 1, -1):
            left_sum += arr[i]
            left_crossing_max = max(left_crossing_max, left_sum)
        
        # Right part: from mid+1 to right
        right_sum = 0
        right_crossing_max = float('-inf')
        for i in range(mid + 1, right + 1):
            right_sum += arr[i]
            right_crossing_max = max(right_crossing_max, right_sum)
        
        # Maximum crossing subarray
        crossing_max = left_crossing_max + right_crossing_max
        
        return max(left_max, right_max, crossing_max)
    
    return max_subarray_helper(0, len(arr) - 1)
```

**Why this works**: We divide the problem into smaller subproblems, solve them recursively, and combine the results. The key insight is handling the case where the maximum subarray crosses the middle.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

# Kadane's algorithm
max_ending_here = arr[0]
max_so_far = arr[0]

for i in range(1, n):
    max_ending_here = max(arr[i], max_ending_here + arr[i])
    max_so_far = max(max_so_far, max_ending_here)

print(max_so_far)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Try all subarrays |
| Prefix Sum | O(n²) | O(n) | Precompute sums for O(1) lookup |
| Kadane's Algorithm | O(n) | O(1) | Dynamic programming approach |
| Divide and Conquer | O(n log n) | O(log n) | Recursive divide and conquer |

## Key Insights for Other Problems

### 1. **Dynamic Programming for Subarray Problems**
**Principle**: Use DP to build optimal solutions incrementally.
**Applicable to**:
- Maximum/minimum subarray problems
- Subarray sum problems
- Subsequence problems
- Optimization problems

**Example Problems**:
- Maximum subarray sum
- Longest increasing subsequence
- Maximum product subarray
- Subarray with given sum

### 2. **Prefix Sum Technique**
**Principle**: Precompute cumulative sums to answer range queries in O(1).
**Applicable to**:
- Range sum queries
- Subarray sum problems
- Cumulative statistics
- Range-based problems

**Example Problems**:
- Subarray sum equals k
- Range sum queries
- Maximum subarray sum
- Subarray with given sum

### 3. **Kadane's Algorithm Pattern**
**Principle**: At each step, decide whether to extend current subarray or start new one.
**Applicable to**:
- Maximum subarray problems
- Maximum subsequence problems
- Optimization problems
- Dynamic programming

**Example Problems**:
- Maximum subarray sum
- Maximum product subarray
- Longest subarray with sum k
- Maximum circular subarray sum

### 4. **Divide and Conquer for Range Problems**
**Principle**: Divide problem into smaller subproblems and combine results.
**Applicable to**:
- Range-based problems
- Merge sort variations
- Binary search applications
- Recursive problems

**Example Problems**:
- Maximum subarray sum
- Closest pair of points
- Merge sort
- Quick sort

## Notable Techniques

### 1. **Kadane's Algorithm Pattern**
```python
# Common pattern for maximum subarray
max_ending_here = arr[0]
max_so_far = arr[0]

for i in range(1, len(arr)):
    max_ending_here = max(arr[i], max_ending_here + arr[i])
    max_so_far = max(max_so_far, max_ending_here)
```

### 2. **Prefix Sum Pattern**
```python
# Calculate prefix sums
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + arr[i]

# Get sum of subarray [start, end]
subarray_sum = prefix[end + 1] - prefix[start]
```

### 3. **Divide and Conquer Pattern**
```python
def solve(left, right):
    if left == right:
        return base_case
    
    mid = (left + right) // 2
    left_result = solve(left, mid)
    right_result = solve(mid + 1, right)
    crossing_result = handle_crossing_case(left, mid, right)
    
    return combine(left_result, right_result, crossing_result)
```

## Edge Cases to Remember

1. **All negative numbers**: Maximum sum is the largest single element
2. **All positive numbers**: Maximum sum is sum of entire array
3. **Single element**: Return that element
4. **Large numbers**: Handle integer overflow
5. **Zero elements**: Handle empty array case

## Problem-Solving Framework

1. **Identify subarray nature**: This is a range-based optimization problem
2. **Consider DP approach**: Kadane's algorithm is most efficient
3. **Consider prefix sums**: Good for multiple range queries
4. **Handle edge cases**: All negative, single element, etc.
5. **Choose optimal approach**: Kadane's for single query, prefix sums for multiple

---

*This analysis shows how to systematically improve from O(n³) to O(n) and extracts reusable insights for subarray problems.* 