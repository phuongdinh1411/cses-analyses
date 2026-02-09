---
layout: simple
title: "Backtracking"
permalink: /problem_soulutions/Orange/Backtracking/
---

# Backtracking

Backtracking problems involving systematic exploration of solution spaces through recursive trial and error, pruning invalid paths to find valid solutions.

## Problems

### Digger Octaves

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

#### Problem Statement

After many years spent playing Digger, little Ivan realized he was not taking advantage of the octaves. Digger is a Canadian computer game, originally designed for the IBM personal computer, back in 1983. The aim of the game is to collect precious gold and emeralds buried deep in subterranean levels of an old abandoned mine.

We Digger gurus call a set of eight consecutive emeralds an octave. Notice that, by consecutive we mean that we can collect them one after another. Your Digger Mobile is able to move in the four directions: North, South, West and East.

In a simplified Digger version, consisting only of emeralds and empty spaces, you will have to count how many octaves are present for a given map.

#### Input Format
- Input starts with an integer T, representing the number of test cases (1 <= T <= 20).
- Each test case consists of a map:
  - An integer N (1 <= N <= 8), representing the side length of the square-shaped map.
  - N lines follow, N characters each.
  - 'X' represents an emerald, '.' represents an empty space.

#### Output Format
For each test case print the number of octaves on a single line.

#### Example
```
Input:
2
3
XXX
X.X
XXX
2
XX
XX

Output:
8
0
```
In the first case, the 3x3 grid has 8 emeralds connected in a ring pattern. There are 8 different sets of 8 consecutive emeralds (octaves) that can be collected. In the second case, there are only 4 emeralds, so no octave (8 consecutive emeralds) is possible.

#### Solution

##### Approach
Use DFS/backtracking to find all paths of exactly 8 consecutive emeralds. To avoid counting the same set of emeralds multiple times (via different orderings), we use a set to store unique combinations of 8 cells.

##### Python Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    grid = []
    for i in range(n):
      grid.append(input().strip())

    # Directions: up, down, left, right
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    # Set to store unique octaves (as frozensets of positions)
    octaves = set()

    def dfs(x, y, path, visited):
      if len(path) == 8:
        # Store as frozenset to make it hashable and order-independent
        octaves.add(frozenset(path))
        return

      for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited and grid[nx][ny] == 'X':
          visited.add((nx, ny))
          path.append((nx, ny))
          dfs(nx, ny, path, visited)
          path.pop()
          visited.remove((nx, ny))

    # Start DFS from each emerald
    for i in range(n):
      for j in range(n):
        if grid[i][j] == 'X':
          visited = {(i, j)}
          path = [(i, j)]
          dfs(i, j, path, visited)

    print(len(octaves))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(4^8 * n^2) in worst case, but much less due to pruning
- **Space Complexity:** O(n^2 + number of unique octaves)

---

### Dreamoon and WiFi

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Dreamoon is standing at the position 0 on a number line. Drazil is sending a list of commands through Wi-Fi to Dreamoon's smartphone and Dreamoon follows them.

Each command is one of the following two types:
1. Go 1 unit towards the positive direction, denoted as `+`
2. Go 1 unit towards the negative direction, denoted as `-`

But the Wi-Fi condition is so poor that Dreamoon's smartphone reports some of the commands can't be recognized and Dreamoon knows that some of them might even be wrong though successfully recognized. Dreamoon decides to follow every recognized command and toss a fair coin to decide those unrecognized ones (that means, he moves to 1 unit to the negative or positive direction with the same probability 0.5).

You are given an original list of commands sent by Drazil and list received by Dreamoon. What is the probability that Dreamoon ends in the position originally supposed to be final by Drazil's commands?

#### Example
```
Input:
++-+-
+-+??

Output:
0.500000000000
```
The original commands "++-+-" result in position 0+1+1-1+1-1 = 1. The received commands "+-+??" give a fixed position of +1-1+1 = 1, with 2 unknown commands. To reach target position 1, Dreamoon needs the two '?' to sum to 0 (one '+' and one '-'). There are 4 possible outcomes for two coin tosses (++, +-, -+, --), and 2 of them (+-  and -+) give the desired result. Thus probability = 2/4 = 0.5.

