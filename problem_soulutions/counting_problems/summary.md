---
layout: simple
title: "Counting Problems Summary"
permalink: /problem_soulutions/counting_problems/summary
---

# Counting Problems

Welcome to the Counting Problems section! This category covers combinatorics and mathematical counting techniques for solving complex enumeration problems.

## Key Concepts & Techniques

### Combinatorial Principles

#### Addition Principle
- **When to use**: Counting disjoint cases that don't overlap
- **Formula**: If A and B are disjoint, |A ∪ B| = |A| + |B|
- **Example**: Count ways to choose red OR blue balls
- **Implementation**: Sum the counts of each case

#### Multiplication Principle
- **When to use**: Counting independent choices made sequentially
- **Formula**: If choices are independent, total = choice1 × choice2 × ...
- **Example**: Count ways to choose shirt AND pants AND shoes
- **Implementation**: Multiply the counts of each choice

#### Inclusion-Exclusion Principle
- **When to use**: Counting elements in union of overlapping sets
- **Formula**: |A ∪ B| = |A| + |B| - |A ∩ B|
- **Example**: Count numbers divisible by 2 OR 3
- **Implementation**: Add individual counts, subtract intersections

#### Binomial Coefficients
- **When to use**: Counting combinations (unordered selections)
- **Formula**: C(n,k) = n! / (k!(n-k)!)
- **Example**: Count ways to choose k items from n items
- **Implementation**: Use factorial precomputation or Pascal's triangle

### Advanced Counting Techniques

#### Generating Functions
- **When to use**: Counting sequences with specific properties
- **Formula**: G(x) = Σ aₙxⁿ where aₙ is the count
- **Example**: Count ways to make change with coins
- **Implementation**: Use polynomial multiplication

#### Recurrence Relations
- **When to use**: When counting follows a pattern
- **Formula**: aₙ = f(aₙ₋₁, aₙ₋₂, ..., a₀)
- **Example**: Fibonacci sequence, Catalan numbers
- **Implementation**: Use dynamic programming or matrix exponentiation

#### Burnside's Lemma
- **When to use**: Counting objects under group actions (symmetry)
- **Formula**: |X/G| = (1/|G|) Σ |X^g| where X^g are fixed points
- **Example**: Count distinct colorings of a necklace
- **Implementation**: Count fixed points under each group action

#### Catalan Numbers
- **When to use**: Counting valid parentheses, binary trees, paths
- **Formula**: Cₙ = (1/(n+1)) × C(2n,n)
- **Example**: Count valid parentheses expressions
- **Implementation**: Use recurrence Cₙ = Σ Cᵢ × Cₙ₋₁₋ᵢ

### Mathematical Tools

#### Modular Arithmetic
- **When to use**: Handling large numbers that don't fit in standard types
- **Properties**: (a + b) mod m = ((a mod m) + (b mod m)) mod m
- **Example**: Count combinations modulo 10⁹ + 7
- **Implementation**: Apply modulo at each step to prevent overflow

