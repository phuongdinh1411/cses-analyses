# CSES Longest Common Subsequence - Problem Analysis

## Problem Statement
Given two strings, find the length of their longest common subsequence (LCS). A subsequence is a sequence that can be derived from another sequence by deleting some elements without changing the order of the remaining elements.

### Input
The first input line has a string s.
The second input line has a string t.

### Output
Print one integer: the length of the longest common subsequence.

### Constraints
- 1 ≤ |s|, |t| ≤ 5000

### Example
```
Input:
AYXT
AYZXT

Output:
4
```

## Solution Progression

### Approach 1: Recursive - O(2^(n+m))
**Description**: Use recursive approach to find LCS.

```python
def longest_common_subsequence_naive(s, t):
    def lcs_recursive(i, j):
        if i == 0 or j == 0:
            return 0
        
        if s[i-1] == t[j-1]:
            return 1 + lcs_recursive(i-1, j-1)
        else:
            return max(lcs_recursive(i-1, j), lcs_recursive(i, j-1))
    
    return lcs_recursive(len(s), len(t))
```

**Why this is inefficient**: We have overlapping subproblems, leading to exponential time complexity.

### Improvement 1: Dynamic Programming - O(n*m)
**Description**: Use 2D DP table to store results of subproblems.

```python
def longest_common_subsequence_optimized(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[n][m]
```

**Why this improvement works**: We use a 2D DP table where dp[i][j] represents the length of LCS of s[0:i] and t[0:j]. We fill the table using the recurrence relation.

## Final Optimal Solution

```python
s = input()
t = input()

def find_longest_common_subsequence(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[n][m]

result = find_longest_common_subsequence(s, t)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^(n+m)) | O(n+m) | Overlapping subproblems |
| Dynamic Programming | O(n*m) | O(n*m) | Use 2D DP table |

## Key Insights for Other Problems

### 1. **Longest Common Subsequence**
**Principle**: Use 2D DP to find the longest common subsequence between two sequences.
**Applicable to**: String problems, sequence problems, DP problems

### 2. **2D Dynamic Programming**
**Principle**: Use 2D DP table to store results of subproblems for sequence alignment.
**Applicable to**: Sequence problems, alignment problems, DP problems

### 3. **Recurrence Relations**
**Principle**: Use recurrence relations to build optimal solutions from smaller subproblems.
**Applicable to**: DP problems, optimization problems, sequence problems

## Notable Techniques

### 1. **2D DP Table Construction**
```python
def build_2d_dp_table(n, m):
    return [[0] * (m + 1) for _ in range(n + 1)]
```

### 2. **LCS Recurrence**
```python
def lcs_recurrence(dp, s, t, i, j):
    if s[i-1] == t[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1
    else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[i][j]
```

### 3. **DP Table Filling**
```python
def fill_dp_table(s, t):
    n, m = len(s), len(t)
    dp = build_2d_dp_table(n, m)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            lcs_recurrence(dp, s, t, i, j)
    
    return dp[n][m]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a longest common subsequence problem
2. **Choose approach**: Use 2D dynamic programming
3. **Define DP state**: dp[i][j] = LCS length of s[0:i] and t[0:j]
4. **Base case**: dp[0][j] = dp[i][0] = 0
5. **Recurrence relation**: 
   - If s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + 1
   - Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
6. **Fill DP table**: Iterate through all states
7. **Return result**: Output dp[n][m]

---

*This analysis shows how to efficiently find the longest common subsequence using 2D dynamic programming.* 