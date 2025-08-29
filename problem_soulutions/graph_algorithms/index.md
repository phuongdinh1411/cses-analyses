---
layout: simple
title: "Graph Algorithms"
permalink: /cses-analyses/problem_soulutions/graph_algorithms
---

# Graph Algorithms

Welcome to the Graph Algorithms section! This category focuses on problems involving networks, connectivity, and relationships between entities.

## Overview

Graph Algorithms help you master:
- **Graph representation** and traversal techniques
- **Shortest path** and connectivity algorithms
- **Network flow** and matching problems
- **Advanced graph** concepts and optimizations

## Topics Covered

### 🛣️ **Shortest Path Problems**
- **Shortest Routes I** - Dijkstra's algorithm
- **Shortest Routes II** - Floyd-Warshall algorithm
- **Flight Discount** - Modified shortest path
- **High Score** - Negative cycle detection
- **Police Chase** - Maximum flow with minimum cost

### 🔗 **Connectivity & Components**
- **Building Roads** - Minimum spanning tree
- **Road Construction** - MST with constraints
- **Road Construction II-IV** - Advanced MST variants
- **Road Reparation** - Minimum cost repairs
- **Strongly Connected Components** - Tarjan's algorithm

### 🎯 **Traversal & Search**
- **Counting Rooms** - Connected component counting
- **Labyrinth** - BFS/DFS maze solving
- **Monsters** - Multi-source BFS
- **Message Route** - Shortest path in unweighted graph
- **Round Trip** - Cycle detection

### 🏗️ **Network & Flow**
- **Download Speed** - Maximum flow
- **School Dance** - Bipartite matching
- **Distinct Routes** - Edge-disjoint paths
- **Coin Collector** - Maximum independent set

### 🎮 **Advanced Graph Problems**
- **Building Teams** - Bipartite graph coloring
- **Planets and Kingdoms** - Strongly connected components
- **Planets Cycles** - Cycle detection in directed graphs
- **Planets Queries I-II** - Lowest common ancestor
- **Giant Pizza** - 2-SAT problem
- **Hamiltonian Flights** - Hamiltonian path
- **Knights Tour** - Eulerian path
- **De Bruijn Sequence** - Eulerian circuit
- **Teleporters Path** - Eulerian trail

### 🔍 **Specialized Algorithms**
- **Cycle Finding** - Floyd's cycle-finding algorithm
- **Coordinate Compression** - Efficient coordinate mapping
- **Mail Delivery** - Chinese postman problem

## Learning Path

### 🟢 **Beginner Level** (Start Here)
1. **Counting Rooms** - Basic DFS/BFS
2. **Labyrinth** - Graph traversal
3. **Building Roads** - Simple MST
4. **Message Route** - Shortest path in unweighted graph

### 🟡 **Intermediate Level**
1. **Shortest Routes I** - Dijkstra's algorithm
2. **Building Teams** - Bipartite graph coloring
3. **Road Construction** - MST with constraints
4. **Monsters** - Multi-source BFS

### 🔴 **Advanced Level**
1. **Shortest Routes II** - Floyd-Warshall
2. **Strongly Connected Components** - Tarjan's algorithm
3. **Download Speed** - Maximum flow
4. **Giant Pizza** - 2-SAT problem

## Key Concepts

### 🏗️ **Graph Representation**
- **Adjacency Matrix**: `O(V²)` space, `O(1)` edge queries
- **Adjacency List**: `O(V + E)` space, `O(degree)` edge queries
- **Edge List**: `O(E)` space, `O(E)` edge queries

### 🔍 **Traversal Algorithms**
- **Depth-First Search (DFS)**: Stack-based, good for connectivity
- **Breadth-First Search (BFS)**: Queue-based, good for shortest paths
- **Topological Sort**: DAG ordering, dependency resolution

