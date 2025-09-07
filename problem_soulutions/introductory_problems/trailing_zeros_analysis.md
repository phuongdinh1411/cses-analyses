---
layout: simple
title: "Trailing Zeros"
permalink: /problem_soulutions/introductory_problems/trailing_zeros_analysis
---

# Trailing Zeros

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand factorial properties and trailing zero counting concepts
- Apply mathematical formulas to count trailing zeros without computing large factorials
- Implement efficient trailing zero counting algorithms with proper mathematical calculations
- Optimize trailing zero counting using mathematical analysis and prime factorization
- Handle edge cases in factorial problems (large n, mathematical precision, overflow prevention)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Factorial properties, trailing zero counting, mathematical formulas, prime factorization
- **Data Structures**: Mathematical calculations, prime tracking, factorization tracking, mathematical operations
- **Mathematical Concepts**: Factorial theory, prime factorization, trailing zero mathematics, mathematical analysis
- **Programming Skills**: Mathematical calculations, prime factorization, trailing zero counting, algorithm implementation
- **Related Problems**: Factorial problems, Mathematical formulas, Prime factorization, Trailing zero problems

## Problem Description

**Problem**: Calculate the number of trailing zeros in n! (n factorial).

**Input**: An integer n (1 ≤ n ≤ 10⁹)

**Output**: The number of trailing zeros in n!.

**Example**:
```
Input: 20

Output: 4

Explanation: 20! = 2432902008176640000 has 4 trailing zeros.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Calculate n! (n factorial)
- Count the number of trailing zeros
- Handle very large values of n efficiently

**Key Observations:**
- Trailing zeros come from factors of 10
- 10 = 2 × 5, so we need pairs of 2 and 5
- In factorial, there are always more factors of 2 than 5
- So we only need to count factors of 5

### Step 2: Brute Force Approach
**Idea**: Calculate n! and count trailing zeros directly.

```python
def trailing_zeros_brute_force(n):
    # Calculate factorial
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    
    # Count trailing zeros
    count = 0
    while factorial % 10 == 0:
        count += 1
        factorial //= 10
    
    return count
```

**Why this doesn't work:**
- For large n, factorial becomes extremely large
- Causes integer overflow
- Completely impractical for n up to 10⁹

### Step 3: Mathematical Analysis
**Idea**: Count factors of 5 without calculating factorial.

```python
def trailing_zeros_math(n):
    # Count factors of 5 (since 2s are more abundant)
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    return count
```

**Why this works:**
- Trailing zeros come from factors of 10 = 2 × 5
- In factorial, there are always more factors of 2 than 5
- So we only need to count factors of 5
- We count multiples of 5, 25, 125, etc.

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_trailing_zeros():
    n = int(input())
    
    # Count factors of 5
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    print(count)

# Main execution
if __name__ == "__main__":
    solve_trailing_zeros()
```

