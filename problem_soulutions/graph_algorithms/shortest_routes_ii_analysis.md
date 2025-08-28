---
layout: simple
title: "Shortest Routes II"permalink: /problem_soulutions/graph_algorithms/shortest_routes_ii_analysis
---


# Shortest Routes II

## Problem Statement
There are n cities and m flight connections. Your task is to find the shortest route between any two cities.

### Input
The first input line has two integers n and m: the number of cities and flight connections. The cities are numbered 1,2,…,n.
Then, there are m lines describing the flight connections. Each line has three integers a, b, and c: there is a flight from city a to city b with cost c.

### Output
Print n lines with n integers each: the shortest route lengths between all pairs of cities. If there is no route, print -1.

### Constraints
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ n^2
- 1 ≤ a,b ≤ n
- 1 ≤ c ≤ 10^9

### Example
```
Input:
4 3
1 2 1
2 3 1
3 4 1

Output:
0 1 2 3
-1 0 1 2
-1 -1 0 1
-1 -1 -1 0
```

## Solution Progression

### Approach 1: Floyd-Warshall Algorithm - O(n³)
**Description**: Use Floyd-Warshall algorithm to find shortest paths between all pairs of vertices.

```python
def shortest_routes_floyd_warshall(n, m, flights):
    # Initialize distance matrix
    distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        distances[i][i] = 0
    
    # Add direct edges
    for a, b, c in flights:
        distances[a][b] = min(distances[a][b], c)
    
    def floyd_warshall():
        # Floyd-Warshall algorithm
        for k in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if (distances[i][k] != float('inf') and 
                        distances[k][j] != float('inf')):
                        distances[i][j] = min(distances[i][j], 
                                            distances[i][k] + distances[k][j])
    
    floyd_warshall()
    
    # Convert to output format
    result = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if distances[i][j] == float('inf'):
                row.append(-1)
            else:
                row.append(distances[i][j])
        result.append(row)
    
    return result
```

**Why this is efficient**: Floyd-Warshall is optimal for all-pairs shortest path problems in dense graphs.

### Improvement 1: Optimized Floyd-Warshall with Early Termination - O(n³)
**Description**: Use optimized Floyd-Warshall with early termination and better memory access patterns.

```python
def shortest_routes_optimized_floyd_warshall(n, m, flights):
    # Initialize distance matrix
    distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        distances[i][i] = 0
    
    # Add direct edges
    for a, b, c in flights:
        distances[a][b] = min(distances[a][b], c)
    
    def floyd_warshall_optimized():
        # Optimized Floyd-Warshall with early termination
        for k in range(1, n + 1):
            for i in range(1, n + 1):
                if distances[i][k] == float('inf'):
                    continue
                for j in range(1, n + 1):
                    if distances[k][j] != float('inf'):
                        new_dist = distances[i][k] + distances[k][j]
                        if new_dist < distances[i][j]:
                            distances[i][j] = new_dist
    
    floyd_warshall_optimized()
    
    # Convert to output format
    result = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if distances[i][j] == float('inf'):
                row.append(-1)
            else:
                row.append(distances[i][j])
        result.append(row)
    
    return result
```

**Why this improvement works**: Early termination when intermediate paths don't exist can improve performance.

### Improvement 2: Johnson's Algorithm - O(n² * log(n) + n*m)
**Description**: Use Johnson's algorithm which combines Bellman-Ford and Dijkstra's for better performance on sparse graphs.

```python
import heapq

def shortest_routes_johnson(n, m, flights):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def johnson():
        # Step 1: Add a new vertex connected to all vertices with weight 0
        for i in range(1, n + 1):
            graph[0].append((i, 0))
        
        # Step 2: Run Bellman-Ford from the new vertex to get h values
        h = [float('inf')] * (n + 1)
        h[0] = 0
        
        for _ in range(n):
            for u in range(n + 1):
                for v, w in graph[u]:
                    if h[u] != float('inf'):
                        h[v] = min(h[v], h[u] + w)
        
        # Step 3: Remove the added vertex and reweight edges
        graph[0].clear()
        
        # Step 4: Run Dijkstra's from each vertex
        distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        
        for start in range(1, n + 1):
            distances[start][start] = 0
            pq = [(0, start)]
            
            while pq:
                dist, node = heapq.heappop(pq)
                if dist > distances[start][node]:
                    continue
                
                for neighbor, weight in graph[node]:
                    # Reweighted edge weight
                    new_weight = weight + h[node] - h[neighbor]
                    new_dist = dist + new_weight
                    
                    if new_dist < distances[start][neighbor]:
                        distances[start][neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))
            
            # Restore original distances
            for end in range(1, n + 1):
                if distances[start][end] != float('inf'):
                    distances[start][end] = distances[start][end] - h[start] + h[end]
        
        return distances
    
    distances = johnson()
    
    # Convert to output format
    result = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if distances[i][j] == float('inf'):
                row.append(-1)
            else:
                row.append(distances[i][j])
        result.append(row)
    
    return result
```

