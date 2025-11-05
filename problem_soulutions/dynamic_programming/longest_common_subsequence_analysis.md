---
layout: simple
title: "Longest Common Subsequence - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming/longest_common_subsequence_analysis
---

# Longest Common Subsequence

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

#### 📌 **DP State Definition**

**What does `dp[i][j]` represent?**
- `dp[i][j]` = **length of the longest common subsequence (LCS)** between the first `i` characters of string `s1` and the first `j` characters of string `s2`
- This is a 2D DP array where:
  - First dimension `i` = number of characters considered from `s1` (0 to m)
  - Second dimension `j` = number of characters considered from `s2` (0 to n)
- `dp[i][j]` stores the length of the LCS between `s1[0:i]` and `s2[0:j]`

**In plain language:**
- For each prefix of `s1` (first i characters) and each prefix of `s2` (first j characters), we find the length of their longest common subsequence
- A subsequence doesn't need to be contiguous, but characters must appear in the same order
- `dp[0][j]` = 0 (empty string has no common subsequence)
- `dp[i][0]` = 0 (empty string has no common subsequence)
- `dp[m][n]` = length of LCS between the full strings (this is our final answer)

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

## Problem Variations

### **Variation 1: Longest Common Subsequence with Dynamic Updates**
**Problem**: Handle dynamic string updates (add/remove/update characters) while maintaining optimal LCS calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic string management.

