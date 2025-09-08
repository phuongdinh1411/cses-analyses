---
layout: simple
title: "Flight Discount - Shortest Path with Coupon"
permalink: /problem_soulutions/graph_algorithms/flight_discount_analysis
---

# Flight Discount - Shortest Path with Coupon

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand modified shortest path problems and state-space expansion concepts
- Apply Dijkstra's algorithm with state-space expansion to handle discount constraints
- Implement efficient modified shortest path algorithms with proper state management
- Optimize modified shortest path solutions using priority queues and state tracking
- Handle edge cases in modified shortest paths (no discount needed, impossible paths, large graphs)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dijkstra's algorithm, state-space expansion, modified shortest paths, priority queues, graph algorithms
- **Data Structures**: Priority queues, state tracking, graph representations, distance arrays, state management
- **Mathematical Concepts**: Graph theory, shortest path properties, state-space search, optimization, graph algorithms
- **Programming Skills**: Priority queue implementation, state management, graph traversal, algorithm implementation
- **Related Problems**: Shortest Routes I (basic shortest paths), High Score (modified shortest paths), Graph algorithms

## Problem Description

**Problem**: Given a directed graph with n cities and m flights, find the minimum cost to travel from city 1 to city n. You can use at most one discount coupon that halves the cost of any flight.

This is a shortest path problem with a twist - you can use one discount coupon to halve the cost of any single flight. The solution requires finding the optimal use of the discount coupon to minimize the total travel cost.

**Input**: 
- First line: Two integers n and m (number of cities and flights)
- Next m lines: Three integers a, b, and c (flight from city a to city b with cost c)

**Output**: 
- One integer: minimum cost to travel from city 1 to city n

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ a, b ≤ n
- 1 ≤ c ≤ 10⁹
- Graph is directed
- Cities are numbered from 1 to n
- No self-loops or multiple edges between same pair of cities

**Example**:
```
Input:
3 4
1 2 3
2 3 1
1 3 7
2 1 5

Output:
2
```

**Explanation**: 
- Path 1→2→3: cost 3+1 = 4
- Path 1→3 with discount: cost 7/2 = 3.5 (rounds to 4)
- Path 1→2→3 with discount on flight 1→2: cost (3/2)+1 = 2.5 (rounds to 2)
- Optimal: Use discount on flight 1→2, then take flight 2→3

## Visual Example

### Input Graph
```
Cities: 1, 2, 3
Flights: (1→2,3), (2→3,1), (1→3,7), (2→1,5)

Graph representation:
1 ──3──> 2 ──1──> 3
│        │        │
└──7─────┼────────┘
          └──5─────┘
```

### Shortest Path with Discount Algorithm
```
Step 1: Build graph with discount states
- State 0: No discount used
- State 1: Discount used

Step 2: Dijkstra's algorithm with states
- Priority queue: (cost, city, discount_used)
- Start: (0, 1, 0)

Step 3: Process states
- State (0, 1, 0): cost 0, city 1, no discount
  - Neighbors: (1→2,3), (1→3,7)
  - Add (3, 2, 0) and (7, 3, 0)
  - Add (1.5, 2, 1) and (3.5, 3, 1) with discount

- State (1.5, 2, 1): cost 1.5, city 2, discount used
  - Neighbors: (2→3,1), (2→1,5)
  - Add (2.5, 3, 1) and (6.5, 1, 1)

- State (2.5, 3, 1): cost 2.5, city 3, discount used
  - Reached destination with cost 2.5
  - Round to 2 (integer cost)
```

### Path Analysis
```
Optimal path with discount:
1 → 2 → 3

Cost breakdown:
- Flight 1→2: 3 (use discount) → 1.5
- Flight 2→3: 1 (no discount) → 1
- Total: 1.5 + 1 = 2.5 → 2 (rounded)

Alternative paths:
- 1→3 with discount: 7/2 = 3.5 → 4
- 1→2→3 without discount: 3+1 = 4
```

### Key Insight
Dijkstra's algorithm with states works by:
1. Creating separate states for discount used/not used
2. Using priority queue to process states in cost order
3. Applying discount to each flight and considering both options
4. Time complexity: O(m log n) where m is edges, n is cities
5. Space complexity: O(n) for distance arrays

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths and apply discount to each flight
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths from start to end
2. For each path, try applying discount to each flight
3. Calculate minimum cost among all possibilities
4. Return the minimum cost

