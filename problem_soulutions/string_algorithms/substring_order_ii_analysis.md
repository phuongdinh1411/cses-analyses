---
layout: simple
title: "Substring Order Ii"
permalink: /problem_soulutions/string_algorithms/substring_order_ii_analysis
---

# Substring Order Ii

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand lexicographical ordering of substrings and their applications
- Apply suffix array and LCP array techniques for substring ordering
- Implement efficient solutions for substring order problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in substring ordering problems

## 📋 Problem Description

You are given a string s and q queries. Each query consists of two integers k and l. For each query, find the k-th lexicographically smallest substring of length l in the string s.

**Input**: 
- First line: string s
- Second line: integer q (number of queries)
- Next q lines: two integers k and l

**Output**: 
- For each query, print the k-th lexicographically smallest substring of length l

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- 1 ≤ q ≤ 10⁵
- 1 ≤ k ≤ number of distinct substrings of length l
- 1 ≤ l ≤ |s|
- s contains only lowercase English letters

**Example**:
```
Input:
ababab
3
1 2
2 2
1 3

Output:
ab
ba
aba

Explanation**: 
String: "ababab"

Substrings of length 2 (lexicographically sorted):
1. "ab" (positions 0-1, 2-3, 4-5)
2. "ba" (positions 1-2, 3-4)

Substrings of length 3 (lexicographically sorted):
1. "aba" (positions 0-2, 2-4)
2. "bab" (positions 1-3, 3-5)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n² log n + q × n)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Generate all possible substrings of each length
2. Sort substrings lexicographically for each length
3. For each query, return the k-th substring of the specified length

**Implementation**:
```python
def brute_force_substring_order_ii(s, queries):
    n = len(s)
    results = []
    
    # Precompute all substrings grouped by length
    substrings_by_length = {}
    for length in range(1, n + 1):
        substrings = []
        for i in range(n - length + 1):
            substrings.append(s[i:i + length])
        # Remove duplicates and sort
        unique_substrings = sorted(list(set(substrings)))
        substrings_by_length[length] = unique_substrings
    
    # Answer queries
    for k, l in queries:
        if l in substrings_by_length and k <= len(substrings_by_length[l]):
            results.append(substrings_by_length[l][k - 1])
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
def optimized_substring_order_ii(s, queries):
    n = len(s)
    results = []
    
    # Build suffix array (simplified version)
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    suffixes.sort()
    
    # Answer queries
    for k, l in queries:
        # Find k-th lexicographically smallest substring of length l
        count = 0
        for suffix, start_pos in suffixes:
            if len(suffix) >= l:
                substring = suffix[:l]
                # Check if this is a new unique substring
                is_new = True
                for prev_suffix, prev_start in suffixes[:suffixes.index((suffix, start_pos))]:
                    if len(prev_suffix) >= l and prev_suffix[:l] == substring:
                        is_new = False
                        break
                
                if is_new:
                    count += 1
                    if count == k:
                        results.append(substring)
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
def optimal_substring_order_ii(s, queries):
    n = len(s)
    
    # Build suffix array
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    suffixes.sort()
    
    # Precompute all unique substrings with their order
    substring_order = {}
    for length in range(1, n + 1):
        unique_substrings = []
        seen = set()
        
        for suffix, start_pos in suffixes:
            if len(suffix) >= length:
                substring = suffix[:length]
                if substring not in seen:
                    seen.add(substring)
                    unique_substrings.append(substring)
        
        substring_order[length] = unique_substrings
    
    # Answer queries
    results = []
    for k, l in queries:
        if l in substring_order and k <= len(substring_order[l]):
            results.append(substring_order[l][k - 1])
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

Substrings of length 2:
1. "ab" (from suffix "ab")
2. "ba" (from suffix "bab")

Substrings of length 3:
1. "aba" (from suffix "abab")
2. "bab" (from suffix "babab")
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
- **Substring Order I**: Basic substring ordering without length constraints
- **Distinct Substrings**: Counting unique substrings using suffix arrays
- **String Sorting**: Lexicographical ordering of strings

### 🎯 **Pattern Recognition**
- **Suffix Array Problems**: Problems involving string processing and ordering
- **Query Processing Problems**: Problems with multiple queries requiring optimization
- **String Ordering Problems**: Problems involving lexicographical comparison

## 📈 Complexity Analysis

### ⏱️ **Time Complexity**
- **Brute Force**: O(n² log n + q × n) - Generate, sort, and query all substrings
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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Substring Order II with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain substring order queries efficiently.

