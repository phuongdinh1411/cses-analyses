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
This is the standard LCS, run on word lists instead of characters.
1. Split the whole input on '#'. Consecutive pieces form the two texts of a test case.
2. Fill `dp[i][j]`, the LCS length of the first i words and the first j words.
3. Walk back from `dp[m][n]` to recover the words.

Keep the DP and backtrack indices separate from any input-cursor variable. Reusing `i` for both resets the cursor and loops forever.

### Python Solution

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

  # Reconstruct using tuple unpacking in while loop
  result = []
  i, j = m, n
  while i > 0 and j > 0:
    if words1[i-1] == words2[j-1]:
      result.append(words1[i-1])
      i, j = i - 1, j - 1
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

  # Process pairs using range with step 2
  for idx in range(0, len(parts) - 1, 2):
    text1, text2 = parts[idx].split(), parts[idx + 1].split()

    if text1 and text2:
      result = lcs_words(text1, text2)
      print(' '.join(result))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(m × n) where m, n are word counts
- **Space Complexity:** O(m × n)

### Key Insight
This is the classic LCS problem applied to word sequences rather than character sequences. The algorithm is identical: build a DP table where dp[i][j] represents the LCS length of the first i words of text1 and first j words of text2. Backtrack to reconstruct the actual sequence.
