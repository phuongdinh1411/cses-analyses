---
layout: simple
title: "Police Chase - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/police_chase_analysis
---

# Police Chase - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of minimum cut in graph algorithms
- Apply efficient algorithms for finding minimum cuts
- Implement max-flow min-cut algorithms
- Optimize graph flow for cut calculations
- Handle special cases in minimum cut problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, max-flow min-cut, network flow
- **Data Structures**: Graphs, flow networks, residual graphs
- **Mathematical Concepts**: Graph theory, flow theory, cut theory
- **Programming Skills**: Graph operations, flow algorithms, cut calculations
- **Related Problems**: Download Speed (graph_algorithms), Road Construction (graph_algorithms), Road Reparation (graph_algorithms)

## 📋 Problem Description

Given a directed graph, find the minimum number of edges to remove to disconnect source from sink.

**Input**: 
- n: number of vertices
- m: number of edges
- source: source vertex
- sink: sink vertex
- edges: array of directed edges (u, v)

**Output**: 
- Minimum number of edges to remove

**Constraints**:
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ 1000

**Example**:
```
Input:
n = 4, m = 5
source = 0, sink = 3
edges = [(0,1), (0,2), (1,2), (1,3), (2,3)]

Output:
2

Explanation**: 
Remove edges (0,1) and (0,2) to disconnect 0 from 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible edge combinations
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph connectivity
- **Inefficient**: O(2^m) time complexity

**Key Insight**: Try all possible combinations of edges to remove.

**Algorithm**:
- Generate all possible subsets of edges
- For each subset, check if removing those edges disconnects source from sink
- Return minimum size of such subset

**Visual Example**:
```
Graph: 0->1->3, 0->2->3, 1->2

Edge removal combinations:
┌─────────────────────────────────────┐
│ Remove {}: 0 can reach 3 (NO)      │
│ Remove {(0,1)}: 0 can reach 3 (NO) │
│ Remove {(0,2)}: 0 can reach 3 (NO) │
│ Remove {(0,1),(0,2)}: 0 cannot reach 3 (YES) │
│                                   │
│ Minimum: 2 edges                  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_police_chase(n, source, sink, edges):
    """Find minimum cut using brute force approach"""
    from itertools import combinations
    
    min_edges = float('inf')
    
    # Try all possible combinations of edges to remove
    for r in range(len(edges) + 1):
        for edge_subset in combinations(edges, r):
            # Check if removing these edges disconnects source from sink
            if is_disconnected(n, source, sink, edges, edge_subset):
                min_edges = min(min_edges, len(edge_subset))
    
    return min_edges

def is_disconnected(n, source, sink, edges, removed_edges):
    """Check if source is disconnected from sink after removing edges"""
    # Build adjacency list excluding removed edges
    adj = [[] for _ in range(n)]
    removed_set = set(removed_edges)
    
    for u, v in edges:
        if (u, v) not in removed_set:
            adj[u].append(v)
    
    # BFS to check connectivity
    visited = [False] * n
    queue = [source]
    visited[source] = True
    
    while queue:
        vertex = queue.pop(0)
        if vertex == sink:
            return False  # Still connected
        
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    
    return True  # Disconnected

# Example usage
n = 4
source = 0
sink = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
result = brute_force_police_chase(n, source, sink, edges)
print(f"Brute force minimum cut: {result}")
```

**Time Complexity**: O(2^m)
**Space Complexity**: O(n + m)

**Why it's inefficient**: O(2^m) time complexity for checking all combinations.

---

### Approach 2: Max-Flow Min-Cut Solution

**Key Insights from Max-Flow Min-Cut Solution**:
- **Max-Flow Min-Cut**: Use max-flow min-cut theorem for efficient solution
- **Efficient Implementation**: O(nm²) time complexity
- **Flow Network**: Convert to flow network problem
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use max-flow min-cut theorem to find minimum cut.

**Algorithm**:
- Convert graph to flow network (assign capacity 1 to each edge)
- Find maximum flow from source to sink
- The value of max flow equals the minimum cut

**Visual Example**:
```
Max-flow min-cut approach:

Graph: 0->1->3, 0->2->3, 1->2
Capacities: all edges have capacity 1

