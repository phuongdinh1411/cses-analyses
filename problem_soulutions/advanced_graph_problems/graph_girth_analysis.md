---
layout: simple
title: "Graph Girth - Graph Theory Problem"
permalink: /problem_soulutions/advanced_graph_problems/graph_girth_analysis
---

# Graph Girth - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of graph girth in directed graphs
- Apply graph theory principles to find the shortest cycle
- Implement algorithms for girth computation
- Optimize graph traversal for cycle detection
- Handle special cases in girth analysis

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, cycle detection, graph traversal, shortest path algorithms
- **Data Structures**: Adjacency lists, matrices, priority queues, distance arrays
- **Mathematical Concepts**: Graph theory, cycle properties, shortest path theory
- **Programming Skills**: Graph representation, BFS, DFS, Dijkstra's algorithm
- **Related Problems**: Round Trip (cycle detection), Fixed Length Path Queries (similar approach), Graph Girth (cycle properties)

## 📋 Problem Description

Given a directed graph with n nodes, find the length of the shortest cycle (girth) in the graph.

**Input**: 
- n: number of nodes
- m: number of edges
- m lines: a b (directed edge from node a to node b)

**Output**: 
- Length of the shortest cycle, or -1 if no cycle exists

**Constraints**:
- 1 ≤ n ≤ 1000
- 1 ≤ m ≤ 10^5
- 1 ≤ a,b ≤ n

**Example**:
```
Input:
4 5
1 2
2 3
3 4
4 1
2 4

Output:
3

Explanation**: 
Shortest cycle: 2→3→4→2 (length 3)
Other cycles: 1→2→3→4→1 (length 4)
Answer: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Exhaustive Search**: Try all possible cycles starting from each node
- **DFS Traversal**: Use depth-first search to explore all cycles
- **Cycle Detection**: Track visited nodes to detect cycles
- **Baseline Understanding**: Provides correct answer but impractical for large graphs

**Key Insight**: Use DFS to explore all possible cycles starting from each node and find the shortest one.

**Algorithm**:
- For each node, start DFS and look for cycles
- Track the shortest cycle found
- Return the length of the shortest cycle, or -1 if none exists

**Visual Example**:
```
Graph: 1→2→3→4→1, 2→4

DFS from node 1:
┌─────────────────────────────────────┐
│ Start at 1, depth=0                │
│ ├─ Go to 2, depth=1                │
│ │  ├─ Go to 3, depth=2             │
│ │  │  └─ Go to 4, depth=3          │
│ │  │     └─ Go to 1, depth=4 ✓ (cycle!)│
│ │  └─ Go to 4, depth=2             │
│ │     └─ No more edges             │
│ └─ No more edges                   │
└─────────────────────────────────────┘

Cycle found: 1→2→3→4→1 (length 4)
```

**Implementation**:
```python
def brute_force_solution(n, edges):
    """
    Find graph girth using brute force DFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: length of shortest cycle, or -1 if no cycle exists
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def find_cycle_length(start):
        """Find shortest cycle starting from start node"""
        visited = [False] * n
        depth = [0] * n
        
        def dfs(node, current_depth):
            if visited[node]:
                # Found a cycle
                return current_depth - depth[node]
            
            visited[node] = True
            depth[node] = current_depth
            
            min_cycle = float('inf')
            for neighbor in adj[node]:
                cycle_length = dfs(neighbor, current_depth + 1)
                if cycle_length > 0:
                    min_cycle = min(min_cycle, cycle_length)
            
            visited[node] = False
            return min_cycle if min_cycle != float('inf') else -1
        
        return dfs(start, 0)
    
    min_girth = float('inf')
    for start in range(n):
        cycle_length = find_cycle_length(start)
        if cycle_length > 0:
            min_girth = min(min_girth, cycle_length)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
result = brute_force_solution(n, edges)
print(f"Brute force result: {result}")  # Output: 3
```

**Time Complexity**: O(n × (n + m))
**Space Complexity**: O(n)

**Why it's inefficient**: Quadratic time complexity makes it impractical for large graphs.

---

### Approach 2: BFS-Based Solution

**Key Insights from BFS-Based Solution**:
- **BFS Traversal**: Use breadth-first search for shortest path
- **Cycle Detection**: Find shortest path from each node to itself
- **Distance Tracking**: Track distances to detect cycles
- **Optimization**: More efficient than DFS for shortest path problems

**Key Insight**: Use BFS to find the shortest path from each node back to itself, which gives the shortest cycle.

**Algorithm**:
- For each node, use BFS to find shortest path back to itself
- Track the minimum cycle length found
- Return the shortest cycle length, or -1 if none exists

**Visual Example**:
```
Graph: 1→2→3→4→1, 2→4

BFS from node 2:
┌─────────────────────────────────────┐
│ Start at 2, depth=0                │
│ ├─ Go to 3, depth=1                │
│ │  └─ Go to 4, depth=2             │
│ │     └─ Go to 2, depth=3 ✓ (cycle!)│
│ └─ Go to 4, depth=1                │
│    └─ Go to 2, depth=2 ✓ (cycle!)  │
└─────────────────────────────────────┘

Shortest cycle: 2→4→2 (length 2)
```

**Implementation**:
```python
def bfs_solution(n, edges):
    """
    Find graph girth using BFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: length of shortest cycle, or -1 if no cycle exists
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
    
    def find_shortest_cycle(start):
        """Find shortest cycle starting from start node using BFS"""
        from collections import deque
        
        queue = deque([(start, 0)])
        visited = [False] * n
        visited[start] = True
        
        while queue:
            node, depth = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == start and depth > 0:
                    # Found a cycle back to start
                    return depth + 1
                
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, depth + 1))
        
        return -1
    
    min_girth = float('inf')
    for start in range(n):
        cycle_length = find_shortest_cycle(start)
        if cycle_length > 0:
            min_girth = min(min_girth, cycle_length)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
