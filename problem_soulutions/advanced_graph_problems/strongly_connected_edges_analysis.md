---
layout: simple
title: "Strongly Connected Edges"permalink: /problem_soulutions/advanced_graph_problems/strongly_connected_edges_analysis
---


# Strongly Connected Edges

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

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Strongly Connected Edges with Costs**
**Variation**: Each edge has a cost, find minimum cost edges to make graph strongly connected.
**Approach**: Use weighted edge selection with cost optimization.
```python
def cost_based_strongly_connected_edges(n, m, edges, edge_costs):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # Find SCCs using Kosaraju's algorithm
    scc_id, num_sccs = kosaraju_algorithm(n, adj)
    
    if num_sccs == 1:
        return 0, []  # Already strongly connected
    
    # Build condensation graph
    condensation_adj, in_degree, out_degree = build_condensation_graph(n, edges, scc_id, num_sccs)
    
    # Find sources and sinks
    sources = [i for i in range(num_sccs) if in_degree[i] == 0]
    sinks = [i for i in range(num_sccs) if out_degree[i] == 0]
    
    # Find minimum cost edges to connect sources and sinks
    min_cost_edges = []
    total_cost = 0
    
    # Connect sources to sinks with minimum cost
    for i, source in enumerate(sources):
        sink = sinks[i % len(sinks)]
        # Find minimum cost edge between source and sink components
        min_cost = float('inf')
        best_edge = None
        
        for node1 in range(1, n + 1):
            if scc_id[node1] == source:
                for node2 in range(1, n + 1):
                    if scc_id[node2] == sink:
                        cost = edge_costs.get((node1, node2), float('inf'))
                        if cost < min_cost:
                            min_cost = cost
                            best_edge = (node1, node2)
        
        if best_edge:
            min_cost_edges.append(best_edge)
            total_cost += min_cost
    
    return total_cost, min_cost_edges
```

#### 2. **Strongly Connected Edges with Constraints**
**Variation**: Limited budget, restricted edges, or specific connectivity requirements.
**Approach**: Use constraint satisfaction with edge selection.
```python
def constrained_strongly_connected_edges(n, m, edges, budget, restricted_edges):
    # Build adjacency lists excluding restricted edges
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        if (a, b) not in restricted_edges:
            adj[a].append(b)
            adj_rev[b].append(a)
    
    # Find SCCs
    scc_id, num_sccs = kosaraju_algorithm(n, adj)
    
    if num_sccs == 1:
        return 0, []  # Already strongly connected
    
    # Build condensation graph
    condensation_adj, in_degree, out_degree = build_condensation_graph(n, edges, scc_id, num_sccs)
    
    # Find sources and sinks
    sources = [i for i in range(num_sccs) if in_degree[i] == 0]
    sinks = [i for i in range(num_sccs) if out_degree[i] == 0]
    
    # Find edges to add within budget
    edges_to_add = []
    current_cost = 0
    
    for i, source in enumerate(sources):
        if current_cost >= budget:
            break
        
        sink = sinks[i % len(sinks)]
        # Find available edge between source and sink
        for node1 in range(1, n + 1):
            if scc_id[node1] == source:
                for node2 in range(1, n + 1):
                    if scc_id[node2] == sink:
                        if (node1, node2) not in restricted_edges:
                            edge_cost = 1  # Simplified cost
                            if current_cost + edge_cost <= budget:
                                edges_to_add.append((node1, node2))
                                current_cost += edge_cost
                                break
                if current_cost + 1 <= budget:
                    break
    
    return current_cost, edges_to_add
```

#### 3. **Strongly Connected Edges with Probabilities**
**Variation**: Each edge has a probability of success, find expected edges needed.
**Approach**: Use probabilistic analysis or Monte Carlo simulation.
```python
def probabilistic_strongly_connected_edges(n, m, edges, edge_probabilities, num_samples=1000):
    import random
    
    # Monte Carlo simulation
    total_edges_needed = 0
    
    for _ in range(num_samples):
        # Sample edges based on probabilities
        sampled_edges = []
        for a, b in edges:
            prob = edge_probabilities.get((a, b), 0.5)
            if random.random() < prob:
                sampled_edges.append((a, b))
        
        # Check if sampled graph is strongly connected
        if not is_strongly_connected(n, sampled_edges):
            # Find minimum edges to add
            edges_needed = find_minimum_edges_to_add(n, sampled_edges)
            total_edges_needed += edges_needed
    
    expected_edges = total_edges_needed / num_samples
    return expected_edges

def is_strongly_connected(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Check if graph is strongly connected
    scc_id, num_sccs = kosaraju_algorithm(n, adj)
    return num_sccs == 1

def find_minimum_edges_to_add(n, edges):
    # Implementation similar to main algorithm
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    scc_id, num_sccs = kosaraju_algorithm(n, adj)
    if num_sccs == 1:
        return 0
    
    condensation_adj, in_degree, out_degree = build_condensation_graph(n, edges, scc_id, num_sccs)
    sources = sum(1 for i in range(num_sccs) if in_degree[i] == 0)
    sinks = sum(1 for i in range(num_sccs) if out_degree[i] == 0)
    
    return max(sources, sinks)
```