#### Solution

##### Approach
1. Calculate the target position from s1
2. Use backtracking to explore all possible outcomes for '?' characters
3. Count how many outcomes lead to the target position
4. Probability = valid_outcomes / total_outcomes

##### Python Solution

```python
from math import comb

def solve():
  s1 = input().strip()
  s2 = input().strip()

  target = sum(1 if c == '+' else -1 for c in s1)
  fixed = sum(1 if c == '+' else (-1 if c == '-' else 0) for c in s2)
  q = s2.count('?')

  if q == 0:
    print(1.0 if fixed == target else 0.0)
    return

  diff = target - fixed + q
  if diff < 0 or diff % 2 != 0 or diff > 2 * q:
    print(0.0)
    return

  p = diff // 2
  probability = comb(q, p) / (2 ** q)
  print(f"{probability:.12f}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(2^n) for backtracking, O(n) for mathematical solution
- **Space Complexity:** O(n) for recursion stack

---

### Lotto

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

In the German Lotto you have to select 6 numbers from the set {1, 2, ..., 49}. A popular strategy to play Lotto - although it doesn't increase your chance of winning - is to select a subset S containing k (k > 6) of these 49 numbers, and then play several games with choosing numbers only from S.

Your job is to write a program that reads in the number k and the set S and then prints all possible games choosing numbers only from S.

#### Example
```
Input:
7 1 2 3 4 5 6 7
0

Output:
1 2 3 4 5 6
1 2 3 4 5 7
1 2 3 4 6 7
1 2 3 5 6 7
1 2 4 5 6 7
1 3 4 5 6 7
2 3 4 5 6 7
```
With k=7 numbers {1,2,3,4,5,6,7}, we generate all C(7,6)=7 combinations of 6 numbers in lexicographical order. Each line represents one possible Lotto game selection.

#### Solution

##### Approach
Generate all combinations of 6 numbers from the given set using backtracking. Since the input is already sorted, the output will automatically be in lexicographical order.

##### Python Solution

```python
from itertools import combinations

def solve():
  first_case = True

  while True:
    line = input().split()
    k = int(line[0])

    if k == 0:
      break

    numbers = list(map(int, line[1:k+1]))

    if not first_case:
      print()
    first_case = False

    for combo in combinations(numbers, 6):
      print(' '.join(map(str, combo)))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(C(k, 6)) = O(k! / (6! * (k-6)!)) combinations
- **Space Complexity:** O(6) for the current combination

---

### Minimize Absolute Difference

#### Problem Information
- **Source:** TopCoder
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

You are given an array x that contains exactly five positive integers. You want to put four of them instead of the question marks into the following expression: `|(? / ?) - (? / ?)|`. Your goal is to make the value of the expression as small as possible.

#### Example
```
Input:
1 2 3 4 5

Output:
3 1 4 2
```
With array [1, 2, 3, 4, 5] (indices 0-4), choosing indices 3,1,4,2 gives |(4/2) - (5/3)| = |2 - 1.667| = 0.333, which is the minimum possible absolute difference. The output represents the indices of the four chosen numbers in the expression (a/b) - (c/d).

#### Solution

##### Approach
Since we only have 5 numbers and need to choose 4 with specific positions, we can enumerate all permutations. There are P(5,4) = 120 possible arrangements.

##### Python Solution

```python
from itertools import permutations

def solve():
  x = list(map(int, input().split()))

  min_diff = float('inf')
  best_indices = None

  for perm in permutations(range(5), 4):
    a, b, c, d = perm
    diff = abs(x[a] / x[b] - x[c] / x[d])

    if diff < min_diff or (diff == min_diff and list(perm) < list(best_indices)):
      min_diff = diff
      best_indices = perm

  print(' '.join(map(str, best_indices)))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(P(5,4)) = O(120) = O(1) constant
- **Space Complexity:** O(1)

---

### Splitting numbers

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

#### Problem Statement

We define the operation of splitting a binary number n into two numbers a(n), b(n) as follows:
- The indices of the bits of a(n) that are 1 are i1, i3, i5, ... (odd-positioned 1s)
- The indices of the bits of b(n) that are 1 are i2, i4, i6, ... (even-positioned 1s)

#### Example
```
Input:
13
47
0

