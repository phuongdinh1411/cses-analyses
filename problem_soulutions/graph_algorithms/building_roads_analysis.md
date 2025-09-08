---
layout: simple
title: "Building Roads - Minimum Connectivity"
permalink: /problem_soulutions/graph_algorithms/building_roads_analysis
---

# Building Roads - Minimum Connectivity

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand connectivity problems and minimum edge addition concepts
- Apply DFS or BFS to count connected components in undirected graphs
- Implement efficient connectivity algorithms with proper component counting
- Optimize connectivity solutions using Union-Find data structure and graph representations
- Handle edge cases in connectivity problems (already connected, single component, disconnected graphs)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: DFS, BFS, connected components, Union-Find, graph connectivity, component counting
- **Data Structures**: Union-Find, adjacency lists, visited arrays, graph representations
- **Mathematical Concepts**: Graph theory, connected components, connectivity properties, graph connectivity
- **Programming Skills**: Graph traversal, component counting, Union-Find implementation, algorithm implementation
- **Related Problems**: Counting Rooms (connected components), Road Construction (MST), Graph connectivity

## Problem Description

There are n cities and m roads between them. Your task is to determine the minimum number of new roads that need to be built so that there is a route between any two cities.

**Input**: 
- First line: Two integers n and m (number of cities and roads)
- Next m lines: Two integers a and b (road between cities a and b)

**Output**: 
- One integer: minimum number of new roads needed

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n
- All roads are bidirectional
- Cities are numbered from 1 to n
- Find minimum number of new roads to connect all cities
- Each road connects exactly two cities
- Roads are undirected (bidirectional)
- Goal is to make the graph connected

**Example**:
```
Input:
4 2
1 2
3 4

Output:
1
```

**Explanation**: 
- Cities 1 and 2 are connected (component 1)
- Cities 3 and 4 are connected (component 2)
- We need 1 road to connect these 2 components
- Result: 2 components - 1 = 1 road needed

## Visual Example

### Input Graph
```
Cities: 1, 2, 3, 4
Roads: (1,2), (3,4)

    1 ──── 2    3 ──── 4
    │      │    │      │
    └──────┘    └──────┘
   Component 1  Component 2
```

### Connected Components Analysis
```
Component 1: {1, 2}
- Cities 1 and 2 are connected
- No connection to other cities

Component 2: {3, 4}
- Cities 3 and 4 are connected
- No connection to other cities

Total Components: 2
```

### Solution Process
```
Step 1: Identify connected components
┌─────────────────────────────────────┐
│ Component 1: {1, 2}                 │
│ Component 2: {3, 4}                 │
│ Total: 2 components                 │
└─────────────────────────────────────┘

Step 2: Calculate minimum roads needed
┌─────────────────────────────────────┐
│ Formula: (Number of Components) - 1 │
│ Calculation: 2 - 1 = 1              │
│ Result: 1 road needed               │
└─────────────────────────────────────┘

Step 3: Show the solution
┌─────────────────────────────────────┐
│ Add road: 2 ──── 3                  │
│ Final graph:                        │
│ 1 ──── 2 ──── 3 ──── 4             │
│ All cities now connected!           │
└─────────────────────────────────────┘
```

### Graph Connectivity Visualization
```
Before (Disconnected):
    1 ──── 2    3 ──── 4
    │      │    │      │
    └──────┘    └──────┘
   Component 1  Component 2

After (Connected):
    1 ──── 2 ──── 3 ──── 4
    │      │      │      │
    └──────┴──────┴──────┘
        Single Component

Added Road: 2 ──── 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Component Counting (Inefficient)

**Key Insights from Brute Force Solution:**
- Use simple adjacency matrix to represent the graph
- Check all pairs of cities to determine connectivity
- Count components by checking connectivity between all cities
- Simple but computationally expensive approach

**Algorithm:**
1. Build adjacency matrix from roads
2. Use Floyd-Warshall to find all-pairs connectivity
3. Count connected components by grouping cities
4. Calculate minimum roads needed

**Visual Example:**
```
Brute force: Check all pairs
For cities: 1, 2, 3, 4 with roads (1,2), (3,4)

Adjacency Matrix:
    1  2  3  4
1 [ 0  1  0  0 ]
2 [ 1  0  0  0 ]
3 [ 0  0  0  1 ]
4 [ 0  0  1  0 ]

After Floyd-Warshall:
    1  2  3  4
1 [ 0  1  0  0 ]
2 [ 1  0  0  0 ]
3 [ 0  0  0  1 ]
4 [ 0  0  1  0 ]

