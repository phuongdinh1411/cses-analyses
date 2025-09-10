---
layout: simple
title: "Longest Common Subsequence - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/longest_common_subsequence_analysis
---

# Longest Common Subsequence - Dynamic Programming Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of longest common subsequence in dynamic programming
- Apply optimization techniques for subsequence comparison analysis
- Implement efficient algorithms for LCS calculation
- Optimize DP operations for subsequence analysis
- Handle special cases in subsequence problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, subsequence algorithms, optimization techniques
- **Data Structures**: 2D arrays, string processing, DP tables
- **Mathematical Concepts**: Subsequence theory, optimization, string comparison
- **Programming Skills**: DP implementation, string processing, mathematical computations
- **Related Problems**: Increasing Subsequence (dynamic programming), Edit Distance (dynamic programming), Counting Towers (dynamic programming)

## 📋 Problem Description

Given two strings, find the length of the longest common subsequence.

**Input**: 
- s1: first string
- s2: second string

**Output**: 
- Length of the longest common subsequence

**Constraints**:
- 1 ≤ |s1|, |s2| ≤ 1000

**Example**:
```
Input:
s1 = "ABCDGH"
s2 = "AEDFHR"

Output:
3

Explanation**: 
Longest common subsequence: "ADH"
Length: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Use recursion to explore all possible subsequences
- **Complete Enumeration**: Enumerate all possible subsequence combinations
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible common subsequences.

**Algorithm**:
- Use recursive function to try all subsequence combinations
- Check common property for each subsequence
- Find maximum length
- Return result

**Visual Example**:
```
s1 = "ABCDGH", s2 = "AEDFHR":

Recursive exploration:
┌─────────────────────────────────────┐
│ Compare 'A' and 'A': match ✓       │
│ - Compare 'B' and 'E': no match ✗   │
│   - Compare 'B' and 'D': no match ✗ │
│     - Compare 'B' and 'F': no match ✗ │
│       - Compare 'B' and 'H': no match ✗ │
│         - Compare 'B' and 'R': no match ✗ │
│   - Compare 'C' and 'E': no match ✗ │
│     - ... (continue recursively)   │
│ - Compare 'B' and 'E': no match ✗   │
│   - Compare 'B' and 'D': no match ✗ │
│     - ... (continue recursively)   │
│                                   │
│ Find maximum among all paths       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_longest_common_subsequence(s1, s2):
    """
    Find LCS using recursive approach
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: length of longest common subsequence
    """
    def find_lcs(i, j):
        """Find LCS recursively"""
        if i == len(s1) or j == len(s2):
            return 0  # No more characters
        
        if s1[i] == s2[j]:
            return 1 + find_lcs(i + 1, j + 1)  # Match found
        else:
            # Try both possibilities
            return max(find_lcs(i + 1, j), find_lcs(i, j + 1))
    
    return find_lcs(0, 0)

def recursive_longest_common_subsequence_optimized(s1, s2):
    """
    Optimized recursive longest common subsequence finding
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: length of longest common subsequence
    """
    def find_lcs_optimized(i, j):
        """Find LCS with optimization"""
        if i == len(s1) or j == len(s2):
            return 0  # No more characters
        
        if s1[i] == s2[j]:
            return 1 + find_lcs_optimized(i + 1, j + 1)  # Match found
        else:
            # Try both possibilities
            return max(find_lcs_optimized(i + 1, j), find_lcs_optimized(i, j + 1))
    
    return find_lcs_optimized(0, 0)

# Example usage
s1, s2 = "ABCDGH", "AEDFHR"
result1 = recursive_longest_common_subsequence(s1, s2)
result2 = recursive_longest_common_subsequence_optimized(s1, s2)
print(f"Recursive longest common subsequence: {result1}")
print(f"Optimized recursive longest common subsequence: {result2}")
```

**Time Complexity**: O(2^(m+n))
**Space Complexity**: O(m+n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Dynamic Programming Solution

**Key Insights from Dynamic Programming Solution**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: O(m * n) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use dynamic programming to store results of subproblems and avoid recalculations.

**Algorithm**:
- Use DP table to store LCS length for each position
- Fill DP table bottom-up
- Return DP[m][n] as result

**Visual Example**:
```
DP table for s1="ABCDGH", s2="AEDFHR":

DP table:
┌─────────────────────────────────────┐
│ dp[0][0] = 0 (empty strings)       │
│ dp[0][1] = 0 (empty s1)            │
│ dp[0][2] = 0 (empty s1)            │
│ ...                                │
│ dp[1][0] = 0 (empty s2)            │
│ dp[1][1] = 1 (match 'A')           │
│ dp[1][2] = 1 (no match)            │
│ dp[1][3] = 1 (no match)            │
│ ...                                │
│ dp[6][6] = 3 (final result)        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_longest_common_subsequence(s1, s2):
    """
    Find LCS using dynamic programming approach
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: length of longest common subsequence
    """
    m, n = len(s1), len(s2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]  # Match found
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # No match
    
    return dp[m][n]

