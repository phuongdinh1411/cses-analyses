---
layout: simple
title: "Pattern Positions - Find All Pattern Occurrences"
permalink: /problem_soulutions/string_algorithms/pattern_positions_analysis
---

# Pattern Positions - Find All Pattern Occurrences

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand pattern position problems and string matching algorithms for occurrence detection
- Apply KMP algorithm or Z-algorithm to efficiently find all pattern occurrence positions
- Implement efficient pattern position algorithms with O(n + m) time complexity
- Optimize pattern matching using failure functions, prefix functions, and preprocessing techniques
- Handle edge cases in pattern positions (pattern longer than text, no matches, overlapping matches)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: KMP algorithm, Z-algorithm, string matching, pattern matching, failure functions, prefix functions
- **Data Structures**: Arrays, string data structures, pattern tracking, position tracking, occurrence tracking
- **Mathematical Concepts**: String matching theory, pattern analysis, failure function mathematics, prefix analysis
- **Programming Skills**: String manipulation, KMP implementation, Z-algorithm implementation, pattern matching, algorithm implementation
- **Related Problems**: String Matching (similar concept), String Functions (basic string operations), String algorithms

## 📋 Problem Description

Given a string and a pattern, find all positions where the pattern occurs in the string.

This is a string matching problem that requires finding all starting positions where a pattern occurs in a text string. The solution involves using efficient algorithms like KMP (Knuth-Morris-Pratt) or Z-algorithm to achieve linear time complexity.

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
ababab
ab

Output:
1 3 5

Explanation**: 
- String: "ababab"
- Pattern: "ab"
- Position 1: "ab"abab (match at index 0, 1-indexed = 1)
- Position 3: ab"ab"ab (match at index 2, 1-indexed = 3)
- Position 5: abab"ab" (match at index 4, 1-indexed = 5)
```

## 🎯 Visual Example

### Input
```
String: "ababab"
Pattern: "ab"
```

### KMP Algorithm Process
```
Step 1: Build failure function for pattern "ab"
- Pattern: a b
- Index:  0 1
- failure[0] = 0
- failure[1] = 0 (no proper prefix-suffix match)

Step 2: Pattern matching
- String: a b a b a b
- Index:  0 1 2 3 4 5
- Pattern: a b
- Index:  0 1

Step 3: Matching process
- Position 0: "ab" matches → Found at position 1 (1-indexed)
- Position 2: "ab" matches → Found at position 3 (1-indexed)
- Position 4: "ab" matches → Found at position 5 (1-indexed)
```

### Pattern Matching Visualization
```
String: a b a b a b
Index:  0 1 2 3 4 5

Pattern "ab" at position 0:
a b a b a b
a b
✓ ✓ → Match at position 1

Pattern "ab" at position 2:
a b a b a b
    a b
    ✓ ✓ → Match at position 3

Pattern "ab" at position 4:
a b a b a b
        a b
        ✓ ✓ → Match at position 5
```

### Key Insight
KMP algorithm works by:
1. Building a failure function to avoid redundant comparisons
2. Using the failure function to skip positions that can't match
3. Achieving O(n + m) time complexity where n = text length, m = pattern length
4. Space complexity: O(m) for failure function

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find all starting positions where a pattern occurs in a text string
- **Key Insight**: Use KMP algorithm or Z-algorithm for linear time complexity
- **Challenge**: Handle large strings efficiently without O(|s| × |p|) complexity

### Step 2: Initial Approach
**Check all positions (inefficient but correct):**

```python
def pattern_positions_naive(s, p):
    positions = []
    n, m = len(s), len(p)
    
    for i in range(n - m + 1):
        if s[i: i + m] == 
p: positions.append(i + 1)  # 1-indexed
    
    return positions
```

**Why this is inefficient**: Quadratic time complexity for large strings.

### Improvement 1: KMP Algorithm - O(|s| + |p|)
**Description**: Use the Knuth-Morris-Pratt algorithm for efficient string matching.

```python
def pattern_positions_kmp(s, p):
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
def pattern_positions_boyer_moore(s, p):
    def build_bad_char_table(pattern):
        table = {}
        m = len(pattern)
        for i in range(m - 1):
            table[pattern[i]] = m - 1 - i
        return table
    
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
            j -= 1
            k -= 1
        
        if j == -1:
            positions.append(k + 2)  # 1-indexed
            i += 1
        else:
            shift = bad_char.get(s[k], m)
            i += max(1, shift - (m - 1 - j))
    
    return positions
