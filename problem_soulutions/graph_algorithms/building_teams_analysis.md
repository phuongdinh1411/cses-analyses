---
layout: problem-analysis
title: "Building Teams"
difficulty: Easy
tags: [graph, bipartite, bfs, dfs, 2-coloring]
cses_link: https://cses.fi/problemset/task/1668
---

# Building Teams

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Divide n pupils into 2 teams so no two friends are on the same team |
| Input | n pupils, m friendships (edges) |
| Output | Team assignment (1 or 2) for each pupil, or "IMPOSSIBLE" |
| Constraints | 1 <= n <= 10^5, 1 <= m <= 2*10^5 |
| Core Concept | Bipartite graph checking / 2-coloring |
| Time Complexity | O(n + m) |

## Learning Goals

After solving this problem, you will understand:
1. **Bipartite Graphs**: A graph whose vertices can be divided into two disjoint sets such that every edge connects vertices from different sets
2. **Graph 2-Coloring**: Assigning one of two colors to each vertex so adjacent vertices have different colors
3. **Odd Cycle Detection**: Why odd-length cycles make bipartite coloring impossible

## Problem Statement

There are n pupils and m friendships. Your task is to divide the pupils into two teams such that no two pupils in the same team are friends. If this is possible, output the team assignment; otherwise, output "IMPOSSIBLE".

**Example Input:**
```
5 3
1 2
2 3
3 4
```

**Example Output:**
```
1 2 1 2 1
```

## Key Insight

This problem is equivalent to checking if the graph is **bipartite**.

A graph is bipartite if and only if it contains **no odd-length cycles**.

Why? When you traverse a cycle and alternate colors:
- Even-length cycle: You return to the start with the opposite color (valid)
- Odd-length cycle: You return to the start with the SAME color (conflict!)

## Algorithm: BFS/DFS 2-Coloring

**Core idea**: Start from any uncolored vertex, assign it color 1, then assign the opposite color to all neighbors. If we ever find a neighbor with the same color, the graph is not bipartite.

**Steps:**
1. Build adjacency list from friendships
2. Initialize all vertices as uncolored (-1 or 0)
3. For each uncolored vertex (handles disconnected components!):
   - Start BFS/DFS from this vertex
   - Assign alternating colors to neighbors
   - If a neighbor already has the same color as current vertex -> IMPOSSIBLE
4. Output the color assignment

## Handling Disconnected Components

**Critical**: The graph may have multiple disconnected components. You must check EACH component separately!

```
Component 1: 1--2--3     Component 2: 4--5
```

If you only start from vertex 1, vertices 4 and 5 remain uncolored. Always iterate through all vertices and start a new BFS/DFS from any uncolored vertex.

## Visual Diagram

**Case 1: Valid 2-Coloring (Even Cycle / Tree)**
```
    1(A) --- 2(B)
      |       |
    4(B) --- 3(A)

Colors alternate around the cycle (length 4 = even)
Team A: {1, 3}    Team B: {2, 4}
```

**Case 2: Impossible (Odd Cycle)**
```
    1(A) --- 2(B)
      \     /
       \   /
        3(?)

Starting from 1(A):
  - 2 gets color B (opposite of A)
  - 3 gets color A (opposite of B)
  - But 3 is connected to 1, which is also A!

CONFLICT! Triangle (length 3 = odd) cannot be 2-colored.
```

## Dry Run Example

**Input:** n=5, m=3, edges: (1,2), (2,3), (3,4)

```
Initial graph:
1 --- 2 --- 3 --- 4     5 (isolated)

Step 1: Start BFS from vertex 1
  color[1] = 1
  Queue: [1]

Step 2: Process vertex 1
  Neighbor 2: uncolored -> color[2] = 2
  Queue: [2]

Step 3: Process vertex 2
  Neighbor 1: color[1]=1 != color[2]=2 (OK)
  Neighbor 3: uncolored -> color[3] = 1
  Queue: [3]

Step 4: Process vertex 3
  Neighbor 2: color[2]=2 != color[3]=1 (OK)
  Neighbor 4: uncolored -> color[4] = 2
  Queue: [4]

Step 5: Process vertex 4
  Neighbor 3: color[3]=1 != color[4]=2 (OK)
  Queue: []

Step 6: Vertex 5 is still uncolored (disconnected!)
  Start new BFS from vertex 5
  color[5] = 1

Final: [1, 2, 1, 2, 1]
```

