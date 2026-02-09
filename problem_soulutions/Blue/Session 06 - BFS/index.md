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
from collections import deque

def can_reach_destination(start, end, n, m, matrix):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    visited = [[False] * m for _ in range(n)]
    visited[start[0]][start[1]] = True

    queue = deque([start])

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) == tuple(end):
                if matrix[nx][ny] == 'X':
                    return 'YES'
                # Check if destination has another adjacent passable cell
                for ddx, ddy in directions:
                    nnx, nny = nx + ddx, ny + ddy
                    if (0 <= nnx < n and 0 <= nny < m and
                        matrix[nnx][nny] == '.' and (nnx, nny) != (x, y)):
                        return 'YES'
                return 'NO'
            if (0 <= nx < n and 0 <= ny < m and
                matrix[nx][ny] == '.' and not visited[nx][ny]):
                queue.append((nx, ny))
                visited[nx][ny] = True

    return 'NO'

def solution():
    n, m = map(int, input().split())
    matrix = [input().strip() for _ in range(n)]

    r1, c1 = map(int, input().split())
    r2, c2 = map(int, input().split())
    start = (r1 - 1, c1 - 1)
    end = (r2 - 1, c2 - 1)

    print(can_reach_destination(start, end, n, m, matrix))

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
from collections import deque

def bfs_count_possible_leaves(n, max_cats, cats, graph):
    consecutive_cats = [-1] * (n + 1)
    consecutive_cats[1] = cats[0]
    total_restaurants = 0

    queue = deque([1])

    while queue:
        u = queue.popleft()
        # Leaf node (not root)
        if len(graph[u]) == 1 and u != 1:
            total_restaurants += 1
            continue

        for v in graph[u]:
            if consecutive_cats[v] == -1:
                consecutive_cats[v] = consecutive_cats[u] + 1 if cats[v - 1] else 0
                if consecutive_cats[v] <= max_cats:
                    queue.append(v)

    return total_restaurants

def solution():
    n, m = map(int, input().split())
    cats = list(map(int, input().split()))
    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    print(bfs_count_possible_leaves(n, m, cats, graph))

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
from collections import deque

def find_minimum_time(key_value, lock_value, magic_keys):
    if key_value == lock_value:
        return 0

    MOD = 100000
    dist = [-1] * MOD
    dist[key_value] = 0
    queue = deque([key_value])

    while queue:
        curr = queue.popleft()
        for key in magic_keys:
            new_val = (curr * key) % MOD
            if dist[new_val] == -1:
                dist[new_val] = dist[curr] + 1
                if new_val == lock_value:
                    return dist[new_val]
                queue.append(new_val)

    return -1

def solution():
    key_value, lock_value = map(int, input().split())
    n = int(input())
    magic_keys = list(map(int, input().split()))
    print(find_minimum_time(key_value, lock_value, magic_keys))

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
from collections import deque, defaultdict

def bfs(n, edges, start):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    dist = [-1] * (n + 1)
    dist[start] = 0
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    return [dist[i] * 6 if dist[i] != -1 else -1 for i in range(1, n + 1) if i != start]

if __name__ == '__main__':
    q = int(input())

    for _ in range(q):
        n, m = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(m)]
        start = int(input())
        result = bfs(n, edges, start)
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
from collections import deque

def calculate_possible_cells(width, height, matrix, prince_pos):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    visited = [[False] * width for _ in range(height)]
    visited[prince_pos[0]][prince_pos[1]] = True
    total_cells = 1

    queue = deque([prince_pos])

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < height and 0 <= ny < width and
                matrix[nx][ny] == '.' and not visited[nx][ny]):
                queue.append((nx, ny))
                visited[nx][ny] = True
                total_cells += 1

    return total_cells

def solution():
    results = []
    T = int(input())

    for case in range(1, T + 1):
        width, height = map(int, input().split())
        matrix = []
        prince_pos = None

        for row in range(height):
            line = input().strip()
            if '@' in line:
                prince_pos = (row, line.index('@'))
            matrix.append(line)

        cells = calculate_possible_cells(width, height, matrix, prince_pos)
        results.append(f'Case {case}: {cells}')

    print('\n'.join(results))

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
from collections import deque

