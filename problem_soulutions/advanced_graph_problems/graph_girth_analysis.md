---
layout: simple
title: "Graph Girth
permalink: /problem_soulutions/advanced_graph_problems/graph_girth_analysis/
---

# Graph Girth

## Problem Statement
Given an undirected graph with n nodes and m edges, find the length of the shortest cycle in the graph (the girth). If the graph has no cycles, output -1.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print the length of the shortest cycle in the graph, or -1 if there are no cycles.

### Constraints
- 1 ≤ n ≤ 2500
- 1 ≤ m ≤ 5000
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 6
1 2
2 3
3 4
4 5
5 1
2 4

Output:
3
```

## Solution Progression

### Approach 1: BFS from Each Node - O(n²(n + m))
**Description**: For each node, run BFS to find the shortest cycle starting from that node.

```python
def graph_girth_naive(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)"
    min_cycle = float('inf')
    
    # Try each node as starting point
    for start in range(1, n + 1):
        # BFS to find shortest cycle from start
        queue = [(start, -1, 0)]  # (node, parent, distance)
        visited = {start}
        
        while queue:
            node, parent, dist = queue.pop(0)
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor == start and dist >= 2:
                    # Found a cycle back to start
                    min_cycle = min(min_cycle, dist + 1)
                    break
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this is inefficient**: This approach has O(n²(n + m)) complexity and doesn't efficiently find the shortest cycle.

### Improvement 1: BFS with Distance Tracking - O(n(n + m))
**Description**: Use BFS with better distance tracking to find shortest cycles.

```python
def graph_girth_improved(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try each node as starting point
    for start in range(1, n + 1):
        # BFS with distance tracking
        queue = [(start, -1, 0)]  # (node, parent, distance)
        distance = {start: 0}
        
        while queue:
            node, parent, dist = queue.pop(0)
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in distance:
                    # Found a cycle
                    cycle_length = distance[node] + distance[neighbor] + 1
                    if cycle_length >= 3:  # Valid cycle
                        min_cycle = min(min_cycle, cycle_length)
                else:
                    distance[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this improvement works**: Better distance tracking allows finding cycles more efficiently.

### Approach 2: Floyd-Warshall for All-Pairs Shortest Paths - O(n³)
**Description**: Use Floyd-Warshall to find all-pairs shortest paths, then find the minimum cycle.

```python
def graph_girth_floyd_warshall(n, m, edges):
    # Initialize distance matrix
    dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    
    # Add edges
    for a, b in edges:
        dist[a][b] = 1
        dist[b][a] = 1
    
    # Floyd-Warshall
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Find minimum cycle
    min_cycle = float('inf')
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if dist[i][j] != float('inf'):
                # Check if there's a direct edge between i and j
                for a, b in edges:
                    if (a == i and b == j) or (a == j and b == i):
                        cycle_length = dist[i][j] + 1
                        min_cycle = min(min_cycle, cycle_length)
                        break
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this is inefficient**: O(n³) complexity is too slow for the given constraints.

### Approach 3: BFS with Edge Removal - O(nm)
**Description**: For each edge, remove it and find shortest path between its endpoints.

