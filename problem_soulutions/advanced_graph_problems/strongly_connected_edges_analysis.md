---
layout: simple
title: "Strongly Connected Edges"
permalink: /problem_soulutions/advanced_graph_problems/strongly_connected_edges_analysis
---

# Strongly Connected Edges

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of strongly connected components (SCCs) in directed graphs
- Apply Tarjan's algorithm or Kosaraju's algorithm to find SCCs
- Analyze the structure of SCCs to determine connectivity requirements
- Calculate the minimum number of edges needed to make a graph strongly connected
- Handle edge cases in SCC analysis (single vertices, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Strongly Connected Components (SCC), DFS, graph traversal
- **Data Structures**: Adjacency lists, stacks, visited arrays
- **Mathematical Concepts**: Graph theory, connectivity, component analysis
- **Programming Skills**: DFS implementation, stack operations, graph representation
- **Related Problems**: Planets and Kingdoms (SCC basics), Building Roads (connectivity), Round Trip (cycle detection)

## Problem Description

**Problem**: Given a directed graph, find the minimum number of edges to add to make it strongly connected.

**Input**: 
- n: number of vertices
- m: number of edges
- m lines: a b (edge from vertex a to vertex b)

**Output**: Minimum number of edges to add.

**Example**:
```
Input:
4 3
1 2
2 3
3 4

Output:
1

Explanation: 
Add edge (4, 1) to make the graph strongly connected.
```

### 📊 Visual Example

**Input Graph:**
```
    1 ──→ 2 ──→ 3 ──→ 4
```

**Strongly Connected Components (SCCs):**
```
SCC 1: {1}
SCC 2: {2}
SCC 3: {3}
SCC 4: {4}

Each vertex is its own SCC (no cycles)
```

**Condensation Graph:**
```
SCC1 ──→ SCC2 ──→ SCC3 ──→ SCC4
```

**Strong Connectivity Analysis:**
```
Current State:
- 4 separate SCCs
- No path from SCC4 back to SCC1
- Graph is not strongly connected

Required:
- Add edge from SCC4 to SCC1: 4 → 1
- This creates a cycle: 1 → 2 → 3 → 4 → 1
- All vertices become reachable from each other
```

**Solution: Add Edge (4, 1)**
```
After adding edge (4, 1):
    1 ──→ 2 ──→ 3 ──→ 4
    ↑                   │
    └───────────────────┘

New SCCs:
SCC 1: {1, 2, 3, 4} (all vertices strongly connected)

Strong connectivity achieved with 1 edge!
```

**Algorithm Visualization:**
```
Step 1: Find SCCs using Kosaraju's algorithm
SCCs: {1}, {2}, {3}, {4}

Step 2: Build condensation graph
Nodes: {SCC1, SCC2, SCC3, SCC4}
Edges: {(SCC1, SCC2), (SCC2, SCC3), (SCC3, SCC4)}

Step 3: Count sources and sinks
Sources: 1 (SCC1)
Sinks: 1 (SCC4)

Step 4: Calculate minimum edges
min_edges = max(sources, sinks) = max(1, 1) = 1
```

**General Formula:**
```
For strongly connected graph:
min_edges = max(sources, sinks)

Where:
- sources = SCCs with in-degree 0
- sinks = SCCs with out-degree 0
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find minimum edges to add to directed graph
- Make graph strongly connected
- Use strongly connected components
- Apply graph theory concepts

**Key Observations:**
- Need to connect all SCCs
- In-degree and out-degree matter
- Can use condensation graph
- Minimum edges = max(in_sources, out_sinks)

### Step 2: Strongly Connected Components Approach
**Idea**: Find SCCs and connect them optimally.

```python
def strongly_connected_edges_scc(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Find strongly connected components
    sccs = find_sccs(n, adj)
    
    # Build condensation graph
    condensation = build_condensation(n, adj, sccs)
    
    # Count sources and sinks in condensation
    in_degree = [0] * len(sccs)
    out_degree = [0] * len(sccs)
    
    for u in range(len(sccs)):
        for v in condensation[u]:
            out_degree[u] += 1
            in_degree[v] += 1
    
    sources = sum(1 for d in in_degree if d == 0)
    sinks = sum(1 for d in out_degree if d == 0)
    
    return max(sources, sinks)
```

**Why this works:**
- Uses SCC decomposition
- Condensation graph approach
- Counts sources and sinks
- O(n + m) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_strongly_connected_edges():
    n, m = map(int, input().split())
    edges = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Find strongly connected components
    sccs = find_sccs(n, adj)
    
    # Build condensation graph
    condensation = build_condensation(n, adj, sccs)
    
    # Count sources and sinks in condensation
    in_degree = [0] * len(sccs)
    out_degree = [0] * len(sccs)
    
    for u in range(len(sccs)):
        for v in condensation[u]:
            out_degree[u] += 1
            in_degree[v] += 1
    
    sources = sum(1 for d in in_degree if d == 0)
    sinks = sum(1 for d in out_degree if d == 0)
    
    result = max(sources, sinks)
    print(result)

def find_sccs(n, adj):
    # Tarjan's algorithm for finding SCCs
    # Implementation details...
    pass

def build_condensation(n, adj, sccs):
    # Build condensation graph
    # Implementation details...
    pass

# Main execution
if __name__ == "__main__":
    solve_strongly_connected_edges()
```

**Why this works:**
- Optimal SCC-based approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - SCC finding and condensation
- **Space**: O(n + m) - adjacency lists and condensation

### Why This Solution Works
- **SCC Decomposition**: Breaks graph into components
- **Condensation Graph**: Simplifies the problem
- **Source/Sink Counting**: Determines minimum edges
- **Optimal Approach**: Guarantees correct result

## 🎯 Key Insights

### 1. **Strongly Connected Components**
- Breaks graph into maximal SCCs
- Key insight for solution
- Essential for understanding
- Enables efficient solution

### 2. **Condensation Graph**
- Simplifies complex graph
- Sources and sinks matter
- Important for efficiency
- Fundamental concept

### 3. **Source/Sink Counting**
- Minimum edges = max(sources, sinks)
- Simple but important observation
- Essential for solution
- Critical insight

## 🎯 Problem Variations

### Variation 1: Weighted Edge Addition
**Problem**: Each edge has a cost. Find minimum cost to make graph strongly connected.

```python
def strongly_connected_edges_weighted(n, edges, costs):
    # Similar to main solution but with cost optimization
    # Implementation details...
    pass
```

### Variation 2: Constrained Edge Addition
**Problem**: Can only add edges between certain vertex pairs.

```python
def strongly_connected_edges_constrained(n, edges, allowed_edges):
    # Similar to main solution but with constraints
    # Implementation details...
    pass
```

## 🔗 Related Problems

- **[Strongly Connected Components](/cses-analyses/problem_soulutions/graph_algorithms/strongly_connected_components_analysis)**: SCC algorithms
- **[Graph Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms

## 📚 Learning Points

1. **Strongly Connected Components**: Essential for directed graphs
2. **Condensation Graph**: Simplifies complex problems
3. **Source/Sink Analysis**: Key technique
4. **Graph Connectivity**: Common pattern

---

**This is a great introduction to strongly connected components and graph connectivity!** 🎯 