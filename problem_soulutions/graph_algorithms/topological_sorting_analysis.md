---
layout: simple
title: "Topological Sorting - CSES Problem Analysis"
permalink: /problem_soulutions/graph_algorithms/topological_sorting_analysis
difficulty: Easy
tags: [graph, topological-sort, dag, bfs, dfs]
cses_link: https://cses.fi/problemset/task/1679
---

# Topological Sorting

## Problem Overview

| Attribute       | Value                                    |
|-----------------|------------------------------------------|
| Problem         | Course Scheduling / Topological Sort     |
| Difficulty      | Easy                                     |
| Category        | Graph Algorithms                         |
| Time Complexity | O(n + m)                                 |
| Space Complexity| O(n + m)                                 |
| Key Technique   | Kahn's Algorithm (BFS) / DFS Post-order  |

## Learning Goals

By completing this problem, you will learn:
1. **Topological Sorting**: Linear ordering of vertices in a DAG
2. **Kahn's Algorithm (BFS)**: In-degree based iterative approach
3. **DFS-based Approach**: Post-order traversal with reversal
4. **Cycle Detection**: Identifying when topological sort is impossible

## Problem Statement

You have `n` courses and `m` requirements. Each requirement states that course `a` must be completed before course `b`. Find a valid order to complete all courses, or report "IMPOSSIBLE" if no valid order exists (cycle detected).

**Input:**
- First line: n (courses), m (requirements)
- Next m lines: pairs (a, b) meaning a must come before b

**Output:**
- A valid course ordering, or "IMPOSSIBLE"

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 x 10^5

**Example:**
```
Input:
5 3
1 2
2 3
4 5

Output:
1 4 2 5 3
```

## What is Topological Sort?

**Definition:** A linear ordering of vertices in a directed graph such that for every directed edge u -> v, vertex u comes before vertex v in the ordering.

**Key Property:** Topological sorting is only possible for **DAGs** (Directed Acyclic Graphs). If the graph contains a cycle, no valid topological order exists.

```
Valid DAG:              Graph with Cycle:
  1 --> 2 --> 3           1 --> 2
  |           ^           ^     |
  v           |           |     v
  4 --------->+           4 <-- 3

Topological Order:      NO topological order
[1, 4, 2, 3] or         exists (cycle: 1->2->3->4->1)
[1, 2, 4, 3]
```

## Approach 1: Kahn's Algorithm (BFS)

### Algorithm Steps

1. **Compute in-degrees**: Count incoming edges for each vertex
2. **Initialize queue**: Add all vertices with in-degree 0
3. **Process queue**: Remove vertex, add to result, decrement neighbors' in-degrees
4. **Add new sources**: When a vertex reaches in-degree 0, add to queue
5. **Cycle check**: If processed vertices < n, a cycle exists

### Visual Walkthrough

```
Graph: 1->2, 1->4, 2->3, 4->3

Initial State:
  Vertices:    1   2   3   4
  In-degree:   0   1   2   1
  Queue: [1]
  Result: []

Step 1: Process vertex 1
  - Remove 1 from queue
  - Add 1 to result
  - Decrement in-degree of neighbors (2, 4)

  In-degree:   0   0   2   0
  Queue: [2, 4]
  Result: [1]

Step 2: Process vertex 2
  - Remove 2 from queue
  - Add 2 to result
  - Decrement in-degree of 3

  In-degree:   0   0   1   0
  Queue: [4]
  Result: [1, 2]

Step 3: Process vertex 4
  - Remove 4 from queue
  - Add 4 to result
  - Decrement in-degree of 3

  In-degree:   0   0   0   0
  Queue: [3]
  Result: [1, 2, 4]

Step 4: Process vertex 3
  - Remove 3 from queue
  - Add 3 to result

  Queue: []
  Result: [1, 2, 4, 3]

Final: 4 vertices processed = n, valid topological order!
```

### Python Implementation (Kahn's BFS)

```python
from collections import deque

def topological_sort_bfs(n, edges):
  """Kahn's algorithm for topological sorting."""
  # Build adjacency list and compute in-degrees
  adj = [[] for _ in range(n + 1)]
  in_degree = [0] * (n + 1)

  for a, b in edges:
    adj[a].append(b)
    in_degree[b] += 1

  # Initialize queue with vertices having in-degree 0
  queue = deque()
  for i in range(1, n + 1):
    if in_degree[i] == 0:
      queue.append(i)

  result = []

  while queue:
    node = queue.popleft()
    result.append(node)

    for neighbor in adj[node]:
      in_degree[neighbor] -= 1
      if in_degree[neighbor] == 0:
        queue.append(neighbor)

  # Cycle detection: if not all vertices processed
  if len(result) != n:
    return None  # IMPOSSIBLE

  return result

# Read input and solve
n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]

result = topological_sort_bfs(n, edges)
if result:
  print(' '.join(map(str, result)))
else:
  print("IMPOSSIBLE")
```