#### Combinatorial Identities
- **When to use**: Simplifying complex counting expressions
- **Examples**: 
  - C(n,k) = C(n,n-k) (symmetry)
  - C(n,k) = C(n-1,k-1) + C(n-1,k) (Pascal's identity)
- **Implementation**: Use identities to reduce computation

#### Probability Theory
- **When to use**: Counting with probability or expected values
- **Formula**: P(A) = |A| / |S| where S is sample space
- **Example**: Expected number of inversions in random permutation
- **Implementation**: Count favorable outcomes / total outcomes

#### Number Theory
- **When to use**: Problems involving prime factorization or divisibility
- **Examples**: Count numbers with specific prime factors
- **Implementation**: Use sieve algorithms or factorization

### Specialized Counting Techniques

#### Stars and Bars
- **When to use**: Counting ways to distribute identical objects
- **Formula**: C(n+k-1, k-1) ways to distribute n objects into k bins
- **Example**: Count ways to distribute 10 identical balls into 3 boxes
- **Implementation**: Use binomial coefficient formula

#### Principle of Reflection
- **When to use**: Counting paths that avoid certain boundaries
- **Formula**: Total paths - reflected paths
- **Example**: Count paths from (0,0) to (n,m) staying above y=x
- **Implementation**: Use reflection to count invalid paths

#### Bijective Proofs
- **When to use**: Proving two sets have same size by finding bijection
- **Method**: Show one-to-one correspondence between sets
- **Example**: Prove C(n,k) = C(n,n-k) by showing bijection
- **Implementation**: Construct explicit mapping between sets

#### Pigeonhole Principle
- **When to use**: Proving existence of certain configurations
- **Statement**: If n+1 objects are placed in n boxes, some box has ≥2 objects
- **Example**: Prove that in any group of 13 people, two have same birthday month
- **Implementation**: Use contradiction or direct counting

## Problem Categories

### Basic Counting
- [Counting Combinations](counting_combinations_analysis) - Basic combination counting
- [Counting Permutations](counting_permutations_analysis) - Permutation enumeration
- [Counting Sequences](counting_sequences_analysis) - Sequence counting
- [Counting Reorders](counting_reorders_analysis) - Reordering problems
- [Empty String](empty_string_analysis) - String counting

### Grid Problems
- [Grid Completion](grid_completion_analysis) - Filling grid cells
- [Grid Paths II](grid_paths_ii_analysis) - Path counting in grids
- [All Letter Subgrid Count I](all_letter_subgrid_count_i_analysis) - Letter grid counting
- [All Letter Subgrid Count II](all_letter_subgrid_count_ii_analysis) - Advanced grid counting
- [Border Subgrid Count I](border_subgrid_count_i_analysis) - Border counting
- [Border Subgrid Count II](border_subgrid_count_ii_analysis) - Complex border counting
- [Filled Subgrid Count I](filled_subgrid_count_i_analysis) - Fill counting
- [Filled Subgrid Count II](filled_subgrid_count_ii_analysis) - Advanced fill counting

### Distribution Problems
- [Collecting Numbers Distribution](collecting_numbers_distribution_analysis) - Number distribution
- [Functional Graph Distribution](functional_graph_distribution_analysis) - Graph counting
- [Tournament Graph Distribution](tournament_graph_distribution_analysis) - Tournament graphs

### Special Counting
- [Counting Bishops](counting_bishops_analysis) - Chess piece counting
- [Permutation Inversions](permutation_inversions_analysis) - Inversion counting
- [Raab Game II](raab_game_ii_analysis) - Game state counting

## Detailed Examples and Implementations

### Classic Counting Problems with Code

#### 1. Permutations and Combinations
```python
def factorial(n, mod=None):
    if n < 0:
        return 0
    if n <= 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
        if mod:
            result %= mod
    
    return result

def permutations(n, r, mod=None):
    if r > n or r < 0:
        return 0
    
    result = 1
    for i in range(n - r + 1, n + 1):
        result *= i
        if mod:
            result %= mod
    
    return result

def combinations(n, r, mod=None):
    if r > n or r < 0:
        return 0
    if r > n - r:
        r = n - r
    
    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
        if mod:
            result %= mod
    
    return result

def combinations_with_repetition(n, r, mod=None):
    return combinations(n + r - 1, r, mod)

def multinomial_coefficient(n, k_list, mod=None):
    if sum(k_list) != n:
        return 0
    
    result = factorial(n, mod)
    for k in k_list:
        result = result // factorial(k, mod)
        if mod:
            result %= mod
    
    return result
```

#### 2. Inclusion-Exclusion Principle
```python
def inclusion_exclusion_sets(sets):
    n = len(sets)
    total = 0
    
    # Generate all non-empty subsets
    for mask in range(1, 1 << n):
        intersection = set(sets[0]) if sets else set()
        
        # Find intersection of sets in current subset
        for i in range(n):
            if mask & (1 << i):
                intersection &= set(sets[i])
        
        # Add or subtract based on subset size
        if bin(mask).count('1') % 2 == 1:
            total += len(intersection)
        else:
            total -= len(intersection)
    
    return total

def count_divisible_by_any(numbers, divisors):
    n = len(divisors)
    total = 0
    
    for mask in range(1, 1 << n):
        lcm = 1
        for i in range(n):
            if mask & (1 << i):
                lcm = lcm * divisors[i] // gcd(lcm, divisors[i])
        
        count = sum(1 for num in numbers if num % lcm == 0)
        
        if bin(mask).count('1') % 2 == 1:
            total += count
        else:
            total -= count
    
    return total

def derangements(n, mod=None):
    if n == 0:
        return 1
    if n == 1:
        return 0
    
    # Using inclusion-exclusion: !n = n! * sum((-1)^k / k!)
    result = 0
    factorial_n = factorial(n, mod)
    
    for k in range(n + 1):
        term = factorial_n // factorial(k, mod)
        if k % 2 == 0:
            result += term
        else:
            result -= term
        
        if mod:
            result %= mod
    
    return result
```

#### 3. Catalan Numbers and Applications
```python
def catalan_number(n, mod=None):
    if n <= 1:
        return 1
    
    # C(n) = (2n)! / ((n+1)! * n!)
    numerator = factorial(2 * n, mod)
    denominator = (factorial(n + 1, mod) * factorial(n, mod)) % mod if mod else factorial(n + 1) * factorial(n)
    
    if mod:
        # Use modular inverse for division
        return (numerator * mod_inverse(denominator, mod)) % mod
    else:
        return numerator // denominator

def catalan_numbers_sequence(n, mod=None):
    if n == 0:
        return [1]
    
    catalan = [0] * (n + 1)
    catalan[0] = 1
    
    for i in range(1, n + 1):
        for j in range(i):
            catalan[i] += catalan[j] * catalan[i - 1 - j]
            if mod:
                catalan[i] %= mod
    
    return catalan

def count_binary_trees(n, mod=None):
    return catalan_number(n, mod)

def count_valid_parentheses(n, mod=None):
    return catalan_number(n, mod)

def count_dyck_paths(n, mod=None):
    return catalan_number(n, mod)
```

#### 4. Stars and Bars Method
```python
def stars_and_bars(n, k, mod=None):
    """
    Count ways to distribute n identical objects into k distinct boxes
    Equivalent to C(n + k - 1, k - 1)
    """
    return combinations(n + k - 1, k - 1, mod)

def positive_stars_and_bars(n, k, mod=None):
    """
    Count ways to distribute n identical objects into k distinct boxes
    with at least one object in each box
    Equivalent to C(n - 1, k - 1)
    """
    if n < k:
        return 0
    return combinations(n - 1, k - 1, mod)

def bounded_stars_and_bars(n, k, limits, mod=None):
    """
    Count ways to distribute n identical objects into k distinct boxes
    with each box having at most limit[i] objects
    """
    total = 0
    
    # Use inclusion-exclusion
    for mask in range(1 << k):
        temp_n = n
        sign = 1
        
        for i in range(k):
            if mask & (1 << i):
                temp_n -= limits[i] + 1
                sign *= -1
        
        if temp_n >= 0:
            total += sign * combinations(temp_n + k - 1, k - 1, mod)
            if mod:
                total %= mod
    
    return total
```

### Advanced Counting Techniques

#### 1. Burnside's Lemma
```python
def burnside_lemma(actions, elements):
    """
    Count distinct orbits under group actions
    actions: list of functions representing group actions
    elements: list of elements to act upon
    """
    total_fixed = 0
    
    for action in actions:
        fixed_count = 0
        for element in elements:
            if action(element) == element:
                fixed_count += 1
        total_fixed += fixed_count
    
    return total_fixed // len(actions)

def count_necklaces(n, k):
    """
    Count distinct necklaces with n beads and k colors
    considering rotations as equivalent
    """
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    total = 0
    for i in range(n):
        total += k ** gcd(i, n)
    
    return total // n

def count_binary_strings_rotations(n):
    """
    Count distinct binary strings of length n
    considering rotations as equivalent
    """
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    total = 0
    for i in range(n):
        total += 2 ** gcd(i, n)
    
    return total // n
```

#### 2. Modular Arithmetic Operations
```python
def mod_inverse(a, mod):
    """Find modular inverse using extended Euclidean algorithm"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, y = extended_gcd(a, mod)
    if gcd != 1:
        raise ValueError("Modular inverse doesn't exist")
    
    return (x % mod + mod) % mod

def mod_power(base, exp, mod):
    """Fast modular exponentiation"""
    result = 1
    base %= mod
    
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    
    return result

def mod_factorial(n, mod):
    """Compute n! mod mod"""
    result = 1
    for i in range(2, n + 1):
        result = (result * i) % mod
    return result

def mod_combinations(n, r, mod):
    """Compute C(n,r) mod mod"""
    if r > n or r < 0:
        return 0
    if r > n - r:
        r = n - r
    
    numerator = 1
    denominator = 1
    
    for i in range(r):
        numerator = (numerator * (n - i)) % mod
        denominator = (denominator * (i + 1)) % mod
    
    return (numerator * mod_inverse(denominator, mod)) % mod
```

#### 3. Probability and Expected Value
```python
def probability_union(events, probabilities):
    """
    Calculate P(A1 ∪ A2 ∪ ... ∪ An) using inclusion-exclusion
    """
    n = len(events)
    total = 0
    
    for mask in range(1, 1 << n):
        intersection_prob = 1
        for i in range(n):
            if mask & (1 << i):
                intersection_prob *= probabilities[i]
        
        if bin(mask).count('1') % 2 == 1:
            total += intersection_prob
        else:
            total -= intersection_prob
    
    return total

def expected_value_outcomes(outcomes, probabilities):
    """Calculate expected value E[X] = Σ x * P(x)"""
    return sum(outcome * prob for outcome, prob in zip(outcomes, probabilities))

def geometric_distribution_expected(p):
    """Expected number of trials until first success"""
    return 1 / p

def coupon_collector_expected(n):
    """
    Expected number of trials to collect all n coupons
    E[X] = n * H_n where H_n is n-th harmonic number
    """
    harmonic = sum(1 / i for i in range(1, n + 1))
    return n * harmonic
```

## Tips for Success

1. **Master Basic Principles**: Addition and multiplication
2. **Understand Combinations**: nCr calculations
3. **Learn Modular Arithmetic**: Handle large numbers
4. **Practice Implementation**: Code counting formulas
5. **Study Special Sequences**: Catalan, Fibonacci, etc.
6. **Know Advanced Techniques**: Burnside's lemma, generating functions

## Common Pitfalls to Avoid

1. **Integer Overflow**: Large numbers
2. **Double Counting**: Overlapping cases
3. **Missing Cases**: Incomplete counting
4. **Modulo Errors**: Wrong arithmetic

## Advanced Topics

### Combinatorial Objects
- **Permutations**: Ordering elements
- **Combinations**: Selecting elements
- **Partitions**: Breaking into parts
- **Compositions**: Ordered partitions

### Counting Techniques
- **Stars and Bars**: Distribution counting
- **Principle of Reflection**: Path counting
- **Generating Functions**: Sequence analysis
- **Bijective Proofs**: Direct counting

### Special Numbers
- **Stirling Numbers**: Set partitions
- **Bell Numbers**: Total partitions
- **Catalan Numbers**: Parentheses matching
- **Lucas Numbers**: Special sequences

## Algorithm Complexities

### Basic Operations
- **Combination Calculation**: O(n) time
- **Permutation Generation**: O(n!) time
- **Grid Counting**: O(n²) typical
- **Distribution Counting**: O(n log n) typical

### Advanced Operations
- **Generating Functions**: Variable complexity
- **Graph Counting**: Often exponential
- **Grid Path Counting**: Often exponential
- **Modular Exponentiation**: O(log n) time

---

Ready to start? Begin with [Counting Combinations](counting_combinations_analysis) and work your way through the problems in order of difficulty!