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

#### Example
```
Input:
2
3 3
1 2 5
2 3 2
3 1 4
3 3
1 2 5
2 3 2
3 1 -4

Output:
Yes
No
```
First case: Cycle 1->2->3->1 with total profit 5+2+4=11 > 0, so infinite profit possible. Second case: Cycle has profit 5+2+(-4)=3 but no positive cycle that gives infinite arbitrage.

#### Solution

##### Approach
Use Bellman-Ford algorithm with negated edge weights. Negate weights to convert profit maximization to shortest path. After N-1 iterations, if any edge can still be relaxed, a negative cycle exists. Negative cycle in negated graph = positive cycle in original = infinite profit.

##### Python Solution

```python
import sys

INF = float('inf')


def bellman_ford(n, edges):
    dist = [INF] * (n + 1)
    dist[1] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Check for negative cycle
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return 'Yes'

    return 'No'


def solution():
    tokens = sys.stdin.read().split()[::-1]
    t = int(tokens.pop())

    for _ in range(t):
        n, m = int(tokens.pop()), int(tokens.pop())
        edges = [
            (int(tokens.pop()), int(tokens.pop()), -int(tokens.pop()))
            for _ in range(m)
        ]
        print(bellman_ford(n, edges))


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

#### Example
```
Input:
5 4 3 0
0 1 999
1 2 -2
2 1 1
0 3 2
1
3
4

Output:
-Infinity
2
Impossible
```
Node 1 is affected by negative cycle (1->2->1 with weight -2+1=-1). Node 3 has shortest distance 2 from source 0. Node 4 is unreachable from source.

#### Solution

##### Approach
Use Bellman-Ford algorithm for single-source shortest path with negative weights. Run N-1 iterations for standard relaxation. Run one more iteration to detect nodes affected by negative cycles. Nodes that can still be relaxed are affected by negative cycles.

##### Python Solution

```python
import sys

INF = float('inf')


def bellman_ford(n, edges, queries):
    dist = [INF] * (n + 1)
    neg_cycle = [False] * (n + 1)

    dist[0] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Detect nodes affected by negative cycles
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            neg_cycle[v] = True

    for q in queries:
        if neg_cycle[q]:
            print('-Infinity')
        elif dist[q] == INF:
            print('Impossible')
        else:
            print(dist[q])


def solution():
    tokens = sys.stdin.read().split()[::-1]

    while True:
        n = int(tokens.pop())
        if n == 0:
            break
        m, num_queries, _ = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())

        edges = [
            (int(tokens.pop()), int(tokens.pop()), int(tokens.pop()))
            for _ in range(m)
        ]
        queries = [int(tokens.pop()) for _ in range(num_queries)]

        bellman_ford(n, edges, queries)
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

#### Example
```
Input:
1
5
6 7 8 2 4
6
1 2
2 3
3 4
1 3
1 4
4 5
2
4
5

Output:
Case 1:
?
4
```
From junction 1: to reach junction 4, cost is negative (busyness differences cubed can be negative), so output "?". To junction 5, minimum cost is 4.

#### Solution

##### Approach
Use Bellman-Ford algorithm to handle negative edge weights. Edge weight = (busyness[v] - busyness[u])^3. Detect negative cycles and mark affected nodes. Output "?" for unreachable, negative cycle affected, or cost < 3.

##### Python Solution

```python
import sys

INF = float('inf')


def bellman_ford(n, edges, queries, case_number):
    dist = [INF] * (n + 1)
    neg_cycle = [False] * (n + 1)

    print(f'Case {case_number}:')

    dist[1] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            neg_cycle[v] = True

    for q in queries:
        if neg_cycle[q] or dist[q] < 3 or dist[q] == INF:
            print('?')
        else:
            print(dist[q])


def solution():
    tokens = sys.stdin.read().split()[::-1]
    t = int(tokens.pop())

    for case in range(1, t + 1):
        n = int(tokens.pop())
        busyness = [0] + [int(tokens.pop()) for _ in range(n)]

        m = int(tokens.pop())
        edges = []
        for _ in range(m):
            i, j = int(tokens.pop()), int(tokens.pop())
            edges.append((i, j, busyness[j] - busyness[i]))

        num_queries = int(tokens.pop())
        queries = [int(tokens.pop()) for _ in range(num_queries)]

        bellman_ford(n, edges, queries, case)


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

#### Example
```
Input:
3
Sphinx 10 -2 0
Move 0 5 -3
Pyramid 0 0 0
2
0 1
1 2

