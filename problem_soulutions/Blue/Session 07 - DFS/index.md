---
layout: simple
title: "Session 07 - DFS"
permalink: /problem_soulutions/Blue/Session 07 - DFS/
---

# Session 07 - DFS

This session covers Depth-First Search (DFS) algorithm, including graph traversal, connected components, and backtracking problems.

## Problems

### 723D (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/contest/723/problem/D
#
# Problem: Lakes in Berland
#
# Berland is an n×m grid where:
# - '*' represents land
# - '.' represents water
#
# A "lake" is a connected component of water cells that does NOT touch the
# boundary of the grid. Water touching the boundary is considered part of
# the ocean/sea.
#
# The government wants to keep exactly k lakes. They will fill the smallest
# lakes with land to achieve this. Find the minimum number of cells to fill
# and output the resulting map.
#
# Input:
# - Line 1: n m k (grid dimensions, desired number of lakes)
# - Next n lines: The grid
#
# Output:
# - Line 1: Number of cells filled
# - Next n lines: The resulting grid after filling
#
# Approach: DFS to find all lakes (water components not touching boundary),
#           sort by size, fill the smallest ones until k remain


def fill_the_lakes(n, m, k, matrix):

    lakes = []

    dx = [1, 0, -1, 0]
    dy = [0, -1, 0, 1]

    visited = [[False for i in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            is_lake = False
            lake = []

            if matrix[i][j] == '.' and not visited[i][j]:
                if i == 0 or i == n - 1 or j == 0 or j == m - 1:
                    is_lake = False
                else:
                    is_lake = True
                lake.append([i, j])
                s = [[i, j]]
                visited[i][j] = True
                while len(s) > 0:
                    checking_node = s[-1]
                    s.pop()
                    for ll in range(4):
                        neighbor_x = checking_node[0] + dx[ll]
                        neighbor_y = checking_node[1] + dy[ll]
                        if 0 <= neighbor_x < n and 0 <= neighbor_y < m and matrix[neighbor_x][neighbor_y] == '.' and not visited[neighbor_x][neighbor_y]:
                            s.append([neighbor_x, neighbor_y])
                            lake.append([neighbor_x, neighbor_y])
                            visited[neighbor_x][neighbor_y] = True
                            if neighbor_x == 0 or neighbor_x == n - 1 or neighbor_y == 0 or neighbor_y == m - 1:
                                is_lake = False
            if is_lake and len(lake) > 0:
                lakes.append(lake)
    lakes = sorted(lakes, key=lambda _lake:len(_lake))

    to_be_filled = len(lakes) - k

    filled_cells = 0
    for i in range(to_be_filled):
        lake_len = len(lakes[i])
        for j in range(lake_len):
            matrix[lakes[i][j][0]][lakes[i][j][1]] = '*'
            filled_cells += 1

    print(filled_cells)
    for i in range(n):
        print(''.join(matrix[i]))


def solution():
    n, m, k = map(int, input().split())
    matrix = []
    for i in range(n):
        matrix.append(list(input().strip()))

    fill_the_lakes(n, m, k, matrix)


solution()
```

### bishu-and-his-girlfriend (Hackerearth)

```python
#  Problem from Hackerearth
#  https://www.hackerearth.com/fr/practice/algorithms/graphs/depth-first-search/practice-problems/algorithm/bishu-and-his-girlfriend/description/
#
# Problem: Bishu and His Girlfriend
#
# Bishu lives at node 1 of a tree with N nodes. There are Q girls living at
# various nodes. Bishu wants to find the closest girl. If multiple girls are
# at the same minimum distance, choose the one with the smallest node number.
#
# Input:
# - Line 1: N (number of nodes)
# - Next N-1 lines: u v (edges of the tree)
# - Line N+1: Q (number of girls)
# - Next Q lines: Node number where each girl lives
#
# Output: The node number of the closest girl (ties broken by smallest node)
#
# Approach: DFS/BFS from node 1, track distances, find minimum distance girl


def find_girl(N, graph, girls):
    s = []
    visited = [False for i in range(N + 1)]

    roads = [0 for i in range(N + 1)]

    visited[1] = True
    s.append(1)

    selected_girl = N
    selected_road = N

    while len(s) > 0:
        u = s[-1]
        s.pop()

        for v in graph[u]:
            if not visited[v]:
                roads[v] = roads[u] + 1
                if roads[v] <= selected_road:
                    if girls[v]:
                        if roads[v] < selected_road or (roads[v] == selected_road and selected_girl > v):
                            selected_girl = v
                            selected_road = roads[v]
                            visited[v] = True
                    else:
                        visited[v] = True
                        s.append(v)

    return selected_girl


def solution():
    N = int(input())
    roads = []
    graph = [[] for i in range(N + 1)]
    for i in range(N-1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    Q = int(input())
    girls = [0 for i in range(N + 1)]
    for i in range(Q):
        girls[int(input())] = 1

    print(find_girl(N, graph, girls))


solution()
```

### CAM5 (SPOJ)

```python
#  Problem from SPOJ
#  https://www.spoj.com/problems/CAM5/
#
# Problem: CAM5 - Connected Components (Friendship Problem)
#
# Given N people (numbered 0 to N-1) and E friendship pairs, find the number
# of friend groups (connected components). Two people are in the same group
# if they are friends directly or through other friends.
#
# Input:
# - Line 1: T (number of test cases)
# - For each test case:
#   - Line 1: N (number of people)
#   - Line 2: E (number of friendship pairs)
#   - Next E lines: u v (friendship between person u and v)
#
# Output: For each test case, print the number of friend groups
#
# Approach: DFS to count connected components in undirected graph


def calc_disjoint_sets(Ni, graph):
    result = 0
    visited = [False for i in range(Ni)]

    for i in range(Ni):
        if visited[i]:
            continue
        stack = [i]
        visited[i] = True

        while len(stack) > 0:
            u = stack[-1]
            stack.pop()
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        result += 1

    return result


def solution():
    results = []
    while True:
        new_line = input().strip()
        if new_line:
            t = int(new_line)
            break
    for i in range(t):
        while True:
            new_line = input().strip()
            if new_line:
                Ni = int(new_line)
                break
        ei = int(input())
        graph = [[] for jj in range(Ni)]
        for j in range(ei):
            start, end = map(int, input().split())
            graph[start].append(end)
            graph[end].append(start)

        results.append(calc_disjoint_sets(Ni, graph))

    print(*results, sep='\n')


solution()
```

### Dudu (URI)

```python
# Problem from URI
# https://www.urionlinejudge.com.br/judge/en/problems/view/1610
#
# Problem: Dudu - Cycle Detection
#
# Given a directed graph with N nodes and M edges, determine if there is a
# cycle in the graph. Output "SIM" (yes) if a cycle exists, "NAO" (no) otherwise.
#
# Input:
# - Line 1: T (number of test cases)
# - For each test case:
#   - Line 1: N M (nodes, edges)
#   - Next M lines: A B (directed edge from A to B)
#
# Output: For each test case, print "SIM" if cycle exists, "NAO" otherwise
#
# Approach: DFS with cycle detection (check if we revisit a node in current path)


def sim_nao(N, graph):
    global_visited = [False for i in range(N+1)]

    for i in range(1, N + 1):
        if not global_visited[i]:
            visited = [False for l in range(N + 1)]
            s = [i]
            global_visited[i] = True
            visited[i] = True
            path = [0] * (N+1)
            while len(s) > 0:
                u = s[-1]
                s.pop()
                for v in graph[u]:
                    if not visited[v]:
                        visited[v] = True
                        if not global_visited[v]:
                            s.append(v)
                            global_visited[u] = True
                    else:
                        return 'SIM'

    return 'NAO'


def solution():
    results = []
    T = int(input())
    for i in range(T):

        while True:
            new_line = input().strip()
            if new_line:
                N, M = map(int, new_line.split())
                break

        graph = [[] for i in range(N + 1)]
        for j in range(M):
            while True:
                new_line = input().strip()
                if new_line:
                    A, B = map(int, new_line.split())
                    if not B in graph[A]:
                        graph[A].append(B)
                    break
        results.append(sim_nao(N, graph))

    print(*results, sep='\n')


solution()
```

