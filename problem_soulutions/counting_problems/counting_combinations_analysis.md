---
layout: simple
title: "Counting Combinations"
permalink: /problem_soulutions/counting_problems/counting_combinations_analysis
---


# Counting Combinations

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of combinations and binomial coefficients
- Apply the formula C(n,k) = n!/(k!(n-k)!) for combination counting
- Implement modular arithmetic for large combination calculations
- Optimize combination calculations using precomputed factorials and modular inverses
- Handle edge cases in combination counting (k=0, k=n, large numbers)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Combinatorics, binomial coefficients, modular arithmetic, factorial calculations
- **Data Structures**: Arrays for precomputed factorials, modular inverse tables
- **Mathematical Concepts**: Factorials, combinations, modular arithmetic, Fermat's little theorem
- **Programming Skills**: Modular arithmetic, factorial computation, modular inverse calculation
- **Related Problems**: Counting Permutations (permutation counting), Two Sets II (combination problems), Coin Combinations I (counting problems)

## 📋 Problem Description

Given integers n and k, count the number of ways to choose k elements from a set of n elements (combinations).

This is a combinatorics problem where we need to calculate the number of ways to choose k elements from a set of n elements without considering order. This is the classic "n choose k" problem, which can be solved using the binomial coefficient formula with modular arithmetic.

**Input**: 
- First line: two integers n and k (total number of elements and number to choose)

**Output**: 
- Print the number of combinations modulo 10⁹ + 7

**Constraints**:
- 1 ≤ n ≤ 10⁶
- 0 ≤ k ≤ n

**Example**:
```
Input:
5 2

Output:
10
```

**Explanation**: 
From a set of 5 elements, we can choose 2 elements in C(5,2) = 10 ways:
- {1,2}, {1,3}, {1,4}, {1,5}, {2,3}, {2,4}, {2,5}, {3,4}, {3,5}, {4,5}

### 📊 Visual Example

**All Combinations of 5 Elements Choose 2:**
```
Set: {1, 2, 3, 4, 5}
Choose: 2 elements

Combination 1: {1, 2}
Combination 2: {1, 3}
Combination 3: {1, 4}
Combination 4: {1, 5}
Combination 5: {2, 3}
Combination 6: {2, 4}
Combination 7: {2, 5}
Combination 8: {3, 4}
Combination 9: {3, 5}
Combination 10: {4, 5}

Total: 10 combinations
```

**Binomial Coefficient Formula:**
```
C(n, k) = n! / (k! * (n-k)!)

For C(5, 2):
C(5, 2) = 5! / (2! * 3!)
        = 120 / (2 * 6)
        = 120 / 12
        = 10
```

**Pascal's Triangle:**
```
Row 0:        1
Row 1:      1   1
Row 2:    1   2   1
Row 3:  1   3   3   1
Row 4: 1   4   6   4   1
Row 5:1   5  10  10   5   1

C(5, 2) = 10 (from row 5, position 2)
```

**Recursive Formula:**
```
C(n, k) = C(n-1, k-1) + C(n-1, k)

For C(5, 2):
C(5, 2) = C(4, 1) + C(4, 2)
        = 4 + 6
        = 10

Explanation:
- C(4, 1): Choose 1 from {1,2,3,4} and add element 5
- C(4, 2): Choose 2 from {1,2,3,4} without element 5
```

**Dynamic Programming Table:**
```
     k=0  k=1  k=2  k=3  k=4  k=5
n=0:  1    0    0    0    0    0
n=1:  1    1    0    0    0    0
n=2:  1    2    1    0    0    0
n=3:  1    3    3    1    0    0
n=4:  1    4    6    4    1    0
n=5:  1    5   10   10    5    1

Answer: dp[5][2] = 10
```

