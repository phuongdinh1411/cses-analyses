---
layout: simple
title: "Session 12 - Floyd-Warshall"
permalink: /problem_soulutions/Blue/Session 12 - Floyd-Warshall/
---

# Session 12 - Floyd-Warshall

This session covers the Floyd-Warshall algorithm for finding all-pairs shortest paths in weighted graphs.

## Problems

### Maximum Weight Composition

#### Problem Information
- **Source:** CodeChef
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given N intervals with start position, end position, and cost, find the maximum total cost by selecting non-overlapping intervals. An interval from [si, ei] must end before the next one starts.

#### Input Format
- T: number of test cases
- For each test case:
  - N: number of intervals
  - N lines with si ei ci: start, end, and cost of interval

#### Output Format
- Maximum total cost achievable with non-overlapping intervals

#### Solution

##### Approach
Use dynamic programming approach (simplified from Floyd-Warshall concept). For each endpoint, compute maximum cost considering all intervals ending there. mmax[x] = max(mmax[x], graph[xx][x] + mmax[xx]) for all xx < x. Essentially an interval scheduling maximization problem.

##### Python Solution

```python
import sys

INF = int(1e9)


def floyd_warshall(M, graph):
    dist = [[0] * M for i in range(M)]
    for i in range(M):
        for j in range(M):
            dist[i][j] = graph[i][j]

    for x in range(5):
        for k in range(M):
            for i in range(M):
                for j in range(M):
                    if i <= k <= j and dist[i][j] < dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

    max_comp = 0
    for i in range(M):
        for j in range(M):
            if max_comp < dist[i][j]:
                max_comp = dist[i][j]

    return max_comp


def solution():
    T = int(input().strip())
    M = 49
    for i in range(T):
        graph = [[0] * M for x in range(M)]
        N = int(input().strip())
        e_max = 0

        for j in range(N):
            si, ei, ci = map(int, input().strip().split())
            if ei > e_max:
                e_max = ei
            if ci > graph[si][ei]:
                graph[si][ei] = ci

        mmax = [0 for x in range(M)]
        for x in range(1, e_max + 1):
            m = 0
            for xx in range(x):
                if m < graph[xx][x] + mmax[xx]:
                    m = graph[xx][x] + mmax[xx]
                mmax[x] = m

        print(mmax[e_max])


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * M^2) where M is maximum endpoint value
- **Space Complexity:** O(M^2)

---

### Greg and Graph

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a weighted directed graph and an order of vertex deletions, compute the sum of all shortest paths after each deletion (in reverse, after each vertex is added back). Process deletions in reverse order to build the graph.

#### Input Format
- N: number of vertices
- N x N adjacency matrix with edge weights
- Deletion order: sequence of N vertices to be deleted

#### Output Format
- N integers: sum of all shortest paths after adding vertices in reverse deletion order (i.e., before each deletion in original order)

#### Solution

##### Approach
Reverse the deletion order to process as additions. Use incremental Floyd-Warshall: when adding vertex k, update all pairs (i,j) considering k as intermediate vertex. After adding each vertex, sum all current shortest paths. Output results in reverse (corresponding to original deletion order).

##### Python Solution

```python
INF = float(1e9)


def floyd_warshall(N, matrix, del_list):

    ans = [0 for i in range(N + 1)]

    for k in range(N, 0, -1):
        c = del_list[k]
        for i in range(k + 1, N + 1):
            a = del_list[i]
            for j in range(k, N + 1):
                b = del_list[j]
                matrix[c][a] = min(matrix[c][a], matrix[c][b] + matrix[b][a])
                matrix[a][c] = min(matrix[a][c], matrix[a][b] + matrix[b][c])

        for i in range(k, N + 1):
            a = del_list[i]
            for j in range(k, N + 1):
                b = del_list[j]
                if a == b:
                    continue
                matrix[a][b] = min(matrix[a][b], matrix[a][c] + matrix[c][b])

        for i in range(k, N + 1):
            a = del_list[i]
            for j in range(k, N + 1):
                b = del_list[j]
                ans[k] += matrix[a][b]

    return ans[1:N+1]


def solution():
    N = int(input().strip())
    matrix = [[]]
    for i in range(N):
        new_line = [0] + list(map(int, input().strip().split()))
        matrix.append(new_line)

    del_list = [0] + list(map(int, input().strip().split()))

    print(*floyd_warshall(N, matrix, del_list), sep=' ')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N^3)
- **Space Complexity:** O(N^2)

---

### Arbitrage

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given currency exchange rates between different currencies, determine if arbitrage is possible. Arbitrage means starting with some currency and exchanging through a sequence of currencies to end up with more of the original currency than you started with.

