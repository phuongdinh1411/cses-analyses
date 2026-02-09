# Password

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Given string s, find the longest substring t that is:
1. A prefix of s
2. A suffix of s
3. Appears somewhere in the middle of s (not at the very beginning or end)

If no such substring exists, print "Just a legend".

## Input Format
- Single line: string s (length 1 to 10⁶), consisting of lowercase Latin letters

## Output Format
Print the substring t, or "Just a legend" if it doesn't exist.

## Example
```
Input:
fixprefixsuffix

Output:
fix
```
"fix" is a prefix (starts at position 0), a suffix (ends at last position), and appears in the middle as part of "prefix". It satisfies all three conditions.

```
Input:
abcdabc

Output:
Just a legend
```
"abc" is both prefix and suffix, but doesn't appear in the middle (positions 1-5).

## Solution

### Approach
Use KMP failure function:
1. Find all prefix-suffix lengths using failure function
2. Check which of these also appear in the middle
3. Return the longest valid one

### Python Solution

```python
def solve():
  s = input().strip()
  n = len(s)

  if n < 3:
    print("Just a legend")
    return

  # Build KMP failure function
  fail = [0] * n
  for i in range(1, n):
    j = fail[i - 1]
    while j > 0 and s[i] != s[j]:
      j = fail[j - 1]
    if s[i] == s[j]:
      j += 1
    fail[i] = j

  # Find all valid prefix-suffix lengths using set
  prefix_suffix_lens = set()
  length = fail[n - 1]
  while length > 0:
    prefix_suffix_lens.add(length)
    length = fail[length - 1]

  # Find lengths that appear in the middle using set comprehension
  middle_lens = {fail[i] for i in range(n - 2) if fail[i] > 0}

  # Find longest length that is both prefix-suffix AND appears in middle
  valid_lens = prefix_suffix_lens & middle_lens

  # Simplified conditional output
  print(s[:max(valid_lens)] if valid_lens else "Just a legend")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  s = input().strip()
  n = len(s)

  # KMP failure function
  pi = [0] * n
  for i in range(1, n):
    j = pi[i - 1]
    while j > 0 and s[i] != s[j]:
      j = pi[j - 1]
    if s[i] == s[j]:
      j += 1
    pi[i] = j

  # Count occurrences of each prefix (by its length)
  cnt = [0] * (n + 1)
  for i in range(n):
    cnt[pi[i]] += 1

  # Accumulate: prefix of length k includes prefix of length pi[k-1]
  for i in range(n - 1, 0, -1):
    cnt[pi[i - 1]] += cnt[i]

  # Find valid prefix-suffix that appears >= 3 times
  # (start, end, middle)
  length = pi[n - 1]
  while length > 0:
    # cnt[length] >= 2 means it appears at least twice besides being suffix
    # But we need it to appear in the middle
    # Check if this prefix appears at position other than 0 and n-length
    if cnt[length] >= 3:
      print(s[:length])
      return
    # Or if it appears as a prefix of the suffix prefix
    if cnt[length] >= 2 and pi[length - 1] > 0:
      print(s[:pi[length - 1]])
      return
    length = pi[length - 1]

  print("Just a legend")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(N)

### Key Insight
The KMP failure function gives us all prefix-suffix matches. We need to find one that also appears in the middle. Track which lengths appear in the middle (via fail[i] for i in [0, n-2]), then find the longest one that's also a prefix-suffix.
