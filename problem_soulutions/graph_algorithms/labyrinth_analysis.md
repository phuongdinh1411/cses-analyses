# CSES Labyrinth - Problem Analysis

## Problem Statement
You are given a map of a labyrinth, and your task is to count the number of walls between the upper-left and lower-right corner.

The labyrinth consists of n×m squares, and each square is either wall or floor. You can walk left, right, up, and down through the floor squares.

### Input
The first input line has two integers n and m: the height and width of the labyrinth.
Then there are n lines that describe the labyrinth. Each line has m characters: "." denotes a floor and "#" denotes a wall.

### Output
Print one integer: the number of walls between the upper-left and lower-right corner.

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
2
```

## Solution Progression

### Approach 1: BFS with Wall Counting - O(n*m)
**Description**: Use breadth-first search to find the shortest path and count walls.

```python
from collections import deque

def labyrinth_bfs(n, m, grid):
    def bfs():
        queue = deque([(0, 0, 0)])  # (row, col, walls)
        visited = [[False] * m for _ in range(n)]
        
        while queue:
            row, col, walls = queue.popleft()
            
            if row == n-1 and col == m-1:
                return walls
            
            if visited[row][col]:
                continue
            
            visited[row][col] = True
            
            # Explore all four directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    not visited[nr][nc]):
                    if grid[nr][nc] == '#':
                        queue.append((nr, nc, walls + 1))
                    else:
                        queue.appendleft((nr, nc, walls))  # Prioritize floors
        
        return -1  # No path found
    
    return bfs()
```

**Why this is efficient**: We use BFS with a modified queue that prioritizes floor cells over wall cells, ensuring we find the path with minimum walls.

### Improvement 1: Dijkstra's Algorithm - O(n*m * log(n*m))
**Description**: Use Dijkstra's algorithm with a priority queue to find the shortest path.

```python
import heapq

def labyrinth_dijkstra(n, m, grid):
    def dijkstra():
        pq = [(0, 0, 0)]  # (walls, row, col)
        distances = [[float('inf')] * m for _ in range(n)]
        distances[0][0] = 0
        
        while pq:
            walls, row, col = heapq.heappop(pq)
            
            if row == n-1 and col == m-1:
                return walls
            
            if walls > distances[row][col]:
                continue
            
            # Explore all four directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m:
                    new_walls = walls + (1 if grid[nr][nc] == '#' else 0)
                    if new_walls < distances[nr][nc]:
                        distances[nr][nc] = new_walls
                        heapq.heappush(pq, (new_walls, nr, nc))
        
        return -1  # No path found
    
    return dijkstra()
```

**Why this improvement works**: Dijkstra's algorithm guarantees finding the shortest path with minimum wall count, though it's slightly more complex than BFS.

### Improvement 2: 0-1 BFS - O(n*m)
**Description**: Use 0-1 BFS which is more efficient than Dijkstra's for this problem.

```python
from collections import deque

def labyrinth_01_bfs(n, m, grid):
    def bfs_01():
        queue = deque([(0, 0, 0)])  # (row, col, walls)
        visited = [[False] * m for _ in range(n)]
        
        while queue:
            row, col, walls = queue.popleft()
            
            if row == n-1 and col == m-1:
                return walls
            
            if visited[row][col]:
                continue
            
            visited[row][col] = True
            
            # Explore all four directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    not visited[nr][nc]):
                    if grid[nr][nc] == '#':
                        queue.append((nr, nc, walls + 1))  # Add to end
                    else:
                        queue.appendleft((nr, nc, walls))  # Add to front
        
        return -1  # No path found
    
    return bfs_01()
```

**Why this improvement works**: 0-1 BFS is optimal for this problem since we have only two types of edges (0 and 1), making it more efficient than Dijkstra's.

### Alternative: A* Search - O(n*m * log(n*m))
**Description**: Use A* search with Manhattan distance heuristic for potentially faster search.

```python
import heapq

def labyrinth_astar(n, m, grid):
    def manhattan_distance(row, col):
        return abs(n-1 - row) + abs(m-1 - col)
    
    def astar():
        pq = [(manhattan_distance(0, 0), 0, 0, 0)]  # (f, walls, row, col)
        distances = [[float('inf')] * m for _ in range(n)]
        distances[0][0] = 0
        
        while pq:
            f, walls, row, col = heapq.heappop(pq)
            
            if row == n-1 and col == m-1:
                return walls
            
            if walls > distances[row][col]:
                continue
            
            # Explore all four directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m:
                    new_walls = walls + (1 if grid[nr][nc] == '#' else 0)
                    if new_walls < distances[nr][nc]:
                        distances[nr][nc] = new_walls
                        h = manhattan_distance(nr, nc)
                        heapq.heappush(pq, (new_walls + h, new_walls, nr, nc))
        
        return -1  # No path found
    
    return astar()
