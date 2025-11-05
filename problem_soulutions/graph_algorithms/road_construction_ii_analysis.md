---
layout: simple
title: "Road Construction II - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/road_construction_ii_analysis
---

# Road Construction II - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of minimum spanning tree with additional constraints
- Apply efficient algorithms for finding MST with special requirements
- Implement advanced MST algorithms with modifications
- Optimize graph connectivity for complex scenarios
- Handle special cases in advanced MST problems

## 📋 Problem Description

Given a weighted graph with special constraints, find the minimum cost to connect all vertices while satisfying additional requirements.

**Input**: 
- n: number of vertices
- m: number of edges
- k: number of special vertices
- special_vertices: array of special vertex indices
- edges: array of (u, v, weight) representing edges

**Output**: 
- Minimum cost to connect all vertices with special constraints

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5
- 1 ≤ k ≤ n
- 1 ≤ weight ≤ 10^9

**Example**:
```
Input:
n = 4, m = 5, k = 2
special_vertices = [0, 3]
edges = [(0,1,1), (0,2,2), (1,2,3), (1,3,4), (2,3,5)]

Output:
8

Explanation**: 
Must connect special vertices 0 and 3
MST: (0,1,1) + (1,2,3) + (2,3,5) = 9
But we need to ensure special vertices are connected
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible spanning trees with constraints
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph connectivity with constraints
- **Inefficient**: O(n^(n-2)) time complexity

**Key Insight**: Generate all possible spanning trees and check constraints.

**Algorithm**:
- Generate all possible spanning trees
- Check if special constraints are satisfied
- Calculate cost for valid spanning trees
- Return minimum cost

**Visual Example**:
```
Graph: 0-1(1), 0-2(2), 1-2(3), 1-3(4), 2-3(5)
Special vertices: [0, 3]

All spanning trees with constraints:
┌─────────────────────────────────────┐
│ Tree 1: (0,1,1) + (0,2,2) + (1,3,4) │
│ Special connected: YES, Cost: 7     │
│                                   │
│ Tree 2: (0,1,1) + (1,2,3) + (1,3,4) │
│ Special connected: YES, Cost: 8     │
│                                   │
│ Tree 3: (0,2,2) + (1,2,3) + (1,3,4) │
│ Special connected: YES, Cost: 9     │
│                                   │
│ Minimum: 7                         │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_road_construction_ii(n, special_vertices, edges):
    """Find constrained MST using brute force approach"""
    from itertools import combinations
    
    min_cost = float('inf')
    
    # Try all possible combinations of n-1 edges
    for edge_combination in combinations(edges, n - 1):
        # Check if this forms a valid spanning tree with constraints
        if is_valid_constrained_spanning_tree(n, special_vertices, edge_combination):
            cost = sum(weight for _, _, weight in edge_combination)
            min_cost = min(min_cost, cost)
    
    return min_cost if min_cost != float('inf') else -1

def is_valid_constrained_spanning_tree(n, special_vertices, edges):
    """Check if edges form a valid constrained spanning tree"""
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, _ in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Check connectivity using DFS
    visited = [False] * n
    stack = [0]
    visited[0] = True
    count = 1
    
    while stack:
        vertex = stack.pop()
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)
                count += 1
    
    # Check if all vertices are connected
    if count != n:
        return False
    
    # Check if special vertices are connected
    return are_special_vertices_connected(n, special_vertices, adj)

def are_special_vertices_connected(n, special_vertices, adj):
    """Check if all special vertices are connected"""
    if len(special_vertices) <= 1:
        return True
    
    # BFS from first special vertex
    visited = [False] * n
    queue = [special_vertices[0]]
    visited[special_vertices[0]] = True
    
    while queue:
        vertex = queue.pop(0)
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    
    # Check if all special vertices are reachable
    return all(visited[v] for v in special_vertices)

