---
layout: simple
title: "Mail Delivery"
permalink: /cses-analyses/problem_soulutions/graph_algorithms/mail_delivery_analysis
---


# Mail Delivery

## Problem Statement
Given an undirected graph with n nodes and m edges, find an Eulerian circuit (a path that visits every edge exactly once and returns to the starting node).

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge between nodes a and b.

### Output
Print the nodes in the order they are visited in the Eulerian circuit, or "IMPOSSIBLE" if no Eulerian circuit exists.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 4
1 2
2 3
3 4
4 1

Output:
1 2 3 4 1
```

## Solution Progression

### Approach 1: Hierholzer's Algorithm - O(n + m)
**Description**: Use Hierholzer's algorithm to find Eulerian circuit.

```python
def mail_delivery_naive(n, m, edges):
    # Check if Eulerian circuit exists
    # All vertices must have even degree
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_eulerian_circuit():
        # Start from any vertex
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                # Take an edge
                next_node = adj[current].pop()
                # Remove the reverse edge
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                # No more edges from current vertex
                path.append(stack.pop())
        
        return path[::-1]  # Reverse to get correct order
    
    circuit = find_eulerian_circuit()
    
    # Check if all edges were used
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, circuit))
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized Hierholzer's Algorithm - O(n + m)
**Description**: Use optimized Hierholzer's algorithm with better edge management.

```python
def mail_delivery_optimized(n, m, edges):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm with edge tracking
    def find_eulerian_circuit():
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, circuit))
```

**Why this improvement works**: We use Hierholzer's algorithm with optimized edge management to find Eulerian circuit efficiently.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_mail_delivery_route(n, m, edges):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if all degrees are even
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Hierholzer's algorithm
    def find_eulerian_circuit():
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    # Check if all edges were used
    if len(circuit) != m + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, circuit))

