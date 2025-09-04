---
layout: simple
title: "High Score - Longest Path with Negative Weights"
permalink: /problem_soulutions/graph_algorithms/high_score_analysis
---

# High Score - Longest Path with Negative Weights

## 📋 Problem Description

There are n cities and m flight connections. Your task is to find the highest possible score for a route from city 1 to city n.

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
2
```

**Explanation**: 
- Path 1 → 2 → 4: score = 3 + (-1) = 2
- Path 1 → 3 → 4: score = (-2) + 7 = 5
- Path 1 → 4: score = 2
- Highest score: 5 (path 1 → 3 → 4)

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find highest score path from city 1 to city n
- **Key Insight**: This is a longest path problem with potentially negative weights
- **Challenge**: Handle negative cycles that could lead to infinite scores

### Step 2: Initial Approach
**Bellman-Ford algorithm for longest path with negative cycle detection:**

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

**Why this is efficient**: Bellman-Ford can handle negative edge weights and detect cycles.

### Improvement 1: Optimized Bellman-Ford with Early Termination - O(n*m)
**Description**: Use optimized Bellman-Ford with early termination and better cycle detection.

```python
def high_score_optimized_bellman_ford(n, m, flights):
    def bellman_ford_optimized():
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        
        # Relax edges n-1 times
        for _ in range(n - 1):
            improved = False
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        distances[b] = distances[a] + c
                        improved = True
            
            # Early termination if no improvement
            if not improved:
                break
        
        # Check for positive cycles that can reach node n
        for _ in range(n - 1):
            for a, b, c in flights:
                if distances[a] != float('-inf'):
                    if distances[a] + c > distances[b]:
                        # Check if this improvement can reach node n
                        if can_reach_n_optimized(b, n, flights, distances):
                            return float('inf')
        
        return distances[n]
    
    def can_reach_n_optimized(start, target, flights, distances):
        # Use BFS for faster reachability check
        from collections import deque
        
        visited = [False] * (n + 1)
        queue = deque([start])
        visited[start] = True
        
        while queue:
            node = queue.popleft()
            if node == target:
                return True
            
            for a, b, c in flights:
                if a == node and not visited[b]:
                    visited[b] = True
                    queue.append(b)
        
        return False
    
    result = bellman_ford_optimized()
    
    if result == float('inf'):
        return -1  # Positive cycle found
    elif result == float('-inf'):
        return -1  # No path exists
    else:
        return result
```

**Why this improvement works**: Early termination and optimized reachability checks improve performance.

### Step 3: Optimization/Alternative
**SPFA (Shortest Path Faster Algorithm) with negative cycle detection:**

```python
from collections import deque

def high_score_spfa(n, m, flights):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def spfa():
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        
        # Queue for nodes to process
        queue = deque([1])
        in_queue = [False] * (n + 1)
        in_queue[1] = True
        
        # Count visits to detect cycles
        visit_count = [0] * (n + 1)
        
        while queue:
            node = queue.popleft()
            in_queue[node] = False
            
            for neighbor, weight in graph[node]:
                new_dist = distances[node] + weight
                if new_dist > distances[neighbor]:
                    distances[neighbor] = new_dist
                    visit_count[neighbor] += 1
                    
                    # If a node is visited too many times, there's a cycle
                    if visit_count[neighbor] >= n:
                        # Check if this cycle can reach node n
                        if can_reach_n_spfa(neighbor, n, graph):
                            return float('inf')
                    
                    if not in_queue[neighbor]:
                        queue.append(neighbor)
                        in_queue[neighbor] = True
        
        return distances[n]
    
    def can_reach_n_spfa(start, target, graph):
        visited = [False] * (n + 1)
        queue = deque([start])
        visited[start] = True
        
        while queue:
            node = queue.popleft()
            if node == target:
                return True
            
            for neighbor, weight in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return False
    
    result = spfa()
    
    if result == float('inf'):
        return -1  # Positive cycle found
    elif result == float('-inf'):
        return -1  # No path exists
    else:
        return result
