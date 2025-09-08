---
layout: simple
title: "Cycle Finding - Negative Cycle Detection"
permalink: /problem_soulutions/graph_algorithms/cycle_finding_analysis
---

# Cycle Finding - Negative Cycle Detection

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand negative cycle detection problems and Bellman-Ford algorithm concepts
- Apply Bellman-Ford algorithm to detect negative cycles in weighted graphs
- Implement efficient negative cycle detection algorithms with proper cycle reconstruction
- Optimize negative cycle detection using graph representations and algorithm optimizations
- Handle edge cases in negative cycle detection (no cycles, positive cycles, disconnected graphs)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Bellman-Ford algorithm, negative cycle detection, cycle reconstruction, weighted graph algorithms
- **Data Structures**: Distance arrays, parent arrays, graph representations, cycle tracking
- **Mathematical Concepts**: Graph theory, negative cycles, shortest path properties, cycle detection
- **Programming Skills**: Graph traversal, distance calculations, cycle reconstruction, algorithm implementation
- **Related Problems**: High Score (negative weights), Shortest Routes I (shortest paths), Graph algorithms

## Problem Description

**Problem**: Given a directed graph with n nodes and m edges, find a negative cycle if it exists. If there is no negative cycle, print "NO". Otherwise, print "YES" and the nodes in the cycle.

This is a classic negative cycle detection problem using the Bellman-Ford algorithm. We need to detect if there exists a cycle where the sum of edge weights is negative.

**Input**: 
- First line: Two integers n and m (number of nodes and edges)
- Next m lines: Three integers a, b, and c (edge from node a to node b with weight c)

**Output**: 
- Print "NO" if no negative cycle exists
- Print "YES" followed by cycle nodes if negative cycle exists

**Constraints**:
- 1 ≤ n ≤ 2500
- 1 ≤ m ≤ 5000
- 1 ≤ a, b ≤ n
- -10⁹ ≤ c ≤ 10⁹
- Graph is directed
- Nodes are numbered from 1 to n
- No self-loops or multiple edges between same pair of nodes

**Example**:
```
Input:
4 5
1 2 1
2 3 2
3 4 1
4 2 -5
2 1 1

Output:
YES
2 3 4 2
```

**Explanation**: 
- The cycle 2 → 3 → 4 → 2 has total weight: 2 + 1 + (-5) = -2
- This is a negative cycle, so we output "YES" and the cycle

## Visual Example

### Input Graph
```
Nodes: 1, 2, 3, 4
Edges: (1→2,1), (2→3,2), (3→4,1), (4→2,-5), (2→1,1)

Graph representation:
1 ──1──> 2 ──2──> 3 ──1──> 4
│        │              │
└──1─────┼──(-5)────────┘
          │
          └──────────────┘
```

### Negative Cycle Detection Process
```
Step 1: Initialize distances
- dist[1] = dist[2] = dist[3] = dist[4] = 0

Step 2: Bellman-Ford algorithm
- Iteration 1:
  - dist[2] = min(dist[2], dist[1] + 1) = min(0, 0 + 1) = 1
  - dist[3] = min(dist[3], dist[2] + 2) = min(0, 1 + 2) = 3
  - dist[4] = min(dist[4], dist[3] + 1) = min(0, 3 + 1) = 4
  - dist[2] = min(dist[2], dist[4] + (-5)) = min(1, 4 + (-5)) = -1
  - dist[1] = min(dist[1], dist[2] + 1) = min(0, -1 + 1) = 0

- Iteration 2:
  - dist[2] = min(dist[2], dist[1] + 1) = min(-1, 0 + 1) = -1
  - dist[3] = min(dist[3], dist[2] + 2) = min(3, -1 + 2) = 1
  - dist[4] = min(dist[4], dist[3] + 1) = min(4, 1 + 1) = 2
  - dist[2] = min(dist[2], dist[4] + (-5)) = min(-1, 2 + (-5)) = -3
  - dist[1] = min(dist[1], dist[2] + 1) = min(0, -3 + 1) = -2

- Iteration 3:
  - dist[2] = min(dist[2], dist[1] + 1) = min(-3, -2 + 1) = -3
  - dist[3] = min(dist[3], dist[2] + 2) = min(1, -3 + 2) = -1
  - dist[4] = min(dist[4], dist[3] + 1) = min(2, -1 + 1) = 0
  - dist[2] = min(dist[2], dist[4] + (-5)) = min(-3, 0 + (-5)) = -5
  - dist[1] = min(dist[1], dist[2] + 1) = min(-2, -5 + 1) = -4

Step 3: Check for negative cycle
- Iteration 4: distances still decreasing
- Negative cycle detected: 2 → 3 → 4 → 2
```

