---
layout: simple
title: "Mobius Function and Inversion - Number Theory"
permalink: /problem_soulutions/counting_problems/mobius_function_analysis
difficulty: Hard
tags: [number-theory, mobius-function, inclusion-exclusion, sieve, divisibility]
---

# Mobius Function and Inversion

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Number Theory / Counting |
| **Key Technique** | Mobius Function, Linear Sieve, Inclusion-Exclusion |
| **Applications** | Coprime counting, GCD queries, Square-free counting |

### Function Definition

The **Mobius function** mu(n) is defined as:

```
mu(n) = 1       if n = 1
mu(n) = (-1)^k  if n is a product of k distinct primes
mu(n) = 0       if n has a squared prime factor
```

| n | Factorization | mu(n) | Reason |
|---|---------------|-------|--------|
| 1 | 1 | 1 | Base case |
| 2 | 2 | -1 | One prime |
| 6 | 2 * 3 | 1 | Two distinct primes |
| 4 | 2^2 | 0 | Squared factor |
| 30 | 2 * 3 * 5 | -1 | Three distinct primes |

### Learning Goals

After studying this topic, you will be able to:
- [ ] Compute mu(n) efficiently using a linear sieve
- [ ] Apply Mobius inversion to transform summation formulas
- [ ] Count coprime pairs in a range using inclusion-exclusion
- [ ] Solve square-free number counting problems
- [ ] Optimize GCD-based counting queries

---

## Intuition: Connection to Inclusion-Exclusion

### The Core Insight

> **Key Idea:** The Mobius function encodes inclusion-exclusion coefficients for divisibility problems.

The fundamental property:

```
Sum of mu(d) over all divisors d of n = [n == 1]
```

Where [P] is 1 if P is true, 0 otherwise. For counting with GCD:

```
[gcd(a,b) = 1] = Sum of mu(d) for all d | gcd(a,b)
```

### Analogy

Think of Mobius inversion like the sieve of Eratosthenes:
- **Sieve**: Marks multiples to identify primes
- **Mobius**: Uses divisor structure to isolate exact conditions

---

## Mobius Inversion Formula

If f and g are arithmetic functions with:

```
g(n) = Sum of f(d) for all divisors d of n
```

Then we can **invert** to recover f:

```
f(n) = Sum of mu(d) * g(n/d) for all divisors d of n
```

### Practical Application: Coprime Pairs

**Problem:** Count pairs (a, b) with 1 <= a, b <= N and gcd(a, b) = 1.

Let f(k) = pairs with gcd = k exactly, g(k) = pairs with k | gcd = floor(N/k)^2.

For coprime pairs:
```
f(1) = Sum of mu(d) * floor(N/d)^2 for d from 1 to N
```

---

## Dry Run: Computing Coprime Pairs

**Problem:** Count pairs (a, b) with 1 <= a, b <= 6 and gcd(a, b) = 1.

### Step 1: Compute Mobius Values

```
mu[1]=1, mu[2]=-1, mu[3]=-1, mu[4]=0, mu[5]=-1, mu[6]=1
```

### Step 2: Apply the Formula

```
Answer = Sum of mu[d] * floor(6/d)^2 for d = 1 to 6

d=1: mu[1] * (6)^2  =  1 * 36 =  36
d=2: mu[2] * (3)^2  = -1 * 9  =  -9
d=3: mu[3] * (2)^2  = -1 * 4  =  -4
d=4: mu[4] * (1)^2  =  0 * 1  =   0
d=5: mu[5] * (1)^2  = -1 * 1  =  -1
d=6: mu[6] * (1)^2  =  1 * 1  =   1

Total = 36 - 9 - 4 + 0 - 1 + 1 = 23
```

### Verification

The 23 coprime pairs include: (1,1), (1,2), ..., (6,5). Manual count confirms 23.

---

## Solution: Linear Sieve for Mobius Function

### Algorithm

Key observations:
1. mu[1] = 1
2. mu[p] = -1 for prime p
3. mu[p*k] = 0 if p | k, else mu[p*k] = -mu[k]

### Python Implementation

```python
def linear_sieve_mobius(n):
    """
    Compute Mobius function for all integers 1 to n.
    Time: O(n), Space: O(n)
    """
    mu = [0] * (n + 1)
    is_prime = [True] * (n + 1)
    primes = []
    mu[1] = 1

    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1

        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]

    return mu, primes


def count_coprime_pairs(n):
    """Count pairs (a,b) with 1 <= a,b <= n and gcd(a,b) = 1."""
    mu, _ = linear_sieve_mobius(n)
    return sum(mu[d] * (n // d) ** 2 for d in range(1, n + 1))


def count_coprime_pairs_optimized(n):
    """Optimized O(sqrt(n)) using prefix sums."""
    mu, _ = linear_sieve_mobius(n)
    prefix_mu = [0] * (n + 2)
    for i in range(1, n + 1):
        prefix_mu[i] = prefix_mu[i - 1] + mu[i]

    result, d = 0, 1
    while d <= n:
        q = n // d
        d_max = n // q
        mu_sum = prefix_mu[d_max] - prefix_mu[d - 1]
        result += mu_sum * q * q
        d = d_max + 1
    return result
```

### C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

class MobiusSieve {
public:
    vector<int> mu;
    vector<int> primes;
    vector<long long> prefix_mu;

    MobiusSieve(int n) : mu(n + 1), prefix_mu(n + 2, 0) {
        vector<bool> is_prime(n + 1, true);
        mu[1] = 1;

        for (int i = 2; i <= n; i++) {
            if (is_prime[i]) {
                primes.push_back(i);
                mu[i] = -1;
            }
            for (int p : primes) {
                if ((long long)i * p > n) break;
                is_prime[i * p] = false;
                if (i % p == 0) { mu[i * p] = 0; break; }
                else { mu[i * p] = -mu[i]; }
            }
        }
        for (int i = 1; i <= n; i++)
            prefix_mu[i] = prefix_mu[i - 1] + mu[i];
    }

