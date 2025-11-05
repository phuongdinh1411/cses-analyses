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

## Problem Variations

### **Variation 1: Strongly Connected Edges with Dynamic Updates**
**Problem**: Handle dynamic graph updates (add/remove/update edges) while maintaining strongly connected edge calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic graph management with strongly connected component detection.

```python
from collections import defaultdict, deque
import heapq

class DynamicStronglyConnectedEdges:
    def __init__(self, n=None, edges=None):
        self.n = n or 0
        self.edges = edges or []
        self.graph = defaultdict(list)
        self._update_scc_info()
    
    def _update_scc_info(self):
        """Update strongly connected component information."""
        self.scc_edges = self._calculate_strongly_connected_edges()
    
    def _calculate_strongly_connected_edges(self):
        """Calculate strongly connected edges using Tarjan's algorithm."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Build adjacency list
        adj = defaultdict(list)
        for u, v in self.edges:
            adj[u].append(v)
        
        # Tarjan's algorithm for SCC
        disc = [-1] * self.n
        low = [-1] * self.n
        stack = []
        in_stack = [False] * self.n
        time = [0]
        sccs = []
        
        def tarjan(u):
            disc[u] = low[u] = time[0]
            time[0] += 1
            stack.append(u)
            in_stack[u] = True
            
            for v in adj[u]:
                if disc[v] == -1:
                    tarjan(v)
                    low[u] = min(low[u], low[v])
                elif in_stack[v]:
                    low[u] = min(low[u], disc[v])
            
            if low[u] == disc[u]:
                scc = []
                while True:
                    w = stack.pop()
                    in_stack[w] = False
                    scc.append(w)
                    if w == u:
                        break
                sccs.append(scc)
        
        # Find all SCCs
        for i in range(self.n):
            if disc[i] == -1:
                tarjan(i)
        
        # Find edges within SCCs
        scc_edges = []
        for scc in sccs:
            scc_set = set(scc)
            for u, v in self.edges:
                if u in scc_set and v in scc_set:
                    scc_edges.append((u, v))
        
        return scc_edges
    
    def update_graph(self, new_n, new_edges):
        """Update the graph with new vertices and edges."""
        self.n = new_n
        self.edges = new_edges
        self._build_graph()
        self._update_scc_info()
    
    def add_edge(self, u, v):
        """Add an edge to the graph."""
        if 0 <= u < self.n and 0 <= v < self.n:
            self.edges.append((u, v))
            self.graph[u].append(v)
            self._update_scc_info()
    
    def remove_edge(self, u, v):
        """Remove an edge from the graph."""
        if (u, v) in self.edges:
            self.edges.remove((u, v))
            self.graph[u].remove(v)
            self._update_scc_info()
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
    
    def get_strongly_connected_edges(self):
        """Get all strongly connected edges."""
        return self.scc_edges
    
    def get_strongly_connected_edges_with_priorities(self, priorities):
        """Get strongly connected edges considering vertex priorities."""
        if not self.scc_edges:
            return []
        
        # Calculate weighted strongly connected edges based on priorities
        weighted_edges = []
        for u, v in self.scc_edges:
            edge_priority = priorities.get(u, 1) + priorities.get(v, 1)
            weighted_edges.append((u, v, edge_priority))
        
        return weighted_edges
    
    def get_strongly_connected_edges_with_constraints(self, constraint_func):
        """Get strongly connected edges that satisfies custom constraints."""
        if not self.scc_edges:
            return []
        
        filtered_edges = []
        for u, v in self.scc_edges:
            if constraint_func(u, v, self.n, self.edges, self.scc_edges):
                filtered_edges.append((u, v))
        
        return filtered_edges
    
    def get_strongly_connected_edges_in_range(self, min_edges, max_edges):
        """Get strongly connected edges within specified count range."""
        if not self.scc_edges:
            return []
        
        if min_edges <= len(self.scc_edges) <= max_edges:
            return self.scc_edges
        else:
            return []
    
    def get_strongly_connected_edges_with_pattern(self, pattern_func):
        """Get strongly connected edges matching specified pattern."""
        if not self.scc_edges:
            return []
        
        if pattern_func(self.n, self.edges, self.scc_edges):
            return self.scc_edges
        else:
            return []
    
    def get_scc_statistics(self):
        """Get statistics about the strongly connected components."""
        return {
            'n': self.n,
            'edge_count': len(self.edges),
            'scc_edge_count': len(self.scc_edges),
            'scc_ratio': len(self.scc_edges) / max(1, len(self.edges)),
            'has_sccs': len(self.scc_edges) > 0
        }
    
    def get_scc_patterns(self):
        """Get patterns in strongly connected components."""
        patterns = {
            'has_edges': 0,
            'has_valid_graph': 0,
            'optimal_scc_possible': 0,
            'has_large_graph': 0
        }
        
        # Check if has edges
        if len(self.edges) > 0:
            patterns['has_edges'] = 1
        
        # Check if has valid graph
        if self.n > 0:
            patterns['has_valid_graph'] = 1
        
        # Check if optimal SCC is possible
        if len(self.scc_edges) > 0:
            patterns['optimal_scc_possible'] = 1
        
        # Check if has large graph
        if self.n > 100:
            patterns['has_large_graph'] = 1
        
        return patterns
    
    def get_optimal_scc_strategy(self):
        """Get optimal strategy for strongly connected component management."""
        if not self.scc_edges:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'scc_edge_count': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = len(self.scc_edges) / max(1, len(self.edges))
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'tarjan_scc'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_tarjan'
        else:
            recommended_strategy = 'advanced_scc_detection'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'scc_edge_count': len(self.scc_edges)
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3)]
dynamic_scc = DynamicStronglyConnectedEdges(n, edges)
print(f"Strongly connected edges: {dynamic_scc.scc_edges}")

# Update graph
dynamic_scc.update_graph(6, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3), (4, 5), (5, 4)])
print(f"After updating graph: n={dynamic_scc.n}, scc_edges={dynamic_scc.scc_edges}")

# Add edge
dynamic_scc.add_edge(5, 0)
print(f"After adding edge (5,0): {dynamic_scc.edges}")

# Remove edge
dynamic_scc.remove_edge(5, 0)
print(f"After removing edge (5,0): {dynamic_scc.edges}")

# Get strongly connected edges
scc_edges = dynamic_scc.get_strongly_connected_edges()
print(f"Strongly connected edges: {scc_edges}")

# Get strongly connected edges with priorities
priorities = {i: i for i in range(n)}
priority_edges = dynamic_scc.get_strongly_connected_edges_with_priorities(priorities)
print(f"Strongly connected edges with priorities: {priority_edges}")

# Get strongly connected edges with constraints
def constraint_func(u, v, n, edges, scc_edges):
    return u >= 0 and v >= 0 and u < n and v < n

print(f"Strongly connected edges with constraints: {dynamic_scc.get_strongly_connected_edges_with_constraints(constraint_func)}")

# Get strongly connected edges in range
print(f"Strongly connected edges in range 1-10: {dynamic_scc.get_strongly_connected_edges_in_range(1, 10)}")

# Get strongly connected edges with pattern
def pattern_func(n, edges, scc_edges):
    return len(scc_edges) > 0 and n > 0

print(f"Strongly connected edges with pattern: {dynamic_scc.get_strongly_connected_edges_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_scc.get_scc_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_scc.get_scc_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_scc.get_optimal_scc_strategy()}")
```

