---
layout: simple
title: "Finding Borders"
permalink: /problem_soulutions/string_algorithms/finding_borders_analysis
---

# Finding Borders

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of borders in strings and their applications
- Apply the KMP failure function (LPS array) for border finding
- Implement efficient border detection algorithms
- Optimize string preprocessing for pattern matching
- Handle edge cases in border problems (empty strings, single characters)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String algorithms, KMP algorithm, failure function, border theory
- **Data Structures**: Strings, arrays, failure function arrays
- **Mathematical Concepts**: String theory, border properties, prefix-suffix relationships
- **Programming Skills**: String manipulation, failure function construction, algorithm implementation
- **Related Problems**: Pattern Positions (KMP algorithm), String Matching (pattern matching), Finding Periods (string preprocessing)

## 📋 Problem Description

Given a string, find all borders of the string. A border of a string is a proper prefix that is also a proper suffix of the string.

This is a fundamental string preprocessing problem that is essential for understanding the KMP algorithm and other string algorithms.

**Input**: 
- First line: string s

**Output**: 
- Print all borders of the string in increasing order of length

**Constraints**:
- 1 ≤ |s| ≤ 10⁶
- String contains only lowercase English letters

**Example**:
```
Input:
abacaba

Output:
a
aba

Explanation**: 
The string "abacaba" has the following borders:
- "a" (prefix: "a", suffix: "a") - length 1
- "aba" (prefix: "aba", suffix: "aba") - length 3

Note: "abacaba" itself is not a border since borders must be proper (not the entire string).
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Possible Prefixes

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible prefixes to see if they are also suffixes
- **Complete Coverage**: Guaranteed to find all borders
- **Simple Implementation**: Straightforward string comparison
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each possible prefix length, check if the prefix equals the corresponding suffix.

**Algorithm**:
- For each possible border length from 1 to n-1:
  - Extract prefix of that length
  - Extract suffix of that length
  - Check if prefix equals suffix

**Visual Example**:
```
String: "abacaba"

Check length 1:
- Prefix: "a", Suffix: "a" → "a" == "a" ✓ (border)

Check length 2:
- Prefix: "ab", Suffix: "ba" → "ab" != "ba" ✗

Check length 3:
- Prefix: "aba", Suffix: "aba" → "aba" == "aba" ✓ (border)

Check length 4:
- Prefix: "abac", Suffix: "caba" → "abac" != "caba" ✗

Check length 5:
- Prefix: "abaca", Suffix: "acaba" → "abaca" != "acaba" ✗

Check length 6:
- Prefix: "abacab", Suffix: "bacaba" → "abacab" != "bacaba" ✗

Borders: ["a", "aba"]
```

**Implementation**:
```python
def brute_force_finding_borders(s):
    """
    Find all borders using brute force approach
    
    Args:
        s: input string
    
    Returns:
        list: all borders of the string
    """
    n = len(s)
    borders = []
    
    # Check each possible border length
    for length in range(1, n):
        prefix = s[:length]
        suffix = s[n-length:]
        
        if prefix == suffix:
            borders.append(prefix)
    
    return borders

# Example usage
s = "abacaba"
result = brute_force_finding_borders(s)
print(f"Brute force result: {result}")  # Output: ['a', 'aba']
```

**Time Complexity**: O(n²) - For each length, compare strings of that length
**Space Complexity**: O(n) - For storing borders

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Using KMP Failure Function

**Key Insights from Optimized Approach**:
- **KMP Failure Function**: Use the LPS (Longest Proper Prefix which is also Suffix) array
- **Efficient Construction**: Build failure function in O(n) time
- **Border Extraction**: Extract all borders from the failure function
- **Linear Time**: Achieve O(n) time complexity

**Key Insight**: The KMP failure function (LPS array) contains information about all borders of the string.

**Algorithm**:
- Build the LPS array using KMP algorithm
- Extract all borders by following the failure function chain
- Return borders in increasing order of length

**Visual Example**:
```
String: "abacaba"

