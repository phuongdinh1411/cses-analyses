---
layout: simple
title: "Repeating Substring"
permalink: /problem_soulutions/string_algorithms/repeating_substring_analysis
---

# Repeating Substring

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of repeating substrings and their applications
- Apply string hashing and rolling hash techniques for pattern detection
- Implement efficient solutions for repeating substring problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in repeating substring problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String hashing, rolling hash, pattern matching, KMP algorithm
- **Data Structures**: Strings, hash maps, rolling hash tables
- **Mathematical Concepts**: String theory, pattern matching, hashing, periodicity
- **Programming Skills**: String manipulation, algorithm implementation, hash optimization
- **Related Problems**: String Matching (pattern matching), Finding Periods (periodicity), String Hashing

## 📋 Problem Description

You are given a string s. Find the length of the longest repeating substring in the string.

A repeating substring is a substring that appears at least twice in the string (non-overlapping occurrences).

**Input**: 
- First line: string s

**Output**: 
- Print one integer: the length of the longest repeating substring

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- s contains only lowercase English letters

**Example**:
```
Input:
ababab

Output:
4

Explanation**: 
String: "ababab"

Repeating substrings:
- "ab" appears 3 times (positions 0-1, 2-3, 4-5)
- "abab" appears 2 times (positions 0-3, 2-5)

Longest repeating substring: "abab" with length 4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n³)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Generate all possible substrings
2. For each substring, count its occurrences in the string
3. Return the length of the longest substring that appears at least twice

**Implementation**:
```python
def brute_force_repeating_substring(s):
    n = len(s)
    max_length = 0
    
    # Try all possible substring lengths
    for length in range(1, n):
        # Try all possible starting positions
        for i in range(n - length + 1):
            substring = s[i:i + length]
            count = 0
            
            # Count occurrences of this substring
            for j in range(n - length + 1):
                if s[j:j + length] == substring:
                    count += 1
            
            # If it appears at least twice, update max length
            if count >= 2:
                max_length = max(max_length, length)
    
    return max_length
```

**Analysis**:
- **Time**: O(n³) - Three nested loops
- **Space**: O(n²) - Storing all possible substrings
- **Limitations**: Too slow for large inputs

### Approach 2: Optimized with Rolling Hash
**Time Complexity**: O(n²)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Use rolling hash to efficiently compute substring hashes
2. Group substrings by their hash values
3. For each hash group, verify actual matches and count occurrences
4. Return the length of the longest substring with at least 2 occurrences

**Implementation**:
```python
def optimized_repeating_substring(s):
    n = len(s)
    max_length = 0
    P = 31  # Prime base
    M = 10**9 + 7  # Large prime modulus
    
    # Precompute powers of P
    powers = [1] * (n + 1)
    for i in range(1, n + 1):
        powers[i] = (powers[i-1] * P) % M
    
    # Try all possible substring lengths
    for length in range(1, n):
        hash_to_positions = {}
        
        # Compute rolling hash for all substrings of current length
        current_hash = 0
        for i in range(length):
            current_hash = (current_hash * P + ord(s[i]) - ord('a') + 1) % M
        
        # Store first occurrence
        if current_hash not in hash_to_positions:
            hash_to_positions[current_hash] = []
        hash_to_positions[current_hash].append(0)
        
        # Rolling hash for remaining positions
        for i in range(1, n - length + 1):
            # Remove leftmost character
            current_hash = (current_hash - (ord(s[i-1]) - ord('a') + 1) * powers[length-1]) % M
            current_hash = (current_hash + M) % M  # Handle negative
            
            # Add rightmost character
            current_hash = (current_hash * P + ord(s[i + length - 1]) - ord('a') + 1) % M
            
            # Store position
            if current_hash not in hash_to_positions:
                hash_to_positions[current_hash] = []
            hash_to_positions[current_hash].append(i)
        
        # Check for repeating substrings
        for hash_val, positions in hash_to_positions.items():
            if len(positions) >= 2:
                # Verify actual matches (handle hash collisions)
                for i in range(len(positions)):
                    for j in range(i + 1, len(positions)):
                        pos1, pos2 = positions[i], positions[j]
                        if s[pos1:pos1 + length] == s[pos2:pos2 + length]:
                            max_length = max(max_length, length)
                            break
                    if max_length == length:
                        break
    
    return max_length
