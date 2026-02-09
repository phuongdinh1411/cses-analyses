# Gaint and Sifat

## Problem Information
- **Source:** Codechef
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Sifat needs to find how many times word s occurs as a substring in sentence S (after removing all spaces from S).

## Input Format
- First line: T (1 ≤ T ≤ 30) - number of test cases
- Each test case: two lines
  - First line: sentence S
  - Second line: word s

## Constraints
- 1 ≤ |S| ≤ 100000
- 1 ≤ |s| ≤ |S|

## Output Format
For each case, print case number and count of occurrences of s in S (spaces removed).

## Example
```
Input:
2
i love programming
gram
this is the test
is

Output:
Case 1: 1
Case 2: 2
```
Case 1: "i love programming" becomes "iloveprogramming". "gram" appears once (in "programming").
Case 2: "this is the test" becomes "thisisthetest". "is" appears twice (in "this" and "is").

## Solution

### Approach
1. Remove all spaces from S
2. Use KMP algorithm to count occurrences of pattern s in text S

### Python Solution

```python
def kmp_count(text, pattern):
  """Count occurrences of pattern in text using KMP"""
  if not pattern:
    return 0

  # Build failure function
  m = len(pattern)
  fail = [0] * m

  for i in range(1, m):
    j = fail[i - 1]
    while j > 0 and pattern[i] != pattern[j]:
      j = fail[j - 1]
    if pattern[i] == pattern[j]:
      j += 1
    fail[i] = j

  # Search
  count = 0
  j = 0
  for i in range(len(text)):
    while j > 0 and text[i] != pattern[j]:
      j = fail[j - 1]
    if text[i] == pattern[j]:
      j += 1
    if j == m:
      count += 1
      j = fail[j - 1]  # Continue searching for overlapping matches

  return count

def solve():
  t = int(input())

  for case in range(1, t + 1):
    S = input().replace(' ', '')  # Remove all spaces
    s = input().strip()

    count = kmp_count(S, s)
    print(f"Case {case}: {count}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    text = input().replace(' ', '')
    pattern = input().strip()

    # Build KMP prefix function
    def build_lps(p):
      lps = [0] * len(p)
      length = 0
      i = 1
      while i < len(p):
        if p[i] == p[length]:
          length += 1
          lps[i] = length
          i += 1
        elif length != 0:
          length = lps[length - 1]
        else:
          lps[i] = 0
          i += 1
      return lps

    lps = build_lps(pattern)

    # KMP search
    count = 0
    i = j = 0
    while i < len(text):
      if text[i] == pattern[j]:
        i += 1
        j += 1
        if j == len(pattern):
          count += 1
          j = lps[j - 1]
      elif j != 0:
        j = lps[j - 1]
      else:
        i += 1

    print(f"Case {case}: {count}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(|S| + |s|) per test case
- **Space Complexity:** O(|s|) for failure function

### Key Insight
After removing spaces from S, this becomes a standard string matching problem. KMP algorithm efficiently counts all (possibly overlapping) occurrences of the pattern in linear time.
