---
layout: simple
title: "Minimum Window Substring - Two Pointers Technique"
permalink: /problem_soulutions/sliding_window/minimum_window_substring_analysis
---

# Minimum Window Substring - Two Pointers Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement two pointers technique for minimum window problems
- Apply sliding window technique for variable-size windows with character coverage
- Optimize substring character coverage calculations using hash maps
- Handle edge cases in minimum window problems
- Recognize when to use two pointers vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Two pointers, sliding window, hash maps, string manipulation
- **Data Structures**: Strings, hash maps, sets
- **Mathematical Concepts**: Substring character coverage optimization, window management
- **Programming Skills**: String manipulation, two pointers implementation
- **Related Problems**: Longest substring without repeating, subarray with K distinct, sliding window problems

## 📋 Problem Description

Given two strings s and t, find the minimum window substring of s that contains all characters of t.

**Input**: 
- First line: string s
- Second line: string t

**Output**: 
- Single string: minimum window substring of s that contains all characters of t

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- 1 ≤ |t| ≤ 10⁵
- s and t contain only lowercase English letters

**Example**:
```
Input:
ADOBECODEBANC
ABC

Output:
BANC

Explanation**: 
The minimum window substring that contains all characters of "ABC" is "BANC".
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n³)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each starting position i from 0 to n-1
2. For each ending position j from i to n-1
3. Check if substring from i to j contains all characters of t
4. If yes, update minimum window
5. Return minimum window

**Implementation**:
```python
def brute_force_minimum_window_substring(s, t):
    n = len(s)
    min_window = ""
    min_length = float('inf')
    
    for i in range(n):
        for j in range(i, n):
            substring = s[i:j+1]
            if contains_all_characters(substring, t):
                if len(substring) < min_length:
                    min_length = len(substring)
                    min_window = substring
    
    return min_window

def contains_all_characters(s, t):
    char_count = {}
    for char in t:
        char_count[char] = char_count.get(char, 0) + 1
    
    for char in s:
        if char in char_count:
            char_count[char] -= 1
            if char_count[char] == 0:
                del char_count[char]
    
    return len(char_count) == 0
```

### Approach 2: Optimized with Hash Map
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each starting position i from 0 to n-1
2. Use hash map to track characters from position i
3. For each ending position j from i to n-1
4. Add s[j] to hash map
5. If hash map contains all characters of t, update minimum window
6. Return minimum window

**Implementation**:
```python
def optimized_minimum_window_substring(s, t):
    n = len(s)
    min_window = ""
    min_length = float('inf')
    
    for i in range(n):
        char_count = {}
        for j in range(i, n):
            char_count[s[j]] = char_count.get(s[j], 0) + 1
            if contains_all_characters(char_count, t):
                if j - i + 1 < min_length:
                    min_length = j - i + 1
                    min_window = s[i:j+1]
    
    return min_window

def contains_all_characters(char_count, t):
    for char in t:
        if char not in char_count or char_count[char] == 0:
            return False
    return True
```

### Approach 3: Optimal with Two Pointers
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use two pointers: left and right
2. Use hash map to track frequency of characters in current window
3. Expand right pointer while maintaining character coverage
4. When all characters covered, contract left pointer to minimize window
5. Update minimum window throughout
6. Return minimum window

**Implementation**:
```python
def optimal_minimum_window_substring(s, t):
    n = len(s)
    min_window = ""
    min_length = float('inf')
    
    # Count characters in t
    t_count = {}
    for char in t:
        t_count[char] = t_count.get(char, 0) + 1
    
    left = 0
    window_count = {}
    required = len(t_count)
    formed = 0
    
    for right in range(n):
        # Add character to window
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1
        
        # Check if character count matches requirement
        if char in t_count and window_count[char] == t_count[char]:
            formed += 1
        
        # Try to contract window
        while left <= right and formed == required:
            # Update minimum window
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right+1]
            
            # Remove character from window
            char = s[left]
            window_count[char] -= 1
            if char in t_count and window_count[char] < t_count[char]:
                formed -= 1
            left += 1
    
    return min_window
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all possible substrings |
| Optimized | O(n²) | O(n) | Use hash map for faster character check |
| Optimal | O(n) | O(n) | Use two pointers with hash map |

### Time Complexity
- **Time**: O(n) - Each character is processed at most twice
- **Space**: O(n) - Hash map for character frequencies

### Why This Solution Works
- **Two Pointers**: Use left and right pointers to maintain a sliding window
- **Hash Map Tracking**: Track frequency of characters in current window
- **Window Management**: Expand when not all characters covered, contract when all covered
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Minimum Window Subsequence**
**Problem**: Find the minimum window in string S that contains all characters of string T as a subsequence.

**Key Differences**: Subsequence instead of substring, different matching criteria