```

**Why this improvement works**: SPFA is often faster than Bellman-Ford in practice.

### Alternative: DFS with Cycle Detection - O(n*m)
**Description**: Use DFS with cycle detection for educational purposes.

```python
def high_score_dfs(n, m, flights):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    def dfs_with_cycle_detection():
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        visited = [False] * (n + 1)
        in_stack = [False] * (n + 1)
        
        def dfs(node):
            if in_stack[node]:
                # Found a cycle, check if it can reach node n
                if can_reach_n_dfs(node, n, graph):
                    return float('inf')
                return distances[node]
            
            if visited[node]:
                return distances[node]
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor, weight in graph[node]:
                new_dist = distances[node] + weight
                if new_dist > distances[neighbor]:
                    distances[neighbor] = new_dist
                    result = dfs(neighbor)
                    if result == float('inf'):
                        return float('inf')
            
            in_stack[node] = False
            return distances[node]
        
        result = dfs(1)
        return distances[n] if result != float('inf') else float('inf')
    
    def can_reach_n_dfs(start, target, graph):
        visited = [False] * (n + 1)
        
        def dfs_reach(node):
            if node == target:
                return True
            if visited[node]:
                return False
            visited[node] = True
            
            for neighbor, weight in graph[node]:
                if dfs_reach(neighbor):
                    return True
            return False
        
        return dfs_reach(start)
    
    result = dfs_with_cycle_detection()
    
    if result == float('inf'):
        return -1  # Positive cycle found
    elif result == float('-inf'):
        return -1  # No path exists
    else:
        return result
```

**Why this works**: DFS approach can be useful for understanding the problem conceptually.

### Step 4: Complete Solution

```python
from collections import deque

n, m = map(int, input().split())
flights = [tuple(map(int, input().split())) for _ in range(m)]

# Build adjacency list
graph = [[] for _ in range(n + 1)]
for a, b, c in flights:
    graph[a].append((b, c))

def spfa():
    distances = [float('-inf')] * (n + 1)
    distances[1] = 0
    
    # Queue for nodes to process
    queue = deque([1])
    in_queue = [False] * (n + 1)
    in_queue[1] = True
    
    # Count visits to detect cycles
    visit_count = [0] * (n + 1)
    
    while queue:
        node = queue.popleft()
        in_queue[node] = False
        
        for neighbor, weight in graph[node]:
            new_dist = distances[node] + weight
            if new_dist > distances[neighbor]:
                distances[neighbor] = new_dist
                visit_count[neighbor] += 1
                
                # If a node is visited too many times, there's a cycle
                if visit_count[neighbor] >= n:
                    # Check if this cycle can reach node n
                    if can_reach_n(neighbor, n):
                        return float('inf')
                
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True
    
    return distances[n]

def can_reach_n(start, target):
    visited = [False] * (n + 1)
    queue = deque([start])
    visited[start] = True
    
    while queue:
        node = queue.popleft()
        if node == target:
            return True
        
        for neighbor, weight in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    
    return False

result = spfa()

if result == float('inf'):
    print(-1)  # Positive cycle found
elif result == float('-inf'):
    print(-1)  # No path exists
else:
    print(result)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Simple path with positive weights (should return path sum)
