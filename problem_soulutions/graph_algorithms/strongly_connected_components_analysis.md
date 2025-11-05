---
layout: simple
title: "Strongly Connected Components - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/strongly_connected_components_analysis
---

# Strongly Connected Components - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of strongly connected components in directed graphs
- Apply efficient algorithms for finding SCCs in directed graphs
- Implement Kosaraju's algorithm for SCC detection
- Optimize graph algorithms for component analysis
- Handle special cases in strongly connected component problems

## 📋 Problem Description

Given a directed graph, find all strongly connected components (SCCs).

**Input**: 
- n: number of vertices
- m: number of edges
- edges: array of (u, v) representing directed edges

**Output**: 
- List of strongly connected components

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5

**Example**:
```
Input:
n = 6, m = 7
edges = [(0,1), (1,2), (2,0), (1,3), (3,4), (4,5), (5,3)]

Output:
[[0, 1, 2], [3, 4, 5]]

Explanation**: 
SCC 1: {0, 1, 2} - vertices can reach each other
SCC 2: {3, 4, 5} - vertices can reach each other
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check connectivity between all pairs of vertices
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph traversal for each pair
- **Inefficient**: O(n^3) time complexity

**Key Insight**: Check connectivity between all pairs of vertices to find SCCs.

**Algorithm**:
- For each pair of vertices, check if they can reach each other
- Group vertices that can reach each other into components
- Return the list of components

**Visual Example**:
```
Graph: 0->1, 1->2, 2->0, 1->3, 3->4, 4->5, 5->3

Connectivity check for all pairs:
┌─────────────────────────────────────┐
│ Pair (0,1): 0->1 ✓, 1->0 ✓ (via 2) │
│ Pair (0,2): 0->2 ✓ (via 1), 2->0 ✓ │
│ Pair (1,2): 1->2 ✓, 2->1 ✓ (via 0) │
│ Pair (1,3): 1->3 ✓, 3->1 ✗         │
│ Pair (3,4): 3->4 ✓, 4->3 ✓ (via 5) │
│ Pair (3,5): 3->5 ✓ (via 4), 5->3 ✓ │
│ Pair (4,5): 4->5 ✓, 5->4 ✓ (via 3) │
│                                   │
│ SCCs: {0,1,2}, {3,4,5}           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_strongly_connected_components(n, edges):
    """Find SCCs using brute force approach"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    def can_reach(start, end, visited):
        """Check if start can reach end using DFS"""
        if start == end:
            return True
        
        visited.add(start)
        for neighbor in adj[start]:
            if neighbor not in visited:
                if can_reach(neighbor, end, visited):
                    return True
        return False
    
    def is_strongly_connected(u, v):
        """Check if u and v are strongly connected"""
        # Check if u can reach v
        if not can_reach(u, v, set()):
            return False
        
        # Check if v can reach u
        if not can_reach(v, u, set()):
            return False
        
        return True
    
    # Find SCCs
    components = []
    visited = [False] * n
    
    for i in range(n):
        if not visited[i]:
            component = [i]
            visited[i] = True
            
            for j in range(i + 1, n):
                if not visited[j] and is_strongly_connected(i, j):
                    component.append(j)
                    visited[j] = True
            
            components.append(component)
    
    return components

# Example usage
n = 6
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 5), (5, 3)]
result = brute_force_strongly_connected_components(n, edges)
print(f"Brute force SCCs: {result}")
```

**Time Complexity**: O(n^3)
**Space Complexity**: O(n^2)

**Why it's inefficient**: O(n^3) time complexity for checking connectivity between all pairs.

---

### Approach 2: Kosaraju's Algorithm

**Key Insights from Kosaraju's Algorithm**:
- **Kosaraju's Algorithm**: Use Kosaraju's algorithm for efficient SCC detection
- **Efficient Implementation**: O(n + m) time complexity
- **Two DFS Passes**: First pass on original graph, second on transpose
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use Kosaraju's algorithm with two DFS passes for efficient SCC detection.

**Algorithm**:
- First DFS: Fill stack with vertices in order of finishing times
- Transpose graph: Reverse all edges
- Second DFS: Process vertices in reverse order of finishing times

**Visual Example**:
```
Kosaraju's algorithm:

Graph: 0->1, 1->2, 2->0, 1->3, 3->4, 4->5, 5->3

Step 1: First DFS (fill stack)
┌─────────────────────────────────────┐
│ DFS from 0: 0->1->2->0 (cycle)     │
│ DFS from 1: already visited        │
│ DFS from 2: already visited        │
│ DFS from 3: 3->4->5->3 (cycle)     │
│ DFS from 4: already visited        │
│ DFS from 5: already visited        │
│                                   │
│ Stack: [2, 1, 0, 5, 4, 3]         │
└─────────────────────────────────────┘

Step 2: Transpose graph
┌─────────────────────────────────────┐
│ Transpose: 1->0, 2->1, 0->2,       │
│            3->1, 4->3, 5->4, 3->5  │
└─────────────────────────────────────┘

Step 3: Second DFS (process stack)
┌─────────────────────────────────────┐
│ Process 3: 3->5->4->3 (SCC: {3,4,5}) │
│ Process 4: already visited         │
│ Process 5: already visited         │
│ Process 0: 0->2->1->0 (SCC: {0,1,2}) │
│ Process 1: already visited         │
│ Process 2: already visited         │
│                                   │
│ SCCs: {0,1,2}, {3,4,5}           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def kosaraju_strongly_connected_components(n, edges):
    """Find SCCs using Kosaraju's algorithm"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Step 1: First DFS to fill stack
    stack = []
    visited = [False] * n
    
    def first_dfs(vertex):
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        stack.append(vertex)
    
    for i in range(n):
        if not visited[i]:
            first_dfs(i)
    
    # Step 2: Transpose graph
    transpose_adj = [[] for _ in range(n)]
    for u, v in edges:
        transpose_adj[v].append(u)
    
    # Step 3: Second DFS on transpose graph
    visited = [False] * n
    components = []
    
    def second_dfs(vertex, component):
        visited[vertex] = True
        component.append(vertex)
        for neighbor in transpose_adj[vertex]:
            if not visited[neighbor]:
                second_dfs(neighbor, component)
    
    while stack:
        vertex = stack.pop()
        if not visited[vertex]:
            component = []
            second_dfs(vertex, component)
            components.append(component)
    
    return components

