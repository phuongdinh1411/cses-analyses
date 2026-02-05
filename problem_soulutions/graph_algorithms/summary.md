---
layout: simple
title: "Graph Algorithms Summary"
permalink: /problem_soulutions/graph_algorithms/summary
---

# Graph Algorithms

Welcome to the Graph Algorithms section! This category covers fundamental and advanced algorithms for solving problems involving networks, paths, and connectivity.

## Key Concepts & Techniques

### Graph Representation

#### Adjacency List
- **When to use**: Sparse graphs, most common representation
- **Space**: O(V + E) where V is vertices, E is edges
- **Pros**: Space efficient, easy to iterate neighbors
- **Cons**: Slower edge existence check
- **Implementation**: Array of lists or vector of vectors

#### Adjacency Matrix
- **When to use**: Dense graphs, frequent edge queries
- **Space**: O(V²)
- **Pros**: Fast edge existence check, simple implementation
- **Cons**: Memory intensive for large sparse graphs
- **Implementation**: 2D array or vector of vectors

#### Edge List
- **When to use**: Simple representation, Kruskal's algorithm
- **Space**: O(E)
- **Pros**: Simple, good for edge-based algorithms
- **Cons**: Slow neighbor queries
- **Implementation**: List of (u, v, weight) tuples

#### Implicit Graphs
- **When to use**: Grid-based problems, game states
- **Space**: O(1) per state
- **Pros**: No explicit graph construction needed
- **Cons**: Neighbors computed on-the-fly
- **Implementation**: Function to generate neighbors

### Basic Graph Algorithms

#### Depth-First Search (DFS)
- **When to use**: Path finding, cycle detection, topological sort
- **Time**: O(V + E)
- **Space**: O(V) for recursion stack
- **Applications**: Connected components, maze solving, tree traversal
- **Implementation**: Recursive or iterative with stack

#### Breadth-First Search (BFS)
- **When to use**: Shortest path in unweighted graphs, level-order traversal
- **Time**: O(V + E)
- **Space**: O(V) for queue
- **Applications**: Shortest path, level-by-level processing
- **Implementation**: Queue-based iterative approach

#### Topological Sort
- **When to use**: DAG ordering, dependency resolution
- **Time**: O(V + E)
- **Space**: O(V)
- **Applications**: Course scheduling, build systems, dependency graphs
- **Implementation**: DFS with finish time or Kahn's algorithm

#### Connected Components
- **When to use**: Graph partitioning, network analysis
- **Time**: O(V + E)
- **Space**: O(V)
- **Applications**: Social networks, image segmentation
- **Implementation**: DFS or Union-Find

### Shortest Path Algorithms

#### Dijkstra's Algorithm
- **When to use**: Single-source shortest path in non-negative weighted graphs
- **Time**: O((V + E) log V) with priority queue
- **Space**: O(V)
- **Applications**: GPS navigation, network routing
- **Implementation**: Priority queue (min-heap)

#### Floyd-Warshall Algorithm
- **When to use**: All-pairs shortest paths, small dense graphs
- **Time**: O(V³)
- **Space**: O(V²)
- **Applications**: Distance matrices, transitive closure
- **Implementation**: Triple nested loop with dynamic programming

#### Bellman-Ford Algorithm
- **When to use**: Single-source shortest path with negative weights
- **Time**: O(VE)
- **Space**: O(V)
- **Applications**: Currency exchange, negative cycle detection
- **Implementation**: Relax all edges V-1 times

#### A* Algorithm
- **When to use**: Pathfinding with heuristic, game AI
- **Time**: O(b^d) where b is branching factor, d is depth
- **Space**: O(b^d)
- **Applications**: Game pathfinding, robotics
- **Implementation**: Priority queue with f(n) = g(n) + h(n)

### Advanced Graph Algorithms

#### Strongly Connected Components (SCC)
- **Kosaraju's Algorithm**: Two-pass DFS
  - *When to use*: General SCC detection
  - *Time*: O(V + E)
  - *Implementation*: DFS on original graph, then on transpose