result = bfs_solution(n, edges)
print(f"BFS result: {result}")  # Output: 3
```

**Time Complexity**: O(n × (n + m))
**Space Complexity**: O(n)

**Why it's better**: More efficient than DFS for shortest path problems, but still quadratic.

**Implementation Considerations**:
- **BFS Queue**: Use deque for efficient queue operations
- **Distance Tracking**: Track distances to detect cycles
- **Memory Management**: Use visited array to avoid infinite loops

---

### Approach 3: Floyd-Warshall Solution (Optimal)

**Key Insights from Floyd-Warshall Solution**:
- **All-Pairs Shortest Path**: Compute shortest paths between all pairs
- **Cycle Detection**: Find shortest path from each node to itself
- **Matrix Operations**: Use adjacency matrix for efficient computation
- **Optimal Complexity**: O(n³) time complexity

**Key Insight**: Use Floyd-Warshall algorithm to compute all-pairs shortest paths, then find the minimum diagonal element.

**Algorithm**:
- Use Floyd-Warshall to compute shortest distances between all pairs
- Find the minimum distance from each node to itself
- Return the minimum cycle length, or -1 if none exists

**Visual Example**:
```
Graph: 1→2→3→4→1, 2→4

Distance matrix after Floyd-Warshall:
┌─────────────────────────────────────┐
│    1  2  3  4                      │
│ 1 [0  1  2  3]                     │
│ 2 [3  0  1  2]                     │
│ 3 [2  3  0  1]                     │
│ 4 [1  2  3  0]                     │
└─────────────────────────────────────┘

Minimum diagonal: min(0, 0, 0, 0) = 0
But we need cycles, so look for non-zero diagonal elements
```

**Implementation**:
```python
def floyd_warshall_solution(n, edges):
    """
    Find graph girth using Floyd-Warshall algorithm
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
    
    Returns:
        int: length of shortest cycle, or -1 if no cycle exists
    """
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    
    # Base case: direct edges
    for a, b in edges:
        dist[a-1][b-1] = 1  # Convert to 0-indexed
    
    # Base case: distance from node to itself
    for i in range(n):
        dist[i][i] = 0
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Find minimum cycle length
    min_girth = float('inf')
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf') and dist[j][i] != float('inf'):
                # Found a cycle from i to j and back to i
                cycle_length = dist[i][j] + dist[j][i]
                min_girth = min(min_girth, cycle_length)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