- **Test 2**: Path with negative weights (should return maximum score)
- **Test 3**: Graph with positive cycle reachable from destination (should return -1)
- **Test 4**: No path exists (should return -1)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bellman-Ford | O(n*m) | O(n) | Handles negative weights |
| Optimized Bellman-Ford | O(n*m) | O(n) | Early termination |
| SPFA | O(n*m) | O(n + m) | Often faster in practice |
| DFS | O(n*m) | O(n) | Educational approach |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Longest Path Problem**: Find maximum weight path in directed graph
- **Negative Weight Handling**: Use Bellman-Ford or SPFA for negative weights
- **Cycle Detection**: Detect positive cycles that can reach destination
- **Reachability Check**: Verify if cycles can actually reach target node

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Longest Path with Constraints**
```python
def longest_path_with_constraints(n, m, edges, constraints):
    # Find longest path with additional constraints
    # constraints = list of (node, max_visits) tuples
    
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        graph[a].append((b, c))
    
    def spfa_with_constraints():
        # distances[node][visits] = maximum distance to node with visits
        distances = [[float('-inf')] * (max_visits + 1) for _ in range(n + 1)]
        distances[1][0] = 0
        
        queue = deque([(1, 0)])  # (node, visits)
        in_queue = [[False] * (max_visits + 1) for _ in range(n + 1)]
        in_queue[1][0] = True
        
        while queue:
            node, visits = queue.popleft()
            in_queue[node][visits] = False
            
            for neighbor, weight in graph[node]:
                new_visits = visits + 1
                if new_visits <= max_visits:
                    new_dist = distances[node][visits] + weight
                    if new_dist > distances[neighbor][new_visits]:
                        distances[neighbor][new_visits] = new_dist
                        if not in_queue[neighbor][new_visits]:
                            queue.append((neighbor, new_visits))
                            in_queue[neighbor][new_visits] = True
        
        return max(distances[n])
    
    max_visits = max(constraint[1] for constraint in constraints)
    return spfa_with_constraints()
```

#### **2. Multiple Source Longest Path**
```python
def multiple_source_longest_path(n, m, edges, sources):
    # Find longest path from any source to destination
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        graph[a].append((b, c))
    
    def spfa_multiple_sources():
        distances = [float('-inf')] * (n + 1)
        
        # Initialize all sources
        queue = deque()
        in_queue = [False] * (n + 1)
        
        for source in sources:
            distances[source] = 0
            queue.append(source)
            in_queue[source] = True
        
        visit_count = [0] * (n + 1)
        
        while queue:
            node = queue.popleft()
            in_queue[node] = False
            
            for neighbor, weight in graph[node]:
                new_dist = distances[node] + weight
                if new_dist > distances[neighbor]:
                    distances[neighbor] = new_dist
                    visit_count[neighbor] += 1
                    
                    if visit_count[neighbor] >= n:
                        # Check for positive cycle
                        if can_reach_n(neighbor, n):
                            return float('inf')
                    
                    if not in_queue[neighbor]:
                        queue.append(neighbor)
                        in_queue[neighbor] = True
        
        return distances[n]
    
    def can_reach_n(start, target):
        visited = [False] * (n + 1)
        queue = deque([start])
        visited[start] = True
        
        while queue:
            node = queue.popleft()
            if node == target:
                return True
            
            for neighbor, weight in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return False
    
    return spfa_multiple_sources()
```

#### **3. Longest Path with Time Windows**
```python
def longest_path_time_windows(n, m, edges, time_windows):
    # Find longest path with time window constraints
    # time_windows[node] = (earliest_time, latest_time)
    
    from collections import deque
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        graph[a].append((b, c))
    
    def spfa_time_windows():
        # distances[node][time] = maximum distance to node at time
        max_time = max(tw[1] for tw in time_windows.values())
        distances = [[float('-inf')] * (max_time + 1) for _ in range(n + 1)]
        
        # Initialize source at time 0
        distances[1][0] = 0
        queue = deque([(1, 0)])
        in_queue = [[False] * (max_time + 1) for _ in range(n + 1)]
        in_queue[1][0] = True
        
        while queue:
            node, time = queue.popleft()
            in_queue[node][time] = False
            
            for neighbor, weight in graph[node]:
                new_time = time + 1
                if new_time <= max_time:
                    # Check time window constraint
                    earliest, latest = time_windows[neighbor]
                    if earliest <= new_time <= latest:
                        new_dist = distances[node][time] + weight
                        if new_dist > distances[neighbor][new_time]:
                            distances[neighbor][new_time] = new_dist
                            if not in_queue[neighbor][new_time]:
                                queue.append((neighbor, new_time))
                                in_queue[neighbor][new_time] = True
        
        return max(distances[n])
    
    return spfa_time_windows()
```

## 🔗 Related Problems

### Links to Similar Problems
- **Shortest Path**: Related path-finding algorithms
- **Negative Cycle Detection**: Cycle detection problems
- **Graph Algorithms**: Various graph traversal problems
- **Dynamic Programming**: Path optimization problems

