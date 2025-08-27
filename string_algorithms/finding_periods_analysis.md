# CSES Finding Periods - Problem Analysis

## Problem Statement
Given a string, find the smallest period of the string. A period is the smallest positive integer k such that the string can be written as a repetition of its first k characters.

### Input
The first input line has a string s.

### Output
Print the smallest period of the string.

### Constraints
- 1 ≤ |s| ≤ 10^6

### Example
```
Input:
abcabcabc

Output:
3
```

## Solution Progression

### Approach 1: Naive Period Finding - O(|s|²)
**Description**: Check each possible period length by testing if the string repeats.

```python
def finding_periods_naive(s):
    n = len(s)
    
    for k in range(1, n + 1):
        if n % k == 0:
            # Check if string repeats with period k
            is_period = True
            for i in range(k, n):
                if s[i] != s[i % k]:
                    is_period = False
                    break
            
            if is_period:
                return k
    
    return n
```

**Why this is inefficient**: Quadratic time complexity for large strings.

### Improvement 1: KMP-based Period Finding - O(|s|)
**Description**: Use KMP failure function to find the smallest period efficiently.

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

def finding_periods_kmp(s):
    n = len(s)
    lps = compute_lps(s)
    
    # The smallest period is n - lps[n-1]
    period = n - lps[n - 1]
    
    # Verify that this is actually a period
    if n % period == 0:
        return period
    else:
        return n
```

**Why this improvement works**: KMP failure function gives us the border length, which helps find the period.

### Improvement 2: Z-Algorithm Approach - O(|s|)
**Description**: Use Z-algorithm to find the smallest period by checking self-matching.

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

def finding_periods_z_algorithm(s):
    n = len(s)
    z = compute_z_array(s)
    
    # Find the smallest period
    for k in range(1, n + 1):
        if n % k == 0:
            # Check if string repeats with period k
            is_period = True
            for i in range(k, n, k):
                if z[i] < min(k, n - i):
                    is_period = False
                    break
            
            if is_period:
                return k
    
    return n
```

**Why this improvement works**: Z-algorithm helps us check if the string repeats with a given period.

### Alternative: Border-based Period Finding - O(|s|)
**Description**: Use border properties to find the smallest period.

```python
def finding_periods_border_based(s):
    n = len(s)
    
    # Find the longest border
    lps = compute_lps(s)
    longest_border = lps[n - 1]
    
    # The smallest period is n - longest_border
    period = n - longest_border
    
    # Verify that this is actually a period
    if n % period == 0:
        # Additional check: verify the period works
        for i in range(period, n):
            if s[i] != s[i % period]:
                return n
        return period
    else:
        return n
```

**Why this works**: The border-based approach uses the relationship between borders and periods.

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

def finding_periods_kmp(s):
    n = len(s)
    lps = compute_lps(s)
    
    # The smallest period is n - lps[n-1]
    period = n - lps[n - 1]
    
    # Verify that this is actually a period
    if n % period == 0:
        # Additional check: verify the period works
        for i in range(period, n):
            if s[i] != s[i % period]:
                return n
        return period
    else:
        return n

period = finding_periods_kmp(s)
print(period)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|²) | O(1) | Simple but slow |
| KMP | O(|s|) | O(|s|) | Use failure function |
| Z-Algorithm | O(|s|) | O(|s|) | Z-array computation |
| Border-based | O(|s|) | O(|s|) | Border-period relationship |

## Key Insights for Other Problems

### 1. **Period Finding Problems**
**Principle**: Use KMP failure function or border properties to find periods efficiently.
**Applicable to**:
- Period finding problems
- String algorithms
- Pattern matching
- Algorithm design

**Example Problems**:
- Period finding problems
- String algorithms
- Pattern matching
- Algorithm design

### 2. **Border-Period Relationship**
**Principle**: The smallest period is related to the longest border of the string.
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

### 3. **Period Verification**
**Principle**: Always verify that a candidate period actually works for the entire string.
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

### 4. **Divisibility Check**
**Principle**: A valid period must divide the string length evenly.
**Applicable to**:
- String algorithms
- Number theory
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Number theory
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **KMP Period Finding Pattern**
```python
def find_period_kmp(s):
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
    
    n = len(s)
    lps = compute_lps(s)
    period = n - lps[n - 1]
    
    if n % period == 0:
        for i in range(period, n):
            if s[i] != s[i % period]:
                return n
        return period
    else:
        return n
```

### 2. **Z-Algorithm Period Pattern**
```python
def find_period_z_algorithm(s):
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
    
    n = len(s)
    z = compute_z_array(s)
    
    for k in range(1, n + 1):
        if n % k == 0:
            is_period = True
            for i in range(k, n, k):
                if z[i] < min(k, n - i):
                    is_period = False
                    break
            
            if is_period:
                return k
    
    return n
```

### 3. **Period Verification Pattern**
```python
def verify_period(s, period):
    n = len(s)
    if n % period != 0:
        return False
    
    for i in range(period, n):
        if s[i] != s[i % period]:
            return False
    
    return True
```

## Edge Cases to Remember

1. **Single character**: Period is 1
2. **All same characters**: Period is 1
3. **No repetition**: Period equals string length
4. **Empty string**: Handle appropriately
5. **Prime length**: Period might be the full length

## Problem-Solving Framework

1. **Identify period nature**: This is a period finding problem
2. **Choose algorithm**: Use KMP failure function for efficiency
3. **Compute border**: Find the longest border using LPS array
4. **Calculate period**: Period = string length - border length
5. **Verify period**: Ensure the period actually works for the entire string

---

*This analysis shows how to efficiently find periods using KMP failure function and border properties.* 