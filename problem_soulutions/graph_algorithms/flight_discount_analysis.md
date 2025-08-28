---
layout: simple
title: "Flight Discount"
permalink: /problem_soulutions/graph_algorithms/flight_discount_analysis
---


# Flight Discount

## Problem Statement
Given a directed graph with n cities and m flights, find the minimum cost to travel from city 1 to city n. You can use at most one discount coupon that halves the cost of any flight.

### Input
The first input line has two integers n and m: the number of cities and flights.
Then there are m lines describing the flights. Each line has three integers a, b, and c: there is a flight from city a to city b with cost c.

### Output
Print one integer: the minimum cost to travel from city 1 to city n.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n
- 1 ≤ c ≤ 10^9

### Example
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

## Solution Progression

### Approach 1: Dijkstra with Discount State - O(m log n)
**Description**: Use Dijkstra's algorithm with a state to track discount usage.

```python
import heapq

def flight_discount_naive(n, m, edges):
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

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Dijkstra with State - O(m log n)
**Description**: Use optimized Dijkstra with cleaner state management.

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
            # Try without discount
            new_cost = cost + weight
            if new_cost < dist[neighbor][used]:
                dist[neighbor][used] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, used))
            
            # Try with discount (if not used yet)
            if not used:
                new_cost = cost + weight // 2
                if new_cost < dist[neighbor][1]:
                    dist[neighbor][1] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, True))
    
    return min(dist[n][0], dist[n][1])
```

**Why this improvement works**: We use Dijkstra's algorithm with a state to track whether the discount has been used. We maintain two distances for each node: one without discount and one with discount.

## Final Optimal Solution

```python
import heapq

n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b, c = map(int, input().split())
    edges.append((a, b, c))

def find_minimum_cost_with_discount(n, m, edges):
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
            # Try without discount
            new_cost = cost + weight
            if new_cost < dist[neighbor][used]:
                dist[neighbor][used] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, used))
            
            # Try with discount (if not used yet)
            if not used:
                new_cost = cost + weight // 2
                if new_cost < dist[neighbor][1]:
                    dist[neighbor][1] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, True))
    
    return min(dist[n][0], dist[n][1])

result = find_minimum_cost_with_discount(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Dijkstra with State | O(m log n) | O(n) | Use state to track discount usage |
| Optimized Dijkstra | O(m log n) | O(n) | Cleaner state management |

## Key Insights for Other Problems

### 1. **Dijkstra with State**
**Principle**: Use Dijkstra's algorithm with additional state to handle constraints like discount usage.
**Applicable to**: Shortest path problems, constraint problems, graph problems

### 2. **State Management**
**Principle**: Maintain multiple distances for each node based on different states.
**Applicable to**: State-dependent problems, constraint problems, optimization problems

### 3. **Discount Optimization**
**Principle**: Find optimal use of limited resources (like discounts) in path problems.
**Applicable to**: Resource optimization problems, path problems, constraint problems

## Notable Techniques

### 1. **Dijkstra with State**
```python
def dijkstra_with_state(n, adj, start, end):
    pq = [(0, start, False)]  # (cost, node, state)
    dist = [[float('inf')] * 2 for _ in range(n + 1)]
    dist[start][0] = 0
    
    while pq:
        cost, node, state = heapq.heappop(pq)
        
        if node == end:
            return cost
        
        if cost > dist[node][state]:
            continue
        
        for neighbor, weight in adj[node]:
            # Process with current state
            new_cost = cost + weight
            if new_cost < dist[neighbor][state]:
                dist[neighbor][state] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, state))
            
            # Process with state change (if applicable)
            if not state:
                new_cost = cost + weight // 2
                if new_cost < dist[neighbor][1]:
                    dist[neighbor][1] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, True))
    
    return min(dist[end][0], dist[end][1])
```

### 2. **State Tracking**
```python
def track_state(cost, node, used, dist, pq):
    if cost < dist[node][used]:
        dist[node][used] = cost
        heapq.heappush(pq, (cost, node, used))
```

### 3. **Discount Application**
```python
def apply_discount(weight, discount_used):
    if not discount_used:
        return weight // 2
    return weight