## 📚 Learning Points

### Key Takeaways
- **Longest path** problems require special algorithms for negative weights
- **Bellman-Ford** and **SPFA** handle negative weights effectively
- **Cycle detection** is crucial for avoiding infinite scores
- **Reachability checks** ensure cycles can actually reach destination
- **Graph algorithms** have many variations for different constraints

## Key Insights for Other Problems

### 1. **Longest Path Problems**
**Principle**: Convert longest path problems to shortest path problems by negating edge weights.
**Applicable to**:
- Longest path problems
- Graph algorithms
- Dynamic programming
- Algorithm design

**Example Problems**:
- Longest path problems
- Graph algorithms
- Dynamic programming
- Algorithm design

### 2. **Negative Cycle Detection**
**Principle**: Use appropriate algorithms to detect negative cycles in graphs.
**Applicable to**:
- Cycle detection
- Graph algorithms
- Network analysis
- Algorithm design

**Example Problems**:
- Cycle detection
- Graph algorithms
- Network analysis
- Algorithm design

### 3. **Reachability Analysis**
**Principle**: Analyze reachability to determine if cycles affect the target node.
**Applicable to**:
- Graph algorithms
- Network analysis
- Algorithm design
- Problem solving

**Example Problems**:
- Graph algorithms
- Network analysis
- Algorithm design
- Problem solving

### 4. **Algorithm Selection for Negative Weights**
**Principle**: Choose appropriate algorithms when dealing with negative edge weights.
**Applicable to**:
- Graph algorithms
- Algorithm selection
- Problem solving
- System design

**Example Problems**:
- Graph algorithms
- Algorithm selection
- Problem solving
- System design

## Notable Techniques

### 1. **SPFA Pattern**
```python
def spfa(graph, start, n):
    distances = [float('-inf')] * n
    distances[start] = 0
    queue = deque([start])
    in_queue = [False] * n
    in_queue[start] = True
    visit_count = [0] * n
    
    while queue:
        node = queue.popleft()
        in_queue[node] = False
        
        for neighbor, weight in graph[node]:
            new_dist = distances[node] + weight
            if new_dist > distances[neighbor]:
                distances[neighbor] = new_dist
                visit_count[neighbor] += 1
                
                if visit_count[neighbor] >= n:
                    return float('inf')  # Cycle detected
                
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True
    
    return distances
```

### 2. **Bellman-Ford Pattern**
```python
def bellman_ford(edges, n, start):
    distances = [float('-inf')] * n
    distances[start] = 0
    
    # Relax edges n-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if distances[u] != float('-inf'):
                distances[v] = max(distances[v], distances[u] + w)
    
    # Check for cycles
    for u, v, w in edges:
        if distances[u] != float('-inf'):
            if distances[u] + w > distances[v]:
                return float('inf')  # Cycle detected
    
    return distances
```

### 3. **Cycle Detection Pattern**
```python
def detect_cycle_reachability(graph, start, target, n):
    visit_count = [0] * n
    
    def dfs(node):
        visit_count[node] += 1
        if visit_count[node] >= n:
            return can_reach_target(node, target)
        
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        return False
    
    return dfs(start)
```

## Edge Cases to Remember

1. **Positive cycles**: Return -1 if a positive cycle can reach the target
2. **No path exists**: Return -1 if no path exists
3. **Negative weights**: Handle properly with appropriate algorithms
4. **Self-loops**: Handle properly
5. **Multiple edges**: Consider maximum weight

## Problem-Solving Framework

1. **Identify longest path nature**: This is a longest path problem with negative weights
2. **Choose algorithm**: Use SPFA or Bellman-Ford for negative weights
3. **Handle cycles**: Detect positive cycles that can reach the target
4. **Check reachability**: Ensure cycles can actually reach the target node
5. **Format output**: Return appropriate result based on findings

---

