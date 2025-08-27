# CSES Distinct Routes - Problem Analysis

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