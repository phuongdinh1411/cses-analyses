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

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Shortest Routes I with Costs**
**Variation**: Each route has additional costs (tolls, fuel, etc.) beyond distance.
**Approach**: Use Dijkstra's algorithm with multi-dimensional cost tracking.
```python
def cost_based_shortest_routes_i(n, m, edges, costs):
    # costs[(a, b)] = additional cost for route from a to b
    
    # Build adjacency list with costs
    graph = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        additional_cost = costs.get((a, b), 0)
        graph[a].append((b, w, additional_cost))
    
    def dijkstra_with_costs():
        # (total_cost, distance, node)
        distances = [float('inf')] * (n + 1)
        total_costs = [float('inf')] * (n + 1)
        distances[1] = 0
        total_costs[1] = 0
        
        pq = [(0, 0, 1)]  # (total_cost, distance, node)
        
        while pq:
            total_cost, dist, node = heapq.heappop(pq)
            
            if total_cost > total_costs[node]:
                continue
            
            for neighbor, weight, cost in graph[node]:
                new_dist = dist + weight
                new_total_cost = total_cost + weight + cost
                
                if new_total_cost < total_costs[neighbor]:
                    distances[neighbor] = new_dist
                    total_costs[neighbor] = new_total_cost
                    heapq.heappush(pq, (new_total_cost, new_dist, neighbor))
        
        return distances, total_costs
    
    distances, costs = dijkstra_with_costs()
    return distances[1:], costs[1:]
```

#### 2. **Shortest Routes I with Constraints**
**Variation**: Limited fuel, time constraints, or restricted routes.
**Approach**: Use BFS with state tracking for constraint satisfaction.
```python
def constrained_shortest_routes_i(n, m, edges, max_fuel, restricted_routes):
    # max_fuel = maximum fuel capacity
    # restricted_routes = set of routes that cannot be used
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        if (a, b) not in restricted_routes and (b, a) not in restricted_routes:
            graph[a].append((b, w))
            graph[b].append((a, w))
    
    def bfs_with_constraints():
        # (node, fuel, distance)
        queue = deque([(1, 0, 0)])
        visited = set()
        distances = [float('inf')] * (n + 1)
        
        while queue:
            node, fuel, dist = queue.popleft()
            
            if fuel > max_fuel:
                continue
            
            if dist < distances[node]:
                distances[node] = dist
            
            state = (node, fuel)
            if state in visited:
                continue
            visited.add(state)
            
            for neighbor, weight in graph[node]:
                new_fuel = fuel + weight
                if new_fuel <= max_fuel:
                    queue.append((neighbor, new_fuel, dist + weight))
        
        return distances
    
    distances = bfs_with_constraints()
    return [d if d != float('inf') else -1 for d in distances[1:]]
```

#### 3. **Shortest Routes I with Probabilities**
**Variation**: Each route has a probability of being available or having delays.
**Approach**: Use Monte Carlo simulation or expected value calculation.
```python
def probabilistic_shortest_routes_i(n, m, edges, probabilities):
    # probabilities[(a, b)] = probability route from a to b is available
    
    def monte_carlo_simulation(trials=1000):
        successful_routes = [0] * (n + 1)
        
        for _ in range(trials):
            # Simulate available routes
            available_edges = []
            for a, b, w in edges:
                if random.random() < probabilities.get((a, b), 1.0):
                    available_edges.append((a, b, w))
            
            # Calculate shortest paths with available routes
            distances = calculate_shortest_paths(n, available_edges)
            
            for i in range(1, n + 1):
                if distances[i] != float('inf'):
                    successful_routes[i] += 1
        
        return [successful_routes[i] / trials for i in range(1, n + 1)]
    
    def calculate_shortest_paths(n, edges):
        graph = [[] for _ in range(n + 1)]
        for a, b, w in edges:
            graph[a].append((b, w))
        
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
    
    return monte_carlo_simulation()
```

