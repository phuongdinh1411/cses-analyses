---
layout: simple
title: "Advanced Graph Problems Summary"
permalink: /problem_soulutions/advanced_graph_problems/summary
---

# Advanced Graph Problems

Welcome to the Advanced Graph Problems section! This category covers complex graph algorithms and techniques for solving challenging network problems.

## Key Concepts & Techniques

### Advanced Graph Theory

#### Hamiltonian Paths and Cycles
- **Hamiltonian Path**: Visit each vertex exactly once
  - *When to use*: When you need to visit all vertices exactly once
  - *Time*: O(n!) brute force, O(n²2ⁿ) with DP
  - *Space*: O(n2ⁿ) for DP
  - *Applications*: TSP, scheduling, routing
  - *Implementation*: Backtracking or DP with bitmask
- **Hamiltonian Cycle**: Closed path visiting all vertices
  - *When to use*: When you need closed path visiting all vertices
  - *Time*: O(n!) brute force, O(n²2ⁿ) with DP
  - *Space*: O(n2ⁿ) for DP
  - *Applications*: TSP, circuit design, optimization
  - *Implementation*: Backtracking or DP with bitmask
- **Fixed Length Hamiltonian**: Paths/cycles of specific length
  - *When to use*: When you need paths/cycles of specific length
  - *Time*: O(n²2ⁿ) with DP
  - *Space*: O(n2ⁿ) for DP
  - *Applications*: Constrained TSP, optimization
  - *Implementation*: DP with bitmask and length tracking

#### Eulerian Paths and Circuits
- **Eulerian Path**: Use each edge exactly once
  - *When to use*: When you need to use all edges exactly once
  - *Time*: O(V + E)
  - *Space*: O(V + E)
  - *Applications*: Mail delivery, network traversal, optimization
  - *Implementation*: Hierholzer's algorithm or Fleury's algorithm
- **Eulerian Circuit**: Closed path using all edges
  - *When to use*: When you need closed path using all edges
  - *Time*: O(V + E)
  - *Space*: O(V + E)
  - *Applications*: Circuit design, network optimization
  - *Implementation*: Hierholzer's algorithm
- **Fixed Length Eulerian**: Paths/circuits of specific length
  - *When to use*: When you need paths/circuits of specific length
  - *Time*: O(V + E) with modifications
  - *Space*: O(V + E)
  - *Applications*: Constrained traversal, optimization
  - *Implementation*: Modified Hierholzer's algorithm

#### Network Flow and Design
- **Maximum Flow**: Maximum flow through network
  - *When to use*: When you need maximum flow through network
  - *Time*: O(VE²) with Edmonds-Karp, O(V²E) with Dinic's
  - *Space*: O(V + E)
  - *Applications*: Network optimization, resource allocation
  - *Implementation*: Ford-Fulkerson, Edmonds-Karp, or Dinic's algorithm
- **Minimum Cut**: Minimum capacity cut
  - *When to use*: When you need minimum capacity cut
  - *Time*: O(VE²) with Edmonds-Karp
  - *Space*: O(V + E)
  - *Applications*: Network reliability, optimization
  - *Implementation*: Use max flow to find min cut
- **Network Design**: Optimize network structure
  - *When to use*: When you need to optimize network structure
  - *Time*: Depends on specific problem
  - *Space*: O(V + E)
  - *Applications*: Network optimization, facility location
  - *Implementation*: Use flow algorithms or optimization techniques

### Advanced Graph Algorithms

#### Matrix Exponentiation for Path Counting
- **Path Counting**: Count paths of specific length
  - *When to use*: When you need to count paths of specific length
  - *Time*: O(n³ log k) where k is path length
  - *Space*: O(n²)
  - *Applications*: Path counting, reachability, optimization
  - *Implementation*: Use matrix exponentiation on adjacency matrix
- **Walk Counting**: Count walks of specific length
  - *When to use*: When you need to count walks of specific length
  - *Time*: O(n³ log k) where k is walk length
  - *Space*: O(n²)
  - *Applications*: Walk counting, reachability, optimization
  - *Implementation*: Use matrix exponentiation on adjacency matrix
- **Circuit Counting**: Count circuits of specific length
  - *When to use*: When you need to count circuits of specific length
  - *Time*: O(n³ log k) where k is circuit length
  - *Space*: O(n²)
  - *Applications*: Circuit counting, optimization
  - *Implementation*: Use matrix exponentiation with modifications

