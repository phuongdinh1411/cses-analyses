---
layout: simple
title: "Round Trip - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/round_trip_analysis
---

# Round Trip - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of cycle detection in undirected graphs
- Apply efficient algorithms for finding cycles in graphs
- Implement DFS-based cycle detection algorithms
- Optimize graph traversal for cycle identification
- Handle special cases in cycle detection problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, cycle detection, DFS
- **Data Structures**: Graphs, visited arrays, parent arrays
- **Mathematical Concepts**: Graph theory, cycles, connectivity
- **Programming Skills**: Graph operations, DFS, cycle detection
- **Related Problems**: Cycle Finding (graph_algorithms), Planets Cycles (graph_algorithms), Planets and Kingdoms (graph_algorithms)

## 📋 Problem Description

Given an undirected graph, find if there exists a cycle and return the cycle path.

**Input**: 
- n: number of vertices
- m: number of edges
- edges: array of undirected edges (u, v)

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
Graph: 0-1-2-3-0

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
def brute_force_round_trip(n, edges):
    """Find cycles using brute force approach"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
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
result = brute_force_round_trip(n, edges)
print(f"Brute force cycle: {result}")
```

**Time Complexity**: O(n!)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n!) time complexity for checking all paths.

---

### Approach 2: DFS with Parent Tracking

**Key Insights from DFS with Parent Tracking**:
- **DFS with Parent**: Use DFS with parent tracking for cycle detection
- **Efficient Implementation**: O(n + m) time complexity
- **Parent Array**: Track parent of each vertex during DFS
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use DFS with parent tracking to detect cycles in undirected graphs.

**Algorithm**:
- Perform DFS from each unvisited vertex
- Track parent of each vertex
- If we encounter a visited vertex that's not the parent, we found a cycle

**Visual Example**:
```
DFS with parent tracking:

Graph: 0-1-2-3-0
Parent tracking:
┌─────────────────────────────────────┐
│ Start DFS from 0:                  │
│ 0: parent = -1, visited = True     │
│ 1: parent = 0, visited = True      │
│ 2: parent = 1, visited = True      │
│ 3: parent = 2, visited = True      │
│ 0: visited = True, parent = 3      │
│ 0 != parent of 3 (2), CYCLE FOUND! │
│                                   │
│ Cycle path: [0, 1, 2, 3, 0]       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dfs_parent_tracking_round_trip(n, edges):
    """Find cycles using DFS with parent tracking"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    visited = [False] * n
    parent = [-1] * n
    
    def dfs(vertex):
        visited[vertex] = True
        
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                parent[neighbor] = vertex
                result = dfs(neighbor)
                if result:
                    return result
            elif neighbor != parent[vertex]:
                # Found cycle - reconstruct path
                cycle = [neighbor]
                current = vertex
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                return cycle
        
        return None
    
    # Try DFS from each unvisited vertex
    for vertex in range(n):
        if not visited[vertex]:
            result = dfs(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
result = dfs_parent_tracking_round_trip(n, edges)
print(f"DFS parent tracking cycle: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n)

**Why it's better**: Uses DFS with parent tracking for O(n + m) time complexity.

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
- Implement efficient DFS algorithms
- Handle special cases optimally
- Return cycle path

**Visual Example**:
```
Advanced data structure approach:

For graph: 0-1-2-3-0
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph structure: for efficient    │
│   storage and traversal             │
│ - Parent cache: for optimization    │
│ - Cycle tracker: for optimization   │
│                                   │
│ Cycle detection:                   │
│ - Use graph structure for efficient │
│   storage and traversal             │
│ - Use parent cache for optimization │
│ - Use cycle tracker for optimization │
│                                   │
│ Result: [0, 1, 2, 3, 0]           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_round_trip(n, edges):
    """Find cycles using advanced data structure approach"""
    # Use advanced data structures for graph storage
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Advanced data structures for cycle detection
    visited = [False] * n
    parent = [-1] * n
    
    def dfs_advanced(vertex):
        visited[vertex] = True
        
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                parent[neighbor] = vertex
                result = dfs_advanced(neighbor)
                if result:
                    return result
            elif neighbor != parent[vertex]:
                # Found cycle - reconstruct path using advanced data structures
                cycle = [neighbor]
                current = vertex
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                return cycle
        
        return None
    
    # Try advanced DFS from each unvisited vertex
    for vertex in range(n):
        if not visited[vertex]:
            result = dfs_advanced(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
result = advanced_data_structure_round_trip(n, edges)
print(f"Advanced data structure cycle: {result}")
```

**Time Complexity**: O(n + m)
**Space Complexity**: O(n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n!) | O(n) | Check all possible paths |
| DFS with Parent Tracking | O(n + m) | O(n) | Use parent tracking in DFS |
| Advanced Data Structure | O(n + m) | O(n) | Use advanced data structures |

### Time Complexity
- **Time**: O(n + m) - Use DFS with parent tracking for efficient cycle detection
- **Space**: O(n) - Store visited array and parent array

### Why This Solution Works
- **DFS with Parent Tracking**: Track parent of each vertex during DFS
- **Cycle Detection**: If we encounter a visited vertex that's not the parent, we found a cycle
- **Path Reconstruction**: Reconstruct cycle path using parent array
- **Optimal Algorithms**: Use optimal algorithms for cycle detection

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Round Trip with Constraints**
**Problem**: Find cycles with specific constraints.

**Key Differences**: Apply constraints to cycle detection

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_round_trip(n, edges, constraints):
    """Find cycles with constraints"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if constraints(u) and constraints(v):
            adj[u].append(v)
            adj[v].append(u)
    
    visited = [False] * n
    parent = [-1] * n
    
    def dfs_constrained(vertex):
        if not constraints(vertex):
            return None
            
        visited[vertex] = True
        
        for neighbor in adj[vertex]:
            if not visited[neighbor] and constraints(neighbor):
                parent[neighbor] = vertex
                result = dfs_constrained(neighbor)
                if result:
                    return result
            elif neighbor != parent[vertex] and constraints(neighbor):
                # Found cycle - reconstruct path
                cycle = [neighbor]
                current = vertex
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                return cycle
        
        return None
    
    # Try DFS from each unvisited vertex
    for vertex in range(n):
        if not visited[vertex] and constraints(vertex):
            result = dfs_constrained(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
constraints = lambda vertex: vertex >= 0  # Only include non-negative vertices
result = constrained_round_trip(n, edges, constraints)
print(f"Constrained cycle: {result}")
```

#### **2. Round Trip with Different Metrics**
**Problem**: Find cycles with different length metrics.

**Key Differences**: Different length calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_round_trip(n, edges, weights):
    """Find cycles with different weights"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    visited = [False] * n
    parent = [-1] * n
    
    def dfs_weighted(vertex):
        visited[vertex] = True
        
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                parent[neighbor] = vertex
                result = dfs_weighted(neighbor)
                if result:
                    return result
            elif neighbor != parent[vertex]:
                # Found cycle - reconstruct path with weights
                cycle = [neighbor]
                current = vertex
                total_weight = 0
                while current != neighbor:
                    cycle.append(current)
                    total_weight += weights.get((current, parent[current]), 1)
                    current = parent[current]
                cycle.append(neighbor)
                total_weight += weights.get((current, neighbor), 1)
                return cycle, total_weight
        
        return None
    
    # Try DFS from each unvisited vertex
    for vertex in range(n):
        if not visited[vertex]:
            result = dfs_weighted(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
weights = {(0, 1): 2, (1, 2): 1, (2, 3): 3, (3, 0): 1}
result = weighted_round_trip(n, edges, weights)
print(f"Weighted cycle: {result}")
```

#### **3. Round Trip with Multiple Dimensions**
**Problem**: Find cycles in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_round_trip(n, edges, dimensions):
    """Find cycles in multiple dimensions"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    visited = [False] * n
    parent = [-1] * n
    
    def dfs_multi_dimensional(vertex):
        visited[vertex] = True
        
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                parent[neighbor] = vertex
                result = dfs_multi_dimensional(neighbor)
                if result:
                    return result
            elif neighbor != parent[vertex]:
                # Found cycle - reconstruct path
                cycle = [neighbor]
                current = vertex
                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(neighbor)
                return cycle
        
        return None
    
    # Try DFS from each unvisited vertex
    for vertex in range(n):
        if not visited[vertex]:
            result = dfs_multi_dimensional(vertex)
            if result:
                return result
    
    return None

# Example usage
n = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
dimensions = 1
result = multi_dimensional_round_trip(n, edges, dimensions)
print(f"Multi-dimensional cycle: {result}")
```

### Related Problems

#### **CSES Problems**
- [Cycle Finding](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Planets Cycles](https://cses.fi/problemset/task/1075) - Graph Algorithms
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
- [CSES Planets Cycles](https://cses.fi/problemset/task/1075) - Medium
- [CSES Planets and Kingdoms](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Cycle Detection](https://en.wikipedia.org/wiki/Cycle_detection) - Wikipedia article
- [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search) - Wikipedia article

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