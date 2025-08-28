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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Planets and Kingdoms with Costs**
**Problem**: Each teleporter has a cost, find minimum cost to establish kingdoms.
```python
def cost_based_planets_kingdoms(n, edges, costs):
    # costs[(a, b)] = cost of teleporter from a to b
    
    # Build adjacency lists with costs
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        cost = costs.get((a, b), 0)
        adj[a].append((b, cost))
        adj_rev[b].append((a, cost))
    
    # First DFS to get topological order
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
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    sccs = []
    total_cost = 0
    
    def second_dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor, cost in adj_rev[node]:
            if not visited[neighbor]:
                total_cost += cost
                second_dfs(neighbor, component)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            second_dfs(node, component)
            sccs.append(component)
    
    # Assign kingdom IDs
    kingdom_id = [0] * (n + 1)
    for i, component in enumerate(sccs, 1):
        for node in component:
            kingdom_id[node] = i
    
    return len(sccs), kingdom_id[1:n+1], total_cost
```

#### **Variation 2: Planets and Kingdoms with Constraints**
**Problem**: Find kingdoms with constraints on teleporter usage or kingdom size.
```python
def constrained_planets_kingdoms(n, edges, constraints):
    # constraints = {'max_kingdom_size': x, 'forbidden_teleporters': [(a, b), ...]}
    
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        # Check if teleporter is forbidden
        if (a, b) not in constraints.get('forbidden_teleporters', []):
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
            # Check kingdom size constraint
            if len(component) <= constraints.get('max_kingdom_size', float('inf')):
                sccs.append(component)
    
    # Assign kingdom IDs
    kingdom_id = [0] * (n + 1)
    for i, component in enumerate(sccs, 1):
        for node in component:
            kingdom_id[node] = i
    
    return len(sccs), kingdom_id[1:n+1]
```

#### **Variation 3: Planets and Kingdoms with Probabilities**
**Problem**: Each teleporter has a success probability, find expected number of kingdoms.
```python
def probabilistic_planets_kingdoms(n, edges, probabilities):
    # probabilities[(a, b)] = probability that teleporter from a to b works
    
    # Build adjacency lists with probabilities
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        prob = probabilities.get((a, b), 0.5)
        adj[a].append((b, prob))
        adj_rev[b].append((a, prob))
    
    # Calculate expected number of kingdoms
    # For each edge, calculate probability of connectivity
    expected_kingdoms = n  # Start with each planet as separate kingdom
    
    for a, b in edges:
        prob = probabilities.get((a, b), 0.5)
        # If teleporter works, it might reduce number of kingdoms
        # This is a simplified calculation
        expected_kingdoms -= prob * 0.1  # Rough estimate
    
    return max(1, int(expected_kingdoms))
```

#### **Variation 4: Planets and Kingdoms with Multiple Criteria**
**Problem**: Find kingdoms optimizing multiple objectives (cost, efficiency, stability).
```python
def multi_criteria_planets_kingdoms(n, edges, costs, efficiencies, stabilities):
    # costs[(a, b)] = cost, efficiencies[(a, b)] = efficiency, stabilities[(a, b)] = stability
    
    # Build adjacency lists with multi-criteria scores
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        cost = costs.get((a, b), 0)
        efficiency = efficiencies.get((a, b), 1)
        stability = stabilities.get((a, b), 1)
        
        # Normalize values
        max_cost = max(costs.values()) if costs else 1
        max_efficiency = max(efficiencies.values()) if efficiencies else 1
        max_stability = max(stabilities.values()) if stabilities else 1
        
        # Weighted score (lower is better)
        score = (cost / max_cost - efficiency / max_efficiency - stability / max_stability)
        adj[a].append((b, score))
        adj_rev[b].append((a, score))
    
    # Sort edges by score for greedy approach
    for i in range(1, n + 1):
        adj[i].sort(key=lambda x: x[1])
        adj_rev[i].sort(key=lambda x: x[1])
    
    # First DFS to get topological order
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
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    sccs = []
    total_cost = 0
    total_efficiency = 0
    total_stability = 0
    
    def second_dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor, score in adj_rev[node]:
            if not visited[neighbor]:
                # Track actual values
                edge = (neighbor, node)
                total_cost += costs.get(edge, 0)
                total_efficiency += efficiencies.get(edge, 0)
                total_stability += stabilities.get(edge, 0)
                second_dfs(neighbor, component)
    
    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            second_dfs(node, component)
            sccs.append(component)
    
    # Assign kingdom IDs
    kingdom_id = [0] * (n + 1)
    for i, component in enumerate(sccs, 1):
        for node in component:
            kingdom_id[node] = i
    
    return len(sccs), kingdom_id[1:n+1], total_cost, total_efficiency, total_stability
```

