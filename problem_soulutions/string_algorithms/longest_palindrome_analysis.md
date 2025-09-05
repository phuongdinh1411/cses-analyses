---
layout: simple
title: "Longest Palindrome - Longest Palindromic Substring"
permalink: /problem_soulutions/string_algorithms/longest_palindrome_analysis
---

# Longest Palindrome - Longest Palindromic Substring

## 📋 Problem Description

Given a string, find the longest palindromic substring.

This is a classic string algorithm problem that requires finding the longest substring that reads the same forwards and backwards. The solution involves using efficient algorithms like Manacher's algorithm or expand around centers approach to achieve linear time complexity.

**Input**: 
- First line: A string s

**Output**: 
- Print the longest palindromic substring

**Constraints**:
- 1 ≤ |s| ≤ 10⁶

**Example**:
```
Input:
babad

Output:
bab

Explanation**: 
- String: "babad"
- Possible palindromes: "b", "a", "b", "a", "d", "aba", "bab"
- Longest palindrome: "bab" (length 3)
- Alternative: "aba" is also valid with same length
```

## 🎯 Visual Example

### Input
```
String: "babad"
```

### Palindrome Detection Process
```
Step 1: Check all possible palindromes
- Length 1: "b", "a", "b", "a", "d" (all palindromes)
- Length 2: "ba", "ab", "ba", "ad" (none are palindromes)
- Length 3: "bab", "aba", "bad" (first two are palindromes)
- Length 4: "baba", "abad" (none are palindromes)
- Length 5: "babad" (not a palindrome)

Step 2: Find longest palindrome
- "bab" (length 3) - centered at index 1
- "aba" (length 3) - centered at index 2
- Both are valid longest palindromes
```

### Palindrome Visualization
```
String: b a b a d
Index:  0 1 2 3 4

Palindrome "bab" (centered at index 1):
b a b a d
  ↑
  b a b
  ✓ ✓ ✓

Palindrome "aba" (centered at index 2):
b a b a d
    ↑
    a b a
    ✓ ✓ ✓
```

### Key Insight
Expand around centers algorithm works by:
1. For each position, expand left and right to find longest palindrome
2. Handle both odd-length (center at character) and even-length (center between characters) palindromes
3. Time complexity: O(n²) for expand around centers
4. Space complexity: O(1) for the algorithm
5. Manacher's algorithm achieves O(n) time complexity

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find the longest substring that is a palindrome
- **Key Insight**: Use expand around centers or Manacher's algorithm for efficiency
- **Challenge**: Handle large strings efficiently without O(|s|³) complexity

### Step 2: Initial Approach
**Check all substrings (inefficient but correct):**

```python
def longest_palindrome_naive(s):
    n = len(s)
    max_length = 1
    start = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            substring = s[i:j + 1]
            if substring == substring[::-1]:
                if j - i + 1 > max_length:
                    max_length = j - i + 1
                    start = i
    
    return s[start:start + max_length]
```

**Why this is inefficient**: Cubic time complexity for large strings.

### Improvement 1: Expand Around Center - O(|s|²)
**Description**: For each position, expand around it to find palindromes.

```python
def longest_palindrome_expand(s):
    n = len(s)
    max_length = 1
    start = 0
    
    def expand_around_center(left, right):
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(n):
        # Check odd length palindromes
        len1 = expand_around_center(i, i)
        if len1 > max_length:
            max_length = len1
            start = i - len1 // 2
        
        # Check even length palindromes
        len2 = expand_around_center(i, i + 1)
        if len2 > max_length:
            max_length = len2
            start = i - len2 // 2 + 1
    
    return s[start:start + max_length]
```

**Why this improvement works**: Expand around center reduces time complexity to quadratic.
### Improvement 2: Manacher's Algorithm - O(|s|)
**Description**: Use Manacher's algorithm to find the longest palindrome in linear time.

```python
def longest_palindrome_manacher(s):
    # Transform string to handle even length palindromes
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    
    center = right = 0
    
    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        # Expand around current center
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        # Update center and right boundary
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find the longest palindrome
    max_length = max(p)
    center_index = p.index(max_length)
    
    # Convert back to original string indices
    start = (center_index - max_length) // 2
    end = (center_index + max_length) // 2
    
    return s[start:end]
```

