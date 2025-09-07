---
layout: simple
title: "Finding Periods"
permalink: /problem_soulutions/string_algorithms/finding_periods_analysis
---


# Finding Periods

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand period finding problems and string repetition analysis
- Apply string matching algorithms or divisor checking to find smallest periods
- Implement efficient period finding algorithms with O(n) or O(n log n) time complexity
- Optimize period detection using string matching, prefix functions, and mathematical analysis
- Handle edge cases in period finding (no period, single character, all same characters)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String matching, period analysis, prefix functions, divisor checking, string repetition
- **Data Structures**: String data structures, prefix arrays, period tracking, repetition tracking
- **Mathematical Concepts**: Period theory, string repetition mathematics, divisor mathematics, prefix analysis
- **Programming Skills**: String manipulation, prefix function implementation, period detection, algorithm implementation
- **Related Problems**: Finding Borders (similar concept), String Functions (basic string operations), String algorithms

## 📋 Problem Description

Given a string, find the smallest period of the string. A period is the smallest positive integer k such that the string can be written as a repetition of its first k characters.

This is a string algorithm problem where we need to find the smallest period of a string. A period is the length of the smallest repeating unit that can generate the entire string. We can solve this efficiently using string matching algorithms or by checking divisors of the string length.

**Input**: 
- First line: string s (the input string)

**Output**: 
- Print the smallest period of the string

**Constraints**:
- 1 ≤ |s| ≤ 10⁶

**Example**:
```
Input:
abcabcabc

Output:
3
```

**Explanation**: 
The string "abcabcabc" can be written as a repetition of "abc" (3 characters):
- "abc" + "abc" + "abc" = "abcabcabc"
- The smallest period is 3, which is the length of the repeating unit "abc"

## 🎯 Visual Example

### Input
```
String: "abcabcabc"
```

### Period Detection Process
```
Step 1: Check possible periods
- Length 1: "a" → "aaaaaaaaa" ≠ "abcabcabc" ✗
- Length 2: "ab" → "ababababa" ≠ "abcabcabc" ✗
- Length 3: "abc" → "abcabcabc" = "abcabcabc" ✓

Step 2: Verify period
- String: "abcabcabc"
- Period: "abc" (length 3)
- Repetition: "abc" + "abc" + "abc" = "abcabcabc"
- Smallest period: 3
```

### Period Visualization
```
String: a b c a b c a b c
Index:  0 1 2 3 4 5 6 7 8

Period "abc" (length 3):
a b c a b c a b c
a b c a b c a b c
✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓

Repeating unit: "abc"
Number of repetitions: 3
Total length: 3 × 3 = 9
```

### Key Insight
Period finding works by:
1. Checking each possible period length from 1 to n
2. Verifying if the string can be constructed by repeating the first k characters
3. Using string matching to check if pattern repeats
4. Time complexity: O(n²) for naive approach
5. Space complexity: O(1) for the algorithm

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
## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(|s|²) for naive approach, O(|s|) for optimized approach
- **Space Complexity**: O(|s|) for storing the string and auxiliary data
- **Why it works**: We can optimize by only checking divisors of the string length and using efficient string matching

### Key Implementation Points
- Only check divisors of the string length as potential periods
- Use efficient string matching to verify if a period is valid
- Handle edge cases like single character strings and non-periodic strings
- Optimize by checking smaller divisors first

## 🎯 Key Insights

### Important Concepts and Patterns
- **Period Detection**: Finding the smallest repeating unit in a string
- **String Periodicity**: Understanding when a string has a period
- **Divisor Checking**: Only checking divisors of string length for efficiency
- **String Matching**: Efficiently verifying if a period is valid

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Finding All Periods**
```python
def find_all_periods(s):
    # Find all possible periods of the string
    n = len(s)
    periods = []
    
    for k in range(1, n + 1):
        if n % k == 0:
            # Check if string repeats with period k
            is_period = True
            for i in range(k, n):
                if s[i] != s[i % k]:
                    is_period = False
                    break
            
            if is_period:
                periods.append(k)
    
    return periods

# Example usage
s = "abcabcabc"
periods = find_all_periods(s)
print(f"All periods: {periods}")
```

#### **2. Finding Period with KMP Algorithm**
```python
def find_period_kmp(s):
    # Find period using KMP failure function
    n = len(s)
    if n == 0:
        return 0
    
    # Build failure function
    failure = [0] * n
    j = 0
    
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = failure[j - 1]
        
        if s[i] == s[j]:
            j += 1
        
        failure[i] = j
    
    # The period is n - failure[n-1] if it divides n
    period = n - failure[n - 1]
    if n % period == 0:
        return period
    else:
        return n

# Example usage
s = "abcabcabc"
period = find_period_kmp(s)
print(f"Period (KMP): {period}")
```

#### **3. Finding Period with Z-Algorithm**
```python
def find_period_z_algorithm(s):
    # Find period using Z-algorithm
    n = len(s)
    if n == 0:
        return 0
    
    # Build Z-array
    z = [0] * n
    z[0] = n
    
    l, r = 0, 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    
    # Find the smallest period
    for i in range(1, n):
        if z[i] == n - i and n % i == 0:
            return i
    
    return n

# Example usage
s = "abcabcabc"
period = find_period_z_algorithm(s)
print(f"Period (Z-algorithm): {period}")
```

#### **4. Finding Period with Multiple Strings**
```python
def find_period_multiple_strings(strings):
    # Find periods for multiple strings
    results = {}
    
    for s in strings:
        n = len(s)
        period = n  # Default to full string length
        
        # Check all possible periods
        for k in range(1, n + 1):
            if n % k == 0:
                is_period = True
                for i in range(k, n):
                    if s[i] != s[i % k]:
                        is_period = False
                        break
                
                if is_period:
                    period = k
                    break
        
        results[s] = period
    
    return results

# Example usage
strings = ["abcabcabc", "ababab", "abcdef", "aaaa"]
results = find_period_multiple_strings(strings)
for s, period in results.items():
    print(f"String '{s}' has period {period}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **String Algorithms**: String matching, Pattern matching
- **Period Detection**: String periodicity, Repetitive patterns
- **String Analysis**: String properties, String structure
- **String Matching**: KMP algorithm, Z-algorithm

## 📚 Learning Points

### Key Takeaways
- **Period detection** is essential for understanding string structure
- **String periodicity** can be efficiently detected using various algorithms
- **Divisor checking** optimizes the search for valid periods
- **String matching algorithms** like KMP and Z-algorithm can be adapted for period finding

---

*This analysis demonstrates efficient period finding techniques and shows various extensions for periodicity problems.* 