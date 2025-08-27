# CSES Counting Combinations - Problem Analysis

## Problem Statement
Given integers n and k, count the number of ways to choose k elements from a set of n elements (combinations).

### Input
The first input line has two integers n and k: the total number of elements and the number to choose.

### Output
Print the number of combinations modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 10^6
- 0 ≤ k ≤ n

### Example
```
Input:
5 2

Output:
10
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

*This analysis shows how to efficiently count combinations using mathematical formulas and modular arithmetic.* 