**DP State Transitions:**
```
For n=2:
┌─────────────────────────────────────┐
│ dp[2][0] = dp[1][0] = 1            │
│ dp[2][1] = dp[1][0] + dp[1][1] = 2 │
│ dp[2][2] = dp[1][1] = 1            │
└─────────────────────────────────────┘

For n=3:
┌─────────────────────────────────────┐
│ dp[3][0] = dp[2][0] = 1            │
│ dp[3][1] = dp[2][0] + dp[2][1] = 3 │
│ dp[3][2] = dp[2][1] + dp[2][2] = 3 │
│ dp[3][3] = dp[2][2] = 1            │
└─────────────────────────────────────┘
```

**Mathematical Properties:**
```
Symmetry: C(n, k) = C(n, n-k)
Example: C(5, 2) = C(5, 3) = 10

Boundary conditions:
C(n, 0) = 1 (choose nothing)
C(n, n) = 1 (choose everything)
C(n, 1) = n (choose one element)
```

**Algorithm Flowchart:**
```
┌─────────────────────────────────────┐
│ Start: Read n and k                 │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ If k > n or k < 0: return 0         │
│ If k == 0 or k == n: return 1       │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Use formula:                        │
│ C(n,k) = n! / (k! * (n-k)!)        │
│ with modular arithmetic             │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return result modulo 10^9 + 7       │
└─────────────────────────────────────┘
```

**Key Insight Visualization:**
```
For C(5, 2), we can think of it as:

Method 1: Include element 5
┌─────────────────────────────────────┐
│ Choose 1 more from {1,2,3,4}       │
│ Ways: C(4, 1) = 4                  │
│ Combinations: {1,5}, {2,5}, {3,5}, {4,5}│
└─────────────────────────────────────┘

Method 2: Exclude element 5
┌─────────────────────────────────────┐
│ Choose 2 from {1,2,3,4}            │
│ Ways: C(4, 2) = 6                  │
│ Combinations: {1,2}, {1,3}, {1,4}, {2,3}, {2,4}, {3,4}│
└─────────────────────────────────────┘

Total: 4 + 6 = 10 ways
```

## Solution Progression

### Approach 1: Recursive Definition - O(2^n)
**Description**: Use recursive definition of combinations.

```python
def counting_combinations_naive(n, k):
    MOD = 10**9 + 7
    
    def comb(n, k):
        if k == 0 or k == n:
            return 1
        return (comb(n-1, k-1) + comb(n-1, k)) % MOD
    
    return comb(n, k)
```

**Why this is inefficient**: O(2^n) complexity is too slow for large n.

### Improvement 1: Dynamic Programming - O(nk)
**Description**: Use DP to avoid recalculating subproblems.

```python
def counting_combinations_dp(n, k):
    MOD = 10**9 + 7
    
    # dp[i][j] = C(i,j)
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        dp[i][0] = 1
        if i <= k:
            dp[i][i] = 1
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, min(i, k + 1)):
            dp[i][j] = (dp[i-1][j-1] + dp[i-1][j]) % MOD
    
    return dp[n][k]
```

**Why this improvement works**: DP avoids recalculating subproblems.

### Approach 2: Mathematical Formula - O(n)
**Description**: Use mathematical formula with modular arithmetic.

```python
def counting_combinations_mathematical(n, k):
    MOD = 10**9 + 7
    
    if k > n:
        return 0
    
    # C(n,k) = n! / (k! * (n-k)!)
    # Use modular arithmetic
    def factorial(n):
        result = 1
        for i in range(1, n + 1):
            result = (result * i) % MOD
        return result
    
    def mod_inverse(a, m):
        # Fermat's little theorem: a^(m-1) ≡ 1 (mod m)
        return pow(a, m-2, m)
    
    numerator = factorial(n)
    denominator = (factorial(k) * factorial(n - k)) % MOD
    inverse = mod_inverse(denominator, MOD)
    
    return (numerator * inverse) % MOD
```

**Why this improvement works**: Mathematical formula with modular arithmetic.

