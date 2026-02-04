---
layout: simple
title: "Session 19 - Kruskal"
permalink: /problem_soulutions/Blue/Session 19 - Kruskal/
---

# Session 19 - Kruskal

This session covers Kruskal's algorithm for finding Minimum Spanning Trees (MST) using edge sorting and Union-Find data structure.

## Problems

### 1123_Trail Maintenance (LightOJ)

```python
# Problem from LightOJ
# http://lightoj.com/volume_showproblem.php?problem=1123
#
# Problem: Trail Maintenance (LightOJ 1123)
#
# Description:
# A park has N fields connected by trails. Trails are added one by one.
# After each trail is added, compute the MST weight. Output -1 if the
# graph is not yet connected (before N-1 edges are added).
#
# Input:
# - T (test cases)
# - For each test case:
#   - N (fields), M (trails to add)
#   - M lines: x, y, z (trail from field x to y with length z)
#
# Output:
# - After each trail addition: MST weight or -1 if not connected
#
# Approach:
# - Incrementally add edges to the graph
# - After each addition, run Kruskal's algorithm to find MST
# - Use DSU for cycle detection in Kruskal's
# - Return -1 until at least N-1 edges connect all nodes


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return str(self.source) + '-' + str(self.target) + ': ' + str(self.weight)


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for _ in range(V + 1)]


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


def kruskal(number_of_fields):
    graph.sort(key=lambda _edge: _edge.weight)
    i = 0
    mst = 0
    while len(dist) != number_of_fields - 1 and i < len(graph):
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
            mst += edge.weight

    if len(dist) == number_of_fields - 1:
        return mst
    else:
        return -1


def solution():

    T = int(input())

    for t in range(T):
        global graph, dist
        graph = []
        N, M = map(int, input().split())
        print('Case {0}:'.format(t + 1))
        for i in range(M):
            x, y, z = map(int, input().split())
            graph.append(Triad(x, y, z))
            if i < N - 1:
                print(-1)
            else:
                dist = []
                make_set(N)
                minimum_distance = kruskal(N)
                print(minimum_distance)


solution()
```

### 11631 (UVA)

```python
# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2678
#
# Problem: Dark Roads (UVA 11631)
#
# Description:
# A city wants to save electricity by turning off some street lights.
# They need to keep lights on only for roads in the MST (to maintain
# connectivity). Calculate how much power can be saved.
#
# Input:
# - Multiple test cases until m=n=0
# - m (junctions), n (roads)
# - n lines: x, y, z (road from x to y with power cost z)
#
# Output:
# - Total power saved = (sum of all edges) - (MST weight)
#
# Approach:
# - Use Kruskal's algorithm to find MST
# - Sum weights of edges not in MST (edges that form cycles)
# - This gives the total power that can be saved


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return str(self.source) + '-' + str(self.target) + ': ' + str(self.weight)


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for _ in range(V + 1)]


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


def kruskal(number_of_cities):
    graph.sort(key=lambda _edge: _edge.weight)
    i = 0
    saved = 0
    while len(dist) != number_of_cities - 1:
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
        else:
            saved += edge.weight

    for j in range(i, len(graph)):
        saved += graph[j].weight

    return saved


def solution():

    while True:
        global graph, dist
        graph = []
        dist = []
        m, n = map(int, input().split())
        if m == 0:
            break
        for _ in range(n):
            x, y, z = map(int, input().split())
            graph.append(Triad(x, y, z))

        make_set(m)

        print(kruskal(m))


solution()
```

### 11710 (UVA)

