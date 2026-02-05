---
layout: simple
title: "Hash Map"
permalink: /problem_soulutions/Orange/Hash Map/
---
# Hash Map

Problems that leverage hash maps (dictionaries) for efficient lookups, counting, and data organization with average O(1) time complexity.

## Problems

### Camp Schedule

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

A programming camp has schedule s (binary string where '1' = contest day, '0' = day off). Gleb wants the optimal schedule t to appear as a substring as many times as possible, while keeping the same number of contest days and days off.

Rearrange the characters of s to maximize occurrences of t as a substring.

#### Input Format
- First line: string s (1 ≤ |s| ≤ 500000)
- Second line: string t (1 ≤ |t| ≤ 500000)
- Both strings contain only '0' and '1'

#### Output Format
Print the rearranged schedule with maximum occurrences of t. Must have same count of 0s and 1s as s.

#### Solution

##### Approach
Use KMP to find the failure function of t, which tells us the overlap when placing t consecutively. Greedily place as many copies of t as possible using the available 0s and 1s.

##### Python Solution

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

##### Alternative

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

##### Complexity Analysis
- **Time Complexity:** O(|s| + |t|)
- **Space Complexity:** O(|s| + |t|)

##### Key Insight
Using KMP's failure function, we know how much of t overlaps with itself. After placing the first copy of t, each additional copy only needs the non-overlapping suffix, saving characters for more copies.

---

### Cipher

#### Problem Information
- **Source:** HackerRank
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Jack and Daniel encrypt messages using a cipher. A message b is encoded by writing it k times (shifted by 0, 1, ..., k-1 positions) and XORing all columns together.

Given encoded string s and parameter k, decode the original message.

Example: b = 1001011, k = 4
```
1001011      shift 0
01001011     shift 1
001001011    shift 2
0001001011   shift 3
----------
1110101001   XORed result s
```

#### Input Format
- First line: n and k (length of original, number of shifts)
- Second line: encoded string s of length n + k - 1

#### Constraints
- 1 ≤ n ≤ 10⁶
- 1 ≤ k ≤ 10⁶

#### Output Format
Decoded message of length n.

#### Solution

##### Approach
For each position i in the encoded string s:
- s[i] = XOR of b[i], b[i-1], ..., b[i-k+1] (for valid indices)

We can decode left to right:
- b[0] = s[0]
- For i ≥ 1: b[i] = s[i] XOR b[i-1] XOR b[i-2] XOR ... (up to k-1 previous bits)

Use a running XOR of the last min(k, i+1) bits of b.

##### Python Solution

```python
def solve():
  n, k = map(int, input().split())
  s = input().strip()

  b = []
  xor_sum = 0  # Running XOR of last k bits of b

  for i in range(n):
    # s[i] = xor of b[max(0,i-k+1)] to b[i]
    # So b[i] = s[i] XOR (xor of b[max(0,i-k+1)] to b[i-1])
    # The "xor of previous" is our running xor_sum

    bit = int(s[i]) ^ xor_sum
    b.append(str(bit))

    # Update running XOR
    xor_sum ^= bit

    # Remove contribution of b[i-k+1] if it exists (sliding window)
    if i >= k - 1:
      xor_sum ^= int(b[i - k + 1])

  print(''.join(b))

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  n, k = map(int, input().split())
  s = input().strip()

  result = []
  window_xor = 0

  for i in range(n):
    # Decode b[i]
    # s[i] contains XOR of b[i-k+1..i], but we only have b[0..i-1]
    # s[i] = window_xor ^ b[i], so b[i] = s[i] ^ window_xor

    b_i = int(s[i]) ^ window_xor
    result.append(b_i)

    # Add b[i] to window
    window_xor ^= b_i

    # Remove b[i-k+1] from window if window exceeds k
    if i - k + 1 >= 0:
      window_xor ^= result[i - k + 1]

  print(''.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

##### One-liner

```python
def solve():
  n, k = map(int, input().split())
  s = input().strip()

  b = [0] * n
  xor = 0

  for i in range(n):
    b[i] = int(s[i]) ^ xor
    xor ^= b[i]
    if i >= k - 1:
      xor ^= b[i - k + 1]

  print(''.join(map(str, b)))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(N)

