---
layout: simple
title: "Shortest Routes II - All Pairs Shortest Paths"
permalink: /problem_soulutions/graph_algorithms/shortest_routes_ii_analysis
---

# Shortest Routes II - All Pairs Shortest Paths

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand all-pairs shortest path problems and Floyd-Warshall algorithm fundamentals
- Apply Floyd-Warshall algorithm to find shortest paths between all pairs of vertices
- Implement efficient all-pairs shortest path algorithms with proper matrix operations
- Optimize all-pairs shortest path solutions using space-efficient techniques and matrix operations
- Handle edge cases in all-pairs shortest paths (negative cycles, unreachable pairs, large graphs)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Floyd-Warshall algorithm, all-pairs shortest paths, dynamic programming, matrix operations
- **Data Structures**: 2D arrays, adjacency matrices, distance matrices, graph representations
- **Mathematical Concepts**: Graph theory, shortest path properties, dynamic programming, matrix operations
- **Programming Skills**: Matrix manipulation, dynamic programming, graph algorithms, algorithm implementation
- **Related Problems**: Shortest Routes I (single-source shortest paths), High Score (negative weights), Graph algorithms

## Problem Description

**Problem**: There are n cities and m flight connections. Your task is to find the shortest route between any two cities.

This is an all-pairs shortest path problem where we need to find the shortest distance between every pair of cities. We can solve this using the Floyd-Warshall algorithm.

**Input**: 
- First line: Two integers n and m (number of cities and flight connections)
- Next m lines: Three integers a, b, and c (flight from city a to city b with cost c)

**Output**: 
- n lines with n integers each: shortest route lengths between all pairs of cities
- If no route exists, print -1

**Constraints**:
- 1 ≤ n ≤ 500
- 1 ≤ m ≤ n²
- 1 ≤ a, b ≤ n
- 1 ≤ c ≤ 10⁹
- Cities are numbered 1, 2, ..., n
- Graph is directed
- No self-loops or multiple edges between same pair of cities
- All edge weights are non-negative

**Example**:
```
Input:
4 3
1 2 1
2 3 1
3 4 1

Output:
0 1 2 3
-1 0 1 2
-1 -1 0 1
-1 -1 -1 0
```

**Explanation**: 
- City 1 to City 2: 1 (direct flight)
- City 1 to City 3: 2 (path: 1 → 2 → 3, cost: 1 + 1 = 2)
- City 1 to City 4: 3 (path: 1 → 2 → 3 → 4, cost: 1 + 1 + 1 = 3)
- Cities 2, 3, 4 have similar patterns

## Visual Example

### Input Graph
```
Cities: 1, 2, 3, 4
Flights: (1→2, cost=1), (2→3, cost=1), (3→4, cost=1)

Graph representation:
1 ──1──> 2 ──1──> 3 ──1──> 4
```

### Floyd-Warshall Algorithm Process
```
Initial distance matrix:
    1  2  3  4
1 [ 0  1  ∞  ∞]
2 [ ∞  0  1  ∞]
3 [ ∞  ∞  0  1]
4 [ ∞  ∞  ∞  0]

Step 1: k = 1 (intermediate city 1)
- No changes (city 1 has no incoming edges)

Step 2: k = 2 (intermediate city 2)
- Check if d[i][1] + d[1][j] < d[i][j]
- d[1][3] = min(d[1][3], d[1][2] + d[2][3]) = min(∞, 1 + 1) = 2
- d[1][4] = min(d[1][4], d[1][2] + d[2][4]) = min(∞, 1 + ∞) = ∞

Updated matrix:
    1  2  3  4
1 [ 0  1  2  ∞]
2 [ ∞  0  1  ∞]
3 [ ∞  ∞  0  1]
4 [ ∞  ∞  ∞  0]

Step 3: k = 3 (intermediate city 3)
- d[1][4] = min(d[1][4], d[1][3] + d[3][4]) = min(∞, 2 + 1) = 3
- d[2][4] = min(d[2][4], d[2][3] + d[3][4]) = min(∞, 1 + 1) = 2

Updated matrix:
    1  2  3  4
1 [ 0  1  2  3]
2 [ ∞  0  1  2]
3 [ ∞  ∞  0  1]
4 [ ∞  ∞  ∞  0]

Step 4: k = 4 (intermediate city 4)
- No changes (city 4 has no outgoing edges)

Final distance matrix:
    1  2  3  4
1 [ 0  1  2  3]
2 [ ∞  0  1  2]
3 [ ∞  ∞  0  1]
4 [ ∞  ∞  ∞  0]
```

