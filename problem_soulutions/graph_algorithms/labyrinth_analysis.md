---
layout: simple
title: "Labyrinth"
permalink: /problem_soulutions/graph_algorithms/labyrinth_analysis
difficulty: Easy
tags: [graph, bfs, shortest-path, grid, path-reconstruction]
cses_link: https://cses.fi/problemset/task/1193
---

# Labyrinth

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Find shortest path from A to B in a grid |
| Input | n x m grid with walls '#', floor '.', start 'A', end 'B' |
| Output | Path length and direction string, or "NO" if impossible |
| Constraints | 1 <= n, m <= 1000 |
| Core Technique | BFS with path reconstruction |
| Time Complexity | O(n * m) |
| Space Complexity | O(n * m) |

## Learning Goals

After solving this problem, you will understand:
1. **BFS for shortest path**: Why BFS guarantees the shortest path in unweighted graphs
2. **Path reconstruction**: Using parent pointers to rebuild the path from destination to source
3. **Direction encoding**: Storing movement directions for path output

## Problem Statement

You are given a map of a labyrinth. Your task is to find a path from start to end.

- `#` = wall (cannot pass)
- `.` = floor (can pass)
- `A` = start position
- `B` = end position

Output "YES" followed by path length and directions (L/R/U/D), or "NO" if no path exists.

**Example Input:**
```
5 8
########
#.A#...#
#.##.#B#
#......#
########
```

**Example Output:**
```
YES
9
LDDRRRRRU
```

## Key Insight

BFS explores nodes level by level. The first time we reach any cell, we've found the shortest path to it. This is because all edges have equal weight (1 step).

```
Why BFS works for shortest path:
- Level 0: Start cell (distance 0)
- Level 1: All cells 1 step away
- Level 2: All cells 2 steps away
- ...
- First time reaching B = shortest path to B
```

## Algorithm

1. **Find start and end positions** by scanning the grid
2. **Run BFS from start**:
   - Use a queue for BFS traversal
   - Track visited cells to avoid revisiting
   - Store parent pointer and direction for each cell
3. **When reaching end**: Reconstruct path by backtracking through parents
4. **Reverse the path** (we built it backwards from B to A)

## Path Reconstruction

We store for each cell: (parent_cell, direction_to_reach_this_cell)

```
Backtracking from B to A:
B <- parent of B <- parent of that <- ... <- A

Directions collected: [U, R, R, R, R, D, D, L]  (reversed order)
Final path: LDDRRRRRU (after reversing)
```

## Direction Encoding

When moving from cell (r, c) to neighbor (nr, nc):
- Move UP (r-1, c): store 'U' at neighbor
- Move DOWN (r+1, c): store 'D' at neighbor
- Move LEFT (r, c-1): store 'L' at neighbor
- Move RIGHT (r, c+1): store 'R' at neighbor

The direction stored represents "how we arrived at this cell".

## Visual Diagram

```
Initial Grid:              BFS Exploration (distances):
########                   ########
#.A#...#                   #2A#...#
#.##.#B#                   #3##6#B#  <- B found at distance 9
#......#                   #456789#
########                   ########

Parent Pointers (showing direction to reach each cell):
########
#LA#...#      L = came from right (moved left to get here)
#D##.#U#      D = came from above (moved down to get here)
#DRRRRU#      etc.
########

Path Reconstruction:
B(2,6) <- U <- (3,6) <- R <- (3,5) <- R <- (3,4) <- R <- (3,3) <- R <- (3,2)
       <- D <- (2,2) <- D <- (1,2) <- L <- A(1,2)

Reversed: L, D, D, R, R, R, R, U -> "LDDRRRRRU"
```

## Dry Run Example

```
Grid (0-indexed):
Row 0: ########
Row 1: #.A#...#    A at (1,2)
Row 2: #.##.#B#    B at (2,6)
Row 3: #......#
Row 4: ########

BFS Steps:
Step 0: Queue = [(1,2)], visited = {(1,2)}
Step 1: Process (1,2), add (1,1) with 'L'
        Queue = [(1,1)], visited = {(1,2), (1,1)}
Step 2: Process (1,1), add (2,1) with 'D'
        Queue = [(2,1)]
Step 3: Process (2,1), add (3,1) with 'D'
        Queue = [(3,1)]
Step 4: Process (3,1), add (3,2) with 'R'
        Queue = [(3,2)]
... continue until B is reached ...

When (2,6) is dequeued: FOUND! Backtrack to get path.
```

## Python Solution

```python
from collections import deque

def solve():
 n, m = map(int, input().split())
 grid = [input().strip() for _ in range(n)]

 # Find start and end
 start = end = None
 for i in range(n):
  for j in range(m):
   if grid[i][j] == 'A':
    start = (i, j)
   elif grid[i][j] == 'B':
    end = (i, j)

 # Direction vectors: (dr, dc, char)
 directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]

 # BFS
 queue = deque([start])
 parent = {start: None}  # Maps cell -> (parent_cell, direction)

 while queue:
  r, c = queue.popleft()

  if (r, c) == end:
   # Reconstruct path
   path = []
   curr = end
   while parent[curr] is not None:
    prev, direction = parent[curr]
    path.append(direction)
    curr = prev
   path.reverse()

   print("YES")
   print(len(path))
   print(''.join(path))
   return

  for dr, dc, direction in directions:
   nr, nc = r + dr, c + dc
   if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#' and (nr, nc) not in parent:
    parent[(nr, nc)] = ((r, c), direction)
    queue.append((nr, nc))

 print("NO")

solve()
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting to reverse path | Path is backwards (B to A) | Always reverse after backtracking |
| Wrong direction encoding | Store direction of parent instead of current move | Store direction when adding to queue |
| Not marking start as visited | Start might be re-added to queue | Initialize visited with start cell |
| Checking visited after dequeue | Same cell added multiple times | Check visited when adding to queue |
| Using DFS instead of BFS | DFS doesn't guarantee shortest path | Use queue (BFS), not stack (DFS) |

## Direction Encoding Pitfall

```
WRONG: Store direction at parent cell
  When at (1,2) moving to (2,2), storing 'D' at (1,2)
  This loses information about how we reached (2,2)

CORRECT: Store direction at destination cell
  When at (1,2) moving to (2,2), storing 'D' at (2,2)
  This tells us: "we moved DOWN to reach (2,2)"
```

## Complexity Analysis

- **Time**: O(n * m) - each cell visited at most once
- **Space**: O(n * m) - for parent array and queue

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | LeetCode | 8 directions instead of 4 |
| [Message Route](https://cses.fi/problemset/task/1667) | CSES | Graph instead of grid |
| [Counting Rooms](https://cses.fi/problemset/task/1192) | CSES | Count components, no path needed |
| [Maze (shortest path)](https://leetcode.com/problems/the-maze-ii/) | LeetCode | Ball rolls until hitting wall |