- **Tarjan's Algorithm**: Single-pass DFS
  - *When to use*: When you need SCC during DFS
  - *Time*: O(V + E)
  - *Implementation*: DFS with low-link values

#### Minimum Spanning Tree (MST)
- **Kruskal's Algorithm**: Edge-based approach
  - *When to use*: Sparse graphs
  - *Time*: O(E log E)
  - *Implementation*: Sort edges, use Union-Find
- **Prim's Algorithm**: Vertex-based approach
  - *When to use*: Dense graphs
  - *Time*: O(E log V)
  - *Implementation*: Priority queue with vertices

#### Network Flow
- **Ford-Fulkerson**: Maximum flow
  - *When to use*: General max flow problems
  - *Time*: O(E × max_flow)
  - *Implementation*: DFS to find augmenting paths
- **Edmonds-Karp**: BFS-based max flow
  - *When to use*: When you need polynomial time guarantee
  - *Time*: O(VE²)
  - *Implementation*: BFS to find shortest augmenting paths
- **Dinic's Algorithm**: Layered network approach
  - *When to use*: High-performance max flow
  - *Time*: O(V²E)
  - *Implementation*: BFS to create layers, DFS with blocking flow

### Specialized Graph Algorithms

#### Bipartite Matching
- **Hungarian Algorithm**: Assignment problem
  - *When to use*: Maximum weight bipartite matching
  - *Time*: O(V³)
  - *Implementation*: Augmenting path with dual variables
- **Hopcroft-Karp**: Maximum cardinality matching
  - *When to use*: Unweighted bipartite matching
  - *Time*: O(E√V)
  - *Implementation*: BFS to find multiple augmenting paths

#### Eulerian Paths/Circuits
- **Hierholzer's Algorithm**: Find Eulerian circuit
  - *When to use*: When graph has Eulerian circuit
  - *Time*: O(E)
  - *Implementation*: DFS with edge removal
- **Fleury's Algorithm**: Find Eulerian path
  - *When to use*: When graph has Eulerian path
  - *Time*: O(E²)
  - *Implementation*: Choose edges carefully to maintain connectivity

#### Hamiltonian Paths/Cycles
- **Backtracking**: Find Hamiltonian cycle
  - *When to use*: Small graphs, exact solution needed
  - *Time*: O(V!)
  - *Implementation*: DFS with path tracking
- **Dynamic Programming**: TSP with bitmask
  - *When to use*: TSP with small number of cities
  - *Time*: O(V²2^V)
  - *Implementation*: DP with bitmask for visited cities

### Graph Optimization Techniques

#### Binary Lifting
- **When to use**: Fast ancestor queries in trees
- **Time**: O(log V) per query after O(V log V) preprocessing
- **Space**: O(V log V)
- **Applications**: LCA queries, k-th ancestor
- **Implementation**: Precompute 2^i-th ancestors for each node

#### Heavy-Light Decomposition
- **When to use**: Path queries and updates in trees
- **Time**: O(log² V) per query
- **Space**: O(V)
- **Applications**: Path sum, path maximum, path updates
- **Implementation**: Decompose tree into heavy chains, use segment trees

#### Centroid Decomposition
- **When to use**: Tree problems with divide-and-conquer
- **Time**: O(V log V) for decomposition
- **Space**: O(V)
- **Applications**: Tree distances, tree counting
- **Implementation**: Find centroid, solve recursively

#### Union-Find (Disjoint Set Union)
- **When to use**: Dynamic connectivity, MST algorithms
- **Time**: O(α(V)) per operation (almost constant)
- **Space**: O(V)
- **Applications**: Kruskal's MST, connected components
- **Implementation**: Path compression and union by rank

## Problem Categories

### Graph Traversal
- [Counting Rooms](counting_rooms_analysis) - Connected components in grid
- [Labyrinth](labyrinth_analysis) - Finding path in maze
- [Building Roads](building_roads_analysis) - Minimum connections needed
- [Message Route](message_route_analysis) - Shortest path in unweighted graph
- [Building Teams](building_teams_analysis) - Graph bicoloring

