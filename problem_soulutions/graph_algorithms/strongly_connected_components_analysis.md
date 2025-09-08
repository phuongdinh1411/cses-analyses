---
layout: simple
title: "Strongly Connected Components - Graph Decomposition"
permalink: /problem_soulutions/graph_algorithms/strongly_connected_components_analysis
---

# Strongly Connected Components - Graph Decomposition

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand strongly connected components and graph decomposition concepts
- Apply Tarjan's algorithm or Kosaraju's algorithm to find SCCs in directed graphs
- Implement efficient SCC algorithms with proper stack usage and graph traversal
- Optimize SCC solutions using graph representations and algorithm optimizations
- Handle edge cases in SCC problems (single nodes, disconnected graphs, self-loops)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tarjan's algorithm, Kosaraju's algorithm, strongly connected components, graph decomposition
- **Data Structures**: Stacks, adjacency lists, graph representations, component tracking
- **Mathematical Concepts**: Graph theory, strongly connected components, graph decomposition, DFS properties
- **Programming Skills**: Stack implementation, DFS/BFS, graph traversal, algorithm implementation
- **Related Problems**: Building Teams (graph coloring), Cycle Finding (cycle detection), Graph connectivity

## Problem Description

**Problem**: Given a directed graph with n nodes and m edges, find all strongly connected components (SCCs). A strongly connected component is a subset of vertices where every vertex is reachable from every other vertex in the component.

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
- Graph is directed
- Nodes are numbered from 1 to n

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

## Visual Example

### Input Graph
```
Nodes: 1, 2, 3, 4, 5
Edges: (1→2), (2→3), (3→1), (3→4), (4→5)

Graph representation:
1 ──> 2 ──> 3 ──> 4 ──> 5
│     │     │
└─────┼─────┘
      │
      └────────┘
```

### Strongly Connected Components (SCCs) Detection
```
Step 1: Build adjacency lists
- Node 1: [2]
- Node 2: [3]
- Node 3: [1, 4]
- Node 4: [5]
- Node 5: []

Step 2: First DFS pass (finish times)
- Start from node 1: 1 → 2 → 3 → 1 (cycle detected)
- Finish times: [3, 2, 1, 4, 5]

Step 3: Build transpose graph
- Node 1: [3]
- Node 2: [1]
- Node 3: [2]
- Node 4: [3]
- Node 5: [4]

Step 4: Second DFS pass (SCCs)
- Process in reverse finish time order: [5, 4, 1, 2, 3]
- Node 5: SCC 1 (only itself)
- Node 4: SCC 2 (only itself)
- Node 1: SCC 3 (1 → 2 → 3 → 1)
- Node 2: already in SCC 3
- Node 3: already in SCC 3
```

### SCC Analysis
```
Strongly Connected Components:
- SCC 1: {5}
- SCC 2: {4}
- SCC 3: {1, 2, 3}

Component verification:
- SCC 1: Node 5 can reach itself ✓
- SCC 2: Node 4 can reach itself ✓
- SCC 3: All nodes can reach each other ✓
  - 1 → 2 → 3 → 1
  - 2 → 3 → 1 → 2
  - 3 → 1 → 2 → 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force SCC Detection (Inefficient)

**Key Insights from Brute Force Solution:**
- Check all possible pairs of nodes to determine if they are in the same SCC
- Use Floyd-Warshall algorithm to find all-pairs reachability
- Group nodes that can reach each other into components
- Simple but computationally expensive approach

**Algorithm:**
1. Build adjacency matrix from edges
2. Use Floyd-Warshall to find all-pairs reachability
3. Group nodes that can reach each other bidirectionally
4. Return strongly connected components

**Visual Example:**
```
Brute force: Check all pairs
For nodes: 1, 2, 3, 4, 5 with edges (1→2), (2→3), (3→1), (3→4), (4→5)

Reachability Matrix (after Floyd-Warshall):
    1  2  3  4  5
1 [ 1  1  1  1  1 ]
2 [ 1  1  1  1  1 ]
3 [ 1  1  1  1  1 ]
4 [ 0  0  0  1  1 ]
5 [ 0  0  0  0  1 ]

SCCs: {1,2,3} and {4} and {5} → 3 components
```

**Implementation:**
```python
def strongly_connected_components_brute_force(n, m, edges):
    # Build adjacency matrix
    adj = [[False] * (n + 1) for _ in range(n + 1)]
    for a, b in edges:
        adj[a][b] = True
    
    # Floyd-Warshall for all-pairs reachability
    for k in range(1, n + 1):
    for i in range(1, n + 1):
            for j in range(1, n + 1):
                if adj[i][k] and adj[k][j]:
                    adj[i][j] = True
    
    # Find SCCs by checking bidirectional reachability
    visited = [False] * (n + 1)
    sccs = []
    
    for i in range(1, n + 1):
        if not visited[i]:
            component = []
            for j in range(1, n + 1):
                if adj[i][j] and adj[j][i]:  # Bidirectional reachability
                    component.append(j)
                    visited[j] = True
            sccs.append(component)
    
    return sccs
