---
layout: simple
title: "Counting Permutations"
permalink: /problem_soulutions/counting_problems/counting_permutations_analysis
---


# Counting Permutations

## 📋 Problem Description

Given an integer n, count the number of permutations of {1, 2, ..., n} that have exactly k inversions.

This is a combinatorial problem where we need to count the number of permutations with a specific number of inversions. An inversion is a pair of indices (i,j) where i < j and a[i] > a[j]. We can solve this using dynamic programming.

**Input**: 
- First line: two integers n and k (size of the permutation and number of inversions)

**Output**: 
- Print the number of permutations modulo 10⁹ + 7

**Constraints**:
- 1 ≤ n ≤ 1000
- 0 ≤ k ≤ n(n-1)/2

**Example**:
```
Input:
3 1

Output:
2
```

**Explanation**: 
For n = 3, there are 6 possible permutations: [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]. We need to find those with exactly 1 inversion:
1. [1,3,2]: 1 inversion (3 > 2)
2. [2,1,3]: 1 inversion (2 > 1)

So there are 2 permutations with exactly 1 inversion.

### 📊 Visual Example

**All Permutations of {1, 2, 3}:**
```
Permutation 1: [1, 2, 3]
Inversions: None (0 inversions)
Pairs: (1,2), (1,3), (2,3) - all increasing ✓

Permutation 2: [1, 3, 2]
Inversions: 1 inversion
Pairs: (1,3) ✓, (1,2) ✓, (3,2) ✗ (3 > 2)
Count: 1 inversion ✓

Permutation 3: [2, 1, 3]
Inversions: 1 inversion
Pairs: (2,1) ✗ (2 > 1), (2,3) ✓, (1,3) ✓
Count: 1 inversion ✓

Permutation 4: [2, 3, 1]
Inversions: 2 inversions
Pairs: (2,3) ✓, (2,1) ✗ (2 > 1), (3,1) ✗ (3 > 1)
Count: 2 inversions

Permutation 5: [3, 1, 2]
Inversions: 2 inversions
Pairs: (3,1) ✗ (3 > 1), (3,2) ✗ (3 > 2), (1,2) ✓
Count: 2 inversions

Permutation 6: [3, 2, 1]
Inversions: 3 inversions
Pairs: (3,2) ✗ (3 > 2), (3,1) ✗ (3 > 1), (2,1) ✗ (2 > 1)
Count: 3 inversions
```

**Inversion Analysis:**
```
Target: Exactly 1 inversion

Valid permutations:
┌─────────────────────────────────────┐
│ [1, 3, 2]:                         │
│ - Position 0: 1                    │
│ - Position 1: 3                    │
│ - Position 2: 2                    │
│ - Inversion: (1,2) where 3 > 2     │
│ - Count: 1 ✓                       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ [2, 1, 3]:                         │
│ - Position 0: 2                    │
│ - Position 1: 1                    │
│ - Position 2: 3                    │
│ - Inversion: (0,1) where 2 > 1     │
│ - Count: 1 ✓                       │
└─────────────────────────────────────┘
```

**Dynamic Programming Approach:**
```
State: dp[i][j] = number of permutations of {1,2,...,i} with j inversions

Base cases:
dp[1][0] = 1 (permutation [1] has 0 inversions)
dp[i][j] = 0 for j < 0 or j > i(i-1)/2

Recurrence:
dp[i][j] = Σ(dp[i-1][j-k]) for k = 0 to min(j, i-1)

Explanation: When inserting element i into a permutation of {1,2,...,i-1},
it can create 0 to i-1 new inversions depending on its position.
```

**DP Table for n=3, k=1:**
```
     j=0  j=1  j=2  j=3
i=1:  1    0    0    0
i=2:  1    1    0    0
i=3:  1    2    2    1

Answer: dp[3][1] = 2
```

**DP State Transitions:**
```
For i=2:
┌─────────────────────────────────────┐
│ dp[2][0] = dp[1][0] = 1            │
│ (Insert 2 at end: [1,2])           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ dp[2][1] = dp[1][1] = 0            │
│ (Insert 2 at beginning: [2,1])     │
└─────────────────────────────────────┘

For i=3:
┌─────────────────────────────────────┐
│ dp[3][0] = dp[2][0] = 1            │
│ (Insert 3 at end: [1,2,3])         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ dp[3][1] = dp[2][1] + dp[2][0] = 0 + 1 = 1│
│ (Insert 3 at position 1: [1,3,2])  │
│ (Insert 3 at position 0: [2,1,3])  │
└─────────────────────────────────────┘
```