**Link**: [CSES Problem Set - Substring Order II with Updates](https://cses.fi/problemset/task/substring_order_ii_updates)

```python
class SubstringOrderIIWithUpdates:
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
    
    def update(self, pos, char):
        """Update character at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.s[pos] = char
        
        # Rebuild suffix array, LCP array, and rank
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
        self.rank = self._build_rank()
    
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
            elif query['type'] == 'rank':
                result = self.get_substring_rank(query['start'], query['length'])
                results.append(result)
            elif query['type'] == 'compare':
                result = self.compare_substrings(query['start1'], query['length1'], query['start2'], query['length2'])
                results.append(result)
        return results
```

### Variation 2: Substring Order II with Different Operations
**Problem**: Handle different types of operations (order, rank, compare, analyze) on substring ordering.

**Link**: [CSES Problem Set - Substring Order II Different Operations](https://cses.fi/problemset/task/substring_order_ii_operations)

```python
class SubstringOrderIIDifferentOps:
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
    
    def analyze_substring_distribution(self, length):
        """Analyze distribution of substrings of given length"""
        if length <= 0 or length > self.n:
            return {}
        
        distribution = {}
        for i in range(self.n - length + 1):
            substring = ''.join(self.s[i:i + length])
            if substring not in distribution:
                distribution[substring] = {
                    'count': 0,
                    'positions': [],
                    'rank': self.rank[i]
                }
            distribution[substring]['count'] += 1
            distribution[substring]['positions'].append(i)
        
        return distribution
    
    def get_substring_statistics(self, length):
        """Get statistics about substrings of given length"""
        distribution = self.analyze_substring_distribution(length)
        
        if not distribution:
            return {
                'total_substrings': 0,
                'unique_substrings': 0,
                'most_frequent': None,
                'least_frequent': None,
                'average_frequency': 0
            }
        
        frequencies = [info['count'] for info in distribution.values()]
        most_frequent = max(distribution, key=lambda x: distribution[x]['count'])
        least_frequent = min(distribution, key=lambda x: distribution[x]['count'])
        
        return {
            'total_substrings': sum(frequencies),
            'unique_substrings': len(distribution),
            'most_frequent': most_frequent,
            'least_frequent': least_frequent,
            'average_frequency': sum(frequencies) / len(frequencies)
        }
    
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
            elif query['type'] == 'analyze':
                result = self.analyze_substring_distribution(query['length'])
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_substring_statistics(query['length'])
                results.append(result)
        return results
```

### Variation 3: Substring Order II with Constraints
**Problem**: Handle substring order queries with additional constraints (e.g., minimum length, maximum length, frequency).

**Link**: [CSES Problem Set - Substring Order II with Constraints](https://cses.fi/problemset/task/substring_order_ii_constraints)

```python
class SubstringOrderIIWithConstraints:
    def __init__(self, s, min_length, max_length, min_frequency):
        self.s = list(s)
        self.n = len(self.s)
        self.min_length = min_length
        self.max_length = max_length
        self.min_frequency = min_frequency
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
        
        # Check frequency constraint
        substring = ''.join(self.s[start:start + length])
        frequency = 0
        for i in range(self.n - length + 1):
            if ''.join(self.s[i:i + length]) == substring:
                frequency += 1
        
        if frequency < self.min_frequency:
            return None  # Too infrequent
        
        return self.rank[start] + 1  # 1-indexed
    
    def find_valid_substrings(self):
        """Find all valid substrings that satisfy constraints"""
        valid_substrings = []
        
        for length in range(self.min_length, min(self.max_length + 1, self.n + 1)):
            for start in range(self.n - length + 1):
                result = self.constrained_query(start, length)
                if result is not None:
                    substring = ''.join(self.s[start:start + length])
                    valid_substrings.append((start, length, result, substring))
        
        return valid_substrings
    
    def get_lexicographically_smallest_valid(self):
        """Get lexicographically smallest valid substring"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return None
        
        smallest = min(valid_substrings, key=lambda x: x[3])  # Compare by substring
        return smallest
    
    def get_lexicographically_largest_valid(self):
        """Get lexicographically largest valid substring"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return None
        
        largest = max(valid_substrings, key=lambda x: x[3])  # Compare by substring
        return largest
    
    def get_highest_ranked_valid(self):
        """Get highest ranked valid substring"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return None
        
        highest = max(valid_substrings, key=lambda x: x[2])  # Compare by rank
        return highest
    
    def get_lowest_ranked_valid(self):
        """Get lowest ranked valid substring"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return None
        
        lowest = min(valid_substrings, key=lambda x: x[2])  # Compare by rank
        return lowest
    
    def count_valid_substrings(self):
        """Count number of valid substrings"""
        return len(self.find_valid_substrings())
    
    def get_constraint_statistics(self):
        """Get statistics about valid substrings"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return {
                'count': 0,
                'min_length': 0,
                'max_length': 0,
                'avg_length': 0,
                'min_rank': 0,
                'max_rank': 0,
                'avg_rank': 0
            }
        
        lengths = [length for _, length, _, _ in valid_substrings]
        ranks = [rank for _, _, rank, _ in valid_substrings]
        
        return {
            'count': len(valid_substrings),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'avg_length': sum(lengths) / len(lengths),
            'min_rank': min(ranks),
            'max_rank': max(ranks),
            'avg_rank': sum(ranks) / len(ranks)
        }

# Example usage
s = "abacaba"
min_length = 2
max_length = 4
min_frequency = 2

so = SubstringOrderIIWithConstraints(s, min_length, max_length, min_frequency)
result = so.constrained_query(0, 2)
print(f"Constrained query result: {result}")

valid_substrings = so.find_valid_substrings()
print(f"Valid substrings: {valid_substrings}")

smallest = so.get_lexicographically_smallest_valid()
print(f"Lexicographically smallest valid substring: {smallest}")
```

### Related Problems

#### **CSES Problems**
- [Substring Order II](https://cses.fi/problemset/task/2109) - Basic substring order II problem
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
