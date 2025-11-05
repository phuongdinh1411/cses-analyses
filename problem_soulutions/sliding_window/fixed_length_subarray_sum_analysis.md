---
layout: simple
title: "Fixed Length Subarray Sum - Sliding Window Technique"
permalink: /problem_soulutions/sliding_window/fixed_length_subarray_sum_analysis
---

# Fixed Length Subarray Sum - Sliding Window Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement sliding window technique for fixed-size subarrays
- Apply efficient window management for subarray problems
- Optimize subarray sum calculations using sliding window
- Handle edge cases in fixed-length subarray problems
- Recognize when to use sliding window vs other approaches

## 📋 Problem Description

Given an array of integers and a fixed length k, find the maximum sum of any contiguous subarray of length k.

**Input**: 
- First line: n (number of elements) and k (subarray length)
- Second line: n integers separated by spaces

**Output**: 
- Single integer: maximum sum of any contiguous subarray of length k

**Constraints**:
- 1 ≤ k ≤ n ≤ 10⁵
- -10⁴ ≤ arr[i] ≤ 10⁴

**Example**:
```
Input:
6 3
-2 1 -3 4 -1 2

Output:
5

Explanation**: 
The subarrays of length 3 are:
[-2, 1, -3] = -4
[1, -3, 4] = 2
[-3, 4, -1] = 0
[4, -1, 2] = 5  ← Maximum sum
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible subarrays of fixed length k
- **Complete Coverage**: Guarantees finding the optimal solution by examining all possibilities
- **Simple Implementation**: Straightforward loop to generate all subarrays of length k
- **Inefficient**: Recalculates sums for overlapping subarrays

**Key Insight**: Generate all possible subarrays of length k and calculate their sums to find the maximum.

**Algorithm**:
- For each starting position i from 0 to n-k
- Calculate sum of subarray from i to i+k-1
- Keep track of maximum sum found

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2], k = 3

All subarrays of length 3:
i=0: [-2, 1, -3] = -4
i=1: [1, -3, 4] = 2
i=2: [-3, 4, -1] = 0
i=3: [4, -1, 2] = 5  ← Maximum sum

Maximum sum: 5
```

**Implementation**:
```python
def brute_force_fixed_length_subarray_sum(arr, k):
    """
    Find maximum sum of subarray of fixed length k using brute force
    
    Args:
        arr: List of integers
        k: Length of subarray
    
    Returns:
        int: Maximum sum of any contiguous subarray of length k
    """
    n = len(arr)
    max_sum = float('-inf')
    
    for i in range(n - k + 1):
        # Calculate sum of subarray from i to i+k-1
        current_sum = sum(arr[i:i+k])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
k = 3
result = brute_force_fixed_length_subarray_sum(arr, k)
print(f"Brute force result: {result}")  # Output: 5
```

**Time Complexity**: O(n×k) - For each position, calculate sum of k elements
**Space Complexity**: O(1) - Only using constant extra space

**Why it's inefficient**: Recalculates overlapping sums, leading to redundant work.

---

### Approach 2: Optimized with Prefix Sums

**Key Insights from Optimized Approach**:
- **Prefix Sum Optimization**: Use prefix sums to calculate subarray sums in O(1) time
- **Efficiency Improvement**: Reduce time complexity from O(n×k) to O(n)
- **Space Trade-off**: Use O(n) extra space for prefix sums to speed up calculations
- **Better Performance**: Significantly faster than brute force for larger inputs

**Key Insight**: Precompute prefix sums to eliminate the need to recalculate subarray sums.

**Algorithm**:
- Calculate prefix sum array where prefix[i] = sum of elements from 0 to i
- For each starting position i from 0 to n-k
- Calculate subarray sum as prefix[i+k-1] - prefix[i-1] (or prefix[i+k-1] if i=0)
- Keep track of maximum sum found

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2], k = 3
Prefix: [-2, -1, -4, 0, -1, 1]

Subarray sums using prefix:
i=0: prefix[2] = -4
i=1: prefix[3] - prefix[0] = 0 - (-2) = 2
i=2: prefix[4] - prefix[1] = -1 - (-1) = 0
i=3: prefix[5] - prefix[2] = 1 - (-4) = 5  ← Maximum sum