*This analysis shows how to efficiently solve longest path problems with negative weights and cycle detection.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: High Score with Costs**
**Problem**: Each edge has an additional cost, find maximum score with minimum total cost.
```python
def cost_based_high_score(n, m, flights, costs):
    # costs[(a, b)] = additional cost for flight (a, b)
    
    # Build adjacency list with costs
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        additional_cost = costs.get((a, b), 0)
        graph[a].append((b, c, additional_cost))
    
    # SPFA with cost tracking
    distances = [float('-inf')] * (n + 1)
    total_costs = [float('inf')] * (n + 1)
    distances[1] = 0
    total_costs[1] = 0
    
    queue = deque([1])
    in_queue = [False] * (n + 1)
    in_queue[1] = True
    visit_count = [0] * (n + 1)
    
    while queue:
        node = queue.popleft()
        in_queue[node] = False
        
        for neighbor, weight, cost in graph[node]:
            new_dist = distances[node] + weight
            new_cost = total_costs[node] + cost
            
            if new_dist > distances[neighbor] or (new_dist == distances[neighbor] and new_cost < total_costs[neighbor]):
                distances[neighbor] = new_dist
                total_costs[neighbor] = new_cost
                visit_count[neighbor] += 1
                
                if visit_count[neighbor] >= n:
                    if can_reach_target(neighbor, n, graph):
                        return float('inf'), float('inf')
                
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True
    
    return distances[n], total_costs[n]
```

#### **Variation 2: High Score with Constraints**
**Problem**: Find maximum score with constraints on path length or node visits.
```python
def constrained_high_score(n, m, flights, constraints):
    # constraints = {'max_length': x, 'max_visits': y, 'min_score': z}
    
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        graph[a].append((b, c))
    
    # SPFA with constraints
    distances = [float('-inf')] * (n + 1)
    path_lengths = [0] * (n + 1)
    visit_counts = [0] * (n + 1)
    distances[1] = 0
    
    queue = deque([1])
    in_queue = [False] * (n + 1)
    in_queue[1] = True
    cycle_count = [0] * (n + 1)
    
    while queue:
        node = queue.popleft()
        in_queue[node] = False
        
        for neighbor, weight in graph[node]:
            new_dist = distances[node] + weight
            new_length = path_lengths[node] + 1
            new_visits = visit_counts[node] + 1
            
            # Apply constraints
            if 'max_length' in constraints and new_length > constraints['max_length']:
                continue
            if 'max_visits' in constraints and new_visits > constraints['max_visits']:
                continue
            if 'min_score' in constraints and new_dist < constraints['min_score']:
                continue
            
            if new_dist > distances[neighbor]:
                distances[neighbor] = new_dist
                path_lengths[neighbor] = new_length
                visit_counts[neighbor] = new_visits
                cycle_count[neighbor] += 1
                
                if cycle_count[neighbor] >= n:
                    if can_reach_target(neighbor, n, graph):
                        return float('inf')
                
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True
    
    return distances[n] if distances[n] != float('-inf') else -1
```

#### **Variation 3: High Score with Probabilities**
**Problem**: Each flight has a probability of success, find expected maximum score.
```python
def probabilistic_high_score(n, m, flights, probabilities):
    # probabilities[(a, b)] = probability that flight (a, b) succeeds
    
    # Build adjacency list with probabilities
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        prob = probabilities.get((a, b), 1.0)
        graph[a].append((b, c, prob))
    
    # Use Monte Carlo simulation
    import random
    
    def simulate_high_score():
        # Randomly sample flights based on probabilities
        sampled_flights = []
        for a, b, c in flights:
            if random.random() < probabilities.get((a, b), 1.0):
                sampled_flights.append((a, b, c))
        
        # Build graph for sampled flights
        sampled_graph = [[] for _ in range(n + 1)]
        for a, b, c in sampled_flights:
            sampled_graph[a].append((b, c))
        
        # SPFA on sampled graph
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        
        queue = deque([1])
        in_queue = [False] * (n + 1)
        in_queue[1] = True
        visit_count = [0] * (n + 1)
        
        while queue:
            node = queue.popleft()
            in_queue[node] = False
            
            for neighbor, weight in sampled_graph[node]:
                new_dist = distances[node] + weight
                if new_dist > distances[neighbor]:
                    distances[neighbor] = new_dist
                    visit_count[neighbor] += 1
                    
                    if visit_count[neighbor] >= n:
                        if can_reach_target(neighbor, n, sampled_graph):
                            return float('inf')
                    
                    if not in_queue[neighbor]:
                        queue.append(neighbor)
                        in_queue[neighbor] = True
        
        return distances[n]
    
    # Run multiple simulations
    num_simulations = 1000
    total_score = 0
    infinite_count = 0
    
    for _ in range(num_simulations):
        score = simulate_high_score()
        if score == float('inf'):
            infinite_count += 1
        else:
            total_score += score
    
    expected_score = total_score / num_simulations
    infinite_probability = infinite_count / num_simulations
    
    return expected_score, infinite_probability
```

