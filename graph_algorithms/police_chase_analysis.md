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