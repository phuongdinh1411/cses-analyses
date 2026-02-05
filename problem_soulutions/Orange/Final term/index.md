---
layout: simple
title: "Final Term"
permalink: /problem_soulutions/Orange/Final term/
---
# Final term

A collection of problems from the final term examination covering various algorithmic topics.

## Problems

### File Recover Testing

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a length K and a string S, generate a text of exactly K characters by repeating S cyclically. Determine the maximum number of times the string S appears consecutively in this generated text.

For example: K=14, S="abcab" generates "abcabcabcabcab" where "abcab" appears 4 times (at positions 1, 4, 7, 10).

#### Input Format
- Multiple test cases
- Each line: integer K (1 ≤ K ≤ 10^9) and string S (up to 10^6 lowercase letters)
- End of input: "-1 *"

#### Output Format
For each test case, output the maximum number of times S appears in the generated text of length K.

#### Solution

##### Approach
This is a string pattern matching problem with an important insight:
1. When we repeat string S cyclically, the pattern S can overlap with itself
2. Use KMP prefix function to find the longest proper prefix that is also a suffix
3. The period of the string is `len(S) - prefix[len(S)-1]`
4. After the first occurrence of S, each additional occurrence starts after `period` characters

Formula: If K ≥ len(S), count = (K - prefix[last]) / (len(S) - prefix[last])

##### Python Solution

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

##### Alternative

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

##### Complexity Analysis
- **Time Complexity:** O(|S|) for computing prefix function
- **Space Complexity:** O(|S|) for the prefix array

##### Key Insight
When string S repeats cyclically:
- S = "abcab", prefix function gives [0,0,0,1,2], so prefix[4] = 2
- Period = 5 - 2 = 3 (the string "abc" repeats)
- After first full occurrence of S (needs 5 chars), each additional occurrence needs only 3 more characters because "ab" overlaps

The formula `(K - prefix[n-1]) / (n - prefix[n-1])` directly gives us the count without generating the actual string.

---

### Little Deepu and Array

#### Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Little Deepu has an array of positive elements. He performs M HIT operations where HIT(X) decreases the value of all elements greater than X by 1.

After all M operations, print the final array.

#### Input Format
- First line: N (size of array)
- Second line: N elements of array
- Third line: M (number of operations)
- Next M lines: X value for each HIT operation

#### Constraints
- 1 ≤ N ≤ 100000
- 1 ≤ Aᵢ ≤ 10^9
- 1 ≤ M ≤ 20000
- 1 ≤ X ≤ 10^9

#### Output Format
Print the final array after M HIT operations.

#### Solution

##### Approach
Instead of simulating each HIT operation on the entire array (O(N*M)), we can:
1. Sort all HIT thresholds
2. For each element, count how many thresholds it exceeds
3. Subtract that count from the element

Key insight: If element A[i] > X, it gets decremented. So we count how many X values each element exceeds.

##### Python Solution

