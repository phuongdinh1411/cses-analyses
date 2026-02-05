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

#### Solution

##### Approach
A graph is Cthulhu iff: n == m AND all vertices are in one component. Use Disjoint Set Union (DSU) to check connectivity. If n != m, immediately return NO. Check if all vertices have the same parent (single component).

##### Python Solution

```python
parent = dict()
ranks = dict()


def make_set(N):
  global parent, ranks
  parent = [i for i in range(N + 5)]
  ranks = [0 for i in range(N + 5)]


def find_set(u):
  if parent[u] != u:
    parent[u] = find_set(parent[u])
  return parent[u]


def union_set(u, v):
  up = find_set(u)
  vp = find_set(v)

  if up == vp:
    return
  if ranks[up] > ranks[vp]:
    parent[vp] = up
  elif ranks[up] < ranks[vp]:
    parent[up] = vp
  else:
    parent[up] = vp
    ranks[vp] += 1


def solution():
  m, n = map(int, input().split())
  if m != n:
    print('NO')
    return

  make_set(m)
  for i in range(m):
    a, b = map(int, input().split())
    union_set(a, b)

  top_parent = find_set(1)
  for i in range(2, m):
    if find_set(i) != top_parent:
      print('NO')
      return

  print('FHTAGN!')


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

#### Solution

##### Approach
Use DSU to group drifts that share x or y coordinates. Count the number of distinct connected components. Answer is (number of components - 1).

##### Python Solution

```python
parent = dict()
ranks = dict()


def make_set(N):
  global parent, ranks
  parent = [i for i in range(N + 5)]
  ranks = [0 for i in range(N + 5)]


def find_set(u):
  if parent[u] != u:
    parent[u] = find_set(parent[u])
  return parent[u]


def union_set(u, v):
  up = find_set(u)
  vp = find_set(v)

  if up == vp:
    return
  if ranks[up] > ranks[vp]:
    parent[vp] = up
  elif ranks[up] < ranks[vp]:
    parent[up] = vp
  else:
    parent[up] = vp
    ranks[vp] += 1


def solution():
  n_drifts = int(input())
  make_set(n_drifts)
  drifts = []
  for i in range(n_drifts):
    x, y = map(int, input().split())
    drifts.append([x, y])

  for i in range(n_drifts - 1):
    for j in range(i + 1, n_drifts):
      if drifts[i][0] == drifts[j][0] or drifts[i][1] == drifts[j][1]:
        union_set(i, j)

  leaders = dict()
  for i in range(n_drifts):
    leader = find_set(i)
    if leaders.get(leader) is not None:
      leaders[leader] += 1
    else:
      leaders[leader] = 1

  print(len(leaders) - 1)


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

#### Solution

##### Approach
Use DSU to create constraints between numbers. If x exists but (a-x) doesn't, x must go to set B (union with B marker). If x exists but (b-x) doesn't, x must go to set A (union with A marker). If both exist, union x with both complements. Check if A and B markers end up in same set (impossible).

##### Python Solution

```python
parent = []
ranks = []


def make_set(N):
  global parent, ranks
  parent = [i for i in range(N + 5)]
  ranks = [0 for i in range(N + 5)]


def find_set(u):
  if parent[u] != u:
    parent[u] = find_set(parent[u])
  else:
    parent[u] = u
  return parent[u]


def union_set(u, v):
  up = find_set(u)
  vp = find_set(v)

  if ranks[up] > ranks[vp]:
    parent[vp] = up
  elif ranks[up] < ranks[vp]:
    parent[up] = vp
  else:
    parent[up] = vp
    ranks[vp] += 1


def solution():
  set_indicators = dict()
  n, a, b = map(int, input().split())
  numbers = list(map(int, input().split()))
  A = n + 1
  B = A + 1

  make_set(n)
  for i in range(n):
    set_indicators[numbers[i]] = i

  for i in range(n):
    if set_indicators.get(a - numbers[i]) is not None:
      union_set(i, set_indicators.get(a - numbers[i]))
    else:
      union_set(i, B)
    if set_indicators.get(b - numbers[i]) is not None:
      union_set(i, set_indicators.get(b - numbers[i]))
    else:
      union_set(i, A)
  if find_set(A) == find_set(B):
    print('NO')
    return

  print('YES')
  for i in range(n):
    print(1 if find_set(i) == find_set(n + 2) else 0)


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

#### Solution

##### Approach
Use DSU with 2n elements: i for country, i+n for "enemy of country i". setFriends: union(x, y) and union(x+n, y+n). setEnemies: union(x, y+n) and union(y, x+n). Check contradictions before operations.

##### Python Solution

```python
parent = []
ranks = []


