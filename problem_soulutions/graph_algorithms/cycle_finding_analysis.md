---
layout: simple
title: "Cycle Finding - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/cycle_finding_analysis
---

# Cycle Finding - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of cycle detection in directed and undirected graphs
- Apply efficient algorithms for finding cycles in graphs
- Implement DFS-based cycle detection with color coding
- Optimize graph algorithms for cycle detection problems
- Handle special cases in cycle detection problems

## 📋 Problem Description

Given a directed graph, find if it contains a cycle and return the cycle if it exists.

**Input**: 
- n: number of vertices
- m: number of edges
- edges: array of (u, v) representing directed edges

**Output**: 
- Cycle as a list of vertices, or -1 if no cycle exists

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5

**Example**:
```
Input:
n = 4, m = 4
edges = [(0,1), (1,2), (2,3), (3,0)]

Output:
[0, 1, 2, 3, 0]

Explanation**: 
Cycle: 0 -> 1 -> 2 -> 3 -> 0
All vertices form a directed cycle
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible paths to find cycles
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph traversal for each path
- **Inefficient**: O(n!) time complexity

**Key Insight**: Check every possible path to find if any forms a cycle.

**Algorithm**:
- Generate all possible paths in the graph
- Check if any path forms a cycle
- Return the first cycle found

**Visual Example**:
```
Graph: 0->1, 1->2, 2->3, 3->0

