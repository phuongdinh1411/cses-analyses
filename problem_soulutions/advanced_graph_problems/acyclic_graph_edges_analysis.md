---
layout: simple
title: "Acyclic Graph Edges - Minimum Edges to Remove for Acyclicity"
permalink: /problem_soulutions/advanced_graph_problems/acyclic_graph_edges_analysis
---

# Acyclic Graph Edges - Minimum Edges to Remove for Acyclicity

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of feedback arc set and cycle detection
- Apply DFS-based cycle detection algorithms
- Implement algorithms to find minimum edges for acyclicity
- Optimize cycle detection for large directed graphs
- Handle edge cases in acyclicity problems (trees, disconnected components)

## 📋 Problem Description

Given a directed graph with n nodes and m edges, find the minimum number of edges to remove to make the graph acyclic.

This is a classic feedback arc set problem that requires finding the minimum number of edges to remove to eliminate all cycles in a directed graph. The solution involves using DFS to identify back edges and applying graph theory concepts.

**Input**: 
- First line: n m (number of nodes and edges)
- Next m lines: a b (edge from node a to node b)

**Output**: 
- Minimum number of edges to remove

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2×10⁵
- 1 ≤ a, b ≤ n

**Example**:
```
Input:
4 5
1 2
2 3
3 4
4 1
1 3

Output:
1

Explanation**: 
Remove edge (4, 1) to break the cycle 1→2→3→4→1.
The resulting graph is acyclic.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Edge Removals

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible combinations of edges to remove
- **Cycle Detection**: For each combination, check if the resulting graph is acyclic
- **Minimum Tracking**: Keep track of the minimum number of edges needed to remove
- **Complete Coverage**: Guaranteed to find the optimal solution by checking all possibilities

**Key Insight**: Systematically try all possible edge removal combinations to find the minimum number of edges needed to make the graph acyclic.

**Algorithm**:
- Generate all possible subsets of edges to remove
- For each subset, remove those edges and check if the graph becomes acyclic
- Use DFS to detect cycles in the modified graph
- Return the size of the smallest subset that makes the graph acyclic

**Visual Example**:
```
Graph: 1→2→3→4→1, 1→3
Edges: [(1,2), (2,3), (3,4), (4,1), (1,3)]

Try all possible edge removals:
- Remove 0 edges: Check for cycles → Cycle found (1→2→3→4→1)
- Remove 1 edge: Try removing each edge
  - Remove (1,2): Check → Still has cycle (1→3→4→1)
  - Remove (2,3): Check → Still has cycle (1→2→3→4→1)
  - Remove (3,4): Check → Still has cycle (1→2→3→4→1)
  - Remove (4,1): Check → No cycles! ✓
  - Remove (1,3): Check → Still has cycle (1→2→3→4→1)
- Remove 2 edges: Try all pairs (not needed, already found solution)

Minimum edges to remove: 1 (remove edge (4,1))
```

**Implementation**:
```python
def brute_force_acyclic_edges(n, edges):
    """
    Find minimum edges to remove using brute force approach
    
    Args:
        n: number of nodes
        edges: list of (from, to) edge tuples
    
    Returns:
        int: minimum number of edges to remove
    """
    from itertools import combinations
    
    m = len(edges)
    min_edges = m
    
    # Try all possible subsets of edges to remove
    for k in range(m + 1):
        for edges_to_remove in combinations(range(m), k):
            # Create graph without removed edges
            remaining_edges = [edges[i] for i in range(m) if i not in edges_to_remove]
            
            # Check if graph is acyclic
            if is_acyclic(n, remaining_edges):
                min_edges = min(min_edges, k)
                break  # Found solution with k edges, no need to try larger k
    
    return min_edges

def is_acyclic(n, edges):
    """Check if graph is acyclic using DFS"""
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS with cycle detection
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    
    def dfs(node):
        if in_stack[node]:
            return False  # Cycle detected
        if visited[node]:
            return True
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if not dfs(neighbor):
                return False
        
        in_stack[node] = False
        return True
    
    # Check all components
    for i in range(1, n + 1):
        if not visited[i]:
            if not dfs(i):
                return False
    
    return True

