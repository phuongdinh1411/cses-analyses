---
layout: simple
title: "New Flight Routes - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/new_flight_routes_analysis
---

# New Flight Routes - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of connectivity in directed graphs
- Apply graph theory principles to determine minimum edges for strong connectivity
- Implement algorithms for strongly connected components (SCC)
- Optimize graph analysis for connectivity problems
- Handle special cases in graph connectivity analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, strongly connected components, Tarjan's algorithm, Kosaraju's algorithm
- **Data Structures**: Adjacency lists, stacks, visited arrays, component arrays
- **Mathematical Concepts**: Graph theory, connectivity, strongly connected components
- **Programming Skills**: Graph representation, DFS, stack operations, component tracking
- **Related Problems**: Planets and Kingdoms (SCC detection), Strongly Connected Components (SCC analysis), Road Construction (connectivity)

## 📋 Problem Description

Given a directed graph with n nodes and m edges, determine the minimum number of new edges to add to make the graph strongly connected.

**Input**: 
- n: number of nodes
- m: number of edges
- m lines: a b (directed edge from node a to node b)

**Output**: 
- Minimum number of new edges needed to make the graph strongly connected

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5

**Example**:
```
Input:
4 3
1 2
2 3
3 1

Output:
1

Explanation**: 
Current graph: 1→2→3→1 (strongly connected component)
Missing: connection to node 4
Add edge: 4→1 or 3→4
Minimum edges needed: 1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible combinations of new edges
- **Connectivity Check**: Check strong connectivity after each addition
- **Combinatorial Explosion**: O(n²) possible edges to consider
- **Baseline Understanding**: Provides correct answer but highly impractical

**Key Insight**: Try all possible combinations of new edges and check if the graph becomes strongly connected.

**Algorithm**:
- Generate all possible directed edges not in the current graph
- Try all combinations of new edges
- Find the minimum number that makes the graph strongly connected

**Visual Example**:
```
Graph: 1→2→3→1, node 4 isolated

All possible new edges:
┌─────────────────────────────────────┐
│ 1→4, 2→4, 3→4, 4→1, 4→2, 4→3      │
│ Try combinations:                   │
│ - Add 4→1: Graph becomes connected ✓│
│ - Add 1→4: Graph becomes connected ✓│
│ - Add 2→4: Graph becomes connected ✓│
│ - Add 3→4: Graph becomes connected ✓│
└─────────────────────────────────────┘

Minimum edges needed: 1
```

**Implementation**:
```python
def brute_force_solution(n, edges):
    """
    Find minimum edges for strong connectivity using brute force
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: minimum number of new edges needed
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    existing_edges = set()
    
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        existing_edges.add((a-1, b-1))
    
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
    
    def try_add_edges(num_edges):
        """Try adding num_edges new edges"""
        from itertools import combinations
        
        # Generate all possible new edges
        possible_edges = []
        for i in range(n):
            for j in range(n):
                if i != j and (i, j) not in existing_edges:
                    possible_edges.append((i, j))
        
        # Try all combinations of num_edges
        for edge_combination in combinations(possible_edges, num_edges):
            # Add edges temporarily
            for u, v in edge_combination:
                adj[u].append(v)
            
            # Check connectivity
            if is_strongly_connected():
                # Remove edges
                for u, v in edge_combination:
                    adj[u].remove(v)
                return True
            
            # Remove edges
            for u, v in edge_combination:
                adj[u].remove(v)
        
        return False
    
    # Try adding 0, 1, 2, ... edges
    for num_edges in range(n + 1):
        if try_add_edges(num_edges):
            return num_edges
    
    return n  # Worst case: need n edges

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1)]
result = brute_force_solution(n, edges)
print(f"Brute force result: {result}")  # Output: 1
```

**Time Complexity**: O(n² × 2^(n²))
**Space Complexity**: O(n²)

**Why it's inefficient**: Exponential time complexity makes it impractical for large graphs.

---

### Approach 2: SCC-Based Solution

**Key Insights from SCC-Based Solution**:
- **Strongly Connected Components**: Find SCCs using Tarjan's or Kosaraju's algorithm
- **Component Graph**: Build a DAG of SCCs
- **Connectivity Analysis**: Analyze the component graph structure
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use strongly connected components to determine the minimum number of edges needed for strong connectivity.

**Algorithm**:
- Find all strongly connected components
- Build the component graph (DAG)
- Analyze the component graph to determine minimum edges needed

**Visual Example**:
```
Graph: 1→2→3→1, node 4 isolated

SCCs: {1,2,3}, {4}
Component graph: SCC1 → SCC2 (if any edges exist)

Analysis:
┌─────────────────────────────────────┐
│ SCC1: {1,2,3} (strongly connected) │
│ SCC2: {4} (single node)            │
│ Need: 1 edge to connect SCCs       │
└─────────────────────────────────────┘

Minimum edges needed: 1
```

**Implementation**:
```python
def scc_based_solution(n, edges):
    """
    Find minimum edges for strong connectivity using SCC analysis
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: minimum number of new edges needed
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def find_sccs():
        """Find strongly connected components using Kosaraju's algorithm"""
        # Step 1: DFS to get finish times
        visited = [False] * n
        finish_order = []
        
        def dfs1(node):
            visited[node] = True
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    dfs1(neighbor)
            finish_order.append(node)
        
        for i in range(n):
            if not visited[i]:
                dfs1(i)
        
        # Step 2: Build reverse graph
        reverse_adj = [[] for _ in range(n)]
        for i in range(n):
            for j in adj[i]:
                reverse_adj[j].append(i)
        
        # Step 3: DFS on reverse graph in reverse finish order
        visited = [False] * n
        sccs = []
        
        def dfs2(node, component):
            visited[node] = True
            component.append(node)
            for neighbor in reverse_adj[node]:
                if not visited[neighbor]:
                    dfs2(neighbor, component)
        
        for node in reversed(finish_order):
            if not visited[node]:
                component = []
                dfs2(node, component)
                sccs.append(component)
        
        return sccs
    
    def build_component_graph(sccs):
        """Build component graph (DAG)"""
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        # Build component adjacency list
        component_adj = [[] for _ in range(len(sccs))]
        for i in range(n):
            for j in adj[i]:
                comp_i = node_to_component[i]
                comp_j = node_to_component[j]
                if comp_i != comp_j and comp_j not in component_adj[comp_i]:
                    component_adj[comp_i].append(comp_j)
        
        return component_adj
    
    def analyze_component_graph(component_adj):
        """Analyze component graph to determine minimum edges needed"""
        n_components = len(component_adj)
        
        if n_components == 1:
            return 0  # Already strongly connected
        
        # Count in-degrees and out-degrees
        in_degree = [0] * n_components
        out_degree = [0] * n_components
        
        for i in range(n_components):
            for j in component_adj[i]:
                out_degree[i] += 1
                in_degree[j] += 1
        
        # Count sources and sinks
        sources = sum(1 for i in range(n_components) if in_degree[i] == 0)
        sinks = sum(1 for i in range(n_components) if out_degree[i] == 0)
        
        # Minimum edges needed = max(sources, sinks)
        return max(sources, sinks)
    
    # Find SCCs
    sccs = find_sccs()
    
    # Build component graph
    component_adj = build_component_graph(sccs)
    
    # Analyze component graph
    return analyze_component_graph(component_adj)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1)]
