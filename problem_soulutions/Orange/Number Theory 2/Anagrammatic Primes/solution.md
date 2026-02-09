# Anagrammatic Primes

## Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

An anagrammatic prime is a prime number that remains prime no matter how its digits are rearranged.

Given n, find the smallest anagrammatic prime that is:
- Greater than n
- Less than the next power of 10 greater than n

Output 0 if no such prime exists in that range.

## Input Format
- Multiple test cases until line with 0
- Each line: positive integer n (< 10000000)

## Output Format
For each n, print the smallest anagrammatic prime in range (n, next_power_of_10), or 0 if none exists.

## Example
```
Input:
1
25
100
0

Output:
2
0
0
```
For n=1: Range is (1, 10). Smallest anagrammatic prime > 1 is 2.
For n=25: Range is (25, 100). No anagrammatic prime exists in this range (11 is below 25, next would be too large).
For n=100: Range is (100, 1000). No anagrammatic primes exist in this range.

## Solution

### Approach
Key observations:
1. Multi-digit anagrammatic primes can only contain digits 1, 3, 7, 9 (others make some permutation even or divisible by 5)
2. For 2+ digits, all digits must be the same (else some permutation might not be prime)
3. Repunit primes (111...1) and repdigit primes (like 11, 77777) are candidates

Actually, for multi-digit numbers:
- 2 digits: 11 is anagrammatic prime
- 3+ digits: Must be all same digit, and that digit repunit must be prime

Precompute all anagrammatic primes up to 10^7.

### Python Solution

```python
def solve():
  # Precompute all anagrammatic primes up to 10^7
  MAX = 10**7

  def is_prime(n):
    if n < 2:
      return False
    if n == 2:
      return True
    if n % 2 == 0:
      return False
    for i in range(3, int(n**0.5) + 1, 2):
      if n % i == 0:
        return False
    return True

  def get_permutations(n):
    from itertools import permutations
    digits = str(n)
    perms = set()
    for p in permutations(digits):
      if p[0] != '0':  # No leading zeros
        perms.add(int(''.join(p)))
    return perms

  def is_anagrammatic_prime(n):
    perms = get_permutations(n)
    return all(is_prime(p) for p in perms)

  # Find all anagrammatic primes
  anagrammatic = []

  # Single digit primes are anagrammatic
  for p in [2, 3, 5, 7]:
    anagrammatic.append(p)

  # For multi-digit, check candidates
  # Multi-digit anagrammatic primes: 11, R2 (11 is prime)
  # After checking: 2, 3, 5, 7, 11, R19, R23, ... repunits

  # Actually, let's just check small numbers
  for n in range(10, 1000):
    if is_anagrammatic_prime(n):
      anagrammatic.append(n)

  # For larger numbers, only repdigit 1s (repunits) could work
  # But 111 = 3 * 37, 1111 = 11 * 101, etc.
  # Check repunits
  for length in range(3, 8):
    repunit = int('1' * length)
    if is_prime(repunit):
      anagrammatic.append(repunit)

  anagrammatic.sort()

  # For each query
  import sys
  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      break

    # Find next power of 10 > n
    power = 1
    while power <= n:
      power *= 10

    # Find smallest anagrammatic prime in (n, power)
    result = 0
    for p in anagrammatic:
      if p > n and p < power:
        result = p
        break

    print(result)

if __name__ == "__main__":
  solve()
```

### Precomputed Solution

```python
def solve():
  # Known anagrammatic primes up to 10^7
  # Single digits: 2, 3, 5, 7
  # Two digits: 11
  # Beyond that: only R2 = 11 works in reasonable range
  # R19 = 1111111111111111111 (19 ones) is prime but > 10^7

  # For this problem, anagrammatic primes are: 2, 3, 5, 7, 11
  # After 11, next would be a repunit prime but those are very large

  anagrammatic = [2, 3, 5, 7, 11]

  import sys
  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      break

    # Next power of 10
    limit = 10
    while limit <= n:
      limit *= 10

    result = 0
    for p in anagrammatic:
      if n < p < limit:
        result = p
        break

    print(result)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(1) per query (with precomputation)
- **Space Complexity:** O(1)

### Key Insight
Anagrammatic primes are very rare. For single digits: 2, 3, 5, 7. For two digits: only 11 (same digits). For 3+ digits, any number with different digits will have permutations that are even or divisible by 5, so only repdigits work, and only repunit (all 1s) primes exist. The next repunit prime after R2=11 is R19 which exceeds 10^7.
