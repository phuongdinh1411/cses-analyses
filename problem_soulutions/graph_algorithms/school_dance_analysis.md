---
layout: simple
title: "School Dance - Maximum Bipartite Matching"
permalink: /problem_soulutions/graph_algorithms/school_dance_analysis
---

# School Dance - Maximum Bipartite Matching

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand bipartite matching problems and maximum matching concepts
- Apply maximum flow algorithms or Hungarian algorithm to solve bipartite matching
- Implement efficient bipartite matching algorithms with proper graph construction
- Optimize bipartite matching solutions using flow networks and matching algorithms
- Handle edge cases in bipartite matching (no matches possible, complete matching, disconnected components)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Maximum flow, bipartite matching, Hungarian algorithm, flow networks, matching algorithms
- **Data Structures**: Bipartite graphs, flow networks, matching data structures, graph representations
- **Mathematical Concepts**: Graph theory, bipartite graphs, matching theory, flow networks, optimization
- **Programming Skills**: Graph construction, flow algorithms, matching implementation, algorithm implementation
- **Related Problems**: Download Speed (maximum flow), Police Chase (flow problems), Bipartite matching

## Problem Description

**Problem**: Given n boys and m girls, where each boy can dance with certain girls, find the maximum number of boys and girls that can be matched for dancing.

This is a maximum bipartite matching problem where we need to find the maximum number of pairs that can be formed between boys and girls based on their preferences.

**Input**: 
- First line: Two integers n and m (number of boys and girls)
- Next n lines: k integers (girls that boy i can dance with)

**Output**: 
- Maximum number of boys and girls that can be matched

**Constraints**:
- 1 ≤ n, m ≤ 500
- 1 ≤ k ≤ m
- Each boy can dance with multiple girls
- Each girl can dance with multiple boys
- Boys and girls are numbered from 1 to n and 1 to m respectively

**Example**:
```
Input:
3 3
1 2
2 3
1 3

Output:
3
```

**Explanation**: 
- Boy 1 can dance with girls 1, 2
- Boy 2 can dance with girls 2, 3
- Boy 3 can dance with girls 1, 3
- Maximum matching: (1,1), (2,2), (3,3) = 3 pairs

## Visual Example

### Input Preferences
```
Boys: 3, Girls: 3
Preferences:
- Boy 1: can dance with girls 1, 2
- Boy 2: can dance with girls 2, 3
- Boy 3: can dance with girls 1, 3
```

### Bipartite Graph Construction
```
Step 1: Build bipartite graph
- Left side: Boys {1, 2, 3}
- Right side: Girls {1, 2, 3}
- Edges: (1,1), (1,2), (2,2), (2,3), (3,1), (3,3)

Graph representation:
Boys    Girls
1 ────── 1
│       │
└───────┼─── 2
        │   │
2 ──────┼───┼─── 3
        │   │
3 ──────┼───┘
        │
        └───── 3
```

### Maximum Matching Algorithm Process
```
Step 1: Initialize matching
- Matching: {}

Step 2: Find augmenting paths
- Start from unmatched boy 1
- Path: 1 → 1 (girl 1 unmatched)
- Add (1,1) to matching

- Start from unmatched boy 2
- Path: 2 → 2 (girl 2 unmatched)
- Add (2,2) to matching

- Start from unmatched boy 3
- Path: 3 → 3 (girl 3 unmatched)
- Add (3,3) to matching

Step 3: No more augmenting paths
- Maximum matching: {(1,1), (2,2), (3,3)}
- Size: 3
```

### Matching Analysis
```
Maximum matching found:
- Boy 1 ↔ Girl 1
- Boy 2 ↔ Girl 2
- Boy 3 ↔ Girl 3

All boys and girls are matched ✓
Maximum matching size: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Bipartite Matching (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible combinations of boy-girl pairs
- Check if each combination forms a valid matching
- Simple but computationally expensive approach
- Not suitable for large graphs

**Algorithm:**
1. Generate all possible combinations of boy-girl pairs
2. Check if each combination forms a valid matching
3. Count the maximum number of valid pairs
4. Return the maximum matching size

**Visual Example:**
```
Brute force: Try all possible matchings
For preferences: Boy1→{1,2}, Boy2→{2,3}, Boy3→{1,3}

