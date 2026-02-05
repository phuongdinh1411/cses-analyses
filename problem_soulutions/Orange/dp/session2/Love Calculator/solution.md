# Love Calculator

## Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Given two names, find:
1. The length of the shortest string containing both names as subsequences
2. The number of such shortest strings

## Input Format
- T test cases (T ≤ 125)
- Each test case: two lines with names (≤ 30 capital letters each)

## Output Format
For each test case: "Case X: L C" where L is shortest length and C is count of unique shortest strings.

## Solution

### Approach
This is the Shortest Common Supersequence (SCS) problem with counting.

1. Length = len(A) + len(B) - LCS(A, B)
2. Count requires counting all optimal paths in the LCS DP table

Use two DP tables:
- dp[i][j] = LCS length of A[:i] and B[:j]
- cnt[i][j] = number of ways to achieve SCS of A[:i] and B[:j]

### Python Solution

```python
def solve():
 t = int(input())

 for case in range(1, t + 1):
  a = input().strip()
  b = input().strip()

  m, n = len(a), len(b)

  # LCS DP
  lcs = [[0] * (n + 1) for _ in range(m + 1)]

  for i in range(1, m + 1):
   for j in range(1, n + 1):
    if a[i-1] == b[j-1]:
     lcs[i][j] = lcs[i-1][j-1] + 1
    else:
     lcs[i][j] = max(lcs[i-1][j], lcs[i][j-1])

  # SCS length
  scs_len = m + n - lcs[m][n]

  # Count SCS: cnt[i][j] = ways to form SCS of a[:i] and b[:j]
  cnt = [[0] * (n + 1) for _ in range(m + 1)]
  cnt[0][0] = 1

  # Base cases
  for i in range(1, m + 1):
   cnt[i][0] = 1
  for j in range(1, n + 1):
   cnt[0][j] = 1

  for i in range(1, m + 1):
   for j in range(1, n + 1):
    if a[i-1] == b[j-1]:
     # Must take this character (extends LCS)
     cnt[i][j] = cnt[i-1][j-1]
    else:
     # Choose which character to append
     # Only count paths that maintain optimal LCS
     if lcs[i-1][j] > lcs[i][j-1]:
      cnt[i][j] = cnt[i-1][j]
     elif lcs[i][j-1] > lcs[i-1][j]:
      cnt[i][j] = cnt[i][j-1]
     else:
      cnt[i][j] = cnt[i-1][j] + cnt[i][j-1]

  print(f"Case {case}: {scs_len} {cnt[m][n]}")

if __name__ == "__main__":
 solve()
```

### Alternative Solution with Explanation

```python
def solve():
 t = int(input())

 for case in range(1, t + 1):
  a = input().strip()
  b = input().strip()

  m, n = len(a), len(b)

  # dp[i][j] = (scs_length, count) for a[:i] and b[:j]
  # scs_length = i + j - lcs[i][j]

  lcs = [[0] * (n + 1) for _ in range(m + 1)]
  cnt = [[0] * (n + 1) for _ in range(m + 1)]

  # Base: empty strings
  cnt[0][0] = 1
  for i in range(1, m + 1):
   cnt[i][0] = 1  # Only one way: use all of a
  for j in range(1, n + 1):
   cnt[0][j] = 1  # Only one way: use all of b

  for i in range(1, m + 1):
   for j in range(1, n + 1):
    if a[i-1] == b[j-1]:
     lcs[i][j] = lcs[i-1][j-1] + 1
     cnt[i][j] = cnt[i-1][j-1]
    else:
     lcs[i][j] = max(lcs[i-1][j], lcs[i][j-1])

     if lcs[i-1][j] > lcs[i][j-1]:
      cnt[i][j] = cnt[i-1][j]
     elif lcs[i][j-1] > lcs[i-1][j]:
      cnt[i][j] = cnt[i][j-1]
     else:
      cnt[i][j] = cnt[i-1][j] + cnt[i][j-1]

  scs_len = m + n - lcs[m][n]
  print(f"Case {case}: {scs_len} {cnt[m][n]}")

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(m × n)
- **Space Complexity:** O(m × n)

### Key Insight
SCS length = len(A) + len(B) - LCS(A,B). For counting, when characters match we must use that match (one path). When they don't match, we can go either direction if both give optimal LCS, so we add the counts. This counts distinct ways to interleave non-LCS characters while maintaining order.
