# CSES Minimal Rotation - Problem Analysis

## Problem Statement
Given a string, find the lexicographically smallest rotation of the string.

### Input
The first input line has a string s.

### Output
Print the lexicographically smallest rotation of the string.

### Constraints
- 1 ≤ |s| ≤ 10^6

### Example
```
Input:
baabaa

Output:
aabaab
```

## Solution Progression

### Approach 1: Generate All Rotations - O(|s|²)
**Description**: Generate all possible rotations and find the lexicographically smallest one.

```python
def minimal_rotation_naive(s):
    n = len(s)
    rotations = []
    
    # Generate all rotations
    for i in range(n):
        rotation = s[i:] + s[:i]
        rotations.append(rotation)
    
    # Find the lexicographically smallest
    return min(rotations)
```

**Why this is inefficient**: Quadratic time complexity and space complexity.

### Improvement 1: Booth's Algorithm - O(|s|)
**Description**: Use Booth's algorithm to find the lexicographically smallest rotation efficiently.

```python
def minimal_rotation_booth(s):
    n = len(s)
    s = s + s  # Double the string for easier handling
    f = [0] * (2 * n)
    
    k = 0
    for j in range(1, 2 * n):
        i = f[j - k - 1]
        while i > 0 and s[j] != s[k + i]:
            if s[j] < s[k + i]:
                k = j - i
            i = f[i - 1]
        
        if s[j] == s[k + i]:
            i += 1
        else:
            if s[j] < s[k]:
                k = j
            i = 0
        
        f[j - k] = i
    
    return s[k:k + n]
```

**Why this improvement works**: Booth's algorithm finds the minimal rotation in linear time.

### Improvement 2: Duval's Algorithm - O(|s|)
**Description**: Use Duval's algorithm for finding the minimal rotation.

```python
def minimal_rotation_duval(s):
    n = len(s)
    s = s + s
    i = 0
    j = 1
    
    while j < n:
        k = 0
        while k < n and s[i + k] == s[j + k]:
            k += 1
        
        if k == n:
            break
        
        if s[i + k] < s[j + k]:
            j += k + 1
        else:
            i = j
            j = i + 1
    
    return s[i:i + n]
```

**Why this improvement works**: Duval's algorithm is simpler and more efficient for this problem.

### Alternative: Suffix Array Approach - O(|s| log |s|)
**Description**: Use suffix array to find the minimal rotation.

```python
def build_suffix_array(s):
    n = len(s)
    s = s + s  # Double the string
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    return [i for _, i in suffixes]

def minimal_rotation_suffix_array(s):
    n = len(s)
    suffix_array = build_suffix_array(s)
    
    # Find the first suffix that starts within the first n characters
    for i in suffix_array:
        if i < n:
            return s[i:] + s[:i]
    
    return s
```

**Why this works**: Suffix array gives us all suffixes in lexicographic order.

## Final Optimal Solution

```python
s = input().strip()

def minimal_rotation_duval(s):
    n = len(s)
    s = s + s
    i = 0
    j = 1
    
    while j < n:
        k = 0
        while k < n and s[i + k] == s[j + k]:
            k += 1
        
        if k == n:
            break
        
        if s[i + k] < s[j + k]:
            j += k + 1
        else:
            i = j
            j = i + 1
    
    return s[i:i + n]

result = minimal_rotation_duval(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|²) | O(|s|²) | Generate all rotations |
| Booth's | O(|s|) | O(|s|) | Use failure function |
| Duval's | O(|s|) | O(|s|) | Simple comparison |
| Suffix Array | O(|s| log |s|) | O(|s|) | Lexicographic ordering |

## Key Insights for Other Problems

### 1. **Minimal Rotation Problems**
**Principle**: Use specialized algorithms like Booth's or Duval's for finding minimal rotations.
**Applicable to**:
- Minimal rotation problems
- String algorithms
- Lexicographic ordering
- Algorithm design

**Example Problems**:
- Minimal rotation problems
- String algorithms
- Lexicographic ordering
- Algorithm design

### 2. **String Doubling Technique**
**Principle**: Double the string to handle rotations more easily.
**Applicable to**:
- String algorithms
- Rotation problems
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Rotation problems
- Algorithm design
- Problem solving

### 3. **Lexicographic Comparison**
**Principle**: Use efficient comparison techniques for lexicographic ordering.
**Applicable to**:
- String algorithms
- Sorting
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Sorting
- Algorithm design
- Problem solving

### 4. **Failure Function Applications**
**Principle**: Use failure functions to optimize string comparisons.
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

### 1. **Duval's Algorithm Pattern**
```python
def minimal_rotation_duval(s):
    n = len(s)
    s = s + s
    i = 0
    j = 1
    
    while j < n:
        k = 0
        while k < n and s[i + k] == s[j + k]:
            k += 1
        
        if k == n:
            break
        
        if s[i + k] < s[j + k]:
            j += k + 1
        else:
            i = j
            j = i + 1
    
    return s[i:i + n]
```

### 2. **Booth's Algorithm Pattern**
```python
def minimal_rotation_booth(s):
    n = len(s)
    s = s + s
    f = [0] * (2 * n)
    
    k = 0
    for j in range(1, 2 * n):
        i = f[j - k - 1]
        while i > 0 and s[j] != s[k + i]:
            if s[j] < s[k + i]:
                k = j - i
            i = f[i - 1]
        
        if s[j] == s[k + i]:
            i += 1
        else:
            if s[j] < s[k]:
                k = j
            i = 0
        
        f[j - k] = i
    
    return s[k:k + n]
```

### 3. **Suffix Array Pattern**
```python
def minimal_rotation_suffix_array(s):
    n = len(s)
    s = s + s
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    
    for _, i in suffixes:
        if i < n:
            return s[i:i + n]
    
    return s
```

## Edge Cases to Remember

1. **Single character**: Return the character itself
2. **All same characters**: Any rotation is minimal
3. **Already minimal**: Return the original string
4. **Empty string**: Handle appropriately
5. **Repeated patterns**: Handle efficiently

## Problem-Solving Framework

1. **Identify rotation nature**: This is a minimal rotation problem
2. **Choose algorithm**: Use Duval's algorithm for efficiency
3. **Double string**: Concatenate string with itself
4. **Find minimal**: Use comparison-based approach
5. **Return result**: Return the minimal rotation

---

*This analysis shows how to efficiently find the lexicographically smallest rotation using specialized algorithms.* 