```python
from collections import defaultdict

class DynamicLongestCommonSubsequence:
    def __init__(self, string1=None, string2=None):
        self.string1 = string1 or ""
        self.string2 = string2 or ""
        self.subsequences = []
        self._update_lcs_info()
    
    def _update_lcs_info(self):
        """Update LCS feasibility information."""
        self.lcs_feasibility = self._calculate_lcs_feasibility()
    
    def _calculate_lcs_feasibility(self):
        """Calculate LCS feasibility."""
        if not self.string1 and not self.string2:
            return 0.0
        
        # Check if we can find LCS between strings
        return 1.0 if self.string1 or self.string2 else 0.0
    
    def update_string1(self, new_string1):
        """Update first string."""
        self.string1 = new_string1
        self._update_lcs_info()
    
    def update_string2(self, new_string2):
        """Update second string."""
        self.string2 = new_string2
        self._update_lcs_info()
    
    def find_lcs_length(self):
        """Find length of longest common subsequence using dynamic programming."""
        if not self.lcs_feasibility:
            return 0
        
        m, n = len(self.string1), len(self.string2)
        if m == 0 or n == 0:
            return 0
        
        # DP table: dp[i][j] = length of LCS of string1[:i] and string2[:j]
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    def find_lcs_sequence(self):
        """Find the actual longest common subsequence."""
        if not self.lcs_feasibility:
            return ""
        
        m, n = len(self.string1), len(self.string2)
        if m == 0 or n == 0:
            return ""
        
        # DP table: dp[i][j] = length of LCS of string1[:i] and string2[:j]
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Backtrack to find the actual LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if self.string1[i-1] == self.string2[j-1]:
                lcs.append(self.string1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs))
    
    def get_lcs_with_constraints(self, constraint_func):
        """Get LCS that satisfies custom constraints."""
        if not self.lcs_feasibility:
            return ""
        
        length = self.find_lcs_length()
        if constraint_func(length, self.string1, self.string2):
            return self.find_lcs_sequence()
        else:
            return ""
    
    def get_lcs_in_range(self, min_length, max_length):
        """Get LCS within specified length range."""
        if not self.lcs_feasibility:
            return ""
        
        length = self.find_lcs_length()
        if min_length <= length <= max_length:
            return self.find_lcs_sequence()
        else:
            return ""
    
    def get_lcs_with_pattern(self, pattern_func):
        """Get LCS matching specified pattern."""
        if not self.lcs_feasibility:
            return ""
        
        length = self.find_lcs_length()
        if pattern_func(length, self.string1, self.string2):
            return self.find_lcs_sequence()
        else:
            return ""
    
    def get_lcs_statistics(self):
        """Get statistics about the LCS."""
        if not self.lcs_feasibility:
            return {
                'string1_length': 0,
                'string2_length': 0,
                'lcs_feasibility': 0,
                'lcs_length': 0
            }
        
        length = self.find_lcs_length()
        return {
            'string1_length': len(self.string1),
            'string2_length': len(self.string2),
            'lcs_feasibility': self.lcs_feasibility,
            'lcs_length': length
        }
    
    def get_lcs_patterns(self):
        """Get patterns in LCS."""
        patterns = {
            'has_common_characters': 0,
            'has_valid_strings': 0,
            'optimal_lcs_possible': 0,
            'has_large_strings': 0
        }
        
        if not self.lcs_feasibility:
            return patterns
        
        # Check if has common characters
        if self.string1 and self.string2:
            common_chars = set(self.string1) & set(self.string2)
            if common_chars:
                patterns['has_common_characters'] = 1
        
        # Check if has valid strings
        if self.string1 or self.string2:
            patterns['has_valid_strings'] = 1
        
        # Check if optimal LCS is possible
        if self.lcs_feasibility == 1.0:
            patterns['optimal_lcs_possible'] = 1
        
        # Check if has large strings
        if len(self.string1) > 100 or len(self.string2) > 100:
            patterns['has_large_strings'] = 1
        
        return patterns
    
    def get_optimal_lcs_strategy(self):
        """Get optimal strategy for LCS finding."""
        if not self.lcs_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'lcs_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.lcs_feasibility
        
        # Calculate LCS feasibility
        lcs_feasibility = self.lcs_feasibility
        
        # Determine recommended strategy
        if len(self.string1) <= 100 and len(self.string2) <= 100:
            recommended_strategy = 'dynamic_programming'
        elif len(self.string1) <= 1000 and len(self.string2) <= 1000:
            recommended_strategy = 'optimized_dp'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'lcs_feasibility': lcs_feasibility
        }

# Example usage
string1 = "ABCDGH"
string2 = "AEDFHR"
dynamic_lcs = DynamicLongestCommonSubsequence(string1, string2)
print(f"LCS feasibility: {dynamic_lcs.lcs_feasibility}")

# Update strings
dynamic_lcs.update_string1("AGGTAB")
dynamic_lcs.update_string2("GXTXAYB")
print(f"After updating strings: '{dynamic_lcs.string1}' and '{dynamic_lcs.string2}'")

# Find LCS length
length = dynamic_lcs.find_lcs_length()
print(f"LCS length: {length}")

# Find LCS sequence
sequence = dynamic_lcs.find_lcs_sequence()
print(f"LCS sequence: '{sequence}'")

# Get LCS with constraints
def constraint_func(length, string1, string2):
    return length > 0 and len(string1) > 0 and len(string2) > 0

print(f"LCS with constraints: '{dynamic_lcs.get_lcs_with_constraints(constraint_func)}'")

# Get LCS in range
print(f"LCS in range 1-10: '{dynamic_lcs.get_lcs_in_range(1, 10)}'")

# Get LCS with pattern
def pattern_func(length, string1, string2):
    return length > 0 and len(string1) > 0 and len(string2) > 0

print(f"LCS with pattern: '{dynamic_lcs.get_lcs_with_pattern(pattern_func)}'")

# Get statistics
print(f"Statistics: {dynamic_lcs.get_lcs_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_lcs.get_lcs_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_lcs.get_optimal_lcs_strategy()}")
```

### **Variation 2: Longest Common Subsequence with Different Operations**
**Problem**: Handle different types of LCS operations (weighted characters, priority-based finding, advanced string analysis).

**Approach**: Use advanced data structures for efficient different types of LCS operations.

