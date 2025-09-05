---
layout: simple
title: "Minimum Window Substring Analysis"
permalink: /problem_soulutions/sliding_window/minimum_window_substring_analysis
---


# Minimum Window Substring Analysis

## Problem Description

**Problem**: Given a string S and a string T, find the minimum window in S which will contain all the characters in T.

**Input**: 
- S: the source string
- T: the target string

**Output**: The minimum window substring of S that contains all characters from T.

**Example**:
```
Input:
S = "ADOBECODEBANC"
T = "ABC"

Output:
"BANC"

Explanation: 
The minimum window "BANC" contains all characters from T:
- 'A' appears in "BANC"
- 'B' appears in "BANC" 
- 'C' appears in "BANC"
This is the smallest substring that contains all required characters.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the smallest substring containing all target characters
- Handle character frequency requirements
- Use sliding window technique efficiently
- Track character counts dynamically

**Key Observations:**
- Need to track character frequencies
- Window can expand and contract
- Must contain ALL characters from T
- Window size should be minimized

### Step 2: Sliding Window Approach
**Idea**: Use two pointers (left and right) to maintain a window that contains all characters from T, then minimize the window size.

```python
def minimum_window_substring_sliding_window(s, t):
    if not s or not t:
        return ""
    
    # Count characters in target string T
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    # Track current window character counts
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        # Add current character to window
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        # Check if this character completes a required character
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        # Try to minimize window from left
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            # Update minimum window if current is smaller
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            # Remove leftmost character
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window
```

**Why this works:**
- Sliding window efficiently finds minimum valid substring
- Character counting ensures all required characters are present
- Window contraction minimizes substring length
- O(n) time complexity is optimal

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_minimum_window_substring():
    s = input().strip()
    t = input().strip()
    
    result = find_minimum_window(s, t)
    print(result)

def find_minimum_window(s, t):
    """Find minimum window substring containing all characters from T"""
    if not s or not t:
        return ""
    
    # Count characters in target string T
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    # Track current window character counts
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        # Add current character to window
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        # Check if this character completes a required character
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        # Try to minimize window from left
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            # Update minimum window if current is smaller
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            # Remove leftmost character
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window

# Main execution
if __name__ == "__main__":
    solve_minimum_window_substring()
```

**Why this works:**
- Optimal sliding window algorithm approach
- Handles all edge cases correctly
- Efficient character counting
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ("ADOBECODEBANC", "ABC", "BANC"),
        ("a", "a", "a"),
        ("a", "aa", ""),
        ("aa", "aa", "aa"),
        ("cabwefgewcwaefgcf", "cae", "cwae"),
    ]
    
    for s, t, expected in test_cases:
        result = solve_test(s, t)
        print(f"S: '{s}', T: '{t}'")
        print(f"Expected: '{expected}', Got: '{result}'")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(s, t):
    return find_minimum_window(s, t)

def find_minimum_window(s, t):
    if not s or not t:
        return ""
    
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the string with sliding window
- **Space**: O(k) - where k is the number of unique characters in T

### Why This Solution Works
- **Sliding Window**: Efficiently finds minimum valid substring
- **Character Counting**: Ensures all required characters are present
- **Window Optimization**: Contracts window to minimize length
- **Optimal Algorithm**: Best known approach for this problem

## 🎯 Key Insights

### 1. **Sliding Window Technique**
- Use two pointers to maintain a valid window
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Character Frequency Tracking**
- Count characters in target and current window
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Window Contraction**
- Minimize window size while maintaining validity
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Minimum Window with Character Order
**Problem**: Find minimum window where characters appear in the same order as in T.

```python
def minimum_window_with_order(s, t):
    if not s or not t:
        return ""
    
    # Find minimum window maintaining character order
    min_window = ""
    min_length = float('inf')
    
    for i in range(len(s)):
        if s[i] == t[0]:  # Start of potential window
            window_start = i
            t_index = 0
            
            for j in range(i, len(s)):
                if s[j] == t[t_index]:
                    t_index += 1
                    if t_index == len(t):  # Found complete window
                        window_length = j - window_start + 1
                        if window_length < min_length:
                            min_length = window_length
                            min_window = s[window_start:j + 1]
                        break
    
    return min_window

# Example usage
result = minimum_window_with_order("ADOBECODEBANC", "ABC")
print(f"Ordered minimum window: {result}")
```

