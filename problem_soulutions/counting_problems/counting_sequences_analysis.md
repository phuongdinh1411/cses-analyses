---
layout: simple
title: "Counting Sequences"
permalink: /problem_soulutions/counting_problems/counting_sequences_analysis
---


# Counting Sequences

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand sequence counting with constraints and consecutive element restrictions
- [ ] **Objective 2**: Apply dynamic programming to count valid sequences with constraints
- [ ] **Objective 3**: Implement efficient DP algorithms for sequence counting problems
- [ ] **Objective 4**: Optimize sequence counting using mathematical formulas and DP optimization
- [ ] **Objective 5**: Handle large sequence counts using modular arithmetic and space optimization

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, sequence algorithms, constraint handling, combinatorics
- **Data Structures**: Arrays, DP tables, sequence data structures
- **Mathematical Concepts**: Sequences, combinatorics, modular arithmetic, constraint counting
- **Programming Skills**: Dynamic programming implementation, sequence generation, modular arithmetic
- **Related Problems**: Counting Combinations (counting problems), Dice Combinations (DP counting), Coin Combinations I (DP with constraints)

## 📋 Problem Description

Given integers n and k, count the number of sequences of length n where each element is between 1 and k, and no two consecutive elements are equal.

This is a combinatorics problem where we need to count valid sequences with the constraint that no two consecutive elements can be the same. We can solve this using dynamic programming by tracking the last element of the sequence.

**Input**: 
- First line: two integers n and k (sequence length and maximum value)

**Output**: 
- Print the number of valid sequences modulo 10⁹ + 7

**Constraints**:
- 1 ≤ n ≤ 10⁶
- 1 ≤ k ≤ 10⁶

**Example**:
```
Input:
3 2

Output:
2
```

**Explanation**: 
For n = 3 and k = 2, there are 2 valid sequences:
1. [1, 2, 1] - no consecutive elements are equal
2. [2, 1, 2] - no consecutive elements are equal

The sequences [1, 1, 2], [1, 2, 2], [2, 1, 1], and [2, 2, 1] are invalid because they have consecutive equal elements.

### 📊 Visual Example

**All Possible Sequences for n=3, k=2:**
```
Total possible sequences: 2³ = 8

Sequence 1: [1, 1, 1]
Consecutive check: 1=1, 1=1 ✗
Status: Invalid (consecutive 1s)

Sequence 2: [1, 1, 2]
Consecutive check: 1=1 ✗
Status: Invalid (consecutive 1s)

Sequence 3: [1, 2, 1]
Consecutive check: 1≠2, 2≠1 ✓
Status: Valid ✓

Sequence 4: [1, 2, 2]
Consecutive check: 1≠2, 2=2 ✗
Status: Invalid (consecutive 2s)

Sequence 5: [2, 1, 1]
Consecutive check: 2≠1, 1=1 ✗
Status: Invalid (consecutive 1s)

Sequence 6: [2, 1, 2]
Consecutive check: 2≠1, 1≠2 ✓
Status: Valid ✓

Sequence 7: [2, 2, 1]
Consecutive check: 2=2 ✗
Status: Invalid (consecutive 2s)

Sequence 8: [2, 2, 2]
Consecutive check: 2=2, 2=2 ✗
Status: Invalid (consecutive 2s)
```

**Valid Sequences Analysis:**
```
Valid sequences: 2 out of 8

┌─────────────────────────────────────┐
│ [1, 2, 1]:                         │
│ - Position 0: 1                    │
│ - Position 1: 2 (≠ 1) ✓            │
│ - Position 2: 1 (≠ 2) ✓            │
│ - No consecutive equal elements     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ [2, 1, 2]:                         │
│ - Position 0: 2                    │
│ - Position 1: 1 (≠ 2) ✓            │
│ - Position 2: 2 (≠ 1) ✓            │
│ - No consecutive equal elements     │
└─────────────────────────────────────┘
```

**Dynamic Programming Approach:**
```
State: dp[i][j] = number of valid sequences of length i ending with j

Base case:
dp[1][j] = 1 for all j from 1 to k

Recurrence:
dp[i][j] = Σ(dp[i-1][l]) for all l ≠ j

Explanation: To form a sequence of length i ending with j,
we can append j to any valid sequence of length i-1 that doesn't end with j.
```

**DP Table for n=3, k=2:**
```
     j=1  j=2
i=1:  1    1
i=2:  1    1
i=3:  1    1

Total: dp[3][1] + dp[3][2] = 1 + 1 = 2
```

