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
10
25
100
991
0

Output:
2
11
31
113
0
```
- n = 1: the range is (1, 10), and the answer is 2.
- n = 25: the range is (25, 100), and 31 qualifies (13 is too small).
- n = 100: the range is (100, 1000), and 113 qualifies, since 113, 131 and 311 are all prime.
- n = 991: no anagrammatic prime lies strictly between 991 and 1000.

## Solution

### Approach
Generate every anagrammatic prime below 10⁷ once, then answer each query with a scan.

1. With two or more digits, every digit must be 1, 3, 7 or 9. Otherwise some permutation ends in an even digit or in 5.
2. Enumerate digit multisets over {1, 3, 7, 9} with up to 7 digits (each multiset once), and keep those whose permutations are all prime.
3. For a query n, the limit is `10 ** len(str(n))`. Print the first listed prime p with n < p < limit, or 0 if there is none.

Below 10⁷ the full list is 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, 97, 113, 131, 199, 311, 337, 373, 733, 919, 991. The next one is the repunit R19.

### Python Solution

```python
import sys
from itertools import permutations, product


def is_prime(n):
  if n < 2:
    return False
  if n % 2 == 0:
    return n == 2
  i = 3
  while i * i <= n:
    if n % i == 0:
      return False
    i += 2
  return True


def anagrammatic_primes(max_digits=7):
  # With 2+ digits, any 0, 2, 4, 5, 6, 8 can be moved last, making the number even or divisible by 5.
  found = [2, 3, 5, 7]
  for length in range(2, max_digits + 1):
    for digits in product("1379", repeat=length):
      if list(digits) != sorted(digits):
        continue  # test each digit multiset once
      perms = {int("".join(p)) for p in permutations(digits)}
      if all(is_prime(p) for p in perms):
        found.extend(perms)
  return sorted(found)


def solve():
  primes = anagrammatic_primes()
  for line in sys.stdin:
    n = int(line)
    if n == 0:
      break
    limit = 10 ** len(str(n))  # next power of 10 above n
    print(next((p for p in primes if n < p < limit), 0))


if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** precomputation tests at most 4⁷ digit strings, then O(22) per query
- **Space Complexity:** O(1)

### Key Insight
Anagrammatic (permutable) primes are rare: 22 exist below 10⁷, none with 4 to 7 digits. The digit rule shrinks the search to 4⁷ candidates, so precomputing is instant. So every query with n ≥ 991 answers 0.

