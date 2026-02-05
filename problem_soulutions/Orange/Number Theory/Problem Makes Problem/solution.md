# Problem Makes Problem

## Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

How many ways can you make n by adding k non-negative integers?

For example, n=4 with k=3 has 15 solutions (like 0+0+4, 0+1+3, 1+1+2, etc.).

## Input Format
- T test cases
- Each test case: two integers n and k

## Output Format
For each test case, print the number of ways modulo 10^9+7.

## Solution

### Approach
This is the Stars and Bars combinatorics problem.

The number of ways to distribute n identical items into k distinct bins (where bins can be empty) is:
C(n + k - 1, k - 1) = C(n + k - 1, n)

Use modular arithmetic and precompute factorials for efficient computation.

### Python Solution

```python
def solve():
  MOD = 10**9 + 7
  MAX = 2 * 10**6 + 10

  # Precompute factorials and inverse factorials
  fact = [1] * MAX
  for i in range(1, MAX):
    fact[i] = fact[i-1] * i % MOD

  # Modular inverse using Fermat's little theorem
  inv_fact = [1] * MAX
  inv_fact[MAX-1] = pow(fact[MAX-1], MOD-2, MOD)
  for i in range(MAX-2, -1, -1):
    inv_fact[i] = inv_fact[i+1] * (i+1) % MOD

  def nCr(n, r):
    if r < 0 or r > n:
      return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD

  t = int(input())
  for case in range(1, t+1):
    n, k = map(int, input().split())

    # Stars and Bars: C(n + k - 1, k - 1)
    result = nCr(n + k - 1, k - 1)
    print(f"Case {case}: {result}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  MOD = 10**9 + 7

  # Precompute
  MAXN = 2000005
  fact = [1] * MAXN
  inv = [1] * MAXN
  inv_fact = [1] * MAXN

  for i in range(2, MAXN):
    fact[i] = fact[i-1] * i % MOD
    inv[i] = (MOD - MOD // i) * inv[MOD % i] % MOD
    inv_fact[i] = inv_fact[i-1] * inv[i] % MOD

  def C(n, k):
    if k < 0 or k > n:
      return 0
    return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD

  t = int(input())
  for case in range(1, t + 1):
    n, k = map(int, input().split())
    # Ways = C(n+k-1, k-1)
    ans = C(n + k - 1, k - 1)
    print(f"Case {case}: {ans}")

if __name__ == "__main__":
  solve()
```

### Lucas Theorem Solution (for larger moduli)

```python
def solve():
  MOD = 10**9 + 7

  def power(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
      if exp & 1:
        result = result * base % mod
      exp >>= 1
      base = base * base % mod
    return result

  def mod_inverse(a, mod):
    return power(a, mod - 2, mod)

  # Precompute factorials up to expected max
  MAX = 2 * 10**6 + 5
  fact = [1] * MAX
  for i in range(1, MAX):
    fact[i] = fact[i-1] * i % MOD

  inv_fact = [1] * MAX
  inv_fact[MAX-1] = mod_inverse(fact[MAX-1], MOD)
  for i in range(MAX-2, -1, -1):
    inv_fact[i] = inv_fact[i+1] * (i+1) % MOD

  def nCr(n, r):
    if r > n or r < 0:
      return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD

  t = int(input())
  for case in range(1, t+1):
    n, k = map(int, input().split())
    print(f"Case {case}: {nCr(n + k - 1, k - 1)}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(MAX) for precomputation, O(1) per query
- **Space Complexity:** O(MAX)

### Key Insight
This is the classic "Stars and Bars" combinatorics problem. We need to place n identical objects (stars) into k bins using k-1 dividers (bars). The total positions are n + k - 1, and we choose k - 1 for bars (or equivalently n for stars): C(n + k - 1, k - 1).
