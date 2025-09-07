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

## 📋 Problem Description

There are n cities and m flight connections. Find the shortest route from city 1 to all other cities.

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

### 📊 Visual Example

**Input Graph:**
```
Cities: 1, 2, 3
Flights: (1→2, cost=6), (1→3, cost=2), (3→2, cost=3), (1→3, cost=4)

    1 ──6──→ 2
    │         ↑
    │2        │3
    ↓         │
    3 ────────┘
```

**Dijkstra's Algorithm Execution:**
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

**Shortest Path Visualization:**
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

**Dijkstra's Algorithm Flowchart:**
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

**Priority Queue Operations:**
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

**Distance Updates:**
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

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find shortest paths from source city 1 to all other cities
- **Key Insight**: Use Dijkstra's algorithm for non-negative edge weights
- **Challenge**: Handle large graphs efficiently with priority queue

### Step 2: Brute Force Approach
**Try all possible paths and find minimum:**

```python
def shortest_routes_naive(n, m, flights):
    from itertools import permutations
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def find_all_paths(start, end, visited, path, cost):
        if start == end:
            return [path + [end]]
        
        paths = []
        for neighbor, weight in graph[start]:
            if neighbor not in visited:
                new_paths = find_all_paths(neighbor, end, visited | {start}, path + [start], cost + weight)
                paths.extend(new_paths)
        
        return paths
    
    # Find shortest path to each city
    distances = [0]  # Distance to city 1
    for target in range(2, n + 1):
        all_paths = find_all_paths(1, target, set(), [], 0)
        if all_paths:
            min_cost = min(sum(graph[path[i]][path[i+1]] for i in range(len(path)-1)) 
                         for path in all_paths)
            distances.append(min_cost)
        else:
            distances.append(-1)
    
    return distances
```

**Complexity**: O(n!) - extremely slow for large graphs

### Step 3: Optimization
**Use Dijkstra's algorithm with priority queue:**

```python
def shortest_routes_dijkstra(n, m, flights):
    import heapq
    
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

**Key Insight**: Use priority queue to always process closest unvisited node

### Step 4: Complete Solution

```python
def solve_shortest_routes_i():
    n, m = map(int, input().split())
    flights = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        flights.append((a, b, c))
    
    result = find_shortest_routes(n, m, flights)
    print(*result)

def find_shortest_routes(n, m, flights):
    import heapq
    
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