### Shortest Paths
- [Shortest Routes I](shortest_routes_i_analysis) - Dijkstra's algorithm
- [Shortest Routes II](shortest_routes_ii_analysis) - Floyd-Warshall algorithm
- [Flight Discount](flight_discount_analysis) - Modified shortest path
- [High Score](high_score_analysis) - Longest path with negative edges
- [Flight Routes](flight_routes_analysis) - K shortest paths

### Graph Cycles
- [Round Trip](round_trip_analysis) - Finding cycles
- [Monsters](monsters_analysis) - Multi-source shortest path
- [Cycle Finding](cycle_finding_analysis) - Negative cycle detection
- [Planets Cycles](planets_cycles_analysis) - Cycle detection in functional graph

### Strongly Connected Components
- [Planets and Kingdoms](planets_and_kingdoms_analysis) - Finding SCCs
- [Giant Pizza](giant_pizza_analysis) - 2-SAT problem
- [Strongly Connected Components](strongly_connected_components_analysis) - Kosaraju's algorithm

### Flow Networks
- [Mail Delivery](mail_delivery_analysis) - Eulerian circuit
- [Police Chase](police_chase_analysis) - Minimum cut
- [School Dance](school_dance_analysis) - Maximum bipartite matching
- [Distinct Routes](distinct_routes_analysis) - Edge-disjoint paths

### Advanced Problems
- [Road Construction](road_construction_analysis) - Dynamic connectivity
- [Road Construction II](road_construction_ii_analysis) - Advanced road building
- [Road Construction III](road_construction_iii_analysis) - Complex road network
- [Road Construction IV](road_construction_iv_analysis) - Expert road planning
- [Road Reparation](road_reparation_analysis) - Minimum spanning tree

### Special Graph Problems
- [Planets Queries I](planets_queries_i_analysis) - Binary lifting
- [Planets Queries II](planets_queries_ii_analysis) - Advanced graph queries
- [Teleporters Path](teleporters_path_analysis) - Eulerian path
- [Hamiltonian Flights](hamiltonian_flights_analysis) - Hamiltonian paths
- [Knights Tour](knights_tour_analysis) - Knight's tour on chessboard

## Detailed Examples and Implementations

### Classic Graph Algorithms with Code

#### 1. Depth-First Search (DFS)
```python
# Recursive DFS
def dfs_recursive(graph, start, visited=None):
 if visited is None:
  visited = set()
 
 visited.add(start)
 print(start)  # Process node
 
 for neighbor in graph[start]:
  if neighbor not in visited:
   dfs_recursive(graph, neighbor, visited)
 
 return visited

# Iterative DFS with stack
def dfs_iterative(graph, start):
 visited = set()
 stack = [start]
 
 while stack:
  node = stack.pop()
  if node not in visited:
   visited.add(node)
   print(node)  # Process node
   
   # Add neighbors in reverse order for same traversal as recursive
   for neighbor in reversed(graph[node]):
    if neighbor not in visited:
     stack.append(neighbor)
 
 return visited

# DFS with path tracking
def dfs_with_path(graph, start, target):
 def dfs_helper(node, path, visited):
  if node == target:
   return path + [node]
  
  visited.add(node)
  for neighbor in graph[node]:
   if neighbor not in visited:
    result = dfs_helper(neighbor, path + [node], visited)
    if result:
     return result
  
  visited.remove(node)
  return None
 
 return dfs_helper(start, [], set())
```

#### 2. Breadth-First Search (BFS)
```python
# Basic BFS
def bfs(graph, start):
 visited = set()
 queue = deque([start])
 visited.add(start)
 
 while queue:
  node = queue.popleft()
  print(node)  # Process node
  
  for neighbor in graph[node]:
   if neighbor not in visited:
    visited.add(neighbor)
    queue.append(neighbor)
 
 return visited

# BFS with distance tracking
def bfs_with_distance(graph, start):
 visited = set()
 queue = deque([(start, 0)])
 visited.add(start)
 distances = {start: 0}
 
 while queue:
  node, dist = queue.popleft()
  
  for neighbor in graph[node]:
   if neighbor not in visited:
    visited.add(neighbor)
    distances[neighbor] = dist + 1
    queue.append((neighbor, dist + 1))
 
 return distances

# BFS for shortest path
def bfs_shortest_path(graph, start, target):
 if start == target:
  return [start]
 
 visited = set()
 queue = deque([(start, [start])])
 visited.add(start)
 
 while queue:
  node, path = queue.popleft()
  
  for neighbor in graph[node]:
   if neighbor == target:
    return path + [neighbor]
   
   if neighbor not in visited:
    visited.add(neighbor)
    queue.append((neighbor, path + [neighbor]))
 
 return None  # No path found
```

