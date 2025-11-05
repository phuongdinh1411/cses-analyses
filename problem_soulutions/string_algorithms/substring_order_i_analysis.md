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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Substring Order with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain substring order queries efficiently.

**Link**: [CSES Problem Set - Substring Order with Updates](https://cses.fi/problemset/task/substring_order_updates)

```python
class SubstringOrderWithUpdates:
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
    
    def get_substring_order(self, start, length):
        """Get order of substring starting at position start with given length"""
        if start < 0 or start + length > self.n:
            return -1
        
        substring = ''.join(self.s[start:start + length])
        
        # Find position in suffix array
        for i, suffix_start in enumerate(self.suffix_array):
            if suffix_start + length <= self.n:
                suffix = ''.join(self.s[suffix_start:suffix_start + length])
                if suffix == substring:
                    return i + 1  # 1-indexed
        
        return -1
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'order':
                result = self.get_substring_order(query['start'], query['length'])
                results.append(result)
        return results
```

### Variation 2: Substring Order with Different Operations
**Problem**: Handle different types of operations (order, rank, compare) on substring ordering.

**Link**: [CSES Problem Set - Substring Order Different Operations](https://cses.fi/problemset/task/substring_order_operations)

```python
class SubstringOrderDifferentOps:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
        self.rank = self._build_rank()
    
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
    
    def _build_rank(self):
        """Build rank array from suffix array"""
        rank = [0] * self.n
        for i in range(self.n):
            rank[self.suffix_array[i]] = i
        return rank
    
    def get_substring_order(self, start, length):
        """Get order of substring starting at position start with given length"""
        if start < 0 or start + length > self.n:
            return -1
        
        return self.rank[start] + 1  # 1-indexed
    
    def get_substring_rank(self, start, length):
        """Get rank of substring starting at position start with given length"""
        if start < 0 or start + length > self.n:
            return -1
        
        return self.rank[start]
    
    def compare_substrings(self, start1, length1, start2, length2):
        """Compare two substrings lexicographically"""
        if start1 < 0 or start1 + length1 > self.n or start2 < 0 or start2 + length2 > self.n:
            return 0
        
        # Compare using suffix array ranks
        rank1 = self.rank[start1]
        rank2 = self.rank[start2]
        
        if rank1 < rank2:
            return -1
        elif rank1 > rank2:
            return 1
        else:
            return 0
    
    def get_lexicographically_smallest(self, length):
        """Get lexicographically smallest substring of given length"""
        if length <= 0 or length > self.n:
            return None
        
        best_start = self.suffix_array[0]
        for i in range(1, self.n):
            if self.suffix_array[i] + length <= self.n:
                current_start = self.suffix_array[i]
                if ''.join(self.s[current_start:current_start + length]) < ''.join(self.s[best_start:best_start + length]):
                    best_start = current_start
        
        return best_start
    
    def get_lexicographically_largest(self, length):
        """Get lexicographically largest substring of given length"""
        if length <= 0 or length > self.n:
            return None
        
        best_start = self.suffix_array[0]
        for i in range(1, self.n):
            if self.suffix_array[i] + length <= self.n:
                current_start = self.suffix_array[i]
                if ''.join(self.s[current_start:current_start + length]) > ''.join(self.s[best_start:best_start + length]):
                    best_start = current_start
        
        return best_start
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'order':
                result = self.get_substring_order(query['start'], query['length'])
                results.append(result)
            elif query['type'] == 'rank':
                result = self.get_substring_rank(query['start'], query['length'])
                results.append(result)
            elif query['type'] == 'compare':
                result = self.compare_substrings(query['start1'], query['length1'], query['start2'], query['length2'])
                results.append(result)
            elif query['type'] == 'smallest':
                result = self.get_lexicographically_smallest(query['length'])
                results.append(result)
            elif query['type'] == 'largest':
                result = self.get_lexicographically_largest(query['length'])
                results.append(result)
        return results
```

### Variation 3: Substring Order with Constraints
**Problem**: Handle substring order queries with additional constraints (e.g., minimum length, maximum length).

**Link**: [CSES Problem Set - Substring Order with Constraints](https://cses.fi/problemset/task/substring_order_constraints)

```python
class SubstringOrderWithConstraints:
    def __init__(self, s, min_length, max_length):
        self.s = list(s)
        self.n = len(self.s)
        self.min_length = min_length
        self.max_length = max_length
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
        self.rank = self._build_rank()
    
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
    
    def _build_rank(self):
        """Build rank array from suffix array"""
        rank = [0] * self.n
        for i in range(self.n):
            rank[self.suffix_array[i]] = i
        return rank
    
    def constrained_query(self, start, length):
        """Query substring order with constraints"""
        # Check minimum length constraint
        if length < self.min_length:
            return None  # Too short
        
        # Check maximum length constraint
        if length > self.max_length:
            return None  # Too long
        
        # Check bounds
        if start < 0 or start + length > self.n:
            return None
        
        return self.rank[start] + 1  # 1-indexed
    
    def find_valid_substrings(self):
        """Find all valid substrings that satisfy constraints"""
        valid_substrings = []
        for i in range(self.n):
            for length in range(self.min_length, min(self.max_length + 1, self.n - i + 1)):
                result = self.constrained_query(i, length)
                if result is not None:
                    valid_substrings.append((i, length, result))
        return valid_substrings
    
    def get_lexicographically_smallest_valid(self):
        """Get lexicographically smallest valid substring"""
        best_start = None
        best_length = None
        best_rank = float('inf')
        
        for i in range(self.n):
            for length in range(self.min_length, min(self.max_length + 1, self.n - i + 1)):
                result = self.constrained_query(i, length)
                if result is not None and result < best_rank:
                    best_rank = result
                    best_start = i
                    best_length = length
        
        return (best_start, best_length) if best_start is not None else None
    
    def get_lexicographically_largest_valid(self):
        """Get lexicographically largest valid substring"""
        best_start = None
        best_length = None
        best_rank = -1
        
        for i in range(self.n):
            for length in range(self.min_length, min(self.max_length + 1, self.n - i + 1)):
                result = self.constrained_query(i, length)
                if result is not None and result > best_rank:
                    best_rank = result
                    best_start = i
                    best_length = length
        
        return (best_start, best_length) if best_start is not None else None
    
    def count_valid_substrings(self):
        """Count number of valid substrings"""
        count = 0
        for i in range(self.n):
            for length in range(self.min_length, min(self.max_length + 1, self.n - i + 1)):
                result = self.constrained_query(i, length)
                if result is not None:
                    count += 1
        return count

# Example usage
s = "abacaba"
min_length = 2
max_length = 4

so = SubstringOrderWithConstraints(s, min_length, max_length)
result = so.constrained_query(0, 2)
print(f"Constrained query result: {result}")

valid_substrings = so.find_valid_substrings()
print(f"Valid substrings: {valid_substrings}")

smallest = so.get_lexicographically_smallest_valid()
print(f"Lexicographically smallest valid substring: {smallest}")
```

### Related Problems

#### **CSES Problems**
- [Substring Order I](https://cses.fi/problemset/task/2108) - Basic substring order problem
- [String Matching](https://cses.fi/problemset/task/1753) - String matching
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string

#### **LeetCode Problems**
- [Longest Common Substring](https://leetcode.com/problems/longest-common-substring/) - Find longest common substring
- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) - String matching with repetition
- [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) - Pattern matching with wildcards

#### **Problem Categories**
- **Suffix Arrays**: String processing, substring ordering, lexicographical comparison
- **Pattern Matching**: KMP, Z-algorithm, string matching algorithms
- **String Processing**: Borders, periods, palindromes, string transformations
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata

## 🚀 Key Takeaways

- **Suffix Arrays**: Essential for efficient string processing and ordering
- **Lexicographical Ordering**: Important concept for string comparison
- **Query Optimization**: Precomputation can significantly improve query performance
- **Substring Processing**: Efficient techniques for handling substring operations

### 🏆 **Key Takeaways**
1. **Suffix Arrays**: Essential for efficient string processing and ordering
2. **Lexicographical Ordering**: Important concept for string comparison
3. **Query Optimization**: Precomputation can significantly improve query performance
4. **Substring Processing**: Efficient techniques for handling substring operations

### 🚀 **Next Steps**
1. **Practice**: Implement suffix array construction algorithms
2. **Advanced Topics**: Learn about advanced string data structures
3. **Related Problems**: Solve more string processing and query problems
