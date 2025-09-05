---
layout: simple
title: "String Rotation"
permalink: /problem_soulutions/string_algorithms/string_rotation_analysis
---


# String Rotation

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand string rotation problems and lexicographic ordering concepts
- [ ] **Objective 2**: Apply Booth's algorithm or rotation comparison to find lexicographically smallest rotation
- [ ] **Objective 3**: Implement efficient string rotation algorithms with O(n) or O(n log n) time complexity
- [ ] **Objective 4**: Optimize string rotation using Booth's algorithm, string doubling, and lexicographic comparison
- [ ] **Objective 5**: Handle edge cases in string rotation (single character, all same characters, already minimal)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Booth's algorithm, string rotation, lexicographic ordering, string comparison, rotation algorithms
- **Data Structures**: String data structures, rotation tracking, comparison tracking, lexicographic tracking
- **Mathematical Concepts**: String rotation theory, lexicographic mathematics, rotation analysis, string comparison
- **Programming Skills**: String manipulation, rotation implementation, lexicographic comparison, algorithm implementation
- **Related Problems**: Minimal Rotation (similar concept), String algorithms, Lexicographic problems

## 📋 Problem Description

Given a string s, find the lexicographically smallest rotation of the string.

This is a string algorithm problem where we need to find the lexicographically smallest rotation of a given string. A rotation is obtained by moving characters from the beginning to the end. We can solve this efficiently using the Booth's algorithm or by comparing all rotations.

**Input**: 
- First line: string s (the input string)

**Output**: 
- Print the lexicographically smallest rotation

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- String contains only lowercase letters

**Example**:
```
Input:
abacaba

Output:
aabacab
```

**Explanation**: 
The rotations of "abacaba" are:
1. "abacaba" (original)
2. "bacabaa" (rotate left by 1)
3. "acabaab" (rotate left by 2)
4. "cabaaba" (rotate left by 3)
5. "abaabac" (rotate left by 4)
6. "baabaca" (rotate left by 5)
7. "aabacab" (rotate left by 6)

The lexicographically smallest is "aabacab".

## 🎯 Visual Example

### Input
```
String: "abacaba"
```

### All Rotations Generation
```
Original: a b a c a b a
Index:    0 1 2 3 4 5 6

Rotation 0: a b a c a b a (original)
Rotation 1: b a c a b a a (left by 1)
Rotation 2: a c a b a a b (left by 2)
Rotation 3: c a b a a b a (left by 3)
Rotation 4: a b a a b a c (left by 4)
Rotation 5: b a a b a c a (left by 5)
Rotation 6: a a b a c a b (left by 6)
```

### Lexicographical Comparison
```
Rotation 0: "abacaba"
Rotation 1: "bacabaa"
Rotation 2: "acabaab"
Rotation 3: "cabaaba"
Rotation 4: "abaabac"
Rotation 5: "baabaca"
Rotation 6: "aabacab" ← Smallest
```

### Booth's Algorithm Visualization
```
String: "abacaba"
Extended: "abacabaabacaba" (for circular comparison)

Step 1: Initialize i=0, j=1, k=0
Step 2: Compare characters at positions i+k and j+k
Step 3: If equal, increment k
Step 4: If different, update i or j based on comparison
Step 5: Continue until k reaches string length

Final result: i=6, giving rotation "aabacab"
```

### Key Insight
String rotation problem can be solved by:
1. Generating all rotations and comparing (O(n²))
2. Using Booth's algorithm for O(n) solution
3. Finding the lexicographically smallest rotation
4. Handling circular string comparisons efficiently

## Solution Progression

### Approach 1: Generate All Rotations - O(|s|²)
**Description**: Generate all possible rotations and find the lexicographically smallest one.

```python
def string_rotation_naive(s):
    n = len(s)
    rotations = []
    
    # Generate all rotations
    for i in range(n):
        rotation = s[i:] + s[:i]
        rotations.append(rotation)
    
    # Find lexicographically smallest
    return min(rotations)
```

