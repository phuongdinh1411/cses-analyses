---
layout: simple
title: "Bellman-Ford"
permalink: /problem_soulutions/Blue/Session 11 - Bellman-Ford/
---

# Bellman-Ford

This session covers the Bellman-Ford algorithm for finding shortest paths in graphs with negative edge weights and detecting negative cycles.

## Problems

### Monk's Business Day

#### Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Monk is planning a business trip between cities. Each road has a profit/cost. Determine if Monk can make infinite profit by traveling in cycles (arbitrage). Essentially, detect if there's a positive cycle in the graph.

#### Input Format
- T: number of test cases
- For each test case:
  - N M: number of cities and roads
  - M lines with i j C: road from i to j with profit C

#### Output Format
- "Yes" if infinite profit is possible (positive cycle exists), "No" otherwise

#### Solution

##### Approach
Use Bellman-Ford algorithm with negated edge weights. Negate weights to convert profit maximization to shortest path. After N-1 iterations, if any edge can still be relaxed, a negative cycle exists. Negative cycle in negated graph = positive cycle in original = infinite profit.

##### Python Solution

```python
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


INF = int(1e9)


def bellman_ford(N, M, E):
  dist = [INF for i in range(N + 1)]

  dist[1] = 0
  for i in range(1, N):
    for j in range(M):
      u = E[j][0]
      v = E[j][1]
      w = E[j][2]
      if dist[u] != INF and dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
  for j in range(M):
    u = E[j][0]
    v = E[j][1]
    w = E[j][2]
    if dist[u] != INF and dist[u] + w < dist[v]:
      return 'Yes'

  return 'No'


def solution():
  T = int(inp.next())
  for t in range(T):
    N = int(inp.next())
    M = int(inp.next())
    E = []
    for m in range(M):
      i = int(inp.next())
      j = int(inp.next())
      C = int(inp.next())
      E.append([i, j, -C])
    print(bellman_ford(N, M, E))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V * E) where V is vertices and E is edges
- **Space Complexity:** O(V + E)

---

### Single Source Shortest Path, Negative Weights

#### Problem Information
- **Source:** Kattis
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a directed weighted graph with possible negative edge weights, find the shortest path from source to multiple query nodes. Handle negative cycles by reporting "-Infinity" for affected nodes.

#### Input Format
- Multiple test cases until n=0
- For each test case:
  - n m q s: nodes, edges, queries, source
  - m lines with u v w: directed edge from u to v with weight w
  - q query nodes

#### Output Format
- For each query:
  - Shortest distance, or "Impossible" if unreachable, or "-Infinity" if affected by negative cycle

#### Solution

##### Approach
Use Bellman-Ford algorithm for single-source shortest path with negative weights. Run N-1 iterations for standard relaxation. Run one more iteration to detect nodes affected by negative cycles. Nodes that can still be relaxed are affected by negative cycles.

##### Python Solution

```python
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


INF = int(1e9)


def bellman_ford(N, M, E, q):
  dist = [INF for i in range(N + 1)]
  flag = [False for i in range(N + 1)]

  dist[0] = 0
  for i in range(1, N):
    for j in range(M):
      u = E[j][0]
      v = E[j][1]
      w = E[j][2]
      if dist[u] != INF and dist[u] + w < dist[v]:
        dist[v] = dist[u] + w

  for j in range(M):
    u = E[j][0]
    v = E[j][1]
    w = E[j][2]
    if dist[u] != INF and dist[u] + w < dist[v]:
      dist[v] = dist[u] + w
      flag[v] = True

  for cq in q:
    if flag[cq]:
      print('-Infinity')
    elif dist[cq] == INF:
      print('Impossible')
    else:
      print(dist[cq])


def solution():
  while True:
    N = int(inp.next())
    if N == 0:
      break
    M = int(inp.next())
    Q = int(inp.next())
    S = int(inp.next())

    E = []
    for m in range(M):
      i = int(inp.next())
      j = int(inp.next())
      w = int(inp.next())
      E.append([i, j, w])
    q = []
    for x in range(Q):
      q.append(int(inp.next()))

    bellman_ford(N, M, E, q)
    print()


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V * E) per test case
- **Space Complexity:** O(V + E)

