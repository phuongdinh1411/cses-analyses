# Suffix Equal Prefix

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

There is a curious boy in Noapara village, his name is "MODON". He wrote a line of small letters only. Now, he wants to know how many proper suffixes are also prefixes of that line. A proper suffix is a suffix of a text whose length is less than the original text.

Help "MODON" find the answer.

## Input Format
- First line: T (T ≤ 50), the number of test cases
- Each case: A string S where 1 ≤ length(S) ≤ 10^6

## Output Format
For each case, print the case number and the answer.

## Solution

### Approach
Use the KMP prefix function (failure function). The prefix function `pi[i]` gives the length of the longest proper prefix of `s[0..i]` that is also a suffix.

To count all proper suffixes that are also prefixes:
1. Compute prefix function for the string
2. Start from `pi[n-1]` and follow the chain: `pi[n-1]`, `pi[pi[n-1]-1]`, etc.
3. Each non-zero value in this chain represents a valid suffix=prefix length

### Python Solution

```python
def compute_prefix(s):
  """KMP prefix function"""
  n = len(s)
  pi = [0] * n

  for i in range(1, n):
    j = pi[i - 1]
    while j > 0 and s[i] != s[j]:
      j = pi[j - 1]
    if s[i] == s[j]:
      j += 1
    pi[i] = j

  return pi

def count_suffix_prefix(s):
  """Count proper suffixes that are also prefixes"""
  n = len(s)
  if n == 0:
    return 0

  pi = compute_prefix(s)

  # Follow the chain from pi[n-1]
  count = 0
  length = pi[n - 1]

  while length > 0:
    count += 1
    length = pi[length - 1]

  return count

def solve():
  t = int(input())

  for case in range(1, t + 1):
    s = input().strip()
    result = count_suffix_prefix(s)
    print(f"Case {case}: {result}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution using Z-function

```python
def z_function(s):
  """Z-function: z[i] = length of longest substring starting from i that matches prefix"""
  n = len(s)
  z = [0] * n
  z[0] = n
  l, r = 0, 0

  for i in range(1, n):
    if i < r:
      z[i] = min(r - i, z[i - l])
    while i + z[i] < n and s[z[i]] == s[i + z[i]]:
      z[i] += 1
    if i + z[i] > r:
      l, r = i, i + z[i]

  return z

def count_suffix_prefix_z(s):
  """Count using Z-function"""
  n = len(s)
  if n == 0:
    return 0

  z = z_function(s)

  # A suffix starting at position i is also a prefix if z[i] == n - i
  count = 0
  for i in range(1, n):
    if z[i] == n - i:
      count += 1

  return count

def solve():
  t = int(input())

  for case in range(1, t + 1):
    s = input().strip()
    result = count_suffix_prefix_z(s)
    print(f"Case {case}: {result}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(|S|) for computing prefix/Z function
- **Space Complexity:** O(|S|) for the prefix/Z array

### Key Insight
The KMP prefix function naturally encodes information about suffix-prefix matches. If `pi[n-1] = k`, then the suffix of length k equals the prefix of length k. Following the chain `pi[k-1]`, `pi[pi[k-1]-1]`, etc. gives us all such matching lengths.

Example: For "abcab", pi = [0,0,0,1,2], so pi[4]=2 means "ab" is both suffix and prefix. Following: pi[1]=0, so we stop. Answer = 1.
