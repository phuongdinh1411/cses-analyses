---
layout: simple
title: "Pattern Positions"
permalink: /problem_soulutions/string_algorithms/pattern_positions_analysis
---

# Pattern Positions

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand pattern matching and string searching algorithms
- Apply the Knuth-Morris-Pratt (KMP) algorithm for efficient pattern matching
- Implement the Rabin-Karp algorithm using rolling hash
- Optimize string matching algorithms for large inputs
- Handle edge cases in pattern matching (empty patterns, repeated patterns)

## 📋 Problem Description

Given a text string and a pattern string, find all positions where the pattern occurs in the text. This is the fundamental pattern matching problem that forms the basis for many other string algorithms.

**Input**: 
- First line: text string
- Second line: pattern string

**Output**: 
- Print all positions (0-indexed) where the pattern occurs in the text, separated by spaces

**Constraints**:
- 1 ≤ |text|, |pattern| ≤ 10⁶
- Both strings contain only lowercase English letters

**Example**:
```
Input:
ababcababc
abc

Output:
2 7

Explanation**: 
The pattern "abc" occurs at positions 2 and 7 in the text "ababcababc":
- Position 2: "ababcababc" → "abc" matches
- Position 7: "ababcababc" → "abc" matches
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Naive String Matching

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check every possible position in the text
- **Character-by-Character Comparison**: Compare pattern with text at each position
- **Complete Coverage**: Guaranteed to find all occurrences
- **Simple Implementation**: Straightforward nested loops approach

**Key Insight**: For each position in the text, check if the pattern matches starting from that position.

**Algorithm**:
- For each position i in the text:
  - Check if pattern matches text[i:i+len(pattern)]
  - If match found, record the position

**Visual Example**:
```
Text: "ababcababc", Pattern: "abc"

Check position 0: "aba" vs "abc" → No match
Check position 1: "bab" vs "abc" → No match  
Check position 2: "abc" vs "abc" → Match! (position 2)
Check position 3: "bca" vs "abc" → No match
Check position 4: "cab" vs "abc" → No match
Check position 5: "aba" vs "abc" → No match
Check position 6: "bab" vs "abc" → No match
Check position 7: "abc" vs "abc" → Match! (position 7)

Results: [2, 7]
```

**Implementation**:
```python
def brute_force_pattern_positions(text, pattern):
    """
    Find all pattern occurrences using brute force approach
    
    Args:
        text: the text string to search in
        pattern: the pattern string to find
    
    Returns:
        list: positions where pattern occurs
    """
    n, m = len(text), len(pattern)
    positions = []
    
    # Check each possible starting position
    for i in range(n - m + 1):
        # Check if pattern matches at position i
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        
        if match:
            positions.append(i)
    
    return positions

# Example usage
text = "ababcababc"
pattern = "abc"
result = brute_force_pattern_positions(text, pattern)
print(f"Brute force result: {result}")  # Output: [2, 7]
```

**Time Complexity**: O(n × m) - For each position, compare up to m characters
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Rabin-Karp Algorithm

**Key Insights from Optimized Approach**:
- **Rolling Hash**: Use hash function to compare strings efficiently
- **Hash Comparison**: Compare hash values instead of character-by-character
- **Efficient Updates**: Update hash in O(1) time when sliding the window
- **Collision Handling**: Handle hash collisions with additional verification

**Key Insight**: Use rolling hash to compare strings in O(1) time, reducing overall complexity.

**Algorithm**:
- Compute hash of pattern
- Compute hash of first window in text
- Slide window and update hash efficiently
- Compare hashes and verify matches

**Visual Example**:
```
Text: "ababcababc", Pattern: "abc"

Step 1: Compute pattern hash
Pattern "abc": hash = (1×26² + 2×26¹ + 3×26⁰) mod p

Step 2: Compute first window hash
Text[0:3] "aba": hash = (1×26² + 2×26¹ + 1×26⁰) mod p

Step 3: Slide window and update hash
Window "bab": hash = (2×26² + 1×26¹ + 2×26⁰) mod p
Window "abc": hash = (1×26² + 2×26¹ + 3×26⁰) mod p → Match!

