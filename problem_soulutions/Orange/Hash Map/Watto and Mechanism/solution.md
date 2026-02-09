# Watto and Mechanism

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

## Problem Statement

Watto has a mechanism with n strings in memory. For each query string s, determine if there exists a string t in memory that:
- Has the same length as s
- Differs from s in exactly one position

Strings contain only letters 'a', 'b', 'c'.

## Input Format
- First line: n and m (number of strings and queries)
- Next n lines: strings in memory
- Next m lines: query strings
- Total length ≤ 6×10⁵

## Output Format
For each query, print "YES" if such string exists, "NO" otherwise.

## Example
```
Input:
2 3
abc
aac
abc
acc
bbc

Output:
YES
YES
NO
```
Memory: {"abc", "aac"}. Query "abc": differs by 1 from "aac" (position 1: b vs a). YES. Query "acc": differs by 1 from "aac" (position 2: c vs a). YES. Query "bbc": differs by 2 from "abc", differs by 2 from "aac". NO.

## Solution

### Approach
Use hashing. For each string, compute hash values for all possible single-character changes. Store original hashes in a set. For queries, check if any single-character change produces a hash in the set.

### Python Solution

```python
def solve():
  import sys
  input = sys.stdin.readline

  n, m = map(int, input().split())

  # Store hashes of all strings in memory, grouped by length
  from collections import defaultdict
  memory = defaultdict(set)

  BASE = 31
  MOD = 10**18 + 9

  def compute_hash(s):
    h = 0
    for c in s:
      h = (h * BASE + ord(c) - ord('a') + 1) % MOD
    return h

  # Precompute powers of BASE
  max_len = 600001
  pw = [1] * max_len
  for i in range(1, max_len):
    pw[i] = (pw[i-1] * BASE) % MOD

  for _ in range(n):
    s = input().strip()
    h = compute_hash(s)
    memory[len(s)].add(h)

  results = []

  for _ in range(m):
    s = input().strip()
    length = len(s)
    h = compute_hash(s)

    found = False
    current_hash = h

    # Try changing each position
    for i in range(length):
      pos = length - 1 - i  # Position from right
      old_val = ord(s[i]) - ord('a') + 1

      for c in 'abc':
        new_val = ord(c) - ord('a') + 1
        if new_val != old_val:
          # Compute new hash
          diff = (new_val - old_val) * pw[pos]
          new_hash = (current_hash + diff) % MOD

          if new_hash in memory[length]:
            found = True
            break

      if found:
        break

    results.append("YES" if found else "NO")

  print('\n'.join(results))

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Rolling Hash

```python
def solve():
  n, m = map(int, input().split())

  from collections import defaultdict
  BASE = 31
  MOD = 2**61 - 1

  strings_by_len = defaultdict(set)

  def poly_hash(s):
    h = 0
    for c in s:
      h = (h * BASE + ord(c)) % MOD
    return h

  # Read and hash all strings
  for _ in range(n):
    s = input().strip()
    strings_by_len[len(s)].add(poly_hash(s))

  # Precompute powers
  pow_base = [1]
  for _ in range(600005):
    pow_base.append((pow_base[-1] * BASE) % MOD)

  for _ in range(m):
    s = input().strip()
    L = len(s)
    h = poly_hash(s)

    found = False
    for i in range(L):
      old_c = ord(s[i])
      for new_c in [ord('a'), ord('b'), ord('c')]:
        if new_c != old_c:
          diff = (new_c - old_c) * pow_base[L - 1 - i]
          new_h = (h + diff) % MOD
          if new_h in strings_by_len[L]:
            found = True
            break
      if found:
        break

    print("YES" if found else "NO")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N×L + M×L×3) where L is average string length
- **Space Complexity:** O(N) for storing hashes

### Key Insight
Instead of comparing strings directly (too slow), use polynomial hashing. For each query, generate hashes of all strings that differ by exactly one character and check if any exists in our hash set. With only 3 possible characters, each position has 2 alternative values to try.
