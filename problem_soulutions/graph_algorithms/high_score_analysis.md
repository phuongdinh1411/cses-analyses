---
layout: simple
title: "High Score - Longest Path with Negative Weights"
permalink: /problem_soulutions/graph_algorithms/high_score_analysis
---

# High Score - Longest Path with Negative Weights

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand longest path problems and negative weight handling in graphs
- Apply Bellman-Ford algorithm or modified Dijkstra's to handle negative weights
- Implement efficient longest path algorithms with negative cycle detection
- Optimize longest path solutions using graph representations and cycle detection
- Handle edge cases in longest path problems (negative cycles, unreachable destinations, infinite scores)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Bellman-Ford algorithm, negative weight handling, longest path problems, cycle detection
- **Data Structures**: Distance arrays, graph representations, cycle tracking, path data structures
- **Mathematical Concepts**: Graph theory, negative weights, longest path properties, cycle detection
- **Programming Skills**: Graph traversal, distance calculations, cycle detection, algorithm implementation
- **Related Problems**: Shortest Routes I (shortest paths), Download Speed (flow problems), Graph algorithms

## Problem Description

**Problem**: There are n cities and m flight connections. Your task is to find the highest possible score for a route from city 1 to city n.

This is a longest path problem in a directed graph with potentially negative weights. We need to find the maximum score path from source to destination, handling negative cycles that could lead to infinite scores.

**Input**: 
- First line: Two integers n and m (number of cities and flight connections)
- Next m lines: Three integers a, b, and c (flight from city a to city b with score c)

**Output**: 
- Highest possible score for a route from city 1 to city n, or -1 if no route exists

**Constraints**:
- 1 ≤ n ≤ 2500
- 1 ≤ m ≤ 5000
- 1 ≤ a, b ≤ n
- -10⁹ ≤ c ≤ 10⁹
- Graph is directed
- Cities are numbered from 1 to n
- No self-loops or multiple edges between same pair of cities

**Example**:
```
Input:
4 5
1 2 3
2 4 -1
1 3 -2
3 4 7
1 4 2

Output:
5
```

**Explanation**: 
- Path 1 → 2 → 4: score = 3 + (-1) = 2
- Path 1 → 3 → 4: score = (-2) + 7 = 5
- Path 1 → 4: score = 2
- Highest score: 5 (path 1 → 3 → 4)

## Visual Example

### Input Graph
```
Cities: 1, 2, 3, 4
Flights: (1→2,3), (2→4,-1), (1→3,-2), (3→4,7), (1→4,2)

Graph representation:
1 ──3──> 2 ──(-1)──> 4
│        │            │
└──(-2)──┼──7─────────┘
          │
          └──2─────┘
```

### Longest Path Algorithm Process
```
Step 1: Initialize distances
- dist[1] = 0 (source)
- dist[2] = dist[3] = dist[4] = -∞

Step 2: Bellman-Ford algorithm
- Iteration 1:
  - dist[2] = max(dist[2], dist[1] + 3) = max(-∞, 0 + 3) = 3
  - dist[3] = max(dist[3], dist[1] + (-2)) = max(-∞, 0 + (-2)) = -2
  - dist[4] = max(dist[4], dist[1] + 2) = max(-∞, 0 + 2) = 2

- Iteration 2:
  - dist[4] = max(dist[4], dist[2] + (-1)) = max(2, 3 + (-1)) = 2
  - dist[4] = max(dist[4], dist[3] + 7) = max(2, -2 + 7) = 5

- Iteration 3:
  - No more updates

Step 3: Check for negative cycles
- No negative cycles detected
- Final distance to city 4: 5
```

### Path Analysis
```
Optimal path: 1 → 3 → 4
Score breakdown:
- Flight 1→3: -2
- Flight 3→4: 7
- Total score: -2 + 7 = 5

Alternative paths:
- 1 → 2 → 4: 3 + (-1) = 2
- 1 → 4: 2
```

### Key Insight
Bellman-Ford algorithm works by:
1. Relaxing all edges for n-1 iterations
2. Finding longest paths by maximizing distances
3. Detecting negative cycles in final iteration
4. Time complexity: O(n × m) for n iterations
5. Space complexity: O(n) for distance array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths from source to destination
- Calculate score for each path and find maximum
- Simple but computationally expensive approach
- Not suitable for large graphs

