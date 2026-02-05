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

## Solution

### Approach
1. For each prefix of B (length 1, 2, ..., |B|), count occurrences in A
2. Find the longest prefix with count ≥ n
3. Use KMP for efficient counting

### Python Solution

```python
def count_occurrences(text, pattern):
  """Count occurrences of pattern in text using KMP"""
  if not pattern:
    return len(text) + 1

  # Build failure function for pattern
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
  for char in text:
    while j > 0 and char != pattern[j]:
      j = fail[j - 1]
    if char == pattern[j]:
      j += 1
    if j == m:
      count += 1
      j = fail[j - 1]

  return count

def solve():
  A = input().strip()
  B = input().strip()
  n = int(input())

  # Binary search on prefix length
  # Or linear search from longest to shortest

  result = ""

  # Try each prefix length from longest to shortest
  for length in range(len(B), 0, -1):
    prefix = B[:length]
    if count_occurrences(A, prefix) >= n:
      result = prefix
      break

  if result:
    print(result)
  else:
    print("IMPOSSIBLE")

if __name__ == "__main__":
  solve()
```

### Optimized Solution with Single KMP Pass

```python
def solve():
  A = input().strip()
  B = input().strip()
  n = int(input())

  # Build KMP failure function for B
  m = len(B)
  fail = [0] * m
  for i in range(1, m):
    j = fail[i - 1]
    while j > 0 and B[i] != B[j]:
      j = fail[j - 1]
    if B[i] == B[j]:
      j += 1
    fail[i] = j

  # Count occurrences of each prefix length
  # cnt[k] = number of times prefix of length k appears in A
  cnt = [0] * (m + 1)

  j = 0
  for char in A:
    while j > 0 and char != B[j]:
      j = fail[j - 1]
    if j < m and char == B[j]:
      j += 1

    # Prefix of length j matched here
    cnt[j] += 1

  # Propagate counts: if prefix of length k appears, so does prefix of length fail[k-1]
  for k in range(m, 0, -1):
    cnt[fail[k - 1]] += cnt[k]

  # Find longest prefix with count >= n
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
