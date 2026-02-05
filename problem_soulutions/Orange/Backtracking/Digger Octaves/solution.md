# Digger Octaves

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

## Problem Statement

After many years spent playing Digger, little Ivan realized he was not taking advantage of the octaves. Digger is a Canadian computer game, originally designed for the IBM personal computer, back in 1983. The aim of the game is to collect precious gold and emeralds buried deep in subterranean levels of an old abandoned mine.

We Digger gurus call a set of eight consecutive emeralds an octave. Notice that, by consecutive we mean that we can collect them one after another. Your Digger Mobile is able to move in the four directions: North, South, West and East.

In a simplified Digger version, consisting only of emeralds and empty spaces, you will have to count how many octaves are present for a given map.

## Input Format
- Input starts with an integer T, representing the number of test cases (1 ≤ T ≤ 20).
- Each test case consists of a map:
  - An integer N (1 ≤ N ≤ 8), representing the side length of the square-shaped map.
  - N lines follow, N characters each.
  - 'X' represents an emerald, '.' represents an empty space.

## Output Format
For each test case print the number of octaves on a single line.

## Solution

### Approach
Use DFS/backtracking to find all paths of exactly 8 consecutive emeralds. To avoid counting the same set of emeralds multiple times (via different orderings), we use a set to store unique combinations of 8 cells.

### Python Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  n = int(input())
  grid = []
  for i in range(n):
   grid.append(input().strip())

  # Directions: up, down, left, right
  dx = [-1, 1, 0, 0]
  dy = [0, 0, -1, 1]

  # Set to store unique octaves (as frozensets of positions)
  octaves = set()

  def dfs(x, y, path, visited):
   if len(path) == 8:
    # Store as frozenset to make it hashable and order-independent
    octaves.add(frozenset(path))
    return

   for i in range(4):
    nx, ny = x + dx[i], y + dy[i]
    if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited and grid[nx][ny] == 'X':
     visited.add((nx, ny))
     path.append((nx, ny))
     dfs(nx, ny, path, visited)
     path.pop()
     visited.remove((nx, ny))

  # Start DFS from each emerald
  for i in range(n):
   for j in range(n):
    if grid[i][j] == 'X':
     visited = {(i, j)}
     path = [(i, j)]
     dfs(i, j, path, visited)

  print(len(octaves))

if __name__ == "__main__":
 solve()
```

### Alternative Solution with Bitmask

```python
def solve():
 t = int(input())

 for _ in range(t):
  n = int(input())
  grid = []
  for i in range(n):
   grid.append(input().strip())

  dx = [-1, 1, 0, 0]
  dy = [0, 0, -1, 1]

  octaves = set()

  def dfs(x, y, bitmask, count):
   if count == 8:
    octaves.add(bitmask)
    return

   for i in range(4):
    nx, ny = x + dx[i], y + dy[i]
    bit = nx * n + ny
    if 0 <= nx < n and 0 <= ny < n and not (bitmask & (1 << bit)) and grid[nx][ny] == 'X':
     dfs(nx, ny, bitmask | (1 << bit), count + 1)

  for i in range(n):
   for j in range(n):
    if grid[i][j] == 'X':
     bit = i * n + j
     dfs(i, j, 1 << bit, 1)

  print(len(octaves))

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(4^8 × n²) in worst case, but much less due to pruning
- **Space Complexity:** O(n² + number of unique octaves)
