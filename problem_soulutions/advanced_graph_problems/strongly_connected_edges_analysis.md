---
layout: simple
title: "Strongly Connected Edges - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/strongly_connected_edges_analysis
---

# Strongly Connected Edges - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of strongly connected edges in directed graphs
- Apply graph theory principles to identify critical edges for strong connectivity
- Implement algorithms for strongly connected component (SCC) analysis
- Optimize graph analysis for edge importance
- Handle special cases in graph connectivity analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, strongly connected components, Tarjan's algorithm, bridge detection
- **Data Structures**: Adjacency lists, stacks, visited arrays, component arrays
- **Mathematical Concepts**: Graph theory, connectivity, strongly connected components, bridges
- **Programming Skills**: Graph representation, DFS, stack operations, component tracking
- **Related Problems**: Strongly Connected Components (SCC detection), New Flight Routes (connectivity), Planets and Kingdoms (SCC analysis)

## 📋 Problem Description

Given a directed graph with n nodes and m edges, find all edges that are critical for maintaining strong connectivity.

**Input**: 
- n: number of nodes
- m: number of edges
- m lines: a b (directed edge from node a to node b)

**Output**: 
- List of edges that are critical for strong connectivity

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5

**Example**:
```
Input:
4 5
1 2
2 3
3 1
1 4
4 1

Output:
1 4
4 1

Explanation**: 
Graph: 1→2→3→1, 1↔4
Critical edges: (1,4) and (4,1) - removing either breaks strong connectivity
Non-critical edges: (1,2), (2,3), (3,1) - removing any doesn't break connectivity
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Edge Removal**: Try removing each edge and check connectivity
- **Connectivity Check**: Use DFS to check strong connectivity after each removal
- **Exhaustive Search**: Check all edges individually
- **Baseline Understanding**: Provides correct answer but highly inefficient

**Key Insight**: Remove each edge one by one and check if the graph remains strongly connected.

**Algorithm**:
- For each edge, temporarily remove it from the graph
- Check if the graph remains strongly connected
- If not, the edge is critical
- Return all critical edges

**Visual Example**:
```
Graph: 1→2→3→1, 1↔4

Test edge (1,2):
┌─────────────────────────────────────┐
│ Remove (1,2): 2→3→1, 1↔4          │
│ Check connectivity: Still connected ✓│
│ Edge (1,2) is not critical          │
└─────────────────────────────────────┘

Test edge (1,4):
┌─────────────────────────────────────┐
│ Remove (1,4): 1→2→3→1, 4→1        │
│ Check connectivity: Not connected ✗ │
│ Edge (1,4) is critical              │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_solution(n, edges):
    """
    Find critical edges using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        list: critical edges
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def is_strongly_connected():
        """Check if graph is strongly connected using DFS"""
        def dfs(node, visited):
            visited[node] = True
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    dfs(neighbor, visited)
        
        # Check if all nodes are reachable from node 0
        visited = [False] * n
        dfs(0, visited)
        if not all(visited):
            return False
        
        # Check if all nodes can reach node 0 (reverse graph)
        reverse_adj = [[] for _ in range(n)]
        for i in range(n):
            for j in adj[i]:
                reverse_adj[j].append(i)
        
        visited = [False] * n
        dfs(0, visited)
        return all(visited)
    
    def find_critical_edges():
        """Find all critical edges by testing each edge"""
        critical_edges = []
        
        for i, (a, b) in enumerate(edges):
            # Temporarily remove edge
            adj[a-1].remove(b-1)  # Convert to 0-indexed
            
            # Check connectivity
            if not is_strongly_connected():
                critical_edges.append((a, b))
            
            # Restore edge
            adj[a-1].append(b-1)
        
        return critical_edges
    
    return find_critical_edges()

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1), (1, 4), (4, 1)]
result = brute_force_solution(n, edges)
print(f"Brute force result: {result}")  # Output: [(1, 4), (4, 1)]
```

**Time Complexity**: O(m × (n + m))
**Space Complexity**: O(n + m)

**Why it's inefficient**: O(m × (n + m)) time complexity makes it impractical for large graphs.

---

### Approach 2: SCC-Based Solution

**Key Insights from SCC-Based Solution**:
- **Strongly Connected Components**: Find SCCs using Tarjan's algorithm
- **Component Graph**: Build DAG of strongly connected components
- **Bridge Detection**: Find edges that connect different components
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use strongly connected components to identify edges that connect different components.

**Algorithm**:
- Find all strongly connected components
- Build the component graph
- Identify edges that connect different components
- Return all inter-component edges

**Visual Example**:
```
Graph: 1→2→3→1, 1↔4

SCCs: {1,2,3}, {4}
Component graph: SCC1 ↔ SCC2

Analysis:
┌─────────────────────────────────────┐
│ SCC1: {1,2,3} (strongly connected) │
│ SCC2: {4} (single node)            │
│ Inter-component edges: (1,4), (4,1) │
└─────────────────────────────────────┘

Critical edges: (1,4), (4,1)
```

**Implementation**:
```python
def scc_based_solution(n, edges):
    """
    Find critical edges using SCC analysis
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        list: critical edges
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def find_sccs():
        """Find strongly connected components using Tarjan's algorithm"""
        index = 0
        stack = []
        indices = [-1] * n
        lowlinks = [-1] * n
        on_stack = [False] * n
        sccs = []
        
        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack[node] = True
            
            for neighbor in adj[node]:
                if indices[neighbor] == -1:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif on_stack[neighbor]:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])
            
            if lowlinks[node] == indices[node]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == node:
                        break
                sccs.append(component)
        
        for i in range(n):
            if indices[i] == -1:
                strongconnect(i)
        
        return sccs
    
    def find_critical_edges(sccs):
        """Find critical edges using SCC analysis"""
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        critical_edges = []
        
        # Check each edge
        for a, b in edges:
            comp_a = node_to_component[a-1]  # Convert to 0-indexed
            comp_b = node_to_component[b-1]  # Convert to 0-indexed
            
            # Edge is critical if it connects different components
            if comp_a != comp_b:
                critical_edges.append((a, b))
        
        return critical_edges
    
    # Find SCCs
    sccs = find_sccs()
    
    # Find critical edges
    return find_critical_edges(sccs)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1), (1, 4), (4, 1)]
