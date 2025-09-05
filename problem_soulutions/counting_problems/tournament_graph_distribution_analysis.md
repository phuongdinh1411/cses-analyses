---
layout: simple
title: "Tournament Graph Distribution"
permalink: /problem_soulutions/counting_problems/tournament_graph_distribution_analysis
---


# Tournament Graph Distribution

## 📋 Problem Description

Given n teams, count the number of different tournament graphs where each team plays against every other team exactly once, and the result is a valid tournament (no cycles).

This is a graph theory problem where we need to count the number of valid tournament graphs. A tournament is a directed graph where every pair of vertices is connected by exactly one directed edge, and it must be acyclic (no directed cycles).

**Input**: 
- First line: integer n (number of teams)

**Output**: 
- Print the number of different tournament graphs modulo 10⁹ + 7

**Constraints**:
- 1 ≤ n ≤ 20

**Example**:
```
Input:
3

Output:
2
```

**Explanation**: 
For n = 3 teams, there are 2 valid tournament graphs:
1. Team 1 beats Team 2, Team 2 beats Team 3, Team 1 beats Team 3
2. Team 1 beats Team 3, Team 3 beats Team 2, Team 1 beats Team 2

Both result in acyclic tournament graphs where each team plays every other team exactly once.

### 📊 Visual Example

**Tournament Graph for n=3:**
```
Teams: {1, 2, 3}
Each team plays every other team exactly once
```

**All Possible Tournament Graphs:**
```
Tournament 1: 1 → 2 → 3 → 1
┌─────────────────────────────────────┐
│ Team 1 beats Team 2                │
│ Team 2 beats Team 3                │
│ Team 1 beats Team 3                │
│ Graph: 1 → 2 → 3 → 1              │
│ Has cycle: 1 → 2 → 3 → 1 ✗        │
│ Invalid tournament ✗               │
└─────────────────────────────────────┘

Tournament 2: 1 → 2 → 3
┌─────────────────────────────────────┐
│ Team 1 beats Team 2                │
│ Team 2 beats Team 3                │
│ Team 1 beats Team 3                │
│ Graph: 1 → 2 → 3                  │
│ No cycles ✓                        │
│ Valid tournament ✓                 │
└─────────────────────────────────────┘

Tournament 3: 1 → 3 → 2
┌─────────────────────────────────────┐
│ Team 1 beats Team 3                │
│ Team 3 beats Team 2                │
│ Team 1 beats Team 2                │
│ Graph: 1 → 3 → 2                  │
│ No cycles ✓                        │
│ Valid tournament ✓                 │
└─────────────────────────────────────┘

Tournament 4: 2 → 1 → 3
┌─────────────────────────────────────┐
│ Team 2 beats Team 1                │
│ Team 1 beats Team 3                │
│ Team 2 beats Team 3                │
│ Graph: 2 → 1 → 3                  │
│ No cycles ✓                        │
│ Valid tournament ✓                 │
└─────────────────────────────────────┘

Tournament 5: 2 → 3 → 1
┌─────────────────────────────────────┐
│ Team 2 beats Team 3                │
│ Team 3 beats Team 1                │
│ Team 2 beats Team 1                │
│ Graph: 2 → 3 → 1                  │
│ No cycles ✓                        │
│ Valid tournament ✓                 │
└─────────────────────────────────────┘

Tournament 6: 3 → 1 → 2
┌─────────────────────────────────────┐
│ Team 3 beats Team 1                │
│ Team 1 beats Team 2                │
│ Team 3 beats Team 2                │
│ Graph: 3 → 1 → 2                  │
│ No cycles ✓                        │
│ Valid tournament ✓                 │
└─────────────────────────────────────┘

Tournament 7: 3 → 2 → 1
┌─────────────────────────────────────┐
│ Team 3 beats Team 2                │
│ Team 2 beats Team 1                │
│ Team 3 beats Team 1                │
│ Graph: 3 → 2 → 1                  │
│ No cycles ✓                        │
│ Valid tournament ✓                 │
└─────────────────────────────────────┘

Total valid tournaments: 6
```