```python
def graph_girth_optimal(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # For each edge, find shortest path between its endpoints
    for a, b in edges:
        # Remove edge (a,b) temporarily
        adj[a].remove(b)
        adj[b].remove(a)
        
        # BFS to find shortest path from a to b
        queue = [(a, 0)]
        visited = {a}
        
        while queue:
            node, dist = queue.pop(0)
            
            if node == b:
                # Found path from a to b
                cycle_length = dist + 1
                min_cycle = min(min_cycle, cycle_length)
                break
            
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this improvement works**: This approach finds the shortest cycle by considering each edge and finding the shortest path between its endpoints.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_graph_girth(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # For each edge, find shortest path between its endpoints
    for a, b in edges:
        # Remove edge (a,b) temporarily
        adj[a].remove(b)
        adj[b].remove(a)
        
        # BFS to find shortest path from a to b
        queue = [(a, 0)]
        visited = {a}
        found_path = False
        
        while queue and not found_path:
            node, dist = queue.pop(0)
            
            if node == b:
                # Found path from a to b
                cycle_length = dist + 1
                min_cycle = min(min_cycle, cycle_length)
                found_path = True
                break
            
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
    
    return min_cycle if min_cycle != float('inf') else -1

result = find_graph_girth(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS from Each Node | O(n²(n + m)) | O(n) | Simple but inefficient cycle detection |
| BFS with Distance Tracking | O(n(n + m)) | O(n) | Better distance tracking |
| Floyd-Warshall | O(n³) | O(n²) | All-pairs shortest paths |
| BFS with Edge Removal | O(nm) | O(n) | Optimal approach for girth |

## Key Insights for Other Problems

### 1. **Girth Detection with Edge Removal**
**Principle**: The shortest cycle containing an edge (a,b) is the shortest path from a to b plus the edge itself.
**Applicable to**: Cycle detection problems, graph analysis problems, shortest path problems

### 2. **BFS for Unweighted Shortest Paths**
**Principle**: BFS finds the shortest path in unweighted graphs efficiently.
**Applicable to**: Unweighted graph problems, shortest path problems, connectivity problems

### 3. **Cycle Length Calculation**
**Principle**: A cycle's length is the sum of the shortest path between two nodes plus the direct edge between them.
**Applicable to**: Cycle analysis problems, graph theory problems, path problems

## Notable Techniques

### 1. **Edge Removal and Restoration**
```python
def find_cycle_with_edge_removal(adj, edge):
    a, b = edge
    # Remove edge temporarily
    adj[a].remove(b)
    adj[b].remove(a)
    
    # Find shortest path
    shortest_path = bfs_shortest_path(adj, a, b)
    
    # Restore edge
    adj[a].append(b)
    adj[b].append(a)
    
    return shortest_path + 1 if shortest_path != -1 else float('inf')
```

### 2. **BFS for Shortest Path**
```python
def bfs_shortest_path(adj, start, end):
    queue = [(start, 0)]
    visited = {start}
    
    while queue:
        node, dist = queue.pop(0)
        
        if node == end:
            return dist
        
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # No path found
```

### 3. **Minimum Cycle Detection**
```python
def find_minimum_cycle(n, edges):
    adj = build_adjacency_list(n, edges)
    min_cycle = float('inf')
    
    for edge in edges:
        cycle_length = find_cycle_with_edge_removal(adj, edge)
        min_cycle = min(min_cycle, cycle_length)
    
    return min_cycle if min_cycle != float('inf') else -1