**Algorithm:**
1. Generate all possible paths from source to destination
2. Calculate the total score for each path
3. Find the maximum score among all paths
4. Return the maximum score

**Visual Example:**
```
Brute force: Try all possible paths
For graph: 1 ──3──> 2 ──(-1)──> 4
           │        │            │
           └──(-2)──┼──7─────────┘
                     │
                     └──2─────┘

All possible paths:
- Path 1: 1 → 4 (score: 2)
- Path 2: 1 → 2 → 4 (score: 3 + (-1) = 2)
- Path 3: 1 → 3 → 4 (score: (-2) + 7 = 5)

Maximum score: 5
```

**Implementation:**
```python
def high_score_brute_force(n, m, flights):
    from itertools import combinations
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        adj[a].append((b, c))
    
    # Find all paths from source to destination
    all_paths = []
    
    def find_paths(current, target, path, score, visited):
        if current == target:
            all_paths.append((path[:], score))
            return
        
        for next_node, weight in adj[current]:
            if next_node not in visited:
                visited.add(next_node)
                path.append(next_node)
                find_paths(next_node, target, path, score + weight, visited)
                path.pop()
                visited.remove(next_node)
    
    # Find all paths from 1 to n
    find_paths(1, n, [1], 0, {1})
    
    if not all_paths:
        return -1  # No path exists
    
    max_score = max(score for path, score in all_paths)
    return max_score
```

**Time Complexity:** O(2^n × n) for checking all possible paths
**Space Complexity:** O(2^n × n) for storing all paths

**Why it's inefficient:**
- Exponential time complexity O(2^n)
- Not suitable for large graphs
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: Bellman-Ford Algorithm (Better)

**Key Insights from Bellman-Ford Solution:**
- Use Bellman-Ford algorithm to find longest paths
- Handle negative weights and detect negative cycles
- Much more efficient than brute force approach
- Standard method for longest path problems with negative weights

**Algorithm:**
1. Initialize distances with -∞ except source (0)
2. Relax all edges for n-1 iterations
3. Check for negative cycles in final iteration
4. Return the maximum distance to destination

**Visual Example:**
```
Bellman-Ford algorithm for graph: 1 ──3──> 2 ──(-1)──> 4
                                    │        │            │
                                    └──(-2)──┼──7─────────┘
                                              │
                                              └──2─────┘

Step 1: Initialize distances
- dist[1] = 0 (source)
- dist[2] = dist[3] = dist[4] = -∞

Step 2: Relax edges for n-1 iterations

Iteration 1:
- dist[2] = max(dist[2], dist[1] + 3) = max(-∞, 0 + 3) = 3
- dist[3] = max(dist[3], dist[1] + (-2)) = max(-∞, 0 + (-2)) = -2
- dist[4] = max(dist[4], dist[1] + 2) = max(-∞, 0 + 2) = 2

Iteration 2:
- dist[4] = max(dist[4], dist[2] + (-1)) = max(2, 3 + (-1)) = 2
- dist[4] = max(dist[4], dist[3] + 7) = max(2, -2 + 7) = 5

Iteration 3:
- No more updates

Step 3: Check for negative cycles
- No negative cycles detected
- Final distance to city 4: 5
```

**Implementation:**
```python
def high_score_bellman_ford(n, m, flights):
    def bellman_ford():
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        
        # Relax edges n-1 times
        for _ in range(n - 1):
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        distances[b] = distances[a] + c
        
        # Check for negative cycles that can reach node n
        for _ in range(n - 1):
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        # If this edge can reach node n, there's a positive cycle
                        if can_reach_n(b, n, flights):
                            return float('inf')
        
        return distances[n]
    
    def can_reach_n(start, target, flights):
        # Simple DFS to check if we can reach target from start
        visited = [False] * (n + 1)
        
        def dfs(node):
            if node == target:
                return True
            if visited[node]:
                return False
            visited[node] = True
            
            for a, b, c in flights:
                if a == node and not visited[b]:
                    if dfs(b):
                        return True
            return False
        
        return dfs(start)
    
    result = bellman_ford()
    
    if result == float('inf'):
        return -1  # Positive cycle found
    elif result == float('-inf'):
        return -1  # No path exists
    else:
        return result
```

**Time Complexity:** O(n × m) for n iterations
**Space Complexity:** O(n) for distance array

**Why it's better:**
- Polynomial time complexity O(n × m)
- Standard method for longest path problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Bellman-Ford with Early Termination (Optimal)