## Approach 2: DFS-based Topological Sort

### Algorithm Steps

1. **Track states**: Use colors (WHITE=unvisited, GRAY=in-progress, BLACK=done)
2. **DFS traversal**: Visit all unvisited vertices
3. **Post-order recording**: Add vertex to result after all descendants processed
4. **Cycle detection**: If we reach a GRAY vertex, cycle exists
5. **Reverse result**: Post-order gives reverse topological order

### Visual Walkthrough

```
Graph: 1->2, 1->4, 2->3, 4->3

DFS from vertex 1:

Call Stack          State           Post-order Stack
-----------         -----           ----------------
dfs(1)              1: GRAY         []
  dfs(2)            2: GRAY         []
    dfs(3)          3: GRAY         []
    return          3: BLACK        [3]
  return            2: BLACK        [3, 2]
  dfs(4)            4: GRAY         [3, 2]
    3 is BLACK, skip
  return            4: BLACK        [3, 2, 4]
return              1: BLACK        [3, 2, 4, 1]

Reverse post-order: [1, 4, 2, 3] -> Valid topological order!

Cycle Detection Example:
Graph: 1->2, 2->3, 3->1

dfs(1)              1: GRAY
  dfs(2)            2: GRAY
    dfs(3)          3: GRAY
      Neighbor 1 is GRAY -> CYCLE DETECTED!
```

### Python Implementation (DFS)

```python
import sys
sys.setrecursionlimit(200005)

def topological_sort_dfs(n, edges):
  """DFS-based topological sorting with cycle detection."""
  adj = [[] for _ in range(n + 1)]
  for a, b in edges:
    adj[a].append(b)

  WHITE, GRAY, BLACK = 0, 1, 2
  color = [WHITE] * (n + 1)
  result = []
  has_cycle = False

  def dfs(node):
    nonlocal has_cycle
    if has_cycle:
      return

    color[node] = GRAY

    for neighbor in adj[node]:
      if color[neighbor] == GRAY:
        has_cycle = True
        return
      if color[neighbor] == WHITE:
        dfs(neighbor)

    color[node] = BLACK
    result.append(node)

  for i in range(1, n + 1):
    if color[i] == WHITE:
      dfs(i)
      if has_cycle:
        return None

  result.reverse()
  return result

# Read input and solve
n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]

result = topological_sort_dfs(n, edges)
if result:
  print(' '.join(map(str, result)))
else:
  print("IMPOSSIBLE")
```

## Dry Run Example

**Input:**
```
5 4
1 2
2 3
1 3
4 5
```

**Graph Visualization:**
```
1 ---> 2

|      |
v      v
+----> 3      4 ---> 5
```

**Kahn's Algorithm Execution:**
```
Step  | Queue     | In-degrees [1,2,3,4,5] | Result
------|-----------|------------------------|--------
Init  | [1, 4]    | [0, 1, 2, 0, 1]        | []
1     | [4, 2]    | [0, 0, 1, 0, 1]        | [1]
2     | [2, 5]    | [0, 0, 1, 0, 0]        | [1, 4]
3     | [5, 3]    | [0, 0, 0, 0, 0]        | [1, 4, 2]
4     | [3]       | [0, 0, 0, 0, 0]        | [1, 4, 2, 5]
5     | []        | [0, 0, 0, 0, 0]        | [1, 4, 2, 5, 3]

Output: 1 4 2 5 3
```

## Complexity Analysis

| Approach | Time       | Space      | Notes                           |
|----------|------------|------------|---------------------------------|
| Kahn's   | O(n + m)   | O(n + m)   | Iterative, good for large graphs|
| DFS      | O(n + m)   | O(n + m)   | Recursive, risk of stack overflow|

Both approaches visit each vertex and edge exactly once.

## Common Mistakes

1. **Forgetting cycle detection**: Always check if all nodes were processed (Kahn's) or track GRAY nodes (DFS)

2. **Wrong order in DFS**: Must reverse the post-order result. Adding to front of list or reversing at end

3. **1-indexed vs 0-indexed**: CSES uses 1-indexed vertices. Ensure arrays are sized correctly

4. **Not handling disconnected components**: Start BFS/DFS from all unvisited vertices, not just vertex 1

5. **Stack overflow in DFS**: For large n, increase recursion limit (Python) or use iterative DFS

## Related Problems

| Problem                          | Platform  | Link                                              |
|----------------------------------|-----------|---------------------------------------------------|
| Course Schedule                  | LeetCode  | https://leetcode.com/problems/course-schedule/    |
| Course Schedule II               | LeetCode  | https://leetcode.com/problems/course-schedule-ii/ |
| Alien Dictionary                 | LeetCode  | https://leetcode.com/problems/alien-dictionary/   |
| Game Routes                      | CSES      | https://cses.fi/problemset/task/1681              |
| Longest Flight Route             | CSES      | https://cses.fi/problemset/task/1680              |
