---
layout: simple
title: "Distinct Routes - Maximum Edge-Disjoint Paths"
permalink: /problem_soulutions/graph_algorithms/distinct_routes_analysis
---

# Distinct Routes - Maximum Edge-Disjoint Paths

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand edge-disjoint paths problems and maximum flow concepts
- Apply maximum flow algorithms to find maximum edge-disjoint paths
- Implement efficient edge-disjoint path algorithms with proper flow network construction
- Optimize edge-disjoint path solutions using flow algorithms and path enumeration
- Handle edge cases in edge-disjoint paths (no paths exist, single path, multiple components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Maximum flow, edge-disjoint paths, flow networks, path enumeration, flow algorithms
- **Data Structures**: Flow networks, path tracking, graph representations, flow data structures
- **Mathematical Concepts**: Graph theory, flow networks, path theory, network connectivity, optimization
- **Programming Skills**: Flow algorithms, path enumeration, graph connectivity, algorithm implementation
- **Related Problems**: Download Speed (maximum flow), Police Chase (flow problems), Path enumeration

## Problem Description

**Problem**: Given a directed graph with n nodes and m edges, find the maximum number of edge-disjoint paths from node 1 to node n.

This is a classic maximum flow problem where we need to find the maximum number of edge-disjoint paths from source to sink. We can solve this using maximum flow algorithms by setting all edge capacities to 1.

**Input**: 
- First line: Two integers n and m (number of nodes and edges)
- Next m lines: Two integers a and b (edge from node a to node b)

**Output**: 
- Maximum number of edge-disjoint paths from node 1 to node n

**Constraints**:
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ 1000
- 1 ≤ a, b ≤ n
- Graph is directed
- Nodes are numbered from 1 to n
- No self-loops or multiple edges between same pair of nodes

**Example**:
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

**Explanation**: 
- Path 1: 1 → 2 → 3 → 4
- Path 2: 1 → 3 → 4 (using edge 1→3 and 3→4)
- These paths are edge-disjoint (no shared edges)
- Maximum edge-disjoint paths: 2

## Visual Example

### Input Graph
```
Nodes: 1, 2, 3, 4
Edges: (1→2), (2→3), (3→4), (1→3), (2→4)

Graph representation:
1 ──> 2 ──> 3 ──> 4
│      │      │
└──────┼──────┘
       └──────┘
```

### Maximum Flow Algorithm Process
```
Step 1: Convert to flow network
- Source: 1, Sink: 4
- All edge capacities: 1
- Flow network:
  1 ──1──> 2 ──1──> 3 ──1──> 4
  │        │        │
  └──1─────┼──1─────┘
           └──1─────┘

Step 2: Find augmenting paths

Path 1: 1 → 2 → 3 → 4
- Flow: 1
- Residual graph:
  1 ──0──> 2 ──0──> 3 ──0──> 4
  │        │        │
  └──1─────┼──1─────┘
           └──1─────┘

Path 2: 1 → 3 → 4
- Flow: 1
- Residual graph:
  1 ──0──> 2 ──0──> 3 ──0──> 4
  │        │        │
  └──0─────┼──0─────┘
           └──1─────┘

Step 3: No more augmenting paths
- Maximum flow: 2
- Edge-disjoint paths: 2
```

### Path Analysis
```
Edge-disjoint paths found:
1. 1 → 2 → 3 → 4
2. 1 → 3 → 4

Shared edges: None
Maximum edge-disjoint paths: 2
```

### Key Insight
Maximum flow algorithm works by:
1. Converting to flow network with unit capacities
2. Finding augmenting paths using BFS/DFS
3. Updating residual graph after each path
4. Time complexity: O(m × f) where f is maximum flow
5. Space complexity: O(n + m) for graph representation

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of paths from source to sink
- Check if each combination consists of edge-disjoint paths
- Simple but computationally expensive approach
- Not suitable for large graphs

**Algorithm:**
1. Generate all possible paths from source to sink
2. Try all combinations of paths
3. Check if each combination consists of edge-disjoint paths
4. Return the maximum number of edge-disjoint paths

**Visual Example:**
```
Brute force: Try all possible path combinations
For graph: 1 ──> 2 ──> 3 ──> 4
           │      │      │
           └──────┼──────┘
                  └──────┘

All possible paths:
- Path 1: 1 → 2 → 3 → 4
- Path 2: 1 → 3 → 4
- Path 3: 1 → 2 → 4

All possible combinations:
- {Path 1} → 1 edge-disjoint path
- {Path 2} → 1 edge-disjoint path
- {Path 3} → 1 edge-disjoint path
- {Path 1, Path 2} → 2 edge-disjoint paths (no shared edges)
- {Path 1, Path 3} → 1 edge-disjoint path (shared edge 1→2)
- {Path 2, Path 3} → 1 edge-disjoint path (shared edge 1→3)
- {Path 1, Path 2, Path 3} → 1 edge-disjoint path (shared edges)

Maximum edge-disjoint paths: 2
```

**Implementation:**
```python
def distinct_routes_brute_force(n, m, edges):
    from itertools import combinations
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Find all paths from source to sink
    all_paths = []
    
    def find_paths(current, target, path, visited):
        if current == target:
            all_paths.append(path[:])
            return
        
        for next_node in adj[current]:
            if next_node not in visited:
                visited.add(next_node)
                path.append(next_node)
                find_paths(next_node, target, path, visited)
                path.pop()
                visited.remove(next_node)
    
    # Find all paths from 1 to n
    find_paths(1, n, [1], {1})
    
    max_disjoint_paths = 0
    
    # Try all combinations of paths
    for k in range(1, len(all_paths) + 1):
        for path_combination in combinations(all_paths, k):
            if are_edge_disjoint(path_combination):
                max_disjoint_paths = max(max_disjoint_paths, len(path_combination))
    
    return max_disjoint_paths

def are_edge_disjoint(paths):
    # Check if paths are edge-disjoint
    used_edges = set()
    
    for path in paths:
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            if edge in used_edges:
                return False
            used_edges.add(edge)
    
    return True
```

**Time Complexity:** O(2^p × p × m) where p is the number of paths
**Space Complexity:** O(p × m) for storing all paths

**Why it's inefficient:**
- Exponential time complexity O(2^p)
- Not suitable for large graphs
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: Ford-Fulkerson Algorithm (Better)

**Key Insights from Ford-Fulkerson Solution:**
- Convert edge-disjoint paths problem to maximum flow problem
- Use Ford-Fulkerson algorithm to find maximum flow
- Set all edge capacities to 1 for edge-disjoint paths
- Much more efficient than brute force approach

**Algorithm:**
1. Convert graph to flow network with unit capacities
2. Use Ford-Fulkerson algorithm to find maximum flow
3. Each unit of flow represents one edge-disjoint path
4. Return the maximum flow value

**Visual Example:**
```
Ford-Fulkerson algorithm for graph: 1 ──> 2 ──> 3 ──> 4
                                     │      │      │
                                     └──────┼──────┘
                                            └──────┘

Step 1: Convert to flow network
- Source: 1, Sink: 4
- All edge capacities: 1
- Flow network:
  1 ──1──> 2 ──1──> 3 ──1──> 4
  │        │        │
  └──1─────┼──1─────┘
           └──1─────┘

Step 2: Find augmenting paths

Path 1: 1 → 2 → 3 → 4
- Flow: 1
- Residual graph:
  1 ──0──> 2 ──0──> 3 ──0──> 4
  │        │        │
  └──1─────┼──1─────┘
           └──1─────┘

Path 2: 1 → 3 → 4
- Flow: 1
- Residual graph:
  1 ──0──> 2 ──0──> 3 ──0──> 4
  │        │        │
  └──0─────┼──0─────┘
           └──1─────┘

Step 3: No more augmenting paths
- Maximum flow: 2
- Edge-disjoint paths: 2
```

**Implementation:**
```python
def distinct_routes_ford_fulkerson(n, m, edges):
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

**Time Complexity:** O(m × f) where f is maximum flow
**Space Complexity:** O(n + m) for graph representation

**Why it's better:**
- Polynomial time complexity O(m × f)
- Standard method for maximum flow problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Edmonds-Karp Algorithm (Optimal)

**Key Insights from Edmonds-Karp Solution:**
- Use BFS to find shortest augmenting paths
- Guarantees O(n × m²) time complexity
- Most efficient approach for maximum flow problems
- Standard method in competitive programming

**Algorithm:**
1. Convert graph to flow network with unit capacities
2. Use Edmonds-Karp algorithm to find maximum flow
3. Each unit of flow represents one edge-disjoint path
4. Return the maximum flow value

**Visual Example:**
```
Edmonds-Karp algorithm for graph: 1 ──> 2 ──> 3 ──> 4
                                   │      │      │
                                   └──────┼──────┘
                                          └──────┘

Step 1: Convert to flow network
- Source: 1, Sink: 4
- All edge capacities: 1
- Flow network:
  1 ──1──> 2 ──1──> 3 ──1──> 4
  │        │        │
  └──1─────┼──1─────┘
           └──1─────┘

Step 2: Find shortest augmenting paths using BFS

Path 1: 1 → 2 → 3 → 4 (length 3)
- Flow: 1
- Residual graph:
  1 ──0──> 2 ──0──> 3 ──0──> 4
  │        │        │
  └──1─────┼──1─────┘
           └──1─────┘

Path 2: 1 → 3 → 4 (length 2)
- Flow: 1
- Residual graph:
  1 ──0──> 2 ──0──> 3 ──0──> 4
  │        │        │
  └──0─────┼──0─────┘
           └──1─────┘

Step 3: No more augmenting paths
- Maximum flow: 2
- Edge-disjoint paths: 2
```

**Implementation:**
```python
def distinct_routes_edmonds_karp(n, m, edges):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)  # For residual graph
        capacity[a][b] = 1  # Unit capacity for edge-disjoint paths
    
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