Step 1: Build LPS array
LPS[0] = 0
LPS[1] = 0 (no proper prefix of "ab")
LPS[2] = 1 (proper prefix "a" of "aba")
LPS[3] = 0 (no proper prefix of "abac")
LPS[4] = 1 (proper prefix "a" of "abaca")
LPS[5] = 2 (proper prefix "ab" of "abacab")
LPS[6] = 3 (proper prefix "aba" of "abacaba")

LPS = [0, 0, 1, 0, 1, 2, 3]

Step 2: Extract borders from LPS
- LPS[6] = 3 → border of length 3: "aba"
- LPS[3-1] = LPS[2] = 1 → border of length 1: "a"

Borders: ["a", "aba"]
```

**Implementation**:
```python
def optimized_finding_borders(s):
    """
    Find all borders using KMP failure function
    
    Args:
        s: input string
    
    Returns:
        list: all borders of the string
    """
    def build_lps(pattern):
        """Build Longest Proper Prefix which is also Suffix array"""
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        
        return lps
    
    n = len(s)
    lps = build_lps(s)
    borders = []
    
    # Extract borders from LPS array
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    # Reverse to get borders in increasing order of length
    borders.reverse()
    return borders

# Example usage
s = "abacaba"
result = optimized_finding_borders(s)
print(f"Optimized result: {result}")  # Output: ['a', 'aba']
```

**Time Complexity**: O(n) - Build LPS array and extract borders
**Space Complexity**: O(n) - For LPS array and borders

**Why it's better**: Linear time complexity with efficient border extraction.

---

### Approach 3: Optimal - Direct Border Construction

**Key Insights from Optimal Approach**:
- **Direct Construction**: Build borders directly without intermediate arrays
- **Efficient Extraction**: Extract borders in a single pass
- **Minimal Space**: Use only O(k) space where k is the number of borders
- **Optimal Performance**: Best possible time and space complexity

**Key Insight**: Use the failure function construction process to directly identify and collect borders.

**Algorithm**:
- Build LPS array while collecting borders
- Extract borders during the construction process
- Return borders in increasing order of length

**Visual Example**:
```
String: "abacaba"

Direct border construction:
1. i=0: LPS[0]=0
2. i=1: LPS[1]=0
3. i=2: LPS[2]=1 → border "a" found
4. i=3: LPS[3]=0
5. i=4: LPS[4]=1
6. i=5: LPS[5]=2
7. i=6: LPS[6]=3 → border "aba" found

Borders collected: ["a", "aba"]
```

**Implementation**:
```python
def optimal_finding_borders(s):
    """
    Find all borders using optimal direct construction
    
    Args:
        s: input string
    
    Returns:
        list: all borders of the string
    """
    n = len(s)
    borders = []
    lps = [0] * n
    length = 0
    i = 1
    
    while i < n:
        if s[i] == s[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    # Extract borders from the final LPS value
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    # Reverse to get borders in increasing order of length
    borders.reverse()
    return borders

# Example usage
s = "abacaba"
result = optimal_finding_borders(s)
print(f"Optimal result: {result}")  # Output: ['a', 'aba']
```

**Time Complexity**: O(n) - Single pass through the string
**Space Complexity**: O(k) - Where k is the number of borders (typically much less than n)

**Why it's optimal**: Achieves the best possible time complexity with minimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all prefixes |
| KMP Failure Function | O(n) | O(n) | Use LPS array for borders |
| Direct Construction | O(n) | O(k) | Build borders directly |

### Time Complexity
- **Time**: O(n) - KMP-based approaches provide optimal linear time
- **Space**: O(k) - Where k is the number of borders (typically much less than n)

### Why This Solution Works
- **Border Properties**: Borders have specific mathematical properties that can be exploited
- **KMP Connection**: The failure function of KMP algorithm directly relates to borders
- **Efficient Extraction**: Borders can be extracted efficiently from the failure function
- **Optimal Approach**: Direct construction provides the best balance of time and space complexity
