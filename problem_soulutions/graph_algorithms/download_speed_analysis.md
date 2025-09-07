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

## 📋 Problem Description

Given a network with n computers and m connections, find the maximum download speed from computer 1 to computer n. Each connection has a capacity.

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

## 🎯 Visual Example

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

### Key Insight
Maximum flow algorithm works by:
1. Finding augmenting paths from source to sink
2. Pushing flow along each path up to bottleneck capacity
3. Updating residual graph after each path
4. Time complexity: O(m × f) where f is maximum flow
5. Space complexity: O(n + m) for graph representation

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find maximum flow from source to sink in network
- **Key Insight**: Use maximum flow algorithms like Ford-Fulkerson
- **Challenge**: Efficiently find augmenting paths and update residual graph

### Step 2: Initial Approach
**Ford-Fulkerson algorithm for maximum flow:**

```python
def download_speed_naive(n, m, connections):
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

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Ford-Fulkerson with BFS - O(n * m * max_flow)
**Description**: Use optimized Ford-Fulkerson algorithm with better BFS implementation.

```python
def download_speed_optimized(n, m, connections):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
    
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

**Why this improvement works**: We use optimized Ford-Fulkerson algorithm with better BFS implementation to find maximum flow efficiently.

### Step 3: Optimization/Alternative
**Enhanced Ford-Fulkerson with better path finding:**

### Step 4: Complete Solution

```python
from collections import deque

n, m = map(int, input().split())
connections = []
for _ in range(m):
    a, b, c = map(int, input().split())
    connections.append((a, b, c))

def find_maximum_download_speed(n, m, connections):
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

result = find_maximum_download_speed(n, m, connections)
print(result)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple network with single path (should return path capacity)
- **Test 2**: Network with multiple paths (should return sum of path capacities)
- **Test 3**: Network with bottleneck (should return bottleneck capacity)
- **Test 4**: Network with no path (should return 0)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Ford-Fulkerson | O(n * m * max_flow) | O(n²) | Use Ford-Fulkerson for maximum flow |
| Optimized Ford-Fulkerson | O(n * m * max_flow) | O(n²) | Optimized Ford-Fulkerson implementation |

## 🎨 Visual Example

### Input Example
```
4 computers, 5 connections:
Connection 1: 1 → 2 (capacity: 3)
Connection 2: 2 → 3 (capacity: 2)
Connection 3: 3 → 4 (capacity: 3)
Connection 4: 1 → 3 (capacity: 1)
Connection 5: 2 → 4 (capacity: 2)
```

### Network Graph Visualization
```
Computers: 1, 2, 3, 4
Connections with capacities:

    1 ──3──→ 2
    │        │
    │1       │2
    ↓        ↓
    3 ──3──→ 4
    │
    │2
    ↓
    4

Source: Computer 1
Sink: Computer 4
```

### Ford-Fulkerson Algorithm Process
```
Step 1: Find augmenting path 1 → 2 → 3 → 4
- Path: 1 → 2 → 3 → 4
- Bottleneck: min(3, 2, 3) = 2
- Send flow: 2
- Update residual capacities
- Total flow: 2

Residual graph after step 1:
    1 ──1──→ 2
    │        │
    │1       │0
    ↓        ↓
    3 ──3──→ 4
    │
    │2
    ↓
    4

Step 2: Find augmenting path 1 → 3 → 4
- Path: 1 → 3 → 4
- Bottleneck: min(1, 3) = 1
- Send flow: 1
- Update residual capacities
- Total flow: 3

Residual graph after step 2:
    1 ──1──→ 2
    │        │
    │0       │0
    ↓        ↓
    3 ──2──→ 4
    │
    │2
    ↓
    4

Step 3: Find augmenting path 1 → 2 → 4
- Path: 1 → 2 → 4
- Bottleneck: min(1, 2) = 1
- Send flow: 1
- Update residual capacities
- Total flow: 4

Residual graph after step 3:
    1 ──0──→ 2
    │        │
    │0       │0
    ↓        ↓
    3 ──2──→ 4
    │
    │1
    ↓
    4

Step 4: Find augmenting path 1 → 2 → 3 → 4
- Path: 1 → 2 → 3 → 4
- Bottleneck: min(0, 0, 2) = 0
- No flow possible

No more augmenting paths found.
Maximum flow: 4
```

### Flow Paths Summary
```
Path 1: 1 → 2 → 3 → 4 (flow: 2)
Path 2: 1 → 3 → 4 (flow: 1)
Path 3: 1 → 2 → 4 (flow: 1)

