---
layout: simple
title: "Longest Substring Without Repeating - Two Pointers Technique"
permalink: /problem_soulutions/sliding_window/longest_substring_without_repeating_analysis
---

# Longest Substring Without Repeating - Two Pointers Technique

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand and implement two pointers technique for substring problems
- Apply sliding window technique for variable-size windows with character constraints
- Optimize substring distinct character calculations using hash maps
- Handle edge cases in substring problems
- Recognize when to use two pointers vs other approaches

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Two pointers, sliding window, hash maps, string manipulation
- **Data Structures**: Strings, hash maps, sets
- **Mathematical Concepts**: Substring distinct character optimization, window management
- **Programming Skills**: String manipulation, two pointers implementation
- **Related Problems**: Subarray distinct values, subarray with K distinct, sliding window problems

## 📋 Problem Description

Given a string, find the length of the longest substring without repeating characters.

**Input**: 
- First line: string s

**Output**: 
- Single integer: length of longest substring without repeating characters

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- s contains only lowercase English letters

**Example**:
```
Input:
abcabcbb

Output:
3

Explanation**: 
The longest substring without repeating characters is "abc" with length 3.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n³)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each starting position i from 0 to n-1
2. For each ending position j from i to n-1
3. Check if substring from i to j has no repeating characters
4. If yes, update maximum length
5. Return maximum length

**Implementation**:
```python
def brute_force_longest_substring_without_repeating(s):
    n = len(s)
    max_length = 0
    
    for i in range(n):
        for j in range(i, n):
            substring = s[i:j+1]
            if len(set(substring)) == len(substring):
                max_length = max(max_length, j - i + 1)
    
    return max_length
```

### Approach 2: Optimized with Hash Map
**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

**Algorithm**:
1. For each starting position i from 0 to n-1
2. Use hash map to track characters from position i
3. For each ending position j from i to n-1
4. Add s[j] to hash map
5. If hash map size equals substring length, update maximum length
6. Return maximum length

**Implementation**:
```python
def optimized_longest_substring_without_repeating(s):
    n = len(s)
    max_length = 0
    
    for i in range(n):
        char_count = {}
        for j in range(i, n):
            char_count[s[j]] = char_count.get(s[j], 0) + 1
            if len(char_count) == j - i + 1:
                max_length = max(max_length, j - i + 1)
    
    return max_length
```

### Approach 3: Optimal with Two Pointers
**Time Complexity**: O(n)  
**Space Complexity**: O(n)

**Algorithm**:
1. Use two pointers: left and right
2. Use hash map to track frequency of characters in current window
3. Expand right pointer while maintaining no repeating characters
4. When duplicate found, contract left pointer until no duplicates
5. Update maximum length throughout
6. Return maximum length

**Implementation**:
```python
def optimal_longest_substring_without_repeating(s):
    n = len(s)
    left = 0
    max_length = 0
    char_count = {}
    
    for right in range(n):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        while char_count[s[right]] > 1:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all possible substrings |
| Optimized | O(n²) | O(n) | Use hash map for faster distinct check |
| Optimal | O(n) | O(n) | Use two pointers with hash map |

### Time Complexity
- **Time**: O(n) - Each character is processed at most twice
- **Space**: O(n) - Hash map for character frequencies

### Why This Solution Works
- **Two Pointers**: Use left and right pointers to maintain a sliding window
- **Hash Map Tracking**: Track frequency of characters in current window
- **Window Management**: Expand when no duplicates, contract when duplicate found
- **Optimal Approach**: O(n) time complexity is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Longest Substring with At Most K Distinct Characters**
**Problem**: Find the length of the longest substring that contains at most k distinct characters.

**Key Differences**: Allow k distinct characters instead of no repeats

**Solution Approach**: Use sliding window with character count tracking

**Implementation**:
```python
def longest_substring_k_distinct(s, k):
    """
    Find longest substring with at most k distinct characters
    """
    if not s or k == 0:
        return 0
    
    char_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Add current character
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink window if more than k distinct characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage
s = "eceba"
k = 2
result = longest_substring_k_distinct(s, k)
print(f"Longest substring with {k} distinct chars: {result}")  # Output: 3
```

#### **2. Longest Substring with At Most Two Distinct Characters**
**Problem**: Find the length of the longest substring that contains at most two distinct characters.

**Key Differences**: Specifically two distinct characters

**Solution Approach**: Use sliding window with character count tracking

**Implementation**:
```python
def longest_substring_two_distinct(s):
    """
    Find longest substring with at most two distinct characters
    """
    if len(s) <= 2:
        return len(s)
    
    char_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Add current character
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink window if more than 2 distinct characters
        while len(char_count) > 2:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage
s = "eceba"
result = longest_substring_two_distinct(s)
print(f"Longest substring with 2 distinct chars: {result}")  # Output: 3
```

#### **3. Longest Substring with At Most K Repeating Characters**
**Problem**: Find the length of the longest substring where each character appears at most k times.

**Key Differences**: Limit frequency of each character instead of distinct count

**Solution Approach**: Use sliding window with frequency tracking

**Implementation**:
```python
def longest_substring_k_repeating(s, k):
    """
    Find longest substring where each character appears at most k times
    """
    if not s or k == 0:
        return 0
    
    char_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Add current character
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink window if any character appears more than k times
        while char_count[s[right]] > k:
            char_count[s[left]] -= 1
            left += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage
s = "aaabb"
k = 3
result = longest_substring_k_repeating(s, k)
print(f"Longest substring with {k} repeating chars: {result}")  # Output: 3
```

### Related Problems

#### **CSES Problems**
- [Longest Substring Without Repeating Characters](https://cses.fi/problemset/task/2101) - Find longest substring with unique characters
- [Substring with K Distinct Characters](https://cses.fi/problemset/task/2102) - Find substring with exactly k distinct characters
- [Longest Substring with At Most K Distinct Characters](https://cses.fi/problemset/task/2103) - Find longest substring with at most k distinct characters

#### **LeetCode Problems**
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) - Classic sliding window problem
- [Longest Substring with At Most Two Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/) - Two distinct characters variant
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) - K distinct characters variant
- [Longest Substring with At Most K Repeating Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-repeating-characters/) - K repeating characters variant

#### **Problem Categories**
- **Sliding Window**: Substring problems, character frequency tracking, window management
- **Two Pointers**: Left and right pointer technique, window expansion and contraction
- **Hash Map**: Character frequency tracking, efficient lookups
- **String Processing**: Substring analysis, character counting, pattern matching

## 🚀 Key Takeaways

- **Two Pointers Technique**: The standard approach for substring problems
- **Sliding Window**: Maintain a window with no repeating characters
- **Hash Map Tracking**: Use hash map to track character frequencies efficiently
- **Window Management**: Expand and contract window based on character uniqueness
- **Pattern Recognition**: This technique applies to many substring problems