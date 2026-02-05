# Irreducible Basic Fractions

## Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

A fraction m/n is basic if 0 ≤ m < n, and irreducible if gcd(m, n) = 1.

Given n, count the irreducible basic fractions with denominator n.

For example, n=12 has 4 irreducible basic fractions: 1/12, 5/12, 7/12, 11/12.

## Input Format
- Multiple test cases until n = 0
- Each line: positive integer n (< 10^9)

## Output Format
For each n, print the count of irreducible basic fractions.

## Solution

### Approach
This is Euler's Totient Function φ(n)!

φ(n) counts integers from 1 to n-1 that are coprime with n.
These are exactly the numerators of irreducible fractions m/n.

φ(n) = n × ∏(1 - 1/p) for all prime factors p of n

### Python Solution

```python
def euler_totient(n):
  """Calculate Euler's totient function φ(n)"""
  result = n
  p = 2

  while p * p <= n:
    if n % p == 0:
      # Remove all factors of p
      while n % p == 0:
        n //= p
      # Apply formula
      result -= result // p

    p += 1

  # If n > 1, then it's a prime factor
  if n > 1:
    result -= result // n

  return result

def solve():
  import sys

  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      break

    print(euler_totient(n))

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def phi(n):
  """Euler's totient using prime factorization"""
  result = n
  d = 2

  while d * d <= n:
    if n % d == 0:
      result -= result // d
      while n % d == 0:
        n //= d
    d += 1

  if n > 1:
    result -= result // n

  return result

def solve():
  import sys
  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      break
    print(phi(n))

if __name__ == "__main__":
  solve()
```

### Optimized with Prime Check

```python
def euler_phi(n):
  if n == 1:
    return 1

  result = n
  temp = n

  # Check for factor 2
  if temp % 2 == 0:
    result -= result // 2
    while temp % 2 == 0:
      temp //= 2

  # Check odd factors
  i = 3
  while i * i <= temp:
    if temp % i == 0:
      result -= result // i
      while temp % i == 0:
        temp //= i
    i += 2

  # Remaining prime factor
  if temp > 1:
    result -= result // temp

  return result

def solve():
  while True:
    n = int(input())
    if n == 0:
      break
    print(euler_phi(n))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(√n) per query
- **Space Complexity:** O(1)

### Key Insight
The count of irreducible fractions m/n (where 0 < m < n and gcd(m,n) = 1) is exactly Euler's totient φ(n). This counts integers from 1 to n-1 coprime with n. Use the formula φ(n) = n × ∏(1 - 1/p) where p ranges over prime factors of n.