#### Input Format
- Multiple test cases until n=0
- For each test case:
  - n: number of currencies
  - n currency names
  - m: number of exchange rates
  - m lines: currency1 rate currency2 (exchange currency1 to currency2 at given rate)

#### Output Format
- "Case X: Yes" if arbitrage is possible, "Case X: No" otherwise

#### Solution

##### Approach
Use modified Floyd-Warshall for product maximization instead of sum minimization. matrix[i][j] = max(matrix[i][j], matrix[i][k] * matrix[k][j]). If any diagonal element > 1 after algorithm, arbitrage exists (cycle with gain).

##### Python Solution

```python
INF = float(1e9)


def floyd_warshall(M, matrix):

    for k in range(M):
        for i in range(M):
            for j in range(M):
                if matrix[i][j] < matrix[i][k] * matrix[k][j]:
                    matrix[i][j] = matrix[i][k] * matrix[k][j]
    for i in range(M):
        if matrix[i][i] > 1:
            return 'Yes'

    return 'No'


def solution():
    n_case = 1
    while True:
        line = input().strip()
        while not line:
            line = input().strip()
        M = int(line)
        if M == 0:
            break

        my_dict = {}
        for i in range(M):
            my_dict[input().strip()] = i

        exchanges = int(input().strip())
        matrix = [[0.0] * M for i in range(M)]
        for i in range(exchanges):
            c1, rate, c2 = map(str, input().strip().split())
            matrix[my_dict[c1]][my_dict[c2]] = float(rate)

        print('Case ' + str(n_case) + ': ' + floyd_warshall(M, matrix))
        n_case += 1


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N^3) per test case
- **Space Complexity:** O(N^2)

---

### Social Network

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given a social network represented as a friendship matrix, find the person who can make the most new friends through existing friends (friends-of-friends). A person can become friends with someone who is a friend of their friend but not already their direct friend.

#### Input Format
- T: number of test cases
- For each test case:
  - M x M matrix where 'Y' means friendship exists, 'N' means no friendship

#### Output Format
- For each test case: person_index max_new_friends (0-indexed person who gains most new friends through friend-of-friend connections)

#### Solution

##### Approach
Use modified Floyd-Warshall concept for transitive closure. For each person i, count people j where i and j are not friends directly but share a common friend k (matrix[i][k]='Y' and matrix[k][j]='Y'). Track which person gains the most potential new friends.

##### Python Solution

```python
def floyd_warshall(M, matrix):
    dist = [[False] * M for i in range(M)]
    for i in range(M):
        n_friend = 0
        for j in range(M):
            if matrix[i][j] == 'Y':
                n_friend += 1
                dist[i][j] = True

    n_more_friends = [0 for i in range(M)]
    for k in range(M):
        for i in range(M):
            for j in range(M):
                if not dist[i][j] and i != j and matrix[i][k] == 'Y' and matrix[k][j] == 'Y':
                    dist[i][j] = True
                    n_more_friends[i] += 1

    max_new_friends = n_more_friends[0]
    most_pop_person = 0
    for i in range(1, M):
        if n_more_friends[i] > max_new_friends:
            max_new_friends = n_more_friends[i]
            most_pop_person = i
    print(most_pop_person, max_new_friends)


def solution():
    T = int(input())
    for i in range(T):
        matrix = []
        first_line = input().strip()
        M = len(first_line)
        matrix.append(first_line)
        for j in range(M - 1):
            matrix.append(input().strip())

        floyd_warshall(M, matrix)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * M^3)
- **Space Complexity:** O(M^2)

---

### Meeting Prof. Miguel

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Two people (young and old) want to meet. Each has their own transportation network (some roads are unidirectional, some bidirectional). Find meeting points where the total travel cost is minimized. Output the minimum cost and all cities where they can meet with that cost.

#### Input Format
- Multiple test cases until N=0
- For each test case:
  - N: number of streets
  - N lines: age direction city1 city2 cost
    - age: Y (young) or O (old)
    - direction: U (unidirectional) or B (bidirectional)
  - Start positions: young_start old_start

#### Output Format
- Minimum total cost and meeting city/cities, or "You will never meet."

#### Solution

##### Approach
Build separate graphs for young and old person. Run Floyd-Warshall on both graphs. Find city minimizing young_dist[start_y][city] + old_dist[start_o][city]. Output all cities achieving minimum cost.

##### Python Solution