```

**Why this improvement works**: Boyer-Moore uses bad character rule to skip comparisons.

### Alternative: Z-Algorithm - O(|s| + |p|)
**Description**: Use Z-algorithm to find pattern occurrences.

```python
def pattern_positions_z(s, p):
    def compute_z_array(text):
        n = len(text)
        z = [0] * n
        l = r = 0
        
        for i in range(1, n):
            if i > r:
                l = r = i
                while r < n and text[r - l] == text[r]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and text[r - l] == text[r]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        return z
    
    # Concatenate pattern + separator + string
    text = p + '$' + s
    z = compute_z_array(text)
    
    positions = []
    m = len(p)
    
    for i in range(m + 1, len(z)):
        if z[i] == m:
            positions.append(i - m)  # Convert to 1-indexed
    
    return positions
```

**Why this works**: Z-algorithm efficiently finds all occurrences of a pattern.

### Step 4: Complete Solution

```python
s = input().strip()
p = input().strip()

def pattern_positions_kmp(s, p):
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

positions = pattern_positions_kmp(s, p)
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
| Naive | O(|s| × |p|) | O(1) | Check each position |
| KMP | O(|s| + |p|) | O(|p|) | Use failure function |
| Boyer-Moore | O(|s| + |p|) | O(|p|) | Use bad character rule |
| Z-Algorithm | O(|s| + |p|) | O(|s| + |p|) | Use Z-array |

## 🎨 Visual Example

### Input Example
```
Text:    "ababab"
Pattern: "ab"
```

### Naive Pattern Matching Process
```
Text:    a b a b a b
Pattern: a b
Index:   0 1 2 3 4 5

Step 1: Check position 0
a b a b a b
a b
✓ Match at position 0 (1-indexed: 1)

Step 2: Check position 1
a b a b a b
  a b
✗ No match (a ≠ b)

Step 3: Check position 2
a b a b a b
    a b
✓ Match at position 2 (1-indexed: 3)

Step 4: Check position 3
a b a b a b
      a b
✗ No match (a ≠ b)

Step 5: Check position 4
a b a b a b
        a b
✓ Match at position 4 (1-indexed: 5)

Result: [1, 3, 5]
```

### KMP Algorithm Process
```
Text:    a b a b a b
Pattern: a b
LPS:     [0, 0]

Step 1: i=0, j=0
a b a b a b
a b
✓ a=a, i=1, j=1

Step 2: i=1, j=1
a b a b a b
a b
✓ b=b, i=2, j=2

Step 3: j == pattern length (2)
→ Match found at position 0 (1-indexed: 1)
→ j = LPS[1] = 0

Step 4: i=2, j=0
a b a b a b
    a b
✓ a=a, i=3, j=1

Step 5: i=3, j=1
a b a b a b
    a b
✓ b=b, i=4, j=2

Step 6: j == pattern length (2)
→ Match found at position 2 (1-indexed: 3)
→ j = LPS[1] = 0

Step 7: i=4, j=0
a b a b a b
        a b
✓ a=a, i=5, j=1

Step 8: i=5, j=1
a b a b a b
        a b
✓ b=b, i=6, j=2

Step 9: j == pattern length (2)
→ Match found at position 4 (1-indexed: 5)
→ j = LPS[1] = 0

Result: [1, 3, 5]
```

### Z-Algorithm Process
```
Combined String: ab$ababab
Pattern: ab
Separator: $

Z-Array Construction:
Index:  0 1 2 3 4 5 6 7 8
String: a b $ a b a b a b
Z:      8 0 0 2 0 2 0 2 0

Explanation:
- Z[0] = 8: Entire string matches itself
- Z[1] = 0: "b" doesn't match prefix starting at 0
- Z[2] = 0: "$" doesn't match prefix starting at 0
- Z[3] = 2: "ab" matches prefix of length 2
- Z[4] = 0: "a" doesn't match prefix starting at 0
- Z[5] = 2: "ab" matches prefix of length 2
- Z[6] = 0: "a" doesn't match prefix starting at 0
- Z[7] = 2: "ab" matches prefix of length 2
- Z[8] = 0: "b" doesn't match prefix starting at 0

Pattern matches found where Z[i] == pattern length (2):
- Z[3] = 2 → Match at position 3-2-1 = 0 (1-indexed: 1)
- Z[5] = 2 → Match at position 5-2-1 = 2 (1-indexed: 3)
- Z[7] = 2 → Match at position 7-2-1 = 4 (1-indexed: 5)

Result: [1, 3, 5]
```