## Implementation: BFS Approach

### Python (BFS)
```python
from collections import deque

def solve():
  n, m = map(int, input().split())

  # Build adjacency list (1-indexed)
  adj = [[] for _ in range(n + 1)]
  for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  color = [0] * (n + 1)  # 0 = uncolored, 1 or 2 = team

  def bfs(start):
    queue = deque([start])
    color[start] = 1

    while queue:
      u = queue.popleft()
      for v in adj[u]:
        if color[v] == 0:
          color[v] = 3 - color[u]  # Alternate: 1->2, 2->1
          queue.append(v)
        elif color[v] == color[u]:
          return False  # Same color = conflict
    return True

  # Check ALL components
  for i in range(1, n + 1):
    if color[i] == 0:
      if not bfs(i):
        print("IMPOSSIBLE")
        return

  print(*color[1:])

solve()
```

### Python (DFS)
```python
import sys
sys.setrecursionlimit(200005)

def solve():
  n, m = map(int, input().split())

  adj = [[] for _ in range(n + 1)]
  for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  color = [0] * (n + 1)
  possible = True

  def dfs(u, c):
    nonlocal possible
    color[u] = c
    for v in adj[u]:
      if color[v] == 0:
        dfs(v, 3 - c)
      elif color[v] == c:
        possible = False

  for i in range(1, n + 1):
    if color[i] == 0:
      dfs(i, 1)

  if possible:
    print(*color[1:])
  else:
    print("IMPOSSIBLE")

solve()
```

## Why Odd Cycle = Impossible

Consider walking around a cycle and assigning alternating colors:

```
Vertex:  v1 -> v2 -> v3 -> ... -> vk -> v1
Color:    A     B     A    ...    ?     A

If k is EVEN:  vk gets color B, connects back to v1(A) - OK!
If k is ODD:   vk gets color A, connects back to v1(A) - CONFLICT!
```

The mathematical reason: In a cycle of length k, vertex vi gets color based on (i mod 2). If k is odd, vertex vk and v1 have the same parity, hence the same color.

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build adjacency list | O(m) | O(n + m) |
| BFS/DFS traversal | O(n + m) | O(n) for queue/stack |
| **Total** | **O(n + m)** | **O(n + m)** |

## Common Mistakes

1. **Forgetting disconnected components**: Only running BFS/DFS from vertex 1 misses isolated components
   ```python
 # WRONG: Only starts from vertex 1
 bfs(1)

 # CORRECT: Check all vertices
 for i in range(1, n + 1):
   if color[i] == 0:
     bfs(i)
 ```

2. **Wrong initial color check**: Using 0 as a valid color instead of "uncolored"
   ```python
 # WRONG: 0 could be confused with unvisited
 color = [0] * n  # Is 0 a team or unvisited?

 # CORRECT: Use distinct values
 color = [0] * n  # 0 = unvisited, 1 and 2 = teams
 # OR
 color = [-1] * n  # -1 = unvisited, 0 and 1 = teams
 ```

3. **Not handling self-loops**: A self-loop (edge from v to v) makes the graph non-bipartite

4. **Stack overflow with DFS**: For large graphs, use iterative DFS or increase recursion limit

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) | LeetCode | Same problem, 0-indexed |
| [Possible Bipartition](https://leetcode.com/problems/possible-bipartition/) | LeetCode | Dislikes instead of friendships |
| [Round Trip](https://cses.fi/problemset/task/1669) | CSES | Find the actual odd cycle |
