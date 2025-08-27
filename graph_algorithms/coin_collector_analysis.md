# CSES Coin Collector - Problem Analysis

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