def make_set(N):
  global parent, ranks
  parent = [i for i in range(2*N + 5)]
  ranks = [0 for i in range(2*N + 5)]


def find_set(u):
  if parent[u] != u:
    parent[u] = find_set(parent[u])
  return parent[u]


def union_set(u, v):
  up = find_set(u)
  vp = find_set(v)

  if up == vp:
    return
  if ranks[up] > ranks[vp]:
    parent[vp] = up
  elif ranks[up] < ranks[vp]:
    parent[up] = vp
  else:
    parent[up] = vp
    ranks[vp] += 1


def solution():
  n = int(input())
  make_set(n)
  while True:
    c, x, y = map(int, input().split())
    if c == 0:
      break
    if c == 1:
      if find_set(x) == find_set(y + n) or find_set(y) == find_set(x + n):
        print(-1)
      else:
        union_set(x, y)
        union_set(x + n, y + n)
    if c == 2:
      if find_set(x) == find_set(y) or find_set(x + n) == find_set(y + n):
        print(-1)
      else:
        union_set(x, y + n)
        union_set(y, x + n)
    if c == 3:
      if find_set(x) == find_set(y) or find_set(x + n) == find_set(y + n):
        print(1)
      else:
        print(0)
    if c == 4:
      if find_set(x) == find_set(y + n) or find_set(y) == find_set(x + n):
        print(1)
      else:
        print(0)


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

#### Solution

##### Approach
Create a 2D array tracking which person supports which topic. Use DSU to group people with identical opinion vectors. Compare opinion arrays and union people with same opinions. Count distinct groups (unique parents).

##### Python Solution

```python
parent = []
ranks = []


def make_set(N):
  global parent, ranks
  parent = [i for i in range(N + 5)]
  ranks = [0 for i in range(N + 5)]


def find_set(u):
  if parent[u] != u:
    parent[u] = find_set(parent[u])
  return parent[u]


def union_set(u, v):
  up = find_set(u)
  vp = find_set(v)

  if up == vp:
    return
  if ranks[up] > ranks[vp]:
    parent[vp] = up
  elif ranks[up] < ranks[vp]:
    parent[up] = vp
  else:
    parent[up] = vp
    ranks[vp] += 1


def has_same_opinion(opinions1, opinions2, length):
  for i in range(length):
    if opinions1[i] != opinions2[i]:
      return False
  return True


def solution():
  TC = int(input())
  input()
  for t in range(TC):
    P, T = map(int, input().split())
    opinions = [[False for i in range(T + 5)] for i in range(P + 5)]

    while True:
      try:
        line = input()
      except:
        break
      if not line:
        break
      try:
        p, t = map(int, line.split())
      except:
        break
      opinions[p][t] = True

    make_set(P)

    for i in range(1, P):
      for j in range(i + 1, P + 1):
        if has_same_opinion(opinions[i], opinions[j], T + 1):
          union_set(i, j)

    opinions_set = dict()

    for i in range(1, P + 1):
      leader = find_set(i)
      if opinions_set.get(leader) is not None:
        opinions_set[leader] += 1
      else:
        opinions_set[leader] = 1

    print(len(opinions_set))
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

#### Solution

##### Approach
Use DSU with size tracking. When unioning two groups, combine their sizes. Track and return the maximum group size seen.

##### Python Solution

```python
parent = []
ranks = []
members = []


