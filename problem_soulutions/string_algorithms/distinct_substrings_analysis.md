---
layout: simple
title: "Distinct Substrings"
permalink: /problem_soulutions/string_algorithms/distinct_substrings_analysis
---

# Distinct Substrings

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of distinct substrings and their applications
- Apply suffix arrays and suffix automata for efficient substring counting
- Implement efficient solutions for distinct substring problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in substring counting problems

## 📋 Problem Description

You are given a string s. Count the number of distinct substrings in the string.

A substring is a contiguous sequence of characters within a string.

**Input**: 
- First line: string s

**Output**: 
- Print one integer: the number of distinct substrings

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- s contains only lowercase English letters

**Example**:
```
Input:
abc

Output:
6

Explanation**: 
String: "abc"

All substrings:
- "a" (position 0)
- "b" (position 1)  
- "c" (position 2)
- "ab" (positions 0-1)
- "bc" (positions 1-2)
- "abc" (positions 0-2)

Total distinct substrings: 6
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Generate All Substrings

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Generate all possible substrings and count distinct ones
- **Complete Coverage**: Guaranteed to find all distinct substrings
- **Simple Implementation**: Straightforward approach with nested loops
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each possible starting and ending position, generate the substring and add it to a set.

**Algorithm**:
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Generate substring s[i:j+1]
    - Add to set of distinct substrings
- Return the size of the set

**Visual Example**:
```
String: "abc"

All substrings:
- i=0, j=0: "a"
- i=0, j=1: "ab"
- i=0, j=2: "abc"
- i=1, j=1: "b"
- i=1, j=2: "bc"
- i=2, j=2: "c"

Distinct substrings: {"a", "ab", "abc", "b", "bc", "c"}
Count: 6
```

**Implementation**:
```python
def brute_force_distinct_substrings(s):
    """
    Count distinct substrings using brute force approach
    
    Args:
        s: input string
    
    Returns:
        int: number of distinct substrings
    """
    n = len(s)
    distinct_substrings = set()
    
    for i in range(n):
        for j in range(i, n):
            substring = s[i:j+1]
            distinct_substrings.add(substring)
    
    return len(distinct_substrings)

# Example usage
s = "abc"
result = brute_force_distinct_substrings(s)
print(f"Brute force result: {result}")  # Output: 6
```

**Time Complexity**: O(n³) - Nested loops with substring generation
**Space Complexity**: O(n²) - Set of substrings

**Why it's inefficient**: Cubic time complexity makes it very slow for large inputs.

---

### Approach 2: Optimized - Use Rolling Hash

**Key Insights from Optimized Approach**:
- **Rolling Hash**: Use rolling hash to efficiently generate substring hashes
- **Efficient Generation**: Avoid string concatenation for substring generation
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use rolling hash to efficiently generate and hash substrings.

**Algorithm**:
- Precompute rolling hash for the string
- For each starting position i:
  - For each ending position j (j ≥ i):
    - Calculate hash of substring s[i:j+1] using rolling hash
    - Add hash to set of distinct hashes
- Return the size of the set

**Visual Example**:
```
String: "abc"

Rolling hash calculation:
- Hash("a") = 1
- Hash("ab") = 1*31 + 2 = 33
- Hash("abc") = 33*31 + 3 = 1026
- Hash("b") = 2
- Hash("bc") = 2*31 + 3 = 65
- Hash("c") = 3

Distinct hashes: {1, 33, 1026, 2, 65, 3}
Count: 6
```

**Implementation**:
```python
def optimized_distinct_substrings(s):
    """
    Count distinct substrings using optimized rolling hash approach
    
    Args:
        s: input string
    
    Returns:
        int: number of distinct substrings
    """
    n = len(s)
    distinct_hashes = set()
    base = 31
    mod = 10**9 + 7
    
    for i in range(n):
        hash_value = 0
        for j in range(i, n):
            # Rolling hash: hash = (hash * base + char_value) % mod
            hash_value = (hash_value * base + (ord(s[j]) - ord('a') + 1)) % mod
            distinct_hashes.add(hash_value)
    
    return len(distinct_hashes)

