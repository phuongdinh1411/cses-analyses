---
layout: simple
title: "Bit Strings"
permalink: /problem_soulutions/introductory_problems/bit_strings_analysis
---

# Bit Strings

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand combinatorics and counting principles for binary strings
- Apply modular arithmetic and exponentiation to calculate large numbers
- Implement efficient modular exponentiation algorithms with proper overflow handling
- Optimize counting problems using mathematical formulas and modular arithmetic
- Handle edge cases in counting problems (large n, modular arithmetic, overflow prevention)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Modular arithmetic, exponentiation, counting principles, combinatorics
- **Data Structures**: Basic arithmetic operations, modular arithmetic, overflow handling
- **Mathematical Concepts**: Combinatorics, modular arithmetic, exponentiation, binary counting
- **Programming Skills**: Modular arithmetic, exponentiation, overflow handling, algorithm implementation
- **Related Problems**: Counting problems, Modular arithmetic, Exponentiation, Combinatorics

## Problem Description

**Problem**: Calculate the number of bit strings of length n.

**Input**: An integer n (1 ≤ n ≤ 10⁶)

**Output**: The number of bit strings modulo 10⁹+7

**Constraints**:
- 1 ≤ n ≤ 10⁶
- Each bit can be either 0 or 1
- Result must be modulo 10⁹+7
- Handle large numbers efficiently
- Use modular arithmetic to prevent overflow

**Example**:
```
Input: 3
Output: 8

Explanation: The 8 possible bit strings are:
000, 001, 010, 011, 100, 101, 110, 111
```

## Visual Example

### Input and Bit String Generation
```
Input: n = 3
Output: 8

All possible bit strings of length 3:
Position:  2  1  0
String 0:  0  0  0
String 1:  0  0  1
String 2:  0  1  0
String 3:  0  1  1
String 4:  1  0  0
String 5:  1  0  1
String 6:  1  1  0
String 7:  1  1  1

Total: 8 bit strings
```

### Counting Process
```
For each position, we have 2 choices (0 or 1):

Position 0: 2 choices
Position 1: 2 choices  
Position 2: 2 choices

Total combinations = 2 × 2 × 2 = 2³ = 8
```

### Modular Arithmetic
```
Calculate 2³ modulo 10⁹+7:

2³ = 8
8 mod (10⁹+7) = 8

For larger n, we need modular exponentiation:
2^n mod (10⁹+7) = pow(2, n, 10⁹+7)
```

### Key Insight
The solution works by:
1. Using the mathematical formula 2^n for bit string counting
2. Applying modular arithmetic to handle large numbers
3. Using efficient modular exponentiation
4. Time complexity: O(log n) for modular exponentiation
5. Space complexity: O(1) for constant variables

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Generation (Inefficient)

**Key Insights from Brute Force Solution:**
- Generate all possible bit strings and count them
- Simple but computationally expensive approach
- Not suitable for large n values
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible bit strings of length n
2. Count the total number of generated strings
3. Return the count modulo 10⁹+7
4. Handle overflow with modular arithmetic

**Visual Example:**
```
Brute force: Generate all bit strings
For n = 3:
- Generate: 000, 001, 010, 011, 100, 101, 110, 111
- Count: 8 strings
- Return: 8 mod (10⁹+7) = 8
```

**Implementation:**
```python
def bit_strings_brute_force(n):
    MOD = 10**9 + 7
    
    def generate_strings(length, current=""):
        if length == 0:
            return [current]
        
        strings = []
        strings.extend(generate_strings(length - 1, current + "0"))
        strings.extend(generate_strings(length - 1, current + "1"))
        return strings
    
    all_strings = generate_strings(n)
    return len(all_strings) % MOD

def solve_bit_strings_brute_force():
    n = int(input())
    result = bit_strings_brute_force(n)
    print(result)
```

**Time Complexity:** O(2^n) for generating all bit strings
**Space Complexity:** O(2^n) for storing all bit strings

**Why it's inefficient:**
- O(2^n) time complexity is too slow for large n
- Not suitable for competitive programming with n up to 10^6
- Inefficient for large inputs
- Poor performance with exponential growth

### Approach 2: Iterative Multiplication (Better)

**Key Insights from Iterative Multiplication Solution:**
- Use iterative multiplication to calculate 2^n
- Much more efficient than brute force approach
- Standard method for modular exponentiation
- Can handle larger inputs than brute force

**Algorithm:**
1. Start with result = 1
2. Multiply by 2, n times
3. Take modulo at each step to prevent overflow
4. Return the final result

**Visual Example:**
```
Iterative multiplication for n = 3:
- Start: result = 1
- Step 1: result = (1 × 2) mod (10⁹+7) = 2
- Step 2: result = (2 × 2) mod (10⁹+7) = 4
- Step 3: result = (4 × 2) mod (10⁹+7) = 8
- Final: 8
```

**Implementation:**
```python
def bit_strings_iterative(n):
    MOD = 10**9 + 7
    result = 1
    
    for _ in range(n):
        result = (result * 2) % MOD
    
    return result

def solve_bit_strings_iterative():
    n = int(input())
    result = bit_strings_iterative(n)
    print(result)
```

**Time Complexity:** O(n) for n multiplications
**Space Complexity:** O(1) for storing variables

**Why it's better:**
- O(n) time complexity is much better than O(2^n)
- Uses iterative multiplication for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Modular Exponentiation (Optimal)

**Key Insights from Modular Exponentiation Solution:**
- Use binary exponentiation for efficient calculation
- Most efficient approach for large exponentiation
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use binary exponentiation algorithm
2. Calculate 2^n efficiently using bit manipulation
3. Apply modular arithmetic throughout
4. Return the result modulo 10⁹+7