**Why this improvement works**: Manacher's algorithm uses palindrome properties to achieve linear time.

### Step 3: Optimization/Alternative
**Dynamic Programming approach:**

```python
def longest_palindrome_dp(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    
    # All single characters are palindromes
    for i in range(n):
        dp[i][i] = True
    
    max_length = 1
    start = 0
    
    # Check for length 2 palindromes
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            max_length = 2
            start = i
    
    # Check for length > 2 palindromes
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_length:
                    max_length = length
                    start = i
    
    return s[start:start + max_length]
```

**Why this works**: Dynamic programming builds solutions from smaller subproblems.

### Step 4: Complete Solution

```python
s = input().strip()

def longest_palindrome_manacher(s):
    # Transform string to handle even length palindromes
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    
    center = right = 0
    
    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        # Expand around current center
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        # Update center and right boundary
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find the longest palindrome
    max_length = max(p)
    center_index = p.index(max_length)
    
    # Convert back to original string indices
    start = (center_index - max_length) // 2
    end = (center_index + max_length) // 2
    
    return s[start:end]

result = longest_palindrome_manacher(s)
print(result)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic palindrome (should return longest palindrome)
- **Test 2**: No palindrome (should return single character)
- **Test 3**: Multiple palindromes (should return longest)
- **Test 4**: Even length palindrome (should handle correctly)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|³) | O(1) | Check all substrings |
| Expand Centers | O(|s|²) | O(1) | Expand around each center |
| Dynamic Programming | O(|s|²) | O(|s|²) | Build from smaller subproblems |
| Manacher's | O(|s|) | O(|s|) | Use palindrome properties |

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|³) | O(|s|) | Check all substrings |
| Expand Around Center | O(|s|²) | O(1) | Expand from each position |
| Manacher's | O(|s|) | O(|s|) | Use palindrome properties |
| Dynamic Programming | O(|s|²) | O(|s|²) | Build from subproblems |

## 🎨 Visual Example

### Input Example
```
String: "babad"
```

### All Possible Palindromes
```
String: b a b a d
Index:  0 1 2 3 4

Single characters (always palindromes):
- "b" at index 0
- "a" at index 1  
- "b" at index 2
- "a" at index 3
- "d" at index 4

Two characters:
- "ba" at indices 0-1: b ≠ a ✗
- "ab" at indices 1-2: a ≠ b ✗
- "ba" at indices 2-3: b ≠ a ✗
- "ad" at indices 3-4: a ≠ d ✗

Three characters:
- "bab" at indices 0-2: b = b ✓ (length 3)
- "aba" at indices 1-3: a = a ✓ (length 3)
- "bad" at indices 2-4: b ≠ d ✗

Four characters:
- "baba" at indices 0-3: b ≠ a ✗
- "abad" at indices 1-4: a ≠ d ✗

Five characters:
- "babad" at indices 0-4: b ≠ d ✗

Longest palindromes: "bab" and "aba" (both length 3)
```

### Expand Around Centers Approach
```
String: b a b a d
Index:  0 1 2 3 4

Center at index 0 (odd length):
b a b a d
↑
Expand: left=0, right=0
- s[0] = s[0] ✓ → "b" (length 1)
- left=-1, right=1 → stop (out of bounds)

Center at index 1 (odd length):
b a b a d
  ↑
Expand: left=1, right=1
- s[1] = s[1] ✓ → "a" (length 1)
- left=0, right=2: s[0] = s[2] ✓ → "bab" (length 3)
- left=-1, right=3 → stop (out of bounds)

Center at index 2 (odd length):
b a b a d
    ↑
Expand: left=2, right=2
- s[2] = s[2] ✓ → "b" (length 1)
- left=1, right=3: s[1] = s[3] ✓ → "aba" (length 3)
- left=0, right=4: s[0] ≠ s[4] ✗ → stop

Center at index 3 (odd length):
b a b a d
      ↑
Expand: left=3, right=3
- s[3] = s[3] ✓ → "a" (length 1)
- left=2, right=4: s[2] ≠ s[4] ✗ → stop

Center at index 4 (odd length):
b a b a d
        ↑
Expand: left=4, right=4
- s[4] = s[4] ✓ → "d" (length 1)
- left=3, right=5 → stop (out of bounds)

