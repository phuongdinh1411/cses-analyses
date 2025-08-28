---
layout: simple
title: "Minimal Rotation"permalink: /problem_soulutions/string_algorithms/minimal_rotation_analysis
---


# Minimal Rotation

## Problem Statement
Given a string, find the lexicographically smallest rotation of the string.

### Input
The first input line has a string s.

### Output
Print the lexicographically smallest rotation of the string.

### Constraints
- 1 ≤ |s| ≤ 10^6

### Example
```
Input:
baabaa

Output:
aabaab
```

## Solution Progression

### Approach 1: Generate All Rotations - O(|s|²)
**Description**: Generate all possible rotations and find the lexicographically smallest one.

```python
def minimal_rotation_naive(s):
    n = len(s)
    rotations = []
    
    # Generate all rotations
    for i in range(n):
        rotation = s[i:] + s[:i]
        rotations.append(rotation)
    
    # Find the lexicographically smallest
    return min(rotations)
```

**Why this is inefficient**: Quadratic time complexity and space complexity.
### Improvement 1: Booth's Algorithm - O(|s|)
**Description**: Use Booth's algorithm to find the lexicographically smallest rotation efficiently.

```python
def minimal_rotation_booth(s):
    n = len(s)
    s = s + s  # Double the string for easier handling
    f = [0] * (2 * n)
    
    k = 0
    for j in range(1, 2 * n):
        i = f[j - k - 1]
        while i > 0 and s[j] != s[k + i]:
            if s[j] < s[k + i]:
                k = j - i
            i = f[i - 1]
        
        if s[j] == s[k + i]:
            i += 1
        else:
            if s[j] < s[k]:
                k = j
            i = 0
        
        f[j - k] = i
    
    return s[k:k + n]
```

**Why this improvement works**: Booth's algorithm finds the minimal rotation in linear time.

### Improvement 2: Duval's Algorithm - O(|s|)
**Description**: Use Duval's algorithm for finding the minimal rotation.

```python
def minimal_rotation_duval(s):
    n = len(s)
    s = s + s
    i = 0
    j = 1
    
    while j < n:
        k = 0
        while k < n and s[i + k] == s[j + k]:
            k += 1
        
        if k == n:
            break
        
        if s[i + k] < s[j + k]:
            j += k + 1
        else:
            i = j
            j = i + 1
    
    return s[i:i + n]
```

**Why this improvement works**: Duval's algorithm is simpler and more efficient for this problem.

### Alternative: Suffix Array Approach - O(|s| log |s|)
**Description**: Use suffix array to find the minimal rotation.

```python
def build_suffix_array(s):
    n = len(s)
    s = s + s  # Double the string
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    return [i for _, i in suffixes]

def minimal_rotation_suffix_array(s):
    n = len(s)
    suffix_array = build_suffix_array(s)
    
    # Find the first suffix that starts within the first n characters
    for i in suffix_array:
        if i < n:
            return s[i:] + s[:i]
    
    return s
```

**Why this works**: Suffix array gives us all suffixes in lexicographic order.

## Final Optimal Solution

```python
s = input().strip()

def minimal_rotation_duval(s):
    n = len(s)
    s = s + s
    i = 0
    j = 1
    
    while j < n:
        k = 0
        while k < n and s[i + k] == s[j + k]:
            k += 1
        
        if k == n:
            break
        
        if s[i + k] < s[j + k]:
            j += k + 1
        else:
            i = j
            j = i + 1
    
    return s[i:i + n]

result = minimal_rotation_duval(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|²) | O(|s|²) | Generate all rotations |
| Booth's | O(|s|) | O(|s|) | Use failure function |
| Duval's | O(|s|) | O(|s|) | Simple comparison |
| Suffix Array | O(|s| log |s|) | O(|s|) | Lexicographic ordering |

## Key Insights for Other Problems

### 1. **Minimal Rotation Problems**
**Principle**: Use specialized algorithms like Booth's or Duval's for finding minimal rotations.
**Applicable to**:
- Minimal rotation problems
- String algorithms
- Lexicographic ordering
- Algorithm design

**Example Problems**:
- Minimal rotation problems
- String algorithms
- Lexicographic ordering
- Algorithm design

### 2. **String Doubling Technique**
**Principle**: Double the string to handle rotations more easily.
**Applicable to**:
- String algorithms
- Rotation problems
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Rotation problems
- Algorithm design
- Problem solving

### 3. **Lexicographic Comparison**
**Principle**: Use efficient comparison techniques for lexicographic ordering.
**Applicable to**:
- String algorithms
- Sorting
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Sorting
- Algorithm design
- Problem solving

### 4. **Failure Function Applications**
**Principle**: Use failure functions to optimize string comparisons.
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

### 1. **Duval's Algorithm Pattern**
```python
def minimal_rotation_duval(s):
    n = len(s)
    s = s + s
    i = 0
    j = 1
    
    while j < n:
        k = 0
        while k < n and s[i + k] == s[j + k]:
            k += 1
        
        if k == n:
            break
        
        if s[i + k] < s[j + k]:
            j += k + 1
        else:
            i = j
            j = i + 1
    
    return s[i:i + n]