**Key Insights from Optimized Bellman-Ford Solution:**
- Use early termination when no more updates occur
- Optimize cycle detection for better performance
- Most efficient approach for longest path problems
- Standard method in competitive programming

**Algorithm:**
1. Initialize distances with -∞ except source (0)
2. Relax all edges with early termination
3. Check for negative cycles efficiently
4. Return the maximum distance to destination

**Visual Example:**
```
Optimized Bellman-Ford algorithm for graph: 1 ──3──> 2 ──(-1)──> 4
                                               │        │            │
                                               └──(-2)──┼──7─────────┘
                                                         │
                                                         └──2─────┘

Step 1: Initialize distances
- dist[1] = 0 (source)
- dist[2] = dist[3] = dist[4] = -∞

Step 2: Relax edges with early termination

Iteration 1:
- dist[2] = max(dist[2], dist[1] + 3) = max(-∞, 0 + 3) = 3
- dist[3] = max(dist[3], dist[1] + (-2)) = max(-∞, 0 + (-2)) = -2
- dist[4] = max(dist[4], dist[1] + 2) = max(-∞, 0 + 2) = 2
- Updates occurred, continue

Iteration 2:
- dist[4] = max(dist[4], dist[2] + (-1)) = max(2, 3 + (-1)) = 2
- dist[4] = max(dist[4], dist[3] + 7) = max(2, -2 + 7) = 5
- Updates occurred, continue

Iteration 3:
- No more updates, terminate early
- Final distance to city 4: 5
```

**Implementation:**
```python
def high_score_optimized_bellman_ford(n, m, flights):
    def bellman_ford_optimized():
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        
        # Relax edges with early termination
        for iteration in range(n - 1):
            updated = False
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        distances[b] = distances[a] + c
                        updated = True
            
            if not updated:
                break  # Early termination
        
        # Check for negative cycles that can reach node n
        for _ in range(n - 1):
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        # If this edge can reach node n, there's a positive cycle
                        if can_reach_n(b, n, flights):
                            return float('inf')
        
        return distances[n]
    
    def can_reach_n(start, target, flights):
        # Simple DFS to check if we can reach target from start
        visited = [False] * (n + 1)
        
        def dfs(node):
            if node == target:
                return True
            if visited[node]:
                return False
            visited[node] = True
            
            for a, b, c in flights:
                if a == node and not visited[b]:
                    if dfs(b):
                        return True
        return False
        
        return dfs(start)
    
    result = bellman_ford_optimized()
    
    if result == float('inf'):
        return -1  # Positive cycle found
    elif result == float('-inf'):
        return -1  # No path exists
    else:
        return result

def solve_high_score():
    n, m = map(int, input().split())
    flights = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        flights.append((a, b, c))
    
    result = high_score_optimized_bellman_ford(n, m, flights)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_high_score()
```

**Time Complexity:** O(n × m) for n iterations with early termination
**Space Complexity:** O(n) for distance array

**Why it's optimal:**
- O(n × m) time complexity is optimal for Bellman-Ford
- Uses early termination to improve performance
- Most efficient approach for competitive programming
- Standard method for longest path problems

## 🎯 Problem Variations

### Variation 1: Longest Path with Different Weight Constraints
**Problem**: Find longest path with different weight constraints and penalties.