##### Key Insight
The encoded string at position i is the XOR of a window of k bits from the original. By maintaining a sliding window XOR, we can decode each bit in O(1) time. When the window slides past position k, we XOR out the oldest bit.

---

### Good Substrings

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

You've got string s, consisting of small English letters. Some of the English letters are good, the rest are bad.

A substring s[l...r] (1 ≤ l ≤ r ≤ |s|) of string s = s1s2...s|s| (where |s| is the length of string s) is string sl, sl+1, ..., sr.

The substring s[l...r] is good, if among the letters sl, sl+1, ..., sr there are at most k bad ones.

Your task is to find the number of distinct good substrings of the given string s. Two substrings s[x...y] and s[p...q] are considered distinct if their content is different, i.e. s[x...y] ≠ s[p...q].

#### Input Format
- The first line of the input is the non-empty string s, consisting of small English letters, the string's length is at most 1500 characters.
- The second line of the input is the string of characters 0 and 1, the length is exactly 26 characters. Character equals 1 means the i-th English letter is good, otherwise it's bad.
- The third line of the input consists a single integer k (0 ≤ k ≤ |s|) - the maximum acceptable number of bad characters in a good substring.

#### Output Format
Print a single integer - the number of distinct good substrings of string s.

#### Solution

##### Approach
We need to count distinct substrings with at most k bad characters. Two approaches:

1. **Hash Set**: Store all good substrings in a set and count unique ones
2. **Trie**: Use a Trie to efficiently store and count unique substrings

The Trie approach is more efficient for this problem.

##### Python Solution

```python
def solve():
  s = input().strip()
  good_bad = input().strip()
  k = int(input())

  def is_bad(c):
    return good_bad[ord(c) - ord('a')] == '0'

  n = len(s)
  good_substrings = set()

  for i in range(n):
    bad_count = 0
    substring = ""
    for j in range(i, n):
      substring += s[j]
      if is_bad(s[j]):
        bad_count += 1

      if bad_count > k:
        break

      good_substrings.add(substring)

  print(len(good_substrings))

if __name__ == "__main__":
  solve()
```

##### Python Solution

```python
class TrieNode:
  def __init__(self):
    self.children = {}
    self.is_end = False

def solve():
  s = input().strip()
  good_bad = input().strip()
  k = int(input())

  def is_bad(c):
    return good_bad[ord(c) - ord('a')] == '0'

  n = len(s)
  root = TrieNode()
  count = 0

  for i in range(n):
    bad_count = 0
    node = root

    for j in range(i, n):
      c = s[j]
      if is_bad(c):
        bad_count += 1

      if bad_count > k:
        break

      if c not in node.children:
        node.children[c] = TrieNode()
        count += 1  # New unique substring found

      node = node.children[c]

  print(count)

if __name__ == "__main__":
  solve()
```

##### Python Solution

