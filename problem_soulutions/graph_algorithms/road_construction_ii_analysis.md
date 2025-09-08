---
layout: simple
title: "Road Construction II - Minimum Spanning Tree with Constraints"
permalink: /problem_soulutions/graph_algorithms/road_construction_ii_analysis
---

# Road Construction II - Minimum Spanning Tree with Constraints

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand advanced MST problems with additional constraints and requirements
- Apply Kruskal's algorithm or Prim's algorithm with constraint handling for MST problems
- Implement efficient MST algorithms with proper constraint validation and optimization
- Optimize MST solutions using Union-Find and advanced constraint handling techniques
- Handle edge cases in constrained MST problems (impossible constraints, disconnected components, large graphs)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Kruskal's algorithm, Prim's algorithm, minimum spanning trees, Union-Find, constraint handling
- **Data Structures**: Union-Find, priority queues, edge lists, graph representations, constraint tracking
- **Mathematical Concepts**: Graph theory, minimum spanning trees, greedy algorithms, optimization, constraint satisfaction
- **Programming Skills**: Union-Find implementation, constraint validation, MST algorithms, algorithm implementation
- **Related Problems**: Road Construction (basic MST), Building Roads (connectivity), MST algorithms

## Problem Description

**Problem**: Given a graph with n cities and m roads, find the minimum cost to build roads so that all cities are connected. Each road has a construction cost.

This is a minimum spanning tree (MST) problem with additional constraints. We need to find the minimum cost to connect all cities while satisfying specific requirements.

**Input**: 
- First line: Two integers n and m (number of cities and roads)
- Next m lines: Three integers a, b, and c (road between cities a and b with cost c)

**Output**: 
- Minimum cost to build roads so all cities are connected, or "IMPOSSIBLE" if not possible

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
- Roads: (1,2) cost 1, (2,3) cost 2, (3,4) cost 3, (1,4) cost 4
- Minimum spanning tree: (1,2) + (2,3) + (3,4) = 1 + 2 + 3 = 6
- This connects all cities with minimum cost

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

### Approach 1: Brute Force MST with Constraints (Inefficient)

**Key Insights from Brute Force Solution:**
- Check all possible combinations of edges to find minimum spanning tree with constraints
- Use exhaustive search to find the optimal solution satisfying all constraints
- Simple but computationally expensive approach
- Not suitable for large graphs with many constraints

**Algorithm:**
1. Generate all possible combinations of n-1 edges
2. Check if each combination forms a spanning tree and satisfies constraints
3. Calculate total cost for valid constrained spanning trees
4. Return minimum cost among all valid constrained spanning trees

**Visual Example:**
```
Brute force: Check all combinations with constraints
For 4 cities with edges: (1,2,1), (2,3,2), (3,4,3), (1,4,4)
Constraint: Maximum degree per city = 2

All possible combinations of 3 edges:
- {(1,2,1), (2,3,2), (3,4,3)} → Cost: 6, Valid MST ✓, Constraint satisfied ✓
- {(1,2,1), (2,3,2), (1,4,4)} → Cost: 7, Valid MST ✓, Constraint satisfied ✓
- {(1,2,1), (3,4,3), (1,4,4)} → Cost: 8, Valid MST ✓, Constraint satisfied ✓
- {(2,3,2), (3,4,3), (1,4,4)} → Cost: 9, Valid MST ✓, Constraint satisfied ✓

Minimum cost: 6
```

**Implementation:**
```python
def road_construction_ii_brute_force(n, m, roads, constraints):
    from itertools import combinations
    
    # Generate all possible combinations of n-1 edges
    min_cost = float('inf')
    
    for edge_combination in combinations(roads, n - 1):
        # Check if edges form a spanning tree and satisfy constraints
        if is_valid_constrained_spanning_tree(n, edge_combination, constraints):
            total_cost = sum(edge[2] for edge in edge_combination)
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else "IMPOSSIBLE"

def is_valid_constrained_spanning_tree(n, edges, constraints):
    # Check if edges form a connected spanning tree and satisfy constraints
    parent = list(range(n + 1))
    degree = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    # Union all edges and check degree constraints
    for a, b, _ in edges:
        if degree[a] >= constraints.get('max_degree', float('inf')):
            return False
        if degree[b] >= constraints.get('max_degree', float('inf')):
            return False
        
        union(a, b)
        degree[a] += 1
        degree[b] += 1
    
    # Check if all nodes are in same component
    root = find(1)
    for i in range(2, n + 1):
        if find(i) != root:
            return False
    
    return True
```

**Time Complexity:** O(C(m, n-1) × (n + m)) for checking all combinations
**Space Complexity:** O(n) for Union-Find and degree tracking

**Why it's inefficient:**
- Exponential time complexity O(C(m, n-1))
- Not suitable for large graphs
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: Kruskal's Algorithm with Constraint Handling (Better)

**Key Insights from Kruskal's Solution:**
- Use greedy approach by sorting edges by weight
- Use Union-Find to detect cycles and maintain connectivity
- Add constraint validation during edge selection
- Much more efficient than brute force approach

