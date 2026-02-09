# Check Transcription

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

## Problem Statement

Given a binary string s (0s and 1s) and a text t (lowercase letters), find the number of ways to assign non-empty strings r0 and r1 (r0 ≠ r1) such that replacing each 0 in s with r0 and each 1 with r1 produces t.

## Input Format
- First line: binary string s (2 ≤ |s| ≤ 10^5)
- Second line: text t (1 ≤ |t| ≤ 10^6)

## Output Format
Print the number of valid (r0, r1) pairs.

## Example
```
Input:
01
aaaaaa

Output:
2
```
Pattern "01" with text "aaaaaa" (length 6). We need c0*L0 + c1*L1 = 6 where c0=1, c1=1. So L0 + L1 = 6. Valid pairs: (L0=1, L1=5) gives r0="a", r1="aaaaa" - works since both are different. (L0=5, L1=1) gives r0="aaaaa", r1="a" - also works. So 2 valid pairs.

## Solution

### Approach
Let c0 = count of 0s in s, c1 = count of 1s in s.
If r0 has length L0 and r1 has length L1, then:
`c0 * L0 + c1 * L1 = len(t)`

Iterate over possible L0 values, compute L1, then verify if the assignment is consistent using hashing.

### Python Solution

```python
def solve():
  s = input().strip()
  t = input().strip()

  c0, c1 = s.count('0'), s.count('1')
  m = len(t)

  count = 0

  # Try all possible lengths for L0
  # c0 * L0 + c1 * L1 = m
  for L0 in range(1, m + 1):
    # Handle case where pattern has no 1s
    if c1 == 0:
      if c0 * L0 == m:
        r0 = t[:L0]
        # Verify all positions map to r0
        if all(t[i*L0:(i+1)*L0] == r0 for i in range(c0)):
          count += 1
      continue

    remaining = m - c0 * L0
    if remaining <= 0 or remaining % c1 != 0:
      continue
    L1 = remaining // c1
    if L1 <= 0:
      continue

    # Verify consistency
    r0, r1 = None, None
    valid = True
    pos = 0

    for ch in s:
      length = L0 if ch == '0' else L1
      substr = t[pos:pos + length]

      if ch == '0':
        if r0 is None:
          r0 = substr
        elif r0 != substr:
          valid = False
          break
      else:
        if r1 is None:
          r1 = substr
        elif r1 != substr:
          valid = False
          break
      pos += length

    if valid and r0 != r1:
      count += 1

  print(count)

if __name__ == "__main__":
  solve()
```

### Optimized Solution with Hashing

```python
def solve():
  s = input().strip()
  t = input().strip()

  c0 = s.count('0')
  c1 = s.count('1')
  m = len(t)

  MOD = (1 << 61) - 1
  BASE = 31

  # Precompute hashes and powers
  h = [0] * (m + 1)
  pw = [1] * (m + 1)

  for i in range(m):
    h[i + 1] = (h[i] * BASE + ord(t[i])) % MOD
    pw[i + 1] = (pw[i] * BASE) % MOD

  def get_hash(l, r):  # hash of t[l:r]
    return (h[r] - h[l] * pw[r - l] % MOD + MOD) % MOD

  count = 0

  for L0 in range(1, m + 1):
    if c1 == 0:
      if c0 * L0 == m:
        # Check all 0s consistent
        hash0 = get_hash(0, L0)
        valid = True
        pos = 0
        for ch in s:
          if get_hash(pos, pos + L0) != hash0:
            valid = False
            break
          pos += L0
        if valid:
          count += 1
      continue

    remaining = m - c0 * L0
    if remaining <= 0 or remaining % c1 != 0:
      continue
    L1 = remaining // c1
    if L1 <= 0:
      continue

    # Verify with hashing
    hash0, hash1 = None, None
    valid = True
    pos = 0

    for ch in s:
      if ch == '0':
        curr = get_hash(pos, pos + L0)
        if hash0 is None:
          hash0 = curr
        elif hash0 != curr:
          valid = False
          break
        pos += L0
      else:
        curr = get_hash(pos, pos + L1)
        if hash1 is None:
          hash1 = curr
        elif hash1 != curr:
          valid = False
          break
        pos += L1

    if valid and hash0 != hash1:
      count += 1

  print(count)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(|t|/min(c0,c1) × |s|) with hashing
- **Space Complexity:** O(|t|)

### Key Insight
The constraint c0×L0 + c1×L1 = |t| limits possible (L0, L1) pairs. For each valid pair, verify consistency by checking that all occurrences of 0 map to the same substring and all 1s map to another (different) substring. Polynomial hashing makes substring comparison O(1).