**Why this improvement works**: Johnson's algorithm is more efficient for sparse graphs compared to Floyd-Warshall.

### Alternative: Matrix Multiplication Approach - O(n³ * log(n))
**Description**: Use matrix multiplication approach for all-pairs shortest paths.

```python
def shortest_routes_matrix_multiplication(n, m, flights):
    # Initialize distance matrix
    distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        distances[i][i] = 0
    
    # Add direct edges
    for a, b, c in flights:
        distances[a][b] = min(distances[a][b], c)
    
    def matrix_multiply():
        # Matrix multiplication approach
        for _ in range(n - 1):
            new_distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    new_distances[i][j] = distances[i][j]
                    for k in range(1, n + 1):
                        if (distances[i][k] != float('inf') and 
                            distances[k][j] != float('inf')):
                            new_distances[i][j] = min(new_distances[i][j], 
                                                    distances[i][k] + distances[k][j])
            distances = new_distances
    
    matrix_multiply()
    
    # Convert to output format
    result = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if distances[i][j] == float('inf'):
                row.append(-1)
            else:
                row.append(distances[i][j])
        result.append(row)
    
    return result
```

**Why this works**: Matrix multiplication approach can be useful for understanding the concept.

## Final Optimal Solution

```python
n, m = map(int, input().split())
flights = [tuple(map(int, input().split())) for _ in range(m)]

# Initialize distance matrix
distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]

# Set diagonal to 0
for i in range(1, n + 1):
    distances[i][i] = 0

# Add direct edges
for a, b, c in flights:
    distances[a][b] = min(distances[a][b], c)

# Floyd-Warshall algorithm
for k in range(1, n + 1):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if (distances[i][k] != float('inf') and 
                distances[k][j] != float('inf')):
                distances[i][j] = min(distances[i][j], 
                                    distances[i][k] + distances[k][j])

# Convert to output format
for i in range(1, n + 1):
    row = []
    for j in range(1, n + 1):
        if distances[i][j] == float('inf'):
            row.append(-1)
        else:
            row.append(distances[i][j])
    print(*row)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Floyd-Warshall | O(n³) | O(n²) | Optimal for dense graphs |
| Optimized Floyd-Warshall | O(n³) | O(n²) | Early termination |
| Johnson's | O(n² * log(n) + n*m) | O(n²) | Better for sparse graphs |
| Matrix Multiplication | O(n³ * log(n)) | O(n²) | Educational approach |

## Key Insights for Other Problems

### 1. **All-Pairs Shortest Path**
**Principle**: Use appropriate algorithm based on graph density and requirements.
**Applicable to**:
- All-pairs shortest path problems
- Graph algorithms
- Network analysis
- Algorithm design

**Example Problems**:
- All-pairs shortest path problems
- Graph algorithms
- Network analysis
- Algorithm design

### 2. **Dynamic Programming in Graphs**
**Principle**: Use dynamic programming to build shortest paths incrementally.
**Applicable to**:
- Floyd-Warshall algorithm
- Graph algorithms
- Dynamic programming
- Algorithm optimization

**Example Problems**:
- Floyd-Warshall algorithm
- Graph algorithms
- Dynamic programming
- Algorithm optimization

### 3. **Matrix Operations**
**Principle**: Use matrix operations to represent and compute graph properties.
**Applicable to**:
- Graph algorithms
- Linear algebra
- Algorithm design
- Mathematical modeling

**Example Problems**:
- Graph algorithms
- Linear algebra
- Algorithm design
- Mathematical modeling

### 4. **Algorithm Selection**
**Principle**: Choose the most appropriate algorithm based on problem constraints and graph characteristics.
**Applicable to**:
- Algorithm design
- Problem solving
- Performance optimization
- System design

**Example Problems**:
- Algorithm design
- Problem solving
- Performance optimization
- System design

## Notable Techniques

### 1. **Floyd-Warshall Pattern**
```python
def floyd_warshall(graph, n):
    distances = [[float('inf')] * n for _ in range(n)]
    
    # Initialize
    for i in range(n):
        distances[i][i] = 0
    for u, v, w in graph:
        distances[u][v] = w
    
    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if (distances[i][k] != float('inf') and 
                    distances[k][j] != float('inf')):
                    distances[i][j] = min(distances[i][j], 
                                        distances[i][k] + distances[k][j])
    
    return distances