```

**Why this works**: A* search uses a heuristic to guide the search toward the goal, potentially reducing the number of nodes explored.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

def bfs_01():
    queue = deque([(0, 0, 0)])  # (row, col, walls)
    visited = [[False] * m for _ in range(n)]
    
    while queue:
        row, col, walls = queue.popleft()
        
        if row == n-1 and col == m-1:
            return walls
        
        if visited[row][col]:
            continue
        
        visited[row][col] = True
        
        # Explore all four directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                not visited[nr][nc]):
                if grid[nr][nc] == '#':
                    queue.append((nr, nc, walls + 1))  # Add to end
                else:
                    queue.appendleft((nr, nc, walls))  # Add to front
    
    return -1  # No path found

result = bfs_01()
print(result if result != -1 else "IMPOSSIBLE")
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS with Wall Counting | O(n*m) | O(n*m) | Use modified queue |
| Dijkstra's | O(n*m * log(n*m)) | O(n*m) | Guaranteed shortest path |
| 0-1 BFS | O(n*m) | O(n*m) | Optimal for 0-1 weights |
| A* Search | O(n*m * log(n*m)) | O(n*m) | Heuristic-guided search |

## Key Insights for Other Problems

### 1. **Shortest Path with Weighted Edges**
**Principle**: Use appropriate shortest path algorithms based on edge weights and problem constraints.
**Applicable to**:
- Shortest path problems
- Weighted graphs
- Grid problems
- Path finding

**Example Problems**:
- Shortest path
- Weighted graphs
- Grid problems
- Path finding

### 2. **0-1 BFS for Binary Weights**
**Principle**: Use 0-1 BFS when edges have only two possible weights (0 and 1).
**Applicable to**:
- Binary weight graphs
- Shortest path problems
- Grid problems
- Algorithm optimization

**Example Problems**:
- Binary weight graphs
- Shortest path problems
- Grid problems
- Algorithm optimization

### 3. **Priority Queue vs Deque**
**Principle**: Choose between priority queue and deque based on edge weight characteristics.
**Applicable to**:
- Graph algorithms
- Shortest path
- Algorithm design
- Performance optimization

**Example Problems**:
- Graph algorithms
- Shortest path
- Algorithm design
- Performance optimization

### 4. **Heuristic Search**
**Principle**: Use heuristic functions to guide search algorithms toward the goal.
**Applicable to**:
- Search algorithms
- Path finding
- Optimization problems
- Algorithm design

**Example Problems**:
- Search algorithms
- Path finding
- Optimization problems
- Algorithm design

## Notable Techniques

### 1. **0-1 BFS Pattern**
```python
from collections import deque
def bfs_01():
    queue = deque([(start, 0)])
    while queue:
        node, cost = queue.popleft()
        for neighbor in graph[node]:
            new_cost = cost + weight
            if weight == 0:
                queue.appendleft((neighbor, new_cost))
            else:
                queue.append((neighbor, new_cost))
```

### 2. **Dijkstra's Pattern**
```python
import heapq
def dijkstra():
    pq = [(0, start)]
    distances = [float('inf')] * n
    while pq:
        dist, node = heapq.heappop(pq)
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
```

### 3. **Grid Path Finding Pattern**
```python
# Define directions
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for dr, dc in directions:
    nr, nc = row + dr, col + dc
    if valid_cell(nr, nc):
        # Process neighbor
```

## Edge Cases to Remember

1. **No path exists**: Return -1 or "IMPOSSIBLE"
2. **Start/end is wall**: Handle properly
3. **Single cell grid**: Handle edge case
4. **Large grid**: Use efficient algorithm
5. **Boundary conditions**: Check grid boundaries

## Problem-Solving Framework

1. **Identify path finding nature**: This is a shortest path problem with weighted edges
2. **Choose algorithm**: Use 0-1 BFS for binary weights
3. **Handle edge weights**: Walls have weight 1, floors have weight 0
4. **Use appropriate data structure**: Deque for 0-1 BFS
5. **Check path existence**: Handle case where no path exists

---

*This analysis shows how to efficiently solve shortest path problems in grids with weighted edges using appropriate graph algorithms.* 