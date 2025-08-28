---
layout: simple
title: "Longest Palindrome
permalink: /problem_soulutions/string_algorithms/longest_palindrome_analysis/
---

# Longest Palindrome

## Problem Statement
Given a string, find the longest palindromic substring.

### Input
The first input line has a string s.

### Output
Print the longest palindromic substring.

### Constraints
- 1 ≤ |s| ≤ 10^6

### Example
```
Input:
babad

Output:
bab
```

## Solution Progression

### Approach 1: Check All Substrings - O(|s|³)
**Description**: Check all possible substrings to find the longest palindrome.

```python
def longest_palindrome_naive(s):
    n = len(s)
    max_length = 1
    start = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            substring = s[i:j + 1]
            if substring == substring[::-1]:
                if j - i + 1 > max_length:
                    max_length = j - i + 1
                    start = i
    
    return s[start:start + max_length]
```

**Why this is inefficient**: Cubic time complexity for large strings.

### Improvement 1: Expand Around Center - O(|s|²)
**Description**: For each position, expand around it to find palindromes.

```python
def longest_palindrome_expand(s):
    n = len(s)
    max_length = 1
    start = 0
    
    def expand_around_center(left, right):
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(n):
        # Check odd length palindromes
        len1 = expand_around_center(i, i)
        if len1 > max_length:
            max_length = len1
            start = i - len1 // 2
        
        # Check even length palindromes
        len2 = expand_around_center(i, i + 1)
        if len2 > max_length:
            max_length = len2
            start = i - len2 // 2 + 1
    
    return s[start:start + max_length]
```

**Why this improvement works**: Expand around center reduces time complexity to quadratic."
### Improvement 2: Manacher's Algorithm - O(|s|)
**Description**: Use Manacher's algorithm to find the longest palindrome in linear time.

```python
def longest_palindrome_manacher(s):
    # Transform string to handle even length palindromes
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    
    center = right = 0
    
    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        # Expand around current center
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        # Update center and right boundary
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find the longest palindrome
    max_length = max(p)
    center_index = p.index(max_length)
    
    # Convert back to original string indices
    start = (center_index - max_length) // 2
    end = (center_index + max_length) // 2
    
    return s[start:end]
```

**Why this improvement works**: Manacher's algorithm uses palindrome properties to achieve linear time.

### Alternative: Dynamic Programming - O(|s|²)
**Description**: Use dynamic programming to find the longest palindrome.

```python
def longest_palindrome_dp(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    
    # All single characters are palindromes
    for i in range(n):
        dp[i][i] = True
    
    max_length = 1
    start = 0
    
    # Check for length 2 palindromes
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            max_length = 2
            start = i
    
    # Check for length > 2 palindromes
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_length:
                    max_length = length
                    start = i
    
    return s[start:start + max_length]
```

**Why this works**: Dynamic programming builds solutions from smaller subproblems.

## Final Optimal Solution

```python
s = input().strip()

def longest_palindrome_manacher(s):
    # Transform string to handle even length palindromes
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    
    center = right = 0
    
    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        # Expand around current center
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        # Update center and right boundary
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find the longest palindrome
    max_length = max(p)
    center_index = p.index(max_length)
    
    # Convert back to original string indices
    start = (center_index - max_length) // 2
    end = (center_index + max_length) // 2
    
    return s[start:end]

result = longest_palindrome_manacher(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|³) | O(|s|) | Check all substrings |
| Expand Around Center | O(|s|²) | O(1) | Expand from each position |
| Manacher's | O(|s|) | O(|s|) | Use palindrome properties |
| Dynamic Programming | O(|s|²) | O(|s|²) | Build from subproblems |

## Key Insights for Other Problems

### 1. **Palindrome Problems**
**Principle**: Use specialized algorithms like Manacher's for efficient palindrome detection.
**Applicable to**:
- Palindrome problems
- String algorithms
- Pattern matching
- Algorithm design

**Example Problems**:
- Palindrome problems
- String algorithms
- Pattern matching
- Algorithm design

### 2. **String Transformation**
**Principle**: Transform strings to handle edge cases more easily.
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

### 3. **Palindrome Properties**
**Principle**: Use palindrome properties to optimize algorithms.
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

### 4. **Dynamic Programming on Strings**
**Principle**: Use DP to build solutions from smaller subproblems.
**Applicable to**:
- String algorithms
- Dynamic programming
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Dynamic programming
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **Manacher's Algorithm Pattern**
```python
def manacher_palindrome(s):
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    
    center = right = 0
    
    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    return p
