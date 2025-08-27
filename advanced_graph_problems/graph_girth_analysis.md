# CSES Graph Girth - Problem Analysis

## Problem Statement
Given an undirected graph with n nodes and m edges, find the length of the shortest cycle in the graph (the girth). If the graph has no cycles, output -1.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print the length of the shortest cycle in the graph, or -1 if there are no cycles.

### Constraints
- 1 ≤ n ≤ 2500
- 1 ≤ m ≤ 5000
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 6
1 2
2 3
3 4
4 5
5 1
2 4

Output:
3
```

## Solution Progression

### Approach 1: BFS from Each Node - O(n²(n + m))
**Description**: For each node, run BFS to find the shortest cycle starting from that node.

```python
def graph_girth_naive(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try each node as starting point
    for start in range(1, n + 1):
        # BFS to find shortest cycle from start
        queue = [(start, -1, 0)]  # (node, parent, distance)
        visited = {start}
        
        while queue:
            node, parent, dist = queue.pop(0)
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor == start and dist >= 2:
                    # Found a cycle back to start
                    min_cycle = min(min_cycle, dist + 1)
                    break
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this is inefficient**: This approach has O(n²(n + m)) complexity and doesn't efficiently find the shortest cycle.

### Improvement 1: BFS with Distance Tracking - O(n(n + m))
**Description**: Use BFS with better distance tracking to find shortest cycles.

```python
def graph_girth_improved(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # Try each node as starting point
    for start in range(1, n + 1):
        # BFS with distance tracking
        queue = [(start, -1, 0)]  # (node, parent, distance)
        distance = {start: 0}
        
        while queue:
            node, parent, dist = queue.pop(0)
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                
                if neighbor in distance:
                    # Found a cycle
                    cycle_length = distance[node] + distance[neighbor] + 1
                    if cycle_length >= 3:  # Valid cycle
                        min_cycle = min(min_cycle, cycle_length)
                else:
                    distance[neighbor] = dist + 1
                    queue.append((neighbor, node, dist + 1))
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this improvement works**: Better distance tracking allows finding cycles more efficiently.

### Approach 2: Floyd-Warshall for All-Pairs Shortest Paths - O(n³)
**Description**: Use Floyd-Warshall to find all-pairs shortest paths, then find the minimum cycle.

```python
def graph_girth_floyd_warshall(n, m, edges):
    # Initialize distance matrix
    dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    
    # Add edges
    for a, b in edges:
        dist[a][b] = 1
        dist[b][a] = 1
    
    # Floyd-Warshall
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Find minimum cycle
    min_cycle = float('inf')
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if dist[i][j] != float('inf'):
                # Check if there's a direct edge between i and j
                for a, b in edges:
                    if (a == i and b == j) or (a == j and b == i):
                        cycle_length = dist[i][j] + 1
                        min_cycle = min(min_cycle, cycle_length)
                        break
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this is inefficient**: O(n³) complexity is too slow for the given constraints.

### Approach 3: BFS with Edge Removal - O(nm)
**Description**: For each edge, remove it and find shortest path between its endpoints.

```python
def graph_girth_optimal(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # For each edge, find shortest path between its endpoints
    for a, b in edges:
        # Remove edge (a,b) temporarily
        adj[a].remove(b)
        adj[b].remove(a)
        
        # BFS to find shortest path from a to b
        queue = [(a, 0)]
        visited = {a}
        
        while queue:
            node, dist = queue.pop(0)
            
            if node == b:
                # Found path from a to b
                cycle_length = dist + 1
                min_cycle = min(min_cycle, cycle_length)
                break
            
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
    
    return min_cycle if min_cycle != float('inf') else -1
```

**Why this improvement works**: This approach finds the shortest cycle by considering each edge and finding the shortest path between its endpoints.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_graph_girth(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # For each edge, find shortest path between its endpoints
    for a, b in edges:
        # Remove edge (a,b) temporarily
        adj[a].remove(b)
        adj[b].remove(a)
        
        # BFS to find shortest path from a to b
        queue = [(a, 0)]
        visited = {a}
        found_path = False
        
        while queue and not found_path:
            node, dist = queue.pop(0)
            
            if node == b:
                # Found path from a to b
                cycle_length = dist + 1
                min_cycle = min(min_cycle, cycle_length)
                found_path = True
                break
            
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
    
    return min_cycle if min_cycle != float('inf') else -1

result = find_graph_girth(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS from Each Node | O(n²(n + m)) | O(n) | Simple but inefficient cycle detection |
| BFS with Distance Tracking | O(n(n + m)) | O(n) | Better distance tracking |
| Floyd-Warshall | O(n³) | O(n²) | All-pairs shortest paths |
| BFS with Edge Removal | O(nm) | O(n) | Optimal approach for girth |

## Key Insights for Other Problems

### 1. **Girth Detection with Edge Removal**
**Principle**: The shortest cycle containing an edge (a,b) is the shortest path from a to b plus the edge itself.
**Applicable to**: Cycle detection problems, graph analysis problems, shortest path problems

### 2. **BFS for Unweighted Shortest Paths**
**Principle**: BFS finds the shortest path in unweighted graphs efficiently.
**Applicable to**: Unweighted graph problems, shortest path problems, connectivity problems

### 3. **Cycle Length Calculation**
**Principle**: A cycle's length is the sum of the shortest path between two nodes plus the direct edge between them.
**Applicable to**: Cycle analysis problems, graph theory problems, path problems

## Notable Techniques

### 1. **Edge Removal and Restoration**
```python
def find_cycle_with_edge_removal(adj, edge):
    a, b = edge
    # Remove edge temporarily
    adj[a].remove(b)
    adj[b].remove(a)
    
    # Find shortest path
    shortest_path = bfs_shortest_path(adj, a, b)
    
    # Restore edge
    adj[a].append(b)
    adj[b].append(a)
    
    return shortest_path + 1 if shortest_path != -1 else float('inf')
```

### 2. **BFS for Shortest Path**
```python
def bfs_shortest_path(adj, start, end):
    queue = [(start, 0)]
    visited = {start}
    
    while queue:
        node, dist = queue.pop(0)
        
        if node == end:
            return dist
        
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # No path found
```

### 3. **Minimum Cycle Detection**
```python
def find_minimum_cycle(n, edges):
    adj = build_adjacency_list(n, edges)
    min_cycle = float('inf')
    
    for edge in edges:
        cycle_length = find_cycle_with_edge_removal(adj, edge)
        min_cycle = min(min_cycle, cycle_length)
    
    return min_cycle if min_cycle != float('inf') else -1
```

### 4. **Graph Girth Algorithm**
```python
def graph_girth_algorithm(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    min_cycle = float('inf')
    
    # For each edge, find shortest path between endpoints
    for a, b in edges:
        # Remove edge temporarily
        adj[a].remove(b)
        adj[b].remove(a)
        
        # Find shortest path
        path_length = bfs_shortest_path(adj, a, b)
        if path_length != -1:
            min_cycle = min(min_cycle, path_length + 1)
        
        # Restore edge
        adj[a].append(b)
        adj[b].append(a)
    
    return min_cycle if min_cycle != float('inf') else -1
```

## Problem-Solving Framework

1. **Identify problem type**: This is a graph girth (shortest cycle) problem
2. **Choose approach**: Use BFS with edge removal technique
3. **Initialize data structure**: Build adjacency list representation
4. **Iterate through edges**: For each edge, temporarily remove it
5. **Find shortest path**: Use BFS to find shortest path between edge endpoints
6. **Calculate cycle length**: Add 1 to path length to include the removed edge
7. **Track minimum**: Keep track of the minimum cycle length found
8. **Return result**: Return minimum cycle length or -1 if no cycles exist

---

*This analysis shows how to efficiently find the girth (shortest cycle) of an undirected graph using BFS with edge removal technique.* 