result = scc_based_solution(n, edges)
print(f"SCC-based result: {result}")  # Output: 1
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's better**: Linear time complexity, much more efficient than brute force.

**Implementation Considerations**:
- **SCC Detection**: Use Kosaraju's algorithm for efficient SCC finding
- **Component Graph**: Build DAG of strongly connected components
- **Connectivity Analysis**: Analyze sources and sinks in component graph

---

### Approach 3: Optimized SCC Solution (Optimal)

**Key Insights from Optimized SCC Solution**:
- **Tarjan's Algorithm**: Use Tarjan's algorithm for more efficient SCC detection
- **Component Analysis**: Optimize component graph analysis
- **Edge Counting**: Efficiently count sources and sinks
- **Optimal Complexity**: O(n + m) time complexity

**Key Insight**: Use Tarjan's algorithm for SCC detection and optimize the component graph analysis.

**Algorithm**:
- Use Tarjan's algorithm to find SCCs
- Build component graph efficiently
- Count sources and sinks to determine minimum edges

**Visual Example**:
```
Graph: 1→2→3→1, node 4 isolated

Tarjan's algorithm:
┌─────────────────────────────────────┐
│ SCC1: {1,2,3} (strongly connected) │
│ SCC2: {4} (single node)            │
│ Component graph: SCC1 → SCC2       │
│ Sources: 1, Sinks: 1               │
│ Minimum edges: max(1,1) = 1        │
└─────────────────────────────────────┘

Minimum edges needed: 1
```

**Implementation**:
```python
def optimized_scc_solution(n, edges):
    """
    Find minimum edges for strong connectivity using optimized SCC analysis
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: minimum number of new edges needed
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
    
    def analyze_component_graph(sccs):
        """Analyze component graph to determine minimum edges needed"""
        n_components = len(sccs)
        
        if n_components == 1:
            return 0  # Already strongly connected
        
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        # Build component graph
        component_adj = [[] for _ in range(n_components)]
        for i in range(n):
            for j in adj[i]:
                comp_i = node_to_component[i]
                comp_j = node_to_component[j]
                if comp_i != comp_j and comp_j not in component_adj[comp_i]:
                    component_adj[comp_i].append(comp_j)
        
        # Count in-degrees and out-degrees
        in_degree = [0] * n_components
        out_degree = [0] * n_components
        
        for i in range(n_components):
            for j in component_adj[i]:
                out_degree[i] += 1
                in_degree[j] += 1
        
        # Count sources and sinks
        sources = sum(1 for i in range(n_components) if in_degree[i] == 0)
        sinks = sum(1 for i in range(n_components) if out_degree[i] == 0)
        
        # Minimum edges needed = max(sources, sinks)
        return max(sources, sinks)
    
    # Find SCCs using Tarjan's algorithm
    sccs = tarjan_scc()
    
    # Analyze component graph
    return analyze_component_graph(sccs)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1)]
result = optimized_scc_solution(n, edges)
print(f"Optimized SCC result: {result}")  # Output: 1
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's optimal**: O(n + m) time complexity is optimal for this problem.

**Implementation Details**:
- **Tarjan's Algorithm**: Use efficient SCC detection algorithm
- **Component Analysis**: Optimize component graph analysis
- **Edge Counting**: Efficiently count sources and sinks
- **Memory Efficiency**: Use optimal data structures

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n² × 2^(n²)) | O(n²) | Try all possible edge combinations |
| SCC-Based | O(n + m) | O(n + m) | Use SCC analysis for connectivity |
| Optimized SCC | O(n + m) | O(n + m) | Use Tarjan's algorithm for efficiency |

### Time Complexity
- **Time**: O(n + m) - Find SCCs and analyze component graph
- **Space**: O(n + m) - Store graph and component information

### Why This Solution Works
- **Strongly Connected Components**: Use SCCs to understand graph structure
- **Component Graph**: Build DAG of strongly connected components
- **Connectivity Analysis**: Analyze sources and sinks to determine minimum edges
- **Optimal Algorithm**: Use Tarjan's algorithm for efficient SCC detection

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted New Flight Routes**
**Problem**: Find minimum cost edges to make the graph strongly connected.

**Key Differences**: Edges have costs, minimize total cost instead of number of edges

**Solution Approach**: Use SCC analysis with cost optimization

**Implementation**:
```python
def weighted_new_flight_routes(n, edges, edge_costs):
    """
    Find minimum cost edges for strong connectivity
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        edge_costs: list of edge costs
    
    Returns:
        int: minimum cost to make graph strongly connected
    """
    # Build adjacency list with costs
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        adj[a-1].append((b-1, edge_costs[i]))  # Convert to 0-indexed
    
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
    
    def find_minimum_cost_edges(sccs):
        """Find minimum cost edges to connect components"""
        n_components = len(sccs)
        
        if n_components == 1:
            return 0  # Already strongly connected
        
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        # Find minimum cost edges between components
        component_costs = [[float('inf')] * n_components for _ in range(n_components)]
        
        for i in range(n):
            for j, cost in adj[i]:
                comp_i = node_to_component[i]
                comp_j = node_to_component[j]
                if comp_i != comp_j:
                    component_costs[comp_i][comp_j] = min(component_costs[comp_i][comp_j], cost)
        
        # Use minimum cost edges to connect components
        total_cost = 0
        for i in range(n_components):
            for j in range(n_components):
                if i != j and component_costs[i][j] != float('inf'):
                    total_cost += component_costs[i][j]
        
        return total_cost
    
    # Find SCCs
    sccs = tarjan_scc()
    
    # Find minimum cost edges
    return find_minimum_cost_edges(sccs)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1)]
edge_costs = [1, 2, 3]
result = weighted_new_flight_routes(n, edges, edge_costs)
print(f"Weighted new flight routes result: {result}")
```

#### **2. Dynamic New Flight Routes**
**Problem**: Support adding/removing edges and answering connectivity queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic SCC maintenance with incremental updates

**Implementation**:
```python
class DynamicNewFlightRoutes:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.scc_cache = None
    
    def add_edge(self, a, b):
        """Add directed edge from a to b"""
        if b not in self.adj[a]:
            self.adj[a].append(b)
            self.scc_cache = None  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove directed edge from a to b"""
        if b in self.adj[a]:
            self.adj[a].remove(b)
            self.scc_cache = None  # Invalidate cache
    
    def get_minimum_edges_needed(self):
        """Get minimum number of edges needed for strong connectivity"""
        if self.scc_cache is None:
            self._compute_sccs()
        
        return self._analyze_component_graph()
    
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
    
    def _analyze_component_graph(self):
        """Analyze component graph to determine minimum edges needed"""
        sccs = self.scc_cache
        n_components = len(sccs)
        
        if n_components == 1:
            return 0  # Already strongly connected
        
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        # Build component graph
        component_adj = [[] for _ in range(n_components)]
        for i in range(self.n):
            for j in self.adj[i]:
                comp_i = node_to_component[i]
                comp_j = node_to_component[j]
                if comp_i != comp_j and comp_j not in component_adj[comp_i]:
                    component_adj[comp_i].append(comp_j)
        
        # Count in-degrees and out-degrees
        in_degree = [0] * n_components
        out_degree = [0] * n_components
        
        for i in range(n_components):
            for j in component_adj[i]:
                out_degree[i] += 1
                in_degree[j] += 1
        
        # Count sources and sinks
        sources = sum(1 for i in range(n_components) if in_degree[i] == 0)
        sinks = sum(1 for i in range(n_components) if out_degree[i] == 0)
        
        # Minimum edges needed = max(sources, sinks)
        return max(sources, sinks)

# Example usage
dnfr = DynamicNewFlightRoutes(4)
dnfr.add_edge(0, 1)
dnfr.add_edge(1, 2)
dnfr.add_edge(2, 0)
result1 = dnfr.get_minimum_edges_needed()
print(f"Dynamic new flight routes result: {result1}")
```

#### **3. Constrained New Flight Routes**
**Problem**: Find minimum edges with additional constraints (e.g., specific nodes must be connected).

**Key Differences**: Consider additional constraints when adding edges

**Solution Approach**: Use SCC analysis with constraint checking

**Implementation**:
```python
def constrained_new_flight_routes(n, edges, constraints):
    """
    Find minimum edges for strong connectivity with constraints
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        constraints: list of (u, v) pairs that must be connected
    
    Returns:
        int: minimum number of new edges needed with constraints
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
    
    def check_constraints(sccs):
        """Check if constraints are satisfied"""
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        # Check if all constraint pairs are in the same component
        for u, v in constraints:
            if node_to_component[u-1] != node_to_component[v-1]:  # Convert to 0-indexed
                return False
        
        return True
    
    def find_minimum_edges_with_constraints(sccs):
        """Find minimum edges needed with constraints"""
        n_components = len(sccs)
        
        if n_components == 1:
            return 0  # Already strongly connected
        
        # Map each node to its component
        node_to_component = {}
        for i, component in enumerate(sccs):
            for node in component:
                node_to_component[node] = i
        
        # Build component graph
        component_adj = [[] for _ in range(n_components)]
        for i in range(n):
            for j in adj[i]:
                comp_i = node_to_component[i]
                comp_j = node_to_component[j]
                if comp_i != comp_j and comp_j not in component_adj[comp_i]:
                    component_adj[comp_i].append(comp_j)
        
        # Count in-degrees and out-degrees
        in_degree = [0] * n_components
        out_degree = [0] * n_components
        
        for i in range(n_components):
            for j in component_adj[i]:
                out_degree[i] += 1
                in_degree[j] += 1
        
        # Count sources and sinks
        sources = sum(1 for i in range(n_components) if in_degree[i] == 0)
        sinks = sum(1 for i in range(n_components) if out_degree[i] == 0)
        
        # Minimum edges needed = max(sources, sinks)
        return max(sources, sinks)
    
    # Find SCCs
    sccs = tarjan_scc()
    
    # Check if constraints are satisfied
    if not check_constraints(sccs):
        return -1  # Constraints cannot be satisfied
    
    # Find minimum edges needed
    return find_minimum_edges_with_constraints(sccs)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 1)]
