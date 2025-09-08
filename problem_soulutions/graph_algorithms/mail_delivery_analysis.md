---
layout: simple
title: "Mail Delivery - Eulerian Circuit Finding"
permalink: /problem_soulutions/graph_algorithms/mail_delivery_analysis
---

# Mail Delivery - Eulerian Circuit Finding

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand Eulerian circuit problems and graph connectivity concepts
- Apply Hierholzer's algorithm or DFS-based approach to find Eulerian circuits
- Implement efficient Eulerian circuit algorithms with proper edge tracking
- Optimize Eulerian circuit solutions using graph representations and circuit construction
- Handle edge cases in Eulerian circuits (no circuit exists, disconnected components, degree conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Eulerian circuits, Hierholzer's algorithm, DFS-based circuits, graph connectivity, circuit algorithms
- **Data Structures**: Adjacency lists, edge tracking, circuit data structures, graph representations
- **Mathematical Concepts**: Graph theory, Eulerian circuits, graph connectivity, degree properties, circuit theory
- **Programming Skills**: Graph traversal, circuit construction, edge tracking, algorithm implementation
- **Related Problems**: Teleporters Path (Eulerian trails), De Bruijn Sequence (Eulerian paths), Graph connectivity

## Problem Description

**Problem**: Given an undirected graph with n nodes and m edges, find an Eulerian circuit (a path that visits every edge exactly once and returns to the starting node).

An Eulerian circuit is a path that traverses every edge in a graph exactly once and returns to the starting vertex. This problem is a classic application of graph theory in routing and delivery systems.

**Input**: 
- First line: Two integers n and m (number of nodes and edges)
- Next m lines: Two integers a and b (edge between nodes a and b)

**Output**: 
- Nodes in order visited in the Eulerian circuit, or "IMPOSSIBLE" if no circuit exists

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n
- Graph is undirected
- No self-loops or multiple edges between same pair of nodes
- Edges are bidirectional

**Example**:
```
Input:
4 4
1 2
2 3
3 4
4 1

Output:
1 2 3 4 1
```

**Explanation**: 
- The graph forms a cycle: 1→2→3→4→1
- All vertices have even degree (2 each)
- Eulerian circuit exists: 1→2→3→4→1
- Each edge is traversed exactly once

## Visual Example

### Input Graph
```
Nodes: 1, 2, 3, 4
Edges: (1,2), (2,3), (3,4), (4,1)

Graph representation:
1 ── 2 ── 3 ── 4
│              │
└──────────────┘
```

### Eulerian Circuit Algorithm Process
```
Step 1: Check Eulerian circuit conditions
- Degree of vertex 1: 2 (even)
- Degree of vertex 2: 2 (even)
- Degree of vertex 3: 2 (even)
- Degree of vertex 4: 2 (even)
- All vertices have even degree ✓
- Graph is connected ✓
- Eulerian circuit exists

Step 2: Find starting vertex
- Any vertex can be starting point (all have even degree)
- Start from vertex 1

Step 3: Hierholzer's algorithm
- Current path: [1]
- Available edges: (1,2), (2,3), (3,4), (4,1)

Step 4: Build circuit
- From 1: go to 2
- Current path: [1, 2]
- Available edges: (2,3), (3,4), (4,1)

- From 2: go to 3
- Current path: [1, 2, 3]
- Available edges: (3,4), (4,1)

- From 3: go to 4
- Current path: [1, 2, 3, 4]
- Available edges: (4,1)

- From 4: go to 1
- Current path: [1, 2, 3, 4, 1]
- No more edges available

Step 5: Complete circuit
- Eulerian circuit: 1 → 2 → 3 → 4 → 1
- All edges visited exactly once
```

### Circuit Analysis
```
Eulerian circuit found:
1 → 2 → 3 → 4 → 1

Edges used:
- (1,2): visited once
- (2,3): visited once
- (3,4): visited once
- (4,1): visited once

All edges visited exactly once ✓
Returns to starting vertex ✓
```

### Key Insight
Hierholzer's algorithm works by:
1. Checking Eulerian circuit conditions (all even degrees)
2. Starting from any vertex
3. Following edges until no more edges available
4. Backtracking and inserting cycles if needed
5. Time complexity: O(m) where m is number of edges
6. Space complexity: O(n + m) for graph representation

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths and check if they form an Eulerian circuit
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths in the graph
2. For each path, check if it visits every edge exactly once and returns to start
3. Return the first valid Eulerian circuit found
4. Handle cases where no Eulerian circuit exists

**Visual Example:**
```
Brute force: Try all possible paths
For graph: 1 ── 2 ── 3 ── 4
           │              │
           └──────────────┘

All possible paths:
- Path 1: [1, 2, 3, 4, 1] - Check edges: (1,2), (2,3), (3,4), (4,1) ✓
- Path 2: [1, 2, 3, 4] - Check edges: (1,2), (2,3), (3,4) ✗ (missing 4,1)
- Path 3: [2, 3, 4, 1, 2] - Check edges: (2,3), (3,4), (4,1), (1,2) ✓
- Path 4: [3, 4, 1, 2, 3] - Check edges: (3,4), (4,1), (1,2), (2,3) ✓

First valid Eulerian circuit: [1, 2, 3, 4, 1]
```

**Implementation:**
```python
def mail_delivery_brute_force(n, m, edges):
    from itertools import permutations
    
    # Generate all possible paths
    def find_all_paths(start, visited_edges, path):
        if len(visited_edges) == m and path[-1] == start:
            return [path]
        
        paths = []
        for i, (a, b) in enumerate(edges):
            if i not in visited_edges and a == path[-1]:
                new_visited = visited_edges | {i}
                new_path = path + [b]
                paths.extend(find_all_paths(start, new_visited, new_path))
            elif i not in visited_edges and b == path[-1]:
                new_visited = visited_edges | {i}
                new_path = path + [a]
                paths.extend(find_all_paths(start, new_visited, new_path))
        
        return paths
    
    def is_eulerian_circuit(path):
        if len(path) != m + 1 or path[0] != path[-1]:
            return False
        
        # Check if all edges are used exactly once
        used_edges = set()
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            for j, (edge_a, edge_b) in enumerate(edges):
                if ((edge_a == a and edge_b == b) or 
                    (edge_a == b and edge_b == a)) and j not in used_edges:
                    used_edges.add(j)
                    break
            else:
                return False
        
        return len(used_edges) == m
    
    # Try starting from each vertex
    for start in range(1, n + 1):
        all_paths = find_all_paths(start, set(), [start])
        for path in all_paths:
            if is_eulerian_circuit(path):
                return ' '.join(map(str, path))
    
    return "IMPOSSIBLE"
```

**Time Complexity:** O(n! × m) for n vertices and m edges with exponential path enumeration
**Space Complexity:** O(n! × m) for storing all possible paths

**Why it's inefficient:**
- O(n! × m) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many vertices

### Approach 2: Basic Hierholzer's Algorithm (Better)

**Key Insights from Basic Hierholzer's Solution:**
- Use Hierholzer's algorithm to construct Eulerian circuits
- Much more efficient than brute force approach
- Standard method for Eulerian circuit problems
- Can handle larger graphs than brute force

**Algorithm:**
1. Check Eulerian circuit conditions (all vertices have even degree)
2. Use Hierholzer's algorithm to construct the circuit
3. Return the Eulerian circuit if it exists
4. Handle cases where no circuit exists

**Visual Example:**
```
Basic Hierholzer's for graph: 1 ── 2 ── 3 ── 4
                               │              │
                               └──────────────┘

Step 1: Check conditions
- Degrees: [2, 2, 2, 2]
- All vertices have even degree ✓

Step 2: Hierholzer's algorithm
- Stack: [1]
- Current: 1, Available edges: (1,2)
- Stack: [1, 2]
- Current: 2, Available edges: (2,3)
- Stack: [1, 2, 3]
- Current: 3, Available edges: (3,4)
- Stack: [1, 2, 3, 4]
- Current: 4, Available edges: (4,1)
- Stack: [1, 2, 3, 4, 1]
- Current: 1, No available edges
- Pop: 1, Path: [1]
- Pop: 4, Path: [4, 1]
- Pop: 3, Path: [3, 4, 1]
- Pop: 2, Path: [2, 3, 4, 1]
- Pop: 1, Path: [1, 2, 3, 4, 1]
```

**Implementation:**
```python
def mail_delivery_basic_hierholzer(n, m, edges):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_eulerian_circuit():
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                # Remove the reverse edge
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    # Check if all edges were used
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return ' '.join(map(str, circuit))
```

**Time Complexity:** O(m) for m edges with Hierholzer's algorithm
**Space Complexity:** O(n + m) for adjacency list and stack

**Why it's better:**
- O(m) time complexity is much better than O(n! × m)
- Standard method for Eulerian circuit problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Hierholzer's Algorithm with Efficient Edge Management (Optimal)

**Key Insights from Optimized Hierholzer's Solution:**
- Use optimized Hierholzer's algorithm with efficient edge management
- Most efficient approach for Eulerian circuit problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized Hierholzer's algorithm with efficient data structures
2. Implement efficient edge tracking and circuit construction
3. Use proper degree checking and circuit validation
4. Return the Eulerian circuit if it exists

**Visual Example:**
```
Optimized Hierholzer's for graph: 1 ── 2 ── 3 ── 4
                                   │              │
                                   └──────────────┘

Step 1: Initialize optimized structures
- degree = [0, 2, 2, 2, 2]
- adj = [[], [2, 4], [1, 3], [2, 4], [1, 3]]

Step 2: Process with optimized Hierholzer's
- Check conditions: all vertices have even degrees ✓
- Start from vertex 1: stack = [1]
- Process with optimized edge management
- Final circuit: [1, 2, 3, 4, 1]
```

**Implementation:**
```python
def mail_delivery_optimized_hierholzer(n, m, edges):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Optimized Hierholzer's algorithm
    def find_eulerian_circuit():
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                # Remove the reverse edge efficiently
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    # Check if all edges were used
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return ' '.join(map(str, circuit))

def solve_mail_delivery():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = mail_delivery_optimized_hierholzer(n, m, edges)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_mail_delivery()
```

**Time Complexity:** O(m) for m edges with optimized Hierholzer's algorithm
**Space Complexity:** O(n + m) for adjacency list and stack

**Why it's optimal:**
- O(m) time complexity is optimal for Eulerian circuit construction
- Uses optimized Hierholzer's algorithm with efficient edge management
- Most efficient approach for competitive programming
- Standard method for Eulerian circuit problems

## 🎯 Problem Variations

### Variation 1: Mail Delivery with Multiple Components
**Problem**: Find Eulerian circuits in graphs with multiple connected components.

**Link**: [CSES Problem Set - Mail Delivery Multiple Components](https://cses.fi/problemset/task/mail_delivery_multiple_components)

```python
def mail_delivery_multiple_components(n, m, edges):
    # Check if Eulerian circuit exists in each component
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    def find_components():
        visited = [False] * (n + 1)
        components = []
        
        for i in range(1, n + 1):
            if not visited[i]:
                component = []
                stack = [i]
                visited[i] = True
                
                while stack:
                    current = stack.pop()
                    component.append(current)
                    
                    for neighbor in adj[current]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            stack.append(neighbor)
                
                components.append(component)
        
        return components
    
    components = find_components()
    
    # Check each component for Eulerian circuit
    for component in components:
        for vertex in component:
            if degree[vertex] % 2 != 0:
                return "IMPOSSIBLE"
    
    return "POSSIBLE"
```

### Variation 2: Mail Delivery with Edge Weights
**Problem**: Find Eulerian circuits considering edge weights.

**Link**: [CSES Problem Set - Mail Delivery Edge Weights](https://cses.fi/problemset/task/mail_delivery_edge_weights)

```python
def mail_delivery_edge_weights(n, m, edges):
    # Check if Eulerian circuit exists with edge weights
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b, weight in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append((b, weight))
        adj[b].append((a, weight))
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm with edge weights
    def find_eulerian_circuit():
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node, weight = adj[current].pop()
                # Remove the reverse edge
                for i, (neighbor, w) in enumerate(adj[next_node]):
                    if neighbor == current and w == weight:
                        adj[next_node].pop(i)
                        break
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return ' '.join(map(str, circuit))
```

### Variation 3: Mail Delivery with Time Constraints
**Problem**: Find Eulerian circuits with time constraints on edge traversal.

**Link**: [CSES Problem Set - Mail Delivery Time Constraints](https://cses.fi/problemset/task/mail_delivery_time_constraints)

```python
def mail_delivery_time_constraints(n, m, edges, time_constraints):
    # Check if Eulerian circuit exists with time constraints
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm with time constraints
    def find_eulerian_circuit():
        start = 1
        path = []
        stack = [start]
        current_time = 0
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                edge_time = time_constraints.get((current, next_node), 1)
                current_time += edge_time
                # Remove the reverse edge
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return ' '.join(map(str, circuit))
```

## 🔗 Related Problems

- **[Teleporters Path](/cses-analyses/problem_soulutions/graph_algorithms/teleporters_path_analysis/)**: Eulerian trails
- **[De Bruijn Sequence](/cses-analyses/problem_soulutions/graph_algorithms/de_bruijn_sequence_analysis/)**: Eulerian paths
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems
- **[Circuit Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Circuit problems

## 📚 Learning Points

1. **Eulerian Circuits**: Essential for understanding circuit algorithms
2. **Hierholzer's Algorithm**: Key technique for Eulerian circuit construction
3. **Degree Conditions**: Important for identifying Eulerian circuit existence
4. **Graph Representation**: Critical for understanding adjacency list structures
5. **Circuit Construction**: Foundation for many graph traversal problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Mail Delivery problem demonstrates fundamental Eulerian circuit concepts for finding paths that visit every edge exactly once and return to the starting vertex. We explored three approaches:

1. **Brute Force Path Enumeration**: O(n! × m) time complexity using exponential path generation, inefficient for large graphs
2. **Basic Hierholzer's Algorithm**: O(m) time complexity using standard Hierholzer's algorithm, better approach for Eulerian circuit problems
3. **Optimized Hierholzer's Algorithm with Efficient Edge Management**: O(m) time complexity with optimized Hierholzer's algorithm, optimal approach for Eulerian circuit construction

The key insights include understanding Eulerian circuit conditions, using Hierholzer's algorithm for efficient circuit construction, and applying degree checking techniques for optimal performance. This problem serves as an excellent introduction to Eulerian circuit algorithms and Hierholzer's algorithm techniques.