def make_set(N):
  global parent, ranks, members
  parent = [i for i in range(N + 5)]
  ranks = [0 for i in range(N + 5)]
  members = [1 for i in range(N + 5)]


def find_set(u):
  if parent[u] != u:
    parent[u] = find_set(parent[u])
  return parent[u]


def union_set(u, v):
  up = find_set(u)
  vp = find_set(v)

  if up == vp:
    return members[vp]
  if ranks[up] > ranks[vp]:
    parent[vp] = up
    members[up] = members[up] + members[vp]
    return members[up]
  elif ranks[up] < ranks[vp]:
    parent[up] = vp
    members[vp] = members[vp] + members[up]
    return members[vp]
  else:
    parent[up] = vp
    ranks[vp] += 1
    members[vp] = members[vp] + members[up]
    return members[vp]


def solution():
  T = int(input())
  for t in range(T):
    N, M = map(int, input().split())

    max_members = 1

    make_set(N)
    for i in range(M):
      u, v = map(int, input().split())
      current_members = union_set(u, v)
      if max_members < current_members:
        max_members = current_members

    print(max_members)


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

#### Solution

##### Approach
Use DSU with string keys (names) stored in dictionary. Track member count for each group's root. When unioning, combine member counts. Print merged group size after each union.

##### Python Solution

```python
parent = dict()
ranks = dict()
members = dict()


def make_set():
  global parent, ranks, members
  parent = dict()
  ranks = dict()
  members = dict()


def find_set(u):
  if parent.get(u) is not None and parent[u] is not u:
    parent[u] = find_set(parent[u])
  else:
    parent[u] = u
  return parent[u]


def union_set(u, v):
  up = find_set(u)
  vp = find_set(v)
  if ranks.get(up) is None:
    ranks[up] = 1
  if ranks.get(vp) is None:
    ranks[vp] = 1
  if members.get(up) is None:
    members[up] = 1
  if members.get(vp) is None:
    members[vp] = 1

  if up == vp:
    return members[vp]

  if ranks[up] > ranks[vp]:
    parent[vp] = up
    members[up] = members[up] + members[vp]
    return members[up]
  elif ranks[up] < ranks[vp]:
    parent[up] = vp
    members[vp] = members[vp] + members[up]
    return members[vp]
  else:
    parent[up] = vp
    ranks[vp] += 1
    members[vp] = members[vp] + members[up]
    return members[vp]


def solution():
  T = int(input())
  for t in range(T):
    F = int(input())

    make_set()
    for i in range(F):
      u, v = map(str, input().split())
      current_members = union_set(u, v)
      print(current_members)


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

#### Solution

##### Approach
Use DSU to track connected components. Convert letters to indices (A=0, B=1, etc.). Union nodes for each edge. Count distinct root parents.

##### Python Solution

```python
parent = dict()
ranks = dict()


def make_set(N):
  global parent, ranks
  parent = [i for i in range(N + 5)]
  ranks = [0 for i in range(N + 5)]


def find_set(u):
  if parent[u] != u:
    parent[u] = find_set(parent[u])
  return parent[u]


def union_set(u, v):
  up = find_set(u)
  vp = find_set(v)

  if up == vp:
    return
  if ranks[up] > ranks[vp]:
    parent[vp] = up
  elif ranks[up] < ranks[vp]:
    parent[up] = vp
  else:
    parent[up] = vp
    ranks[vp] += 1


def solution():
  T = int(input())
  input()
  for t in range(T):
    n_nodes = ord(input()) - 64
    make_set(n_nodes)
    while True:
      try:
        line = input()
        u = ord(line[0]) - 65
        v = ord(line[1]) - 65
        union_set(u, v)
      except:
        break

    leaders = dict()
    for i in range(n_nodes):
      leader = find_set(i)
      if leaders.get(leader) is not None:
        leaders[leader] += 1
      else:
        leaders[leader] = 1

    print(len(leaders))
    if t != T - 1:
      print()


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E * alpha(V))
- **Space Complexity:** O(V)
