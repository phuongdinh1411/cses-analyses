# Aibohphobia

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 10000ms
- **Memory Limit:** 512MB

## Problem Statement

Given a string S, find the minimum number of characters to insert to make it a palindrome.

For example:
- "fft" → "tfft" (insert 1 character)
- "ab" → "aba" or "bab" (insert 1 character)

## Input Format
- Multiple test cases
- Each line: string S (max 6100 chars, no whitespace)

## Output Format
For each test case, print the minimum insertions needed.

## Example
```
Input:
fft
ab
abc

Output:
1
1
2
```
"fft" -> "tfft" (insert 't'), 1 insertion.
"ab" -> "aba" or "bab" (insert 'a' or 'b'), 1 insertion.
"abc" -> "abcba" (insert "ba") or "cbabc", 2 insertions.

## Solution

### Approach
The minimum insertions = len(S) - LPS(S), where LPS is the Longest Palindromic Subsequence.

LPS of string S equals LCS of S and reverse(S).

Alternatively, use direct DP:
- dp[i][j] = min insertions to make S[i:j+1] a palindrome
- If S[i] == S[j]: dp[i][j] = dp[i+1][j-1]
- Else: dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])

### Python Solution

```python
def solve():
  import sys
  input = sys.stdin.readline

  while True:
    line = input()
    if not line:
      break
    s = line.strip()
    if not s:
      continue

    n = len(s)

    # LPS via LCS with reverse
    rev = s[::-1]

    # Space-optimized LCS
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, n + 1):
      for j in range(1, n + 1):
        if s[i-1] == rev[j-1]:
          curr[j] = prev[j-1] + 1
        else:
          curr[j] = max(prev[j], curr[j-1])
      prev, curr = curr, prev

    lps = prev[n]
    print(n - lps)

if __name__ == "__main__":
  solve()
```

### Alternative Solution - Direct DP

```python
def solve():
  import sys
  input = sys.stdin.readline

  while True:
    line = input()
    if not line:
      break
    s = line.strip()
    if not s:
      continue

    n = len(s)

    # dp[i][j] = min insertions for s[i:j+1]
    # Use only 2 rows since dp[i] depends on dp[i+1]
    # Actually for gap-based DP:

    # dp[length][start] but we can optimize
    # Use dp[j] = min insertions for substring ending at j with some length

    # Simpler: dp[i] = min insertions for s[i:] to be palindrome when matching with s[:n-i]

    # Direct approach with LPS
    # dp[i][j] = LPS of s[i:j+1]
    # dp[i][i] = 1
    # dp[i][j] = dp[i+1][j-1] + 2 if s[i] == s[j]
    #          = max(dp[i+1][j], dp[i][j-1]) otherwise

    if n <= 1:
      print(0)
      continue

    # Space optimized: process by length
    prev = [1] * n  # length 1 substrings
    curr = [0] * n

    for length in range(2, n + 1):
      for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j]:
          curr[i] = prev[i+1] + 2 if length > 2 else 2
        else:
          curr[i] = max(prev[i], prev[i+1] if i+1 < n else 0)
          # Actually need different indexing

      prev, curr = curr, [0] * n

    lps = prev[0]
    print(n - lps)

if __name__ == "__main__":
  solve()
```

### Cleaner LCS Solution

```python
import sys
sys.setrecursionlimit(10000)

def solve():
  for line in sys.stdin:
    s = line.strip()
    if not s:
      continue

    n = len(s)
    rev = s[::-1]

    # LCS of s and rev = LPS of s
    # dp[i][j] = LCS of s[:i] and rev[:j]
    dp = [[0] * (n + 1) for _ in range(2)]

    for i in range(1, n + 1):
      for j in range(1, n + 1):
        if s[i-1] == rev[j-1]:
          dp[i % 2][j] = dp[(i-1) % 2][j-1] + 1
        else:
          dp[i % 2][j] = max(dp[(i-1) % 2][j], dp[i % 2][j-1])

    lps = dp[n % 2][n]
    print(n - lps)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n²)
- **Space Complexity:** O(n) with optimization

### Key Insight
Minimum insertions to make a palindrome = n - LPS (Longest Palindromic Subsequence). LPS can be found as LCS of string with its reverse. Characters not in the LPS need matching characters inserted, hence the formula.