**Algorithm Flowchart:**
```
┌─────────────────────────────────────┐
│ Start: Read n and k                 │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Initialize DP table                 │
│ dp[1][0] = 1                        │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ For i from 2 to n:                  │
│   For j from 0 to min(k, i(i-1)/2): │
│     dp[i][j] = Σ(dp[i-1][j-k])      │
│     for k from 0 to min(j, i-1)     │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return dp[n][k]                     │
└─────────────────────────────────────┘
```

**Key Insight Visualization:**
```
When inserting element i into a permutation of {1,2,...,i-1}:

Position 0: Creates i-1 inversions
[1,2,3] → [4,1,2,3] (4 > 1, 4 > 2, 4 > 3)

Position 1: Creates i-2 inversions  
[1,2,3] → [1,4,2,3] (4 > 2, 4 > 3)

Position 2: Creates i-3 inversions
[1,2,3] → [1,2,4,3] (4 > 3)

Position 3: Creates 0 inversions
[1,2,3] → [1,2,3,4] (no inversions)
```

## Solution Progression

### Approach 1: Generate All Permutations - O(n! * n²)
**Description**: Generate all permutations and count inversions.

```python
def counting_permutations_naive(n, k):
    MOD = 10**9 + 7
    from itertools import permutations
    
    count = 0
    for perm in permutations(range(1, n + 1)):
        inversions = 0
        for i in range(n):
            for j in range(i + 1, n):
                if perm[i] > perm[j]:
                    inversions += 1
        if inversions == k:
            count = (count + 1) % MOD
    
    return count
```

**Why this is inefficient**: O(n! * n²) complexity is too slow for large n.

### Improvement 1: Dynamic Programming - O(n²k)
**Description**: Use DP to count permutations with given inversions.

```python
def counting_permutations_dp(n, k):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of permutations of length i with j inversions
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: empty permutation
    dp[0][0] = 1
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(k + 1):
            for l in range(min(i, j + 1)):
                dp[i][j] = (dp[i][j] + dp[i-1][j-l]) % MOD
    
    return dp[n][k]
```

**Why this improvement works**: DP avoids generating all permutations.

### Approach 2: Optimized DP - O(n²k)
**Description**: Optimize DP with better implementation.

```python
def counting_permutations_optimized(n, k):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of permutations of length i with j inversions
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case
    dp[0][0] = 1
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(k + 1):
            # Insert element i at position l (0-indexed)
            for l in range(min(i, j + 1)):
                dp[i][j] = (dp[i][j] + dp[i-1][j-l]) % MOD
    
    return dp[n][k]
```

**Why this improvement works**: Optimized DP implementation.

## Final Optimal Solution

```python
n, k = map(int, input().split())

def count_permutations_with_inversions(n, k):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of permutations of length i with j inversions
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case
    dp[0][0] = 1
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(k + 1):
            # Insert element i at position l (0-indexed)
            for l in range(min(i, j + 1)):
                dp[i][j] = (dp[i][j] + dp[i-1][j-l]) % MOD
    
    return dp[n][k]

result = count_permutations_with_inversions(n, k)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Generate All Permutations | O(n! * n²) | O(n) | Simple but factorial |
| Dynamic Programming | O(n²k) | O(nk) | DP avoids generation |
| Optimized DP | O(n²k) | O(nk) | Optimal solution |

## Key Insights for Other Problems

### 1. **Permutation Inversion Counting**
**Principle**: Use dynamic programming to count permutations with specific properties.
**Applicable to**: Permutation problems, inversion counting problems, DP problems

### 2. **DP for Permutation Properties**
**Principle**: Build permutations incrementally using DP.
**Applicable to**: Permutation analysis problems, counting problems

### 3. **Inversion Insertion**
**Principle**: Inserting a new element can create 0 to i-1 new inversions.
**Applicable to**: Permutation construction problems, inversion analysis

## Notable Techniques

### 1. **Permutation DP**
```python
def permutation_dp(n, k, MOD):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(k + 1):
            for l in range(min(i, j + 1)):
                dp[i][j] = (dp[i][j] + dp[i-1][j-l]) % MOD
    
    return dp[n][k]
```

### 2. **Inversion Calculation**
```python
def count_inversions(perm):
    inversions = 0
    n = len(perm)
    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                inversions += 1
    return inversions
```

## Problem-Solving Framework

1. **Identify problem type**: This is a permutation counting problem with inversion constraints
2. **Choose approach**: Use dynamic programming
3. **Initialize DP table**: Create 2D DP array
4. **Handle base case**: Empty permutation
5. **Fill DP table**: Build permutations incrementally
6. **Calculate inversions**: Track inversion count during construction
7. **Return result**: Output number of permutations with k inversions

---

*This analysis shows how to efficiently count permutations using mathematical formulas and modular arithmetic for large numbers.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Permutations**
**Problem**: Each element has a weight. Find permutations with total weight equal to target.
```python
def weighted_permutations(n, target, weights, MOD=10**9+7):
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