#### Graph Properties and Analysis
- **Graph Girth**: Shortest cycle length
  - *When to use*: When you need shortest cycle length
  - *Time*: O(V(V + E)) with BFS
  - *Space*: O(V + E)
  - *Applications*: Graph analysis, optimization, network design
  - *Implementation*: BFS from each vertex to find shortest cycle
- **Strongly Connected Components**: Find SCCs
  - *When to use*: When you need to find strongly connected components
  - *Time*: O(V + E)
  - *Space*: O(V + E)
  - *Applications*: Graph analysis, network optimization
  - *Implementation*: Kosaraju's or Tarjan's algorithm
- **Critical Edges**: Edges whose removal affects connectivity
  - *When to use*: When you need to find critical edges
  - *Time*: O(V + E)
  - *Space*: O(V + E)
  - *Applications*: Network reliability, optimization
  - *Implementation*: Use bridge finding or connectivity analysis

#### Tree Algorithms and Encoding
- **Prufer Code**: Encode trees as sequences
  - *When to use*: When you need to encode trees as sequences
  - *Time*: O(n) for encoding/decoding
  - *Space*: O(n)
  - *Applications*: Tree representation, optimization, counting
  - *Implementation*: Use Prufer sequence construction
- **Tree Traversals**: Advanced traversal techniques
  - *When to use*: When you need advanced tree traversal
  - *Time*: O(n) for traversal
  - *Space*: O(n)
  - *Applications*: Tree analysis, optimization, queries
  - *Implementation*: Use DFS, BFS, or specialized traversals
- **Tree Properties**: Analyze tree characteristics
  - *When to use*: When you need to analyze tree characteristics
  - *Time*: O(n) for analysis
  - *Space*: O(n)
  - *Applications*: Tree analysis, optimization, queries
  - *Implementation*: Use tree DP or specialized algorithms

### Specialized Graph Techniques

#### Graph Compression and Optimization
- **Graph Compression**: Reduce graph size
  - *When to use*: When you need to reduce graph size
  - *Time*: Depends on compression technique
  - *Space*: Reduced space usage
  - *Applications*: Large graphs, memory optimization
  - *Implementation*: Use graph compression techniques
- **Graph Partitioning**: Divide graph into parts
  - *When to use*: When you need to divide graph into parts
  - *Time*: Depends on partitioning technique
  - *Space*: O(V + E)
  - *Applications*: Parallel processing, optimization
  - *Implementation*: Use graph partitioning algorithms
- **Graph Clustering**: Group similar vertices
  - *When to use*: When you need to group similar vertices
  - *Time*: Depends on clustering technique
  - *Space*: O(V + E)
  - *Applications*: Community detection, optimization
  - *Implementation*: Use graph clustering algorithms

#### Dynamic Graph Algorithms
- **Dynamic Connectivity**: Handle edge additions/deletions
  - *When to use*: When you need to handle dynamic edges
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Dynamic networks, online algorithms
  - *Implementation*: Use link-cut trees or dynamic connectivity
- **Dynamic Shortest Paths**: Handle edge weight changes
  - *When to use*: When you need to handle dynamic edge weights
  - *Time*: O(V²) per update
  - *Space*: O(V²)
  - *Applications*: Dynamic networks, online algorithms
  - *Implementation*: Use dynamic shortest path algorithms
- **Dynamic Flow**: Handle flow changes
  - *When to use*: When you need to handle dynamic flow
  - *Time*: Depends on specific algorithm
  - *Space*: O(V + E)
  - *Applications*: Dynamic networks, online algorithms
  - *Implementation*: Use dynamic flow algorithms

#### Graph Query Processing
- **Path Queries**: Answer path-related queries
  - *When to use*: When you need to answer path queries
  - *Time*: O(log n) per query
  - *Space*: O(n log n)
  - *Applications*: Graph databases, optimization
  - *Implementation*: Use binary lifting or segment trees
- **Distance Queries**: Answer distance queries
  - *When to use*: When you need to answer distance queries
  - *Time*: O(log n) per query
  - *Space*: O(n log n)
  - *Applications*: Graph databases, optimization
  - *Implementation*: Use binary lifting or segment trees
- **Connectivity Queries**: Answer connectivity queries
  - *When to use*: When you need to answer connectivity queries
  - *Time*: O(α(n)) per query
  - *Space*: O(n)
  - *Applications*: Graph databases, optimization
  - *Implementation*: Use Union-Find or dynamic connectivity

