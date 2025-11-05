---
layout: simple
title: "Counting Reorders - Combinatorial Problem"
permalink: /problem_soulutions/counting_problems/counting_reorders_analysis
---

# Counting Reorders - Combinatorial Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of reordering elements in combinatorics
- Apply mathematical formulas for counting reorderings
- Implement efficient algorithms for reorder counting
- Optimize reorder calculations for large numbers
- Handle special cases in reorder counting

## 📋 Problem Description

Given an array of n elements, count the number of ways to reorder the elements such that no element appears in its original position (derangements).

**Input**: 
- n: number of elements

**Output**: 
- Number of derangements D(n) modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 4

Output:
9

Explanation**: 
D(4) = 9
Derangements of [1,2,3,4]:
[2,1,4,3], [2,3,4,1], [2,4,1,3]
[3,1,4,2], [3,4,1,2], [3,4,2,1]
[4,1,2,3], [4,3,1,2], [4,3,2,1]
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution

**Key Insights from Recursive Solution**:
- **Recursive Formula**: Use D(n) = (n-1) * (D(n-1) + D(n-2))
- **Base Cases**: D(1) = 0, D(2) = 1
- **Overlapping Subproblems**: Same subproblems calculated multiple times
- **Baseline Understanding**: Provides correct answer but inefficient

**Key Insight**: Use recursive formula for derangements with base cases.

**Algorithm**:
- Use recursive formula: D(n) = (n-1) * (D(n-1) + D(n-2))
- Handle base cases: D(1) = 0, D(2) = 1
- Apply modulo operation

**Visual Example**:
```
Derangement formula:
┌─────────────────────────────────────┐
│ D(n) = (n-1) × (D(n-1) + D(n-2))  │
│ D(1) = 0                           │
│ D(2) = 1                           │
│ D(3) = 2 × (1 + 0) = 2             │
│ D(4) = 3 × (2 + 1) = 9             │
└─────────────────────────────────────┘

Recursive calculation:
┌─────────────────────────────────────┐
│ D(4) = 3 × (D(3) + D(2))          │
│ D(3) = 2 × (D(2) + D(1)) = 2 × (1 + 0) = 2 │
│ D(2) = 1                           │
│ D(4) = 3 × (2 + 1) = 9             │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_reorder_solution(n, mod=10**9+7):
    """
    Calculate derangements using recursive approach
    
    Args:
        n: number of elements
        mod: modulo value
    
    Returns:
        int: D(n) modulo mod
    """
    def derangement(n):
        """Calculate derangement recursively"""
        if n == 1:
            return 0
        if n == 2:
            return 1
        
        # D(n) = (n-1) * (D(n-1) + D(n-2))
        return ((n - 1) * (derangement(n - 1) + derangement(n - 2))) % mod
    
    return derangement(n)

# Example usage
n = 4
result = recursive_reorder_solution(n)
print(f"Recursive reorder result: D({n}) = {result}")
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to overlapping subproblems.

---

### Approach 2: Memoized Recursive Solution

**Key Insights from Memoized Recursive Solution**:
- **Memoization**: Store previously calculated values
- **Overlapping Subproblems**: Avoid recalculating same subproblems
- **Time Optimization**: Reduce time complexity to O(n)
- **Space Trade-off**: Use O(n) space for memoization

**Key Insight**: Use memoization to store previously calculated derangement values.

**Algorithm**:
- Use memoization to store calculated values
- Check memoization table before calculating
- Store results in memoization table

**Visual Example**:
```
Memoized calculation:
┌─────────────────────────────────────┐
│ memo = {1: 0, 2: 1}                │
│ D(3) = 2 × (D(2) + D(1))          │
│ D(2) = 1 (from memo)               │
│ D(1) = 0 (from memo)               │
│ D(3) = 2 × (1 + 0) = 2             │
│ memo[3] = 2                        │
│ D(4) = 3 × (D(3) + D(2))          │
│ D(3) = 2 (from memo)               │
│ D(2) = 1 (from memo)               │
│ D(4) = 3 × (2 + 1) = 9             │
│ memo[4] = 9                        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def memoized_reorder_solution(n, mod=10**9+7):
    """
    Calculate derangements using memoized recursive approach
    
    Args:
        n: number of elements
        mod: modulo value
    
    Returns:
        int: D(n) modulo mod
    """
    memo = {1: 0, 2: 1}
    
    def derangement(n):
        """Calculate derangement with memoization"""
        if n in memo:
            return memo[n]
        
        # D(n) = (n-1) * (D(n-1) + D(n-2))
        result = ((n - 1) * (derangement(n - 1) + derangement(n - 2))) % mod
        memo[n] = result
        return result
    
    return derangement(n)