Total maximum flow: 2 + 1 + 1 = 4
```

### Residual Graph Concept
```
For each edge (u, v) with capacity c and flow f:
- Forward edge: (u, v) with residual capacity c - f
- Backward edge: (v, u) with residual capacity f

Example edge 1 → 2 with capacity 3:
- If flow = 2: forward edge (1,2) has capacity 1, backward edge (2,1) has capacity 2
- If flow = 3: forward edge (1,2) has capacity 0, backward edge (2,1) has capacity 3
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Ford-Fulkerson  │ O(n×m×f)     │ O(n²)        │ Augmenting   │
│                 │              │              │ paths        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Edmonds-Karp    │ O(n×m²)      │ O(n²)        │ BFS for      │
│                 │              │              │ shortest path│
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dinic's         │ O(n²×m)      │ O(n²)        │ Level graph  │
│                 │              │              │ + blocking   │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **Maximum Flow**: Find maximum flow from source to sink in network
- **Ford-Fulkerson Algorithm**: Use BFS to find augmenting paths
- **Residual Graph**: Maintain residual capacities for flow updates
- **Augmenting Paths**: Find paths with positive residual capacity

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Dinic's Algorithm for Maximum Flow**
```python
def dinic_maximum_flow(n, m, connections):
    # More efficient maximum flow algorithm
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
    
    def bfs_level_graph(source, sink):
        level = [-1] * (n + 1)
        level[source] = 0
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            for next_node in adj[current]:
                if level[next_node] == -1 and capacity[current][next_node] > 0:
                    level[next_node] = level[current] + 1
                    queue.append(next_node)
        
        return level[sink] != -1
    
    def dfs_blocking_flow(current, sink, flow, level):
        if current == sink:
            return flow
        
        for next_node in adj[current]:
            if level[next_node] == level[current] + 1 and capacity[current][next_node] > 0:
                pushed = dfs_blocking_flow(next_node, sink, min(flow, capacity[current][next_node]), level)
                if pushed > 0:
                    capacity[current][next_node] -= pushed
                    capacity[next_node][current] += pushed
                    return pushed
        return 0
    
    max_flow = 0
    while bfs_level_graph(1, n):
        while True:
            flow = dfs_blocking_flow(1, n, float('inf'), level)
            if flow == 0:
                break
            max_flow += flow
    
    return max_flow
```

#### **2. Minimum Cost Maximum Flow**
```python
def min_cost_max_flow(n, m, connections, costs):
    # Find maximum flow with minimum cost
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i, (a, b, c) in enumerate(connections):
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
        cost[a][b] = costs[i]
        cost[b][a] = -costs[i]  # Negative cost for reverse edge
    
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
        
        return dist, parent
    
    max_flow = 0
    total_cost = 0
    
    while True:
        dist, parent = bellman_ford()
        if dist[n] == float('inf'):
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
        
        max_flow += bottleneck
    
    return max_flow, total_cost
```

#### **3. Multi-Source Multi-Sink Flow**
```python
def multi_source_sink_flow(n, m, connections, sources, sinks):
    # Find maximum flow with multiple sources and sinks
    # Add super source and super sink
    super_source = 0
    super_sink = n + 1
    
    adj = [[] for _ in range(n + 2)]
    capacity = [[0] * (n + 2) for _ in range(n + 2)]
    
    # Add connections from super source to sources
    for source in sources:
        adj[super_source].append(source)
        adj[source].append(super_source)
        capacity[super_source][source] = float('inf')
    
    # Add connections from sinks to super sink
    for sink in sinks:
        adj[sink].append(super_sink)
        adj[super_sink].append(sink)
        capacity[sink][super_sink] = float('inf')
    
    # Add original connections
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
    
    def bfs(source, sink):
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
        flow = bfs(super_source, super_sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

## 🔗 Related Problems

### Links to Similar Problems
- **Network Flow**: Core flow algorithms
- **Maximum Flow**: Flow optimization problems
- **Graph Connectivity**: Connectivity and cut problems
- **Network Optimization**: Network design problems

## 📚 Learning Points

### Key Takeaways
- **Maximum flow** is fundamental for network optimization
- **Ford-Fulkerson** provides a simple but effective approach
- **Residual graphs** are crucial for flow updates
- **Augmenting paths** are the key to increasing flow
- **Network flow** has many real-world applications

## Key Insights for Other Problems

### 1. **Maximum Flow**
**Principle**: Use Ford-Fulkerson or Dinic's algorithm to find maximum flow.
**Applicable to**: Flow problems, network problems, capacity problems

### 2. **Residual Graph**
**Principle**: Maintain residual graph to find augmenting paths.
**Applicable to**: Flow problems, graph problems, network problems

### 3. **Augmenting Path**
**Principle**: Find paths with positive residual capacity to increase flow.
**Applicable to**: Flow problems, path problems, optimization problems

## Notable Techniques

### 1. **Ford-Fulkerson Algorithm**
```python
def ford_fulkerson(n, adj, capacity, source, sink):
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