```python
def solve():
  n = int(input())
  arr = list(map(int, input().split()))
  m = int(input())

  hits = []
  for _ in range(m):
    hits.append(int(input()))

  # Sort hit thresholds
  hits.sort()

  # For each element, find how many hits affect it
  result = []
  for a in arr:
    # Count how many X values are < a (element will be decremented for each)
    # Binary search for position where hits[i] >= a
    import bisect
    count = bisect.bisect_left(hits, a)
    result.append(a - count)

  print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
from bisect import bisect_left

def solve():
  n = int(input())
  arr = list(map(int, input().split()))
  m = int(input())
  hits = [int(input()) for _ in range(m)]

  # Sort hits for binary search
  hits.sort()

  # For each element, count hits where X < element
  # (element decreases by 1 for each such X)
  result = []
  for a in arr:
    # Number of X values strictly less than a
    decrements = bisect_left(hits, a)
    result.append(a - decrements)

  print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
from bisect import bisect_left

def solve():
  n = int(input())
  arr = list(map(int, input().split()))
  m = int(input())
  hits = sorted(int(input()) for _ in range(m))

  # Each HIT(X) decrements elements > X
  # So element A becomes A - (count of X where X < A)
  output = []
  for val in arr:
    # How many hit values are strictly less than val
    dec = bisect_left(hits, val)
    output.append(str(val - dec))

  print(' '.join(output))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N log M + M log M) - sorting hits and binary search for each element
- **Space Complexity:** O(M) for storing hit thresholds

##### Key Insight
HIT(X) decrements all values > X. So for an element with value V:
- It gets decremented once for each X where X < V
- Final value = V - (count of X values < V)

Using binary search on sorted hit values gives us this count efficiently.

---

### Mancunian and K-Ordered LCS

#### Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 512MB

#### Problem Statement

Find the k-ordered LCS of two sequences. A k-ordered LCS is the LCS of two sequences if you are allowed to change at most k elements in the first sequence to any value you wish.

#### Input Format
- First line: N, M, and k (lengths of sequences and parameter)
- Second line: N integers (first sequence)
- Third line: M integers (second sequence)

#### Constraints
- 1 ≤ N, M ≤ 2000
- 1 ≤ k ≤ 5
- 1 ≤ element ≤ 10⁹

#### Output Format
Print the length of k-ordered LCS.

#### Solution

##### Approach
Use DP with an additional dimension for the number of changes used.
- `dp[i][j][c]` = length of LCS considering first i elements of seq1, first j elements of seq2, using c changes
- If we change element i to match element j, we use one change

##### Python Solution

```python
def solve():
  n, m, k = map(int, input().split())
  a = list(map(int, input().split()))
  b = list(map(int, input().split()))

  # dp[i][j][c] = max LCS length using first i of a, first j of b, with c changes
  # c changes means we changed c elements in a to match elements in b

  dp = [[[-1] * (k + 2) for _ in range(m + 1)] for _ in range(n + 1)]

  # Base case
  for i in range(n + 1):
    for c in range(k + 2):
      dp[i][0][c] = 0
  for j in range(m + 1):
    for c in range(k + 2):
      dp[0][j][c] = 0

  for i in range(1, n + 1):
    for j in range(1, m + 1):
      for c in range(k + 1):
        # Option 1: Don't include a[i-1] in LCS
        dp[i][j][c] = max(dp[i][j][c], dp[i-1][j][c])

        # Option 2: Don't include b[j-1] in LCS
        dp[i][j][c] = max(dp[i][j][c], dp[i][j-1][c])

        # Option 3: Match a[i-1] with b[j-1]
        if a[i-1] == b[j-1]:
          dp[i][j][c] = max(dp[i][j][c], dp[i-1][j-1][c] + 1)

        # Option 4: Change a[i-1] to b[j-1] (costs 1 change)
        if c > 0:
          dp[i][j][c] = max(dp[i][j][c], dp[i-1][j-1][c-1] + 1)

  print(max(dp[n][m][c] for c in range(k + 1)))

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  n, m, k = map(int, input().split())
  a = list(map(int, input().split()))
  b = list(map(int, input().split()))

  # dp[j][c] for space optimization
  INF = float('-inf')

  dp = [[0] * (k + 1) for _ in range(m + 1)]

  for i in range(1, n + 1):
    new_dp = [[0] * (k + 1) for _ in range(m + 1)]

    for j in range(1, m + 1):
      for c in range(k + 1):
        # Skip a[i-1]
        new_dp[j][c] = max(new_dp[j][c], dp[j][c])
        # Skip b[j-1]
        new_dp[j][c] = max(new_dp[j][c], new_dp[j-1][c])

        # Natural match
        if a[i-1] == b[j-1]:
          new_dp[j][c] = max(new_dp[j][c], dp[j-1][c] + 1)

        # Use a change
        if c > 0:
          new_dp[j][c] = max(new_dp[j][c], dp[j-1][c-1] + 1)

    dp = new_dp

  print(max(dp[m]))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N × M × K)
- **Space Complexity:** O(M × K) with optimization

##### Key Insight
This extends classical LCS by allowing k "free" matches where we pretend a[i] equals any b[j] we want. Each such pretend match costs one of our k changes.

---

### Message Spreading

#### Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

There are N students in a class, each with a different funny story. They want to share stories by sending electronic messages. A sender includes all stories they know, and each message has only one recipient.

Find the minimum number of messages needed so everyone gets all the funny stories.

#### Input Format
- First line: T (number of test cases)
- Each test case: N (number of students)

#### Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N ≤ 10⁵

#### Output Format
For each test case, print the minimum number of messages needed.

#### Solution

##### Approach
This is a classic problem. With N students:
- First, everyone sends their story to one person (N-1 messages, one person has all stories)
- Then that person sends to everyone else (N-1 messages)

But we can optimize: use a tree-like broadcast structure.
- Minimum messages = 2*(N-1) for N ≥ 2
- For N = 1: 0 messages needed

Actually, the optimal is **2*(N-1)** for N > 1.

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())

    if n == 1:
      print(0)
    else:
      # Minimum messages = 2 * (n - 1)
      # First phase: gather all stories to one person (n-1 messages)
      # Second phase: distribute from that person (n-1 messages)
      print(2 * (n - 1))

if __name__ == "__main__":
  solve()
```

##### Mathematical

```python
def solve():
  """
  For N students to all know all N stories:

  Lower bound: Each student except the "collector" must send at least once
  to contribute their story = N-1 messages minimum for gathering.

  Each student except the "distributor" must receive at least once
  to get all stories = N-1 messages minimum for distributing.

  Total minimum = 2*(N-1)

  This is achievable:
  Round 1: Students 2,3,...,N each send to student 1 (N-1 messages)
      Now student 1 knows all stories
  Round 2: Student 1 sends to students 2,3,...,N (N-1 messages)
      Now everyone knows all stories
  """
  t = int(input())

  for _ in range(t):
    n = int(input())
    print(max(0, 2 * (n - 1)))

