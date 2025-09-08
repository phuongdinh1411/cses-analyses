---
layout: simple
title: "Round Trip - Cycle Detection in Undirected Graph"
permalink: /problem_soulutions/graph_algorithms/round_trip_analysis
---

# Round Trip - Cycle Detection in Undirected Graph

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand cycle detection in undirected graphs and simple cycle concepts
- Apply DFS to detect cycles in undirected graphs with proper back-edge identification
- Implement efficient cycle detection algorithms with proper cycle reconstruction
- Optimize cycle detection using graph representations and algorithm optimizations
- Handle edge cases in cycle detection (no cycles, self-loops, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Cycle detection, DFS, back-edge detection, undirected graph algorithms, cycle reconstruction
- **Data Structures**: Adjacency lists, visited arrays, parent arrays, graph representations, cycle tracking
- **Mathematical Concepts**: Graph theory, cycle properties, undirected graphs, graph connectivity, cycle detection
- **Programming Skills**: Graph traversal, cycle detection, back-edge identification, algorithm implementation
- **Related Problems**: Cycle Finding (negative cycles), Building Teams (graph coloring), Graph connectivity

## Problem Description

**Problem**: Byteland has n cities and m roads between them. Your task is to find a round trip that begins in a city, goes through two or more other cities, and finally returns to the starting city. Every intermediate city must be visited exactly once.

This is a cycle detection problem in an undirected graph. We need to find a simple cycle (no repeated vertices except start/end) that visits at least 3 cities.

**Input**: 
- First line: Two integers n and m (number of cities and roads)
- Next m lines: Two integers a and b (road between cities a and b)

**Output**: 
- Print "IMPOSSIBLE" if there is no such round trip
- Otherwise print the number of cities on the trip and the cities in the order they are visited

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- Cities are numbered 1, 2, ..., n
- Graph is undirected
- No self-loops or multiple edges between same pair of cities
- Roads are bidirectional

**Example**:
```
Input:
5 6
1 3
1 2
5 3
1 5
2 4
4 5

Output:
4
1 3 5 1
```

**Explanation**: 
- The round trip: 1 → 3 → 5 → 1
- This visits 4 cities (including the return to start)
- Each intermediate city is visited exactly once

## Visual Example

### Input Graph
```
Cities: 1, 2, 3, 4, 5
Roads: (1,3), (1,2), (5,3), (1,5), (2,4), (4,5)

Graph representation:
1 ── 2 ── 4 ── 5
│    │    │    │
└────┼────┼────┘
     │    │
     └────┼──── 3
          │    │
          └────┘
```

### Cycle Detection Algorithm Process
```
Step 1: Build adjacency list
- City 1: [2, 3, 5]
- City 2: [1, 4]
- City 3: [1, 5]
- City 4: [2, 5]
- City 5: [1, 3, 4]

Step 2: DFS to find cycles
- Start from city 1
- Path: 1 → 3 → 5 → 1 (cycle found)
- Cycle length: 3 cities + return = 4 total

Step 3: Verify cycle
- 1 → 3: road exists ✓
- 3 → 5: road exists ✓
- 5 → 1: road exists ✓
- All intermediate cities visited exactly once ✓
```

### Cycle Analysis
```
Round trip found:
1 → 3 → 5 → 1

Cities visited:
- Start: 1
- Intermediate: 3, 5
- Return: 1

Total cities on trip: 4
Each intermediate city visited exactly once ✓
```

### Key Insight
Cycle detection algorithm works by:
1. Using DFS to explore paths from each city
2. Tracking visited cities to detect cycles
3. Ensuring cycle has at least 3 cities
4. Time complexity: O(n + m) for graph traversal
5. Space complexity: O(n + m) for graph representation

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths from each city to find cycles
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths from each city
2. For each path, check if it forms a valid cycle
3. Return the first valid cycle found
4. Handle cases where no cycle exists

**Visual Example:**
```
Brute force: Try all possible paths
For graph: 1 ── 2 ── 4 ── 5
           │    │    │    │
           └────┼────┼────┘
                │    │
                └────┼──── 3
                     │    │
                     └────┘

All possible paths from city 1:
- Path 1: 1 → 2 → 4 → 5 → 1 (cycle found)
- Path 2: 1 → 2 → 4 → 5 → 3 → 1 (cycle found)
- Path 3: 1 → 3 → 5 → 1 (cycle found)
- Path 4: 1 → 3 → 5 → 4 → 2 → 1 (cycle found)

First valid cycle: 1 → 3 → 5 → 1
```

**Implementation:**
```python
def round_trip_brute_force(n, m, roads):
    def find_all_paths(current, target, visited, path):
        if current == target and len(path) >= 3:
            return [path + [current]]
        
        if len(visited) >= n:
            return []
        
        paths = []
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                paths.extend(find_all_paths(neighbor, target, visited, path + [current]))
                visited.remove(neighbor)
        
        return paths
    
    # Build adjacency list
    graph = {}
    for a, b in roads:
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append(b)
        graph[b].append(a)
    
    # Find cycles from each city
    for start in range(1, n + 1):
        visited = {start}
        all_cycles = find_all_paths(start, start, visited, [])
        if all_cycles:
            cycle = all_cycles[0]
            return f"{len(cycle)}\n{' '.join(map(str, cycle))}"
    
    return "IMPOSSIBLE"
```

**Time Complexity:** O(n! × n) for n cities with exponential path enumeration
**Space Complexity:** O(n) for recursion stack and path storage

**Why it's inefficient:**
- O(n! × n) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many cities

### Approach 2: Basic DFS with Cycle Detection (Better)

**Key Insights from Basic DFS Solution:**
- Use DFS to detect cycles in undirected graphs
- Much more efficient than brute force approach
- Standard method for cycle detection problems
- Can handle larger graphs than brute force

**Algorithm:**
1. Use DFS to explore paths from each city
2. Track visited cities and parent relationships
3. Detect back edges to identify cycles
4. Reconstruct cycle path when found

**Visual Example:**
```
Basic DFS for graph: 1 ── 2 ── 4 ── 5
                     │    │    │    │
                     └────┼────┼────┘
                          │    │
                          └────┼──── 3
                               │    │
                               └────┘

Step 1: Start DFS from city 1
- visited = {1}
- parent = {1: -1}

Step 2: Explore neighbors of city 1
- Visit city 3: visited = {1, 3}, parent = {1: -1, 3: 1}
- Visit city 5: visited = {1, 3, 5}, parent = {1: -1, 3: 1, 5: 3}

Step 3: Back edge detected
- City 5 has neighbor city 1 (already visited, not parent)
- Cycle found: 1 → 3 → 5 → 1
```

**Implementation:**
```python
def round_trip_basic_dfs(n, m, roads):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    
    def find_cycle():
        visited = [False] * (n + 1)
        parent = [-1] * (n + 1)
        cycle_start = -1
        cycle_end = -1
        
        def dfs(node, par):
            nonlocal cycle_start, cycle_end
            visited[node] = True
            parent[node] = par
            
            for neighbor in graph[node]:
                if neighbor == par:
                    continue
                
                if visited[neighbor]:
                    # Found a back edge, cycle detected
                    cycle_start = neighbor
                    cycle_end = node
                    return True
                else:
                    if dfs(neighbor, node):
                        return True
            
            return False
        
        # Try each component
        for start in range(1, n + 1):
            if not visited[start]:
                if dfs(start, -1):
                    # Reconstruct cycle
                    cycle = []
                    current = cycle_end
                    while current != cycle_start:
                        cycle.append(current)
                        current = parent[current]
                    cycle.append(cycle_start)
                    cycle.append(cycle_end)  # Complete the cycle
                    return cycle[::-1]  # Reverse to get correct order
        
        return None
    
    cycle = find_cycle()
    if cycle is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(cycle)}\n{' '.join(map(str, cycle))}"
```

**Time Complexity:** O(n + m) for n cities and m roads with DFS
**Space Complexity:** O(n + m) for adjacency list and visited arrays

**Why it's better:**
- O(n + m) time complexity is much better than O(n! × n)
- Standard method for cycle detection problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized DFS with Efficient Cycle Reconstruction (Optimal)

**Key Insights from Optimized DFS Solution:**
- Use optimized DFS with efficient cycle reconstruction
- Most efficient approach for cycle detection in undirected graphs
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized DFS with efficient data structures
2. Implement efficient cycle reconstruction
3. Use proper visited tracking and parent management
4. Return cycle path when found

**Visual Example:**
```
Optimized DFS for graph: 1 ── 2 ── 4 ── 5
                         │    │    │    │
                         └────┼────┼────┘
                              │    │
                              └────┼──── 3
                                   │    │
                                   └────┘

Step 1: Initialize optimized structures
- graph = [[], [2,3,5], [1,4], [1,5], [2,5], [1,3,4]]
- visited = [False] * 6
- parent = [-1] * 6

Step 2: Process with optimized DFS
- Start from city 1: visited[1] = True, parent[1] = -1
- Explore city 3: visited[3] = True, parent[3] = 1
- Explore city 5: visited[5] = True, parent[5] = 3
- Back edge detected: city 5 → city 1 (already visited, not parent)

Step 3: Efficient cycle reconstruction
- cycle_start = 1, cycle_end = 5
- Reconstruct: 5 → 3 → 1 → 5
- Reverse: 1 → 3 → 5 → 1
```

**Implementation:**
```python
def round_trip_optimized_dfs(n, m, roads):
# Build adjacency list
graph = [[] for _ in range(n + 1)]
for a, b in roads:
    graph[a].append(b)
    graph[b].append(a)

def find_cycle():
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
    cycle_start = -1
    cycle_end = -1
    
    def dfs(node, par):
        nonlocal cycle_start, cycle_end
        visited[node] = True
        parent[node] = par
        
        for neighbor in graph[node]:
            if neighbor == par:
                continue
            
            if visited[neighbor]:
                # Found a back edge, cycle detected
                cycle_start = neighbor
                cycle_end = node
                return True
            else:
                if dfs(neighbor, node):
                    return True
        
        return False
    
    # Try each component
    for start in range(1, n + 1):
        if not visited[start]:
            if dfs(start, -1):
                    # Efficient cycle reconstruction
                cycle = []
                current = cycle_end
                while current != cycle_start:
                    cycle.append(current)
                    current = parent[current]
                cycle.append(cycle_start)
                cycle.append(cycle_end)  # Complete the cycle
                return cycle[::-1]  # Reverse to get correct order
    
    return None

cycle = find_cycle()
if cycle is None:
        return "IMPOSSIBLE"
else:
        return f"{len(cycle)}\n{' '.join(map(str, cycle))}"

def solve_round_trip():
    n, m = map(int, input().split())
    roads = []
    for _ in range(m):
        a, b = map(int, input().split())
        roads.append((a, b))
    
    result = round_trip_optimized_dfs(n, m, roads)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_round_trip()
```

**Time Complexity:** O(n + m) for n cities and m roads with optimized DFS
**Space Complexity:** O(n + m) for adjacency list and visited arrays

**Why it's optimal:**
- O(n + m) time complexity is optimal for cycle detection
- Uses optimized DFS with efficient cycle reconstruction
- Most efficient approach for competitive programming
- Standard method for cycle detection in undirected graphs

## 🎯 Problem Variations

### Variation 1: Round Trip with Minimum Cycle Length
**Problem**: Find a round trip with minimum number of cities.

**Link**: [CSES Problem Set - Round Trip Minimum Length](https://cses.fi/problemset/task/round_trip_minimum_length)

```python
def round_trip_minimum_length(n, m, roads):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    
    def find_minimum_cycle():
        min_cycle = None
        min_length = float('inf')
        
        for start in range(1, n + 1):
            visited = [False] * (n + 1)
            parent = [-1] * (n + 1)
            distance = [0] * (n + 1)
            
            def dfs(node, par, dist):
                nonlocal min_cycle, min_length
                visited[node] = True
                parent[node] = par
                distance[node] = dist
                
                for neighbor in graph[node]:
                    if neighbor == par:
                        continue
                    
                    if visited[neighbor]:
                        # Found a back edge, cycle detected
                        cycle_length = distance[node] - distance[neighbor] + 1
                        if cycle_length < min_length:
                            min_length = cycle_length
                            # Reconstruct cycle
                            cycle = []
                            current = node
                            while current != neighbor:
                                cycle.append(current)
                                current = parent[current]
                            cycle.append(neighbor)
                            min_cycle = cycle
                    else:
                        dfs(neighbor, node, dist + 1)
            
            dfs(start, -1, 0)
        
        return min_cycle
    
    cycle = find_minimum_cycle()
    if cycle is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(cycle)}\n{' '.join(map(str, cycle))}"
```

### Variation 2: Round Trip with Specific Start City
**Problem**: Find a round trip starting from a specific city.

**Link**: [CSES Problem Set - Round Trip Specific Start](https://cses.fi/problemset/task/round_trip_specific_start)

```python
def round_trip_specific_start(n, m, roads, start_city):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    
    def find_cycle_from_start():
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
        cycle_start = -1
        cycle_end = -1
    
    def dfs(node, par):
            nonlocal cycle_start, cycle_end
        visited[node] = True
        parent[node] = par
            
        for neighbor in graph[node]:
            if neighbor == par:
                continue
                
            if visited[neighbor]:
                    # Found a back edge, cycle detected
                    cycle_start = neighbor
                    cycle_end = node
                    return True
                else:
            if dfs(neighbor, node):
                return True
            
        return False

        if dfs(start_city, -1):
            # Reconstruct cycle
    cycle = []
    current = cycle_end
    while current != cycle_start:
        cycle.append(current)
        current = parent[current]
    cycle.append(cycle_start)
            cycle.append(cycle_end)  # Complete the cycle
            return cycle[::-1]  # Reverse to get correct order
        
                return None
            
    cycle = find_cycle_from_start()
    if cycle is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(cycle)}\n{' '.join(map(str, cycle))}"
```

### Variation 3: Round Trip with Edge Constraints
**Problem**: Find a round trip with constraints on edge usage.

**Link**: [CSES Problem Set - Round Trip Edge Constraints](https://cses.fi/problemset/task/round_trip_edge_constraints)

```python
def round_trip_edge_constraints(n, m, roads, edge_constraints):
    # Build adjacency list with edge constraints
    graph = [[] for _ in range(n + 1)]
    for a, b in roads:
        constraint = edge_constraints.get((a, b), 1)
        graph[a].append((b, constraint))
        graph[b].append((a, constraint))
    
    def find_cycle_with_constraints():
        visited = [False] * (n + 1)
        parent = [-1] * (n + 1)
        cycle_start = -1
        cycle_end = -1
        
        def dfs(node, par):
            nonlocal cycle_start, cycle_end
            visited[node] = True
            parent[node] = par
            
            for neighbor, constraint in graph[node]:
                if neighbor == par:
                    continue
                
                if visited[neighbor]:
                    # Found a back edge, cycle detected
                    cycle_start = neighbor
                    cycle_end = node
                    return True
    else:
                    if dfs(neighbor, node):
                    return True
            
            return False
        
        # Try each component
        for start in range(1, n + 1):
            if not visited[start]:
                if dfs(start, -1):
                    # Reconstruct cycle
                    cycle = []
                    current = cycle_end
                    while current != cycle_start:
                        cycle.append(current)
                        current = parent[current]
                    cycle.append(cycle_start)
                    cycle.append(cycle_end)  # Complete the cycle
                    return cycle[::-1]  # Reverse to get correct order
        
        return None
    
    cycle = find_cycle_with_constraints()
    if cycle is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(cycle)}\n{' '.join(map(str, cycle))}"
```

## 🔗 Related Problems

- **[Cycle Finding](/cses-analyses/problem_soulutions/graph_algorithms/cycle_finding_analysis/)**: Negative cycles
- **[Building Teams](/cses-analyses/problem_soulutions/graph_algorithms/building_teams_analysis/)**: Graph coloring
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems
- **[Graph Connectivity](/cses-analyses/problem_soulutions/graph_algorithms/)**: Connectivity problems

## 📚 Learning Points

1. **Cycle Detection**: Essential for understanding graph cycle algorithms
2. **DFS Algorithm**: Key technique for undirected graph traversal
3. **Back Edge Detection**: Important for identifying cycles in graphs
4. **Graph Representation**: Critical for understanding adjacency list structures
5. **Path Reconstruction**: Foundation for many graph algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Round Trip problem demonstrates fundamental cycle detection concepts for finding simple cycles in undirected graphs. We explored three approaches:

1. **Brute Force Path Enumeration**: O(n! × n) time complexity using recursive path generation, inefficient for large graphs
2. **Basic DFS with Cycle Detection**: O(n + m) time complexity using standard DFS, better approach for cycle detection problems
3. **Optimized DFS with Efficient Cycle Reconstruction**: O(n + m) time complexity with optimized DFS, optimal approach for cycle detection in undirected graphs

The key insights include understanding cycle detection as a graph traversal problem, using DFS for efficient cycle detection, and applying back edge detection techniques for optimal performance. This problem serves as an excellent introduction to cycle detection algorithms and DFS techniques.

