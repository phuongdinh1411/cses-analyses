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

## 📋 Problem Description

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

## 🎯 Visual Example

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

## 🚀 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find maximum coins collectible by traversing DAG
- **Key Insight**: Use dynamic programming with topological sorting
- **Challenge**: Handle DAG structure and maximize path sum

### Step 2: Brute Force Approach
**Try all possible paths and find maximum:**

```python
def coin_collector_naive(n, m, coins, edges):
    # Build adjacency list
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

**Complexity**: O(n + m) - actually optimal for this problem

### Step 3: Optimization
**Use optimized data structures and better implementation:**

```python
def coin_collector_optimized(n, m, coins, edges):
    # Build adjacency list
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
    
    # Dynamic programming with better structure
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

### Step 4: Complete Solution

```python
def solve_coin_collector():
    n, m = map(int, input().split())
    coins = [0] + list(map(int, input().split()))
    edges = []
    for _ in range(m):
        a, b = map(int, input().split())
        edges.append((a, b))
    
    result = find_maximum_coins(n, m, coins, edges)
    print(result)

def find_maximum_coins(n, m, coins, edges):
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

if __name__ == "__main__":
    solve_coin_collector()
```

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ((4, 4, [1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (1, 4)]), 10),
        ((3, 2, [5, 3, 2], [(1, 2), (2, 3)]), 10),
        ((2, 1, [1, 2], [(1, 2)]), 3),
        ((1, 0, [5], []), 5),  # Single node
    ]
    
    for (n, m, coins, edges), expected in test_cases:
        coins_with_offset = [0] + coins
        result = find_maximum_coins(n, m, coins_with_offset, edges)
        print(f"n={n}, m={m}, coins={coins}, edges={edges}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def find_maximum_coins(n, m, coins, edges):
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
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

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - single pass through nodes and edges
- **Space**: O(n + m) - adjacency list and dynamic programming array

### Why This Solution Works
- **Topological Sorting**: Ensures we process nodes in correct dependency order
- **Dynamic Programming**: Builds optimal solution incrementally
- **DAG Property**: No cycles allow for optimal substructure
- **Greedy Choice**: Always choose maximum path to each node

## 🎨 Visual Example

### Input Example
```
4 nodes, 4 edges:
Node 1: 1 coin
Node 2: 2 coins
Node 3: 3 coins
Node 4: 4 coins

Edges: (1→2), (2→3), (3→4), (1→4)
```

### DAG Visualization
```
Nodes with coin values:
1(1) ──→ 2(2) ──→ 3(3) ──→ 4(4)
│                              │
└──────────────────────────────┘

All possible paths:
- Path 1: 1 → 2 → 3 → 4 (coins: 1+2+3+4 = 10)
- Path 2: 1 → 4 (coins: 1+4 = 5)
- Path 3: 1 → 2 → 4 (coins: 1+2+4 = 7)
```

### Topological Sorting
```
Step 1: Calculate in-degrees
- Node 1: in-degree = 0
- Node 2: in-degree = 1 (from 1)
- Node 3: in-degree = 1 (from 2)
- Node 4: in-degree = 2 (from 1, 3)

Step 2: Kahn's algorithm
- Queue: [1] (in-degree = 0)
- Process 1: remove from queue, add to result
- Update in-degrees: 2→0, 4→1
- Queue: [2]
- Process 2: remove from queue, add to result
- Update in-degrees: 3→0
- Queue: [3]
- Process 3: remove from queue, add to result
- Update in-degrees: 4→0
- Queue: [4]
- Process 4: remove from queue, add to result

Topological order: [1, 2, 3, 4]
```

### Dynamic Programming Process
```
Step 1: Initialize DP array
- dp[1] = 1 (coin at node 1)
- dp[2] = 0 (not processed yet)
- dp[3] = 0 (not processed yet)
- dp[4] = 0 (not processed yet)

Step 2: Process nodes in topological order
- Process node 1: dp[1] = 1
- Process node 2: dp[2] = max(0, dp[1] + 2) = 3
- Process node 3: dp[3] = max(0, dp[2] + 3) = 6
- Process node 4: dp[4] = max(0, dp[1] + 4, dp[3] + 4) = max(0, 5, 10) = 10

Final DP array: [1, 3, 6, 10]
Maximum coins: 10
```

### Path Reconstruction
```
From DP array: [1, 3, 6, 10]

To find the path that gives maximum coins:
- Start from node 4 (dp[4] = 10)
- Check predecessors: 1, 3
- dp[1] + 4 = 1 + 4 = 5
- dp[3] + 4 = 6 + 4 = 10 ✓
- Move to node 3
- Check predecessors: 2
- dp[2] + 3 = 3 + 3 = 6 ✓
- Move to node 2
- Check predecessors: 1
- dp[1] + 2 = 1 + 2 = 3 ✓
- Move to node 1
- No predecessors

Optimal path: 1 → 2 → 3 → 4
Total coins: 1 + 2 + 3 + 4 = 10
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP + Topo Sort  │ O(n + m)     │ O(n + m)     │ Process in   │
│                 │              │              │ dependency   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DFS + Memo      │ O(n + m)     │ O(n)         │ Recursive    │
│                 │              │              │ with cache   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ BFS + DP        │ O(n + m)     │ O(n + m)     │ Level-by-    │
│                 │              │              │ level        │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Dynamic Programming on DAG**
- Use dynamic programming with topological sorting for DAG problems
- Important for understanding
- Ensures optimal substructure
- Essential for algorithm

### 2. **Topological Sorting**
- Use Kahn's algorithm for efficient topological sorting
- Important for understanding
- Maintains dependency order
- Essential for correctness

### 3. **Maximum Path Sum**
- Use dynamic programming to find maximum path sum in DAG
- Important for understanding
- Builds optimal solution incrementally
- Essential for optimization

## 🎯 Problem Variations

### Variation 1: Coin Collector with Constraints
**Problem**: Find maximum coins with constraints on path length or node visits.

```python
def coin_collector_with_constraints(n, m, coins, edges, max_length):
    """Find maximum coins with path length constraint"""
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # DP with length constraint: dp[node][length] = max coins
    dp = [[0] * (max_length + 1) for _ in range(n + 1)]
    
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append((i, 1))  # (node, current_length)
    
    while queue:
        node, length = queue.popleft()
        if length <= max_length:
            dp[node][length] = coins[node]
            
            for neighbor in adj[node]:
                if length + 1 <= max_length:
                    dp[neighbor][length + 1] = max(
                        dp[neighbor][length + 1], 
                        dp[node][length] + coins[neighbor]
                    )
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append((neighbor, length + 1))
    
    return max(max(row) for row in dp)

# Example usage
result = coin_collector_with_constraints(4, 4, [1, 2, 3, 4], 
                                       [(1, 2), (2, 3), (3, 4), (1, 4)], 3)
print(f"Max coins with length constraint 3: {result}")
```

### Variation 2: Coin Collector with Multiple Paths
**Problem**: Find maximum coins considering multiple paths to each node.

```python
def coin_collector_multiple_paths(n, m, coins, edges):
    """Find maximum coins considering all possible paths"""
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # DP with multiple path consideration
    dp = [0] * (n + 1)
    paths = [[] for _ in range(n + 1)]
    
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
            dp[i] = coins[i]
            paths[i] = [i]
    
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            new_value = dp[node] + coins[neighbor]
            if new_value > dp[neighbor]:
                dp[neighbor] = new_value
                paths[neighbor] = paths[node] + [neighbor]
            
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Find node with maximum coins
    max_coins = max(dp)
    max_node = dp.index(max_coins)
    
    return max_coins, paths[max_node]

# Example usage
max_coins, best_path = coin_collector_multiple_paths(4, 4, [1, 2, 3, 4], 
                                                    [(1, 2), (2, 3), (3, 4), (1, 4)])
print(f"Max coins: {max_coins}, Best path: {best_path}")
```

### Variation 3: Coin Collector with Weighted Edges
**Problem**: Find maximum coins considering both node values and edge costs.

```python
def coin_collector_weighted_edges(n, m, coins, edges, edge_costs):
    """Find maximum coins considering edge costs"""
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for i, (a, b) in enumerate(edges):
        cost = edge_costs[i]
        adj[a].append((b, cost))
        in_degree[b] += 1
    
    # DP considering edge costs
    dp = [0] * (n + 1)
    
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
            dp[i] = coins[i]
    
    while queue:
        node = queue.popleft()
        
        for neighbor, cost in adj[node]:
            new_value = dp[node] + coins[neighbor] - cost
            dp[neighbor] = max(dp[neighbor], new_value)
            
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp)

