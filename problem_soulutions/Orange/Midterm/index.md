---
layout: simple
title: "Midterm"
permalink: /problem_soulutions/Orange/Midterm/
---
# Midterm

A collection of problems from the midterm examination covering various algorithmic concepts.

## Problems

### Examination Papers

#### Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

A professor needs to transfer examination papers from one box to another while maintaining descending order of marks. The rules are:

1. Can only withdraw/place papers from/on top of a pile
2. Three locations available: source box (Chemistry), destination box (CS), and table
3. Papers on the table must be in a single pile
4. A paper with lower marks never comes below a paper with higher marks

This is the classic Tower of Hanoi problem! Compute the number of moves required to transfer N papers.

#### Input Format
- First line: T (number of test cases)
- Next T lines: N (number of papers)

#### Constraints
- 1 ≤ T ≤ 100
- 1 ≤ N ≤ 10^9

#### Output Format
Print the number of moves required modulo 10^9 + 7 for each test case.

#### Solution

##### Approach
This is exactly the Tower of Hanoi problem:
- 3 pegs: source, destination, auxiliary (table)
- N disks (papers) of different sizes
- Rule: smaller disk must always be on top

The minimum number of moves for Tower of Hanoi with N disks is **2^N - 1**.

##### Python Solution

```python
MOD = 10**9 + 7

def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    # Tower of Hanoi formula: 2^n - 1
    result = (pow(2, n, MOD) - 1) % MOD
    print(result)

if __name__ == "__main__":
  solve()
```

### Solution with Fast Modular Exponentiation

```python
MOD = 10**9 + 7

def mod_pow(base, exp, mod):
  """Fast modular exponentiation"""
  result = 1
  base %= mod

  while exp > 0:
    if exp % 2 == 1:
      result = (result * base) % mod
    exp //= 2
    base = (base * base) % mod

  return result

def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    result = (mod_pow(2, n, MOD) - 1 + MOD) % MOD
    print(result)

if __name__ == "__main__":
  solve()
```

##### One-liner

```python
def solve():
  M = 10**9 + 7
  t = int(input())
  for _ in range(t):
    print((pow(2, int(input()), M) - 1) % M)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(log N) for modular exponentiation
- **Space Complexity:** O(1)

##### Key Insight
This is the Tower of Hanoi in disguise:
- Chemistry box = Source peg
- CS box = Destination peg
- Table = Auxiliary peg
- Papers ordered by marks = Disks of different sizes

The recurrence relation:
- T(1) = 1
- T(n) = 2 × T(n-1) + 1

Solving: T(n) = 2^n - 1

Since N can be up to 10^9, we need fast modular exponentiation to compute 2^N mod (10^9 + 7).

---

### Oliver and the Game

#### Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Oliver and Bob are playing Hide and Seek in the city of Byteland. The city has N houses connected by roads forming a tree structure with the King's Mansion at node 1 as the root.

Oliver hides in house X and Bob starts from house Y. Bob can either move:
- **Type 0**: Towards the King's Mansion (up the tree towards root)
- **Type 1**: Away from the King's Mansion (down the tree away from root)

Given Q queries, determine if Bob can find Oliver (reach house X from house Y) given the movement direction.

#### Input Format
- First line: N (total houses)
- Next N-1 lines: A B (road between houses A and B)
- Next line: Q (number of queries)
- Next Q lines: type X Y (0/1, Oliver's house, Bob's house)

#### Output Format
For each query, print "YES" if Bob can find Oliver, "NO" otherwise.

#### Solution

##### Approach
Use DFS to compute entry and exit times (Euler tour) for each node:
- Node A is ancestor of B if: entry[A] ≤ entry[B] and exit[A] ≥ exit[B]

For query (type, X, Y):
- **Type 0** (towards root): Bob can reach X only if X is an ancestor of Y
- **Type 1** (away from root): Bob can reach X only if X is a descendant of Y (Y is ancestor of X)

##### Python Solution

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200000)

def solve():
  n = int(input())

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  # DFS to compute entry and exit times
  entry = [0] * (n + 1)
  exit_time = [0] * (n + 1)
  timer = [0]

  def dfs(u, parent):
    timer[0] += 1
    entry[u] = timer[0]

    for v in adj[u]:
      if v != parent:
        dfs(v, u)

    timer[0] += 1
    exit_time[u] = timer[0]

  # Root the tree at node 1 (King's Mansion)
  dfs(1, -1)

  def is_ancestor(a, b):
    """Check if a is ancestor of b"""
    return entry[a] <= entry[b] and exit_time[a] >= exit_time[b]

  q = int(input())
  results = []

  for _ in range(q):
    query_type, x, y = map(int, input().split())

    if query_type == 0:
      # Moving towards mansion: X must be ancestor of Y
      if is_ancestor(x, y) and x != y:
        results.append("YES")
      else:
        results.append("NO")
    else:
      # Moving away from mansion: X must be descendant of Y (Y is ancestor of X)
      if is_ancestor(y, x) and x != y:
        results.append("YES")
      else:
        results.append("NO")

  print('\n'.join(results))

if __name__ == "__main__":
  solve()
```

