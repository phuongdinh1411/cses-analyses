---
layout: simple
title: "Pattern Positions"
permalink: /problem_soulutions/string_algorithms/pattern_positions_analysis
---

# Pattern Positions

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand pattern matching and string searching algorithms
- Apply the Knuth-Morris-Pratt (KMP) algorithm for efficient pattern matching
- Implement the Rabin-Karp algorithm using rolling hash
- Optimize string matching algorithms for large inputs
- Handle edge cases in pattern matching (empty patterns, repeated patterns)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String algorithms, pattern matching, KMP algorithm, rolling hash, Z-algorithm
- **Data Structures**: Strings, arrays, hash functions, failure functions
- **Mathematical Concepts**: String theory, hashing, pattern matching, failure function construction
- **Programming Skills**: String manipulation, algorithm implementation, hash functions
- **Related Problems**: String Matching (pattern matching), Finding Borders (string preprocessing), Longest Palindrome (string algorithms)

## 📋 Problem Description

Given a text string and a pattern string, find all positions where the pattern occurs in the text. This is the fundamental pattern matching problem that forms the basis for many other string algorithms.

**Input**: 
- First line: text string
- Second line: pattern string

**Output**: 
- Print all positions (0-indexed) where the pattern occurs in the text, separated by spaces

**Constraints**:
- 1 ≤ |text|, |pattern| ≤ 10⁶
- Both strings contain only lowercase English letters

**Example**:
```
Input:
ababcababc
abc

Output:
2 7

Explanation**: 
The pattern "abc" occurs at positions 2 and 7 in the text "ababcababc":
- Position 2: "ababcababc" → "abc" matches
- Position 7: "ababcababc" → "abc" matches
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Naive String Matching

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check every possible position in the text
- **Character-by-Character Comparison**: Compare pattern with text at each position
- **Complete Coverage**: Guaranteed to find all occurrences
- **Simple Implementation**: Straightforward nested loops approach

**Key Insight**: For each position in the text, check if the pattern matches starting from that position.

**Algorithm**:
- For each position i in the text:
  - Check if pattern matches text[i:i+len(pattern)]
  - If match found, record the position

**Visual Example**:
```
Text: "ababcababc", Pattern: "abc"

Check position 0: "aba" vs "abc" → No match
Check position 1: "bab" vs "abc" → No match  
Check position 2: "abc" vs "abc" → Match! (position 2)
Check position 3: "bca" vs "abc" → No match
Check position 4: "cab" vs "abc" → No match
Check position 5: "aba" vs "abc" → No match
Check position 6: "bab" vs "abc" → No match
Check position 7: "abc" vs "abc" → Match! (position 7)

Results: [2, 7]
```

**Implementation**:
```python
def brute_force_pattern_positions(text, pattern):
    """
    Find all pattern occurrences using brute force approach
    
    Args:
        text: the text string to search in
        pattern: the pattern string to find
    
    Returns:
        list: positions where pattern occurs
    """
    n, m = len(text), len(pattern)
    positions = []
    
    # Check each possible starting position
    for i in range(n - m + 1):
        # Check if pattern matches at position i
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        
        if match:
            positions.append(i)
    
    return positions

# Example usage
text = "ababcababc"
pattern = "abc"
result = brute_force_pattern_positions(text, pattern)
print(f"Brute force result: {result}")  # Output: [2, 7]
```

**Time Complexity**: O(n × m) - For each position, compare up to m characters
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Rabin-Karp Algorithm

**Key Insights from Optimized Approach**:
- **Rolling Hash**: Use hash function to compare strings efficiently
- **Hash Comparison**: Compare hash values instead of character-by-character
- **Efficient Updates**: Update hash in O(1) time when sliding the window
- **Collision Handling**: Handle hash collisions with additional verification

**Key Insight**: Use rolling hash to compare strings in O(1) time, reducing overall complexity.

**Algorithm**:
- Compute hash of pattern
- Compute hash of first window in text
- Slide window and update hash efficiently
- Compare hashes and verify matches

**Visual Example**:
```
Text: "ababcababc", Pattern: "abc"

Step 1: Compute pattern hash
Pattern "abc": hash = (1×26² + 2×26¹ + 3×26⁰) mod p

Step 2: Compute first window hash
Text[0:3] "aba": hash = (1×26² + 2×26¹ + 1×26⁰) mod p

Step 3: Slide window and update hash
Window "bab": hash = (2×26² + 1×26¹ + 2×26⁰) mod p
Window "abc": hash = (1×26² + 2×26¹ + 3×26⁰) mod p → Match!