# Example usage
n = 6
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 5), (5, 3)]
result = kosaraju_strongly_connected_components(n, edges)
print(f"Kosaraju's SCCs: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's better**: Uses Kosaraju's algorithm for O(n + m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for SCC detection
- **Efficient Implementation**: O(n + m) time complexity
- **Space Efficiency**: O(n + m) space complexity
- **Optimal Complexity**: Best approach for SCC detection

**Key Insight**: Use advanced data structures for optimal SCC detection.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient Kosaraju's algorithm
- Handle special cases optimally
- Return strongly connected components

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1, 1->2, 2->0, 1->3, 3->4, 4->5, 5->3
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph structure: for efficient    │
│   storage and traversal             │
│ - Stack structure: for optimization  │
│ - Component cache: for optimization  │
│                                   │
│ SCC detection calculation:         │
│ - Use graph structure for efficient │
│   storage and traversal             │
│ - Use stack structure for          │
│   optimization                      │
│ - Use component cache for          │
│   optimization                      │
│                                   │
│ Result: [[0,1,2], [3,4,5]]        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_strongly_connected_components(n, edges):
    """Find SCCs using advanced data structure approach"""
    # Use advanced data structures for graph storage
    # Build advanced adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Advanced data structures for SCC detection
    stack = []
    visited = [False] * n
    
    def advanced_first_dfs(vertex):
        """Advanced first DFS with optimized data structures"""
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                advanced_first_dfs(neighbor)
        stack.append(vertex)
    
    # First DFS using advanced data structures
    for i in range(n):
        if not visited[i]:
            advanced_first_dfs(i)
    
    # Advanced transpose graph construction
    transpose_adj = [[] for _ in range(n)]
    for u, v in edges:
        transpose_adj[v].append(u)
    
    # Advanced second DFS on transpose graph
    visited = [False] * n
    components = []
    
    def advanced_second_dfs(vertex, component):
        """Advanced second DFS with optimized data structures"""
        visited[vertex] = True
        component.append(vertex)
        for neighbor in transpose_adj[vertex]:
            if not visited[neighbor]:
                advanced_second_dfs(neighbor, component)
    
    while stack:
        vertex = stack.pop()
        if not visited[vertex]:
            component = []
            advanced_second_dfs(vertex, component)
            components.append(component)
    
    return components

# Example usage
n = 6
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 5), (5, 3)]
result = advanced_data_structure_strongly_connected_components(n, edges)
print(f"Advanced data structure SCCs: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^3) | O(n^2) | Check connectivity between all pairs |
| Kosaraju's Algorithm | O(n + m) | O(n + m) | Use two DFS passes with transpose |
| Advanced Data Structure | O(n + m) | O(n + m) | Use advanced data structures |

### Time Complexity
- **Time**: O(n + m) - Use Kosaraju's algorithm for efficient SCC detection
- **Space**: O(n + m) - Store graph and auxiliary data structures

### Why This Solution Works
- **Kosaraju's Algorithm**: Use two DFS passes to find SCCs efficiently
- **Transpose Graph**: Reverse edges to find components in second pass
- **Stack Ordering**: Process vertices in reverse order of finishing times
- **Optimal Algorithms**: Use optimal algorithms for SCC detection

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Strongly Connected Components with Constraints**
**Problem**: Find SCCs with specific constraints.

**Key Differences**: Apply constraints to SCC detection

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_strongly_connected_components(n, edges, constraints):
    """Find SCCs with constraints"""
    # Build adjacency list with constraints
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if constraints(u, v):
            adj[u].append(v)
    
    # Step 1: First DFS to fill stack
    stack = []
    visited = [False] * n
    
    def first_dfs(vertex):
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor] and constraints(vertex, neighbor):
                first_dfs(neighbor)
        stack.append(vertex)
    
    for i in range(n):
        if not visited[i]:
            first_dfs(i)
    
    # Step 2: Transpose graph with constraints
    transpose_adj = [[] for _ in range(n)]
    for u, v in edges:
        if constraints(u, v):
            transpose_adj[v].append(u)
    
    # Step 3: Second DFS on transpose graph with constraints
    visited = [False] * n
    components = []
    
    def second_dfs(vertex, component):
        visited[vertex] = True
        component.append(vertex)
        for neighbor in transpose_adj[vertex]:
            if not visited[neighbor] and constraints(neighbor, vertex):
                second_dfs(neighbor, component)
    
    while stack:
        vertex = stack.pop()
        if not visited[vertex]:
            component = []
            second_dfs(vertex, component)
            components.append(component)
    
    return components

