---
layout: simple
title: "Number Theory 2"
permalink: /problem_soulutions/Orange/Number Theory 2/
---
# Number Theory 2

Advanced number theory problems involving prime factorization, Euler's totient function, and other mathematical concepts.

## Problems

### Anagrammatic Primes

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

An anagrammatic prime is a prime number that remains prime no matter how its digits are rearranged.

Given n, find the smallest anagrammatic prime that is:
- Greater than n
- Less than the next power of 10 greater than n

Output 0 if no such prime exists in that range.

#### Input Format
- Multiple test cases until line with 0
- Each line: positive integer n (< 10000000)

#### Output Format
For each n, print the smallest anagrammatic prime in range (n, next_power_of_10), or 0 if none exists.

#### Solution

##### Approach
Key observations:
1. Multi-digit anagrammatic primes can only contain digits 1, 3, 7, 9 (others make some permutation even or divisible by 5)
2. For 2+ digits, all digits must be the same (else some permutation might not be prime)
3. Repunit primes (111...1) and repdigit primes (like 11, 77777) are candidates

Actually, for multi-digit numbers:
- 2 digits: 11 is anagrammatic prime
- 3+ digits: Must be all same digit, and that digit repunit must be prime

Precompute all anagrammatic primes up to 10^7.

##### Python Solution

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

##### Complexity Analysis
- **Time Complexity:** O(1) per query (with precomputation)
- **Space Complexity:** O(1)

##### Key Insight
Anagrammatic primes are very rare. For single digits: 2, 3, 5, 7. For two digits: only 11 (same digits). For 3+ digits, any number with different digits will have permutations that are even or divisible by 5, so only repdigits work, and only repunit (all 1s) primes exist. The next repunit prime after R2=11 is R19 which exceeds 10^7.

---

### Dynamic Frog

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

A frog needs to cross a river of distance D using rocks. Rocks are either:
- Big (B): Can be used multiple times
- Small (S): Can only be used once (must be used going AND coming back)

The frog must go from left bank to right bank and return. Minimize the maximum single jump distance.

#### Input Format
- T test cases
- Each test case:
  - First line: N (rocks), D (river width)
  - Second line: N rock descriptions as "S-M" or "B-M" where M is distance from left bank

#### Output Format
For each case: "Case X: Y" where Y is the minimized maximum jump.

#### Solution

##### Approach
Since small rocks can only be used once, and frog must go and return:
- Going: Can use any rocks
- Returning: Small rocks are gone

Key insight: Process rocks by position. For the return trip, small rocks won't exist, so the frog must jump over gaps where small rocks were.

Strategy: On the way there, use all rocks. On return, only big rocks remain. The answer is the maximum of:
1. Max jump on the way there (using all rocks)
2. Max jump on return (only big rocks + banks)

##### Python Solution

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    parts = input().split()
    n, d = int(parts[0]), int(parts[1])

    rocks = []
    for i in range(n):
      rock = parts[2 + i] if len(parts) > 2 + i else input().split()[0]
      rock_type = rock[0]
      dist = int(rock[2:])
      rocks.append((dist, rock_type))

    rocks.sort()

    # Add banks
    positions = [0]  # left bank
    big_positions = [0]

    for dist, rock_type in rocks:
      positions.append(dist)
      if rock_type == 'B':
        big_positions.append(dist)

    positions.append(d)  # right bank
    big_positions.append(d)

    # Max jump going (using all rocks)
    max_jump_go = 0
    for i in range(1, len(positions)):
      max_jump_go = max(max_jump_go, positions[i] - positions[i-1])

    # Max jump returning (only big rocks)
    max_jump_return = 0
    for i in range(1, len(big_positions)):
      max_jump_return = max(max_jump_return, big_positions[i] - big_positions[i-1])

    result = max(max_jump_go, max_jump_return)
    print(f"Case {case}: {result}")

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    line = input().split()
    n, d = int(line[0]), int(line[1])

    rocks = []
    idx = 2
    while len(rocks) < n:
      if idx < len(line):
        rocks.append(line[idx])
        idx += 1
      else:
        rocks.extend(input().split())

    # Parse rocks
    parsed = []
    for rock in rocks:
      rock_type = rock[0]
      pos = int(rock.split('-')[1])
      parsed.append((pos, rock_type))

    parsed.sort()

    # Calculate jumps
    all_pos = [0] + [p for p, _ in parsed] + [d]
    big_pos = [0] + [p for p, t in parsed if t == 'B'] + [d]

    max_go = max(all_pos[i] - all_pos[i-1] for i in range(1, len(all_pos)))
    max_return = max(big_pos[i] - big_pos[i-1] for i in range(1, len(big_pos)))

    print(f"Case {case}: {max(max_go, max_return)}")