Maximum sum: 5
```

**Implementation**:
```python
def optimized_fixed_length_subarray_sum(arr, k):
    """
    Find maximum sum of subarray of fixed length k using prefix sums
    
    Args:
        arr: List of integers
        k: Length of subarray
    
    Returns:
        int: Maximum sum of any contiguous subarray of length k
    """
    n = len(arr)
    
    # Calculate prefix sums
    prefix = [0] * n
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i-1] + arr[i]
    
    max_sum = float('-inf')
    
    for i in range(n - k + 1):
        # Calculate subarray sum using prefix sums
        if i == 0:
            current_sum = prefix[i + k - 1]
        else:
            current_sum = prefix[i + k - 1] - prefix[i - 1]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
k = 3
result = optimized_fixed_length_subarray_sum(arr, k)
print(f"Optimized result: {result}")  # Output: 5
```

**Time Complexity**: O(n) - Single pass for prefix sums, single pass for finding maximum
**Space Complexity**: O(n) - Prefix sum array

**Why it's better**: Much faster than brute force, but uses extra space.

---

### Approach 3: Optimal with Sliding Window

**Key Insights from Optimal Approach**:
- **Sliding Window Technique**: Maintain a window of fixed size k and slide it across the array
- **Efficient Updates**: Add new element and remove old element in O(1) time
- **Optimal Complexity**: Achieve O(n) time and O(1) space complexity
- **No Redundant Calculations**: Each element is added and removed exactly once

**Key Insight**: Use sliding window to maintain current sum efficiently by adding new element and removing old element.

**Algorithm**:
- Calculate sum of first k elements
- For each position i from k to n-1:
  - Add arr[i] to current sum
  - Remove arr[i-k] from current sum
  - Update maximum sum if current sum is greater
- Return maximum sum

**Visual Example**:
```
Array: [-2, 1, -3, 4, -1, 2], k = 3

Initial window: [-2, 1, -3], sum = -4
Slide right: Remove -2, add 4
New window: [1, -3, 4], sum = -4 - (-2) + 4 = 2
Slide right: Remove 1, add -1
New window: [-3, 4, -1], sum = 2 - 1 + (-1) = 0
Slide right: Remove -3, add 2
New window: [4, -1, 2], sum = 0 - (-3) + 2 = 5  ← Maximum sum

Maximum sum: 5
```

**Implementation**:
```python
def optimal_fixed_length_subarray_sum(arr, k):
    """
    Find maximum sum of subarray of fixed length k using sliding window
    
    Args:
        arr: List of integers
        k: Length of subarray
    
    Returns:
        int: Maximum sum of any contiguous subarray of length k
    """
    n = len(arr)
    
    # Calculate sum of first k elements
    current_sum = sum(arr[:k])
    max_sum = current_sum
    
    # Slide the window
    for i in range(k, n):
        # Add new element and remove old element
        current_sum = current_sum + arr[i] - arr[i - k]
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example usage
arr = [-2, 1, -3, 4, -1, 2]
k = 3
result = optimal_fixed_length_subarray_sum(arr, k)
print(f"Optimal result: {result}")  # Output: 5
```

**Time Complexity**: O(n) - Single pass through the array
**Space Complexity**: O(1) - Only using constant extra space

**Why it's optimal**: Best possible time complexity with minimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n×k) | O(1) | Check all possible subarrays of length k |
| Optimized | O(n) | O(n) | Use prefix sums for faster calculation |
| Optimal | O(n) | O(1) | Use sliding window technique |

### Time Complexity
- **Time**: O(n) - Single pass through the array
- **Space**: O(1) - Only using constant extra space

### Why This Solution Works
- **Sliding Window**: Maintain a window of fixed size and slide it efficiently
- **Efficient Updates**: Add new element and remove old element in O(1) time
- **No Redundant Calculations**: Each element is processed exactly once
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Fixed Length Subarray Sum with Range Queries**
**Problem**: Find sum of subarrays of fixed length k for multiple range queries.

**Key Differences**: Handle multiple queries efficiently

**Solution Approach**: Precompute all sums and answer queries in O(1)

**Implementation**:
```python
def fixed_length_subarray_sum_queries(arr, k, queries):
    """
    Answer multiple queries for fixed length subarray sums
    """
    n = len(arr)
    if k > n:
        return [0] * len(queries)
    
    # Precompute all sums using sliding window
    sums = []
    current_sum = sum(arr[:k])
    sums.append(current_sum)
    
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] + arr[i]
        sums.append(current_sum)
    
    # Answer queries
    results = []
    for l, r in queries:
        if l < 0 or r >= len(sums) or l > r:
            results.append(0)
        else:
            results.append(sum(sums[l:r+1]))
    
    return results

