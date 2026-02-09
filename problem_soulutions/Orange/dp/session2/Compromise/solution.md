# Compromise

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Two politicians submit proposals as sequences of words. Find and print the longest common subsequence of words from both proposals.

## Input Format
- Multiple test cases until EOF
- Each test case: two texts (sequences of lowercase words)
- Words < 30 chars, texts < 100 words each
- Texts separated by '#', test cases separated by '#'

## Output Format
For each test case, print the longest common subsequence of words.

## Example
```
Input:
die eier von bransen
#
die eansen von eansen
#

Output:
die von
```
Text1: [die, eier, von, bransen], Text2: [die, eansen, von, eansen]. The LCS of words is [die, von] with length 2.

## Solution

### Approach
Standard LCS problem but on sequences of words instead of characters.
1. Parse both texts into word arrays
2. Compute LCS using DP
3. Backtrack to reconstruct the actual LCS sequence

### Python Solution

```python
def solve():
  import sys

  lines = sys.stdin.read().strip().split('\n')
  i = 0

  while i < len(lines):
    # Read first text until '#'
    text1 = []
    while i < len(lines) and lines[i].strip() != '#':
      text1.extend(lines[i].split())
      i += 1
    i += 1  # skip '#'

    # Read second text until '#' or EOF
    text2 = []
    while i < len(lines) and lines[i].strip() != '#':
      text2.extend(lines[i].split())
      i += 1
    i += 1  # skip '#'

    if not text1 or not text2:
      continue

    # LCS on word arrays
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
      for j in range(1, n + 1):
        if text1[i-1] == text2[j-1]:
          dp[i][j] = dp[i-1][j-1] + 1
        else:
          dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack to get LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
      if text1[i-1] == text2[j-1]:
        lcs.append(text1[i-1])
        i -= 1
        j -= 1
      elif dp[i-1][j] > dp[i][j-1]:
        i -= 1
      else:
        j -= 1

    lcs.reverse()
    print(' '.join(lcs))

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def lcs_words(words1, words2):
  m, n = len(words1), len(words2)

  # dp[i][j] = LCS length of words1[:i] and words2[:j]
  dp = [[0] * (n + 1) for _ in range(m + 1)]

  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if words1[i-1] == words2[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1
      else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

  # Reconstruct
  result = []
  i, j = m, n
  while i > 0 and j > 0:
    if words1[i-1] == words2[j-1]:
      result.append(words1[i-1])
      i -= 1
      j -= 1
    elif dp[i-1][j] >= dp[i][j-1]:
      i -= 1
    else:
      j -= 1

  return result[::-1]

def solve():
  import sys
  content = sys.stdin.read()

  # Split by '#' to get test cases
  parts = content.strip().split('#')

  i = 0
  while i + 1 < len(parts):
    text1 = parts[i].split()
    text2 = parts[i + 1].split()

    if text1 and text2:
      result = lcs_words(text1, text2)
      print(' '.join(result))

    i += 2

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(m × n) where m, n are word counts
- **Space Complexity:** O(m × n)

### Key Insight
This is the classic LCS problem applied to word sequences rather than character sequences. The algorithm is identical: build a DP table where dp[i][j] represents the LCS length of the first i words of text1 and first j words of text2. Backtrack to reconstruct the actual sequence.