---

### Extended Traffic

#### Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 32MB

#### Problem Statement

Dhaka city has junctions with "busyness" values. The cost to travel from junction u to v is (busyness[v] - busyness[u])^3, which can be negative. Find the minimum cost from junction 1 to query junctions. If cost < 3 or unreachable or affected by negative cycle, output "?".

#### Input Format
- T: number of test cases
- For each test case:
  - N: number of junctions
  - N busyness values
  - M: number of roads
  - M lines with u v: directed road from u to v
  - Q: number of queries
  - Q query junction numbers

#### Output Format
- For each case: "Case X:" followed by minimum cost for each query (or "?")

#### Solution

##### Approach
Use Bellman-Ford algorithm to handle negative edge weights. Edge weight = (busyness[v] - busyness[u])^3. Detect negative cycles and mark affected nodes. Output "?" for unreachable, negative cycle affected, or cost < 3.

##### Python Solution

```python
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


INF = int(1e9)


def bellman_ford(N, M, E, q, case_number):
  dist = [INF for i in range(N + 1)]
  flag = [False for i in range(N + 1)]

  print('Case ' + str(case_number) + ':')

  dist[1] = 0
  for i in range(0, N-1):
    for j in range(M):
      u = E[j][0]
      v = E[j][1]
      w = E[j][2]
      if dist[u] != INF and dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
  for j in range(M):
    u = E[j][0]
    v = E[j][1]
    w = E[j][2]
    if dist[u] != INF and dist[u] + w < dist[v]:
      dist[v] = dist[u] + w
      flag[v] = True

  for cq in q:
    if flag[cq] or dist[cq] < 3 or dist[cq] == INF:
      print('?')
    else:
      print(dist[cq])


def solution():
  T = int(inp.next())
  for t in range(T):
    N = int(inp.next())
    busyness = [0 for x in range(N + 1)]
    counter = 1
    for x in range(N):
      busyness[counter] = int(inp.next())
      counter += 1

    M = int(inp.next())
    E = []
    for m in range(M):
      i = int(inp.next())
      j = int(inp.next())
      E.append([i, j, busyness[j] - busyness[i]])
    nq = int(inp.next())
    q = []
    for x in range(nq):
      q.append(int(inp.next()))

    bellman_ford(N, M, E, q, t + 1)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * V * E) where T is test cases
- **Space Complexity:** O(V + E)

---

### Babylon Tours

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given N monuments in Babylon with travel costs between them (can be negative), find the shortest path for multiple tour queries. Detect if a query path is affected by a negative cycle.

#### Input Format
- Multiple test cases until N=0
- For each test case:
  - N: number of monuments
  - N lines: monument name followed by N costs (0 means no direct path)
  - Q: number of queries
  - Q lines with source and destination monument indices

#### Output Format
- For each case: "Case #X:" followed by results for each query
  - "monument1-monument2 cost" or "NOT REACHABLE" or "NEGATIVE CYCLE"

#### Solution

##### Approach
Use Bellman-Ford algorithm for each unique source in queries. Handle negative edge weights and detect negative cycles. Cache results to avoid recomputing for same source.

##### Python Solution

```python
from collections import defaultdict

INF = int(1e9)


def bellman_ford(N, M, E, query):
  dist = [INF for i in range(N + 1)]
  flag = [False for i in range(N + 1)]

  dist[query] = 0
  for i in range(0, N-1):
    for j in range(M):
      u = E[j][0]
      v = E[j][1]
      w = E[j][2]
      if dist[u] != INF and dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
  for j in range(M):
    u = E[j][0]
    v = E[j][1]
    w = E[j][2]
    if dist[u] != INF and dist[u] + w < dist[v]:
      dist[v] = dist[u] + w
      flag[v] = True

  return [dist, flag]


