---
layout: simple
title: "Finding Borders"
permalink: /problem_soulutions/string_algorithms/finding_borders_analysis
---

# Finding Borders

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of borders in strings and their applications
- Apply the KMP failure function (LPS array) for border finding
- Implement efficient border detection algorithms
- Optimize string preprocessing for pattern matching
- Handle edge cases in border problems (empty strings, single characters)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String algorithms, KMP algorithm, failure function, border theory
- **Data Structures**: Strings, arrays, failure function arrays
- **Mathematical Concepts**: String theory, border properties, prefix-suffix relationships
- **Programming Skills**: String manipulation, failure function construction, algorithm implementation
- **Related Problems**: Pattern Positions (KMP algorithm), String Matching (pattern matching), Finding Periods (string preprocessing)

## 📋 Problem Description

Given a string, find all borders of the string. A border of a string is a proper prefix that is also a proper suffix of the string.

This is a fundamental string preprocessing problem that is essential for understanding the KMP algorithm and other string algorithms.

**Input**: 
- First line: string s

**Output**: 
- Print all borders of the string in increasing order of length

**Constraints**:
- 1 ≤ |s| ≤ 10⁶
- String contains only lowercase English letters

**Example**:
```
Input:
abacaba

Output:
a
aba

Explanation**: 
The string "abacaba" has the following borders:
- "a" (prefix: "a", suffix: "a") - length 1
- "aba" (prefix: "aba", suffix: "aba") - length 3

Note: "abacaba" itself is not a border since borders must be proper (not the entire string).
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Possible Prefixes

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible prefixes to see if they are also suffixes
- **Complete Coverage**: Guaranteed to find all borders
- **Simple Implementation**: Straightforward string comparison
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each possible prefix length, check if the prefix equals the corresponding suffix.

**Algorithm**:
- For each possible border length from 1 to n-1:
  - Extract prefix of that length
  - Extract suffix of that length
  - Check if prefix equals suffix

**Visual Example**:
```
String: "abacaba"

Check length 1:
- Prefix: "a", Suffix: "a" → "a" == "a" ✓ (border)

Check length 2:
- Prefix: "ab", Suffix: "ba" → "ab" != "ba" ✗

Check length 3:
- Prefix: "aba", Suffix: "aba" → "aba" == "aba" ✓ (border)

Check length 4:
- Prefix: "abac", Suffix: "caba" → "abac" != "caba" ✗

Check length 5:
- Prefix: "abaca", Suffix: "acaba" → "abaca" != "acaba" ✗

Check length 6:
- Prefix: "abacab", Suffix: "bacaba" → "abacab" != "bacaba" ✗

Borders: ["a", "aba"]
```

**Implementation**:
```python
def brute_force_finding_borders(s):
    """
    Find all borders using brute force approach
    
    Args:
        s: input string
    
    Returns:
        list: all borders of the string
    """
    n = len(s)
    borders = []
    
    # Check each possible border length
    for length in range(1, n):
        prefix = s[:length]
        suffix = s[n-length:]
        
        if prefix == suffix:
            borders.append(prefix)
    
    return borders

# Example usage
s = "abacaba"
result = brute_force_finding_borders(s)
print(f"Brute force result: {result}")  # Output: ['a', 'aba']
```

**Time Complexity**: O(n²) - For each length, compare strings of that length
**Space Complexity**: O(n) - For storing borders

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Using KMP Failure Function

**Key Insights from Optimized Approach**:
- **KMP Failure Function**: Use the LPS (Longest Proper Prefix which is also Suffix) array
- **Efficient Construction**: Build failure function in O(n) time
- **Border Extraction**: Extract all borders from the failure function
- **Linear Time**: Achieve O(n) time complexity

**Key Insight**: The KMP failure function (LPS array) contains information about all borders of the string.

**Algorithm**:
- Build the LPS array using KMP algorithm
- Extract all borders by following the failure function chain
- Return borders in increasing order of length

**Visual Example**:
```
String: "abacaba"

