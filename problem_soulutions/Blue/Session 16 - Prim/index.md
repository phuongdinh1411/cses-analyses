---
layout: simple
title: "Session 16 - Prim"
permalink: /problem_soulutions/Blue/Session 16 - Prim/
---

# Session 16 - Prim

This session covers Prim's algorithm for finding Minimum Spanning Trees (MST) in weighted undirected graphs.

## Problems

### efficient-network (Hackerearth)

```python
# Problem from Hackerearth
# https://www.hackerearth.com/challenges/hiring/globalsoft-backend-hiring-challenge/algorithm/efficient-network/
#
# Problem: Efficient Network
#
# Description:
# Build an efficient network connecting N nodes using M weighted edges.
# Additionally, you have Q "free" connections with costs C[i] that can
# replace the most expensive edges in the MST to minimize total cost.
#
# Input:
# - First line: N (nodes), M (edges)
# - Next M lines: A, B, W (edge from A to B with weight W)
# - Next line: Q (number of free connections)
# - Next line: Q space-separated costs C[i]
#
# Output:
# - Minimum total cost to connect all nodes
#
# Approach:
# - Use Prim's algorithm with priority queue to find MST
# - Sort MST edge weights and free connection costs
# - Greedily replace expensive MST edges with cheaper free connections


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph, C):

    dist = [-1 for x in range(N+1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(1, 0))
    dist[1] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for neighbor in graph[u]:
            v = neighbor.id
            w = neighbor.dist
            if not visited[v] and (w < dist[v] or dist[v] == -1):
                dist[v] = w
                heapq.heappush(pqueue, Node(v, w))

    dist.sort()
    C.sort()

    for i in range(len(C)):
        if i <= N + 1:
            if dist[-i - 1] > C[i]:
                dist[-i - 1] = C[i]
            else:
                break
        else:
            break

    result = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            result += dist[i]

    return result


def solution():

    N, M = map(int, input().split())

    graph = [[] for i in range(N + 1)]
    for i in range(M):
        A, B, W = map(int, input().split())

        graph[A].append(Node(B, W))
        graph[B].append(Node(A, W))

    Q = int(input())
    C = []
    if Q > 0:
        C = list(map(int, input().strip().split()))

    result = prim(N, graph, C)

    print(result)


solution()
```

### primsmstsub (Hackerrank)

```python
# Problem from Hackerrank
# https://www.hackerrank.com/challenges/primsmstsub/problem
#
# Problem: Prim's (MST): Special Subtree
#
# Description:
# Given an undirected weighted graph, find the weight of the Minimum
# Spanning Tree (MST). The MST connects all nodes with minimum total
# edge weight without forming cycles.
#
# Input:
# - First line: N (nodes), M (edges)
# - Next M lines: A, B, W (edge between nodes A and B with weight W)
#
# Output:
# - Single integer: total weight of the MST
#
# Approach:
# - Prim's algorithm using a min-heap (priority queue)
# - Start from node 1, greedily add minimum weight edges
# - Track visited nodes to avoid cycles
# - Time complexity: O(E log V)


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph):

    dist = [-1 for x in range(N+1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(1, 0))
    dist[1] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for neighbor in graph[u]:
            v = neighbor.id
            w = neighbor.dist
            if not visited[v] and (w < dist[v] or dist[v] == -1):
                dist[v] = w
                heapq.heappush(pqueue, Node(v, w))

    result = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            result += dist[i]

    return result


def solution():

    N, M = map(int, input().split())

    graph = [[] for i in range(N + 1)]
    for i in range(M):
        A, B, W = map(int, input().split())

        graph[A].append(Node(B, W))
        graph[B].append(Node(A, W))

    result = prim(N, graph)

    print(result)


solution()
```

### Road_Construction (LightOJ)

```python
# Problem from LightOJ
# http://lightoj.com/volume_showproblem.php?problem=1041
#
# Problem: Road Construction (LightOJ 1041)
#
# Description:
# Given pairs of cities with road construction costs, find the minimum
# cost to connect all cities. Cities are given by name (strings).
# If it's impossible to connect all cities, output "Impossible".
#
# Input:
# - First line: T (test cases)
# - For each test case:
#   - Blank line
#   - M (number of roads)
#   - M lines: city1 city2 cost (road between cities with construction cost)
#
# Output:
# - For each test case: "Case X: cost" or "Case X: Impossible"
#
# Approach:
# - Map city names to indices using dictionary
# - Apply Prim's algorithm with priority queue
# - Handle disconnected components (return "Impossible")


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph):

    dist = [-1 for x in range(N+1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(1, 0))
    dist[1] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for neighbor in graph[u]:
            v = neighbor.id
            w = neighbor.dist
            if not visited[v] and (w < dist[v] or dist[v] == -1):
                dist[v] = w
                heapq.heappush(pqueue, Node(v, w))

    result = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            result += dist[i]
        else:
            return 'Impossible'

    return str(result)


def solution():

    t = int(input())
    for j in range(t):
        input()
        m = int(input())
        graph = [[] for i in range(m * 2 + 1)]
        cities = {}
        index = 0
        for i in range(m):
            city1, city2, cost = map(str, input().strip().split())
            if cities.get(city1) is None:
                index += 1
                cities[city1] = index
            if cities.get(city2) is None:
                index += 1
                cities[city2] = index
            cost = int(cost)
            graph[cities[city1]].append(Node(cities[city2], cost))
            graph[cities[city2]].append(Node(cities[city1], cost))

        result = prim(len(cities), graph)

        print('Case {}: {}'.format(j + 1, result))


solution()
```

