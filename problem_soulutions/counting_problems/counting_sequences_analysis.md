# CSES Counting Sequences - Problem Analysis

## Problem Statement
Given integers n and k, count the number of sequences of length n where each element is between 1 and k, and no two consecutive elements are equal.

### Input
The first input line has two integers n and k: the length of the sequence and the maximum value.

### Output
Print the number of valid sequences modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 10^6
- 1 ≤ k ≤ 10^6

### Example
```
Input:
3 2

Output:
2
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

*This analysis shows how to efficiently count sequences with constraints using mathematical formulas and dynamic programming.* 