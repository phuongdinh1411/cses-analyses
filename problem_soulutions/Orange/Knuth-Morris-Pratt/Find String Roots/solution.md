# Find String Roots

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

The Nth root of a string S is a string T such that T concatenated N times equals S. For example:
- S = "abcabcabcabc" has 4th root T = "abc"
- For N = 2, the 2nd root is "abcabc"
- For N = 1, any string S is its own 1st root

Find the maximum N such that the Nth root of S exists.

## Input Format
- Multiple test cases, one per line
- Each line: a non-empty string S (≤ 10⁵ characters)
- Input ends with "*"

## Output Format
For each test case, print the greatest N such that the Nth root exists.

## Solution

### Approach
Use KMP failure function. If the string has period P, then N = len(S) / P.
The period P = len(S) - failure[len(S)-1].
N is valid only if len(S) is divisible by P.

### Python Solution

```python
def compute_failure(s):
  """KMP failure function"""
  n = len(s)
  fail = [0] * n

  for i in range(1, n):
    j = fail[i - 1]
    while j > 0 and s[i] != s[j]:
      j = fail[j - 1]
    if s[i] == s[j]:
      j += 1
    fail[i] = j

  return fail

def solve():
  while True:
    s = input().strip()
    if s == '*':
      break

    n = len(s)
    fail = compute_failure(s)

    # Period of the string
    period = n - fail[n - 1]

    # Check if n is divisible by period
    if n % period == 0:
      print(n // period)
    else:
      print(1)

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  while True:
    s = input().strip()
    if s == '*':
      break

    n = len(s)

    # Build KMP prefix function
    pi = [0] * n
    for i in range(1, n):
      j = pi[i - 1]
      while j > 0 and s[i] != s[j]:
        j = pi[j - 1]
      if s[i] == s[j]:
        j += 1
      pi[i] = j

    # The smallest period is n - pi[n-1]
    # If n is divisible by this period, that's our answer
    smallest_period = n - pi[n - 1]

    if n % smallest_period == 0:
      print(n // smallest_period)
    else:
      print(1)  # String is not periodic, only 1st root exists

if __name__ == "__main__":
  solve()
```

### One-liner Style

```python
def kmp_period(s):
  n = len(s)
  pi = [0] * n
  for i in range(1, n):
    j = pi[i-1]
    while j and s[i] != s[j]: j = pi[j-1]
    pi[i] = j + (s[i] == s[j])
  p = n - pi[-1]
  return n // p if n % p == 0 else 1

while True:
  s = input().strip()
  if s == '*': break
  print(kmp_period(s))
```

### Complexity Analysis
- **Time Complexity:** O(|S|) per string
- **Space Complexity:** O(|S|) for failure array

### Key Insight
The KMP failure function reveals the string's periodic structure. If fail[n-1] = k, then the first k characters match the last k characters, meaning the string has period (n-k). The maximum N is n/period if n is divisible by the period.
