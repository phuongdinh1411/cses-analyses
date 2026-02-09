# Topological Sorting

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

## Problem Statement

Sandro is a well organised person. Every day he makes a list of things which need to be done and enumerates them from 1 to n. However, some things need to be done before others. Find out whether Sandro can solve all his duties and if so, print the correct order.

If there are multiple solutions, print the one whose first number is smallest, if there are still multiple solutions, print the one whose second number is smallest, and so on (lexicographically smallest).

## Input Format
- First line: n and m (1 ≤ n ≤ 10000, 1 ≤ m ≤ 1000000)
- Next m lines: two distinct integers x and y (1 ≤ x, y ≤ n) meaning job x needs to be done before job y

## Output Format
- Print "Sandro fails." if there's a cycle (impossible to complete all duties)
- Otherwise, print the correct ordering with jobs separated by whitespace

## Example
```
Input:
5 4
1 2
2 3
1 3
1 5

Output:
1 2 4 3 5
```
Jobs 1 must be done before 2, 3, and 5. Job 2 must be done before 3. Job 4 has no dependencies. The lexicographically smallest valid ordering is 1, 2, 4, 3, 5.

## Solution

### Approach
Use Kahn's algorithm (BFS-based topological sort) with a **min-heap** instead of a regular queue to ensure lexicographically smallest ordering.

### Python Solution

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

### Alternative Solution with DFS

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

### Complexity Analysis
- **Time Complexity:** O(V + E) for topological sort, O(V log V) for heap operations
- **Space Complexity:** O(V + E) for adjacency list

### Key Insight
Using a min-heap (priority queue) instead of a regular queue in Kahn's algorithm ensures that we always process the smallest available vertex, producing the lexicographically smallest topological ordering.