### Path Analysis
```
Shortest paths found:
- 1 → 2: 1 (direct)
- 1 → 3: 2 (via 2: 1 → 2 → 3)
- 1 → 4: 3 (via 2,3: 1 → 2 → 3 → 4)
- 2 → 3: 1 (direct)
- 2 → 4: 2 (via 3: 2 → 3 → 4)
- 3 → 4: 1 (direct)

Unreachable paths (∞):
- 2 → 1: No path exists
- 3 → 1: No path exists
- 3 → 2: No path exists
- 4 → 1: No path exists
- 4 → 2: No path exists
- 4 → 3: No path exists
```

### Key Insight
Floyd-Warshall algorithm works by:
1. Using each city as an intermediate point
2. Checking if going through that city gives a shorter path
3. Updating distances if a shorter path is found
4. Time complexity: O(n³) where n = number of cities
5. Space complexity: O(n²) for the distance matrix

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths between every pair of cities
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths between every pair of cities
2. For each path, calculate the total cost
3. Return the minimum cost among all paths for each pair
4. Handle cases where no path exists

**Visual Example:**
```
Brute force: Try all possible paths
For graph: 1 ──1──> 2 ──1──> 3 ──1──> 4

All possible paths from 1 to 4:
- Path 1: 1 → 2 → 3 → 4 (cost = 1 + 1 + 1 = 3)
- Path 2: 1 → 2 → 4 (cost = 1 + ∞ = ∞) - No direct edge
- Path 3: 1 → 3 → 4 (cost = ∞ + 1 = ∞) - No direct edge
- Path 4: 1 → 4 (cost = ∞) - No direct edge

Minimum cost: 3
```

**Implementation:**
```python
def shortest_routes_brute_force(n, m, edges):
    def find_all_paths(current, target, visited, path_cost):
        if current == target:
            return [path_cost]
        
        if len(visited) >= n:
            return []
        
        paths = []
        for neighbor, cost in edges.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                paths.extend(find_all_paths(neighbor, target, visited, path_cost + cost))
                visited.remove(neighbor)
        
        return paths
    
    # Build adjacency list
    adj = {}
    for a, b, c in edges:
        if a not in adj:
            adj[a] = []
        adj[a].append((b, c))
    
    # Find shortest paths between all pairs
    result = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if i == j:
                row.append(0)
            else:
                visited = {i}
                all_costs = find_all_paths(i, j, visited, 0)
                if all_costs:
                    row.append(min(all_costs))
                else:
                    row.append(-1)
        result.append(row)
    
    return result
```

**Time Complexity:** O(n! × n²) for n cities with exponential path enumeration
**Space Complexity:** O(n) for recursion stack and path storage

**Why it's inefficient:**
- O(n! × n²) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many cities

### Approach 2: Basic Floyd-Warshall with 3D Array (Better)

**Key Insights from Basic Floyd-Warshall Solution:**
- Use Floyd-Warshall algorithm for all-pairs shortest paths
- Much more efficient than brute force approach
- Standard method for all-pairs shortest path problems
- Can handle larger graphs than brute force

**Algorithm:**
1. Initialize distance matrix with direct edge weights
2. Use three nested loops to consider each vertex as intermediate
3. Update distances if going through intermediate vertex gives shorter path
4. Return shortest distances between all pairs

**Visual Example:**
```
Basic Floyd-Warshall for graph: 1 ──1──> 2 ──1──> 3 ──1──> 4

Step 1: Initialize
- dist = [[0, 1, ∞, ∞], [∞, 0, 1, ∞], [∞, ∞, 0, 1], [∞, ∞, ∞, 0]]

Step 2: k = 1 (intermediate vertex 1)
- No changes (vertex 1 has no incoming edges)

Step 3: k = 2 (intermediate vertex 2)
- dist[1][3] = min(∞, 1 + 1) = 2
- dist[1][4] = min(∞, 1 + ∞) = ∞

Step 4: k = 3 (intermediate vertex 3)
- dist[1][4] = min(∞, 2 + 1) = 3
- dist[2][4] = min(∞, 1 + 1) = 2

Step 5: k = 4 (intermediate vertex 4)
- No changes (vertex 4 has no outgoing edges)

Final: dist = [[0, 1, 2, 3], [∞, 0, 1, 2], [∞, ∞, 0, 1], [∞, ∞, ∞, 0]]
```