```

### 2. **Johnson's Pattern**
```python
def johnson(graph, n):
    # Add source vertex
    for i in range(n):
        graph.append((n, i, 0))
    
    # Bellman-Ford for h values
    h = [float('inf')] * (n + 1)
    h[n] = 0
    for _ in range(n):
        for u, v, w in graph:
            if h[u] != float('inf'):
                h[v] = min(h[v], h[u] + w)
    
    # Remove source and reweight
    graph = [(u, v, w + h[u] - h[v]) for u, v, w in graph if u != n]
    
    # Dijkstra's from each vertex
    distances = [[float('inf')] * n for _ in range(n)]
    for start in range(n):
        distances[start] = dijkstra(graph, start, n)
        for end in range(n):
            if distances[start][end] != float('inf'):
                distances[start][end] = distances[start][end] - h[start] + h[end]
    
    return distances
```

### 3. **Matrix Multiplication Pattern**
```python
def matrix_multiply_shortest_paths(distances, n):
    for _ in range(n - 1):
        new_distances = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_distances[i][j] = distances[i][j]
                for k in range(n):
                    if (distances[i][k] != float('inf') and 
                        distances[k][j] != float('inf')):
                        new_distances[i][j] = min(new_distances[i][j], 
                                                distances[i][k] + distances[k][j])
        distances = new_distances
    return distances
```

## Edge Cases to Remember

1. **No path exists**: Return -1 for unreachable pairs
2. **Negative cycles**: Handle with appropriate algorithm
3. **Self-loops**: Set diagonal to 0
4. **Multiple edges**: Consider minimum weight
5. **Large distances**: Use appropriate data types

## Problem-Solving Framework

1. **Identify all-pairs nature**: This is an all-pairs shortest path problem
2. **Choose algorithm**: Use Floyd-Warshall for dense graphs
3. **Handle edge cases**: Check for unreachable pairs
4. **Optimize performance**: Use early termination
5. **Format output**: Convert distances to required format

---

*This analysis shows how to efficiently solve all-pairs shortest path problems using various graph algorithms.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Shortest Routes II with Costs**
**Variation**: Each route has additional costs beyond distance (tolls, fuel, etc.).
**Approach**: Use Floyd-Warshall with multi-dimensional cost tracking.
```python
def cost_based_shortest_routes_ii(n, m, flights, costs):
    # costs[(a, b)] = additional cost for flight from a to b
    
    # Initialize distance and cost matrices
    distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    total_costs = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        distances[i][i] = 0
        total_costs[i][i] = 0
    
    # Add direct edges with costs
    for a, b, c in flights:
        additional_cost = costs.get((a, b), 0)
        total_cost = c + additional_cost
        if total_cost < total_costs[a][b]:
            distances[a][b] = c
            total_costs[a][b] = total_cost
    
    # Floyd-Warshall with cost tracking
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if (total_costs[i][k] != float('inf') and 
                    total_costs[k][j] != float('inf')):
                    new_total_cost = total_costs[i][k] + total_costs[k][j]
                    if new_total_cost < total_costs[i][j]:
                        total_costs[i][j] = new_total_cost
                        distances[i][j] = distances[i][k] + distances[k][j]
    
    return distances, total_costs
```

#### 2. **Shortest Routes II with Constraints**
**Variation**: Limited fuel, time constraints, or restricted routes.
**Approach**: Use constrained Floyd-Warshall with state tracking.
```python
def constrained_shortest_routes_ii(n, m, flights, max_fuel, restricted_routes):
    # max_fuel = maximum fuel capacity
    # restricted_routes = set of routes that cannot be used
    
    # Initialize distance matrix
    distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        distances[i][i] = 0
    
    # Add direct edges (excluding restricted routes)
    for a, b, c in flights:
        if (a, b) not in restricted_routes and c <= max_fuel:
            distances[a][b] = min(distances[a][b], c)
    
    # Constrained Floyd-Warshall
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if (distances[i][k] != float('inf') and 
                    distances[k][j] != float('inf')):
                    total_fuel = distances[i][k] + distances[k][j]
                    if total_fuel <= max_fuel:
                        distances[i][j] = min(distances[i][j], total_fuel)
    
    return distances
```

#### 3. **Shortest Routes II with Probabilities**
**Variation**: Each route has a probability of being available or having delays.
**Approach**: Use Monte Carlo simulation or expected value calculation.
```python
import random

def probabilistic_shortest_routes_ii(n, m, flights, probabilities):
    # probabilities[(a, b)] = probability flight from a to b is available
    
    def monte_carlo_simulation(trials=1000):
        successful_routes = [[0] * (n + 1) for _ in range(n + 1)]
        
        for _ in range(trials):
            # Simulate available flights
            available_flights = []
            for a, b, c in flights:
                if random.random() < probabilities.get((a, b), 1.0):
                    available_flights.append((a, b, c))
            
            # Calculate shortest paths with available flights
            distances = calculate_all_pairs_shortest_paths(n, available_flights)
            
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if distances[i][j] != float('inf'):
                        successful_routes[i][j] += 1
        
        # Calculate probabilities
        result = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                result[i][j] = successful_routes[i][j] / trials
        
        return result
    
    def calculate_all_pairs_shortest_paths(n, flights):
        distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            distances[i][i] = 0
        
        for a, b, c in flights:
            distances[a][b] = min(distances[a][b], c)
        
        # Floyd-Warshall
        for k in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if (distances[i][k] != float('inf') and 
                        distances[k][j] != float('inf')):
                        distances[i][j] = min(distances[i][j], 
                                            distances[i][k] + distances[k][j])
        
        return distances
    
    return monte_carlo_simulation()