### Optimization Techniques

#### Algorithm Selection
- **Choose Right Algorithm**: Based on problem constraints
  - *When to use*: When multiple algorithms available
  - *Example*: Use matrix exponentiation for path counting, DP for Hamiltonian
- **Hybrid Approaches**: Combine multiple techniques
  - *When to use*: When single approach not optimal
  - *Example*: Combine flow algorithms with optimization techniques
- **Adaptive Algorithms**: Adjust based on input
  - *When to use*: When input characteristics vary
  - *Example*: Adaptive graph algorithms, dynamic optimization

#### Space Optimization
- **Graph Compression**: Reduce memory usage
  - *When to use*: When memory is limited
  - *Example*: Compress adjacency lists, use sparse representations
- **Lazy Evaluation**: Compute on demand
  - *When to use*: When not all values needed
  - *Example*: Lazy graph construction, on-demand computation
- **Memory Pool**: Reuse allocated memory
  - *When to use*: When memory allocation is expensive
  - *Example*: Reuse graph structures, memory pools

#### Time Optimization
- **Precomputation**: Compute values once
  - *When to use*: When same calculations repeated
  - *Example*: Precompute shortest paths, precompute connectivity
- **Caching**: Store computed results
  - *When to use*: When calculations are expensive
  - *Example*: Cache graph properties, cache query results
- **Parallel Processing**: Use multiple processors
  - *When to use*: When parallel processing available
  - *Example*: Parallel graph algorithms, parallel optimization

## Problem Categories

### Graph Properties
- [Acyclic Graph Edges](acyclic_graph_edges_analysis) - Maintaining acyclicity
- [Strongly Connected Edges](strongly_connected_edges_analysis) - Critical edges
- [Graph Girth](graph_girth_analysis) - Shortest cycle

### Path and Circuit Queries
- [Fixed Length Path Queries](fixed_length_path_queries_analysis) - Path counting
- [Fixed Length Tour Queries](fixed_length_tour_queries_analysis) - Tour counting
- [Fixed Length Trail Queries](fixed_length_trail_queries_analysis) - Trail counting
- [Fixed Length Walk Queries](fixed_length_walk_queries_analysis) - Walk counting

### Hamiltonian Problems
- [Fixed Length Hamiltonian Path Queries](fixed_length_hamiltonian_path_queries_analysis) - Hamiltonian paths
- [Fixed Length Hamiltonian Path Queries II](fixed_length_hamiltonian_path_queries_ii_analysis) - Advanced paths
- [Fixed Length Hamiltonian Cycle Queries](fixed_length_hamiltonian_cycle_queries_analysis) - Hamiltonian cycles
- [Fixed Length Hamiltonian Cycle Queries II](fixed_length_hamiltonian_cycle_queries_ii_analysis) - Advanced cycles
- [Fixed Length Hamiltonian Tour Queries](fixed_length_hamiltonian_tour_queries_analysis) - Hamiltonian tours
- [Fixed Length Hamiltonian Tour Queries II](fixed_length_hamiltonian_tour_queries_ii_analysis) - Advanced tours
- [Fixed Length Hamiltonian Trail Queries](fixed_length_hamiltonian_trail_queries_analysis) - Hamiltonian trails
- [Fixed Length Hamiltonian Trail Queries II](fixed_length_hamiltonian_trail_queries_ii_analysis) - Advanced trails

### Eulerian Problems
- [Fixed Length Eulerian Circuit Queries](fixed_length_eulerian_circuit_queries_analysis) - Eulerian circuits
- [Fixed Length Eulerian Trail Queries](fixed_length_eulerian_trail_queries_analysis) - Eulerian trails

### Network and Flow Problems
- [MST Edge Check](mst_edge_check_analysis) - Spanning tree edges
- [New Flight Routes](new_flight_routes_analysis) - Network design
- [Transfer Speeds Sum](transfer_speeds_sum_analysis) - Network optimization
- [Nearest Shops](nearest_shops_analysis) - Facility location
- [Creating Offices](creating_offices_analysis) - Facility location
- [Course Schedule II](course_schedule_ii_analysis) - Task scheduling

### Tree Problems
- [Tree Traversals](tree_traversals_analysis) - Advanced traversal
- [Prufer Code](prufer_code_analysis) - Tree encoding

## Detailed Examples and Implementations

### Advanced Graph Algorithms with Code