**Visual Example:**
```
Binary exponentiation for n = 3:
- 3 in binary: 11₂ = 1×2¹ + 1×2⁰
- Step 1: result = 1, base = 2, exp = 3
- Step 2: exp is odd (3), result = 1 × 2 = 2, base = 2² = 4, exp = 1
- Step 3: exp is odd (1), result = 2 × 4 = 8, base = 4² = 16, exp = 0
- Step 4: exp is 0, stop
- Result: 2³ = 8
```

**Implementation:**
```python
def bit_strings_optimal(n):
    MOD = 10**9 + 7
    result = pow(2, n, MOD)  # Modular exponentiation
    return result

def solve_bit_strings():
    n = int(input())
    result = bit_strings_optimal(n)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_bit_strings()
```

**Time Complexity:** O(log n) for binary exponentiation
**Space Complexity:** O(1) for storing variables

**Why it's optimal:**
- O(log n) time complexity is optimal for exponentiation
- Uses binary exponentiation for efficient calculation
- Most efficient approach for competitive programming
- Standard method for modular exponentiation

## 🎯 Problem Variations

### Variation 1: Bit Strings with Constraints
**Problem**: Count bit strings with specific constraints (e.g., no consecutive 1s).

**Link**: [CSES Problem Set - Bit Strings Constraints](https://cses.fi/problemset/task/bit_strings_constraints)

```python
def bit_strings_constraints(n, constraints):
    MOD = 10**9 + 7
    
    def count_valid_strings(length, last_bit, memo):
        if length == 0:
            return 1
        
        if (length, last_bit) in memo:
            return memo[(length, last_bit)]
        
        count = 0
        if constraints.get('no_consecutive_1s', False) and last_bit == 1:
            count = count_valid_strings(length - 1, 0, memo)
        else:
            count = (count_valid_strings(length - 1, 0, memo) + 
                    count_valid_strings(length - 1, 1, memo)) % MOD
        
        memo[(length, last_bit)] = count
        return count
    
    memo = {}
    return count_valid_strings(n, -1, memo)
```

### Variation 2: Bit Strings with Minimum/Maximum 1s
**Problem**: Count bit strings with minimum or maximum number of 1s.

**Link**: [CSES Problem Set - Bit Strings Min Max](https://cses.fi/problemset/task/bit_strings_min_max)

```python
def bit_strings_min_max(n, min_ones, max_ones):
    MOD = 10**9 + 7
    
    def count_strings(length, ones_count, memo):
        if length == 0:
            return 1 if min_ones <= ones_count <= max_ones else 0
        
        if (length, ones_count) in memo:
            return memo[(length, ones_count)]
        
        count = 0
        # Add 0
        count = (count + count_strings(length - 1, ones_count, memo)) % MOD
        # Add 1
        count = (count + count_strings(length - 1, ones_count + 1, memo)) % MOD
        
        memo[(length, ones_count)] = count
        return count
    
    memo = {}
    return count_strings(n, 0, memo)
```

### Variation 3: Bit Strings with Pattern Constraints
**Problem**: Count bit strings that avoid specific patterns.

**Link**: [CSES Problem Set - Bit Strings Patterns](https://cses.fi/problemset/task/bit_strings_patterns)

```python
def bit_strings_patterns(n, forbidden_patterns):
    MOD = 10**9 + 7
    
    def count_strings(length, current_suffix, memo):
        if length == 0:
            return 1
        
        if (length, current_suffix) in memo:
            return memo[(length, current_suffix)]
        
        count = 0
        for bit in ['0', '1']:
            new_suffix = current_suffix + bit
            if len(new_suffix) > max(len(pattern) for pattern in forbidden_patterns):
                new_suffix = new_suffix[-max(len(pattern) for pattern in forbidden_patterns):]
            
            if not any(pattern in new_suffix for pattern in forbidden_patterns):
                count = (count + count_strings(length - 1, new_suffix, memo)) % MOD
        
        memo[(length, current_suffix)] = count
        return count
    
    memo = {}
    return count_strings(n, "", memo)
```

## 🔗 Related Problems

- **[Counting Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Counting problems
- **[Modular Arithmetic](/cses-analyses/problem_soulutions/introductory_problems/)**: Modular arithmetic problems
- **[Exponentiation](/cses-analyses/problem_soulutions/introductory_problems/)**: Exponentiation problems
- **[Combinatorics](/cses-analyses/problem_soulutions/introductory_problems/)**: Combinatorics problems

## 📚 Learning Points

1. **Combinatorics**: Essential for understanding counting principles
2. **Modular Arithmetic**: Key technique for handling large numbers
3. **Exponentiation**: Important for understanding power calculations
4. **Binary Counting**: Critical for understanding bit string problems
5. **Mathematical Formulas**: Foundation for many counting algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Bit Strings problem demonstrates fundamental combinatorics concepts for counting binary strings. We explored three approaches:

1. **Brute Force Generation**: O(2^n) time complexity using recursive generation of all bit strings, inefficient for large n
2. **Iterative Multiplication**: O(n) time complexity using iterative multiplication with modular arithmetic, better approach for counting problems
3. **Modular Exponentiation**: O(log n) time complexity with binary exponentiation, optimal approach for large exponentiation

The key insights include understanding combinatorics principles, using modular arithmetic for efficient large number handling, and applying binary exponentiation techniques for optimal performance. This problem serves as an excellent introduction to counting problems and modular arithmetic algorithms.