Output:
9 4
37 10
```
For n=13 (binary 1101), the 1-bits are at positions 0, 2, 3 (counting from right, 0-indexed). The 1st and 3rd 1-bits (positions 0 and 3) go to a, giving 1001 = 9. The 2nd 1-bit (position 2) goes to b, giving 0100 = 4. For n=47 (binary 101111), the 1-bits at odd positions (1st, 3rd, 5th) form a=37, and even positions (2nd, 4th) form b=10.

#### Solution

##### Python Solution

```python
def solve():
  while True:
    n = int(input())
    if n == 0:
      break

    a, b = 0, 0
    count = 0
    bit_pos = 0

    while n:
      if n & 1:
        if count % 2 == 0:
          a |= (1 << bit_pos)
        else:
          b |= (1 << bit_pos)
        count += 1
      n >>= 1
      bit_pos += 1

    print(a, b)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(log n)
- **Space Complexity:** O(1)

---

### The Boggle Game

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

In the PigEwu language, each word has exactly 4 letters and contains exactly 2 vowels (A, E, I, O, U, Y).

In Boggle, you have a 4x4 grid of letters. A word is a sequence of 4 distinct adjacent squares (sharing edge or corner) forming a legal PigEwu word.

Given two Boggle boards, find all PigEwu words common to both boards.

#### Example
```
Input:
AAAA
BBBB
CCCC
DDDD

AAAB
BBBC
CCCD
DDDE

Output:
AAAB
AABB
ABAB
ABBA
ABBB
```
Each board is 4x4. Valid PigEwu words must: (1) be exactly 4 letters, (2) contain exactly 2 vowels, (3) use distinct adjacent squares. The output lists all such words that can be formed on both boards, sorted lexicographically. Words like "AAAB" contain 2 vowels (A, A) and can be traced on both boards using adjacent cells.

#### Solution

##### Python Solution

```python
def solve():
  VOWELS = set('AEIOUY')
  DIRS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

  def count_vowels(word):
    return sum(1 for c in word if c in VOWELS)

  def find_words(board):
    words = set()
    visited = [[False] * 4 for _ in range(4)]

    def dfs(r, c, path):
      if len(path) == 4:
        if count_vowels(path) == 2:
          words.add(path)
        return

      visited[r][c] = True

      for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 4 and 0 <= nc < 4 and not visited[nr][nc]:
          dfs(nr, nc, path + board[nr][nc])

      visited[r][c] = False

    for i in range(4):
      for j in range(4):
        dfs(i, j, board[i][j])

    return words

  # Process boards and find common words
  # ... (implementation continues)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(4 * 4 * 8^3) = O(2048) per board for DFS exploration
- **Space Complexity:** O(W) where W is number of unique words found

---

### The Hamming Distance

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given N (length of bit strings) and H (Hamming distance), print all bit strings of length N that are Hamming distance H from the bit string containing all 0's. That is, all bit strings of length N with exactly H 1's, in ascending lexicographical order.

#### Example
```
Input:
1

4 2

Output:
0011
0101
0110
1001
1010
1100

```
With N=4 and H=2, we need all 4-bit strings with exactly 2 ones (Hamming distance 2 from "0000"). There are C(4,2)=6 such strings, listed in lexicographical order. Each string has exactly 2 bits set to 1.

#### Solution

##### Python Solution

```python
from itertools import combinations

def solve():
  t = int(input())
  input()

  for case in range(t):
    line = input().split()
    n, h = int(line[0]), int(line[1])

    for positions in combinations(range(n), h):
      bits = ['0'] * n
      for pos in positions:
        bits[pos] = '1'
      print(''.join(bits))

    print()

    try:
      if case < t - 1:
        input()
    except:
      pass

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(C(N, H)) to generate all combinations
- **Space Complexity:** O(N) for the current string
