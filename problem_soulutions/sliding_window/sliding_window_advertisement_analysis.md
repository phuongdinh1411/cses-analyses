---
layout: simple
title: "Sliding Window Advertisement Analysis"
permalink: /problem_soulutions/sliding_window/sliding_window_advertisement_analysis
---


# Sliding Window Advertisement Analysis

## Problem Description

**Problem**: Given an array of n integers and a window size k, find the maximum sum of any subarray of size k.

**Input**: 
- n: the size of the array
- k: the window size
- arr: array of n integers

**Output**: The maximum sum of any subarray of size k.

**Example**:
```
Input:
5 3
1 2 3 4 5

Output:
12

Explanation: 
The subarrays of size 3 are:
- [1, 2, 3] → sum = 6
- [2, 3, 4] → sum = 9  
- [3, 4, 5] → sum = 12 (maximum)
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the maximum sum among all subarrays of fixed size k
- Use sliding window technique for efficiency
- Avoid recalculating sums for overlapping windows
- Handle edge cases properly

**Key Observations:**
- Window size is fixed at k
- Windows overlap significantly
- We can reuse previous calculations
- Need to track maximum sum found

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays of size k and calculate their sums.

```python
def sliding_window_sum_naive(n, k, arr):
    max_sum = float('-inf')
    
    for i in range(n - k + 1):
        current_sum = sum(arr[i:i+k])
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
def sliding_window_sum_optimal(n, k, arr):
    # Calculate sum of first window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Add new element and remove old element
        current_sum = current_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

**Why this improvement works:**
- Instead of recalculating the sum for each window, we maintain a running sum
- Add the new element and subtract the old element
- Time complexity: O(n)
- Much more efficient for large inputs

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_sliding_window_advertisement():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    result = find_maximum_window_sum(n, k, arr)
    print(result)

def find_maximum_window_sum(n, k, arr):
    """Find maximum sum of any subarray of size k using sliding window"""
    if k > n:
        return 0
    
    # Calculate sum of first window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Add new element and remove old element
        current_sum = current_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Main execution
if __name__ == "__main__":
    solve_sliding_window_advertisement()
```

**Why this works:**
- Optimal sliding window algorithm approach
- Handles all edge cases correctly
- Efficient sum calculation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((5, 3, [1, 2, 3, 4, 5]), 12),
        ((4, 2, [1, 2, 3, 4]), 7),
        ((3, 3, [1, 2, 3]), 6),
        ((5, 1, [1, 2, 3, 4, 5]), 5),
        ((4, 4, [1, 2, 3, 4]), 10),
    ]
    
    for (n, k, arr), expected in test_cases:
        result = find_maximum_window_sum(n, k, arr)
        print(f"n={n}, k={k}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_maximum_window_sum(n, k, arr):
    if k > n:
        return 0
    
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    for i in range(k, n):
        current_sum = current_sum + arr[i] - arr[i - k]
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
Input: n=5, k=3, arr=[1, 2, 3, 4, 5]
Output: 12 (maximum sum of subarray of size 3)
```

### Array Visualization
```
Array: [1, 2, 3, 4, 5]
Index:  0  1  2  3  4
```

### All Subarrays of Size 3
```
Subarray [0:3] = [1, 2, 3]     → sum = 1+2+3 = 6
Subarray [1:4] = [2, 3, 4]     → sum = 2+3+4 = 9
Subarray [2:5] = [3, 4, 5]     → sum = 3+4+5 = 12 ← maximum

Maximum sum: 12
```

### Sliding Window Process
```
Window size: k = 3
Initial window: indices [0, 1, 2]

Step 1: Calculate initial sum
- Window: [1, 2, 3]
- Sum: 1 + 2 + 3 = 6
- Max sum: 6

Step 2: Slide window right
- Remove: arr[0] = 1
- Add: arr[3] = 4
- Window: [2, 3, 4]
- Sum: 6 - 1 + 4 = 9
- Max sum: max(6, 9) = 9

Step 3: Slide window right
- Remove: arr[1] = 2
- Add: arr[4] = 5
- Window: [3, 4, 5]
- Sum: 9 - 2 + 5 = 12
- Max sum: max(9, 12) = 12

Final result: 12
```

