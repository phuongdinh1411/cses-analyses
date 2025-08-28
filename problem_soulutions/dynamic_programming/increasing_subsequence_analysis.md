---
layout: simple
title: "Increasing Subsequence
permalink: /problem_soulutions/dynamic_programming/increasing_subsequence_analysis/
---

# Increasing Subsequence

## Problem Statement
Given an array of n integers, find the length of the longest increasing subsequence (LIS).

### Input
The first input line has an integer n: the size of the array.
The second line has n integers a1,a2,…,an: the array.

### Output
Print one integer: the length of the longest increasing subsequence.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
8
7 3 5 3 6 2 9 8

Output:
4
```

## Solution Progression

### Approach 1: Recursive - O(2^n)
**Description**: Use recursive approach to find LIS.

```python
def increasing_subsequence_naive(n, arr):
    def lis_recursive(index, prev):
        if index == n:
            return 0
        
        # Skip current element
        skip = lis_recursive(index + 1, prev)"
        # Include current element if it's greater than previous
        include = 0
        if arr[index] > prev:
            include = 1 + lis_recursive(index + 1, arr[index])
        
        return max(skip, include)
    
    return lis_recursive(0, float('-inf'))
```

**Why this is inefficient**: We have overlapping subproblems, leading to exponential time complexity.

### Improvement 1: Dynamic Programming - O(n²)
**Description**: Use 1D DP array to store LIS ending at each position.

```python
def increasing_subsequence_optimized(n, arr):
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

**Why this improvement works**: We use a 1D DP array where dp[i] represents the length of LIS ending at position i. We fill the array by checking all previous positions.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

def find_longest_increasing_subsequence(n, arr):
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

result = find_longest_increasing_subsequence(n, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Overlapping subproblems |
| Dynamic Programming | O(n²) | O(n) | Use 1D DP array |

## Key Insights for Other Problems

### 1. **Longest Increasing Subsequence**
**Principle**: Use 1D DP to find the longest increasing subsequence in an array.
**Applicable to**: Sequence problems, DP problems, optimization problems

### 2. **1D Dynamic Programming**
**Principle**: Use 1D DP array to store optimal solutions ending at each position.
**Applicable to**: Sequence problems, optimization problems, DP problems

### 3. **Subsequence Optimization**
**Principle**: Find optimal subsequences by considering all previous positions.
**Applicable to**: Subsequence problems, optimization problems, sequence problems

## Notable Techniques

### 1. **1D DP Array Construction**
```python
def build_1d_dp_array(n):
    return [1] * n
```

### 2. **LIS Update**
```python
def update_lis(dp, arr, i):
    for j in range(i):
        if arr[i] > arr[j]:
            dp[i] = max(dp[i], dp[j] + 1)
```

### 3. **DP Array Filling**
```python
def fill_dp_array(arr, n):
    dp = build_1d_dp_array(n)
    
    for i in range(1, n):
        update_lis(dp, arr, i)
    
    return max(dp)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a longest increasing subsequence problem
2. **Choose approach**: Use 1D dynamic programming
3. **Define DP state**: dp[i] = length of LIS ending at position i
4. **Base case**: dp[i] = 1 for all i
5. **Recurrence relation**: dp[i] = max(dp[j] + 1) for all j < i where arr[i] > arr[j]
6. **Fill DP array**: Iterate through all positions
7. **Return result**: Output maximum value in dp array

---

*This analysis shows how to efficiently find the longest increasing subsequence using 1D dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Longest Decreasing Subsequence**
**Problem**: Find the length of the longest decreasing subsequence.
```python
def longest_decreasing_subsequence(n, arr):
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] < arr[j]:  # Changed condition
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

#### **Variation 2: Longest Non-Decreasing Subsequence**
**Problem**: Find the length of the longest non-decreasing subsequence (allows equal elements).
```python
def longest_nondecreasing_subsequence(n, arr):
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] >= arr[j]:  # Changed condition
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

#### **Variation 3: Count All Increasing Subsequences**
**Problem**: Count the total number of increasing subsequences.
```python
def count_increasing_subsequences(n, arr):
    dp = [1] * n  # dp[i] = count of LIS ending at i
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] += dp[j]
    
    return sum(dp)
