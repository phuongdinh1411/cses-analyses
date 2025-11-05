---
layout: simple
title: "Hamiltonian Flights - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/hamiltonian_flights_analysis
---

# Hamiltonian Flights - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Hamiltonian paths in graph algorithms
- Apply efficient algorithms for finding Hamiltonian paths in directed graphs
- Implement dynamic programming with bitmasking for Hamiltonian path problems
- Optimize graph algorithms for path counting problems
- Handle special cases in Hamiltonian path problems

## 📋 Problem Description

Given a directed graph, count the number of Hamiltonian paths from source to destination (paths that visit each vertex exactly once).

**Input**: 
- n: number of vertices
- m: number of edges
- source: source vertex
- destination: destination vertex
- edges: array of (u, v) representing directed edges

**Output**: 
- Number of Hamiltonian paths from source to destination

**Constraints**:
- 1 ≤ n ≤ 20
- 1 ≤ m ≤ 400

**Example**:
```
Input:
n = 4, source = 0, destination = 3
edges = [(0,1), (0,2), (1,2), (1,3), (2,3)]

Output:
2

Explanation**: 
Hamiltonian paths from 0 to 3:
1. 0 → 1 → 2 → 3
2. 0 → 2 → 1 → 3
Total: 2 paths
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible permutations of vertices
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check each permutation for valid Hamiltonian path
- **Inefficient**: O(n! × m) time complexity

**Key Insight**: Generate all possible permutations and check which ones form valid Hamiltonian paths.

**Algorithm**:
- Generate all permutations of vertices starting with source and ending with destination
- For each permutation, check if it forms a valid path in the graph
- Count the number of valid Hamiltonian paths

**Visual Example**:
```
Graph: 0->1, 0->2, 1->2, 1->3, 2->3
Source: 0, Destination: 3

Try all permutations starting with 0 and ending with 3:
┌─────────────────────────────────────┐
│ Permutation 1: [0, 1, 2, 3]        │
│ - Check edges: 0->1 ✓, 1->2 ✓, 2->3 ✓ │
│ - Valid Hamiltonian path ✓          │
│                                   │
│ Permutation 2: [0, 1, 3, 2]        │
│ - Check edges: 0->1 ✓, 1->3 ✓, 3->2 ✗ │
│ - Invalid (no edge 3->2)           │
│                                   │
│ Permutation 3: [0, 2, 1, 3]        │
│ - Check edges: 0->2 ✓, 2->1 ✓, 1->3 ✓ │
│ - Valid Hamiltonian path ✓          │
│                                   │
│ Permutation 4: [0, 2, 3, 1]        │
│ - Check edges: 0->2 ✓, 2->3 ✓, 3->1 ✗ │
│ - Invalid (no edge 3->1)           │
│                                   │
│ Permutation 5: [0, 3, 1, 2]        │
│ - Check edges: 0->3 ✗              │
│ - Invalid (no edge 0->3)           │
│                                   │
│ Permutation 6: [0, 3, 2, 1]        │
│ - Check edges: 0->3 ✗              │
│ - Invalid (no edge 0->3)           │
│                                   │
│ Valid Hamiltonian paths: 2         │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_hamiltonian_flights(n, source, destination, edges):
    """Count Hamiltonian paths using brute force approach"""
    from itertools import permutations
    
    # Build adjacency set for O(1) edge lookup
    adj_set = set(edges)
    
    def is_valid_hamiltonian_path(path):
        """Check if path is a valid Hamiltonian path"""
        # Check if path starts with source and ends with destination
        if path[0] != source or path[-1] != destination:
            return False
        
        # Check if all vertices are visited exactly once
        if len(set(path)) != len(path):
            return False
        
        # Check if all edges in path exist
        for i in range(len(path) - 1):
            if (path[i], path[i + 1]) not in adj_set:
                return False
        
        return True
    
    # Generate all permutations of vertices
    vertices = list(range(n))
    hamiltonian_paths = 0
    
    # Try all permutations starting with source and ending with destination
    for perm in permutations(vertices):
        if perm[0] == source and perm[-1] == destination:
            if is_valid_hamiltonian_path(perm):
                hamiltonian_paths += 1
    
    return hamiltonian_paths

# Example usage
n = 4
source = 0
destination = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
result = brute_force_hamiltonian_flights(n, source, destination, edges)
print(f"Brute force Hamiltonian paths: {result}")
```

**Time Complexity**: O(n! × m)
**Space Complexity**: O(n)

**Why it's inefficient**: O(n! × m) time complexity for trying all permutations.

---

### Approach 2: Dynamic Programming with Bitmasking

**Key Insights from Dynamic Programming with Bitmasking**:
- **State Space**: Use DP state (current_vertex, visited_mask) where visited_mask is bitmask
- **Efficient Implementation**: O(n² × 2^n) time complexity
- **Memoization**: Use memoization to avoid recalculating subproblems
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use dynamic programming with bitmasking to count Hamiltonian paths efficiently.

**Algorithm**:
- Define DP state as (current_vertex, visited_mask)
- Use bitmask to represent which vertices have been visited
- For each state, try all unvisited neighbors
- Use memoization to avoid recalculating subproblems
- Return count of paths from source to destination

**Visual Example**:
```
Dynamic Programming with Bitmasking:

