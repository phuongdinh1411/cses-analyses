---
layout: simple
title: "Strongly Connected Components - Graph Decomposition"
permalink: /problem_soulutions/graph_algorithms/strongly_connected_components_analysis
---

# Strongly Connected Components - Graph Decomposition

## 📋 Problem Description

Given a directed graph with n nodes and m edges, find all strongly connected components (SCCs). A strongly connected component is a subset of vertices where every vertex is reachable from every other vertex in the component.

This is a fundamental graph theory problem that involves decomposing a directed graph into its maximal strongly connected subgraphs. SCCs are important for understanding graph structure and connectivity.

**Input**: 
- First line: Two integers n and m (number of nodes and edges)
- Next m lines: Two integers a and b (edge from node a to node b)

**Output**: 
- First line: Number of SCCs
- Next lines: Nodes in each component

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n

**Example**:
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

**Explanation**: 
- Component 1: Nodes 1, 2, 3 form a cycle (1→2→3→1)
- Component 2: Node 4 (can reach 5 but can't be reached from 1,2,3)
- Component 3: Node 5 (can't reach any other nodes)
- Total: 3 strongly connected components

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find all strongly connected components in a directed graph
- **Key Insight**: Use Kosaraju's algorithm with two DFS passes
- **Challenge**: Handle large graphs efficiently and correctly identify SCCs

### Step 2: Brute Force Approach
**Use Kosaraju's algorithm to find strongly connected components:**

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

**Complexity**: O(n + m) - optimal for this problem

### Step 3: Optimization
**Use optimized Kosaraju's algorithm with better structure:**

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

sccs = find_strongly_connected_components(n, m, edges)
print(len(sccs))
for component in sccs:
    print(*component)

def test_solution():
    # Test case 1: Simple graph with 2 SCCs
    n1, m1 = 4, 4
    edges1 = [(1, 2), (2, 3), (3, 1), (4, 1)]
    result1 = find_strongly_connected_components(n1, m1, edges1)
    print(f"Test 1: {len(result1)} SCCs")
    for i, component in enumerate(result1):
        print(f"  SCC {i+1}: {component}")
    
    # Test case 2: Single SCC
    n2, m2 = 3, 3
    edges2 = [(1, 2), (2, 3), (3, 1)]
    result2 = find_strongly_connected_components(n2, m2, edges2)
    print(f"\nTest 2: {len(result2)} SCCs")
    for i, component in enumerate(result2):
        print(f"  SCC {i+1}: {component}")
    
    # Test case 3: Disconnected components
    n3, m3 = 5, 2
    edges3 = [(1, 2), (4, 5)]
    result3 = find_strongly_connected_components(n3, m3, edges3)
    print(f"\nTest 3: {len(result3)} SCCs")
    for i, component in enumerate(result3):
        print(f"  SCC {i+1}: {component}")

if __name__ == "__main__":
    solve_strongly_connected_components()
```

## Implementation Details

### 1. **Graph Representation**
- **Adjacency Lists**: We use two adjacency lists - one for the original graph and one for the reversed graph
- **Edge Storage**: Store edges in both directions for efficient traversal

### 2. **Two-Phase DFS Approach**
- **Phase 1**: Perform DFS on the original graph to get topological finish order
- **Phase 2**: Perform DFS on the reversed graph in reverse finish order to find SCCs

### 3. **SCC Identification**
- **Component Tracking**: Each DFS call in phase 2 identifies one complete SCC
- **Visited Management**: Separate visited arrays for each phase to ensure correctness

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Kosaraju's Algorithm | O(n + m) | O(n + m) | Use two DFS traversals |
| Optimized Kosaraju's | O(n + m) | O(n + m) | Better structure and clarity |

## Key Insights

### 1. **Two-Phase DFS Strategy**
- **First Phase**: Get topological finish order from original graph
- **Second Phase**: Use reversed graph and finish order to identify SCCs
- **Key Insight**: The finish order ensures we process nodes in the correct order

### 2. **Graph Reversal for SCC Detection**
- **Reversed Edges**: Creating a reversed graph helps identify reachability
- **SCC Property**: In a reversed graph, nodes in the same SCC can still reach each other
- **Component Isolation**: Each DFS call in phase 2 identifies one complete SCC

### 3. **Efficient Component Tracking**
- **Visited Arrays**: Separate visited arrays for each phase prevent interference
- **Component Building**: Build components incrementally during DFS traversal
- **Order Dependency**: Processing nodes in reverse finish order is crucial

## Key Insights for Other Problems

### 1. **Strongly Connected Components**
**Principle**: Use Kosaraju's algorithm to find all strongly connected components in a directed graph.
**Applicable to**: Graph problems, component problems, connectivity problems

### 2. **Kosaraju's Algorithm**
**Principle**: Use two DFS traversals to find SCCs: first for topological order, second on reversed graph.
**Applicable to**: SCC problems, graph decomposition problems, connectivity problems

### 3. **Graph Decomposition**
**Principle**: Decompose directed graphs into strongly connected components for analysis.
**Applicable to**: SCC problems, graph decomposition problems, connectivity problems

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

## Problem Variations

### **Variation 1: SCCs with Edge Costs**
**Problem**: Find SCCs and calculate the total cost of edges within each component.
```python
def find_scc_with_costs(n, edges, costs):
    # costs = {(a, b): cost} - cost of each edge
    
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

### **Variation 2: SCCs with Size Constraints**
**Problem**: Find SCCs that satisfy size constraints (minimum/maximum component size).
```python
def find_constrained_scc(n, edges, min_size=1, max_size=float('inf')):
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
            
            # Apply size constraints
            if min_size <= len(component) <= max_size:
                sccs.append(component)
    
    return sccs
```

### **Variation 3: Dynamic SCC Updates**
**Problem**: Handle dynamic edge additions/deletions and maintain SCC information.
```python
class DynamicSCC:
    def __init__(self, n):
        self.n = n
        self.edges = set()
        self.adj = [[] for _ in range(n + 1)]
        self.adj_rev = [[] for _ in range(n + 1)]
        self.sccs = []
        self.update_sccs()
    
    def add_edge(self, a, b):
        if (a, b) not in self.edges:
            self.edges.add((a, b))
            self.adj[a].append(b)
            self.adj_rev[b].append(a)
            self.update_sccs()
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.edges.remove((a, b))
            self.adj[a].remove(b)
            self.adj_rev[b].remove(a)
            self.update_sccs()
    
    def update_sccs(self):
        # Recompute SCCs using Kosaraju's algorithm
        visited = [False] * (self.n + 1)
        finish_order = []
        
        def first_dfs(node):
            visited[node] = True
            for neighbor in self.adj[node]:
                if not visited[neighbor]:
                    first_dfs(neighbor)
            finish_order.append(node)
        
        for i in range(1, self.n + 1):
            if not visited[i]:
                first_dfs(i)
        
        visited = [False] * (self.n + 1)
        self.sccs = []
        
        def second_dfs(node, component):
            visited[node] = True
            component.append(node)
            for neighbor in self.adj_rev[node]:
                if not visited[neighbor]:
                    second_dfs(neighbor, component)
        
        for node in reversed(finish_order):
            if not visited[node]:
                component = []
                second_dfs(node, component)
                self.sccs.append(component)
    
    def get_sccs(self):
        return self.sccs
```

### **Variation 4: SCC Condensation Graph**
**Problem**: Build a condensation graph where each SCC becomes a single node.
```python
def build_condensation_graph(n, edges):
    # Find all SCCs first
    sccs = find_strongly_connected_components(n, len(edges), edges)
    
    # Create mapping from node to SCC ID
    node_to_scc = {}
    for i, scc in enumerate(sccs):
        for node in scc:
            node_to_scc[node] = i
    
    # Build condensation graph
    condensation_edges = set()
    for a, b in edges:
        scc_a = node_to_scc[a]
        scc_b = node_to_scc[b]
        if scc_a != scc_b:  # Only add edge if nodes are in different SCCs
            condensation_edges.add((scc_a, scc_b))
    
    # Build adjacency list for condensation graph
    condensation_adj = [[] for _ in range(len(sccs))]
    for scc_a, scc_b in condensation_edges:
        condensation_adj[scc_a].append(scc_b)
    
    return condensation_adj, sccs
```

### **Variation 5: SCC with Node Weights**
**Problem**: Find SCCs and calculate total weight of nodes in each component.
```python
def find_scc_with_weights(n, edges, node_weights):
    # node_weights = [w1, w2, ..., wn] - weight of each node
    
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
    
    # Second DFS for SCCs with weight calculation
    visited = [False] * (n + 1)
    sccs = []
    scc_weights = []
    
    def second_dfs(node, component, component_weight):
        visited[node] = True
        component.append(node)
        component_weight[0] += node_weights[node - 1]  # Convert to 0-indexed
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, component, component_weight)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            component_weight = [0]
            second_dfs(node, component, component_weight)
            sccs.append(component)
            scc_weights.append(component_weight[0])
    
    return sccs, scc_weights
```

### 🎯 **Competitive Programming Variations**
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

## Related Problems

### **1. Graph Connectivity Problems**
- **Connected Components**: Find connected components in undirected graphs
- **Bridges and Articulation Points**: Find critical edges and nodes
- **Biconnected Components**: Find biconnected components in graphs

### **2. Path and Cycle Problems**
- **Eulerian Paths/Circuits**: Find paths that use every edge exactly once
- **Hamiltonian Paths/Cycles**: Find paths that visit every node exactly once
- **Shortest Paths**: Find shortest paths between nodes

### **3. Graph Decomposition Problems**
- **Topological Sorting**: Order nodes in a DAG
- **Bipartite Graph Detection**: Check if graph is bipartite
- **Planar Graph Problems**: Problems on planar graphs

## Learning Points

### **1. Algorithm Design**
- **Two-Phase Approach**: Breaking complex problems into simpler phases
- **Graph Reversal**: Using reversed graphs for specific properties
- **DFS Applications**: Multiple ways to use DFS for different purposes

### **2. Implementation Techniques**
- **Efficient Graph Representation**: Using adjacency lists for sparse graphs
- **Visited Array Management**: Proper handling of visited states
- **Component Building**: Incremental construction of solution components

### **3. Problem-Solving Strategies**
- **Component Analysis**: Breaking graphs into manageable components
- **Reachability Analysis**: Understanding node reachability in graphs
- **Graph Properties**: Leveraging specific graph properties for solutions

---

*This analysis demonstrates efficient SCC detection techniques and shows various extensions for component analysis problems.* 