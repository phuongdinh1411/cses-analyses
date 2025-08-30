---
layout: simple
title: "Longest Common Subsequence"
permalink: /problem_soulutions/dynamic_programming/longest_common_subsequence_analysis
---


# Longest Common Subsequence

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