---
layout: simple
title: "Prim"
permalink: /problem_soulutions/Blue/Session 16 - Prim/
---

# Prim

This session covers Prim's algorithm for finding Minimum Spanning Trees (MST) in weighted undirected graphs.

## Problems

### Efficient Network

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Build an efficient network connecting N nodes using M weighted edges. Additionally, you have Q "free" connections with costs C[i] that can replace the most expensive edges in the MST to minimize total cost.

#### Input Format
- First line: N (nodes), M (edges)
- Next M lines: A, B, W (edge from A to B with weight W)
- Next line: Q (number of free connections)
- Next line: Q space-separated costs C[i]

#### Output Format
Minimum total cost to connect all nodes.

#### Example
```
Input:
4 5
1 2 10
2 3 5
3 4 8
1 4 12
2 4 6
2
3 4

Output:
18
```
MST edges: 2-3 (5), 2-4 (6), 1-2 (10) = 21. Free connections [3,4] sorted. Replace edge 10 with 3, replace edge 6 with 4. New total = 5 + 4 + 3 + 6 = 18.

#### Solution

##### Approach
Use Prim's algorithm with priority queue to find MST. Sort MST edge weights and free connection costs. Greedily replace expensive MST edges with cheaper free connections.

##### Python Solution

```python
import heapq


def prim(N, graph, C):
  dist = [-1] * (N + 1)
  visited = [False] * (N + 1)
  pqueue = [(0, 1)]  # (distance, node) - tuples work with heapq
  dist[1] = 0

  while pqueue:
    d, u = heapq.heappop(pqueue)
    visited[u] = True
    for v, w in graph[u]:
      if not visited[v] and (dist[v] == -1 or w < dist[v]):
        dist[v] = w
        heapq.heappush(pqueue, (w, v))

  dist.sort()
  C.sort()

  for i, c in enumerate(C):
    if i > N + 1 or dist[-i - 1] <= c:
      break
    dist[-i - 1] = c

  return sum(d for d in dist[1:N + 1] if d != -1)


def solution():
  N, M = map(int, input().split())

  graph = [[] for _ in range(N + 1)]
  for _ in range(M):
    A, B, W = map(int, input().split())
    graph[A].append((B, W))
    graph[B].append((A, W))

  Q = int(input())
  C = list(map(int, input().strip().split())) if Q > 0 else []

  print(prim(N, graph, C))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log V) for Prim's algorithm + O(Q log Q) for sorting free connections
- **Space Complexity:** O(V + E) for graph storage

---

### Prim's MST: Special Subtree

#### Problem Information
- **Source:** Hackerrank
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given an undirected weighted graph, find the weight of the Minimum Spanning Tree (MST). The MST connects all nodes with minimum total edge weight without forming cycles.

#### Input Format
- First line: N (nodes), M (edges)
- Next M lines: A, B, W (edge between nodes A and B with weight W)

#### Output Format
Single integer: total weight of the MST.

#### Example
```
Input:
5 6
1 2 3
1 3 4
2 3 2
2 4 6
3 4 1
4 5 5

Output:
11
```
MST edges: 3-4 (1), 2-3 (2), 1-2 (3), 4-5 (5). Total weight = 1 + 2 + 3 + 5 = 11.

#### Solution

##### Approach
Prim's algorithm using a min-heap (priority queue). Start from node 1, greedily add minimum weight edges. Track visited nodes to avoid cycles.

##### Python Solution

```python
import heapq


def prim(N, graph):
  dist = [-1] * (N + 1)
  visited = [False] * (N + 1)
  pqueue = [(0, 1)]  # (distance, node)
  dist[1] = 0

  while pqueue:
    _, u = heapq.heappop(pqueue)
    visited[u] = True
    for v, w in graph[u]:
      if not visited[v] and (dist[v] == -1 or w < dist[v]):
        dist[v] = w
        heapq.heappush(pqueue, (w, v))

  return sum(d for d in dist[1:N + 1] if d != -1)


def solution():
  N, M = map(int, input().split())

  graph = [[] for _ in range(N + 1)]
  for _ in range(M):
    A, B, W = map(int, input().split())
    graph[A].append((B, W))
    graph[B].append((A, W))

  print(prim(N, graph))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log V)
