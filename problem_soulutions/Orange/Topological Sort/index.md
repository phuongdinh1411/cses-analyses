---
layout: simple
title: "Topological Sort"
permalink: /problem_soulutions/Orange/Topological Sort/
---
# Topological Sort

Problems involving topological ordering of directed acyclic graphs (DAGs), commonly used for dependency resolution and scheduling tasks.

## Problems

### Answer the boss

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

#### Problem Statement

Eloy wants to know the "rank" of each employee in a company. Given the number of employees and relations between them (who is lower than whom), output the rank of each employee.

Rank 1 is the "boss" (not bullied by anybody). Employees with the same rank should be listed in lexicographical order.

#### Input Format
- First line: T (number of test cases)
- For each test case:
  - First line: N (employees) and R (relations)
  - Next R lines: R1 R2 meaning "employee R1 is lower than R2's rank"

#### Constraints
- 1 ≤ N ≤ 1000
- 1 ≤ R ≤ 10000

#### Output Format
For each test case, print "Scenario #i:" followed by N lines with rank and employee index, sorted by rank then by employee index.

#### Solution

##### Approach
1. Build a directed graph where edge (R2 → R1) means R1 is subordinate to R2
2. Use topological sort to process nodes in order
3. Rank of each node = max(rank of all superiors) + 1
4. Nodes with no incoming edges (in original graph) have rank 1

##### Python Solution

```python
from collections import defaultdict, deque

def solve():
  t = int(input())

  for case in range(1, t + 1):
    n, r = map(int, input().split())

    # adj[v] contains subordinates of v
    # in_degree tracks how many superiors each employee has
    adj = defaultdict(list)
    in_degree = [0] * n

    for _ in range(r):
      r1, r2 = map(int, input().split())
      # r1 is lower than r2, so r2 -> r1
      adj[r2].append(r1)
      in_degree[r1] += 1

    # Compute ranks using modified topological sort
    rank = [0] * n
    queue = deque()

    # Start with bosses (no one above them)
    for i in range(n):
      if in_degree[i] == 0:
        rank[i] = 1
        queue.append(i)

    while queue:
      u = queue.popleft()
      for v in adj[u]:
        rank[v] = max(rank[v], rank[u] + 1)
        in_degree[v] -= 1
        if in_degree[v] == 0:
          queue.append(v)

    # Create result list and sort
    employees = [(rank[i], i) for i in range(n)]
    employees.sort()

    print(f"Scenario #{case}:")
    for r, idx in employees:
      print(r, idx)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  t = int(input())

  for case in range(1, t + 1):
    n, r = map(int, input().split())

    adj = [[] for _ in range(n)]
    in_degree = [0] * n

    for _ in range(r):
      r1, r2 = map(int, input().split())
      adj[r2].append(r1)
      in_degree[r1] += 1

    # DFS to compute ranks
    rank = [0] * n

    def dfs(u, current_rank):
      rank[u] = max(rank[u], current_rank)
      for v in adj[u]:
        dfs(v, rank[u] + 1)

    # Start DFS from all bosses
    for i in range(n):
      if in_degree[i] == 0:
        dfs(i, 1)

    # Sort and output
    result = sorted([(rank[i], i) for i in range(n)])

    print(f"Scenario #{case}:")
    for r, idx in result:
      print(r, idx)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N + R) for topological sort, O(N log N) for sorting output
- **Space Complexity:** O(N + R) for adjacency list

##### Key Insight
The rank of an employee is 1 + maximum rank among all their superiors. Process employees in topological order (superiors before subordinates) to correctly compute ranks.

---

### Beverages

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Dilbert has just finished college and decided to go out with friends. He has some strange habits and thus he decided to celebrate this important moment of his life drinking a lot. He will start drinking beverages with low alcohol content, like beer, and then will move to a beverage that contains more alcohol, like wine, until there are no more available beverages. Once Dilbert starts to drink wine he will not drink beer again, so the alcohol content of the beverages never decreases with time.

You should help Dilbert by indicating an order in which he can drink the beverages in the way he wishes.

#### Input Format
- Each test case starts with N (1 ≤ N ≤ 100), the number of available beverages.
- Then N lines follow with the name of each beverage (less than 51 characters, no white spaces).
- Then an integer M (0 ≤ M ≤ 200) followed by M lines in the form "B1 B2", indicating that B2 has more alcohol than B1, so B1 should be drunk before B2.
- There is a blank line after each test case.
- In case there is no relation between two beverages, Dilbert should drink the one that appears first in the input.
- Input is terminated by EOF.

#### Output Format
For each test case print: "Case #C: Dilbert should drink beverages in this order: B1 B2 ... BN." followed by a blank line.

#### Solution

##### Approach
This is a topological sort problem with a twist: when there are multiple valid choices, we must pick the beverage that appeared earliest in the input (smallest index). Use a min-heap (priority queue) to always select the smallest index among nodes with zero in-degree.

##### Python Solution

```python
import heapq
from collections import defaultdict