#### 4. **Strongly Connected Edges with Multiple Criteria**
**Variation**: Optimize for multiple objectives (edge count, cost, probability).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_strongly_connected_edges(n, m, edges, criteria_weights):
    # criteria_weights = {'count': 0.4, 'cost': 0.3, 'probability': 0.3}
    
    def calculate_edge_score(edge_attributes):
        return (criteria_weights['count'] * edge_attributes['count'] + 
                criteria_weights['cost'] * edge_attributes['cost'] + 
                criteria_weights['probability'] * edge_attributes['probability'])
    
    # Find minimum edges needed
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    scc_id, num_sccs = kosaraju_algorithm(n, adj)
    if num_sccs == 1:
        edge_attrs = {'count': 0, 'cost': 0, 'probability': 1.0}
        return calculate_edge_score(edge_attrs), []
    
    condensation_adj, in_degree, out_degree = build_condensation_graph(n, edges, scc_id, num_sccs)
    sources = sum(1 for i in range(num_sccs) if in_degree[i] == 0)
    sinks = sum(1 for i in range(num_sccs) if out_degree[i] == 0)
    min_edges = max(sources, sinks)
    
    # Calculate edge attributes
    edge_attrs = {
        'count': min_edges,
        'cost': min_edges,  # Simplified cost
        'probability': 0.5  # Simplified probability
    }
    
    score = calculate_edge_score(edge_attrs)
    return score, min_edges
```

#### 5. **Strongly Connected Edges with Dynamic Updates**
**Variation**: Graph structure can be modified dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicStronglyConnectedEdges:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.scc_cache = None
        self.condensation_cache = None
    
    def add_edge(self, a, b):
        self.adj[a].append(b)
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        self.adj[a].remove(b)
        self.invalidate_cache()
    
    def invalidate_cache(self):
        self.scc_cache = None
        self.condensation_cache = None
    
    def get_minimum_edges_needed(self):
        if self.scc_cache is None:
            self.scc_cache = self.compute_sccs()
        
        scc_id, num_sccs = self.scc_cache
        if num_sccs == 1:
            return 0
        
        if self.condensation_cache is None:
            self.condensation_cache = self.build_condensation(scc_id, num_sccs)
        
        condensation_adj, in_degree, out_degree = self.condensation_cache
        sources = sum(1 for i in range(num_sccs) if in_degree[i] == 0)
        sinks = sum(1 for i in range(num_sccs) if out_degree[i] == 0)
        
        return max(sources, sinks)
    
    def compute_sccs(self):
        # Kosaraju's algorithm implementation
        adj_rev = [[] for _ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            for neighbor in self.adj[i]:
                adj_rev[neighbor].append(i)
        
        # First DFS
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
        
        # Second DFS
        visited = [False] * (self.n + 1)
        scc_id = [0] * (self.n + 1)
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
    
    def build_condensation(self, scc_id, num_sccs):
        condensation_adj = [[] for _ in range(num_sccs)]
        in_degree = [0] * num_sccs
        out_degree = [0] * num_sccs
        
        for i in range(1, self.n + 1):
            for neighbor in self.adj[i]:
                scc_a = scc_id[i]
                scc_b = scc_id[neighbor]
                if scc_a != scc_b:
                    condensation_adj[scc_a].append(scc_b)
                    in_degree[scc_b] += 1
                    out_degree[scc_a] += 1
        
        return condensation_adj, in_degree, out_degree
```

### Related Problems & Concepts

#### 1. **Strongly Connected Components Problems**
- **SCC Detection**: Find all strongly connected components
- **SCC Counting**: Count number of SCCs
- **SCC Size**: Find largest/smallest SCC
- **SCC Connectivity**: Check connectivity between SCCs

#### 2. **Graph Connectivity Problems**
- **Strong Connectivity**: Check if graph is strongly connected
- **Weak Connectivity**: Check if undirected graph is connected
- **Connectivity Augmentation**: Add edges to improve connectivity
- **Connectivity Maintenance**: Maintain connectivity under updates

#### 3. **Graph Theory Problems**
- **Condensation Graph**: DAG of SCCs
- **Sources and Sinks**: Nodes with zero in/out degree
- **Graph Decomposition**: Break graph into components
- **Graph Analysis**: Analyze graph structure and properties

#### 4. **Algorithm Problems**
- **Kosaraju's Algorithm**: Find SCCs using two DFS passes
- **Tarjan's Algorithm**: Find SCCs using single DFS
- **DFS Applications**: Depth-first search variations
- **Graph Traversal**: BFS, DFS, and their applications

#### 5. **Network Problems**
- **Network Connectivity**: Ensure network connectivity
- **Network Reliability**: Improve network reliability
- **Network Design**: Design robust networks
- **Network Analysis**: Analyze network structure

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large graphs
- **Edge Cases**: Robust graph operations

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient graph traversal
- **Sliding Window**: Optimal subgraph problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Graph Theory**
- **Graph Properties**: Connectivity, diameter, girth
- **Graph Decomposition**: Breaking graphs into components
- **Graph Algorithms**: SCC algorithms, connectivity algorithms
- **Graph Analysis**: Analyzing graph structure

#### 2. **Network Theory**
- **Network Connectivity**: Ensuring network connectivity
- **Network Reliability**: Improving network reliability
- **Network Design**: Designing robust networks
- **Network Analysis**: Analyzing network structure

#### 3. **Optimization Theory**
- **Minimum Edge Addition**: Adding minimum edges for connectivity
- **Network Optimization**: Optimizing network structure
- **Connectivity Optimization**: Optimizing connectivity
- **Graph Optimization**: Optimizing graph properties

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Graph and connectivity problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Graph Problems**: SCC detection, connectivity
- **Network Problems**: Network design, reliability
- **Algorithm Problems**: DFS, BFS, graph algorithms
- **Optimization Problems**: Minimum edge addition 