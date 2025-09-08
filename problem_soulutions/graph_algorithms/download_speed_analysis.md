---
layout: simple
title: "Download Speed - Maximum Network Flow"
permalink: /problem_soulutions/graph_algorithms/download_speed_analysis
---

# Download Speed - Maximum Network Flow

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand maximum flow problems and network flow concepts
- Apply Ford-Fulkerson algorithm or Edmonds-Karp algorithm to find maximum flow
- Implement efficient maximum flow algorithms with proper residual graph handling
- Optimize maximum flow solutions using graph representations and flow algorithms
- Handle edge cases in maximum flow problems (no flow paths, capacity constraints, disconnected graphs)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Ford-Fulkerson algorithm, Edmonds-Karp algorithm, maximum flow, residual graphs, flow networks
- **Data Structures**: Adjacency lists, residual graphs, flow tracking, graph representations
- **Mathematical Concepts**: Graph theory, flow networks, maximum flow properties, network optimization
- **Programming Skills**: Graph traversal, flow calculations, residual graph manipulation, algorithm implementation
- **Related Problems**: School Dance (bipartite matching), Police Chase (flow problems), Network flow algorithms

## Problem Description

**Problem**: Given a network with n computers and m connections, find the maximum download speed from computer 1 to computer n. Each connection has a capacity.

This is a classic maximum flow problem where we need to find the maximum amount of data that can flow from source (computer 1) to sink (computer n) through the network connections.

**Input**: 
- First line: Two integers n and m (number of computers and connections)
- Next m lines: Three integers a, b, and c (connection from computer a to computer b with capacity c)

**Output**: 
- Maximum download speed from computer 1 to computer n

**Constraints**:
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ 1000
- 1 ≤ a, b ≤ n
- 1 ≤ c ≤ 10⁹
- Graph is directed
- Computers are numbered from 1 to n

**Example**:
```
Input:
4 5
1 2 3
2 3 2
3 4 3
1 3 1
2 4 2

Output:
5
```

**Explanation**: 
- Path 1: 1 → 2 → 3 → 4 (capacity: min(3,2,3) = 2)
- Path 2: 1 → 3 → 4 (capacity: min(1,3) = 1)
- Path 3: 1 → 2 → 4 (capacity: min(3,2) = 2)
- Maximum flow: 2 + 1 + 2 = 5

## Visual Example

### Input Network
```
Computers: 1, 2, 3, 4
Connections: (1→2,3), (2→3,2), (3→4,3), (1→3,1), (2→4,2)

Network representation:
1 ──3──> 2 ──2──> 3 ──3──> 4
│        │        │
└──1─────┼──2─────┘
          └──2─────┘
```

### Maximum Flow Algorithm Process
```
Step 1: Initialize flow network
- Source: 1, Sink: 4
- All flows initially 0

Step 2: Find augmenting paths

Path 1: 1 → 2 → 3 → 4
- Bottleneck: min(3,2,3) = 2
- Flow: 2
- Residual graph:
  1 ──1──> 2 ──0──> 3 ──1──> 4
  │        │        │
  └──1─────┼──2─────┘
            └──2─────┘

Path 2: 1 → 3 → 4
- Bottleneck: min(1,1) = 1
- Flow: 1
- Residual graph:
  1 ──1──> 2 ──0──> 3 ──0──> 4
  │        │        │
  └──0─────┼──2─────┘
            └──2─────┘

Path 3: 1 → 2 → 4
- Bottleneck: min(1,2) = 1
- Flow: 1
- Residual graph:
  1 ──0──> 2 ──0──> 3 ──0──> 4
  │        │        │
  └──0─────┼──2─────┘
            └──1─────┘

Step 3: No more augmenting paths
- Maximum flow: 2 + 1 + 1 = 4
```

### Flow Analysis
```
Maximum flow paths:
1. 1 → 2 → 3 → 4: flow 2
2. 1 → 3 → 4: flow 1
3. 1 → 2 → 4: flow 1

Total maximum flow: 4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Maximum Flow (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths from source to sink
- Calculate flow for each path and sum them up
- Simple but computationally expensive approach
- Not suitable for large networks

**Algorithm:**
1. Generate all possible paths from source to sink
2. Calculate maximum flow for each path
3. Sum up all flows to get total maximum flow
4. Return the total maximum flow

**Visual Example:**
```
Brute force: Try all possible paths
For network: 1→2→3→4, 1→3→4, 1→2→4 with capacities (3,2,3), (1,3), (3,2)

All possible paths:
- Path 1: 1 → 2 → 3 → 4 → Flow: min(3,2,3) = 2
- Path 2: 1 → 3 → 4 → Flow: min(1,3) = 1
- Path 3: 1 → 2 → 4 → Flow: min(3,2) = 2