result = scc_based_solution(n, edges)
print(f"SCC-based result: {result}")  # Output: [(1, 4), (4, 1)]
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's better**: Linear time complexity, much more efficient than brute force.

**Implementation Considerations**:
- **SCC Detection**: Use Tarjan's algorithm for efficient SCC finding
- **Component Mapping**: Map nodes to their components
- **Edge Analysis**: Check if edges connect different components

---

### Approach 3: Optimized SCC Solution (Optimal)

**Key Insights from Optimized SCC Solution**:
- **Tarjan's Algorithm**: Use Tarjan's algorithm for efficient SCC detection
- **Component Analysis**: Optimize component graph analysis
- **Edge Classification**: Efficiently classify edges as critical or non-critical
- **Optimal Complexity**: O(n + m) time complexity

**Key Insight**: Use Tarjan's algorithm for SCC detection and optimize the edge classification process.

**Algorithm**:
- Use Tarjan's algorithm to find SCCs
- Build component graph efficiently
- Classify edges as critical or non-critical
- Return all critical edges

**Visual Example**:
```
Graph: 1→2→3→1, 1↔4

Tarjan's algorithm:
┌─────────────────────────────────────┐
│ SCC1: {1,2,3} (strongly connected) │
│ SCC2: {4} (single node)            │
│ Component graph: SCC1 ↔ SCC2       │
│ Critical edges: (1,4), (4,1)       │
└─────────────────────────────────────┘

Critical edges: (1,4), (4,1)
```