#### 1. Hamiltonian Paths and Cycles
```python
def hamiltonian_path_exists(graph, n):
    """Check if Hamiltonian path exists using dynamic programming"""
    # dp[mask][i] = True if we can visit all vertices in mask ending at vertex i
    dp = [[False] * n for _ in range(1 << n)]
    
    # Base case: single vertex
    for i in range(n):
        dp[1 << i][i] = True
    
    # Fill DP table
    for mask in range(1 << n):
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            
            for j in range(n):
                if i != j and (mask & (1 << j)) and graph[j][i]:
                    dp[mask][i] |= dp[mask ^ (1 << i)][j]
    
    # Check if any vertex can be the end of Hamiltonian path
    full_mask = (1 << n) - 1
    return any(dp[full_mask][i] for i in range(n))

def hamiltonian_cycle_exists(graph, n):
    """Check if Hamiltonian cycle exists using dynamic programming"""
    # dp[mask][i] = True if we can visit all vertices in mask ending at vertex i
    dp = [[False] * n for _ in range(1 << n)]
    
    # Base case: single vertex
    for i in range(n):
        dp[1 << i][i] = True
    
    # Fill DP table
    for mask in range(1 << n):
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            
            for j in range(n):
                if i != j and (mask & (1 << j)) and graph[j][i]:
                    dp[mask][i] |= dp[mask ^ (1 << i)][j]
    
    # Check if we can return to starting vertex
    full_mask = (1 << n) - 1
    for i in range(n):
        if dp[full_mask][i] and graph[i][0]:  # Can return to vertex 0
            return True
    
    return False

def find_hamiltonian_path(graph, n):
    """Find actual Hamiltonian path using backtracking"""
    def backtrack(path, used):
        if len(path) == n:
            return path[:]
        
        current = path[-1]
        for next_vertex in range(n):
            if not used[next_vertex] and graph[current][next_vertex]:
                used[next_vertex] = True
                path.append(next_vertex)
                
                result = backtrack(path, used)
                if result:
                    return result
                
                path.pop()
                used[next_vertex] = False
        
        return None
    
    # Try starting from each vertex
    for start in range(n):
        used = [False] * n
        used[start] = True
        result = backtrack([start], used)
        if result:
            return result
    
    return None

def count_hamiltonian_paths(graph, n):
    """Count number of Hamiltonian paths using dynamic programming"""
    # dp[mask][i] = number of ways to visit all vertices in mask ending at vertex i
    dp = [[0] * n for _ in range(1 << n)]
    
    # Base case: single vertex
    for i in range(n):
        dp[1 << i][i] = 1
    
    # Fill DP table
    for mask in range(1 << n):
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            
            for j in range(n):
                if i != j and (mask & (1 << j)) and graph[j][i]:
                    dp[mask][i] += dp[mask ^ (1 << i)][j]
    
    # Sum all possible ending vertices
    full_mask = (1 << n) - 1
    return sum(dp[full_mask][i] for i in range(n))
```

#### 2. Eulerian Paths and Circuits
```python
def has_eulerian_circuit(graph, n):
    """Check if graph has Eulerian circuit"""
    # All vertices must have even degree
    for i in range(n):
        if sum(graph[i]) % 2 != 0:
            return False
    
    # Graph must be connected
    return is_connected(graph, n)

def has_eulerian_path(graph, n):
    """Check if graph has Eulerian path"""
    odd_degree_count = 0
    
    for i in range(n):
        degree = sum(graph[i])
        if degree % 2 != 0:
            odd_degree_count += 1
    
    # Eulerian path exists if 0 or 2 vertices have odd degree
    return odd_degree_count == 0 or odd_degree_count == 2

def find_eulerian_circuit(graph, n):
    """Find Eulerian circuit using Hierholzer's algorithm"""
    if not has_eulerian_circuit(graph, n):
        return None
    
    # Create adjacency list
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if graph[i][j]:
                adj[i].append(j)
    
    # Find starting vertex (any vertex with edges)
    start = 0
    for i in range(n):
        if adj[i]:
            start = i
            break
    
    stack = [start]
    path = []
    
    while stack:
        current = stack[-1]
        if adj[current]:
            # Follow edge
            next_vertex = adj[current].pop()
            stack.append(next_vertex)
        else:
            # No more edges, add to path
            path.append(stack.pop())
    
    return path[::-1]  # Reverse to get correct order

def find_eulerian_path(graph, n):
    """Find Eulerian path using Hierholzer's algorithm"""
    if not has_eulerian_path(graph, n):
        return None
    
    # Create adjacency list
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if graph[i][j]:
                adj[i].append(j)
    
    # Find starting vertex (vertex with odd degree, or any vertex)
    start = 0
    for i in range(n):
        if len(adj[i]) % 2 != 0:
            start = i
            break
    
    stack = [start]
    path = []
    
    while stack:
        current = stack[-1]
        if adj[current]:
            # Follow edge
            next_vertex = adj[current].pop()
            stack.append(next_vertex)
        else:
            # No more edges, add to path
            path.append(stack.pop())
    
    return path[::-1]  # Reverse to get correct order

def is_connected(graph, n):
    """Check if graph is connected using DFS"""
    visited = [False] * n
    
    def dfs(vertex):
        visited[vertex] = True
        for neighbor in range(n):
            if graph[vertex][neighbor] and not visited[neighbor]:
                dfs(neighbor)
    
    # Find first vertex with edges
    start = 0
    for i in range(n):
        if any(graph[i]):
            start = i
            break
    
    dfs(start)
    
    # Check if all vertices with edges are visited
    for i in range(n):
        if any(graph[i]) and not visited[i]:
            return False
    
    return True
```