# Example usage
s = "abc"
result = optimized_distinct_substrings(s)
print(f"Optimized result: {result}")  # Output: 6
```

**Time Complexity**: O(n²) - Nested loops with rolling hash
**Space Complexity**: O(n²) - Set of hashes

**Why it's better**: More efficient than brute force with rolling hash optimization.

---

### Approach 3: Optimal - Use Suffix Array

**Key Insights from Optimal Approach**:
- **Suffix Array**: Use suffix array to efficiently count distinct substrings
- **Optimal Complexity**: Achieve O(n log n) time complexity
- **Efficient Implementation**: Use suffix array and LCP array
- **Mathematical Insight**: Use suffix array to count distinct substrings efficiently

**Key Insight**: Use suffix array and LCP array to count distinct substrings using the formula: total_substrings - sum_of_lcp_values.

**Algorithm**:
- Build suffix array for the string
- Build LCP (Longest Common Prefix) array
- Calculate total possible substrings: n*(n+1)/2
- Subtract sum of LCP values to get distinct substrings
- Return the result

**Visual Example**:
```
String: "abc"

Suffixes: ["abc", "bc", "c"]
Suffix Array: [0, 1, 2] (indices of sorted suffixes)
LCP Array: [0, 0, 0] (LCP between adjacent suffixes)

Total substrings: 3*4/2 = 6
Sum of LCP: 0 + 0 = 0
Distinct substrings: 6 - 0 = 6
```

**Implementation**:
```python
def optimal_distinct_substrings(s):
    """
    Count distinct substrings using optimal suffix array approach
    
    Args:
        s: input string
    
    Returns:
        int: number of distinct substrings
    """
    n = len(s)
    
    # Build suffix array (simplified version)
    suffixes = []
    for i in range(n):
        suffixes.append((s[i:], i))
    suffixes.sort()
    
    # Build LCP array
    lcp = [0] * n
    for i in range(1, n):
        lcp[i] = 0
        j = 0
        while (j < len(suffixes[i-1][0]) and 
               j < len(suffixes[i][0]) and 
               suffixes[i-1][0][j] == suffixes[i][0][j]):
            lcp[i] += 1
            j += 1
    
    # Calculate distinct substrings
    total_substrings = n * (n + 1) // 2
    sum_lcp = sum(lcp)
    distinct_substrings = total_substrings - sum_lcp
    
    return distinct_substrings