**Why this is inefficient**: We need to generate all rotations and compare them, leading to O(|s|²) time complexity.
### Improvement 1: Booth's Algorithm - O(|s|)
**Description**: Use Booth's algorithm to find the lexicographically smallest rotation efficiently.

```python
def string_rotation_booth(s):
    n = len(s)
    s = s + s  # Double the string for easier processing
    
    # Initialize failure function
    failure = [0] * (2 * n)
    
    # Find the lexicographically smallest rotation
    i = 0
    for j in range(1, 2 * n):
        k = failure[j - i - 1]
        while k > 0 and s[j] != s[i + k]:
            if s[j] < s[i + k]:
                i = j - k
            k = failure[k - 1]
        
        if s[j] != s[i + k]:
            if s[j] < s[i]:
                i = j
            failure[j - i] = 0
        else:
            failure[j - i] = k + 1
    
    return s[i:i + n]
```

**Why this improvement works**: Booth's algorithm finds the lexicographically smallest rotation in linear time using failure function.

## Final Optimal Solution

```python
s = input().strip()

def find_lexicographically_smallest_rotation(s):
    n = len(s)
    s = s + s  # Double the string for easier processing
    
    # Initialize failure function
    failure = [0] * (2 * n)
    
    # Find the lexicographically smallest rotation
    i = 0
    for j in range(1, 2 * n):
        k = failure[j - i - 1]
        while k > 0 and s[j] != s[i + k]:
            if s[j] < s[i + k]:
                i = j - k
            k = failure[k - 1]
        
        if s[j] != s[i + k]:
            if s[j] < s[i]:
                i = j
            failure[j - i] = 0
        else:
            failure[j - i] = k + 1
    
    return s[i:i + n]

result = find_lexicographically_smallest_rotation(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|²) | O(|s|²) | Generate all rotations |
| Booth's Algorithm | O(|s|) | O(|s|) | Use failure function for linear time |

## Key Insights for Other Problems

### 1. **String Rotation Problems**
**Principle**: Use Booth's algorithm to find lexicographically smallest rotation.
**Applicable to**: String problems, rotation problems, lexicographic ordering

### 2. **Booth's Algorithm**
**Principle**: Use failure function to find minimal rotation efficiently.
**Applicable to**: String algorithms, rotation problems, minimal string problems

### 3. **Lexicographic Ordering**
**Principle**: Compare strings character by character to find minimal ordering.
**Applicable to**: String comparison, sorting problems, minimal element problems

## Notable Techniques

### 1. **Booth's Algorithm Implementation**
```python
def booth_algorithm(s):
    n = len(s)
    s = s + s
    
    failure = [0] * (2 * n)
    i = 0
    
    for j in range(1, 2 * n):
        k = failure[j - i - 1]
        while k > 0 and s[j] != s[i + k]:
            if s[j] < s[i + k]:
                i = j - k
            k = failure[k - 1]
        
        if s[j] != s[i + k]:
            if s[j] < s[i]:
                i = j
            failure[j - i] = 0
        else:
            failure[j - i] = k + 1
    
    return s[i:i + n]
```

### 2. **Rotation Generation**
```python
def generate_rotations(s):
    n = len(s)
    rotations = []
    
    for i in range(n):
        rotation = s[i:] + s[:i]
        rotations.append(rotation)
    
    return rotations
```

### 3. **Lexicographic Comparison**
```python
def lexicographic_compare(s1, s2):
    n = min(len(s1), len(s2))
    
    for i in range(n):
        if s1[i] < s2[i]:
            return -1
        elif s1[i] > s2[i]:
            return 1
    
    if len(s1) < len(s2):
        return -1
    elif len(s1) > len(s2):
        return 1
    else:
        return 0