Center between 0-1 (even length):
b a b a d
↑
Expand: left=0, right=1
- s[0] ≠ s[1] ✗ → stop

Center between 1-2 (even length):
b a b a d
  ↑
Expand: left=1, right=2
- s[1] ≠ s[2] ✗ → stop

Center between 2-3 (even length):
b a b a d
    ↑
Expand: left=2, right=3
- s[2] ≠ s[3] ✗ → stop

Center between 3-4 (even length):
b a b a d
      ↑
Expand: left=3, right=4
- s[3] ≠ s[4] ✗ → stop

Result: Longest palindrome is "bab" or "aba" (length 3)
```

### Manacher's Algorithm Process
```
Original: b a b a d
Transformed: # b # a # b # a # d #
Index:        0 1 2 3 4 5 6 7 8 9 10 11

Radius array (R):
Index: 0 1 2 3 4 5 6 7 8 9 10 11
String: # b # a # b # a # d #
R:      0 1 0 3 0 1 0 3 0 1 0 0

Explanation:
- R[1] = 1: "b" is palindrome of radius 1
- R[3] = 3: "a#b#a" is palindrome of radius 3
- R[5] = 1: "b" is palindrome of radius 1  
- R[7] = 3: "a#b#a" is palindrome of radius 3
- R[9] = 1: "d" is palindrome of radius 1

Longest palindrome: radius 3 → length 3
Original positions: "bab" or "aba"
```

### Dynamic Programming Approach
```
String: b a b a d
Index:  0 1 2 3 4

DP Table (dp[i][j] = true if s[i:j+1] is palindrome):
    0 1 2 3 4
0   T F T F F
1     T F T F
2       T F F
3         T F
4           T

Explanation:
- dp[0][0] = T: "b" is palindrome
- dp[1][1] = T: "a" is palindrome
- dp[0][2] = T: "bab" is palindrome (s[0]=s[2] and dp[1][1]=T)
- dp[2][2] = T: "b" is palindrome
- dp[1][3] = T: "aba" is palindrome (s[1]=s[3] and dp[2][2]=T)
- dp[3][3] = T: "a" is palindrome
- dp[4][4] = T: "d" is palindrome

Longest palindromes: "bab" (indices 0-2) and "aba" (indices 1-3)
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Naive           │ O(n³)        │ O(1)         │ Check all    │
│                 │              │              │ substrings   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Expand Centers  │ O(n²)        │ O(1)         │ Expand from  │
│                 │              │              │ each center  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dynamic Prog    │ O(n²)        │ O(n²)        │ Build from   │
│                 │              │              │ subproblems  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Manacher's      │ O(n)         │ O(n)         │ Use palindrome│
│                 │              │              │ properties   │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Palindrome Detection Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: string s │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Choose Algorithm│
              │ (Expand/Manacher)│
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each center │
              │ (position)      │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Expand left and │
              │ right while     │
              │ characters match│
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Update longest  │
              │ palindrome      │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return longest  │
              │ palindrome      │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **Manacher's Algorithm**: Use palindrome properties for linear time
- **Expand Around Centers**: Check palindromes from each position
- **Dynamic Programming**: Build solutions from smaller subproblems
- **String Transformation**: Handle even/odd length palindromes

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Longest Palindrome with Character Constraints**
```python
def longest_palindrome_constrained(s, allowed_chars):
    # Handle palindromes with character constraints
    
    def is_valid_palindrome(substring):
        return all(char in allowed_chars for char in substring)
    
    def expand_around_center(s, left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if is_valid_palindrome(s[left:right + 1]):
                left -= 1
                right += 1
            else:
                break
        return s[left + 1:right]
    
    max_palindrome = ""
    
    for i in range(len(s)):
        # Odd length palindromes
        palindrome1 = expand_around_center(s, i, i)
        if len(palindrome1) > len(max_palindrome):
            max_palindrome = palindrome1
        
        # Even length palindromes
        palindrome2 = expand_around_center(s, i, i + 1)
        if len(palindrome2) > len(max_palindrome):
            max_palindrome = palindrome2
    
    return max_palindrome
```