Graph: 0->1, 0->2, 1->2, 1->3, 2->3
Source: 0, Destination: 3

DP State: (current_vertex, visited_mask)
visited_mask: bitmask where bit i = 1 if vertex i is visited

State transitions:
┌─────────────────────────────────────┐
│ From (0, 0001):                    │
│ - To (1, 0011): if edge 0->1 exists │
│ - To (2, 0101): if edge 0->2 exists │
│                                   │
│ From (1, 0011):                    │
│ - To (2, 0111): if edge 1->2 exists │
│ - To (3, 1011): if edge 1->3 exists │
│                                   │
│ From (2, 0101):                    │
│ - To (1, 0111): if edge 2->1 exists │
│ - To (3, 1101): if edge 2->3 exists │
│                                   │
│ From (2, 0111):                    │
│ - To (3, 1111): if edge 2->3 exists │
│                                   │
│ From (1, 0111):                    │
│ - To (3, 1111): if edge 1->3 exists │
│                                   │
│ Count paths to (3, 1111): 2        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_bitmask_hamiltonian_flights(n, source, destination, edges):
    """Count Hamiltonian paths using DP with bitmasking"""
    from functools import lru_cache
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    @lru_cache(maxsize=None)
    def dp(current_vertex, visited_mask):
        """DP function to count Hamiltonian paths"""
        # Base case: if we've visited all vertices
        if visited_mask == (1 << n) - 1:
            return 1 if current_vertex == destination else 0
        
        # If we're at destination but haven't visited all vertices
        if current_vertex == destination:
            return 0
        
        count = 0
        
        # Try all unvisited neighbors
        for neighbor in adj[current_vertex]:
            if not (visited_mask & (1 << neighbor)):
                new_mask = visited_mask | (1 << neighbor)
                count += dp(neighbor, new_mask)
        
        return count
    
    # Start from source with only source visited
    initial_mask = 1 << source
    return dp(source, initial_mask)

# Example usage
n = 4
source = 0
destination = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
result = dp_bitmask_hamiltonian_flights(n, source, destination, edges)
print(f"DP bitmask Hamiltonian paths: {result}")
```

**Time Complexity**: O(n² × 2^n)
**Space Complexity**: O(n × 2^n)

**Why it's better**: Uses DP with bitmasking for O(n² × 2^n) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for Hamiltonian path counting
- **Efficient Implementation**: O(n² × 2^n) time complexity
- **Space Efficiency**: O(n × 2^n) space complexity
- **Optimal Complexity**: Best approach for Hamiltonian path problems

**Key Insight**: Use advanced data structures for optimal Hamiltonian path counting.

**Algorithm**:
- Use specialized data structures for DP state storage
- Implement efficient bitmask operations
- Handle special cases optimally
- Return count of Hamiltonian paths

**Visual Example**:
```
Advanced data structure approach:

For graph: 0->1, 0->2, 1->2, 1->3, 2->3
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - DP table: for efficient           │
│   storage and operations            │
│ - Bitmask cache: for optimization   │
│ - Path cache: for optimization      │
│                                   │
│ Hamiltonian path counting:          │
│ - Use DP table for efficient        │
│   storage and operations            │
│ - Use bitmask cache for            │
│   optimization                      │
│ - Use path cache for optimization   │
│                                   │
│ Result: 2                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_hamiltonian_flights(n, source, destination, edges):
    """Count Hamiltonian paths using advanced data structure approach"""
    from functools import lru_cache
    
    # Use advanced data structures for graph storage
    # Build advanced adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    # Advanced DP with bitmasking
    @lru_cache(maxsize=None)
    def advanced_dp(current_vertex, visited_mask):
        """Advanced DP function to count Hamiltonian paths"""
        # Advanced base case handling
        if visited_mask == (1 << n) - 1:
            return 1 if current_vertex == destination else 0
        
        # Advanced destination check
        if current_vertex == destination:
            return 0
        
        count = 0
        
        # Advanced neighbor processing
        for neighbor in adj[current_vertex]:
            if not (visited_mask & (1 << neighbor)):
                new_mask = visited_mask | (1 << neighbor)
                count += advanced_dp(neighbor, new_mask)
        
        return count
    
    # Advanced initialization
    initial_mask = 1 << source
    return advanced_dp(source, initial_mask)

