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
Generate every anagrammatic prime below 10⁷ once, then answer each query with a scan.

1. With two or more digits, every digit must be 1, 3, 7 or 9. Otherwise some permutation ends in an even digit or in 5.
2. Enumerate digit multisets over {1, 3, 7, 9} with up to 7 digits (each multiset once), and keep those whose permutations are all prime.
3. For a query n, the limit is `10 ** len(str(n))`. Print the first listed prime p with n < p < limit, or 0 if there is none.

Below 10⁷ the full list is 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, 97, 113, 131, 199, 311, 337, 373, 733, 919, 991. The next one is the repunit R19.

##### Python Solution

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

##### Complexity Analysis
- **Time Complexity:** precomputation tests at most 4⁷ digit strings, then O(22) per query
- **Space Complexity:** O(1)

##### Key Insight
Anagrammatic (permutable) primes are rare: 22 exist below 10⁷, none with 4 to 7 digits. The digit rule shrinks the search to 4⁷ candidates, so precomputing is instant. So every query with n ≥ 991 answers 0.

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
Big rocks and the two banks can be used on both trips, so list each of them twice. A small rock can be used once, so list it once. Sort the list.

In an optimal plan the two trips alternate through this sorted list: one trip lands on even indices, the other on odd ones. Each jump therefore spans two consecutive list entries, and the answer is `max(stones[i+2] - stones[i])`.

The intuitive plan of using every rock going and only big rocks returning is wrong. With D = 10 and small rocks at 3 and 6, it gives 10, while splitting the small rocks gives 7.

##### Python Solution

```python
import sys


def solve():
  data = sys.stdin.read().split()
  idx = 0
  t = int(data[idx]); idx += 1

  for case in range(1, t + 1):
    n, d = int(data[idx]), int(data[idx + 1]); idx += 2

    # Big rocks serve both trips, so list them twice; banks too.
    stones = [0, 0, d, d]
    for rock in data[idx:idx + n]:
      kind, pos = rock[0], int(rock[2:])
      stones += [pos, pos] if kind == 'B' else [pos]
    idx += n
    stones.sort()

    # Alternate stones between the two trips: trip one takes even indices, trip two odd ones.
    best = max(stones[i + 2] - stones[i] for i in range(len(stones) - 2))
    print(f"Case {case}: {best}")


if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for sorting
- **Space Complexity:** O(N)

##### Key Insight
Duplicate every stone that both trips may use, then let the trips alternate. The worst jump is the largest gap between list entries two apart.

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

