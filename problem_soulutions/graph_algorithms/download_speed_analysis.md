# CSES Download Speed - Problem Analysis

## Problem Statement
Given a network with n computers and m connections, find the maximum download speed from computer 1 to computer n. Each connection has a capacity.

### Input
The first input line has two integers n and m: the number of computers and connections.
Then there are m lines describing the connections. Each line has three integers a, b, and c: there is a connection from computer a to computer b with capacity c.

### Output
Print the maximum download speed from computer 1 to computer n.

### Constraints
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ 1000
- 1 ≤ a,b ≤ n
- 1 ≤ c ≤ 10^9

### Example
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

## Solution Progression

### Approach 1: Ford-Fulkerson Algorithm - O(n * m * max_flow)
**Description**: Use Ford-Fulkerson algorithm to find maximum flow.

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

## Final Optimal Solution

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

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Ford-Fulkerson | O(n * m * max_flow) | O(n²) | Use Ford-Fulkerson for maximum flow |
| Optimized Ford-Fulkerson | O(n * m * max_flow) | O(n²) | Optimized Ford-Fulkerson implementation |

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