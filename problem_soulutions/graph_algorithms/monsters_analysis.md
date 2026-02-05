---
layout: simple
title: "Monsters - Multi-Source BFS Grid Escape"
permalink: /problem_soulutions/graph_algorithms/monsters_analysis
difficulty: Medium
tags: [graph, bfs, multi-source-bfs, grid]
cses_link: https://cses.fi/problemset/task/1194
---

# Monsters - Multi-Source BFS Grid Escape

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Escape from grid while avoiding monsters |
| Technique | Multi-source BFS + Standard BFS |
| Time Complexity | O(n * m) |
| Space Complexity | O(n * m) |
| Key Insight | Compute monster arrival times first, then find safe path for player |

## Learning Goals

After solving this problem, you will understand:
- **Multi-source BFS**: Starting BFS from multiple sources simultaneously
- **Arrival time computation**: Computing who arrives first at each cell
- **Two-phase BFS**: Using one BFS result to constrain another BFS
- **Path reconstruction**: Building the escape route from parent pointers

## Problem Statement

You are given an n x m grid containing:
- `A` - Your starting position (exactly one)
- `M` - Monster positions (zero or more)
- `#` - Walls (impassable)
- `.` - Empty cells

**Goal**: Escape to any boundary cell before any monster can catch you.

**Rules**:
- You and all monsters move simultaneously, one cell per turn
- Monsters move optimally to catch you
- You escape if you reach a boundary cell AND no monster reaches that cell at the same time or earlier
- Output the escape path if possible, otherwise "NO"

**Constraints**: 1 <= n, m <= 1000

## Key Insight: Who Arrives First?

The critical insight is to think about **arrival times**:

```
For each cell, we need to know:
1. When can the NEAREST monster reach this cell?
2. When can the player reach this cell?

Player can safely visit a cell only if:
    player_arrival_time < monster_arrival_time
```

This transforms a complex chase problem into a simple comparison problem.

## Algorithm: Two-Phase BFS

### Phase 1: Multi-Source BFS from All Monsters

Start BFS with ALL monsters in the queue at time 0. This computes the minimum time for ANY monster to reach each cell.

```
Why multi-source BFS?
- Single-source BFS from each monster: O(k * n * m) where k = number of monsters
- Multi-source BFS: O(n * m) regardless of monster count

All monsters start at time 0, BFS naturally finds the minimum arrival time.
```

### Phase 2: Player BFS with Constraints

Run BFS from player position. Only visit cells where:
```
player_time < monster_time[cell]
```

If player reaches any boundary cell satisfying this condition, escape is possible.

## Visual Diagram

```
Initial Grid:              Monster Times (Phase 1):      Player BFS (Phase 2):
+---+---+---+---+---+      +---+---+---+---+---+         +---+---+---+---+---+

| # | # | # | # | # |      | # | # | # | # | # |         | # | # | # | # | # |
+---+---+---+---+---+      +---+---+---+---+---+         +---+---+---+---+---+

| # | A | . | . | # |      | # | 4 | 3 | 2 | # |         | # | 0 | 1 | X | # |
+---+---+---+---+---+      +---+---+---+---+---+         +---+---+---+---+---+

| # | . | # | M | # |      | # | 3 | # | 0 | # |         | # | 1 | # | X | # |
+---+---+---+---+---+      +---+---+---+---+---+         +---+---+---+---+---+

| # | . | . | . | . |      | # | 2 | 1 | 1 | 2 |         | # | 2 | 3 |ESC| X |
+---+---+---+---+---+      +---+---+---+---+---+         +---+---+---+---+---+

Monster at (2,3) spreads:   Player at (1,1):
- Time 0: (2,3)             - Can visit (1,2) at t=1 (monster arrives t=3)
- Time 1: (2,2)blocked,     - Can visit (2,1) at t=1 (monster arrives t=3)
          (3,3), (3,2)      - Cannot visit (1,3) at t=2 (monster arrives t=2)
- Time 2: (3,1), (3,4)...   - Escape at (3,4) at t=4 (boundary, monster arrives later)
```

## Dry Run Example

```
Grid (5x8):
########
#M....A#
#.#..#.#
#......#
########

Step 1: Find positions
- Player A at (1, 6)
- Monster M at (1, 1)

Step 2: Multi-source BFS from monsters
monster_time:
  # # # # # # # #
  # 0 1 2 3 4 5 #    <- Monster spreads right
  # 1 # 3 4 # 6 #
  # 2 3 4 5 6 7 #
  # # # # # # # #

Step 3: Player BFS
- Start: (1,6) at time 0
- Try (1,5): player_time=1 < monster_time=4  -> Valid, visit
- Try (1,4): player_time=2 < monster_time=3  -> Valid, visit
- Try (2,4): player_time=3 < monster_time=4  -> Valid, visit
- Try (3,4): player_time=4 < monster_time=5  -> Valid, visit
- Try (3,5): player_time=5 < monster_time=6  -> Valid, visit
- Try (3,6): player_time=6 < monster_time=7  -> Valid, visit
- Try (3,7): BOUNDARY! player_time=7 < monster_time=8 -> ESCAPE!

Path reconstruction: LLLDDRR
Result: YES, LLLDDRR
```