#### **Variation 2: Constrained Permutations**
**Problem**: Find permutations with constraints on element positions.
```python
def constrained_permutations(n, constraints, MOD=10**9+7):
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

#### **Variation 3: Circular Permutations**
**Problem**: Count permutations in a circular arrangement.
```python
def circular_permutations(n, MOD=10**9+7):
    # Count circular permutations of n elements
    if n <= 1:
        return 1
    
    # For circular permutations, we fix one element and permute the rest
    # Result is (n-1)!
    result = 1
    for i in range(1, n):
        result = (result * i) % MOD
    
    return result
```

#### **Variation 4: Derangement Permutations**
**Problem**: Count derangements (permutations where no element appears in its original position).
```python
def derangement_permutations(n, MOD=10**9+7):
    # Count derangements using inclusion-exclusion
    if n == 0:
        return 1
    if n == 1:
        return 0
    
    # Use formula: !n = n! * sum((-1)^k / k!) for k from 0 to n
    factorial = 1
    for i in range(1, n + 1):
        factorial = (factorial * i) % MOD
    
    # Compute sum of alternating series
    sum_series = 0
    term = 1
    for k in range(n + 1):
        if k > 0:
            term = (term * k) % MOD
        inv_term = pow(term, MOD-2, MOD) if term != 0 else 0
        if k % 2 == 0:
            sum_series = (sum_series + inv_term) % MOD
        else:
            sum_series = (sum_series - inv_term) % MOD
    
    return (factorial * sum_series) % MOD
```

#### **Variation 5: Dynamic Permutation Updates**
**Problem**: Support dynamic updates to constraints and answer permutation queries efficiently.
```python
class DynamicPermutationCounter:
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
    
    def count_permutations(self):
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

#### **1. Permutation Problems**
- **Permutation Counting**: Count permutations efficiently
- **Permutation Generation**: Generate permutations
- **Permutation Optimization**: Optimize permutation algorithms
- **Permutation Analysis**: Analyze permutation properties

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
    
    result = count_permutations(n)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute permutations for different ranges