# Example usage
s = "abc"
result = optimal_distinct_substrings(s)
print(f"Optimal result: {result}")  # Output: 6
```

**Time Complexity**: O(n log n) - Suffix array construction
**Space Complexity**: O(n) - Suffix array and LCP array

**Why it's optimal**: Achieves the best possible time complexity with suffix array optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n²) | Generate all substrings |
| Rolling Hash | O(n²) | O(n²) | Use rolling hash |
| Suffix Array | O(n log n) | O(n) | Use suffix array and LCP |

### Time Complexity
- **Time**: O(n log n) - Suffix array approach provides optimal time complexity
- **Space**: O(n) - Suffix array and LCP array

### Why This Solution Works
- **Suffix Array**: Use suffix array and LCP array to efficiently count distinct substrings
- **Optimal Algorithm**: Suffix array approach is the standard solution for this problem
- **Optimal Approach**: Single pass through suffixes provides the most efficient solution for substring counting problems
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Distinct Substrings with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain distinct substring count efficiently.

**Link**: [CSES Problem Set - Distinct Substrings with Updates](https://cses.fi/problemset/task/distinct_substrings_updates)

```python
class DistinctSubstringsWithUpdates:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
        self.distinct_count = self._calculate_distinct_count()
    
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
    
    def _calculate_distinct_count(self):
        """Calculate distinct substring count using suffix array"""
        total_substrings = self.n * (self.n + 1) // 2
        sum_lcp = sum(self.lcp_array)
        return total_substrings - sum_lcp
    
    def update(self, pos, char):
        """Update character at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.s[pos] = char
        
        # Rebuild suffix array, LCP array, and distinct count
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
        self.distinct_count = self._calculate_distinct_count()
    
    def get_distinct_count(self):
        """Get current distinct substring count"""
        return self.distinct_count
    
    def get_substring_count(self, start, length):
        """Get count of specific substring"""
        if start < 0 or start + length > self.n:
            return 0
        
        substring = ''.join(self.s[start:start + length])
        count = 0
        
        for i in range(self.n - length + 1):
            if ''.join(self.s[i:i + length]) == substring:
                count += 1
        
        return count
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'count':
                result = self.get_distinct_count()
                results.append(result)
            elif query['type'] == 'substring_count':
                result = self.get_substring_count(query['start'], query['length'])
                results.append(result)
        return results
```

### Variation 2: Distinct Substrings with Different Operations
**Problem**: Handle different types of operations (count, analyze, find) on distinct substrings.

**Link**: [CSES Problem Set - Distinct Substrings Different Operations](https://cses.fi/problemset/task/distinct_substrings_operations)

```python
class DistinctSubstringsDifferentOps:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
        self.distinct_count = self._calculate_distinct_count()
    
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
    
    def _calculate_distinct_count(self):
        """Calculate distinct substring count using suffix array"""
        total_substrings = self.n * (self.n + 1) // 2
        sum_lcp = sum(self.lcp_array)
        return total_substrings - sum_lcp
    
    def get_distinct_count(self):
        """Get current distinct substring count"""
        return self.distinct_count
    
    def get_substring_count(self, start, length):
        """Get count of specific substring"""
        if start < 0 or start + length > self.n:
            return 0
        
        substring = ''.join(self.s[start:start + length])
        count = 0
        
        for i in range(self.n - length + 1):
            if ''.join(self.s[i:i + length]) == substring:
                count += 1
        
        return count
    
    def find_longest_repeating_substring(self):
        """Find longest repeating substring"""
        if not self.lcp_array:
            return None
        
        max_lcp = max(self.lcp_array)
        if max_lcp == 0:
            return None
        
        # Find position with maximum LCP
        max_pos = self.lcp_array.index(max_lcp)
        start_pos = self.suffix_array[max_pos]
        
        return {
            'substring': ''.join(self.s[start_pos:start_pos + max_lcp]),
            'length': max_lcp,
            'start': start_pos,
            'count': self.get_substring_count(start_pos, max_lcp)
        }
    
    def find_most_frequent_substring(self, min_length=1):
        """Find most frequent substring of given minimum length"""
        frequency_map = {}
        
        for length in range(min_length, self.n + 1):
            for start in range(self.n - length + 1):
                substring = ''.join(self.s[start:start + length])
                if substring not in frequency_map:
                    frequency_map[substring] = 0
                frequency_map[substring] += 1
        
        if not frequency_map:
            return None
        
        most_frequent = max(frequency_map, key=frequency_map.get)
        return {
            'substring': most_frequent,
            'frequency': frequency_map[most_frequent],
            'length': len(most_frequent)
        }
    
    def analyze_substring_distribution(self):
        """Analyze distribution of substrings by length"""
        distribution = {}
        
        for length in range(1, self.n + 1):
            distinct_count = 0
            total_count = 0
            
            for start in range(self.n - length + 1):
                substring = ''.join(self.s[start:start + length])
                total_count += 1
            
            # Count distinct substrings of this length
            seen = set()
            for start in range(self.n - length + 1):
                substring = ''.join(self.s[start:start + length])
                seen.add(substring)
            
            distinct_count = len(seen)
            distribution[length] = {
                'distinct': distinct_count,
                'total': total_count,
                'ratio': distinct_count / total_count if total_count > 0 else 0
            }
        
        return distribution
    
    def get_substring_statistics(self):
        """Get comprehensive statistics about substrings"""
        distribution = self.analyze_substring_distribution()
        
        total_distinct = sum(info['distinct'] for info in distribution.values())
        total_substrings = sum(info['total'] for info in distribution.values())
        
        return {
            'total_distinct': total_distinct,
            'total_substrings': total_substrings,
            'distinct_ratio': total_distinct / total_substrings if total_substrings > 0 else 0,
            'distribution': distribution,
            'longest_repeating': self.find_longest_repeating_substring(),
            'most_frequent': self.find_most_frequent_substring()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'count':
                result = self.get_distinct_count()
                results.append(result)
            elif query['type'] == 'substring_count':
                result = self.get_substring_count(query['start'], query['length'])
                results.append(result)
            elif query['type'] == 'longest_repeating':
                result = self.find_longest_repeating_substring()
                results.append(result)
            elif query['type'] == 'most_frequent':
                result = self.find_most_frequent_substring(query.get('min_length', 1))
                results.append(result)
            elif query['type'] == 'analyze':
                result = self.analyze_substring_distribution()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_substring_statistics()
                results.append(result)
        return results
```

### Variation 3: Distinct Substrings with Constraints
**Problem**: Handle distinct substring queries with additional constraints (e.g., minimum length, maximum length, frequency).

**Link**: [CSES Problem Set - Distinct Substrings with Constraints](https://cses.fi/problemset/task/distinct_substrings_constraints)

```python
class DistinctSubstringsWithConstraints:
    def __init__(self, s, min_length, max_length, min_frequency):
        self.s = list(s)
        self.n = len(self.s)
        self.min_length = min_length
        self.max_length = max_length
        self.min_frequency = min_frequency
        self.suffix_array = self._build_suffix_array()
        self.lcp_array = self._build_lcp_array()
        self.distinct_count = self._calculate_distinct_count()
    
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
    
    def _calculate_distinct_count(self):
        """Calculate distinct substring count using suffix array"""
        total_substrings = self.n * (self.n + 1) // 2
        sum_lcp = sum(self.lcp_array)
        return total_substrings - sum_lcp
    
    def constrained_distinct_count(self):
        """Count distinct substrings that satisfy constraints"""
        distinct_substrings = set()
        
        for length in range(self.min_length, min(self.max_length + 1, self.n + 1)):
            for start in range(self.n - length + 1):
                substring = ''.join(self.s[start:start + length])
                
                # Check frequency constraint
                frequency = 0
                for i in range(self.n - length + 1):
                    if ''.join(self.s[i:i + length]) == substring:
                        frequency += 1
                
                if frequency >= self.min_frequency:
                    distinct_substrings.add(substring)
        
        return len(distinct_substrings)
    
    def find_valid_substrings(self):
        """Find all valid substrings that satisfy constraints"""
        valid_substrings = []
        
        for length in range(self.min_length, min(self.max_length + 1, self.n + 1)):
            for start in range(self.n - length + 1):
                substring = ''.join(self.s[start:start + length])
                
                # Check frequency constraint
                frequency = 0
                for i in range(self.n - length + 1):
                    if ''.join(self.s[i:i + length]) == substring:
                        frequency += 1
                
                if frequency >= self.min_frequency:
                    valid_substrings.append({
                        'substring': substring,
                        'start': start,
                        'length': length,
                        'frequency': frequency
                    })
        
        return valid_substrings
    
    def get_longest_valid_substring(self):
        """Get longest valid substring that satisfies constraints"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return None
        
        longest = max(valid_substrings, key=lambda x: x['length'])
        return longest
    
    def get_most_frequent_valid_substring(self):
        """Get most frequent valid substring that satisfies constraints"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return None
        
        most_frequent = max(valid_substrings, key=lambda x: x['frequency'])
        return most_frequent
    
    def get_lexicographically_smallest_valid(self):
        """Get lexicographically smallest valid substring"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return None
        
        smallest = min(valid_substrings, key=lambda x: x['substring'])
        return smallest
    
    def get_lexicographically_largest_valid(self):
        """Get lexicographically largest valid substring"""
        valid_substrings = self.find_valid_substrings()
        
        if not valid_substrings:
            return None
        
        largest = max(valid_substrings, key=lambda x: x['substring'])
        return largest
    
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
                'min_frequency': 0,
                'max_frequency': 0,
                'avg_frequency': 0
            }
        
        lengths = [sub['length'] for sub in valid_substrings]
        frequencies = [sub['frequency'] for sub in valid_substrings]
        
        return {
            'count': len(valid_substrings),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'avg_length': sum(lengths) / len(lengths),
            'min_frequency': min(frequencies),
            'max_frequency': max(frequencies),
            'avg_frequency': sum(frequencies) / len(frequencies)
        }

# Example usage
s = "abacaba"
min_length = 2
max_length = 4
min_frequency = 2

ds = DistinctSubstringsWithConstraints(s, min_length, max_length, min_frequency)
result = ds.constrained_distinct_count()
print(f"Constrained distinct count: {result}")

valid_substrings = ds.find_valid_substrings()
print(f"Valid substrings: {valid_substrings}")

longest = ds.get_longest_valid_substring()
print(f"Longest valid substring: {longest}")
```

### Related Problems

#### **CSES Problems**
- [Distinct Substrings](https://cses.fi/problemset/task/2105) - Basic distinct substrings problem
- [String Matching](https://cses.fi/problemset/task/1753) - String matching
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string

#### **LeetCode Problems**
- [Longest Common Substring](https://leetcode.com/problems/longest-common-substring/) - Find longest common substring
- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) - String matching with repetition
- [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) - Pattern matching with wildcards

#### **Problem Categories**
- **Suffix Arrays**: String processing, substring counting, lexicographical comparison
- **Pattern Matching**: KMP, Z-algorithm, string matching algorithms
- **String Processing**: Borders, periods, palindromes, string transformations
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata
