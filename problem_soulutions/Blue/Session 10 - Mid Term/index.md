---
layout: simple
title: "Mid Term"
permalink: /problem_soulutions/Blue/Session 10 - Mid Term/
---

# Mid Term

Mid-term examination problems covering topics from Sessions 01-09 including graph algorithms, data structures, and string processing.

## Problems

### Bombs NO they are Mines

#### Problem Information
- **Source:** Custom
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a grid of R rows and C columns, find the shortest path from a source cell to a destination cell. Some cells contain mines and are blocked.

#### Input Format
- Multiple test cases until R = 0
- First line: R C (rows and columns)
- Next line: number of rows containing mines
- Following lines: row_index, count, and column indices of mines in that row
- Source coordinates (row, col)
- Destination coordinates (row, col)

#### Output Format
Minimum number of steps to reach destination, or -1 if impossible.

#### Solution

##### Approach
Dijkstra's algorithm (BFS would also work since all edges have weight 1). Use priority queue to explore cells in order of distance. Move in 4 directions and avoid cells marked as mines.

##### Python Solution

```python
import heapq

class Node:
  def __init__(self, idx, idy, dist):
    self.dist = dist
    self.idx = idx
    self.idy = idy

  def __lt__(self, other):
    return self.dist < other.dist

def dijkstra(r, c, s, d, matrix):
  dist = [[-1 for x in range(c)] for y in range(r)]
  pqueue = []
  heapq.heappush(pqueue, Node(s[0], s[1], 0))
  dist[s[0]][s[1]] = 0

  dx = [1, 0, -1, 0]
  dy = [0, -1, 0, 1]

  while len(pqueue) > 0:
    top = heapq.heappop(pqueue)
    u = top.idx
    v = top.idy
    w = top.dist
    for ll in range(4):
      neighbor_x = u + dx[ll]
      neighbor_y = v + dy[ll]
      if 0 <= neighbor_x < r and 0 <= neighbor_y < c and matrix[neighbor_x][neighbor_y] == False:
        if w + 1 < dist[neighbor_x][neighbor_y] or dist[neighbor_x][neighbor_y] == -1:
          dist[neighbor_x][neighbor_y] = w + 1
          heapq.heappush(pqueue, Node(neighbor_x, neighbor_y, dist[neighbor_x][neighbor_y]))

  return dist[d[0]][d[1]]

def solution():
  while True:
    R, C = map(int, input().strip().split())
    if R == 0:
      break

    boom_rows = int(input())
    matrix = [[False for i in range(C)] for j in range(R)]

    for i in range(boom_rows):
      booms = list(map(int, input().strip().split()))
      for j in range(2, booms[1] + 2):
        matrix[booms[0]][booms[j]] = True

    s = list(map(int, input().strip().split()))
    d = list(map(int, input().strip().split()))
    print(dijkstra(R, C, s, d, matrix))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(R * C * log(R * C)) for Dijkstra on grid
- **Space Complexity:** O(R * C) for distance matrix and mine grid

---

### Regular Bracket Sequence

#### Problem Information
- **Source:** Codeforces 26B
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a bracket sequence consisting only of '(' and ')' characters, find the length of the longest regular (properly nested) bracket subsequence.

#### Input Format
A single string containing only '(' and ')' characters. Length up to 10^6.

#### Output Format
A single integer: the length of the longest regular bracket subsequence.

#### Solution

##### Approach
Greedy approach using a counter. Track opening brackets with a counter. For each closing bracket, if there's a matching opening bracket, add 2 to total. If no matching opening bracket, skip it.

##### Python Solution

```python
def solution():
  s = input().strip()
  pos = 0
  total = 0
  for c in s:
    if c == '(':
      pos += 1
    else:
      pos -= 1
      if pos >= 0:
        total += 2
      else:
        pos += 1

  print(total)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n) where n is string length
- **Space Complexity:** O(1)

---

### Queries about less or equal elements

#### Problem Information
- **Source:** Codeforces 600B
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given two arrays A and B, for each element b[i] in B, find how many elements in A are less than or equal to b[i].

#### Input Format
- First line: n m (sizes of arrays A and B)
- Second line: n integers (array A)
- Third line: m integers (array B)

#### Output Format
m integers: for each b[i], the count of elements in A that are <= b[i].

#### Solution

##### Approach
Sort array A. For each query b[i], use binary search (bisect_right) to find the position where b[i] would be inserted, which gives the count.

##### Python Solution

```python
import bisect

def solution():
  n, m = map(int, input().strip().split())
  a = list(map(int, input().strip().split()))
  b = list(map(int, input().strip().split()))

  a.sort()

  for i in range(m - 1):
    print(bisect.bisect_right(a, b[i]), end=' ')
  print(bisect.bisect_right(a, b[m - 1]))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n + m log n) for sorting and m queries
- **Space Complexity:** O(n) for sorted array

---

### Find the Median

#### Problem Information
- **Source:** Custom
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given an array of N integers, find the median value. For an array sorted in ascending order, the median is the middle element at index N/2 (0-indexed after sorting).

#### Input Format
- First line: N (number of elements)
- Second line: N space-separated integers

#### Output Format
A single integer: the median of the array.

#### Solution

##### Approach
Sort the array in ascending order and return the element at index N//2.

##### Python Solution

```python
def solution():
  n = int(input())
  ar = list(map(int, input().strip().split()))
  ar.sort()
  mid_index = n//2

  print(ar[mid_index])

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) for sorting
- **Space Complexity:** O(n) for array storage