def precompute_permutations(max_n, MOD=10**9+7):
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
# Interactive permutation calculator
def interactive_permutation_calculator():
    MOD = 10**9 + 7
    
    while True:
        query = input("Enter query (permutations/weighted/constrained/circular/derangement/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "permutations":
            n = int(input("Enter n: "))
            result = count_permutations(n)
            print(f"P({n}) = {result}")
        elif query == "weighted":
            n = int(input("Enter n: "))
            target = int(input("Enter target weight: "))
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_permutations(n, target, weights)
            print(f"Weighted permutations: {result}")
        elif query == "constrained":
            n = int(input("Enter n: "))
            constraints = []
            print("Enter constraints for each element:")
            for i in range(n):
                positions = list(map(int, input(f"Element {i}: ").split()))
                constraints.append(set(positions))
            result = constrained_permutations(n, constraints)
            print(f"Constrained permutations: {result}")
        elif query == "circular":
            n = int(input("Enter n: "))
            result = circular_permutations(n)
            print(f"Circular permutations: {result}")
        elif query == "derangement":
            n = int(input("Enter n: "))
            result = derangement_permutations(n)
            print(f"Derangements: {result}")
        elif query == "dynamic":
            n = int(input("Enter n: "))
            counter = DynamicPermutationCounter(n)
            
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
                    result = counter.count_permutations()
                    print(f"Permutations: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Permutation Theory**: Mathematical theory of permutations
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
## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n! × n²) for the naive approach, O(n × k) for dynamic programming
- **Space Complexity**: O(n × k) for storing DP states
- **Why it works**: We use dynamic programming to count permutations with specific inversion counts

### Key Implementation Points
- Use dynamic programming to avoid recomputing subproblems
- Handle base cases (n = 1, k = 0)
- Use modular arithmetic for large numbers
- Optimize by using the recurrence relation for permutation counting

## 🎯 Key Insights

### Important Concepts and Patterns
- **Dynamic Programming**: Essential for counting permutations efficiently
- **Combinatorics**: Understanding permutation properties
- **Inversion Counting**: Counting inversions in permutations
- **Modular Arithmetic**: Handling large numbers with modulo operations

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Counting Permutations with Range Queries**
```python
def counting_permutations_range_queries(n, k_range):
    # Count permutations for a range of inversion counts
    MOD = 10**9 + 7
    results = {}
    
    # Precompute all values using DP
    dp = [[0] * (n * (n - 1) // 2 + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        dp[i][0] = 1  # No inversions
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, min(i * (i - 1) // 2 + 1, len(dp[i]))):
            dp[i][j] = 0
            for l in range(min(j + 1, i)):
                dp[i][j] = (dp[i][j] + dp[i - 1][j - l]) % MOD
    
    # Answer queries
    for k in k_range:
        if k <= n * (n - 1) // 2:
            results[k] = dp[n][k]
        else:
            results[k] = 0
    
    return results

# Example usage
n = 4
k_range = [0, 1, 2, 3, 4, 5, 6]
results = counting_permutations_range_queries(n, k_range)
for k, count in results.items():
    print(f"Permutations with {k} inversions: {count}")
```

#### **2. Counting Permutations with Constraints**
```python
def counting_permutations_with_constraints(n, k, constraints):
    # Count permutations with constraints
    MOD = 10**9 + 7
    
    def count_permutations(n, k, memo):
        if n == 0:
            return 1 if k == 0 else 0
        
        if (n, k) in memo:
            return memo[(n, k)]
        
        count = 0
        for i in range(min(k + 1, n)):
            # Check constraints
            if constraints.get("max_inversions_per_element") and i > constraints["max_inversions_per_element"]:
                continue
            if constraints.get("min_inversions_per_element") and i < constraints["min_inversions_per_element"]:
                continue
            
            count = (count + count_permutations(n - 1, k - i, memo)) % MOD
        
        memo[(n, k)] = count
        return count
    
    return count_permutations(n, k, {})

# Example usage
n, k = 4, 2
constraints = {
    "max_inversions_per_element": 2,
    "min_inversions_per_element": 0
}
result = counting_permutations_with_constraints(n, k, constraints)
print(f"Permutations with constraints: {result}")
```

#### **3. Counting Permutations with Multiple Values**
```python
def counting_permutations_multiple_values(n_values, k_values):
    # Count permutations for multiple n and k values
    MOD = 10**9 + 7
    results = {}
    
    for n in n_values:
        for k in k_values:
            if k <= n * (n - 1) // 2:
                # Use DP to count permutations
                dp = [[0] * (k + 1) for _ in range(n + 1)]
                
                # Base cases
                for i in range(n + 1):
                    dp[i][0] = 1
                
                # Fill DP table
                for i in range(1, n + 1):
                    for j in range(1, min(k + 1, i * (i - 1) // 2 + 1)):
                        dp[i][j] = 0
                        for l in range(min(j + 1, i)):
                            dp[i][j] = (dp[i][j] + dp[i - 1][j - l]) % MOD
                
                results[(n, k)] = dp[n][k]
            else:
                results[(n, k)] = 0
    
    return results

# Example usage
n_values = [3, 4]
k_values = [1, 2, 3]
results = counting_permutations_multiple_values(n_values, k_values)
for (n, k), count in results.items():
    print(f"Permutations of {n} elements with {k} inversions: {count}")
```

#### **4. Counting Permutations with Statistics**
```python
def counting_permutations_with_statistics(n, k):
    # Count permutations and provide statistics
    MOD = 10**9 + 7
    
    # Count permutations using DP
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        dp[i][0] = 1
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, min(k + 1, i * (i - 1) // 2 + 1)):
            dp[i][j] = 0
            for l in range(min(j + 1, i)):
                dp[i][j] = (dp[i][j] + dp[i - 1][j - l]) % MOD
    
    total_permutations = dp[n][k]
    
    # Calculate statistics
    max_possible_inversions = n * (n - 1) // 2
    total_permutations_all = 1
    for i in range(1, n + 1):
        total_permutations_all = (total_permutations_all * i) % MOD
    
    statistics = {
        "permutations_with_k_inversions": total_permutations,
        "total_permutations": total_permutations_all,
        "max_possible_inversions": max_possible_inversions,
        "inversion_rate": k / max_possible_inversions if max_possible_inversions > 0 else 0,
        "permutation_rate": total_permutations / total_permutations_all if total_permutations_all > 0 else 0
    }
    
    return total_permutations, statistics

# Example usage
n, k = 4, 2
count, stats = counting_permutations_with_statistics(n, k)
print(f"Permutations with {k} inversions: {count}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Dynamic Programming**: Permutation DP, Counting DP
- **Combinatorics**: Permutation counting, Arrangement counting
- **Number Theory**: Modular arithmetic, Factorial calculations
- **Sorting**: Inversion counting, Merge sort

## 📚 Learning Points

### Key Takeaways
- **Dynamic programming** is essential for counting permutations efficiently
- **Combinatorics** provides the mathematical foundation for permutation counting
- **Inversion counting** is a fundamental concept in permutation analysis
- **Modular arithmetic** is crucial for handling large numbers

---

*This analysis demonstrates efficient permutation counting techniques and shows various extensions for combinatorial and modular arithmetic problems.* 