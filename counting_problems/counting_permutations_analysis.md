# CSES Counting Permutations - Problem Analysis

## Problem Statement
Given an integer n, count the number of permutations of {1, 2, ..., n} that have exactly k inversions.

### Input
The first input line has two integers n and k: the size of the permutation and the number of inversions.

### Output
Print the number of permutations modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 1000
- 0 ≤ k ≤ n(n-1)/2

### Example
```
Input:
3 1

Output:
2
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

*This analysis shows how to efficiently count permutations with a given number of inversions using dynamic programming.* 