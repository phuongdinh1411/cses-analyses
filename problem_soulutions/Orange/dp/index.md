---
layout: simple
title: "Dynamic Programming"
permalink: /problem_soulutions/Orange/dp/
---
# Dynamic Programming

Dynamic programming problems organized by sessions, covering various DP techniques and patterns.

## Problems

## Session 1

### Alphacode

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Alice and Bob need to send secret messages to each other and are discussing ways to encode their messages:

Alice: "Let's just use a very simple code: We'll assign A the code word 1, B will be 2, and so on down to Z being assigned 26."

Bob: "That's a stupid code, Alice. Suppose I send you the word BEAN encoded as 25114. You could decode that in many different ways!"

Alice: "Sure you could, but what words would you get? Other than BEAN, you'd get BEAAD, YAAD, YAN, YKD and BEKD. I think you would be able to figure out the correct decoding. And why would you send me the word BEAN anyway?"

Bob: "OK, maybe that's a bad example, but I bet you that if you got a string of length 5000 there would be tons of different decodings and with that many you would find at least two different ones that would make sense."

Alice: "How many different decodings?"
Bob: "Jillions!"

For some reason, Alice is still unconvinced by Bob's argument, so she requires a program that will determine how many decodings there can be for a given string using her code.

#### Input Format
- Input will consist of multiple input sets.
- Each set will consist of a single line of at most 5000 digits representing a valid encryption (no line will begin with a 0).
- There will be no spaces between the digits.
- An input line of 0 will terminate the input and should not be processed.

#### Output Format
For each input set, output the number of possible decodings for the input string. All answers will be within the range of a 64 bit signed integer.

#### Solution