### Boyer-Moore Algorithm Process
```
Text:    a b a b a b
Pattern: a b
Index:   0 1 2 3 4 5

Bad Character Table:
- 'a': 1 (pattern length - 1 - last occurrence of 'a')
- 'b': 0 (pattern length - 1 - last occurrence of 'b')

Step 1: Start at position 1 (pattern length - 1)
a b a b a b
    a b
Compare from right: b=b ✓, a=a ✓
→ Match found at position 0 (1-indexed: 1)
→ Shift by 1

Step 2: Position 2
a b a b a b
      a b
Compare from right: b=b ✓, a=a ✓
→ Match found at position 2 (1-indexed: 3)
→ Shift by 1

Step 3: Position 4
a b a b a b
          a b
Compare from right: b=b ✓, a=a ✓
→ Match found at position 4 (1-indexed: 5)
→ Shift by 1

Result: [1, 3, 5]
```

### Pattern Matching Visualization
```
Text:    a b a b a b
Pattern: a b
         1 2 3 4 5 6  (1-indexed positions)

Matches:
Position 1: "ab"abab
Position 3: ab"ab"ab  
Position 5: abab"ab"

Pattern appears 3 times at positions: 1, 3, 5
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Naive           │ O(n×m)       │ O(1)         │ Check each   │
│                 │              │              │ position     │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ KMP             │ O(n+m)       │ O(m)         │ Use failure  │
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
              │ (KMP/Z-Algo/    │
              │  Boyer-Moore)   │
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
              │ Search Pattern  │
              │ in Text         │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Collect All     │
              │ Match Positions │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return Positions│
              │ (1-indexed)     │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **KMP Algorithm**: Use failure function for efficient pattern matching
- **Pattern Matching**: Find all occurrences of pattern in text
- **Linear Time**: Achieve O(|s| + |p|) complexity
- **Multiple Algorithms**: KMP, Boyer-Moore, Z-algorithm options

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Pattern Positions with Wildcards**
```python
def pattern_positions_wildcards(s, p):
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

#### **2. Pattern Positions with Multiple Patterns**
```python
def pattern_positions_multiple_patterns(s, patterns):
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

#### **3. Pattern Positions with Dynamic Updates**
```python
def pattern_positions_dynamic(operations):
    # Handle pattern positions with dynamic text updates
    
    s = ""
    pattern = ""
    positions = []
    
    for operation in operations:
        if operation[0] == 'set_pattern':
            # Set pattern
            pattern = operation[1]
            positions = find_pattern_positions(s, pattern)
        
        elif operation[0] == 'add_char':
            # Add character to string
            char = operation[1]
            s += char
            
            # Update positions
            positions = find_pattern_positions(s, pattern)
        
        elif operation[0] == 'remove_char':
            # Remove last character
            if len(s) > 0:
                s = s[:-1]
                positions = find_pattern_positions(s, pattern)
        
        elif operation[0] == 'query':
            # Return current positions
            yield positions
    
    return list(pattern_positions_dynamic(operations))

def find_pattern_positions(s, p):
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
- **KMP algorithm** is essential for efficient pattern matching
- **Failure function** enables linear time complexity
- **Multiple algorithms** exist for different scenarios
- **Pattern preprocessing** is crucial for performance

## Key Insights for Other Problems

### 1. **String Matching Problems**
**Principle**: Use specialized algorithms like KMP for efficient string matching.
**Applicable to**:
- String matching
- Pattern recognition
- Text processing
- Algorithm design

**Example Problems**:
- String matching
- Pattern recognition
- Text processing
- Algorithm design

### 2. **Failure Function (LPS)**
**Principle**: Use failure function to avoid unnecessary comparisons in string matching.
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
**Principle**: Use bad character rule to skip comparisons in string matching.
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