### 2. **Residual Graph Construction**
```python
def build_residual_graph(n, connections):
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
    
    return adj, capacity
```

### 3. **BFS for Augmenting Path**
```python
def find_augmenting_path(n, adj, capacity, source, sink):
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
```

## Problem-Solving Framework

1. **Identify problem type**: This is a maximum flow problem
2. **Choose approach**: Use Ford-Fulkerson algorithm
3. **Build graph**: Create adjacency list with capacities
4. **Initialize residual graph**: Set up residual capacities
5. **Find augmenting paths**: Use BFS to find paths with positive residual capacity
6. **Update flow**: Increase flow along augmenting paths
7. **Return result**: Output maximum flow value

---

*This analysis shows how to efficiently find maximum flow using Ford-Fulkerson algorithm.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Download Speed with Node Capacities**
**Problem**: Each computer has a maximum download capacity, find maximum flow with node constraints.
```python
def download_speed_node_capacities(n, connections, node_capacities):
    # node_capacities[i] = maximum download capacity of computer i
    
    # Split each node into in and out nodes
    # Node i becomes in_i and out_i with capacity node_capacities[i] between them
    
    new_n = 2 * n
    adj = [[] for _ in range(new_n + 1)]
    capacity = [[0] * (new_n + 1) for _ in range(new_n + 1)]
    
    # Add node capacity edges (in_i -> out_i with capacity node_capacities[i])
    for i in range(1, n + 1):
        in_node = i
        out_node = n + i
        adj[in_node].append(out_node)
        adj[out_node].append(in_node)
        capacity[in_node][out_node] = node_capacities[i - 1]
    
    # Add original edges (out_i -> in_j)
    for a, b, c in connections:
        out_a = n + a
        in_b = b
        adj[out_a].append(in_b)
        adj[in_b].append(out_a)
        capacity[out_a][in_b] = c  # Original edge capacity
    
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

#### **Variation 2: Download Speed with Costs**
**Problem**: Each connection has a cost, find maximum flow with minimum total cost.
```python
def cost_based_download_speed(n, connections, costs):
    # costs[(a, b)] = cost per unit flow on connection (a, b)
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
        capacity[b][a] = 0
        cost[a][b] = costs.get((a, b), 0)
        cost[b][a] = -cost[a][b]  # Reverse edge cost
    
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
    max_flow = 0
    
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
        
        max_flow += bottleneck
    
    return max_flow, total_cost
```

#### **Variation 3: Download Speed with Probabilities**
**Problem**: Each connection has a success probability, find expected maximum flow.
```python
def probabilistic_download_speed(n, connections, probabilities):
    # probabilities[(a, b)] = probability that connection (a, b) works
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
        capacity[b][a] = 0
    
    # Calculate expected flow based on connection probabilities
    expected_flow = 0
    
    # For each connection, calculate expected contribution
    for a, b, c in connections:
        prob = probabilities.get((a, b), 0.5)
        expected_flow += c * prob
    
    return expected_flow
```

#### **Variation 4: Download Speed with Multiple Sources**
**Problem**: Multiple computers can serve as sources, find maximum flow from any source to destination.
```python
def multi_source_download_speed(n, connections, sources):
    # sources = list of source computers
    
    # Create super source
    super_source = 0
    adj = [[] for _ in range(n + 2)]
    capacity = [[0] * (n + 2) for _ in range(n + 2)]
    
    # Add original connections
    for a, b, c in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = c
        capacity[b][a] = 0
    
    # Add edges from super source to all sources
    for source in sources:
        adj[super_source].append(source)
        adj[source].append(super_source)
        capacity[super_source][source] = float('inf')  # Infinite capacity
    
    # Use Ford-Fulkerson with super source
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
                    if next_node == n:
                        break
        
        if parent[n] == -1:
            return 0
        
        # Find bottleneck
        bottleneck = float('inf')
        current = n
        while current != super_source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = n
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

