# CSES Strongly Connected Edges - Problem Analysis

## Problem Statement
Given a directed graph with n nodes and m edges, find the minimum number of edges to add to make the graph strongly connected.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge from node a to node b.

### Output
Print the minimum number of edges to add.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 2
1 2
3 4

Output:
2
```

## Solution Progression

### Approach 1: Naive Strongly Connected Components - O(n + m)
**Description**: Use Kosaraju's algorithm to find strongly connected components and count needed edges.

```python
def strongly_connected_edges_naive(n, m, edges):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # Kosaraju's algorithm
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    # First DFS to get finish order
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS to find SCCs
    visited = [False] * (n + 1)
    scc_id = [0] * (n + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            second_dfs(node, current_scc)
            current_scc += 1
    
    # Count SCCs
    return current_scc - 1  # Need to connect all SCCs
```

**Why this is inefficient**: This approach doesn't correctly calculate the minimum edges needed.

### Improvement 1: Condensation Graph Analysis - O(n + m)
**Description**: Build condensation graph and analyze in/out degrees to find minimum edges needed.

```python
def strongly_connected_edges_condensation(n, m, edges):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # Kosaraju's algorithm to find SCCs
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
    
    visited = [False] * (n + 1)
    scc_id = [0] * (n + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            second_dfs(node, current_scc)
            current_scc += 1
    
    # Build condensation graph
    condensation_adj = [[] for _ in range(current_scc)]
    in_degree = [0] * current_scc
    out_degree = [0] * current_scc
    
    for a, b in edges:
        scc_a = scc_id[a]
        scc_b = scc_id[b]
        if scc_a != scc_b:
            condensation_adj[scc_a].append(scc_b)
            in_degree[scc_b] += 1
            out_degree[scc_a] += 1
    
    # Count sources and sinks
    sources = sum(1 for i in range(current_scc) if in_degree[i] == 0)
    sinks = sum(1 for i in range(current_scc) if out_degree[i] == 0)
    
    # If only one SCC, no edges needed
    if current_scc == 1:
        return 0
    
    # Minimum edges needed = max(sources, sinks)
    return max(sources, sinks)
```

**Why this improvement works**: Uses condensation graph analysis to find the minimum edges needed to make the graph strongly connected.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_minimum_edges_to_add(n, m, edges):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # Kosaraju's algorithm to find SCCs
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
    
    visited = [False] * (n + 1)
    scc_id = [0] * (n + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            second_dfs(node, current_scc)
            current_scc += 1
    
    # Build condensation graph
    condensation_adj = [[] for _ in range(current_scc)]
    in_degree = [0] * current_scc
    out_degree = [0] * current_scc
    
    for a, b in edges:
        scc_a = scc_id[a]
        scc_b = scc_id[b]
        if scc_a != scc_b:
            condensation_adj[scc_a].append(scc_b)
            in_degree[scc_b] += 1
            out_degree[scc_a] += 1
    
    # Count sources and sinks
    sources = sum(1 for i in range(current_scc) if in_degree[i] == 0)
    sinks = sum(1 for i in range(current_scc) if out_degree[i] == 0)
    
    # If only one SCC, no edges needed
    if current_scc == 1:
        return 0
    
    # Minimum edges needed = max(sources, sinks)
    return max(sources, sinks)

result = find_minimum_edges_to_add(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive SCC | O(n + m) | O(n) | Simple SCC counting |
| Condensation Graph | O(n + m) | O(n) | Analysis of condensation graph |

## Key Insights for Other Problems

### 1. **Strongly Connected Components**
**Principle**: A graph is strongly connected if every node can reach every other node.
**Applicable to**: Connectivity problems, graph analysis problems, network problems

### 2. **Condensation Graph**
**Principle**: The condensation graph of SCCs is always a DAG and helps analyze connectivity.
**Applicable to**: Graph analysis problems, connectivity problems, network problems

### 3. **Sources and Sinks Analysis**
**Principle**: The minimum edges needed equals the maximum of sources and sinks in the condensation graph.
**Applicable to**: Connectivity problems, graph optimization problems, network problems

## Notable Techniques

### 1. **Kosaraju's Algorithm**
```python
def kosaraju_algorithm(n, adj):
    # Build reverse adjacency list
    adj_rev = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for neighbor in adj[i]:
            adj_rev[neighbor].append(i)
    
    # First DFS to get finish order
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
    
    # Second DFS to find SCCs
    visited = [False] * (n + 1)
    scc_id = [0] * (n + 1)
    current_scc = 0
    
    def second_dfs(node, scc):
        visited[node] = True
        scc_id[node] = scc
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, scc)
    
    for node in reversed(finish_order):
        if not visited[node]:
            second_dfs(node, current_scc)
            current_scc += 1
    
    return scc_id, current_scc
```

### 2. **Condensation Graph Construction**
```python
def build_condensation_graph(n, edges, scc_id, num_sccs):
    condensation_adj = [[] for _ in range(num_sccs)]
    in_degree = [0] * num_sccs
    out_degree = [0] * num_sccs
    
    for a, b in edges:
        scc_a = scc_id[a]
        scc_b = scc_id[b]
        if scc_a != scc_b:
            condensation_adj[scc_a].append(scc_b)
            in_degree[scc_b] += 1
            out_degree[scc_a] += 1
    
    return condensation_adj, in_degree, out_degree
```

### 3. **Sources and Sinks Counting**
```python
def count_sources_and_sinks(num_sccs, in_degree, out_degree):
    sources = sum(1 for i in range(num_sccs) if in_degree[i] == 0)
    sinks = sum(1 for i in range(num_sccs) if out_degree[i] == 0)
    return sources, sinks
```

## Problem-Solving Framework

1. **Identify problem type**: This is a strongly connected components problem
2. **Choose approach**: Use Kosaraju's algorithm to find SCCs
3. **Initialize data structure**: Build adjacency lists and reverse adjacency list
4. **Find SCCs**: Use Kosaraju's algorithm with two DFS passes
5. **Build condensation graph**: Create DAG of SCCs
6. **Analyze degrees**: Count sources and sinks in condensation graph
7. **Return result**: Output minimum edges needed (max of sources and sinks)

---

*This analysis shows how to efficiently find the minimum edges needed to make a graph strongly connected using condensation graph analysis.* 