if __name__ == "__main__":
  solve()
```

### Input Parsing Variant

```python
def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  t = int(data[idx])
  idx += 1

  for case in range(1, t + 1):
    n = int(data[idx])
    d = int(data[idx + 1])
    idx += 2

    rocks = []
    for _ in range(n):
      rock = data[idx]
      idx += 1
      rock_type = rock[0]
      pos = int(rock[2:])
      rocks.append((pos, rock_type))

    rocks.sort()

    # All positions for going
    all_pos = [0] + [p for p, _ in rocks] + [d]
    # Big rocks only for return
    big_pos = [0] + [p for p, t in rocks if t == 'B'] + [d]

    max_go = max(all_pos[i] - all_pos[i-1] for i in range(1, len(all_pos)))
    max_ret = max(big_pos[i] - big_pos[i-1] for i in range(1, len(big_pos)))

    print(f"Case {case}: {max(max_go, max_ret)}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for sorting
- **Space Complexity:** O(N)

##### Key Insight
The frog uses all rocks going forward, but small rocks disappear after one use. On the return trip, only big rocks remain. The answer is the maximum of the largest gap in each direction. Going: gaps between consecutive rocks (including banks). Returning: gaps between consecutive big rocks only.

---

### Irreducible Basic Fractions

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

A fraction m/n is basic if 0 ≤ m < n, and irreducible if gcd(m, n) = 1.

Given n, count the irreducible basic fractions with denominator n.

For example, n=12 has 4 irreducible basic fractions: 1/12, 5/12, 7/12, 11/12.

#### Input Format
- Multiple test cases until n = 0
- Each line: positive integer n (< 10^9)

#### Output Format
For each n, print the count of irreducible basic fractions.

#### Solution

##### Approach
This is Euler's Totient Function φ(n)!

φ(n) counts integers from 1 to n-1 that are coprime with n.
These are exactly the numerators of irreducible fractions m/n.

φ(n) = n × ∏(1 - 1/p) for all prime factors p of n

##### Python Solution

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

##### Alternative

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

##### Optimized

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

##### Complexity Analysis
- **Time Complexity:** O(√n) per query
- **Space Complexity:** O(1)

##### Key Insight
The count of irreducible fractions m/n (where 0 < m < n and gcd(m,n) = 1) is exactly Euler's totient φ(n). This counts integers from 1 to n-1 coprime with n. Use the formula φ(n) = n × ∏(1 - 1/p) where p ranges over prime factors of n.

---

### Largest Prime Divisor

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a number N, find its largest prime divisor. If N is divisible by more than one prime, output the largest. If N is divisible by exactly one prime (N is a prime power), output -1.

#### Input Format
- At most 450 test cases
- Each line: integer N (up to 14 digits)
- Input ends with 0

#### Output Format
For each N, print its largest prime divisor, or -1 if N is a prime power.

#### Solution

##### Approach
1. Factor N to find all prime divisors
2. If only one unique prime exists, output -1
3. Otherwise, output the largest prime divisor

For large numbers (up to 10^14), we need efficient factorization:
- Trial division up to √N
- If remainder > 1 after trial division, it's a prime factor

##### Python Solution

```python
def largest_prime_divisor(n):
  """Find largest prime divisor, or -1 if only one prime divides n"""
  if n <= 1:
    return -1

  primes = []
  temp = n

  # Trial division
  d = 2
  while d * d <= temp:
    if temp % d == 0:
      primes.append(d)
      while temp % d == 0:
        temp //= d
    d += 1

  # If temp > 1, it's a prime factor
  if temp > 1:
    primes.append(temp)

  if len(primes) <= 1:
    return -1

  return max(primes)

def solve():
  import sys

  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      break

    print(largest_prime_divisor(n))

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  import sys

  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      break

    original = n
    prime_factors = []

    # Factor out 2
    if n % 2 == 0:
      prime_factors.append(2)
      while n % 2 == 0:
        n //= 2

    # Factor out odd numbers
    i = 3
    while i * i <= n:
      if n % i == 0:
        prime_factors.append(i)
        while n % i == 0:
          n //= i
      i += 2

    # Remaining prime
    if n > 1:
      prime_factors.append(n)

    if len(prime_factors) <= 1:
      print(-1)
    else:
      print(max(prime_factors))

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def largest_prime_divisor(n):
  if n <= 1:
    return -1

  first_prime = None
  largest = None

  # Factor out 2
  if n % 2 == 0:
    first_prime = 2
    largest = 2
    while n % 2 == 0:
      n //= 2

  # Factor out odd numbers
  d = 3
  while d * d <= n:
    if n % d == 0:
      if first_prime is None:
        first_prime = d
      largest = d
      while n % d == 0:
        n //= d
    d += 2

  # Remaining prime factor
  if n > 1:
    if first_prime is None:
      first_prime = n
    largest = n

  # If only one prime found
  if first_prime == largest and n == 1:
    # Check if there was only one prime
    # Actually need to track count
    pass

  # Re-implement with proper counting
  return largest if largest != first_prime or n > 1 else -1

def solve():
  while True:
    n = int(input())
    if n == 0:
      break

    primes = set()
    temp = n

    d = 2
    while d * d <= temp:
      if temp % d == 0:
        primes.add(d)
        while temp % d == 0:
          temp //= d
      d += 1 if d == 2 else 2

    if temp > 1:
      primes.add(temp)

    if len(primes) <= 1:
      print(-1)
    else:
      print(max(primes))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(√N) per query
- **Space Complexity:** O(log N) for storing prime factors

##### Key Insight
A number is a "prime power" if it has exactly one distinct prime factor (like 8 = 2³, 27 = 3³). We need at least two distinct prime factors to have a meaningful "largest". Factor the number efficiently using trial division up to √N, tracking distinct primes found.

---

### Pashmak and Parmida's problem

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given array a of n integers, define f(l, r, x) = count of indices k where l ≤ k ≤ r and a[k] = x.

Count pairs (i, j) where 1 ≤ i < j ≤ n and f(1, i, a[i]) > f(j, n, a[j]).

#### Input Format
- First line: n (1 ≤ n ≤ 10^6)
- Second line: n integers a1, a2, ..., an (1 ≤ ai ≤ 10^9)

#### Output Format
Print the count of valid pairs.

#### Solution

##### Approach
1. Compute L[i] = f(1, i, a[i]) = count of a[i] in prefix [1..i]
2. Compute R[j] = f(j, n, a[j]) = count of a[j] in suffix [j..n]
3. Count pairs where L[i] > R[j] with i < j

This is an inversion count problem! Use merge sort or BIT/Fenwick tree.

##### Python Solution

```python
def solve():
  import sys
  from collections import defaultdict

  input = sys.stdin.readline

  n = int(input())
  a = list(map(int, input().split()))

  # Compute L[i] = f(1, i, a[i])
  L = [0] * n
  count_left = defaultdict(int)
  for i in range(n):
    count_left[a[i]] += 1
    L[i] = count_left[a[i]]

  # Compute R[j] = f(j, n, a[j])
  R = [0] * n
  count_right = defaultdict(int)
  for j in range(n - 1, -1, -1):
    count_right[a[j]] += 1
    R[j] = count_right[a[j]]

  # Count pairs (i, j) where i < j and L[i] > R[j]
  # This is inversion count: count pairs where L[i] > R[j] for i < j

  # Use merge sort or BIT
  # BIT approach: process from right to left
  # For each j, count how many i < j have L[i] > R[j]

  # Compress R values (they're at most n)
  # BIT[x] = count of positions j seen so far with R[j] = x

  # Process from left to right:
  # For position i, we want to count j > i with R[j] < L[i]
  # Process from right to left:
  # At position i, count positions j > i (already processed) with R[j] < L[i]

  max_val = n + 1
  BIT = [0] * (max_val + 1)

  def update(idx, delta=1):
    while idx <= max_val:
      BIT[idx] += delta
      idx += idx & (-idx)

  def query(idx):
    total = 0
    while idx > 0:
      total += BIT[idx]
      idx -= idx & (-idx)
    return total

  result = 0

  # Process from right to left
  for i in range(n - 1, -1, -1):
    # Count j > i (already in BIT) with R[j] < L[i]
    if L[i] > 1:
      result += query(L[i] - 1)

    # Add R[i] to BIT
    update(R[i])

  print(result)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  import sys
  from collections import defaultdict

  input = sys.stdin.readline

  n = int(input())
  a = list(map(int, input().split()))

  # Compute L and R
  L = [0] * n
  R = [0] * n

  cnt = defaultdict(int)
  for i in range(n):
    cnt[a[i]] += 1
    L[i] = cnt[a[i]]

  cnt.clear()
  for j in range(n - 1, -1, -1):
    cnt[a[j]] += 1
    R[j] = cnt[a[j]]

  # Count inversions: pairs (i, j) with i < j and L[i] > R[j]
  def merge_count(arr, temp, left, mid, right):
    i = left
    j = mid + 1
    k = left
    count = 0

    while i <= mid and j <= right:
      if arr[i][0] <= arr[j][0]:
        temp[k] = arr[i]
        i += 1
      else:
        temp[k] = arr[j]
        count += (mid - i + 1)
        j += 1
      k += 1

    while i <= mid:
      temp[k] = arr[i]
      i += 1
      k += 1

    while j <= right:
      temp[k] = arr[j]
      j += 1
      k += 1

    for i in range(left, right + 1):
      arr[i] = temp[i]

    return count

  def merge_sort_count(arr, temp, left, right):
    count = 0
    if left < right:
      mid = (left + right) // 2
      count += merge_sort_count(arr, temp, left, mid)
      count += merge_sort_count(arr, temp, mid + 1, right)
      count += merge_count(arr, temp, left, mid, right)
    return count

  # Create pairs (R[j], original_index) but we need L[i] > R[j]
  # Actually need: pairs where earlier L > later R

  # Use modified approach: create array where arr[i] = (L[i], R[i])
  # ... this gets complex, BIT is cleaner

  # Stick with BIT solution
  max_val = n + 1
  BIT = [0] * (max_val + 2)

  def update(idx):
    idx += 1
    while idx <= max_val + 1:
      BIT[idx] += 1
      idx += idx & (-idx)

  def query(idx):
    idx += 1
    total = 0
    while idx > 0:
      total += BIT[idx]
      idx -= idx & (-idx)
    return total

  result = 0
  for i in range(n - 1, -1, -1):
    if L[i] > 1:
      result += query(L[i] - 2)  # R[j] < L[i] means R[j] <= L[i]-1
    update(R[i] - 1)

  print(result)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n)

