---
layout: simple
title: "Counting Reorders"
permalink: /problem_soulutions/counting_problems/counting_reorders_analysis
---


# Counting Reorders

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

*This analysis shows how to efficiently count reorderings using dynamic programming with state compression and memoization.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Reorderings**
**Problem**: Each element has a weight. Find reorderings with total weight equal to target.
```python
def weighted_reorderings(n, target, weights, MOD=10**9+7):
    # weights[i] = weight of element i
    dp = [[0] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(target + 1):
            # Don't include element i
            dp[i][j] = dp[i-1][j]
            
            # Include element i if weight allows
            if j >= weights[i-1]:
                dp[i][j] = (dp[i][j] + dp[i-1][j - weights[i-1]] * i) % MOD
    
    return dp[n][target]
```

#### **Variation 2: Constrained Reorderings**
**Problem**: Find reorderings with constraints on element positions.
```python
def constrained_reorderings(n, constraints, MOD=10**9+7):
    # constraints[i] = set of allowed positions for element i
    dp = [[0] * (1 << n) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for mask in range(1 << n):
            for pos in range(n):
                if (mask >> pos) & 1 and pos in constraints[i-1]:
                    prev_mask = mask ^ (1 << pos)
                    dp[i][mask] = (dp[i][mask] + dp[i-1][prev_mask]) % MOD
    
    return dp[n][(1 << n) - 1]
```

#### **Variation 3: Circular Reorderings**
**Problem**: Count reorderings in a circular arrangement.
```python
def circular_reorderings(n, MOD=10**9+7):
    # Count circular reorderings of n elements
    if n <= 1:
        return 1
    
    # For circular reorderings, we fix one element and reorder the rest
    # Result is (n-1)!
    result = 1
    for i in range(1, n):
        result = (result * i) % MOD
    
    return result
```

#### **Variation 4: Partial Reorderings**
**Problem**: Count reorderings where only k elements are reordered.
```python
def partial_reorderings(n, k, MOD=10**9+7):
    # Count reorderings where only k elements are reordered
    if k > n:
        return 0
    
    # Use formula: C(n,k) * k!
    combination = 1
    for i in range(k):
        combination = (combination * (n - i)) % MOD
        combination = (combination * pow(i + 1, MOD-2, MOD)) % MOD
    
    factorial = 1
    for i in range(1, k + 1):
        factorial = (factorial * i) % MOD
    
    return (combination * factorial) % MOD
```

#### **Variation 5: Dynamic Reordering Updates**
**Problem**: Support dynamic updates to constraints and answer reordering queries efficiently.
```python
class DynamicReorderingCounter:
    def __init__(self, n, MOD=10**9+7):
        self.n = n
        self.MOD = MOD
        self.constraints = [set(range(n)) for _ in range(n)]  # Default: all positions allowed
        self.factorial = [1] * (n + 1)
        
        # Precompute factorials
        for i in range(1, n + 1):
            self.factorial[i] = (self.factorial[i-1] * i) % MOD
    
    def update_constraint(self, element, allowed_positions):
        self.constraints[element] = set(allowed_positions)
    
    def count_reorderings(self):
        # Use dynamic programming with current constraints
        dp = [[0] * (1 << self.n) for _ in range(self.n + 1)]
        dp[0][0] = 1
        
        for i in range(1, self.n + 1):
            for mask in range(1 << self.n):
                for pos in range(self.n):
                    if (mask >> pos) & 1 and pos in self.constraints[i-1]:
                        prev_mask = mask ^ (1 << pos)
                        dp[i][mask] = (dp[i][mask] + dp[i-1][prev_mask]) % self.MOD
        
        return dp[self.n][(1 << self.n) - 1]
```

### 🔗 **Related Problems & Concepts**

#### **1. Reordering Problems**
- **Reordering Counting**: Count reorderings efficiently
- **Reordering Generation**: Generate reorderings
- **Reordering Optimization**: Optimize reordering algorithms
- **Reordering Analysis**: Analyze reordering properties

#### **2. Dynamic Programming Problems**
- **DP Optimization**: Optimize dynamic programming
- **DP State Management**: Manage DP states efficiently
- **DP Transitions**: Design DP transitions
- **DP Analysis**: Analyze DP algorithms