```

## Problem-Solving Framework

1. **Identify problem type**: This is a string rotation problem
2. **Choose approach**: Use Booth's algorithm for efficient solution
3. **Double the string**: Create s + s for easier processing
4. **Apply Booth's algorithm**: Find minimal rotation using failure function
5. **Return result**: Output the lexicographically smallest rotation

---

*This analysis shows how to efficiently find the lexicographically smallest rotation using Booth's algorithm.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: String Rotation with Constraints**
**Problem**: Find lexicographically smallest rotation with additional constraints.
```python
def constrained_string_rotation(s, constraints):
    # constraints = {'min_length': x, 'max_length': y, 'alphabet': chars}
    
    n = len(s)
    s = s + s
    
    # Apply constraints
    if 'min_length' in constraints and n < constraints['min_length']:
        return None
    
    if 'max_length' in constraints and n > constraints['max_length']:
        return None
    
    if 'alphabet' in constraints:
        if not all(c in constraints['alphabet'] for c in s[:n]):
            return None
    
    # Use Booth's algorithm
    failure = [0] * (2 * n)
    i = 0
    
    for j in range(1, 2 * n):
        k = failure[j - i - 1]
        while k > 0 and s[j] != s[i + k]:
            if s[j] < s[i + k]:
                i = j - k
            k = failure[k - 1]
        
        if s[j] != s[i + k]:
            if s[j] < s[i]:
                i = j
            failure[j - i] = 0
        else:
            failure[j - i] = k + 1
    
    return s[i:i + n]
```

#### **Variation 2: String Rotation with Multiple Criteria**
**Problem**: Find rotation that optimizes multiple criteria (lexicographic, length, etc.).
```python
def multi_criteria_rotation(s, criteria):
    # criteria = {'lexicographic': weight1, 'length': weight2, 'palindrome': weight3}
    
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
        
        # Length score (shorter is better)
        if 'length' in criteria:
            score += criteria['length'] * len(rotation)
        
        # Palindrome score
        if 'palindrome' in criteria:
            if rotation == rotation[::-1]:
                score += criteria['palindrome']
        
        rotations.append((rotation, score))
    
    # Return rotation with minimum score
    return min(rotations, key=lambda x: x[1])[0]
```

#### **Variation 3: String Rotation with Probabilities**
**Problem**: Find expected lexicographically smallest rotation with probabilistic characters.
```python
def probabilistic_string_rotation(s, char_probs):
    # char_probs[c] = probability of character c
    
    n = len(s)
    # For probabilistic strings, we calculate expected minimal rotation
    expected_rotation = ""
    
    # Calculate expected character at each position
    for i in range(n):
        expected_char = min(char_probs.keys(), key=lambda c: ord(c))
        expected_rotation += expected_char
    
    # Find rotation of expected string
    return booth_algorithm(expected_rotation)
```

#### **Variation 4: String Rotation with Updates**
**Problem**: Handle dynamic updates to the string and find new minimal rotation.
```python
def dynamic_string_rotation(s, updates):
    # updates = [(pos, new_char), ...]
    
    s = list(s)  # Convert to list for updates
    rotation_history = []
    
    for pos, new_char in updates:
        s[pos] = new_char
        # Find minimal rotation after each update
        rotation = booth_algorithm(''.join(s))
        rotation_history.append(rotation)
    
    return rotation_history
```

#### **Variation 5: String Rotation with Multiple Strings**
**Problem**: Find lexicographically smallest rotation among multiple strings.
```python
def multiple_string_rotation(strings):
    # Find minimal rotation for each string
    minimal_rotations = []
    
    for s in strings:
        rotation = booth_algorithm(s)
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
- **Booth's Algorithm**: Find minimal rotation efficiently
- **KMP Algorithm**: Pattern matching in strings
- **Suffix Arrays**: Sort all suffixes
- **Suffix Trees**: Tree representation of suffixes

#### **4. Optimization Problems**
- **Minimization**: Find minimum value solutions
- **Multi-objective Optimization**: Optimize multiple criteria
- **Constrained Optimization**: Optimization with constraints
- **Dynamic Optimization**: Optimization with changing data

#### **5. Algorithmic Techniques**
- **Failure Functions**: KMP failure function applications
- **Sliding Window**: Process data in windows
- **Two Pointers**: Use two pointers for efficiency
- **Binary Search**: Search in sorted data

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    rotation = booth_algorithm(s)
    print(rotation)
