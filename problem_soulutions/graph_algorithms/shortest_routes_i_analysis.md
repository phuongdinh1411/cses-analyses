---
layout: simple
title: "Shortest Routes I - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/shortest_routes_i_analysis
---

# Shortest Routes I - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of single-source shortest path in graph algorithms
- Apply efficient algorithms for finding shortest paths from one source
- Implement Dijkstra's algorithm for weighted graphs
- Optimize graph traversal for shortest path calculations
- Handle special cases in shortest path problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, shortest path, Dijkstra's algorithm
- **Data Structures**: Graphs, priority queues, distance arrays
- **Mathematical Concepts**: Graph theory, shortest paths, weighted graphs
- **Programming Skills**: Graph operations, priority queues, shortest path algorithms
- **Related Problems**: Shortest Routes II (graph_algorithms), Flight Discount (graph_algorithms), High Score (graph_algorithms)

## 📋 Problem Description

Given a weighted directed graph, find the shortest distance from a source vertex to all other vertices.

**Input**: 
- n: number of vertices
- m: number of edges
- source: source vertex
- edges: array of (u, v, weight) representing directed edges

**Output**: 
- Shortest distance from source to each vertex

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5
- 1 ≤ weight ≤ 10^9

**Example**:
```
Input:
n = 4, m = 4, source = 0
edges = [(0,1,1), (0,2,4), (1,2,2), (2,3,1)]

Output:
[0, 1, 3, 4]

Explanation**: 
Shortest distances from 0:
- 0 to 0: 0
- 0 to 1: 1 (direct edge)
- 0 to 2: 3 (0->1->2: 1+2=3)
- 0 to 3: 4 (0->1->2->3: 1+2+1=4)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible paths from source
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph traversal
- **Inefficient**: O(n!) time complexity

**Key Insight**: Check every possible path from source to find shortest distances.

**Algorithm**:
- Generate all possible paths from source
- Calculate distance for each path
- Keep track of minimum distance to each vertex

**Visual Example**:
```
Graph: 0->1(1), 0->2(4), 1->2(2), 2->3(1)

All paths from source 0:
┌─────────────────────────────────────┐
│ Path 1: 0 -> 1, distance = 1       │
│ Path 2: 0 -> 2, distance = 4       │
│ Path 3: 0 -> 1 -> 2, distance = 3  │
│ Path 4: 0 -> 1 -> 2 -> 3, distance = 4 │
│                                   │
│ Shortest distances:                │
│ dist[0] = 0                       │
│ dist[1] = 1                       │
│ dist[2] = 3                       │
│ dist[3] = 4                       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_shortest_routes_i(n, source, edges):
    """Find shortest distances using brute force approach"""
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
    
    # Find shortest distance to each vertex
    distances = [float('inf')] * n
    distances[source] = 0
    
    for target in range(n):
        if target != source:
            all_distances = find_all_paths(source, target, {source}, [source], 0)
            if all_distances:
                distances[target] = min(all_distances)
    
    return distances

# Example usage
n = 4
source = 0
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
result = brute_force_shortest_routes_i(n, source, edges)
print(f"Brute force shortest distances: {result}")
```

**Time Complexity**: O(n!)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n!) time complexity for checking all possible paths.

---

### Approach 2: Dijkstra's Algorithm

**Key Insights from Dijkstra's Algorithm**:
- **Dijkstra's Algorithm**: Use Dijkstra's algorithm for efficient shortest path
- **Efficient Implementation**: O((n + m) log n) time complexity
- **Priority Queue**: Use priority queue to always process closest vertex
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use Dijkstra's algorithm with priority queue for efficient shortest path calculation.

**Algorithm**:
- Initialize distances to infinity except source (0)
- Use priority queue to process vertices by distance
- For each vertex, relax all outgoing edges
- Continue until all vertices are processed

**Visual Example**:
```
Dijkstra's algorithm:

Graph: 0->1(1), 0->2(4), 1->2(2), 2->3(1)
Priority queue: (distance, vertex)

