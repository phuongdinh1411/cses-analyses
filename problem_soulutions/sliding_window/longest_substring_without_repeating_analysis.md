---
layout: simple
title: "Longest Substring Without Repeating Characters Analysis"
permalink: /problem_soulutions/sliding_window/longest_substring_without_repeating_analysis
---


# Longest Substring Without Repeating Characters Analysis

## Problem Description

**Problem**: Given a string, find the length of the longest substring without repeating characters.

**Input**: 
- s: a string

**Output**: The length of the longest substring without repeating characters.

**Example**:
```
Input:
abcabcbb

Output:
3

Explanation: 
The longest substring without repeating characters is "abc" with length 3.
Other valid substrings include "bca", "cab", etc.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the longest substring with all unique characters
- Use sliding window technique for efficiency
- Track character uniqueness dynamically
- Handle edge cases properly

**Key Observations:**
- Need to track unique characters in current window
- Window can expand and contract
- Must maintain character uniqueness
- Window size should be maximized

### Step 2: Brute Force Approach
**Idea**: Check all possible substrings to find the longest one without repeating characters.

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

**Why this is inefficient:**
- Time complexity: O(n³)
- Lots of redundant calculations
- Not scalable for large inputs
- Inefficient uniqueness checking

### Step 3: Optimization with Sliding Window
**Idea**: Use sliding window technique with hash set to track unique characters.

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

**Why this improvement works:**
- Time complexity: O(n)
- Efficiently maintains window with unique characters
- Single pass through the string
- Optimal algorithm for this problem

### Step 4: Alternative Approach with Hash Map
**Idea**: Use sliding window with hash map to track character frequencies.

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

**Why this works:**
- Hash map provides more detailed character tracking
- Useful for variations with character constraints
- Same time complexity: O(n)
- Good alternative approach

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_longest_substring_without_repeating():
    s = input().strip()
    
    result = find_longest_substring_without_repeating(s)
    print(result)

def find_longest_substring_without_repeating(s):
    """Find length of longest substring without repeating characters"""
    if not s:
        return 0
    
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

# Main execution
if __name__ == "__main__":
    solve_longest_substring_without_repeating()
```

**Why this works:**
- Optimal sliding window algorithm approach
- Handles all edge cases correctly
- Efficient character tracking
- Clear and readable code
        max_length = max(max_length, right - left + 1)
    
    return max_length

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        ("a", 1),
        ("abc", 3),
    ]
    
    for s, expected in test_cases:
        result = find_longest_substring_without_repeating(s)
        print(f"s: '{s}'")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_longest_substring_without_repeating(s):
    if not s:
        return 0
    
    n = len(s)
    left = 0
    max_length = 0
    char_set = set()
    
    for right in range(n):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the string with sliding window
- **Space**: O(min(m, n)) - where m is the size of the character set

### Why This Solution Works
- **Sliding Window**: Efficiently finds longest unique substring
- **Character Tracking**: Maintains uniqueness with hash set
- **Optimal Algorithm**: Best known approach for this problem
- **Edge Case Handling**: Properly handles empty strings and single characters

## 🎯 Key Insights

### 1. **Sliding Window Technique**
- Use two pointers to maintain a valid window
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Character Uniqueness Tracking**
- Track unique characters in current window
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Window Contraction**
- Shrink window when duplicates are found
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Longest Substring with At Most K Repeating Characters
**Problem**: Find longest substring with at most k repeating characters.

```python
def longest_substring_with_k_repeating(s, k):
    if not s:
        return 0
    
    n = len(s)
    left = 0
    max_length = 0
    char_count = {}
    
    for right in range(n):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink window if we have more than k repeating characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage
result = longest_substring_with_k_repeating("eceba", 2)
print(f"Longest substring with at most 2 repeating: {result}")
```

### Variation 2: Longest Substring with Character Order Constraint
**Problem**: Find longest substring where characters appear in alphabetical order.

```python
def longest_substring_alphabetical_order(s):
    if not s:
        return 0
    
    n = len(s)
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if s[i] >= s[i-1]:
            current_length += 1
        else:
            current_length = 1
        max_length = max(max_length, current_length)
    
    return max_length

# Example usage
result = longest_substring_alphabetical_order("abcabcbb")
print(f"Longest alphabetical substring: {result}")
```

### Variation 3: Longest Substring with Character Frequency Constraint
**Problem**: Find longest substring where each character appears exactly k times.

```python
def longest_substring_exact_k_frequency(s, k):
    if not s or k <= 0:
        return 0
    
    n = len(s)
    max_length = 0
    
    for i in range(n):
        char_count = {}
        for j in range(i, n):
            char_count[s[j]] = char_count.get(s[j], 0) + 1
            
            # Check if all characters have exactly k frequency
            valid = True
            for count in char_count.values():
                if count != k:
                    valid = False
                    break
            
            if valid:
                max_length = max(max_length, j - i + 1)
    
    return max_length

# Example usage
result = longest_substring_exact_k_frequency("aabbcc", 2)
print(f"Longest substring with exact 2 frequency: {result}")
```

### Variation 4: Longest Substring with Range Queries
**Problem**: Answer queries about longest substring without repeating characters in specific ranges.

```python
def longest_substring_range_queries(s, queries):
    """Answer longest substring queries for specific ranges"""
    results = []
    
    for start, end in queries:
        if start > end or start < 0 or end >= len(s):
            results.append(0)
        else:
            # Extract substring for this range
            substring = s[start:end + 1]
            max_length = find_longest_substring_without_repeating_in_range(substring)
            results.append(max_length)
    
    return results

def find_longest_substring_without_repeating_in_range(s):
    """Find longest substring without repeating characters in a specific range"""
    if not s:
        return 0
    
    n = len(s)
    left = 0
    max_length = 0
    char_set = set()
    
    for right in range(n):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example usage
queries = [(0, 4), (1, 6), (2, 7)]
result = longest_substring_range_queries("abcabcbb", queries)
print(f"Range query results: {result}")
```

### Variation 5: Longest Substring with Character Weights
**Problem**: Each character has a weight, find longest substring with maximum total weight.

```python
def longest_substring_with_max_weight(s, weights):
    if not s:
        return 0
    
    n = len(s)
    left = 0
    max_length = 0
    max_weight = 0
    char_set = set()
    current_weight = 0
    
    for right in range(n):
        while s[right] in char_set:
            char_set.remove(s[left])
            current_weight -= weights.get(s[left], 0)
            left += 1
        
        char_set.add(s[right])
        current_weight += weights.get(s[right], 0)
        
        if right - left + 1 > max_length or \
           (right - left + 1 == max_length and current_weight > max_weight):
            max_length = right - left + 1
            max_weight = current_weight
    
    return max_length, max_weight

# Example usage
weights = {'a': 3, 'b': 2, 'c': 1}
result, weight = longest_substring_with_max_weight("abcabcbb", weights)
print(f"Longest substring with max weight: {result}, Weight: {weight}")
```

## 🔗 Related Problems

- **[Minimum Window Substring](/cses-analyses/problem_soulutions/sliding_window/)**: Substring optimization problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray problems
- **[Sliding Window Advertisement](/cses-analyses/problem_soulutions/sliding_window/)**: Other sliding window problems

## 📚 Learning Points

1. **Sliding Window Technique**: Essential for substring optimization
2. **Character Uniqueness Tracking**: Important for string problems
3. **Window Contraction**: Key for optimization
4. **Hash Set/Map Usage**: Important for efficient character tracking

---

**This is a great introduction to longest substring without repeating problems!** 🎯
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