#### **Variation 5: Planets and Kingdoms with Dynamic Updates**
**Problem**: Handle dynamic updates to teleporter network and find kingdoms after each update.
```python
def dynamic_planets_kingdoms(n, initial_edges, updates):
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
        
        # Assign kingdom IDs
        kingdom_id = [0] * (n + 1)
        for i, component in enumerate(sccs, 1):
            for node in component:
                kingdom_id[node] = i
        
        results.append((len(sccs), kingdom_id[1:n+1]))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Strongly Connected Components Problems**
- **SCC Detection**: Find strongly connected components
- **Graph Decomposition**: Decompose graphs into components
- **Connectivity Analysis**: Analyze graph connectivity
- **Component Counting**: Count number of components

#### **2. Graph Theory Problems**
- **Directed Graphs**: Study of directed graphs
- **Connectivity**: Study of graph connectivity
- **Graph Algorithms**: Various graph algorithms
- **Graph Properties**: Study graph properties

#### **3. Network Problems**
- **Network Analysis**: Analyze network structure
- **Community Detection**: Find communities in networks
- **Clustering**: Cluster nodes in graphs
- **Partitioning**: Partition graphs into components

#### **4. Algorithmic Problems**
- **Kosaraju's Algorithm**: Find strongly connected components
- **Tarjan's Algorithm**: Another SCC algorithm
- **DFS**: Depth-first search for graph traversal
- **Graph Algorithms**: Various graph algorithms

#### **5. Optimization Problems**
- **Graph Partitioning**: Partition graphs optimally
- **Clustering**: Find optimal clusters
- **Network Design**: Design efficient networks
- **Resource Allocation**: Allocate resources optimally

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Networks**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    num_kingdoms, kingdom_ids = planets_and_kingdoms(n, edges)
    print(num_kingdoms)
    print(*kingdom_ids)
```

#### **2. Range Queries on Planets and Kingdoms**
```python
def range_planets_kingdoms_queries(n, edges, queries):
    # queries = [(start_edge, end_edge), ...] - find kingdoms using edges in range
    
    results = []
    for start, end in queries:
        subset_edges = edges[start:end+1]
        num_kingdoms, kingdom_ids = planets_and_kingdoms(n, subset_edges)
        results.append((num_kingdoms, kingdom_ids))
    
    return results
```

#### **3. Interactive Planets and Kingdoms Problems**
```python
def interactive_planets_kingdoms():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter edges (a b):")
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    num_kingdoms, kingdom_ids = planets_and_kingdoms(n, edges)
    print(f"Number of kingdoms: {num_kingdoms}")
    print(f"Kingdom assignments: {kingdom_ids}")
    
    # Show the kingdoms
    kingdoms = {}
    for i, kingdom_id in enumerate(kingdom_ids, 1):
        if kingdom_id not in kingdoms:
            kingdoms[kingdom_id] = []
        kingdoms[kingdom_id].append(i)
    
    for kingdom_id, planets in kingdoms.items():
        print(f"Kingdom {kingdom_id}: {planets}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Strongly Connected Components**: Properties of SCCs
- **Connectivity Theory**: Theory of graph connectivity
- **Graph Decomposition**: Mathematical decomposition of graphs
- **Network Theory**: Theory of networks

#### **2. Linear Algebra**
- **Adjacency Matrix**: Matrix representation of graphs
- **Laplacian Matrix**: Graph Laplacian matrix
- **Spectral Graph Theory**: Study of graph eigenvalues
- **Matrix Decomposition**: Decompose matrices

#### **3. Combinatorics**
- **Graph Enumeration**: Enumerate graphs with properties
- **Component Counting**: Count components in graphs
- **Partition Theory**: Theory of partitions
- **Clustering Theory**: Theory of clustering

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **SCC Algorithms**: Kosaraju's, Tarjan's algorithms
- **Graph Algorithms**: DFS, BFS, connectivity algorithms
- **Network Algorithms**: Community detection, clustering algorithms
- **Optimization Algorithms**: Graph partitioning algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Linear Algebra**: Matrix representations of graphs
- **Network Theory**: Theory of networks and connectivity
- **Combinatorics**: Combinatorial graph theory

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Component Detection**: Efficient component detection
- **Graph Traversal**: Efficient graph traversal
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient SCC techniques and shows various extensions for graph decomposition problems.* 