### CSTREET (SPOJ)

```python
# Problem from SPOJ
# https://www.spoj.com/problems/CSTREET/
#
# Problem: Cobbled Streets (SPOJ CSTREET)
#
# Description:
# A town needs to pave roads between junctions. The cost per meter is p,
# and you're given road lengths. Find the minimum total cost to connect
# all junctions so everyone can reach everyone else.
#
# Input:
# - First line: T (test cases)
# - For each test case:
#   - p (cost per meter)
#   - n (number of junctions)
#   - m (number of possible roads)
#   - m lines: a, b, c (road from junction a to b with length c)
#
# Output:
# - For each test case: minimum total cost (MST weight * p)
#
# Approach:
# - Use Prim's algorithm to find MST
# - Multiply MST total edge weight by price per meter p


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph):

    dist = [-1 for x in range(N+1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(1, 0))
    dist[1] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for neighbor in graph[u]:
            v = neighbor.id
            w = neighbor.dist
            if not visited[v] and (w < dist[v] or dist[v] == -1):
                dist[v] = w
                heapq.heappush(pqueue, Node(v, w))

    result = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            result += dist[i]

    return result


def solution():

    t = int(input())
    for j in range(t):
        p = int(input())
        n = int(input())
        m = int(input())
        graph = [[] for i in range(n + 1)]
        for i in range(m):
            a, b, c = map(int, input().strip().split())
            graph[a].append(Node(b, c))
            graph[b].append(Node(a, c))

        result = prim(n, graph)

        print(result * p)


solution()
```

### MST (SPOJ)

```python
# Problem from SPOJ
# https://www.spoj.com/problems/MST/
#
# Problem: Minimum Spanning Tree (SPOJ MST)
#
# Description:
# Given an undirected weighted graph, find the total weight of its
# Minimum Spanning Tree. Classic MST problem.
#
# Input:
# - First line: N (nodes), M (edges)
# - Next M lines: A, B, W (edge between A and B with weight W)
#
# Output:
# - Single integer: total weight of the MST
#
# Approach:
# - Standard Prim's algorithm implementation
# - Use min-heap priority queue for efficient minimum edge selection
# - Maintain visited array to avoid cycles


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph):

    dist = [-1 for x in range(N+1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(1, 0))
    dist[1] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for neighbor in graph[u]:
            v = neighbor.id
            w = neighbor.dist
            if not visited[v] and (w < dist[v] or dist[v] == -1):
                dist[v] = w
                heapq.heappush(pqueue, Node(v, w))

    result = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            result += dist[i]

    return result


def solution():

    N, M = map(int, input().split())

    graph = [[] for i in range(N + 1)]
    for i in range(M):
        A, B, W = map(int, input().split())

        graph[A].append(Node(B, W))
        graph[B].append(Node(A, W))

    result = prim(N, graph)

    print(result)


solution()
```

### 10048 (UVA)

```python
# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=989
#
# Problem: Audiophobia (UVA 10048)
#
# Description:
# In a city with crossings connected by streets, each street has a noise level.
# For multiple queries, find the path between two crossings that minimizes
# the maximum noise level encountered (minimax path problem).
#
# Input:
# - Multiple test cases until C=S=Q=0
# - C (crossings), S (streets), Q (queries)
# - S lines: crossing1, crossing2, noise_level
# - Q lines: source, destination (query pairs)
#
# Output:
# - For each query: minimum possible maximum noise level, or "no path"
#
# Approach:
# - Modified Floyd-Warshall algorithm
# - Instead of summing distances, take minimum of maximum edge weights
# - graph[i][j] = min(graph[i][j], max(graph[i][k], graph[k][j]))


INF = 1e9


def solution():

    index = 0
    while True:
        C, S, Q = map(int, input().strip().split())
        if C == 0:
            break
        if index > 0:
            print()
        graph = [[INF for j in range(C + 1)] for i in range(C + 1)]
        for i in range(S):
            A, B, W = map(int, input().strip().split())
            graph[A][B] = min(graph[A][B], W)
            graph[B][A] = min(graph[A][B], W)

        for k in range(1, C + 1):
            for i in range(1, C + 1):
                for j in range(1, C + 1):
                    graph[i][j] = min(graph[i][j], max(graph[i][k], graph[k][j]))

        index += 1
        print("Case #{}".format(index))
        for i in range(Q):
            s, e = map(int, input().strip().split())
            if graph[s][e] == INF:
                print('no path')
            else:
                print(graph[s][e])


solution()
```

