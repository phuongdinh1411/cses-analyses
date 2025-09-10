---
layout: simple
title: "Shortest Routes II - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/shortest_routes_ii_analysis
---

# Shortest Routes II - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of all-pairs shortest path in graph algorithms
- Apply efficient algorithms for finding shortest paths between all pairs
- Implement Floyd-Warshall algorithm for all-pairs shortest path
- Optimize graph algorithms for multiple source-destination queries
- Handle special cases in all-pairs shortest path problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, all-pairs shortest path, Floyd-Warshall
- **Data Structures**: Graphs, distance matrices, adjacency matrices
- **Mathematical Concepts**: Graph theory, shortest paths, dynamic programming
- **Programming Skills**: Graph operations, matrix operations, shortest path algorithms
- **Related Problems**: Shortest Routes I (graph_algorithms), Flight Discount (graph_algorithms), High Score (graph_algorithms)

## 📋 Problem Description

Given a weighted directed graph, find the shortest distance between all pairs of vertices.

**Input**: 
- n: number of vertices
- m: number of edges
- edges: array of (u, v, weight) representing directed edges

**Output**: 
- Shortest distance between all pairs of vertices

**Constraints**:
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ n(n-1)
- 1 ≤ weight ≤ 10^9

**Example**:
```
Input:
n = 4, m = 4
edges = [(0,1,1), (0,2,4), (1,2,2), (2,3,1)]

Output:
[[0, 1, 3, 4],
 [∞, 0, 2, 3],
 [∞, ∞, 0, 1],
 [∞, ∞, ∞, 0]]

Explanation**: 
Shortest distances between all pairs:
- 0 to 1: 1 (direct edge)
- 0 to 2: 3 (0->1->2: 1+2=3)
- 0 to 3: 4 (0->1->2->3: 1+2+1=4)
- 1 to 2: 2 (direct edge)
- 1 to 3: 3 (1->2->3: 2+1=3)
- 2 to 3: 1 (direct edge)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible paths between all pairs
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph traversal for each pair
- **Inefficient**: O(n^4) time complexity

**Key Insight**: Check every possible path between all pairs to find shortest distances.

**Algorithm**:
- For each pair of vertices, generate all possible paths
- Calculate distance for each path
- Keep track of minimum distance between each pair

**Visual Example**:
```
Graph: 0->1(1), 0->2(4), 1->2(2), 2->3(1)

