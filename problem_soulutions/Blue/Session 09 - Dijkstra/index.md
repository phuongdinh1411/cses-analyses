---
layout: simple
title: "Dijkstra"
permalink: /problem_soulutions/Blue/Session 09 - Dijkstra/
---

# Dijkstra

Dijkstra's shortest path algorithm problems for weighted graphs with non-negative edge weights.

## Problems

### Chocolate Journey

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

There are N cities connected by M bidirectional roads. K cities have chocolate shops. You need to travel from city A to city B, but must buy chocolate from one of the K cities. The chocolate expires after X time units, so you must reach B within X time from the chocolate city.

Find the minimum time to go from A to a chocolate city and then to B, such that the chocolate city to B takes at most X time.

#### Input Format
- Line 1: N M K X (cities, roads, chocolate cities, max time for chocolate)
- Line 2: K integers (chocolate city IDs)
- Next M lines: u v w (bidirectional road with weight w)
- Last line: A B (start and destination)

#### Output Format
Minimum total time, or -1 if impossible.

#### Solution

##### Approach
Run Dijkstra from A and from B. For each chocolate city within X distance from B, calculate total path through that city.

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

def dijkstra(N, A, graph):
 dist = [-1 for x in range(N+1)]
 pqueue = []
 heapq.heappush(pqueue, Node(A, 0))
 dist[A] = 0

 while len(pqueue) > 0:
  top = heapq.heappop(pqueue)
  u = top.id
  w = top.dist
  for neighbor in graph[u]:
   if w + neighbor.dist < dist[neighbor.id] or dist[neighbor.id] == -1:
    dist[neighbor.id] = w + neighbor.dist
    heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))

 return dist

def solution():
 N = int(inp.next())
 M = int(inp.next())
 k = int(inp.next())
 x = int(inp.next())

 chocolate_cities = []
 for i in range(k):
  chocolate_cities.append(int(inp.next()))

 graph = [[] for i in range(N + 1)]
 for i in range(M):
  A = int(inp.next())
  B = int(inp.next())
  W = int(inp.next())

  graph[B].append(Node(A, W))
  graph[A].append(Node(B, W))

 A = int(inp.next())
 B = int(inp.next())

 dist_from_b = dijkstra(N, B, graph)
 found_chocolate_city_to_b = False
 for i in range(k):
  if x >= dist_from_b[chocolate_cities[i]] >= 0:
   found_chocolate_city_to_b = True
   break

 if not found_chocolate_city_to_b:
  print(-1)
  return

 dist_from_a = dijkstra(N, A, graph)

 found_chocolate_city_to_a = False
 for i in range(k):
  if dist_from_a[chocolate_cities[i]] >= 0:
   found_chocolate_city_to_a = True
   break

 if not found_chocolate_city_to_a:
  print(-1)
  return

 min_time = -1

 for i in range(k):
  if x >= dist_from_b[chocolate_cities[i]] >= 0 and dist_from_a[chocolate_cities[i]] >= 0:
   if min_time == -1 or min_time > dist_from_b[chocolate_cities[i]] + dist_from_a[chocolate_cities[i]]:
    min_time = dist_from_b[chocolate_cities[i]] + dist_from_a[chocolate_cities[i]]

 print(min_time)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O((N + M) log N) for two Dijkstra runs
- **Space Complexity:** O(N + M) for graph and distance arrays

---

### Commandos

#### Problem Information
- **Source:** LightOJ 1174
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 32MB

#### Problem Statement

A group of commandos starts at building S. They must visit ALL N buildings to complete their mission, then gather at building D. All commandos move simultaneously and take optimal paths.

The total time is determined by the last commando to reach D. Find the minimum time for all commandos to complete the mission.

#### Input Format
- Line 1: T (test cases)
- For each test case:
  - Line 1: N (buildings)
  - Line 2: R (roads)
  - Next R lines: u v (bidirectional road)
  - Last line: S D (start and destination buildings)

#### Output Format
Maximum of (dist[S][i] + dist[i][D]) for all buildings i.

#### Solution

##### Approach
Run Dijkstra from S and from D, find max sum for any building to get the time of the slowest commando.

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
   if neighbor.id == T:
    return dist[neighbor.id]

def solution():
 T = int(inp.next())
 results = []
 case_number = 0

 for i in range(T):
  case_number += 1
  N = int(inp.next())
  R = int(inp.next())
  graph = [[] for i in range(N + 1)]
  for j in range(R):
   A = int(inp.next())
   B = int(inp.next())

   graph[B].append(Node(A, 1))
   graph[A].append(Node(B, 1))

  s = int(inp.next())
  d = int(inp.next())

  mx = 0
  for j in range(N):
   p = dijkstra(N, s, j, graph)
   q = dijkstra(N, j, d, graph)
   mx = max(mx, p + q)

  results.append('Case ' + str(case_number) + ': ' + str(mx))

 print(*results, sep='\n')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N * (N + R) log N) for N Dijkstra runs
