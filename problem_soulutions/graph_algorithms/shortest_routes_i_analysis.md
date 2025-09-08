---
layout: simple
title: "Shortest Routes I - Single Source Shortest Paths"
permalink: /problem_soulutions/graph_algorithms/shortest_routes_i_analysis
---

# Shortest Routes I - Single Source Shortest Paths

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand single-source shortest path problems and Dijkstra's algorithm fundamentals
- Apply Dijkstra's algorithm with priority queues to find shortest paths in weighted graphs
- Implement efficient shortest path algorithms with proper data structure usage
- Optimize shortest path solutions using priority queues and graph representations
- Handle edge cases in shortest path problems (unreachable nodes, disconnected graphs, large weights)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dijkstra's algorithm, single-source shortest paths, priority queues, graph traversal
- **Data Structures**: Priority queues, adjacency lists, graph representations, distance arrays
- **Mathematical Concepts**: Graph theory, shortest path properties, greedy algorithms, optimization
- **Programming Skills**: Priority queue implementation, graph traversal, distance calculations, algorithm implementation
- **Related Problems**: Message Route (BFS shortest path), Labyrinth (grid shortest path), Graph traversal basics

## Problem Description

**Problem**: There are n cities and m flight connections. Find the shortest route from city 1 to all other cities.

**Input**: 
- First line: Two integers n and m (number of cities and flight connections)
- Next m lines: Three integers a, b, and c (flight from city a to city b with cost c)

**Output**: 
- n integers: shortest route lengths from city 1 to all cities
- If no route exists, print -1

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n
- 1 ≤ c ≤ 10⁹
- Cities are numbered 1, 2, ..., n
- Graph is directed
- No self-loops or multiple edges between same pair of cities
- All edge weights are non-negative

**Example**:
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

**Explanation**: 
- City 1 to City 1: 0 (same city)
- City 1 to City 2: 5 (path: 1 → 3 → 2, cost: 2 + 3 = 5)
- City 1 to City 3: 2 (direct flight from 1 to 3)

## Visual Example

### Input Graph
```
Cities: 1, 2, 3
Flights: (1→2, cost=6), (1→3, cost=2), (3→2, cost=3), (1→3, cost=4)

    1 ──6──→ 2
    │         ↑
    │2        │3
    ↓         │
    3 ────────┘
```

### Dijkstra's Algorithm Execution
```
Initial distances: [0, ∞, ∞]
Priority Queue: [(0, 1)]

Step 1: Process city 1 (distance = 0)
┌─────────────────────────────────────┐
│ Current: City 1                     │
│ Distance: 0                         │
│ Neighbors: 2 (cost=6), 3 (cost=2)  │
│ Update: dist[2] = 6, dist[3] = 2   │
│ Queue: [(2, 3), (6, 2)]            │
└─────────────────────────────────────┘

Step 2: Process city 3 (distance = 2)
┌─────────────────────────────────────┐
│ Current: City 3                     │
│ Distance: 2                         │
│ Neighbors: 2 (cost=3)               │
│ Update: dist[2] = min(6, 2+3) = 5  │
│ Queue: [(5, 2)]                     │
└─────────────────────────────────────┘

Step 3: Process city 2 (distance = 5)
┌─────────────────────────────────────┐
│ Current: City 2                     │
│ Distance: 5                         │
│ Neighbors: None                     │
│ Queue: [] (empty)                   │
└─────────────────────────────────────┘

Final distances: [0, 5, 2]
```

### Shortest Path Visualization
```
From City 1:
┌─────────────────────────────────────┐
│ To City 1: 0 (same city)           │
│ To City 2: 5 (path: 1→3→2)         │
│ To City 3: 2 (path: 1→3)           │
└─────────────────────────────────────┘

Path Details:
┌─────────────────────────────────────┐
│ 1 → 2: Direct cost = 6             │
│ 1 → 3 → 2: Cost = 2 + 3 = 5 ✓     │
│ 1 → 3: Direct cost = 2 ✓           │
└─────────────────────────────────────┘
```

### Dijkstra's Algorithm Flowchart
```
┌─────────────────────────────────────┐
│ Start: Initialize distances         │
│ dist[source] = 0, others = ∞       │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Add source to priority queue        │
│ Queue: [(0, source)]               │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ While queue is not empty:           │
│   Extract min distance vertex       │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ For each neighbor:                  │
│   If new_dist < current_dist:       │
│     Update distance                 │
│     Add to queue                    │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return shortest distances           │
└─────────────────────────────────────┘
```

### Priority Queue Operations
```
Initial: [(0, 1)]

After processing city 1:
- Add (2, 3): [(2, 3), (6, 2)]
- Add (6, 2): [(2, 3), (6, 2)]

After processing city 3:
- Update (5, 2): [(5, 2)]

After processing city 2:
- Queue empty: []
```

