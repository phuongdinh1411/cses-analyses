---
layout: simple
title: "BFS"
permalink: /problem_soulutions/Blue/Session 06 - BFS/
---

# BFS

Breadth-First Search problems involving shortest paths in unweighted graphs, level-order traversal, and grid-based exploration.

## Problems

### Ice Cave

#### Problem Information
- **Source:** [Codeforces 540C](https://codeforces.com/problemset/problem/540/C)
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

You're in an ice cave represented as an n x m grid. Each cell is either:
- '.' (intact ice) - you can step on it, but it will crack and become 'X'
- 'X' (cracked ice) - you cannot step on it; stepping on it means falling through

You start at position (r1, c1) and want to reach (r2, c2). The goal is to FALL THROUGH the ice at the destination (the destination must become cracked when you step on it).

You can reach the destination if:
- There's a valid path from start to an adjacent cell of destination
- The destination ice will crack when you step on it (either already cracked, or you've visited an adjacent cell that cracks it)

#### Input Format
- Line 1: n m (grid dimensions)
- Next n lines: Grid of '.' and 'X'
- Line n+2: r1 c1 (starting position, 1-indexed)
- Line n+3: r2 c2 (destination position, 1-indexed)

#### Output Format
"YES" if you can reach and fall through at destination, "NO" otherwise.

#### Example
```
Input:
4 6
......
X.X.X.
....X.
......
2 2
2 5

Output:
YES
```
Start at (2,2), destination (2,5). Can navigate around obstacles and reach destination to fall through.

```
Input:
2 2
..
..
1 1
2 2

Output:
NO
```
Destination (2,2) is intact ice '.'. Need to crack it first, but no way to approach it twice.

#### Solution

##### Approach
Use BFS pathfinding with special handling for the destination cell. When we reach a cell adjacent to the destination, we check if the destination is already cracked (can step on it directly) or if there's another path to crack it first.

##### Python Solution

```python
import queue

def can_reach_destination(starting_point, ending_point, n, m, matrix):
  dx = [1, 0, -1, 0]
  dy = [0, -1, 0, 1]

  visited = [[False for i in range(m)] for j in range(n)]
  visited[starting_point[0]][starting_point[1]] = True

  q = queue.Queue()
  q.put(starting_point)

  while not q.empty():
    checking_node = q.get()
    for l in range(4):
      neighbor_x = checking_node[0] + dx[l]
      neighbor_y = checking_node[1] + dy[l]
      if neighbor_x == ending_point[0] and neighbor_y == ending_point[1]:
        if matrix[neighbor_x][neighbor_y] == 'X':
          return 'YES'
        else:
          for end_check in range(4):
            end_neighbor_x = neighbor_x + dx[end_check]
            end_neighbor_y = neighbor_y + dy[end_check]
            if 0 <= end_neighbor_x < n and 0 <= end_neighbor_y < m and matrix[end_neighbor_x][end_neighbor_y] == '.':
              if end_neighbor_x != checking_node[0] or end_neighbor_y != checking_node[1]:
                return 'YES'
          return 'NO'
      else:
        if 0 <= neighbor_x < n and 0 <= neighbor_y < m and matrix[neighbor_x][neighbor_y] == '.' and not visited[neighbor_x][neighbor_y]:
          q.put([neighbor_x, neighbor_y])
          visited[neighbor_x][neighbor_y] = True

  return 'NO'

def solution():
  n, m = map(int, input().split())
  matrix = []
  for i in range(n):
    matrix.append(input().strip())

  starting_point = list(map(int, input().split()))
  ending_point = list(map(int, input().split()))

  starting_point[0] -= 1
  starting_point[1] -= 1
  ending_point[0] -= 1
  ending_point[1] -= 1

  print(can_reach_destination(starting_point, ending_point, n, m, matrix))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * m) for BFS traversal of the grid
- **Space Complexity:** O(n * m) for visited array and queue

---

### Kefa and Park

#### Problem Information
- **Source:** [Codeforces 580C](https://codeforces.com/problemset/problem/580/C)
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Kefa wants to visit restaurants located at the leaves of a tree. The tree has n vertices rooted at vertex 1. Each vertex either has a cat (1) or not (0). Kefa is afraid of cats and won't go through a path with more than m consecutive vertices containing cats.

Count the number of restaurants (leaf nodes) Kefa can reach from the root without passing through more than m consecutive cats.

#### Input Format
- Line 1: n m (vertices count, max consecutive cats allowed)
- Line 2: n integers a[i] (1 if vertex i has a cat, 0 otherwise)
- Next n-1 lines: u v (edge between vertices u and v)

#### Output Format
Number of restaurants (leaves) Kefa can visit.

#### Example
```
Input:
4 1
1 1 0 0
1 2
1 3
1 4

Output:
2
```
Tree rooted at 1 (has cat). Children 2 (cat), 3 (no cat), 4 (no cat). From 1→2: 2 consecutive cats (exceeds m=1). 1→3 and 1→4: only 1 cat. Can reach restaurants at 3 and 4.

#### Solution

##### Approach
BFS from root, tracking consecutive cats on each path. When we encounter a non-cat vertex, reset the counter. Stop exploring a path if consecutive cats exceed m.

##### Python Solution

```python
import queue

def bfs_count_possible_leaves(n, m, a, graph):
  consecutive_cats = [-1 for i in range(n+9)]
  total_restaurants = 0
  consecutive_cats[1] = a[0]

  q = queue.Queue()
  q.put(1)

  while not q.empty():
    u = q.get()
    if len(graph[u]) == 1 and u != 1:
      total_restaurants += 1
    else:
      for v in graph[u]:
        if consecutive_cats[v] == -1:
          if a[v-1] == 0:
            consecutive_cats[v] = 0
          else:
            consecutive_cats[v] = consecutive_cats[u] + 1
          if consecutive_cats[v] <= m:
            q.put(v)
  return total_restaurants

def solution():
  n, m = map(int, input().split())
  a = list(map(int, input().split()))
  graph = [[] for i in range(n + 1)]
  for i in range(1, n):
    s, e = map(int, input().split())
    graph[s].append(e)
    graph[e].append(s)

  print(bfs_count_possible_leaves(n, m, a, graph))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n) for BFS traversal of the tree
- **Space Complexity:** O(n) for the graph and auxiliary arrays

---

### Dhoom 4

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

You have a key with value K and need to unlock a lock with value L. You also have N magic numbers. Each time you can multiply your key value by any magic number, taking the result modulo 100000.

Find the minimum number of operations to transform key value K into lock value L. If impossible, return -1.

#### Input Format
- Line 1: K L (initial key value, target lock value)
- Line 2: N (number of magic numbers)
- Line 3: N integers (the magic numbers)

#### Output Format
Minimum operations to reach lock value, or -1 if impossible.

#### Example
```
Input:
3 30
3
2 5 7

Output:
2
```
3 × 2 = 6, 6 × 5 = 30. Two operations.

```
Input:
1 1
1
2

Output:
0
```
Already at target, 0 operations needed.

#### Solution

##### Approach
BFS where each state is a key value (0-99999), and edges represent multiplications by magic numbers. This finds the shortest path from K to L in the state space.

##### Python Solution

```python
import queue

def find_minimum_time(key_value, lock_value, keys):
  if key_value == lock_value:
    return 0

  visited = [False for i in range(100000)]
  path = [-1 for i in range(100000)]
  q = queue.Queue()
  q.put(key_value)

  while not q.empty():
    u = q.get()
    for key in keys:
      new_key = (key * u) % 100000
      if not visited[new_key]:
        visited[new_key] = True
        q.put(new_key)
        path[new_key] = u
        if lock_value == new_key:
          return get_time(key_value, lock_value, path)

  return -1

def get_time(key_value, lock_value, path):
  total_time = 0
  current_node = lock_value
  while True:
    if key_value == path[current_node]:
      return total_time + 1
    else:
      total_time += 1
      current_node = path[current_node]

def solution():
  key_value, lock_value = map(int, input().split())
  N = int(input())
  keys = list(map(int, input().split()))

  print(find_minimum_time(key_value, lock_value, keys))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(100000 * N) in worst case
- **Space Complexity:** O(100000) for visited array and path reconstruction

---

### BFS: Shortest Reach in a Graph

#### Problem Information
- **Source:** Hackerrank
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given an undirected graph with n nodes and m edges, find the shortest distance from a starting node s to all other nodes. Each edge has weight 6. If a node is unreachable, report -1.

#### Input Format
- Line 1: q (number of queries/test cases)
- For each query:
  - Line 1: n m (nodes, edges)
  - Next m lines: u v (edge between u and v)
  - Last line: s (starting node)

#### Output Format
For each query, print n-1 space-separated integers representing shortest distances from s to nodes 1, 2, ..., n (excluding s itself).

#### Example
```
Input:
1
4 2
1 2
1 3
1

Output:
6 6 -1
```
From node 1: distance to 2 is 6 (1 hop), to 3 is 6 (1 hop), to 4 is -1 (unreachable).

#### Solution

##### Approach
Standard BFS from the starting node, multiply hop count by 6 for final distance since all edges have weight 6.

##### Python Solution

```python
import queue

def bfs(n, m, edges, s):
  MAX = n + 9
  visited = [False for i in range(MAX)]
  path = [-1 for i in range(MAX)]
  for i in range(1, n + 1):
    visited[i] = False

  graph = [[] for i in range(MAX)]
  for e in edges:
    graph[e[0]].append(e[1])
    graph[e[1]].append(e[0])

  q = queue.Queue()
  visited[s] = True
  q.put(s)

  while not q.empty():
    u = q.get()
    for v in graph[u]:
      if not visited[v]:
        visited[v] = True
        q.put(v)
        path[v] = u

  _result = []
  for i in range(1, n + 1):
    if i != s:
      _result.append(calc_path(s, i, path))

  return _result

def calc_path(s, f, path):
  steps = 0
  if path[f] == -1:
    return -1

  while True:
    steps += 1
    f = path[f]
    if f == s:
      break
  return steps * 6

if __name__ == '__main__':
  q = int(input())

  for q_itr in range(q):
    nm = input().split()
    n = int(nm[0])
    m = int(nm[1])

    edges = []
    for _ in range(m):
      edges.append(list(map(int, input().rstrip().split())))

    s = int(input())
    result = bfs(n, m, edges, s)
    print(' '.join(map(str, result)))
```

##### Complexity Analysis
- **Time Complexity:** O(n + m) for BFS
- **Space Complexity:** O(n + m) for graph storage and auxiliary arrays

---

### Guilty Prince

#### Problem Information
- **Source:** LightOJ 1012
- **Difficulty:** Secret
- **Time Limit:** 500ms
- **Memory Limit:** 32MB

#### Problem Statement

A prince is standing in a dungeon cell. The dungeon is a W x H grid where:
- '.' represents an empty cell (passable)
- '#' represents a wall (impassable)
- '@' represents the prince's starting position (also passable)

The prince can move in 4 directions (up, down, left, right). Count the total number of cells the prince can reach from his starting position.

#### Input Format
- Line 1: T (number of test cases)
- For each test case:
  - Line 1: W H (width and height of dungeon)
  - Next H lines: The dungeon grid

#### Output Format
For each test case, print "Case X: Y" where Y is the count of reachable cells (including the starting cell).

#### Example
```
Input:
1
4 4
...#
.@.#
....
####

Output:
Case 1: 8
```
Prince at (1,1). Can reach all cells except walls (#). Reachable: 8 cells.

#### Solution

##### Approach
BFS flood fill from prince's position to count all reachable cells.

##### Python Solution

```python
import queue

def calculate_possible_cells(wi, hi, matrix, prince_position):
  total_possible_cells = 1
  dx = [1, 0, -1, 0]
  dy = [0, -1, 0, 1]

  visited = [[False for i in range(wi)] for j in range(hi)]
  q = queue.Queue()
  q.put(prince_position)

  while not q.empty():
    checking_node = q.get()
    for i in range(4):
      neighbor_x = checking_node[0] + dx[i]
      neighbor_y = checking_node[1] + dy[i]
      if neighbor_x >= 0 and neighbor_y >= 0 and neighbor_x < hi and neighbor_y < wi and matrix[neighbor_x][neighbor_y] == '.':
        if not visited[neighbor_x][neighbor_y]:
          q.put([neighbor_x, neighbor_y])
          visited[neighbor_x][neighbor_y] = True
          total_possible_cells += 1

  return total_possible_cells

def solution():
  results = []
  T = int(input())
  for i in range(T):
    Wi, Hi = map(int, input().split())
    matrix = []
    prince_position = []
    for j in range(Hi):
      new_line = input().strip()
      if new_line.find('@') >= 0:
        prince_position.append(j)
        prince_position.append(new_line.find('@'))
      matrix.append(new_line)
    results.append('Case {0}: {1}'.format(i + 1, calculate_possible_cells(Wi, Hi, matrix, prince_position)))

  print(*results, sep='\n')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(W * H) for BFS traversal
- **Space Complexity:** O(W * H) for visited array

---

### KOZE - Sheep

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

A backyard is represented as an N x M grid with:
- '#' - fence (impassable)
- '.' - empty grass
- 'k' - sheep
- 'v' - wolf

Wolves eat sheep unless they're in a fenced area (surrounded by fence on all sides, not touching the boundary). In a fenced area, if there are more sheep than wolves, the sheep survive; otherwise wolves survive. Outside fenced areas (connected to boundary), both survive.

Count how many sheep and wolves survive.

#### Input Format
- Line 1: N M (grid dimensions)
- Next N lines: The backyard grid

#### Output Format
Two integers - surviving sheep and wolves.

#### Example
```
Input:
5 5
#####
#k.v#
#...#
#####
.....

Output:
1 0
```
Top fenced area has 1 sheep, 1 wolf. Sheep > wolves, so sheep survives. Outside area (bottom) is empty.

#### Solution

##### Approach
BFS to find connected components of non-fence cells. For each component, check if it touches the boundary. If it's a closed sector, only the majority survives; if connected to boundary, all survive.

##### Python Solution

```python
import queue

def calc_survive(N, M, matrix):
  visited = [[False for i in range(M)] for j in range(N)]
  dx = [1, 0, -1, 0]
  dy = [0, -1, 0, 1]

  wolfs_counter = 0
  sheeps_counter = 0

  for row_counter in range(N):
    for col_counter in range(M):
      if (matrix[row_counter][col_counter] == '.' or matrix[row_counter][col_counter] == 'k' or
            matrix[row_counter][col_counter] == 'v') and not visited[row_counter][col_counter]:
        visited[row_counter][col_counter] = True
        q = queue.Queue()
        q.put([row_counter, col_counter])
        sheeps, wolfs = 0, 0
        if matrix[row_counter][col_counter] == 'k':
          sheeps = 1
        if matrix[row_counter][col_counter] == 'v':
          wolfs = 1
        belong_to_sector = True
        while not q.empty():
          checking_node = q.get()
          for l in range(4):
            neighbor_x = checking_node[0] + dx[l]
            neighbor_y = checking_node[1] + dy[l]
            if 0 <= neighbor_x < N and 0 <= neighbor_y < M and (
                      matrix[neighbor_x][neighbor_y] == '.' or matrix[neighbor_x][
                    neighbor_y] == 'k' or
                    matrix[neighbor_x][neighbor_y] == 'v') and not visited[neighbor_x][neighbor_y]:
              q.put([neighbor_x, neighbor_y])
              visited[neighbor_x][neighbor_y] = True
              if matrix[neighbor_x][neighbor_y] == 'k':
                sheeps += 1
              if matrix[neighbor_x][neighbor_y] == 'v':
                wolfs += 1
              if neighbor_y == 0 or neighbor_x == 0 or neighbor_y == M - 1 or neighbor_x == N - 1:
                belong_to_sector = False
        if belong_to_sector:
          if sheeps > wolfs:
            sheeps_counter += sheeps
          else:
            wolfs_counter += wolfs
        else:
          sheeps_counter += sheeps
          wolfs_counter += wolfs

  return [sheeps_counter, wolfs_counter]

def solution():
  while True:
    new_line = input().strip()
    if new_line:
      N, M = map(int, new_line.split())
      break
  backyard = []
  i = 0
  while i < N:
    new_line = input().strip()
    if new_line:
      backyard.append(new_line)
      i += 1

  print(*calc_survive(N, M, backyard), sep=' ')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N * M) for BFS traversal
- **Space Complexity:** O(N * M) for visited array

---

### MAKEMAZE - Valid Maze

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 601ms
- **Memory Limit:** 1536MB

#### Problem Statement

A maze is represented as an M x N grid with:
- '.' representing open cells (passable)
- '#' representing walls (blocked)

A maze is "valid" if:
1. There are exactly 2 openings on the boundary (entry and exit)
2. There exists a path between these two openings

#### Input Format
- Line 1: T (number of test cases)
- For each test case:
  - Line 1: M N (rows, columns)
  - Next M lines: The maze grid

#### Output Format
For each test case, print "valid" or "invalid".

#### Example
```
Input:
2
3 3
###
#.#
###
3 4
####
#..#
#.##

Output:
invalid
valid
```
First maze: no boundary openings (all '#' on edges) → invalid. Second maze: two openings on boundary, connected → valid.

#### Solution

##### Approach
First count boundary openings. If exactly 2, build a graph and use BFS to check if they're connected.

##### Python Solution

```python
import queue

def check_path(m, n, maze_graph, start_point, end_point):
  visited = [[False for i in range(n)] for j in range(m)]

  q = queue.Queue()
  visited[start_point[0]][start_point[1]] = True
  q.put(start_point)
  while not q.empty():
    u = q.get()
    for v in maze_graph[u[0]][u[1]]:
      if not visited[v[0]][v[1]]:
        if v[0] == end_point[0] and v[1] == end_point[1]:
          return True
        visited[v[0]][v[1]] = True
        q.put(v)

  return False

def get_edge_openings(m, n, maze_matrix):
  edge_openings_counter = 0
  edge_openings = []
  for i in range(m):
    if maze_matrix[i][0]:
      edge_openings_counter += 1
      edge_openings.append([i, 0])
    if n > 1 and maze_matrix[i][n - 1]:
      edge_openings_counter += 1
      edge_openings.append([i, n - 1])
    if edge_openings_counter > 2:
      return []

  for i in range(1, n - 1, 1):
    if maze_matrix[0][i]:
      edge_openings_counter += 1
      edge_openings.append([0, i])
    if m > 1 and maze_matrix[m - 1][i]:
      edge_openings_counter += 1
      edge_openings.append([m - 1, i])
    if edge_openings_counter > 2:
      return []

  return edge_openings

def check_valid_maze(m, n, maze_matrix):
  edge_openings = get_edge_openings(m, n, maze_matrix)
  if len(edge_openings) == 2:
    maze_graph = []
    for i in range(m):
      maze_graph.append([[] for l in range(n)])
      for j in range(n):
        if maze_matrix[i][j] == 1:
          if i > 0 and maze_matrix[i - 1][j] == 1:
            maze_graph[i][j].append([i - 1, j])
          if j > 0 and maze_matrix[i][j - 1] == 1:
            maze_graph[i][j].append([i, j - 1])
          if i < m - 1 and maze_matrix[i + 1][j] == 1:
            maze_graph[i][j].append([i + 1, j])
          if j < n - 1 and maze_matrix[i][j + 1] == 1:
            maze_graph[i][j].append([i, j + 1])
    return check_path(m, n, maze_graph, edge_openings[0], edge_openings[1])
  return False

def solution():
  t = int(input())
  result = []

  for i in range(t):
    m, n = map(int, input().split())
    M = []
    for row in range(m):
      M.append([])
      rowi = input().strip()
      for col in range(n):
        M[row].append(1 if rowi[col] == '.' else 0)

    result.append('valid' if check_valid_maze(m, n, M) else 'invalid')

  print(*result, sep='\n')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(M * N) for BFS
- **Space Complexity:** O(M * N) for graph and visited array

---

### Oil Slicks (Slick)

#### Problem Information
- **Source:** SPOJ UCV2013H
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given an N x M grid representing an ocean area where:
- 0 = water
- 1 = oil

An oil slick is a connected component of oil cells (4-directional adjacency). Count the total number of slicks and categorize them by size.

#### Input Format
- Multiple test cases until N=0 M=0
- For each test case:
  - Line 1: N M (grid dimensions)
  - Next N lines: M integers (0 or 1)

#### Output Format
For each test case:
- Line 1: Total number of slicks
- Following lines: "size count" pairs in increasing order of size

#### Example
```
Input:
3 3
1 0 0
1 0 1
0 0 1
0 0

Output:
2
2 2
```
Two slicks: one of size 2 (top-left corner), one of size 2 (bottom-right). Total: 2 slicks, both of size 2.

#### Solution

##### Approach
BFS flood fill to find and measure connected components of oil cells.

##### Python Solution

```python
import queue

def calc_slick(N, M, matrix):
  total_slicks = 0
  slick_list = {}

  dx = [1, 0, -1, 0]
  dy = [0, -1, 0, 1]

  for row_counter in range(N):
    for col_counter in range(M):
      if matrix[row_counter][col_counter] == 1:
        total_slicks += 1
        slick_size = 1
        q = queue.Queue()
        q.put([row_counter, col_counter])
        matrix[row_counter][col_counter] = 0
        while not q.empty():
          checking_node = q.get()
          for l in range(4):
            neighbor_x = checking_node[0] + dx[l]
            neighbor_y = checking_node[1] + dy[l]
            if 0 <= neighbor_x < N and 0 <= neighbor_y < M and matrix[neighbor_x][neighbor_y] == 1:
              q.put([neighbor_x, neighbor_y])
              slick_size += 1
              matrix[neighbor_x][neighbor_y] = 0

        if slick_size in slick_list:
          slick_list[slick_size] += 1
        else:
          slick_list[slick_size] = 1

  results = [[total_slicks]]

  for key in sorted(slick_list):
    results.append([key, slick_list[key]])

  return results

def solution():
  results = []
  while True:
    N, M = map(int, input().split())
    if N == 0:
      break
    matrix = []
    for i in range(N):
      matrix.append(list(map(int, input().split())))

    results.append(calc_slick(N, M, matrix))

  for i in range(len(results)):
    for j in range(len(results[i])):
      print(*results[i][j], sep=' ')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N * M) per test case
- **Space Complexity:** O(N * M) for the matrix and queue