---

### CamelCase

#### Problem Information
- **Source:** Hackerrank
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a string in camelCase format (first word starts with lowercase, subsequent words start with uppercase), count the number of words.

#### Input Format
A single line containing a camelCase string.

#### Output Format
A single integer: the number of words in the string.

#### Solution

##### Approach
Start with count = 1 (for the first word). Iterate through each character. If character is uppercase (ASCII < 97), increment counter. Each uppercase letter marks the start of a new word.

##### Python Solution

```python
def solution():
  s = input().strip()
  counter = 1
  for c in s:
    if ord(c) < 97:
      counter += 1

  print(counter)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n) where n is string length
- **Space Complexity:** O(1)

---

### Country Roads

#### Problem Information
- **Source:** LightOJ 1002
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 32MB

#### Problem Statement

Given an undirected weighted graph representing cities and roads, find the minimum "maximum edge weight" path from a source city to all other cities. The cost of a path is the maximum edge weight along that path (minimax path problem).

#### Input Format
- T: number of test cases
- For each test case:
  - N M: number of nodes and edges
  - M lines with A B W: edge from A to B with weight W
  - t: the source node

#### Output Format
For each test case: "Case X:" followed by the minimum maximum edge weight to reach each city (0 to N-1), or "Impossible" if unreachable.

#### Solution

##### Approach
Modified Dijkstra's algorithm. Instead of summing weights, track the maximum edge weight on the path. For relaxation: dist[v] = max(dist[u], edge_weight) if this is smaller than current dist[v].

##### Python Solution

```python
import heapq
import sys

class input_tokenizer:
  __tokens = None

  def has_next(self):
    return self.__tokens != [] and self.__tokens != None

  def next(self):
    token = self.__tokens[-1]
    self.__tokens.pop()
    return token

  def __init__(self):
    self.__tokens = sys.stdin.read().split()[::-1]

inp = input_tokenizer()

class Node:
  def __init__(self, id, dist):
    self.dist = dist
    self.id = id

  def __lt__(self, other):
    return self.dist < other.dist

def dijkstra(n, t, graph):
  dist = [-1 for x in range(n+1)]
  pqueue = []
  heapq.heappush(pqueue, Node(t, 0))
  dist[t] = 0

  while len(pqueue) > 0:
    top = heapq.heappop(pqueue)
    u = top.id
    w = top.dist
    for neighbor in graph[u]:
      if (neighbor.dist < dist[neighbor.id] and dist[u] < dist[neighbor.id]) or dist[neighbor.id] == -1:
        dist[neighbor.id] = max(neighbor.dist, dist[u])
        heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))

  return dist

def solution():
  T = int(inp.next())
  case_number = 0

  for i in range(T):
    case_number += 1
    N = int(inp.next())
    M = int(inp.next())
    graph = [[] for x in range(N + 1)]
    for j in range(M):
      A = int(inp.next())
      B = int(inp.next())
      W = int(inp.next())

      graph[B].append(Node(A, W))
      graph[A].append(Node(B, W))

    t = int(inp.next())

    print('Case ' + str(case_number) + ':')
    dist = dijkstra(N, t, graph)
    for d in dist:
      if d > -1:
        print(d)
      else:
        print('Impossible')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O((N + M) log N) for modified Dijkstra
- **Space Complexity:** O(N + M) for graph and distance arrays

---

### Pangram

#### Problem Information
- **Source:** Custom
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

A pangram is a sentence that contains every letter of the alphabet at least once. Given a string, determine if it is a pangram.

#### Input Format
- First line: N (length of the string)
- Second line: a string of N characters

#### Output Format
"YES" if the string is a pangram, "NO" otherwise.

#### Solution

##### Approach
Use a boolean array of size 26 to track presence of each letter. Convert each character to index (0-25) regardless of case. Mark the corresponding index as True. If all 26 positions are True, it's a pangram.

##### Python Solution