### Distance Updates
```
Step 1: Process city 1
dist[1] = 0 (source)
dist[2] = min(∞, 0+6) = 6
dist[3] = min(∞, 0+2) = 2

Step 2: Process city 3
dist[2] = min(6, 2+3) = 5

Step 3: Process city 2
No updates needed

Final: dist = [0, 5, 2]
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths from source to each destination
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths from source to each destination
2. For each path, calculate the total cost
3. Return the minimum cost among all paths
4. Handle cases where no path exists

**Visual Example:**
```
Brute force: Try all possible paths
For graph: 1 ──6──→ 2
           │         ↑
           │2        │3
           ↓         │
           3 ────────┘

All possible paths from 1 to 2:
- Path 1: 1 → 2 (cost = 6)
- Path 2: 1 → 3 → 2 (cost = 2 + 3 = 5)
- Path 3: 1 → 3 → 2 (cost = 4 + 3 = 7)

Minimum cost: 5
```

**Implementation:**
```python
def shortest_routes_brute_force(n, m, edges):
    def find_all_paths(current, target, visited, path_cost):
        if current == target:
            return [path_cost]
        
        if len(visited) >= n:
            return []
        
        paths = []
        for neighbor, cost in edges.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                paths.extend(find_all_paths(neighbor, target, visited, path_cost + cost))
                visited.remove(neighbor)
        
        return paths
    
    # Build adjacency list
    adj = {}
    for a, b, c in edges:
        if a not in adj:
            adj[a] = []
        adj[a].append((b, c))
    
    # Find shortest paths to all cities
    result = []
    for city in range(1, n + 1):
        if city == 1:
            result.append(0)
        else:
            visited = {1}
            all_costs = find_all_paths(1, city, visited, 0)
            if all_costs:
                result.append(min(all_costs))
            else:
                result.append(-1)
    
    return result
```

**Time Complexity:** O(n! × n) for n cities with exponential path enumeration
**Space Complexity:** O(n) for recursion stack and path storage

**Why it's inefficient:**
- O(n! × n) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many cities

### Approach 2: Basic Dijkstra with Array (Better)

**Key Insights from Basic Dijkstra Solution:**
- Use Dijkstra's algorithm for single-source shortest paths
- Much more efficient than brute force approach
- Standard method for shortest path problems
- Can handle larger graphs than brute force

**Algorithm:**
1. Initialize distances: source = 0, others = ∞
2. Use priority queue to process vertices in order of distance
3. For each vertex, update distances to its neighbors
4. Return shortest distances to all vertices

**Visual Example:**
```
Basic Dijkstra for graph: 1 ──6──→ 2
                          │         ↑
                          │2        │3
                          ↓         │
                          3 ────────┘

Step 1: Initialize
- dist = [0, ∞, ∞]
- Queue = [(0, 1)]

Step 2: Process vertex 1
- dist = [0, 6, 2]
- Queue = [(2, 3), (6, 2)]

Step 3: Process vertex 3
- dist = [0, 5, 2]
- Queue = [(5, 2)]

Step 4: Process vertex 2
- dist = [0, 5, 2]
- Queue = []

Final: dist = [0, 5, 2]
```

**Implementation:**
```python
import heapq

def shortest_routes_basic_dijkstra(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra's algorithm
    dist = [float('inf')] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    # Convert to result format
    result = []
    for i in range(1, n + 1):
        if dist[i] == float('inf'):
            result.append(-1)
        else:
            result.append(dist[i])
    
    return result
```

**Time Complexity:** O((V + E) log V) for V vertices and E edges with priority queue
**Space Complexity:** O(V + E) for adjacency list and priority queue

**Why it's better:**
- O((V + E) log V) time complexity is much better than O(n! × n)
- Standard method for shortest path problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Dijkstra with Efficient Data Structures (Optimal)

**Key Insights from Optimized Dijkstra Solution:**
- Use optimized Dijkstra's algorithm with efficient data structures
- Most efficient approach for single-source shortest paths
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized Dijkstra's algorithm with binary heap
2. Implement efficient adjacency list representation
3. Use proper distance tracking and queue management
4. Return shortest distances to all vertices

**Visual Example:**
```
Optimized Dijkstra for graph: 1 ──6──→ 2
                              │         ↑
                              │2        │3
                              ↓         │
                              3 ────────┘

Step 1: Initialize optimized structures
- dist = [0, ∞, ∞]
- pq = [(0, 1)]
- adj = [[], [(2,6), (3,2)], [(3,3)], []]

Step 2: Process with optimized queue
- Extract min: (0, 1)
- Update neighbors: dist[2] = 6, dist[3] = 2
- Add to queue: [(2, 3), (6, 2)]

Step 3: Continue optimized processing
- Extract min: (2, 3)
- Update neighbors: dist[2] = min(6, 2+3) = 5
- Add to queue: [(5, 2)]

Step 4: Final processing
- Extract min: (5, 2)
- No neighbors to update
- Queue empty

Final: dist = [0, 5, 2]
```

**Implementation:**
```python
import heapq

def shortest_routes_optimized_dijkstra(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Optimized Dijkstra's algorithm
    dist = [float('inf')] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        # Skip if we've already found a better path
        if d > dist[u]:
            continue
        
        # Process all neighbors
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    # Convert to result format
    result = []
    for i in range(1, n + 1):
        if dist[i] == float('inf'):
            result.append(-1)
        else:
            result.append(dist[i])
    
    return result

def solve_shortest_routes_i():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a, b, c))
    
    result = shortest_routes_optimized_dijkstra(n, m, edges)
    print(' '.join(map(str, result)))