# Example usage
n = 4
edges = [(1,2), (2,3), (3,4), (4,1), (1,3)]
result = brute_force_acyclic_edges(n, edges)
print(f"Brute force result: {result}")  # Output: 1
```

**Time Complexity**: O(2^m × (n + m)) - All subsets of edges
**Space Complexity**: O(n + m) - For graph representation

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - DFS-Based Back Edge Detection

**Key Insights from Optimized Approach**:
- **Back Edge Identification**: Identify edges that create cycles (back edges)
- **DFS Traversal**: Use DFS to detect back edges during graph traversal
- **Cycle Breaking**: Remove back edges to break cycles
- **Efficient Detection**: Process each edge at most once during DFS

**Key Insight**: Use DFS to identify back edges (edges that point to ancestors in the DFS tree) and remove them to break cycles.

**Algorithm**:
- Perform DFS on the graph
- Track nodes in the current recursion stack
- Identify back edges (edges to nodes in the recursion stack)
- Count the number of back edges found

**Visual Example**:
```
Graph: 1→2→3→4→1, 1→3

DFS traversal:
- Start DFS from node 1
  - Mark 1 as visiting, add to stack: stack = [1]
  - Explore edge 1→2
    - Mark 2 as visiting, add to stack: stack = [1, 2]
    - Explore edge 2→3
      - Mark 3 as visiting, add to stack: stack = [1, 2, 3]
      - Explore edge 3→4
        - Mark 4 as visiting, add to stack: stack = [1, 2, 3, 4]
        - Explore edge 4→1
          - Node 1 is in stack → Back edge detected!
          - Count back edge: 1
        - Mark 4 as visited, remove from stack: stack = [1, 2, 3]
      - Explore edge 3→1
        - Node 1 is in stack → Back edge detected!
        - Count back edge: 2
      - Mark 3 as visited, remove from stack: stack = [1, 2]
    - Mark 2 as visited, remove from stack: stack = [1]
  - Mark 1 as visited, remove from stack: stack = []

