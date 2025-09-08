---
layout: simple
title: "Police Chase - Minimum Cut Problem"
permalink: /problem_soulutions/graph_algorithms/police_chase_analysis
---

# Police Chase - Minimum Cut Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand minimum cut problems and network connectivity concepts
- Apply maximum flow algorithms to find minimum cuts using max-flow min-cut theorem
- Implement efficient minimum cut algorithms with proper flow network construction
- Optimize minimum cut solutions using flow algorithms and cut identification
- Handle edge cases in minimum cut problems (already disconnected, single edge cuts, multiple components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Maximum flow, minimum cut, max-flow min-cut theorem, flow networks, cut algorithms
- **Data Structures**: Flow networks, cut tracking, graph representations, flow data structures
- **Mathematical Concepts**: Graph theory, flow networks, cut theory, network connectivity, optimization
- **Programming Skills**: Flow algorithms, cut identification, graph connectivity, algorithm implementation
- **Related Problems**: Download Speed (maximum flow), School Dance (flow problems), Network connectivity

## Problem Description

**Problem**: Given a network with n computers and m connections, find the minimum number of connections that need to be cut to disconnect computer 1 from computer n.

This is a minimum cut problem where we need to find the minimum number of edges to remove to disconnect the source from the sink. We can solve this using maximum flow algorithms like Ford-Fulkerson or Dinic's algorithm.

**Input**: 
- First line: Two integers n and m (number of computers and connections)
- Next m lines: Two integers a and b (connection between computers a and b)

**Output**: 
- Minimum number of connections that need to be cut

**Constraints**:
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ 1000
- 1 ≤ a, b ≤ n
- Network is undirected
- Computers are numbered from 1 to n
- No self-loops or multiple edges between same pair of computers

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
- Network: 1-2-3-4, 1-3, 2-4
- To disconnect 1 from 4, we need to cut at least 2 connections
- One possible cut: remove edges (1,2) and (3,4)
- This disconnects computer 1 from computer 4

## Visual Example

### Input Network
```
Computers: 1, 2, 3, 4
Connections: (1,2), (2,3), (3,4), (1,3), (2,4)

Network representation:
1 ── 2 ── 3 ── 4
│    │    │
└────┼────┘
     └────┘
```

### Minimum Cut Algorithm Process
```
Step 1: Convert to flow network
- Source: 1, Sink: 4
- All edge capacities: 1
- Flow network:
  1 ──1── 2 ──1── 3 ──1── 4
  │    │    │
  └──1─┼──1─┘
       └──1─┘

Step 2: Find maximum flow

Path 1: 1 → 2 → 3 → 4
- Flow: 1
- Residual graph:
  1 ──0── 2 ──0── 3 ──0── 4
  │    │    │
  └──1─┼──1─┘
       └──1─┘

Path 2: 1 → 3 → 4
- Flow: 1
- Residual graph:
  1 ──0── 2 ──0── 3 ──0── 4
  │    │    │
  └──0─┼──0─┘
       └──1─┘

Step 3: No more augmenting paths
- Maximum flow: 2
- Minimum cut: 2
```

### Cut Analysis
```
Minimum cut edges:
1. (1,2) - cuts path 1 → 2 → 3 → 4
2. (3,4) - cuts path 1 → 3 → 4

After cutting these edges:
1 ── 2 ── 3 ── 4
│    │    │
└────┼────┘
     └────┘

Computer 1 is disconnected from computer 4.
```

### Key Insight
Minimum cut algorithm works by:
1. Converting to flow network with unit capacities
2. Finding maximum flow using Ford-Fulkerson
3. Minimum cut = maximum flow (Max-Flow Min-Cut theorem)
4. Time complexity: O(m × f) where f is maximum flow
5. Space complexity: O(n + m) for graph representation

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Cut Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of edges to cut
- Check if each combination disconnects source from sink
- Simple but computationally expensive approach
- Not suitable for large graphs

**Algorithm:**
1. Generate all possible combinations of edges
2. For each combination, remove edges and check connectivity
3. Find the minimum size combination that disconnects source from sink
4. Return the minimum cut size

**Visual Example:**
```
Brute force: Try all possible edge combinations
For network: 1 ── 2 ── 3 ── 4
             │    │    │
             └────┼────┘
                  └────┘

All possible edge combinations:
- {1,2} → Check connectivity: 1 disconnected from 4? No
- {2,3} → Check connectivity: 1 disconnected from 4? No
- {3,4} → Check connectivity: 1 disconnected from 4? No
- {1,3} → Check connectivity: 1 disconnected from 4? No
- {2,4} → Check connectivity: 1 disconnected from 4? No
- {1,2, 2,3} → Check connectivity: 1 disconnected from 4? Yes
- {1,2, 3,4} → Check connectivity: 1 disconnected from 4? Yes
- {2,3, 3,4} → Check connectivity: 1 disconnected from 4? Yes
- ... and so on

Minimum cut size: 2
```

**Implementation:**
```python
def police_chase_brute_force(n, m, connections):
    from itertools import combinations
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    edges = []
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        edges.append((a, b))
    
    def is_connected(source, sink, removed_edges):
        # Check if source and sink are connected after removing edges
        visited = [False] * (n + 1)
        stack = [source]
        visited[source] = True
        
        while stack:
            current = stack.pop()
            if current == sink:
                return True
            
            for next_node in adj[current]:
                if (not visited[next_node] and 
                    (current, next_node) not in removed_edges and
                    (next_node, current) not in removed_edges):
                    visited[next_node] = True
                    stack.append(next_node)
        
        return False
    
    min_cut = float('inf')
    
    # Try all possible combinations of edges
    for k in range(1, len(edges) + 1):
        for edge_combination in combinations(edges, k):
            if not is_connected(1, n, set(edge_combination)):
                min_cut = min(min_cut, len(edge_combination))
    
    return min_cut
```

**Time Complexity:** O(2^m × (n + m)) for checking all combinations
**Space Complexity:** O(n + m) for graph representation

**Why it's inefficient:**
- Exponential time complexity O(2^m)
- Not suitable for large graphs
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: Ford-Fulkerson Algorithm (Better)

**Key Insights from Ford-Fulkerson Solution:**
- Use maximum flow to find minimum cut using Max-Flow Min-Cut theorem
- Convert minimum cut problem to maximum flow problem
- Much more efficient than brute force approach
- Standard method for minimum cut problems

**Algorithm:**
1. Convert graph to flow network with unit capacities
2. Use Ford-Fulkerson algorithm to find maximum flow
3. Minimum cut = maximum flow (Max-Flow Min-Cut theorem)
4. Return the maximum flow value

**Visual Example:**
```
Ford-Fulkerson algorithm for network: 1 ── 2 ── 3 ── 4
                                        │    │    │
                                        └────┼────┘
                                             └────┘

Step 1: Convert to flow network
- Source: 1, Sink: 4
- All edge capacities: 1
- Flow network:
  1 ──1── 2 ──1── 3 ──1── 4
  │    │    │
  └──1─┼──1─┘
       └──1─┘

Step 2: Find maximum flow

Path 1: 1 → 2 → 3 → 4
- Flow: 1
- Residual graph:
  1 ──0── 2 ──0── 3 ──0── 4
  │    │    │
  └──1─┼──1─┘
       └──1─┘

Path 2: 1 → 3 → 4
- Flow: 1
- Residual graph:
  1 ──0── 2 ──0── 3 ──0── 4
  │    │    │
  └──0─┼──0─┘
       └──1─┘

Step 3: No more augmenting paths
- Maximum flow: 2
- Minimum cut: 2
```

**Implementation:**
```python
def police_chase_ford_fulkerson(n, m, connections):
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        capacity[b][a] = 1  # Undirected graph
    
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
- Standard method for minimum cut problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Edmonds-Karp Algorithm (Optimal)

**Key Insights from Edmonds-Karp Solution:**
- Use BFS to find shortest augmenting paths
- Guarantees O(n × m²) time complexity
- Most efficient approach for minimum cut problems
- Standard method in competitive programming

**Algorithm:**
1. Convert graph to flow network with unit capacities
2. Use Edmonds-Karp algorithm to find maximum flow
3. Minimum cut = maximum flow (Max-Flow Min-Cut theorem)
4. Return the maximum flow value

**Visual Example:**
```
Edmonds-Karp algorithm for network: 1 ── 2 ── 3 ── 4
                                      │    │    │
                                      └────┼────┘
                                           └────┘

Step 1: Convert to flow network
- Source: 1, Sink: 4
- All edge capacities: 1
- Flow network:
  1 ──1── 2 ──1── 3 ──1── 4
  │    │    │
  └──1─┼──1─┘
       └──1─┘

Step 2: Find shortest augmenting paths using BFS

Path 1: 1 → 2 → 3 → 4 (length 3)
- Flow: 1
- Residual graph:
  1 ──0── 2 ──0── 3 ──0── 4
  │    │    │
  └──1─┼──1─┘
       └──1─┘

Path 2: 1 → 3 → 4 (length 2)
- Flow: 1
- Residual graph:
  1 ──0── 2 ──0── 3 ──0── 4
  │    │    │
  └──0─┼──0─┘
       └──1─┘

Step 3: No more augmenting paths
- Maximum flow: 2
- Minimum cut: 2
```

**Implementation:**
```python
def police_chase_edmonds_karp(n, m, connections):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        capacity[b][a] = 1  # Undirected graph
    
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

def solve_police_chase():
    n, m = map(int, input().split())
    connections = []
    for _ in range(m):
        a, b = map(int, input().split())
        connections.append((a, b))
    
    result = police_chase_edmonds_karp(n, m, connections)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_police_chase()
```

**Time Complexity:** O(n × m²) for Edmonds-Karp algorithm
**Space Complexity:** O(n + m) for graph representation

**Why it's optimal:**
- O(n × m²) time complexity is optimal for maximum flow
- Uses BFS to find shortest augmenting paths
- Most efficient approach for competitive programming
- Standard method for minimum cut problems

## 🎯 Problem Variations

### Variation 1: Minimum Cut with Different Edge Capacities
**Problem**: Find minimum cut with different edge capacities.

**Link**: [CSES Problem Set - Minimum Cut with Capacities](https://cses.fi/problemset/task/minimum_cut_capacities)

```python
def police_chase_capacities(n, m, connections, capacities):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i, (a, b) in enumerate(connections):
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = capacities[i]
        capacity[b][a] = capacities[i]  # Undirected graph
    
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

### Variation 2: Minimum Cut with Multiple Sources and Sinks
**Problem**: Find minimum cut with multiple sources and sinks.

**Link**: [CSES Problem Set - Minimum Cut Multiple Sources](https://cses.fi/problemset/task/minimum_cut_multiple_sources)

```python
def police_chase_multiple_sources(n, m, connections, sources, sinks):
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
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        capacity[b][a] = 1  # Undirected graph
    
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

### Variation 3: Minimum Cut with Node Capacities
**Problem**: Find minimum cut with node capacities instead of edge capacities.

**Link**: [CSES Problem Set - Minimum Cut Node Capacities](https://cses.fi/problemset/task/minimum_cut_node_capacities)

```python
def police_chase_node_capacities(n, m, connections, node_capacities):
    from collections import deque
    
    # Split each node into two nodes (in and out)
    # Node i becomes i_in and i_out
    # Add edge from i_in to i_out with capacity node_capacities[i]
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(2 * n + 1)]
    capacity = [[0] * (2 * n + 1) for _ in range(2 * n + 1)]
    
    # Add edges from i_in to i_out
    for i in range(1, n + 1):
        adj[i].append(i + n)
        adj[i + n].append(i)
        capacity[i][i + n] = node_capacities[i]
    
    # Add original edges (from i_out to j_in)
    for a, b in connections:
        adj[a + n].append(b)
        adj[b].append(a + n)
        capacity[a + n][b] = float('inf')
        capacity[b][a + n] = float('inf')
    
    def bfs(source, sink):
        # Find shortest augmenting path using BFS
        parent = [-1] * (2 * n + 1)
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
        flow = bfs(1, n + n)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

## 🔗 Related Problems

- **[Download Speed](/cses-analyses/problem_soulutions/graph_algorithms/download_speed_analysis/)**: Maximum flow problems
- **[Distinct Routes](/cses-analyses/problem_soulutions/graph_algorithms/distinct_routes_analysis/)**: Edge-disjoint paths problems
- **[School Dance](/cses-analyses/problem_soulutions/graph_algorithms/school_dance_analysis/)**: Bipartite matching problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Minimum Cut**: Essential for analyzing network connectivity and reliability
2. **Max-Flow Min-Cut Theorem**: Key theoretical foundation for flow problems
3. **Flow Networks**: Important data structure for flow problems
4. **Residual Graphs**: Critical for flow algorithm implementation
5. **Augmenting Paths**: Foundation for maximum flow algorithms
6. **Network Optimization**: Foundation for many real-world problems

## 📝 Summary

The Police Chase problem demonstrates fundamental minimum cut concepts for analyzing network connectivity. We explored three approaches:

1. **Brute Force Cut Enumeration**: O(2^m × (n + m)) time complexity using exhaustive search, inefficient for large graphs
2. **Ford-Fulkerson Algorithm**: O(m × f) time complexity using augmenting paths, better approach for flow problems
3. **Edmonds-Karp Algorithm**: O(n × m²) time complexity using BFS for shortest paths, optimal approach for minimum cut

The key insights include understanding minimum cut as maximum flow problems, using the Max-Flow Min-Cut theorem, and applying augmenting path algorithms for efficient flow computation. This problem serves as an excellent introduction to minimum cut algorithms and network optimization techniques.

