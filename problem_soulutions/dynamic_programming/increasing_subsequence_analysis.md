---
layout: simple
title: "Increasing Subsequence"
permalink: /problem_soulutions/dynamic_programming/increasing_subsequence_analysis
---


# Increasing Subsequence

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand subsequence problems and longest increasing subsequence optimization
- Apply DP techniques to solve subsequence problems with increasing constraints
- Implement efficient DP solutions for LIS and subsequence optimization
- Optimize DP solutions using space-efficient techniques and subsequence tracking
- Handle edge cases in subsequence DP (decreasing arrays, single elements, all equal elements)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, subsequence problems, LIS algorithms, subsequence optimization
- **Data Structures**: Arrays, DP tables, subsequence tracking structures
- **Mathematical Concepts**: Subsequence theory, increasing sequences, optimization principles, sequence analysis
- **Programming Skills**: Array manipulation, subsequence calculations, iterative programming, DP implementation
- **Related Problems**: Longest Common Subsequence (subsequence problems), Edit Distance (string DP), Sequence problems

## Problem Description

Given an array of n integers, find the length of the longest increasing subsequence (LIS). A subsequence is a sequence that can be derived from the array by deleting some elements without changing the order of the remaining elements.

**Input**: 
- First line: integer n (size of the array)
- Second line: n integers a1, a2, ..., an (the array elements)

**Output**: 
- Print the length of the longest increasing subsequence

**Constraints**:
- 1 ≤ n ≤ 2 × 10^5
- 1 ≤ ai ≤ 10^9
- Find longest increasing subsequence length
- Elements must be in strictly increasing order
- Can skip elements but cannot reorder
- Subsequence must be increasing

**Example**:
```
Input:
8
7 3 5 3 6 2 9 8

Output:
4

Explanation**: 
The longest increasing subsequence is [3, 5, 6, 9] with length 4.
Other valid LIS include [3, 5, 6, 8] and [3, 3, 6, 9].
```

## Visual Example

### Input and Problem Setup
```
Input: n = 8, arr = [7, 3, 5, 3, 6, 2, 9, 8]

Goal: Find longest increasing subsequence length
Subsequence: Elements in same order, can skip elements
Result: Length of longest increasing subsequence
Note: Elements must be in strictly increasing order
```

### Subsequence Analysis
```
For array [7, 3, 5, 3, 6, 2, 9, 8]:

Position 0: 7 → Can start LIS of length 1
Position 1: 3 → Can start LIS of length 1, cannot extend 7
Position 2: 5 → Can extend LIS from 3, length 2
Position 3: 3 → Cannot extend any LIS, can start new LIS of length 1
Position 4: 6 → Can extend LIS from 3,5, length 3
Position 5: 2 → Cannot extend any LIS, can start new LIS of length 1
Position 6: 9 → Can extend LIS from 3,5,6, length 4
Position 7: 8 → Can extend LIS from 3,5,6, length 4

LIS: [3, 5, 6, 9] (length 4)
```

### Dynamic Programming Pattern
```
DP State: dp[i] = length of LIS ending at position i

Base case: dp[i] = 1 (each element forms LIS of length 1)

Recurrence: dp[i] = max(dp[j] + 1) for all j < i where arr[j] < arr[i]

Key insight: Use 1D DP to handle subsequence optimization
```

### State Transition Visualization
```
Building DP array for arr = [7, 3, 5, 3, 6, 2, 9, 8]:

Initialize: dp = [1, 1, 1, 1, 1, 1, 1, 1]

Position 0: arr[0] = 7
dp[0] = 1 (base case)

Position 1: arr[1] = 3
dp[1] = 1 (cannot extend any previous LIS)

Position 2: arr[2] = 5
dp[2] = max(dp[0] + 1, dp[1] + 1) = max(2, 2) = 2

Position 3: arr[3] = 3
dp[3] = 1 (cannot extend any previous LIS)

Position 4: arr[4] = 6
dp[4] = max(dp[0] + 1, dp[1] + 1, dp[2] + 1, dp[3] + 1) = max(2, 2, 3, 2) = 3

Position 5: arr[5] = 2
dp[5] = 1 (cannot extend any previous LIS)

Position 6: arr[6] = 9
dp[6] = max(dp[0] + 1, dp[1] + 1, dp[2] + 1, dp[3] + 1, dp[4] + 1, dp[5] + 1) = max(2, 2, 3, 2, 4, 2) = 4

Position 7: arr[7] = 8
dp[7] = max(dp[0] + 1, dp[1] + 1, dp[2] + 1, dp[3] + 1, dp[4] + 1, dp[5] + 1, dp[6] + 1) = max(2, 2, 3, 2, 4, 2, 5) = 5

Final: max(dp) = 4 (LIS length)
```