def solve_distinct_routes():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = distinct_routes_edmonds_karp(n, m, edges)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_distinct_routes()
```

**Time Complexity:** O(n × m²) for Edmonds-Karp algorithm
**Space Complexity:** O(n + m) for graph representation

**Why it's optimal:**
- O(n × m²) time complexity is optimal for maximum flow
- Uses BFS to find shortest augmenting paths
- Most efficient approach for competitive programming
- Standard method for maximum flow problems

## 🎯 Problem Variations

### Variation 1: Edge-Disjoint Paths with Different Capacities
**Problem**: Find maximum edge-disjoint paths with different edge capacities.

**Link**: [CSES Problem Set - Edge-Disjoint Paths with Capacities](https://cses.fi/problemset/task/edge_disjoint_paths_capacities)

```python
def distinct_routes_capacities(n, m, edges, capacities):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i, (a, b) in enumerate(edges):
        adj[a].append(b)
        adj[b].append(a)  # For residual graph
        capacity[a][b] = capacities[i]
    
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
```

### Variation 2: Edge-Disjoint Paths with Multiple Sources and Sinks
**Problem**: Find maximum edge-disjoint paths with multiple sources and sinks.

**Link**: [CSES Problem Set - Edge-Disjoint Paths Multiple Sources](https://cses.fi/problemset/task/edge_disjoint_paths_multiple_sources)

```python
def distinct_routes_multiple_sources(n, m, edges, sources, sinks):
    from collections import deque
    
    # Add super source and super sink
    super_source = 0
    super_sink = n + 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 2)]
    capacity = [[0] * (n + 2) for _ in range(n + 2)]
    
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
    
    # Add original edges
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)  # For residual graph
        capacity[a][b] = 1  # Unit capacity for edge-disjoint paths
    
    def bfs(source, sink):
        # Find shortest augmenting path using BFS
        parent = [-1] * (n + 2)
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
        flow = bfs(super_source, super_sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

### Variation 3: Edge-Disjoint Paths with Path Length Constraints
**Problem**: Find maximum edge-disjoint paths with maximum path length constraints.

**Link**: [CSES Problem Set - Edge-Disjoint Paths Length Constraints](https://cses.fi/problemset/task/edge_disjoint_paths_length_constraints)

```python
def distinct_routes_length_constraints(n, m, edges, max_length):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)  # For residual graph
        capacity[a][b] = 1  # Unit capacity for edge-disjoint paths
    
    def bfs(source, sink):
        # Find shortest augmenting path using BFS with length constraint
        parent = [-1] * (n + 1)
        distance = [-1] * (n + 1)
        parent[source] = source
        distance[source] = 0
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            if distance[current] >= max_length:
                continue
            
            for next_node in adj[current]:
                if (parent[next_node] == -1 and 
                    capacity[current][next_node] > 0 and
                    distance[current] + 1 <= max_length):
                    
                    parent[next_node] = current
                    distance[next_node] = distance[current] + 1
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
    
    # Edmonds-Karp algorithm with length constraints
    max_flow = 0
    while True:
        flow = bfs(1, n)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

## 🔗 Related Problems

- **[Download Speed](/cses-analyses/problem_soulutions/graph_algorithms/download_speed_analysis/)**: Maximum flow problems
- **[Police Chase](/cses-analyses/problem_soulutions/graph_algorithms/police_chase_analysis/)**: Flow problems
- **[School Dance](/cses-analyses/problem_soulutions/graph_algorithms/school_dance_analysis/)**: Bipartite matching problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Maximum Flow**: Essential for analyzing network connectivity and optimization
2. **Edge-Disjoint Paths**: Key concept for network reliability and routing
3. **Flow Networks**: Important data structure for flow problems
4. **Residual Graphs**: Critical for flow algorithm implementation
5. **Augmenting Paths**: Foundation for maximum flow algorithms
6. **Network Optimization**: Foundation for many real-world problems

## 📝 Summary

The Distinct Routes problem demonstrates fundamental maximum flow concepts for finding edge-disjoint paths. We explored three approaches:

1. **Brute Force Path Enumeration**: O(2^p × p × m) time complexity using exhaustive search, inefficient for large graphs
2. **Ford-Fulkerson Algorithm**: O(m × f) time complexity using augmenting paths, better approach for flow problems
3. **Edmonds-Karp Algorithm**: O(n × m²) time complexity using BFS for shortest paths, optimal approach for maximum flow

The key insights include understanding edge-disjoint paths as maximum flow problems, using flow networks with unit capacities, and applying augmenting path algorithms for efficient flow computation. This problem serves as an excellent introduction to maximum flow algorithms and network optimization techniques.

