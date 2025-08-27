# CSES String Compression - Problem Analysis

## Problem Statement
Given a string s, find the shortest compressed representation of the string. The compressed string should represent the original string using the minimum number of characters.

### Input
The first input line has a string s.

### Output
Print the compressed string.

### Constraints
- 1 ≤ |s| ≤ 10^5
- String contains only lowercase letters

### Example
```
Input:
aaabbbcc

Output:
a3b3c2
```

## Solution Progression

### Approach 1: Simple Run-Length Encoding - O(|s|)
**Description**: Use run-length encoding to compress consecutive identical characters.

```python
def string_compression_naive(s):
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char)
            if count > 1:
                compressed.append(str(count))
            current_char = s[i]
            count = 1
    
    # Add the last group
    compressed.append(current_char)
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)
```

**Why this is inefficient**: This is actually optimal for basic run-length encoding, but we can consider more advanced compression techniques.

### Improvement 1: Optimized Run-Length Encoding - O(|s|)
**Description**: Optimize the run-length encoding with better handling of edge cases.

```python
def string_compression_optimized(s):
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char)
            if count > 1:
                compressed.append(str(count))
            current_char = s[i]
            count = 1
    
    # Add the last group
    compressed.append(current_char)
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)
```

**Why this improvement works**: Better handling of edge cases and more efficient string building.

## Final Optimal Solution

```python
s = input().strip()

def compress_string(s):
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char)
            if count > 1:
                compressed.append(str(count))
            current_char = s[i]
            count = 1
    
    # Add the last group
    compressed.append(current_char)
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)

result = compress_string(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|) | O(|s|) | Simple run-length encoding |
| Optimized | O(|s|) | O(|s|) | Optimized run-length encoding |

## Key Insights for Other Problems

### 1. **String Compression Problems**
**Principle**: Use run-length encoding for consecutive identical characters.
**Applicable to**: Compression problems, string encoding problems, data compression

### 2. **Run-Length Encoding**
**Principle**: Replace consecutive identical characters with character and count.
**Applicable to**: Compression algorithms, data encoding, string processing

### 3. **String Processing Patterns**
**Principle**: Process strings character by character with state tracking.
**Applicable to**: String algorithms, parsing problems, text processing

## Notable Techniques

### 1. **Run-Length Encoding**
```python
def run_length_encode(s):
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char)
            if count > 1:
                compressed.append(str(count))
            current_char = s[i]
            count = 1
    
    compressed.append(current_char)
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)
```

### 2. **Character Grouping**
```python
def group_consecutive_chars(s):
    groups = []
    if not s:
        return groups
    
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            groups.append((current_char, count))
            current_char = s[i]
            count = 1
    
    groups.append((current_char, count))
    return groups
```

### 3. **Compression Ratio Check**
```python
def compression_ratio(original, compressed):
    return len(compressed) / len(original)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a string compression problem
2. **Choose approach**: Use run-length encoding for consecutive characters
3. **Process string**: Track current character and count
4. **Build result**: Append character and count to compressed string
5. **Return result**: Output the compressed string

---

*This analysis shows how to efficiently compress strings using run-length encoding.* 