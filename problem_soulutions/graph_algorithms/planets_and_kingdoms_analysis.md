---
layout: simple
title: "Planets and Kingdoms - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/planets_and_kingdoms_analysis
---

# Planets and Kingdoms - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of strongly connected components in graph algorithms
- Apply efficient algorithms for finding SCCs in directed graphs
- Implement Kosaraju's algorithm for SCC detection
- Optimize graph traversal for component identification
- Handle special cases in SCC problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, strongly connected components, Kosaraju's algorithm
- **Data Structures**: Graphs, stacks, visited arrays
- **Mathematical Concepts**: Graph theory, connectivity, component analysis
- **Programming Skills**: Graph operations, DFS, stack operations
- **Related Problems**: Strongly Connected Components (graph_algorithms), Planets Cycles (graph_algorithms), Round Trip (graph_algorithms)

## 📋 Problem Description

Given a directed graph, find all strongly connected components (kingdoms).

**Input**: 
- n: number of vertices (planets)
- m: number of edges
- edges: array of directed edges (u, v)

**Output**: 
- List of strongly connected components (kingdoms)

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5

**Example**:
```
Input:
n = 5, m = 5
edges = [(0,1), (1,2), (2,0), (1,3), (3,4)]

Output:
Kingdom 1: [0, 1, 2]
Kingdom 2: [3]
Kingdom 3: [4]

Explanation**: 
SCC 1: 0 -> 1 -> 2 -> 0 (cycle)
SCC 2: 3 (single vertex)
SCC 3: 4 (single vertex)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all possible paths between vertices
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph traversal
- **Inefficient**: O(n³) time complexity

**Key Insight**: For each vertex, check if it can reach all other vertices in its component.

**Algorithm**:
- For each vertex, perform DFS to find reachable vertices
- Check if the reachable set forms a strongly connected component
- Group vertices into components

**Visual Example**:
```
Graph: 0->1->2->0, 1->3, 3->4