#### 3. Network Flow Algorithms
```python
class MaxFlow:
    def __init__(self, n):
        self.n = n
        self.capacity = [[0] * n for _ in range(n)]
        self.adj = [[] for _ in range(n)]
    
    def add_edge(self, u, v, cap):
        self.capacity[u][v] += cap
        self.adj[u].append(v)
        self.adj[v].append(u)
    
    def ford_fulkerson(self, source, sink):
        """Find maximum flow using Ford-Fulkerson algorithm"""
        max_flow = 0
        parent = [-1] * self.n
        
        def bfs():
            visited = [False] * self.n
            queue = [source]
            visited[source] = True
            
            while queue:
                u = queue.pop(0)
                for v in self.adj[u]:
                    if not visited[v] and self.capacity[u][v] > 0:
                        visited[v] = True
                        parent[v] = u
                        queue.append(v)
                        if v == sink:
                            return True
            return False
        
        while bfs():
            path_flow = float('inf')
            s = sink
            
            # Find minimum capacity in path
            while s != source:
                path_flow = min(path_flow, self.capacity[parent[s]][s])
                s = parent[s]
            
            # Update residual capacities
            v = sink
            while v != source:
                u = parent[v]
                self.capacity[u][v] -= path_flow
                self.capacity[v][u] += path_flow
                v = parent[v]
            
            max_flow += path_flow
        
        return max_flow
    
    def edmonds_karp(self, source, sink):
        """Find maximum flow using Edmonds-Karp algorithm (BFS-based)"""
        max_flow = 0
        parent = [-1] * self.n
        
        def bfs():
            visited = [False] * self.n
            queue = [(source, float('inf'))]
            visited[source] = True
            
            while queue:
                u, flow = queue.pop(0)
                for v in self.adj[u]:
                    if not visited[v] and self.capacity[u][v] > 0:
                        visited[v] = True
                        parent[v] = u
                        new_flow = min(flow, self.capacity[u][v])
                        queue.append((v, new_flow))
                        if v == sink:
                            return new_flow
            return 0
        
        while True:
            flow = bfs()
            if flow == 0:
                break
            
            max_flow += flow
            v = sink
            
            # Update residual capacities
            while v != source:
                u = parent[v]
                self.capacity[u][v] -= flow
                self.capacity[v][u] += flow
                v = parent[v]
        
        return max_flow
    
    def dinic(self, source, sink):
        """Find maximum flow using Dinic's algorithm"""
        def bfs():
            level = [-1] * self.n
            level[source] = 0
            queue = [source]
            
            while queue:
                u = queue.pop(0)
                for v in self.adj[u]:
                    if level[v] < 0 and self.capacity[u][v] > 0:
                        level[v] = level[u] + 1
                        queue.append(v)
            
            return level[sink] >= 0
        
        def dfs(u, flow):
            if u == sink:
                return flow
            
            for v in self.adj[u]:
                if level[v] == level[u] + 1 and self.capacity[u][v] > 0:
                    pushed = dfs(v, min(flow, self.capacity[u][v]))
                    if pushed > 0:
                        self.capacity[u][v] -= pushed
                        self.capacity[v][u] += pushed
                        return pushed
            return 0
        
        max_flow = 0
        while bfs():
            while True:
                flow = dfs(source, float('inf'))
                if flow == 0:
                    break
                max_flow += flow
        return max_flow

def min_cut_max_flow(graph, source, sink):
    """Find minimum cut using max flow"""
    n = len(graph)
    max_flow_solver = MaxFlow(n)
    
    # Copy graph
    for i in range(n):
        for j in range(n):
            if graph[i][j] > 0:
                max_flow_solver.add_edge(i, j, graph[i][j])
    
    max_flow = max_flow_solver.ford_fulkerson(source, sink)
    
    # Find reachable vertices from source
    visited = [False] * n
    queue = [source]
    visited[source] = True
    
    while queue:
        u = queue.pop(0)
        for v in range(n):
            if not visited[v] and max_flow_solver.capacity[u][v] > 0:
                visited[v] = True
                queue.append(v)
    
    # Find cut edges
    cut_edges = []
    for i in range(n):
        for j in range(n):
            if visited[i] and not visited[j] and graph[i][j] > 0:
                cut_edges.append((i, j))
    
    return max_flow, cut_edges
```

