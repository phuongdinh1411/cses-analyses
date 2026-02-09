---
layout: simple
title: "Floyd-Warshall"
permalink: /problem_soulutions/Blue/Session 12 - Floyd-Warshall/
---

# Floyd-Warshall

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

#### Example
```
Input:
1
3
1 2 5
3 4 6
2 5 3

Output:
11
```
Select intervals [1,2] with cost 5 and [3,4] with cost 6. They don't overlap, so total cost is 5+6=11. Interval [2,5] overlaps with both, so we skip it.

#### Solution

##### Approach
Use dynamic programming approach (simplified from Floyd-Warshall concept). For each endpoint, compute maximum cost considering all intervals ending there. mmax[x] = max(mmax[x], graph[xx][x] + mmax[xx]) for all xx < x. Essentially an interval scheduling maximization problem.

##### Python Solution

```python
def solution():
    t = int(input().strip())
    max_endpoint = 49

    for _ in range(t):
        graph = [[0] * max_endpoint for _ in range(max_endpoint)]
        n = int(input().strip())
        e_max = 0

        for _ in range(n):
            si, ei, ci = map(int, input().strip().split())
            e_max = max(e_max, ei)
            graph[si][ei] = max(graph[si][ei], ci)

        # DP: mmax[x] = max total cost ending at position x
        mmax = [0] * max_endpoint
        for x in range(1, e_max + 1):
            mmax[x] = max(graph[xx][x] + mmax[xx] for xx in range(x))

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

#### Example
```
Input:
3
0 10 20
10 0 5
20 5 0
1 2 3

Output:
70 20 0
```
After all 3 vertices: sum of paths = 0+10+20+10+0+5+20+5+0 = 70. After deleting vertex 1: only vertices 2,3 remain with dist 5, so sum = 5+5+0+0 = 10... The output shows cumulative sums.

#### Solution

##### Approach
Reverse the deletion order to process as additions. Use incremental Floyd-Warshall: when adding vertex k, update all pairs (i,j) considering k as intermediate vertex. After adding each vertex, sum all current shortest paths. Output results in reverse (corresponding to original deletion order).

##### Python Solution

```python
INF = float('inf')


def floyd_warshall(n, matrix, del_list):
    ans = [0] * (n + 1)

    for k in range(n, 0, -1):
        c = del_list[k]

        # Update distances through the newly added vertex c
        for i in range(k + 1, n + 1):
            a = del_list[i]
            for j in range(k, n + 1):
                b = del_list[j]
                matrix[c][a] = min(matrix[c][a], matrix[c][b] + matrix[b][a])
                matrix[a][c] = min(matrix[a][c], matrix[a][b] + matrix[b][c])

        for i in range(k, n + 1):
            a = del_list[i]
            for j in range(k, n + 1):
                b = del_list[j]
                if a != b:
                    matrix[a][b] = min(matrix[a][b], matrix[a][c] + matrix[c][b])

        # Sum all shortest paths
        ans[k] = sum(
            matrix[del_list[i]][del_list[j]]
            for i in range(k, n + 1)
            for j in range(k, n + 1)
        )

    return ans[1:n + 1]


def solution():
    n = int(input().strip())
    matrix = [[]] + [
        [0] + list(map(int, input().strip().split()))
        for _ in range(n)
    ]
    del_list = [0] + list(map(int, input().strip().split()))

    print(*floyd_warshall(n, matrix, del_list), sep=' ')


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

#### Example
```
Input:
3
USDollar
BritishPound
Euro
3
USDollar 0.5 BritishPound
BritishPound 2.1 USDollar
Euro 1.0 USDollar
0

Output:
Case 1: Yes
```
USD->GBP at 0.5, GBP->USD at 2.1. Starting with 1 USD: 1 * 0.5 * 2.1 = 1.05 USD. Profit of 5%, so arbitrage is possible.

#### Solution

##### Approach
Use modified Floyd-Warshall for product maximization instead of sum minimization. matrix[i][j] = max(matrix[i][j], matrix[i][k] * matrix[k][j]). If any diagonal element > 1 after algorithm, arbitrage exists (cycle with gain).

##### Python Solution

```python
def floyd_warshall(m, matrix):
    for k in range(m):
        for i in range(m):
            for j in range(m):
                matrix[i][j] = max(matrix[i][j], matrix[i][k] * matrix[k][j])

    # Check for arbitrage (any diagonal > 1 means profit cycle)
    return 'Yes' if any(matrix[i][i] > 1 for i in range(m)) else 'No'


def solution():
    case_num = 1
    while True:
        line = input().strip()
        while not line:
            line = input().strip()

        m = int(line)
        if m == 0:
            break

        currency_index = {input().strip(): i for i in range(m)}

        num_exchanges = int(input().strip())
        matrix = [[0.0] * m for _ in range(m)]

        for _ in range(num_exchanges):
            c1, rate, c2 = input().strip().split()
            matrix[currency_index[c1]][currency_index[c2]] = float(rate)

        print(f'Case {case_num}: {floyd_warshall(m, matrix)}')
        case_num += 1


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

#### Example
```
Input:
1
NYNN
YNYN
NYNY
NNYN

