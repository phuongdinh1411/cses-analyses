---
layout: simple
title: "Tournament Graph Distribution"permalink: /problem_soulutions/counting_problems/tournament_graph_distribution_analysis
---


# Tournament Graph Distribution

## Problem Statement
Given n teams, count the number of different tournament graphs where each team plays against every other team exactly once, and the result is a valid tournament (no cycles).

### Input
The first input line has an integer n: the number of teams.

### Output
Print the number of different tournament graphs modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 20

### Example
```
Input:
3

Output:
2
```

## Solution Progression

### Approach 1: Generate All Tournaments - O(n!)
**Description**: Generate all possible tournament graphs and count valid ones.

```python
def tournament_graph_distribution_naive(n):
    MOD = 10**9 + 7
    from itertools import permutations
    
    def is_valid_tournament(edges):
        # Check for cycles using DFS
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
        
        visited = [False] * n
        rec_stack = [False] * n
        
        def has_cycle(node):
            visited[node] = True
            rec_stack[node] = True
            
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    if has_cycle(neighbor):
                        return True
                elif rec_stack[neighbor]:
                    return True
            
            rec_stack[node] = False
            return False
        
        for i in range(n):
            if not visited[i]:
                if has_cycle(i):
                    return False
        
        return True
    
    # Generate all possible edge orientations
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))
    
    count = 0
    # Try all possible orientations
    for orientation in range(2 ** len(edges)):
        tournament_edges = []
        for i, (u, v) in enumerate(edges):
            if orientation & (1 << i):
                tournament_edges.append((u, v))
            else:
                tournament_edges.append((v, u))
        
        if is_valid_tournament(tournament_edges):
            count = (count + 1) % MOD
    
    return count
```

**Why this is inefficient**: O(n!) complexity is too slow for large n.

### Improvement 1: Dynamic Programming - O(n²)
**Description**: Use DP to count valid tournament graphs.

```python
def tournament_graph_distribution_dp(n):
    MOD = 10**9 + 7
    
    # dp[i] = number of valid tournaments with i teams
    dp = [0] * (n + 1)
    
    # Base case
    dp[1] = 1
    
    # Fill DP table
    for i in range(2, n + 1):
        # For i teams, we can have any subset of i-1 teams as winners
        # and the remaining team as loser
        dp[i] = (dp[i-1] * i) % MOD
    
    return dp[n]
```

**Why this improvement works**: Uses mathematical formula for tournament counting.

### Approach 2: Mathematical Formula - O(n)
**Description**: Use mathematical formula for tournament counting.

```python
def tournament_graph_distribution_mathematical(n):
    MOD = 10**9 + 7
    
    if n == 1:
        return 1
    
    # Formula: n! / 2^(n*(n-1)/2)
    # But for valid tournaments, it's just n!
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % MOD
    
    return result
```

**Why this improvement works**: Mathematical formula gives optimal solution.

## Final Optimal Solution

```python
n = int(input())

def count_tournament_graphs(n):
    MOD = 10**9 + 7
    
    if n == 1:
        return 1
    
    # Number of valid tournaments = n!
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % MOD
    
    return result

result = count_tournament_graphs(n)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Generate All Tournaments | O(n!) | O(n²) | Simple but factorial |
| Dynamic Programming | O(n²) | O(n) | DP approach |
| Mathematical Formula | O(n) | O(1) | Optimal solution |

## Key Insights for Other Problems

### 1. **Tournament Graph Properties**
**Principle**: Valid tournaments have no cycles and represent a total ordering.
**Applicable to**: Graph theory problems, tournament problems, ordering problems

### 2. **Mathematical Counting**
**Principle**: The number of valid tournaments with n teams is n!.
**Applicable to**: Combinatorics problems, counting problems, factorial problems

### 3. **Cycle Detection**
**Principle**: Valid tournaments must be acyclic (no cycles).
**Applicable to**: Graph validation problems, cycle detection problems

## Notable Techniques

### 1. **Tournament Counting**
```python
def count_tournaments(n, MOD):
    if n == 1:
        return 1
    
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % MOD
    
    return result
```

### 2. **Cycle Detection**
```python
def has_cycle(adj, n):
    visited = [False] * n
    rec_stack = [False] * n
    
    def dfs(node):
        visited[node] = True
        rec_stack[node] = True
        
        for neighbor in adj[node]:
            if not visited[neighbor]:
                if dfs(neighbor):
                    return True
            elif rec_stack[neighbor]:
                return True
        
        rec_stack[node] = False
        return False
    
    for i in range(n):
        if not visited[i]:
            if dfs(i):
                return True
    
    return False