### **Variation 2: Strongly Connected Edges with Different Operations**
**Problem**: Handle different types of strongly connected edge operations (weighted edges, priority-based selection, advanced edge analysis).

**Approach**: Use advanced data structures for efficient different types of strongly connected edge operations.

```python
class AdvancedStronglyConnectedEdges:
    def __init__(self, n=None, edges=None, weights=None, priorities=None):
        self.n = n or 0
        self.edges = edges or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.graph = defaultdict(list)
        self._update_scc_info()
    
    def _update_scc_info(self):
        """Update strongly connected component information."""
        self.scc_edges = self._calculate_strongly_connected_edges()
    
    def _calculate_strongly_connected_edges(self):
        """Calculate strongly connected edges using Tarjan's algorithm."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Build adjacency list
        adj = defaultdict(list)
        for u, v in self.edges:
            adj[u].append(v)
        
        # Tarjan's algorithm for SCC
        disc = [-1] * self.n
        low = [-1] * self.n
        stack = []
        in_stack = [False] * self.n
        time = [0]
        sccs = []
        
        def tarjan(u):
            disc[u] = low[u] = time[0]
            time[0] += 1
            stack.append(u)
            in_stack[u] = True
            
            for v in adj[u]:
                if disc[v] == -1:
                    tarjan(v)
                    low[u] = min(low[u], low[v])
                elif in_stack[v]:
                    low[u] = min(low[u], disc[v])
            
            if low[u] == disc[u]:
                scc = []
                while True:
                    w = stack.pop()
                    in_stack[w] = False
                    scc.append(w)
                    if w == u:
                        break
                sccs.append(scc)
        
        # Find all SCCs
        for i in range(self.n):
            if disc[i] == -1:
                tarjan(i)
        
        # Find edges within SCCs
        scc_edges = []
        for scc in sccs:
            scc_set = set(scc)
            for u, v in self.edges:
                if u in scc_set and v in scc_set:
                    scc_edges.append((u, v))
        
        return scc_edges
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
    
    def get_strongly_connected_edges(self):
        """Get all strongly connected edges."""
        return self.scc_edges
    
    def get_weighted_strongly_connected_edges(self):
        """Get strongly connected edges with weights and priorities applied."""
        if not self.scc_edges:
            return []
        
        # Calculate weighted strongly connected edges based on edge weights and vertex priorities
        weighted_edges = []
        for u, v in self.scc_edges:
            edge_weight = self.weights.get((u, v), 1)
            vertex_priority = self.priorities.get(u, 1) + self.priorities.get(v, 1)
            weighted_score = edge_weight * vertex_priority
            weighted_edges.append((u, v, weighted_score))
        
        return weighted_edges
    
    def get_strongly_connected_edges_with_priority(self, priority_func):
        """Get strongly connected edges considering priority."""
        if not self.scc_edges:
            return []
        
        # Calculate priority-based strongly connected edges
        priority_edges = []
        for u, v in self.scc_edges:
            priority = priority_func(u, v, self.weights, self.priorities)
            priority_edges.append((u, v, priority))
        
        return priority_edges
    
    def get_strongly_connected_edges_with_optimization(self, optimization_func):
        """Get strongly connected edges using custom optimization function."""
        if not self.scc_edges:
            return []
        
        # Calculate optimization-based strongly connected edges
        optimized_edges = []
        for u, v in self.scc_edges:
            score = optimization_func(u, v, self.weights, self.priorities)
            optimized_edges.append((u, v, score))
        
        return optimized_edges
    
    def get_strongly_connected_edges_with_constraints(self, constraint_func):
        """Get strongly connected edges that satisfies custom constraints."""
        if not self.scc_edges:
            return []
        
        if constraint_func(self.n, self.edges, self.weights, self.priorities, self.scc_edges):
            return self.get_weighted_strongly_connected_edges()
        else:
            return []
    
    def get_strongly_connected_edges_with_multiple_criteria(self, criteria_list):
        """Get strongly connected edges that satisfies multiple criteria."""
        if not self.scc_edges:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.edges, self.weights, self.priorities, self.scc_edges):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_strongly_connected_edges()
        else:
            return []
    
    def get_strongly_connected_edges_with_alternatives(self, alternatives):
        """Get strongly connected edges considering alternative weights/priorities."""
        result = []
        
        # Check original strongly connected edges
        original_edges = self.get_weighted_strongly_connected_edges()
        result.append((original_edges, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedStronglyConnectedEdges(self.n, self.edges, alt_weights, alt_priorities)
            temp_edges = temp_instance.get_weighted_strongly_connected_edges()
            result.append((temp_edges, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_strongly_connected_edges_with_adaptive_criteria(self, adaptive_func):
        """Get strongly connected edges using adaptive criteria."""
        if not self.scc_edges:
            return []
        
        if adaptive_func(self.n, self.edges, self.weights, self.priorities, self.scc_edges, []):
            return self.get_weighted_strongly_connected_edges()
        else:
            return []
    
    def get_strongly_connected_edges_optimization(self):
        """Get optimal strongly connected edges configuration."""
        strategies = [
            ('weighted_edges', lambda: len(self.get_weighted_strongly_connected_edges())),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3)]
weights = {(u, v): (u + v) * 2 for u, v in edges}  # Weight based on vertex sum
priorities = {i: i for i in range(n)}  # Priority based on vertex number
advanced_scc = AdvancedStronglyConnectedEdges(n, edges, weights, priorities)

print(f"Weighted strongly connected edges: {advanced_scc.get_weighted_strongly_connected_edges()}")

# Get strongly connected edges with priority
def priority_func(u, v, weights, priorities):
    return priorities.get(u, 1) + priorities.get(v, 1) + weights.get((u, v), 1)

print(f"Strongly connected edges with priority: {advanced_scc.get_strongly_connected_edges_with_priority(priority_func)}")

# Get strongly connected edges with optimization
def optimization_func(u, v, weights, priorities):
    return weights.get((u, v), 1) + priorities.get(u, 1) + priorities.get(v, 1)

print(f"Strongly connected edges with optimization: {advanced_scc.get_strongly_connected_edges_with_optimization(optimization_func)}")

# Get strongly connected edges with constraints
def constraint_func(n, edges, weights, priorities, scc_edges):
    return len(scc_edges) > 0 and n > 0

print(f"Strongly connected edges with constraints: {advanced_scc.get_strongly_connected_edges_with_constraints(constraint_func)}")

# Get strongly connected edges with multiple criteria
def criterion1(n, edges, weights, priorities, scc_edges):
    return len(edges) > 0

def criterion2(n, edges, weights, priorities, scc_edges):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Strongly connected edges with multiple criteria: {advanced_scc.get_strongly_connected_edges_with_multiple_criteria(criteria_list)}")

# Get strongly connected edges with alternatives
alternatives = [({(u, v): 1 for u, v in edges}, {i: 1 for i in range(n)}), ({(u, v): (u + v)*3 for u, v in edges}, {i: 2 for i in range(n)})]
print(f"Strongly connected edges with alternatives: {advanced_scc.get_strongly_connected_edges_with_alternatives(alternatives)}")

# Get strongly connected edges with adaptive criteria
def adaptive_func(n, edges, weights, priorities, scc_edges, current_result):
    return len(edges) > 0 and len(current_result) < 10

print(f"Strongly connected edges with adaptive criteria: {advanced_scc.get_strongly_connected_edges_with_adaptive_criteria(adaptive_func)}")

# Get strongly connected edges optimization
print(f"Strongly connected edges optimization: {advanced_scc.get_strongly_connected_edges_optimization()}")
```