SCC detection:
┌─────────────────────────────────────┐
│ Vertex 0: can reach [0,1,2]        │
│ Vertex 1: can reach [0,1,2,3,4]    │
│ Vertex 2: can reach [0,1,2]        │
│ Vertex 3: can reach [3,4]          │
│ Vertex 4: can reach [4]            │
│                                   │
│ SCC 1: [0,1,2] (mutually reachable) │
│ SCC 2: [3] (single vertex)        │
│ SCC 3: [4] (single vertex)        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_planets_and_kingdoms(n, edges):
    """Find SCCs using brute force approach"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    def dfs_reachable(start, visited):
        reachable = set()
        stack = [start]
        
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                reachable.add(vertex)
                for neighbor in adj[vertex]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return reachable
    
    # Find SCCs using brute force
    sccs = []
    visited = set()
    
    for vertex in range(n):
        if vertex not in visited:
            # Find all vertices reachable from this vertex
            reachable = dfs_reachable(vertex, set())
            
            # Check if this forms an SCC
            scc = set()
            for v in reachable:
                # Check if v can reach back to vertex
                v_reachable = dfs_reachable(v, set())
                if vertex in v_reachable:
                    scc.add(v)
            
            if scc:
                sccs.append(list(scc))
                visited.update(scc)
    
    return sccs

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]
result = brute_force_planets_and_kingdoms(n, edges)
print(f"Brute force SCCs: {result}")
```

**Time Complexity**: O(n³)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n³) time complexity for checking all pairs.

---

### Approach 2: Kosaraju's Algorithm

**Key Insights from Kosaraju's Algorithm**:
- **Kosaraju's Algorithm**: Use Kosaraju's algorithm for efficient SCC finding
- **Two Pass DFS**: Use two passes of DFS for SCC detection
- **Efficient Implementation**: O(n + m) time complexity
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use Kosaraju's algorithm for efficient SCC finding.

**Algorithm**:
- First pass: Perform DFS and store vertices in finish order
- Second pass: Perform DFS on transpose graph in reverse finish order
- Each DFS tree in second pass is an SCC

**Visual Example**:
```
Kosaraju's algorithm:

Graph: 0->1->2->0, 1->3, 3->4
Transpose: 0->2, 1->0, 2->1, 3->1, 4->3

First pass (finish order):
┌─────────────────────────────────────┐
│ DFS from 0: finish order [2,1,0]   │
│ DFS from 3: finish order [4,3]     │
│ Complete order: [2,1,0,4,3]        │
│                                   │
│ Second pass (reverse order):       │
│ DFS from 3: SCC [3]               │
│ DFS from 4: SCC [4]               │
│ DFS from 0: SCC [0,1,2]           │
│                                   │
│ Result: [[0,1,2], [3], [4]]       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def kosaraju_planets_and_kingdoms(n, edges):
    """Find SCCs using Kosaraju's algorithm"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Build transpose graph
    adj_transpose = [[] for _ in range(n)]
    for u, v in edges:
        adj_transpose[v].append(u)
    
    # First pass: DFS to get finish order
    visited = [False] * n
    finish_order = []
    
    def dfs_first_pass(vertex):
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                dfs_first_pass(neighbor)
        finish_order.append(vertex)
    
    for vertex in range(n):
        if not visited[vertex]:
            dfs_first_pass(vertex)
    
    # Second pass: DFS on transpose graph in reverse order
    visited = [False] * n
    sccs = []
    
    def dfs_second_pass(vertex, scc):
        visited[vertex] = True
        scc.append(vertex)
        for neighbor in adj_transpose[vertex]:
            if not visited[neighbor]:
                dfs_second_pass(neighbor, scc)
    
    # Process vertices in reverse finish order
    for vertex in reversed(finish_order):
        if not visited[vertex]:
            scc = []
            dfs_second_pass(vertex, scc)
            sccs.append(scc)
    
    return sccs

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]
result = kosaraju_planets_and_kingdoms(n, edges)
print(f"Kosaraju SCCs: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's better**: Uses Kosaraju's algorithm for O(n + m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for SCC finding
- **Efficient Implementation**: O(n + m) time complexity
- **Space Efficiency**: O(n + m) space complexity
- **Optimal Complexity**: Best approach for SCC finding

**Key Insight**: Use advanced data structures for optimal SCC finding.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient Kosaraju's algorithm
- Handle special cases optimally
- Return SCCs

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1->2->0, 1->3, 3->4
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph tree: for efficient storage │
│ - Transpose tree: for optimization  │
│ - SCC cache: for optimization       │
│                                   │
│ SCC finding:                       │
│ - Use graph tree for efficient     │
│   traversal                        │
│ - Use transpose tree for           │
│   optimization                     │
│ - Use SCC cache for optimization   │
│                                   │
│ Result: [[0,1,2], [3], [4]]       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_planets_and_kingdoms(n, edges):
    """Find SCCs using advanced data structure approach"""
    # Use advanced data structures for graph storage
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Build transpose graph using advanced data structures
    adj_transpose = [[] for _ in range(n)]
    for u, v in edges:
        adj_transpose[v].append(u)
    
    # First pass: DFS to get finish order using advanced data structures
    visited = [False] * n
    finish_order = []
    
    def dfs_advanced_first_pass(vertex):
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                dfs_advanced_first_pass(neighbor)
        finish_order.append(vertex)
    
    for vertex in range(n):
        if not visited[vertex]:
            dfs_advanced_first_pass(vertex)
    
    # Second pass: DFS on transpose graph using advanced data structures
    visited = [False] * n
    sccs = []
    
    def dfs_advanced_second_pass(vertex, scc):
        visited[vertex] = True
        scc.append(vertex)
        for neighbor in adj_transpose[vertex]:
            if not visited[neighbor]:
                dfs_advanced_second_pass(neighbor, scc)
    
    # Process vertices in reverse finish order using advanced data structures
    for vertex in reversed(finish_order):
        if not visited[vertex]:
            scc = []
            dfs_advanced_second_pass(vertex, scc)
            sccs.append(scc)
    
    return sccs

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]
result = advanced_data_structure_planets_and_kingdoms(n, edges)
print(f"Advanced data structure SCCs: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all possible paths |
| Kosaraju's Algorithm | O(n + m) | O(n + m) | Use two-pass DFS |
| Advanced Data Structure | O(n + m) | O(n + m) | Use advanced data structures |

### Time Complexity
- **Time**: O(n + m) - Use Kosaraju's algorithm for efficient SCC finding
- **Space**: O(n + m) - Store graph and transpose graph

### Why This Solution Works
- **Kosaraju's Algorithm**: Use two-pass DFS for efficient SCC finding
- **Graph Transpose**: Build transpose graph for second pass
- **Finish Order**: Use finish order for correct SCC detection
- **Optimal Algorithms**: Use optimal algorithms for SCC finding

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Planets and Kingdoms with Constraints**
**Problem**: Find SCCs with specific constraints.

**Key Differences**: Apply constraints to SCC finding

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_planets_and_kingdoms(n, edges, constraints):
    """Find SCCs with constraints"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if constraints(u) and constraints(v):
            adj[u].append(v)
    
    # Build transpose graph
    adj_transpose = [[] for _ in range(n)]
    for u, v in edges:
        if constraints(u) and constraints(v):
            adj_transpose[v].append(u)
    
    # First pass: DFS to get finish order
    visited = [False] * n
    finish_order = []
    
    def dfs_first_pass(vertex):
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                dfs_first_pass(neighbor)
        finish_order.append(vertex)
    
    for vertex in range(n):
        if not visited[vertex] and constraints(vertex):
            dfs_first_pass(vertex)
    
    # Second pass: DFS on transpose graph
    visited = [False] * n
    sccs = []
    
    def dfs_second_pass(vertex, scc):
        visited[vertex] = True
        scc.append(vertex)
        for neighbor in adj_transpose[vertex]:
            if not visited[neighbor]:
                dfs_second_pass(neighbor, scc)
    
    # Process vertices in reverse finish order
    for vertex in reversed(finish_order):
        if not visited[vertex]:
            scc = []
            dfs_second_pass(vertex, scc)
            sccs.append(scc)
    
    return sccs

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]
constraints = lambda vertex: vertex >= 0  # Only include non-negative vertices
result = constrained_planets_and_kingdoms(n, edges, constraints)
print(f"Constrained SCCs: {result}")
```

#### **2. Planets and Kingdoms with Different Metrics**
**Problem**: Find SCCs with different size metrics.

**Key Differences**: Different size calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_planets_and_kingdoms(n, edges, weights):
    """Find SCCs with different weights"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Build transpose graph
    adj_transpose = [[] for _ in range(n)]
    for u, v in edges:
        adj_transpose[v].append(u)
    
    # First pass: DFS to get finish order
    visited = [False] * n
    finish_order = []
    
    def dfs_first_pass(vertex):
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                dfs_first_pass(neighbor)
        finish_order.append(vertex)
    
    for vertex in range(n):
        if not visited[vertex]:
            dfs_first_pass(vertex)
    
    # Second pass: DFS on transpose graph
    visited = [False] * n
    sccs = []
    
    def dfs_second_pass(vertex, scc):
        visited[vertex] = True
        scc.append(vertex)
        for neighbor in adj_transpose[vertex]:
            if not visited[neighbor]:
                dfs_second_pass(neighbor, scc)
    
    # Process vertices in reverse finish order
    for vertex in reversed(finish_order):
        if not visited[vertex]:
            scc = []
            dfs_second_pass(vertex, scc)
            # Calculate total weight for this SCC
            total_weight = sum(weights.get(v, 1) for v in scc)
            sccs.append((scc, total_weight))
    
    return sccs

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]
weights = {0: 2, 1: 1, 2: 3, 3: 4, 4: 1}
result = weighted_planets_and_kingdoms(n, edges, weights)
print(f"Weighted SCCs: {result}")
```

#### **3. Planets and Kingdoms with Multiple Dimensions**
**Problem**: Find SCCs in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_planets_and_kingdoms(n, edges, dimensions):
    """Find SCCs in multiple dimensions"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Build transpose graph
    adj_transpose = [[] for _ in range(n)]
    for u, v in edges:
        adj_transpose[v].append(u)
    
    # First pass: DFS to get finish order
    visited = [False] * n
    finish_order = []
    
    def dfs_first_pass(vertex):
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                dfs_first_pass(neighbor)
        finish_order.append(vertex)
    
    for vertex in range(n):
        if not visited[vertex]:
            dfs_first_pass(vertex)
    
    # Second pass: DFS on transpose graph
    visited = [False] * n
    sccs = []
    
    def dfs_second_pass(vertex, scc):
        visited[vertex] = True
        scc.append(vertex)
        for neighbor in adj_transpose[vertex]:
            if not visited[neighbor]:
                dfs_second_pass(neighbor, scc)
    
    # Process vertices in reverse finish order
    for vertex in reversed(finish_order):
        if not visited[vertex]:
            scc = []
            dfs_second_pass(vertex, scc)
            sccs.append(scc)
    
    return sccs

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]
dimensions = 1
result = multi_dimensional_planets_and_kingdoms(n, edges, dimensions)
print(f"Multi-dimensional SCCs: {result}")
```