Total flow: 2 + 1 + 2 = 5
```

**Implementation:**
```python
def download_speed_brute_force(n, m, connections):
    from itertools import permutations
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b, c in connections:
        adj[a].append(b)
        capacity[a][b] = c
    
    def find_all_paths(source, sink, path, visited):
        if source == sink:
            return [path[:]]
        
        paths = []
        for next_node in adj[source]:
            if next_node not in visited and capacity[source][next_node] > 0:
                visited.add(next_node)
                path.append(next_node)
                paths.extend(find_all_paths(next_node, sink, path, visited))
                path.pop()
                visited.remove(next_node)
        
        return paths
    
    # Find all paths from source to sink
    all_paths = find_all_paths(1, n, [1], {1})
    
    total_flow = 0
    for path in all_paths:
        # Calculate bottleneck capacity for this path
        bottleneck = float('inf')
        for i in range(len(path) - 1):
            bottleneck = min(bottleneck, capacity[path[i]][path[i+1]])
        
        total_flow += bottleneck
    
    return total_flow
```

**Time Complexity:** O(n! × n) for finding all paths
**Space Complexity:** O(n²) for adjacency matrix

**Why it's inefficient:**
- Exponential time complexity O(n!)
- Not suitable for large networks
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: Ford-Fulkerson Algorithm (Better)

**Key Insights from Ford-Fulkerson Solution:**
- Use augmenting paths to find maximum flow
- Update residual graph after each path
- Much more efficient than brute force approach
- Standard method for maximum flow problems

**Algorithm:**
1. Initialize flow network with zero flows
2. Find augmenting path from source to sink using BFS
3. Calculate bottleneck capacity along the path
4. Update residual graph by pushing flow along the path
5. Repeat until no more augmenting paths exist

**Visual Example:**
```
Ford-Fulkerson algorithm for network: 1→2→3→4, 1→3→4, 1→2→4 with capacities (3,2,3), (1,3), (3,2)

Step 1: Find augmenting path 1 → 2 → 3 → 4
- Bottleneck: min(3,2,3) = 2
- Push flow 2, update residual graph

Step 2: Find augmenting path 1 → 3 → 4
- Bottleneck: min(1,3) = 1
- Push flow 1, update residual graph

Step 3: Find augmenting path 1 → 2 → 4
- Bottleneck: min(1,2) = 1
- Push flow 1, update residual graph

Step 4: No more augmenting paths
- Maximum flow: 2 + 1 + 1 = 4
```

**Implementation:**
```python
def download_speed_ford_fulkerson(n, m, connections):
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)  # For residual graph
        capacity[a][b] = c
    
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

**Time Complexity:** O(m × f) where f is maximum flow
**Space Complexity:** O(n²) for adjacency matrix

**Why it's better:**
- Polynomial time complexity O(m × f)
- Simple and intuitive approach
- Standard method for maximum flow problems
- Suitable for competitive programming

### Approach 3: Edmonds-Karp Algorithm (Optimal)

**Key Insights from Edmonds-Karp Solution:**
- Use BFS to find shortest augmenting paths
- Guarantees O(n × m²) time complexity
- Most efficient approach for maximum flow problems
- Standard method in competitive programming

**Algorithm:**
1. Initialize flow network with zero flows
2. Find shortest augmenting path from source to sink using BFS
3. Calculate bottleneck capacity along the path
4. Update residual graph by pushing flow along the path
5. Repeat until no more augmenting paths exist

**Visual Example:**
```
Edmonds-Karp algorithm for network: 1→2→3→4, 1→3→4, 1→2→4 with capacities (3,2,3), (1,3), (3,2)

Step 1: Find shortest augmenting path 1 → 2 → 3 → 4
- Bottleneck: min(3,2,3) = 2
- Push flow 2, update residual graph

Step 2: Find shortest augmenting path 1 → 3 → 4
- Bottleneck: min(1,3) = 1
- Push flow 1, update residual graph

Step 3: Find shortest augmenting path 1 → 2 → 4
- Bottleneck: min(1,2) = 1
- Push flow 1, update residual graph

Step 4: No more augmenting paths
- Maximum flow: 2 + 1 + 1 = 4
```

**Implementation:**
```python
def download_speed_edmonds_karp(n, m, connections):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)  # For residual graph
        capacity[a][b] = c
    
    def bfs(source, sink):
        # Find shortest augmenting path using BFS
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
    
    # Edmonds-Karp algorithm
    max_flow = 0
    while True:
        flow = bfs(1, n)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow

def solve_download_speed():
    n, m = map(int, input().split())
    connections = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        connections.append((a, b, c))
    
    result = download_speed_edmonds_karp(n, m, connections)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_download_speed()
```