#### 3. Dijkstra's Algorithm
```python
import heapq

def dijkstra(graph, start):
 distances = {node: float('inf') for node in graph}
 distances[start] = 0
 pq = [(0, start)]
 visited = set()
 
 while pq:
  current_dist, node = heapq.heappop(pq)
  
  if node in visited:
   continue
  
  visited.add(node)
  
  for neighbor, weight in graph[node]:
   if neighbor not in visited:
    new_dist = current_dist + weight
    if new_dist < distances[neighbor]:
     distances[neighbor] = new_dist
     heapq.heappush(pq, (new_dist, neighbor))
 
 return distances

# Dijkstra with path reconstruction
def dijkstra_with_path(graph, start, target):
 distances = {node: float('inf') for node in graph}
 distances[start] = 0
 previous = {node: None for node in graph}
 pq = [(0, start)]
 visited = set()
 
 while pq:
  current_dist, node = heapq.heappop(pq)
  
  if node in visited:
   continue
  
  visited.add(node)
  
  if node == target:
   break
  
  for neighbor, weight in graph[node]:
   if neighbor not in visited:
    new_dist = current_dist + weight
    if new_dist < distances[neighbor]:
     distances[neighbor] = new_dist
     previous[neighbor] = node
     heapq.heappush(pq, (new_dist, neighbor))
 
 # Reconstruct path
 if distances[target] == float('inf'):
  return None, float('inf')
 
 path = []
 node = target
 while node is not None:
  path.append(node)
  node = previous[node]
 
 return path[::-1], distances[target]
```

#### 4. Floyd-Warshall Algorithm
```python
def floyd_warshall(graph):
 n = len(graph)
 dist = [[float('inf')] * n for _ in range(n)]
 
 # Initialize distances
 for i in range(n):
  dist[i][i] = 0
  for j, weight in graph[i]:
   dist[i][j] = weight
 
 # Floyd-Warshall algorithm
 for k in range(n):
  for i in range(n):
   for j in range(n):
    if dist[i][k] + dist[k][j] < dist[i][j]:
     dist[i][j] = dist[i][k] + dist[k][j]
 
 return dist

# Floyd-Warshall with path reconstruction
def floyd_warshall_with_path(graph):
 n = len(graph)
 dist = [[float('inf')] * n for _ in range(n)]
 next_node = [[None] * n for _ in range(n)]
 
 # Initialize
 for i in range(n):
  dist[i][i] = 0
  for j, weight in graph[i]:
   dist[i][j] = weight
   next_node[i][j] = j
 
 # Floyd-Warshall
 for k in range(n):
  for i in range(n):
   for j in range(n):
    if dist[i][k] + dist[k][j] < dist[i][j]:
     dist[i][j] = dist[i][k] + dist[k][j]
     next_node[i][j] = next_node[i][k]
 
 def get_path(i, j):
  if next_node[i][j] is None:
   return []
  
  path = [i]
  while i != j:
   i = next_node[i][j]
   path.append(i)
  
  return path
 
 return dist, get_path
```

### Advanced Graph Algorithms

