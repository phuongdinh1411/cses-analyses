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

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Palindrome detection, Manacher's algorithm, center expansion
- **Data Structures**: Strings, arrays, character arrays
- **Mathematical Concepts**: Palindrome properties, symmetry, string theory
- **Programming Skills**: String manipulation, algorithm implementation, symmetry detection
- **Related Problems**: String Matching (pattern matching), Pattern Positions (string algorithms)

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