---
layout: simple
title: "Trailing Zeros"
permalink: /problem_soulutions/introductory_problems/trailing_zeros_analysis
---

# Trailing Zeros

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand factorial properties and trailing zero counting concepts
- Apply mathematical formulas to count trailing zeros without computing large factorials
- Implement efficient trailing zero counting algorithms with proper mathematical calculations
- Optimize trailing zero counting using mathematical analysis and prime factorization
- Handle edge cases in factorial problems (large n, mathematical precision, overflow prevention)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Factorial properties, trailing zero counting, mathematical formulas, prime factorization
- **Data Structures**: Mathematical calculations, prime tracking, factorization tracking, mathematical operations
- **Mathematical Concepts**: Factorial theory, prime factorization, trailing zero mathematics, mathematical analysis
- **Programming Skills**: Mathematical calculations, prime factorization, trailing zero counting, algorithm implementation
- **Related Problems**: Factorial problems, Mathematical formulas, Prime factorization, Trailing zero problems

## Problem Description

**Problem**: Calculate the number of trailing zeros in n! (n factorial).

**Input**: An integer n (1 ≤ n ≤ 10⁹)

**Output**: The number of trailing zeros in n!.

**Constraints**:
- 1 ≤ n ≤ 10⁹
- Trailing zeros come from factors of 10 = 2 × 5
- In factorial, there are always more factors of 2 than 5
- Need to count factors of 5 efficiently
- Cannot compute n! directly for large n

**Example**:
```
Input: 20

Output: 4

Explanation: 20! = 2432902008176640000 has 4 trailing zeros.
```

## Visual Example

### Input and Factorial Calculation
```
Input: n = 20

20! = 20 × 19 × 18 × ... × 2 × 1
20! = 2432902008176640000
Trailing zeros: 4
```

### Factor Analysis
```
Numbers 1 to 20:
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20

Factors of 5:
- 5: 1 factor of 5
- 10: 1 factor of 5
- 15: 1 factor of 5
- 20: 1 factor of 5

Total factors of 5: 4
```

### Mathematical Formula
```
For n = 20:
- Count multiples of 5: 20/5 = 4
- Count multiples of 25: 20/25 = 0
- Count multiples of 125: 20/125 = 0
- Total trailing zeros = 4 + 0 + 0 = 4
```

### Key Insight
The solution works by:
1. Using mathematical properties of factorial
2. Counting factors of 5 instead of computing factorial
3. Using logarithmic time complexity
4. Time complexity: O(log n) for mathematical approach
5. Space complexity: O(1) for constant variables

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Factorial Calculation (Inefficient)

**Key Insights from Brute Force Solution:**
- Calculate n! directly and count trailing zeros
- Simple but computationally expensive approach
- Not suitable for large n
- Straightforward implementation but poor performance

**Algorithm:**
1. Calculate n! by multiplying all numbers from 1 to n
2. Count trailing zeros by repeatedly dividing by 10
3. Handle large numbers with integer overflow
4. Return the count of trailing zeros

**Visual Example:**
```
Brute force: Calculate factorial directly
For n = 20:
- Calculate 20! = 2432902008176640000
- Count trailing zeros: 0000 → 4 zeros
```

**Implementation:**
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

def solve_trailing_zeros_brute_force():
    n = int(input())
    result = trailing_zeros_brute_force(n)
    print(result)
```

**Time Complexity:** O(n) for calculating factorial
**Space Complexity:** O(log n!) for storing factorial

**Why it's inefficient:**
- O(n) time complexity is too slow for large n
- Not suitable for competitive programming with n up to 10⁹
- Inefficient for large inputs
- Poor performance with factorial growth

### Approach 2: Mathematical Analysis with Factor Counting (Better)

**Key Insights from Mathematical Solution:**
- Use mathematical properties of factorial
- Much more efficient than brute force approach
- Standard method for trailing zero problems
- Can handle larger n than brute force

**Algorithm:**
1. Understand that trailing zeros come from factors of 10 = 2 × 5
2. Count factors of 5 (since 2s are more abundant)
3. Count multiples of 5, 25, 125, etc.
4. Sum all contributions

**Visual Example:**
```
Mathematical approach: Count factors of 5
For n = 20:
- Count multiples of 5: 20/5 = 4
- Count multiples of 25: 20/25 = 0
- Count multiples of 125: 20/125 = 0
- Total trailing zeros = 4 + 0 + 0 = 4
```

**Implementation:**
```python
def trailing_zeros_mathematical(n):
    # Count factors of 5 (since 2s are more abundant)
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    return count

def solve_trailing_zeros_mathematical():
    n = int(input())
    result = trailing_zeros_mathematical(n)
    print(result)
```

**Time Complexity:** O(log n) for mathematical calculation
**Space Complexity:** O(1) for storing variables

**Why it's better:**
- O(log n) time complexity is much better than O(n)
- Uses mathematical properties for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Mathematical Formula (Optimal)

**Key Insights from Optimized Mathematical Solution:**
- Use optimized mathematical formulas for efficiency
- Most efficient approach for trailing zero problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized mathematical formulas
2. Apply efficient factor counting
3. Handle edge cases efficiently
4. Return the optimal solution

**Visual Example:**
```
Optimized mathematical: Use efficient formulas
For n = 20:
- Count factors of 5: 20/5 + 20/25 + 20/125 + ... = 4
- Result = 4
```

**Implementation:**
```python
def trailing_zeros_optimized(n):
    # Count factors of 5
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    return count