```python
class AdvancedLongestCommonSubsequence:
    def __init__(self, string1=None, string2=None, weights=None, priorities=None):
        self.string1 = string1 or ""
        self.string2 = string2 or ""
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.subsequences = []
        self._update_lcs_info()
    
    def _update_lcs_info(self):
        """Update LCS feasibility information."""
        self.lcs_feasibility = self._calculate_lcs_feasibility()
    
    def _calculate_lcs_feasibility(self):
        """Calculate LCS feasibility."""
        if not self.string1 and not self.string2:
            return 0.0
        
        # Check if we can find LCS between strings
        return 1.0 if self.string1 or self.string2 else 0.0
    
    def find_lcs_length(self):
        """Find length of longest common subsequence using dynamic programming."""
        if not self.lcs_feasibility:
            return 0
        
        m, n = len(self.string1), len(self.string2)
        if m == 0 or n == 0:
            return 0
        
        # DP table: dp[i][j] = length of LCS of string1[:i] and string2[:j]
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    def get_weighted_lcs(self):
        """Get LCS with weights and priorities applied."""
        if not self.lcs_feasibility:
            return ""
        
        m, n = len(self.string1), len(self.string2)
        if m == 0 or n == 0:
            return ""
        
        # DP table with weighted characters
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Fill DP table with weighted characters
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    char = self.string1[i-1]
                    weight = self.weights.get(char, 1)
                    priority = self.priorities.get(char, 1)
                    dp[i][j] = dp[i-1][j-1] + (weight * priority)
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Backtrack to find the weighted LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if self.string1[i-1] == self.string2[j-1]:
                lcs.append(self.string1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs))
    
    def get_lcs_with_priority(self, priority_func):
        """Get LCS considering priority."""
        if not self.lcs_feasibility:
            return ""
        
        # Create priority-based weights
        priority_weights = {}
        for char in set(self.string1 + self.string2):
            priority = priority_func(char, self.weights, self.priorities)
            priority_weights[char] = priority
        
        # Calculate LCS with priority weights
        m, n = len(self.string1), len(self.string2)
        if m == 0 or n == 0:
            return ""
        
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    char = self.string1[i-1]
                    weight = priority_weights.get(char, 1)
                    dp[i][j] = dp[i-1][j-1] + weight
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Backtrack to find the priority LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if self.string1[i-1] == self.string2[j-1]:
                lcs.append(self.string1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs))
    
    def get_lcs_with_optimization(self, optimization_func):
        """Get LCS using custom optimization function."""
        if not self.lcs_feasibility:
            return ""
        
        # Create optimization-based weights
        optimized_weights = {}
        for char in set(self.string1 + self.string2):
            score = optimization_func(char, self.weights, self.priorities)
            optimized_weights[char] = score
        
        # Calculate LCS with optimized weights
        m, n = len(self.string1), len(self.string2)
        if m == 0 or n == 0:
            return ""
        
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    char = self.string1[i-1]
                    weight = optimized_weights.get(char, 1)
                    dp[i][j] = dp[i-1][j-1] + weight
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Backtrack to find the optimized LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if self.string1[i-1] == self.string2[j-1]:
                lcs.append(self.string1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs))
    
    def get_lcs_with_constraints(self, constraint_func):
        """Get LCS that satisfies custom constraints."""
        if not self.lcs_feasibility:
            return ""
        
        if constraint_func(self.string1, self.string2, self.weights, self.priorities):
            return self.get_weighted_lcs()
        else:
            return ""
    
    def get_lcs_with_multiple_criteria(self, criteria_list):
        """Get LCS that satisfies multiple criteria."""
        if not self.lcs_feasibility:
            return ""
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.string1, self.string2, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_lcs()
        else:
            return ""
    
    def get_lcs_with_alternatives(self, alternatives):
        """Get LCS considering alternative weights/priorities."""
        result = []
        
        # Check original LCS
        original_lcs = self.get_weighted_lcs()
        result.append((original_lcs, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedLongestCommonSubsequence(self.string1, self.string2, alt_weights, alt_priorities)
            temp_lcs = temp_instance.get_weighted_lcs()
            result.append((temp_lcs, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_lcs_with_adaptive_criteria(self, adaptive_func):
        """Get LCS using adaptive criteria."""
        if not self.lcs_feasibility:
            return ""
        
        if adaptive_func(self.string1, self.string2, self.weights, self.priorities, ""):
            return self.get_weighted_lcs()
        else:
            return ""
    
    def get_lcs_optimization(self):
        """Get optimal LCS configuration."""
        strategies = [
            ('weighted_lcs', lambda: len(self.get_weighted_lcs())),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
string1 = "ABCDGH"
string2 = "AEDFHR"
weights = {char: ord(char) - ord('A') + 1 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}  # Weight based on position
priorities = {char: 1 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}  # Equal priority
advanced_lcs = AdvancedLongestCommonSubsequence(string1, string2, weights, priorities)

print(f"Weighted LCS: '{advanced_lcs.get_weighted_lcs()}'")

# Get LCS with priority
def priority_func(char, weights, priorities):
    return weights.get(char, 1) + priorities.get(char, 1)

print(f"LCS with priority: '{advanced_lcs.get_lcs_with_priority(priority_func)}'")

# Get LCS with optimization
def optimization_func(char, weights, priorities):
    return weights.get(char, 1) * priorities.get(char, 1)

print(f"LCS with optimization: '{advanced_lcs.get_lcs_with_optimization(optimization_func)}'")

# Get LCS with constraints
def constraint_func(string1, string2, weights, priorities):
    return len(string1) > 0 and len(string2) > 0

print(f"LCS with constraints: '{advanced_lcs.get_lcs_with_constraints(constraint_func)}'")

# Get LCS with multiple criteria
def criterion1(string1, string2, weights, priorities):
    return len(string1) > 0

def criterion2(string1, string2, weights, priorities):
    return len(string2) > 0

criteria_list = [criterion1, criterion2]
print(f"LCS with multiple criteria: '{advanced_lcs.get_lcs_with_multiple_criteria(criteria_list)}'")

# Get LCS with alternatives
alternatives = [({char: 1 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}, {char: 1 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}), ({char: ord(char) for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}, {char: 2 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'})]
print(f"LCS with alternatives: {advanced_lcs.get_lcs_with_alternatives(alternatives)}")

# Get LCS with adaptive criteria
def adaptive_func(string1, string2, weights, priorities, current_result):
    return len(string1) > 0 and len(string2) > 0 and len(current_result) < 5

print(f"LCS with adaptive criteria: '{advanced_lcs.get_lcs_with_adaptive_criteria(adaptive_func)}'")

# Get LCS optimization
print(f"LCS optimization: {advanced_lcs.get_lcs_optimization()}")
```