## Python Solution

```python
from collections import deque
import sys
input = sys.stdin.readline

def solve():
  n, m = map(int, input().split())
  grid = [input().strip() for _ in range(n)]

  # Directions: U, D, L, R
  dirs = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]

  # Find player and monsters
  player = None
  monsters = []
  for i in range(n):
    for j in range(m):
      if grid[i][j] == 'A':
        player = (i, j)
      elif grid[i][j] == 'M':
        monsters.append((i, j))

  # Phase 1: Multi-source BFS from all monsters
  INF = float('inf')
  monster_time = [[INF] * m for _ in range(n)]
  queue = deque()

  # Add ALL monsters to queue at time 0
  for r, c in monsters:
    monster_time[r][c] = 0
    queue.append((r, c))

  while queue:
    r, c = queue.popleft()
    for dr, dc, _ in dirs:
      nr, nc = r + dr, c + dc
      if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':
        if monster_time[nr][nc] == INF:
          monster_time[nr][nc] = monster_time[r][c] + 1
          queue.append((nr, nc))

  # Phase 2: Player BFS
  player_time = [[INF] * m for _ in range(n)]
  parent = [[None] * m for _ in range(n)]
  pr, pc = player
  player_time[pr][pc] = 0
  queue = deque([(pr, pc)])

  def is_boundary(r, c):
    return r == 0 or r == n - 1 or c == 0 or c == m - 1

  # Check if player starts on boundary
  if is_boundary(pr, pc):
    print("YES")
    print(0)
    return

  while queue:
    r, c = queue.popleft()
    for dr, dc, direction in dirs:
      nr, nc = r + dr, c + dc
      if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':
        new_time = player_time[r][c] + 1
        # Key condition: player must arrive BEFORE monsters
        if player_time[nr][nc] == INF and new_time < monster_time[nr][nc]:
          player_time[nr][nc] = new_time
          parent[nr][nc] = (r, c, direction)

          # Check if reached boundary
          if is_boundary(nr, nc):
            # Reconstruct path
            path = []
            curr = (nr, nc)
            while parent[curr[0]][curr[1]] is not None:
              pr, pc, d = parent[curr[0]][curr[1]]
              path.append(d)
              curr = (pr, pc)
            path.reverse()
            print("YES")
            print(len(path))
            print(''.join(path))
            return

          queue.append((nr, nc))

  print("NO")

solve()
```

## Complexity Analysis

| Phase | Time | Space | Description |
|-------|------|-------|-------------|
| Multi-source BFS | O(n * m) | O(n * m) | Each cell visited once |
| Player BFS | O(n * m) | O(n * m) | Each cell visited once |
| Path reconstruction | O(path length) | O(1) | Backtrack through parents |
| **Total** | **O(n * m)** | **O(n * m)** | Linear in grid size |

## Common Mistakes

### 1. Not Using Multi-Source BFS

```python
# WRONG: BFS from each monster separately
for monster in monsters:
  bfs_from_single_source(monster)  # O(k * n * m) - too slow!

# CORRECT: Multi-source BFS
for monster in monsters:
  queue.append(monster)
  monster_time[monster] = 0
bfs()  # O(n * m) - all monsters at once
```

### 2. Wrong Time Comparison

```python
# WRONG: Using <= allows monster to catch player
if new_time <= monster_time[nr][nc]:  # Bug! Same time = caught

# CORRECT: Strict less than
if new_time < monster_time[nr][nc]:  # Player must arrive BEFORE
```

### 3. Forgetting Edge Case: Player Starts on Boundary

```python
# Don't forget to check if player is already on boundary
if is_boundary(player_row, player_col):
  print("YES")
  print(0)  # Empty path
  return
```

### 4. Not Handling Multiple Monsters Correctly

```python
# WRONG: Only considering closest monster
min_dist = min(distance_to_each_monster)

# CORRECT: Use multi-source BFS - automatically handles all monsters
```

## Related Problems

| Problem | Platform | Key Similarity |
|---------|----------|----------------|
| [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | LeetCode | Multi-source BFS spreading |
| [01 Matrix](https://leetcode.com/problems/01-matrix/) | LeetCode | Multi-source distance calculation |
| [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | LeetCode | Grid BFS pathfinding |
| [Labyrinth](https://cses.fi/problemset/task/1193) | CSES | Grid escape without monsters |

## Summary

The Monsters problem elegantly demonstrates why multi-source BFS is powerful:

1. **Transform the problem**: From "avoid all monsters" to "arrive before any monster"
2. **Compute arrival times**: Multi-source BFS gives minimum monster arrival time per cell
3. **Constrained pathfinding**: Player BFS only visits "safe" cells
4. **Path reconstruction**: Standard backtracking through parent pointers

This two-phase approach separates concerns cleanly and runs in optimal O(n * m) time.