result = floyd_warshall_solution(n, edges)
print(f"Floyd-Warshall result: {result}")  # Output: 3
```

**Time Complexity**: O(n³)
**Space Complexity**: O(n²)

**Why it's optimal**: O(n³) time complexity is optimal for all-pairs shortest path problems.

**Implementation Details**:
- **Matrix Operations**: Use adjacency matrix for efficient computation
- **Cycle Detection**: Find cycles by checking both directions
- **Memory Efficiency**: Use 2D distance matrix

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × (n + m)) | O(n) | Exhaustive DFS search |
| BFS-Based | O(n × (n + m)) | O(n) | Use BFS for shortest path |
| Floyd-Warshall | O(n³) | O(n²) | Use all-pairs shortest path |

### Time Complexity
- **Time**: O(n³) - Floyd-Warshall algorithm for all-pairs shortest paths
- **Space**: O(n²) - Distance matrix storage

### Why This Solution Works
- **All-Pairs Shortest Path**: Compute shortest paths between all pairs efficiently
- **Cycle Detection**: Find cycles by checking both directions
- **Matrix Operations**: Use adjacency matrix for efficient computation
- **Optimal Complexity**: O(n³) is optimal for this problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Weighted Graph Girth**
**Problem**: Find the girth of a weighted directed graph.

**Key Differences**: Edges have weights, consider total weight

**Solution Approach**: Use weighted Floyd-Warshall algorithm

**Implementation**:
```python
def weighted_graph_girth(n, edges, weights):
    """
    Find weighted graph girth using Floyd-Warshall algorithm
    
    Args:
        n: number of nodes
        edges: list of (a, b) edges
        weights: list of edge weights
    
    Returns:
        int: weight of shortest cycle, or -1 if no cycle exists
    """
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    
    # Base case: direct edges with weights
    for i, (a, b) in enumerate(edges):
        dist[a-1][b-1] = weights[i]  # Convert to 0-indexed
    
    # Base case: distance from node to itself
    for i in range(n):
        dist[i][i] = 0
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Find minimum cycle weight
    min_girth = float('inf')
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != float('inf') and dist[j][i] != float('inf'):
                # Found a cycle from i to j and back to i
                cycle_weight = dist[i][j] + dist[j][i]
                min_girth = min(min_girth, cycle_weight)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