```

### 3. **Tournament Validation**
```python
def is_valid_tournament(edges, n):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    
    return not has_cycle(adj, n)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a tournament graph counting problem
2. **Choose approach**: Use mathematical formula
3. **Handle base case**: n = 1 case
4. **Apply formula**: Number of valid tournaments = n!
5. **Use modular arithmetic**: Handle large numbers
6. **Return result**: Output the count modulo 10^9 + 7

---

*This analysis shows how to efficiently count the distribution of tournament graph components using graph theory analysis and component counting.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Tournament Graph Distribution**
**Problem**: Each node has a weight. Find the distribution of weighted tournament graph components.
```python
def weighted_tournament_graph_distribution(n, edges, weights):
    # weights[i] = weight of node i
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    
    visited = [False] * n
    component_weights = {}
    component_count = 0
    
    def dfs(node, component_id):
        visited[node] = True
        component_weights[component_id] = component_weights.get(component_id, 0) + weights[node]
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, component_id)
    
    for i in range(n):
        if not visited[i]:
            dfs(i, component_count)
            component_count += 1
    
    return component_weights
```

#### **Variation 2: Constrained Tournament Graph Distribution**
**Problem**: Find distribution when components are constrained by maximum size.
```python
def constrained_tournament_graph_distribution(n, edges, max_component_size):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    
    visited = [False] * n
    component_sizes = {}
    component_count = 0
    
    def dfs(node, component_id):
        visited[node] = True
        component_sizes[component_id] = component_sizes.get(component_id, 0) + 1
        
        for neighbor in graph[node]:
            if not visited[neighbor] and component_sizes[component_id] < max_component_size:
                dfs(neighbor, component_id)
    
    for i in range(n):
        if not visited[i]:
            dfs(i, component_count)
            component_count += 1
    
    return component_sizes
```

#### **Variation 3: Cycle-Based Tournament Graph Distribution**
**Problem**: Find distribution based on cycle lengths in tournament graphs.
```python
def cycle_based_tournament_graph_distribution(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    
    visited = [False] * n
    cycle_lengths = {}
    component_count = 0
    
    def find_cycle_length(node, component_id):
        if visited[node]:
            return 0
        
        visited[node] = True
        cycle_length = 1
        
        for neighbor in graph[node]:
            if not visited[neighbor]:
                cycle_length += find_cycle_length(neighbor, component_id)
            else:
                # Found a cycle
                cycle_lengths[component_id] = cycle_length
        
        return cycle_length
    
    for i in range(n):
        if not visited[i]:
            find_cycle_length(i, component_count)
            component_count += 1
    
    return cycle_lengths
```

#### **Variation 4: Directed Tournament Graph Distribution**
**Problem**: Handle directed tournament graphs with specific traversal rules.
```python
def directed_tournament_graph_distribution(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    
    visited = [False] * n
    component_sizes = {}
    component_count = 0
    
    def dfs(node, component_id):
        visited[node] = True
        component_sizes[component_id] = component_sizes.get(component_id, 0) + 1
        
        # Only traverse in the direction of edges
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, component_id)
    
    for i in range(n):
        if not visited[i]:
            dfs(i, component_count)
            component_count += 1
    
    return component_sizes
```

#### **Variation 5: Dynamic Tournament Graph Updates**
**Problem**: Support dynamic updates to the graph and answer distribution queries efficiently.
```python
class DynamicTournamentGraphCounter:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.component_sizes = {}
        self.visited = [False] * n
    
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self._recompute_components()
    
    def remove_edge(self, u, v):
        if v in self.graph[u]:
            self.graph[u].remove(v)
            self._recompute_components()
    
    def _recompute_components(self):
        self.visited = [False] * self.n
        self.component_sizes = {}
        component_count = 0
        
        def dfs(node, component_id):
            self.visited[node] = True
            self.component_sizes[component_id] = self.component_sizes.get(component_id, 0) + 1
            
            for neighbor in self.graph[node]:
                if not self.visited[neighbor]:
                    dfs(neighbor, component_id)
        
        for i in range(self.n):
            if not self.visited[i]:
                dfs(i, component_count)
                component_count += 1
    
    def get_component_distribution(self):
        return self.component_sizes
```

### 🔗 **Related Problems & Concepts**

#### **1. Graph Problems**
- **Graph Traversal**: Traverse graphs efficiently
- **Component Analysis**: Analyze graph components
- **Cycle Detection**: Detect cycles in graphs
- **Graph Optimization**: Optimize graph operations

#### **2. Distribution Problems**
- **Component Distribution**: Distribute components in graphs
- **Size Distribution**: Analyze size distributions
- **Weight Distribution**: Analyze weight distributions
- **Pattern Distribution**: Analyze pattern distributions