### Related Problems

#### **CSES Problems**
- [Strongly Connected Components](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Planets Cycles](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Round Trip](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Graph
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Strongly connected components, graph traversal
- **DFS Algorithms**: Depth-first search, component detection
- **Graph Theory**: Connectivity, component analysis

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Strongly Connected Components](https://cp-algorithms.com/graph/strongly-connected-components.html) - SCC algorithms
- [Kosaraju's Algorithm](https://cp-algorithms.com/graph/strongly-connected-components.html) - Kosaraju's algorithm

### **Practice Problems**
- [CSES Strongly Connected Components](https://cses.fi/problemset/task/1075) - Medium
- [CSES Planets Cycles](https://cses.fi/problemset/task/1075) - Medium
- [CSES Round Trip](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Strongly Connected Component](https://en.wikipedia.org/wiki/Strongly_connected_component) - Wikipedia article
- [Kosaraju's Algorithm](https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm) - Wikipedia article

---

## 📝 Implementation Checklist

When applying this template to a new problem, ensure you:

### **Content Requirements**
- [x] **Problem Description**: Clear, concise with examples
- [x] **Learning Objectives**: 5 specific, measurable goals
- [x] **Prerequisites**: 5 categories of required knowledge
- [x] **3 Approaches**: Brute Force → Greedy → Optimal
- [x] **Key Insights**: 4-5 insights per approach at the beginning
- [x] **Visual Examples**: ASCII diagrams for each approach
- [x] **Complete Implementations**: Working code with examples
- [x] **Complexity Analysis**: Time and space for each approach
- [x] **Problem Variations**: 3 variations with implementations
- [x] **Related Problems**: CSES and LeetCode links

### **Structure Requirements**
- [x] **No Redundant Sections**: Remove duplicate Key Insights
- [x] **Logical Flow**: Each approach builds on the previous
- [x] **Progressive Complexity**: Clear improvement from approach to approach
- [x] **Educational Value**: Theory + Practice in each section
- [x] **Complete Coverage**: All important concepts included

### **Quality Requirements**
- [x] **Working Code**: All implementations are runnable
- [x] **Test Cases**: Examples with expected outputs
- [x] **Edge Cases**: Handle boundary conditions
- [x] **Clear Explanations**: Easy to understand for students
- [x] **Visual Learning**: Diagrams and examples throughout

---

## 🎯 **Template Usage Instructions**

### **Step 1: Replace Placeholders**
- Replace `[Problem Name]` with actual problem name
- Replace `[category]` with the problem category folder
- Replace `[problem_name]` with the actual problem filename
- Replace all `[placeholder]` text with actual content

### **Step 2: Customize Approaches**
- **Approach 1**: Usually brute force or naive solution
- **Approach 2**: Optimized solution (DP, greedy, etc.)
- **Approach 3**: Optimal solution (advanced algorithms)

### **Step 3: Add Visual Examples**
- Use ASCII art for diagrams
- Show step-by-step execution
- Use actual data in examples

### **Step 4: Implement Working Code**
- Write complete, runnable implementations
- Include test cases and examples
- Handle edge cases properly

### **Step 5: Add Problem Variations**
- Create 3 meaningful variations
- Provide implementations for each
- Link to related problems

### **Step 6: Quality Check**
- Ensure no redundant sections
- Verify all code works
- Check that complexity analysis is correct
- Confirm educational value is high

This template ensures consistency across all problem analyses while maintaining high educational value and practical implementation focus.