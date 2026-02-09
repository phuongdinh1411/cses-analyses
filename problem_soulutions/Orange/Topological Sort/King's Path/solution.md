# King's Path

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

## Problem Statement

A black king is on a chess field with 10^9 rows and 10^9 columns. Some cells are allowed, given as n segments. Each segment describes cells in columns from aᵢ to bᵢ in row rᵢ.

Find the minimum number of moves for the king to get from (x₀, y₀) to (x₁, y₁), moving only along allowed cells. A king can move to any of the 8 neighboring cells in one move.

## Input Format
- First line: x₀, y₀, x₁, y₁ (initial and final positions)
- Second line: n (number of segments, 1 ≤ n ≤ 10^5)
- Next n lines: rᵢ, aᵢ, bᵢ (row and column range)
- Total length of all segments ≤ 10^5

## Output Format
Print minimum moves, or -1 if no path exists.

## Example
```
Input:
1 1 3 3
2
1 1 3
2 1 3

Output:
4
```
The king starts at (1,1) and needs to reach (3,3). Allowed cells are row 1 columns 1-3 and row 2 columns 1-3. The minimum path takes 4 moves: (1,1) -> (1,2) -> (2,2) -> (2,3) -> (3,3).

## Solution

### Approach
Since total allowed cells ≤ 10^5, use BFS on the sparse graph. Store allowed cells in a set and use coordinate compression or direct hashing.

### Python Solution

```python
from collections import deque

def solve():
  x0, y0, x1, y1 = map(int, input().split())
  n = int(input())

  allowed = set()
  allowed.add((x0, y0))
  allowed.add((x1, y1))

  for _ in range(n):
    r, a, b = map(int, input().split())
    for c in range(a, b + 1):
      allowed.add((r, c))

  # BFS
  dx = [0, 0, 1, -1, 1, -1, 1, -1]
  dy = [1, -1, 0, 0, 1, -1, -1, 1]

  dist = {(x0, y0): 0}
  queue = deque([(x0, y0)])

  while queue:
    x, y = queue.popleft()

    if (x, y) == (x1, y1):
      print(dist[(x, y)])
      return

    for i in range(8):
      nx, ny = x + dx[i], y + dy[i]

      if (nx, ny) in allowed and (nx, ny) not in dist:
        dist[(nx, ny)] = dist[(x, y)] + 1
        queue.append((nx, ny))

  print(-1)

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Set Operations

```python
from collections import deque

def solve():
  x0, y0, x1, y1 = map(int, input().split())
  n = int(input())

  allowed = set()

  for _ in range(n):
    r, a, b = map(int, input().split())
    for c in range(a, b + 1):
      allowed.add((r, c))

  # King moves: 8 directions
  directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

  if (x0, y0) not in allowed or (x1, y1) not in allowed:
    print(-1)
    return

  visited = set()
  queue = deque([(x0, y0, 0)])
  visited.add((x0, y0))

  while queue:
    x, y, d = queue.popleft()

    if x == x1 and y == y1:
      print(d)
      return

    for dx, dy in directions:
      nx, ny = x + dx, y + dy
      if (nx, ny) in allowed and (nx, ny) not in visited:
        visited.add((nx, ny))
        queue.append((nx, ny, d + 1))

  print(-1)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(S) where S is total number of allowed cells (≤ 10^5)
- **Space Complexity:** O(S) for storing allowed cells and BFS queue

### Key Insight
Despite the huge grid (10^9 × 10^9), only up to 10^5 cells are allowed. We can store these in a set and run standard BFS. The key is using coordinate hashing or tuples to efficiently check if a cell is allowed.
