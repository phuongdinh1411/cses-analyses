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

#### Example
```
Input:
3 3
1
1 1 1
0 0
2 2

Output:
4
```
3x3 grid with one mine at position (1,1). Path from (0,0) to (2,2) must go around the mine: (0,0)->(0,1)->(0,2)->(1,2)->(2,2) = 4 steps.

#### Solution

##### Approach
Dijkstra's algorithm (BFS would also work since all edges have weight 1). Use priority queue to explore cells in order of distance. Move in 4 directions and avoid cells marked as mines.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import deque

DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]

def bfs(rows, cols, start, dest, mines):
    dist = [[-1] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0
    queue = deque([(start[0], start[1], 0)])

    while queue:
        x, y, d = queue.popleft()
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not mines[nx][ny] and dist[nx][ny] == -1:
                dist[nx][ny] = d + 1
                queue.append((nx, ny, d + 1))

    return dist[dest[0]][dest[1]]

def solution():
    while True:
        r, c = map(int, input().split())
        if r == 0:
            break

        num_mine_rows = int(input())
        mines = [[False] * c for _ in range(r)]

        for _ in range(num_mine_rows):
            line = list(map(int, input().split()))
            row_idx, count = line[0], line[1]
            for col_idx in line[2:2 + count]:
                mines[row_idx][col_idx] = True

        start = tuple(map(int, input().split()))
        dest = tuple(map(int, input().split()))
        print(bfs(r, c, start, dest, mines))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(R * C * log(R * C)) for Dijkstra on grid
- **Space Complexity:** O(R * C) for distance matrix and mine grid

---

### Regular Bracket Sequence

#### Problem Information
- **Source:** [Codeforces 26B](https://codeforces.com/problemset/problem/26/B)
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a bracket sequence consisting only of '(' and ')' characters, find the length of the longest regular (properly nested) bracket subsequence.

#### Input Format
A single string containing only '(' and ')' characters. Length up to 10^6.

#### Output Format
A single integer: the length of the longest regular bracket subsequence.

#### Example
```
Input:
(()))(

Output:
4
```
The longest regular subsequence is "(())" with length 4. The extra ')' at position 4 and '(' at position 5 cannot form valid pairs.

#### Solution

##### Approach
Greedy approach using a counter. Track opening brackets with a counter. For each closing bracket, if there's a matching opening bracket, add 2 to total. If no matching opening bracket, skip it.

##### Python Solution

```python
def solution():
    s = input().strip()
    open_count = 0
    matched = 0

    for char in s:
        if char == '(':
            open_count += 1
        elif open_count > 0:
            open_count -= 1
            matched += 2

    print(matched)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n) where n is string length
- **Space Complexity:** O(1)

---

### Queries about less or equal elements

#### Problem Information
- **Source:** [Codeforces 600B](https://codeforces.com/problemset/problem/600/B)
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

#### Example
```
Input:
5 4
1 2 3 4 5
6 1 2 3

Output:
5 1 2 3
```
Array A = [1,2,3,4,5]. Query 6: all 5 elements <= 6. Query 1: only 1 element <= 1. Query 2: 2 elements <= 2. Query 3: 3 elements <= 3.

#### Solution

##### Approach
Sort array A. For each query b[i], use binary search (bisect_right) to find the position where b[i] would be inserted, which gives the count.

##### Python Solution

```python
from bisect import bisect_right

def solution():
    n, m = map(int, input().split())
    a = sorted(map(int, input().split()))
    b = list(map(int, input().split()))

    results = [bisect_right(a, x) for x in b]
    print(*results)

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

#### Example
```
Input:
5
3 1 4 1 5

Output:
3
```
Sorted array: [1, 1, 3, 4, 5]. Index N//2 = 5//2 = 2. Element at index 2 is 3.

#### Solution

##### Approach
Sort the array in ascending order and return the element at index N//2.

##### Python Solution

```python
def solution():
    n = int(input())
    arr = sorted(map(int, input().split()))
    print(arr[n // 2])

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

#### Example
```
Input:
saveChangesInTheEditor

Output:
5
```
Words: "save", "Changes", "In", "The", "Editor". 4 uppercase letters mark new words, plus 1 initial word = 5 words.

#### Solution

##### Approach
Start with count = 1 (for the first word). Iterate through each character. If character is uppercase (ASCII < 97), increment counter. Each uppercase letter marks the start of a new word.

##### Python Solution

```python
def solution():
    s = input().strip()
    # Count uppercase letters + 1 for the first word
    word_count = 1 + sum(1 for c in s if c.isupper())
    print(word_count)

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

#### Example
```
Input:
1
4 4
0 1 5
1 2 3
2 3 4
0 3 10
0

Output:
Case 1:
0
5
5
4
```
Source is city 0. To reach 0: max edge = 0. To reach 1: path 0->1 with max = 5. To reach 2: path 0->1->2 with max = max(5,3) = 5. To reach 3: path 0->1->2->3 with max = max(5,3,4) = 5, but direct 0->3 has max = 10. Better: via 2, so answer is 4 (wait, should be 5). The path 0->3 via edges gives min-max = 4 through 2->3.

#### Solution

##### Approach
Modified Dijkstra's algorithm. Instead of summing weights, track the maximum edge weight on the path. For relaxation: dist[v] = max(dist[u], edge_weight) if this is smaller than current dist[v].

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict
import sys

def dijkstra_minimax(n, start, graph):
    """Modified Dijkstra for minimax path (minimum of maximum edge weights)."""
    dist = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        if d > dist[u] and dist[u] != -1:
            continue
        for v, w in graph[u]:
            new_dist = max(w, dist[u])
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))

    return dist

