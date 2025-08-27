# CSES Counting Rooms - Problem Analysis

## Problem Statement
You are given a map of a building, and your task is to count the number of its rooms. The size of the map is n×m squares, and each square is either floor or wall. You can walk left, right, up, and down through the floor squares.

### Input
The first input line has two integers n and m: the height and width of the map.
Then there are n lines that describe the map. Each line has m characters: "." denotes a floor and "#" denotes a wall.

### Output
Print one integer: the number of rooms.

### Constraints
- 1 ≤ n,m ≤ 1000

### Example
```
Input:
5 8
########
#..#...#
####.#.#
#..#...#
########

Output:
3
```

## Solution Progression

### Approach 1: Recursive DFS - O(n*m)
**Description**: Use depth-first search to explore each room and mark visited cells.

```python
def counting_rooms_dfs(n, m, grid):
    def dfs(row, col):
        if (row < 0 or row >= n or col < 0 or col >= m or 
            grid[row][col] == '#' or visited[row][col]):
            return
        
        visited[row][col] = True
        
        # Explore all four directions
        dfs(row + 1, col)  # Down
        dfs(row - 1, col)  # Up
        dfs(row, col + 1)  # Right
        dfs(row, col - 1)  # Left
    
    visited = [[False] * m for _ in range(n)]
    rooms = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                dfs(i, j)
                rooms += 1
    
    return rooms
```

**Why this is efficient**: We visit each cell at most once, and each cell is processed in O(1) time. The total complexity is O(n*m).

### Improvement 1: Iterative DFS with Stack - O(n*m)
**Description**: Use iterative DFS with a stack to avoid recursion stack overflow.

```python
def counting_rooms_iterative_dfs(n, m, grid):
    def dfs_iterative(start_row, start_col):
        stack = [(start_row, start_col)]
        
        while stack:
            row, col = stack.pop()
            
            if (row < 0 or row >= n or col < 0 or col >= m or 
                grid[row][col] == '#' or visited[row][col]):
                continue
            
            visited[row][col] = True
            
            # Add all four directions to stack
            stack.append((row + 1, col))  # Down
            stack.append((row - 1, col))  # Up
            stack.append((row, col + 1))  # Right
            stack.append((row, col - 1))  # Left
    
    visited = [[False] * m for _ in range(n)]
    rooms = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                dfs_iterative(i, j)
                rooms += 1
    
    return rooms
```

**Why this improvement works**: Iterative DFS avoids potential stack overflow for very large grids and can be more efficient in some cases.

### Improvement 2: BFS with Queue - O(n*m)
**Description**: Use breadth-first search with a queue for level-by-level exploration.

```python
from collections import deque

def counting_rooms_bfs(n, m, grid):
    def bfs(start_row, start_col):
        queue = deque([(start_row, start_col)])
        
        while queue:
            row, col = queue.popleft()
            
            if (row < 0 or row >= n or col < 0 or col >= m or 
                grid[row][col] == '#' or visited[row][col]):
                continue
            
            visited[row][col] = True
            
            # Add all four directions to queue
            queue.append((row + 1, col))  # Down
            queue.append((row - 1, col))  # Up
            queue.append((row, col + 1))  # Right
            queue.append((row, col - 1))  # Left
    
    visited = [[False] * m for _ in range(n)]
    rooms = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                bfs(i, j)
                rooms += 1
    
    return rooms
```

**Why this improvement works**: BFS explores the room level by level, which can be more memory-efficient for very large rooms.

### Alternative: Union-Find (Disjoint Set) - O(n*m * α(n*m))
**Description**: Use union-find data structure to connect adjacent floor cells.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

def counting_rooms_union_find(n, m, grid):
    uf = UnionFind(n * m)
    
    # Connect adjacent floor cells
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                continue
            
            current = i * m + j
            
            # Check all four directions
            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ni, nj = i + di, j + dj
                if (0 <= ni < n and 0 <= nj < m and 
                    grid[ni][nj] == '.'):
                    neighbor = ni * m + nj
                    uf.union(current, neighbor)
    
    # Count unique components
    components = set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.':
                components.add(uf.find(i * m + j))
    
    return len(components)