# Example usage
n = 4
result = memoized_reorder_solution(n)
print(f"Memoized reorder result: D({n}) = {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Eliminates overlapping subproblems and reduces time complexity.

**Implementation Considerations**:
- **Memoization**: Store calculated values to avoid recalculation
- **Base Cases**: Handle base cases properly
- **Modular Arithmetic**: Apply modulo operations throughout

---

### Approach 3: Dynamic Programming Solution (Optimal)

**Key Insights from Dynamic Programming Solution**:
- **Bottom-up Approach**: Build solution from base cases
- **Space Optimization**: Use only necessary variables
- **Efficient Calculation**: O(n) time with O(1) space
- **Optimal Complexity**: Best approach for single query

**Key Insight**: Use dynamic programming with space optimization for efficient derangement calculation.

**Algorithm**:
- Use bottom-up approach starting from base cases
- Maintain only last two values for space optimization
- Apply modular arithmetic throughout

**Visual Example**:
```
DP calculation with space optimization:
┌─────────────────────────────────────┐
│ prev2 = D(1) = 0                   │
│ prev1 = D(2) = 1                   │
│ for i in range(3, n+1):            │
│   curr = (i-1) × (prev1 + prev2)   │
│   prev2 = prev1                     │
│   prev1 = curr                      │
│ return prev1                        │
└─────────────────────────────────────┘

Step-by-step calculation:
┌─────────────────────────────────────┐
│ i=3: curr = 2 × (1 + 0) = 2        │
│       prev2 = 1, prev1 = 2         │
│ i=4: curr = 3 × (2 + 1) = 9        │
│       prev2 = 2, prev1 = 9         │
│ Result: 9                           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_reorder_solution(n, mod=10**9+7):
    """
    Calculate derangements using dynamic programming approach
    
    Args:
        n: number of elements
        mod: modulo value
    
    Returns:
        int: D(n) modulo mod
    """
    if n == 1:
        return 0
    if n == 2:
        return 1
    
    # Base cases
    prev2 = 0  # D(1)
    prev1 = 1  # D(2)
    
    # Calculate D(i) for i from 3 to n
    for i in range(3, n + 1):
        # D(i) = (i-1) * (D(i-1) + D(i-2))
        curr = ((i - 1) * (prev1 + prev2)) % mod
        prev2 = prev1
        prev1 = curr
    
    return prev1

def optimized_dp_reorder_solution(n, mod=10**9+7):
    """
    Calculate derangements using optimized DP approach
    
    Args:
        n: number of elements
        mod: modulo value
    
    Returns:
        int: D(n) modulo mod
    """
    if n <= 1:
        return 0
    if n == 2:
        return 1
    
    # Use array for multiple queries
    dp = [0] * (n + 1)
    dp[1] = 0
    dp[2] = 1
    
    for i in range(3, n + 1):
        dp[i] = ((i - 1) * (dp[i - 1] + dp[i - 2])) % mod
    
    return dp[n]

# Example usage
n = 4
result1 = dp_reorder_solution(n)
result2 = optimized_dp_reorder_solution(n)
print(f"DP reorder result: D({n}) = {result1}")
print(f"Optimized DP reorder result: D({n}) = {result2}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1) (space-optimized version)

**Why it's optimal**: O(n) time complexity with optimal space usage.

**Implementation Details**:
- **Bottom-up Approach**: Build solution from base cases
- **Space Optimization**: Use only necessary variables
- **Modular Arithmetic**: Apply modulo operations throughout
- **Single Query**: Efficient for single derangement calculation

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^n) | O(n) | Recursive formula with base cases |
| Memoized | O(n) | O(n) | Memoization to avoid overlapping subproblems |
| Dynamic Programming | O(n) | O(1) | Bottom-up approach with space optimization |

### Time Complexity
- **Time**: O(n) - Calculate each derangement once
- **Space**: O(1) - Use only necessary variables

### Why This Solution Works
- **Mathematical Formula**: Use derangement formula D(n) = (n-1) * (D(n-1) + D(n-2))
- **Dynamic Programming**: Build solution from base cases
- **Space Optimization**: Use only necessary variables
- **Modular Arithmetic**: Handle large numbers efficiently

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Partial Derangements**
**Problem**: Count derangements where exactly k elements are in their original positions.

**Key Differences**: Allow some elements to be in original positions

**Solution Approach**: Use inclusion-exclusion principle

**Implementation**:
```python
def partial_derangements(n, k, mod=10**9+7):
    """
    Calculate partial derangements where exactly k elements are in original positions
    
    Args:
        n: number of elements
        k: number of elements in original positions
        mod: modulo value
    
    Returns:
        int: Number of partial derangements modulo mod
    """
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
    for i in range(k, n + 1):
        # C(n,i) * D(n-i)
        term = (combination(n, i, mod) * derangement(n - i, mod)) % mod
        if (i - k) % 2 == 0:
            result = (result + term) % mod
        else:
            result = (result - term + mod) % mod
    
    return result

# Example usage
n, k = 5, 2  # Exactly 2 elements in original positions
result = partial_derangements(n, k)
print(f"Partial derangements with {k} fixed: {result}")
```

#### **2. Circular Derangements**
**Problem**: Count derangements in a circular arrangement.

**Key Differences**: Elements are arranged in a circle

**Solution Approach**: Use circular derangement formula

**Implementation**:
```python
def circular_derangements(n, mod=10**9+7):
    """
    Calculate circular derangements
    
    Args:
        n: number of elements
        mod: modulo value
    
    Returns:
        int: Number of circular derangements modulo mod
    """
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
    
    # Circular derangement formula: D_c(n) = D(n) + D(n-1)
    if n <= 1:
        return 0
    if n == 2:
        return 1
    
    d_n = derangement(n, mod)
    d_n_minus_1 = derangement(n - 1, mod)
    
    return (d_n + d_n_minus_1) % mod

# Example usage
n = 4
result = circular_derangements(n)
print(f"Circular derangements for {n} elements: {result}")
```

#### **3. Weighted Derangements**
**Problem**: Count derangements with weights for each position.

**Key Differences**: Each position has a weight

**Solution Approach**: Use weighted derangement formula

**Implementation**:
```python
def weighted_derangements(weights, mod=10**9+7):
    """
    Calculate weighted derangements
    
    Args:
        weights: list of weights for each position
        mod: modulo value
    
    Returns:
        int: Number of weighted derangements modulo mod
    """
    n = len(weights)
    
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
    
    # Calculate weighted derangement
    # D_w(n) = sum of weights * D(n)
    total_weight = sum(weights) % mod
    d_n = derangement(n, mod)
    
    return (total_weight * d_n) % mod

# Example usage
weights = [1, 2, 3, 4]  # Weights for each position
result = weighted_derangements(weights)
print(f"Weighted derangements: {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Permutations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Combinations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Sequences](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Permutations](https://leetcode.com/problems/permutations/) - Permutations
- [Permutations II](https://leetcode.com/problems/permutations-ii/) - Permutations with duplicates
- [Next Permutation](https://leetcode.com/problems/next-permutation/) - Permutation generation

#### **Problem Categories**
- **Combinatorics**: Mathematical counting, derangements, permutations
- **Dynamic Programming**: DP optimization, mathematical DP
- **Mathematical Algorithms**: Modular arithmetic, number theory

## 🔗 Additional Resources

### **Algorithm References**
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Binomial coefficients
- [Derangements](https://cp-algorithms.com/combinatorics/inclusion-exclusion.html) - Inclusion-exclusion principle
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP introduction

### **Practice Problems**
- [CSES Counting Permutations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Sequences](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Combinatorics](https://en.wikipedia.org/wiki/Combinatorics) - Wikipedia article
