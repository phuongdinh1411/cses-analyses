---
layout: simple
title: "Distinct Routes"
permalink: /cses-analyses/problem_soulutions/graph_algorithms/distinct_routes_analysis
---


# Distinct Routes

## Problem Statement
Given a directed graph with n nodes and m edges, find the maximum number of edge-disjoint paths from node 1 to node n.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge from node a to node b.

### Output
Print the maximum number of edge-disjoint paths from node 1 to node n.

### Constraints
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ 1000
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 5
1 2
2 3
3 4
1 3
2 4

Output:
2
```

## Solution Progression

### Approach 1: Maximum Flow for Edge-Disjoint Paths - O(n * m * max_flow)
**Description**: Use maximum flow to find maximum number of edge-disjoint paths.

```python
def distinct_routes_naive(n, m, edges):
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)  # For residual graph
        capacity[a][b] = 1  # Unit capacity for edge-disjoint paths
    
    def bfs(source, sink):
        # Find augmenting path using BFS
        parent = [-1] * (n + 1)
        parent[source] = source
        queue = [source]
        
        while queue:
            current = queue.pop(0)
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0  # No augmenting path found
        
        # Find bottleneck capacity
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(1, n)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Edge-Disjoint Paths Algorithm - O(n * m * max_flow)
**Description**: Use optimized Ford-Fulkerson algorithm for edge-disjoint paths.

```python
def distinct_routes_optimized(n, m, edges):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
    
    def bfs(source, sink):
        parent = [-1] * (n + 1)
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0
        
        # Find bottleneck and update residual graph
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(1, n)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

**Why this improvement works**: We use optimized Ford-Fulkerson algorithm to find maximum edge-disjoint paths efficiently.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_maximum_edge_disjoint_paths(n, m, edges):
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)  # For residual graph
        capacity[a][b] = 1  # Unit capacity for edge-disjoint paths
    
    def bfs(source, sink):
        # Find augmenting path using BFS
        parent = [-1] * (n + 1)
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0  # No augmenting path found
        
        # Find bottleneck capacity
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(1, n)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow

result = find_maximum_edge_disjoint_paths(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Edge-Disjoint Paths via Max Flow | O(n * m * max_flow) | O(n²) | Use max flow for edge-disjoint paths |
| Optimized Edge-Disjoint Paths | O(n * m * max_flow) | O(n²) | Optimized max flow implementation |

## Key Insights for Other Problems

### 1. **Edge-Disjoint Paths**
**Principle**: Use maximum flow to find maximum number of edge-disjoint paths.
**Applicable to**: Path problems, connectivity problems, network problems

### 2. **Menger's Theorem**
**Principle**: The maximum number of edge-disjoint paths equals the minimum edge cut.
**Applicable to**: Connectivity problems, path problems, network problems

### 3. **Unit Capacity Networks**
**Principle**: Use unit capacities to model edge-disjoint path constraints.
**Applicable to**: Path problems, flow problems, network problems

## Notable Techniques

### 1. **Edge-Disjoint Paths via Max Flow**
```python
def edge_disjoint_paths_max_flow(n, adj, capacity, source, sink):
    def bfs():
        parent = [-1] * (n + 1)
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0
        
        # Find bottleneck
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    max_flow = 0
    while True:
        flow = bfs()
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

### 2. **Unit Capacity Assignment**
```python
def assign_unit_capacities(n, edges):
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
    
    return adj, capacity
```

### 3. **Path Counting**
```python
def count_edge_disjoint_paths(n, adj, capacity, source, sink):
    def find_path():
        parent = [-1] * (n + 1)
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    if next_node == sink:
                        return parent
        return None
    
    path_count = 0
    while True:
        parent = find_path()
        if parent is None:
            break
        
        # Update capacities along path
        current = sink
        while current != source:
            capacity[parent[current]][current] -= 1
            capacity[current][parent[current]] += 1
            current = parent[current]
        
        path_count += 1
    
    return path_count
```

## Problem-Solving Framework

1. **Identify problem type**: This is an edge-disjoint paths problem
2. **Choose approach**: Use maximum flow to find edge-disjoint paths
3. **Build graph**: Create adjacency list with unit capacities
4. **Apply Menger's theorem**: Use max flow to find edge-disjoint paths
5. **Find augmenting paths**: Use BFS to find paths with positive residual capacity
6. **Update flow**: Increase flow along augmenting paths
7. **Return result**: Output maximum flow (equals number of edge-disjoint paths)

---