**DP State Transitions:**
```
For i=2:
┌─────────────────────────────────────┐
│ dp[2][1] = dp[1][2] = 1            │
│ (Append 1 to sequences ending with 2)│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ dp[2][2] = dp[1][1] = 1            │
│ (Append 2 to sequences ending with 1)│
└─────────────────────────────────────┘

For i=3:
┌─────────────────────────────────────┐
│ dp[3][1] = dp[2][2] = 1            │
│ (Append 1 to sequences ending with 2)│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ dp[3][2] = dp[2][1] = 1            │
│ (Append 2 to sequences ending with 1)│
└─────────────────────────────────────┘
```

**Optimized DP Formula:**
```
Let total[i] = total number of valid sequences of length i
total[i] = dp[i][1] + dp[i][2] + ... + dp[i][k]

For each j:
dp[i][j] = total[i-1] - dp[i-1][j]

This gives us:
dp[i][j] = (k-1) * total[i-1] / k

Final answer: total[n] = k * (k-1)^(n-1)
```

**Mathematical Formula:**
```
For n=3, k=2:
total[3] = 2 * (2-1)^(3-1) = 2 * 1² = 2

General formula:
total[n] = k * (k-1)^(n-1)

Explanation:
- First element: k choices
- Each subsequent element: (k-1) choices (cannot be same as previous)
- Total: k * (k-1)^(n-1)
```

**Algorithm Flowchart:**
```
┌─────────────────────────────────────┐
│ Start: Read n and k                 │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ If n == 1: return k                 │
│ Else: return k * (k-1)^(n-1)        │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return result modulo 10^9 + 7       │
└─────────────────────────────────────┘
```

**Key Insight Visualization:**
```
For any valid sequence of length i-1:
┌─────────────────────────────────────┐
│ [a₁, a₂, ..., aᵢ₋₁]                │
│ Last element: aᵢ₋₁                  │
│ Next element can be: any value ≠ aᵢ₋₁│
│ Choices: k - 1                      │
└─────────────────────────────────────┘

Example with k=3:
┌─────────────────────────────────────┐
│ [1, 2, 1] (valid sequence)         │
│ Last element: 1                     │
│ Next element: 2 or 3 (not 1)        │
│ New sequences: [1,2,1,2], [1,2,1,3]│
└─────────────────────────────────────┘
```

## Solution Progression

### Approach 1: Brute Force Generation - O(k^n)
**Description**: Generate all possible sequences and count valid ones.

```python
def counting_sequences_naive(n, k):
    MOD = 10**9 + 7
    
    def generate_sequences(length, prev):
        if length == 0:
            return 1
        
        count = 0
        for i in range(1, k + 1):
            if i != prev:
                count = (count + generate_sequences(length - 1, i)) % MOD
        
        return count
    
    return generate_sequences(n, -1)
```

**Why this is inefficient**: O(k^n) complexity is too slow for large n and k.

### Improvement 1: Dynamic Programming - O(nk)
**Description**: Use DP to avoid recalculating subproblems.

```python
def counting_sequences_dp(n, k):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of sequences of length i ending with j
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: sequences of length 1
    for j in range(1, k + 1):
        dp[1][j] = 1
    
    # Fill DP table
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            # Sum all previous values except j
            for prev in range(1, k + 1):
                if prev != j:
                    dp[i][j] = (dp[i][j] + dp[i-1][prev]) % MOD
    
    # Sum all sequences of length n
    result = 0
    for j in range(1, k + 1):
        result = (result + dp[n][j]) % MOD
    
    return result
```

**Why this improvement works**: DP avoids recalculating subproblems, reducing complexity to O(nk).

### Approach 2: Optimized DP - O(nk)
**Description**: Optimize DP by precomputing sums.

```python
def counting_sequences_optimized(n, k):
    MOD = 10**9 + 7
    
    # dp[i][j] = number of sequences of length i ending with j
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: sequences of length 1
    for j in range(1, k + 1):
        dp[1][j] = 1
    
    # Fill DP table with optimization
    for i in range(2, n + 1):
        # Calculate sum of all previous values
        total_prev = sum(dp[i-1][j] for j in range(1, k + 1)) % MOD
        
        for j in range(1, k + 1):
            # dp[i][j] = total_prev - dp[i-1][j]
            dp[i][j] = (total_prev - dp[i-1][j]) % MOD
    
    # Sum all sequences of length n
    result = sum(dp[n][j] for j in range(1, k + 1)) % MOD
    
    return result
```