    long long countCoprimePairs(int m) {
        long long result = 0;
        for (int d = 1; d <= m; d++)
            result += (long long)mu[d] * (m / d) * (m / d);
        return result;
    }

    long long countCoprimePairsOptimized(int m) {
        long long result = 0;
        for (int d = 1, d_max; d <= m; d = d_max + 1) {
            int q = m / d;
            d_max = m / q;
            long long mu_sum = prefix_mu[d_max] - prefix_mu[d - 1];
            result += mu_sum * (long long)q * q;
        }
        return result;
    }
};

long long countSquareFree(int n, MobiusSieve& sieve) {
    long long result = 0;
    for (int d = 1; (long long)d * d <= n; d++)
        result += (long long)sieve.mu[d] * (n / ((long long)d * d));
    return result;
}
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Linear sieve | O(N) | O(N) |
| Coprime pairs (basic) | O(N) | O(N) |
| Coprime pairs (optimized) | O(sqrt(N)) | O(N) |
| Square-free count | O(sqrt(N)) | O(sqrt(N)) |

---

## Common Mistakes

### Mistake 1: Incorrect Sieve for Squared Factors

```python
# WRONG
for i in range(2, n + 1):
    if is_prime[i]:
        mu[i] = -1
    else:
        mu[i] = 0  # Wrong! 6=2*3 is square-free, mu[6]=1
```

**Fix:** Track square-free property during sieve.

### Mistake 2: Integer Overflow

```cpp
// WRONG
int result = mu[d] * (n / d) * (n / d);  // Overflow!

// CORRECT
long long result = (long long)mu[d] * (n / d) * (n / d);
```

### Mistake 3: Wrong Sign in Multiplication

```python
# WRONG
mu[i * p] = mu[i]  # Should be -mu[i]

# CORRECT
mu[i * p] = -mu[i]  # Sign flips when adding new prime
```

### Mistake 4: Missing Base Case

```python
# WRONG: mu[1] never set
mu = [0] * (n + 1)

# CORRECT
mu = [0] * (n + 1)
mu[1] = 1
```

---

## Edge Cases

| Case | Input | Expected | Reason |
|------|-------|----------|--------|
| n = 1 | Coprime pairs to 1 | 1 | Only (1,1) |
| Prime | mu(prime) | -1 | Single prime factor |
| Prime power | mu(p^k), k > 1 | 0 | Squared factor |
| Square-free composite | mu(2*3*5*7) | 1 | Even prime count |
| Perfect square | mu(36) | 0 | 36 = 6^2 |

---

## When to Use This Pattern

### Use Mobius Function When:

- **Counting coprime pairs/tuples** in a range
- **GCD queries**: "How many pairs have GCD exactly k?"
- **Square-free counting**: Numbers without squared prime factors
- **Euler's totient problems**: phi(n) uses Mobius inversion
- **Divisibility constraints**: "exactly divides" conditions

### Identification Checklist:

- [ ] Problem involves counting with GCD conditions
- [ ] Need to transform "at least" to "exactly" counts
- [ ] Divisibility plays a central role
- [ ] Looking for inclusion-exclusion with divisors
- [ ] Problem mentions "square-free" numbers

### Do Not Use When:

- Simple prime factorization suffices
- Constraints allow brute force GCD checking
- No divisibility structure to exploit

---

## Related Problems

### Foundational

| Problem | Key Concept |
|---------|-------------|
| CSES: Common Divisors | GCD counting basics |
| SPOJ: GCDEX | Sum of GCDs |
| Project Euler 72 | Counting reduced fractions |

### Intermediate

| Problem | Mobius Usage |
|---------|--------------|
| SPOJ: SQFREE | Square-free counting |
| Codeforces: Coprime | Coprime pairs in array |

### Advanced

| Problem | Complexity |
|---------|------------|
| SPOJ: LCMSUM | LCM sum with Mobius |
| Codeforces: GCD Table | 2D Mobius application |

---

## Applications Summary

**1. Coprime Pair Counting**
```
Count(gcd=1, 1..N) = Sum of mu[d] * floor(N/d)^2
```

**2. Square-Free Counting**
```
Count(square-free, 1..N) = Sum of mu[d] * floor(N/d^2) for d=1 to sqrt(N)
```

**3. Euler's Totient via Mobius**
```
phi(n) = Sum of mu[d] * (n/d) for all d | n
```

**4. GCD = k Pair Counting**
```
Count(gcd=k, 1..N) = Sum of mu[d] * floor(N/(k*d))^2
```

---

## Key Takeaways

1. **Mobius function** encodes inclusion-exclusion for divisibility
2. **Linear sieve** computes all mu[1..N] in O(N) time
3. **Inversion formula** transforms "divides" sums to "equals" counts
4. **Prefix sums + sqrt decomposition** optimize to O(sqrt(N)) queries

---

## Practice Checklist

- [ ] Implement linear sieve for Mobius function from scratch
- [ ] Derive the coprime pair counting formula
- [ ] Apply sqrt decomposition for O(sqrt(N)) queries
- [ ] Recognize problems where Mobius inversion applies
- [ ] Handle edge cases (n=1, prime powers, overflow)

---

## Additional Resources

- [CP-Algorithms: Mobius Function](https://cp-algorithms.com/algebra/mobius-function.html)
- [Codeforces: Mobius Inversion Tutorial](https://codeforces.com/blog/entry/53925)
- [Project Euler 72: Counting Fractions](https://projecteuler.net/problem=72)
