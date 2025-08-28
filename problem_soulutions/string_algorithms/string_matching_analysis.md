---
layout: simple
title: "String Matching
permalink: /problem_soulutions/string_algorithms/string_matching_analysis/"
---


# String Matching

## Problem Statement
Given a string and a pattern, find all occurrences of the pattern in the string.

### Input
The first input line has a string s.
The second input line has a pattern p.

### Output
Print all positions where the pattern occurs in the string (1-indexed).

### Constraints
- 1 ≤ |s|, |p| ≤ 10^6

### Example
```
Input:
ABCABCA
ABC

Output:
1 4
```

## Solution Progression

### Approach 1: Naive String Matching - O(|s| * |p|)
**Description**: Check each position in the string for a match with the pattern.

```python
def string_matching_naive(s, p):
    positions = []
    n, m = len(s), len(p)
    
    for i in range(n - m + 1):
        if s[i:i + m] == p:
            positions.append(i + 1)  # 1-indexed
    
    return positions
```

**Why this is inefficient**: Quadratic time complexity for large strings.

### Improvement 1: KMP Algorithm - O(|s| + |p|)
**Description**: Use Knuth-Morris-Pratt algorithm for efficient string matching.

```python
def compute_lps(pattern):
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

def string_matching_kmp(s, p):
    positions = []
    n, m = len(s), len(p)
    
    if m == 0:
        return []
    
    lps = compute_lps(p)
    i = j = 0
    
    while i < n:
        if p[j] == s[i]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j + 1)  # 1-indexed
            j = lps[j - 1]
        elif i < n and p[j] != s[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions
```

**Why this improvement works**: KMP algorithm uses failure function to avoid unnecessary comparisons.

### Improvement 2: Boyer-Moore Algorithm - O(|s| + |p|)
**Description**: Use Boyer-Moore algorithm with bad character rule for efficient matching.

```python
def build_bad_char_table(pattern):
    m = len(pattern)
    bad_char = {}
    
    for i in range(m - 1):
        bad_char[pattern[i]] = m - 1 - i
    
    return bad_char

def string_matching_boyer_moore(s, p):
    positions = []
    n, m = len(s), len(p)
    
    if m == 0:
        return []
    
    bad_char = build_bad_char_table(p)
    i = m - 1
    
    while i < n:
        j = m - 1
        k = i
        
        while j >= 0 and s[k] == p[j]:
            k -= 1
            j -= 1
        
        if j == -1:
            positions.append(k + 2)  # 1-indexed
            i += 1
        else:
            i += bad_char.get(s[i], m)
    
    return positions
```

**Why this improvement works**: Boyer-Moore uses bad character rule to skip more positions.

### Alternative: Z-Algorithm - O(|s| + |p|)
**Description**: Use Z-algorithm for pattern matching by concatenating pattern and string.

```python
def compute_z_array(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    
    for i in range(1, n):
        if i > r:
            l = r = i
            while r < n and s[r - l] == s[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            k = i - l
            if z[k] < r - i + 1:
                z[i] = z[k]
            else:
                l = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    
    return z

def string_matching_z_algorithm(s, p):
    positions = []
    n, m = len(s), len(p)
    
    if m == 0:
        return []"
    # Concatenate pattern + '$' + string
    combined = p + '$' + s
    z = compute_z_array(combined)
    
    # Find positions where z[i] == m (pattern length)
    for i in range(m + 1, len(combined)):
        if z[i] == m:
            positions.append(i - m)  # Convert to 1-indexed
    
    return positions
```

**Why this works**: Z-algorithm finds all occurrences of pattern in linear time.

## Final Optimal Solution

