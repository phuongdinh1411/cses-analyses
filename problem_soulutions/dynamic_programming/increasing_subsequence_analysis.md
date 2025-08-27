# CSES Increasing Subsequence - Problem Analysis

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
        skip = lis_recursive(index + 1, prev)
        
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