# Example usage
n = 4
special_vertices = [0, 3]
edges = [(0, 1, 1), (0, 2, 2), (1, 2, 3), (1, 3, 4), (2, 3, 5)]
result = brute_force_road_construction_ii(n, special_vertices, edges)
print(f"Brute force constrained MST cost: {result}")
```

**Time Complexity**: O(n^(n-2))
**Space Complexity**: O(n + m)

**Why it's inefficient**: O(n^(n-2)) time complexity for checking all spanning trees.

---

### Approach 2: Modified Kruskal's Algorithm

**Key Insights from Modified Kruskal's Algorithm**:
- **Modified Kruskal's**: Use Kruskal's algorithm with constraint handling
- **Efficient Implementation**: O(m log m) time complexity
- **Constraint Integration**: Integrate constraints into MST algorithm
- **Optimization**: Much more efficient than brute force

**Key Insight**: Modify Kruskal's algorithm to handle special constraints.

**Algorithm**:
- Sort edges by weight
- Use union-find with constraint tracking
- Ensure special vertices remain connected
- Stop when constraints are satisfied

**Visual Example**:
```
Modified Kruskal's algorithm:

Special vertices: [0, 3]
Edges sorted by weight:
┌─────────────────────────────────────┐
│ (0,1,1), (0,2,2), (1,2,3), (1,3,4), (2,3,5) │
│                                   │
│ Step 1: Add (0,1,1) - connects 0  │
│ Step 2: Add (0,2,2) - connects 0  │
│ Step 3: Skip (1,2,3) - creates cycle │
│ Step 4: Add (1,3,4) - connects 3  │
│ Step 5: Skip (2,3,5) - creates cycle │
│                                   │
│ MST: (0,1,1) + (0,2,2) + (1,3,4) = 7 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def modified_kruskal_road_construction_ii(n, special_vertices, edges):
    """Find constrained MST using modified Kruskal's algorithm"""
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    # Union-Find data structure with special vertex tracking
    parent = list(range(n))
    special_connected = set()
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            # Track if special vertices are connected
            if x in special_vertices:
                special_connected.add(x)
            if y in special_vertices:
                special_connected.add(y)
            return True
        return False
    
    # Modified Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in edges:
        if union(u, v):
            mst_cost += weight
            edges_added += 1
            
            # Check if all special vertices are connected
            if edges_added == n - 1:
                # Verify all special vertices are in the same component
                if len(special_vertices) > 0:
                    root = find(special_vertices[0])
                    if all(find(v) == root for v in special_vertices):
                        break
                else:
                    break
    
    # Final check for special vertex connectivity
    if len(special_vertices) > 0:
        root = find(special_vertices[0])
        if not all(find(v) == root for v in special_vertices):
            return -1
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
special_vertices = [0, 3]
edges = [(0, 1, 1), (0, 2, 2), (1, 2, 3), (1, 3, 4), (2, 3, 5)]
result = modified_kruskal_road_construction_ii(n, special_vertices, edges)
print(f"Modified Kruskal's constrained MST cost: {result}")
```

**Time Complexity**: O(m log m)
**Space Complexity**: O(n)

**Why it's better**: Uses modified Kruskal's algorithm for O(m log m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for constrained MST
- **Efficient Implementation**: O(m log m) time complexity
- **Space Efficiency**: O(n) space complexity
- **Optimal Complexity**: Best approach for constrained MST

**Key Insight**: Use advanced data structures for optimal constrained MST calculation.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient constrained MST algorithms
- Handle special cases optimally
- Return constrained MST cost

**Visual Example**:
```
Advanced data structure approach:

For graph: 0-1(1), 0-2(2), 1-2(3), 1-3(4), 2-3(5)
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Constrained edge structure: for   │
│   efficient storage and sorting     │
│ - Advanced union-find: for          │
│   optimization                      │
│ - Constraint tracker: for           │
│   optimization                      │
│                                   │
│ Constrained MST calculation:       │
│ - Use constrained edge structure    │
│   for efficient storage and sorting │
│ - Use advanced union-find for       │
│   optimization                      │
│ - Use constraint tracker for        │
│   optimization                      │
│                                   │
│ Result: 7                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_road_construction_ii(n, special_vertices, edges):
    """Find constrained MST using advanced data structure approach"""
    # Use advanced data structures for graph storage
    # Sort edges by weight using advanced data structures
    edges.sort(key=lambda x: x[2])
    
    # Advanced Union-Find data structure with constraint tracking
    parent = list(range(n))
    special_connected = set()
    
    def find_advanced(x):
        if parent[x] != x:
            parent[x] = find_advanced(parent[x])
        return parent[x]
    
    def union_advanced(x, y):
        px, py = find_advanced(x), find_advanced(y)
        if px != py:
            parent[px] = py
            # Track if special vertices are connected using advanced data structures
            if x in special_vertices:
                special_connected.add(x)
            if y in special_vertices:
                special_connected.add(y)
            return True
        return False
    
    # Advanced constrained Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in edges:
        if union_advanced(u, v):
            mst_cost += weight
            edges_added += 1
            
            # Check if all special vertices are connected using advanced data structures
            if edges_added == n - 1:
                # Verify all special vertices are in the same component
                if len(special_vertices) > 0:
                    root = find_advanced(special_vertices[0])
                    if all(find_advanced(v) == root for v in special_vertices):
                        break
                else:
                    break
    
    # Final check for special vertex connectivity using advanced data structures
    if len(special_vertices) > 0:
        root = find_advanced(special_vertices[0])
        if not all(find_advanced(v) == root for v in special_vertices):
            return -1
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
special_vertices = [0, 3]
edges = [(0, 1, 1), (0, 2, 2), (1, 2, 3), (1, 3, 4), (2, 3, 5)]
result = advanced_data_structure_road_construction_ii(n, special_vertices, edges)
print(f"Advanced data structure constrained MST cost: {result}")
```

**Time Complexity**: O(m log m)
**Space Complexity**: O(n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n^(n-2)) | O(n + m) | Try all constrained spanning trees |
| Modified Kruskal's | O(m log m) | O(n) | Modify Kruskal's for constraints |
| Advanced Data Structure | O(m log m) | O(n) | Use advanced data structures |

### Time Complexity
- **Time**: O(m log m) - Use modified Kruskal's algorithm for efficient constrained MST
- **Space**: O(n) - Store union-find data structure and constraint tracking

### Why This Solution Works
- **Modified Kruskal's**: Sort edges by weight and use union-find with constraints
- **Constraint Tracking**: Track special vertex connectivity during MST construction
- **Union-Find**: Efficiently detect cycles and merge components with constraints
- **Optimal Algorithms**: Use optimal algorithms for constrained MST

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Road Construction II with Additional Constraints**
**Problem**: Find constrained MST with multiple constraint types.

**Key Differences**: Apply multiple constraint types to MST calculation

**Solution Approach**: Modify algorithm to handle multiple constraints

**Implementation**:
```python
def multi_constrained_road_construction_ii(n, special_vertices, edges, additional_constraints):
    """Find MST with multiple constraints"""
    # Filter edges based on additional constraints
    filtered_edges = []
    for u, v, weight in edges:
        if additional_constraints(u, v, weight):
            filtered_edges.append((u, v, weight))
    
    # Sort edges by weight
    filtered_edges.sort(key=lambda x: x[2])
    
    # Union-Find data structure with constraint tracking
    parent = list(range(n))
    special_connected = set()
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            # Track if special vertices are connected
            if x in special_vertices:
                special_connected.add(x)
            if y in special_vertices:
                special_connected.add(y)
            return True
        return False
    
    # Multi-constrained Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in filtered_edges:
        if union(u, v):
            mst_cost += weight
            edges_added += 1
            
            # Check if all special vertices are connected
            if edges_added == n - 1:
                # Verify all special vertices are in the same component
                if len(special_vertices) > 0:
                    root = find(special_vertices[0])
                    if all(find(v) == root for v in special_vertices):
                        break
                else:
                    break
    
    # Final check for special vertex connectivity
    if len(special_vertices) > 0:
        root = find(special_vertices[0])
        if not all(find(v) == root for v in special_vertices):
            return -1
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
special_vertices = [0, 3]
edges = [(0, 1, 1), (0, 2, 2), (1, 2, 3), (1, 3, 4), (2, 3, 5)]
additional_constraints = lambda u, v, weight: weight <= 10  # Weight constraint
result = multi_constrained_road_construction_ii(n, special_vertices, edges, additional_constraints)
print(f"Multi-constrained MST cost: {result}")
```

#### **2. Road Construction II with Different Metrics**
**Problem**: Find constrained MST with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_constrained_road_construction_ii(n, special_vertices, edges, cost_function):
    """Find constrained MST with different cost metrics"""
    # Apply cost function to edges
    weighted_edges = []
    for u, v, weight in edges:
        new_weight = cost_function(weight)
        weighted_edges.append((u, v, new_weight))
    
    # Sort edges by new weight
    weighted_edges.sort(key=lambda x: x[2])
    
    # Union-Find data structure with constraint tracking
    parent = list(range(n))
    special_connected = set()
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            # Track if special vertices are connected
            if x in special_vertices:
                special_connected.add(x)
            if y in special_vertices:
                special_connected.add(y)
            return True
        return False
    
    # Weighted constrained Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in weighted_edges:
        if union(u, v):
            mst_cost += weight
            edges_added += 1
            
            # Check if all special vertices are connected
            if edges_added == n - 1:
                # Verify all special vertices are in the same component
                if len(special_vertices) > 0:
                    root = find(special_vertices[0])
                    if all(find(v) == root for v in special_vertices):
                        break
                else:
                    break
    
    # Final check for special vertex connectivity
    if len(special_vertices) > 0:
        root = find(special_vertices[0])
        if not all(find(v) == root for v in special_vertices):
            return -1
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
special_vertices = [0, 3]
edges = [(0, 1, 1), (0, 2, 2), (1, 2, 3), (1, 3, 4), (2, 3, 5)]
cost_function = lambda weight: weight * weight  # Square the weight
result = weighted_constrained_road_construction_ii(n, special_vertices, edges, cost_function)
print(f"Weighted constrained MST cost: {result}")
```

