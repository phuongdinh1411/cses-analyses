---
layout: simple
title: "Strongly Connected Components"
permalink: /problem_soulutions/graph_algorithms/strongly_connected_components_analysis
---


# Strongly Connected Components

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Strongly Connected Components with Costs**
**Problem**: Each edge has a cost, find SCCs with minimum total cost.
```python
def cost_based_scc(n, edges, costs):
    # costs[(a, b)] = cost of edge from a to b
    
    # Build adjacency lists with costs
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        cost = costs.get((a, b), 0)
        adj[a].append((b, cost))
        adj_rev[b].append((a, cost))
    
    # First DFS for topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor, _ in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS for SCCs with cost tracking
    visited = [False] * (n + 1)
    sccs = []
    scc_costs = []
    
    def second_dfs(node, component, component_cost):
        visited[node] = True
        component.append(node)
        for neighbor, cost in adj_rev[node]:
            if not visited[neighbor]:
                component_cost[0] += cost
                second_dfs(neighbor, component, component_cost)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            component_cost = [0]
            second_dfs(node, component, component_cost)
            sccs.append(component)
            scc_costs.append(component_cost[0])
    
    return sccs, scc_costs
```

#### **Variation 2: Strongly Connected Components with Constraints**
**Problem**: Find SCCs with constraints on component size or structure.
```python
def constrained_scc(n, edges, constraints):
    # constraints = {'max_size': x, 'min_size': y, 'max_components': z}
    
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
    
    # Second DFS for SCCs with constraints
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
            
            # Apply constraints
            if 'max_size' in constraints and len(component) > constraints['max_size']:
                continue  # Skip this component
            if 'min_size' in constraints and len(component) < constraints['min_size']:
                continue  # Skip this component
            
            sccs.append(component)
            
            # Check max components constraint
            if 'max_components' in constraints and len(sccs) >= constraints['max_components']:
                break
    
    return sccs
```

#### **Variation 3: Strongly Connected Components with Probabilities**
**Problem**: Each edge has a probability of existing, find expected SCCs.
```python
def probabilistic_scc(n, edges, probabilities):
    # probabilities[(a, b)] = probability that edge from a to b exists
    
    # Use Monte Carlo simulation
    import random
    
    def simulate_scc():
        # Randomly sample edges based on probabilities
        sampled_edges = []
        for a, b in edges:
            if random.random() < probabilities.get((a, b), 1.0):
                sampled_edges.append((a, b))
        
        # Build adjacency lists for sampled edges
        adj = [[] for _ in range(n + 1)]
        adj_rev = [[] for _ in range(n + 1)]
        
        for a, b in sampled_edges:
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
        
        for i in range(1, n + 1):
            if not visited[i]:
                first_dfs(i)
        
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
    
    # Run multiple simulations
    num_simulations = 1000
    all_sccs = []
    for _ in range(num_simulations):
        sccs = simulate_scc()
        all_sccs.append(sccs)
    
    # Calculate expected number of SCCs
    expected_scc_count = sum(len(sccs) for sccs in all_sccs) / num_simulations
    
    # Find most common SCC structure
    from collections import Counter
    scc_structures = Counter(tuple(tuple(sorted(comp)) for comp in sccs) for sccs in all_sccs)
    most_common_structure = scc_structures.most_common(1)[0][0]
    
    return expected_scc_count, list(most_common_structure)
```

#### **Variation 4: Strongly Connected Components with Multiple Criteria**
**Problem**: Find SCCs considering multiple criteria (size, cost, connectivity).
```python
def multi_criteria_scc(n, edges, criteria):
    # criteria = {'size_weight': x, 'cost_weight': y, 'connectivity_weight': z}
    
    # Build adjacency lists with costs
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    costs = criteria.get('costs', {})
    
    for a, b in edges:
        cost = costs.get((a, b), 0)
        adj[a].append((b, cost))
        adj_rev[b].append((a, cost))
    
    # Kosaraju's algorithm
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor, _ in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    visited = [False] * (n + 1)
    sccs = []
    
    def second_dfs(node, component, component_cost):
        visited[node] = True
        component.append(node)
        for neighbor, cost in adj_rev[node]:
            if not visited[neighbor]:
                component_cost[0] += cost
                second_dfs(neighbor, component, component_cost)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            component_cost = [0]
            second_dfs(node, component, component_cost)
            
            # Calculate weighted score
            size_score = len(component) * criteria.get('size_weight', 1)
            cost_score = component_cost[0] * criteria.get('cost_weight', 1)
            connectivity_score = len(component) * (len(component) - 1) * criteria.get('connectivity_weight', 1)
            
            total_score = size_score + cost_score + connectivity_score
            sccs.append((component, total_score))
    
    # Sort by weighted score
    sccs.sort(key=lambda x: x[1], reverse=True)
    return [scc[0] for scc in sccs]
```