```python
def solve():
  s = input().strip()
  good_bad = input().strip()
  k = int(input())

  def is_bad(c):
    return good_bad[ord(c) - ord('a')] == '0'

  n = len(s)
  MOD = 10**18 + 9
  BASE = 31

  good_substrings = set()

  for i in range(n):
    bad_count = 0
    hash_val = 0
    power = 1

    for j in range(i, n):
      if is_bad(s[j]):
        bad_count += 1

      if bad_count > k:
        break

      # Rolling hash
      hash_val = (hash_val * BASE + ord(s[j]) - ord('a') + 1) % MOD
      good_substrings.add((j - i + 1, hash_val))  # (length, hash) pair

  print(len(good_substrings))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n²) for generating all substrings
- **Space Complexity:** O(n²) in worst case for storing substrings

##### Key Insight
Using a Trie allows us to efficiently detect when a new unique substring is found - it happens exactly when we create a new node in the Trie.

---

### N meetings in one room

#### Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

There is one meeting room in Flipkart. There are n meetings in the form of (Sᵢ, Fᵢ) where Sᵢ is the start time and Fᵢ is the finish time of meeting i.

Find the maximum number of meetings that can be accommodated in the meeting room.

#### Input Format
- First line: T (number of test cases)
- For each test case:
  - First line: N (number of meetings)
  - Second line: N start times Sᵢ
  - Third line: N finish times Fᵢ

#### Output Format
Print the order in which meetings should take place (1-indexed), separated by spaces.

#### Solution

##### Approach
This is the classic Activity Selection problem. Greedy approach:
1. Sort meetings by finish time
2. Select the meeting with earliest finish time
3. Skip all meetings that overlap with selected meeting
4. Repeat until no meetings left

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    starts = list(map(int, input().split()))
    ends = list(map(int, input().split()))

    # Create list of (end_time, start_time, original_index)
    meetings = [(ends[i], starts[i], i + 1) for i in range(n)]

    # Sort by end time
    meetings.sort()

    result = []
    last_end = -1

    for end, start, idx in meetings:
      if start > last_end:
        result.append(idx)
        last_end = end

    print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    starts = list(map(int, input().split()))
    ends = list(map(int, input().split()))

    # Create meetings with 1-based index
    meetings = []
    for i in range(n):
      meetings.append((ends[i], starts[i], i + 1))

    # Sort by end time, then by start time
    meetings.sort(key=lambda x: (x[0], x[1]))

    selected = []
    prev_end = 0

    for end, start, idx in meetings:
      if start >= prev_end:
        selected.append(idx)
        prev_end = end

    print(' '.join(map(str, selected)))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for sorting
- **Space Complexity:** O(N) for storing meetings

##### Key Insight
The greedy choice is to always pick the meeting that ends earliest among non-conflicting meetings. This leaves maximum room for subsequent meetings. Sorting by end time and greedily selecting non-overlapping meetings gives the optimal solution.

---

### Suffix Equal Prefix

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

There is a curious boy in Noapara village, his name is "MODON". He wrote a line of small letters only. Now, he wants to know how many proper suffixes are also prefixes of that line. A proper suffix is a suffix of a text whose length is less than the original text.

Help "MODON" find the answer.

#### Input Format
- First line: T (T ≤ 50), the number of test cases
- Each case: A string S where 1 ≤ length(S) ≤ 10^6

#### Output Format
For each case, print the case number and the answer.

#### Solution

##### Approach
Use the KMP prefix function (failure function). The prefix function `pi[i]` gives the length of the longest proper prefix of `s[0..i]` that is also a suffix.

To count all proper suffixes that are also prefixes:
1. Compute prefix function for the string
2. Start from `pi[n-1]` and follow the chain: `pi[n-1]`, `pi[pi[n-1]-1]`, etc.
3. Each non-zero value in this chain represents a valid suffix=prefix length

##### Python Solution

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

##### Alternative

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

##### Complexity Analysis
- **Time Complexity:** O(|S|) for computing prefix/Z function
- **Space Complexity:** O(|S|) for the prefix/Z array

##### Key Insight
The KMP prefix function naturally encodes information about suffix-prefix matches. If `pi[n-1] = k`, then the suffix of length k equals the prefix of length k. Following the chain `pi[k-1]`, `pi[pi[k-1]-1]`, etc. gives us all such matching lengths.

Example: For "abcab", pi = [0,0,0,1,2], so pi[4]=2 means "ab" is both suffix and prefix. Following: pi[1]=0, so we stop. Answer = 1.

---

### The Monk and Prateek

#### Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

The Monk is testing Prateek with a hash function called the r3gz3n function:

`f(n) = N ⊕ (sum of digits of N)`

For example, f(81) = 81 ⊕ (8 + 1) = 81 ⊕ 9 = 88.

Given a list of N numbers, find:
1. The value of the r3gz3n function which occurs the maximum number of times
2. The number of collisions with the hash function

**Notes:**
- If all values are unique, print the maximum hashed value
- If multiple hashed values have the same maximum count, print the smallest one

#### Input Format
- First line: N (number of numbers)
- Second line: N integers separated by space

#### Constraints
- 1 ≤ N ≤ 10^5
- 1 ≤ Nᵢ ≤ 10^7

#### Output Format
Print two integers: the value with maximum occurrences (or max value if all unique) and the number of collisions.

#### Solution

##### Approach
1. Compute the hash value for each number: `f(n) = n XOR digit_sum(n)`
2. Use a hash map to count occurrences of each hash value
3. Count collisions (when a hash value already exists)
4. Find the most frequent hash value (smallest if tie)

##### Python Solution

```python
def digit_sum(n):
  total = 0
  while n:
    total += n % 10
    n //= 10
  return total

