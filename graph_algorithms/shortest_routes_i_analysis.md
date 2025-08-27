# CSES Shortest Routes I - Problem Analysis

## Problem Statement
There are n cities and m flight connections. Your task is to find the shortest route from city 1 to all other cities.

### Input
The first input line has two integers n and m: the number of cities and flight connections. The cities are numbered 1,2,…,n.
Then, there are m lines describing the flight connections. Each line has three integers a, b, and c: there is a flight from city a to city b with cost c.

### Output
Print n integers: the shortest route lengths from city 1 to all cities. If there is no route, print -1.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n
- 1 ≤ c ≤ 10^9

### Example
```
Input:
3 4
1 2 6
1 3 2
3 2 3
1 3 4

Output:
0 5 2
```

## Solution Progression

### Approach 1: Dijkstra's Algorithm - O((n + m) * log(n))
**Description**: Use Dijkstra's algorithm with a priority queue to find shortest paths.

```python
import heapq

def shortest_routes_dijkstra(n, m, flights):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def dijkstra():
        distances = [float('inf')] * (n + 1)
        distances[1] = 0
        
        # Priority queue: (distance, node)
        pq = [(0, 1)]
        
        while pq:
            dist, node = heapq.heappop(pq)
            
            # If we've already found a shorter path, skip
            if dist > distances[node]:
                continue
            
            # Explore neighbors
            for neighbor, weight in graph[node]:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return distances
    
    distances = dijkstra()
    
    # Convert to output format
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result
```

**Why this is efficient**: Dijkstra's algorithm is optimal for finding shortest paths in graphs with non-negative edge weights.

### Improvement 1: Optimized Dijkstra with Early Termination - O((n + m) * log(n))
**Description**: Use optimized Dijkstra with early termination and better data structures.

```python
import heapq

def shortest_routes_optimized_dijkstra(n, m, flights):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def dijkstra_optimized():
        distances = [float('inf')] * (n + 1)
        distances[1] = 0
        
        # Use set for faster lookups
        visited = set()
        pq = [(0, 1)]
        
        while pq and len(visited) < n:
            dist, node = heapq.heappop(pq)
            
            if node in visited:
                continue
            
            visited.add(node)
            
            # Early termination if all nodes are visited
            if len(visited) == n:
                break
            
            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    new_dist = dist + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))
        
        return distances
    
    distances = dijkstra_optimized()
    
    # Convert to output format
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result
```

**Why this improvement works**: Early termination and using a set for visited nodes can improve performance for large graphs.

### Improvement 2: Bellman-Ford Algorithm - O(n*m)
**Description**: Use Bellman-Ford algorithm for graphs that might have negative edges.

```python
def shortest_routes_bellman_ford(n, m, flights):
    def bellman_ford():
        distances = [float('inf')] * (n + 1)
        distances[1] = 0
        
        # Relax edges n-1 times
        for _ in range(n - 1):
            for a, b, c in flights:
                if distances[a] != float('inf'):
                    if distances[a] + c < distances[b]:
                        distances[b] = distances[a] + c
        
        return distances
    
    distances = bellman_ford()
    
    # Convert to output format
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result
```

**Why this improvement works**: Bellman-Ford can handle negative edge weights and is simpler to implement.

### Alternative: SPFA (Shortest Path Faster Algorithm) - O(n*m)
**Description**: Use SPFA which is an optimization of Bellman-Ford.

```python
from collections import deque

def shortest_routes_spfa(n, m, flights):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def spfa():
        distances = [float('inf')] * (n + 1)
        distances[1] = 0
        
        # Queue for nodes to process
        queue = deque([1])
        in_queue = [False] * (n + 1)
        in_queue[1] = True
        
        while queue:
            node = queue.popleft()
            in_queue[node] = False
            
            for neighbor, weight in graph[node]:
                new_dist = distances[node] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    if not in_queue[neighbor]:
                        queue.append(neighbor)
                        in_queue[neighbor] = True
        
        return distances
    
    distances = spfa()
    
    # Convert to output format
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result
```

**Why this works**: SPFA is often faster than Bellman-Ford in practice, especially for sparse graphs.

## Final Optimal Solution