##### Key Insight
Precompute L[i] (count of a[i] in prefix) and R[j] (count of a[j] in suffix). The problem becomes: count pairs (i,j) with i < j and L[i] > R[j]. This is a modified inversion count, solvable with BIT: process right-to-left, for each position count how many larger indices have smaller R values.

---

### Prime Cut

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

A prime number is a counting number that is evenly divisible only by 1 and itself. Given N and C:
- Find all prime numbers between 1 and N (inclusive), treating 1 as prime for this problem
- Print 2C prime numbers from the center if the list has even length
- Print 2C-1 prime numbers from the center if the list has odd length
- If the center list exceeds the prime list bounds, print all primes

#### Input Format
- Multiple test cases, each on one line
- Each line: N (1 ≤ N ≤ 1000) and C (1 ≤ C ≤ N)

#### Output Format
For each test case: "N C: p1 p2 ... pk" followed by a blank line, where p1...pk are the center primes.

#### Solution

##### Approach
1. Use Sieve of Eratosthenes to precompute all primes up to 1000
2. Note: This problem considers 1 as a prime number
3. For each query, find primes ≤ N, then extract center elements

##### Python Solution

```python
def sieve(n):
  """Sieve of Eratosthenes - returns primes up to n, including 1"""
  is_prime = [True] * (n + 1)
  is_prime[0] = False
  if n >= 1:
    is_prime[1] = True  # Treat 1 as prime for this problem

  for i in range(2, int(n**0.5) + 1):
    if is_prime[i]:
      for j in range(i*i, n + 1, i):
        is_prime[j] = False

  return [i for i in range(n + 1) if is_prime[i]]

def solve():
  # Precompute primes up to 1000
  all_primes = sieve(1000)

  import sys
  for line in sys.stdin:
    parts = line.split()
    if len(parts) < 2:
      continue

    n, c = int(parts[0]), int(parts[1])

    # Get primes <= n
    primes = [p for p in all_primes if p <= n]
    length = len(primes)

    # Determine how many to print
    if length % 2 == 0:
      count = 2 * c
    else:
      count = 2 * c - 1

    # If count exceeds list, print all
    if count >= length:
      result = primes
    else:
      # Find center elements
      start = (length - count) // 2
      result = primes[start:start + count]

    print(f"{n} {c}:", ' '.join(map(str, result)))
    print()

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  # Sieve including 1 as "prime"
  MAX_N = 1000
  is_prime = [True] * (MAX_N + 1)
  is_prime[0] = False

  for i in range(2, int(MAX_N**0.5) + 1):
    if is_prime[i]:
      for j in range(i*i, MAX_N + 1, i):
        is_prime[j] = False

  primes = [1] + [i for i in range(2, MAX_N + 1) if is_prime[i]]

  import sys
  for line in sys.stdin:
    try:
      n, c = map(int, line.split())
    except:
      continue

    # Find primes up to n
    idx = 0
    while idx < len(primes) and primes[idx] <= n:
      idx += 1
    prime_list = primes[:idx]
    L = len(prime_list)

    # Calculate center range
    center_count = 2 * c if L % 2 == 0 else 2 * c - 1
    center_count = min(center_count, L)

    start = (L - center_count) // 2
    end = start + center_count

    result = prime_list[start:end]
    print(f"{n} {c}:", ' '.join(map(str, result)))
    print()

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N log log N) for sieve preprocessing, O(1) per query
- **Space Complexity:** O(N) for storing primes

##### Key Insight
This problem unusually treats 1 as a prime number. The main challenge is correctly computing the center slice:
- For even-length list: take 2C elements centered
- For odd-length list: take 2C-1 elements centered
- Start index = (length - count) // 2

---

### Send a Table

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Jimmy needs to precompute a function Answer(x, y) for x, y in [1, N]. He discovered that if gcd(x, y) = k, then Answer(x, y) can be derived from Answer(x/k, y/k).

For N = 4, the 16 possible inputs reduce to 11 unique cases (after GCD reduction):
- Direct cases: (1,1), (1,2), (2,1), (1,3), (3,1), (1,4), (4,1), (2,3), (3,2), (3,4), (4,3)

Given N, count how many Answer values Jimmy needs to precompute.

#### Input Format
- Up to 600 lines
- Each line: integer N (< 50001)
- Input ends with 0

#### Output Format
For each N, print the count of required precomputed values.

#### Solution

##### Approach
We need to count pairs (x, y) where 1 ≤ x, y ≤ N and gcd(x, y) = 1.

This equals: 2 × Σφ(k) for k from 1 to N, minus 1 (to not double count (1,1)).

Or: count = 2 × (Σφ(k) for k=1 to N) - 1

Since pairs (x,y) and (y,x) are different unless x=y, and the only coprime pair with x=y is (1,1).

##### Python Solution

```python
def solve():
  MAX = 50001

  # Compute Euler's totient for all numbers up to MAX
  phi = list(range(MAX))

  for i in range(2, MAX):
    if phi[i] == i:  # i is prime
      for j in range(i, MAX, i):
        phi[j] -= phi[j] // i

  # Precompute prefix sums
  prefix = [0] * MAX
  for i in range(1, MAX):
    prefix[i] = prefix[i-1] + phi[i]

  # Answer for N is 2 * prefix[N] - 1
  # Because pairs (x,y) with gcd=1 counted twice except (1,1)

  import sys
  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      break

    # Count coprime pairs (x, y) with 1 <= x, y <= n
    # = 2 * sum(phi[1..n]) - 1
    result = 2 * prefix[n] - 1
    print(result)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  MAX = 50001

  # Sieve to compute phi
  phi = list(range(MAX))

  for i in range(2, MAX):
    if phi[i] == i:  # i is prime
      for j in range(i, MAX, i):
        phi[j] = phi[j] // i * (i - 1)

  # Prefix sum of phi values
  total = [0] * MAX
  for i in range(1, MAX):
    total[i] = total[i-1] + phi[i]

  while True:
    n = int(input())
    if n == 0:
      break

    # Coprime pairs in [1,N] x [1,N]
    # For each k, phi[k] counts numbers in [1,k-1] coprime with k
    # Plus 1 for the pair (k, k) when k=1

    # Total coprime ordered pairs = 2 * sum(phi[1..N]) - 1
    print(2 * total[n] - 1)

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  MAX = 50001

  # Linear sieve for phi
  phi = [0] * MAX
  phi[1] = 1

  for i in range(2, MAX):
    if phi[i] == 0:  # i is prime
      phi[i] = i - 1
      for j in range(2 * i, MAX, i):
        if phi[j] == 0:
          phi[j] = j
        phi[j] = phi[j] // i * (i - 1)

  # Handle remaining unset values
  for i in range(2, MAX):
    if phi[i] == 0:
      phi[i] = i - 1  # i is prime

  # Cumulative sum
  cumsum = [0] * MAX
  for i in range(1, MAX):
    cumsum[i] = cumsum[i-1] + phi[i]

  import sys
  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      break
    print(2 * cumsum[n] - 1)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N log log N) for sieve, O(1) per query
- **Space Complexity:** O(N)

##### Key Insight
Pairs (x, y) that reduce to a canonical form via GCD are exactly coprime pairs. Count of coprime pairs in [1,N]² equals the sum of φ(k) for k=1 to N, counted twice for (x,y) and (y,x), except (1,1) which appears once. Formula: 2 × Σφ(k) - 1.

