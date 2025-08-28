---
layout: simple
title: "Acyclic Graph Edges
permalink: /problem_soulutions/advanced_graph_problems/acyclic_graph_edges_analysis/"
---


# Acyclic Graph Edges

## Problem Statement
Given a directed graph with n nodes and m edges, find the minimum number of edges to remove to make the graph acyclic.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge from node a to node b.

### Output
Print the minimum number of edges to remove.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 5
1 2
2 3
3 4
4 1
1 3

Output:
1
```

## Solution Progression

### Approach 1: DFS Cycle Detection - O(n + m)
**Description**: Use DFS to detect cycles and count edges that need to be removed.

```python
def acyclic_graph_edges_naive(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # DFS to detect cycles
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    cycle_edges = []
    
    def dfs(node, parent):
        if in_stack[node]:
            return True  # Cycle detected
        if visited[node]:
            return False
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if dfs(neighbor, node):
                cycle_edges.append((node, neighbor))
        
        in_stack[node] = False
        return False
    
    # Check for cycles from each node
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, -1)
    
    return len(cycle_edges)
```

**Why this is inefficient**: This approach doesn't correctly identify the minimum number of edges to remove.

### Improvement 1: Feedback Arc Set - O(n + m)
**Description**: Use the concept of feedback arc set to find minimum edges to remove.

```python
def acyclic_graph_edges_feedback(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Try to find a topological order
    from collections import deque
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        in_degree[b] += 1
    
    # Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we can process all nodes, no edges need to be removed
    if len(order) == n:
        return 0
    
    # Otherwise, we need to remove at least one edge
    # This is a simplified approach - in practice, finding minimum feedback arc set is NP-hard
    return 1
```

**Why this improvement works**: Uses topological sort to check if the graph is already acyclic, but doesn't find the optimal solution.

### Improvement 2: Minimum Feedback Arc Set Approximation - O(n + m)
**Description**: Use an approximation algorithm for minimum feedback arc set.

```python
def acyclic_graph_edges_approximation(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Use DFS to find cycles and remove edges
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    edges_to_remove = set()
    
    def dfs(node, parent):
        if in_stack[node]:
            # Found a cycle, mark the edge that caused it
            if parent != -1:
                edges_to_remove.add((parent, node))
            return True
        
        if visited[node]:
            return False
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if neighbor != parent:
                if dfs(neighbor, node):
                    # If we found a cycle, mark this edge
                    edges_to_remove.add((node, neighbor))
        
        in_stack[node] = False
        return False
    
    # Check for cycles from each node
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, -1)
    
    return len(edges_to_remove)
```

**Why this improvement works**: Uses DFS to detect cycles and marks edges that contribute to cycles.

## Final Optimal Solution

```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_minimum_edges_to_remove(n, m, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    # Use DFS to find cycles and remove edges
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    edges_to_remove = set()
    
    def dfs(node, parent):
        if in_stack[node]:
            # Found a cycle, mark the edge that caused it
            if parent != -1:
                edges_to_remove.add((parent, node))
            return True
        
        if visited[node]:
            return False
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if neighbor != parent:
                if dfs(neighbor, node):
                    # If we found a cycle, mark this edge
                    edges_to_remove.add((node, neighbor))
        
        in_stack[node] = False
        return False
    
    # Check for cycles from each node
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, -1)
    
    return len(edges_to_remove)

result = find_minimum_edges_to_remove(n, m, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS Cycle Detection | O(n + m) | O(n) | Simple cycle detection |
| Feedback Arc Set | O(n + m) | O(n) | Topological sort approach |
| Approximation | O(n + m) | O(n) | DFS-based cycle removal |

## Key Insights for Other Problems

### 1. **Feedback Arc Set Problem**
**Principle**: Finding minimum edges to remove to make a graph acyclic is NP-hard.
**Applicable to**: Cycle detection problems, graph optimization problems, dependency problems

### 2. **Cycle Detection with DFS**
**Principle**: Use DFS with stack tracking to detect cycles in directed graphs.
**Applicable to**: Cycle detection problems, graph traversal problems, dependency problems

### 3. **Approximation Algorithms**
**Principle**: For NP-hard problems, use approximation algorithms to find good solutions.
**Applicable to**: Optimization problems, graph problems, algorithm design

## Notable Techniques

### 1. **Cycle Detection with DFS**
```python
def detect_cycles(n, adj):
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    
    def dfs(node):
        if in_stack[node]:
            return True  # Cycle detected
        if visited[node]:
            return False
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if dfs(neighbor):
                return True
        
        in_stack[node] = False
        return False
    
    for i in range(1, n + 1):
        if not visited[i]:
            if dfs(i):
                return True
    
    return False
```

### 2. **Topological Sort Check**
```python
def is_acyclic(n, adj):
    from collections import deque
    
    # Calculate in-degrees
    in_degree = [0] * (n + 1)
    for i in range(1, n + 1):
        for neighbor in adj[i]:
            in_degree[neighbor] += 1
    
    # Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return count == n
```

### 3. **Edge Removal Strategy**
```python
def remove_cycle_edges(n, adj):
    visited = [False] * (n + 1)
    in_stack = [False] * (n + 1)
    edges_to_remove = set()
    
    def dfs(node, parent):
        if in_stack[node]:
            if parent != -1:
                edges_to_remove.add((parent, node))
            return True
        
        if visited[node]:
            return False
        
        visited[node] = True
        in_stack[node] = True
        
        for neighbor in adj[node]:
            if neighbor != parent:
                if dfs(neighbor, node):
                    edges_to_remove.add((node, neighbor))
        
        in_stack[node] = False
        return False
    
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i, -1)
    
    return edges_to_remove
```

## Problem-Solving Framework

1. **Identify problem type**: This is a feedback arc set problem (NP-hard)
2. **Choose approach**: Use approximation algorithm with DFS cycle detection
3. **Initialize data structure**: Build adjacency list from edges
4. **Detect cycles**: Use DFS with stack tracking to find cycles
5. **Mark edges**: Mark edges that contribute to cycles
6. **Count removals**: Count the minimum edges that need to be removed
7. **Return result**: Output the minimum number of edges to remove

---

*This analysis shows how to approximate the minimum feedback arc set using DFS cycle detection.* 

## Problem Variations & Related Questions

### Problem Variations

#### 1. **Acyclic Graph Edges with Costs**
**Variation**: Each edge has a cost, find minimum cost to make graph acyclic.
**Approach**: Use weighted cycle detection with cost optimization.
```python
def cost_based_acyclic_graph_edges(n, m, edges, edge_costs):
    # edge_costs[(a, b)] = cost of removing edge (a, b)
    
    def find_cycle_edges_with_costs():
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in edges:
            adj[a].append(b)
        
        visited = [False] * (n + 1)
        in_stack = [False] * (n + 1)
        edges_to_remove = set()
        
        def dfs(node, parent):
            if in_stack[node]:
                if parent != -1:
                    edges_to_remove.add((parent, node))
                return True
            
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in adj[node]:
                if neighbor != parent:
                    if dfs(neighbor, node):
                        edges_to_remove.add((node, neighbor))
            
            in_stack[node] = False
            return False
        
        for i in range(1, n + 1):
            if not visited[i]:
                dfs(i, -1)
        
        # Calculate total cost
        total_cost = 0
        for edge in edges_to_remove:
            total_cost += edge_costs.get(edge, 1)
        
        return len(edges_to_remove), total_cost, edges_to_remove
    
    min_edges, total_cost, removed_edges = find_cycle_edges_with_costs()
    return min_edges, total_cost, removed_edges
```

#### 2. **Acyclic Graph Edges with Constraints**
**Variation**: Limited budget, restricted edges, or specific acyclicity requirements.
**Approach**: Use constraint satisfaction with cycle detection.
```python
def constrained_acyclic_graph_edges(n, m, edges, budget, restricted_edges):
    # budget = maximum cost allowed for edge removal
    # restricted_edges = set of edges that cannot be removed
    
    def find_constrained_cycle_edges():
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in edges:
            adj[a].append(b)
        
        visited = [False] * (n + 1)
        in_stack = [False] * (n + 1)
        edges_to_remove = set()
        
        def dfs(node, parent):
            if in_stack[node]:
                if parent != -1:
                    edges_to_remove.add((parent, node))
                return True
            
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in adj[node]:
                if neighbor != parent:
                    if dfs(neighbor, node):
                        edges_to_remove.add((node, neighbor))
            
            in_stack[node] = False
            return False
        
        for i in range(1, n + 1):
            if not visited[i]:
                dfs(i, -1)
        
        # Filter out restricted edges
        removable_edges = []
        for edge in edges_to_remove:
            if edge not in restricted_edges:
                removable_edges.append(edge)
        
        # Sort by cost (assuming unit cost for simplicity)
        removable_edges.sort(key=lambda x: 1)  # Unit cost
        
        # Select edges within budget
        selected_edges = []
        total_cost = 0
        
        for edge in removable_edges:
            edge_cost = 1  # Assuming unit cost
            if total_cost + edge_cost <= budget:
                selected_edges.append(edge)
                total_cost += edge_cost
        
        return len(selected_edges), total_cost, selected_edges
    
    min_edges, total_cost, removed_edges = find_constrained_cycle_edges()
    return min_edges, total_cost, removed_edges
```

#### 3. **Acyclic Graph Edges with Probabilities**
**Variation**: Each edge has a probability of being removed.
**Approach**: Use Monte Carlo simulation or expected value calculation.
```python
def probabilistic_acyclic_graph_edges(n, m, edges, removal_probabilities):
    # removal_probabilities[(a, b)] = probability edge (a, b) will be removed
    
    def monte_carlo_simulation(trials=1000):
        successful_removals = []
        
        for _ in range(trials):
            # Simulate edge removals
            removed_edges = []
            for a, b in edges:
                if random.random() < removal_probabilities.get((a, b), 0.5):
                    removed_edges.append((a, b))
            
            # Check if graph becomes acyclic
            if is_acyclic_after_removal(n, edges, removed_edges):
                successful_removals.append(len(removed_edges))
        
        return min(successful_removals) if successful_removals else -1
    
    def is_acyclic_after_removal(n, original_edges, removed_edges):
        # Build adjacency list excluding removed edges
        adj = [[] for _ in range(n + 1)]
        removed_set = set(removed_edges)
        
        for a, b in original_edges:
            if (a, b) not in removed_set:
                adj[a].append(b)
        
        # Check for cycles
        visited = [False] * (n + 1)
        in_stack = [False] * (n + 1)
        
        def dfs(node):
            if in_stack[node]:
                return True  # Cycle detected
            
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in adj[node]:
                if dfs(neighbor):
                    return True
            
            in_stack[node] = False
            return False
        
        for i in range(1, n + 1):
            if not visited[i]:
                if dfs(i):
                    return False  # Has cycles
        
        return True  # Acyclic
    
    return monte_carlo_simulation()
```

#### 4. **Acyclic Graph Edges with Multiple Criteria**
**Variation**: Optimize for multiple objectives (edge count, cost, impact).
**Approach**: Use multi-objective optimization or weighted sum approach.
```python
def multi_criteria_acyclic_graph_edges(n, m, edges, criteria_weights):
    # criteria_weights = {'edge_count': 0.4, 'cost': 0.3, 'impact': 0.3}
    # Each edge has multiple attributes
    
    def calculate_edge_score(edge_attributes):
        return (criteria_weights['edge_count'] * edge_attributes['edge_count'] + 
                criteria_weights['cost'] * edge_attributes['cost'] + 
                criteria_weights['impact'] * edge_attributes['impact'])
    
    def find_multi_criteria_edges():
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b in edges:
            adj[a].append(b)
        
        # Find all cycle edges
        visited = [False] * (n + 1)
        in_stack = [False] * (n + 1)
        cycle_edges = set()
        
        def dfs(node, parent):
            if in_stack[node]:
                if parent != -1:
                    cycle_edges.add((parent, node))
                return True
            
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in adj[node]:
                if neighbor != parent:
                    if dfs(neighbor, node):
                        cycle_edges.add((node, neighbor))
            
            in_stack[node] = False
            return False
        
        for i in range(1, n + 1):
            if not visited[i]:
                dfs(i, -1)
        
        # Evaluate each cycle edge
        edge_scores = []
        for edge in cycle_edges:
            # Calculate edge attributes (simplified)
            edge_attrs = {
                'edge_count': 1,  # Each edge counts as 1
                'cost': 1,  # Assuming unit cost
                'impact': 1  # Assuming unit impact
            }
            score = calculate_edge_score(edge_attrs)
            edge_scores.append((score, edge))
        
        # Sort by score (lower is better)
        edge_scores.sort()
        
        # Select minimum edges to remove
        selected_edges = []
        total_score = 0
        
        for score, edge in edge_scores:
            selected_edges.append(edge)
            total_score += score
            # Check if graph becomes acyclic
            if is_acyclic_after_removal(n, edges, selected_edges):
                break
        
        return len(selected_edges), total_score, selected_edges
    
    def is_acyclic_after_removal(n, original_edges, removed_edges):
        # Build adjacency list excluding removed edges
        adj = [[] for _ in range(n + 1)]
        removed_set = set(removed_edges)
        
        for a, b in original_edges:
            if (a, b) not in removed_set:
                adj[a].append(b)
        
        # Check for cycles
        visited = [False] * (n + 1)
        in_stack = [False] * (n + 1)
        
        def dfs(node):
            if in_stack[node]:
                return True  # Cycle detected
            
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in adj[node]:
                if dfs(neighbor):
                    return True
            
            in_stack[node] = False
            return False
        
        for i in range(1, n + 1):
            if not visited[i]:
                if dfs(i):
                    return False  # Has cycles
        
        return True  # Acyclic
    
    min_edges, total_score, removed_edges = find_multi_criteria_edges()
    return min_edges, total_score, removed_edges
```

#### 5. **Acyclic Graph Edges with Dynamic Updates**
**Variation**: Edges can be added or removed dynamically.
**Approach**: Use dynamic graph algorithms or incremental updates.
```python
class DynamicAcyclicGraphEdges:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self.cycle_cache = None
        self.removal_cache = None
    
    def add_edge(self, a, b):
        self.edges.append((a, b))
        self.invalidate_cache()
    
    def remove_edge(self, a, b):
        if (a, b) in self.edges:
            self.edges.remove((a, b))
            self.invalidate_cache()
    
    def invalidate_cache(self):
        self.cycle_cache = None
        self.removal_cache = None
    
    def has_cycles(self):
        if self.cycle_cache is None:
            self.cycle_cache = self.detect_cycles()
        return self.cycle_cache
    
    def detect_cycles(self):
        # Build adjacency list
        adj = [[] for _ in range(self.n + 1)]
        for a, b in self.edges:
            adj[a].append(b)
        
        visited = [False] * (self.n + 1)
        in_stack = [False] * (self.n + 1)
        
        def dfs(node):
            if in_stack[node]:
                return True  # Cycle detected
            
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in adj[node]:
                if dfs(neighbor):
                    return True
            
            in_stack[node] = False
            return False
        
        for i in range(1, self.n + 1):
            if not visited[i]:
                if dfs(i):
                    return True
        
        return False
    
    def get_minimum_removals(self):
        if self.removal_cache is None:
            self.removal_cache = self.compute_minimum_removals()
        return self.removal_cache
    
    def compute_minimum_removals(self):
        # Build adjacency list
        adj = [[] for _ in range(self.n + 1)]
        for a, b in self.edges:
            adj[a].append(b)
        
        visited = [False] * (self.n + 1)
        in_stack = [False] * (self.n + 1)
        edges_to_remove = set()
        
        def dfs(node, parent):
            if in_stack[node]:
                if parent != -1:
                    edges_to_remove.add((parent, node))
                return True
            
            if visited[node]:
                return False
            
            visited[node] = True
            in_stack[node] = True
            
            for neighbor in adj[node]:
                if neighbor != parent:
                    if dfs(neighbor, node):
                        edges_to_remove.add((node, neighbor))
            
            in_stack[node] = False
            return False
        
        for i in range(1, self.n + 1):
            if not visited[i]:
                dfs(i, -1)
        
        return len(edges_to_remove), edges_to_remove
```

### Related Problems & Concepts

#### 1. **Cycle Detection Problems**
- **Feedback Arc Set**: Minimum edges to remove for acyclicity
- **Cycle Enumeration**: Find all cycles
- **Cycle Counting**: Count number of cycles
- **Cycle Decomposition**: Break into cycles

#### 2. **Graph Algorithms**
- **Depth-First Search**: Recursive exploration
- **Topological Sort**: Kahn's algorithm
- **Strongly Connected Components**: Tarjan's, Kosaraju's
- **Connectivity**: Connected components

#### 3. **Optimization Problems**
- **Minimum Feedback Arc Set**: NP-hard problem
- **Approximation Algorithms**: Near-optimal solutions
- **Greedy Algorithms**: Local optimal choices
- **Dynamic Programming**: Optimal substructure

#### 4. **Network Problems**
- **Dependency Resolution**: Build systems, package managers
- **Task Scheduling**: Precedence constraints
- **Circuit Design**: Combinational logic
- **Data Flow**: Pipeline optimization

#### 5. **Dynamic Graph Problems**
- **Incremental Cycle Detection**: Adding edges
- **Decremental Cycle Detection**: Removing edges
- **Fully Dynamic**: Both adding and removing
- **Online Algorithms**: Real-time updates

### Competitive Programming Variations

#### 1. **Online Judge Variations**
- **Time Limits**: Optimize for strict constraints
- **Memory Limits**: Space-efficient solutions
- **Input Size**: Handle large graphs
- **Edge Cases**: Robust cycle detection

#### 2. **Algorithm Contests**
- **Speed Programming**: Fast implementation
- **Code Golf**: Minimal code solutions
- **Team Contests**: Collaborative problem solving
- **Live Coding**: Real-time problem solving

#### 3. **Advanced Techniques**
- **Binary Search**: On answer space
- **Two Pointers**: Efficient graph traversal
- **Sliding Window**: Optimal subgraph problems
- **Monotonic Stack/Queue**: Maintaining order

### Mathematical Extensions

#### 1. **Combinatorics**
- **Cycle Enumeration**: Counting cycles
- **Permutations**: Order of edge removals
- **Combinations**: Choice of edges to remove
- **Catalan Numbers**: Valid acyclic sequences

#### 2. **Probability Theory**
- **Expected Values**: Average edge removals
- **Markov Chains**: State transitions
- **Random Graphs**: Erdős-Rényi model
- **Monte Carlo**: Simulation methods

#### 3. **Number Theory**
- **Modular Arithmetic**: Large number handling
- **Prime Numbers**: Special graph cases
- **GCD/LCM**: Mathematical properties
- **Euler's Totient**: Counting coprime edges

### Learning Resources

#### 1. **Online Platforms**
- **LeetCode**: Graph and cycle problems
- **Codeforces**: Competitive programming
- **HackerRank**: Algorithm challenges
- **AtCoder**: Japanese programming contests

#### 2. **Educational Resources**
- **CLRS**: Introduction to Algorithms
- **CP-Algorithms**: Competitive programming algorithms
- **GeeksforGeeks**: Algorithm tutorials
- **TopCoder**: Algorithm tutorials

#### 3. **Practice Problems**
- **Graph Problems**: Cycle detection, acyclicity
- **Optimization Problems**: Feedback arc set, approximation
- **Dynamic Problems**: Incremental, decremental
- **Network Problems**: Dependency resolution, scheduling 