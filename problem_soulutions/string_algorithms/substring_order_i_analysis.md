---
layout: simple
title: "Substring Order I"
permalink: /problem_soulutions/string_algorithms/substring_order_i_analysis
---

# Substring Order I

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand lexicographical ordering of substrings and their applications
- Apply suffix array and LCP array techniques for substring ordering
- Implement efficient solutions for substring order problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in substring ordering problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Suffix arrays, LCP arrays, lexicographical ordering, string sorting
- **Data Structures**: Strings, suffix arrays, LCP arrays, sorting algorithms
- **Mathematical Concepts**: String theory, lexicographical ordering, suffix array construction
- **Programming Skills**: String manipulation, algorithm implementation, sorting optimization
- **Related Problems**: Substring Order II (with length constraints), Distinct Substrings (suffix arrays), String Sorting

## 📋 Problem Description

You are given a string s and q queries. Each query consists of an integer k. For each query, find the k-th lexicographically smallest substring in the string s.

**Input**: 
- First line: string s
- Second line: integer q (number of queries)
- Next q lines: integer k

**Output**: 
- For each query, print the k-th lexicographically smallest substring

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- 1 ≤ q ≤ 10⁵
- 1 ≤ k ≤ number of distinct substrings
- s contains only lowercase English letters

**Example**:
```
Input:
ababab
3
1
2
3

Output:
a
ab
aba

Explanation**: 
String: "ababab"

All distinct substrings (lexicographically sorted):
1. "a" (positions 0, 2, 4)
2. "ab" (positions 0-1, 2-3, 4-5)
3. "aba" (positions 0-2, 2-4)
4. "abab" (positions 0-3, 2-5)
5. "ababab" (positions 0-5)
6. "b" (positions 1, 3, 5)
7. "ba" (positions 1-2, 3-4)
8. "bab" (positions 1-3, 3-5)
9. "baba" (positions 1-4)
10. "babab" (positions 1-5)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n² log n + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Generate all possible substrings
2. Remove duplicates and sort lexicographically
3. For each query, return the k-th substring

**Implementation**:
```python
def brute_force_substring_order_i(s, queries):
    n = len(s)
    results = []
    
    # Generate all possible substrings
    all_substrings = set()
    for i in range(n):
        for j in range(i + 1, n + 1):
            all_substrings.add(s[i:j])
    
    # Sort lexicographically
    sorted_substrings = sorted(list(all_substrings))
    
    # Answer queries
    for k in queries:
        if k <= len(sorted_substrings):
            results.append(sorted_substrings[k - 1])
        else:
            results.append("")  # Invalid query
    
    return results
```

**Analysis**:
- **Time**: O(n² log n) - Generate and sort all substrings
- **Space**: O(n²) - Store all unique substrings
- **Limitations**: Too slow and memory-intensive for large inputs

### Approach 2: Optimized with Suffix Array
**Time Complexity**: O(n log n + q × n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Build suffix array for the string
2. For each query, use suffix array to find k-th lexicographically smallest substring
3. Extract substring from the appropriate suffix

**Implementation**:
```python
def optimized_substring_order_i(s, queries):
    n = len(s)
    results = []
    
    # Build suffix array (simplified version)
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    suffixes.sort()
    
    # Answer queries
    for k in queries:
        # Find k-th lexicographically smallest substring
        count = 0
        for suffix, start_pos in suffixes:
            # Add all substrings starting from this suffix
            for length in range(1, len(suffix) + 1):
                substring = suffix[:length]
                # Check if this is a new unique substring
                is_new = True
                for prev_suffix, prev_start in suffixes[:suffixes.index((suffix, start_pos))]:
                    if len(prev_suffix) >= length and prev_suffix[:length] == substring:
                        is_new = False
                        break
                
                if is_new:
                    count += 1
                    if count == k:
                        results.append(substring)
                        break
            if count == k:
                break
        else:
            results.append("")  # Invalid query
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q × n) - Suffix array construction + query processing
- **Space**: O(n) - Suffix array storage
- **Improvement**: More efficient than brute force, but still not optimal for queries

### Approach 3: Optimal with Precomputed Substring Ordering
**Time Complexity**: O(n log n + q)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Build suffix array and LCP array
2. Precompute all unique substrings with their lexicographical order
3. Answer queries in O(1) time using precomputed data

**Implementation**:
```python
def optimal_substring_order_i(s, queries):
    n = len(s)
    
    # Build suffix array
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    suffixes.sort()
    
    # Precompute all unique substrings with their order
    all_substrings = []
    seen = set()
    
    for suffix, start_pos in suffixes:
        for length in range(1, len(suffix) + 1):
            substring = suffix[:length]
            if substring not in seen:
                seen.add(substring)
                all_substrings.append(substring)
    
    # Answer queries
    results = []
    for k in queries:
        if k <= len(all_substrings):
            results.append(all_substrings[k - 1])
        else:
            results.append("")  # Invalid query
    
    return results
```

