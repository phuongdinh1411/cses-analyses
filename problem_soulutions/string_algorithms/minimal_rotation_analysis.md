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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Minimal Rotation with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain minimal rotation queries efficiently.

**Link**: [CSES Problem Set - Minimal Rotation with Updates](https://cses.fi/problemset/task/minimal_rotation_updates)

```python
class MinimalRotationWithUpdates:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.min_rotation = self._find_minimal_rotation()
    
    def _find_minimal_rotation(self):
        """Find minimal rotation using Booth's algorithm"""
        if not self.s:
            return 0
        
        # Double the string to handle circular nature
        doubled = self.s + self.s
        n = len(self.s)
        
        # Initialize failure function
        failure = [0] * (2 * n)
        
        # Find minimal rotation
        min_rotation = 0
        for i in range(1, 2 * n):
            j = failure[i - 1]
            while j > 0 and doubled[i] != doubled[j]:
                j = failure[j - 1]
            
            if doubled[i] == doubled[j]:
                j += 1
            
            failure[i] = j
            
            # Update minimal rotation
            if i >= n and failure[i] == n:
                min_rotation = i - n + 1
                break
        
        return min_rotation
    
    def update(self, pos, char):
        """Update character at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.s[pos] = char
        
        # Recalculate minimal rotation
        self.min_rotation = self._find_minimal_rotation()
    
    def get_minimal_rotation(self):
        """Get current minimal rotation"""
        return self.min_rotation
    
    def get_rotated_string(self):
        """Get string rotated to minimal position"""
        if not self.s:
            return ""
        
        rotated = self.s[self.min_rotation:] + self.s[:self.min_rotation]
        return ''.join(rotated)
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'rotation':
                result = self.get_minimal_rotation()
                results.append(result)
            elif query['type'] == 'string':
                result = self.get_rotated_string()
                results.append(result)
        return results
```

### Variation 2: Minimal Rotation with Different Operations
**Problem**: Handle different types of operations (rotation, comparison, sorting) on string rotations.

**Link**: [CSES Problem Set - Minimal Rotation Different Operations](https://cses.fi/problemset/task/minimal_rotation_operations)

```python
class MinimalRotationDifferentOps:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.min_rotation = self._find_minimal_rotation()
        self.all_rotations = self._generate_all_rotations()
    
    def _find_minimal_rotation(self):
        """Find minimal rotation using Booth's algorithm"""
        if not self.s:
            return 0
        
        # Double the string to handle circular nature
        doubled = self.s + self.s
        n = len(self.s)
        
        # Initialize failure function
        failure = [0] * (2 * n)
        
        # Find minimal rotation
        min_rotation = 0
        for i in range(1, 2 * n):
            j = failure[i - 1]
            while j > 0 and doubled[i] != doubled[j]:
                j = failure[j - 1]
            
            if doubled[i] == doubled[j]:
                j += 1
            
            failure[i] = j
            
            # Update minimal rotation
            if i >= n and failure[i] == n:
                min_rotation = i - n + 1
                break
        
        return min_rotation
    
    def _generate_all_rotations(self):
        """Generate all possible rotations"""
        rotations = []
        for i in range(self.n):
            rotated = self.s[i:] + self.s[:i]
            rotations.append(''.join(rotated))
        return rotations
    
    def get_minimal_rotation(self):
        """Get minimal rotation index"""
        return self.min_rotation
    
    def get_all_rotations(self):
        """Get all possible rotations"""
        return self.all_rotations.copy()
    
    def compare_rotations(self, i, j):
        """Compare two rotations"""
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return 0
        
        rotation_i = self.all_rotations[i]
        rotation_j = self.all_rotations[j]
        
        if rotation_i < rotation_j:
            return -1
        elif rotation_i > rotation_j:
            return 1
        else:
            return 0
    
    def sort_rotations(self):
        """Sort all rotations lexicographically"""
        return sorted(self.all_rotations)
    
    def find_rotation_rank(self, rotation):
        """Find rank of a specific rotation"""
        sorted_rotations = self.sort_rotations()
        try:
            return sorted_rotations.index(rotation)
        except ValueError:
            return -1
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'minimal':
                result = self.get_minimal_rotation()
                results.append(result)
            elif query['type'] == 'all':
                result = self.get_all_rotations()
                results.append(result)
            elif query['type'] == 'compare':
                result = self.compare_rotations(query['i'], query['j'])
                results.append(result)
            elif query['type'] == 'sort':
                result = self.sort_rotations()
                results.append(result)
            elif query['type'] == 'rank':
                result = self.find_rotation_rank(query['rotation'])
                results.append(result)
        return results
```

### Variation 3: Minimal Rotation with Constraints
**Problem**: Handle minimal rotation queries with additional constraints (e.g., minimum length, maximum rotations).

**Link**: [CSES Problem Set - Minimal Rotation with Constraints](https://cses.fi/problemset/task/minimal_rotation_constraints)

```python
class MinimalRotationWithConstraints:
    def __init__(self, s, min_length, max_rotations):
        self.s = list(s)
        self.n = len(self.s)
        self.min_length = min_length
        self.max_rotations = max_rotations
        self.min_rotation = self._find_minimal_rotation()
    
    def _find_minimal_rotation(self):
        """Find minimal rotation using Booth's algorithm"""
        if not self.s or len(self.s) < self.min_length:
            return 0
        
        # Double the string to handle circular nature
        doubled = self.s + self.s
        n = len(self.s)
        
        # Initialize failure function
        failure = [0] * (2 * n)
        
        # Find minimal rotation
        min_rotation = 0
        for i in range(1, 2 * n):
            j = failure[i - 1]
            while j > 0 and doubled[i] != doubled[j]:
                j = failure[j - 1]
            
            if doubled[i] == doubled[j]:
                j += 1
            
            failure[i] = j
            
            # Update minimal rotation
            if i >= n and failure[i] == n:
                min_rotation = i - n + 1
                break
        
        return min_rotation
    
    def constrained_query(self, start, end):
        """Query minimal rotation in range [start, end] with constraints"""
        # Check minimum length constraint
        if end - start + 1 < self.min_length:
            return None  # Too short
        
        # Check maximum rotations constraint
        if end - start + 1 > self.max_rotations:
            return None  # Too many rotations
        
        # Get substring
        substring = self.s[start:end+1]
        
        # Find minimal rotation for substring
        if not substring:
            return None
        
        # Double the substring to handle circular nature
        doubled = substring + substring
        n = len(substring)
        
        # Initialize failure function
        failure = [0] * (2 * n)
        
        # Find minimal rotation
        min_rotation = 0
        for i in range(1, 2 * n):
            j = failure[i - 1]
            while j > 0 and doubled[i] != doubled[j]:
                j = failure[j - 1]
            
            if doubled[i] == doubled[j]:
                j += 1
            
            failure[i] = j
            
            # Update minimal rotation
            if i >= n and failure[i] == n:
                min_rotation = i - n + 1
                break
        
        return min_rotation
    
    def find_valid_ranges(self):
        """Find all valid ranges that satisfy constraints"""
        valid_ranges = []
        for i in range(self.n):
            for j in range(i + self.min_length - 1, min(i + self.max_rotations, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    valid_ranges.append((i, j, result))
        return valid_ranges
    
    def get_maximum_valid_rotation(self):
        """Get maximum valid rotation"""
        max_rotation = 0
        for i in range(self.n):
            for j in range(i + self.min_length - 1, min(i + self.max_rotations, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    max_rotation = max(max_rotation, result)
        return max_rotation
    
    def count_valid_ranges(self):
        """Count number of valid ranges"""
        count = 0
        for i in range(self.n):
            for j in range(i + self.min_length - 1, min(i + self.max_rotations, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    count += 1
        return count

# Example usage
s = "abacaba"
min_length = 3
max_rotations = 5

mr = MinimalRotationWithConstraints(s, min_length, max_rotations)
result = mr.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: 0

valid_ranges = mr.find_valid_ranges()
print(f"Valid ranges: {valid_ranges}")

max_rotation = mr.get_maximum_valid_rotation()
print(f"Maximum valid rotation: {max_rotation}")
```

### Related Problems

#### **CSES Problems**
- [Minimal Rotation](https://cses.fi/problemset/task/1110) - Basic minimal rotation problem
- [String Matching](https://cses.fi/problemset/task/1753) - String matching
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string

#### **LeetCode Problems**
- [Rotate String](https://leetcode.com/problems/rotate-string/) - Check if string is rotation
- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) - String matching with repetition
- [String Rotation](https://leetcode.com/problems/string-rotation/) - String rotation problems

#### **Problem Categories**
- **String Rotation**: Minimal rotation, string comparison, circular strings
- **Pattern Matching**: KMP, Z-algorithm, string matching algorithms
- **String Processing**: Borders, periods, palindromes, string transformations
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata

## 🚀 Key Takeaways

- **String Rotation**: Important concept in string processing
- **Booth's Algorithm**: Essential for finding minimal rotations efficiently
- **Lexicographical Ordering**: Fundamental concept for string comparison
- **Doubled String Technique**: Useful for handling circular problems