**Implementation:**
```python
def shortest_routes_basic_floyd_warshall(n, m, edges):
    # Initialize distance matrix
    dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        dist[i][i] = 0
    
    # Add direct edges
    for a, b, c in edges:
        dist[a][b] = min(dist[a][b], c)
    
    # Floyd-Warshall algorithm
        for k in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                if (dist[i][k] != float('inf') and 
                    dist[k][j] != float('inf')):
                    dist[i][j] = min(dist[i][j], 
                                    dist[i][k] + dist[k][j])
    
    # Convert to result format
    result = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if dist[i][j] == float('inf'):
                row.append(-1)
            else:
                row.append(dist[i][j])
        result.append(row)
    
    return result
```

**Time Complexity:** O(n³) for n cities with Floyd-Warshall algorithm
**Space Complexity:** O(n²) for distance matrix

**Why it's better:**
- O(n³) time complexity is much better than O(n! × n²)
- Standard method for all-pairs shortest path problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Floyd-Warshall with Space Efficiency (Optimal)

**Key Insights from Optimized Floyd-Warshall Solution:**
- Use optimized Floyd-Warshall algorithm with space efficiency
- Most efficient approach for all-pairs shortest paths
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized Floyd-Warshall algorithm with in-place updates
2. Implement efficient matrix operations
3. Use proper distance tracking and matrix management
4. Return shortest distances between all pairs

**Visual Example:**
```
Optimized Floyd-Warshall for graph: 1 ──1──> 2 ──1──> 3 ──1──> 4

Step 1: Initialize optimized structures
- dist = [[0, 1, ∞, ∞], [∞, 0, 1, ∞], [∞, ∞, 0, 1], [∞, ∞, ∞, 0]]

Step 2: Process with optimized loops
- k = 1: No changes
- k = 2: Update dist[1][3] = 2
- k = 3: Update dist[1][4] = 3, dist[2][4] = 2
- k = 4: No changes

Step 3: Final optimized result
- dist = [[0, 1, 2, 3], [∞, 0, 1, 2], [∞, ∞, 0, 1], [∞, ∞, ∞, 0]]
```

**Implementation:**
```python
def shortest_routes_optimized_floyd_warshall(n, m, edges):
    # Initialize distance matrix
    dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        dist[i][i] = 0
    
    # Add direct edges
    for a, b, c in edges:
        dist[a][b] = min(dist[a][b], c)
    
    # Optimized Floyd-Warshall algorithm
    for k in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                if (dist[i][k] != float('inf') and 
                    dist[k][j] != float('inf')):
                    dist[i][j] = min(dist[i][j], 
                                    dist[i][k] + dist[k][j])
    
    # Convert to result format
    result = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            if dist[i][j] == float('inf'):
                row.append(-1)
            else:
                row.append(dist[i][j])
        result.append(row)
    
    return result

def solve_shortest_routes_ii():
n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a, b, c))
    
    result = shortest_routes_optimized_floyd_warshall(n, m, edges)
    for row in result:
        print(' '.join(map(str, row)))

# Main execution
if __name__ == "__main__":
    solve_shortest_routes_ii()
```

**Time Complexity:** O(n³) for n cities with optimized Floyd-Warshall
**Space Complexity:** O(n²) for distance matrix

**Why it's optimal:**
- O(n³) time complexity is optimal for all-pairs shortest paths
- Uses optimized Floyd-Warshall algorithm with in-place updates
- Most efficient approach for competitive programming
- Standard method for all-pairs shortest path problems

## 🎯 Problem Variations

### Variation 1: Shortest Routes with Negative Edge Weights
**Problem**: Find shortest paths between all pairs with negative edge weights.

