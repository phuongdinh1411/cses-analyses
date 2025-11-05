---
layout: simple
title: "Longest Palindrome - Manacher's Algorithm"
permalink: /problem_soulutions/string_algorithms/longest_palindrome_analysis
---

# Longest Palindrome - Manacher's Algorithm

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand palindrome detection and longest palindrome finding
- Apply Manacher's algorithm for optimal palindrome detection
- Implement center expansion technique for palindrome finding
- Optimize palindrome algorithms for large inputs
- Handle edge cases in palindrome problems (single characters, even/odd lengths)

## 📋 Problem Description

Given a string, find the longest palindromic substring. A palindrome is a string that reads the same forwards and backwards.

This is a classic string algorithm problem that can be solved using multiple approaches, with Manacher's algorithm providing the optimal solution.

**Input**: 
- First line: string s (the input string)

**Output**: 
- Print the longest palindromic substring

**Constraints**:
- 1 ≤ |s| ≤ 10⁶
- String contains only lowercase English letters

**Example**:
```
Input:
babad

Output:
bab

Explanation**: 
The string "babad" contains several palindromes:
- "b" (length 1)
- "a" (length 1) 
- "b" (length 1)
- "a" (length 1)
- "d" (length 1)
- "aba" (length 3)
- "bab" (length 3)

The longest palindromes are "aba" and "bab", both of length 3.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Substrings

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible substrings
- **Palindrome Validation**: For each substring, check if it's a palindrome
- **Complete Coverage**: Guaranteed to find the longest palindrome
- **Simple Implementation**: Straightforward nested loops approach

**Key Insight**: Generate all possible substrings and check which ones are palindromes.

**Algorithm**:
- Generate all possible substrings
- For each substring, check if it's a palindrome
- Keep track of the longest palindrome found

**Visual Example**:
```
String: "babad"

All possible substrings:
1. "b" → Palindrome ✓ (length 1)
2. "ba" → Not palindrome ✗
3. "bab" → Palindrome ✓ (length 3)
4. "baba" → Not palindrome ✗
5. "babad" → Not palindrome ✗
6. "a" → Palindrome ✓ (length 1)
7. "ab" → Not palindrome ✗
8. "aba" → Palindrome ✓ (length 3)
9. "abad" → Not palindrome ✗
10. "b" → Palindrome ✓ (length 1)
11. "ba" → Not palindrome ✗
12. "bad" → Not palindrome ✗
13. "a" → Palindrome ✓ (length 1)
14. "ad" → Not palindrome ✗
15. "d" → Palindrome ✓ (length 1)

Longest palindromes: "bab" and "aba" (length 3)
```

**Implementation**:
```python
def brute_force_longest_palindrome(s):
    """
    Find longest palindrome using brute force approach
    
    Args:
        s: input string
    
    Returns:
        str: longest palindromic substring
    """
    def is_palindrome(substring):
        """Check if a substring is a palindrome"""
        return substring == substring[::-1]
    
    n = len(s)
    longest = ""
    
    # Check all possible substrings
    for i in range(n):
        for j in range(i, n):
            substring = s[i:j+1]
            if is_palindrome(substring) and len(substring) > len(longest):
                longest = substring
    
    return longest

# Example usage
s = "babad"
result = brute_force_longest_palindrome(s)
print(f"Brute force result: {result}")  # Output: "bab"
```

**Time Complexity**: O(n³) - Check all substrings and validate palindromes
**Space Complexity**: O(1) - Constant extra space

**Why it's inefficient**: Cubic time complexity makes it very slow for large inputs.

---

### Approach 2: Optimized - Center Expansion

**Key Insights from Optimized Approach**:
- **Center-Based**: Consider each character as a potential center of a palindrome
- **Expansion**: Expand outward from each center to find palindromes
- **Even/Odd Lengths**: Handle both odd-length and even-length palindromes
- **Efficient Validation**: Stop expansion when characters don't match

**Key Insight**: For each possible center, expand outward to find the longest palindrome centered at that position.

**Algorithm**:
- For each position, consider it as center of odd-length palindrome
- For each position, consider it as center of even-length palindrome
- Expand outward from each center until characters don't match
- Keep track of the longest palindrome found

**Visual Example**:
```
String: "babad"

Center expansion:
1. Center at index 0 ('b'):
   - Odd: "b" → length 1
   - Even: "b" vs "" → length 1

