---
layout: simple
title: "Kruskal"
permalink: /problem_soulutions/Blue/Session 19 - Kruskal/
---

# Kruskal

This session covers Kruskal's algorithm for finding Minimum Spanning Trees (MST) using edge sorting and Union-Find data structure.

## Problems

### Trail Maintenance

#### Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 32MB

#### Problem Statement

A park has N fields connected by trails. Trails are added one by one. After each trail is added, compute the MST weight. Output -1 if the graph is not yet connected (before N-1 edges are added).

#### Input Format
- T (test cases)
- For each test case:
  - N (fields), M (trails to add)
  - M lines: x, y, z (trail from field x to y with length z)

#### Output Format
After each trail addition: MST weight or -1 if not connected.

#### Example
```
Input:
1
3 4
1 2 5
2 3 3
1 3 4
1 2 2

Output:
Case 1:
-1
-1
7
5
```

#### Solution

##### Approach
Incrementally add edges to the graph. After each addition, run Kruskal's algorithm to find MST. Use DSU for cycle detection in Kruskal's. Return -1 until at least N-1 edges connect all nodes.

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
      return False
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1
    return True


def kruskal(n, edges):
  """Returns MST weight or -1 if not connected."""
  edges.sort(key=lambda e: e[2])  # Sort by weight
  dsu = DSU(n)
  mst_weight = 0
  mst_edges = 0

  for u, v, w in edges:
    if dsu.union(u, v):
      mst_weight += w
      mst_edges += 1
      if mst_edges == n - 1:
        return mst_weight

  return -1


def solution():
  T = int(input())

  for t in range(T):
    N, M = map(int, input().split())
    print(f'Case {t + 1}:')
    edges = []

    for i in range(M):
      x, y, z = map(int, input().split())
      edges.append((x, y, z))
      print(-1 if i < N - 1 else kruskal(N, edges[:]))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(M^2 log M) for repeated Kruskal's
- **Space Complexity:** O(M + N)

---

### Dark Roads

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

A city wants to save electricity by turning off some street lights. They need to keep lights on only for roads in the MST (to maintain connectivity). Calculate how much power can be saved.

#### Input Format
- Multiple test cases until m=n=0
- m (junctions), n (roads)
- n lines: x, y, z (road from x to y with power cost z)

#### Output Format
Total power saved = (sum of all edges) - (MST weight)

#### Example
```
Input:
4 5
0 1 10
0 2 20
1 2 5
1 3 15
2 3 8
0 0

Output:
30
```

#### Solution

##### Approach
Use Kruskal's algorithm to find MST. Sum weights of edges not in MST (edges that form cycles). This gives the total power that can be saved.

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
      return False
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1
    return True


def kruskal_saved(m, edges):
  """Returns total weight of edges NOT in MST (power saved)."""
  edges.sort(key=lambda e: e[2])
  dsu = DSU(m)
  total_weight = sum(e[2] for e in edges)
  mst_weight = 0
  mst_count = 0

  for u, v, w in edges:
    if mst_count == m - 1:
      break
    if dsu.union(u, v):
      mst_weight += w
      mst_count += 1

  return total_weight - mst_weight


def solution():
  while True:
    m, n = map(int, input().split())
    if m == 0:
      break

    edges = [tuple(map(int, input().split())) for _ in range(n)]
    print(kruskal_saved(m, edges))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log E)
- **Space Complexity:** O(E + V)

---

### Expensive Subway

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Calculate the minimum cost to build a subway system connecting all stations. Stations are given as names (strings). If impossible to connect all stations, output "Impossible".

#### Input Format
- Multiple test cases until s=c=0
- s (stations), c (connections)
- s station names
- c lines: station1 station2 cost
- End station name (ignored)

#### Output Format
MST weight or "Impossible" if graph is disconnected.

#### Example
```
Input:
4 4
Central
North
South
East
Central North 10
Central South 15
North East 20
South East 25
Terminal
0 0

Output:
45
```

#### Solution

##### Approach
Map station names to indices using dictionary. Apply Kruskal's algorithm to find MST. Check if MST spans all stations (exactly s-1 edges).

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
      return False
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1
    return True


def kruskal(n, edges):
  edges.sort(key=lambda e: e[2])
  dsu = DSU(n)
  mst_weight = 0
  mst_count = 0

  for u, v, w in edges:
    if dsu.union(u, v):
      mst_weight += w
      mst_count += 1
      if mst_count == n - 1:
        return mst_weight

  return 'Impossible'


def solution():
  while True:
    s, c = map(int, input().split())
    if s == 0:
      break

    stations = {input().strip(): i for i in range(s)}
    edges = []
    for _ in range(c):
      x, y, z = input().split()
      edges.append((stations[x], stations[y], int(z)))

    input()  # Skip terminal station
    print(kruskal(s, edges))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log E)
- **Space Complexity:** O(E + V)

---

### Airports

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Connect N cities using either airports or roads. Each city needs either an airport OR road connection to an airport city. Building an airport costs A, and each road has its own cost. Minimize total cost.

#### Input Format
- T (test cases)
- For each test case:
  - N (cities), M (possible roads), A (airport cost)
  - M lines: x, y, z (road from x to y with cost z)

#### Output Format
"Case #X: cost airports" (total cost and number of airports built)

#### Example
```
Input:
1
4 3 100
1 2 50
2 3 60
3 4 70

Output:
Case #1: 210 1
```

#### Solution

##### Approach
Modified Kruskal's algorithm. Only add edge to MST if its cost < airport cost A. Cities not connected by cheap roads get airports. Count components (each needs one airport).

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
      return False
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1
    return True


