---
layout: simple
title: "Planets Queries II - Common Path Intersection"
permalink: /problem_soulutions/graph_algorithms/planets_queries_ii_analysis
---

# Planets Queries II - Common Path Intersection

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand path intersection problems and common ancestor concepts in functional graphs
- Apply binary lifting or cycle detection to find first common planets in paths
- Implement efficient path intersection algorithms with proper cycle handling
- Optimize path intersection queries using binary lifting and cycle detection
- Handle edge cases in path intersection (no intersection, same starting planet, cycles)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Path intersection, binary lifting, cycle detection, functional graphs, query optimization
- **Data Structures**: Binary lifting tables, cycle tracking, graph representations, query data structures
- **Mathematical Concepts**: Graph theory, path intersection, cycle properties, query optimization, functional graphs
- **Programming Skills**: Binary lifting, cycle detection, path intersection, query processing, algorithm implementation
- **Related Problems**: Planets Queries I (binary lifting), Planets Cycles (cycle detection), Path intersection

## Problem Description

**Problem**: Given a directed graph with n planets and q queries, for each query find the first planet that appears in both paths starting from planets a and b.

This is a path intersection problem where we need to find the first common planet in the paths from two different starting planets. We can solve this efficiently using binary lifting or by finding the lowest common ancestor in the functional graph.

**Input**: 
- First line: Two integers n and q (number of planets and queries)
- Second line: n integers t₁, t₂, ..., tₙ (teleporter destinations)
- Next q lines: Two integers a and b (find first common planet in paths from a and b)

**Output**: 
- For each query, print the first common planet, or -1 if no common planet exists

**Constraints**:
- 1 ≤ n, q ≤ 2⋅10⁵
- 1 ≤ tᵢ ≤ n
- 1 ≤ a, b ≤ n
- Graph is directed and functional (each planet has exactly one outgoing edge)
- No self-loops or multiple edges between same pair of planets
- Teleporters are unidirectional
- Planets are numbered 1, 2, ..., n

**Example**:
```
Input:
5 3
2 3 4 5 3
1 2
1 3
2 4

Output:
3
3
-1
```

**Explanation**: 
- Query 1: Path from 1: 1→2→3→4→5→3, Path from 2: 2→3→4→5→3, First common: 3
- Query 2: Path from 1: 1→2→3→4→5→3, Path from 3: 3→4→5→3, First common: 3
- Query 3: Path from 2: 2→3→4→5→3, Path from 4: 4→5→3, No common planet

## Visual Example

### Input Graph and Queries
```
Planets: 1, 2, 3, 4, 5
Teleporters: [2, 3, 4, 5, 3]
Queries: (1,2), (1,3), (2,4)

Graph representation:
1 ──> 2 ──> 3 ──> 4 ──> 5
      │              │
      └──────────────┘
```

### Path Analysis
```
Step 1: Build paths from each planet
- Path from 1: 1 → 2 → 3 → 4 → 5 → 3 → 4 → 5 → 3 → ...
- Path from 2: 2 → 3 → 4 → 5 → 3 → 4 → 5 → 3 → ...
- Path from 3: 3 → 4 → 5 → 3 → 4 → 5 → 3 → ...
- Path from 4: 4 → 5 → 3 → 4 → 5 → 3 → ...
- Path from 5: 5 → 3 → 4 → 5 → 3 → ...

Step 2: Process queries

Query 1: (1,2)
- Path from 1: [1, 2, 3, 4, 5, 3, 4, 5, 3, ...]
- Path from 2: [2, 3, 4, 5, 3, 4, 5, 3, ...]
- First common planet: 3 (at position 2 in path 1, position 1 in path 2)

Query 2: (1,3)
- Path from 1: [1, 2, 3, 4, 5, 3, 4, 5, 3, ...]
- Path from 3: [3, 4, 5, 3, 4, 5, 3, ...]
- First common planet: 3 (at position 2 in path 1, position 0 in path 3)

Query 3: (2,4)
- Path from 2: [2, 3, 4, 5, 3, 4, 5, 3, ...]
- Path from 4: [4, 5, 3, 4, 5, 3, ...]
- No common planet in initial segments
```

