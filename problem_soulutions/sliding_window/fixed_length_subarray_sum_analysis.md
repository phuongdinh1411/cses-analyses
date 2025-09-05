---
layout: simple
title: "Fixed Length Subarray Sum Analysis"
permalink: /problem_soulutions/sliding_window/fixed_length_subarray_sum_analysis
---


# Fixed Length Subarray Sum Analysis

## Problem Description

**Problem**: Given an array of n integers and a fixed length k, find the maximum sum of a subarray of length k.

**Input**: 
- n: the size of the array
- k: the fixed subarray length
- arr: array of n integers

**Output**: The maximum sum of a subarray of length k.

**Example**:
```
Input:
5 3
2 1 3 5 2

Output:
10

Explanation: 
The subarrays of length 3 are:
- [2, 1, 3] → sum = 6
- [1, 3, 5] → sum = 9
- [3, 5, 2] → sum = 10 (maximum)
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the maximum sum among all subarrays of fixed length k
- Use efficient algorithms to avoid brute force
- Handle edge cases properly
- Optimize for large inputs

**Key Observations:**
- Subarray length is fixed at k
- Windows overlap significantly
- We can reuse previous calculations
- Need to track maximum sum found

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays of length k and calculate their sums.

```python
def fixed_length_subarray_sum_naive(n, k, arr):
    max_sum = float('-inf')
    
    for i in range(n - k + 1):
        current_sum = sum(arr[i:i + k])
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this is inefficient:**
- For each window, we recalculate the sum from scratch
- Time complexity: O(n × k)
- Lots of redundant calculations
- Not scalable for large inputs

### Step 3: Optimization with Sliding Window
**Idea**: Use sliding window technique to maintain a running sum and avoid recalculating.