- **Space Complexity:** O(V + E)

---

### Road Construction

#### Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 32MB

#### Problem Statement

Given pairs of cities with road construction costs, find the minimum cost to connect all cities. Cities are given by name (strings). If it's impossible to connect all cities, output "Impossible".

#### Input Format
- First line: T (test cases)
- For each test case:
  - Blank line
  - M (number of roads)
  - M lines: city1 city2 cost (road between cities with construction cost)

#### Output Format
For each test case: "Case X: cost" or "Case X: Impossible"

#### Example
```
Input:
2

3
Dhaka Sylhet 100
Sylhet Chittagong 150
Chittagong Dhaka 200

2
Tokyo Osaka 50

Output:
Case 1: 250
Case 2: 50
```
Case 1: MST connects all 3 cities with edges Dhaka-Sylhet (100) and Sylhet-Chittagong (150) = 250.
Case 2: Only 2 cities with one road, MST = 50.

#### Solution

##### Approach
Map city names to indices using dictionary. Apply Prim's algorithm with priority queue. Handle disconnected components (return "Impossible").

##### Python Solution

```python
import heapq


def prim(N, graph):
  dist = [-1] * (N + 1)
  visited = [False] * (N + 1)
  pqueue = [(0, 1)]
  dist[1] = 0

  while pqueue:
    _, u = heapq.heappop(pqueue)
    visited[u] = True
    for v, w in graph[u]:
      if not visited[v] and (dist[v] == -1 or w < dist[v]):
        dist[v] = w
        heapq.heappush(pqueue, (w, v))

  for i in range(1, N + 1):
    if dist[i] == -1:
      return 'Impossible'

  return str(sum(d for d in dist[1:N + 1] if d != -1))


def solution():
  t = int(input())
  for j in range(t):
    input()
    m = int(input())
    graph = [[] for _ in range(m * 2 + 1)]
    cities = {}

    for _ in range(m):
      city1, city2, cost = input().strip().split()
      cost = int(cost)
      if city1 not in cities:
        cities[city1] = len(cities) + 1
      if city2 not in cities:
        cities[city2] = len(cities) + 1
      graph[cities[city1]].append((cities[city2], cost))
      graph[cities[city2]].append((cities[city1], cost))

    print(f"Case {j + 1}: {prim(len(cities), graph)}")


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log V)
- **Space Complexity:** O(V + E)

---

### Cobbled Streets

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

A town needs to pave roads between junctions. The cost per meter is p, and you're given road lengths. Find the minimum total cost to connect all junctions so everyone can reach everyone else.

#### Input Format
- First line: T (test cases)
- For each test case:
  - p (cost per meter)
  - n (number of junctions)
  - m (number of possible roads)
  - m lines: a, b, c (road from junction a to b with length c)

#### Output Format
For each test case: minimum total cost (MST weight * p)

#### Example
```
Input:
1
2
4
5
1 2 3
1 3 4
2 3 5
2 4 6
3 4 2

Output:
18
```
Cost per meter = 2. MST edges: 3-4 (2), 1-2 (3), 1-3 (4). Total length = 9. Cost = 9 * 2 = 18.

#### Solution

##### Approach
Use Prim's algorithm to find MST. Multiply MST total edge weight by price per meter p.

##### Python Solution

```python
import heapq


def prim(N, graph):
  dist = [-1] * (N + 1)
  visited = [False] * (N + 1)
  pqueue = [(0, 1)]
  dist[1] = 0

  while pqueue:
    _, u = heapq.heappop(pqueue)
    visited[u] = True
    for v, w in graph[u]:
      if not visited[v] and (dist[v] == -1 or w < dist[v]):
        dist[v] = w
        heapq.heappush(pqueue, (w, v))

  return sum(d for d in dist[1:N + 1] if d != -1)


def solution():
  t = int(input())
  for _ in range(t):
    p = int(input())
    n = int(input())
    m = int(input())
    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
      a, b, c = map(int, input().strip().split())
      graph[a].append((b, c))
      graph[b].append((a, c))

    print(prim(n, graph) * p)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log V)
- **Space Complexity:** O(V + E)

---

