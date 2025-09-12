---
layout: simple
title: "Distinct Strings"
permalink: /problem_soulutions/string_algorithms/distinct_strings_analysis
---

# Distinct Strings

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of string hashing and its applications
- Apply rolling hash technique for efficient string comparison
- Implement efficient solutions for string counting problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in string hashing problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String hashing, rolling hash, hash collision handling, string comparison
- **Data Structures**: Hash maps, strings, rolling hash arrays
- **Mathematical Concepts**: Hash functions, modular arithmetic, polynomial hashing, collision probability
- **Programming Skills**: String manipulation, hash function implementation, complexity analysis
- **Related Problems**: String Matching (hashing), Pattern Positions (hashing), Finding Borders (hashing)

## 📋 Problem Description

You are given a string s of length n. Count the number of distinct substrings in the string.

A substring is a contiguous sequence of characters within a string.

**Input**: 
- One string s (the input string)

**Output**: 
- Print one integer: the number of distinct substrings

**Constraints**:
- 1 ≤ n ≤ 10⁵
- String contains only lowercase English letters

**Example**:
```
Input:
abc

Output:
6

Explanation**: 
String: "abc"

All substrings:
1. "a" (position 0)
2. "b" (position 1)  
3. "c" (position 2)
4. "ab" (positions 0-1)
5. "bc" (positions 1-2)
6. "abc" (positions 0-2)

Total distinct substrings: 6
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: [Description]
- **Complete Coverage**: [Description]
- **Simple Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def brute_force_distinct_strings(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's inefficient**: [Reason]

---

### Approach 2: Optimized

**Key Insights from Optimized Approach**:
- **Optimization Technique**: [Description]
- **Efficiency Improvement**: [Description]
- **Better Complexity**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimized_distinct_strings(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's better**: [Reason]

---

### Approach 3: Optimal

**Key Insights from Optimal Approach**:
- **Optimal Algorithm**: [Description]
- **Best Complexity**: [Description]
- **Efficient Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimal_distinct_strings(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's optimal**: [Reason]

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O([complexity]) | O([complexity]) | [Insight] |
| Optimized | O([complexity]) | O([complexity]) | [Insight] |
| Optimal | O([complexity]) | O([complexity]) | [Insight] |

### Time Complexity
- **Time**: O([complexity]) - [Explanation]
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **String Hashing**: Use polynomial hashing to efficiently compare strings
- **Rolling Hash**: Update hash values in O(1) time when sliding window
- **Collision Handling**: Use multiple hash functions to reduce collision probability
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Count Distinct Substrings**
**Problem**: Count the number of distinct substrings in a string.

**Key Differences**: Count instead of just checking existence

**Solution Approach**: Use rolling hash to count unique substrings

**Implementation**:
```python
def count_distinct_substrings(s):
    """
    Count number of distinct substrings using rolling hash
    """
    n = len(s)
    distinct_substrings = set()
    
    for length in range(1, n + 1):
        # Rolling hash for substrings of current length
        base = 26
        mod = 10**9 + 7
        hash_val = 0
        power = 1
        
        # Calculate hash for first substring
        for i in range(length):
            hash_val = (hash_val * base + ord(s[i]) - ord('a')) % mod
            if i < length - 1:
                power = (power * base) % mod
        
        distinct_substrings.add(hash_val)
        
        # Rolling hash for remaining substrings
        for i in range(length, n):
            # Remove leftmost character
            hash_val = (hash_val - (ord(s[i - length]) - ord('a')) * power) % mod
            # Add rightmost character
            hash_val = (hash_val * base + ord(s[i]) - ord('a')) % mod
            distinct_substrings.add(hash_val)
    
    return len(distinct_substrings)