2. Center at index 1 ('a'):
   - Odd: "a" → "bab" → length 3
   - Even: "a" vs "b" → length 1

3. Center at index 2 ('b'):
   - Odd: "b" → "aba" → length 3
   - Even: "b" vs "a" → length 1

4. Center at index 3 ('a'):
   - Odd: "a" → length 1
   - Even: "a" vs "b" → length 1

5. Center at index 4 ('d'):
   - Odd: "d" → length 1
   - Even: "d" vs "" → length 1

Longest palindromes: "bab" and "aba" (length 3)
```

**Implementation**:
```python
def optimized_longest_palindrome(s):
    """
    Find longest palindrome using center expansion
    
    Args:
        s: input string
    
    Returns:
        str: longest palindromic substring
    """
    def expand_around_center(left, right):
        """Expand around center and return palindrome length"""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    if not s:
        return ""
    
    start = end = 0
    
    for i in range(len(s)):
        # Check odd-length palindromes
        len1 = expand_around_center(i, i)
        # Check even-length palindromes
        len2 = expand_around_center(i, i + 1)
        
        # Get maximum length
        max_len = max(len1, len2)
        
        # Update start and end if we found a longer palindrome
        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2
    
    return s[start:end + 1]

# Example usage
s = "babad"
result = optimized_longest_palindrome(s)
print(f"Optimized result: {result}")  # Output: "bab"
```

**Time Complexity**: O(n²) - For each center, expand up to n characters
**Space Complexity**: O(1) - Constant extra space

**Why it's better**: Much more efficient than brute force, but still quadratic.

---

### Approach 3: Optimal - Manacher's Algorithm

**Key Insights from Optimal Approach**:
- **Linear Time**: Achieve O(n) time complexity
- **Palindrome Properties**: Use properties of palindromes to avoid redundant calculations
- **Mirror Property**: Use information from previously computed palindromes
- **Boundary Tracking**: Track the rightmost boundary of palindromes

**Key Insight**: Use the mirror property of palindromes to avoid redundant calculations by leveraging information from previously computed palindromes.

**Algorithm**:
- Transform string to handle even-length palindromes
- Use array to store palindrome lengths
- Use mirror property to avoid redundant calculations
- Expand only when necessary

**Visual Example**:
```
String: "babad"
Transformed: "#b#a#b#a#d#"

Manacher's algorithm:
i=0: P[0] = 0
i=1: P[1] = 1 (palindrome "#b#")
i=2: P[2] = 0
i=3: P[3] = 3 (palindrome "#b#a#b#")
i=4: P[4] = 0
i=5: P[5] = 3 (palindrome "#a#b#a#")
i=6: P[6] = 0
i=7: P[7] = 0
i=8: P[8] = 0
i=9: P[9] = 0
i=10: P[10] = 0

Maximum P[i] = 3, corresponding to "bab" or "aba"
```

**Implementation**:
```python
def optimal_longest_palindrome(s):
    """
    Find longest palindrome using Manacher's algorithm
    
    Args:
        s: input string
    
    Returns:
        str: longest palindromic substring
    """
    if not s:
        return ""
    
    # Transform string to handle even-length palindromes
    transformed = "#" + "#".join(s) + "#"
    n = len(transformed)
    
    # Array to store palindrome lengths
    P = [0] * n
    center = right = 0
    max_len = 0
    max_center = 0
    
    for i in range(n):
        # Use mirror property if i is within current right boundary
        if i < right:
            P[i] = min(right - i, P[2 * center - i])
        
        # Expand around center i
        try:
            while (i + P[i] + 1 < n and 
                   i - P[i] - 1 >= 0 and 
                   transformed[i + P[i] + 1] == transformed[i - P[i] - 1]):
                P[i] += 1
        except IndexError:
            pass
        
        # Update center and right boundary if necessary
        if i + P[i] > right:
            center = i
            right = i + P[i]
        
        # Update maximum palindrome
        if P[i] > max_len:
            max_len = P[i]
            max_center = i
    
    # Extract the longest palindrome
    start = (max_center - max_len) // 2
    return s[start:start + max_len]