**Mathematical Formula:**
```
For n teams, the number of valid tournament graphs is:
┌─────────────────────────────────────┐
│ n! / 2^(n(n-1)/2)                  │
│                                     │
│ Where:                              │
│ - n! = number of ways to order teams│
│ - 2^(n(n-1)/2) = number of ways to  │
│   assign directions to edges        │
└─────────────────────────────────────┘

For n=3: 3! / 2^(3×2/2) = 6 / 2³ = 6 / 8 = 0.75
```

**Step-by-Step Calculation:**
```
Step 1: Count total possible tournaments
┌─────────────────────────────────────┐
│ Total edges: n(n-1)/2 = 3×2/2 = 3  │
│ Each edge can be directed in 2 ways │
│ Total tournaments: 2³ = 8           │
└─────────────────────────────────────┘

Step 2: Count valid tournaments
┌─────────────────────────────────────┐
│ Valid tournaments: 6               │
│ (All except the cyclic one)        │
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
│ Generate all possible tournament    │
│ graphs using bitmask               │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ For each tournament graph:          │
│   Check if it's acyclic            │
│   If acyclic: count++              │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ Return total count                  │
└─────────────────────────────────────┘
```

**Key Insight Visualization:**
```
For any tournament graph:
┌─────────────────────────────────────┐
│ - Every pair of teams plays exactly │
│   once                              │
│ - The result is a directed edge     │
│ - The graph must be acyclic         │
│ - This means there's a total        │
│   ordering of teams                 │
└─────────────────────────────────────┘

Example with n=3:
┌─────────────────────────────────────┐
│ Valid orderings:                   │
│ - 1 → 2 → 3                        │
│ - 1 → 3 → 2                        │
│ - 2 → 1 → 3                        │
│ - 2 → 3 → 1                        │
│ - 3 → 1 → 2                        │
│ - 3 → 2 → 1                        │
│ Total: 6                           │
└─────────────────────────────────────┘
```

**Cycle Detection:**
```
To check if a tournament graph is acyclic:
┌─────────────────────────────────────┐
│ 1. Use topological sorting         │
│ 2. If topological sort exists,     │
│    the graph is acyclic            │
│ 3. If topological sort fails,      │
│    the graph has a cycle           │
└─────────────────────────────────────┘

Example: 1 → 2 → 3 → 1
┌─────────────────────────────────────┐
│ Topological sort:                  │
│ - Start with node 1                │
│ - Remove 1, add 2 to queue         │
│ - Remove 2, add 3 to queue         │
│ - Remove 3, but 1 is still in      │
│   the graph (cycle detected) ✗     │
└─────────────────────────────────────┘
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
## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n!) for generating all tournaments, O(n²) for cycle detection
- **Space Complexity**: O(n²) for storing the tournament graph
- **Why it works**: We generate all possible tournament graphs and check for cycles using DFS

### Key Implementation Points
- Generate all possible tournament graphs systematically
- Use DFS to detect cycles in directed graphs
- Handle modular arithmetic for large numbers
- Optimize by pruning invalid tournaments early

## 🎯 Key Insights

### Important Concepts and Patterns
- **Tournament Graphs**: Directed graphs with exactly one edge between each pair of vertices
- **Cycle Detection**: Essential for ensuring valid tournaments
- **Graph Theory**: Understanding tournament properties
- **Combinatorics**: Counting valid graph structures

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Tournament Graph Distribution with Constraints**
```python
def tournament_graph_distribution_with_constraints(n, constraints):
    # Count tournament graphs with additional constraints
    MOD = 10**9 + 7
    
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
    
    def generate_tournaments(pos, edges):
        if pos == n * (n - 1) // 2:
            return 1 if is_valid_tournament(edges) else 0
        
        count = 0
        u, v = pos // (n - 1), pos % (n - 1)
        if v >= u:
            v += 1
        
        # Try both directions
        for direction in [(u, v), (v, u)]:
            # Check constraints
            if constraints.get("forbidden_edges") and direction in constraints["forbidden_edges"]:
                continue
            if constraints.get("required_edges") and direction not in constraints.get("required_edges", []):
                continue
            
            count = (count + generate_tournaments(pos + 1, edges + [direction])) % MOD
        
        return count
    
    return generate_tournaments(0, [])

