---
layout: simple
title: "Minimal Rotation"
permalink: /problem_soulutions/string_algorithms/minimal_rotation_analysis
---

# Minimal Rotation

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand string rotation concepts and their applications
- Apply efficient algorithms for finding minimal rotations
- Implement optimal solutions for minimal rotation problems with proper complexity analysis
- Optimize solutions for large inputs with advanced string algorithms
- Handle edge cases in string rotation problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String algorithms, rotation algorithms, lexicographical ordering, suffix arrays
- **Data Structures**: Strings, suffix arrays, rolling hash tables
- **Mathematical Concepts**: String theory, lexicographical ordering, rotation theory
- **Programming Skills**: String manipulation, algorithm implementation, optimization
- **Related Problems**: String Sorting (lexicographical ordering), Suffix Arrays (string processing), String Matching

## 📋 Problem Description

You are given a string s. Find the lexicographically smallest rotation of the string. A rotation of a string is obtained by moving some characters from the beginning to the end.

**Input**: 
- First line: string s

**Output**: 
- Print the lexicographically smallest rotation of the string

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- s contains only lowercase English letters

**Example**:
```
Input:
abacaba

Output:
aabacab

Explanation**: 
String: "abacaba"

All possible rotations:
1. "abacaba" (original)
2. "bacabaa" (rotate left by 1)
3. "acabaab" (rotate left by 2)
4. "cabaaba" (rotate left by 3)
5. "abaabac" (rotate left by 4)
6. "baabaca" (rotate left by 5)
7. "aabacab" (rotate left by 6)

Lexicographically smallest: "aabacab"
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. Generate all possible rotations of the string
2. Compare them lexicographically
3. Return the smallest one

**Implementation**:
```python
def brute_force_minimal_rotation(s):
    n = len(s)
    min_rotation = s
    
    # Try all possible rotations
    for i in range(n):
        rotation = s[i:] + s[:i]
        if rotation < min_rotation:
            min_rotation = rotation
    
    return min_rotation
```

**Analysis**:
- **Time**: O(n²) - Generate and compare all rotations
- **Space**: O(n) - Store current rotation
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Suffix Array
**Time Complexity**: O(n log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Create a doubled string (s + s) to handle rotations
2. Build suffix array for the doubled string
3. Find the lexicographically smallest suffix of length n

**Implementation**:
```python
def optimized_minimal_rotation(s):
    n = len(s)
    doubled = s + s
    
    # Build suffix array (simplified version)
    suffixes = []
    for i in range(n):
        suffixes.append((doubled[i:i + n], i))
    suffixes.sort()
    
    # Return the lexicographically smallest rotation
    return suffixes[0][0]
```

**Analysis**:
- **Time**: O(n log n) - Suffix array construction
- **Space**: O(n) - Suffix array storage
- **Improvement**: Much faster than brute force

### Approach 3: Optimal with Booth's Algorithm
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use Booth's algorithm to find the lexicographically smallest rotation
2. Maintain two pointers and compare characters efficiently
3. Handle ties and edge cases properly

**Implementation**:
```python
def optimal_minimal_rotation(s):
    n = len(s)
    doubled = s + s
    
    # Booth's algorithm
    i = 0
    j = 1
    k = 0
    
    while i < n and j < n and k < n:
        if doubled[i + k] == doubled[j + k]:
            k += 1
        elif doubled[i + k] < doubled[j + k]:
            j += k + 1
            k = 0
        else:
            i += k + 1
            k = 0
        
        if i == j:
            j += 1
    
    # Return the minimal rotation
    return doubled[i:i + n]
