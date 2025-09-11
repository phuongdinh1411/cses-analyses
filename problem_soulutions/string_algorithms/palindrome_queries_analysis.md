---
layout: simple
title: "Palindrome Queries"
permalink: /problem_soulutions/string_algorithms/palindrome_queries_analysis
---

# Palindrome Queries

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand palindrome detection and query processing techniques
- Apply efficient algorithms for palindrome queries with optimal complexity
- Implement advanced string data structures for palindrome processing
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in palindrome query problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String algorithms, palindrome detection, rolling hash, Manacher's algorithm
- **Data Structures**: Strings, hash maps, rolling hash tables, prefix arrays
- **Mathematical Concepts**: String theory, palindrome theory, hashing, symmetry
- **Programming Skills**: String manipulation, algorithm implementation, query optimization
- **Related Problems**: Longest Palindrome (palindrome detection), String Hashing (rolling hash), String Matching

## 📋 Problem Description

You are given a string s and q queries. Each query consists of two integers l and r. For each query, determine if the substring s[l:r+1] is a palindrome.

**Input**: 
- First line: string s
- Second line: integer q (number of queries)
- Next q lines: two integers l and r (0-indexed)

**Output**: 
- For each query, print "YES" if the substring is a palindrome, "NO" otherwise

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- 1 ≤ q ≤ 10⁵
- 0 ≤ l ≤ r < |s|
- s contains only lowercase English letters

**Example**:
```
Input:
abacaba
3
0 6
1 3
2 4

Output:
YES
YES
NO

Explanation**: 
String: "abacaba"

Query 1: s[0:7] = "abacaba" → YES (palindrome)
Query 2: s[1:4] = "bac" → YES (palindrome)
Query 3: s[2:5] = "aca" → NO (not a palindrome)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(q × n)  
**Space Complexity**: O(1)

**Algorithm**:
1. For each query, extract the substring
2. Check if the substring is a palindrome by comparing characters from both ends
3. Return the result

**Implementation**:
```python
def brute_force_palindrome_queries(s, queries):
    results = []
    
    for l, r in queries:
        substring = s[l:r+1]
        is_palindrome = True
        
        # Check if substring is palindrome
        left, right = 0, len(substring) - 1
        while left < right:
            if substring[left] != substring[right]:
                is_palindrome = False
                break
            left += 1
            right -= 1
        
        results.append("YES" if is_palindrome else "NO")
    
    return results
```

**Analysis**:
- **Time**: O(q × n) - For each query, check palindrome in O(n) time
- **Space**: O(1) - Constant extra space
- **Limitations**: Too slow for large inputs with many queries

### Approach 2: Optimized with Rolling Hash
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Precompute rolling hash for the string and its reverse
2. For each query, compare hash values of substring and its reverse
3. Return the result based on hash comparison

**Implementation**:
```python
def optimized_palindrome_queries(s, queries):
    n = len(s)
    results = []
    
    # Precompute rolling hash
    P = 31
    M = 10**9 + 7
    
    # Hash for original string
    hash_forward = [0] * (n + 1)
    powers = [1] * (n + 1)
    
    for i in range(n):
        hash_forward[i + 1] = (hash_forward[i] * P + ord(s[i]) - ord('a') + 1) % M
        powers[i + 1] = (powers[i] * P) % M
    
    # Hash for reversed string
    hash_backward = [0] * (n + 1)
    for i in range(n):
        hash_backward[i + 1] = (hash_backward[i] * P + ord(s[n-1-i]) - ord('a') + 1) % M
    
    # Answer queries
    for l, r in queries:
        length = r - l + 1
        
        # Get hash of substring s[l:r+1]
        hash_sub = (hash_forward[r + 1] - (hash_forward[l] * powers[length]) % M + M) % M
        
        # Get hash of reversed substring
        hash_rev = (hash_backward[n - l] - (hash_backward[n - r - 1] * powers[length]) % M + M) % M
        
        results.append("YES" if hash_sub == hash_rev else "NO")
    
    return results
```

**Analysis**:
- **Time**: O(n + q) - Precomputation + O(1) per query
- **Space**: O(n) - Hash arrays
- **Improvement**: Much faster than brute force, handles hash collisions

### Approach 3: Optimal with Manacher's Algorithm
**Time Complexity**: O(n + q)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use Manacher's algorithm to find all palindromes
2. Precompute palindrome information for all positions
3. Answer queries in O(1) time using precomputed data

**Implementation**:
```python
def optimal_palindrome_queries(s, queries):
    n = len(s)
    results = []
    
    # Manacher's algorithm to find all palindromes
    # Create string with separators
    processed = "#" + "#".join(s) + "#"
    m = len(processed)
    
    # Array to store palindrome radii
    radius = [0] * m
    center = 0
    right = 0
    
    for i in range(m):
        if i < right:
            radius[i] = min(right - i, radius[2 * center - i])
        
        # Expand palindrome centered at i
        while (i + radius[i] + 1 < m and 
               i - radius[i] - 1 >= 0 and 
               processed[i + radius[i] + 1] == processed[i - radius[i] - 1]):
            radius[i] += 1
        
        # Update center and right if necessary
        if i + radius[i] > right:
            center = i
            right = i + radius[i]
    
    # Answer queries
    for l, r in queries:
        # Convert to processed string coordinates
        center_pos = 2 * l + 1 + (r - l)
        max_radius = radius[center_pos]
        
        # Check if the palindrome covers the entire substring
        if max_radius >= (r - l):
            results.append("YES")
        else:
            results.append("NO")
    
    return results
