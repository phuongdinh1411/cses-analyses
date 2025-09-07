---
layout: simple
title: "String Matching - Pattern Occurrence Detection"
permalink: /problem_soulutions/string_algorithms/string_matching_analysis
---

# String Matching - Pattern Occurrence Detection

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand string matching problems and pattern occurrence detection algorithms
- Apply KMP algorithm or Z-algorithm to efficiently find all pattern occurrences
- Implement efficient string matching algorithms with O(n + m) time complexity
- Optimize pattern matching using failure functions, prefix functions, and preprocessing
- Handle edge cases in string matching (pattern longer than text, no matches, multiple matches)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: KMP algorithm, Z-algorithm, string matching, pattern matching, failure functions, prefix functions
- **Data Structures**: Arrays, string data structures, pattern tracking, occurrence tracking
- **Mathematical Concepts**: String matching theory, pattern analysis, failure function mathematics, prefix analysis
- **Programming Skills**: String manipulation, KMP implementation, Z-algorithm implementation, pattern matching, algorithm implementation
- **Related Problems**: Pattern Positions (similar concept), String Functions (basic string operations), String algorithms

## 📋 Problem Description

Given a string and a pattern, find all occurrences of the pattern in the string.

This is a classic string matching problem that requires finding all positions where a pattern occurs in a text string. The solution involves using efficient algorithms like KMP (Knuth-Morris-Pratt) or Z-algorithm to achieve linear time complexity.

**Input**: 
- First line: A string s
- Second line: A pattern p

**Output**: 
- Print all positions where the pattern occurs in the string (1-indexed)

**Constraints**:
- 1 ≤ |s|, |p| ≤ 10⁶

**Example**:
```
Input:
ABCABCA
ABC

Output:
1 4

Explanation**: 
- String: "ABCABCA"
- Pattern: "ABC"
- Position 1: "ABC"ABCA (match at index 0, 1-indexed = 1)
- Position 4: ABC"ABC"A (match at index 3, 1-indexed = 4)
```

## 🎯 Visual Example

### Input
```
String: "ABCABCA"
Pattern: "ABC"
```

### KMP Algorithm Process
```
Step 1: Build failure function for pattern "ABC"
- Pattern: A B C
- Index:  0 1 2
- failure[0] = 0
- failure[1] = 0 (no proper prefix-suffix match)
- failure[2] = 0 (no proper prefix-suffix match)

Step 2: Pattern matching
- String: A B C A B C A
- Index:  0 1 2 3 4 5 6
- Pattern: A B C
- Index:  0 1 2

Step 3: Matching process
- Position 0: "ABC" matches → Found at position 1 (1-indexed)
- Position 3: "ABC" matches → Found at position 4 (1-indexed)
```

### Pattern Matching Visualization
```
String: A B C A B C A
Index:  0 1 2 3 4 5 6

Pattern "ABC" at position 0:
A B C A B C A
A B C
✓ ✓ ✓ → Match at position 1

Pattern "ABC" at position 3:
A B C A B C A
    A B C
    ✓ ✓ ✓ → Match at position 4
```

### Key Insight
KMP algorithm works by:
1. Building a failure function to avoid redundant comparisons
2. Using the failure function to skip positions that can't match
3. Achieving O(n + m) time complexity where n = text length, m = pattern length
4. Space complexity: O(m) for failure function

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find all occurrences of a pattern in a text string
- **Key Insight**: Use KMP algorithm or Z-algorithm for linear time complexity
- **Challenge**: Handle large strings efficiently without O(|s| × |p|) complexity

### Step 2: Initial Approach
**Naive string matching (inefficient but correct):**