### Approach 3: Optimized Formula - O(n)
**Description**: Optimize the formula calculation.

```python
def counting_combinations_optimized(n, k):
    MOD = 10**9 + 7
    
    if k > n:
        return 0
    
    # C(n,k) = n! / (k! * (n-k)!)
    # Optimize by canceling common factors
    if k > n - k:
        k = n - k  # C(n,k) = C(n,n-k)
    
    result = 1
    for i in range(k):
        result = (result * (n - i)) % MOD
        result = (result * pow(i + 1, MOD - 2, MOD)) % MOD
    
    return result
```

**Why this improvement works**: Optimized calculation with modular inverses.

## Final Optimal Solution

```python
n, k = map(int, input().split())

def count_combinations(n, k):
    MOD = 10**9 + 7
    
    if k > n:
        return 0
    
    # Optimize by using symmetry
    if k > n - k:
        k = n - k
    
    result = 1
    for i in range(k):
        result = (result * (n - i)) % MOD
        result = (result * pow(i + 1, MOD - 2, MOD)) % MOD
    
    return result

result = count_combinations(n, k)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive Definition | O(2^n) | O(n) | Simple but exponential |
| Dynamic Programming | O(nk) | O(nk) | DP avoids recalculation |
| Mathematical Formula | O(n) | O(1) | Formula with modular arithmetic |
| Optimized Formula | O(n) | O(1) | Optimal solution |

## Key Insights for Other Problems

### 1. **Combination Properties**
**Principle**: C(n,k) = C(n,n-k) and C(n,k) = C(n-1,k-1) + C(n-1,k).
**Applicable to**: Combinatorics problems, combination counting problems

### 2. **Modular Arithmetic**
**Principle**: Use modular arithmetic and Fermat's little theorem for division.
**Applicable to**: Large number problems, modular arithmetic problems

### 3. **Optimization Techniques**
**Principle**: Use symmetry and cancel common factors to optimize calculations.
**Applicable to**: Mathematical optimization problems, formula simplification

## Notable Techniques

### 1. **Pascal's Triangle**
```python
def pascal_triangle(n, k, MOD):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = 1
        if i <= k:
            dp[i][i] = 1
    
    for i in range(1, n + 1):
        for j in range(1, min(i, k + 1)):
            dp[i][j] = (dp[i-1][j-1] + dp[i-1][j]) % MOD
    
    return dp[n][k]
```

### 2. **Modular Inverse**
```python
def mod_inverse(a, m):
    return pow(a, m - 2, m)
```

### 3. **Optimized Combination**
```python
def optimized_combination(n, k, MOD):
    if k > n:
        return 0
    
    if k > n - k:
        k = n - k
    
    result = 1
    for i in range(k):
        result = (result * (n - i)) % MOD
        result = (result * pow(i + 1, MOD - 2, MOD)) % MOD
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a combination counting problem
2. **Choose approach**: Use optimized mathematical formula
3. **Handle edge cases**: k > n case
4. **Use symmetry**: C(n,k) = C(n,n-k) for optimization
5. **Apply formula**: C(n,k) = n! / (k! * (n-k)!)
6. **Use modular arithmetic**: Handle large numbers
7. **Return result**: Output the combination count modulo 10^9 + 7

---

*This analysis shows how to efficiently count combinations using dynamic programming with modulo arithmetic for large numbers.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Combinations**
**Problem**: Each element has a weight. Find combinations with total weight equal to target.
```python
def weighted_combinations(n, target, weights, MOD=10**9+7):
    # weights[i] = weight of element i
    dp = [[0] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(target + 1):
            # Don't include element i
            dp[i][j] = dp[i-1][j]
            
            # Include element i if weight allows
            if j >= weights[i-1]:
                dp[i][j] = (dp[i][j] + dp[i-1][j - weights[i-1]]) % MOD
    
    return dp[n][target]
```

