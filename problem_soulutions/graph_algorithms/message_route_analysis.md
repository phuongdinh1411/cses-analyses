---
layout: simple
title: "Message Route
permalink: /problem_soulutions/graph_algorithms/message_route_analysis/"
---


# Message Route

## Problem Statement
There are n computers numbered 1,2,…,n. The computers are connected through m cables. Your task is to find a route from computer 1 to computer n.

### Input
The first input line has two integers n and m: the number of computers and cables. The computers are numbered 1,2,…,n.
Then, there are m lines describing the cables. Each line has two integers a and b: there is a cable between computers a and b.

### Output"
Print "IMPOSSIBLE" if there is no route, and otherwise print the number of computers on the route and the route itself.

### Constraints
- 2 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5

### Example
```
Input:
5 5
1 2
1 3
1 4
2 3
5 4

Output:
3
1 4 5
```

## Solution Progression

### Approach 1: BFS with Path Tracking - O(n + m)
**Description**: Use breadth-first search to find the shortest path and track the path.

```python
from collections import deque

def message_route_bfs(n, m, cables):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def bfs():
        queue = deque([(1, [1])])  # (node, path)
        visited = [False] * (n + 1)
        visited[1] = True
        
        while queue:
            node, path = queue.popleft()
            
            if node == n:
                return path
            
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return None  # No path found
    
    path = bfs()
    if path is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(path)}\n{' '.join(map(str, path))}"
```

**Why this is efficient**: BFS guarantees finding the shortest path, and we visit each node at most once.

### Improvement 1: BFS with Parent Tracking - O(n + m)
**Description**: Use BFS with parent tracking to reconstruct the path more efficiently.

```python
from collections import deque

def message_route_bfs_parent(n, m, cables):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def bfs():
        queue = deque([1])
        visited = [False] * (n + 1)
        parent = [-1] * (n + 1)
        visited[1] = True
        
        while queue:
            node = queue.popleft()
            
            if node == n:
                # Reconstruct path
                path = []
                current = n
                while current != -1:
                    path.append(current)
                    current = parent[current]
                return path[::-1]  # Reverse to get correct order
            
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    parent[neighbor] = node
                    queue.append(neighbor)
        
        return None  # No path found
    
    path = bfs()
    if path is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(path)}\n{' '.join(map(str, path))}"
```

**Why this improvement works**: Parent tracking is more memory-efficient than storing entire paths in the queue.

### Improvement 2: DFS with Path Tracking - O(n + m)
**Description**: Use depth-first search with path tracking for alternative approach.

```python
def message_route_dfs(n, m, cables):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def dfs(node, path, visited):
        if node == n:
            return path
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                result = dfs(neighbor, path + [neighbor], visited)
                if result is not None:
                    return result
                visited[neighbor] = False  # Backtrack
        
        return None
    
    visited = [False] * (n + 1)
    visited[1] = True
    path = dfs(1, [1], visited)
    
    if path is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(path)}\n{' '.join(map(str, path))}"
```

**Why this improvement works**: DFS can find a path (though not necessarily the shortest) and uses less memory than BFS.

### Alternative: Bidirectional BFS - O(n + m)
**Description**: Use bidirectional BFS for potentially faster path finding.