### Step-by-Step Window Movement
```
Initial: left=0, right=2, sum=6, max_sum=6

Step 1: left=0, right=2
- Window: [1, 2, 3]
- Sum: 1 + 2 + 3 = 6
- Max sum: 6

Step 2: left=1, right=3
- Remove arr[0]=1, add arr[3]=4
- Window: [2, 3, 4]
- Sum: 6 - 1 + 4 = 9
- Max sum: max(6, 9) = 9

Step 3: left=2, right=4
- Remove arr[1]=2, add arr[4]=5
- Window: [3, 4, 5]
- Sum: 9 - 2 + 5 = 12
- Max sum: max(9, 12) = 12

Final result: 12
```

### Window States Visualization
```
left=0, right=2: [1,2,3]       sum=6  max=6
left=1, right=3: [2,3,4]       sum=9  max=9
left=2, right=4: [3,4,5]       sum=12 max=12 ← final

Maximum subarray: [3, 4, 5] with sum 12
```

### Different Examples
```
Example 1: arr=[5, 1, 3, 2, 4], k=3
- Subarrays: [5,1,3], [1,3,2], [3,2,4]
- Sums: 9, 6, 9
- Maximum: 9

Example 2: arr=[2, 1, 5, 1, 3, 2], k=3
- Subarrays: [2,1,5], [1,5,1], [5,1,3], [1,3,2]
- Sums: 8, 7, 9, 6
- Maximum: 9

Example 3: arr=[1, 1, 1, 1, 1], k=2
- Subarrays: [1,1], [1,1], [1,1], [1,1]
- Sums: 2, 2, 2, 2
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

### 3. **Overlapping Window Optimization**
- Avoid recalculating sums for overlapping parts
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Minimum Window Sum
**Problem**: Find the minimum sum of any subarray of size k.

```python
def find_minimum_window_sum(n, k, arr):
    if k > n:
        return 0
    
    # Calculate sum of first window
    current_sum = sum(arr[:k])
    min_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Add new element and remove old element
        current_sum = current_sum + arr[i] - arr[i - k]
        min_sum = min(min_sum, current_sum)
    
    return min_sum

# Example usage
result = find_minimum_window_sum(5, 3, [1, 2, 3, 4, 5])
print(f"Minimum window sum: {result}")
```

### Variation 2: Variable Window Size
**Problem**: Find the maximum sum of any subarray with size at most k.

```python
def find_maximum_variable_window_sum(n, k, arr):
    max_sum = float('-inf')
    current_sum = 0
    left = 0
    
    for right in range(n):
        current_sum += arr[right]
        
        # Try to shrink window from left
        while left <= right and right - left + 1 > k:
            current_sum -= arr[left]
            left += 1
        
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
result = find_maximum_variable_window_sum(5, 3, [1, 2, 3, 4, 5])
print(f"Maximum variable window sum: {result}")
```

### Variation 3: Window with Constraints
**Problem**: Find maximum sum of any subarray of size k where no two adjacent elements are negative.

```python
def find_maximum_constrained_window_sum(n, k, arr):
    if k > n:
        return 0
    
    # Check if first window is valid
    valid_first = True
    for i in range(k - 1):
        if arr[i] < 0 and arr[i + 1] < 0:
            valid_first = False
            break
    
    if not valid_first:
        return float('-inf')
    
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Check if new window is valid
        valid_new = True
        if arr[i - k] < 0 and arr[i - k + 1] < 0:
            valid_new = False
        if arr[i - 1] < 0 and arr[i] < 0:
            valid_new = False
        
        if valid_new:
            current_sum = current_sum + arr[i] - arr[i - k]
            max_sum = max(max_sum, current_sum)
        else:
            # Recalculate sum for new window
            current_sum = sum(arr[i - k + 1:i + 1])
            max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