```

### 4. **Graph Girth Algorithm**
```python
def graph_girth_algorithm(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # For each edge, find shortest path between endpoints
    for a, b in edges:
        # Remove edge temporarily
        adj[a].remove(b)
        adj[b].remove(a)
        
        # Find shortest path
        path_length = bfs_shortest_path(adj, a, b)
        if path_length != -1:
            min_cycle = min(min_cycle, path_length + 1)
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
    
    return min_cycle if min_cycle != float('inf') else -1
```

## Problem-Solving Framework

1. **Identify problem type**: This is a graph girth (shortest cycle) problem
2. **Choose approach**: Use BFS with edge removal technique
3. **Initialize data structure**: Build adjacency list representation
4. **Iterate through edges**: For each edge, temporarily remove it
5. **Find shortest path**: Use BFS to find shortest path between edge endpoints
6. **Calculate cycle length**: Add 1 to path length to include the removed edge
7. **Track minimum**: Keep track of the minimum cycle length found
8. **Return result**: Return minimum cycle length or -1 if no cycles exist

---

*This analysis shows how to efficiently find the girth (shortest cycle) of an undirected graph using BFS with edge removal technique.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Graph Girth with Costs**
**Variation**: Each edge has a cost, find minimum cost cycle.
**Approach**: Use weighted BFS with cost tracking.
```python
def cost_based_graph_girth(n, m, edges, edge_costs):
    # edge_costs[(a, b)] = cost of edge (a, b)
    
    def find_weighted_cycle_with_edge_removal(adj, edge):
        a, b = edge
        # Remove edge temporarily
        adj[a].remove(b)
        adj[b].remove(a)
        
        # Find shortest weighted path
        shortest_path_cost = dijkstra_shortest_path(adj, a, b, edge_costs)
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
        
        edge_cost = edge_costs.get((a, b), 1)
        return shortest_path_cost + edge_cost if shortest_path_cost != float('inf') else float('inf')
    
    def dijkstra_shortest_path(adj, start, end, costs):
        import heapq
        
        distances = [float('inf')] * (n + 1)
        distances[start] = 0
        pq = [(0, start)]
        
        while pq:
            dist, node = heapq.heappop(pq)
            
            if node == end:
                return dist
            
            if dist > distances[node]:
                continue
            
            for neighbor in adj[node]:
                edge_cost = costs.get((node, neighbor), 1)
                new_dist = dist + edge_cost
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return float('inf')
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle_cost = float('inf')
    
    # For each edge, find minimum cost cycle containing it
    for a, b in edges:
        cycle_cost = find_weighted_cycle_with_edge_removal(adj, (a, b))
        min_cycle_cost = min(min_cycle_cost, cycle_cost)
    
    return min_cycle_cost if min_cycle_cost != float('inf') else -1
```

#### 2. **Graph Girth with Constraints**
**Variation**: Limited path length, restricted edges, or specific cycle requirements.
**Approach**: Use constraint satisfaction with cycle detection.
```python
def constrained_graph_girth(n, m, edges, max_cycle_length, restricted_edges):
    # max_cycle_length = maximum allowed cycle length
    # restricted_edges = set of edges that cannot be used in cycles
    
    def find_constrained_cycle_with_edge_removal(adj, edge):
        a, b = edge
        if (a, b) in restricted_edges or (b, a) in restricted_edges:
            return float('inf')
        
        # Remove edge temporarily
        adj[a].remove(b)
        adj[b].remove(a)
        
        # Find shortest path with constraint
        path_length = constrained_bfs_shortest_path(adj, a, b, max_cycle_length - 1)
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
        
        return path_length + 1 if path_length != -1 else float('inf')
    
    def constrained_bfs_shortest_path(adj, start, end, max_length):
        queue = [(start, 0)]
        visited = {start}
        
        while queue:
            node, dist = queue.pop(0)
            
            if node == end:
                return dist
            
            if dist >= max_length:
                continue
            
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return -1
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # For each edge, find constrained cycle
    for a, b in edges:
        cycle_length = find_constrained_cycle_with_edge_removal(adj, (a, b))
        if cycle_length <= max_cycle_length:
            min_cycle = min(min_cycle, cycle_length)
    
    return min_cycle if min_cycle != float('inf') else -1
```

#### 3. **Graph Girth with Probabilities**
**Variation**: Each edge has a probability of being available.
**Approach**: Use Monte Carlo simulation or expected value calculation.
```python
def probabilistic_graph_girth(n, m, edges, edge_probabilities):
    # edge_probabilities[(a, b)] = probability edge (a, b) is available
    
    def monte_carlo_simulation(trials=1000):
        cycle_lengths = []
        
        for _ in range(trials):
            # Simulate available edges
            available_edges = []
            for a, b in edges:
                if random.random() < edge_probabilities.get((a, b), 0.5):
                    available_edges.append((a, b))
            
            # Find girth with available edges
            girth = find_girth_with_edges(n, available_edges)
            if girth != -1:
                cycle_lengths.append(girth)
        
        return min(cycle_lengths) if cycle_lengths else -1
    
    def find_girth_with_edges(n, available_edges):
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in available_edges:
            adj[a].append(b)
            adj[b].append(a)
        
        min_cycle = float('inf')
        
        # For each edge, find cycle
        for a, b in available_edges:
            # Remove edge temporarily
            adj[a].remove(b)
            adj[b].remove(a)
            
            # Find shortest path
            path_length = bfs_shortest_path(adj, a, b)
            if path_length != -1:
                min_cycle = min(min_cycle, path_length + 1)
            
            # Restore edge
            adj[a].append(b)
            adj[b].append(a)
        
        return min_cycle if min_cycle != float('inf') else -1
    
    def bfs_shortest_path(adj, start, end):
        queue = [(start, 0)]
        visited = {start}
        
        while queue:
            node, dist = queue.pop(0)
            
            if node == end:
                return dist
            
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return -1
    
    return monte_carlo_simulation()
```

#### 4. **Graph Girth with Multiple Criteria**
**Variation**: Optimize for multiple objectives (length, cost, reliability).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_graph_girth(n, m, edges, criteria_weights):
    # criteria_weights = {'length': 0.4, 'cost': 0.3, 'reliability': 0.3}
    # Each edge has multiple attributes
    
    def calculate_cycle_score(cycle_attributes):
        return (criteria_weights['length'] * cycle_attributes['length'] + 
                criteria_weights['cost'] * cycle_attributes['cost'] + 
                criteria_weights['reliability'] * cycle_attributes['reliability'])
    
    def find_multi_criteria_girth():
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        
        min_score = float('inf')
        best_cycle = None
        
        # For each edge, find optimal cycle
        for a, b in edges:
            # Remove edge temporarily
            adj[a].remove(b)
            adj[b].remove(a)
            
            # Find shortest path
            path_length = bfs_shortest_path(adj, a, b)
            
            # Restore edge
            adj[a].append(b)
            adj[b].append(a)
            
            if path_length != -1:
                cycle_length = path_length + 1
                
                # Calculate cycle attributes (simplified)
                cycle_attrs = {
                    'length': cycle_length,
                    'cost': cycle_length * 10,  # Assuming cost proportional to length
                    'reliability': 1.0 / cycle_length  # Shorter cycles more reliable
                }
                
                score = calculate_cycle_score(cycle_attrs)
                if score < min_score:
                    min_score = score
                    best_cycle = (a, b, cycle_length)
        
        return best_cycle, min_score
    
    def bfs_shortest_path(adj, start, end):
        queue = [(start, 0)]
        visited = {start}
        
        while queue:
            node, dist = queue.pop(0)
            
            if node == end:
                return dist
            
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return -1
    
    cycle, score = find_multi_criteria_girth()
    return cycle, score
```

#### 5. **Graph Girth with Dynamic Updates**
**Variation**: Edges can be added or removed dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicGraphGirth:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self.girth_cache = None
    
    def add_edge(self, a, b):
        self.edges.append((a, b))
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.edges.remove((a, b))
            self.invalidate_cache()
    
    def invalidate_cache(self):
        self.girth_cache = None
    
    def get_girth(self):
        if self.girth_cache is None:
            self.girth_cache = self.compute_girth()
        return self.girth_cache
    
    def compute_girth(self):
        # Build adjacency list
        adj = [[] for _ in range(self.n + 1)]
        for a, b in self.edges:
            adj[a].append(b)
            adj[b].append(a)
        
        min_cycle = float('inf')
        
        # For each edge, find cycle
        for a, b in self.edges:
            # Remove edge temporarily
            adj[a].remove(b)
            adj[b].remove(a)
            
            # Find shortest path
            path_length = self.bfs_shortest_path(adj, a, b)
            if path_length != -1:
                min_cycle = min(min_cycle, path_length + 1)
            
            # Restore edge
            adj[a].append(b)
            adj[b].append(a)
        
        return min_cycle if min_cycle != float('inf') else -1
    
    def bfs_shortest_path(self, adj, start, end):
        queue = [(start, 0)]
        visited = {start}
        
        while queue:
            node, dist = queue.pop(0)
            
            if node == end:
                return dist
            
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return -1
```

### Related Problems & Concepts

#### 1. **Cycle Detection Problems**
- **Graph Girth**: Shortest cycle in graph
- **Cycle Enumeration**: Find all cycles
- **Cycle Counting**: Count number of cycles
- **Cycle Decomposition**: Break into cycles

#### 2. **Shortest Path Problems**
- **Single Source**: Dijkstra's, Bellman-Ford
- **All Pairs**: Floyd-Warshall
- **K-Shortest Paths**: Yen's algorithm
- **Disjoint Paths**: Menger's theorem

#### 3. **Graph Algorithms**
- **Breadth-First Search**: Level-by-level exploration
- **Depth-First Search**: Recursive exploration
- **Connectivity**: Strongly connected components
- **Flow Networks**: Maximum flow, minimum cut

#### 4. **Optimization Problems**
- **Minimum Cycle**: Shortest cycle finding
- **Cycle Cover**: Covering with cycles
- **Cycle Packing**: Maximum disjoint cycles
- **Cycle Decomposition**: Breaking into cycles

#### 5. **Dynamic Graph Problems**
- **Incremental Girth**: Adding edges
- **Decremental Girth**: Removing edges
- **Fully Dynamic**: Both adding and removing
- **Online Algorithms**: Real-time updates

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large graphs
- **Edge Cases**: Robust cycle detection

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient graph traversal
- **Sliding Window**: Optimal subgraph problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Combinatorics**
- **Cycle Enumeration**: Counting cycles
- **Permutations**: Order of cycle visits
- **Combinations**: Choice of cycle edges
- **Catalan Numbers**: Valid cycle sequences

#### 2. **Probability Theory**
- **Expected Values**: Average cycle length
- **Markov Chains**: State transitions
- **Random Graphs**: Erdős-Rényi model
- **Monte Carlo**: Simulation methods

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special graph cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime cycles

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Graph and cycle problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Graph Problems**: Cycle detection, girth
- **Path Problems**: Shortest path, all pairs
- **Dynamic Problems**: Incremental, decremental
- **Optimization Problems**: Multi-objective, constrained 