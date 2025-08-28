---
layout: simple
title: "Empty String"permalink: /problem_soulutions/counting_problems/empty_string_analysis
---


# Empty String

## Problem Statement
Given a string s, you can perform the following operation: remove two adjacent equal characters. Count the number of different ways to reduce the string to an empty string.

### Input
The first input line has a string s.

### Output
Print one integer: the number of ways to reduce the string to empty.

### Constraints
- 1 ≤ |s| ≤ 100
- String contains only lowercase letters

### Example
```
Input:
aab

Output:
2
```

## Solution Progression

### Approach 1: Generate All Removal Sequences - O(n!)
**Description**: Generate all possible sequences of removing adjacent equal characters.

```python
def empty_string_naive(s):
    def can_remove(s, i):
        return i + 1 < len(s) and s[i] == s[i + 1]
    
    def remove_chars(s, i):
        return s[:i] + s[i + 2:]
    
    def count_ways(s):
        if len(s) == 0:
            return 1
        
        count = 0
        for i in range(len(s) - 1):
            if can_remove(s, i):
                new_s = remove_chars(s, i)
                count += count_ways(new_s)
        
        return count
    
    return count_ways(s)
```

**Why this is inefficient**: We need to try all possible removal sequences, leading to factorial time complexity.

### Improvement 1: Dynamic Programming with Memoization - O(n³)
**Description**: Use dynamic programming to avoid recalculating the same subproblems.

```python
def empty_string_dp(s):
    n = len(s)
    dp = {}
    
    def count_ways(left, right):
        if left > right:
            return 1
        
        if (left, right) in dp:
            return dp[(left, right)]
        
        count = 0
        
        # Try removing pairs of adjacent equal characters
        for i in range(left, right):
            if s[i] == s[i + 1]:
                # Remove characters at positions i and i+1
                count += count_ways(left, i - 1) * count_ways(i + 2, right)
        
        dp[(left, right)] = count
        return count
    
    return count_ways(0, n - 1)
```

**Why this improvement works**: Dynamic programming with memoization avoids recalculating the same subproblems.

## Final Optimal Solution

```python
s = input().strip()

def count_empty_string_ways(s):
    n = len(s)
    dp = {}
    
    def count_ways(left, right):
        if left > right:
            return 1
        
        if (left, right) in dp:
            return dp[(left, right)]
        
        count = 0
        
        # Try removing pairs of adjacent equal characters
        for i in range(left, right):
            if s[i] == s[i + 1]:
                # Remove characters at positions i and i+1
                count += count_ways(left, i - 1) * count_ways(i + 2, right)
        
        dp[(left, right)] = count
        return count
    
    return count_ways(0, n - 1)

result = count_empty_string_ways(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n!) | O(n) | Generate all removal sequences |
| Dynamic Programming | O(n³) | O(n²) | Use memoization to avoid recalculation |

## Key Insights for Other Problems

### 1. **String Reduction Problems**
**Principle**: Use dynamic programming to count different ways to reduce strings.
**Applicable to**: String problems, reduction problems, counting problems

### 2. **Dynamic Programming with Memoization**
**Principle**: Store results of subproblems to avoid recalculating.
**Applicable to**: Optimization problems, counting problems, recursive problems

### 3. **Adjacent Character Removal**
**Principle**: Focus on removing adjacent equal characters systematically.
**Applicable to**: String manipulation problems, pattern matching problems

## Notable Techniques

### 1. **Dynamic Programming Pattern**
```python
def dp_with_memoization(s):
    n = len(s)
    dp = {}
    
    def solve(left, right):
        if left > right:
            return 1
        
        if (left, right) in dp:
            return dp[(left, right)]
        
        # Solve subproblem
        result = solve_subproblem(left, right)
        dp[(left, right)] = result
        return result
    
    return solve(0, n - 1)
```

### 2. **Adjacent Pair Removal**
```python
def remove_adjacent_pairs(s, left, right):
    count = 0
    
    for i in range(left, right):
        if s[i] == s[i + 1]:
            # Remove characters at positions i and i+1
            count += solve(left, i - 1) * solve(i + 2, right)
    
    return count
```

### 3. **String Reduction Check**
```python
def can_reduce_to_empty(s):
    if len(s) == 0:
        return True
    
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            new_s = s[:i] + s[i + 2:]
            if can_reduce_to_empty(new_s):
                return True
    
    return False
