---
layout: simple
title: "Counting Combinations - Combinatorial Problem"
permalink: /problem_soulutions/counting_problems/counting_combinations_analysis
---

# Counting Combinations - Combinatorial Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of combinations in combinatorics
- Apply mathematical formulas for counting combinations
- Implement efficient algorithms for combination counting
- Optimize combination calculations for large numbers
- Handle special cases in combination counting

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Combinatorics, mathematical formulas, modular arithmetic
- **Data Structures**: Arrays, mathematical computations, factorial calculations
- **Mathematical Concepts**: Combinations, permutations, binomial coefficients, modular arithmetic
- **Programming Skills**: Mathematical computations, modular arithmetic, large number handling
- **Related Problems**: Counting Permutations (combinatorics), Counting Sequences (combinatorics), Counting Reorders (combinatorics)

## 📋 Problem Description

Given n and k, count the number of ways to choose k elements from n elements (combinations).

**Input**: 
- n: total number of elements
- k: number of elements to choose

**Output**: 
- Number of combinations C(n,k) modulo 10^9+7

**Constraints**:
- 1 ≤ k ≤ n ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 5, k = 3

Output:
10

Explanation**: 
C(5,3) = 5! / (3! * (5-3)!) = 120 / (6 * 2) = 10
Ways to choose 3 elements from 5: {1,2,3}, {1,2,4}, {1,2,5}, {1,3,4}, {1,3,5}, {1,4,5}, {2,3,4}, {2,3,5}, {2,4,5}, {3,4,5}
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Naive Factorial Solution

**Key Insights from Naive Factorial Solution**:
- **Direct Formula**: Use C(n,k) = n! / (k! * (n-k)!)
- **Factorial Calculation**: Calculate factorials directly
- **Overflow Issues**: May cause integer overflow for large numbers
- **Baseline Understanding**: Provides correct answer but inefficient for large inputs

**Key Insight**: Use the mathematical formula for combinations with direct factorial calculation.

**Algorithm**:
- Calculate n!, k!, and (n-k)!
- Compute C(n,k) = n! / (k! * (n-k)!)
- Apply modulo operation

**Visual Example**:
```
n = 5, k = 3

Factorial calculations:
┌─────────────────────────────────────┐
│ 5! = 5 × 4 × 3 × 2 × 1 = 120      │
│ 3! = 3 × 2 × 1 = 6                │
│ (5-3)! = 2! = 2 × 1 = 2           │
│ C(5,3) = 120 / (6 × 2) = 10       │
└─────────────────────────────────────┘

Combination visualization:
┌─────────────────────────────────────┐
│ Elements: {1, 2, 3, 4, 5}         │
│ Choose 3:                          │
│ {1,2,3}, {1,2,4}, {1,2,5}         │
│ {1,3,4}, {1,3,5}, {1,4,5}         │
│ {2,3,4}, {2,3,5}, {2,4,5}         │
│ {3,4,5}                            │
│ Total: 10 combinations             │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def naive_factorial_solution(n, k, mod=10**9+7):
    """
    Calculate combinations using naive factorial approach
    
    Args:
        n: total number of elements
        k: number of elements to choose
        mod: modulo value
    
    Returns:
        int: C(n,k) modulo mod
    """
    def factorial(x):
        """Calculate factorial of x"""
        result = 1
        for i in range(1, x + 1):
            result = (result * i) % mod
        return result
    
    # Calculate factorials
    n_fact = factorial(n)
    k_fact = factorial(k)
    n_k_fact = factorial(n - k)
    
    # Calculate combination using formula
    # C(n,k) = n! / (k! * (n-k)!)
    denominator = (k_fact * n_k_fact) % mod
    
    # Use modular inverse for division
    def mod_inverse(a, mod):
        """Calculate modular inverse using Fermat's little theorem"""
        return pow(a, mod - 2, mod)
    
    inverse_denominator = mod_inverse(denominator, mod)
    result = (n_fact * inverse_denominator) % mod
    
    return result

# Example usage
n, k = 5, 3
result = naive_factorial_solution(n, k)
print(f"Naive factorial result: C({n},{k}) = {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's inefficient**: May cause overflow and is inefficient for large numbers.

---

### Approach 2: Optimized Factorial Solution

**Key Insights from Optimized Factorial Solution**:
- **Modular Arithmetic**: Use modular arithmetic throughout calculations
- **Modular Inverse**: Use Fermat's little theorem for modular inverse
- **Overflow Prevention**: Prevent integer overflow with modular operations
- **Optimization**: More efficient than naive approach

**Key Insight**: Use modular arithmetic and modular inverse to prevent overflow and handle large numbers.

**Algorithm**:
- Calculate factorials with modular arithmetic
- Use modular inverse for division
- Apply modulo operations throughout

**Visual Example**:
```
n = 5, k = 3, mod = 10^9+7