##### Approach
This is a classic DP problem similar to climbing stairs:
- `dp[i]` = number of ways to decode the first i characters
- At each position, we can either:
  1. Take a single digit (if it's 1-9)
  2. Take two digits (if they form 10-26)

##### Python Solution

```python
def solve(s):
  n = len(s)
  if n == 0 or s[0] == '0':
    return 0

  # dp[i] = number of ways to decode first i characters
  dp = [0] * (n + 1)
  dp[0] = 1  # Empty string
  dp[1] = 1  # First character (already checked it's not 0)

  for i in range(2, n + 1):
    # Single digit decode (1-9)
    if s[i-1] != '0':
      dp[i] = dp[i-1]

    # Two digit decode (10-26)
    two_digit = int(s[i-2:i])
    if 10 <= two_digit <= 26:
      dp[i] += dp[i-2]

  return dp[n]

def main():
  while True:
    s = input().strip()
    if s == '0':
      break
    print(solve(s))

if __name__ == "__main__":
  main()
```

##### Complexity Analysis
- **Time Complexity:** O(n) where n is the length of the string
- **Space Complexity:** O(n) for the DP array (can be optimized to O(1))

---

### Bytelandian gold coins

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

In Byteland they have a very strange monetary system. Each Bytelandian gold coin has an integer number written on it. A coin n can be exchanged in a bank into three coins: n/2, n/3 and n/4. But these numbers are all rounded down (the banks have to make a profit). You can also sell Bytelandian coins for American dollars. The exchange rate is 1:1. But you can not buy Bytelandian coins.

You have one gold coin. What is the maximum amount of American dollars you can get for it?

#### Input Format
- The input will contain several test cases (not more than 10).
- Each testcase is a single line with a number n, 0 ≤ n ≤ 1000000000.
- It is the number written on your coin.

#### Output Format
For each test case output a single line, containing the maximum amount of American dollars you can make.

#### Solution

##### Approach
This is a recursive problem with memoization:
- For a coin with value n, we can either:
  1. Keep it and get n dollars
  2. Exchange it for coins worth n/2, n/3, and n/4, then recursively find the max for each
- Answer is max(n, solve(n/2) + solve(n/3) + solve(n/4))

Since n can be up to 10^9, we use a dictionary for memoization instead of an array.

##### Python Solution

```python
import sys
sys.setrecursionlimit(100000)

memo = {}

def solve(n):
  if n == 0:
    return 0

  if n in memo:
    return memo[n]

  # Either keep the coin or exchange it
  exchanged = solve(n // 2) + solve(n // 3) + solve(n // 4)
  result = max(n, exchanged)

  memo[n] = result
  return result

def main():
  try:
    while True:
      n = int(input())
      print(solve(n))
  except EOFError:
    pass

if __name__ == "__main__":
  main()
```

##### Alternative

```python
def solve_iterative(n):
  if n < 12:
    return n

  # Use dictionary for sparse memoization
  dp = {}

  def get_value(x):
    if x < 12:
      return x
    if x in dp:
      return dp[x]

    result = max(x, get_value(x // 2) + get_value(x // 3) + get_value(x // 4))
    dp[x] = result
    return result

  return get_value(n)

def main():
  try:
    while True:
      n = int(input())
      print(solve_iterative(n))
  except EOFError:
    pass

if __name__ == "__main__":
  main()
```

##### Complexity Analysis
- **Time Complexity:** O(n) unique subproblems, but due to the division, it's actually O(log^3 n) approximately
- **Space Complexity:** O(log n) for recursion stack and memoization

##### Key Insight
For small values of n (n < 12), it's always better to keep the coin since n/2 + n/3 + n/4 < n. For larger values, exchanging becomes profitable.

---

### Ingenuous Cubrency

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

People in Cubeland use cubic coins. Not only the unit of currency is called a cube but also the coins are shaped like cubes and their values are cubes. Coins with values of all cubic numbers up to 9261 (= 21³), i.e., coins with the denominations of 1, 8, 27, ..., up to 9261 cubes, are available in Cubeland.

Your task is to count the number of ways to pay a given amount using cubic coins of Cubeland.

For example, there are 3 ways to pay 21 cubes:
- Twenty one 1-cube coins
- One 8-cube coin and thirteen 1-cube coins
- Two 8-cube coins and five 1-cube coins

#### Input Format
- Input consists of lines each containing an integer amount to be paid.
- All amounts are positive and less than 10000.

#### Output Format
For each of the given amounts, output one line containing the number of ways to pay the given amount using the coins available in Cubeland.

#### Solution

##### Approach
This is a classic coin change counting problem (unbounded knapsack variant). We have coins with values 1³, 2³, 3³, ..., 21³ and need to count the number of ways to make a given amount.

Use dynamic programming where `dp[i]` = number of ways to make amount `i`.

##### Python Solution

```python
def solve():
  # Precompute cubic coins: 1, 8, 27, 64, ..., 9261
  coins = [i**3 for i in range(1, 22)]  # 1^3 to 21^3

  # Precompute dp for all amounts up to 10000
  MAX_AMOUNT = 10000
  dp = [0] * (MAX_AMOUNT + 1)
  dp[0] = 1  # One way to make 0: use no coins

  # For each coin, update all amounts that can use it
  for coin in coins:
    for amount in range(coin, MAX_AMOUNT + 1):
      dp[amount] += dp[amount - coin]

  # Process queries
  import sys
  for line in sys.stdin:
    n = int(line.strip())
    print(dp[n])

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def count_ways(amount):
  coins = [i**3 for i in range(1, 22)]

  dp = [0] * (amount + 1)
  dp[0] = 1

  for coin in coins:
    if coin > amount:
      break
    for i in range(coin, amount + 1):
      dp[i] += dp[i - coin]

  return dp[amount]

def solve():
  while True:
    try:
      n = int(input())
      print(count_ways(n))
    except EOFError:
      break

if __name__ == "__main__":
  solve()
```

### Solution with Memoization

```python
from functools import lru_cache

def solve():
  coins = tuple(i**3 for i in range(1, 22))

  @lru_cache(maxsize=None)
  def count(amount, idx):
    if amount == 0:
      return 1
    if amount < 0 or idx >= len(coins):
      return 0

    # Don't use current coin OR use it (and stay at same index for unlimited use)
    return count(amount, idx + 1) + count(amount - coins[idx], idx)

  while True:
    try:
      n = int(input())
      print(count(n, 0))
    except EOFError:
      break

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N × K) where N is the amount and K is the number of coin types (21)
- **Space Complexity:** O(N) for the dp array

##### Key Insight
This is the classic "coin change ways" problem. The key to counting combinations (not permutations) is to iterate over coins in the outer loop and amounts in the inner loop. This ensures each combination is counted exactly once by enforcing an ordering on coin usage.

The coins are: 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197, 2744, 3375, 4096, 4913, 5832, 6859, 8000, 9261

---

### K-based Numbers

#### Problem Information
- **Source:** Timus Online Judge
- **Difficulty:** Secret
- **Time Limit:** 500ms
- **Memory Limit:** 256MB

#### Problem Statement

Let's consider K-based numbers, containing exactly N digits. We define a number to be valid if its K-based notation doesn't contain two successive zeros. For example:

- 1010230 is a valid 7-digit number
- 1000198 is not a valid number (contains "00")
- 0001235 is not a 7-digit number, it is a 4-digit number

Given two numbers N and K, you are to calculate an amount of valid K-based numbers, containing N digits. You may assume that 2 ≤ K ≤ 10; N ≥ 2; N + K ≤ 18.

#### Input Format
The numbers N and K in decimal notation separated by the line break.

#### Output Format
The result in decimal notation.

#### Solution

##### Approach
Use dynamic programming where:
- `dp[i][0]` = count of valid i-digit numbers ending with 0
- `dp[i][1]` = count of valid i-digit numbers ending with non-zero

Transitions:
- A number ending with 0 can only be extended from a number ending with non-zero (to avoid "00")
- A number ending with non-zero can be extended from any valid number

##### Python Solution

```python
def solve():
  n = int(input())
  k = int(input())

  # dp[i][0] = valid i-digit numbers ending with 0
  # dp[i][1] = valid i-digit numbers ending with non-zero

  # First digit cannot be 0 (would make it not N digits)
  # dp[1][0] = 0 (first digit can't be 0)
  # dp[1][1] = k-1 (digits 1 to k-1)

  dp = [[0, 0] for _ in range(n + 1)]
  dp[1][0] = 0  # First digit cannot be 0
  dp[1][1] = k - 1  # First digit can be 1 to k-1

  for i in range(2, n + 1):
    # Ending with 0: previous must end with non-zero
    dp[i][0] = dp[i-1][1]

    # Ending with non-zero: previous can be anything
    # (k-1) choices for the current non-zero digit
    dp[i][1] = (dp[i-1][0] + dp[i-1][1]) * (k - 1)

  # Total valid N-digit numbers
  print(dp[n][0] + dp[n][1])

if __name__ == "__main__":
  solve()
```

### Space Optimized Solution

```python
def solve():
  n = int(input())
  k = int(input())

  # Only need previous state
  end_zero = 0      # Numbers ending with 0
  end_nonzero = k - 1  # Numbers ending with non-zero (first digit: 1 to k-1)

  for i in range(2, n + 1):
    new_end_zero = end_nonzero
    new_end_nonzero = (end_zero + end_nonzero) * (k - 1)

    end_zero = new_end_zero
    end_nonzero = new_end_nonzero

  print(end_zero + end_nonzero)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(1) for optimized version, O(N) for basic DP

---

### Minimum Indexed Character

#### Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a string `str` and another string `patt`. Find the character in `patt` that is present at the minimum index in `str`. If no character of `patt` is present in `str` then print "No character present".

#### Input Format
- The first line of input contains an integer T denoting the number of test cases.
- Each test case contains two strings `str` and `patt` respectively.
- 1 ≤ T ≤ 10^5
- The total length of two strings in all test cases is not larger than 2 × 10^5.

#### Output Format
Output the character in `patt` that is present at the minimum index in `str`. Print "No character present" (without quotes) if no character of `patt` is present in `str`.

#### Solution

##### Approach
1. Create a set/dictionary of all characters in `str` for O(1) lookup
2. Iterate through `patt` and find the first character that exists in `str`
3. Return that character, or "No character present" if none found

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    str_input, patt = input().split()

    # Create set of characters in str for O(1) lookup
    str_chars = set(str_input)

    result = "No character present"

    # Find first character in patt that exists in str
    for char in patt:
      if char in str_chars:
        result = char
        break

    print(result)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  t = int(input())

  for _ in range(t):
    str_input, patt = input().split()

    # Map each character to its first occurrence index in str
    char_index = {}
    for i, char in enumerate(str_input):
      if char not in char_index:
        char_index[char] = i

    min_index = float('inf')
    result_char = None

    # Find character in patt with minimum index in str
    for char in patt:
      if char in char_index and char_index[char] < min_index:
        min_index = char_index[char]
        result_char = char

    if result_char:
      print(result_char)
    else:
      print("No character present")

if __name__ == "__main__":
  solve()
```

##### One-liner

```python
def solve():
  t = int(input())

  for _ in range(t):
    s, p = input().split()
    chars = set(s)
    result = next((c for c in p if c in chars), "No character present")
    print(result)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(|str| + |patt|) per test case
- **Space Complexity:** O(|str|) for the character set

##### Key Insight
The problem asks for the character from `patt` that appears at the minimum index in `str`. This is equivalent to finding the first character in `patt` that exists anywhere in `str`, since we iterate through `patt` in order and the first match will have the smallest index in our iteration (which corresponds to appearing earliest in `patt`, but the actual requirement is minimum index in `str`).

Note: The wording is slightly ambiguous - if we need the character that appears earliest in `str` (regardless of order in `patt`), we would use the alternative solution that tracks actual indices.

---

### OR in Matrix

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Define logical OR on {0, 1}: result is 1 if either or both values are 1, otherwise 0.

Nam has matrix A of m×n with elements 0 or 1. He creates matrix B where:
- B[i][j] = A[i][1] OR A[i][2] OR ... OR A[i][n] (OR of row i) AND A[1][j] OR A[2][j] OR ... OR A[m][j] (OR of column j)

Actually: B[i][j] = OR of all elements in row i AND column j of matrix A.

Given matrix B, find if matrix A exists that produces B.

#### Input Format
- First line: m, n (dimensions)
- Next m lines: n integers (matrix B, each element is 0 or 1)

#### Output Format
Print "NO" if no valid A exists. Otherwise print "YES" and a valid matrix A.

#### Solution

##### Approach
Key observations:
1. If B[i][j] = 0, then both row i of A and column j of A must be all zeros
2. If B[i][j] = 1, then at least one element in row i OR column j of A must be 1

Strategy:
1. Start with A filled with 1s
2. For each B[i][j] = 0, set entire row i and column j of A to 0
3. Verify: compute B' from A and check if B' = B

##### Python Solution

```python
def solve():
  m, n = map(int, input().split())
  B = []
  for _ in range(m):
    row = list(map(int, input().split()))
    B.append(row)

  # Initialize A with all 1s
  A = [[1] * n for _ in range(m)]

  # For each B[i][j] = 0, entire row i and column j of A must be 0
  for i in range(m):
    for j in range(n):
      if B[i][j] == 0:
        # Set row i to all 0s
        for k in range(n):
          A[i][k] = 0
        # Set column j to all 0s
        for k in range(m):
          A[k][j] = 0

  # Verify: compute B' from A
  # B'[i][j] = (OR of row i) OR (OR of column j)?
  # Actually B[i][j] = OR of (A[i][k] for all k) combined with OR of (A[k][j] for all k)
  # Re-reading: B[i][j] is OR of all A in row i, then OR with OR of all A in column j

  # Precompute row OR and column OR
  row_or = [0] * m
  col_or = [0] * n

  for i in range(m):
    for j in range(n):
      row_or[i] |= A[i][j]
      col_or[j] |= A[i][j]

  # B'[i][j] = row_or[i] | col_or[j]
  valid = True
  for i in range(m):
    for j in range(n):
      computed = row_or[i] | col_or[j]
      if computed != B[i][j]:
        valid = False
        break
    if not valid:
      break

  if valid:
    print("YES")
    for row in A:
      print(' '.join(map(str, row)))
  else:
    print("NO")

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  m, n = map(int, input().split())
  B = [list(map(int, input().split())) for _ in range(m)]

  # For B[i][j] = 0: row i and col j in A must be all 0s
  # For B[i][j] = 1: at least one of row i or col j in A must have a 1

  zero_rows = set()
  zero_cols = set()

  for i in range(m):
    for j in range(n):
      if B[i][j] == 0:
        zero_rows.add(i)
        zero_cols.add(j)

  # Build A: 1 unless in zero_row or zero_col
  A = [[0 if i in zero_rows or j in zero_cols else 1
    for j in range(n)] for i in range(m)]

  # Verify
  row_or = [any(A[i]) for i in range(m)]
  col_or = [any(A[i][j] for i in range(m)) for j in range(n)]

  for i in range(m):
    for j in range(n):
      expected = 1 if (row_or[i] or col_or[j]) else 0
      if expected != B[i][j]:
        print("NO")
        return

  print("YES")
  for row in A:
    print(' '.join(map(str, row)))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(m × n)
- **Space Complexity:** O(m × n)

##### Key Insight
B[i][j] = 0 forces all of row i and column j in A to be 0. After marking these constraints, fill remaining cells with 1. Then verify the constructed A produces B. If B[i][j] = 1 but all of row i and column j are forced to 0, no solution exists.

---

### Philosophers Stone

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Harry is in a chamber with h×w tiles, each containing some philosopher's stones. He starts at any tile in the first row and moves to the last row, collecting stones along the way.

Movement rules:
- From a tile, he can move to the tile directly below, diagonally below-left, or diagonally below-right

Find the maximum stones Harry can collect.

#### Input Format
- T test cases
- Each test case:
  - First line: h (rows), w (columns)
  - Next h lines: w integers (stones on each tile)

#### Output Format
For each test case, print the maximum stones collectible.

#### Solution

##### Approach
Classic DP problem. Let dp[i][j] = max stones collectible reaching tile (i, j).

Transition: dp[i][j] = stones[i][j] + max(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])

Base case: dp[0][j] = stones[0][j] for all j in first row.

Answer: max(dp[h-1][j]) for all j.

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    h, w = map(int, input().split())
    stones = []
    for _ in range(h):
      row = list(map(int, input().split()))
      stones.append(row)

    # dp[i][j] = max stones to reach (i, j)
    dp = [[0] * w for _ in range(h)]

    # Base case: first row
    for j in range(w):
      dp[0][j] = stones[0][j]

    # Fill DP
    for i in range(1, h):
      for j in range(w):
        # Can come from (i-1, j-1), (i-1, j), (i-1, j+1)
        best = dp[i-1][j]  # directly above

        if j > 0:
          best = max(best, dp[i-1][j-1])  # above-left
        if j < w - 1:
          best = max(best, dp[i-1][j+1])  # above-right

        dp[i][j] = stones[i][j] + best

    # Answer is max in last row
    print(max(dp[h-1]))

if __name__ == "__main__":
  solve()
```

### Space-Optimized Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    h, w = map(int, input().split())
    stones = []
    for _ in range(h):
      row = list(map(int, input().split()))
      stones.append(row)

    # Only need previous row
    prev = stones[0][:]

    for i in range(1, h):
      curr = [0] * w
      for j in range(w):
        best = prev[j]
        if j > 0:
          best = max(best, prev[j-1])
        if j < w - 1:
          best = max(best, prev[j+1])
        curr[j] = stones[i][j] + best
      prev = curr

    print(max(prev))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(h × w) per test case
- **Space Complexity:** O(w) with optimization

##### Key Insight
This is a path-finding DP where we want to maximize the sum collected. Each cell can be reached from three cells above it. Process row by row, keeping track of the maximum stones reachable at each position.

---

## Session 2

### Advanced Fruits

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Create a shortest name for a new fruit that contains both original fruit names as substrings. For example, "apple" and "pear" can combine to "applear" (contains both "apple" and "pear").

#### Input Format
- Multiple test cases until EOF
- Each line: two fruit names (alphabetic, max 100 chars each)

#### Output Format
For each test case, output the shortest combined name.

#### Solution

##### Approach
This is the Shortest Common Supersequence (SCS) problem. The SCS length is:
`len(A) + len(B) - LCS(A, B)`

To construct the SCS:
1. Compute LCS DP table
2. Backtrack to build the result, including non-LCS characters

##### Python Solution

```python
def shortest_supersequence(a, b):
  m, n = len(a), len(b)

  # LCS DP table
  dp = [[0] * (n + 1) for _ in range(m + 1)]

  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if a[i-1] == b[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1
      else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

  # Backtrack to construct SCS
  result = []
  i, j = m, n

  while i > 0 and j > 0:
    if a[i-1] == b[j-1]:
      result.append(a[i-1])
      i -= 1
      j -= 1
    elif dp[i-1][j] > dp[i][j-1]:
      result.append(a[i-1])
      i -= 1
    else:
      result.append(b[j-1])
      j -= 1

  # Add remaining characters
  while i > 0:
    result.append(a[i-1])
    i -= 1
  while j > 0:
    result.append(b[j-1])
    j -= 1

  return ''.join(reversed(result))

def solve():
  import sys
  for line in sys.stdin:
    parts = line.strip().split()
    if len(parts) < 2:
      continue
    a, b = parts[0], parts[1]
    print(shortest_supersequence(a, b))

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  import sys
  for line in sys.stdin:
    parts = line.strip().split()
    if len(parts) < 2:
      continue
    a, b = parts[0], parts[1]

    m, n = len(a), len(b)

    # dp[i][j] = shortest supersequence of a[:i] and b[:j]
    dp = [[""] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(1, m + 1):
      dp[i][0] = a[:i]
    for j in range(1, n + 1):
      dp[0][j] = b[:j]

    for i in range(1, m + 1):
      for j in range(1, n + 1):
        if a[i-1] == b[j-1]:
          dp[i][j] = dp[i-1][j-1] + a[i-1]
        else:
          if len(dp[i-1][j]) < len(dp[i][j-1]):
            dp[i][j] = dp[i-1][j] + a[i-1]
          else:
            dp[i][j] = dp[i][j-1] + b[j-1]

    print(dp[m][n])

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(m × n)
- **Space Complexity:** O(m × n)

##### Key Insight
The Shortest Common Supersequence is the inverse of LCS. We want the shortest string containing both inputs as subsequences. By finding LCS, we know which characters can be shared, then merge the rest in order. The backtracking builds the SCS by including LCS characters once and non-LCS characters from both strings.

---

### Aibohphobia

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 10000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a string S, find the minimum number of characters to insert to make it a palindrome.

For example:
- "fft" → "tfft" (insert 1 character)
- "ab" → "aba" or "bab" (insert 1 character)

#### Input Format
- Multiple test cases
- Each line: string S (max 6100 chars, no whitespace)

#### Output Format
For each test case, print the minimum insertions needed.

#### Solution

##### Approach
The minimum insertions = len(S) - LPS(S), where LPS is the Longest Palindromic Subsequence.

LPS of string S equals LCS of S and reverse(S).

Alternatively, use direct DP:
- dp[i][j] = min insertions to make S[i:j+1] a palindrome
- If S[i] == S[j]: dp[i][j] = dp[i+1][j-1]
- Else: dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])

##### Python Solution

```python
def solve():
  import sys
  input = sys.stdin.readline

  while True:
    line = input()
    if not line:
      break
    s = line.strip()
    if not s:
      continue

    n = len(s)

    # LPS via LCS with reverse
    rev = s[::-1]

    # Space-optimized LCS
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, n + 1):
      for j in range(1, n + 1):
        if s[i-1] == rev[j-1]:
          curr[j] = prev[j-1] + 1
        else:
          curr[j] = max(prev[j], curr[j-1])
      prev, curr = curr, prev

    lps = prev[n]
    print(n - lps)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  import sys
  input = sys.stdin.readline

  while True:
    line = input()
    if not line:
      break
    s = line.strip()
    if not s:
      continue

    n = len(s)

    # dp[i][j] = min insertions for s[i:j+1]
    # Use only 2 rows since dp[i] depends on dp[i+1]
    # Actually for gap-based DP:

    # dp[length][start] but we can optimize
    # Use dp[j] = min insertions for substring ending at j with some length

    # Simpler: dp[i] = min insertions for s[i:] to be palindrome when matching with s[:n-i]

    # Direct approach with LPS
    # dp[i][j] = LPS of s[i:j+1]
    # dp[i][i] = 1
    # dp[i][j] = dp[i+1][j-1] + 2 if s[i] == s[j]
    #          = max(dp[i+1][j], dp[i][j-1]) otherwise

    if n <= 1:
      print(0)
      continue

    # Space optimized: process by length
    prev = [1] * n  # length 1 substrings
    curr = [0] * n

    for length in range(2, n + 1):
      for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j]:
          curr[i] = prev[i+1] + 2 if length > 2 else 2
        else:
          curr[i] = max(prev[i], prev[i+1] if i+1 < n else 0)
          # Actually need different indexing

      prev, curr = curr, [0] * n

    lps = prev[0]
    print(n - lps)