### Key Insight
The solution works by:
1. Using 1D dynamic programming to handle subsequence optimization
2. For each position, considering all previous positions
3. Building solutions from smaller subproblems
4. Using optimal substructure property
5. Time complexity: O(n²) for filling DP array
6. Space complexity: O(n) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible subsequences recursively
- Use recursive approach to explore all increasing subsequence possibilities
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. For each position, try including or skipping the current element
2. If including, ensure it's greater than the previous element
3. Recursively explore all valid subsequence paths
4. Return maximum length found

**Visual Example:**
```
Brute force approach: Try all possible subsequences
For array [7, 3, 5]:

Recursive tree:
                    (0, -∞)
              /            \
          (1, -∞)        (1, 7)
         /      \        /      \
    (2, -∞)  (2, 3)  (2, 7)  (2, 7)
   /    \     /  \   /  \     /  \
(3, -∞) (3, 5) (3, 3) (3, 5) (3, 7) (3, 7) (3, 7) (3, 7)
```

**Implementation:**
```python
def increasing_subsequence_brute_force(arr):
    def count_lis(index, last_element):
        if index == len(arr):
            return 0
        
        # Skip current element
        skip = count_lis(index + 1, last_element)
        
        # Include current element if valid
        include = 0
        if arr[index] > last_element:
            include = 1 + count_lis(index + 1, arr[index])
        
        return max(skip, include)
    
    return count_lis(0, float('-inf'))

def solve_increasing_subsequence_brute_force():
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = increasing_subsequence_brute_force(arr)
    print(result)
```

**Time Complexity:** O(2^n) for trying all possible subsequences
**Space Complexity:** O(n) for recursion depth

**Why it's inefficient:**
- O(2^n) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large arrays
- Poor performance with exponential growth

### Approach 2: Dynamic Programming (Better)

**Key Insights from DP Solution:**
- Use 1D DP array to store LIS length ending at each position
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. For each position, check all previous positions
3. If current element is greater, extend the LIS
4. Keep track of maximum length found

**Visual Example:**
```
DP approach: Build solutions iteratively
For arr = [7, 3, 5, 3, 6, 2, 9, 8]:

Initialize: dp = [1, 1, 1, 1, 1, 1, 1, 1]

After processing: dp = [1, 1, 2, 1, 3, 1, 4, 4]

Final result: max(dp) = 4
```

**Implementation:**
```python
def increasing_subsequence_dp(arr):
    n = len(arr)
    # dp[i] = length of LIS ending at position i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

def solve_increasing_subsequence_dp():
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = increasing_subsequence_dp(arr)
    print(result)
```

**Time Complexity:** O(n²) for filling DP array
**Space Complexity:** O(n) for DP array

**Why it's better:**
- O(n²) time complexity is much better than O(2^n)
- Uses dynamic programming for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Binary Search + DP (Optimal)

**Key Insights from Optimized Solution:**
- Use binary search to find the position to insert each element
- Maintain an array of smallest tail elements for each LIS length
- Each element can either extend an existing LIS or start a new one
- Use binary search to find the correct position efficiently

**Algorithm:**
1. Maintain an array of smallest tail elements for each LIS length
2. For each element, use binary search to find insertion position
3. If element is larger than all tails, extend the LIS
4. Otherwise, replace the first element that's not smaller

**Visual Example:**
```
Optimized DP: Use binary search for efficient insertion
For arr = [7, 3, 5, 3, 6, 2, 9, 8]:

tails = []
For 7: tails = [7]
For 3: tails = [3] (replace 7)
For 5: tails = [3, 5] (extend)
For 3: tails = [3, 5] (no change)
For 6: tails = [3, 5, 6] (extend)
For 2: tails = [2, 5, 6] (replace 3)
For 9: tails = [2, 5, 6, 9] (extend)
For 8: tails = [2, 5, 6, 8] (replace 9)
```

