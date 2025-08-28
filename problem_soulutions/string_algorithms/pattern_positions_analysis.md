---
layout: simple
title: "Pattern Positions
permalink: /problem_soulutions/string_algorithms/pattern_positions_analysis/
---

# Pattern Positions

## Problem Statement
Given a string and a pattern, find all positions where the pattern occurs in the string.

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
ababab
ab

Output:
1 3 5
```

## Solution Progression

### Approach 1: Check All Positions - O(|s| × |p|)
**Description**: Check each position in the string to see if the pattern starts there.

```python
def pattern_positions_naive(s, p):
    positions = []
    n, m = len(s), len(p)
    
    for i in range(n - m + 1):
        if s[i:i + m] == p:
            positions.append(i + 1)  # 1-indexed
    
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

### Improvement 2: Boyer-Moore Algorithm - O(|s| + |p|)
**Description**: Use Boyer-Moore algorithm with bad character rule for efficient matching.

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
    
    # Concatenate pattern + separator + string"
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

## Final Optimal Solution

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

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s| × |p|) | O(1) | Check each position |
| KMP | O(|s| + |p|) | O(|p|) | Use failure function |
| Boyer-Moore | O(|s| + |p|) | O(|p|) | Use bad character rule |
| Z-Algorithm | O(|s| + |p|) | O(|s| + |p|) | Use Z-array |

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
    for l, r, pattern in queries:
        substring = s[l:r]
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