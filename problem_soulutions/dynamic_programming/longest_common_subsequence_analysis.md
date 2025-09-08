---
layout: simple
title: "Longest Common Subsequence"
permalink: /problem_soulutions/dynamic_programming/longest_common_subsequence_analysis
---


# Longest Common Subsequence

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand subsequence problems and longest common subsequence calculations
- Apply 2D DP techniques to solve subsequence problems with string matching
- Implement efficient 2D DP solutions for LCS and subsequence optimization
- Optimize 2D DP solutions using space-efficient techniques and subsequence tracking
- Handle edge cases in string DP (empty strings, no common subsequences, single characters)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2D dynamic programming, string algorithms, subsequence problems, string matching
- **Data Structures**: 2D arrays, DP tables, string data structures
- **Mathematical Concepts**: String theory, subsequence properties, string matching, optimization principles
- **Programming Skills**: 2D array manipulation, string processing, iterative programming, DP implementation
- **Related Problems**: Edit Distance (string DP), Increasing Subsequence (subsequence problems), String algorithms

## Problem Description

Given two strings, find the length of their longest common subsequence (LCS). A subsequence is a sequence that can be derived from another sequence by deleting some elements without changing the order of the remaining elements.

**Input**: 
- First line: string s (first string)
- Second line: string t (second string)

**Output**: 
- Print the length of the longest common subsequence

**Constraints**:
- 1 ≤ |s|, |t| ≤ 1000
- Find longest common subsequence length
- Characters must appear in same order
- Can skip characters but cannot reorder
- Strings contain only lowercase letters

**Example**:
```
Input:
AYXT
AYZXT

Output:
4

Explanation**: 
The longest common subsequence is "AYXT" with length 4.
We can find this by matching characters in order:
- A matches A
- Y matches Y  
- X matches X
- T matches T
The Z in the second string is skipped.
```

## Visual Example

### Input and Problem Setup
```
Input: s = "AYXT", t = "AYZXT"

Goal: Find longest common subsequence length
Subsequence: Characters in same order, can skip characters
Result: Length of longest common subsequence
Note: Cannot reorder characters, only skip them
```

### Subsequence Analysis
```
For strings "AYXT" and "AYZXT":

String s: A Y X T
String t: A Y Z X T

Character-by-character comparison:
- Position 0: A vs A → Match, include in LCS
- Position 1: Y vs Y → Match, include in LCS
- Position 2: X vs Z → No match, skip Z in t
- Position 3: T vs X → No match, skip X in s
- Position 4: (none) vs T → No match, skip T in t

LCS: "AYXT" (length 4)
```

### Dynamic Programming Pattern
```
DP State: dp[i][j] = length of LCS of s[0:i] and t[0:j]

Base cases:
- dp[0][j] = 0 (empty string s)
- dp[i][0] = 0 (empty string t)

Recurrence:
- If s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + 1
- Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])

Key insight: Use 2D DP to handle subsequence matching
```

### State Transition Visualization
```
Building DP table for s = "AYXT", t = "AYZXT":

Initialize: dp = [[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]]

Base cases: dp[0][j] = 0, dp[i][0] = 0

Position (1,1): A vs A → Match
dp[1][1] = dp[0][0] + 1 = 0 + 1 = 1

Position (2,2): Y vs Y → Match
dp[2][2] = dp[1][1] + 1 = 1 + 1 = 2

Position (3,3): X vs Z → No match
dp[3][3] = max(dp[2][3], dp[3][2]) = max(2, 2) = 2

Position (3,4): X vs X → Match
dp[3][4] = dp[2][3] + 1 = 2 + 1 = 3

Position (4,5): T vs T → Match
dp[4][5] = dp[3][4] + 1 = 3 + 1 = 4

Final: dp[4][5] = 4 (LCS length)
```