- **Space Complexity:** O(N + R) for graph storage

---

### MICEMAZE - Mice and Maze

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1129ms
- **Memory Limit:** 1536MB

#### Problem Statement

N mice are in a maze with N cells. Cell E is the exit. Each mouse starts in a different cell and has T seconds to reach the exit. Passages are one-way with travel times.

Count how many mice can reach the exit within the time limit.

#### Input Format
- Line 1: N (cells/mice)
- Line 2: E (exit cell)
- Line 3: T (time limit)
- Line 4: M (number of passages)
- Next M lines: A B W (one-way passage from A to B taking W time)

#### Output Format
Number of mice that can reach exit in time.

#### Solution

##### Approach
Run Dijkstra from exit on REVERSED graph. Count cells whose distance is within T.

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

def dijkstra(E, T, N, graph):
 dist = [-1 for x in range(N+1)]
 path = [-1 for y in range(N+1)]
 pqueue = []
 heapq.heappush(pqueue, Node(E, 0))
 dist[E] = 0

 while len(pqueue) > 0:
  top = heapq.heappop(pqueue)
  u = top.id
  w = top.dist
  for neighbor in graph[u]:
   if w + neighbor.dist < dist[neighbor.id] or dist[neighbor.id] == -1:
    dist[neighbor.id] = w + neighbor.dist
    heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))
    path[neighbor.id] = u

 result = 0
 for i in range(1, N+1):
  if 0 <= dist[i] <= T:
   result += 1

 return result

def solution():
 N = int(inp.next())
 E = int(inp.next())
 T = int(inp.next())
 M = int(inp.next())

 graph = [[] for i in range(N + 1)]
 for i in range(M):
  A = int(inp.next())
  B = int(inp.next())
  W = int(inp.next())

  graph[B].append(Node(A, W))

 result = dijkstra(E, T, N, graph)

 print(result)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O((N + M) log N) for Dijkstra
- **Space Complexity:** O(N + M) for graph and distance arrays

---

### SHPATH - The Shortest Path

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1537ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given a weighted directed graph where cities have names, answer multiple shortest path queries between pairs of cities.

#### Input Format
- Line 1: S (number of test cases)
- For each test case:
  - Line 1: N (number of cities)
  - For each city:
    - City name
    - Number of neighbors, followed by (neighbor_id, cost) pairs
  - Line: R (number of queries)
  - Next R lines: source_name destination_name

#### Output Format
Shortest path distance for each query.

#### Solution

##### Approach
Dijkstra from source to destination for each query using city name to index mapping.

##### Python Solution