Continue sliding...
```

**Implementation**:
```python
def optimized_pattern_positions(text, pattern):
    """
    Find all pattern occurrences using Rabin-Karp algorithm
    
    Args:
        text: the text string to search in
        pattern: the pattern string to find
    
    Returns:
        list: positions where pattern occurs
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Hash parameters
    base = 26
    mod = 10**9 + 7
    
    # Compute pattern hash
    pattern_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
    
    # Compute first window hash
    window_hash = 0
    for i in range(m):
        window_hash = (window_hash * base + ord(text[i])) % mod
    
    positions = []
    
    # Check first window
    if window_hash == pattern_hash and text[:m] == pattern:
        positions.append(0)
    
    # Slide window and update hash
    base_power = pow(base, m - 1, mod)
    for i in range(1, n - m + 1):
        # Remove leftmost character and add rightmost character
        window_hash = ((window_hash - ord(text[i-1]) * base_power) * base + ord(text[i + m - 1])) % mod
        
        # Check for match
        if window_hash == pattern_hash and text[i:i+m] == pattern:
            positions.append(i)
    
    return positions

# Example usage
text = "ababcababc"
pattern = "abc"
result = optimized_pattern_positions(text, pattern)
print(f"Optimized result: {result}")  # Output: [2, 7]
```

**Time Complexity**: O(n + m) - Average case, O(n × m) worst case
**Space Complexity**: O(1) - Constant extra space

**Why it's better**: Much more efficient on average, but worst case is still quadratic.

---

### Approach 3: Optimal - Knuth-Morris-Pratt (KMP) Algorithm

**Key Insights from Optimal Approach**:
- **Failure Function**: Preprocess pattern to create failure function (LPS array)
- **Skip Characters**: Skip characters that are guaranteed not to match
- **Linear Time**: Achieve O(n + m) time complexity in all cases
- **No Backtracking**: Never backtrack in the text

**Key Insight**: Preprocess the pattern to create a failure function that tells us how many characters to skip when a mismatch occurs.

**Algorithm**:
- Build failure function (LPS array) for the pattern
- Use failure function to skip characters during matching
- Never backtrack in the text

**Visual Example**:
```
Pattern: "abc"

Step 1: Build LPS array
LPS[0] = 0 (no proper prefix)
LPS[1] = 0 (no proper prefix of "ab")
LPS[2] = 0 (no proper prefix of "abc")

Step 2: KMP matching
Text: "ababcababc"
Pattern: "abc"

i=0, j=0: 'a' == 'a' → i=1, j=1
i=1, j=1: 'b' == 'b' → i=2, j=2  
i=2, j=2: 'a' != 'c' → j = LPS[1] = 0
i=2, j=0: 'a' == 'a' → i=3, j=1
i=3, j=1: 'b' == 'b' → i=4, j=2
i=4, j=2: 'c' == 'c' → Match at position 2!

Continue...
```

**Implementation**:
```python
def optimal_pattern_positions(text, pattern):
    """
    Find all pattern occurrences using KMP algorithm
    
    Args:
        text: the text string to search in
        pattern: the pattern string to find
    
    Returns:
        list: positions where pattern occurs
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
    
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Build LPS array
    lps = build_lps(pattern)
    
    positions = []
    i = j = 0  # i for text, j for pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions

