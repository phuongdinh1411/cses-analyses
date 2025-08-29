---
layout: simple
title: "Trailing Zeros"
permalink: /cses-analyses/problem_soulutions/introductory_problems/trailing_zeros_analysis
---


# Trailing Zeros

## Problem Statement
Your task is to calculate the number of trailing zeros in a factorial.

For example, 20!=2432902008176640000 and it has 4 trailing zeros.

### Input
The only input line contains an integer n.

### Output
Print the number of trailing zeros in n!.

### Constraints
- 1 ≤ n ≤ 10^9

### Example
```
Input:
20

Output:
4
```

## Solution Progression

### Approach 1: Brute Force Calculation - O(n)
**Description**: Calculate n! and count trailing zeros.

```python
def trailing_zeros_brute_force(n):
    # Calculate factorial
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    
    # Count trailing zeros
    count = 0
    while factorial % 10 == 0:
        count += 1
        factorial //= 10
    
    return count
```
**Why this is inefficient**: We're calculating the entire factorial, which becomes extremely large for large n. This leads to integer overflow and is completely impractical.

### Improvement 1: Mathematical Analysis - O(log n)
**Description**: Use mathematical analysis to count trailing zeros without calculating factorial.

```python
def trailing_zeros_math(n):
    # Count factors of 5 (since 2s are more abundant)
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    return count
```

**Why this improvement works**: Trailing zeros in factorial come from factors of 10, which are 2 × 5. Since there are always more factors of 2 than 5 in factorial, we only need to count factors of 5. We count multiples of 5, 25, 125, etc.

### Improvement 2: Optimized Counting - O(log n)
**Description**: Use a more efficient approach to count factors of 5.

```python
def trailing_zeros_optimized(n):
    count = 0
    i = 5
    
    while i <= n:
        count += n // i
        i *= 5
    
    return count
```

**Why this improvement works**: This approach is more concise and directly counts the number of factors of 5 in the factorial.

### Alternative: Logarithmic Approach - O(log n)
**Description**: Use logarithmic approach for even more efficiency.

```python
import math

def trailing_zeros_log(n):
    if n == 0:
        return 0
    
    # Find the highest power of 5 that divides n!
    max_power = int(math.log(n, 5))
    count = 0
    
    for power in range(1, max_power + 1):
        count += n // (5 ** power)
    
    return count
```

**Why this works**: We use logarithm to find the maximum power of 5 we need to consider, then count all factors of 5 up to that power.

## Final Optimal Solution

```python
n = int(input())

count = 0
i = 5

while i <= n:
    count += n // i
    i *= 5

print(count)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n) | O(1) | Calculate factorial |
| Mathematical Analysis | O(log n) | O(1) | Count factors of 5 |
| Optimized Counting | O(log n) | O(1) | Efficient counting |
| Logarithmic | O(log n) | O(1) | Use logarithm |

## Key Insights for Other Problems

### 1. **Mathematical Analysis**
**Principle**: Use mathematical analysis to avoid brute force calculations.
**Applicable to**:
- Mathematical problems
- Number theory
- Algorithm optimization
- Problem solving

**Example Problems**:
- Trailing zeros
- Mathematical problems
- Number theory
- Algorithm optimization

### 2. **Prime Factorization**
**Principle**: Use prime factorization to understand number properties.
**Applicable to**:
- Number theory
- Mathematical problems
- Factorization problems
- Algorithm design

**Example Problems**:
- Prime factorization
- Number theory problems
- Mathematical problems
- Algorithm design

### 3. **Counting Factors**
**Principle**: Count specific factors instead of calculating large numbers.
**Applicable to**:
- Counting problems
- Number theory
- Mathematical problems
- Algorithm optimization

**Example Problems**:
- Factor counting
- Number theory problems
- Mathematical problems
- Algorithm optimization

### 4. **Logarithmic Analysis**
**Principle**: Use logarithmic analysis to understand growth patterns.
**Applicable to**:
- Mathematical analysis
- Algorithm complexity
- Growth analysis
- Problem solving

**Example Problems**:
- Mathematical analysis
- Algorithm complexity
- Growth analysis
- Problem solving

## Notable Techniques

### 1. **Mathematical Analysis Pattern**
```python
# Use mathematical analysis instead of brute force
def analyze_mathematically(inputs):
    # Find mathematical pattern
    pattern = find_pattern(inputs)
    # Apply mathematical formula
    return apply_formula(pattern, inputs)
```

### 2. **Factor Counting Pattern**
```python
# Count specific factors efficiently
def count_factors(n, factor):
    count = 0
    power = factor
    while power <= n:
        count += n // power
        power *= factor
    return count
```

### 3. **Logarithmic Analysis Pattern**
```python
# Use logarithm for analysis
import math
def logarithmic_analysis(n, base):
    max_power = int(math.log(n, base))
    # Process up to max_power
```

## Edge Cases to Remember

1. **n = 0**: Result is 0 (0! = 1, no trailing zeros)
2. **n = 1**: Result is 0 (1! = 1, no trailing zeros)
3. **n = 5**: Result is 1 (5! = 120, one trailing zero)
4. **Large n**: Handle efficiently with mathematical analysis
5. **Integer overflow**: Avoid calculating large factorials

## Problem-Solving Framework

1. **Identify mathematical nature**: This is about counting factors in factorial
2. **Use mathematical analysis**: Avoid calculating large factorials
3. **Count specific factors**: Focus on factors of 5 (limiting factor)
4. **Handle edge cases**: Consider special cases and boundaries
5. **Optimize for efficiency**: Use O(log n) approach

---

*This analysis shows how to efficiently count trailing zeros using mathematical analysis instead of brute force calculation.* 