#### **Variation 5: Strongly Connected Components with Dynamic Updates**
**Problem**: Handle dynamic updates to edges and find SCCs after each update.
```python
def dynamic_scc(n, initial_edges, updates):
    # updates = [(edge_to_add, edge_to_remove), ...]
    
    edges = initial_edges.copy()
    results = []
    
    for edge_to_add, edge_to_remove in updates:
        # Update edges
        if edge_to_remove in edges:
            edges.remove(edge_to_remove)
        if edge_to_add:
            edges.append(edge_to_add)
        
        # Rebuild adjacency lists
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
        
        for i in range(1, n + 1):
            if not visited[i]:
                first_dfs(i)
        
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
        
        results.append(sccs)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Graph Problems**
- **Directed Graphs**: Properties of directed graphs
- **Connectivity**: Strong and weak connectivity
- **Graph Decomposition**: Decomposing graphs into components
- **Graph Traversal**: BFS/DFS on directed graphs

#### **2. Component Problems**
- **Connected Components**: Find connected components in undirected graphs
- **Biconnected Components**: Find biconnected components
- **Articulation Points**: Find articulation points
- **Bridge Detection**: Find bridges in graphs

#### **3. Algorithmic Techniques**
- **Kosaraju's Algorithm**: Two-pass DFS for SCCs
- **Tarjan's Algorithm**: Single-pass DFS for SCCs
- **DFS Traversal**: Depth-first search algorithms
- **Graph Transpose**: Transposing directed graphs

#### **4. Optimization Problems**
- **Minimum Cost Components**: Find minimum cost SCCs
- **Multi-Criteria Optimization**: Optimize multiple objectives
- **Constraint Satisfaction**: Satisfy component constraints
- **Dynamic Updates**: Handle dynamic graph changes

#### **5. Mathematical Concepts**
- **Graph Theory**: Properties of directed graphs
- **Component Theory**: Mathematical theory of components
- **Connectivity Theory**: Theory of graph connectivity
- **Combinatorics**: Counting components and structures

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    sccs = find_scc(n, edges)
    print(len(sccs))
    for scc in sccs:
        print(len(scc), *scc)
```

#### **2. Range Queries on SCCs**
```python
def range_scc_queries(n, edges, queries):
    # queries = [(start_node, end_node), ...] - find SCCs in range
    
    # Precompute all SCCs
    sccs = find_scc(n, edges)
    
    results = []
    for start, end in queries:
        range_sccs = []
        for scc in sccs:
            range_scc = [node for node in scc if start <= node <= end]
            if range_scc:
                range_sccs.append(range_scc)
        results.append(range_sccs)
    
    return results
```

#### **3. Interactive SCC Problems**
```python
def interactive_scc():
    n = int(input("Enter number of nodes: "))
    m = int(input("Enter number of edges: "))
    print("Enter edges (a b):")
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    sccs = find_scc(n, edges)
    print(f"Number of SCCs: {len(sccs)}")
    for i, scc in enumerate(sccs, 1):
        print(f"SCC {i}: {scc}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **SCC Properties**: Properties of strongly connected components
- **Component Theory**: Mathematical theory of graph components
- **Connectivity Theory**: Theory of graph connectivity
- **Graph Decomposition**: Decomposing graphs into components

#### **2. Component Analysis**
- **Component Statistics**: Statistical properties of components
- **Component Enumeration**: Enumerating different component structures
- **Component Patterns**: Recognizing patterns in components
- **Component Evolution**: How components change with graph modifications

#### **3. Combinatorics**
- **Component Counting**: Counting different component structures
- **Component Enumeration**: Enumerating all possible component configurations
- **Pattern Recognition**: Recognizing patterns in component structures
- **Enumeration**: Enumerating valid component configurations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Kosaraju's Algorithm**: Two-pass DFS for SCCs
- **Tarjan's Algorithm**: Single-pass DFS for SCCs
- **DFS/BFS**: Graph traversal algorithms
- **Graph Algorithms**: Various graph algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Component Theory**: Mathematical theory of components
- **Connectivity Theory**: Theory of graph connectivity
- **Combinatorics**: Counting and enumeration techniques

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **DFS Implementation**: Efficient DFS implementations
- **Algorithm Optimization**: Improving time and space complexity
- **Dynamic Programming**: Handling dynamic updates

---

*This analysis demonstrates efficient SCC detection techniques and shows various extensions for component analysis problems.* 