# CSES New Flight Routes - Problem Analysis

## Problem Statement
Given a directed graph with n nodes and m edges, find the minimum number of new edges to add so that the graph becomes strongly connected.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is a directed edge from node a to node b.

### Output
Print the minimum number of new edges needed.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2*10^5
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

### Approach 1: Brute Force Edge Addition - O(n²)
**Description**: Try adding edges and check if the graph becomes strongly connected.

```python
def new_flight_routes_naive(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    def is_strongly_connected():
        # Check if every node can reach every other node
        for start in range(1, n + 1):
            visited = set()
            queue = [start]
            visited.add(start)
            
            while queue:
                node = queue.pop(0)
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            if len(visited) != n:
                return False
        return True
    
    if is_strongly_connected():
        return 0
    
    # Try adding edges
    min_edges = float('inf')
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                adj[i].append(j)
                if is_strongly_connected():
                    min_edges = min(min_edges, 1)
                adj[i].pop()
    
    return min_edges if min_edges != float('inf') else -1
```

**Why this is inefficient**: O(n²) complexity and doesn't handle the problem correctly.

### Improvement 1: Strongly Connected Components - O(n + m)
**Description**: Use Kosaraju's algorithm to find SCCs and calculate minimum edges needed.

```python
def new_flight_routes_improved(n, m, edges):
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

**Why this improvement works**: Uses SCC condensation to determine minimum edges needed.

### Approach 2: Optimal SCC Analysis - O(n + m)
**Description**: Optimized SCC analysis with better implementation.

```python
def new_flight_routes_optimal(n, m, edges):
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

**Why this improvement works**: Optimal solution using SCC condensation analysis.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_minimum_new_edges(n, m, edges):
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

result = find_minimum_new_edges(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force Edge Addition | O(n²) | O(n + m) | Simple but inefficient |
| Strongly Connected Components | O(n + m) | O(n + m) | Uses SCC condensation |
| Optimal SCC Analysis | O(n + m) | O(n + m) | Optimal solution |

## Key Insights for Other Problems

### 1. **Strongly Connected Components**
**Principle**: A graph is strongly connected if every node can reach every other node.
**Applicable to**: Graph connectivity problems, SCC problems, reachability problems

### 2. **Condensation Graph**
**Principle**: The condensation graph of SCCs helps determine minimum edges needed.
**Applicable to**: Graph analysis problems, connectivity optimization problems

### 3. **Source and Sink Counting**
**Principle**: Minimum edges needed = max(number of sources, number of sinks) in condensation graph.
**Applicable to**: Graph optimization problems, connectivity problems

## Notable Techniques

### 1. **Kosaraju's Algorithm**
```python
def kosaraju_scc(adj, adj_rev, n):
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
    
    return scc_id, current_scc
```

### 2. **Condensation Graph Building**
```python
def build_condensation_graph(edges, scc_id, num_sccs):
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

### 3. **Minimum Edges Calculation**
```python
def calculate_minimum_edges(num_sccs, in_degree, out_degree):
    if num_sccs == 1:
        return 0
    
    sources = sum(1 for i in range(num_sccs) if in_degree[i] == 0)
    sinks = sum(1 for i in range(num_sccs) if out_degree[i] == 0)
    
    return max(sources, sinks)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a strongly connected component problem
2. **Choose approach**: Use Kosaraju's algorithm for SCCs
3. **Initialize data structures**: Build adjacency lists for original and reversed graphs
4. **Find SCCs**: Use Kosaraju's algorithm to find strongly connected components
5. **Build condensation graph**: Create graph of SCCs
6. **Count sources and sinks**: Find nodes with in-degree 0 and out-degree 0
7. **Calculate minimum edges**: Use max(sources, sinks) formula
8. **Return result**: Output minimum edges needed

---

*This analysis shows how to efficiently find the minimum number of edges needed to make a directed graph strongly connected using SCC analysis.* 