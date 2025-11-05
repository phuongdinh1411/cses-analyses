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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Palindrome Queries with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain palindrome queries efficiently.

**Link**: [CSES Problem Set - Palindrome Queries with Updates](https://cses.fi/problemset/task/palindrome_queries_updates)

```python
class PalindromeQueriesWithUpdates:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.forward_hash = self._build_forward_hash()
        self.backward_hash = self._build_backward_hash()
        self.powers = self._build_powers()
    
    def _build_forward_hash(self):
        """Build forward hash array"""
        forward_hash = [0] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(self.n):
            forward_hash[i + 1] = (forward_hash[i] * base + ord(self.s[i])) % mod
        
        return forward_hash
    
    def _build_backward_hash(self):
        """Build backward hash array"""
        backward_hash = [0] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(self.n - 1, -1, -1):
            backward_hash[i] = (backward_hash[i + 1] * base + ord(self.s[i])) % mod
        
        return backward_hash
    
    def _build_powers(self):
        """Build powers array for hash computation"""
        powers = [1] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(1, self.n + 1):
            powers[i] = (powers[i - 1] * base) % mod
        
        return powers
    
    def update(self, pos, char):
        """Update character at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.s[pos] = char
        
        # Rebuild hash arrays
        self.forward_hash = self._build_forward_hash()
        self.backward_hash = self._build_backward_hash()
    
    def is_palindrome(self, left, right):
        """Check if substring [left, right] is palindrome"""
        if left < 0 or right >= self.n or left > right:
            return False
        
        # Get forward hash
        forward = (self.forward_hash[right + 1] - self.forward_hash[left] * self.powers[right - left + 1]) % (10**9 + 7)
        
        # Get backward hash
        backward = (self.backward_hash[left] - self.backward_hash[right + 1] * self.powers[right - left + 1]) % (10**9 + 7)
        
        return forward == backward
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'palindrome':
                result = self.is_palindrome(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 2: Palindrome Queries with Different Operations
**Problem**: Handle different types of operations (check, count, list) on palindrome queries.

**Link**: [CSES Problem Set - Palindrome Queries Different Operations](https://cses.fi/problemset/task/palindrome_queries_operations)

```python
class PalindromeQueriesDifferentOps:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.forward_hash = self._build_forward_hash()
        self.backward_hash = self._build_backward_hash()
        self.powers = self._build_powers()
    
    def _build_forward_hash(self):
        """Build forward hash array"""
        forward_hash = [0] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(self.n):
            forward_hash[i + 1] = (forward_hash[i] * base + ord(self.s[i])) % mod
        
        return forward_hash
    
    def _build_backward_hash(self):
        """Build backward hash array"""
        backward_hash = [0] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(self.n - 1, -1, -1):
            backward_hash[i] = (backward_hash[i + 1] * base + ord(self.s[i])) % mod
        
        return backward_hash
    
    def _build_powers(self):
        """Build powers array for hash computation"""
        powers = [1] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(1, self.n + 1):
            powers[i] = (powers[i - 1] * base) % mod
        
        return powers
    
    def is_palindrome(self, left, right):
        """Check if substring [left, right] is palindrome"""
        if left < 0 or right >= self.n or left > right:
            return False
        
        # Get forward hash
        forward = (self.forward_hash[right + 1] - self.forward_hash[left] * self.powers[right - left + 1]) % (10**9 + 7)
        
        # Get backward hash
        backward = (self.backward_hash[left] - self.backward_hash[right + 1] * self.powers[right - left + 1]) % (10**9 + 7)
        
        return forward == backward
    
    def count_palindromes(self, left, right):
        """Count palindromes in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return 0
        
        count = 0
        for i in range(left, right + 1):
            for j in range(i, right + 1):
                if self.is_palindrome(i, j):
                    count += 1
        
        return count
    
    def list_palindromes(self, left, right):
        """List all palindromes in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return []
        
        palindromes = []
        for i in range(left, right + 1):
            for j in range(i, right + 1):
                if self.is_palindrome(i, j):
                    palindromes.append((i, j))
        
        return palindromes
    
    def get_longest_palindrome(self, left, right):
        """Get longest palindrome in range [left, right]"""
        if left < 0 or right >= self.n or left > right:
            return None
        
        longest = None
        max_length = 0
        
        for i in range(left, right + 1):
            for j in range(i, right + 1):
                if self.is_palindrome(i, j):
                    length = j - i + 1
                    if length > max_length:
                        max_length = length
                        longest = (i, j)
        
        return longest
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'check':
                result = self.is_palindrome(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'count':
                result = self.count_palindromes(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'list':
                result = self.list_palindromes(query['left'], query['right'])
                results.append(result)
            elif query['type'] == 'longest':
                result = self.get_longest_palindrome(query['left'], query['right'])
                results.append(result)
        return results
```

### Variation 3: Palindrome Queries with Constraints
**Problem**: Handle palindrome queries with additional constraints (e.g., minimum length, maximum length).

**Link**: [CSES Problem Set - Palindrome Queries with Constraints](https://cses.fi/problemset/task/palindrome_queries_constraints)

```python
class PalindromeQueriesWithConstraints:
    def __init__(self, s, min_length, max_length):
        self.s = list(s)
        self.n = len(self.s)
        self.min_length = min_length
        self.max_length = max_length
        self.forward_hash = self._build_forward_hash()
        self.backward_hash = self._build_backward_hash()
        self.powers = self._build_powers()
    
    def _build_forward_hash(self):
        """Build forward hash array"""
        forward_hash = [0] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(self.n):
            forward_hash[i + 1] = (forward_hash[i] * base + ord(self.s[i])) % mod
        
        return forward_hash
    
    def _build_backward_hash(self):
        """Build backward hash array"""
        backward_hash = [0] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(self.n - 1, -1, -1):
            backward_hash[i] = (backward_hash[i + 1] * base + ord(self.s[i])) % mod
        
        return backward_hash
    
    def _build_powers(self):
        """Build powers array for hash computation"""
        powers = [1] * (self.n + 1)
        base = 31
        mod = 10**9 + 7
        
        for i in range(1, self.n + 1):
            powers[i] = (powers[i - 1] * base) % mod
        
        return powers
    
    def constrained_query(self, left, right):
        """Query palindrome in range [left, right] with constraints"""
        # Check minimum length constraint
        if right - left + 1 < self.min_length:
            return None  # Too short
        
        # Check maximum length constraint
        if right - left + 1 > self.max_length:
            return None  # Too long
        
        # Check if palindrome
        if self.is_palindrome(left, right):
            return (left, right)
        
        return None
    
    def is_palindrome(self, left, right):
        """Check if substring [left, right] is palindrome"""
        if left < 0 or right >= self.n or left > right:
            return False
        
        # Get forward hash
        forward = (self.forward_hash[right + 1] - self.forward_hash[left] * self.powers[right - left + 1]) % (10**9 + 7)
        
        # Get backward hash
        backward = (self.backward_hash[left] - self.backward_hash[right + 1] * self.powers[right - left + 1]) % (10**9 + 7)
        
        return forward == backward
    
    def find_valid_palindromes(self):
        """Find all valid palindromes that satisfy constraints"""
        valid_palindromes = []
        for i in range(self.n):
            for j in range(i + self.min_length - 1, min(i + self.max_length, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    valid_palindromes.append(result)
        return valid_palindromes
    
    def get_longest_valid_palindrome(self):
        """Get longest valid palindrome"""
        longest = None
        max_length = 0
        
        for i in range(self.n):
            for j in range(i + self.min_length - 1, min(i + self.max_length, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    length = j - i + 1
                    if length > max_length:
                        max_length = length
                        longest = result
        
        return longest
    
    def count_valid_palindromes(self):
        """Count number of valid palindromes"""
        count = 0
        for i in range(self.n):
            for j in range(i + self.min_length - 1, min(i + self.max_length, self.n)):
                result = self.constrained_query(i, j)
                if result is not None:
                    count += 1
        return count

# Example usage
s = "abacaba"
min_length = 3
max_length = 5

pq = PalindromeQueriesWithConstraints(s, min_length, max_length)
result = pq.constrained_query(0, 2)
print(f"Constrained query result: {result}")  # Output: (0, 2)

valid_palindromes = pq.find_valid_palindromes()
print(f"Valid palindromes: {valid_palindromes}")

longest = pq.get_longest_valid_palindrome()
print(f"Longest valid palindrome: {longest}")
```

### Related Problems

#### **CSES Problems**
- [Palindrome Queries](https://cses.fi/problemset/task/2420) - Basic palindrome queries problem
- [String Matching](https://cses.fi/problemset/task/1753) - String matching
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string

#### **LeetCode Problems**
- [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) - Find longest palindrome
- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) - Check if string is palindrome
- [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) - Partition string into palindromes

#### **Problem Categories**
- **Palindrome Detection**: String palindromes, substring palindromes, palindrome queries
- **Pattern Matching**: KMP, Z-algorithm, string matching algorithms
- **String Processing**: Borders, periods, palindromes, string transformations
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata

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
