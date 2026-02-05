# Book of Evil

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

## Problem Statement

Paladin Manao is searching for the Book of Evil in a swampy area with n settlements connected by n-1 bidirectional paths (a tree). The Book has damage range d, meaning it affects settlements at distance d or less.

Manao knows m settlements that are affected. Determine how many settlements could possibly contain the Book of Evil.

## Input Format
- First line: n, m, d (1 ≤ m ≤ n ≤ 100000; 0 ≤ d ≤ n-1)
- Second line: m distinct integers p₁, p₂, ..., pₘ (affected settlements)
- Next n-1 lines: pairs of integers describing paths

## Output Format
Print the number of settlements that may contain the Book of Evil. Print 0 if no valid settlement exists.

## Solution

### Approach
A settlement can contain the Book if its maximum distance to any affected settlement is ≤ d.

Key insight: The farthest affected settlement from any node must be one of the two endpoints of the "diameter" of affected settlements.

1. Find the two endpoints (u, v) of the diameter among affected settlements using two BFS/DFS
2. For each settlement, check if max(dist to u, dist to v) ≤ d

### Python Solution

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

### Alternative Solution with DFS

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

### Complexity Analysis
- **Time Complexity:** O(N) - three BFS/DFS traversals
- **Space Complexity:** O(N) for adjacency list and distance arrays

### Key Insight
For a tree, the maximum distance from any node to the affected set is determined by the two farthest apart affected nodes (the "diameter" of affected nodes). If a settlement is within distance d from both endpoints of this diameter, it's within distance d from all affected settlements.