```

#### **2. Range Queries on String Rotations**
```python
def range_string_rotation_queries(s, queries):
    # queries = [(l, r), ...] - find minimal rotation of substring s[l:r]
    
    results = []
    for l, r in queries: substring = s[
l: r]
        rotation = booth_algorithm(substring)
        results.append(rotation)
    
    return results
```

#### **3. Interactive String Rotation Problems**
```python
def interactive_string_rotation():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        rotation = booth_algorithm(s)
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

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(|s|) for Booth's algorithm, O(|s|²) for naive approach
- **Space Complexity**: O(|s|) for storing the string
- **Why it works**: Booth's algorithm efficiently finds the lexicographically smallest rotation by comparing rotations in linear time

### Key Implementation Points
- Use Booth's algorithm for optimal O(|s|) time complexity
- Compare rotations efficiently without generating all of them
- Handle edge cases like single character strings
- Use string concatenation to simulate rotations

## 🎯 Key Insights

### Important Concepts and Patterns
- **Booth's Algorithm**: Efficient algorithm for finding lexicographically smallest rotation
- **String Rotation**: Moving characters from beginning to end
- **Lexicographic Order**: Dictionary order comparison of strings
- **String Comparison**: Efficient comparison of rotated strings

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. String Rotation with K-th Smallest**
```python
def kth_smallest_rotation(s, k):
    # Find the k-th lexicographically smallest rotation
    n = len(s)
    rotations = []
    
    # Generate all rotations
    for i in range(n):
        rotation = s[i:] + s[:i]
        rotations.append((rotation, i))
    
    # Sort by rotation string
    rotations.sort(key=lambda x: x[0])
    
    # Return k-th smallest (1-indexed)
    if k <= len(rotations):
        return rotations[k-1][0]
    else:
        return None

# Example usage
s = "abacaba"
k = 3
result = kth_smallest_rotation(s, k)
print(f"K-th smallest rotation: {result}")
```

#### **2. String Rotation with Maximum Lexicographic**
```python
def maximum_lexicographic_rotation(s):
    # Find the lexicographically largest rotation
    n = len(s)
    max_rotation = s
    max_index = 0
    
    for i in range(1, n):
        rotation = s[i:] + s[:i]
        if rotation > max_rotation:
            max_rotation = rotation
            max_index = i
    
    return max_rotation, max_index

# Example usage
s = "abacaba"
result, index = maximum_lexicographic_rotation(s)
print(f"Maximum rotation: {result} at index {index}")
```

#### **3. String Rotation with Period Detection**
```python
def rotation_period_detection(s):
    # Find the period of the string (smallest rotation that gives original string)
    n = len(s)
    
    for i in range(1, n):
        if n % i == 0:  # Only check divisors of n
            is_period = True
            for j in range(i, n):
                if s[j] != s[j % i]:
                    is_period = False
                    break
            if is_period:
                return i
    
    return n  # No period found, period is the full string

# Example usage
s = "ababab"
period = rotation_period_detection(s)
print(f"Period: {period}")
```

#### **4. String Rotation with Circular Matching**
```python
def circular_string_matching(s, pattern):
    # Check if pattern appears in any rotation of s
    n = len(s)
    m = len(pattern)
    
    # Create doubled string to handle rotations
    doubled_s = s + s
    
    # Check if pattern appears in doubled string
    for i in range(n):
        if doubled_s[i:i+m] == pattern:
            return True
    
    return False

# Example usage
s = "abacaba"
pattern = "caba"
result = circular_string_matching(s, pattern)
print(f"Pattern found in rotation: {result}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **String Algorithms**: String matching, Pattern matching
- **Lexicographic Order**: String sorting, String comparison
- **String Rotation**: Circular strings, String transformations
- **Period Detection**: String periods, Repetitive patterns

## 📚 Learning Points

### Key Takeaways
- **Booth's algorithm** is the most efficient way to find lexicographically smallest rotation
- **String rotation** is a fundamental string transformation operation
- **Lexicographic order** is essential for string comparison and sorting
- **String periods** can be detected using rotation analysis

---

*This analysis demonstrates efficient string rotation techniques and shows various extensions for string manipulation problems.* 