Components: {1,2} and {3,4} → 2 components
```

**Implementation:**
```python
def building_roads_brute_force(n, m, roads):
    # Build adjacency matrix
    adj = [[False] * (n + 1) for _ in range(n + 1)]
    for a, b in roads:
        adj[a][b] = True
        adj[b][a] = True
    
    # Floyd-Warshall for all-pairs connectivity
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if adj[i][k] and adj[k][j]:
                    adj[i][j] = True
    
    # Count components
    visited = [False] * (n + 1)
    components = 0
    
    for i in range(1, n + 1):
        if not visited[i]:
            components += 1
            for j in range(1, n + 1):
                if adj[i][j]:
                    visited[j] = True
    
    return components - 1
```

**Time Complexity:** O(n³) for Floyd-Warshall algorithm
**Space Complexity:** O(n²) for adjacency matrix

**Why it's inefficient:**
- Uses O(n²) space for adjacency matrix
- O(n³) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Overkill for this specific problem

### Approach 2: DFS Component Counting (Better)

**Key Insights from DFS Solution:**
- Use adjacency list for efficient graph representation
- Use depth-first search to explore connected components
- Count components by starting DFS from unvisited nodes
- Much more efficient than brute force approach

**Algorithm:**
1. Build adjacency list from roads
2. Use DFS to explore each connected component
3. Count components by tracking DFS starts
4. Calculate minimum roads needed

**Visual Example:**
```
DFS component counting for cities: 1, 2, 3, 4 with roads (1,2), (3,4)

DFS from city 1:
- Visit 1 → Visit 2 → Backtrack
- Component 1: {1, 2}

DFS from city 3 (unvisited):
- Visit 3 → Visit 4 → Backtrack  
- Component 2: {3, 4}

Total Components: 2
```

**Implementation:**
```python
def building_roads_dfs(n, m, roads):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    
    def dfs(node):
        if visited[node]:
            return
        visited[node] = True
        for neighbor in graph[node]:
            dfs(neighbor)
    
    visited = [False] * (n + 1)
    components = 0
    
    # Count connected components
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
            components += 1
    
    # Minimum roads needed = components - 1
    return components - 1
```

**Time Complexity:** O(n + m) for DFS traversal
**Space Complexity:** O(n + m) for adjacency list and visited array

**Why it's better:**
- Uses O(n + m) space instead of O(n²)
- O(n + m) time complexity is optimal
- Simple and intuitive approach
- Standard method for component counting

### Approach 3: Union-Find Component Counting (Optimal)

**Key Insights from Union-Find Solution:**
- Use Union-Find data structure for efficient connectivity queries
- Union operations merge components as roads are processed
- Find operations determine component membership
- Most efficient approach for dynamic connectivity

**Algorithm:**
1. Initialize Union-Find with n cities
2. Process each road by unioning the connected cities
3. Count unique root components
4. Calculate minimum roads needed

**Visual Example:**
```
Union-Find for cities: 1, 2, 3, 4 with roads (1,2), (3,4)

Initial: Parent = [1, 2, 3, 4] (each city is its own component)

Process road (1,2):
- Union(1, 2): Parent = [1, 1, 3, 4]
- Component 1: {1, 2}

Process road (3,4):
- Union(3, 4): Parent = [1, 1, 3, 3]
- Component 2: {3, 4}

Count unique roots: {1, 3} → 2 components
```

**Implementation:**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True

def building_roads_union_find(n, m, roads):
    uf = UnionFind(n)
    
    # Union all connected cities
    for a, b in roads:
        uf.union(a, b)
    
    # Count unique components
    components = set()
    for i in range(1, n + 1):
        components.add(uf.find(i))
    
    # Minimum roads needed = components - 1
    return len(components) - 1

def solve_building_roads():
    n, m = map(int, input().split())
    roads = [tuple(map(int, input().split())) for _ in range(m)]
    
    result = building_roads_union_find(n, m, roads)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_building_roads()
```

**Time Complexity:** O(n + m * α(n)) where α is the inverse Ackermann function
**Space Complexity:** O(n) for Union-Find data structure

**Why it's optimal:**
- Most efficient for connectivity queries
- Handles dynamic connectivity changes
- Optimal time complexity with path compression
- Best approach for competitive programming

## 🎯 Problem Variations

### Variation 1: Building Roads with Costs
**Problem**: Each road has a construction cost, find minimum cost roads to connect all cities.