```

### 2. **Booth's Algorithm Pattern**
```python
def minimal_rotation_booth(s):
    n = len(s)
    s = s + s
    f = [0] * (2 * n)
    
    k = 0
    for j in range(1, 2 * n):
        i = f[j - k - 1]
        while i > 0 and s[j] != s[k + i]:
            if s[j] < s[k + i]:
                k = j - i
            i = f[i - 1]
        
        if s[j] == s[k + i]:
            i += 1
        else:
            if s[j] < s[k]:
                k = j
            i = 0
        
        f[j - k] = i
    
    return s[k:k + n]
```

### 3. **Suffix Array Pattern**
```python
def minimal_rotation_suffix_array(s):
    n = len(s)
    s = s + s
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    
    for _, i in suffixes:
        if i < n:
            return s[i:i + n]
    
    return s
```

## Edge Cases to Remember

1. **Single character**: Return the character itself
2. **All same characters**: Any rotation is minimal
3. **Already minimal**: Return the original string
4. **Empty string**: Handle appropriately
5. **Repeated patterns**: Handle efficiently

## Problem-Solving Framework

1. **Identify rotation nature**: This is a minimal rotation problem
2. **Choose algorithm**: Use Duval's algorithm for efficiency
3. **Double string**: Concatenate string with itself
4. **Find minimal**: Use comparison-based approach
5. **Return result**: Return the minimal rotation

---

*This analysis shows how to efficiently find the lexicographically smallest rotation using specialized algorithms.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Minimal Rotation with Constraints**
**Problem**: Find minimal rotation with additional constraints (length, alphabet, etc.).
```python
def constrained_minimal_rotation(s, constraints):
    # constraints = {'min_length': x, 'max_length': y, 'alphabet': chars}
    
    n = len(s)
    
    # Apply constraints
    if 'min_length' in constraints and n < constraints['min_length']:
        return None
    
    if 'max_length' in constraints and n > constraints['max_length']:
        return None
    
    if 'alphabet' in constraints:
        if not all(c in constraints['alphabet'] for c in s):
            return None
    
    # Use Duval's algorithm
    s = s + s
    i = 0
    j = 1
    
    while j < n:
        k = 0
        while k < n and s[i + k] == s[j + k]:
            k += 1
        
        if k == n:
            break
        
        if s[i + k] < s[j + k]:
            j += k + 1
        else:
            i = j
            j = i + 1
    
    return s[i:i + n]
```

#### **Variation 2: Minimal Rotation with Multiple Criteria**
**Problem**: Find rotation that optimizes multiple criteria simultaneously.
```python
def multi_criteria_minimal_rotation(s, criteria):
    # criteria = {'lexicographic': weight1, 'palindrome': weight2, 'periodicity': weight3}
    
    n = len(s)
    rotations = []
    
    # Generate all rotations
    for i in range(n):
        rotation = s[i:] + s[:i]
        score = 0
        
        # Lexicographic score (lower is better)
        if 'lexicographic' in criteria:
            lex_score = sum(ord(c) for c in rotation)
            score += criteria['lexicographic'] * lex_score
        
        # Palindrome score
        if 'palindrome' in criteria:
            if rotation == rotation[::-1]:
                score += criteria['palindrome']
        
        # Periodicity score
        if 'periodicity' in criteria:
            period = find_period(rotation)
            if period < n:
                score += criteria['periodicity'] * (n / period)
        
        rotations.append((rotation, score))
    
    # Return rotation with minimum score
    return min(rotations, key=lambda x: x[1])[0]