All possible matchings:
- Matching 1: {(1,1), (2,2), (3,3)} → Size: 3
- Matching 2: {(1,1), (2,3), (3,1)} → Size: 3
- Matching 3: {(1,2), (2,2), (3,1)} → Size: 3
- Matching 4: {(1,2), (2,3), (3,3)} → Size: 3

Maximum matching size: 3
```

**Implementation:**
```python
def school_dance_brute_force(n, m, preferences):
    from itertools import combinations, product
    
    # Generate all possible boy-girl pairs
    all_pairs = []
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            all_pairs.append((boy, girl))
    
    max_matching = 0
    
    # Try all possible combinations of pairs
    for k in range(min(n, m) + 1):
        for pair_set in combinations(all_pairs, k):
            if is_valid_matching(pair_set):
                max_matching = max(max_matching, len(pair_set))
    
    return max_matching

def is_valid_matching(pair_set):
    # Check if no boy or girl appears twice
    boys = set()
    girls = set()
    
    for boy, girl in pair_set:
        if boy in boys or girl in girls:
            return False
        boys.add(boy)
        girls.add(girl)
    
    return True
```

**Time Complexity:** O(2^(n×m) × (n + m)) for checking all combinations
**Space Complexity:** O(n + m) for storing pairs

**Why it's inefficient:**
- Exponential time complexity O(2^(n×m))
- Not suitable for large graphs
- Overkill for this specific problem
- Impractical for competitive programming

### Approach 2: Maximum Flow Algorithm (Better)

**Key Insights from Maximum Flow Solution:**
- Convert bipartite matching to maximum flow problem
- Use flow network with source and sink
- Much more efficient than brute force approach
- Standard method for bipartite matching problems

**Algorithm:**
1. Build flow network: Source → Boys → Girls → Sink
2. Set all edge capacities to 1
3. Find maximum flow from source to sink
4. Maximum flow equals maximum matching size

**Visual Example:**
```
Maximum flow algorithm for preferences: Boy1→{1,2}, Boy2→{2,3}, Boy3→{1,3}

Step 1: Build flow network
- Source → Boys: capacity 1
- Boys → Girls: capacity 1 (based on preferences)
- Girls → Sink: capacity 1

Flow network:
Source ──1──> Boy1 ──1──> Girl1 ──1──> Sink
   │           │           │
   └──1──> Boy2 ──1──> Girl2 ──1──> Sink
   │           │           │
   └──1──> Boy3 ──1──> Girl3 ──1──> Sink

Step 2: Find maximum flow
- Path 1: Source → Boy1 → Girl1 → Sink (flow: 1)
- Path 2: Source → Boy2 → Girl2 → Sink (flow: 1)
- Path 3: Source → Boy3 → Girl3 → Sink (flow: 1)

Maximum flow: 3
Maximum matching size: 3
```

**Implementation:**
```python
def school_dance_max_flow(n, m, preferences):
    # Build flow network: Source -> Boys -> Girls -> Sink
    total_nodes = 2 + n + m  # source + boys + girls + sink
    source = 0
    sink = total_nodes - 1
    
    # Build adjacency list with capacities
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys (capacity 1)
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls (capacity 1)
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink (capacity 1)
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    def bfs(source, sink):
        # Find augmenting path using BFS
        parent = [-1] * total_nodes
        parent[source] = source
        queue = [source]
        
        while queue:
            current = queue.pop(0)
            
            for next_node in adj[current]:
                if parent[next_node] == -1 and capacity[current][next_node] > 0:
                    parent[next_node] = current
                    queue.append(next_node)
                    
                    if next_node == sink:
                        break
        
        if parent[sink] == -1:
            return 0  # No augmenting path found
        
        # Find bottleneck capacity
        bottleneck = float('inf')
        current = sink
        while current != source:
            bottleneck = min(bottleneck, capacity[parent[current]][current])
            current = parent[current]
        
        # Update residual graph
        current = sink
        while current != source:
            capacity[parent[current]][current] -= bottleneck
            capacity[current][parent[current]] += bottleneck
            current = parent[current]
        
        return bottleneck
    
    # Ford-Fulkerson algorithm
    max_flow = 0
    while True:
        flow = bfs(source, sink)
        if flow == 0:
            break
        max_flow += flow
    
    return max_flow