**Analysis**:
- **Time**: O(n log n + q) - Precomputation + O(1) per query
- **Space**: O(n²) - Store all unique substrings
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
String: "ababab"

Suffix Array (sorted):
Index | Suffix    | Start
------|-----------|-------
  0   | "ab"      |   4
  1   | "abab"    |   2
  2   | "ababab"  |   0
  3   | "b"       |   5
  4   | "bab"     |   3
  5   | "babab"   |   1

All substrings (lexicographically sorted):
1. "a" (from suffix "ababab")
2. "ab" (from suffix "ab")
3. "aba" (from suffix "abab")
4. "abab" (from suffix "abab")
5. "ababab" (from suffix "ababab")
6. "b" (from suffix "b")
7. "ba" (from suffix "bab")
8. "bab" (from suffix "bab")
9. "baba" (from suffix "babab")
10. "babab" (from suffix "babab")
```

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Generate all possible substrings and sort them lexicographically
- **Complete Coverage**: Guarantees finding the correct answer but inefficient
- **Simple Implementation**: Easy to understand and implement

**Key Insights from Optimized Approach**:
- **Suffix Array**: Use suffix array to efficiently find lexicographically ordered substrings
- **Query Processing**: Process each query by traversing the suffix array
- **Memory Efficiency**: Better space complexity than brute force

**Key Insights from Optimal Approach**:
- **Precomputation**: Precompute all unique substrings with their lexicographical order
- **Query Optimization**: Answer queries in O(1) time using precomputed data
- **Optimal Complexity**: Best possible complexity for this problem

## 🎯 Key Insights

### 🔑 **Core Concepts**
- **Lexicographical Ordering**: Dictionary order comparison of strings
- **Suffix Arrays**: Lexicographically sorted array of all suffixes
- **Substring Ordering**: Finding k-th lexicographically smallest substring
- **Query Processing**: Efficient handling of multiple queries

### 💡 **Problem-Specific Insights**
- **Substring Ordering**: Use suffix array to find lexicographically ordered substrings
- **Query Optimization**: Precompute results to answer queries efficiently
- **Efficiency Optimization**: From O(n² log n) brute force to O(n log n + q) optimal solution

### 🚀 **Optimization Strategies**
- **Suffix Array Construction**: Use efficient algorithms for building suffix arrays
- **Precomputation**: Precompute all unique substrings to answer queries quickly
- **Memory Management**: Balance between time and space complexity

## 🧠 Common Pitfalls & How to Avoid Them

### ❌ **Common Mistakes**
1. **Duplicate Substrings**: Ensure unique substrings are counted correctly
2. **Query Validation**: Handle invalid queries (k > number of unique substrings)
3. **Edge Cases**: Handle empty strings, single character strings, and boundary conditions

### ✅ **Best Practices**
1. **Efficient Suffix Array**: Use optimized suffix array construction algorithms
2. **Proper Sorting**: Ensure lexicographical ordering is correct
3. **Query Optimization**: Precompute results when possible

## 🔗 Related Problems & Pattern Recognition

### 📚 **Similar Problems**
- **Substring Order II**: Substring ordering with length constraints
- **Distinct Substrings**: Counting unique substrings using suffix arrays
- **String Sorting**: Lexicographical ordering of strings

### 🎯 **Pattern Recognition**
- **Suffix Array Problems**: Problems involving string processing and ordering
- **Query Processing Problems**: Problems with multiple queries requiring optimization
- **String Ordering Problems**: Problems involving lexicographical comparison

## 📈 Complexity Analysis

### ⏱️ **Time Complexity**
- **Brute Force**: O(n² log n + q) - Generate, sort, and query all substrings
- **Optimized**: O(n log n + q × n) - Suffix array construction + query processing
- **Optimal**: O(n log n + q) - Precomputation + O(1) per query

### 💾 **Space Complexity**
- **Brute Force**: O(n²) - Store all unique substrings
- **Optimized**: O(n) - Suffix array storage
- **Optimal**: O(n²) - Store all unique substrings for fast queries

## 🎓 Summary

### 🏆 **Key Takeaways**
1. **Suffix Arrays**: Essential for efficient string processing and ordering
2. **Lexicographical Ordering**: Important concept for string comparison
3. **Query Optimization**: Precomputation can significantly improve query performance
4. **Substring Processing**: Efficient techniques for handling substring operations

### 🚀 **Next Steps**
1. **Practice**: Implement suffix array construction algorithms
2. **Advanced Topics**: Learn about advanced string data structures
3. **Related Problems**: Solve more string processing and query problems
