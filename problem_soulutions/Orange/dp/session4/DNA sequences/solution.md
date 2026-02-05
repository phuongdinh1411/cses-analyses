# DNA sequences

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Find the longest common subsequence of two strings where the subsequence must be formed by consecutive segments of length at least K from both strings.

For example, with K=3 and strings "lovxxelyxxxxx" and "xxxxxxxlovely":
- "lovely" is not valid (segment "lov" has length 3, but other segments don't)
- "loxxxelyxxxxx" is valid if all matching segments have length ≥ K

## Input Format
- Multiple test cases until line with 0
- Each test case:
  - First line: K (minimum segment length)
  - Next two lines: the two strings (lowercase, length ≤ 1000)

## Output Format
For each test case, print the length of the longest valid subsequence, or 0 if none exists.

## Solution

### Approach
Modified LCS where we track consecutive matches:
- dp[i][j][len] = whether we can match with current segment of length `len`
- Or simpler: dp[i][j] = length of current matching segment ending at (i,j)
- Keep track of best valid subsequence length

### Python Solution

```python
def solve():
 while True:
  k = int(input())
  if k == 0:
   break

  s1 = input().strip()
  s2 = input().strip()

  n, m = len(s1), len(s2)

  # dp[i][j] = length of consecutive match ending at s1[i-1], s2[j-1]
  # best[i][j] = best valid LCS length ending before or at (i,j)
  dp = [[0] * (m + 1) for _ in range(n + 1)]
  best = [[0] * (m + 1) for _ in range(n + 1)]

  result = 0

  for i in range(1, n + 1):
   for j in range(1, m + 1):
    # Update best from previous positions
    best[i][j] = max(best[i-1][j], best[i][j-1])

    if s1[i-1] == s2[j-1]:
     dp[i][j] = dp[i-1][j-1] + 1

     # If segment length >= k, it's valid
     if dp[i][j] >= k:
      # Can extend previous best by segment length
      # best[i-dp[i][j]][j-dp[i][j]] + dp[i][j]
      seg_start_i = i - dp[i][j]
      seg_start_j = j - dp[i][j]
      candidate = best[seg_start_i][seg_start_j] + dp[i][j]
      best[i][j] = max(best[i][j], candidate)
      result = max(result, best[i][j])
    else:
     dp[i][j] = 0

  print(result)

if __name__ == "__main__":
 solve()
```

### Alternative Solution

```python
def solve():
 while True:
  k = int(input())
  if k == 0:
   break

  s1 = input().strip()
  s2 = input().strip()

  n, m = len(s1), len(s2)

  # match[i][j] = length of matching segment ending at i,j
  match = [[0] * (m + 1) for _ in range(n + 1)]

  # dp[i][j] = max LCS with valid segments ending at or before i,j
  dp = [[0] * (m + 1) for _ in range(n + 1)]

  for i in range(1, n + 1):
   for j in range(1, m + 1):
    # Propagate best from neighbors
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    if s1[i-1] == s2[j-1]:
     match[i][j] = match[i-1][j-1] + 1

     # Check all valid segment lengths >= k
     for seg_len in range(k, match[i][j] + 1):
      prev_i = i - seg_len
      prev_j = j - seg_len
      dp[i][j] = max(dp[i][j], dp[prev_i][prev_j] + seg_len)

  print(dp[n][m])

if __name__ == "__main__":
 solve()
```

### Optimized Solution

```python
def solve():
 while True:
  k = int(input())
  if k == 0:
   break

  s1 = input().strip()
  s2 = input().strip()

  n, m = len(s1), len(s2)

  # match[i][j] = consecutive match length ending at i-1, j-1
  match = [[0] * (m + 1) for _ in range(n + 1)]
  dp = [[0] * (m + 1) for _ in range(n + 1)]

  for i in range(1, n + 1):
   for j in range(1, m + 1):
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    if s1[i-1] == s2[j-1]:
     match[i][j] = match[i-1][j-1] + 1

     if match[i][j] >= k:
      # Use segment of exactly k or extend
      start_i = i - k
      start_j = j - k
      dp[i][j] = max(dp[i][j], dp[start_i][start_j] + k)

      # Or extend existing segment
      if match[i][j] > k:
       dp[i][j] = max(dp[i][j], dp[i-1][j-1] + 1)

  print(dp[n][m])

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(n × m) or O(n × m × min(n,m)) for simpler version
- **Space Complexity:** O(n × m)

### Key Insight
Track both the current consecutive match length and the best valid LCS so far. When a segment reaches length K, it becomes valid and can extend the previous best. The key is that once a segment is valid (≥K), adding one more character keeps it valid.