```python
# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2757
#
# Problem: Expensive Subway (UVA 11710)
#
# Description:
# Calculate the minimum cost to build a subway system connecting all stations.
# Stations are given as names (strings). If impossible to connect all stations,
# output "Impossible".
#
# Input:
# - Multiple test cases until s=c=0
# - s (stations), c (connections)
# - s station names
# - c lines: station1 station2 cost
# - End station name (ignored)
#
# Output:
# - MST weight or "Impossible" if graph is disconnected
#
# Approach:
# - Map station names to indices using dictionary
# - Apply Kruskal's algorithm to find MST
# - Check if MST spans all stations (exactly s-1 edges)


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return str(self.source) + '-' + str(self.target) + ': ' + str(self.weight)


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for _ in range(V + 1)]


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


def kruskal(number_of_cities):
    graph.sort(key=lambda _edge: _edge.weight)
    i = 0
    mst = 0
    while len(dist) != number_of_cities - 1 and i < len(graph):
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
            mst += edge.weight

    if len(dist) == number_of_cities - 1:
        return mst
    else:
        return 'Impossible'


def solution():

    while True:
        global graph, dist
        graph = []
        dist = []
        station_dictionary = {}
        s, c = map(int, input().split())
        if s == 0:
            break

        for i in range(s):
            station = input().strip()
            station_dictionary[station] = i
        for _ in range(c):
            x, y, z = input().split()
            graph.append(Triad(station_dictionary[x], station_dictionary[y], int(z)))

        input()

        make_set(s)

        print(kruskal(s))


solution()
```

### 11733 (UVA)

```python
# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2833
#
# Problem: Airports (UVA 11733)
#
# Description:
# Connect N cities using either airports or roads. Each city needs either
# an airport OR road connection to an airport city. Building an airport
# costs A, and each road has its own cost. Minimize total cost.
#
# Input:
# - T (test cases)
# - For each test case:
#   - N (cities), M (possible roads), A (airport cost)
#   - M lines: x, y, z (road from x to y with cost z)
#
# Output:
# - "Case #X: cost airports" (total cost and number of airports built)
#
# Approach:
# - Modified Kruskal's algorithm
# - Only add edge to MST if its cost < airport cost A
# - Cities not connected by cheap roads get airports
# - Count components (each needs one airport)


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return str(self.source) + '-' + str(self.target) + ': ' + str(self.weight)


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for _ in range(V + 1)]


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


def kruskal(number_of_cities, airport_cost):
    graph.sort(key=lambda _edge: _edge.weight)
    i = 0
    mst = 0
    n_airports = number_of_cities
    while len(dist) != number_of_cities - 1 and i < len(graph):
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
            if edge.weight < airport_cost:
                n_airports -= 1
                mst += edge.weight

    return mst + n_airports * airport_cost, n_airports


def solution():

    T = int(input())

    for t in range(T):
        global graph, dist
        graph = []
        dist = []
        N, M, A = map(int, input().split())

        for _ in range(M):
            x, y, z = map(int, input().split())
            graph.append(Triad(x, y, z))

        make_set(N)

        cost, n_airports = kruskal(N, A)

        print('Case #{0}: {1} {2}'.format(t + 1, cost, n_airports))


solution()
```

### 11857 (UVA)

```python
# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2957
#
# Problem: Driving Range (UVA 11857)
#
# Description:
# Find the minimum driving range needed for an electric car to travel
# between any two cities. The car must be able to travel the longest
# edge in the MST (the bottleneck edge).
#
# Input:
# - Multiple test cases until N=M=0
# - N (cities), M (roads)
# - M lines: x, y, z (road from x to y with distance z)
#
# Output:
# - Minimum driving range (maximum edge weight in MST)
# - "IMPOSSIBLE" if cities are not all connected
#
# Approach:
# - Use Kruskal's algorithm to build MST
# - Track the maximum edge weight added to MST
# - This gives the minimum driving range needed


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return str(self.source) + '-' + str(self.target) + ': ' + str(self.weight)


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for _ in range(V + 1)]


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


def kruskal(number_of_cities):
    graph.sort(key=lambda _edge: _edge.weight)
    i = 0
    minimum_distance = 0
    while len(dist) != number_of_cities - 1 and i < len(graph):
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
            minimum_distance = edge.weight

    if len(dist) == number_of_cities - 1:
        return minimum_distance
    else:
        return 'IMPOSSIBLE'


def solution():

    while True:
        global graph, dist
        graph = []
        dist = []
        N, M = map(int, input().split())

        if N == 0 and M == 0:
            break

        for _ in range(M):
            x, y, z = map(int, input().split())
            graph.append(Triad(x, y, z))

        make_set(N)

        minimum_distance = kruskal(N)

        print(minimum_distance)


solution()
```

