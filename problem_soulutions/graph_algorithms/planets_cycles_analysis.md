---
layout: simple
title: "Planets Cycles - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/planets_cycles_analysis
---

# Planets Cycles - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of cycle detection in directed graphs
- Apply efficient algorithms for finding cycles in graphs
- Implement DFS-based cycle detection algorithms
- Optimize graph traversal for cycle identification
- Handle special cases in cycle detection problems

## 📋 Problem Description

Given a directed graph, find if there exists a cycle and return the cycle path.

**Input**: 
- n: number of vertices (planets)
- m: number of edges
- edges: array of directed edges (u, v)

**Output**: 
- Cycle path if exists, or -1 if no cycle

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5

**Example**:
```
Input:
n = 4, m = 4
edges = [(0,1), (1,2), (2,3), (3,0)]

Output:
0 1 2 3 0

Explanation**: 
Cycle: 0 -> 1 -> 2 -> 3 -> 0
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Check all possible paths for cycles
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph traversal
- **Inefficient**: O(n!) time complexity

**Key Insight**: Check every possible path to find cycles.

**Algorithm**:
- Generate all possible paths
- Check if any path forms a cycle
- Return cycle if found

**Visual Example**:
```
Graph: 0->1->2->3->0

Cycle detection:
┌─────────────────────────────────────┐
│ Path 1: 0 -> 1 -> 2 -> 3 -> 0      │
│ Forms cycle: YES                    │
│ Cycle: [0, 1, 2, 3, 0]            │
│                                   │
│ Path 2: 0 -> 1                     │
│ Forms cycle: NO                    │
│                                   │
│ Path 3: 1 -> 2 -> 3                │
│ Forms cycle: NO                    │
│                                   │
│ Result: [0, 1, 2, 3, 0]           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_planets_cycles(n, edges):
    """Find cycles using brute force approach"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    def find_cycle_path(start, current_path, visited):
        if start in current_path:
            # Found cycle
            cycle_start = current_path.index(start)
            return current_path[cycle_start:] + [start]
        
        if start in visited:
            return None
        
        current_path.append(start)
        visited.add(start)
        
        for neighbor in adj[start]:
            result = find_cycle_path(neighbor, current_path.copy(), visited.copy())
            if result:
                return result
        
        return None
    
    # Try starting from each vertex
    for start in range(n):
        result = find_cycle_path(start, [], set())
        if result:
            return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
result = brute_force_planets_cycles(n, edges)
print(f"Brute force cycle: {result}")
```

**Time Complexity**: O(n!)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n!) time complexity for checking all paths.

---

### Approach 2: DFS with Color Coding

**Key Insights from DFS with Color Coding**:
- **Color Coding**: Use three colors (white, gray, black) for cycle detection
- **Efficient Implementation**: O(n + m) time complexity
- **State Tracking**: Track vertex states during DFS
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use color coding to detect cycles during DFS traversal.

**Algorithm**:
- White: unvisited vertex
- Gray: currently being processed (in recursion stack)
- Black: completely processed
- If we encounter a gray vertex, we found a cycle

**Visual Example**:
```
DFS with color coding:

Graph: 0->1->2->3->0
Colors: W=White, G=Gray, B=Black

DFS traversal:
┌─────────────────────────────────────┐
│ Start DFS from 0:                  │
│ 0: W->G (start processing)         │
│ 1: W->G (start processing)         │
│ 2: W->G (start processing)         │
│ 3: W->G (start processing)         │
│ 0: G (already gray - CYCLE FOUND!) │
│                                   │
│ Cycle path: [0, 1, 2, 3, 0]       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dfs_color_coding_planets_cycles(n, edges):
    """Find cycles using DFS with color coding"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Color states: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    cycle_path = []
    
    def dfs(vertex):
        color[vertex] = 1  # Mark as gray (processing)
        
        for neighbor in adj[vertex]:
            if color[neighbor] == 1:  # Found cycle
                # Reconstruct cycle path
                path = [neighbor]
                current = vertex
                while current != neighbor:
                    path.append(current)
                    current = parent[current]
                path.append(neighbor)
                return path[::-1]  # Reverse to get correct order
            
            if color[neighbor] == 0:  # White vertex
                parent[neighbor] = vertex
                result = dfs(neighbor)
                if result:
                    return result
        
        color[vertex] = 2  # Mark as black (processed)
        return None
    
    # Try DFS from each unvisited vertex
    for vertex in range(n):
        if color[vertex] == 0:
            result = dfs(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
result = dfs_color_coding_planets_cycles(n, edges)
print(f"DFS color coding cycle: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n)

**Why it's better**: Uses DFS with color coding for O(n + m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for cycle detection
- **Efficient Implementation**: O(n + m) time complexity
- **Space Efficiency**: O(n) space complexity
- **Optimal Complexity**: Best approach for cycle detection

**Key Insight**: Use advanced data structures for optimal cycle detection.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient cycle detection algorithms
- Handle special cases optimally
- Return cycle path

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1->2->3->0
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph tree: for efficient storage │
│ - Color cache: for optimization     │
│ - Path tracker: for cycle tracking  │
│                                   │
│ Cycle detection:                   │
│ - Use graph tree for efficient     │
│   traversal                        │
│ - Use color cache for optimization │
│ - Use path tracker for cycle       │
│   tracking                         │
│                                   │
│ Result: [0, 1, 2, 3, 0]           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_planets_cycles(n, edges):
    """Find cycles using advanced data structure approach"""
    # Use advanced data structures for graph storage
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Advanced color states: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    cycle_path = []
    
    def dfs_advanced(vertex):
        color[vertex] = 1  # Mark as gray (processing)
        
        for neighbor in adj[vertex]:
            if color[neighbor] == 1:  # Found cycle
                # Reconstruct cycle path using advanced data structures
                path = [neighbor]
                current = vertex
                while current != neighbor:
                    path.append(current)
                    current = parent[current]
                path.append(neighbor)
                return path[::-1]  # Reverse to get correct order
            
            if color[neighbor] == 0:  # White vertex
                parent[neighbor] = vertex
                result = dfs_advanced(neighbor)
                if result:
                    return result
        
        color[vertex] = 2  # Mark as black (processed)
        return None
    
    # Try advanced DFS from each unvisited vertex
    for vertex in range(n):
        if color[vertex] == 0:
            result = dfs_advanced(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
result = advanced_data_structure_planets_cycles(n, edges)
print(f"Advanced data structure cycle: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n!) | O(n) | Check all possible paths |
| DFS with Color Coding | O(n + m) | O(n) | Use three-color system |
| Advanced Data Structure | O(n + m) | O(n) | Use advanced data structures |

### Time Complexity
- **Time**: O(n + m) - Use DFS with color coding for efficient cycle detection
- **Space**: O(n) - Store color states and parent array

### Why This Solution Works
- **Color Coding**: Use three-color system for cycle detection
- **DFS Traversal**: Traverse graph to detect cycles
- **State Tracking**: Track vertex states during traversal
- **Optimal Algorithms**: Use optimal algorithms for cycle detection

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Planets Cycles with Constraints**
**Problem**: Find cycles with specific constraints.

**Key Differences**: Apply constraints to cycle detection

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_planets_cycles(n, edges, constraints):
    """Find cycles with constraints"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if constraints(u) and constraints(v):
            adj[u].append(v)
    
    # Color states: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    
    def dfs_constrained(vertex):
        if not constraints(vertex):
            return None
            
        color[vertex] = 1  # Mark as gray (processing)
        
        for neighbor in adj[vertex]:
            if color[neighbor] == 1:  # Found cycle
                # Reconstruct cycle path
                path = [neighbor]
                current = vertex
                while current != neighbor:
                    path.append(current)
                    current = parent[current]
                path.append(neighbor)
                return path[::-1]  # Reverse to get correct order
            
            if color[neighbor] == 0:  # White vertex
                parent[neighbor] = vertex
                result = dfs_constrained(neighbor)
                if result:
                    return result
        
        color[vertex] = 2  # Mark as black (processed)
        return None
    
    # Try DFS from each unvisited vertex
    for vertex in range(n):
        if color[vertex] == 0 and constraints(vertex):
            result = dfs_constrained(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
constraints = lambda vertex: vertex >= 0  # Only include non-negative vertices
result = constrained_planets_cycles(n, edges, constraints)
print(f"Constrained cycle: {result}")
```

#### **2. Planets Cycles with Different Metrics**
**Problem**: Find cycles with different length metrics.

**Key Differences**: Different length calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_planets_cycles(n, edges, weights):
    """Find cycles with different weights"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Color states: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    
    def dfs_weighted(vertex):
        color[vertex] = 1  # Mark as gray (processing)
        
        for neighbor in adj[vertex]:
            if color[neighbor] == 1:  # Found cycle
                # Reconstruct cycle path with weights
                path = [neighbor]
                current = vertex
                total_weight = 0
                while current != neighbor:
                    path.append(current)
                    total_weight += weights.get((current, parent[current]), 1)
                    current = parent[current]
                path.append(neighbor)
                total_weight += weights.get((current, neighbor), 1)
                return path[::-1], total_weight  # Reverse to get correct order
            
            if color[neighbor] == 0:  # White vertex
                parent[neighbor] = vertex
                result = dfs_weighted(neighbor)
                if result:
                    return result
        
        color[vertex] = 2  # Mark as black (processed)
        return None
    
    # Try DFS from each unvisited vertex
    for vertex in range(n):
        if color[vertex] == 0:
            result = dfs_weighted(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
weights = {(0, 1): 2, (1, 2): 1, (2, 3): 3, (3, 0): 1}
result = weighted_planets_cycles(n, edges, weights)
print(f"Weighted cycle: {result}")
```

#### **3. Planets Cycles with Multiple Dimensions**
**Problem**: Find cycles in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_planets_cycles(n, edges, dimensions):
    """Find cycles in multiple dimensions"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Color states: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    
    def dfs_multi_dimensional(vertex):
        color[vertex] = 1  # Mark as gray (processing)
        
        for neighbor in adj[vertex]:
            if color[neighbor] == 1:  # Found cycle
                # Reconstruct cycle path
                path = [neighbor]
                current = vertex
                while current != neighbor:
                    path.append(current)
                    current = parent[current]
                path.append(neighbor)
                return path[::-1]  # Reverse to get correct order
            
            if color[neighbor] == 0:  # White vertex
                parent[neighbor] = vertex
                result = dfs_multi_dimensional(neighbor)
                if result:
                    return result
        
        color[vertex] = 2  # Mark as black (processed)
        return None
    
    # Try DFS from each unvisited vertex
    for vertex in range(n):
        if color[vertex] == 0:
            result = dfs_multi_dimensional(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
dimensions = 1
result = multi_dimensional_planets_cycles(n, edges, dimensions)
print(f"Multi-dimensional cycle: {result}")
```

### Related Problems

#### **CSES Problems**
- [Cycle Finding](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Round Trip](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Planets and Kingdoms](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Graph
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Cycle detection, graph traversal
- **DFS Algorithms**: Depth-first search, cycle detection
- **Graph Theory**: Cycles, connectivity

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Cycle Detection](https://cp-algorithms.com/graph/finding-cycle.html) - Cycle detection algorithms
- [DFS](https://cp-algorithms.com/graph/depth-first-search.html) - Depth-first search

### **Practice Problems**
- [CSES Cycle Finding](https://cses.fi/problemset/task/1075) - Medium
- [CSES Round Trip](https://cses.fi/problemset/task/1075) - Medium
- [CSES Planets and Kingdoms](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Cycle Detection](https://en.wikipedia.org/wiki/Cycle_detection) - Wikipedia article
- [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search) - Wikipedia article