```

**Why this works**: Union-find connects all adjacent floor cells into components, and the number of unique components gives us the number of rooms.

## Final Optimal Solution

```python
n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

def dfs(row, col):
    if (row < 0 or row >= n or col < 0 or col >= m or 
        grid[row][col] == '#' or visited[row][col]):
        return
    
    visited[row][col] = True
    
    # Explore all four directions
    dfs(row + 1, col)  # Down
    dfs(row - 1, col)  # Up
    dfs(row, col + 1)  # Right
    dfs(row, col - 1)  # Left

visited = [[False] * m for _ in range(n)]
rooms = 0

for i in range(n):
    for j in range(m):
        if grid[i][j] == '.' and not visited[i][j]:
            dfs(i, j)
            rooms += 1

print(rooms)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive DFS | O(n*m) | O(n*m) | Visit each cell once |
| Iterative DFS | O(n*m) | O(n*m) | Avoid stack overflow |
| BFS | O(n*m) | O(n*m) | Level-by-level exploration |
| Union-Find | O(n*m * α(n*m)) | O(n*m) | Connect components |

## Key Insights for Other Problems

### 1. **Connected Components in Grids**
**Principle**: Use graph traversal algorithms to find connected components in grid-based problems.
**Applicable to**:
- Grid problems
- Connected components
- Flood fill
- Graph traversal

**Example Problems**:
- Counting rooms
- Number of islands
- Flood fill
- Connected components

### 2. **DFS vs BFS for Graph Traversal**
**Principle**: Choose between DFS and BFS based on problem requirements and constraints.
**Applicable to**:
- Graph traversal
- Connected components
- Path finding
- Algorithm design

**Example Problems**:
- Graph traversal
- Connected components
- Path finding
- Algorithm design

### 3. **Grid Representation**
**Principle**: Represent grids as graphs where adjacent cells are connected nodes.
**Applicable to**:
- Grid problems
- Graph algorithms
- Spatial problems
- Algorithm design

**Example Problems**:
- Grid problems
- Graph algorithms
- Spatial problems
- Algorithm design

### 4. **Union-Find for Connectivity**
**Principle**: Use union-find data structure to efficiently handle connectivity queries.
**Applicable to**:
- Connectivity problems
- Component counting
- Dynamic connectivity
- Algorithm design

**Example Problems**:
- Connectivity problems
- Component counting
- Dynamic connectivity
- Algorithm design

## Notable Techniques

### 1. **DFS Pattern**
```python
def dfs(row, col):
    if not valid_cell(row, col) or visited[row][col]:
        return
    visited[row][col] = True
    for dr, dc in directions:
        dfs(row + dr, col + dc)
```

### 2. **BFS Pattern**
```python
from collections import deque
def bfs(start_row, start_col):
    queue = deque([(start_row, start_col)])
    while queue:
        row, col = queue.popleft()
        if not valid_cell(row, col) or visited[row][col]:
            continue
        visited[row][col] = True
        for dr, dc in directions:
            queue.append((row + dr, col + dc))
```

### 3. **Grid Traversal Pattern**
```python
# Define directions
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for i in range(n):
    for j in range(m):
        if grid[i][j] == '.' and not visited[i][j]:
            # Start traversal
```

## Edge Cases to Remember

1. **Empty grid**: Return 0
2. **All walls**: Return 0
3. **Single floor cell**: Return 1
4. **Large grid**: Use efficient traversal
5. **Boundary conditions**: Handle grid boundaries properly

## Problem-Solving Framework

1. **Identify graph nature**: This is a connected components problem in a grid
2. **Choose traversal method**: Use DFS or BFS to explore connected cells
3. **Mark visited cells**: Avoid revisiting the same cell
4. **Count components**: Each unvisited floor cell starts a new room
5. **Handle boundaries**: Check grid boundaries in traversal

---

*This analysis shows how to efficiently solve connected components problems in grids using graph traversal algorithms.* 