#### **3. Modular Arithmetic Problems**
- **Modular Operations**: Perform modular operations
- **Modular Inverses**: Compute modular inverses
- **Modular Optimization**: Optimize modular arithmetic
- **Modular Analysis**: Analyze modular properties

#### **4. Constraint Problems**
- **Constraint Satisfaction**: Satisfy constraints efficiently
- **Constraint Optimization**: Optimize constraint algorithms
- **Constraint Analysis**: Analyze constraint properties
- **Constraint Relaxation**: Relax constraints when needed

#### **5. Counting Problems**
- **Counting Algorithms**: Efficient counting algorithms
- **Counting Optimization**: Optimize counting operations
- **Counting Analysis**: Analyze counting properties
- **Counting Techniques**: Various counting techniques

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    
    result = count_reorders(n)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute reorderings for different ranges
def precompute_reorderings(max_n, MOD=10**9+7):
    factorial = [1] * (max_n + 1)
    
    for i in range(1, max_n + 1):
        factorial[i] = (factorial[i-1] * i) % MOD
    
    return factorial

# Answer range queries efficiently
def range_query(factorial, n):
    return factorial[n]
```

#### **3. Interactive Problems**
```python
# Interactive reordering calculator
def interactive_reordering_calculator():
    MOD = 10**9 + 7
    
    while True:
        query = input("Enter query (reorderings/weighted/constrained/circular/partial/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "reorderings":
            n = int(input("Enter n: "))
            result = count_reorders(n)
            print(f"R({n}) = {result}")
        elif query == "weighted":
            n = int(input("Enter n: "))
            target = int(input("Enter target weight: "))
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_reorderings(n, target, weights)
            print(f"Weighted reorderings: {result}")
        elif query == "constrained":
            n = int(input("Enter n: "))
            constraints = []
            print("Enter constraints for each element:")
            for i in range(n):
                positions = list(map(int, input(f"Element {i}: ").split()))
                constraints.append(set(positions))
            result = constrained_reorderings(n, constraints)
            print(f"Constrained reorderings: {result}")
        elif query == "circular":
            n = int(input("Enter n: "))
            result = circular_reorderings(n)
            print(f"Circular reorderings: {result}")
        elif query == "partial":
            n, k = map(int, input("Enter n and k: ").split())
            result = partial_reorderings(n, k)
            print(f"Partial reorderings: {result}")
        elif query == "dynamic":
            n = int(input("Enter n: "))
            counter = DynamicReorderingCounter(n)
            
            while True:
                cmd = input("Enter command (update/count/back): ")
                if cmd == "back":
                    break
                elif cmd == "update":
                    element = int(input("Enter element: "))
                    positions = list(map(int, input("Enter allowed positions: ").split()))
                    counter.update_constraint(element, positions)
                    print("Constraint updated")
                elif cmd == "count":
                    result = counter.count_reorderings()
                    print(f"Reorderings: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Reordering Theory**: Mathematical theory of reorderings
- **Factorial Properties**: Properties of factorials
- **Inclusion-Exclusion**: Count using inclusion-exclusion
- **Generating Functions**: Use generating functions for counting

#### **2. Number Theory**
- **Modular Arithmetic**: Properties of modular arithmetic
- **Prime Factorization**: Factor numbers for modular operations
- **Fermat's Little Theorem**: For modular inverses
- **Chinese Remainder Theorem**: For multiple moduli

#### **3. Optimization Theory**
- **Combinatorial Optimization**: Optimize combinatorial problems
- **Dynamic Programming**: Optimize using dynamic programming
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Dynamic Programming**: Efficient DP algorithms
- **Modular Arithmetic**: Modular arithmetic algorithms
- **Combinatorial Algorithms**: Combinatorial algorithms
- **Optimization Algorithms**: Optimization algorithms

#### **2. Mathematical Concepts**
- **Combinatorics**: Foundation for counting problems
- **Number Theory**: Mathematical properties of numbers
- **Modular Theory**: Properties of modular arithmetic
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Combinatorial Processing**: Efficient combinatorial processing techniques
- **Modular Processing**: Modular processing techniques

---

*This analysis demonstrates efficient reordering counting techniques and shows various extensions for combinatorial and modular arithmetic problems.* 