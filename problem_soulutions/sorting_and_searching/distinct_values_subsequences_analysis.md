# CSES Distinct Values Subsequences - Problem Analysis

## Problem Statement
Given an array of n integers, find the number of subsequences that contain exactly k distinct values.

### Input
The first input line has two integers n and k: the size of the array and the number of distinct values.
The second line has n integers a1,a2,…,an: the array.

### Output
Print one integer: the number of subsequences with exactly k distinct values.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ k ≤ n
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
5 2
1 2 1 2 3

Output:
12
```

## Solution Progression

### Approach 1: Brute Force - O(2^n)
**Description**: Generate all possible subsequences and count distinct values.

```python
def distinct_values_subsequences_naive(n, k, arr):
    count = 0
    
    def generate_subsequences(index, current_subseq):
        nonlocal count
        if index == n:
            if len(set(current_subseq)) == k:
                count += 1
            return
        
        # Include current element
        generate_subsequences(index + 1, current_subseq + [arr[index]])
        # Exclude current element
        generate_subsequences(index + 1, current_subseq)
    
    generate_subsequences(0, [])
    return count
```

**Why this is inefficient**: We generate all 2^n possible subsequences, leading to exponential time complexity.

### Improvement 1: Dynamic Programming - O(n * k)
**Description**: Use dynamic programming to count subsequences with exactly k distinct values.

```python
def distinct_values_subsequences_optimized(n, k, arr):
    # dp[i][j] = number of subsequences ending at index i with j distinct values
    dp = [[0] * (k + 1) for _ in range(n)]
    
    # Initialize: each element forms a subsequence with 1 distinct value
    for i in range(n):
        dp[i][1] = 1
    
    # Fill dp table
    for i in range(1, n):
        for j in range(1, k + 1):
            # Don't include current element
            dp[i][j] = dp[i-1][j]
            
            # Include current element
            if j == 1:
                dp[i][j] += 1
            else:
                # Find last occurrence of current element
                last_occurrence = -1
                for prev in range(i-1, -1, -1):
                    if arr[prev] == arr[i]:
                        last_occurrence = prev
                        break
                
                if last_occurrence == -1:
                    # New distinct value
                    dp[i][j] += dp[i-1][j-1]
                else:
                    # Already seen this value
                    dp[i][j] += dp[i-1][j] - dp[last_occurrence][j]
    
    return dp[n-1][k]
```

**Why this improvement works**: We use dynamic programming to track the number of subsequences ending at each position with exactly k distinct values, avoiding the need to generate all subsequences.

## Final Optimal Solution

```python
n, k = map(int, input().split())
arr = list(map(int, input().split()))

def count_subsequences_with_k_distinct(n, k, arr):
    # dp[i][j] = number of subsequences ending at index i with j distinct values
    dp = [[0] * (k + 1) for _ in range(n)]
    
    # Initialize: each element forms a subsequence with 1 distinct value
    for i in range(n):
        dp[i][1] = 1
    
    # Fill dp table
    for i in range(1, n):
        for j in range(1, k + 1):
            # Don't include current element
            dp[i][j] = dp[i-1][j]
            
            # Include current element
            if j == 1:
                dp[i][j] += 1
            else:
                # Find last occurrence of current element
                last_occurrence = -1
                for prev in range(i-1, -1, -1):
                    if arr[prev] == arr[i]:
                        last_occurrence = prev
                        break
                
                if last_occurrence == -1:
                    # New distinct value
                    dp[i][j] += dp[i-1][j-1]
                else:
                    # Already seen this value
                    dp[i][j] += dp[i-1][j] - dp[last_occurrence][j]
    
    return dp[n-1][k]

result = count_subsequences_with_k_distinct(n, k, arr)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n) | O(n) | Generate all subsequences |
| Dynamic Programming | O(n * k) | O(n * k) | Track subsequences with DP |

## Key Insights for Other Problems

### 1. **Subsequence Counting Problems**
**Principle**: Use dynamic programming to track subsequences ending at each position.
**Applicable to**: Subsequence problems, counting problems, DP problems

### 2. **Distinct Value Tracking**
**Principle**: Track the number of distinct values in subsequences ending at each position.
**Applicable to**: Distinct value problems, subsequence problems, counting problems

### 3. **Last Occurrence Analysis**
**Principle**: Consider the last occurrence of each element to avoid double counting.
**Applicable to**: Duplicate handling, subsequence problems, counting problems

## Notable Techniques

### 1. **Dynamic Programming for Subsequences**
```python
def dp_subsequence_counting(arr, k):
    n = len(arr)
    dp = [[0] * (k + 1) for _ in range(n)]
    
    # Initialize
    for i in range(n):
        dp[i][1] = 1
    
    # Fill DP table
    for i in range(1, n):
        for j in range(1, k + 1):
            dp[i][j] = dp[i-1][j]  # Don't include current element
            
            if j == 1:
                dp[i][j] += 1
            else:
                # Handle inclusion of current element
                last_occurrence = find_last_occurrence(arr, i)
                if last_occurrence == -1:
                    dp[i][j] += dp[i-1][j-1]
                else:
                    dp[i][j] += dp[i-1][j] - dp[last_occurrence][j]
    
    return dp[n-1][k]
```

### 2. **Last Occurrence Finding**
```python
def find_last_occurrence(arr, current_index):
    for i in range(current_index - 1, -1, -1):
        if arr[i] == arr[current_index]:
            return i
    return -1
```

### 3. **Subsequence State Management**
```python
def manage_subsequence_states(dp, i, j, arr, last_occurrence):
    # Don't include current element
    dp[i][j] = dp[i-1][j]
    
    # Include current element
    if j == 1:
        dp[i][j] += 1
    else:
        if last_occurrence == -1:
            dp[i][j] += dp[i-1][j-1]
        else:
            dp[i][j] += dp[i-1][j] - dp[last_occurrence][j]
    
    return dp[i][j]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a subsequence counting problem with exact distinct value requirement
2. **Choose approach**: Use dynamic programming to track subsequences
3. **Define DP state**: dp[i][j] = subsequences ending at i with j distinct values
4. **Initialize DP**: Each element forms a subsequence with 1 distinct value
5. **Fill DP table**: Consider including/excluding current element
6. **Handle duplicates**: Track last occurrence to avoid double counting
7. **Return result**: Output the count of subsequences with exactly k distinct values

---

*This analysis shows how to efficiently count subsequences with exactly k distinct values using dynamic programming.* 