# Example usage
edge_costs = [1, 1, 1, 2]  # Cost for each edge
result = coin_collector_weighted_edges(4, 4, [1, 2, 3, 4], 
                                      [(1, 2), (2, 3), (3, 4), (1, 4)], edge_costs)
print(f"Max coins with edge costs: {result}")
```

### Variation 4: Coin Collector with Time Windows
**Problem**: Find maximum coins considering time constraints for visiting nodes.

```python
def coin_collector_time_windows(n, m, coins, edges, time_windows):
    """Find maximum coins with time window constraints"""
    adj = [[] for _ in range(n + 1)]
    in_degree = [0] * (n + 1)
    
    for a, b in edges:
        adj[a].append(b)
        in_degree[b] += 1
    
    # DP with time consideration: dp[node][time] = max coins
    max_time = max(end for _, end in time_windows)
    dp = [[0] * (max_time + 1) for _ in range(n + 1)]
    
    from collections import deque
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            start, end = time_windows[i-1]
            for t in range(start, end + 1):
                dp[i][t] = coins[i]
            queue.append(i)
    
    while queue:
        node = queue.popleft()
        
        for neighbor in adj[node]:
            start, end = time_windows[neighbor-1]
            for t in range(start, end + 1):
                for prev_t in range(t):
                    if dp[node][prev_t] > 0:
                        dp[neighbor][t] = max(
                            dp[neighbor][t], 
                            dp[node][prev_t] + coins[neighbor]
                        )
            
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(max(row) for row in dp)

