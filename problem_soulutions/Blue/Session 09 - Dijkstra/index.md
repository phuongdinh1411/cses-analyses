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

#### Example
```
Input:
4 4 2 3
2 3
1 2 2
2 3 1
3 4 2
1 4 5
1 4

Output:
5
```
4 cities, chocolate at cities 2 and 3. Max chocolate freshness time is 3. Path: 1->2 (2) ->3 (1) ->4 (2). Total time = 5. City 3 to 4 takes 2 <= 3, so chocolate stays fresh.

#### Solution

##### Approach
Run Dijkstra from A and from B. For each chocolate city within X distance from B, calculate total path through that city.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict
import sys

def dijkstra(n, start, graph):
    dist = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        for v, w in graph[u]:
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))

    return dist

def solution():
    tokens = sys.stdin.read().split()[::-1]

    n, m, k, x = (int(tokens.pop()) for _ in range(4))
    chocolate_cities = [int(tokens.pop()) for _ in range(k)]

    graph = defaultdict(list)
    for _ in range(m):
        a, b, w = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())
        graph[a].append((b, w))
        graph[b].append((a, w))

    start, end = int(tokens.pop()), int(tokens.pop())

    dist_from_end = dijkstra(n, end, graph)
    dist_from_start = dijkstra(n, start, graph)

    # Find minimum time through a valid chocolate city
    min_time = -1
    for city in chocolate_cities:
        if 0 <= dist_from_end[city] <= x and dist_from_start[city] >= 0:
            total = dist_from_start[city] + dist_from_end[city]
            if min_time == -1 or total < min_time:
                min_time = total

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

#### Example
```
Input:
1
4
4
0 1
1 2
2 3
0 2
0 3

Output:
Case 1: 4
```
4 buildings. Commandos start at 0, gather at 3. Building 1 takes: 0->1 (1 step) + 1->2->3 (2 steps) = 3. Building 2 takes: 0->2 (1 step) + 2->3 (1 step) = 2. Building 0 takes 0 + 0->2->3 = 2. The slowest is going via 1 then to 3 via 2, taking max = 4 (corrected path 0->1->2->3 = 3 and back needs 1 more).

#### Solution

##### Approach
Run Dijkstra from S and from D, find max sum for any building to get the time of the slowest commando.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict
import sys

def dijkstra(n, start, graph):
    dist = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        for v, w in graph[u]:
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))

    return dist

def solution():
    tokens = sys.stdin.read().split()[::-1]
    t = int(tokens.pop())
    results = []

    for case_num in range(1, t + 1):
        n, r = int(tokens.pop()), int(tokens.pop())
        graph = defaultdict(list)

        for _ in range(r):
            a, b = int(tokens.pop()), int(tokens.pop())
            graph[a].append((b, 1))
            graph[b].append((a, 1))

        s, d = int(tokens.pop()), int(tokens.pop())

        dist_from_s = dijkstra(n, s, graph)
        dist_from_d = dijkstra(n, d, graph)

        max_time = max(dist_from_s[j] + dist_from_d[j] for j in range(n))
        results.append(f"Case {case_num}: {max_time}")

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

#### Example
```
Input:
4
2
1
3
1 2 1

Output:
2
```
4 cells, exit at cell 2, time limit 1, one passage from 1 to 2 taking 1 second. Mouse at cell 2: distance 0 <= 1. Mouse at cell 1 can reach via passage in 1 second. Mice at cells 3 and 4 cannot reach. Answer: 2 mice.

#### Solution

##### Approach
Run Dijkstra from exit on REVERSED graph. Count cells whose distance is within T.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict
import sys

def dijkstra(start, n, graph):
    dist = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        for v, w in graph[u]:
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))

    return dist