### Variation 2: Minimum Window with K Missing Characters
**Problem**: Find minimum window that contains all characters from T except at most K missing characters.

```python
def minimum_window_with_k_missing(s, t, k):
    if not s or not t:
        return ""
    
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    missing_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        if char in target_count:
            if current_count[char] == target_count[char]:
                formed_chars += 1
            elif current_count[char] < target_count[char]:
                missing_chars += 1
        
        # Allow K missing characters
        while left <= right and (formed_chars == required_chars or missing_chars <= k):
            char = s[left]
            
            if formed_chars == required_chars and right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            current_count[char] -= 1
            if char in target_count:
                if current_count[char] < target_count[char]:
                    missing_chars -= 1
                elif current_count[char] == target_count[char] - 1:
                    formed_chars -= 1
            
            left += 1
    
    return min_window

# Example usage
result = minimum_window_with_k_missing("ADOBECODEBANC", "ABC", 1)
print(f"Minimum window with 1 missing: {result}")
```

### Variation 3: Minimum Window with Character Weights
**Problem**: Each character has a weight, find minimum window with maximum total weight.

```python
def minimum_window_with_weights(s, t, weights):
    if not s or not t:
        return ""
    
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    max_weight = 0
    
    for right in range(len(s)):
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            # Calculate current window weight
            current_weight = sum(weights.get(c, 0) for c in s[left:right + 1])
            
            if right - left + 1 < min_length or \
               (right - left + 1 == min_length and current_weight > max_weight):
                min_length = right - left + 1
                min_window = s[left:right + 1]
                max_weight = current_weight
            
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window, max_weight

# Example usage
weights = {'A': 3, 'B': 2, 'C': 1}
result, weight = minimum_window_with_weights("ADOBECODEBANC", "ABC", weights)
print(f"Weighted minimum window: {result}, Weight: {weight}")
```

### Variation 4: Minimum Window with Dynamic Target
**Problem**: Target string T can change dynamically, maintain minimum window.

```python
class DynamicMinimumWindow:
    def __init__(self, s):
        self.s = s
        self.target_count = {}
        self.current_count = {}
        self.formed_chars = 0
        self.required_chars = 0
    
    def set_target(self, t):
        """Update target string and recalculate"""
        self.target_count = {}
        for char in t:
            self.target_count[char] = self.target_count.get(char, 0) + 1
        self.required_chars = len(self.target_count)
        self.formed_chars = 0
        self.current_count = {}
    
    def find_minimum_window(self):
        """Find minimum window for current target"""
        if not self.target_count:
            return ""
        
        left = 0
        min_window = ""
        min_length = float('inf')
        
        for right in range(len(self.s)):
            char = self.s[right]
            self.current_count[char] = self.current_count.get(char, 0) + 1
            
            if char in self.target_count and self.current_count[char] == self.target_count[char]:
                self.formed_chars += 1
            
            while left <= right and self.formed_chars == self.required_chars:
                char = self.s[left]
                
                if right - left + 1 < min_length:
                    min_length = right - left + 1
                    min_window = self.s[left:right + 1]
                
                self.current_count[char] -= 1
                if char in self.target_count and self.current_count[char] < self.target_count[char]:
                    self.formed_chars -= 1
                
                left += 1
        
        return min_window

# Example usage
dynamic_window = DynamicMinimumWindow("ADOBECODEBANC")
dynamic_window.set_target("ABC")
result1 = dynamic_window.find_minimum_window()
print(f"Window for 'ABC': {result1}")

dynamic_window.set_target("AB")
result2 = dynamic_window.find_minimum_window()
print(f"Window for 'AB': {result2}")
```

### Variation 5: Minimum Window with Range Queries
**Problem**: Answer queries about minimum window in specific ranges of the string.

```python
def minimum_window_range_queries(s, t, queries):
    """Answer minimum window queries for specific ranges"""
    results = []
    
    for start, end in queries:
        # Extract substring for this range
        substring = s[start:end + 1]
        
        # Find minimum window in substring
        window = find_minimum_window_in_range(substring, t)
        results.append(window)
    
    return results

def find_minimum_window_in_range(s, t):
    """Find minimum window in a specific range"""
    if not s or not t:
        return ""
    
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window

# Example usage
queries = [(0, 5), (2, 8), (5, 12)]
result = minimum_window_range_queries("ADOBECODEBANC", "ABC", queries)
print(f"Range query results: {result}")
```