```python
s = input().strip()
p = input().strip()

def compute_lps(pattern):
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

def string_matching_kmp(s, p):
    positions = []
    n, m = len(s), len(p)
    
    if m == 0:
        return []
    
    lps = compute_lps(p)
    i = j = 0
    
    while i < n:
        if p[j] == s[i]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j + 1)  # 1-indexed
            j = lps[j - 1]
        elif i < n and p[j] != s[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions

positions = string_matching_kmp(s, p)
print(*positions)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s| * |p|) | O(1) | Simple but slow |
| KMP | O(|s| + |p|) | O(|p|) | Use failure function |
| Boyer-Moore | O(|s| + |p|) | O(|p|) | Bad character rule |
| Z-Algorithm | O(|s| + |p|) | O(|s| + |p|) | Z-array computation |

## Key Insights for Other Problems

### 1. **String Matching Problems**
**Principle**: Use efficient algorithms like KMP, Boyer-Moore, or Z-algorithm for pattern matching.
**Applicable to**:
- String matching problems
- Pattern matching
- String algorithms
- Algorithm design

**Example Problems**:
- String matching problems
- Pattern matching
- String algorithms
- Algorithm design

### 2. **Failure Function (LPS)**
**Principle**: Use longest proper prefix that is also a suffix to avoid unnecessary comparisons.
**Applicable to**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

### 3. **Bad Character Rule**
**Principle**: Use character mismatch information to skip more positions in Boyer-Moore.
**Applicable to**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

### 4. **Z-Array Applications**
**Principle**: Use Z-array to find all occurrences of patterns in linear time.
**Applicable to**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **KMP Algorithm Pattern**
```python
def kmp_string_matching(s, p):
    def compute_lps(pattern):
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
    
    positions = []
    n, m = len(s), len(p)
    lps = compute_lps(p)
    i = j = 0
    
    while i < n:
        if p[j] == s[i]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j + 1)
            j = lps[j - 1]
        elif i < n and p[j] != s[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions
```

### 2. **Boyer-Moore Pattern**
```python
def boyer_moore_string_matching(s, p):
    def build_bad_char_table(pattern):
        m = len(pattern)
        bad_char = {}
        
        for i in range(m - 1):
            bad_char[pattern[i]] = m - 1 - i
        
        return bad_char
    
    positions = []
    n, m = len(s), len(p)
    bad_char = build_bad_char_table(p)
    i = m - 1
    
    while i < n:
        j = m - 1
        k = i
        
        while j >= 0 and s[k] == p[j]:
            k -= 1
            j -= 1
        
        if j == -1:
            positions.append(k + 2)
            i += 1
        else:
            i += bad_char.get(s[i], m)
    
    return positions
```

### 3. **Z-Algorithm Pattern**
```python
def z_algorithm_string_matching(s, p):
    def compute_z_array(s):
        n = len(s)
        z = [0] * n
        l = r = 0
        
        for i in range(1, n):
            if i > r:
                l = r = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and s[r - l] == s[r]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        
        return z
    
    combined = p + '$' + s
    z = compute_z_array(combined)
    positions = []
    
    for i in range(len(p) + 1, len(combined)):
        if z[i] == len(p):
            positions.append(i - len(p))
    
    return positions
```

## Edge Cases to Remember

1. **Empty pattern**: Return all positions
2. **Empty string**: Return empty list
3. **Pattern longer than string**: Return empty list
4. **Pattern equals string**: Return position 1
5. **Multiple occurrences**: Return all positions

## Problem-Solving Framework

1. **Identify matching nature**: This is a string matching problem
2. **Choose algorithm**: Use KMP for general cases, Boyer-Moore for large alphabets
3. **Preprocess pattern**: Build failure function or bad character table
4. **Match efficiently**: Use preprocessing to skip unnecessary comparisons
5. **Return positions**: Return all 1-indexed positions

---

*This analysis shows how to efficiently find pattern occurrences using advanced string matching algorithms.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Case-Insensitive Matching**
**Problem**: Find pattern matches ignoring case differences.
```python
def case_insensitive_matching(s, p):
    s_lower = s.lower()
    p_lower = p.lower()
    positions = []
    n, m = len(s), len(p)
    
    for i in range(n - m + 1):
        if s_lower[i:i + m] == p_lower:
            positions.append(i + 1)
    
    return positions
```

#### **Variation 2: Multiple Pattern Matching**
**Problem**: Find all occurrences of multiple patterns in the string.
```python
def multiple_pattern_matching(s, patterns):
    # Use Aho-Corasick algorithm for multiple patterns
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end = False
            self.pattern = None
            self.fail = None
    
    def build_trie(patterns):
        root = TrieNode()
        for pattern in patterns:
            node = root
            for char in pattern:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end = True
            node.pattern = pattern
        return root
    
    def build_failure_links(root):
        queue = []
        for char, child in root.children.items():
            child.fail = root
            queue.append(child)
        
        while queue:
            current = queue.pop(0)
            for char, child in current.children.items():
                fail = current.fail
                while fail and char not in fail.children:
                    fail = fail.fail
                child.fail = fail.children[char] if fail else root
                queue.append(child)
    
    root = build_trie(patterns)
    build_failure_links(root)
    
    results = {pattern: [] for pattern in patterns}
    current = root
    
    for i, char in enumerate(s):
        while current and char not in current.children:
            current = current.fail
        current = current.children[char] if current else root
        
        temp = current
        while temp:
            if temp.is_end:
                results[temp.pattern].append(i - len(temp.pattern) + 2)  # 1-indexed
            temp = temp.fail
    
    return results
```

#### **Variation 3: Fuzzy String Matching**
**Problem**: Find pattern matches allowing k mismatches.
```python
def fuzzy_string_matching(s, p, k):
    positions = []
    n, m = len(s), len(p)
    
    for i in range(n - m + 1):
        mismatches = 0
        for j in range(m):
            if s[i + j] != p[j]:
                mismatches += 1
                if mismatches > k:
                    break
        if mismatches <= k:
            positions.append(i + 1)
    
    return positions
```

#### **Variation 4: Regular Expression Matching**
**Problem**: Find matches using simple regular expressions (.*, ?, +).
```python
def regex_matching(s, pattern):
    # Simple regex matching with .* and ?
    n, m = len(s), len(pattern)
    
    def match(i, j):
        if j == m:
            return i == n
        
        if j + 1 < m and pattern[j + 1] == '*':
            # Handle *
            if match(i, j + 2):  # Skip *
                return True
            if i < n and (pattern[j] == '.' or s[i] == pattern[j]):
                return match(i + 1, j)
            return False
        elif j + 1 < m and pattern[j + 1] == '?':
            # Handle ?
            if match(i, j + 2):  # Skip ?
                return True
            if i < n and (pattern[j] == '.' or s[i] == pattern[j]):
                return match(i + 1, j + 2)
            return False
        else:
            # Handle normal character
            if i < n and (pattern[j] == '.' or s[i] == pattern[j]):
                return match(i + 1, j + 1)
            return False
    
    positions = []
    for i in range(n):
        if match(i, 0):
            positions.append(i + 1)
    
    return positions
```

#### **Variation 5: Circular String Matching**
**Problem**: Find pattern matches in circular string (string can wrap around).
```python
def circular_string_matching(s, p):
    # Create circular string by duplicating
    circular_s = s + s
    positions = []
    n, m = len(s), len(p)
    
    for i in range(n):  # Only check starting positions in original string
        if circular_s[i:i + m] == p:
            positions.append(i + 1)
    
    return positions
```

### 🔗 **Related Problems & Concepts**

#### **1. String Processing Problems**
- **String Manipulation**: Concatenation, substring, replacement
- **String Validation**: Check if string follows certain patterns
- **String Compression**: Compress strings efficiently
- **String Transformation**: Convert between different formats

#### **2. Pattern Matching Algorithms**
- **KMP Algorithm**: Linear time pattern matching
- **Boyer-Moore**: Efficient with bad character rule
- **Rabin-Karp**: Hash-based pattern matching
- **Aho-Corasick**: Multiple pattern matching

#### **3. String Analysis Problems**
- **Palindrome Detection**: Check if string is palindrome
- **Anagram Detection**: Check if strings are anagrams
- **String Similarity**: Calculate similarity between strings
- **String Alignment**: Align strings optimally

#### **4. Text Processing Problems**
- **Text Search**: Search for words in text
- **Text Parsing**: Parse structured text
- **Text Compression**: Compress text data
- **Text Indexing**: Build search indices

#### **5. Bioinformatics Problems**
- **DNA Sequence Matching**: Match DNA sequences
- **Protein Sequence Alignment**: Align protein sequences
- **Genome Assembly**: Assemble genome fragments
- **Sequence Motif Finding**: Find common patterns

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    p = input().strip()
    positions = string_matching_kmp(s, p)
    print(*positions if positions else "No matches found")
```

#### **2. Range Queries on String Properties**
```python
# Precompute pattern occurrences for all substrings
def precompute_occurrences(s, max_length):
    n = len(s)
    occurrences = {}
    
    for length in range(1, max_length + 1):
        for i in range(n - length + 1):
            substring = s[i:i + length]
            if substring not in occurrences:
                occurrences[substring] = []
            occurrences[substring].append(i + 1)
    
    return occurrences

# Answer queries about pattern occurrences
def pattern_query(occurrences, pattern):
    return occurrences.get(pattern, [])
```

#### **3. Interactive String Problems**
```python
# Interactive string matching game
def interactive_string_matching():
    s = input("Enter the main string: ")
    print(f"String length: {len(s)}")
    
    while True:
        p = input("Enter pattern to search (or 'quit' to exit): ")
        if p.lower() == 'quit':
            break
        
        positions = string_matching_kmp(s, p)
        if positions:
            print(f"Pattern found at positions: {positions}")
        else:
            print("Pattern not found")
```

### 🧮 **Mathematical Extensions**

#### **1. String Theory Concepts**
- **String Properties**: Periodicity, borders, periods
- **String Functions**: Failure function, border array
- **String Automata**: Finite automata for string matching
- **String Complexity**: Kolmogorov complexity of strings

#### **2. Algorithmic String Analysis**
- **Suffix Arrays**: Sort all suffixes of a string
- **Suffix Trees**: Tree representation of all suffixes
- **LCP Arrays**: Longest common prefix arrays
- **Burrows-Wheeler Transform**: String transformation

#### **3. Advanced Pattern Matching**
- **Approximate Matching**: Allow errors in matching
- **Weighted Matching**: Assign weights to matches
- **Constrained Matching**: Add constraints to matches
- **Multi-dimensional Matching**: Match in multiple dimensions

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **String Algorithms**: KMP, Boyer-Moore, Rabin-Karp
- **Suffix Structures**: Suffix arrays, suffix trees, suffix automata
- **Compression Algorithms**: LZ77, LZ78, Huffman coding
- **Parsing Algorithms**: Regular expression parsing, context-free parsing

#### **2. Mathematical Concepts**
- **Combinatorics**: String combinatorics and counting
- **Information Theory**: Entropy, compression, encoding
- **Formal Languages**: Regular languages, context-free languages
- **Automata Theory**: Finite automata, pushdown automata

#### **3. Programming Concepts**
- **String Representations**: Character arrays, string objects
- **Memory Management**: Efficient string storage and manipulation
- **Algorithm Optimization**: Improving string algorithm performance
- **Error Handling**: Dealing with invalid inputs and edge cases

---

*This analysis demonstrates efficient string matching techniques and shows various extensions for pattern matching problems.* 