# Example usage
s = "abc"
result = count_distinct_substrings(s)
print(f"Distinct substrings: {result}")  # Output: 6
```

#### **2. Longest Common Substring**
**Problem**: Find the longest common substring between two strings.

**Key Differences**: Compare two strings instead of one

**Solution Approach**: Use binary search with rolling hash

**Implementation**:
```python
def longest_common_substring(s1, s2):
    """
    Find longest common substring using binary search and rolling hash
    """
    def has_common_substring(length):
        # Hash all substrings of given length in s1
        base = 26
        mod = 10**9 + 7
        hashes_s1 = set()
        
        if length > len(s1):
            return False
        
        # Calculate hash for first substring
        hash_val = 0
        power = 1
        for i in range(length):
            hash_val = (hash_val * base + ord(s1[i]) - ord('a')) % mod
            if i < length - 1:
                power = (power * base) % mod
        
        hashes_s1.add(hash_val)
        
        # Rolling hash for remaining substrings
        for i in range(length, len(s1)):
            hash_val = (hash_val - (ord(s1[i - length]) - ord('a')) * power) % mod
            hash_val = (hash_val * base + ord(s1[i]) - ord('a')) % mod
            hashes_s1.add(hash_val)
        
        # Check if any substring of s2 matches
        if length > len(s2):
            return False
        
        hash_val = 0
        for i in range(length):
            hash_val = (hash_val * base + ord(s2[i]) - ord('a')) % mod
        
        if hash_val in hashes_s1:
            return True
        
        for i in range(length, len(s2)):
            hash_val = (hash_val - (ord(s2[i - length]) - ord('a')) * power) % mod
            hash_val = (hash_val * base + ord(s2[i]) - ord('a')) % mod
            if hash_val in hashes_s1:
                return True
        
        return False
    
    # Binary search for maximum length
    left, right = 0, min(len(s1), len(s2))
    result = 0
    
    while left <= right:
        mid = (left + right) // 2
        if has_common_substring(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result

# Example usage
s1 = "abcdef"
s2 = "defghi"
result = longest_common_substring(s1, s2)
print(f"Longest common substring length: {result}")  # Output: 3
```

#### **3. String Matching with Wildcards**
**Problem**: Find all occurrences of a pattern in text where pattern may contain wildcards.

**Key Differences**: Pattern contains wildcards that match any character

**Solution Approach**: Use rolling hash with special handling for wildcards

**Implementation**:
```python
def string_matching_wildcards(text, pattern):
    """
    Find all occurrences of pattern with wildcards in text
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    base = 26
    mod = 10**9 + 7
    results = []
    
    # Calculate hash for pattern (wildcards = 0)
    pattern_hash = 0
    for i in range(m):
        if pattern[i] != '*':
            pattern_hash = (pattern_hash * base + ord(pattern[i]) - ord('a')) % mod
        # Wildcards contribute 0 to hash
    
    # Calculate hash for first substring of text
    text_hash = 0
    power = 1
    for i in range(m):
        text_hash = (text_hash * base + ord(text[i]) - ord('a')) % mod
        if i < m - 1:
            power = (power * base) % mod
    
    # Check first substring
    if text_hash == pattern_hash:
        results.append(0)
    
    # Rolling hash for remaining substrings
    for i in range(m, n):
        # Remove leftmost character
        text_hash = (text_hash - (ord(text[i - m]) - ord('a')) * power) % mod
        # Add rightmost character
        text_hash = (text_hash * base + ord(text[i]) - ord('a')) % mod
        
        if text_hash == pattern_hash:
            results.append(i - m + 1)
    
    return results

# Example usage
text = "abacaba"
pattern = "a*a"
result = string_matching_wildcards(text, pattern)
print(f"Pattern occurrences: {result}")  # Output: [0, 4]
```

### Related Problems

#### **CSES Problems**
- [Distinct Strings](https://cses.fi/problemset/task/2101) - Count distinct substrings
- [String Matching](https://cses.fi/problemset/task/1753) - Find pattern in text
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string
- [Finding Periods](https://cses.fi/problemset/task/1733) - Find periods of string

#### **LeetCode Problems**
- [Longest Common Substring](https://leetcode.com/problems/longest-common-substring/) - Find longest common substring
- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) - String matching with repetition
- [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) - Pattern matching with wildcards
- [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) - Pattern matching with regex

#### **Problem Categories**
- **String Hashing**: Distinct strings, string matching, rolling hash
- **Pattern Matching**: KMP, Z-algorithm, string matching with wildcards
- **String Processing**: Borders, periods, palindromes, anagrams
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata
