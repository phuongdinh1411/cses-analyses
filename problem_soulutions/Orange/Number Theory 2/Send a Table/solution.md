# Send a Table

## Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Jimmy needs to precompute a function Answer(x, y) for x, y in [1, N]. He discovered that if gcd(x, y) = k, then Answer(x, y) can be derived from Answer(x/k, y/k).

For N = 4, the 16 possible inputs reduce to 11 unique cases (after GCD reduction):
- Direct cases: (1,1), (1,2), (2,1), (1,3), (3,1), (1,4), (4,1), (2,3), (3,2), (3,4), (4,3)

Given N, count how many Answer values Jimmy needs to precompute.

## Input Format
- Up to 600 lines
- Each line: integer N (< 50001)
- Input ends with 0

## Output Format
For each N, print the count of required precomputed values.

## Example
```
Input:
4
2
0

Output:
11
3
```
For N=4: Count of coprime pairs (x,y) where 1 <= x,y <= 4. These are: (1,1), (1,2), (2,1), (1,3), (3,1), (1,4), (4,1), (2,3), (3,2), (3,4), (4,3) = 11 pairs.
For N=2: Coprime pairs are (1,1), (1,2), (2,1) = 3 pairs.

## Solution

### Approach
We need to count pairs (x, y) where 1 ≤ x, y ≤ N and gcd(x, y) = 1.

This equals: 2 × Σφ(k) for k from 1 to N, minus 1 (to not double count (1,1)).

Or: count = 2 × (Σφ(k) for k=1 to N) - 1

Since pairs (x,y) and (y,x) are different unless x=y, and the only coprime pair with x=y is (1,1).

### Python Solution

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

### Alternative Solution

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

### Optimized Sieve

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

### Complexity Analysis
- **Time Complexity:** O(N log log N) for sieve, O(1) per query
- **Space Complexity:** O(N)

### Key Insight
Pairs (x, y) that reduce to a canonical form via GCD are exactly coprime pairs. Count of coprime pairs in [1,N]² equals the sum of φ(k) for k=1 to N, counted twice for (x,y) and (y,x), except (1,1) which appears once. Formula: 2 × Σφ(k) - 1.
