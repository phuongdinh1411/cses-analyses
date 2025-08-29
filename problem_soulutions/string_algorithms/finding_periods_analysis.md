---
layout: simple
title: "Finding Periods"
permalink: /cses-analyses/problem_soulutions/string_algorithms/finding_periods_analysis
---


# Finding Periods

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Finding Periods with Constraints**
**Problem**: Find periods with additional constraints (minimum/maximum length, etc.).
```python
def constrained_finding_periods(s, constraints):
    # constraints = {'min_period': x, 'max_period': y, 'alphabet': chars}
    
    n = len(s)
    
    # Apply constraints
    if 'alphabet' in constraints:
        if not all(c in constraints['alphabet'] for c in s):
            return n
    
    # Use KMP failure function
    lps = compute_lps(s)
    period = n - lps[n - 1]
    
    # Apply period constraints
    if 'min_period' in constraints:
        period = max(period, constraints['min_period'])
    
    if 'max_period' in constraints:
        period = min(period, constraints['max_period'])
    
    # Verify period
    if n % period == 0:
        for i in range(period, n):
            if s[i] != s[i % period]:
                return n
        return period
    else:
        return n
```

#### **Variation 2: Finding Periods with Multiple Criteria**
**Problem**: Find periods that optimize multiple criteria (length, frequency, etc.).
```python
def multi_criteria_finding_periods(s, criteria):
    # criteria = {'length_weight': w1, 'frequency_weight': w2, 'simplicity_weight': w3}
    
    n = len(s)
    best_period = n
    best_score = 0
    
    # Try all possible periods
    for period in range(1, n + 1):
        if n % period == 0:
            is_valid = True
            for i in range(period, n):
                if s[i] != s[i % period]:
                    is_valid = False
                    break
            
            if is_valid:
                score = 0
                
                # Length score (shorter is better)
                if 'length_weight' in criteria:
                    score += criteria['length_weight'] * (n / period)
                
                # Frequency score (higher frequency is better)
                if 'frequency_weight' in criteria:
                    score += criteria['frequency_weight'] * (n // period)
                
                # Simplicity score (simpler patterns are better)
                if 'simplicity_weight' in criteria:
                    # Count unique characters in period
                    unique_chars = len(set(s[:period]))
                    score += criteria['simplicity_weight'] * (period - unique_chars)
                
                if score > best_score:
                    best_score = score
                    best_period = period
    
    return best_period
```

#### **Variation 3: Finding Periods with Costs**
**Problem**: Each character has a cost, find period with minimum total cost.
```python
def cost_based_finding_periods(s, char_costs):
    # char_costs[c] = cost of character c
    
    n = len(s)
    best_period = n
    min_cost = float('inf')
    
    # Try all possible periods
    for period in range(1, n + 1):
        if n % period == 0:
            is_valid = True
            for i in range(period, n):
                if s[i] != s[i % period]:
                    is_valid = False
                    break
            
            if is_valid:
                # Calculate cost of the period
                period_cost = sum(char_costs.get(c, 1) for c in s[:period])
                total_cost = period_cost * (n // period)
                
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_period = period
    
    return best_period
```

#### **Variation 4: Finding Periods with Probabilities**
**Problem**: Characters have probabilities, find expected period.
```python
def probabilistic_finding_periods(s, char_probs):
    # char_probs[c] = probability of character c
    
    n = len(s)
    # For probabilistic strings, calculate expected period
    expected_period = n
    
    # Calculate expected period based on character probabilities
    for period in range(1, n + 1):
        if n % period == 0:
            prob_period = 1.0
            for i in range(period, n):
                if s[i] == s[i % period]:
                    prob_period *= char_probs.get(s[i], 0.1)
                else:
                    prob_period = 0
                    break
            
            if prob_period >= 0.5:  # Threshold for "period"
                expected_period = min(expected_period, period)
    
    return expected_period
```