def solve():
  case_num = 0

  try:
    while True:
      n = int(input())
      case_num += 1

      # Read beverage names and create mapping
      beverages = []
      name_to_id = {}

      for i in range(n):
        name = input().strip()
        beverages.append(name)
        name_to_id[name] = i

      # Build graph
      graph = defaultdict(list)
      in_degree = [0] * n

      m = int(input())
      for _ in range(m):
        line = input().split()
        b1, b2 = line[0], line[1]
        u, v = name_to_id[b1], name_to_id[b2]
        graph[u].append(v)
        in_degree[v] += 1

      # Read blank line
      try:
        input()
      except:
        pass

      # Topological sort using min-heap (to get lexicographically smallest by input order)
      heap = []
      for i in range(n):
        if in_degree[i] == 0:
          heapq.heappush(heap, i)

      result = []
      while heap:
        u = heapq.heappop(heap)
        result.append(beverages[u])

        for v in graph[u]:
          in_degree[v] -= 1
          if in_degree[v] == 0:
            heapq.heappush(heap, v)

      # Output
      print(f"Case #{case_num}: Dilbert should drink beverages in this order: {' '.join(result)}.")
      print()

  except EOFError:
    pass

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
import heapq

def topological_sort(n, graph, in_degree):
  """Topological sort with tie-breaking by index (input order)"""
  result = []
  heap = [i for i in range(n) if in_degree[i] == 0]
  heapq.heapify(heap)

  while heap:
    u = heapq.heappop(heap)
    result.append(u)

    for v in graph[u]:
      in_degree[v] -= 1
      if in_degree[v] == 0:
        heapq.heappush(heap, v)

  return result

def solve():
  import sys
  input_data = sys.stdin.read().split('\n')
  idx = 0
  case_num = 0

  while idx < len(input_data):
    try:
      n = int(input_data[idx])
    except:
      break

    idx += 1
    case_num += 1

    # Read beverages
    beverages = []
    name_to_id = {}
    for i in range(n):
      name = input_data[idx].strip()
      beverages.append(name)
      name_to_id[name] = i
      idx += 1

    # Read constraints
    m = int(input_data[idx])
    idx += 1

    graph = [[] for _ in range(n)]
    in_degree = [0] * n

    for _ in range(m):
      parts = input_data[idx].split()
      b1, b2 = parts[0], parts[1]
      u, v = name_to_id[b1], name_to_id[b2]
      graph[u].append(v)
      in_degree[v] += 1
      idx += 1

    # Skip blank line
    if idx < len(input_data) and input_data[idx].strip() == '':
      idx += 1

    # Topological sort
    order = topological_sort(n, graph, in_degree)
    result = [beverages[i] for i in order]

    print(f"Case #{case_num}: Dilbert should drink beverages in this order: {' '.join(result)}.")
    print()

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N + M + N log N) where N is beverages and M is constraints
- **Space Complexity:** O(N + M) for graph storage

##### Key Insight
Using a min-heap instead of a regular queue ensures that when multiple beverages have zero in-degree, we always pick the one that appeared first in the input (smallest index).

---