```

## Problem-Solving Framework

1. **Identify problem type**: This is a shortest path problem with a discount constraint
2. **Choose approach**: Use Dijkstra's algorithm with state tracking
3. **Define state**: Track whether discount has been used
4. **Initialize**: Set up priority queue and distance arrays
5. **Process nodes**: Handle both with and without discount cases
6. **Update distances**: Maintain separate distances for each state
7. **Return result**: Output minimum of both final states

---

*This analysis shows how to efficiently find the minimum cost path with discount using Dijkstra's algorithm with state tracking.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Flight Discount with Multiple Discounts**
**Problem**: Each flight can have multiple discounts with different percentages.
```python
def multiple_discount_flight(n, m, edges, discounts):
    # discounts[(a, b)] = list of available discounts for edge (a, b)
    
    # Build adjacency list with discounts
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        edge_discounts = discounts.get((a, b), [])
        adj[a].append((b, c, edge_discounts))
    
    # Dijkstra with multiple discount states
    import heapq
    
    # dist[node][discount_mask] = minimum cost to reach node with discount usage mask
    dist = [[float('inf')] * (1 << len(discounts)) for _ in range(n + 1)]
    dist[1][0] = 0
    
    pq = [(0, 1, 0)]  # (cost, node, discount_mask)
    
    while pq:
        cost, node, mask = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[node][mask]:
            continue
        
        for neighbor, weight, edge_discounts in adj[node]:
            # Try without using any discount
            new_cost = cost + weight
            if new_cost < dist[neighbor][mask]:
                dist[neighbor][mask] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, mask))
            
            # Try using each available discount
            for i, discount in enumerate(edge_discounts):
                if not (mask & (1 << i)):  # Discount not used yet
                    discounted_cost = cost + weight * (100 - discount) // 100
                    new_mask = mask | (1 << i)
                    if discounted_cost < dist[neighbor][new_mask]:
                        dist[neighbor][new_mask] = discounted_cost
                        heapq.heappush(pq, (discounted_cost, neighbor, new_mask))
    
    return min(dist[n])
```

#### **Variation 2: Flight Discount with Constraints**
**Problem**: Find minimum cost path with constraints on discount usage.
```python
def constrained_flight_discount(n, m, edges, constraints):
    # constraints = {'max_discounts': x, 'min_cost': y, 'max_cost': z}
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        adj[a].append((b, c))
    
    import heapq
    
    # dist[node][discounts_used] = minimum cost to reach node with discounts_used
    dist = [[float('inf')] * (constraints.get('max_discounts', 1) + 1) for _ in range(n + 1)]
    dist[1][0] = 0
    
    pq = [(0, 1, 0)]  # (cost, node, discounts_used)
    
    while pq:
        cost, node, discounts_used = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        # Apply cost constraints
        if 'min_cost' in constraints and cost < constraints['min_cost']:
            continue
        if 'max_cost' in constraints and cost > constraints['max_cost']:
            continue
        
        if cost > dist[node][discounts_used]:
            continue
        
        for neighbor, weight in adj[node]:
            # Try without discount
            new_cost = cost + weight
            if new_cost < dist[neighbor][discounts_used]:
                dist[neighbor][discounts_used] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, discounts_used))
            
            # Try with discount (if available)
            if discounts_used < constraints.get('max_discounts', 1):
                discounted_cost = cost + weight // 2
                if discounted_cost < dist[neighbor][discounts_used + 1]:
                    dist[neighbor][discounts_used + 1] = discounted_cost
                    heapq.heappush(pq, (discounted_cost, neighbor, discounts_used + 1))
    
    return min(dist[n])
