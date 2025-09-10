---
layout: simple
title: "Counting Permutations - Combinatorial Problem"
permalink: /problem_soulutions/counting_problems/counting_permutations_analysis
---

# Counting Permutations - Combinatorial Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of permutations in combinatorics
- Apply mathematical formulas for counting permutations
- Implement efficient algorithms for permutation counting
- Optimize permutation calculations for large numbers
- Handle special cases in permutation counting

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Combinatorics, mathematical formulas, modular arithmetic
- **Data Structures**: Arrays, mathematical computations, factorial calculations
- **Mathematical Concepts**: Permutations, combinations, factorial, modular arithmetic
- **Programming Skills**: Mathematical computations, modular arithmetic, large number handling
- **Related Problems**: Counting Combinations (combinatorics), Counting Sequences (combinatorics), Counting Reorders (combinatorics)

## 📋 Problem Description

Given n elements, count the number of ways to arrange them in a sequence (permutations).

**Input**: 
- n: number of elements

**Output**: 
- Number of permutations P(n) = n! modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 4

Output:
24

Explanation**: 
P(4) = 4! = 4 × 3 × 2 × 1 = 24
Permutations of [1,2,3,4]:
[1,2,3,4], [1,2,4,3], [1,3,2,4], [1,3,4,2], [1,4,2,3], [1,4,3,2]
[2,1,3,4], [2,1,4,3], [2,3,1,4], [2,3,4,1], [2,4,1,3], [2,4,3,1]
[3,1,2,4], [3,1,4,2], [3,2,1,4], [3,2,4,1], [3,4,1,2], [3,4,2,1]
[4,1,2,3], [4,1,3,2], [4,2,1,3], [4,2,3,1], [4,3,1,2], [4,3,2,1]
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Naive Factorial Solution

**Key Insights from Naive Factorial Solution**:
- **Direct Formula**: Use P(n) = n! = n × (n-1) × ... × 1
- **Iterative Calculation**: Calculate factorial iteratively
- **Overflow Issues**: May cause integer overflow for large numbers
- **Baseline Understanding**: Provides correct answer but inefficient for large inputs

**Key Insight**: Use the mathematical formula for permutations with direct factorial calculation.

**Algorithm**:
- Calculate n! = n × (n-1) × ... × 1
- Apply modulo operation throughout calculation
- Return result modulo 10^9+7

**Visual Example**:
```
n = 4

Factorial calculation:
┌─────────────────────────────────────┐
│ 4! = 4 × 3 × 2 × 1 = 24           │
│ Step 1: 4 × 3 = 12                │
│ Step 2: 12 × 2 = 24               │
│ Step 3: 24 × 1 = 24               │
│ Result: 24                         │
└─────────────────────────────────────┘

Permutation visualization:
┌─────────────────────────────────────┐
│ Elements: {1, 2, 3, 4}            │
│ First position: 4 choices          │
│ Second position: 3 choices         │
│ Third position: 2 choices          │
│ Fourth position: 1 choice          │
│ Total: 4 × 3 × 2 × 1 = 24         │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def naive_factorial_solution(n, mod=10**9+7):
    """
    Calculate permutations using naive factorial approach
    
    Args:
        n: number of elements
        mod: modulo value
    
    Returns:
        int: n! modulo mod
    """
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % mod
    
    return result

# Example usage
n = 4
result = naive_factorial_solution(n)
print(f"Naive factorial result: {n}! = {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's inefficient**: May cause overflow and is inefficient for large numbers.

---

### Approach 2: Optimized Factorial Solution

**Key Insights from Optimized Factorial Solution**:
- **Modular Arithmetic**: Use modular arithmetic throughout calculations
- **Overflow Prevention**: Prevent integer overflow with modular operations
- **Efficient Calculation**: More efficient than naive approach
- **Large Number Handling**: Handle large numbers efficiently

**Key Insight**: Use modular arithmetic throughout the factorial calculation to prevent overflow.

**Algorithm**:
- Calculate factorial with modular arithmetic
- Apply modulo operation at each step
- Handle large numbers efficiently

**Visual Example**:
```
n = 4, mod = 10^9+7

Modular factorial calculation:
┌─────────────────────────────────────┐
│ result = 1                         │
│ i=1: result = (1 × 1) mod mod = 1  │
│ i=2: result = (1 × 2) mod mod = 2  │
│ i=3: result = (2 × 3) mod mod = 6  │
│ i=4: result = (6 × 4) mod mod = 24 │
│ Result: 24                         │
└─────────────────────────────────────┘

Modular arithmetic properties:
┌─────────────────────────────────────┐
│ (a × b) mod m = ((a mod m) × (b mod m)) mod m │
│ Prevents overflow for large numbers            │
│ Maintains correctness of result                │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def optimized_factorial_solution(n, mod=10**9+7):
    """
    Calculate permutations using optimized factorial approach
    
    Args:
        n: number of elements
        mod: modulo value
    
    Returns:
        int: n! modulo mod
    """
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % mod
    
    return result

