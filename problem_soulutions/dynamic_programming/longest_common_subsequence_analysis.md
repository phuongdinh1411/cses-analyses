---
layout: simple
title: "Longest Common Subsequence"
permalink: /problem_soulutions/dynamic_programming/longest_common_subsequence_analysis
---


# Longest Common Subsequence

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand subsequence problems and longest common subsequence calculations
- [ ] **Objective 2**: Apply 2D DP techniques to solve subsequence problems with string matching
- [ ] **Objective 3**: Implement efficient 2D DP solutions for LCS and subsequence optimization
- [ ] **Objective 4**: Optimize 2D DP solutions using space-efficient techniques and subsequence tracking
- [ ] **Objective 5**: Handle edge cases in string DP (empty strings, no common subsequences, single characters)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: 2D dynamic programming, string algorithms, subsequence problems, string matching
- **Data Structures**: 2D arrays, DP tables, string data structures
- **Mathematical Concepts**: String theory, subsequence properties, string matching, optimization principles
- **Programming Skills**: 2D array manipulation, string processing, iterative programming, DP implementation
- **Related Problems**: Edit Distance (string DP), Increasing Subsequence (subsequence problems), String algorithms

## Problem Description

**Problem**: Given two strings, find the length of their longest common subsequence (LCS). A subsequence is a sequence that can be derived from another sequence by deleting some elements without changing the order of the remaining elements.

**Input**: 
- s: first string
- t: second string

**Output**: Length of the longest common subsequence.

**Example**:
```
Input:
AYXT
AYZXT

Output:
4

Explanation: 
The longest common subsequence is "AYXT" with length 4.
We can find this by matching characters in order:
- A matches A
- Y matches Y  
- X matches X
- T matches T
The Z in the second string is skipped.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the longest sequence that appears in both strings
- Characters must appear in the same order in both strings
- We can skip characters but cannot reorder them
- Use dynamic programming for efficiency

**Key Observations:**
- If characters match, we can extend the LCS
- If characters don't match, we take the maximum of two options
- This is a classic dynamic programming problem
- Can use 2D DP table

### Step 2: Dynamic Programming Approach
**Idea**: Use 2D DP table to store LCS lengths for all subproblems.

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
```

**Why this works:**
- Uses optimal substructure property
- Handles all cases correctly
- Efficient implementation
- O(n*m) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_longest_common_subsequence():
    s = input()
    t = input()
    
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

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ("AYXT", "AYZXT", 4),
        ("ABCDGH", "AEDFHR", 3),
        ("AGGTAB", "GXTXAYB", 4),
        ("ABC", "DEF", 0),
        ("", "ABC", 0),
        ("ABC", "", 0),
    ]
    
    for s, t, expected in test_cases:
        result = solve_test(s, t)
        print(f"s='{s}', t='{t}', expected={expected}, result={result}")
        assert result == expected, f"Failed for s='{s}', t='{t}'"
        print("✓ Passed")
        print()

def solve_test(s, t):
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n*m) - we fill a 2D DP table
- **Space**: O(n*m) - we store the entire DP table

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes LCS using optimal substructure
- **State Transition**: dp[i][j] = max(dp[i-1][j], dp[i][j-1], dp[i-1][j-1] + 1 if match)
- **Base Case**: dp[0][j] = dp[i][0] = 0 for all i, j
- **Optimal Substructure**: LCS of prefixes can be built from smaller subproblems

## 🎨 Visual Example

### Input Example
```
String 1: "AYXT"
String 2: "AYZXT"
```

### All Possible Common Subsequences
```
String 1: A Y X T
String 2: A Y Z X T

All common subsequences:
1. "A" (length 1)
2. "Y" (length 1)
3. "X" (length 1)
4. "T" (length 1)
5. "AY" (length 2)
6. "AX" (length 2)
7. "AT" (length 2)
8. "YX" (length 2)
9. "YT" (length 2)
10. "XT" (length 2)
11. "AYX" (length 3)
12. "AYT" (length 3)
13. "AXT" (length 3)
14. "YXT" (length 3)
15. "AYXT" (length 4)

Longest common subsequence: "AYXT" (length 4)
```