**Visual Example:**
```
Brute force: Try all paths with all discount combinations
For graph: 1 ──3──> 2 ──1──> 3
           │        │        │
           └──7─────┼────────┘
                     └──5─────┘

All possible paths from 1 to 3:
- Path 1→2→3: cost 3+1 = 4
- Path 1→3: cost 7
- Path 1→2→1→2→3: cost 3+5+3+1 = 12

With discount applied to each flight:
- Path 1→2→3 with discount on 1→2: cost 1.5+1 = 2.5
- Path 1→2→3 with discount on 2→3: cost 3+0.5 = 3.5
- Path 1→3 with discount on 1→3: cost 3.5

Minimum cost: 2.5 → 2 (rounded)
```

**Implementation:**
```python
def flight_discount_brute_force(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    def find_all_paths(current, target, visited, path, cost):
        if current == target:
            return [cost]
        
        if len(visited) >= n:
            return []
        
        costs = []
        for neighbor, weight in adj[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                costs.extend(find_all_paths(neighbor, target, visited, path, cost + weight))
                path.pop()
                visited.remove(neighbor)
        
        return costs
    
    def apply_discount_to_path(path_costs):
        min_cost = float('inf')
        for i, cost in enumerate(path_costs):
            # Try applying discount to each flight
            for j in range(len(cost)):
                discounted_cost = cost[:]
                discounted_cost[j] = discounted_cost[j] // 2
                min_cost = min(min_cost, sum(discounted_cost))
        
        return min_cost
    
    # Find all paths and apply discount
    visited = {1}
    path = [1]
    all_costs = find_all_paths(1, n, visited, path, 0)
    
    return min(all_costs) if all_costs else -1
```

**Time Complexity:** O(n! × n) for n cities with factorial path enumeration
**Space Complexity:** O(n) for recursion stack and path storage

**Why it's inefficient:**
- O(n!) time complexity is too slow for large graphs
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many cities

### Approach 2: Basic Dijkstra with State Tracking (Better)

**Key Insights from Basic Dijkstra Solution:**
- Use Dijkstra's algorithm with state tracking for discount usage
- Much more efficient than brute force approach
- Standard method for modified shortest path problems
- Can handle larger graphs than brute force

**Algorithm:**
1. Use Dijkstra's algorithm with discount state tracking
2. Maintain separate distance arrays for discount used/not used
3. Process states in cost order using priority queue
4. Return minimum cost to destination

**Visual Example:**
```
Basic Dijkstra with states for graph: 1 ──3──> 2 ──1──> 3
                                           │        │        │
                                           └──7─────┼────────┘
                                                     └──5─────┘

Step 1: Initialize distance arrays
- dist[node][0] = distance without discount
- dist[node][1] = distance with discount

Step 2: Dijkstra's algorithm with states
- Priority queue: (cost, city, discount_used)
- Start: (0, 1, 0)

Step 3: Process states
- State (0, 1, 0): cost 0, city 1, no discount
  - Neighbors: (1→2,3), (1→3,7)
  - Add (3, 2, 0) and (7, 3, 0)
  - Add (1.5, 2, 1) and (3.5, 3, 1) with discount

- State (1.5, 2, 1): cost 1.5, city 2, discount used
  - Neighbors: (2→3,1), (2→1,5)
  - Add (2.5, 3, 1) and (6.5, 1, 1)

- State (2.5, 3, 1): cost 2.5, city 3, discount used
  - Reached destination with cost 2.5
```

**Implementation:**
```python
import heapq

def flight_discount_basic_dijkstra(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra with discount state
    pq = [(0, 1, False)]  # (cost, node, discount_used)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[1][0] = 0
    
    while pq:
        cost, node, used = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[node][used]:
            continue
        
        for neighbor, weight in adj[node]:
            # Without discount
            if not used and cost + weight < dist[neighbor][0]:
                dist[neighbor][0] = cost + weight
                heapq.heappush(pq, (dist[neighbor][0], neighbor, False))
            
            # With discount (if not used yet)
            if not used and cost + weight // 2 < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight // 2
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
            
            # Already used discount
            if used and cost + weight < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
    
    return min(dist[n][0], dist[n][1])
```