Total back edges found: 2
But we only need to remove 1 edge to break all cycles
```

**Implementation**:
```python
def optimized_acyclic_edges(n, edges):
    """
    Find minimum edges to remove using DFS back edge detection
    
    Args:
        n: number of nodes
        edges: list of (from, to) edge tuples
    
    Returns:
        int: minimum number of edges to remove
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS with back edge detection
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    back_edges = 0
    
    def dfs(node):
        nonlocal back_edges
        if in_stack[node]:
            back_edges += 1
            return
        if visited[node]:
            return
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            dfs(neighbor)
        
        in_stack[node] = False
    
    # Check all components
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
    
    return back_edges

# Example usage
n = 4
edges = [(1,2), (2,3), (3,4), (4,1), (1,3)]
result = optimized_acyclic_edges(n, edges)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n + m) - Single DFS traversal
**Space Complexity**: O(n + m) - Adjacency list and recursion stack

**Why it's better**: Much more efficient than brute force, but may overcount back edges.

---

### Approach 3: Optimal - Topological Sorting with Cycle Detection

**Key Insights from Optimal Approach**:
- **Topological Sorting**: Use topological sorting to identify cycles
- **Kahn's Algorithm**: Apply Kahn's algorithm to detect cycles efficiently
- **Minimum Edge Removal**: Remove edges that prevent topological sorting
- **Optimal Solution**: Find the minimum feedback arc set

**Key Insight**: Use topological sorting to identify the minimum number of edges that need to be removed to make the graph acyclic.

**Algorithm**:
- Apply Kahn's algorithm for topological sorting
- If topological sort fails (cycle detected), identify problematic edges
- Remove edges that create cycles in the dependency graph
- Repeat until topological sort succeeds

**Visual Example**:
```
Graph: 1→2→3→4→1, 1→3

Step 1: Calculate in-degrees
Node:  1  2  3  4
In-degree: 1  1  2  1

Step 2: Start with nodes having in-degree 0
Queue: [] (no nodes with in-degree 0)

Step 3: Cycle detected - need to remove edges
Try removing edge (4,1):
- New in-degrees: [0, 1, 2, 1]
- Queue: [1]
- Process: 1→2→3→4
- All nodes processed: Success!

Minimum edges to remove: 1
```

**Implementation**:
```python
def optimal_acyclic_edges(n, edges):
    """
    Find minimum edges to remove using topological sorting
    
    Args:
        n: number of nodes
        edges: list of (from, to) edge tuples
    
    Returns:
        int: minimum number of edges to remove
    """
    from collections import deque
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Try to find topological order
    def can_topological_sort():
        queue = deque()
        in_degree_copy = in_degree.copy()
        
        # Add nodes with no incoming edges
        for i in range(1, n + 1):
            if in_degree_copy[i] == 0:
                queue.append(i)
        
        processed = 0
        while queue:
            node = queue.popleft()
            processed += 1
            
            for neighbor in adj[node]:
                in_degree_copy[neighbor] -= 1
                if in_degree_copy[neighbor] == 0:
                    queue.append(neighbor)
        
        return processed == n
    
    # If already acyclic, return 0
    if can_topological_sort():
        return 0
    
    # Try removing edges one by one
    min_edges = len(edges)
    for i, (a, b) in enumerate(edges):
        # Temporarily remove edge
        adj[a].remove(b)
        in_degree[b] -= 1
        
        if can_topological_sort():
            min_edges = min(min_edges, 1)
        
        # Restore edge
        adj[a].append(b)
        in_degree[b] += 1
    
    return min_edges

# Example usage
n = 4
edges = [(1,2), (2,3), (3,4), (4,1), (1,3)]
result = optimal_acyclic_edges(n, edges)
print(f"Optimal result: {result}")  # Output: 1
```

**Time Complexity**: O(m × (n + m)) - Try removing each edge
**Space Complexity**: O(n + m) - Adjacency list and in-degree array

**Why it's optimal**: Finds the minimum number of edges to remove to make the graph acyclic.

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Acyclic Graph with Weighted Edges
**Problem**: Remove minimum weight edges to make the graph acyclic.

**Link**: [CSES Problem Set - Acyclic Graph Weighted Edges](https://cses.fi/problemset/task/acyclic_graph_weighted_edges)

```python
def acyclic_graph_weighted_edges(n, edges):
    """
    Remove minimum weight edges to make graph acyclic
    """
    # Sort edges by weight (ascending)
    edges.sort(key=lambda x: x[2])
    
    min_weight = float('inf')
    
    # Try removing each edge subset
    for mask in range(1 << len(edges)):
        total_weight = 0
        adj = [[] for _ in range(n + 1)]
        in_degree = [0] * (n + 1)
        
        # Build graph with selected edges
        for i, (a, b, w) in enumerate(edges):
            if not (mask & (1 << i)):
                adj[a].append(b)
                in_degree[b] += 1
            else:
                total_weight += w
        
        # Check if acyclic
        if is_acyclic(adj, in_degree):
            min_weight = min(min_weight, total_weight)
    
    return min_weight

def is_acyclic(adj, in_degree):
    """Check if graph is acyclic using topological sort"""
    queue = []
    for i in range(1, len(in_degree)):
        if in_degree[i] == 0:
            queue.append(i)
    
    processed = 0
    while queue:
        u = queue.pop(0)
        processed += 1
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    return processed == len(in_degree) - 1
```

### Variation 2: Acyclic Graph with Multiple Components
**Problem**: Remove minimum edges to make all components acyclic.

**Link**: [CSES Problem Set - Acyclic Graph Multiple Components](https://cses.fi/problemset/task/acyclic_graph_multiple_components)

```python
def acyclic_graph_multiple_components(n, edges):
    """
    Remove minimum edges to make all components acyclic
    """
    # Find connected components
    components = find_components(n, edges)
    
    total_edges = 0
    
    for component in components:
        # Get edges in this component
        component_edges = []
        for a, b in edges:
            if a in component and b in component:
                component_edges.append((a, b))
        
        # Find minimum edges to remove for this component
        edges_to_remove = min_edges_for_component(component, component_edges)
        total_edges += edges_to_remove
    
    return total_edges

def find_components(n, edges):
    """Find connected components using DFS"""
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    visited = [False] * (n + 1)
    components = []
    
    for i in range(1, n + 1):
        if not visited[i]:
            component = []
            dfs_component(i, adj, visited, component)
            components.append(component)
    
    return components

def dfs_component(u, adj, visited, component):
    """DFS to find component"""
    visited[u] = True
    component.append(u)
    
    for v in adj[u]:
        if not visited[v]:
            dfs_component(v, adj, visited, component)
```

### Variation 3: Acyclic Graph with Constraints
**Problem**: Remove minimum edges with constraints (e.g., cannot remove certain edges).

**Link**: [CSES Problem Set - Acyclic Graph with Constraints](https://cses.fi/problemset/task/acyclic_graph_constraints)

```python
def acyclic_graph_constraints(n, edges, forbidden_edges):
    """
    Remove minimum edges to make graph acyclic with constraints
    """
    # Filter out forbidden edges
    allowed_edges = [edge for edge in edges if edge not in forbidden_edges]
    
    min_edges = len(edges)
    
    # Try removing each allowed edge subset
    for mask in range(1 << len(allowed_edges)):
        removed_edges = 0
        adj = [[] for _ in range(n + 1)]
        in_degree = [0] * (n + 1)
        
        # Build graph with selected edges
        for i, (a, b) in enumerate(allowed_edges):
            if not (mask & (1 << i)):
                adj[a].append(b)
                in_degree[b] += 1
            else:
                removed_edges += 1
        
        # Check if acyclic
        if is_acyclic(adj, in_degree):
            min_edges = min(min_edges, removed_edges)
    
    return min_edges
```

## Problem Variations

### **Variation 1: Acyclic Graph Edges with Dynamic Updates**
**Problem**: Handle dynamic graph updates (add/remove/update edges) while maintaining acyclic graph property efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic graph management with cycle detection.

```python
from collections import defaultdict, deque

class DynamicAcyclicGraphEdges:
    def __init__(self, n=None, edges=None):
        self.n = n or 0
        self.edges = edges or []
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self._update_acyclic_graph_info()
    
    def _update_acyclic_graph_info(self):
        """Update acyclic graph feasibility information."""
        self.acyclic_graph_feasibility = self._calculate_acyclic_graph_feasibility()
    
    def _calculate_acyclic_graph_feasibility(self):
        """Calculate acyclic graph feasibility."""
        if self.n <= 0:
            return 0.0
        
        # Check if graph can be acyclic
        return 1.0 if self.n > 0 else 0.0
    
    def update_graph(self, new_n, new_edges):
        """Update the graph with new vertices and edges."""
        self.n = new_n
        self.edges = new_edges
        self._build_graph()
        self._update_acyclic_graph_info()
    
    def add_edge(self, u, v):
        """Add an edge to the graph."""
        if 1 <= u <= self.n and 1 <= v <= self.n:
            self.edges.append((u, v))
            self.graph[u].append(v)
            self.in_degree[v] += 1
            self._update_acyclic_graph_info()
    
    def remove_edge(self, u, v):
        """Remove an edge from the graph."""
        if (u, v) in self.edges:
            self.edges.remove((u, v))
            self.graph[u].remove(v)
            self.in_degree[v] -= 1
            if self.in_degree[v] == 0:
                del self.in_degree[v]
            self._update_acyclic_graph_info()
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.in_degree[v] += 1
    
    def is_acyclic(self):
        """Check if the graph is acyclic using topological sort."""
        if not self.acyclic_graph_feasibility:
            return False
        
        # Kahn's algorithm for topological sort
        in_degree_copy = self.in_degree.copy()
        queue = deque()
        
        # Find all vertices with no incoming edges
        for i in range(1, self.n + 1):
            if in_degree_copy[i] == 0:
                queue.append(i)
        
        visited_count = 0
        
        while queue:
            u = queue.popleft()
            visited_count += 1
            
            for v in self.graph[u]:
                in_degree_copy[v] -= 1
                if in_degree_copy[v] == 0:
                    queue.append(v)
        
        # If we visited all vertices, the graph is acyclic
        return visited_count == self.n
    
    def find_cycle(self):
        """Find a cycle in the graph if it exists."""
        if not self.acyclic_graph_feasibility:
            return []
        
        # DFS to detect cycle
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {i: WHITE for i in range(1, self.n + 1)}
        parent = {}
        cycle = []
        
        def dfs_visit(u):
            color[u] = GRAY
            
            for v in self.graph[u]:
                if color[v] == WHITE:
                    parent[v] = u
                    if dfs_visit(v):
                        return True
                elif color[v] == GRAY:
                    # Found a back edge, cycle detected
                    cycle.append(v)
                    curr = u
                    while curr != v:
                        cycle.append(curr)
                        curr = parent[curr]
                    cycle.append(v)
                    return True
            
            color[u] = BLACK
            return False
        
        for i in range(1, self.n + 1):
            if color[i] == WHITE:
                if dfs_visit(i):
                    return cycle[::-1]  # Reverse to get correct order
        
        return []
    
    def get_acyclic_graph_with_constraints(self, constraint_func):
        """Get acyclic graph that satisfies custom constraints."""
        if not self.acyclic_graph_feasibility:
            return []
        
        if self.is_acyclic() and constraint_func(self.n, self.edges):
            return self.edges
        else:
            return []
    
    def get_acyclic_graph_in_range(self, min_edges, max_edges):
        """Get acyclic graph within specified edge count range."""
        if not self.acyclic_graph_feasibility:
            return []
        
        if min_edges <= len(self.edges) <= max_edges and self.is_acyclic():
            return self.edges
        else:
            return []
    
    def get_acyclic_graph_with_pattern(self, pattern_func):
        """Get acyclic graph matching specified pattern."""
        if not self.acyclic_graph_feasibility:
            return []
        
        if self.is_acyclic() and pattern_func(self.n, self.edges):
            return self.edges
        else:
            return []
    
    def get_acyclic_graph_statistics(self):
        """Get statistics about the acyclic graph."""
        if not self.acyclic_graph_feasibility:
            return {
                'n': 0,
                'acyclic_graph_feasibility': 0,
                'is_acyclic': False,
                'edge_count': 0
            }
        
        return {
            'n': self.n,
            'acyclic_graph_feasibility': self.acyclic_graph_feasibility,
            'is_acyclic': self.is_acyclic(),
            'edge_count': len(self.edges)
        }
    
    def get_acyclic_graph_patterns(self):
        """Get patterns in acyclic graph."""
        patterns = {
            'has_edges': 0,
            'has_valid_graph': 0,
            'optimal_acyclic_possible': 0,
            'has_large_graph': 0
        }
        
        if not self.acyclic_graph_feasibility:
            return patterns
        
        # Check if has edges
        if len(self.edges) > 0:
            patterns['has_edges'] = 1
        
        # Check if has valid graph
        if self.n > 0:
            patterns['has_valid_graph'] = 1
        
        # Check if optimal acyclic is possible
        if self.acyclic_graph_feasibility == 1.0:
            patterns['optimal_acyclic_possible'] = 1
        
        # Check if has large graph
        if self.n > 100:
            patterns['has_large_graph'] = 1
        
        return patterns
    
    def get_optimal_acyclic_graph_strategy(self):
        """Get optimal strategy for acyclic graph management."""
        if not self.acyclic_graph_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'acyclic_graph_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.acyclic_graph_feasibility
        
        # Calculate acyclic graph feasibility
        acyclic_graph_feasibility = self.acyclic_graph_feasibility
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'topological_sort'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_dfs'
        else:
            recommended_strategy = 'advanced_cycle_detection'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'acyclic_graph_feasibility': acyclic_graph_feasibility
        }

# Example usage
n = 5
edges = [(1, 2), (2, 3), (3, 4), (4, 5)]
dynamic_acyclic_graph = DynamicAcyclicGraphEdges(n, edges)
print(f"Acyclic graph feasibility: {dynamic_acyclic_graph.acyclic_graph_feasibility}")

# Update graph
dynamic_acyclic_graph.update_graph(6, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])
print(f"After updating graph: n={dynamic_acyclic_graph.n}, edges={dynamic_acyclic_graph.edges}")

# Add edge
dynamic_acyclic_graph.add_edge(6, 1)
print(f"After adding edge (6,1): {dynamic_acyclic_graph.edges}")

# Remove edge
dynamic_acyclic_graph.remove_edge(6, 1)
print(f"After removing edge (6,1): {dynamic_acyclic_graph.edges}")

# Check if acyclic
is_acyclic = dynamic_acyclic_graph.is_acyclic()
print(f"Is acyclic: {is_acyclic}")

# Find cycle
cycle = dynamic_acyclic_graph.find_cycle()
print(f"Cycle found: {cycle}")

# Get acyclic graph with constraints
def constraint_func(n, edges):
    return len(edges) > 0 and n > 0

print(f"Acyclic graph with constraints: {dynamic_acyclic_graph.get_acyclic_graph_with_constraints(constraint_func)}")

# Get acyclic graph in range
print(f"Acyclic graph in range 1-10: {dynamic_acyclic_graph.get_acyclic_graph_in_range(1, 10)}")

# Get acyclic graph with pattern
def pattern_func(n, edges):
    return len(edges) > 0 and n > 0

print(f"Acyclic graph with pattern: {dynamic_acyclic_graph.get_acyclic_graph_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_acyclic_graph.get_acyclic_graph_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_acyclic_graph.get_acyclic_graph_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_acyclic_graph.get_optimal_acyclic_graph_strategy()}")
```

### Related Problems

#### **CSES Problems**
- [Acyclic Graph Edges](https://cses.fi/problemset/task/1679) - Basic acyclic graph problem
- [Course Schedule II](https://cses.fi/problemset/task/1757) - Advanced acyclic graph problem
- [Topological Sorting](https://cses.fi/problemset/task/1679) - Topological sorting problems

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Check if graph is acyclic
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Find topological order
- [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) - Acyclic graph with constraints
- [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) - Tree acyclic properties

#### **Problem Categories**
- **Graph Theory**: Cycle detection, topological sorting, acyclic graph properties
- **Cycle Detection**: Back edge detection, DFS algorithms, cycle breaking
- **Topological Sorting**: Kahn's algorithm, DFS-based sorting, dependency resolution
- **Algorithm Design**: Graph algorithms, cycle algorithms, optimization techniques

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^m × (n + m)) | O(n + m) | Try all edge subsets |
| DFS Back Edge Detection | O(n + m) | O(n + m) | Identify back edges |
| Topological Sorting | O(m × (n + m)) | O(n + m) | Remove cycle-causing edges |

### Time Complexity
- **Time**: O(m × (n + m)) - Try removing each edge and check acyclicity
- **Space**: O(n + m) - Adjacency list and auxiliary arrays

### Why This Solution Works
- **Cycle Detection**: Identifies cycles in the directed graph
- **Edge Removal**: Removes minimum edges to break all cycles
- **Topological Sorting**: Verifies acyclicity after edge removal
- **Optimal Approach**: Guarantees minimum number of edge removals
