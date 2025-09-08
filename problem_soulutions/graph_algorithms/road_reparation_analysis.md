---
layout: simple
title: "Road Reparation - Minimum Spanning Tree"
permalink: /problem_soulutions/graph_algorithms/road_reparation_analysis
---

# Road Reparation - Minimum Spanning Tree

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand minimum spanning tree problems and road repair optimization concepts
- Apply Kruskal's algorithm or Prim's algorithm to find minimum cost spanning trees
- Implement efficient MST algorithms with proper Union-Find data structure usage
- Optimize MST solutions using Union-Find and graph representations
- Handle edge cases in MST problems (impossible connectivity, single node, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Kruskal's algorithm, Prim's algorithm, minimum spanning trees, Union-Find, MST algorithms
- **Data Structures**: Union-Find, priority queues, edge lists, graph representations
- **Mathematical Concepts**: Graph theory, minimum spanning trees, greedy algorithms, optimization
- **Programming Skills**: Union-Find implementation, edge sorting, MST algorithms, algorithm implementation
- **Related Problems**: Road Construction (MST), Building Roads (connectivity), Graph algorithms

## Problem Description

**Problem**: Given a graph with n cities and m roads, find the minimum cost to repair roads so that all cities are connected. Each road has a repair cost.

**Input**: 
- First line: Two integers n and m (number of cities and roads)
- Next m lines: Three integers a, b, and c (road between cities a and b with repair cost c)

**Output**: 
- Minimum cost to repair roads for connectivity, or "IMPOSSIBLE" if not possible

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n
- 1 ≤ c ≤ 10⁹
- Graph is undirected
- Cities are numbered from 1 to n

**Example**:
```
Input:
4 4
1 2 1
2 3 2
3 4 3
1 4 4

Output:
6
```

**Explanation**: 
- Minimum spanning tree: (1,2), (2,3), (3,4)
- Total cost: 1 + 2 + 3 = 6
- All cities are connected with minimum cost

## Visual Example

### Input Graph
```
Cities: 1, 2, 3, 4
Roads: (1,2,1), (2,3,2), (3,4,3), (1,4,4)

Graph representation:
1 ──1── 2 ──2── 3 ──3── 4
│                    │
└────────4───────────┘
```

### Kruskal's Algorithm Process
```
Step 1: Sort edges by weight
Edges: [(1,2,1), (2,3,2), (3,4,3), (1,4,4)]

Step 2: Initialize Union-Find
Parent: [1, 2, 3, 4] (each city is its own parent)
Rank: [0, 0, 0, 0]

Step 3: Process edges in order

Edge (1,2,1):
- Find(1) = 1, Find(2) = 2
- Different components, add edge
- Union(1,2): Parent[2] = 1, Rank[1] = 1
- MST edges: [(1,2,1)]
- Total cost: 1

Edge (2,3,2):
- Find(2) = 1, Find(3) = 3
- Different components, add edge
- Union(1,3): Parent[3] = 1, Rank[1] = 1
- MST edges: [(1,2,1), (2,3,2)]
- Total cost: 1 + 2 = 3

Edge (3,4,3):
- Find(3) = 1, Find(4) = 4
- Different components, add edge
- Union(1,4): Parent[4] = 1, Rank[1] = 2
- MST edges: [(1,2,1), (2,3,2), (3,4,3)]
- Total cost: 1 + 2 + 3 = 6

Edge (1,4,4):
- Find(1) = 1, Find(4) = 1
- Same component, skip edge
- MST edges: [(1,2,1), (2,3,2), (3,4,3)]
- Total cost: 6
```

### Final MST
```
Minimum Spanning Tree:
1 ──1── 2 ──2── 3 ──3── 4

Total cost: 6
All cities are connected with minimum cost.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force MST (Inefficient)

**Key Insights from Brute Force Solution:**
- Check all possible combinations of edges to find minimum spanning tree
- Use exhaustive search to find the optimal solution
- Simple but computationally expensive approach
- Not suitable for large graphs

**Algorithm:**
1. Generate all possible combinations of n-1 edges
2. Check if each combination forms a spanning tree
3. Calculate total cost for valid spanning trees
4. Return minimum cost among all valid spanning trees

**Visual Example:**
```
Brute force: Check all combinations
For 4 cities with edges: (1,2,1), (2,3,2), (3,4,3), (1,4,4)

All possible combinations of 3 edges:
- {(1,2,1), (2,3,2), (3,4,3)} → Cost: 6, Valid MST ✓
- {(1,2,1), (2,3,2), (1,4,4)} → Cost: 7, Valid MST ✓
- {(1,2,1), (3,4,3), (1,4,4)} → Cost: 8, Valid MST ✓
- {(2,3,2), (3,4,3), (1,4,4)} → Cost: 9, Valid MST ✓

Minimum cost: 6
```

**Implementation:**
```python
def road_reparation_brute_force(n, m, roads):
    from itertools import combinations
    
    # Generate all possible combinations of n-1 edges
    min_cost = float('inf')
    
    for edge_combination in combinations(roads, n - 1):
        # Check if edges form a spanning tree
        if is_spanning_tree(n, edge_combination):
            total_cost = sum(edge[2] for edge in edge_combination)
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else "IMPOSSIBLE"

def is_spanning_tree(n, edges):
    # Check if edges form a connected spanning tree
    parent = list(range(n + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    # Union all edges
    for a, b, _ in edges:
        union(a, b)
    
    # Check if all nodes are in same component
    root = find(1)
    for i in range(2, n + 1):
        if find(i) != root:
            return False
    
    return True
```

**Time Complexity:** O(C(m, n-1) × (n + m)) for checking all combinations
**Space Complexity:** O(n) for Union-Find data structure

**Why it's inefficient:**
- Exponential time complexity O(C(m, n-1))
- Not suitable for large graphs
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: Kruskal's Algorithm (Better)

**Key Insights from Kruskal's Solution:**
- Use greedy approach by sorting edges by weight
- Use Union-Find to detect cycles and maintain connectivity
- Add edges that connect different components
- Much more efficient than brute force approach

**Algorithm:**
1. Sort all edges by weight in ascending order
2. Initialize Union-Find data structure
3. Process edges in sorted order
4. Add edge if it connects different components
5. Stop when n-1 edges are added or all edges processed

**Visual Example:**
```
Kruskal's algorithm for cities: 1, 2, 3, 4 with edges (1,2,1), (2,3,2), (3,4,3), (1,4,4)

Step 1: Sort edges by weight
Edges: [(1,2,1), (2,3,2), (3,4,3), (1,4,4)]

Step 2: Process edges in order
- Edge (1,2,1): Add to MST, cost = 1
- Edge (2,3,2): Add to MST, cost = 1 + 2 = 3
- Edge (3,4,3): Add to MST, cost = 1 + 2 + 3 = 6
- Edge (1,4,4): Skip (creates cycle)

Final MST: {(1,2,1), (2,3,2), (3,4,3)} with cost 6
```

**Implementation:**
```python
def road_reparation_kruskal(n, m, roads):
    # Sort roads by cost
    roads.sort(key=lambda x: x[2])
    
    # Union-Find for cycle detection
    parent = list(range(n + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    # Kruskal's algorithm
    total_cost = 0
    edges_used = 0
    
    for a, b, cost in roads:
        if find(a) != find(b):
            union(a, b)
            total_cost += cost
            edges_used += 1
    
    # Check if all cities are connected
    if edges_used == n - 1:
        return total_cost
    else:
        return "IMPOSSIBLE"
```

**Time Complexity:** O(m log m) for sorting + O(m α(n)) for Union-Find
**Space Complexity:** O(n) for Union-Find data structure

**Why it's better:**
- Polynomial time complexity O(m log m)
- Simple and intuitive greedy approach
- Standard method for MST problems
- Suitable for competitive programming

### Approach 3: Optimized Kruskal's Algorithm (Optimal)

**Key Insights from Optimized Kruskal's Solution:**
- Use Union-Find with path compression and union by rank
- Optimize Union-Find operations for better performance
- Most efficient approach for MST problems
- Standard method in competitive programming

**Algorithm:**
1. Sort all edges by weight in ascending order
2. Initialize optimized Union-Find with path compression and union by rank
3. Process edges in sorted order
4. Add edge if it connects different components using optimized Union-Find
5. Stop when n-1 edges are added or all edges processed

**Visual Example:**
```
Optimized Kruskal's algorithm for cities: 1, 2, 3, 4 with edges (1,2,1), (2,3,2), (3,4,3), (1,4,4)

Step 1: Sort edges by weight
Edges: [(1,2,1), (2,3,2), (3,4,3), (1,4,4)]

Step 2: Initialize optimized Union-Find
Parent: [1, 2, 3, 4], Rank: [0, 0, 0, 0]

Step 3: Process edges with optimized Union-Find
- Edge (1,2,1): Union(1,2), cost = 1
- Edge (2,3,2): Union(1,3), cost = 1 + 2 = 3
- Edge (3,4,3): Union(1,4), cost = 1 + 2 + 3 = 6
- Edge (1,4,4): Skip (same component)

Final MST: {(1,2,1), (2,3,2), (3,4,3)} with cost 6
```

**Implementation:**
```python
def road_reparation_optimized(n, m, roads):
    # Sort roads by cost
    roads.sort(key=lambda x: x[2])
    
    # Union-Find with path compression and union by rank
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1
        return True
    
    # Kruskal's algorithm
    total_cost = 0
    edges_used = 0
    
    for a, b, cost in roads:
        if union(a, b):
            total_cost += cost
            edges_used += 1
    
    # Check if all cities are connected
    if edges_used == n - 1:
        return total_cost
    else:
        return "IMPOSSIBLE"

def solve_road_reparation():
    n, m = map(int, input().split())
    roads = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        roads.append((a, b, c))
    
    result = road_reparation_optimized(n, m, roads)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_road_reparation()
```

**Time Complexity:** O(m log m) for sorting + O(m α(n)) for optimized Union-Find
**Space Complexity:** O(n) for Union-Find data structure

**Why it's optimal:**
- O(m log m) time complexity is optimal for MST problems
- Optimized Union-Find with path compression and union by rank
- Most efficient approach for competitive programming
- Standard method for MST problems

## 🎯 Problem Variations

### Variation 1: MST with Edge Weight Constraints
**Problem**: Find minimum spanning tree with constraints on edge weights.

**Link**: [CSES Problem Set - MST with Weight Constraints](https://cses.fi/problemset/task/mst_weight_constraints)

```python
def mst_with_weight_constraints(n, m, roads, constraints):
    # constraints = {'min_weight': x, 'max_weight': y}
    
    # Filter edges based on weight constraints
    filtered_roads = []
    for a, b, cost in roads:
        if constraints.get('min_weight', 0) <= cost <= constraints.get('max_weight', float('inf')):
            filtered_roads.append((a, b, cost))
    
    # Find MST using filtered edges
    return road_reparation_optimized(n, len(filtered_roads), filtered_roads)
```

### Variation 2: MST with Node Degree Constraints
**Problem**: Find minimum spanning tree with constraints on node degrees.

**Link**: [CSES Problem Set - MST with Degree Constraints](https://cses.fi/problemset/task/mst_degree_constraints)

```python
def mst_with_degree_constraints(n, m, roads, constraints):
    # constraints = {'max_degree': x}
    
    # Use modified Kruskal's algorithm with degree tracking
    roads.sort(key=lambda x: x[2])
    
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    degree = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1
        return True
    
    total_cost = 0
    edges_used = 0
    
    for a, b, cost in roads:
        if find(a) != find(b) and degree[a] < constraints['max_degree'] and degree[b] < constraints['max_degree']:
            union(a, b)
            degree[a] += 1
            degree[b] += 1
            total_cost += cost
            edges_used += 1
    
    return total_cost if edges_used == n - 1 else "IMPOSSIBLE"
```

### Variation 3: Dynamic MST Updates
**Problem**: Handle dynamic updates to edges and find MST after each update.

**Link**: [CSES Problem Set - Dynamic MST](https://cses.fi/problemset/task/dynamic_mst)

```python
def dynamic_mst(n, m, initial_roads, updates):
    # updates = [(edge_to_add, edge_to_remove), ...]
    
    roads = initial_roads.copy()
    results = []
    
    for edge_to_add, edge_to_remove in updates:
        # Update roads
        if edge_to_remove in roads:
            roads.remove(edge_to_remove)
        if edge_to_add:
            roads.append(edge_to_add)
        
        # Find MST with updated roads
        result = road_reparation_optimized(n, len(roads), roads)
        results.append(result)
    
    return results
```

## 🔗 Related Problems

- **[Road Construction](/cses-analyses/problem_soulutions/graph_algorithms/road_construction_analysis/)**: MST construction problems
- **[Building Roads](/cses-analyses/problem_soulutions/graph_algorithms/building_roads_analysis/)**: Connectivity problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems
- **[Union-Find Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Disjoint set problems

## 📚 Learning Points

1. **Minimum Spanning Tree**: Essential for connectivity optimization
2. **Kruskal's Algorithm**: Greedy approach for MST problems
3. **Union-Find**: Efficient data structure for cycle detection
4. **Greedy Algorithms**: Local optimal choices lead to global optimum
5. **Graph Theory**: Foundation for many algorithmic problems
6. **Optimization**: Finding minimum cost solutions

## 📝 Summary

The Road Reparation problem demonstrates fundamental minimum spanning tree concepts for optimizing connectivity costs. We explored three approaches:

1. **Brute Force MST**: O(C(m, n-1) × (n + m)) time complexity using exhaustive search, inefficient for large graphs
2. **Kruskal's Algorithm**: O(m log m) time complexity using greedy approach with Union-Find, optimal and intuitive approach
3. **Optimized Kruskal's Algorithm**: O(m log m) time complexity using optimized Union-Find, most efficient approach

The key insights include understanding minimum spanning trees as optimal connectivity solutions, using greedy algorithms for efficient MST construction, and applying Union-Find data structures for cycle detection. This problem serves as an excellent introduction to graph optimization algorithms and connectivity analysis.