Modular factorial calculations:
┌─────────────────────────────────────┐
│ 5! mod mod = 120 mod mod = 120     │
│ 3! mod mod = 6 mod mod = 6         │
│ 2! mod mod = 2 mod mod = 2         │
│ denominator = (6 × 2) mod mod = 12 │
│ inverse = 12^(mod-2) mod mod       │
│ result = (120 × inverse) mod mod   │
└─────────────────────────────────────┘

Modular arithmetic properties:
┌─────────────────────────────────────┐
│ (a × b) mod m = ((a mod m) × (b mod m)) mod m │
│ a^(-1) mod m = a^(m-2) mod m (if m is prime)  │
│ (a / b) mod m = (a × b^(-1)) mod m            │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def optimized_factorial_solution(n, k, mod=10**9+7):
    """
    Calculate combinations using optimized factorial approach
    
    Args:
        n: total number of elements
        k: number of elements to choose
        mod: modulo value
    
    Returns:
        int: C(n,k) modulo mod
    """
    def factorial_mod(x, mod):
        """Calculate factorial of x modulo mod"""
        result = 1
        for i in range(1, x + 1):
            result = (result * i) % mod
        return result
    
    def mod_inverse(a, mod):
        """Calculate modular inverse using Fermat's little theorem"""
        return pow(a, mod - 2, mod)
    
    # Calculate factorials with modular arithmetic
    n_fact = factorial_mod(n, mod)
    k_fact = factorial_mod(k, mod)
    n_k_fact = factorial_mod(n - k, mod)
    
    # Calculate denominator
    denominator = (k_fact * n_k_fact) % mod
    
    # Use modular inverse for division
    inverse_denominator = mod_inverse(denominator, mod)
    result = (n_fact * inverse_denominator) % mod
    
    return result