```python
INF = float(1e9)
MAXN = 26


def floyd_warshall(young_graph, old_graph, start_young, start_old):
    for k in range(MAXN):
        for i in range(MAXN):
            for j in range(MAXN):
                young_graph[i][j] = min(young_graph[i][j], young_graph[i][k] + young_graph[k][j])
                old_graph[i][j] = min(old_graph[i][j], old_graph[i][k] + old_graph[k][j])

    min_dist, min_i = INF, -1
    for i in range(MAXN):
        d = young_graph[start_young][i] + old_graph[start_old][i]
        if d < min_dist:
            min_dist, min_i = d, i
    if min_dist >= INF:
        print('You will never meet.')
    else:
        flag = False
        for i in range(MAXN):
            d = young_graph[start_young][i] + old_graph[start_old][i]
            if d == min_dist:
                if flag:
                    print(' {:s}'.format(chr(ord('A') + i)), end='')
                else:
                    flag = True
                    print('{:d} {:s}'.format(min_dist, chr(ord('A') + i)), end='')
        print()


def solution():
    counte = 1
    while True:
        N = int(input().strip())
        if N == 0:
            break

        young_graph = [[INF] * MAXN for i in range(MAXN)]
        old_graph = [[INF] * MAXN for i in range(MAXN)]

        for i in range(MAXN):
            young_graph[i][i] = old_graph[i][i] = 0

        for i in range(N):
            line = list(map(str, input().strip().split()))

            if line[0] == 'Y':
                x = ord(line[2]) - 65
                y = ord(line[3]) - 65
                if x != y:
                    young_graph[x][y] = int(line[-1])
                    if line[1] == 'B':
                        young_graph[y][x] = int(line[-1])
            else:
                x = ord(line[2]) - 65
                y = ord(line[3]) - 65
                if x != y:
                    old_graph[x][y] = int(line[-1])
                    if line[1] == 'B':
                        old_graph[y][x] = int(line[-1])

        start_young, start_old = map(lambda x: ord(x) - 65, input().strip().split())

        floyd_warshall(young_graph, old_graph, start_young, start_old)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(26^3) = O(1) per test case (constant alphabet size)
- **Space Complexity:** O(26^2) = O(1)

---

### Asterix and Obelix

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Asterix and Obelix travel between cities. Each city has a "feast cost" that Obelix must pay when visiting. The total trip cost is the sum of road costs plus the maximum feast cost of any city visited on the path. Find minimum total cost for queries between city pairs.

#### Input Format
- Multiple test cases until C=0
- For each test case:
  - C R Q: cities, roads, queries
  - C feast costs for each city
  - R lines with c1 c2 d: road between c1 and c2 with distance d
  - Q lines with c1 c2: query for minimum cost from c1 to c2

#### Output Format
- For each case: "Case #X" followed by minimum costs for each query (-1 if impossible)

#### Solution

##### Approach
Use modified Floyd-Warshall tracking both path distance and maximum feast cost. For each intermediate vertex k, update if new path has lower total cost (distance + max_feast_cost). Run multiple iterations to ensure convergence.

##### Python Solution

```python
import sys

INF = int(1e9)


def floyd_warshall(M, graph, case_number, queries, feast_cost):
    dist = [[INF] * M for i in range(M)]
    worst_feast_costs = [[INF] * M for i in range(M)]
    for i in range(M):
        worst_feast_costs[i][i] = feast_cost[i]
    for i in range(M):
        for j in range(M):
            dist[i][j] = graph[i][j]
            max_feast_cost = max(worst_feast_costs[i][i], worst_feast_costs[j][j])
            worst_feast_costs[i][j] = max_feast_cost
            worst_feast_costs[j][i] = max_feast_cost

    for t in range(2):
        for k in range(M):
            for i in range(M):
                for j in range(M):
                    max_feast_cost = max(worst_feast_costs[i][k], worst_feast_costs[k][j])
                    if dist[i][j] + worst_feast_costs[i][j] > dist[i][k] + dist[k][j] + max_feast_cost:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        worst_feast_costs[i][j] = max_feast_cost

    print('Case #' + str(case_number))
    for i in range(len(queries)):
        cost = dist[queries[i][0] - 1][queries[i][1] - 1]
        if cost == INF:
            print(-1)
        else:
            print(cost + worst_feast_costs[queries[i][0] - 1][queries[i][1] - 1])


