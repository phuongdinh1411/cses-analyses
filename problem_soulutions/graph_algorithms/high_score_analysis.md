---
difficulty: Hard
tags: [graph, bellman-ford, longest-path, positive-cycle]
cses_link: https://cses.fi/problemset/task/1673
---

# High Score - Longest Path with Positive Cycles

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find maximum score from room 1 to room n |
| Core Challenge | Detect if infinite score is possible via positive cycles |
| Algorithm | Modified Bellman-Ford for longest path |
| Time Complexity | O(n * m) |
| Space Complexity | O(n + m) |
| Key Insight | Positive cycle on path from 1 to n = infinite score |

## Learning Goals

After studying this problem, you will understand:

1. **Longest Path in Graphs**: How to adapt shortest path algorithms for longest path
2. **Positive Cycle Detection**: Identifying cycles that increase score infinitely
3. **Bellman-Ford Modification**: Using Bellman-Ford for maximization instead of minimization
4. **Reachability Analysis**: Why a cycle must be on a valid path to matter

## Problem Statement

You are in a game with n rooms and m tunnels. Each tunnel has a score (can be positive or negative). Starting from room 1, find the maximum score you can collect when reaching room n.

**Input:**
- First line: n (rooms), m (tunnels)
- Next m lines: a, b, x (tunnel from a to b with score x)

**Output:**
- Maximum score from room 1 to room n
- Print -1 if you can get an arbitrarily large score (infinite)

**Constraints:**
- 1 <= n <= 2500
- 1 <= m <= 5000
- 1 <= a, b <= n
- -10^9 <= x <= 10^9

**Example:**
```
Input:
4 5
1 2 3
2 4 -1
1 3 -2
3 4 7
1 4 4

Output:
5

Explanation: Path 1 -> 3 -> 4 gives score -2 + 7 = 5
```

## Key Insight: Longest Path via Weight Negation

The standard Bellman-Ford finds shortest paths. To find longest paths:

**Method 1: Negate weights and find shortest path**
- Negate all edge weights
- Find shortest path (which is longest in original)
- Positive cycle becomes negative cycle after negation

**Method 2: Modify relaxation directly**
- Instead of: `dist[v] = min(dist[v], dist[u] + w)`
- Use: `dist[v] = max(dist[v], dist[u] + w)`
- Initialize dist[1] = 0, others = -infinity

We'll use Method 2 for clarity.

## Critical Concept: Cycle Must Be On Path

**This is the tricky part that many solutions miss!**

A positive cycle only gives infinite score if:
1. The cycle is reachable from room 1 (source)
2. Room n is reachable from the cycle (destination)

```
Example where cycle does NOT matter:

    1 -----> 4 (destination)
    |
    v
    2 <---> 3  (positive cycle between 2 and 3)

The cycle 2-3 exists, but room 4 is NOT reachable from it.
Answer: finite (not -1)
```

```
Example where cycle DOES matter:

    1 --> 2 <--> 3 --> 4
          ^      |
          |______|  (positive cycle)

Room 4 IS reachable from the cycle.
Answer: -1 (infinite)
```

## Algorithm

### Step 1: Modified Bellman-Ford (n-1 iterations)

```
dist[1] = 0
dist[2..n] = -infinity

For i = 1 to n-1:
    For each edge (u, v, w):
        If dist[u] != -infinity:
            dist[v] = max(dist[v], dist[u] + w)
```

### Step 2: Detect Positive Cycles on Valid Paths

Run n more iterations. Any node that can still be improved is part of a positive cycle or reachable from one.

```
For i = 1 to n:
    For each edge (u, v, w):
        If dist[u] != -infinity AND dist[u] + w > dist[v]:
            Mark v as "can_improve" (part of/reachable from positive cycle)
```

### Step 3: Check if Destination is Affected

If node n is marked as "can_improve", return -1. Otherwise, return dist[n].

## Visual Diagram

