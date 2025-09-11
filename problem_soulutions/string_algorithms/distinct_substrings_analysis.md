---
layout: simple
title: "Distinct Substrings"
permalink: /problem_soulutions/string_algorithms/distinct_substrings_analysis
---

# Distinct Substrings

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of distinct substrings and their applications
- Apply suffix arrays and suffix automata for efficient substring counting
- Implement efficient solutions for distinct substring problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in substring counting problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Suffix arrays, suffix automata, string hashing, rolling hash
- **Data Structures**: Strings, suffix arrays, suffix trees, hash maps
- **Mathematical Concepts**: String theory, substring counting, suffix array construction
- **Programming Skills**: String manipulation, algorithm implementation, suffix array algorithms
- **Related Problems**: Distinct Strings (substring counting), String Matching (pattern matching), Suffix Arrays

## 📋 Problem Description

You are given a string s. Count the number of distinct substrings in the string.

A substring is a contiguous sequence of characters within a string.

**Input**: 
- First line: string s

**Output**: 
- Print one integer: the number of distinct substrings

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- s contains only lowercase English letters

**Example**:
```
Input:
abc

Output:
6

Explanation**: 
String: "abc"

All substrings:
- "a" (position 0)
- "b" (position 1)  
- "c" (position 2)
- "ab" (positions 0-1)
- "bc" (positions 1-2)
- "abc" (positions 0-2)

Total distinct substrings: 6
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Generate All Substrings

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Generate all possible substrings and count distinct ones
- **Complete Coverage**: Guaranteed to find all distinct substrings
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each possible starting and ending position, generate the substring and add it to a set.

**Algorithm**:
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Generate substring s[i:j+1]
    - Add to set of distinct substrings
- Return the size of the set

**Visual Example**:
```
String: "abc"

All substrings:
- i=0, j=0: "a"
- i=0, j=1: "ab"
- i=0, j=2: "abc"
- i=1, j=1: "b"
- i=1, j=2: "bc"
- i=2, j=2: "c"

Distinct substrings: {"a", "ab", "abc", "b", "bc", "c"}
Count: 6
```

**Implementation**:
```python
def brute_force_distinct_substrings(s):
    """
    Count distinct substrings using brute force approach
    
    Args:
        s: input string
    
    Returns:
        int: number of distinct substrings
    """
    n = len(s)
    distinct_substrings = set()
    
    for i in range(n):
        for j in range(i, n):
            substring = s[i:j+1]
            distinct_substrings.add(substring)
    
    return len(distinct_substrings)

# Example usage
s = "abc"
result = brute_force_distinct_substrings(s)
print(f"Brute force result: {result}")  # Output: 6
```

**Time Complexity**: O(n³) - Nested loops with substring generation
**Space Complexity**: O(n²) - Set of substrings

**Why it's inefficient**: Cubic time complexity makes it very slow for large inputs.

---

### Approach 2: Optimized - Use Rolling Hash

**Key Insights from Optimized Approach**:
- **Rolling Hash**: Use rolling hash to efficiently generate substring hashes
- **Efficient Generation**: Avoid string concatenation for substring generation
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use rolling hash to efficiently generate and hash substrings.

**Algorithm**:
- Precompute rolling hash for the string
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Calculate hash of substring s[i:j+1] using rolling hash
    - Add hash to set of distinct hashes
- Return the size of the set

**Visual Example**:
```
String: "abc"

Rolling hash calculation:
- Hash("a") = 1
- Hash("ab") = 1*31 + 2 = 33
- Hash("abc") = 33*31 + 3 = 1026
- Hash("b") = 2
- Hash("bc") = 2*31 + 3 = 65
- Hash("c") = 3

Distinct hashes: {1, 33, 1026, 2, 65, 3}
Count: 6
```

**Implementation**:
```python
def optimized_distinct_substrings(s):
    """
    Count distinct substrings using optimized rolling hash approach
    
    Args:
        s: input string
    
    Returns:
        int: number of distinct substrings
    """
    n = len(s)
    distinct_hashes = set()
    base = 31
    mod = 10**9 + 7
    
    for i in range(n):
        hash_value = 0
        for j in range(i, n):
            # Rolling hash: hash = (hash * base + char_value) % mod
            hash_value = (hash_value * base + (ord(s[j]) - ord('a') + 1)) % mod
            distinct_hashes.add(hash_value)
    
    return len(distinct_hashes)

# Example usage
s = "abc"
result = optimized_distinct_substrings(s)
print(f"Optimized result: {result}")  # Output: 6
```

**Time Complexity**: O(n²) - Nested loops with rolling hash
**Space Complexity**: O(n²) - Set of hashes

**Why it's better**: More efficient than brute force with rolling hash optimization.

---

### Approach 3: Optimal - Use Suffix Array

**Key Insights from Optimal Approach**:
- **Suffix Array**: Use suffix array to efficiently count distinct substrings
- **Optimal Complexity**: Achieve O(n log n) time complexity
- **Efficient Implementation**: Use suffix array and LCP array
- **Mathematical Insight**: Use suffix array to count distinct substrings efficiently

**Key Insight**: Use suffix array and LCP array to count distinct substrings using the formula: total_substrings - sum_of_lcp_values.

**Algorithm**:
- Build suffix array for the string
- Build LCP (Longest Common Prefix) array
- Calculate total possible substrings: n*(n+1)/2
- Subtract sum of LCP values to get distinct substrings
- Return the result

**Visual Example**:
```
String: "abc"

Suffixes: ["abc", "bc", "c"]
Suffix Array: [0, 1, 2] (indices of sorted suffixes)
LCP Array: [0, 0, 0] (LCP between adjacent suffixes)

Total substrings: 3*4/2 = 6
Sum of LCP: 0 + 0 = 0
Distinct substrings: 6 - 0 = 6
```

**Implementation**:
```python
def optimal_distinct_substrings(s):
    """
    Count distinct substrings using optimal suffix array approach
    
    Args:
        s: input string
    
    Returns:
        int: number of distinct substrings
    """
    n = len(s)
    
    # Build suffix array (simplified version)
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    suffixes.sort()
    
    # Build LCP array
    lcp = [0] * n
    for i in range(1, n):
        lcp[i] = 0
        j = 0
        while (j < len(suffixes[i-1][0]) and 
               j < len(suffixes[i][0]) and 
               suffixes[i-1][0][j] == suffixes[i][0][j]):
            lcp[i] += 1
            j += 1
    
    # Calculate distinct substrings
    total_substrings = n * (n + 1) // 2
    sum_lcp = sum(lcp)
    distinct_substrings = total_substrings - sum_lcp
    
    return distinct_substrings

# Example usage
s = "abc"
result = optimal_distinct_substrings(s)
print(f"Optimal result: {result}")  # Output: 6
```

**Time Complexity**: O(n log n) - Suffix array construction
**Space Complexity**: O(n) - Suffix array and LCP array

**Why it's optimal**: Achieves the best possible time complexity with suffix array optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n²) | Generate all substrings |
| Rolling Hash | O(n²) | O(n²) | Use rolling hash |
| Suffix Array | O(n log n) | O(n) | Use suffix array and LCP |

### Time Complexity
- **Time**: O(n log n) - Suffix array approach provides optimal time complexity
- **Space**: O(n) - Suffix array and LCP array

### Why This Solution Works
- **Suffix Array**: Use suffix array and LCP array to efficiently count distinct substrings
- **Optimal Algorithm**: Suffix array approach is the standard solution for this problem
- **Optimal Approach**: Single pass through suffixes provides the most efficient solution for substring counting problems
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