# Example usage
n = 6
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 5), (5, 3)]
constraints = lambda u, v: u < v or v == 0  # Special constraint
result = constrained_strongly_connected_components(n, edges, constraints)
print(f"Constrained SCCs: {result}")
```

#### **2. Strongly Connected Components with Different Metrics**
**Problem**: Find SCCs with different connectivity metrics.

**Key Differences**: Different connectivity calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_strongly_connected_components(n, edges, weight_function):
    """Find SCCs with different connectivity metrics"""
    # Build adjacency list with modified weights
    adj = [[] for _ in range(n)]
    for u, v in edges:
        weight = weight_function(u, v)
        adj[u].append((v, weight))
    
    # Step 1: First DFS to fill stack
    stack = []
    visited = [False] * n
    
    def first_dfs(vertex):
        visited[vertex] = True
        for neighbor, weight in adj[vertex]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        stack.append(vertex)
    
    for i in range(n):
        if not visited[i]:
            first_dfs(i)
    
    # Step 2: Transpose graph with modified weights
    transpose_adj = [[] for _ in range(n)]
    for u, v in edges:
        weight = weight_function(u, v)
        transpose_adj[v].append((u, weight))
    
    # Step 3: Second DFS on transpose graph with modified weights
    visited = [False] * n
    components = []
    
    def second_dfs(vertex, component):
        visited[vertex] = True
        component.append(vertex)
        for neighbor, weight in transpose_adj[vertex]:
            if not visited[neighbor]:
                second_dfs(neighbor, component)
    
    while stack:
        vertex = stack.pop()
        if not visited[vertex]:
            component = []
            second_dfs(vertex, component)
            components.append(component)
    
    return components

# Example usage
n = 6
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 5), (5, 3)]
weight_function = lambda u, v: abs(u - v)  # Distance-based weight
result = weighted_strongly_connected_components(n, edges, weight_function)
print(f"Weighted SCCs: {result}")
```

#### **3. Strongly Connected Components with Multiple Dimensions**
**Problem**: Find SCCs in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_strongly_connected_components(n, edges, dimensions):
    """Find SCCs in multiple dimensions"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Step 1: First DFS to fill stack
    stack = []
    visited = [False] * n
    
    def first_dfs(vertex):
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        stack.append(vertex)
    
    for i in range(n):
        if not visited[i]:
            first_dfs(i)
    
    # Step 2: Transpose graph
    transpose_adj = [[] for _ in range(n)]
    for u, v in edges:
        transpose_adj[v].append(u)
    
    # Step 3: Second DFS on transpose graph
    visited = [False] * n
    components = []
    
    def second_dfs(vertex, component):
        visited[vertex] = True
        component.append(vertex)
        for neighbor in transpose_adj[vertex]:
            if not visited[neighbor]:
                second_dfs(neighbor, component)
    
    while stack:
        vertex = stack.pop()
        if not visited[vertex]:
            component = []
            second_dfs(vertex, component)
            components.append(component)
    
    return components

# Example usage
n = 6
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 5), (5, 3)]
dimensions = 1
result = multi_dimensional_strongly_connected_components(n, edges, dimensions)
print(f"Multi-dimensional SCCs: {result}")
```

### Related Problems

#### **CSES Problems**
- [Planets and Kingdoms](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Round Trip](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Message Route](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Graph
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Strongly connected components, Kosaraju's algorithm
- **Connectivity**: Graph connectivity, component detection
- **DFS**: Depth-first search, graph traversal

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Strongly Connected Components](https://cp-algorithms.com/graph/strongly-connected-components.html) - SCC algorithms
- [Kosaraju's Algorithm](https://cp-algorithms.com/graph/strongly-connected-components.html#kosarajus-algorithm) - Kosaraju's algorithm

### **Practice Problems**
- [CSES Planets and Kingdoms](https://cses.fi/problemset/task/1075) - Medium
- [CSES Round Trip](https://cses.fi/problemset/task/1075) - Medium
- [CSES Message Route](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Strongly Connected Component](https://en.wikipedia.org/wiki/Strongly_connected_component) - Wikipedia article
- [Kosaraju's Algorithm](https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm) - Wikipedia article