```

**Time Complexity:** O(n³) for Floyd-Warshall algorithm
**Space Complexity:** O(n²) for adjacency matrix

**Why it's inefficient:**
- Uses O(n²) space for adjacency matrix
- O(n³) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Overkill for this specific problem

### Approach 2: Kosaraju's Algorithm (Better)

**Key Insights from Kosaraju's Solution:**
- Use two DFS passes to find strongly connected components
- First DFS to get topological order of finish times
- Build transpose graph (reverse all edges)
- Second DFS on transpose graph in reverse finish time order
- Much more efficient than brute force approach

**Algorithm:**
1. Build adjacency lists for original and transpose graphs
2. First DFS to get finish times (topological order)
3. Build transpose graph by reversing all edges
4. Second DFS on transpose graph in reverse finish time order
5. Each DFS tree in second pass forms an SCC

**Visual Example:**
```
Kosaraju's algorithm for nodes: 1, 2, 3, 4, 5 with edges (1→2), (2→3), (3→1), (3→4), (4→5)

Step 1: First DFS (finish times)
- DFS from 1: 1 → 2 → 3 → 1 (cycle), finish times: [3, 2, 1, 4, 5]

Step 2: Build transpose graph
- Original: 1→2, 2→3, 3→1, 3→4, 4→5
- Transpose: 2→1, 3→2, 1→3, 4→3, 5→4

Step 3: Second DFS (reverse finish time order: [5, 4, 1, 2, 3])
- DFS from 5: SCC 1 = {5}
- DFS from 4: SCC 2 = {4}
- DFS from 1: SCC 3 = {1, 2, 3}
```

**Implementation:**
```python
def strongly_connected_components_kosaraju(n, m, edges):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS to get finish times
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
    
    # Second DFS on reversed graph
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

**Time Complexity:** O(n + m) for two DFS traversals
**Space Complexity:** O(n + m) for adjacency lists and visited arrays

**Why it's better:**
- Uses O(n + m) space instead of O(n²)
- O(n + m) time complexity is optimal
- Simple and intuitive two-pass approach
- Standard method for SCC detection

### Approach 3: Tarjan's Algorithm (Optimal)

**Key Insights from Tarjan's Solution:**
- Use single DFS with stack and low-link values
- Track discovery time and low-link value for each node
- Use stack to keep track of current SCC
- Most efficient approach for SCC detection

**Algorithm:**
1. Use DFS with discovery time and low-link tracking
2. Maintain stack of nodes in current path
3. When low-link equals discovery time, pop stack to form SCC
4. Update low-link values during backtracking

**Visual Example:**
```
Tarjan's algorithm for nodes: 1, 2, 3, 4, 5 with edges (1→2), (2→3), (3→1), (3→4), (4→5)

DFS traversal with discovery times and low-link values:
- Node 1: disc=1, low=1, stack=[1]
- Node 2: disc=2, low=2, stack=[1,2]
- Node 3: disc=3, low=3, stack=[1,2,3]
- Back to 1: low[3]=1, low[2]=1, low[1]=1
- SCC found: {1,2,3}
- Node 4: disc=4, low=4, stack=[4]
- Node 5: disc=5, low=5, stack=[4,5]
- SCC found: {5}, then {4}
```

**Implementation:**
```python
def strongly_connected_components_tarjan(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Tarjan's algorithm variables
    disc = [0] * (n + 1)  # Discovery time
    low = [0] * (n + 1)   # Low-link value
    stack = []
    in_stack = [False] * (n + 1)
    time = 0
    sccs = []
    
    def tarjan_dfs(node):
        nonlocal time
        time += 1
        disc[node] = low[node] = time
        stack.append(node)
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if disc[neighbor] == 0:  # Not visited
                tarjan_dfs(neighbor)
                low[node] = min(low[node], low[neighbor])
            elif in_stack[neighbor]:  # In current stack
                low[node] = min(low[node], disc[neighbor])
        
        # If low-link equals discovery time, we found an SCC
        if low[node] == disc[node]:
            component = []
            while True:
                w = stack.pop()
                in_stack[w] = False
                component.append(w)
                if w == node:
                    break
            sccs.append(component)
            
    for i in range(1, n + 1):
        if disc[i] == 0:
            tarjan_dfs(i)
    
    return sccs

def solve_strongly_connected_components():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    sccs = strongly_connected_components_tarjan(n, m, edges)
    print(len(sccs))
    for component in sccs:
        print(*component)

# Main execution
if __name__ == "__main__":
    solve_strongly_connected_components()
```

**Time Complexity:** O(n + m) for single DFS traversal
**Space Complexity:** O(n + m) for adjacency list and stack