```

#### **Variation 3: Flight Discount with Probabilities**
**Problem**: Each discount has a probability of working, find expected minimum cost.
```python
def probabilistic_flight_discount(n, m, edges, discount_probabilities):
    # discount_probabilities[(a, b)] = probability that discount works for edge (a, b)
    
    # Build adjacency list with probabilities
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        prob = discount_probabilities.get((a, b), 0.0)
        adj[a].append((b, c, prob))
    
    import heapq
    
    # dist[node][discount_used] = (cost, probability)
    dist = [[(float('inf'), 0.0)] * 2 for _ in range(n + 1)]
    dist[1][0] = (0, 1.0)
    
    pq = [(0, 1, False, 1.0)]  # (cost, node, discount_used, probability)
    
    while pq:
        cost, node, used, prob = heapq.heappop(pq)
        
        if node == n:
            return cost, prob
        
        if cost > dist[node][used][0]:
            continue
        
        for neighbor, weight, discount_prob in adj[node]:
            # Try without discount
            new_cost = cost + weight
            if new_cost < dist[neighbor][used][0]:
                dist[neighbor][used] = (new_cost, prob)
                heapq.heappush(pq, (new_cost, neighbor, used, prob))
            
            # Try with discount (if not used yet)
            if not used:
                discounted_cost = cost + weight // 2
                new_prob = prob * discount_prob
                if discounted_cost < dist[neighbor][1][0]:
                    dist[neighbor][1] = (discounted_cost, new_prob)
                    heapq.heappush(pq, (discounted_cost, neighbor, True, new_prob))
    
    # Return minimum cost path with its probability
    if dist[n][0][0] < dist[n][1][0]:
        return dist[n][0]
    else:
        return dist[n][1]
```

#### **Variation 4: Flight Discount with Time Constraints**
**Problem**: Each flight has a time duration, find minimum cost path within time limit.
```python
def time_constrained_flight_discount(n, m, edges, time_limit):
    # edges = [(a, b, cost, time), ...]
    
    # Build adjacency list with times
    adj = [[] for _ in range(n + 1)]
    for a, b, cost, time in edges:
        adj[a].append((b, cost, time))
    
    import heapq
    
    # dist[node][discount_used][time] = minimum cost to reach node with discount_used at time
    dist = [[[float('inf')] * (time_limit + 1) for _ in range(2)] for _ in range(n + 1)]
    dist[1][0][0] = 0
    
    pq = [(0, 1, False, 0)]  # (cost, node, discount_used, time)
    
    while pq:
        cost, node, used, time = heapq.heappop(pq)
        
        if node == n:
            return cost
        
        if cost > dist[node][used][time]:
            continue
        
        for neighbor, weight, flight_time in adj[node]:
            new_time = time + flight_time
            if new_time > time_limit:
                continue
            
            # Try without discount
            new_cost = cost + weight
            if new_cost < dist[neighbor][used][new_time]:
                dist[neighbor][used][new_time] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, used, new_time))
            
            # Try with discount (if not used yet)
            if not used:
                discounted_cost = cost + weight // 2
                if discounted_cost < dist[neighbor][1][new_time]:
                    dist[neighbor][1][new_time] = discounted_cost
                    heapq.heappush(pq, (discounted_cost, neighbor, True, new_time))
    
    # Find minimum cost within time limit
    min_cost = float('inf')
    for used in range(2):
        for t in range(time_limit + 1):
            min_cost = min(min_cost, dist[n][used][t])
    
    return min_cost if min_cost != float('inf') else -1
```

#### **Variation 5: Flight Discount with Dynamic Updates**
**Problem**: Handle dynamic updates to flight costs and find minimum cost after each update.
```python
def dynamic_flight_discount(n, m, initial_edges, updates):
    # updates = [(edge_index, new_cost), ...]
    
    edges = initial_edges.copy()
    results = []
    
    for edge_index, new_cost in updates:
        # Update edge cost
        a, b, old_cost = edges[edge_index]
        edges[edge_index] = (a, b, new_cost)
        
        # Rebuild adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b, c in edges:
            adj[a].append((b, c))
        
        # Run Dijkstra with discount
        import heapq
        
        dist = [[float('inf')] * 2 for _ in range(n + 1)]
        dist[1][0] = 0
        
        pq = [(0, 1, False)]
        
        while pq:
            cost, node, used = heapq.heappop(pq)
            
            if node == n:
                break
            
            if cost > dist[node][used]:
                continue
            
            for neighbor, weight in adj[node]:
                # Try without discount
                new_cost = cost + weight
                if new_cost < dist[neighbor][used]:
                    dist[neighbor][used] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, used))
                
                # Try with discount (if not used yet)
                if not used:
                    discounted_cost = cost + weight // 2
                    if discounted_cost < dist[neighbor][1]:
                        dist[neighbor][1] = discounted_cost
                        heapq.heappush(pq, (discounted_cost, neighbor, True))
        
        result = min(dist[n][0], dist[n][1])
        results.append(result)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Shortest Path Problems**