if __name__ == "__main__":
  solve()
```

### Cleaner LCS Solution

```python
import sys
sys.setrecursionlimit(10000)

def solve():
  for line in sys.stdin:
    s = line.strip()
    if not s:
      continue

    n = len(s)
    rev = s[::-1]

    # LCS of s and rev = LPS of s
    # dp[i][j] = LCS of s[:i] and rev[:j]
    dp = [[0] * (n + 1) for _ in range(2)]

    for i in range(1, n + 1):
      for j in range(1, n + 1):
        if s[i-1] == rev[j-1]:
          dp[i % 2][j] = dp[(i-1) % 2][j-1] + 1
        else:
          dp[i % 2][j] = max(dp[(i-1) % 2][j], dp[i % 2][j-1])

    lps = dp[n % 2][n]
    print(n - lps)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n²)
- **Space Complexity:** O(n) with optimization

##### Key Insight
Minimum insertions to make a palindrome = n - LPS (Longest Palindromic Subsequence). LPS can be found as LCS of string with its reverse. Characters not in the LPS need matching characters inserted, hence the formula.

---

### Compromise

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Two politicians submit proposals as sequences of words. Find and print the longest common subsequence of words from both proposals.

#### Input Format
- Multiple test cases until EOF
- Each test case: two texts (sequences of lowercase words)
- Words < 30 chars, texts < 100 words each
- Texts separated by '#', test cases separated by '#'

#### Output Format
For each test case, print the longest common subsequence of words.

#### Solution

##### Approach
Standard LCS problem but on sequences of words instead of characters.
1. Parse both texts into word arrays
2. Compute LCS using DP
3. Backtrack to reconstruct the actual LCS sequence

##### Python Solution