def find_period(s):
    n = len(s)
    for i in range(1, n + 1):
        if n % i == 0 and s[:i] * (n // i) == s:
            return i
    return n
```

#### **Variation 3: Minimal Rotation with Probabilities**
**Problem**: Find expected minimal rotation with probabilistic character distributions.
```python
def probabilistic_minimal_rotation(s, char_probs):
    # char_probs[c] = probability of character c
    
    n = len(s)
    # For probabilistic strings, calculate expected minimal rotation
    expected_rotation = ""
    
    # Calculate expected character at each position
    for i in range(n):
        expected_char = min(char_probs.keys(), key=lambda c: ord(c))
        expected_rotation += expected_char
    
    # Find minimal rotation of expected string
    return minimal_rotation_duval(expected_rotation)
```

#### **Variation 4: Minimal Rotation with Updates**
**Problem**: Handle dynamic updates to the string and find new minimal rotation.
```python
def dynamic_minimal_rotation(s, updates):
    # updates = [(pos, new_char), ...]
    
    s = list(s)  # Convert to list for updates
    rotation_history = []
    
    for pos, new_char in updates:
        s[pos] = new_char
        # Find minimal rotation after each update
        rotation = minimal_rotation_duval(''.join(s))
        rotation_history.append(rotation)
    
    return rotation_history
```

#### **Variation 5: Minimal Rotation with Multiple Strings**
**Problem**: Find minimal rotation among multiple strings.
```python
def multiple_string_minimal_rotation(strings):
    # Find minimal rotation for each string
    minimal_rotations = []
    
    for s in strings:
        rotation = minimal_rotation_duval(s)
        minimal_rotations.append(rotation)
    
    # Find lexicographically smallest among all minimal rotations
    return min(minimal_rotations)
```

### 🔗 **Related Problems & Concepts**

#### **1. String Rotation Problems**
- **Cyclic Shifts**: Shift characters cyclically
- **String Permutations**: Generate all permutations
- **String Anagrams**: Find anagrams of strings
- **Circular Strings**: Handle circular string properties

#### **2. Lexicographic Ordering**
- **String Comparison**: Compare strings lexicographically
- **String Sorting**: Sort strings in lexicographic order
- **Minimal Elements**: Find minimal elements in sets
- **Order Statistics**: Find k-th smallest element

#### **3. String Algorithms**
- **Duval's Algorithm**: Find minimal rotation efficiently
- **Booth's Algorithm**: Alternative minimal rotation algorithm
- **Suffix Arrays**: Sort all suffixes
- **Suffix Trees**: Tree representation of suffixes

#### **4. Optimization Problems**
- **Minimization**: Find minimum value solutions
- **Multi-objective Optimization**: Optimize multiple criteria
- **Constrained Optimization**: Optimization with constraints
- **Dynamic Optimization**: Optimization with changing data

#### **5. Algorithmic Techniques**
- **Two Pointers**: Use two pointers for efficiency
- **Sliding Window**: Process data in windows
- **String Concatenation**: Double strings for easier processing
- **Comparison-based Algorithms**: Use comparisons for ordering

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    rotation = minimal_rotation_duval(s)
    print(rotation)
```

#### **2. Range Queries on Minimal Rotations**
```python
def range_minimal_rotation_queries(s, queries):
    # queries = [(l, r), ...] - find minimal rotation of substring s[l:r]
    
    results = []
    for l, r in queries:
        substring = s[l:r]
        rotation = minimal_rotation_duval(substring)
        results.append(rotation)
    
    return results
```

#### **3. Interactive Minimal Rotation Problems**
```python
def interactive_minimal_rotation():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        rotation = minimal_rotation_duval(s)
        print(f"Original: {s}")
        print(f"Minimal rotation: {rotation}")
        
        # Show all rotations
        n = len(s)
        all_rotations = [s[i:] + s[:i] for i in range(n)]
        print(f"All rotations: {all_rotations}")
```

### 🧮 **Mathematical Extensions**

#### **1. Group Theory**
- **Cyclic Groups**: Study of cyclic structures
- **Permutation Groups**: Groups of permutations
- **Symmetry Groups**: Groups of symmetries
- **Group Actions**: Actions of groups on sets

#### **2. Combinatorics**
- **String Enumeration**: Count strings with certain properties
- **Permutation Enumeration**: Count permutations
- **Circular Permutations**: Permutations in circular arrangements
- **Lexicographic Ordering**: Ordering of combinatorial objects

#### **3. String Theory**
- **String Properties**: Periodicity, borders, periods
- **String Functions**: Mathematical functions on strings
- **String Complexity**: Complexity measures for strings
- **String Transformations**: Mathematical transformations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **String Algorithms**: KMP, Boyer-Moore, Rabin-Karp
- **Suffix Structures**: Suffix arrays, suffix trees, suffix automata
- **Sorting Algorithms**: Comparison-based and linear sorting
- **Search Algorithms**: Binary search, linear search

#### **2. Mathematical Concepts**
- **Combinatorics**: Counting, permutations, combinations
- **Group Theory**: Groups, subgroups, group actions
- **Order Theory**: Partial orders, total orders, lattices
- **Number Theory**: Properties of integers and sequences

#### **3. Programming Concepts**
- **String Manipulation**: Efficient string operations
- **Algorithm Design**: Systematic approach to problem solving
- **Complexity Analysis**: Time and space complexity
- **Optimization Techniques**: Improving algorithm performance

---

*This analysis demonstrates efficient minimal rotation techniques and shows various extensions for string manipulation problems.* 