```

### 2. **Expand Around Center Pattern**
```python
def expand_around_center(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    max_length = 1
    start = 0
    
    for i in range(len(s)):
        len1 = expand(i, i)
        len2 = expand(i, i + 1)
        
        if len1 > max_length:
            max_length = len1
            start = i - len1 // 2
        
        if len2 > max_length:
            max_length = len2
            start = i - len2 // 2 + 1
    
    return s[start:start + max_length]
```

### 3. **DP Palindrome Pattern**
```python
def dp_palindrome(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    
    for i in range(n):
        dp[i][i] = True
    
    max_length = 1
    start = 0
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j] and (length == 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                if length > max_length:
                    max_length = length
                    start = i
    
    return s[start:start + max_length]
```

## Edge Cases to Remember

1. **Single character**: Return the character itself
2. **All same characters**: Return the entire string
3. **No palindromes**: Return the first character
4. **Empty string**: Handle appropriately
5. **Multiple palindromes**: Return the longest one

## Problem-Solving Framework

1. **Identify palindrome nature**: This is a longest palindrome problem
2. **Choose algorithm**: Use Manacher's algorithm for efficiency
3. **Transform string**: Add separators to handle even length palindromes
4. **Find palindromes**: Use palindrome properties to expand efficiently
5. **Return result**: Return the longest palindromic substring

---

*This analysis shows how to efficiently find the longest palindromic substring using Manacher's algorithm and other techniques.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Longest Palindrome with Constraints**
**Problem**: Find longest palindrome with additional constraints (length, alphabet, etc.).
```python
def constrained_longest_palindrome(s, constraints):
    # constraints = {'min_length': x, 'max_length': y, 'alphabet': chars}
    
    n = len(s)
    
    # Apply constraints
    if 'alphabet' in constraints:
        if not all(c in constraints['alphabet'] for c in s):
            return ""
    
    if 'min_length' in constraints and n < constraints['min_length']:
        return ""
    
    if 'max_length' in constraints:
        n = min(n, constraints['max_length'])
    
    # Use Manacher's algorithm
    t = '#' + '#'.join(s[:n]) + '#'
    n_t = len(t)
    p = [0] * n_t
    
    center = right = 0
    
    for i in range(n_t):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n_t and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find longest palindrome within constraints
    max_length = 0
    start = 0
    
    for i in range(n_t):
        length = p[i]
        if 'min_length' in constraints:
            length = max(length, constraints['min_length'])
        if length > max_length:
            max_length = length
            start = (i - p[i]) // 2
    
    return s[start:start + max_length] if max_length > 0 else ""
```

#### **Variation 2: Longest Palindrome with Costs**
**Problem**: Each character has a cost, find longest palindrome with minimum cost.
```python
def cost_based_longest_palindrome(s, char_costs):
    # char_costs[c] = cost of character c
    
    n = len(s)
    t = '#' + '#'.join(s) + '#'
    n_t = len(t)
    p = [0] * n_t
    
    center = right = 0
    
    for i in range(n_t):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n_t and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find palindrome with minimum cost
    max_length = 0
    min_cost = float('inf')
    best_palindrome = ""
    
    for i in range(n_t):
        length = p[i]
        start = (i - p[i]) // 2
        palindrome = s[start:start + length]
        cost = sum(char_costs.get(c, 1) for c in palindrome)
        
        if length > max_length or (length == max_length and cost < min_cost):
            max_length = length
            min_cost = cost
            best_palindrome = palindrome
    
    return best_palindrome
```

#### **Variation 3: Longest Palindrome with Probabilities**
**Problem**: Characters have probabilities, find expected longest palindrome.
```python
def probabilistic_longest_palindrome(s, char_probs):
    # char_probs[c] = probability of character c
    
    n = len(s)
    # For probabilistic strings, calculate expected longest palindrome
    expected_length = 0
    
    # Calculate expected length based on character probabilities
    for length in range(1, n + 1):
        for start in range(n - length + 1):
            prob_palindrome = 1.0
            for i in range(length // 2):
                if start + i < n and start + length - 1 - i < n:
                    if s[start + i] == s[start + length - 1 - i]:
                        prob_palindrome *= char_probs.get(s[start + i], 0.1)
                    else:
                        prob_palindrome = 0
                        break
            
            if prob_palindrome >= 0.5:  # Threshold for "palindrome"
                expected_length = max(expected_length, length)
    
    return s[:expected_length] if expected_length > 0 else ""
```

#### **Variation 4: Longest Palindrome with Updates**
**Problem**: Handle dynamic updates to the string and find new longest palindrome.
```python
def dynamic_longest_palindrome(s, updates):
    # updates = [(pos, new_char), ...]
    
    s = list(s)  # Convert to list for updates
    palindrome_history = []
    
    for pos, new_char in updates:
        s[pos] = new_char
        # Find longest palindrome after each update
        palindrome = expand_around_center(''.join(s))
        palindrome_history.append(palindrome)
    
    return palindrome_history
```

#### **Variation 5: Longest Palindrome with Multiple Strings**
**Problem**: Find longest palindrome among multiple strings.
```python
def multiple_string_longest_palindrome(strings):
    # Find longest palindrome among all strings
    
    longest_palindrome = ""
    
    for s in strings:
        palindrome = expand_around_center(s)
        if len(palindrome) > len(longest_palindrome):
            longest_palindrome = palindrome
    
    return longest_palindrome
```

### 🔗 **Related Problems & Concepts**

#### **1. Palindrome Problems**
- **Palindrome Checking**: Check if string is palindrome
- **Palindrome Counting**: Count palindromic substrings
- **Palindrome Partitioning**: Partition string into palindromes
- **Palindrome Construction**: Construct palindromes

#### **2. String Analysis Problems**
- **Symmetry Analysis**: Analyze symmetric properties
- **Mirror Properties**: Study mirror-like properties
- **Center Analysis**: Analyze center-based properties
- **Border Analysis**: Find borders and periods

#### **3. String Algorithms**
- **Manacher's Algorithm**: Efficient palindrome finding
- **Expand Around Center**: Simple palindrome algorithm
- **Dynamic Programming**: DP approach to palindromes
- **Suffix Structures**: Suffix arrays, suffix trees

#### **4. Optimization Problems**
- **Maximization**: Find maximum value solutions
- **Cost Optimization**: Optimize with respect to costs
- **Constrained Optimization**: Optimization with constraints
- **Multi-objective Optimization**: Optimize multiple criteria

#### **5. Algorithmic Techniques**
- **Two Pointers**: Use two pointers for efficiency
- **Sliding Window**: Process data in windows
- **String Transformation**: Transform strings for easier processing
- **Center Expansion**: Expand around centers

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    palindrome = expand_around_center(s)
    print(len(palindrome))
    print(palindrome)
```

#### **2. Range Queries on Longest Palindromes**
```python
def range_longest_palindrome_queries(s, queries):
    # queries = [(l, r), ...] - find longest palindrome in s[l:r]
    
    results = []
    for l, r in queries:
        substring = s[l:r]
        palindrome = expand_around_center(substring)
        results.append(palindrome)
    
    return results
```

#### **3. Interactive Longest Palindrome Problems**
```python
def interactive_longest_palindrome():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        palindrome = expand_around_center(s)
        print(f"String: {s}")
        print(f"Longest palindrome: {palindrome}")
        print(f"Length: {len(palindrome)}")
```

### 🧮 **Mathematical Extensions**

#### **1. Symmetry Theory**
- **Symmetry Groups**: Study of symmetric structures
- **Reflection Symmetry**: Mirror-like symmetry
- **Rotational Symmetry**: Rotation-based symmetry
- **Translational Symmetry**: Translation-based symmetry

#### **2. Combinatorial Analysis**
- **Palindrome Enumeration**: Count palindromes with properties
- **Symmetry Enumeration**: Count symmetric structures
- **Pattern Enumeration**: Count patterns in palindromes
- **Combinatorial Counting**: Count combinations and permutations

#### **3. String Theory**
- **String Properties**: Periodicity, borders, periods
- **String Functions**: Mathematical functions on strings
- **String Complexity**: Complexity measures for strings
- **String Transformations**: Mathematical transformations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **String Matching**: KMP, Boyer-Moore, Rabin-Karp algorithms
- **Suffix Structures**: Suffix arrays, suffix trees, suffix automata
- **String Compression**: LZ77, LZ78, Huffman coding
- **String Parsing**: Regular expressions, context-free parsing

#### **2. Mathematical Concepts**
- **Combinatorics**: String combinatorics and counting
- **Group Theory**: Symmetry groups and transformations
- **Number Theory**: Properties of integers and sequences
- **Geometry**: Geometric properties of strings

#### **3. Programming Concepts**
- **String Manipulation**: Efficient string operations
- **Algorithm Design**: Systematic approach to problem solving
- **Complexity Analysis**: Time and space complexity
- **Optimization Techniques**: Improving algorithm performance

---

*This analysis demonstrates efficient longest palindrome finding techniques and shows various extensions for palindrome problems.* 