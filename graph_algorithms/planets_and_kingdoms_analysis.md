# CSES Planets and Kingdoms - Problem Analysis

## Problem Statement
Given a directed graph with n planets and m teleporters, find all strongly connected components (kingdoms) and assign each planet to a kingdom.

### Input
The first input line has two integers n and m: the number of planets and teleporters.
Then there are m lines describing the teleporters. Each line has two integers a and b: there is a teleporter from planet a to planet b.

### Output
Print the number of kingdoms and then for each planet, print which kingdom it belongs to.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 4
1 2
2 3
3 1
4 1

Output:
2
1 1 1 2
```

## Solution Progression

### Approach 1: Kosaraju's Algorithm - O(n + m)
**Description**: Use Kosaraju's algorithm to find strongly connected components.

```python
def planets_and_kingdoms_naive(n, m, teleporters):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in teleporters:
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
    kingdom_id = [0] * (n + 1)
    current_kingdom = 0
    
    def second_dfs(node, kingdom):
        visited[node] = True
        kingdom_id[node] = kingdom
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, kingdom)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_kingdom += 1
            second_dfs(node, current_kingdom)
    
    return current_kingdom, kingdom_id[1:n+1]
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Kosaraju's Algorithm - O(n + m)
**Description**: Use optimized Kosaraju's algorithm with better structure.

```python
def planets_and_kingdoms_optimized(n, m, teleporters):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in teleporters:
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
    kingdom_id = [0] * (n + 1)
    current_kingdom = 0
    
    def second_dfs(node, kingdom):
        visited[node] = True
        kingdom_id[node] = kingdom
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, kingdom)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_kingdom += 1
            second_dfs(node, current_kingdom)
    
    return current_kingdom, kingdom_id[1:n+1]
```

**Why this improvement works**: We use Kosaraju's algorithm with optimized structure to find strongly connected components efficiently.

## Final Optimal Solution

```python
n, m = map(int, input().split())
teleporters = []
for _ in range(m):
    a, b = map(int, input().split())
    teleporters.append((a, b))

def find_planets_and_kingdoms(n, m, teleporters):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in teleporters:
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
    kingdom_id = [0] * (n + 1)
    current_kingdom = 0
    
    def second_dfs(node, kingdom):
        visited[node] = True
        kingdom_id[node] = kingdom
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, kingdom)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_kingdom += 1
            second_dfs(node, current_kingdom)
    
    return current_kingdom, kingdom_id[1:n+1]

num_kingdoms, kingdoms = find_planets_and_kingdoms(n, m, teleporters)
print(num_kingdoms)
print(*kingdoms)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Kosaraju's Algorithm | O(n + m) | O(n + m) | Use Kosaraju's for strongly connected components |
| Optimized Kosaraju's | O(n + m) | O(n + m) | Optimized Kosaraju's implementation |

## Key Insights for Other Problems

### 1. **Strongly Connected Components**
**Principle**: Use Kosaraju's or Tarjan's algorithm to find strongly connected components.
**Applicable to**: SCC problems, graph decomposition problems, connectivity problems

### 2. **Kosaraju's Algorithm**
**Principle**: Use two DFS passes to find strongly connected components.
**Applicable to**: SCC problems, graph problems, connectivity problems

### 3. **Graph Decomposition**
**Principle**: Decompose directed graph into strongly connected components.
**Applicable to**: Graph analysis problems, connectivity problems, optimization problems

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

### 2. **SCC Assignment**
```python
def assign_scc_ids(n, sccs):
    kingdom_id = [0] * (n + 1)
    for i, component in enumerate(sccs, 1):
        for node in component:
            kingdom_id[node] = i
    return kingdom_id
```

### 3. **Graph Reversal**
```python
def reverse_graph(adj):
    adj_rev = [[] for _ in range(len(adj))]
    for u in range(len(adj)):
        for v in adj[u]:
            adj_rev[v].append(u)
    return adj_rev
```

## Problem-Solving Framework

1. **Identify problem type**: This is a strongly connected components problem
2. **Choose approach**: Use Kosaraju's algorithm
3. **Build graph**: Create adjacency lists for original and reversed graph
4. **First DFS**: Get topological order of nodes
5. **Second DFS**: Find SCCs using reversed graph
6. **Assign kingdoms**: Map each node to its kingdom ID
7. **Return result**: Output number of kingdoms and assignments

---

*This analysis shows how to efficiently find strongly connected components using Kosaraju's algorithm.* 