def r3gz3n(n):
  return n ^ digit_sum(n)

def solve():
  n = int(input())
  numbers = list(map(int, input().split()))

  hash_count = {}
  collisions = 0
  max_hash = float('-inf')

  for num in numbers:
    h = r3gz3n(num)
    max_hash = max(max_hash, h)

    if h in hash_count:
      collisions += 1
      hash_count[h] += 1
    else:
      hash_count[h] = 1

  # Find most frequent hash value
  if collisions == 0:
    # All unique - return max hash value
    print(max_hash, 0)
  else:
    # Find value with maximum count (smallest if tie)
    max_count = max(hash_count.values())
    most_frequent = min(h for h, c in hash_count.items() if c == max_count)
    print(most_frequent, collisions)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
from collections import Counter

def solve():
  n = int(input())
  nums = list(map(int, input().split()))

  def hash_func(x):
    return x ^ sum(int(d) for d in str(x))

  hashes = [hash_func(x) for x in nums]
  count = Counter(hashes)

  collisions = len(hashes) - len(count)

  if collisions == 0:
    result = max(hashes)
  else:
    max_freq = max(count.values())
    result = min(h for h, c in count.items() if c == max_freq)

  print(result, collisions)

if __name__ == "__main__":
  solve()
```

##### One-liner

```python
from collections import Counter

def solve():
  n = int(input())
  nums = list(map(int, input().split()))

  h = lambda x: x ^ sum(map(int, str(x)))
  hashes = [h(x) for x in nums]
  cnt = Counter(hashes)
  colls = len(hashes) - len(cnt)

  if colls == 0:
    print(max(hashes), 0)
  else:
    mx = max(cnt.values())
    print(min(k for k, v in cnt.items() if v == mx), colls)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N × D) where D is the average number of digits (at most 8 for 10^7)
- **Space Complexity:** O(N) for the hash count map

##### Key Insight
A collision occurs when two different input numbers produce the same hash value. The total number of collisions is `total_numbers - unique_hash_values`. When finding the most frequent hash value with ties, we need to return the smallest one.

---

### Watto and Mechanism

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Watto has a mechanism with n strings in memory. For each query string s, determine if there exists a string t in memory that:
- Has the same length as s
- Differs from s in exactly one position

Strings contain only letters 'a', 'b', 'c'.

#### Input Format
- First line: n and m (number of strings and queries)
- Next n lines: strings in memory
- Next m lines: query strings
- Total length ≤ 6×10⁵

#### Output Format
For each query, print "YES" if such string exists, "NO" otherwise.

#### Solution

##### Approach
Use hashing. For each string, compute hash values for all possible single-character changes. Store original hashes in a set. For queries, check if any single-character change produces a hash in the set.

##### Python Solution

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

##### Alternative

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

##### Complexity Analysis
- **Time Complexity:** O(N×L + M×L×3) where L is average string length
- **Space Complexity:** O(N) for storing hashes

##### Key Insight
Instead of comparing strings directly (too slow), use polynomial hashing. For each query, generate hashes of all strings that differ by exactly one character and check if any exists in our hash set. With only 3 possible characters, each position has 2 alternative values to try.