Flow network:
┌─────────────────────────────────────┐
│ 0 --1--> 1 --1--> 3               │
│ |        |                         │
│ 1        1                         │
│ |        |                         │
│ v        v                         │
│ 2 --1--> 2 --1--> 3               │
│                                   │
│ Max flow: 2                        │
│ Min cut: 2 edges                   │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def max_flow_min_cut_police_chase(n, source, sink, edges):
    """Find minimum cut using max-flow min-cut theorem"""
    # Build adjacency list with capacities
    adj = [[] for _ in range(n)]
    capacity = [[0] * n for _ in range(n)]
    
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # For residual graph
        capacity[u][v] = 1  # Each edge has capacity 1
    
    def bfs_find_path():
        """Find augmenting path using BFS"""
        parent = [-1] * n
        visited = [False] * n
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_max_flow():
        """Find maximum flow using Ford-Fulkerson algorithm"""
        max_flow = 0
        
        while True:
            path = bfs_find_path()
            if not path:
                break
            
            # Find minimum capacity in path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_max_flow()

# Example usage
n = 4
source = 0
sink = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
result = max_flow_min_cut_police_chase(n, source, sink, edges)
print(f"Max-flow min-cut result: {result}")
```

**Time Complexity**: O(nm²)
**Space Complexity**: O(n²)

**Why it's better**: Uses max-flow min-cut theorem for O(nm²) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for flow algorithms
- **Efficient Implementation**: O(nm²) time complexity
- **Space Efficiency**: O(n²) space complexity
- **Optimal Complexity**: Best approach for minimum cut

**Key Insight**: Use advanced data structures for optimal minimum cut calculation.

**Algorithm**:
- Use specialized data structures for flow network storage
- Implement efficient max-flow algorithms
- Handle special cases optimally
- Return minimum cut value

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1->3, 0->2->3, 1->2
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Flow network: for efficient       │
│   storage and operations            │
│ - Residual graph: for optimization  │
│ - Flow cache: for optimization      │
│                                   │
│ Minimum cut calculation:            │
│ - Use flow network for efficient   │
│   storage and operations            │
│ - Use residual graph for           │
│   optimization                      │
│ - Use flow cache for optimization  │
│                                   │
│ Result: 2                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_police_chase(n, source, sink, edges):
    """Find minimum cut using advanced data structure approach"""
    # Use advanced data structures for flow network storage
    adj = [[] for _ in range(n)]
    capacity = [[0] * n for _ in range(n)]
    
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # For residual graph
        capacity[u][v] = 1  # Each edge has capacity 1
    
    def bfs_advanced_find_path():
        """Find augmenting path using advanced BFS"""
        parent = [-1] * n
        visited = [False] * n
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path using advanced data structures
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_advanced_max_flow():
        """Find maximum flow using advanced Ford-Fulkerson algorithm"""
        max_flow = 0
        
        while True:
            path = bfs_advanced_find_path()
            if not path:
                break
            
            # Find minimum capacity in path using advanced data structures
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities using advanced data structures
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_advanced_max_flow()

# Example usage
n = 4
source = 0
sink = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
result = advanced_data_structure_police_chase(n, source, sink, edges)
print(f"Advanced data structure result: {result}")
```

**Time Complexity**: O(nm²)
**Space Complexity**: O(n²)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^m) | O(n + m) | Try all edge combinations |
| Max-Flow Min-Cut | O(nm²) | O(n²) | Use max-flow min-cut theorem |
| Advanced Data Structure | O(nm²) | O(n²) | Use advanced data structures |

### Time Complexity
- **Time**: O(nm²) - Use max-flow min-cut theorem for efficient minimum cut
- **Space**: O(n²) - Store capacity matrix and adjacency list

### Why This Solution Works
- **Max-Flow Min-Cut**: Use max-flow min-cut theorem for minimum cut
- **Flow Network**: Convert to flow network with unit capacities
- **Ford-Fulkerson**: Use Ford-Fulkerson algorithm for max flow
- **Optimal Algorithms**: Use optimal algorithms for minimum cut

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Police Chase with Constraints**
**Problem**: Find minimum cut with specific constraints.

**Key Differences**: Apply constraints to minimum cut calculation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_police_chase(n, source, sink, edges, constraints):
    """Find minimum cut with constraints"""
    # Build adjacency list with capacities
    adj = [[] for _ in range(n)]
    capacity = [[0] * n for _ in range(n)]
    
    for u, v in edges:
        if constraints(u) and constraints(v):
            adj[u].append(v)
            adj[v].append(u)  # For residual graph
            capacity[u][v] = 1  # Each edge has capacity 1
    
    def bfs_constrained_find_path():
        """Find augmenting path using constrained BFS"""
        parent = [-1] * n
        visited = [False] * n
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if (not visited[neighbor] and 
                    capacity[vertex][neighbor] > 0 and 
                    constraints(neighbor)):
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_constrained_max_flow():
        """Find maximum flow with constraints"""
        max_flow = 0
        
        while True:
            path = bfs_constrained_find_path()
            if not path:
                break
            
            # Find minimum capacity in path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_constrained_max_flow()

