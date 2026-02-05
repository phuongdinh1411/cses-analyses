---
difficulty: Easy
tags: [graph, bfs, dfs, flood-fill, grid]
cses_link: https://cses.fi/problemset/task/1192
---

# Counting Rooms

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem | Count connected floor regions in a grid |
| Input | n x m grid with '#' (walls) and '.' (floors) |
| Output | Number of separate rooms (connected components) |
| Constraints | 1 <= n, m <= 1000 |
| Key Technique | Flood-fill / BFS / DFS |
| Time Complexity | O(n * m) |

## Learning Goals

After solving this problem, you will understand:

1. **Grid as Graph**: How to treat a 2D grid as an implicit graph
2. **Flood-Fill Algorithm**: The classic technique for "painting" connected regions
3. **Connected Components**: Counting separate regions in a graph
4. **BFS vs DFS on Grids**: When and how to use each traversal method

This is the **first graph problem** every student should master!

## Problem Statement

You are given a map of a building with n rows and m columns. Each cell is either:
- `#` - a wall
- `.` - a floor tile

Two floor tiles belong to the same room if you can walk from one to the other moving only up, down, left, or right (4-directional connectivity). Count the total number of rooms.

**Example Input:**
```
5 8
########
#..#...#
####.#.#
#..#...#
########
```

**Example Output:**
```
3
```

## Intuition

Think of pouring paint on each unvisited floor tile:

1. Start at any unvisited `.` cell
2. The paint "floods" to all connected floor cells
3. Once flooding stops, you've found one complete room
4. Repeat until all floor cells are painted
5. Count how many times you poured paint = number of rooms

Each flood-fill operation marks an entire connected component!

## Algorithm

```
room_count = 0
for each cell (i, j) in grid:
    if cell is '.' AND not visited:
        room_count += 1
        flood_fill(i, j)  // Mark all connected cells as visited

return room_count
```

The key insight: **Every time we start a new flood-fill, we've discovered a new room.**

## Visual Diagram: Flood-Fill Process

```
Initial:     Room 1:      Room 2:      Room 3 (Final):
########     ########     ########     ########
#..#...#     #11#...#     #11#222#     #11#222#
####.#.#     ####.#.#     ####2#2#     ####2#2#
#..#...#     #..#...#     #..#222#     #33#222#
########     ########     ########     ########
                                       Result: 3 rooms
```

## Dry Run Example

**Grid (3x4):**
```
.##.
....
.##.
```

| Step | Action | Room Count |
|------|--------|------------|
| 1 | Visit (0,0), start BFS | 1 |
| 2 | BFS floods to: (1,0), (1,1), (1,2), (1,3), (0,3), (2,0), (2,3) | 1 |
| 3-10 | All remaining cells: either '#' or already visited | 1 |

**Result: 1 room** (all floor tiles connect around the walls)

## Implementation: BFS Approach

BFS uses a queue to explore level-by-level. Good for finding shortest paths and when recursion depth is a concern.

### Python (BFS)

```python
from collections import deque

def count_rooms_bfs(n, m, grid):
  visited = [[False] * m for _ in range(n)]
  directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

  def bfs(start_row, start_col):
    queue = deque([(start_row, start_col)])
    visited[start_row][start_col] = True

    while queue:
      row, col = queue.popleft()
      for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < n and 0 <= new_col < m and
          not visited[new_row][new_col] and
          grid[new_row][new_col] == '.'):
          visited[new_row][new_col] = True
          queue.append((new_row, new_col))

  room_count = 0
  for i in range(n):
    for j in range(m):
      if grid[i][j] == '.' and not visited[i][j]:
        bfs(i, j)
        room_count += 1

  return room_count

# Read input
n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]
print(count_rooms_bfs(n, m, grid))
```

## Implementation: DFS Approach

DFS explores as deep as possible before backtracking. Simpler to implement but watch for stack overflow on large grids.

### Python (DFS - Iterative)

```python
def count_rooms_dfs(n, m, grid):
  visited = [[False] * m for _ in range(n)]
  directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

  def dfs(start_row, start_col):
    stack = [(start_row, start_col)]
    visited[start_row][start_col] = True

    while stack:
      row, col = stack.pop()
      for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < n and 0 <= new_col < m and
          not visited[new_row][new_col] and
          grid[new_row][new_col] == '.'):
          visited[new_row][new_col] = True
          stack.append((new_row, new_col))

  room_count = 0
  for i in range(n):
    for j in range(m):
      if grid[i][j] == '.' and not visited[i][j]:
        dfs(i, j)
        room_count += 1

  return room_count

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]
print(count_rooms_dfs(n, m, grid))
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not marking visited when adding to queue | Mark visited BEFORE adding, not when processing |
| Wrong boundary check order | Check bounds BEFORE accessing grid[row][col] |
| Using recursive DFS on large grids | Use iterative DFS/BFS to avoid stack overflow |
| Checking only 2 directions | Use all 4 directions: up, down, left, right |
| Off-by-one in bounds | Use `0 <= x < n` not `0 <= x <= n` |

**Critical Bug:**
```python
# WRONG                              # CORRECT
queue.append((r, c))                 visited[r][c] = True
visited[r][c] = True                 queue.append((r, c))
```

## Complexity Analysis

| Metric | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n * m) | Each cell visited exactly once |
| Space | O(n * m) | Visited array + queue/stack (worst case: all cells are floor) |

## Related Problems

| Problem | Platform | Key Difference |
|---------|----------|----------------|
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | LeetCode | Same problem, different input format |
| [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | LeetCode | Find largest room size |
| [Flood Fill](https://leetcode.com/problems/flood-fill/) | LeetCode | Fill with specific color |
| [Building Roads](https://cses.fi/problemset/task/1666) | CSES | Connect components with minimum edges |
| [Labyrinth](https://cses.fi/problemset/task/1193) | CSES | Find path between two points |