#### 4. Matrix Exponentiation for Path Counting
```python
def matrix_multiply(A, B, mod=None):
    """Multiply two matrices"""
    n = len(A)
    m = len(B[0])
    k = len(B)
    
    result = [[0] * m for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            for l in range(k):
                result[i][j] += A[i][l] * B[l][j]
                if mod:
                    result[i][j] %= mod
    
    return result

def matrix_power(matrix, power, mod=None):
    """Compute matrix^power using binary exponentiation"""
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    
    # Initialize result as identity matrix
    for i in range(n):
        result[i][i] = 1
    
    base = [row[:] for row in matrix]
    
    while power > 0:
        if power % 2 == 1:
            result = matrix_multiply(result, base, mod)
        base = matrix_multiply(base, base, mod)
        power //= 2
    
    return result

def count_paths_of_length(graph, length, mod=None):
    """Count number of paths of given length using matrix exponentiation"""
    n = len(graph)
    
    # Raise adjacency matrix to the power of length
    result_matrix = matrix_power(graph, length, mod)
    
    # Sum all entries to get total number of paths
    total_paths = 0
    for i in range(n):
        for j in range(n):
            total_paths += result_matrix[i][j]
            if mod:
                total_paths %= mod
    
    return total_paths

def count_walks_between_vertices(graph, start, end, length, mod=None):
    """Count walks of given length between two vertices"""
    n = len(graph)
    result_matrix = matrix_power(graph, length, mod)
    return result_matrix[start][end]

def count_cycles_of_length(graph, length, mod=None):
    """Count cycles of given length"""
    n = len(graph)
    result_matrix = matrix_power(graph, length, mod)
    
    # Sum diagonal entries (cycles start and end at same vertex)
    total_cycles = 0
    for i in range(n):
        total_cycles += result_matrix[i][i]
        if mod:
            total_cycles %= mod
    
    return total_cycles

def count_paths_with_constraints(graph, length, constraints, mod=None):
    """Count paths with specific constraints using matrix exponentiation"""
    n = len(graph)
    
    # Apply constraints to adjacency matrix
    constrained_graph = [row[:] for row in graph]
    
    for constraint in constraints:
        if constraint['type'] == 'forbidden_edge':
            u, v = constraint['edge']
            constrained_graph[u][v] = 0
        elif constraint['type'] == 'required_vertex':
            vertex = constraint['vertex']
            # Set all edges not involving this vertex to 0
            for i in range(n):
                for j in range(n):
                    if i != vertex and j != vertex:
                        constrained_graph[i][j] = 0
    
    return count_paths_of_length(constrained_graph, length, mod)
```

