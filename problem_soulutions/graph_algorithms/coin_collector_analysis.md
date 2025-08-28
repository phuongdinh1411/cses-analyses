---
layout: simple
title: "Coin Collector
permalink: /problem_soulutions/graph_algorithms/coin_collector_analysis/"
---


# Coin Collector

## Problem Statement
Given a directed acyclic graph (DAG) with n nodes and m edges, where each node has a coin value, find the maximum number of coins that can be collected by traversing the graph.

### Input
The first input line has two integers n and m: the number of nodes and edges.
Then there are n lines with coin values. The i-th line has an integer c_i: the coin value at node i.
Then there are m lines describing the edges. Each line has two integers a and b: there is an edge from node a to node b.

### Output
Print the maximum number of coins that can be collected.

### Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ m ≤ 2⋅10^5
- 1 ≤ c_i ≤ 10^9
- 1 ≤ a,b ≤ n

### Example
```
Input:
4 4
1 2 3 4
1 2
2 3
3 4
1 4

Output:
10
```

## Solution Progression

### Approach 1: Dynamic Programming on DAG - O(n + m)
**Description**: Use dynamic programming with topological sorting to find maximum path sum.

```python
def coin_collector_naive(n, m, coins, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1"
    # Topological sort using Kahn's algorithm
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Dynamic programming: dp[i] = max coins collectible starting from node i
    dp = [0] * (n + 1)
    
    while queue:
        node = queue.pop(0)
        dp[node] = coins[node]  # Base case: collect coins at current node
        
        for neighbor in adj[node]:
            # Update dp[neighbor] with maximum value
            dp[neighbor] = max(dp[neighbor], dp[node] + coins[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp)
```

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized DP on DAG - O(n + m)
**Description**: Use optimized dynamic programming with better topological sorting.

```python
def coin_collector_optimized(n, m, coins, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Topological sort using Kahn's algorithm
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Dynamic programming
    dp = [0] * (n + 1)
    
    while queue:
        node = queue.popleft()
        dp[node] = coins[node]
        
        for neighbor in adj[node]:
            dp[neighbor] = max(dp[neighbor], dp[node] + coins[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp)
```

**Why this improvement works**: We use dynamic programming with optimized topological sorting to find maximum path sum efficiently.

## Final Optimal Solution