#### **2. Longest Palindrome with Length Constraints**
```python
def longest_palindrome_length_constrained(s, min_length, max_length):
    # Handle palindromes with length constraints
    
    def expand_around_center(s, left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    
    max_palindrome = ""
    
    for i in range(len(s)):
        # Odd length palindromes
        palindrome1 = expand_around_center(s, i, i)
        if min_length <= len(palindrome1) <= max_length and len(palindrome1) > len(max_palindrome):
            max_palindrome = palindrome1
        
        # Even length palindromes
        palindrome2 = expand_around_center(s, i, i + 1)
        if min_length <= len(palindrome2) <= max_length and len(palindrome2) > len(max_palindrome):
            max_palindrome = palindrome2
    
    return max_palindrome
```

#### **3. Longest Palindrome with Dynamic Updates**
```python
def longest_palindrome_dynamic(operations):
    # Handle palindromes with dynamic string updates
    
    s = ""
    max_palindrome = ""
    
    for operation in operations:
        if operation[0] == 'add':
            # Add character to string
            char = operation[1]
            s += char
            
            # Recalculate longest palindrome
            max_palindrome = calculate_longest_palindrome(s)
        
        elif operation[0] == 'remove':
            # Remove last character
            if len(s) > 0:
                s = s[:-1]
                max_palindrome = calculate_longest_palindrome(s)
        
        elif operation[0] == 'query':
            # Return current longest palindrome
            yield max_palindrome
    
    return list(longest_palindrome_dynamic(operations))

def calculate_longest_palindrome(s):
    if len(s) == 0:
        return ""
    
    def expand_around_center(s, left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    
    max_palindrome = ""
    
    for i in range(len(s)):
        # Odd length palindromes
        palindrome1 = expand_around_center(s, i, i)
        if len(palindrome1) > len(max_palindrome):
            max_palindrome = palindrome1
        
        # Even length palindromes
        palindrome2 = expand_around_center(s, i, i + 1)
        if len(palindrome2) > len(max_palindrome):
            max_palindrome = palindrome2
    
    return max_palindrome
```

## 🔗 Related Problems

### Links to Similar Problems
- **Palindrome Problems**: String palindrome detection
- **String Algorithms**: Advanced string processing
- **Dynamic Programming**: String DP problems
- **Manacher's Algorithm**: Linear time palindrome algorithms

## 📚 Learning Points

### Key Takeaways
- **Manacher's algorithm** provides optimal O(|s|) solution
- **Expand around centers** is intuitive and efficient
- **Dynamic programming** builds from smaller subproblems
- **String transformation** handles even/odd length cases

## Key Insights for Other Problems

### 1. **Palindrome Problems**
**Principle**: Use specialized algorithms like Manacher's for efficient palindrome detection.
**Applicable to**:
- Palindrome problems
- String algorithms
- Pattern matching
- Algorithm design

**Example Problems**:
- Palindrome problems
- String algorithms
- Pattern matching
- Algorithm design

### 2. **String Transformation**
**Principle**: Transform strings to handle edge cases more easily.
**Applicable to**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

### 3. **Palindrome Properties**
**Principle**: Use palindrome properties to optimize algorithms.
**Applicable to**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

### 4. **Dynamic Programming on Strings**
**Principle**: Use DP to build solutions from smaller subproblems.
**Applicable to**:
- String algorithms
- Dynamic programming
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Dynamic programming
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **Manacher's Algorithm Pattern**
```python
def manacher_palindrome(s):
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    
    center = right = 0
    
    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    return p
```

### 2. **Expand Around Center Pattern**
```python
def expand_around_center(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    max_length = 1
    start = 0
    
    for i in range(len(s)):
        len1 = expand(i, i)
        len2 = expand(i, i + 1)
        
        if len1 > max_length:
            max_length = len1
            start = i - len1 // 2
        
        if len2 > max_length:
            max_length = len2
            start = i - len2 // 2 + 1
    
    return s[start:start + max_length]
```

### 3. **DP Palindrome Pattern**
```python
def dp_palindrome(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    
    for i in range(n):
        dp[i][i] = True
    
    max_length = 1
    start = 0
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j] and (length == 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                if length > max_length:
                    max_length = length
                    start = i
    
    return s[start:start + max_length]
```

## Edge Cases to Remember