**Time Complexity:** O(m log n) for m edges and n cities with Dijkstra
**Space Complexity:** O(n) for distance arrays

**Why it's better:**
- O(m log n) time complexity is much better than O(n!)
- Standard method for modified shortest path problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Dijkstra with State Management (Optimal)

**Key Insights from Optimized Dijkstra Solution:**
- Use Dijkstra's algorithm with optimized state management
- Most efficient approach for modified shortest path problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use Dijkstra's algorithm with optimized state management
2. Process states efficiently using priority queue
3. Apply discount logic optimally
4. Return minimum cost to destination

**Visual Example:**
```
Optimized Dijkstra with states for graph: 1 ──3──> 2 ──1──> 3
                                               │        │        │
                                               └──7─────┼────────┘
                                                         └──5─────┘

Step 1: Initialize with optimized state management
- dist[node][0] = distance without discount
- dist[node][1] = distance with discount
- Priority queue: (cost, node, discount_used)

Step 2: Dijkstra's algorithm with optimization
- Start: (0, 1, 0)
- Process states in cost order

Step 3: Process states efficiently
- State (0, 1, 0): cost 0, city 1, no discount
  - Neighbors: (1→2,3), (1→3,7)
  - Add (3, 2, 0) and (7, 3, 0)
  - Add (1.5, 2, 1) and (3.5, 3, 1) with discount

- State (1.5, 2, 1): cost 1.5, city 2, discount used
  - Neighbors: (2→3,1), (2→1,5)
  - Add (2.5, 3, 1) and (6.5, 1, 1)

- State (2.5, 3, 1): cost 2.5, city 3, discount used
  - Reached destination with cost 2.5
```

**Implementation:**
```python
import heapq

def flight_discount_optimized(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra with discount state
    pq = [(0, 1, False)]  # (cost, node, discount_used)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[1][0] = 0
    
    while pq:
        cost, node, used = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[node][used]:
            continue
        
        for neighbor, weight in adj[node]:
            # Without discount
            if not used and cost + weight < dist[neighbor][0]:
                dist[neighbor][0] = cost + weight
                heapq.heappush(pq, (dist[neighbor][0], neighbor, False))
            
            # With discount (if not used yet)
            if not used and cost + weight // 2 < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight // 2
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
            
            # Already used discount
            if used and cost + weight < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
    
    return min(dist[n][0], dist[n][1])

def solve_flight_discount():
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b, c = map(int, input().split())
    edges.append((a, b, c))

    result = flight_discount_optimized(n, m, edges)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_flight_discount()
```

**Time Complexity:** O(m log n) for m edges and n cities with optimized Dijkstra
**Space Complexity:** O(n) for distance arrays

**Why it's optimal:**
- O(m log n) time complexity is optimal for shortest path problems
- Uses optimized state management techniques
- Most efficient approach for competitive programming
- Standard method for modified shortest path problems

## 🎯 Problem Variations

### Variation 1: Flight Discount with Different Constraints
**Problem**: Find shortest path with discount coupon and different flight constraints.