#### **Variation 5: Download Speed with Dynamic Updates**
**Problem**: Handle dynamic updates to connection capacities and find maximum flow after each update.
```python
def dynamic_download_speed(n, initial_connections, updates):
    # updates = [(connection, new_capacity), ...]
    
    connections = initial_connections.copy()
    results = []
    
    for connection, new_capacity in updates:
        # Update connection capacity
        a, b, old_capacity = connection
        connections.remove(connection)
        connections.append((a, b, new_capacity))
        
        # Recompute maximum flow
        adj = [[] for _ in range(n + 1)]
        capacity = [[0] * (n + 1) for _ in range(n + 1)]
        
        for a, b, c in connections:
            adj[a].append(b)
            adj[b].append(a)
            capacity[a][b] = c
            capacity[b][a] = 0
        
        # Use Ford-Fulkerson
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
        
        results.append(max_flow)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Network Flow Problems**
- **Maximum Flow**: Find maximum flow in network
- **Minimum Cost Flow**: Flow with minimum cost
- **Multi-commodity Flow**: Multiple flows in same network
- **Circulation Problems**: Flow conservation constraints

#### **2. Network Design Problems**
- **Network Planning**: Design efficient networks
- **Bandwidth Allocation**: Allocate bandwidth optimally
- **Traffic Engineering**: Optimize network traffic
- **Resource Allocation**: Allocate network resources

#### **3. Optimization Problems**
- **Linear Programming**: LP formulation of flow problems
- **Integer Programming**: Integer solutions for flow
- **Multi-objective Optimization**: Optimize multiple objectives
- **Dynamic Programming**: Handle dynamic updates

#### **4. Graph Theory Problems**
- **Connectivity**: Study of network connectivity
- **Cut Problems**: Find minimum/maximum cuts
- **Path Problems**: Find optimal paths
- **Matching Problems**: Find optimal matchings

#### **5. Algorithmic Techniques**
- **Ford-Fulkerson**: Maximum flow algorithm
- **Dinic's Algorithm**: Faster maximum flow algorithm
- **Push-Relabel**: Another maximum flow approach
- **Menger's Theorem**: Relates connectivity to disjoint paths

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Networks**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    connections = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        connections.append((a, b, c))
    
    result = download_speed(n, connections)
    print(result)
```

#### **2. Range Queries on Download Speed**
```python
def range_download_speed_queries(n, connections, queries):
    # queries = [(start_connection, end_connection), ...] - find max flow using connections in range
    
    results = []
    for start, end in queries: subset_connections = connections[
start: end+1]
        result = download_speed(n, subset_connections)
        results.append(result)
    
    return results
```

#### **3. Interactive Download Speed Problems**
```python
def interactive_download_speed():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter connections (a b capacity):")
    connections = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        connections.append((a, b, c))
    
    result = download_speed(n, connections)
    print(f"Maximum download speed: {result}")
    
    # Show the flow
    flow_edges = find_flow_edges(n, connections)
    print(f"Flow edges: {flow_edges}")
```

### 🧮 **Mathematical Extensions**

#### **1. Network Theory**
- **Flow Theory**: Mathematical theory of flows
- **Network Topology**: Study of network structure
- **Connectivity Theory**: Theory of network connectivity
- **Cut Theory**: Theory of cuts in networks

#### **2. Linear Programming**
- **Flow LP**: Linear programming formulation of flow
- **Dual Problems**: Dual of flow problems
- **Integer Programming**: Integer solutions for flow
- **Multi-commodity Flow**: Multiple commodities

#### **3. Optimization Theory**
- **Network Optimization**: Optimize network performance
- **Resource Optimization**: Optimize resource allocation
- **Traffic Optimization**: Optimize traffic flow
- **Cost Optimization**: Optimize network costs

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Flow Algorithms**: Ford-Fulkerson, Dinic's, Push-Relabel
- **Network Algorithms**: Connectivity, path finding algorithms
- **Optimization Algorithms**: Linear programming, integer programming
- **Graph Algorithms**: Various graph algorithms

#### **2. Mathematical Concepts**
- **Network Theory**: Properties and theorems about networks
- **Linear Algebra**: Matrix representations of networks
- **Optimization**: Mathematical optimization techniques
- **Graph Theory**: Theory of graphs and networks

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Flow Networks**: Representing flow problems
- **Residual Graphs**: Building residual graphs
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient network flow techniques and shows various extensions for download speed problems.* 