#### **3. Tournament Problems**
- **Tournament Analysis**: Analyze tournament properties
- **Tournament Generation**: Generate tournaments efficiently
- **Tournament Optimization**: Optimize tournament algorithms
- **Tournament Mapping**: Map tournaments to graphs

#### **4. Cycle Problems**
- **Cycle Detection**: Detect cycles efficiently
- **Cycle Analysis**: Analyze cycle properties
- **Cycle Optimization**: Optimize cycle algorithms
- **Cycle Counting**: Count cycles in graphs

#### **5. Component Problems**
- **Component Counting**: Count components efficiently
- **Component Analysis**: Analyze component properties
- **Component Optimization**: Optimize component algorithms
- **Component Mapping**: Map components in graphs

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))
    
    result = tournament_graph_distribution(n, edges)
    print(len(result))
    for component_id, size in result.items():
        print(f"Component {component_id}: {size}")
```

#### **2. Range Queries**
```python
# Precompute distributions for different graph regions
def precompute_distributions(n, edges):
    # Precompute for all possible edge subsets
    distributions = {}
    
    # Generate all possible edge subsets
    m = len(edges)
    for mask in range(1 << m):
        subset_edges = []
        for i in range(m):
            if mask & (1 << i):
                subset_edges.append(edges[i])
        
        dist = tournament_graph_distribution(n, subset_edges)
        distributions[mask] = dist
    
    return distributions

# Answer range queries efficiently
def range_query(distributions, edge_mask):
    return distributions.get(edge_mask, {})
```

#### **3. Interactive Problems**
```python
# Interactive tournament graph analyzer
def interactive_tournament_analyzer():
    n = int(input("Enter number of nodes: "))
    m = int(input("Enter number of edges: "))
    edges = []
    
    print("Enter edges:")
    for i in range(m):
        u, v = map(int, input(f"Edge {i+1}: ").split())
        edges.append((u, v))
    
    print("Edges:", edges)
    
    while True:
        query = input("Enter query (distribution/weighted/constrained/cycle/directed/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "distribution":
            result = tournament_graph_distribution(n, edges)
            print(f"Component distribution: {result}")
        elif query == "weighted":
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_tournament_graph_distribution(n, edges, weights)
            print(f"Weighted distribution: {result}")
        elif query == "constrained":
            max_size = int(input("Enter max component size: "))
            result = constrained_tournament_graph_distribution(n, edges, max_size)
            print(f"Constrained distribution: {result}")
        elif query == "cycle":
            result = cycle_based_tournament_graph_distribution(n, edges)
            print(f"Cycle-based distribution: {result}")
        elif query == "directed":
            result = directed_tournament_graph_distribution(n, edges)
            print(f"Directed distribution: {result}")
        elif query == "dynamic":
            counter = DynamicTournamentGraphCounter(n)
            for u, v in edges:
                counter.add_edge(u, v)
            print(f"Initial distribution: {counter.get_component_distribution()}")
            
            while True:
                cmd = input("Enter command (add/remove/distribution/back): ")
                if cmd == "back":
                    break
                elif cmd == "add":
                    u, v = map(int, input("Enter edge to add: ").split())
                    counter.add_edge(u, v)
                    print("Edge added")
                elif cmd == "remove":
                    u, v = map(int, input("Enter edge to remove: ").split())
                    counter.remove_edge(u, v)
                    print("Edge removed")
                elif cmd == "distribution":
                    result = counter.get_component_distribution()
                    print(f"Current distribution: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **Component Theory**: Mathematical theory of graph components
- **Cycle Theory**: Properties of cycles in graphs
- **Tournament Theory**: Properties of tournament graphs
- **Distribution Theory**: Mathematical properties of distributions

#### **2. Number Theory**
- **Graph Patterns**: Mathematical patterns in graphs
- **Component Sequences**: Sequences of component sizes
- **Modular Arithmetic**: Graph operations with modular arithmetic
- **Number Sequences**: Sequences in graph counting

#### **3. Optimization Theory**
- **Graph Optimization**: Optimize graph operations
- **Component Optimization**: Optimize component analysis
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Graph Traversal**: Efficient graph traversal algorithms
- **Component Analysis**: Component analysis algorithms
- **Cycle Detection**: Cycle detection algorithms
- **Dynamic Programming**: For optimization problems

#### **2. Mathematical Concepts**
- **Graph Theory**: Foundation for graph problems
- **Component Theory**: Mathematical properties of components
- **Cycle Theory**: Properties of cycles
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Graph Processing**: Efficient graph processing techniques
- **Component Analysis**: Component analysis techniques

---

*This analysis demonstrates efficient tournament graph distribution counting techniques and shows various extensions for graph and component problems.* 