```python
from collections import deque

def message_route_bidirectional_bfs(n, m, cables):
    # Build adjacency list
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    def bidirectional_bfs():
        if n == 1:
            return [1]
        
        # Forward BFS from start
        forward_queue = deque([1])
        forward_visited = {1: 0}  # node: distance
        forward_parent = {1: -1}
        
        # Backward BFS from end
        backward_queue = deque([n])
        backward_visited = {n: 0}  # node: distance
        backward_parent = {n: -1}
        
        while forward_queue and backward_queue:
            # Forward step
            if len(forward_queue) <= len(backward_queue):
                current = forward_queue.popleft()
                if current in backward_visited:
                    # Path found, reconstruct
                    return reconstruct_path(current, forward_parent, backward_parent)
                
                for neighbor in graph[current]:
                    if neighbor not in forward_visited:
                        forward_visited[neighbor] = forward_visited[current] + 1
                        forward_parent[neighbor] = current
                        forward_queue.append(neighbor)
            
            # Backward step
            else:
                current = backward_queue.popleft()
                if current in forward_visited:
                    # Path found, reconstruct
                    return reconstruct_path(current, forward_parent, backward_parent)
                
                for neighbor in graph[current]:
                    if neighbor not in backward_visited:
                        backward_visited[neighbor] = backward_visited[current] + 1
                        backward_parent[neighbor] = current
                        backward_queue.append(neighbor)
        
        return None
    
    def reconstruct_path(meeting_node, forward_parent, backward_parent):
        # Reconstruct forward path
        forward_path = []
        current = meeting_node
        while current != -1:
            forward_path.append(current)
            current = forward_parent[current]
        forward_path = forward_path[::-1]
        
        # Reconstruct backward path
        backward_path = []
        current = backward_parent[meeting_node]
        while current != -1:
            backward_path.append(current)
            current = backward_parent[current]
        
        return forward_path + backward_path
    
    path = bidirectional_bfs()
    if path is None:
        return "IMPOSSIBLE"
    else:
        return f"{len(path)}\n{' '.join(map(str, path))}"
```

**Why this works**: Bidirectional BFS can be faster than unidirectional BFS, especially when the path is long.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
cables = [tuple(map(int, input().split())) for _ in range(m)]

# Build adjacency list
graph = [[] for _ in range(n + 1)]
for a, b in cables:
    graph[a].append(b)
    graph[b].append(a)

def bfs():
    queue = deque([1])
    visited = [False] * (n + 1)
    parent = [-1] * (n + 1)
    visited[1] = True
    
    while queue:
        node = queue.popleft()
        
        if node == n:
            # Reconstruct path
            path = []
            current = n
            while current != -1:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse to get correct order
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = node
                queue.append(neighbor)
    
    return None  # No path found

path = bfs()
if path is None:
    print("IMPOSSIBLE")
else:
    print(len(path))
    print(*path)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| BFS with Path Tracking | O(n + m) | O(n + m) | Store paths in queue |
| BFS with Parent Tracking | O(n + m) | O(n) | Reconstruct path |
| DFS | O(n + m) | O(n) | Find any path |
| Bidirectional BFS | O(n + m) | O(n) | Faster for long paths |

## Key Insights for Other Problems

### 1. **Shortest Path in Unweighted Graphs**
**Principle**: Use BFS to find the shortest path in unweighted graphs.
**Applicable to**:
- Shortest path problems
- Unweighted graphs
- Path finding
- Graph algorithms

**Example Problems**:
- Shortest path
- Unweighted graphs
- Path finding
- Graph algorithms

### 2. **Path Reconstruction**
**Principle**: Use parent tracking to efficiently reconstruct paths from graph traversal.
**Applicable to**:
- Path finding
- Graph traversal
- Algorithm design
- Memory optimization

**Example Problems**:
- Path finding
- Graph traversal
- Algorithm design
- Memory optimization

### 3. **Bidirectional Search**
**Principle**: Use bidirectional search to potentially reduce search space and improve performance.
**Applicable to**:
- Search algorithms
- Path finding
- Performance optimization
- Algorithm design

**Example Problems**:
- Search algorithms
- Path finding
- Performance optimization
- Algorithm design

### 4. **Graph Connectivity**
**Principle**: Check for connectivity between source and destination nodes.
**Applicable to**:
- Connectivity problems
- Graph analysis
- Network problems
- Algorithm design

**Example Problems**:
- Connectivity problems
- Graph analysis
- Network problems
- Algorithm design

## Notable Techniques

### 1. **BFS with Parent Tracking**
```python
def bfs_with_parent(graph, start, end):
    queue = deque([start])
    visited = [False] * len(graph)
    parent = [-1] * len(graph)
    visited[start] = True
    
    while queue:
        node = queue.popleft()
        if node == end:
            return reconstruct_path(end, parent)
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = node
                queue.append(neighbor)
    return None
```

### 2. **Path Reconstruction**
```python
def reconstruct_path(end, parent):
    path = []
    current = end
    while current != -1:
        path.append(current)
        current = parent[current]
    return path[::-1]
```