```

**Time Complexity:** O(n × m × (n + m)) for maximum flow
**Space Complexity:** O((n + m)²) for adjacency matrix

**Why it's better:**
- Polynomial time complexity O(n × m × (n + m))
- Simple and intuitive approach
- Standard method for bipartite matching problems
- Suitable for competitive programming

### Approach 3: Hopcroft-Karp Algorithm (Optimal)

**Key Insights from Hopcroft-Karp Solution:**
- Use BFS to find multiple augmenting paths simultaneously
- Optimize bipartite matching for better performance
- Most efficient approach for bipartite matching problems
- Standard method in competitive programming

**Algorithm:**
1. Build bipartite graph from preferences
2. Use BFS to find multiple augmenting paths simultaneously
3. Use DFS to augment along found paths
4. Repeat until no more augmenting paths exist

**Visual Example:**
```
Hopcroft-Karp algorithm for preferences: Boy1→{1,2}, Boy2→{2,3}, Boy3→{1,3}

Step 1: Build bipartite graph
- Left side: Boys {1, 2, 3}
- Right side: Girls {1, 2, 3}
- Edges: (1,1), (1,2), (2,2), (2,3), (3,1), (3,3)

Step 2: Find multiple augmenting paths
- BFS finds: [1→1, 2→2, 3→3]
- All paths are disjoint, augment simultaneously

Step 3: Update matching
- Matching: {(1,1), (2,2), (3,3)}
- Size: 3

Step 4: No more augmenting paths
- Maximum matching: {(1,1), (2,2), (3,3)}
- Size: 3
```

**Implementation:**
```python
def school_dance_hopcroft_karp(n, m, preferences):
    # Build bipartite graph
    adj = [[] for _ in range(n + 1)]
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            adj[boy].append(girl)
    
    # Hopcroft-Karp algorithm
    pair_u = [0] * (n + 1)  # pair for boys
    pair_v = [0] * (m + 1)  # pair for girls
    dist = [0] * (n + 1)
    
    def bfs():
        queue = []
        for u in range(1, n + 1):
            if pair_u[u] == 0:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = float('inf')
        
        dist[0] = float('inf')
        
        while queue:
            u = queue.pop(0)
            if dist[u] < dist[0]:
                for v in adj[u]:
                    if dist[pair_v[v]] == float('inf'):
                        dist[pair_v[v]] = dist[u] + 1
                        queue.append(pair_v[v])
        
        return dist[0] != float('inf')
    
    def dfs(u):
        if u != 0:
            for v in adj[u]:
                if dist[pair_v[v]] == dist[u] + 1:
                    if dfs(pair_v[v]):
                        pair_u[u] = v
                        pair_v[v] = u
                        return True
            dist[u] = float('inf')
            return False
        return True
    
    # Find maximum matching
    matching = 0
    while bfs():
        for u in range(1, n + 1):
            if pair_u[u] == 0:
                if dfs(u):
                    matching += 1
    
    return matching

def solve_school_dance():
    n, m = map(int, input().split())
    preferences = []
    for _ in range(n):
        line = list(map(int, input().split()))
        k = line[0]
        girls = line[1:k+1]
        preferences.append(girls)
    
    result = school_dance_hopcroft_karp(n, m, preferences)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_school_dance()
```

**Time Complexity:** O(√n × m) for Hopcroft-Karp algorithm
**Space Complexity:** O(n + m) for graph representation

**Why it's optimal:**
- O(√n × m) time complexity is optimal for bipartite matching
- Uses BFS to find multiple augmenting paths simultaneously
- Most efficient approach for competitive programming
- Standard method for bipartite matching problems

## 🎯 Problem Variations

### Variation 1: Weighted Bipartite Matching
**Problem**: Find maximum weight bipartite matching where each edge has a weight.

**Link**: [CSES Problem Set - Weighted Bipartite Matching](https://cses.fi/problemset/task/weighted_bipartite_matching)

```python
def weighted_bipartite_matching(n, m, preferences, weights):
    # Use Hungarian algorithm for weighted bipartite matching
    # or convert to minimum cost maximum flow problem
    
    # Build flow network with weights
    total_nodes = 2 + n + m
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    cost = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to girls with weights
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
            cost[boy][girl_node] = weights[boy-1][girl-1]
            cost[girl_node][boy] = -weights[boy-1][girl-1]
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    # Use minimum cost maximum flow algorithm
    return min_cost_max_flow(adj, capacity, cost, source, sink)
