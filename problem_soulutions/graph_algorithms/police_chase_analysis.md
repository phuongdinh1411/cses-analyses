# CSES Police Chase - Problem Analysis

## Problem Statement
Given a network with n computers and m connections, find the minimum number of connections that need to be cut to disconnect computer 1 from computer n.

### Input
The first input line has two integers n and m: the number of computers and connections.
Then there are m lines describing the connections. Each line has two integers a and b: there is a connection between computers a and b.

### Output
Print the minimum number of connections that need to be cut.

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

### Approach 1: Minimum Cut using Max Flow - O(n * m * max_flow)
**Description**: Use maximum flow to find minimum cut (Menger's theorem).

```python
def police_chase_naive(n, m, connections):
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

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Minimum Cut Algorithm - O(n * m * max_flow)
**Description**: Use optimized Ford-Fulkerson algorithm for minimum cut.

```python
def police_chase_optimized(n, m, connections):
    from collections import deque
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        capacity[b][a] = 1
    
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

**Why this improvement works**: We use optimized Ford-Fulkerson algorithm to find minimum cut efficiently.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
connections = []
for _ in range(m):
    a, b = map(int, input().split())
    connections.append((a, b))

def find_minimum_cut(n, m, connections):
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

result = find_minimum_cut(n, m, connections)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Minimum Cut via Max Flow | O(n * m * max_flow) | O(n²) | Use max flow to find minimum cut |
| Optimized Minimum Cut | O(n * m * max_flow) | O(n²) | Optimized max flow implementation |

## Key Insights for Other Problems

### 1. **Minimum Cut**
**Principle**: Use maximum flow to find minimum cut (Menger's theorem).
**Applicable to**: Cut problems, connectivity problems, network problems

### 2. **Menger's Theorem**
**Principle**: The minimum number of edges to disconnect two vertices equals the maximum number of edge-disjoint paths.
**Applicable to**: Connectivity problems, path problems, network problems

### 3. **Edge Connectivity**
**Principle**: Find minimum number of edges whose removal disconnects the graph.
**Applicable to**: Connectivity problems, network problems, graph problems

## Notable Techniques

### 1. **Minimum Cut via Max Flow**
```python
def minimum_cut_max_flow(n, adj, capacity, source, sink):
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

### 2. **Edge Capacity Assignment**
```python
def assign_edge_capacities(n, connections):
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        capacity[b][a] = 1
    
    return adj, capacity
```

### 3. **Connectivity Check**
```python
def check_connectivity(n, adj, source, sink):
    visited = [False] * (n + 1)
    queue = deque([source])
    visited[source] = True
    
    while queue:
        current = queue.popleft()
        for next_node in adj[current]:
            if not visited[next_node]:
                visited[next_node] = True
                queue.append(next_node)
    
    return visited[sink]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a minimum cut problem
2. **Choose approach**: Use maximum flow to find minimum cut
3. **Build graph**: Create adjacency list with unit capacities
4. **Apply Menger's theorem**: Use max flow to find minimum cut
5. **Find augmenting paths**: Use BFS to find paths with positive residual capacity
6. **Update flow**: Increase flow along augmenting paths
7. **Return result**: Output maximum flow (equals minimum cut)

---

*This analysis shows how to efficiently find minimum cut using maximum flow algorithm.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Police Chase with Edge Capacities**
**Problem**: Find minimum cut with different edge capacities (some roads are wider than others).
```python
def police_chase_with_capacities(n, connections, capacities):
    # capacities[(a, b)] = capacity of connection (a, b)
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        cap = capacities.get((a, b), 1)
        capacity[a][b] = cap
        capacity[b][a] = cap
    
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

#### **Variation 2: Police Chase with Node Capacities**
**Problem**: Find minimum node cut (nodes can only handle limited traffic).
```python
def police_chase_node_capacities(n, connections, node_capacities):
    # node_capacities[i] = capacity of node i
    
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
        capacity[in_node][out_node] = node_capacities.get(i, 1)
    
    # Add original edges (out_i -> in_j)
    for a, b in connections:
        out_a = n + a
        in_b = b
        adj[out_a].append(in_b)
        adj[in_b].append(out_a)
        capacity[out_a][in_b] = float('inf')  # Original edges have infinite capacity
    
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

#### **Variation 3: Police Chase with Costs**
**Problem**: Each connection has a cost, find minimum cut with minimum total cost.
```python
def cost_based_police_chase(n, connections, costs):
    # costs[(a, b)] = cost of blocking connection (a, b)
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        capacity[b][a] = 1
        cost[a][b] = costs.get((a, b), 0)
        cost[b][a] = cost[a][b]
    
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
    cut_size = 0
    
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
        
        cut_size += bottleneck
    
    return cut_size, total_cost
```

#### **Variation 4: Police Chase with Probabilities**
**Problem**: Each connection has a probability of being blocked, find expected minimum cut.
```python
def probabilistic_police_chase(n, connections, probabilities):
    # probabilities[(a, b)] = probability that connection (a, b) can be blocked
    
    adj = [[] for _ in range(n + 1)]
    capacity = [[0] * (n + 1) for _ in range(n + 1)]
    
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        capacity[b][a] = 1
    
    # For probabilistic connections, calculate expected minimum cut
    expected_cut = 0
    
    # Calculate expected cut based on connection probabilities
    for a, b in connections:
        if a == 1 or b == n:  # Direct connections from source or to sink
            prob = probabilities.get((a, b), 0.5)
            expected_cut += prob
    
    return expected_cut
```

#### **Variation 5: Police Chase with Multiple Targets**
**Problem**: Find minimum cut to separate multiple sources from multiple targets.
```python
def multi_target_police_chase(n, connections, sources, targets):
    # sources = list of source nodes, targets = list of target nodes
    
    # Create super source and super sink
    super_source = 0
    super_sink = n + 1
    
    adj = [[] for _ in range(n + 2)]
    capacity = [[0] * (n + 2) for _ in range(n + 2)]
    
    # Add original connections
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
        capacity[a][b] = 1
        capacity[b][a] = 1
    
    # Add edges from super source to sources
    for source in sources:
        adj[super_source].append(source)
        adj[source].append(super_source)
        capacity[super_source][source] = float('inf')
    
    # Add edges from targets to super sink
    for target in targets:
        adj[target].append(super_sink)
        adj[super_sink].append(target)
        capacity[target][super_sink] = float('inf')
    
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

#### **2. Connectivity Problems**
- **Edge Connectivity**: Minimum edges to disconnect graph
- **Node Connectivity**: Minimum nodes to disconnect graph
- **Strongly Connected Components**: Find strongly connected components
- **Biconnected Components**: Find biconnected components

#### **3. Cut Problems**
- **Minimum Cut**: Find minimum capacity cut
- **Maximum Cut**: Find maximum capacity cut
- **Multi-way Cut**: Separate multiple sets of nodes
- **Steiner Cut**: Cut with Steiner nodes

#### **4. Security Problems**
- **Network Security**: Protect networks from attacks
- **Access Control**: Control access to resources
- **Traffic Control**: Manage network traffic
- **Resource Protection**: Protect critical resources

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
        a, b = map(int, input().split())
        connections.append((a, b))
    
    result = police_chase_min_cut(n, connections)
    print(result)
```

#### **2. Range Queries on Police Chase**
```python
def range_police_chase_queries(n, connections, queries):
    # queries = [(source, target), ...] - find min cut between source and target
    
    results = []
    for source, target in queries:
        # Modify the graph to have source and target as specified
        result = police_chase_min_cut(n, connections, source, target)
        results.append(result)
    
    return results
```

#### **3. Interactive Police Chase Problems**
```python
def interactive_police_chase():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter connections (a b):")
    connections = []
    for _ in range(m):
        a, b = map(int, input().split())
        connections.append((a, b))
    
    result = police_chase_min_cut(n, connections)
    print(f"Minimum connections to block: {result}")
    
    # Show the cut
    cut_edges = find_minimum_cut_edges(n, connections)
    print(f"Edges to block: {cut_edges}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Menger's Theorem**: Maximum number of edge-disjoint paths equals minimum edge cut
- **Network Flow Theory**: Theory of flows in networks
- **Connectivity Theory**: Study of graph connectivity
- **Cut Theory**: Theory of cuts in graphs

#### **2. Linear Programming**
- **Network Flow LP**: Linear programming formulation of network flow
- **Dual Problems**: Dual of maximum flow is minimum cut
- **Integer Programming**: Integer solutions for flow problems
- **Multi-commodity Flow**: Multiple commodities in network

#### **3. Security Analysis**
- **Network Vulnerability**: Analyze network vulnerabilities
- **Attack Modeling**: Model different types of attacks
- **Defense Strategies**: Develop defense strategies
- **Risk Assessment**: Assess security risks

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Network Flow**: Ford-Fulkerson, Dinic's, Push-Relabel algorithms
- **Graph Algorithms**: BFS, DFS, connectivity algorithms
- **Security Algorithms**: Intrusion detection, access control
- **Optimization Algorithms**: Linear programming, integer programming

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Linear Algebra**: Matrix representations of graphs
- **Optimization**: Linear programming for network problems
- **Security Theory**: Mathematical foundations of security

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Flow Networks**: Representing flow problems
- **Cut Reconstruction**: Finding actual cuts from flow
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient network flow techniques and shows various extensions for police chase problems.* 