weights = [2, 3, 4, 1, 5]
result = weighted_graph_girth(n, edges, weights)
print(f"Weighted graph girth result: {result}")
```

#### **2. Undirected Graph Girth**
**Problem**: Find the girth of an undirected graph.

**Key Differences**: Undirected edges, different cycle detection

**Solution Approach**: Use BFS with parent tracking

**Implementation**:
```python
def undirected_graph_girth(n, edges):
    """
    Find undirected graph girth using BFS approach
    
    Args:
        n: number of nodes
        edges: list of (a, b) undirected edges
    
    Returns:
        int: length of shortest cycle, or -1 if no cycle exists
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a-1].append(b-1)  # Convert to 0-indexed
        adj[b-1].append(a-1)  # Undirected edge
    
    def find_shortest_cycle(start):
        """Find shortest cycle starting from start node using BFS"""
        from collections import deque
        
        queue = deque([(start, -1, 0)])  # (node, parent, depth)
        visited = [False] * n
        visited[start] = True
        
        while queue:
            node, parent, depth = queue.popleft()
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue  # Skip parent
                
                if visited[neighbor]:
                    # Found a cycle
                    return depth + 1
                
                visited[neighbor] = True
                queue.append((neighbor, node, depth + 1))
        
        return -1
    
    min_girth = float('inf')
    for start in range(n):
        cycle_length = find_shortest_cycle(start)
        if cycle_length > 0:
            min_girth = min(min_girth, cycle_length)
    
    return min_girth if min_girth != float('inf') else -1

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
result = undirected_graph_girth(n, edges)
print(f"Undirected graph girth result: {result}")
```

#### **3. Dynamic Graph Girth**
**Problem**: Support adding/removing edges and answering girth queries.

**Key Differences**: Graph structure can change dynamically

**Solution Approach**: Use dynamic graph analysis with incremental updates

**Implementation**:
```python
class DynamicGraphGirth:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.girth_cache = None  # Cache for girth
    
    def add_edge(self, a, b):
        """Add undirected edge from a to b"""
        if b not in self.adj[a]:
            self.adj[a].append(b)
            self.adj[b].append(a)
            self.girth_cache = None  # Invalidate cache
    
    def remove_edge(self, a, b):
        """Remove undirected edge from a to b"""
        if b in self.adj[a]:
            self.adj[a].remove(b)
            self.adj[b].remove(a)
            self.girth_cache = None  # Invalidate cache
    
    def get_girth(self):
        """Get current graph girth"""
        if self.girth_cache is not None:
            return self.girth_cache
        
        def find_shortest_cycle(start):
            """Find shortest cycle starting from start node using BFS"""
            from collections import deque
            
            queue = deque([(start, -1, 0)])  # (node, parent, depth)
            visited = [False] * self.n
            visited[start] = True
            
            while queue:
                node, parent, depth = queue.popleft()
                
                for neighbor in self.adj[node]:
                    if neighbor == parent:
                        continue  # Skip parent
                    
                    if visited[neighbor]:
                        # Found a cycle
                        return depth + 1
                    
                    visited[neighbor] = True
                    queue.append((neighbor, node, depth + 1))
            
            return -1
        
        min_girth = float('inf')
        for start in range(self.n):
            cycle_length = find_shortest_cycle(start)
            if cycle_length > 0:
                min_girth = min(min_girth, cycle_length)
        
        self.girth_cache = min_girth if min_girth != float('inf') else -1
        return self.girth_cache

# Example usage
dgg = DynamicGraphGirth(4)
dgg.add_edge(0, 1)
dgg.add_edge(1, 2)
dgg.add_edge(2, 3)
dgg.add_edge(3, 0)
result1 = dgg.get_girth()
print(f"Dynamic graph girth result: {result1}")
```

## Problem Variations

### **Variation 1: Graph Girth with Dynamic Updates**
**Problem**: Handle dynamic graph updates (add/remove/update edges) while maintaining graph girth calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic graph management with girth detection.

```python
from collections import defaultdict, deque
import heapq

class DynamicGraphGirth:
    def __init__(self, n=None, edges=None):
        self.n = n or 0
        self.edges = edges or []
        self.graph = defaultdict(list)
        self._update_girth_info()
    
    def _update_girth_info(self):
        """Update girth information."""
        self.girth = self._calculate_girth()
    
    def _calculate_girth(self):
        """Calculate the girth of the graph."""
        if self.n <= 0 or len(self.edges) == 0:
            return float('inf')
        
        min_cycle_length = float('inf')
        
        # Try BFS from each vertex to find shortest cycle
        for start in range(self.n):
            dist = [-1] * self.n
            parent = [-1] * self.n
            queue = deque([start])
            dist[start] = 0
            
            while queue:
                u = queue.popleft()
                
                for v in self.graph[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        queue.append(v)
                    elif parent[u] != v:  # Found a back edge
                        cycle_length = dist[u] + dist[v] + 1
                        min_cycle_length = min(min_cycle_length, cycle_length)
        
        return min_cycle_length if min_cycle_length != float('inf') else -1
    
    def update_graph(self, new_n, new_edges):
        """Update the graph with new vertices and edges."""
        self.n = new_n
        self.edges = new_edges
        self._build_graph()
        self._update_girth_info()
    
    def add_edge(self, u, v):
        """Add an edge to the graph."""
        if 0 <= u < self.n and 0 <= v < self.n:
            self.edges.append((u, v))
            self.graph[u].append(v)
            self.graph[v].append(u)
            self._update_girth_info()
    
    def remove_edge(self, u, v):
        """Remove an edge from the graph."""
        if (u, v) in self.edges:
            self.edges.remove((u, v))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_girth_info()
        elif (v, u) in self.edges:
            self.edges.remove((v, u))
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            self._update_girth_info()
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def is_cyclic(self):
        """Check if the graph is cyclic."""
        return self.girth != -1 and self.girth != float('inf')
    
    def get_girth(self):
        """Get the current girth of the graph."""
        return self.girth
    
    def get_girth_with_priorities(self, priorities):
        """Get girth considering vertex priorities."""
        if not self.is_cyclic():
            return -1
        
        # Calculate weighted girth based on priorities
        weighted_girth = 0
        for u, v in self.edges:
            edge_weight = priorities.get(u, 1) + priorities.get(v, 1)
            weighted_girth += edge_weight
        
        return weighted_girth
    
    def get_girth_with_constraints(self, constraint_func):
        """Get girth that satisfies custom constraints."""
        if not self.is_cyclic():
            return -1
        
        if constraint_func(self.n, self.edges, self.girth):
            return self.girth
        else:
            return -1
    
    def get_girth_in_range(self, min_girth, max_girth):
        """Get girth within specified range."""
        if not self.is_cyclic():
            return -1
        
        if min_girth <= self.girth <= max_girth:
            return self.girth
        else:
            return -1
    
    def get_girth_with_pattern(self, pattern_func):
        """Get girth matching specified pattern."""
        if not self.is_cyclic():
            return -1
        
        if pattern_func(self.n, self.edges, self.girth):
            return self.girth
        else:
            return -1
    
    def get_girth_statistics(self):
        """Get statistics about the graph girth."""
        return {
            'n': self.n,
            'edge_count': len(self.edges),
            'girth': self.girth,
            'is_cyclic': self.is_cyclic(),
            'has_cycles': self.girth != -1 and self.girth != float('inf')
        }
    
    def get_girth_patterns(self):
        """Get patterns in graph girth."""
        patterns = {
            'has_edges': 0,
            'has_valid_graph': 0,
            'optimal_girth_possible': 0,
            'has_large_graph': 0
        }
        
        # Check if has edges
        if len(self.edges) > 0:
            patterns['has_edges'] = 1
        
        # Check if has valid graph
        if self.n > 0:
            patterns['has_valid_graph'] = 1
        
        # Check if optimal girth is possible
        if self.is_cyclic():
            patterns['optimal_girth_possible'] = 1
        
        # Check if has large graph
        if self.n > 100:
            patterns['has_large_graph'] = 1
        
        return patterns
    
    def get_optimal_girth_strategy(self):
        """Get optimal strategy for girth management."""
        if not self.is_cyclic():
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'girth': -1
            }
        
        # Calculate efficiency rate
        efficiency_rate = 1.0 if self.girth > 0 else 0.0
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'bfs_girth_search'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_bfs'
        else:
            recommended_strategy = 'advanced_girth_detection'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'girth': self.girth
        }

# Example usage
n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
dynamic_girth = DynamicGraphGirth(n, edges)
print(f"Graph girth: {dynamic_girth.girth}")

# Update graph
dynamic_girth.update_graph(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 2)])
print(f"After updating graph: n={dynamic_girth.n}, girth={dynamic_girth.girth}")

# Add edge
dynamic_girth.add_edge(5, 1)
print(f"After adding edge (5,1): {dynamic_girth.edges}")

# Remove edge
dynamic_girth.remove_edge(5, 1)
print(f"After removing edge (5,1): {dynamic_girth.edges}")

# Check if cyclic
is_cyclic = dynamic_girth.is_cyclic()
print(f"Is cyclic: {is_cyclic}")

# Get girth
girth = dynamic_girth.get_girth()
print(f"Girth: {girth}")

# Get girth with priorities
priorities = {i: i for i in range(n)}
priority_girth = dynamic_girth.get_girth_with_priorities(priorities)
print(f"Girth with priorities: {priority_girth}")

# Get girth with constraints
def constraint_func(n, edges, girth):
    return girth > 0 and len(edges) > 0

print(f"Girth with constraints: {dynamic_girth.get_girth_with_constraints(constraint_func)}")

# Get girth in range
print(f"Girth in range 3-6: {dynamic_girth.get_girth_in_range(3, 6)}")

# Get girth with pattern
def pattern_func(n, edges, girth):
    return girth > 0 and len(edges) > 0

print(f"Girth with pattern: {dynamic_girth.get_girth_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_girth.get_girth_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_girth.get_girth_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_girth.get_optimal_girth_strategy()}")
```

### **Variation 2: Graph Girth with Different Operations**
**Problem**: Handle different types of girth operations (weighted girth, priority-based selection, advanced girth analysis).

**Approach**: Use advanced data structures for efficient different types of girth operations.

```python
class AdvancedGraphGirth:
    def __init__(self, n=None, edges=None, weights=None, priorities=None):
        self.n = n or 0
        self.edges = edges or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.graph = defaultdict(list)
        self._update_girth_info()
    
    def _update_girth_info(self):
        """Update girth information."""
        self.girth = self._calculate_girth()
    
    def _calculate_girth(self):
        """Calculate the girth of the graph."""
        if self.n <= 0 or len(self.edges) == 0:
            return float('inf')
        
        min_cycle_length = float('inf')
        
        # Try BFS from each vertex to find shortest cycle
        for start in range(self.n):
            dist = [-1] * self.n
            parent = [-1] * self.n
            queue = deque([start])
            dist[start] = 0
            
            while queue:
                u = queue.popleft()
                
                for v in self.graph[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        queue.append(v)
                    elif parent[u] != v:  # Found a back edge
                        cycle_length = dist[u] + dist[v] + 1
                        min_cycle_length = min(min_cycle_length, cycle_length)
        
        return min_cycle_length if min_cycle_length != float('inf') else -1
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def is_cyclic(self):
        """Check if the graph is cyclic."""
        return self.girth != -1 and self.girth != float('inf')
    
    def get_girth(self):
        """Get the current girth of the graph."""
        return self.girth
    
    def get_weighted_girth(self):
        """Get girth with weights and priorities applied."""
        if not self.is_cyclic():
            return -1
        
        # Calculate weighted girth based on edge weights and vertex priorities
        weighted_girth = 0
        for u, v in self.edges:
            edge_weight = self.weights.get((u, v), 1)
            vertex_priority = self.priorities.get(u, 1) + self.priorities.get(v, 1)
            weighted_girth += edge_weight * vertex_priority
        
        return weighted_girth
    
    def get_girth_with_priority(self, priority_func):
        """Get girth considering priority."""
        if not self.is_cyclic():
            return -1
        
        # Calculate priority-based girth
        priority = priority_func(self.n, self.edges, self.weights, self.priorities, self.girth)
        return priority
    
    def get_girth_with_optimization(self, optimization_func):
        """Get girth using custom optimization function."""
        if not self.is_cyclic():
            return -1
        
        # Calculate optimization-based girth
        score = optimization_func(self.n, self.edges, self.weights, self.priorities, self.girth)
        return score
    
    def get_girth_with_constraints(self, constraint_func):
        """Get girth that satisfies custom constraints."""
        if not self.is_cyclic():
            return -1
        
        if constraint_func(self.n, self.edges, self.weights, self.priorities, self.girth):
            return self.get_weighted_girth()
        else:
            return -1
    
    def get_girth_with_multiple_criteria(self, criteria_list):
        """Get girth that satisfies multiple criteria."""
        if not self.is_cyclic():
            return -1
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.edges, self.weights, self.priorities, self.girth):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_girth()
        else:
            return -1
    
    def get_girth_with_alternatives(self, alternatives):
        """Get girth considering alternative weights/priorities."""
        result = []
        
        # Check original girth
        original_girth = self.get_weighted_girth()
        result.append((original_girth, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedGraphGirth(self.n, self.edges, alt_weights, alt_priorities)
            temp_girth = temp_instance.get_weighted_girth()
            result.append((temp_girth, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_girth_with_adaptive_criteria(self, adaptive_func):
        """Get girth using adaptive criteria."""
        if not self.is_cyclic():
            return -1
        
        if adaptive_func(self.n, self.edges, self.weights, self.priorities, self.girth, []):
            return self.get_weighted_girth()
        else:
            return -1
    
    def get_girth_optimization(self):
        """Get optimal girth configuration."""
        strategies = [
            ('weighted_girth', lambda: self.get_weighted_girth()),
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
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
weights = {(u, v): (u + v) * 2 for u, v in edges}  # Weight based on vertex sum
priorities = {i: i for i in range(n)}  # Priority based on vertex number
advanced_girth = AdvancedGraphGirth(n, edges, weights, priorities)

print(f"Weighted girth: {advanced_girth.get_weighted_girth()}")

# Get girth with priority
def priority_func(n, edges, weights, priorities, girth):
    return sum(priorities.values()) + girth

print(f"Girth with priority: {advanced_girth.get_girth_with_priority(priority_func)}")

# Get girth with optimization
def optimization_func(n, edges, weights, priorities, girth):
    return sum(weights.values()) + girth

print(f"Girth with optimization: {advanced_girth.get_girth_with_optimization(optimization_func)}")

# Get girth with constraints
def constraint_func(n, edges, weights, priorities, girth):
    return girth > 0 and len(edges) > 0

print(f"Girth with constraints: {advanced_girth.get_girth_with_constraints(constraint_func)}")

# Get girth with multiple criteria
def criterion1(n, edges, weights, priorities, girth):
    return len(edges) > 0

def criterion2(n, edges, weights, priorities, girth):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Girth with multiple criteria: {advanced_girth.get_girth_with_multiple_criteria(criteria_list)}")

# Get girth with alternatives
alternatives = [({(u, v): 1 for u, v in edges}, {i: 1 for i in range(n)}), ({(u, v): (u + v)*3 for u, v in edges}, {i: 2 for i in range(n)})]
print(f"Girth with alternatives: {advanced_girth.get_girth_with_alternatives(alternatives)}")

# Get girth with adaptive criteria
def adaptive_func(n, edges, weights, priorities, girth, current_result):
    return len(edges) > 0 and len(current_result) < 10

print(f"Girth with adaptive criteria: {advanced_girth.get_girth_with_adaptive_criteria(adaptive_func)}")

# Get girth optimization
print(f"Girth optimization: {advanced_girth.get_girth_optimization()}")
```

### **Variation 3: Graph Girth with Constraints**
**Problem**: Handle girth calculation with additional constraints (length limits, girth constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedGraphGirth:
    def __init__(self, n=None, edges=None, constraints=None):
        self.n = n or 0
        self.edges = edges or []
        self.constraints = constraints or {}
        self.graph = defaultdict(list)
        self._update_girth_info()
    
    def _update_girth_info(self):
        """Update girth information."""
        self.girth = self._calculate_girth()
    
    def _calculate_girth(self):
        """Calculate the girth of the graph."""
        if self.n <= 0 or len(self.edges) == 0:
            return float('inf')
        
        min_cycle_length = float('inf')
        
        # Try BFS from each vertex to find shortest cycle
        for start in range(self.n):
            dist = [-1] * self.n
            parent = [-1] * self.n
            queue = deque([start])
            dist[start] = 0
            
            while queue:
                u = queue.popleft()
                
                for v in self.graph[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        queue.append(v)
                    elif parent[u] != v:  # Found a back edge
                        cycle_length = dist[u] + dist[v] + 1
                        min_cycle_length = min(min_cycle_length, cycle_length)
        
        return min_cycle_length if min_cycle_length != float('inf') else -1
    
    def _is_valid_edge(self, u, v):
        """Check if edge is valid considering constraints."""
        # Edge constraints
        if 'allowed_edges' in self.constraints:
            if (u, v) not in self.constraints['allowed_edges'] and (v, u) not in self.constraints['allowed_edges']:
                return False
        
        if 'forbidden_edges' in self.constraints:
            if (u, v) in self.constraints['forbidden_edges'] or (v, u) in self.constraints['forbidden_edges']:
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
                if not constraint(u, v, self.n, self.edges, self.girth):
                    return False
        
        return True
    
    def _build_graph(self):
        """Build the graph from edges."""
        self.graph = defaultdict(list)
        
        for u, v in self.edges:
            if self._is_valid_edge(u, v):
                self.graph[u].append(v)
                self.graph[v].append(u)
    
    def is_cyclic(self):
        """Check if the graph is cyclic."""
        return self.girth != -1 and self.girth != float('inf')
    
    def get_girth(self):
        """Get the current girth of the graph."""
        return self.girth
    
    def get_girth_with_length_constraints(self, min_girth, max_girth):
        """Get girth considering length constraints."""
        if not self.is_cyclic():
            return -1
        
        if min_girth <= self.girth <= max_girth:
            return self.girth
        else:
            return -1
    
    def get_girth_with_girth_constraints(self, girth_constraints):
        """Get girth considering girth constraints."""
        if not self.is_cyclic():
            return -1
        
        satisfies_constraints = True
        for constraint in girth_constraints:
            if not constraint(self.n, self.edges, self.girth):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.girth
        else:
            return -1
    
    def get_girth_with_pattern_constraints(self, pattern_constraints):
        """Get girth considering pattern constraints."""
        if not self.is_cyclic():
            return -1
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n, self.edges, self.girth):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.girth
        else:
            return -1
    
    def get_girth_with_mathematical_constraints(self, constraint_func):
        """Get girth that satisfies custom mathematical constraints."""
        if not self.is_cyclic():
            return -1
        
        if constraint_func(self.n, self.edges, self.girth):
            return self.girth
        else:
            return -1
    
    def get_girth_with_optimization_constraints(self, optimization_func):
        """Get girth using custom optimization constraints."""
        if not self.is_cyclic():
            return -1
        
        # Calculate optimization score for girth
        score = optimization_func(self.n, self.edges, self.girth)
        
        if score > 0:
            return self.girth
        else:
            return -1
    
    def get_girth_with_multiple_constraints(self, constraints_list):
        """Get girth that satisfies multiple constraints."""
        if not self.is_cyclic():
            return -1
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n, self.edges, self.girth):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.girth
        else:
            return -1
    
    def get_girth_with_priority_constraints(self, priority_func):
        """Get girth with priority-based constraints."""
        if not self.is_cyclic():
            return -1
        
        # Calculate priority for girth
        priority = priority_func(self.n, self.edges, self.girth)
        
        if priority > 0:
            return self.girth
        else:
            return -1
    
    def get_girth_with_adaptive_constraints(self, adaptive_func):
        """Get girth with adaptive constraints."""
        if not self.is_cyclic():
            return -1
        
        if adaptive_func(self.n, self.edges, self.girth, []):
            return self.girth
        else:
            return -1
    
    def get_optimal_girth_strategy(self):
        """Get optimal girth strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_girth_with_length_constraints),
            ('girth_constraints', self.get_girth_with_girth_constraints),
            ('pattern_constraints', self.get_girth_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    result = strategy_func(1, 1000)
                elif strategy_name == 'girth_constraints':
                    girth_constraints = [lambda n, edges, girth: len(edges) > 0]
                    result = strategy_func(girth_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n, edges, girth: len(edges) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and result > best_score:
                    best_score = result
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_edges': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)],
    'forbidden_edges': [(0, 3), (1, 4)],
    'max_vertex': 10,
    'min_vertex': 0,
    'pattern_constraints': [lambda u, v, n, edges, girth: u >= 0 and v >= 0 and u < n and v < n]
}

n = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
constrained_girth = ConstrainedGraphGirth(n, edges, constraints)

print("Length-constrained girth:", constrained_girth.get_girth_with_length_constraints(3, 6))

print("Girth-constrained girth:", constrained_girth.get_girth_with_girth_constraints([lambda n, edges, girth: len(edges) > 0]))

print("Pattern-constrained girth:", constrained_girth.get_girth_with_pattern_constraints([lambda n, edges, girth: len(edges) > 0]))

# Mathematical constraints
def custom_constraint(n, edges, girth):
    return girth > 0 and len(edges) > 0

print("Mathematical constraint girth:", constrained_girth.get_girth_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n, edges, girth):
    return 1 <= girth <= 20

range_constraints = [range_constraint]
print("Range-constrained girth:", constrained_girth.get_girth_with_length_constraints(1, 20))

# Multiple constraints
def constraint1(n, edges, girth):
    return len(edges) > 0

def constraint2(n, edges, girth):
    return girth > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints girth:", constrained_girth.get_girth_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n, edges, girth):
    return n + len(edges) + girth

print("Priority-constrained girth:", constrained_girth.get_girth_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, edges, girth, current_result):
    return len(edges) > 0 and len(current_result) < 10

print("Adaptive constraint girth:", constrained_girth.get_girth_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_girth.get_optimal_girth_strategy()
print(f"Optimal girth strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Round Trip](https://cses.fi/problemset/task/1669) - Cycle detection
- [Fixed Length Path Queries](https://cses.fi/problemset/task/2417) - Similar approach
- [Graph Girth](https://cses.fi/problemset/task/1707) - Cycle properties

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Cycle detection
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Topological sort
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Cycle detection

#### **Problem Categories**
- **Graph Theory**: Cycle detection, girth computation
- **Shortest Path**: All-pairs shortest path, BFS
- **Combinatorial Optimization**: Cycle finding, graph traversal

## 🔗 Additional Resources

### **Algorithm References**
- [Floyd-Warshall Algorithm](https://cp-algorithms.com/graph/all-pair-shortest-path-floyd-warshall.html) - All-pairs shortest path
- [BFS](https://cp-algorithms.com/graph/breadth-first-search.html) - Breadth-first search
- [Cycle Detection](https://cp-algorithms.com/graph/finding-cycle.html) - Cycle detection algorithms

### **Practice Problems**
- [CSES Round Trip](https://cses.fi/problemset/task/1669) - Medium
- [CSES Graph Girth](https://cses.fi/problemset/task/1707) - Medium
- [CSES Hamiltonian Flights](https://cses.fi/problemset/task/1690) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
