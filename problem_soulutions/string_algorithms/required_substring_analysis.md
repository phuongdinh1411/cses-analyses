# CSES Required Substring - Problem Analysis

## Problem Statement
Given a string and a required substring, find the minimum number of characters to add to make the string contain the required substring.

### Input
The first input line has a string s.
The second input line has a required substring t.

### Output
Print the minimum number of characters to add.

### Constraints
- 1 ≤ |s|, |t| ≤ 10^5

### Example
```
Input:
abab
ab

Output:
0
```

## Solution Progression

### Approach 1: Check All Positions - O(|s| × |t|)
**Description**: Check if the required substring already exists in the string.

```python
def required_substring_naive(s, t):
    def is_substring(s, t):
        n, m = len(s), len(t)
        for i in range(n - m + 1):
            if s[i:i + m] == t:
                return True
        return False
    
    if is_substring(s, t):
        return 0
    
    # Try adding characters at the end
    min_chars = len(t)
    for i in range(1, len(t)):
        if is_substring(s + t[:i], t):
            min_chars = min(min_chars, i)
    
    return min_chars
```

**Why this is inefficient**: Quadratic time complexity and doesn't consider all possible positions.

### Improvement 1: Use KMP Algorithm - O(|s| + |t|)
**Description**: Use KMP algorithm to find the longest suffix of s that is a prefix of t.

```python
def required_substring_kmp(s, t):
    def compute_lps(pattern):
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
    
    def kmp_search(text, pattern):
        n, m = len(text), len(pattern)
        if m == 0:
            return True
        
        lps = compute_lps(pattern)
        i = j = 0
        
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                return True
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return False
    
    # Check if substring already exists
    if kmp_search(s, t):
        return 0
    
    # Find the longest suffix of s that is a prefix of t
    max_overlap = 0
    for i in range(1, min(len(s), len(t)) + 1):
        if s[-i:] == t[:i]:
            max_overlap = i
    
    return len(t) - max_overlap
```

**Why this improvement works**: KMP algorithm efficiently finds pattern matches and helps determine the minimum characters needed.

### Improvement 2: Use Z-Algorithm - O(|s| + |t|)
**Description**: Use Z-algorithm to find the longest suffix of s that is a prefix of t.

```python
def required_substring_z(s, t):
    def compute_z_array(text):
        n = len(text)
        z = [0] * n
        l = r = 0
        
        for i in range(1, n):
            if i > r:
                l = r = i
                while r < n and text[r - l] == text[r]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and text[r - l] == text[r]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        return z
    
    # Check if substring already exists
    if t in s:
        return 0
    
    # Concatenate t + separator + s to find overlap
    text = t + '$' + s
    z = compute_z_array(text)
    
    # Find the longest suffix of s that is a prefix of t
    max_overlap = 0
    for i in range(len(t) + 1, len(z)):
        if z[i] == len(t):
            return 0  # Substring already exists
        max_overlap = max(max_overlap, z[i])
    
    return len(t) - max_overlap
```

**Why this improvement works**: Z-algorithm efficiently finds the longest common prefix between strings.

### Alternative: Use Rolling Hash - O(|s| + |t|)
**Description**: Use rolling hash to find the longest suffix of s that is a prefix of t.

```python
def required_substring_rolling_hash(s, t):
    def compute_hash(s, base=31, mod=10**9 + 7):
        n = len(s)
        hash_values = [0] * (n + 1)
        power = [1] * (n + 1)
        
        for i in range(n):
            hash_values[i + 1] = (hash_values[i] * base + ord(s[i])) % mod
            power[i + 1] = (power[i] * base) % mod
        
        return hash_values, power
    
    def get_hash(hash_values, power, mod, left, right):
        return (hash_values[right] - hash_values[left] * power[right - left]) % mod
    
    # Check if substring already exists
    if t in s:
        return 0
    
    n, m = len(s), len(t)
    s_hash, s_power = compute_hash(s)
    t_hash, t_power = compute_hash(t)
    mod = 10**9 + 7
    
    # Find the longest suffix of s that is a prefix of t
    max_overlap = 0
    for i in range(1, min(n, m) + 1):
        s_suffix_hash = get_hash(s_hash, s_power, mod, n - i, n)
        t_prefix_hash = get_hash(t_hash, t_power, mod, 0, i)
        
        if s_suffix_hash == t_prefix_hash:
            max_overlap = i
    
    return m - max_overlap
```

**Why this works**: Rolling hash efficiently compares substrings for equality.

## Final Optimal Solution

