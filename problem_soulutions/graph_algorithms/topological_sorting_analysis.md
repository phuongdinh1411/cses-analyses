# CSES Topological Sorting - Problem Analysis

## Problem Statement
Given a directed acyclic graph (DAG) with n nodes and m edges, find a topological ordering of the nodes. A topological ordering is a linear ordering of vertices such that for every directed edge (u, v), vertex u comes before vertex v in the ordering.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge from node a to node b.

### Output
Print a valid topological ordering of the nodes.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 4
1 2
2 3
1 3
4 5

Output:
1 4 2 5 3
```

## Solution Progression

### Approach 1: DFS with Finish Times - O(n + m)
**Description**: Use DFS to get topological ordering based on finish times.

```python
def topological_sorting_naive(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
    
    return finish_order[::-1]
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Kahn's Algorithm - O(n + m)
**Description**: Use Kahn's algorithm (BFS-based) for topological sorting.

```python
from collections import deque

def topological_sorting_optimized(n, m, edges):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return topo_order
```

**Why this improvement works**: We use Kahn's algorithm which processes nodes in order of their in-degrees, ensuring topological ordering.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_topological_sorting(n, m, edges):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return topo_order

result = find_topological_sorting(n, m, edges)
print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS with Finish Times | O(n + m) | O(n) | Use DFS to get finish order |
| Kahn's Algorithm | O(n + m) | O(n) | Use BFS with in-degree tracking |

## Key Insights for Other Problems

### 1. **Topological Sorting**
**Principle**: Use Kahn's algorithm or DFS to find topological ordering of DAG nodes.
**Applicable to**: DAG problems, ordering problems, dependency problems

### 2. **Kahn's Algorithm**
**Principle**: Process nodes in order of their in-degrees to ensure topological ordering.
**Applicable to**: Topological sorting problems, dependency resolution problems

### 3. **In-Degree Tracking**
**Principle**: Track in-degrees of nodes to determine processing order in DAGs.
**Applicable to**: DAG problems, dependency problems, ordering problems

## Notable Techniques

### 1. **Kahn's Algorithm Implementation**
```python
def kahns_algorithm(n, edges):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Process nodes with zero in-degree
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return topo_order
```

### 2. **In-Degree Calculation**
```python
def calculate_in_degrees(edges, n):
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        in_degree[b] += 1
    
    return in_degree
```

### 3. **DFS Topological Sort**
```python
def dfs_topological_sort(adj, n):
    visited = [False] * (n + 1)
    finish_order = []
    
    def dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
    
    return finish_order[::-1]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a topological sorting problem
2. **Choose approach**: Use Kahn's algorithm or DFS
3. **Build graph**: Create adjacency list and calculate in-degrees
4. **Initialize queue**: Add nodes with zero in-degree
5. **Process nodes**: Remove nodes and update in-degrees
6. **Build order**: Collect nodes in topological order
7. **Return result**: Output topological ordering

---

*This analysis shows how to efficiently find topological ordering using Kahn's algorithm.* 