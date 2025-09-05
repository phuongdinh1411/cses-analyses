---
layout: simple
title: "Functional Graph Distribution"
permalink: /problem_soulutions/counting_problems/functional_graph_distribution_analysis
---


# Functional Graph Distribution

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand functional graphs and their properties in graph theory
- [ ] **Objective 2**: Apply combinatorics to count all possible functions from a set to itself
- [ ] **Objective 3**: Implement efficient algorithms for counting functional graphs
- [ ] **Objective 4**: Optimize functional graph counting using mathematical formulas and modular arithmetic
- [ ] **Objective 5**: Handle large functional graph counts using modular arithmetic and optimization

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, functional graphs, combinatorics, modular arithmetic
- **Data Structures**: Arrays, mathematical computation structures
- **Mathematical Concepts**: Functions, graph theory, combinatorics, modular arithmetic, exponentiation
- **Programming Skills**: Modular arithmetic, large number handling, mathematical computation
- **Related Problems**: Counting Combinations (combinatorics), Counting Permutations (counting problems), Graph theory problems

## 📋 Problem Description

Given n nodes, count the number of different functional graphs (directed graphs where each node has exactly one outgoing edge).

This is a combinatorics problem where we need to count all possible functions from a set of n elements to itself. Each node must have exactly one outgoing edge, which means we're counting all possible mappings from {1, 2, ..., n} to {1, 2, ..., n}.

**Input**: 
- First line: integer n (number of nodes)

**Output**: 
- Print the number of different functional graphs modulo 10⁹ + 7

**Constraints**:
- 1 ≤ n ≤ 10⁵

**Example**:
```
Input:
3

Output:
27
```

**Explanation**: 
For n = 3, there are 3³ = 27 different functional graphs:
- Each of the 3 nodes can point to any of the 3 nodes (including itself)
- This gives us 3 × 3 × 3 = 27 total possibilities

### 📊 Visual Example

**Functional Graph for n=3:**
```
Nodes: {1, 2, 3}
Each node must have exactly one outgoing edge
```

**All Possible Functions:**
```
Function 1: f(1)=1, f(2)=1, f(3)=1
┌─────────────────────────────────────┐
│ 1 → 1, 2 → 1, 3 → 1                │
│ Graph: 1 ← 2 ← 3                    │
│ All nodes point to node 1           │
└─────────────────────────────────────┘

Function 2: f(1)=1, f(2)=1, f(3)=2
┌─────────────────────────────────────┐
│ 1 → 1, 2 → 1, 3 → 2                │
│ Graph: 1 ← 2, 2 ← 3                │
│ Nodes 1,2 point to 1, node 3 points to 2│
└─────────────────────────────────────┘

Function 3: f(1)=1, f(2)=1, f(3)=3
┌─────────────────────────────────────┐
│ 1 → 1, 2 → 1, 3 → 3                │
│ Graph: 1 ← 2, 3 → 3                │
│ Nodes 1,2 point to 1, node 3 points to itself│
└─────────────────────────────────────┘

... (continuing for all 27 functions)
```

**Mathematical Formula:**
```
For n nodes, each node can point to any of the n nodes:
┌─────────────────────────────────────┐
│ Node 1: n choices                   │
│ Node 2: n choices                   │
│ Node 3: n choices                   │
│ ...                                 │
│ Node n: n choices                   │
│                                     │
│ Total: n × n × ... × n = n^n       │
└─────────────────────────────────────┘

For n=3: 3³ = 27
```

**Step-by-Step Calculation:**
```
Step 1: Count choices for each node
┌─────────────────────────────────────┐
│ Node 1: 3 choices (1, 2, 3)        │
│ Node 2: 3 choices (1, 2, 3)        │
│ Node 3: 3 choices (1, 2, 3)        │
└─────────────────────────────────────┘

Step 2: Calculate total combinations
┌─────────────────────────────────────┐
│ Total = 3 × 3 × 3 = 27             │
└─────────────────────────────────────┘
```

**Algorithm Flowchart:**
```
┌─────────────────────────────────────┐
│ Start: Read n                      │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Calculate n^n using modular         │
│ exponentiation                      │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return result modulo 10^9 + 7       │
└─────────────────────────────────────┘
```

**Key Insight Visualization:**
```
For any functional graph:
┌─────────────────────────────────────┐
│ - Each node has exactly one        │
│   outgoing edge                     │
│ - This edge can point to any node   │
│   (including itself)                │
│ - The graph represents a function   │
│   from {1,2,...,n} to {1,2,...,n}  │
└─────────────────────────────────────┘

Example with n=2:
┌─────────────────────────────────────┐
│ Possible functions:                 │
│ f(1)=1, f(2)=1: 1 → 1, 2 → 1      │
│ f(1)=1, f(2)=2: 1 → 1, 2 → 2      │
│ f(1)=2, f(2)=1: 1 → 2, 2 → 1      │
│ f(1)=2, f(2)=2: 1 → 2, 2 → 2      │
│ Total: 2² = 4                      │
└─────────────────────────────────────┘
```

