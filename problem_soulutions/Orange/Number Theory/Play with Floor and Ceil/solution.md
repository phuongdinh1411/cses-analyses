# Play with Floor and Ceil

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

For any integers x and k, there exist integers p and q such that:
x = p × floor(x/k) + q × ceil(x/k)

Given x and k, find p and q.

## Input Format
- T test cases (1 ≤ T ≤ 1000)
- Each test case: two positive integers x and k (< 10^8)

## Output Format
For each test case, print p and q (space-separated).

## Solution

### Approach
Let a = floor(x/k) and b = ceil(x/k).

If x is divisible by k: a = b = x/k, so x = (x/k) × k means p + q = k works.
Simple solution: p = k, q = 0.

If x is not divisible by k: b = a + 1.
We need: p × a + q × (a + 1) = x
→ (p + q) × a + q = x
→ p × a + q × a + q = x

Using Extended Euclidean Algorithm to solve: p × a + q × b = x
Since gcd(a, b) = gcd(a, a+1) = 1, solution always exists.

### Python Solution

```python
def extended_gcd(a, b):
 """Returns (gcd, x, y) such that a*x + b*y = gcd"""
 if b == 0:
  return a, 1, 0
 gcd, x1, y1 = extended_gcd(b, a % b)
 x = y1
 y = x1 - (a // b) * y1
 return gcd, x, y

def solve():
 t = int(input())

 for _ in range(t):
  x, k = map(int, input().split())

  a = x // k          # floor(x/k)
  b = (x + k - 1) // k  # ceil(x/k)

  if a == b:
   # x is divisible by k
   # x = p*a + q*a = (p+q)*a
   # So p + q = x/a = k
   print(k, 0)
  else:
   # a and b differ by 1, gcd(a, b) = 1
   # Solve p*a + q*b = x using extended Euclidean
   gcd, p0, q0 = extended_gcd(a, b)

   # p0*a + q0*b = 1
   # So (p0*x)*a + (q0*x)*b = x
   p = p0 * x
   q = q0 * x

   print(p, q)

if __name__ == "__main__":
 solve()
```

### Alternative Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  x, k = map(int, input().split())

  floor_val = x // k
  ceil_val = -(-x // k)  # Ceiling division trick

  if floor_val == ceil_val:
   # x divisible by k
   print(k, 0)
  else:
   # floor_val and ceil_val differ by 1
   # ceil_val = floor_val + 1
   # Need: p * floor_val + q * (floor_val + 1) = x
   # Let r = x % k (remainder)
   # Then x = floor_val * k + r
   # And ceil_val = floor_val + 1

   # p * floor_val + q * ceil_val = x
   # With gcd = 1, use extended Euclidean
   a, b = floor_val, ceil_val

   # Extended GCD for consecutive integers
   # gcd(a, a+1) = 1
   # a*1 + (a+1)*(-a) + (a+1) = a - a^2 - a + a + 1 = 1
   # So: a*(-a) + (a+1)*(a+1-1) = a*(-a) + (a+1)*a = -a^2 + a^2 + a = a... wrong

   # Direct: a*1 + b*0 when b=a (not applicable here)
   # For a, a+1: 1 = (a+1) - a = a*(-1) + (a+1)*1
   # So p0 = -1, q0 = 1 gives a*(-1) + (a+1)*1 = 1

   p = -x
   q = x

   print(p, q)

if __name__ == "__main__":
 solve()
```

### Simplified Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  x, k = map(int, input().split())

  a = x // k  # floor
  b = (x + k - 1) // k  # ceil

  if a == b:
   print(k, 0)
  else:
   # gcd(a, a+1) = 1
   # a * (-1) + (a+1) * 1 = 1
   # Multiply by x: a * (-x) + (a+1) * x = x
   print(-x, x)

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(1) per test case
- **Space Complexity:** O(1)

### Key Insight
When floor(x/k) ≠ ceil(x/k), they differ by exactly 1, making gcd = 1. For consecutive integers a and a+1: a×(-1) + (a+1)×1 = 1. Multiply by x to get the solution: p = -x, q = x. When floor = ceil, x is divisible by k, and p = k, q = 0 works.