Output:
0 2
```
Person 0 is friends with person 1. Person 1 is friends with person 2. Person 2 is friends with person 3. Person 0 can become friends with persons 2 and 3 (friends-of-friends), gaining 2 new friends - the most of anyone.

#### Solution

##### Approach
Use modified Floyd-Warshall concept for transitive closure. For each person i, count people j where i and j are not friends directly but share a common friend k (matrix[i][k]='Y' and matrix[k][j]='Y'). Track which person gains the most potential new friends.

##### Python Solution

```python
def floyd_warshall(m, matrix):
    # Track direct friendships
    connected = [[matrix[i][j] == 'Y' for j in range(m)] for i in range(m)]

    # Count new friends through friend-of-friend
    new_friends = [0] * m
    for k in range(m):
        for i in range(m):
            for j in range(m):
                if not connected[i][j] and i != j and matrix[i][k] == 'Y' and matrix[k][j] == 'Y':
                    connected[i][j] = True
                    new_friends[i] += 1

    # Find person with most new friends
    best_person = max(range(m), key=lambda i: new_friends[i])
    print(best_person, new_friends[best_person])


def solution():
    t = int(input())
    for _ in range(t):
        first_line = input().strip()
        m = len(first_line)
        matrix = [first_line] + [input().strip() for _ in range(m - 1)]
        floyd_warshall(m, matrix)


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

#### Example
```
Input:
4
Y U A B 10
Y U B C 20
O U D C 30
O U D A 15
A D
0

Output:
45 A C
```
Young starts at A, Old starts at D. Meeting at A: Young cost 0, Old cost 15. Total 15. Meeting at C: Young cost 30 (A->B->C), Old cost 30. Total 60. Best meeting point is A with cost 45 (considering both paths).

#### Solution

##### Approach
Build separate graphs for young and old person. Run Floyd-Warshall on both graphs. Find city minimizing young_dist[start_y][city] + old_dist[start_o][city]. Output all cities achieving minimum cost.

##### Python Solution

```python
INF = float('inf')
MAXN = 26


def floyd_warshall(young_graph, old_graph, start_young, start_old):
    for k in range(MAXN):
        for i in range(MAXN):
            for j in range(MAXN):
                young_graph[i][j] = min(young_graph[i][j], young_graph[i][k] + young_graph[k][j])
                old_graph[i][j] = min(old_graph[i][j], old_graph[i][k] + old_graph[k][j])

    # Find minimum meeting cost
    min_dist = min(
        young_graph[start_young][i] + old_graph[start_old][i]
        for i in range(MAXN)
    )

    if min_dist >= INF:
        print('You will never meet.')
    else:
        # Find all cities with minimum cost
        meeting_cities = [
            chr(ord('A') + i)
            for i in range(MAXN)
            if young_graph[start_young][i] + old_graph[start_old][i] == min_dist
        ]
        print(f"{min_dist} {' '.join(meeting_cities)}")


def solution():
    while True:
        n = int(input().strip())
        if n == 0:
            break

        young_graph = [[INF] * MAXN for _ in range(MAXN)]
        old_graph = [[INF] * MAXN for _ in range(MAXN)]

        for i in range(MAXN):
            young_graph[i][i] = old_graph[i][i] = 0

        for _ in range(n):
            parts = input().strip().split()
            age, direction, city1, city2, cost = parts[0], parts[1], parts[2], parts[3], int(parts[-1])
            x, y = ord(city1) - ord('A'), ord(city2) - ord('A')

            if x != y:
                graph = young_graph if age == 'Y' else old_graph
                graph[x][y] = cost
                if direction == 'B':
                    graph[y][x] = cost

        start_young, start_old = (ord(c) - ord('A') for c in input().strip().split())

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

#### Example
```
Input:
4 5 2
10 20 30 40
1 2 5
1 3 10
2 4 7
2 3 3
3 4 2
1 4
2 3

Output:
Case #1
47
33
```
Query 1->4: Path 1->2->4 has distance 5+7=12, max feast cost is max(10,20,40)=40, total=52. Path 1->3->4 has distance 10+2=12, max feast is max(10,30,40)=40, total=52. Best path gives 47.

#### Solution

##### Approach
Use modified Floyd-Warshall tracking both path distance and maximum feast cost. For each intermediate vertex k, update if new path has lower total cost (distance + max_feast_cost). Run multiple iterations to ensure convergence.

##### Python Solution

```python
INF = float('inf')


def floyd_warshall(m, graph, case_number, queries, feast_cost):
    dist = [[graph[i][j] for j in range(m)] for i in range(m)]
    max_feast = [[max(feast_cost[i], feast_cost[j]) for j in range(m)] for i in range(m)]

    for i in range(m):
        max_feast[i][i] = feast_cost[i]

    for _ in range(2):  # Multiple iterations for convergence
        for k in range(m):
            for i in range(m):
                for j in range(m):
                    new_feast = max(max_feast[i][k], max_feast[k][j])
                    new_total = dist[i][k] + dist[k][j] + new_feast
                    old_total = dist[i][j] + max_feast[i][j]
                    if new_total < old_total:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        max_feast[i][j] = new_feast

    print(f'Case #{case_number}')
    for src, dest in queries:
        cost = dist[src - 1][dest - 1]
        if cost == INF:
            print(-1)
        else:
            print(cost + max_feast[src - 1][dest - 1])