```python
def solve():
  import sys

  lines = sys.stdin.read().strip().split('\n')
  i = 0

  while i < len(lines):
    # Read first text until '#'
    text1 = []
    while i < len(lines) and lines[i].strip() != '#':
      text1.extend(lines[i].split())
      i += 1
    i += 1  # skip '#'

    # Read second text until '#' or EOF
    text2 = []
    while i < len(lines) and lines[i].strip() != '#':
      text2.extend(lines[i].split())
      i += 1
    i += 1  # skip '#'

    if not text1 or not text2:
      continue

    # LCS on word arrays
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
      for j in range(1, n + 1):
        if text1[i-1] == text2[j-1]:
          dp[i][j] = dp[i-1][j-1] + 1
        else:
          dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack to get LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
      if text1[i-1] == text2[j-1]:
        lcs.append(text1[i-1])
        i -= 1
        j -= 1
      elif dp[i-1][j] > dp[i][j-1]:
        i -= 1
      else:
        j -= 1

    lcs.reverse()
    print(' '.join(lcs))

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def lcs_words(words1, words2):
  m, n = len(words1), len(words2)

  # dp[i][j] = LCS length of words1[:i] and words2[:j]
  dp = [[0] * (n + 1) for _ in range(m + 1)]

  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if words1[i-1] == words2[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1
      else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

  # Reconstruct
  result = []
  i, j = m, n
  while i > 0 and j > 0:
    if words1[i-1] == words2[j-1]:
      result.append(words1[i-1])
      i -= 1
      j -= 1
    elif dp[i-1][j] >= dp[i][j-1]:
      i -= 1
    else:
      j -= 1

  return result[::-1]

def solve():
  import sys
  content = sys.stdin.read()

  # Split by '#' to get test cases
  parts = content.strip().split('#')

  i = 0
  while i + 1 < len(parts):
    text1 = parts[i].split()
    text2 = parts[i + 1].split()

    if text1 and text2:
      result = lcs_words(text1, text2)
      print(' '.join(result))

    i += 2

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(m × n) where m, n are word counts
- **Space Complexity:** O(m × n)

##### Key Insight
This is the classic LCS problem applied to word sequences rather than character sequences. The algorithm is identical: build a DP table where dp[i][j] represents the LCS length of the first i words of text1 and first j words of text2. Backtrack to reconstruct the actual sequence.

---

### Cross-country

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Agnes participates in cross-country races where participants follow route cards specifying checkpoints. She wants to choose a date from her admirers based on who can meet her the most times during the race.

Scoring rules:
- A runner scores one point if he meets Agnes at a checkpoint
- After scoring, both must move to their next checkpoints before scoring again
- Routes may cross the same checkpoint multiple times
- Each competitor must follow their card exactly

Find the maximum number of times Tom can meet Agnes.

#### Input Format
- First line: d (number of data sets, 1 ≤ d ≤ 10)
- For each data set:
  - First line: Agnes' route (checkpoints separated by spaces, ending with 0)
  - Following lines: Tom's possible routes (each ending with 0)
  - A line starting with 0 marks end of data set
- Checkpoints are integers in [1, 1000]
- 2 to 2000 checkpoints per route

#### Output Format
For each data set, output the maximum number of times Tom can meet Agnes.

#### Solution

##### Approach
This is a **Longest Common Subsequence (LCS)** problem! Tom needs to find checkpoints that appear in both his and Agnes' routes in the same order. The maximum meetings equals the LCS length between Agnes' route and Tom's route.

##### Python Solution

```python
def lcs(agnes, tom):
  """Find longest common subsequence length"""
  m, n = len(agnes), len(tom)
  dp = [[0] * (n + 1) for _ in range(m + 1)]

  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if agnes[i-1] == tom[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1
      else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

  return dp[m][n]

def solve():
  d = int(input())

  for _ in range(d):
    # Read Agnes' route
    agnes = []
    line = input().split()
    for x in line:
      val = int(x)
      if val == 0:
        break
      agnes.append(val)

    max_meetings = 0

    # Read Tom's routes
    while True:
      line = input().split()

      # Check for end of data set
      if line[0] == '0':
        break

      tom = []
      for x in line:
        val = int(x)
        if val == 0:
          break
        tom.append(val)

      # Compute LCS
      meetings = lcs(agnes, tom)
      max_meetings = max(max_meetings, meetings)

    print(max_meetings)

if __name__ == "__main__":
  solve()
```

### Space-Optimized Solution

```python
def lcs_optimized(agnes, tom):
  """LCS with O(n) space"""
  m, n = len(agnes), len(tom)
  prev = [0] * (n + 1)
  curr = [0] * (n + 1)

  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if agnes[i-1] == tom[j-1]:
        curr[j] = prev[j-1] + 1
      else:
        curr[j] = max(prev[j], curr[j-1])
    prev, curr = curr, [0] * (n + 1)

  return prev[n]

def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  d = int(data[idx])
  idx += 1

  for _ in range(d):
    # Read Agnes' route
    agnes = []
    while data[idx] != '0':
      agnes.append(int(data[idx]))
      idx += 1
    idx += 1  # Skip the 0

    max_meetings = 0

    # Read Tom's routes
    while True:
      if data[idx] == '0':
        idx += 1
        break

      tom = []
      while data[idx] != '0':
        tom.append(int(data[idx]))
        idx += 1
      idx += 1  # Skip the 0

      meetings = lcs_optimized(agnes, tom)
      max_meetings = max(max_meetings, meetings)

    print(max_meetings)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(M × N) per route comparison where M and N are route lengths
- **Space Complexity:** O(M × N) for standard LCS, O(N) for optimized version

##### Key Insight
The problem is exactly LCS (Longest Common Subsequence). Agnes and Tom both follow their routes in order, and Tom scores a point each time they're at the same checkpoint. This is equivalent to finding common elements that appear in the same relative order in both sequences - the definition of LCS.

---

### LCS of three strings

#### Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given three strings X, Y, and Z, find the length of their longest common subsequence.

#### Input Format
- T test cases
- Each test case:
  - First line: n, m, k (lengths of X, Y, Z)
  - Second line: three space-separated strings X, Y, Z

#### Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N, M, K ≤ 100

#### Output Format
For each test case, print the LCS length.

#### Solution

##### Approach
Extend the 2D LCS DP to 3D:
- dp[i][j][k] = LCS length of X[:i], Y[:j], Z[:k]
- If X[i-1] == Y[j-1] == Z[k-1]: dp[i][j][k] = dp[i-1][j-1][k-1] + 1
- Else: dp[i][j][k] = max(dp[i-1][j][k], dp[i][j-1][k], dp[i][j][k-1])

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, m, k = map(int, input().split())
    parts = input().split()
    X, Y, Z = parts[0], parts[1], parts[2]

    # 3D DP
    dp = [[[0] * (k + 1) for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
      for j in range(1, m + 1):
        for l in range(1, k + 1):
          if X[i-1] == Y[j-1] == Z[l-1]:
            dp[i][j][l] = dp[i-1][j-1][l-1] + 1
          else:
            dp[i][j][l] = max(dp[i-1][j][l],
                    dp[i][j-1][l],
                    dp[i][j][l-1])

    print(dp[n][m][k])

if __name__ == "__main__":
  solve()
```

### Space-Optimized Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, m, k = map(int, input().split())
    parts = input().split()
    X, Y, Z = parts[0], parts[1], parts[2]

    # Only need 2 layers: current and previous for first dimension
    prev = [[0] * (k + 1) for _ in range(m + 1)]
    curr = [[0] * (k + 1) for _ in range(m + 1)]

    for i in range(1, n + 1):
      # Also need prev_j for second dimension
      prev_j = [0] * (k + 1)

      for j in range(1, m + 1):
        prev_l = 0
        for l in range(1, k + 1):
          if X[i-1] == Y[j-1] == Z[l-1]:
            curr[j][l] = prev[j-1][l-1] + 1
          else:
            curr[j][l] = max(prev[j][l],
                    curr[j-1][l],
                    curr[j][l-1])

      prev, curr = curr, [[0] * (k + 1) for _ in range(m + 1)]

    print(prev[m][k])

if __name__ == "__main__":
  solve()
```

##### Recursive

```python
import sys
sys.setrecursionlimit(1000000)

def solve():
  t = int(input())

  for _ in range(t):
    n, m, k = map(int, input().split())
    parts = input().split()
    X, Y, Z = parts[0], parts[1], parts[2]

    memo = {}

    def lcs(i, j, l):
      if i == 0 or j == 0 or l == 0:
        return 0

      if (i, j, l) in memo:
        return memo[(i, j, l)]

      if X[i-1] == Y[j-1] == Z[l-1]:
        result = lcs(i-1, j-1, l-1) + 1
      else:
        result = max(lcs(i-1, j, l), lcs(i, j-1, l), lcs(i, j, l-1))

      memo[(i, j, l)] = result
      return result

    print(lcs(n, m, k))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n × m × k)
- **Space Complexity:** O(n × m × k), can be reduced to O(m × k)

##### Key Insight
The 3-string LCS is a natural extension of 2-string LCS to 3D. When all three characters match, we extend the LCS. Otherwise, we try excluding one character at a time from each string and take the maximum.

---

### Love Calculator

#### Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given two names, find:
1. The length of the shortest string containing both names as subsequences
2. The number of such shortest strings

#### Input Format
- T test cases (T ≤ 125)
- Each test case: two lines with names (≤ 30 capital letters each)

#### Output Format
For each test case: "Case X: L C" where L is shortest length and C is count of unique shortest strings.

#### Solution

##### Approach
This is the Shortest Common Supersequence (SCS) problem with counting.

1. Length = len(A) + len(B) - LCS(A, B)
2. Count requires counting all optimal paths in the LCS DP table

Use two DP tables:
- dp[i][j] = LCS length of A[:i] and B[:j]
- cnt[i][j] = number of ways to achieve SCS of A[:i] and B[:j]

##### Python Solution

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    a = input().strip()
    b = input().strip()

    m, n = len(a), len(b)

    # LCS DP
    lcs = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
      for j in range(1, n + 1):
        if a[i-1] == b[j-1]:
          lcs[i][j] = lcs[i-1][j-1] + 1
        else:
          lcs[i][j] = max(lcs[i-1][j], lcs[i][j-1])

    # SCS length
    scs_len = m + n - lcs[m][n]

    # Count SCS: cnt[i][j] = ways to form SCS of a[:i] and b[:j]
    cnt = [[0] * (n + 1) for _ in range(m + 1)]
    cnt[0][0] = 1

    # Base cases
    for i in range(1, m + 1):
      cnt[i][0] = 1
    for j in range(1, n + 1):
      cnt[0][j] = 1

    for i in range(1, m + 1):
      for j in range(1, n + 1):
        if a[i-1] == b[j-1]:
          # Must take this character (extends LCS)
          cnt[i][j] = cnt[i-1][j-1]
        else:
          # Choose which character to append
          # Only count paths that maintain optimal LCS
          if lcs[i-1][j] > lcs[i][j-1]:
            cnt[i][j] = cnt[i-1][j]
          elif lcs[i][j-1] > lcs[i-1][j]:
            cnt[i][j] = cnt[i][j-1]
          else:
            cnt[i][j] = cnt[i-1][j] + cnt[i][j-1]

    print(f"Case {case}: {scs_len} {cnt[m][n]}")

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    a = input().strip()
    b = input().strip()

    m, n = len(a), len(b)

    # dp[i][j] = (scs_length, count) for a[:i] and b[:j]
    # scs_length = i + j - lcs[i][j]

    lcs = [[0] * (n + 1) for _ in range(m + 1)]
    cnt = [[0] * (n + 1) for _ in range(m + 1)]

    # Base: empty strings
    cnt[0][0] = 1
    for i in range(1, m + 1):
      cnt[i][0] = 1  # Only one way: use all of a
    for j in range(1, n + 1):
      cnt[0][j] = 1  # Only one way: use all of b

    for i in range(1, m + 1):
      for j in range(1, n + 1):
        if a[i-1] == b[j-1]:
          lcs[i][j] = lcs[i-1][j-1] + 1
          cnt[i][j] = cnt[i-1][j-1]
        else:
          lcs[i][j] = max(lcs[i-1][j], lcs[i][j-1])

          if lcs[i-1][j] > lcs[i][j-1]:
            cnt[i][j] = cnt[i-1][j]
          elif lcs[i][j-1] > lcs[i-1][j]:
            cnt[i][j] = cnt[i][j-1]
          else:
            cnt[i][j] = cnt[i-1][j] + cnt[i][j-1]

    scs_len = m + n - lcs[m][n]
    print(f"Case {case}: {scs_len} {cnt[m][n]}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(m × n)
- **Space Complexity:** O(m × n)

##### Key Insight
SCS length = len(A) + len(B) - LCS(A,B). For counting, when characters match we must use that match (one path). When they don't match, we can go either direction if both give optimal LCS, so we add the counts. This counts distinct ways to interleave non-LCS characters while maintaining order.

---

### Palindromic characteristics

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

The palindromic characteristics of string s is a sequence of |s| integers, where the k-th number is the count of non-empty substrings that are k-palindromes.

A string is a 1-palindrome if it reads the same forward and backward.
A string is a k-palindrome (k > 1) if:
1. Its left half equals its right half
2. Both halves are (k-1)-palindromes

Count the number of k-palindrome substrings for each k from 1 to |s|.

#### Input Format
- Single line: string s (1 ≤ |s| ≤ 5000, lowercase)

#### Output Format
Print |s| integers - the palindromic characteristics.

#### Solution

##### Approach
1. First, find all palindromic substrings using Manacher's or DP
2. For each palindrome, compute its k-level
3. A palindrome of length L has k-level = 1 + k-level of its half (if half is palindrome)

Use DP:
- is_pal[i][j] = true if s[i:j+1] is palindrome
- k_level[i][j] = k-palindrome level of s[i:j+1]

##### Python Solution

```python
def solve():
  s = input().strip()
  n = len(s)

  if n == 0:
    return

  # is_pal[i][j] = True if s[i:j+1] is palindrome
  is_pal = [[False] * n for _ in range(n)]

  # Base cases: single characters
  for i in range(n):
    is_pal[i][i] = True

  # Length 2
  for i in range(n - 1):
    is_pal[i][i + 1] = (s[i] == s[i + 1])

  # Longer palindromes
  for length in range(3, n + 1):
    for i in range(n - length + 1):
      j = i + length - 1
      is_pal[i][j] = (s[i] == s[j]) and is_pal[i + 1][j - 1]

  # k_level[i][j] = k-palindrome level
  k_level = [[0] * n for _ in range(n)]

  # Compute k-levels for all palindromes
  for length in range(1, n + 1):
    for i in range(n - length + 1):
      j = i + length - 1
      if is_pal[i][j]:
        if length == 1:
          k_level[i][j] = 1
        else:
          # Half length
          half_len = length // 2
          half_end = i + half_len - 1
          # Left half is s[i:i+half_len]
          k_level[i][j] = 1 + k_level[i][half_end]

  # Count palindromes at each k-level
  count = [0] * (n + 1)

  for i in range(n):
    for j in range(i, n):
      if is_pal[i][j]:
        count[k_level[i][j]] += 1

  # A k-palindrome is also a (k-1)-palindrome, etc.
  # Propagate counts downward
  for k in range(n, 1, -1):
    count[k - 1] += count[k]

  # Output counts for k = 1 to n
  print(' '.join(map(str, count[1:n + 1])))

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  s = input().strip()
  n = len(s)

  # is_pal[i][j] = True if s[i:j+1] is palindrome
  is_pal = [[False] * n for _ in range(n)]

  for i in range(n):
    is_pal[i][i] = True
  for i in range(n - 1):
    is_pal[i][i + 1] = (s[i] == s[i + 1])
  for length in range(3, n + 1):
    for i in range(n - length + 1):
      j = i + length - 1
      is_pal[i][j] = (s[i] == s[j]) and is_pal[i + 1][j - 1]

  # k_level for each palindrome
  k_level = [[0] * n for _ in range(n)]

  # Process by increasing length to use computed half values
  for length in range(1, n + 1):
    for i in range(n - length + 1):
      j = i + length - 1
      if is_pal[i][j]:
        if length == 1:
          k_level[i][j] = 1
        else:
          half = (length - 1) // 2
          # Left half: s[i : i + half + 1]
          k_level[i][j] = 1 + k_level[i][i + half]

  # Count by k-level
  count = [0] * (n + 2)
  for i in range(n):
    for j in range(i, n):
      if is_pal[i][j]:
        count[k_level[i][j]] += 1

  # Propagate: k-palindrome is also (k-1)-palindrome
  for k in range(n, 0, -1):
    count[k - 1] += count[k]

  print(' '.join(map(str, count[1:n + 1])))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n²)
- **Space Complexity:** O(n²)

##### Key Insight
First find all palindromic substrings with standard DP. Then compute k-levels: a palindrome's k-level is 1 + k-level of its left half (if half is also a palindrome). Finally, since a k-palindrome is also (k-1), (k-2), ... 1-palindrome, propagate counts downward.

---

## Session 3

### Beautiful People

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

A prestigious club has N members, each with strength Si and beauty Bi. Member i hates member j if Si < Sj and Bi > Bj, or Si > Sj and Bi < Bj.

For a party, select maximum members such that no two hate each other. Two members don't hate each other if Si ≤ Sj and Bi ≤ Bj (or vice versa).

#### Input Format
- First line: N (number of members, 2 ≤ N ≤ 100,000)
- Next N lines: Si and Bi (1 ≤ Si, Bi ≤ 10^9)

#### Output Format
- First line: maximum members that can be invited
- Second line: their indices (1-indexed)

#### Solution

##### Approach
This is a variant of Longest Increasing Subsequence (LIS) in 2D.

1. Sort members by strength Si
2. For members with same strength, sort by beauty Bi in descending order
3. Find LIS on beauty values

The descending sort for same strength ensures we don't pick two members with same strength but different beauty (which would hate each other).

##### Python Solution

```python
import bisect

def solve():
  n = int(input())
  members = []

  for i in range(n):
    s, b = map(int, input().split())
    members.append((s, b, i + 1))  # (strength, beauty, original_index)

  # Sort by strength ascending, then beauty descending (for same strength)
  members.sort(key=lambda x: (x[0], -x[1]))

  # LIS on beauty with index tracking
  # dp[i] = smallest ending beauty for LIS of length i+1
  # parent tracking for reconstruction

  dp = []  # (beauty, index in members)
  dp_idx = []  # index in members array for each dp entry
  parent = [-1] * n
  pos = [-1] * n  # position in LIS for each member

  for i, (s, b, orig_idx) in enumerate(members):
    # Binary search for position
    idx = bisect.bisect_left(dp, b)

    if idx == len(dp):
      dp.append(b)
      dp_idx.append(i)
    else:
      dp[idx] = b
      dp_idx[idx] = i

    pos[i] = idx
    if idx > 0:
      parent[i] = dp_idx[idx - 1]

  # Reconstruct LIS
  lis_length = len(dp)
  result = []

  # Find the last element in LIS
  curr = dp_idx[lis_length - 1]
  while curr != -1:
    result.append(members[curr][2])  # original index
    curr = parent[curr]

  result.reverse()

  print(lis_length)
  print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
import bisect

def solve():
  n = int(input())
  members = []

  for i in range(n):
    s, b = map(int, input().split())
    members.append((s, b, i + 1))

  # Sort: strength ascending, beauty descending for same strength
  members.sort(key=lambda x: (x[0], -x[1]))

  # Extract beauties for LIS
  beauties = [m[1] for m in members]

  # LIS with reconstruction
  tails = []  # tails[i] = smallest ending value for LIS of length i+1
  tail_indices = []
  predecessor = [-1] * n
  lis_pos = [0] * n

  for i in range(n):
    b = beauties[i]
    pos = bisect.bisect_left(tails, b)

    if pos == len(tails):
      tails.append(b)
      tail_indices.append(i)
    else:
      tails[pos] = b
      tail_indices[pos] = i

    lis_pos[i] = pos
    if pos > 0:
      predecessor[i] = tail_indices[pos - 1]

  # Reconstruct
  lis_len = len(tails)
  path = []
  idx = tail_indices[-1]

  while idx != -1:
    path.append(members[idx][2])
    idx = predecessor[idx]

  path.reverse()

  print(lis_len)
  print(' '.join(map(str, path)))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N)
- **Space Complexity:** O(N)

##### Key Insight
After sorting by strength, the problem reduces to LIS on beauty. The key trick: for same strength, sort beauty descending to prevent selecting multiple members with same strength (as that would mean one hates the other if beauties differ). LIS with binary search gives O(N log N) complexity.

---

### Check Transcription

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a binary string s (0s and 1s) and a text t (lowercase letters), find the number of ways to assign non-empty strings r0 and r1 (r0 ≠ r1) such that replacing each 0 in s with r0 and each 1 with r1 produces t.

#### Input Format
- First line: binary string s (2 ≤ |s| ≤ 10^5)
- Second line: text t (1 ≤ |t| ≤ 10^6)

#### Output Format
Print the number of valid (r0, r1) pairs.

#### Solution

##### Approach
Let c0 = count of 0s in s, c1 = count of 1s in s.
If r0 has length L0 and r1 has length L1, then:
`c0 * L0 + c1 * L1 = len(t)`

Iterate over possible L0 values, compute L1, then verify if the assignment is consistent using hashing.

##### Python Solution

```python
def solve():
  s = input().strip()
  t = input().strip()

  c0 = s.count('0')
  c1 = s.count('1')
  n = len(s)
  m = len(t)

  # Special case: all same characters in s
  first_char = s[0]

  count = 0

  # Try all possible lengths for r_first_char
  # c0 * L0 + c1 * L1 = m
  # L0 >= 1, L1 >= 1

  for L_first in range(1, m + 1):
    # Remaining length after assigning L_first to first_char
    if first_char == '0':
      L0 = L_first
      if c1 == 0:
        if c0 * L0 == m:
          # Check consistency
          r0 = t[:L0]
          # Verify all 0s map to r0
          valid = True
          pos = 0
          for ch in s:
            if t[pos:pos + L0] != r0:
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
    else:
      L1 = L_first
      if c0 == 0:
        if c1 * L1 == m:
          r1 = t[:L1]
          valid = True
          pos = 0
          for ch in s:
            if t[pos:pos + L1] != r1:
              valid = False
              break
            pos += L1
          if valid:
            count += 1
        continue

      remaining = m - c1 * L1
      if remaining <= 0 or remaining % c0 != 0:
        continue
      L0 = remaining // c0
      if L0 <= 0:
        continue

    # Verify consistency
    r0, r1 = None, None
    valid = True
    pos = 0

    for ch in s:
      if ch == '0':
        substr = t[pos:pos + L0]
        if r0 is None:
          r0 = substr
        elif r0 != substr:
          valid = False
          break
        pos += L0
      else:
        substr = t[pos:pos + L1]
        if r1 is None:
          r1 = substr
        elif r1 != substr:
          valid = False
          break
        pos += L1

    if valid and r0 != r1:
      count += 1

  print(count)

if __name__ == "__main__":
  solve()
```

##### Optimized

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

##### Complexity Analysis
- **Time Complexity:** O(|t|/min(c0,c1) × |s|) with hashing
- **Space Complexity:** O(|t|)

##### Key Insight
The constraint c0×L0 + c1×L1 = |t| limits possible (L0, L1) pairs. For each valid pair, verify consistency by checking that all occurrences of 0 map to the same substring and all 1s map to another (different) substring. Polynomial hashing makes substring comparison O(1).

---

### Prince And Princess

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

On an n×n chessboard, Prince makes p jumps visiting p+1 distinct squares (x1, x2, ..., x_{p+1}). Princess makes q jumps visiting q+1 distinct squares (y1, y2, ..., y_{q+1}).

Find the longest common subsequence of their paths - the maximum number of squares they both visit in the same order.

#### Input Format
- Multiple test cases
- Each test case:
  - First line: n, p, q
  - Second line: p+1 integers (Prince's path)
  - Third line: q+1 integers (Princess's path)

#### Output Format
For each test case: "Case X: L" where L is the LCS length.

#### Solution

##### Approach
Direct LCS would be O(p×q) which is too slow for p, q up to 62500.

Key insight: All numbers in each sequence are distinct and ≤ n².
Transform to LIS: Map Prince's sequence to positions 1, 2, ..., p+1. Then for each element in Princess's sequence, replace with its position in Prince's sequence (or skip if not present). The LCS equals LIS of the transformed sequence.

##### Python Solution

```python
import bisect

def solve():
  import sys
  input = sys.stdin.readline

  case = 0
  while True:
    line = input().split()
    if not line:
      break

    n, p, q = int(line[0]), int(line[1]), int(line[2])
    case += 1

    prince = list(map(int, input().split()))
    princess = list(map(int, input().split()))

    # Map prince's sequence to positions
    pos = {}
    for i, val in enumerate(prince):
      pos[val] = i

    # Transform princess's sequence
    transformed = []
    for val in princess:
      if val in pos:
        transformed.append(pos[val])

    # LIS on transformed sequence
    if not transformed:
      print(f"Case {case}: 0")
      continue

    tails = []
    for x in transformed:
      idx = bisect.bisect_left(tails, x)
      if idx == len(tails):
        tails.append(x)
      else:
        tails[idx] = x

    print(f"Case {case}: {len(tails)}")

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
import bisect
import sys

def solve():
  input = sys.stdin.readline
  case = 0

  while True:
    try:
      line = input()
      if not line.strip():
        break
      n, p, q = map(int, line.split())
    except:
      break

    case += 1

    prince = list(map(int, input().split()))
    princess = list(map(int, input().split()))

    # Create position map for prince
    prince_pos = {v: i for i, v in enumerate(prince)}

    # Convert princess to positions in prince's sequence
    seq = [prince_pos[v] for v in princess if v in prince_pos]

    # LIS
    dp = []
    for x in seq:
      pos = bisect.bisect_left(dp, x)
      if pos == len(dp):
        dp.append(x)
      else:
        dp[pos] = x

    print(f"Case {case}: {len(dp)}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O((p + q) log(p))
- **Space Complexity:** O(p + q)

##### Key Insight
LCS of two sequences with distinct elements can be reduced to LIS. Map first sequence elements to their indices. Transform second sequence using this mapping (keeping only common elements). LCS length equals LIS length of transformed sequence. This reduces O(pq) to O((p+q) log p).

---

### Testing the CATCHER

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

A CATCHER missile defense system can intercept missiles if:
1. The missile is the first one, OR
2. The missile height is ≤ the height of the last intercepted missile

Given a sequence of incoming missile heights, find the maximum number of missiles the CATCHER can intercept.

#### Input Format
- Multiple test cases
- Each test case: sequence of missile heights ending with -1
- Input ends with -1 as first value

#### Output Format
For each test: "Test #X:" followed by "maximum possible number of missiles: Y"

#### Solution

##### Approach
This is the Longest Non-Increasing Subsequence problem, which is equivalent to:
- Longest Decreasing Subsequence (LDS) if heights are strictly decreasing
- Or Longest Non-Increasing Subsequence if equal heights allowed

Since each missile must have height ≤ previous intercepted missile, we need the longest non-increasing subsequence.

This equals the Longest Increasing Subsequence of the reversed sequence.

##### Python Solution

```python
import bisect

def longest_non_increasing(arr):
  """Find length of longest non-increasing subsequence"""
  if not arr:
    return 0

  # Reverse and find LIS with non-strict inequality
  # Or: find longest non-decreasing in reversed array
  # Equivalent to finding LIS on negated values

  # For non-increasing: each next element <= previous
  # Use LIS on negated values with bisect_right for non-strict

  tails = []
  for x in arr:
    neg_x = -x
    # bisect_right for non-strict (allowing equal)
    idx = bisect.bisect_right(tails, neg_x)
    if idx == len(tails):
      tails.append(neg_x)
    else:
      tails[idx] = neg_x

  return len(tails)

def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0
  case = 0

  while idx < len(data):
    missiles = []
    while idx < len(data):
      h = int(data[idx])
      idx += 1
      if h == -1:
        break
      missiles.append(h)

    if not missiles:
      break

    case += 1
    result = longest_non_increasing(missiles)

    if case > 1:
      print()
    print(f"Test #{case}:")
    print(f"  maximum possible number of missiles intercepted: {result}")

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  import sys
  data = list(map(int, sys.stdin.read().split()))
  idx = 0
  case = 0

  while idx < len(data):
    missiles = []
    while idx < len(data):
      h = data[idx]
      idx += 1
      if h == -1:
        break
      missiles.append(h)

    if not missiles:
      break

    case += 1
    n = len(missiles)

    # dp[i] = length of longest non-increasing subsequence ending at i
    dp = [1] * n

    for i in range(1, n):
      for j in range(i):
        if missiles[j] >= missiles[i]:
          dp[i] = max(dp[i], dp[j] + 1)

    result = max(dp)

    if case > 1:
      print()
    print(f"Test #{case}:")
    print(f"  maximum possible number of missiles intercepted: {result}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) with binary search, O(n²) with basic DP
- **Space Complexity:** O(n)

##### Key Insight
The problem asks for the longest subsequence where each element is ≤ the previous one (non-increasing). This is the reverse of LIS. Use LIS algorithm on negated values, using bisect_right instead of bisect_left to handle equal elements (non-strict inequality).

---

### The Tower of Babylon

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

The Babylonians have n types of blocks with unlimited supply. Each block type has dimensions (xi, yi, zi). Blocks can be rotated to use any two dimensions as the base.

Build the tallest tower by stacking blocks such that each block's base dimensions are strictly smaller than the block below it.

#### Input Format
- Multiple test cases
- Each test case:
  - First line: n (number of block types, n ≤ 30)
  - Next n lines: three integers (xi, yi, zi)
- Input ends with n = 0

#### Output Format
For each test case: "Case X: maximum height = H"

#### Solution

##### Approach
1. Generate all rotations of each block (3 orientations per block: each dimension as height)
2. Sort blocks by base area (or by one base dimension)
3. Apply LIS-style DP: for each block, find the tallest tower ending with that block

A block can be placed on another if both base dimensions are strictly smaller.

##### Python Solution

```python
def solve():
  case = 0

  while True:
    n = int(input())
    if n == 0:
      break

    case += 1

    # Generate all rotations
    blocks = []  # (base1, base2, height)

    for _ in range(n):
      dims = list(map(int, input().split()))
      x, y, z = dims

      # All 3 rotations (choosing each dimension as height)
      # Store as (min_base, max_base, height) for consistent comparison
      rotations = [
        (min(y, z), max(y, z), x),
        (min(x, z), max(x, z), y),
        (min(x, y), max(x, y), z)
      ]

      for rot in rotations:
        blocks.append(rot)

    # Sort by base area (or by first dimension)
    blocks.sort()

    m = len(blocks)

    # dp[i] = max height of tower with blocks[i] on top
    dp = [b[2] for b in blocks]  # Initialize with just the block's height

    for i in range(1, m):
      for j in range(i):
        # blocks[j] can be below blocks[i] if strictly smaller base
        if blocks[j][0] < blocks[i][0] and blocks[j][1] < blocks[i][1]:
          dp[i] = max(dp[i], dp[j] + blocks[i][2])

    max_height = max(dp)
    print(f"Case {case}: maximum height = {max_height}")

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  import sys
  input = sys.stdin.readline
  case = 0

  while True:
    n = int(input())
    if n == 0:
      break

    case += 1
    blocks = []

    for _ in range(n):
      x, y, z = map(int, input().split())

      # Generate all orientations
      # (width, depth, height) - width <= depth for consistency
      dims = sorted([x, y, z])
      a, b, c = dims

      # Three unique orientations
      blocks.append((a, b, c))  # smallest two as base
      blocks.append((a, c, b))  # smallest and largest as base
      blocks.append((b, c, a))  # two largest as base

    # Remove duplicates and sort
    blocks = list(set(blocks))
    blocks.sort()

    m = len(blocks)
    dp = [0] * m

    for i in range(m):
      dp[i] = blocks[i][2]  # height of current block

      for j in range(i):
        if blocks[j][0] < blocks[i][0] and blocks[j][1] < blocks[i][1]:
          dp[i] = max(dp[i], dp[j] + blocks[i][2])

    print(f"Case {case}: maximum height = {max(dp)}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n² × 9) = O(n²) since at most 3n blocks after rotation
- **Space Complexity:** O(n)

##### Key Insight
Each block can be oriented in 3 ways (choosing which dimension is height). Generate all orientations, then this becomes a DAG longest path problem. Sort by base dimensions and use DP where dp[i] = max tower height with block i on top. A block j can support block i if both of j's base dimensions are strictly smaller.

---

### Wavio Sequence

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

A Wavio sequence has these properties:
- Length L = 2n + 1 (odd length)
- First n+1 integers are strictly increasing
- Last n+1 integers are strictly decreasing
- No adjacent integers are equal

Find the length of the longest Wavio subsequence.

Example: In "1 2 3 2 1 2 3 4 3 2 1 5 4 1 2 3 2 2 1", the longest Wavio is "1 2 3 4 5 4 3 2 1" with length 9.

#### Input Format
- Multiple test cases until EOF
- Each test case:
  - First line: N (1 ≤ N ≤ 10000)
  - Following lines: N integers

#### Output Format
For each test case, print the length of longest Wavio sequence.

#### Solution

##### Approach
For each position i:
1. Compute LIS ending at i (increasing from left)
2. Compute LDS starting at i (decreasing to right)
3. Wavio with peak at i has length 2 * min(LIS[i], LDS[i]) - 1

Use binary search for O(n log n) LIS/LDS computation.

##### Python Solution

```python
import bisect

def compute_lis_ending(arr):
  """For each i, compute length of LIS ending at i"""
  n = len(arr)
  lis = [0] * n
  tails = []

  for i in range(n):
    pos = bisect.bisect_left(tails, arr[i])
    lis[i] = pos + 1

    if pos == len(tails):
      tails.append(arr[i])
    else:
      tails[pos] = arr[i]

  return lis

def compute_lds_starting(arr):
  """For each i, compute length of LDS starting at i"""
  n = len(arr)
  lds = [0] * n
  tails = []

  # Process from right to left
  for i in range(n - 1, -1, -1):
    pos = bisect.bisect_left(tails, arr[i])
    lds[i] = pos + 1

    if pos == len(tails):
      tails.append(arr[i])
    else:
      tails[pos] = arr[i]

  return lds

def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  while idx < len(data):
    n = int(data[idx])
    idx += 1

    arr = []
    for _ in range(n):
      arr.append(int(data[idx]))
      idx += 1

    # Compute LIS ending at each position
    lis = compute_lis_ending(arr)

    # Compute LDS starting at each position
    lds = compute_lds_starting(arr)

    # Find max Wavio length
    max_wavio = 0
    for i in range(n):
      # Wavio with peak at i
      k = min(lis[i], lds[i])
      wavio_len = 2 * k - 1
      max_wavio = max(max_wavio, wavio_len)

    print(max_wavio)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
import bisect
import sys

def solve():
  input_data = sys.stdin.read().split()
  idx = 0

  while idx < len(input_data):
    n = int(input_data[idx])
    idx += 1

    arr = [int(input_data[idx + i]) for i in range(n)]
    idx += n

    # LIS[i] = length of longest strictly increasing subsequence ending at i
    LIS = [0] * n
    tails = []
    for i in range(n):
      pos = bisect.bisect_left(tails, arr[i])
      LIS[i] = pos + 1
      if pos == len(tails):
        tails.append(arr[i])
      else:
        tails[pos] = arr[i]

    # LDS[i] = length of longest strictly decreasing subsequence starting at i
    # Equivalent to LIS from right with negated values
    LDS = [0] * n
    tails = []
    for i in range(n - 1, -1, -1):
      pos = bisect.bisect_left(tails, arr[i])
      LDS[i] = pos + 1
      if pos == len(tails):
        tails.append(arr[i])
      else:
        tails[pos] = arr[i]

    # Maximum Wavio length
    result = max(2 * min(LIS[i], LDS[i]) - 1 for i in range(n))
    print(result)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n)

##### Key Insight
A Wavio sequence is a "mountain" shape: strictly increasing to a peak, then strictly decreasing. For each position as the peak, the Wavio length is 2 * min(LIS_ending_here, LDS_starting_here) - 1. The minimum ensures both sides can match in length. Pre-compute LIS and LDS arrays in O(n log n) using binary search.

---

## Session 4

### DNA sequences

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Find the longest common subsequence of two strings where the subsequence must be formed by consecutive segments of length at least K from both strings.

For example, with K=3 and strings "lovxxelyxxxxx" and "xxxxxxxlovely":
- "lovely" is not valid (segment "lov" has length 3, but other segments don't)
- "loxxxelyxxxxx" is valid if all matching segments have length ≥ K

#### Input Format
- Multiple test cases until line with 0
- Each test case:
  - First line: K (minimum segment length)
  - Next two lines: the two strings (lowercase, length ≤ 1000)

#### Output Format
For each test case, print the length of the longest valid subsequence, or 0 if none exists.

#### Solution

##### Approach
Modified LCS where we track consecutive matches:
- dp[i][j][len] = whether we can match with current segment of length `len`
- Or simpler: dp[i][j] = length of current matching segment ending at (i,j)
- Keep track of best valid subsequence length

##### Python Solution

```python
def solve():
  while True:
    k = int(input())
    if k == 0:
      break

    s1 = input().strip()
    s2 = input().strip()

    n, m = len(s1), len(s2)

    # dp[i][j] = length of consecutive match ending at s1[i-1], s2[j-1]
    # best[i][j] = best valid LCS length ending before or at (i,j)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best = [[0] * (m + 1) for _ in range(n + 1)]

    result = 0

    for i in range(1, n + 1):
      for j in range(1, m + 1):
        # Update best from previous positions
        best[i][j] = max(best[i-1][j], best[i][j-1])

        if s1[i-1] == s2[j-1]:
          dp[i][j] = dp[i-1][j-1] + 1

          # If segment length >= k, it's valid
          if dp[i][j] >= k:
            # Can extend previous best by segment length
            # best[i-dp[i][j]][j-dp[i][j]] + dp[i][j]
            seg_start_i = i - dp[i][j]
            seg_start_j = j - dp[i][j]
            candidate = best[seg_start_i][seg_start_j] + dp[i][j]
            best[i][j] = max(best[i][j], candidate)
            result = max(result, best[i][j])
        else:
          dp[i][j] = 0

    print(result)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  while True:
    k = int(input())
    if k == 0:
      break

    s1 = input().strip()
    s2 = input().strip()

    n, m = len(s1), len(s2)

    # match[i][j] = length of matching segment ending at i,j
    match = [[0] * (m + 1) for _ in range(n + 1)]

    # dp[i][j] = max LCS with valid segments ending at or before i,j
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
      for j in range(1, m + 1):
        # Propagate best from neighbors
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        if s1[i-1] == s2[j-1]:
          match[i][j] = match[i-1][j-1] + 1

          # Check all valid segment lengths >= k
          for seg_len in range(k, match[i][j] + 1):
            prev_i = i - seg_len
            prev_j = j - seg_len
            dp[i][j] = max(dp[i][j], dp[prev_i][prev_j] + seg_len)

    print(dp[n][m])

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  while True:
    k = int(input())
    if k == 0:
      break

    s1 = input().strip()
    s2 = input().strip()

    n, m = len(s1), len(s2)

    # match[i][j] = consecutive match length ending at i-1, j-1
    match = [[0] * (m + 1) for _ in range(n + 1)]
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
      for j in range(1, m + 1):
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        if s1[i-1] == s2[j-1]:
          match[i][j] = match[i-1][j-1] + 1

          if match[i][j] >= k:
            # Use segment of exactly k or extend
            start_i = i - k
            start_j = j - k
            dp[i][j] = max(dp[i][j], dp[start_i][start_j] + k)

            # Or extend existing segment
            if match[i][j] > k:
              dp[i][j] = max(dp[i][j], dp[i-1][j-1] + 1)

    print(dp[n][m])

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n × m) or O(n × m × min(n,m)) for simpler version
- **Space Complexity:** O(n × m)

##### Key Insight
Track both the current consecutive match length and the best valid LCS so far. When a segment reaches length K, it becomes valid and can extend the previous best. The key is that once a segment is valid (≥K), adding one more character keeps it valid.

---

### Dividing coins

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 5000ms
- **Memory Limit:** 512MB

#### Problem Statement

Divide a bag of coins between two people as fairly as possible. Minimize the absolute difference between the total values each person receives.

#### Input Format
- First line: n (number of test cases)
- Each test case:
  - Line 1: m (number of coins, m ≤ 100)
  - Line 2: m coin values (1 to 500 cents each)

#### Output Format
For each test case, print the minimum possible difference.

#### Solution

##### Approach
This is the Partition Problem - a variant of subset sum.

Let total = sum of all coins. We want to find subset with sum closest to total/2. The minimum difference will be total - 2 * (closest sum to total/2).

Use DP to find all achievable sums up to total/2.

##### Python Solution

```python
def solve():
  n = int(input())

  for _ in range(n):
    m = int(input())
    coins = list(map(int, input().split()))

    total = sum(coins)
    target = total // 2

    # dp[i] = True if sum i is achievable
    dp = [False] * (target + 1)
    dp[0] = True

    for coin in coins:
      # Process in reverse to avoid using same coin twice
      for s in range(target, coin - 1, -1):
        if dp[s - coin]:
          dp[s] = True

    # Find largest achievable sum <= target
    for s in range(target, -1, -1):
      if dp[s]:
        best = s
        break

    # Minimum difference
    print(total - 2 * best)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  n = int(input())

  for _ in range(n):
    m = int(input())
    coins = list(map(int, input().split()))

    total = sum(coins)
    target = total // 2

    # Use integer as bitset for achievable sums
    achievable = 1  # bit 0 set = sum 0 achievable

    for coin in coins:
      achievable |= (achievable << coin)

    # Mask to only consider sums <= target
    mask = (1 << (target + 1)) - 1
    achievable &= mask

    # Find highest set bit
    best = achievable.bit_length() - 1

    print(total - 2 * best)

if __name__ == "__main__":
  solve()
```

##### Recursive

```python
def solve():
  n = int(input())

  for _ in range(n):
    m = int(input())
    coins = list(map(int, input().split()))

    total = sum(coins)
    target = total // 2

    memo = {}

    def can_make(idx, remaining):
      if remaining == 0:
        return True
      if idx == m or remaining < 0:
        return False

      if (idx, remaining) in memo:
        return memo[(idx, remaining)]

      result = can_make(idx + 1, remaining) or \
          can_make(idx + 1, remaining - coins[idx])

      memo[(idx, remaining)] = result
      return result

    # Find largest achievable sum
    for s in range(target, -1, -1):
      if can_make(0, s):
        print(total - 2 * s)
        break

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(m × total)
- **Space Complexity:** O(total)

##### Key Insight
To minimize difference when splitting into two groups, find a subset with sum as close to total/2 as possible. If one group has sum S, the other has total - S, difference is |total - 2S|. This is minimized when S is closest to total/2. Use 0/1 knapsack DP to find achievable sums.

---

### Diving for Gold

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

John the diver wants to recover gold from a shipwreck. He has limited air (t seconds underwater). Each treasure has:
- Depth di
- Gold value vi
- Time to descend: w × di
- Time to ascend: 2w × di

Total time for treasure i: 3w × di

Find the maximum gold John can recover and which treasures to take.

#### Input Format
- Multiple test cases (blank line separated)
- Each test case:
  - First line: t (time limit) and w (constant)
  - Second line: n (number of treasures)
  - Next n lines: di and vi (depth and gold value)

#### Output Format
For each test case:
- Line 1: Maximum gold
- Line 2: Number of treasures recovered
- Following lines: depth and gold of each recovered treasure (in input order)

#### Solution

##### Approach
This is a 0/1 Knapsack problem.
- Weight of item i: 3 × w × di (time cost)
- Value of item i: vi (gold)
- Capacity: t (time limit)

Track which items are selected for reconstruction.

##### Python Solution

```python
def solve():
  import sys
  data = sys.stdin.read().strip().split('\n')
  idx = 0
  first = True

  while idx < len(data):
    # Skip empty lines
    while idx < len(data) and not data[idx].strip():
      idx += 1

    if idx >= len(data):
      break

    t, w = map(int, data[idx].split())
    idx += 1

    n = int(data[idx])
    idx += 1

    treasures = []
    for _ in range(n):
      d, v = map(int, data[idx].split())
      treasures.append((d, v))
      idx += 1

    # Calculate time cost for each treasure
    costs = [3 * w * d for d, v in treasures]
    values = [v for d, v in treasures]

    # 0/1 Knapsack
    # dp[c] = max gold with time capacity c
    dp = [0] * (t + 1)
    # For reconstruction: track which items
    parent = [[-1] * (t + 1) for _ in range(n + 1)]

    for i in range(n):
      for c in range(t, costs[i] - 1, -1):
        if dp[c - costs[i]] + values[i] > dp[c]:
          dp[c] = dp[c - costs[i]] + values[i]

    # Reconstruction with separate tracking
    # Re-run with full tracking
    dp2 = [[0] * (t + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
      for c in range(t + 1):
        dp2[i][c] = dp2[i-1][c]
        if c >= costs[i-1] and dp2[i-1][c - costs[i-1]] + values[i-1] > dp2[i][c]:
          dp2[i][c] = dp2[i-1][c - costs[i-1]] + values[i-1]

    # Backtrack to find items
    selected = []
    c = t
    for i in range(n, 0, -1):
      if dp2[i][c] != dp2[i-1][c]:
        selected.append(i - 1)
        c -= costs[i-1]

    selected.reverse()

    # Output
    if not first:
      print()
    first = False

    print(dp[t])
    print(len(selected))
    for i in selected:
      print(treasures[i][0], treasures[i][1])

if __name__ == "__main__":
  solve()
```

### Space-Optimized with Reconstruction

```python
def solve():
  import sys
  input_data = sys.stdin.read().strip().split('\n')
  idx = 0
  first = True

  while idx < len(input_data):
    while idx < len(input_data) and not input_data[idx].strip():
      idx += 1

    if idx >= len(input_data):
      break

    t, w = map(int, input_data[idx].split())
    idx += 1

    n = int(input_data[idx])
    idx += 1

    treasures = []
    for _ in range(n):
      d, v = map(int, input_data[idx].split())
      treasures.append((d, v))
      idx += 1

    # Time costs
    costs = [3 * w * d for d, v in treasures]
    values = [v for d, v in treasures]

    # DP with item tracking
    # dp[c] = (max_value, set of item indices)
    INF = float('inf')
    dp = [(0, []) for _ in range(t + 1)]

    for i in range(n):
      for c in range(t, costs[i] - 1, -1):
        prev_val, prev_items = dp[c - costs[i]]
        new_val = prev_val + values[i]

        if new_val > dp[c][0]:
          dp[c] = (new_val, prev_items + [i])

    max_gold, selected = dp[t]

    if not first:
      print()
    first = False

    print(max_gold)
    print(len(selected))
    for i in selected:
      print(treasures[i][0], treasures[i][1])

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n × t)
- **Space Complexity:** O(n × t) for reconstruction, O(t) for value only

##### Key Insight
Classic 0/1 knapsack where each treasure's "weight" is the time cost (3 × w × depth) and "value" is the gold. Track selected items during DP for reconstruction. Output must preserve original input order of selected treasures.

---

### Exact Change

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

You want to buy an item priced at P cents. You have n bills/coins with various denominations. The seller doesn't give change. Find:
1. The minimum amount you must pay (≥ P)
2. The minimum number of bills/coins to pay that amount

#### Input Format
- First line: number of test cases
- Each test case:
  - Line 1: price P (up to 10000 cents)
  - Line 2: n (number of bills/coins, up to 100)
  - Next n lines: value of each bill/coin (up to 10000 cents)

Total value of bills ≥ P.

#### Output Format
For each test case: "amount_paid number_of_items"

#### Solution

##### Approach
Modified subset sum where we want the minimum sum ≥ P using minimum items.

DP state: dp[s] = minimum coins to make exactly sum s
Since we need sum ≥ P, track sums up to some reasonable limit (P + max_coin or total sum).

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    price = int(input())
    n = int(input())
    coins = [int(input()) for _ in range(n)]

    # Maximum sum we might need to consider
    # At most price + max single coin (to avoid overpaying too much)
    max_sum = min(price + max(coins), sum(coins))

    INF = float('inf')

    # dp[s] = minimum coins to achieve sum exactly s
    dp = [INF] * (max_sum + 1)
    dp[0] = 0

    for coin in coins:
      # Process in reverse (0/1 knapsack)
      for s in range(max_sum, coin - 1, -1):
        if dp[s - coin] != INF:
          dp[s] = min(dp[s], dp[s - coin] + 1)

    # Find minimum sum >= price with minimum coins
    best_sum = -1
    best_coins = INF

    for s in range(price, max_sum + 1):
      if dp[s] != INF:
        if dp[s] < best_coins:
          best_sum = s
          best_coins = dp[s]
          break  # First valid sum >= price with minimum coins

    # Actually need to find minimum sum first, then minimum coins for that sum
    # Re-interpret: find smallest sum >= price that is achievable
    for s in range(price, max_sum + 1):
      if dp[s] != INF:
        print(s, dp[s])
        break

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  t = int(input())

  for _ in range(t):
    price = int(input())
    n = int(input())
    coins = [int(input()) for _ in range(n)]

    total = sum(coins)
    max_sum = total  # Could be smarter but safe

    INF = float('inf')

    # dp[s] = minimum number of coins to make sum s
    dp = [INF] * (max_sum + 1)
    dp[0] = 0

    for coin in coins:
      for s in range(max_sum, coin - 1, -1):
        if dp[s - coin] < INF:
          dp[s] = min(dp[s], dp[s - coin] + 1)

    # Find smallest achievable sum >= price
    result_sum = -1
    result_coins = -1

    for s in range(price, max_sum + 1):
      if dp[s] < INF:
        result_sum = s
        result_coins = dp[s]
        break

    print(result_sum, result_coins)

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  import sys
  input = sys.stdin.readline

  t = int(input())

  for _ in range(t):
    price = int(input())
    n = int(input())
    coins = [int(input()) for _ in range(n)]

    # Limit search space
    max_coin = max(coins)
    limit = price + max_coin

    INF = n + 1  # Can't use more than n coins

    dp = [INF] * (limit + 1)
    dp[0] = 0

    for coin in coins:
      for s in range(limit, coin - 1, -1):
        if dp[s - coin] < INF:
          dp[s] = min(dp[s], dp[s - coin] + 1)

    # Find minimum achievable sum >= price
    for s in range(price, limit + 1):
      if dp[s] < INF:
        print(s, dp[s])
        break

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n × (P + max_coin))
- **Space Complexity:** O(P + max_coin)

##### Key Insight
First priority: minimize amount paid (smallest sum ≥ P). Second priority: minimize coins used. Use 0/1 knapsack to find achievable sums and minimum coins for each sum. Then scan from P upward to find the first achievable sum - this automatically satisfies both criteria since we pick the smallest valid sum first.

---

### Pick The Sticks

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 5000ms
- **Memory Limit:** 512MB

#### Problem Statement

Place gold sticks of various lengths on a container of length L. Sticks can overlap the container ends as long as their center of gravity remains inside. Maximize the total value of sticks placed.

Key insight: At most 2 sticks can hang over edges (one on each side), and they can extend by up to half their length.

#### Input Format
- T test cases
- Each test case:
  - First line: N (sticks), L (container length)
  - Next N lines: ai (stick length), vi (stick value)

#### Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N ≤ 500
- 1 ≤ L ≤ 1000
- 1 ≤ ai ≤ 1000
- 1 ≤ vi ≤ 10^9

#### Output Format
For each test case: "Case #x: y" where y is maximum value.

#### Solution

##### Approach
Modified 0/1 knapsack with states tracking how many sticks hang over edges (0, 1, or 2).

dp[i][j][k] = max value using capacity j with k sticks hanging over edges (k ∈ {0, 1, 2})

For a hanging stick, it only uses half its length of container space.

##### Python Solution

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    n, L = map(int, input().split())

    sticks = []
    for _ in range(n):
      a, v = map(int, input().split())
      sticks.append((a, v))

    # Multiply L by 2 to avoid floating point
    L *= 2

    # dp[capacity][hanging_count] = max value
    # hanging_count: 0, 1, or 2
    INF = float('-inf')

    # Initialize
    dp = [[INF] * 3 for _ in range(L + 1)]
    dp[0][0] = 0

    for a, v in sticks:
      full_len = a * 2  # full stick length (doubled)
      half_len = a      # half length (since L is doubled)

      # Process in reverse for 0/1 knapsack
      new_dp = [row[:] for row in dp]

      for c in range(L + 1):
        for h in range(3):
          if dp[c][h] == INF:
            continue

          # Option 1: Place stick fully inside (uses full length)
          if c + full_len <= L:
            new_dp[c + full_len][h] = max(new_dp[c + full_len][h], dp[c][h] + v)

          # Option 2: Place stick hanging over edge (uses half length)
          if h < 2 and c + half_len <= L:
            new_dp[c + half_len][h + 1] = max(new_dp[c + half_len][h + 1], dp[c][h] + v)

      dp = new_dp

    # Find maximum value
    result = 0
    for c in range(L + 1):
      for h in range(3):
        if dp[c][h] != INF:
          result = max(result, dp[c][h])

    print(f"Case #{case}: {result}")

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    n, L = map(int, input().split())

    sticks = []
    for _ in range(n):
      a, v = map(int, input().split())
      sticks.append((a, v))

    # Use 2*L to handle half-lengths as integers
    capacity = 2 * L
    NEG_INF = float('-inf')

    # dp[c][e] = max value with c capacity used and e edge slots used (0, 1, 2)
    dp = [[NEG_INF] * 3 for _ in range(capacity + 1)]
    dp[0][0] = 0

    for length, value in sticks:
      full_cost = 2 * length  # fully inside
      half_cost = length       # hanging (uses only half)

      # Process backwards
      for c in range(capacity, -1, -1):
        for e in range(3):
          if dp[c][e] == NEG_INF:
            continue

          # Option A: place fully inside
          nc = c + full_cost
          if nc <= capacity:
            dp[nc][e] = max(dp[nc][e], dp[c][e] + value)

          # Option B: place hanging
          if e < 2:
            nc = c + half_cost
            if nc <= capacity:
              dp[nc][e + 1] = max(dp[nc][e + 1], dp[c][e] + value)

    # Get max value
    ans = 0
    for c in range(capacity + 1):
      for e in range(3):
        if dp[c][e] != NEG_INF:
          ans = max(ans, dp[c][e])

    print(f"Case #{case}: {ans}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N × L)
- **Space Complexity:** O(L)

##### Key Insight
At most 2 sticks can hang over edges (one per side). A hanging stick uses only half its length of container space. Use 3D DP tracking: capacity used and number of hanging sticks (0/1/2). Multiply lengths by 2 to handle half-lengths as integers.

---

### Polo the Penguin and the Test

#### Problem Information
- **Source:** Codechef
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Polo has N different questions on his test. For each question i:
- Ci = number of tests containing this question
- Pi = points for correct answer
- Ti = time needed to learn this question

Polo has W minutes total. Maximize the total points he can get.

#### Input Format
- T test cases
- Each test case:
  - First line: N (questions), W (available time)
  - Next N lines: Ci, Pi, Ti for each question

#### Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N ≤ 100
- 1 ≤ Ci, Pi, Ti ≤ 100
- 1 ≤ W ≤ 100

#### Output Format
For each test case, print maximum points achievable.

#### Solution

##### Approach
This is a 0/1 Knapsack problem:
- Each question is an item
- Weight = Ti (time to learn)
- Value = Ci × Pi (total points from all tests)
- Capacity = W (total time available)

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, w = map(int, input().split())

    questions = []
    for _ in range(n):
      c, p, ti = map(int, input().split())
      questions.append((ti, c * p))  # (time_cost, value)

    # 0/1 Knapsack
    dp = [0] * (w + 1)

    for time_cost, value in questions:
      for capacity in range(w, time_cost - 1, -1):
        dp[capacity] = max(dp[capacity], dp[capacity - time_cost] + value)

    print(dp[w])

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  t = int(input())

  for _ in range(t):
    n, w = map(int, input().split())

    questions = []
    for _ in range(n):
      c, p, ti = map(int, input().split())
      questions.append((ti, c * p))

    # 2D DP for clarity
    # dp[i][j] = max value using first i questions with capacity j
    dp = [[0] * (w + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
      time_cost, value = questions[i - 1]
      for j in range(w + 1):
        # Don't take question i
        dp[i][j] = dp[i - 1][j]
        # Take question i (if possible)
        if j >= time_cost:
          dp[i][j] = max(dp[i][j], dp[i - 1][j - time_cost] + value)

    print(dp[n][w])

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N × W)
- **Space Complexity:** O(W) with optimization

##### Key Insight
Each question appears in Ci tests and gives Pi points per test, so total value is Ci × Pi. Learning a question takes Ti time. This maps directly to 0/1 knapsack: select questions to maximize total value within time budget W.

---

### Scuba diver

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

A scuba diver needs specific amounts of oxygen (t) and nitrogen (a) for a dive. He has n cylinders available, each with:
- Oxygen volume: ti
- Nitrogen volume: ai
- Weight: wi

Find the minimum total weight of cylinders to carry to meet both gas requirements.

#### Input Format
- c test cases (separated by blank lines)
- Each test case:
  - First line: t, a (required oxygen and nitrogen)
  - Second line: n (number of cylinders)
  - Next n lines: ti, ai, wi (oxygen, nitrogen, weight) for each cylinder

#### Constraints
- 1 ≤ t ≤ 21
- 1 ≤ a ≤ 79
- 1 ≤ n ≤ 1000

#### Output Format
For each test case, print the minimum weight needed.

#### Solution

##### Approach
This is a 2D knapsack problem (minimization variant):
- Two constraints: oxygen ≥ t, nitrogen ≥ a
- Minimize total weight

dp[i][j] = minimum weight to get at least i oxygen and j nitrogen

##### Python Solution

```python
def solve():
  import sys
  input = sys.stdin.readline

  c = int(input())

  for _ in range(c):
    line = input().split()
    t_req, a_req = int(line[0]), int(line[1])

    n = int(input())

    cylinders = []
    for _ in range(n):
      parts = input().split()
      ti, ai, wi = int(parts[0]), int(parts[1]), int(parts[2])
      cylinders.append((ti, ai, wi))

    INF = float('inf')

    # dp[o][n] = min weight to get at least o oxygen and n nitrogen
    dp = [[INF] * (a_req + 1) for _ in range(t_req + 1)]
    dp[0][0] = 0

    for ti, ai, wi in cylinders:
      # Process in reverse (0/1 knapsack)
      for o in range(t_req, -1, -1):
        for ni in range(a_req, -1, -1):
          if dp[o][ni] < INF:
            # New oxygen and nitrogen (cap at requirements)
            new_o = min(o + ti, t_req)
            new_n = min(ni + ai, a_req)
            dp[new_o][new_n] = min(dp[new_o][new_n], dp[o][ni] + wi)

    print(dp[t_req][a_req])

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  c = int(data[idx])
  idx += 1

  for _ in range(c):
    t_req = int(data[idx])
    a_req = int(data[idx + 1])
    idx += 2

    n = int(data[idx])
    idx += 1

    cylinders = []
    for _ in range(n):
      ti = int(data[idx])
      ai = int(data[idx + 1])
      wi = int(data[idx + 2])
      idx += 3
      cylinders.append((ti, ai, wi))

    INF = float('inf')

    # dp[oxygen][nitrogen] = min weight
    dp = [[INF] * (a_req + 1) for _ in range(t_req + 1)]
    dp[0][0] = 0

    for oxy, nit, weight in cylinders:
      new_dp = [row[:] for row in dp]

      for o in range(t_req + 1):
        for n in range(a_req + 1):
          if dp[o][n] == INF:
            continue

          # Add this cylinder
          no = min(o + oxy, t_req)
          nn = min(n + nit, a_req)
          new_dp[no][nn] = min(new_dp[no][nn], dp[o][n] + weight)

      dp = new_dp

    print(dp[t_req][a_req])

if __name__ == "__main__":
  solve()
```

### In-Place Solution

```python
def solve():
  import sys
  input = sys.stdin.readline

  c = int(input())

  for _ in range(c):
    t_req, a_req = map(int, input().split())
    n = int(input())

    INF = 10**9

    # dp[o][n] = min weight for o oxygen, n nitrogen
    dp = [[INF] * (a_req + 1) for _ in range(t_req + 1)]
    dp[0][0] = 0

    for _ in range(n):
      ti, ai, wi = map(int, input().split())

      # Reverse iteration for 0/1 knapsack
      for o in range(t_req, -1, -1):
        for ni in range(a_req, -1, -1):
          if dp[o][ni] < INF:
            new_o = min(o + ti, t_req)
            new_n = min(ni + ai, a_req)
            dp[new_o][new_n] = min(dp[new_o][new_n], dp[o][ni] + wi)

    print(dp[t_req][a_req])

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n × t × a)
- **Space Complexity:** O(t × a)

##### Key Insight
This is a 2D 0/1 knapsack where we minimize weight while meeting two constraints (oxygen ≥ t, nitrogen ≥ a). Since we need "at least" the requirements, we cap states at the requirement values - any excess doesn't help. dp[t_req][a_req] gives the minimum weight to meet both requirements exactly or exceed them.