**Link**: [CSES Problem Set - Longest Path with Weight Constraints](https://cses.fi/problemset/task/longest_path_weight_constraints)

```python
def high_score_weight_constraints(n, m, flights, weight_constraints):
    def bellman_ford_optimized():
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        
        # Relax edges with early termination
        for iteration in range(n - 1):
            updated = False
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    # Apply weight constraints
                    if c >= weight_constraints.get('min_weight', float('-inf')):
                        if distances[a] + c > distances[b]:
                            distances[b] = distances[a] + c
                            updated = True
            
            if not updated:
                break  # Early termination
        
        # Check for negative cycles that can reach node n
        for _ in range(n - 1):
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        if can_reach_n(b, n, flights):
                            return float('inf')
        
        return distances[n]
    
    def can_reach_n(start, target, flights):
        visited = [False] * (n + 1)
        
        def dfs(node):
            if node == target:
                return True
            if visited[node]:
                return False
            visited[node] = True
            
            for a, b, c in flights:
                if a == node and not visited[b]:
                    if dfs(b):
                        return True
        return False
    
        return dfs(start)
    
    result = bellman_ford_optimized()
    
    if result == float('inf'):
        return -1  # Positive cycle found
    elif result == float('-inf'):
        return -1  # No path exists
    else:
        return result
```

### Variation 2: Longest Path with Multiple Destinations
**Problem**: Find longest path with multiple possible destinations.

**Link**: [CSES Problem Set - Longest Path Multiple Destinations](https://cses.fi/problemset/task/longest_path_multiple_destinations)

```python
def high_score_multiple_destinations(n, m, flights, destinations):
    def bellman_ford_optimized():
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        
        # Relax edges with early termination
        for iteration in range(n - 1):
            updated = False
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        distances[b] = distances[a] + c
                        updated = True
            
            if not updated:
                break  # Early termination
        
        # Check for negative cycles that can reach any destination
        for _ in range(n - 1):
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        if can_reach_any_destination(b, destinations, flights):
                        return float('inf')
            
        # Find maximum distance to any destination
        max_distance = float('-inf')
        for dest in destinations:
            if distances[dest] > max_distance:
                max_distance = distances[dest]
        
        return max_distance
    
    def can_reach_any_destination(start, destinations, flights):
        visited = [False] * (n + 1)
        
        def dfs(node):
            if node in destinations:
                return True
            if visited[node]:
                return False
            visited[node] = True
            
            for a, b, c in flights:
                if a == node and not visited[b]:
                    if dfs(b):
                    return True
            return False
        
        return dfs(start)
    
    result = bellman_ford_optimized()
    
    if result == float('inf'):
        return -1  # Positive cycle found
    elif result == float('-inf'):
        return -1  # No path exists
    else:
        return result
```

### Variation 3: Longest Path with Path Length Constraints
**Problem**: Find longest path with maximum path length constraints.

**Link**: [CSES Problem Set - Longest Path Length Constraints](https://cses.fi/problemset/task/longest_path_length_constraints)

```python
def high_score_length_constraints(n, m, flights, max_length):
    def bellman_ford_optimized():
    distances = [float('-inf')] * (n + 1)
    distances[1] = 0
    
        # Relax edges with early termination and length constraints
        for iteration in range(min(n - 1, max_length)):
            updated = False
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        distances[b] = distances[a] + c
                        updated = True
            
            if not updated:
                break  # Early termination
        
        # Check for negative cycles that can reach node n
        for _ in range(min(n - 1, max_length)):
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        if can_reach_n(b, n, flights):
                        return float('inf')
    
    return distances[n]

    def can_reach_n(start, target, flights):
    visited = [False] * (n + 1)
    
        def dfs(node):
        if node == target:
            return True
            if visited[node]:
                return False
            visited[node] = True
            
            for a, b, c in flights:
                if a == node and not visited[b]:
                    if dfs(b):
                        return True
    return False

        return dfs(start)
    
    result = bellman_ford_optimized()

if result == float('inf'):
        return -1  # Positive cycle found
elif result == float('-inf'):
        return -1  # No path exists
else:
        return result
```

## 🔗 Related Problems

- **[Shortest Routes I](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_i_analysis/)**: Shortest path problems
- **[Shortest Routes II](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_ii_analysis/)**: All-pairs shortest paths
- **[Flight Discount](/cses-analyses/problem_soulutions/graph_algorithms/flight_discount_analysis/)**: Path optimization problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Longest Path**: Essential for analyzing path optimization and scoring problems
2. **Bellman-Ford Algorithm**: Key algorithm for handling negative weights
3. **Negative Cycle Detection**: Critical for preventing infinite scores
4. **Early Termination**: Important optimization technique for graph algorithms
5. **Path Optimization**: Foundation for many real-world routing problems
6. **Graph Theory**: Foundation for many optimization problems

## 📝 Summary

The High Score problem demonstrates fundamental longest path concepts for analyzing path optimization with negative weights. We explored three approaches:

1. **Brute Force Path Enumeration**: O(2^n × n) time complexity using exhaustive search, inefficient for large graphs
2. **Bellman-Ford Algorithm**: O(n × m) time complexity using edge relaxation, better approach for longest path problems
3. **Optimized Bellman-Ford with Early Termination**: O(n × m) time complexity with early termination, optimal approach for longest path

The key insights include understanding longest path as maximization problems, using Bellman-Ford for negative weight handling, and applying cycle detection for preventing infinite scores. This problem serves as an excellent introduction to longest path algorithms and path optimization techniques.

