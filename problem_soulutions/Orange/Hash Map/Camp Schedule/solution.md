# Camp Schedule

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

A programming camp has schedule s (binary string where '1' = contest day, '0' = day off). Gleb wants the optimal schedule t to appear as a substring as many times as possible, while keeping the same number of contest days and days off.

Rearrange the characters of s to maximize occurrences of t as a substring.

## Input Format
- First line: string s (1 ≤ |s| ≤ 500000)
- Second line: string t (1 ≤ |t| ≤ 500000)
- Both strings contain only '0' and '1'

## Output Format
Print the rearranged schedule with maximum occurrences of t. Must have same count of 0s and 1s as s.

## Solution

### Approach
Use KMP to find the failure function of t, which tells us the overlap when placing t consecutively. Greedily place as many copies of t as possible using the available 0s and 1s.

### Python Solution

```python
def compute_lps(pattern):
  """KMP failure function"""
  m = len(pattern)
  lps = [0] * m
  length = 0
  i = 1

  while i < m:
    if pattern[i] == pattern[length]:
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
  s = input().strip()
  t = input().strip()

  # Count available 0s and 1s
  zeros = s.count('0')
  ones = s.count('1')

  # Count 0s and 1s needed for one copy of t
  t_zeros = t.count('0')
  t_ones = t.count('1')

  if t_zeros == 0 and t_ones == 0:
    print(s)
    return

  # Compute LPS for overlap
  lps = compute_lps(t)
  overlap = lps[-1] if t else 0

  # The non-overlapping suffix of t
  suffix = t[overlap:]
  suffix_zeros = suffix.count('0')
  suffix_ones = suffix.count('1')

  result = []

  # Place first copy of t if possible
  if zeros >= t_zeros and ones >= t_ones:
    result.append(t)
    zeros -= t_zeros
    ones -= t_ones

    # Place more copies using overlap
    while zeros >= suffix_zeros and ones >= suffix_ones:
      result.append(suffix)
      zeros -= suffix_zeros
      ones -= suffix_ones

  # Append remaining characters
  result.append('0' * zeros)
  result.append('1' * ones)

  print(''.join(result))

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  s = input().strip()
  t = input().strip()

  cnt0 = s.count('0')
  cnt1 = s.count('1')

  t0 = t.count('0')
  t1 = t.count('1')

  # KMP failure function
  def kmp_fail(p):
    n = len(p)
    fail = [0] * n
    j = 0
    for i in range(1, n):
      while j > 0 and p[i] != p[j]:
        j = fail[j-1]
      if p[i] == p[j]:
        j += 1
      fail[i] = j
    return fail

  fail = kmp_fail(t)
  overlap = fail[-1] if t else 0

  # After first t, each additional t adds only t[overlap:]
  add = t[overlap:]
  add0 = add.count('0')
  add1 = add.count('1')

  ans = []

  # Try to place first t
  if cnt0 >= t0 and cnt1 >= t1:
    ans.append(t)
    cnt0 -= t0
    cnt1 -= t1

    # Keep adding overlapped copies
    while cnt0 >= add0 and cnt1 >= add1:
      ans.append(add)
      cnt0 -= add0
      cnt1 -= add1

  # Fill remaining
  ans.append('0' * cnt0 + '1' * cnt1)

  print(''.join(ans))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(|s| + |t|)
- **Space Complexity:** O(|s| + |t|)

### Key Insight
Using KMP's failure function, we know how much of t overlaps with itself. After placing the first copy of t, each additional copy only needs the non-overlapping suffix, saving characters for more copies.