##### Iterative

```python
from collections import defaultdict

def solve():
  n = int(input())

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  # Iterative DFS for entry/exit times
  entry = [0] * (n + 1)
  exit_time = [0] * (n + 1)

  timer = 0
  stack = [(1, -1, False)]  # (node, parent, processed)

  while stack:
    node, parent, processed = stack.pop()

    if processed:
      timer += 1
      exit_time[node] = timer
    else:
      timer += 1
      entry[node] = timer
      stack.append((node, parent, True))

      for child in adj[node]:
        if child != parent:
          stack.append((child, node, False))

  def is_ancestor(a, b):
    return entry[a] <= entry[b] and exit_time[a] >= exit_time[b]

  q = int(input())

  for _ in range(q):
    t, x, y = map(int, input().split())

    if t == 0:
      # Towards root: x must be ancestor of y
      print("YES" if x != y and is_ancestor(x, y) else "NO")
    else:
      # Away from root: x must be descendant of y
      print("YES" if x != y and is_ancestor(y, x) else "NO")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N) for DFS preprocessing, O(1) per query
- **Space Complexity:** O(N) for storing entry/exit times

##### Key Insight
Using Euler tour (entry/exit times), we can check ancestor-descendant relationships in O(1):
- A is ancestor of B iff entry[A] ≤ entry[B] and exit[A] ≥ exit[B]

Moving "towards mansion" means moving up to ancestors, and "away from mansion" means moving down to descendants.

---

### Palindromic Series

#### Problem Information
- **Source:** GeeksforGeeks
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Adobe is given a number N. He has to create an alphabetical string in lowercase from that number and check if it's a palindrome.

The mapping is: a = 0, b = 1, c = 2, ..., j = 9

For example: If the number is 61:
- The substring is "gb" (g=6, b=1)
- The length is 7 (6 + 1 = 7)
- Repeat "gb" to get 7 characters: "gbgbgbg"
- Check if "gbgbgbg" is a palindrome

**Note:** No number starts with zero. Consider alphabets a to j only (single digit numbers 0-9).

#### Input Format
- First line: T (number of test cases)
- Each test case: A number N

#### Constraints
- 1 ≤ T ≤ 10000
- 1 ≤ N ≤ 10^7

#### Output Format
For each test case, print "YES" if the string is palindrome, "NO" otherwise.

#### Solution

##### Approach
1. Extract digits from N and compute their sum (length of final string)
2. Build the string by repeating the digits cyclically until reaching the sum length
3. Check if the resulting string is a palindrome

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = input().strip()
    digits = [int(d) for d in n]
    length = sum(digits)

    # Build string of given length by repeating digits
    result = []
    idx = 0
    for i in range(length):
      result.append(digits[idx])
      idx = (idx + 1) % len(digits)

    # Check palindrome
    is_palindrome = result == result[::-1]
    print("YES" if is_palindrome else "NO")

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = input().strip()
    digits = [int(d) for d in n]
    length = sum(digits)
    num_digits = len(digits)

    # Check palindrome without building full string
    is_palindrome = True
    for i in range(length // 2):
      left_digit = digits[i % num_digits]
      right_digit = digits[(length - 1 - i) % num_digits]
      if left_digit != right_digit:
        is_palindrome = False
        break

    print("YES" if is_palindrome else "NO")

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def is_palindrome_series(n_str):
  digits = list(n_str)
  length = sum(int(d) for d in digits)
  num_digits = len(digits)

  # Build and check
  s = ''.join(digits[i % num_digits] for i in range(length))
  return s == s[::-1]

def solve():
  t = int(input())
  for _ in range(t):
    n = input().strip()
    print("YES" if is_palindrome_series(n) else "NO")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(S) where S is the sum of digits (length of resulting string)
- **Space Complexity:** O(S) for storing the string, or O(D) where D is number of digits for optimized version

##### Example
For N = 61:
- Digits: [6, 1]
- Sum: 6 + 1 = 7
- String: "6161616" (repeating [6,1] for 7 characters)
- As letters: "gbgbgbg"
- Is palindrome? Yes (reads same forwards and backwards)

For N = 12:
- Digits: [1, 2]
- Sum: 1 + 2 = 3
- String: "121"
- Is palindrome? Yes

---

### Polo the Penguin and the XOR

#### Problem Information
- **Source:** Codechef
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Polo, the Penguin, likes the XOR operation.

XOR-sum of a list of numbers is the result of XOR-ing all of them. XOR-sum of (A₁ ⊕ A₂ ⊕ ... ⊕ Aₙ) is defined as A₁ ⊕ (A₂ ⊕ (A₃ ⊕ (... ⊕ Aₙ)))

He has an array A consisting of N integers. Index in the array are numbered from 1 to N, inclusive. Let us denote by F(L, R), the XOR-sum of all integers in the array A whose indices lie from L to R, inclusive, i.e. F(L, R) = A_L ⊕ A_{L+1} ⊕ ... ⊕ A_R.

Your task is to find the total sum of XOR-sums F(L, R) over all L and R, such that 1 ≤ L ≤ R ≤ N.

#### Input Format
- First line: T denoting the number of test cases
- For each test case:
  - First line: N denoting the size of array
  - Second line: N space-separated integers A₁, A₂, ..., Aₙ

#### Constraints
- 1 ≤ T ≤ 100,000
- 1 ≤ N ≤ 100,000
- 0 ≤ Aᵢ ≤ 1,000,000,000 (10⁹)
- The total sum of all N over all test cases will not exceed 100,000

#### Output Format
For each test case, output a single line containing the total sum to the corresponding test case.

#### Solution

##### Approach
For each bit position, count how many subarrays have that bit set in their XOR.

Key insight: Use prefix XOR. Let `P[i] = A[1] ⊕ A[2] ⊕ ... ⊕ A[i]` (with P[0] = 0).
Then `F(L, R) = P[R] ⊕ P[L-1]`.

For a specific bit b:
- F(L,R) has bit b set if P[R] and P[L-1] differ at bit b
- Count pairs where one has bit b set and one doesn't

For each bit position:
- Count of prefix values with bit set: `ones`
- Count with bit unset: `zeros`
- Number of subarrays with bit set = `ones × zeros`
- Contribution to sum = `ones × zeros × 2^b`

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    # Compute prefix XOR
    prefix = [0] * (n + 1)
    for i in range(n):
      prefix[i + 1] = prefix[i] ^ arr[i]

    total_sum = 0

    # For each bit position (up to 30 bits for 10^9)
    for bit in range(30):
      mask = 1 << bit
      ones = 0
      zeros = 0

      # Count prefix values with this bit set/unset
      for i in range(n + 1):
        if prefix[i] & mask:
          ones += 1
        else:
          zeros += 1

      # Number of subarrays with this bit set in XOR
      # = pairs where P[R] and P[L-1] differ at this bit
      count = ones * zeros

      # Add contribution
      total_sum += count * mask

    print(total_sum)

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    total_sum = 0
    prefix_xor = 0

    # For each bit, track count of 0s and 1s in prefix XOR
    bit_count = [[1, 0] for _ in range(30)]  # Initially prefix[0]=0

    for num in arr:
      prefix_xor ^= num

      for bit in range(30):
        mask = 1 << bit
        bit_val = (prefix_xor >> bit) & 1

        # Subarrays ending here with this bit set
        # = count of previous prefixes with opposite bit
        opposite = 1 - bit_val
        count = bit_count[bit][opposite]
        total_sum += count * mask

        # Update count
        bit_count[bit][bit_val] += 1

    print(total_sum)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N × 30) = O(N) per test case
- **Space Complexity:** O(30) = O(1) for bit counts

##### Key Insight
Using prefix XOR, `F(L,R) = P[R] ⊕ P[L-1]`. For each bit position, a subarray contributes `2^bit` to the sum if that bit is set in its XOR. This happens when P[R] and P[L-1] differ at that bit position. The total contribution of bit b is `(count_of_1s × count_of_0s) × 2^b`.

---

### The Sultan's Successors

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

The Sultan of Nubia has no children, so she has decided that the country will be split into up to k separate parts on her death and each part will be inherited by whoever performs best at some test.

To ensure that only highly intelligent people eventually become her successors, the Sultan has devised an ingenious test. In a large hall have been placed k chessboards. Each chessboard has numbers in the range 1 to 99 written on each square and is supplied with 8 jewelled chess queens.

The task facing each potential successor is to place the 8 queens on the chess board in such a way that no queen threatens another one, and so that the numbers on the squares thus selected sum to a number at least as high as one already chosen by the Sultan.

For those unfamiliar with the rules of chess, this implies that each row and column of the board contains exactly one queen, and each diagonal contains no more than one.

#### Input Format
- Input will consist of k (the number of boards), on a line by itself
- Followed by k sets of 64 numbers, each set consisting of eight lines of eight numbers
- Each number will be a positive integer less than 100
- There will never be more than 20 boards

#### Output Format
Output will consist of k numbers consisting of your k scores, each score on a line by itself and right justified in a field 5 characters wide.

#### Solution

##### Approach
This is the classic N-Queens problem with a twist - we need to maximize the sum of values on chosen squares.

Use backtracking:
1. Place queens row by row
2. For each row, try each column
3. Check if the position is safe (no queen in same column or diagonals)
4. Track the maximum sum achievable

##### Python Solution

```python
def solve():
  def is_safe(queens, row, col):
    """Check if placing a queen at (row, col) is safe"""
    for r in range(row):
      c = queens[r]
      # Same column
      if c == col:
        return False
      # Same diagonal
      if abs(r - row) == abs(c - col):
        return False
    return True

  def backtrack(board, queens, row, current_sum, max_sum):
    """Backtrack to find all valid 8-queens placements"""
    if row == 8:
      return max(max_sum[0], current_sum)

    for col in range(8):
      if is_safe(queens, row, col):
        queens[row] = col
        new_sum = current_sum + board[row][col]
        max_sum[0] = max(max_sum[0], backtrack(board, queens, row + 1, new_sum, max_sum))

    return max_sum[0]

  k = int(input())

  for _ in range(k):
    board = []
    for i in range(8):
      row = list(map(int, input().split()))
      board.append(row)

    queens = [-1] * 8  # queens[i] = column of queen in row i
    max_sum = [0]

    result = backtrack(board, queens, 0, 0, max_sum)

    # Right-justify in field of 5 characters
    print(f"{result:5d}")

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  def backtrack(board, row, cols, diag1, diag2, current_sum):
    """
    cols: bitmask of occupied columns
    diag1: bitmask of occupied \ diagonals
    diag2: bitmask of occupied / diagonals
    """
    if row == 8:
      return current_sum

    max_sum = 0
    for col in range(8):
      d1 = row - col + 7  # \ diagonal index (0-14)
      d2 = row + col      # / diagonal index (0-14)

      if not (cols & (1 << col)) and not (diag1 & (1 << d1)) and not (diag2 & (1 << d2)):
        new_sum = backtrack(
          board,
          row + 1,
          cols | (1 << col),
          diag1 | (1 << d1),
          diag2 | (1 << d2),
          current_sum + board[row][col]
        )
        max_sum = max(max_sum, new_sum)

    return max_sum

  k = int(input())

  for _ in range(k):
    board = []
    for i in range(8):
      row = list(map(int, input().split()))
      board.append(row)

    result = backtrack(board, 0, 0, 0, 0, 0)
    print(f"{result:5d}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(8!) = O(40320) per board - the number of valid 8-queens configurations is 92
- **Space Complexity:** O(8) for recursion depth

##### Key Insight
There are only 92 valid ways to place 8 queens on a chessboard. We enumerate all of them and track the maximum sum.