All possible paths:
┌─────────────────────────────────────┐
│ Path 1: 0 -> 1 -> 2 -> 3 -> 0 ✓    │
│ Path 2: 0 -> 1 -> 2 -> 3           │
│ Path 3: 1 -> 2 -> 3 -> 0 -> 1 ✓    │
│ Path 4: 2 -> 3 -> 0 -> 1 -> 2 ✓    │
│ Path 5: 3 -> 0 -> 1 -> 2 -> 3 ✓    │
│                                   │
│ Check each path:                   │
│ - Path 1: starts and ends at 0 ✓   │
│ - Path 3: starts and ends at 1 ✓   │
│ - Path 4: starts and ends at 2 ✓   │
│ - Path 5: starts and ends at 3 ✓   │
│                                   │
│ Cycles found: 1, 3, 4, 5          │
│ Return: [0, 1, 2, 3, 0]          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_cycle_finding(n, edges):
    """Find cycle using brute force approach"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    def find_all_paths(start, current_path, visited):
        """Find all possible paths from start"""
        if len(current_path) > 1 and current_path[0] == current_path[-1]:
            return [current_path]  # Found a cycle
        
        if len(current_path) > n:
            return []  # Path too long, no cycle
        
        paths = []
        for neighbor in adj[start]:
            if neighbor not in visited:
                new_path = current_path + [neighbor]
                new_visited = visited | {neighbor}
                paths.extend(find_all_paths(neighbor, new_path, new_visited))
        
        return paths
    
    # Try starting from each vertex
    for start in range(n):
        paths = find_all_paths(start, [start], {start})
        if paths:
            return paths[0]
    
    return -1

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
result = brute_force_cycle_finding(n, edges)
print(f"Brute force cycle: {result}")
```

**Time Complexity**: O(n!)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n!) time complexity for checking all possible paths.

---

### Approach 2: DFS with Color Coding

**Key Insights from DFS with Color Coding**:
- **Color Coding**: Use three colors (white, gray, black) to track vertex states
- **Efficient Implementation**: O(n + m) time complexity
- **Cycle Detection**: Detect back edges during DFS traversal
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use DFS with color coding to detect back edges that indicate cycles.

**Algorithm**:
- Use three colors: white (unvisited), gray (visiting), black (visited)
- During DFS, if we encounter a gray vertex, we found a back edge (cycle)
- Track the path to reconstruct the cycle

**Visual Example**:
```
DFS with color coding:

Graph: 0->1, 1->2, 2->3, 3->0
Colors: white (0), gray (1), black (2)

Step 1: Start DFS from 0
┌─────────────────────────────────────┐
│ Color[0] = gray (visiting)         │
│ Stack: [0]                         │
│                                   │
│ Step 2: Visit 1                    │
│ Color[1] = gray (visiting)         │
│ Stack: [0, 1]                     │
│                                   │
│ Step 3: Visit 2                    │
│ Color[2] = gray (visiting)         │
│ Stack: [0, 1, 2]                  │
│                                   │
│ Step 4: Visit 3                    │
│ Color[3] = gray (visiting)         │
│ Stack: [0, 1, 2, 3]               │
│                                   │
│ Step 5: Try to visit 0             │
│ Color[0] = gray (already visiting) │
│ Back edge found! Cycle detected!   │
│                                   │
│ Reconstruct cycle: [0, 1, 2, 3, 0] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dfs_color_coding_cycle_finding(n, edges):
    """Find cycle using DFS with color coding"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Color coding: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    cycle = []
    
    def dfs(vertex):
        """DFS with color coding for cycle detection"""
        color[vertex] = 1  # Mark as gray (visiting)
        
        for neighbor in adj[vertex]:
            if color[neighbor] == 0:  # White (unvisited)
                parent[neighbor] = vertex
                if dfs(neighbor):
                    return True
            elif color[neighbor] == 1:  # Gray (visiting) - back edge found!
                # Reconstruct cycle
                cycle.append(neighbor)
                current = vertex
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                cycle.reverse()
                return True
        
        color[vertex] = 2  # Mark as black (visited)
        return False
    
    # Try DFS from each unvisited vertex
    for i in range(n):
        if color[i] == 0:  # White (unvisited)
            if dfs(i):
                return cycle
    
    return -1

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
result = dfs_color_coding_cycle_finding(n, edges)
print(f"DFS color coding cycle: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's better**: Uses DFS with color coding for O(n + m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for cycle detection
- **Efficient Implementation**: O(n + m) time complexity
- **Space Efficiency**: O(n + m) space complexity
- **Optimal Complexity**: Best approach for cycle detection

**Key Insight**: Use advanced data structures for optimal cycle detection.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient DFS with optimized color coding
- Handle special cases optimally
- Return cycle

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1, 1->2, 2->3, 3->0
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph structure: for efficient    │
│   storage and traversal             │
│ - Color cache: for optimization     │
│ - Parent cache: for optimization    │
│                                   │
│ Cycle detection calculation:       │
│ - Use graph structure for efficient │
│   storage and traversal             │
│ - Use color cache for optimization  │
│ - Use parent cache for optimization │
│                                   │
│ Result: [0, 1, 2, 3, 0]          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_cycle_finding(n, edges):
    """Find cycle using advanced data structure approach"""
    # Use advanced data structures for graph storage
    # Build advanced adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Advanced data structures for cycle detection
    # Color coding: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    cycle = []
    
    def advanced_dfs(vertex):
        """Advanced DFS with optimized color coding"""
        color[vertex] = 1  # Mark as gray (visiting)
        
        # Process neighbors using advanced data structures
        for neighbor in adj[vertex]:
            if color[neighbor] == 0:  # White (unvisited)
                parent[neighbor] = vertex
                if advanced_dfs(neighbor):
                    return True
            elif color[neighbor] == 1:  # Gray (visiting) - back edge found!
                # Advanced cycle reconstruction
                cycle.append(neighbor)
                current = vertex
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                cycle.reverse()
                return True
        
        color[vertex] = 2  # Mark as black (visited)
        return False
    
    # Advanced DFS from each unvisited vertex
    for i in range(n):
        if color[i] == 0:  # White (unvisited)
            if advanced_dfs(i):
                return cycle
    
    return -1

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
result = advanced_data_structure_cycle_finding(n, edges)
print(f"Advanced data structure cycle: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n + m)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n!) | O(n) | Try all possible paths |
| DFS Color Coding | O(n + m) | O(n + m) | Use color coding to detect back edges |
| Advanced Data Structure | O(n + m) | O(n + m) | Use advanced data structures |

### Time Complexity
- **Time**: O(n + m) - Use DFS with color coding for efficient cycle detection
- **Space**: O(n + m) - Store graph and auxiliary data structures

### Why This Solution Works
- **Color Coding**: Use three colors to track vertex states during DFS
- **Back Edge Detection**: Detect cycles by finding back edges to gray vertices
- **Cycle Reconstruction**: Reconstruct cycle using parent pointers
- **Optimal Algorithms**: Use optimal algorithms for cycle detection

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Cycle Finding with Constraints**
**Problem**: Find cycles with specific constraints.

**Key Differences**: Apply constraints to cycle detection

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_cycle_finding(n, edges, constraints):
    """Find cycles with constraints"""
    # Build adjacency list with constraints
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if constraints(u, v):
            adj[u].append(v)
    
    # Color coding: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    cycle = []
    
    def constrained_dfs(vertex):
        """DFS with constraints for cycle detection"""
        color[vertex] = 1  # Mark as gray (visiting)
        
        for neighbor in adj[vertex]:
            if constraints(vertex, neighbor):
                if color[neighbor] == 0:  # White (unvisited)
                    parent[neighbor] = vertex
                    if constrained_dfs(neighbor):
                        return True
                elif color[neighbor] == 1:  # Gray (visiting) - back edge found!
                    # Reconstruct cycle with constraints
                    cycle.append(neighbor)
                    current = vertex
                    while current != neighbor:
                        cycle.append(current)
                        current = parent[current]
                    cycle.append(neighbor)
                    cycle.reverse()
                    return True
        
        color[vertex] = 2  # Mark as black (visited)
        return False
    
    # Try constrained DFS from each unvisited vertex
    for i in range(n):
        if color[i] == 0:  # White (unvisited)
            if constrained_dfs(i):
                return cycle
    
    return -1

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
constraints = lambda u, v: u < v or v == 0  # Special constraint
result = constrained_cycle_finding(n, edges, constraints)
print(f"Constrained cycle: {result}")
```

#### **2. Cycle Finding with Different Metrics**
**Problem**: Find cycles with different length metrics.

**Key Differences**: Different cycle length calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_cycle_finding(n, edges, weight_function):
    """Find cycles with different weight metrics"""
    # Build adjacency list with modified weights
    adj = [[] for _ in range(n)]
    for u, v in edges:
        weight = weight_function(u, v)
        adj[u].append((v, weight))
    
    # Color coding: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    cycle = []
    
    def weighted_dfs(vertex):
        """DFS with weights for cycle detection"""
        color[vertex] = 1  # Mark as gray (visiting)
        
        for neighbor, weight in adj[vertex]:
            if color[neighbor] == 0:  # White (unvisited)
                parent[neighbor] = vertex
                if weighted_dfs(neighbor):
                    return True
            elif color[neighbor] == 1:  # Gray (visiting) - back edge found!
                # Reconstruct cycle with weights
                cycle.append(neighbor)
                current = vertex
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                cycle.reverse()
                return True
        
        color[vertex] = 2  # Mark as black (visited)
        return False
    
    # Try weighted DFS from each unvisited vertex
    for i in range(n):
        if color[i] == 0:  # White (unvisited)
            if weighted_dfs(i):
                return cycle
    
    return -1

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
weight_function = lambda u, v: abs(u - v)  # Distance-based weight
result = weighted_cycle_finding(n, edges, weight_function)
print(f"Weighted cycle: {result}")
```

#### **3. Cycle Finding with Multiple Dimensions**
**Problem**: Find cycles in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_cycle_finding(n, edges, dimensions):
    """Find cycles in multiple dimensions"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Color coding: 0=white, 1=gray, 2=black
    color = [0] * n
    parent = [-1] * n
    cycle = []
    
    def multi_dimensional_dfs(vertex):
        """DFS for multiple dimensions"""
        color[vertex] = 1  # Mark as gray (visiting)
        
        for neighbor in adj[vertex]:
            if color[neighbor] == 0:  # White (unvisited)
                parent[neighbor] = vertex
                if multi_dimensional_dfs(neighbor):
                    return True
            elif color[neighbor] == 1:  # Gray (visiting) - back edge found!
                # Reconstruct cycle
                cycle.append(neighbor)
                current = vertex
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                cycle.reverse()
                return True
        
        color[vertex] = 2  # Mark as black (visited)
        return False
    
    # Try multi-dimensional DFS from each unvisited vertex
    for i in range(n):
        if color[i] == 0:  # White (unvisited)
            if multi_dimensional_dfs(i):
                return cycle
    
    return -1

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
dimensions = 1
result = multi_dimensional_cycle_finding(n, edges, dimensions)
print(f"Multi-dimensional cycle: {result}")
```

### Related Problems

#### **CSES Problems**
- [Round Trip](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Planets Cycles](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Message Route](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Graph
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Cycle detection, DFS, color coding
- **Cycle Detection**: Back edge detection, cycle reconstruction
- **Graph Traversal**: DFS, graph coloring

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Cycle Detection](https://cp-algorithms.com/graph/finding-cycle.html) - Cycle detection algorithms
- [DFS](https://cp-algorithms.com/graph/depth-first-search.html) - DFS algorithms

### **Practice Problems**
- [CSES Round Trip](https://cses.fi/problemset/task/1075) - Medium
- [CSES Planets Cycles](https://cses.fi/problemset/task/1075) - Medium
- [CSES Message Route](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Cycle (Graph Theory)](https://en.wikipedia.org/wiki/Cycle_(graph_theory)) - Wikipedia article
- [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search) - Wikipedia article