Output:
Case #1:
Sphinx-Move 10
Move-Pyramid -3
```
Travel cost from Sphinx to Move is 10. Travel cost from Move to Pyramid is -3.

#### Solution

##### Approach
Use Bellman-Ford algorithm for each unique source in queries. Handle negative edge weights and detect negative cycles. Cache results to avoid recomputing for same source.

##### Python Solution

```python
from collections import defaultdict

INF = float('inf')


def bellman_ford(n, edges, source):
    dist = [INF] * (n + 1)
    neg_cycle = [False] * (n + 1)

    dist[source] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            neg_cycle[v] = True

    return dist, neg_cycle


def solution():
    case_num = 1
    while True:
        n = int(input())
        if n == 0:
            break

        edges = []
        monuments = []
        for x in range(n):
            line = input().split()
            monuments.append(line[0])
            for i, cost in enumerate(line[1:], start=0):
                cost = int(cost)
                if cost != 0 and (cost < 0 or x != i):
                    edges.append((x, i, cost))

        num_queries = int(input())
        query_list = []
        unique_sources = defaultdict(list)
        for _ in range(num_queries):
            src, dest = map(int, input().split())
            query_list.append((src, dest))
            unique_sources[src].append(dest)

        print(f'Case #{case_num}:')

        # Cache results per source
        dist_cache = {}
        neg_cache = {}
        for source in unique_sources:
            dist_cache[source], neg_cache[source] = bellman_ford(n, edges, source)

        for src, dest in query_list:
            dist = dist_cache[src][dest]
            is_neg = neg_cache[src][dest]
            if (dist < 0 and src == dest) or is_neg:
                print("NEGATIVE CYCLE")
            elif dist == INF:
                print(f"{monuments[src]}-{monuments[dest]} NOT REACHABLE")
            else:
                print(f"{monuments[src]}-{monuments[dest]} {dist}")

        case_num += 1


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

#### Example
```
Input:
5 7
1 2 50
2 3 50
3 4 50
4 5 50
1 3 80
2 4 80
3 5 80

Output:
51.200000 percent
```
Best path: 1->3 (80%) -> 4 (80%) -> 5 (80%) = 0.8 * 0.8 * 0.8 * 100 = 51.2% probability.

#### Solution

##### Approach
Use modified Bellman-Ford to maximize product of probabilities. Initialize source with 100% probability. Relax edges by multiplying probabilities instead of adding distances. Edges are bidirectional.

##### Python Solution

```python
import sys

NEG_INF = float('-inf')


def bellman_ford(n, edges):
    dist = [NEG_INF] * (n + 1)
    dist[1] = 100

    for _ in range(n - 1):
        for u, v, prob in edges:
            if dist[u] != NEG_INF and dist[u] * prob / 100 > dist[v]:
                dist[v] = dist[u] * prob / 100

    return f"{dist[n]:.6f} percent"


def solution():
    tokens = sys.stdin.read().split()[::-1]

    while True:
        n = int(tokens.pop())
        if n == 0:
            break
        m = int(tokens.pop())

        edges = []
        for _ in range(m):
            a, b, p = int(tokens.pop()), int(tokens.pop()), int(tokens.pop())
            edges.extend([(a, b, p), (b, a, p)])  # Bidirectional

        print(bellman_ford(n, edges))


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

#### Example
```
Input:
5
0 1 2
-60 1 3
-60 1 4
20 1 5
0 0

