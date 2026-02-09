# Ones

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

For any integer n (not divisible by 2 or 5), find the smallest number consisting only of 1s that is divisible by n.

Output the number of digits in this smallest "repunit".

## Input Format
- Multiple test cases until EOF
- Each line: integer n (0 < n ≤ 10000, not divisible by 2 or 5)

## Output Format
For each n, print the number of 1s in the smallest repunit divisible by n.

## Example
```
Input:
3
7

Output:
3
6
```
For n=3: The smallest repunit divisible by 3 is 111 (3 ones), since 111 = 3 x 37.
For n=7: The smallest repunit divisible by 7 is 111111 (6 ones), since 111111 = 7 x 15873.

## Solution

### Approach
A repunit with k digits is: (10^k - 1) / 9

We need the smallest k such that n divides (10^k - 1) / 9.

Since gcd(n, 9) might not be 1, we work with: find smallest k where 10^k ≡ 1 (mod 9n/gcd(9,n))

Simpler approach: directly compute remainders.
- Start with remainder = 1
- Keep appending 1s: remainder = (remainder * 10 + 1) % n
- Count until remainder = 0

### Python Solution

```python
def solve():
  import sys

  for line in sys.stdin:
    n = int(line.strip())
    if n == 0:
      continue

    # Find smallest repunit divisible by n
    # repunit(k) = 111...1 (k ones) = (10^k - 1) / 9

    remainder = 1 % n
    count = 1

    while remainder != 0:
      remainder = (remainder * 10 + 1) % n
      count += 1

    print(count)

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Explanation

```python
def min_repunit_digits(n):
  """
  Find minimum k such that 111...1 (k ones) is divisible by n.

  The number with k ones is: (10^k - 1) / 9

  We iterate: r_1 = 1, r_k = r_{k-1} * 10 + 1
  Stop when r_k ≡ 0 (mod n)
  """
  if n == 1:
    return 1

  remainder = 1
  digits = 1

  while remainder % n != 0:
    remainder = (remainder * 10 + 1) % n
    digits += 1

  return digits

def solve():
  import sys
  for line in sys.stdin:
    line = line.strip()
    if not line:
      continue
    n = int(line)
    print(min_repunit_digits(n))

if __name__ == "__main__":
  solve()
```

### Mathematical Insight Solution

```python
def solve():
  """
  For n not divisible by 2 or 5, a repunit divisible by n always exists.

  By pigeonhole principle, since there are only n possible remainders,
  within n+1 iterations we must find a repeat, and since we start at 1,
  we'll eventually hit 0.
  """
  import sys

  for line in sys.stdin:
    n = int(line.strip())

    r = 1
    k = 1

    while r != 0:
      r = (r * 10 + 1) % n
      k += 1

    print(k)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n) per test case (at most n iterations by pigeonhole)
- **Space Complexity:** O(1)

### Key Insight
A repunit 111...1 with k digits equals (10^k - 1)/9. Since n is coprime with 10 (not divisible by 2 or 5), by Fermat's little theorem a solution exists. We simulate building the repunit digit by digit, tracking remainder mod n, until we find remainder 0.