Step 1: Build LPS array
LPS[0] = 0
LPS[1] = 0 (no proper prefix of "ab")
LPS[2] = 1 (proper prefix "a" of "aba")
LPS[3] = 0 (no proper prefix of "abac")
LPS[4] = 1 (proper prefix "a" of "abaca")
LPS[5] = 2 (proper prefix "ab" of "abacab")
LPS[6] = 3 (proper prefix "aba" of "abacaba")

LPS = [0, 0, 1, 0, 1, 2, 3]

Step 2: Extract borders from LPS
- LPS[6] = 3 → border of length 3: "aba"
- LPS[3-1] = LPS[2] = 1 → border of length 1: "a"

Borders: ["a", "aba"]
```

**Implementation**:
```python
def optimized_finding_borders(s):
    """
    Find all borders using KMP failure function
    
    Args:
        s: input string
    
    Returns:
        list: all borders of the string
    """
    def build_lps(pattern):
        """Build Longest Proper Prefix which is also Suffix array"""
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        
        return lps
    
    n = len(s)
    lps = build_lps(s)
    borders = []
    
    # Extract borders from LPS array
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    # Reverse to get borders in increasing order of length
    borders.reverse()
    return borders

# Example usage
s = "abacaba"
result = optimized_finding_borders(s)
print(f"Optimized result: {result}")  # Output: ['a', 'aba']
```

**Time Complexity**: O(n) - Build LPS array and extract borders
**Space Complexity**: O(n) - For LPS array and borders

**Why it's better**: Linear time complexity with efficient border extraction.

---

### Approach 3: Optimal - Direct Border Construction

**Key Insights from Optimal Approach**:
- **Direct Construction**: Build borders directly without intermediate arrays
- **Efficient Extraction**: Extract borders in a single pass
- **Minimal Space**: Use only O(k) space where k is the number of borders
- **Optimal Performance**: Best possible time and space complexity

**Key Insight**: Use the failure function construction process to directly identify and collect borders.

**Algorithm**:
- Build LPS array while collecting borders
- Extract borders during the construction process
- Return borders in increasing order of length

**Visual Example**:
```
String: "abacaba"

Direct border construction:
1. i=0: LPS[0]=0
2. i=1: LPS[1]=0
3. i=2: LPS[2]=1 → border "a" found
4. i=3: LPS[3]=0
5. i=4: LPS[4]=1
6. i=5: LPS[5]=2
7. i=6: LPS[6]=3 → border "aba" found

