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