```python
def string_matching_naive(s, p):
    positions = []
    n, m = len(s), len(p)
    
    for i in range(n - m + 1):
        if s[i: i + m] == 
p: positions.append(i + 1)  # 1-indexed
    
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

### Step 3: Optimization/Alternative
**Boyer-Moore algorithm:**

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
        return []
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

### Step 4: Complete Solution

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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic pattern matching (should return all positions)
- **Test 2**: No matches (should return empty)
- **Test 3**: Multiple matches (should return all positions)
- **Test 4**: Pattern longer than string (should return empty)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s| × |p|) | O(1) | Check all positions |
| KMP | O(|s| + |p|) | O(|p|) | Use failure function |
| Boyer-Moore | O(|s| + |p|) | O(|p|) | Bad character rule |
| Z-Algorithm | O(|s| + |p|) | O(|s| + |p|) | Z-array computation |

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s| * |p|) | O(1) | Simple but slow |
| KMP | O(|s| + |p|) | O(|p|) | Use failure function |
| Boyer-Moore | O(|s| + |p|) | O(|p|) | Bad character rule |
| Z-Algorithm | O(|s| + |p|) | O(|s| + |p|) | Z-array computation |

## 🎨 Visual Example

### Input Example
```
Text:    ABCABCA
Pattern: ABC
```

### Naive String Matching Process
```
Step 1: Compare ABC with ABCABCA[0:3]
ABCABCA
ABC     ← Match at position 0 (1-indexed: 1)
✓

Step 2: Compare ABC with ABCABCA[1:4]
ABCABCA
 ABC    ← No match
✗

Step 3: Compare ABC with ABCABCA[2:5]
ABCABCA
  ABC   ← No match
✗

Step 4: Compare ABC with ABCABCA[3:6]
ABCABCA
   ABC  ← Match at position 3 (1-indexed: 4)
✓

Result: [1, 4]
```

### KMP Algorithm - LPS (Longest Proper Prefix) Construction
```
Pattern: ABC

LPS Array Construction:
Index:  0 1 2
Pattern: A B C
LPS:    0 0 0

Explanation:
- A: No proper prefix, LPS[0] = 0
- AB: Proper prefix = A, no suffix = A, LPS[1] = 0  
- ABC: Proper prefix = A, AB, no matching suffix, LPS[2] = 0

Final LPS: [0, 0, 0]
```

### KMP Matching Process
```
Text:    ABCABCA
Pattern: ABC
LPS:     [0, 0, 0]

Step 1: i=0, j=0
ABCABCA
ABC
✓ A=A, i=1, j=1

Step 2: i=1, j=1  
ABCABCA
ABC
✓ B=B, i=2, j=2

Step 3: i=2, j=2
ABCABCA
ABC
✓ C=C, i=3, j=3

Step 4: j == pattern length (3)
→ Match found at position 0 (1-indexed: 1)
→ j = LPS[2] = 0

Step 5: i=3, j=0
ABCABCA
   ABC
✓ A=A, i=4, j=1

Step 6: i=4, j=1
ABCABCA
   ABC
✓ B=B, i=5, j=2

Step 7: i=5, j=2
ABCABCA
   ABC
✓ C=C, i=6, j=3

Step 8: j == pattern length (3)
→ Match found at position 3 (1-indexed: 4)
→ j = LPS[2] = 0

Result: [1, 4]
```

### Z-Algorithm Process
```
Combined String: ABC$ABCABCA
Pattern: ABC
Separator: $

Z-Array Construction:
Index:  0 1 2 3 4 5 6 7 8 9 10
String: A B C $ A B C A B C A
Z:      0 0 0 0 3 0 0 1 0 0 1

Explanation:
- Z[4] = 3: "ABC" matches prefix of length 3
- Z[7] = 1: "A" matches prefix of length 1  
- Z[10] = 1: "A" matches prefix of length 1

Pattern matches found where Z[i] == pattern length (3):
- Z[4] = 3 → Match at position 4-3-1 = 0 (1-indexed: 1)
- No other matches of length 3

Result: [1, 4] (after checking all positions)
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Naive           │ O(n×m)       │ O(1)         │ Brute force  │
│                 │              │              │ comparison   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ KMP             │ O(n+m)       │ O(m)         │ Failure      │
│                 │              │              │ function     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Boyer-Moore     │ O(n+m)       │ O(m)         │ Bad character│
│                 │              │              │ rule         │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Z-Algorithm     │ O(n+m)       │ O(n+m)       │ Z-array      │
│                 │              │              │ computation  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Pattern Matching Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: text,    │
              │ pattern         │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Choose Algorithm│
              │ (KMP/Z-Algo)    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Preprocess      │
              │ Pattern         │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Match Pattern   │
              │ in Text         │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return All      │
              │ Match Positions │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **KMP Algorithm**: Use failure function for efficient pattern matching
