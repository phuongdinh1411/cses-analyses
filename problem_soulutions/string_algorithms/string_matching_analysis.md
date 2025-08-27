# CSES String Matching - Problem Analysis

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