---
layout: simple
title: "Coin Collector - Maximum Path Sum in DAG"
permalink: /problem_soulutions/graph_algorithms/coin_collector_analysis
---

# Coin Collector - Maximum Path Sum in DAG

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand maximum path sum problems in DAGs and dynamic programming concepts
- Apply topological sorting and dynamic programming to find maximum path sums in DAGs
- Implement efficient DAG algorithms with proper topological ordering and DP
- Optimize DAG path sum solutions using topological sorting and dynamic programming
- Handle edge cases in DAG path problems (single nodes, disconnected components, negative values)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Topological sorting, dynamic programming, DAG algorithms, maximum path sum, DP on DAGs
- **Data Structures**: DAG representations, topological order, DP arrays, graph representations
- **Mathematical Concepts**: Graph theory, DAG properties, dynamic programming, path optimization, topological ordering
- **Programming Skills**: Topological sorting, dynamic programming, DAG traversal, algorithm implementation
- **Related Problems**: Topological Sorting (DAG algorithms), High Score (path optimization), Dynamic programming

## Problem Description

Given a directed acyclic graph (DAG) with n nodes and m edges, where each node has a coin value, find the maximum number of coins that can be collected by traversing the graph.

**Input**: 
- First line: Two integers n and m (number of nodes and edges)
- Next n lines: Integer cᵢ (coin value at node i)
- Next m lines: Two integers a and b (edge from node a to node b)

**Output**: 
- Maximum number of coins that can be collected

**Constraints**:
- 1 ≤ n ≤ 10⁵
- 1 ≤ m ≤ 2⋅10⁵
- 1 ≤ cᵢ ≤ 10⁹
- 1 ≤ a, b ≤ n
- Graph is directed and acyclic
- No self-loops or multiple edges between same pair of nodes
- Edges are unidirectional
- Nodes are numbered 1, 2, ..., n
- Find maximum coins by traversing the graph
- Each node can be visited at most once
- Must follow directed edges
- Goal is to maximize total coin collection

**Example**:
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

**Explanation**: 
- Path 1 → 2 → 3 → 4: 1 + 2 + 3 + 4 = 10
- Path 1 → 4: 1 + 4 = 5
- Maximum coins: 10 (longest path)

## Visual Example

### Input Graph
```
Nodes: 1, 2, 3, 4
Coin values: [1, 2, 3, 4]
Edges: (1→2), (2→3), (3→4), (1→4)

Graph representation:
1(1) ──> 2(2) ──> 3(3) ──> 4(4)
│                              │
└──────────────────────────────┘
```

### Dynamic Programming Process
```
Step 1: Topological sort
- Order: 1, 2, 3, 4

Step 2: Initialize DP
- dp[i] = maximum coins collectible ending at node i
- dp[1] = 1 (coin at node 1)

Step 3: Fill DP table
- Node 1: dp[1] = 1
- Node 2: dp[2] = max(dp[1] + 2, 2) = max(1 + 2, 2) = 3
- Node 3: dp[3] = max(dp[2] + 3, 3) = max(3 + 3, 3) = 6
- Node 4: dp[4] = max(dp[3] + 4, dp[1] + 4, 4) = max(6 + 4, 1 + 4, 4) = 10

Step 4: Find maximum
- Maximum coins: max(dp[1], dp[2], dp[3], dp[4]) = 10
```

### Path Analysis
```
Optimal path: 1 → 2 → 3 → 4
Coin collection:
- Node 1: 1 coin
- Node 2: 2 coins
- Node 3: 3 coins
- Node 4: 4 coins
- Total: 1 + 2 + 3 + 4 = 10 coins

Alternative paths:
- 1 → 4: 1 + 4 = 5 coins
- 1 → 2 → 3: 1 + 2 + 3 = 6 coins
```

### Key Insight
Dynamic programming with topological sort works by:
1. Processing nodes in topological order
2. For each node, considering all incoming paths
3. Taking maximum coins from all possible paths
4. Time complexity: O(n + m) for DAG traversal
5. Space complexity: O(n) for DP array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Path Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible paths in the DAG to find maximum coin collection
- Simple but computationally expensive approach
- Not suitable for large graphs
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible paths from each node
2. For each path, calculate the total coin collection
3. Return the maximum coin collection found
4. Handle cases where no path exists