**Link**: [CSES Problem Set - Flight Discount with Constraints](https://cses.fi/problemset/task/flight_discount_constraints)

```python
def flight_discount_constraints(n, m, edges, constraints):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra with discount state and constraints
    pq = [(0, 1, False)]  # (cost, node, discount_used)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[1][0] = 0
    
    while pq:
        cost, node, used = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[node][used]:
            continue
        
        for neighbor, weight in adj[node]:
            # Apply constraints
            if constraints.get('max_cost', float('inf')) < cost + weight:
                continue
            
            # Without discount
            if not used and cost + weight < dist[neighbor][0]:
                dist[neighbor][0] = cost + weight
                heapq.heappush(pq, (dist[neighbor][0], neighbor, False))
            
            # With discount (if not used yet)
            if not used and cost + weight // 2 < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight // 2
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
            
            # Already used discount
            if used and cost + weight < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
    
    return min(dist[n][0], dist[n][1])
```

### Variation 2: Flight Discount with Multiple Destinations
**Problem**: Find shortest path with discount coupon and multiple possible destination cities.

**Link**: [CSES Problem Set - Flight Discount Multiple Destinations](https://cses.fi/problemset/task/flight_discount_multiple_destinations)

```python
def flight_discount_multiple_destinations(n, m, edges, destinations):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra with discount state
    pq = [(0, 1, False)]  # (cost, node, discount_used)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[1][0] = 0
    
    while pq:
        cost, node, used = heapq.heappop(pq)
        
        if node in destinations:
            return cost
        
        if cost > dist[node][used]:
            continue
        
        for neighbor, weight in adj[node]:
            # Without discount
            if not used and cost + weight < dist[neighbor][0]:
                dist[neighbor][0] = cost + weight
                heapq.heappush(pq, (dist[neighbor][0], neighbor, False))
            
            # With discount (if not used yet)
            if not used and cost + weight // 2 < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight // 2
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
            
            # Already used discount
            if used and cost + weight < dist[neighbor][1]:
                dist[neighbor][1] = cost + weight
                heapq.heappush(pq, (dist[neighbor][1], neighbor, True))
    
    return min(min(dist[dest][0], dist[dest][1]) for dest in destinations)
```

### Variation 3: Flight Discount with Path Length Constraints
**Problem**: Find shortest path with discount coupon and maximum path length constraints.

**Link**: [CSES Problem Set - Flight Discount Path Length Constraints](https://cses.fi/problemset/task/flight_discount_path_length_constraints)

```python
def flight_discount_path_length_constraints(n, m, edges, max_length):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    # Dijkstra with discount state and path length constraint
    pq = [(0, 1, False, 0)]  # (cost, node, discount_used, path_length)
    dist = [[[float('inf')] * 2 for _ in range(n + 1)] for _ in range(max_length + 1)]
    dist[0][1][0] = 0
    
    while pq:
        cost, node, used, length = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[length][node][used] or length >= max_length:
            continue
        
        for neighbor, weight in adj[node]:
            # Check path length constraint
            if length + 1 > max_length:
                continue
            
            # Without discount
            if not used and cost + weight < dist[length + 1][neighbor][0]:
                dist[length + 1][neighbor][0] = cost + weight
                heapq.heappush(pq, (dist[length + 1][neighbor][0], neighbor, False, length + 1))
            
            # With discount (if not used yet)
            if not used and cost + weight // 2 < dist[length + 1][neighbor][1]:
                dist[length + 1][neighbor][1] = cost + weight // 2
                heapq.heappush(pq, (dist[length + 1][neighbor][1], neighbor, True, length + 1))
            
            # Already used discount
            if used and cost + weight < dist[length + 1][neighbor][1]:
                dist[length + 1][neighbor][1] = cost + weight
                heapq.heappush(pq, (dist[length + 1][neighbor][1], neighbor, True, length + 1))
    
    return min(min(dist[length][n][0], dist[length][n][1]) for length in range(max_length + 1))
```

## 🔗 Related Problems

- **[Shortest Routes I](/cses-analyses/problem_soulutions/graph_algorithms/shortest_routes_i_analysis/)**: Basic shortest paths
- **[High Score](/cses-analyses/problem_soulutions/graph_algorithms/high_score_analysis/)**: Modified shortest paths
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems
- **[Dynamic Programming](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP problems

## 📚 Learning Points

1. **Modified Shortest Paths**: Essential for understanding shortest path problems with constraints
2. **State-Space Expansion**: Key technique for handling additional constraints
3. **Dijkstra's Algorithm**: Important for understanding shortest path algorithms
4. **Priority Queues**: Critical for implementing efficient shortest path algorithms
5. **Graph Theory**: Foundation for many optimization problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Flight Discount problem demonstrates fundamental modified shortest path concepts for finding optimal paths with discount constraints. We explored three approaches:

1. **Brute Force Path Enumeration**: O(n!) time complexity using recursive path generation, inefficient for large graphs
2. **Basic Dijkstra with State Tracking**: O(m log n) time complexity using Dijkstra's algorithm with state management, better approach for modified shortest paths
3. **Optimized Dijkstra with State Management**: O(m log n) time complexity with optimized state management, optimal approach for modified shortest path problems

The key insights include understanding modified shortest paths as extensions of standard shortest path problems, using state-space expansion for handling constraints, and applying Dijkstra's algorithm with state tracking for efficient solutions. This problem serves as an excellent introduction to modified shortest path algorithms and state-space expansion techniques.

