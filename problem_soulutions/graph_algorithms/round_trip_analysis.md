---
layout: simple
title: "Round Trip - Cycle Detection in Undirected Graph"
permalink: /problem_soulutions/graph_algorithms/round_trip_analysis
difficulty: Medium
tags: [graph, dfs, cycle-detection, undirected]
cses_link: https://cses.fi/problemset/task/1669
---

# Round Trip - Cycle Detection in Undirected Graph

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find a cycle (round trip) in an undirected graph |
| Input | n cities, m bidirectional roads |
| Output | Cycle path starting and ending at same city, or "IMPOSSIBLE" |
| Constraints | 2 <= n <= 10^5, 1 <= m <= 2*10^5 |
| Time Limit | 1 second |

## Learning Goals

After solving this problem, you will understand:
1. **Cycle detection in undirected graphs** - How back edges indicate cycles
2. **Parent tracking during DFS** - Why we need to track where we came from
3. **Cycle extraction** - How to reconstruct the cycle path using parent pointers

## Problem Statement

Byteland has n cities and m roads. Each road connects two cities bidirectionally. Your task is to find a route that starts from a city, visits at least one other city, and returns to the starting city. All roads on the route must be distinct.

**Input:**
- First line: n (cities) and m (roads)
- Next m lines: two integers a and b (road between cities a and b)

**Output:**
- If a round trip exists: first line is the number of cities, second line is the route
- If no round trip exists: print "IMPOSSIBLE"

**Example:**
```
Input:
5 6
1 3
1 2
5 3
1 5
2 4
4 5

Output:
4
3 5 1 3
```

## Key Insight: Back Edge Detection

In an undirected graph, a **cycle exists if and only if** we encounter an already-visited node that is NOT our immediate parent during DFS.

```
Why parent check matters:

    1 --- 2          When at node 2, we see node 1 is visited.
                     But 1 is our parent (we came from 1).
                     This is NOT a cycle - just the edge we used!

    1 --- 2          When at node 3, we see node 1 is visited.
     \   /           Node 1 is NOT our parent (parent is 2).
      \ /            This IS a cycle: 1 -> 2 -> 3 -> 1
       3
```

**Key difference from directed graphs:** In directed graphs, we use colors (white/gray/black) to detect back edges. In undirected graphs, we simply check if visited node != parent.

## Algorithm: DFS with Parent Tracking

```
1. Build adjacency list from edges
2. For each unvisited node, start DFS:
   a. Mark current node as visited
   b. For each neighbor:
      - If unvisited: set parent[neighbor] = current, recurse
      - If visited AND neighbor != parent[current]: CYCLE FOUND!
3. When cycle found at edge (u, v) where v is already visited:
   - Trace back from u to v using parent pointers
   - This gives us the cycle path
```

## Visual: DFS Tree and Back Edge

```
Original Graph:              DFS Tree:

    1 --- 2                     1 (root)
     \   /                      |
      \ /                       2
       3                        |
       |                        3 --- back edge to 1!
       4                        |
                                4

DFS traversal from node 1:
- Visit 1, parent[1] = -1
- Visit 2, parent[2] = 1
- Visit 3, parent[3] = 2
- At 3, see neighbor 1: visited AND 1 != parent[3] (which is 2)
- CYCLE FOUND! Back edge: 3 -> 1

Cycle extraction:
- Start at 3, trace parents until we reach 1
- Path: 3 -> 2 -> 1, then add 3 again
- Cycle: [1, 2, 3, 1] or equivalently [3, 2, 1, 3]
```

## Dry Run Example

```
Input: n=5, m=6
Edges: (1,3), (1,2), (5,3), (1,5), (2,4), (4,5)

Adjacency List:
1: [3, 2, 5]
2: [1, 4]
3: [1, 5]
4: [2, 5]
5: [3, 1, 4]

DFS from node 1:
Step 1: Visit 1, parent[1]=-1, visited={1}
Step 2: Go to neighbor 3, parent[3]=1, visited={1,3}
Step 3: From 3, go to neighbor 5, parent[5]=3, visited={1,3,5}
Step 4: From 5, check neighbor 3 -> visited, parent[5]=3, SKIP (it's parent)
Step 5: From 5, check neighbor 1 -> visited, parent[5]=3, 1 != 3
        CYCLE FOUND! Back edge: 5 -> 1

Cycle Extraction:
- cycle_end = 1, current = 5
- Trace: 5 -> parent[5]=3 -> parent[3]=1 = cycle_end, STOP
- Cycle: [1, 3, 5, 1]

Output: 4 cities, path: 1 3 5 1
```

## Python Solution

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(200005)

def solve():
  n, m = map(int, input().split())

  adj = defaultdict(list)
  for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  visited = [False] * (n + 1)
  parent = [-1] * (n + 1)
  cycle = []

  def dfs(u):
    visited[u] = True
    for v in adj[u]:
      if not visited[v]:
        parent[v] = u
        if dfs(v):
          return True
      elif v != parent[u]:
        # Found cycle! Extract it
        cycle.append(v)
        curr = u
        while curr != v:
          cycle.append(curr)
          curr = parent[curr]
        cycle.append(v)
        return True
    return False

  # Try DFS from each unvisited node (handles disconnected graphs)
  for start in range(1, n + 1):
    if not visited[start]:
      if dfs(start):
        print(len(cycle))
        print(*cycle)
        return

  print("IMPOSSIBLE")

solve()
```

## Handling Disconnected Graphs

The graph may have multiple connected components. A cycle can exist in any component, so we must try DFS from each unvisited node:

```python
for start in range(1, n + 1):
  if not visited[start]:
    if dfs(start):  # Found cycle in this component
      return
```

If no component contains a cycle, we output "IMPOSSIBLE".

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Not tracking parent | Will detect the edge you just came from as a "cycle" | Always track `parent[v] = u` before recursing |
| Using directed graph algorithm | Colors (white/gray/black) are for directed graphs | For undirected, just check `v != parent[u]` |
| Only starting DFS from node 1 | Misses cycles in disconnected components | Loop through all nodes, start DFS from unvisited ones |
| Wrong cycle extraction order | Cycle might be reversed | Either order is valid as long as start == end |
| Off-by-one with 1-indexed nodes | Array out of bounds | Use size `n+1` for 1-indexed problems |

## Output Format

The cycle must:
1. Start and end with the **same city**
2. Have length >= 3 (at least 3 cities including the repeated endpoint)
3. Use distinct roads (automatically satisfied by our DFS approach)

```
Valid:   3 1 5 3     (starts and ends at 3)
Valid:   1 2 4 5 1   (starts and ends at 1)
Invalid: 1 2 1       (only 2 distinct cities, not a valid cycle for this problem)
```

## Complexity Analysis

| Aspect | Complexity | Reason |
|--------|-----------|--------|
| Time | O(n + m) | Each node and edge visited at most once |
| Space | O(n + m) | Adjacency list + visited/parent arrays |

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|---------------|
| [Course Schedule](https://leetcode.com/problems/course-schedule/) | LeetCode | Directed graph, detect if cycle exists (no extraction) |
| [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | LeetCode | Directed graph, topological sort |
| [Round Trip II](https://cses.fi/problemset/task/1678) | CSES | Directed graph version of this problem |
| [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | LeetCode | Find the edge that creates a cycle (Union-Find) |