### Cycle Analysis
```
Negative cycle found: 2 → 3 → 4 → 2

Weight calculation:
- Edge 2→3: 2
- Edge 3→4: 1
- Edge 4→2: -5
- Total weight: 2 + 1 + (-5) = -2

Negative cycle detected ✓
```

### Key Insight
Bellman-Ford algorithm works by:
1. Relaxing all edges for n-1 iterations
2. Checking if distances can still be improved in n-th iteration
3. If yes, negative cycle exists
4. Time complexity: O(n × m) for n iterations
5. Space complexity: O(n) for distance array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Cycle Detection (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths to detect cycles
- Check if any cycle has negative total weight
- Simple but computationally expensive approach
- Not suitable for large graphs

**Algorithm:**
1. Generate all possible cycles in the graph
2. Calculate the total weight for each cycle
3. Check if any cycle has negative total weight
4. Return the first negative cycle found

**Visual Example:**
```
Brute force: Try all possible cycles
For graph: 1 ──1──> 2 ──2──> 3 ──1──> 4
           │        │              │
           └──1─────┼──(-5)────────┘
                     │
                     └──────────────┘

All possible cycles:
- Cycle 1: 1 → 2 → 1 (weight: 1 + 1 = 2)
- Cycle 2: 2 → 3 → 4 → 2 (weight: 2 + 1 + (-5) = -2)
- Cycle 3: 1 → 2 → 3 → 4 → 2 → 1 (weight: 1 + 2 + 1 + (-5) + 1 = 0)

Negative cycle found: 2 → 3 → 4 → 2
```

**Implementation:**
```python
def cycle_finding_brute_force(n, m, edges):
    from itertools import combinations, permutations
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Try all possible cycles
    for length in range(2, n + 1):
        for nodes in combinations(range(1, n + 1), length):
            for perm in permutations(nodes):
                # Check if this permutation forms a cycle
                total_weight = 0
                valid_cycle = True
                
                for i in range(len(perm)):
                    current = perm[i]
                    next_node = perm[(i + 1) % len(perm)]
                    
                    # Check if edge exists
                    edge_found = False
                    for neighbor, weight in adj[current]:
                        if neighbor == next_node:
                            total_weight += weight
                            edge_found = True
                            break
                    
                    if not edge_found:
                        valid_cycle = False
                        break
                
                if valid_cycle and total_weight < 0:
                    return True, list(perm)
    
    return False, None
```

**Time Complexity:** O(n! × n) for checking all possible cycles
**Space Complexity:** O(n!) for storing all permutations

**Why it's inefficient:**
- Exponential time complexity O(n!)
- Not suitable for large graphs
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: Bellman-Ford Algorithm (Better)

**Key Insights from Bellman-Ford Solution:**
- Use Bellman-Ford algorithm to detect negative cycles
- Much more efficient than brute force approach
- Standard method for negative cycle detection
- Can detect cycles but needs additional work for reconstruction

**Algorithm:**
1. Initialize distances with infinity except source (0)
2. Relax all edges for n-1 iterations
3. Check if distances can still be improved in n-th iteration
4. If yes, negative cycle exists

**Visual Example:**
```
Bellman-Ford algorithm for graph: 1 ──1──> 2 ──2──> 3 ──1──> 4
                                    │        │              │
                                    └──1─────┼──(-5)────────┘
                                              │
                                              └──────────────┘

Step 1: Initialize distances
- dist[1] = 0, dist[2] = dist[3] = dist[4] = ∞

Step 2: Relax edges for n-1 iterations

Iteration 1:
- dist[2] = min(dist[2], dist[1] + 1) = min(∞, 0 + 1) = 1
- dist[3] = min(dist[3], dist[2] + 2) = min(∞, 1 + 2) = 3
- dist[4] = min(dist[4], dist[3] + 1) = min(∞, 3 + 1) = 4
- dist[2] = min(dist[2], dist[4] + (-5)) = min(1, 4 + (-5)) = -1
- dist[1] = min(dist[1], dist[2] + 1) = min(0, -1 + 1) = 0

Iteration 2:
- dist[2] = min(dist[2], dist[1] + 1) = min(-1, 0 + 1) = -1
- dist[3] = min(dist[3], dist[2] + 2) = min(3, -1 + 2) = 1
- dist[4] = min(dist[4], dist[3] + 1) = min(4, 1 + 1) = 2
- dist[2] = min(dist[2], dist[4] + (-5)) = min(-1, 2 + (-5)) = -3
- dist[1] = min(dist[1], dist[2] + 1) = min(0, -3 + 1) = -2

Iteration 3:
- dist[2] = min(dist[2], dist[1] + 1) = min(-3, -2 + 1) = -3
- dist[3] = min(dist[3], dist[2] + 2) = min(1, -3 + 2) = -1
- dist[4] = min(dist[4], dist[3] + 1) = min(2, -1 + 1) = 0
- dist[2] = min(dist[2], dist[4] + (-5)) = min(-3, 0 + (-5)) = -5
- dist[1] = min(dist[1], dist[2] + 1) = min(-2, -5 + 1) = -4

Step 3: Check for negative cycle
- Iteration 4: distances still decreasing
- Negative cycle detected: 2 → 3 → 4 → 2
```

**Implementation:**
```python
def cycle_finding_bellman_ford(n, m, edges):
    # Initialize distances and parent array
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    dist[1] = 0
    
    # Run Bellman-Ford for n-1 iterations
    for i in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    
    # Check for negative cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            # Negative cycle found
            return True, u, v, parent
    
    return False, None, None, None
```

**Time Complexity:** O(n × m) for n iterations
**Space Complexity:** O(n) for distance and parent arrays

**Why it's better:**
- Polynomial time complexity O(n × m)
- Standard method for negative cycle detection
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Bellman-Ford with Cycle Reconstruction (Optimal)

**Key Insights from Bellman-Ford with Cycle Reconstruction Solution:**
- Use Bellman-Ford algorithm with improved cycle reconstruction
- Most efficient approach for negative cycle detection
- Standard method in competitive programming
- Can reconstruct the actual cycle path

**Algorithm:**
1. Initialize distances with infinity except source (0)
2. Relax all edges for n-1 iterations
3. Check if distances can still be improved in n-th iteration
4. If yes, reconstruct the negative cycle path

**Visual Example:**
```
Bellman-Ford with cycle reconstruction for graph: 1 ──1──> 2 ──2──> 3 ──1──> 4
                                                      │        │              │
                                                      └──1─────┼──(-5)────────┘
                                                                │
                                                                └──────────────┘

Step 1: Initialize distances and parent array
- dist[1] = 0, dist[2] = dist[3] = dist[4] = ∞
- parent[1] = parent[2] = parent[3] = parent[4] = -1

Step 2: Relax edges for n-1 iterations

Iteration 1:
- dist[2] = min(dist[2], dist[1] + 1) = min(∞, 0 + 1) = 1, parent[2] = 1
- dist[3] = min(dist[3], dist[2] + 2) = min(∞, 1 + 2) = 3, parent[3] = 2
- dist[4] = min(dist[4], dist[3] + 1) = min(∞, 3 + 1) = 4, parent[4] = 3
- dist[2] = min(dist[2], dist[4] + (-5)) = min(1, 4 + (-5)) = -1, parent[2] = 4
- dist[1] = min(dist[1], dist[2] + 1) = min(0, -1 + 1) = 0, parent[1] = 2

Iteration 2:
- dist[2] = min(dist[2], dist[1] + 1) = min(-1, 0 + 1) = -1, parent[2] = 1
- dist[3] = min(dist[3], dist[2] + 2) = min(3, -1 + 2) = 1, parent[3] = 2
- dist[4] = min(dist[4], dist[3] + 1) = min(4, 1 + 1) = 2, parent[4] = 3
- dist[2] = min(dist[2], dist[4] + (-5)) = min(-1, 2 + (-5)) = -3, parent[2] = 4
- dist[1] = min(dist[1], dist[2] + 1) = min(0, -3 + 1) = -2, parent[1] = 2

Iteration 3:
- dist[2] = min(dist[2], dist[1] + 1) = min(-3, -2 + 1) = -3, parent[2] = 1
- dist[3] = min(dist[3], dist[2] + 2) = min(1, -3 + 2) = -1, parent[3] = 2
- dist[4] = min(dist[4], dist[3] + 1) = min(2, -1 + 1) = 0, parent[4] = 3
- dist[2] = min(dist[2], dist[4] + (-5)) = min(-3, 0 + (-5)) = -5, parent[2] = 4
- dist[1] = min(dist[1], dist[2] + 1) = min(-2, -5 + 1) = -4, parent[1] = 2

Step 3: Check for negative cycle and reconstruct
- Iteration 4: distances still decreasing
- Negative cycle detected: 2 → 3 → 4 → 2
- Cycle reconstruction: 2 → 3 → 4 → 2
```

**Implementation:**
```python
def cycle_finding_optimized(n, m, edges):
    # Initialize distances and parent array
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    dist[1] = 0
    
    # Run Bellman-Ford for n-1 iterations
    for i in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    
    # Check for negative cycle and find the cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            # Negative cycle found, reconstruct the cycle
            cycle = []
            visited = [False] * (n + 1)
            
            # Start from the node that can be relaxed
            current = v
            while not visited[current]:
                visited[current] = True
                cycle.append(current)
                current = parent[current]
            
            # Find the start of the cycle
            cycle_start = current
            cycle_nodes = []
            current = v
            while current != cycle_start:
                cycle_nodes.append(current)
                current = parent[current]
            cycle_nodes.append(cycle_start)
            cycle_nodes.reverse()
            
            return True, cycle_nodes
    
    return False, None

def solve_cycle_finding():
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b, c = map(int, input().split())
    edges.append((a, b, c))

    has_cycle, cycle = cycle_finding_optimized(n, m, edges)
    
    if has_cycle:
        print("YES")
        print(*cycle)
    else:
        print("NO")

# Main execution
if __name__ == "__main__":
    solve_cycle_finding()
```

**Time Complexity:** O(n × m) for n iterations with cycle reconstruction
**Space Complexity:** O(n) for distance and parent arrays

**Why it's optimal:**
- O(n × m) time complexity is optimal for Bellman-Ford
- Can reconstruct the actual cycle path
- Most efficient approach for competitive programming
- Standard method for negative cycle detection

## 🎯 Problem Variations

### Variation 1: Negative Cycle Detection with Different Constraints
**Problem**: Detect negative cycles with different weight constraints and penalties.

**Link**: [CSES Problem Set - Negative Cycle Detection with Constraints](https://cses.fi/problemset/task/negative_cycle_constraints)

```python
def cycle_finding_constraints(n, m, edges, constraints):
    # Initialize distances and parent array
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    dist[1] = 0
    
    # Run Bellman-Ford for n-1 iterations
    for i in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                # Apply constraints
                if w >= constraints.get('min_weight', float('-inf')):
                dist[v] = dist[u] + w
                parent[v] = u
    
    # Check for negative cycle and find the cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            # Negative cycle found, reconstruct the cycle
            cycle = []
            visited = [False] * (n + 1)
            
            # Start from the node that can be relaxed
            current = v
            while not visited[current]:
                visited[current] = True
                cycle.append(current)
                current = parent[current]
            
            # Find the start of the cycle
            cycle_start = current
            cycle_nodes = []
            current = v
            while current != cycle_start:
                cycle_nodes.append(current)
                current = parent[current]
            cycle_nodes.append(cycle_start)
            cycle_nodes.reverse()
            
            return True, cycle_nodes
    
    return False, None
```

### Variation 2: Negative Cycle Detection with Multiple Sources
**Problem**: Detect negative cycles with multiple possible sources.

**Link**: [CSES Problem Set - Negative Cycle Detection Multiple Sources](https://cses.fi/problemset/task/negative_cycle_multiple_sources)

```python
def cycle_finding_multiple_sources(n, m, edges, sources):
    # Initialize distances and parent array
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    
    # Initialize all sources
    for source in sources:
        dist[source] = 0
    
    # Run Bellman-Ford for n-1 iterations
    for i in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    
    # Check for negative cycle and find the cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            # Negative cycle found, reconstruct the cycle
            cycle = []
            visited = [False] * (n + 1)
            
            # Start from the node that can be relaxed
            current = v
            while not visited[current]:
                visited[current] = True
                cycle.append(current)
        current = parent[current]
            
            # Find the start of the cycle
            cycle_start = current
            cycle_nodes = []
            current = v
            while current != cycle_start:
                cycle_nodes.append(current)
                current = parent[current]
            cycle_nodes.append(cycle_start)
            cycle_nodes.reverse()
            
            return True, cycle_nodes
    
    return False, None
```

### Variation 3: Negative Cycle Detection with Path Length Constraints
**Problem**: Detect negative cycles with maximum path length constraints.

**Link**: [CSES Problem Set - Negative Cycle Detection Length Constraints](https://cses.fi/problemset/task/negative_cycle_length_constraints)

```python
def cycle_finding_length_constraints(n, m, edges, max_length):
    # Initialize distances and parent array
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    dist[1] = 0
    
    # Run Bellman-Ford for min(n-1, max_length) iterations
    for i in range(min(n - 1, max_length)):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    
    # Check for negative cycle and find the cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            # Negative cycle found, reconstruct the cycle
    cycle = []
            visited = [False] * (n + 1)
            
            # Start from the node that can be relaxed
                        current = v
            while not visited[current]:
                visited[current] = True
                            cycle.append(current)
                            current = parent[current]
                        
            # Find the start of the cycle
                        cycle_start = current
                        cycle_nodes = []
                        current = v
                        while current != cycle_start:
                            cycle_nodes.append(current)
                            current = parent[current]
                        cycle_nodes.append(cycle_start)
            cycle_nodes.reverse()
            
            return True, cycle_nodes
    
    return False, None
```

## 🔗 Related Problems

- **[High Score](/cses-analyses/problem_soulutions/graph_algorithms/high_score_analysis/)**: Negative weight handling
- **[Shortest Routes I](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_i_analysis/)**: Shortest path problems
- **[Shortest Routes II](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_ii_analysis/)**: All-pairs shortest paths
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Negative Cycle Detection**: Essential for analyzing graphs with negative weights
2. **Bellman-Ford Algorithm**: Key algorithm for negative cycle detection
3. **Cycle Reconstruction**: Important for finding the actual cycle path
4. **Graph Theory**: Foundation for many optimization problems
5. **Algorithm Optimization**: Critical for competitive programming performance
6. **Data Structures**: Foundation for many graph algorithms

## 📝 Summary

The Cycle Finding problem demonstrates fundamental negative cycle detection concepts for analyzing graphs with negative weights. We explored three approaches:

1. **Brute Force Cycle Detection**: O(n! × n) time complexity using exhaustive search, inefficient for large graphs
2. **Bellman-Ford Algorithm**: O(n × m) time complexity using edge relaxation, better approach for negative cycle detection
3. **Bellman-Ford with Cycle Reconstruction**: O(n × m) time complexity with cycle reconstruction, optimal approach for negative cycle detection

The key insights include understanding negative cycles as optimization problems, using Bellman-Ford for efficient detection, and applying cycle reconstruction for finding actual cycle paths. This problem serves as an excellent introduction to negative cycle detection algorithms and graph theory optimization techniques.