**Why this improvement works**: Precomputing sums reduces inner loop complexity.

### Approach 3: Mathematical Formula - O(n)
**Description**: Use mathematical formula for the solution.

```python
def counting_sequences_mathematical(n, k):
    MOD = 10**9 + 7
    
    if n == 1:
        return k
    
    # Formula: k * (k-1)^(n-1)
    result = k
    for _ in range(n - 1):
        result = (result * (k - 1)) % MOD
    
    return result
```

**Why this improvement works**: Mathematical formula gives O(n) solution.

## Final Optimal Solution

```python
n, k = map(int, input().split())

def count_sequences(n, k):
    MOD = 10**9 + 7
    
    if n == 1:
        return k
    
    # Formula: k * (k-1)^(n-1)
    result = k
    for _ in range(n - 1):
        result = (result * (k - 1)) % MOD
    
    return result

result = count_sequences(n, k)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force Generation | O(k^n) | O(n) | Simple but exponential |
| Dynamic Programming | O(nk) | O(nk) | DP avoids recalculation |
| Optimized DP | O(nk) | O(nk) | Precomputed sums |
| Mathematical Formula | O(n) | O(1) | Optimal solution |

## Key Insights for Other Problems

### 1. **Sequence Counting with Constraints**
**Principle**: When counting sequences with constraints, look for mathematical patterns.
**Applicable to**: Sequence counting problems, constraint satisfaction problems, combinatorics problems

### 2. **Dynamic Programming for Sequences**
**Principle**: DP can efficiently count sequences by building solutions incrementally.
**Applicable to**: Sequence problems, counting problems, DP problems

### 3. **Mathematical Formula Derivation**
**Principle**: Many counting problems have closed-form mathematical solutions.
**Applicable to**: Combinatorics problems, mathematical counting problems

## Notable Techniques

### 1. **Dynamic Programming for Sequences**
```python
def dp_sequence_counting(n, k, MOD):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case
    for j in range(1, k + 1):
        dp[1][j] = 1
    
    # Fill DP table
    for i in range(2, n + 1):
        total_prev = sum(dp[i-1][j] for j in range(1, k + 1)) % MOD
        for j in range(1, k + 1):
            dp[i][j] = (total_prev - dp[i-1][j]) % MOD
    
    return sum(dp[n][j] for j in range(1, k + 1)) % MOD
```

### 2. **Mathematical Formula**
```python
def mathematical_sequence_counting(n, k, MOD):
    if n == 1:
        return k
    
    result = k
    for _ in range(n - 1):
        result = (result * (k - 1)) % MOD
    
    return result
```

### 3. **Modular Arithmetic**
```python
def modular_sequence_counting(n, k, MOD):
    if n == 1:
        return k % MOD
    
    # Use fast exponentiation for large n
    result = k
    power = pow(k - 1, n - 1, MOD)
    result = (result * power) % MOD
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a sequence counting problem with constraints
2. **Choose approach**: Use mathematical formula for optimal solution
3. **Handle base case**: n = 1 case
4. **Apply formula**: k * (k-1)^(n-1)
5. **Use modular arithmetic**: Handle large numbers
6. **Return result**: Output the count modulo 10^9 + 7

---

*This analysis shows how to efficiently count sequences using dynamic programming with state tracking and memoization.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Sequences**
**Problem**: Each element has a weight. Find sequences with total weight equal to target.
```python
def weighted_sequences(n, target, weights, MOD=10**9+7):
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

#### **Variation 2: Constrained Sequences**
**Problem**: Find sequences with constraints on element selection.
```python
def constrained_sequences(n, k, constraints, MOD=10**9+7):
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

#### **Variation 3: Ordered Sequences**
**Problem**: Count sequences where order matters (permutations with repetition).
```python
def ordered_sequences(n, k, MOD=10**9+7):
    # Count ordered sequences of k elements from n
    if k > n:
        return 0
    
    # Use formula: n^k
    result = 1
    for _ in range(k):
        result = (result * n) % MOD
    
    return result
```

#### **Variation 4: Circular Sequences**
**Problem**: Count sequences in a circular arrangement.
```python
def circular_sequences(n, k, MOD=10**9+7):
    # Count circular sequences of k elements from n
    if k == 0:
        return 1
    if k == 1:
        return n
    if k > n:
        return 0
    
    # For circular sequences, we need to handle wrap-around
    # Use inclusion-exclusion principle
    result = 0
    
    # Count linear sequences
    linear = ordered_sequences(n, k, MOD)
    
    # Subtract sequences that wrap around
    if k > 1:
        # Count sequences that start and end at adjacent positions
        wrap_around = ordered_sequences(n - k + 1, k - 1, MOD)
        result = (linear - wrap_around) % MOD
    else:
        result = linear
    
    return result
```