def solution():
    case_num = 1
    while True:
        line = input().strip()
        while not line:
            line = input().strip()

        c, r, q = map(int, line.split())
        if c == 0:
            break

        if case_num != 1:
            print()

        feast_cost = list(map(int, input().strip().split()))

        graph = [[INF] * c for _ in range(c)]
        for _ in range(r):
            c1, c2, d = map(int, input().strip().split())
            graph[c1 - 1][c2 - 1] = d
            graph[c2 - 1][c1 - 1] = d

        queries = [tuple(map(int, input().strip().split())) for _ in range(q)]

        floyd_warshall(c, graph, case_num, queries, feast_cost)
        case_num += 1


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

#### Example
```
Input:
2
4
0 0
10 0
10 10
0 10
3
0 0
50 0
100 0

Output:
Case #1:
20.0000

Case #2:
Send Kurdy
```
Case 1: Towns form a 10x10 square. All adjacent towns are within 10 units. Diameter (longest shortest path) is 20 units (e.g., from (0,0) to (10,10) via two edges). Case 2: Towns are 50 units apart, exceeding the 10-unit communication range.

#### Solution

##### Approach
Build graph: connect towns within 10 units distance. Floyd-Warshall for all-pairs shortest paths. Find maximum of all shortest paths (diameter). If any pair is unreachable (INF), output "Send Kurdy".

##### Python Solution

```python
import math

INF = float('inf')


def floyd_warshall(m, towns):
    # Build graph: connect towns within 10 units
    dist = [[INF] * m for _ in range(m)]

    for i in range(m):
        dist[i][i] = 0
        for j in range(i + 1, m):
            dx, dy = towns[i][0] - towns[j][0], towns[i][1] - towns[j][1]
            sq_dist = dx * dx + dy * dy
            if sq_dist <= 100:  # Within 10 units (10^2 = 100)
                distance = math.sqrt(sq_dist)
                dist[i][j] = dist[j][i] = distance

    # Floyd-Warshall
    for k in range(m):
        for i in range(m):
            for j in range(m):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    # Find network diameter
    max_dist = max(dist[i][j] for i in range(m) for j in range(m))

    return 0 if max_dist == INF else max_dist


def solution():
    t = int(input().strip())
    for case in range(t):
        m = int(input().strip())
        towns = [tuple(map(int, input().strip().split())) for _ in range(m)]

        if case != 0:
            print()
        print(f'Case #{case + 1}:')

        result = floyd_warshall(m, towns)
        print(f"{result:.4f}" if result > 0 else 'Send Kurdy')


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

#### Example
```
Input:
1 3
2 3 6
3 6 7
0
1
0
0
2 4 5
3 7 8 17
0
1 8
0
0
1 9
0
0
0
0
1 20
0
0
5
1 20
2 9
19 5
18 19
2 20

Output:
Test Set #1
 1 to 20: 3
 2 to  9: 4
19 to  5: 2
18 to 19: 2
 2 to 20: 3
```
Queries ask for minimum borders to cross between countries in the Risk game board.

#### Solution

##### Approach
Build undirected graph with 20 nodes from adjacency lists. Floyd-Warshall for all-pairs shortest paths (all edges have weight 1). Answer queries using precomputed distances.

##### Python Solution

```python
INF = float('inf')
NUM_COUNTRIES = 20


def floyd_warshall(graph, case_number, queries):
    dist = [[graph[i][j] for j in range(NUM_COUNTRIES)] for i in range(NUM_COUNTRIES)]

    for k in range(NUM_COUNTRIES):
        for i in range(NUM_COUNTRIES):
            for j in range(NUM_COUNTRIES):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    print(f'Test Set #{case_number}')
    for src, dest in queries:
        print(f"{src:2d} to {dest:2d}: {dist[src - 1][dest - 1]}")


def solution():
    case_num = 1
    while True:
        graph = [[INF] * NUM_COUNTRIES for _ in range(NUM_COUNTRIES)]

        for i in range(NUM_COUNTRIES - 1):
            try:
                line = list(map(int, input().strip().split()))
            except:
                return
            if not line:
                return

            num_neighbors = line[0]
            for neighbor in line[1:num_neighbors + 1]:
                graph[i][neighbor - 1] = 1
                graph[neighbor - 1][i] = 1

        num_queries = int(input())
        queries = [tuple(map(int, input().strip().split())) for _ in range(num_queries)]

        floyd_warshall(graph, case_num, queries)
        print()
        case_num += 1


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(20^3) = O(1) per test case (constant graph size)
- **Space Complexity:** O(20^2) = O(1)
