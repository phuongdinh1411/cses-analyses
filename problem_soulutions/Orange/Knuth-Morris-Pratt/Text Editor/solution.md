# Text Editor

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Given text A, pattern B, and minimum count n, find the longest prefix of B that appears at least n times in A. If no such prefix exists, print "IMPOSSIBLE".

## Input Format
- First line: text A (1 ≤ |A| ≤ 10⁵)
- Second line: pattern B (1 ≤ |B| ≤ |A|)
- Third line: integer n (1 ≤ n ≤ |A|)

## Output Format
Print the longest prefix of B that appears at least n times in A, or "IMPOSSIBLE".

## Example
```
Input:
abacaba
aba
2

Output:
aba
```
Text A = "abacaba", pattern B = "aba", minimum count n = 2. The prefix "aba" appears at positions 0 and 4 in A (2 times), so output "aba".

```
Input:
xyz
abc
1

Output:
IMPOSSIBLE
```
No prefix of "abc" appears in "xyz".

## Solution

### Approach
Run KMP for pattern B over text A once:
1. At each position of A, record `j`, the length of the longest prefix of B ending there, in `cnt[j]`. When a full match ends (`j == m`), fall back to `fail[m-1]` before reading the next character.
2. Every border of a matched prefix also ends at that position, so push counts down the border chain, from longest to shortest: `cnt[fail[k-1]] += cnt[k]`.
3. `cnt[k]` is now the number of (possibly overlapping) occurrences of `B[:k]`. Return the longest k with `cnt[k] >= n`.

Trying every prefix length with a separate KMP search also works, but costs O(|A|·|B|).

### Python Solution

```python
def solve():
  A = input().strip()
  B = input().strip()
  n = int(input())

  m = len(B)
  fail = [0] * m
  for i in range(1, m):
    j = fail[i - 1]
    while j > 0 and B[i] != B[j]:
      j = fail[j - 1]
    if B[i] == B[j]:
      j += 1
    fail[i] = j

  # cnt[k] = number of positions in A where the longest matched prefix of B has length k
  cnt = [0] * (m + 1)
  j = 0
  for char in A:
    if j == m:
      j = fail[j - 1]
    while j > 0 and char != B[j]:
      j = fail[j - 1]
    if char == B[j]:
      j += 1
    cnt[j] += 1

  # Every border of a matched prefix also ends there, so push counts down the border chain
  for k in range(m, 0, -1):
    cnt[fail[k - 1]] += cnt[k]

  for length in range(m, 0, -1):
    if cnt[length] >= n:
      print(B[:length])
      return
  print("IMPOSSIBLE")


if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(|A| + |B|)
- **Space Complexity:** O(|B|)

### Key Insight
When matching pattern B against text A, at each position we've matched some prefix of B. Count how many times each prefix length is reached. Then propagate counts downward (longer prefix matches imply shorter prefix matches) to get total counts.
