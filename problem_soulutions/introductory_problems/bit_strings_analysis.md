---
layout: simple
title: "Bit Strings
permalink: /problem_soulutions/introductory_problems/bit_strings_analysis/"
---


# Bit Strings

## Problem Statement
Your task is to calculate the number of bit strings of length n.

For example, if n=3, the correct answer is 8, because the possible bit strings are 000, 001, 010, 011, 100, 101, 110, and 111.

### Input
The only input line contains an integer n.

### Output
Print the result modulo 10^9+7.

### Constraints
- 1 ≤ n ≤ 10^6

### Example
```
Input:
3

Output:
8
```

## Solution Progression

### Approach 1: Brute Force Generation - O(2^n)
**Description**: Generate all possible bit strings and count them.

```python
def bit_strings_brute_force(n):
    def generate_strings(length, current):
        if length == 0:
            return [current]
        
        strings = []"
        strings.extend(generate_strings(length - 1, current + '0'))
        strings.extend(generate_strings(length - 1, current + '1'))
        return strings
    
    all_strings = generate_strings(n, '')
    return len(all_strings) % (10**9 + 7)
```

**Why this is inefficient**: We're generating all 2^n bit strings, which is completely impractical for large n (up to 10^6).

### Improvement 1: Mathematical Formula - O(1)
**Description**: Use the mathematical formula 2^n to calculate the result directly.

```python
def bit_strings_math(n):
    MOD = 10**9 + 7
    result = pow(2, n, MOD)
    return result
```

**Why this improvement works**: For each position in the bit string, we have 2 choices (0 or 1). Therefore, the total number of bit strings is 2^n. We use modular exponentiation to handle large numbers efficiently.

### Improvement 2: Iterative Calculation - O(n)
**Description**: Calculate 2^n iteratively to avoid large intermediate values.

```python
def bit_strings_iterative(n):
    MOD = 10**9 + 7
    result = 1
    
    for _ in range(n):
        result = (result * 2) % MOD
    
    return result
```

**Why this improvement works**: We calculate 2^n by multiplying by 2 n times, taking modulo at each step to avoid integer overflow.

### Alternative: Binary Exponentiation - O(log n)
**Description**: Use binary exponentiation for more efficient calculation.

```python
def bit_strings_binary_exp(n):
    MOD = 10**9 + 7
    
    def binary_pow(base, exp, mod):
        result = 1
        base = base % mod
        
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            base = (base * base) % mod
            exp //= 2
        
        return result
    
    return binary_pow(2, n, MOD)
```

**Why this works**: Binary exponentiation calculates 2^n in O(log n) time by using the fact that 2^n = (2^(n/2))^2 when n is even.

## Final Optimal Solution

```python
n = int(input())
MOD = 10**9 + 7

# Use built-in pow function with modular arithmetic
result = pow(2, n, MOD)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n) | O(2^n) | Generate all strings |
| Mathematical Formula | O(1) | O(1) | Use 2^n formula |
| Iterative | O(n) | O(1) | Calculate iteratively |
| Binary Exponentiation | O(log n) | O(1) | Use binary exponentiation |

## Key Insights for Other Problems

### 1. **Mathematical Formula Recognition**
**Principle**: Recognize when mathematical formulas can replace brute force approaches.
**Applicable to**:
- Counting problems
- Mathematical problems
- Combinatorial problems
- Algorithm optimization

**Example Problems**:
- Bit strings
- Counting problems
- Mathematical sequences
- Combinatorial problems

### 2. **Modular Arithmetic**
**Principle**: Use modular arithmetic to handle large numbers and prevent overflow.
**Applicable to**:
- Large number problems
- Modular arithmetic
- Number theory
- Algorithm optimization

**Example Problems**:
- Large number calculations
- Modular arithmetic
- Number theory problems
- Algorithm optimization

### 3. **Exponentiation Optimization**
**Principle**: Use efficient exponentiation algorithms for large powers.
**Applicable to**:
- Exponentiation problems
- Algorithm optimization
- Mathematical problems
- Performance optimization

**Example Problems**:
- Exponentiation
- Algorithm optimization
- Mathematical problems
- Performance optimization

### 4. **Combinatorial Counting**
**Principle**: Use combinatorial principles to count possibilities efficiently.
**Applicable to**:
- Counting problems
- Combinatorial problems
- Mathematical problems
- Algorithm design

**Example Problems**:
- Counting problems
- Combinatorial problems
- Mathematical problems
- Algorithm design

## Notable Techniques

### 1. **Mathematical Formula Pattern**
```python
# Use mathematical formula instead of brute force
def solve_with_formula(inputs):
    return mathematical_formula(inputs)
```

### 2. **Modular Arithmetic Pattern**
```python
# Use modular arithmetic for large numbers
MOD = 10**9 + 7
result = (result * factor) % MOD
```

### 3. **Binary Exponentiation Pattern**
```python
# Use binary exponentiation for efficiency
def binary_pow(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result
```

## Edge Cases to Remember

1. **n = 1**: Result is 2 (0, 1)
2. **n = 0**: Result is 1 (empty string)
3. **Large n**: Handle with modular arithmetic
4. **Integer overflow**: Use modular arithmetic throughout
5. **Multiple test cases**: Process each case independently

## Problem-Solving Framework

1. **Identify counting nature**: This is about counting all possible bit strings
2. **Use mathematical formula**: Recognize that it's 2^n
3. **Handle large numbers**: Use modular arithmetic
4. **Optimize for efficiency**: Use built-in pow function
5. **Verify correctness**: Test with small examples

---

*This analysis shows how to efficiently count bit strings using mathematical formulas and modular arithmetic.* 