# Example usage
text = "ababcababc"
pattern = "abc"
result = optimal_pattern_positions(text, pattern)
print(f"Optimal result: {result}")  # Output: [2, 7]
```

**Time Complexity**: O(n + m) - Linear time in all cases
**Space Complexity**: O(m) - For LPS array

**Why it's optimal**: Guaranteed linear time complexity with no backtracking in text.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × m) | O(1) | Check all positions |
| Rabin-Karp | O(n + m) avg, O(n × m) worst | O(1) | Rolling hash comparison |
| KMP Algorithm | O(n + m) | O(m) | Failure function preprocessing |

### Time Complexity
- **Time**: O(n + m) - KMP algorithm provides optimal linear time
- **Space**: O(m) - For LPS array in KMP algorithm

### Why This Solution Works
- **Pattern Preprocessing**: KMP algorithm preprocesses pattern for efficient matching
- **No Backtracking**: Never need to backtrack in the text
- **Optimal Complexity**: Guaranteed linear time in all cases
- **Optimal Approach**: KMP algorithm provides the best theoretical and practical performance

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Pattern Positions with Dynamic Updates
**Problem**: Handle dynamic updates to text and pattern strings and maintain pattern position queries efficiently.

**Link**: [CSES Problem Set - Pattern Positions with Updates](https://cses.fi/problemset/task/pattern_positions_updates)

```python
class PatternPositionsWithUpdates:
    def __init__(self, text, pattern):
        self.text = list(text)
        self.pattern = list(pattern)
        self.n = len(self.text)
        self.m = len(self.pattern)
        self.lps = self._build_lps()
        self.positions = self._find_all_positions()
    
    def _build_lps(self):
        """Build Longest Proper Prefix which is also Suffix array"""
        lps = [0] * self.m
        length = 0
        i = 1
        
        while i < self.m:
            if self.pattern[i] == self.pattern[length]:
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
    
    def _find_all_positions(self):
        """Find all positions where pattern occurs in text"""
        positions = []
        i = j = 0  # i for text, j for pattern
        
        while i < self.n:
            if self.text[i] == self.pattern[j]:
                i += 1
                j += 1
            
            if j == self.m:
                positions.append(i - j)
                j = self.lps[j - 1]
            elif i < self.n and self.text[i] != self.pattern[j]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
        
        return positions
    
    def update_text(self, pos, char):
        """Update character in text at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.text[pos] = char
        self.positions = self._find_all_positions()
    
    def update_pattern(self, pos, char):
        """Update character in pattern at position pos"""
        if pos < 0 or pos >= self.m:
            return
        
        self.pattern[pos] = char
        self.lps = self._build_lps()
        self.positions = self._find_all_positions()
    
    def get_positions(self):
        """Get all positions where pattern occurs in text"""
        return self.positions.copy()
    
    def count_occurrences(self):
        """Count number of occurrences of pattern in text"""
        return len(self.positions)
    
    def find_next_occurrence(self, start_pos):
        """Find next occurrence of pattern starting from start_pos"""
        for pos in self.positions:
            if pos >= start_pos:
                return pos
        return -1
    
    def find_previous_occurrence(self, end_pos):
        """Find previous occurrence of pattern ending before end_pos"""
        for pos in reversed(self.positions):
            if pos < end_pos:
                return pos
        return -1
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update_text':
                self.update_text(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'update_pattern':
                self.update_pattern(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'positions':
                result = self.get_positions()
                results.append(result)
            elif query['type'] == 'count':
                result = self.count_occurrences()
                results.append(result)
            elif query['type'] == 'next':
                result = self.find_next_occurrence(query['start_pos'])
                results.append(result)
            elif query['type'] == 'previous':
                result = self.find_previous_occurrence(query['end_pos'])
                results.append(result)
        return results
```

### Variation 2: Pattern Positions with Different Operations
**Problem**: Handle different types of operations (find, count, analyze) on pattern matching.

**Link**: [CSES Problem Set - Pattern Positions Different Operations](https://cses.fi/problemset/task/pattern_positions_operations)

```python
class PatternPositionsDifferentOps:
    def __init__(self, text, pattern):
        self.text = list(text)
        self.pattern = list(pattern)
        self.n = len(self.text)
        self.m = len(self.pattern)
        self.lps = self._build_lps()
        self.positions = self._find_all_positions()
    
    def _build_lps(self):
        """Build Longest Proper Prefix which is also Suffix array"""
        lps = [0] * self.m
        length = 0
        i = 1
        
        while i < self.m:
            if self.pattern[i] == self.pattern[length]:
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
    
    def _find_all_positions(self):
        """Find all positions where pattern occurs in text"""
        positions = []
        i = j = 0  # i for text, j for pattern
        
        while i < self.n:
            if self.text[i] == self.pattern[j]:
                i += 1
                j += 1
            
            if j == self.m:
                positions.append(i - j)
                j = self.lps[j - 1]
            elif i < self.n and self.text[i] != self.pattern[j]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
        
        return positions
    
    def get_positions(self):
        """Get all positions where pattern occurs in text"""
        return self.positions.copy()
    
    def count_occurrences(self):
        """Count number of occurrences of pattern in text"""
        return len(self.positions)
    
    def find_next_occurrence(self, start_pos):
        """Find next occurrence of pattern starting from start_pos"""
        for pos in self.positions:
            if pos >= start_pos:
                return pos
        return -1
    
    def find_previous_occurrence(self, end_pos):
        """Find previous occurrence of pattern ending before end_pos"""
        for pos in reversed(self.positions):
            if pos < end_pos:
                return pos
        return -1
    
    def find_overlapping_occurrences(self):
        """Find all overlapping occurrences of pattern in text"""
        overlapping = []
        
        for i in range(len(self.positions) - 1):
            current_pos = self.positions[i]
            next_pos = self.positions[i + 1]
            
            if next_pos < current_pos + self.m:
                overlapping.append({
                    'first': current_pos,
                    'second': next_pos,
                    'overlap': current_pos + self.m - next_pos
                })
        
        return overlapping
    
    def find_non_overlapping_occurrences(self):
        """Find all non-overlapping occurrences of pattern in text"""
        non_overlapping = []
        last_end = -1
        
        for pos in self.positions:
            if pos > last_end:
                non_overlapping.append(pos)
                last_end = pos + self.m - 1
        
        return non_overlapping
    
    def analyze_pattern_distribution(self):
        """Analyze distribution of pattern occurrences"""
        if not self.positions:
            return {
                'total_occurrences': 0,
                'overlapping_occurrences': 0,
                'non_overlapping_occurrences': 0,
                'average_gap': 0,
                'min_gap': 0,
                'max_gap': 0
            }
        
        overlapping = self.find_overlapping_occurrences()
        non_overlapping = self.find_non_overlapping_occurrences()
        
        gaps = []
        for i in range(len(self.positions) - 1):
            gap = self.positions[i + 1] - self.positions[i]
            gaps.append(gap)
        
        return {
            'total_occurrences': len(self.positions),
            'overlapping_occurrences': len(overlapping),
            'non_overlapping_occurrences': len(non_overlapping),
            'average_gap': sum(gaps) / len(gaps) if gaps else 0,
            'min_gap': min(gaps) if gaps else 0,
            'max_gap': max(gaps) if gaps else 0
        }
    
    def get_pattern_statistics(self):
        """Get comprehensive statistics about pattern matching"""
        distribution = self.analyze_pattern_distribution()
        
        return {
            'pattern': ''.join(self.pattern),
            'text_length': self.n,
            'pattern_length': self.m,
            'distribution': distribution,
            'positions': self.positions,
            'overlapping': self.find_overlapping_occurrences(),
            'non_overlapping': self.find_non_overlapping_occurrences()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'positions':
                result = self.get_positions()
                results.append(result)
            elif query['type'] == 'count':
                result = self.count_occurrences()
                results.append(result)
            elif query['type'] == 'next':
                result = self.find_next_occurrence(query['start_pos'])
                results.append(result)
            elif query['type'] == 'previous':
                result = self.find_previous_occurrence(query['end_pos'])
                results.append(result)
            elif query['type'] == 'overlapping':
                result = self.find_overlapping_occurrences()
                results.append(result)
            elif query['type'] == 'non_overlapping':
                result = self.find_non_overlapping_occurrences()
                results.append(result)
            elif query['type'] == 'analyze':
                result = self.analyze_pattern_distribution()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_pattern_statistics()
                results.append(result)
        return results
```

### Variation 3: Pattern Positions with Constraints
**Problem**: Handle pattern position queries with additional constraints (e.g., minimum gap, maximum gap, frequency).

**Link**: [CSES Problem Set - Pattern Positions with Constraints](https://cses.fi/problemset/task/pattern_positions_constraints)

```python
class PatternPositionsWithConstraints:
    def __init__(self, text, pattern, min_gap, max_gap, min_frequency):
        self.text = list(text)
        self.pattern = list(pattern)
        self.n = len(self.text)
        self.m = len(self.pattern)
        self.min_gap = min_gap
        self.max_gap = max_gap
        self.min_frequency = min_frequency
        self.lps = self._build_lps()
        self.positions = self._find_all_positions()
    
    def _build_lps(self):
        """Build Longest Proper Prefix which is also Suffix array"""
        lps = [0] * self.m
        length = 0
        i = 1
        
        while i < self.m:
            if self.pattern[i] == self.pattern[length]:
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
    
    def _find_all_positions(self):
        """Find all positions where pattern occurs in text"""
        positions = []
        i = j = 0  # i for text, j for pattern
        
        while i < self.n:
            if self.text[i] == self.pattern[j]:
                i += 1
                j += 1
            
            if j == self.m:
                positions.append(i - j)
                j = self.lps[j - 1]
            elif i < self.n and self.text[i] != self.pattern[j]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
        
        return positions
    
    def constrained_position_query(self, start_pos, end_pos):
        """Query pattern positions with constraints"""
        if start_pos < 0 or end_pos >= self.n or start_pos > end_pos:
            return []
        
        valid_positions = []
        
        for pos in self.positions:
            if start_pos <= pos <= end_pos:
                valid_positions.append(pos)
        
        # Check gap constraints
        if len(valid_positions) < 2:
            return valid_positions
        
        constrained_positions = [valid_positions[0]]
        
        for i in range(1, len(valid_positions)):
            gap = valid_positions[i] - valid_positions[i - 1]
            if self.min_gap <= gap <= self.max_gap:
                constrained_positions.append(valid_positions[i])
        
        # Check frequency constraint
        if len(constrained_positions) < self.min_frequency:
            return []
        
        return constrained_positions
    
    def find_valid_occurrences(self):
        """Find all valid occurrences that satisfy constraints"""
        valid_occurrences = []
        
        if len(self.positions) < self.min_frequency:
            return valid_occurrences
        
        # Check gap constraints
        constrained_positions = [self.positions[0]]
        
        for i in range(1, len(self.positions)):
            gap = self.positions[i] - self.positions[i - 1]
            if self.min_gap <= gap <= self.max_gap:
                constrained_positions.append(self.positions[i])
        
        # Check frequency constraint
        if len(constrained_positions) >= self.min_frequency:
            valid_occurrences = constrained_positions
        
        return valid_occurrences
    
    def get_longest_valid_sequence(self):
        """Get longest valid sequence of pattern occurrences"""
        valid_occurrences = self.find_valid_occurrences()
        
        if not valid_occurrences:
            return []
        
        longest_sequence = []
        current_sequence = [valid_occurrences[0]]
        
        for i in range(1, len(valid_occurrences)):
            gap = valid_occurrences[i] - valid_occurrences[i - 1]
            
            if self.min_gap <= gap <= self.max_gap:
                current_sequence.append(valid_occurrences[i])
            else:
                if len(current_sequence) > len(longest_sequence):
                    longest_sequence = current_sequence.copy()
                current_sequence = [valid_occurrences[i]]
        
        if len(current_sequence) > len(longest_sequence):
            longest_sequence = current_sequence
        
        return longest_sequence
    
    def get_shortest_valid_sequence(self):
        """Get shortest valid sequence of pattern occurrences"""
        valid_occurrences = self.find_valid_occurrences()
        
        if not valid_occurrences:
            return []
        
        shortest_sequence = valid_occurrences[:self.min_frequency]
        
        for i in range(self.min_frequency, len(valid_occurrences)):
            for j in range(i - self.min_frequency + 1):
                sequence = valid_occurrences[j:i + 1]
                if len(sequence) >= self.min_frequency:
                    if len(sequence) < len(shortest_sequence):
                        shortest_sequence = sequence
        
        return shortest_sequence
    
    def count_valid_occurrences(self):
        """Count number of valid occurrences"""
        return len(self.find_valid_occurrences())
    
    def get_constraint_statistics(self):
        """Get statistics about valid occurrences"""
        valid_occurrences = self.find_valid_occurrences()
        
        if not valid_occurrences:
            return {
                'count': 0,
                'min_gap': 0,
                'max_gap': 0,
                'avg_gap': 0,
                'longest_sequence': 0,
                'shortest_sequence': 0
            }
        
        gaps = []
        for i in range(len(valid_occurrences) - 1):
            gap = valid_occurrences[i + 1] - valid_occurrences[i]
            gaps.append(gap)
        
        longest_sequence = self.get_longest_valid_sequence()
        shortest_sequence = self.get_shortest_valid_sequence()
        
        return {
            'count': len(valid_occurrences),
            'min_gap': min(gaps) if gaps else 0,
            'max_gap': max(gaps) if gaps else 0,
            'avg_gap': sum(gaps) / len(gaps) if gaps else 0,
            'longest_sequence': len(longest_sequence),
            'shortest_sequence': len(shortest_sequence)
        }

# Example usage
text = "abacabacabac"
pattern = "aba"
min_gap = 2
max_gap = 6
min_frequency = 2

pp = PatternPositionsWithConstraints(text, pattern, min_gap, max_gap, min_frequency)
result = pp.constrained_position_query(0, 11)
print(f"Constrained position query result: {result}")

valid_occurrences = pp.find_valid_occurrences()
print(f"Valid occurrences: {valid_occurrences}")

longest_sequence = pp.get_longest_valid_sequence()
print(f"Longest valid sequence: {longest_sequence}")
```

### Related Problems

#### **CSES Problems**
- [Pattern Positions](https://cses.fi/problemset/task/1753) - Basic pattern positions problem
- [String Matching](https://cses.fi/problemset/task/1753) - String matching
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string

#### **LeetCode Problems**
- [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) - Find all anagram positions
- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) - String matching with repetition
- [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) - Pattern matching with wildcards

#### **Problem Categories**
- **KMP Algorithm**: String matching, pattern detection, failure function
- **Pattern Matching**: KMP, Z-algorithm, string matching algorithms
- **String Processing**: Borders, periods, palindromes, string transformations
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata
