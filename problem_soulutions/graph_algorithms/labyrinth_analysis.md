---
layout: simple
title: "Labyrinth
permalink: /problem_soulutions/graph_algorithms/labyrinth_analysis/
---

# Labyrinth

## Problem Statement
You are given a map of a labyrinth, and your task is to count the number of walls between the upper-left and lower-right corner.

The labyrinth consists of n×m squares, and each square is either wall or floor. You can walk left, right, up, and down through the floor squares.

### Input
The first input line has two integers n and m: the height and width of the labyrinth."
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

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Labyrinth with Costs**
**Variation**: Each wall has a different cost to break through.
**Approach**: Use Dijkstra's algorithm with cost tracking.
```python
def cost_based_labyrinth(n, m, grid, costs):
    # costs[i][j] = cost to break wall at position (i, j)
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    dist = [[float('inf')] * m for _ in range(n)]
    dist[0][0] = 0
    
    pq = [(0, 0, 0)]  # (cost, row, col)
    
    while pq:
        cost, row, col = heapq.heappop(pq)
        
        if row == n-1 and col == m-1:
            return cost
        
        if cost > dist[row][col]:
            continue
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < m:
                wall_cost = costs[nr][nc] if grid[nr][nc] == '#' else 0
                new_cost = cost + wall_cost
                
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(pq, (new_cost, nr, nc))
    
    return -1
```

#### 2. **Labyrinth with Constraints**
**Variation**: Limited number of walls can be broken.
**Approach**: Use BFS with state tracking.
```python
def constrained_labyrinth(n, m, grid, max_walls):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited = set()
    queue = deque([(0, 0, 0, 0)])  # (row, col, walls_broken, steps)
    
    while queue:
        row, col, walls, steps = queue.popleft()
        
        if row == n-1 and col == m-1:
            return steps
        
        state = (row, col, walls)
        if state in visited:
            continue
        visited.add(state)
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < m:
                if grid[nr][nc] == '.':
                    queue.append((nr, nc, walls, steps + 1))
                elif grid[nr][nc] == '#' and walls < max_walls:
                    queue.append((nr, nc, walls + 1, steps + 1))
    
    return -1
```

#### 3. **Labyrinth with Probabilities**
**Variation**: Each wall has a probability of being breakable.
**Approach**: Use Monte Carlo simulation or expected value calculation.
```python
def probabilistic_labyrinth(n, m, grid, probabilities):
    # probabilities[i][j] = probability wall at (i,j) can be broken
    
    def monte_carlo_simulation(trials=1000):
        successful_paths = 0
        
        for _ in range(trials):
            if can_reach_end_with_probabilities(n, m, grid, probabilities):
                successful_paths += 1
        
        return successful_paths / trials
    
    def can_reach_end_with_probabilities(n, m, grid, probs):
        # Simplified simulation - in practice would use more sophisticated approach
        visited = [[False] * m for _ in range(n)]
        return dfs_with_probabilities(0, 0, n, m, grid, probs, visited)
    
    return monte_carlo_simulation()
```

#### 4. **Labyrinth with Multiple Exits**
**Variation**: Multiple possible exit points with different values.
**Approach**: Find shortest path to each exit and choose best.
```python
def multiple_exits_labyrinth(n, m, grid, exits):
    # exits = [(row, col, value), ...]
    
    def find_shortest_to_exit(start_row, start_col, exit_row, exit_col):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        visited = [[False] * m for _ in range(n)]
        queue = deque([(start_row, start_col, 0)])
        
        while queue:
            row, col, steps = queue.popleft()
            
            if row == exit_row and col == exit_col:
                return steps
            
            if visited[row][col]:
                continue
            visited[row][col] = True
            
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == '.':
                    queue.append((nr, nc, steps + 1))
        
        return float('inf')
    
    best_value = 0
    for exit_row, exit_col, value in exits:
        steps = find_shortest_to_exit(0, 0, exit_row, exit_col)
        if steps != float('inf'):
            best_value = max(best_value, value - steps)
    
    return best_value
```

#### 5. **Labyrinth with Dynamic Walls**
**Variation**: Walls can appear/disappear based on time or conditions.
**Approach**: Use time-based state tracking or dynamic programming.
```python
def dynamic_walls_labyrinth(n, m, grid, wall_schedule):
    # wall_schedule[(row, col)] = [(start_time, end_time), ...]
    
    def is_wall_at_time(row, col, time):
        if grid[row][col] == '#':
            return True
        if (row, col) in wall_schedule:
            for start, end in wall_schedule[(row, col)]:
                if start <= time <= end:
                    return True
        return False
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited = set()
    queue = deque([(0, 0, 0)])  # (row, col, time)
    
    while queue:
        row, col, time = queue.popleft()
        
        if row == n-1 and col == m-1:
            return time
        
        state = (row, col, time)
        if state in visited:
            continue
        visited.add(state)
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < m:
                if not is_wall_at_time(nr, nc, time + 1):
                    queue.append((nr, nc, time + 1))
    
    return -1
```

### Related Problems & Concepts

#### 1. **Path Finding Problems**
- **Shortest Path**: Dijkstra's, Bellman-Ford, Floyd-Warshall
- **Grid Path Finding**: BFS, DFS, A* search
- **Maze Problems**: Wall following, flood fill
- **Navigation**: GPS routing, robot navigation

#### 2. **Graph Theory**
- **Connectivity**: Strongly connected components
- **Flow Networks**: Maximum flow, minimum cut
- **Matching**: Bipartite matching, stable marriage
- **Coloring**: Graph coloring, bipartite graphs

#### 3. **Dynamic Programming**
- **Grid DP**: Path counting, minimum cost paths
- **State Compression**: Bit manipulation for states
- **Memoization**: Caching recursive solutions
- **Optimal Substructure**: Breaking down problems

#### 4. **Search Algorithms**
- **Breadth-First Search**: Level-by-level exploration
- **Depth-First Search**: Recursive exploration
- **A* Search**: Heuristic-guided search
- **Iterative Deepening**: Memory-efficient search

#### 5. **Optimization Problems**
- **Shortest Path**: Minimum distance/cost
- **Resource Allocation**: Limited resources
- **Scheduling**: Time-based constraints
- **Network Flow**: Maximum throughput

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict time constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large datasets
- **Edge Cases**: Robust error handling

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient array processing
- **Sliding Window**: Optimal subarray problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Combinatorics**
- **Path Counting**: Number of valid paths
- **Permutations**: Order of moves
- **Combinations**: Choice of walls to break
- **Catalan Numbers**: Valid path sequences

#### 2. **Probability Theory**
- **Expected Values**: Average path length
- **Markov Chains**: State transitions
- **Random Walks**: Stochastic processes
- **Monte Carlo**: Simulation methods

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime numbers

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Grid and graph problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Grid Problems**: Maze navigation, path finding
- **Graph Problems**: Shortest path, connectivity
- **Dynamic Programming**: State optimization
- **Search Problems**: BFS, DFS, A* search 