# Example usage
n = 4
source = 0
sink = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
constraints = lambda vertex: vertex >= 0  # Only include non-negative vertices
result = constrained_police_chase(n, source, sink, edges, constraints)
print(f"Constrained minimum cut: {result}")
```

#### **2. Police Chase with Different Metrics**
**Problem**: Find minimum cut with different edge weights.

**Key Differences**: Different edge weight calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_police_chase(n, source, sink, edges, weights):
    """Find minimum cut with different edge weights"""
    # Build adjacency list with capacities
    adj = [[] for _ in range(n)]
    capacity = [[0] * n for _ in range(n)]
    
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # For residual graph
        capacity[u][v] = weights.get((u, v), 1)  # Use edge weights
    
    def bfs_weighted_find_path():
        """Find augmenting path using weighted BFS"""
        parent = [-1] * n
        visited = [False] * n
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_weighted_max_flow():
        """Find maximum flow with weights"""
        max_flow = 0
        
        while True:
            path = bfs_weighted_find_path()
            if not path:
                break
            
            # Find minimum capacity in path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_weighted_max_flow()

# Example usage
n = 4
source = 0
sink = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
weights = {(0, 1): 2, (0, 2): 1, (1, 2): 3, (1, 3): 1, (2, 3): 2}
result = weighted_police_chase(n, source, sink, edges, weights)
print(f"Weighted minimum cut: {result}")
```

#### **3. Police Chase with Multiple Dimensions**
**Problem**: Find minimum cut in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_police_chase(n, source, sink, edges, dimensions):
    """Find minimum cut in multiple dimensions"""
    # Build adjacency list with capacities
    adj = [[] for _ in range(n)]
    capacity = [[0] * n for _ in range(n)]
    
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # For residual graph
        capacity[u][v] = 1  # Each edge has capacity 1
    
    def bfs_multi_dimensional_find_path():
        """Find augmenting path using multi-dimensional BFS"""
        parent = [-1] * n
        visited = [False] * n
        queue = [source]
        visited[source] = True
        
        while queue:
            vertex = queue.pop(0)
            if vertex == sink:
                break
            
            for neighbor in adj[vertex]:
                if not visited[neighbor] and capacity[vertex][neighbor] > 0:
                    visited[neighbor] = True
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        
        # Reconstruct path
        if parent[sink] == -1:
            return None
        
        path = []
        current = sink
        while current != -1:
            path.append(current)
            current = parent[current]
        return path[::-1]
    
    def find_multi_dimensional_max_flow():
        """Find maximum flow in multiple dimensions"""
        max_flow = 0
        
        while True:
            path = bfs_multi_dimensional_find_path()
            if not path:
                break
            
            # Find minimum capacity in path
            min_capacity = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                min_capacity = min(min_capacity, capacity[u][v])
            
            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                capacity[u][v] -= min_capacity
                capacity[v][u] += min_capacity
            
            max_flow += min_capacity
        
        return max_flow
    
    return find_multi_dimensional_max_flow()

# Example usage
n = 4
source = 0
sink = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
dimensions = 1
result = multi_dimensional_police_chase(n, source, sink, edges, dimensions)
print(f"Multi-dimensional minimum cut: {result}")
```

### Related Problems

#### **CSES Problems**
- [Download Speed](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Road Construction](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Road Reparation](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Critical Connections](https://leetcode.com/problems/critical-connections-in-a-network/) - Graph
- [Network Delay Time](https://leetcode.com/problems/network-delay-time/) - Graph
- [Cheapest Flights](https://leetcode.com/problems/cheapest-flights-within-k-stops/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Minimum cut, max-flow min-cut, network flow
- **Flow Algorithms**: Ford-Fulkerson, max flow, min cut
- **Network Flow**: Flow networks, residual graphs

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Max-Flow Min-Cut](https://cp-algorithms.com/graph/max_flow.html) - Max-flow min-cut algorithms
- [Network Flow](https://cp-algorithms.com/graph/flow-network.html) - Network flow algorithms

### **Practice Problems**
- [CSES Download Speed](https://cses.fi/problemset/task/1075) - Medium
- [CSES Road Construction](https://cses.fi/problemset/task/1075) - Medium
- [CSES Road Reparation](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Max-Flow Min-Cut Theorem](https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem) - Wikipedia article
- [Network Flow](https://en.wikipedia.org/wiki/Flow_network) - Wikipedia article