```python
import heapq

n, m = map(int, input().split())
flights = [tuple(map(int, input().split())) for _ in range(m)]

# Build adjacency list
graph = [[] for _ in range(n + 1)]
for a, b, c in flights:
    graph[a].append((b, c))

def dijkstra():
    distances = [float('inf')] * (n + 1)
    distances[1] = 0
    
    # Priority queue: (distance, node)
    pq = [(0, 1)]
    
    while pq:
        dist, node = heapq.heappop(pq)
        
        # If we've already found a shorter path, skip
        if dist > distances[node]:
            continue
        
        # Explore neighbors
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

distances = dijkstra()

# Convert to output format
result = []
for i in range(1, n + 1):
    if distances[i] == float('inf'):
        result.append(-1)
    else:
        result.append(distances[i])

print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Dijkstra's | O((n + m) * log(n)) | O(n + m) | Optimal for non-negative weights |
| Optimized Dijkstra | O((n + m) * log(n)) | O(n + m) | Early termination |
| Bellman-Ford | O(n*m) | O(n) | Handles negative weights |
| SPFA | O(n*m) | O(n + m) | Optimized Bellman-Ford |

## Key Insights for Other Problems

### 1. **Shortest Path Algorithms**
**Principle**: Choose appropriate shortest path algorithm based on graph characteristics.
**Applicable to**:
- Shortest path problems
- Graph algorithms
- Network routing
- Algorithm design

**Example Problems**:
- Shortest path problems
- Graph algorithms
- Network routing
- Algorithm design

### 2. **Priority Queue Usage**
**Principle**: Use priority queues to efficiently process nodes in order of increasing distance.
**Applicable to**:
- Dijkstra's algorithm
- Priority-based algorithms
- Graph traversal
- Algorithm optimization

**Example Problems**:
- Dijkstra's algorithm
- Priority-based algorithms
- Graph traversal
- Algorithm optimization

### 3. **Edge Relaxation**
**Principle**: Relax edges to update shortest path distances during algorithm execution.
**Applicable to**:
- Shortest path algorithms
- Dynamic programming
- Graph algorithms
- Algorithm design

**Example Problems**:
- Shortest path algorithms
- Dynamic programming
- Graph algorithms
- Algorithm design

### 4. **Negative Edge Handling**
**Principle**: Use appropriate algorithms (Bellman-Ford, SPFA) for graphs with negative edge weights.
**Applicable to**:
- Negative weight graphs
- Graph algorithms
- Algorithm selection
- Problem solving

**Example Problems**:
- Negative weight graphs
- Graph algorithms
- Algorithm selection
- Problem solving

## Notable Techniques

### 1. **Dijkstra's Pattern**
```python
def dijkstra(graph, start, n):
    distances = [float('inf')] * n
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        dist, node = heapq.heappop(pq)
        if dist > distances[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances
```

### 2. **Bellman-Ford Pattern**
```python
def bellman_ford(edges, n, start):
    distances = [float('inf')] * n
    distances[start] = 0
    
    for _ in range(n - 1):
        for u, v, w in edges:
            if distances[u] != float('inf'):
                distances[v] = min(distances[v], distances[u] + w)
    
    return distances
```

### 3. **SPFA Pattern**
```python
def spfa(graph, start, n):
    distances = [float('inf')] * n
    distances[start] = 0
    queue = deque([start])
    in_queue = [False] * n
    in_queue[start] = True
    
    while queue:
        node = queue.popleft()
        in_queue[node] = False
        
        for neighbor, weight in graph[node]:
            new_dist = distances[node] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True
    
    return distances
```

## Edge Cases to Remember

1. **No path exists**: Return -1 for unreachable nodes
2. **Negative cycles**: Handle with appropriate algorithm
3. **Large edge weights**: Use appropriate data types
4. **Self-loops**: Handle properly
5. **Multiple edges**: Consider minimum weight

## Problem-Solving Framework

1. **Identify shortest path nature**: This is a single-source shortest path problem
2. **Choose algorithm**: Use Dijkstra's for non-negative weights
3. **Handle edge cases**: Check for unreachable nodes
4. **Optimize performance**: Use priority queue efficiently
5. **Format output**: Convert distances to required format

---

*This analysis shows how to efficiently solve single-source shortest path problems using various graph algorithms.* 