### DP State Representation
```
dp[i][j] = length of LCS of s[0:i] and t[0:j]

For strings "AYXT" and "AYZXT":
dp[0][j] = 0 for all j (empty string)
dp[i][0] = 0 for all i (empty string)

dp[1][1] = 1 (LCS of "A" and "A" is "A")
dp[1][2] = 1 (LCS of "A" and "AY" is "A")
dp[1][3] = 1 (LCS of "A" and "AYZ" is "A")
dp[1][4] = 1 (LCS of "A" and "AYZX" is "A")
dp[1][5] = 1 (LCS of "A" and "AYZXT" is "A")

dp[2][1] = 1 (LCS of "AY" and "A" is "A")
dp[2][2] = 2 (LCS of "AY" and "AY" is "AY")
dp[2][3] = 2 (LCS of "AY" and "AYZ" is "AY")
dp[2][4] = 2 (LCS of "AY" and "AYZX" is "AY")
dp[2][5] = 2 (LCS of "AY" and "AYZXT" is "AY")

dp[3][1] = 1 (LCS of "AYX" and "A" is "A")
dp[3][2] = 2 (LCS of "AYX" and "AY" is "AY")
dp[3][3] = 2 (LCS of "AYX" and "AYZ" is "AY")
dp[3][4] = 3 (LCS of "AYX" and "AYZX" is "AYX")
dp[3][5] = 3 (LCS of "AYX" and "AYZXT" is "AYX")

dp[4][1] = 1 (LCS of "AYXT" and "A" is "A")
dp[4][2] = 2 (LCS of "AYXT" and "AY" is "AY")
dp[4][3] = 2 (LCS of "AYXT" and "AYZ" is "AY")
dp[4][4] = 3 (LCS of "AYXT" and "AYZX" is "AYX")
dp[4][5] = 4 (LCS of "AYXT" and "AYZXT" is "AYXT")
```

### DP Table Construction
```
String 1: "AYXT"
String 2: "AYZXT"

Step 1: Initialize base cases
dp[0][j] = 0 for all j
dp[i][0] = 0 for all i

Step 2: Fill DP table
dp[1][1] = 1 (A matches A)
dp[1][2] = 1 (A matches A)
dp[1][3] = 1 (A matches A)
dp[1][4] = 1 (A matches A)
dp[1][5] = 1 (A matches A)

dp[2][1] = 1 (Y doesn't match A, take max of dp[1][1] and dp[2][0])
dp[2][2] = 2 (Y matches Y, dp[1][1] + 1 = 2)
dp[2][3] = 2 (Y doesn't match Z, take max of dp[1][3] and dp[2][2])
dp[2][4] = 2 (Y doesn't match X, take max of dp[1][4] and dp[2][3])
dp[2][5] = 2 (Y doesn't match T, take max of dp[1][5] and dp[2][4])

dp[3][1] = 1 (X doesn't match A, take max of dp[2][1] and dp[3][0])
dp[3][2] = 2 (X doesn't match Y, take max of dp[2][2] and dp[3][1])
dp[3][3] = 2 (X doesn't match Z, take max of dp[2][3] and dp[3][2])
dp[3][4] = 3 (X matches X, dp[2][3] + 1 = 3)
dp[3][5] = 3 (X doesn't match T, take max of dp[2][5] and dp[3][4])

dp[4][1] = 1 (T doesn't match A, take max of dp[3][1] and dp[4][0])
dp[4][2] = 2 (T doesn't match Y, take max of dp[3][2] and dp[4][1])
dp[4][3] = 2 (T doesn't match Z, take max of dp[3][3] and dp[4][2])
dp[4][4] = 3 (T doesn't match X, take max of dp[3][4] and dp[4][3])
dp[4][5] = 4 (T matches T, dp[3][4] + 1 = 4)

Final result: dp[4][5] = 4
```

### Visual DP Table
```
String 1: "AYXT"
String 2: "AYZXT"

DP Table (LCS lengths):
     0  1  2  3  4  5
0:    0  0  0  0  0  0
1:    0  1  1  1  1  1
2:    0  1  2  2  2  2
3:    0  1  2  2  3  3
4:    0  1  2  2  3  4

Each cell shows length of LCS of corresponding prefixes
```

