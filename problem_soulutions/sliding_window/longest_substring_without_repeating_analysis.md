# CSES Longest Substring Without Repeating Characters - Problem Analysis

## Problem Statement
Given a string, find the length of the longest substring without repeating characters.

### Input
The first input line has a string s.

### Output
Print one integer: the length of the longest substring without repeating characters.

### Constraints
- 1 ≤ |s| ≤ 10^5

### Example
```
Input:
abcabcbb

Output:
3
```

## Solution Progression

### Approach 1: Check All Substrings - O(n³)
**Description**: Check all possible substrings to find the longest one without repeating characters.

```python
def longest_substring_naive(s):
    n = len(s)
    max_length = 0
    
    for i in range(n):
        for j in range(i, n):
            substring = s[i:j+1]
            if len(set(substring)) == len(substring):
                max_length = max(max_length, len(substring))
    
    return max_length
```

**Why this is inefficient**: Cubic time complexity for large strings.

### Improvement 1: Sliding Window with Hash Set - O(n)
**Description**: Use sliding window technique with hash set to track unique characters.

```python
def longest_substring_sliding_window(s):
    n = len(s)
    left = 0
    max_length = 0
    char_set = set()
    
    for right in range(n):
        # If character is already in set, shrink window from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character to set
        char_set.add(s[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

**Why this improvement works**: Sliding window efficiently maintains a window with unique characters.

### Alternative: Sliding Window with Hash Map - O(n)
**Description**: Use sliding window with hash map to track character frequencies.

```python
def longest_substring_hash_map(s):
    n = len(s)
    left = 0
    max_length = 0
    char_count = {}
    
    for right in range(n):
        # Add current character
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink window if we have repeating characters
        while char_count[s[right]] > 1:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

**Why this works**: Hash map efficiently tracks character frequencies in the current window.

## Final Optimal Solution

```python
s = input().strip()

def longest_substring_sliding_window(s):
    n = len(s)
    left = 0
    max_length = 0
    char_set = set()
    
    for right in range(n):
        # If character is already in set, shrink window from left
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character to set
        char_set.add(s[right])
        
        # Update maximum length
        max_length = max(max_length, right - left + 1)
    
    return max_length

result = longest_substring_sliding_window(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n³) | O(n) | Check all substrings |
| Sliding Window | O(n) | O(min(m,n)) | Use hash set for unique characters |
| Hash Map | O(n) | O(min(m,n)) | Use hash map for frequency |

## Key Insights for Other Problems

### 1. **Longest Substring Problems**
**Principle**: Use sliding window to efficiently find the longest substring satisfying constraints.
**Applicable to**: Longest substring problems, string algorithms, sliding window applications

### 2. **Sliding Window Technique**
**Principle**: Use sliding window to maintain constraints while expanding and contracting the window.
**Applicable to**: Window-based problems, string problems, two pointer problems

### 3. **Hash Set/Map for Uniqueness**
**Principle**: Use hash set/map to efficiently track unique elements in the current window.
**Applicable to**: Uniqueness problems, frequency counting, hash applications

## Notable Techniques

### 1. **Sliding Window Pattern**
```python
def sliding_window_unique_substring(s):
    left = 0
    max_length = 0
    char_set = set()
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### 2. **Hash Map Pattern**
```python
def hash_map_unique_substring(s):
    left = 0
    max_length = 0
    char_count = {}
    
    for right in range(len(s)):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        while char_count[s[right]] > 1:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

## Problem-Solving Framework

1. **Identify substring nature**: This is a longest substring without repeating characters problem
2. **Choose approach**: Use sliding window with hash set for efficiency
3. **Track unique characters**: Maintain set of characters in current window
4. **Shrink window**: Remove characters from left when duplicates found
5. **Update maximum**: Track the longest valid window

---

*This analysis shows how to efficiently find the longest substring without repeating characters using sliding window technique.* 