```python
def solution():
  num_of_chars = int(input())
  checking_string = input().strip()

  checking_array = [False for i in range(26)]

  for i in range(num_of_chars):
    char_index = ord(checking_string[i]) - 65
    if char_index >= 26:
      char_index = ord(checking_string[i]) - 97

    checking_array[char_index] = True

  for i in range(26):
    if not checking_array[i]:
      print('NO')
      return
  print('YES')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n) where n is string length
- **Space Complexity:** O(1) for fixed-size array of 26

---

### Printer Queue

#### Problem Information
- **Source:** UVA 12100
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

A printer queue processes jobs based on priority, not just FIFO order. Jobs with higher priority are printed first. If the front job doesn't have the highest priority, it's moved to the back of the queue. Find when a specific job (at position m) will be printed.

#### Input Format
- T: number of test cases
- For each test case:
  - n m: number of jobs and position of our job (0-indexed)
  - n integers: priorities of each job

#### Output Format
For each test case: the order in which our job is printed (1-indexed).

#### Solution

##### Approach
Simulate the printer queue. Sort priorities in descending order to know which priority should print next. If front job has the current highest priority, print it; otherwise move to back. Track when our target job gets printed.

##### Python Solution

```python
def solution():
  tcs = int(input())
  for i in range(tcs):
    n, m = map(int, input().split())
    printer_queue = list(map(int, input().split()))
    sorted_list = sorted(printer_queue, reverse=True)
    counter = 0
    pointer = 0
    largest_pos = 0
    while True:
      if largest_pos >= n:
        break

      if printer_queue[pointer] == sorted_list[largest_pos]:
        counter += 1
        largest_pos += 1
        if pointer == m:
          break
      else:
        if pointer == m:
          m = len(printer_queue)
        printer_queue.append(printer_queue[pointer])

      pointer += 1

    print(counter)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n^2) worst case for queue simulation
- **Space Complexity:** O(n) for queue and sorted list

---

### Soldier and Bananas

#### Problem Information
- **Source:** Codeforces 546A
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

A soldier wants to buy w bananas. The cost of bananas is progressive: the 1st banana costs k dollars, 2nd costs 2*k, 3rd costs 3*k, and so on. The soldier has n dollars. How much more money does he need to borrow?

#### Input Format
Single line with three integers: k n w
- k: base cost of first banana
- n: dollars the soldier has
- w: number of bananas to buy

#### Output Format
Single integer: amount to borrow (0 if soldier has enough).

#### Solution

##### Approach
Total cost = k * (1 + 2 + ... + w) = k * w * (w + 1) / 2. Amount to borrow = max(0, total_cost - n).

##### Python Solution

```python
def solution():
  k, n, w = map(int, input().strip().split())

  result = int((w + 1) * w * k / 2 - n)
  if result < 0:
    result = 0

  print(result)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(1)
- **Space Complexity:** O(1)

---

### Word Transformation

#### Problem Information
- **Source:** UVA 429
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a dictionary of words and pairs of words, find the minimum number of single-character transformations needed to change one word into another. A valid transformation changes exactly one character while keeping the resulting word in the dictionary.

#### Input Format
- N: number of test cases
- For each test case:
  - Dictionary words (one per line) until '*'
  - Query pairs (start_word end_word) until blank line

#### Output Format
For each query: start_word end_word min_transformations.

#### Solution

##### Approach
Build a graph where nodes are dictionary words. Connect two words with an edge if they differ by exactly one character. Use Dijkstra's algorithm (or BFS) to find shortest path between query words.

##### Python Solution

```python
import heapq

class Node:
  def __init__(self, id, dist):
    self.dist = dist
    self.id = id

  def __lt__(self, other):
    return self.dist < other.dist

def dijkstra(n, S, T, graph):
  dist = [-1 for x in range(n+1)]
  pqueue = []
  heapq.heappush(pqueue, Node(S, 0))
  dist[S] = 0

  while len(pqueue) > 0:
    top = heapq.heappop(pqueue)
    u = top.id
    w = top.dist
    for neighbor in graph[u]:
      if w + neighbor.dist < dist[neighbor.id] or dist[neighbor.id] == -1:
        dist[neighbor.id] = w + neighbor.dist
        heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))

  return dist[T]

def solution():
  N = int(input().strip())
  for tc in range(N):
    dictionary = []
    while True:
      new_word = input().strip()
      if not new_word:
        continue
      if new_word == '*':
        break
      dictionary.append(new_word)

    queries = []
    while True:
      try:
        new_query = input().strip()
      except Exception as e:
        break
      if not new_query:
        break
      queries.append(list(map(str, new_query.split())))

    n_words = len(dictionary)
    n_queries = len(queries)
    graph = [[] for i in range(n_words)]
    for i in range(n_words):
      for j in range(i, n_words):
        if len(dictionary[i]) == len(dictionary[j]):
          diff = 0
          w_length = len(dictionary[i])
          for c in range(w_length):
            if dictionary[i][c] is not dictionary[j][c]:
              diff += 1
            if diff > 1:
              break

          if diff == 1:
            graph[i].append(Node(j, 1))
            graph[j].append(Node(i, 1))

    for q in range(n_queries):
      start = -1
      end = -1
      for w in range(n_words):
        if start >= 0 and end >= 0:
          break
        if queries[q][0] == dictionary[w]:
          start = w
        if queries[q][1] == dictionary[w]:
          end = w

      print(queries[q][0], queries[q][1], dijkstra(n_words, start, end, graph), sep=' ')
    if tc < N - 1:
      print()

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(W^2 * L + Q * (W + E) log W) where W is word count, L is max word length, Q is queries
- **Space Complexity:** O(W^2) for graph edges in worst case