**Why it's optimal:**
- Single DFS pass instead of two
- O(n + m) time complexity is optimal
- More memory efficient than Kosaraju's
- Standard method in competitive programming

## 🎯 Problem Variations

### Variation 1: SCC with Component Size Constraints
**Problem**: Find strongly connected components with constraints on component sizes.

**Link**: [CSES Problem Set - SCC with Size Constraints](https://cses.fi/problemset/task/scc_size_constraints)

```python
def scc_with_size_constraints(n, m, edges, constraints):
    # constraints = {'min_size': x, 'max_size': y}
    
    # Find SCCs using Tarjan's algorithm
    sccs = strongly_connected_components_tarjan(n, m, edges)
    
    # Filter SCCs based on size constraints
    filtered_sccs = []
    for component in sccs:
        size = len(component)
        if constraints.get('min_size', 1) <= size <= constraints.get('max_size', float('inf')):
            filtered_sccs.append(component)
    
    return filtered_sccs
```

### Variation 2: SCC with Edge Weight Constraints
**Problem**: Find strongly connected components considering edge weights.

**Link**: [CSES Problem Set - Weighted SCC](https://cses.fi/problemset/task/weighted_scc)

```python
def weighted_scc(n, m, edges, weights):
    # weights[(a, b)] = weight of edge from a to b
    
    # Build weighted adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        weight = weights.get((a, b), 1)
        adj[a].append((b, weight))
    
    # Modified Tarjan's algorithm for weighted edges
    disc = [0] * (n + 1)
    low = [0] * (n + 1)
    stack = []
    in_stack = [False] * (n + 1)
    time = 0
    sccs = []
    
    def tarjan_dfs(node):
        nonlocal time
        time += 1
        disc[node] = low[node] = time
        stack.append(node)
        in_stack[node] = True
        
        for neighbor, weight in adj[node]:
            if disc[neighbor] == 0:
                tarjan_dfs(neighbor)
                low[node] = min(low[node], low[neighbor])
            elif in_stack[neighbor]:
                low[node] = min(low[node], disc[neighbor])
        
        if low[node] == disc[node]:
            component = []
            while True:
                w = stack.pop()
                in_stack[w] = False
                component.append(w)
                if w == node:
                    break
            sccs.append(component)
    
    for i in range(1, n + 1):
        if disc[i] == 0:
            tarjan_dfs(i)
    
    return sccs
```

### Variation 3: Dynamic SCC Updates
**Problem**: Handle dynamic updates to edges and find SCCs after each update.

**Link**: [CSES Problem Set - Dynamic SCC](https://cses.fi/problemset/task/dynamic_scc)

```python
def dynamic_scc(n, m, initial_edges, updates):
    # updates = [(edge_to_add, edge_to_remove), ...]
    
    edges = initial_edges.copy()
    results = []
    
    for edge_to_add, edge_to_remove in updates:
        # Update edges
        if edge_to_remove in edges:
            edges.remove(edge_to_remove)
        if edge_to_add:
            edges.append(edge_to_add)
        
        # Find SCCs with updated edges
        sccs = strongly_connected_components_tarjan(n, len(edges), edges)
        results.append(sccs)
    
    return results
```

## 🔗 Related Problems

- **[Building Teams](/cses-analyses/problem_soulutions/graph_algorithms/building_teams_analysis/)**: Graph coloring problems
- **[Cycle Finding](/cses-analyses/problem_soulutions/graph_algorithms/cycle_finding_analysis/)**: Cycle detection problems
- **[Planets and Kingdoms](/cses-analyses/problem_soulutions/graph_algorithms/planets_and_kingdoms_analysis/)**: SCC applications
- **[Graph Connectivity](/cses-analyses/problem_soulutions/graph_algorithms/)**: Connectivity problems

## 📚 Learning Points

1. **Strongly Connected Components**: Essential for directed graph analysis
2. **Kosaraju's Algorithm**: Two-pass DFS approach for SCC detection
3. **Tarjan's Algorithm**: Single-pass DFS with stack for SCC detection
4. **Graph Decomposition**: Breaking graphs into meaningful components
5. **DFS Properties**: Understanding discovery times and low-link values
6. **Graph Theory**: Foundation for many algorithmic problems

## 📝 Summary

The Strongly Connected Components problem demonstrates fundamental graph decomposition concepts for analyzing directed graph connectivity. We explored three approaches:

1. **Brute Force SCC Detection**: O(n³) time complexity using Floyd-Warshall algorithm, inefficient for large graphs
2. **Kosaraju's Algorithm**: O(n + m) time complexity using two DFS passes, optimal and intuitive approach
3. **Tarjan's Algorithm**: O(n + m) time complexity using single DFS with stack, most memory efficient

The key insights include understanding strongly connected components as maximal subgraphs where every node can reach every other node, using DFS-based algorithms for efficient detection, and applying graph decomposition techniques. This problem serves as an excellent introduction to advanced graph algorithms and connectivity analysis.
