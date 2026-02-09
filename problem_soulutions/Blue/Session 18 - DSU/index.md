---
layout: simple
title: "DSU"
permalink: /problem_soulutions/Blue/Session 18 - DSU/
---

# DSU

This session covers Disjoint Set Union (DSU) data structure, also known as Union-Find, for efficiently managing connected components.

## Problems

### Cthulhu

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Determine if a given graph represents "Cthulhu" - a connected graph with exactly one cycle (i.e., the number of edges equals the number of vertices and all vertices are connected).

#### Input Format
- First line: n (vertices), m (edges)
- Next m lines: a, b (edge between vertices a and b)

#### Output Format
- "FHTAGN!" if the graph is a Cthulhu
- "NO" otherwise

#### Example
```
Input:
6 6
1 2
2 3
3 1
4 5
5 6
6 4

Output:
NO
```
There are 6 vertices and 6 edges, but the graph has 2 connected components (triangle 1-2-3 and triangle 4-5-6). Cthulhu requires a single connected component.

#### Solution

##### Approach
A graph is Cthulhu iff: n == m AND all vertices are in one component. Use Disjoint Set Union (DSU) to check connectivity. If n != m, immediately return NO. Check if all vertices have the same parent (single component).

##### Python Solution

```python
class DSU:
  def __init__(self, n):
    self.parent = list(range(n + 1))
    self.rank = [0] * (n + 1)

  def find(self, u):
    if self.parent[u] != u:
      self.parent[u] = self.find(self.parent[u])  # Path compression
    return self.parent[u]

  def union(self, u, v):
    pu, pv = self.find(u), self.find(v)
    if pu == pv:
      return
    # Union by rank
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1


def solution():
  n, m = map(int, input().split())
  if n != m:
    print('NO')
    return

  dsu = DSU(n)
  for _ in range(m):
    a, b = map(int, input().split())
    dsu.union(a, b)

  # Check if all vertices are in one component
  root = dsu.find(1)
  if all(dsu.find(i) == root for i in range(1, n + 1)):
    print('FHTAGN!')
  else:
    print('NO')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * alpha(n)) where alpha is inverse Ackermann function
- **Space Complexity:** O(n)

---

### Ice Skating

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Bajtek wants to visit all snow drifts in a field. He can move from one drift to another if they share the same x-coordinate OR y-coordinate. Find the minimum number of extra paths (not along same x or y) needed to connect all drifts.

#### Input Format
- First line: n (number of snow drifts)
- Next n lines: x, y (coordinates of each drift)

#### Output Format
Minimum number of extra paths needed (= number of connected components - 1).

#### Example
```
Input:
4
0 0
1 0
0 1
2 2

Output:
1
```
Drifts at (0,0), (1,0), (0,1) share x=0 or y=0, forming one component. Drift (2,2) is isolated. Answer = 2 components - 1 = 1.

#### Solution

##### Approach
Use DSU to group drifts that share x or y coordinates. Count the number of distinct connected components. Answer is (number of components - 1).

##### Python Solution

```python
class DSU:
  def __init__(self, n):
    self.parent = list(range(n))
    self.rank = [0] * n

  def find(self, u):
    if self.parent[u] != u:
      self.parent[u] = self.find(self.parent[u])
    return self.parent[u]

  def union(self, u, v):
    pu, pv = self.find(u), self.find(v)
    if pu == pv:
      return
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1


def solution():
  n = int(input())
  drifts = [tuple(map(int, input().split())) for _ in range(n)]

  dsu = DSU(n)
  for i in range(n):
    for j in range(i + 1, n):
      if drifts[i][0] == drifts[j][0] or drifts[i][1] == drifts[j][1]:
        dsu.union(i, j)

  # Count unique components
  components = len({dsu.find(i) for i in range(n)})
  print(components - 1)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n^2 * alpha(n))
- **Space Complexity:** O(n)

---

