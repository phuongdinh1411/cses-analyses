# Advanced Fruits

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Create a shortest name for a new fruit that contains both original fruit names as substrings. For example, "apple" and "pear" can combine to "applear" (contains both "apple" and "pear").

## Input Format
- Multiple test cases until EOF
- Each line: two fruit names (alphabetic, max 100 chars each)

## Output Format
For each test case, output the shortest combined name.

## Solution

### Approach
This is the Shortest Common Supersequence (SCS) problem. The SCS length is:
`len(A) + len(B) - LCS(A, B)`

To construct the SCS:
1. Compute LCS DP table
2. Backtrack to build the result, including non-LCS characters

### Python Solution

```python
def shortest_supersequence(a, b):
 m, n = len(a), len(b)

 # LCS DP table
 dp = [[0] * (n + 1) for _ in range(m + 1)]

 for i in range(1, m + 1):
  for j in range(1, n + 1):
   if a[i-1] == b[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
   else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

 # Backtrack to construct SCS
 result = []
 i, j = m, n

 while i > 0 and j > 0:
  if a[i-1] == b[j-1]:
   result.append(a[i-1])
   i -= 1
   j -= 1
  elif dp[i-1][j] > dp[i][j-1]:
   result.append(a[i-1])
   i -= 1
  else:
   result.append(b[j-1])
   j -= 1

 # Add remaining characters
 while i > 0:
  result.append(a[i-1])
  i -= 1
 while j > 0:
  result.append(b[j-1])
  j -= 1

 return ''.join(reversed(result))

def solve():
 import sys
 for line in sys.stdin:
  parts = line.strip().split()
  if len(parts) < 2:
   continue
  a, b = parts[0], parts[1]
  print(shortest_supersequence(a, b))

if __name__ == "__main__":
 solve()
```

### Alternative Solution - Direct SCS DP

```python
def solve():
 import sys
 for line in sys.stdin:
  parts = line.strip().split()
  if len(parts) < 2:
   continue
  a, b = parts[0], parts[1]

  m, n = len(a), len(b)

  # dp[i][j] = shortest supersequence of a[:i] and b[:j]
  dp = [[""] * (n + 1) for _ in range(m + 1)]

  # Base cases
  for i in range(1, m + 1):
   dp[i][0] = a[:i]
  for j in range(1, n + 1):
   dp[0][j] = b[:j]

  for i in range(1, m + 1):
   for j in range(1, n + 1):
    if a[i-1] == b[j-1]:
     dp[i][j] = dp[i-1][j-1] + a[i-1]
    else:
     if len(dp[i-1][j]) < len(dp[i][j-1]):
      dp[i][j] = dp[i-1][j] + a[i-1]
     else:
      dp[i][j] = dp[i][j-1] + b[j-1]

  print(dp[m][n])

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(m × n)
- **Space Complexity:** O(m × n)

### Key Insight
The Shortest Common Supersequence is the inverse of LCS. We want the shortest string containing both inputs as subsequences. By finding LCS, we know which characters can be shared, then merge the rest in order. The backtracking builds the SCS by including LCS characters once and non-LCS characters from both strings.