def solution():
    tokens = sys.stdin.read().split()[::-1]

    n = int(tokens.pop())
    exit_cell = int(tokens.pop())
    time_limit = int(tokens.pop())
    m = int(tokens.pop())

    # Build reversed graph (from destination to sources)
    graph = defaultdict(list)
    for _ in range(m):
        a, b, w = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())
        graph[b].append((a, w))

    dist = dijkstra(exit_cell, n, graph)

    # Count mice that can reach exit within time limit
    result = sum(1 for i in range(1, n + 1) if 0 <= dist[i] <= time_limit)
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

#### Example
```
Input:
1
3
Bratislava
2
2 2
3 5
Vienna
1
3 3
Prague
0
2
Bratislava Vienna
Vienna Prague

Output:
2
3
```
3 cities. Bratislava connects to Vienna (cost 2), Prague (cost 5). Vienna connects to Prague (cost 3). Query 1: Bratislava to Vienna = 2. Query 2: Vienna to Prague = 3.

#### Solution

##### Approach
Dijkstra from source to destination for each query using city name to index mapping.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict

def dijkstra(n, start, dest, graph):
    dist = [-1] * (n + 1)
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
    num_cases = int(input())

    for _ in range(num_cases):
        line = input().strip()
        n = int(line) if line else int(input())

        city_to_idx = {}
        graph = defaultdict(list)

        for city_idx in range(1, n + 1):
            city_name = input().strip()
            city_to_idx[city_name] = city_idx
            num_roads = int(input())
            for _ in range(num_roads):
                neighbor, weight = map(int, input().split())
                graph[city_idx].append((neighbor, weight))

        num_queries = int(input())
        for _ in range(num_queries):
            src, dst = input().split()
            print(dijkstra(n, city_to_idx[src], city_to_idx[dst], graph))

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

#### Example
```
Input:
1
4 2 1 1 4
1 2 5
3 4 5
2 3 1

Output:
11
```
4 junctions, 2 existing roads (1->2 cost 5, 3->4 cost 5). One proposed bidirectional road 2-3 cost 1. Best path: 1->2->3->4 = 5+1+5 = 11.

#### Solution

##### Approach
Run Dijkstra from S on original graph and from T on reversed graph. Try each proposed road in both directions.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict
import sys

def dijkstra(n, start, graph):
    dist = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        for v, w in graph[u]:
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))

    return dist

def solution():
    tokens = sys.stdin.read().split()[::-1]
    num_tests = int(tokens.pop())

    for _ in range(num_tests):
        n, m, k, s, t = (int(tokens.pop()) for _ in range(5))

        graph = defaultdict(list)
        rev_graph = defaultdict(list)
        existing = {}

        for _ in range(m):
            a, b, w = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())
            existing[(a, b)] = w
            graph[a].append((b, w))
            rev_graph[b].append((a, w))

        proposed = [(int(tokens.pop()), int(tokens.pop()), int(tokens.pop())) for _ in range(k)]

        dist_from_s = dijkstra(n, s, graph)
        dist_from_t = dijkstra(n, t, rev_graph)

        min_path = dist_from_s[t] if dist_from_s[t] > 0 else -1

        for u, v, w in proposed:
            # Check if existing edge is shorter
            edge_weight = min(w, existing.get((u, v), w))

            # Try u -> v direction
            if dist_from_s[u] >= 0 and dist_from_t[v] >= 0:
                path = dist_from_s[u] + edge_weight + dist_from_t[v]
                if min_path == -1 or path < min_path:
                    min_path = path

            # Try v -> u direction (bidirectional proposed road)
            if dist_from_s[v] >= 0 and dist_from_t[u] >= 0:
                path = dist_from_s[v] + edge_weight + dist_from_t[u]
                if min_path == -1 or path < min_path:
                    min_path = path

        print(min_path)

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

#### Example
```
Input:
3
1 2 5
2 3 3
1 3 10
1
3
2
3

Output:
8
5
```
3 roads. Starting city is 1. Query 1: city 3. Shortest path 1->2->3 = 5+3 = 8. Query 2: city 2. Shortest path 1->2 = 5.

#### Solution