### Two Sets

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given n integers and two values a and b, partition the integers into two sets A and B such that:
- For every x in set A, (a - x) must also be in set A
- For every x in set B, (b - x) must also be in set B

Determine if such a partition is possible.

#### Input Format
- First line: n, a, b
- Second line: n distinct integers

#### Output Format
- "YES" followed by n lines (0 for set B, 1 for set A), or "NO"

#### Example
```
Input:
4 5 9
2 3 4 5

Output:
YES
1
1
0
0
```
a=5, b=9. Set A: {2,3} because 2+3=5. Set B: {4,5} because 4+5=9.

#### Solution

##### Approach
Use DSU to create constraints between numbers. If x exists but (a-x) doesn't, x must go to set B (union with B marker). If x exists but (b-x) doesn't, x must go to set A (union with A marker). If both exist, union x with both complements. Check if A and B markers end up in same set (impossible).

##### Python Solution

```python
class DSU:
  def __init__(self, n):
    self.parent = list(range(n))
    self.rank = [0] * n

  def find(self, u):
    if self.parent[u] != u:
      self.parent[u] = self.find(self.parent[u])
    return self.parent[u]

  def union(self, u, v):
    pu, pv = self.find(u), self.find(v)
    if pu == pv:
      return
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1


def solution():
  n, a, b = map(int, input().split())
  numbers = list(map(int, input().split()))
  A, B = n, n + 1  # Markers for set A and set B

  dsu = DSU(n + 2)
  num_to_idx = {num: i for i, num in enumerate(numbers)}

  for i, num in enumerate(numbers):
    # If a-num exists, union with it; else must be in set B
    if a - num in num_to_idx:
      dsu.union(i, num_to_idx[a - num])
    else:
      dsu.union(i, B)

    # If b-num exists, union with it; else must be in set A
    if b - num in num_to_idx:
      dsu.union(i, num_to_idx[b - num])
    else:
      dsu.union(i, A)

  if dsu.find(A) == dsu.find(B):
    print('NO')
    return

  print('YES')
  set_b_root = dsu.find(B)
  for i in range(n):
    print(1 if dsu.find(i) == set_b_root else 0)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * alpha(n))
- **Space Complexity:** O(n)

---

### War

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Track relationships between countries: friends and enemies.
- Friends of friends are friends
- Enemies of enemies are friends

Process operations: setFriends, setEnemies, areFriends, areEnemies. Return -1 if an operation creates a contradiction.

#### Input Format
- n (number of countries)
- Operations until "0 0 0":
  - 1 x y: setFriends(x, y)
  - 2 x y: setEnemies(x, y)
  - 3 x y: areFriends(x, y)?
  - 4 x y: areEnemies(x, y)?

#### Output Format
- For operations 1-2: print -1 if contradiction
- For operations 3-4: print 1 (yes) or 0 (no/unknown)

#### Example
```
Input:
5
1 0 1
2 1 2
3 0 2
4 0 2
1 1 2
0 0 0

Output:
1
1
-1
```
setFriends(0,1), setEnemies(1,2). areFriends(0,2)? 0 and 1 are friends, 1 and 2 are enemies, so 0 and 2 are enemies (answer: 1). areEnemies(0,2)? Yes (answer: 1). setFriends(1,2)? Contradicts existing enemy relation (answer: -1).

#### Solution

##### Approach
Use DSU with 2n elements: i for country, i+n for "enemy of country i". setFriends: union(x, y) and union(x+n, y+n). setEnemies: union(x, y+n) and union(y, x+n). Check contradictions before operations.

##### Python Solution

```python
class DSU:
  def __init__(self, n):
    self.parent = list(range(n))
    self.rank = [0] * n

  def find(self, u):
    if self.parent[u] != u:
      self.parent[u] = self.find(self.parent[u])
    return self.parent[u]

  def union(self, u, v):
    pu, pv = self.find(u), self.find(v)
    if pu == pv:
      return
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1

  def same(self, u, v):
    return self.find(u) == self.find(v)


