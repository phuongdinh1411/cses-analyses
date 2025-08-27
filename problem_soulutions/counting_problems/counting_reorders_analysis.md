# CSES Counting Reorders - Problem Analysis

## Problem Statement
Given a string s, count the number of different strings that can be obtained by reordering the characters of s.

### Input
The first input line has a string s.

### Output
Print the number of different reorderings modulo 10^9 + 7.

### Constraints
- 1 ≤ |s| ≤ 100

### Example
```
Input:
aab

Output:
3
```

## Solution Progression

### Approach 1: Generate All Permutations - O(|s|!)
**Description**: Generate all permutations and count unique ones.

```python
def counting_reorders_naive(s):
    MOD = 10**9 + 7
    from itertools import permutations
    
    unique_perms = set()
    for perm in permutations(s):
        unique_perms.add(''.join(perm))
    
    return len(unique_perms) % MOD
```

**Why this is inefficient**: O(|s|!) complexity is too slow for long strings.

### Improvement 1: Mathematical Formula - O(|s|)
**Description**: Use multinomial coefficient formula.

```python
def counting_reorders_optimized(s):
    MOD = 10**9 + 7
    
    # Count frequency of each character
    from collections import Counter
    freq = Counter(s)
    
    # Calculate multinomial coefficient: n! / (f1! * f2! * ... * fk!)
    n = len(s)
    
    # Calculate n!
    factorial_n = 1
    for i in range(1, n + 1):
        factorial_n = (factorial_n * i) % MOD
    
    # Calculate denominator: f1! * f2! * ... * fk!
    denominator = 1
    for count in freq.values():
        factorial_count = 1
        for i in range(1, count + 1):
            factorial_count = (factorial_count * i) % MOD
        denominator = (denominator * factorial_count) % MOD
    
    # Calculate result using modular inverse
    def mod_inverse(a, m):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, y = extended_gcd(a, m)
        if gcd != 1:
            return None
        return (x % m + m) % m
    
    inverse_denominator = mod_inverse(denominator, MOD)
    result = (factorial_n * inverse_denominator) % MOD
    
    return result
```

**Why this improvement works**: Mathematical formula gives O(|s|) solution.

## Final Optimal Solution

```python
s = input().strip()

def count_reorders(s):
    MOD = 10**9 + 7
    
    # Count frequency of each character
    from collections import Counter
    freq = Counter(s)
    
    # Calculate multinomial coefficient: n! / (f1! * f2! * ... * fk!)
    n = len(s)
    
    # Calculate n!
    factorial_n = 1
    for i in range(1, n + 1):
        factorial_n = (factorial_n * i) % MOD
    
    # Calculate denominator: f1! * f2! * ... * fk!
    denominator = 1
    for count in freq.values():
        factorial_count = 1
        for i in range(1, count + 1):
            factorial_count = (factorial_count * i) % MOD
        denominator = (denominator * factorial_count) % MOD
    
    # Calculate result using modular inverse
    def mod_inverse(a, m):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, y = extended_gcd(a, m)
        if gcd != 1:
            return None
        return (x % m + m) % m
    
    inverse_denominator = mod_inverse(denominator, MOD)
    result = (factorial_n * inverse_denominator) % MOD
    
    return result

result = count_reorders(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Generate All Permutations | O(|s|!) | O(|s|!) | Simple but factorial |
| Mathematical Formula | O(|s|) | O(|s|) | Optimal solution |

## Key Insights for Other Problems

### 1. **Multinomial Coefficient**
**Principle**: Number of distinct permutations = n! / (f1! * f2! * ... * fk!).
**Applicable to**: Permutation counting problems, combinatorics problems

### 2. **Modular Inverse**
**Principle**: Use extended Euclidean algorithm for modular division.
**Applicable to**: Modular arithmetic problems, division problems

### 3. **Frequency Counting**
**Principle**: Count character frequencies to calculate multinomial coefficient.
**Applicable to**: String analysis problems, counting problems

## Notable Techniques

### 1. **Multinomial Coefficient Calculation**
```python
def multinomial_coefficient(freq, MOD):
    n = sum(freq.values())
    
    # Calculate n!
    factorial_n = 1
    for i in range(1, n + 1):
        factorial_n = (factorial_n * i) % MOD
    
    # Calculate denominator
    denominator = 1
    for count in freq.values():
        factorial_count = 1
        for i in range(1, count + 1):
            factorial_count = (factorial_count * i) % MOD
        denominator = (denominator * factorial_count) % MOD
    
    return factorial_n, denominator
```

### 2. **Modular Inverse**
```python
def mod_inverse(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m
```

### 3. **Frequency Analysis**
```python
def analyze_frequency(s):
    from collections import Counter
    return Counter(s)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a permutation counting problem with duplicates
2. **Choose approach**: Use multinomial coefficient formula
3. **Count frequencies**: Count frequency of each character
4. **Calculate factorial**: Compute n! and denominator
5. **Use modular inverse**: Handle division in modular arithmetic
6. **Return result**: Output number of distinct reorderings

---

*This analysis shows how to efficiently count distinct reorderings of a string using multinomial coefficients.* 