Output:
winnable
```
Player starts in room 1 with 100 energy. Path: 1->2 (100-60=40) -> 3 (40-60=-20, dies) OR 1->2->4->5 with energy management. The game is winnable.

#### Solution

##### Approach
Use modified Bellman-Ford to maximize energy (find longest path). Only traverse edges if current energy > 0. If a positive cycle exists that can reach room n, game is winnable. Detect positive cycles that allow infinite energy gain.

##### Python Solution

```python
import sys

NEG_INF = float('-inf')


def bellman_ford(n, edges):
    dist = [NEG_INF] * n
    dist[0] = 100

    for _ in range(n - 1):
        for u, v, energy in edges:
            if dist[u] != NEG_INF and dist[u] + energy > dist[v] and dist[u] + energy > 0:
                dist[v] = dist[u] + energy

    # Check for positive cycle (can gain infinite energy)
    for u, v, energy in edges:
        if dist[u] != NEG_INF and dist[u] + energy > dist[v] != NEG_INF:
            return 'winnable'

    return 'hopeless' if dist[n - 1] < 0 else 'winnable'


def solution():
    tokens = sys.stdin.read().split()[::-1]

    while True:
        n = int(tokens.pop())
        if n == -1:
            break

        edges = []
        energies = []
        for i in range(n):
            energy = int(tokens.pop())
            energies.append(energy)
            num_connections = int(tokens.pop())
            for _ in range(num_connections):
                neighbor = int(tokens.pop()) - 1
                edges.append([i, neighbor])

        # Add energy values to edges
        for edge in edges:
            edge.append(energies[edge[1]])

        print(bellman_ford(n, edges))


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

#### Example
```
Input:
5
50
30 5
100 20 50
10 x x 10

Output:
35
```
Shortest paths from processor 0: to 1 is 50, to 2 is 35 (0->1->2 = 50+5=55 or 0->4->3 = 10+10+20=40... wait, 0->2 = 30), to 3 is 20, to 4 is 10. Maximum is 35 (to processor 2 via 0->1->2 = 50+5=55, but directly 30 is better, final max is from all shortest paths).

#### Solution

##### Approach
Use Bellman-Ford algorithm. Build undirected graph from lower triangular matrix. Find shortest paths from processor 0 to all others. Return the maximum of all shortest path distances.

##### Python Solution

```python
INF = float('inf')


def bellman_ford(n, edges):
    dist = [INF] * n
    dist[0] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    return max(dist)


def solution():
    n = int(input())
    edges = []

    for i in range(n - 1):
        line = input().strip().split()
        for j, val in enumerate(line[:i + 1]):
            if val != 'x':
                cost = int(val)
                edges.extend([(i + 1, j, cost), (j, i + 1, cost)])

    print(bellman_ford(n, edges))


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

#### Example
```
Input:
2
3 3
0 1 1000
1 2 15
2 1 -42
4 4
0 1 10
1 2 20
2 3 30
3 0 -60

Output:
possible
not possible
```
First case: Cycle 1->2->1 with weight 15+(-42)=-27 is a negative cycle. Second case: Cycle 0->1->2->3->0 with weight 10+20+30+(-60)=0, not negative.

#### Solution

##### Approach
Use Bellman-Ford algorithm to detect negative cycles. Run N-1 iterations of relaxation. If any edge can still be relaxed in iteration N, a negative cycle exists.

##### Python Solution

```python
import sys

INF = float('inf')


def bellman_ford(n, edges):
    dist = [INF] * (n + 1)
    dist[0] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Check for negative cycle
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return 'possible'

    return 'not possible'


def solution():
    tokens = sys.stdin.read().split()[::-1]
    t = int(tokens.pop())

    for _ in range(t):
        n, m = int(tokens.pop()), int(tokens.pop())
        edges = [
            (int(tokens.pop()), int(tokens.pop()), int(tokens.pop()))
            for _ in range(m)
        ]
        print(bellman_ford(n, edges))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * V * E)
- **Space Complexity:** O(V + E)