result = find_maximum_constrained_window_sum(5, 3, [1, -2, 3, -4, 5])
print(f"Maximum constrained window sum: {result}")
```

### Variation 4: Circular Array Window
**Problem**: Find maximum sum of any subarray of size k in a circular array.

```python
def find_maximum_circular_window_sum(n, k, arr):
    if k > n:
        return 0
    
    # Handle circular case by extending array
    extended_arr = arr + arr[:k-1]
    
    # Calculate sum of first window
    current_sum = sum(extended_arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, len(extended_arr)):
        current_sum = current_sum + extended_arr[i] - extended_arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
result = find_maximum_circular_window_sum(5, 3, [1, 2, 3, 4, 5])
print(f"Maximum circular window sum: {result}")
```

### Variation 5: Window with Range Queries
**Problem**: Answer queries about maximum window sum in specific ranges.

```python
def maximum_window_sum_queries(n, k, arr, queries):
    """Answer maximum window sum queries for specific ranges"""
    results = []
    
    for start, end in queries:
        if end - start + 1 < k:
            results.append(0)  # Window too small
        else:
            # Extract subarray for this range
            subarray = arr[start:end + 1]
            max_sum = find_maximum_window_sum_in_range(len(subarray), k, subarray)
            results.append(max_sum)
    
    return results

def find_maximum_window_sum_in_range(n, k, arr):
    """Find maximum window sum in a specific range"""
    if k > n:
        return 0
    
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    for i in range(k, n):
        current_sum = current_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
queries = [(0, 4), (1, 3), (2, 4)]
result = maximum_window_sum_queries(5, 3, [1, 2, 3, 4, 5], queries)
print(f"Range query results: {result}")
```

## 🔗 Related Problems

- **[Fixed Length Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Fixed-size subarray problems
- **[Maximum Subarray Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Maximum sum problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray sum problems

## 📚 Learning Points

1. **Sliding Window Technique**: Essential for fixed-size subarray problems
2. **Running Sum Maintenance**: Important for efficient calculations
3. **Window Optimization**: Key for avoiding redundant work
4. **Edge Case Handling**: Important for robust solutions

---

**This is a great introduction to sliding window algorithms!** 🎯

## Key Insights for Other Problems

### 1. **Fixed Window Size Problems**
**Principle**: Use sliding window to efficiently process fixed-size windows without recalculating.
**Applicable to**: Fixed window problems, subarray problems, sliding window applications

### 2. **Running Sum Technique**
**Principle**: Maintain a running sum/count to avoid recalculating for each window.
**Applicable to**: Sum problems, average problems, sliding window optimizations

### 3. **Window Maintenance**
**Principle**: Add new elements and remove old elements to maintain the current window state.
**Applicable to**: Window-based problems, stream processing, real-time algorithms

## Notable Techniques

### 1. **Sliding Window Sum Pattern**
```python
def sliding_window_sum_pattern(arr, k):
    if len(arr) < k:
        return 0
    
    # Initialize first window
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide window
    for i in range(k, len(arr)):
        current_sum = current_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

### 2. **Generic Sliding Window Pattern**
```python
def generic_sliding_window(arr, k):
    if len(arr) < k:
        return 0
    
    # Initialize window
    window_sum = sum(arr[:k])
    result = window_sum
    
    # Slide window
    for i in range(k, len(arr)):
        window_sum = window_sum + arr[i] - arr[i - k]
        result = max(result, window_sum)  # or min, or other operation
    
    return result
```

## Problem-Solving Framework

1. **Identify window size**: This is a fixed-size window problem (size k)
2. **Choose approach**: Use sliding window with running sum for efficiency
3. **Initialize window**: Calculate sum of first k elements
4. **Slide window**: Add new element, remove old element, update result
5. **Return maximum**: Track the maximum sum found

---

*This analysis shows how to efficiently find the maximum sum of any subarray of fixed size k using sliding window technique.* 