### Book of Evil

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Paladin Manao is searching for the Book of Evil in a swampy area with n settlements connected by n-1 bidirectional paths (a tree). The Book has damage range d, meaning it affects settlements at distance d or less.

Manao knows m settlements that are affected. Determine how many settlements could possibly contain the Book of Evil.

#### Input Format
- First line: n, m, d (1 ≤ m ≤ n ≤ 100000; 0 ≤ d ≤ n-1)
- Second line: m distinct integers p₁, p₂, ..., pₘ (affected settlements)
- Next n-1 lines: pairs of integers describing paths

#### Output Format
Print the number of settlements that may contain the Book of Evil. Print 0 if no valid settlement exists.

#### Solution

##### Approach
A settlement can contain the Book if its maximum distance to any affected settlement is ≤ d.

Key insight: The farthest affected settlement from any node must be one of the two endpoints of the "diameter" of affected settlements.

1. Find the two endpoints (u, v) of the diameter among affected settlements using two BFS/DFS
2. For each settlement, check if max(dist to u, dist to v) ≤ d

##### Python Solution

```python
from collections import deque

def solve():
  n, m, d = map(int, input().split())
  affected = set(map(int, input().split()))

  adj = [[] for _ in range(n + 1)]
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  def bfs(start):
    """Returns distances from start to all nodes"""
    dist = [-1] * (n + 1)
    dist[start] = 0
    queue = deque([start])

    while queue:
      u = queue.popleft()
      for v in adj[u]:
        if dist[v] == -1:
          dist[v] = dist[u] + 1
          queue.append(v)

    return dist

  # Find first endpoint: farthest affected node from any affected node
  first_affected = next(iter(affected))
  dist_from_first = bfs(first_affected)

  u = max(affected, key=lambda x: dist_from_first[x])

  # Find second endpoint: farthest affected node from u
  dist_from_u = bfs(u)
  v = max(affected, key=lambda x: dist_from_u[x])

  # Get distances from both endpoints
  dist_from_v = bfs(v)

  # Count settlements where max distance to affected is <= d
  result = 0
  for i in range(1, n + 1):
    if max(dist_from_u[i], dist_from_v[i]) <= d:
      result += 1

  print(result)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
import sys
sys.setrecursionlimit(200000)

def solve():
  n, m, d = map(int, input().split())
  affected = list(map(int, input().split()))
  affected_set = set(affected)

  adj = [[] for _ in range(n + 1)]
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  def dfs(start):
    dist = [-1] * (n + 1)
    dist[start] = 0
    stack = [start]

    while stack:
      u = stack.pop()
      for v in adj[u]:
        if dist[v] == -1:
          dist[v] = dist[u] + 1
          stack.append(v)

    return dist

  # Find diameter endpoints among affected nodes
  dist1 = dfs(affected[0])
  u = max(affected, key=lambda x: dist1[x])

  dist_u = dfs(u)
  v = max(affected, key=lambda x: dist_u[x])

  dist_v = dfs(v)

  # Count valid positions
  count = sum(1 for i in range(1, n + 1)
        if max(dist_u[i], dist_v[i]) <= d)

  print(count)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N) - three BFS/DFS traversals
- **Space Complexity:** O(N) for adjacency list and distance arrays

##### Key Insight
For a tree, the maximum distance from any node to the affected set is determined by the two farthest apart affected nodes (the "diameter" of affected nodes). If a settlement is within distance d from both endpoints of this diameter, it's within distance d from all affected settlements.

---

### Fox and Names

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Fox Ciel is going to publish a paper on FOCS (Foxes Operated Computer Systems). She heard a rumor: the authors list on the paper is always sorted in the lexicographical order.

After checking some examples, she found out that sometimes it wasn't true. On some papers authors' names weren't sorted in lexicographical order in normal sense. But it was always true that after some modification of the order of letters in alphabet, the order of authors becomes lexicographical!

She wants to know, if there exists an order of letters in Latin alphabet such that the names on the paper she is submitting are following in the lexicographical order. If so, you should find out any such order.

Lexicographical order is defined in following way. When we compare s and t, first we find the leftmost position with differing characters: si ≠ ti. If there is no such position (i.e. s is a prefix of t or vice versa) the shortest string is less. Otherwise, we compare characters si and ti according to their order in alphabet.

#### Input Format
- The first line contains an integer n (1 ≤ n ≤ 100): number of names.
- Each of the following n lines contain one string namei (1 ≤ |namei| ≤ 100), the i-th name.
- Each name contains only lowercase Latin letters. All names are different.

#### Output Format
If there exists such order of letters that the given names are sorted lexicographically, output any such order as a permutation of characters 'a'-'z'.

Otherwise output a single word "Impossible" (without quotes).

#### Solution

##### Approach
1. Compare adjacent names to find character ordering constraints
2. Build a directed graph where an edge (u, v) means character u must come before v
3. Use topological sort to find a valid ordering
4. If a cycle exists, output "Impossible"
5. Special case: if a longer string is a prefix of a shorter one, it's impossible

##### Python Solution

```python
from collections import deque, defaultdict

