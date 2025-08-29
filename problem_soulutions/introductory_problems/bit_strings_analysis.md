---
layout: simple
title: "Bit Strings"
permalink: /problem_soulutions/introductory_problems/bit_strings_analysis
---

# Bit Strings

## Problem Description

**Problem**: Calculate the number of bit strings of length n.

**Input**: An integer n (1 ≤ n ≤ 10⁶)

**Output**: The number of bit strings modulo 10⁹+7

**Example**:
```
Input: 3
Output: 8

Explanation: The 8 possible bit strings are:
000, 001, 010, 011, 100, 101, 110, 111
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Count all possible binary strings of length n
- Each position can be either 0 or 1
- We need the result modulo 10⁹+7

**Key Observations:**
- For each position, we have 2 choices (0 or 1)
- Total combinations = 2 × 2 × 2 × ... × 2 (n times) = 2ⁿ
- We need to handle large numbers with modulo arithmetic

### Step 2: Mathematical Formula
**Idea**: Use the formula 2ⁿ directly.

**Why this works:**
- Each bit has 2 possible values
- Total combinations = 2ⁿ
- This is the most efficient approach

```python
def solve_bit_strings(n):
    MOD = 10**9 + 7
    result = pow(2, n, MOD)  # Modular exponentiation
    return result
```

**Why modular exponentiation?**
- 2ⁿ can be very large (up to 2^10^6)
- We need the result modulo 10⁹+7
- `pow(2, n, MOD)` calculates (2ⁿ) % MOD efficiently

### Step 3: Alternative - Iterative Approach
**Idea**: Calculate 2ⁿ step by step to avoid large numbers.

```python
def solve_iterative(n):
    MOD = 10**9 + 7
    result = 1
    
    for _ in range(n):
        result = (result * 2) % MOD
    
    return result
```

**Why this works:**
- Start with 1, multiply by 2 n times
- Take modulo at each step to keep numbers small
- Final result is (2ⁿ) % MOD

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_bit_strings():
    n = int(input())
    MOD = 10**9 + 7
    result = pow(2, n, MOD)
    return result

# Main execution
if __name__ == "__main__":
    result = solve_bit_strings()
    print(result)
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (1, 2),      # 2^1 = 2
        (2, 4),      # 2^2 = 4
        (3, 8),      # 2^3 = 8
        (10, 1024),  # 2^10 = 1024
    ]
    
    for n, expected in test_cases:
        result = solve_bit_strings_test(n)
        print(f"n = {n}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_bit_strings_test(n):
    MOD = 10**9 + 7
    return pow(2, n, MOD)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Mathematical Formula**: O(log n) - Modular exponentiation
- **Iterative Approach**: O(n) - Linear time

### Space Complexity
- O(1) - We only use a few variables

### Why Modular Exponentiation?
- **Efficient**: Uses binary exponentiation algorithm
- **Handles Large Numbers**: Works for n up to 10⁶
- **Built-in**: Python's `pow()` function is optimized

## 🎯 Key Insights

### 1. **Counting Principle**
- If we have k choices for each of n positions
- Total combinations = kⁿ
- For bit strings: k = 2, so total = 2ⁿ

### 2. **Modular Arithmetic**
- (a × b) % m = ((a % m) × (b % m)) % m
- This allows us to work with large numbers safely

### 3. **Binary Exponentiation**
- Calculate aⁿ in O(log n) time
- Break down exponent into binary representation
- Square the base at each step

## 🔗 Related Problems

- **[Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)**: Generate all permutations
- **[Gray Code](/cses-analyses/problem_soulutions/introductory_problems/gray_code_analysis)**: Generate bit strings with specific properties
- **[Permutations](/cses-analyses/problem_soulutions/introductory_problems/permutations_analysis)**: Count arrangements

## 🎯 Problem Variations

### Variation 1: Ternary Strings
**Problem**: Generate all strings of length n using digits 0, 1, 2.

```python
def ternary_strings(n):
    MOD = 10**9 + 7
    return pow(3, n, MOD)  # 3^n
```

### Variation 2: Binary Strings with Constraints
**Problem**: Count binary strings of length n with no consecutive 1s.

```python
def no_consecutive_ones(n):
    if n == 1:
        return 2
    if n == 2:
        return 3
    
    # Fibonacci-like sequence
    dp = [0] * (n + 1)
    dp[1] = 2  # 0, 1
    dp[2] = 3  # 00, 01, 10
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

### Variation 3: Balanced Binary Strings
**Problem**: Count binary strings of length n with equal number of 0s and 1s.

```python
def balanced_binary_strings(n):
    if n % 2 != 0:
        return 0  # Impossible for odd length
    
    from math import comb
    return comb(n, n // 2)  # Choose n/2 positions for 1s
```

## 📚 Learning Points

1. **Counting Principles**: Fundamental combinatorics
2. **Modular Arithmetic**: Essential for large number problems
3. **Binary Exponentiation**: Efficient power calculation
4. **Mathematical Formulas**: Sometimes the simplest solution is best

---

**This is a great introduction to counting problems and modular arithmetic!** 🎯 