```python
import heapq

class Node:
 def __init__(self, id, dist):
  self.dist = dist
  self.id = id

 def __lt__(self, other):
  return self.dist < other.dist

def dijkstra(n, s, d, graph):
 dist = [-1 for x in range(n + 1)]
 pqueue = []
 heapq.heappush(pqueue, Node(s, 0))
 dist[s] = 0

 while len(pqueue) > 0:
  top = heapq.heappop(pqueue)
  u = top.id
  w = top.dist
  for neighbor in graph[u]:
   if w + neighbor.dist < dist[neighbor.id] or dist[neighbor.id] == -1:
    dist[neighbor.id] = w + neighbor.dist
    heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))

 return dist[d]

def solution():
 s = int(input())

 for i in range(s):
  new_line = input().strip()
  if not new_line:
   n = int(input())
  else:
   n = int(new_line)
  cities_index = {}
  graph = [[] for xx in range(n + 1)]
  for xxx in range(n):
   cities_index[input()] = xxx + 1
   n_road = int(input())
   for r in range(n_road):
    ct, we = map(int, input().strip().split())
    graph[xxx + 1].append(Node(ct, we))

  num_roads = int(input())
  for nr in range(num_roads):
   st, ds = map(str, input().strip().split())
   print(dijkstra(n, cities_index[st], cities_index[ds], graph))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(R * (N + M) log N) for R queries
- **Space Complexity:** O(N + M) for graph storage

---

### TRAFFICN - Traffic Network

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 211ms
- **Memory Limit:** 1536MB

#### Problem Statement

A city has N junctions connected by M one-way roads. The mayor can build ONE new bidirectional road from a list of K proposals. Find the minimum shortest path from junction S to T after optimally choosing which new road to build (or not building any).

#### Input Format
- Line 1: T (test cases)
- For each test case:
  - Line 1: N M K S T
  - Next M lines: u v w (existing one-way road)
  - Next K lines: u v w (proposed bidirectional road)

#### Output Format
Minimum shortest path S to T, or -1 if unreachable.

#### Solution

##### Approach
Run Dijkstra from S on original graph and from T on reversed graph. Try each proposed road in both directions.

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

def dijkstra(n, s, graph):
 dist = [-1 for x in range(n + 1)]
 pqueue = []
 heapq.heappush(pqueue, Node(s, 0))
 dist[s] = 0

 while len(pqueue) > 0:
  top = heapq.heappop(pqueue)
  u = top.id
  w = top.dist
  for neighbor in graph[u]:
   if w + neighbor.dist < dist[neighbor.id] or dist[neighbor.id] == -1:
    dist[neighbor.id] = w + neighbor.dist
    heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))

 return dist

def solution():
 T = int(inp.next())

 for test_case in range(T):
  n = int(inp.next())
  m = int(inp.next())
  k = int(inp.next())
  s = int(inp.next())
  t = int(inp.next())
  graph = [[] for i in range(n + 1)]
  rev_graph = [[] for i in range(n + 1)]
  matrix = [[-1 for i in range(n+1)] for j in range(n+1)]
  for i in range(m):
   A = int(inp.next())
   B = int(inp.next())
   W = int(inp.next())

   matrix[A][B] = W

   graph[A].append(Node(B, W))
   rev_graph[B].append(Node(A, W))

  propose_roads = []
  for i in range(k):
   A = int(inp.next())
   B = int(inp.next())
   W = int(inp.next())

   propose_roads.append({"u": A, "v": B, "w": W})

  from_s = dijkstra(n, s, graph)
  from_t = dijkstra(n, t, rev_graph)

  minimum_path = -1

  for new_road in propose_roads:
   new_path = -1
   midle_weight = new_road['w']
   if 0 < matrix[new_road['u']][new_road['v']] < midle_weight:
    midle_weight = matrix[new_road['u']][new_road['v']]
   if from_s[new_road['u']] >= 0 and from_t[new_road['v']] >= 0:
    new_path = from_s[new_road['u']] + from_t[new_road['v']] + midle_weight

   if from_t[new_road['u']] >= 0 and from_s[new_road['v']] >= 0:
    new_path2 = from_t[new_road['u']] + from_s[new_road['v']] + midle_weight
    if new_path == -1 or new_path > new_path2:
     new_path = new_path2

   if minimum_path == -1 or new_path < minimum_path:
    minimum_path = new_path

  if 0 < from_s[t] < minimum_path:
   minimum_path = from_s[t]
  print(minimum_path)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O((N + M) log N + K) for two Dijkstra runs plus K road checks
- **Space Complexity:** O(N^2) for adjacency matrix, O(N + M) for graphs

---

### TRVCOST - Travelling Cost

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 296ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given N bidirectional weighted roads and a starting city U, answer Q queries about the shortest distance from U to various destination cities.

#### Input Format
- Line 1: N (number of roads)
- Next N lines: A B W (bidirectional road between A and B with cost W)
- Line: U (starting city)
- Line: Q (number of queries)
- Next Q lines: destination city

#### Output Format
For each query, print shortest distance or "NO PATH".

#### Solution

##### Approach
Single Dijkstra from U, answer all queries from the precomputed distance array.

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

MAX = 1100

class Node:
 def __init__(self, id, dist):
  self.dist = dist
  self.id = id

 def __lt__(self, other):
  return self.dist < other.dist

def dijkstra(s, graph, queries):
 dist = [-1 for x in range(MAX)]
 path = [-1 for y in range(MAX)]
 pqueue = []
 heapq.heappush(pqueue, Node(s, 0))
 dist[s] = 0

 while len(pqueue) > 0:
  top = heapq.heappop(pqueue)
  u = top.id
  w = top.dist
  for neighbor in graph[u]:
   if w + neighbor.dist < dist[neighbor.id] or dist[neighbor.id] == -1:
    dist[neighbor.id] = w + neighbor.dist
    heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))
    path[neighbor.id] = u

 results = []
 nqueries = len(queries)
 for i in range(nqueries):
  if dist[queries[i]] != -1:
   results.append(str(dist[queries[i]]))
  else:
   results.append('NO PATH')

 return results

def solution():
 N = int(inp.next())

 graph = [[] for i in range(MAX)]
 for i in range(N):
  A = int(inp.next())
  B = int(inp.next())
  W = int(inp.next())

  graph[A].append(Node(B, W))
  graph[B].append(Node(A, W))

 U = int(inp.next())
 Q = int(inp.next())
 queries = []
 for i in range(Q):
  queries.append(int(inp.next()))

 results = dijkstra(U, graph, queries)

 print(*results, sep='\n')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O((V + N) log V + Q) where V is max vertex
- **Space Complexity:** O(V + N) for graph and distance arrays

---

### Sending Email

#### Problem Information
- **Source:** UVA 10986
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a network of N servers connected by M bidirectional cables with latencies, find the minimum latency to send an email from server S to server T.

#### Input Format
- Line 1: N (test cases)
- For each test case:
  - Line 1: n m S T (servers, cables, source, target)
  - Next m lines: A B W (cable between A and B with latency W)

#### Output Format
"Case #X: Y" where Y is shortest distance, or "unreachable".

#### Solution

##### Approach
Standard Dijkstra's algorithm from S to T.

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

def dijkstra(n, S, T, graph, case_number):
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

 result = 'unreachable'
 if dist[T] >= 0:
  result = str(dist[T])

 return 'Case #' + str(case_number) + ': ' + result

def solution():
 N = int(inp.next())
 results = []
 case_number = 0

 for i in range(N):
  case_number += 1
  n = int(inp.next())
  m = int(inp.next())
  S = int(inp.next())
  T = int(inp.next())
  graph = [[] for i in range(n + 1)]
  for i in range(m):
   A = int(inp.next())
   B = int(inp.next())
   W = int(inp.next())

   graph[B].append(Node(A, W))
   graph[A].append(Node(B, W))

  results.append(dijkstra(n, S, T, graph, case_number))

 print(*results, sep='\n')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O((n + m) log n) per test case
- **Space Complexity:** O(n + m) for graph storage

---

### Almost Shortest Path

#### Problem Information
- **Source:** UVA 12144
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Find the "almost shortest path" from S to D. This is the shortest path that does NOT use any edge that appears in ANY shortest path from S to D.

#### Input Format
- Multiple test cases until n=0 m=0
- For each test case:
  - Line 1: n m (nodes, edges)
  - Line 2: S D (source, destination)
  - Next m lines: A B W (directed edge from A to B with weight W)

#### Output Format
Almost shortest path length, or -1 if impossible.

#### Solution

##### Approach
Run Dijkstra from S and reverse Dijkstra from D. Identify edges on shortest paths where dist_S[u] + w + dist_D[v] == shortest, remove them, run Dijkstra again.

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

def dijkstra(n, s, graph, matrix):
 dist = [-1 for x in range(n)]
 path = [-1 for y in range(n)]
 pqueue = []
 heapq.heappush(pqueue, Node(s, 0))
 dist[s] = 0

 while len(pqueue) > 0:
  top = heapq.heappop(pqueue)
  u = top.id
  w = top.dist
  for neighbor in graph[u]:
   if matrix[u][neighbor.id] != -1:
    if w + neighbor.dist < dist[neighbor.id] or dist[neighbor.id] == -1:
     dist[neighbor.id] = w + neighbor.dist
     heapq.heappush(pqueue, Node(neighbor.id, dist[neighbor.id]))
     path[neighbor.id] = u

 return [dist, path]

def solution():
 while True:
  n = int(inp.next())
  if n == 0:
   break
  m = int(inp.next())
  s = int(inp.next())
  d = int(inp.next())
  graph = [[] for i in range(n)]
  rev_graph = [[] for i in range(n)]
  matrix = [[-1 for i in range(n)] for j in range(n)]
  rev_matrix = [[-1 for i in range(n)] for j in range(n)]
  for i in range(m):
   A = int(inp.next())
   B = int(inp.next())
   W = int(inp.next())

   matrix[A][B] = W
   rev_matrix[B][A] = W

   graph[A].append(Node(B, W))
   rev_graph[B].append(Node(A, W))

  from_s = dijkstra(n, s, graph, matrix)
  from_d = dijkstra(n, d, rev_graph, rev_matrix)

  dist_from_s = from_s[0]
  dist_from_d = from_d[0]

  shortest = dist_from_s[d]

  if shortest == -1:
   print(-1)
   continue

  for i in range(n):
   if dist_from_d[i] + dist_from_s[i] == shortest:
    matrix[s][i] = -1
    matrix[i][d] = -1

  shortest = dijkstra(n, s, graph, matrix)[0][d]

  print(shortest)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O((n + m) log n) for multiple Dijkstra runs
- **Space Complexity:** O(n^2) for adjacency matrix
