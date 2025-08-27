# CSES Longest Palindrome - Problem Analysis

## Problem Statement
Given a string, find the longest palindromic substring.

### Input
The first input line has a string s.

### Output
Print the longest palindromic substring.

### Constraints
- 1 ≤ |s| ≤ 10^6

### Example
```
Input:
babad

Output:
bab
```

## Solution Progression

### Approach 1: Check All Substrings - O(|s|³)
**Description**: Check all possible substrings to find the longest palindrome.

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

### Alternative: Dynamic Programming - O(|s|²)
**Description**: Use dynamic programming to find the longest palindrome.

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

## Final Optimal Solution

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

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|³) | O(|s|) | Check all substrings |
| Expand Around Center | O(|s|²) | O(1) | Expand from each position |
| Manacher's | O(|s|) | O(|s|) | Use palindrome properties |
| Dynamic Programming | O(|s|²) | O(|s|²) | Build from subproblems |

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