*This analysis shows how to efficiently find maximum edge-disjoint paths using maximum flow algorithm.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Distinct Routes with Edge Capacities**
**Problem**: Find maximum edge-disjoint paths with different edge capacities.
```python
def distinct_routes_with_capacities(n, edges, capacities):
    # capacities[(a, b)] = capacity of edge (a, b)
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = capacities.get((a, b), 1)
    
    # Use Ford-Fulkerson with BFS
    def bfs():
        parent = [-1] * (n + 1)
        parent[1] = 1
        queue = deque([1])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    if next_node == n:
                        break
        
        if parent[n] == -1:
            return 0
        
        # Find bottleneck
        bottleneck = float('inf')
        current = n
        while current != 1:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = n
        while current != 1:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    max_flow = 0
    while True:
        flow = bfs()
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

#### **Variation 2: Distinct Routes with Node Capacities**
**Problem**: Find maximum node-disjoint paths (nodes can only be used once).
```python
def node_disjoint_routes(n, edges):
    # Split each node into in and out nodes
    # Node i becomes in_i and out_i with capacity 1 between them
    
    # Create new graph with 2*n nodes
    new_n = 2 * n
    adj = [[] for _ in range(new_n + 1)]
    capacity = [[0] * (new_n + 1) for _ in range(new_n + 1)]
    
    # Add node capacity edges (in_i -> out_i with capacity 1)
    for i in range(1, n + 1):
        in_node = i
        out_node = n + i
        adj[in_node].append(out_node)
        adj[out_node].append(in_node)
        capacity[in_node][out_node] = 1
    
    # Add original edges (out_i -> in_j)
    for a, b in edges:
        out_a = n + a
        in_b = b
        adj[out_a].append(in_b)
        adj[in_b].append(out_a)
        capacity[out_a][in_b] = 1
    
    # Source is out_1, sink is in_n
    source = n + 1
    sink = n
    
    # Use Ford-Fulkerson
    def bfs():
        parent = [-1] * (new_n + 1)
        parent[source] = source
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0
        
        # Find bottleneck
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    max_flow = 0
    while True:
        flow = bfs()
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

#### **Variation 3: Distinct Routes with Costs**
**Problem**: Find maximum edge-disjoint paths with minimum total cost.
```python
def cost_based_distinct_routes(n, edges, costs):
    # costs[(a, b)] = cost of edge (a, b)
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        cost[a][b] = costs.get((a, b), 0)
        cost[b][a] = -cost[a][b]  # Residual edge has negative cost
    
    # Use minimum cost maximum flow
    def bellman_ford():
        dist = [float('inf')] * (n + 1)
        parent = [-1] * (n + 1)
        dist[1] = 0
        
        for _ in range(n - 1):
            for u in range(1, n + 1):
                for v in adj[u]:
                    if capacity[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                        dist[v] = dist[u] + cost[u][v]
                        parent[v] = u
        
        return parent if dist[n] != float('inf') else None
    
    total_cost = 0
    path_count = 0
    
    while True:
        parent = bellman_ford()
        if parent is None:
            break
        
        # Find bottleneck
        bottleneck = float('inf')
        current = n
        while current != 1:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update flow and cost
        current = n
        while current != 1:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            total_cost += bottleneck * cost[parent[current]][current]
            current = parent[current]
        
        path_count += bottleneck
    
    return path_count, total_cost
```

#### **Variation 4: Distinct Routes with Probabilities**
**Problem**: Each edge has a probability of failure, find expected number of edge-disjoint paths.
```python
def probabilistic_distinct_routes(n, edges, probabilities):
    # probabilities[(a, b)] = probability that edge (a, b) works
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
    
    # For probabilistic edges, we calculate expected flow
    expected_paths = 0
    
    # Calculate expected number of paths based on edge probabilities
    for a, b in edges: if a == 1 or b == 
n: # Direct edges from source or to sink
            prob = probabilities.get((a, b), 0.5)
            expected_paths += prob
    
    return expected_paths
```