**Time Complexity:** O(n × m²) for Edmonds-Karp algorithm
**Space Complexity:** O(n²) for adjacency matrix

**Why it's optimal:**
- O(n × m²) time complexity is optimal for maximum flow problems
- Uses BFS to find shortest augmenting paths
- Most efficient approach for competitive programming
- Standard method for maximum flow problems

## 🎯 Problem Variations

### Variation 1: Maximum Flow with Multiple Sources and Sinks
**Problem**: Find maximum flow in a network with multiple sources and sinks.

**Link**: [CSES Problem Set - Multi-Source Multi-Sink Flow](https://cses.fi/problemset/task/multi_source_sink_flow)

```python
def multi_source_sink_flow(n, m, connections, sources, sinks):
    # Add super source and super sink
    super_source = 0
    super_sink = n + 1
    
    # Connect super source to all sources
    for source in sources:
        connections.append((super_source, source, float('inf')))
    
    # Connect all sinks to super sink
    for sink in sinks:
        connections.append((sink, super_sink, float('inf')))
    
    # Find maximum flow from super source to super sink
    return download_speed_edmonds_karp(n + 2, len(connections), connections)
```

### Variation 2: Maximum Flow with Edge Capacities and Node Capacities
**Problem**: Find maximum flow considering both edge and node capacities.

**Link**: [CSES Problem Set - Flow with Node Capacities](https://cses.fi/problemset/task/flow_node_capacities)

```python
def flow_with_node_capacities(n, m, connections, node_capacities):
    # Split each node into two nodes (in and out)
    # Connect in-node to out-node with node capacity
    
    new_connections = []
    for a, b, c in connections:
        # Connect out-node of a to in-node of b
        new_connections.append((a + n, b, c))
    
    # Connect in-node to out-node for each node
    for i in range(1, n + 1):
        new_connections.append((i, i + n, node_capacities[i]))
    
    # Find maximum flow from source to sink
    return download_speed_edmonds_karp(2 * n, len(new_connections), new_connections)
```

### Variation 3: Minimum Cost Maximum Flow
**Problem**: Find maximum flow with minimum cost.

**Link**: [CSES Problem Set - Minimum Cost Maximum Flow](https://cses.fi/problemset/task/min_cost_max_flow)

```python
def min_cost_max_flow(n, m, connections, costs):
    # Use Bellman-Ford to find minimum cost paths
    # Push flow along minimum cost paths
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i, (a, b, c) in enumerate(connections):
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
        cost[a][b] = costs[i]
        cost[b][a] = -costs[i]  # Negative cost for reverse edges
    
    def bellman_ford(source, sink):
        # Find minimum cost path using Bellman-Ford
        dist = [float('inf')] * (n + 1)
        parent = [-1] * (n + 1)
        dist[source] = 0
        
        for _ in range(n - 1):
            for u in range(1, n + 1):
                for v in adj[u]:
                    if capacity[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                        dist[v] = dist[u] + cost[u][v]
                        parent[v] = u
        
        if parent[sink] == -1:
            return 0, 0
        
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
        
        return bottleneck, bottleneck * dist[sink]
    
    max_flow = 0
    total_cost = 0
    
    while True:
        flow, cost_flow = bellman_ford(1, n)
        if flow == 0:
            break
        max_flow += flow
        total_cost += cost_flow
    
    return max_flow, total_cost
```

## 🔗 Related Problems

- **[School Dance](/cses-analyses/problem_soulutions/graph_algorithms/school_dance_analysis/)**: Bipartite matching problems
- **[Police Chase](/cses-analyses/problem_soulutions/graph_algorithms/police_chase_analysis/)**: Flow problems
- **[Network Flow Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Flow network problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Maximum Flow**: Essential for network optimization problems
2. **Ford-Fulkerson Algorithm**: Basic approach for maximum flow problems
3. **Edmonds-Karp Algorithm**: Optimal approach using BFS for shortest paths
4. **Residual Graphs**: Key concept for flow network manipulation
5. **Augmenting Paths**: Core mechanism for finding maximum flow
6. **Network Flow Theory**: Foundation for many optimization problems

## 📝 Summary

The Download Speed problem demonstrates fundamental maximum flow concepts for optimizing network data transfer. We explored three approaches:

1. **Brute Force Maximum Flow**: O(n! × n) time complexity using exhaustive path search, inefficient for large networks
2. **Ford-Fulkerson Algorithm**: O(m × f) time complexity using augmenting paths, optimal and intuitive approach
3. **Edmonds-Karp Algorithm**: O(n × m²) time complexity using BFS for shortest paths, most efficient approach

The key insights include understanding maximum flow as network optimization problems, using augmenting paths for efficient flow calculation, and applying residual graph concepts for flow network manipulation. This problem serves as an excellent introduction to network flow algorithms and optimization theory.
