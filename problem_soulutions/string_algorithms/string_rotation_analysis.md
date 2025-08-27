# CSES String Rotation - Problem Analysis

## Problem Statement
Given a string s, find the lexicographically smallest rotation of the string.

### Input
The first input line has a string s.

### Output
Print the lexicographically smallest rotation.

### Constraints
- 1 ≤ |s| ≤ 10^5
- String contains only lowercase letters

### Example
```
Input:
abacaba

Output:
aabacab
```

## Solution Progression

### Approach 1: Generate All Rotations - O(|s|²)
**Description**: Generate all possible rotations and find the lexicographically smallest one.

```python
def string_rotation_naive(s):
    n = len(s)
    rotations = []
    
    # Generate all rotations
    for i in range(n):
        rotation = s[i:] + s[:i]
        rotations.append(rotation)
    
    # Find lexicographically smallest
    return min(rotations)
```

**Why this is inefficient**: We need to generate all rotations and compare them, leading to O(|s|²) time complexity.

### Improvement 1: Booth's Algorithm - O(|s|)
**Description**: Use Booth's algorithm to find the lexicographically smallest rotation efficiently.

```python
def string_rotation_booth(s):
    n = len(s)
    s = s + s  # Double the string for easier processing
    
    # Initialize failure function
    failure = [0] * (2 * n)
    
    # Find the lexicographically smallest rotation
    i = 0
    for j in range(1, 2 * n):
        k = failure[j - i - 1]
        while k > 0 and s[j] != s[i + k]:
            if s[j] < s[i + k]:
                i = j - k
            k = failure[k - 1]
        
        if s[j] != s[i + k]:
            if s[j] < s[i]:
                i = j
            failure[j - i] = 0
        else:
            failure[j - i] = k + 1
    
    return s[i:i + n]
```

**Why this improvement works**: Booth's algorithm finds the lexicographically smallest rotation in linear time using failure function.

## Final Optimal Solution

```python
s = input().strip()

def find_lexicographically_smallest_rotation(s):
    n = len(s)
    s = s + s  # Double the string for easier processing
    
    # Initialize failure function
    failure = [0] * (2 * n)
    
    # Find the lexicographically smallest rotation
    i = 0
    for j in range(1, 2 * n):
        k = failure[j - i - 1]
        while k > 0 and s[j] != s[i + k]:
            if s[j] < s[i + k]:
                i = j - k
            k = failure[k - 1]
        
        if s[j] != s[i + k]:
            if s[j] < s[i]:
                i = j
            failure[j - i] = 0
        else:
            failure[j - i] = k + 1
    
    return s[i:i + n]

result = find_lexicographically_smallest_rotation(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|²) | O(|s|²) | Generate all rotations |
| Booth's Algorithm | O(|s|) | O(|s|) | Use failure function for linear time |

## Key Insights for Other Problems

### 1. **String Rotation Problems**
**Principle**: Use Booth's algorithm to find lexicographically smallest rotation.
**Applicable to**: String problems, rotation problems, lexicographic ordering

### 2. **Booth's Algorithm**
**Principle**: Use failure function to find minimal rotation efficiently.
**Applicable to**: String algorithms, rotation problems, minimal string problems

### 3. **Lexicographic Ordering**
**Principle**: Compare strings character by character to find minimal ordering.
**Applicable to**: String comparison, sorting problems, minimal element problems

## Notable Techniques

### 1. **Booth's Algorithm Implementation**
```python
def booth_algorithm(s):
    n = len(s)
    s = s + s
    
    failure = [0] * (2 * n)
    i = 0
    
    for j in range(1, 2 * n):
        k = failure[j - i - 1]
        while k > 0 and s[j] != s[i + k]:
            if s[j] < s[i + k]:
                i = j - k
            k = failure[k - 1]
        
        if s[j] != s[i + k]:
            if s[j] < s[i]:
                i = j
            failure[j - i] = 0
        else:
            failure[j - i] = k + 1
    
    return s[i:i + n]
```

### 2. **Rotation Generation**
```python
def generate_rotations(s):
    n = len(s)
    rotations = []
    
    for i in range(n):
        rotation = s[i:] + s[:i]
        rotations.append(rotation)
    
    return rotations
```

### 3. **Lexicographic Comparison**
```python
def lexicographic_compare(s1, s2):
    n = min(len(s1), len(s2))
    
    for i in range(n):
        if s1[i] < s2[i]:
            return -1
        elif s1[i] > s2[i]:
            return 1
    
    if len(s1) < len(s2):
        return -1
    elif len(s1) > len(s2):
        return 1
    else:
        return 0
```

## Problem-Solving Framework

1. **Identify problem type**: This is a string rotation problem
2. **Choose approach**: Use Booth's algorithm for efficient solution
3. **Double the string**: Create s + s for easier processing
4. **Apply Booth's algorithm**: Find minimal rotation using failure function
5. **Return result**: Output the lexicographically smallest rotation

---

*This analysis shows how to efficiently find the lexicographically smallest rotation using Booth's algorithm.* 