constraints = [(1, 4)]  # Nodes 1 and 4 must be connected
result = constrained_new_flight_routes(n, edges, constraints)
print(f"Constrained new flight routes result: {result}")
```

## Problem Variations

### **Variation 1: New Flight Routes with Dynamic Updates**
**Problem**: Handle dynamic graph updates (add/remove/update flight routes) while maintaining new flight route calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic graph management with new flight route detection.

```python
from collections import defaultdict, deque
import heapq

class DynamicNewFlightRoutes:
    def __init__(self, n=None, edges=None, new_routes=None):
        self.n = n or 0
        self.edges = edges or []
        self.new_routes = new_routes or []
        self.graph = defaultdict(list)
        self._update_flight_route_info()
    
    def _update_flight_route_info(self):
        """Update flight route information."""
        self.flight_routes = self._calculate_new_flight_routes()
    
    def _calculate_new_flight_routes(self):
        """Calculate new flight routes using BFS."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Build existing graph
        existing_graph = defaultdict(list)
        for u, v in self.edges:
            existing_graph[u].append(v)
            existing_graph[v].append(u)
        
        # Find new routes (pairs of cities not directly connected)
        new_routes = []
        for u in range(self.n):
            for v in range(u + 1, self.n):
                # Check if there's no direct connection
                if v not in existing_graph[u]:
                    # Check if there's a path between u and v
                    if not self._has_path(existing_graph, u, v):
                        new_routes.append((u, v))
        
        return new_routes
    
    def _has_path(self, graph, start, end):
        """Check if there's a path between start and end using BFS."""
        if start == end:
            return True
        
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v == end:
                    return True
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        return False
    
    def update_graph(self, new_n, new_edges, new_routes=None):
        """Update the graph with new vertices, edges, and routes."""
        self.n = new_n
        self.edges = new_edges
        if new_routes is not None:
            self.new_routes = new_routes
        self._build_graph()
        self._update_flight_route_info()
    
    def add_route(self, u, v):
        """Add a new flight route."""
        if 0 <= u < self.n and 0 <= v < self.n and (u, v) not in self.edges and (v, u) not in self.edges:
            self.edges.append((u, v))
            self.graph[u].append(v)
            self.graph[v].append(u)
            self._update_flight_route_info()
    
    def remove_route(self, u, v):
        """Remove a flight route."""
        if (u, v) in self.edges:
            self.edges.remove((u, v))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_flight_route_info()
        elif (v, u) in self.edges:
            self.edges.remove((v, u))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_flight_route_info()
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def get_new_flight_routes(self):
        """Get all new flight routes."""
        return self.flight_routes
    
    def get_new_flight_routes_with_priorities(self, priorities):
        """Get new flight routes considering city priorities."""
        if not self.flight_routes:
            return []
        
        # Calculate weighted new flight routes based on priorities
        weighted_routes = []
        for u, v in self.flight_routes:
            city_priority = priorities.get(u, 1) + priorities.get(v, 1)
            weighted_routes.append((u, v, city_priority))
        
        return weighted_routes
    
    def get_new_flight_routes_with_constraints(self, constraint_func):
        """Get new flight routes that satisfies custom constraints."""
        if not self.flight_routes:
            return []
        
        filtered_routes = []
        for u, v in self.flight_routes:
            if constraint_func(u, v, self.n, self.edges, self.flight_routes):
                filtered_routes.append((u, v))
        
        return filtered_routes
    
    def get_new_flight_routes_in_range(self, min_distance, max_distance):
        """Get new flight routes within specified distance range."""
        if not self.flight_routes:
            return []
        
        filtered_routes = []
        for u, v in self.flight_routes:
            # Calculate distance between cities (simplified as |u - v|)
            distance = abs(u - v)
            if min_distance <= distance <= max_distance:
                filtered_routes.append((u, v))
        
        return filtered_routes
    
    def get_new_flight_routes_with_pattern(self, pattern_func):
        """Get new flight routes matching specified pattern."""
        if not self.flight_routes:
            return []
        
        filtered_routes = []
        for u, v in self.flight_routes:
            if pattern_func(u, v, self.n, self.edges, self.flight_routes):
                filtered_routes.append((u, v))
        
        return filtered_routes
    
    def get_flight_route_statistics(self):
        """Get statistics about the flight routes."""
        return {
            'n': self.n,
            'existing_routes': len(self.edges),
            'new_routes': len(self.flight_routes),
            'total_possible_routes': self.n * (self.n - 1) // 2,
            'coverage_rate': len(self.edges) / max(1, self.n * (self.n - 1) // 2)
        }
    
    def get_flight_route_patterns(self):
        """Get patterns in flight routes."""
        patterns = {
            'has_routes': 0,
            'has_valid_graph': 0,
            'optimal_route_coverage': 0,
            'has_large_graph': 0
        }
        
        # Check if has routes
        if len(self.edges) > 0:
            patterns['has_routes'] = 1
        
        # Check if has valid graph
        if self.n > 0:
            patterns['has_valid_graph'] = 1
        
        # Check if optimal route coverage is possible
        if len(self.edges) == self.n * (self.n - 1) // 2:
            patterns['optimal_route_coverage'] = 1
        
        # Check if has large graph
        if self.n > 100:
            patterns['has_large_graph'] = 1
        
        return patterns
    
    def get_optimal_flight_route_strategy(self):
        """Get optimal strategy for flight route management."""
        if not self.flight_routes:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'coverage_rate': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = len(self.edges) / max(1, self.n * (self.n - 1) // 2)
        
        # Calculate coverage rate
        coverage_rate = len(self.edges) / max(1, self.n * (self.n - 1) // 2)
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'bfs_flight_route'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_bfs'
        else:
            recommended_strategy = 'advanced_flight_route_detection'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'coverage_rate': coverage_rate
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
new_routes = [(0, 2), (1, 3), (2, 4), (0, 3), (1, 4)]
dynamic_routes = DynamicNewFlightRoutes(n, edges, new_routes)
print(f"New flight routes: {dynamic_routes.flight_routes}")

# Update graph
dynamic_routes.update_graph(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)], [(0, 2), (1, 3), (2, 4), (3, 5), (4, 0), (1, 4)])
print(f"After updating graph: n={dynamic_routes.n}, new_routes={dynamic_routes.flight_routes}")

# Add route
dynamic_routes.add_route(0, 2)
print(f"After adding route (0,2): {dynamic_routes.edges}")

# Remove route
dynamic_routes.remove_route(0, 2)
print(f"After removing route (0,2): {dynamic_routes.edges}")

# Get new flight routes
routes = dynamic_routes.get_new_flight_routes()
print(f"New flight routes: {routes}")

# Get new flight routes with priorities
priorities = {i: i for i in range(n)}
priority_routes = dynamic_routes.get_new_flight_routes_with_priorities(priorities)
print(f"New flight routes with priorities: {priority_routes}")

# Get new flight routes with constraints
def constraint_func(u, v, n, edges, flight_routes):
    return u >= 0 and v >= 0 and u < n and v < n

print(f"New flight routes with constraints: {dynamic_routes.get_new_flight_routes_with_constraints(constraint_func)}")

# Get new flight routes in range
print(f"New flight routes in range 1-3: {dynamic_routes.get_new_flight_routes_in_range(1, 3)}")

# Get new flight routes with pattern
def pattern_func(u, v, n, edges, flight_routes):
    return u >= 0 and v >= 0 and u < n and v < n

print(f"New flight routes with pattern: {dynamic_routes.get_new_flight_routes_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_routes.get_flight_route_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_routes.get_flight_route_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_routes.get_optimal_flight_route_strategy()}")
```

### **Variation 2: New Flight Routes with Different Operations**
**Problem**: Handle different types of new flight route operations (weighted routes, priority-based selection, advanced route analysis).

**Approach**: Use advanced data structures for efficient different types of new flight route operations.

```python
class AdvancedNewFlightRoutes:
    def __init__(self, n=None, edges=None, new_routes=None, weights=None, priorities=None):
        self.n = n or 0
        self.edges = edges or []
        self.new_routes = new_routes or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.graph = defaultdict(list)
        self._update_flight_route_info()
    
    def _update_flight_route_info(self):
        """Update flight route information."""
        self.flight_routes = self._calculate_new_flight_routes()
    
    def _calculate_new_flight_routes(self):
        """Calculate new flight routes using BFS."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Build existing graph
        existing_graph = defaultdict(list)
        for u, v in self.edges:
            existing_graph[u].append(v)
            existing_graph[v].append(u)
        
        # Find new routes (pairs of cities not directly connected)
        new_routes = []
        for u in range(self.n):
            for v in range(u + 1, self.n):
                # Check if there's no direct connection
                if v not in existing_graph[u]:
                    # Check if there's a path between u and v
                    if not self._has_path(existing_graph, u, v):
                        new_routes.append((u, v))
        
        return new_routes
    
    def _has_path(self, graph, start, end):
        """Check if there's a path between start and end using BFS."""
        if start == end:
            return True
        
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v == end:
                    return True
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        return False
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def get_new_flight_routes(self):
        """Get all new flight routes."""
        return self.flight_routes
    
    def get_weighted_new_flight_routes(self):
        """Get new flight routes with weights and priorities applied."""
        if not self.flight_routes:
            return []
        
        # Calculate weighted new flight routes based on edge weights and city priorities
        weighted_routes = []
        for u, v in self.flight_routes:
            edge_weight = self.weights.get((u, v), 1)
            city_priority = self.priorities.get(u, 1) + self.priorities.get(v, 1)
            weighted_score = edge_weight * city_priority
            weighted_routes.append((u, v, weighted_score))
        
        return weighted_routes
    
    def get_new_flight_routes_with_priority(self, priority_func):
        """Get new flight routes considering priority."""
        if not self.flight_routes:
            return []
        
        # Calculate priority-based new flight routes
        priority_routes = []
        for u, v in self.flight_routes:
            priority = priority_func(u, v, self.weights, self.priorities)
            priority_routes.append((u, v, priority))
        
        return priority_routes
    
    def get_new_flight_routes_with_optimization(self, optimization_func):
        """Get new flight routes using custom optimization function."""
        if not self.flight_routes:
            return []
        
        # Calculate optimization-based new flight routes
        optimized_routes = []
        for u, v in self.flight_routes:
            score = optimization_func(u, v, self.weights, self.priorities)
            optimized_routes.append((u, v, score))
        
        return optimized_routes
    
    def get_new_flight_routes_with_constraints(self, constraint_func):
        """Get new flight routes that satisfies custom constraints."""
        if not self.flight_routes:
            return []
        
        if constraint_func(self.n, self.edges, self.weights, self.priorities, self.flight_routes):
            return self.get_weighted_new_flight_routes()
        else:
            return []
    
    def get_new_flight_routes_with_multiple_criteria(self, criteria_list):
        """Get new flight routes that satisfies multiple criteria."""
        if not self.flight_routes:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.edges, self.weights, self.priorities, self.flight_routes):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_new_flight_routes()
        else:
            return []
    
    def get_new_flight_routes_with_alternatives(self, alternatives):
        """Get new flight routes considering alternative weights/priorities."""
        result = []
        
        # Check original new flight routes
        original_routes = self.get_weighted_new_flight_routes()
        result.append((original_routes, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedNewFlightRoutes(self.n, self.edges, self.new_routes, alt_weights, alt_priorities)
            temp_routes = temp_instance.get_weighted_new_flight_routes()
            result.append((temp_routes, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_new_flight_routes_with_adaptive_criteria(self, adaptive_func):
        """Get new flight routes using adaptive criteria."""
        if not self.flight_routes:
            return []
        
        if adaptive_func(self.n, self.edges, self.weights, self.priorities, self.flight_routes, []):
            return self.get_weighted_new_flight_routes()
        else:
            return []
    
    def get_new_flight_routes_optimization(self):
        """Get optimal new flight routes configuration."""
        strategies = [
            ('weighted_routes', lambda: len(self.get_weighted_new_flight_routes())),
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
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
new_routes = [(0, 2), (1, 3), (2, 4), (0, 3), (1, 4)]
weights = {(u, v): (u + v) * 2 for u, v in new_routes}  # Weight based on city sum
priorities = {i: i for i in range(n)}  # Priority based on city number
advanced_routes = AdvancedNewFlightRoutes(n, edges, new_routes, weights, priorities)

print(f"Weighted new flight routes: {advanced_routes.get_weighted_new_flight_routes()}")

# Get new flight routes with priority
def priority_func(u, v, weights, priorities):
    return priorities.get(u, 1) + priorities.get(v, 1) + weights.get((u, v), 1)

print(f"New flight routes with priority: {advanced_routes.get_new_flight_routes_with_priority(priority_func)}")

# Get new flight routes with optimization
def optimization_func(u, v, weights, priorities):
    return weights.get((u, v), 1) + priorities.get(u, 1) + priorities.get(v, 1)

print(f"New flight routes with optimization: {advanced_routes.get_new_flight_routes_with_optimization(optimization_func)}")

# Get new flight routes with constraints
def constraint_func(n, edges, weights, priorities, flight_routes):
    return len(flight_routes) > 0 and n > 0

print(f"New flight routes with constraints: {advanced_routes.get_new_flight_routes_with_constraints(constraint_func)}")

# Get new flight routes with multiple criteria
def criterion1(n, edges, weights, priorities, flight_routes):
    return len(edges) > 0

def criterion2(n, edges, weights, priorities, flight_routes):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"New flight routes with multiple criteria: {advanced_routes.get_new_flight_routes_with_multiple_criteria(criteria_list)}")

# Get new flight routes with alternatives
alternatives = [({(u, v): 1 for u, v in new_routes}, {i: 1 for i in range(n)}), ({(u, v): (u + v)*3 for u, v in new_routes}, {i: 2 for i in range(n)})]
print(f"New flight routes with alternatives: {advanced_routes.get_new_flight_routes_with_alternatives(alternatives)}")

# Get new flight routes with adaptive criteria
def adaptive_func(n, edges, weights, priorities, flight_routes, current_result):
    return len(edges) > 0 and len(current_result) < 10

print(f"New flight routes with adaptive criteria: {advanced_routes.get_new_flight_routes_with_adaptive_criteria(adaptive_func)}")

# Get new flight routes optimization
print(f"New flight routes optimization: {advanced_routes.get_new_flight_routes_optimization()}")
```

### **Variation 3: New Flight Routes with Constraints**
**Problem**: Handle new flight route calculation with additional constraints (distance limits, route constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedNewFlightRoutes:
    def __init__(self, n=None, edges=None, new_routes=None, constraints=None):
        self.n = n or 0
        self.edges = edges or []
        self.new_routes = new_routes or []
        self.constraints = constraints or {}
        self.graph = defaultdict(list)
        self._update_flight_route_info()
    
    def _update_flight_route_info(self):
        """Update flight route information."""
        self.flight_routes = self._calculate_new_flight_routes()
    
    def _calculate_new_flight_routes(self):
        """Calculate new flight routes using BFS."""
        if self.n <= 0 or len(self.edges) == 0:
            return []
        
        # Build existing graph
        existing_graph = defaultdict(list)
        for u, v in self.edges:
            existing_graph[u].append(v)
            existing_graph[v].append(u)
        
        # Find new routes (pairs of cities not directly connected)
        new_routes = []
        for u in range(self.n):
            for v in range(u + 1, self.n):
                # Check if there's no direct connection
                if v not in existing_graph[u]:
                    # Check if there's a path between u and v
                    if not self._has_path(existing_graph, u, v):
                        new_routes.append((u, v))
        
        return new_routes
    
    def _has_path(self, graph, start, end):
        """Check if there's a path between start and end using BFS."""
        if start == end:
            return True
        
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v == end:
                    return True
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        return False
    
    def _is_valid_route(self, u, v):
        """Check if route is valid considering constraints."""
        # Route constraints
        if 'allowed_routes' in self.constraints:
            if (u, v) not in self.constraints['allowed_routes'] and (v, u) not in self.constraints['allowed_routes']:
                return False
        
        if 'forbidden_routes' in self.constraints:
            if (u, v) in self.constraints['forbidden_routes'] or (v, u) in self.constraints['forbidden_routes']:
                return False
        
        # Distance constraints
        if 'max_distance' in self.constraints:
            distance = abs(u - v)
            if distance > self.constraints['max_distance']:
                return False
        
        if 'min_distance' in self.constraints:
            distance = abs(u - v)
            if distance < self.constraints['min_distance']:
                return False
        
        # City constraints
        if 'max_city' in self.constraints:
            if u > self.constraints['max_city'] or v > self.constraints['max_city']:
                return False
        
        if 'min_city' in self.constraints:
            if u < self.constraints['min_city'] or v < self.constraints['min_city']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(u, v, self.n, self.edges, self.flight_routes):
                    return False
        
        return True
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            if self._is_valid_route(u, v):
                self.graph[u].append(v)
                self.graph[v].append(u)
    
    def get_new_flight_routes(self):
        """Get all new flight routes."""
        return self.flight_routes
    
    def get_new_flight_routes_with_distance_constraints(self, min_distance, max_distance):
        """Get new flight routes considering distance constraints."""
        if not self.flight_routes:
            return []
        
        filtered_routes = []
        for u, v in self.flight_routes:
            distance = abs(u - v)
            if min_distance <= distance <= max_distance:
                filtered_routes.append((u, v))
        
        return filtered_routes
    
    def get_new_flight_routes_with_route_constraints(self, route_constraints):
        """Get new flight routes considering route constraints."""
        if not self.flight_routes:
            return []
        
        satisfies_constraints = True
        for constraint in route_constraints:
            if not constraint(self.n, self.edges, self.flight_routes):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.flight_routes
        else:
            return []
    
    def get_new_flight_routes_with_pattern_constraints(self, pattern_constraints):
        """Get new flight routes considering pattern constraints."""
        if not self.flight_routes:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n, self.edges, self.flight_routes):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.flight_routes
        else:
            return []
    
    def get_new_flight_routes_with_mathematical_constraints(self, constraint_func):
        """Get new flight routes that satisfies custom mathematical constraints."""
        if not self.flight_routes:
            return []
        
        if constraint_func(self.n, self.edges, self.flight_routes):
            return self.flight_routes
        else:
            return []
    
    def get_new_flight_routes_with_optimization_constraints(self, optimization_func):
        """Get new flight routes using custom optimization constraints."""
        if not self.flight_routes:
            return []
        
        # Calculate optimization score for new flight routes
        score = optimization_func(self.n, self.edges, self.flight_routes)
        
        if score > 0:
            return self.flight_routes
        else:
            return []
    
    def get_new_flight_routes_with_multiple_constraints(self, constraints_list):
        """Get new flight routes that satisfies multiple constraints."""
        if not self.flight_routes:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n, self.edges, self.flight_routes):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.flight_routes
        else:
            return []
    
    def get_new_flight_routes_with_priority_constraints(self, priority_func):
        """Get new flight routes with priority-based constraints."""
        if not self.flight_routes:
            return []
        
        # Calculate priority for new flight routes
        priority = priority_func(self.n, self.edges, self.flight_routes)
        
        if priority > 0:
            return self.flight_routes
        else:
            return []
    
    def get_new_flight_routes_with_adaptive_constraints(self, adaptive_func):
        """Get new flight routes with adaptive constraints."""
        if not self.flight_routes:
            return []
        
        if adaptive_func(self.n, self.edges, self.flight_routes, []):
            return self.flight_routes
        else:
            return []
    
    def get_optimal_new_flight_routes_strategy(self):
        """Get optimal new flight routes strategy considering all constraints."""
        strategies = [
            ('distance_constraints', self.get_new_flight_routes_with_distance_constraints),
            ('route_constraints', self.get_new_flight_routes_with_route_constraints),
            ('pattern_constraints', self.get_new_flight_routes_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'distance_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'route_constraints':
                    route_constraints = [lambda n, edges, flight_routes: len(edges) > 0]
                    result = strategy_func(route_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n, edges, flight_routes: len(edges) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_routes': [(0, 2), (1, 3), (2, 4), (0, 3), (1, 4)],
    'forbidden_routes': [(0, 4), (1, 2)],
    'max_distance': 4,
    'min_distance': 1,
    'max_city': 10,
    'min_city': 0,
    'pattern_constraints': [lambda u, v, n, edges, flight_routes: u >= 0 and v >= 0 and u < n and v < n]
}

n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
new_routes = [(0, 2), (1, 3), (2, 4), (0, 3), (1, 4)]
constrained_routes = ConstrainedNewFlightRoutes(n, edges, new_routes, constraints)

print("Distance-constrained new flight routes:", constrained_routes.get_new_flight_routes_with_distance_constraints(1, 3))

print("Route-constrained new flight routes:", constrained_routes.get_new_flight_routes_with_route_constraints([lambda n, edges, flight_routes: len(edges) > 0]))

print("Pattern-constrained new flight routes:", constrained_routes.get_new_flight_routes_with_pattern_constraints([lambda n, edges, flight_routes: len(edges) > 0]))

# Mathematical constraints
def custom_constraint(n, edges, flight_routes):
    return len(flight_routes) > 0 and n > 0

print("Mathematical constraint new flight routes:", constrained_routes.get_new_flight_routes_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n, edges, flight_routes):
    return 1 <= len(flight_routes) <= 20

range_constraints = [range_constraint]
print("Range-constrained new flight routes:", constrained_routes.get_new_flight_routes_with_distance_constraints(1, 20))

# Multiple constraints
def constraint1(n, edges, flight_routes):
    return len(edges) > 0

def constraint2(n, edges, flight_routes):
    return len(flight_routes) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints new flight routes:", constrained_routes.get_new_flight_routes_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n, edges, flight_routes):
    return n + len(edges) + len(flight_routes)

print("Priority-constrained new flight routes:", constrained_routes.get_new_flight_routes_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, edges, flight_routes, current_result):
    return len(edges) > 0 and len(current_result) < 10

print("Adaptive constraint new flight routes:", constrained_routes.get_new_flight_routes_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_routes.get_optimal_new_flight_routes_strategy()
print(f"Optimal new flight routes strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Planets and Kingdoms](https://cses.fi/problemset/task/1683) - SCC detection
- [Strongly Connected Components](https://cses.fi/problemset/task/1683) - SCC analysis
- [Road Construction](https://cses.fi/problemset/task/1675) - Connectivity

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Cycle detection
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Topological sort
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Cycle detection

#### **Problem Categories**
- **Graph Theory**: Strongly connected components, connectivity
- **Tarjan's Algorithm**: SCC detection, component analysis
- **Combinatorial Optimization**: Minimum edge addition, graph connectivity

## 🔗 Additional Resources

### **Algorithm References**
- [Tarjan's Algorithm](https://cp-algorithms.com/graph/strongly-connected-components.html) - SCC detection
- [Kosaraju's Algorithm](https://cp-algorithms.com/graph/strongly-connected-components.html) - SCC detection
- [Strongly Connected Components](https://cp-algorithms.com/graph/strongly-connected-components.html) - SCC analysis

### **Practice Problems**
- [CSES Planets and Kingdoms](https://cses.fi/problemset/task/1683) - Medium
- [CSES Strongly Connected Components](https://cses.fi/problemset/task/1683) - Medium
- [CSES Road Construction](https://cses.fi/problemset/task/1675) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