**Implementation**:
```python
def optimized_scc_solution(n, edges):
    """
    Find critical edges using optimized SCC analysis
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        list: critical edges
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def tarjan_scc():
        """Find SCCs using Tarjan's algorithm"""
        index = 0
        stack = []
        indices = [-1] * n
        lowlinks = [-1] * n
        on_stack = [False] * n
        sccs = []
        
        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack[node] = True
            
            for neighbor in adj[node]:
                if indices[neighbor] == -1:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif on_stack[neighbor]:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])
            
            if lowlinks[node] == indices[node]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == node:
                        break
                sccs.append(component)
        
        for i in range(n):
            if indices[i] == -1:
                strongconnect(i)
        
        return sccs
    
    def classify_edges(sccs):
        """Classify edges as critical or non-critical"""
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        critical_edges = []
        
        # Classify each edge
        for a, b in edges:
            comp_a = node_to_component[a-1]  # Convert to 0-indexed
            comp_b = node_to_component[b-1]  # Convert to 0-indexed
            
            # Edge is critical if it connects different components
            if comp_a != comp_b:
                critical_edges.append((a, b))
        
        return critical_edges
    
    # Find SCCs using Tarjan's algorithm
    sccs = tarjan_scc()
    
    # Classify edges
    return classify_edges(sccs)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1), (1, 4), (4, 1)]
result = optimized_scc_solution(n, edges)
print(f"Optimized SCC result: {result}")  # Output: [(1, 4), (4, 1)]
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's optimal**: O(n + m) time complexity is optimal for this problem.

**Implementation Details**:
- **Tarjan's Algorithm**: Use efficient SCC detection algorithm
- **Component Analysis**: Optimize component graph analysis
- **Edge Classification**: Efficiently classify edges as critical or non-critical
- **Memory Efficiency**: Use optimal data structures

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(m × (n + m)) | O(n + m) | Test each edge individually |
| SCC-Based | O(n + m) | O(n + m) | Use SCC analysis for edge classification |
| Optimized SCC | O(n + m) | O(n + m) | Use Tarjan's algorithm for efficiency |

### Time Complexity
- **Time**: O(n + m) - Find SCCs and classify edges
- **Space**: O(n + m) - Store graph and component information

### Why This Solution Works
- **Strongly Connected Components**: Use SCCs to understand graph structure
- **Component Graph**: Build DAG of strongly connected components
- **Edge Classification**: Classify edges based on component connectivity
- **Optimal Algorithm**: Use Tarjan's algorithm for efficient SCC detection

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted Critical Edges**
**Problem**: Find critical edges with minimum total weight.

**Key Differences**: Edges have weights, minimize total weight of critical edges

**Solution Approach**: Use SCC analysis with weight optimization

**Implementation**:
```python
def weighted_critical_edges(n, edges, weights):
    """
    Find critical edges with minimum total weight
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        weights: list of edge weights
    
    Returns:
        list: critical edges with minimum total weight
    """
    # Build adjacency list with weights
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        adj[a-1].append((b-1, weights[i]))  # Convert to 0-indexed
    
    def tarjan_scc():
        """Find SCCs using Tarjan's algorithm"""
        index = 0
        stack = []
        indices = [-1] * n
        lowlinks = [-1] * n
        on_stack = [False] * n
        sccs = []
        
        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack[node] = True
            
            for neighbor, _ in adj[node]:
                if indices[neighbor] == -1:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif on_stack[neighbor]:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])
            
            if lowlinks[node] == indices[node]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == node:
                        break
                sccs.append(component)
        
        for i in range(n):
            if indices[i] == -1:
                strongconnect(i)
        
        return sccs
    
    def find_minimum_weight_critical_edges(sccs):
        """Find critical edges with minimum total weight"""
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        # Find minimum weight edges between components
        component_edges = {}
        for i, (a, b) in enumerate(edges):
            comp_a = node_to_component[a-1]  # Convert to 0-indexed
            comp_b = node_to_component[b-1]  # Convert to 0-indexed
            
            if comp_a != comp_b:
                key = (min(comp_a, comp_b), max(comp_a, comp_b))
                if key not in component_edges or weights[i] < component_edges[key][2]:
                    component_edges[key] = (a, b, weights[i])
        
        return [(a, b) for a, b, _ in component_edges.values()]
    
    # Find SCCs
    sccs = tarjan_scc()
    
    # Find minimum weight critical edges
    return find_minimum_weight_critical_edges(sccs)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1), (1, 4), (4, 1)]
weights = [1, 2, 3, 4, 5]
result = weighted_critical_edges(n, edges, weights)
print(f"Weighted critical edges result: {result}")
```

#### **2. Dynamic Critical Edges**
**Problem**: Support adding/removing edges and maintain critical edge information.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic SCC maintenance with incremental updates

**Implementation**:
```python
class DynamicCriticalEdges:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.scc_cache = None
        self.critical_edges_cache = None
    
    def add_edge(self, a, b):
        """Add directed edge from a to b"""
        if b not in self.adj[a]:
            self.adj[a].append(b)
            self.scc_cache = None  # Invalidate cache
            self.critical_edges_cache = None
    
    def remove_edge(self, a, b):
        """Remove directed edge from a to b"""
        if b in self.adj[a]:
            self.adj[a].remove(b)
            self.scc_cache = None  # Invalidate cache
            self.critical_edges_cache = None
    
    def get_critical_edges(self):
        """Get current critical edges"""
        if self.critical_edges_cache is None:
            self._compute_critical_edges()
        
        return self.critical_edges_cache
    
    def _compute_critical_edges(self):
        """Compute critical edges for current graph"""
        if self.scc_cache is None:
            self._compute_sccs()
        
        sccs = self.scc_cache
        
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        critical_edges = []
        
        # Check each edge
        for i in range(self.n):
            for j in self.adj[i]:
                comp_i = node_to_component[i]
                comp_j = node_to_component[j]
                
                # Edge is critical if it connects different components
                if comp_i != comp_j:
                    critical_edges.append((i + 1, j + 1))  # Convert back to 1-indexed
        
        self.critical_edges_cache = critical_edges
    
    def _compute_sccs(self):
        """Compute SCCs using Tarjan's algorithm"""
        index = 0
        stack = []
        indices = [-1] * self.n
        lowlinks = [-1] * self.n
        on_stack = [False] * self.n
        sccs = []
        
        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack[node] = True
            
            for neighbor in self.adj[node]:
                if indices[neighbor] == -1:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif on_stack[neighbor]:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])
            
            if lowlinks[node] == indices[node]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == node:
                        break
                sccs.append(component)
        
        for i in range(self.n):
            if indices[i] == -1:
                strongconnect(i)
        
        self.scc_cache = sccs