**Visual Example:**
```
Brute force: Try all possible paths
For DAG: 1→2→3→4, 1→4
- Path 1: [1] → 1 coin
- Path 2: [1,2] → 1+2 = 3 coins
- Path 3: [1,2,3] → 1+2+3 = 6 coins
- Path 4: [1,2,3,4] → 1+2+3+4 = 10 coins
- Path 5: [1,4] → 1+4 = 5 coins
- Try all possible paths
```

**Implementation:**
```python
def coin_collector_brute_force(n, m, coins, edges):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
    
    def find_all_paths(start, current_path, visited):
        paths = []
        current_path.append(start)
        visited.add(start)
        
        # If no outgoing edges, this is a complete path
        if not adj[start]:
            paths.append(current_path[:])
        else:
            for neighbor in adj[start]:
                if neighbor not in visited:
                    paths.extend(find_all_paths(neighbor, current_path[:], visited.copy()))
        
        return paths
    
    max_coins = 0
    
    # Try all possible starting nodes
    for start in range(1, n + 1):
        paths = find_all_paths(start, [], set())
        for path in paths:
            total_coins = sum(coins[node] for node in path)
            max_coins = max(max_coins, total_coins)
    
    return max_coins

def solve_coin_collector_brute_force():
    n, m = map(int, input().split())
    coins = [0] + list(map(int, input().split()))
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = coin_collector_brute_force(n, m, coins, edges)
    print(result)
```

**Time Complexity:** O(n! × n) for n nodes with exponential path enumeration
**Space Complexity:** O(n) for storing paths

**Why it's inefficient:**
- O(n!) time complexity is too slow for large graphs
- Not suitable for competitive programming with n up to 10^5
- Inefficient for large inputs
- Poor performance with many nodes

### Approach 2: Basic Dynamic Programming with Topological Sort (Better)

**Key Insights from Basic DP Solution:**
- Use dynamic programming with topological sorting
- Much more efficient than brute force approach
- Standard method for DAG path problems
- Can handle larger graphs than brute force

**Algorithm:**
1. Perform topological sort on the DAG
2. Use dynamic programming to find maximum path sum
3. For each node, consider all incoming paths
4. Return the maximum coin collection

**Visual Example:**
```
Basic DP for DAG: 1→2→3→4, 1→4
- Topological order: [1, 2, 3, 4]
- DP: dp[1] = 1, dp[2] = 3, dp[3] = 6, dp[4] = 10
- Maximum: 10 coins
```

**Implementation:**
```python
def coin_collector_basic_dp(n, m, coins, edges):
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Topological sort using Kahn's algorithm
    queue = []
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Dynamic programming: dp[i] = max coins collectible ending at node i
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

def solve_coin_collector_basic():
    n, m = map(int, input().split())
    coins = [0] + list(map(int, input().split()))
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = coin_collector_basic_dp(n, m, coins, edges)
    print(result)
```

**Time Complexity:** O(n + m) for n nodes and m edges with topological sort and DP
**Space Complexity:** O(n + m) for graph representation and DP array

**Why it's better:**
- O(n + m) time complexity is much better than O(n! × n)
- Standard method for DAG path problems
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Dynamic Programming with Efficient Topological Sort (Optimal)

**Key Insights from Optimized DP Solution:**
- Use optimized topological sorting with efficient data structures
- Most efficient approach for DAG path problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized adjacency list representation
2. Perform topological sort with efficient queue operations
3. Use optimized dynamic programming with better data structures
4. Return the maximum coin collection efficiently

**Visual Example:**
```
Optimized DP for DAG: 1→2→3→4, 1→4
- Optimized topological order: [1, 2, 3, 4]
- Optimized DP: dp[1] = 1, dp[2] = 3, dp[3] = 6, dp[4] = 10
- Maximum: 10 coins
```

**Implementation:**
```python
def coin_collector_optimized_dp(n, m, coins, edges):
    # Build adjacency list and in-degree
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # Topological sort using Kahn's algorithm with deque
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Dynamic programming with optimized structure
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

def solve_coin_collector():
    n, m = map(int, input().split())
    coins = [0] + list(map(int, input().split()))
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = coin_collector_optimized_dp(n, m, coins, edges)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_coin_collector()
```

**Time Complexity:** O(n + m) for n nodes and m edges with optimized topological sort and DP
**Space Complexity:** O(n + m) for graph representation and DP array

**Why it's optimal:**
- O(n + m) time complexity is optimal for DAG path problems
- Uses optimized topological sorting with efficient data structures
- Most efficient approach for competitive programming
- Standard method for DAG path optimization

## 🎯 Problem Variations

### Variation 1: Coin Collector with Multiple Starting Points
**Problem**: Find maximum coins starting from any node.

**Link**: [CSES Problem Set - Coin Collector Multiple Starts](https://cses.fi/problemset/task/coin_collector_multiple_starts)

```python
def coin_collector_multiple_starts(n, m, coins, edges):
    # Build adjacency list and in-degree
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
    
    # Dynamic programming: dp[i] = max coins collectible ending at node i
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

### Variation 2: Coin Collector with Path Length Constraints
**Problem**: Find maximum coins with path length constraints.

**Link**: [CSES Problem Set - Coin Collector Path Length](https://cses.fi/problemset/task/coin_collector_path_length)

```python
def coin_collector_path_length(n, m, coins, edges, max_length):
    # Build adjacency list and in-degree
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
    
    # Dynamic programming with path length constraint
    # dp[i][j] = max coins collectible ending at node i with path length j
    dp = [[0] * (max_length + 1) for _ in range(n + 1)]
    
    while queue:
        node = queue.popleft()
        dp[node][1] = coins[node]  # Base case: path length 1
        
        for neighbor in adj[node]:
            for length in range(1, max_length):
                if dp[node][length] > 0:
                    dp[neighbor][length + 1] = max(dp[neighbor][length + 1], dp[node][length] + coins[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    max_coins = 0
    for i in range(1, n + 1):
        for j in range(1, max_length + 1):
            max_coins = max(max_coins, dp[i][j])
    
    return max_coins
```

### Variation 3: Coin Collector with Negative Coins
**Problem**: Find maximum coins with negative coin values.

**Link**: [CSES Problem Set - Coin Collector Negative Coins](https://cses.fi/problemset/task/coin_collector_negative_coins)

```python
def coin_collector_negative_coins(n, m, coins, edges):
    # Build adjacency list and in-degree
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
    
    # Dynamic programming with negative values
    dp = [float('-inf')] * (n + 1)
    
    while queue:
        node = queue.popleft()
        dp[node] = coins[node]  # Base case: collect coins at current node
        
        for neighbor in adj[node]:
            dp[neighbor] = max(dp[neighbor], dp[node] + coins[neighbor])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp)
```

## 🔗 Related Problems

- **[Topological Sorting](/cses-analyses/problem_soulutions/graph_algorithms/topological_sorting_analysis/)**: DAG algorithms
- **[High Score](/cses-analyses/problem_soulutions/graph_algorithms/high_score_analysis/)**: Path optimization
- **[Dynamic Programming](/cses-analyses/problem_soulutions/dynamic_programming/)**: DP problems
- **[DAG Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: DAG problems

## 📚 Learning Points

1. **Dynamic Programming on DAGs**: Essential for understanding path optimization problems
2. **Topological Sorting**: Key technique for processing DAGs
3. **DAG Properties**: Important for understanding graph structure
4. **Path Optimization**: Critical for understanding optimization problems
5. **Maximum Path Sum**: Foundation for many graph algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Coin Collector problem demonstrates fundamental dynamic programming concepts for finding optimal path solutions in DAGs. We explored three approaches:

1. **Brute Force Path Enumeration**: O(n! × n) time complexity using exponential path generation, inefficient for large graphs
2. **Basic Dynamic Programming with Topological Sort**: O(n + m) time complexity using standard DP and topological sort, better approach for DAG path problems
3. **Optimized Dynamic Programming with Efficient Topological Sort**: O(n + m) time complexity with optimized DP and topological sort, optimal approach for DAG path optimization

The key insights include understanding dynamic programming principles, using topological sorting for efficient DAG processing, and applying path optimization techniques for optimal performance. This problem serves as an excellent introduction to dynamic programming on DAGs and path optimization algorithms.