#### **Variation 5: Finding Periods with Multiple Strings**
**Problem**: Find common periods across multiple strings.
```python
def multiple_string_finding_periods(strings):
    # Find common periods across all strings
    
    if not strings:
        return 1
    
    # Find periods for each string
    periods = []
    for s in strings:
        period = find_period_kmp(s)
        periods.append(period)
    
    # Find greatest common divisor of all periods
    from math import gcd
    common_period = periods[0]
    for period in periods[1:]:
        common_period = gcd(common_period, period)
    
    return common_period
```

### 🔗 **Related Problems & Concepts**

#### **1. Periodicity Problems**
- **Period Detection**: Detect periodic patterns
- **Period Analysis**: Analyze periodic properties
- **Period Prediction**: Predict future periods
- **Period Classification**: Classify periods

#### **2. String Analysis Problems**
- **Border Analysis**: Find borders and periods
- **Suffix Analysis**: Analyze suffix properties
- **Prefix Analysis**: Analyze prefix properties
- **Pattern Analysis**: Analyze repeating patterns

#### **3. String Algorithms**
- **KMP Algorithm**: Efficient pattern matching
- **Z-Algorithm**: Linear time string processing
- **Failure Functions**: KMP failure function applications
- **Border Functions**: Border-based algorithms

#### **4. Optimization Problems**
- **Minimization**: Find minimum value solutions
- **Cost Optimization**: Optimize with respect to costs
- **Constrained Optimization**: Optimization with constraints
- **Multi-objective Optimization**: Optimize multiple criteria

#### **5. Algorithmic Techniques**
- **Dynamic Programming**: Solve optimization problems
- **Two Pointers**: Use two pointers for efficiency
- **Sliding Window**: Process data in windows
- **Mathematical Analysis**: Use mathematical properties

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    period = find_period_kmp(s)
    print(period)
```

#### **2. Range Queries on Period Finding**
```python
def range_period_finding_queries(s, queries):
    # queries = [(l, r), ...] - find period of substring s[l:r]
    
    results = []
    for l, r in queries: substring = s[
l: r]
        period = find_period_kmp(substring)
        results.append(period)
    
    return results
```

#### **3. Interactive Period Finding Problems**
```python
def interactive_period_finding():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        period = find_period_kmp(s)
        print(f"String: {s}")
        print(f"Period: {period}")
        
        # Show the repeating pattern
        if period < len(s):
            pattern = s[:period]
            print(f"Repeating pattern: {pattern}")
```

### 🧮 **Mathematical Extensions**

#### **1. Number Theory**
- **Divisibility**: Study of divisibility properties
- **Greatest Common Divisor**: Find GCD of numbers
- **Least Common Multiple**: Find LCM of numbers
- **Prime Factorization**: Factor numbers into primes

#### **2. Periodicity Theory**
- **Periodic Functions**: Study of periodic mathematical functions
- **Fourier Analysis**: Analyze periodic components
- **Harmonic Analysis**: Study of harmonic patterns
- **Wave Theory**: Study of wave-like patterns

#### **3. String Theory**
- **String Properties**: Periodicity, borders, periods
- **String Functions**: Mathematical functions on strings
- **String Complexity**: Complexity measures for strings
- **String Transformations**: Mathematical transformations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **String Matching**: KMP, Boyer-Moore, Rabin-Karp algorithms
- **Suffix Structures**: Suffix arrays, suffix trees, suffix automata
- **String Compression**: LZ77, LZ78, Huffman coding
- **String Parsing**: Regular expressions, context-free parsing

#### **2. Mathematical Concepts**
- **Number Theory**: Properties of integers and divisibility
- **Combinatorics**: String combinatorics and counting
- **Information Theory**: Entropy, compression, encoding
- **Formal Languages**: Regular languages, context-free languages

#### **3. Programming Concepts**
- **String Manipulation**: Efficient string operations
- **Algorithm Design**: Systematic approach to problem solving
- **Complexity Analysis**: Time and space complexity
- **Optimization Techniques**: Improving algorithm performance

---

*This analysis demonstrates efficient period finding techniques and shows various extensions for periodicity problems.* 