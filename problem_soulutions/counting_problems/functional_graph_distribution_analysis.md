---
layout: simple
title: "Functional Graph Distribution
permalink: /problem_soulutions/counting_problems/functional_graph_distribution_analysis/
---

# Functional Graph Distribution

## Problem Statement
Given n nodes, count the number of different functional graphs (directed graphs where each node has exactly one outgoing edge).

### Input
The first input line has an integer n: the number of nodes.

### Output
Print the number of different functional graphs modulo 10^9 + 7.

### Constraints
- 1 ≤ n ≤ 10^5

### Example
```
Input:
3

Output:
27
```

## Solution Progression

### Approach 1: Generate All Functions - O(n^n)
**Description**: Generate all possible functions and count them.

```python
def functional_graph_distribution_naive(n):
    MOD = 10**9 + 7
    
    def count_functions(pos):
        if pos == n:
            return 1
        
        count = 0
        for target in range(n):
            count = (count + count_functions(pos + 1)) % MOD
        
        return count
    
    return count_functions(0)
```

**Why this is inefficient**: O(n^n) complexity is too slow for large n.

### Improvement 1: Mathematical Formula - O(n)
**Description**: Use mathematical formula for function counting.

```python
def functional_graph_distribution_improved(n):
    MOD = 10**9 + 7
    
    # Number of functions = n^n
    result = 1
    for _ in range(n):
        result = (result * n) % MOD
    
    return result
```

**Why this improvement works**: Uses mathematical formula for function counting.

### Approach 2: Fast Exponentiation - O(log n)
**Description**: Use fast exponentiation for large n.

```python
def functional_graph_distribution_optimal(n):
    MOD = 10**9 + 7
    
    # Number of functions = n^n
    return pow(n, n, MOD)
```

**Why this improvement works**: Fast exponentiation gives optimal solution.

## Final Optimal Solution

```python
n = int(input())

def count_functional_graphs(n):
    MOD = 10**9 + 7
    
    # Number of functional graphs = n^n
    return pow(n, n, MOD)

result = count_functional_graphs(n)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Generate All Functions | O(n^n) | O(n) | Simple but exponential |
| Mathematical Formula | O(n) | O(1) | Formula approach |
| Fast Exponentiation | O(log n) | O(1) | Optimal solution |

## Key Insights for Other Problems

### 1. **Functional Graph Properties**
**Principle**: Each node has exactly one outgoing edge in a functional graph.
**Applicable to**: Graph theory problems, function counting problems

### 2. **Function Counting**
**Principle**: The number of functions from n elements to n elements is n^n.
**Applicable to**: Combinatorics problems, function analysis problems

### 3. **Fast Exponentiation**
**Principle**: Use fast exponentiation for large power calculations.
**Applicable to**: Large number problems, exponentiation problems

## Notable Techniques

### 1. **Fast Exponentiation**
```python
def fast_pow(base, exp, MOD):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % MOD
        base = (base * base) % MOD
        exp //= 2
    return result
```

### 2. **Function Counting**
```python
def count_functions(n, MOD):
    return pow(n, n, MOD)
```

### 3. **Functional Graph Analysis**
```python
def analyze_functional_graphs(n):
    # Each node can point to any of n nodes
    # Total combinations = n^n
    return pow(n, n, 10**9 + 7)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a functional graph counting problem
2. **Choose approach**: Use mathematical formula with fast exponentiation
3. **Apply formula**: Number of functional graphs = n^n
4. **Use fast exponentiation**: Handle large numbers efficiently
5. **Return result**: Output the count modulo 10^9 + 7

---

*This analysis shows how to efficiently count functional graphs using mathematical formulas and fast exponentiation.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Functional Graph Distribution**
**Problem**: Each node has a weight. Find the distribution of weighted functional graph components.
```python
def weighted_functional_graph_distribution(n, edges, weights):
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

#### **Variation 2: Constrained Functional Graph Distribution**
**Problem**: Find distribution when components are constrained by maximum size.
```python
def constrained_functional_graph_distribution(n, edges, max_component_size):
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

#### **Variation 3: Cycle-Based Functional Graph Distribution**
**Problem**: Find distribution based on cycle lengths in functional graphs.
```python
def cycle_based_functional_graph_distribution(n, edges):
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

#### **Variation 4: Directed Functional Graph Distribution**
**Problem**: Handle directed functional graphs with specific traversal rules.
```python
def directed_functional_graph_distribution(n, edges):
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

#### **Variation 5: Dynamic Functional Graph Updates**
**Problem**: Support dynamic updates to the graph and answer distribution queries efficiently.
```python
class DynamicFunctionalGraphCounter:
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

#### **3. Functional Problems**
- **Functional Analysis**: Analyze functional properties
- **Function Composition**: Compose functions efficiently
- **Function Optimization**: Optimize function operations
- **Function Mapping**: Map functions to graphs

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
    
    result = functional_graph_distribution(n, edges)
    print(len(result))
    for component_id, size in result.items():"
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
        
        dist = functional_graph_distribution(n, subset_edges)
        distributions[mask] = dist
    
    return distributions

# Answer range queries efficiently
def range_query(distributions, edge_mask):
    return distributions.get(edge_mask, {})
```

#### **3. Interactive Problems**
```python
# Interactive functional graph analyzer
def interactive_functional_analyzer():
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
            result = functional_graph_distribution(n, edges)
            print(f"Component distribution: {result}")
        elif query == "weighted":
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_functional_graph_distribution(n, edges, weights)
            print(f"Weighted distribution: {result}")
        elif query == "constrained":
            max_size = int(input("Enter max component size: "))
            result = constrained_functional_graph_distribution(n, edges, max_size)
            print(f"Constrained distribution: {result}")
        elif query == "cycle":
            result = cycle_based_functional_graph_distribution(n, edges)
            print(f"Cycle-based distribution: {result}")
        elif query == "directed":
            result = directed_functional_graph_distribution(n, edges)
            print(f"Directed distribution: {result}")
        elif query == "dynamic":
            counter = DynamicFunctionalGraphCounter(n)
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
- **Functional Theory**: Properties of functional graphs
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

*This analysis demonstrates efficient functional graph distribution counting techniques and shows various extensions for graph and component problems.* 