### 4. **Z-Algorithm Applications**
**Principle**: Use Z-algorithm for efficient pattern matching and string analysis.
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
    
    if m == 0:
        return []
    
    lps = compute_lps(p)
    i = j = 0
    
    while i < n:
        if p[j] == s[i]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j)
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
        table = {}
        m = len(pattern)
        for i in range(m - 1):
            table[pattern[i]] = m - 1 - i
        return table
    
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
            j -= 1
            k -= 1
        
        if j == -1:
            positions.append(k + 1)
            i += 1
        else:
            shift = bad_char.get(s[k], m)
            i += max(1, shift - (m - 1 - j))
    
    return positions
```

### 3. **Z-Algorithm Pattern**
```python
def z_algorithm_string_matching(s, p):
    def compute_z_array(text):
        n = len(text)
        z = [0] * n
        l = r = 0
        
        for i in range(1, n):
            if i > r:
                l = r = i
                while r < n and text[r - l] == text[r]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and text[r - l] == text[r]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        return z
    
    text = p + '$' + s
    z = compute_z_array(text)
    
    positions = []
    m = len(p)
    
    for i in range(m + 1, len(z)):
        if z[i] == m:
            positions.append(i - m - 1)
    
    return positions
```

## Edge Cases to Remember

1. **Empty pattern**: Return all positions
2. **Empty string**: Return empty list
3. **Pattern longer than string**: Return empty list
4. **Pattern not found**: Return empty list
5. **Multiple occurrences**: Return all positions
6. **1-indexed output**: Convert 0-indexed to 1-indexed

## Problem-Solving Framework

1. **Identify string matching**: This is a pattern matching problem
2. **Choose algorithm**: Use KMP algorithm for efficiency
3. **Compute failure function**: Build LPS array for the pattern
4. **Match pattern**: Use failure function to avoid unnecessary comparisons
5. **Return positions**: Return all 1-indexed positions

---

*This analysis shows how to efficiently find all pattern occurrences using KMP algorithm and other string matching techniques.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Pattern Positions with Multiple Patterns**
**Problem**: Find positions of multiple patterns in a string.
```python
def multiple_pattern_positions(s, patterns):
    # patterns = [pattern1, pattern2, ...]
    
    all_positions = {}
    
    for pattern in patterns:
        positions = kmp_string_matching(s, pattern)
        all_positions[pattern] = positions
    
    return all_positions
```

#### **Variation 2: Pattern Positions with Constraints**
**Problem**: Find pattern positions with additional constraints (overlap, distance, etc.).
```python
def constrained_pattern_positions(s, p, constraints):
    # constraints = {'min_distance': x, 'max_overlap': y, 'alphabet': chars}
    
    # Apply alphabet constraint
    if 'alphabet' in constraints:
        if not all(c in constraints['alphabet'] for c in p):
            return []
    
    positions = kmp_string_matching(s, p)
    
    # Apply distance constraints
    if 'min_distance' in constraints:
        filtered_positions = []
        for i, pos in enumerate(positions):
            if i == 0 or pos - positions[i-1] >= constraints['min_distance']:
                filtered_positions.append(pos)
        positions = filtered_positions
    
    # Apply overlap constraints
    if 'max_overlap' in constraints:
        filtered_positions = []
        for i, pos in enumerate(positions):
            if i == 0 or pos - positions[i-1] >= len(p) - constraints['max_overlap']:
                filtered_positions.append(pos)
        positions = filtered_positions
    
    return positions
```

#### **Variation 3: Pattern Positions with Costs**
**Problem**: Each pattern match has a cost, find positions with minimum total cost.
```python
def cost_based_pattern_positions(s, p, match_cost, max_cost):
    # match_cost = cost per pattern match
    
    positions = kmp_string_matching(s, p)
    
    # Calculate total cost
    total_cost = len(positions) * match_cost
    
    if total_cost <= max_cost:
        return positions
    else:
        # Return subset of positions within budget
        max_matches = max_cost // match_cost
        return positions[:max_matches]