def solution():
  n = int(input())
  dsu = DSU(2 * n)  # i = country, i+n = enemy of country

  while True:
    c, x, y = map(int, input().split())
    if c == 0:
      break

    if c == 1:  # setFriends
      if dsu.same(x, y + n) or dsu.same(y, x + n):
        print(-1)
      else:
        dsu.union(x, y)
        dsu.union(x + n, y + n)

    elif c == 2:  # setEnemies
      if dsu.same(x, y) or dsu.same(x + n, y + n):
        print(-1)
      else:
        dsu.union(x, y + n)
        dsu.union(y, x + n)

    elif c == 3:  # areFriends
      print(1 if dsu.same(x, y) or dsu.same(x + n, y + n) else 0)

    elif c == 4:  # areEnemies
      print(1 if dsu.same(x, y + n) or dsu.same(y, x + n) else 0)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(Q * alpha(n)) where Q is number of operations
- **Space Complexity:** O(n)

---

### Forests

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

In a meeting with P people and T topics, each person raises their hand for topics they support. Group people who have identical opinions (same set of supported topics). Count the number of distinct opinion groups.

#### Input Format
- T (test cases)
- For each test case:
  - P (people), T (topics)
  - Lines of "person topic" pairs (person supports topic)

#### Output Format
For each test case: number of distinct opinion groups.

#### Example
```
Input:
1

3 4
1 1
1 2
2 2
3 1
3 2

Output:
2
```
Person 1 supports topics {1,2}, Person 2 supports {2}, Person 3 supports {1,2}. Persons 1 and 3 have identical opinions, so 2 groups.

#### Solution

##### Approach
Create a 2D array tracking which person supports which topic. Use DSU to group people with identical opinion vectors. Compare opinion arrays and union people with same opinions. Count distinct groups (unique parents).

##### Python Solution

```python
class DSU:
  def __init__(self, n):
    self.parent = list(range(n + 1))
    self.rank = [0] * (n + 1)

  def find(self, u):
    if self.parent[u] != u:
      self.parent[u] = self.find(self.parent[u])
    return self.parent[u]

  def union(self, u, v):
    pu, pv = self.find(u), self.find(v)
    if pu == pv:
      return
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1


def solution():
  TC = int(input())
  input()

  for t in range(TC):
    P, T = map(int, input().split())
    opinions = [set() for _ in range(P + 1)]  # Use sets for efficiency

    while True:
      try:
        line = input()
        if not line:
          break
        p, topic = map(int, line.split())
        opinions[p].add(topic)
      except:
        break

    dsu = DSU(P)

    for i in range(1, P):
      for j in range(i + 1, P + 1):
        if opinions[i] == opinions[j]:
          dsu.union(i, j)

    # Count distinct groups
    groups = len({dsu.find(i) for i in range(1, P + 1)})
    print(groups)
    if t != TC - 1:
      print()


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(P^2 * T) for comparing opinions + O(P * alpha(P)) for DSU
- **Space Complexity:** O(P * T)

---

### Friends

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

In a town with N citizens and M friendship relations, find the size of the largest group of friends. A group is defined as people connected directly or indirectly through friendships.

#### Input Format
- T (test cases)
- For each test case:
  - N (citizens), M (friendships)
  - M lines: u, v (u and v are friends)

#### Output Format
For each test case: size of the largest friend group.

#### Example
```
Input:
1
5 4
1 2
3 4
2 3
4 5

Output:
5
```
Friendships connect: 1-2, 3-4, 2-3, 4-5. All 5 people are connected through the chain. Largest group = 5.

#### Solution

##### Approach
Use DSU with size tracking. When unioning two groups, combine their sizes. Track and return the maximum group size seen.

##### Python Solution

```python
class DSU:
  def __init__(self, n):
    self.parent = list(range(n + 1))
    self.rank = [0] * (n + 1)
    self.size = [1] * (n + 1)

  def find(self, u):
    if self.parent[u] != u:
      self.parent[u] = self.find(self.parent[u])
    return self.parent[u]

  def union(self, u, v):
    """Union two sets and return the size of the resulting set."""
    pu, pv = self.find(u), self.find(v)
    if pu == pv:
      return self.size[pu]

    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    self.size[pu] += self.size[pv]
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1

    return self.size[pu]