#### 1. Strongly Connected Components (Kosaraju's)
```python
def kosaraju_scc(graph):
 n = len(graph)
 visited = [False] * n
 order = []
 
 # First pass: get finish times
 def dfs1(node):
  visited[node] = True
  for neighbor in graph[node]:
   if not visited[neighbor]:
    dfs1(neighbor)
  order.append(node)
 
 for i in range(n):
  if not visited[i]:
   dfs1(i)
 
 # Reverse graph
 reversed_graph = [[] for _ in range(n)]
 for i in range(n):
  for j in graph[i]:
   reversed_graph[j].append(i)
 
 # Second pass: find SCCs
 visited = [False] * n
 sccs = []
 
 def dfs2(node, component):
  visited[node] = True
  component.append(node)
  for neighbor in reversed_graph[node]:
   if not visited[neighbor]:
    dfs2(neighbor, component)
 
 for node in reversed(order):
  if not visited[node]:
   component = []
   dfs2(node, component)
   sccs.append(component)
 
 return sccs
```

#### 2. Minimum Spanning Tree (Kruskal's)
```python
class UnionFind:
 def __init__(self, n):
  self.parent = list(range(n))
  self.rank = [0] * n
 
 def find(self, x):
  if self.parent[x] != x:
   self.parent[x] = self.find(self.parent[x])
  return self.parent[x]
 
 def union(self, x, y):
  px, py = self.find(x), self.find(y)
  if px == py:
   return False
  
  if self.rank[px] < self.rank[py]:
   px, py = py, px
  
  self.parent[py] = px
  if self.rank[px] == self.rank[py]:
   self.rank[px] += 1
  
  return True

def kruskal_mst(edges, n):
 edges.sort(key=lambda x: x[2])  # Sort by weight
 uf = UnionFind(n)
 mst = []
 total_weight = 0
 
 for u, v, weight in edges:
  if uf.union(u, v):
   mst.append((u, v, weight))
   total_weight += weight
   if len(mst) == n - 1:
    break
 
 return mst, total_weight
```

#### 3. Network Flow (Ford-Fulkerson)
```python
def ford_fulkerson(graph, source, sink):
 def bfs_path(graph, source, sink, parent):
  visited = [False] * len(graph)
  queue = deque([source])
  visited[source] = True
  
  while queue:
   u = queue.popleft()
   for v, capacity in enumerate(graph[u]):
    if not visited[v] and capacity > 0:
     visited[v] = True
     parent[v] = u
     if v == sink:
      return True
     queue.append(v)
  
  return False
 
 n = len(graph)
 parent = [-1] * n
 max_flow = 0
 
 while bfs_path(graph, source, sink, parent):
  path_flow = float('inf')
  s = sink
  
  while s != source:
   path_flow = min(path_flow, graph[parent[s]][s])
   s = parent[s]
  
  max_flow += path_flow
  v = sink
  
  while v != source:
   u = parent[v]
   graph[u][v] -= path_flow
   graph[v][u] += path_flow
   v = parent[v]
 
 return max_flow
```

### Graph Representation Examples

#### 1. Adjacency List Implementation
```python
class Graph:
 def __init__(self, vertices):
  self.vertices = vertices
  self.adj_list = [[] for _ in range(vertices)]
 
 def add_edge(self, u, v, weight=1):
  self.adj_list[u].append((v, weight))
  # For undirected graph, also add reverse edge
  # self.adj_list[v].append((u, weight))
 
 def get_neighbors(self, vertex):
  return self.adj_list[vertex]
 
 def has_edge(self, u, v):
  return any(neighbor == v for neighbor, _ in self.adj_list[u])
 
 def get_weight(self, u, v):
  for neighbor, weight in self.adj_list[u]:
   if neighbor == v:
    return weight
  return float('inf')
```

#### 2. Adjacency Matrix Implementation
```python
class GraphMatrix:
 def __init__(self, vertices):
  self.vertices = vertices
  self.matrix = [[0] * vertices for _ in range(vertices)]
 
 def add_edge(self, u, v, weight=1):
  self.matrix[u][v] = weight
  # For undirected graph, also set reverse edge
  # self.matrix[v][u] = weight
 
 def has_edge(self, u, v):
  return self.matrix[u][v] != 0
 
 def get_weight(self, u, v):
  return self.matrix[u][v] if self.matrix[u][v] != 0 else float('inf')
 
 def get_neighbors(self, vertex):
  neighbors = []
  for i in range(self.vertices):
   if self.matrix[vertex][i] != 0:
    neighbors.append((i, self.matrix[vertex][i]))
  return neighbors
```