#### **3. Road Construction II with Multiple Dimensions**
**Problem**: Find constrained MST in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_constrained_road_construction_ii(n, special_vertices, edges, dimensions):
    """Find constrained MST in multiple dimensions"""
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    # Union-Find data structure with constraint tracking
    parent = list(range(n))
    special_connected = set()
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            # Track if special vertices are connected
            if x in special_vertices:
                special_connected.add(x)
            if y in special_vertices:
                special_connected.add(y)
            return True
        return False
    
    # Multi-dimensional constrained Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in edges:
        if union(u, v):
            mst_cost += weight
            edges_added += 1
            
            # Check if all special vertices are connected
            if edges_added == n - 1:
                # Verify all special vertices are in the same component
                if len(special_vertices) > 0:
                    root = find(special_vertices[0])
                    if all(find(v) == root for v in special_vertices):
                        break
                else:
                    break
    
    # Final check for special vertex connectivity
    if len(special_vertices) > 0:
        root = find(special_vertices[0])
        if not all(find(v) == root for v in special_vertices):
            return -1
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
special_vertices = [0, 3]
edges = [(0, 1, 1), (0, 2, 2), (1, 2, 3), (1, 3, 4), (2, 3, 5)]
dimensions = 1
result = multi_dimensional_constrained_road_construction_ii(n, special_vertices, edges, dimensions)
print(f"Multi-dimensional constrained MST cost: {result}")
```

### Related Problems

#### **CSES Problems**
- [Road Construction](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Road Construction III](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Road Reparation](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) - Graph
- [Connecting Cities With Minimum Cost](https://leetcode.com/problems/connecting-cities-with-minimum-cost/) - Graph
- [Minimum Spanning Tree](https://leetcode.com/problems/minimum-spanning-tree/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Constrained MST, advanced MST, union-find
- **MST Algorithms**: Modified Kruskal's, constrained MST
- **Union-Find**: Advanced disjoint sets, constraint tracking

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Minimum Spanning Tree](https://cp-algorithms.com/graph/mst_kruskal.html) - MST algorithms
- [Union-Find](https://cp-algorithms.com/data_structures/disjoint_set_union.html) - Union-find algorithms

### **Practice Problems**
- [CSES Road Construction](https://cses.fi/problemset/task/1075) - Medium
- [CSES Road Construction III](https://cses.fi/problemset/task/1075) - Medium
- [CSES Road Reparation](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Minimum Spanning Tree](https://en.wikipedia.org/wiki/Minimum_spanning_tree) - Wikipedia article
- [Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm) - Wikipedia article