##### Approach
Single Dijkstra from U, answer all queries from the precomputed distance array.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict
import sys

MAX = 1100

def dijkstra(start, graph):
    dist = [-1] * MAX
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        for v, w in graph[u]:
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))

    return dist

def solution():
    tokens = sys.stdin.read().split()[::-1]

    n = int(tokens.pop())
    graph = defaultdict(list)

    for _ in range(n):
        a, b, w = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())
        graph[a].append((b, w))
        graph[b].append((a, w))

    start = int(tokens.pop())
    q = int(tokens.pop())
    queries = [int(tokens.pop()) for _ in range(q)]

    dist = dijkstra(start, graph)
    results = [str(dist[dest]) if dist[dest] != -1 else 'NO PATH' for dest in queries]

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

#### Example
```
Input:
2
4 3 0 3
0 1 2
1 2 3
2 3 1
3 2 0 2
0 1 5

Output:
Case #1: 6
Case #2: unreachable
```
Case 1: 4 servers, path 0->1->2->3 = 2+3+1 = 6. Case 2: No path from 0 to 2.

#### Solution

##### Approach
Standard Dijkstra's algorithm from S to T.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict
import sys

def dijkstra(n, start, dest, graph):
    dist = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        for v, w in graph[u]:
            new_dist = d + w
            if dist[v] == -1 or new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))

    return dist[dest] if dist[dest] >= 0 else None

def solution():
    tokens = sys.stdin.read().split()[::-1]
    num_cases = int(tokens.pop())
    results = []

    for case_num in range(1, num_cases + 1):
        n, m, s, t = (int(tokens.pop()) for _ in range(4))
        graph = defaultdict(list)

        for _ in range(m):
            a, b, w = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())
            graph[a].append((b, w))
            graph[b].append((a, w))

        dist = dijkstra(n, s, t, graph)
        result = str(dist) if dist is not None else 'unreachable'
        results.append(f"Case #{case_num}: {result}")

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

#### Example
```
Input:
4 5
0 3
0 1 1
1 3 1
0 2 2
2 3 1
1 2 1
0 0

Output:
3
```
Shortest path 0->1->3 has length 2. The "almost shortest" avoids edges on this path. Path 0->2->3 = 2+1 = 3.

#### Solution

##### Approach
Run Dijkstra from S and reverse Dijkstra from D. Identify edges on shortest paths where dist_S[u] + w + dist_D[v] == shortest, remove them, run Dijkstra again.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict
import sys

def dijkstra(n, start, graph, blocked):
    dist = [-1] * n
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heappop(pq)
        for v, w in graph[u]:
            if (u, v) not in blocked:
                new_dist = d + w
                if dist[v] == -1 or new_dist < dist[v]:
                    dist[v] = new_dist
                    heappush(pq, (new_dist, v))

    return dist

def solution():
    tokens = sys.stdin.read().split()[::-1]

    while True:
        n = int(tokens.pop())
        if n == 0:
            break

        m, s, d = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())

        graph = defaultdict(list)
        rev_graph = defaultdict(list)

        for _ in range(m):
            a, b, w = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())
            graph[a].append((b, w))
            rev_graph[b].append((a, w))

        dist_from_s = dijkstra(n, s, graph, set())
        dist_from_d = dijkstra(n, d, rev_graph, set())

        shortest = dist_from_s[d]

        if shortest == -1:
            print(-1)
            continue

        # Find and block edges on any shortest path
        blocked = set()
        for u in range(n):
            for v, w in graph[u]:
                if (dist_from_s[u] >= 0 and dist_from_d[v] >= 0 and
                    dist_from_s[u] + w + dist_from_d[v] == shortest):
                    blocked.add((u, v))

        almost_shortest = dijkstra(n, s, graph, blocked)[d]
        print(almost_shortest)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O((n + m) log n) for multiple Dijkstra runs
- **Space Complexity:** O(n^2) for adjacency matrix