if __name__ == "__main__":
    solve_shortest_routes_i()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((3, 4, [(1, 2, 6), (1, 3, 2), (3, 2, 3), (1, 3, 4)]), [0, 5, 2]),
        ((4, 3, [(1, 2, 1), (2, 3, 2), (3, 4, 3)]), [0, 1, 3, 6]),
        ((2, 1, [(1, 2, 5)]), [0, 5]),
        ((3, 2, [(1, 2, 1), (2, 3, 1)]), [0, 1, 2]),
        ((3, 1, [(2, 3, 1)]), [0, -1, -1]),  # No path to cities 2, 3
    ]
    
    for (n, m, flights), expected in test_cases:
        result = find_shortest_routes(n, m, flights)
        print(f"n={n}, m={m}, flights={flights}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_shortest_routes(n, m, flights):
    import heapq
    
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def dijkstra():
        distances = [float('inf')] * (n + 1)
        distances[1] = 0
        
        pq = [(0, 1)]
        
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
    
    distances = dijkstra()
    
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O((n + m) × log(n)) - Dijkstra's algorithm with priority queue
- **Space**: O(n + m) - adjacency list and priority queue

### Why This Solution Works
- **Dijkstra's Algorithm**: Optimal for non-negative edge weights
- **Priority Queue**: Always processes closest unvisited node
- **Greedy Approach**: Local optimal choice leads to global optimum
- **Efficient Implementation**: Uses heap for O(log n) operations

## 🎨 Visual Example

### Input Example
```
3 cities, 4 flights:
Flight 1: City 1 → City 2 (cost: 6)
Flight 2: City 1 → City 3 (cost: 2)
Flight 3: City 3 → City 2 (cost: 3)
Flight 4: City 1 → City 3 (cost: 4)
```

### Graph Visualization
```
Cities: 1, 2, 3
Flights with costs:

    1 ──6──→ 2
    │        ↑
    │2       │3
    ↓        │
    3 ───────┘

Adjacency List:
City 1: [(2,6), (3,2), (3,4)]
City 2: []
City 3: [(2,3)]
```

### Dijkstra's Algorithm Process
```
Initial distances: [∞, ∞, ∞]
Start from City 1: distances[1] = 0

Step 1: Process City 1 (distance = 0)
- Update neighbors:
  - City 2: min(∞, 0+6) = 6
  - City 3: min(∞, 0+2) = 2
- Distances: [0, 6, 2]
- Priority Queue: [(2,6), (3,2)]

Step 2: Process City 3 (distance = 2)
- Update neighbors:
  - City 2: min(6, 2+3) = 5
- Distances: [0, 5, 2]
- Priority Queue: [(2,5)]

Step 3: Process City 2 (distance = 5)
- No unvisited neighbors
- Distances: [0, 5, 2]
- Priority Queue: []

Final distances: [0, 5, 2]
```

### Priority Queue States
```
Initial: []
After processing City 1: [(2,6), (3,2)]
After processing City 3: [(2,5)]
After processing City 2: []

Note: (2,6) was replaced by (2,5) when shorter path found
```

### Path Reconstruction
```
Shortest path from City 1 to City 2:
- Distance: 5
- Path: 1 → 3 → 2
- Cost: 2 + 3 = 5

Shortest path from City 1 to City 3:
- Distance: 2
- Path: 1 → 3
- Cost: 2
```

### Distance Updates
```
City 1 to City 2:
- Direct path: 1 → 2 (cost: 6)
- Via City 3: 1 → 3 → 2 (cost: 2 + 3 = 5)
- Minimum: 5

City 1 to City 3:
- Direct path: 1 → 3 (cost: 2)
- Minimum: 2
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dijkstra        │ O((V+E)logV) │ O(V+E)       │ Greedy with  │
│                 │              │              │ priority queue│
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bellman-Ford    │ O(VE)        │ O(V+E)       │ Relax edges  │
│                 │              │              │ V-1 times    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Floyd-Warshall  │ O(V³)        │ O(V²)        │ All pairs    │
│                 │              │              │ shortest paths│
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Dijkstra's Algorithm**
- Greedy algorithm for shortest paths
- Important for understanding
- Works only with non-negative weights
- Essential for algorithm

### 2. **Priority Queue Usage**
- Always process closest unvisited node
- Important for understanding
- Ensures optimal path discovery
- Essential for efficiency

### 3. **Graph Representation**
- Use adjacency list for sparse graphs
- Important for understanding
- Efficient for most real-world graphs
- Essential for performance

## 🎯 Problem Variations

### Variation 1: Shortest Routes with Negative Weights
**Problem**: Find shortest paths when edges can have negative weights (Bellman-Ford algorithm).

```python
def shortest_routes_bellman_ford(n, m, flights):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def bellman_ford():
        distances = [float('inf')] * (n + 1)
        distances[1] = 0
        
        # Relax edges n-1 times
        for _ in range(n - 1):
            for u in range(1, n + 1):
                for v, weight in graph[u]:
                    if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
        
        # Check for negative cycles
        for u in range(1, n + 1):
            for v, weight in graph[u]:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    return None  # Negative cycle detected
        
        return distances
    
    distances = bellman_ford()
    
    if distances is None:
        return [-1] * n  # Negative cycle
    
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result

# Example usage
result = shortest_routes_bellman_ford(3, 3, [(1, 2, 1), (2, 3, -2), (3, 1, 1)])
print(f"Shortest routes with negative weights: {result}")
```

### Variation 2: Shortest Routes with K Stops
**Problem**: Find shortest path from city 1 to city n with at most k stops.

```python
def shortest_routes_k_stops(n, m, flights, k):
    import heapq
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def dijkstra_k_stops():
        # distances[node][stops] = shortest distance to node with stops stops
        distances = [[float('inf')] * (k + 1) for _ in range(n + 1)]
        distances[1][0] = 0
        
        # Priority queue: (distance, node, stops)
        pq = [(0, 1, 0)]
        
        while pq:
            dist, node, stops = heapq.heappop(pq)
            
            if dist > distances[node][stops]:
                continue
            
            if stops < k:
                for neighbor, weight in graph[node]:
                    new_dist = dist + weight
                    if new_dist < distances[neighbor][stops + 1]:
                        distances[neighbor][stops + 1] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor, stops + 1))
        
        return distances
    
    distances = dijkstra_k_stops()
    
    # Find minimum distance to target with any number of stops
    min_distance = min(distances[n])
    
    return min_distance if min_distance != float('inf') else -1