#### 5. Graph Girth and Cycle Detection
```python
def find_graph_girth(graph, n):
    """Find girth (length of shortest cycle) of graph"""
    min_cycle_length = float('inf')
    
    for start in range(n):
        # BFS from each vertex to find shortest cycle
        distances = [-1] * n
        parent = [-1] * n
        queue = [(start, 0)]
        distances[start] = 0
        
        while queue:
            vertex, dist = queue.pop(0)
            
            for neighbor in range(n):
                if graph[vertex][neighbor]:
                    if distances[neighbor] == -1:
                        distances[neighbor] = dist + 1
                        parent[neighbor] = vertex
                        queue.append((neighbor, dist + 1))
                    elif neighbor != parent[vertex] and parent[vertex] != -1:
                        # Found a cycle
                        cycle_length = distances[vertex] + distances[neighbor] + 1
                        min_cycle_length = min(min_cycle_length, cycle_length)
    
    return min_cycle_length if min_cycle_length != float('inf') else -1

def find_all_cycles(graph, n):
    """Find all cycles in graph using DFS"""
    visited = [False] * n
    rec_stack = [False] * n
    cycles = []
    
    def dfs(vertex, parent, path):
        visited[vertex] = True
        rec_stack[vertex] = True
        path.append(vertex)
        
        for neighbor in range(n):
            if graph[vertex][neighbor]:
                if not visited[neighbor]:
                    dfs(neighbor, vertex, path)
                elif rec_stack[neighbor] and neighbor != parent:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle[:])
        
        path.pop()
        rec_stack[vertex] = False
    
    for i in range(n):
        if not visited[i]:
            dfs(i, -1, [])
    
    return cycles

def detect_negative_cycle(graph, n):
    """Detect negative cycle using Bellman-Ford algorithm"""
    distances = [float('inf')] * n
    distances[0] = 0
    
    # Relax edges n-1 times
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if graph[u][v] != 0 and distances[u] != float('inf'):
                    if distances[u] + graph[u][v] < distances[v]:
                        distances[v] = distances[u] + graph[u][v]
    
    # Check for negative cycle
    for u in range(n):
        for v in range(n):
            if graph[u][v] != 0 and distances[u] != float('inf'):
                if distances[u] + graph[u][v] < distances[v]:
                    return True
    
    return False

def find_strongly_connected_components_tarjan(graph, n):
    """Find strongly connected components using Tarjan's algorithm"""
    index = 0
    stack = []
    indices = [-1] * n
    lowlinks = [-1] * n
    on_stack = [False] * n
    sccs = []
    
    def strongconnect(vertex):
        nonlocal index
        indices[vertex] = index
        lowlinks[vertex] = index
        index += 1
        stack.append(vertex)
        on_stack[vertex] = True
        
        for neighbor in range(n):
            if graph[vertex][neighbor]:
                if indices[neighbor] == -1:
                    strongconnect(neighbor)
                    lowlinks[vertex] = min(lowlinks[vertex], lowlinks[neighbor])
                elif on_stack[neighbor]:
                    lowlinks[vertex] = min(lowlinks[vertex], indices[neighbor])
        
        if lowlinks[vertex] == indices[vertex]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == vertex:
                    break
            sccs.append(scc)
    
    for i in range(n):
        if indices[i] == -1:
            strongconnect(i)
    
    return sccs
```