#### **Variation 5: Dynamic Sequence Updates**
**Problem**: Support dynamic updates to constraints and answer sequence queries efficiently.
```python
class DynamicSequenceCounter:
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
    
    def count_sequences(self, k):
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

#### **1. Sequence Problems**
- **Sequence Counting**: Count sequences efficiently
- **Sequence Generation**: Generate sequences
- **Sequence Optimization**: Optimize sequence algorithms
- **Sequence Analysis**: Analyze sequence properties

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
    
    result = count_sequences(n, k)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute sequences for different ranges
def precompute_sequences(max_n, max_k, MOD=10**9+7):
    dp = [[0] * (max_k + 1) for _ in range(max_n + 1)]
    
    # Base case
    for i in range(max_n + 1):
        dp[i][0] = 1
    
    # Fill DP table
    for i in range(1, max_n + 1):
        for j in range(1, max_k + 1):
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
# Interactive sequence calculator
def interactive_sequence_calculator():
    MOD = 10**9 + 7
    
    while True:
        query = input("Enter query (sequences/weighted/constrained/ordered/circular/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "sequences":
            n, k = map(int, input("Enter n and k: ").split())
            result = count_sequences(n, k)
            print(f"S({n},{k}) = {result}")
        elif query == "weighted":
            n = int(input("Enter n: "))
            target = int(input("Enter target weight: "))
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_sequences(n, target, weights)
            print(f"Weighted sequences: {result}")
        elif query == "constrained":
            n, k = map(int, input("Enter n and k: ").split())
            constraints = list(map(int, input("Enter constraints: ").split()))
            result = constrained_sequences(n, k, constraints)
            print(f"Constrained sequences: {result}")
        elif query == "ordered":
            n, k = map(int, input("Enter n and k: ").split())
            result = ordered_sequences(n, k)
            print(f"Ordered sequences: {result}")
        elif query == "circular":
            n, k = map(int, input("Enter n and k: ").split())
            result = circular_sequences(n, k)
            print(f"Circular sequences: {result}")
        elif query == "dynamic":
            n = int(input("Enter n: "))
            counter = DynamicSequenceCounter(n)
            
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
                    result = counter.count_sequences(k)
                    print(f"Sequences: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Sequence Theory**: Mathematical theory of sequences
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

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n × k) for the DP approach
- **Space Complexity**: O(k) for storing DP states
- **Why it works**: We use dynamic programming to count sequences by tracking the last element and avoiding consecutive equal elements

### Key Implementation Points
- Use dynamic programming with state representing the last element
- For each position, count sequences ending with each possible value
- Ensure no two consecutive elements are equal
- Use modular arithmetic to prevent overflow

## 🎯 Key Insights

### Important Concepts and Patterns
- **Dynamic Programming**: Essential for counting sequences with constraints
- **State Tracking**: Track the last element to avoid consecutive equal elements
- **Modular Arithmetic**: Required for handling large numbers
- **Combinatorics**: Foundation for counting problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Counting Sequences with Additional Constraints**
```python
def counting_sequences_with_constraints(n, k, constraints):
    # Count sequences with additional constraints
    MOD = 10**9 + 7
    
    # Check constraints
    if constraints.get("min_length", 1) > n:
        return 0
    if constraints.get("max_length", float('inf')) < n:
        return 0
    if constraints.get("min_value", 1) > 1:
        return 0
    if constraints.get("max_value", k) < k:
        k = constraints["max_value"]
    
    # DP: dp[i][j] = number of sequences of length i ending with j
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: sequences of length 1
    for j in range(1, k + 1):
        dp[1][j] = 1
    
    # Fill DP table
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            # Sum all sequences of length i-1 that don't end with j
            for prev_j in range(1, k + 1):
                if prev_j != j:
                    dp[i][j] = (dp[i][j] + dp[i-1][prev_j]) % MOD
    
    # Sum all sequences of length n
    result = 0
    for j in range(1, k + 1):
        result = (result + dp[n][j]) % MOD
    
    return result