# Example usage
s = "babad"
result = optimal_longest_palindrome(s)
print(f"Optimal result: {result}")  # Output: "bab"
```

**Time Complexity**: O(n) - Linear time complexity
**Space Complexity**: O(n) - For transformed string and P array

**Why it's optimal**: Guaranteed linear time complexity with optimal space usage.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(1) | Check all substrings |
| Center Expansion | O(n²) | O(1) | Expand from each center |
| Manacher's Algorithm | O(n) | O(n) | Use palindrome properties |

### Time Complexity
- **Time**: O(n) - Manacher's algorithm provides optimal linear time
- **Space**: O(n) - For transformed string and palindrome length array

### Why This Solution Works
- **Palindrome Properties**: Leverage symmetry properties of palindromes
- **Mirror Property**: Use information from previously computed palindromes
- **Linear Expansion**: Each character is processed at most once
- **Optimal Approach**: Manacher's algorithm provides the best theoretical performance

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Longest Palindrome with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain longest palindrome information efficiently.

**Link**: [CSES Problem Set - Longest Palindrome with Updates](https://cses.fi/problemset/task/longest_palindrome_updates)

```python
class LongestPalindromeWithUpdates:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.transformed = self._transform_string()
        self.palindrome_lengths = self._manacher_algorithm()
        self.longest_palindrome = self._find_longest_palindrome()
    
    def _transform_string(self):
        """Transform string for Manacher's algorithm"""
        if not self.s:
            return ['#', '$']
        
        transformed = ['#']
        for char in self.s:
            transformed.append(char)
            transformed.append('#')
        transformed.append('$')
        
        return transformed
    
    def _manacher_algorithm(self):
        """Manacher's algorithm to find palindrome lengths"""
        n = len(self.transformed)
        P = [0] * n
        center = 0
        right = 0
        
        for i in range(1, n - 1):
            # Mirror position
            mirror = 2 * center - i
            
            if i < right:
                P[i] = min(right - i, P[mirror])
            
            # Expand around center i
            try:
                while (i + P[i] + 1 < n and 
                       i - P[i] - 1 >= 0 and 
                       self.transformed[i + P[i] + 1] == self.transformed[i - P[i] - 1]):
                    P[i] += 1
            except IndexError:
                pass
            
            # Update center and right boundary if necessary
            if i + P[i] > right:
                center = i
                right = i + P[i]
        
        return P
    
    def _find_longest_palindrome(self):
        """Find the longest palindrome from palindrome lengths"""
        max_length = 0
        center_index = 0
        
        for i in range(len(self.palindrome_lengths)):
            if self.palindrome_lengths[i] > max_length:
                max_length = self.palindrome_lengths[i]
                center_index = i
        
        if max_length == 0:
            return None
        
        # Convert back to original string coordinates
        start = (center_index - max_length) // 2
        end = (center_index + max_length) // 2
        
        return {
            'palindrome': ''.join(self.s[start:end]),
            'start': start,
            'end': end,
            'length': max_length
        }
    
    def update(self, pos, char):
        """Update character at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.s[pos] = char
        
        # Rebuild transformed string, palindrome lengths, and longest palindrome
        self.transformed = self._transform_string()
        self.palindrome_lengths = self._manacher_algorithm()
        self.longest_palindrome = self._find_longest_palindrome()
    
    def get_longest_palindrome(self):
        """Get the longest palindrome"""
        return self.longest_palindrome
    
    def get_palindrome_at_position(self, pos):
        """Get palindrome centered at position pos"""
        if pos < 0 or pos >= self.n:
            return None
        
        # Convert to transformed string position
        transformed_pos = 2 * pos + 1
        length = self.palindrome_lengths[transformed_pos]
        
        if length == 0:
            return None
        
        start = (transformed_pos - length) // 2
        end = (transformed_pos + length) // 2
        
        return {
            'palindrome': ''.join(self.s[start:end]),
            'start': start,
            'end': end,
            'length': length
        }
    
    def get_all_palindromes(self):
        """Get all palindromes in the string"""
        palindromes = []
        
        for i in range(len(self.palindrome_lengths)):
            if self.palindrome_lengths[i] > 0:
                start = (i - self.palindrome_lengths[i]) // 2
                end = (i + self.palindrome_lengths[i]) // 2
                
                palindromes.append({
                    'palindrome': ''.join(self.s[start:end]),
                    'start': start,
                    'end': end,
                    'length': self.palindrome_lengths[i]
                })
        
        return palindromes
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'longest':
                result = self.get_longest_palindrome()
                results.append(result)
            elif query['type'] == 'palindrome_at':
                result = self.get_palindrome_at_position(query['pos'])
                results.append(result)
            elif query['type'] == 'all_palindromes':
                result = self.get_all_palindromes()
                results.append(result)
        return results
```

### Variation 2: Longest Palindrome with Different Operations
**Problem**: Handle different types of operations (find, analyze, compare) on palindrome detection.

**Link**: [CSES Problem Set - Longest Palindrome Different Operations](https://cses.fi/problemset/task/longest_palindrome_operations)

```python
class LongestPalindromeDifferentOps:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.transformed = self._transform_string()
        self.palindrome_lengths = self._manacher_algorithm()
        self.longest_palindrome = self._find_longest_palindrome()
    
    def _transform_string(self):
        """Transform string for Manacher's algorithm"""
        if not self.s:
            return ['#', '$']
        
        transformed = ['#']
        for char in self.s:
            transformed.append(char)
            transformed.append('#')
        transformed.append('$')
        
        return transformed
    
    def _manacher_algorithm(self):
        """Manacher's algorithm to find palindrome lengths"""
        n = len(self.transformed)
        P = [0] * n
        center = 0
        right = 0
        
        for i in range(1, n - 1):
            # Mirror position
            mirror = 2 * center - i
            
            if i < right:
                P[i] = min(right - i, P[mirror])
            
            # Expand around center i
            try:
                while (i + P[i] + 1 < n and 
                       i - P[i] - 1 >= 0 and 
                       self.transformed[i + P[i] + 1] == self.transformed[i - P[i] - 1]):
                    P[i] += 1
            except IndexError:
                pass
            
            # Update center and right boundary if necessary
            if i + P[i] > right:
                center = i
                right = i + P[i]
        
        return P
    
    def _find_longest_palindrome(self):
        """Find the longest palindrome from palindrome lengths"""
        max_length = 0
        center_index = 0
        
        for i in range(len(self.palindrome_lengths)):
            if self.palindrome_lengths[i] > max_length:
                max_length = self.palindrome_lengths[i]
                center_index = i
        
        if max_length == 0:
            return None
        
        # Convert back to original string coordinates
        start = (center_index - max_length) // 2
        end = (center_index + max_length) // 2
        
        return {
            'palindrome': ''.join(self.s[start:end]),
            'start': start,
            'end': end,
            'length': max_length
        }
    
    def get_longest_palindrome(self):
        """Get the longest palindrome"""
        return self.longest_palindrome
    
    def get_palindrome_at_position(self, pos):
        """Get palindrome centered at position pos"""
        if pos < 0 or pos >= self.n:
            return None
        
        # Convert to transformed string position
        transformed_pos = 2 * pos + 1
        length = self.palindrome_lengths[transformed_pos]
        
        if length == 0:
            return None
        
        start = (transformed_pos - length) // 2
        end = (transformed_pos + length) // 2
        
        return {
            'palindrome': ''.join(self.s[start:end]),
            'start': start,
            'end': end,
            'length': length
        }
    
    def get_all_palindromes(self):
        """Get all palindromes in the string"""
        palindromes = []
        
        for i in range(len(self.palindrome_lengths)):
            if self.palindrome_lengths[i] > 0:
                start = (i - self.palindrome_lengths[i]) // 2
                end = (i + self.palindrome_lengths[i]) // 2
                
                palindromes.append({
                    'palindrome': ''.join(self.s[start:end]),
                    'start': start,
                    'end': end,
                    'length': self.palindrome_lengths[i]
                })
        
        return palindromes
    
    def find_palindromes_of_length(self, target_length):
        """Find all palindromes of specific length"""
        palindromes = []
        
        for i in range(len(self.palindrome_lengths)):
            if self.palindrome_lengths[i] == target_length:
                start = (i - self.palindrome_lengths[i]) // 2
                end = (i + self.palindrome_lengths[i]) // 2
                
                palindromes.append({
                    'palindrome': ''.join(self.s[start:end]),
                    'start': start,
                    'end': end,
                    'length': self.palindrome_lengths[i]
                })
        
        return palindromes
    
    def find_palindromes_in_range(self, start_pos, end_pos):
        """Find all palindromes within a specific range"""
        palindromes = []
        
        for i in range(len(self.palindrome_lengths)):
            if self.palindrome_lengths[i] > 0:
                start = (i - self.palindrome_lengths[i]) // 2
                end = (i + self.palindrome_lengths[i]) // 2
                
                if start >= start_pos and end <= end_pos:
                    palindromes.append({
                        'palindrome': ''.join(self.s[start:end]),
                        'start': start,
                        'end': end,
                        'length': self.palindrome_lengths[i]
                    })
        
        return palindromes
    
    def analyze_palindrome_distribution(self):
        """Analyze distribution of palindromes by length"""
        distribution = {}
        
        for i in range(len(self.palindrome_lengths)):
            length = self.palindrome_lengths[i]
            if length > 0:
                if length not in distribution:
                    distribution[length] = {
                        'count': 0,
                        'palindromes': [],
                        'positions': []
                    }
                
                distribution[length]['count'] += 1
                start = (i - length) // 2
                end = (i + length) // 2
                distribution[length]['palindromes'].append(''.join(self.s[start:end]))
                distribution[length]['positions'].append((start, end))
        
        return distribution
    
    def get_palindrome_statistics(self):
        """Get comprehensive statistics about palindromes"""
        distribution = self.analyze_palindrome_distribution()
        all_palindromes = self.get_all_palindromes()
        
        if not all_palindromes:
            return {
                'total_palindromes': 0,
                'longest_length': 0,
                'shortest_length': 0,
                'average_length': 0,
                'distribution': {}
            }
        
        lengths = [p['length'] for p in all_palindromes]
        
        return {
            'total_palindromes': len(all_palindromes),
            'longest_length': max(lengths),
            'shortest_length': min(lengths),
            'average_length': sum(lengths) / len(lengths),
            'distribution': distribution,
            'longest_palindrome': self.get_longest_palindrome()
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'longest':
                result = self.get_longest_palindrome()
                results.append(result)
            elif query['type'] == 'palindrome_at':
                result = self.get_palindrome_at_position(query['pos'])
                results.append(result)
            elif query['type'] == 'all_palindromes':
                result = self.get_all_palindromes()
                results.append(result)
            elif query['type'] == 'palindromes_of_length':
                result = self.find_palindromes_of_length(query['length'])
                results.append(result)
            elif query['type'] == 'palindromes_in_range':
                result = self.find_palindromes_in_range(query['start'], query['end'])
                results.append(result)
            elif query['type'] == 'analyze':
                result = self.analyze_palindrome_distribution()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_palindrome_statistics()
                results.append(result)
        return results
```

### Variation 3: Longest Palindrome with Constraints
**Problem**: Handle palindrome queries with additional constraints (e.g., minimum length, maximum length, frequency).

**Link**: [CSES Problem Set - Longest Palindrome with Constraints](https://cses.fi/problemset/task/longest_palindrome_constraints)

```python
class LongestPalindromeWithConstraints:
    def __init__(self, s, min_length, max_length, min_frequency):
        self.s = list(s)
        self.n = len(self.s)
        self.min_length = min_length
        self.max_length = max_length
        self.min_frequency = min_frequency
        self.transformed = self._transform_string()
        self.palindrome_lengths = self._manacher_algorithm()
        self.longest_palindrome = self._find_longest_palindrome()
    
    def _transform_string(self):
        """Transform string for Manacher's algorithm"""
        if not self.s:
            return ['#', '$']
        
        transformed = ['#']
        for char in self.s:
            transformed.append(char)
            transformed.append('#')
        transformed.append('$')
        
        return transformed
    
    def _manacher_algorithm(self):
        """Manacher's algorithm to find palindrome lengths"""
        n = len(self.transformed)
        P = [0] * n
        center = 0
        right = 0
        
        for i in range(1, n - 1):
            # Mirror position
            mirror = 2 * center - i
            
            if i < right:
                P[i] = min(right - i, P[mirror])
            
            # Expand around center i
            try:
                while (i + P[i] + 1 < n and 
                       i - P[i] - 1 >= 0 and 
                       self.transformed[i + P[i] + 1] == self.transformed[i - P[i] - 1]):
                    P[i] += 1
            except IndexError:
                pass
            
            # Update center and right boundary if necessary
            if i + P[i] > right:
                center = i
                right = i + P[i]
        
        return P
    
    def _find_longest_palindrome(self):
        """Find the longest palindrome from palindrome lengths"""
        max_length = 0
        center_index = 0
        
        for i in range(len(self.palindrome_lengths)):
            if self.palindrome_lengths[i] > max_length:
                max_length = self.palindrome_lengths[i]
                center_index = i
        
        if max_length == 0:
            return None
        
        # Convert back to original string coordinates
        start = (center_index - max_length) // 2
        end = (center_index + max_length) // 2
        
        return {
            'palindrome': ''.join(self.s[start:end]),
            'start': start,
            'end': end,
            'length': max_length
        }
    
    def constrained_palindrome_query(self):
        """Query palindromes with constraints"""
        valid_palindromes = []
        
        for i in range(len(self.palindrome_lengths)):
            length = self.palindrome_lengths[i]
            
            # Check length constraints
            if length < self.min_length or length > self.max_length:
                continue
            
            # Check frequency constraint (how many times the palindrome appears)
            start = (i - length) // 2
            end = (i + length) // 2
            palindrome = ''.join(self.s[start:end])
            frequency = self._count_palindrome_frequency(palindrome)
            
            if frequency < self.min_frequency:
                continue
            
            valid_palindromes.append({
                'palindrome': palindrome,
                'start': start,
                'end': end,
                'length': length,
                'frequency': frequency
            })
        
        return valid_palindromes
    
    def _count_palindrome_frequency(self, palindrome):
        """Count how many times a palindrome appears in the string"""
        count = 0
        palindrome_length = len(palindrome)
        
        for i in range(self.n - palindrome_length + 1):
            if ''.join(self.s[i:i + palindrome_length]) == palindrome:
                count += 1
        
        return count
    
    def find_valid_palindromes(self):
        """Find all valid palindromes that satisfy constraints"""
        return self.constrained_palindrome_query()
    
    def get_longest_valid_palindrome(self):
        """Get longest valid palindrome that satisfies constraints"""
        valid_palindromes = self.find_valid_palindromes()
        
        if not valid_palindromes:
            return None
        
        longest = max(valid_palindromes, key=lambda x: x['length'])
        return longest
    
    def get_shortest_valid_palindrome(self):
        """Get shortest valid palindrome that satisfies constraints"""
        valid_palindromes = self.find_valid_palindromes()
        
        if not valid_palindromes:
            return None
        
        shortest = min(valid_palindromes, key=lambda x: x['length'])
        return shortest
    
    def get_most_frequent_valid_palindrome(self):
        """Get most frequent valid palindrome that satisfies constraints"""
        valid_palindromes = self.find_valid_palindromes()
        
        if not valid_palindromes:
            return None
        
        most_frequent = max(valid_palindromes, key=lambda x: x['frequency'])
        return most_frequent
    
    def get_least_frequent_valid_palindrome(self):
        """Get least frequent valid palindrome that satisfies constraints"""
        valid_palindromes = self.find_valid_palindromes()
        
        if not valid_palindromes:
            return None
        
        least_frequent = min(valid_palindromes, key=lambda x: x['frequency'])
        return least_frequent
    
    def count_valid_palindromes(self):
        """Count number of valid palindromes"""
        return len(self.find_valid_palindromes())
    
    def get_constraint_statistics(self):
        """Get statistics about valid palindromes"""
        valid_palindromes = self.find_valid_palindromes()
        
        if not valid_palindromes:
            return {
                'count': 0,
                'min_length': 0,
                'max_length': 0,
                'avg_length': 0,
                'min_frequency': 0,
                'max_frequency': 0,
                'avg_frequency': 0
            }
        
        lengths = [p['length'] for p in valid_palindromes]
        frequencies = [p['frequency'] for p in valid_palindromes]
        
        return {
            'count': len(valid_palindromes),
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

lp = LongestPalindromeWithConstraints(s, min_length, max_length, min_frequency)
result = lp.constrained_palindrome_query()
print(f"Constrained palindrome query result: {result}")

valid_palindromes = lp.find_valid_palindromes()
print(f"Valid palindromes: {valid_palindromes}")

longest = lp.get_longest_valid_palindrome()
print(f"Longest valid palindrome: {longest}")
```

### Related Problems

#### **CSES Problems**
- [Longest Palindrome](https://cses.fi/problemset/task/1111) - Basic longest palindrome problem
- [Palindrome Queries](https://cses.fi/problemset/task/2420) - Palindrome queries
- [String Matching](https://cses.fi/problemset/task/1753) - String matching

#### **LeetCode Problems**
- [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) - Find longest palindromic substring
- [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) - Count palindromic substrings
- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) - Check if string is palindrome

#### **Problem Categories**
- **Manacher's Algorithm**: Palindrome detection, string processing, symmetry properties
- **String Processing**: Palindromes, string transformations, pattern matching
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata