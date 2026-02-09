---
layout: simple
title: "DFS"
permalink: /problem_soulutions/Blue/Session 07 - DFS/
---

# DFS

Depth-First Search problems involving graph traversal, connected components, cycle detection, and backtracking.

## Problems

### Lakes in Berland

#### Problem Information
- **Source:** [Codeforces 723D](https://codeforces.com/problemset/problem/723/D)
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Berland is an n x m grid where:
- '*' represents land
- '.' represents water

A "lake" is a connected component of water cells that does NOT touch the boundary of the grid. Water touching the boundary is considered part of the ocean/sea.

The government wants to keep exactly k lakes. They will fill the smallest lakes with land to achieve this. Find the minimum number of cells to fill and output the resulting map.

#### Input Format
- Line 1: n m k (grid dimensions, desired number of lakes)
- Next n lines: The grid

#### Output Format
- Line 1: Number of cells filled
- Next n lines: The resulting grid after filling

#### Example
```
Input:
3 3 0
***
*.*
***

Output:
1
***
***
***
```
One lake (center cell). k=0 means fill all lakes. Fill 1 cell.

#### Solution

##### Approach
Use DFS to find all lakes (water components not touching boundary), sort by size, fill the smallest ones until k remain.

##### Python Solution

```python
def fill_the_lakes(n, m, k, matrix):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    visited = [[False] * m for _ in range(n)]
    lakes = []

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == '.' and not visited[i][j]:
                is_lake = i not in (0, n - 1) and j not in (0, m - 1)
                lake = [(i, j)]
                stack = [(i, j)]
                visited[i][j] = True

                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < n and 0 <= ny < m and
                            matrix[nx][ny] == '.' and not visited[nx][ny]):
                            stack.append((nx, ny))
                            lake.append((nx, ny))
                            visited[nx][ny] = True
                            if nx in (0, n - 1) or ny in (0, m - 1):
                                is_lake = False

                if is_lake and lake:
                    lakes.append(lake)

    # Sort lakes by size and fill smallest ones
    lakes.sort(key=len)
    to_fill = len(lakes) - k
    filled_cells = 0

    for lake in lakes[:to_fill]:
        for x, y in lake:
            matrix[x][y] = '*'
            filled_cells += 1

    print(filled_cells)
    for row in matrix:
        print(''.join(row))

def solution():
    n, m, k = map(int, input().split())
    matrix = [list(input().strip()) for _ in range(n)]
    fill_the_lakes(n, m, k, matrix)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * m) for DFS traversal plus O(L log L) for sorting lakes
- **Space Complexity:** O(n * m) for visited array and lake storage

---

### Bishu and His Girlfriend

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Bishu lives at node 1 of a tree with N nodes. There are Q girls living at various nodes. Bishu wants to find the closest girl. If multiple girls are at the same minimum distance, choose the one with the smallest node number.

#### Input Format
- Line 1: N (number of nodes)
- Next N-1 lines: u v (edges of the tree)
- Line N+1: Q (number of girls)
- Next Q lines: Node number where each girl lives

#### Output Format
The node number of the closest girl (ties broken by smallest node).

#### Example
```
Input:
5
1 2
1 3
2 4
2 5
2
4
5

Output:
4
```
Tree: 1-2-4, 1-2-5, 1-3. Girls at nodes 4 and 5 (both distance 2 from node 1). Node 4 < 5, so output 4.

#### Solution

##### Approach
DFS from node 1, track distances, find minimum distance girl with smallest node number as tiebreaker.

##### Python Solution

```python
def find_girl(n, graph, girls):
    visited = [False] * (n + 1)
    dist = [0] * (n + 1)
    visited[1] = True
    stack = [1]

    best_girl = n
    best_dist = n

    while stack:
        u = stack.pop()

        for v in graph[u]:
            if not visited[v]:
                dist[v] = dist[u] + 1
                visited[v] = True

                if dist[v] <= best_dist:
                    if girls[v]:
                        if dist[v] < best_dist or v < best_girl:
                            best_girl = v
                            best_dist = dist[v]
                    else:
                        stack.append(v)

    return best_girl

def solution():
    n = int(input())
    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    q = int(input())
    girls = [False] * (n + 1)
    for _ in range(q):
        girls[int(input())] = True

    print(find_girl(n, graph, girls))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N) for DFS traversal of the tree
- **Space Complexity:** O(N) for graph and auxiliary arrays

---

### CAM5 - Connected Components

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 227ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given N people (numbered 0 to N-1) and E friendship pairs, find the number of friend groups (connected components). Two people are in the same group if they are friends directly or through other friends.

#### Input Format
- Line 1: T (number of test cases)
- For each test case:
  - Line 1: N (number of people)
  - Line 2: E (number of friendship pairs)
  - Next E lines: u v (friendship between person u and v)

#### Output Format
For each test case, print the number of friend groups.

#### Example
```
Input:
2
5
3
0 1
1 2
3 4
4
2
0 1
2 3

Output:
2
2
```
First test case: 5 people, 3 friendships. People 0-1-2 form one group, people 3-4 form another. Two groups.
Second test case: 4 people, 2 friendships. People 0-1 form one group, people 2-3 form another. Two groups.

#### Solution

##### Approach
DFS to count connected components in an undirected graph. Start DFS from each unvisited node and increment the component count.

##### Python Solution

```python
def count_components(n, graph):
    visited = [False] * n
    components = 0

    for start in range(n):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True

        while stack:
            u = stack.pop()
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)

        components += 1

    return components

def solution():
    results = []

    while True:
        line = input().strip()
        if line:
            t = int(line)
            break

    for _ in range(t):
        while True:
            line = input().strip()
            if line:
                n = int(line)
                break

        e = int(input())
        graph = [[] for _ in range(n)]

        for _ in range(e):
            u, v = map(int, input().split())
            graph[u].append(v)
            graph[v].append(u)

        results.append(count_components(n, graph))

    print('\n'.join(map(str, results)))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N + E) for DFS traversal
- **Space Complexity:** O(N + E) for graph storage

---

### Dudu - Cycle Detection

#### Problem Information
- **Source:** URI 1610
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a directed graph with N nodes and M edges, determine if there is a cycle in the graph. Output "SIM" (yes) if a cycle exists, "NAO" (no) otherwise.

#### Input Format
- Line 1: T (number of test cases)
- For each test case:
  - Line 1: N M (nodes, edges)
  - Next M lines: A B (directed edge from A to B)

#### Output Format
For each test case, print "SIM" if cycle exists, "NAO" otherwise.

#### Example
```
Input:
2
3 3
1 2
2 3
3 1
3 2
1 2
2 3

Output:
SIM
NAO
```
First test case: 3 nodes with edges 1->2, 2->3, 3->1 forming a cycle. Output "SIM".
Second test case: 3 nodes with edges 1->2, 2->3. No cycle exists. Output "NAO".

#### Solution

##### Approach
DFS with cycle detection. Track visited nodes in the current DFS path. If we revisit a node already in the current path, a cycle exists.

##### Python Solution

```python
def has_cycle(n, graph):
    # States: 0 = unvisited, 1 = in current path, 2 = fully processed
    state = [0] * (n + 1)

    for start in range(1, n + 1):
        if state[start] != 0:
            continue

        stack = [(start, False)]  # (node, processed)

        while stack:
            node, processed = stack.pop()

            if processed:
                state[node] = 2
                continue

            if state[node] == 1:
                return 'SIM'

            if state[node] == 2:
                continue

            state[node] = 1
            stack.append((node, True))

            for neighbor in graph[node]:
                if state[neighbor] == 1:
                    return 'SIM'
                if state[neighbor] == 0:
                    stack.append((neighbor, False))

    return 'NAO'

def solution():
    results = []
    t = int(input())

    for _ in range(t):
        while True:
            line = input().strip()
            if line:
                n, m = map(int, line.split())
                break

        graph = [[] for _ in range(n + 1)]

        for _ in range(m):
            while True:
                line = input().strip()
                if line:
                    a, b = map(int, line.split())
                    if b not in graph[a]:
                        graph[a].append(b)
                    break

        results.append(has_cycle(n, graph))

    print('\n'.join(results))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N + M) for DFS
- **Space Complexity:** O(N + M) for graph and visited arrays