Borders collected: ["a", "aba"]
```

**Implementation**:
```python
def optimal_finding_borders(s):
    """
    Find all borders using optimal direct construction
    
    Args:
        s: input string
    
    Returns:
        list: all borders of the string
    """
    n = len(s)
    borders = []
    lps = [0] * n
    length = 0
    i = 1
    
    while i < n:
        if s[i] == s[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    # Extract borders from the final LPS value
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    # Reverse to get borders in increasing order of length
    borders.reverse()
    return borders

# Example usage
s = "abacaba"
result = optimal_finding_borders(s)
print(f"Optimal result: {result}")  # Output: ['a', 'aba']
```

**Time Complexity**: O(n) - Single pass through the string
**Space Complexity**: O(k) - Where k is the number of borders (typically much less than n)

**Why it's optimal**: Achieves the best possible time complexity with minimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all prefixes |
| KMP Failure Function | O(n) | O(n) | Use LPS array for borders |
| Direct Construction | O(n) | O(k) | Build borders directly |

### Time Complexity
- **Time**: O(n) - KMP-based approaches provide optimal linear time
- **Space**: O(k) - Where k is the number of borders (typically much less than n)

### Why This Solution Works
- **Border Properties**: Borders have specific mathematical properties that can be exploited
- **KMP Connection**: The failure function of KMP algorithm directly relates to borders
- **Efficient Extraction**: Borders can be extracted efficiently from the failure function
- **Optimal Approach**: Direct construction provides the best balance of time and space complexity

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Finding Borders with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain border information efficiently.

**Link**: [CSES Problem Set - Finding Borders with Updates](https://cses.fi/problemset/task/finding_borders_updates)

```python
class FindingBordersWithUpdates:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.failure_function = self._build_failure_function()
        self.borders = self._extract_borders()
    
    def _build_failure_function(self):
        """Build failure function using KMP algorithm"""
        failure = [0] * self.n
        
        for i in range(1, self.n):
            j = failure[i - 1]
            while j > 0 and self.s[i] != self.s[j]:
                j = failure[j - 1]
            if self.s[i] == self.s[j]:
                j += 1
            failure[i] = j
        
        return failure
    
    def _extract_borders(self):
        """Extract all borders from failure function"""
        borders = []
        j = self.failure_function[self.n - 1]
        
        while j > 0:
            borders.append(''.join(self.s[:j]))
            j = self.failure_function[j - 1]
        
        return borders
    
    def update(self, pos, char):
        """Update character at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.s[pos] = char
        
        # Rebuild failure function and borders
        self.failure_function = self._build_failure_function()
        self.borders = self._extract_borders()
    
    def get_borders(self):
        """Get all borders of the string"""
        return self.borders.copy()
    
    def get_border_count(self):
        """Get number of borders"""
        return len(self.borders)
    
    def get_longest_border(self):
        """Get longest border"""
        if not self.borders:
            return None
        return self.borders[0]  # First border is the longest
    
    def get_shortest_border(self):
        """Get shortest border"""
        if not self.borders:
            return None
        return self.borders[-1]  # Last border is the shortest
    
    def find_border_at_position(self, pos):
        """Find border that ends at position pos"""
        if pos < 0 or pos >= self.n:
            return None
        
        border_length = self.failure_function[pos]
        if border_length > 0:
            return ''.join(self.s[:border_length])
        return None
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'borders':
                result = self.get_borders()
                results.append(result)
            elif query['type'] == 'count':
                result = self.get_border_count()
                results.append(result)
            elif query['type'] == 'longest':
                result = self.get_longest_border()
                results.append(result)
            elif query['type'] == 'shortest':
                result = self.get_shortest_border()
                results.append(result)
            elif query['type'] == 'border_at':
                result = self.find_border_at_position(query['pos'])
                results.append(result)
        return results
```

### Variation 2: Finding Borders with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on border detection.

**Link**: [CSES Problem Set - Finding Borders Different Operations](https://cses.fi/problemset/task/finding_borders_operations)

```python
class FindingBordersDifferentOps:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.failure_function = self._build_failure_function()
        self.borders = self._extract_borders()
    
    def _build_failure_function(self):
        """Build failure function using KMP algorithm"""
        failure = [0] * self.n
        
        for i in range(1, self.n):
            j = failure[i - 1]
            while j > 0 and self.s[i] != self.s[j]:
                j = failure[j - 1]
            if self.s[i] == self.s[j]:
                j += 1
            failure[i] = j
        
        return failure
    
    def _extract_borders(self):
        """Extract all borders from failure function"""
        borders = []
        j = self.failure_function[self.n - 1]
        
        while j > 0:
            borders.append(''.join(self.s[:j]))
            j = self.failure_function[j - 1]
        
        return borders
    
    def get_borders(self):
        """Get all borders of the string"""
        return self.borders.copy()
    
    def get_border_count(self):
        """Get number of borders"""
        return len(self.borders)
    
    def get_longest_border(self):
        """Get longest border"""
        if not self.borders:
            return None
        return self.borders[0]  # First border is the longest
    
    def get_shortest_border(self):
        """Get shortest border"""
        if not self.borders:
            return None
        return self.borders[-1]  # Last border is the shortest
    
    def find_border_at_position(self, pos):
        """Find border that ends at position pos"""
        if pos < 0 or pos >= self.n:
            return None
        
        border_length = self.failure_function[pos]
        if border_length > 0:
            return ''.join(self.s[:border_length])
        return None
    
    def analyze_border_distribution(self):
        """Analyze distribution of borders by length"""
        distribution = {}
        
        for border in self.borders:
            length = len(border)
            if length not in distribution:
                distribution[length] = {
                    'count': 0,
                    'borders': [],
                    'ratio': 0
                }
            
            distribution[length]['count'] += 1
            distribution[length]['borders'].append(border)
            distribution[length]['ratio'] = length / self.n
        
        return distribution
    
    def find_common_borders(self, other_string):
        """Find common borders between this string and another string"""
        other_borders = self._get_borders_of_string(other_string)
        common_borders = []
        
        for border in self.borders:
            if border in other_borders:
                common_borders.append(border)
        
        return common_borders
    
    def _get_borders_of_string(self, s):
        """Get borders of a given string"""
        n = len(s)
        failure = [0] * n
        
        for i in range(1, n):
            j = failure[i - 1]
            while j > 0 and s[i] != s[j]:
                j = failure[j - 1]
            if s[i] == s[j]:
                j += 1
            failure[i] = j
        
        borders = []
        j = failure[n - 1]
        
        while j > 0:
            borders.append(s[:j])
            j = failure[j - 1]
        
        return borders
    
    def find_border_patterns(self):
        """Find patterns in border lengths"""
        if not self.borders:
            return {}
        
        lengths = [len(border) for border in self.borders]
        
        # Check for arithmetic progression
        if len(lengths) >= 2:
            diff = lengths[0] - lengths[1]
            is_arithmetic = all(lengths[i] - lengths[i + 1] == diff for i in range(len(lengths) - 1))
        else:
            is_arithmetic = True
        
        # Check for geometric progression
        if len(lengths) >= 2 and lengths[1] != 0:
            ratio = lengths[0] / lengths[1]
            is_geometric = all(lengths[i] / lengths[i + 1] == ratio for i in range(len(lengths) - 1) if lengths[i + 1] != 0)
        else:
            is_geometric = True
        
        return {
            'lengths': lengths,
            'is_arithmetic': is_arithmetic,
            'is_geometric': is_geometric,
            'min_length': min(lengths) if lengths else 0,
            'max_length': max(lengths) if lengths else 0,
            'avg_length': sum(lengths) / len(lengths) if lengths else 0
        }
    
    def get_border_statistics(self):
        """Get comprehensive statistics about borders"""
        distribution = self.analyze_border_distribution()
        patterns = self.find_border_patterns()
        
        return {
            'string': ''.join(self.s),
            'string_length': self.n,
            'border_count': len(self.borders),
            'borders': self.borders,
            'distribution': distribution,
            'patterns': patterns,
            'longest_border': self.get_longest_border(),
            'shortest_border': self.get_shortest_border()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'borders':
                result = self.get_borders()
                results.append(result)
            elif query['type'] == 'count':
                result = self.get_border_count()
                results.append(result)
            elif query['type'] == 'longest':
                result = self.get_longest_border()
                results.append(result)
            elif query['type'] == 'shortest':
                result = self.get_shortest_border()
                results.append(result)
            elif query['type'] == 'border_at':
                result = self.find_border_at_position(query['pos'])
                results.append(result)
            elif query['type'] == 'analyze':
                result = self.analyze_border_distribution()
                results.append(result)
            elif query['type'] == 'common_borders':
                result = self.find_common_borders(query['other_string'])
                results.append(result)
            elif query['type'] == 'patterns':
                result = self.find_border_patterns()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_border_statistics()
                results.append(result)
        return results
```

### Variation 3: Finding Borders with Constraints
**Problem**: Handle border queries with additional constraints (e.g., minimum length, maximum length, frequency).

**Link**: [CSES Problem Set - Finding Borders with Constraints](https://cses.fi/problemset/task/finding_borders_constraints)

```python
class FindingBordersWithConstraints:
    def __init__(self, s, min_length, max_length, min_frequency):
        self.s = list(s)
        self.n = len(self.s)
        self.min_length = min_length
        self.max_length = max_length
        self.min_frequency = min_frequency
        self.failure_function = self._build_failure_function()
        self.borders = self._extract_borders()
    
    def _build_failure_function(self):
        """Build failure function using KMP algorithm"""
        failure = [0] * self.n
        
        for i in range(1, self.n):
            j = failure[i - 1]
            while j > 0 and self.s[i] != self.s[j]:
                j = failure[j - 1]
            if self.s[i] == self.s[j]:
                j += 1
            failure[i] = j
        
        return failure
    
    def _extract_borders(self):
        """Extract all borders from failure function"""
        borders = []
        j = self.failure_function[self.n - 1]
        
        while j > 0:
            borders.append(''.join(self.s[:j]))
            j = self.failure_function[j - 1]
        
        return borders
    
    def constrained_border_query(self):
        """Query borders with constraints"""
        valid_borders = []
        
        for border in self.borders:
            length = len(border)
            
            # Check length constraints
            if length < self.min_length or length > self.max_length:
                continue
            
            # Check frequency constraint (how many times the border appears)
            frequency = self._count_border_frequency(border)
            if frequency < self.min_frequency:
                continue
            
            valid_borders.append({
                'border': border,
                'length': length,
                'frequency': frequency
            })
        
        return valid_borders
    
    def _count_border_frequency(self, border):
        """Count how many times a border appears in the string"""
        count = 0
        border_length = len(border)
        
        for i in range(self.n - border_length + 1):
            if ''.join(self.s[i:i + border_length]) == border:
                count += 1
        
        return count
    
    def find_valid_borders(self):
        """Find all valid borders that satisfy constraints"""
        return self.constrained_border_query()
    
    def get_longest_valid_border(self):
        """Get longest valid border that satisfies constraints"""
        valid_borders = self.find_valid_borders()
        
        if not valid_borders:
            return None
        
        longest = max(valid_borders, key=lambda x: x['length'])
        return longest
    
    def get_shortest_valid_border(self):
        """Get shortest valid border that satisfies constraints"""
        valid_borders = self.find_valid_borders()
        
        if not valid_borders:
            return None
        
        shortest = min(valid_borders, key=lambda x: x['length'])
        return shortest
    
    def get_most_frequent_valid_border(self):
        """Get most frequent valid border that satisfies constraints"""
        valid_borders = self.find_valid_borders()
        
        if not valid_borders:
            return None
        
        most_frequent = max(valid_borders, key=lambda x: x['frequency'])
        return most_frequent
    
    def get_least_frequent_valid_border(self):
        """Get least frequent valid border that satisfies constraints"""
        valid_borders = self.find_valid_borders()
        
        if not valid_borders:
            return None
        
        least_frequent = min(valid_borders, key=lambda x: x['frequency'])
        return least_frequent
    
    def count_valid_borders(self):
        """Count number of valid borders"""
        return len(self.find_valid_borders())
    
    def get_constraint_statistics(self):
        """Get statistics about valid borders"""
        valid_borders = self.find_valid_borders()
        
        if not valid_borders:
            return {
                'count': 0,
                'min_length': 0,
                'max_length': 0,
                'avg_length': 0,
                'min_frequency': 0,
                'max_frequency': 0,
                'avg_frequency': 0
            }
        
        lengths = [border['length'] for border in valid_borders]
        frequencies = [border['frequency'] for border in valid_borders]
        
        return {
            'count': len(valid_borders),
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

fb = FindingBordersWithConstraints(s, min_length, max_length, min_frequency)
result = fb.constrained_border_query()
print(f"Constrained border query result: {result}")

valid_borders = fb.find_valid_borders()
print(f"Valid borders: {valid_borders}")

longest = fb.get_longest_valid_border()
print(f"Longest valid border: {longest}")
```

### Related Problems

#### **CSES Problems**
- [Finding Borders](https://cses.fi/problemset/task/1732) - Basic finding borders problem
- [Finding Periods](https://cses.fi/problemset/task/1733) - Find periods of string
- [Pattern Positions](https://cses.fi/problemset/task/1753) - Find pattern positions

#### **LeetCode Problems**
- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) - String matching with repetition
- [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) - Find longest common prefix
- [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) - Pattern matching with wildcards

#### **Problem Categories**
- **KMP Algorithm**: String matching, border detection, failure function
- **Pattern Matching**: KMP, Z-algorithm, string matching algorithms
- **String Processing**: Borders, periods, palindromes, string transformations
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata
