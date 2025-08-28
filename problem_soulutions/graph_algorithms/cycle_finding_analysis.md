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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Cycle Finding with Costs**
**Problem**: Find negative cycle with minimum total cost.
```python
def cost_based_cycle_finding(n, m, edges, costs):
    # costs[(a, b)] = additional cost for edge (a, b)
    
    # Build adjacency list with costs
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        additional_cost = costs.get((a, b), 0)
        adj[a].append((b, w + additional_cost))
    
    # Bellman-Ford with cost tracking
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    cycle_cost = [0] * (n + 1)
    
    # Initialize from all nodes
    for start in range(1, n + 1):
        if dist[start] == float('inf'):
            dist[start] = 0
            
            # Run Bellman-Ford
            for i in range(n - 1):
                for u in range(1, n + 1):
                    for v, w in adj[u]:
                        if dist[u] != float('inf') and dist[u] + w < dist[v]:
                            dist[v] = dist[u] + w
                            parent[v] = u
                            cycle_cost[v] = cycle_cost[u] + w
            
            # Check for negative cycle
            for u in range(1, n + 1):
                for v, w in adj[u]:
                    if dist[u] != float('inf') and dist[u] + w < dist[v]:
                        # Found negative cycle, reconstruct
                        cycle = []
                        visited = set()
                        current = v
                        
                        while current not in visited:
                            visited.add(current)
                            cycle.append(current)
                            current = parent[current]
                        
                        cycle_start = current
                        cycle_nodes = []
                        current = v
                        while current != cycle_start:
                            cycle_nodes.append(current)
                            current = parent[current]
                        cycle_nodes.append(cycle_start)
                        
                        total_cost = sum(cycle_cost[node] for node in cycle_nodes)
                        return True, cycle_nodes[::-1], total_cost
    
    return False, None, 0
```

#### **Variation 2: Cycle Finding with Constraints**
**Problem**: Find negative cycle with constraints on cycle length or node count.
```python
def constrained_cycle_finding(n, m, edges, constraints):
    # constraints = {'min_length': x, 'max_length': y, 'min_cost': z}
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
    
    # Bellman-Ford with constraints
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    cycle_length = [0] * (n + 1)
    
    for start in range(1, n + 1):
        if dist[start] == float('inf'):
            dist[start] = 0
            
            # Run Bellman-Ford
            for i in range(n - 1):
                for u in range(1, n + 1):
                    for v, w in adj[u]:
                        if dist[u] != float('inf') and dist[u] + w < dist[v]:
                            dist[v] = dist[u] + w
                            parent[v] = u
                            cycle_length[v] = cycle_length[u] + 1
            
            # Check for negative cycle with constraints
            for u in range(1, n + 1):
                for v, w in adj[u]:
                    if dist[u] != float('inf') and dist[u] + w < dist[v]:
                        # Reconstruct cycle
                        cycle = []
                        visited = set()
                        current = v
                        
                        while current not in visited:
                            visited.add(current)
                            cycle.append(current)
                            current = parent[current]
                        
                        cycle_start = current
                        cycle_nodes = []
                        current = v
                        while current != cycle_start:
                            cycle_nodes.append(current)
                            current = parent[current]
                        cycle_nodes.append(cycle_start)
                        
                        final_cycle = cycle_nodes[::-1]
                        
                        # Apply constraints
                        if 'min_length' in constraints and len(final_cycle) < constraints['min_length']:
                            continue
                        if 'max_length' in constraints and len(final_cycle) > constraints['max_length']:
                            continue
                        if 'min_cost' in constraints and dist[v] > constraints['min_cost']:
                            continue
                        
                        return True, final_cycle
    
    return False, None
```

#### **Variation 3: Cycle Finding with Probabilities**
**Problem**: Each edge has a probability of existing, find expected negative cycle.
```python
def probabilistic_cycle_finding(n, m, edges, probabilities):
    # probabilities[(a, b)] = probability that edge (a, b) exists
    
    # Use Monte Carlo simulation
    import random
    
    def simulate_cycle_finding():
        # Randomly sample edges based on probabilities
        sampled_edges = []
        for a, b, w in edges:
            if random.random() < probabilities.get((a, b), 1.0):
                sampled_edges.append((a, b, w))
        
        # Build adjacency list for sampled edges
        adj = [[] for _ in range(n + 1)]
        for a, b, w in sampled_edges:
            adj[a].append((b, w))
        
        # Bellman-Ford
        dist = [float('inf')] * (n + 1)
        parent = [-1] * (n + 1)
        
        for start in range(1, n + 1):
            if dist[start] == float('inf'):
                dist[start] = 0
                
                for i in range(n - 1):
                    for u in range(1, n + 1):
                        for v, w in adj[u]:
                            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                                dist[v] = dist[u] + w
                                parent[v] = u
                
                # Check for negative cycle
                for u in range(1, n + 1):
                    for v, w in adj[u]:
                        if dist[u] != float('inf') and dist[u] + w < dist[v]:
                            return True, v
        
        return False, None
    
    # Run multiple simulations
    num_simulations = 1000
    cycle_count = 0
    total_cycle_cost = 0
    
    for _ in range(num_simulations):
        has_cycle, cycle_node = simulate_cycle_finding()
        if has_cycle:
            cycle_count += 1
            # Calculate cycle cost (simplified)
            total_cycle_cost += abs(dist[cycle_node]) if cycle_node else 0
    
    expected_cycle_probability = cycle_count / num_simulations
    expected_cycle_cost = total_cycle_cost / num_simulations if cycle_count > 0 else 0
    
    return expected_cycle_probability, expected_cycle_cost
```

