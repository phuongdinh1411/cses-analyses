# CSES High Score - Problem Analysis

## Problem Statement
There are n cities and m flight connections. Your task is to find the highest possible score for a route from city 1 to city n.

### Input
The first input line has two integers n and m: the number of cities and flight connections. The cities are numbered 1,2,…,n.
Then, there are m lines describing the flight connections. Each line has three integers a, b, and c: there is a flight from city a to city b with score c.

### Output
Print one integer: the highest possible score for a route from city 1 to city n. If there is no route, print -1.

### Constraints
- 1 ≤ n ≤ 2500
- 1 ≤ m ≤ 5000
- 1 ≤ a,b ≤ n
- -10^9 ≤ c ≤ 10^9

### Example
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

## Solution Progression

### Approach 1: Bellman-Ford with Negative Cycle Detection - O(n*m)
**Description**: Use Bellman-Ford algorithm to find the longest path, handling negative cycles.

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

### Improvement 2: SPFA with Negative Cycle Detection - O(n*m)
**Description**: Use SPFA (Shortest Path Faster Algorithm) for better performance.

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

## Final Optimal Solution

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

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bellman-Ford | O(n*m) | O(n) | Handles negative weights |
| Optimized Bellman-Ford | O(n*m) | O(n) | Early termination |
| SPFA | O(n*m) | O(n + m) | Often faster in practice |
| DFS | O(n*m) | O(n) | Educational approach |

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