**Why this works:**
- Efficient mathematical approach
- Handles large values of n correctly
- Counts all factors of 5 in factorial

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (5, 1),    # 5! = 120 has 1 trailing zero
        (10, 2),   # 10! = 3628800 has 2 trailing zeros
        (20, 4),   # 20! has 4 trailing zeros
        (25, 6),   # 25! has 6 trailing zeros (extra from 25)
    ]
    
    for n, expected in test_cases:
        result = solve_test(n)
        print(f"n = {n}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n):
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    return count

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(log n) - we iterate through powers of 5
- **Space**: O(1) - constant space

### Why This Solution Works
- **Mathematical**: Uses mathematical properties of factorial
- **Efficient**: Logarithmic time complexity
- **Correct**: Counts all factors of 5 accurately

## 🎨 Visual Example

### Input Example
```
Input: n = 20
Output: 4 (20! has 4 trailing zeros)
```

### Factorial Calculation
```
20! = 20 × 19 × 18 × ... × 2 × 1
20! = 2432902008176640000
Trailing zeros: 4
```

### Factor Analysis
```
Numbers 1 to 20:
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20

Factors of 2: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20
- 2: 1 factor of 2
- 4: 2 factors of 2  
- 6: 1 factor of 2
- 8: 3 factors of 2
- 10: 1 factor of 2
- 12: 2 factors of 2
- 14: 1 factor of 2
- 16: 4 factors of 2
- 18: 1 factor of 2
- 20: 2 factors of 2
Total factors of 2: 1+2+1+3+1+2+1+4+1+2 = 18

Factors of 5: 5, 10, 15, 20
- 5: 1 factor of 5
- 10: 1 factor of 5
- 15: 1 factor of 5  
- 20: 1 factor of 5
Total factors of 5: 4

Trailing zeros = min(18, 4) = 4
```

### Mathematical Formula Application
```
For n = 20:
Factors of 5 = ⌊20/5⌋ + ⌊20/25⌋ + ⌊20/125⌋ + ...
Factors of 5 = ⌊4⌋ + ⌊0.8⌋ + ⌊0.16⌋ + ...
Factors of 5 = 4 + 0 + 0 + ... = 4

Factors of 2 = ⌊20/2⌋ + ⌊20/4⌋ + ⌊20/8⌋ + ⌊20/16⌋ + ...
Factors of 2 = ⌊10⌋ + ⌊5⌋ + ⌊2.5⌋ + ⌊1.25⌋ + ...
Factors of 2 = 10 + 5 + 2 + 1 + 0 + ... = 18

Trailing zeros = min(18, 4) = 4
```

### Step-by-Step Process
```
Step 1: Count multiples of 5
Numbers divisible by 5: 5, 10, 15, 20
Count: 4

Step 2: Count multiples of 25
Numbers divisible by 25: none (25 > 20)
Count: 0

Step 3: Count multiples of 125
Numbers divisible by 125: none (125 > 20)
Count: 0

Total factors of 5: 4 + 0 + 0 = 4
```

### Different Examples
```
n=5: 5! = 120 → 1 trailing zero
Factors of 5: ⌊5/5⌋ = 1

n=10: 10! = 3628800 → 2 trailing zeros  
Factors of 5: ⌊10/5⌋ = 2

n=25: 25! → 6 trailing zeros
Factors of 5: ⌊25/5⌋ + ⌊25/25⌋ = 5 + 1 = 6

n=100: 100! → 24 trailing zeros
Factors of 5: ⌊100/5⌋ + ⌊100/25⌋ = 20 + 4 = 24
```

### Why Only Count Factors of 5
```
In any factorial n!:
- There are always more factors of 2 than 5
- 10 = 2 × 5, so each trailing zero needs one 2 and one 5
- Since 2s are abundant, the limiting factor is 5s
- Therefore, trailing zeros = number of factors of 5
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Mathematical    │ O(log n)     │ O(1)         │ Count        │
│ Formula         │              │              │ factors of 5 │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n)         │ O(1)         │ Calculate    │
│                 │              │              │ factorial    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Prime           │ O(n)         │ O(1)         │ Factor       │
│ Factorization   │              │              │ each number  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Trailing Zeros Source**
- Trailing zeros come from factors of 10
- 10 = 2 × 5, so we need pairs of 2 and 5
- In factorial, there are always more factors of 2 than 5

### 2. **Counting Factors of 5**
- Count multiples of 5: n // 5
- Count multiples of 25: n // 25
- Count multiples of 125: n // 125
- And so on...

### 3. **Mathematical Formula**
- Total factors of 5 = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ...
- This gives us the exact number of trailing zeros

## 🎯 Problem Variations

### Variation 1: Trailing Zeros in Product
**Problem**: Find trailing zeros in product of numbers from a to b.

```python
def trailing_zeros_product(a, b):
    # Count factors of 5 in range [a, b]
    def count_factors_5(n):
        count = 0
        power = 5
        while power <= n:
            count += n // power
            power *= 5
        return count
    
    # Use inclusion-exclusion
    return count_factors_5(b) - count_factors_5(a - 1)
```

### Variation 2: Trailing Zeros in Different Bases
**Problem**: Find trailing zeros in n! when written in base k.

```python
def trailing_zeros_base_k(n, k):
    # Factorize k into prime factors
    def factorize(k):
        factors = {}
        d = 2
        while d * d <= k:
            while k % d == 0:
                factors[d] = factors.get(d, 0) + 1
                k //= d
            d += 1
        if k > 1:
            factors[k] = factors.get(k, 0) + 1
        return factors
    
    factors = factorize(k)
    min_zeros = float('inf')
    
    for prime, power in factors.items():
        # Count factors of prime in n!
        count = 0
        p = prime
        while p <= n:
            count += n // p
            p *= prime
        
        # Number of complete sets of this prime
        zeros = count // power
        min_zeros = min(min_zeros, zeros)
    
    return min_zeros
```

### Variation 3: Trailing Zeros in Sum
**Problem**: Find trailing zeros in sum of factorials.

```python
def trailing_zeros_sum_factorials(n):
    # Sum = 1! + 2! + 3! + ... + n!
    # For large n, most terms contribute no trailing zeros
    # Only need to consider terms up to a certain point
    
    total_zeros = 0
    for i in range(1, min(n + 1, 25)):  # 25! has many trailing zeros
        # Count trailing zeros in i!
        count = 0
        power = 5
        while power <= i:
            count += i // power
            power *= 5
        total_zeros += count
    
    return total_zeros
```

### Variation 4: Trailing Zeros in Binary
**Problem**: Find trailing zeros in binary representation of n!.

```python
def trailing_zeros_binary(n):
    # Count factors of 2 in n!
    count = 0
    power = 2
    
    while power <= n:
        count += n // power
        power *= 2
    
    return count
```

### Variation 5: Trailing Zeros with Constraints
**Problem**: Find trailing zeros in n! where n has certain constraints.

```python
def trailing_zeros_constrained(n, constraints):
    # constraints is a list of forbidden numbers
    # We need to calculate factorial excluding these numbers
    
    def factorial_without_constraints(n, constraints):
        result = 1
        for i in range(1, n + 1):
            if i not in constraints:
                result *= i
        return result
    
    # For small n, we can calculate directly
    if n <= 20:
        factorial = factorial_without_constraints(n, constraints)
        count = 0
        while factorial % 10 == 0:
            count += 1
            factorial //= 10
        return count
    
    # For large n, use mathematical approach
    # This is more complex and depends on the specific constraints
    pass
```

## 🔗 Related Problems

- **[Missing Number](/cses-analyses/problem_soulutions/introductory_problems/missing_number_analysis)**: Mathematical problems
- **[Digit Queries](/cses-analyses/problem_soulutions/introductory_problems/digit_queries_analysis)**: Number sequence problems
- **[Bit Strings](/cses-analyses/problem_soulutions/introductory_problems/bit_strings_analysis)**: Counting problems

## 📚 Learning Points

1. **Mathematical Analysis**: Understanding factorial properties
2. **Prime Factorization**: Working with prime factors
3. **Efficient Counting**: Avoiding brute force calculations
4. **Mathematical Formulas**: Using mathematical properties for optimization

---

**This is a great introduction to mathematical analysis and efficient counting problems!** 🎯 