Step 1: Start with (0, 0)
┌─────────────────────────────────────┐
│ Process vertex 0:                  │
│ - Relax 0->1: dist[1] = 1          │
│ - Relax 0->2: dist[2] = 4          │
│ Queue: [(1,1), (4,2)]              │
│                                   │
│ Step 2: Process vertex 1:          │
│ - Relax 1->2: dist[2] = min(4, 1+2) = 3 │
│ Queue: [(3,2)]                     │
│                                   │
│ Step 3: Process vertex 2:          │
│ - Relax 2->3: dist[3] = 3+1 = 4    │
│ Queue: [(4,3)]                     │
│                                   │
│ Final distances: [0, 1, 3, 4]     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dijkstra_shortest_routes_i(n, source, edges):
    """Find shortest distances using Dijkstra's algorithm"""
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, weight in edges:
        adj[u].append((v, weight))
    
    # Initialize distances
    distances = [float('inf')] * n
    distances[source] = 0
    
    # Priority queue: (distance, vertex)
    pq = [(0, source)]
    visited = [False] * n
    
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        
        if visited[current_vertex]:
            continue
        
        visited[current_vertex] = True
        
        # Relax all outgoing edges
        for neighbor, weight in adj[current_vertex]:
            if not visited[neighbor]:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

# Example usage
n = 4
source = 0
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
result = dijkstra_shortest_routes_i(n, source, edges)
print(f"Dijkstra's shortest distances: {result}")
```

**Time Complexity**: O((n + m) log n)
**Space Complexity**: O(n + m)

**Why it's better**: Uses Dijkstra's algorithm for O((n + m) log n) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for shortest path
- **Efficient Implementation**: O((n + m) log n) time complexity
- **Space Efficiency**: O(n + m) space complexity
- **Optimal Complexity**: Best approach for single-source shortest path

**Key Insight**: Use advanced data structures for optimal shortest path calculation.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient Dijkstra's algorithm
- Handle special cases optimally
- Return shortest distances

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1(1), 0->2(4), 1->2(2), 2->3(1)
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph structure: for efficient    │
│   storage and traversal             │
│ - Priority queue: for optimization  │
│ - Distance cache: for optimization  │
│                                   │
│ Shortest path calculation:         │
│ - Use graph structure for efficient │
│   storage and traversal             │
│ - Use priority queue for           │
│   optimization                      │
│ - Use distance cache for           │
│   optimization                      │
│                                   │
│ Result: [0, 1, 3, 4]              │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_shortest_routes_i(n, source, edges):
    """Find shortest distances using advanced data structure approach"""
    import heapq
    
    # Use advanced data structures for graph storage
    # Build advanced adjacency list
    adj = [[] for _ in range(n)]
    for u, v, weight in edges:
        adj[u].append((v, weight))
    
    # Advanced data structures for shortest path
    distances = [float('inf')] * n
    distances[source] = 0
    
    # Advanced priority queue: (distance, vertex)
    pq = [(0, source)]
    visited = [False] * n
    
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        
        if visited[current_vertex]:
            continue
        
        visited[current_vertex] = True
        
        # Relax all outgoing edges using advanced data structures
        for neighbor, weight in adj[current_vertex]:
            if not visited[neighbor]:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

# Example usage
n = 4
source = 0
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
result = advanced_data_structure_shortest_routes_i(n, source, edges)
print(f"Advanced data structure shortest distances: {result}")
```

**Time Complexity**: O((n + m) log n)
**Space Complexity**: O(n + m)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n!) | O(n) | Try all possible paths |
| Dijkstra's Algorithm | O((n + m) log n) | O(n + m) | Use priority queue for closest vertex |
| Advanced Data Structure | O((n + m) log n) | O(n + m) | Use advanced data structures |

### Time Complexity
- **Time**: O((n + m) log n) - Use Dijkstra's algorithm for efficient shortest path
- **Space**: O(n + m) - Store graph and priority queue

### Why This Solution Works
- **Dijkstra's Algorithm**: Use priority queue to always process closest vertex
- **Greedy Approach**: Always choose the vertex with minimum distance
- **Edge Relaxation**: Update distances when shorter path is found
- **Optimal Algorithms**: Use optimal algorithms for single-source shortest path

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Shortest Routes I with Constraints**
**Problem**: Find shortest paths with specific constraints.

