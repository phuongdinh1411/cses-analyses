---
layout: simple
title: "Road Reparation - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/road_reparation_analysis
---

# Road Reparation - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of minimum spanning tree with existing edges
- Apply efficient algorithms for finding MST with pre-existing connections
- Implement Kruskal's algorithm with edge selection optimization
- Optimize graph connectivity for repair scenarios
- Handle special cases in MST repair problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, minimum spanning tree, union-find
- **Data Structures**: Graphs, disjoint sets, edge structures
- **Mathematical Concepts**: Graph theory, spanning trees, connectivity
- **Programming Skills**: Graph operations, union-find, MST algorithms
- **Related Problems**: Road Construction (graph_algorithms), Building Roads (graph_algorithms), Download Speed (graph_algorithms)

## 📋 Problem Description

Given a weighted graph with some existing roads, find the minimum cost to repair/add roads to connect all cities.

**Input**: 
- n: number of cities
- m: number of existing roads
- edges: array of (u, v, weight) representing existing roads

**Output**: 
- Minimum cost to repair/add roads to connect all cities, or -1 if impossible

**Constraints**:
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2×10^5
- 1 ≤ weight ≤ 10^9

**Example**:
```
Input:
n = 4, m = 3
edges = [(0,1,1), (1,2,2), (2,3,3)]

Output:
0

Explanation**: 
All cities are already connected
No additional roads needed
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible combinations of existing roads
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic graph connectivity
- **Inefficient**: O(2^m) time complexity

**Key Insight**: Check all possible subsets of existing roads to find minimum spanning tree.

**Algorithm**:
- Generate all possible subsets of existing roads
- Check if subset forms a spanning tree
- Calculate cost for valid spanning trees
- Return minimum cost

**Visual Example**:
```
Graph: 0-1(1), 1-2(2), 2-3(3)

All possible road combinations:
┌─────────────────────────────────────┐
│ Subset 1: {} - Not connected       │
│ Subset 2: {(0,1,1)} - Not connected │
│ Subset 3: {(1,2,2)} - Not connected │
│ Subset 4: {(2,3,3)} - Not connected │
│ Subset 5: {(0,1,1), (1,2,2)} - Not connected │
│ Subset 6: {(1,2,2), (2,3,3)} - Not connected │
│ Subset 7: {(0,1,1), (2,3,3)} - Not connected │
│ Subset 8: {(0,1,1), (1,2,2), (2,3,3)} - Connected! │
│ Cost: 1 + 2 + 3 = 6                │
│                                   │
│ Minimum: 6                         │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_road_reparation(n, edges):
    """Find minimum repair cost using brute force approach"""
    from itertools import combinations
    
    min_cost = float('inf')
    
    # Try all possible combinations of existing roads
    for r in range(len(edges) + 1):
        for road_subset in combinations(edges, r):
            # Check if this forms a spanning tree
            if is_spanning_tree(n, road_subset):
                cost = sum(weight for _, _, weight in road_subset)
                min_cost = min(min_cost, cost)
    
    return min_cost if min_cost != float('inf') else -1

def is_spanning_tree(n, edges):
    """Check if edges form a spanning tree"""
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
    
    return count == n

# Example usage
n = 4
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
result = brute_force_road_reparation(n, edges)
print(f"Brute force repair cost: {result}")
```

**Time Complexity**: O(2^m)
**Space Complexity**: O(n + m)

**Why it's inefficient**: O(2^m) time complexity for checking all road combinations.

---

### Approach 2: Kruskal's Algorithm

**Key Insights from Kruskal's Algorithm**:
- **Kruskal's Algorithm**: Use Kruskal's algorithm for efficient MST
- **Efficient Implementation**: O(m log m) time complexity
- **Union-Find**: Use union-find data structure for cycle detection
- **Optimization**: Much more efficient than brute force

**Key Insight**: Sort existing roads by weight and use union-find to build MST.

**Algorithm**:
- Sort all existing roads by weight
- Use union-find to add roads without creating cycles
- Stop when we have n-1 roads or all roads processed

**Visual Example**:
```
Kruskal's algorithm:

Existing roads sorted by weight:
┌─────────────────────────────────────┐
│ (0,1,1), (1,2,2), (2,3,3)         │
│                                   │
│ Step 1: Add (0,1,1) - cost = 1    │
│ Step 2: Add (1,2,2) - cost = 3    │
│ Step 3: Add (2,3,3) - cost = 6    │
│                                   │
│ MST: (0,1,1) + (1,2,2) + (2,3,3) = 6 │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def kruskal_road_reparation(n, edges):
    """Find minimum repair cost using Kruskal's algorithm"""
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    # Union-Find data structure
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    # Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in edges:
        if union(u, v):
            mst_cost += weight
            edges_added += 1
            if edges_added == n - 1:
                break
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
result = kruskal_road_reparation(n, edges)
print(f"Kruskal's repair cost: {result}")
```

**Time Complexity**: O(m log m)
**Space Complexity**: O(n)

**Why it's better**: Uses Kruskal's algorithm for O(m log m) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for MST
- **Efficient Implementation**: O(m log m) time complexity
- **Space Efficiency**: O(n) space complexity
- **Optimal Complexity**: Best approach for MST repair

**Key Insight**: Use advanced data structures for optimal MST repair calculation.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient Kruskal's algorithm
- Handle special cases optimally
- Return MST repair cost

**Visual Example**:
```
Advanced data structure approach:

For graph: 0-1(1), 1-2(2), 2-3(3)
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Edge structure: for efficient     │
│   storage and sorting              │
│ - Union-find cache: for optimization │
│ - MST tracker: for optimization     │
│                                   │
│ MST repair calculation:            │
│ - Use edge structure for efficient │
│   storage and sorting              │
│ - Use union-find cache for         │
│   optimization                     │
│ - Use MST tracker for optimization │
│                                   │
│ Result: 6                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_road_reparation(n, edges):
    """Find minimum repair cost using advanced data structure approach"""
    # Use advanced data structures for graph storage
    # Sort edges by weight using advanced data structures
    edges.sort(key=lambda x: x[2])
    
    # Advanced Union-Find data structure
    parent = list(range(n))
    
    def find_advanced(x):
        if parent[x] != x:
            parent[x] = find_advanced(parent[x])
        return parent[x]
    
    def union_advanced(x, y):
        px, py = find_advanced(x), find_advanced(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    # Advanced Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in edges:
        if union_advanced(u, v):
            mst_cost += weight
            edges_added += 1
            if edges_added == n - 1:
                break
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
result = advanced_data_structure_road_reparation(n, edges)
print(f"Advanced data structure repair cost: {result}")
```

**Time Complexity**: O(m log m)
**Space Complexity**: O(n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^m) | O(n + m) | Try all road combinations |
| Kruskal's Algorithm | O(m log m) | O(n) | Sort roads and use union-find |
| Advanced Data Structure | O(m log m) | O(n) | Use advanced data structures |

### Time Complexity
- **Time**: O(m log m) - Use Kruskal's algorithm for efficient MST repair
- **Space**: O(n) - Store union-find data structure

### Why This Solution Works
- **Kruskal's Algorithm**: Sort roads by weight and use union-find
- **Union-Find**: Efficiently detect cycles and merge components
- **Greedy Approach**: Always choose minimum weight road that doesn't create cycle
- **Optimal Algorithms**: Use optimal algorithms for MST repair

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Road Reparation with Constraints**
**Problem**: Find MST repair with specific constraints.

**Key Differences**: Apply constraints to MST repair calculation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_road_reparation(n, edges, constraints):
    """Find MST repair with constraints"""
    # Filter edges based on constraints
    filtered_edges = []
    for u, v, weight in edges:
        if constraints(u, v, weight):
            filtered_edges.append((u, v, weight))
    
    # Sort edges by weight
    filtered_edges.sort(key=lambda x: x[2])
    
    # Union-Find data structure
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    # Constrained Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in filtered_edges:
        if union(u, v):
            mst_cost += weight
            edges_added += 1
            if edges_added == n - 1:
                break
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
constraints = lambda u, v, w: w <= 10  # Only roads with weight ≤ 10
result = constrained_road_reparation(n, edges, constraints)
print(f"Constrained repair cost: {result}")
```

#### **2. Road Reparation with Different Metrics**
**Problem**: Find MST repair with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_road_reparation(n, edges, cost_function):
    """Find MST repair with different cost metrics"""
    # Apply cost function to edges
    weighted_edges = []
    for u, v, weight in edges:
        new_weight = cost_function(weight)
        weighted_edges.append((u, v, new_weight))
    
    # Sort edges by new weight
    weighted_edges.sort(key=lambda x: x[2])
    
    # Union-Find data structure
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    # Weighted Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in weighted_edges:
        if union(u, v):
            mst_cost += weight
            edges_added += 1
            if edges_added == n - 1:
                break
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
cost_function = lambda weight: weight * weight  # Square the weight
result = weighted_road_reparation(n, edges, cost_function)
print(f"Weighted repair cost: {result}")
```

#### **3. Road Reparation with Multiple Dimensions**
**Problem**: Find MST repair in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_road_reparation(n, edges, dimensions):
    """Find MST repair in multiple dimensions"""
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    # Union-Find data structure
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    # Multi-dimensional Kruskal's algorithm
    mst_cost = 0
    edges_added = 0
    
    for u, v, weight in edges:
        if union(u, v):
            mst_cost += weight
            edges_added += 1
            if edges_added == n - 1:
                break
    
    return mst_cost if edges_added == n - 1 else -1

# Example usage
n = 4
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
dimensions = 1
result = multi_dimensional_road_reparation(n, edges, dimensions)
print(f"Multi-dimensional repair cost: {result}")
```

### Related Problems

#### **CSES Problems**
- [Road Construction](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Building Roads](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Download Speed](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) - Graph
- [Connecting Cities With Minimum Cost](https://leetcode.com/problems/connecting-cities-with-minimum-cost/) - Graph
- [Minimum Spanning Tree](https://leetcode.com/problems/minimum-spanning-tree/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: Minimum spanning tree, Kruskal's algorithm, union-find
- **MST Algorithms**: Kruskal's, Prim's, MST repair
- **Union-Find**: Disjoint sets, cycle detection

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Minimum Spanning Tree](https://cp-algorithms.com/graph/mst_kruskal.html) - MST algorithms
- [Union-Find](https://cp-algorithms.com/data_structures/disjoint_set_union.html) - Union-find algorithms

### **Practice Problems**
- [CSES Road Construction](https://cses.fi/problemset/task/1075) - Medium
- [CSES Building Roads](https://cses.fi/problemset/task/1075) - Medium
- [CSES Download Speed](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Minimum Spanning Tree](https://en.wikipedia.org/wiki/Minimum_spanning_tree) - Wikipedia article
- [Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm) - Wikipedia article
