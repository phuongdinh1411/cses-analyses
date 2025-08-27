# CSES Cycle Finding - Problem Analysis

## Problem Statement
Given a directed graph with n nodes and m edges, find a negative cycle if it exists. If there is no negative cycle, print "NO". Otherwise, print "YES" and the nodes in the cycle.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has three integers a, b, and c: there is an edge from node a to node b with weight c.

### Output
If there is no negative cycle, print "NO". Otherwise, print "YES" and the nodes in the cycle.

### Constraints
- 1 ≤ n ≤ 2500
- 1 ≤ m ≤ 5000
- 1 ≤ a,b ≤ n
- -10^9 ≤ c ≤ 10^9

### Example
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

## Solution Progression

### Approach 1: Bellman-Ford with Cycle Detection - O(n*m)
**Description**: Use Bellman-Ford algorithm to detect negative cycles.

```python
def cycle_finding_naive(n, m, edges):
    # Initialize distances
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

**Why this is inefficient**: We need to reconstruct the cycle path, which can be complex.

### Improvement 1: Bellman-Ford with Path Reconstruction - O(n*m)
**Description**: Use Bellman-Ford with improved cycle reconstruction.

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
            
            # Reverse to get correct order
            cycle_nodes.reverse()
            return True, cycle_nodes
    
    return False, None
```

**Why this improvement works**: We use Bellman-Ford algorithm to detect negative cycles and then reconstruct the cycle path using the parent array.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b, c = map(int, input().split())
    edges.append((a, b, c))

def find_negative_cycle(n, m, edges):
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
            
            # Reverse to get correct order
            cycle_nodes.reverse()
            return True, cycle_nodes
    
    return False, None

has_cycle, cycle = find_negative_cycle(n, m, edges)

if has_cycle:
    print("YES")
    print(*cycle)
else:
    print("NO")
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Bellman-Ford | O(n*m) | O(n) | Use Bellman-Ford for negative cycle detection |
| Path Reconstruction | O(n*m) | O(n) | Reconstruct cycle using parent array |

## Key Insights for Other Problems

### 1. **Negative Cycle Detection**
**Principle**: Use Bellman-Ford algorithm to detect negative cycles in directed graphs.
**Applicable to**: Graph problems, cycle problems, shortest path problems

### 2. **Bellman-Ford Algorithm**
**Principle**: Use Bellman-Ford to find shortest paths and detect negative cycles.
**Applicable to**: Shortest path problems, cycle detection problems, graph problems

### 3. **Cycle Reconstruction**
**Principle**: Reconstruct cycles using parent array after detecting negative cycles.
**Applicable to**: Cycle problems, path reconstruction problems, graph problems

## Notable Techniques

### 1. **Bellman-Ford Implementation**
```python
def bellman_ford(n, edges, start):
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    dist[start] = 0
    
    for i in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    
    return dist, parent
```

### 2. **Negative Cycle Detection**
```python
def detect_negative_cycle(edges, dist):
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return True, u, v
    return False, None, None
```

### 3. **Cycle Reconstruction**
```python
def reconstruct_cycle(parent, start, end):
    cycle = []
    current = end
    visited = set()
    
    while current not in visited:
        visited.add(current)
        cycle.append(current)
        current = parent[current]
    
    # Find cycle start and reconstruct
    cycle_start = current
    cycle_nodes = []
    current = end
    while current != cycle_start:
        cycle_nodes.append(current)
        current = parent[current]
    cycle_nodes.append(cycle_start)
    
    return cycle_nodes[::-1]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a negative cycle detection problem
2. **Choose approach**: Use Bellman-Ford algorithm
3. **Initialize**: Set up distance and parent arrays
4. **Run Bellman-Ford**: Perform n-1 iterations of edge relaxation
5. **Detect negative cycle**: Check if any edge can still be relaxed
6. **Reconstruct cycle**: Use parent array to find the cycle path
7. **Return result**: Output cycle if found, "NO" otherwise

---

*This analysis shows how to efficiently detect negative cycles using Bellman-Ford algorithm with cycle reconstruction.* 