#### 6. Advanced Graph Queries
```python
class GraphQueryProcessor:
    def __init__(self, graph, n):
        self.n = n
        self.graph = graph
        self.log = 0
        while (1 << self.log) <= n:
            self.log += 1
        
        # Binary lifting for LCA
        self.up = [[-1] * n for _ in range(self.log)]
        self.depth = [0] * n
        self.distances = [[0] * n for _ in range(n)]
        
        self.preprocess()
    
    def preprocess(self):
        """Preprocess for efficient queries"""
        # Floyd-Warshall for all-pairs shortest paths
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    self.distances[i][j] = 0
                elif self.graph[i][j] > 0:
                    self.distances[i][j] = self.graph[i][j]
                else:
                    self.distances[i][j] = float('inf')
        
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if self.distances[i][k] + self.distances[k][j] < self.distances[i][j]:
                        self.distances[i][j] = self.distances[i][k] + self.distances[k][j]
    
    def shortest_path(self, u, v):
        """Get shortest path distance between u and v"""
        return self.distances[u][v]
    
    def path_exists(self, u, v):
        """Check if path exists between u and v"""
        return self.distances[u][v] != float('inf')
    
    def count_paths(self, u, v, max_length):
        """Count paths from u to v with length <= max_length"""
        # Use matrix exponentiation
        result = 0
        current_matrix = [[0] * self.n for _ in range(self.n)]
        
        # Initialize with adjacency matrix
        for i in range(self.n):
            for j in range(self.n):
                current_matrix[i][j] = 1 if self.graph[i][j] > 0 else 0
        
        # Sum powers from 1 to max_length
        for length in range(1, max_length + 1):
            if length > 1:
                current_matrix = matrix_multiply(current_matrix, 
                    [[1 if self.graph[i][j] > 0 else 0 for j in range(self.n)] for i in range(self.n)])
            result += current_matrix[u][v]
        
        return result
    
    def diameter(self):
        """Find diameter of graph (longest shortest path)"""
        max_distance = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.distances[i][j] != float('inf'):
                    max_distance = max(max_distance, self.distances[i][j])
        return max_distance
    
    def radius(self):
        """Find radius of graph (minimum eccentricity)"""
        eccentricities = []
        for i in range(self.n):
            max_dist = 0
            for j in range(self.n):
                if self.distances[i][j] != float('inf'):
                    max_dist = max(max_dist, self.distances[i][j])
            eccentricities.append(max_dist)
        return min(eccentricities)
    
    def center(self):
        """Find center vertices (vertices with minimum eccentricity)"""
        eccentricities = []
        for i in range(self.n):
            max_dist = 0
            for j in range(self.n):
                if self.distances[i][j] != float('inf'):
                    max_dist = max(max_dist, self.distances[i][j])
            eccentricities.append(max_dist)
        
        min_eccentricity = min(eccentricities)
        return [i for i in range(self.n) if eccentricities[i] == min_eccentricity]

def dynamic_connectivity_queries(edges, queries):
    """Handle dynamic connectivity queries"""
    n = max(max(edge) for edge in edges) + 1
    graph = [[False] * n for _ in range(n)]
    results = []
    
    for query in queries:
        if query[0] == 'add':
            u, v = query[1], query[2]
            graph[u][v] = graph[v][u] = True
        elif query[0] == 'remove':
            u, v = query[1], query[2]
            graph[u][v] = graph[v][u] = False
        elif query[0] == 'connected':
            u, v = query[1], query[2]
            # Use BFS to check connectivity
            visited = [False] * n
            queue = [u]
            visited[u] = True
            connected = False
            
            while queue:
                current = queue.pop(0)
                if current == v:
                    connected = True
                    break
                
                for neighbor in range(n):
                    if graph[current][neighbor] and not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            
            results.append(connected)
    
    return results
```

## Tips for Success

1. **Master Basic Graph Theory**: Foundation for advanced problems
2. **Understand Path Types**: Different traversal requirements
3. **Learn Network Flow**: Essential for many problems
4. **Practice Implementation**: Code complex algorithms
5. **Study Matrix Methods**: For path counting and optimization
6. **Handle Dynamic Updates**: For online graph problems

## Common Pitfalls to Avoid

1. **Time Limits**: With exponential algorithms
2. **Memory Limits**: With large graphs
3. **Edge Cases**: Special graph structures
4. **Implementation Errors**: Complex algorithms

## Advanced Topics

### Graph Properties
- **Connectivity**: Strong components
- **Path Types**: Different traversals
- **Graph Metrics**: Distance measures
- **Graph Operations**: Modifications

### Algorithm Techniques
- **Matrix Methods**: Path counting
- **Flow Algorithms**: Network capacity
- **Tree Algorithms**: Special graphs
- **Query Processing**: Efficient answers

### Special Cases
- **Directed Graphs**: Edge direction
- **Weighted Graphs**: Edge weights
- **Bipartite Graphs**: Two-color property
- **Planar Graphs**: Geometric embedding

## 📚 **Additional Learning Resources**

### **LeetCode Pattern Integration**
For interview preparation and pattern recognition, complement your CSES learning with these LeetCode resources:

- **[Awesome LeetCode Resources](https://github.com/ashishps1/awesome-leetcode-resources)** - Comprehensive collection of LeetCode patterns, templates, and curated problem lists
- **[Advanced Graph Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Complex graph algorithms and optimization techniques
- **[Network Flow Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Advanced graph theory and flow algorithms

### **Related LeetCode Problems**
Practice these LeetCode problems to reinforce advanced graph algorithm concepts:

- **Advanced Graph Traversal**: [Word Ladder](https://leetcode.com/problems/word-ladder/), [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/), [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)
- **Network Flow**: [Maximum Flow](https://leetcode.com/problems/maximum-flow/), [Minimum Cost to Connect All Points](https://leetcode.com/problems/min-cost-connect-points/)
- **Graph Optimization**: [Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/), [Redundant Connection](https://leetcode.com/problems/redundant-connection/)
- **Advanced Algorithms**: [Course Schedule](https://leetcode.com/problems/course-schedule/), [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/), [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)

---

Ready to start? Begin with [Acyclic Graph Edges](acyclic_graph_edges_analysis) and work your way through the problems in order of difficulty!