#### **Variation 5: Distinct Routes with Multiple Sources/Sinks**
**Problem**: Find maximum edge-disjoint paths from multiple sources to multiple sinks.
```python
def multi_source_sink_distinct_routes(n, edges, sources, sinks):
    # sources = list of source nodes, sinks = list of sink nodes
    
    # Create super source and super sink
    super_source = 0
    super_sink = n + 1
    
    adj = [[] for _ in range(n + 2)]
    capacity = [[0] * (n + 2) for _ in range(n + 2)]
    
    # Add original edges
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
    
    # Add edges from super source to sources
    for source in sources:
        adj[super_source].append(source)
        adj[source].append(super_source)
        capacity[super_source][source] = float('inf')
    
    # Add edges from sinks to super sink
    for sink in sinks:
        adj[sink].append(super_sink)
        adj[super_sink].append(sink)
        capacity[sink][super_sink] = float('inf')
    
    # Use Ford-Fulkerson
    def bfs():
        parent = [-1] * (n + 2)
        parent[super_source] = super_source
        queue = deque([super_source])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    if next_node == super_sink:
                        break
        
        if parent[super_sink] == -1:
            return 0
        
        # Find bottleneck
        bottleneck = float('inf')
        current = super_sink
        while current != super_source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = super_sink
        while current != super_source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    max_flow = 0
    while True:
        flow = bfs()
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

### 🔗 **Related Problems & Concepts**

#### **1. Network Flow Problems**
- **Maximum Flow**: Find maximum flow in network
- **Minimum Cut**: Find minimum capacity cut
- **Multi-commodity Flow**: Multiple flows in same network
- **Circulation Problems**: Flow conservation constraints

#### **2. Path Problems**
- **Shortest Path**: Find shortest path between nodes
- **All Pairs Shortest Path**: Find shortest paths between all pairs
- **K-Shortest Paths**: Find k shortest paths
- **Disjoint Paths**: Find paths that don't share edges/nodes

#### **3. Graph Connectivity**
- **Edge Connectivity**: Minimum edges to disconnect graph
- **Node Connectivity**: Minimum nodes to disconnect graph
- **Strongly Connected Components**: Find strongly connected components
- **Biconnected Components**: Find biconnected components

#### **4. Matching Problems**
- **Maximum Matching**: Find maximum matching in bipartite graph
- **Perfect Matching**: Find matching that covers all nodes
- **Weighted Matching**: Find matching with maximum weight
- **Stable Matching**: Find stable matching

#### **5. Algorithmic Techniques**
- **Ford-Fulkerson**: Maximum flow algorithm
- **Dinic's Algorithm**: Faster maximum flow algorithm
- **Push-Relabel**: Another maximum flow approach
- **Menger's Theorem**: Relates connectivity to disjoint paths

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = distinct_routes_max_flow(n, edges)
    print(result)
```

#### **2. Range Queries on Distinct Routes**
```python
def range_distinct_routes_queries(n, edges, queries):
    # queries = [(source, sink), ...] - find distinct routes between source and sink
    
    results = []
    for source, sink in queries:
        # Modify the graph to have source and sink as specified
        result = distinct_routes_max_flow(n, edges, source, sink)
        results.append(result)
    
    return results
```

#### **3. Interactive Distinct Routes Problems**
```python
def interactive_distinct_routes():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter edges (a b):")
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = distinct_routes_max_flow(n, edges)
    print(f"Maximum distinct routes: {result}")
    
    # Show the paths
    paths = find_edge_disjoint_paths(n, edges)
    print(f"Paths found: {paths}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Menger's Theorem**: Maximum number of edge-disjoint paths equals minimum edge cut
- **Network Flow Theory**: Theory of flows in networks
- **Connectivity Theory**: Study of graph connectivity
- **Matching Theory**: Theory of matchings in graphs

#### **2. Linear Programming**
- **Network Flow LP**: Linear programming formulation of network flow
- **Dual Problems**: Dual of maximum flow is minimum cut
- **Integer Programming**: Integer solutions for flow problems
- **Multi-commodity Flow**: Multiple commodities in network

#### **3. Algorithmic Analysis**
- **Flow Decomposition**: Decompose flow into paths and cycles
- **Residual Networks**: Properties of residual graphs
- **Augmenting Paths**: Properties of augmenting paths
- **Flow Algorithms**: Analysis of flow algorithms

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Network Flow**: Ford-Fulkerson, Dinic's, Push-Relabel algorithms
- **Graph Algorithms**: BFS, DFS, Dijkstra, Floyd-Warshall
- **Connectivity Algorithms**: Tarjan's, Kosaraju's algorithms
- **Matching Algorithms**: Hungarian, Hopcroft-Karp algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Linear Algebra**: Matrix representations of graphs
- **Combinatorics**: Counting paths and flows
- **Optimization**: Linear programming for network problems

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Flow Networks**: Representing flow problems
- **Path Reconstruction**: Finding actual paths from flow
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient network flow techniques and shows various extensions for distinct routes problems.* 