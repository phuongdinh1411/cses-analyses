---
layout: simple
title: "Graph Algorithms Summary"
permalink: /problem_soulutions/graph_algorithms/summary
---

# Graph Algorithms

Welcome to the Graph Algorithms section! This category covers fundamental and advanced algorithms for solving problems involving networks, paths, and connectivity.

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

## Learning Path

### For Beginners (Start Here)
1. Start with **Counting Rooms** for basic graph traversal
2. Move to **Building Roads** for connectivity problems
3. Try **Message Route** for shortest paths
4. Learn bipartite graphs with **Building Teams**

### Intermediate Level
1. Master Dijkstra's with **Shortest Routes I**
2. Practice cycle detection with **Round Trip**
3. Explore SCCs with **Planets and Kingdoms**
4. Study flow networks with **School Dance**

### Advanced Level
1. Challenge yourself with **Giant Pizza**
2. Master advanced paths with **Hamiltonian Flights**
3. Solve complex networks with **Road Construction IV**
4. Tackle special queries with **Planets Queries II**

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

## Tips for Success

1. **Master Graph Traversal**: Foundation for all algorithms
2. **Understand Representations**: Choose appropriate ones
3. **Practice Implementation**: Code common algorithms
4. **Learn Optimization**: Improve time and space complexity

## Common Pitfalls to Avoid

1. **Infinite Loops**: In cycle detection
2. **Memory Limits**: With adjacency matrices
3. **Time Limits**: With inefficient algorithms
4. **Edge Cases**: Disconnected graphs, self-loops

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

---

Ready to start? Begin with [Counting Rooms](counting_rooms_analysis) and work your way through the problems in order of difficulty!