#### **Variation 2: Constrained Combinations**
**Problem**: Find combinations with constraints on element selection.
```python
def constrained_combinations(n, k, constraints, MOD=10**9+7):
    # constraints[i] = max times element i can be selected
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(k + 1):
            # Don't include element i
            dp[i][j] = dp[i-1][j]
            
            # Include element i up to constraint limit
            for count in range(1, min(constraints[i-1], j) + 1):
                dp[i][j] = (dp[i][j] + dp[i-1][j - count]) % MOD
    
    return dp[n][k]
```

#### **Variation 3: Ordered Combinations**
**Problem**: Count combinations where order matters (permutations with repetition).
```python
def ordered_combinations(n, k, MOD=10**9+7):
    # Count ordered combinations of k elements from n
    if k > n:
        return 0
    
    # Use formula: n! / (k! * (n-k)!)
    numerator = 1
    denominator = 1
    
    for i in range(k):
        numerator = (numerator * (n - i)) % MOD
        denominator = (denominator * (i + 1)) % MOD
    
    # Modular multiplicative inverse
    def mod_inverse(a, m):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            return None
        return (x % m + m) % m
    
    inv_denominator = mod_inverse(denominator, MOD)
    return (numerator * inv_denominator) % MOD
```

#### **Variation 4: Circular Combinations**
**Problem**: Count combinations in a circular arrangement.
```python
def circular_combinations(n, k, MOD=10**9+7):
    # Count combinations in circular arrangement
    if k == 0:
        return 1
    if k == 1:
        return n
    if k > n:
        return 0
    
    # For circular combinations, we need to handle wrap-around
    # Use inclusion-exclusion principle
    result = 0
    
    # Count linear combinations
    linear = ordered_combinations(n, k, MOD)
    
    # Subtract combinations that wrap around
    if k > 1:
        # Count combinations that start and end at adjacent positions
        wrap_around = ordered_combinations(n - k + 1, k - 1, MOD)
        result = (linear - wrap_around) % MOD
    else:
        result = linear
    
    return result
```

#### **Variation 5: Dynamic Combination Updates**
**Problem**: Support dynamic updates to constraints and answer combination queries efficiently.
```python
class DynamicCombinationCounter:
    def __init__(self, n, MOD=10**9+7):
        self.n = n
        self.MOD = MOD
        self.constraints = [1] * n  # Default: each element can be used once
        self.factorial = [1] * (n + 1)
        self.inv_factorial = [1] * (n + 1)
        
        # Precompute factorials and inverse factorials
        for i in range(1, n + 1):
            self.factorial[i] = (self.factorial[i-1] * i) % MOD
        
        # Compute inverse factorials using Fermat's little theorem
        for i in range(1, n + 1):
            self.inv_factorial[i] = pow(self.factorial[i], MOD-2, MOD)
    
    def update_constraint(self, i, new_constraint):
        self.constraints[i] = new_constraint
    
    def count_combinations(self, k):
        if k > sum(self.constraints):
            return 0
        
        # Use dynamic programming with current constraints
        dp = [[0] * (k + 1) for _ in range(self.n + 1)]
        dp[0][0] = 1
        
        for i in range(1, self.n + 1):
            for j in range(k + 1):
                dp[i][j] = dp[i-1][j]
                
                for count in range(1, min(self.constraints[i-1], j) + 1):
                    dp[i][j] = (dp[i][j] + dp[i-1][j - count]) % self.MOD
        
        return dp[self.n][k]
```

### 🔗 **Related Problems & Concepts**

#### **1. Combination Problems**
- **Combination Counting**: Count combinations efficiently
- **Combination Generation**: Generate combinations
- **Combination Optimization**: Optimize combination algorithms
- **Combination Analysis**: Analyze combination properties

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
    n, k = map(int, input().split())
    
    result = count_combinations(n, k)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute combinations for different ranges