Continue sliding...
```

**Implementation**:
```python
def optimized_pattern_positions(text, pattern):
    """
    Find all pattern occurrences using Rabin-Karp algorithm
    
    Args:
        text: the text string to search in
        pattern: the pattern string to find
    
    Returns:
        list: positions where pattern occurs
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Hash parameters
    base = 26
    mod = 10**9 + 7
    
    # Compute pattern hash
    pattern_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
    
    # Compute first window hash
    window_hash = 0
    for i in range(m):
        window_hash = (window_hash * base + ord(text[i])) % mod
    
    positions = []
    
    # Check first window
    if window_hash == pattern_hash and text[:m] == pattern:
        positions.append(0)
    
    # Slide window and update hash
    base_power = pow(base, m - 1, mod)
    for i in range(1, n - m + 1):
        # Remove leftmost character and add rightmost character
        window_hash = ((window_hash - ord(text[i-1]) * base_power) * base + ord(text[i + m - 1])) % mod
        
        # Check for match
        if window_hash == pattern_hash and text[i:i+m] == pattern:
            positions.append(i)
    
    return positions

# Example usage
text = "ababcababc"
pattern = "abc"
result = optimized_pattern_positions(text, pattern)
print(f"Optimized result: {result}")  # Output: [2, 7]
```

**Time Complexity**: O(n + m) - Average case, O(n × m) worst case
**Space Complexity**: O(1) - Constant extra space

**Why it's better**: Much more efficient on average, but worst case is still quadratic.

---

### Approach 3: Optimal - Knuth-Morris-Pratt (KMP) Algorithm

**Key Insights from Optimal Approach**:
- **Failure Function**: Preprocess pattern to create failure function (LPS array)
- **Skip Characters**: Skip characters that are guaranteed not to match
- **Linear Time**: Achieve O(n + m) time complexity in all cases
- **No Backtracking**: Never backtrack in the text

**Key Insight**: Preprocess the pattern to create a failure function that tells us how many characters to skip when a mismatch occurs.

**Algorithm**:
- Build failure function (LPS array) for the pattern
- Use failure function to skip characters during matching
- Never backtrack in the text

**Visual Example**:
```
Pattern: "abc"

Step 1: Build LPS array
LPS[0] = 0 (no proper prefix)
LPS[1] = 0 (no proper prefix of "ab")
LPS[2] = 0 (no proper prefix of "abc")

Step 2: KMP matching
Text: "ababcababc"
Pattern: "abc"

i=0, j=0: 'a' == 'a' → i=1, j=1
i=1, j=1: 'b' == 'b' → i=2, j=2  
i=2, j=2: 'a' != 'c' → j = LPS[1] = 0
i=2, j=0: 'a' == 'a' → i=3, j=1
i=3, j=1: 'b' == 'b' → i=4, j=2
i=4, j=2: 'c' == 'c' → Match at position 2!

Continue...
```

**Implementation**:
```python
def optimal_pattern_positions(text, pattern):
    """
    Find all pattern occurrences using KMP algorithm
    
    Args:
        text: the text string to search in
        pattern: the pattern string to find
    
    Returns:
        list: positions where pattern occurs
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
    
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Build LPS array
    lps = build_lps(pattern)
    
    positions = []
    i = j = 0  # i for text, j for pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions

# Example usage
text = "ababcababc"
pattern = "abc"
result = optimal_pattern_positions(text, pattern)
print(f"Optimal result: {result}")  # Output: [2, 7]
```

**Time Complexity**: O(n + m) - Linear time in all cases
**Space Complexity**: O(m) - For LPS array

**Why it's optimal**: Guaranteed linear time complexity with no backtracking in text.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × m) | O(1) | Check all positions |
| Rabin-Karp | O(n + m) avg, O(n × m) worst | O(1) | Rolling hash comparison |
| KMP Algorithm | O(n + m) | O(m) | Failure function preprocessing |

### Time Complexity
- **Time**: O(n + m) - KMP algorithm provides optimal linear time
- **Space**: O(m) - For LPS array in KMP algorithm

### Why This Solution Works
- **Pattern Preprocessing**: KMP algorithm preprocesses pattern for efficient matching
- **No Backtracking**: Never need to backtrack in the text
- **Optimal Complexity**: Guaranteed linear time in all cases
- **Optimal Approach**: KMP algorithm provides the best theoretical and practical performance