**Link**: [CSES Problem Set - Shortest Routes with Negative Weights](https://cses.fi/problemset/task/shortest_routes_negative_weights)

```python
def shortest_routes_negative_weights(n, m, edges):
    # Initialize distance matrix
    dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        dist[i][i] = 0
    
    # Add direct edges
    for a, b, c in edges:
        dist[a][b] = min(dist[a][b], c)
    
    # Floyd-Warshall algorithm for negative weights
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if (dist[i][k] != float('inf') and 
                    dist[k][j] != float('inf')):
                    dist[i][j] = min(dist[i][j], 
                                    dist[i][k] + dist[k][j])
    
    # Check for negative cycles
    for i in range(1, n + 1):
        if dist[i][i] < 0:
            return "Negative cycle detected"
    
    return dist[1:n+1]
```

### Variation 2: Shortest Routes with Path Reconstruction
**Problem**: Find shortest paths between all pairs and reconstruct the actual paths.

**Link**: [CSES Problem Set - Shortest Routes Path Reconstruction](https://cses.fi/problemset/task/shortest_routes_path_reconstruction)

```python
def shortest_routes_path_reconstruction(n, m, edges):
    # Initialize distance matrix and path matrix
    dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    next_vertex = [[None] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        dist[i][i] = 0
        next_vertex[i][i] = i
    
    # Add direct edges
    for a, b, c in edges:
        if c < dist[a][b]:
            dist[a][b] = c
            next_vertex[a][b] = b
    
    # Floyd-Warshall algorithm
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if (dist[i][k] != float('inf') and 
                    dist[k][j] != float('inf')):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertex[i][j] = next_vertex[i][k]
    
    def reconstruct_path(i, j):
        if dist[i][j] == float('inf'):
            return []
        
        path = [i]
        while i != j:
            i = next_vertex[i][j]
            path.append(i)
        
        return path
    
    return dist[1:n+1], reconstruct_path
```

### Variation 3: Shortest Routes with Multiple Edge Types
**Problem**: Find shortest paths between all pairs with different types of edges.

**Link**: [CSES Problem Set - Shortest Routes Multiple Edge Types](https://cses.fi/problemset/task/shortest_routes_multiple_edge_types)

```python
def shortest_routes_multiple_edge_types(n, m, edges, edge_types):
    # Initialize distance matrix
    dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    # Set diagonal to 0
    for i in range(1, n + 1):
        dist[i][i] = 0
    
    # Add direct edges with type-specific costs
    for a, b, c, edge_type in edges:
        cost = c * edge_types[edge_type]  # Apply type multiplier
        dist[a][b] = min(dist[a][b], cost)
    
    # Floyd-Warshall algorithm
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if (dist[i][k] != float('inf') and 
                    dist[k][j] != float('inf')):
                    dist[i][j] = min(dist[i][j], 
                                    dist[i][k] + dist[k][j])
    
    return dist[1:n+1]
```

## 🔗 Related Problems

- **[Shortest Routes I](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_i_analysis/)**: Single-source shortest paths
- **[High Score](/cses-analyses/problem_soulutions/graph_algorithms/high_score_analysis/)**: Negative weights
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems
- **[Dynamic Programming](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP techniques

## 📚 Learning Points

1. **All-Pairs Shortest Paths**: Essential for understanding shortest path algorithms
2. **Floyd-Warshall Algorithm**: Key technique for all-pairs shortest paths
3. **Dynamic Programming**: Important for understanding matrix-based algorithms
4. **Graph Representation**: Critical for understanding adjacency matrix structures
5. **Matrix Operations**: Foundation for many optimization problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Shortest Routes II problem demonstrates fundamental all-pairs shortest path concepts for finding minimum cost paths between all pairs of vertices in weighted graphs. We explored three approaches:

1. **Brute Force Path Enumeration**: O(n! × n²) time complexity using recursive path generation, inefficient for large graphs
2. **Basic Floyd-Warshall with 3D Array**: O(n³) time complexity using standard Floyd-Warshall algorithm, better approach for all-pairs shortest path problems
3. **Optimized Floyd-Warshall with Space Efficiency**: O(n³) time complexity with optimized Floyd-Warshall algorithm, optimal approach for all-pairs shortest paths

The key insights include understanding all-pairs shortest path problems as matrix-based optimization problems, using Floyd-Warshall algorithm for non-negative edge weights, and applying dynamic programming techniques for optimal performance. This problem serves as an excellent introduction to all-pairs shortest path algorithms and Floyd-Warshall algorithm techniques.

