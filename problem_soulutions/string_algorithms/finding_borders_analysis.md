# CSES Finding Borders - Problem Analysis

## Problem Statement
Given a string, find all borders of the string. A border is a proper prefix that is also a proper suffix.

### Input
The first input line has a string s.

### Output
Print all borders of the string in ascending order of length.

### Constraints
- 1 ≤ |s| ≤ 10^6

### Example
```
Input:
ababab

Output:
ab
abab
```

## Solution Progression

### Approach 1: Naive Border Finding - O(|s|²)
**Description**: Check each possible prefix to see if it's also a suffix.

```python
def finding_borders_naive(s):
    borders = []
    n = len(s)
    
    for length in range(1, n):
        prefix = s[:length]
        suffix = s[n - length:]
        if prefix == suffix:
            borders.append(prefix)
    
    return borders
```

**Why this is inefficient**: Quadratic time complexity for large strings.

### Improvement 1: KMP Failure Function - O(|s|)
**Description**: Use KMP failure function to find all borders efficiently.

```python
def compute_lps(s):
    n = len(s)
    lps = [0] * n
    length = 0
    i = 1
    
    while i < n:
        if s[i] == s[length]:
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

def finding_borders_kmp(s):
    borders = []
    n = len(s)
    lps = compute_lps(s)
    
    # Find all borders using LPS array
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    return borders[::-1]  # Return in ascending order
```

**Why this improvement works**: KMP failure function directly gives us border lengths in linear time.

### Improvement 2: Z-Algorithm Approach - O(|s|)
**Description**: Use Z-algorithm to find borders by comparing string with itself.

```python
def compute_z_array(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    
    for i in range(1, n):
        if i > r:
            l = r = i
            while r < n and s[r - l] == s[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            k = i - l
            if z[k] < r - i + 1:
                z[i] = z[k]
            else:
                l = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    
    return z

def finding_borders_z_algorithm(s):
    borders = []
    n = len(s)
    z = compute_z_array(s)
    
    # Find borders using Z-array
    for i in range(1, n):
        if z[i] == n - i:
            borders.append(s[:z[i]])
    
    return borders
```

**Why this improvement works**: Z-algorithm finds all positions where string matches its own suffix.

### Alternative: Rolling Hash Approach - O(|s|)
**Description**: Use rolling hash to compare prefixes and suffixes efficiently.

```python
def finding_borders_rolling_hash(s):
    borders = []
    n = len(s)
    
    # Simple hash function
    def hash_string(s):
        hash_val = 0
        for char in s:
            hash_val = (hash_val * 31 + ord(char)) % (10**9 + 7)
        return hash_val
    
    # Check each possible border length
    for length in range(1, n):
        prefix_hash = hash_string(s[:length])
        suffix_hash = hash_string(s[n - length:])
        
        if prefix_hash == suffix_hash and s[:length] == s[n - length:]:
            borders.append(s[:length])
    
    return borders
```

**Why this works**: Rolling hash provides fast comparison of prefixes and suffixes.

## Final Optimal Solution

```python
s = input().strip()

def compute_lps(s):
    n = len(s)
    lps = [0] * n
    length = 0
    i = 1
    
    while i < n:
        if s[i] == s[length]:
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

def finding_borders_kmp(s):
    borders = []
    n = len(s)
    lps = compute_lps(s)
    
    # Find all borders using LPS array
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    return borders[::-1]  # Return in ascending order

borders = finding_borders_kmp(s)
for border in borders:
    print(border)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|²) | O(|s|) | Simple but slow |
| KMP | O(|s|) | O(|s|) | Use failure function |
| Z-Algorithm | O(|s|) | O(|s|) | Z-array computation |
| Rolling Hash | O(|s|) | O(|s|) | Hash-based comparison |

## Key Insights for Other Problems

### 1. **Border Finding Problems**
**Principle**: Use KMP failure function or Z-algorithm to find borders efficiently.
**Applicable to**:
- Border finding problems
- String algorithms
- Pattern matching
- Algorithm design

**Example Problems**:
- Border finding problems
- String algorithms
- Pattern matching
- Algorithm design

### 2. **LPS Array Applications**
**Principle**: Use longest proper prefix that is also a suffix for border detection.
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

### 3. **Z-Array for Self-Matching**
**Principle**: Use Z-array to find positions where string matches its own suffix.
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

### 4. **Hash-based String Comparison**
**Principle**: Use rolling hash for efficient string comparison.
**Applicable to**:
- String algorithms
- Hash functions
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Hash functions
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **KMP Border Finding Pattern**
```python
def find_borders_kmp(s):
    def compute_lps(s):
        n = len(s)
        lps = [0] * n
        length = 0
        i = 1
        
        while i < n:
            if s[i] == s[length]:
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
    
    borders = []
    n = len(s)
    lps = compute_lps(s)
    
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    return borders[::-1]
```

### 2. **Z-Algorithm Border Pattern**
```python
def find_borders_z_algorithm(s):
    def compute_z_array(s):
        n = len(s)
        z = [0] * n
        l = r = 0
        
        for i in range(1, n):
            if i > r:
                l = r = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and s[r - l] == s[r]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        
        return z
    
    borders = []
    n = len(s)
    z = compute_z_array(s)
    
    for i in range(1, n):
        if z[i] == n - i:
            borders.append(s[:z[i]])
    
    return borders
```

### 3. **Rolling Hash Border Pattern**
```python
def find_borders_rolling_hash(s):
    def hash_string(s):
        hash_val = 0
        for char in s:
            hash_val = (hash_val * 31 + ord(char)) % (10**9 + 7)
        return hash_val
    
    borders = []
    n = len(s)
    
    for length in range(1, n):
        prefix_hash = hash_string(s[:length])
        suffix_hash = hash_string(s[n - length:])
        
        if prefix_hash == suffix_hash and s[:length] == s[n - length:]:
            borders.append(s[:length])
    
    return borders
```

## Edge Cases to Remember

1. **Empty string**: No borders
2. **Single character**: No borders
3. **All same characters**: Multiple borders
4. **No borders**: Return empty list
5. **Multiple borders**: Return all in ascending order

## Problem-Solving Framework

1. **Identify border nature**: This is a border finding problem
2. **Choose algorithm**: Use KMP failure function for efficiency
3. **Compute LPS**: Build longest proper prefix that is also a suffix array
4. **Extract borders**: Use LPS array to find all border lengths
5. **Return result**: Return borders in ascending order

---

*This analysis shows how to efficiently find borders using KMP failure function and other string algorithms.* 