### Advanced Graph Techniques

#### 1. Binary Lifting for LCA
```python
class BinaryLifting:
 def __init__(self, tree, root=0):
  self.n = len(tree)
  self.log = 20  # Adjust based on max depth
  self.up = [[-1] * self.n for _ in range(self.log)]
  self.depth = [0] * self.n
  
  self.dfs(tree, root, -1)
  
  for k in range(1, self.log):
   for v in range(self.n):
    if self.up[k-1][v] != -1:
     self.up[k][v] = self.up[k-1][self.up[k-1][v]]
 
 def dfs(self, tree, v, p):
  self.up[0][v] = p
  for u in tree[v]:
   if u != p:
    self.depth[u] = self.depth[v] + 1
    self.dfs(tree, u, v)
 
 def lca(self, u, v):
  if self.depth[u] < self.depth[v]:
   u, v = v, u
  
  # Bring u to same depth as v
  for k in range(self.log-1, -1, -1):
   if self.depth[u] - (1 << k) >= self.depth[v]:
    u = self.up[k][u]
  
  if u == v:
   return u
  
  # Find LCA
  for k in range(self.log-1, -1, -1):
   if self.up[k][u] != -1 and self.up[k][u] != self.up[k][v]:
    u = self.up[k][u]
    v = self.up[k][v]
  
  return self.up[0][u]
 
 def kth_ancestor(self, v, k):
  for i in range(self.log):
   if k & (1 << i):
    v = self.up[i][v]
    if v == -1:
     break
  return v
```

#### 2. Heavy-Light Decomposition
```python
class HeavyLightDecomposition:
 def __init__(self, tree, root=0):
  self.n = len(tree)
  self.tree = tree
  self.root = root
  self.parent = [-1] * self.n
  self.depth = [0] * self.n
  self.size = [0] * self.n
  self.heavy = [-1] * self.n
  self.head = [0] * self.n
  self.pos = [0] * self.n
  self.cur_pos = 0
  
  self.dfs1(root)
  self.dfs2(root, root)
 
 def dfs1(self, v):
  self.size[v] = 1
  for u in self.tree[v]:
   if u != self.parent[v]:
    self.parent[u] = v
    self.depth[u] = self.depth[v] + 1
    self.dfs1(u)
    self.size[v] += self.size[u]
    if self.heavy[v] == -1 or self.size[u] > self.size[self.heavy[v]]:
     self.heavy[v] = u
 
 def dfs2(self, v, h):
  self.head[v] = h
  self.pos[v] = self.cur_pos
  self.cur_pos += 1
  
  if self.heavy[v] != -1:
   self.dfs2(self.heavy[v], h)
  
  for u in self.tree[v]:
   if u != self.parent[v] and u != self.heavy[v]:
    self.dfs2(u, u)
 
 def query_path(self, u, v):
  res = 0
  while self.head[u] != self.head[v]:
   if self.depth[self.head[u]] > self.depth[self.head[v]]:
    u, v = v, u
   
   # Query segment tree from pos[head[v]] to pos[v]
   # res = max(res, seg_tree.query(self.pos[self.head[v]], self.pos[v]))
   v = self.parent[self.head[v]]
  
  if self.depth[u] > self.depth[v]:
   u, v = v, u
  
  # Query segment tree from pos[u] to pos[v]
  # res = max(res, seg_tree.query(self.pos[u], self.pos[v]))
  return res
```

### Graph Problem Patterns

#### 1. Cycle Detection
```python
def has_cycle_directed(graph):
 WHITE, GRAY, BLACK = 0, 1, 2
 color = [WHITE] * len(graph)
 
 def dfs(node):
  if color[node] == GRAY:
   return True  # Back edge found
  if color[node] == BLACK:
   return False
  
  color[node] = GRAY
  for neighbor in graph[node]:
   if dfs(neighbor):
    return True
  
  color[node] = BLACK
  return False
 
 for i in range(len(graph)):
  if color[i] == WHITE:
   if dfs(i):
    return True
 
 return False

def has_cycle_undirected(graph):
 visited = [False] * len(graph)
 
 def dfs(node, parent):
  visited[node] = True
  for neighbor in graph[node]:
   if not visited[neighbor]:
    if dfs(neighbor, node):
     return True
   elif neighbor != parent:
    return True
  return False
 
 for i in range(len(graph)):
  if not visited[i]:
   if dfs(i, -1):
    return True
 
 return False
```