## 🔗 Related Problems

- **[Longest Substring Without Repeating](/cses-analyses/problem_soulutions/sliding_window/)**: Substring optimization problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray problems
- **[Sliding Window Advertisement](/cses-analyses/problem_soulutions/sliding_window/)**: Other sliding window problems

## 📚 Learning Points

1. **Sliding Window Technique**: Essential for substring optimization
2. **Character Frequency Tracking**: Important for string problems
3. **Window Contraction**: Key for optimization
4. **Dynamic Programming**: Important for complex variations

---

**This is a great introduction to minimum window substring algorithms!** 🎯

**Problem**: Given a string S and a string T, find the minimum window in S which will contain all the characters in T.

**Input**: 
- S: the source string
- T: the target string

**Output**: The minimum window substring of S that contains all characters from T.

**Example**:
```
Input:
S = "ADOBECODEBANC"
T = "ABC"

Output:
"BANC"

Explanation: 
The minimum window "BANC" contains all characters from T:
- 'A' appears in "BANC"
- 'B' appears in "BANC" 
- 'C' appears in "BANC"
This is the smallest substring that contains all required characters.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the smallest substring containing all target characters
- Handle character frequency requirements
- Use sliding window technique efficiently
- Track character counts dynamically

**Key Observations:**
- Need to track character frequencies
- Window can expand and contract
- Must contain ALL characters from T
- Window size should be minimized

### Step 2: Sliding Window Approach
**Idea**: Use two pointers (left and right) to maintain a window that contains all characters from T, then minimize the window size.

```python
def minimum_window_substring_sliding_window(s, t):
    if not s or not t:
        return ""
    
    # Count characters in target string T
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    # Track current window character counts
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        # Add current character to window
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        # Check if this character completes a required character
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        # Try to minimize window from left
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            # Update minimum window if current is smaller
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            # Remove leftmost character
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window
```

**Why this works:**
- Sliding window efficiently finds minimum valid substring
- Character counting ensures all required characters are present
- Window contraction minimizes substring length
- O(n) time complexity is optimal

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_minimum_window_substring():
    s = input().strip()
    t = input().strip()
    
    result = find_minimum_window(s, t)
    print(result)

def find_minimum_window(s, t):
    """Find minimum window substring containing all characters from T"""
    if not s or not t:
        return ""
    
    # Count characters in target string T
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    # Track current window character counts
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        # Add current character to window
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        # Check if this character completes a required character
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        # Try to minimize window from left
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            # Update minimum window if current is smaller
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            # Remove leftmost character
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window

# Main execution
if __name__ == "__main__":
    solve_minimum_window_substring()
```

**Why this works:**
- Optimal sliding window algorithm approach
- Handles all edge cases correctly
- Efficient character counting
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ("ADOBECODEBANC", "ABC", "BANC"),
        ("a", "a", "a"),
        ("a", "aa", ""),
        ("aa", "aa", "aa"),
        ("cabwefgewcwaefgcf", "cae", "cwae"),
    ]
    
    for s, t, expected in test_cases:
        result = solve_test(s, t)
        print(f"S: '{s}', T: '{t}'")
        print(f"Expected: '{expected}', Got: '{result}'")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(s, t):
    return find_minimum_window(s, t)

def find_minimum_window(s, t):
    if not s or not t:
        return ""
    
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through the string with sliding window
- **Space**: O(k) - where k is the number of unique characters in T

### Why This Solution Works
- **Sliding Window**: Efficiently finds minimum valid substring
- **Character Counting**: Ensures all required characters are present
- **Window Optimization**: Contracts window to minimize length
- **Optimal Algorithm**: Best known approach for this problem

## 🎯 Key Insights

### 1. **Sliding Window Technique**
- Use two pointers to maintain a valid window
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Character Frequency Tracking**
- Count characters in target and current window
- Important for understanding
- Simple but important concept
- Essential for algorithm

### 3. **Window Contraction**
- Minimize window size while maintaining validity
- Important for understanding
- Fundamental concept
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Minimum Window with Character Order
**Problem**: Find minimum window where characters appear in the same order as in T.