# Example usage
n, k = 3, 2
constraints = {"min_length": 1, "max_length": 10, "min_value": 1, "max_value": 2}
result = counting_sequences_with_constraints(n, k, constraints)
print(f"Constrained sequence count: {result}")
```

#### **2. Counting Sequences with Forbidden Patterns**
```python
def counting_sequences_with_forbidden_patterns(n, k, forbidden_patterns):
    # Count sequences avoiding forbidden patterns
    MOD = 10**9 + 7
    
    # DP: dp[i][j] = number of sequences of length i ending with j
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: sequences of length 1
    for j in range(1, k + 1):
        dp[1][j] = 1
    
    # Fill DP table
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            # Sum all sequences of length i-1 that don't end with j
            for prev_j in range(1, k + 1):
                if prev_j != j:
                    # Check if this transition creates a forbidden pattern
                    is_forbidden = False
                    for pattern in forbidden_patterns:
                        if len(pattern) == 2 and pattern[0] == prev_j and pattern[1] == j:
                            is_forbidden = True
                            break
                    
                    if not is_forbidden:
                        dp[i][j] = (dp[i][j] + dp[i-1][prev_j]) % MOD
    
    # Sum all sequences of length n
    result = 0
    for j in range(1, k + 1):
        result = (result + dp[n][j]) % MOD
    
    return result

# Example usage
n, k = 3, 2
forbidden_patterns = [[1, 2]]  # Forbid the pattern 1,2
result = counting_sequences_with_forbidden_patterns(n, k, forbidden_patterns)
print(f"Sequence count avoiding forbidden patterns: {result}")
```

#### **3. Counting Sequences with Multiple Lengths**
```python
def counting_sequences_multiple_lengths(lengths, k):
    # Count sequences for multiple lengths
    MOD = 10**9 + 7
    results = {}
    
    max_length = max(lengths)
    
    # DP: dp[i][j] = number of sequences of length i ending with j
    dp = [[0] * (k + 1) for _ in range(max_length + 1)]
    
    # Base case: sequences of length 1
    for j in range(1, k + 1):
        dp[1][j] = 1
    
    # Fill DP table
    for i in range(2, max_length + 1):
        for j in range(1, k + 1):
            # Sum all sequences of length i-1 that don't end with j
            for prev_j in range(1, k + 1):
                if prev_j != j:
                    dp[i][j] = (dp[i][j] + dp[i-1][prev_j]) % MOD
    
    # Calculate results for each length
    for n in lengths:
        result = 0
        for j in range(1, k + 1):
            result = (result + dp[n][j]) % MOD
        results[n] = result
    
    return results

# Example usage
lengths = [1, 2, 3, 4]
k = 2
results = counting_sequences_multiple_lengths(lengths, k)
for n, count in results.items():
    print(f"Sequences of length {n}: {count}")
```

#### **4. Counting Sequences with Statistics**
```python
def counting_sequences_with_statistics(n, k):
    # Count sequences and provide statistics
    MOD = 10**9 + 7
    
    # DP: dp[i][j] = number of sequences of length i ending with j
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: sequences of length 1
    for j in range(1, k + 1):
        dp[1][j] = 1
    
    # Fill DP table
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            # Sum all sequences of length i-1 that don't end with j
            for prev_j in range(1, k + 1):
                if prev_j != j:
                    dp[i][j] = (dp[i][j] + dp[i-1][prev_j]) % MOD
    
    # Calculate total count
    total_count = 0
    for j in range(1, k + 1):
        total_count = (total_count + dp[n][j]) % MOD
    
    # Calculate statistics
    ending_counts = {}
    for j in range(1, k + 1):
        ending_counts[j] = dp[n][j]
    
    statistics = {
        "total_sequences": total_count,
        "sequence_length": n,
        "max_value": k,
        "ending_distribution": ending_counts,
        "most_common_ending": max(ending_counts, key=ending_counts.get) if ending_counts else None
    }
    
    return total_count, statistics

# Example usage
n, k = 3, 2
count, stats = counting_sequences_with_statistics(n, k)
print(f"Sequence count: {count}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Dynamic Programming**: Sequence DP, State DP
- **Combinatorics**: Permutation counting, Arrangement counting
- **Modular Arithmetic**: Modular exponentiation, Modular inverses
- **Counting Problems**: Subset counting, Path counting

## 📚 Learning Points

### Key Takeaways
- **Dynamic programming** is essential for counting sequences with constraints
- **State tracking** helps avoid consecutive equal elements
- **Modular arithmetic** is required for handling large numbers
- **Combinatorics** provides the mathematical foundation for counting problems

---

*This analysis demonstrates efficient sequence counting techniques and shows various extensions for combinatorial and modular arithmetic problems.* 