**Link**: [CSES Problem Set - Building Roads with Costs](https://cses.fi/problemset/task/building_roads_costs)

```python
def building_roads_with_costs(n, m, roads, costs):
    # costs[(a, b)] = cost of building road between cities a and b
    
    # Build adjacency list with costs
    graph = [[] for _ in range(n + 1)]
    for a, b in roads:
        cost = costs.get((a, b), 1)
        graph[a].append((b, cost))
        graph[b].append((a, cost))
    
    # Find connected components
    visited = [False] * (n + 1)
    components = []
    
    def dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor, cost in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, component)
    
    for i in range(1, n + 1):
        if not visited[i]:
            component = []
            dfs(i, component)
            components.append(component)
    
    # Calculate minimum cost to connect components
    if len(components) <= 1:
        return 0, []
    
    # Find minimum cost edges between components
    min_cost_edges = []
    total_cost = 0
    
    for i in range(len(components) - 1):
        min_cost = float('inf')
        best_edge = None
        
        for node1 in components[i]:
            for node2 in components[i + 1]:
                cost = costs.get((node1, node2), float('inf'))
                if cost < min_cost:
                    min_cost = cost
                    best_edge = (node1, node2)
        
        if best_edge:
            min_cost_edges.append(best_edge)
            total_cost += min_cost
    
    return total_cost, min_cost_edges
```

### Variation 2: Building Roads with Constraints
**Problem**: Find minimum roads with constraints on road types or city connections.

**Link**: [CSES Problem Set - Building Roads with Constraints](https://cses.fi/problemset/task/building_roads_constraints)

```python
def building_roads_with_constraints(n, m, roads, constraints):
    # constraints = {'max_roads': x, 'forbidden_pairs': [(a, b), ...], 'required_pairs': [(a, b), ...]}
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in roads:
        # Check forbidden pairs
        if (a, b) in constraints.get('forbidden_pairs', []):
            continue
        graph[a].append(b)
        graph[b].append(a)
    
    # Find connected components
    visited = [False] * (n + 1)
    components = []
    
    def dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, component)
    
    for i in range(1, n + 1):
        if not visited[i]:
            component = []
            dfs(i, component)
            components.append(component)
    
    # Add required roads first
    required_roads = []
    for a, b in constraints.get('required_pairs', []):
        required_roads.append((a, b))
    
    # Calculate additional roads needed
    additional_roads_needed = len(components) - 1 - len(required_roads)
    
    # Check max roads constraint
    max_roads = constraints.get('max_roads', float('inf'))
    if len(required_roads) + additional_roads_needed > max_roads:
        return -1  # Impossible
    
    return additional_roads_needed, required_roads
```

### Variation 3: Dynamic Road Building
**Problem**: Handle dynamic updates to roads and find minimum roads needed after each update.

**Link**: [CSES Problem Set - Dynamic Road Building](https://cses.fi/problemset/task/dynamic_road_building)

```python
def dynamic_building_roads(n, m, initial_roads, updates):
    # updates = [(road_to_add, road_to_remove), ...]
    
    roads = initial_roads.copy()
    results = []
    
    for road_to_add, road_to_remove in updates:
        # Update roads
        if road_to_remove in roads:
            roads.remove(road_to_remove)
        if road_to_add:
            roads.append(road_to_add)
        
        # Rebuild graph
        graph = [[] for _ in range(n + 1)]
        for a, b in roads:
            graph[a].append(b)
            graph[b].append(a)
        
        # Count components
        visited = [False] * (n + 1)
        components = 0
        
        def dfs(node):
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor)
        
        for i in range(1, n + 1):
            if not visited[i]:
                dfs(i)
                components += 1
        
        roads_needed = max(0, components - 1)
        results.append(roads_needed)
    
    return results
```

## 🔗 Related Problems

- **[Counting Rooms](/cses-analyses/problem_soulutions/graph_algorithms/counting_rooms_analysis/)**: Connected components problems
- **[Road Construction](/cses-analyses/problem_soulutions/graph_algorithms/road_construction_analysis/)**: Minimum spanning tree problems
- **[Graph Connectivity](/cses-analyses/problem_soulutions/graph_algorithms/)**: Connectivity problems
- **[Network Design](/cses-analyses/problem_soulutions/graph_algorithms/)**: Network optimization problems

## 📚 Learning Points

1. **Connected Components**: Essential for graph connectivity problems
2. **Component Counting**: Important for minimum edge calculations
3. **Graph Traversal**: Key technique for component exploration
4. **Union-Find**: Efficient data structure for connectivity queries
5. **Minimum Edges**: Critical concept for connectivity optimization
6. **Graph Theory**: Foundation for many algorithmic problems

## 📝 Summary

The Building Roads problem demonstrates fundamental graph connectivity concepts for finding minimum edges to connect all components. We explored three approaches:

1. **Brute Force Component Counting**: O(n³) time complexity using Floyd-Warshall algorithm, inefficient for large graphs
2. **DFS Component Counting**: O(n + m) time complexity using depth-first search, optimal and intuitive approach
3. **Union-Find Component Counting**: O(n + m * α(n)) time complexity using Union-Find data structure, most efficient for dynamic connectivity

The key insights include counting connected components to determine minimum edges needed, using graph traversal algorithms for component exploration, and applying the formula (components - 1) for minimum connectivity. This problem serves as an excellent introduction to graph connectivity algorithms and component counting techniques.