```python
def fixed_length_subarray_sum_sliding_window(n, k, arr):
    # Calculate sum of first window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this improvement works:**
- Instead of recalculating the sum for each window, we maintain a running sum
- Subtract the old element and add the new element
- Time complexity: O(n)
- Much more efficient for large inputs

### Step 4: Alternative Approach with Prefix Sum
**Idea**: Use prefix sum to calculate subarray sums in constant time.

```python
def fixed_length_subarray_sum_prefix_sum(n, k, arr):
    # Calculate prefix sum
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    # Find maximum sum of subarrays of length k
    max_sum = float('-inf')
    for i in range(n - k + 1):
        current_sum = prefix_sum[i + k] - prefix_sum[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this works:**
- Prefix sum allows us to calculate subarray sums in constant time
- Time complexity: O(n) for preprocessing + O(n) for queries
- Space complexity: O(n) for storing prefix sums
- Good alternative when multiple queries are needed

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_fixed_length_subarray_sum():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = find_maximum_fixed_length_sum(n, k, arr)
    print(result)

def find_maximum_fixed_length_sum(n, k, arr):
    """Find maximum sum of subarrays with fixed length k using sliding window"""
    if k > n:
        return 0
    
    # Calculate sum of first window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Main execution
if __name__ == "__main__":
    solve_fixed_length_subarray_sum()
```

**Why this works:**
- Optimal sliding window algorithm approach
- Handles all edge cases correctly
- Efficient sum calculation
- Clear and readable code
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 3, [2, 1, 3, 5, 2]), 10),
        ((4, 2, [1, 2, 3, 4]), 7),
        ((3, 3, [1, 2, 3]), 6),
        ((5, 1, [1, 2, 3, 4, 5]), 5),
        ((4, 4, [1, 2, 3, 4]), 10),
    ]
    
    for (n, k, arr), expected in test_cases:
        result = find_maximum_fixed_length_sum(n, k, arr)
        print(f"n={n}, k={k}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_maximum_fixed_length_sum(n, k, arr):
    if k > n:
        return 0
    
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the array with sliding window
- **Space**: O(1) - only using a few variables

### Why This Solution Works
- **Sliding Window**: Efficiently finds maximum sum without recalculating
- **Running Sum**: Maintains current window sum by adding/removing elements
- **Optimal Algorithm**: Best known approach for this problem
- **Edge Case Handling**: Properly handles cases where k > n

## 🎨 Visual Example

### Input Example
```
Input: n=5, k=3, arr=[2, 1, 3, 5, 2]
Output: 10 (maximum sum of subarray of length 3)
```

### Array Visualization
```
Array: [2, 1, 3, 5, 2]
Index:  0  1  2  3  4
```

### All Subarrays of Length 3
```
Subarray [0:3] = [2, 1, 3]     → sum = 2+1+3 = 6
Subarray [1:4] = [1, 3, 5]     → sum = 1+3+5 = 9
Subarray [2:5] = [3, 5, 2]     → sum = 3+5+2 = 10 ← maximum

Maximum sum: 10
```

### Sliding Window Process
```
Window size: k = 3
Initial window: indices [0, 1, 2]

Step 1: Calculate initial sum
- Window: [2, 1, 3]
- Sum: 2 + 1 + 3 = 6
- Max sum: 6

Step 2: Slide window right
- Remove: arr[0] = 2
- Add: arr[3] = 5
- Window: [1, 3, 5]
- Sum: 6 - 2 + 5 = 9
- Max sum: max(6, 9) = 9

Step 3: Slide window right
- Remove: arr[1] = 1
- Add: arr[4] = 2
- Window: [3, 5, 2]
- Sum: 9 - 1 + 2 = 10
- Max sum: max(9, 10) = 10

Final result: 10
```

### Step-by-Step Window Movement
```
Initial: left=0, right=2, sum=6, max_sum=6

Step 1: left=0, right=2
- Window: [2, 1, 3]
- Sum: 2 + 1 + 3 = 6
- Max sum: 6

Step 2: left=1, right=3
- Remove arr[0]=2, add arr[3]=5
- Window: [1, 3, 5]
- Sum: 6 - 2 + 5 = 9
- Max sum: max(6, 9) = 9

Step 3: left=2, right=4
- Remove arr[1]=1, add arr[4]=2
- Window: [3, 5, 2]
- Sum: 9 - 1 + 2 = 10
- Max sum: max(9, 10) = 10

Final result: 10
```

### Window States Visualization
```
left=0, right=2: [2,1,3]       sum=6  max=6
left=1, right=3: [1,3,5]       sum=9  max=9
left=2, right=4: [3,5,2]       sum=10 max=10 ← final

Maximum subarray: [3, 5, 2] with sum 10
```

### Different Examples
```
Example 1: arr=[1, 2, 3, 4, 5], k=2
- Subarrays: [1,2], [2,3], [3,4], [4,5]
- Sums: 3, 5, 7, 9
- Maximum: 9

Example 2: arr=[5, 1, 3, 2, 4], k=3
- Subarrays: [5,1,3], [1,3,2], [3,2,4]
- Sums: 9, 6, 9
- Maximum: 9

Example 3: arr=[1, 1, 1, 1], k=2
- Subarrays: [1,1], [1,1], [1,1]
- Sums: 2, 2, 2
- Maximum: 2
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sliding Window  │ O(n)         │ O(1)         │ Fixed size   │
│                 │              │              │ window       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(nk)        │ O(1)         │ Check all    │
│                 │              │              │ subarrays    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Prefix Sum      │ O(n)         │ O(n)         │ Precompute   │
│                 │              │              │ sums         │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Sliding Window Technique**
- Use fixed-size window that slides through the array
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Running Sum Maintenance**
- Add new element and subtract old element
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Fixed Length Optimization**
- Avoid recalculating sums for overlapping parts
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Minimum Fixed Length Sum
**Problem**: Find the minimum sum of any subarray of length k.

```python
def find_minimum_fixed_length_sum(n, k, arr):
    if k > n:
        return 0
    
    current_sum = sum(arr[:k])
    min_sum = current_sum
    
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] + arr[i]
        min_sum = min(min_sum, current_sum)
    
    return min_sum

# Example usage
result = find_minimum_fixed_length_sum(5, 3, [2, 1, 3, 5, 2])
print(f"Minimum fixed length sum: {result}")
```

### Variation 2: Fixed Length with Constraints
**Problem**: Find maximum sum of subarrays of length k where all elements are positive.

```python
def find_maximum_positive_fixed_length_sum(n, k, arr):
    if k > n:
        return 0
    
    # Check if first window is valid
    if any(x <= 0 for x in arr[:k]):
        return float('-inf')
    
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    for i in range(k, n):
        # Check if new window is valid
        if arr[i - k] <= 0 or arr[i] <= 0:
            # Recalculate sum for new window
            current_sum = sum(arr[i - k + 1:i + 1])
            if any(x <= 0 for x in arr[i - k + 1:i + 1]):
                continue
        else:
            current_sum = current_sum - arr[i - k] + arr[i]
        
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
result = find_maximum_positive_fixed_length_sum(5, 3, [2, 1, 3, 5, 2])
print(f"Maximum positive fixed length sum: {result}")
```

### Variation 3: Fixed Length with Range Queries
**Problem**: Answer queries about maximum fixed length sum in specific ranges.

```python
def fixed_length_sum_queries(n, k, arr, queries):
    """Answer fixed length sum queries for specific ranges"""
    results = []
    
    for start, end in queries:
        if end - start + 1 < k:
            results.append(0)  # Range too small
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            max_sum = find_maximum_fixed_length_sum_in_range(len(subarray), k, subarray)
            results.append(max_sum)
    
    return results

def find_maximum_fixed_length_sum_in_range(n, k, arr):
    """Find maximum fixed length sum in a specific range"""
    if k > n:
        return 0
    
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
queries = [(0, 4), (1, 3), (2, 4)]
result = fixed_length_sum_queries(5, 3, [2, 1, 3, 5, 2], queries)
print(f"Range query results: {result}")
```

### Variation 4: Fixed Length with Circular Array
**Problem**: Find maximum sum of subarrays of length k in a circular array.

```python
def find_maximum_circular_fixed_length_sum(n, k, arr):
    if k > n:
        return 0
    
    # Handle circular case by extending array
    extended_arr = arr + arr[:k-1]
    
    current_sum = sum(extended_arr[:k])
    max_sum = current_sum
    
    for i in range(k, len(extended_arr)):
        current_sum = current_sum - extended_arr[i - k] + extended_arr[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
result = find_maximum_circular_fixed_length_sum(5, 3, [2, 1, 3, 5, 2])
print(f"Maximum circular fixed length sum: {result}")
```

### Variation 5: Fixed Length with Weights
**Problem**: Each element has a weight, find maximum weighted sum of subarrays of length k.

```python
def find_maximum_weighted_fixed_length_sum(n, k, arr, weights):
    if k > n:
        return 0
    
    # Calculate weighted sum of first window
    current_sum = sum(arr[i] * weights[i] for i in range(k))
    max_sum = current_sum
    
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] * weights[i - k] + arr[i] * weights[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
weights = [1, 2, 1, 2, 1]
result = find_maximum_weighted_fixed_length_sum(5, 3, [2, 1, 3, 5, 2], weights)
print(f"Maximum weighted fixed length sum: {result}")
```

## 🔗 Related Problems

- **[Sliding Window Advertisement](/cses-analyses/problem_soulutions/sliding_window/)**: Fixed-size subarray problems
- **[Maximum Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Maximum sum problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray sum problems

## 📚 Learning Points

1. **Sliding Window Technique**: Essential for fixed-size subarray problems
2. **Running Sum Maintenance**: Important for efficient calculations
3. **Fixed Length Optimization**: Key for avoiding redundant work
4. **Edge Case Handling**: Important for robust solutions

---

**This is a great introduction to fixed length subarray problems!** 🎯
    
    return max_sum
```

### 2. **Prefix Sum Pattern**
```python
def prefix_sum_fixed_length(arr, k):
    n = len(arr)
    prefix_sum = [0] * (n + 1)
    
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    
    max_sum = float('-inf')
    for i in range(n - k + 1):
        current_sum = prefix_sum[i + k] - prefix_sum[i]
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

### 3. **Window Maintenance Pattern**
```python
def maintain_fixed_window(arr, k, operation):
    # Initialize window
    window = arr[:k]
    result = operation(window)
    
    # Slide window
    for i in range(k, len(arr)):
        window.pop(0)  # Remove oldest element
        window.append(arr[i])  # Add newest element
        result = max(result, operation(window))
    
    return result
```

## Edge Cases to Remember

1. **k = 1**: Return maximum element
2. **k = n**: Return sum of all elements
3. **All negative numbers**: Return sum of k consecutive negative numbers
4. **All positive numbers**: Return sum of k consecutive positive numbers
5. **Large numbers**: Use appropriate data types

## Problem-Solving Framework

1. **Identify fixed length nature**: This is a fixed length subarray problem
2. **Choose approach**: Use sliding window for efficiency
3. **Initialize window**: Calculate sum of first window
4. **Slide window**: Maintain sum by adding new and removing old elements
5. **Track maximum**: Update maximum sum when needed

---

*This analysis shows how to efficiently find the maximum sum of subarrays with fixed length using sliding window technique.* 