### 10397 (UVA)

```python
# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1338
#
# Problem: Connect the Campus (UVA 10397)
#
# Description:
# A university campus has n buildings at (x, y) coordinates. Some buildings
# are already connected by existing cables. Find the minimum additional
# cable length needed to connect all buildings (Euclidean distances).
#
# Input:
# - n (number of buildings)
# - n lines: x, y coordinates of each building
# - m (number of existing connections)
# - m lines: pairs of already connected buildings
#
# Output:
# - Minimum cable length needed (2 decimal places)
#
# Approach:
# - Create complete graph with Euclidean distances between all buildings
# - Set existing connections to weight 0
# - Apply Prim's algorithm to find MST
# - Sum only non-zero edges (new cables needed)


import math
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


def prim(N, graph):

    dist = [-1.0 for x in range(N+1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(0, 0))
    dist[0] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for i in range(N):
            v = i
            w = graph[u][i]
            if not visited[v] and w != -1 and (w < dist[v] or dist[v] == -1.0):
                dist[v] = w
                heapq.heappush(pqueue, Node(v, w))

    result = 0
    for i in range(N):
        if dist[i] != -1.0:
            result += dist[i]

    return result


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) * (city1[0] - city2[0]) + (city1[1] - city2[1]) * (city1[1] - city2[1]))


def solution():

    while True:
        try:
            n = int(inp.next())
        except:
            return
        cities = []
        for i in range(n):
            x = int(inp.next())
            y = int(inp.next())
            cities.append([x, y])
        graph = [[-1.0 for j in range(n + 1)] for i in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n):
                distij = distance(cities[i], cities[j])
                graph[i][j] = distij
                graph[j][i] = distij

        m = int(inp.next())
        for i in range(m):
            x = int(inp.next())
            y = int(inp.next())
            graph[x - 1][y - 1] = 0
            graph[y - 1][x - 1] = 0

        result = prim(n, graph)

        print("{:.2f}".format(result))


solution()
```

### 10600 (UVA)

```python
# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1541
#
# Problem: ACM Contest and Blackout (UVA 10600)
#
# Description:
# Find both the Minimum Spanning Tree (MST) and the Second-Best MST for
# a given graph. The second-best MST differs by exactly one edge from the MST.
#
# Input:
# - T (test cases)
# - For each test case:
#   - N (nodes), M (edges)
#   - M lines: A, B, C (edge between A and B with weight C)
#
# Output:
# - For each test case: two integers - MST weight and second-best MST weight
#
# Approach:
# - First, find the MST using Prim's algorithm (track the path/edges used)
# - For second-best MST: try removing each MST edge one at a time
# - Recompute MST without that edge, find minimum among all such trees
# - Time complexity: O(V * E log V)


import heapq


class Node:
    def __init__(self, id, dist):
        self.dist = dist
        self.id = id

    def __lt__(self, other):
        return self.dist < other.dist


def prim(N, graph):

    dist = [-1 for x in range(N+1)]
    path = [-1 for x in range(N + 1)]
    visited = [False for i in range(N + 1)]
    pqueue = []
    heapq.heappush(pqueue, Node(1, 0))
    dist[1] = 0

    while len(pqueue) > 0:
        top = heapq.heappop(pqueue)
        u = top.id
        visited[u] = True
        for i in range(1, N + 1):
            v = i
            w = graph[u][i]
            if not visited[v] and w != -1 and (w < dist[v] or dist[v] == -1):
                dist[v] = w
                path[v] = u
                heapq.heappush(pqueue, Node(v, w))

    mst_cost = 0
    for i in range(1, N + 1):
        if dist[i] != -1:
            mst_cost += dist[i]

    return path, mst_cost


def solution():

    T = int(input())
    for i in range(T):
        N, M = map(int, input().strip().split())

        graph = [[-1 for j in range(N + 1)] for i in range(N + 1)]
        for i in range(M):
            A, B, C = map(int, input().strip().split())
            graph[A][B] = C
            graph[B][A] = C

        mst, mst_cost = prim(N, graph)

        second_mst_cost = 1e9
        for i in range(len(mst)):
            if mst[i] != -1:
                tmp_weight = graph[i][mst[i]]
                graph[i][mst[i]] = -1
                graph[mst[i]][i] = -1
                current_mst, current_mst_cost = prim(N, graph)
                if current_mst_cost < second_mst_cost:
                    second_mst_cost = current_mst_cost
                graph[i][mst[i]] = tmp_weight
                graph[mst[i]][i] = tmp_weight

        print(mst_cost, second_mst_cost)


solution()
```