#### 2. Topological Sort
```python
def topological_sort_kahn(graph):
 n = len(graph)
 in_degree = [0] * n
 
 # Calculate in-degrees
 for i in range(n):
  for j in graph[i]:
   in_degree[j] += 1
 
 # Find all vertices with no incoming edges
 queue = deque([i for i in range(n) if in_degree[i] == 0])
 result = []
 
 while queue:
  u = queue.popleft()
  result.append(u)
  
  for v in graph[u]:
   in_degree[v] -= 1
   if in_degree[v] == 0:
    queue.append(v)
 
 return result if len(result) == n else None  # Cycle detected

def topological_sort_dfs(graph):
 n = len(graph)
 visited = [False] * n
 stack = []
 
 def dfs(node):
  visited[node] = True
  for neighbor in graph[node]:
   if not visited[neighbor]:
    dfs(neighbor)
  stack.append(node)
 
 for i in range(n):
  if not visited[i]:
   dfs(i)
 
 return stack[::-1]
```

## Tips for Success

1. **Master Graph Traversal**: Foundation for all algorithms
2. **Understand Representations**: Choose appropriate ones
3. **Practice Implementation**: Code common algorithms
4. **Learn Optimization**: Improve time and space complexity
5. **Study Patterns**: Learn common graph problem patterns
6. **Handle Edge Cases**: Consider disconnected components, cycles, etc.

## Common Pitfalls to Avoid

1. **Infinite Loops**: In cycle detection
2. **Memory Limits**: With adjacency matrices
3. **Time Limits**: With inefficient algorithms
4. **Edge Cases**: Disconnected graphs, self-loops
5. **Index Errors**: Off-by-one mistakes in graph traversal
6. **Stack Overflow**: Deep recursion in large graphs

## Advanced Topics

### Graph Theory
- **Euler Tours**: Edge traversal
- **Hamilton Paths**: Vertex traversal
- **Planar Graphs**: Geometric properties
- **Graph Coloring**: Vertex coloring

### Optimization Techniques
- **Binary Lifting**: Fast ancestor queries
- **Heavy-Light Decomposition**: Path queries
- **Centroid Decomposition**: Tree distances
- **Dynamic Connectivity**: Online updates

## 📚 **Additional Learning Resources**

### **LeetCode Pattern Integration**
For interview preparation and pattern recognition, complement your CSES learning with these LeetCode resources:

- **[Awesome LeetCode Resources](https://github.com/ashishps1/awesome-leetcode-resources)** - Comprehensive collection of LeetCode patterns, templates, and curated problem lists
- **[Graph Algorithm Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Essential graph patterns including DFS, BFS, and shortest path algorithms
- **[Graph Problem Templates](https://github.com/ashishps1/awesome-leetcode-resources#-must-read-leetcode-articles)** - Specific graph algorithm templates and optimization techniques

### **Related LeetCode Problems**
Practice these LeetCode problems to reinforce graph algorithm concepts:

- **DFS/BFS Pattern**: [Number of Islands](https://leetcode.com/problems/number-of-islands/), [Word Search](https://leetcode.com/problems/word-search/), [Course Schedule](https://leetcode.com/problems/course-schedule/)
- **Shortest Path Pattern**: [Network Delay Time](https://leetcode.com/problems/network-delay-time/), [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)
- **Topological Sort Pattern**: [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/), [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)
- **Union-Find Pattern**: [Number of Connected Components](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/), [Redundant Connection](https://leetcode.com/problems/redundant-connection/)

---

Ready to start? Begin with [Counting Rooms](counting_rooms_analysis) and work your way through the problems in order of difficulty!