#### **Variation 4: High Score with Multiple Criteria**
**Problem**: Find maximum score considering multiple criteria (score, time, cost).
```python
def multi_criteria_high_score(n, m, flights, criteria):
    # criteria = {'score_weight': x, 'time_weight': y, 'cost_weight': z}
    
    # Build adjacency list with multiple attributes
    graph = [[] for _ in range(n + 1)]
    for a, b, c in flights:
        # Assume each flight has time and cost attributes
        time = criteria.get('time', {}).get((a, b), 1)
        cost = criteria.get('cost', {}).get((a, b), 0)
        graph[a].append((b, c, time, cost))
    
    # SPFA with multi-criteria tracking
    distances = [float('-inf')] * (n + 1)
    total_times = [0] * (n + 1)
    total_costs = [0] * (n + 1)
    distances[1] = 0
    
    queue = deque([1])
    in_queue = [False] * (n + 1)
    in_queue[1] = True
    visit_count = [0] * (n + 1)
    
    best_score = float('-inf')
    best_criteria_score = float('-inf')
    
    while queue:
        node = queue.popleft()
        in_queue[node] = False
        
        for neighbor, weight, time, cost in graph[node]:
            new_dist = distances[node] + weight
            new_time = total_times[node] + time
            new_cost = total_costs[node] + cost
            
            if new_dist > distances[neighbor]:
                distances[neighbor] = new_dist
                total_times[neighbor] = new_time
                total_costs[neighbor] = new_cost
                visit_count[neighbor] += 1
                
                if visit_count[neighbor] >= n:
                    if can_reach_target(neighbor, n, graph):
                        return float('inf')
                
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True
                
                # Calculate multi-criteria score
                if neighbor == n:
                    criteria_score = (new_dist * criteria.get('score_weight', 1) + 
                                    new_time * criteria.get('time_weight', 1) + 
                                    new_cost * criteria.get('cost_weight', 1))
                    if criteria_score > best_criteria_score:
                        best_criteria_score = criteria_score
                        best_score = new_dist
    
    return best_score, best_criteria_score
```

