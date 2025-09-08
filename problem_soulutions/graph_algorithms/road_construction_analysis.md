---
layout: simple
title: "Road Construction - Minimum Spanning Tree"
permalink: /problem_soulutions/graph_algorithms/road_construction_analysis
---

# Road Construction - Minimum Spanning Tree

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand minimum spanning tree problems and MST concepts
- Apply Kruskal's algorithm or Prim's algorithm to find minimum spanning trees
- Implement efficient MST algorithms with proper Union-Find data structure usage
- Optimize MST solutions using Union-Find and graph representations
- Handle edge cases in MST problems (impossible to connect, single node, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Kruskal's algorithm, Prim's algorithm, minimum spanning trees, Union-Find, MST algorithms
- **Data Structures**: Union-Find, priority queues, edge lists, graph representations
- **Mathematical Concepts**: Graph theory, minimum spanning trees, greedy algorithms, optimization
- **Programming Skills**: Union-Find implementation, edge sorting, MST algorithms, algorithm implementation
- **Related Problems**: Building Roads (connectivity), Road Construction II (MST variations), Graph algorithms

## Problem Description

**Problem**: Given a graph with n cities and m roads, find the minimum cost to build roads so that all cities are connected. Each road has a construction cost.

This is a classic minimum spanning tree (MST) problem where we need to find the minimum cost to connect all cities. We can solve this using Kruskal's algorithm with Union-Find data structure.

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
- No self-loops or multiple edges between same pair of cities
- Roads are bidirectional
- Cities are numbered 1, 2, ..., n

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

### Key Insight
Kruskal's algorithm works by:
1. Sorting edges by weight (greedy approach)
2. Using Union-Find to detect cycles
3. Adding edges that connect different components
4. Time complexity: O(m log m) for sorting + O(m α(n)) for Union-Find
5. Space complexity: O(n) for Union-Find data structure

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Edge Selection (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of edges to find minimum spanning tree
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible combinations of n-1 edges
2. For each combination, check if it forms a spanning tree
3. Calculate the total cost for valid spanning trees
4. Return the minimum cost found

**Visual Example:**
```
Brute force: Try all possible edge combinations
For 4 cities, need 3 edges to connect all:
- Combination 1: [(1,2,1), (2,3,2), (3,4,3)] → Cost: 6 ✓
- Combination 2: [(1,2,1), (2,3,2), (1,4,4)] → Cost: 7
- Combination 3: [(1,2,1), (3,4,3), (1,4,4)] → Cost: 8
- Try all C(m, n-1) combinations
```

**Implementation:**
```python
def road_construction_brute_force(n, m, roads):
    from itertools import combinations
    
    def is_connected(edges):
        # Check if edges form a connected graph
        parent = list(range(n + 1))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            parent[find(x)] = find(y)
        
        for a, b, _ in edges:
            union(a, b)
        
        # Check if all cities are in same component
        root = find(1)
        for i in range(2, n + 1):
            if find(i) != root:
                return False
        return True
    
    min_cost = float('inf')
    
    # Try all combinations of n-1 edges
    for edge_combination in combinations(roads, n - 1):
        if is_connected(edge_combination):
            total_cost = sum(cost for _, _, cost in edge_combination)
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else "IMPOSSIBLE"

def solve_road_construction_brute_force():
    n, m = map(int, input().split())
    roads = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        roads.append((a, b, c))
    
    result = road_construction_brute_force(n, m, roads)
    print(result)
```

**Time Complexity:** O(C(m, n-1) × n) for m edges with exponential combinations
**Space Complexity:** O(n) for Union-Find

**Why it's inefficient:**
- O(C(m, n-1)) time complexity is too slow for large graphs
- Not suitable for competitive programming with m up to 2×10^5
- Inefficient for large inputs
- Poor performance with many edges

### Approach 2: Basic Kruskal's Algorithm (Better)

**Key Insights from Basic Kruskal's Solution:**
- Use Kruskal's algorithm with basic Union-Find
- Much more efficient than brute force approach
- Standard method for minimum spanning tree problems
- Can handle larger graphs than brute force

**Algorithm:**
1. Sort edges by weight in ascending order
2. Use Union-Find to detect cycles
3. Add edges that connect different components
4. Return the total cost of the minimum spanning tree

**Visual Example:**
```
Basic Kruskal's for graph: (1,2,1), (2,3,2), (3,4,3), (1,4,4)
- Sort edges: [(1,2,1), (2,3,2), (3,4,3), (1,4,4)]
- Add (1,2,1): Cost = 1
- Add (2,3,2): Cost = 1 + 2 = 3
- Add (3,4,3): Cost = 1 + 2 + 3 = 6
- Skip (1,4,4): Already connected
```

**Implementation:**
```python
def road_construction_basic_kruskal(n, m, roads):
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

def solve_road_construction_basic():
    n, m = map(int, input().split())
    roads = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        roads.append((a, b, c))
    
    result = road_construction_basic_kruskal(n, m, roads)
    print(result)
```

**Time Complexity:** O(m log m) for m edges with sorting and Union-Find
**Space Complexity:** O(n) for Union-Find data structure

**Why it's better:**
- O(m log m) time complexity is much better than O(C(m, n-1))
- Standard method for minimum spanning tree problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Kruskal's Algorithm with Union-Find (Optimal)

**Key Insights from Optimized Kruskal's Solution:**
- Use Kruskal's algorithm with optimized Union-Find (path compression and union by rank)
- Most efficient approach for minimum spanning tree problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Sort edges by weight in ascending order
2. Use optimized Union-Find with path compression and union by rank
3. Add edges that connect different components
4. Return the total cost of the minimum spanning tree

**Visual Example:**
```
Optimized Kruskal's for graph: (1,2,1), (2,3,2), (3,4,3), (1,4,4)
- Sort edges: [(1,2,1), (2,3,2), (3,4,3), (1,4,4)]
- Initialize: parent = [0,1,2,3,4], rank = [0,0,0,0,0]
- Add (1,2,1): parent = [0,1,1,3,4], rank = [0,1,0,0,0]
- Add (2,3,2): parent = [0,1,1,1,4], rank = [0,1,0,0,0]
- Add (3,4,3): parent = [0,1,1,1,1], rank = [0,2,0,0,0]
- Skip (1,4,4): Already connected
```

**Implementation:**
```python
def road_construction_optimized_kruskal(n, m, roads):
    # Sort roads by cost
    roads.sort(key=lambda x: x[2])
    
    # Union-Find with path compression and union by rank
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        
        # Union by rank
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

def solve_road_construction():
    n, m = map(int, input().split())
    roads = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        roads.append((a, b, c))
    
    result = road_construction_optimized_kruskal(n, m, roads)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_road_construction()
```

**Time Complexity:** O(m log m) for m edges with optimized Union-Find
**Space Complexity:** O(n) for Union-Find data structure

**Why it's optimal:**
- O(m log m) time complexity is optimal for MST problems
- Uses optimized Union-Find with path compression and union by rank
- Most efficient approach for competitive programming
- Standard method for minimum spanning tree problems

## 🎯 Problem Variations

### Variation 1: Road Construction with Maximum Cost
**Problem**: Find maximum cost to build roads so all cities are connected.

**Link**: [CSES Problem Set - Road Construction Maximum Cost](https://cses.fi/problemset/task/road_construction_maximum_cost)

```python
def road_construction_maximum_cost(n, m, roads):
    # Sort roads by cost in descending order
    roads.sort(key=lambda x: x[2], reverse=True)
    
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
    
    # Kruskal's algorithm for maximum spanning tree
    total_cost = 0
    edges_used = 0
    
    for a, b, cost in roads:
        if union(a, b):
            total_cost += cost
            edges_used += 1
    
    if edges_used == n - 1:
        return total_cost
    else:
        return "IMPOSSIBLE"
```

### Variation 2: Road Construction with Budget Constraint
**Problem**: Find minimum cost to connect all cities within a given budget.

**Link**: [CSES Problem Set - Road Construction Budget](https://cses.fi/problemset/task/road_construction_budget)

```python
def road_construction_budget(n, m, roads, budget):
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
    
    # Kruskal's algorithm with budget constraint
    total_cost = 0
    edges_used = 0
    
    for a, b, cost in roads:
        if total_cost + cost <= budget and union(a, b):
            total_cost += cost
            edges_used += 1
    
    if edges_used == n - 1:
        return total_cost
    else:
        return "IMPOSSIBLE"
```

### Variation 3: Road Construction with Multiple Components
**Problem**: Find minimum cost to connect all cities, allowing multiple components.

**Link**: [CSES Problem Set - Road Construction Components](https://cses.fi/problemset/task/road_construction_components)

```python
def road_construction_components(n, m, roads, max_components):
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
    
    def count_components():
        components = set()
        for i in range(1, n + 1):
            components.add(find(i))
        return len(components)
    
    # Kruskal's algorithm with component constraint
    total_cost = 0
    edges_used = 0
    
    for a, b, cost in roads:
        if union(a, b):
            total_cost += cost
            edges_used += 1
        
        # Check if we have acceptable number of components
        if count_components() <= max_components:
            return total_cost
    
    return "IMPOSSIBLE"
```

## 🔗 Related Problems

- **[Building Roads](/cses-analyses/problem_soulutions/graph_algorithms/building_roads_analysis/)**: Connectivity
- **[Road Construction II](/cses-analyses/problem_soulutions/graph_algorithms/road_construction_ii_analysis/)**: MST variations
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph problems
- **[Minimum Spanning Tree](/cses-analyses/problem_soulutions/graph_algorithms/)**: MST problems

## 📚 Learning Points

1. **Kruskal's Algorithm**: Essential for understanding minimum spanning tree problems
2. **Union-Find Data Structure**: Key technique for cycle detection
3. **Greedy Algorithms**: Important for understanding optimization problems
4. **Graph Theory**: Critical for understanding connectivity problems
5. **Minimum Spanning Tree**: Foundation for many network optimization problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Road Construction problem demonstrates fundamental minimum spanning tree concepts for finding optimal connectivity solutions. We explored three approaches:

1. **Brute Force Edge Selection**: O(C(m, n-1) × n) time complexity using exponential combinations, inefficient for large graphs
2. **Basic Kruskal's Algorithm**: O(m log m) time complexity using standard Kruskal's algorithm, better approach for MST problems
3. **Optimized Kruskal's Algorithm with Union-Find**: O(m log m) time complexity with optimized Union-Find, optimal approach for minimum spanning tree

The key insights include understanding Kruskal's algorithm principles, using Union-Find for efficient cycle detection, and applying greedy algorithms for optimal performance. This problem serves as an excellent introduction to minimum spanning tree algorithms and network optimization techniques.