def solve():
  n = int(input())
  names = [input().strip() for _ in range(n)]

  # Build graph
  graph = defaultdict(set)
  in_degree = {chr(ord('a') + i): 0 for i in range(26)}

  # Compare adjacent names
  for i in range(n - 1):
    s1, s2 = names[i], names[i + 1]
    min_len = min(len(s1), len(s2))

    found = False
    for j in range(min_len):
      if s1[j] != s2[j]:
        # s1[j] must come before s2[j] in the alphabet
        if s2[j] not in graph[s1[j]]:
          graph[s1[j]].add(s2[j])
          in_degree[s2[j]] += 1
        found = True
        break

    # If s1 is a prefix of s2, that's fine
    # But if s2 is a prefix of s1, it's impossible
    if not found and len(s1) > len(s2):
      print("Impossible")
      return

  # Topological sort using Kahn's algorithm
  queue = deque()
  for char in in_degree:
    if in_degree[char] == 0:
      queue.append(char)

  result = []
  while queue:
    char = queue.popleft()
    result.append(char)

    for neighbor in graph[char]:
      in_degree[neighbor] -= 1
      if in_degree[neighbor] == 0:
        queue.append(neighbor)

  # Check if all characters are included (no cycle)
  if len(result) != 26:
    print("Impossible")
  else:
    print(''.join(result))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n × L + 26) where L is the maximum name length
- **Space Complexity:** O(26²) for the graph

##### Example
For names ["hack", "heaven"], comparing:
- 'h' == 'h' ✓
- 'a' vs 'e' → 'a' must come before 'e'

The topological sort will produce an alphabet where 'a' comes before 'e'.

---

### Hierarchy

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1500ms
- **Memory Limit:** 1024MB

#### Problem Statement

A group of graduated students wants to establish a company hierarchy. One student will be the main boss, and each other student will have exactly one boss. Every boss has a strictly greater salary than all subordinates (no cycles).

K most successful students (numbered 1 to K) have given statements about who they want to be superior to. A superior means being the boss or one of the boss's superiors (not necessarily direct boss).

Create a hierarchy satisfying all successful students' wishes.

#### Input Format
- First line: N (total students, N ≤ 100000) and K (successful students, K < N)
- Next K lines: For student A, first an integer W (number of wishes, 1 ≤ W ≤ 10), then W integers representing students that A wants to be superior to

#### Output Format
Output N integers. The A-th integer is 0 if student A is the main boss, otherwise it's the boss of student A.

#### Solution

##### Approach
1. Build a directed graph where edge (A → B) means A wants to be superior to B
2. Perform topological sort to get a valid ordering
3. Assign each person's boss as the previous person in the topological order
4. The first person in the order becomes the main boss (0)

##### Python Solution

