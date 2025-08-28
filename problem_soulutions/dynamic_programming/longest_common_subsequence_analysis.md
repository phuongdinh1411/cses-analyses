---
layout: simple
title: "Longest Common Subsequence
permalink: /problem_soulutions/dynamic_programming/longest_common_subsequence_analysis/
---

# Longest Common Subsequence

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Longest Common Substring**
**Problem**: Find the longest common substring (consecutive characters) between two strings.
```python
def longest_common_substring(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_length = 0
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                max_length = max(max_length, dp[i][j])
            else:
                dp[i][j] = 0  # Reset to 0 for non-consecutive
    
    return max_length
```

#### **Variation 2: Count All Common Subsequences**
**Problem**: Count the total number of common subsequences between two strings.
```python
def count_common_subsequences(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base case: empty string is common to all
    for i in range(n + 1):
        dp[i][0] = 1
    for j in range(m + 1):
        dp[0][j] = 1
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + dp[i-1][j] + dp[i][j-1] - dp[i-1][j-1]
            else:
                dp[i][j] = dp[i-1][j] + dp[i][j-1] - dp[i-1][j-1]
    
    return dp[n][m]
```

#### **Variation 3: Longest Common Subsequence with Constraints**
**Problem**: Find LCS where characters must be at least k positions apart.
```python
def constrained_lcs(s, t, k):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1] and abs(i - j) >= k:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[n][m]
```

#### **Variation 4: Weighted Longest Common Subsequence**
**Problem**: Each character has a weight, find LCS with maximum total weight.
```python
def weighted_lcs(s, t, weights):
    # weights[char] = weight of character char
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + weights.get(s[i-1], 1)
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[n][m]
```

#### **Variation 5: Longest Common Subsequence with Multiple Strings**
**Problem**: Find LCS among k strings.
```python
def multiple_lcs(strings):
    k = len(strings)
    if k == 0:
        return 0
    if k == 1:
        return len(strings[0])
    
    # For k=2, use standard LCS
    if k == 2:
        return longest_common_subsequence_optimized(strings[0], strings[1])
    
    # For k>2, use recursive approach
    def solve(indices):
        if any(indices[i] == 0 for i in range(k)):
            return 0
        
        # Check if all current characters match
        current_chars = [strings[i][indices[i]-1] for i in range(k)]
        if len(set(current_chars)) == 1:
            new_indices = [indices[i] - 1 for i in range(k)]
            return 1 + solve(new_indices)
        else:
            # Try removing character from each string
            max_lcs = 0
            for i in range(k):
                new_indices = list(indices)
                new_indices[i] -= 1
                max_lcs = max(max_lcs, solve(new_indices))
            return max_lcs
    
    return solve([len(s) for s in strings])
```

### 🔗 **Related Problems & Concepts**

#### **1. String Matching Problems**
- **Longest Common Substring**: Find longest consecutive common substring
- **Edit Distance**: Minimum operations to transform one string to another
- **String Alignment**: Align strings with gaps
- **Pattern Matching**: Find patterns in strings

#### **2. Dynamic Programming Patterns**
- **2D DP**: Two state variables (position in each string)
- **3D DP**: Three state variables (position, additional constraint)
- **State Compression**: Optimize space complexity
- **Memoization**: Top-down approach with caching

#### **3. Sequence Analysis**
- **Sequence Alignment**: Align similar sequences
- **Pattern Recognition**: Find patterns in sequences
- **Bioinformatics**: DNA/RNA sequence analysis
- **Natural Language Processing**: Text similarity

#### **4. Optimization Problems**
- **Maximum Value**: Find maximum weight/value
- **Minimum Cost**: Find minimum cost solution
- **Resource Allocation**: Optimal use of limited resources
- **Scheduling**: Optimal arrangement of tasks

#### **5. Algorithmic Techniques**
- **Recursive Backtracking**: Try all possible alignments
- **Memoization**: Cache computed results
- **Bottom-Up DP**: Build solution iteratively
- **State Space Search**: Explore all possible states

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Constraints**
```python
t = int(input())
for _ in range(t):
    s = input()
    t = input()
    result = find_longest_common_subsequence(s, t)
    print(result)
```

#### **2. Range Queries on LCS**
```python
def range_lcs_queries(s, t, queries):
    n, m = len(s), len(t)
    
    # Precompute LCS for all prefixes
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Answer queries
    for start_s, end_s, start_t, end_t in queries:
        # Calculate LCS for substrings
        sub_s = s[start_s:end_s+1]
        sub_t = t[start_t:end_t+1]
        result = find_longest_common_subsequence(sub_s, sub_t)
        print(result)
```

#### **3. Interactive LCS Problems**
```python
def interactive_lcs_game():"
    s = input("Enter first string: ")
    t = input("Enter second string: ")
    
    print(f"String 1: {s}")
    print(f"String 2: {t}")
    
    player_guess = int(input("Enter LCS length: "))
    actual_lcs = find_longest_common_subsequence(s, t)
    
    if player_guess == actual_lcs:
        print("Correct!")
    else:
        print(f"Wrong! LCS length is {actual_lcs}")
```

### 🧮 **Mathematical Extensions**

#### **1. Sequence Analysis**
- **Alignment Theory**: Mathematical study of sequence alignments
- **Edit Distance**: Minimum operations for transformation
- **Similarity Measures**: Quantify sequence similarity
- **Pattern Recognition**: Find mathematical patterns

#### **2. Advanced DP Techniques**
- **Digit DP**: Count sequences with specific properties
- **Convex Hull Trick**: Optimize DP transitions
- **Divide and Conquer**: Split problems into subproblems
- **Persistent Data Structures**: Maintain sequence history

#### **3. Combinatorial Analysis**
- **Subsequence Counting**: Count valid subsequences
- **String Permutations**: Analyze string arrangements
- **Generating Functions**: Represent sequences algebraically
- **Asymptotic Analysis**: Behavior for large strings

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Needleman-Wunsch**: Global sequence alignment
- **Smith-Waterman**: Local sequence alignment
- **Hirschberg's Algorithm**: Space-efficient LCS
- **Suffix Trees**: Efficient string processing

#### **2. Mathematical Concepts**
- **Combinatorics**: Counting principles and techniques
- **String Theory**: Mathematical study of strings
- **Optimization Theory**: Finding optimal solutions
- **Probability Theory**: Random string processes

#### **3. Programming Concepts**
- **Dynamic Programming**: Optimal substructure and overlapping subproblems
- **Memoization**: Caching computed results
- **Space-Time Trade-offs**: Optimizing for different constraints
- **Algorithm Design**: Creating efficient solutions

---

*This analysis demonstrates the power of dynamic programming for sequence alignment problems and shows various extensions and applications.* 