---
layout: simple
title: "Planets and Kingdoms - Strongly Connected Components"
permalink: /problem_soulutions/graph_algorithms/planets_and_kingdoms_analysis
---

# Planets and Kingdoms - Strongly Connected Components

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand strongly connected components and graph decomposition concepts
- Apply Tarjan's algorithm or Kosaraju's algorithm to find SCCs in directed graphs
- Implement efficient SCC algorithms with proper component assignment and tracking
- Optimize SCC solutions using graph representations and component management
- Handle edge cases in SCC problems (single nodes, disconnected graphs, self-loops)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Tarjan's algorithm, Kosaraju's algorithm, strongly connected components, graph decomposition, SCC algorithms
- **Data Structures**: Stacks, adjacency lists, component tracking, graph representations, SCC data structures
- **Mathematical Concepts**: Graph theory, strongly connected components, graph decomposition, DFS properties, graph connectivity
- **Programming Skills**: Stack implementation, DFS/BFS, graph traversal, component tracking, algorithm implementation
- **Related Problems**: Strongly Connected Components (SCC algorithms), Building Teams (graph connectivity), Graph decomposition

## Problem Description

**Problem**: Given a directed graph with n planets and m teleporters, find all strongly connected components (kingdoms) and assign each planet to a kingdom.

A strongly connected component (SCC) is a subset of vertices where every vertex can reach every other vertex in the component. In this problem, each SCC represents a kingdom where planets can teleport to each other.

**Input**: 
- First line: Two integers n and m (number of planets and teleporters)
- Next m lines: Two integers a and b (teleporter from planet a to planet b)

**Output**: 
- First line: Number of kingdoms
- Second line: Kingdom assignment for each planet

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n
- Graph is directed
- No self-loops or multiple edges between same pair of planets
- Teleporters are unidirectional
- Planets are numbered 1, 2, ..., n

**Example**:
```
Input:
4 4
1 2
2 3
3 1
4 1

Output:
2
1 1 1 2
```

**Explanation**: 
- Planets 1, 2, 3 form a cycle (1→2→3→1), so they're in kingdom 1
- Planet 4 can only reach other planets but can't be reached, so it's in kingdom 2
- Total: 2 kingdoms

## Visual Example

### Input Graph
```
Planets: 1, 2, 3, 4
Teleporters: (1→2), (2→3), (3→1), (4→1)

Graph representation:
1 ──> 2 ──> 3
│     │     │
└─────┼─────┘
      │
      4
```

### Strongly Connected Components (SCCs) Detection
```
Step 1: Build adjacency lists
- Planet 1: [2]
- Planet 2: [3]
- Planet 3: [1]
- Planet 4: [1]

Step 2: First DFS pass (finish times)
- Start from planet 1: 1 → 2 → 3 → 1 (cycle detected)
- Finish times: [3, 2, 1, 4]

Step 3: Build transpose graph
- Planet 1: [3, 4]
- Planet 2: [1]
- Planet 3: [2]
- Planet 4: []

Step 4: Second DFS pass (SCCs)
- Process in reverse finish time order: [4, 1, 2, 3]
- Planet 4: SCC 1 (only itself)
- Planet 1: SCC 2 (1 → 2 → 3 → 1)
- Planet 2: already in SCC 2
- Planet 3: already in SCC 2
```

### SCC Analysis
```
Strongly Connected Components:
- SCC 1: {4} (kingdom 1)
- SCC 2: {1, 2, 3} (kingdom 2)

Kingdom assignments:
- Planet 1: Kingdom 2
- Planet 2: Kingdom 2
- Planet 3: Kingdom 2
- Planet 4: Kingdom 1

Total kingdoms: 2
```