```

#### **Variation 4: Pattern Positions with Probabilities**
**Problem**: Characters have probabilities, find expected pattern positions.
```python
def probabilistic_pattern_positions(s, p, char_probs):
    # char_probs[c] = probability of character c
    
    n, m = len(s), len(p)
    expected_positions = []
    
    # Calculate expected positions based on character probabilities
    for i in range(n - m + 1):
        prob_match = 1.0
        for j in range(m):
            if i + j < n:
                prob_match *= char_probs.get(s[i + j], 0.1)
        
        if prob_match >= 0.5:  # Threshold for expected match
            expected_positions.append(i + 1)  # 1-indexed
    
    return expected_positions
```

#### **Variation 5: Pattern Positions with Updates**
**Problem**: Handle dynamic updates to the string and find new pattern positions.
```python
def dynamic_pattern_positions(s, p, updates):
    # updates = [(pos, new_char), ...]
    
    s = list(s)  # Convert to list for updates
    position_history = []
    
    for pos, new_char in updates:
        s[pos] = new_char
        # Find pattern positions after each update
        positions = kmp_string_matching(''.join(s), p)
        position_history.append(positions)
    
    return position_history
```

### 🔗 **Related Problems & Concepts**

#### **1. String Matching Problems**
- **Pattern Matching**: Find patterns in strings
- **Substring Search**: Search for substrings efficiently
- **Multiple Pattern Matching**: Match multiple patterns simultaneously
- **Approximate String Matching**: Allow errors in matching

#### **2. String Analysis Problems**
- **Pattern Frequency**: Count pattern occurrences
- **Pattern Distribution**: Analyze pattern distribution
- **Pattern Evolution**: Track pattern changes over time
- **Pattern Clustering**: Group similar patterns

#### **3. String Algorithms**
- **KMP Algorithm**: Efficient pattern matching
- **Boyer-Moore**: Fast string searching
- **Rabin-Karp**: Hash-based string matching
- **Z-Algorithm**: Linear time string processing

#### **4. Optimization Problems**
- **Minimization**: Find minimum value solutions
- **Cost Optimization**: Optimize with respect to costs
- **Constrained Optimization**: Optimization with constraints
- **Multi-objective Optimization**: Optimize multiple criteria

#### **5. Algorithmic Techniques**
- **Failure Functions**: KMP failure function applications
- **Sliding Window**: Process data in windows
- **Two Pointers**: Use two pointers for efficiency
- **Hash Functions**: Fast string hashing

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    p = input().strip()
    positions = kmp_string_matching(s, p)
    print(*positions if positions else "No matches found")
```

#### **2. Range Queries on Pattern Positions**
```python
def range_pattern_position_queries(s, queries):
    # queries = [(l, r, pattern), ...] - find pattern in substring s[l:r]
    
    results = []
    for l, r, pattern in queries: substring = s[
l: r]
        positions = kmp_string_matching(substring, pattern)
        # Adjust positions to original string coordinates
        adjusted_positions = [pos + l + 1 for pos in positions]  # 1-indexed
        results.append(adjusted_positions)
    
    return results
```

#### **3. Interactive Pattern Position Problems**
```python
def interactive_pattern_positions():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        p = input("Enter pattern: ")
        positions = kmp_string_matching(s, p)
        print(f"String: {s}")
        print(f"Pattern: {p}")
        print(f"Positions: {positions if positions else 'No matches found'}")
```

### 🧮 **Mathematical Extensions**

#### **1. String Theory**
- **String Properties**: Periodicity, borders, periods
- **String Functions**: Failure function, border array
- **String Complexity**: Kolmogorov complexity of strings
- **String Enumeration**: Count strings with certain properties

#### **2. Pattern Analysis**
- **Pattern Recognition**: Recognize patterns in data
- **Pattern Classification**: Classify patterns into categories
- **Pattern Prediction**: Predict future patterns
- **Pattern Mining**: Extract patterns from data

#### **3. Probability Theory**
- **Expected Values**: Calculate expected outcomes
- **Probability Distributions**: Character probability distributions
- **Stochastic Processes**: Random string generation
- **Markov Chains**: State transitions in strings

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **String Matching**: KMP, Boyer-Moore, Rabin-Karp algorithms
- **Suffix Structures**: Suffix arrays, suffix trees, suffix automata
- **String Compression**: LZ77, LZ78, Huffman coding
- **String Parsing**: Regular expressions, context-free parsing

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

*This analysis demonstrates efficient pattern position finding techniques and shows various extensions for string matching problems.* 