```

## Problem-Solving Framework

1. **Identify problem type**: This is a string reduction counting problem
2. **Choose approach**: Use dynamic programming with memoization
3. **Define subproblems**: Count ways to reduce substring [left, right]
4. **Implement recursion**: Try removing adjacent equal pairs
5. **Count results**: Sum up all valid reduction sequences

---

*This analysis shows how to efficiently count empty strings using dynamic programming with state tracking and memoization.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Empty Strings**
**Problem**: Each operation has a weight. Find empty strings with total weight equal to target.
```python
def weighted_empty_strings(n, target, weights, MOD=10**9+7):
    # weights[i] = weight of operation i
    dp = [[0] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(target + 1):
            # Don't include operation i
            dp[i][j] = dp[i-1][j]
            
            # Include operation i if weight allows
            if j >= weights[i-1]:
                dp[i][j] = (dp[i][j] + dp[i-1][j - weights[i-1]]) % MOD
    
    return dp[n][target]
```

#### **Variation 2: Constrained Empty Strings**
**Problem**: Find empty strings with constraints on operation usage.
```python
def constrained_empty_strings(n, k, constraints, MOD=10**9+7):
    # constraints[i] = max times operation i can be used
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(k + 1):
            # Don't include operation i
            dp[i][j] = dp[i-1][j]
            
            # Include operation i up to constraint limit
            for count in range(1, min(constraints[i-1], j) + 1):
                dp[i][j] = (dp[i][j] + dp[i-1][j - count]) % MOD
    
    return dp[n][k]
```

#### **Variation 3: Ordered Empty Strings**
**Problem**: Count empty strings where order of operations matters.
```python
def ordered_empty_strings(n, k, MOD=10**9+7):
    # Count ordered empty strings using k operations from n
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

#### **Variation 4: Circular Empty Strings**
**Problem**: Count empty strings in a circular arrangement.
```python
def circular_empty_strings(n, k, MOD=10**9+7):
    # Count circular empty strings using k operations from n
    if k == 0:
        return 1
    if k == 1:
        return n
    if k > n:
        return 0
    
    # For circular empty strings, we need to handle wrap-around
    # Use inclusion-exclusion principle
    result = 0
    
    # Count linear empty strings
    linear = ordered_empty_strings(n, k, MOD)
    
    # Subtract empty strings that wrap around
    if k > 1:
        # Count empty strings that start and end at adjacent positions
        wrap_around = ordered_empty_strings(n - k + 1, k - 1, MOD)
        result = (linear - wrap_around) % MOD
    else:
        result = linear
    
    return result
```

#### **Variation 5: Dynamic Empty String Updates**
**Problem**: Support dynamic updates to constraints and answer empty string queries efficiently.
```python
class DynamicEmptyStringCounter:
    def __init__(self, n, MOD=10**9+7):
        self.n = n
        self.MOD = MOD
        self.constraints = [1] * n  # Default: each operation can be used once
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
    
    def count_empty_strings(self, k):
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

#### **1. String Problems**
- **String Manipulation**: Manipulate strings efficiently
- **String Generation**: Generate strings
- **String Optimization**: Optimize string algorithms
- **String Analysis**: Analyze string properties

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
    
    result = count_empty_strings(n, k)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute empty strings for different ranges
def precompute_empty_strings(max_n, max_k, MOD=10**9+7):
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
# Interactive empty string calculator
def interactive_empty_string_calculator():
    MOD = 10**9 + 7
    
    while True:
        query = input("Enter query (empty_strings/weighted/constrained/ordered/circular/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "empty_strings":
            n, k = map(int, input("Enter n and k: ").split())
            result = count_empty_strings(n, k)
            print(f"E({n},{k}) = {result}")
        elif query == "weighted":
            n = int(input("Enter n: "))
            target = int(input("Enter target weight: "))
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_empty_strings(n, target, weights)
            print(f"Weighted empty strings: {result}")
        elif query == "constrained":
            n, k = map(int, input("Enter n and k: ").split())
            constraints = list(map(int, input("Enter constraints: ").split()))
            result = constrained_empty_strings(n, k, constraints)
            print(f"Constrained empty strings: {result}")
        elif query == "ordered":
            n, k = map(int, input("Enter n and k: ").split())
            result = ordered_empty_strings(n, k)
            print(f"Ordered empty strings: {result}")
        elif query == "circular":
            n, k = map(int, input("Enter n and k: ").split())
            result = circular_empty_strings(n, k)
            print(f"Circular empty strings: {result}")
        elif query == "dynamic":
            n = int(input("Enter n: "))
            counter = DynamicEmptyStringCounter(n)
            
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
                    result = counter.count_empty_strings(k)
                    print(f"Empty strings: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Empty String Theory**: Mathematical theory of empty strings
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

*This analysis demonstrates efficient empty string counting techniques and shows various extensions for combinatorial and modular arithmetic problems.* 