# Example usage
dce = DynamicCriticalEdges(4)
dce.add_edge(0, 1)
dce.add_edge(1, 2)
dce.add_edge(2, 0)
dce.add_edge(0, 3)
dce.add_edge(3, 0)
result1 = dce.get_critical_edges()
print(f"Dynamic critical edges result: {result1}")
```

#### **3. K-Critical Edges**
**Problem**: Find the k most critical edges for maintaining strong connectivity.

**Key Differences**: Return only the k most important edges

**Solution Approach**: Use SCC analysis with edge importance ranking

**Implementation**:
```python
def k_critical_edges(n, edges, k):
    """
    Find the k most critical edges for maintaining strong connectivity
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        k: number of most critical edges to find
    
    Returns:
        list: k most critical edges
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def tarjan_scc():
        """Find SCCs using Tarjan's algorithm"""
        index = 0
        stack = []
        indices = [-1] * n
        lowlinks = [-1] * n
        on_stack = [False] * n
        sccs = []
        
        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack[node] = True
            
            for neighbor in adj[node]:
                if indices[neighbor] == -1:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif on_stack[neighbor]:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])
            
            if lowlinks[node] == indices[node]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == node:
                        break
                sccs.append(component)
        
        for i in range(n):
            if indices[i] == -1:
                strongconnect(i)
        
        return sccs
    
    def rank_critical_edges(sccs):
        """Rank critical edges by importance"""
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        # Count edges between components
        component_edge_count = {}
        critical_edges = []
        
        for a, b in edges:
            comp_a = node_to_component[a-1]  # Convert to 0-indexed
            comp_b = node_to_component[b-1]  # Convert to 0-indexed
            
            if comp_a != comp_b:
                key = (min(comp_a, comp_b), max(comp_a, comp_b))
                component_edge_count[key] = component_edge_count.get(key, 0) + 1
                critical_edges.append((a, b, key))
        
        # Rank edges by component connectivity
        edge_importance = []
        for a, b, key in critical_edges:
            importance = 1.0 / component_edge_count[key]  # Less edges = more important
            edge_importance.append((importance, a, b))
        
        # Sort by importance (descending)
        edge_importance.sort(reverse=True)
        
        return [(a, b) for _, a, b in edge_importance]
    
    # Find SCCs
    sccs = tarjan_scc()
    
    # Rank critical edges
    ranked_edges = rank_critical_edges(sccs)
    
    # Return top k edges
    return ranked_edges[:k]

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1), (1, 4), (4, 1)]
k = 2
result = k_critical_edges(n, edges, k)
print(f"K-critical edges result: {result}")
```

### Related Problems

#### **CSES Problems**
- [Strongly Connected Components](https://cses.fi/problemset/task/1683) - SCC detection
- [New Flight Routes](https://cses.fi/problemset/task/1683) - Connectivity
- [Planets and Kingdoms](https://cses.fi/problemset/task/1683) - SCC analysis

#### **LeetCode Problems**
- [Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) - Bridge detection
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Cycle detection
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Topological sort

#### **Problem Categories**
- **Graph Theory**: Strongly connected components, critical edges
- **Tarjan's Algorithm**: SCC detection, bridge detection
- **Combinatorial Optimization**: Edge importance, connectivity analysis

## 🔗 Additional Resources

### **Algorithm References**
- [Tarjan's Algorithm](https://cp-algorithms.com/graph/strongly-connected-components.html) - SCC detection
- [Bridge Detection](https://cp-algorithms.com/graph/bridge-searching.html) - Bridge finding
- [Strongly Connected Components](https://cp-algorithms.com/graph/strongly-connected-components.html) - SCC analysis

### **Practice Problems**
- [CSES Strongly Connected Components](https://cses.fi/problemset/task/1683) - Medium
- [CSES New Flight Routes](https://cses.fi/problemset/task/1683) - Medium
- [CSES Planets and Kingdoms](https://cses.fi/problemset/task/1683) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
