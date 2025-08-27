# CSES Monsters - Problem Analysis

## Problem Statement
You are playing a game where you have a grid of size n×m. Each cell is either free (.) or a wall (#). You are initially in the upper-left corner, and you want to reach the lower-right corner. However, there are monsters that move according to a specific pattern.

Your task is to determine if it is possible to reach the destination without being caught by a monster.

### Input
The first input line has two integers n and m: the height and width of the grid.
Then there are n lines that describe the grid. Each line has m characters: "." denotes a free cell, "#" denotes a wall, "A" denotes your starting position, and "M" denotes a monster.

### Output
Print "YES" if it is possible to reach the destination, and "NO" otherwise.

### Constraints
- 1 ≤ n,m ≤ 1000

### Example
```
Input:
5 8
########
#M..A..#
#.#.M#.#
#M#..#..
#.######

Output:
YES
```

## Solution Progression

### Approach 1: Multi-Source BFS - O(n*m)
**Description**: Use multi-source BFS to find the shortest distance from monsters to each cell, then check if you can reach the destination.

```python
from collections import deque

def monsters_multi_bfs(n, m, grid):
    def find_monster_distances():
        distances = [[float('inf')] * m for _ in range(n)]
        queue = deque()
        
        # Find all monsters and add them to queue
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'M':
                    queue.append((i, j, 0))
                    distances[i][j] = 0
        
        # BFS to find distances from monsters
        while queue:
            row, col, dist = queue.popleft()
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    grid[nr][nc] != '#' and 
                    distances[nr][nc] == float('inf')):
                    distances[nr][nc] = dist + 1
                    queue.append((nr, nc, dist + 1))
        
        return distances
    
    def can_reach_destination():
        # Find start position
        start_row, start_col = -1, -1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'A':
                    start_row, start_col = i, j
                    break
            if start_row != -1:
                break
        
        monster_distances = find_monster_distances()
        
        # BFS from start to destination
        queue = deque([(start_row, start_col, 0)])
        visited = [[False] * m for _ in range(n)]
        visited[start_row][start_col] = True
        
        while queue:
            row, col, dist = queue.popleft()
            
            # Check if we reached destination
            if row == n-1 and col == m-1:
                return True
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    grid[nr][nc] != '#' and 
                    not visited[nr][nc] and
                    dist + 1 < monster_distances[nr][nc]):
                    visited[nr][nc] = True
                    queue.append((nr, nc, dist + 1))
        
        return False
    
    return "YES" if can_reach_destination() else "NO"
```

**Why this is efficient**: We use BFS to find distances from monsters and then check if we can reach the destination before monsters.

### Improvement 1: Optimized BFS with Early Termination - O(n*m)
**Description**: Use optimized BFS with early termination for better performance.

```python
from collections import deque

def monsters_optimized_bfs(n, m, grid):
    def find_monster_distances():
        distances = [[float('inf')] * m for _ in range(n)]
        queue = deque()
        
        # Find all monsters
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'M':
                    queue.append((i, j))
                    distances[i][j] = 0
        
        # Multi-source BFS
        while queue:
            row, col = queue.popleft()
            current_dist = distances[row][col]
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    grid[nr][nc] != '#' and 
                    distances[nr][nc] == float('inf')):
                    distances[nr][nc] = current_dist + 1
                    queue.append((nr, nc))
        
        return distances
    
    def can_escape():
        # Find start position
        start_row, start_col = -1, -1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'A':
                    start_row, start_col = i, j
                    break
            if start_row != -1:
                break
        
        monster_distances = find_monster_distances()
        
        # Check if start is already caught
        if monster_distances[start_row][start_col] == 0:
            return False
        
        # BFS from start
        queue = deque([(start_row, start_col, 0)])
        visited = [[False] * m for _ in range(n)]
        visited[start_row][start_col] = True
        
        while queue:
            row, col, dist = queue.popleft()
            
            # Check if we reached destination
            if row == n-1 and col == m-1:
                return True
            
            # Check if we can reach border (alternative escape)
            if row == 0 or row == n-1 or col == 0 or col == m-1:
                return True
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    grid[nr][nc] != '#' and 
                    not visited[nr][nc] and
                    dist + 1 < monster_distances[nr][nc]):
                    visited[nr][nc] = True
                    queue.append((nr, nc, dist + 1))
        
        return False
    
    return "YES" if can_escape() else "NO"
```

**Why this improvement works**: We add early termination when reaching the border and optimize the monster distance calculation.

### Improvement 2: BFS with Priority Queue - O(n*m * log(n*m))
**Description**: Use BFS with priority queue to prioritize safer paths.

```python
import heapq
from collections import deque

def monsters_priority_bfs(n, m, grid):
    def find_monster_distances():
        distances = [[float('inf')] * m for _ in range(n)]
        queue = deque()
        
        # Find all monsters
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'M':
                    queue.append((i, j))
                    distances[i][j] = 0
        
        # Multi-source BFS
        while queue:
            row, col = queue.popleft()
            current_dist = distances[row][col]
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    grid[nr][nc] != '#' and 
                    distances[nr][nc] == float('inf')):
                    distances[nr][nc] = current_dist + 1
                    queue.append((nr, nc))
        
        return distances
    
    def can_escape_priority():
        # Find start position
        start_row, start_col = -1, -1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'A':
                    start_row, start_col = i, j
                    break
            if start_row != -1:
                break
        
        monster_distances = find_monster_distances()
        
        # Priority queue: (safety_margin, row, col, dist)
        pq = [(-monster_distances[start_row][start_col], start_row, start_col, 0)]
        visited = [[False] * m for _ in range(n)]
        visited[start_row][start_col] = True
        
        while pq:
            safety_margin, row, col, dist = heapq.heappop(pq)
            safety_margin = -safety_margin  # Convert back to positive
            
            # Check if we reached destination
            if row == n-1 and col == m-1:
                return True
            
            # Check if we can reach border
            if row == 0 or row == n-1 or col == 0 or col == m-1:
                return True
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    grid[nr][nc] != '#' and 
                    not visited[nr][nc]):
                    new_safety = monster_distances[nr][nc] - (dist + 1)
                    if new_safety > 0:
                        visited[nr][nc] = True
                        heapq.heappush(pq, (-new_safety, nr, nc, dist + 1))
        
        return False
    
    return "YES" if can_escape_priority() else "NO"
```

**Why this improvement works**: Priority queue helps us explore safer paths first, potentially finding a solution faster.

### Alternative: A* Search - O(n*m * log(n*m))
**Description**: Use A* search with heuristic for potentially faster path finding.

```python
import heapq
from collections import deque

def monsters_astar(n, m, grid):
    def manhattan_distance(row, col):
        return abs(n-1 - row) + abs(m-1 - col)
    
    def find_monster_distances():
        distances = [[float('inf')] * m for _ in range(n)]
        queue = deque()
        
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'M':
                    queue.append((i, j))
                    distances[i][j] = 0
        
        while queue:
            row, col = queue.popleft()
            current_dist = distances[row][col]
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    grid[nr][nc] != '#' and 
                    distances[nr][nc] == float('inf')):
                    distances[nr][nc] = current_dist + 1
                    queue.append((nr, nc))
        
        return distances
    
    def astar_search():
        # Find start position
        start_row, start_col = -1, -1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'A':
                    start_row, start_col = i, j
                    break
            if start_row != -1:
                break
        
        monster_distances = find_monster_distances()
        
        # A* search: (f_score, safety_margin, row, col, g_score)
        pq = [(manhattan_distance(start_row, start_col), 
               monster_distances[start_row][start_col], 
               start_row, start_col, 0)]
        visited = [[False] * m for _ in range(n)]
        visited[start_row][start_col] = True
        
        while pq:
            f_score, safety_margin, row, col, g_score = heapq.heappop(pq)
            
            # Check if we reached destination
            if row == n-1 and col == m-1:
                return True
            
            # Check if we can reach border
            if row == 0 or row == n-1 or col == 0 or col == m-1:
                return True
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < n and 0 <= nc < m and 
                    grid[nr][nc] != '#' and 
                    not visited[nr][nc]):
                    new_g_score = g_score + 1
                    new_safety = monster_distances[nr][nc] - new_g_score
                    if new_safety > 0:
                        visited[nr][nc] = True
                        h_score = manhattan_distance(nr, nc)
                        f_score = new_g_score + h_score
                        heapq.heappush(pq, (f_score, new_safety, nr, nc, new_g_score))
        
        return False
    
    return "YES" if astar_search() else "NO"
```

**Why this works**: A* search uses a heuristic to guide the search toward the goal, potentially reducing the number of nodes explored.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

def find_monster_distances():
    distances = [[float('inf')] * m for _ in range(n)]
    queue = deque()
    
    # Find all monsters
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'M':
                queue.append((i, j))
                distances[i][j] = 0
    
    # Multi-source BFS
    while queue:
        row, col = queue.popleft()
        current_dist = distances[row][col]
        
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                grid[nr][nc] != '#' and 
                distances[nr][nc] == float('inf')):
                distances[nr][nc] = current_dist + 1
                queue.append((nr, nc))
    
    return distances

def can_escape():
    # Find start position
    start_row, start_col = -1, -1
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A':
                start_row, start_col = i, j
                break
        if start_row != -1:
            break
    
    monster_distances = find_monster_distances()
    
    # Check if start is already caught
    if monster_distances[start_row][start_col] == 0:
        return False
    
    # BFS from start
    queue = deque([(start_row, start_col, 0)])
    visited = [[False] * m for _ in range(n)]
    visited[start_row][start_col] = True
    
    while queue:
        row, col, dist = queue.popleft()
        
        # Check if we reached destination
        if row == n-1 and col == m-1:
            return True
        
        # Check if we can reach border
        if row == 0 or row == n-1 or col == 0 or col == m-1:
            return True
        
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < n and 0 <= nc < m and 
                grid[nr][nc] != '#' and 
                not visited[nr][nc] and
                dist + 1 < monster_distances[nr][nc]):
                visited[nr][nc] = True
                queue.append((nr, nc, dist + 1))
    
    return False

print("YES" if can_escape() else "NO")
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Multi-Source BFS | O(n*m) | O(n*m) | Find monster distances first |
| Optimized BFS | O(n*m) | O(n*m) | Early termination at border |
| Priority BFS | O(n*m * log(n*m)) | O(n*m) | Prioritize safer paths |
| A* Search | O(n*m * log(n*m)) | O(n*m) | Heuristic-guided search |