```

#### **Variation 4: Longest Increasing Subsequence with Sum**
**Problem**: Find the longest increasing subsequence with maximum sum.
```python
def lis_with_max_sum(n, arr):
    dp = [arr[i] for i in range(n)]  # dp[i] = max sum of LIS ending at i
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + arr[i])
    
    return max(dp)
```

#### **Variation 5: Longest Increasing Subsequence with Constraints**
**Problem**: Find LIS where adjacent elements differ by at most k.
```python
def constrained_lis(n, arr, k):
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j] and arr[i] - arr[j] <= k:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

### 🔗 **Related Problems & Concepts**

#### **1. Subsequence Problems**
- **Longest Common Subsequence**: Find LCS of two strings
- **Longest Palindromic Subsequence**: Find LPS in a string
- **Maximum Sum Subsequence**: Find subsequence with max sum
- **Bitonic Subsequence**: Increasing then decreasing

#### **2. Dynamic Programming Patterns**
- **1D DP**: Single state variable (position)
- **2D DP**: Two state variables (position, previous value)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Sequence Analysis**
- **Monotonic Sequences**: Always increasing/decreasing
- **Peak Finding**: Find local maxima/minima
- **Pattern Matching**: Find specific patterns in sequences
- **Sequence Alignment**: Align similar sequences

#### **4. Optimization Problems**
- **Longest Path**: Find longest path in DAG
- **Shortest Path**: Find shortest path in graph
- **Resource Allocation**: Optimal use of limited resources
- **Scheduling**: Optimal arrangement of tasks

#### **5. Algorithmic Techniques**
- **Binary Search**: Optimize LIS to O(n log n)
- **Segment Trees**: Range queries on sequences
- **Fenwick Trees**: Efficient prefix sums
- **Sparse Tables**: Range minimum/maximum queries

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    result = longest_increasing_subsequence(n, arr)
    print(result)
```

#### **2. Range Queries on LIS**
```python
def range_lis_queries(n, arr, queries):
    # Precompute LIS for all ranges
    results = []
    
    for l, r in queries:
        subarray = arr[l:r+1]
        lis_length = longest_increasing_subsequence(len(subarray), subarray)
        results.append(lis_length)
    
    return results
```

#### **3. Interactive LIS Problems**
```python
def interactive_lis_game():
    n = int(input())
    arr = list(map(int, input().split()))
    
    # Player tries to find LIS
    player_guess = int(input())
    actual_lis = longest_increasing_subsequence(n, arr)
    
    if player_guess == actual_lis:
        print("Correct!")
    else:
        print(f"Wrong! Actual LIS length is {actual_lis}")
```

### 🧮 **Mathematical Extensions**

#### **1. Expected LIS Length**
- **Random Permutations**: Average LIS length in random arrays
- **Probability Analysis**: Probability of specific LIS lengths
- **Asymptotic Behavior**: LIS behavior for large arrays
- **Distribution Analysis**: Distribution of LIS lengths

#### **2. Advanced LIS Algorithms**
- **Patience Sorting**: O(n log n) algorithm using patience game
- **Binary Search Optimization**: Use binary search for O(n log n)
- **Segment Tree Approach**: Use segment trees for range queries
- **Parallel Algorithms**: Parallel LIS computation

#### **3. Geometric Interpretations**
- **Dilworth's Theorem**: Relate LIS to chain decomposition
- **Erdős–Szekeres Theorem**: Guaranteed LIS/LDS in permutations
- **Young Tableaux**: Connect LIS to Young diagrams
- **Schensted Correspondence**: Bijection between permutations and pairs of Young tableaux

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Patience Sorting**: Efficient LIS algorithm
- **Merge Sort**: Divide and conquer sorting
- **Binary Search**: Efficient searching in sorted arrays
- **Segment Trees**: Range query data structures

#### **2. Mathematical Concepts**
- **Combinatorics**: Permutation and combination theory
- **Probability Theory**: Random processes and outcomes
- **Order Theory**: Partial orders and chains
- **Group Theory**: Permutation groups and symmetries

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Algorithm Optimization**: Time and space complexity improvements
- **Data Structures**: Efficient storage and retrieval
- **Problem Reduction**: Transform problems to known algorithms

---

*This analysis demonstrates the versatility of the LIS problem and its connections to various algorithmic and mathematical concepts.* 