```python
def minimum_window_with_order(s, t):
    if not s or not t:
        return ""
    
    # Find minimum window maintaining character order
    min_window = ""
    min_length = float('inf')
    
    for i in range(len(s)):
        if s[i] == t[0]:  # Start of potential window
            window_start = i
            t_index = 0
            
            for j in range(i, len(s)):
                if s[j] == t[t_index]:
                    t_index += 1
                    if t_index == len(t):  # Found complete window
                        window_length = j - window_start + 1
                        if window_length < min_length:
                            min_length = window_length
                            min_window = s[window_start:j + 1]
                        break
    
    return min_window

# Example usage
result = minimum_window_with_order("ADOBECODEBANC", "ABC")
print(f"Ordered minimum window: {result}")
```

### Variation 2: Minimum Window with K Missing Characters
**Problem**: Find minimum window that contains all characters from T except at most K missing characters.

```python
def minimum_window_with_k_missing(s, t, k):
    if not s or not t:
        return ""
    
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    missing_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        if char in target_count:
            if current_count[char] == target_count[char]:
                formed_chars += 1
            elif current_count[char] < target_count[char]:
                missing_chars += 1
        
        # Allow K missing characters
        while left <= right and (formed_chars == required_chars or missing_chars <= k):
            char = s[left]
            
            if formed_chars == required_chars and right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            current_count[char] -= 1
            if char in target_count:
                if current_count[char] < target_count[char]:
                    missing_chars -= 1
                elif current_count[char] == target_count[char] - 1:
                    formed_chars -= 1
            
            left += 1
    
    return min_window

# Example usage
result = minimum_window_with_k_missing("ADOBECODEBANC", "ABC", 1)
print(f"Minimum window with 1 missing: {result}")
```

### Variation 3: Minimum Window with Character Weights
**Problem**: Each character has a weight, find minimum window with maximum total weight.

```python
def minimum_window_with_weights(s, t, weights):
    if not s or not t:
        return ""
    
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    max_weight = 0
    
    for right in range(len(s)):
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            # Calculate current window weight
            current_weight = sum(weights.get(c, 0) for c in s[left:right + 1])
            
            if right - left + 1 < min_length or \
               (right - left + 1 == min_length and current_weight > max_weight):
                min_length = right - left + 1
                min_window = s[left:right + 1]
                max_weight = current_weight
            
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window, max_weight

# Example usage
weights = {'A': 3, 'B': 2, 'C': 1}
result, weight = minimum_window_with_weights("ADOBECODEBANC", "ABC", weights)
print(f"Weighted minimum window: {result}, Weight: {weight}")
```

### Variation 4: Minimum Window with Dynamic Target
**Problem**: Target string T can change dynamically, maintain minimum window.

```python
class DynamicMinimumWindow:
    def __init__(self, s):
        self.s = s
        self.target_count = {}
        self.current_count = {}
        self.formed_chars = 0
        self.required_chars = 0
    
    def set_target(self, t):
        """Update target string and recalculate"""
        self.target_count = {}
        for char in t:
            self.target_count[char] = self.target_count.get(char, 0) + 1
        self.required_chars = len(self.target_count)
        self.formed_chars = 0
        self.current_count = {}
    
    def find_minimum_window(self):
        """Find minimum window for current target"""
        if not self.target_count:
            return ""
        
        left = 0
        min_window = ""
        min_length = float('inf')
        
        for right in range(len(self.s)):
            char = self.s[right]
            self.current_count[char] = self.current_count.get(char, 0) + 1
            
            if char in self.target_count and self.current_count[char] == self.target_count[char]:
                self.formed_chars += 1
            
            while left <= right and self.formed_chars == self.required_chars:
                char = self.s[left]
                
                if right - left + 1 < min_length:
                    min_length = right - left + 1
                    min_window = self.s[left:right + 1]
                
                self.current_count[char] -= 1
                if char in self.target_count and self.current_count[char] < self.target_count[char]:
                    self.formed_chars -= 1
                
                left += 1
        
        return min_window

# Example usage
dynamic_window = DynamicMinimumWindow("ADOBECODEBANC")
dynamic_window.set_target("ABC")
result1 = dynamic_window.find_minimum_window()
print(f"Window for 'ABC': {result1}")

dynamic_window.set_target("AB")
result2 = dynamic_window.find_minimum_window()
print(f"Window for 'AB': {result2}")
```