# Example usage
n, k = 5, 3
result = optimized_factorial_solution(n, k)
print(f"Optimized factorial result: C({n},{k}) = {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's better**: Prevents overflow and handles large numbers efficiently.

**Implementation Considerations**:
- **Modular Arithmetic**: Use modular arithmetic throughout
- **Modular Inverse**: Use Fermat's little theorem for modular inverse
- **Overflow Prevention**: Prevent integer overflow with modular operations

---

### Approach 3: Dynamic Programming Solution (Optimal)

**Key Insights from Dynamic Programming Solution**:
- **Pascal's Triangle**: Use Pascal's triangle property C(n,k) = C(n-1,k-1) + C(n-1,k)
- **Memoization**: Store previously calculated values
- **Efficient Calculation**: O(n*k) time complexity
- **Optimal Complexity**: Best approach for multiple queries

**Key Insight**: Use Pascal's triangle property and dynamic programming for efficient combination calculation.

**Algorithm**:
- Use Pascal's triangle: C(n,k) = C(n-1,k-1) + C(n-1,k)
- Build combination table using dynamic programming
- Apply modular arithmetic throughout

**Visual Example**:
```
Pascal's Triangle for combinations:
┌─────────────────────────────────────┐
│ n\k  0  1  2  3  4  5              │
│ 0    1  0  0  0  0  0              │
│ 1    1  1  0  0  0  0              │
│ 2    1  2  1  0  0  0              │
│ 3    1  3  3  1  0  0              │
│ 4    1  4  6  4  1  0              │
│ 5    1  5 10 10  5  1              │
└─────────────────────────────────────┘

DP calculation for C(5,3):
┌─────────────────────────────────────┐
│ C(5,3) = C(4,2) + C(4,3)          │
│ C(4,2) = C(3,1) + C(3,2) = 3 + 3 = 6 │
│ C(4,3) = C(3,2) + C(3,3) = 3 + 1 = 4 │
│ C(5,3) = 6 + 4 = 10                │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_combination_solution(n, k, mod=10**9+7):
    """
    Calculate combinations using dynamic programming approach
    
    Args:
        n: total number of elements
        k: number of elements to choose
        mod: modulo value
    
    Returns:
        int: C(n,k) modulo mod
    """
    # Initialize DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        dp[i][0] = 1  # C(n,0) = 1
    
    # Fill DP table using Pascal's triangle property
    for i in range(1, n + 1):
        for j in range(1, min(i + 1, k + 1)):
            # C(n,k) = C(n-1,k-1) + C(n-1,k)
            dp[i][j] = (dp[i-1][j-1] + dp[i-1][j]) % mod
    
    return dp[n][k]

def optimized_dp_combination_solution(n, k, mod=10**9+7):
    """
    Calculate combinations using space-optimized DP approach
    
    Args:
        n: total number of elements
        k: number of elements to choose
        mod: modulo value
    
    Returns:
        int: C(n,k) modulo mod
    """
    # Optimize space by using only one row
    if k > n - k:
        k = n - k  # C(n,k) = C(n,n-k)
    
    # Initialize current row
    prev = [0] * (k + 1)
    prev[0] = 1
    
    # Fill DP table row by row
    for i in range(1, n + 1):
        curr = [0] * (k + 1)
        curr[0] = 1
        
        for j in range(1, min(i + 1, k + 1)):
            # C(n,k) = C(n-1,k-1) + C(n-1,k)
            curr[j] = (prev[j-1] + prev[j]) % mod
        
        prev = curr
    
    return prev[k]

# Example usage
n, k = 5, 3
result1 = dp_combination_solution(n, k)
result2 = optimized_dp_combination_solution(n, k)
print(f"DP result: C({n},{k}) = {result1}")
print(f"Optimized DP result: C({n},{k}) = {result2}")
```

**Time Complexity**: O(n*k)
**Space Complexity**: O(k) (optimized version)

**Why it's optimal**: Efficient for multiple queries and handles large numbers well.

**Implementation Details**:
- **Pascal's Triangle**: Use Pascal's triangle property for efficient calculation
- **Space Optimization**: Use only one row for space optimization
- **Modular Arithmetic**: Apply modular arithmetic throughout
- **Multiple Queries**: Efficient for multiple combination calculations

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive Factorial | O(n) | O(1) | Direct formula with factorial calculation |
| Optimized Factorial | O(n) | O(1) | Modular arithmetic with modular inverse |
| Dynamic Programming | O(n*k) | O(k) | Pascal's triangle with DP |

### Time Complexity
- **Time**: O(n*k) - Fill DP table
- **Space**: O(k) - Store one row of DP table

### Why This Solution Works
- **Mathematical Properties**: Use Pascal's triangle property
- **Dynamic Programming**: Store previously calculated values
- **Modular Arithmetic**: Handle large numbers efficiently
- **Space Optimization**: Use only necessary space

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Multiple Combination Queries**
**Problem**: Answer multiple combination queries efficiently.

**Key Differences**: Handle multiple queries with different n and k values

**Solution Approach**: Use precomputed factorial and inverse arrays

**Implementation**:
```python
class CombinationCalculator:
    def __init__(self, max_n, mod=10**9+7):
        self.mod = mod
        self.max_n = max_n
        
        # Precompute factorials
        self.fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            self.fact[i] = (self.fact[i-1] * i) % mod
        
        # Precompute modular inverses
        self.inv_fact = [1] * (max_n + 1)
        self.inv_fact[max_n] = pow(self.fact[max_n], mod - 2, mod)
        for i in range(max_n - 1, -1, -1):
            self.inv_fact[i] = (self.inv_fact[i + 1] * (i + 1)) % mod
    
    def combination(self, n, k):
        """Calculate C(n,k) using precomputed values"""
        if k > n or k < 0:
            return 0
        
        # C(n,k) = n! / (k! * (n-k)!)
        numerator = self.fact[n]
        denominator = (self.inv_fact[k] * self.inv_fact[n - k]) % self.mod
        
        return (numerator * denominator) % self.mod

# Example usage
calc = CombinationCalculator(1000000)
queries = [(5, 3), (10, 5), (100, 50)]
for n, k in queries:
    result = calc.combination(n, k)
    print(f"C({n},{k}) = {result}")
```

#### **2. Combination with Repetition**
**Problem**: Count combinations with repetition allowed.

**Key Differences**: Elements can be chosen multiple times

**Solution Approach**: Use formula C(n+k-1, k) for combinations with repetition

**Implementation**:
```python
def combination_with_repetition(n, k, mod=10**9+7):
    """
    Calculate combinations with repetition
    
    Args:
        n: number of distinct elements
        k: number of elements to choose (with repetition)
        mod: modulo value
    
    Returns:
        int: C(n+k-1, k) modulo mod
    """
    # C(n+k-1, k) = (n+k-1)! / (k! * (n-1)!)
    def factorial_mod(x, mod):
        result = 1
        for i in range(1, x + 1):
            result = (result * i) % mod
        return result
    
    def mod_inverse(a, mod):
        return pow(a, mod - 2, mod)
    
    numerator = factorial_mod(n + k - 1, mod)
    denominator = (factorial_mod(k, mod) * factorial_mod(n - 1, mod)) % mod
    
    inverse_denominator = mod_inverse(denominator, mod)
    result = (numerator * inverse_denominator) % mod
    
    return result

# Example usage
n, k = 3, 4  # Choose 4 elements from 3 types with repetition
result = combination_with_repetition(n, k)
print(f"Combinations with repetition C({n}+{k}-1,{k}) = {result}")
```

#### **3. Large Combination Calculation**
**Problem**: Calculate combinations for very large numbers.

**Key Differences**: Handle extremely large n and k values

**Solution Approach**: Use Lucas theorem for large numbers

**Implementation**:
```python
def lucas_combination(n, k, mod=10**9+7):
    """
    Calculate combinations using Lucas theorem for large numbers
    
    Args:
        n: total number of elements
        k: number of elements to choose
        mod: modulo value
    
    Returns:
        int: C(n,k) modulo mod
    """
    def small_combination(n, k, mod):
        """Calculate combination for small numbers"""
        if k > n or k < 0:
            return 0
        
        result = 1
        for i in range(k):
            result = (result * (n - i)) % mod
            result = (result * pow(i + 1, mod - 2, mod)) % mod
        
        return result
    
    def lucas_theorem(n, k, mod):
        """Apply Lucas theorem recursively"""
        if k == 0:
            return 1
        if k > n:
            return 0
        
        # Get digits in base mod
        n_digits = []
        k_digits = []
        
        temp_n, temp_k = n, k
        while temp_n > 0 or temp_k > 0:
            n_digits.append(temp_n % mod)
            k_digits.append(temp_k % mod)
            temp_n //= mod
            temp_k //= mod
        
        # Pad with zeros if necessary
        max_len = max(len(n_digits), len(k_digits))
        n_digits.extend([0] * (max_len - len(n_digits)))
        k_digits.extend([0] * (max_len - len(k_digits)))
        
        # Apply Lucas theorem
        result = 1
        for i in range(max_len):
            result = (result * small_combination(n_digits[i], k_digits[i], mod)) % mod
        
        return result
    
    return lucas_theorem(n, k, mod)

# Example usage
n, k = 1000000, 500000
result = lucas_combination(n, k)
print(f"Large combination C({n},{k}) = {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Permutations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Sequences](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Reorders](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Combinations
- [Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/) - Combinations
- [Combination Sum](https://leetcode.com/problems/combination-sum/) - Combinations

#### **Problem Categories**
- **Combinatorics**: Mathematical counting, combinations, permutations
- **Dynamic Programming**: DP optimization, mathematical DP
- **Mathematical Algorithms**: Modular arithmetic, number theory

## 🔗 Additional Resources

### **Algorithm References**
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Binomial coefficients
- [Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html) - Modular inverse
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP introduction

### **Practice Problems**
- [CSES Counting Permutations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Sequences](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Reorders](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Combinatorics](https://en.wikipedia.org/wiki/Combinatorics) - Wikipedia article