### 3. **Bidirectional BFS Pattern**
```python
def bidirectional_bfs(graph, start, end):
    forward_queue = deque([start])
    backward_queue = deque([end])
    forward_visited = {start}
    backward_visited = {end}
    
    while forward_queue and backward_queue:
        # Alternate between forward and backward
        if len(forward_queue) <= len(backward_queue):
            # Forward step
            pass
        else:
            # Backward step
            pass
```

## Edge Cases to Remember

1. **No path exists**: Return "IMPOSSIBLE"
2. **Start equals end**: Return path with single node
3. **Single node graph**: Handle properly
4. **Large graph**: Use efficient algorithm
5. **Disconnected graph**: Check connectivity

## Problem-Solving Framework

1. **Identify path finding nature**: This is a shortest path problem in unweighted graph
2. **Choose algorithm**: Use BFS for shortest path
3. **Track path**: Use parent tracking for efficient reconstruction
4. **Check connectivity**: Ensure path exists
5. **Handle output format**: Print path length and nodes

---

*This analysis shows how to efficiently solve shortest path problems in unweighted graphs using BFS with path reconstruction.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Edges**
**Problem**: Each cable has a weight. Find the route with minimum total weight.
```python
def weighted_message_route(n, m, cables):
    # cables = [(a, b, weight), ...]
    graph = [[] for _ in range(n + 1)]
    for a, b, w in cables:
        graph[a].append((b, w))
        graph[b].append((a, w))
    
    # Use Dijkstra's algorithm
    import heapq
    pq = [(0, 1, [1])]  # (cost, node, path)
    visited = set()
    
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == n:
            return len(path), path
        
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                new_cost = cost + weight
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_cost, neighbor, new_path))
    
    return "IMPOSSIBLE"
```

#### **Variation 2: Multiple Destinations**
**Problem**: Find shortest path to any of k destination computers.
```python
def multi_destination_route(n, m, cables, destinations):
    # destinations = set of target nodes
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    queue = deque([(1, [1])])
    visited = set()
    
    while queue:
        node, path = queue.popleft()
        if node in destinations:
            return len(path), path
        
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
    
    return "IMPOSSIBLE"
```

#### **Variation 3: All Shortest Paths**
**Problem**: Find all shortest paths from computer 1 to computer n.
```python
def all_shortest_paths(n, m, cables):
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    # BFS to find shortest distance
    queue = deque([1])
    distance = [-1] * (n + 1)
    distance[1] = 0
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    
    if distance[n] == -1:
        return "IMPOSSIBLE"
    
    # DFS to find all paths with shortest distance
    def dfs(node, path, remaining):
        if node == n and remaining == 0:
            all_paths.append(path[:])
            return
        
        for neighbor in graph[node]:
            if distance[neighbor] == distance[node] + 1 and remaining > 0:
                dfs(neighbor, path + [neighbor], remaining - 1)
    
    all_paths = []
    dfs(1, [1], distance[n])
    return all_paths
```

#### **Variation 4: Path with Constraints**
**Problem**: Find a path that avoids certain computers and uses at most k cables.
```python
def constrained_route(n, m, cables, forbidden, max_cables):
    # forbidden = set of computers to avoid
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        if a not in forbidden and b not in forbidden:
            graph[a].append(b)
            graph[b].append(a)
    
    queue = deque([(1, [1], 0)])  # (node, path, cables_used)
    visited = set()
    
    while queue:
        node, path, cables_used = queue.popleft()
        if node == n:
            return len(path), path
        
        if cables_used >= max_cables:
            continue
        
        state = (node, cables_used)
        if state in visited:
            continue
        visited.add(state)
        
        for neighbor in graph[node]:
            if neighbor not in path:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path, cables_used + 1))
    
    return "IMPOSSIBLE"
```

#### **Variation 5: Dynamic Network**
**Problem**: Cables can be added/removed dynamically. Handle queries to find paths.
```python
class DynamicNetwork:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n + 1)]
    
    def add_cable(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)
    
    def remove_cable(self, a, b):
        self.graph[a] = [x for x in self.graph[a] if x != b]
        self.graph[b] = [x for x in self.graph[b] if x != a]
    
    def find_path(self):
        # Standard BFS
        queue = deque([(1, [1])])
        visited = set()
        
        while queue:
            node, path = queue.popleft()
            if node == self.n:
                return len(path), path
            
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return "IMPOSSIBLE"
```