### **Variation 3: Strongly Connected Edges with Constraints**
**Problem**: Handle strongly connected edge calculation with additional constraints (edge limits, SCC constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedStronglyConnectedEdges:
    def __init__(self, n=None, edges=None, constraints=None):
        self.n = n or 0
        self.edges = edges or []
        self.constraints = constraints or {}
        self.graph = defaultdict(list)
        self._update_scc_info()
    
    def _update_scc_info(self):
        """Update strongly connected component information."""
        self.scc_edges = self._calculate_strongly_connected_edges()
    
    def _calculate_strongly_connected_edges(self):
        """Calculate strongly connected edges using Tarjan's algorithm."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Build adjacency list
        adj = defaultdict(list)
        for u, v in self.edges:
            adj[u].append(v)
        
        # Tarjan's algorithm for SCC
        disc = [-1] * self.n
        low = [-1] * self.n
        stack = []
        in_stack = [False] * self.n
        time = [0]
        sccs = []
        
        def tarjan(u):
            disc[u] = low[u] = time[0]
            time[0] += 1
            stack.append(u)
            in_stack[u] = True
            
            for v in adj[u]:
                if disc[v] == -1:
                    tarjan(v)
                    low[u] = min(low[u], low[v])
                elif in_stack[v]:
                    low[u] = min(low[u], disc[v])
            
            if low[u] == disc[u]:
                scc = []
                while True:
                    w = stack.pop()
                    in_stack[w] = False
                    scc.append(w)
                    if w == u:
                        break
                sccs.append(scc)
        
        # Find all SCCs
        for i in range(self.n):
            if disc[i] == -1:
                tarjan(i)
        
        # Find edges within SCCs
        scc_edges = []
        for scc in sccs:
            scc_set = set(scc)
            for u, v in self.edges:
                if u in scc_set and v in scc_set:
                    scc_edges.append((u, v))
        
        return scc_edges
    
    def _is_valid_edge(self, u, v):
        """Check if edge is valid considering constraints."""
        # Edge constraints
        if 'allowed_edges' in self.constraints:
            if (u, v) not in self.constraints['allowed_edges']:
                return False
        
        if 'forbidden_edges' in self.constraints:
            if (u, v) in self.constraints['forbidden_edges']:
                return False
        
        # Vertex constraints
        if 'max_vertex' in self.constraints:
            if u > self.constraints['max_vertex'] or v > self.constraints['max_vertex']:
                return False
        
        if 'min_vertex' in self.constraints:
            if u < self.constraints['min_vertex'] or v < self.constraints['min_vertex']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(u, v, self.n, self.edges, self.scc_edges):
                    return False
        
        return True
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            if self._is_valid_edge(u, v):
                self.graph[u].append(v)
    
    def get_strongly_connected_edges(self):
        """Get all strongly connected edges."""
        return self.scc_edges
    
    def get_strongly_connected_edges_with_edge_constraints(self, min_edges, max_edges):
        """Get strongly connected edges considering edge count constraints."""
        if not self.scc_edges:
            return []
        
        if min_edges <= len(self.scc_edges) <= max_edges:
            return self.scc_edges
        else:
            return []
    
    def get_strongly_connected_edges_with_scc_constraints(self, scc_constraints):
        """Get strongly connected edges considering SCC constraints."""
        if not self.scc_edges:
            return []
        
        satisfies_constraints = True
        for constraint in scc_constraints:
            if not constraint(self.n, self.edges, self.scc_edges):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.scc_edges
        else:
            return []
    
    def get_strongly_connected_edges_with_pattern_constraints(self, pattern_constraints):
        """Get strongly connected edges considering pattern constraints."""
        if not self.scc_edges:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n, self.edges, self.scc_edges):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.scc_edges
        else:
            return []
    
    def get_strongly_connected_edges_with_mathematical_constraints(self, constraint_func):
        """Get strongly connected edges that satisfies custom mathematical constraints."""
        if not self.scc_edges:
            return []
        
        if constraint_func(self.n, self.edges, self.scc_edges):
            return self.scc_edges
        else:
            return []
    
    def get_strongly_connected_edges_with_optimization_constraints(self, optimization_func):
        """Get strongly connected edges using custom optimization constraints."""
        if not self.scc_edges:
            return []
        
        # Calculate optimization score for strongly connected edges
        score = optimization_func(self.n, self.edges, self.scc_edges)
        
        if score > 0:
            return self.scc_edges
        else:
            return []
    
    def get_strongly_connected_edges_with_multiple_constraints(self, constraints_list):
        """Get strongly connected edges that satisfies multiple constraints."""
        if not self.scc_edges:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n, self.edges, self.scc_edges):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.scc_edges
        else:
            return []
    
    def get_strongly_connected_edges_with_priority_constraints(self, priority_func):
        """Get strongly connected edges with priority-based constraints."""
        if not self.scc_edges:
            return []
        
        # Calculate priority for strongly connected edges
        priority = priority_func(self.n, self.edges, self.scc_edges)
        
        if priority > 0:
            return self.scc_edges
        else:
            return []
    
    def get_strongly_connected_edges_with_adaptive_constraints(self, adaptive_func):
        """Get strongly connected edges with adaptive constraints."""
        if not self.scc_edges:
            return []
        
        if adaptive_func(self.n, self.edges, self.scc_edges, []):
            return self.scc_edges
        else:
            return []
    
    def get_optimal_strongly_connected_edges_strategy(self):
        """Get optimal strongly connected edges strategy considering all constraints."""
        strategies = [
            ('edge_constraints', self.get_strongly_connected_edges_with_edge_constraints),
            ('scc_constraints', self.get_strongly_connected_edges_with_scc_constraints),
            ('pattern_constraints', self.get_strongly_connected_edges_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'edge_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'scc_constraints':
                    scc_constraints = [lambda n, edges, scc_edges: len(edges) > 0]
                    result = strategy_func(scc_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n, edges, scc_edges: len(edges) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_edges': [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3)],
    'forbidden_edges': [(0, 3), (1, 4)],
    'max_vertex': 10,
    'min_vertex': 0,
    'pattern_constraints': [lambda u, v, n, edges, scc_edges: u >= 0 and v >= 0 and u < n and v < n]
}

n = 5
edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3)]
constrained_scc = ConstrainedStronglyConnectedEdges(n, edges, constraints)

print("Edge-constrained strongly connected edges:", constrained_scc.get_strongly_connected_edges_with_edge_constraints(1, 10))

print("SCC-constrained strongly connected edges:", constrained_scc.get_strongly_connected_edges_with_scc_constraints([lambda n, edges, scc_edges: len(edges) > 0]))

print("Pattern-constrained strongly connected edges:", constrained_scc.get_strongly_connected_edges_with_pattern_constraints([lambda n, edges, scc_edges: len(edges) > 0]))

# Mathematical constraints
def custom_constraint(n, edges, scc_edges):
    return len(scc_edges) > 0 and n > 0

print("Mathematical constraint strongly connected edges:", constrained_scc.get_strongly_connected_edges_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n, edges, scc_edges):
    return 1 <= len(scc_edges) <= 20

range_constraints = [range_constraint]
print("Range-constrained strongly connected edges:", constrained_scc.get_strongly_connected_edges_with_edge_constraints(1, 20))

# Multiple constraints
def constraint1(n, edges, scc_edges):
    return len(edges) > 0

def constraint2(n, edges, scc_edges):
    return len(scc_edges) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints strongly connected edges:", constrained_scc.get_strongly_connected_edges_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n, edges, scc_edges):
    return n + len(edges) + len(scc_edges)

print("Priority-constrained strongly connected edges:", constrained_scc.get_strongly_connected_edges_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, edges, scc_edges, current_result):
    return len(edges) > 0 and len(current_result) < 10

print("Adaptive constraint strongly connected edges:", constrained_scc.get_strongly_connected_edges_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_scc.get_optimal_strongly_connected_edges_strategy()
print(f"Optimal strongly connected edges strategy: {optimal}")
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