# Example usage
result = shortest_routes_k_stops(4, 4, [(1, 2, 1), (2, 3, 2), (3, 4, 3), (1, 4, 10)], 2)
print(f"Shortest route with at most 2 stops: {result}")
```

### Variation 3: Shortest Routes with Time Windows
**Problem**: Find shortest path considering time windows when flights are available.

```python
def shortest_routes_time_windows(n, m, flights, time_windows):
    import heapq
    
    # Build adjacency list with time windows
    graph = [[] for _ in range(n + 1)]
    for i, (a, b, c) in enumerate(flights):
        start_time, end_time = time_windows[i]
        graph[a].append((b, c, start_time, end_time))
    
    def dijkstra_time_windows():
        distances = [float('inf')] * (n + 1)
        distances[1] = 0
        
        # Priority queue: (distance, node, current_time)
        pq = [(0, 1, 0)]  # Start at time 0
        
        while pq:
            dist, node, current_time = heapq.heappop(pq)
            
            if dist > distances[node]:
                continue
            
            for neighbor, weight, start_time, end_time in graph[node]:
                # Check if flight is available at current time
                if start_time <= current_time <= end_time:
                    new_dist = dist + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor, current_time + weight))
        
        return distances
    
    distances = dijkstra_time_windows()
    
    result = []
    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(-1)
        else:
            result.append(distances[i])
    
    return result

# Example usage
flights = [(1, 2, 1), (2, 3, 2), (1, 3, 5)]
time_windows = [(0, 10), (5, 15), (0, 20)]  # (start_time, end_time)
result = shortest_routes_time_windows(3, 3, flights, time_windows)
print(f"Shortest routes with time windows: {result}")
```

### Variation 4: Shortest Routes with Multiple Criteria
**Problem**: Find shortest path considering multiple criteria like cost, time, and reliability.

```python
def shortest_routes_multi_criteria(n, m, flights, criteria):
    import heapq
    
    # Build adjacency list with multiple criteria
    graph = [[] for _ in range(n + 1)]
    for i, (a, b, c) in enumerate(flights):
        cost = c
        time = criteria['time'][i]
        reliability = criteria['reliability'][i]
        graph[a].append((b, cost, time, reliability))
    
    def dijkstra_multi_criteria():
        # distances[node] = (total_cost, total_time, total_reliability)
        distances = [(float('inf'), float('inf'), 0)] * (n + 1)
        distances[1] = (0, 0, 1.0)
        
        # Priority queue: (total_cost, total_time, node, total_reliability)
        pq = [(0, 0, 1, 1.0)]
        
        while pq:
            total_cost, total_time, node, total_reliability = heapq.heappop(pq)
            
            if (total_cost, total_time) > (distances[node][0], distances[node][1]):
                continue
            
            for neighbor, cost, time, reliability in graph[node]:
                new_cost = total_cost + cost
                new_time = total_time + time
                new_reliability = total_reliability * reliability
                
                if (new_cost < distances[neighbor][0] or 
                    (new_cost == distances[neighbor][0] and new_time < distances[neighbor][1])):
                    distances[neighbor] = (new_cost, new_time, new_reliability)
                    heapq.heappush(pq, (new_cost, new_time, neighbor, new_reliability))
        
        return distances
    
    distances = dijkstra_multi_criteria()
    
    result = []
    for i in range(1, n + 1):
        if distances[i][0] == float('inf'):
            result.append((-1, -1, 0))
        else:
            result.append((distances[i][0], distances[i][1], distances[i][2]))
    
    return result