```python
from collections import defaultdict

def solve():
  n, k = map(int, input().split())

  adj = defaultdict(list)

  for u in range(k):
    line = list(map(int, input().split()))
    w = line[0]
    for i in range(1, w + 1):
      v = line[i] - 1  # 0-indexed
      adj[u].append(v)

  # DFS-based topological sort
  WHITE, GRAY, BLACK = 0, 1, 2
  color = [WHITE] * n
  topo_order = []

  def dfs(u):
    color[u] = GRAY
    for v in adj[u]:
      if color[v] == WHITE:
        dfs(v)
    color[u] = BLACK
    topo_order.append(u)

  for i in range(n):
    if color[i] == WHITE:
      dfs(i)

  topo_order.reverse()

  # Assign bosses
  boss = [0] * n
  boss[topo_order[0]] = 0  # Main boss

  for i in range(1, n):
    boss[topo_order[i]] = topo_order[i - 1] + 1  # 1-indexed output

  for i in range(n):
    print(boss[i])

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def solve():
  n, k = map(int, input().split())

  adj = [[] for _ in range(n)]

  for u in range(k):
    line = list(map(int, input().split()))
    w = line[0]
    for i in range(1, w + 1):
      v = line[i] - 1
      adj[u].append(v)

  # Iterative DFS for topological sort
  visited = [False] * n
  topo_order = []

  for start in range(n):
    if visited[start]:
      continue

    stack = [(start, False)]

    while stack:
      node, processed = stack.pop()

      if processed:
        topo_order.append(node)
        continue

      if visited[node]:
        continue

      visited[node] = True
      stack.append((node, True))

      for neighbor in adj[node]:
        if not visited[neighbor]:
          stack.append((neighbor, False))

  topo_order.reverse()

  # Assign bosses based on topological order
  boss = [0] * n
  for i in range(1, n):
    boss[topo_order[i]] = topo_order[i - 1] + 1

  for b in boss:
    print(b)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N + E) where E is total number of wishes
- **Space Complexity:** O(N + E) for adjacency list

##### Key Insight
The topological order gives us a valid hierarchy chain. If A must be superior to B, then A appears before B in topological order. By making each person's boss the immediately preceding person in this order, we create a chain that satisfies all constraints.

---

### King's Path

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

#### Problem Statement

A black king is on a chess field with 10^9 rows and 10^9 columns. Some cells are allowed, given as n segments. Each segment describes cells in columns from aᵢ to bᵢ in row rᵢ.

Find the minimum number of moves for the king to get from (x₀, y₀) to (x₁, y₁), moving only along allowed cells. A king can move to any of the 8 neighboring cells in one move.

#### Input Format
- First line: x₀, y₀, x₁, y₁ (initial and final positions)
- Second line: n (number of segments, 1 ≤ n ≤ 10^5)
- Next n lines: rᵢ, aᵢ, bᵢ (row and column range)
- Total length of all segments ≤ 10^5

#### Output Format
Print minimum moves, or -1 if no path exists.

#### Solution

##### Approach
Since total allowed cells ≤ 10^5, use BFS on the sparse graph. Store allowed cells in a set and use coordinate compression or direct hashing.

##### Python Solution

```python
from collections import deque

def solve():
  x0, y0, x1, y1 = map(int, input().split())
  n = int(input())

  allowed = set()
  allowed.add((x0, y0))
  allowed.add((x1, y1))

  for _ in range(n):
    r, a, b = map(int, input().split())
    for c in range(a, b + 1):
      allowed.add((r, c))

  # BFS
  dx = [0, 0, 1, -1, 1, -1, 1, -1]
  dy = [1, -1, 0, 0, 1, -1, -1, 1]

  dist = {(x0, y0): 0}
  queue = deque([(x0, y0)])

  while queue:
    x, y = queue.popleft()

    if (x, y) == (x1, y1):
      print(dist[(x, y)])
      return

    for i in range(8):
      nx, ny = x + dx[i], y + dy[i]

      if (nx, ny) in allowed and (nx, ny) not in dist:
        dist[(nx, ny)] = dist[(x, y)] + 1
        queue.append((nx, ny))

  print(-1)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
from collections import deque