```
Problem: 4 rooms, 5 tunnels

    +3      -1
1 -----> 2 -----> 4

|                 ^
| -2              | +7
v                 |
3 ----------------+

Also: 1 --+4--> 4

Bellman-Ford for LONGEST path:

Initial:  dist = [0, -inf, -inf, -inf]  (1-indexed)

Iteration 1:
  Edge 1->2 (+3): dist[2] = max(-inf, 0+3) = 3
  Edge 1->3 (-2): dist[3] = max(-inf, 0-2) = -2
  Edge 1->4 (+4): dist[4] = max(-inf, 0+4) = 4
  Edge 2->4 (-1): dist[4] = max(4, 3-1) = 4
  Edge 3->4 (+7): dist[4] = max(4, -2+7) = 5

  After: dist = [0, 3, -2, 5]

Iteration 2:
  No improvements possible (no positive cycles)

  After: dist = [0, 3, -2, 5]

Final check (n more iterations):
  No nodes can be improved further

Answer: dist[4] = 5
```

## Dry Run: Example with Positive Cycle

```
Input:
4 4
1 2 1
2 3 5
3 2 5
2 4 1

Graph:
       +1      +1
    1 ----> 2 ----> 4
            |  ^
         +5 |  | +5
            v  |
            3--+

Positive cycle: 2 -> 3 -> 2 (total: +10 per loop)

Initial: dist = [0, -inf, -inf, -inf]

Iteration 1:
  1->2: dist[2] = 1
  2->3: dist[3] = 6
  3->2: dist[2] = max(1, 6+5) = 11
  2->4: dist[4] = 12

Iteration 2:
  2->3: dist[3] = max(6, 11+5) = 16
  3->2: dist[2] = max(11, 16+5) = 21
  2->4: dist[4] = max(12, 21+1) = 22

Iteration 3:
  Still improving! This continues forever...

Positive cycle detection (iterations n to 2n-1):
  Node 2, 3, 4 keep improving
  Node 4 is destination and is improving

Answer: -1 (infinite score possible)
```

## Implementation

### Python Solution

```python
from collections import deque

def high_score(n, m, edges):
 """
 Find maximum score from room 1 to room n.
 Returns -1 if infinite score is possible.
 """
 NEG_INF = float('-inf')

 # Initialize distances: room 1 = 0, others = -infinity
 dist = [NEG_INF] * (n + 1)
 dist[1] = 0

 # Build adjacency list for reachability check
 adj = [[] for _ in range(n + 1)]
 for a, b, x in edges:
  adj[a].append(b)

 # Step 1: Bellman-Ford for longest path (n-1 iterations)
 for _ in range(n - 1):
  for a, b, x in edges:
   if dist[a] != NEG_INF and dist[a] + x > dist[b]:
    dist[b] = dist[a] + x

 # Step 2: Detect nodes that can be improved (positive cycle reachable)
 # Run n more iterations to propagate "infinite" status
 can_improve = [False] * (n + 1)

 for _ in range(n):
  for a, b, x in edges:
   if dist[a] != NEG_INF and dist[a] + x > dist[b]:
    dist[b] = dist[a] + x
    can_improve[b] = True
   # Propagate: if source can improve, destination can too
   if can_improve[a]:
    can_improve[b] = True

 # Step 3: Check if destination n can be infinitely improved
 if can_improve[n]:
  return -1

 return dist[n]


def high_score_with_reachability(n, m, edges):
 """
 Alternative approach with explicit reachability checks.
 More intuitive but slightly more code.
 """
 NEG_INF = float('-inf')

 # Build forward and reverse adjacency lists
 adj = [[] for _ in range(n + 1)]
 radj = [[] for _ in range(n + 1)]
 for a, b, x in edges:
  adj[a].append((b, x))
  radj[b].append(a)

 # Check which nodes are reachable from node 1
 reachable_from_1 = [False] * (n + 1)
 queue = deque([1])
 reachable_from_1[1] = True
 while queue:
  u = queue.popleft()
  for v, _ in adj[u]:
   if not reachable_from_1[v]:
    reachable_from_1[v] = True
    queue.append(v)

 # Check which nodes can reach node n (BFS on reverse graph)
 can_reach_n = [False] * (n + 1)
 queue = deque([n])
 can_reach_n[n] = True
 while queue:
  u = queue.popleft()
  for v in radj[u]:
   if not can_reach_n[v]:
    can_reach_n[v] = True
    queue.append(v)

 # Bellman-Ford for longest path
 dist = [NEG_INF] * (n + 1)
 dist[1] = 0

 for _ in range(n - 1):
  for a, b, x in edges:
   if dist[a] != NEG_INF and dist[a] + x > dist[b]:
    dist[b] = dist[a] + x

 # Check for positive cycles on valid paths
 for _ in range(n):
  for a, b, x in edges:
   if dist[a] != NEG_INF and dist[a] + x > dist[b]:
    # Node b can be improved = part of positive cycle
    # Check if this cycle is on a path from 1 to n
    if reachable_from_1[a] and can_reach_n[b]:
     return -1
    dist[b] = dist[a] + x

 return dist[n]


# Read input and solve
if __name__ == "__main__":
 n, m = map(int, input().split())
 edges = []
 for _ in range(m):
  a, b, x = map(int, input().split())
  edges.append((a, b, x))

 print(high_score(n, m, edges))
```

### Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Bellman-Ford (n-1 iterations) | O(n * m) | O(n) |
| Positive cycle detection (n iterations) | O(n * m) | O(n) |
| Total | O(n * m) | O(n + m) |

- **Time**: O(n * m) where n = nodes, m = edges
- **Space**: O(n + m) for distances and edge list

## Common Mistakes

### Mistake 1: Not Checking if Cycle Affects Destination

```python
# WRONG: Detecting any positive cycle
for a, b, x in edges:
 if dist[a] + x > dist[b]:
  return -1  # Wrong! Cycle might not reach n

# CORRECT: Check if cycle is on path to n
for a, b, x in edges:
 if dist[a] + x > dist[b]:
  if reachable_from_1[a] and can_reach_n[b]:
   return -1
```

### Mistake 2: Using BFS/DFS for Longest Path

Longest path in general graphs is NP-hard. But with Bellman-Ford, we can detect when it's infinite (positive cycle) and compute the finite answer otherwise.

### Mistake 3: Integer Overflow

With weights up to 10^9 and paths up to 2500 edges:
- Maximum score: 2500 * 10^9 = 2.5 * 10^12
- Use `long long` in C++ or Python's arbitrary precision

### Mistake 4: Wrong Initialization

```python
# WRONG: Initialize all to 0
dist = [0] * (n + 1)

# CORRECT: Initialize to -infinity, except source
dist = [NEG_INF] * (n + 1)
dist[1] = 0
```

## Why 2n-1 Total Iterations?

- **First n-1 iterations**: Find longest paths assuming no positive cycles
- **Next n iterations**: Propagate the "can be improved" status
  - If a node is on a positive cycle, it needs up to n iterations to propagate to all reachable nodes
  - This ensures we correctly identify ALL nodes that can reach node n from a positive cycle

## Related Problems

| Problem | Key Difference |
|---------|----------------|
| [Cycle Finding (CSES)](https://cses.fi/problemset/task/1669) | Find any negative cycle, not on specific path |
| [Shortest Routes I](https://cses.fi/problemset/task/1671) | Shortest path, no negative weights |
| [Shortest Routes II](https://cses.fi/problemset/task/1672) | All-pairs shortest path |

## Summary

1. **Problem**: Longest path from 1 to n with possible infinite score
2. **Key Insight**: Convert to shortest path by negating, or modify Bellman-Ford to maximize
3. **Critical Check**: Positive cycle must be reachable from 1 AND must be able to reach n
4. **Algorithm**: Bellman-Ford (n-1 iter) + positive cycle propagation (n iter)
5. **Answer**: -1 if node n is on/reachable from a positive cycle, else dist[n]