def solution():
  counter = 1
  while True:
    N = int(input())
    if N == 0:
      break

    E = []
    monuments = ['' for i in range(N)]
    for x in range(N):
      line = input().split()
      monuments[x] = line[0]
      for i in range(1, N + 1):
        if int(line[i]) != 0:
          if int(line[i]) < 0 or x != i - 1:
            E.append([x, i - 1, int(line[i])])

    nq = int(input())
    q = []
    queries = defaultdict(list)
    for x in range(nq):
      pair = list(map(int, (input().split())))
      q.append(pair)
      queries[pair[0]].append(pair[1])

    print('Case #' + str(counter) + ':')

    dists = [[] for x in range(N)]
    neg_flags = [[] for x in range(N)]

    for query in queries.keys():
      bf_result = bellman_ford(N, len(E), E, query)
      dists[query] = bf_result[0]
      neg_flags[query] = bf_result[1]

    for qq in q:
      dist = dists[qq[0]][qq[1]]
      is_neg = neg_flags[qq[0]][qq[1]]
      if (dist < 0 and qq[0] == qq[1]) or is_neg:
        print("NEGATIVE CYCLE")
      else:
        if dist == INF:
          dist = "NOT REACHABLE"
        start_city = monuments[qq[0]]
        dest_city = monuments[qq[1]]
        print("{}-{} {}".format(start_city, dest_city, dist))

    counter += 1


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(Q * V * E) where Q is unique query sources
- **Space Complexity:** O(V^2) for caching distances

---

### 106 Miles To Chicago

#### Problem Information
- **Source:** URI Online Judge
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

A spy needs to travel from intersection 1 to intersection n through Chicago. Each road segment has a probability of not being spotted (given as percentage). Find the maximum probability of traveling the entire path without being spotted. The total probability is the product of individual segment probabilities.

#### Input Format
- Multiple test cases until n=0
- For each test case:
  - n m: number of intersections and streets
  - m lines with a b p: street between a and b with p% probability of not being spotted

#### Output Format
- Maximum probability (as percentage) of reaching n from 1 unspotted

#### Solution

##### Approach
Use modified Bellman-Ford to maximize product of probabilities. Initialize source with 100% probability. Relax edges by multiplying probabilities instead of adding distances. Edges are bidirectional.

##### Python Solution

```python
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


INF = -int(1e9)


def bellman_ford(n, m, E):
  dist = [INF for i in range(n + 1)]
  dist[1] = 100
  for i in range(1, n):
    for j in range(m):
      u = E[j][0]
      v = E[j][1]
      w = E[j][2]
      if dist[u] != INF and dist[u] * w / 100 > dist[v]:
        dist[v] = dist[u] * w / 100

  return "{:.6f}".format(dist[n]) + ' percent'


def solution():
  while True:
    n = int(inp.next())
    if n == 0:
      break
    m = int(inp.next())

    E = []
    for i in range(m):
      a = int(inp.next())
      b = int(inp.next())
      p = int(inp.next())
      E.append([a, b, p])
      E.append([b, a, p])

    print(bellman_ford(n, m * 2, E))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V * E)
- **Space Complexity:** O(V + E)

---

### XYZZY

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

A text adventure game where the player starts in room 1 with 100 energy. Moving to a room adds/subtracts energy based on the room's energy value. The player dies if energy drops to 0 or below. Determine if the player can reach the last room (room n) with positive energy.

#### Input Format
- Multiple test cases until n=-1
- For each test case:
  - n: number of rooms
  - For each room: energy_value, num_connections, connected_rooms...

#### Output Format
- "winnable" if player can reach room n with positive energy, "hopeless" otherwise

#### Solution

##### Approach
Use modified Bellman-Ford to maximize energy (find longest path). Only traverse edges if current energy > 0. If a positive cycle exists that can reach room n, game is winnable. Detect positive cycles that allow infinite energy gain.

##### Python Solution

```python
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


INF = int(1e9)