**Solution Approach**: Use two pointers with subsequence matching

**Implementation**:
```python
def minimum_window_subsequence(s, t):
    """
    Find minimum window in s that contains t as subsequence
    """
    if not s or not t:
        return ""
    
    min_len = float('inf')
    min_start = 0
    
    for i in range(len(s)):
        if s[i] == t[0]:
            # Try to match subsequence starting from i
            t_idx = 0
            for j in range(i, len(s)):
                if s[j] == t[t_idx]:
                    t_idx += 1
                    if t_idx == len(t):
                        # Found complete subsequence
                        if j - i + 1 < min_len:
                            min_len = j - i + 1
                            min_start = i
                        break
    
    return s[min_start:min_start + min_len] if min_len != float('inf') else ""

# Example usage
s = "abcdebdde"
t = "bde"
result = minimum_window_subsequence(s, t)
print(f"Minimum window subsequence: {result}")  # Output: "bcde"
```

#### **2. Minimum Window Substring with Order**
**Problem**: Find the minimum window in string S that contains all characters of string T in the same order.

**Key Differences**: Characters must appear in the same order as in T

**Solution Approach**: Use sliding window with order tracking

**Implementation**:
```python
def minimum_window_ordered(s, t):
    """
    Find minimum window in s that contains t in order
    """
    if not s or not t:
        return ""
    
    min_len = float('inf')
    min_start = 0
    
    for i in range(len(s)):
        if s[i] == t[0]:
            # Try to match ordered sequence starting from i
            t_idx = 0
            for j in range(i, len(s)):
                if s[j] == t[t_idx]:
                    t_idx += 1
                    if t_idx == len(t):
                        # Found complete ordered sequence
                        if j - i + 1 < min_len:
                            min_len = j - i + 1
                            min_start = i
                        break
    
    return s[min_start:min_start + min_len] if min_len != float('inf') else ""

# Example usage
s = "ADOBECODEBANC"
t = "ABC"
result = minimum_window_ordered(s, t)
print(f"Minimum window ordered: {result}")  # Output: "ADOBEC"
```

#### **3. Minimum Window Substring with Frequency**
**Problem**: Find the minimum window in string S that contains all characters of string T with exact frequency.

**Key Differences**: Must match exact frequency of each character

**Solution Approach**: Use sliding window with frequency tracking

**Implementation**:
```python
def minimum_window_frequency(s, t):
    """
    Find minimum window in s that contains t with exact frequency
    """
    if not s or not t:
        return ""
    
    # Count frequency of characters in t
    t_count = {}
    for char in t:
        t_count[char] = t_count.get(char, 0) + 1
    
    # Track frequency in current window
    window_count = {}
    left = 0
    min_len = float('inf')
    min_start = 0
    matched = 0
    
    for right in range(len(s)):
        # Add current character to window
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1
        
        # Check if we have enough of this character
        if char in t_count and window_count[char] == t_count[char]:
            matched += 1
        
        # Try to shrink window
        while matched == len(t_count):
            # Update minimum window
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_start = left
            
            # Remove leftmost character
            left_char = s[left]
            window_count[left_char] -= 1
            if left_char in t_count and window_count[left_char] < t_count[left_char]:
                matched -= 1
            left += 1
    
    return s[min_start:min_start + min_len] if min_len != float('inf') else ""

# Example usage
s = "ADOBECODEBANC"
t = "ABC"
result = minimum_window_frequency(s, t)
print(f"Minimum window frequency: {result}")  # Output: "BANC"
```

### Related Problems

#### **CSES Problems**
- [Minimum Window Substring](https://cses.fi/problemset/task/2101) - Find minimum window containing all characters
- [Substring with All Characters](https://cses.fi/problemset/task/2102) - Find substring containing all characters
- [Minimum Window Subsequence](https://cses.fi/problemset/task/2103) - Find minimum window containing subsequence

#### **LeetCode Problems**
- [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) - Classic minimum window problem
- [Minimum Window Subsequence](https://leetcode.com/problems/minimum-window-subsequence/) - Subsequence variant
- [Longest Substring with At Most Two Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/) - Two distinct characters
- [Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) - Word concatenation variant

#### **Problem Categories**
- **Sliding Window**: Minimum window problems, character coverage, window optimization
- **Two Pointers**: Left and right pointer technique, window expansion and contraction
- **Hash Map**: Character frequency tracking, efficient lookups
- **String Processing**: Substring analysis, character matching, pattern recognition

## 🚀 Key Takeaways

- **Two Pointers Technique**: The standard approach for minimum window problems
- **Sliding Window**: Maintain a window that covers all required characters
- **Hash Map Tracking**: Use hash map to track character frequencies efficiently
- **Window Management**: Expand and contract window based on character coverage
- **Pattern Recognition**: This technique applies to many minimum window problems