### Minimum Spanning Tree

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given an undirected weighted graph, find the total weight of its Minimum Spanning Tree. Classic MST problem.

#### Input Format
- First line: N (nodes), M (edges)
- Next M lines: A, B, W (edge between A and B with weight W)

#### Output Format
Single integer: total weight of the MST.

#### Example
```
Input:
4 5
1 2 1
1 3 2
2 3 3
2 4 4
3 4 5

Output:
7
```
MST edges: 1-2 (1), 1-3 (2), 2-4 (4). Total = 1 + 2 + 4 = 7.

#### Solution

##### Approach
Standard Prim's algorithm implementation. Use min-heap priority queue for efficient minimum edge selection. Maintain visited array to avoid cycles.

##### Python Solution

```python
import heapq


def prim(N, graph):
  dist = [-1] * (N + 1)
  visited = [False] * (N + 1)
  pqueue = [(0, 1)]
  dist[1] = 0

  while pqueue:
    _, u = heapq.heappop(pqueue)
    visited[u] = True
    for v, w in graph[u]:
      if not visited[v] and (dist[v] == -1 or w < dist[v]):
        dist[v] = w
        heapq.heappush(pqueue, (w, v))

  return sum(d for d in dist[1:N + 1] if d != -1)


def solution():
  N, M = map(int, input().split())

  graph = [[] for _ in range(N + 1)]
  for _ in range(M):
    A, B, W = map(int, input().split())
    graph[A].append((B, W))
    graph[B].append((A, W))

  print(prim(N, graph))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(E log V)
- **Space Complexity:** O(V + E)

---

### Audiophobia

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

In a city with crossings connected by streets, each street has a noise level. For multiple queries, find the path between two crossings that minimizes the maximum noise level encountered (minimax path problem).

#### Input Format
- Multiple test cases until C=S=Q=0
- C (crossings), S (streets), Q (queries)
- S lines: crossing1, crossing2, noise_level
- Q lines: source, destination (query pairs)

#### Output Format
For each query: minimum possible maximum noise level, or "no path"

#### Example
```
Input:
4 4 2
1 2 50
2 3 30
3 4 40
1 4 100
1 4
2 4
0 0 0

Output:
Case #1
50
40
```
Query 1-4: Path 1-2-3-4 has max noise 50, path 1-4 has noise 100. Minimax = 50.
Query 2-4: Path 2-3-4 has max noise 40, which is the minimax path.

#### Solution

##### Approach
Modified Floyd-Warshall algorithm. Instead of summing distances, take minimum of maximum edge weights: graph[i][j] = min(graph[i][j], max(graph[i][k], graph[k][j]))

##### Python Solution

```python
INF = 1e9


def solution():
  case_num = 0
  while True:
    C, S, Q = map(int, input().strip().split())
    if C == 0:
      break
    if case_num > 0:
      print()

    graph = [[INF] * (C + 1) for _ in range(C + 1)]
    for _ in range(S):
      A, B, W = map(int, input().strip().split())
      graph[A][B] = graph[B][A] = min(graph[A][B], W)

    # Floyd-Warshall for minimax path
    for k in range(1, C + 1):
      for i in range(1, C + 1):
        for j in range(1, C + 1):
          graph[i][j] = min(graph[i][j], max(graph[i][k], graph[k][j]))

    case_num += 1
    print(f"Case #{case_num}")
    for _ in range(Q):
      s, e = map(int, input().strip().split())
      print('no path' if graph[s][e] == INF else int(graph[s][e]))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V^3) for Floyd-Warshall
- **Space Complexity:** O(V^2)

---

### Connect the Campus

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

A university campus has n buildings at (x, y) coordinates. Some buildings are already connected by existing cables. Find the minimum additional cable length needed to connect all buildings (Euclidean distances).

#### Input Format
- n (number of buildings)
- n lines: x, y coordinates of each building
- m (number of existing connections)
- m lines: pairs of already connected buildings

#### Output Format
Minimum cable length needed (2 decimal places).

#### Example
```
Input:
4
0 0
0 10
10 0
10 10
1
1 2

Output:
20.00
```
Building 1 and 2 are already connected (cost 0). Need cables: 1-3 (distance 10) and 3-4 (distance 10). Total new cable = 20.00.