def calc_survive(n, m, matrix):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    visited = [[False] * m for _ in range(n)]
    passable = {'.', 'k', 'v'}

    total_sheep = total_wolves = 0

    for start_row in range(n):
        for start_col in range(m):
            if matrix[start_row][start_col] in passable and not visited[start_row][start_col]:
                visited[start_row][start_col] = True
                queue = deque([(start_row, start_col)])
                sheep = wolves = 0
                is_enclosed = start_row not in (0, n - 1) and start_col not in (0, m - 1)

                if matrix[start_row][start_col] == 'k':
                    sheep = 1
                elif matrix[start_row][start_col] == 'v':
                    wolves = 1

                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < n and 0 <= ny < m and
                            matrix[nx][ny] in passable and not visited[nx][ny]):
                            queue.append((nx, ny))
                            visited[nx][ny] = True

                            if matrix[nx][ny] == 'k':
                                sheep += 1
                            elif matrix[nx][ny] == 'v':
                                wolves += 1

                            if nx in (0, n - 1) or ny in (0, m - 1):
                                is_enclosed = False

                if is_enclosed:
                    if sheep > wolves:
                        total_sheep += sheep
                    else:
                        total_wolves += wolves
                else:
                    total_sheep += sheep
                    total_wolves += wolves

    return total_sheep, total_wolves

def solution():
    while True:
        line = input().strip()
        if line:
            n, m = map(int, line.split())
            break

    backyard = []
    while len(backyard) < n:
        line = input().strip()
        if line:
            backyard.append(line)

    print(*calc_survive(n, m, backyard))

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
from collections import deque

def check_path(maze, start, end, rows, cols):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    visited = [[False] * cols for _ in range(rows)]
    visited[start[0]][start[1]] = True
    queue = deque([start])

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < rows and 0 <= ny < cols and
                maze[nx][ny] and not visited[nx][ny]):
                if (nx, ny) == end:
                    return True
                visited[nx][ny] = True
                queue.append((nx, ny))

    return False

def get_edge_openings(maze, rows, cols):
    openings = []

    # Check left and right edges
    for i in range(rows):
        if maze[i][0]:
            openings.append((i, 0))
        if cols > 1 and maze[i][cols - 1]:
            openings.append((i, cols - 1))
        if len(openings) > 2:
            return []

    # Check top and bottom edges (excluding corners)
    for j in range(1, cols - 1):
        if maze[0][j]:
            openings.append((0, j))
        if rows > 1 and maze[rows - 1][j]:
            openings.append((rows - 1, j))
        if len(openings) > 2:
            return []

    return openings

def check_valid_maze(maze, rows, cols):
    openings = get_edge_openings(maze, rows, cols)
    if len(openings) == 2:
        return check_path(maze, openings[0], openings[1], rows, cols)
    return False

def solution():
    t = int(input())
    results = []

    for _ in range(t):
        rows, cols = map(int, input().split())
        maze = [[c == '.' for c in input().strip()] for _ in range(rows)]
        results.append('valid' if check_valid_maze(maze, rows, cols) else 'invalid')

    print('\n'.join(results))

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
from collections import deque, defaultdict

def calc_slick(n, m, matrix):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    total_slicks = 0
    slick_sizes = defaultdict(int)

    for row in range(n):
        for col in range(m):
            if matrix[row][col] == 1:
                total_slicks += 1
                slick_size = 1
                matrix[row][col] = 0
                queue = deque([(row, col)])

                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and matrix[nx][ny] == 1:
                            queue.append((nx, ny))
                            matrix[nx][ny] = 0
                            slick_size += 1

                slick_sizes[slick_size] += 1

    results = [[total_slicks]]
    results.extend([size, count] for size, count in sorted(slick_sizes.items()))
    return results

def solution():
    all_results = []

    while True:
        n, m = map(int, input().split())
        if n == 0:
            break
        matrix = [list(map(int, input().split())) for _ in range(n)]
        all_results.append(calc_slick(n, m, matrix))

    for result in all_results:
        for line in result:
            print(*line)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N * M) per test case
- **Space Complexity:** O(N * M) for the matrix and queue