### LCS Construction
```
String 1: "AYXT"
String 2: "AYZXT"

LCS: "AYXT" (length 4)
- A matches A (position 0,0)
- Y matches Y (position 1,1)
- X matches X (position 2,3)
- T matches T (position 3,4)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(2^(m+n))   │ O(m+n)       │ Try all      │
│                 │              │              │ subsequences │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Memoized        │ O(m*n)       │ O(m*n)       │ Cache        │
│ Recursion       │              │              │ results      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bottom-up DP    │ O(m*n)       │ O(m*n)       │ Build from   │
│                 │              │              │ base cases   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Space-optimized │ O(m*n)       │ O(min(m,n))  │ Use only     │
│ DP              │              │              │ current row  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Dynamic Programming for String Problems**
- Find optimal substructure in string problems
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **2D DP Table**
- Use 2D table for two-string problems
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Subsequence vs Substring**
- Subsequence allows skipping characters
- Important for understanding
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Print the LCS
**Problem**: Find and print the actual longest common subsequence.

```python
def print_longest_common_subsequence(s, t):
    n, m = len(s), len(t)
    
    # dp[i][j] = length of LCS of s[0:i] and t[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Reconstruct the LCS
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

# Example usage
result = print_longest_common_subsequence("AYXT", "AYZXT")
print(f"LCS: {result}")
```

### Variation 2: Count All LCS
**Problem**: Count the number of different longest common subsequences.

```python
def count_longest_common_subsequences(s, t):
    n, m = len(s), len(t)
    
    # dp[i][j] = length of LCS of s[0:i] and t[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # count[i][j] = number of LCS of s[0:i] and t[0:j]
    count = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 or j == 0:
                count[i][j] = 1
            elif s[i-1] == t[j-1]:
                count[i][j] = count[i-1][j-1]
            else:
                if dp[i-1][j] == dp[i][j]:
                    count[i][j] += count[i-1][j]
                if dp[i][j-1] == dp[i][j]:
                    count[i][j] += count[i][j-1]
                if dp[i-1][j-1] == dp[i][j]:
                    count[i][j] -= count[i-1][j-1]
    
    return count[n][m]

# Example usage
result = count_longest_common_subsequences("AYXT", "AYZXT")
print(f"Number of LCS: {result}")
```

### Variation 3: LCS with Constraints
**Problem**: Find LCS with additional constraints.

```python
def constrained_lcs(s, t, constraints):
    n, m = len(s), len(t)
    
    # dp[i][j][k] = length of LCS of s[0:i] and t[0:j] with constraint k
    dp = [[[0] * (len(constraints) + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            for k in range(len(constraints) + 1):
                if s[i-1] == t[j-1]:
                    dp[i][j][k] = dp[i-1][j-1][k] + 1
                else:
                    dp[i][j][k] = max(dp[i-1][j][k], dp[i][j-1][k])
                
                # Apply constraints
                if k < len(constraints) and constraints[k](s[i-1], t[j-1]):
                    dp[i][j][k+1] = max(dp[i][j][k+1], dp[i][j][k])
    
    return dp[n][m][len(constraints)]

# Example usage
def constraint_func(c1, c2):
    return c1.isupper() and c2.isupper()

constraints = [constraint_func]
result = constrained_lcs("AYXT", "AYZXT", constraints)
print(f"Constrained LCS length: {result}")
```

### Variation 4: LCS with Weights
**Problem**: Find LCS where each character has a weight.

```python
def weighted_lcs(s, t, weights):
    n, m = len(s), len(t)
    
    # dp[i][j] = weight of LCS of s[0:i] and t[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + weights.get(s[i-1], 1)
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[n][m]

# Example usage
weights = {'A': 2, 'Y': 3, 'X': 1, 'T': 4}
result = weighted_lcs("AYXT", "AYZXT", weights)
print(f"Weighted LCS: {result}")
```

### Variation 5: LCS with Dynamic Programming Optimization
**Problem**: Optimize the DP solution for better performance.

```python
def optimized_lcs(s, t):
    n, m = len(s), len(t)
    
    # Use only 2 rows to save space
    dp = [[0] * (m + 1) for _ in range(2)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i % 2][j] = dp[(i-1) % 2][j-1] + 1
            else:
                dp[i % 2][j] = max(dp[(i-1) % 2][j], dp[i % 2][j-1])
    
    return dp[n % 2][m]

# Example usage
result = optimized_lcs("AYXT", "AYZXT")
print(f"Optimized LCS length: {result}")
```

## 🔗 Related Problems

- **[Edit Distance](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar string problems
- **[Longest Increasing Subsequence](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar subsequence problems
- **[String Matching](/cses-analyses/problem_soulutions/dynamic_programming/)**: String algorithm problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for string problems
2. **2D DP Tables**: Important for two-string problems
3. **Subsequence vs Substring**: Important for understanding constraints
4. **String Algorithms**: Important for text processing

---

**This is a great introduction to dynamic programming for string problems!** 🎯 