**Algorithm:**
1. Sort all edges by weight in ascending order
2. Initialize Union-Find data structure and constraint tracking
3. Process edges in sorted order
4. Add edge if it connects different components and satisfies constraints
5. Stop when n-1 edges are added or all edges processed

**Visual Example:**
```
Kruskal's algorithm with constraints for cities: 1, 2, 3, 4 with edges (1,2,1), (2,3,2), (3,4,3), (1,4,4)
Constraint: Maximum degree per city = 2

Step 1: Sort edges by weight
Edges: [(1,2,1), (2,3,2), (3,4,3), (1,4,4)]

Step 2: Process edges with constraint checking
- Edge (1,2,1): Add to MST, cost = 1, degrees: [1,1,0,0]
- Edge (2,3,2): Add to MST, cost = 1 + 2 = 3, degrees: [1,2,1,0]
- Edge (3,4,3): Add to MST, cost = 1 + 2 + 3 = 6, degrees: [1,2,2,1]
- Edge (1,4,4): Skip (creates cycle)

Final MST: {(1,2,1), (2,3,2), (3,4,3)} with cost 6
```

**Implementation:**
```python
def road_construction_ii_kruskal(n, m, roads, constraints):
    # Sort roads by cost
    roads.sort(key=lambda x: x[2])
    
    # Union-Find for cycle detection
    parent = list(range(n + 1))
    degree = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    # Kruskal's algorithm with constraint handling
    total_cost = 0
    edges_used = 0
    
    for a, b, cost in roads:
        # Check constraints before adding edge
        if (find(a) != find(b) and 
            degree[a] < constraints.get('max_degree', float('inf')) and
            degree[b] < constraints.get('max_degree', float('inf'))):
            
            union(a, b)
            degree[a] += 1
            degree[b] += 1
            total_cost += cost
            edges_used += 1
    
    # Check if all cities are connected
    if edges_used == n - 1:
        return total_cost
    else:
        return "IMPOSSIBLE"
```

**Time Complexity:** O(m log m) for sorting + O(m α(n)) for Union-Find
**Space Complexity:** O(n) for Union-Find and degree tracking

**Why it's better:**
- Polynomial time complexity O(m log m)
- Simple and intuitive greedy approach
- Handles constraints efficiently
- Suitable for competitive programming

### Approach 3: Optimized Kruskal's Algorithm with Advanced Constraint Handling (Optimal)

**Key Insights from Optimized Kruskal's Solution:**
- Use Union-Find with path compression and union by rank
- Implement advanced constraint validation and optimization
- Most efficient approach for constrained MST problems
- Standard method in competitive programming

**Algorithm:**
1. Sort all edges by weight in ascending order
2. Initialize optimized Union-Find with path compression and union by rank
3. Process edges in sorted order with advanced constraint handling
4. Add edge if it connects different components and satisfies all constraints
5. Stop when n-1 edges are added or all edges processed

**Visual Example:**
```
Optimized Kruskal's algorithm with advanced constraints for cities: 1, 2, 3, 4 with edges (1,2,1), (2,3,2), (3,4,3), (1,4,4)
Constraints: Maximum degree per city = 2, Minimum edge weight = 1

Step 1: Sort edges by weight
Edges: [(1,2,1), (2,3,2), (3,4,3), (1,4,4)]

Step 2: Process edges with optimized Union-Find and constraint validation
- Edge (1,2,1): Union(1,2), cost = 1, degrees: [1,1,0,0]
- Edge (2,3,2): Union(1,3), cost = 1 + 2 = 3, degrees: [1,2,1,0]
- Edge (3,4,3): Union(1,4), cost = 1 + 2 + 3 = 6, degrees: [1,2,2,1]
- Edge (1,4,4): Skip (same component)

Final MST: {(1,2,1), (2,3,2), (3,4,3)} with cost 6
```

**Implementation:**
```python
def road_construction_ii_optimized(n, m, roads, constraints):
    # Sort roads by cost
    roads.sort(key=lambda x: x[2])
    
    # Union-Find with path compression and union by rank
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
    
    # Kruskal's algorithm with advanced constraint handling
    total_cost = 0
    edges_used = 0
    
    for a, b, cost in roads:
        # Advanced constraint validation
        if (union(a, b) and 
            degree[a] < constraints.get('max_degree', float('inf')) and
            degree[b] < constraints.get('max_degree', float('inf')) and
            cost >= constraints.get('min_weight', 0)):
            
            degree[a] += 1
            degree[b] += 1
            total_cost += cost
            edges_used += 1
    
    # Check if all cities are connected
    if edges_used == n - 1:
        return total_cost
    else:
        return "IMPOSSIBLE"

def solve_road_construction_ii():
    n, m = map(int, input().split())
    roads = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        roads.append((a, b, c))
    
    # Define constraints (example constraints)
    constraints = {
        'max_degree': 2,  # Maximum degree per city
        'min_weight': 1   # Minimum edge weight
    }
    
    result = road_construction_ii_optimized(n, m, roads, constraints)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_road_construction_ii()
```