def solution():
  T = int(input())
  for _ in range(T):
    N, M = map(int, input().split())
    dsu = DSU(N)
    max_size = 1

    for _ in range(M):
      u, v = map(int, input().split())
      max_size = max(max_size, dsu.union(u, v))

    print(max_size)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(M * alpha(N))
- **Space Complexity:** O(N)

---

### Virtual Friends

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

A social network tracks friendships. When two people become friends, their friend networks merge. After each friendship, output the total size of the merged network.

#### Input Format
- T (test cases)
- For each test case:
  - F (number of friendships)
  - F lines: name1 name2 (these two become friends)

#### Output Format
After each friendship: size of the resulting friend network.

#### Example
```
Input:
1
3
Fred Barney
Barney Betty
Betty Wilma

Output:
2
3
4
```
Fred-Barney: network size 2. Barney-Betty: Betty joins Fred-Barney network, size 3. Betty-Wilma: Wilma joins, size 4.

#### Solution

##### Approach
Use DSU with string keys (names) stored in dictionary. Track member count for each group's root. When unioning, combine member counts. Print merged group size after each union.

##### Python Solution

```python
from collections import defaultdict


class DSU:
  def __init__(self):
    self.parent = {}
    self.rank = defaultdict(int)
    self.size = defaultdict(lambda: 1)

  def find(self, u):
    if u not in self.parent:
      self.parent[u] = u
    if self.parent[u] != u:
      self.parent[u] = self.find(self.parent[u])
    return self.parent[u]

  def union(self, u, v):
    pu, pv = self.find(u), self.find(v)
    if pu == pv:
      return self.size[pu]

    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    self.size[pu] += self.size[pv]
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1

    return self.size[pu]


def solution():
  T = int(input())
  for _ in range(T):
    F = int(input())
    dsu = DSU()

    for _ in range(F):
      u, v = input().split()
      print(dsu.union(u, v))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(F * alpha(F))
- **Space Complexity:** O(F)

---

### Graph Connectivity

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a graph where nodes are labeled with uppercase letters and edges connect pairs of nodes, count the number of connected components.

#### Input Format
- T (test cases)
- For each test case:
  - Highest node letter (e.g., 'D' means nodes A, B, C, D exist)
  - Edge pairs (two letters per line, e.g., "AB" means A-B edge)
  - Blank line separates test cases

#### Output Format
For each test case: number of connected components.

#### Example
```
Input:
1

D
AB
BC

Output:
2
```
Nodes A, B, C, D exist. Edges: A-B, B-C form one component {A,B,C}. Node D is isolated. Total = 2 components.

#### Solution

##### Approach
Use DSU to track connected components. Convert letters to indices (A=0, B=1, etc.). Union nodes for each edge. Count distinct root parents.

##### Python Solution

```python
class DSU:
  def __init__(self, n):
    self.parent = list(range(n))
    self.rank = [0] * n

  def find(self, u):
    if self.parent[u] != u:
      self.parent[u] = self.find(self.parent[u])
    return self.parent[u]

  def union(self, u, v):
    pu, pv = self.find(u), self.find(v)
    if pu == pv:
      return
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1


def solution():
  T = int(input())
  input()

  for t in range(T):
    n_nodes = ord(input()) - ord('A') + 1
    dsu = DSU(n_nodes)

    while True:
      try:
        line = input()
        if not line:
          break
        u, v = ord(line[0]) - ord('A'), ord(line[1]) - ord('A')
        dsu.union(u, v)
      except:
        break

    components = len({dsu.find(i) for i in range(n_nodes)})
    print(components)
    if t != T - 1:
      print()


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E * alpha(V))
- **Space Complexity:** O(V)