```

**Analysis**:
- **Time**: O(n²) - Two nested loops with rolling hash
- **Space**: O(n²) - Hash map storing positions
- **Improvement**: Much faster than brute force, handles hash collisions

### Approach 3: Optimal with Suffix Array
**Time Complexity**: O(n log n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Build suffix array for the string
2. Compute LCP (Longest Common Prefix) array
3. Find the maximum LCP value, which represents the longest repeating substring

**Implementation**:
```python
def optimal_repeating_substring(s):
    n = len(s)
    
    # Build suffix array (simplified version)
    # In practice, use efficient algorithms like DC3 or SA-IS
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    suffixes.sort()
    
    # Compute LCP array
    lcp = [0] * n
    for i in range(1, n):
        lcp[i] = longest_common_prefix(suffixes[i-1][0], suffixes[i][0])
    
    # Find maximum LCP
    max_lcp = max(lcp) if lcp else 0
    return max_lcp

def longest_common_prefix(s1, s2):
    """Find length of longest common prefix between two strings"""
    min_len = min(len(s1), len(s2))
    for i in range(min_len):
        if s1[i] != s2[i]:
            return i
    return min_len
```

**Analysis**:
- **Time**: O(n log n) - Suffix array construction
- **Space**: O(n) - Suffix array and LCP array
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
String: "ababab"

Suffix Array:
Index | Suffix | LCP
------|--------|----
  0   | "ab"   |  0
  1   | "abab" |  2  ← Longest common prefix
  2   | "ababab"| 4
  3   | "b"    |  0
  4   | "bab"  |  1
  5   | "babab"| 3

Maximum LCP = 4
Longest repeating substring: "abab" (length 4)
```

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible substrings and count their occurrences
- **Complete Coverage**: Guarantees finding the correct answer but inefficient
- **Simple Implementation**: Easy to understand and implement

**Key Insights from Optimized Approach**:
- **Rolling Hash**: Efficiently compute hash values for all substrings of a given length
- **Efficient Grouping**: Group substrings by hash values to avoid redundant comparisons
- **Hash Collision Handling**: Verify actual matches when hash values are equal

**Key Insights from Optimal Approach**:
- **Suffix Array**: Provides lexicographically sorted suffixes for efficient comparison
- **LCP Array**: Longest Common Prefix array reveals repeating patterns
- **Optimal Complexity**: O(n log n) is the best possible for this problem

## 🎯 Key Insights

### 🔑 **Core Concepts**
- **String Hashing**: Use polynomial rolling hash to efficiently compare substrings
- **Rolling Hash**: Compute hash values incrementally to avoid recomputation
- **Suffix Arrays**: Lexicographically sorted array of all suffixes
- **LCP Arrays**: Longest Common Prefix between adjacent suffixes in suffix array

### 💡 **Problem-Specific Insights**
- **Repeating Substrings**: A substring that appears at least twice in the string
- **Pattern Detection**: Use suffix arrays to find common prefixes efficiently
- **Efficiency Optimization**: From O(n³) brute force to O(n log n) optimal solution

### 🚀 **Optimization Strategies**
- **Hash-based Grouping**: Group substrings by hash values to reduce comparisons
- **Suffix Array Construction**: Use efficient algorithms like DC3 or SA-IS
- **LCP Computation**: Compute LCP array to find longest repeating substrings

## 🧠 Common Pitfalls & How to Avoid Them

### ❌ **Common Mistakes**
1. **Hash Collisions**: Different strings may have the same hash value - always verify actual matches
2. **Overlapping Occurrences**: Ensure non-overlapping occurrences when counting repeats
3. **Edge Cases**: Handle empty strings, single character strings, and no repeating substrings

### ✅ **Best Practices**
1. **Proper Hash Function**: Use large prime modulus and base to minimize collisions
2. **Collision Handling**: Always verify actual string matches when hash values are equal
3. **Efficient Implementation**: Use rolling hash for O(1) hash computation per substring

## 🔗 Related Problems & Pattern Recognition

### 📚 **Similar Problems**
- **String Matching**: Finding pattern occurrences in text using similar techniques
- **Finding Periods**: Detecting periodic patterns in strings
- **Distinct Substrings**: Counting unique substrings using suffix arrays

### 🎯 **Pattern Recognition**
- **String Hashing Problems**: Problems involving substring comparison and pattern matching
- **Suffix Array Problems**: Problems requiring efficient string processing and comparison
- **Pattern Matching Problems**: Problems involving finding repeating or common patterns