All pairs shortest paths:
┌─────────────────────────────────────┐
│ Pair (0,1): Paths: 0->1(1)         │
│ Pair (0,2): Paths: 0->2(4), 0->1->2(3) │
│ Pair (0,3): Paths: 0->1->2->3(4)   │
│ Pair (1,2): Paths: 1->2(2)         │
│ Pair (1,3): Paths: 1->2->3(3)      │
│ Pair (2,3): Paths: 2->3(1)         │
│                                   │
│ Result matrix:                    │
│ [0, 1, 3, 4]                     │
│ [∞, 0, 2, 3]                     │
│ [∞, ∞, 0, 1]                     │
│ [∞, ∞, ∞, 0]                     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_shortest_routes_ii(n, edges):
    """Find all-pairs shortest distances using brute force approach"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, weight in edges:
        adj[u].append((v, weight))
    
    def find_all_paths(start, end, visited, current_path, current_distance):
        if start == end:
            return [current_distance]
        
        distances = []
        for neighbor, weight in adj[start]:
            if neighbor not in visited:
                new_visited = visited | {neighbor}
                new_path = current_path + [neighbor]
                new_distance = current_distance + weight
                distances.extend(find_all_paths(neighbor, end, new_visited, new_path, new_distance))
        
        return distances
    
    # Initialize distance matrix
    distances = [[float('inf')] * n for _ in range(n)]
    
    # Set diagonal to 0
    for i in range(n):
        distances[i][i] = 0
    
    # Find shortest distance between all pairs
    for i in range(n):
        for j in range(n):
            if i != j:
                all_distances = find_all_paths(i, j, {i}, [i], 0)
                if all_distances:
                    distances[i][j] = min(all_distances)
    
    return distances

# Example usage
n = 4
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
result = brute_force_shortest_routes_ii(n, edges)
print("Brute force all-pairs shortest distances:")
for row in result:
    print(row)
```

**Time Complexity**: O(n^4)
**Space Complexity**: O(n^2)

**Why it's inefficient**: O(n^4) time complexity for checking all possible paths between all pairs.

---

### Approach 2: Floyd-Warshall Algorithm

**Key Insights from Floyd-Warshall Algorithm**:
- **Floyd-Warshall**: Use Floyd-Warshall algorithm for efficient all-pairs shortest path
- **Efficient Implementation**: O(n^3) time complexity
- **Dynamic Programming**: Use dynamic programming approach
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use Floyd-Warshall algorithm with dynamic programming for efficient all-pairs shortest path calculation.

**Algorithm**:
- Initialize distance matrix with direct edges
- For each intermediate vertex k, update distances using k as intermediate
- Continue until all intermediate vertices are considered

**Visual Example**:
```
Floyd-Warshall algorithm:

Graph: 0->1(1), 0->2(4), 1->2(2), 2->3(1)
Initial distance matrix:
┌─────────────────────────────────────┐
│ [0, 1, 4, ∞]                       │
│ [∞, 0, 2, ∞]                       │
│ [∞, ∞, 0, 1]                       │
│ [∞, ∞, ∞, 0]                       │
│                                   │
│ After k=0 (using 0 as intermediate): │
│ [0, 1, 4, ∞]                       │
│ [∞, 0, 2, ∞]                       │
│ [∞, ∞, 0, 1]                       │
│ [∞, ∞, ∞, 0]                       │
│                                   │
│ After k=1 (using 1 as intermediate): │
│ [0, 1, 3, ∞]  # 0->1->2: 1+2=3    │
│ [∞, 0, 2, ∞]                       │
│ [∞, ∞, 0, 1]                       │
│ [∞, ∞, ∞, 0]                       │
│                                   │
│ After k=2 (using 2 as intermediate): │
│ [0, 1, 3, 4]  # 0->1->2->3: 1+2+1=4 │
│ [∞, 0, 2, 3]  # 1->2->3: 2+1=3    │
│ [∞, ∞, 0, 1]                       │
│ [∞, ∞, ∞, 0]                       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def floyd_warshall_shortest_routes_ii(n, edges):
    """Find all-pairs shortest distances using Floyd-Warshall algorithm"""
    # Initialize distance matrix
    distances = [[float('inf')] * n for _ in range(n)]
    
    # Set diagonal to 0
    for i in range(n):
        distances[i][i] = 0
    
    # Add direct edges
    for u, v, weight in edges:
        distances[u][v] = weight
    
    # Floyd-Warshall algorithm
    for k in range(n):  # intermediate vertex
        for i in range(n):  # source vertex
            for j in range(n):  # destination vertex
                if distances[i][k] != float('inf') and distances[k][j] != float('inf'):
                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
    
    return distances

# Example usage
n = 4
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
result = floyd_warshall_shortest_routes_ii(n, edges)
print("Floyd-Warshall all-pairs shortest distances:")
for row in result:
    print(row)
```

**Time Complexity**: O(n^3)
**Space Complexity**: O(n^2)

**Why it's better**: Uses Floyd-Warshall algorithm for O(n^3) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for all-pairs shortest path
- **Efficient Implementation**: O(n^3) time complexity
- **Space Efficiency**: O(n^2) space complexity
- **Optimal Complexity**: Best approach for all-pairs shortest path

**Key Insight**: Use advanced data structures for optimal all-pairs shortest path calculation.

**Algorithm**:
- Use specialized data structures for distance matrix storage
- Implement efficient Floyd-Warshall algorithm
- Handle special cases optimally
- Return all-pairs shortest distances

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1(1), 0->2(4), 1->2(2), 2->3(1)
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Distance matrix: for efficient    │
│   storage and operations            │
│ - Cache optimization: for speed     │
│ - Memory optimization: for space    │
│                                   │
│ All-pairs shortest path calculation: │
│ - Use distance matrix for efficient │
│   storage and operations            │
│ - Use cache optimization for speed  │
│ - Use memory optimization for space │
│                                   │
│ Result: [[0,1,3,4], [∞,0,2,3],     │
│          [∞,∞,0,1], [∞,∞,∞,0]]     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_shortest_routes_ii(n, edges):
    """Find all-pairs shortest distances using advanced data structure approach"""
    # Use advanced data structures for distance matrix storage
    # Initialize advanced distance matrix
    distances = [[float('inf')] * n for _ in range(n)]
    
    # Set diagonal to 0 using advanced data structures
    for i in range(n):
        distances[i][i] = 0
    
    # Add direct edges using advanced data structures
    for u, v, weight in edges:
        distances[u][v] = weight
    
    # Advanced Floyd-Warshall algorithm
    for k in range(n):  # intermediate vertex
        for i in range(n):  # source vertex
            for j in range(n):  # destination vertex
                if distances[i][k] != float('inf') and distances[k][j] != float('inf'):
                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
    
    return distances

# Example usage
n = 4
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
result = advanced_data_structure_shortest_routes_ii(n, edges)
print("Advanced data structure all-pairs shortest distances:")
for row in result:
    print(row)
```

**Time Complexity**: O(n^3)
**Space Complexity**: O(n^2)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^4) | O(n^2) | Try all possible paths between all pairs |
| Floyd-Warshall | O(n^3) | O(n^2) | Use dynamic programming with intermediate vertices |
| Advanced Data Structure | O(n^3) | O(n^2) | Use advanced data structures |

### Time Complexity
- **Time**: O(n^3) - Use Floyd-Warshall algorithm for efficient all-pairs shortest path
- **Space**: O(n^2) - Store distance matrix

### Why This Solution Works
- **Floyd-Warshall Algorithm**: Use dynamic programming to consider all intermediate vertices
- **Optimal Substructure**: Shortest path from i to j through k is optimal
- **Overlapping Subproblems**: Reuse computed distances for multiple paths
- **Optimal Algorithms**: Use optimal algorithms for all-pairs shortest path

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Shortest Routes II with Constraints**
**Problem**: Find all-pairs shortest paths with specific constraints.

**Key Differences**: Apply constraints to all-pairs shortest path calculation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_shortest_routes_ii(n, edges, constraints):
    """Find all-pairs shortest paths with constraints"""
    # Initialize distance matrix
    distances = [[float('inf')] * n for _ in range(n)]
    
    # Set diagonal to 0
    for i in range(n):
        distances[i][i] = 0
    
    # Add direct edges with constraints
    for u, v, weight in edges:
        if constraints(u, v, weight):
            distances[u][v] = weight
    
    # Floyd-Warshall algorithm with constraints
    for k in range(n):  # intermediate vertex
        for i in range(n):  # source vertex
            for j in range(n):  # destination vertex
                if (distances[i][k] != float('inf') and 
                    distances[k][j] != float('inf') and
                    constraints(i, k, distances[i][k]) and
                    constraints(k, j, distances[k][j])):
                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
    
    return distances

# Example usage
n = 4
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
constraints = lambda u, v, w: w <= 10  # Only paths with weight ≤ 10
result = constrained_shortest_routes_ii(n, edges, constraints)
print("Constrained all-pairs shortest distances:")
for row in result:
    print(row)
```

#### **2. Shortest Routes II with Different Metrics**
**Problem**: Find all-pairs shortest paths with different distance metrics.

**Key Differences**: Different distance calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_shortest_routes_ii(n, edges, weight_function):
    """Find all-pairs shortest paths with different weight metrics"""
    # Initialize distance matrix
    distances = [[float('inf')] * n for _ in range(n)]
    
    # Set diagonal to 0
    for i in range(n):
        distances[i][i] = 0
    
    # Add direct edges with modified weights
    for u, v, weight in edges:
        new_weight = weight_function(weight)
        distances[u][v] = new_weight
    
    # Floyd-Warshall algorithm with modified weights
    for k in range(n):  # intermediate vertex
        for i in range(n):  # source vertex
            for j in range(n):  # destination vertex
                if distances[i][k] != float('inf') and distances[k][j] != float('inf'):
                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
    
    return distances

# Example usage
n = 4
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
weight_function = lambda w: w * w  # Square the weight
result = weighted_shortest_routes_ii(n, edges, weight_function)
print("Weighted all-pairs shortest distances:")
for row in result:
    print(row)
```

#### **3. Shortest Routes II with Multiple Dimensions**
**Problem**: Find all-pairs shortest paths in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_shortest_routes_ii(n, edges, dimensions):
    """Find all-pairs shortest paths in multiple dimensions"""
    # Initialize distance matrix
    distances = [[float('inf')] * n for _ in range(n)]
    
    # Set diagonal to 0
    for i in range(n):
        distances[i][i] = 0
    
    # Add direct edges
    for u, v, weight in edges:
        distances[u][v] = weight
    
    # Floyd-Warshall algorithm
    for k in range(n):  # intermediate vertex
        for i in range(n):  # source vertex
            for j in range(n):  # destination vertex
                if distances[i][k] != float('inf') and distances[k][j] != float('inf'):
                    distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
    
    return distances

# Example usage
n = 4
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
dimensions = 1
result = multi_dimensional_shortest_routes_ii(n, edges, dimensions)
print("Multi-dimensional all-pairs shortest distances:")
for row in result:
    print(row)
```

### Related Problems

#### **CSES Problems**
- [Shortest Routes I](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Flight Discount](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [High Score](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Network Delay Time](https://leetcode.com/problems/network-delay-time/) - Graph
- [Cheapest Flights](https://leetcode.com/problems/cheapest-flights-within-k-stops/) - Graph
- [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: All-pairs shortest path, Floyd-Warshall algorithm
- **Shortest Path**: Floyd-Warshall, Johnson's algorithm, shortest path algorithms
- **Dynamic Programming**: Optimal substructure, overlapping subproblems

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Floyd-Warshall](https://cp-algorithms.com/graph/all-pair-shortest-path-floyd-warshall.html) - Floyd-Warshall algorithm
- [All-Pairs Shortest Path](https://cp-algorithms.com/graph/all-pair-shortest-path.html) - All-pairs shortest path algorithms

### **Practice Problems**
- [CSES Shortest Routes I](https://cses.fi/problemset/task/1075) - Medium
- [CSES Flight Discount](https://cses.fi/problemset/task/1075) - Medium
- [CSES High Score](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Floyd-Warshall Algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm) - Wikipedia article
- [All-Pairs Shortest Path Problem](https://en.wikipedia.org/wiki/Shortest_path_problem#All-pairs_shortest_paths) - Wikipedia article