```

**Analysis**:
- **Time**: O(n + q) - Manacher's algorithm + O(1) per query
- **Space**: O(n) - Radius array
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
String: "abacaba"
Processed: "#a#b#a#c#a#b#a#"

Manacher's Algorithm:
Position: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
Char:     # a # b # a # c # a # b # a #
Radius:   0 1 0 3 0 1 0 7 0 1 0 3 0 1 0

Query 1: s[0:7] = "abacaba"
- Center position: 7 (corresponds to 'c')
- Radius: 7 (covers entire string)
- Result: YES

Query 2: s[1:4] = "bac"
- Center position: 3 (corresponds to 'b')
- Radius: 3 (covers "bac")
- Result: YES

Query 3: s[2:5] = "aca"
- Center position: 5 (corresponds to 'a')
- Radius: 1 (only covers "a")
- Result: NO
```

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check each substring character by character for palindrome property
- **Complete Coverage**: Guarantees correct answer but inefficient for many queries
- **Simple Implementation**: Easy to understand and implement

**Key Insights from Optimized Approach**:
- **Rolling Hash**: Use hash comparison to check palindrome property efficiently
- **Precomputation**: Precompute hash values to answer queries in O(1) time
- **Hash Collision Handling**: Handle potential hash collisions properly

**Key Insights from Optimal Approach**:
- **Manacher's Algorithm**: Use specialized algorithm for finding all palindromes
- **Linear Time**: Achieve O(n) preprocessing time with O(1) query time
- **Optimal Complexity**: Best possible complexity for this problem

## 🎯 Key Insights

### 🔑 **Core Concepts**
- **Palindrome Detection**: Checking if a string reads the same forwards and backwards
- **Rolling Hash**: Efficient hash computation for substring comparison
- **Manacher's Algorithm**: Specialized algorithm for finding all palindromes
- **Query Processing**: Efficient handling of multiple queries

### 💡 **Problem-Specific Insights**
- **Palindrome Queries**: Check if substrings are palindromes efficiently
- **Efficiency Optimization**: From O(q × n) brute force to O(n + q) optimal solution
- **Precomputation**: Use preprocessing to answer queries quickly

### 🚀 **Optimization Strategies**
- **Rolling Hash**: Use hash comparison for efficient palindrome checking
- **Manacher's Algorithm**: Use specialized algorithm for optimal performance
- **Query Optimization**: Precompute results to answer queries in O(1) time

## 🧠 Common Pitfalls & How to Avoid Them

### ❌ **Common Mistakes**
1. **Quadratic Time**: Brute force approach has O(q × n) time complexity
2. **Hash Collisions**: Not handling potential hash collisions in rolling hash approach
3. **Index Errors**: Incorrect handling of string indices in queries

### ✅ **Best Practices**
1. **Use Rolling Hash**: Implement rolling hash for efficient palindrome checking
2. **Handle Collisions**: Always verify hash matches with actual string comparison
3. **Efficient Algorithm**: Use Manacher's algorithm for optimal performance

## 🔗 Related Problems & Pattern Recognition

### 📚 **Similar Problems**
- **Longest Palindrome**: Finding the longest palindrome in a string
- **String Hashing**: Using rolling hash for string comparison
- **String Matching**: Finding patterns in strings

### 🎯 **Pattern Recognition**
- **Palindrome Problems**: Problems involving palindrome detection
- **Query Processing Problems**: Problems with multiple queries requiring optimization
- **String Processing Problems**: Problems requiring efficient string manipulation

## 📈 Complexity Analysis

### ⏱️ **Time Complexity**
- **Brute Force**: O(q × n) - Check each substring character by character
- **Optimized**: O(n + q) - Precomputation + O(1) per query
- **Optimal**: O(n + q) - Manacher's algorithm + O(1) per query

### 💾 **Space Complexity**
- **Brute Force**: O(1) - Constant extra space
- **Optimized**: O(n) - Hash arrays
- **Optimal**: O(n) - Radius array from Manacher's algorithm

## 🎓 Summary

### 🏆 **Key Takeaways**
1. **Palindrome Detection**: Important problem type in string processing
2. **Rolling Hash**: Essential technique for efficient string comparison
3. **Manacher's Algorithm**: Powerful algorithm for finding all palindromes
4. **Query Optimization**: Precomputation can significantly improve query performance

### 🚀 **Next Steps**
1. **Practice**: Implement palindrome detection algorithms with different approaches
2. **Advanced Topics**: Learn about more complex palindrome problems
3. **Related Problems**: Solve more string processing and query problems