def bellman_ford(N, M, E):
  dist = [-INF for i in range(N)]

  dist[0] = 100
  for i in range(0, N-1):
    for j in range(M):
      u = E[j][0]
      v = E[j][1]
      w = E[j][2]
      if dist[u] != -INF and dist[u] + w > dist[v] and dist[u] + w > 0:
        dist[v] = dist[u] + w
  for j in range(M):
    u = E[j][0]
    v = E[j][1]
    w = E[j][2]
    if dist[u] != -INF and dist[u] + w > dist[v] != -INF:
      return 'winnable'

  return 'hopeless' if dist[N - 1] < 0 else 'winnable'


def solution():
  while True:
    N = int(inp.next())
    if N == -1:
      break
    E = []
    energies = []
    for i in range(N):
      energy = int(inp.next())
      energies.append(energy)
      connections = int(inp.next())
      for j in range(connections):
        neighbor = int(inp.next()) - 1
        E.append([i, neighbor])
    for connection in E:
      connection.append(energies[connection[1]])
    print(bellman_ford(N, len(E), E))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V * E)
- **Space Complexity:** O(V + E)

---

### MPI Maelstrom

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

N processors are connected in a network. The communication time between processors is given in a lower triangular matrix format. Some connections may not exist (marked as 'x'). Find the minimum time to broadcast a message from processor 0 to all other processors (maximum shortest path from source).

#### Input Format
- N: number of processors
- Lower triangular matrix of communication times ('x' means no connection)

#### Output Format
- Maximum shortest path distance from processor 0 (broadcast completion time)

#### Solution

##### Approach
Use Bellman-Ford algorithm. Build undirected graph from lower triangular matrix. Find shortest paths from processor 0 to all others. Return the maximum of all shortest path distances.

##### Python Solution

```python
INF = int(1e9)


def bellman_ford(N, M, E):
  dist = [INF for i in range(N)]

  dist[0] = 0
  for i in range(0, N-1):
    for j in range(M):
      u = E[j][0]
      v = E[j][1]
      w = E[j][2]
      if dist[u] != INF and dist[u] + w < dist[v]:
        dist[v] = dist[u] + w

  max = 0
  for di in dist:
    if di > max:
      max = di

  return max


def solution():
  N = int(input())
  E = []
  for i in range(N - 1):
    line = list(map(str, input().strip().split()))
    for j in range(i + 1):
      if line[j] is not 'x':
        E.append([i + 1, j, int(line[j])])
        E.append([j, i + 1, int(line[j])])

  print(bellman_ford(N, len(E), E))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(V * E)
- **Space Complexity:** O(V + E)

---

### Wormholes

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

A spaceship can travel through wormholes that may have negative time travel (going back in time). Determine if it's possible to travel back in time indefinitely by finding a negative cycle in the graph.

#### Input Format
- T: number of test cases
- For each test case:
  - n m: number of star systems and wormholes
  - m lines with x y t: wormhole from x to y with time t (can be negative)

#### Output Format
- "possible" if negative cycle exists (infinite time travel possible)
- "not possible" otherwise

#### Solution

##### Approach
Use Bellman-Ford algorithm to detect negative cycles. Run N-1 iterations of relaxation. If any edge can still be relaxed in iteration N, a negative cycle exists.

##### Python Solution

```python
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


INF = int(1e9)


def bellman_ford(N, M, E):
  dist = [INF for i in range(N + 1)]

  dist[0] = 0
  for i in range(0, N-1):
    for j in range(M):
      u = E[j][0]
      v = E[j][1]
      w = E[j][2]
      if dist[u] != INF and dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
  for j in range(M):
    u = E[j][0]
    v = E[j][1]
    w = E[j][2]
    if dist[u] != INF and dist[u] + w < dist[v]:
      return 'possible'

  return 'not possible'


def solution():
  T = int(inp.next())
  for t in range(T):
    N = int(inp.next())
    M = int(inp.next())
    E = []
    for m in range(M):
      i = int(inp.next())
      j = int(inp.next())
      C = int(inp.next())
      E.append([i, j, C])
    print(bellman_ford(N, M, E))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * V * E)
- **Space Complexity:** O(V + E)