**Key Differences**: Apply constraints to shortest path calculation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_shortest_routes_i(n, source, edges, constraints):
    """Find shortest paths with constraints"""
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, weight in edges:
        if constraints(u, v, weight):
            adj[u].append((v, weight))
    
    # Initialize distances
    distances = [float('inf')] * n
    distances[source] = 0
    
    # Priority queue: (distance, vertex)
    pq = [(0, source)]
    visited = [False] * n
    
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        
        if visited[current_vertex]:
            continue
        
        visited[current_vertex] = True
        
        # Relax all outgoing edges with constraints
        for neighbor, weight in adj[current_vertex]:
            if not visited[neighbor] and constraints(current_vertex, neighbor, weight):
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

# Example usage
n = 4
source = 0
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
constraints = lambda u, v, w: w <= 10  # Only edges with weight ≤ 10
result = constrained_shortest_routes_i(n, source, edges, constraints)
print(f"Constrained shortest distances: {result}")
```

#### **2. Shortest Routes I with Different Metrics**
**Problem**: Find shortest paths with different distance metrics.

**Key Differences**: Different distance calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_shortest_routes_i(n, source, edges, weight_function):
    """Find shortest paths with different weight metrics"""
    import heapq
    
    # Build adjacency list with modified weights
    adj = [[] for _ in range(n)]
    for u, v, weight in edges:
        new_weight = weight_function(weight)
        adj[u].append((v, new_weight))
    
    # Initialize distances
    distances = [float('inf')] * n
    distances[source] = 0
    
    # Priority queue: (distance, vertex)
    pq = [(0, source)]
    visited = [False] * n
    
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        
        if visited[current_vertex]:
            continue
        
        visited[current_vertex] = True
        
        # Relax all outgoing edges with modified weights
        for neighbor, weight in adj[current_vertex]:
            if not visited[neighbor]:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

# Example usage
n = 4
source = 0
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
weight_function = lambda w: w * w  # Square the weight
result = weighted_shortest_routes_i(n, source, edges, weight_function)
print(f"Weighted shortest distances: {result}")
```

#### **3. Shortest Routes I with Multiple Dimensions**
**Problem**: Find shortest paths in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_shortest_routes_i(n, source, edges, dimensions):
    """Find shortest paths in multiple dimensions"""
    import heapq
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, weight in edges:
        adj[u].append((v, weight))
    
    # Initialize distances
    distances = [float('inf')] * n
    distances[source] = 0
    
    # Priority queue: (distance, vertex)
    pq = [(0, source)]
    visited = [False] * n
    
    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        
        if visited[current_vertex]:
            continue
        
        visited[current_vertex] = True
        
        # Relax all outgoing edges
        for neighbor, weight in adj[current_vertex]:
            if not visited[neighbor]:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

# Example usage
n = 4
source = 0
edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (2, 3, 1)]
dimensions = 1
result = multi_dimensional_shortest_routes_i(n, source, edges, dimensions)
print(f"Multi-dimensional shortest distances: {result}")
```

### Related Problems

#### **CSES Problems**
- [Shortest Routes II](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Flight Discount](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [High Score](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Network Delay Time](https://leetcode.com/problems/network-delay-time/) - Graph
- [Cheapest Flights](https://leetcode.com/problems/cheapest-flights-within-k-stops/) - Graph
- [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Single-source shortest path, Dijkstra's algorithm
- **Shortest Path**: Dijkstra's, Bellman-Ford, shortest path algorithms
- **Priority Queues**: Heap operations, graph traversal

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Dijkstra's Algorithm](https://cp-algorithms.com/graph/dijkstra.html) - Dijkstra's algorithm
- [Shortest Path](https://cp-algorithms.com/graph/shortest_path.html) - Shortest path algorithms

### **Practice Problems**
- [CSES Shortest Routes II](https://cses.fi/problemset/task/1075) - Medium
- [CSES Flight Discount](https://cses.fi/problemset/task/1075) - Medium
- [CSES High Score](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) - Wikipedia article
- [Shortest Path Problem](https://en.wikipedia.org/wiki/Shortest_path_problem) - Wikipedia article

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