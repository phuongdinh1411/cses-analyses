---
difficulty: Easy
tags: [graph, bfs, shortest-path, path-reconstruction]
cses_link: https://cses.fi/problemset/task/1667
---

# Message Route

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find shortest path from computer 1 to computer n |
| Graph Type | Unweighted, undirected |
| Algorithm | BFS (Breadth-First Search) |
| Key Technique | Parent tracking for path reconstruction |
| Time Complexity | O(n + m) |
| Space Complexity | O(n + m) |

## Learning Goals

1. Build an adjacency list from edge input
2. Use BFS to find shortest paths in unweighted graphs
3. Reconstruct paths using a parent array
4. Handle the "IMPOSSIBLE" case when no path exists

## Problem Statement

Syrjala's network has `n` computers and `m` connections. Find the minimum-hop route from computer 1 to computer n, or report "IMPOSSIBLE" if no path exists.

**Input:** n, m followed by m edges (a, b)
**Output:** Number of computers on route + the route, or "IMPOSSIBLE"

**Example:**
```
Input:        Output:
5 5           3
1 2           1 4 5
1 3
1 4
2 3
5 4
```

## Key Insight

**BFS guarantees the shortest path in an unweighted graph.**

BFS explores nodes level by level. The first time we reach any node is via the shortest path.

```
BFS Levels:
- Level 0: Start node (distance 0)
- Level 1: All nodes 1 edge away
- Level 2: All nodes 2 edges away
- ...and so on
```

## Algorithm Steps

### Step 1: Build Adjacency List
```python
adj = [[] for _ in range(n + 1)]  # 1-indexed
for a, b in edges:
 adj[a].append(b)
 adj[b].append(a)  # Bidirectional!
```

### Step 2: BFS with Parent Tracking
```python
from collections import deque

parent = [-1] * (n + 1)
parent[1] = 0  # Sentinel for start node
queue = deque([1])

while queue:
 u = queue.popleft()
 if u == n: break
 for v in adj[u]:
  if parent[v] == -1:
   parent[v] = u
   queue.append(v)
```

### Step 3: Check & Reconstruct Path
```python
if parent[n] == -1:
 print("IMPOSSIBLE")
else:
 path = []
 cur = n
 while cur != 0:
  path.append(cur)
  cur = parent[cur]
 path.reverse()
 print(len(path))
 print(*path)
```

## Visual Diagram: BFS Levels

```
Example Graph:        BFS from node 1:
    1 --- 2
    |     |           Level 0: [1]         dist=0
    3 --- 4 --- 5     Level 1: [2,3,4]     dist=1
                      Level 2: [5]         dist=2

Parent array:  [0, 1, 1, 1, 4]  (index = node, value = parent)
               ^-sentinel

Path reconstruction: 5 -> 4 -> 1 -> 0(stop), reverse: [1, 4, 5]
```

## Dry Run

**Input:** n=5, edges: (1,2), (1,3), (1,4), (2,3), (5,4)

```
Adjacency: 1:[2,3,4], 2:[1,3], 3:[1,2], 4:[1,5], 5:[4]

Step | Queue     | Action              | Parent Array
-----|-----------|---------------------|-------------------
  1  | [1]       | Pop 1, add 2,3,4    | [0,-1,-1,-1,-1,-1]
  2  | [2,3,4]   | Pop 2, 1,3 visited  | [0, 0, 1, 1, 1,-1]
  3  | [3,4]     | Pop 3, 1,2 visited  | (unchanged)
  4  | [4]       | Pop 4, add 5        | [0, 0, 1, 1, 1, 4]
  5  | [5]       | Pop 5, u==n, DONE   |

Path: 5->4->1, reverse: [1,4,5], length: 3
```

## Python Solution

```python
from collections import deque
import sys
input = sys.stdin.readline

def solve():
 n, m = map(int, input().split())

 adj = [[] for _ in range(n + 1)]
 for _ in range(m):
  a, b = map(int, input().split())
  adj[a].append(b)
  adj[b].append(a)

 parent = [-1] * (n + 1)
 parent[1] = 0
 queue = deque([1])

 while queue:
  u = queue.popleft()
  if u == n:
   break
  for v in adj[u]:
   if parent[v] == -1:
    parent[v] = u
    queue.append(v)

 if parent[n] == -1:
  print("IMPOSSIBLE")
  return

 path = []
 cur = n
 while cur != 0:
  path.append(cur)
  cur = parent[cur]
 path.reverse()

 print(len(path))
 print(*path)

solve()
```

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Using DFS | DFS doesn't guarantee shortest path | Use BFS |
| One-way edges | Graph is undirected | Add both `adj[a].push_back(b)` AND `adj[b].push_back(a)` |
| Wrong array size | Nodes are 1-indexed | Use size `n+1` for arrays |
| No path check | May crash on disconnected graph | Check `parent[n] != -1` before reconstruction |

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build adjacency list | O(m) | O(n + m) |
| BFS traversal | O(n + m) | O(n) |
| Path reconstruction | O(n) | O(n) |
| **Total** | **O(n + m)** | **O(n + m)** |

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| Word Ladder | LeetCode | Implicit graph from word transformations |
| Shortest Path in Binary Matrix | LeetCode | Grid-based, 8 directions |
| Labyrinth (CSES) | CSES | Grid graph, output directions |
| Shortest Routes I (CSES) | CSES | Weighted edges, use Dijkstra |