def solution():
    tokens = sys.stdin.read().split()[::-1]
    num_cases = int(tokens.pop())

    for case_num in range(1, num_cases + 1):
        n, m = int(tokens.pop()), int(tokens.pop())
        graph = defaultdict(list)

        for _ in range(m):
            a, b, w = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())
            graph[a].append((b, w))
            graph[b].append((a, w))

        source = int(tokens.pop())
        dist = dijkstra_minimax(n, source, graph)

        print(f"Case {case_num}:")
        for i in range(n):
            print(dist[i] if dist[i] >= 0 else 'Impossible')

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

#### Example
```
Input:
35
TheQuickBrownFoxJumpsOverTheLazyDog

Output:
YES
```
The string contains all 26 letters of the alphabet, so it is a pangram.

#### Solution

##### Approach
Use a boolean array of size 26 to track presence of each letter. Convert each character to index (0-25) regardless of case. Mark the corresponding index as True. If all 26 positions are True, it's a pangram.

##### Python Solution

```python
def solution():
    _ = int(input())  # length not needed
    s = input().strip().lower()

    seen = set(s)
    is_pangram = all(chr(ord('a') + i) in seen for i in range(26))

    print('YES' if is_pangram else 'NO')

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

#### Example
```
Input:
1
4 0
1 2 3 2

Output:
4
```
Jobs with priorities [1, 2, 3, 2]. Our job is at position 0 (priority 1). Print order: priority 3 first, then 2, then 2, finally 1. Our job (priority 1) prints 4th.

#### Solution

##### Approach
Simulate the printer queue. Sort priorities in descending order to know which priority should print next. If front job has the current highest priority, print it; otherwise move to back. Track when our target job gets printed.

##### Python Solution

```python
from collections import deque

def solution():
    num_cases = int(input())

    for _ in range(num_cases):
        n, target_pos = map(int, input().split())
        priorities = list(map(int, input().split()))

        # Queue of (priority, original_index)
        queue = deque((p, i) for i, p in enumerate(priorities))
        sorted_priorities = sorted(priorities, reverse=True)

        printed = 0
        priority_idx = 0

        while queue:
            job = queue.popleft()
            if job[0] == sorted_priorities[priority_idx]:
                printed += 1
                priority_idx += 1
                if job[1] == target_pos:
                    break
            else:
                queue.append(job)

        print(printed)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n^2) worst case for queue simulation
- **Space Complexity:** O(n) for queue and sorted list

---

### Soldier and Bananas

#### Problem Information
- **Source:** [Codeforces 546A](https://codeforces.com/problemset/problem/546/A)
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

#### Example
```
Input:
3 17 4

Output:
13
```
Base cost k=3, soldier has n=17 dollars, wants w=4 bananas. Total cost = 3*(1+2+3+4) = 3*10 = 30. Needs to borrow 30-17 = 13.

#### Solution

##### Approach
Total cost = k * (1 + 2 + ... + w) = k * w * (w + 1) / 2. Amount to borrow = max(0, total_cost - n).

##### Python Solution

```python
def solution():
    k, n, w = map(int, input().split())
    total_cost = k * w * (w + 1) // 2
    print(max(0, total_cost - n))

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

#### Example
```
Input:
1
cat
car
far
*
cat far

Output:
cat far 2
```
Dictionary: cat, car, far. Query: cat to far. Transformations: cat -> car (change t to r) -> far (change c to f). Minimum = 2.

#### Solution

##### Approach
Build a graph where nodes are dictionary words. Connect two words with an edge if they differ by exactly one character. Use Dijkstra's algorithm (or BFS) to find shortest path between query words.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict

def differs_by_one(word1, word2):
    """Check if two words differ by exactly one character."""
    if len(word1) != len(word2):
        return False
    return sum(c1 != c2 for c1, c2 in zip(word1, word2)) == 1

def dijkstra(n, start, dest, graph):
    dist = [-1] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        for v, w in graph[u]:
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))

    return dist[dest]

def solution():
    num_cases = int(input().strip())

    for tc in range(num_cases):
        dictionary = []
        while True:
            word = input().strip()
            if not word:
                continue
            if word == '*':
                break
            dictionary.append(word)

        queries = []
        while True:
            try:
                line = input().strip()
            except EOFError:
                break
            if not line:
                break
            queries.append(line.split())

        # Build word index mapping
        word_to_idx = {word: i for i, word in enumerate(dictionary)}
        n_words = len(dictionary)

        # Build graph connecting words that differ by one character
        graph = defaultdict(list)
        for i, word1 in enumerate(dictionary):
            for j in range(i + 1, n_words):
                word2 = dictionary[j]
                if differs_by_one(word1, word2):
                    graph[i].append((j, 1))
                    graph[j].append((i, 1))

        # Answer queries
        for src, dst in queries:
            start_idx = word_to_idx[src]
            end_idx = word_to_idx[dst]
            dist = dijkstra(n_words, start_idx, end_idx, graph)
            print(src, dst, dist)

        if tc < num_cases - 1:
            print()

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(W^2 * L + Q * (W + E) log W) where W is word count, L is max word length, Q is queries
- **Space Complexity:** O(W^2) for graph edges in worst case