if __name__ == "__main__":
  solve()
```

##### One-liner

```python
t = int(input())
for _ in range(t):
  n = int(input())
  print(2 * n - 2 if n > 1 else 0)
```

##### Complexity Analysis
- **Time Complexity:** O(1) per test case
- **Space Complexity:** O(1)

##### Key Insight
This is an information dissemination problem. The minimum number of messages is 2(N-1):
- Phase 1 (Aggregation): N-1 messages to collect all stories at one person
- Phase 2 (Broadcast): N-1 messages to distribute to everyone else

---

### Trainsorting

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Erin is an engineer. She drives trains. She also arranges the cars within each train. She prefers to put the cars in decreasing order of weight, with the heaviest car at the front of the train.

Unfortunately, sorting train cars is not easy. One cannot simply pick up a car and place it somewhere else. It is impractical to insert a car within an existing train. A car may only be added to the beginning or end of the train.

Cars arrive at the train station in a predetermined order. When each car arrives, Erin can add it to the beginning or end of her train, or refuse to add it at all. The resulting train should be as long as possible, but the cars within it must be ordered by weight.

Given the weights of the cars in the order in which they arrive, what is the longest train that Erin can make?

#### Input Format
- The first line is the number of test cases to follow.
- Each test case:
  - The first line contains an integer 0 ≤ n ≤ 2000, the number of cars.
  - Each of the following n lines contains a non-negative integer giving the weight of a car.
  - No two cars have the same weight.

#### Output Format
Output a single integer giving the number of cars in the longest train that can be made with the given restrictions.

#### Solution

##### Approach
For each car, we can either:
1. Add it to the front (it must be heavier than current front)
2. Add it to the back (it must be lighter than current back)
3. Skip it

This can be solved using LIS (Longest Increasing Subsequence) and LDS (Longest Decreasing Subsequence):
- For each position i, find the LIS ending at i (cars that can be added to the back)
- For each position i, find the LDS ending at i (cars that can be added to the front)
- The answer is max(LIS[i] + LDS[i] - 1) for all i

##### Python Solution

```python
def longest_increasing_subsequence(arr):
  """Returns array where lis[i] = length of LIS ending at index i"""
  n = len(arr)
  if n == 0:
    return []

  lis = [1] * n

  for i in range(1, n):
    for j in range(i):
      if arr[j] < arr[i]:
        lis[i] = max(lis[i], lis[j] + 1)

  return lis

def longest_decreasing_subsequence(arr):
  """Returns array where lds[i] = length of LDS ending at index i"""
  n = len(arr)
  if n == 0:
    return []

  lds = [1] * n

  for i in range(1, n):
    for j in range(i):
      if arr[j] > arr[i]:
        lds[i] = max(lds[i], lds[j] + 1)

  return lds

def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())

    if n == 0:
      print(0)
      continue

    weights = []
    for _ in range(n):
      weights.append(int(input()))

    # LIS[i] = longest increasing subsequence ending at i
    # This represents cars added to the back
    lis = longest_increasing_subsequence(weights)

    # LDS[i] = longest decreasing subsequence ending at i
    # This represents cars added to the front
    lds = longest_decreasing_subsequence(weights)

    # For each position i as the "pivot" car, the maximum train length is
    # LIS[i] + LDS[i] - 1 (subtract 1 because car i is counted twice)
    max_length = 0
    for i in range(n):
      max_length = max(max_length, lis[i] + lds[i] - 1)

    print(max_length)

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
import bisect

def lis_lengths(arr):
  """O(n log n) LIS computation"""
  n = len(arr)
  lis = [1] * n
  tails = []

  for i, x in enumerate(arr):
    pos = bisect.bisect_left(tails, x)
    if pos == len(tails):
      tails.append(x)
    else:
      tails[pos] = x
    lis[i] = pos + 1

  return lis

def lds_lengths(arr):
  """O(n log n) LDS computation"""
  return lis_lengths([-x for x in arr])

def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())

    if n == 0:
      print(0)
      continue

    weights = [int(input()) for _ in range(n)]

    lis = lis_lengths(weights)
    lds = lds_lengths(weights)

    max_length = max(lis[i] + lds[i] - 1 for i in range(n))
    print(max_length)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n²) for basic solution, O(n log n) for optimized
- **Space Complexity:** O(n)

##### Key Insight
The train forms a "bitonic" sequence - increasing then decreasing. Each car can serve as the "pivot" point, with LIS to its left (back of train) and LDS to its right (front of train).

