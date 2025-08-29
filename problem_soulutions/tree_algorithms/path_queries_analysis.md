---
layout: simple
title: "Path Queries"
permalink: /problem_soulutions/tree_algorithms/path_queries_analysis
---


# Path Queries

## Problem Statement
Given a tree with n nodes, each node has a value. Process q queries. Each query asks for the sum of values on the path between two nodes.

### Input
The first input line has two integers n and q: the number of nodes and the number of queries.
The second line has n integers x1,x2,…,xn: the values of the nodes.
Then there are n-1 lines describing the edges. Each line has two integers a and b: an edge between nodes a and b.
Finally, there are q lines describing the queries. Each line has two integers a and b: the path between nodes a and b.

### Output
Print the answer to each query.

### Constraints
- 1 ≤ n,q ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 3
1 2 3 4 5
1 2
1 3
2 4
2 5
1 4
2 3
4 5

Output:
7
4
11
```

## Solution Progression

### Approach 1: Find Path for Each Query - O(q × n)
**Description**: For each query, find the path between the two nodes and calculate the sum.

```python
def path_queries_naive(n, values, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    def find_path_sum(a, b):
        # Find path using BFS
        visited = [False] * (n + 1)
        parent = [-1] * (n + 1)
        queue = [a]
        visited[a] = True
        
        while queue:
            current = queue.pop(0)
            if current == b:
                break
            
            for neighbor in adj[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        # Reconstruct path and calculate sum
        path = []
        current = b
        while current != -1:
            path.append(current)
            current = parent[current]
        
        path.reverse()
        return sum(values[node] for node in path)
    
    results = []
    for a, b in queries:
        sum_val = find_path_sum(a, b)
        results.append(sum_val)
    
    return results
```

**Why this is inefficient**: For each query, we need to find the path between two nodes, leading to O(q × n) time complexity.

### Improvement 1: LCA with Path Decomposition - O(n log n + q log n)
**Description**: Use Lowest Common Ancestor (LCA) to decompose paths and calculate sums efficiently.

```python
def path_queries_lca(n, values, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    # Build parent and depth arrays
    parent = [-1] * (n + 1)
    depth = [0] * (n + 1)
    
    def dfs(node, p, d):
        parent[node] = p
        depth[node] = d
        
        for child in adj[node]:
            if child != p:
                dfs(child, node, d + 1)
    
    # Start DFS from root (node 1)
    dfs(1, -1, 0)
    
    # Build LCA using binary lifting
    log_n = 20
    ancestor = [[-1] * log_n for _ in range(n + 1)]
    
    # Initialize first level
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(1, n + 1):
            if ancestor[i][j-1] != -1:
                ancestor[i][j] = ancestor[ancestor[i][j-1]][j-1]
    
    def lca(u, v):
        # Make sure u is deeper
        if depth[u] < depth[v]:
            u, v = v, u
        
        # Bring u to same level as v
        diff = depth[u] - depth[v]
        for i in range(log_n):
            if diff & (1 << i):
                u = ancestor[u][i]
        
        if u == v:
            return u
        
        # Find LCA
        for i in range(log_n - 1, -1, -1):
            if ancestor[u][i] != ancestor[v][i]:
                u = ancestor[u][i]
                v = ancestor[v][i]
        
        return parent[u]
    
    def path_sum(a, b):
        lca_node = lca(a, b)
        
        # Calculate sum from a to LCA
        sum_a_to_lca = 0
        current = a
        while current != lca_node:
            sum_a_to_lca += values[current]
            current = parent[current]
        sum_a_to_lca += values[lca_node]
        
        # Calculate sum from b to LCA
        sum_b_to_lca = 0
        current = b
        while current != lca_node:
            sum_b_to_lca += values[current]
            current = parent[current]
        
        return sum_a_to_lca + sum_b_to_lca
    
    results = []
    for a, b in queries:
        sum_val = path_sum(a, b)
        results.append(sum_val)
    
    return results
```

**Why this improvement works**: Using LCA allows us to decompose any path into two paths from nodes to their LCA, making path sum calculation efficient.

## Final Optimal Solution

```python
n, q = map(int, input().split())
values = [0] + list(map(int, input().split()))

# Read edges
edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    edges.append((a, b))

# Read queries
queries = []
for _ in range(q):
    a, b = map(int, input().split())
    queries.append((a, b))

# Build adjacency list
adj = [[] for _ in range(n + 1)]
for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)

# Build parent and depth arrays
parent = [-1] * (n + 1)
depth = [0] * (n + 1)

def dfs(node, p, d):
    parent[node] = p
    depth[node] = d
    
    for child in adj[node]:
        if child != p:
            dfs(child, node, d + 1)

# Start DFS from root (node 1)
dfs(1, -1, 0)

# Build LCA using binary lifting
log_n = 20
ancestor = [[-1] * log_n for _ in range(n + 1)]

# Initialize first level
for i in range(1, n + 1):
    ancestor[i][0] = parent[i]

# Build binary lifting table
for j in range(1, log_n):
    for i in range(1, n + 1):
        if ancestor[i][j-1] != -1:
            ancestor[i][j] = ancestor[ancestor[i][j-1]][j-1]

def lca(u, v):
    # Make sure u is deeper
    if depth[u] < depth[v]:
        u, v = v, u
    
    # Bring u to same level as v
    diff = depth[u] - depth[v]
    for i in range(log_n):
        if diff & (1 << i):
            u = ancestor[u][i]
    
    if u == v:
        return u
    
    # Find LCA
    for i in range(log_n - 1, -1, -1):
        if ancestor[u][i] != ancestor[v][i]:
            u = ancestor[u][i]
            v = ancestor[v][i]
    
    return parent[u]

def path_sum(a, b):
    lca_node = lca(a, b)
    
    # Calculate sum from a to LCA
    sum_a_to_lca = 0
    current = a
    while current != lca_node:
        sum_a_to_lca += values[current]
        current = parent[current]
    sum_a_to_lca += values[lca_node]
    
    # Calculate sum from b to LCA
    sum_b_to_lca = 0
    current = b
    while current != lca_node:
        sum_b_to_lca += values[current]
        current = parent[current]
    
    return sum_a_to_lca + sum_b_to_lca

# Process queries
for a, b in queries:
    result = path_sum(a, b)
    print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(q × n) | O(n) | Find path for each query |
| LCA + Path Decomposition | O(n log n + q log n) | O(n log n) | Use LCA to decompose paths |

## Key Insights for Other Problems

### 1. **Path Query Problems**
**Principle**: Use LCA to decompose paths into manageable segments.
**Applicable to**: Tree problems, path problems, query problems

### 2. **Path Decomposition**
**Principle**: Break any path into two paths from nodes to their LCA.
**Applicable to**: Tree problems, path analysis, query optimization

### 3. **Binary Lifting for LCA**
**Principle**: Use binary lifting to find LCA in O(log n) time.
**Applicable to**: Tree problems, LCA problems, binary lifting applications

## Notable Techniques

### 1. **LCA with Binary Lifting**
```python
def build_lca_table(n, parent):
    log_n = 20
    ancestor = [[-1] * log_n for _ in range(n + 1)]
    
    # Initialize first level
    for i in range(1, n + 1):
        ancestor[i][0] = parent[i]
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(1, n + 1):
            if ancestor[i][j-1] != -1:
                ancestor[i][j] = ancestor[ancestor[i][j-1]][j-1]
    
    return ancestor
```

### 2. **Path Sum Calculation**
```python
def calculate_path_sum(a, b, lca_node, values, parent):
    # Calculate sum from a to LCA
    sum_a_to_lca = 0
    current = a
    while current != lca_node:
        sum_a_to_lca += values[current]
        current = parent[current]
    sum_a_to_lca += values[lca_node]
    
    # Calculate sum from b to LCA
    sum_b_to_lca = 0
    current = b
    while current != lca_node:
        sum_b_to_lca += values[current]
        current = parent[current]
    
    return sum_a_to_lca + sum_b_to_lca
```

### 3. **Path Decomposition**
```python
def decompose_path(a, b, lca_func):
    lca_node = lca_func(a, b)
    return (a, lca_node), (b, lca_node)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a path query problem in trees
2. **Choose approach**: Use LCA to decompose paths efficiently
3. **Build data structures**: Calculate depths and build LCA table
4. **Implement path decomposition**: Break paths into segments using LCA
5. **Process queries**: Calculate path sums using decomposed segments

---

*This analysis shows how to efficiently calculate path sums using LCA and path decomposition technique.*