# Example usage
arr = [1, 2, 3, 4, 5, 6]
k = 3
queries = [(0, 1), (1, 2), (0, 2)]
result = fixed_length_subarray_sum_queries(arr, k, queries)
print(f"Fixed length subarray sum queries: {result}")  # Output: [9, 12, 21]
```

#### **2. Fixed Length Subarray Sum with Updates**
**Problem**: Find sum of subarrays of fixed length k with array update operations.

**Key Differences**: Array can be updated between queries

**Solution Approach**: Use segment tree or maintain sliding window with updates

**Implementation**:
```python
def fixed_length_subarray_sum_with_updates(arr, k, updates):
    """
    Find fixed length subarray sums with array updates
    """
    n = len(arr)
    if k > n:
        return []
    
    results = []
    
    for update in updates:
        if update[0] == 'update':
            idx, val = update[1], update[2]
            arr[idx] = val
        else:  # query
            if k > n:
                results.append(0)
            else:
                current_sum = sum(arr[:k])
                max_sum = current_sum
                
                for i in range(k, n):
                    current_sum = current_sum - arr[i - k] + arr[i]
                    max_sum = max(max_sum, current_sum)
                
                results.append(max_sum)
    
    return results

# Example usage
arr = [1, 2, 3, 4, 5]
k = 3
updates = [('query',), ('update', 1, 10), ('query',)]
result = fixed_length_subarray_sum_with_updates(arr, k, updates)
print(f"Fixed length subarray sum with updates: {result}")
```

#### **3. Fixed Length Subarray Sum with Constraints**
**Problem**: Find sum of subarrays of fixed length k that satisfy certain constraints.

**Key Differences**: Add constraints to the subarray selection

**Solution Approach**: Use sliding window with constraint checking

**Implementation**:
```python
def fixed_length_subarray_sum_constraints(arr, k, constraints):
    """
    Find fixed length subarray sums with constraints
    """
    n = len(arr)
    if k > n:
        return []
    
    results = []
    current_sum = sum(arr[:k])
    
    # Check if first window satisfies constraints
    if satisfies_constraints(arr[:k], constraints):
        results.append(current_sum)
    
    # Slide window and check constraints
    for i in range(k, n):
        current_sum = current_sum - arr[i - k] + arr[i]
        current_window = arr[i - k + 1:i + 1]
        
        if satisfies_constraints(current_window, constraints):
            results.append(current_sum)
    
    return results

def satisfies_constraints(window, constraints):
    """
    Check if window satisfies given constraints
    """
    if 'min_sum' in constraints and sum(window) < constraints['min_sum']:
        return False
    if 'max_sum' in constraints and sum(window) > constraints['max_sum']:
        return False
    if 'min_element' in constraints and min(window) < constraints['min_element']:
        return False
    if 'max_element' in constraints and max(window) > constraints['max_element']:
        return False
    return True

# Example usage
arr = [1, 2, 3, 4, 5, 6]
k = 3
constraints = {'min_sum': 6, 'max_sum': 12}
result = fixed_length_subarray_sum_constraints(arr, k, constraints)
print(f"Fixed length subarray sum with constraints: {result}")  # Output: [6, 9, 12]
```

### Related Problems

#### **CSES Problems**
- [Fixed Length Subarray Sum](https://cses.fi/problemset/task/2101) - Find sum of subarrays of fixed length
- [Sliding Window Maximum](https://cses.fi/problemset/task/2102) - Find maximum in sliding window
- [Sliding Window Minimum](https://cses.fi/problemset/task/2103) - Find minimum in sliding window

#### **LeetCode Problems**
- [Maximum Sum of 3 Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/) - Multiple fixed-length subarrays
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) - Maximum in sliding window
- [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) - Median in sliding window
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) - Variable window

#### **Problem Categories**
- **Sliding Window**: Fixed-size windows, efficient window management, window optimization
- **Array Processing**: Subarray analysis, sum calculation, window operations
- **Query Processing**: Range queries, update operations, constraint checking
- **Optimization**: Performance optimization, space efficiency, algorithm efficiency

## 🚀 Key Takeaways

- **Sliding Window Technique**: The standard approach for fixed-size subarray problems
- **Efficient Window Management**: Add and remove elements in O(1) time
- **Space Optimization**: Can achieve O(1) space complexity with careful implementation
- **Pattern Recognition**: This technique applies to many fixed-size window problems
- **Performance**: Much more efficient than recalculating sums for each window