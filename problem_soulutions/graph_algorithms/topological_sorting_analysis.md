---
layout: simple
title: CSES Topological Sorting - Problem Analysis
permalink: /problem_soulutions/graph_algorithms/topological_sorting_analysis/
---

# CSES Topological Sorting - Problem Analysis

## Problem Statement
Given a directed acyclic graph (DAG) with n nodes and m edges, find a topological ordering of the nodes. A topological ordering is a linear ordering of vertices such that for every directed edge (u, v), vertex u comes before vertex v in the ordering.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge from node a to node b.

### Output
Print a valid topological ordering of the nodes.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
5 4
1 2
2 3
1 3
4 5

Output:
1 4 2 5 3
```

## Solution Progression

### Approach 1: DFS with Finish Times - O(n + m)
**Description**: Use DFS to get topological ordering based on finish times.

```python
def topological_sorting_naive(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS to get topological order
    visited = [False] * (n + 1)
    finish_order = []
    
    def dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
    
    return finish_order[::-1]
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Kahn's Algorithm - O(n + m)
**Description**: Use Kahn's algorithm (BFS-based) for topological sorting.

```python
from collections import deque

def topological_sorting_optimized(n, m, edges):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return topo_order
```

**Why this improvement works**: We use Kahn's algorithm which processes nodes in order of their in-degrees, ensuring topological ordering.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_topological_sorting(n, m, edges):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return topo_order

result = find_topological_sorting(n, m, edges)
print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS with Finish Times | O(n + m) | O(n) | Use DFS to get finish order |
| Kahn's Algorithm | O(n + m) | O(n) | Use BFS with in-degree tracking |

## Key Insights for Other Problems

### 1. **Topological Sorting**
**Principle**: Use Kahn's algorithm or DFS to find topological ordering of DAG nodes.
**Applicable to**: DAG problems, ordering problems, dependency problems

### 2. **Kahn's Algorithm**
**Principle**: Process nodes in order of their in-degrees to ensure topological ordering.
**Applicable to**: Topological sorting problems, dependency resolution problems

### 3. **In-Degree Tracking**
**Principle**: Track in-degrees of nodes to determine processing order in DAGs.
**Applicable to**: DAG problems, dependency problems, ordering problems

## Notable Techniques

### 1. **Kahn's Algorithm Implementation**
```python
def kahns_algorithm(n, edges):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Process nodes with zero in-degree
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return topo_order
```

### 2. **In-Degree Calculation**
```python
def calculate_in_degrees(edges, n):
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        in_degree[b] += 1
    
    return in_degree
```

### 3. **DFS Topological Sort**
```python
def dfs_topological_sort(adj, n):
    visited = [False] * (n + 1)
    finish_order = []
    
    def dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)
        finish_order.append(node)
    
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)
    
    return finish_order[::-1]
```

## Problem-Solving Framework

1. **Identify problem type**: This is a topological sorting problem
2. **Choose approach**: Use Kahn's algorithm or DFS
3. **Build graph**: Create adjacency list and calculate in-degrees
4. **Initialize queue**: Add nodes with zero in-degree
5. **Process nodes**: Remove nodes and update in-degrees
6. **Build order**: Collect nodes in topological order
7. **Return result**: Output topological ordering

---

*This analysis shows how to efficiently find topological ordering using Kahn's algorithm.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Topological Sorting with Costs**
**Problem**: Each edge has a cost, find topological order with minimum total cost.
```python
def cost_based_topological_sorting(n, edges, costs):
    # costs[(a, b)] = cost of edge from a to b
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append((b, costs.get((a, b), 0)))
        in_degree[b] += 1
    
    # Process nodes with zero in-degree
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    total_cost = 0
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor, cost in adj[node]:
            total_cost += cost
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return topo_order, total_cost
```

#### **Variation 2: Topological Sorting with Constraints**
**Problem**: Find topological order with constraints on node ordering.
```python
def constrained_topological_sorting(n, edges, constraints):
    # constraints = [(a, b), ...] where a must come before b in any valid order
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Add constraint edges
    for a, b in constraints:
        if b not in adj[a]:  # Avoid duplicate edges
            adj[a].append(b)
            in_degree[b] += 1
    
    # Process nodes with zero in-degree
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return topo_order if len(topo_order) == n else None
```

#### **Variation 3: Topological Sorting with Probabilities**
**Problem**: Each edge has a probability of existing, find expected topological order.
```python
def probabilistic_topological_sorting(n, edges, probabilities):
    # probabilities[(a, b)] = probability that edge from a to b exists
    
    # Build adjacency list with probabilities
    adj = [[] for _ in range(n + 1)]
    
    for a, b in edges:
        prob = probabilities.get((a, b), 1.0)
        adj[a].append((b, prob))
    
    # Use Monte Carlo simulation
    import random
    
    def simulate_topological_sort():
        # Randomly sample edges based on probabilities
        sampled_edges = []
        for a, b in edges:
            if random.random() < probabilities.get((a, b), 1.0):
                sampled_edges.append((a, b))
        
        # Build in-degree count for sampled edges
        in_degree = [0] * (n + 1)
        for a, b in sampled_edges:
            in_degree[b] += 1
        
        # Kahn's algorithm
        from collections import deque
        queue = deque()
        for i in range(1, n + 1):
            if in_degree[i] == 0:
                queue.append(i)
        
        topo_order = []
        while queue:
            node = queue.popleft()
            topo_order.append(node)
            
            for a, b in sampled_edges:
                if a == node:
                    in_degree[b] -= 1
                    if in_degree[b] == 0:
                        queue.append(b)
        
        return topo_order if len(topo_order) == n else None
    
    # Run multiple simulations
    num_simulations = 1000
    results = []
    for _ in range(num_simulations):
        result = simulate_topological_sort()
        if result:
            results.append(result)
    
    # Return most common ordering
    if results:
        from collections import Counter
        order_counts = Counter(tuple(order) for order in results)
        most_common = order_counts.most_common(1)[0][0]
        return list(most_common)
    
    return None
```

#### **Variation 4: Topological Sorting with Multiple Criteria**
**Problem**: Find topological order considering multiple criteria (cost, time, priority).
```python
def multi_criteria_topological_sorting(n, edges, criteria):
    # criteria = {'cost': costs, 'time': times, 'priority': priorities}
    
    # Build adjacency list with multiple criteria
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        edge_data = {
            'cost': criteria['cost'].get((a, b), 0),
            'time': criteria['time'].get((a, b), 0),
            'priority': criteria['priority'].get((a, b), 0)
        }
        adj[a].append((b, edge_data))
        in_degree[b] += 1
    
    # Process nodes with zero in-degree using priority queue
    from heapq import heappush, heappop
    
    # Priority queue based on multiple criteria
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            # Use negative priority for max heap
            heappush(queue, (-criteria['priority'].get(i, 0), i))
    
    topo_order = []
    total_cost = 0
    total_time = 0
    
    while queue:
        priority, node = heappop(queue)
        topo_order.append(node)
        
        for neighbor, edge_data in adj[node]:
            total_cost += edge_data['cost']
            total_time += edge_data['time']
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heappush(queue, (-criteria['priority'].get(neighbor, 0), neighbor))
    
    return topo_order, total_cost, total_time
```

#### **Variation 5: Topological Sorting with Dynamic Updates**
**Problem**: Handle dynamic updates to edges and find topological order after each update.
```python
def dynamic_topological_sorting(n, initial_edges, updates):
    # updates = [(edge_to_add, edge_to_remove), ...]
    
    edges = initial_edges.copy()
    results = []
    
    for edge_to_add, edge_to_remove in updates:
        # Update edges
        if edge_to_remove in edges:
            edges.remove(edge_to_remove)
        if edge_to_add:
            edges.append(edge_to_add)
        
        # Rebuild adjacency list and in-degree count
        adj = [[] for _ in range(n + 1)]
        in_degree = [0] * (n + 1)
        
        for a, b in edges:
            adj[a].append(b)
            in_degree[b] += 1
        
        # Kahn's algorithm
        from collections import deque
        queue = deque()
        for i in range(1, n + 1):
            if in_degree[i] == 0:
                queue.append(i)
        
        topo_order = []
        while queue:
            node = queue.popleft()
            topo_order.append(node)
            
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        result = topo_order if len(topo_order) == n else None
        results.append(result)
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Graph Problems**
- **Directed Acyclic Graphs**: Properties of DAGs
- **Cycle Detection**: Detect cycles in directed graphs
- **Strongly Connected Components**: Find SCCs in directed graphs
- **Graph Traversal**: BFS/DFS on directed graphs

#### **2. Ordering Problems**
- **Dependency Resolution**: Resolve dependencies between items
- **Task Scheduling**: Schedule tasks with dependencies
- **Build Systems**: Order compilation of source files
- **Course Prerequisites**: Order courses based on prerequisites

#### **3. Algorithmic Techniques**
- **Kahn's Algorithm**: BFS-based topological sorting
- **DFS Topological Sort**: DFS-based topological sorting
- **In-Degree Tracking**: Track in-degrees for processing order
- **Priority Queues**: Use priority queues for ordering

#### **4. Optimization Problems**
- **Minimum Cost Ordering**: Find minimum cost topological order
- **Multi-Criteria Optimization**: Optimize multiple objectives
- **Constraint Satisfaction**: Satisfy ordering constraints
- **Dynamic Updates**: Handle dynamic graph changes

#### **5. Mathematical Concepts**
- **Partial Orders**: Mathematical theory of partial orders
- **Linear Extensions**: Extensions of partial orders
- **Graph Theory**: Properties of directed graphs
- **Combinatorics**: Counting valid orderings

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = topological_sort(n, edges)
    if result:
        print(*result)
    else:
        print("IMPOSSIBLE")
```

#### **2. Range Queries on Topological Order**
```python
def range_topological_queries(n, edges, queries):
    # queries = [(start_node, end_node), ...] - find order in range
    
    # Precompute topological order
    topo_order = topological_sort(n, edges)
    
    results = []
    for start, end in queries:
        range_order = []
        for node in topo_order:
            if start <= node <= end:
                range_order.append(node)
        results.append(range_order)
    
    return results
```

#### **3. Interactive Topological Sorting Problems**
```python
def interactive_topological_sorting():
    n = int(input("Enter number of nodes: "))
    m = int(input("Enter number of edges: "))
    print("Enter edges (a b):")
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = topological_sort(n, edges)
    if result:
        print(f"Topological order: {result}")
    else:
        print("No valid topological order exists (cycle detected)")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **DAG Properties**: Properties of directed acyclic graphs
- **Topological Order Theory**: Mathematical theory of topological orders
- **Partial Order Theory**: Theory of partial orders and linear extensions
- **Graph Decomposition**: Decomposing graphs into components

#### **2. Order Theory**
- **Partial Orders**: Mathematical theory of partial orders
- **Linear Extensions**: Extensions of partial orders to total orders
- **Order Statistics**: Statistical properties of orderings
- **Order Enumeration**: Enumerating all valid orderings

#### **3. Combinatorics**
- **Order Counting**: Counting different topological orders
- **Permutation Analysis**: Analyzing permutations and orderings
- **Pattern Recognition**: Recognizing patterns in orderings
- **Enumeration**: Enumerating valid orderings

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Kahn's Algorithm**: BFS-based topological sorting
- **DFS Topological Sort**: DFS-based topological sorting
- **Cycle Detection**: Detect cycles in directed graphs
- **Graph Algorithms**: Various graph algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Order Theory**: Mathematical theory of orders
- **Partial Order Theory**: Theory of partial orders
- **Combinatorics**: Counting and enumeration techniques

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Queue Data Structures**: Efficient queue implementations
- **Algorithm Optimization**: Improving time and space complexity
- **Dynamic Programming**: Handling dynamic updates

---

*This analysis demonstrates efficient topological sorting techniques and shows various extensions for ordering problems.* 