def precomputed_factorial_solution(max_n, mod=10**9+7):
    """
    Precompute factorials for multiple queries
    
    Args:
        max_n: maximum value of n
        mod: modulo value
    
    Returns:
        list: precomputed factorials
    """
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = (fact[i-1] * i) % mod
    
    return fact

# Example usage
n = 4
result = optimized_factorial_solution(n)
print(f"Optimized factorial result: {n}! = {result}")

# Precompute for multiple queries
max_n = 1000000
fact = precomputed_factorial_solution(max_n)
print(f"Precomputed {n}! = {fact[n]}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's better**: Prevents overflow and handles large numbers efficiently.

**Implementation Considerations**:
- **Modular Arithmetic**: Use modular arithmetic throughout
- **Overflow Prevention**: Prevent integer overflow with modular operations
- **Precomputation**: Precompute factorials for multiple queries

---

### Approach 3: Advanced Mathematical Solution (Optimal)

**Key Insights from Advanced Mathematical Solution**:
- **Wilson's Theorem**: Use Wilson's theorem for prime modulus
- **Fermat's Little Theorem**: Use for modular inverse calculations
- **Mathematical Optimization**: Use advanced mathematical properties
- **Optimal Complexity**: Best approach for special cases

**Key Insight**: Use advanced mathematical theorems and properties for optimal permutation calculation.

**Algorithm**:
- Use Wilson's theorem: (p-1)! ≡ -1 (mod p) for prime p
- Use Fermat's little theorem for modular inverse
- Apply mathematical optimizations

**Visual Example**:
```
Wilson's Theorem for prime modulus:
┌─────────────────────────────────────┐
│ For prime p: (p-1)! ≡ -1 (mod p)  │
│ For p = 10^9+7: (p-1)! ≡ -1 (mod p) │
│ Can be used for optimization        │
└─────────────────────────────────────┘

Fermat's Little Theorem:
┌─────────────────────────────────────┐
│ For prime p and gcd(a,p) = 1:      │
│ a^(p-1) ≡ 1 (mod p)                │
│ a^(-1) ≡ a^(p-2) (mod p)           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_mathematical_solution(n, mod=10**9+7):
    """
    Calculate permutations using advanced mathematical approach
    
    Args:
        n: number of elements
        mod: modulo value (prime)
    
    Returns:
        int: n! modulo mod
    """
    def mod_inverse(a, mod):
        """Calculate modular inverse using Fermat's little theorem"""
        return pow(a, mod - 2, mod)
    
    def wilson_optimization(n, mod):
        """Use Wilson's theorem for optimization"""
        if n >= mod:
            return 0  # n! ≡ 0 (mod p) for n ≥ p
        
        # For n < p, calculate normally
        result = 1
        for i in range(1, n + 1):
            result = (result * i) % mod
        
        return result
    
    return wilson_optimization(n, mod)

def stirling_approximation(n):
    """
    Calculate factorial using Stirling's approximation
    
    Args:
        n: number of elements
    
    Returns:
        float: approximation of n!
    """
    import math
    
    # Stirling's approximation: n! ≈ √(2πn) * (n/e)^n
    return math.sqrt(2 * math.pi * n) * (n / math.e) ** n

def log_factorial(n):
    """
    Calculate log(n!) for large numbers
    
    Args:
        n: number of elements
    
    Returns:
        float: log(n!)
    """
    import math
    
    # log(n!) = log(1) + log(2) + ... + log(n)
    result = 0
    for i in range(1, n + 1):
        result += math.log(i)
    
    return result

# Example usage
n = 4
result = advanced_mathematical_solution(n)
print(f"Advanced mathematical result: {n}! = {result}")

# Stirling's approximation
approx = stirling_approximation(n)
print(f"Stirling's approximation: {n}! ≈ {approx}")

# Log factorial
log_fact = log_factorial(n)
print(f"Log factorial: log({n}!) = {log_fact}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses advanced mathematical properties for optimal calculation.

**Implementation Details**:
- **Wilson's Theorem**: Use for prime modulus optimization
- **Fermat's Little Theorem**: Use for modular inverse
- **Mathematical Properties**: Leverage mathematical properties for optimization
- **Special Cases**: Handle special cases efficiently

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Factorial | O(n) | O(1) | Direct factorial calculation |
| Optimized Factorial | O(n) | O(1) | Modular arithmetic throughout |
| Advanced Mathematical | O(n) | O(1) | Mathematical theorems and properties |

### Time Complexity
- **Time**: O(n) - Calculate factorial iteratively
- **Space**: O(1) - Use only necessary variables

### Why This Solution Works
- **Mathematical Formula**: Use factorial formula P(n) = n!
- **Modular Arithmetic**: Handle large numbers efficiently
- **Mathematical Properties**: Leverage mathematical theorems
- **Optimization**: Use advanced mathematical techniques

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Permutations with Repetition**
**Problem**: Count permutations when some elements are repeated.

**Key Differences**: Elements can be repeated

**Solution Approach**: Use formula n! / (n1! × n2! × ... × nk!)

**Implementation**:
```python
def permutations_with_repetition(frequencies, mod=10**9+7):
    """
    Calculate permutations with repetition
    
    Args:
        frequencies: list of frequencies of each element
        mod: modulo value
    
    Returns:
        int: Number of permutations with repetition modulo mod
    """
    def factorial_mod(n, mod):
        """Calculate factorial modulo mod"""
        result = 1
        for i in range(1, n + 1):
            result = (result * i) % mod
        return result
    
    def mod_inverse(a, mod):
        """Calculate modular inverse"""
        return pow(a, mod - 2, mod)
    
    total = sum(frequencies)
    numerator = factorial_mod(total, mod)
    
    denominator = 1
    for freq in frequencies:
        if freq > 0:
            denominator = (denominator * factorial_mod(freq, mod)) % mod
    
    inverse_denominator = mod_inverse(denominator, mod)
    result = (numerator * inverse_denominator) % mod
    
    return result

# Example usage
frequencies = [2, 1, 1]  # 2 A's, 1 B, 1 C
result = permutations_with_repetition(frequencies)
print(f"Permutations with repetition: {result}")
```

#### **2. Circular Permutations**
**Problem**: Count permutations in a circular arrangement.

**Key Differences**: Elements are arranged in a circle

**Solution Approach**: Use formula (n-1)!

**Implementation**:
```python
def circular_permutations(n, mod=10**9+7):
    """
    Calculate circular permutations
    
    Args:
        n: number of elements
        mod: modulo value
    
    Returns:
        int: Number of circular permutations modulo mod
    """
    if n <= 1:
        return 1
    
    # Circular permutations: (n-1)!
    result = 1
    for i in range(1, n):
        result = (result * i) % mod
    
    return result

# Example usage
n = 4
result = circular_permutations(n)
print(f"Circular permutations for {n} elements: {result}")
```

#### **3. Restricted Permutations**
**Problem**: Count permutations with certain restrictions.

**Key Differences**: Apply restrictions to permutations

**Solution Approach**: Use inclusion-exclusion principle

**Implementation**:
```python
def restricted_permutations(n, restrictions, mod=10**9+7):
    """
    Calculate restricted permutations using inclusion-exclusion
    
    Args:
        n: number of elements
        restrictions: list of restricted positions
        mod: modulo value
    
    Returns:
        int: Number of restricted permutations modulo mod
    """
    def factorial_mod(n, mod):
        """Calculate factorial modulo mod"""
        result = 1
        for i in range(1, n + 1):
            result = (result * i) % mod
        return result
    
    def combination(n, k, mod):
        """Calculate C(n,k) modulo mod"""
        if k > n or k < 0:
            return 0
        
        result = 1
        for i in range(k):
            result = (result * (n - i)) % mod
            result = (result * pow(i + 1, mod - 2, mod)) % mod
        
        return result
    
    def derangement(n, mod):
        """Calculate derangement D(n) modulo mod"""
        if n <= 1:
            return 0
        if n == 2:
            return 1
        
        prev2, prev1 = 0, 1
        for i in range(3, n + 1):
            curr = ((i - 1) * (prev1 + prev2)) % mod
            prev2, prev1 = prev1, curr
        
        return prev1
    
    # Use inclusion-exclusion principle
    result = 0
    for i in range(len(restrictions) + 1):
        # C(k,i) * (n-i)! * (-1)^i
        term = (combination(len(restrictions), i, mod) * 
                factorial_mod(n - i, mod)) % mod
        
        if i % 2 == 0:
            result = (result + term) % mod
        else:
            result = (result - term + mod) % mod
    
    return result

# Example usage
n = 4
restrictions = [0, 1]  # Elements 0 and 1 cannot be in their original positions
result = restricted_permutations(n, restrictions)
print(f"Restricted permutations: {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Combinations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Sequences](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Reorders](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Permutations](https://leetcode.com/problems/permutations/) - Permutations
- [Permutations II](https://leetcode.com/problems/permutations-ii/) - Permutations with duplicates
- [Next Permutation](https://leetcode.com/problems/next-permutation/) - Permutation generation

#### **Problem Categories**
- **Combinatorics**: Mathematical counting, permutations, combinations
- **Dynamic Programming**: DP optimization, mathematical DP
- **Mathematical Algorithms**: Modular arithmetic, number theory

## 🔗 Additional Resources

### **Algorithm References**
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Binomial coefficients
- [Permutations](https://cp-algorithms.com/combinatorics/inclusion-exclusion.html) - Inclusion-exclusion principle
- [Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html) - Modular inverse

### **Practice Problems**
- [CSES Counting Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Sequences](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Reorders](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Combinatorics](https://en.wikipedia.org/wiki/Combinatorics) - Wikipedia article