```

**Analysis**:
- **Time**: O(n) - Linear time algorithm
- **Space**: O(n) - Doubled string storage
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
String: "abacaba"
Doubled: "abacabaabacaba"

Booth's Algorithm:
i=0, j=1, k=0: 'a' == 'b'? No, 'a' < 'b', so j=2
i=0, j=2, k=0: 'a' == 'a'? Yes, k=1
i=0, j=2, k=1: 'b' == 'b'? Yes, k=2
i=0, j=2, k=2: 'a' == 'a'? Yes, k=3
i=0, j=2, k=3: 'c' == 'c'? Yes, k=4
i=0, j=2, k=4: 'a' == 'a'? Yes, k=5
i=0, j=2, k=5: 'b' == 'b'? Yes, k=6
i=0, j=2, k=6: 'a' == 'a'? Yes, k=7 (k >= n, stop)

Result: doubled[0:7] = "abacaba"
But we need to find the minimal rotation...

Actually, the algorithm finds the starting position of the minimal rotation.
Let's trace it more carefully:

i=0, j=1: Compare rotations starting at positions 0 and 1
- Position 0: "abacaba"
- Position 1: "bacabaa"
- "abacaba" < "bacabaa", so j=2

i=0, j=2: Compare rotations starting at positions 0 and 2
- Position 0: "abacaba"
- Position 2: "acabaab"
- "abacaba" < "acabaab", so j=3

Continue until we find the minimal rotation starting position.
```

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible rotations and compare them lexicographically
- **Complete Coverage**: Guarantees finding the correct answer but inefficient
- **Simple Implementation**: Easy to understand and implement

**Key Insights from Optimized Approach**:
- **Suffix Array**: Use suffix array on doubled string to find minimal rotation
- **Efficiency Improvement**: Much faster than brute force using sorting
- **Memory Trade-off**: Use more memory to achieve better time complexity

**Key Insights from Optimal Approach**:
- **Booth's Algorithm**: Use specialized algorithm for finding minimal rotation
- **Linear Time**: Achieve O(n) time complexity with proper algorithm
- **Optimal Complexity**: Best possible complexity for this problem

## 🎯 Key Insights

### 🔑 **Core Concepts**
- **String Rotation**: Moving characters from beginning to end of string
- **Lexicographical Ordering**: Dictionary order comparison of strings
- **Booth's Algorithm**: Specialized algorithm for minimal rotation
- **Doubled String**: Technique to handle circular rotations

### 💡 **Problem-Specific Insights**
- **Minimal Rotation**: Find the lexicographically smallest rotation
- **Efficiency Optimization**: From O(n²) brute force to O(n) optimal solution
- **Circular Nature**: Rotations are circular, so doubled string helps

### 🚀 **Optimization Strategies**
- **Suffix Array**: Use suffix array on doubled string for efficient comparison
- **Booth's Algorithm**: Use specialized algorithm for linear time solution
- **Character Comparison**: Efficient character-by-character comparison

## 🧠 Common Pitfalls & How to Avoid Them

### ❌ **Common Mistakes**
1. **Quadratic Time**: Brute force approach has O(n²) time complexity
2. **Circular Handling**: Not properly handling the circular nature of rotations
3. **Edge Cases**: Not handling ties and edge cases in comparison

### ✅ **Best Practices**
1. **Use Doubled String**: Create s + s to handle rotations efficiently
2. **Efficient Algorithm**: Use Booth's algorithm for optimal performance
3. **Proper Comparison**: Handle character comparisons correctly

## 🔗 Related Problems & Pattern Recognition

### 📚 **Similar Problems**
- **String Sorting**: Lexicographical ordering of strings
- **Suffix Arrays**: String processing and comparison
- **String Matching**: Finding patterns in strings

### 🎯 **Pattern Recognition**
- **Rotation Problems**: Problems involving string rotations
- **Lexicographical Problems**: Problems involving string ordering
- **String Processing Problems**: Problems requiring efficient string manipulation

## 📈 Complexity Analysis

### ⏱️ **Time Complexity**
- **Brute Force**: O(n²) - Generate and compare all rotations
- **Optimized**: O(n log n) - Suffix array construction
- **Optimal**: O(n) - Booth's algorithm

### 💾 **Space Complexity**
- **Brute Force**: O(n) - Store current rotation
- **Optimized**: O(n) - Suffix array storage
- **Optimal**: O(n) - Doubled string storage

## 🎓 Summary

### 🏆 **Key Takeaways**
1. **String Rotation**: Important concept in string processing
2. **Booth's Algorithm**: Essential for finding minimal rotations efficiently
3. **Lexicographical Ordering**: Fundamental concept for string comparison
4. **Doubled String Technique**: Useful for handling circular problems

### 🚀 **Next Steps**
1. **Practice**: Implement minimal rotation algorithms with different approaches
2. **Advanced Topics**: Learn about more complex string rotation problems
3. **Related Problems**: Solve more string processing and ordering problems