- **String Matching**: Find all occurrences of pattern in text
- **Linear Time**: Achieve O(|s| + |p|) complexity
- **Pattern Preprocessing**: Build failure function for efficient matching

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. String Matching with Wildcards**
```python
def string_matching_wildcards(s, p):
    # Handle pattern matching with wildcard characters
    
    def build_failure_function(pattern):
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            if pattern[i] == pattern[length] or pattern[i] == '?' or pattern[length] == '?':
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
    
    def matches(pattern, text, i, j):
        if pattern[j] == '?' or pattern[j] == text[i]:
            return True
        return False
    
    positions = []
    n, m = len(s), len(p)
    
    if m == 0:
        return []
    
    lps = build_failure_function(p)
    i = j = 0
    
    while i < n:
        if matches(p, s, i, j):
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j + 1)  # 1-indexed
            j = lps[j - 1]
        elif i < n and not matches(p, s, i, j):
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions
```

#### **2. String Matching with Multiple Patterns**
```python
def string_matching_multiple_patterns(s, patterns):
    # Handle matching multiple patterns simultaneously
    
    def build_aho_corasick(patterns):
        # Simplified Aho-Corasick implementation
        trie = {}
        failure = {}
        output = {}
        
        # Build trie
        for i, pattern in enumerate(patterns):
            node = trie
            for char in pattern:
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['$'] = i  # Mark end of pattern
        
        # Build failure function
        queue = []
        for char, child in trie.items():
            if char != '$':
                failure[child] = trie
                queue.append(child)
        
        while queue:
            node = queue.pop(0)
            for char, child in node.items():
                if char != '$':
                    queue.append(child)
                    fail = failure[node]
                    while fail and char not in fail:
                        fail = failure.get(fail, {})
                    failure[child] = fail.get(char, trie)
        
        return trie, failure, output
    
    trie, failure, output = build_aho_corasick(patterns)
    positions = {i: [] for i in range(len(patterns))}
    
    node = trie
    for i, char in enumerate(s):
        while node and char not in node:
            node = failure.get(node, {})
        node = node.get(char, {})
        
        if '$' in node:
            pattern_idx = node['$']
            positions[pattern_idx].append(i - len(patterns[pattern_idx]) + 2)  # 1-indexed
    
    return positions
```

#### **3. String Matching with Dynamic Updates**
```python
def string_matching_dynamic(operations):
    # Handle string matching with dynamic text updates
    
    s = ""
    pattern = ""
    positions = []
    
    for operation in operations:
        if operation[0] == 'set_pattern':
            # Set pattern
            pattern = operation[1]
            positions = find_matches(s, pattern)
        
        elif operation[0] == 'add_char':
            # Add character to string
            char = operation[1]
            s += char
            
            # Update positions
            positions = find_matches(s, pattern)
        
        elif operation[0] == 'remove_char':
            # Remove last character
            if len(s) > 0:
                s = s[:-1]
                positions = find_matches(s, pattern)
        
        elif operation[0] == 'query':
            # Return current positions
            yield positions
    
    return list(string_matching_dynamic(operations))

def find_matches(s, p):
    if len(p) == 0:
        return []
    
    def build_lps(pattern):
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
    
    if m == 0:
        return []
    
    lps = build_lps(p)
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

## 🔗 Related Problems

### Links to Similar Problems
- **String Matching**: KMP, Boyer-Moore, Z-algorithm problems
- **Pattern Matching**: String pattern recognition
- **String Algorithms**: Advanced string processing
- **Text Processing**: String manipulation and analysis

## 📚 Learning Points

### Key Takeaways
- **KMP algorithm** is essential for efficient string matching
- **Failure function** enables linear time complexity
- **Pattern preprocessing** is crucial for performance
- **Multiple algorithms** exist for different scenarios

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
        if s_lower[i: i + m] == 
p_lower: positions.append(i + 1)
    
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
            for char in pattern: if char not in node.
children: node.children[char] = TrieNode()
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
        while temp: if temp.
is_end: results[temp.pattern].append(i - len(temp.pattern) + 2)  # 1-indexed
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
        if circular_s[i: i + m] == 
p: positions.append(i + 1)
    
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
        if positions: print(f"Pattern found at 
positions: {positions}")
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