### 🛣️ **Shortest Path Algorithms**
- **Dijkstra's**: Single-source, non-negative weights
- **Bellman-Ford**: Single-source, handles negative weights
- **Floyd-Warshall**: All-pairs shortest paths
- **SPFA**: Optimized Bellman-Ford

### 🌳 **Minimum Spanning Tree**
- **Kruskal's**: Sort edges, union-find
- **Prim's**: Priority queue, grows tree
- **Boruvka's**: Parallel algorithm

## Algorithmic Techniques

### 🔍 **Breadth-First Search**
```python
from collections import deque

def bfs(graph, start):
    n = len(graph)
    visited = [False] * n
    distance = [-1] * n
    queue = deque([start])
    
    visited[start] = True
    distance[start] = 0
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    
    return distance
```

### 🛣️ **Dijkstra's Algorithm**
```python
import heapq

def dijkstra(graph, start):
    n = len(graph)
    distance = [float('inf')] * n
    distance[start] = 0
    pq = [(0, start)]
    
    while pq:
        dist, node = heapq.heappop(pq)
        if dist > distance[node]:
            continue
            
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distance[neighbor]:
                distance[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distance
```

### 🌳 **Kruskal's MST**
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

def kruskal(edges, n):
    edges.sort(key=lambda x: x[2])  # Sort by weight
    uf = UnionFind(n)
    mst_weight = 0
    
    for u, v, weight in edges:
        if uf.union(u, v):
            mst_weight += weight
    
    return mst_weight
```

### 🔗 **Strongly Connected Components (Tarjan)**
```python
def tarjan_scc(graph):
    n = len(graph)
    disc = [-1] * n
    low = [-1] * n
    stack = []
    in_stack = [False] * n
    time = 0
    sccs = []
    
    def dfs(node):
        nonlocal time
        disc[node] = low[node] = time
        time += 1
        stack.append(node)
        in_stack[node] = True
        
        for neighbor in graph[node]:
            if disc[neighbor] == -1:
                dfs(neighbor)
                low[node] = min(low[node], low[neighbor])
            elif in_stack[neighbor]:
                low[node] = min(low[node], disc[neighbor])
        
        if low[node] == disc[node]:
            scc = []
            while True:
                v = stack.pop()
                in_stack[v] = False
                scc.append(v)
                if v == node:
                    break
            sccs.append(scc)
    
    for i in range(n):
        if disc[i] == -1:
            dfs(i)
    
    return sccs
```

## Common Graph Patterns

### 🔍 **Connected Components**
- **Undirected**: DFS/BFS to find all reachable nodes
- **Directed**: Tarjan's algorithm for strongly connected components
- **Bipartite**: BFS with coloring to check bipartiteness

### 🛣️ **Path Problems**
- **Shortest path**: Dijkstra's for non-negative, Bellman-Ford for negative
- **All-pairs**: Floyd-Warshall for small graphs
- **Hamiltonian path**: NP-complete, use backtracking for small graphs

### 🌳 **Tree Problems**
- **Minimum spanning tree**: Kruskal's or Prim's
- **Lowest common ancestor**: Binary lifting or Euler tour
- **Tree diameter**: Two BFS runs

## Tips for Success

1. **Choose Representation**: Use adjacency list for sparse graphs, matrix for dense
2. **Handle Cycles**: Be careful with directed graphs and cycles
3. **Optimize Traversal**: Use appropriate data structures (queue for BFS, stack for DFS)
4. **Consider Constraints**: Edge cases like disconnected graphs, self-loops
5. **Use Specialized Algorithms**: Don't reinvent the wheel for common problems

## Related Topics

After mastering graph algorithms, explore:
- **Advanced Graph Problems** - Complex graph theory concepts
- **Range Queries** - Efficient query processing on trees
- **String Algorithms** - Pattern matching and text processing
- **Competitive Programming** - Advanced problem-solving strategies

---

*Ready to master networks and connectivity? Start with the beginner problems and build your graph skills!* 