#### Solution

##### Approach
Create complete graph with Euclidean distances between all buildings. Set existing connections to weight 0. Apply Prim's algorithm to find MST. Sum only non-zero edges (new cables needed).

##### Python Solution

```python
import math
import heapq
import sys


class InputTokenizer:
  def __init__(self):
    self._tokens = sys.stdin.read().split()[::-1]

  def has_next(self):
    return bool(self._tokens)

  def next(self):
    return self._tokens.pop()


inp = InputTokenizer()


def prim(N, graph):
  dist = [-1.0] * (N + 1)
  visited = [False] * (N + 1)
  pqueue = [(0.0, 0)]
  dist[0] = 0

  while pqueue:
    _, u = heapq.heappop(pqueue)
    visited[u] = True
    for v in range(N):
      w = graph[u][v]
      if not visited[v] and w != -1 and (dist[v] == -1.0 or w < dist[v]):
        dist[v] = w
        heapq.heappush(pqueue, (w, v))

  return sum(d for d in dist[:N] if d != -1.0)


def solution():
  while inp.has_next():
    n = int(inp.next())
    cities = [(int(inp.next()), int(inp.next())) for _ in range(n)]

    graph = [[-1.0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
      for j in range(i + 1, n):
        d = math.hypot(cities[i][0] - cities[j][0], cities[i][1] - cities[j][1])
        graph[i][j] = graph[j][i] = d

    m = int(inp.next())
    for _ in range(m):
      x, y = int(inp.next()) - 1, int(inp.next()) - 1
      graph[x][y] = graph[y][x] = 0

    print(f"{prim(n, graph):.2f}")


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V^2 log V) for dense graph with Prim's
- **Space Complexity:** O(V^2)

---

### ACM Contest and Blackout

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Find both the Minimum Spanning Tree (MST) and the Second-Best MST for a given graph. The second-best MST differs by exactly one edge from the MST.

#### Input Format
- T (test cases)
- For each test case:
  - N (nodes), M (edges)
  - M lines: A, B, C (edge between A and B with weight C)

#### Output Format
For each test case: two integers - MST weight and second-best MST weight.

#### Example
```
Input:
1
4 5
1 2 1
1 3 2
2 3 3
2 4 4
3 4 5

Output:
7 8
```
MST: 1-2 (1), 1-3 (2), 2-4 (4) = 7. Second-best MST: Remove edge 1-3, use 2-3 instead. Or remove 2-4, use 3-4. Best second MST = 8.

#### Solution

##### Approach
First, find the MST using Prim's algorithm (track the path/edges used). For second-best MST: try removing each MST edge one at a time. Recompute MST without that edge, find minimum among all such trees.

##### Python Solution

```python
import heapq


def prim(N, graph):
  dist = [-1] * (N + 1)
  path = [-1] * (N + 1)
  visited = [False] * (N + 1)
  pqueue = [(0, 1)]
  dist[1] = 0

  while pqueue:
    _, u = heapq.heappop(pqueue)
    visited[u] = True
    for v in range(1, N + 1):
      w = graph[u][v]
      if not visited[v] and w != -1 and (dist[v] == -1 or w < dist[v]):
        dist[v] = w
        path[v] = u
        heapq.heappush(pqueue, (w, v))

  mst_cost = sum(d for d in dist[1:N + 1] if d != -1)
  return path, mst_cost


def solution():
  T = int(input())
  for _ in range(T):
    N, M = map(int, input().strip().split())

    graph = [[-1] * (N + 1) for _ in range(N + 1)]
    for _ in range(M):
      A, B, C = map(int, input().strip().split())
      graph[A][B] = graph[B][A] = C

    mst, mst_cost = prim(N, graph)

    second_mst_cost = int(1e9)
    for i, parent in enumerate(mst):
      if parent != -1:
        tmp_weight = graph[i][parent]
        graph[i][parent] = graph[parent][i] = -1
        _, current_cost = prim(N, graph)
        second_mst_cost = min(second_mst_cost, current_cost)
        graph[i][parent] = graph[parent][i] = tmp_weight

    print(mst_cost, second_mst_cost)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V * E log V) for finding second-best MST
- **Space Complexity:** O(V^2)