### 🔗 **Related Problems & Concepts**

#### **1. Shortest Path Problems**
- **Dijkstra's Algorithm**: For weighted graphs
- **Bellman-Ford**: For graphs with negative weights
- **Floyd-Warshall**: For all-pairs shortest paths
- **A* Algorithm**: For heuristic-based pathfinding

#### **2. Graph Traversal Problems**
- **DFS vs BFS**: When to use each
- **Connected Components**: Find all reachable nodes
- **Cycle Detection**: Detect cycles in graphs
- **Topological Sort**: Order nodes in DAG

#### **3. Network Flow Problems**
- **Maximum Flow**: Find maximum flow between source and sink
- **Minimum Cut**: Find minimum capacity cut
- **Bipartite Matching**: Match nodes in bipartite graphs
- **Multi-commodity Flow**: Multiple source-sink pairs

#### **4. Graph Connectivity Problems**
- **Articulation Points**: Find critical nodes
- **Bridges**: Find critical edges
- **Strongly Connected Components**: Find SCCs in directed graphs
- **Biconnected Components**: Find biconnected components

#### **5. Path Problems**
- **Hamiltonian Path**: Visit each node exactly once
- **Eulerian Path**: Use each edge exactly once
- **Longest Path**: Find longest simple path
- **Path Counting**: Count number of paths

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Networks**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    cables = []
    for _ in range(m):
        a, b = map(int, input().split())
        cables.append((a, b))
    
    result = message_route_bfs(n, m, cables)
    print(result)
```

#### **2. Range Queries on Path Properties**
```python
# Precompute shortest distances for all pairs
def precompute_distances(n, m, cables):
    graph = [[] for _ in range(n + 1)]
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    
    distances = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        distances[i][i] = 0
        queue = deque([i])
        visited = set()
        
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor in graph[node]:
                if distances[i][neighbor] == float('inf'):
                    distances[i][neighbor] = distances[i][node] + 1
                    queue.append(neighbor)
    
    return distances

# Answer queries about path lengths
def path_query(distances, a, b):
    return distances[a][b] if distances[a][b] != float('inf') else -1
```

#### **3. Interactive Network Problems**
```python
# Interactive network exploration
def interactive_network():
    n, m = map(int, input().split())
    graph = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)
    
    current = 1
    path = [1]
    
    while current != n:
        print(f"Current node: {current}")
        print(f"Neighbors: {graph[current]}")
        
        next_node = int(input("Choose next node: "))
        if next_node in graph[current]:
            current = next_node
            path.append(current)
        else:
            print("Invalid choice!")
    
    print(f"Path found: {path}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory Concepts**
- **Graph Properties**: Planarity, bipartiteness, connectivity
- **Graph Invariants**: Chromatic number, clique number, independence number
- **Graph Decompositions**: Tree decomposition, path decomposition
- **Graph Algorithms**: Minimum spanning tree, maximum matching

#### **2. Network Analysis**
- **Centrality Measures**: Betweenness, closeness, eigenvector centrality
- **Community Detection**: Find communities in networks
- **Network Flow**: Analyze flow patterns and bottlenecks
- **Network Resilience**: Analyze network robustness

#### **3. Advanced Pathfinding**
- **Bidirectional Search**: Search from both ends
- **Contraction Hierarchies**: Preprocess for faster queries
- **Landmark-based Routing**: Use landmarks for approximation
- **Multi-level Routing**: Hierarchical pathfinding

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Graph Algorithms**: BFS, DFS, Dijkstra, Floyd-Warshall
- **Network Flow**: Ford-Fulkerson, Dinic's algorithm
- **Matching Algorithms**: Hungarian algorithm, Hopcroft-Karp
- **Connectivity Algorithms**: Tarjan's algorithm, Kosaraju's algorithm

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Linear Algebra**: Matrix representations of graphs
- **Combinatorics**: Counting paths and cycles
- **Optimization**: Linear programming for network problems

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Path Reconstruction**: Backtracking from target to source
- **State Management**: Tracking visited nodes and distances
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates fundamental graph traversal techniques and shows various extensions for pathfinding problems.* 