1. **Single character**: Return the character itself
2. **All same characters**: Return the entire string
3. **No palindromes**: Return the first character
4. **Empty string**: Handle appropriately
5. **Multiple palindromes**: Return the longest one

## Problem-Solving Framework

1. **Identify palindrome nature**: This is a longest palindrome problem
2. **Choose algorithm**: Use Manacher's algorithm for efficiency
3. **Transform string**: Add separators to handle even length palindromes
4. **Find palindromes**: Use palindrome properties to expand efficiently
5. **Return result**: Return the longest palindromic substring

---

*This analysis shows how to efficiently find the longest palindromic substring using Manacher's algorithm and other techniques.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Longest Palindrome with Constraints**
**Problem**: Find longest palindrome with additional constraints (length, alphabet, etc.).
```python
def constrained_longest_palindrome(s, constraints):
    # constraints = {'min_length': x, 'max_length': y, 'alphabet': chars}
    
    n = len(s)
    
    # Apply constraints
    if 'alphabet' in constraints:
        if not all(c in constraints['alphabet'] for c in s):
            return ""
    
    if 'min_length' in constraints and n < constraints['min_length']:
        return ""
    
    if 'max_length' in constraints:
        n = min(n, constraints['max_length'])
    
    # Use Manacher's algorithm
    t = '#' + '#'.join(s[:n]) + '#'
    n_t = len(t)
    p = [0] * n_t
    
    center = right = 0
    
    for i in range(n_t):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n_t and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find longest palindrome within constraints
    max_length = 0
    start = 0
    
    for i in range(n_t):
        length = p[i]
        if 'min_length' in constraints:
            length = max(length, constraints['min_length'])
        if length > max_length:
            max_length = length
            start = (i - p[i]) // 2
    
    return s[start:start + max_length] if max_length > 0 else ""
```

#### **Variation 2: Longest Palindrome with Costs**
**Problem**: Each character has a cost, find longest palindrome with minimum cost.
```python
def cost_based_longest_palindrome(s, char_costs):
    # char_costs[c] = cost of character c
    
    n = len(s)
    t = '#' + '#'.join(s) + '#'
    n_t = len(t)
    p = [0] * n_t
    
    center = right = 0
    
    for i in range(n_t):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        left = i - (p[i] + 1)
        right_expand = i + (p[i] + 1)
        
        while left >= 0 and right_expand < n_t and t[left] == t[right_expand]:
            p[i] += 1
            left -= 1
            right_expand += 1
        
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find palindrome with minimum cost
    max_length = 0
    min_cost = float('inf')
    best_palindrome = ""
    
    for i in range(n_t):
        length = p[i]
        start = (i - p[i]) // 2
        palindrome = s[start:start + length]
        cost = sum(char_costs.get(c, 1) for c in palindrome)
        
        if length > max_length or (length == max_length and cost < min_cost):
            max_length = length
            min_cost = cost
            best_palindrome = palindrome
    
    return best_palindrome
```

#### **Variation 3: Longest Palindrome with Probabilities**
**Problem**: Characters have probabilities, find expected longest palindrome.
```python
def probabilistic_longest_palindrome(s, char_probs):
    # char_probs[c] = probability of character c
    
    n = len(s)
    # For probabilistic strings, calculate expected longest palindrome
    expected_length = 0
    
    # Calculate expected length based on character probabilities
    for length in range(1, n + 1):
        for start in range(n - length + 1):
            prob_palindrome = 1.0
            for i in range(length // 2):
                if start + i < n and start + length - 1 - i < n:
                    if s[start + i] == s[start + length - 1 - i]:
                        prob_palindrome *= char_probs.get(s[start + i], 0.1)
                    else:
                        prob_palindrome = 0
                        break
            
            if prob_palindrome >= 0.5:  # Threshold for "palindrome"
                expected_length = max(expected_length, length)
    
    return s[:expected_length] if expected_length > 0 else ""
```

#### **Variation 4: Longest Palindrome with Updates**
**Problem**: Handle dynamic updates to the string and find new longest palindrome.
```python
def dynamic_longest_palindrome(s, updates):
    # updates = [(pos, new_char), ...]
    
    s = list(s)  # Convert to list for updates
    palindrome_history = []
    
    for pos, new_char in updates:
        s[pos] = new_char
        # Find longest palindrome after each update
        palindrome = expand_around_center(''.join(s))
        palindrome_history.append(palindrome)
    
    return palindrome_history
```