def solution():
    n_case = 1
    while True:

        line = input().strip()
        while not line:
            line = input().strip()
        C, R, Q = map(int, line.split())
        if C == 0:
            break
        if n_case != 1:
            print()
        feast_cost = list(map(int, input().strip().split()))

        graph = [[INF] * C for i in range(C)]
        for i in range(R):
            c1, c2, d = map(int, input().strip().split())
            graph[c1 - 1][c2 - 1] = d
            graph[c2 - 1][c1 - 1] = d

        queries = []
        for i in range(Q):
            query = list(map(int, input().strip().split()))
            queries.append(query)

        floyd_warshall(C, graph, n_case, queries, feast_cost)
        n_case += 1


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(C^3) per test case
- **Space Complexity:** O(C^2)

---

### Thunder Mountain

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given towns with 2D coordinates, two towns can communicate directly if their distance is at most 10 units. Find the maximum shortest path between any pair of towns (network diameter). If not all towns are connected, output "Send Kurdy" (network needs a messenger).

#### Input Format
- T: number of test cases
- For each test case:
  - N: number of towns
  - N lines with x y: coordinates of each town

#### Output Format
- "Case #X:" followed by the network diameter (maximum shortest path) or "Send Kurdy" if not all towns are reachable

#### Solution

##### Approach
Build graph: connect towns within 10 units distance. Floyd-Warshall for all-pairs shortest paths. Find maximum of all shortest paths (diameter). If any pair is unreachable (INF), output "Send Kurdy".

##### Python Solution

```python
import math

INF = float(1e9)


def floyd_warshall(M, towns):

    graph = [[INF] * M for i in range(M)]
    for i in range(M):
        for j in range(i + 1, M):
            pow2_dist = math.pow((towns[i][0] - towns[j][0]), 2) + math.pow((towns[i][1] - towns[j][1]), 2)
            if pow2_dist <= 100:
                graph[i][j] = math.sqrt(pow2_dist)
                graph[j][i] = math.sqrt(pow2_dist)

    for i in range(M):
        graph[i][i] = 0

    dist = [[INF] * M for i in range(M)]
    for i in range(M):
        for j in range(M):
            dist[i][j] = graph[i][j]

    for k in range(M):
        for i in range(M):
            for j in range(M):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    max_range = 0
    for i in range(M):
        for j in range(M):
            if dist[i][j] == INF:
                return 0
            if max_range < dist[i][j]:
                max_range = dist[i][j]

    return max_range


def solution():
    T = int(input().strip())
    for t in range(T):
        M = int(input().strip())
        towns = []
        for i in range(M):
            x, y = map(int, input().strip().split())
            towns.append([x, y])

        if t != 0:
            print()
        print('Case #' + str(t + 1) + ':')
        result = floyd_warshall(M, towns)
        if result > 0:
            print("{:.4f}".format(result))
        else:
            print('Send Kurdy')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * N^3)
- **Space Complexity:** O(N^2)

---

### Risk

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

The game of Risk has 20 countries. Given the adjacency information for each country, answer queries about the minimum number of borders (edges) that must be crossed to get from one country to another.

#### Input Format
- Multiple test sets (19 lines of adjacency data per set)
- Line i: number of neighbors of country i+1, followed by neighbor numbers
- After adjacency data: number of queries
- Query lines: source destination

#### Output Format
- "Test Set #X" followed by formatted output for each query: "source to destination: distance"

#### Solution

##### Approach
Build undirected graph with 20 nodes from adjacency lists. Floyd-Warshall for all-pairs shortest paths (all edges have weight 1). Answer queries using precomputed distances.

##### Python Solution

```python
import sys

INF = int(1e9)


def floyd_warshall(M, graph, case_number, queries):
    dist = [[INF] * M for i in range(M)]
    for i in range(M):
        for j in range(M):
            dist[i][j] = graph[i][j]

    for k in range(M):
        for i in range(M):
            for j in range(M):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    print('Test Set #' + str(case_number))
    for i in range(len(queries)):
        print("{:2d} to {:2d}: {:d}".format(queries[i][0], queries[i][1], dist[queries[i][0] - 1][queries[i][1] - 1]).rstrip('0'))


def solution():
    n_case = 1
    while True:
        M = 20
        graph = [[INF] * M for i in range(M)]
        for i in range(M - 1):
            try:
                line = list(map(int, input().strip().split()))
            except:
                return
            if len(line) == 0:
                return
            n_neighbor = line[0]
            for j in range(1, n_neighbor + 1):
                graph[i][line[j] - 1] = 1
                graph[line[j] - 1][i] = 1

        n_queries = int(input())
        queries = []
        for i in range(n_queries):
            query = list(map(int, input().strip().split()))
            queries.append(query)

        floyd_warshall(M, graph, n_case, queries)
        print()
        n_case += 1


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(20^3) = O(1) per test case (constant graph size)
- **Space Complexity:** O(20^2) = O(1)