## Key Insights for Other Problems

### 1. **Multi-Source BFS**
**Principle**: Use BFS from multiple starting points to find distances to all reachable nodes.
**Applicable to**:
- Multi-source problems
- Distance calculations
- Flood fill
- Graph algorithms

**Example Problems**:
- Multi-source problems
- Distance calculations
- Flood fill
- Graph algorithms

### 2. **Safety Margin Calculation**
**Principle**: Calculate the safety margin between player and monster positions.
**Applicable to**:
- Safety analysis
- Risk assessment
- Game theory
- Algorithm design

**Example Problems**:
- Safety analysis
- Risk assessment
- Game theory
- Algorithm design

### 3. **Grid Path Finding with Constraints**
**Principle**: Find paths in grids while respecting dynamic constraints (monster positions).
**Applicable to**:
- Grid path finding
- Constraint satisfaction
- Dynamic obstacles
- Algorithm design

**Example Problems**:
- Grid path finding
- Constraint satisfaction
- Dynamic obstacles
- Algorithm design

### 4. **Early Termination**
**Principle**: Use early termination conditions to improve algorithm efficiency.
**Applicable to**:
- Algorithm optimization
- Performance improvement
- Search algorithms
- Problem solving

**Example Problems**:
- Algorithm optimization
- Performance improvement
- Search algorithms
- Problem solving

## Notable Techniques

### 1. **Multi-Source BFS Pattern**
```python
def multi_source_bfs(sources, graph):
    queue = deque(sources)
    distances = [float('inf')] * len(graph)
    for source in sources:
        distances[source] = 0
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)
    return distances
```

### 2. **Safety Margin Pattern**
```python
def calculate_safety_margin(player_pos, monster_distances, player_dist):
    return monster_distances[player_pos] - player_dist
```

### 3. **Grid BFS Pattern**
```python
def grid_bfs(grid, start, target):
    queue = deque([(start[0], start[1], 0)])
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    visited[start[0]][start[1]] = True
    
    while queue:
        row, col, dist = queue.popleft()
        if (row, col) == target:
            return dist
        
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if valid_cell(nr, nc, grid) and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc, dist + 1))
```

## Edge Cases to Remember

1. **No monsters**: Always possible to reach destination
2. **Start position is wall**: Impossible
3. **Destination is wall**: Impossible
4. **Monster at start**: Impossible
5. **Large grid**: Use efficient algorithm

## Problem-Solving Framework

1. **Identify multi-source nature**: This is a multi-source BFS problem
2. **Calculate monster distances**: Use multi-source BFS from all monsters
3. **Find player path**: Use BFS from player with safety constraints
4. **Check safety margin**: Ensure player reaches destination before monsters
5. **Handle edge cases**: Consider border escape and immediate capture

---

*This analysis shows how to efficiently solve multi-source BFS problems with safety constraints using graph algorithms.* 