#### **Variation 5: Longest Palindrome with Multiple Strings**
**Problem**: Find longest palindrome among multiple strings.
```python
def multiple_string_longest_palindrome(strings):
    # Find longest palindrome among all strings
    
    longest_palindrome = ""
    
    for s in strings:
        palindrome = expand_around_center(s)
        if len(palindrome) > len(longest_palindrome):
            longest_palindrome = palindrome
    
    return longest_palindrome
```

### 🔗 **Related Problems & Concepts**

#### **1. Palindrome Problems**
- **Palindrome Checking**: Check if string is palindrome
- **Palindrome Counting**: Count palindromic substrings
- **Palindrome Partitioning**: Partition string into palindromes
- **Palindrome Construction**: Construct palindromes

#### **2. String Analysis Problems**
- **Symmetry Analysis**: Analyze symmetric properties
- **Mirror Properties**: Study mirror-like properties
- **Center Analysis**: Analyze center-based properties
- **Border Analysis**: Find borders and periods

#### **3. String Algorithms**
- **Manacher's Algorithm**: Efficient palindrome finding
- **Expand Around Center**: Simple palindrome algorithm
- **Dynamic Programming**: DP approach to palindromes
- **Suffix Structures**: Suffix arrays, suffix trees

#### **4. Optimization Problems**
- **Maximization**: Find maximum value solutions
- **Cost Optimization**: Optimize with respect to costs
- **Constrained Optimization**: Optimization with constraints
- **Multi-objective Optimization**: Optimize multiple criteria

#### **5. Algorithmic Techniques**
- **Two Pointers**: Use two pointers for efficiency
- **Sliding Window**: Process data in windows
- **String Transformation**: Transform strings for easier processing
- **Center Expansion**: Expand around centers

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    palindrome = expand_around_center(s)
    print(len(palindrome))
    print(palindrome)
```

#### **2. Range Queries on Longest Palindromes**
```python
def range_longest_palindrome_queries(s, queries):
    # queries = [(l, r), ...] - find longest palindrome in s[l:r]
    
    results = []
    for l, r in queries: substring = s[
l: r]
        palindrome = expand_around_center(substring)
        results.append(palindrome)
    
    return results
```

#### **3. Interactive Longest Palindrome Problems**
```python
def interactive_longest_palindrome():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        palindrome = expand_around_center(s)
        print(f"String: {s}")
        print(f"Longest palindrome: {palindrome}")
        print(f"Length: {len(palindrome)}")
```

### 🧮 **Mathematical Extensions**

#### **1. Symmetry Theory**
- **Symmetry Groups**: Study of symmetric structures
- **Reflection Symmetry**: Mirror-like symmetry
- **Rotational Symmetry**: Rotation-based symmetry
- **Translational Symmetry**: Translation-based symmetry

#### **2. Combinatorial Analysis**
- **Palindrome Enumeration**: Count palindromes with properties
- **Symmetry Enumeration**: Count symmetric structures
- **Pattern Enumeration**: Count patterns in palindromes
- **Combinatorial Counting**: Count combinations and permutations

#### **3. String Theory**
- **String Properties**: Periodicity, borders, periods
- **String Functions**: Mathematical functions on strings
- **String Complexity**: Complexity measures for strings
- **String Transformations**: Mathematical transformations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **String Matching**: KMP, Boyer-Moore, Rabin-Karp algorithms
- **Suffix Structures**: Suffix arrays, suffix trees, suffix automata
- **String Compression**: LZ77, LZ78, Huffman coding
- **String Parsing**: Regular expressions, context-free parsing

#### **2. Mathematical Concepts**
- **Combinatorics**: String combinatorics and counting
- **Group Theory**: Symmetry groups and transformations
- **Number Theory**: Properties of integers and sequences
- **Geometry**: Geometric properties of strings

#### **3. Programming Concepts**
- **String Manipulation**: Efficient string operations
- **Algorithm Design**: Systematic approach to problem solving
- **Complexity Analysis**: Time and space complexity
- **Optimization Techniques**: Improving algorithm performance

---

*This analysis demonstrates efficient longest palindrome finding techniques and shows various extensions for palindrome problems.* 