**Implementation:**
```python
def solve_increasing_subsequence():
    n = int(input())
    arr = list(map(int, input().split()))
    
    tails = []
    
    for num in arr:
        # Find position to insert num using binary search
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        if left == len(tails):
            tails.append(num)  # Extend LIS
        else:
            tails[left] = num  # Replace element
    
    print(len(tails))

# Main execution
if __name__ == "__main__":
    solve_increasing_subsequence()
```

**Time Complexity:** O(n log n) for binary search for each element
**Space Complexity:** O(n) for tails array

**Why it's optimal:**
- O(n log n) time complexity is optimal for this problem
- Uses binary search for efficient element insertion
- Most efficient approach for competitive programming
- Standard method for subsequence optimization problems

## 🎯 Problem Variations

### Variation 1: Longest Increasing Subsequence with Path Reconstruction
**Problem**: Find the actual LIS sequence, not just the length.

**Link**: [CSES Problem Set - LIS Path](https://cses.fi/problemset/task/lis_path)

```python
def longest_increasing_subsequence_path(arr):
    n = len(arr)
    dp = [1] * n
    parent = [-1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    
    # Find the end of the longest subsequence
    max_length = max(dp)
    end_index = dp.index(max_length)
    
    # Reconstruct the path
    lis = []
    while end_index != -1:
        lis.append(arr[end_index])
        end_index = parent[end_index]
    
    return lis[::-1]
```

### Variation 2: Longest Increasing Subsequence with Different Constraints
**Problem**: Find LIS with additional constraints (e.g., element differences).

**Link**: [CSES Problem Set - LIS Constraints](https://cses.fi/problemset/task/lis_constraints)

```python
def longest_increasing_subsequence_constraints(arr, min_diff):
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j] and arr[i] - arr[j] >= min_diff:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

### Variation 3: Longest Increasing Subsequence with Multiple Arrays
**Problem**: Find LIS across multiple arrays.

**Link**: [CSES Problem Set - LIS Multiple](https://cses.fi/problemset/task/lis_multiple)

```python
def longest_increasing_subsequence_multiple(arrays):
    all_elements = []
    for i, arr in enumerate(arrays):
        for j, val in enumerate(arr):
            all_elements.append((val, i, j))
    
    # Sort by value
    all_elements.sort()
    
    # Find LIS with array index constraint
    n = len(all_elements)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if (all_elements[i][0] > all_elements[j][0] and 
                all_elements[i][1] >= all_elements[j][1]):
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

## 🔗 Related Problems

- **[Longest Common Subsequence](/cses-analyses/problem_soulutions/dynamic_programming/)**: Subsequence problems
- **[Edit Distance](/cses-analyses/problem_soulutions/dynamic_programming/)**: String DP problems
- **[Sequence Problems](/cses-analyses/problem_soulutions/sorting_and_searching/)**: Sequence optimization problems
- **[Grid Paths](/cses-analyses/problem_soulutions/dynamic_programming/)**: 2D DP problems

## 📚 Learning Points

1. **Subsequence Problems**: Essential for understanding LIS and subsequence optimization
2. **Dynamic Programming**: Key technique for solving subsequence problems efficiently
3. **Array Processing**: Important for understanding how to handle subsequence calculations
4. **Binary Search**: Critical for understanding how to optimize subsequence problems
5. **Optimal Substructure**: Foundation for building solutions from smaller subproblems
6. **Bottom-Up DP**: Critical for building solutions from smaller subproblems

## 📝 Summary

The Increasing Subsequence problem demonstrates subsequence optimization and dynamic programming principles for efficient sequence analysis. We explored three approaches:

1. **Recursive Brute Force**: O(2^n) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n²) time complexity using 1D DP, better approach for subsequence problems
3. **Binary Search + DP**: O(n log n) time complexity with binary search optimization, optimal approach for competitive programming

The key insights include understanding subsequence optimization principles, using dynamic programming for efficient computation, and applying binary search techniques for subsequence problems. This problem serves as an excellent introduction to subsequence algorithms in competitive programming.