### Variation 5: Minimum Window with Range Queries
**Problem**: Answer queries about minimum window in specific ranges of the string.

```python
def minimum_window_range_queries(s, t, queries):
    """Answer minimum window queries for specific ranges"""
    results = []
    
    for start, end in queries:
        # Extract substring for this range
        substring = s[start:end + 1]
        
        # Find minimum window in substring
        window = find_minimum_window_in_range(substring, t)
        results.append(window)
    
    return results

def find_minimum_window_in_range(s, t):
    """Find minimum window in a specific range"""
    if not s or not t:
        return ""
    
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    current_count = {}
    required_chars = len(target_count)
    formed_chars = 0
    
    left = 0
    min_window = ""
    min_length = float('inf')
    
    for right in range(len(s)):
        char = s[right]
        current_count[char] = current_count.get(char, 0) + 1
        
        if char in target_count and current_count[char] == target_count[char]:
            formed_chars += 1
        
        while left <= right and formed_chars == required_chars:
            char = s[left]
            
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            
            current_count[char] -= 1
            if char in target_count and current_count[char] < target_count[char]:
                formed_chars -= 1
            
            left += 1
    
    return min_window

# Example usage
queries = [(0, 5), (2, 8), (5, 12)]
result = minimum_window_range_queries("ADOBECODEBANC", "ABC", queries)
print(f"Range query results: {result}")
```

## 🔗 Related Problems

- **[Longest Substring Without Repeating](/cses-analyses/problem_soulutions/sliding_window/)**: Substring optimization problems
- **[Subarray with Given Sum](/cses-analyses/problem_soulutions/sliding_window/)**: Subarray problems
- **[Sliding Window Advertisement](/cses-analyses/problem_soulutions/sliding_window/)**: Other sliding window problems

## 📚 Learning Points

1. **Sliding Window Technique**: Essential for substring optimization
2. **Character Frequency Tracking**: Important for string problems
3. **Window Contraction**: Key for optimization
4. **Dynamic Programming**: Important for complex variations

---

**This is a great introduction to minimum window substring algorithms!** 🎯 

## 🎨 Visual Example

### Input Example
```
Input: S="ADOBECODEBANC", T="ABC"
Output: "BANC" (minimum window containing all characters from T)
```

### Character Frequency Analysis
```
Target T="ABC":
- A: 1 occurrence
- B: 1 occurrence  
- C: 1 occurrence

Source S="ADOBECODEBANC":
A D O B E C O D E B A N C
0 1 2 3 4 5 6 7 8 9 10 11 12
```

### Sliding Window Process
```
left=0, right=0: "A"           → missing B,C
left=0, right=1: "AD"          → missing B,C
left=0, right=2: "ADO"         → missing B,C
left=0, right=3: "ADOB"        → missing A,C
left=0, right=4: "ADOBE"       → missing A,C
left=0, right=5: "ADOBEC"      → missing A → valid window!
  Try shrinking: left=1 → "DOBEC" → missing A → invalid
  Keep window: "ADOBEC" (length 6)

left=1, right=6: "DOBECO"      → missing A,C
left=1, right=7: "DOBECOD"     → missing A,C
left=1, right=8: "DOBECODE"    → missing A,C
left=1, right=9: "DOBECODEB"   → missing A,C
left=1, right=10: "DOBECODEBA" → missing C
left=1, right=11: "DOBECODEBAN" → missing C
left=1, right=12: "DOBECODEBANC" → valid window!
  Try shrinking: left=2 → "OBECODEBANC" → valid
  Try shrinking: left=3 → "BECODEBANC" → valid
  Try shrinking: left=4 → "ECODEBANC" → missing B → invalid
  Keep window: "BECODEBANC" (length 9)

Continue until find minimum...
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Sliding Window  │ O(|S|+|T|)   │ O(|S|+|T|)   │ Two pointers │
│                 │              │              │ + frequency  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(|S|³)      │ O(1)         │ Check all    │
│                 │              │              │ substrings   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Hash Map        │ O(|S|²)      │ O(|T|)       │ Frequency    │
│                 │              │              │ tracking     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```