```

#### 4. **Shortest Routes II with Multiple Criteria**
**Variation**: Optimize for multiple objectives (distance, time, cost, comfort).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_shortest_routes_ii(n, m, flights, criteria_weights):
    # criteria_weights = {'distance': 0.4, 'time': 0.3, 'cost': 0.2, 'comfort': 0.1}
    # flights = [(a, b, distance, time, cost, comfort), ...]
    
    # Initialize matrices for each criterion
    distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    times = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    costs = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    comforts = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    scores = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        distances[i][i] = times[i][i] = costs[i][i] = comforts[i][i] = scores[i][i] = 0
    
    # Add direct edges
    for a, b, dist, time, cost, comfort in flights:
        distances[a][b] = dist
        times[a][b] = time
        costs[a][b] = cost
        comforts[a][b] = comfort
        scores[a][b] = (criteria_weights['distance'] * dist + 
                       criteria_weights['time'] * time + 
                       criteria_weights['cost'] * cost + 
                       criteria_weights['comfort'] * comfort)
    
    # Multi-criteria Floyd-Warshall
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if (scores[i][k] != float('inf') and 
                    scores[k][j] != float('inf')):
                    new_score = scores[i][k] + scores[k][j]
                    if new_score < scores[i][j]:
                        scores[i][j] = new_score
                        distances[i][j] = distances[i][k] + distances[k][j]
                        times[i][j] = times[i][k] + times[k][j]
                        costs[i][j] = costs[i][k] + costs[k][j]
                        comforts[i][j] = comforts[i][k] + comforts[k][j]
    
    return distances, times, costs, comforts, scores
```

#### 5. **Shortest Routes II with Dynamic Updates**
**Variation**: Routes can be added, removed, or modified dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicShortestRoutesII:
    def __init__(self, n):
        self.n = n
        self.distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            self.distances[i][i] = 0
    
    def add_flight(self, a, b, c):
        if c < self.distances[a][b]:
            self.distances[a][b] = c
            self.update_all_pairs()
    
    def remove_flight(self, a, b):
        # Mark as unavailable and recalculate
        self.distances[a][b] = float('inf')
        self.update_all_pairs()
    
    def update_flight_weight(self, a, b, new_weight):
        self.distances[a][b] = new_weight
        self.update_all_pairs()
    
    def update_all_pairs(self):
        # Recalculate all pairs shortest paths
        for k in range(1, self.n + 1):
            for i in range(1, self.n + 1):
                for j in range(1, self.n + 1):
                    if (self.distances[i][k] != float('inf') and 
                        self.distances[k][j] != float('inf')):
                        self.distances[i][j] = min(self.distances[i][j], 
                                                 self.distances[i][k] + self.distances[k][j])
    
    def get_distances(self):
        return self.distances
```

### Related Problems & Concepts

#### 1. **All-Pairs Shortest Path Problems**
- **Floyd-Warshall**: O(n³) for dense graphs
- **Johnson's Algorithm**: O(n² log n + nm) for sparse graphs
- **Matrix Multiplication**: O(n³ log n) educational approach
- **Transitive Closure**: Boolean reachability

#### 2. **Graph Algorithms**
- **Connectivity**: Strongly connected components
- **Flow Networks**: Maximum flow, minimum cut
- **Matching**: Bipartite matching, stable marriage
- **Coloring**: Graph coloring, bipartite graphs

#### 3. **Dynamic Programming**
- **State Optimization**: Multi-dimensional states
- **Memoization**: Caching recursive solutions
- **Optimal Substructure**: Breaking down problems
- **State Compression**: Bit manipulation for states

#### 4. **Network Problems**
- **Routing**: Internet routing, GPS navigation
- **Flow**: Traffic flow, data flow
- **Connectivity**: Network reliability, fault tolerance
- **Scheduling**: Task scheduling, resource allocation

#### 5. **Algorithm Design**
- **Data Structures**: Matrices, adjacency lists
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
- **Graph Problems**: All pairs shortest path, connectivity
- **Path Problems**: K-shortest paths, disjoint paths
- **Network Problems**: Flow, routing, connectivity
- **Optimization Problems**: Multi-objective, constrained 