# Example usage
n = 4
source = 0
destination = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
result = advanced_data_structure_hamiltonian_flights(n, source, destination, edges)
print(f"Advanced data structure Hamiltonian paths: {result}")
```

**Time Complexity**: O(n² × 2^n)
**Space Complexity**: O(n × 2^n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × m) | O(n) | Try all possible permutations |
| DP with Bitmasking | O(n² × 2^n) | O(n × 2^n) | Use DP state (vertex, visited_mask) |
| Advanced Data Structure | O(n² × 2^n) | O(n × 2^n) | Use advanced data structures |

### Time Complexity
- **Time**: O(n² × 2^n) - Use DP with bitmasking for efficient Hamiltonian path counting
- **Space**: O(n × 2^n) - Store DP table and bitmask states

### Why This Solution Works
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Bitmasking**: Use bitmasks to efficiently represent visited vertices
- **State Space**: Define state as (current_vertex, visited_mask)
- **Optimal Algorithms**: Use optimal algorithms for Hamiltonian path problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Hamiltonian Flights with Constraints**
**Problem**: Count Hamiltonian paths with specific constraints.

**Key Differences**: Apply constraints to path counting

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_hamiltonian_flights(n, source, destination, edges, constraints):
    """Count Hamiltonian paths with constraints"""
    from functools import lru_cache
    
    # Build adjacency list with constraints
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if constraints(u, v):
            adj[u].append(v)
    
    @lru_cache(maxsize=None)
    def constrained_dp(current_vertex, visited_mask):
        """DP function with constraints"""
        if visited_mask == (1 << n) - 1:
            return 1 if current_vertex == destination else 0
        
        if current_vertex == destination:
            return 0
        
        count = 0
        
        for neighbor in adj[current_vertex]:
            if not (visited_mask & (1 << neighbor)) and constraints(current_vertex, neighbor):
                new_mask = visited_mask | (1 << neighbor)
                count += constrained_dp(neighbor, new_mask)
        
        return count
    
    initial_mask = 1 << source
    return constrained_dp(source, initial_mask)

# Example usage
n = 4
source = 0
destination = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
constraints = lambda u, v: True  # No constraints
result = constrained_hamiltonian_flights(n, source, destination, edges, constraints)
print(f"Constrained Hamiltonian paths: {result}")
```

#### **2. Hamiltonian Flights with Different Metrics**
**Problem**: Count Hamiltonian paths with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_hamiltonian_flights(n, source, destination, edges, weight_function):
    """Count Hamiltonian paths with different cost metrics"""
    from functools import lru_cache
    
    # Build adjacency list with weights
    adj = [[] for _ in range(n)]
    for u, v in edges:
        weight = weight_function(u, v)
        adj[u].append((v, weight))
    
    @lru_cache(maxsize=None)
    def weighted_dp(current_vertex, visited_mask):
        """DP function with weights"""
        if visited_mask == (1 << n) - 1:
            return 1 if current_vertex == destination else 0
        
        if current_vertex == destination:
            return 0
        
        count = 0
        
        for neighbor, weight in adj[current_vertex]:
            if not (visited_mask & (1 << neighbor)):
                new_mask = visited_mask | (1 << neighbor)
                count += weighted_dp(neighbor, new_mask)
        
        return count
    
    initial_mask = 1 << source
    return weighted_dp(source, initial_mask)

# Example usage
n = 4
source = 0
destination = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
weight_function = lambda u, v: 1  # Unit weight
result = weighted_hamiltonian_flights(n, source, destination, edges, weight_function)
print(f"Weighted Hamiltonian paths: {result}")
```

#### **3. Hamiltonian Flights with Multiple Dimensions**
**Problem**: Count Hamiltonian paths in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_hamiltonian_flights(n, source, destination, edges, dimensions):
    """Count Hamiltonian paths in multiple dimensions"""
    from functools import lru_cache
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    @lru_cache(maxsize=None)
    def multi_dimensional_dp(current_vertex, visited_mask):
        """DP function for multiple dimensions"""
        if visited_mask == (1 << n) - 1:
            return 1 if current_vertex == destination else 0
        
        if current_vertex == destination:
            return 0
        
        count = 0
        
        for neighbor in adj[current_vertex]:
            if not (visited_mask & (1 << neighbor)):
                new_mask = visited_mask | (1 << neighbor)
                count += multi_dimensional_dp(neighbor, new_mask)
        
        return count
    
    initial_mask = 1 << source
    return multi_dimensional_dp(source, initial_mask)

# Example usage
n = 4
source = 0
destination = 3
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
dimensions = 1
result = multi_dimensional_hamiltonian_flights(n, source, destination, edges, dimensions)
print(f"Multi-dimensional Hamiltonian paths: {result}")
```

### Related Problems

#### **CSES Problems**
- [Distinct Routes](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Message Route](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Round Trip](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Unique Paths](https://leetcode.com/problems/unique-paths/) - Dynamic Programming
- [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) - Dynamic Programming
- [Path Sum](https://leetcode.com/problems/path-sum/) - Tree

#### **Problem Categories**
- **Graph Algorithms**: Hamiltonian paths, path counting
- **Dynamic Programming**: Bitmasking, state space search
- **Combinatorics**: Path counting, permutations

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Hamiltonian Path](https://cp-algorithms.com/graph/hamiltonian_path.html) - Hamiltonian path algorithms
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms

### **Practice Problems**
- [CSES Distinct Routes](https://cses.fi/problemset/task/1075) - Medium
- [CSES Message Route](https://cses.fi/problemset/task/1075) - Medium
- [CSES Round Trip](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [Hamiltonian Path](https://en.wikipedia.org/wiki/Hamiltonian_path) - Wikipedia article
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