result = find_mail_delivery_route(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Hierholzer's Algorithm | O(n + m) | O(n + m) | Use Hierholzer's for Eulerian circuit |
| Optimized Hierholzer's | O(n + m) | O(n + m) | Optimized Hierholzer's implementation |

## Key Insights for Other Problems

### 1. **Eulerian Circuit**
**Principle**: Use Hierholzer's algorithm to find Eulerian circuit.
**Applicable to**: Eulerian path problems, circuit problems, graph traversal problems

### 2. **Degree Check**
**Principle**: Check if all vertices have even degree for Eulerian circuit.
**Applicable to**: Eulerian problems, graph analysis problems, connectivity problems

### 3. **Hierholzer's Algorithm**
**Principle**: Use stack-based approach to find Eulerian circuit.
**Applicable to**: Eulerian problems, circuit problems, graph problems

## Notable Techniques

### 1. **Hierholzer's Algorithm Implementation**
```python
def hierholzer_algorithm(n, adj):
    # Check if Eulerian circuit exists
    degree = [0] * (n + 1)
    for u in range(1, n + 1):
        degree[u] = len(adj[u])
    
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return None  # No Eulerian circuit
    
    # Find Eulerian circuit
    start = 1
    path = []
    stack = [start]
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node = adj[current].pop()
            adj[next_node].remove(current)
            stack.append(next_node)
        else:
            path.append(stack.pop())
    
    return path[::-1]
```

### 2. **Eulerian Circuit Check**
```python
def check_eulerian_circuit(n, adj):
    for i in range(1, n + 1):
        if len(adj[i]) % 2 != 0:
            return False
    return True
```

### 3. **Edge Management**
```python
def remove_edge(adj, u, v):
    adj[u].remove(v)
    adj[v].remove(u)
```

## Problem-Solving Framework

1. **Identify problem type**: This is an Eulerian circuit problem
2. **Choose approach**: Use Hierholzer's algorithm
3. **Check conditions**: Verify all vertices have even degree
4. **Build graph**: Create adjacency list representation
5. **Find circuit**: Use Hierholzer's algorithm to find Eulerian circuit
6. **Verify result**: Check if all edges were used
7. **Return result**: Output circuit or "IMPOSSIBLE"

---

*This analysis shows how to efficiently find Eulerian circuit using Hierholzer's algorithm.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Mail Delivery with Costs**
**Problem**: Each street has a delivery cost, find minimum cost Eulerian circuit.
```python
def cost_based_mail_delivery(n, edges, costs):
    # costs[(a, b)] = cost of delivering mail on street (a, b)
    
    # Calculate degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check Eulerian circuit conditions
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Build adjacency list with costs
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = costs.get((a, b), 0)
        adj[a].append((b, cost))
        adj[b].append((a, cost))
    
    # Use Hierholzer's algorithm with cost tracking
    start = 1
    path = []
    stack = [start]
    total_cost = 0
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node, cost = adj[current].pop()
            # Remove reverse edge
            for i, (node, _) in enumerate(adj[next_node]):
                if node == current:
                    adj[next_node].pop(i)
                    break
            stack.append(next_node)
            total_cost += cost
        else:
            path.append(stack.pop())
    
    if len(path) != len(edges) + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, path[::-1])), total_cost
```

#### **Variation 2: Mail Delivery with Constraints**
**Problem**: Find Eulerian circuit with constraints on street usage.
```python
def constrained_mail_delivery(n, edges, constraints):
    # constraints = {'max_uses': x, 'forbidden_streets': [(a, b), ...]}
    
    # Calculate degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check Eulerian circuit conditions
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        # Check if street is forbidden
        if (a, b) not in constraints.get('forbidden_streets', []):
            adj[a].append(b)
            adj[b].append(a)
    
    # Use Hierholzer's algorithm
    start = 1
    path = []
    stack = [start]
    edge_uses = {}  # Track edge usage
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node = adj[current].pop()
            edge = tuple(sorted([current, next_node]))
            
            # Check usage constraints
            if edge_uses.get(edge, 0) < constraints.get('max_uses', float('inf')):
                edge_uses[edge] = edge_uses.get(edge, 0) + 1
                # Remove reverse edge
                adj[next_node].remove(current)
                stack.append(next_node)
        else:
            path.append(stack.pop())
    
    if len(path) != len(edges) + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, path[::-1]))
```

#### **Variation 3: Mail Delivery with Probabilities**
**Problem**: Each street has a success probability, find most reliable Eulerian circuit.
```python
def probabilistic_mail_delivery(n, edges, probabilities):
    # probabilities[(a, b)] = probability that mail delivery succeeds on street (a, b)
    
    # Calculate degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check Eulerian circuit conditions
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Build adjacency list with probabilities
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        prob = probabilities.get((a, b), 0.5)
        adj[a].append((b, prob))
        adj[b].append((a, prob))
    
    # Use Hierholzer's algorithm with probability tracking
    start = 1
    path = []
    stack = [start]
    total_probability = 1.0
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node, prob = adj[current].pop()
            # Remove reverse edge
            for i, (node, _) in enumerate(adj[next_node]):
                if node == current:
                    adj[next_node].pop(i)
                    break
            stack.append(next_node)
            total_probability *= prob
        else:
            path.append(stack.pop())
    
    if len(path) != len(edges) + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, path[::-1])), total_probability
```

#### **Variation 4: Mail Delivery with Multiple Criteria**
**Problem**: Find Eulerian circuit optimizing multiple objectives (cost, time, reliability).
```python
def multi_criteria_mail_delivery(n, edges, costs, times, reliabilities):
    # costs[(a, b)] = cost, times[(a, b)] = time, reliabilities[(a, b)] = reliability
    
    # Calculate degrees
    degree = [0] * (n + 1)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    
    # Check Eulerian circuit conditions
    for i in range(1, n + 1):
        if degree[i] % 2 != 0:
            return "IMPOSSIBLE"
    
    # Normalize values
    max_cost = max(costs.values()) if costs else 1
    max_time = max(times.values()) if times else 1
    max_reliability = max(reliabilities.values()) if reliabilities else 1
    
    # Build adjacency list with weighted scores
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        cost = costs.get((a, b), 0) / max_cost
        time = times.get((a, b), 0) / max_time
        reliability = reliabilities.get((a, b), 1) / max_reliability
        
        # Weighted score (lower is better)
        score = 0.4 * cost + 0.3 * time - 0.3 * reliability
        adj[a].append((b, score))
        adj[b].append((a, score))
    
    # Sort edges by score for greedy approach
    for i in range(1, n + 1):
        adj[i].sort(key=lambda x: x[1])
    
    # Use Hierholzer's algorithm
    start = 1
    path = []
    stack = [start]
    total_cost = 0
    total_time = 0
    total_reliability = 1.0
    
    while stack:
        current = stack[-1]
        
        if adj[current]:
            next_node, score = adj[current].pop()
            # Remove reverse edge
            for i, (node, _) in enumerate(adj[next_node]):
                if node == current:
                    adj[next_node].pop(i)
                    break
            
            stack.append(next_node)
            
            # Track actual values
            edge = tuple(sorted([current, next_node]))
            total_cost += costs.get(edge, 0)
            total_time += times.get(edge, 0)
            total_reliability *= reliabilities.get(edge, 1)
        else:
            path.append(stack.pop())
    
    if len(path) != len(edges) + 1:
        return "IMPOSSIBLE"
    
    return " ".join(map(str, path[::-1])), total_cost, total_time, total_reliability
```

#### **Variation 5: Mail Delivery with Dynamic Updates**
**Problem**: Handle dynamic updates to street network and find Eulerian circuit after each update.
```python
def dynamic_mail_delivery(n, initial_edges, updates):
    # updates = [(edge_to_add, edge_to_remove), ...]
    
    edges = initial_edges.copy()
    results = []
    
    for edge_to_add, edge_to_remove in updates:
        # Update edges
        if edge_to_remove in edges:
            edges.remove(edge_to_remove)
        if edge_to_add:
            edges.append(edge_to_add)
        
        # Recompute Eulerian circuit
        # Calculate degrees
        degree = [0] * (n + 1)
        for a, b in edges:
            degree[a] += 1
            degree[b] += 1
        
        # Check Eulerian circuit conditions
        possible = True
        for i in range(1, n + 1):
            if degree[i] % 2 != 0:
                possible = False
                break
        
        if not possible:
            results.append("IMPOSSIBLE")
            continue
        
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        
        # Use Hierholzer's algorithm
        start = 1
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if adj[current]:
                next_node = adj[current].pop()
                adj[next_node].remove(current)
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        if len(path) != len(edges) + 1:
            results.append("IMPOSSIBLE")
        else:
            results.append(" ".join(map(str, path[::-1])))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Eulerian Path Problems**
- **Eulerian Circuit**: Circuit using each edge exactly once
- **Eulerian Trail**: Trail using each edge exactly once
- **Semi-Eulerian**: Graph with Eulerian trail but not circuit
- **Eulerian Graph**: Graph with Eulerian circuit

#### **2. Graph Traversal Problems**
- **Hamiltonian Path**: Path visiting each vertex exactly once
- **Hamiltonian Cycle**: Cycle visiting each vertex exactly once
- **Chinese Postman**: Find shortest closed walk using all edges
- **Traveling Salesman**: Find shortest Hamiltonian cycle

#### **3. Path Problems**
- **Shortest Path**: Find shortest path between vertices
- **All Pairs Shortest Path**: Find shortest paths between all pairs
- **K-Shortest Paths**: Find k shortest paths
- **Disjoint Paths**: Find edge-disjoint paths

#### **4. Graph Theory Problems**
- **Connectivity**: Study of graph connectivity
- **Degree Analysis**: Analyze vertex degrees
- **Graph Properties**: Study graph properties
- **Trail Theory**: Theory of trails and paths

#### **5. Algorithmic Techniques**
- **Hierholzer's Algorithm**: Find Eulerian trail/circuit
- **DFS**: Depth-first search for path finding
- **BFS**: Breadth-first search for path finding
- **Graph Algorithms**: Various graph algorithms

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Networks**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = find_mail_delivery_route(n, m, edges)
    print(result)
```

#### **2. Range Queries on Mail Delivery**
```python
def range_mail_delivery_queries(n, edges, queries):
    # queries = [(start_edge, end_edge), ...] - find circuit using edges in range
    
    results = []
    for start, end in queries: subset_edges = edges[
start: end+1]
        result = find_mail_delivery_route(n, len(subset_edges), subset_edges)
        results.append(result)
    
    return results
```

#### **3. Interactive Mail Delivery Problems**
```python
def interactive_mail_delivery():
    n, m = map(int, input("Enter n and m: ").split())
    print("Enter edges (a b):")
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = find_mail_delivery_route(n, m, edges)
    print(f"Mail delivery route: {result}")
    
    # Show the circuit
    if result != "IMPOSSIBLE":
        circuit = result.split()
        print(f"Circuit: {' -> '.join(circuit)}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Euler's Theorem**: Conditions for Eulerian trail/circuit
- **Degree Theory**: Properties of vertex degrees
- **Connectivity Theory**: Theory of graph connectivity
- **Trail Theory**: Mathematical theory of trails

#### **2. Linear Algebra**
- **Adjacency Matrix**: Matrix representation of graphs
- **Incidence Matrix**: Edge-vertex incidence matrix
- **Laplacian Matrix**: Graph Laplacian matrix
- **Spectral Graph Theory**: Study of graph eigenvalues

#### **3. Combinatorics**
- **Path Counting**: Count number of paths
- **Trail Counting**: Count number of trails
- **Graph Enumeration**: Enumerate graphs with properties
- **Permutation Theory**: Theory of permutations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Eulerian Algorithms**: Hierholzer's, Fleury's algorithms
- **Path Algorithms**: DFS, BFS, Dijkstra, Floyd-Warshall
- **Graph Algorithms**: Connectivity, traversal algorithms
- **Optimization Algorithms**: Linear programming, integer programming

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Linear Algebra**: Matrix representations of graphs
- **Combinatorics**: Combinatorial graph theory
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Path Finding**: Efficient path finding algorithms
- **Trail Construction**: Building trails from graph data
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient Eulerian circuit techniques and shows various extensions for mail delivery problems.* 