#### **Variation 4: Cycle Finding with Multiple Criteria**
**Problem**: Find negative cycle considering multiple criteria (cost, length, node count).
```python
def multi_criteria_cycle_finding(n, m, edges, criteria):
    # criteria = {'cost_weight': x, 'length_weight': y, 'node_weight': z}
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        adj[a].append((b, w))
    
    # Bellman-Ford with multi-criteria tracking
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    cycle_length = [0] * (n + 1)
    node_count = [0] * (n + 1)
    
    best_cycle = None
    best_score = float('inf')
    
    for start in range(1, n + 1):
        if dist[start] == float('inf'):
            dist[start] = 0
            
            # Run Bellman-Ford
            for i in range(n - 1):
                for u in range(1, n + 1):
                    for v, w in adj[u]:
                        if dist[u] != float('inf') and dist[u] + w < dist[v]:
                            dist[v] = dist[u] + w
                            parent[v] = u
                            cycle_length[v] = cycle_length[u] + 1
                            node_count[v] = node_count[u] + 1
            
            # Check for negative cycle
            for u in range(1, n + 1):
                for v, w in adj[u]:
                    if dist[u] != float('inf') and dist[u] + w < dist[v]:
                        # Reconstruct cycle
                        cycle = []
                        visited = set()
                        current = v
                        
                        while current not in visited:
                            visited.add(current)
                            cycle.append(current)
                            current = parent[current]
                        
                        cycle_start = current
                        cycle_nodes = []
                        current = v
                        while current != cycle_start:
                            cycle_nodes.append(current)
                            current = parent[current]
                        cycle_nodes.append(cycle_start)
                        
                        final_cycle = cycle_nodes[::-1]
                        
                        # Calculate multi-criteria score
                        cost_score = abs(dist[v]) * criteria.get('cost_weight', 1)
                        length_score = len(final_cycle) * criteria.get('length_weight', 1)
                        node_score = len(set(final_cycle)) * criteria.get('node_weight', 1)
                        
                        total_score = cost_score + length_score + node_score
                        
                        if total_score < best_score:
                            best_score = total_score
                            best_cycle = final_cycle
    
    return best_cycle is not None, best_cycle, best_score
```

#### **Variation 5: Cycle Finding with Dynamic Updates**
**Problem**: Handle dynamic updates to edges and find negative cycles after each update.
```python
def dynamic_cycle_finding(n, m, initial_edges, updates):
    # updates = [(edge_index, new_weight), ...]
    
    edges = initial_edges.copy()
    results = []
    
    for edge_index, new_weight in updates:
        # Update edge weight
        a, b, old_weight = edges[edge_index]
        edges[edge_index] = (a, b, new_weight)
        
        # Rebuild adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b, w in edges:
            adj[a].append((b, w))
        
        # Bellman-Ford
        dist = [float('inf')] * (n + 1)
        parent = [-1] * (n + 1)
        
        has_cycle = False
        cycle_nodes = None
        
        for start in range(1, n + 1):
            if dist[start] == float('inf'):
                dist[start] = 0
                
                for i in range(n - 1):
                    for u in range(1, n + 1):
                        for v, w in adj[u]:
                            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                                dist[v] = dist[u] + w
                                parent[v] = u
                
                # Check for negative cycle
                for u in range(1, n + 1):
                    for v, w in adj[u]:
                        if dist[u] != float('inf') and dist[u] + w < dist[v]:
                            # Reconstruct cycle
                            cycle = []
                            visited = set()
                            current = v
                            
                            while current not in visited:
                                visited.add(current)
                                cycle.append(current)
                                current = parent[current]
                            
                            cycle_start = current
                            cycle_nodes = []
                            current = v
                            while current != cycle_start:
                                cycle_nodes.append(current)
                                current = parent[current]
                            cycle_nodes.append(cycle_start)
                            
                            has_cycle = True
                            cycle_nodes = cycle_nodes[::-1]
                            break
                    
                    if has_cycle:
                        break
                
                if has_cycle:
                    break
        
        results.append((has_cycle, cycle_nodes))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Cycle Detection Problems**
- **Negative Cycle Detection**: Find cycles with negative total weight
- **Positive Cycle Detection**: Find cycles with positive total weight
- **Zero Cycle Detection**: Find cycles with zero total weight
- **Cycle Enumeration**: Enumerate all cycles in a graph

#### **2. Shortest Path Problems**
- **Bellman-Ford Algorithm**: Handle negative weights and detect cycles
- **Dijkstra's Algorithm**: Find shortest paths in positive weighted graphs
- **Floyd-Warshall Algorithm**: All-pairs shortest paths
- **Negative Weight Handling**: Algorithms for negative weights

#### **3. Graph Analysis Problems**
- **Graph Connectivity**: Analyze graph connectivity
- **Component Analysis**: Analyze graph components
- **Path Analysis**: Analyze paths in graphs
- **Cycle Analysis**: Analyze cycles in graphs

#### **4. Algorithmic Techniques**
- **Bellman-Ford**: Algorithm for shortest paths with negative weights
- **Cycle Reconstruction**: Reconstruct cycles from parent arrays
- **Path Tracking**: Track paths during algorithm execution
- **State Management**: Manage algorithm state

#### **5. Mathematical Concepts**
- **Graph Theory**: Properties of graphs and cycles
- **Cycle Theory**: Mathematical theory of cycles
- **Path Theory**: Mathematical theory of paths
- **Algorithm Analysis**: Analysis of graph algorithms

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b, w = map(int, input().split())
        edges.append((a, b, w))
    
    has_cycle, cycle = find_negative_cycle(n, m, edges)
    if has_cycle:
        print("YES")
        print(*cycle)
    else:
        print("NO")
```

#### **2. Range Queries on Cycle Properties**
```python
def range_cycle_queries(n, edges, queries):
    # queries = [(start_node, end_node), ...] - find cycles in range
    
    results = []
    for start, end in queries:
        # Filter edges in range
        range_edges = [(a, b, w) for a, b, w in edges if start <= a <= end and start <= b <= end]
        
        has_cycle, cycle = find_negative_cycle(end - start + 1, len(range_edges), range_edges)
        results.append((has_cycle, cycle))
    
    return results
```

#### **3. Interactive Cycle Detection Problems**
```python
def interactive_cycle_finding():
    n = int(input("Enter number of nodes: "))
    m = int(input("Enter number of edges: "))
    print("Enter edges (from to weight):")
    edges = []
    for _ in range(m):
        a, b, w = map(int, input().split())
        edges.append((a, b, w))
    
    has_cycle, cycle = find_negative_cycle(n, m, edges)
    if has_cycle:
        print(f"Negative cycle found: {cycle}")
    else:
        print("No negative cycle found")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Cycle Properties**: Properties of cycles in graphs
- **Negative Cycle Theory**: Mathematical theory of negative cycles
- **Graph Decomposition**: Decomposing graphs into cycles
- **Cycle Analysis**: Analysis of cycle structures

#### **2. Algorithm Theory**
- **Bellman-Ford Theory**: Mathematical theory of Bellman-Ford algorithm
- **Cycle Detection Theory**: Mathematical theory of cycle detection
- **Path Reconstruction**: Mathematical path reconstruction
- **Algorithm Complexity**: Complexity analysis of cycle algorithms

#### **3. Optimization Theory**
- **Cycle Optimization**: Optimizing cycle properties
- **Path Optimization**: Optimizing path properties
- **Graph Optimization**: Optimizing graph properties
- **Multi-Criteria Optimization**: Multi-criteria optimization in graphs

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Bellman-Ford Algorithm**: Algorithm for shortest paths with negative weights
- **Cycle Detection Algorithms**: Various cycle detection algorithms
- **Graph Traversal**: Graph traversal algorithms
- **Path Finding**: Path finding algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Cycle Theory**: Mathematical theory of cycles
- **Algorithm Analysis**: Analysis of algorithm complexity
- **Optimization Theory**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Graph Representations**: Efficient graph representations
- **Algorithm Implementation**: Efficient algorithm implementations
- **Data Structures**: Data structures for graph algorithms
- **Dynamic Programming**: Dynamic programming techniques

---

*This analysis demonstrates efficient cycle detection techniques and shows various extensions for cycle finding problems.* 