```

### Variation 2: Bipartite Matching with Capacity Constraints
**Problem**: Find maximum bipartite matching with capacity constraints on nodes.

**Link**: [CSES Problem Set - Bipartite Matching with Capacities](https://cses.fi/problemset/task/bipartite_matching_capacities)

```python
def bipartite_matching_with_capacities(n, m, preferences, boy_capacity, girl_capacity):
    # Build flow network with node capacities
    total_nodes = 2 + n + m
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys with capacity constraints
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = boy_capacity[boy-1]
    
    # Boys to girls
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            girl_node = n + girl
            adj[boy].append(girl_node)
            adj[girl_node].append(boy)
            capacity[boy][girl_node] = 1
    
    # Girls to sink with capacity constraints
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = girl_capacity[girl-1]
    
    # Find maximum flow
    return max_flow(adj, capacity, source, sink)
```

### Variation 3: Bipartite Matching with Multiple Edge Types
**Problem**: Find maximum bipartite matching considering different types of edges.

**Link**: [CSES Problem Set - Bipartite Matching with Edge Types](https://cses.fi/problemset/task/bipartite_matching_edge_types)

```python
def bipartite_matching_edge_types(n, m, preferences, edge_types, type_limits):
    # Group edges by type
    edges_by_type = {}
    for boy in range(1, n + 1):
        for girl in preferences[boy - 1]:
            edge_type = edge_types[boy-1][girl-1]
            if edge_type not in edges_by_type:
                edges_by_type[edge_type] = []
            edges_by_type[edge_type].append((boy, girl))
    
    # Build flow network with type constraints
    total_nodes = 2 + n + m + len(edges_by_type)
    source = 0
    sink = total_nodes - 1
    
    adj = [[] for _ in range(total_nodes)]
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Source to boys
    for boy in range(1, n + 1):
        adj[source].append(boy)
        adj[boy].append(source)
        capacity[source][boy] = 1
    
    # Boys to type nodes
    type_offset = n + 1
    for edge_type, edges in edges_by_type.items():
        type_node = type_offset + edge_type
        for boy, girl in edges:
            adj[boy].append(type_node)
            adj[type_node].append(boy)
            capacity[boy][type_node] = 1
    
    # Type nodes to girls with type limits
    for edge_type, edges in edges_by_type.items():
        type_node = type_offset + edge_type
        for boy, girl in edges:
            girl_node = n + girl
            adj[type_node].append(girl_node)
            adj[girl_node].append(type_node)
            capacity[type_node][girl_node] = 1
    
    # Girls to sink
    for girl in range(1, m + 1):
        girl_node = n + girl
        adj[girl_node].append(sink)
        adj[sink].append(girl_node)
        capacity[girl_node][sink] = 1
    
    # Find maximum flow
    return max_flow(adj, capacity, source, sink)
```

## 🔗 Related Problems

- **[Download Speed](/cses-analyses/problem_soulutions/graph_algorithms/download_speed_analysis/)**: Maximum flow problems
- **[Police Chase](/cses-analyses/problem_soulutions/graph_algorithms/police_chase_analysis/)**: Flow problems
- **[Bipartite Matching](/cses-analyses/problem_soulutions/graph_algorithms/)**: Matching problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph theory problems

## 📚 Learning Points

1. **Bipartite Matching**: Essential for assignment and pairing problems
2. **Maximum Flow**: Key technique for solving bipartite matching problems
3. **Hopcroft-Karp Algorithm**: Optimal approach for bipartite matching
4. **Flow Networks**: Important concept for graph optimization problems
5. **Augmenting Paths**: Core mechanism for finding maximum matchings
6. **Graph Theory**: Foundation for many optimization problems

## 📝 Summary

The School Dance problem demonstrates fundamental bipartite matching concepts for optimizing pairing assignments. We explored three approaches:

1. **Brute Force Bipartite Matching**: O(2^(n×m) × (n + m)) time complexity using exhaustive search, inefficient for large graphs
2. **Maximum Flow Algorithm**: O(n × m × (n + m)) time complexity using flow networks, optimal and intuitive approach
3. **Hopcroft-Karp Algorithm**: O(√n × m) time complexity using optimized bipartite matching, most efficient approach

The key insights include understanding bipartite matching as flow network problems, using maximum flow algorithms for efficient matching calculation, and applying Hopcroft-Karp algorithm for optimal bipartite matching performance. This problem serves as an excellent introduction to bipartite matching algorithms and optimization theory.