def kruskal_with_airports(n, edges, airport_cost):
  edges.sort(key=lambda e: e[2])
  dsu = DSU(n)
  road_cost = 0
  n_airports = n  # Start with each city needing an airport

  for u, v, w in edges:
    if dsu.union(u, v) and w < airport_cost:
      road_cost += w
      n_airports -= 1  # Two cities share one airport via road

  return road_cost + n_airports * airport_cost, n_airports


def solution():
  T = int(input())

  for t in range(T):
    N, M, A = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(M)]
    cost, n_airports = kruskal_with_airports(N, edges, A)
    print(f'Case #{t + 1}: {cost} {n_airports}')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log E)
- **Space Complexity:** O(E + V)

---

### Driving Range

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Find the minimum driving range needed for an electric car to travel between any two cities. The car must be able to travel the longest edge in the MST (the bottleneck edge).

#### Input Format
- Multiple test cases until N=M=0
- N (cities), M (roads)
- M lines: x, y, z (road from x to y with distance z)

#### Output Format
- Minimum driving range (maximum edge weight in MST)
- "IMPOSSIBLE" if cities are not all connected

#### Example
```
Input:
4 5
0 1 100
1 2 150
2 3 200
0 3 300
1 3 120
0 0

Output:
150
```

#### Solution

##### Approach
Use Kruskal's algorithm to build MST. Track the maximum edge weight added to MST. This gives the minimum driving range needed.

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
      return False
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1
    return True


def kruskal_max_edge(n, edges):
  """Returns the maximum edge weight in MST (minimum driving range)."""
  edges.sort(key=lambda e: e[2])
  dsu = DSU(n)
  max_edge = 0
  mst_count = 0

  for u, v, w in edges:
    if dsu.union(u, v):
      max_edge = w
      mst_count += 1
      if mst_count == n - 1:
        return max_edge

  return 'IMPOSSIBLE'


def solution():
  while True:
    N, M = map(int, input().split())
    if N == 0 and M == 0:
      break

    edges = [tuple(map(int, input().split())) for _ in range(M)]
    print(kruskal_max_edge(N, edges))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log E)
- **Space Complexity:** O(E + V)

---

### Oreon

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a weighted adjacency matrix of cities, find and print all edges in the Minimum Spanning Tree. Cities are labeled A, B, C, etc. Output edges in sorted order (by source, then by weight).

#### Input Format
- Number of test cases
- For each test case:
  - Number of cities
  - Adjacency matrix (comma-separated, 0 means no edge)

#### Output Format
"Case X:" followed by MST edges in format "A-B W"

#### Example
```
Input:
1
3
0, 10, 20
10, 0, 15
20, 15, 0

Output:
Case 1:
A-B 10
B-C 15
```

#### Solution

##### Approach
Parse adjacency matrix to create edge list. Apply Kruskal's algorithm with edges sorted by (weight, source). Print MST edges with city letters.

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
      return False
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1
    return True


def kruskal(n, edges):
  """Returns list of MST edges as (source, target, weight) tuples."""
  edges.sort(key=lambda e: (e[2], e[0]))  # Sort by weight, then source
  dsu = DSU(n)
  mst = []

  for u, v, w in edges:
    if dsu.union(u, v):
      mst.append((u, v, w))
      if len(mst) == n - 1:
        break

  return mst


def solution():
  T = int(input())

  for t in range(T):
    n = int(input())
    edges = []

    for i in range(n):
      row = list(map(int, input().split(', ')))
      for j in range(i):
        if row[j] > 0:
          edges.append((j, i, row[j]))

    mst = kruskal(n, edges)
    print(f'Case {t + 1}:')
    for u, v, w in mst:
      print(f"{chr(u + 65)}-{chr(v + 65)} {w}")


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V^2 + E log E)
- **Space Complexity:** O(V^2)

---

### Anti Brute Force Lock

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

A safe has N locks, each with a 4-digit combination. Starting from "0000", find the minimum total number of dial rotations to unlock all locks. Each dial can rotate in either direction (0->1 or 0->9).

#### Input Format
- Number of test cases
- For each test case:
  - N (number of locks)
  - N 4-digit lock combinations

#### Output Format
Minimum total rotations to unlock all locks.

#### Example
```
Input:
1
3 1234 5678 9012

Output:
26
```

#### Solution

##### Approach
Model as MST problem: nodes are lock combinations. Edge weight = minimum rotations to change one combination to another. Find minimum rotation from "0000" to any lock, then MST of all locks. Total = initial approach cost + MST weight.

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
      return False
    if self.rank[pu] < self.rank[pv]:
      pu, pv = pv, pu
    self.parent[pv] = pu
    if self.rank[pu] == self.rank[pv]:
      self.rank[pu] += 1
    return True


def calculate_rolls(start, stop):
  """Calculate minimum dial rotations between two 4-digit codes."""
  return sum(
    min(abs(int(a) - int(b)), 10 - abs(int(a) - int(b)))
    for a, b in zip(start, stop)
  )


def kruskal(n, edges):
  edges.sort(key=lambda e: e[2])
  dsu = DSU(n)
  mst_weight = 0
  mst_count = 0

  for u, v, w in edges:
    if dsu.union(u, v):
      mst_weight += w
      mst_count += 1
      if mst_count == n - 1:
        break

  return mst_weight


def solution():
  T = int(input())

  for _ in range(T):
    parts = input().split()
    n = int(parts[0])
    locks = parts[1:n + 1]

    # Find minimum initial cost from 0000 to any lock
    initial = min(calculate_rolls('0000', lock) for lock in locks)

    # Build edges between all lock pairs
    edges = [
      (i, j, calculate_rolls(locks[i], locks[j]))
      for i in range(n) for j in range(i + 1, n)
    ]

    print(kruskal(n, edges) + initial)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N^2 log N) for building and sorting edges
- **Space Complexity:** O(N^2)