def precompute_combinations(max_n, max_k, MOD=10**9+7):
    dp = [[0] * (max_k + 1) for _ in range(max_n + 1)]
    
    # Base case
    for i in range(max_n + 1):
        dp[i][0] = 1
    
    # Fill DP table
    for i in range(1, max_n + 1):
        for j in range(1, min(i + 1, max_k + 1)):
            dp[i][j] = (dp[i-1][j] + dp[i-1][j-1]) % MOD
    
    return dp

# Answer range queries efficiently
def range_query(dp, n, k):
    if k > n:
        return 0
    return dp[n][k]
```

#### **3. Interactive Problems**
```python
# Interactive combination calculator
def interactive_combination_calculator():
    MOD = 10**9 + 7
    
    while True:
        query = input("Enter query (combinations/weighted/constrained/ordered/circular/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "combinations":
            n, k = map(int, input("Enter n and k: ").split())
            result = count_combinations(n, k)
            print(f"C({n},{k}) = {result}")
        elif query == "weighted":
            n = int(input("Enter n: "))
            target = int(input("Enter target weight: "))
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_combinations(n, target, weights)
            print(f"Weighted combinations: {result}")
        elif query == "constrained":
            n, k = map(int, input("Enter n and k: ").split())
            constraints = list(map(int, input("Enter constraints: ").split()))
            result = constrained_combinations(n, k, constraints)
            print(f"Constrained combinations: {result}")
        elif query == "ordered":
            n, k = map(int, input("Enter n and k: ").split())
            result = ordered_combinations(n, k)
            print(f"Ordered combinations: {result}")
        elif query == "circular":
            n, k = map(int, input("Enter n and k: ").split())
            result = circular_combinations(n, k)
            print(f"Circular combinations: {result}")
        elif query == "dynamic":
            n = int(input("Enter n: "))
            counter = DynamicCombinationCounter(n)
            
            while True:
                cmd = input("Enter command (update/count/back): ")
                if cmd == "back":
                    break
                elif cmd == "update":
                    i, constraint = map(int, input("Enter index and new constraint: ").split())
                    counter.update_constraint(i, constraint)
                    print("Constraint updated")
                elif cmd == "count":
                    k = int(input("Enter k: "))
                    result = counter.count_combinations(k)
                    print(f"Combinations: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Combination Theory**: Mathematical theory of combinations
- **Binomial Coefficients**: Properties of binomial coefficients
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
## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n) for precomputing factorials, O(1) per query
- **Space Complexity**: O(n) for storing factorials and modular inverses
- **Why it works**: We precompute factorials and their modular inverses to calculate combinations efficiently using the formula C(n,k) = n! / (k! * (n-k)!)

### Key Implementation Points
- Precompute factorials modulo 10⁹ + 7
- Precompute modular inverses of factorials using Fermat's little theorem
- Use the formula C(n,k) = n! / (k! * (n-k)!) with modular arithmetic
- Handle edge cases like k = 0 or k = n

## 🎯 Key Insights

### Important Concepts and Patterns
- **Binomial Coefficients**: Mathematical foundation for combinations
- **Modular Arithmetic**: Essential for handling large numbers
- **Fermat's Little Theorem**: Used for computing modular inverses
- **Precomputation**: Efficient technique for multiple queries

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Counting Combinations with Multiple Queries**
```python
def counting_combinations_multiple_queries(queries):
    # Precompute factorials and modular inverses
    MOD = 10**9 + 7
    MAX_N = 10**6
    
    # Precompute factorials
    fact = [1] * (MAX_N + 1)
    for i in range(1, MAX_N + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    # Precompute modular inverses using Fermat's little theorem
    inv_fact = [1] * (MAX_N + 1)
    inv_fact[MAX_N] = pow(fact[MAX_N], MOD - 2, MOD)
    for i in range(MAX_N - 1, -1, -1):
        inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % MOD
    
    def comb(n, k):
        if k > n or k < 0:
            return 0
        return (fact[n] * inv_fact[k] % MOD) * inv_fact[n - k] % MOD
    
    # Answer all queries
    results = []
    for n, k in queries:
        results.append(comb(n, k))
    
    return results

# Example usage
queries = [(5, 2), (10, 3), (100, 50)]
results = counting_combinations_multiple_queries(queries)
print(f"Combination results: {results}")
```

#### **2. Counting Combinations with Range Queries**
```python
def counting_combinations_range_queries(n, range_queries):
    # Count combinations for range queries on k
    MOD = 10**9 + 7
    
    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    # Precompute modular inverses
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, -1, -1):
        inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % MOD
    
    def comb(n, k):
        if k > n or k < 0:
            return 0
        return (fact[n] * inv_fact[k] % MOD) * inv_fact[n - k] % MOD
    
    # Answer range queries
    results = []
    for start_k, end_k in range_queries:
        total = 0
        for k in range(start_k, end_k + 1):
            total = (total + comb(n, k)) % MOD
        results.append(total)
    
    return results

# Example usage
n = 10
range_queries = [(0, 5), (3, 7), (8, 10)]
results = counting_combinations_range_queries(n, range_queries)
print(f"Range query results: {results}")
```

#### **3. Counting Combinations with Constraints**
```python
def counting_combinations_with_constraints(n, k, constraints):
    # Count combinations with additional constraints
    MOD = 10**9 + 7
    
    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    # Precompute modular inverses
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, -1, -1):
        inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % MOD
    
    def comb(n, k):
        if k > n or k < 0:
            return 0
        return (fact[n] * inv_fact[k] % MOD) * inv_fact[n - k] % MOD
    
    # Apply constraints
    if constraints.get("min_k", 0) > k:
        return 0
    if constraints.get("max_k", n) < k:
        return 0
    if constraints.get("even_k", False) and k % 2 != 0:
        return 0
    if constraints.get("odd_k", False) and k % 2 == 0:
        return 0
    
    return comb(n, k)

# Example usage
n, k = 10, 3
constraints = {"min_k": 2, "max_k": 5, "even_k": False}
result = counting_combinations_with_constraints(n, k, constraints)
print(f"Constrained combination: {result}")
```

#### **4. Counting Combinations with Statistics**
```python
def counting_combinations_with_statistics(n):
    # Calculate combination statistics for all k
    MOD = 10**9 + 7
    
    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    # Precompute modular inverses
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n - 1, -1, -1):
        inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % MOD
    
    def comb(n, k):
        if k > n or k < 0:
            return 0
        return (fact[n] * inv_fact[k] % MOD) * inv_fact[n - k] % MOD
    
    # Calculate all combinations
    combinations = [comb(n, k) for k in range(n + 1)]
    
    # Calculate statistics
    total = sum(combinations) % MOD
    max_comb = max(combinations)
    max_k = combinations.index(max_comb)
    min_comb = min(combinations)
    min_k = combinations.index(min_comb)
    
    statistics = {
        "total_combinations": total,
        "max_combination": max_comb,
        "max_k": max_k,
        "min_combination": min_comb,
        "min_k": min_k,
        "all_combinations": combinations
    }
    
    return statistics

# Example usage
n = 10
stats = counting_combinations_with_statistics(n)
print(f"Combination statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Combinatorics**: Permutations, Arrangements, Partitions
- **Modular Arithmetic**: Modular exponentiation, Modular inverses
- **Mathematical Algorithms**: Factorial computation, Prime factorization
- **Counting Problems**: Subset counting, Path counting

## 📚 Learning Points

### Key Takeaways
- **Binomial coefficients** are fundamental in combinatorics
- **Modular arithmetic** is essential for handling large numbers
- **Precomputation** can significantly improve performance for multiple queries
- **Fermat's little theorem** provides an efficient way to compute modular inverses

---

*This analysis demonstrates efficient combination counting techniques and shows various extensions for combinatorial and modular arithmetic problems.* 