#### **Variation 5: High Score with Dynamic Updates**
**Problem**: Handle dynamic updates to flight scores and find maximum score after each update.
```python
def dynamic_high_score(n, m, initial_flights, updates):
    # updates = [(flight_index, new_score), ...]
    
    flights = initial_flights.copy()
    results = []
    
    for flight_index, new_score in updates:
        # Update flight score
        a, b, old_score = flights[flight_index]
        flights[flight_index] = (a, b, new_score)
        
        # Rebuild graph
        graph = [[] for _ in range(n + 1)]
        for a, b, c in flights:
            graph[a].append((b, c))
        
        # SPFA
        distances = [float('-inf')] * (n + 1)
        distances[1] = 0
        
        queue = deque([1])
        in_queue = [False] * (n + 1)
        in_queue[1] = True
        visit_count = [0] * (n + 1)
        
        while queue:
            node = queue.popleft()
            in_queue[node] = False
            
            for neighbor, weight in graph[node]:
                new_dist = distances[node] + weight
                if new_dist > distances[neighbor]:
                    distances[neighbor] = new_dist
                    visit_count[neighbor] += 1
                    
                    if visit_count[neighbor] >= n:
                        if can_reach_target(neighbor, n, graph):
                            results.append(float('inf'))
                            break
                    
                    if not in_queue[neighbor]:
                        queue.append(neighbor)
                        in_queue[neighbor] = True
            else:
                continue
            break
        else:
            results.append(distances[n] if distances[n] != float('-inf') else -1)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Longest Path Problems**
- **Longest Path in DAG**: Find longest path in directed acyclic graphs
- **Longest Path with Cycles**: Handle cycles in longest path problems
- **Longest Path with Constraints**: Add constraints to longest path problems
- **Longest Path Optimization**: Optimize longest path algorithms

#### **2. Graph Optimization Problems**
- **Path Optimization**: Optimize paths in graphs
- **Score Optimization**: Optimize scores in graph problems
- **Multi-Criteria Optimization**: Optimize multiple objectives
- **Dynamic Optimization**: Handle dynamic graph changes

#### **3. Algorithmic Techniques**
- **SPFA Algorithm**: Shortest Path Faster Algorithm
- **Bellman-Ford**: Algorithm for shortest/longest paths
- **Cycle Detection**: Detect cycles in graphs
- **Reachability Analysis**: Analyze reachability in graphs

#### **4. Constraint Problems**
- **Path Constraints**: Constraints on path properties
- **Score Constraints**: Constraints on score values
- **Time Constraints**: Time-based constraints
- **Resource Constraints**: Resource-based constraints

#### **5. Mathematical Concepts**
- **Graph Theory**: Properties of graphs and paths
- **Optimization Theory**: Mathematical optimization techniques
- **Probability Theory**: Probability theory in graphs
- **Algorithm Analysis**: Analysis of graph algorithms

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    flights = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        flights.append((a, b, c))
    
    result = find_high_score(n, m, flights)
    print(result)
```

#### **2. Range Queries on Flight Scores**
```python
def range_flight_score_queries(n, flights, queries):
    # queries = [(start_node, end_node), ...] - find max score in range
    
    results = []
    for start, end in queries:
        # Filter flights in range
        range_flights = [(a, b, c) for a, b, c in flights if start <= a <= end and start <= b <= end]
        
        result = find_high_score(end - start + 1, len(range_flights), range_flights)
        results.append(result)
    
    return results
```

#### **3. Interactive High Score Problems**
```python
def interactive_high_score():
    n = int(input("Enter number of cities: "))
    m = int(input("Enter number of flights: "))
    print("Enter flights (from to score):")
    flights = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        flights.append((a, b, c))
    
    result = find_high_score(n, m, flights)
    print(f"Maximum score: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Longest Path Theory**: Mathematical theory of longest paths
- **Path Optimization**: Mathematical path optimization
- **Graph Algorithms**: Mathematical analysis of graph algorithms
- **Path Analysis**: Analysis of path-based algorithms

#### **2. Optimization Theory**
- **Score Optimization**: Mathematical score optimization
- **Path Optimization**: Mathematical path optimization
- **Multi-Criteria Optimization**: Mathematical multi-criteria optimization
- **Dynamic Optimization**: Mathematical dynamic optimization

#### **3. Probability Theory**
- **Probabilistic Paths**: Probability theory applied to paths
- **Expected Values**: Expected score calculations
- **Probability Distributions**: Probability distributions in graphs
- **Stochastic Optimization**: Stochastic optimization techniques

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **SPFA Algorithm**: Efficient longest path algorithm
- **Bellman-Ford Algorithm**: Algorithm for longest paths
- **Cycle Detection**: Cycle detection algorithms
- **Graph Algorithms**: Various graph algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Optimization Theory**: Mathematical optimization techniques
- **Probability Theory**: Mathematical probability theory
- **Algorithm Analysis**: Analysis of algorithm complexity

#### **3. Programming Concepts**
- **Graph Representations**: Efficient graph representations
- **Queue Data Structures**: Queue implementations
- **Algorithm Optimization**: Improving algorithm performance
- **Dynamic Programming**: Handling dynamic updates

---

*This analysis demonstrates efficient longest path techniques and shows various extensions for high score problems.* 