# Example usage
time_windows = [(0, 2), (1, 3), (2, 4), (0, 4)]  # (start_time, end_time)
result = coin_collector_time_windows(4, 4, [1, 2, 3, 4], 
                                    [(1, 2), (2, 3), (3, 4), (1, 4)], time_windows)
print(f"Max coins with time windows: {result}")
```

### Variation 5: Dynamic Coin Collector
**Problem**: Maintain maximum coins as coins are added/removed dynamically.

```python
class DynamicCoinCollector:
    def __init__(self, n):
        self.n = n
        self.coins = [0] * (n + 1)
        self.adj = [[] for _ in range(n + 1)]
        self.in_degree = [0] * (n + 1)
        self.dp = [0] * (n + 1)
    
    def add_edge(self, a, b):
        """Add edge from a to b"""
        self.adj[a].append(b)
        self.in_degree[b] += 1
        self.update_dp()
    
    def remove_edge(self, a, b):
        """Remove edge from a to b"""
        if b in self.adj[a]:
            self.adj[a].remove(b)
            self.in_degree[b] -= 1
            self.update_dp()
            return True
        return False
    
    def update_coins(self, node, new_value):
        """Update coin value at node"""
        self.coins[node] = new_value
        self.update_dp()
    
    def update_dp(self):
        """Recalculate dynamic programming values"""
        from collections import deque
        
        # Reset
        temp_in_degree = self.in_degree.copy()
        self.dp = [0] * (self.n + 1)
        
        queue = deque()
        for i in range(1, self.n + 1):
            if temp_in_degree[i] == 0:
                queue.append(i)
                self.dp[i] = self.coins[i]
        
        while queue:
            node = queue.popleft()
            
            for neighbor in self.adj[node]:
                self.dp[neighbor] = max(
                    self.dp[neighbor], 
                    self.dp[node] + self.coins[neighbor]
                )
                temp_in_degree[neighbor] -= 1
                if temp_in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
    def get_maximum_coins(self):
        """Get current maximum coins"""
        return max(self.dp)

# Example usage
collector = DynamicCoinCollector(4)
collector.update_coins(1, 1)
collector.update_coins(2, 2)
collector.update_coins(3, 3)
collector.update_coins(4, 4)

collector.add_edge(1, 2)
print(f"After adding edge (1,2): {collector.get_maximum_coins()}")

collector.add_edge(2, 3)
print(f"After adding edge (2,3): {collector.get_maximum_coins()}")

collector.add_edge(3, 4)
print(f"After adding edge (3,4): {collector.get_maximum_coins()}")
```

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
    
    # Use DP with multiple criteria
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
            move_time = times.get((node, neighbor), 0)
            move_energy = energies.get((node, neighbor), 0)
            
            new_coins = dp[node][0] + coins[neighbor]
            new_time = dp[node][1] + move_time
            new_energy = dp[node][2] + move_energy
            
            if new_coins > dp[neighbor][0]:
                dp[neighbor] = (new_coins, new_time, new_energy)
            
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dp, key=lambda x: x[0])

# Example usage
times = {(1, 2): 1, (2, 3): 2, (3, 4): 1}
energies = {(1, 2): 5, (2, 3): 3, (3, 4): 4}
result = multi_criteria_coin_collector(4, adj, coins, times, energies)
print(f"Multi-criteria result: {result}")
```

---

## 🔗 Related Problems

- **[Topological Sorting](/cses-analyses/problem_soulutions/graph_algorithms/)**: DAG ordering problems
- **[Shortest Routes I](/cses-analyses/problem_soulutions/graph_algorithms/)**: Path finding problems
- **[Building Roads](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph connectivity problems

## 📚 Learning Points

1. **Dynamic Programming on DAG**: Essential for optimal path problems in directed acyclic graphs
2. **Topological Sorting**: Important for processing nodes in dependency order
3. **Maximum Path Sum**: Key technique for optimization problems in graphs
4. **Kahn's Algorithm**: Efficient approach for topological sorting
5. **Graph Traversal**: Foundation for all graph algorithms

---

**This is a great introduction to dynamic programming on DAGs and coin collection problems!** 🎯
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