# File Recover Testing

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Given a length K and a string S, generate a text of exactly K characters by repeating S cyclically. Determine the maximum number of times the string S appears consecutively in this generated text.

For example: K=14, S="abcab" generates "abcabcabcabcab" where "abcab" appears 4 times (at positions 1, 4, 7, 10).

## Input Format
- Multiple test cases
- Each line: integer K (1 ≤ K ≤ 10^9) and string S (up to 10^6 lowercase letters)
- End of input: "-1 *"

## Output Format
For each test case, output the maximum number of times S appears in the generated text of length K.

## Solution

### Approach
This is a string pattern matching problem with an important insight:
1. When we repeat string S cyclically, the pattern S can overlap with itself
2. Use KMP prefix function to find the longest proper prefix that is also a suffix
3. The period of the string is `len(S) - prefix[len(S)-1]`
4. After the first occurrence of S, each additional occurrence starts after `period` characters

Formula: If K ≥ len(S), count = (K - prefix[last]) / (len(S) - prefix[last])

### Python Solution

```python
def compute_prefix(pattern):
  """KMP prefix function"""
  m = len(pattern)
  prefix = [0] * m
  j = 0

  for i in range(1, m):
    while j > 0 and pattern[i] != pattern[j]:
      j = prefix[j - 1]
    if pattern[i] == pattern[j]:
      j += 1
    prefix[i] = j

  return prefix

def solve():
  import sys

  for line in sys.stdin:
    parts = line.split()
    k = int(parts[0])
    s = parts[1]

    if k == -1:
      break

    n = len(s)

    if k < n:
      print(0)
      continue

    prefix = compute_prefix(s)

    # Period of string S
    period = n - prefix[n - 1]

    # Number of occurrences
    # First occurrence needs n characters
    # Each subsequent occurrence needs 'period' more characters
    count = (k - prefix[n - 1]) // period

    print(count)

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Detailed Explanation

```python
def kmp_prefix(s):
  n = len(s)
  lps = [0] * n  # Longest Proper Prefix which is also Suffix
  length = 0
  i = 1

  while i < n:
    if s[i] == s[length]:
      length += 1
      lps[i] = length
      i += 1
    elif length != 0:
      length = lps[length - 1]
    else:
      lps[i] = 0
      i += 1

  return lps

def solve():
  while True:
    line = input().split()
    k, s = int(line[0]), line[1]

    if k == -1:
      break

    n = len(s)

    if k < n:
      print(0)
      continue

    lps = kmp_prefix(s)

    # The "overlap" is lps[n-1]
    # The "unique part" is n - lps[n-1]
    # First match: needs n chars
    # Each additional match: needs (n - lps[n-1]) chars

    overlap = lps[n - 1]
    step = n - overlap

    # Count = 1 + (k - n) // step = (k - overlap) // step
    count = (k - overlap) // step

    print(count)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(|S|) for computing prefix function
- **Space Complexity:** O(|S|) for the prefix array

### Key Insight
When string S repeats cyclically:
- S = "abcab", prefix function gives [0,0,0,1,2], so prefix[4] = 2
- Period = 5 - 2 = 3 (the string "abc" repeats)
- After first full occurrence of S (needs 5 chars), each additional occurrence needs only 3 more characters because "ab" overlaps

The formula `(K - prefix[n-1]) / (n - prefix[n-1])` directly gives us the count without generating the actual string.