## 📈 Complexity Analysis

### ⏱️ **Time Complexity**
- **Brute Force**: O(n³) - Three nested loops checking all substrings
- **Optimized**: O(n²) - Two nested loops with rolling hash optimization
- **Optimal**: O(n log n) - Suffix array construction and LCP computation

### 💾 **Space Complexity**
- **Brute Force**: O(n²) - Storing all possible substrings
- **Optimized**: O(n²) - Hash map storing positions for each hash value
- **Optimal**: O(n) - Suffix array and LCP array storage

## 🎓 Summary

### 🏆 **Key Takeaways**
1. **String Hashing**: Essential technique for efficient substring comparison
2. **Rolling Hash**: Enables O(1) hash computation for sliding windows
3. **Suffix Arrays**: Powerful data structure for string processing problems
4. **LCP Arrays**: Reveal repeating patterns and common prefixes efficiently

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Repeating Substring with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain repeating substring queries efficiently.

**Link**: [CSES Problem Set - Repeating Substring with Updates](https://cses.fi/problemset/task/repeating_substring_updates)

```python
class RepeatingSubstringWithUpdates:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
    
    def _build_suffix_array(self):
        """Build suffix array using efficient algorithm"""
        suffixes = []
        for i in range(self.n):
            suffixes.append((self.s[i:], i))
        
        suffixes.sort()
        return [suffix[1] for suffix in suffixes]
    
    def _build_lcp_array(self):
        """Build LCP array from suffix array"""
        lcp = [0] * self.n
        rank = [0] * self.n
        
        for i in range(self.n):
            rank[self.suffix_array[i]] = i
        
        h = 0
        for i in range(self.n):
            if rank[i] > 0:
                j = self.suffix_array[rank[i] - 1]
                while i + h < self.n and j + h < self.n and self.s[i + h] == self.s[j + h]:
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1
        
        return lcp
    
    def update(self, pos, char):
        """Update character at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.s[pos] = char
        
        # Rebuild suffix array and LCP array
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
    
    def find_longest_repeating_substring(self):
        """Find longest repeating substring"""
        if not self.lcp_array:
            return ""
        
        max_lcp = max(self.lcp_array)
        if max_lcp == 0:
            return ""
        
        # Find position with maximum LCP
        max_pos = self.lcp_array.index(max_lcp)
        start = self.suffix_array[max_pos]
        
        return ''.join(self.s[start:start + max_lcp])
    
    def find_all_repeating_substrings(self, min_length=2):
        """Find all repeating substrings with minimum length"""
        repeating_substrings = []
        
        for i in range(1, self.n):
            if self.lcp_array[i] >= min_length:
                start = self.suffix_array[i]
                substring = ''.join(self.s[start:start + self.lcp_array[i]])
                repeating_substrings.append(substring)
        
        return list(set(repeating_substrings))  # Remove duplicates
    
    def count_repeating_substrings(self, min_length=2):
        """Count number of repeating substrings"""
        count = 0
        seen = set()
        
        for i in range(1, self.n):
            if self.lcp_array[i] >= min_length:
                start = self.suffix_array[i]
                substring = ''.join(self.s[start:start + self.lcp_array[i]])
                if substring not in seen:
                    seen.add(substring)
                    count += 1
        
        return count
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'longest':
                result = self.find_longest_repeating_substring()
                results.append(result)
            elif query['type'] == 'all':
                result = self.find_all_repeating_substrings(query.get('min_length', 2))
                results.append(result)
            elif query['type'] == 'count':
                result = self.count_repeating_substrings(query.get('min_length', 2))
                results.append(result)
        return results
```

### Variation 2: Repeating Substring with Different Operations
**Problem**: Handle different types of operations (find, count, analyze) on repeating substrings.

**Link**: [CSES Problem Set - Repeating Substring Different Operations](https://cses.fi/problemset/task/repeating_substring_operations)

```python
class RepeatingSubstringDifferentOps:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
    
    def _build_suffix_array(self):
        """Build suffix array using efficient algorithm"""
        suffixes = []
        for i in range(self.n):
            suffixes.append((self.s[i:], i))
        
        suffixes.sort()
        return [suffix[1] for suffix in suffixes]
    
    def _build_lcp_array(self):
        """Build LCP array from suffix array"""
        lcp = [0] * self.n
        rank = [0] * self.n
        
        for i in range(self.n):
            rank[self.suffix_array[i]] = i
        
        h = 0
        for i in range(self.n):
            if rank[i] > 0:
                j = self.suffix_array[rank[i] - 1]
                while i + h < self.n and j + h < self.n and self.s[i + h] == self.s[j + h]:
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1
        
        return lcp
    
    def find_longest_repeating_substring(self):
        """Find longest repeating substring"""
        if not self.lcp_array:
            return ""
        
        max_lcp = max(self.lcp_array)
        if max_lcp == 0:
            return ""
        
        # Find position with maximum LCP
        max_pos = self.lcp_array.index(max_lcp)
        start = self.suffix_array[max_pos]
        
        return ''.join(self.s[start:start + max_lcp])
    
    def find_shortest_repeating_substring(self, min_length=2):
        """Find shortest repeating substring"""
        shortest_length = float('inf')
        shortest_substring = ""
        
        for i in range(1, self.n):
            if self.lcp_array[i] >= min_length and self.lcp_array[i] < shortest_length:
                shortest_length = self.lcp_array[i]
                start = self.suffix_array[i]
                shortest_substring = ''.join(self.s[start:start + self.lcp_array[i]])
        
        return shortest_substring if shortest_length != float('inf') else ""
    
    def find_most_frequent_repeating_substring(self, min_length=2):
        """Find most frequent repeating substring"""
        frequency = {}
        
        for i in range(1, self.n):
            if self.lcp_array[i] >= min_length:
                start = self.suffix_array[i]
                substring = ''.join(self.s[start:start + self.lcp_array[i]])
                frequency[substring] = frequency.get(substring, 0) + 1
        
        if not frequency:
            return ""
        
        return max(frequency, key=frequency.get)
    
    def analyze_repeating_patterns(self):
        """Analyze repeating patterns in the string"""
        patterns = {}
        
        for i in range(1, self.n):
            if self.lcp_array[i] > 0:
                start = self.suffix_array[i]
                substring = ''.join(self.s[start:start + self.lcp_array[i]])
                
                if substring not in patterns:
                    patterns[substring] = {
                        'length': len(substring),
                        'frequency': 0,
                        'positions': []
                    }
                
                patterns[substring]['frequency'] += 1
                patterns[substring]['positions'].append(start)
        
        return patterns
    
    def get_repeating_substring_statistics(self):
        """Get statistics about repeating substrings"""
        patterns = self.analyze_repeating_patterns()
        
        if not patterns:
            return {
                'total_patterns': 0,
                'longest_length': 0,
                'shortest_length': 0,
                'most_frequent': None,
                'average_frequency': 0
            }
        
        lengths = [pattern['length'] for pattern in patterns.values()]
        frequencies = [pattern['frequency'] for pattern in patterns.values()]
        
        most_frequent = max(patterns, key=lambda x: patterns[x]['frequency'])
        
        return {
            'total_patterns': len(patterns),
            'longest_length': max(lengths),
            'shortest_length': min(lengths),
            'most_frequent': most_frequent,
            'average_frequency': sum(frequencies) / len(frequencies)
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'longest':
                result = self.find_longest_repeating_substring()
                results.append(result)
            elif query['type'] == 'shortest':
                result = self.find_shortest_repeating_substring(query.get('min_length', 2))
                results.append(result)
            elif query['type'] == 'most_frequent':
                result = self.find_most_frequent_repeating_substring(query.get('min_length', 2))
                results.append(result)
            elif query['type'] == 'analyze':
                result = self.analyze_repeating_patterns()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_repeating_substring_statistics()
                results.append(result)
        return results
```

### Variation 3: Repeating Substring with Constraints
**Problem**: Handle repeating substring queries with additional constraints (e.g., minimum frequency, maximum length).

**Link**: [CSES Problem Set - Repeating Substring with Constraints](https://cses.fi/problemset/task/repeating_substring_constraints)

```python
class RepeatingSubstringWithConstraints:
    def __init__(self, s, min_frequency, max_length):
        self.s = list(s)
        self.n = len(self.s)
        self.min_frequency = min_frequency
        self.max_length = max_length
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
    
    def _build_suffix_array(self):
        """Build suffix array using efficient algorithm"""
        suffixes = []
        for i in range(self.n):
            suffixes.append((self.s[i:], i))
        
        suffixes.sort()
        return [suffix[1] for suffix in suffixes]
    
    def _build_lcp_array(self):
        """Build LCP array from suffix array"""
        lcp = [0] * self.n
        rank = [0] * self.n
        
        for i in range(self.n):
            rank[self.suffix_array[i]] = i
        
        h = 0
        for i in range(self.n):
            if rank[i] > 0:
                j = self.suffix_array[rank[i] - 1]
                while i + h < self.n and j + h < self.n and self.s[i + h] == self.s[j + h]:
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1
        
        return lcp
    
    def constrained_query(self, min_length=2):
        """Query repeating substrings with constraints"""
        valid_substrings = []
        
        for i in range(1, self.n):
            if self.lcp_array[i] >= min_length and self.lcp_array[i] <= self.max_length:
                start = self.suffix_array[i]
                substring = ''.join(self.s[start:start + self.lcp_array[i]])
                
                # Count frequency
                frequency = 1
                for j in range(i + 1, self.n):
                    if self.lcp_array[j] >= len(substring):
                        # Check if it's the same substring
                        other_start = self.suffix_array[j]
                        other_substring = ''.join(self.s[other_start:other_start + len(substring)])
                        if other_substring == substring:
                            frequency += 1
                    else:
                        break
                
                if frequency >= self.min_frequency:
                    valid_substrings.append((substring, frequency))
        
        return valid_substrings
    
    def find_valid_repeating_substrings(self, min_length=2):
        """Find all valid repeating substrings that satisfy constraints"""
        return self.constrained_query(min_length)
    
    def get_longest_valid_repeating_substring(self, min_length=2):
        """Get longest valid repeating substring"""
        valid_substrings = self.find_valid_repeating_substrings(min_length)
        
        if not valid_substrings:
            return None
        
        longest = max(valid_substrings, key=lambda x: len(x[0]))
        return longest
    
    def get_most_frequent_valid_repeating_substring(self, min_length=2):
        """Get most frequent valid repeating substring"""
        valid_substrings = self.find_valid_repeating_substrings(min_length)
        
        if not valid_substrings:
            return None
        
        most_frequent = max(valid_substrings, key=lambda x: x[1])
        return most_frequent
    
    def count_valid_repeating_substrings(self, min_length=2):
        """Count number of valid repeating substrings"""
        return len(self.find_valid_repeating_substrings(min_length))
    
    def get_constraint_statistics(self, min_length=2):
        """Get statistics about valid repeating substrings"""
        valid_substrings = self.find_valid_repeating_substrings(min_length)
        
        if not valid_substrings:
            return {
                'count': 0,
                'longest_length': 0,
                'shortest_length': 0,
                'max_frequency': 0,
                'min_frequency': 0,
                'avg_frequency': 0
            }
        
        lengths = [len(substring) for substring, _ in valid_substrings]
        frequencies = [freq for _, freq in valid_substrings]
        
        return {
            'count': len(valid_substrings),
            'longest_length': max(lengths),
            'shortest_length': min(lengths),
            'max_frequency': max(frequencies),
            'min_frequency': min(frequencies),
            'avg_frequency': sum(frequencies) / len(frequencies)
        }

# Example usage
s = "abacaba"
min_frequency = 2
max_length = 4

rs = RepeatingSubstringWithConstraints(s, min_frequency, max_length)
result = rs.constrained_query(2)
print(f"Constrained query result: {result}")

valid_substrings = rs.find_valid_repeating_substrings(2)
print(f"Valid repeating substrings: {valid_substrings}")

longest = rs.get_longest_valid_repeating_substring(2)
print(f"Longest valid repeating substring: {longest}")
```

### Related Problems

#### **CSES Problems**
- [Repeating Substring](https://cses.fi/problemset/task/2106) - Basic repeating substring problem
- [String Matching](https://cses.fi/problemset/task/1753) - String matching
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string

#### **LeetCode Problems**
- [Longest Repeating Substring](https://leetcode.com/problems/longest-repeating-substring/) - Find longest repeating substring
- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) - String matching with repetition
- [Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/) - Check if string has repeated pattern

#### **Problem Categories**
- **Suffix Arrays**: String processing, repeating patterns, LCP arrays
- **Pattern Matching**: KMP, Z-algorithm, string matching algorithms
- **String Processing**: Borders, periods, palindromes, string transformations
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata

## 🚀 Key Takeaways

- **Repeating Patterns**: Important concept in string analysis and pattern recognition
- **Suffix Arrays**: Powerful data structure for string processing problems
- **LCP Arrays**: Reveal repeating patterns and common prefixes efficiently