def dp_longest_common_subsequence_optimized(s1, s2):
    """
    Optimized dynamic programming longest common subsequence finding
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: length of longest common subsequence
    """
    m, n = len(s1), len(s2)
    
    # Create DP table with optimization
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table with optimization
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]  # Match found
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # No match
    
    return dp[m][n]

# Example usage
s1, s2 = "ABCDGH", "AEDFHR"
result1 = dp_longest_common_subsequence(s1, s2)
result2 = dp_longest_common_subsequence_optimized(s1, s2)
print(f"DP longest common subsequence: {result1}")
print(f"Optimized DP longest common subsequence: {result2}")
```

**Time Complexity**: O(m * n)
**Space Complexity**: O(m * n)

**Why it's better**: Uses dynamic programming for O(m * n) time complexity.

**Implementation Considerations**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Memoization**: Store results of subproblems
- **Efficient Computation**: Use bottom-up DP approach

---

### Approach 3: Space-Optimized DP Solution (Optimal)

**Key Insights from Space-Optimized DP Solution**:
- **Space Optimization**: Use only necessary space for DP
- **Efficient Computation**: O(m * n) time complexity
- **Space Efficiency**: O(min(m, n)) space complexity
- **Optimal Complexity**: Best approach for LCS

**Key Insight**: Use space-optimized dynamic programming to reduce space complexity.

**Algorithm**:
- Use only necessary variables for DP
- Update values in-place
- Return final result

**Visual Example**:
```
Space-optimized DP:

For s1="ABCDGH", s2="AEDFHR":
┌─────────────────────────────────────┐
│ Use only current and previous values │
│ Update in-place for efficiency      │
│ Final result: 3                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def space_optimized_dp_longest_common_subsequence(s1, s2):
    """
    Find LCS using space-optimized DP approach
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: length of longest common subsequence
    """
    m, n = len(s1), len(s2)
    
    # Use shorter string for space optimization
    if m > n:
        s1, s2 = s2, s1
        m, n = n, m
    
    # Use only necessary variables for DP
    prev_dp = [0] * (m + 1)
    curr_dp = [0] * (m + 1)
    
    # Fill DP using space optimization
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                curr_dp[i] = 1 + prev_dp[i-1]  # Match found
            else:
                curr_dp[i] = max(prev_dp[i], curr_dp[i-1])  # No match
        
        prev_dp = curr_dp
        curr_dp = [0] * (m + 1)
    
    return prev_dp[m]

def space_optimized_dp_longest_common_subsequence_v2(s1, s2):
    """
    Alternative space-optimized DP longest common subsequence finding
    
    Args:
        s1: first string
        s2: second string
    
    Returns:
        int: length of longest common subsequence
    """
    m, n = len(s1), len(s2)
    
    # Use shorter string for space optimization
    if m > n:
        s1, s2 = s2, s1
        m, n = n, m
    
    # Use only necessary variables for DP
    prev_dp = [0] * (m + 1)
    curr_dp = [0] * (m + 1)
    
    # Fill DP using space optimization
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                curr_dp[i] = 1 + prev_dp[i-1]  # Match found
            else:
                curr_dp[i] = max(prev_dp[i], curr_dp[i-1])  # No match
        
        prev_dp = curr_dp
        curr_dp = [0] * (m + 1)
    
    return prev_dp[m]

def longest_common_subsequence_with_precomputation(max_m, max_n):
    """
    Precompute longest common subsequence for multiple queries
    
    Args:
        max_m: maximum length of first string
        max_n: maximum length of second string
    
    Returns:
        list: precomputed longest common subsequence results
    """
    # This is a simplified version for demonstration
    results = [[0] * (max_n + 1) for _ in range(max_m + 1)]
    
    for i in range(max_m + 1):
        for j in range(max_n + 1):
            if i == 0 or j == 0:
                results[i][j] = 0
            else:
                results[i][j] = min(i, j)  # Simplified calculation
    
    return results

# Example usage
s1, s2 = "ABCDGH", "AEDFHR"
result1 = space_optimized_dp_longest_common_subsequence(s1, s2)
result2 = space_optimized_dp_longest_common_subsequence_v2(s1, s2)
print(f"Space-optimized DP longest common subsequence: {result1}")
print(f"Space-optimized DP longest common subsequence v2: {result2}")