### 1208 (UVA)

```python
# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3649
#
# Problem: Oreon (UVA 1208)
#
# Description:
# Given a weighted adjacency matrix of cities, find and print all edges
# in the Minimum Spanning Tree. Cities are labeled A, B, C, etc.
# Output edges in sorted order (by source, then by weight).
#
# Input:
# - Number of test cases
# - For each test case:
#   - Number of cities
#   - Adjacency matrix (comma-separated, 0 means no edge)
#
# Output:
# - "Case X:" followed by MST edges in format "A-B W"
#
# Approach:
# - Parse adjacency matrix to create edge list
# - Apply Kruskal's algorithm with edges sorted by (weight, source)
# - Print MST edges with city letters


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for i in range(V + 1)]


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


def kruskal(number_of_cities):
    graph.sort(key=lambda _edge: (_edge.weight, _edge.source))
    i = 0
    while len(dist) != number_of_cities - 1:
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)


def print_MST():
    ans = 0
    for e in dist:
        source = chr(e.source + 65)
        target = chr(e.target + 65)
        print("{0}-{1} {2}".format(source, target, e.weight))
        ans += e.weight


def solution():

    number_of_test_cases = int(input())

    for t in range(number_of_test_cases):
        global graph, dist
        graph = []
        dist = []
        number_of_cities = int(input())
        for i in range(number_of_cities):
            securities = input().split(', ')
            for j in range(i):
                security = int(securities[j])
                if security > 0:
                    graph.append(Triad(j, i, security))
        make_set(number_of_cities)
        kruskal(number_of_cities)
        print('Case {0}:'.format(t + 1))
        print_MST()


solution()
```

### 1235 (UVA)

```python
# Problem from UVA
# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3676
#
# Problem: Anti Brute Force Lock (UVA 1235)
#
# Description:
# A safe has N locks, each with a 4-digit combination. Starting from "0000",
# find the minimum total number of dial rotations to unlock all locks.
# Each dial can rotate in either direction (0->1 or 0->9).
#
# Input:
# - Number of test cases
# - For each test case:
#   - N (number of locks)
#   - N 4-digit lock combinations
#
# Output:
# - Minimum total rotations to unlock all locks
#
# Approach:
# - Model as MST problem: nodes are lock combinations
# - Edge weight = minimum rotations to change one combination to another
# - Find minimum rotation from "0000" to any lock, then MST of all locks
# - Total = initial approach cost + MST weight


class Triad:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight

    def __repr__(self):
        return str(self.source) + '-' + str(self.target) + ': ' + str(self.weight)


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
    global parent, ranks, dist
    parent = [i for i in range(V + 1)]
    ranks = [0 for _ in range(V + 1)]


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


def kruskal(number_of_cities):
    graph.sort(key=lambda _edge: _edge.weight)
    i = 0
    mst = 0
    while len(dist) != number_of_cities - 1:
        edge = graph[i]
        i += 1
        u = find_set(edge.source)
        v = find_set(edge.target)
        if u != v:
            dist.append(edge)
            union_set(u, v)
            mst += edge.weight

    return mst


def calculate_rolls(start, stop):
    rolls = 0
    for i in range(4):
        sta, sto = int(start[i]), int(stop[i])
        rolls += min(abs(sta - sto), 10 - abs(sta - sto))

    return rolls


def solution():

    number_of_test_cases = int(input())

    for t in range(number_of_test_cases):
        global graph, dist
        graph = []
        dist = []
        line = input().split()
        number_of_locks = int(line[0])
        line[0] = '0000'
        initial = 100
        for i in range(1, number_of_locks + 1):
            initial = min(initial, calculate_rolls('0000', line[i]))
        for i in range(1, number_of_locks + 1):
            for j in range(i + 1, number_of_locks + 1):
                source = line[i]
                target = line[j]
                weight = calculate_rolls(source, target)
                graph.append(Triad(i, j, weight))

        make_set(number_of_locks)

        print(kruskal(number_of_locks) + initial)


solution()
```