```python
from collections import deque

n, m = map(int, input().split())
coins = [0] + list(map(int, input().split()))
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))

def find_maximum_coins(n, m, coins, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Topological sort using Kahn's algorithm
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Dynamic programming
    dp = [0] * (n + 1)
    
    while queue:
        node = queue.popleft()
        dp[node] = coins[node]
        
        for neighbor in adj[node]:
            dp[neighbor] = max(dp[neighbor], dp[node] + coins[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp)

result = find_maximum_coins(n, m, coins, edges)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DP on DAG | O(n + m) | O(n + m) | Use dynamic programming on topological order |
| Optimized DP | O(n + m) | O(n + m) | Optimized DP implementation |

## Key Insights for Other Problems

### 1. **Dynamic Programming on DAG**
**Principle**: Use dynamic programming with topological sorting for DAG problems.
**Applicable to**: DAG problems, path problems, optimization problems

### 2. **Topological Sorting**
**Principle**: Use Kahn's algorithm or DFS for topological sorting.
**Applicable to**: DAG problems, dependency problems, ordering problems

### 3. **Maximum Path Sum**
**Principle**: Use dynamic programming to find maximum path sum in DAG.
**Applicable to**: Path problems, optimization problems, graph problems

## Notable Techniques

### 1. **Dynamic Programming on DAG**
```python
def dp_on_dag(n, adj, values):
    # Topological sort
    in_degree = [0] * (n + 1)
    for u in range(1, n + 1):
        for v in adj[u]:
            in_degree[v] += 1
    
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # DP
    dp = [0] * (n + 1)
    while queue:
        node = queue.popleft()
        dp[node] = values[node]
        
        for neighbor in adj[node]:
            dp[neighbor] = max(dp[neighbor], dp[node] + values[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return dp
```

### 2. **Kahn's Algorithm**
```python
def kahn_algorithm(n, adj):
    in_degree = [0] * (n + 1)
    for u in range(1, n + 1):
        for v in adj[u]:
            in_degree[v] += 1
    
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

### 3. **Maximum Path Sum**
```python
def max_path_sum_dag(n, adj, values):
    dp = [0] * (n + 1)
    in_degree = [0] * (n + 1)
    
    for u in range(1, n + 1):
        for v in adj[u]:
            in_degree[v] += 1
    
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    while queue:
        node = queue.popleft()
        dp[node] = values[node]
        
        for neighbor in adj[node]:
            dp[neighbor] = max(dp[neighbor], dp[node] + values[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a dynamic programming on DAG problem
2. **Choose approach**: Use dynamic programming with topological sorting
3. **Build graph**: Create adjacency list and calculate in-degrees
4. **Topological sort**: Use Kahn's algorithm to get topological order
5. **Dynamic programming**: Calculate maximum path sum for each node
6. **Return result**: Output maximum value from all nodes

---

*This analysis shows how to efficiently find maximum path sum in a DAG using dynamic programming.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Coin Collector with Costs**
**Problem**: Each move has a cost, find maximum profit (coins - costs) path.
```python
def cost_based_coin_collector(n, adj, coins, costs):
    # costs[(a, b)] = cost of moving from a to b
    
    # Calculate in-degrees
    in_degree = [0] * (n + 1)
    for u in range(1, n + 1):
        for v in adj[u]:
            in_degree[v] += 1
    
    # Use DP with cost tracking
    dp = [float('-inf')] * (n + 1)
    
    # Find starting nodes (in-degree 0)
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
            dp[i] = coins[i]  # Start with coin value
    
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            cost = costs.get((node, neighbor), 0)
            # Update profit: current profit + neighbor coins - move cost
            dp[neighbor] = max(dp[neighbor], dp[node] + coins[neighbor] - cost)
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp)
```

#### **Variation 2: Coin Collector with Constraints**
**Problem**: Find maximum coin collection with constraints on path length or node visits.
```python
def constrained_coin_collector(n, adj, coins, constraints):
    # constraints = {'max_length': x, 'forbidden_nodes': [nodes], 'required_nodes': [nodes]}
    
    # Calculate in-degrees
    in_degree = [0] * (n + 1)
    for u in range(1, n + 1):
        for v in adj[u]:
            in_degree[v] += 1
    
    # Use DP with constraint checking
    dp = [float('-inf')] * (n + 1)
    
    # Find starting nodes
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0 and i not in constraints.get('forbidden_nodes', []):
            queue.append(i)
            dp[i] = coins[i]
    
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            # Check constraints
            if neighbor in constraints.get('forbidden_nodes', []):
                continue
            
            dp[neighbor] = max(dp[neighbor], dp[node] + coins[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all required nodes are reachable
    required_nodes = constraints.get('required_nodes', [])
    for node in required_nodes:
        if dp[node] == float('-inf'):
            return -1  # Impossible
    
    return max(dp)
```

#### **Variation 3: Coin Collector with Probabilities**
**Problem**: Each coin has a probability of being collected, find expected maximum collection.
```python
def probabilistic_coin_collector(n, adj, coins, probabilities):
    # probabilities[i] = probability of collecting coin at node i
    
    # Calculate in-degrees
    in_degree = [0] * (n + 1)
    for u in range(1, n + 1):
        for v in adj[u]:
            in_degree[v] += 1
    
    # Use DP with probability tracking
    dp = [0.0] * (n + 1)
    
    # Find starting nodes
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
            dp[i] = coins[i] * probabilities[i]  # Expected value
    
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            expected_coin = coins[neighbor] * probabilities[neighbor]
            dp[neighbor] = max(dp[neighbor], dp[node] + expected_coin)
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp)
```

#### **Variation 4: Coin Collector with Multiple Criteria**
**Problem**: Find path optimizing multiple objectives (coins, time, energy).
```python
def multi_criteria_coin_collector(n, adj, coins, times, energies):
    # times[(a, b)] = time to move from a to b, energies[(a, b)] = energy cost
    
    # Calculate in-degrees
    in_degree = [0] * (n + 1)
    for u in range(1, n + 1):
        for v in adj[u]:
            in_degree[v] += 1
    
    # Normalize values
    max_coins = max(coins) if coins else 1
    max_time = max(times.values()) if times else 1
    max_energy = max(energies.values()) if energies else 1
    
    # Use DP with multi-criteria tracking
    dp = [(0, 0, 0)] * (n + 1)  # (coins, time, energy)
    
    # Find starting nodes
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
            dp[i] = (coins[i], 0, 0)
    
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            time_cost = times.get((node, neighbor), 0)
            energy_cost = energies.get((node, neighbor), 0)
            
            new_coins = dp[node][0] + coins[neighbor]
            new_time = dp[node][1] + time_cost
            new_energy = dp[node][2] + energy_cost
            
            # Weighted score (higher is better)
            current_score = (new_coins / max_coins - new_time / max_time - new_energy / max_energy)
            existing_score = (dp[neighbor][0] / max_coins - dp[neighbor][1] / max_time - dp[neighbor][2] / max_energy)
            
            if current_score > existing_score:
                dp[neighbor] = (new_coins, new_time, new_energy)
            
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp, key=lambda x: x[0])  # Return maximum coins
```

#### **Variation 5: Coin Collector with Dynamic Updates**
**Problem**: Handle dynamic updates to coin values and find maximum collection after each update.
```python
def dynamic_coin_collector(n, adj, initial_coins, updates):
    # updates = [(node, new_coin_value), ...]
    
    coins = initial_coins.copy()
    results = []
    
    for node, new_value in updates:
        # Update coin value
        coins[node] = new_value
        
        # Recompute maximum collection
        # Calculate in-degrees
        in_degree = [0] * (n + 1)
        for u in range(1, n + 1):
            for v in adj[u]:
                in_degree[v] += 1
        
        # Use DP
        dp = [0] * (n + 1)
        
        # Find starting nodes
        queue = deque()
        for i in range(1, n + 1):
            if in_degree[i] == 0:
                queue.append(i)
                dp[i] = coins[i]
        
        while queue:
            node = queue.popleft()
            
            for neighbor in adj[node]:
                dp[neighbor] = max(dp[neighbor], dp[node] + coins[neighbor])
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        results.append(max(dp))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Dynamic Programming Problems**
- **DAG DP**: Dynamic programming on directed acyclic graphs
- **Path Problems**: Find optimal paths in graphs
- **Optimization Problems**: Optimize objective functions
- **State Compression**: Compress states efficiently

#### **2. Graph Theory Problems**
- **Topological Sorting**: Order nodes in DAG
- **Path Finding**: Find paths with specific properties
- **Connectivity**: Study graph connectivity
- **Traversal**: Various graph traversal algorithms

#### **3. Optimization Problems**
- **Maximum Path Sum**: Find path with maximum sum
- **Minimum Path Sum**: Find path with minimum sum
- **Multi-objective**: Optimize multiple objectives
- **Constrained**: Optimization with constraints

#### **4. Algorithmic Problems**
- **Kahn's Algorithm**: Topological sorting algorithm
- **DFS**: Depth-first search for path finding
- **BFS**: Breadth-first search for path finding
- **Graph Algorithms**: Various graph algorithms

#### **5. Combinatorial Problems**
- **Path Counting**: Count different paths
- **Path Enumeration**: Enumerate all paths
- **Subset Problems**: Problems involving subsets
- **Permutation Problems**: Problems involving permutations

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Graphs**
```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    coins = list(map(int, input().split()))
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
    
    result = coin_collector(n, adj, coins)
    print(result)
```

#### **2. Range Queries on Coin Collection**
```python
def range_coin_collector_queries(n, adj, coins, queries):
    # queries = [(start_node, end_node), ...] - find max collection from start to end
    
    results = []
    for start, end in queries:
        # Modify graph to have only nodes from start to end
        modified_adj = [[] for _ in range(n + 1)]
        for u in range(1, n + 1):
            if start <= u <= end:
                for v in adj[u]:
                    if start <= v <= end:
                        modified_adj[u].append(v)
        
        result = coin_collector(end - start + 1, modified_adj, coins[start-1:end])
        results.append(result)
    
    return results
```

#### **3. Interactive Coin Collector Problems**
```python
def interactive_coin_collector():
    n, m = map(int, input("Enter n and m: ").split())
    coins = list(map(int, input("Enter coin values: ").split()))
    print("Enter edges (a b):")
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
    
    result = coin_collector(n, adj, coins)
    print(f"Maximum coin collection: {result}")
    
    # Show the path
    path = find_optimal_path(n, adj, coins)
    print(f"Optimal path: {' -> '.join(map(str, path))}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **DAG Properties**: Properties of directed acyclic graphs
- **Path Theory**: Mathematical theory of paths
- **Connectivity Theory**: Theory of graph connectivity
- **Topology**: Topological properties of graphs

#### **2. Optimization Theory**
- **Linear Programming**: LP formulation of path problems
- **Dynamic Programming**: Mathematical foundations of DP
- **Multi-objective Optimization**: Multiple objectives
- **Constrained Optimization**: Optimization with constraints

#### **3. Combinatorics**
- **Path Counting**: Mathematical counting of paths
- **Graph Enumeration**: Enumerate graphs with properties
- **Permutation Theory**: Theory of permutations
- **Optimization Theory**: Mathematical optimization

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Dynamic Programming**: DAG DP, state compression
- **Graph Algorithms**: Topological sort, path finding
- **Optimization Algorithms**: Linear programming, integer programming
- **Combinatorial Algorithms**: Enumeration, counting algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Optimization**: Mathematical optimization techniques
- **Combinatorics**: Combinatorial mathematics
- **Linear Algebra**: Matrix representations of graphs

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **Dynamic Programming**: Optimal substructure, overlapping subproblems
- **State Management**: Efficient state representation
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient DAG dynamic programming techniques and shows various extensions for coin collection problems.* 