- **Dijkstra's Algorithm**: Find shortest paths in weighted graphs
- **Bellman-Ford Algorithm**: Handle negative weights
- **Floyd-Warshall Algorithm**: All-pairs shortest paths
- **A* Algorithm**: Heuristic-based shortest path

#### **2. State-Dependent Problems**
- **State Management**: Handle multiple states for each node
- **State Transitions**: Manage transitions between states
- **State Optimization**: Optimize based on state constraints
- **Multi-State Dijkstra**: Dijkstra with multiple states

#### **3. Constraint Problems**
- **Resource Constraints**: Limited resources (discounts, time, etc.)
- **Cost Constraints**: Minimum/maximum cost requirements
- **Time Constraints**: Time-based limitations
- **Probability Constraints**: Probabilistic outcomes

#### **4. Optimization Problems**
- **Cost Optimization**: Minimize total cost
- **Resource Optimization**: Optimal use of limited resources
- **Multi-Criteria Optimization**: Optimize multiple objectives
- **Dynamic Optimization**: Handle dynamic changes

#### **5. Graph Problems**
- **Weighted Graphs**: Graphs with edge weights
- **Directed Graphs**: Directed edge relationships
- **Path Problems**: Finding optimal paths
- **Graph Traversal**: Efficient graph exploration

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a, b, c))
    
    result = find_minimum_cost_with_discount(n, m, edges)
    print(result)
```

#### **2. Range Queries on Flight Costs**
```python
def range_flight_cost_queries(n, edges, queries):
    # queries = [(start_node, end_node), ...] - find minimum cost in range
    
    results = []
    for start, end in queries:
        # Run Dijkstra from start to end
        adj = [[] for _ in range(n + 1)]
        for a, b, c in edges: if start <= a <= end and start <= b <= 
end: adj[a].append((b, c))
        
        result = find_minimum_cost_with_discount(end - start + 1, len(edges), edges)
        results.append(result)
    
    return results
```

#### **3. Interactive Flight Discount Problems**
```python
def interactive_flight_discount():
    n = int(input("Enter number of cities: "))
    m = int(input("Enter number of flights: "))
    print("Enter flights (from to cost):")
    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a, b, c))
    
    result = find_minimum_cost_with_discount(n, m, edges)
    print(f"Minimum cost with discount: {result}")
    
    # Show path details
    path = find_path_with_discount(n, m, edges)
    print(f"Optimal path: {path}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Shortest Path Theory**: Mathematical theory of shortest paths
- **Path Optimization**: Mathematical optimization of paths
- **Graph Algorithms**: Mathematical analysis of graph algorithms
- **Path Analysis**: Analysis of path-based algorithms

#### **2. Optimization Theory**
- **Cost Optimization**: Mathematical cost optimization
- **Resource Optimization**: Mathematical resource optimization
- **Constraint Optimization**: Mathematical constraint optimization
- **Multi-Objective Optimization**: Mathematical multi-objective optimization

#### **3. Probability Theory**
- **Probabilistic Paths**: Probability theory applied to paths
- **Expected Values**: Expected cost calculations
- **Probability Distributions**: Probability distributions in graphs
- **Stochastic Optimization**: Stochastic optimization techniques

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Dijkstra's Algorithm**: Efficient shortest path algorithm
- **State-Dependent Algorithms**: Algorithms with state management
- **Constraint Satisfaction**: Constraint satisfaction algorithms
- **Graph Algorithms**: Various graph algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Optimization Theory**: Mathematical optimization techniques
- **Probability Theory**: Mathematical probability theory
- **Complexity Analysis**: Analysis of algorithm complexity

#### **3. Programming Concepts**
- **State Management**: Efficient state management techniques
- **Priority Queues**: Priority queue data structures
- **Algorithm Optimization**: Improving algorithm performance
- **Dynamic Programming**: Handling dynamic updates

---

*This analysis demonstrates efficient shortest path techniques with constraints and shows various extensions for flight discount problems.* 