# Example usage
flights = [(1, 2, 1), (2, 3, 2), (1, 3, 5)]
criteria = {
    'time': [1, 2, 3],
    'reliability': [0.9, 0.8, 0.7]
}
result = shortest_routes_multi_criteria(3, 3, flights, criteria)
print(f"Multi-criteria shortest routes: {result}")
```

### Variation 5: Shortest Routes with Dynamic Updates
**Problem**: Maintain shortest paths as flight connections are added/removed dynamically.

```python
class DynamicShortestRoutes:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n + 1)]
        self.distances = [float('inf')] * (n + 1)
        self.distances[1] = 0
    
    def add_flight(self, a, b, c):
        """Add flight from city a to city b with cost c"""
        self.graph[a].append((b, c))
        self.update_shortest_paths()
    
    def remove_flight(self, a, b, c):
        """Remove flight from city a to city b with cost c"""
        if (b, c) in self.graph[a]:
            self.graph[a].remove((b, c))
            self.update_shortest_paths()
            return True
        return False
    
    def update_shortest_paths(self):
        """Recalculate shortest paths using Dijkstra's algorithm"""
        import heapq
        
        # Reset distances
        self.distances = [float('inf')] * (self.n + 1)
        self.distances[1] = 0
        
        # Priority queue: (distance, node)
        pq = [(0, 1)]
        
        while pq:
            dist, node = heapq.heappop(pq)
            
            if dist > self.distances[node]:
                continue
            
            for neighbor, weight in self.graph[node]:
                new_dist = dist + weight
                if new_dist < self.distances[neighbor]:
                    self.distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
    
    def get_shortest_routes(self):
        """Get current shortest routes to all cities"""
        result = []
        for i in range(1, self.n + 1):
            if self.distances[i] == float('inf'):
                result.append(-1)
            else:
                result.append(self.distances[i])
        return result

# Example usage
sorter = DynamicShortestRoutes(3)
print(f"Initial routes: {sorter.get_shortest_routes()}")

sorter.add_flight(1, 2, 1)
print(f"After adding flight (1,2): {sorter.get_shortest_routes()}")

sorter.add_flight(2, 3, 2)
print(f"After adding flight (2,3): {sorter.get_shortest_routes()}")

sorter.add_flight(1, 3, 5)
print(f"After adding flight (1,3): {sorter.get_shortest_routes()}")
```

## 🔗 Related Problems

- **[Shortest Routes II](/cses-analyses/problem_soulutions/graph_algorithms/)**: All-pairs shortest paths
- **[Message Route](/cses-analyses/problem_soulutions/graph_algorithms/)**: Path finding problems
- **[Flight Discount](/cses-analyses/problem_soulutions/graph_algorithms/)**: Discount-based routing

## 📚 Learning Points

1. **Dijkstra's Algorithm**: Essential for single-source shortest paths with non-negative weights
2. **Priority Queue**: Important for efficient node selection in graph algorithms
3. **Graph Representation**: Key for efficient graph operations
4. **Dynamic Updates**: Important for maintaining shortest paths as graph changes
5. **Multi-Criteria Optimization**: Key for real-world routing problems

---

**This is a great introduction to shortest path algorithms and graph routing!** 🎯 