```python
s = input().strip()
t = input().strip()

def required_substring_kmp(s, t):
    def compute_lps(pattern):
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
    
    def kmp_search(text, pattern):
        n, m = len(text), len(pattern)
        if m == 0:
            return True
        
        lps = compute_lps(pattern)
        i = j = 0
        
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                return True
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return False
    
    # Check if substring already exists
    if kmp_search(s, t):
        return 0
    
    # Find the longest suffix of s that is a prefix of t
    max_overlap = 0
    for i in range(1, min(len(s), len(t)) + 1):
        if s[-i:] == t[:i]:
            max_overlap = i
    
    return len(t) - max_overlap

result = required_substring_kmp(s, t)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s| × |t|) | O(1) | Check all positions |
| KMP | O(|s| + |t|) | O(|t|) | Use KMP algorithm |
| Z-Algorithm | O(|s| + |t|) | O(|s| + |t|) | Use Z-algorithm |
| Rolling Hash | O(|s| + |t|) | O(|s| + |t|) | Use rolling hash |

## Key Insights for Other Problems

### 1. **String Extension Problems**
**Principle**: Use pattern matching algorithms to find optimal extension points.
**Applicable to**:
- String extension problems
- Pattern matching
- String algorithms
- Algorithm design

**Example Problems**:
- String extension problems
- Pattern matching
- String algorithms
- Algorithm design

### 2. **Overlap Detection**
**Principle**: Find the longest suffix of one string that is a prefix of another.
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

### 3. **KMP for Overlap**
**Principle**: Use KMP algorithm to efficiently find pattern matches and overlaps.
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

### 4. **Z-Algorithm Applications**
**Principle**: Use Z-algorithm for efficient string comparison and overlap detection.
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

## Notable Techniques

### 1. **KMP Overlap Detection Pattern**
```python
def find_overlap_kmp(s, t):
    def compute_lps(pattern):
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
    
    def kmp_search(text, pattern):
        n, m = len(text), len(pattern)
        if m == 0:
            return True
        
        lps = compute_lps(pattern)
        i = j = 0
        
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                return True
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return False
    
    # Check if substring already exists
    if kmp_search(s, t):
        return 0
    
    # Find the longest suffix of s that is a prefix of t
    max_overlap = 0
    for i in range(1, min(len(s), len(t)) + 1):
        if s[-i:] == t[:i]:
            max_overlap = i
    
    return len(t) - max_overlap
```

### 2. **Z-Algorithm Overlap Pattern**
```python
def find_overlap_z(s, t):
    def compute_z_array(text):
        n = len(text)
        z = [0] * n
        l = r = 0
        
        for i in range(1, n):
            if i > r:
                l = r = i
                while r < n and text[r - l] == text[r]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and text[r - l] == text[r]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        return z
    
    # Check if substring already exists
    if t in s:
        return 0
    
    # Concatenate t + separator + s to find overlap
    text = t + '$' + s
    z = compute_z_array(text)
    
    # Find the longest suffix of s that is a prefix of t
    max_overlap = 0
    for i in range(len(t) + 1, len(z)):
        if z[i] == len(t):
            return 0  # Substring already exists
        max_overlap = max(max_overlap, z[i])
    
    return len(t) - max_overlap
```

### 3. **Rolling Hash Overlap Pattern**
```python
def find_overlap_rolling_hash(s, t):
    def compute_hash(s, base=31, mod=10**9 + 7):
        n = len(s)
        hash_values = [0] * (n + 1)
        power = [1] * (n + 1)
        
        for i in range(n):
            hash_values[i + 1] = (hash_values[i] * base + ord(s[i])) % mod
            power[i + 1] = (power[i] * base) % mod
        
        return hash_values, power
    
    def get_hash(hash_values, power, mod, left, right):
        return (hash_values[right] - hash_values[left] * power[right - left]) % mod
    
    # Check if substring already exists
    if t in s:
        return 0
    
    n, m = len(s), len(t)
    s_hash, s_power = compute_hash(s)
    t_hash, t_power = compute_hash(t)
    mod = 10**9 + 7
    
    # Find the longest suffix of s that is a prefix of t
    max_overlap = 0
    for i in range(1, min(n, m) + 1):
        s_suffix_hash = get_hash(s_hash, s_power, mod, n - i, n)
        t_prefix_hash = get_hash(t_hash, t_power, mod, 0, i)
        
        if s_suffix_hash == t_prefix_hash:
            max_overlap = i
    
    return m - max_overlap
```

## Edge Cases to Remember

1. **Substring already exists**: Return 0
2. **Empty required substring**: Return 0
3. **Empty string**: Return length of required substring
4. **No overlap**: Return length of required substring
5. **Perfect overlap**: Return 0
6. **Partial overlap**: Return remaining characters needed

## Problem-Solving Framework

1. **Check existence**: First check if the required substring already exists
2. **Find overlap**: Find the longest suffix of s that is a prefix of t
3. **Calculate minimum**: The minimum characters needed is |t| - overlap_length
4. **Return result**: Return the calculated minimum

---

*This analysis shows how to efficiently find the minimum characters needed to make a string contain a required substring using KMP algorithm and other string matching techniques.* 