def solve_trailing_zeros():
    n = int(input())
    result = trailing_zeros_optimized(n)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_trailing_zeros()
```

**Time Complexity:** O(log n) for optimized mathematical calculation
**Space Complexity:** O(1) for storing variables

**Why it's optimal:**
- O(log n) time complexity is optimal for this problem
- Uses optimized mathematical formulas
- Most efficient approach for competitive programming
- Standard method for trailing zero calculation optimization

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Trailing Zeros in Different Bases
**Problem**: Calculate trailing zeros in n! for different bases (e.g., base 12).

**Link**: [CSES Problem Set - Trailing Zeros Different Bases](https://cses.fi/problemset/task/trailing_zeros_different_bases)

```python
def trailing_zeros_different_base(n, base):
    # Factorize the base
    factors = {}
    temp = base
    for i in range(2, int(temp**0.5) + 1):
        while temp % i == 0:
            factors[i] = factors.get(i, 0) + 1
            temp //= i
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    
    # Count factors for each prime in the base
    min_count = float('inf')
    for prime, exp in factors.items():
        count = 0
        power = prime
        while power <= n:
            count += n // power
            power *= prime
        min_count = min(min_count, count // exp)
    
    return min_count
```

### Variation 2: Trailing Zeros in Product of Range
**Problem**: Calculate trailing zeros in the product of numbers from a to b.

**Link**: [CSES Problem Set - Trailing Zeros Range Product](https://cses.fi/problemset/task/trailing_zeros_range_product)

```python
def trailing_zeros_range_product(a, b):
    def count_factors(n, factor):
        count = 0
        power = factor
        while power <= n:
            count += n // power
            power *= factor
        return count
    
    # Count factors of 5 in range [a, b]
    count_5 = count_factors(b, 5) - count_factors(a - 1, 5)
    count_2 = count_factors(b, 2) - count_factors(a - 1, 2)
    
    return min(count_2, count_5)
```

### Variation 3: Trailing Zeros in Binomial Coefficient
**Problem**: Calculate trailing zeros in C(n, k) = n! / (k! × (n-k)!).

**Link**: [CSES Problem Set - Trailing Zeros Binomial](https://cses.fi/problemset/task/trailing_zeros_binomial)

```python
def trailing_zeros_binomial(n, k):
    def count_factors(n, factor):
        count = 0
        power = factor
        while power <= n:
            count += n // power
            power *= factor
        return count
    
    # Count factors of 5 in n!, k!, and (n-k)!
    count_5 = count_factors(n, 5) - count_factors(k, 5) - count_factors(n - k, 5)
    count_2 = count_factors(n, 2) - count_factors(k, 2) - count_factors(n - k, 2)
    
    return min(count_2, count_5)
```

### Related Problems

#### **CSES Problems**
- [Trailing Zeros](https://cses.fi/problemset/task/1618) - Count trailing zeros in factorial
- [Factorial](https://cses.fi/problemset/task/1083) - Calculate factorial
- [Prime Factorization](https://cses.fi/problemset/task/1081) - Prime factorization problems

#### **LeetCode Problems**
- [Factorial Trailing Zeroes](https://leetcode.com/problems/factorial-trailing-zeroes/) - Count trailing zeros
- [Preimage Size of Factorial Zeroes Function](https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/) - Find numbers with k trailing zeros
- [Count Primes](https://leetcode.com/problems/count-primes/) - Count prime numbers
- [Ugly Number](https://leetcode.com/problems/ugly-number/) - Check if number has only 2,3,5 factors

#### **Problem Categories**
- **Number Theory**: Factorial properties, prime factorization, mathematical analysis
- **Mathematical Formulas**: Efficient counting, mathematical optimization, formula derivation
- **Prime Numbers**: Prime factorization, factor counting, mathematical properties
- **Algorithm Design**: Mathematical algorithms, optimization techniques, efficient calculations

## 📚 Learning Points

1. **Factorial Properties**: Essential for understanding trailing zero problems
2. **Mathematical Analysis**: Key technique for efficient counting
3. **Prime Factorization**: Important for understanding factor counting
4. **Mathematical Formulas**: Critical for understanding efficient calculations
5. **Algorithm Optimization**: Foundation for many mathematical algorithms
6. **Mathematical Properties**: Critical for competitive programming performance

## 📝 Summary

The Trailing Zeros problem demonstrates factorial properties and mathematical analysis concepts for efficient counting. We explored three approaches:

1. **Brute Force Factorial Calculation**: O(n) time complexity using direct factorial calculation, inefficient for large n
2. **Mathematical Analysis with Factor Counting**: O(log n) time complexity using mathematical properties and factor counting, better approach for trailing zero problems
3. **Optimized Mathematical Formula**: O(log n) time complexity with optimized mathematical formulas, optimal approach for trailing zero calculation optimization

The key insights include understanding factorial properties, using mathematical analysis for efficient factor counting, and applying mathematical formulas for optimal performance. This problem serves as an excellent introduction to factorial mathematics and mathematical analysis algorithms.