#### 4. **Shortest Routes I with Multiple Criteria**
**Variation**: Optimize for multiple objectives (distance, time, cost, comfort).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_shortest_routes_i(n, m, edges, criteria_weights):
    # criteria_weights = {'distance': 0.4, 'time': 0.3, 'cost': 0.2, 'comfort': 0.1}
    # edges = [(a, b, distance, time, cost, comfort), ...]
    
    # Build adjacency list with multiple criteria
    graph = [[] for _ in range(n + 1)]
    for a, b, dist, time, cost, comfort in edges:
        graph[a].append((b, dist, time, cost, comfort))
    
    def multi_objective_dijkstra():
        # Calculate weighted scores
        def calculate_score(dist, time, cost, comfort):
            return (criteria_weights['distance'] * dist + 
                   criteria_weights['time'] * time + 
                   criteria_weights['cost'] * cost + 
                   criteria_weights['comfort'] * comfort)
        
        scores = [float('inf')] * (n + 1)
        scores[1] = 0
        distances = [float('inf')] * (n + 1)
        distances[1] = 0
        
        pq = [(0, 0, 1)]  # (score, distance, node)
        
        while pq:
            score, dist, node = heapq.heappop(pq)
            
            if score > scores[node]:
                continue
            
            for neighbor, d, t, c, comf in graph[node]:
                new_dist = dist + d
                new_score = calculate_score(d, t, c, comf)
                
                if new_score < scores[neighbor]:
                    scores[neighbor] = new_score
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_score, new_dist, neighbor))
        
        return distances, scores
    
    distances, scores = multi_objective_dijkstra()
    return distances[1:], scores[1:]
```

#### 5. **Shortest Routes I with Dynamic Updates**
**Variation**: Routes can be added, removed, or modified dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicShortestRoutes:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n + 1)]
        self.distances = [float('inf')] * (n + 1)
        self.distances[1] = 0
    
    def add_edge(self, a, b, weight):
        self.graph[a].append((b, weight))
        self.update_distances()
    
    def remove_edge(self, a, b):
        self.graph[a] = [(neighbor, w) for neighbor, w in self.graph[a] if neighbor != b]
        self.update_distances()
    
    def update_edge_weight(self, a, b, new_weight):
        for i, (neighbor, weight) in enumerate(self.graph[a]):
            if neighbor == b:
                self.graph[a][i] = (b, new_weight)
                break
        self.update_distances()
    
    def update_distances(self):
        # Recalculate shortest paths
        self.distances = [float('inf')] * (self.n + 1)
        self.distances[1] = 0
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
    
    def get_distances(self):
        return [d if d != float('inf') else -1 for d in self.distances[1:]]
```

### Related Problems & Concepts

#### 1. **Shortest Path Problems**
- **Single Source**: Dijkstra's, Bellman-Ford, SPFA
- **All Pairs**: Floyd-Warshall, Johnson's algorithm
- **K-Shortest Paths**: Yen's algorithm, Eppstein's algorithm
- **Disjoint Paths**: Menger's theorem, max flow

#### 2. **Graph Algorithms**
- **Connectivity**: Strongly connected components
- **Flow Networks**: Maximum flow, minimum cut
- **Matching**: Bipartite matching, stable marriage
- **Coloring**: Graph coloring, bipartite graphs

#### 3. **Optimization Problems**
- **Linear Programming**: Network flow, assignment
- **Dynamic Programming**: State optimization
- **Greedy Algorithms**: Local optimal choices
- **Heuristic Search**: A*, genetic algorithms

#### 4. **Network Problems**
- **Routing**: Internet routing, GPS navigation
- **Flow**: Traffic flow, data flow
- **Connectivity**: Network reliability, fault tolerance
- **Scheduling**: Task scheduling, resource allocation

#### 5. **Algorithm Design**
- **Data Structures**: Priority queues, heaps
- **Complexity Analysis**: Time and space complexity
- **Algorithm Selection**: Choosing appropriate algorithms
- **Optimization**: Performance tuning, efficiency

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large graphs
- **Edge Cases**: Robust algorithm implementation

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
- **Path Counting**: Number of shortest paths
- **Permutations**: Order of visits
- **Combinations**: Choice of routes
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
- **Euler's Totient**: Counting coprime paths

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Graph and shortest path problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Graph Problems**: Shortest path, connectivity
- **Path Problems**: All pairs, k-shortest paths
- **Network Problems**: Flow, routing, connectivity
- **Optimization Problems**: Multi-objective, constrained 