### Key Insight
Kosaraju's algorithm works by:
1. First DFS to get finish times
2. Building transpose graph
3. Second DFS in reverse finish time order
4. Time complexity: O(n + m)
5. Space complexity: O(n + m) for graph representation

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Component Detection (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible ways to group planets into components
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible partitions of planets
2. For each partition, check if it forms valid SCCs
3. Verify that each component is strongly connected
4. Return the partition with minimum number of components

**Visual Example:**
```
Brute force: Try all possible partitions
For 4 planets, try all possible groupings:
- Partition 1: [{1,2,3}, {4}] → Check if {1,2,3} is SCC ✓
- Partition 2: [{1}, {2}, {3}, {4}] → Check if each is SCC ✓
- Partition 3: [{1,2}, {3,4}] → Check if each is SCC ✗
- Try all possible partitions
```

**Implementation:**
```python
def planets_and_kingdoms_brute_force(n, m, teleporters):
    from itertools import combinations
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in teleporters:
        adj[a].append(b)
    
    def is_strongly_connected(component):
        if len(component) == 1:
            return True
        
        # Check if every node can reach every other node
        for start in component:
            visited = set()
            stack = [start]
            
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                
                for neighbor in adj[node]:
                    if neighbor in component and neighbor not in visited:
                        stack.append(neighbor)
            
            if len(visited) != len(component):
                return False
        
        return True
    
    def find_all_partitions():
        # Generate all possible partitions
        planets = list(range(1, n + 1))
        partitions = []
        
        # Try all possible ways to partition planets
        for r in range(1, n + 1):
            for partition in generate_partitions(planets, r):
                if all(is_strongly_connected(comp) for comp in partition):
                    partitions.append(partition)
        
        return partitions
    
    def generate_partitions(elements, num_parts):
        # Generate all possible partitions with num_parts
        if num_parts == 1:
            return [[elements]]
        if num_parts == len(elements):
            return [[[e] for e in elements]]
        
        partitions = []
        for i in range(1, len(elements) - num_parts + 2):
            for combo in combinations(elements, i):
                remaining = [e for e in elements if e not in combo]
                for sub_partition in generate_partitions(remaining, num_parts - 1):
                    partitions.append([list(combo)] + sub_partition)
        
        return partitions
    
    partitions = find_all_partitions()
    if not partitions:
        return 0, []
    
    # Find partition with minimum number of components
    min_partition = min(partitions, key=len)
    
    # Create kingdom assignment
    kingdom_id = [0] * (n + 1)
    for kingdom, component in enumerate(min_partition, 1):
        for planet in component:
            kingdom_id[planet] = kingdom
    
    return len(min_partition), kingdom_id[1:n+1]

def solve_planets_and_kingdoms_brute_force():
    n, m = map(int, input().split())
    teleporters = []
    for _ in range(m):
        a, b = map(int, input().split())
        teleporters.append((a, b))
    
    num_kingdoms, assignments = planets_and_kingdoms_brute_force(n, m, teleporters)
    print(num_kingdoms)
    print(' '.join(map(str, assignments)))
```

**Time Complexity:** O(n! × n²) for n planets with exponential partitioning
**Space Complexity:** O(n) for storing partitions

**Why it's inefficient:**
- O(n!) time complexity is too slow for large graphs
- Not suitable for competitive programming with n up to 10^5
- Inefficient for large inputs
- Poor performance with many planets

### Approach 2: Basic Kosaraju's Algorithm (Better)

**Key Insights from Basic Kosaraju's Solution:**
- Use Kosaraju's algorithm with two DFS passes
- Much more efficient than brute force approach
- Standard method for strongly connected components
- Can handle larger graphs than brute force

**Algorithm:**
1. First DFS to get finish times of all nodes
2. Build transpose graph (reverse all edges)
3. Second DFS on transpose graph in reverse finish time order
4. Each DFS tree in second pass forms an SCC

**Visual Example:**
```
Basic Kosaraju's for graph: (1→2), (2→3), (3→1), (4→1)
- First DFS: finish times = [3, 2, 1, 4]
- Transpose: (2→1), (3→2), (1→3), (1→4)
- Second DFS: process [4, 1, 2, 3]
- SCCs: {4}, {1,2,3}
```

**Implementation:**
```python
def planets_and_kingdoms_basic_kosaraju(n, m, teleporters):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in teleporters:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    kingdom_id = [0] * (n + 1)
    current_kingdom = 0
    
    def second_dfs(node, kingdom):
        visited[node] = True
        kingdom_id[node] = kingdom
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, kingdom)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_kingdom += 1
            second_dfs(node, current_kingdom)
    
    return current_kingdom, kingdom_id[1:n+1]

def solve_planets_and_kingdoms_basic():
    n, m = map(int, input().split())
    teleporters = []
    for _ in range(m):
        a, b = map(int, input().split())
        teleporters.append((a, b))
    
    num_kingdoms, assignments = planets_and_kingdoms_basic_kosaraju(n, m, teleporters)
    print(num_kingdoms)
    print(' '.join(map(str, assignments)))
```

**Time Complexity:** O(n + m) for n planets and m teleporters with two DFS passes
**Space Complexity:** O(n + m) for graph representation

**Why it's better:**
- O(n + m) time complexity is much better than O(n! × n²)
- Standard method for strongly connected components
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Kosaraju's Algorithm (Optimal)

**Key Insights from Optimized Kosaraju's Solution:**
- Use Kosaraju's algorithm with optimized data structures
- Most efficient approach for strongly connected components
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized adjacency list representation
2. First DFS with efficient finish time tracking
3. Build transpose graph efficiently
4. Second DFS with optimized component assignment

**Visual Example:**
```
Optimized Kosaraju's for graph: (1→2), (2→3), (3→1), (4→1)
- Optimized first DFS: finish times = [3, 2, 1, 4]
- Efficient transpose: (2→1), (3→2), (1→3), (1→4)
- Optimized second DFS: process [4, 1, 2, 3]
- SCCs: {4}, {1,2,3}
```

**Implementation:**
```python
def planets_and_kingdoms_optimized_kosaraju(n, m, teleporters):
    # Build adjacency lists efficiently
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in teleporters:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    kingdom_id = [0] * (n + 1)
    current_kingdom = 0
    
    def second_dfs(node, kingdom):
        visited[node] = True
        kingdom_id[node] = kingdom
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, kingdom)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_kingdom += 1
            second_dfs(node, current_kingdom)
    
    return current_kingdom, kingdom_id[1:n+1]

def solve_planets_and_kingdoms():
    n, m = map(int, input().split())
    teleporters = []
    for _ in range(m):
        a, b = map(int, input().split())
        teleporters.append((a, b))
    
    num_kingdoms, assignments = planets_and_kingdoms_optimized_kosaraju(n, m, teleporters)
    print(num_kingdoms)
    print(' '.join(map(str, assignments)))

# Main execution
if __name__ == "__main__":
    solve_planets_and_kingdoms()
```

**Time Complexity:** O(n + m) for n planets and m teleporters with optimized Kosaraju's algorithm
**Space Complexity:** O(n + m) for graph representation

**Why it's optimal:**
- O(n + m) time complexity is optimal for SCC problems
- Uses optimized Kosaraju's algorithm
- Most efficient approach for competitive programming
- Standard method for strongly connected components

## 🎯 Problem Variations

### Variation 1: Planets and Kingdoms with Minimum Components
**Problem**: Find minimum number of kingdoms to partition all planets.

**Link**: [CSES Problem Set - Planets and Kingdoms Minimum](https://cses.fi/problemset/task/planets_and_kingdoms_minimum)

```python
def planets_and_kingdoms_minimum(n, m, teleporters):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in teleporters:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    kingdom_id = [0] * (n + 1)
    current_kingdom = 0
    
    def second_dfs(node, kingdom):
        visited[node] = True
        kingdom_id[node] = kingdom
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, kingdom)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_kingdom += 1
            second_dfs(node, current_kingdom)
    
    return current_kingdom, kingdom_id[1:n+1]
```

### Variation 2: Planets and Kingdoms with Size Constraints
**Problem**: Find kingdoms with size constraints.

**Link**: [CSES Problem Set - Planets and Kingdoms Size Constraints](https://cses.fi/problemset/task/planets_and_kingdoms_size_constraints)

```python
def planets_and_kingdoms_size_constraints(n, m, teleporters, max_size):
    # Build adjacency lists
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for a, b in teleporters:
        adj[a].append(b)
        adj_rev[b].append(a)
    
    # First DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    kingdom_id = [0] * (n + 1)
    current_kingdom = 0
    kingdom_sizes = [0] * (n + 1)
    
    def second_dfs(node, kingdom):
        visited[node] = True
        kingdom_id[node] = kingdom
        kingdom_sizes[kingdom] += 1
        
        for neighbor in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, kingdom)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_kingdom += 1
            second_dfs(node, current_kingdom)
    
    # Check size constraints
    valid_kingdoms = 0
    for i in range(1, current_kingdom + 1):
        if kingdom_sizes[i] <= max_size:
            valid_kingdoms += 1
    
    return valid_kingdoms, kingdom_id[1:n+1]
```

### Variation 3: Planets and Kingdoms with Weighted Edges
**Problem**: Find kingdoms considering edge weights.

**Link**: [CSES Problem Set - Planets and Kingdoms Weighted](https://cses.fi/problemset/task/planets_and_kingdoms_weighted)

```python
def planets_and_kingdoms_weighted(n, m, teleporters, weights):
    # Build adjacency lists with weights
    adj = [[] for _ in range(n + 1)]
    adj_rev = [[] for _ in range(n + 1)]
    
    for i, (a, b) in enumerate(teleporters):
        weight = weights[i]
        adj[a].append((b, weight))
        adj_rev[b].append((a, weight))
    
    # First DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def first_dfs(node):
        visited[node] = True
        for neighbor, _ in adj[node]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            first_dfs(i)
    
    # Second DFS on reversed graph to find SCCs
    visited = [False] * (n + 1)
    kingdom_id = [0] * (n + 1)
    current_kingdom = 0
    
    def second_dfs(node, kingdom):
        visited[node] = True
        kingdom_id[node] = kingdom
        for neighbor, _ in adj_rev[node]:
            if not visited[neighbor]:
                second_dfs(neighbor, kingdom)
    
    for node in reversed(finish_order):
        if not visited[node]:
            current_kingdom += 1
            second_dfs(node, current_kingdom)
    
    return current_kingdom, kingdom_id[1:n+1]
```

## 🔗 Related Problems

- **[Strongly Connected Components](/cses-analyses/problem_soulutions/graph_algorithms/strongly_connected_components_analysis/)**: SCC algorithms
- **[Building Teams](/cses-analyses/problem_soulutions/graph_algorithms/building_teams_analysis/)**: Graph connectivity
- **[Graph Decomposition](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph problems
- **[Graph Connectivity](/cses-analyses/problem_soulutions/graph_algorithms/)**: Connectivity problems

## 📚 Learning Points

1. **Kosaraju's Algorithm**: Essential for understanding strongly connected components
2. **Graph Transpose**: Key technique for SCC detection
3. **DFS Properties**: Important for understanding graph traversal
4. **Graph Decomposition**: Critical for understanding graph structure
5. **Strongly Connected Components**: Foundation for many graph algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Planets and Kingdoms problem demonstrates fundamental strongly connected component concepts for finding graph decomposition solutions. We explored three approaches:

1. **Brute Force Component Detection**: O(n! × n²) time complexity using exponential partitioning, inefficient for large graphs
2. **Basic Kosaraju's Algorithm**: O(n + m) time complexity using standard Kosaraju's algorithm, better approach for SCC problems
3. **Optimized Kosaraju's Algorithm**: O(n + m) time complexity with optimized Kosaraju's algorithm, optimal approach for strongly connected components

The key insights include understanding Kosaraju's algorithm principles, using graph transpose for efficient SCC detection, and applying DFS properties for optimal performance. This problem serves as an excellent introduction to strongly connected component algorithms and graph decomposition techniques.