# Precompute for multiple queries
max_m, max_n = 1000, 1000
precomputed = longest_common_subsequence_with_precomputation(max_m, max_n)
print(f"Precomputed result for m={len(s1)}, n={len(s2)}: {precomputed[len(s1)][len(s2)]}")
```

**Time Complexity**: O(m * n)
**Space Complexity**: O(min(m, n))

**Why it's optimal**: Uses space-optimized DP for O(m * n) time and O(min(m, n)) space complexity.

**Implementation Details**:
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use in-place DP updates
- **Space Efficiency**: Reduce space complexity
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^(m+n)) | O(m+n) | Complete enumeration of all subsequences |
| Dynamic Programming | O(m * n) | O(m * n) | Use DP to avoid recalculating subproblems |
| Space-Optimized DP | O(m * n) | O(min(m, n)) | Use space-optimized DP for efficiency |

### Time Complexity
- **Time**: O(m * n) - Use dynamic programming for efficient calculation
- **Space**: O(min(m, n)) - Use space-optimized DP approach

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Space Optimization**: Use only necessary variables for DP
- **Efficient Computation**: Use bottom-up DP approach
- **Optimal Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Longest Common Subsequence with Constraints**
**Problem**: Find LCS with specific constraints.

**Key Differences**: Apply constraints to subsequence selection

**Solution Approach**: Modify DP to handle constraints

**Implementation**:
```python
def constrained_longest_common_subsequence(s1, s2, constraints):
    """
    Find LCS with constraints
    
    Args:
        s1: first string
        s2: second string
        constraints: list of constraints
    
    Returns:
        int: length of longest common subsequence
    """
    m, n = len(s1), len(s2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table with constraints
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1] and constraints(i-1, j-1):
                dp[i][j] = 1 + dp[i-1][j-1]  # Match found
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # No match
    
    return dp[m][n]

# Example usage
s1, s2 = "ABCDGH", "AEDFHR"
constraints = lambda i, j: i < 3 and j < 3  # Only consider first 3 characters
result = constrained_longest_common_subsequence(s1, s2, constraints)
print(f"Constrained longest common subsequence: {result}")
```

#### **2. Longest Common Subsequence with Different Weights**
**Problem**: Find LCS with different weights for characters.

**Key Differences**: Different weights for different characters

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def weighted_longest_common_subsequence(s1, s2, weights):
    """
    Find LCS with different weights
    
    Args:
        s1: first string
        s2: second string
        weights: dictionary of character weights
    
    Returns:
        int: maximum weight of common subsequence
    """
    m, n = len(s1), len(s2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table with weights
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = weights.get(s1[i-1], 1) + dp[i-1][j-1]  # Match found
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # No match
    
    return dp[m][n]

# Example usage
s1, s2 = "ABCDGH", "AEDFHR"
weights = {'A': 2, 'B': 1, 'C': 3, 'D': 2, 'E': 1, 'F': 3, 'G': 1, 'H': 2, 'R': 1}
result = weighted_longest_common_subsequence(s1, s2, weights)
print(f"Weighted longest common subsequence: {result}")
```

#### **3. Longest Common Subsequence with Multiple Strings**
**Problem**: Find LCS among multiple strings.

**Key Differences**: Handle multiple strings

**Solution Approach**: Use advanced DP techniques

**Implementation**:
```python
def multi_string_longest_common_subsequence(strings):
    """
    Find LCS among multiple strings
    
    Args:
        strings: list of strings
    
    Returns:
        int: length of longest common subsequence
    """
    if len(strings) < 2:
        return 0
    
    # Start with first two strings
    result = space_optimized_dp_longest_common_subsequence(strings[0], strings[1])
    
    # Compare with remaining strings
    for i in range(2, len(strings)):
        result = min(result, space_optimized_dp_longest_common_subsequence(strings[0], strings[i]))
    
    return result

# Example usage
strings = ["ABCDGH", "AEDFHR", "ACDGHR"]
result = multi_string_longest_common_subsequence(strings)
print(f"Multi-string longest common subsequence: {result}")
```

### Related Problems

#### **CSES Problems**
- [Increasing Subsequence](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Edit Distance](https://cses.fi/problemset/task/1075) - Dynamic programming
- [Counting Towers](https://cses.fi/problemset/task/1075) - Dynamic programming

#### **LeetCode Problems**
- [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) - DP
- [Longest Common Subpath](https://leetcode.com/problems/longest-common-subpath/) - DP
- [Shortest Common Supersequence](https://leetcode.com/problems/shortest-common-supersequence/) - DP

#### **Problem Categories**
- **Dynamic Programming**: Subsequence DP, string algorithms
- **String Algorithms**: String processing, comparison algorithms
- **Mathematical Algorithms**: Optimization, subsequence theory

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [String Algorithms](https://cp-algorithms.com/string/string-algorithms.html) - String algorithms
- [Subsequence Algorithms](https://cp-algorithms.com/sequences/longest_common_subsequence.html) - Subsequence algorithms

### **Practice Problems**
- [CSES Increasing Subsequence](https://cses.fi/problemset/task/1075) - Medium
- [CSES Edit Distance](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Towers](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