# Example usage
n = 3
constraints = {"forbidden_edges": [], "required_edges": []}
result = tournament_graph_distribution_with_constraints(n, constraints)
print(f"Tournament graphs with constraints: {result}")
```

#### **2. Tournament Graph Distribution with Team Strengths**
```python
def tournament_graph_distribution_with_strengths(n, team_strengths):
    # Count tournament graphs considering team strengths
    MOD = 10**9 + 7
    
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
    
    def generate_tournaments(pos, edges):
        if pos == n * (n - 1) // 2:
            return 1 if is_valid_tournament(edges) else 0
        
        count = 0
        u, v = pos // (n - 1), pos % (n - 1)
        if v >= u:
            v += 1
        
        # Determine winner based on team strengths
        if team_strengths[u] > team_strengths[v]:
            winner, loser = u, v
        elif team_strengths[v] > team_strengths[u]:
            winner, loser = v, u
        else:
            # Equal strength - try both directions
            for direction in [(u, v), (v, u)]:
                count = (count + generate_tournaments(pos + 1, edges + [direction])) % MOD
            return count
        
        count = (count + generate_tournaments(pos + 1, edges + [(winner, loser)])) % MOD
        return count
    
    return generate_tournaments(0, [])

# Example usage
n = 3
team_strengths = [3, 2, 1]  # Team 0 is strongest, Team 2 is weakest
result = tournament_graph_distribution_with_strengths(n, team_strengths)
print(f"Tournament graphs with team strengths: {result}")
```

#### **3. Tournament Graph Distribution with Multiple Sizes**
```python
def tournament_graph_distribution_multiple_sizes(sizes):
    # Count tournament graphs for multiple sizes
    MOD = 10**9 + 7
    results = {}
    
    for n in sizes:
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
        
        def generate_tournaments(pos, edges):
            if pos == n * (n - 1) // 2:
                return 1 if is_valid_tournament(edges) else 0
            
            count = 0
            u, v = pos // (n - 1), pos % (n - 1)
            if v >= u:
                v += 1
            
            # Try both directions
            for direction in [(u, v), (v, u)]:
                count = (count + generate_tournaments(pos + 1, edges + [direction])) % MOD
            
            return count
        
        results[n] = generate_tournaments(0, [])
    
    return results

# Example usage
sizes = [2, 3, 4]
results = tournament_graph_distribution_multiple_sizes(sizes)
for n, count in results.items():
    print(f"Tournament graphs for {n} teams: {count}")
```

#### **4. Tournament Graph Distribution with Statistics**
```python
def tournament_graph_distribution_with_statistics(n):
    # Count tournament graphs and provide statistics
    MOD = 10**9 + 7
    tournaments = []
    
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
    
    def generate_tournaments(pos, edges):
        if pos == n * (n - 1) // 2:
            if is_valid_tournament(edges):
                tournaments.append(edges[:])
                return 1
            return 0
        
        count = 0
        u, v = pos // (n - 1), pos % (n - 1)
        if v >= u:
            v += 1
        
        # Try both directions
        for direction in [(u, v), (v, u)]:
            count = (count + generate_tournaments(pos + 1, edges + [direction])) % MOD
        
        return count
    
    total_count = generate_tournaments(0, [])
    
    # Calculate statistics
    win_counts = [0] * n
    for tournament in tournaments:
        for u, v in tournament:
            win_counts[u] += 1
    
    statistics = {
        "total_tournaments": total_count,
        "teams": n,
        "total_matches": n * (n - 1) // 2,
        "average_wins": [count / total_count for count in win_counts] if total_count > 0 else [0] * n,
        "sample_tournaments": tournaments[:5]  # First 5 tournaments
    }
    
    return total_count, statistics

# Example usage
n = 3
count, stats = tournament_graph_distribution_with_statistics(n)
print(f"Total tournament graphs: {count}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **Graph Theory**: Tournament graphs, Directed acyclic graphs
- **Combinatorics**: Graph counting, Arrangement counting
- **Cycle Detection**: DFS, Topological sorting
- **Counting Problems**: Subset counting, Path counting

## 📚 Learning Points

### Key Takeaways
- **Tournament graphs** are fundamental structures in graph theory
- **Cycle detection** is essential for ensuring valid tournaments
- **Graph generation** requires systematic exploration of all possibilities
- **Combinatorics** provides the mathematical foundation for counting problems

---

*This analysis demonstrates efficient tournament graph distribution counting techniques and shows various extensions for graph and component problems.* 