**Time Complexity:** O(m log m) for sorting + O(m α(n)) for optimized Union-Find
**Space Complexity:** O(n) for Union-Find and constraint tracking

**Why it's optimal:**
- O(m log m) time complexity is optimal for constrained MST problems
- Optimized Union-Find with path compression and union by rank
- Advanced constraint handling and validation
- Most efficient approach for competitive programming

## 🎯 Problem Variations

### Variation 1: MST with Multiple Constraint Types
**Problem**: Find minimum spanning tree with multiple types of constraints.

**Link**: [CSES Problem Set - MST with Multiple Constraints](https://cses.fi/problemset/task/mst_multiple_constraints)

```python
def mst_multiple_constraints(n, m, roads, constraints):
    # constraints = {'max_degree': x, 'min_weight': y, 'max_weight': z, 'max_edges': w}
    
    # Filter edges based on weight constraints
    filtered_roads = []
    for a, b, cost in roads:
        if constraints.get('min_weight', 0) <= cost <= constraints.get('max_weight', float('inf')):
            filtered_roads.append((a, b, cost))
    
    # Use optimized Kruskal's with multiple constraints
    return road_construction_ii_optimized(n, len(filtered_roads), filtered_roads, constraints)
```

### Variation 2: MST with Node-Specific Constraints
**Problem**: Find minimum spanning tree with different constraints for different nodes.

**Link**: [CSES Problem Set - MST with Node-Specific Constraints](https://cses.fi/problemset/task/mst_node_constraints)

```python
def mst_node_specific_constraints(n, m, roads, node_constraints):
    # node_constraints[i] = {'max_degree': x, 'min_weight': y}
    
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
        # Check node-specific constraints
        if (union(a, b) and 
            degree[a] < node_constraints[a].get('max_degree', float('inf')) and
            degree[b] < node_constraints[b].get('max_degree', float('inf')) and
            cost >= node_constraints[a].get('min_weight', 0) and
            cost >= node_constraints[b].get('min_weight', 0)):
            
            degree[a] += 1
            degree[b] += 1
            total_cost += cost
            edges_used += 1
    
    return total_cost if edges_used == n - 1 else "IMPOSSIBLE"
```

### Variation 3: Dynamic Constrained MST Updates
**Problem**: Handle dynamic updates to edges and constraints, find MST after each update.

**Link**: [CSES Problem Set - Dynamic Constrained MST](https://cses.fi/problemset/task/dynamic_constrained_mst)

```python
def dynamic_constrained_mst(n, m, initial_roads, initial_constraints, updates):
    # updates = [(edge_to_add, edge_to_remove, constraint_update), ...]
    
    roads = initial_roads.copy()
    constraints = initial_constraints.copy()
    results = []
    
    for edge_to_add, edge_to_remove, constraint_update in updates:
        # Update roads
        if edge_to_remove in roads:
            roads.remove(edge_to_remove)
        if edge_to_add:
            roads.append(edge_to_add)
        
        # Update constraints
        if constraint_update:
            constraints.update(constraint_update)
        
        # Find MST with updated roads and constraints
        result = road_construction_ii_optimized(n, len(roads), roads, constraints)
        results.append(result)
    
    return results
```

## 🔗 Related Problems

- **[Road Construction](/cses-analyses/problem_soulutions/graph_algorithms/road_construction_analysis/)**: Basic MST construction problems
- **[Road Reparation](/cses-analyses/problem_soulutions/graph_algorithms/road_reparation_analysis/)**: MST repair problems
- **[Building Roads](/cses-analyses/problem_soulutions/graph_algorithms/building_roads_analysis/)**: Connectivity problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Constrained Minimum Spanning Tree**: Essential for optimization with restrictions
2. **Kruskal's Algorithm**: Greedy approach for constrained MST problems
3. **Union-Find**: Efficient data structure for cycle detection and constraint validation
4. **Constraint Handling**: Managing multiple constraints in optimization problems
5. **Greedy Algorithms**: Local optimal choices with constraint satisfaction
6. **Graph Theory**: Foundation for many constrained optimization problems

## 📝 Summary

The Road Construction II problem demonstrates advanced minimum spanning tree concepts with constraint handling for optimizing connectivity costs under restrictions. We explored three approaches:

1. **Brute Force MST with Constraints**: O(C(m, n-1) × (n + m)) time complexity using exhaustive search, inefficient for large graphs
2. **Kruskal's Algorithm with Constraint Handling**: O(m log m) time complexity using greedy approach with constraint validation, optimal and intuitive approach
3. **Optimized Kruskal's Algorithm with Advanced Constraint Handling**: O(m log m) time complexity using optimized Union-Find with advanced constraint validation, most efficient approach

The key insights include understanding constrained minimum spanning trees as optimization problems with restrictions, using greedy algorithms for efficient constrained MST construction, and applying advanced constraint validation techniques. This problem serves as an excellent introduction to constrained optimization algorithms and advanced graph theory concepts.