**Modular Exponentiation:**
```
To calculate n^n mod (10^9 + 7):
┌─────────────────────────────────────┐
│ Use binary exponentiation:          │
│ - Convert n to binary              │
│ - Use the identity:                │
│   a^b = (a^(b/2))² if b is even   │
│   a^b = a × (a^(b-1)) if b is odd  │
└─────────────────────────────────────┘

Example: 3³ mod 10^9 + 7
┌─────────────────────────────────────┐
│ 3³ = 3 × 3² = 3 × 9 = 27           │
│ 27 mod (10^9 + 7) = 27             │
└─────────────────────────────────────┘
```

**Time Complexity:**
```
┌─────────────────────────────────────┐
│ Modular exponentiation: O(log n)   │
│ Total: O(log n)                    │
└─────────────────────────────────────┘
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
## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(1) for the mathematical formula approach
- **Space Complexity**: O(1) for storing the result
- **Why it works**: We use the mathematical formula n^n to count all possible functions from n elements to n elements

### Key Implementation Points
- Use the mathematical formula n^n for counting functional graphs
- Handle modular arithmetic to prevent overflow
- Use fast exponentiation for large values of n
- Consider edge cases like n = 1

## 🎯 Key Insights

### Important Concepts and Patterns
- **Function Counting**: Mathematical foundation for counting functions
- **Modular Arithmetic**: Required for handling large numbers
- **Fast Exponentiation**: Efficient way to compute n^n mod MOD
- **Combinatorics**: Foundation for counting problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Functional Graph Distribution with Constraints**
```python
def functional_graph_distribution_with_constraints(n, constraints):
    # Count functional graphs with additional constraints
    MOD = 10**9 + 7
    
    # Check constraints
    if constraints.get("min_nodes", 1) > n:
        return 0
    if constraints.get("max_nodes", float('inf')) < n:
        return 0
    if constraints.get("allowed_sizes") and n not in constraints["allowed_sizes"]:
        return 0
    
    # Calculate n^n mod MOD
    result = pow(n, n, MOD)
    
    return result

# Example usage
n = 3
constraints = {"min_nodes": 1, "max_nodes": 10, "allowed_sizes": [1, 2, 3, 4, 5]}
result = functional_graph_distribution_with_constraints(n, constraints)
print(f"Constrained functional graph count: {result}")
```

#### **2. Functional Graph Distribution with Cycle Constraints**
```python
def functional_graph_distribution_with_cycle_constraints(n, cycle_constraints):
    # Count functional graphs with constraints on cycles
    MOD = 10**9 + 7
    
    # Check cycle constraints
    if cycle_constraints.get("min_cycles", 0) > n:
        return 0
    if cycle_constraints.get("max_cycles", n) < 1:
        return 0
    if cycle_constraints.get("allowed_cycle_lengths"):
        # This is more complex and would require advanced combinatorics
        pass
    
    # For now, just return the basic count
    result = pow(n, n, MOD)
    
    return result

# Example usage
n = 3
cycle_constraints = {"min_cycles": 1, "max_cycles": 3, "allowed_cycle_lengths": [1, 2, 3]}
result = functional_graph_distribution_with_cycle_constraints(n, cycle_constraints)
print(f"Cycle-constrained functional graph count: {result}")
```

#### **3. Functional Graph Distribution with Multiple Sizes**
```python
def functional_graph_distribution_multiple_sizes(sizes):
    # Count functional graphs for multiple sizes
    MOD = 10**9 + 7
    results = {}
    
    for n in sizes:
        # Calculate n^n mod MOD
        result = pow(n, n, MOD)
        results[n] = result
    
    return results

# Example usage
sizes = [1, 2, 3, 4, 5]
results = functional_graph_distribution_multiple_sizes(sizes)
for n, count in results.items():
    print(f"Functional graphs for n={n}: {count}")
```

#### **4. Functional Graph Distribution with Statistics**
```python
def functional_graph_distribution_with_statistics(n):
    # Count functional graphs and provide statistics
    MOD = 10**9 + 7
    
    # Calculate n^n mod MOD
    result = pow(n, n, MOD)
    
    # Calculate statistics
    statistics = {
        "total_count": result,
        "nodes": n,
        "theoretical_max": n**n,
        "modulo": MOD,
        "has_cycles": True,  # All functional graphs have cycles
        "min_cycles": 1,     # At least one cycle
        "max_cycles": n      # At most n cycles (one per node)
    }
    
    return result, statistics

# Example usage
n = 3
count, stats = functional_graph_distribution_with_statistics(n)
print(f"Functional graph count: {count}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Graph Algorithms**: Graph counting, Graph construction
- **Combinatorics**: Function counting, Permutation counting
- **Modular Arithmetic**: Modular exponentiation, Modular inverses
- **Counting Problems**: Subset counting, Path counting

## 📚 Learning Points

### Key Takeaways
- **Function counting** is fundamental for understanding functional graphs
- **Mathematical formulas** can often replace complex algorithms
- **Modular arithmetic** is required for handling large numbers
- **Fast exponentiation** is essential for computing large powers efficiently

---

*This analysis demonstrates efficient functional graph distribution counting techniques and shows various extensions for graph and component problems.* 