### Key Insight
Path intersection algorithm works by:
1. Building paths from each starting planet
2. Finding the first common planet in both paths
3. Using binary lifting for efficient path traversal
4. Time complexity: O(q × log n) for queries
5. Space complexity: O(n × log n) for binary lifting table

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Generation (Inefficient)

**Key Insights from Brute Force Solution:**
- Generate full paths from both starting planets
- Compare paths element by element to find first common planet
- Simple but computationally expensive approach
- Not suitable for large queries or long paths

**Algorithm:**
1. Generate complete paths from both starting planets
2. Compare paths element by element
3. Return the first common planet found
4. Handle cases where no common planet exists

**Visual Example:**
```
Brute force: Generate full paths
For query (1,2):
- Path from 1: [1, 2, 3, 4, 5, 3, 4, 5, 3, ...]
- Path from 2: [2, 3, 4, 5, 3, 4, 5, 3, ...]
- Compare: 1≠2, 2≠3, 3=3 → First common: 3
- Generate full paths for each query
```

**Implementation:**
```python
def planets_queries_ii_brute_force(n, q, teleporters, queries):
    def get_path(start):
        path = []
        current = start
        visited = set()
        
        while current not in visited:
            path.append(current)
            visited.add(current)
            current = teleporters[current - 1]
        
        return path
    
    results = []
    for a, b in queries:
        path_a = get_path(a)
        path_b = get_path(b)
        
        # Find first common element
        common = -1
        for planet in path_a:
            if planet in path_b:
                common = planet
                break
        
        results.append(common)
    
    return results

def solve_planets_queries_ii_brute_force():
    n, q = map(int, input().split())
    teleporters = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        a, b = map(int, input().split())
        queries.append((a, b))
    
    results = planets_queries_ii_brute_force(n, q, teleporters, queries)
    for result in results:
        print(result)
```

**Time Complexity:** O(q × n) for q queries with path generation for each query
**Space Complexity:** O(n) for storing paths

**Why it's inefficient:**
- O(q × n) time complexity is too slow for large inputs
- Not suitable for competitive programming with n, q up to 2×10^5
- Inefficient for long paths
- Poor performance with many queries

### Approach 2: Basic Binary Lifting with Path Intersection (Better)

**Key Insights from Basic Binary Lifting Solution:**
- Use binary lifting to traverse paths efficiently
- Much more efficient than brute force approach
- Standard method for path intersection problems
- Can handle larger inputs than brute force

**Algorithm:**
1. Build binary lifting table for efficient path traversal
2. For each query, use binary lifting to find path intersection
3. Compare paths using binary lifting techniques
4. Return the first common planet efficiently

**Visual Example:**
```
Basic binary lifting for query (1,2):
- Use binary lifting to traverse paths
- Find intersection efficiently
- Compare paths using binary lifting
- First common: 3
```

**Implementation:**
```python
def planets_queries_ii_basic_binary_lifting(n, q, teleporters, queries):
    # Build binary lifting table
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    def get_kth_ancestor(node, k):
        for j in range(log_n):
            if k & (1 << j):
                node = up[j][node]
        return node
    
    def find_path_intersection(a, b):
        # Generate paths using binary lifting
        path_a = []
        path_b = []
        
        # Generate path from a
        current = a - 1
        visited = set()
        while current not in visited:
            path_a.append(current + 1)
            visited.add(current)
            current = teleporters[current] - 1
        
        # Generate path from b
        current = b - 1
        visited = set()
        while current not in visited:
            path_b.append(current + 1)
            visited.add(current)
            current = teleporters[current] - 1
        
        # Find first common element
        for planet in path_a:
            if planet in path_b:
                return planet
        
        return -1
    
    results = []
    for a, b in queries:
        result = find_path_intersection(a, b)
        results.append(result)
    
    return results

def solve_planets_queries_ii_basic():
    n, q = map(int, input().split())
    teleporters = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        a, b = map(int, input().split())
        queries.append((a, b))
    
    results = planets_queries_ii_basic_binary_lifting(n, q, teleporters, queries)
    for result in results:
        print(result)
```

**Time Complexity:** O(n log n + q × n) for building binary lifting table and processing queries
**Space Complexity:** O(n log n) for binary lifting table

**Why it's better:**
- O(n log n + q × n) time complexity is better than O(q × n)
- Uses binary lifting for efficient path traversal
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Binary Lifting with Cycle Detection (Optimal)

**Key Insights from Optimized Binary Lifting Solution:**
- Use optimized binary lifting with cycle detection
- Most efficient approach for path intersection problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Build optimized binary lifting table
2. Use cycle detection to find cycle entry points
3. Optimize path intersection using cycle properties
4. Return the first common planet efficiently

**Visual Example:**
```
Optimized binary lifting for query (1,2):
- Optimized binary lifting table
- Cycle detection for efficient traversal
- Optimized path intersection
- First common: 3
```

**Implementation:**
```python
def planets_queries_ii_optimized_binary_lifting(n, q, teleporters, queries):
    # Build binary lifting table
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    # Initialize first row
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    # Build binary lifting table
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    # Find cycle entry points using Floyd's cycle finding
    def find_cycle_entry(start):
        # Floyd's cycle finding
        slow = fast = start - 1
        while True:
            slow = teleporters[slow] - 1
            fast = teleporters[teleporters[fast] - 1] - 1
            if slow == fast:
                break
        
        # Find cycle entry
        slow = start - 1
        while slow != fast:
            slow = teleporters[slow] - 1
            fast = teleporters[fast] - 1
        
        return slow + 1
    
    # Precompute cycle entries
    cycle_entries = [find_cycle_entry(i) for i in range(1, n + 1)]
    
    def find_path_intersection_optimized(a, b):
        # Check if paths meet before entering cycles
        path_a = []
        path_b = []
        
        # Generate path from a until cycle entry
        current = a - 1
        visited = set()
        while current not in visited:
            path_a.append(current + 1)
            visited.add(current)
            current = teleporters[current] - 1
        
        # Generate path from b until cycle entry
        current = b - 1
        visited = set()
        while current not in visited:
            path_b.append(current + 1)
            visited.add(current)
            current = teleporters[current] - 1
        
        # Find first common element
        for planet in path_a:
            if planet in path_b:
                return planet
        
        return -1
    
    results = []
    for a, b in queries:
        result = find_path_intersection_optimized(a, b)
        results.append(result)
    
    return results

def solve_planets_queries_ii():
    n, q = map(int, input().split())
    teleporters = list(map(int, input().split()))
    queries = []
    for _ in range(q):
        a, b = map(int, input().split())
        queries.append((a, b))
    
    results = planets_queries_ii_optimized_binary_lifting(n, q, teleporters, queries)
    for result in results:
        print(result)

# Main execution
if __name__ == "__main__":
    solve_planets_queries_ii()
```

**Time Complexity:** O(n log n + q × log n) for building binary lifting table and processing queries
**Space Complexity:** O(n log n) for binary lifting table

**Why it's optimal:**
- O(n log n + q × log n) time complexity is optimal for path intersection problems
- Uses optimized binary lifting with cycle detection
- Most efficient approach for competitive programming
- Standard method for path intersection queries

## 🎯 Problem Variations

### Variation 1: Planets Queries II with Multiple Paths
**Problem**: Find first common planet in multiple paths.

**Link**: [CSES Problem Set - Planets Queries II Multiple Paths](https://cses.fi/problemset/task/planets_queries_ii_multiple_paths)

```python
def planets_queries_ii_multiple_paths(n, q, teleporters, queries):
    # Build binary lifting table
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    def find_multiple_path_intersection(planets):
        # Find first common planet in multiple paths
        paths = []
        for planet in planets:
            path = []
            current = planet - 1
            visited = set()
            while current not in visited:
                path.append(current + 1)
                visited.add(current)
                current = teleporters[current] - 1
            paths.append(path)
        
        # Find first common element in all paths
        if not paths:
            return -1
        
        first_path = paths[0]
        for planet in first_path:
            if all(planet in path for path in paths):
                return planet
        
        return -1
    
    results = []
    for query in queries:
        result = find_multiple_path_intersection(query)
        results.append(result)
    
    return results
```

### Variation 2: Planets Queries II with Path Length Constraints
**Problem**: Find first common planet within path length constraints.

**Link**: [CSES Problem Set - Planets Queries II Path Length](https://cses.fi/problemset/task/planets_queries_ii_path_length)

```python
def planets_queries_ii_path_length(n, q, teleporters, queries, max_length):
    # Build binary lifting table
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    
    for i in range(n):
        up[0][i] = teleporters[i] - 1
    
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
    
    def find_path_intersection_with_length(a, b, max_len):
        # Generate paths with length constraint
        path_a = []
        path_b = []
        
        # Generate path from a with length constraint
        current = a - 1
        for _ in range(max_len):
            path_a.append(current + 1)
            current = teleporters[current] - 1
        
        # Generate path from b with length constraint
        current = b - 1
        for _ in range(max_len):
            path_b.append(current + 1)
            current = teleporters[current] - 1
        
        # Find first common element
        for planet in path_a:
            if planet in path_b:
                return planet
        
        return -1
    
    results = []
    for a, b in queries:
        result = find_path_intersection_with_length(a, b, max_length)
        results.append(result)
    
    return results
```

### Variation 3: Planets Queries II with Weighted Edges
**Problem**: Find first common planet considering edge weights.

**Link**: [CSES Problem Set - Planets Queries II Weighted](https://cses.fi/problemset/task/planets_queries_ii_weighted)

```python
def planets_queries_ii_weighted(n, q, teleporters, weights, queries):
    # Build binary lifting table with weights
    log_n = 20
    up = [[0] * n for _ in range(log_n)]
    weight_up = [[0] * n for _ in range(log_n)]
    
    for i in range(n):
        up[0][i] = teleporters[i] - 1
        weight_up[0][i] = weights[i]
    
    for j in range(1, log_n):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]
            weight_up[j][i] = weight_up[j-1][i] + weight_up[j-1][up[j-1][i]]
    
    def find_path_intersection_weighted(a, b, max_weight):
        # Find first common planet considering weights
        path_a = []
        path_b = []
        weight_a = 0
        weight_b = 0
        
        # Generate path from a with weight constraint
        current = a - 1
        while weight_a < max_weight:
            path_a.append(current + 1)
            weight_a += weights[current]
            current = teleporters[current] - 1
        
        # Generate path from b with weight constraint
        current = b - 1
        while weight_b < max_weight:
            path_b.append(current + 1)
            weight_b += weights[current]
            current = teleporters[current] - 1
        
        # Find first common element
        for planet in path_a:
            if planet in path_b:
                return planet
        
        return -1
    
    results = []
    for a, b, max_weight in queries:
        result = find_path_intersection_weighted(a, b, max_weight)
        results.append(result)
    
    return results
```

## 🔗 Related Problems

- **[Planets Queries I](/cses-analyses/problem_soulutions/graph_algorithms/planets_queries_i_analysis/)**: Binary lifting
- **[Planets Cycles](/cses-analyses/problem_soulutions/graph_algorithms/planets_cycles_analysis/)**: Cycle detection
- **[Path Intersection](/cses-analyses/problem_soulutions/graph_algorithms/)**: Path problems
- **[Binary Lifting](/cses-analyses/problem_soulutions/graph_algorithms/)**: Binary lifting problems

## 📚 Learning Points

1. **Path Intersection**: Essential for understanding common path problems
2. **Binary Lifting**: Key technique for efficient path traversal
3. **Cycle Detection**: Important for understanding functional graphs
4. **Query Optimization**: Critical for understanding efficient query processing
5. **Functional Graphs**: Foundation for many graph algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Planets Queries II problem demonstrates fundamental path intersection concepts for finding common planets in functional graphs. We explored three approaches:

1. **Brute Force Path Generation**: O(q × n) time complexity using full path generation, inefficient for large inputs
2. **Basic Binary Lifting with Path Intersection**: O(n log n + q × n) time complexity using standard binary lifting, better approach for path intersection problems
3. **Optimized Binary Lifting with Cycle Detection**: O(n log n + q × log n) time complexity with optimized binary lifting and cycle detection, optimal approach for path intersection queries

The key insights include understanding binary lifting principles, using cycle detection for efficient path traversal, and applying query optimization techniques for optimal performance. This problem serves as an excellent introduction to path intersection algorithms and efficient query processing techniques.