def solve():
  x0, y0, x1, y1 = map(int, input().split())
  n = int(input())

  allowed = set()

  for _ in range(n):
    r, a, b = map(int, input().split())
    for c in range(a, b + 1):
      allowed.add((r, c))

  # King moves: 8 directions
  directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

  if (x0, y0) not in allowed or (x1, y1) not in allowed:
    print(-1)
    return

  visited = set()
  queue = deque([(x0, y0, 0)])
  visited.add((x0, y0))

  while queue:
    x, y, d = queue.popleft()

    if x == x1 and y == y1:
      print(d)
      return

    for dx, dy in directions:
      nx, ny = x + dx, y + dy
      if (nx, ny) in allowed and (nx, ny) not in visited:
        visited.add((nx, ny))
        queue.append((nx, ny, d + 1))

  print(-1)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(S) where S is total number of allowed cells (≤ 10^5)
- **Space Complexity:** O(S) for storing allowed cells and BFS queue

##### Key Insight
Despite the huge grid (10^9 × 10^9), only up to 10^5 cells are allowed. We can store these in a set and run standard BFS. The key is using coordinate hashing or tuples to efficiently check if a cell is allowed.

---

### Topological Sorting

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

#### Problem Statement

Sandro is a well organised person. Every day he makes a list of things which need to be done and enumerates them from 1 to n. However, some things need to be done before others. Find out whether Sandro can solve all his duties and if so, print the correct order.

If there are multiple solutions, print the one whose first number is smallest, if there are still multiple solutions, print the one whose second number is smallest, and so on (lexicographically smallest).

#### Input Format
- First line: n and m (1 ≤ n ≤ 10000, 1 ≤ m ≤ 1000000)
- Next m lines: two distinct integers x and y (1 ≤ x, y ≤ n) meaning job x needs to be done before job y

#### Output Format
- Print "Sandro fails." if there's a cycle (impossible to complete all duties)
- Otherwise, print the correct ordering with jobs separated by whitespace

#### Solution

##### Approach
Use Kahn's algorithm (BFS-based topological sort) with a **min-heap** instead of a regular queue to ensure lexicographically smallest ordering.

##### Python Solution

```python
import heapq
from collections import defaultdict

def solve():
  n, m = map(int, input().split())

  adj = defaultdict(list)
  in_degree = [0] * (n + 1)

  for _ in range(m):
    x, y = map(int, input().split())
    adj[x].append(y)
    in_degree[y] += 1

  # Min-heap for lexicographically smallest order
  heap = []
  for i in range(1, n + 1):
    if in_degree[i] == 0:
      heapq.heappush(heap, i)

  result = []

  while heap:
    u = heapq.heappop(heap)
    result.append(u)

    for v in adj[u]:
      in_degree[v] -= 1
      if in_degree[v] == 0:
        heapq.heappush(heap, v)

  if len(result) < n:
    print("Sandro fails.")
  else:
    print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(20000)

def solve():
  n, m = map(int, input().split())

  adj = defaultdict(list)

  for _ in range(m):
    x, y = map(int, input().split())
    adj[x].append(y)

  # Sort adjacency lists in reverse for lexicographic order with DFS
  for u in adj:
    adj[u].sort(reverse=True)

  WHITE, GRAY, BLACK = 0, 1, 2
  color = [WHITE] * (n + 1)
  result = []
  has_cycle = False

  def dfs(u):
    nonlocal has_cycle
    if has_cycle:
      return

    color[u] = GRAY

    for v in adj[u]:
      if color[v] == GRAY:
        has_cycle = True
        return
      if color[v] == WHITE:
        dfs(v)

    color[u] = BLACK
    result.append(u)

  # Process vertices in order for lexicographic result
  for i in range(n, 0, -1):
    if color[i] == WHITE:
      dfs(i)

  if has_cycle or len(result) < n:
    print("Sandro fails.")
  else:
    result.reverse()
    print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(V + E) for topological sort, O(V log V) for heap operations
- **Space Complexity:** O(V + E) for adjacency list

##### Key Insight
Using a min-heap (priority queue) instead of a regular queue in Kahn's algorithm ensures that we always process the smallest available vertex, producing the lexicographically smallest topological ordering.

