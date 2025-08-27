# CSES Strongly Connected Components - Problem Analysis

## Problem Statement
Given a directed graph with n nodes and m edges, find all strongly connected components (SCCs). A strongly connected component is a subset of vertices where every vertex is reachable from every other vertex in the component.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge from node a to node b.

### Output
Print the number of SCCs and the nodes in each component.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 5
1 2
2 3
3 1
3 4
4 5

Output:
3
1 2 3
4
5
```

## Solution Progression

### Approach 1: Kosaraju's Algorithm - O(n + m)
**Description**: Use Kosaraju's algorithm to find strongly connected components.

```python
def strongly_connected_components_naive(n, m, edges):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS to get finish times
    visited = [False] * (n + 1)
    finish_order = []
    
    def dfs1(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs1(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            dfs1(i)
    
    # Second DFS on reversed graph
    visited = [False] * (n + 1)
    sccs = []
    
    def dfs2(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                dfs2(neighbor, component)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            dfs2(node, component)
            sccs.append(component)
    
    return sccs
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Kosaraju's Algorithm - O(n + m)
**Description**: Use optimized Kosaraju's algorithm with better structure.

```python
def strongly_connected_components_optimized(n, m, edges):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    sccs = []
    
    def second_dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, component)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            second_dfs(node, component)
            sccs.append(component)
    
    return sccs
```

**Why this improvement works**: We use Kosaraju's algorithm which involves two DFS traversals: first to get topological order, then on the reversed graph to find SCCs.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_strongly_connected_components(n, m, edges):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    sccs = []
    
    def second_dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, component)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            second_dfs(node, component)
            sccs.append(component)
    
    return sccs

result = find_strongly_connected_components(n, m, edges)
print(len(result))
for component in result:
    print(*component)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Kosaraju's Algorithm | O(n + m) | O(n + m) | Use two DFS traversals |
| Optimized Kosaraju's | O(n + m) | O(n + m) | Better structure and clarity |

## Key Insights for Other Problems

### 1. **Strongly Connected Components**
**Principle**: Use Kosaraju's algorithm to find all strongly connected components in a directed graph.
**Applicable to**: Graph problems, component problems, connectivity problems

### 2. **Kosaraju's Algorithm**
**Principle**: Use two DFS traversals to find SCCs: first for topological order, second on reversed graph.
**Applicable to**: SCC problems, graph decomposition problems, connectivity problems

### 3. **Graph Decomposition**
**Principle**: Decompose directed graphs into strongly connected components for analysis.
**Applicable to**: Graph analysis problems, component problems, connectivity problems

## Notable Techniques

### 1. **Kosaraju's Algorithm Implementation**
```python
def kosaraju_algorithm(n, edges):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS for topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS for SCCs
    visited = [False] * (n + 1)
    sccs = []
    
    def second_dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, component)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            second_dfs(node, component)
            sccs.append(component)
    
    return sccs
```

### 2. **Adjacency List Construction**
```python
def build_adjacency_lists(edges, n):
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    return adj, adj_rev
```

### 3. **DFS Traversal**
```python
def dfs_traversal(adj, start, visited):
    stack = [start]
    visited[start] = True
    component = []
    
    while stack:
        node = stack.pop()
        component.append(node)
        
        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)
    
    return component
```

## Problem-Solving Framework

1. **Identify problem type**: This is a strongly connected components problem
2. **Choose approach**: Use Kosaraju's algorithm
3. **Build graphs**: Create adjacency lists for original and reversed graphs
4. **First DFS**: Get topological order of nodes
5. **Second DFS**: Find SCCs using reversed graph
6. **Process results**: Collect all components
7. **Return result**: Output number and nodes in each SCC

---

*This analysis shows how to efficiently find strongly connected components using Kosaraju's algorithm.* 