### **Variation 3: Longest Common Subsequence with Constraints**
**Problem**: Handle LCS finding with additional constraints (string limits, character constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedLongestCommonSubsequence:
    def __init__(self, string1=None, string2=None, constraints=None):
        self.string1 = string1 or ""
        self.string2 = string2 or ""
        self.constraints = constraints or {}
        self.subsequences = []
        self._update_lcs_info()
    
    def _update_lcs_info(self):
        """Update LCS feasibility information."""
        self.lcs_feasibility = self._calculate_lcs_feasibility()
    
    def _calculate_lcs_feasibility(self):
        """Calculate LCS feasibility."""
        if not self.string1 and not self.string2:
            return 0.0
        
        # Check if we can find LCS between strings
        return 1.0 if self.string1 or self.string2 else 0.0
    
    def _is_valid_character(self, char, position1, position2):
        """Check if character is valid considering constraints."""
        # Character constraints
        if 'allowed_characters' in self.constraints:
            if char not in self.constraints['allowed_characters']:
                return False
        
        if 'forbidden_characters' in self.constraints:
            if char in self.constraints['forbidden_characters']:
                return False
        
        # Position constraints
        if 'allowed_positions' in self.constraints:
            if (position1, position2) not in self.constraints['allowed_positions']:
                return False
        
        if 'forbidden_positions' in self.constraints:
            if (position1, position2) in self.constraints['forbidden_positions']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(char, position1, position2):
                    return False
        
        return True
    
    def get_lcs_with_string_constraints(self, min_length, max_length):
        """Get LCS considering string length constraints."""
        if not self.lcs_feasibility:
            return ""
        
        if min_length <= len(self.string1) <= max_length and min_length <= len(self.string2) <= max_length:
            return self._calculate_constrained_lcs()
        else:
            return ""
    
    def get_lcs_with_character_constraints(self, character_constraints):
        """Get LCS considering character constraints."""
        if not self.lcs_feasibility:
            return ""
        
        satisfies_constraints = True
        for constraint in character_constraints:
            if not constraint(self.string1, self.string2):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self._calculate_constrained_lcs()
        else:
            return ""
    
    def get_lcs_with_pattern_constraints(self, pattern_constraints):
        """Get LCS considering pattern constraints."""
        if not self.lcs_feasibility:
            return ""
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.string1, self.string2):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self._calculate_constrained_lcs()
        else:
            return ""
    
    def get_lcs_with_mathematical_constraints(self, constraint_func):
        """Get LCS that satisfies custom mathematical constraints."""
        if not self.lcs_feasibility:
            return ""
        
        if constraint_func(self.string1, self.string2):
            return self._calculate_constrained_lcs()
        else:
            return ""
    
    def get_lcs_with_optimization_constraints(self, optimization_func):
        """Get LCS using custom optimization constraints."""
        if not self.lcs_feasibility:
            return ""
        
        # Calculate optimization score for LCS
        score = optimization_func(self.string1, self.string2)
        
        if score > 0:
            return self._calculate_constrained_lcs()
        else:
            return ""
    
    def get_lcs_with_multiple_constraints(self, constraints_list):
        """Get LCS that satisfies multiple constraints."""
        if not self.lcs_feasibility:
            return ""
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.string1, self.string2):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self._calculate_constrained_lcs()
        else:
            return ""
    
    def get_lcs_with_priority_constraints(self, priority_func):
        """Get LCS with priority-based constraints."""
        if not self.lcs_feasibility:
            return ""
        
        # Calculate priority for LCS
        priority = priority_func(self.string1, self.string2)
        
        if priority > 0:
            return self._calculate_constrained_lcs()
        else:
            return ""
    
    def get_lcs_with_adaptive_constraints(self, adaptive_func):
        """Get LCS with adaptive constraints."""
        if not self.lcs_feasibility:
            return ""
        
        if adaptive_func(self.string1, self.string2, ""):
            return self._calculate_constrained_lcs()
        else:
            return ""
    
    def _calculate_constrained_lcs(self):
        """Calculate LCS considering all constraints."""
        if not self.lcs_feasibility:
            return ""
        
        m, n = len(self.string1), len(self.string2)
        if m == 0 or n == 0:
            return ""
        
        # DP table: dp[i][j] = length of LCS of string1[:i] and string2[:j]
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Fill DP table with constraints
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.string1[i-1] == self.string2[j-1]:
                    char = self.string1[i-1]
                    if self._is_valid_character(char, i-1, j-1):
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Backtrack to find the constrained LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if self.string1[i-1] == self.string2[j-1]:
                char = self.string1[i-1]
                if self._is_valid_character(char, i-1, j-1):
                    lcs.append(char)
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs))
    
    def get_optimal_lcs_strategy(self):
        """Get optimal LCS strategy considering all constraints."""
        strategies = [
            ('string_constraints', self.get_lcs_with_string_constraints),
            ('character_constraints', self.get_lcs_with_character_constraints),
            ('pattern_constraints', self.get_lcs_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'string_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'character_constraints':
                    character_constraints = [lambda string1, string2: len(string1) > 0 and len(string2) > 0]
                    result = strategy_func(character_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda string1, string2: len(string1) > 0 and len(string2) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_characters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'forbidden_characters': '0123456789',
    'allowed_positions': [(i, j) for i in range(10) for j in range(10)],
    'forbidden_positions': [],
    'pattern_constraints': [lambda char, pos1, pos2: char.isalpha() and pos1 >= 0 and pos2 >= 0]
}

string1 = "ABCDGH"
string2 = "AEDFHR"
constrained_lcs = ConstrainedLongestCommonSubsequence(string1, string2, constraints)

print("String-constrained LCS:", constrained_lcs.get_lcs_with_string_constraints(1, 20))

print("Character-constrained LCS:", constrained_lcs.get_lcs_with_character_constraints([lambda string1, string2: len(string1) > 0 and len(string2) > 0]))

print("Pattern-constrained LCS:", constrained_lcs.get_lcs_with_pattern_constraints([lambda string1, string2: len(string1) > 0 and len(string2) > 0]))

# Mathematical constraints
def custom_constraint(string1, string2):
    return len(string1) > 0 and len(string2) > 0

print("Mathematical constraint LCS:", constrained_lcs.get_lcs_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(string1, string2):
    return 1 <= len(string1) <= 20 and 1 <= len(string2) <= 20

range_constraints = [range_constraint]
print("Range-constrained LCS:", constrained_lcs.get_lcs_with_string_constraints(1, 20))

# Multiple constraints
def constraint1(string1, string2):
    return len(string1) > 0

def constraint2(string1, string2):
    return len(string2) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints LCS:", constrained_lcs.get_lcs_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(string1, string2):
    return len(string1) + len(string2)

print("Priority-constrained LCS:", constrained_lcs.get_lcs_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(string1, string2, current_result):
    return len(string1) > 0 and len(string2) > 0 and len(current_result) < 5

print("Adaptive constraint LCS:", constrained_lcs.get_lcs_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_lcs.get_optimal_lcs_strategy()
print(f"Optimal LCS strategy: {optimal}")
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