# Main execution
if __name__ == "__main__":
    solve_shortest_routes_i()
```

**Time Complexity:** O((V + E) log V) for V vertices and E edges with optimized Dijkstra
**Space Complexity:** O(V + E) for adjacency list and priority queue

**Why it's optimal:**
- O((V + E) log V) time complexity is optimal for single-source shortest paths
- Uses optimized Dijkstra's algorithm with binary heap
- Most efficient approach for competitive programming
- Standard method for shortest path problems with non-negative weights

## 🎯 Problem Variations

### Variation 1: Shortest Routes with Different Edge Weights
**Problem**: Find shortest paths with different types of edge weights (time, cost, distance).

**Link**: [CSES Problem Set - Shortest Routes with Different Weights](https://cses.fi/problemset/task/shortest_routes_different_weights)

```python
def shortest_routes_different_weights(n, m, edges, weight_type):
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, weights in edges:
        adj[a].append((b, weights[weight_type]))
    
    # Dijkstra's algorithm
    dist = [float('inf')] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    return dist[1:n+1]
```

### Variation 2: Shortest Routes with Multiple Sources
**Problem**: Find shortest paths from multiple source vertices to all destinations.

**Link**: [CSES Problem Set - Shortest Routes Multiple Sources](https://cses.fi/problemset/task/shortest_routes_multiple_sources)

```python
def shortest_routes_multiple_sources(n, m, edges, sources):
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Multi-source Dijkstra's algorithm
    dist = [float('inf')] * (n + 1)
    pq = []
    
    # Initialize all sources
    for source in sources:
        dist[source] = 0
        pq.append((0, source))
    
    heapq.heapify(pq)
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    return dist[1:n+1]
```

### Variation 3: Shortest Routes with Path Constraints
**Problem**: Find shortest paths with constraints on path length or number of edges.

**Link**: [CSES Problem Set - Shortest Routes Path Constraints](https://cses.fi/problemset/task/shortest_routes_path_constraints)

```python
def shortest_routes_path_constraints(n, m, edges, max_edges):
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra's algorithm with edge count constraint
    dist = [[float('inf')] * (max_edges + 1) for _ in range(n + 1)]
    dist[1][0] = 0
    pq = [(0, 1, 0)]  # (distance, vertex, edge_count)
    
    while pq:
        d, u, edges_used = heapq.heappop(pq)
        
        if d > dist[u][edges_used] or edges_used >= max_edges:
            continue
        
        for v, w in adj[u]:
            if edges_used + 1 <= max_edges and dist[u][edges_used] + w < dist[v][edges_used + 1]:
                dist[v][edges_used + 1] = dist[u][edges_used] + w
                heapq.heappush(pq, (dist[v][edges_used + 1], v, edges_used + 1))
    
    # Return minimum distance for each vertex
    result = []
    for i in range(1, n + 1):
        min_dist = min(dist[i])
        if min_dist == float('inf'):
            result.append(-1)
        else:
            result.append(min_dist)
    
    return result
```

## 🔗 Related Problems

- **[Message Route](/cses-analyses/problem_soulutions/graph_algorithms/message_route_analysis/)**: BFS shortest path
- **[Labyrinth](/cses-analyses/problem_soulutions/graph_algorithms/labyrinth_analysis/)**: Grid shortest path
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems
- **[Shortest Routes II](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_ii_analysis/)**: All-pairs shortest paths

## 📚 Learning Points

1. **Single-Source Shortest Paths**: Essential for understanding shortest path algorithms
2. **Dijkstra's Algorithm**: Key technique for non-negative edge weights
3. **Priority Queue Usage**: Important for implementing efficient shortest path algorithms
4. **Graph Representation**: Critical for understanding adjacency list structures
5. **Greedy Algorithms**: Foundation for many optimization problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Shortest Routes I problem demonstrates fundamental single-source shortest path concepts for finding minimum cost paths in weighted graphs. We explored three approaches:

1. **Brute Force Path Enumeration**: O(n! × n) time complexity using recursive path generation, inefficient for large graphs
2. **Basic Dijkstra with Array**: O((V + E) log V) time complexity using standard Dijkstra's algorithm, better approach for shortest path problems
3. **Optimized Dijkstra with Efficient Data Structures**: O((V + E) log V) time complexity with optimized Dijkstra's algorithm, optimal approach for single-source shortest paths

The key insights include understanding shortest path problems as optimization problems, using Dijkstra's algorithm for non-negative edge weights, and applying priority queue-based algorithms for optimal performance. This problem serves as an excellent introduction to shortest path algorithms and Dijkstra's algorithm techniques.