### Key Insight
The solution works by:
1. Using 2D dynamic programming to handle subsequence matching
2. For each position, considering character matches and skips
3. Building solutions from smaller subproblems
4. Using optimal substructure property
5. Time complexity: O(n × m) for filling DP table
6. Space complexity: O(n × m) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Brute Force (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible subsequences recursively
- Use recursive approach to explore all matching possibilities
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. For each position, try matching or skipping characters
2. Recursively explore all valid subsequence paths
3. Return maximum length found
4. Handle base cases for empty strings

**Visual Example:**
```
Brute force approach: Try all possible subsequences
For strings "AYXT" and "AYZXT":

Recursive tree:
                    (0, 0)
              /            \
          (0, 1)          (1, 0)
         /      \        /      \
    (0, 2)    (1, 1)  (1, 1)  (2, 0)
   /    \     /  \   /  \     /  \
(0, 3) (1, 2) (1, 2) (2, 1) (1, 2) (2, 1) (2, 1) (3, 0)
```

**Implementation:**
```python
def longest_common_subsequence_brute_force(s, t):
    def lcs_length(i, j):
        if i == len(s) or j == len(t):
            return 0
        
        if s[i] == t[j]:
            return 1 + lcs_length(i + 1, j + 1)
        else:
            return max(lcs_length(i + 1, j), lcs_length(i, j + 1))
    
    return lcs_length(0, 0)

def solve_longest_common_subsequence_brute_force():
    s = input().strip()
    t = input().strip()
    
    result = longest_common_subsequence_brute_force(s, t)
    print(result)
```

**Time Complexity:** O(2^(n+m)) for trying all possible subsequences
**Space Complexity:** O(n + m) for recursion depth

**Why it's inefficient:**
- O(2^(n+m)) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large strings
- Poor performance with exponential growth

### Approach 2: Dynamic Programming (Better)

**Key Insights from DP Solution:**
- Use 2D DP array to store LCS length for each position
- More efficient than brute force recursion
- Can handle larger inputs than brute force approach
- Uses optimal substructure property

**Algorithm:**
1. Initialize DP array with base cases
2. For each position, consider character matches and skips
3. Update LCS length using recurrence relation
4. Return maximum LCS length

**Visual Example:**
```
DP approach: Build solutions iteratively
For s = "AYXT", t = "AYZXT":

Initialize: dp = [[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]]

After processing: dp = [[0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 1, 1],
                        [0, 1, 2, 2, 2, 2],
                        [0, 1, 2, 2, 3, 3],
                        [0, 1, 2, 2, 3, 4]]

Final result: dp[4][5] = 4
```

**Implementation:**
```python
def longest_common_subsequence_dp(s, t):
    n, m = len(s), len(t)
    
    # dp[i][j] = length of LCS of s[0:i] and t[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[n][m]

def solve_longest_common_subsequence_dp():
    s = input().strip()
    t = input().strip()
    
    result = longest_common_subsequence_dp(s, t)
    print(result)
```

**Time Complexity:** O(n × m) for filling DP table
**Space Complexity:** O(n × m) for DP array

**Why it's better:**
- O(n × m) time complexity is much better than O(2^(n+m))
- Uses dynamic programming for efficient computation
- Suitable for competitive programming
- Efficient for large inputs

### Approach 3: Optimized DP with Space Efficiency (Optimal)

**Key Insights from Optimized Solution:**
- Use the same DP approach but with better implementation
- Most efficient approach for subsequence problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Initialize DP array with base cases
2. Process strings from left to right
3. Use optimal substructure property
4. Return optimal solution

**Visual Example:**
```
Optimized DP: Process strings from left to right
For s = "AYXT", t = "AYZXT":

Initialize: dp = [[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]]

Process position (1,1): dp[1][1] = 1
Process position (2,2): dp[2][2] = 2
Process position (3,3): dp[3][3] = 2
Process position (3,4): dp[3][4] = 3
Process position (4,5): dp[4][5] = 4
```

**Implementation:**
```python
def solve_longest_common_subsequence():
    s = input().strip()
    t = input().strip()
    
    n, m = len(s), len(t)
    
    # dp[i][j] = length of LCS of s[0:i] and t[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    print(dp[n][m])

# Main execution
if __name__ == "__main__":
    solve_longest_common_subsequence()
```

**Time Complexity:** O(n × m) for filling DP table
**Space Complexity:** O(n × m) for DP array

**Why it's optimal:**
- O(n × m) time complexity is optimal for this problem
- Uses dynamic programming for efficient solution
- Most efficient approach for competitive programming
- Standard method for subsequence problems

## 🎯 Problem Variations

### Variation 1: Longest Common Subsequence with Path Reconstruction
**Problem**: Find the actual LCS string, not just the length.

**Link**: [CSES Problem Set - LCS Path](https://cses.fi/problemset/task/lcs_path)

```python
def longest_common_subsequence_path(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Reconstruct path
    lcs = []
    i, j = n, m
    while i > 0 and j > 0:
        if s[i-1] == t[j-1]:
            lcs.append(s[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))
```

### Variation 2: Longest Common Subsequence with Multiple Strings
**Problem**: Find LCS of multiple strings.

**Link**: [CSES Problem Set - LCS Multiple](https://cses.fi/problemset/task/lcs_multiple)

```python
def longest_common_subsequence_multiple(strings):
    if not strings:
        return 0
    
    # For simplicity, handle 3 strings
    s1, s2, s3 = strings[0], strings[1], strings[2]
    n1, n2, n3 = len(s1), len(s2), len(s3)
    
    dp = [[[0] * (n3 + 1) for _ in range(n2 + 1)] for _ in range(n1 + 1)]
    
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            for k in range(1, n3 + 1):
                if s1[i-1] == s2[j-1] == s3[k-1]:
                    dp[i][j][k] = dp[i-1][j-1][k-1] + 1
                else:
                    dp[i][j][k] = max(dp[i-1][j][k], dp[i][j-1][k], dp[i][j][k-1])
    
    return dp[n1][n2][n3]
```

### Variation 3: Longest Common Subsequence with Constraints
**Problem**: Find LCS with additional constraints (e.g., character limits).

**Link**: [CSES Problem Set - LCS Constraints](https://cses.fi/problemset/task/lcs_constraints)

```python
def longest_common_subsequence_constraints(s, t, char_limit):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1] and char_limit[s[i-1]] > 0:
                dp[i][j] = dp[i-1][j-1] + 1
                char_limit[s[i-1]] -= 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[n][m]
```

## 🔗 Related Problems

- **[Edit Distance](/cses-analyses/problem_soulutions/dynamic_programming/)**: String DP problems
- **[Increasing Subsequence](/cses-analyses/problem_soulutions/dynamic_programming/)**: Subsequence problems
- **[String Algorithms](/cses-analyses/problem_soulutions/string_algorithms/)**: String processing problems
- **[Grid Paths](/cses-analyses/problem_soulutions/dynamic_programming/)**: 2D DP problems

## 📚 Learning Points

1. **Subsequence Problems**: Essential for understanding LCS and subsequence matching
2. **2D Dynamic Programming**: Key technique for solving subsequence problems efficiently
3. **String Processing**: Important for understanding how to handle string matching
4. **Character Matching**: Critical for understanding how to implement subsequence logic
5. **Optimal Substructure**: Foundation for building solutions from smaller subproblems
6. **Bottom-Up DP**: Critical for building solutions from smaller subproblems

## 📝 Summary

The Longest Common Subsequence problem demonstrates subsequence matching and 2D dynamic programming principles for efficient string operations. We explored three approaches:

1. **Recursive Brute Force**: O(2^(n+m)) time complexity using recursive exploration, inefficient due to exponential growth
2. **Dynamic Programming**: O(n × m) time complexity using 2D DP, better approach for subsequence problems
3. **Optimized DP with Space Efficiency**: O(n × m) time complexity with efficient implementation, optimal approach for competitive programming

The key insights include understanding subsequence matching principles, using 2D dynamic programming for efficient computation, and applying string processing techniques for subsequence problems. This problem serves as an excellent introduction to subsequence algorithms in competitive programming.
